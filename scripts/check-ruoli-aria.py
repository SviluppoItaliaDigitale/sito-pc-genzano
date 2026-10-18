#!/usr/bin/env python3
"""
Controllo dei ruoli ARIA che cancellano la semantica di un comando.

Un <button>, un <a>, un campo o un <summary> sono già comandi per i lettori
di schermo. Un attributo role="listitem" (o "presentation", "none", "img",
"heading"…) su questi elementi sostituisce il ruolo nativo: il pulsante
smette di essere annunciato come pulsante (WCAG 4.1.2). Cerca questi casi
nei template del tema, nel JavaScript del tema e nelle pagine statiche,
compreso l'HTML costruito come stringa dentro il JavaScript, che axe non
vede finché nessuno apre quella vista.

Nasce il 17/10/2026: un audit esterno ha trovato i pulsanti dell'assistente
virtuale con role="listitem"; il gate pa11y-ci non apre l'assistente e
nessun controllo leggeva il codice che li costruisce.

Uso: python3 scripts/check-ruoli-aria.py [file ...]
Exit code = numero di casi trovati (0 = nessuno). Solo Python standard.
"""

from __future__ import annotations

import re
import sys
from fnmatch import fnmatch
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PERIMETRO = [
    ("themes/flavour-pcgenzano/layouts", "*.html"),
    ("themes/flavour-pcgenzano/static/js", "*.js"),
    ("layouts", "*.html"),
    ("static", "*.html"),
    ("static", "*.js"),
]
ESCLUSI = [
    "static/vendor/*",
    "themes/flavour-pcgenzano/static/vendor/*",
    "static/formazione/schede-stampabili/pacchetti/*",
    "static/pagefind/*",
    "static/open-kit/*",
]

# Ruoli che tolgono a un comando la sua natura di comando.
VIETATI = {
    "listitem", "list", "presentation", "none", "img", "heading", "article",
    "region", "group", "row", "cell", "gridcell", "columnheader", "rowheader",
    "status", "alert", "note", "tooltip", "document", "main", "navigation",
    "banner", "contentinfo", "complementary", "form", "search", "table",
    "grid", "generic", "paragraph",
}
TAG = re.compile(
    r"<(button|a|input|select|textarea|summary)\b([^<>]*?)\brole\s*=\s*\\?[\"']([a-z ]+)\\?[\"']",
    re.I | re.S,
)


def file_da_controllare(argv: list[str]) -> list[Path]:
    if argv:
        return [Path(a).resolve() for a in argv if Path(a).suffix in (".html", ".js")]
    out = []
    for cartella, schema in PERIMETRO:
        base = ROOT / cartella
        if base.is_dir():
            out.extend(base.rglob(schema))
    return out


def main(argv: list[str]) -> int:
    trovati = 0
    for f in sorted(set(file_da_controllare(argv))):
        try:
            rel = f.relative_to(ROOT).as_posix()
        except ValueError:
            rel = f.as_posix()
        if any(fnmatch(rel, e) for e in ESCLUSI):
            continue
        testo = f.read_text(encoding="utf-8", errors="replace")
        for m in TAG.finditer(testo):
            ruoli = set(m.group(3).lower().split())
            male = ruoli & VIETATI
            if not male:
                continue
            riga = testo.count("\n", 0, m.start()) + 1
            print(f"{rel}:{riga}: <{m.group(1)}> con role=\"{m.group(3)}\": "
                  f"il comando perde il suo ruolo nativo. Se serve una lista, "
                  f"metti il comando dentro un elemento con role=\"listitem\" (o in un <li>).")
            trovati += 1
    if trovati:
        print(f"\n{trovati} comando/i con un ruolo ARIA che ne cancella la semantica.")
    else:
        print("Ruoli ARIA dei comandi: nessun problema.")
    return min(trovati, 255)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
