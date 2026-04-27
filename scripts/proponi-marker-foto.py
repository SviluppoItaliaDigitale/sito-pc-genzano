#!/usr/bin/env python3
"""
Backfill foto Wikipedia per articoli passati: scansiona content/comunicazioni/
e per ogni articolo con image: "" (vuoto) e SENZA marker TODO-foto-* propone
un marker `# TODO-foto-wikipedia` da inserire manualmente nel frontmatter.

Sicurezza editoriale: NON modifica nessun file. Stampa solo proposte. La scelta
finale di applicare il marker resta all'utente, che decide caso per caso se
l'articolo ha senso con una foto Wikipedia (eventi storici/temi enciclopedici)
o no (eventi locali, comunicazioni interne — meglio cover tipografica).

Logica di proposta del titolo Wikipedia:
1. Estrae il `title:` dal frontmatter
2. Pulisce parole comuni (anniversario, ricordo, anni dopo, ecc.)
3. Suggerisce il titolo come query Wikipedia
4. Per articoli con date storiche evidenti, suggerisce anche il pattern
   "Terremoto del [Luogo] del [Anno]"

Uso:
  python3 scripts/proponi-marker-foto.py             # tutti gli articoli candidati
  python3 scripts/proponi-marker-foto.py --solo 5    # solo i primi 5 candidati
  python3 scripts/proponi-marker-foto.py --csv       # output CSV (slug, title_proposto, marker)

Workflow consigliato:
  1. python3 scripts/proponi-marker-foto.py --csv > /tmp/proposte.csv
  2. Apri /tmp/proposte.csv in editor e segna "y" sulle righe da approvare
  3. Per ogni "y": copia il marker e incollalo nel frontmatter dell'articolo
  4. git commit + push -> il workflow scarica-foto-automatica.yml fa il resto
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "comunicazioni"

# Parole da rimuovere dal title per ottenere la query Wikipedia
NOISE_WORDS = {
    "anniversario", "anni", "dopo", "ricordo", "memoria",
    "celebrazione", "giornata", "il", "lo", "la", "i", "gli", "le",
    "un", "una", "uno", "del", "dello", "della", "dei", "degli", "delle",
    "di", "da", "in", "con", "per", "su", "tra", "fra",
    "che", "ha", "che", "e", "ed", "o", "od", "ma",
    "nostro", "nostra", "nostri", "nostre",
    "nuovo", "nuova", "nuovi", "nuove",
    "rivisto", "ridotto", "completo", "completa",
}


def has_empty_image(text: str) -> bool:
    return bool(re.search(r'^image:\s*["\']{2}\s*$', text, flags=re.MULTILINE))


def has_todo_marker(text: str) -> bool:
    return bool(re.search(r'^# TODO-foto-(wikipedia|nasa|usgs|noaa):', text, flags=re.MULTILINE))


def extract_title(text: str) -> str:
    m = re.search(r'^title:\s*"?(.+?)"?\s*$', text, flags=re.MULTILINE)
    return m.group(1).strip().strip('"').strip("'") if m else ""


def propose_query(title: str) -> str:
    """Ritorna una query Wikipedia probabile dal titolo articolo."""
    # Rimuovi colon e quanto segue (spesso il colon separa il "claim" dal contesto)
    if ":" in title:
        title = title.split(":", 1)[0].strip()
    # Rimuovi parentesi e contenuto
    title = re.sub(r'\([^)]*\)', '', title).strip()
    # Tokenize, rimuovi noise, ricomponi
    words = re.split(r'\s+', title)
    cleaned = [w for w in words if w.lower().strip(",.;:") not in NOISE_WORDS and len(w) > 1]
    return " ".join(cleaned).strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--solo", type=int, default=0, help="processa solo i primi N candidati")
    ap.add_argument("--csv", action="store_true", help="output formato CSV")
    args = ap.parse_args()

    candidates = []
    for md in sorted(CONTENT.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        if not has_empty_image(text):
            continue
        if has_todo_marker(text):
            continue
        title = extract_title(text)
        if not title:
            continue
        slug = md.stem
        query = propose_query(title)
        marker = f'# TODO-foto-wikipedia: bash scripts/foto-da-wikipedia.sh "{query}" {slug}'
        candidates.append((slug, title, query, marker, md))

    if args.solo > 0:
        candidates = candidates[:args.solo]

    if not candidates:
        print("[info] Nessun articolo candidato per il backfill.", file=sys.stderr)
        return 0

    if args.csv:
        # CSV con quoting standard
        import csv
        w = csv.writer(sys.stdout)
        w.writerow(["slug", "titolo_articolo", "query_wikipedia", "approvato_y_n", "marker_da_incollare"])
        for slug, title, query, marker, _ in candidates:
            w.writerow([slug, title, query, "", marker])
        return 0

    # Output umano leggibile
    print(f"# Candidati per backfill foto Wikipedia ({len(candidates)} articoli)")
    print(f"# (articoli con image:'' e senza marker TODO-foto-*)")
    print()
    for slug, title, query, marker, md in candidates:
        print(f"## {slug}")
        print(f"  Titolo:  {title}")
        print(f"  Query:   {query}")
        print(f"  Marker:  {marker}")
        print(f"  File:    {md.relative_to(ROOT)}")
        print()
    print(f"# Per applicare: copia il marker desiderato sotto la riga 'image: \"\"'")
    print(f"# di ogni articolo che vuoi processare. Poi git commit + push.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
