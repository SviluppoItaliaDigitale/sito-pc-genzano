"""Cornice di microtesto anti-appropriazione per le immagini generate dal sito.

Incide lungo i quattro bordi, in caratteri di pochi pixel, la provenienza
dell'immagine (Gruppo, dominio, anno). Da lontano la cornice non si nota,
ingrandendo si legge: chi ripubblica l'immagine si porta dietro l'attribuzione,
e ritagliarla lascia un'immagine evidentemente rifilata. Stessa idea della
cornice della cartina meteo (microtext_frame() in genera-meteo-lazio.py), qui
in versione raster con Pillow per cover tipografiche e immagini social.

Il colore si adatta al fondo pixel per pixel: schiarisce dove il fondo è scuro
e scurisce dove è chiaro, con opacità bassa, così resta un tono vicino al fondo
su qualunque colore (blu istituzionale, accento del badge, sfondi sfocati).
Decorativa: non cambia l'alt delle immagini. La usano genera-cover.py e
genera-immagini-social.py; non va applicata alle foto, solo ai bordi
dell'immagine composta.
"""

from __future__ import annotations

import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

TESTO_BASE = ("PROTEZIONE CIVILE GENZANO DI ROMA · www.protezionecivilegenzano.it · "
              "elaborazione grafica del Gruppo Comunale Volontari di Protezione Civile · "
              "© {anno} · ")

_FONT_CANDIDATI = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
    "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/TTF/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def _font(corpo: int) -> ImageFont.ImageFont:
    for p in _FONT_CANDIDATI:
        if Path(p).exists():
            return ImageFont.truetype(p, corpo)
    try:
        return ImageFont.truetype("LiberationSans-Bold.ttf", corpo)
    except OSError:
        return ImageFont.load_default()


def _striscia(lunghezza: int, spessore: int, testo: str,
              font: ImageFont.ImageFont) -> Image.Image:
    """Maschera L (lunghezza x spessore) con il testo ripetuto fino a riempirla,
    troncato all'ultima parola intera (niente lettere mozzate sul bordo)."""
    m = Image.new("L", (lunghezza, spessore), 0)
    d = ImageDraw.Draw(m)
    larg = max(1, d.textlength(testo, font=font))
    parole = (testo * (int(lunghezza / larg) + 2)).split(" ")
    riga = " ".join(parole)
    while parole and d.textlength(riga, font=font) > lunghezza:
        parole.pop()
        riga = " ".join(parole)
    riga = riga.rstrip(" ·")
    d.text((0, spessore / 2), riga, font=font, fill=255, anchor="lm")
    return m


def _incidi(img: Image.Image, maschera: Image.Image, pos: tuple,
            intensita: float) -> None:
    """Applica la maschera in pos: schiarisce su fondo scuro, scurisce su chiaro."""
    x, y = pos
    box = (x, y, x + maschera.width, y + maschera.height)
    zona = img.crop(box)
    lum = zona.convert("L")
    tono = lum.point(lambda v: 255 if v < 140 else 0)
    bersaglio = Image.merge("RGB", (tono, tono, tono))
    alfa = maschera.point(lambda v: round(v * intensita))
    img.paste(Image.composite(bersaglio, zona, alfa), box[:2])


def cornice_microtesto(img: Image.Image, corpo: int = 8, intensita: float = 0.26,
                       anno: int | None = None) -> Image.Image:
    """Restituisce una copia di img con la cornice di microtesto sui 4 bordi.

    corpo: altezza del carattere in pixel (7-9 per immagini da 1080-1200 px).
    intensita: opacità dello scostamento di tono (0-1); bassa = poco visibile.
    La striscia occupa i primi corpo+4 pixel di ogni bordo; gli angoli restano
    liberi. Il modo dell'immagine (RGB/RGBA) è preservato.
    """
    anno = anno or datetime.date.today().year
    testo = TESTO_BASE.format(anno=anno)
    font = _font(corpo)
    W, H = img.size
    s = corpo + 4

    alfa_orig = img.getchannel("A") if img.mode == "RGBA" else None
    lav = img.convert("RGB")

    oriz = _striscia(W - 2 * s, s, testo, font)
    vert = _striscia(H - 2 * s, s, testo, font)
    _incidi(lav, oriz, (s, 0), intensita)                       # alto
    _incidi(lav, oriz, (s, H - s), intensita)                   # basso
    _incidi(lav, vert.rotate(90, expand=True), (0, s), intensita)       # sinistra, dal basso
    _incidi(lav, vert.rotate(-90, expand=True), (W - s, s), intensita)  # destra, dall'alto

    if alfa_orig is not None:
        lav = lav.convert("RGBA")
        lav.putalpha(alfa_orig)
    elif img.mode != "RGB":
        lav = lav.convert(img.mode)
    return lav
