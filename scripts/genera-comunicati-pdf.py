#!/usr/bin/env python3
"""Genera il PDF di ogni comunicato stampa dalla sua pagina del sito (carta intestata in stampa).
Costruisce il sito con Hugo in una cartella temporanea, stampa la pagina in A4 con Chromium e aggiunge cornice di microtesto (come immagine) e metadati.

Uso:
  python3 scripts/genera-comunicati-pdf.py                  # tutti i comunicati con `pdf:`
  python3 scripts/genera-comunicati-pdf.py SLUG [SLUG ...]  # solo quelli indicati
  python3 scripts/genera-comunicati-pdf.py --check          # controlla i PDF esistenti, non rigenera

I comunicati stanno in content/sala-stampa/comunicati/*.md; il campo `pdf:` del
front matter dice dove scrivere il file dentro static/ (di norma
/comunicati/AAAA/<slug>.pdf, la cartella canonica dei comunicati, rule 04c).
L'aspetto viene dalle regole @media print di
themes/flavour-pcgenzano/static/css/comunicati-stampa.css: lo stesso foglio che
esce stampando la pagina dal browser.

Che cosa fa, per ogni comunicato:
  1. costruisce il sito con Hugo (baseURL di produzione) in una cartella
     temporanea, mai in public/;
  2. lo serve su 127.0.0.1 su una porta libera e blocca ogni richiesta verso
     altri indirizzi (il PDF non dipende dalla rete);
  3. apre la pagina con Chromium (Playwright, browser già installato) e la
     stampa in A4 con i tag di accessibilità (tagged), gli sfondi e le misure
     di pagina del CSS;
  4. con pikepdf: segna come artefatti i contenuti fuori dalla struttura (piè di
     pagina), aggiunge lungo i bordi la cornice di microtesto del Gruppo come
     immagine (non è testo: non finisce nel testo copiato né nella lettura con
     lo screen reader; regola grafica.md), imposta titolo, autore, oggetto,
     lingua it-IT e metadati XMP senza nomi di programmi.

Con --check verifica per ogni comunicato che il PDF esista, abbia i tag, la
lingua it-IT, il titolo uguale a quello del comunicato e metadati senza nomi di
programmi; esce con 1 se qualcosa non va.

Dipendenze: hugo, playwright (Python) con Chromium, pikepdf, Pillow, PyYAML.
"""

from __future__ import annotations

import argparse
import datetime as dt
import functools
import http.server
import importlib.util
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import zlib
from pathlib import Path

import pikepdf
import yaml
from PIL import Image

RADICE = Path(__file__).resolve().parent.parent
CARTELLA = RADICE / "content" / "sala-stampa" / "comunicati"
BASE_PRODUZIONE = "https://www.protezionecivilegenzano.it/"
ENTE = "Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma"
LINGUA = "it-IT"
FUSO = dt.timezone(dt.timedelta(hours=2))  # le date dei comunicati sono in ora italiana

# Nomi di programmi che non devono comparire nei metadati del PDF.
PROGRAMMI = re.compile(r"\b(chromium|chrome|skia|pikepdf|qpdf|libreoffice|openoffice|playwright|"
                       r"puppeteer|hugo|weasyprint|reportlab|ghostscript|pdftex|cairo)\b", re.I)

# Cornice di microtesto: misure in millimetri sulla carta, risoluzione dell'immagine.
CORNICE_DPI = 450
CORNICE_MARGINE_MM = 4.5      # distanza del bordo esterno della striscia dal bordo del foglio
CORNICE_CORPO_MM = 0.95       # altezza del carattere
CORNICE_COLORE = (0, 51, 102)  # #003366
CORNICE_INTENSITA = 0.5       # opacità del microtesto sul bianco della carta

OPERATORI_DISEGNO = {"Tj", "TJ", "'", '"', "S", "s", "f", "F", "f*", "B", "B*",
                     "b", "b*", "sh", "Do"}


# ── Front matter ────────────────────────────────────────────────────────────

def leggi_front_matter(percorso: Path) -> dict:
    testo = percorso.read_text(encoding="utf-8")
    if not testo.startswith("---"):
        return {}
    fine = testo.find("\n---", 3)
    if fine < 0:
        return {}
    return yaml.safe_load(testo[3:fine]) or {}


def comunicati(slug_richiesti: list[str]) -> list[dict]:
    elenco = []
    for f in sorted(CARTELLA.glob("*.md")):
        if f.name == "_index.md":
            continue
        fm = leggi_front_matter(f)
        if not fm.get("pdf"):
            continue
        slug = fm.get("slug") or f.stem
        if slug_richiesti and slug not in slug_richiesti and f.stem not in slug_richiesti:
            continue
        data = fm.get("date")
        if isinstance(data, str):
            data = dt.datetime.fromisoformat(data)
        if isinstance(data, dt.date) and not isinstance(data, dt.datetime):
            data = dt.datetime(data.year, data.month, data.day, 12, 0, tzinfo=FUSO)
        if data.tzinfo is None:
            data = data.replace(tzinfo=FUSO)
        elenco.append({
            "file": f,
            "slug": slug,
            "titolo": str(fm.get("title", "")).strip(),
            "sottotitolo": str(fm.get("sottotitolo", "") or fm.get("description", "")).strip(),
            "data": data,
            "pdf": str(fm["pdf"]),
            "url": f"/sala-stampa/comunicati/{slug}/",
        })
    mancanti = [s for s in slug_richiesti
                if not any(s in (c["slug"], c["file"].stem) for c in elenco)]
    if mancanti:
        sys.exit(f"Comunicati non trovati (o senza `pdf:`): {', '.join(mancanti)}")
    return elenco


# ── Cornice di microtesto ───────────────────────────────────────────────────

def modulo_cornice():
    spec = importlib.util.spec_from_file_location(
        "microtesto_cornice", RADICE / "scripts" / "microtesto_cornice.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _immagine_pdf(pdf: pikepdf.Pdf, maschera: Image.Image) -> pikepdf.Stream:
    """Immagine XObject in tinta unita #003366 con la maschera come trasparenza."""
    w, h = maschera.size
    smask = pikepdf.Stream(pdf, zlib.compress(maschera.tobytes(), 9))
    smask.Type = pikepdf.Name.XObject
    smask.Subtype = pikepdf.Name.Image
    smask.Width, smask.Height = w, h
    smask.ColorSpace = pikepdf.Name.DeviceGray
    smask.BitsPerComponent = 8
    smask.Filter = pikepdf.Name.FlateDecode
    tinta = bytes(CORNICE_COLORE) * (w * h)
    img = pikepdf.Stream(pdf, zlib.compress(tinta, 9))
    img.Type = pikepdf.Name.XObject
    img.Subtype = pikepdf.Name.Image
    img.Width, img.Height = w, h
    img.ColorSpace = pikepdf.Name.DeviceRGB
    img.BitsPerComponent = 8
    img.Filter = pikepdf.Name.FlateDecode
    img.SMask = pdf.make_indirect(smask)
    return pdf.make_indirect(img)


def prepara_cornice(pdf: pikepdf.Pdf, larghezza_pt: float, altezza_pt: float, anno: int) -> dict:
    mc = modulo_cornice()
    px_mm = CORNICE_DPI / 25.4
    corpo = max(8, round(CORNICE_CORPO_MM * px_mm))
    spessore = corpo + 4
    spessore_mm = spessore / px_mm
    font = mc._font(corpo)
    testo = mc.TESTO_BASE.format(anno=anno)
    w_mm = larghezza_pt / 72 * 25.4
    h_mm = altezza_pt / 72 * 25.4
    lung_o_mm = w_mm - 2 * (CORNICE_MARGINE_MM + spessore_mm)
    lung_v_mm = h_mm - 2 * (CORNICE_MARGINE_MM + spessore_mm)

    def maschera(lung_mm: float) -> Image.Image:
        m = mc._striscia(round(lung_mm * px_mm), spessore, testo, font)
        return m.point(lambda v: round(v * CORNICE_INTENSITA))

    orizzontale = maschera(lung_o_mm)
    verticale = maschera(lung_v_mm)
    return {
        "img_o": _immagine_pdf(pdf, orizzontale),
        "img_s": _immagine_pdf(pdf, verticale.rotate(90, expand=True)),   # sinistra, dal basso
        "img_d": _immagine_pdf(pdf, verticale.rotate(-90, expand=True)),  # destra, dall'alto
        "spessore_mm": spessore_mm,
        "lung_o_mm": lung_o_mm,
        "lung_v_mm": lung_v_mm,
    }


def applica_cornice(pdf: pikepdf.Pdf, pagina: pikepdf.Page, cornice: dict) -> None:
    pt = 72 / 25.4
    box = [float(v) for v in pagina.mediabox]
    w_pt, h_pt = box[2] - box[0], box[3] - box[1]
    m, s = CORNICE_MARGINE_MM * pt, cornice["spessore_mm"] * pt
    lo, lv = cornice["lung_o_mm"] * pt, cornice["lung_v_mm"] * pt
    n_o = pagina.add_resource(cornice["img_o"], pikepdf.Name.XObject, prefix="CsCornO")
    n_s = pagina.add_resource(cornice["img_s"], pikepdf.Name.XObject, prefix="CsCornS")
    n_d = pagina.add_resource(cornice["img_d"], pikepdf.Name.XObject, prefix="CsCornD")
    x0, y0 = box[0], box[1]

    def disegna(nome, w, h, x, y):
        return f"q {w:.3f} 0 0 {h:.3f} {x0 + x:.3f} {y0 + y:.3f} cm {nome} Do Q\n"

    flusso = "q\n/Artifact BMC\n"
    flusso += disegna(n_o, lo, s, m + s, h_pt - m - s)   # alto
    flusso += disegna(n_o, lo, s, m + s, m)              # basso
    flusso += disegna(n_s, s, lv, m, m + s)              # sinistra
    flusso += disegna(n_d, s, lv, w_pt - m - s, m + s)   # destra
    flusso += "EMC\nQ\n"
    # Il contenuto della pagina viene chiuso fra q/Q: la cornice parte dal
    # sistema di coordinate iniziale, qualunque trasformazione resti aperta.
    pagina.contents_add(pikepdf.Stream(pdf, b"q\n"), prepend=True)
    pagina.contents_add(pikepdf.Stream(pdf, b"Q\n"), prepend=False)
    pagina.contents_add(pikepdf.Stream(pdf, flusso.encode("ascii")), prepend=False)


# ── Artefatti: contenuto fuori dalla struttura dei tag ──────────────────────

def _operatore(istr) -> str | None:
    if isinstance(istr, pikepdf.ContentStreamInlineImage):
        return "BI"
    return str(istr.operator)


COSTRUZIONE_TRACCIATO = {"m", "l", "c", "v", "y", "h", "re"}


def segna_artefatti(pdf: pikepdf.Pdf, pagina: pikepdf.Page) -> int:
    """Racchiude in /Artifact BMC … EMC il contenuto disegnato fuori da ogni
    sequenza marcata (sfondo della pagina, piè di pagina). Le sequenze marcate
    devono restare annidate correttamente con q/Q e BT/ET: si racchiudono
    quindi blocchi q … Q completi, testi BT … ET completi o singoli tracciati,
    mai pezzi a cavallo. Restituisce quanti operatori di disegno restano fuori
    sia dalla struttura sia dagli artefatti."""
    istr = list(pikepdf.parse_content_stream(pagina))
    ops = [_operatore(i) for i in istr]
    n = len(ops)
    marcato = [0] * n          # profondità delle sequenze marcate prima di ogni istruzione
    livello = 0
    for i, op in enumerate(ops):
        if op == "EMC":
            livello -= 1
        marcato[i] = livello
        if op in ("BDC", "BMC"):
            livello += 1
            marcato[i] = livello
    # Coppie q/Q e BT/ET.
    coppie = []
    pila_q, pila_t = [], []
    for i, op in enumerate(ops):
        if op == "q":
            pila_q.append(i)
        elif op == "Q" and pila_q:
            coppie.append((pila_q.pop(), i))
        elif op == "BT":
            pila_t.append(i)
        elif op == "ET" and pila_t:
            coppie.append((pila_t.pop(), i))

    def fuori_marcatura(a: int, b: int) -> bool:
        return all(marcato[k] == 0 and ops[k] not in ("BDC", "BMC", "EMC") for k in range(a, b + 1))

    def bilanciato(a: int, b: int) -> bool:
        seg = ops[a:b + 1]
        return seg.count("q") == seg.count("Q") and seg.count("BT") == seg.count("ET")

    disegno = {i for i, op in enumerate(ops)
               if marcato[i] == 0 and (op in OPERATORI_DISEGNO or op == "BI")}
    intervalli = []
    # 1. blocchi q … Q e BT … ET interi, fuori da ogni marcatura, i più ampi possibile
    for a, b in sorted(coppie, key=lambda c: c[0] - c[1]):
        if any(a >= x and b <= y for x, y in intervalli):
            continue
        if fuori_marcatura(a, b) and bilanciato(a, b) and any(a <= k <= b for k in disegno):
            intervalli.append((a, b))
    # 2. tracciati e immagini rimasti scoperti, al livello del flusso
    coperto = lambda k: any(x <= k <= y for x, y in intervalli)
    for k in sorted(disegno):
        if coperto(k):
            continue
        if ops[k] in ("Do", "sh", "BI"):
            intervalli.append((k, k))
        elif ops[k] not in ("Tj", "TJ", "'", '"'):
            a = k
            while a > 0 and ops[a - 1] in COSTRUZIONE_TRACCIATO and marcato[a - 1] == 0:
                a -= 1
            intervalli.append((a, k))
    inizio = {a for a, _ in intervalli}
    fine = {b for _, b in intervalli}
    uscita = []
    for i, x in enumerate(istr):
        if i in inizio:
            uscita.append(pikepdf.ContentStreamInstruction(
                [pikepdf.Name("/Artifact")], pikepdf.Operator("BMC")))
        uscita.append(x)
        if i in fine:
            uscita.append(pikepdf.ContentStreamInstruction([], pikepdf.Operator("EMC")))
    pagina.obj.Contents = pdf.make_stream(pikepdf.unparse_content_stream(uscita))
    return conta_fuori_struttura(pagina)


def conta_fuori_struttura(pagina: pikepdf.Page) -> int:
    livello, fuori = 0, 0
    for istr in pikepdf.parse_content_stream(pagina):
        op = _operatore(istr)
        if op in ("BDC", "BMC"):
            livello += 1
        elif op == "EMC":
            livello -= 1
        elif livello == 0 and (op in OPERATORI_DISEGNO or op == "BI"):
            fuori += 1
    return fuori


# ── Metadati ────────────────────────────────────────────────────────────────

def data_pdf(d: dt.datetime) -> str:
    off = d.utcoffset() or dt.timedelta(0)
    minuti = int(off.total_seconds() // 60)
    segno = "+" if minuti >= 0 else "-"
    return d.strftime("D:%Y%m%d%H%M%S") + f"{segno}{abs(minuti) // 60:02d}'{abs(minuti) % 60:02d}'"


def imposta_metadati(pdf: pikepdf.Pdf, c: dict) -> None:
    for chiave in list(pdf.docinfo.keys()):
        del pdf.docinfo[chiave]
    pdf.docinfo["/Title"] = c["titolo"]
    pdf.docinfo["/Author"] = ENTE
    pdf.docinfo["/Subject"] = c["sottotitolo"]
    pdf.docinfo["/Keywords"] = "comunicato stampa; protezione civile; Genzano di Roma"
    pdf.docinfo["/Creator"] = ENTE
    pdf.docinfo["/Producer"] = ENTE
    pdf.docinfo["/CreationDate"] = data_pdf(c["data"])
    pdf.docinfo["/ModDate"] = data_pdf(c["data"])
    if "/Metadata" in pdf.Root:
        del pdf.Root["/Metadata"]
    with pdf.open_metadata(set_pikepdf_as_editor=False, update_docinfo=False) as meta:
        meta["dc:title"] = c["titolo"]
        meta["dc:creator"] = [ENTE]
        meta["dc:description"] = c["sottotitolo"]
        meta["dc:rights"] = (f"{ENTE}. Le testate possono pubblicare il comunicato, in tutto "
                             "o in parte, citando la fonte; per gli altri usi vale la licenza "
                             "CC BY-NC-SA 4.0 del sito.")
        meta["dc:language"] = [LINGUA]
        meta["pdf:Producer"] = ENTE
        meta["pdf:Keywords"] = str(pdf.docinfo["/Keywords"])
        meta["xmp:CreatorTool"] = ENTE
        meta["xmp:CreateDate"] = c["data"].isoformat()
        meta["xmp:ModifyDate"] = c["data"].isoformat()
    pdf.Root.Lang = pikepdf.String(LINGUA)
    vp = pdf.Root.get("/ViewerPreferences")
    if vp is None:
        pdf.Root.ViewerPreferences = pikepdf.Dictionary(DisplayDocTitle=True)
    else:
        vp.DisplayDocTitle = True


# ── Costruzione, server, stampa ─────────────────────────────────────────────

def costruisci_sito(cartella: Path, hugo: str) -> Path:
    dest = cartella / "sito"
    cmd = [hugo, "--logLevel", "error", "--minify", "--baseURL", BASE_PRODUZIONE,
           "--destination", str(dest), "--cacheDir", str(cartella / "cache")]
    r = subprocess.run(cmd, cwd=RADICE, capture_output=True, text=True)
    if r.returncode != 0 or "ERROR" in (r.stdout + r.stderr):
        sys.stderr.write(r.stdout + r.stderr)
        sys.exit("La build di Hugo non è andata a buon fine.")
    return dest


class _Silenzioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):  # niente righe di log per ogni file servito
        pass


def avvia_server(cartella: Path):
    gestore = functools.partial(_Silenzioso, directory=str(cartella))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), gestore)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


def stampa(browser, base: str, c: dict) -> bytes:
    pagina = browser.new_page()
    try:
        pagina.route("**/*", lambda r: r.continue_() if r.request.url.startswith(base) else r.abort())
        pagina.goto(base + c["url"], wait_until="load")
        # Prima il foglio di stampa, poi l'attesa dei caratteri: Titillium Web
        # si scarica solo quando le regole di stampa lo chiedono.
        pagina.emulate_media(media="print")
        pagina.evaluate("document.fonts.load('400 10pt \"Titillium Web Stampa\"')"
                        ".then(() => document.fonts.load('700 10pt \"Titillium Web Stampa\"'))"
                        ".then(() => document.fonts.load('600 10pt \"Titillium Web Stampa\"'))"
                        ".then(() => document.fonts.ready).then(() => true)")
        pagina.wait_for_function("Array.from(document.images).filter(i => i.offsetParent !== null)"
                                 ".every(i => i.complete && i.naturalWidth > 0)", timeout=15000)
        trabocca = pagina.evaluate("""() => {
            const c = document.querySelector('.cs-pagina .col-lg-8');
            if (!c) return 'manca il contenitore del comunicato';
            const fuori = [...c.querySelectorAll('*')].filter(e => e.scrollWidth > e.clientWidth + 1
                && getComputedStyle(e).overflowX !== 'visible');
            return fuori.length ? fuori.length + ' elementi tagliati in larghezza' : '';
        }""")
        if trabocca:
            sys.exit(f"{c['slug']}: {trabocca}")
        return pagina.pdf(prefer_css_page_size=True, print_background=True,
                          tagged=True, outline=True)
    finally:
        pagina.close()


def rifinisci(dati: bytes, c: dict, destinazione: Path) -> dict:
    with tempfile.NamedTemporaryFile(suffix=".pdf") as grezzo:
        grezzo.write(dati)
        grezzo.flush()
        pdf = pikepdf.open(grezzo.name)
        box = [float(v) for v in pdf.pages[0].mediabox]
        cornice = prepara_cornice(pdf, box[2] - box[0], box[3] - box[1], c["data"].year)
        fuori = 0
        for pg in pdf.pages:
            fuori += segna_artefatti(pdf, pg)
            applica_cornice(pdf, pg, cornice)
        imposta_metadati(pdf, c)
        destinazione.parent.mkdir(parents=True, exist_ok=True)
        pdf.save(destinazione, compress_streams=True, deterministic_id=True,
                 object_stream_mode=pikepdf.ObjectStreamMode.generate)
        pagine = len(pdf.pages)
    return {"pagine": pagine, "fuori_struttura": fuori}


# ── Controllo ───────────────────────────────────────────────────────────────

def controlla(c: dict) -> list[str]:
    problemi = []
    f = RADICE / "static" / c["pdf"].lstrip("/")
    if not f.exists():
        return [f"manca il file {f.relative_to(RADICE)}"]
    with pikepdf.open(f) as pdf:
        mark = pdf.Root.get("/MarkInfo")
        if not (mark and bool(mark.get("/Marked"))) or "/StructTreeRoot" not in pdf.Root:
            problemi.append("PDF senza tag")
        if str(pdf.Root.get("/Lang", "")) != LINGUA:
            problemi.append(f"lingua diversa da {LINGUA}")
        if str(pdf.docinfo.get("/Title", "")) != c["titolo"]:
            problemi.append("titolo diverso da quello del comunicato")
        for chiave in ("/Creator", "/Producer", "/Author"):
            if PROGRAMMI.search(str(pdf.docinfo.get(chiave, ""))):
                problemi.append(f"{chiave[1:]} con il nome di un programma")
        if "/Metadata" in pdf.Root:
            xmp = pdf.Root.Metadata.read_bytes().decode("utf-8", "replace")
            if PROGRAMMI.search(re.sub(r"<x:xmpmeta[^>]*>", "", xmp)):
                problemi.append("metadati XMP con il nome di un programma")
        fuori = sum(conta_fuori_struttura(p) for p in pdf.pages)
        if fuori:
            problemi.append(f"{fuori} operatori di disegno fuori da tag e artefatti")
    return problemi


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("slug", nargs="*", help="slug dei comunicati (default: tutti quelli con `pdf:`)")
    ap.add_argument("--check", action="store_true", help="controlla i PDF esistenti senza rigenerarli")
    ap.add_argument("--hugo", default=shutil.which("hugo") or "hugo", help="percorso di hugo")
    args = ap.parse_args(argv)

    elenco = comunicati(args.slug)
    if not elenco:
        print("Nessun comunicato con il campo `pdf:`.")
        return 0

    if args.check:
        errori = 0
        for c in elenco:
            problemi = controlla(c)
            print(f"{'OK ' if not problemi else 'NO '} {c['pdf']}" + (": " + "; ".join(problemi) if problemi else ""))
            errori += bool(problemi)
        return 1 if errori else 0

    from playwright.sync_api import sync_playwright

    with tempfile.TemporaryDirectory(prefix="comunicati-pdf-") as tmp:
        sito = costruisci_sito(Path(tmp), args.hugo)
        server, base = avvia_server(sito)
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch()
                try:
                    for c in elenco:
                        dest = RADICE / "static" / c["pdf"].lstrip("/")
                        esito = rifinisci(stampa(browser, base, c), c, dest)
                        kb = dest.stat().st_size / 1024
                        nota = (f"; {esito['fuori_struttura']} operatori fuori da tag e artefatti"
                                if esito["fuori_struttura"] else "")
                        print(f"{dest.relative_to(RADICE)}: {esito['pagine']} pagine, {kb:.0f} KB{nota}")
                finally:
                    browser.close()
        finally:
            server.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())
