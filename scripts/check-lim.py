#!/usr/bin/env python3
"""
Prova «da LIM»: apre le pagine per le scuole come le apre una lavagna interattiva
(schermo touch, niente mouse né tastiera, proiettore a 1024x768 e 1366x768) e
blocca ciò che in classe non si può usare.

Nasce l'01/11/2026 dalle segnalazioni delle scuole («sulle LIM i contenuti non
vanno bene»). La verifica di quel giorno ha trovato: un gioco che col solo dito
non si poteva giocare (solo trascinamento col mouse), un gioco dove il tocco
selezionava e subito deselezionava, pulsanti da 30x22 px, la barra per il
telefono che copriva i giochi dell'infanzia, etichette che uscivano dallo
schermo. La compatibilità con i browser vecchi delle lavagne la controlla
scripts/check-sintassi-js.cjs; la prova con un browser del 2018 è in
scripts/check-lim-browser-vecchio.cjs (giro settimanale).

Bloccante (exit 1), a ciascuna delle due larghezze:
  - un errore JavaScript durante il caricamento;
  - la pagina più larga dello schermo (barra di scorrimento orizzontale);
  - nei giochi e nei quiz: un comando (pulsante, carta, casella…) con un lato
    sotto i 24 px (WCAG 2.2, 2.5.8); per una casella o un pulsante di scelta
    conta l'etichetta, che è ciò che si tocca;
  - un gioco che usa il trascinamento HTML5 (dragstart) senza dichiarare
    un'alternativa al tocco: nel codice deve esserci il segno
    «alternativa-al-trascinamento» accanto a ciò che la realizza (tocco e
    posa, frecce, trascinamento con pointer events). Il trascinamento HTML5 col
    dito, sulle lavagne, spesso non parte.
Avviso (non blocca): comandi dei giochi fra 24 e 40 px (per un bambino sulla
lavagna servono almeno 40-44 px).
Exit 2: build mancante o Playwright assente.

Uso:
  python3 scripts/check-lim.py [--public public]            tutte le pagine per le scuole
  python3 scripts/check-lim.py --da-git origin/main          solo le pagine toccate (PR)
  python3 scripts/check-lim.py --pagine /giochi/primaria/memory/
Le richieste al dominio di produzione (site-chrome.js carica da lì alcune
risorse) sono servite dalla build locale.
"""
from __future__ import annotations

import argparse
import asyncio
import functools
import http.server
import re
import subprocess
import sys
import threading
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
PRODUZIONE = "https://www.protezionecivilegenzano.it"
SCHERMI = [(1024, 768), (1366, 768)]
SEGNO_ALTERNATIVA = "alternativa-al-trascinamento"

# Pagine Hugo per la scuola (le autonome di static/ si trovano da sole).
PAGINE_HUGO = [
    "/formazione/", "/formazione/crea-la-mia-lezione/", "/formazione/percorsi-didattici/",
    "/formazione/kit-scuola-infanzia/", "/formazione/kit-scuola-primaria/",
    "/formazione/kit-scuola-secondaria-primo-grado/", "/formazione/kit-scuola-secondaria-secondo-grado/",
    "/formazione/kit-calamita/", "/formazione/esperimenti/", "/formazione/libro-che-si-esplora/",
    "/formazione/libro-che-si-esplora-facile/", "/formazione/libro-che-si-esplora-schede/",
    "/giochi/", "/laboratorio-meteo/", "/quiz-preparazione/", "/tabelle-comunicazione/",
    "/formazione/storie-e-racconti/", "/formazione/schede-stampabili/",
]
# Cartelle di static/ con pagine per la scuola: cambiare un file condiviso di una
# famiglia (CSS, JS comuni) ricontrolla tutta la famiglia.
FAMIGLIE = {
    "giochi": "static/giochi/",
    "schede": "static/formazione/schede-stampabili/",
    "kit": "static/formazione/kit-calamita-",
    "storie": "static/formazione/storie-e-racconti/",
    "scuole": "static/scuole/",
    "abili": "static/abili-a-proteggere/",
    "quizpc": "static/quizpc/",
    "formazionepc": "static/formazionepc/",
}
CONDIVISI_TUTTO = (
    "static/app-shared/", "static/vendor/bootstrap-italia/", "themes/flavour-pcgenzano/static/css/custom.css",
    "themes/flavour-pcgenzano/static/css/a11y-toolbar.css", "themes/flavour-pcgenzano/static/js/a11y-toolbar.js",
    "themes/flavour-pcgenzano/layouts/_default/baseof.html", "scripts/check-lim.py", "hugo.toml",
)
GIOCHI = re.compile(r"^/(giochi/(infanzia|primaria|ragazzi)/[^/]+/|quizpc/|formazionepc/|quiz-preparazione/)")


def pagine_static(public: Path) -> list[str]:
    out = []
    for cartella in ("giochi", "formazione/schede-stampabili", "formazione/storie-e-racconti", "scuole",
                     "abili-a-proteggere", "quizpc", "formazionepc"):
        for f in sorted((public / cartella).rglob("index.html")):
            rel = "/" + f.relative_to(public).as_posix()
            if "/pacchetti/" in rel:
                continue
            out.append(rel[: -len("index.html")])
    for f in sorted(public.glob("formazione/kit-calamita-*/*.html")):
        out.append("/" + f.relative_to(public).as_posix().replace("index.html", ""))
    return out


def url_di(path: str) -> str | None:
    """Indirizzo pubblico di un file del repository, se è una pagina per la scuola."""
    if path.startswith("static/") and path.endswith(".html"):
        u = "/" + path[len("static/"):]
        return u[: -len("index.html")] if u.endswith("index.html") else u
    m = re.match(r"content/(formazione|giochi|laboratorio-meteo|quiz-preparazione|tabelle-comunicazione)(/.*)?\.md$", path)
    if m:
        u = "/" + path[len("content/"):-len(".md")]
        u = re.sub(r"/_index$", "", u)
        return u.rstrip("/") + "/"
    return None


def da_git(base: str, tutte: list[str]) -> list[str]:
    diff = subprocess.run(["git", "diff", "--name-only", f"{base}...HEAD"], cwd=RADICE,
                          capture_output=True, text=True, check=True).stdout.split()
    if any(p.startswith(CONDIVISI_TUTTO) for p in diff):
        return tutte
    scelte: set[str] = set()
    for p in diff:
        for pref in FAMIGLIE.values():
            # un file condiviso della famiglia (non una pagina): tutta la famiglia
            if p.startswith(pref) and not p.endswith(".html"):
                scelte.update(u for u in tutte if u.startswith("/" + pref[len("static/"):]))
        u = url_di(p)
        if u and u in tutte:
            scelte.add(u)
        if p.startswith("themes/") and ("shortcodes" in p or "partials" in p or "/static/js/" in p):
            scelte.update(PAGINE_HUGO)
    return sorted(scelte)


SONDA = r"""(giochi) => {
  const vis = e => { const s = getComputedStyle(e), r = e.getBoundingClientRect();
    return s.visibility !== 'hidden' && s.display !== 'none' && r.width > 0 && r.height > 0; };
  const W = innerWidth;
  const ox = document.documentElement.scrollWidth - W;
  let largo = '';
  if (ox > 1) document.querySelectorAll('body *').forEach(e => { const r = e.getBoundingClientRect();
    if (!largo && r.right > W + 1 && r.width > 0 && getComputedStyle(e).position !== 'fixed')
      largo = e.tagName.toLowerCase() + (e.className && typeof e.className === 'string' ? '.' + e.className.split(' ')[0] : ''); });
  const piccoli = [], medi = [];
  if (giochi) {
    const sel = 'button, [role=button], a[href], input:not([type=hidden]), select, summary, [tabindex="0"]';
    document.querySelectorAll(sel).forEach(e => {
      if (!vis(e) || e.closest('header, footer, nav, .it-header-wrapper, .bottom-nav, #a11yToolbar, .a11y-dialog, .sos-modal, #gioco-comandi, .cookiebar, .breadcrumb')) return;
      const cs = getComputedStyle(e);
      if (e.tagName === 'A' && cs.display === 'inline' && e.closest('p, li, td, small, figcaption')) return;
      let r = e.getBoundingClientRect();
      if ((e.type === 'checkbox' || e.type === 'radio') && e.labels && e.labels[0]) r = e.labels[0].getBoundingClientRect();
      const m = Math.min(r.width, r.height);
      const nome = (e.getAttribute('aria-label') || e.textContent || e.id || '').trim().replace(/\s+/g, ' ').slice(0, 30);
      const d = Math.round(r.width) + 'x' + Math.round(r.height) + ' «' + nome + '»';
      if (m < 24) piccoli.push(d); else if (m < 40) medi.push(d);
    });
  }
  return { ox, largo, piccoli: piccoli.slice(0, 5), npiccoli: piccoli.length, medi: medi.slice(0, 3), nmedi: medi.length };
}"""


def trascinamento_senza_alternativa(public: Path, url: str) -> bool:
    f = public / (url.lstrip("/") + ("index.html" if url.endswith("/") else ""))
    if not f.is_file():
        return False
    testo = f.read_text(encoding="utf-8", errors="replace")
    # anche gli script esterni della stessa cartella (js/script.js)
    for js in f.parent.rglob("*.js"):
        testo += js.read_text(encoding="utf-8", errors="replace")
    return "dragstart" in testo and SEGNO_ALTERNATIVA not in testo


async def prova(public: Path, pagine: list[str]) -> tuple[list[str], list[str]]:
    from playwright.async_api import async_playwright

    class Silenzioso(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Silenzioso, directory=str(public)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    errori, avvisi = [], []

    async def da_locale(route):
        percorso = route.request.url[len(PRODUZIONE):].split("?")[0].split("#")[0]
        f = public / percorso.lstrip("/")
        if f.is_dir():
            f = f / "index.html"
        if f.is_file():
            await route.fulfill(path=str(f))
        else:
            await route.abort()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for w, h in SCHERMI:
            ctx = await browser.new_context(viewport={"width": w, "height": h}, has_touch=True, is_mobile=False)
            await ctx.route(PRODUZIONE + "/**", da_locale)
            pagina = await ctx.new_page()
            js: list[str] = []
            pagina.on("pageerror", lambda e: js.append(str(e).splitlines()[0][:160]))
            for u in pagine:
                js.clear()
                try:
                    await pagina.goto(base + u, wait_until="load", timeout=30000)
                    await pagina.wait_for_timeout(300)
                    r = await pagina.evaluate(SONDA, bool(GIOCHI.match(u)))
                except Exception as e:  # noqa: BLE001
                    errori.append(f"{u} [{w}x{h}] pagina non caricata: {str(e).splitlines()[0][:120]}")
                    continue
                for e in js:
                    errori.append(f"{u} [{w}x{h}] errore JavaScript: {e}")
                if r["ox"] > 1:
                    errori.append(f"{u} [{w}x{h}] più larga dello schermo di {r['ox']} px (prima a uscire: {r['largo']})")
                if r["npiccoli"]:
                    errori.append(f"{u} [{w}x{h}] {r['npiccoli']} comandi sotto i 24 px: {'; '.join(r['piccoli'])}")
                if r["nmedi"] and w == SCHERMI[0][0]:
                    avvisi.append(f"{u} {r['nmedi']} comandi fra 24 e 40 px: {'; '.join(r['medi'])}")
            await ctx.close()
        await browser.close()
    srv.shutdown()
    for u in pagine:
        if GIOCHI.match(u) and trascinamento_senza_alternativa(public, u):
            errori.append(f"{u} usa il trascinamento HTML5 senza alternativa al tocco dichiarata "
                          f"(segno «{SEGNO_ALTERNATIVA}» nel codice)")
    return errori, avvisi


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--public", default="public")
    ap.add_argument("--da-git", metavar="BASE")
    ap.add_argument("--pagine", nargs="+")
    a = ap.parse_args()
    public = (RADICE / a.public).resolve() if not Path(a.public).is_absolute() else Path(a.public)
    if not (public / "index.html").is_file():
        print(f"Build mancante in {public}: esegui prima hugo.", file=sys.stderr)
        return 2
    try:
        import playwright  # noqa: F401
    except ImportError:
        print("Playwright mancante: pip install playwright && playwright install chromium", file=sys.stderr)
        return 2
    tutte = [u for u in PAGINE_HUGO + pagine_static(public)
             if (public / u.lstrip("/")).exists() or (public / (u.lstrip("/") + "index.html")).exists()]
    pagine = a.pagine or (da_git(a.da_git, tutte) if a.da_git else tutte)
    if not pagine:
        print("Nessuna pagina per le scuole toccata: niente da provare.")
        return 0
    print(f"Prova da LIM (touch, {', '.join(f'{w}x{h}' for w, h in SCHERMI)}) su {len(pagine)} pagine…")
    errori, avvisi = asyncio.run(prova(public, pagine))
    for x in avvisi[:30]:
        print(f"::warning::{x}")
    if errori:
        print(f"❌ {len(errori)} problemi che sulla lavagna interattiva impediscono o rendono difficile l'uso:")
        for e in errori:
            print("  - " + e)
        return 1
    print(f"✅ Pagine usabili sulla LIM ({len(pagine)} pagine, {len(avvisi)} avvisi).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
