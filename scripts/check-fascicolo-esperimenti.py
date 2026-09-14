#!/usr/bin/env python3
"""Controlla il fascicolo stampabile degli esperimenti come esce dalla stampante.

Nasce dagli errori del 14/09/2026, tutti dello stesso tipo: difetti che **nessun
controllo testuale può vedere**, perché dipendono da come il browser impagina.
In quella giornata sono andati live, o stavano per andarci:

- il fascicolo a 66 pagine invece di 33 (un foglio bianco dopo ogni scheda),
  perché l'area stampabile non è il foglio intero: `@page` di scheda-print.css
  tiene 5mm di margine per lato e ne restano 28,7cm;
- 12 schede su due pagine, perché una figura flottata a destra su un contenitore
  flex non flotta affatto e si prende una riga intera;
- due didascalie **tagliate** dal riquadro del disegno, che l'SVG ritaglia in
  silenzio: nessun errore, solo testo mozzato sul foglio;
- due etichette sovrapposte, fuse in una parola sola.

L'ultimo difetto era sfuggito a una verifica fatta su una pagina di prova
**senza il font delle schede**: con metriche diverse le scritte sembravano
starci. Per questo qui si misura sulla pagina vera, con il suo foglio di stile,
in `media=print`.

    python3 scripts/check-fascicolo-esperimenti.py

Exit code = numero di problemi trovati.
"""

from __future__ import annotations

import http.server
import socketserver
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"
PAGINA = "/formazione/schede-stampabili/esperimenti-protezione-civile/"
PORTA = 8931

# A4 alto 29,7cm meno i 5mm per lato di `@page`: è questo che decide se una
# scheda sta su un foglio, non l'altezza del foglio.
AREA_STAMPABILE_MM = 287
PX_PER_MM = 96 / 25.4


class _Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        rel = path.split("?", 1)[0].split("#", 1)[0].lstrip("/")
        p = STATIC / rel
        if p.is_dir():
            p = p / "index.html"
        return str(p)

    def log_message(self, *a):
        pass


def _servi():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", PORTA), _Handler) as httpd:
        httpd.serve_forever()


# Misura tutto in una volta sola, nel browser, sulla pagina vera.
JS = """
(limite) => {
  const out = {schede: [], tagliate: [], sovrapposte: [], senzaDescrizione: [], alte: []};
  document.querySelectorAll('.scheda-page').forEach(p => {
    const titolo = (p.querySelector('.scheda-titolo-principale') || {}).textContent || '?';
    const nome = titolo.trim();
    out.schede.push(nome);

    const h = p.getBoundingClientRect().height;
    if (h > limite + 1) out.alte.push({nome, h: Math.round(h), limite: Math.round(limite)});

    const svg = p.querySelector('.esp-figura svg');
    if (!svg) { out.senzaDescrizione.push({nome, perche: 'nessuna illustrazione'}); return; }
    const alt = svg.getAttribute('aria-label');
    if (svg.getAttribute('role') !== 'img' || !alt || alt.trim().length < 20)
      out.senzaDescrizione.push({nome, perche: 'role/aria-label assente o troppo breve'});

    const vb = svg.viewBox.baseVal;
    const testi = [...svg.querySelectorAll('text')].map(e => ({s: e.textContent, b: e.getBBox()}));
    testi.forEach(t => {
      const fuori = Math.max(vb.x - t.b.x, t.b.x + t.b.width - (vb.x + vb.width));
      if (fuori > 0.5) out.tagliate.push({nome, s: t.s, fuori: +fuori.toFixed(1)});
    });
    for (let i = 0; i < testi.length; i++)
      for (let j = i + 1; j < testi.length; j++) {
        const A = testi[i].b, B = testi[j].b;
        const ox = Math.min(A.x + A.width, B.x + B.width) - Math.max(A.x, B.x);
        const oy = Math.min(A.y + A.height, B.y + B.height) - Math.max(A.y, B.y);
        if (ox > 0 && oy > 0)
          out.sovrapposte.push({nome, s: testi[i].s + ' / ' + testi[j].s, q: +ox.toFixed(1)});
      }
  });
  return out;
}
"""


def _esperimenti_attesi() -> int:
    """Quanti esperimenti dichiara il generatore: il fascicolo deve avere altrettanti fogli."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("gen", ROOT / "scripts/genera-schede-esperimenti.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["gen"] = mod
    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        pass
    return len(mod.ESPERIMENTI)


def main() -> int:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Serve Playwright:  pip install playwright && playwright install chromium")
        return 1

    attesi = _esperimenti_attesi()
    threading.Thread(target=_servi, daemon=True).start()
    limite = AREA_STAMPABILE_MM * PX_PER_MM

    import os
    exe = os.environ.get("CHROMIUM_PATH")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=exe or None, args=["--no-sandbox"])
        pagina = browser.new_page(viewport={"width": 794, "height": 1123})
        pagina.goto(f"http://127.0.0.1:{PORTA}{PAGINA}", wait_until="load", timeout=60000)
        pagina.wait_for_timeout(800)
        pagina.emulate_media(media="print")   # la stampa è il formato che conta
        pagina.wait_for_timeout(400)
        d = pagina.evaluate(JS, limite)
        browser.close()

    problemi = 0
    print(f"Fascicolo esperimenti — {len(d['schede'])} schede, {attesi} esperimenti attesi")

    if len(d["schede"]) != attesi:
        problemi += 1
        print(f"❌ Schede ({len(d['schede'])}) diverse dagli esperimenti ({attesi}).")

    if d["alte"]:
        problemi += len(d["alte"])
        print(f"❌ {len(d['alte'])} schede più alte dell'area stampabile "
              f"({AREA_STAMPABILE_MM}mm): finirebbero su due fogli.")
        for x in d["alte"]:
            print(f"     {x['h']}px (max {x['limite']}px)  {x['nome']}")

    if d["tagliate"]:
        problemi += len(d["tagliate"])
        print(f"❌ {len(d['tagliate'])} scritte tagliate dal riquadro del disegno "
              f"(l'SVG ritaglia in silenzio):")
        for x in d["tagliate"]:
            print(f"     fuori di {x['fuori']}  «{x['s']}»  [{x['nome']}]")

    if d["sovrapposte"]:
        problemi += len(d["sovrapposte"])
        print(f"❌ {len(d['sovrapposte'])} scritte sovrapposte fra loro:")
        for x in d["sovrapposte"]:
            print(f"     per {x['q']}  «{x['s']}»  [{x['nome']}]")

    if d["senzaDescrizione"]:
        problemi += len(d["senzaDescrizione"])
        print(f"❌ {len(d['senzaDescrizione'])} figure senza descrizione equivalente "
              f"(chi non vede il disegno resta senza):")
        for x in d["senzaDescrizione"]:
            print(f"     {x['perche']}  [{x['nome']}]")

    if not problemi:
        print("✅ Un foglio per esperimento, nessuna scritta tagliata o sovrapposta, "
              "ogni figura ha la sua descrizione.")
    return problemi


if __name__ == "__main__":
    sys.exit(main())
