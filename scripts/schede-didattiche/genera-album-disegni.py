#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera i tre album di disegni da colorare (12 fogli A4 ciascuno)."""
import html, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
from disegni_dati import ALBUM

REV = "13/09/2026"
BASE = ROOT / "static/formazione/schede-stampabili"

CSS = """    .scheda-page:has(> .dis) {{ padding: 0; }}
    .dis {{ padding: 12mm 15mm 5mm; display: flex; flex-direction: column; min-height: 238mm; }}
    .dis .scheda-header {{ margin-bottom: 3mm; align-items: center; }}
    .dis .scheda-header .scheda-titolo-principale {{ font-size: 26px; line-height: 1.15; }}
    .dis .scheda-header .scheda-sottotitolo {{ font-size: 11.5px; }}
    .dis .dis-num {{
      flex-shrink: 0; width: 42px; height: 42px; border: 3px solid var(--scheda-blu); border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 19px; font-weight: 700; color: var(--scheda-blu); margin-left: auto;
    }}
    .dis .dis-quadro {{
      flex: 1; display: flex; align-items: center; justify-content: center;
      border: 2.5px solid var(--scheda-blu); border-radius: 10px; margin: 4mm 0 0; padding: 6mm;
    }}
    .dis .dis-quadro img {{ width: 100%; max-width: 128mm; height: auto; max-height: 150mm; object-fit: contain; }}
    .dis .dis-dida {{ font-size: 15px; text-align: center; margin: 4mm 0 0; color: #1a1a1a; }}
    .dis .dis-firma {{ font-size: 11px; color: #55626e; margin: 3.5mm 0 0; display: flex; gap: 3mm; align-items: baseline; }}
    .dis .dis-firma span {{ flex: 1; border-bottom: 1px solid #93a1af; }}
    .dis .nota-adulto {{ font-size: 10px; line-height: 1.45; margin: 3mm 0 0; }}
    .dis .dis-licenza {{ font-size: 8px; color: #555; margin: 2mm 0 0; }}
    .dis-indice {{ margin: 0 0 1rem; }}
    .dis-indice a {{
      display: inline-block; padding: 0.2rem 0.55rem; margin: 0.12rem; border: 1.5px solid var(--scheda-blu);
      border-radius: 5px; color: var(--scheda-blu); text-decoration: none; font-size: 0.85rem;
    }}
    .dis-indice a:hover, .dis-indice a:focus {{ background: var(--scheda-blu); color: #fff; outline: 2px solid #ffbe2e; outline-offset: 2px; }}
    @media (max-width: 700px) {{
      .dis {{ padding: 6mm 5mm; min-height: auto; }}
      .dis .dis-quadro img {{ max-width: 100%; }}
    }}
"""

def foglio(alb, f, n, tot):
    prima = n == 1
    nota = ("Per l'adulto: si colora come si vuole, non ci sono colori giusti o sbagliati. "
            "Leggi la frase sotto il disegno e lascia che il bambino racconti. "
            "Questi fogli servono a dare un nome alle cose, non a spiegare cosa fare in emergenza: "
            "per quello ci sono le schede di autoprotezione del kit. "
            "Dalla finestra di stampa puoi scegliere solo le pagine che ti servono.")
    blocco_nota = f'      <p class="nota-adulto">{nota}</p>\n' if prima else ""
    # La licenza ARASAAC va su OGNI foglio: l'album si stampa anche una pagina
    # alla volta, e il foglio che finisce in mano al bambino deve portarla.
    blocco_lic = ('      <p class="dis-licenza">Pittogrammi: ARASAAC (arasaac.org), Governo d’Aragona — '
                  'autore Sergio Palao, licenza CC BY-NC-SA 4.0. Questa scheda eredita la stessa licenza.</p>\n')
    tag = "h1" if prima else "h2"
    return f"""  <article class="scheda-page" id="foglio-{n}">
    <div class="dis">
      <header class="scheda-header">
        <div class="scheda-logo" aria-hidden="true">PC</div>
        <div class="scheda-intestazione">
          <div class="scheda-ente">Protezione Civile — Genzano di Roma</div>
          <{tag} class="scheda-titolo-principale">{html.escape(f['tit'])}</{tag}>
          <div class="scheda-sottotitolo">{alb['titolo']} · {alb['sottotitolo']}</div>
        </div>
        <div class="dis-num" aria-hidden="true">{n}</div>
      </header>
      <div class="dis-quadro">
        <img src="/pittogrammi/arasaac-bn/{f['img']}.png" alt="{html.escape(f['alt'], quote=True)}" width="500" height="500">
      </div>
      <p class="dis-dida">{html.escape(f['dida'])}</p>
      <p class="dis-firma">Colorato da <span>&nbsp;</span> il <span>&nbsp;</span></p>
{blocco_nota}{blocco_lic}      <footer class="scheda-footer"><span class="scheda-site">protezionecivilegenzano.it</span>
        <span>{alb['sigla']} · Foglio {n} di {tot} · Rev. 1 · {REV}</span></footer>
    </div>
  </article>
"""

for alb in ALBUM:
    tot = len(alb["fogli"])
    pagine = "".join(foglio(alb, f, i, tot) for i, f in enumerate(alb["fogli"], 1))
    indice = " ".join(f'<a href="#foglio-{i}">{html.escape(f["tit"])}</a>' for i, f in enumerate(alb["fogli"], 1))
    doc = f"""<!DOCTYPE html>
<html lang="it" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Scheda stampabile: {alb['titolo']} — album da colorare</title>
  <meta name="description" content="Album di {tot} fogli A4 da colorare: {alb['intro']}">
  <meta name="robots" content="index, follow">
  <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
  <link rel="stylesheet" href="/formazione/schede-stampabili/assets/scheda-print.css">
  <style>
{CSS.format()}  </style>
</head>
<body>
  <div class="no-print" style="max-width:21cm;margin:1.5rem auto 0;padding:0 1rem;">
    <p style="margin:0 0 0.6rem;"><strong>{tot} fogli, un disegno per foglio.</strong> {alb['intro']} Dalla finestra di stampa puoi scegliere <strong>solo le pagine</strong> che ti servono. Gli altri album: <a href="/formazione/schede-stampabili/">vedi l'elenco delle schede</a>.</p>
    <nav class="dis-indice" aria-label="Vai al foglio">{indice}</nav>
  </div>
{pagine}</body>
</html>
"""
    out = BASE / alb["slug"] / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    print(f"{alb['slug']}: {len(doc)//1024} KB, {tot} fogli")
