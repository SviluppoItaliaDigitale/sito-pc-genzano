#!/usr/bin/env python3
"""
Aggiorna il campo `image:` del frontmatter di ogni articolo
in modo che punti alla cover .webp corrispondente, se esiste.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "comunicazioni"
IMAGES = ROOT / "static" / "images"

def update(md: Path) -> bool:
    cover = IMAGES / f"{md.stem}.webp"
    if not cover.exists():
        return False
    image_url = f"/images/{cover.name}"
    text = md.read_text(encoding="utf-8")
    # Replace line starting with `image:` inside frontmatter
    new_text, n = re.subn(
        r'^image:\s*.*$',
        f'image: "{image_url}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    # Set alt if empty
    title_match = re.search(r'^title:\s*"?(.+?)"?\s*$', text, re.MULTILINE)
    title = title_match.group(1).strip('"').strip("'") if title_match else md.stem
    alt_text = f"Cover dell'articolo: {title}"
    new_text, _ = re.subn(
        r'^image_alt:\s*"".*$',
        f'image_alt: "{alt_text}"',
        new_text,
        count=1,
        flags=re.MULTILINE,
    )
    if new_text != text:
        md.write_text(new_text, encoding="utf-8")
        return True
    return False

changed = 0
for md in sorted(CONTENT.glob("*.md")):
    if update(md):
        print(f"[upd] {md.name}")
        changed += 1
print(f"\nAggiornati {changed} articoli")
