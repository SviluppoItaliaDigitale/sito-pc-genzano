#!/usr/bin/env python3
"""Post-produzione scheda colorabile infanzia.

Prende l'immagine generata dall'AI (line art b/n disegni), automaticamente:
1. Crop dei margini bianchi superiore/inferiore in eccesso
2. Sovrapposizione del logo del Gruppo PC Genzano (a colori, in alto centrato)
3. Footer testuale con revisione e URL del sito
4. Quantizzazione a 64 colori per ridurre il peso del file

Output: PNG ottimizzato pronto per il sito.

Uso:
  python3 post-produzione-scheda-infanzia.py <input.png> <output.png>
"""
from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LOGO = Path("/home/iu0qvw/sito-pc-genzano/static/images/logo-pc-genzano-hires.png")
FONT_BOLD = Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf")

LOGO_SIZE = 260           # logo finale 260x260 (ingrandito per migliore presenza)
HEADER_MARGIN_TOP = 30    # margine sopra il logo
HEADER_MARGIN_BOTTOM = 30 # margine sotto il logo (prima del contenuto AI)
FOOTER_H = 90             # spazio in basso per il footer testuale
WHITE_THRESHOLD = 200     # pixel < 200 = contenuto, >= 200 = bianco
MIN_DARK_PIXELS = 20      # min pixel scuri per considerare una riga "con contenuto"
BREATHING_ROOM = 20       # px di respiro intorno al contenuto AI dopo il crop

FOOTER_TEXT = "Rev. 02 – Maggio 2026  ·  protezionecivilegenzano.it"


def find_content_bounds(img: Image.Image) -> tuple[int, int]:
    """Trova la prima e l'ultima riga con contenuto (pixel scuri).

    Restituisce (top, bottom): top = primo Y con contenuto, bottom = ultimo Y.
    """
    gray = img.convert("L")
    width, height = gray.size
    px = gray.load()

    top = 0
    for y in range(height):
        dark = sum(1 for x in range(width) if px[x, y] < WHITE_THRESHOLD)
        if dark > MIN_DARK_PIXELS:
            top = y
            break

    bottom = height - 1
    for y in range(height - 1, 0, -1):
        dark = sum(1 for x in range(width) if px[x, y] < WHITE_THRESHOLD)
        if dark > MIN_DARK_PIXELS:
            bottom = y
            break

    return top, bottom


def main(input_path: Path, output_path: Path) -> None:
    scheda = Image.open(input_path).convert("RGB")
    logo = Image.open(LOGO).convert("RGBA")

    # crop dei margini bianchi superiore/inferiore in eccesso
    top, bottom = find_content_bounds(scheda)
    crop_top = max(0, top - BREATHING_ROOM)
    crop_bottom = min(scheda.size[1], bottom + BREATHING_ROOM)
    scheda_cropped = scheda.crop((0, crop_top, scheda.size[0], crop_bottom))
    width, content_h = scheda_cropped.size

    # nuovo canvas: header (margine + logo + margine) + contenuto cropped + footer
    header_h = HEADER_MARGIN_TOP + LOGO_SIZE + HEADER_MARGIN_BOTTOM
    new_h = header_h + content_h + FOOTER_H
    canvas = Image.new("RGB", (width, new_h), "white")

    # incolla il contenuto AI cropped sotto la fascia logo
    canvas.paste(scheda_cropped, (0, header_h))

    # logo centrato in alto
    logo_resized = logo.resize((LOGO_SIZE, LOGO_SIZE), Image.LANCZOS)
    logo_x = (width - LOGO_SIZE) // 2
    logo_y = HEADER_MARGIN_TOP
    canvas.paste(logo_resized, (logo_x, logo_y), logo_resized)

    # footer testuale centrato
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(str(FONT_BOLD), 24)
    bbox = draw.textbbox((0, 0), FOOTER_TEXT, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    text_x = (width - text_w) // 2
    text_y = header_h + content_h + (FOOTER_H - text_h) // 2 - 4
    draw.text((text_x, text_y), FOOTER_TEXT, fill=(60, 60, 60), font=font)

    # quantizzazione a 64 colori — mantiene il logo a colori, riduce il peso
    canvas_p = canvas.quantize(colors=64, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    canvas_p.save(output_path, format="PNG", optimize=True)

    size_kb = output_path.stat().st_size // 1024
    rimossi = scheda.size[1] - content_h
    print(f"OK -> {output_path}")
    print(f"   dimensioni: {canvas.size} px  |  peso: {size_kb} KB")
    print(f"   crop: {rimossi}px rimossi dai margini AI")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 post-produzione-scheda-infanzia.py <input.png> <output.png>", file=sys.stderr)
        sys.exit(2)
    main(Path(sys.argv[1]), Path(sys.argv[2]))
