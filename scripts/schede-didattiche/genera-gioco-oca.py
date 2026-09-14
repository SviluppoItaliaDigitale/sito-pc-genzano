#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera il Gioco dell'oca della protezione civile (4 fogli A4).

  1. il tabellone: spirale di 56 caselle numerate, da fuori verso il centro
  2. le carte IMPREVISTO da ritagliare
  3. le carte EMERGENZA da ritagliare (domanda davanti, risposta capovolta)
  4. le regole e le pedine

La spirale è calcolata, non disegnata a mano: cambiare il numero di caselle
vuol dire cambiare COLONNE e RIGHE, e il percorso si ridispone da solo.
"""
import html, pathlib
from oca_dati import CASELLE, IMPREVISTI, EMERGENZE

REV = "13/09/2026"
ROOT = pathlib.Path(__file__).resolve().parents[2]
DEST = ROOT / "static/formazione/schede-stampabili/gioco-oca-protezione-civile/index.html"
COLONNE, RIGHE = 7, 8

# Le pedine sono i mezzi dei soccorsi, uno per giocatore. Si ritagliano e si
# piegano a metà: il disegno in alto è capovolto apposta, così una volta
# piegata la pedina sta in piedi e si vede da tutte e due le parti.
PEDINE = [
 (1, "dis-autopompa",      "Autopompa",  "Camion dei pompieri con la scala e il lampeggiante."),
 (2, "dis-ambulanza",      "Ambulanza",  "Ambulanza vista di lato, con la croce sul fianco."),
 (3, "dis-elicottero",     "Elicottero", "Elicottero in volo, visto di lato."),
 (4, "dis-aereo-soccorsi", "Aereo",      "Aereo a quattro eliche, visto di lato."),
 (5, "dis-cane",           "Cane",       "Cane seduto, con la pettorina da lavoro."),
 (6, "dis-gommone",        "Gommone",    "Gommone con i remi, visto dall'alto."),
]


def percorso_spirale(nc, nr):
    """Ordine delle celle lungo una spirale che entra verso il centro."""
    griglia = [[None] * nc for _ in range(nr)]
    su, giu, sx, dx = 0, nr - 1, 0, nc - 1
    ordine = []
    while su <= giu and sx <= dx:
        for c in range(sx, dx + 1):
            ordine.append((su, c))
        su += 1
        for r in range(su, giu + 1):
            ordine.append((r, dx))
        dx -= 1
        if su <= giu:
            for c in range(dx, sx - 1, -1):
                ordine.append((giu, c))
            giu -= 1
        if sx <= dx:
            for r in range(giu, su - 1, -1):
                ordine.append((r, sx))
            sx += 1
    return ordine

ORDINE = percorso_spirale(COLONNE, RIGHE)
assert len(ORDINE) == len(CASELLE), f"spirale da {len(ORDINE)} celle ma {len(CASELLE)} caselle"

FRECCE = {(0, 1): "\u2192", (0, -1): "\u2190", (1, 0): "\u2193", (-1, 0): "\u2191"}

def freccia(n):
    """Verso dove si va dalla casella n: senza, la spirale è illeggibile."""
    if n >= len(ORDINE):
        return ""
    (r1, c1), (r2, c2) = ORDINE[n - 1], ORDINE[n]
    return FRECCE.get((r2 - r1, c2 - c1), "")

def cella(n, tipo, etichetta, img):
    fig = (f'<img src="/pittogrammi/arasaac-bn/{img}.png" alt="" aria-hidden="true">' if img else "")
    testo = f'<span class="oca-testo">{html.escape(etichetta)}</span>' if etichetta and tipo not in ("partenza", "arrivo") else ""
    if tipo in ("partenza", "arrivo"):
        testo = f'<span class="oca-grande">{html.escape(etichetta)}</span>'
    simbolo = {"imprevisto": "?", "emergenza": "!"}.get(tipo, "")
    sim = f'<span class="oca-simbolo" aria-hidden="true">{simbolo}</span>' if simbolo else ""
    fr = freccia(n)
    frec = f'<span class="oca-freccia" aria-hidden="true">{fr}</span>' if fr else ""
    return (f'<div class="oca-cella oca-{tipo}" style="grid-area:{ORDINE[n-1][0]+1}/{ORDINE[n-1][1]+1}">'
            f'<span class="oca-num">{n}</span>{frec}{sim}{fig}{testo}</div>')

celle = "\n".join(cella(*c) for c in CASELLE)

carte_imp = "".join(
    f'<div class="oca-carta oca-carta-imp"><span class="oca-carta-tipo">Imprevisto</span>'
    f'<div class="oca-carta-corpo">'
    f'<img class="oca-carta-fig" src="/pittogrammi/arasaac-bn/{img}.png" alt="{html.escape(desc, quote=True)}">'
    f'<p class="oca-carta-fatto">{html.escape(f)}</p></div>'
    f'<p class="oca-carta-effetto">{html.escape(e)}</p></div>\n'
    for f, e, img, desc in IMPREVISTI)

carte_eme = "".join(
    f'<div class="oca-carta oca-carta-eme"><span class="oca-carta-tipo">Emergenza</span>'
    f'<p class="oca-carta-fatto">{html.escape(d)}</p>'
    f'<p class="oca-carta-sol soluzione-capovolta">{html.escape(r)}</p></div>\n'
    for d, r, _ in EMERGENZE)

fonti = "".join(f'          <li><a href="{u}">{u}</a></li>\n' for _, _, u in EMERGENZE)
fonti_uniche = "".join(f'          <li><a href="{u}">{u}</a></li>\n' for u in dict.fromkeys(u for _, _, u in EMERGENZE))

pedine = "".join(
    f'<div class="oca-pedina">'
    f'<div class="oca-pedina-lato oca-pedina-sopra">'
    f'<img src="/pittogrammi/arasaac-bn/{img}.png" alt="" aria-hidden="true">'
    f'<span class="oca-pedina-nome">{html.escape(nome)}</span>'
    f'<span class="oca-pedina-num">{n}</span></div>'
    f'<div class="oca-pedina-piega" aria-hidden="true"></div>'
    f'<div class="oca-pedina-lato">'
    f'<span class="oca-pedina-num">{n}</span>'
    f'<span class="oca-pedina-nome">{html.escape(nome)}</span>'
    f'<img src="/pittogrammi/arasaac-bn/{img}.png" alt="{html.escape("Pedina " + str(n) + ": " + desc, quote=True)}">'
    f'</div></div>\n'
    for n, img, nome, desc in PEDINE)

doc = f"""<!DOCTYPE html>
<html lang="it" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Scheda stampabile: Il gioco dell'oca della protezione civile</title>
  <meta name="description" content="Gioco dell'oca da stampare: tabellone a spirale con caselle numerate, carte imprevisto e carte emergenza da ritagliare, pedine e regole. Si gioca con un dado.">
  <meta name="robots" content="index, follow">
  <!-- URL preferito: la copia su GitHub Pages rimanda alla produzione. -->
  <link rel="canonical" href="https://www.protezionecivilegenzano.it/formazione/schede-stampabili/gioco-oca-protezione-civile/">
  <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
  <link rel="stylesheet" href="/formazione/schede-stampabili/assets/scheda-print.css">
  <style>
    .scheda-page:has(> .oca) {{ padding: 0; }}
    .oca {{ padding: 9mm 11mm 4mm; display: flex; flex-direction: column; min-height: 238mm; }}
    .oca .scheda-header {{ margin-bottom: 2.5mm; align-items: center; }}
    .oca .scheda-header .scheda-titolo-principale {{ font-size: 25px; line-height: 1.15; }}
    .oca .scheda-header .scheda-sottotitolo {{ font-size: 11.5px; }}
    .oca .oca-consegna {{ font-size: 11px; margin: 0 0 2.5mm; }}

    .oca .oca-tabellone {{
      display: grid; grid-template-columns: repeat({COLONNE}, 1fr); grid-template-rows: repeat({RIGHE}, 1fr);
      gap: 1.2mm; height: 176mm;
    }}
    .oca .oca-cella {{
      border: 1.2px solid #1a3a5c; border-radius: 3px; position: relative;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      padding: 1mm 0.6mm; text-align: center; overflow: hidden; background: #fff;
    }}
    .oca .oca-num {{
      position: absolute; top: 0.4mm; left: 0.8mm;
      font-family: Verdana, "DejaVu Sans", sans-serif; font-size: 8px; font-weight: 700; color: #003366;
    }}
    .oca .oca-freccia {{
      position: absolute; bottom: 0.3mm; right: 0.9mm;
      font-size: 11px; line-height: 1; color: #8fa0b0;
    }}
    .oca .oca-simbolo {{
      font-family: Verdana, "DejaVu Sans", sans-serif; font-size: 20px; font-weight: 700; line-height: 1;
    }}
    .oca .oca-cella img {{ width: 11mm; height: 11mm; object-fit: contain; }}
    .oca .oca-testo {{ font-size: 6.6px; line-height: 1.2; margin-top: 0.5mm; color: #1a1a1a; }}
    .oca .oca-grande {{ font-family: Verdana, "DejaVu Sans", sans-serif; font-size: 9px; font-weight: 700;
      letter-spacing: 0.06em; text-transform: uppercase; color: #003366; margin-top: 0.5mm; }}
    .oca .oca-imprevisto {{ background: #fff6e0; border-color: #b45309; }}
    .oca .oca-imprevisto .oca-simbolo {{ color: #b45309; }}
    .oca .oca-emergenza {{ background: #fdeceb; border-color: #c1121f; }}
    .oca .oca-emergenza .oca-simbolo {{ color: #c1121f; }}
    .oca .oca-avanti {{ background: #eaf6ec; border-color: #15803d; }}
    .oca .oca-fermo {{ background: #eef1f4; border-color: #55626e; }}
    .oca .oca-partenza, .oca .oca-arrivo {{ background: #e7f0fa; border-color: #003366; border-width: 2px; }}

    .oca .oca-legenda {{ display: flex; flex-wrap: wrap; gap: 2mm 5mm; font-size: 9.5px; margin: 3mm 0 0; }}
    .oca .oca-legenda span b {{ display: inline-block; width: 3.4mm; height: 3.4mm; border: 1.1px solid #1a3a5c;
      border-radius: 2px; vertical-align: -0.5mm; margin-right: 1.2mm; }}

    .oca .oca-mazzo {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2mm; }}
    .oca .oca-carta {{
      border: 1.3px dashed #6b7884; border-radius: 4px; padding: 2mm 2mm 1.4mm;
      display: flex; flex-direction: column; min-height: 46mm; break-inside: avoid;
    }}
    .oca .oca-carta-tipo {{ font-family: Verdana, "DejaVu Sans", sans-serif; font-size: 7px; font-weight: 700;
      letter-spacing: 0.1em; text-transform: uppercase; }}
    .oca .oca-carta-imp .oca-carta-tipo {{ color: #b45309; }}
    .oca .oca-carta-eme .oca-carta-tipo {{ color: #c1121f; }}
    .oca .oca-carta-corpo {{ display: flex; flex-direction: column; align-items: center; text-align: center;
      gap: 1.4mm; flex: 1; margin: 1.4mm 0 0; }}
    .oca .oca-carta-fig {{ width: 21mm; height: 21mm; object-fit: contain; flex: none; }}
    .oca .oca-carta-fatto {{ font-size: 9.5px; line-height: 1.32; margin: 0; }}
    .oca .oca-carta-eme .oca-carta-fatto {{ margin: 1.4mm 0 0; }}
    .oca .oca-carta-effetto {{ font-size: 9px; line-height: 1.3; margin: 1.4mm 0 0;
      border-top: 1px solid #c6d0da; padding-top: 1.2mm; font-weight: 700; color: #003366; }}
    .oca .oca-carta-sol {{ font-size: 8.4px; line-height: 1.3; margin: 1.4mm 0 0;
      border-top: 1px solid #c6d0da; padding-top: 1.2mm; transform: rotate(180deg); color: #384755; }}

    .oca .oca-regole {{ font-size: 11.4px; }}
    .oca .oca-regole h2 {{ font-size: 12.5px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--scheda-blu);
      margin: 3mm 0 1.6mm; padding-bottom: 0.6mm; border-bottom: 2px solid var(--scheda-blu); }}
    .oca .oca-regole ol, .oca .oca-regole ul {{ margin: 0 0 0 5mm; padding: 0; }}
    .oca .oca-fonti {{ columns: 2; column-gap: 6mm; font-size: 10.5px; }}
    .oca .oca-fonti li {{ break-inside: avoid; }}
    .oca .oca-regole li {{ margin-bottom: 1mm; }}
    .oca .oca-pedine {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 2.5mm; margin: 2mm 0 0; }}
    .oca .oca-pedina {{ border: 1.3px dashed #6b7884; border-radius: 3px; overflow: hidden; break-inside: avoid; }}
    .oca .oca-pedina-lato {{ display: flex; flex-direction: column; align-items: center; padding: 1.1mm 0.8mm; }}
    .oca .oca-pedina-sopra {{ transform: rotate(180deg); }}
    .oca .oca-pedina img {{ width: 10.5mm; height: 10.5mm; object-fit: contain; }}
    .oca .oca-pedina-nome {{ font-family: Verdana, "DejaVu Sans", sans-serif; font-size: 7px;
      font-weight: 700; color: #1a1a1a; margin-top: 0.6mm; line-height: 1.1; text-align: center; }}
    .oca .oca-pedina-num {{ font-family: Verdana, "DejaVu Sans", sans-serif; font-size: 11px;
      font-weight: 700; color: #003366; line-height: 1; }}
    .oca .oca-pedina-piega {{ border-top: 1.1px dashed #93a1af; margin: 0 1mm; }}
    .oca .nota-adulto {{ font-size: 10px; line-height: 1.45; margin: 3mm 0 0; }}
    .oca .oca-licenza {{ font-size: 7.6px; color: #555; margin: 1.6mm 0 0; }}
    .oca-indice {{ margin: 0 0 1rem; }}
    .oca-indice a {{ display: inline-block; padding: 0.2rem 0.55rem; margin: 0.12rem;
      border: 1.5px solid var(--scheda-blu); border-radius: 5px; color: var(--scheda-blu);
      text-decoration: none; font-size: 0.85rem; }}
    .oca-indice a:hover, .oca-indice a:focus {{ background: var(--scheda-blu); color: #fff;
      outline: 2px solid #ffbe2e; outline-offset: 2px; }}
    @media (max-width: 700px) {{
      .oca {{ padding: 5mm 4mm; min-height: auto; }}
      .oca .oca-tabellone {{ height: auto; grid-auto-rows: 18mm; }}
      .oca .oca-mazzo {{ grid-template-columns: repeat(2, 1fr); }}
      .oca .oca-pedine {{ grid-template-columns: repeat(3, 1fr); }}
    }}
  </style>
</head>
<body>
  <div class="scheda-toolbar no-print">
    <a href="/formazione/schede-stampabili/" aria-label="Torna alle schede">&larr; Torna alle schede</a>
    <span class="scheda-titolo">Il gioco dell'oca della protezione civile</span>
    <button type="button" onclick="window.print()">&#128424;&#65039; Stampa o salva come PDF</button>
  </div>
  <div class="no-print" style="max-width:21cm;margin:1.5rem auto 0;padding:0 1rem;">
    <p style="margin:0 0 0.6rem;"><strong>Quattro fogli.</strong> Il tabellone, le carte imprevisto, le carte emergenza e le regole con le pedine. Serve un dado. Stampa su cartoncino le due pagine delle carte, oppure incolla i ritagli su un cartoncino riciclato.</p>
    <nav class="oca-indice" aria-label="Vai al foglio"><a href="#tabellone">Foglio 1 — il tabellone</a> <a href="#imprevisti">Foglio 2 — gli imprevisti</a> <a href="#emergenze">Foglio 3 — le emergenze</a> <a href="#regole">Foglio 4 — le regole</a></nav>
  </div>

  <article class="scheda-page" id="tabellone">
    <div class="oca">
      <header class="scheda-header">
        <div class="scheda-logo" aria-hidden="true">PC</div>
        <div class="scheda-intestazione">
          <div class="scheda-ente">Protezione Civile — Genzano di Roma</div>
          <h1 class="scheda-titolo-principale">Il gioco dell'oca della protezione civile</h1>
          <div class="scheda-sottotitolo">Tabellone · Primaria e secondaria di primo grado · una partita 30–40 minuti · un dado e una pedina a testa</div>
        </div>
      </header>
      <p class="oca-consegna"><strong>Foglio 1 — il tabellone.</strong> Si parte dalla casella 1, in alto a sinistra, e si va verso il centro seguendo i numeri. Chi arriva per primo alla casella 56 ha finito.</p>
      <div class="oca-tabellone">
{celle}
      </div>
      <div class="oca-legenda">
        <span><b style="background:#fff6e0;border-color:#b45309"></b>Casella imprevisto: peschi una carta</span>
        <span><b style="background:#fdeceb;border-color:#c1121f"></b>Casella emergenza: peschi una carta e rispondi</span>
        <span><b style="background:#eaf6ec;border-color:#15803d"></b>Casella verde: fai quello che c'è scritto, ti aiuta</span>
        <span><b style="background:#eef1f4;border-color:#55626e"></b>Casella grigia: ti rallenta</span>
      </div>
      <p class="oca-licenza">Pittogrammi: ARASAAC (arasaac.org), Governo d'Aragona — autore Sergio Palao, licenza CC BY-NC-SA 4.0. Questa scheda eredita la stessa licenza.</p>
      <footer class="scheda-footer"><span class="scheda-site">protezionecivilegenzano.it</span>
        <span>OCA-PC · Foglio 1 di 4 · Rev. 1 · {REV}</span></footer>
    </div>
  </article>

  <article class="scheda-page" id="imprevisti">
    <div class="oca">
      <header class="scheda-header">
        <div class="scheda-logo" aria-hidden="true">PC</div>
        <div class="scheda-intestazione">
          <div class="scheda-ente">Protezione Civile — Genzano di Roma</div>
          <h2 class="scheda-titolo-principale">Le carte imprevisto</h2>
          <div class="scheda-sottotitolo">Il gioco dell'oca della protezione civile · Foglio 2</div>
        </div>
      </header>
      <p class="oca-consegna"><strong>Foglio 2 — gli imprevisti.</strong> Ritaglia le carte e mettile in un mazzo, a faccia in giù, accanto al tabellone. Sono le cose che capitano: alcune aiutano, altre rallentano.</p>
      <div class="oca-mazzo">
{carte_imp}      </div>
      <p class="nota-adulto">Per l'adulto: il ritaglio è a carico tuo con i più piccoli; dalla terza primaria i bambini possono ritagliare da seduti, sorvegliati, con forbici a punta arrotondata. Le carte si leggono ad alta voce: è lì che il gioco insegna, non nel punteggio. Il disegno su ogni carta serve a chi ancora non legge: prima di leggere, chiedi che cosa vede.</p>
      <p class="oca-licenza">Pittogrammi: ARASAAC (arasaac.org), Governo d'Aragona — autore Sergio Palao, licenza CC BY-NC-SA 4.0. Questa scheda eredita la stessa licenza.</p>
      <footer class="scheda-footer"><span class="scheda-site">protezionecivilegenzano.it</span>
        <span>OCA-PC · Foglio 2 di 4 · Rev. 1 · {REV}</span></footer>
    </div>
  </article>

  <article class="scheda-page" id="emergenze">
    <div class="oca">
      <header class="scheda-header">
        <div class="scheda-logo" aria-hidden="true">PC</div>
        <div class="scheda-intestazione">
          <div class="scheda-ente">Protezione Civile — Genzano di Roma</div>
          <h2 class="scheda-titolo-principale">Le carte emergenza</h2>
          <div class="scheda-sottotitolo">Il gioco dell'oca della protezione civile · Foglio 3</div>
        </div>
      </header>
      <p class="oca-consegna"><strong>Foglio 3 — le emergenze.</strong> Ritaglia le carte e fanne un secondo mazzo. Sopra c'è la domanda, sotto la risposta scritta al contrario: si legge solo dopo aver risposto, girando la carta.</p>
      <div class="oca-mazzo">
{carte_eme}      </div>
      <p class="nota-adulto">Per l'adulto: Il ritaglio è a carico tuo con i più piccoli; dalla terza primaria i bambini possono ritagliare da seduti, sorvegliati, con forbici a punta arrotondata. Le risposte seguono le indicazioni del Dipartimento della Protezione Civile e le pagine di autoprotezione del sito, elencate nelle regole. Chi non sa rispondere non viene mandato indietro: si legge insieme la risposta e si prosegue. Sbagliare qui serve a imparare, non a perdere.</p>
      <footer class="scheda-footer"><span class="scheda-site">protezionecivilegenzano.it</span>
        <span>OCA-PC · Foglio 3 di 4 · Rev. 1 · {REV}</span></footer>
    </div>
  </article>

  <article class="scheda-page" id="regole">
    <div class="oca">
      <header class="scheda-header">
        <div class="scheda-logo" aria-hidden="true">PC</div>
        <div class="scheda-intestazione">
          <div class="scheda-ente">Protezione Civile — Genzano di Roma</div>
          <h2 class="scheda-titolo-principale">Come si gioca</h2>
          <div class="scheda-sottotitolo">Il gioco dell'oca della protezione civile · Foglio 4</div>
        </div>
      </header>
      <div class="oca-regole">
        <h2>Le regole</h2>
        <ol>
          <li>Si gioca in due o più, con <strong>un dado</strong> e una pedina a testa. Tutti partono dalla casella 1.</li>
          <li>A turno si tira il dado e si avanza di tante caselle quanto il numero uscito.</li>
          <li>Se arrivi su una <strong>casella verde o grigia</strong>, fai quello che c'è scritto.</li>
          <li>Se arrivi su una <strong>casella imprevisto</strong>, peschi una carta, la leggi ad alta voce e fai quello che dice.</li>
          <li>Se arrivi su una <strong>casella emergenza</strong>, peschi una carta e rispondi alla domanda. Se la risposta è giusta <strong>avanzi di 3</strong>. Se non lo è, si legge insieme la risposta girando la carta e <strong>resti dove sei</strong>: nessuno torna indietro per non aver saputo una cosa.</li>
          <li>Vince chi arriva per primo alla casella 56. Con il numero esatto non serve: basta arrivarci o superarla.</li>
        </ol>
        <h2>Le pedine</h2>
        <p style="margin:0 0 1.5mm;">Ogni giocatore sceglie il suo mezzo. Colora la pedina, ritagliala lungo il bordo e <strong>piegala a metà</strong> sulla linea tratteggiata: sta in piedi da sola e si vede da tutte e due le parti.</p>
        <div class="oca-pedine">
{pedine}        </div>
        <h2>Da dove vengono le risposte</h2>
        <ul class="oca-fonti">
{fonti_uniche}        </ul>
      </div>
      <p class="nota-adulto">Per l'adulto: Il ritaglio è a carico tuo con i più piccoli; dalla terza primaria i bambini possono ritagliare da seduti, sorvegliati, con forbici a punta arrotondata. Una partita dura 30–40 minuti, ma si può fermare prima e riprendere. Con i più piccoli gioca insieme a loro e leggi tu le carte. Il gioco serve a far dire ad alta voce i comportamenti giusti: quando qualcuno risponde bene, chiedi anche <em>perché</em>. Le risposte complete, con il prima, il durante e il dopo, sono nelle pagine elencate qui sopra: il gioco le richiama, non le sostituisce.</p>
      <p class="oca-licenza">Pittogrammi: ARASAAC (arasaac.org), Governo d'Aragona — autore Sergio Palao, licenza CC BY-NC-SA 4.0. Questa scheda eredita la stessa licenza.</p>
      <footer class="scheda-footer"><span class="scheda-site">protezionecivilegenzano.it</span>
        <span>OCA-PC · Foglio 4 di 4 · Rev. 1 · {REV}</span></footer>
    </div>
  </article>
</body>
</html>
"""
DEST.parent.mkdir(parents=True, exist_ok=True)
DEST.write_text(doc, encoding="utf-8")
print(f"scritto {len(doc)//1024} KB | {len(CASELLE)} caselle in spirale {COLONNE}x{RIGHE} | "
      f"{len(IMPREVISTI)} imprevisti | {len(EMERGENZE)} emergenze")
