#!/usr/bin/env python3
"""Controlla che la data con l'orario degli articoli usi lo scarto dell'ora italiana di quel giorno.

Un articolo con `date: AAAA-MM-GGTHH:MM:SS+HH:MM` deve avere `+02:00` con l'ora legale
e `+01:00` con l'ora solare (da fine ottobre a fine marzo). Con `+02:00` d'inverno
`T00:02:00` cade alle 23:02 del giorno prima e l'articolo finisce sotto quelli a data
semplice della stessa giornata (12/11/2026, rule 02 § «Regola critica formato data»).

Uso:  python3 scripts/check-scarto-orario.py [FILE ...]   (senza file: tutti gli articoli)
      python3 scripts/check-scarto-orario.py --correggi [FILE ...]
Esce con 1 se trova scarti sbagliati (con --correggi li corregge ed esce con 0).
"""
import datetime
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

RADICE = Path(__file__).resolve().parent.parent
ROMA = ZoneInfo("Europe/Rome")
RIGA = re.compile(
    r'^(date:\s*["\']?)(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2})([+-]\d{2}:\d{2})(["\']?\s*)$',
    re.MULTILINE,
)


def scarto_atteso(giorno: str, ora: str) -> str:
    """Scarto di Europe/Rome per quell'istante locale, nella forma +HH:MM."""
    istante = datetime.datetime.fromisoformat(f"{giorno}T{ora}").replace(tzinfo=ROMA)
    s = istante.strftime("%z")
    return f"{s[:3]}:{s[3:]}"


def frontmatter(testo: str) -> tuple[int, int] | None:
    """Posizione del frontmatter YAML (fra i due `---`), o None."""
    if not testo.startswith("---"):
        return None
    fine = testo.find("\n---", 3)
    return (0, fine) if fine != -1 else None


def main() -> int:
    argomenti = sys.argv[1:]
    correggi = "--correggi" in argomenti
    file = [Path(a) for a in argomenti if a != "--correggi"]
    if not file:
        file = sorted((RADICE / "content" / "comunicazioni").glob("*.md"))
    errori = 0
    for f in file:
        if f.suffix != ".md" or not f.exists():
            continue
        testo = f.read_text(encoding="utf-8")
        zona = frontmatter(testo)
        if not zona:
            continue
        intestazione = testo[: zona[1]]
        m = RIGA.search(intestazione)
        if not m:
            continue
        atteso = scarto_atteso(m.group(2), m.group(3))
        if m.group(4) == atteso:
            continue
        if correggi:
            nuova = f"{m.group(1)}{m.group(2)}T{m.group(3)}{atteso}{m.group(5)}"
            f.write_text(testo[: m.start()] + nuova + testo[m.end():], encoding="utf-8")
            print(f"corretto {f}: {m.group(4)} -> {atteso}")
        else:
            errori += 1
            print(f"::error file={f}::date {m.group(2)}T{m.group(3)}{m.group(4)}: "
                  f"lo scarto dell'ora italiana di quel giorno è {atteso}")
    if errori:
        print(f"{errori} articoli con lo scarto orario sbagliato "
              "(correzione: python3 scripts/check-scarto-orario.py --correggi FILE).")
        return 1
    if not correggi:
        print("OK: scarto orario coerente con l'ora italiana del giorno.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
