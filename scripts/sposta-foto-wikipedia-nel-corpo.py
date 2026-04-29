#!/usr/bin/env python3
"""
Fix retroattivo: gli articoli con image_credit valorizzato hanno usato
erroneamente la foto Wikipedia come cover dell'articolo (immagine nelle
card di anteprima). Questo script:

1. Rinomina static/images/<slug>.webp -> static/images/<slug>-fonte-wikipedia.webp
   (la foto Wikipedia con fascia blu, da usare nel corpo)
2. Genera la cover tipografica (gradiente blu + titolo + fascia) chiamando
   genera-cover.py -> sovrascrive static/images/<slug>.webp
3. Inserisce shortcode {{< foto src="/images/<slug>-fonte-wikipedia.webp"
   alt="..." caption="Foto: <credit>. Fonte originale." >}} subito dopo
   il primo paragrafo del corpo articolo
4. image_credit + image_source_url RESTANO nel frontmatter (mostrati come
   didascalia copertina, ora vuota perché la cover è tipografica) e nel
   caption della foto nel corpo

Uso:
  python3 scripts/sposta-foto-wikipedia-nel-corpo.py            # tutti
  python3 scripts/sposta-foto-wikipedia-nel-corpo.py --dry-run  # vedi cosa farebbe
  python3 scripts/sposta-foto-wikipedia-nel-corpo.py <file.md>  # solo uno
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "comunicazioni"
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


def has_foto_shortcode_already(body: str, foto_filename: str) -> bool:
    """Evita doppia inserzione se script eseguito due volte."""
    return foto_filename in body


def insert_foto_after_first_paragraph(body: str, foto_url: str, alt: str, caption: str) -> str:
    """Inserisce shortcode foto dopo il primo paragrafo (prima newline doppia)."""
    shortcode = (
        f'\n\n{{{{< foto src="{foto_url}"\n'
        f'         alt="{alt}"\n'
        f'         caption="{caption}" >}}}}\n'
    )
    # Trova prima riga vuota dopo testo (= fine primo paragrafo)
    m = re.search(r'(.+?\n)(\n)', body, flags=re.DOTALL)
    if m:
        return body[:m.end(1)] + shortcode + body[m.end(2):]
    # Fallback: aggiungi in cima
    return shortcode.lstrip() + body


def process_article(md_path: Path, dry_run: bool = False) -> bool:
    text = md_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(text)
    if not fm:
        print(f"[skip] {md_path.name}: frontmatter non trovato")
        return False

    credit = get_field(fm, "image_credit")
    source_url = get_field(fm, "image_source_url")
    if not credit:
        print(f"[skip] {md_path.name}: nessun image_credit (non è un articolo affetto)")
        return False

    slug = md_path.stem
    cover_old = IMAGES / f"{slug}.webp"
    foto_new = IMAGES / f"{slug}-fonte-wikipedia.webp"
    foto_url = f"/images/{slug}-fonte-wikipedia.webp"

    if not cover_old.exists():
        print(f"[skip] {md_path.name}: file {cover_old.name} non esiste")
        return False

    title = get_field(fm, "title")
    alt = f"Foto storica: {title}"
    caption_parts = [f"Foto: {credit}"]
    if source_url:
        caption_parts.append(f"[Fonte originale]({source_url})")
    caption = ". ".join(caption_parts) + "."

    if has_foto_shortcode_already(body, f"{slug}-fonte-wikipedia.webp"):
        print(f"[skip] {md_path.name}: shortcode foto già presente")
        return False

    if dry_run:
        print(f"[dry] {md_path.name}:")
        print(f"  - rename {cover_old.name} -> {foto_new.name}")
        print(f"  - genera-cover.py -> nuova {cover_old.name} (cover tipografica)")
        print(f"  - inserisce shortcode foto dopo primo paragrafo, caption: '{caption}'")
        return True

    # 1. Rinomina foto Wikipedia
    shutil.move(str(cover_old), str(foto_new))

    # 2. Genera cover tipografica (sovrascrive cover_old)
    try:
        result = subprocess.run(
            ["python3", str(GENERA_COVER), str(md_path)],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        # Rollback rename
        shutil.move(str(foto_new), str(cover_old))
        print(f"[error] {md_path.name}: genera-cover.py fallito: {e.stderr}", file=sys.stderr)
        return False

    if not cover_old.exists():
        # genera-cover.py non ha creato il file, rollback
        shutil.move(str(foto_new), str(cover_old))
        print(f"[error] {md_path.name}: genera-cover.py non ha creato cover", file=sys.stderr)
        return False

    # 3. Inserisce shortcode nel corpo
    new_body = insert_foto_after_first_paragraph(body, foto_url, alt, caption)
    new_text = f"---\n{fm}---\n{new_body}"
    md_path.write_text(new_text, encoding="utf-8")

    print(f"[ok] {md_path.name}: cover->{slug}.webp (tipografica), foto->{foto_new.name}, shortcode inserito")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file", nargs="?", help="processa solo questo file .md (opzionale)")
    ap.add_argument("--dry-run", action="store_true", help="non modifica nulla, mostra cosa farebbe")
    args = ap.parse_args()

    if args.file:
        targets = [Path(args.file)]
    else:
        # Articolo affetto = ha image: che punta a /images/<slug>.webp E
        # il file webp esiste E NON è una cover tipografica (1200x630).
        # Una cover tipografica generata da genera-cover.py è sempre
        # 1200x630; tutto ciò che ha aspect ratio diverso è una foto
        # (Wikipedia/utente) usata erroneamente come cover.
        try:
            from PIL import Image
        except ImportError:
            print("[warn] Pillow non disponibile, fallback solo image_credit", file=sys.stderr)
            targets = sorted([
                md for md in CONTENT.glob("*.md")
                if "image_credit:" in md.read_text(encoding="utf-8")
            ])
        else:
            targets = []
            for md in sorted(CONTENT.glob("*.md")):
                slug = md.stem
                cover_path = ROOT / "static" / "images" / f"{slug}.webp"
                if not cover_path.is_file():
                    continue
                try:
                    with Image.open(cover_path) as img:
                        w, h = img.size
                except Exception:
                    continue
                # Cover tipografica = 1200x630 (rapporto 1.905). Tolleranza ±2px.
                is_typographic = (1198 <= w <= 1202) and (628 <= h <= 632)
                if is_typographic:
                    continue
                # Sospetto: foto in cover. Verifica anche che il file
                # -fonte-wikipedia non esista già (= articolo già fixato)
                foto_path = ROOT / "static" / "images" / f"{slug}-fonte-wikipedia.webp"
                if foto_path.is_file():
                    continue
                targets.append(md)

    print(f"[info] {len(targets)} articoli candidati")
    ok = 0
    for md in targets:
        if process_article(md, dry_run=args.dry_run):
            ok += 1
    print(f"\n[done] {ok}/{len(targets)} processati")
    return 0


if __name__ == "__main__":
    sys.exit(main())
