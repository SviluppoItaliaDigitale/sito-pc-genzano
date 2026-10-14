#!/usr/bin/env python3
"""Disegna i tre grafici del dossier «Il clima che cambia i rischi» (massime di luglio,
giorni con almeno 30 °C, pioggia annua a Genzano) come WebP 1400×800 in static/images/dossier/.
Legge static/open-data/clima-{luglio-temperature,giorni-30-gradi,pioggia-annuale}-genzano.json.
Si lancia dopo scripts/genera-clima-castelli.py, quando i dati cambiano: medie e anni si ricalcolano."""

from __future__ import annotations

import json
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
DATI = ROOT / "static" / "open-data"
USCITA = ROOT / "static" / "images" / "dossier"
# Titillium Web, il carattere del design system .italia: gli stessi file TTF
# usati da scripts/genera-immagini-social.py.
FONT_DIR = ROOT / "static" / "vendor" / "bootstrap-italia" / "fonts" / "Titillium_Web"

LARGHEZZA, ALTEZZA = 1400, 800
MARGINE_SX, MARGINE_DX = 52, 48
# Righe della tacca più alta e della base: 520 pixel si dividono senza resto
# sia in 4 intervalli (luglio, pioggia) sia in 5 (giorni caldi).
GRAFICO_ALTO, GRAFICO_BASSO = 186, 706
# WebP senza perdita: a tinte piatte pesa meno della compressione con perdita
# (circa 15 KB contro 38) e non sbava il colore sui segni sottili, come i
# tratti delle medie e il segno di un valore zero.
WEBP = {"lossless": True, "quality": 100, "method": 6}
PESO_MASSIMO = 200 * 1024                # limite delle immagini del sito
ANNI_PER_MEDIA = 10                      # primo e ultimo decennio della serie

FONDO = (10, 21, 38)            # #0a1526, blu notte
TITOLO = (241, 246, 252)
SOTTOTITOLO = (178, 189, 207)
GRIGLIA = (47, 58, 80)
ETICHETTE = (154, 165, 181)
CREDITO = (138, 149, 167)
GRIGIO = (169, 182, 204)        # media del primo decennio
AMBRA = (255, 190, 46)          # media dell'ultimo decennio, #ffbe2e del sito

DATI_APERTI = "dati: protezionecivilegenzano.it/open-data"
CREDITO_ERA5_LAND = ("Elaborazione del Gruppo su rianalisi ERA5-Land via Open-Meteo "
                     f"(CC BY 4.0) — {DATI_APERTI}")
CREDITO_ERA5 = ("Elaborazione del Gruppo su rianalisi ERA5 via Open-Meteo "
                f"(CC BY 4.0) — {DATI_APERTI}")

# Ogni grafico ha un titolo che afferma qualcosa: «verifica» controlla che i
# dati lo sostengano ancora, altrimenti lo script si ferma e chiede di
# riscriverlo. I sottotitoli ricevono gli anni della serie in {anni}.
GRAFICI = [
    {
        "dati": "clima-luglio-temperature-genzano.json",
        "uscita": "clima-luglio-genzano.webp",
        "titolo": "Le estati di Genzano si scaldano",
        "sottotitolo": "Temperatura massima media di luglio, {anni} (°C) — scala da {minimo} °C",
        "asse": (20, 32, 3),
        "decimali": 1,
        "colore": (122, 168, 225),          # azzurro
        "credito": CREDITO_ERA5_LAND,
        "verifica": lambda prima, dopo, valori: dopo > prima,
        "motivo": "la media dell'ultimo decennio non è più alta di quella del primo",
    },
    {
        "dati": "clima-giorni-30-gradi-genzano.json",
        "uscita": "clima-giorni-caldi-genzano.webp",
        "titolo": "Le giornate da 30 °C sono raddoppiate",
        "sottotitolo": "Giorni all'anno con massima di almeno 30 °C a Genzano, {anni}",
        "asse": (0, 50, 10),
        "decimali": 1,
        "colore": (218, 84, 79),            # rosso corallo
        "credito": CREDITO_ERA5_LAND,
        "verifica": lambda prima, dopo, valori: dopo >= 2 * prima,
        "motivo": "la media dell'ultimo decennio non è almeno il doppio di quella del primo",
    },
    {
        "dati": "clima-pioggia-annuale-genzano.json",
        "uscita": "clima-pioggia-genzano.webp",
        "titolo": "La pioggia cambia molto da un anno all'altro",
        "sottotitolo": "Precipitazioni totali annue a Genzano, {anni} (mm)",
        "asse": (0, 1600, 400),
        "decimali": 0,
        "colore": (111, 190, 211),          # azzurro-acqua
        "credito": CREDITO_ERA5,
        "verifica": lambda prima, dopo, valori: max(valori) >= Decimal("1.5") * min(valori),
        "motivo": "l'anno più piovoso non arriva a una volta e mezza il più secco",
    },
]


def carattere(peso: str, corpo: int) -> ImageFont.FreeTypeFont:
    file = FONT_DIR / f"titillium-web-v10-latin-ext_latin-{peso}.ttf"
    if not file.is_file():
        raise SystemExit(f"Manca il carattere {file}")
    return ImageFont.truetype(str(file), corpo)


F_TITOLO = carattere("700", 34)
F_SOTTOTITOLO = carattere("regular", 21)
F_LEGENDA = carattere("600", 23)
F_ASSI = carattere("regular", 20)
F_CREDITO = carattere("regular", 20)


def altezza_cifre(font: ImageFont.FreeTypeFont) -> int:
    """Altezza delle cifre sopra la linea di base: serve a centrare le scritte."""
    return -ImageDraw.Draw(Image.new("RGB", (8, 8))).textbbox(
        (0, 0), "0123456789", font=font, anchor="ls")[1]


def numero_it(valore, decimali: int) -> str:
    """Numero all'italiana: virgola decimale e punto delle migliaia."""
    q = Decimal(str(valore)).quantize(Decimal(1).scaleb(-decimali), rounding=ROUND_HALF_UP)
    intero, _, decimale = f"{abs(q):f}".partition(".")
    gruppi = []
    while len(intero) > 3:
        gruppi.insert(0, intero[-3:])
        intero = intero[:-3]
    gruppi.insert(0, intero)
    testo = ("-" if q < 0 else "") + ".".join(gruppi)
    return f"{testo},{decimale}" if decimale else testo


def carica(cfg: dict) -> dict:
    dati = json.loads((DATI / cfg["dati"]).read_text(encoding="utf-8"))
    anni = [int(a) for a in dati["x"]]
    valori = [Decimal(str(v)) for v in dati["serie"][0]["valori"] if v is not None]
    if len(valori) != len(anni):
        raise SystemExit(f"{cfg['dati']}: anni e valori non corrispondono o manca un valore")
    if anni != list(range(anni[0], anni[0] + len(anni))):
        raise SystemExit(f"{cfg['dati']}: gli anni non sono consecutivi")
    if len(anni) < 2 * ANNI_PER_MEDIA:
        raise SystemExit(f"{cfg['dati']}: servono almeno {2 * ANNI_PER_MEDIA} anni")

    def media(tratto):
        return sum(tratto) / Decimal(len(tratto))

    # Primo e ultimo decennio della serie; gli anni in mezzo restano fuori
    # (con la serie 2005-2025 è escluso il 2015).
    prima = media(valori[:ANNI_PER_MEDIA])
    dopo = media(valori[-ANNI_PER_MEDIA:])
    if not cfg["verifica"](prima, dopo, valori):
        raise SystemExit(f"«{cfg['titolo']}»: {cfg['motivo']} "
                         f"({numero_it(prima, 1)} e {numero_it(dopo, 1)}). Riscrivi il titolo.")

    minimo, massimo, passo = cfg["asse"]
    if min(valori) < minimo:
        raise SystemExit(f"{cfg['dati']}: un valore scende sotto {minimo}, la base dell'asse")
    while max(valori) > massimo:           # l'asse cresce di una tacca alla volta
        massimo += passo
    unita = dati["unita"]
    decimali = cfg["decimali"]
    return {
        "anni": anni,
        "valori": valori,
        "tacche": list(range(minimo, massimo + 1, passo)),
        "sottotitolo": cfg["sottotitolo"].format(anni=f"{anni[0]}–{anni[-1]}",
                                                 minimo=numero_it(minimo, 0)),
        "medie": [
            (prima, GRIGIO, f"media {anni[0]}-{anni[ANNI_PER_MEDIA - 1]}: "
                            f"{numero_it(prima, decimali)} {unita}"),
            (dopo, AMBRA, f"media {anni[-ANNI_PER_MEDIA]}-{anni[-1]}: "
                          f"{numero_it(dopo, decimali)} {unita}"),
        ],
    }


class Ingombri:
    """Riquadri di ciò che si disegna: nulla deve uscire dall'immagine né
    toccare altro (scritte, campioni della legenda, area delle barre)."""

    def __init__(self) -> None:
        self.voci: list[tuple[str, tuple[int, int, int, int]]] = []

    def aggiungi(self, nome: str, riquadro) -> None:
        self.voci.append((nome, tuple(int(v) for v in riquadro)))

    def controlla(self, file: str) -> None:
        for nome, (x0, y0, x1, y1) in self.voci:
            if x0 < 8 or y0 < 8 or x1 > LARGHEZZA - 8 or y1 > ALTEZZA - 8:
                raise SystemExit(f"{file}: «{nome}» esce dal bordo dell'immagine")
        for i, (n1, a) in enumerate(self.voci):
            for n2, b in self.voci[i + 1:]:
                if a[0] < b[2] + 6 and b[0] < a[2] + 6 and a[1] < b[3] + 6 and b[1] < a[3] + 6:
                    raise SystemExit(f"{file}: «{n1}» tocca «{n2}»")


def controlla_caratteri(testo: str, font: ImageFont.FreeTypeFont) -> None:
    """Un carattere senza disegno uscirebbe come uno spazio vuoto: si ferma."""
    mancanti = [c for c in dict.fromkeys(testo)
                if not c.isspace() and font.getmask(c).getbbox() is None]
    if mancanti:
        elenco = " ".join(f"«{c}» (U+{ord(c):04X})" for c in mancanti)
        raise SystemExit(f"Il carattere non disegna {elenco} in «{testo}»: scrivilo a parole")


def scrivi(d, ingombri, xy, testo, font, colore, ancora) -> None:
    controlla_caratteri(testo, font)
    ingombri.aggiungi(testo, d.textbbox(xy, testo, font=font, anchor=ancora))
    d.text(xy, testo, font=font, fill=colore, anchor=ancora)


def tratti(y: int, x0: int, x1: int) -> list[tuple[int, int, int, int]]:
    """Rettangoli di una linea tratteggiata spessa 4 pixel: 12 pieni, 10 vuoti."""
    rettangoli = []
    x = x0
    while x < x1:
        rettangoli.append((x, y - 2, min(x + 12, x1) - 1, y + 1))
        x += 22
    return rettangoli


def disegna(cfg: dict, serie: dict, x_grafico: int) -> Path:
    im = Image.new("RGB", (LARGHEZZA, ALTEZZA), FONDO)
    d = ImageDraw.Draw(im)
    ingombri = Ingombri()
    x_fine = LARGHEZZA - MARGINE_DX
    tacche = serie["tacche"]
    minimo, massimo = tacche[0], tacche[-1]

    def y_di(valore) -> float:
        quota = (float(valore) - minimo) / (massimo - minimo)
        return GRAFICO_BASSO - quota * (GRAFICO_BASSO - GRAFICO_ALTO)

    ingombri.aggiungi("area delle barre", (x_grafico, GRAFICO_ALTO, x_fine, GRAFICO_BASSO))

    # Griglia ed etichette dell'asse Y, centrate sulla loro linea.
    meta_cifre = altezza_cifre(F_ASSI) / 2
    for t in tacche:
        y = round(y_di(t))
        d.line([(x_grafico, y), (x_fine, y)], fill=GRIGLIA, width=1)
        scrivi(d, ingombri, (x_grafico - 14, round(y + meta_cifre)), numero_it(t, 0),
               F_ASSI, ETICHETTE, "rs")

    # Barre: un anno per spazio, larghe il 63% dello spazio. Il valore zero
    # resta visibile come un segno di due pixel sulla base.
    anni, valori = serie["anni"], serie["valori"]
    spazio = (x_fine - x_grafico) / len(anni)
    larghezza_barra = round(spazio * 0.63)
    barre = []
    for i, valore in enumerate(valori):
        sx = round(x_grafico + spazio * (i + 0.5) - larghezza_barra / 2)
        alto = min(round(y_di(valore)), GRAFICO_BASSO - 1)
        barre.append((sx, alto, sx + larghezza_barra - 1, GRAFICO_BASSO))
        d.rectangle(barre[-1], fill=cfg["colore"])

    # Medie dei due decenni, tratteggiate su tutta la larghezza. Dove un tratto
    # passa sopra una barra, una riga color fondo sopra e una sotto lo staccano
    # dalla barra; sul fondo non serve e la griglia resta intatta.
    linee = [(colore, tratti(round(y_di(valore)), x_grafico, x_fine))
             for valore, colore, _ in serie["medie"]]
    for _, rettangoli in linee:
        for tx0, ty0, tx1, ty1 in rettangoli:
            for bx0, by0, bx1, by1 in barre:
                bordo = (max(tx0, bx0), max(ty0 - 1, by0), min(tx1, bx1), min(ty1 + 1, by1))
                if bordo[0] <= bordo[2] and bordo[1] <= bordo[3]:
                    d.rectangle(bordo, fill=FONDO)
    for colore, rettangoli in linee:
        for rettangolo in rettangoli:
            d.rectangle(rettangolo, fill=colore)

    # Anni sotto le barre, a due cifre, uno ogni due a partire dal primo.
    base_anni = GRAFICO_BASSO + 20 + altezza_cifre(F_ASSI)
    for i, anno in enumerate(anni):
        if (anno - anni[0]) % 2 == 0:
            scrivi(d, ingombri, (round(x_grafico + spazio * (i + 0.5)), base_anni),
                   f"{anno % 100:02d}", F_ASSI, ETICHETTE, "ms")

    # Titolo e sottotitolo.
    alto_titolo = altezza_cifre(F_TITOLO)
    alto_sotto = altezza_cifre(F_SOTTOTITOLO)
    scrivi(d, ingombri, (MARGINE_SX, 46 + alto_titolo), cfg["titolo"], F_TITOLO, TITOLO, "ls")
    scrivi(d, ingombri, (MARGINE_SX, 90 + alto_sotto), serie["sottotitolo"],
           F_SOTTOTITOLO, SOTTOTITOLO, "ls")

    # Legenda in alto a destra: una riga all'altezza del titolo, una del
    # sottotitolo, allineate al bordo destro dell'area delle barre.
    righe = [46 + alto_titolo / 2, 90 + alto_sotto / 2]
    misura = max(d.textbbox((0, 0), testo, font=F_LEGENDA, anchor="ls")[2]
                 for _, _, testo in serie["medie"])
    campione = 78                            # quattro tratti come quelli delle linee
    x_legenda = x_fine - (campione + 12 + misura)
    meta_legenda = altezza_cifre(F_LEGENDA) / 2
    for centro, (_, colore, testo) in zip(righe, serie["medie"]):
        yc = round(centro)
        for rettangolo in tratti(yc, x_legenda, x_legenda + campione):
            d.rectangle(rettangolo, fill=colore)
        ingombri.aggiungi(f"campione {testo}",
                          (x_legenda, yc - 2, x_legenda + campione - 1, yc + 1))
        scrivi(d, ingombri, (x_legenda + campione + 12, round(centro + meta_legenda)), testo,
               F_LEGENDA, colore, "ls")

    scrivi(d, ingombri, (MARGINE_SX, ALTEZZA - 22), cfg["credito"], F_CREDITO, CREDITO, "ls")

    ingombri.controlla(cfg["uscita"])
    USCITA.mkdir(parents=True, exist_ok=True)
    file = USCITA / cfg["uscita"]
    # Si scrive accanto e si sostituisce solo se il peso va bene: un file oltre il
    # limite non deve restare al posto di quello pubblicato.
    tmp = file.with_suffix(".tmp.webp")
    im.save(tmp, "WEBP", **WEBP)
    if tmp.stat().st_size > PESO_MASSIMO:
        peso = tmp.stat().st_size // 1024
        tmp.unlink()
        raise SystemExit(f"{file.name}: {peso} KB, oltre i 200 KB")
    tmp.replace(file)
    return file


def main() -> None:
    serie = [carica(cfg) for cfg in GRAFICI]
    # Stessa area delle barre per i tre grafici: parte dopo l'etichetta più
    # larga dell'asse Y, così gli anni cadono allo stesso posto in tutti.
    misura = ImageDraw.Draw(Image.new("RGB", (8, 8)))
    piu_larga = max(misura.textbbox((0, 0), numero_it(t, 0), font=F_ASSI, anchor="ls")[2]
                    for s in serie for t in s["tacche"])
    x_grafico = MARGINE_SX + piu_larga + 14
    for cfg, s in zip(GRAFICI, serie):
        file = disegna(cfg, s, x_grafico)
        medie = " | ".join(testo for _, _, testo in s["medie"])
        print(f"{file.relative_to(ROOT)}: {file.stat().st_size / 1024:.1f} KB — {medie}")


if __name__ == "__main__":
    main()
