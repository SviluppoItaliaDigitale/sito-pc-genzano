#!/usr/bin/env python3
"""Illustrazioni schematiche degli esperimenti (SVG disegnati qui, non immagini).

Perché disegnate e non prese da una libreria: i pittogrammi che abbiamo
(ARASAAC, ISO 7010) sono simboli generici — «acqua», «terremoto» — e su una
scheda di esperimento sarebbero decorazione, mentre la regola dice che il
pittogramma è supporto alla comprensione, mai decorazione continua (rule 03).
Quello che serve a un bambino e a un docente è un'altra cosa: **com'è fatto il
montaggio**. Un disegno nostro può mostrare la bottiglia tagliata, il filtro,
la bacinella con la sabbia; un simbolo no.

Scelte tecniche, tutte al servizio della stampa:

- **SVG e non bitmap**: queste schede si stampano. Un vettore resta nitido a
  qualunque risoluzione, pesa poche centinaia di byte e non sgrana.
- **Leggibili in bianco e nero**: le scuole stampano quasi sempre in
  monocromia. Le differenze passano da forme e tratti, mai dal solo colore
  (stesso principio della regola «non affidarsi al solo colore»).
- **Nessuna licenza di terzi**: sono opera nostra, quindi le schede non
  ereditano vincoli oltre a quelli che hanno già.
- **Accessibilità**: ogni figura è `role="img"` con una descrizione testuale
  equivalente (WCAG 1.1.1). È contenuto, non decorazione.

Le scene sono indicizzate per **titolo esatto** dell'esperimento: un titolo
senza illustrazione semplicemente non ne riceve una, senza rompere nulla.
"""

import math

BLU = "#003366"       # tratto istituzionale
ACQUA = "#cfe3f5"     # azzurro chiaro -> grigio chiaro in monocromia
TERRA = "#e6dcc6"     # sabbia/terra
CALDO = "#c2410c"     # arancione bruciato: moto, calore, fiamma
GRIGIO = "#9aa5b1"

VIEWBOX = "0 0 160 120"


# ---------------------------------------------------------------- primitive

def _a(**kw):
    """Attributi SVG: gli underscore diventano trattini (stroke_width -> stroke-width)."""
    return " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items() if v is not None)


def linea(x1, y1, x2, y2, w=2, colore=BLU, tratteggio=None):
    return f'<line {_a(x1=x1, y1=y1, x2=x2, y2=y2, stroke=colore, stroke_width=w, stroke_dasharray=tratteggio)}/>'


def rett(x, y, w, h, r=0, riemp="none", colore=BLU, sw=2, opac=None):
    return f'<rect {_a(x=x, y=y, width=w, height=h, rx=r, fill=riemp, fill_opacity=opac, stroke=colore, stroke_width=sw)}/>'


def cerchio(cx, cy, r, riemp="none", colore=BLU, sw=2):
    return f'<circle {_a(cx=cx, cy=cy, r=r, fill=riemp, stroke=colore, stroke_width=sw)}/>'


def perc(d, riemp="none", colore=BLU, sw=2, tratteggio=None):
    return f'<path {_a(d=d, fill=riemp, stroke=colore, stroke_width=sw, stroke_dasharray=tratteggio)}/>'


def testo(x, y, s, dim=9, colore=BLU, ancora="middle", peso=700):
    return (f'<text {_a(x=x, y=y, font_size=dim, fill=colore, text_anchor=ancora, font_weight=peso)}>'
            f'{s}</text>')


def freccia(x1, y1, x2, y2, colore=CALDO, w=2):
    """Freccia diritta con punta piena."""
    ang = math.atan2(y2 - y1, x2 - x1)
    L, A = 6, 0.45
    p1 = (x2 - L * math.cos(ang - A), y2 - L * math.sin(ang - A))
    p2 = (x2 - L * math.cos(ang + A), y2 - L * math.sin(ang + A))
    return (linea(x1, y1, x2, y2, w, colore) +
            f'<path {_a(d=f"M{x2:.1f},{y2:.1f} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} Z", fill=colore)}/>')


def bicchiere(x, y, w, h, livello=0, liquido=ACQUA, svaso=3):
    """Bicchiere leggermente svasato; `livello` = altezza del liquido dal fondo."""
    out = []
    if livello > 0:
        ly = y + h - livello
        k = svaso * (livello / h)
        out.append(perc(f"M{x + svaso - k:.1f},{ly:.1f} L{x + w - svaso + k:.1f},{ly:.1f} "
                        f"L{x + w - svaso:.1f},{y + h} L{x + svaso:.1f},{y + h} Z",
                        riemp=liquido, colore="none", sw=0))
    out.append(perc(f"M{x},{y} L{x + svaso},{y + h} L{x + w - svaso},{y + h} L{x + w},{y}"))
    return "".join(out)


def vaschetta(x, y, w, h, livello=0, liquido=ACQUA):
    out = []
    if livello > 0:
        out.append(rett(x + 2, y + h - livello, w - 4, livello, riemp=liquido, colore="none", sw=0))
    out.append(perc(f"M{x},{y} L{x},{y + h} L{x + w},{y + h} L{x + w},{y}"))
    return "".join(out)


def gocce(punti, r=1.8, colore=BLU):
    return "".join(cerchio(px, py, r, riemp=colore, colore="none", sw=0) for px, py in punti)


def moto(x, y, lung=8, n=3, passo=5, colore=CALDO):
    """Trattini di movimento (scuotimento)."""
    return "".join(linea(x, y + i * passo, x + lung, y + i * passo, 2, colore) for i in range(n))


def omino(x, y, h=26, colore=BLU):
    """Figura umana stilizzata; (x,y) = piedi, centro."""
    t = h * 0.28
    return (cerchio(x, y - h + t / 2, t / 2, colore=colore) +
            linea(x, y - h + t, x, y - h * 0.38, 2, colore) +
            linea(x, y - h * 0.72, x - h * 0.22, y - h * 0.52, 2, colore) +
            linea(x, y - h * 0.72, x + h * 0.22, y - h * 0.52, 2, colore) +
            linea(x, y - h * 0.38, x - h * 0.2, y, 2, colore) +
            linea(x, y - h * 0.38, x + h * 0.2, y, 2, colore))


def piano(x1, x2, y, colore=BLU):
    return linea(x1, y, x2, y, 2, colore)


# ------------------------------------------------------------------ scene
# Ogni voce: titolo esatto dell'esperimento -> (disegno, descrizione testuale).
# La descrizione è l'equivalente testuale della figura, non una didascalia:
# chi non vede il disegno deve capire lo stesso com'è fatto il montaggio.

def _vulcano():
    d = [
        bicchiere(16, 44, 46, 50, livello=34),
        bicchiere(98, 44, 46, 50, livello=34, liquido=TERRA),
        linea(30, 30, 39, 60), linea(112, 30, 121, 60),          # cannucce
        cerchio(39, 52, 3), cerchio(35, 42, 2.5), cerchio(41, 34, 2),  # bolle libere
        perc("M110,58 q11,-13 22,0", riemp=TERRA),               # bolla che gonfia
        perc("M110,58 q11,-13 22,0"),
        testo(39, 110, "acqua"), testo(121, 110, "pur&egrave;"),
        piano(8, 152, 96),
    ]
    return "".join(d), ("Due bicchieri affiancati con una cannuccia ciascuno: in quello con "
                        "l'acqua le bolle salgono e scoppiano subito, in quello con il pur&egrave; "
                        "denso la bolla resta intrappolata e gonfia la superficie.")


def _gelatina():
    d = [
        rett(22, 62, 116, 26, r=3, riemp=ACQUA),                 # teglia di gelatina
        linea(40, 62, 40, 34), cerchio(40, 30, 5, riemp="#fff"),  # torretta bassa
        linea(112, 62, 112, 20), cerchio(112, 16, 5, riemp="#fff"),  # torretta alta
        moto(6, 66, 10, 3, 6), moto(144, 66, 10, 3, 6),
        testo(80, 104, "si scuote la teglia"),
    ]
    return "".join(d), ("Una teglia di gelatina con due torrette di stuzzicadenti e marshmallow, "
                        "una bassa e una alta; le frecce ai lati indicano che si scuote la teglia.")


def _liquefazione():
    d = [
        vaschetta(16, 46, 52, 48), vaschetta(92, 46, 52, 48),
        rett(18, 62, 48, 30, riemp=TERRA, colore="none", sw=0),   # sabbia asciutta
        # Sabbia satura: la sabbia resta visibile e l'acqua le sta SOPRA in
        # trasparenza. Riempirla di solo azzurro faceva sembrare il contenitore
        # pieno d'acqua, cioè un esperimento diverso da quello descritto.
        rett(94, 62, 48, 30, riemp=TERRA, colore="none", sw=0),
        rett(94, 62, 48, 30, riemp=ACQUA, colore="none", sw=0, opac="0.5"),
        *[cerchio(99 + i * 8, 70 + (i % 2) * 9, 1.5, riemp="#5b87b5", colore="none", sw=0)
          for i in range(6)],                                     # acqua fra i granelli
        linea(94, 62, 142, 62, 2, "#3f6f9f"),                     # superficie lucida
        cerchio(42, 58, 5, riemp="#fff"),                         # biglia in superficie
        cerchio(118, 82, 5, riemp="#fff"),                        # biglia sprofondata
        freccia(118, 68, 118, 76),
        testo(42, 110, "asciutta"), testo(118, 110, "satura"),
    ]
    return "".join(d), ("Due contenitori con sabbia: in quello asciutto la biglia resta appoggiata "
                        "in superficie, in quello saturo d'acqua la stessa biglia sprofonda.")


def _sismografo():
    d = [
        perc("M28,30 L28,86 L108,86 L108,30", sw=2),              # scatola
        rett(40, 44, 34, 26, riemp="#fff"),                       # finestra
        linea(68, 30, 68, 52),                                    # spago
        perc("M60,52 L64,70 L72,70 L76,52 Z", riemp="#fff"),      # bicchiere
        linea(68, 70, 68, 82, 2, CALDO),                          # pennarello
        rett(22, 82, 116, 8, riemp=ACQUA),                        # striscia di carta
        freccia(140, 86, 152, 86),
        perc("M30,86 q6,-4 12,0 q6,4 12,0 q6,-4 12,0", colore=CALDO, sw=1.5),
        testo(80, 108, "si tira la striscia"),
    ]
    return "".join(d), ("Una scatola di cartone con una finestra ritagliata: dentro pende un "
                        "bicchiere con un pennarello che tocca una striscia di carta, tirata "
                        "fuori da un lato e gi&agrave; segnata da una traccia ondulata.")


def _risonanza():
    d = [
        rett(18, 88, 124, 8, riemp=TERRA),                        # base
        linea(44, 88, 44, 66), cerchio(44, 62, 5, riemp="#fff"),
        linea(80, 88, 80, 46), cerchio(80, 42, 5, riemp="#fff"),
        perc("M116,88 q8,-22 4,-42", colore=CALDO), cerchio(120, 42, 5, riemp="#fff", colore=CALDO),
        moto(18, 100, 10, 2, 6), moto(134, 100, 10, 2, 6),
        testo(80, 116, "la base oscilla al ritmo giusto"),
    ]
    return "".join(d), ("Tre cannucce di altezza diversa in piedi su una base, ognuna con un "
                        "gommino in cima: al ritmo giusto una sola, quella evidenziata, oscilla "
                        "molto pi&ugrave; delle altre.")


def _spugna():
    d = [
        perc("M20,86 L140,86", sw=2),
        perc("M34,78 L108,50 L120,66 L46,94 Z", riemp=ACQUA),     # spugna inclinata
        perc("M96,54 L112,48 L118,58 L102,64 Z", riemp=TERRA),    # terra sopra
        freccia(118, 26, 108, 44),
        gocce([(60, 92), (70, 96), (80, 92)]),
        testo(80, 112, "acqua sulla spugna inclinata"),
    ]
    return "".join(d), ("Una spugna appoggiata inclinata su un piatto con un po' di terra sopra; "
                        "dall'alto si versa acqua che la attraversa e cola in basso.")


def _radici():
    d = [
        perc("M14,54 L62,54 L70,86 L14,86 Z", riemp=TERRA),
        perc("M90,54 L138,54 L146,86 L90,86 Z", riemp=TERRA),
        linea(90, 54, 138, 54, 3, "#2f6b3a"),                     # zolla d'erba
        perc("M104,56 l-4,12 M116,56 l0,14 M128,56 l4,12", sw=1.5, colore="#2f6b3a"),
        freccia(30, 24, 36, 46), freccia(110, 24, 116, 46),
        perc("M70,86 q6,8 10,14", colore=TERRA, sw=4),            # colaticcio torbido
        perc("M146,86 q6,8 10,14", colore=ACQUA, sw=4),
        testo(40, 110, "terra nuda"), testo(120, 110, "con radici"),
    ]
    return "".join(d), ("Due vaschette inclinate sotto la stessa pioggia: da quella con terra nuda "
                        "esce acqua torbida e carica di terra, da quella coperta d'erba esce acqua "
                        "molto pi&ugrave; pulita.")


def _asfalto():
    d = [
        perc("M14,56 L64,44 L72,74 L22,86 Z", riemp=TERRA),
        perc("M90,56 L140,44 L148,74 L98,86 Z", riemp=GRIGIO),
        freccia(30, 20, 34, 40), freccia(106, 20, 110, 40),
        gocce([(32, 58), (44, 54), (54, 50)]),                    # assorbita
        perc("M98,80 q14,10 22,18", colore=ACQUA, sw=4),          # scorre via
        testo(40, 110, "prato"), testo(120, 110, "asfalto"),
    ]
    return "".join(d), ("Due vassoi inclinati sotto la stessa acqua: nel vassoio con la terra "
                        "l'acqua viene assorbita, su quello con il foglio di plastica scivola via "
                        "tutta insieme.")


def _pluviometro():
    d = [
        perc("M56,40 L48,58 L48,96 L112,96 L112,58 L104,40", sw=2),   # corpo bottiglia
        perc("M56,40 L48,58 L112,58 L104,40 Z", riemp="#fff"),        # imbuto capovolto
        linea(48, 58, 112, 58, 2, BLU, "3 2"),
        rett(48, 78, 64, 18, riemp=ACQUA, colore="none", sw=0),
        rett(48, 88, 64, 8, riemp=GRIGIO, colore="none", sw=0),       # sassi
        rett(116, 58, 8, 38, riemp="#fff"),                           # righello
        *[linea(116, 64 + i * 8, 121, 64 + i * 8, 1.2) for i in range(4)],
        freccia(80, 18, 80, 34),
        testo(80, 112, "imbuto + righello"),
    ]
    return "".join(d), ("Una bottiglia tagliata a met&agrave;: la parte alta &egrave; capovolta "
                        "dentro la bassa e fa da imbuto, sul fianco &egrave; fissato un righello e "
                        "sul fondo ci sono dei sassi per la stabilit&agrave;.")


def _maremoto():
    d = [
        perc("M12,44 L12,88 L148,88 L148,44", sw=2),
        rett(14, 66, 132, 22, riemp=ACQUA, colore="none", sw=0),
        perc("M14,66 q12,-10 24,0 q12,10 24,0 q12,-10 24,0 q12,10 24,0 q12,-10 24,0"),
        rett(120, 88, 26, 8, riemp=GRIGIO),                       # libro che alza il lato
        perc("M120,66 L146,52 L146,66 Z", riemp=TERRA),           # fondale in salita
        freccia(30, 56, 62, 56),
        testo(80, 110, "il fondale sale: l'onda cresce"),
    ]
    return "".join(d), ("Una vaschetta con acqua tenuta inclinata da un libro sotto un'estremit&agrave;: "
                        "l'onda parte dal lato profondo e cresce avvicinandosi al fondale in salita.")


def _tombino():
    d = [
        perc("M40,52 q40,-14 80,0 L112,64 L48,64 Z", riemp="#fff"),   # colino
        *[linea(50 + i * 9, 56, 50 + i * 9, 64, 1.2) for i in range(8)],
        perc("M48,64 L52,94 L108,94 L112,64", sw=2),                  # contenitore
        rett(52, 84, 56, 10, riemp=ACQUA, colore="none", sw=0),
        perc("M56,48 q6,-5 12,0 M84,46 q6,-5 12,0", colore=TERRA, sw=2.5),  # foglie
        freccia(80, 16, 80, 36),
        testo(80, 112, "foglie sopra: passa meno acqua"),
    ]
    return "".join(d), ("Un colino appoggiato su un contenitore fa da tombino: alcune foglie "
                        "appoggiate sopra ne coprono i fori e l'acqua versata passa pi&ugrave; "
                        "lentamente.")


def _capillarita():
    d = [
        bicchiere(56, 56, 48, 40, livello=22, liquido="#7aa7cf"),
        rett(64, 20, 7, 48, riemp="#e9eef4"),                     # carta assorbente
        rett(78, 20, 7, 48, riemp="#f2f0e8"),                     # stoffa
        rett(92, 20, 7, 48, riemp="#fff"),                        # plastificata
        rett(64, 40, 7, 28, riemp="#7aa7cf", colore="none", sw=0),   # risalita alta
        rett(78, 54, 7, 14, riemp="#7aa7cf", colore="none", sw=0),   # media
        rett(92, 64, 7, 4, riemp="#7aa7cf", colore="none", sw=0),    # quasi nulla
        rett(64, 20, 7, 48), rett(78, 20, 7, 48), rett(92, 20, 7, 48),
        freccia(56, 60, 56, 42),
        testo(80, 112, "carta &middot; stoffa &middot; plastica"),
    ]
    return "".join(d), ("Tre striscioline immerse nello stesso bicchiere di acqua colorata: nella "
                        "carta assorbente l'acqua risale molto, nella stoffa meno, nella carta "
                        "plastificata quasi per niente.")


def _triangolo_fuoco():
    d = [
        rett(56, 88, 48, 6, r=2, riemp="#fff"),                   # piattino
        rett(74, 62, 12, 26, riemp="#fff"),                       # candela
        perc("M80,62 q-7,-9 0,-16 q7,7 0,16 Z", riemp=CALDO, colore=CALDO, sw=1),
        perc("M46,18 L46,88 M114,18 L114,88", sw=2),              # barattolo
        perc("M46,18 L114,18", sw=2),
        freccia(130, 34, 118, 44),
        testo(80, 112, "il barattolo scende sulla fiamma"),
    ]
    return "".join(d), ("Una candelina accesa su un piattino e un barattolo di vetro capovolto "
                        "che viene calato sopra la fiamma fino a coprirla.")


def _bosco_tessere():
    d = [
        *[rett(16 + i * 11, 54, 6, 30, riemp="#fff") for i in range(5)],
        perc("M74,84 L96,60 L102,64 L80,88 Z", riemp="#fff"),     # tessera che cade
        *[rett(112 + i * 11, 54, 6, 30, riemp="#fff") for i in range(3)],
        linea(104, 50, 104, 90, 2, CALDO, "4 3"),                 # varco
        freccia(10, 42, 22, 50),
        testo(80, 110, "il varco ferma la caduta"),
    ]
    return "".join(d), ("Una fila di tessere del domino che cadono una sull'altra si interrompe "
                        "dove c'&egrave; uno spazio vuoto: oltre il varco le tessere restano in piedi.")


def _sole_ombra():
    d = [
        cerchio(24, 22, 9, riemp="#fff", colore=CALDO),
        *[linea(24 + 13 * math.cos(a), 22 + 13 * math.sin(a),
                24 + 17 * math.cos(a), 22 + 17 * math.sin(a), 1.5, CALDO)
          for a in [i * 0.785 for i in range(8)]],
        rett(52, 52, 40, 5, riemp="#fff"),                        # foglio bianco
        rett(102, 52, 40, 5, riemp="#333", colore="#333"),        # foglio nero
        rett(68, 60, 6, 30, r=3, riemp="#fff"), cerchio(71, 92, 5, riemp="#fff"),
        rett(118, 60, 6, 30, r=3, riemp="#fff"), cerchio(121, 92, 5, riemp=CALDO, colore=CALDO),
        rett(119, 74, 4, 16, riemp=CALDO, colore="none", sw=0),
        testo(71, 112, "chiaro"), testo(121, 112, "scuro"),
    ]
    return "".join(d), ("Al sole, due termometri sotto due fogli: sotto il foglio chiaro la "
                        "colonnina resta bassa, sotto il foglio scuro sale.")


def _isolanti():
    d = [
        rett(14, 46, 38, 46, r=3, riemp=ACQUA), rett(14, 40, 38, 8, r=2, riemp="#fff"),
        rett(61, 46, 38, 46, r=3, riemp=ACQUA), rett(61, 40, 38, 8, r=2, riemp="#fff"),
        rett(108, 46, 38, 46, r=3, riemp=ACQUA), rett(108, 40, 38, 8, r=2, riemp="#fff"),
        *[linea(16, 52 + i * 8, 50, 52 + i * 8, 1.4, GRIGIO) for i in range(5)],        # alluminio
        *[perc(f"M63,{52 + i * 8} q9,-5 18,0 q9,5 18,0", sw=1.4, colore="#6b5b3e") for i in range(5)],  # lana
        *[linea(110, 52 + i * 8, 144, 52 + i * 8, 1.4, "#8a8a8a", "3 2") for i in range(5)],  # giornale
        rett(30, 24, 4, 18, r=2, riemp="#fff"),
        testo(33, 110, "alluminio"), testo(80, 110, "lana"), testo(127, 110, "giornale"),
    ]
    return "".join(d), ("Tre barattoli uguali con la stessa acqua tiepida, avvolti uno "
                        "nell'alluminio, uno nella lana e uno nella carta di giornale, con un "
                        "termometro per confrontarli.")


def _sale_ghiaccio():
    d = [
        perc("M18,80 q30,10 60,0", sw=2), perc("M82,80 q30,10 60,0", sw=2),
        perc("M34,58 L62,58 L58,78 L38,78 Z", riemp=ACQUA),       # cubetto intero
        perc("M100,64 L124,64 L120,78 L104,78 Z", riemp=ACQUA),   # cubetto consumato
        # I granelli di sale stanno SOPRA il cubetto, non a mezz'aria: staccati
        # sembravano pioggia e non si capiva su quale dei due si agisce.
        gocce([(102, 60), (109, 57), (116, 60), (122, 58)], 1.5, CALDO),
        gocce([(104, 84), (112, 86), (120, 84)]),
        testo(48, 108, "senza sale"), testo(112, 108, "con sale"),
    ]
    return "".join(d), ("Due cubetti di ghiaccio uguali su due piattini: quello su cui &egrave; "
                        "stato sparso il sale si &egrave; gi&agrave; sciolto molto di pi&ugrave;.")


def _manica_vento():
    d = [
        linea(26, 92, 26, 22, 3), piano(12, 44, 92),
        cerchio(26, 30, 0),                                        # (nessun perno visibile)
        linea(26, 30, 34, 30, 2),
        perc("M34,20 L34,40 L34,40", sw=2),                        # cerchio d'imbocco (di taglio)
        perc("M34,20 q40,4 62,10 q10,2 18,6 M34,40 q40,-2 62,2 q10,1 18,4", sw=2),
        perc("M34,20 L34,40", sw=2),
        *[linea(96 + i * 6, 26 + i * 2, 96 + i * 6, 40 + i * 2, 1.4, GRIGIO) for i in range(4)],
        *[perc(f"M4,{16 + i * 10} q14,-4 26,0", sw=1.5, colore=CALDO) for i in range(3)],
        testo(80, 110, "il vento la riempie e la orienta"),
    ]
    return "".join(d), ("Una manica a vento: un sacchetto fissato a un cerchio di cartoncino in "
                        "cima a un bastoncino, gonfiata e tenuta orizzontale dal vento che arriva "
                        "da sinistra.")


def _distanza_temporale():
    d = [
        perc("M16,34 q-2,-14 12,-14 q4,-10 16,-6 q12,-6 18,6 q12,0 10,14 Z", riemp="#e7ecf2"),
        perc("M40,34 L32,52 L40,52 L32,68", colore=CALDO, sw=2.5),   # fulmine
        cerchio(112, 44, 9), perc("M112,44 q6,-8 0,-14", sw=1.5),    # orecchio stilizzato
        *[perc(f"M{86 + i * 7},{36 - i * 3} q-8,8 0,16", sw=1.4, colore=GRIGIO) for i in range(3)],
        testo(80, 92, "conta i secondi fra lampo e tuono"),
        testo(80, 108, "3 secondi &asymp; 1 km"),
    ]
    return "".join(d), ("Una nuvola con un lampo a sinistra e un orecchio a destra, con le onde "
                        "del tuono che arrivano dopo: si contano i secondi fra il lampo e il tuono.")


def _siccita():
    d = [
        cerchio(28, 22, 8, riemp="#fff", colore=CALDO),
        *[linea(28 + 11 * math.cos(a), 22 + 11 * math.sin(a),
                28 + 15 * math.cos(a), 22 + 15 * math.sin(a), 1.4, CALDO)
          for a in [i * 0.785 for i in range(8)]],
        perc("M104,14 q-2,-8 8,-8 q3,-7 11,-4 q9,-4 12,5 q9,0 7,10 Z", riemp="#e7ecf2"),  # ombra
        perc("M18,60 q30,16 60,0", sw=2), rett(24, 60, 48, 8, riemp=ACQUA, colore="none", sw=0),
        perc("M84,60 q30,16 60,0", sw=2), rett(90, 60, 48, 16, riemp=ACQUA, colore="none", sw=0),
        linea(24, 60, 72, 60, 1.6, CALDO, "3 2"), linea(90, 60, 138, 60, 1.6, CALDO, "3 2"),
        testo(48, 104, "al sole"), testo(114, 104, "all'ombra"),
    ]
    return "".join(d), ("Due piattini con la stessa acqua e il livello segnato: in quello lasciato "
                        "al sole l'acqua &egrave; scesa molto sotto il segno, in quello all'ombra quasi no.")


def _condensa():
    d = [
        bicchiere(26, 40, 44, 54, livello=38),
        bicchiere(96, 40, 44, 54, livello=38),
        *[rett(34 + i * 8, 46, 7, 6, r=1, riemp="#fff") for i in range(3)],   # cubetti di ghiaccio
        gocce([(26, 58), (24, 70), (28, 82), (70, 62), (72, 76)], 2),          # condensa fuori
        testo(48, 110, "acqua e ghiaccio"), testo(118, 110, "acqua ambiente"),
    ]
    return "".join(d), ("Due bicchieri uguali: su quello con acqua e ghiaccio si formano goccioline "
                        "all'esterno, su quello con acqua a temperatura ambiente il vetro resta asciutto.")


def _nube():
    d = [
        rett(14, 22, 132, 72, r=3),                                # stanza
        omino(32, 84, 24),
        *[perc(f"M40,84 a{14 + i * 16},{14 + i * 16} 0 0 1 {28 + i * 32},-{28 + i * 32}",
               sw=1.6, colore=CALDO, tratteggio="4 3") for i in range(3)],
        omino(84, 84, 24), omino(128, 84, 24),
        testo(80, 110, "chi &egrave; vicino lo sente prima"),
    ]
    return "".join(d), ("La pianta di una stanza: da chi sta in un angolo partono onde concentriche "
                        "che raggiungono prima la persona vicina e poi quella lontana.")


def _germi():
    d = [
        cerchio(80, 58, 40, riemp=ACQUA), cerchio(80, 58, 40),
        *[cerchio(80 + 33 * math.cos(i * 0.6), 58 + 33 * math.sin(i * 0.6),
                  1.6, riemp="#333", colore="none", sw=0) for i in range(11)],
        cerchio(80, 58, 15, riemp="#fff", colore="none", sw=0),
        linea(80, 8, 80, 44, 2.5, CALDO), cerchio(80, 46, 4, riemp=CALDO, colore=CALDO),
        *[freccia(80 + 17 * math.cos(a), 58 + 17 * math.sin(a),
                  80 + 27 * math.cos(a), 58 + 27 * math.sin(a))
          for a in [0.4, 1.8, 3.2, 4.6]],
        testo(80, 112, "il sapone allontana il pepe"),
    ]
    return "".join(d), ("Un piatto con acqua e pepe in superficie: appena il dito col sapone tocca "
                        "il centro, il pepe scappa verso il bordo lasciando un cerchio pulito.")


def _acqua_limpida():
    d = [
        perc("M20,22 L20,50 L14,58 L14,84 L38,84 L38,58 L32,50 L32,22", sw=2),   # bottiglia torbida
        rett(15, 62, 22, 21, riemp=TERRA, colore="none", sw=0),
        perc("M120,22 L120,50 L114,58 L114,84 L138,84 L138,58 L132,50 L132,22", sw=2),
        rett(115, 62, 22, 21, riemp=ACQUA, colore="none", sw=0),
        perc("M58,34 L102,34 L84,58 L84,72 L76,72 L76,58 Z", riemp="#fff"),       # imbuto
        perc("M62,38 L98,38", sw=1.4, tratteggio="3 2"),                          # carta da filtro
        bicchiere(64, 78, 32, 26, livello=16),
        testo(80, 116, "torbida e salata: dopo il filtro sono uguali"),
    ]
    return "".join(d), ("Un imbuto con la carta da filtro sopra un bicchiere, fra due bottiglie: "
                        "una con acqua torbida di terra e una con acqua limpida ma salata; dopo il "
                        "filtro l'aspetto &egrave; lo stesso.")


def _distanza_riparo():
    d = [
        perc("M10,50 L30,50 L30,66 L10,66 Z", riemp="#fff"),       # torcia
        perc("M30,52 L74,36 L74,80 L30,64 Z", riemp="#fdf0e2", colore="none", sw=0),
        perc("M30,52 L74,36 M30,64 L74,80", sw=1.4, colore=CALDO, tratteggio="4 3"),
        perc("M48,44 q10,-8 12,4 q6,-4 4,8 L48,60 Z", riemp="#fff"),   # mano vicina
        rett(92, 34, 8, 50, riemp=GRIGIO),                             # libro
        perc("M116,44 q10,-8 12,4 q6,-4 4,8 L116,60 Z", riemp="#fff"), # mano lontana e schermata
        testo(80, 108, "pi&ugrave; lontano e schermato: arriva meno"),
    ]
    return "".join(d), ("Una torcia che illumina una mano vicina in pieno fascio; pi&ugrave; lontano "
                        "un libro spesso fa da schermo e la seconda mana resta in ombra.")


def _zaino():
    d = [
        perc("M22,44 q20,-18 40,0 L62,92 L22,92 Z", riemp="#fff"),
        perc("M30,44 q12,-10 24,0", sw=1.6), rett(30, 60, 24, 12, r=2),
        # Torcia: corpo + fascio, così si distingue da un cerchio qualunque.
        rett(80, 30, 16, 9, r=1, riemp="#fff"),
        perc("M96,28 L106,24 L106,45 L96,41 Z", riemp="#fdf0e2"),
        # Bottiglia d'acqua: collo + corpo.
        rett(118, 22, 5, 7, riemp="#fff"),
        perc("M115,29 L126,29 L128,34 L128,48 L113,48 L113,34 Z", riemp=ACQUA),
        # Radio a pile: antenna, manopola, griglia.
        rett(80, 58, 24, 17, r=2, riemp="#fff"), linea(84, 58, 80, 48),
        cerchio(98, 66, 3.5), *[linea(84, 62 + i * 4, 92, 62 + i * 4, 1.2) for i in range(3)],
        # Fischietto: corpo con boccaglio e foro.
        perc("M113,60 L131,60 q6,0 6,7 q0,7 -6,7 L113,74 Z", riemp="#fff"),
        cerchio(127, 67, 2.2), linea(113, 63, 107, 63, 3),
        perc("M82,88 l6,6 l11,-13", colore="#2f6b3a", sw=3),        # scelta buona
        testo(80, 112, "prima l'indispensabile"),
    ]
    return "".join(d), ("Uno zaino accanto agli oggetti da scegliere: torcia, radio a pile, "
                        "bottiglia d'acqua, fischietto e una barretta, segnati come da mettere dentro.")


def _mappa_pericoli():
    d = [
        rett(16, 18, 128, 76, r=2),
        linea(80, 18, 80, 60), linea(80, 60, 144, 60),
        perc("M30,34 l12,12 M42,34 l-12,12", colore=CALDO, sw=2.5),   # pericolo
        perc("M104,34 l12,12 M116,34 l-12,12", colore=CALDO, sw=2.5),
        cerchio(48, 78, 9, colore="#2f6b3a"), perc("M43,78 l4,4 l7,-8", colore="#2f6b3a", sw=2.2),
        freccia(96, 78, 130, 78, "#2f6b3a"),
        rett(140, 68, 4, 20, riemp="#2f6b3a", colore="none", sw=0),   # uscita
        testo(80, 110, "pericoli, posti sicuri, via d'uscita"),
    ]
    return "".join(d), ("La pianta di una casa con delle croci sui punti pericolosi, un segno di "
                        "spunta sui posti sicuri e una freccia che indica la via d'uscita.")


def _memory():
    d = [
        *[rett(16 + c * 26, 26 + r * 34, 22, 28, r=2, riemp="#eef2f6")
          for r in range(2) for c in range(5) if not (r == 0 and c in (1, 3))],
        # Sulle due carte girate un simbolo leggibile: porta + freccia che esce.
        # La sagoma dell'omino in corsa, a questa dimensione, era uno scarabocchio.
        *[x for c in (42, 94) for x in (
            rett(c, 26, 22, 28, r=2, riemp="#fff"),
            rett(c + 3, 31, 8, 18, riemp="#fff", colore="#2f6b3a"),
            freccia(c + 12, 40, c + 19, 40, "#2f6b3a", 2),
        )],
        testo(80, 108, "due uguali: coppia trovata"),
    ]
    return "".join(d), ("Cartoncini disposti a griglia con il dorso in alto: due sono girati e "
                        "mostrano lo stesso simbolo di uscita di emergenza, cio&egrave; una coppia trovata.")


def _chiamata_112():
    d = [
        omino(34, 88, 30), omino(126, 88, 30),
        rett(46, 56, 9, 15, r=2, riemp="#fff"), rett(106, 56, 9, 15, r=2, riemp="#fff"),
        perc("M62,44 q18,-12 36,0 q-18,12 -36,0 Z", riemp="#fff"),
        testo(80, 48, "112", 12, CALDO),
        *[perc(f"M{58 - i * 5},{60 + i * 4} q-4,6 0,12", sw=1.3, colore=GRIGIO) for i in range(2)],
        testo(80, 110, "dove sei, che cosa &egrave; successo"),
    ]
    return "".join(d), ("Due persone al telefono: chi chiama il 112 e l'operatore che risponde, "
                        "con il numero 112 nel fumetto fra i due.")


def _messaggio_corretto():
    d = [
        omino(30, 82, 28), omino(130, 82, 28),
        rett(42, 40, 20, 16, r=1, riemp="#fff"),
        *[linea(45, 44 + i * 4, 59, 44 + i * 4, 1.2) for i in range(3)],
        rett(98, 40, 20, 16, r=1, riemp="#fff"),
        *[linea(101, 44 + i * 4, 115, 44 + i * 4, 1.2) for i in range(3)],
        freccia(66, 44, 94, 44),
        freccia(94, 56, 66, 56, "#2f6b3a"),
        testo(80, 104, "si ripete e si conferma"),
    ]
    return "".join(d), ("Chi trasmette legge un messaggio scritto e chi riceve lo scrive; una "
                        "freccia di ritorno mostra che il messaggio viene ripetuto e confermato.")


def _telefono_bicchieri():
    d = [
        perc("M14,44 L26,44 L30,74 L18,74 Z", riemp="#fff"),
        perc("M146,44 L134,44 L130,74 L142,74 Z", riemp="#fff"),
        linea(28, 58, 132, 58, 2),
        *[perc(f"M{50 + i * 22},54 q6,4 12,0", sw=1.3, colore=CALDO) for i in range(3)],
        testo(80, 100, "spago teso: la voce passa"),
    ]
    return "".join(d), ("Due bicchieri di plastica uniti da uno spago ben teso, con dei piccoli "
                        "segni di vibrazione lungo il filo.")


def _voce_guida():
    d = [
        omino(46, 86, 32), rett(38, 62, 16, 5, r=2, riemp="#333", colore="#333"),   # benda
        omino(132, 86, 28),
        *[perc(f"M{118 - i * 8},{58 + i * 3} q-6,8 0,14", sw=1.4, colore=CALDO) for i in range(3)],
        rett(72, 78, 14, 10, r=2, riemp="#eef2f6"), rett(96, 74, 14, 14, r=2, riemp="#eef2f6"),
        perc("M46,90 q14,8 26,2", sw=1.6, colore="#2f6b3a", tratteggio="4 3"),
        testo(80, 110, "istruzioni brevi e precise"),
    ]
    return "".join(d), ("Una persona bendata avanza fra alcuni ostacoli morbidi seguendo la voce "
                        "di chi la guida da fuori percorso.")


def _allarme_livello():
    d = [
        vaschetta(16, 44, 76, 50, livello=26),
        rett(48, 44, 5, 26, riemp="#fff"),                          # stecchino guida
        perc("M42,66 q8,-8 16,0 q-8,8 -16,0 Z", riemp=TERRA),       # sughero galleggiante
        linea(50, 46, 50, 30), linea(50, 30, 112, 30),              # contatto mobile
        linea(112, 30, 112, 44),
        cerchio(112, 50, 6, riemp="#fff7d6", colore=CALDO),         # LED acceso
        *[linea(112 + 8 * math.cos(a), 50 + 8 * math.sin(a),
                112 + 12 * math.cos(a), 50 + 12 * math.sin(a), 1.4, CALDO)
          for a in [0.5, 1.6, 2.7, 3.8, 4.9, 6.0]],
        linea(112, 56, 112, 72), rett(102, 72, 20, 14, r=2, riemp="#fff"),  # pila
        testo(112, 96, "pila"), freccia(30, 76, 30, 62),
        testo(80, 112, "l'acqua sale: il circuito si chiude"),
    ]
    return "".join(d), ("Una bacinella in cui l'acqua sale e solleva un tappo di sughero: il "
                        "galleggiante chiude il circuito e il LED collegato alla pila si accende.")


# --------------------------------------------------------------- registro
# Chiave = titolo ESATTO dell'esperimento in `genera-schede-esperimenti.py`.
SCENE = {
    "Vulcano lento o vulcano esplosivo?": _vulcano,
    "Il terremoto di gelatina": _gelatina,
    "Quando il terreno perde sostegno": _liquefazione,
    "Costruiamo un sismografo": _sismografo,
    "Il ritmo che fa oscillare una torre": _risonanza,
    "La spugna e il fango": _spugna,
    "Le radici che tengono la terra": _radici,
    "Città di asfalto, città di prato": _asfalto,
    "Quanta pioggia è caduta?": _pluviometro,
    "L'onda di maremoto": _maremoto,
    "Il tombino ostruito": _tombino,
    "L'acqua risale da sola": _capillarita,
    "Il triangolo del fuoco": _triangolo_fuoco,
    "Il bosco di tessere": _bosco_tessere,
    "Sole o ombra? Chiaro o scuro?": _sole_ombra,
    "Quale materiale conserva il calore?": _isolanti,
    "Il sale che scioglie il ghiaccio": _sale_ghiaccio,
    "La forza del vento (la manica a vento)": _manica_vento,
    "Quanto è lontano il temporale?": _distanza_temporale,
    "L'acqua che sparisce (la siccità)": _siccita,
    "Le goccioline vengono dall'aria": _condensa,
    'Come si sparge una "nube"': _nube,
    "Caccia ai germi (il potere del sapone)": _germi,
    "Acqua limpida significa potabile?": _acqua_limpida,
    "Più lontano, più al riparo": _distanza_riparo,
    "Cosa metto nello zaino?": _zaino,
    "La mappa dei pericoli e dei luoghi sicuri": _mappa_pericoli,
    "Memory dei segnali di sicurezza": _memory,
    "La chiamata perfetta al 112": _chiamata_112,
    "Il messaggio arriva corretto?": _messaggio_corretto,
    "Il telefono con i bicchieri": _telefono_bicchieri,
    "La voce che guida": _voce_guida,
    "Un piccolo allarme di livello": _allarme_livello,
}


def figura(titolo):
    """SVG pronto da inserire nella scheda, o stringa vuota se non c'è il disegno.

    La figura è `role="img"` con descrizione equivalente: per chi non vede il
    disegno la descrizione deve bastare a capire il montaggio (WCAG 1.1.1).
    Il contenuto grafico è `aria-hidden` perché gli screen reader non leggano
    i singoli tracciati.
    """
    scena = SCENE.get(titolo)
    if not scena:
        return ""
    disegno, descrizione = scena()
    return (
        f'<figure class="esp-figura">'
        f'<svg viewBox="{VIEWBOX}" role="img" aria-label="{descrizione}" '
        f'xmlns="http://www.w3.org/2000/svg" fill="none" '
        f'stroke-linecap="round" stroke-linejoin="round">'
        f'<g aria-hidden="true">{disegno}</g>'
        f'</svg></figure>'
    )


def mancanti(titoli):
    """Titoli senza illustrazione: serve al generatore per non lasciarne indietro."""
    return [t for t in titoli if t not in SCENE]
