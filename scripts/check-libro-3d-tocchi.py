#!/usr/bin/env python3
"""Prova del tocco nel «Libro che si esplora»: in ogni capitolo, il tocco al centro di ogni
oggetto toccabile deve prendere proprio quell'oggetto, e nessun comando deve dare errori.

Nasce l'08/11/2026: il raggio del tocco colpiva i contorni (linee) di tutta la scena e in 11
capitoli su 15 il tocco andava all'oggetto più vicino alla telecamera (nello zaino ogni oggetto
rispondeva come la candela). La build e tutti i controlli erano verdi.

Uso: python3 scripts/check-libro-3d-tocchi.py --public public [--pagine /formazione/libro-che-si-esplora/ ...]
Serve la cartella della build (costruita con baseURL di produzione, percorsi dalla radice) e
Playwright con Chromium. Per leggere la scena lo script aggiunge in coda a libro-3d.js, solo nel
browser della prova, una riga che espone current, camera, renderer, goTo, chapter, CH, THREE e
hitAt: se uno di questi nomi cambia nello script del libro, la prova si ferma e va aggiornata.
Esce con 1 se un oggetto non risponde o c'è un errore JavaScript, con 2 se la prova non parte.
"""
import argparse, functools, http.server, sys, threading
from pathlib import Path

PAGINE = ["/formazione/libro-che-si-esplora/", "/formazione/libro-che-si-esplora-facile/"]
ESPONI = ("\nwindow.__lb={get current(){return current},camera,renderer,goTo,"
          "get chapter(){return chapter},CH,THREE,hitAt};\n")
MISURA = """()=>{const L=__lb, T=L.THREE, r=L.renderer.domElement.getBoundingClientRect(), visti={};
  L.current.g.updateMatrixWorld(true);
  L.current.g.traverse(o=>{ if(!o.isMesh||o.userData.pick===undefined) return;
    for(let q=o;q;q=q.parent) if(q.visible===false) return;
    const c=new T.Box3().setFromObject(o).getCenter(new T.Vector3()).project(L.camera);
    if (Math.abs(c.x)>1||Math.abs(c.y)>1) return;
    const id=o.userData.pick, x=r.left+(c.x+1)/2*r.width, y=r.top+(1-c.y)/2*r.height;
    (visti[id]=visti[id]||[]).push(L.hitAt({clientX:x,clientY:y})===id); });
  return {chiave:L.CH[L.chapter].key, oggetti:Object.keys(visti).length,
          mancati:Object.keys(visti).filter(k=>!visti[k].some(Boolean))};}"""


class Silenzioso(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A002 (nome del metodo di base)
        pass


def main():
    ap = argparse.ArgumentParser(description="Prova del tocco nel «Libro che si esplora».")
    ap.add_argument("--public", default="public")
    ap.add_argument("--pagine", nargs="*", default=PAGINE)
    a = ap.parse_args()
    radice = Path(a.public)
    if not (radice / PAGINE[0].strip("/") / "index.html").exists():
        print(f"::error::Build non trovata in {radice}: manca {PAGINE[0]}"); return 2
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("::error::Playwright non installato (pip install playwright; playwright install chromium)"); return 2

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Silenzioso, directory=str(radice)))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_address[1]}"
    problemi = 0
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader"])
        for pagina in a.pagine:
            pg = b.new_page(viewport={"width": 1280, "height": 800})
            errori = []
            pg.on("pageerror", lambda e: errori.append(str(e)))
            pg.route("**/js/libro-3d.js*", lambda route: route.fulfill(
                response=(r := route.fetch()), body=r.text() + ESPONI))
            pg.goto(base + pagina)
            try:
                pg.wait_for_function("window.__lb && __lb.current", timeout=30000)
            except Exception:
                print(f"::error::{pagina}: il libro non è partito (o i nomi interni sono cambiati). Errori: {errori}")
                problemi += 1; pg.close(); continue
            pg.wait_for_timeout(2500)
            n = pg.evaluate("__lb.CH.length")
            for i in range(n):
                pg.evaluate(f"__lb.goTo({i})")
                pg.wait_for_function(f"__lb.chapter==={i}", timeout=20000); pg.wait_for_timeout(1500)  # pop-up finito
                ris = pg.evaluate(MISURA)
                # ogni comando del pannello si preme una volta: deve funzionare senza errori
                for k in range(pg.locator("#lb-tools button").count()):
                    pg.locator("#lb-tools button").nth(k).click(); pg.wait_for_timeout(250)
                esito = "ok" if not ris["mancati"] else f"NON rispondono: {', '.join(ris['mancati'])}"
                print(f"{pagina} capitolo {i+1} ({ris['chiave']}): {ris['oggetti']} oggetti toccabili, {esito}")
                if ris["mancati"]:
                    problemi += 1
                    print(f"::error::{pagina} capitolo {i+1}: il tocco non prende {', '.join(ris['mancati'])}")
            for e in errori:
                problemi += 1; print(f"::error::{pagina}: errore JavaScript: {e}")
            pg.close()
        b.close()
    srv.shutdown()
    print("Prova del tocco: " + ("nessun problema." if not problemi else f"{problemi} problemi."))
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
