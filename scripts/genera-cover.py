#!/usr/bin/env python3
"""
Genera cover grafiche istituzionali per gli articoli del sito.
- Sfondo: gradiente blu istituzionale + accent color per badge
- Titolo dell'articolo centrato
- Fascia blu istituzionale inferiore con logo + dicitura

Uso:
    python3 scripts/genera-cover.py content/comunicazioni/2026-04-21-kit-emergenza-domestico-guida-pratica.md
    python3 scripts/genera-cover.py --all
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

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

FONT_BOLD = "Liberation-Sans-Bold"
FONT_REGULAR = "Liberation-Sans"

W, H = 1200, 630
BAND_H = 100


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


def wrap_title(title: str, max_chars: int = 28) -> str:
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
    return "\n".join(lines[:4])


def slug_from_filename(path: Path) -> str:
    return path.stem


def output_path(md_path: Path) -> Path:
    return IMAGES_DIR / f"{md_path.stem}.webp"


def generate_cover(md_path: Path, force: bool = False) -> Path:
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

    accent = BADGE_COLORS.get(badge, PRIMARY)
    # Wrap a 24 caratteri (era 26): titolo più stretto = sta nella safe zone
    # centrale di 75% richiesta da Facebook composer mobile (incident 16/05/2026
    # "preview ingrandita Giro d'Italia tagliata ai lati").
    wrapped = wrap_title(title, 24)

    # Step 1: build base PNG with gradient + badges + title + band + text
    badge_w = 40 + 12 * len(badge)
    base_cmd = [
        "magick",
        "-size", f"{W}x{H}",
        f"gradient:{PRIMARY}-{PRIMARY_DARK}",
        # Accent line top
        "-fill", accent,
        "-draw", f"rectangle 0,0 {W},8",
        # Accent diagonal decoration
        "-fill", accent,
        "-draw", f"polygon {W-180},0 {W},0 {W},220 {W-20},220",
        # Badge pill
        "-fill", accent,
        "-draw", f"roundrectangle 80,70 {80 + badge_w},120 10,10",
        "-fill", WHITE,
        "-font", FONT_BOLD,
        "-pointsize", "22",
        "-gravity", "NorthWest",
        "-annotate", f"+100+82", badge.upper(),
        # Separator line above band
        "-fill", "rgba(255,255,255,0.15)",
        "-draw", f"rectangle 80,{H-BAND_H-30} 1120,{H-BAND_H-29}",
        # Title — centrato per safe zone Facebook composer mobile.
        # Prima era "gravity West +80-30" → fuori dalla safe zone centrale 75%
        # → tagliato nel composer FB mobile. Ora "Center +0-30" → titolo
        # leggibile sia nel post pubblicato 1.91:1 sia nel composer ingrandito.
        # Incident 16/05/2026 "preview Giro d'Italia tagliata ai lati".
        "-fill", WHITE,
        "-font", FONT_BOLD,
        "-pointsize", "50",
        "-interline-spacing", "16",
        "-gravity", "Center",
        "-annotate", f"+0-30", wrapped,
        # Bottom blue band
        "-fill", PRIMARY,
        "-draw", f"rectangle 0,{H-BAND_H} {W},{H}",
        "-fill", "rgba(255,255,255,0.25)",
        "-draw", f"rectangle 0,{H-BAND_H} {W},{H-BAND_H+2}",
        # Text in band
        "-fill", WHITE,
        "-font", FONT_BOLD,
        "-pointsize", "26",
        "-gravity", "NorthWest",
        "-annotate", f"+180+{H-BAND_H+22}", "PROTEZIONE CIVILE",
        "-fill", "rgba(255,255,255,0.85)",
        "-font", FONT_REGULAR,
        "-pointsize", "16",
        "-annotate", f"+180+{H-BAND_H+60}", "Gruppo Comunale Volontari \u2014 Genzano di Roma",
        "PNG:-",
    ]

    # Step 2: composite logo onto base, then export WebP
    base = subprocess.run(base_cmd, capture_output=True)
    if base.returncode != 0:
        print(f"[error] base {md_path.name}: {base.stderr.decode('utf-8', 'ignore')}")
        return None

    logo_y = H - BAND_H + 15
    composite_cmd = [
        "magick",
        "PNG:-",
        "(", str(LOGO), "-resize", "72x72", ")",
        "-geometry", f"+90+{logo_y}",
        "-composite",
        "-quality", "85",
        "-define", "webp:method=6",
        str(out),
    ]
    result = subprocess.run(composite_cmd, input=base.stdout, capture_output=True)
    if result.returncode != 0:
        print(f"[error] {md_path.name}: {result.stderr}")
        return None

    size_kb = out.stat().st_size // 1024
    if size_kb > 200:
        # Recompress at lower quality
        subprocess.run([
            "magick", str(out), "-quality", "75", "-define", "webp:method=6", str(out)
        ], check=False)
        size_kb = out.stat().st_size // 1024

    print(f"[ok] {out.name}  ({size_kb} KB)")
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
