#!/usr/bin/env python3
"""Post-produzione scheda colorabile infanzia.

Prende l'immagine generata dall'AI (line art b/n disegni), aggiunge:
- in alto: logo del Gruppo PC Genzano a colori, centrato
- in basso: footer testuale "Rev. NN - Mese AAAA · URL"

Output: PNG ottimizzato pronto per il sito.

Uso:
  python3 post-produzione-scheda.py <input.png> <output.png>
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LOGO = Path("/home/iu0qvw/sito-pc-genzano/static/images/logo-pc-genzano-hires.png")
FONT_BOLD = Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf")

HEADER_H = 240   # spazio in alto per il logo + un po' di aria
FOOTER_H = 90    # spazio in basso per il footer testuale
LOGO_SIZE = 200  # logo finale 200x200 (su canvas 1024 wide)
FOOTER_TEXT = "Rev. 02 – Maggio 2026  ·  protezionecivilegenzano.it"


def main(input_path: Path, output_path: Path) -> None:
    scheda = Image.open(input_path).convert("RGB")
    logo = Image.open(LOGO).convert("RGBA")

    width, original_h = scheda.size
    new_h = HEADER_H + original_h + FOOTER_H
    canvas = Image.new("RGB", (width, new_h), "white")

    # incolla la scheda AI sotto la fascia logo
    canvas.paste(scheda, (0, HEADER_H))

    # logo centrato in alto, con margine verticale equilibrato
    logo_resized = logo.resize((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)
    logo_x = (width - LOGO_SIZE) // 2
    logo_y = (HEADER_H - LOGO_SIZE) // 2
    canvas.paste(logo_resized, (logo_x, logo_y), logo_resized)

    # footer testuale centrato
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(str(FONT_BOLD), 26)
    bbox = draw.textbbox((0, 0), FOOTER_TEXT, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = (width - text_w) // 2
    text_y = HEADER_H + original_h + (FOOTER_H - text_h) // 2 - 4
    draw.text((text_x, text_y), FOOTER_TEXT, fill=(60, 60, 60), font=font)

    # quantizzazione a palette adattiva 64 colori — mantiene i colori del logo
    # con perdita visivamente irrilevante e dimensione contenuta
    canvas_p = canvas.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    canvas_p.save(output_path, format="PNG", optimize=True)

    print(f"OK -> {output_path}  ({output_path.stat().st_size // 1024} KB)  {canvas.size}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 post-produzione-scheda.py <input.png> <output.png>", file=sys.stderr)
        sys.exit(2)
    main(Path(sys.argv[1]), Path(sys.argv[2]))
