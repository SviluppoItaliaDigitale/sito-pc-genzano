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

Da riga di comando (dal 22/10/2026) mette la cornice anche a una grafica fatta
in altro modo (Canva, Express, un altro programma), come gli strumenti degli
altri enti (regola grafica.md, § «Nome dell'ente e cornice di microtesto»):

  python3 scripts/microtesto_cornice.py GRAFICA.png [ALTRA.jpg ...]
  python3 scripts/microtesto_cornice.py --prova

Scrive GRAFICA-cornice.png, o GRAFICA-cornice.jpg in JPEG qualità 88, accanto
all'originale, che resta com'è, e non sovrascrive un file che esiste già. Una
grafica che ha già una cornice (il segno «cornice di microtesto» nel file, che
scrivono questo script e gli strumenti degli altri enti) resta com'è: due
cornici una sopra l'altra non si leggono più. Il carattere è di 8 px su una
grafica larga 1080 px e cresce in proporzione. La firma del Gruppo (la fascia
blu con il logo, o il nome scritto per esteso) deve esserci già: lo script la
ricorda e non la aggiunge. Si ferma se i bordi sono trasparenti, perché lì la
cornice non si vedrebbe. Il file nuovo non porta i metadati dell'originale
(EXIF, XMP, testi come il nome del programma che l'ha fatta): resta solo il
profilo colore. Una grafica in CMYK esce in RGB, con il suo profilo quando c'è.
Esce con 1 se una grafica non si è potuta fare.
"""

from __future__ import annotations

import argparse
import datetime
import io
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageOps, PngImagePlugin

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


# ---------------------------------------------------------------------------
# Da riga di comando: la cornice su una grafica fatta in altro modo (22/10/2026)
# ---------------------------------------------------------------------------

SEGNO = "Protezione Civile Genzano di Roma - cornice di microtesto - www.protezionecivilegenzano.it"
# Basta questo pezzo per riconoscere anche la cornice degli altri enti
# (Misericordia di Ariccia, Cooprimavera, ARI Castelli Romani, AGESCI Genzano 2).
SEGNO_COMUNE = b"cornice di microtesto"
QUALITA_JPEG = 88
PROMEMORIA_FIRMA = ("controlla che la grafica porti la firma del Gruppo: la fascia blu con il logo "
                    "(scripts/applica-fascia-foto.sh, sulle foto) o il nome «Protezione Civile — "
                    "Gruppo Comunale Volontari di Genzano di Roma» ben leggibile")


def corpo_per(larghezza: int) -> int:
    """8 px su una grafica larga 1080 px, in proporzione sulle altre, mai sotto i 7."""
    return max(7, round(8 * larghezza / 1080))


def ha_cornice(dati: bytes) -> bool:
    """Vero se il file porta il segno di una cornice di microtesto."""
    return SEGNO_COMUNE in dati


def destinazione(f: Path) -> Path:
    return f.with_name(f"{f.stem}-cornice{f.suffix}")


def cornice_su_file(f: Path) -> int:
    """Una grafica: 0 se è fatta (o lo era già), 1 se c'è un problema, e allora non scrive nulla."""
    if f.suffix.lower() not in (".jpg", ".jpeg", ".png") or not f.is_file():
        print(f"PROBLEMI in {f}: serve un file JPEG o PNG esistente")
        return 1
    dati = f.read_bytes()
    png, jpeg = dati[:8] == b"\x89PNG\r\n\x1a\n", dati[:2] == b"\xff\xd8"
    if png != (f.suffix.lower() == ".png") or not (png or jpeg):
        atteso = "PNG" if f.suffix.lower() == ".png" else "JPEG"
        print(f"PROBLEMI in {f}: il contenuto non è un {atteso} come dice il nome")
        return 1
    if ha_cornice(dati):
        print(f"già fatta: {f} (ha già la cornice; per cambiarla si riparte dalla grafica originale)")
        return 0
    dest = destinazione(f)
    if dest.exists():
        print(f"PROBLEMI in {f}: {dest.name} esiste già e non lo sovrascrivo (spostalo o cancellalo, se vuoi rifarlo)")
        return 1
    try:
        img = Image.open(io.BytesIO(dati))
        img = ImageOps.exif_transpose(img)   # una foto girata dal telefono resta dritta senza i dati EXIF
    except Exception as e:  # file rovinato o formato non letto da Pillow
        print(f"PROBLEMI in {f}: non si apre ({e})")
        return 1
    originale, profilo, nota = img.mode, img.info.get("icc_profile"), ""
    if originale not in ("1", "L", "LA", "P", "PA", "RGB", "RGBA", "CMYK"):
        print(f"PROBLEMI in {f}: colori in un formato che lo script non tratta ({originale}): "
              "esporta la grafica in RGB a 8 bit")
        return 1
    if originale == "CMYK":
        try:   # col profilo della grafica i colori restano quelli voluti
            from PIL import ImageCms   # qui e non in testa: le cover e le immagini social non ne hanno bisogno
            img = ImageCms.profileToProfile(img, ImageCms.ImageCmsProfile(io.BytesIO(profilo)),
                                            ImageCms.createProfile("sRGB"), outputMode="RGB")
        except Exception:   # senza profilo, con un profilo illeggibile o senza ImageCms: conversione semplice
            img = img.convert("RGB")
        profilo, nota = None, " (era in CMYK, ora è in RGB: controlla i colori)"
    elif png and (originale in ("LA", "PA", "RGBA") or "transparency" in img.info):
        img = img.convert("RGBA")   # anche la trasparenza «a colore chiave» di un PNG RGB o in grigi
    elif originale not in ("L", "RGB"):
        img = img.convert("RGB")
    if profilo and originale in ("1", "L", "LA") and img.mode != "L":
        profilo = None   # un profilo dei grigi non vale per i colori
    larghezza, altezza = img.size
    corpo = corpo_per(larghezza)
    if min(larghezza, altezza) < 4 * (corpo + 4):
        print(f"PROBLEMI in {f}: la grafica è troppo piccola ({larghezza}×{altezza} px) per la cornice")
        return 1
    if img.mode == "RGBA":
        s = corpo + 4
        alfa = img.getchannel("A")
        strisce = [alfa.crop(b) for b in ((0, 0, larghezza, s), (0, altezza - s, larghezza, altezza),
                                          (0, s, s, altezza - s), (larghezza - s, s, larghezza, altezza - s))]
        trasparenti = sum(sum(x.point(lambda v: 1 if v < 250 else 0).histogram()[1:2]) for x in strisce)
        totale = sum(x.width * x.height for x in strisce)
        if trasparenti > totale * 0.005:
            print(f"PROBLEMI in {f}: i bordi sono trasparenti e la cornice lì non si vedrebbe: "
                  "esporta la grafica con lo sfondo pieno")
            return 1
    nuova = cornice_microtesto(img, corpo=corpo)
    nuova.info = {}   # nessun metadato dell'originale nel file nuovo, se non il profilo colore
    uscita = io.BytesIO()
    if png:
        info = PngImagePlugin.PngInfo()
        info.add_text("Comment", SEGNO)
        nuova.save(uscita, "PNG", pnginfo=info, icc_profile=profilo, optimize=True)
    else:
        nuova.save(uscita, "JPEG", quality=QUALITA_JPEG, comment=SEGNO.encode("utf-8"),
                   icc_profile=profilo, optimize=True)
    try:
        with open(dest, "xb") as fd:   # «x»: se nel frattempo il file è comparso, non lo sovrascrive
            fd.write(uscita.getvalue())
    except FileExistsError:
        print(f"PROBLEMI in {f}: {dest.name} è comparso nel frattempo e non lo sovrascrivo")
        return 1
    print(f"ok: {dest} ({larghezza}×{altezza} px, cornice in corpo {corpo} px){nota}")
    print(f"  {PROMEMORIA_FIRMA}")
    return 0


def prova() -> int:
    """Prove su grafiche costruite apposta, in una cartella temporanea."""
    from PIL import ImageCms
    falliti: list[str] = []

    def attesa(condizione, messaggio):
        if not condizione:
            falliti.append(messaggio)

    with tempfile.TemporaryDirectory() as cartella:
        t = Path(cartella)
        # 1. PNG 1080×1350, fondo blu con un riquadro bianco: cornice sui quattro lati, niente altro cambia
        buono = t / "grafica.png"
        im = Image.new("RGB", (1080, 1350), (0, 51, 102))
        ImageDraw.Draw(im).rectangle((200, 250, 880, 900), fill=(255, 255, 255))
        im.save(buono)
        prima = buono.read_bytes()
        attesa(cornice_su_file(buono) == 0, "PNG: rifiutato")
        uscita = destinazione(buono)
        attesa(uscita.is_file(), "PNG: manca grafica-cornice.png")
        attesa(buono.read_bytes() == prima, "PNG: l'originale è cambiato")
        if uscita.is_file():
            nuovi = uscita.read_bytes()
            attesa(nuovi.startswith(b"\x89PNG") and ha_cornice(nuovi), "PNG: formato o segno sbagliati")
            vecchia, nuova = Image.open(buono).convert("RGB"), Image.open(uscita).convert("RGB")
            attesa(nuova.size == vecchia.size, "PNG: misure cambiate")
            diff = ImageChops.difference(vecchia, nuova).convert("L")
            s, (W, H) = corpo_per(1080) + 4, diff.size
            for lato, scatola in (("alto", (s, 0, W - s, s)), ("basso", (s, H - s, W - s, H)),
                                  ("sinistra", (0, s, s, H - s)), ("destra", (W - s, s, W, H - s))):
                attesa(diff.crop(scatola).getbbox() is not None, f"PNG: manca la cornice sul lato {lato}")
            attesa(diff.crop((s, s, W - s, H - s)).getbbox() is None, "PNG: la grafica è cambiata fuori dai bordi")
            # 2. mai sovrascrivere il file nuovo
            attesa(cornice_su_file(buono) == 1 and uscita.read_bytes() == nuovi, "file nuovo sovrascritto")
            # 3. mai due cornici
            attesa(cornice_su_file(uscita) == 0 and not destinazione(uscita).exists(),
                   "cornice rifatta su una grafica che l'ha già")
        # 4. JPEG largo 2160 px: corpo 16, segno nel commento, misure uguali
        grande = t / "grande.jpg"
        Image.new("RGB", (2160, 2700), (255, 255, 255)).save(grande, quality=92)
        attesa(cornice_su_file(grande) == 0, "JPEG: rifiutato")
        if destinazione(grande).is_file():
            nuovi = destinazione(grande).read_bytes()
            attesa(nuovi.startswith(b"\xff\xd8") and ha_cornice(nuovi), "JPEG: formato o segno sbagliati")
            nuova = Image.open(destinazione(grande)).convert("L")
            attesa(nuova.size == (2160, 2700), "JPEG: misure cambiate")
            striscia = nuova.crop((corpo_per(2160) + 4, 0, 2160 - corpo_per(2160) - 4, corpo_per(2160) + 4))
            attesa(striscia.getextrema()[0] < 235, "JPEG: la cornice in alto non si vede ingrandendo")
            attesa(nuova.crop((300, 300, 1800, 2400)).getextrema()[0] > 245, "JPEG: segni fuori dai bordi")
        # 5. bordi trasparenti: la cornice non si vedrebbe, quindi si ferma; con i bordi pieni
        #    e un buco trasparente al centro la fa e la trasparenza resta
        trasp = t / "trasparente.png"
        im = Image.new("RGBA", (1080, 1080), (0, 0, 0, 0))
        ImageDraw.Draw(im).ellipse((100, 100, 980, 980), fill=(0, 51, 102, 255))
        im.save(trasp)
        attesa(cornice_su_file(trasp) == 1 and not destinazione(trasp).exists(), "bordi trasparenti accettati")
        buco = t / "buco.png"
        im = Image.new("RGBA", (1080, 1080), (0, 51, 102, 255))
        ImageDraw.Draw(im).ellipse((300, 300, 780, 780), fill=(0, 0, 0, 0))
        im.save(buco)
        attesa(cornice_su_file(buco) == 0, "PNG con un buco trasparente al centro: rifiutato")
        if destinazione(buco).is_file():
            n = Image.open(destinazione(buco))
            attesa(n.mode == "RGBA" and n.getchannel("A").getextrema()[0] == 0, "PNG con un buco: trasparenza persa")
        # 6. un PNG che si chiama .jpg: si ferma e non scrive nulla
        finto = t / "finto.jpg"
        finto.write_bytes(prima)
        attesa(cornice_su_file(finto) == 1 and not destinazione(finto).exists(), "accettato un PNG chiamato .jpg")
        # 7. la cornice di un altro ente: resta com'è
        altro = t / "altro-ente.jpg"
        Image.new("RGB", (1080, 1350), (240, 240, 240)).save(
            altro, comment=b"Cooprimavera Soc. Coop. - cornice di microtesto - www.cooprimavera.com")
        attesa(cornice_su_file(altro) == 0 and not destinazione(altro).exists(),
               "cornice aggiunta sopra quella di un altro ente")
        # 8. PNG a tavolozza: esce a colori pieni, non ridotto a pochi colori
        tav = t / "tavolozza.png"
        im = Image.new("RGB", (1080, 1350), (0, 51, 102))
        ImageDraw.Draw(im).rectangle((300, 300, 780, 1050), fill=(255, 190, 46))
        im.convert("P", palette=Image.Palette.ADAPTIVE, colors=8).save(tav)
        attesa(cornice_su_file(tav) == 0, "PNG a tavolozza: rifiutato")
        if destinazione(tav).is_file():
            attesa(Image.open(destinazione(tav)).mode == "RGB", "PNG a tavolozza: non è uscito a colori pieni")
        # 9. troppo piccola per la cornice
        mini = t / "mini.png"
        Image.new("RGB", (40, 40), (0, 51, 102)).save(mini)
        attesa(cornice_su_file(mini) == 1 and not destinazione(mini).exists(), "accettata una grafica di 40 px")
        # 10. PNG RGB con la trasparenza «a colore chiave» proprio sul colore dei bordi: si ferma
        chiave = t / "chiave.png"
        Image.new("RGB", (1080, 1350), (0, 51, 102)).save(chiave, transparency=(0, 51, 102))
        attesa(cornice_su_file(chiave) == 1 and not destinazione(chiave).exists(),
               "accettati bordi trasparenti a colore chiave")
        # 11. JPEG in CMYK: esce in RGB
        cmyk = t / "cmyk.jpg"
        Image.new("CMYK", (1080, 1350), (100, 60, 0, 40)).save(cmyk, quality=90)
        attesa(cornice_su_file(cmyk) == 0, "JPEG in CMYK: rifiutato")
        if destinazione(cmyk).is_file():
            attesa(Image.open(destinazione(cmyk)).mode == "RGB", "JPEG in CMYK: non è uscito in RGB")
        # 12. nessun metadato dell'originale (EXIF, XMP, testi con il nome del programma), profilo colore sì
        srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()
        xmp = ('<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/'
               '22-rdf-syntax-ns#"><rdf:Description xmlns:xmp="http://ns.adobe.com/xap/1.0/" '
               'xmp:CreatorTool="ProgrammaDiGrafica 3.0"/></rdf:RDF></x:xmpmeta>')
        exif = Image.Exif()
        exif[0x0131] = "ProgrammaDiGrafica 3.0"   # Software
        meta_j, meta_p = t / "metadati.jpg", t / "metadati.png"
        im = Image.new("RGB", (1080, 1350), (0, 51, 102))
        im.save(meta_j, quality=90, exif=exif.tobytes(), xmp=xmp.encode(), icc_profile=srgb)
        testi = PngImagePlugin.PngInfo()
        testi.add_text("Software", "ProgrammaDiGrafica 3.0")
        testi.add_itxt("XML:com.adobe.xmp", xmp)
        im.save(meta_p, pnginfo=testi, exif=exif.tobytes(), icc_profile=srgb)
        for meta in (meta_j, meta_p):
            attesa(cornice_su_file(meta) == 0, f"{meta.name}: rifiutato")
            if destinazione(meta).is_file():
                dati = destinazione(meta).read_bytes()
                attesa(b"ProgrammaDiGrafica" not in dati, f"{meta.name}: metadati dell'originale nel file nuovo")
                attesa(Image.open(destinazione(meta)).info.get("icc_profile") == srgb,
                       f"{meta.name}: profilo colore perso")

    if falliti:
        print("\nPROVA FALLITA:")
        for x in falliti:
            print("  -", x)
        return 1
    print("\nProva superata: PNG e JPEG, quattro lati, originale intatto, niente sovrascritture né doppie "
          "cornici, bordi trasparenti anche a colore chiave, trasparenza al centro, tavolozza, CMYK, "
          "file con il nome sbagliato, grafica troppo piccola, nessun metadato dell'originale.")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Cornice di microtesto del Gruppo su una grafica fatta in altro modo (JPEG o PNG).")
    ap.add_argument("file", nargs="*", type=Path, help="grafiche JPEG o PNG")
    ap.add_argument("--prova", action="store_true", help="prova lo strumento su grafiche costruite apposta")
    a = ap.parse_args(argv)
    if a.prova:
        return prova()
    if not a.file:
        ap.error("indica almeno una grafica, oppure --prova")
    return 1 if sum(cornice_su_file(f) for f in a.file) else 0


if __name__ == "__main__":
    sys.exit(main())
