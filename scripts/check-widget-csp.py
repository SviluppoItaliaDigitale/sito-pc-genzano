#!/usr/bin/env python3
"""Ogni widget esterno ({{< external-widget >}}) deve poter caricarsi con la CSP.

L'iframe di un widget click-to-load si carica solo se il suo dominio è nella
direttiva frame-src della Content-Security-Policy di .htaccess (valida solo su
Aruba, mai su GitHub Pages né in locale: per questo nessuna prova lo vedeva).
Il 31/10/2026 un audit esterno ha trovato il riquadro di MeteoAM bloccato in
/allerte-meteo/ (A06), e lo stesso valeva per la mappa Blitzortung in
/rischi-prevenzione/temporali-intensi/.

Uso: python3 scripts/check-widget-csp.py — esce con 1 se un dominio manca.
"""
import re
import sys
from pathlib import Path

HTACCESS = Path("themes/flavour-pcgenzano/static/.htaccess")


def frame_src():
    for riga in HTACCESS.read_text(encoding="utf-8").splitlines():
        if "Content-Security-Policy" in riga and not riga.lstrip().startswith("#"):
            m = re.search(r"frame-src ([^;\"]+)", riga)
            if m:
                return m.group(1).split()
    sys.exit("frame-src non trovata nella CSP di .htaccess")


def ammesso(origine, regole):
    host = origine.split("://", 1)[1]
    for r in regole:
        r = r.strip("'")
        if r in ("*", origine):
            return True
        if r.startswith("https://*.") and origine.startswith("https://") and host.endswith(r[len("https://*"):]):
            return True
    return False


def main():
    regole = frame_src()
    errori = []
    for f in sorted(Path("content").rglob("*.md")):
        testo = f.read_text(encoding="utf-8")
        for m in re.finditer(r"\{\{<\s*external-widget(.*?)>\}\}", testo, re.S):
            src = re.search(r'\bsrc="(https?://[^/"#?]+)', m.group(1))
            if src and not ammesso(src.group(1), regole):
                riga = testo[: m.start()].count("\n") + 1
                errori.append(f"{f}:{riga}: {src.group(1)} non è in frame-src: il riquadro resterebbe bloccato")
    for e in errori:
        print(e)
    print(f"{len(errori)} widget con dominio non ammesso dalla CSP.")
    return 1 if errori else 0


if __name__ == "__main__":
    sys.exit(main())
