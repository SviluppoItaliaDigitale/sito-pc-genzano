#!/usr/bin/env python3
"""
Applica la fascia blu istituzionale a una foto esistente.
Output: WebP 1200px in static/images/<nome>.webp con fascia blu in basso,
logo, testo "PROTEZIONE CIVILE / Gruppo Comunale Volontari — Genzano di Roma".

Riscritto in Python+Pillow per essere cross-platform e indipendente da
ImageMagick (versioni v6/v7, delegate WebP, policy.xml). Funziona su:
  - Ubuntu desktop (Pillow >= 9, font-liberation, libwebp)
  - GitHub Actions runner ubuntu-latest (apt install python3-pil)
  - macOS, Windows (Pillow installato via pip)

Uso:
  python3 scripts/applica-fascia-foto.py <src.jpg> <nome-output-senza-ext>

Esempi:
  python3 scripts/applica-fascia-foto.py /tmp/foto-evento.jpg 2026-04-27-evento
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = ROOT / "static" / "images"
LOGO_PATH = IMAGES_DIR / "logo-pc-genzano.png"

WIDTH = 1200
BAND_HEIGHT = 100
PRIMARY = (0, 51, 102)  # #003366
WHITE = (255, 255, 255)
WHITE_90 = (255, 255, 255, int(255 * 0.90))
SEPARATOR_COLOR = (255, 255, 255, int(255 * 0.25))

MAX_KB_TARGET = 200


def find_font(weight: str = "Bold") -> Path:
    """Trova LiberationSans-{weight}.ttf attraverso percorsi noti.
    Supporta Ubuntu (apt fonts-liberation), Debian, runner GitHub Actions."""
    candidates = [
        f"/usr/share/fonts/truetype/liberation/LiberationSans-{weight}.ttf",
        f"/usr/share/fonts/liberation/LiberationSans-{weight}.ttf",
        f"/usr/share/fonts/truetype/liberation2/LiberationSans-{weight}.ttf",
        # Fallback macOS/Windows
        f"/System/Library/Fonts/Helvetica.ttc",
        f"C:/Windows/Fonts/arialbd.ttf" if weight == "Bold" else "C:/Windows/Fonts/arial.ttf",
    ]
    for c in candidates:
        if Path(c).is_file():
            return Path(c)
    # Ultimo fallback: font default Pillow (basso quality ma non si blocca)
    return None


def apply_band(src_path: Path, out_name: str) -> Path:
    if not src_path.is_file():
        raise FileNotFoundError(f"sorgente non trovata: {src_path}")
    if not LOGO_PATH.is_file():
        raise FileNotFoundError(f"logo non trovato: {LOGO_PATH}")

    out_path = IMAGES_DIR / f"{out_name}.webp"

    # 1) Carica e ridimensiona la foto a larghezza WIDTH (mantenendo aspect)
    src = Image.open(src_path)
    if src.mode in ("RGBA", "LA", "P"):
        # Per la composizione finale usiamo RGB
        src = src.convert("RGB")
    aspect = src.height / src.width
    new_h = int(WIDTH * aspect)
    src = src.resize((WIDTH, new_h), Image.LANCZOS)

    # 2) Composizione: foto sopra + fascia blu sotto
    total_h = new_h + BAND_HEIGHT
    canvas = Image.new("RGB", (WIDTH, total_h), PRIMARY)
    canvas.paste(src, (0, 0))

    # 3) Linea separatrice bianca semi-trasparente sopra la fascia
    overlay = Image.new("RGBA", (WIDTH, total_h), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    odraw.rectangle([0, new_h, WIDTH, new_h + 2], fill=SEPARATOR_COLOR)
    canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")

    # 4) Logo a sinistra (resize a 72x72)
    try:
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo.thumbnail((72, 72), Image.LANCZOS)
        # Posizione: x=90 (margine sinistro), y centrato verticalmente nella fascia
        logo_y = new_h + (BAND_HEIGHT - logo.height) // 2
        canvas.paste(logo, (90, logo_y), logo)
    except Exception as e:
        print(f"[warn] logo non applicato: {e}", file=sys.stderr)

    # 5) Testo a destra del logo
    draw = ImageDraw.Draw(canvas)
    font_bold_path = find_font("Bold")
    font_reg_path = find_font("Regular")

    try:
        font_title = ImageFont.truetype(str(font_bold_path), 26) if font_bold_path else ImageFont.load_default()
        font_sub = ImageFont.truetype(str(font_reg_path), 16) if font_reg_path else ImageFont.load_default()
    except Exception as e:
        print(f"[warn] fallback font default Pillow: {e}", file=sys.stderr)
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()

    # Testo: "PROTEZIONE CIVILE" + sottotitolo
    text_x = 180
    title_y = new_h + 22
    sub_y = new_h + 60
    draw.text((text_x, title_y), "PROTEZIONE CIVILE", font=font_title, fill=WHITE)
    draw.text((text_x, sub_y), "Gruppo Comunale Volontari — Genzano di Roma", font=font_sub, fill=WHITE)

    # 6) Salvataggio WebP con compressione progressiva fino a <= 200 KB
    out_path.parent.mkdir(parents=True, exist_ok=True)
    save_webp(canvas, out_path)

    size_kb = out_path.stat().st_size // 1024
    print(f"[ok] {out_path.name}  ({size_kb} KB, {WIDTH}x{total_h}px)")
    return out_path


def save_webp(img: Image.Image, out_path: Path):
    """Salva in WebP comprimendo fino a <= 200 KB. Loop progressivo:
    qualità 85 -> 75 -> 60 -> 50 -> 40 -> 30, poi resize 1000/900/800/700px."""
    img.save(out_path, "WEBP", quality=85, method=6)
    size_kb = out_path.stat().st_size // 1024
    if size_kb <= MAX_KB_TARGET:
        return

    for q in (75, 60, 50, 40, 30):
        img.save(out_path, "WEBP", quality=q, method=6)
        size_kb = out_path.stat().st_size // 1024
        if size_kb <= MAX_KB_TARGET:
            return

    # Riduzione larghezza progressiva
    for new_w in (1000, 900, 800, 700):
        ratio = new_w / img.width
        new_h = int(img.height * ratio)
        smaller = img.resize((new_w, new_h), Image.LANCZOS)
        smaller.save(out_path, "WEBP", quality=75, method=6)
        size_kb = out_path.stat().st_size // 1024
        if size_kb <= MAX_KB_TARGET:
            return


def main():
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    src = Path(sys.argv[1])
    name = sys.argv[2]
    try:
        apply_band(src, name)
    except FileNotFoundError as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"[error] {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
