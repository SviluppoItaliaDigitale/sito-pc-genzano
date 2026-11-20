#!/usr/bin/env python3
"""Presentazioni per la classe: dai testi in data/presentazioni/*.yaml ai file
PowerPoint (testo vero, modificabile, note per il docente) e PDF, in tre formati
di schermo: 16:9, 16:10 e 4:3. Il PDF è vettoriale: resta nitido anche sui
monitor interattivi 4K, quindi non serve una versione a parte.

Uso:
  python3 scripts/genera-presentazioni-lim.py              # tutte
  python3 scripts/genera-presentazioni-lim.py nue-112      # una sola (per tema)
  python3 scripts/genera-presentazioni-lim.py --senza-pdf  # solo PowerPoint
  python3 scripts/genera-presentazioni-lim.py --png DIR    # anche le anteprime PNG

Richiede python-pptx, PyYAML, Pillow, fonttools e LibreOffice (per il PDF).
Il testo che non entra nel suo riquadro al corpo minimo ferma lo script: si
accorcia la frase nel file di dati, non si rimpicciolisce oltre.
"""
import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

import yaml
from PIL import Image, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATI = os.path.join(REPO, "data", "presentazioni")
# Presentazioni per la formazione dei volontari: stesso motore, note per
# l'istruttore, elenco in data/formazione_volontari.json invece di Risorse pronte.
DATI_VOLONTARI = os.path.join(REPO, "data", "presentazioni-volontari")
ELENCO_VOLONTARI = os.path.join(REPO, "data", "formazione_volontari.json")
OUT = os.path.join(REPO, "static", "presentazioni")
IMG = os.path.join(REPO, "static", "images")
PITTO = os.path.join(REPO, "static", "pittogrammi")
SITO = "https://www.protezionecivilegenzano.it"

# Formati: nome nel file, larghezza in pollici (l'altezza è sempre 7,5).
FORMATI = [("16x9", 13.333), ("16x10", 12.0), ("4x3", 10.0)]
ALTEZZA = 7.5

BLU = RGBColor(0x00, 0x33, 0x66)
BLU_SCURO = RGBColor(0x00, 0x24, 0x4D)
GIALLO = RGBColor(0xFF, 0xBE, 0x2E)
TESTO = RGBColor(0x1A, 0x1A, 0x1A)
GRIGIO = RGBColor(0x4A, 0x5B, 0x6B)   # 7,0:1 su bianco
MICRO = RGBColor(0xA7, 0xB4, 0xC1)    # cornice di microtesto, volutamente tenue
ROSSO = RGBColor(0xC1, 0x12, 0x1F)
BIANCO = RGBColor(0xFF, 0xFF, 0xFF)
FONDO = RGBColor(0xF4, 0xF7, 0xFB)
FONT = "Titillium Web"
ENTE = "Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma"

# --- Caratteri: Titillium Web dai woff2 del repository, così LibreOffice lo
# incorpora nel PDF e le misure del testo sono quelle vere.
FONTS_DIR = os.path.expanduser("~/.fonts")
TW_SRC = os.path.join(REPO, "static/vendor/bootstrap-italia/fonts/Titillium_Web")
TTF = {}
for peso, nome in (("regular", "TitilliumWeb-regular.ttf"), ("700", "TitilliumWeb-700.ttf"),
                   ("italic", "TitilliumWeb-italic.ttf")):
    dst = os.path.join(FONTS_DIR, nome)
    src = os.path.join(TW_SRC, "titillium-web-v10-latin-ext_latin-%s.woff2" % peso)
    if not os.path.exists(dst):
        from fontTools.ttLib import TTFont
        os.makedirs(FONTS_DIR, exist_ok=True)
        t = TTFont(src)
        t.flavor = None
        t.save(dst)
        subprocess.run(["fc-cache", "-f", FONTS_DIR], capture_output=True)
    TTF[peso] = dst


class TestoTroppoLungo(Exception):
    pass


def righe(testo, size_pt, larghezza_in, grassetto=False):
    """Divide il testo in righe che stanno nella larghezza, misurando i glifi."""
    f = ImageFont.truetype(TTF["700" if grassetto else "regular"], int(size_pt * 10))
    max_px = larghezza_in * 72 * 10  # 1 pt = 1/72 di pollice, misura a 10x
    out, cur = [], ""
    for parola in testo.split():
        prova = (cur + " " + parola).strip()
        if f.getlength(prova) <= max_px:
            cur = prova
        else:
            if cur:
                out.append(cur)
            if f.getlength(parola) > max_px:
                raise TestoTroppoLungo(parola)
            cur = parola
    if cur:
        out.append(cur)
    return out


def altezza_blocco(testi, size_pt, larghezza_in, interlinea=1.2, spazio=0.5, grassetto=False):
    n = sum(len(righe(t, size_pt, larghezza_in, grassetto)) for t in testi)
    return (n * size_pt * interlinea + max(len(testi) - 1, 0) * size_pt * spazio) / 72.0


def scegli_corpo(testi, larghezza_in, altezza_in, corpi, **kw):
    for c in corpi:
        try:
            if altezza_blocco(testi, c, larghezza_in, **kw) <= altezza_in:
                return c
        except TestoTroppoLungo:
            continue
    raise TestoTroppoLungo("%r non entra in %.2f × %.2f pollici nemmeno a %s pt"
                           % (testi, larghezza_in, altezza_in, corpi[-1]))


def lang(run):
    run._r.get_or_add_rPr().set("lang", "it-IT")


def scrivi(run, testo, size, colore, grassetto=False, corsivo=False):
    run.text = testo
    run.font.size = Pt(size)
    run.font.color.rgb = colore
    run.font.bold = grassetto
    run.font.italic = corsivo
    run.font.name = FONT
    lang(run)


def casella(s, x, y, w, h, ancora=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.vertical_anchor = ancora
    for lato in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, lato, 0)
    return tf


FORME = {}   # slide_id -> forme da disegnare nello sfondo
TONDO, OVALE = "tondo", "ovale"


def rettangolo(s, x, y, w, h, colore, forma=None, bordo=None):
    """Le forme decorative vanno nello sfondo della slide, non fra i contenuti:
    così nel PDF non diventano «figure» senza descrizione per gli screen reader."""
    FORME.setdefault(s.slide_id, []).append((forma, x, y, w, h, colore, bordo))


def paragrafi(tf, testi, size, colore, interlinea=1.2, spazio=0.5, grassetto=False, allinea=PP_ALIGN.LEFT):
    for i, t in enumerate(testi):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = allinea
        p.line_spacing = interlinea
        if i:
            p.space_before = Pt(size * spazio)
        scrivi(p.add_run(), t, size, colore, grassetto)


DPI_CORNICE = 200


def cornice_png(W, H, anno, fondo, forme=()):
    """Sfondo della slide: colore pieno, forme decorative e cornice di microtesto lungo i bordi."""
    import hashlib
    scuro = fondo == BLU
    chiave = hashlib.sha1(repr((W, H, anno, str(fondo), forme)).encode()).hexdigest()[:16]
    path = os.path.join(tempfile.gettempdir(), "pcgz-sfondo-%s.png" % chiave)
    if os.path.exists(path):
        return path
    from PIL import ImageDraw
    w, h = int(W * DPI_CORNICE), int(H * DPI_CORNICE)
    im = Image.new("RGBA", (w, h), (fondo[0], fondo[1], fondo[2], 255))
    dr = ImageDraw.Draw(im)
    for forma, x, y, fw, fh, colore, bordo in forme:
        box = [round(x * DPI_CORNICE), round(y * DPI_CORNICE),
               round((x + fw) * DPI_CORNICE) - 1, round((y + fh) * DPI_CORNICE) - 1]
        riemp = tuple(colore) + (255,)
        linea = tuple(bordo) + (255,) if bordo else None
        lw = max(2, round(0.02 * DPI_CORNICE)) if bordo else 0
        if forma == OVALE:
            dr.ellipse(box, fill=riemp, outline=linea, width=lw)
        elif forma == TONDO:
            dr.rounded_rectangle(box, radius=round(min(fw, fh) * 0.1667 * DPI_CORNICE), fill=riemp,
                                 outline=linea, width=lw)
        else:
            dr.rectangle(box, fill=riemp, outline=linea, width=lw)
    f = ImageFont.truetype(TTF["regular"], int(4.5 / 72 * DPI_CORNICE))
    col = (0x5F, 0x7E, 0x9E, 255) if scuro else (0xA7, 0xB4, 0xC1, 255)
    frase = "%s · protezionecivilegenzano.it · %s   " % (ENTE, anno)
    margine = int(0.05 * DPI_CORNICE)

    def striscia(lung):
        s = Image.new("RGBA", (lung, int(f.size * 1.4)), (0, 0, 0, 0))
        d = ImageDraw.Draw(s)
        x = 0
        while x < lung:
            d.text((x, 0), frase, font=f, fill=col)
            x += int(f.getlength(frase))
        return s

    sopra = striscia(w - 2 * margine)
    im.alpha_composite(sopra, (margine, margine))
    im.alpha_composite(sopra, (margine, h - margine - sopra.height))
    lato = striscia(h - 2 * margine - 2 * sopra.height).rotate(90, expand=True)
    im.alpha_composite(lato, (margine, margine + sopra.height))
    im.alpha_composite(lato.rotate(180), (w - margine - lato.width, margine + sopra.height))
    im.convert("RGB").save(path, optimize=True)
    return path


def sfondo(s, png):
    """Immagine di sfondo della slide (p:bg): nei PDF non è un contenuto, gli screen reader la saltano."""
    from lxml import etree
    _, rid = s.part.get_or_add_image_part(png)
    ns_p = "http://schemas.openxmlformats.org/presentationml/2006/main"
    ns_a = "http://schemas.openxmlformats.org/drawingml/2006/main"
    ns_r = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    csld = s._element.find("{%s}cSld" % ns_p)
    bg = etree.Element("{%s}bg" % ns_p)
    bgpr = etree.SubElement(bg, "{%s}bgPr" % ns_p)
    blip = etree.SubElement(bgpr, "{%s}blipFill" % ns_a, dpi="0", rotWithShape="1")
    etree.SubElement(blip, "{%s}blip" % ns_a, {"{%s}embed" % ns_r: rid})
    st = etree.SubElement(blip, "{%s}stretch" % ns_a)
    etree.SubElement(st, "{%s}fillRect" % ns_a)
    etree.SubElement(bgpr, "{%s}effectLst" % ns_a)
    csld.insert(0, bg)


def alt(pic, testo):
    pic._element.nvPicPr.cNvPr.set("descr", testo)
    return pic


class Deck:
    def __init__(self, dati, formato, larghezza):
        self.vol = dati.get("pubblico") == "volontari"
        self.d = dati
        self.fmt = formato
        self.W = larghezza
        self.H = ALTEZZA
        self.prs = Presentation()
        self.prs.slide_width = Inches(self.W)
        self.prs.slide_height = Inches(self.H)
        self.vuota = self.prs.slide_layouts[6]
        self.n = 0
        self.margine = 0.6
        self.fondi = {}

    # ---- elementi comuni
    def nuova(self, fondo=BIANCO):
        s = self.prs.slides.add_slide(self.vuota)
        self.fondi[s.slide_id] = fondo
        FORME[s.slide_id] = []
        self.n += 1
        return s

    def testata(self, s):
        rettangolo(s, 0, 0, self.W, 0.82, BLU)
        rettangolo(s, 0, 0.82, self.W, 0.05, GIALLO)
        alt(s.shapes.add_picture(os.path.join(IMG, "logo-pc-genzano.png"),
                                 Inches(self.margine - 0.1), Inches(0.14), height=Inches(0.56)),
            "Logo della Protezione Civile di Genzano di Roma")
        tf = casella(s, self.margine + 0.62, 0.17, self.W - 3.2, 0.5, MSO_ANCHOR.MIDDLE)
        p = tf.paragraphs[0]
        scrivi(p.add_run(), "Protezione Civile", 13, BIANCO, grassetto=True)
        scrivi(p.add_run(), "  ·  Gruppo Comunale Volontari — Genzano di Roma", 11, RGBColor(0xD6, 0xE2, 0xEE))
        tf = casella(s, self.W - self.margine - 1.6, 0.2, 1.6, 0.45, MSO_ANCHOR.MIDDLE)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.RIGHT
        scrivi(p.add_run(), str(self.n), 14, BIANCO, grassetto=True)

    def note(self, s, testo, fonte=None):
        tf = s.notes_slide.notes_text_frame
        tf.text = ""
        p = tf.paragraphs[0]
        scrivi(p.add_run(), ("Per l'istruttore: " if self.vol else "Per il docente: ") + testo.strip(), 12, TESTO)
        if fonte:
            p = tf.add_paragraph()
            url = fonte if fonte.startswith("http") else SITO + fonte
            scrivi(p.add_run(), "Fonte: " + url, 12, GRIGIO)

    def pittogramma(self, s, chiave, x, y, lato):
        ext = ".svg" if chiave.startswith("iso7010/") else ".png"
        path = os.path.join(PITTO, chiave + ext)
        if not os.path.exists(path):
            raise SystemExit("Pittogramma inesistente: %s" % path)
        if ext == ".svg":
            png = os.path.join(tempfile.gettempdir(), chiave.replace("/", "-") + ".png")
            if not os.path.exists(png):
                subprocess.run(["rsvg-convert", "-w", "600", "-h", "600", "-o", png, path], check=True)
            path = png
        pic = s.shapes.add_picture(path, Inches(x), Inches(y), width=Inches(lato), height=Inches(lato))
        return pic

    # ---- tipi di slide
    def copertina(self):
        d = self.d
        s = self.nuova(BLU)
        rettangolo(s, 0, self.H - 0.42, self.W, 0.42, BLU_SCURO)
        rettangolo(s, self.margine, 2.05, 0.12, 2.6, GIALLO)
        alt(s.shapes.add_picture(os.path.join(IMG, "logo-pc-genzano.png"),
                                 Inches(self.margine), Inches(0.55), height=Inches(1.05)),
            "Logo della Protezione Civile di Genzano di Roma")
        tf = casella(s, self.margine + 1.25, 0.62, self.W - 2.6, 0.9, MSO_ANCHOR.MIDDLE)
        p = tf.paragraphs[0]
        scrivi(p.add_run(), "PROTEZIONE CIVILE", 16, BIANCO, grassetto=True)
        p = tf.add_paragraph()
        scrivi(p.add_run(), "Gruppo Comunale Volontari — Genzano di Roma", 13, RGBColor(0xD6, 0xE2, 0xEE))
        w = self.W - 2 * self.margine - 0.4
        c = scegli_corpo([d["titolo"]], w, 1.9, [46, 42, 38, 34, 30], grassetto=True, interlinea=1.05)
        tf = casella(s, self.margine + 0.4, 2.0, w, 1.9, MSO_ANCHOR.BOTTOM)
        paragrafi(tf, [d["titolo"]], c, BIANCO, interlinea=1.05, grassetto=True)
        tf = casella(s, self.margine + 0.4, 4.1, w, 0.6)
        scrivi(tf.paragraphs[0].add_run(), d["sottotitolo"], 22, GIALLO)
        tf = casella(s, self.margine + 0.4, 5.2, w, 0.9)
        paragrafi(tf, ["Per chi: %s" % d["fascia"], "Durata: %s" % d["durata"]], 16,
                  RGBColor(0xE4, 0xEC, 0xF4), spazio=0.2)
        tf = casella(s, self.margine, self.H - 0.38, self.W - 2 * self.margine, 0.3, MSO_ANCHOR.MIDDLE)
        scrivi(tf.paragraphs[0].add_run(), "protezionecivilegenzano.it  ·  In emergenza chiama il 112",
               12, RGBColor(0xD6, 0xE2, 0xEE))
        if self.vol:
            self.note(s, "Presenta il modulo e i suoi obiettivi. Le note sotto ogni slide dicono che "
                         "cosa approfondire e quali domande fare al gruppo. Alla fine i volontari "
                         "possono allenarsi con il quiz formativo del sito, modalità Allenamento o "
                         "Esame. Testi aggiornati al %s." % self.data_estesa())
        else:
            self.note(s, "Presenta l'argomento e spiega che la lezione parla di azioni concrete. "
                         "Le note sotto ogni slide dicono che cosa raccontare e quali domande fare. "
                         "Testi aggiornati al %s." % self.data_estesa())

    def data_estesa(self):
        mesi = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
                "agosto", "settembre", "ottobre", "novembre", "dicembre"]
        a, m, g = self.d["aggiornato"].split("-")
        return "%d %s %s" % (int(g), mesi[int(m) - 1], a)

    def punti(self, sl):
        s = self.nuova()
        self.testata(s)
        x0 = self.margine
        con_figura = bool(sl.get("pittogramma"))
        lato = 2.7 if self.W >= 12 else 2.3
        wtesto = self.W - 2 * self.margine - (lato + 0.5 if con_figura else 0)
        c = scegli_corpo([sl["titolo"]], wtesto, 1.25, [40, 36, 32, 30], grassetto=True, interlinea=1.05)
        tf = casella(s, x0, 1.2, wtesto, 1.25, MSO_ANCHOR.BOTTOM)
        paragrafi(tf, [sl["titolo"]], c, BLU, interlinea=1.05, grassetto=True)
        rettangolo(s, x0, 2.6, 1.4, 0.07, GIALLO)
        ytesto, htesto = 2.95, self.H - 2.95 - 0.55
        wpunti = wtesto - 0.55
        c = scegli_corpo(sl["punti"], wpunti, htesto, [30, 28, 26, 24, 22], spazio=0.6)
        # Un riquadro per punto, col segno quadrato a sinistra: si legge da lontano.
        y = ytesto
        for t in sl["punti"]:
            h = altezza_blocco([t], c, wpunti)
            rettangolo(s, x0, y + c / 72 * 0.32, 0.2, 0.2, GIALLO)
            tf = casella(s, x0 + 0.5, y, wpunti, h + 0.05)
            paragrafi(tf, [t], c, TESTO)
            y += h + c * 0.6 / 72
        if con_figura:
            xf = self.W - self.margine - lato
            rettangolo(s, xf - 0.15, 1.35, lato + 0.3, lato + 0.3, FONDO, TONDO)
            pic = self.pittogramma(s, sl["pittogramma"], xf, 1.5, lato)
            alt(pic, "Pittogramma: " + sl["titolo"])
        self.note(s, sl["nota"], sl.get("fonte"))

    def domanda(self, sl):
        s = self.nuova(FONDO)
        self.testata(s)
        w = self.W - 2 * self.margine
        tf = casella(s, self.margine, 1.15, w, 0.5)
        scrivi(tf.paragraphs[0].add_run(), "DOMANDA PER IL GRUPPO" if self.vol else "DOMANDA PER LA CLASSE",
               16, ROSSO, grassetto=True)
        c = scegli_corpo([sl["domanda"]], w, 1.35, [38, 34, 30, 28], grassetto=True, interlinea=1.05)
        tf = casella(s, self.margine, 1.65, w, 1.35)
        paragrafi(tf, [sl["domanda"]], c, BLU, interlinea=1.05, grassetto=True)
        lettere = "ABCDEF"
        y = 3.25
        hbox = (self.H - y - 0.55 - 0.2 * (len(sl["punti"]) - 1)) / len(sl["punti"])
        c = min(scegli_corpo([t], w - 1.3, hbox - 0.25, [28, 26, 24, 22]) for t in sl["punti"])
        for i, t in enumerate(sl["punti"]):
            rettangolo(s, self.margine, y, w, hbox, BIANCO, TONDO, bordo=BLU)
            rettangolo(s, self.margine + 0.25, y + (hbox - 0.6) / 2, 0.6, 0.6, BLU, OVALE)
            tfc = casella(s, self.margine + 0.25, y + (hbox - 0.6) / 2, 0.6, 0.6, MSO_ANCHOR.MIDDLE)
            pc = tfc.paragraphs[0]
            pc.alignment = PP_ALIGN.CENTER
            scrivi(pc.add_run(), lettere[i], 22, BIANCO, grassetto=True)
            tf = casella(s, self.margine + 1.1, y, w - 1.3, hbox, MSO_ANCHOR.MIDDLE)
            paragrafi(tf, [t], c, TESTO)
            y += hbox + 0.2
        self.note(s, sl["nota"], sl.get("fonte"))

    def ricorda(self):
        s = self.nuova(BLU)
        tf = casella(s, self.margine, 0.6, self.W - 2 * self.margine, 0.7)
        scrivi(tf.paragraphs[0].add_run(), "Da ricordare", 40, BIANCO, grassetto=True)
        rettangolo(s, self.margine, 1.45, 1.4, 0.07, GIALLO)
        w = self.W - 2 * self.margine - 0.55
        c = scegli_corpo(self.d["ricorda"], w, 3.6, [32, 30, 28, 26, 24], spazio=0.7)
        y = 1.9
        for t in self.d["ricorda"]:
            h = altezza_blocco([t], c, w)
            rettangolo(s, self.margine, y + c / 72 * 0.32, 0.2, 0.2, GIALLO)
            tf = casella(s, self.margine + 0.5, y, w, h + 0.05)
            paragrafi(tf, [t], c, BIANCO)
            y += h + c * 0.7 / 72
        rettangolo(s, self.margine, self.H - 1.75, self.W - 2 * self.margine, 1.1, BIANCO, TONDO)
        tf = casella(s, self.margine, self.H - 1.75, self.W - 2 * self.margine, 1.1, MSO_ANCHOR.MIDDLE)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        scrivi(p.add_run(), "In emergenza chiama il ", 28, TESTO, grassetto=True)
        scrivi(p.add_run(), "112", 36, ROSSO, grassetto=True)
        self.note(s, ("Ripeti con il gruppo i punti da ricordare. Chiedi a ognuno di dirne uno con parole sue."
                      if self.vol else
                      "Ripeti insieme alla classe i punti da ricordare. Chiedi a ognuno di dirne uno con parole sue."))

    def fonti(self):
        s = self.nuova()
        self.testata(s)
        w = self.W - 2 * self.margine
        tf = casella(s, self.margine, 1.15, w, 0.7)
        scrivi(tf.paragraphs[0].add_run(), "Fonti e licenza", 34, BLU, grassetto=True)
        voci = []
        for f in self.d["fonti"]:
            url = f["url"] if f["url"].startswith("http") else SITO + f["url"]
            voci.append("%s — %s" % (f["nome"], url))
        c = scegli_corpo(voci, w - 0.4, 2.7, [18, 16, 15, 14])
        tf = casella(s, self.margine, 2.0, w, 2.8)
        paragrafi(tf, voci, c, TESTO, spazio=0.4)
        lic = ("Testi del %s, distribuiti con licenza Creative Commons BY-NC-SA 4.0: puoi usarli "
               "e adattarli per scopi non commerciali, citando la fonte. Pittogrammi ARASAAC "
               "(autore Sergio Palao, Governo di Aragona), licenza CC BY-NC-SA 4.0; segnali di "
               "sicurezza ISO 7010. Aggiornata il %s." % (ENTE, self.data_estesa()))
        c = scegli_corpo([lic], w, 1.5, [16, 15, 14, 13])
        tf = casella(s, self.margine, self.H - 2.15, w, 1.5)
        paragrafi(tf, [lic], c, GRIGIO)
        self.note(s, "Le pagine indicate qui sono quelle da cui vengono i testi: "
                     "aprile se vuoi approfondire un punto con %s." % ("il gruppo" if self.vol else "la classe"))

    def affiliazioni(self):
        s = self.nuova()
        w = self.W - 2 * self.margine
        tf = casella(s, self.margine, 0.55, w, 0.7)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        scrivi(p.add_run(), "Chi ha preparato questa lezione", 30, BLU, grassetto=True)
        alt(s.shapes.add_picture(os.path.join(IMG, "logo-pc-genzano.png"),
                                 Inches(self.W / 2 - 0.7), Inches(1.45), height=Inches(1.4)),
            "Logo della Protezione Civile di Genzano di Roma")
        tf = casella(s, self.margine, 2.95, w, 0.5)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        scrivi(p.add_run(), ENTE, 16, TESTO, grassetto=True)
        loghi = [("quality-label-esc.png", "Corpo europeo di solidarietà\nQuality Label · E10435833"),
                 ("logo-fepivol.png", "Coordinamento\nFE.PI.VOL."),
                 ("logo-snpc-volontariato.png", "Servizio Nazionale della\nProtezione Civile — Volontariato")]
        col = w / 3
        for i, (f, testo) in enumerate(loghi):
            x = self.margine + i * col
            img = Image.open(os.path.join(IMG, f))
            h = 1.3
            lw = min(h * img.width / img.height, col - 0.4)
            hh = lw * img.height / img.width
            alt(s.shapes.add_picture(os.path.join(IMG, f), Inches(x + (col - lw) / 2),
                                     Inches(3.85 + (h - hh) / 2), width=Inches(lw)),
                "Logo: " + testo.replace("\n", " "))
            tf = casella(s, x + 0.1, 5.3, col - 0.2, 0.9)
            for j, riga in enumerate(testo.split("\n")):
                p = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
                p.alignment = PP_ALIGN.CENTER
                scrivi(p.add_run(), riga, 13, TESTO if j else BLU, grassetto=not j or "E10435833" in riga)
        tf = casella(s, self.margine, self.H - 0.85, w, 0.4)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        scrivi(p.add_run(), "protezionecivilegenzano.it  ·  In emergenza chiama il 112", 14, GRIGIO)
        if self.vol:
            self.note(s, "Il Gruppo è accreditato dal Corpo europeo di solidarietà (codice E10435833) "
                         "e fa parte del Coordinamento FE.PI.VOL. Gli altri moduli e il quiz formativo "
                         "sono nella pagina «Formazione dei volontari» del sito.")
        else:
            self.note(s, "Il Gruppo è accreditato dal Corpo europeo di solidarietà (codice E10435833) "
                         "e fa parte del Coordinamento FE.PI.VOL. Per portare i volontari in classe: "
                         "pagina «Il Gruppo nella tua scuola» sul sito.")

    def costruisci(self):
        self.copertina()
        for sl in self.d["slide"]:
            (self.domanda if sl.get("tipo") == "domanda" else self.punti)(sl)
        self.ricorda()
        self.fonti()
        self.affiliazioni()
        for s in self.prs.slides:
            sfondo(s, cornice_png(self.W, self.H, self.d["aggiornato"][:4], self.fondi[s.slide_id],
                                  tuple(FORME.get(s.slide_id, ()))))
        # Lingua italiana anche negli schemi e negli stili predefiniti: il PDF la eredita da lì.
        radici = [self.prs.part._element] + [m.part._element for m in self.prs.slide_masters]
        radici += [l.part._element for m in self.prs.slide_masters for l in m.slide_layouts]
        if self.prs.notes_master is not None:
            radici.append(self.prs.notes_master.part._element)
        for s in self.prs.slides:
            radici.append(s.notes_slide.part._element)
        for radice in radici:
            for nodo in radice.iter():
                if nodo.get("lang"):
                    nodo.set("lang", "it-IT")
        cp = self.prs.core_properties
        cp.title = self.d["titolo"]
        cp.subject = self.d["sottotitolo"]
        cp.author = ENTE
        cp.last_modified_by = ENTE
        cp.keywords = ("protezione civile, volontariato, formazione, " if self.vol else "protezione civile, scuola, ") + self.d["tema"]
        cp.language = "it-IT"
        cp.comments = "Licenza CC BY-NC-SA 4.0 — " + SITO
        cp.category = "Presentazione per la formazione dei volontari" if self.vol else "Presentazione per la classe"
        return self.prs


def nome_file(dati, formato, pdf):
    base = dati["file"] + "-presentazione"
    if pdf:
        return base + "-pdf" + ("" if formato == "16x9" else "-" + formato) + ".pdf"
    return base + ("" if formato == "16x9" else "-" + formato) + ".pptx"


def in_pdf(pptx, dest):
    tmp = tempfile.mkdtemp()
    filtro = ('pdf:impress_pdf_Export:{"UseTaggedPDF":{"type":"boolean","value":"true"},'
              '"ExportNotes":{"type":"boolean","value":"false"},'
              '"EmbedStandardFonts":{"type":"boolean","value":"true"}}')
    r = subprocess.run(["soffice", "--headless", "--convert-to", filtro, "--outdir", tmp, pptx],
                       capture_output=True, text=True, timeout=240)
    out = os.path.join(tmp, os.path.basename(pptx)[:-5] + ".pdf")
    if not os.path.exists(out):
        raise SystemExit("LibreOffice non ha prodotto il PDF: %s %s" % (r.stdout, r.stderr))
    # LibreOffice dichiara la lingua della propria configurazione: si mette l'italiano.
    # Le due sigle hanno la stessa lunghezza, quindi la tabella dei riferimenti resta valida.
    dati = open(out, "rb").read().replace(b"/Lang(en-US)", b"/Lang(it-IT)").replace(b"/Lang (en-US)", b"/Lang (it-IT)")
    open(out, "wb").write(dati)
    shutil.move(out, dest)
    shutil.rmtree(tmp, ignore_errors=True)


RISORSE = os.path.join(REPO, "data", "risorse_pronte.yaml")
ETICHETTE = [
    ("16x9", True, "Schermo 16:9 — monitor interattivi e TV, anche 4K"),
    ("16x10", True, "Schermo 16:10 — alcune lavagne e i portatili"),
    ("4x3", True, "Schermo 4:3 — LIM con il proiettore"),
    ("16x9", False, "Da modificare, 16:9, con le note"),
    ("16x10", False, "Da modificare, 16:10, con le note"),
    ("4x3", False, "Da modificare, 4:3, con le note"),
]


def peso(path):
    n = os.path.getsize(path)
    return "%.1f MB" % (n / 1048576) if n >= 1048576 else "%d KB" % round(n / 1024)


def aggiorna_risorse(d, n_slide):
    """Scrive in data/risorse_pronte.yaml la voce della presentazione (una per tema)."""
    q = lambda s: "'" + s.replace("'", "''") + "'"
    voce = ["- id: %s-presentazione" % d["tema"],
            "  tema: %s" % d["tema"],
            "  tema_titolo: %s" % q(next(x["titolo"] for x in yaml.safe_load(open(RISORSE, encoding="utf-8"))["temi"]
                                      if x["slug"] == d["tema"])),
            "  tipo: presentazione",
            "  titolo: %s" % q(d["titolo"]),
            "  descrizione: %s" % q("Per un'ora di Educazione Civica: %d slide con il testo "
                                    "modificabile e, sotto ogni slide, le note per il docente."
                                    % n_slide),
            "  file_url: /presentazioni/%s" % nome_file(d, "16x9", True),
            "  dimensione: %s" % peso(os.path.join(OUT, nome_file(d, "16x9", True))),
            "  data_pubblicazione: '%s'" % d["aggiornato"],
            "  licenza: CC BY-NC-SA 4.0",
            "  formati:"]
    for fmt, pdf, et in ETICHETTE:
        nome = nome_file(d, fmt, pdf)
        voce += ["  - etichetta: %s" % q(et),
                 "    url: /presentazioni/%s" % nome,
                 "    dimensione: %s" % peso(os.path.join(OUT, nome))]
    testo = open(RISORSE, encoding="utf-8").read()
    testa, corpo = testo.split("\nmateriali:\n", 1)
    voci = re.split(r"(?m)^(?=- id: )", corpo)
    voci = [v for v in voci if not v.startswith("- id: %s-presentazione\n" % d["tema"])]
    corpo = "".join(voci).rstrip("\n") + "\n" + "\n".join(voce) + "\n"
    open(RISORSE, "w", encoding="utf-8").write(testa + "\nmateriali:\n" + corpo)
    yaml.safe_load(open(RISORSE, encoding="utf-8"))


def aggiorna_volontari(d, n_slide):
    """Scrive in data/formazione_volontari.json la voce della presentazione (una per tema).
    L'ordine delle voci è quello del campo «ordine» del file di dati."""
    import json
    elenco = {"presentazioni": []}
    if os.path.exists(ELENCO_VOLONTARI):
        elenco = json.load(open(ELENCO_VOLONTARI, encoding="utf-8"))
    voci = [v for v in elenco["presentazioni"] if v["tema"] != d["tema"]]
    formati = []
    for formato, etichetta in (("16x9", "16:9"), ("16x10", "16:10"), ("4x3", "4:3")):
        for pdf, tipo in ((True, "PDF"), (False, "PowerPoint")):
            nome = nome_file(d, formato, pdf)
            formati.append({"tipo": tipo, "formato": etichetta, "url": "/presentazioni/" + nome,
                            "dimensione": peso(os.path.join(OUT, nome))})
    voci.append({"tema": d["tema"], "ordine": d.get("ordine", 99), "corso": d.get("corso", ""),
                 "titolo": d["titolo"], "sottotitolo": d["sottotitolo"], "fascia": d["fascia"],
                 "durata": d["durata"], "slide": n_slide, "aggiornato": d["aggiornato"],
                 "formati": formati})
    voci.sort(key=lambda v: (v["ordine"], v["tema"]))
    elenco["presentazioni"] = voci
    with open(ELENCO_VOLONTARI, "w", encoding="utf-8") as f:
        json.dump(elenco, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("temi", nargs="*")
    ap.add_argument("--senza-pdf", action="store_true")
    ap.add_argument("--png", metavar="DIR")
    a = ap.parse_args()
    files = sorted(glob.glob(os.path.join(DATI, "*.yaml"))) + sorted(glob.glob(os.path.join(DATI_VOLONTARI, "*.yaml")))
    if a.temi:
        files = [f for f in files if os.path.basename(f)[:-5] in a.temi]
    if not files:
        sys.exit("Nessun file di dati trovato.")
    for f in files:
        d = yaml.safe_load(open(f, encoding="utf-8"))
        for formato, larg in FORMATI:
            prs = Deck(d, formato, larg).costruisci()
            pptx = os.path.join(OUT, nome_file(d, formato, False))
            prs.save(pptx)
            if not a.senza_pdf:
                pdf = os.path.join(OUT, nome_file(d, formato, True))
                in_pdf(pptx, pdf)
                subprocess.run(["exiftool", "-q", "-overwrite_original", "-Producer=", "-Creator=", pdf],
                               capture_output=True)
                if a.png:
                    os.makedirs(a.png, exist_ok=True)
                    subprocess.run(["pdftoppm", "-r", "50", "-png", pdf,
                                    os.path.join(a.png, "%s-%s" % (d["tema"], formato))], check=True)
            print("ok", d["tema"], formato)
        if not a.senza_pdf:
            if d.get("pubblico") == "volontari":
                aggiorna_volontari(d, len(prs.slides))
            else:
                aggiorna_risorse(d, len(prs.slides))


if __name__ == "__main__":
    main()
