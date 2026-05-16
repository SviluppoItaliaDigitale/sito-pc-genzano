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


def has_brand_band(im: Image.Image) -> bool:
    """Rileva se la foto sorgente ha già una fascia blu istituzionale in basso.

    Strategia robusta (post-incident 16 maggio 2026 "doppia fascia Giro
    d'Italia Formia"): campiona 3 pixel a 98% h (centro fascia attesa) E
    3 pixel a 80% h (zona foto pura sopra la fascia). Se i bottom sono
    blu istituzionale (#003366 ± 30) e gli upper NO, la fascia è già
    presente → lo script va in skip per non sovrapporre una seconda
    fascia.

    Il check al 92% h era falsato perché cadeva in zona di transizione
    foto/fascia, con pixel impuri che davano falsi negativi.
    """
    w, h = im.size
    rgb = im.convert("RGB") if im.mode != "RGB" else im
    BRAND_R, BRAND_G, BRAND_B = PRIMARY  # (0, 51, 102)
    TOL = 30

    def is_brand_blue(px):
        r, g, b = px[:3]
        return (
            abs(r - BRAND_R) <= TOL
            and abs(g - BRAND_G) <= TOL
            and abs(b - BRAND_B) <= TOL
        )

    # 3 sample a 98% h (centro fascia, se presente)
    bottom_samples = [
        rgb.getpixel((int(w * x), int(h * 0.98))) for x in (0.2, 0.5, 0.8)
    ]
    # 3 sample a 80% h (sopra la fascia, in zona foto pura)
    above_samples = [
        rgb.getpixel((int(w * x), int(h * 0.80))) for x in (0.2, 0.5, 0.8)
    ]
    bottom_blue_count = sum(is_brand_blue(p) for p in bottom_samples)
    above_blue_count = sum(is_brand_blue(p) for p in above_samples)
    # Almeno 2 su 3 in basso devono essere blu brand E meno di 2 in alto
    return bottom_blue_count >= 2 and above_blue_count < 2


def apply_band(src_path: Path, out_name: str, force: bool = False) -> Path:
    if not src_path.is_file():
        raise FileNotFoundError(f"sorgente non trovata: {src_path}")
    if not LOGO_PATH.is_file():
        raise FileNotFoundError(f"logo non trovato: {LOGO_PATH}")

    out_path = IMAGES_DIR / f"{out_name}.webp"

    # 1) Carica e ridimensiona la foto a larghezza WIDTH (mantenendo aspect)
    src = Image.open(src_path)

    # 1.PRE) IDEMPOTENZA — se la foto sorgente HA GIÀ una fascia blu
    # istituzionale, NON applicare una seconda fascia. Skip per evitare
    # doppia fascia sovrapposta (incident 16 maggio 2026 "Giro d'Italia
    # Formia" — 3 foto inline con doppia fascia visibile sotto al
    # contenuto). Override possibile con --force.
    if not force and has_brand_band(src):
        print(
            f"[skip] La foto sorgente '{src_path.name}' ha già una fascia blu "
            f"istituzionale (pixel @98%h=brand-blue, @80%h=pura).",
            file=sys.stderr,
        )
        print(
            f"       Non applico una seconda fascia. Usa --force se vuoi "
            f"davvero sovrascrivere il file di destinazione.",
            file=sys.stderr,
        )
        print(f"File NON modificato: {out_path}", file=sys.stderr)
        return out_path

    # 1a) STRIP EXIF — privacy: rimuove coordinate GPS, timestamp,
    # modello camera, autore, software, e altri metadati identificativi
    # che le foto WhatsApp/smartphone portano con sé. Le foto utente
    # pubblicate sul sito istituzionale non devono mai esporre la
    # posizione geografica della persona che ha scattato.
    # Tecnica: ricreare l'immagine da zero copia solo i pixel, scarta
    # tutti i campi EXIF/IPTC/XMP del file sorgente.
    if src.mode in ("RGBA", "LA", "P"):
        src = src.convert("RGB")
    src_pixels = list(src.getdata())
    src_clean = Image.new(src.mode, src.size)
    src_clean.putdata(src_pixels)
    src = src_clean

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
    # Parsing minimale: supporta `--force` come flag opzionale prima/dopo gli args
    args = [a for a in sys.argv[1:] if a != "--force"]
    force = "--force" in sys.argv[1:]
    if len(args) != 2:
        print(__doc__, file=sys.stderr)
        print(
            "\nUso: python3 applica-fascia-foto.py <src> <nome-output> [--force]",
            file=sys.stderr,
        )
        print(
            "\nIDEMPOTENZA: se la foto sorgente ha già una fascia blu "
            "istituzionale, lo script va in skip per non applicare una "
            "seconda fascia (incident 16/05/2026). Usa --force per "
            "bypassare il check.",
            file=sys.stderr,
        )
        sys.exit(1)
    src = Path(args[0])
    name = args[1]
    try:
        apply_band(src, name, force=force)
    except FileNotFoundError as e:
        print(f"[error] {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"[error] {type(e).__name__}: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
