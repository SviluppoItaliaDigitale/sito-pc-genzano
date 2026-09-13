#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Memory della protezione civile: 20 tessere da ritagliare (10 coppie).

Tre fogli A4:
  1. le 20 tessere con i disegni (griglia 4x5, linee di taglio)
  2. i 20 retro uguali, da incollare dietro le tessere
  3. le regole del gioco + la tabella delle coppie per l'adulto

Le illustrazioni sono pittogrammi ARASAAC in bianco e nero (autore Sergio
Palao, origine ARASAAC, CC BY-NC-SA 4.0): i bambini possono colorarle prima
di ritagliare, così ogni classe ha il suo mazzo.
"""
import html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]

REV = "13/09/2026"
DEST = ROOT / "static/formazione/schede-stampabili/memory-protezione-civile-infanzia/index.html"

# Dieci coppie di disegni DIVERSI che vanno insieme: non due volte la stessa
# immagine, ma due cose che si tengono per mano. Il bambino non abbina per
# forma, abbina per significato — ed è lì che il gioco insegna qualcosa.
COPPIE = [
 (("dis-pompiere",     "Il vigile del fuoco", "Vigile del fuoco che spegne le fiamme con la manichetta."),
  ("dis-autopompa",    "L'autopompa",         "Camion dei pompieri con la scala e il lampeggiante."),
  "Il vigile del fuoco arriva sull'autopompa."),
 (("alf-b-barella",    "La barella",          "Barella con le ruote, vista di lato."),
  ("dis-ambulanza",    "L'ambulanza",         "Ambulanza vista di lato, con la croce sul fianco."),
  "La barella sale sull'ambulanza."),
 (("dis-medico",       "Il medico",           "Medico con il camice e lo stetoscopio al collo."),
  ("alf-k-kit",        "La cassetta",         "Valigetta di pronto soccorso con la croce."),
  "Il medico apre la cassetta di pronto soccorso."),
 (("dis-elicottero",   "L'elicottero",        "Elicottero in volo, visto di lato."),
  ("alf-h-piazzola",   "La piazzola",         "Elicottero che atterra su una piazzola con la lettera H."),
  "L'elicottero atterra sulla piazzola con la H."),
 (("dis-gommone",      "Il gommone",          "Gommone con i remi, visto dall'alto."),
  ("alf-f-fiume",      "Il fiume",            "Fiume che scorre fra due rive alberate."),
  "Il gommone va sull'acqua del fiume."),
 (("dis-drone",        "Il drone",            "Drone con quattro eliche e una piccola telecamera."),
  ("alf-j-joystick",   "Il radiocomando",     "Radiocomando con la leva del joystick."),
  "Il drone si guida col radiocomando."),
 (("alf-c-casco",      "Il casco",            "Elmetto di protezione da lavoro."),
  ("alf-g-guanti",     "I guanti",            "Un paio di guanti da lavoro."),
  "Casco e guanti si mettono prima di lavorare."),
 (("alf-z-zaino",      "Lo zaino",            "Zaino con le bretelle e la tasca davanti."),
  ("dis-acqua",        "L'acqua",             "Bottiglia d'acqua accanto a un bicchiere."),
  "Nello zaino l'acqua non manca mai."),
 (("dis-volontari",    "I volontari",         "Tre volontari in divisa, uno accanto all'altro."),
  ("dis-tenda",        "La tenda",            "Tenda da campeggio chiusa, vista di lato."),
  "Sono i volontari a montare la tenda."),
 (("alf-u-uscita",     "L'uscita",            "Persona che esce da una porta aperta."),
  ("alf-l-luogo-sicuro","Il cortile",         "Cortile aperto di una scuola, con gli alberi."),
  "Si esce dalla porta e ci si ritrova in cortile."),
]

# Disposizione delle 20 tessere. Le due carte della stessa coppia non stanno
# mai vicine, così ritagliando non si vede subito che cosa va con che cosa.
# Ogni voce è (indice della coppia, 0 = prima carta / 1 = seconda).
ORDINE = [(0,0), (4,1), (7,0), (2,1),
          (9,0), (1,1), (5,0), (8,1),
          (3,0), (6,1), (0,1), (4,0),
          (7,1), (2,0), (9,1), (1,0),
          (5,1), (8,0), (3,1), (6,0)]

def tessera(i, lato):
    img, nome, alt = COPPIE[i][lato]
    return f"""        <div class="mem-tessera">
          <img src="/pittogrammi/arasaac-bn/{img}.png" alt="{html.escape(alt, quote=True)}" width="500" height="500">
          <span class="mem-nome">{html.escape(nome)}</span>
        </div>
"""

tessere = "".join(tessera(i, lato) for i, lato in ORDINE)
retri = "".join("""        <div class="mem-retro"><span class="mem-retro-logo">PC</span><span class="mem-retro-testo">Memory della<br>protezione civile</span></div>\n""" for _ in range(20))
elenco = "".join(
    f"          <li><strong>{html.escape(a[1])}</strong> e <strong>{html.escape(b[1])}</strong> — {html.escape(perche)}</li>\n"
    for a, b, perche in COPPIE)

doc = f"""<!DOCTYPE html>
<html lang="it" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Scheda stampabile: Memory della protezione civile — 20 tessere da ritagliare</title>
  <meta name="description" content="Gioco del memory da stampare e ritagliare: 20 tessere tutte diverse, che si abbinano a due a due, su mezzi e oggetti della protezione civile. Con il retro da incollare e le regole del gioco.">
  <meta name="robots" content="index, follow">
  <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
  <link rel="stylesheet" href="/formazione/schede-stampabili/assets/scheda-print.css">
  <style>
    .scheda-page:has(> .mem) {{ padding: 0; }}
    .mem {{ padding: 10mm 12mm 4mm; display: flex; flex-direction: column; min-height: 238mm; }}
    .mem .scheda-header {{ margin-bottom: 2.5mm; align-items: center; }}
    .mem .scheda-header .scheda-titolo-principale {{ font-size: 25px; line-height: 1.15; }}
    .mem .scheda-header .scheda-sottotitolo {{ font-size: 11.5px; }}
    .mem .mem-consegna {{ font-size: 11.5px; margin: 0 0 3mm; }}
    .mem .mem-griglia {{
      display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: repeat(5, 1fr);
      gap: 0; border: 1.4px dashed #6b7884; border-radius: 2px; height: 170mm;
    }}
    .mem .mem-tessera, .mem .mem-retro {{
      border: 1.4px dashed #6b7884; margin: -0.7px; display: flex; flex-direction: column;
      align-items: center; justify-content: center; padding: 2mm 1mm; break-inside: avoid; text-align: center;
    }}
    .mem .mem-tessera img {{ width: 25mm; height: 25mm; object-fit: contain; }}
    .mem .mem-nome {{ font-family: Verdana, "DejaVu Sans", sans-serif; font-size: 7.6px;
      font-weight: 700; letter-spacing: 0.02em; color: #1a1a1a; margin-top: 1mm; line-height: 1.15; }}
    .mem .mem-retro {{ background: #f2f6fa; }}
    .mem .mem-retro-logo {{ font-family: Verdana, "DejaVu Sans", sans-serif; font-weight: 700;
      font-size: 19px; color: #003366; border: 2.4px solid #003366; border-radius: 5px; padding: 1.4mm 2.6mm; }}
    .mem .mem-retro-testo {{ font-family: Verdana, "DejaVu Sans", sans-serif; font-size: 7px;
      color: #003366; margin-top: 1.4mm; line-height: 1.3; letter-spacing: 0.04em; }}
    .mem .mem-regole {{ font-size: 12.5px; }}
    .mem .mem-regole h2 {{ font-size: 12.5px; letter-spacing: 0.08em; text-transform: uppercase;
      color: var(--scheda-blu); margin: 4mm 0 2mm; padding-bottom: 0.8mm; border-bottom: 2px solid var(--scheda-blu); }}
    .mem .mem-regole ol, .mem .mem-regole ul {{ margin: 0 0 0 5mm; padding: 0; }}
    .mem .mem-regole li {{ margin-bottom: 1.4mm; }}
    .mem .mem-coppie {{ columns: 2; font-size: 12px; }}
    .mem .mem-licenza {{ font-size: 8px; color: #555; margin: 2mm 0 0; }}
    .mem .nota-adulto {{ font-size: 10px; line-height: 1.45; margin: 3mm 0 0; }}
    .mem-indice {{ margin: 0 0 1rem; }}
    .mem-indice a {{ display: inline-block; padding: 0.2rem 0.55rem; margin: 0.12rem;
      border: 1.5px solid var(--scheda-blu); border-radius: 5px; color: var(--scheda-blu);
      text-decoration: none; font-size: 0.85rem; }}
    .mem-indice a:hover, .mem-indice a:focus {{ background: var(--scheda-blu); color: #fff;
      outline: 2px solid #ffbe2e; outline-offset: 2px; }}
    @media (max-width: 700px) {{
      .mem {{ padding: 5mm 4mm; min-height: auto; }}
      .mem .mem-griglia {{ grid-template-columns: repeat(2, 1fr); grid-template-rows: none; }}
      .mem .mem-coppie {{ columns: 1; }}
    }}
  </style>
</head>
<body>
  <div class="scheda-toolbar no-print">
    <a href="/formazione/schede-stampabili/" aria-label="Torna alle schede">&larr; Torna alle schede</a>
    <span class="scheda-titolo">Memory della protezione civile: 20 tessere da ritagliare</span>
    <button type="button" onclick="window.print()">&#128424;&#65039; Stampa o salva come PDF</button>
  </div>
  <div class="no-print" style="max-width:21cm;margin:1.5rem auto 0;padding:0 1rem;">
    <p style="margin:0 0 0.6rem;"><strong>Tre fogli.</strong> Il primo ha le <strong>20 tessere</strong> da ritagliare, tutte diverse, che si abbinano a due a due (10 coppie), il secondo i <strong>20 retro</strong> uguali da incollare dietro, il terzo le <strong>regole del gioco</strong>. Stampa su cartoncino se puoi: le tessere durano di più.</p>
    <nav class="mem-indice" aria-label="Vai al foglio"><a href="#tessere">Foglio 1 — le tessere</a> <a href="#retro">Foglio 2 — il retro</a> <a href="#regole">Foglio 3 — le regole</a></nav>
  </div>

  <article class="scheda-page" id="tessere">
    <div class="mem">
      <header class="scheda-header">
        <div class="scheda-logo" aria-hidden="true">PC</div>
        <div class="scheda-intestazione">
          <div class="scheda-ente">Protezione Civile — Genzano di Roma</div>
          <h1 class="scheda-titolo-principale">Memory della protezione civile</h1>
          <div class="scheda-sottotitolo">20 tessere da ritagliare · Infanzia 4–6 anni e primaria · Preparazione 40–60 minuti, partita 15–20 · forbici, colla, colori</div>
        </div>
      </header>
      <p class="mem-consegna"><strong>Foglio 1 — le tessere.</strong> Prima colora i disegni, poi ritaglia lungo le linee tratteggiate. Vengono 20 tessere, tutte <strong>diverse</strong>: si abbinano a due a due, perché le due cose vanno insieme.</p>
      <div class="mem-griglia">
{tessere}      </div>
      <p class="nota-adulto">Per l'adulto: la preparazione delle forbici è a carico dell'adulto. A 4 anni ritaglia l'adulto mentre il bambino colora; a 5–6 anni il bambino può ritagliare da seduto, sorvegliato, con forbici a punta arrotondata, un pezzo alla volta. Stampa su cartoncino o incolla le tessere su un cartoncino riciclato: sul foglio sottile i disegni si vedono in trasparenza e il gioco non funziona. Se la classe è numerosa, stampa due copie e fai due mazzi.</p>
      <p class="mem-licenza">Pittogrammi: ARASAAC (arasaac.org), Governo d’Aragona — autore Sergio Palao, licenza CC BY-NC-SA 4.0. Questa scheda eredita la stessa licenza.</p>
      <footer class="scheda-footer"><span class="scheda-site">protezionecivilegenzano.it</span>
        <span>MEM-PC · Foglio 1 di 3 · Rev. 1 · {REV}</span></footer>
    </div>
  </article>

  <article class="scheda-page" id="retro">
    <div class="mem">
      <header class="scheda-header">
        <div class="scheda-logo" aria-hidden="true">PC</div>
        <div class="scheda-intestazione">
          <div class="scheda-ente">Protezione Civile — Genzano di Roma</div>
          <h2 class="scheda-titolo-principale">Il retro delle tessere</h2>
          <div class="scheda-sottotitolo">Memory della protezione civile · Foglio 2</div>
        </div>
      </header>
      <p class="mem-consegna"><strong>Foglio 2 — il retro.</strong> Ritaglia questi 20 riquadri e incollane uno dietro ogni tessera. Servono a rendere le tessere tutte uguali quando sono girate.</p>
      <div class="mem-griglia">
{retri}      </div>
      <p class="nota-adulto">Per l'adulto: il retro si può anche saltare, se stampi su cartoncino spesso. In quel caso gira le tessere dal lato bianco. Controlla che dal retro non si intraveda il disegno: è la sola cosa che rovina il gioco.</p>
      <footer class="scheda-footer"><span class="scheda-site">protezionecivilegenzano.it</span>
        <span>MEM-PC · Foglio 2 di 3 · Rev. 1 · {REV}</span></footer>
    </div>
  </article>

  <article class="scheda-page" id="regole">
    <div class="mem">
      <header class="scheda-header">
        <div class="scheda-logo" aria-hidden="true">PC</div>
        <div class="scheda-intestazione">
          <div class="scheda-ente">Protezione Civile — Genzano di Roma</div>
          <h2 class="scheda-titolo-principale">Come si gioca</h2>
          <div class="scheda-sottotitolo">Memory della protezione civile · Foglio 3</div>
        </div>
      </header>
      <div class="mem-regole">
        <h2>Le regole</h2>
        <ol>
          <li>Mescolate le 20 tessere e mettetele sul tavolo <strong>a faccia in giù</strong>, in quattro file da cinque.</li>
          <li>A turno si girano <strong>due tessere</strong>, una alla volta, e si dice ad alta voce che cosa c'è disegnato.</li>
          <li>Se le due cose <strong>vanno insieme</strong> è una coppia: si tiene, si dice perché, e si gioca ancora.</li>
          <li>Se non c'entrano niente l'una con l'altra si rimettono a faccia in giù, nello stesso posto, e tocca al compagno.</li>
          <li>Si finisce quando sono state trovate tutte e dieci le coppie. Vince chi ne ha di più.</li>
        </ol>
        <h2>Le dieci coppie, per l'adulto</h2>
        <ul class="mem-coppie">
{elenco}        </ul>
        <h2>Per continuare</h2>
        <ul>
          <li><strong>Con i più grandi</strong>: non basta trovare la coppia, bisogna dire <em>perché</em> le due cose stanno insieme. Se non lo si sa, lo si cerca insieme.</li>
          <li><strong>Coppie nuove</strong>: alla fine si prova a formare coppie diverse da quelle dell'elenco, spiegando l'abbinamento. Se la spiegazione sta in piedi, la coppia vale.</li>
          <li><strong>Memory parlato</strong>: chi gira la tessera la descrive senza dire il nome, gli altri indovinano.</li>
        </ul>
      </div>
      <p class="nota-adulto">Per l'adulto: le venti tessere sono tutte diverse e si abbinano per significato, non per forma: è questo che fa imparare qualcosa mentre si gioca. Tieni l'elenco delle coppie sotto gli occhi. Il gioco serve a dare un nome ai mezzi e agli oggetti e a collegarli fra loro, non a insegnare cosa fare in emergenza — per quello ci sono le schede di autoprotezione del kit. Con i bambini più piccoli comincia con <strong>sei tessere</strong> (tre coppie) e aggiungi le altre nelle partite successive. Non tenere il punteggio se il gruppo si innervosisce: si può giocare anche tutti insieme contro il tavolo, cercando di trovare tutte le coppie in squadra.</p>
      <footer class="scheda-footer"><span class="scheda-site">protezionecivilegenzano.it</span>
        <span>MEM-PC · Foglio 3 di 3 · Rev. 1 · {REV}</span></footer>
    </div>
  </article>
</body>
</html>
"""
DEST.parent.mkdir(parents=True, exist_ok=True)
DEST.write_text(doc, encoding="utf-8")
# Il gioco funziona solo se ogni coppia ha entrambe le carte, una volta sola,
# e se le venti immagini sono davvero tutte diverse.
assert sorted(ORDINE) == sorted((i, lato) for i in range(10) for lato in (0, 1)), "tessere mancanti o doppie"
immagini = [COPPIE[i][lato][0] for i, lato in ORDINE]
assert len(set(immagini)) == 20, "due tessere usano lo stesso disegno"
# nessuna coppia adiacente nella griglia 4x5, né di fianco né sopra/sotto
pos = {(i, lato): n for n, (i, lato) in enumerate(ORDINE)}
for i in range(10):
    a, b = pos[(i, 0)], pos[(i, 1)]
    ra, ca, rb, cb = a // 4, a % 4, b // 4, b % 4
    assert abs(ra - rb) + abs(ca - cb) > 1, f"coppia {i} adiacente sul foglio"
print(f"scritto {len(doc)//1024} KB | 20 tessere tutte diverse | 10 coppie complete, nessuna adiacente")
