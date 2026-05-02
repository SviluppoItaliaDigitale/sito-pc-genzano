#!/usr/bin/env python3
"""Rimuove la riga `# TODO-foto-*: ...` dal frontmatter di un articolo.

Usato dal workflow scarica-foto-automatica.yml quando lo script di download
foto fallisce: invece di lasciare il marker pendente (che ri-fallirà ad ogni
run aprendo nuove issue), lo si rimuove e si lascia che auto-cover-mancanti.py
generi la cover tipografica come fallback definitivo.

L'utente che vuole comunque la foto da una fonte può ri-aggiungere il marker
manualmente con titolo/query diversa o con un'altra fonte (NASA, USGS, NOAA,
Pexels, Pixabay, Unsplash).

Uso:
  python3 scripts/rimuovi-marker-foto.py <path-articolo.md>

Exit code: 0 se il marker era presente ed è stato rimosso, 1 se nessun marker
trovato (no-op), 2 se errore di lettura/scrittura.
"""
import re
import sys
from pathlib import Path

PATTERN = re.compile(
    r'^# TODO-foto-(?:wikipedia|nasa|usgs|noaa|pexels|pixabay|unsplash):.*\n',
    re.MULTILINE,
)


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: rimuovi-marker-foto.py <path-articolo.md>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"[error] lettura fallita: {e}", file=sys.stderr)
        return 2
    new_text = PATTERN.sub("", text)
    if new_text == text:
        return 1  # nessun marker da rimuovere
    try:
        path.write_text(new_text, encoding="utf-8")
    except OSError as e:
        print(f"[error] scrittura fallita: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
