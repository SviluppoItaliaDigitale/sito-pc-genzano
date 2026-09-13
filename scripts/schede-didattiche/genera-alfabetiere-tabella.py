#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Alfabetiere in tabella: un solo foglio A4 con tutte e 26 le lettere.

E' la versione riepilogo del quaderno "alfabetiere-az-infanzia": stesse parole,
stessi disegni, una cella per lettera. Serve come poster da appendere o come
foglio unico quando non si vuole stampare tutto il quaderno.
"""
import html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
from alfabeto_dati import LETTERE

REV = "13/09/2026"
DEST = ROOT / "static/formazione/schede-stampabili/alfabetiere-pc-infanzia/index.html"

def cella(d):
    L, l = d["l"], d["l"].lower()
    parola = html.escape(d["parola"])
    return f"""      <div class="alf-cella">
        <img class="alf-img" src="/pittogrammi/arasaac-bn/{d['img']}.png" alt="{html.escape(d['alt'], quote=True)}" width="500" height="500">
        <div class="alf-lettera">{L}<small>{l}</small></div>
        <div class="alf-parola">{parola}</div>
        <div class="alf-traccia" aria-hidden="true">{L} {L} {L}</div>
      </div>
"""

celle = "".join(cella(d) for d in LETTERE)
ospiti = ", ".join(f"<strong>{d['l']}</strong>" for d in LETTERE if d.get("ospite"))

doc = f"""<!DOCTYPE html>
<html lang="it" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Scheda stampabile: Alfabetiere della sicurezza in tabella (A–Z)</title>
  <meta name="description" content="Scheda fotocopiabile su un solo foglio: le 26 lettere dell'alfabeto, ognuna con il disegno da colorare, la parola della protezione civile e la lettera da ricalcare.">
  <meta name="robots" content="index, follow">
  <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
  <link rel="stylesheet" href="/formazione/schede-stampabili/assets/scheda-print.css">
  <style>
    .scheda-page:has(> .alfT) {{ padding: 0; }}
    .alfT {{ padding: 10mm 13mm 4mm; display: flex; flex-direction: column; min-height: 238mm; }}
    .alfT .scheda-header {{ margin-bottom: 2.5mm; align-items: center; }}
    .alfT .scheda-header .scheda-titolo-principale {{ font-size: 25px; line-height: 1.15; }}
    .alfT .scheda-header .scheda-sottotitolo {{ font-size: 11.5px; }}
    .alfT .alf-intro {{ font-size: 10px; margin: 1.5mm 0 2mm; }}
    .alfT .alf-griglia {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 1.8mm; }}
    .alfT .alf-cella {{ border: 1.3px solid #1a3a5c; border-radius: 5px; padding: 1.1mm 0.8mm 0.8mm;
      display: flex; flex-direction: column; align-items: center; text-align: center; break-inside: avoid; }}
    .alfT .alf-img {{ width: 13mm; height: 13mm; object-fit: contain; }}
    .alfT .alf-lettera {{ font-family: Verdana, "DejaVu Sans", sans-serif; font-weight: 700;
      font-size: 13.5px; line-height: 1; color: #003366; margin-top: 0.4mm; }}
    .alfT .alf-lettera small {{ font-size: 11px; color: #5a6a78; margin-left: 2px; }}
    .alfT .alf-parola {{ font-family: Verdana, "DejaVu Sans", sans-serif; font-size: 7.4px;
      font-weight: 700; letter-spacing: 0.02em; color: #1a1a1a; line-height: 1.15; margin-top: 0.4mm;
      min-height: 1.8em; display: flex; align-items: center; }}
    .alfT .alf-traccia {{ font-family: Verdana, "DejaVu Sans", sans-serif; font-size: 13px;
      letter-spacing: 0.22em; color: #c6d0da; border-bottom: 1px dashed #93a1af; width: 100%;
      margin-top: 0.6mm; line-height: 1.15; }}
    .alfT .alf-straniere {{ font-size: 8.6px; border-left: 3px solid #003366; padding: 1mm 0 1mm 2.2mm; margin: 2mm 0 0; }}
    .alfT .alf-licenza {{ font-size: 7.4px; color: #555; margin: 1.2mm 0 0; }}
    .alfT .nota-adulto {{ font-size: 10px; line-height: 1.4; margin: 2.5mm 0 0; }}
    @media (max-width: 700px) {{
      .alfT {{ padding: 5mm 4mm; }}
      .alfT .alf-griglia {{ grid-template-columns: repeat(3, 1fr); }}
    }}
  </style>
</head>
<body>
  <div class="scheda-toolbar no-print">
    <a href="/formazione/schede-stampabili/" aria-label="Torna alle schede">&larr; Torna alle schede</a>
    <span class="scheda-titolo">Alfabetiere della sicurezza: tutte le lettere su un foglio</span>
    <button type="button" onclick="window.print()">&#128424;&#65039; Stampa o salva come PDF</button>
  </div>
  <article class="scheda-page" id="alfabetiere-tabella">
    <div class="alfT">
      <header class="scheda-header">
        <div class="scheda-logo" aria-hidden="true">PC</div>
        <div class="scheda-intestazione">
          <div class="scheda-ente">Protezione Civile — Genzano di Roma</div>
          <h1 class="scheda-titolo-principale">L'alfabetiere della sicurezza</h1>
          <div class="scheda-sottotitolo">Tutte le lettere su un foglio · Infanzia 5–6 anni e classe prima · 20–30 minuti · matita e colori</div>
        </div>
      </header>
      <p class="alf-intro"><strong>Come si usa.</strong> Guarda il disegno, di' la parola ad alta voce, poi ricalca la lettera grigia. Puoi anche colorare i disegni. Per lavorare una lettera alla volta, con lo spazio per scrivere in stampatello e in corsivo, usa il quaderno <a href="/formazione/schede-stampabili/alfabetiere-az-infanzia/">A come Allerta, Z come Zaino</a>.</p>
      <div class="alf-griglia">
{celle}      </div>
      <p class="alf-straniere"><strong>Le lettere ospiti.</strong> {ospiti} non fanno parte dell’alfabeto italiano di 21 lettere: si incontrano nelle parole venute da altre lingue. La <strong>H</strong> invece c’è, ma non ha un suono suo: si scrive in <em>ho, hai, ha, hanno</em> e nei gruppi <em>ch</em> e <em>gh</em>. Sul quaderno A–Z ogni parola straniera è spiegata in italiano.</p>
      <p class="nota-adulto">Per l'adulto: si può usare come poster da appendere o come foglio di lavoro. Non si valuta la calligrafia: va bene anche indicare il disegno e dire la parola. Per i bambini che scrivono ancora poco, proponi solo le lettere del nome.</p>
      <p class="alf-licenza">Pittogrammi: ARASAAC (arasaac.org), Governo d'Aragona — autore Sergio Palao, licenza CC BY-NC-SA 4.0. Questa scheda eredita la stessa licenza.</p>
      <footer class="scheda-footer"><span class="scheda-site">protezionecivilegenzano.it</span>
        <span>ALF-TAB · Foglio unico · Rev. 3 · {REV}</span></footer>
    </div>
  </article>
</body>
</html>
"""
DEST.write_text(doc, encoding="utf-8")
print(f"scritto {len(doc)//1024} KB | {len(LETTERE)} celle")
