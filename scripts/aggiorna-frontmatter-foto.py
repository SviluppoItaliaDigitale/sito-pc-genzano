#!/usr/bin/env python3
"""
Aggiorna il frontmatter di un articolo dopo il download foto Wikipedia:
  - popola `image: "/images/<nome>.webp"` se vuoto
  - popola `image_credit: "..."` (autore + licenza + fonte)
  - rimuove la riga `# TODO-foto-wikipedia: ...` dal frontmatter

Idempotente: se eseguito due volte senza marker, non modifica nulla.

Uso:
  python3 scripts/aggiorna-frontmatter-foto.py \\
    <path-articolo.md> <nome-immagine-senza-ext> \\
    "<autore>" "<licenza>" "<url-origine>"

Esempio:
  python3 scripts/aggiorna-frontmatter-foto.py \\
    content/comunicazioni/2026-05-06-friuli-1976.md \\
    2026-05-06-friuli-1976 \\
    "USGS" "Public domain" \\
    "https://commons.wikimedia.org/wiki/File:USGS_Shakemap.jpg"
"""
import sys
import re
from pathlib import Path


def update_article(article_path: Path, img_name: str, author: str, license_: str, source_url: str) -> bool:
    """Ritorna True se ha modificato il file."""
    if not article_path.is_file():
        print(f"[error] articolo non trovato: {article_path}", file=sys.stderr)
        return False

    text = article_path.read_text(encoding="utf-8")

    # Separa frontmatter e corpo
    m = re.match(r"^---\n(.*?\n)---\n(.*)$", text, flags=re.DOTALL)
    if not m:
        print(f"[error] frontmatter YAML non trovato in {article_path}", file=sys.stderr)
        return False

    fm, body = m.group(1), m.group(2)
    new_fm = fm

    # 1) Rimuove la riga del marker TODO-foto-wikipedia
    new_fm, n_todo = re.subn(
        r"^# *TODO-foto-wikipedia:.*\n",
        "",
        new_fm,
        flags=re.MULTILINE,
    )

    # 2) Popola image se vuoto (image: "" oppure image: '')
    img_path = f'/images/{img_name}.webp'
    if re.search(r'^image:\s*["\']{2}\s*$', new_fm, flags=re.MULTILINE):
        new_fm = re.sub(
            r'^image:\s*["\']{2}\s*$',
            f'image: "{img_path}"',
            new_fm,
            count=1,
            flags=re.MULTILINE,
        )
    elif not re.search(r'^image:', new_fm, flags=re.MULTILINE):
        new_fm = new_fm.rstrip("\n") + f'\nimage: "{img_path}"\n'

    # 3) Popola image_credit se non c'è (Hugo lo gestira' come campo libero,
    #    il template lo puo' mostrare in didascalia copertina).
    credit = f'{author} — {license_} — via Wikimedia Commons'
    credit_escaped = credit.replace('"', '\\"')
    if not re.search(r'^image_credit:', new_fm, flags=re.MULTILINE):
        new_fm = new_fm.rstrip("\n") + f'\nimage_credit: "{credit_escaped}"\nimage_source_url: "{source_url}"\n'

    new_text = f"---\n{new_fm}---\n{body}"

    if new_text == text:
        print(f"[skip] nessuna modifica per {article_path.name}")
        return False

    article_path.write_text(new_text, encoding="utf-8")
    actions = []
    if n_todo:
        actions.append("rimosso TODO")
    actions.append(f"image={img_path}")
    actions.append("image_credit aggiunto")
    print(f"[ok] {article_path.name}: {', '.join(actions)}")
    return True


def main():
    if len(sys.argv) != 6:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    article = Path(sys.argv[1])
    img_name = sys.argv[2]
    author = sys.argv[3] or "Sconosciuto"
    license_ = sys.argv[4] or "Sconosciuta"
    source_url = sys.argv[5] or ""
    changed = update_article(article, img_name, author, license_, source_url)
    sys.exit(0 if changed else 0)


if __name__ == "__main__":
    main()
