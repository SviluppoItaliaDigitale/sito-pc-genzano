#!/usr/bin/env python3
"""Genera la scheda multi-foglio dell'Alfabetiere A-Z (26 fogli A4, 4 scritture)."""
import sys, html
from pathlib import Path
SCR = Path('/tmp/claude-0/-home-user-sito-pc-genzano/1f0b2c84-4e92-5a1c-8a14-ea570e3ed513/scratchpad')
sys.path.insert(0, str(SCR))
from alfabeto_dati import LETTERE
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'static/formazione/schede-stampabili/alfabetiere-az-infanzia'
OUT.mkdir(exist_ok=True)
REV = '13/09/2026'

CSS = """    /* Alfabetiere A-Z — un foglio per lettera, quattro scritture. CSS scoped .alf */
    @font-face {
      font-family: 'PC Corsivo';
      src: url('/formazione/schede-stampabili/assets/edu-cursive-400.woff2') format('woff2');
      font-weight: 400 700;
      font-style: normal;
      font-display: swap;
    }
    .alf-intro {
      max-width: 21cm; margin: 1rem auto 0; padding: 0.8rem 1.2rem;
      background: #eaf2fb; border-left: 4px solid var(--scheda-blu);
      border-radius: 0 8px 8px 0; font-size: 0.95rem; line-height: 1.55; color: #333;
    }
    .alf-lettere { margin-top: 0.6rem; display: flex; flex-wrap: wrap; gap: 0.3rem; }
    .alf-lettere a {
      display: inline-block; min-width: 2rem; text-align: center; padding: 0.25rem 0.4rem;
      border: 1px solid var(--scheda-blu); border-radius: 5px; color: var(--scheda-blu);
      text-decoration: none; font-weight: 700;
    }
    .alf-lettere a:hover, .alf-lettere a:focus { background: var(--scheda-blu); color: #fff; outline: 2px solid #ffbe2e; outline-offset: 2px; }
    .scheda-page:has(> .alf) { padding: 0; }
    .alf { padding: 10mm 13mm 4mm; display: flex; flex-direction: column; min-height: 238mm; font-size: 14.5px; }
    .alf .scheda-header { margin-bottom: 2.5mm; align-items: center; }
    .alf .scheda-header .scheda-titolo-principale { font-size: 25px; line-height: 1.15; }
    .alf .scheda-header .scheda-sottotitolo { font-size: 11.5px; }
    .alf .alf-badge {
      flex-shrink: 0; width: 44px; height: 44px; border: 3px solid var(--scheda-blu); border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 23px; font-weight: 700; color: var(--scheda-blu); margin-left: auto;
    }
    .alf section h2 {
      font-size: 12.5px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--scheda-blu);
      margin: 3mm 0 4.5mm; padding-bottom: 0.8mm; border-bottom: 2px solid var(--scheda-blu);
    }
    .alf .alf-obiettivo { font-size: 12px; color: #384755; margin: 0 0 1mm; }
    .alf .alf-disegno { text-align: center; margin: 0; }
    .alf .alf-licenza { font-size: 8px; color: #555; margin: 2mm 0 0; }
    .alf .alf-disegno img { width: 38mm; height: 38mm; object-fit: contain; }
    .alf .alf-dida { text-align: center; font-size: 13.5px; margin: 0.5mm 0 0; }
    .alf .alf-spiega {
      margin: 1.5mm auto 0; max-width: 152mm; padding: 1.5mm 3mm; font-size: 12px; line-height: 1.35;
      background: #f1f5f7; border-left: 3px solid var(--scheda-blu);
    }
    /* Riga di scrittura tipo quaderno: base continua, altezza maiuscole tratteggiata, altezza x puntinata */
    .alf .alf-riga {
      position: relative; height: 12.5mm; margin-bottom: 4.5mm;
      border-bottom: 1.4px solid #1a1a1a; border-top: 1.1px dashed #93a1af;
    }
    .alf .alf-riga::before {
      content: ""; position: absolute; left: 0; right: 0; top: 45%;
      border-top: 1px dotted #c2ccd6;
    }
    .alf .alf-riga .alf-eti {
      position: absolute; left: 0; top: -4.6mm; font-size: 9px; line-height: 1; letter-spacing: 0.04em;
      text-transform: uppercase; color: #5d6b79; background: #fff; padding-right: 2mm;
    }
    .alf .alf-riga .alf-modelli {
      position: absolute; left: 3mm; right: 2mm; bottom: 0.8mm;
      display: flex; align-items: flex-end; gap: 11mm;
      color: #b6c1cc; font-family: Verdana, Arial, sans-serif; font-size: 38px; line-height: 1;
    }
    .alf .alf-riga.alf-corsivo .alf-modelli { font-family: 'PC Corsivo', 'Segoe Script', cursive; font-size: 40px; gap: 13mm; }
    .alf .alf-riga.alf-parola .alf-modelli { gap: 0; font-size: 30px; }
    .alf .alf-riga.alf-parola.alf-corsivo .alf-modelli { font-size: 32px; }
    .alf .nota-adulto { font-size: 11px; line-height: 1.3; border-top: 1px solid #687889; padding-top: 1.5mm; margin-top: auto; }
    .alf .scheda-footer { margin-top: 2.5mm; padding-top: 2.5mm; padding-bottom: 0; font-size: 10px; }
    @media screen and (max-width: 600px) {
      .alf { padding: 1rem; min-height: 0; }
      .alf .alf-disegno img { width: 100%; max-width: 52mm; height: auto; }
      .alf .alf-riga .alf-modelli { font-size: 28px; gap: 6mm; }
      .alf .alf-riga.alf-corsivo .alf-modelli { font-size: 30px; gap: 7mm; }
    }
    @media print {
      .scheda-toolbar, .alf-intro, .no-print { display: none !important; }
      body { background: #fff; }
      .scheda-page { page-break-after: always; break-after: page; }
      .scheda-page:last-of-type { page-break-after: auto; break-after: auto; }
      .alf { min-height: 232mm; padding: 8mm 11mm 3mm; }
      .alf section { break-inside: avoid; }
      .alf .alf-spiega { background: #fff; }
      .alf .alf-riga .alf-eti { background: #fff; }
    }"""

def riga(etichetta, testo, corsivo=False, parola=False):
    cls = 'alf-riga' + (' alf-corsivo' if corsivo else '') + (' alf-parola' if parola else '')
    return (f'        <div class="{cls}"><span class="alf-eti">{etichetta}</span>'
            f'<span class="alf-modelli" aria-hidden="true">{testo}</span></div>\n')

def foglio(d, n):
    L, l = d['l'], d['l'].lower()
    parola = html.escape(d['parola'])
    spiega = (f'        <p class="alf-spiega"><strong>Che cosa vuol dire.</strong> {d["spiega"]}</p>\n' if d.get('spiega') else '')
    nota = ('Per l’adulto: leggi la consegna ad alta voce e proponi un passaggio alla volta. Prima si colora, poi si ricalca sulle lettere grigie e si continua da soli sulla riga, infine si copia la parola. '
            'Le righe grigie sono il modello: la riga di base è continua, quella in alto tratteggiata. Il corsivo si propone solo a chi lo sta già imparando. '
            + ('Questa lettera non fa parte dell’alfabeto italiano di 21 lettere. ' if d.get('ospite') else '')
            + ('La H fa parte dell’alfabeto italiano ma non ha un suono suo: si scrive in ho, hai, ha, hanno e nei gruppi ch e gh. ' if d.get('muta') else '')
            + ('Spiega la parola straniera prima di farla scrivere. ' if d.get('spiega') else '')
            + ('La parola è lunga: va bene copiarne solo la prima parte. ' if len(d['parola']) > 9 else '')
            + 'Si può anche indicare o dettare. Non si valuta la calligrafia.')
    # La licenza ARASAAC va su OGNI foglio: la scheda invita a stampare una
    # lettera alla volta, e il foglio che finisce in classe deve portarla.
    licenza = '      <p class="alf-licenza">Pittogrammi: ARASAAC (arasaac.org), Governo d\u2019Aragona \u2014 autore Sergio Palao, licenza CC BY-NC-SA 4.0. Questa scheda eredita la stessa licenza.</p>\n'
    righe = (riga('Stampatello maiuscolo', ' '.join([L] * 3))
             + riga('Stampatello minuscolo', ' '.join([l] * 3))
             + riga('Corsivo maiuscolo — solo se lo sta già imparando', ' '.join([L] * 3), corsivo=True)
             + riga('Corsivo minuscolo', ' '.join([l] * 3), corsivo=True))
    return f"""  <article class="scheda-page" id="lettera-{l}">
    <div class="alf">
      <header class="scheda-header">
        <div class="scheda-logo" aria-hidden="true">PC</div>
        <div class="scheda-intestazione">
          <div class="scheda-ente">Protezione Civile — Genzano di Roma</div>
          <{'h1' if n == 1 else 'h2'} class="scheda-titolo-principale">{L} come {parola}</{'h1' if n == 1 else 'h2'}>
          <div class="scheda-sottotitolo">Alfabetiere della sicurezza · Infanzia 5–6 anni e classe prima · 20–30 minuti · matita e colori</div>
        </div>
        <div class="alf-badge" aria-hidden="true">{L}</div>
      </header>
      <p class="alf-obiettivo"><strong>Obiettivo:</strong> riconoscere la lettera {L}, scriverla nelle quattro forme e collegarla a una parola della protezione civile.</p>
      <section>
        <h2>Colora il disegno</h2>
        <div class="alf-disegno">
          <img src="/pittogrammi/arasaac-bn/{d['img']}.png" alt="{html.escape(d['alt'], quote=True)}" width="500" height="500">
        </div>
        <p class="alf-dida">{d['dida']}</p>
{spiega}      </section>
      <section>
        <h2>Ricalca e continua: {L} {l}</h2>
{righe}      </section>
      <section>
        <h2>Copia la parola: {parola}</h2>
{riga('Stampatello', parola, parola=True)}{riga('Corsivo', parola, corsivo=True, parola=True)}      </section>
      <p class="nota-adulto">{nota}</p>
{licenza}      <footer class="scheda-footer"><span class="scheda-site">protezionecivilegenzano.it</span>
        <span>ALF-{L} · Foglio {n} di 26 · Rev. 3 · {REV}</span></footer>
    </div>
  </article>
"""

indice = ' '.join(f'<a href="#lettera-{d["l"].lower()}">{d["l"]}</a>' for d in LETTERE)
pagine = ''.join(foglio(d, i) for i, d in enumerate(LETTERE, 1))
doc = f"""<!DOCTYPE html>
<html lang="it" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Schede stampabili: Alfabetiere della sicurezza A–Z — Infanzia e classe prima</title>
  <meta name="description" content="Schede A4 stampabili: l'alfabeto dalla A alla Z, una lettera per foglio. Disegno da colorare, lettera da ricalcare in stampatello e corsivo, maiuscolo e minuscolo, e parola della protezione civile da copiare.">
  <meta name="robots" content="index, follow">
  <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
  <link rel="stylesheet" href="/formazione/schede-stampabili/assets/scheda-print.css">
  <style>
{CSS}
  </style>
</head>
<body>
  <div class="scheda-toolbar no-print">
    <a href="/formazione/schede-stampabili/">← Torna alle schede</a>
    <span class="scheda-titolo">Alfabetiere della sicurezza A–Z · un foglio per lettera</span>
    <button type="button" onclick="window.print()">Stampa o salva come PDF</button>
  </div>

  <div class="alf-intro no-print">
    <strong>Una lettera per foglio, quattro scritture.</strong> Ogni foglio ha il disegno da colorare, la lettera da ricalcare in <strong>stampatello maiuscolo e minuscolo</strong> e in <strong>corsivo maiuscolo e minuscolo</strong>, e la parola da copiare. Puoi stampare tutto l’alfabeto oppure, dalla finestra di stampa, scegliere <strong>solo le pagine</strong> che ti servono: il foglio 1 è la A, il foglio 26 è la Z. Le lettere <strong>J, K, W, X e Y</strong> non fanno parte dell’alfabeto italiano di 21 lettere: si incontrano nelle parole venute da altre lingue. La <strong>H</strong> invece c’è (si scrive in <em>ho, hai, ha, hanno</em> e nei gruppi <em>ch</em> e <em>gh</em>) ma non ha un suono suo. Dove la parola è straniera, sul foglio trovi il riquadro che la spiega in italiano. Versione riepilogo su un solo foglio: <a href="/formazione/schede-stampabili/alfabetiere-pc-infanzia/">l’alfabetiere in tabella</a>.
    <div class="alf-lettere">{indice}</div>
  </div>

{pagine}  <script>
    // Auto-stampa se chiamato con ?autoprint=1
    (function () {{
      try {{
        var params = new URLSearchParams(window.location.search);
        if (params.get('autoprint') === '1') {{ window.addEventListener('load', function () {{ setTimeout(function () {{ window.print(); }}, 400); }}); }}
      }} catch (e) {{}}
    }})();
  </script>
</body>
</html>
"""
(OUT / 'index.html').write_text(doc, encoding='utf-8')
print('scritto', len(doc) // 1024, 'KB |', doc.count('class="scheda-page"'), 'fogli |', doc.count('alf-corsivo'), 'righe corsivo')
