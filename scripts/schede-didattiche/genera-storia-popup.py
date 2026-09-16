#!/usr/bin/env python3
"""Costruisce «Flavia, Flavio e lo zaino rosso», il libro pop-up con la storia.

Com'è fatto il libro (e perché):

- Ogni foglio A4 **orizzontale** è una doppia pagina: piegato a metà diventa
  un libretto A5. A sinistra il testo da leggere ad alta voce, a destra la
  scena da colorare. È il formato dei libri pop-up veri, e il pop-up si alza
  dal centro come in quelli veri.
- Il pop-up è **già nella pagina**: due righe nere attraversano la piega.
  Il genitore piega il foglio col disegno FUORI (così le righe restano
  visibili e la piega fa da bordo), taglia le due righe partendo dalla piega
  attraverso i due strati, ripiega col disegno DENTRO e spinge da dietro il
  pezzo fra i due tagli: la sua piega si rovescia e la scena si alza. Stesso
  gesto su tutti i dodici capitoli. È il «gradino nella piega», il meccanismo
  più vecchio e più robusto che esista: regge anche se la stampa non è al
  millimetro. Le righe di taglio sono uguali dalle due parti della piega
  (34 mm), altrimenti il pezzo resta attaccato da un lato e non si muove.
- Rilegatura: i retri bianchi si incollano fra loro solo lungo i bordi
  esterni. Colla al centro = pop-up incollato al foglio dietro, che non si
  alza più.
- Le scene sono composte con i pittogrammi ARASAAC in bianco e nero (da
  colorare) e con i segnali ISO 7010 veri (punto di raccolta, uscita di
  emergenza, pericolo generico, pericolo elettrico). I tratti nostri restano
  solo dove un'icona non esiste: la terra, le colline, le onde, il fumo, il
  vento, il diploma, i pali dei cartelli, la finestra di notte, i fornelli, la
  tapparella e le righe del pop-up. Ogni foglio porta l'attribuzione ARASAAC
  e il libro intero eredita la licenza CC BY-NC-SA 4.0.
- Il testo è HTML vero sopra il disegno: si legge con lo screen reader, si
  ingrandisce, si cerca. Il disegno ha la sua descrizione (WCAG 1.1.1).
- Le regole in fondo a ogni capitolo vengono dal quaderno delle tavole
  (`libro_popup_dati.py`), già verificate: qui non si riscrive niente.

Coordinate: tutto in millimetri su un foglio utile di 287×182 (A4 con
5 mm di margine, meno la banda delle affiliazioni in fondo e 5 mm di
respiro: l'area stampabile è 200 mm, non 210). La piega è a
x=143,5. Il pop-up occupa x 109,5–177,5 e y 92–138: 34 mm per parte.
"""

import html
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from libro_popup_dati import TAVOLE
from storia_popup_dati import CAPITOLI, RITORNELLO, SOTTOTITOLO, TITOLO

REV = "Rev. 1 · 16/09/2026"
USCITA = pathlib.Path(__file__).resolve().parents[2] / (
    "static/formazione/schede-stampabili/flavia-libro-popup/index.html")

W, H = 287, 182            # foglio utile, mm (200 - banda 13 - respiro 5)
PIEGA = 143.5              # la piega del libro
FX1, FX2, FY1, FY2 = 109.5, 177.5, 92, 138   # il pop-up (34 mm per parte, 46 mm alto)
assert abs((PIEGA - FX1) - (FX2 - PIEGA)) < 1e-9, "i tagli devono attraversare la piega uguali dai due lati"
NERO, BLU, ARANCIO, GRIGIO = "#111827", "#0284c7", "#ea580c", "#64748b"
TRATTO = 0.55              # spessore delle linee dei disegni, mm

REGOLE = {t["id"]: t for t in TAVOLE}
ARASAAC = "/pittogrammi/arasaac-bn/"     # pittogrammi in bianco e nero, da colorare (CC BY-NC-SA 4.0)
ISO = "/pittogrammi/iso7010/"            # segnali di sicurezza ISO 7010 (pubblico dominio)
CREDITI_ARASAAC = ("Pittogrammi: ARASAAC (arasaac.org), Governo di Aragona — autore Sergio Palao, "
                   "licenza CC BY-NC-SA 4.0. Questo foglio eredita la stessa licenza.")
CREDITI_ISO = " Segnali di sicurezza ISO 7010 da Wikimedia Commons (pubblico dominio)."
# la banda delle affiliazioni (Quality Label ESC + E10435833, FE.PI.VOL., SNPC) dentro il foglio,
# sulla pagina destra: la stessa immagine della ::after condivisa di scheda-print.css
BANDA = ('<img class="st-banda" src="/images/footer-print-affiliazioni.png" '
         'alt="Affiliazioni del Gruppo: Quality Label del Corpo europeo di solidarietà, codice E10435833; Coordinamento FE.PI.VOL.; Servizio Nazionale della Protezione Civile, volontariato" '
         'width="1200" height="140">')


# ------------------------------------------------------------ primitive

def _a(**kw):
    return " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items() if v is not None)


def linea(x1, y1, x2, y2, w=TRATTO, colore=NERO, tratteggio=None, cap="round"):
    return f'<line {_a(x1=x1, y1=y1, x2=x2, y2=y2, stroke=colore, stroke_width=w, stroke_dasharray=tratteggio, stroke_linecap=cap)}/>'


def perc(d, riemp="none", w=TRATTO, colore=NERO, tratteggio=None):
    return f'<path {_a(d=d, fill=riemp, stroke=colore, stroke_width=w, stroke_dasharray=tratteggio, stroke_linejoin="round", stroke_linecap="round")}/>'


def rett(x, y, w, h, r=0, riemp="none", sw=TRATTO, colore=NERO):
    return f'<rect {_a(x=x, y=y, width=w, height=h, rx=r, fill=riemp, stroke=colore, stroke_width=sw)}/>'


def cerchio(cx, cy, r, riemp="none", sw=TRATTO, colore=NERO):
    return f'<circle {_a(cx=cx, cy=cy, r=r, fill=riemp, stroke=colore, stroke_width=sw)}/>'


def ellisse(cx, cy, rx, ry, riemp="none", sw=TRATTO, colore=NERO):
    return f'<ellipse {_a(cx=cx, cy=cy, rx=rx, ry=ry, fill=riemp, stroke=colore, stroke_width=sw)}/>'


def immagine(href, x, y, w, h):
    """Un pittogramma o un segnale dentro la scena (il file viaggia anche nello ZIP offline)."""
    return f'<image href="{href}" x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet"/>'


def testo(x, y, s, dim=3, colore=NERO, ancora="middle", peso=700, larg=None):
    """larg: larghezza imposta (textLength) per le scritte chiuse in un riquadro, così
    non dipendono dal font di sistema di chi stampa (rule 09 § 15-ter, punto d)."""
    extra = {"textLength": larg, "lengthAdjust": "spacingAndGlyphs"} if larg else {}
    return (f'<text {_a(x=x, y=y, font_size=dim, fill=colore, text_anchor=ancora, font_weight=peso, **extra)}>'
            f'{html.escape(s)}</text>')


# ------------------------------------------------------------ i pittogrammi e i segnali

def pitto(nome, x, y, w, h=None):
    """Un pittogramma ARASAAC in bianco e nero (500×500, quadrato)."""
    return immagine(f"{ARASAAC}{nome}.png", x, y, w, h or w)


def segnale(nome, x, y, w, h):
    """Un segnale di sicurezza ISO 7010 (SVG vettoriale)."""
    return immagine(f"{ISO}{nome}.svg", x, y, w, h)


# ------------------------------------------------------------ i tratti nostri (solo dove non c'è un'icona)

def collina(x, y, w, h):
    return perc(f"M{x-w/2},{y} q{w*0.25},{-h*1.6} {w/2},{-h*0.3} q{w*0.25},{-h*0.8} {w/2},{h*0.3} Z", "#fff")


def vento(x, y, w=22):
    return "".join(perc(f"M{x},{y+i*4} q{w*0.35},{-3} {w*0.7},0 q{w*0.15},{1.5} {w*0.05},{-2.2}",
                        w=TRATTO*0.9) for i in range(3))


def fumo(x, y, h=30, w=10):
    """Colonna di fumo che sale da (x,y)."""
    return perc(f"M{x},{y} q{-w},{-h*0.25} {w*0.3},{-h*0.45} q{-w*1.2},{-h*0.3} {w*0.2},{-h*0.55} "
                f"q{w*0.8},{-h*0.25} {w*0.4},{-h*0.15}", w=TRATTO*1.2, tratteggio="2 1.3")


def buca(x, y, w=32, prof=14):
    """Una buca nel prato: bordo di terra e fondo in ombra."""
    return "".join([ellisse(x, y, w/2, prof*0.28, "#fff"),
                    perc(f"M{x-w/2},{y} q0,{prof} {w/2},{prof} q{w/2},0 {w/2},{-prof}", "#e5e7eb"),
                    "".join(linea(x - w*0.35 + i*w*0.14, y + prof*0.15, x - w*0.35 + i*w*0.14 + 0.8, y + prof*0.55, TRATTO*0.8) for i in range(6))])


def diploma_disegno(x, y, w=44, h=30):
    return "".join([rett(x - w/2, y - h, w, h, 1.5, "#fff", TRATTO*1.4),
                    rett(x - w/2 + 2.5, y - h + 2.5, w - 5, h - 5, 1, "#fff", TRATTO*0.7, BLU),
                    testo(x, y - h*0.62, "DIPLOMA", 4.2, BLU), testo(x, y - h*0.4, "di piccola", 2.6, NERO, peso=400),
                    testo(x, y - h*0.22, "protezione civile", 2.6, NERO, peso=400)])


def terra(y=176, x1=148, x2=283):
    return linea(x1, y, x2, y, TRATTO*1.2)


def tremore(x, y, h=12, verso=1):
    """Due archetti di vibrazione (la casa che trema)."""
    return (perc(f"M{x},{y} q{-2.5*verso},{h/2} 0,{h}", w=TRATTO*0.9)
            + perc(f"M{x-3.5*verso},{y-3} q{-4*verso},{h/2+3} 0,{h+6}", w=TRATTO*0.8))


def onde(y=176, x1=148, x2=283):
    """L'acqua che invade la strada: due file di onde."""
    return (perc(f"M{x1},{y} q10,-4 20,0 q10,4 20,0 q10,-4 20,0 q10,4 20,0 q10,-4 20,0 q10,4 20,0 q10,-4 {x2-x1-120},0", "#e5e7eb", TRATTO*1.2)
            + perc(f"M{x1},{y-6} q10,-3 20,0 q10,3 20,0", w=TRATTO*0.9))


def finestra_notte(x, y, w=46, h=40):
    """La finestra sul buio: stelle e luna."""
    return "".join([rett(x, y, w, h, 0, "#e5e7eb", TRATTO*1.1), linea(x + w/2, y, x + w/2, y + h), linea(x, y + h/2, x + w, y + h/2),
                    "".join(cerchio(x + dx, y + dy, 0.7, NERO) for dx, dy in ((6, 6), (14, 12), (30, 5), (40, 14), (10, 30), (36, 32))),
                    perc(f"M{x+36},{y+24} a5,5 0 1,0 0,10 a3.6,3.6 0 1,1 0,-10 Z", "#fff")])


def fornelli(x, y, w=26, h=38):
    """La cucina a gas, vista di fronte."""
    return rett(x, y, w, h, 1, "#fff", TRATTO*1.1) + cerchio(x + 7, y + 3.5, 1.6) + cerchio(x + w - 7, y + 3.5, 1.6)


def tapparella(x, y, w=40, h=30):
    return rett(x, y, w, h, 0, "#fff") + "".join(linea(x, y + 4 + i*4, x + w, y + 4 + i*4, TRATTO*0.8) for i in range(6))


def palo(x, y_terra, alto, larg=12):
    return linea(x, y_terra, x, y_terra - alto, TRATTO*1.4) + linea(x - larg/2, y_terra - alto + 4, x + larg/2, y_terra - alto + 4)


# ------------------------------------------------------------ il pop-up

def popup_cornice():
    """Le righe da tagliare e piegare: identiche su ogni capitolo."""
    return "".join([
        # la piega del libro
        linea(PIEGA, 4, PIEGA, H - 6, 0.5, BLU, "3 2", "butt"),
        # i due tagli
        linea(FX1, FY1, FX2, FY1, 0.7, NERO, None, "butt"),
        linea(FX1, FY2, FX2, FY2, 0.7, NERO, None, "butt"),
        # le cerniere del gradino
        linea(FX1, FY1, FX1, FY2, 0.5, ARANCIO, "0.8 1.4"),
        linea(FX2, FY1, FX2, FY2, 0.5, ARANCIO, "0.8 1.4"),
        # etichette minuscole, fuori dal disegno
        testo(FX2 + 1.5, FY1 + 1, "taglia", 2.3, GRIGIO, "start", 400),
        testo(FX2 + 1.5, FY2 + 1, "taglia", 2.3, GRIGIO, "start", 400),
        testo(PIEGA, H - 2.5, "piega qui", 2.3, BLU, "middle", 400),
    ])


# ------------------------------------------------------------ le scene
# Ogni scena restituisce (svg_interno, descrizione). Il soggetto del pop-up
# sta DENTRO il rettangolo FX1..FX2 × FY1..FY2, centrato sulla piega; il
# resto della scena sta fuori da quel rettangolo, altrimenti verrebbe tagliato.

CX = PIEGA          # centro del pop-up
BASE = FY2 - 3      # «terra» del pop-up
FL = 42             # lato del pittogramma che sta nel pop-up
FLX, FLY = CX - FL / 2, FY1 + 2     # 122,5–164,5 × 94–136: dentro il rettangolo, a cavallo della piega

# I posti della scena, sulla pagina destra e fuori dal pop-up: il cielo (sopra y=88) a
# sinistra e a destra, la terra (in piedi sulla riga a y=176) a sinistra e a destra.


def scena_zaino():
    d = [pitto("alf-z-zaino", FLX, FLY, FL),
         pitto("dis-scuola", 224, 4, 58), pitto("dis-volontari", 182, 124, 52), pitto("dis-adulto-bambino", 232, 124, 52),
         terra()]
    return "".join(d), ("Davanti alla scuola, tre volontari in divisa e due adulti con un bambino. "
                        "Il pop-up è lo zaino di emergenza.")


def scena_tavolo():
    d = [pitto("alf-t-terremoto", FLX, FLY, FL),
         pitto("dis-famiglia", 186, 122, 54), tremore(182, 134, 12, -1), tremore(244, 134, 12, 1),
         terra()]
    return "".join(d), ("La famiglia in piedi mentre la casa trema, con i segni della vibrazione ai lati. "
                        "Il pop-up è un bambino accovacciato sotto un tavolo, con la testa protetta dalle braccia.")


def scena_scuola():
    d = [linea(CX, BASE, CX, BASE - 16, TRATTO*1.4), segnale("punto-raccolta", CX - 11, BASE - 16 - 22, 22, 22),
         pitto("dis-scuola", 150, 4, 62), pitto("pop-sirena", 250, 6, 26),
         pitto("pop-fila", 182, 116, 60), pitto("dis-adulto-bambino", 238, 126, 50),
         terra()]
    return "".join(d), ("Il cortile della scuola con la sirena che suona; i bambini in fila e, accanto, gli adulti "
                        "con un bambino. Il pop-up è il cartello verde del punto di raccolta.")


def scena_temporale():
    d = [pitto("dis-auto", FLX, FLY, FL),
         pitto("dis-temporale", 150, 6, 54), pitto("oca-pioggia", 230, 10, 46),
         pitto("dis-adulto-bambino", 182, 126, 50), pitto("oca-albero", 232, 122, 54),
         terra()]
    return "".join(d), ("Nuvole con fulmine e pioggia; un albero piegato dal vento e, lontano dall'albero, gli "
                        "adulti con un bambino. Il pop-up è la macchina, il posto sicuro con i finestrini chiusi.")


def scena_vento():
    d = [pitto("oca-albero", FLX, FLY, FL),
         vento(150, 30, 26), vento(196, 20, 30), vento(240, 34, 24),
         perc("M262,60 L272,58 L270,70 L260,72 Z", "#fff"),                                  # il cartellone che vola
         pitto("pop-casa", 226, 118, 58),
         palo(186, 176, 58), segnale("pericolo-elettrico", 180, 123.5, 12, 10.5),           # il palo con il segnale (ISO 7010 W012)
         perc("M188,122 q12,22 22,54", w=TRATTO*1.1),                                        # il filo caduto
         terra()]
    return "".join(d), ("Raffiche di vento, un cartellone che vola, la casa chiusa; da un palo con il segnale di "
                        "pericolo elettrico pende un filo caduto a terra. Il pop-up è l'albero piegato dal vento.")


def scena_alluvione():
    d = [pitto("pop-scala", FLX, FLY, FL),
         pitto("oca-pioggia", 150, 6, 50), pitto("alf-f-fiume", 228, 8, 50),
         pitto("pop-casa", 228, 120, 56), onde(), pitto("dis-gommone", 180, 134, 46)]
    return "".join(d), ("Piove, il fosso è diventato un fiume e l'acqua circonda la casa; un gommone dei soccorsi. "
                        "Il pop-up è la scala che sale ai piani alti.")


def scena_incendio():
    d = [pitto("pop-fuoco", FLX, FLY, FL),
         pitto("dis-sole", 152, 8, 36), pitto("dis-elicottero", 226, 8, 50),
         fumo(206, 88, 60, 12),                                                              # la colonna di fumo, fuori dal pop-up
         pitto("dis-pompiere", 178, 128, 48), pitto("dis-famiglia", 236, 128, 48),
         perc("M266,118 l10,0 l-3,-3 m3,3 l-3,3", w=TRATTO*1.2),                             # verso casa, lontano dal fumo
         terra()]
    return "".join(d), ("Dal bosco sale una colonna di fumo; un elicottero e un pompiere con la manichetta lavorano "
                        "sull'incendio; la famiglia cammina dalla parte opposta al fumo. Il pop-up sono le fiamme.")


def scena_fumo():
    d = [pitto("pop-strisciare", FLX, FLY, FL),
         "".join(perc(f"M{150+i*18},{14+(i%2)*3} q6,-4 12,0 q6,4 12,0", w=TRATTO*1.1, tratteggio="2 1.2") for i in range(7)),
         "".join(perc(f"M{156+i*18},{24+(i%2)*3} q6,-4 12,0 q6,4 12,0", w=TRATTO, tratteggio="2 1.2") for i in range(7)),
         segnale("uscita-emergenza-sinistra", 182, 99, 15, 15),                               # l'uscita, sulla parete (ISO 7010 E001)
         pitto("alf-u-uscita", 184, 126, 50),
         fornelli(256, 138), pitto("dis-pentola", 258, 121, 18), fumo(267, 122, 16, 5),       # la pentola che fuma
         terra()]
    return "".join(d), ("Il corridoio pieno di fumo, che resta in alto vicino al soffitto; sui fornelli la pentola "
                        "fuma ancora; il cartello dell'uscita di emergenza e una persona che esce dalla porta. "
                        "Il pop-up è un bambino che avanza a carponi.")


def scena_buca():
    d = [linea(CX, BASE, CX, BASE - 18, TRATTO*1.4), segnale("pericolo-generico", CX - 12, BASE - 18 - 21, 24, 21),
         pitto("dis-sole", 152, 8, 36), collina(232, 130, 100, 28), collina(255, 118, 60, 22),
         pitto("dis-adulto-bambino", 184, 124, 52), buca(252, 166, 34, 10),
         terra(176, 148, 234), terra(176, 270, 283)]
    return "".join(d), ("Un prato ai Castelli con le colline e una buca profonda; gli adulti tengono il bambino "
                        "lontano dal bordo. Il pop-up è il triangolo giallo di pericolo piantato davanti alla buca.")


def scena_blackout():
    d = [pitto("oca-torcia", FLX, FLY, FL),
         finestra_notte(222, 14), pitto("dis-famiglia", 182, 124, 52), pitto("dis-radio", 240, 140, 36),
         terra()]
    return "".join(d), ("Una stanza al buio: dalla finestra si vedono le stelle e la luna; la famiglia è insieme, "
                        "con la radio a pile. Il pop-up è la torcia accesa.")


def scena_telefono():
    d = [pitto("dis-al-telefono", FLX, FLY, FL),
         pitto("dis-sole", 150, 4, 50), tapparella(236, 10, 40, 30),
         pitto("dis-acqua", 186, 136, 40), pitto("dis-cuore", 236, 132, 40),
         terra()]
    return "".join(d), ("Un pomeriggio caldissimo: il sole batte sulla finestra con la tapparella; una bottiglia "
                        "d'acqua con il bicchiere e un cuore. Il pop-up è un bambino che parla al telefono.")


def scena_diploma():
    d = [diploma_disegno(CX, BASE - 4, 44, 30),
         pitto("dis-sole", 152, 8, 34), pitto("dis-cuore", 240, 12, 34),
         pitto("alf-p-protezione-civile", 178, 122, 52), pitto("dis-famiglia", 233, 126, 48), pitto("alf-z-zaino", 150, 142, 28),
         terra()]
    return "".join(d), ("I volontari con il furgone, la famiglia, il sole, un cuore e lo zaino rosso vicino. "
                        "Il pop-up è il diploma di piccola protezione civile.")


SCENE = {"zaino": scena_zaino, "tavolo": scena_tavolo, "scuola": scena_scuola,
         "temporale": scena_temporale, "vento": scena_vento, "alluvione": scena_alluvione,
         "incendio": scena_incendio, "fumo": scena_fumo, "buca": scena_buca,
         "blackout": scena_blackout, "telefono": scena_telefono, "diploma": scena_diploma}


# ------------------------------------------------------------ i fogli

def _regole_capitolo(c):
    voci = []
    for tav, idx in c["regole"]:
        for i in idx:
            voci.append(REGOLE[tav]["regole"][i])
    return voci


def foglio_capitolo(n, c, totale):
    disegno, descrizione = SCENE[c["scena"]]()
    paragrafi = "".join(f"<p>{html.escape(p)}</p>" for p in c["testo"])
    regole = "".join(f"<li>{r}</li>" for r in _regole_capitolo(c))
    icona, icona_desc = c["icona"]
    crediti = CREDITI_ARASAAC + (CREDITI_ISO if ISO in disegno else "")
    return f'''
  <article class="scheda-page" id="{c["id"]}">
    <div class="st-foglio">
      <svg class="st-scena" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img"
           aria-label="{html.escape(descrizione)}" fill="none" stroke-linecap="round" stroke-linejoin="round">
        {popup_cornice()}{disegno}
      </svg>
      <img class="st-icona" src="{ARASAAC}{icona}" alt="{html.escape(icona_desc)}" width="500" height="500">
      <div class="st-testo">
        <p class="st-kicker">Capitolo {n} · {html.escape(c["stagione"])}</p>
        <h2 class="st-titolo">{html.escape(c["titolo"])}</h2>
        {paragrafi}
      </div>
      <aside class="st-regole" aria-label="Le regole di questo capitolo">
        <h3>Che cosa si fa</h3>
        <ul>{regole}</ul>
      </aside>
      <p class="st-crediti">{crediti}</p>
      <p class="st-piede"><span>protezionecivilegenzano.it</span><span>FLAVIA-POPUP · Foglio {n + 2} di {totale} · {REV}</span></p>
      {BANDA}
    </div>
  </article>'''


def foglio_copertina(totale):
    """Foglio 1, piegato col disegno FUORI: a destra la copertina, a sinistra il retro."""
    cx = PIEGA + (W - PIEGA) / 2      # centro della metà destra
    disegno = "".join([
        linea(PIEGA, 4, PIEGA, H - 6, 0.5, BLU, "3 2", "butt"),
        testo(PIEGA - 2, H - 2.5, "piega qui, con il disegno fuori", 2.3, BLU, "end", 400),
        f'<image href="/images/logo-pc-genzano.png" x="{cx - 11}" y="8" width="22" height="22"/>',
        pitto("dis-sole", PIEGA + 3, 2, 20),
        pitto("dis-lettura", 150, 134, 42), pitto("dis-famiglia", 190, 114, 62), pitto("alf-z-zaino", 254, 144, 30),
        linea(PIEGA + 8, 178, W - 8, 178, TRATTO*1.2),
    ])
    return f'''
  <article class="scheda-page" id="copertina">
    <div class="st-foglio">
      <svg class="st-scena" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" role="img"
           aria-label="Copertina: sotto il sole, una famiglia con due bambini, un bambino che legge e lo zaino rosso"
           fill="none" stroke-linecap="round" stroke-linejoin="round">{disegno}</svg>
      <div class="st-cop">
        <p class="st-cop-ente">Gruppo Comunale Volontari di Protezione Civile · Genzano di Roma</p>
        <h1 class="st-cop-titolo">{html.escape(TITOLO)}</h1>
        <p class="st-cop-sotto">{html.escape(SOTTOTITOLO)}</p>
        <p class="st-cop-eta">Una storia da leggere insieme, dai 4 anni. Il genitore taglia, il libro si alza.</p>
      </div>
      <div class="st-retro">
        <h2>Per chi legge ad alta voce</h2>
        <p>Dodici capitoli, un anno nella vita di Flavia e Flavio. In ogni capitolo succede una
        cosa che può succedere davvero — la terra che trema, il fumo, il caldo, la luce che va
        via — e i due fratelli fanno la cosa giusta. Il ritornello è sempre lo stesso:
        <strong>«{html.escape(RITORNELLO)}»</strong> Non dice di non avere paura. Dice che cosa
        fare con la paura.</p>
        <p>Le regole in fondo a ogni capitolo sono le stesse delle pagine sui rischi del nostro
        sito, che citano le fonti istituzionali. Se un'indicazione ufficiale dice altro, vale
        quella. In emergenza si chiama sempre il <strong>112</strong>.</p>
        <p class="st-retro-nota">Materiale didattico del Gruppo Comunale. <strong>Nessun
        ministero, ufficio scolastico o altro ente governativo lo ha approvato, validato o
        adottato.</strong> Testi e scene sono opera del Gruppo; le icone dei capitoli e alcuni
        oggetti sono pittogrammi ARASAAC (autore Sergio Palao, Governo di Aragona), i cartelli
        sono segnali ISO 7010. Per questo il libro si può stampare, copiare e colorare
        liberamente per usi non commerciali, citando le fonti: licenza CC BY-NC-SA 4.0.</p>
        <div class="st-112">
          <h3>La nostra telefonata al 112</h3>
          <p>Compilate insieme, così i bambini sanno che cosa dire.</p>
          <p>Mi chiamo <span class="st-riga"></span></p>
          <p>Abito a <span class="st-riga"></span> in via <span class="st-riga"></span> numero <span class="st-riga st-corta"></span></p>
          <p>Vicino a <span class="st-riga"></span></p>
        </div>
      </div>
      <p class="st-crediti">{CREDITI_ARASAAC}</p>
      <p class="st-piede"><span>protezionecivilegenzano.it</span><span>FLAVIA-POPUP · Foglio 1 di {totale} · {REV}</span></p>
      {BANDA}
    </div>
  </article>'''


def foglio_guida(totale):
    """Foglio 2: come si prepara il libro. Non si rilega.

    L'ordine è quello che funziona davvero con le forbici: prima si piega col
    disegno fuori, così le righe di taglio si vedono e la piega fa da bordo da
    cui partire; poi si ripiega col disegno dentro e si spinge da dietro."""
    # 1. piegato col disegno fuori: le righe si vedono sulla faccia esterna
    p1 = "".join([perc("M30,42 L30,4 L58,8 L58,46 Z", "#fff"), perc("M30,42 L30,4 L2,8 L2,46 Z", "#fff"),
                  linea(30, 4, 30, 42, 0.8, BLU),
                  linea(30, 18, 44, 19, 0.8), linea(30, 30, 44, 31, 0.8),       # le righe nere, dalla piega
                  linea(44, 19, 44, 31, 0.5, ARANCIO, "0.8 1.2"),
                  cerchio(46, 12, 1.2, NERO), cerchio(13, 12, 1.2, NERO),       # due segni di «disegno»: sta fuori
                  perc("M12,30 q4,-6 8,0", w=0.5), perc("M50,36 q-4,-6 -8,0", w=0.5)])
    # 2. le forbici partono dalla piega, lungo le due righe
    p2 = "".join([perc("M30,42 L30,4 L58,8 L58,46 Z", "#fff"), perc("M30,42 L30,4 L2,8 L2,46 Z", "#f8fafc"),
                  linea(30, 4, 30, 42, 0.8, BLU),
                  linea(30, 18, 44, 19, 1.1), linea(30, 30, 44, 31, 1.1),
                  linea(44, 19, 44, 31, 0.5, ARANCIO, "0.8 1.2"),
                  # le forbici: due anelli e due lame che entrano dalla piega
                  cerchio(20, 15, 2.2), cerchio(20, 21, 2.2), perc("M22,16 L36,18.5", w=0.9), perc("M22,20 L36,18.5", w=0.9),
                  perc("M8,26 l6,0 m-6,0 l1.5,-1.5 m-1.5,1.5 l1.5,1.5", w=0.4)])
    # 3. ripiegato dall'altra parte: il disegno è dentro, fuori è bianco
    p3 = "".join([perc("M30,42 L30,4 L58,8 L58,46 Z", "#f8fafc"), perc("M30,42 L30,4 L2,8 L2,46 Z", "#f8fafc"),
                  linea(30, 4, 30, 42, 0.8, BLU), perc("M14,12 q-6,10 0,20", w=0.5), perc("M14,32 l-2,-2 m2,2 l2,-2", w=0.5),
                  perc("M46,12 q6,10 0,20", w=0.5), perc("M46,32 l-2,-2 m2,2 l2,-2", w=0.5)])
    # 4. aperto a metà, un dito da dietro spinge il pezzo: diventa un gradino
    p4 = "".join([perc("M4,36 L30,30 L56,36", w=0.5, colore=GRIGIO), perc("M4,36 L4,8 L30,2 L30,30 Z", "#f8fafc"),
                  perc("M56,36 L56,8 L30,2 L30,30 Z", "#fff"), perc("M20,26 L40,26 L40,14 L20,14 Z", "#fff", 0.9),
                  perc("M30,26 L30,14", w=0.5, colore=ARANCIO, tratteggio="0.8 1.2"),
                  perc("M30,2 L30,-2", w=0.5, colore=GRIGIO),
                  perc("M36,6 l-6,6 m6,-6 l-2.2,0 m2.2,0 l0,2.2", w=0.5),                 # da dietro, verso l'interno
                  perc("M44,44 l-6,-4 m6,4 l-2.5,-0.2 m2.5,0.2 l-0.8,-2.4", w=0.5)])      # ...e la scena viene avanti
    # 5. i fogli incollati dorso a dorso solo lungo i bordi, dentro la copertina
    p5 = "".join([perc("M6,40 L6,4 L18,2 L18,38 Z", "#fff"), perc("M18,38 L18,2 L30,4 L30,40 Z", "#f8fafc"),
                  perc("M30,40 L30,4 L42,2 L42,38 Z", "#fff"), perc("M42,38 L42,2 L54,4 L54,40 Z", "#f8fafc"),
                  perc("M2,42 L2,2 L58,2 L58,42", w=0.9),
                  perc("M19.5,3.5 L19.5,36.5 M28.5,5.5 L28.5,38.5", w=0.6, colore=ARANCIO, tratteggio="1 1"),  # la colla: sui bordi
                  testo(30, 47, "copertina", 2.4, GRIGIO, "middle", 400)])
    passi = [
        ("Piega a metà, disegno fuori", "Piega il foglio sulla riga blu tenendo il disegno all'esterno: le due metà del disegno restano in vista. Premi la piega con l'unghia.", p1),
        ("Taglia le due righe dalla piega", "Foglio ancora piegato: le due righe nere partono dalla piega. Tagliale con le forbici, i due strati insieme, e fermati dove finisce la riga.", p2),
        ("Ripiega, disegno dentro", "Apri il foglio e ripiegalo dall'altra parte, con il disegno all'interno: adesso è una doppia pagina del libro. Premi di nuovo la piega.", p3),
        ("Spingi la scena da dietro", "Apri il foglio a metà. Con un dito da dietro spingi il pezzo fra i due tagli verso l'interno, finché la sua piega si rovescia e viene avanti. Chiudi e premi: riaprendo, la scena si alza.", p4),
        ("Rilega i capitoli", "Incolla i fogli retro contro retro, in ordine, con un filo di colla solo sui bordi esterni: mai al centro, dove il pop-up deve muoversi. La copertina si piega col disegno fuori e abbraccia il blocco. Oppure una cartellina, e i fogli restano sciolti.", p5),
    ]
    blocchi = "".join(
        f'<li class="st-passo"><div class="st-passo-n">{i}</div><svg viewBox="0 0 60 50" aria-hidden="true" fill="none" stroke-linecap="round" stroke-linejoin="round">{dis}</svg>'
        f'<strong>{html.escape(t)}</strong><span>{html.escape(d)}</span></li>'
        for i, (t, d, dis) in enumerate(passi, 1))
    return f'''
  <article class="scheda-page" id="guida">
    <div class="st-foglio st-guida">
      <div class="st-guida-inner">
      <div class="st-guida-testa">
        <p class="st-kicker">Prima di cominciare · questo foglio non si rilega</p>
        <h2 class="st-titolo">Come si prepara il libro</h2>
        <p>Servono le <strong>forbici</strong> e, solo per rilegare, la <strong>colla stick</strong>.
        Ogni capitolo si prepara allo stesso modo, in quattro gesti; il quinto passo si fa una volta
        sola, alla fine. I disegni sono in bianco e nero apposta: i bambini li colorano prima che
        il genitore pieghi e tagli.</p>
      </div>
      <ol class="st-passi">{blocchi}</ol>
      <div class="st-legenda">
        <span><i class="st-tr st-tr-nera"></i> riga nera: si taglia, partendo dalla piega</span>
        <span><i class="st-tr st-tr-blu"></i> riga blu: la piega del libro</span>
        <span><i class="st-tr st-tr-arancio"></i> riga arancione: qui il taglio finisce; è la cerniera del pop-up</span>
      </div>
      <p class="st-guida-nota">Per l'adulto: il pop-up regge anche se la stampa non è al millimetro,
      quindi «adatta alla pagina» va bene. Se il pezzo fatica a rovesciarsi, piegalo prima avanti e
      indietro lungo le due righe arancioni. Le forbici le usa l'adulto o, dai 7 anni, il bambino da
      seduto e sorvegliato, con la punta arrotondata. Carta normale della stampante va bene; su
      cartoncino leggero le scene stanno su meglio.</p>
      </div>
      <p class="st-piede"><span>protezionecivilegenzano.it</span><span>FLAVIA-POPUP · Foglio 2 di {totale} · {REV}</span></p>
      {BANDA}
    </div>
  </article>'''

CSS = """
    /* foglio A4 orizzontale: la .scheda-page condivisa è verticale, qui si ribalta.
       Niente classe sul wrapper: «Stampa tutto» riconosce le pagine dalla stringa esatta
       class="scheda-page" e le riscrive. Niente pagina con nome (@page storia): in Chromium
       il contenuto di una pagina con nome sparisce dal PDF (verificato il 16/09/2026, sia
       qui sia dentro il pacchetto). Da solo il libro stampa in orizzontale con la @page
       globale; dentro «Stampa tutto» (verticale) ogni foglio viene ruotato di 90 gradi. */
    .scheda-page:has(> .st-foglio) { width: 297mm; min-height: 210mm; padding: 5mm; }
    /* la banda delle affiliazioni sta dentro il foglio (così ruota con lui nel pacchetto);
       la ::after condivisa qui si spegne per non averla due volte */
    .scheda-page:has(> .st-foglio)::after { display: none; }
    .st-foglio { position: relative; width: 287mm; height: 195mm; }
    .st-banda { position: absolute; left: 159.6mm; top: 182.5mm; width: 111.4mm; height: 13mm; object-fit: contain; }
    .st-scena { position: absolute; inset: 0; width: 100%; height: 100%; }
    .st-testo { position: absolute; left: 10mm; top: 7mm; width: 94mm; }
    .st-icona { position: absolute; left: 88mm; top: 6mm; width: 16mm; height: 16mm; object-fit: contain;
      border: 0.3mm solid #cbd5e1; border-radius: 2mm; padding: 1mm; background: #fff; }
    .st-kicker, .st-titolo { padding-right: 20mm; }
    .st-crediti { position: absolute; left: 10mm; top: 172.5mm; width: 94mm; margin: 0; font-size: 6.5px;
      line-height: 1.25; color: #475569; }
    .st-kicker { font-size: 9px; font-weight: 700; letter-spacing: 0.09em; text-transform: uppercase;
      color: #ea580c; margin: 0 0 1.5mm; }
    .st-titolo { font-size: 24px; line-height: 1.1; color: var(--scheda-blu); margin: 0 0 3mm; }
    .st-testo p { font-size: 13px; line-height: 1.45; margin: 0 0 2.2mm; }
    .st-regole { position: absolute; left: 10mm; top: 141mm; width: 94mm; border: 1px solid #cbd5e1;
      border-radius: 3px; padding: 2mm 3mm; background: #fff; }
    .st-regole h3 { font-size: 9px; text-transform: uppercase; letter-spacing: 0.07em;
      color: var(--scheda-blu); margin: 0 0 1mm; }
    .st-regole ul { margin: 0 0 0 4mm; padding: 0; }
    .st-regole li { font-size: 9.5px; line-height: 1.3; margin-bottom: 0.6mm; }
    .st-piede { position: absolute; left: 10mm; right: 8mm; bottom: 13.5mm; margin: 0; display: flex;
      justify-content: space-between; font-size: 8px; color: #475569; }
    .st-piede span:first-child { font-weight: 700; color: var(--scheda-blu); }

    /* copertina (metà destra) e retro (metà sinistra) */
    .st-cop { position: absolute; left: 152mm; top: 32mm; width: 127mm; text-align: center; }
    .st-cop-ente { font-size: 9px; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;
      color: #ea580c; margin: 0 0 3mm; }
    .st-cop-titolo { font-size: 31px; line-height: 1.08; color: var(--scheda-blu); margin: 0 0 3mm; }
    .st-cop-sotto { display: inline-block; background: var(--scheda-blu); color: #fff; font-size: 11px;
      font-weight: 700; padding: 1.2mm 4mm; border-radius: 12px; margin: 0 0 3mm; }
    .st-cop-eta { font-size: 11px; margin: 0; }
    .st-retro { position: absolute; left: 10mm; top: 8mm; width: 122mm; }
    .st-retro h2 { font-size: 15px; color: var(--scheda-blu); margin: 0 0 2mm; }
    .st-retro p { font-size: 10.5px; line-height: 1.45; margin: 0 0 2mm; }
    .st-retro-nota { background: #fff7ed; border-left: 3px solid #ea580c; padding: 1.5mm 2.5mm; }
    .st-112 { border: 2px solid var(--scheda-blu); border-radius: 4px; padding: 2.5mm 3mm; margin-top: 3mm; }
    .st-112 h3 { font-size: 12px; color: var(--scheda-blu); margin: 0 0 1mm; }
    .st-112 p { font-size: 11px; margin: 0 0 2.2mm; }
    .st-riga { display: inline-block; width: 46mm; border-bottom: 1px solid #1a1a1a; height: 5mm;
      vertical-align: bottom; }
    .st-riga.st-corta { width: 14mm; }

    /* guida — il contenuto sta in un contenitore posizionato in assoluto, come nei capitoli:
       con la pagina con nome (@page storia) Chromium perde nel PDF il contenuto in flusso normale
       del foglio, mentre quello posizionato in assoluto resta (verificato il 16/09/2026). */
    .st-guida-inner { position: absolute; left: 10mm; top: 7mm; width: 267mm; }
    .st-guida-testa p { font-size: 12px; line-height: 1.45; margin: 0; max-width: 200mm; }
    .st-passi { list-style: none; display: flex; gap: 4mm; margin: 5mm 0 0; padding: 0; }
    /* .st-passo è un blocco, non un contenitore flessibile: dentro una pagina con nome (@page storia)
       Chromium perde nel PDF il contenuto di un <li> flessibile — verificato il 16/09/2026. */
    .st-passo { flex: 1; border: 1px solid #cbd5e1; border-radius: 3px; padding: 3mm; display: block; text-align: center; }
    .st-passo-n { width: 7mm; height: 7mm; border-radius: 50%; background: var(--scheda-blu); color: #fff;
      font-weight: 800; font-size: 12px; line-height: 7mm; margin: 0 auto 1.5mm; }
    .st-passo svg { display: block; width: 42mm; height: 35mm; margin: 0 auto; }
    .st-passo strong { display: block; font-size: 11px; color: var(--scheda-blu); margin: 1.5mm 0 1mm; }
    .st-passo span { font-size: 9.5px; line-height: 1.35; }
    .st-legenda { display: flex; gap: 6mm; flex-wrap: wrap; margin-top: 4mm; font-size: 10px; }
    .st-tr { display: inline-block; width: 12mm; height: 0; vertical-align: middle; margin-right: 1.5mm; }
    .st-tr-nera { border-top: 2px solid #111827; }
    .st-tr-blu { border-top: 2px dashed #0284c7; }
    .st-tr-arancio { border-top: 2px dotted #ea580c; }
    .st-guida-nota { font-size: 9.5px; line-height: 1.4; margin: 3mm 0 0; max-width: 240mm; }
    .st-guida .st-piede { left: 0; right: 0; }

    .st-indice { margin: 0 0 1rem; }
    .st-indice a { display: inline-block; padding: 0.2rem 0.55rem; margin: 0.12rem; border: 1.5px solid var(--scheda-blu);
      border-radius: 5px; color: var(--scheda-blu); text-decoration: none; font-size: 0.85rem; }
    .st-indice a:hover, .st-indice a:focus { background: var(--scheda-blu); color: #fff; outline: 2px solid #ffbe2e; outline-offset: 2px; }

    /* banda affiliazioni (::after condivisa) centrata sulla pagina DESTRA del libro,
       non sulla piega: a schermo è alta 14 mm (immagine 120 mm), in stampa 13 mm (111 mm) */
    @media print {
      @page { size: A4 landscape; margin: 5mm; }
      /* la .scheda-page condivisa mette min-height:auto ma qui la specificità è maggiore: va ripetuto */
      .scheda-page:has(> .st-foglio) { width: 287mm; min-height: auto; padding: 0; margin: 0; }
      /* dentro «Stampa tutto» la pagina resta verticale (il pacchetto impone la sua @page dopo
         gli stili delle schede): il foglio 287×195 ruotato di 90 gradi entra nei 200×287 utili */
      .pacchetto-scheda .scheda-page:has(> .st-foglio) { width: 200mm; height: 287mm; overflow: hidden; }
      .pacchetto-scheda .scheda-page:has(> .st-foglio) > .st-foglio { transform: translateX(195mm) rotate(90deg); transform-origin: 0 0; }
    }
    @media screen and (max-width: 300mm) {
      /* a schermo stretto il foglio si scala tutto insieme, testo compreso: è un'anteprima */
      .scheda-page:has(> .st-foglio) { width: 100%; min-height: 0; padding: 2mm; overflow-x: auto; }
    }
"""


def main():
    totale = len(CAPITOLI) + 2
    fogli = [foglio_copertina(totale), foglio_guida(totale)]
    fogli += [foglio_capitolo(n, c, totale) for n, c in enumerate(CAPITOLI, 1)]
    indice = " ".join([f'<a href="#copertina">Copertina</a>', f'<a href="#guida">Come si prepara</a>']
                      + [f'<a href="#{c["id"]}">{n}. {html.escape(c["titolo"])}</a>' for n, c in enumerate(CAPITOLI, 1)])
    pagina = f'''<!DOCTYPE html>
<html lang="it" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Libro pop-up con storia: {html.escape(TITOLO)} — dodici capitoli da leggere e far saltare su</title>
  <meta name="description" content="Un libro pop-up già pronto, con una storia: {html.escape(TITOLO)}. Dodici capitoli, un anno di piccole emergenze — terremoto, temporale, vento, alluvione, incendio, fumo, caldo, blackout, gas nei posti chiusi, evacuazione a scuola, la telefonata al 112. Il genitore taglia due righe e la scena si alza dal centro del libro. Da leggere insieme dai 4 anni.">
  <meta name="robots" content="index, follow">
  <!-- URL preferito: la copia su GitHub Pages rimanda alla produzione. -->
  <link rel="canonical" href="https://www.protezionecivilegenzano.it/formazione/schede-stampabili/flavia-libro-popup/">
  <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
  <link rel="stylesheet" href="/formazione/schede-stampabili/assets/scheda-print.css">
  <style>{CSS}</style>
</head>
<body>
  <div class="scheda-toolbar no-print">
    <a href="/formazione/schede-stampabili/" aria-label="Torna alle schede">&larr; Torna alle schede</a>
    <span class="scheda-titolo">{html.escape(TITOLO)}</span>
    <button type="button" onclick="window.print()">&#128424;&#65039; Stampa o salva come PDF</button>
  </div>
  <div class="no-print" style="max-width:297mm;margin:1.5rem auto 0;padding:0 1rem;">
    <p style="margin:0 0 0.8rem;"><strong>{totale} fogli A4 orizzontali</strong>: la copertina, le
    istruzioni e dodici capitoli. Ogni foglio si piega a metà e diventa una doppia pagina del
    libro; il pop-up è già disegnato: il genitore piega, taglia due righe dalla piega e spinge la
    scena da dietro. Stampa in
    <strong>orizzontale</strong>, una sola facciata: il retro bianco serve per rilegare.</p>
    <nav class="st-indice" aria-label="Vai al foglio">{indice}</nav>
  </div>
{"".join(fogli)}
</body>
</html>
'''
    USCITA.parent.mkdir(parents=True, exist_ok=True)
    USCITA.write_text(pagina, encoding="utf-8")
    print(f"Scritto {USCITA.relative_to(USCITA.parents[4])} — {totale} fogli ({len(CAPITOLI)} capitoli)")


if __name__ == "__main__":
    main()
