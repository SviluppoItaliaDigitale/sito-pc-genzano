#!/usr/bin/env python3
"""Costruisce il libro pop-up della protezione civile (scheda A4 stampabile).

Perché un generatore e non HTML scritto a mano: le tavole sono tredici e devono
essere IDENTICHE nel montaggio. Se ognuna la scrive una persona, dopo tre
tavole il disegno cambia di un millimetro, l'etichetta cambia parola, e il
bambino deve reimparare ogni volta. Qui la geometria è una funzione: cambia la
figura, non il meccanismo.

Scelta di fondo (revisione 2, 15/09/2026). La prima versione chiedeva cinque
meccanismi diversi — piega a V con due alette, gradino, volvella con
fermacampione, linguetta scorrevole, tasca — più il vocabolario dell'origami
("piega a monte", "piega a valle"), la colla, due grammature di cartoncino e la
stampa obbligatoria al 100%. Per un bambino di sette anni sono cinque lavori
diversi, non un libro.

Adesso il meccanismo è **uno solo**: il gradino tagliato nella piega. Due tagli
e una spinta. Niente colla, niente fermacampione, e soprattutto perdona la
stampa non perfetta: se il foglio esce al 96% il gradino si alza lo stesso,
mentre una piega a V con le alette fuori misura non incolla.
"""

import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from libro_popup_dati import TAVOLE

REV = "Rev. 3 · 16/09/2026"
PITTO = "/pittogrammi/arasaac-bn/"
USCITA = pathlib.Path(__file__).resolve().parents[2] / (
    "static/formazione/schede-stampabili/libro-popup-protezione-civile/index.html")

NERO, BLU, ARANCIO, GRIGIO = "#111827", "#0284c7", "#ea580c", "#64748b"

# Larghezza per carattere nel caso peggiore fra i font di sistema, a corpo 9
# (lezione delle schede esperimenti: il font non è nostro, è quello della
# macchina che stampa, e la stessa frase è larga da 4,4 a 6,0 unità).
LARGO_PEGGIORE = 6.0


def _sta(testo, corpo, spazio):
    """Verifica che una scritta centrata stia nello spazio, nel caso peggiore."""
    largo = len(testo) * LARGO_PEGGIORE * (corpo / 9)
    if largo > spazio:
        raise ValueError(f"Etichetta «{testo}» troppo larga: {largo:.0f} su {spazio} unità "
                         f"disponibili a corpo {corpo}. Accorciala.")
    return testo


def _eti(x, y, testo, corpo=2.8, colore=NERO, spazio=None, peso="bold", ancora="middle"):
    if spazio:
        _sta(testo, corpo, spazio)
    return (f'<text x="{x}" y="{y}" text-anchor="{ancora}" font-size="{corpo}" '
            f'fill="{colore}" font-weight="{peso}">{testo}</text>')


def fustella(scena_file, scena_alt, etichetta):
    """Il gradino: si ritaglia il rettangolo, si piega col disegno fuori, due tagli dalla
    piega, si ripiega col disegno dentro, si spinge da dietro.

    Geometria identica su tutte e tredici le tavole: cambia solo la figura. Le due
    righe di taglio ATTRAVERSANO la piega e sono lunghe uguali sopra e sotto: è la
    condizione perché la linguetta resti attaccata solo alle due cerniere arancioni
    e possa rovesciarsi (la prima versione le disegnava solo sotto la piega, e la
    linguetta restava inchiodata al foglio: nessuno riusciva a montarla). La figura
    sta sotto la piega, col bordo alto sulla piega: è la metà che, appoggiata sul
    tavolo, si alza in piedi davanti a chi guarda. Nessuna misura in millimetri: si
    seguono le righe stampate, quindi la stampa «adatta alla pagina» non rovina nulla.
    """
    sx, dx = 36, 72          # i due tagli
    piega = 33               # a metà del pezzo (6..60)
    alto, basso = 15, 51     # dove finiscono i tagli: 18 sopra e 18 sotto la piega
    assert alto < piega < basso and piega - alto == basso - piega, "i tagli devono attraversare la piega uguali dai due lati"
    return f'''<svg class="fust" viewBox="0 0 108 74" role="img"
     aria-label="Pezzo da ritagliare: un rettangolo con la piega a metà, due tagli che attraversano la piega e una linguetta da spingere da dietro, con sotto la piega {scena_alt.lower()}"
     xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
  <rect x="6" y="6" width="96" height="54" stroke="{NERO}" stroke-width="1" fill="none" rx="1"/>
  {_eti(54, 4.2, "RITAGLIA LUNGO QUESTA RIGA", 3, NERO, spazio=104)}
  <line x1="6" y1="{piega}" x2="102" y2="{piega}" stroke="{BLU}" stroke-width="1" stroke-dasharray="3 2"/>
  {_eti(100.5, 31.6, "piega qui", 2.3, BLU, spazio=26, peso="normal", ancora="end")}
  <line x1="{sx}" y1="{alto}" x2="{sx}" y2="{basso}" stroke="{NERO}" stroke-width="1.2"/>
  <line x1="{dx}" y1="{alto}" x2="{dx}" y2="{basso}" stroke="{NERO}" stroke-width="1.2"/>
  {_eti(sx, 13.2, "taglia", 2.3, GRIGIO, spazio=14, peso="normal")}
  {_eti(dx, 13.2, "taglia", 2.3, GRIGIO, spazio=14, peso="normal")}
  <line x1="{sx}" y1="{alto}" x2="{dx}" y2="{alto}" stroke="{ARANCIO}" stroke-width="0.9" stroke-dasharray="0.8 1.6" stroke-linecap="round"/>
  <line x1="{sx}" y1="{basso}" x2="{dx}" y2="{basso}" stroke="{ARANCIO}" stroke-width="0.9" stroke-dasharray="0.8 1.6" stroke-linecap="round"/>
  {_eti(54, 11, etichetta, 4, NERO, spazio=96)}
  {_eti(54, 22.5, "LINGUETTA", 2.6, GRIGIO, spazio=34, peso="normal")}
  {_eti(54, 26.5, "si spinge da dietro", 2.4, GRIGIO, spazio=34, peso="normal")}
  <image xlink:href="{PITTO}{scena_file}" x="41" y="{piega + 1}" width="26" height="16" preserveAspectRatio="xMidYMid meet"/>
  {_eti(54, 57.5, "questa metà si appoggia sul tavolo", 2.4, GRIGIO, spazio=96, peso="normal")}
  {_eti(54, 68, "Coloralo prima di ritagliare. Niente colla.", 3, GRIGIO, spazio=104, peso="normal")}
</svg>'''

def mini_passi():
    """I cinque passi del montaggio, disegnati. Gli stessi per ogni tavola.

    La piega è orizzontale come nelle tavole. L'ordine è quello che funziona con le
    forbici: si piega col disegno fuori (così le righe restano visibili e la piega fa
    da bordo da cui partire), si taglia dalla piega, si ripiega col disegno dentro e
    si spinge da dietro."""
    def svg(alt, corpo):
        return f'<svg viewBox="0 0 60 40" role="img" aria-label="{alt}">{corpo}</svg>'
    # 1. forbici lungo il bordo del rettangolo
    p1 = svg("Il rettangolo si ritaglia lungo il bordo nero",
             f'<rect x="8" y="8" width="44" height="26" stroke="{NERO}" stroke-width="0.9" fill="none" rx="1"/>'
             f'<line x1="8" y1="21" x2="52" y2="21" stroke="{BLU}" stroke-width="0.6" stroke-dasharray="2 1.5"/>'
             f'<circle cx="18" cy="4" r="1.8" stroke="{NERO}" stroke-width="0.6" fill="none"/><circle cx="18" cy="8.5" r="1.8" stroke="{NERO}" stroke-width="0.6" fill="none"/>'
             f'<path d="M19.6,5 L30,8 M19.6,7.5 L30,8" stroke="{NERO}" stroke-width="0.8" fill="none"/>'
             f'<path d="M34,8 l6,0 m-6,0 l1.5,-1.5 m-1.5,1.5 l1.5,1.5" stroke="{NERO}" stroke-width="0.5" fill="none"/>')
    # 2. piegato a metà con il disegno fuori: si vedono le righe e la figura
    p2 = svg("Il pezzo piegato a metà con il disegno all'esterno: la piega è il bordo in alto, sotto si vedono le due righe nere e la figura",
             f'<rect x="12" y="12" width="36" height="22" stroke="{NERO}" stroke-width="0.7" fill="#fff" rx="0.5"/>'
             f'<line x1="12" y1="12" x2="48" y2="12" stroke="{BLU}" stroke-width="1.4"/>'
             f'<line x1="24" y1="12" x2="24" y2="24" stroke="{NERO}" stroke-width="1.1"/><line x1="36" y1="12" x2="36" y2="24" stroke="{NERO}" stroke-width="1.1"/>'
             f'<line x1="24" y1="24" x2="36" y2="24" stroke="{ARANCIO}" stroke-width="0.7" stroke-dasharray="0.8 1.4"/>'
             f'<circle cx="30" cy="17.5" r="2.6" stroke="{NERO}" stroke-width="0.6" fill="none"/>'
             f'<path d="M14,9 q16,-8 32,0" stroke="{GRIGIO}" stroke-width="0.5" fill="none" stroke-dasharray="1.2 1"/>'
             f'<path d="M46,9 l-2,-1.6 m2,1.6 l-2.4,0.6" stroke="{GRIGIO}" stroke-width="0.5" fill="none"/>')
    # 3. le forbici partono dalla piega, lungo le due righe
    p3 = svg("Le forbici tagliano le due righe nere partendo dalla piega, attraverso i due strati",
             f'<rect x="12" y="12" width="36" height="22" stroke="{NERO}" stroke-width="0.7" fill="#fff" rx="0.5"/>'
             f'<line x1="12" y1="12" x2="48" y2="12" stroke="{BLU}" stroke-width="1.4"/>'
             f'<line x1="24" y1="12" x2="24" y2="24" stroke="{NERO}" stroke-width="1.1"/><line x1="36" y1="12" x2="36" y2="24" stroke="{NERO}" stroke-width="1.1"/>'
             f'<line x1="24" y1="24" x2="36" y2="24" stroke="{ARANCIO}" stroke-width="0.7" stroke-dasharray="0.8 1.4"/>'
             f'<circle cx="21" cy="3.5" r="1.8" stroke="{NERO}" stroke-width="0.6" fill="none"/><circle cx="27" cy="3.5" r="1.8" stroke="{NERO}" stroke-width="0.6" fill="none"/>'
             f'<path d="M22,5 L24,14 M26,5 L24,14" stroke="{NERO}" stroke-width="0.8" fill="none"/>'
             f'<path d="M24,26 l0,4 m0,-4 l-1.5,1.5 m1.5,-1.5 l1.5,1.5" stroke="{GRIGIO}" stroke-width="0.5" fill="none" transform="rotate(180 24 28)"/>')
    # 4. ripiegato dall'altra parte: il disegno è dentro, fuori è bianco
    p4 = svg("Il pezzo ripiegato dall'altra parte, con il disegno all'interno: fuori è bianco",
             f'<rect x="12" y="12" width="36" height="22" stroke="{NERO}" stroke-width="0.7" fill="#f1f5f9" rx="0.5"/>'
             f'<line x1="12" y1="12" x2="48" y2="12" stroke="{BLU}" stroke-width="1.4"/>'
             f'<path d="M6,30 q-6,-10 4,-18" stroke="{NERO}" stroke-width="0.6" fill="none"/><path d="M10,12 l-2.4,0.4 m2.4,-0.4 l-0.6,2.2" stroke="{NERO}" stroke-width="0.6" fill="none"/>'
             f'<path d="M54,30 q6,-10 -4,-18" stroke="{NERO}" stroke-width="0.6" fill="none"/><path d="M50,12 l2.4,0.4 m-2.4,-0.4 l0.6,2.2" stroke="{NERO}" stroke-width="0.6" fill="none"/>')
    # 5. aperto a squadra: la metà col disegno sul tavolo, la linguetta spinta da dietro sta in piedi
    p5 = svg("Il pezzo aperto a squadra: la metà con il disegno è appoggiata sul tavolo, l'altra sta in piedi, e la linguetta spinta da dietro forma un gradino con la figura in piedi",
             f'<path d="M6,36 L36,36 L54,26 L24,26 Z" stroke="{NERO}" stroke-width="0.7" fill="#fff"/>'
             f'<path d="M24,26 L24,4 L54,4 L54,26" stroke="{NERO}" stroke-width="0.7" fill="#f8fafc"/>'
             f'<path d="M14,36 L14,24 L28,24 L28,14 L44,14 L44,26" stroke="{NERO}" stroke-width="0.9" fill="#fff"/>'
             f'<path d="M14,24 L28,24 L28,14" stroke="{ARANCIO}" stroke-width="0.6" fill="none" stroke-dasharray="0.8 1.4"/>'
             f'<circle cx="21" cy="30" r="2.2" stroke="{NERO}" stroke-width="0.6" fill="none"/>'
             f'<path d="M50,10 l-6,4 m6,-4 l-2.6,0.2 m2.6,-0.2 l-0.4,2.4" stroke="{NERO}" stroke-width="0.6" fill="none"/>'
             f'<text x="46" y="36" font-size="3.2" fill="{GRIGIO}" text-anchor="middle">tavolo</text>')
    passi = [
        ("Colora e ritaglia", "Colora la figura, poi ritaglia il rettangolo lungo il bordo nero.", p1),
        ("Piega a metà, disegno fuori", "Piega sulla riga blu tenendo il disegno all'esterno. Premi la piega con l'unghia.", p2),
        ("Taglia le due righe dalla piega", "Pezzo ancora piegato: le due righe nere partono dalla piega. Tagliale, i due strati insieme, fino alla riga arancione.", p3),
        ("Ripiega, disegno dentro", "Apri e ripiega dall'altra parte, con il disegno all'interno. Premi di nuovo la piega.", p4),
        ("Spingi da dietro, poi appoggia", "Apri a metà; da dietro spingi la linguetta verso l'interno finché la sua piega si rovescia. Appoggia sul tavolo la metà col disegno: l'altra metà sta in piedi e la figura si alza.", p5),
    ]
    out = []
    for n, (tit, testo, dis) in enumerate(passi, 1):
        out.append(f'<li class="lib-passo"><div class="lib-passo-n">{n}</div>'
                   f'<div class="lib-passo-dis">{dis}</div>'
                   f'<div class="lib-passo-testo"><strong>{tit}</strong><span>{testo}</span></div></li>')
    return '<ol class="lib-passi">' + "".join(out) + '</ol>'

def intestazione(titolo, sottotitolo):
    return f'''<header class="scheda-header">
        <div class="scheda-logo" aria-hidden="true">PC</div>
        <div class="scheda-intestazione">
          <div class="scheda-ente">Protezione Civile — Genzano di Roma</div>
          <h2 class="scheda-titolo-principale">{titolo}</h2>
          <div class="scheda-sottotitolo">{sottotitolo}</div>
        </div>
      </header>'''


def piede(etichetta):
    return (f'<footer class="scheda-footer"><span class="scheda-site">protezionecivilegenzano.it</span>'
            f'<span>LIBRO-POPUP · {etichetta} · {REV}</span></footer>')


LICENZA = ('<p class="lib-licenza">Pittogrammi: ARASAAC (arasaac.org), Governo di Aragona — '
           'autore Sergio Palao, licenza CC BY-NC-SA 4.0. Questo foglio eredita la stessa licenza.</p>')


def pagina_tavola(n, t):
    regole = "".join(f"<li>{r}</li>" for r in t["regole"])
    pf, pa = t["pitto"]
    sf, sa = t["scena"]
    tessere = ""
    if t.get("tessere"):
        celle = "".join(
            f'<div class="lib-tessera"><img src="{PITTO}{f}" alt="" width="500" height="500">'
            f'<span>{nome}</span></div>' for f, nome in t["tessere"])
        tessere = (f'<div class="lib-tessere-box"><div class="lib-fustella-tit">'
                   f'Le tessere da ritagliare</div><div class="lib-tessere">{celle}</div></div>')
    return f'''
  <article class="scheda-page" id="{t["id"]}" data-scelta="{t["id"]}">
    <div class="lib">
      {intestazione(t["titolo"], t["sottotitolo"])}
      <p class="lib-tag">TAVOLA {n} · {t["tema"]}</p>
      <div class="lib-corpo">
        <div class="lib-testo">
          <p>{t["intro"]}</p>
          <div class="lib-regole"><h3>Che cosa si fa</h3><ul>{regole}</ul></div>
        </div>
        <div class="lib-pitto"><img src="{PITTO}{pf}" alt="{pa}" width="500" height="500"></div>
      </div>
      <div class="lib-fustella">
        <div class="lib-fustella-tit">Il gradino di questa tavola</div>
        <div class="lib-disegno">{fustella(sf, sa, t["scena_eti"])}</div>
        <p class="lib-montaggio"><strong>Sempre gli stessi passi, su tutte le tavole:</strong> ritaglia il
        rettangolo; piegalo sulla riga blu <strong>con il disegno fuori</strong>; taglia le due righe
        nere partendo dalla piega, i due strati insieme; ripiegalo <strong>con il disegno dentro</strong>;
        apri a metà e spingi la linguetta <strong>da dietro</strong>. Appoggia sul tavolo la metà con il
        disegno: l'altra sta in piedi e la figura si alza. Niente colla e niente misure da rispettare.</p>
      </div>
      {tessere}
      <p class="nota-adulto">Per l'adulto: fino ai 6 anni ritaglia tu; dai 7 anni ritagliano
      loro da seduti, sorvegliati, con forbici a punta arrotondata. Le frasi di questa tavola
      vengono {"dall'" if t["fonte"][0] in "aeiou" else "dalla "}{t["fonte"]}. Non sostituiscono il piano di emergenza della scuola o
      dell'edificio in cui vi trovate: se un'indicazione ufficiale dice altro, vale quella.</p>
      {LICENZA}
      {piede(f"Tavola {n} di {len(TAVOLE)}")}
    </div>
  </article>'''


def pagina_copertina():
    voci = "".join(f'<li><strong>Tavola {n}</strong> — {t["titolo"]}</li>'
                   for n, t in enumerate(TAVOLE, 1))
    return f'''
  <article class="scheda-page" id="copertina" data-scelta="copertina">
    <div class="lib lib-cop">
      <img class="lib-cop-logo" src="/images/logo-pc-genzano.png"
           alt="Logo del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma"
           width="400" height="400">
      <div class="lib-cop-ente">Gruppo Comunale Volontari di Protezione Civile<br>Genzano di Roma</div>
      <h1 class="lib-cop-titolo">Il libro pop-up<br>della protezione civile</h1>
      <div class="lib-cop-occhiello">{len(TAVOLE)} tavole da ritagliare, piegare e far saltare su</div>
      <p class="lib-cop-testo">Un libro da costruire con le proprie mani, per imparare che cosa si
      fa quando trema la terra, quando arriva troppa acqua, quando tuona, quando manca la luce,
      quando fa troppo caldo e quando suona l'allarme a scuola. Ogni tavola si monta
      <strong>allo stesso modo</strong>: due tagli e una spinta. Si impara una volta sola.</p>
      <div class="lib-cop-fasce">
        <div><strong>Età</strong><span>6-11 anni, con un adulto</span></div>
        <div><strong>Occorrente</strong><span>forbici e colori. Niente colla</span></div>
        <div><strong>Tempo</strong><span>una tavola per volta, 15-20 minuti</span></div>
      </div>
      <div class="lib-cop-indice"><strong>Le {len(TAVOLE)} tavole</strong><ol>{voci}</ol></div>
      <p class="lib-cop-nota">Questo libro è materiale didattico del Gruppo Comunale.
      <strong>Nessun ministero, ufficio scolastico o altro ente governativo lo ha approvato,
      validato o adottato</strong>: è uno spunto per lavorare in classe o a casa, non un
      programma da seguire. Le indicazioni di autoprotezione riprendono le pagine del nostro
      sito, che citano le fonti istituzionali; dove un'indicazione ufficiale dice altro, vale
      quella. In emergenza si chiama sempre il <strong>112</strong>.</p>
      {piede("Copertina")}
    </div>
  </article>'''


def pagina_guida():
    return f'''
  <article class="scheda-page" id="guida" data-scelta="guida">
    <div class="lib">
      {intestazione("Come si fa", "Cinque passi, uguali per tutte le tavole")}
      <p class="lib-tag">SI IMPARA UNA VOLTA SOLA</p>
      <p class="lib-guida-intro">Tutte le tavole di questo libro si montano nello stesso modo. Non c'è
      colla e non ci sono alette da incollare: si ritaglia, si piega con il disegno fuori, si taglia due
      volte partendo dalla piega, si ripiega con il disegno dentro, si spinge da dietro. Quando hai
      fatto la prima tavola, sai fare anche le altre.</p>
      {mini_passi()}
      <div class="lib-guida">
        <div class="lib-box">
          <h3>Che cosa serve</h3>
          <ul>
            <li><strong>Forbici</strong> a punta arrotondata.</li>
            <li><strong>Colori</strong>: le figure sono in bianco e nero apposta, così ogni libro
            viene diverso. Colora prima di ritagliare.</li>
            <li><strong>Carta</strong>: va bene quella della stampante. Su cartoncino leggero il
            gradino sta su meglio, ma non è obbligatorio.</li>
          </ul>
        </div>
        <div class="lib-box">
          <h3>Le righe del disegno</h3>
          <table class="lib-legenda">
            <tr><td><span class="tr-taglio"></span></td><td><strong>Riga nera</strong> — si taglia, partendo dalla piega: attraversa la piega, uguale sopra e sotto.</td></tr>
            <tr><td><span class="tr-monte"></span></td><td><strong>Riga blu</strong> — la piega del pezzo: prima con il disegno fuori (per tagliare), poi con il disegno dentro (per farlo stare in piedi).</td></tr>
            <tr><td><span class="tr-valle"></span></td><td><strong>Riga arancione</strong> — dove il taglio finisce: è la cerniera della linguetta.</td></tr>
          </table>
          <p class="lib-trucco"><strong>Il trucco:</strong> se la linguetta fatica a rovesciarsi,
          piegala prima avanti e indietro lungo le due righe arancioni. E prima di ogni piega passa
          l'unghia o una penna scarica sulla riga, con il righello: la carta si schiaccia e la piega
          viene dritta invece di strapparsi.</p>
        </div>
      </div>
      <div class="lib-box lib-box-largo">
        <h3>Se vuoi fare di più (facoltativo)</h3>
        <p class="lib-extra">Fai un <strong>secondo gradino più piccolo</strong> dentro alla linguetta:
        due tagli più corti, sempre partendo dalla piega e uguali sopra e sotto, e un'altra spinta da
        dietro. Vengono due scene una dietro l'altra. È lo stesso gesto di prima, quindi non c'è
        niente di nuovo da imparare.</p>
      </div>
      <p class="nota-adulto">Per l'adulto: il pezzo si ritaglia seguendo le righe stampate, non
      misure, quindi la stampa «adatta alla pagina» non rovina il lavoro e non serve impostare il
      100%. Se la linguetta non si muove, quasi sempre uno dei due tagli non attraversa la piega:
      devono essere lunghi uguali sopra e sotto, così la linguetta resta attaccata solo alle due
      cerniere arancioni. Una tavola per volta è il ritmo giusto: montarle tutte in un pomeriggio
      stanca e il libro viene peggio.</p>
      {piede("Guida")}
    </div>
  </article>'''


def pagina_diploma():
    return f'''
  <article class="scheda-page" id="diploma" data-scelta="diploma">
    <div class="lib">
      {intestazione("Il diploma e il tesserino", "Da ritagliare quando il libro è finito")}
      <p class="lib-tag">ALLA FINE</p>
      <div class="lib-diploma">
        <div class="lib-dip-bordo">
          <div class="lib-dip-occhiello">Gruppo Comunale Volontari di Protezione Civile · Genzano di Roma</div>
          <div class="lib-dip-titolo">Diploma di piccola<br>protezione civile</div>
          <p class="lib-dip-testo">Si consegna a</p>
          <div class="lib-dip-riga"></div>
          <p class="lib-dip-testo">che ha costruito il libro pop-up, ha imparato che cosa si fa
          quando trema la terra, quando arriva troppa acqua e quando c'è un incendio, e sa che in
          emergenza si chiama il <strong>112</strong>.</p>
          <div class="lib-dip-firme">
            <div><div class="lib-dip-riga"></div><span>data</span></div>
            <div><div class="lib-dip-riga"></div><span>chi ha aiutato a costruirlo</span></div>
          </div>
        </div>
      </div>
      <div class="lib-tesserino">
        <div class="lib-tess-tit">Il tesserino da tenere in tasca</div>
        <div class="lib-tess-carta">
          <div class="lib-tess-fronte"><strong>112</strong><span>il numero unico delle emergenze</span></div>
          <div class="lib-tess-retro">
            <div><strong>Dico dove sono</strong> — paese, via, numero, un posto che si riconosce.</div>
            <div><strong>Dico che cosa è successo</strong> — con parole semplici.</div>
            <div><strong>Dico se qualcuno sta male</strong> — e quante persone siamo.</div>
            <div><strong>Non chiudo</strong> finché non me lo dicono.</div>
          </div>
        </div>
        <p class="lib-tess-nota">Ritaglia lungo il bordo e piega a metà sulla riga blu, con la
        parte scritta verso l'esterno: senza colla il tesserino ha già due facce, il 112 su un
        lato e le quattro cose da dire sull'altro.</p>
      </div>
      <p class="nota-adulto">Per l'adulto: il diploma non certifica nulla e non ha valore
      ufficiale — è il riconoscimento di un lavoro fatto insieme, e vale esattamente per quello.
      Il tesserino riporta i quattro punti della telefonata al 112 dell'ultima tavola.</p>
      {piede("Diploma")}
    </div>
  </article>'''


CSS = """
    .scheda-page:has(> .lib) { padding: 0; }
    /* La banda affiliazioni (.scheda-page::after, da scheda-print.css) è un
       fratello di .lib: con il padding del foglio azzerato qui sopra andrebbe
       da un bordo all'altro della pagina invece di restare inquadrata come
       nelle altre schede. Le si restituisce lo stesso margine orizzontale
       usato dentro .lib, così il logo non tocca i bordi del foglio. */
    .scheda-page:has(> .lib)::after { margin: 3mm 12mm 0; }
    .lib { padding: 10mm 12mm 4mm; display: flex; flex-direction: column; min-height: 258mm; }
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

    .lib-fustella { margin-top: 3mm; border: 1.4px dashed #0b3c5d; border-radius: 3px;
      padding: 2.5mm 3mm; background: #f8fafc;
      /* si prende lo spazio che avanza sul foglio: un disegno grande si ritaglia
         meglio di uno piccolo, e lo spazio altrimenti resterebbe bianco. */
      flex: 1 1 auto; display: flex; flex-direction: column; min-height: 0; }
    .lib-fustella-tit { font-size: 10.5px; font-weight: 700; color: var(--scheda-blu);
      margin-bottom: 1.5mm; }
    .lib-disegno { text-align: center; background: #fff; border: 1px solid #cbd5e1;
      border-radius: 2px; padding: 2mm; flex: 1 1 0; min-height: 60mm;
      display: flex; align-items: center; justify-content: center; }
    /* nessuna misura fissa sull'SVG: si allarga fino al riquadro, così il
       disegno da ritagliare è grande quanto il foglio permette. */
    .lib-disegno .fust { width: 100%; max-width: 165mm; height: auto; }
    .lib-montaggio { font-size: 10px; line-height: 1.4; margin: 1.8mm 0 0; color: #1a1a1a; }

    /* i tre passi, uguali per tutte le tavole */
    .lib-passi { list-style: none; display: flex; gap: 4mm; margin: 3mm 0 0; padding: 0; }
    .lib-passo { flex: 1; border: 1px solid #cbd5e1; border-radius: 3px; padding: 2mm;
      display: flex; flex-direction: column; align-items: center; text-align: center; }
    .lib-passo-n { width: 7mm; height: 7mm; border-radius: 50%; background: var(--scheda-blu);
      color: #fff; font-weight: 800; font-size: 12px; line-height: 7mm; margin-bottom: 1.5mm; }
    .lib-passo-dis svg { width: 30mm; height: 20mm; }
    .lib-passo-testo strong { display: block; font-size: 10px; color: var(--scheda-blu);
      margin-top: 1mm; }
    .lib-passo-testo span { font-size: 8.8px; line-height: 1.35; }
    .lib-guida-intro { font-size: 11.5px; line-height: 1.45; margin: 0 0 1mm; }

    .lib-guida { display: flex; gap: 5mm; margin-top: 4mm; align-items: flex-start; }
    .lib-box { flex: 1; border: 1px solid #cbd5e1; border-radius: 3px; padding: 2.5mm 3mm; }
    .lib-box-largo { margin-top: 3mm; flex: 0 0 auto; }
    .lib-box h3 { font-size: 11px; text-transform: uppercase; letter-spacing: 0.07em;
      color: var(--scheda-blu); margin: 0 0 1.5mm; padding-bottom: 0.6mm;
      border-bottom: 1.5px solid var(--scheda-blu); }
    .lib-box ul { margin: 0 0 0 4.5mm; padding: 0; }
    .lib-box li { font-size: 10.5px; line-height: 1.35; margin-bottom: 0.9mm; }
    .lib-extra { font-size: 10.5px; line-height: 1.4; margin: 0; }
    .lib-legenda td { font-size: 10.5px; line-height: 1.35; padding: 1mm 2mm 1mm 0;
      vertical-align: middle; }
    .tr-taglio, .tr-monte, .tr-valle { display: block; width: 20mm; height: 0; }
    .tr-taglio { border-top: 2px solid #111827; }
    .tr-monte { border-top: 2px dashed #0284c7; }
    .tr-valle { border-top: 2px dotted #ea580c; }
    .lib-trucco { font-size: 10px; line-height: 1.4; margin: 2mm 0 0; }

    .lib-tessere-box { margin-top: 3mm; border: 1.4px dashed #0b3c5d; border-radius: 3px;
      padding: 2.5mm 3mm; background: #f8fafc; }
    .lib-tessere { display: grid; grid-template-columns: repeat(7, 1fr); gap: 1.5mm; }
    .lib-tessera { border: 1px solid #111827; border-radius: 2px; padding: 1.5mm 0.6mm;
      text-align: center; background: #fff; }
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

    /* scelta delle tavole da stampare (solo a schermo) */
    .lib-scelta { border: 2px solid var(--scheda-blu); border-radius: 6px; padding: 0.9rem 1rem;
      margin: 0 0 1rem; }
    .lib-scelta legend { font-weight: 700; color: var(--scheda-blu); padding: 0 0.4rem;
      font-size: 1rem; }
    .lib-scelta-griglia { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 0.3rem 1rem; margin: 0.4rem 0 0; }
    .lib-scelta label { display: flex; align-items: flex-start; gap: 0.45rem; font-size: 0.9rem;
      line-height: 1.3; padding: 0.15rem 0; cursor: pointer; }
    .lib-scelta input { margin-top: 0.15rem; width: 1.05rem; height: 1.05rem; flex: 0 0 auto; }
    .lib-scelta input:focus-visible { outline: 3px solid #ffbe2e; outline-offset: 2px; }
    .lib-scelta-azioni { display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center;
      margin-top: 0.8rem; padding-top: 0.6rem; border-top: 1px solid #cbd5e1; }
    .lib-scelta-azioni button { font: inherit; padding: 0.35rem 0.8rem; border-radius: 5px;
      border: 1.5px solid var(--scheda-blu); background: #fff; color: var(--scheda-blu);
      cursor: pointer; }
    .lib-scelta-azioni button.primario { background: var(--scheda-blu); color: #fff; }
    .lib-scelta-azioni button:focus-visible { outline: 3px solid #ffbe2e; outline-offset: 2px; }
    .lib-conteggio { font-size: 0.9rem; }
    .lib-esclusa { opacity: 0.4; }
    .lib-esclusa .lib { filter: grayscale(1); }

    .lib-indice { margin: 0 0 1rem; }
    .lib-indice a { display: inline-block; padding: 0.2rem 0.55rem; margin: 0.12rem;
      border: 1.5px solid var(--scheda-blu); border-radius: 5px; color: var(--scheda-blu);
      text-decoration: none; font-size: 0.85rem; }
    .lib-indice a:hover, .lib-indice a:focus { background: var(--scheda-blu); color: #fff;
      outline: 2px solid #ffbe2e; outline-offset: 2px; }

    @media print {
      .lib-esclusa { display: none !important; }
      .lib-ultima-stampata { page-break-after: auto !important; }
    }

    @media screen and (max-width: 700px) {
      .lib { padding: 5mm 4mm; min-height: auto; }
      .lib-corpo, .lib-guida, .lib-cop-fasce, .lib-tess-carta, .lib-passi { flex-direction: column; }
      .lib-pitto { flex-direction: row; }
      .lib-tessere { grid-template-columns: repeat(3, 1fr); }
      .lib-cop-indice ol { columns: 1; }
      .lib-tess-fronte { border-right: none; border-bottom: 2px dashed #0284c7; }
    }
"""

JS = """
  (function () {
    // Scelta delle tavole da stampare. Senza JavaScript non succede niente e si
    // stampa tutto: la scheda resta utilizzabile, che è il comportamento giusto
    // per un materiale che finisce in classe su computer vecchi.
    var form = document.getElementById('scelta');
    if (!form) return;
    var conteggio = document.getElementById('conteggio');

    function aggiorna() {
      var caselle = form.querySelectorAll('input[type=checkbox]');
      var scelti = 0;
      caselle.forEach(function (c) {
        var pagina = document.getElementById(c.value);
        if (!pagina) return;
        pagina.classList.toggle('lib-esclusa', !c.checked);
        if (c.checked) scelti++;
      });
      // L'ultimo foglio stampato non deve forzare un salto pagina: altrimenti
      // esce un foglio bianco in fondo.
      document.querySelectorAll('.lib-ultima-stampata').forEach(function (p) {
        p.classList.remove('lib-ultima-stampata');
      });
      var visibili = document.querySelectorAll('.scheda-page:not(.lib-esclusa)');
      if (visibili.length) visibili[visibili.length - 1].classList.add('lib-ultima-stampata');
      conteggio.textContent = scelti === 0
        ? 'Nessun foglio selezionato: non verrà stampato niente.'
        : (scelti === 1 ? 'Verrà stampato 1 foglio.' : 'Verranno stampati ' + scelti + ' fogli.');
    }

    form.addEventListener('change', aggiorna);
    document.getElementById('tutte').addEventListener('click', function () {
      form.querySelectorAll('input[type=checkbox]').forEach(function (c) { c.checked = true; });
      aggiorna();
    });
    document.getElementById('nessuna').addEventListener('click', function () {
      form.querySelectorAll('input[type=checkbox]').forEach(function (c) {
        c.checked = (c.value === 'copertina' || c.value === 'guida');
      });
      aggiorna();
    });
    document.getElementById('stampa').addEventListener('click', function () { window.print(); });
    aggiorna();
  })();
"""


def blocco_scelta():
    voci = [("copertina", "Copertina"), ("guida", "Come si fa (istruzioni)")]
    voci += [(t["id"], f'Tavola {n} — {t["titolo"]}') for n, t in enumerate(TAVOLE, 1)]
    voci += [("diploma", "Diploma e tesserino")]
    caselle = "".join(
        f'<label><input type="checkbox" value="{vid}" checked> <span>{nome}</span></label>'
        for vid, nome in voci)
    return f'''<form id="scelta" class="lib-scelta no-print">
      <fieldset style="border:0;padding:0;margin:0">
        <legend>Scegli che cosa stampare</legend>
        <p style="margin:0;font-size:0.92rem">Servono solo alcune emergenze? Togli la spunta alle
        altre: verranno stampati soltanto i fogli che hai lasciato selezionati.</p>
        <div class="lib-scelta-griglia">{caselle}</div>
        <div class="lib-scelta-azioni">
          <button type="button" id="tutte">Seleziona tutto</button>
          <button type="button" id="nessuna">Solo copertina e istruzioni</button>
          <button type="button" id="stampa" class="primario">&#128424;&#65039; Stampa o salva come PDF</button>
          <span class="lib-conteggio" id="conteggio" role="status" aria-live="polite"></span>
        </div>
      </fieldset>
    </form>'''


def main():
    pagine = [pagina_copertina(), pagina_guida()]
    pagine += [pagina_tavola(n, t) for n, t in enumerate(TAVOLE, 1)]
    pagine.append(pagina_diploma())
    totale = len(pagine)
    indice = " ".join(
        f'<a href="#{i}">{nome}</a>' for i, nome in
        [("copertina", "Copertina"), ("guida", "Come si fa")]
        + [(t["id"], f'{n}. {t["tema"].title()}') for n, t in enumerate(TAVOLE, 1)]
        + [("diploma", "Diploma")])

    html = f'''<!DOCTYPE html>
<html lang="it" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Scheda stampabile: Il libro pop-up della protezione civile — {len(TAVOLE)} tavole da costruire</title>
  <meta name="description" content="Libro pop-up da stampare, ritagliare e montare: {len(TAVOLE)} tavole su terremoto, alluvione, temporale, vento forte, incendio, caldo, blackout, gas nei posti chiusi, evacuazione a scuola, zaino di emergenza e chiamata al 112. Un solo meccanismo per tutte: due tagli e una spinta, senza colla. Si sceglie quali tavole stampare.">
  <meta name="robots" content="index, follow">
  <!-- URL preferito: la copia su GitHub Pages rimanda alla produzione. -->
  <link rel="canonical" href="https://www.protezionecivilegenzano.it/formazione/schede-stampabili/libro-popup-protezione-civile/">
  <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
  <link rel="stylesheet" href="/formazione/schede-stampabili/assets/scheda-print.css">
  <style>{CSS}</style>
</head>
<body>
  <div class="scheda-toolbar no-print">
    <a href="/formazione/schede-stampabili/" aria-label="Torna alle schede">&larr; Torna alle schede</a>
    <span class="scheda-titolo">Il libro pop-up della protezione civile</span>
    <button type="button" onclick="window.print()">&#128424;&#65039; Stampa o salva come PDF</button>
  </div>
  <div class="no-print" style="max-width:21cm;margin:1.5rem auto 0;padding:0 1rem;">
    <p style="margin:0 0 0.8rem;"><strong>{totale} fogli in tutto</strong>: la copertina, le
    istruzioni, {len(TAVOLE)} tavole e il diploma. Tutte le tavole si montano allo stesso modo —
    <strong>due tagli e una spinta, senza colla</strong> — quindi si impara una volta sola.
    Va bene la carta della stampante; su cartoncino leggero il gradino sta su meglio.</p>
    {blocco_scelta()}
    <nav class="lib-indice" aria-label="Vai al foglio">{indice}</nav>
  </div>
{"".join(pagine)}
  <script>{JS}</script>
</body>
</html>
'''
    USCITA.write_text(html, encoding="utf-8")
    print(f"Scritto {USCITA.relative_to(USCITA.parents[4])} — {totale} fogli ({len(TAVOLE)} tavole)")


if __name__ == "__main__":
    main()
