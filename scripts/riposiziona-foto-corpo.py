#!/usr/bin/env python3
"""
Riposiziona lo shortcode {{< foto >}} all'interno degli articoli che hanno
foto Wikipedia nel corpo: invece di "subito dopo il primo paragrafo intro"
(posizione attuale automatica e generica), sposta a "dentro la prima
sezione H2, dopo il primo paragrafo di contenuto" — collocazione piu'
sensata tematicamente perche' la foto si lega al primo blocco di
contenuto dell'articolo, non alla pura introduzione.

Logica:
1. Trova il blocco shortcode foto (tre righe: src, alt, caption + chiusura)
2. Lo rimuove dalla posizione attuale
3. Lo reinserisce dopo:
   - la prima riga "## ..." (prima H2)
   - + il primo paragrafo non vuoto della sezione

Idempotente: se la foto e' gia' dopo una H2, non sposta.

Uso:
  python3 scripts/riposiziona-foto-corpo.py            # tutti
  python3 scripts/riposiziona-foto-corpo.py <file.md>  # solo uno
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "comunicazioni"


def parse_frontmatter(text: str):
    m = re.match(r"^---\n(.*?\n)---\n(.*)$", text, flags=re.DOTALL)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def find_foto_shortcode(body: str):
    """Trova il blocco {{< foto src=...>}} (multi-line). Ritorna (start, end) char index del blocco completo + newlines circostanti."""
    # Match: {{< foto ... >}} che puo' essere multi-line
    pattern = re.compile(r'\{\{<\s*foto\s+[^>]+?>\}\}', re.DOTALL)
    m = pattern.search(body)
    if not m:
        return None, None, None
    start = m.start()
    end = m.end()
    block = body[start:end]
    # Estendi per inglobare newlines circostanti (per pulizia)
    while start > 0 and body[start - 1] == '\n':
        start -= 1
    while end < len(body) and body[end] == '\n':
        end += 1
    return start, end, block


def is_under_h2(body: str, foto_start: int) -> bool:
    """Verifica se la foto e' gia' sotto una H2 (cerca prima H2 prima della foto)."""
    # Trova ultima riga "## ..." prima di foto_start
    pre = body[:foto_start]
    h2_matches = list(re.finditer(r'^## [^#].*$', pre, flags=re.MULTILINE))
    return len(h2_matches) > 0


def find_first_h2_then_paragraph_end(body: str):
    """Trova la posizione 'dopo prima H2 + primo paragrafo' dove inserire la foto."""
    # Trova prima H2
    h2 = re.search(r'^## [^#].*$', body, flags=re.MULTILINE)
    if not h2:
        return None
    # Dopo H2, salta riga vuota, trova primo paragrafo, poi salta a fine paragrafo (riga vuota successiva)
    after_h2 = h2.end()
    # Trova prima riga non vuota dopo H2
    rest = body[after_h2:]
    # Pattern: \n\n (vuota) + paragrafo + \n\n (vuota)
    para_match = re.search(r'\n\n([^\n].*?)(\n\n|\Z)', rest, flags=re.DOTALL)
    if para_match:
        return after_h2 + para_match.end(1)
    return after_h2


def process(md_path: Path) -> bool:
    text = md_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    if not fm:
        return False

    start, end, block = find_foto_shortcode(body)
    if start is None:
        # Nessuno shortcode foto da spostare
        return False

    if is_under_h2(body, start):
        print(f"[skip] {md_path.name}: foto gia' sotto una H2")
        return False

    # Rimuovi blocco originale
    body_no_foto = body[:start] + body[end:]

    # Trova posizione target (dopo prima H2 + primo paragrafo)
    insert_pos = find_first_h2_then_paragraph_end(body_no_foto)
    if insert_pos is None:
        print(f"[skip] {md_path.name}: nessuna H2 trovata, lascio dov'era")
        return False

    # Inserisci con due newline prima e dopo
    new_body = body_no_foto[:insert_pos] + "\n\n" + block + "\n" + body_no_foto[insert_pos:]
    new_text = f"---\n{fm}---\n{new_body}"

    if new_text == text:
        return False

    md_path.write_text(new_text, encoding="utf-8")
    print(f"[ok] {md_path.name}: foto spostata dopo prima H2 + primo paragrafo")
    return True


def main():
    if len(sys.argv) > 1:
        targets = [Path(sys.argv[1])]
    else:
        targets = sorted([
            md for md in CONTENT.glob("*.md")
            if "fonte-wikipedia.webp" in md.read_text(encoding="utf-8")
        ])

    print(f"[info] {len(targets)} articoli candidati")
    moved = 0
    for md in targets:
        if process(md):
            moved += 1
    print(f"\n[done] {moved}/{len(targets)} foto spostate")
    return 0


if __name__ == "__main__":
    sys.exit(main())
