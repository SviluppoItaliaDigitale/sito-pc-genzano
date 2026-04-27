#!/usr/bin/env python3
"""
Genera cover tipografiche istituzionali per gli articoli che NON hanno foto:
  - articoli con `image: ""` (vuoto)
  - E senza marker `# TODO-foto-*` (in attesa di download da fonti esterne)
  - E senza file static/images/<slug>.webp gia' presente

Per ogni articolo selezionato:
  1. Lancia scripts/genera-cover.py <file.md>     (genera <slug>.webp)
  2. Aggiorna image: "" -> image: "/images/<slug>.webp"
  3. Aggiorna image_alt: "" -> image_alt: "Cover dell'articolo: <title>"

Sicurezza:
  - Non sovrascrive image: gia' valorizzato (es. foto utente in static/images/foto-evento.webp)
  - Non tocca articoli con marker TODO-foto-* (verranno gestiti dal download)
  - Non tocca image_alt gia' valorizzato

Uso:
  python3 scripts/auto-cover-mancanti.py        # processa tutti gli articoli candidati
  python3 scripts/auto-cover-mancanti.py --dry-run  # mostra cosa farebbe senza modificare nulla
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "comunicazioni"
IMAGES = ROOT / "static" / "images"
GENERA_COVER = ROOT / "scripts" / "genera-cover.py"


def has_empty_image(text: str) -> bool:
    """True se l'articolo ha image: "" (o image: '')."""
    return bool(re.search(r'^image:\s*["\']{2}\s*$', text, flags=re.MULTILINE))


def has_todo_marker(text: str) -> bool:
    """True se l'articolo ha un marker TODO-foto-* (verra' processato altrove)."""
    return bool(re.search(r'^# TODO-foto-(wikipedia|nasa|usgs):', text, flags=re.MULTILINE))


def update_frontmatter(md: Path, slug: str, title: str) -> bool:
    """Aggiorna image: e image_alt: SOLO se erano vuoti. Atomico."""
    text = md.read_text(encoding="utf-8")
    if not has_empty_image(text):
        return False

    image_url = f"/images/{slug}.webp"
    new_text, n_img = re.subn(
        r'^image:\s*["\']{2}\s*$',
        f'image: "{image_url}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )
    alt_text = f"Cover dell'articolo: {title}"
    new_text, n_alt = re.subn(
        r'^image_alt:\s*["\']{2}\s*$',
        f'image_alt: "{alt_text}"',
        new_text,
        count=1,
        flags=re.MULTILINE,
    )
    if new_text == text:
        return False
    md.write_text(new_text, encoding="utf-8")
    return True


def extract_title(text: str, fallback: str) -> str:
    m = re.search(r'^title:\s*"?(.+?)"?\s*$', text, flags=re.MULTILINE)
    return m.group(1).strip('"').strip("'") if m else fallback


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="mostra cosa farebbe senza modificare")
    args = ap.parse_args()

    candidates = []
    for md in sorted(CONTENT.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        if not has_empty_image(text):
            continue
        if has_todo_marker(text):
            continue
        slug = md.stem
        if (IMAGES / f"{slug}.webp").exists():
            # cover gia' presente, basta aggiornare il frontmatter
            candidates.append((md, slug, "frontmatter-only"))
        else:
            candidates.append((md, slug, "generate"))

    if not candidates:
        print("[info] Nessun articolo candidato per cover automatica.")
        return 0

    print(f"[info] Trovati {len(candidates)} articoli candidati.")

    if args.dry_run:
        for md, slug, kind in candidates:
            print(f"  [{kind}] {md.name}")
        return 0

    generated = 0
    updated = 0
    failed = 0
    for md, slug, kind in candidates:
        text = md.read_text(encoding="utf-8")
        title = extract_title(text, slug)

        if kind == "generate":
            print(f"[gen] {md.name} ...")
            try:
                subprocess.run(
                    ["python3", str(GENERA_COVER), str(md)],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                generated += 1
            except subprocess.CalledProcessError as e:
                print(f"  [error] genera-cover.py fallito: {e.stderr}", file=sys.stderr)
                failed += 1
                continue

        # Verifica che il file esista ora
        if not (IMAGES / f"{slug}.webp").exists():
            print(f"  [warn] cover non trovata dopo generazione: {slug}.webp")
            failed += 1
            continue

        if update_frontmatter(md, slug, title):
            updated += 1
            print(f"  [ok] frontmatter aggiornato: {md.name}")

    print(f"\n[summary] Cover generate: {generated}, frontmatter aggiornati: {updated}, falliti: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
