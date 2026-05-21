#!/usr/bin/env python3
"""Genera microtext (microstampa) per il sito di Protezione Civile Genzano.

Tecnica di sicurezza tipografica: da lontano l'output sembra una parola o
un'immagine normale; da vicino (zoom o stampa ad alta risoluzione) le linee e
le ombre sono composte da micro-testo personalizzato leggibile.

Tre modalità:

  text       Una parola/frase "macro" (es. "PROTEZIONE CIVILE") la cui sagoma
             è riempita di micro-testo ripetuto. Da lontano = la parola.
  image      Una foto resa interamente con micro-testo (halftone tipografico):
             le zone scure hanno testo fitto/nero, le chiare testo tenue.
  watermark  Sovrappone una filigrana di micro-testo (diagonale, tenue) a
             un'immagine esistente, come microstampa anti-falsificazione.

Idea unificante: in tutte le modalità l'output è
    composite(strato_microtesto, sfondo, maschera)
dove la maschera cambia per modalità (sagoma del macro-testo, luminanza
invertita della foto, oppure overlay alpha per la filigrana).

Stack: Python + Pillow (come genera-cover.py / applica-fascia-foto.py).
Font: Liberation Sans (fonts-liberation). Nessuna dipendenza da ImageMagick.

Esempi:
  python3 scripts/genera-microtext.py text \\
      --macro "PROTEZIONE CIVILE" \\
      --phrase "Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma · " \\
      --out static/images/microtext/banner.png

  python3 scripts/genera-microtext.py image \\
      --in static/images/logo-pc-genzano.png \\
      --phrase "PC Genzano · " --out /tmp/foto-microtext.png

  python3 scripts/genera-microtext.py watermark \\
      --in static/images/2026-03-18-cover.webp \\
      --phrase "Documento autentico — protezionecivilegenzano.it · " \\
      --out /tmp/cover-filigranata.png
"""
import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PRIMARY = "#003366"
WHITE = "#ffffff"

_FONT_DIRS = [
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/liberation2",
    "/usr/share/fonts/liberation",
    "/usr/share/fonts/TTF",
    "/usr/share/fonts/truetype/dejavu",
    "/Library/Fonts",
    "C:/Windows/Fonts",
]
_FONT_FILES = {
    True: ["LiberationSans-Bold.ttf", "DejaVuSans-Bold.ttf", "arialbd.ttf"],
    False: ["LiberationSans-Regular.ttf", "DejaVuSans.ttf", "arial.ttf"],
}


def font(bold: bool, size: int) -> ImageFont.FreeTypeFont:
    for d in _FONT_DIRS:
        for name in _FONT_FILES[bold]:
            p = Path(d) / name
            if p.exists():
                return ImageFont.truetype(str(p), size)
    for name in _FONT_FILES[bold]:
        try:
            return ImageFont.truetype(name, size)
        except Exception:
            continue
    print("[warn] Liberation Sans non trovato, uso font di default", file=sys.stderr)
    return ImageFont.load_default()


def _rgb(value: str) -> tuple:
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def microtext_layer(size: tuple, phrase: str, micro_size: int,
                    color: tuple, bold: bool = False) -> Image.Image:
    """Strato RGB: la frase ripetuta riga per riga su tutta la tela (testo
    `color` su bianco). È l'"inchiostro" che riempirà la maschera."""
    w, h = size
    layer = Image.new("RGB", size, (255, 255, 255))
    d = ImageDraw.Draw(layer)
    f = font(bold, micro_size)
    # larghezza media di un carattere per stimare quante ripetizioni servono
    char_w = max(1, d.textlength("M", font=f) * 0.6)
    reps = int(w / (d.textlength(phrase, font=f) or char_w)) + 2
    line = phrase * reps
    line_h = micro_size + max(1, round(micro_size * 0.15))
    y = 0
    while y < h:
        d.text((0, y), line, font=f, fill=color)
        y += line_h
    return layer


def macro_mask(size: tuple, text: str) -> Image.Image:
    """Maschera L: 255 dove c'è il macro-testo (sagoma da riempire).
    Il macro-testo può essere multilinea usando '|' come separatore di riga:
    più righe = lettere più alte e spesse = sagoma più leggibile da lontano."""
    w, h = size
    lines = [ln for ln in text.split("|")]
    n = len(lines)
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)

    def fits(sz: int) -> bool:
        f = font(True, sz)
        widest = max(d.textlength(ln, font=f) for ln in lines)
        line_h = (f.getbbox("Ag")[3] - f.getbbox("Ag")[1]) * 1.05
        return widest <= w * 0.92 and line_h * n <= h * 0.82

    lo, hi, best = 8, h * 2, 8
    while lo <= hi:
        mid = (lo + hi) // 2
        if fits(mid):
            best, lo = mid, mid + 1
        else:
            hi = mid - 1
    f = font(True, best)
    spacing = best * 0.12
    d.multiline_text((w / 2, h / 2), "\n".join(lines), font=f, fill=255,
                     anchor="mm", align="center", spacing=spacing)
    return mask


def supersample(fn, size, factor, *args, **kwargs):
    big = (size[0] * factor, size[1] * factor)
    return fn(big, *args, **kwargs)


def mode_text(args) -> Image.Image:
    size = (args.width, args.height)
    color = _rgb(args.color)
    micro = microtext_layer(size, args.phrase, args.microsize, color, bold=False)
    # maschera macro ad alta risoluzione poi ridotta = bordi netti e antialias
    mask_big = macro_mask((size[0] * 3, size[1] * 3), args.macro)
    mask = mask_big.resize(size, Image.LANCZOS)
    bg = Image.new("RGB", size, _rgb(args.bg))
    out = Image.composite(micro, bg, mask)
    if args.base:
        out = _overlay_on_base(out, mask, args)
    return out


def mode_image(args) -> Image.Image:
    src = Image.open(args.infile).convert("L")
    size = (args.width, args.height) if args.width and args.height else src.size
    src = src.resize(size, Image.LANCZOS)
    if args.contrast != 1.0:
        from PIL import ImageEnhance
        src = ImageEnhance.Contrast(src).enhance(args.contrast)
    color = _rgb(args.color)
    micro = microtext_layer(size, args.phrase, args.microsize, color, bold=False)
    # maschera = luminanza invertita: scuro nella foto -> testo fitto/scuro
    from PIL import ImageOps
    mask = ImageOps.invert(src)
    bg = Image.new("RGB", size, _rgb(args.bg))
    return Image.composite(micro, bg, mask)


def mode_watermark(args) -> Image.Image:
    base = Image.open(args.infile).convert("RGB")
    size = base.size
    color = _rgb(args.color)
    # strato microtesto ruotato 45°, su tela sovradimensionata per coprire dopo la rotazione
    diag = int((size[0] ** 2 + size[1] ** 2) ** 0.5)
    layer = microtext_layer((diag, diag), args.phrase, args.microsize, color)
    # rendi bianco -> trasparente, testo -> color con alpha = opacity
    layer = layer.convert("RGBA")
    px = layer.load()
    a = int(255 * args.opacity)
    # costruisci alpha: dove non è bianco (c'è testo) opacity, altrimenti 0
    r, g, b = layer.split()[0], layer.split()[1], layer.split()[2]
    from PIL import ImageChops, ImageOps
    gray = ImageOps.grayscale(layer)
    alpha = ImageOps.invert(gray).point(lambda v: a if v > 20 else 0)
    layer.putalpha(alpha)
    if args.angle:
        layer = layer.rotate(args.angle, expand=False, resample=Image.BICUBIC)
    # centra e ritaglia alla dimensione della base
    left = (layer.width - size[0]) // 2
    top = (layer.height - size[1]) // 2
    layer = layer.crop((left, top, left + size[0], top + size[1]))
    out = base.convert("RGBA")
    out.alpha_composite(layer)
    return out.convert("RGB")


def _overlay_on_base(rendered: Image.Image, mask: Image.Image, args) -> Image.Image:
    base = Image.open(args.base).convert("RGB").resize(rendered.size, Image.LANCZOS)
    faded = Image.composite(rendered, base, mask.point(lambda v: int(v * args.opacity)))
    return faded


def save(img: Image.Image, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    ext = out.suffix.lower()
    if ext == ".webp":
        q = 90
        img.save(out, "WEBP", quality=q, method=6)
        while out.stat().st_size > 300 * 1024 and q > 50:
            q -= 10
            img.save(out, "WEBP", quality=q, method=6)
    else:
        img.save(out)
    print(f"[ok] {out}  ({out.stat().st_size // 1024} KB, {img.size[0]}x{img.size[1]})")


def main() -> None:
    ap = argparse.ArgumentParser(description="Generatore di microtext / microstampa")
    ap.add_argument("mode", choices=["text", "image", "watermark"])
    ap.add_argument("--macro", default="PROTEZIONE CIVILE",
                    help="testo grande (modalità text)")
    ap.add_argument("--phrase",
                    default="Protezione Civile Genzano di Roma · protezionecivilegenzano.it · ",
                    help="micro-testo personalizzato ripetuto che compone le linee "
                         "(default: riferimento univoco al Gruppo + dominio ufficiale)")
    ap.add_argument("--in", dest="infile", help="immagine di input (image/watermark)")
    ap.add_argument("--base", help="immagine di sfondo opzionale (modalità text)")
    ap.add_argument("--out", required=True, help="file di output (.png/.webp)")
    ap.add_argument("--width", type=int, default=2000)
    ap.add_argument("--height", type=int, default=700)
    ap.add_argument("--microsize", type=int, default=12, help="corpo del micro-testo in px")
    ap.add_argument("--color", default=PRIMARY, help="colore inchiostro (hex)")
    ap.add_argument("--bg", default=WHITE, help="colore sfondo (hex)")
    ap.add_argument("--opacity", type=float, default=0.18, help="opacità filigrana 0-1")
    ap.add_argument("--angle", type=float, default=30.0, help="rotazione filigrana (gradi)")
    ap.add_argument("--contrast", type=float, default=1.4, help="contrasto foto (image)")
    args = ap.parse_args()

    if args.mode in ("image", "watermark") and not args.infile:
        ap.error(f"--in è obbligatorio in modalità {args.mode}")

    if args.mode == "text":
        img = mode_text(args)
    elif args.mode == "image":
        img = mode_image(args)
    else:
        img = mode_watermark(args)

    save(img, Path(args.out))


if __name__ == "__main__":
    main()
