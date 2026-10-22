#!/usr/bin/env python3
"""
Controllo dei fogli di stampa: stampa davvero le pagine (Chromium, A4, media
print, come «Stampa» o «Salva come PDF» del browser) e guarda i fogli.

Nasce il 06/10/2026: una misura su tutte le pagine stampabili ha trovato 49
schede (quasi tutte dei kit calamità) che mandavano su un foglio in più la sola
fascia delle affiliazioni o una riga di fonti, e quattro pagine del sito che
finivano con un foglio bianco. Nessun controllo leggendo il codice se ne poteva
accorgere: si vede solo stampando (rule 09 § 15-ter).

Dal 22/10/2026 ogni scheda, kit e storia si stampa con più serie di caratteri,
non solo con quelli della macchina di controllo. Le schede, i kit e le storie
non hanno caratteri propri: usano quelli del computer, e la stessa riga è più
o meno larga a seconda del sistema. Con i soli caratteri della CI (Liberation,
con le misure di Arial e Times) 72 pagine stampabili lasciavano un foglio
quasi vuoto su un computer con caratteri più larghi. Le serie stanno in
scripts/fogli-stampa/caratteri/ (vedi LEGGIMI.md lì):
  - liberation: le misure di Arial e Times (Windows, Chromebook, Android,
    Linux con Liberation);
  - windows-mac: schede e storie; i caratteri di sistema di Windows e Mac non
    si installano su Linux, quindi la prova usa Inter (circa il 7% più largo
    di Arial, un punto fra Arial e DejaVu) e, per Georgia, Gelasio, che ha le
    sue stesse misure;
  - adventor: kit; Century Gothic (Windows e Mac con Office) e URW Gothic
    (Linux), nella prova TeX Gyre Adventor, con le misure di Avant Garde
    (circa il 10% più largo di Arial);
  - dejavu: un Linux senza i caratteri di Arial e Times, i più larghi (circa
    il 14% più di Arial, il 28% più di Times).
Sono punti di larghezza, non copie dei caratteri veri: coprono i casi più
comuni, non ogni computer possibile (un foglio che sfora può dipendere anche da
una larghezza che sta in mezzo a due serie).
Prima di stampare, lo script controlla dentro Chromium che ogni serie dia
davvero i caratteri attesi: se un pacchetto manca o una cache di fontconfig è
vecchia, si ferma invece di passare con caratteri sbagliati.
Prima di ogni PDF aspetta anche le immagini di sfondo (ATTENDI_IMMAGINI): la
fascia delle affiliazioni è lo sfondo di un ::after, e con la macchina carica
arrivava dopo il PDF; la misura cambiava con il carico (22/10/2026).

Bloccante (exit 1):
  - un foglio completamente bianco, in qualunque posizione;
  - nelle schede, nei kit e nelle storie: un foglio quasi vuoto (meno
    dell'8% dell'altezza con qualcosa stampato), in qualunque posizione,
    quando i fogli sono più di uno. Fino al 07/10/2026 si guardava solo
    l'ultimo, e una scheda di tre pagine con la fascia delle affiliazioni da
    sola sul secondo foglio passava il controllo;
  - un errore JavaScript durante il caricamento della pagina.
Exit 2: build mancante o caratteri della prova diversi da quelli attesi.

Pagine controllate:
  - schede stampabili, schede dei kit calamità, storie (pagine HTML autonome
    in static/formazione/) e, dal 21/10/2026, i moduli per le scuole
    (static/scuole/), che usano il foglio di stile delle schede: con tre serie
    di caratteri ciascuna;
  - dal 22/10/2026, ogni scheda dentro i pacchetti «Stampa tutto»
    (formazione/schede-stampabili/pacchetti/), stampata isolata nella sua
    sezione (le altre nascoste, tutto il CSS al suo posto) con le stesse serie.
    Nel pacchetto la scala di stampa della scheda diventa lo zoom della sezione,
    che rimpicciolisce anche gli spazi in millimetri (fascia delle affiliazioni,
    piè di pagina): la stessa scheda si impagina in un altro modo e può lasciare
    un foglio quasi vuoto che da sola non lascia. Al primo controllo è successo
    a cinque schede, una anche con i caratteri della CI;
  - un campione fisso di pagine del sito (PAGINE_SITO), dove si guarda solo il
    foglio bianco: le pagine lunghe possono finire con poche righe. Il sito ha
    i suoi caratteri (Titillium Web), quindi basta una serie.

Uso:
  python3 scripts/check-fogli-stampa.py [--public public]              # tutte
  python3 scripts/check-fogli-stampa.py --da-git origin/main   # solo ciò che la PR tocca
  python3 scripts/check-fogli-stampa.py --caratteri liberation # una serie sola, per una prova veloce
  python3 scripts/check-fogli-stampa.py --pagine formazione/schede-stampabili/estate-sicura/ \
      --png /tmp/fogli                                         # una pagina, con i fogli in PNG
Con --da-git si controllano le pagine stampabili modificate (anche solo in
un'immagine della loro cartella; per un'immagine di un kit calamità, le schede
del kit che la nominano) e le loro sezioni nei pacchetti, più le
sezioni entrate in un pacchetto; se cambia un foglio di stile condiviso (print.css dei kit,
scheda-print.css, storia-libro.css, custom.css) si ricontrolla l'intera famiglia
che lo usa (con scheda-print.css anche tutti i pacchetti), se cambia il
generatore dei pacchetti si ricontrollano tutti i pacchetti, se cambia una serie
di caratteri o questo script si ricontrolla tutto. Con --pagine una scheda porta
con sé le sue sezioni nei pacchetti; si può dare anche un pacchetto intero
(formazione/schede-stampabili/pacchetti/primaria.html) o una sua sezione
(…/primaria.html#scheda-NOME). Con --png si salvano i fogli (50 dpi) delle
pagine con un problema, oppure di tutte quelle date con --pagine.

Dipendenze: playwright (Chromium), pymupdf, i pacchetti fonts-liberation,
fonts-inter, fonts-texgyre, fonts-dejavu-core e fonts-noto-color-emoji
(Ubuntu 24.04). Variabile CHROMIUM_PATH facoltativa.
"""
from __future__ import annotations

import argparse
import asyncio
import functools
import http.server
import os
import re
import subprocess
import sys
import threading
from pathlib import Path

RADICE = Path(__file__).resolve().parents[1]
CARTELLA_CARATTERI = Path(__file__).resolve().parent / "fogli-stampa" / "caratteri"
SOGLIA_VUOTO = 0.08      # frazione dell'altezza con qualcosa stampato
PAGINE_SITO = [
    "", "cosa-fare-adesso/", "numeri-utili/", "allerte-meteo/", "piano-familiare/",
    "rischi-prevenzione/rischio-sismico/", "rischi-prevenzione/kit-emergenza/",
    "formazione/", "formazione/cosa-fare-in-caso-di/", "formazione/kit-scuola-infanzia/",
    "formazione/primo-soccorso/defibrillatore-dae/",
    "formazione/rischio-incendio/procedure-emergenza/", "chi-siamo/", "contatti/",
]
FAMIGLIE = {
    "static/formazione/kit-calamita-shared/print.css": "kit",
    "static/formazione/schede-stampabili/assets/scheda-print.css": "schede",
    "static/formazione/storie-e-racconti/assets/storia-libro.css": "storie",
    "themes/flavour-pcgenzano/static/css/custom.css": "tutte",
}
# Pacchetti «Stampa tutto»: una sezione per scheda, generate da GENERATORE_PACCHETTI.
PACCHETTI = "formazione/schede-stampabili/pacchetti"
GENERATORE_PACCHETTI = "scripts/genera-pacchetti-schede.py"
# Nel pacchetto si stampa una sezione per volta: le altre si nascondono, e la
# sezione scelta non porta l'interruzione di pagina che la separa dalla dopo.
ISOLA_SEZIONE = ('.pacchetto-scheda:not([id="{sid}"]) {{ display: none !important; }}'
                 '[id="{sid}"] {{ break-after: auto !important; page-break-after: auto !important; }}')
# Prima di stampare si aspettano le immagini, anche quelle di sfondo: la fascia
# delle affiliazioni è lo sfondo di un ::after e può arrivare dopo l'evento load.
# Con il computer carico il PDF partiva prima e il foglio usciva più vuoto del vero
# (22/10/2026: una scheda risultava quasi vuota al 7,7% invece che all'11,7%).
# Le immagini con loading="lazy" si caricano subito, come quando si stampa dal browser.
ATTENDI_IMMAGINI = """async () => {
  for (const img of document.images) if (img.loading === "lazy") img.loading = "eager";
  const url = new Set(), re = /url\\(\\s*["']?([^"')]+)["']?\\s*\\)/g;
  for (const el of document.querySelectorAll("*")) {
    for (const pseudo of [null, "::before", "::after"]) {
      const s = getComputedStyle(el, pseudo);
      for (const v of [s.backgroundImage, s.content, s.listStyleImage, s.borderImageSource]) {
        if (v && v.includes("url(")) for (const m of v.matchAll(re)) url.add(m[1]);
      }
    }
  }
  const attese = [...url].map(u => new Promise(fatto => {
    const i = new Image(); i.onload = i.onerror = () => fatto(); i.src = u;
  }));
  for (const img of document.images) if (!img.complete) attese.push(new Promise(fatto => {
    img.addEventListener("load", fatto, {once: true});
    img.addEventListener("error", fatto, {once: true});
  }));
  await Promise.race([Promise.all(attese), new Promise(fatto => setTimeout(fatto, 15000))]);
  await document.fonts.ready;  // un carattere chiesto solo dalle regole di stampa
  await new Promise(fatto => { requestAnimationFrame(() => requestAnimationFrame(fatto)); setTimeout(fatto, 200); });
  return url.size;
}"""

# Serie di caratteri: nome del file .conf → come si chiama nei messaggi.
CARATTERI = {
    "liberation": "caratteri di Arial e Times",
    "windows-mac": "caratteri di Windows e Mac (Segoe UI, San Francisco, Georgia)",
    "adventor": "Century Gothic",
    "dejavu": "un Linux senza Arial e Times (DejaVu)",
}
PER_FAMIGLIA = {
    "schede": ("liberation", "windows-mac", "dejavu"),
    "storie": ("liberation", "windows-mac", "dejavu"),
    "kit": ("liberation", "adventor", "dejavu"),
    "sito": ("liberation",),
}
# Le pile di caratteri dei fogli di stile, e che cosa deve uscirne in Chromium
# con ogni serie. Se un foglio di stile cambia pila, lo script si ferma: le
# serie di prova vanno ripensate insieme alla pila.
PILE = {
    "schede": ("static/formazione/schede-stampabili/assets/scheda-print.css",
               '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Cantarell, '
               '"Helvetica Neue", Arial, sans-serif'),
    "kit": ("static/formazione/kit-calamita-shared/print.css",
            "'URW Gothic L', 'Century Gothic', 'Avant Garde Gothic', 'Avant Garde', "
            "'ITC Avant Garde Gothic', 'Liberation Sans', sans-serif"),
    "storie": ("static/formazione/storie-e-racconti/assets/storia-libro.css",
               'Georgia, "Times New Roman", serif'),
    "titoli delle storie": ("static/formazione/storie-e-racconti/assets/storia-libro.css",
                            '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'),
}
ATTESI = {
    "liberation": {"schede": "Liberation Sans", "kit": "Liberation Sans",
                   "storie": "Liberation Serif", "titoli delle storie": "Liberation Sans"},
    "windows-mac": {"schede": "Inter", "storie": "Gelasio", "titoli delle storie": "Inter"},
    "adventor": {"kit": "TeX Gyre Adventor"},
    "dejavu": {"schede": "DejaVu Sans", "kit": "DejaVu Sans",
               "storie": "DejaVu Serif", "titoli delle storie": "DejaVu Sans"},
}
PILA_FAMIGLIA = {"schede": ("schede",), "kit": ("kit",), "storie": ("storie", "titoli delle storie")}


def stampabili(public: Path) -> dict[str, str]:
    """{percorso relativo in public: famiglia} delle pagine HTML autonome."""
    out: dict[str, str] = {}
    base = public / "formazione"
    for f in sorted(base.glob("schede-stampabili/*/index.html")):
        if f.parent.name not in ("pacchetti", "assets"):
            out[f.relative_to(public).as_posix()] = "schede"
    for f in sorted(base.glob("kit-calamita-*/*.html")):
        if f.name != "index.html":          # gli indici dei kit sono pagine di navigazione
            out[f.relative_to(public).as_posix()] = "kit"
    for f in sorted(base.glob("storie-e-racconti/*/index.html")):
        if f.parent.name != "assets":
            out[f.relative_to(public).as_posix()] = "storie"
    # Moduli per le scuole (liberatoria, circolare, convenzione PCTO…): usano il
    # foglio di stile delle schede e si stampano per farli firmare (21/10/2026).
    for f in sorted(public.glob("scuole/*/*/index.html")):
        out[f.relative_to(public).as_posix()] = "schede"
    # le pagine di rimando a un indirizzo nuovo non si stampano
    return {k: v for k, v in out.items()
            if not re.search(r'http-equiv=["\']?refresh', (public / k).read_text(errors="replace"), re.I)}


def ids_sezioni(html: str) -> list[str]:
    """Gli id delle sezioni «pacchetto-scheda» di un pacchetto, in ordine."""
    ids = []
    for tag in re.findall(r"<section\b[^>]*>", html):
        classe = re.search(r'\bclass="([^"]*)"', tag)
        sid = re.search(r'\bid="([^"]+)"', tag)
        if classe and sid and "pacchetto-scheda" in classe.group(1).split():
            ids.append(sid.group(1))
    return ids


def sezioni_pacchetti(public: Path) -> dict[str, list[str]]:
    """{percorso del pacchetto «Stampa tutto» in public: id delle sue sezioni, in ordine}."""
    out: dict[str, list[str]] = {}
    for f in sorted((public / PACCHETTI).glob("*.html")):
        ids = ids_sezioni(f.read_text(errors="replace"))
        if ids:
            out[f.relative_to(public).as_posix()] = ids
    return out


def sezioni_di(slug: str, sezioni: dict[str, list[str]]) -> dict[str, list[str]]:
    """Le sezioni della scheda «slug» nei pacchetti che la contengono."""
    sid = f"scheda-{slug}"
    return {pk: [sid] for pk, ids in sezioni.items() if sid in ids}


def unisci(a: dict[str, list[str]], b: dict[str, list[str]]) -> dict[str, list[str]]:
    out = {pk: list(ids) for pk, ids in a.items()}
    for pk, ids in b.items():
        out.setdefault(pk, [])
        out[pk] += [s for s in ids if s not in out[pk]]
    return out


def da_git(base: str, tutte: dict[str, str],
           sezioni: dict[str, list[str]]) -> tuple[dict[str, str], dict[str, list[str]]]:
    diff = subprocess.run(["git", "diff", "--name-only", f"{base}...HEAD"],
                          capture_output=True, text=True, check=True).stdout.split()
    famiglie = {FAMIGLIE[f] for f in diff if f in FAMIGLIE}
    # Cambia una serie di caratteri o questo script: si ristampa tutto.
    if "tutte" in famiglie or any(f.startswith("scripts/fogli-stampa/") or
                                  f == "scripts/check-fogli-stampa.py" for f in diff):
        return tutte, sezioni
    scelte = {k: v for k, v in tutte.items() if v in famiglie}
    for f in diff:
        if f.startswith("static/"):
            rel = f[len("static/"):]
            # la pagina stessa, o un file nella sua cartella o in una sottocartella
            # (un'immagine nuova cambia l'impaginazione quanto il testo)
            candidate = [rel] if rel.endswith(".html") else \
                [f"{d.as_posix()}/index.html" for d in Path(rel).parents if d.as_posix() != "."]
            for pagina in candidate:
                if pagina in tutte:
                    scelte[pagina] = tutte[pagina]
                    break
            # Le schede dei kit calamità non si chiamano index.html e le loro immagini
            # stanno in img/ dentro la cartella del kit: si ristampano le schede del kit
            # che nominano il file, o tutte se nessuna lo nomina (22/10/2026: prima
            # un'immagine nuova in un kit non faceva ristampare nessuna scheda).
            parti = rel.split("/")
            if not rel.endswith(".html") and len(parti) > 2 and parti[0] == "formazione" \
                    and parti[1].startswith("kit-calamita-"):
                schede_kit = {p: fam for p, fam in tutte.items()
                              if p.startswith(f"formazione/{parti[1]}/")}
                nominano = {p: fam for p, fam in schede_kit.items()
                            if (RADICE / "static" / p).is_file() and
                            Path(rel).name in (RADICE / "static" / p).read_text(errors="replace")}
                scelte.update(nominano or schede_kit)
    # I pacchetti: tutti se cambia il foglio di stile delle schede o il generatore,
    # altrimenti le sezioni delle schede toccate (cartella della scheda, immagini comprese).
    if "schede" in famiglie or GENERATORE_PACCHETTI in diff:
        return scelte, sezioni
    scelte_sez: dict[str, list[str]] = {}
    for f in diff:
        parti = f.split("/")
        if len(parti) > 4 and parti[:3] == ["static", "formazione", "schede-stampabili"] \
                and parti[3] not in ("pacchetti", "assets"):
            scelte_sez = unisci(scelte_sez, sezioni_di(parti[3], sezioni))
        # Un pacchetto che cambia senza che cambi la scheda: una scheda che già c'era
        # entra nel kit della sua fascia. Si stampano le sezioni che prima non c'erano.
        rel = f[len("static/"):] if f.startswith("static/") else ""
        if rel in sezioni:
            prima = subprocess.run(["git", "show", f"{base}:{f}"], capture_output=True, text=True)
            vecchie = set(ids_sezioni(prima.stdout))
            nuove = [s for s in sezioni[rel] if s not in vecchie]
            if nuove:
                scelte_sez = unisci(scelte_sez, {rel: nuove})
    return scelte, scelte_sez


def riempimento(pagina) -> float:
    """Frazione delle righe di pixel con qualcosa stampato (0 = foglio bianco)."""
    pix = pagina.get_pixmap(dpi=30, colorspace="gray")
    w, h, s = pix.width, pix.height, pix.samples
    piene = sum(1 for y in range(h) if min(s[y * w:(y + 1) * w]) < 235)
    return piene / h


def normalizza(testo: str) -> str:
    return re.sub(r"\s+", " ", testo).strip()


def controlla_pile() -> list[str]:
    """Le pile dichiarate qui devono essere quelle dei fogli di stile."""
    errori = []
    for nome, (file, pila) in PILE.items():
        if not (RADICE / file).is_file():
            errori.append(f"manca {file} ({nome}): aggiorna PILE e ATTESI in questo script.")
            continue
        css = normalizza((RADICE / file).read_text(errors="replace"))
        if f"font-family: {normalizza(pila)};" not in css:
            errori.append(f"{file} non dichiara più la pila «{pila}» ({nome}): aggiorna PILE e "
                          "ATTESI in questo script e le serie in scripts/fogli-stampa/caratteri/.")
    return errori


async def caratteri_usati(browser, pile: list[str]) -> dict[str, tuple[str, str]]:
    """Che carattere usa davvero Chromium per ogni pila, letto con il protocollo di debug:
    (carattere principale, elenco di tutti con il numero di glifi disegnati).

    Il principale è quello che disegna più glifi del testo di prova: il protocollo
    elenca i caratteri senza un ordine preciso, e con alcune serie mette per primo
    un carattere di riserva che disegna un solo glifo."""
    pagina = await browser.new_page()
    try:
        html = "".join(f'<p id="p{i}" style="font-family:{PILE[n][1].replace(chr(34), chr(39))}">'
                       "Prova di stampa: àèìòù 112</p>" for i, n in enumerate(pile))
        await pagina.set_content(html)
        cdp = await pagina.context.new_cdp_session(pagina)
        await cdp.send("DOM.enable")
        await cdp.send("CSS.enable")
        radice = (await cdp.send("DOM.getDocument", {"depth": -1}))["root"]["nodeId"]
        usati = {}
        for i, n in enumerate(pile):
            nodo = (await cdp.send("DOM.querySelector", {"nodeId": radice, "selector": f"#p{i}"}))["nodeId"]
            fonti = (await cdp.send("CSS.getPlatformFontsForNode", {"nodeId": nodo}))["fonts"]
            principale = max(fonti, key=lambda f: f["glyphCount"])["familyName"] if fonti else ""
            usati[n] = (principale, ", ".join(f"{f['familyName']} ({f['glyphCount']} glifi)" for f in fonti))
        await cdp.detach()
        return usati
    finally:
        await pagina.close()


def problemi_fogli(fogli: list[float], fam: str) -> tuple[list[int], list[int]]:
    """(fogli bianchi, fogli quasi vuoti), numerati da 1. I quasi vuoti contano solo
    nelle schede, nei kit e nelle storie con più di un foglio, e solo se non ci sono
    fogli bianchi."""
    bianchi = [i + 1 for i, r in enumerate(fogli) if r == 0]
    if bianchi or fam == "sito" or len(fogli) < 2:
        return bianchi, []
    # Ogni foglio, non solo l'ultimo: una pagina che sfora di pochi millimetri
    # manda la sola fascia delle affiliazioni sul foglio dopo, e se la scheda ha
    # più pagine quel foglio sta in mezzo.
    return [], [i + 1 for i, r in enumerate(fogli) if r < SOGLIA_VUOTO]


async def stampa(browser, porta: int, rel: str, fam: str, png: Path | None, sempre: bool):
    """(riempimento di ogni foglio, errori JavaScript, errore di apertura o stampa).
    Con png, salva i fogli in PNG se c'è un problema (o sempre, con sempre=True)."""
    import pymupdf
    pagina = await browser.new_page()
    js: list[str] = []
    pagina.on("pageerror", lambda e: js.append(str(e).splitlines()[0][:160]))
    url = f"http://127.0.0.1:{porta}/{rel[:-len('index.html')] if rel.endswith('index.html') else rel}"
    try:
        risposta = await pagina.goto(url, wait_until="load", timeout=45000)
        if risposta is None or risposta.status >= 400:
            # una pagina d'errore stampa bene: senza questo controllo
            # un indirizzo del campione sparito passerebbe per verificato
            return None, js, f"la pagina non esiste (HTTP {risposta.status if risposta else '—'})"
        await pagina.evaluate("document.fonts.ready.then(() => true)")
        await pagina.emulate_media(media="print")
        await pagina.evaluate(ATTENDI_IMMAGINI)
        pdf = await pagina.pdf(format="A4", prefer_css_page_size=True, print_background=True)
    except Exception as e:  # pagina che non si apre: è un errore anche quello
        return None, js, f"la pagina non si stampa ({str(e).splitlines()[0][:120]})"
    finally:
        await pagina.close()
    doc = pymupdf.open(stream=pdf, filetype="pdf")
    fogli = [riempimento(p) for p in doc]
    if png is not None and (sempre or any(problemi_fogli(fogli, fam))):
        png.mkdir(parents=True, exist_ok=True)
        for i, p in enumerate(doc, 1):
            p.get_pixmap(dpi=50).save(str(png / f"foglio-{i:02d}.png"))
    return fogli, js, None


async def stampa_pacchetto(browser, porta: int, rel: str, ids: list[str], semaforo,
                           png_di, sempre: bool):
    """Stampa le sezioni «ids» di un pacchetto «Stampa tutto», una per volta, nella stessa
    pagina: si apre una volta sola, perché un pacchetto contiene decine di schede.
    ({id della sezione: riempimento dei fogli}, errori JavaScript, errore di apertura o stampa).
    png_di(id) dà la cartella dove salvare i fogli in PNG, o None."""
    import pymupdf
    js: list[str] = []
    esiti: dict[str, list[float]] = {}
    async with semaforo:
        pagina = await browser.new_page()
        pagina.on("pageerror", lambda e: js.append(str(e).splitlines()[0][:160]))
        try:
            risposta = await pagina.goto(f"http://127.0.0.1:{porta}/{rel}", wait_until="load",
                                         timeout=120000)
            if risposta is None or risposta.status >= 400:
                await pagina.close()
                return esiti, js, f"il pacchetto non esiste (HTTP {risposta.status if risposta else '—'})"
            await pagina.evaluate("document.fonts.ready.then(() => true)")
            await pagina.emulate_media(media="print")
            await pagina.evaluate(ATTENDI_IMMAGINI)
        except Exception as e:
            await pagina.close()
            return esiti, js, f"il pacchetto non si apre ({str(e).splitlines()[0][:120]})"
    try:
        for sid in ids:
            async with semaforo:
                stile = await pagina.add_style_tag(content=ISOLA_SEZIONE.format(sid=sid))
                try:
                    pdf = await pagina.pdf(format="A4", prefer_css_page_size=True,
                                           print_background=True)
                finally:
                    await stile.evaluate("e => e.remove()")
            doc = pymupdf.open(stream=pdf, filetype="pdf")
            fogli = [riempimento(p) for p in doc]
            esiti[sid] = fogli
            cart = png_di(sid)
            if cart is not None and (sempre or any(problemi_fogli(fogli, "schede"))):
                cart.mkdir(parents=True, exist_ok=True)
                for i, p in enumerate(doc, 1):
                    p.get_pixmap(dpi=50).save(str(cart / f"foglio-{i:02d}.png"))
    except Exception as e:
        return esiti, js, f"il pacchetto non si stampa ({str(e).splitlines()[0][:120]})"
    finally:
        await pagina.close()
    return esiti, js, None


async def controlla(public: Path, voci: list[tuple[str, str]], serie: list[str],
                    paralleli: int, png: Path | None = None, sempre: bool = False,
                    sezioni: dict[str, list[str]] | None = None) -> tuple[list[str], list[str], int]:
    from playwright.async_api import async_playwright

    class Silenzioso(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    class Server(http.server.ThreadingHTTPServer):
        def handle_error(self, request, client_address):
            # una pagina chiusa mentre riceve ancora un file (un'immagine caricata
            # tardi): non è un errore della prova, e il registro resta leggibile
            if isinstance(sys.exc_info()[1], (BrokenPipeError, ConnectionResetError)):
                return
            super().handle_error(request, client_address)
    srv = Server(("127.0.0.1", 0), functools.partial(Silenzioso, directory=str(public)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    porta = srv.server_address[1]

    sezioni = {pk: ids for pk, ids in (sezioni or {}).items() if ids}
    # Le sezioni dei pacchetti si stampano come le schede.
    in_uso = {f for _, f in voci} | ({"schede"} if sezioni else set())
    usate = [c for c in CARATTERI if c in serie and any(c in PER_FAMIGLIA[f] for f in in_uso)]
    preparazione: list[str] = []
    errori: list[str] = []
    stampe = 0
    async with async_playwright() as p:
        kw = {"executable_path": os.environ["CHROMIUM_PATH"]} if os.environ.get("CHROMIUM_PATH") else {}
        browser = {}
        for c in usate:
            conf = CARTELLA_CARATTERI / f"{c}.conf"
            if not conf.is_file():
                preparazione.append(f"manca {conf.relative_to(RADICE)}")
                continue
            # Il percorso deve essere assoluto: con uno relativo fontconfig non trova il file
            # e torna in silenzio alla configurazione di sistema, cioè a una prova sbagliata.
            browser[c] = await p.chromium.launch(**kw, env=dict(os.environ, FONTCONFIG_FILE=str(conf)))
            famiglie = {f for f in in_uso if c in PER_FAMIGLIA[f] and f in PILA_FAMIGLIA}
            pile = [n for f in sorted(famiglie) for n in PILA_FAMIGLIA[f] if n in ATTESI[c]]
            if pile:
                usati = await caratteri_usati(browser[c], pile)
                for n in pile:
                    principale, tutti = usati[n]
                    if principale != ATTESI[c][n]:
                        preparazione.append(
                            f"con la serie «{c}» la pila delle {n} usa {tutti or 'nessun carattere'} "
                            f"invece di {ATTESI[c][n]}")
        if preparazione:
            for b in browser.values():
                await b.close()
            srv.shutdown()
            return errori, preparazione, 0

        semaforo = asyncio.Semaphore(paralleli)
        lavori = [(rel, fam, c) for rel, fam in voci for c in PER_FAMIGLIA[fam] if c in browser]

        def cartella(rel, fam, c):
            if png is None:
                return None
            nome = re.sub(r"[^A-Za-z0-9._-]+", "_", rel.removesuffix("index.html").strip("/") or "home")
            return png / nome / (c if fam != "sito" else "sito")

        async def uno(rel, fam, c):
            async with semaforo:
                return await stampa(browser[c], porta, rel, fam, cartella(rel, fam, c), sempre)

        # Pacchetti «Stampa tutto»: una pagina per pacchetto e serie, le sezioni una per volta.
        lavori_pacchetti = [(pk, ids, c) for pk, ids in sezioni.items()
                            for c in PER_FAMIGLIA["schede"] if c in browser]

        def png_sezione(pk, c):
            if png is None:
                return lambda sid: None
            nome = re.sub(r"[^A-Za-z0-9._-]+", "_", pk.removesuffix(".html"))
            return lambda sid: png / f"{nome}_{sid}" / c

        esiti, esiti_pacchetti = await asyncio.gather(
            asyncio.gather(*(uno(*x) for x in lavori)),
            asyncio.gather(*(stampa_pacchetto(browser[c], porta, pk, ids, semaforo,
                                              png_sezione(pk, c), sempre)
                             for pk, ids, c in lavori_pacchetti)))
        stampe = len(lavori) + sum(len(ids) for _, ids, _ in lavori_pacchetti)
        for b in browser.values():
            await b.close()
    srv.shutdown()

    visti_js, visti_apertura = set(), set()
    for (rel, fam, c), (fogli, js, apertura) in zip(lavori, esiti):
        if apertura:
            if rel not in visti_apertura:
                visti_apertura.add(rel)
                errori.append(f"{rel}: {apertura}")
            continue
        quali = f" con {CARATTERI[c]}" if fam != "sito" else ""
        bianchi, vuoti = problemi_fogli(fogli, fam)
        if bianchi:
            errori.append(f"{rel}: foglio bianco{quali} (n. {', '.join(map(str, bianchi))} di {len(fogli)})")
        elif vuoti:
            dett = ", ".join(f"n. {i} al {fogli[i - 1]:.0%}" for i in vuoti)
            errori.append(f"{rel}: foglio quasi vuoto{quali} ({len(fogli)} fogli; {dett})")
        for m in js:
            if (rel, m) not in visti_js:
                visti_js.add((rel, m))
                errori.append(f"{rel}: errore JavaScript: {m}")
    for (pk, ids, c), (per_sezione, js, apertura) in zip(lavori_pacchetti, esiti_pacchetti):
        if apertura and pk not in visti_apertura:
            visti_apertura.add(pk)
            errori.append(f"{pk}: {apertura}")
        for sid in ids:
            if sid not in per_sezione:
                continue
            fogli = per_sezione[sid]
            bianchi, vuoti = problemi_fogli(fogli, "schede")
            dove = f"{pk}#{sid}: nel pacchetto «Stampa tutto»"
            if bianchi:
                errori.append(f"{dove}, foglio bianco con {CARATTERI[c]} "
                              f"(n. {', '.join(map(str, bianchi))} di {len(fogli)})")
            elif vuoti:
                dett = ", ".join(f"n. {i} al {fogli[i - 1]:.0%}" for i in vuoti)
                errori.append(f"{dove}, foglio quasi vuoto con {CARATTERI[c]} ({len(fogli)} fogli; {dett})")
        for m in js:
            if (pk, m) not in visti_js:
                visti_js.add((pk, m))
                errori.append(f"{pk}: errore JavaScript: {m}")
    return errori, [], stampe


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--public", default="public")
    ap.add_argument("--da-git", metavar="BASE", help="solo le pagine toccate rispetto a BASE")
    ap.add_argument("--caratteri", default=",".join(CARATTERI),
                    help="serie di caratteri da usare, separate da virgole (predefinito: tutte)")
    ap.add_argument("--paralleli", type=int, default=max(2, min(6, (os.cpu_count() or 2) + 2)),
                    help="stampe contemporanee")
    ap.add_argument("--pagine", nargs="+", metavar="PAGINA",
                    help="solo queste pagine stampabili (percorso nel sito, es. "
                         "formazione/schede-stampabili/estate-sicura/); niente campione del sito")
    ap.add_argument("--png", metavar="CARTELLA",
                    help="salva i fogli in PNG: delle pagine con un problema, o di tutte quelle di --pagine")
    a = ap.parse_args()

    public = Path(a.public).resolve()
    if not public.is_dir():
        print(f"{public} non esiste: esegui prima la build Hugo.", file=sys.stderr)
        return 2
    serie = [c.strip() for c in a.caratteri.split(",") if c.strip()]
    sconosciute = [c for c in serie if c not in CARATTERI]
    if sconosciute or not serie:
        print(f"Serie di caratteri sconosciute: {', '.join(sconosciute) or 'nessuna indicata'} "
              f"(disponibili: {', '.join(CARATTERI)}).", file=sys.stderr)
        return 2
    pile = controlla_pile()
    if pile:
        for e in pile:
            print(f"❌ {e}", file=sys.stderr)
        return 2
    tutte = stampabili(public)
    sezioni = sezioni_pacchetti(public)
    if a.pagine:
        scelte, scelte_sez = {}, {}
        for pag in a.pagine:
            rel, _, frammento = pag.strip("/").partition("#")
            if rel in sezioni:          # un pacchetto intero, o una sua sezione
                if frammento and frammento not in sezioni[rel]:
                    print(f"{pag}: il pacchetto non ha la sezione «{frammento}».", file=sys.stderr)
                    return 2
                scelte_sez = unisci(scelte_sez, {rel: [frammento] if frammento else sezioni[rel]})
                continue
            rel = rel if rel.endswith(".html") else f"{rel}/index.html"
            if rel not in tutte:
                print(f"{pag} non è una pagina stampabile della build (schede, kit, storie, "
                      "moduli per le scuole, pacchetti «Stampa tutto»).", file=sys.stderr)
                return 2
            scelte[rel] = tutte[rel]
            # una scheda porta con sé le sue sezioni nei pacchetti
            parti = rel.split("/")
            if parti[:2] == ["formazione", "schede-stampabili"] and len(parti) == 4:
                scelte_sez = unisci(scelte_sez, sezioni_di(parti[2], sezioni))
        voci = sorted(scelte.items())
        pagine_sito = 0
    else:
        # Il campione di pagine del sito costa poco: si controlla sempre.
        scelte, scelte_sez = da_git(a.da_git, tutte, sezioni) if a.da_git else (tutte, sezioni)
        voci = sorted(scelte.items()) + [(p, "sito") for p in PAGINE_SITO]
        pagine_sito = len(PAGINE_SITO)
    png = Path(a.png).resolve() if a.png else None
    n_sezioni = sum(len(ids) for ids in scelte_sez.values())

    errori, preparazione, stampe = asyncio.run(controlla(public, voci, serie, a.paralleli,
                                                         png, bool(a.pagine), scelte_sez))
    if preparazione:
        print("❌ I caratteri della prova non sono quelli attesi:", file=sys.stderr)
        for e in preparazione:
            print(f"   - {e}", file=sys.stderr)
        print("Servono i pacchetti fonts-liberation fonts-inter fonts-texgyre fonts-dejavu-core "
              "fonts-noto-color-emoji; "
              "se ci sono, una cache di fontconfig può essere vecchia: vedi "
              "scripts/fogli-stampa/caratteri/LEGGIMI.md.", file=sys.stderr)
        return 2

    # Solo le serie che le pagine scelte hanno usato davvero: le schede, per esempio,
    # non si stampano con la serie dei kit.
    in_uso = {f for _, f in voci} | ({"schede"} if n_sezioni else set())
    usate = ", ".join(c for c in CARATTERI
                      if c in serie and any(c in PER_FAMIGLIA[f] for f in in_uso))
    print(f"Pagine stampate: {len(voci)} ({len(scelte)} schede, kit, storie e moduli per le scuole; "
          f"{pagine_sito} pagine del sito) e {n_sezioni} sezioni dei pacchetti «Stampa tutto», "
          f"{stampe} stampe con le serie di caratteri: {usate}")
    for e in errori:
        print(f"❌ {e}")
    if png is not None:
        print(f"Fogli salvati in PNG in {png}")
    if errori:
        print(f"\n{len(errori)} problemi. Un foglio quasi vuoto in una scheda si corregge riducendo "
              "la scala di stampa della sola scheda, al massimo del 12%, in modo che passi con tutte "
              "le serie, da sola e nel pacchetto «Stampa tutto» (vedi le schede già corrette: "
              "commento «controllo fogli di stampa»), o stringendo i suoi spazi; dopo una scala "
              "nuova si rigenerano i pacchetti (scripts/genera-pacchetti-schede.py). Per vedere i "
              "fogli: --pagine PAGINA --png CARTELLA.")
        return 1
    print("✅ Nessun foglio bianco o quasi vuoto, nessun errore JavaScript.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
