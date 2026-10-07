#!/usr/bin/env python3
"""
Controllo dei fogli di stampa: stampa davvero le pagine (Chromium, A4, media
print, come «Stampa» o «Salva come PDF» del browser) e guarda i fogli.

Nasce il 06/10/2026: una misura su tutte le pagine stampabili ha trovato 49
schede (quasi tutte dei kit calamità) che mandavano su un foglio in più la sola
fascia delle affiliazioni o una riga di fonti, e quattro pagine del sito che
finivano con un foglio bianco. Nessun controllo leggendo il codice se ne poteva
accorgere: si vede solo stampando (rule 09 § 15-ter).

Bloccante (exit 1):
  - un foglio completamente bianco, in qualunque posizione;
  - nelle schede, nei kit e nelle storie: un foglio quasi vuoto (meno
    dell'8% dell'altezza con qualcosa stampato), in qualunque posizione,
    quando i fogli sono più di uno. Fino al 07/10/2026 si guardava solo
    l'ultimo, e una scheda di tre pagine con la fascia delle affiliazioni da
    sola sul secondo foglio passava il controllo;
  - un errore JavaScript durante il caricamento della pagina.

Pagine controllate:
  - schede stampabili, schede dei kit calamità, storie (pagine HTML autonome
    in static/formazione/);
  - un campione fisso di pagine del sito (PAGINE_SITO), dove si guarda solo il
    foglio bianco: le pagine lunghe possono finire con poche righe.

Uso:
  python3 scripts/check-fogli-stampa.py [--public public]              # tutte
  python3 scripts/check-fogli-stampa.py --da-git origin/main   # solo ciò che la PR tocca
Con --da-git si controllano le pagine stampabili modificate; se cambia un foglio
di stile condiviso (print.css dei kit, scheda-print.css, storia-libro.css,
custom.css) si ricontrolla l'intera famiglia che lo usa.

Dipendenze: playwright (Chromium), pymupdf. Variabile CHROMIUM_PATH facoltativa.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import os
import re
import subprocess
import sys
import threading
from pathlib import Path

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
    # le pagine di rimando a un indirizzo nuovo non si stampano
    return {k: v for k, v in out.items()
            if not re.search(r'http-equiv=["\']?refresh', (public / k).read_text(errors="replace"), re.I)}


def da_git(base: str, tutte: dict[str, str]) -> dict[str, str]:
    diff = subprocess.run(["git", "diff", "--name-only", f"{base}...HEAD"],
                          capture_output=True, text=True, check=True).stdout.split()
    famiglie = {FAMIGLIE[f] for f in diff if f in FAMIGLIE}
    if "tutte" in famiglie:
        return tutte
    scelte = {k: v for k, v in tutte.items() if v in famiglie}
    for f in diff:
        if f.startswith("static/") and f.endswith(".html"):
            rel = f[len("static/"):]
            if rel in tutte:
                scelte[rel] = tutte[rel]
    return scelte


def riempimento(pagina) -> float:
    """Frazione delle righe di pixel con qualcosa stampato (0 = foglio bianco)."""
    pix = pagina.get_pixmap(dpi=30, colorspace="gray")
    w, h, s = pix.width, pix.height, pix.samples
    piene = sum(1 for y in range(h) if min(s[y * w:(y + 1) * w]) < 235)
    return piene / h


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--public", default="public")
    ap.add_argument("--da-git", metavar="BASE", help="solo le pagine toccate rispetto a BASE")
    a = ap.parse_args()

    import pymupdf
    from playwright.sync_api import sync_playwright

    public = Path(a.public).resolve()
    if not public.is_dir():
        print(f"{public} non esiste: esegui prima la build Hugo.", file=sys.stderr)
        return 2
    tutte = stampabili(public)
    # Il campione di pagine del sito costa mezzo minuto: si controlla sempre.
    scelte = da_git(a.da_git, tutte) if a.da_git else tutte
    sito = PAGINE_SITO

    class Silenzioso(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0),
                                          functools.partial(Silenzioso, directory=str(public)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    porta = srv.server_address[1]

    errori: list[str] = []
    voci = [(k, v) for k, v in scelte.items()] + [(p, "sito") for p in sito]
    with sync_playwright() as p:
        kw = {"executable_path": os.environ["CHROMIUM_PATH"]} if os.environ.get("CHROMIUM_PATH") else {}
        browser = p.chromium.launch(**kw)
        for rel, fam in voci:
            pagina = browser.new_page()
            js: list[str] = []
            pagina.on("pageerror", lambda e, js=js: js.append(str(e).splitlines()[0][:160]))
            url = f"http://127.0.0.1:{porta}/{rel[:-len('index.html')] if rel.endswith('index.html') else rel}"
            try:
                risposta = pagina.goto(url, wait_until="load", timeout=45000)
                if risposta is None or risposta.status >= 400:
                    # una pagina d'errore stampa bene: senza questo controllo
                    # un indirizzo del campione sparito passerebbe per verificato
                    errori.append(f"{rel}: la pagina non esiste (HTTP {risposta.status if risposta else '—'})")
                    pagina.close()
                    continue
                pagina.emulate_media(media="print")
                doc = pymupdf.open(stream=pagina.pdf(format="A4", prefer_css_page_size=True,
                                                     print_background=True), filetype="pdf")
            except Exception as e:  # pagina che non si apre: è un errore anche quello
                errori.append(f"{rel}: la pagina non si stampa ({str(e).splitlines()[0][:120]})")
                pagina.close()
                continue
            fogli = [riempimento(pg) for pg in doc]
            bianchi = [i + 1 for i, r in enumerate(fogli) if r == 0]
            if bianchi:
                errori.append(f"{rel}: foglio bianco (n. {', '.join(map(str, bianchi))} di {len(fogli)})")
            elif fam != "sito" and len(fogli) > 1:
                # Ogni foglio, non solo l'ultimo: una pagina che sfora di pochi
                # millimetri manda la sola fascia delle affiliazioni sul foglio
                # dopo, e se la scheda ha più pagine quel foglio sta in mezzo.
                vuoti = [i + 1 for i, r in enumerate(fogli) if r < SOGLIA_VUOTO]
                if vuoti:
                    dett = ", ".join(f"n. {i} al {fogli[i - 1]:.0%}" for i in vuoti)
                    errori.append(f"{rel}: foglio quasi vuoto ({len(fogli)} fogli; {dett})")
            for m in js:
                errori.append(f"{rel}: errore JavaScript: {m}")
            pagina.close()
        browser.close()
    srv.shutdown()

    print(f"Pagine stampate: {len(voci)} ({len(scelte)} schede, kit e storie; {len(sito)} pagine del sito)")
    for e in errori:
        print(f"❌ {e}")
    if errori:
        print(f"\n{len(errori)} problemi. Un foglio quasi vuoto in una scheda si "
              "corregge riducendo la scala di stampa della sola scheda (vedi le schede già "
              "corrette: commento «controllo fogli di stampa») o stringendo i suoi spazi.")
        return 1
    print("✅ Nessun foglio bianco o quasi vuoto, nessun errore JavaScript.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
