#!/usr/bin/env python3
"""Alleggerisce la sola copia del sito per GitHub Pages. La pubblicazione si interrompe da sola a
10 minuti (tetto di actions/deploy-pages, non alzabile) e una copia da circa 780 MB spesso non fa in tempo.

Dalla sola copia escono sempre: video, audio, presentazioni, tutti gli archivi ZIP, i PDF oltre 2 MB
e i raster non ottimizzati (PNG, JPEG) oltre 2 MB. I collegamenti a quei file puntano alle copie su Aruba,
che non si toccano. WebP, SVG e i documenti sotto i 2 MB restano, così l'anteprima si legge da sola.
Se dopo questi tagli la copia supera ancora il tetto, escono anche i PDF più pesanti fra quelli rimasti.

Uso in deploy.yml, dopo la build per GitHub Pages e prima del manifesto e del caricamento:
    python3 scripts/alleggerisci-copia-pages.py public [--tetto-mb 500]
    python3 scripts/alleggerisci-copia-pages.py --prova [public]   # prove su cartelle finte e, se
                                        # data, sulla build per Aruba, che deve essere riconosciuta e lasciata stare
Uscita 2 se la cartella non è la build per GitHub Pages (la build per Aruba non si tocca mai); uscita 1 se la
copia resta oltre il limite di GitHub anche alleggerita, così il caricamento non parte e il run lo dice.
"""
import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import quote

BASE_PAGES = "https://sviluppoitaliadigitale.github.io/sito-pc-genzano/"
PREFISSO_PAGES = "/sito-pc-genzano/"
BASE_ARUBA = "https://www.protezionecivilegenzano.it/"
MB = 1024 * 1024
IN_PROVA = False
LIMITE_PAGES = 1_000_000_000  # limite di GitHub per un sito Pages: «1 GB», preso nel senso più stretto


def leggibile(byte):
    return f"{byte / 1e9:g} GB" if byte >= 1e9 else f"{byte / MB:.0f} MB"

# Sempre fuori dalla copia: sono i file più pesanti e su Aruba ci sono tutti.
VIDEO = {".mp4", ".m4v", ".mov", ".webm", ".ogv"}
AUDIO = {".m4a", ".mp3", ".wav", ".ogg", ".oga", ".opus", ".aac", ".flac"}
PRESENTAZIONI = {".pptx", ".ppt", ".odp", ".key"}
SEMPRE = VIDEO | AUDIO | PRESENTAZIONI
# Archivi da scaricare: la pagina che li linka resta, il file si apre da Aruba.
ARCHIVI = {".zip"}
# Raster non ottimizzati. WebP e SVG restano: sono già il formato delle foto e dei pittogrammi.
RASTER = {".png", ".jpg", ".jpeg", ".gif", ".tif", ".tiff", ".bmp"}
# 2 MB: sotto restano ordinanze, comunicati, schede e il manuale; sopra ci sono carte, presentazioni
# in PDF e le infografiche PNG da circa 4 MB l'una, che l'anteprima non deve sincronizzare.
SOGLIA_VOLUMINOSO = 2 * MB
# Fuori solo se la copia supera ancora il tetto, dal più pesante: i PDF sotto la soglia.
SE_SERVE = {".pdf", ".zip"}
# File di testo in cui si riscrivono i collegamenti (i file dell'indice Pagefind sono compressi e non citano i media).
TESTO = {".html", ".htm", ".xml", ".json", ".js", ".css", ".txt", ".webmanifest"}

PRIMA = r"""(?<=["'(=\s,;])"""          # un collegamento comincia dopo virgolette, uguale, parentesi, spazio, virgola
DOPO = r"""(?=["'\s)?#<>,;&\\]|$)"""     # e finisce prima di virgolette, spazio, parentesi, query, ancora


def avviso(livello, messaggio):
    """Annotazione di GitHub Actions; nelle prove solo testo, perché lì un errore è il risultato atteso."""
    print(f"[{livello}] {messaggio}" if IN_PROVA else f"::{livello}::{messaggio}")


def categoria(percorso):
    est = percorso.suffix.lower()
    if est in VIDEO:
        return "video"
    if est in AUDIO:
        return "audio"
    if est in PRESENTAZIONI:
        return "presentazioni"
    if est in ARCHIVI:
        return "archivi zip"
    if est in RASTER:
        return "immagini non ottimizzate"
    return "pdf"


def voluminoso(percorso):
    """File che la copia di anteprima non deve sincronizzare: su Aruba ci sono già."""
    est = percorso.suffix.lower()
    if est in SEMPRE or est in ARCHIVI:
        return True
    if est == ".pdf" or est in RASTER:
        return percorso.stat().st_size > SOGLIA_VOLUMINOSO
    return False


def e_build_pages(cartella):
    """La build per GitHub Pages carica i fogli di stile sotto /sito-pc-genzano/; quella per Aruba no."""
    indice = cartella / "index.html"
    if not indice.is_file():
        return False
    testo = indice.read_text("utf-8", errors="replace")
    return bool(re.search(r"""href=["']?/sito-pc-genzano/css/""", testo))


def scegli(cartella, tetto):
    """Restituisce (da togliere, peso totale prima, peso totale dopo)."""
    file = [p for p in cartella.rglob("*") if p.is_file() and not p.is_symlink()]
    totale = sum(p.stat().st_size for p in file)
    togli = sorted((p for p in file if voluminoso(p)), key=lambda p: p.as_posix())
    gia = set(togli)
    dopo = totale - sum(p.stat().st_size for p in togli)
    if dopo > tetto:
        altri = sorted((p for p in file if p not in gia and p.suffix.lower() in SE_SERVE),
                       key=lambda p: (-p.stat().st_size, p.as_posix()))
        for p in altri:
            if dopo <= tetto:
                break
            togli.append(p)
            dopo -= p.stat().st_size
    return togli, totale, dopo


def forme(rel):
    """Il percorso com'è e, se diverso, codificato come in un indirizzo."""
    codificato = quote(rel, safe="/")
    return [rel] if codificato == rel else [rel, codificato]


def riscrivi(cartella, percorsi):
    """Porta su Aruba i collegamenti ai file tolti. Restituisce (file cambiati, collegamenti riscritti)."""
    if not percorsi:
        return 0, 0
    alternative = sorted({f for rel in percorsi for f in forme(rel)}, key=len, reverse=True)
    gruppo = "(" + "|".join(re.escape(a) for a in alternative) + ")"
    host = r"(?:https?:)?//sviluppoitaliadigitale\.github\.io/sito-pc-genzano/"
    schemi = [re.compile(host + gruppo + DOPO),                       # indirizzo completo della copia
              re.compile(PRIMA + re.escape(PREFISSO_PAGES) + gruppo + DOPO),  # /sito-pc-genzano/…
              re.compile(PRIMA + "/" + gruppo + DOPO)]                 # /… senza sottocartella: su Pages non porterebbe da nessuna parte
    cambiati = riscritti = 0
    for p in cartella.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in TESTO or "pagefind" in p.relative_to(cartella).parts:
            continue
        testo = p.read_bytes().decode("utf-8", "surrogateescape")  # a byte: a capo e caratteri restano come sono
        nuovo, n_tot = testo, 0
        for schema in schemi:
            nuovo, n = schema.subn(lambda m: BASE_ARUBA + m.group(1), nuovo)
            n_tot += n
        if n_tot:
            p.write_bytes(nuovo.encode("utf-8", "surrogateescape"))
            cambiati += 1
            riscritti += n_tot
    return cambiati, riscritti


def residui(cartella, percorsi):
    """Collegamenti della copia che portano ancora a un file tolto (sulla copia darebbero 404)."""
    if not percorsi:
        return []
    alternative = sorted({f for rel in percorsi for f in forme(rel)}, key=len, reverse=True)
    schema = re.compile(r"(?:github\.io/sito-pc-genzano/|" + PRIMA + re.escape(PREFISSO_PAGES) + ")("
                        + "|".join(re.escape(a) for a in alternative) + ")" + DOPO)
    trovati = []
    for p in cartella.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in TESTO or "pagefind" in p.relative_to(cartella).parts:
            continue
        for m in schema.finditer(p.read_bytes().decode("utf-8", "surrogateescape")):
            trovati.append(f"{p.relative_to(cartella).as_posix()} → {m.group(1)}")
    return trovati


def alleggerisci(cartella, tetto_mb, riepilogo=None):
    cartella = Path(cartella)
    if not e_build_pages(cartella):
        avviso("error", f"{cartella} non è la build per GitHub Pages (manca /sito-pc-genzano/css/ in index.html): "
                        "non tolgo nulla. La build per Aruba non si tocca.")
        return 2
    togli, prima, dopo = scegli(cartella, tetto_mb * MB)
    rel = [p.relative_to(cartella).as_posix() for p in togli]
    per_cat = {}
    for p in togli:
        n, peso = per_cat.get(categoria(p), (0, 0))
        per_cat[categoria(p)] = (n + 1, peso + p.stat().st_size)
    # i documenti e le immagini tolti si elencano uno per uno: chi guarda l'anteprima sa che si aprono da Aruba
    elenchi = {}
    for p in togli:
        if p.suffix.lower() in SEMPRE:
            continue
        elenchi.setdefault(categoria(p), []).append((p.relative_to(cartella).as_posix(), p.stat().st_size))
    for p in togli:
        p.unlink()
    cambiati, riscritti = riscrivi(cartella, rel)
    resto = residui(cartella, rel)
    righe = [f"Copia per GitHub Pages: {prima / MB:.0f} MB prima, {dopo / MB:.0f} MB dopo (tetto {tetto_mb} MB, "
             f"limite di GitHub {leggibile(LIMITE_PAGES)}). Su Aruba non cambia nulla."]
    for cat, (n, peso) in sorted(per_cat.items()):
        righe.append(f"- {cat}: {n} file, {peso / MB:.0f} MB tolti dalla copia")
        if cat in elenchi:
            righe += [f"  - {doc} ({peso_doc / MB:.0f} MB)" for doc, peso_doc in elenchi[cat]]
    righe.append(f"- collegamenti portati su {BASE_ARUBA}: {riscritti} in {cambiati} file")
    if resto:
        righe.append(f"- collegamenti rimasti verso file tolti: {len(resto)} (sulla copia danno 404)")
        righe += [f"  - {r}" for r in resto[:20]]
    print("\n".join(righe))
    if resto:
        avviso("warning", f"{len(resto)} collegamenti della copia per GitHub Pages portano ancora a file tolti.")
    oltre_limite = dopo > LIMITE_PAGES
    if dopo > tetto_mb * MB:
        avviso("error" if oltre_limite else "warning",
               f"La copia per GitHub Pages pesa ancora {dopo / MB:.0f} MB, oltre il tetto di {tetto_mb} MB"
               + (f" e oltre il limite di GitHub di {leggibile(LIMITE_PAGES)}: non la carico" if oltre_limite else "")
               + ". Va alleggerita ancora (scripts/alleggerisci-copia-pages.py).")
    if riepilogo:
        with open(riepilogo, "a", encoding="utf-8") as f:
            f.write("### Copia per GitHub Pages alleggerita\n\n" + "\n".join(righe) + "\n")
    return 1 if oltre_limite else 0


def prova(build_aruba=None):
    """Cartella finta con i casi veri: indirizzi completi, /sito-pc-genzano/, HTML minificato senza virgolette,
    JSON, query, sottotitoli che restano, file con lo stesso inizio di nome, build per Aruba rifiutata, copia che
    resta oltre il limite. Con build_aruba controlla anche che la build vera per Aruba sia riconosciuta (senza
    toccarla)."""
    global IN_PROVA, LIMITE_PAGES
    IN_PROVA = True
    errori = []

    def controlla(cond, msg):
        if not cond:
            errori.append(msg)

    with tempfile.TemporaryDirectory() as t:
        c = Path(t) / "public"
        (c / "video").mkdir(parents=True)
        (c / "podcast/episodi").mkdir(parents=True)
        (c / "presentazioni").mkdir()
        (c / "manuali").mkdir()
        (c / "css").mkdir()
        (c / "pagefind").mkdir()
        (c / "video/a.mp4").write_bytes(b"0" * 3000)
        (c / "video/a.vtt").write_text("WEBVTT")
        (c / "video/a.mp4.png").write_bytes(b"1")
        (c / "podcast/episodi/b c.m4a").write_bytes(b"0" * 2000)
        (c / "presentazioni/p.pptx").write_bytes(b"0" * 1000)
        (c / "manuali/grande.pdf").write_bytes(b"0" * 5000)
        (c / "manuali/piccolo.pdf").write_bytes(b"0" * 100)
        (c / "pagefind/x.pf_fragment").write_bytes(b"/sito-pc-genzano/video/a.mp4")
        (c / "index.html").write_text(
            '<link href=/sito-pc-genzano/css/x.css rel=stylesheet>'
            '<video src=/sito-pc-genzano/video/a.mp4 poster=/sito-pc-genzano/video/a.mp4.png>'
            '<track src=/sito-pc-genzano/video/a.vtt></video>'
            '<a href="https://sviluppoitaliadigitale.github.io/sito-pc-genzano/presentazioni/p.pptx">PPTX</a>'
            "<a href='/sito-pc-genzano/podcast/episodi/b%20c.m4a?v=1'>audio</a>"
            '<a href="/manuali/grande.pdf">PDF</a><a href="/sito-pc-genzano/manuali/piccolo.pdf">piccolo</a>'
            '<p>/sito-pc-genzano/video/a.mp4.png resta</p>', "utf-8")
        (c / "podcast/index.json").write_text('{"audio":"/sito-pc-genzano/podcast/episodi/b c.m4a"}', "utf-8")
        (c / "rss.xml").write_text('<enclosure url="https://sviluppoitaliadigitale.github.io/sito-pc-genzano/'
                                   'video/a.mp4" />', "utf-8")
        # tetto alto: escono solo video, audio e presentazioni
        esito = alleggerisci(c, tetto_mb=1)
        controlla(esito == 0, f"uscita {esito} invece di 0")
        for tolto in ("video/a.mp4", "podcast/episodi/b c.m4a", "presentazioni/p.pptx"):
            controlla(not (c / tolto).exists(), f"{tolto} doveva uscire dalla copia")
        for resta in ("video/a.vtt", "video/a.mp4.png", "manuali/grande.pdf", "manuali/piccolo.pdf",
                      "pagefind/x.pf_fragment"):
            controlla((c / resta).exists(), f"{resta} doveva restare")
        html = (c / "index.html").read_text("utf-8")
        controlla(f"src={BASE_ARUBA}video/a.mp4 " in html, "video non portato su Aruba")
        controlla("poster=/sito-pc-genzano/video/a.mp4.png" in html, "poster toccato per sbaglio")
        controlla("src=/sito-pc-genzano/video/a.vtt" in html, "sottotitoli toccati per sbaglio")
        controlla(f'href="{BASE_ARUBA}presentazioni/p.pptx"' in html, "presentazione non portata su Aruba")
        controlla(f"href='{BASE_ARUBA}podcast/episodi/b%20c.m4a?v=1'" in html, "audio con spazio non portato su Aruba")
        controlla('href="/manuali/grande.pdf"' in html, "PDF toccato senza bisogno")
        controlla("/sito-pc-genzano/video/a.mp4.png resta" in html, "testo con nome simile toccato")
        controlla(f'"audio":"{BASE_ARUBA}podcast/episodi/b c.m4a"' in (c / "podcast/index.json").read_text("utf-8"),
                  "JSON non riscritto")
        controlla(f'url="{BASE_ARUBA}video/a.mp4"' in (c / "rss.xml").read_text("utf-8"), "RSS non riscritto")
        controlla((c / "pagefind/x.pf_fragment").read_bytes() == b"/sito-pc-genzano/video/a.mp4",
                  "indice Pagefind toccato")
        controlla(residui(c, ["video/a.mp4", "podcast/episodi/b c.m4a", "presentazioni/p.pptx"]) == [],
                  "restano collegamenti a file tolti")
    with tempfile.TemporaryDirectory() as t:
        c = Path(t) / "public"
        (c / "manuali").mkdir(parents=True)
        (c / "index.html").write_text('<link href="/sito-pc-genzano/css/x.css" rel="stylesheet">'
                                      '<a href="/sito-pc-genzano/manuali/grande.pdf">PDF</a>', "utf-8")
        (c / "manuali/grande.pdf").write_bytes(b"0" * (2 * MB))
        (c / "manuali/medio.pdf").write_bytes(b"0" * (MB // 2))
        (c / "manuali/piccolo.pdf").write_bytes(b"0" * 1000)
        # tetto stretto: esce il PDF più pesante, e basta
        controlla(alleggerisci(c, tetto_mb=1) == 0, "seconda prova: uscita diversa da 0")
        controlla(not (c / "manuali/grande.pdf").exists(), "il PDF più pesante doveva uscire")
        controlla((c / "manuali/medio.pdf").exists() and (c / "manuali/piccolo.pdf").exists(),
                  "usciti più PDF del necessario")
        controlla(f'href="{BASE_ARUBA}manuali/grande.pdf"' in (c / "index.html").read_text("utf-8"),
                  "PDF tolto non portato su Aruba")
    with tempfile.TemporaryDirectory() as t:
        c = Path(t) / "public"
        (c / "infografiche").mkdir(parents=True)
        (c / "manuali").mkdir()
        (c / "formazione/pacchetti").mkdir(parents=True)
        (c / "images").mkdir()
        (c / "index.html").write_text(
            '<link href="/sito-pc-genzano/css/x.css" rel="stylesheet">'
            '<img src="/sito-pc-genzano/infografiche/grande.png">'
            '<img src="/sito-pc-genzano/infografiche/piccola.png">'
            '<img src="/sito-pc-genzano/images/foto.webp">'
            '<a href="/sito-pc-genzano/manuali/grosso.pdf">g</a>'
            '<a href="/sito-pc-genzano/manuali/snello.pdf">s</a>'
            '<a href="/sito-pc-genzano/formazione/pacchetti/kit.zip">z</a>', "utf-8")
        (c / "infografiche/grande.png").write_bytes(b"0" * (SOGLIA_VOLUMINOSO + 1))
        (c / "infografiche/piccola.png").write_bytes(b"0" * (MB // 2))
        (c / "images/foto.webp").write_bytes(b"0" * (3 * MB))
        (c / "manuali/grosso.pdf").write_bytes(b"0" * (SOGLIA_VOLUMINOSO + 10))
        (c / "manuali/snello.pdf").write_bytes(b"0" * (MB // 2))
        (c / "formazione/pacchetti/kit.zip").write_bytes(b"0" * 5000)
        # tetto altissimo: escono lo stesso voluminosi e archivi, non perché si supera il tetto
        controlla(alleggerisci(c, tetto_mb=10000) == 0, "soglia voluminosi: uscita diversa da 0")
        for tolto in ("infografiche/grande.png", "manuali/grosso.pdf", "formazione/pacchetti/kit.zip"):
            controlla(not (c / tolto).exists(), f"{tolto} doveva uscire anche sotto il tetto")
        for resta in ("infografiche/piccola.png", "images/foto.webp", "manuali/snello.pdf"):
            controlla((c / resta).exists(), f"{resta} doveva restare")
        html = (c / "index.html").read_text("utf-8")
        controlla(f'src="{BASE_ARUBA}infografiche/grande.png"' in html, "png voluminoso non portato su Aruba")
        controlla('src="/sito-pc-genzano/infografiche/piccola.png"' in html, "png piccola toccata")
        controlla('src="/sito-pc-genzano/images/foto.webp"' in html, "webp toccato")
        controlla(f'href="{BASE_ARUBA}manuali/grosso.pdf"' in html, "pdf voluminoso non portato su Aruba")
        controlla('href="/sito-pc-genzano/manuali/snello.pdf"' in html, "pdf snello toccato")
        controlla(f'href="{BASE_ARUBA}formazione/pacchetti/kit.zip"' in html, "zip non portato su Aruba")
        controlla(residui(c, ["infografiche/grande.png", "manuali/grosso.pdf",
                              "formazione/pacchetti/kit.zip"]) == [],
                  "restano collegamenti ai voluminosi tolti")
    with tempfile.TemporaryDirectory() as t:
        c = Path(t) / "public"
        (c / "video").mkdir(parents=True)
        (c / "index.html").write_text('<link href="/css/x.css" rel="stylesheet"><video src="/video/a.mp4">', "utf-8")
        (c / "video/a.mp4").write_bytes(b"0" * 10)
        controlla(alleggerisci(c, tetto_mb=800) == 2, "la build per Aruba doveva essere rifiutata")
        controlla((c / "video/a.mp4").exists(), "toccata la build per Aruba")
    with tempfile.TemporaryDirectory() as t:
        c = Path(t) / "public"
        (c / "images").mkdir(parents=True)
        (c / "index.html").write_text('<link href="/sito-pc-genzano/css/x.css" rel="stylesheet">', "utf-8")
        (c / "images/grande.webp").write_bytes(b"0" * (3 * MB))
        limite = LIMITE_PAGES
        LIMITE_PAGES = 2 * MB  # una copia che resta oltre il limite anche alleggerita: non si carica
        try:
            controlla(alleggerisci(c, tetto_mb=1) == 1, "copia oltre il limite: l'uscita doveva essere 1")
        finally:
            LIMITE_PAGES = limite
        controlla((c / "images/grande.webp").exists(), "tolto un WebP: le immagini ottimizzate restano")
    if build_aruba:
        c = Path(build_aruba)
        indice = c / "index.html"
        if not indice.is_file():
            errori.append(f"{indice} non c'è: --prova CARTELLA vuole la build per Aruba")
        else:
            testo = indice.read_text("utf-8", errors="replace")
            controlla(re.search(r"""href=["']?/css/""", testo) is not None,
                      f"{c} non carica i fogli di stile da /css/: è davvero la build per Aruba?")
            controlla(not e_build_pages(c), f"{c} è la build per Aruba ma la guardia la scambia per quella per "
                                            "GitHub Pages: lo script la toccherebbe")
    if errori:
        print("PROVE NON RIUSCITE:\n- " + "\n- ".join(errori))
        return 1
    print("Prove riuscite: copia alleggerita, collegamenti su Aruba, build per Aruba rifiutata"
          + (f", {build_aruba} riconosciuta come build per Aruba." if build_aruba else "."))
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("cartella", nargs="?")
    ap.add_argument("--tetto-mb", type=int, default=500)
    ap.add_argument("--prova", action="store_true")
    a = ap.parse_args()
    if a.prova:
        return prova(a.cartella)
    return alleggerisci(a.cartella or "public", a.tetto_mb, os.environ.get("GITHUB_STEP_SUMMARY"))


if __name__ == "__main__":
    sys.exit(main())
