#!/usr/bin/env python3
"""
Genera cover grafiche istituzionali per gli articoli del sito.
- Sfondo: gradiente blu istituzionale + accent color per badge
- Titolo dell'articolo centrato (safe-zone composer Facebook mobile)
- Fascia blu istituzionale inferiore con logo + dicitura

Composizione in Python+Pillow (non ImageMagick) per essere cross-platform e
indipendente dalla fragilità ImageMagick v6/v7 (delegate WebP, font discovery,
sintassi diversa). Stessa scelta gia' adottata per applica-fascia-foto.py.
Dipendenze: python3-pil (Pillow) + font Liberation Sans (fonts-liberation).

Uso:
    python3 scripts/genera-cover.py content/comunicazioni/2026-04-21-kit-emergenza-domestico-guida-pratica.md
    python3 scripts/genera-cover.py --all
    python3 scripts/genera-cover.py --all --force
"""

import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content" / "comunicazioni"
IMAGES_DIR = ROOT / "static" / "images"
LOGO = IMAGES_DIR / "logo-pc-genzano.png"

PRIMARY = "#003366"
PRIMARY_DARK = "#001a33"
WHITE = "#ffffff"

BADGE_COLORS = {
    "Allerta": "#d32f2f",
    "Emergenza": "#b71c1c",
    "Avviso": "#f57c00",
    "Prevenzione": "#1565c0",
    "Informazione": "#0277bd",
    "Formazione": "#6a1b9a",
    "Evento": "#2e7d32",
    "Volontariato": "#00695c",
    "Attività": "#455a64",
    "Radiocomunicazioni": "#37474f",
    "Esercitazione": "#4527a0",
    "Aggiornamento": "#546e7a",
    "Comunicazione": "#263238",
}

W, H = 1200, 630
BAND_H = 100

# Liberation Sans: ricerca robusta del file TTF su Linux/CI/macOS/Windows.
_FONT_DIRS = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/liberation2",
    "/usr/share/fonts/liberation",
    "/usr/share/fonts/TTF",
    "/usr/share/fonts/truetype/dejavu",
    "/Library/Fonts",
    "/System/Library/Fonts/Supplemental",
    "C:/Windows/Fonts",
]
_FONT_FILES = {
    True: ["LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf", "Arial Bold.ttf", "arialbd.ttf"],
    False: ["LiberationSans-Regular.ttf", "DejaVuSans.ttf", "Arial.ttf", "arial.ttf"],
}
_font_cache: dict = {}


def _font_path(bold: bool) -> str | None:
    for d in _FONT_DIRS:
        for name in _FONT_FILES[bold]:
            p = Path(d) / name
            if p.exists():
                return str(p)
    for name in _FONT_FILES[bold]:  # fallback: lascia risolvere a fontconfig
        try:
            ImageFont.truetype(name, 10)
            return name
        except Exception:
            continue
    return None


def font(bold: bool, size: int) -> ImageFont.FreeTypeFont:
    key = (bold, size)
    if key not in _font_cache:
        path = _font_path(bold)
        if path is None:
            print("[warn] font Liberation Sans non trovato, uso il font di default Pillow",
                  file=sys.stderr)
            _font_cache[key] = ImageFont.load_default()
        else:
            _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]


def _rgb(value: str) -> tuple:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def parse_frontmatter(md_path: Path) -> dict:
    text = md_path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def wrap_title(title: str, max_chars: int = 28) -> list:
    words = title.split()
    lines = []
    cur = ""
    for w in words:
        if len(cur) + len(w) + 1 <= max_chars:
            cur = (cur + " " + w).strip()
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:4]


def slug_from_filename(path: Path) -> str:
    return path.stem


def output_path(md_path: Path) -> Path:
    return IMAGES_DIR / f"{md_path.stem}.webp"


def generate_cover(md_path: Path, force: bool = False) -> Path | None:
    fm = parse_frontmatter(md_path)
    if not fm:
        print(f"[skip] {md_path.name}: no frontmatter")
        return None

    title = fm.get("title", md_path.stem)
    badge = fm.get("badge", "Informazione")
    out = output_path(md_path)

    if out.exists() and not force:
        print(f"[exists] {out.name}")
        return out

    accent = _rgb(BADGE_COLORS.get(badge, PRIMARY))
    primary = _rgb(PRIMARY)
    primary_dark = _rgb(PRIMARY_DARK)
    white = _rgb(WHITE)

    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img, "RGBA")

    # Gradiente verticale PRIMARY -> PRIMARY_DARK (una linea per riga)
    for y in range(H):
        t = y / (H - 1)
        d.line([(0, y), (W, y)], fill=(
            round(primary[0] + (primary_dark[0] - primary[0]) * t),
            round(primary[1] + (primary_dark[1] - primary[1]) * t),
            round(primary[2] + (primary_dark[2] - primary[2]) * t),
        ))

    # Accent line in alto + decorazione diagonale in alto a destra
    d.rectangle([0, 0, W, 8], fill=accent)
    d.polygon([(W - 180, 0), (W, 0), (W, 220), (W - 20, 220)], fill=accent)

    # Badge pill
    badge_w = 40 + 12 * len(badge)
    d.rounded_rectangle([80, 70, 80 + badge_w, 120], radius=10, fill=accent)
    d.text((80 + badge_w / 2, 95), badge.upper(), font=font(True, 22),
           fill=white, anchor="mm")

    # Linea separatrice sopra la banda
    d.rectangle([80, H - BAND_H - 30, 1120, H - BAND_H - 29], fill=(255, 255, 255, 38))

    # Titolo centrato (safe-zone composer Facebook mobile: incident 16/05/2026
    # "preview Giro d'Italia tagliata ai lati" quando il titolo era a sinistra).
    # Wrap a 24 caratteri per stare nella safe zone centrale del 75%.
    lines = wrap_title(title, 24)
    line_h = 50 + 16
    cy = (H // 2) - 30 - (line_h * len(lines)) // 2 + line_h // 2
    for i, ln in enumerate(lines):
        d.text((W / 2, cy + i * line_h), ln, font=font(True, 50),
               fill=white, anchor="mm")

    # Banda blu inferiore + linea chiara di stacco
    d.rectangle([0, H - BAND_H, W, H], fill=primary)
    d.rectangle([0, H - BAND_H, W, H - BAND_H + 2], fill=(255, 255, 255, 64))

    # Testo nella banda
    d.text((180, H - BAND_H + 22), "PROTEZIONE CIVILE", font=font(True, 26),
           fill=white, anchor="la")
    d.text((180, H - BAND_H + 60), "Gruppo Comunale Volontari — Genzano di Roma",
           font=font(False, 16), fill=(255, 255, 255, 217), anchor="la")

    # Logo nella banda
    if LOGO.exists():
        logo = Image.open(LOGO).convert("RGBA").resize((72, 72))
        img.paste(logo, (90, H - BAND_H + 15), logo)

    # Export WebP, ricomprimi progressivamente se supera 200 KB
    quality = 85
    img.save(out, "WEBP", quality=quality, method=6)
    while out.stat().st_size > 200 * 1024 and quality > 40:
        quality -= 10
        img.save(out, "WEBP", quality=quality, method=6)

    print(f"[ok] {out.name}  ({out.stat().st_size // 1024} KB)")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", help="md files (if empty, use --all)")
    ap.add_argument("--all", action="store_true", help="process every article")
    ap.add_argument("--force", action="store_true", help="regenerate existing")
    args = ap.parse_args()

    if args.all:
        targets = sorted(CONTENT_DIR.glob("*.md"))
    else:
        targets = [Path(p) for p in args.paths]

    if not targets:
        ap.print_help()
        sys.exit(1)

    for md in targets:
        if not md.exists():
            print(f"[skip] {md} not found")
            continue
        generate_cover(md, force=args.force)


if __name__ == "__main__":
    main()
