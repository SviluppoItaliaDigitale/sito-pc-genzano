#!/usr/bin/env python3
"""
Aggiorna l'articolo dopo il download di una foto da Wikipedia/NASA/USGS/NOAA.

Convenzione di posizionamento foto (MANUALE-SITO.md Parte 14.9):
  - Cover articolo = sempre tipografica (gradiente blu + titolo + fascia)
  - 1ª foto reale = nel corpo, dopo il 1° H2 + primo paragrafo
  - 2ª, 3ª foto (per arricchimenti successivi manuali) = dopo H2 successivi,
    una per ogni evento storico citato (mai foto a casaccio)

Flusso (eseguito qui per la 1ª foto soltanto):
  1. Rinomina static/images/<slug>.webp -> static/images/<slug>-fonte-wikipedia.webp
     (la foto scaricata diventa "foto del corpo")
  2. Lancia genera-cover.py per produrre una cover tipografica istituzionale
     (gradiente blu + titolo articolo + fascia con logo) come <slug>.webp
  3. Aggiorna frontmatter:
     - image: "/images/<slug>.webp" (cover tipografica)
     - image_alt popolato con titolo se vuoto
     - rimuove la riga marker TODO-foto-*
  4. Inserisce nel corpo articolo lo shortcode {{< foto >}} con foto Wikipedia
     dopo la 1ª H2 + primo paragrafo.
     Caption: "Foto: <autore> — <licenza> — via Wikimedia Commons.
     [Fonte originale](<url>)."

Idempotente: se eseguito su articolo gia' processato (slug-fonte-wikipedia.webp
gia' presente), non duplica.

Uso:
  python3 scripts/aggiorna-frontmatter-foto.py \\
    <path-articolo.md> <slug> "<autore>" "<licenza>" "<url-origine>"
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "static" / "images"
GENERA_COVER = ROOT / "scripts" / "genera-cover.py"


def parse_frontmatter(text: str):
    m = re.match(r"^---\n(.*?\n)---\n(.*)$", text, flags=re.DOTALL)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def get_field(fm: str, name: str) -> str:
    m = re.search(rf'^{name}:\s*"?(.*?)"?\s*$', fm, flags=re.MULTILINE)
    return m.group(1).strip() if m else ""


def insert_foto_in_body(body: str, foto_url: str, alt: str, caption: str) -> str:
    """Inserisce {{< foto >}} dopo la prima H2 + primo paragrafo di contenuto."""
    if foto_url in body:
        return body  # gia' presente
    shortcode = (
        f'\n\n{{{{< foto src="{foto_url}"\n'
        f'         alt="{alt}"\n'
        f'         caption="{caption}" >}}}}\n'
    )
    h2 = re.search(r'^## [^#].*$', body, flags=re.MULTILINE)
    if h2:
        rest = body[h2.end():]
        para = re.search(r'\n\n([^\n].*?)(\n\n|\Z)', rest, flags=re.DOTALL)
        if para:
            ins = h2.end() + para.end(1)
            return body[:ins] + shortcode + body[ins:]
    # Fallback: dopo primo paragrafo
    m = re.search(r'(.+?\n)(\n)', body, flags=re.DOTALL)
    if m:
        return body[:m.end(1)] + shortcode + body[m.end(2):]
    return shortcode.lstrip() + body


def update_article(article: Path, slug: str, author: str, license_: str, source_url: str) -> bool:
    if not article.is_file():
        print(f"[error] articolo non trovato: {article}", file=sys.stderr)
        return False

    text = article.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    if fm is None:
        print(f"[error] frontmatter YAML non trovato in {article}", file=sys.stderr)
        return False

    cover_path = IMAGES / f"{slug}.webp"
    foto_path = IMAGES / f"{slug}-fonte-wikipedia.webp"
    cover_url = f"/images/{slug}.webp"
    foto_url = f"/images/{slug}-fonte-wikipedia.webp"

    # 1. Rinomina foto Wikipedia -> -fonte-wikipedia (se non gia' fatto)
    if cover_path.is_file() and not foto_path.is_file():
        shutil.move(str(cover_path), str(foto_path))
        print(f"[ok] foto rinominata: {cover_path.name} -> {foto_path.name}")
    elif foto_path.is_file():
        print(f"[info] foto Wikipedia gia' rinominata: {foto_path.name}")
    else:
        print(f"[error] nessun file foto trovato per slug {slug}", file=sys.stderr)
        return False

    # 2. Genera cover tipografica come <slug>.webp
    if not cover_path.is_file():
        try:
            subprocess.run(
                ["python3", str(GENERA_COVER), str(article)],
                check=True, capture_output=True, text=True,
            )
            print(f"[ok] cover tipografica generata: {cover_path.name}")
        except subprocess.CalledProcessError as e:
            print(f"[error] genera-cover.py fallito: {e.stderr}", file=sys.stderr)
            # Rollback rename foto
            shutil.move(str(foto_path), str(cover_path))
            return False

    # 3. Aggiorna frontmatter
    new_fm = fm
    # Rimuove marker TODO-foto-*
    new_fm, _ = re.subn(
        r"^# *TODO-foto-(?:wikipedia|nasa|usgs|noaa):.*\n",
        "",
        new_fm,
        flags=re.MULTILINE,
    )
    # image: -> cover tipografica (sovrascrivi sempre, anche se vuoto o foto)
    if re.search(r'^image:\s*.*$', new_fm, flags=re.MULTILINE):
        new_fm = re.sub(
            r'^image:\s*.*$',
            f'image: "{cover_url}"',
            new_fm,
            count=1,
            flags=re.MULTILINE,
        )
    else:
        new_fm = new_fm.rstrip("\n") + f'\nimage: "{cover_url}"\n'
    # image_alt: popola se vuoto
    title = get_field(fm, "title")
    alt_cover = f"Cover dell'articolo: {title}" if title else "Cover articolo"
    new_fm = re.sub(
        r'^image_alt:\s*["\']{2}\s*$',
        f'image_alt: "{alt_cover}"',
        new_fm,
        count=1,
        flags=re.MULTILINE,
    )
    # Rimuovi image_credit / image_source_url se presenti (ora sono nel caption)
    new_fm = re.sub(r'^image_credit:.*\n', '', new_fm, flags=re.MULTILINE)
    new_fm = re.sub(r'^image_source_url:.*\n', '', new_fm, flags=re.MULTILINE)

    # 4. Inserisci shortcode foto nel corpo (idempotente)
    foto_alt = f"Foto storica: {title}" if title else "Foto"
    cred = author or "Sconosciuto"
    lic = license_ or "Sconosciuta"
    via = "via Wikimedia Commons" if "wikimedia" in (source_url or "").lower() else "via fonte libera"
    caption_parts = [f"Foto: {cred} — {lic} — {via}"]
    if source_url:
        caption_parts.append(f"[Fonte originale]({source_url})")
    caption = ". ".join(caption_parts) + "."
    # Escape virgolette nel caption
    caption_safe = caption.replace('"', "'")

    new_body = insert_foto_in_body(body, foto_url, foto_alt, caption_safe)

    new_text = f"---\n{new_fm}---\n{new_body}"
    if new_text == text:
        print(f"[skip] {article.name}: nessuna modifica")
        return False

    article.write_text(new_text, encoding="utf-8")
    print(f"[ok] {article.name}: cover tipografica + foto {foto_path.name} + shortcode nel corpo")
    return True


def main():
    if len(sys.argv) != 6:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    article = Path(sys.argv[1])
    slug = sys.argv[2]
    author = sys.argv[3] or "Sconosciuto"
    license_ = sys.argv[4] or "Sconosciuta"
    source_url = sys.argv[5] or ""
    update_article(article, slug, author, license_, source_url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
