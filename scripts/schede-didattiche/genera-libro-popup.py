#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Libro pop-up di protezione civile: undici fogli A4 da stampare e montare.

  1     copertina
  2     guida al taglio e alla piega, con la legenda dei tracciati
  3-10  le otto tavole, ciascuna con il testo e la sua fustella
  11    diploma e tesserino

Le fustelle sono disegnate in millimetri veri (1 unità SVG = 1 mm): stampando
a dimensione reale si ritagliano direttamente dal foglio, righello alla mano.
I quattro meccanismi sono quelli che reggono davvero in mano a un bambino —
piega a V con alette, gradino tagliato nella piega, volvella con fermacampione,
linguetta scorrevole — e nessuno chiede colla dove non serve.

I contenuti stanno in libro_popup_dati.py e vengono tutti da pagine già
pubblicate sul sito: qui non si inventa nessuna istruzione di sicurezza.
"""
import html, pathlib, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from libro_popup_dati import ALLERTA, TAVOLE  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
REV = "13/09/2026"
DEST = ROOT / "static/formazione/schede-stampabili/libro-popup-protezione-civile/index.html"
PITTO = "/pittogrammi/arasaac-bn"

E = lambda s: html.escape(s, quote=True)          # noqa: E731
TAGLIO = 'stroke="#111827" stroke-width="0.5" fill="none"'
MONTE = 'stroke="#0284c7" stroke-width="0.5" fill="none" stroke-dasharray="3 2"'
VALLE = 'stroke="#ea580c" stroke-width="0.5" fill="none" stroke-dasharray="0.7 1.7" stroke-linecap="round"'


def svg(w, h, corpo):
    """Tela in millimetri veri: 1 unità del viewBox = 1 mm sul foglio."""
    return (f'<svg class="fust" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}" '
            f'role="img" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><pattern id="colla" width="3" height="3" patternTransform="rotate(45)" '
            f'patternUnits="userSpaceOnUse"><rect width="3" height="3" fill="#fef3c7"/>'
            f'<line x1="0" y1="0" x2="0" y2="3" stroke="#d97706" stroke-width="0.8"/>'
            f'</pattern></defs>{corpo}</svg>')


def colla(x, y, w, h, testo="INCOLLA"):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#colla)" '
            f'stroke="#d97706" stroke-width="0.4" stroke-dasharray="1.5 1.5"/>'
            f'<text x="{x + w / 2}" y="{y + h / 2 + 1.1}" text-anchor="middle" '
            f'font-size="2.6" fill="#92400e" font-weight="bold">{testo}</text>')


def quota(x1, y, x2, testo):
    """Linea di quota orizzontale con la misura scritta sopra."""
    return (f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#64748b" stroke-width="0.3"/>'
            f'<line x1="{x1}" y1="{y - 1.2}" x2="{x1}" y2="{y + 1.2}" stroke="#64748b" stroke-width="0.3"/>'
            f'<line x1="{x2}" y1="{y - 1.2}" x2="{x2}" y2="{y + 1.2}" stroke="#64748b" stroke-width="0.3"/>'
            f'<text x="{(x1 + x2) / 2}" y="{y - 1.8}" text-anchor="middle" font-size="2.6" '
            f'fill="#475569">{testo}</text>')


def figura(slug, alt, x, y, lato):
    return (f'<image href="{PITTO}/{slug}.png" x="{x}" y="{y}" width="{lato}" height="{lato}" '
            f'preserveAspectRatio="xMidYMid meet"><title>{E(alt)}</title></image>')


# ---------------------------------------------------------------------------
# I quattro meccanismi
# ---------------------------------------------------------------------------
def fustella_vfold(slug, alt):
    """Rettangolo con piega centrale a monte e due alette in basso.

    L'angolo della V non si taglia: lo si ottiene incollando le due alette
    di sbieco, una per facciata, con la piega del pezzo appoggiata sulla
    piega della pagina. Così la fustella resta un rettangolo — che un
    bambino ritaglia dritto — e il meccanismo funziona lo stesso.
    """
    W, H, TAB = 96, 52, 12
    c = W / 2 + 6
    return svg(W + 12, H + TAB + 20, "".join([
        f'<rect x="6" y="6" width="{W}" height="{H}" {TAGLIO} rx="1"/>',
        figura(slug, alt, c - 20, 10, 40),
        f'<line x1="{c}" y1="4" x2="{c}" y2="{6 + H + TAB}" {MONTE}/>',
        f'<line x1="6" y1="{6 + H}" x2="{6 + W}" y2="{6 + H}" {VALLE}/>',
        f'<rect x="6" y="{6 + H}" width="{W}" height="{TAB}" {TAGLIO}/>',
        colla(8, 8 + H, W / 2 - 4, TAB - 4, "ALETTA SINISTRA"),
        colla(c + 2, 8 + H, W / 2 - 4, TAB - 4, "ALETTA DESTRA"),
        quota(6, H + TAB + 16, 6 + W, "96 mm"),
    ]))


def fustella_gradino(slug, alt):
    """Il gradino si taglia dentro la piega del foglio: niente colla.

    I due tagli partono DALLA piega e le vanno perpendicolari; la riga che li
    unisce alla base è la piega su cui il gradino si ribalta in avanti. Tagli
    paralleli alla piega, o staccati da essa, non producono nessun rilievo —
    era l'errore della prima versione.
    """
    W, H = 108, 74
    yF = 20          # la piega del foglio
    D = 34           # quanto sporge il gradino
    x1, x2 = 30, 90
    return svg(W + 12, H + 16, "".join([
        f'<rect x="6" y="6" width="{W}" height="{H}" fill="#ffffff" stroke="#cbd5e1" '
        f'stroke-width="0.4" stroke-dasharray="2 2"/>',
        f'<line x1="6" y1="{yF}" x2="{6 + W}" y2="{yF}" {MONTE}/>',
        f'<text x="{6 + W - 2}" y="{yF - 2}" text-anchor="end" font-size="2.8" '
        f'fill="#0284c7">piega del foglio</text>',
        f'<line x1="{x1}" y1="{yF}" x2="{x1}" y2="{yF + D}" {TAGLIO}/>',
        f'<line x1="{x2}" y1="{yF}" x2="{x2}" y2="{yF + D}" {TAGLIO}/>',
        f'<line x1="{x1}" y1="{yF + D}" x2="{x2}" y2="{yF + D}" {VALLE}/>',
        figura(slug, alt, (x1 + x2) / 2 - 13, yF + 4, 26),
        quota(x1, yF + D + 11, x2, "60 mm"),
        f'<text x="{x2 + 4}" y="{yF + D / 2}" font-size="2.8" fill="#475569">'
        f'profondità 34 mm</text>',
        f'<text x="{6 + W / 2}" y="{yF + D + 20}" text-anchor="middle" font-size="2.8" '
        f'fill="#475569">i due tagli partono dalla piega; poi spingi il gradino in avanti</text>',
    ]))


def fustella_volvella():
    """Disco dei quattro colori + finestra da aprire nel foglio sopra."""
    R, cx, cy = 34, 42, 42
    settori = []
    for i, (nome, colore, _, _) in enumerate(ALLERTA):
        a0, a1 = i * 90 - 90, (i + 1) * 90 - 90
        import math
        p0 = (cx + R * math.cos(math.radians(a0)), cy + R * math.sin(math.radians(a0)))
        p1 = (cx + R * math.cos(math.radians(a1)), cy + R * math.sin(math.radians(a1)))
        am = math.radians((a0 + a1) / 2)
        settori.append(
            f'<path d="M{cx} {cy} L{p0[0]:.1f} {p0[1]:.1f} A{R} {R} 0 0 1 {p1[0]:.1f} {p1[1]:.1f} Z" '
            f'fill="{colore}" fill-opacity="0.18" stroke="#111827" stroke-width="0.4"/>'
            f'<text x="{cx + R * 0.72 * math.cos(am):.1f}" y="{cy + R * 0.72 * math.sin(am):.1f}" '
            f'text-anchor="middle" font-size="3.4" font-weight="bold" fill="#111827">{nome}</text>')
    return svg(148, 86, "".join(settori + [
        f'<circle cx="{cx}" cy="{cy}" r="{R}" {TAGLIO}/>',
        f'<circle cx="{cx}" cy="{cy}" r="2" {TAGLIO}/>',
        f'<line x1="{cx}" y1="{cy}" x2="{cx - 20}" y2="{cy + R + 7}" stroke="#64748b" stroke-width="0.3"/>',
        f'<text x="{cx - 21}" y="{cy + R + 10}" text-anchor="middle" font-size="2.8" fill="#475569">'
        f'foro per il fermacampione</text>',
        f'<line x1="{cx}" y1="{cy}" x2="{cx + 8.6}" y2="{cy - 8.6}" stroke="#64748b" '
        f'stroke-width="0.3" stroke-dasharray="1 1"/>',
        f'<circle cx="{cx + 8.6}" cy="{cy - 8.6}" r="1.2" fill="none" stroke="#111827" '
        f'stroke-width="0.4"/>',
        f'<text x="{cx + 10.5}" y="{cy - 9.6}" font-size="2.4" fill="#475569">'
        f'qui cade il centro della finestra</text>',
        f'<rect x="{cx + R + 14}" y="{cy + 10}" width="20" height="12" fill="none" '
        f'stroke="#111827" stroke-width="0.7"/>',
        f'<text x="{cx + R + 24}" y="{cy + 17.5}" text-anchor="middle" font-size="2.8" '
        f'fill="#111827" font-weight="bold">FINESTRA</text>',
        f'<text x="{cx + R + 24}" y="{cy + 27}" text-anchor="middle" font-size="2.4" '
        f'fill="#475569">20 × 12 mm</text>',
        f'<text x="{cx + R + 12}" y="{cy - 16}" font-size="2.8" fill="#475569">'
        f'la finestra si ritaglia nel foglio,</text>',
        f'<text x="{cx + R + 12}" y="{cy - 12}" font-size="2.8" fill="#475569">'
        f'non nel disco: è la finta da cui</text>',
        f'<text x="{cx + R + 12}" y="{cy - 8}" font-size="2.8" fill="#475569">'
        f'si vede un colore per volta.</text>',
        f'<text x="{cx + R + 12}" y="{cy - 2}" font-size="2.8" fill="#475569">'
        f'Deve stare tutta dentro uno spicchio:</text>',
        f'<text x="{cx + R + 12}" y="{cy + 2}" font-size="2.8" fill="#475569">'
        f'a cavallo di due, i colori si vedrebbero a coppie.</text>',
        f'<text x="{cx + R + 12}" y="{cy + 6}" font-size="2.8" fill="#475569">'
        f'Il centro va a 12 mm dal foro, in diagonale.</text>',
        quota(cx - R, 83, cx + R, "68 mm di diametro"),
    ]))


def fustella_linguetta(slug, alt):
    """Striscia che scorre dentro due fessure: si tira e la figura avanza."""
    W, H = 118, 24
    return svg(W + 12, H + 34, "".join([
        f'<rect x="6" y="6" width="{W}" height="{H}" {TAGLIO} rx="1"/>',
        figura(slug, alt, 10, 7, 22),
        f'<text x="{6 + W - 4}" y="{6 + H / 2 + 1.4}" text-anchor="end" font-size="5" '
        f'font-weight="bold" fill="#0b3c5d">TIRA →</text>',
        quota(6, H + 14, 6 + W, "118 mm"),
        f'<line x1="30" y1="{H + 24}" x2="30" y2="{H + 30}" {TAGLIO}/>',
        f'<line x1="90" y1="{H + 24}" x2="90" y2="{H + 30}" {TAGLIO}/>',
        f'<text x="60" y="{H + 22}" text-anchor="middle" font-size="2.8" fill="#475569">'
        f'le due fessure nel foglio, lunghe 26 mm e distanti 60 mm</text>',
    ]))


def fustella_tasca():
    """Tasca a tre alette: si incolla solo sui bordi, il quarto lato resta aperto."""
    W, H = 104, 56
    return svg(W + 24, H + 26, "".join([
        f'<rect x="12" y="6" width="{W}" height="{H}" {TAGLIO} rx="1"/>',
        f'<line x1="12" y1="{6 + H}" x2="{12 + W}" y2="{6 + H}" {VALLE}/>',
        colla(2, 6, 10, H, "INC."),
        colla(12 + W, 6, 10, H, "INC."),
        colla(12, 6 + H, W, 8, "INCOLLA SOTTO"),
        f'<text x="{12 + W / 2}" y="{6 + H / 2}" text-anchor="middle" font-size="4" '
        f'fill="#94a3b8">il lato di sopra resta aperto</text>',
        quota(12, H + 24, 12 + W, "104 mm"),
    ]))


MECCANISMI = {
    "vfold": ("Piega a V con due alette",
              "Ritaglia il rettangolo con l'aletta sotto. Piega a monte la riga blu al centro "
              "e a valle la riga arancione in fondo. Apri la pagina a 90°, appoggia la piega "
              "del pezzo sulla piega della pagina e incolla le due alette di sbieco, una per "
              "facciata, formando una V. Chiudendo il libro il pezzo si abbassa da solo."),
    "gradino": ("Gradino tagliato nella piega",
                "Piega il foglio a metà. Taglia le due righe nere partendo dalla piega, poi "
                "apri e spingi in avanti la linguetta che si è formata: diventa un gradino "
                "in rilievo. Non serve colla."),
    "volvella": ("Volvella girevole",
                 "Ritaglia il disco e la finestra. Fora il centro del disco e il foglio nello "
                 "stesso punto, unisci con un fermacampione e apri i braccetti dietro. "
                 "Girando il disco, nella finestra compare un colore per volta. "
                 "Il foro lo fa l'adulto, appoggiando il foglio su un tappetino e premendo con "
                 "la punta di una matita: non si fa con le forbici."),
    "linguetta": ("Linguetta scorrevole",
                  "Ritaglia la striscia e le due fessure nel foglio. Infila la striscia da "
                  "sotto nella prima fessura e da sopra nella seconda. Tirando la linguetta "
                  "la figura attraversa la scena."),
    "tasca": ("Tasca porta-tessere",
              "Ritaglia la tasca con le tre alette. Piega a valle la riga arancione, incolla "
              "le tre alette sul foglio e lascia aperto il lato di sopra: è lì che entrano "
              "le tessere."),
}


def fustella(t):
    m = t["meccanismo"]
    if m == "volvella":
        return fustella_volvella()
    if m == "tasca":
        return fustella_tasca()
    slug, alt = t["figura"]
    return {"vfold": fustella_vfold, "gradino": fustella_gradino,
            "linguetta": fustella_linguetta}[m](slug, alt)


# ---------------------------------------------------------------------------
# Pagine
# ---------------------------------------------------------------------------
def intestazione(tag, titolo, sottotitolo, h="h2"):
    return f"""      <header class="scheda-header">
        <div class="scheda-logo" aria-hidden="true">PC</div>
        <div class="scheda-intestazione">
          <div class="scheda-ente">Protezione Civile — Genzano di Roma</div>
          <{h} class="scheda-titolo-principale">{E(titolo)}</{h}>
          <div class="scheda-sottotitolo">{E(sottotitolo)}</div>
        </div>
      </header>
      <p class="lib-tag">{E(tag)}</p>
"""


def piede(n, tot):
    return (f'      <footer class="scheda-footer"><span class="scheda-site">'
            f'protezionecivilegenzano.it</span>\n'
            f'        <span>LIBRO-POPUP · Foglio {n} di {tot} · Rev. 1 · {REV}</span></footer>\n')


LICENZA = ('      <p class="lib-licenza">Pittogrammi: ARASAAC (arasaac.org), Governo di Aragona '
           '— autore Sergio Palao, licenza CC BY-NC-SA 4.0. Questo foglio eredita la stessa '
           'licenza.</p>\n')

TOT = len(TAVOLE) + 3


def pagina_tavola(t, n):
    nome, istruzioni = MECCANISMI[t["meccanismo"]]
    regole = "".join(f"          <li>{r}</li>\n" for r in t["regole"])
    pitto = "".join(
        f'<img src="{PITTO}/{s}.png" alt="{E(a)}" width="500" height="500">' for s, a in t["pittogrammi"])
    legenda = ""
    if t["meccanismo"] == "volvella":
        legenda = ('<table class="lib-allerta">' + "".join(
            f'<tr><td><span class="lib-all-pal" style="background:{c}"></span>{E(nome)}</td>'
            f'<td class="lib-all-che">{E(che)}</td><td>{E(fare)}</td></tr>'
            for nome, c, che, fare in ALLERTA) + "</table>\n      ")
    extra = ""
    if t["meccanismo"] == "tasca":
        extra = ('        <div class="lib-tessere">' + "".join(
            f'<div class="lib-tessera"><img src="{PITTO}/{s}.png" alt="{E(a)}" '
            f'width="500" height="500"><span>{E(a)}</span></div>' for s, a in t["tessere"]) + "</div>\n")
    return f"""  <article class="scheda-page" id="{t['id']}">
    <div class="lib">
{intestazione(f"TAVOLA {t['n']} · {t['tag']}", t["titolo"], t["sottotitolo"])}      <div class="lib-corpo">
        <div class="lib-testo">
          <p>{t['testo']}</p>
          <div class="lib-regole"><h3>Che cosa si fa</h3><ul>
{regole}          </ul></div>
        </div>
        <div class="lib-pitto" aria-hidden="true">{pitto}</div>
      </div>
      {legenda}<div class="lib-fustella">
        <div class="lib-fustella-tit">La fustella · {E(nome)}</div>
        <div class="lib-disegno">{fustella(t)}</div>
        <p class="lib-montaggio">{E(istruzioni)}</p>
      </div>
{extra}      <p class="nota-adulto">Per l'adulto: ritaglia tu le parti piccole con i bambini
      fino ai 6 anni; dai 7 possono ritagliare da seduti, sorvegliati, con forbici a punta
      arrotondata. Fonte delle frasi di questa tavola: {E(t['fonte'])} Non sostituiscono il
      piano di emergenza della scuola o dell'edificio in cui vi trovate: se un'indicazione
      ufficiale dice altro, vale quella.</p>
{LICENZA}{piede(n, TOT)}    </div>
  </article>

"""


def pagina_copertina():
    indice = "".join(
        f'<li><strong>Tavola {t["n"]}</strong> — {E(t["titolo"])}</li>' for t in TAVOLE)
    return f"""  <article class="scheda-page" id="copertina">
    <div class="lib lib-cop">
      <img class="lib-cop-logo" src="/images/logo-pc-genzano.png"
           alt="Logo del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma"
           width="400" height="400">
      <div class="lib-cop-ente">Gruppo Comunale Volontari di Protezione Civile<br>Genzano di Roma</div>
      <h1 class="lib-cop-titolo">Il libro pop-up<br>della protezione civile</h1>
      <div class="lib-cop-occhiello">Otto tavole da ritagliare, piegare e far saltare su</div>
      <p class="lib-cop-testo">Un libro da costruire con le proprie mani, per imparare che cosa
      si fa quando trema la terra, quando arriva troppa acqua, quando c'è un incendio, quando
      suona l'allarme a scuola. Ogni tavola ha una scena che si alza dalla pagina, le frasi da
      ricordare e il disegno tecnico per ritagliarla.</p>
      <div class="lib-cop-fasce">
        <div><strong>Età</strong><span>6-11 anni, con un adulto</span></div>
        <div><strong>Occorrente</strong><span>forbici, colla, un fermacampione, colori per le figure</span></div>
        <div><strong>Tempo</strong><span>una tavola per volta, 30-40 minuti</span></div>
      </div>
      <div class="lib-cop-indice"><strong>Le otto tavole</strong><ol>{indice}</ol></div>
      <p class="lib-cop-nota">Questo libro è materiale didattico del Gruppo Comunale.
      <strong>Nessun ministero, ufficio scolastico o altro ente governativo lo ha approvato,
      validato o adottato</strong>: è uno spunto per lavorare in classe o a casa, non un
      programma da seguire. Le indicazioni di autoprotezione riprendono le pagine del nostro
      sito, che citano le fonti istituzionali; dove un'indicazione ufficiale dice altro, vale
      quella. In emergenza si chiama sempre il <strong>112</strong>.</p>
{piede(1, TOT)}    </div>
  </article>

"""


def pagina_guida():
    voci = "".join(
        f'<tr><td class="lib-mec-nome">{E(n)}</td><td>{E(d)}</td></tr>'
        for n, d in MECCANISMI.values())
    return f"""  <article class="scheda-page" id="guida">
    <div class="lib">
{intestazione("PRIMA DI COMINCIARE", "Come si taglia e come si piega",
              "La legenda dei tracciati, i materiali e i quattro meccanismi del libro")}      <div class="lib-guida">
        <div class="lib-box">
          <h3>Che cosa serve</h3>
          <ul>
            <li><strong>Fogli delle tavole</strong>: cartoncino da 200-250 g/m², così la scena sta in piedi.</li>
            <li><strong>Pezzi mobili</strong>: cartoncino più sottile, 160-190 g/m².</li>
            <li><strong>Colla</strong>: stick o vinilica in poca quantità, stesa con un pennellino.</li>
            <li><strong>Un fermacampione</strong> per il disco della Tavola 1.</li>
            <li>Forbici a punta arrotondata, righello, e una penna scarica per segnare le pieghe.</li>
            <li><strong>I colori</strong>: le figure sono in bianco e nero apposta. Coloratele prima
            di ritagliare, così ogni libro viene diverso dagli altri.</li>
          </ul>
        </div>
        <div class="lib-box">
          <h3>La legenda dei tracciati</h3>
          <table class="lib-legenda">
            <tr><td><span class="tr-taglio"></span></td><td><strong>Riga nera continua</strong> — qui si taglia.</td></tr>
            <tr><td><span class="tr-monte"></span></td><td><strong>Riga blu tratteggiata</strong> — piega a monte: la cresta viene verso di te.</td></tr>
            <tr><td><span class="tr-valle"></span></td><td><strong>Riga arancione punteggiata</strong> — piega a valle: la piega va indietro.</td></tr>
            <tr><td><span class="tr-colla"></span></td><td><strong>Area a righine gialle</strong> — qui va la colla.</td></tr>
          </table>
          <p class="lib-trucco"><strong>Il trucco che cambia tutto:</strong> prima di piegare,
          appoggia il righello sulla riga e ripassala con una penna scarica. La carta si
          schiaccia e la piega viene netta invece di strapparsi.</p>
        </div>
      </div>
      <div class="lib-box lib-box-largo">
        <h3>I quattro meccanismi</h3>
        <table class="lib-mec">{voci}</table>
      </div>
      <p class="nota-adulto">Per l'adulto: le fustelle sono disegnate in millimetri veri.
      Stampa <strong>a dimensione reale</strong> (nella finestra di stampa scegli «100%» e non
      «adatta alla pagina»), altrimenti le misure non tornano e i pezzi non combaciano. Una
      tavola per volta è il ritmo giusto: montarle tutte in un pomeriggio stanca e il libro
      viene peggio.</p>
{piede(2, TOT)}    </div>
  </article>

"""


def pagina_diploma():
    return f"""  <article class="scheda-page" id="diploma">
    <div class="lib">
{intestazione("ALLA FINE", "Il diploma e il tesserino",
              "Da ritagliare quando il libro è finito e le otto tavole si aprono tutte")}      <div class="lib-diploma">
        <div class="lib-dip-bordo">
          <div class="lib-dip-occhiello">Gruppo Comunale Volontari di Protezione Civile · Genzano di Roma</div>
          <div class="lib-dip-titolo">Diploma di piccola<br>protezione civile</div>
          <p class="lib-dip-testo">Si consegna a</p>
          <div class="lib-dip-riga"></div>
          <p class="lib-dip-testo">che ha costruito il libro pop-up, ha imparato che cosa si fa
          quando trema la terra, quando arriva troppa acqua e quando c'è un incendio, e sa che
          in emergenza si chiama il <strong>112</strong>.</p>
          <div class="lib-dip-firme">
            <div><div class="lib-dip-riga"></div><span>data</span></div>
            <div><div class="lib-dip-riga"></div><span>chi ha aiutato a costruirlo</span></div>
          </div>
        </div>
      </div>
      <div class="lib-tesserino">
        <div class="lib-tess-tit">Il tesserino da tenere in tasca</div>
        <div class="lib-tess-carta">
          <div class="lib-tess-fronte">
            <strong>112</strong>
            <span>il numero unico delle emergenze</span>
          </div>
          <div class="lib-tess-retro">
            <div><strong>Dico dove sono</strong> — paese, via, numero, un posto che si riconosce.</div>
            <div><strong>Dico che cosa è successo</strong> — con parole semplici.</div>
            <div><strong>Dico se qualcuno sta male</strong> — e quante persone siamo.</div>
            <div><strong>Non chiudo</strong> finché non me lo dicono.</div>
          </div>
        </div>
        <p class="lib-tess-nota">Ritaglia lungo il bordo, piega a metà sulla riga blu e incolla
        i due <strong>rovesci</strong> l'uno sull'altro, lasciando fuori le facce stampate:
        viene un tesserino a due lati.</p>
      </div>
      <p class="nota-adulto">Per l'adulto: il diploma non certifica nulla e non ha valore
      ufficiale — è il riconoscimento di un lavoro fatto insieme, e vale esattamente per
      quello. Il tesserino riporta i quattro punti della telefonata al 112 della Tavola 8.</p>
{piede(TOT, TOT)}    </div>
  </article>

"""


# ---------------------------------------------------------------------------
CSS = """
    .scheda-page:has(> .lib) { padding: 0; }
    .lib { padding: 10mm 12mm 4mm; display: flex; flex-direction: column; min-height: 238mm; }
    .lib .scheda-header { margin-bottom: 2mm; align-items: center; }
    .lib .scheda-header .scheda-titolo-principale { font-size: 23px; line-height: 1.15; }
    .lib .scheda-header .scheda-sottotitolo { font-size: 11px; }
    .lib-tag { font-size: 9px; font-weight: 700; letter-spacing: 0.09em; text-transform: uppercase;
      color: #ea580c; margin: 0 0 2.5mm; }

    .lib-corpo { display: flex; gap: 5mm; align-items: flex-start; }
    .lib-testo { flex: 1; }
    .lib-testo p { font-size: 11.5px; line-height: 1.45; margin: 0 0 2mm; }
    .lib-regole h3 { font-size: 11px; text-transform: uppercase; letter-spacing: 0.07em;
      color: var(--scheda-blu); margin: 0 0 1.2mm; padding-bottom: 0.6mm;
      border-bottom: 1.5px solid var(--scheda-blu); }
    .lib-regole ul { margin: 0 0 0 4.5mm; padding: 0; }
    .lib-regole li { font-size: 11px; line-height: 1.35; margin-bottom: 0.9mm; }
    .lib-pitto { display: flex; flex-direction: column; gap: 2mm; flex: 0 0 22mm; }
    .lib-pitto img { width: 22mm; height: 22mm; object-fit: contain; }

    .lib-allerta { width: 100%; border-collapse: collapse; margin-top: 2.5mm; }
    .lib-allerta td { font-size: 9.5px; line-height: 1.28; padding: 0.7mm 2mm 0.7mm 0;
      vertical-align: top; border-top: 1px solid #e2e8f0; }
    .lib-allerta td:first-child { width: 26mm; font-weight: 700; white-space: nowrap; }
    .lib-all-che { width: 24mm; font-style: italic; color: #475569; }
    .lib-all-pal { display: inline-block; width: 3.5mm; height: 3.5mm; border-radius: 1px;
      border: 0.6px solid #1a1a1a; margin-right: 1.4mm; vertical-align: -0.5mm; }

    .lib-fustella { margin-top: 3mm; border: 1.4px dashed #0b3c5d; border-radius: 3px;
      padding: 2.5mm 3mm; background: #f8fafc; }
    .lib-fustella-tit { font-size: 10.5px; font-weight: 700; color: var(--scheda-blu);
      margin-bottom: 1.5mm; }
    .lib-disegno { text-align: center; background: #fff; border: 1px solid #cbd5e1;
      border-radius: 2px; padding: 2mm; }
    .lib-disegno .fust { max-width: 100%; height: auto; }
    .lib-montaggio { font-size: 10px; line-height: 1.4; margin: 1.8mm 0 0; color: #1a1a1a; }

    .lib-tessere { display: grid; grid-template-columns: repeat(7, 1fr); gap: 1.5mm; margin-top: 3mm; }
    .lib-tessera { border: 1px solid #111827; border-radius: 2px; padding: 1.5mm 0.6mm;
      text-align: center; }
    .lib-tessera img { width: 15mm; height: 15mm; object-fit: contain; }
    .lib-tessera span { display: block; font-size: 7px; font-weight: 700; line-height: 1.1;
      margin-top: 0.8mm; }

    .lib .nota-adulto { font-size: 9.5px; line-height: 1.4; margin: 3mm 0 0; }
    .lib-licenza { font-size: 8px; color: #555; margin: 1.5mm 0 0; }

    /* copertina */
    .lib-cop { text-align: center; }
    .lib-cop-logo { width: 34mm; height: 34mm; object-fit: contain; margin: 4mm auto 3mm; display: block; }
    .lib-cop-ente { font-size: 11px; font-weight: 700; letter-spacing: 0.06em;
      text-transform: uppercase; color: #ea580c; line-height: 1.3; }
    .lib-cop-titolo { font-size: 34px; font-weight: 800; color: var(--scheda-blu);
      line-height: 1.12; margin: 4mm 0 2mm; }
    .lib-cop-occhiello { display: inline-block; background: var(--scheda-blu); color: #fff;
      font-size: 12px; font-weight: 700; padding: 1.2mm 4mm; border-radius: 12px; }
    .lib-cop-testo { font-size: 12px; line-height: 1.5; max-width: 140mm; margin: 5mm auto 0; }
    .lib-cop-fasce { display: flex; gap: 3mm; justify-content: center; margin: 5mm 0 0; }
    .lib-cop-fasce > div { flex: 1; max-width: 52mm; border: 1px solid #cbd5e1; border-radius: 3px;
      padding: 2mm; }
    .lib-cop-fasce strong { display: block; font-size: 10px; color: var(--scheda-blu);
      text-transform: uppercase; letter-spacing: 0.06em; }
    .lib-cop-fasce span { font-size: 10.5px; }
    .lib-cop-indice { text-align: left; max-width: 150mm; margin: 5mm auto 0; border: 1px solid #cbd5e1;
      border-radius: 3px; padding: 2.5mm 3mm; }
    .lib-cop-indice strong { font-size: 10.5px; color: var(--scheda-blu); text-transform: uppercase;
      letter-spacing: 0.06em; }
    .lib-cop-indice ol { columns: 2; margin: 1.5mm 0 0 5mm; padding: 0; }
    .lib-cop-indice li { font-size: 10px; margin-bottom: 0.6mm; }
    .lib-cop-nota { font-size: 9.5px; line-height: 1.45; text-align: left; max-width: 150mm;
      margin: 4mm auto 0; background: #fff7ed; border-left: 3px solid #ea580c; padding: 2mm 3mm; }
    .lib-cop-loghi { display: flex; justify-content: center; gap: 8mm; margin: auto 0 0; padding-top: 4mm; }
    .lib-logo { text-align: center; }
    .lib-logo img { width: 15mm; height: 15mm; object-fit: contain; display: block; margin: 0 auto 1mm; }
    .lib-logo span { font-size: 7.5px; color: #475569; }

    /* guida */
    .lib-guida { display: flex; gap: 4mm; }
    .lib-box { flex: 1; border: 1px solid #cbd5e1; border-radius: 3px; padding: 2.5mm 3mm; }
    .lib-box-largo { margin-top: 3mm; }
    .lib-box h3 { font-size: 11px; text-transform: uppercase; letter-spacing: 0.07em;
      color: var(--scheda-blu); margin: 0 0 1.5mm; }
    .lib-box ul { margin: 0 0 0 4.5mm; padding: 0; }
    .lib-box li { font-size: 10.5px; line-height: 1.35; margin-bottom: 1mm; }
    .lib-legenda td { font-size: 10.5px; padding: 1mm 0; vertical-align: middle; }
    .lib-legenda td:first-child { width: 22mm; }
    .tr-taglio, .tr-monte, .tr-valle, .tr-colla { display: block; width: 20mm; height: 0; }
    .tr-taglio { border-top: 2px solid #111827; }
    .tr-monte { border-top: 2px dashed #0284c7; }
    .tr-valle { border-top: 2px dotted #ea580c; }
    .tr-colla { height: 4mm; background: repeating-linear-gradient(45deg, #fef3c7, #fef3c7 2px,
      #fde68a 2px, #fde68a 4px); border: 1px dashed #d97706; }
    .lib-trucco { font-size: 10px; line-height: 1.4; margin: 2mm 0 0; }
    .lib-mec td { font-size: 10.5px; line-height: 1.35; padding: 1.2mm 2mm 1.2mm 0;
      vertical-align: top; border-top: 1px solid #e2e8f0; }
    .lib-mec-nome { width: 40mm; font-weight: 700; color: var(--scheda-blu); }

    /* diploma e tesserino */
    .lib-diploma { margin-top: 2mm; }
    .lib-dip-bordo { border: 2.5px double var(--scheda-blu); border-radius: 4px; padding: 6mm;
      text-align: center; }
    .lib-dip-occhiello { font-size: 9.5px; letter-spacing: 0.07em; text-transform: uppercase;
      color: #ea580c; font-weight: 700; }
    .lib-dip-titolo { font-size: 26px; font-weight: 800; color: var(--scheda-blu);
      line-height: 1.15; margin: 3mm 0; }
    .lib-dip-testo { font-size: 11px; line-height: 1.45; margin: 2mm 0; }
    .lib-dip-riga { border-bottom: 1px solid #1a1a1a; height: 7mm; margin: 0 auto; max-width: 90mm; }
    .lib-dip-firme { display: flex; gap: 8mm; margin-top: 5mm; }
    .lib-dip-firme > div { flex: 1; }
    .lib-dip-firme span { font-size: 9px; color: #475569; }
    .lib-tesserino { margin-top: 4mm; }
    .lib-tess-tit { font-size: 11px; font-weight: 700; color: var(--scheda-blu); margin-bottom: 1.5mm; }
    .lib-tess-carta { display: flex; border: 1px solid #111827; border-radius: 2px; }
    .lib-tess-fronte { flex: 0 0 45mm; border-right: 1.5px dashed #0284c7; padding: 3mm;
      text-align: center; }
    .lib-tess-fronte strong { display: block; font-size: 30px; color: #c1121f; font-weight: 800; }
    .lib-tess-fronte span { font-size: 9px; }
    .lib-tess-retro { flex: 1; padding: 2.5mm 3mm; }
    .lib-tess-retro div { font-size: 9.5px; line-height: 1.35; margin-bottom: 0.8mm; }
    .lib-tess-nota { font-size: 9.5px; margin: 1.5mm 0 0; color: #475569; }

    .lib-indice { margin: 0 0 1rem; }
    .lib-indice a { display: inline-block; padding: 0.2rem 0.55rem; margin: 0.12rem;
      border: 1.5px solid var(--scheda-blu); border-radius: 5px; color: var(--scheda-blu);
      text-decoration: none; font-size: 0.85rem; }
    .lib-indice a:hover, .lib-indice a:focus { background: var(--scheda-blu); color: #fff;
      outline: 2px solid #ffbe2e; outline-offset: 2px; }

    @media screen and (max-width: 700px) {
      .lib { padding: 5mm 4mm; min-height: auto; }
      .lib-corpo, .lib-guida, .lib-cop-fasce, .lib-tess-carta { flex-direction: column; }
      .lib-pitto { flex-direction: row; }
      .lib-tessere { grid-template-columns: repeat(3, 1fr); }
      .lib-cop-indice ol { columns: 1; }
      .lib-cop-loghi { flex-wrap: wrap; gap: 4mm; }
      .lib-tess-fronte { border-right: none; border-bottom: 2px dashed #0284c7; }
    }
"""


def main():
    indice = " ".join(
        f'<a href="#{t["id"]}">Tavola {t["n"]}</a>' for t in TAVOLE)
    pagine = pagina_copertina() + pagina_guida()
    for i, t in enumerate(TAVOLE):
        pagine += pagina_tavola(t, i + 3)
    pagine += pagina_diploma()

    doc = f"""<!DOCTYPE html>
<html lang="it" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Scheda stampabile: Il libro pop-up della protezione civile — otto tavole da costruire</title>
  <meta name="description" content="Libro pop-up da stampare, ritagliare e montare: otto tavole che si alzano dalla pagina su terremoto, alluvione, incendio nel bosco, fumo in casa, evacuazione a scuola, zaino di emergenza e chiamata al 112. Con guida al taglio, fustelle in millimetri veri, diploma e tesserino.">
  <meta name="robots" content="index, follow">
  <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
  <link rel="stylesheet" href="/formazione/schede-stampabili/assets/scheda-print.css">
  <style>{CSS}  </style>
</head>
<body>
  <div class="scheda-toolbar no-print">
    <a href="/formazione/schede-stampabili/" aria-label="Torna alle schede">&larr; Torna alle schede</a>
    <span class="scheda-titolo">Il libro pop-up della protezione civile</span>
    <button type="button" onclick="window.print()">&#128424;&#65039; Stampa o salva come PDF</button>
  </div>
  <div class="no-print" style="max-width:21cm;margin:1.5rem auto 0;padding:0 1rem;">
    <p style="margin:0 0 0.6rem;"><strong>Undici fogli.</strong> La copertina, la guida al taglio,
    le <strong>otto tavole</strong> e il diploma. Stampa <strong>a dimensione reale</strong>
    («100%», non «adatta alla pagina»): le fustelle sono disegnate in millimetri veri e devono
    combaciare. Su cartoncino le scene stanno in piedi; su carta normale si afflosciano.</p>
    <nav class="lib-indice" aria-label="Vai alla tavola"><a href="#copertina">Copertina</a>
    <a href="#guida">Guida</a> {indice} <a href="#diploma">Diploma</a></nav>
  </div>

{pagine}</body>
</html>
"""
    DEST.parent.mkdir(parents=True, exist_ok=True)
    DEST.write_text(doc, encoding="utf-8")

    # Ogni pittogramma citato deve esistere davvero, altrimenti la pagina esce
    # con i buchi e ce ne accorgiamo solo guardandola.
    usati = set()
    for t in TAVOLE:
        usati.update(s for s, _ in t["pittogrammi"])
        if "figura" in t:
            usati.add(t["figura"][0])
        usati.update(s for s, _ in t.get("tessere", []))
    mancanti = [s for s in sorted(usati)
                if not (ROOT / "static/pittogrammi/arasaac-bn" / f"{s}.png").exists()]
    assert not mancanti, f"pittogrammi mancanti: {mancanti}"
    assert len(TAVOLE) == 8, "le tavole devono restare otto"
    print(f"scritto {len(doc)//1024} KB · {TOT} fogli · {len(usati)} pittogrammi, tutti presenti")


if __name__ == "__main__":
    main()
