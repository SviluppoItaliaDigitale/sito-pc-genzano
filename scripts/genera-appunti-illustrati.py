#!/usr/bin/env python3
# Compone le pagine degli appunti illustrati a partire dai dati condivisi.
# Con --check confronta i risultati senza scrivere alcun file.
import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = '/formazione/schede-stampabili/'
ICONE = {
    'porta': '<path d="M6 26V3h16v23M10 26V7l8-2v21M14 16h1"/>',
    'tavolo': '<path d="M2 8h24v5H2zM5 13v13m18-13v13"/>',
    'scala': '<path d="M2 26h6v-6h6v-6h6V8h6M2 17 21 2"/>',
    'area': '<rect x="10" y="10" width="8" height="8"/><path d="m2 2 5 5M2 7h5V2m19 0-5 5m0-5v5h5M2 26l5-5m-5 0h5v5m19 0-5-5m0 5v-5h5"/>',
    'onda': '<path d="M1 15h5l3-9 5 17 4-14 3 6h6"/>',
    'mappa': '<path d="m2 6 8-3 8 3 8-3v20l-8 3-8-3-8 3zM10 3v20M18 6v20"/>',
    'casa': '<path d="m2 13 12-10 12 10M5 11v15h18V11M11 26V16h6v10"/>',
    'avviso': '<path d="m14 2 13 24H1zM14 10v8m0 3v1"/>',
    'lampada': '<path d="M9 20c0-4-5-5-5-10a10 10 0 0 1 20 0c0 5-5 6-5 10zM9 24h10M12 27h4"/>',
}

def e(value):
    return html.escape(str(value), quote=True)


def url(value):
    if not isinstance(value, str) or not value.startswith('/') or value.startswith('//'):
        raise ValueError('Occorre un percorso interno al sito.')
    return e(value)


def icona(nome):
    return '<svg class="appunti-icona" viewBox="0 0 28 28" aria-hidden="true">'+ICONE[nome]+'</svg>'


def freccia():
    return '<svg class="appunti-freccia" viewBox="0 0 48 20" aria-hidden="true"><path d="M2 12Q22 5 44 10m-9-7 9 7-10 7"/></svg>'


def link(v):
    return f'<a href="{url(v["url"])}">{e(v["testo"])}</a>'


def ricco(v):
    if isinstance(v, str):
        return e(v)
    out=[]
    for parte in v:
        if isinstance(parte, str):
            out.append(e(parte))
        else:
            c=parte['evidenza']
            if c not in ('azione','luogo','attenzione'):
                raise ValueError('Evidenziatore sconosciuto.')
            out.append(f'<strong class="evidenza-{c}">{e(parte["testo"])}</strong>')
    return ''.join(out)


def elenco(v,tag='ul',classe=''):
    return f'<{tag} class="{classe}">'+''.join('<li>'+ricco(t)+'</li>' for t in v)+f'</{tag}>'


def box(t,c,cl=''):
    return f'<section class="appunti-box {cl}"><h2>{e(t)}</h2>{c}</section>'


def errori(v):
    return box('Occhio all’errore',icona('avviso')+'<ul>'+''.join('<li><a href="'+url(x['url'])+'"><strong>'+e(x['idea'])+'</strong></a> '+e(x['correzione'])+'</li>' for x in v)+'</ul>','appunti-errori')


def concetto(p):
    return '\n'.join([
        box('In breve',''.join('<p>'+e(t)+'</p>' for t in p['in_breve'])),
        box('La sequenza','<ol>'+''.join('<li>'+icona(v['icona'])+e(v['testo'])+'</li>' for v in p['sequenza'])+'</ol>'),
        box('Cause e conseguenze','<ul class="appunti-cause">'+''.join('<li><strong>'+e(a)+'</strong>'+freccia()+'<span>'+e(b)+'</span></li>' for a,b in p['cause_conseguenze'])+'</ul>'),
        box('Chi fa cosa','<ul class="appunti-ruoli">'+''.join('<li>'+icona(v['icona'])+'<span><strong>'+e(v['ruolo'])+':</strong> '+e(v['compito'])+'</span></li>' for v in p['chi_fa_cosa'])+'</ul>'),
        box('Punto chiave','<p><strong>'+e(p['punto_chiave'])+'</strong></p>','appunti-chiave'),
        errori(p['errori']),
        box('Parole chiave','<dl>'+''.join('<div><dt><a href="'+url(v['url'])+'">'+e(v['termine'])+'</a></dt><dd>'+e(v['definizione'])+'</dd></div>' for v in p['parole_chiave'])+'</dl>','appunti-parole appunti-largo'),
        box('Per l’interrogazione',elenco(p['interrogazione'],'ol')+'<p>Rispondi a voce, scrivi oppure disegna.</p>'),
        box('Controlla a casa','<ul class="appunti-check">'+''.join('<li><span class="appunti-casella" aria-hidden="true"></span>'+e(t)+'</li>' for t in p['controlla_casa'])+'</ul>'),
    ])


def procedura(p):
    ex=p['esempio']; v=p['prova']
    return '\n'.join([
        box('La teoria','<p class="appunti-legenda">Evidenziatori: <strong class="evidenza-azione">giallo = azioni</strong>; <strong class="evidenza-luogo">azzurro = numeri e luoghi</strong>; <strong class="evidenza-attenzione">rosa = attenzione</strong>.</p>'+elenco(p['teoria']),'appunti-largo'),
        box('Le regole',elenco(p['regole']),'appunti-regole appunti-largo'),
        box('Esempio guidato','<p>'+e(ex['caso'])+'</p><ol class="appunti-passi">'+''.join('<li><p>'+e(x['spiegazione'])+'</p><p class="appunti-frase">'+e(x['azione'].strip())+'</p></li>' for x in ex['passi'])+'</ol>','appunti-largo'),
        box('Lo schema','<ol class="appunti-schema">'+''.join('<li><span>'+e(t)+'</span>'+(freccia() if i<3 else '')+'</li>' for i,t in enumerate(p['schema']))+'</ol>','appunti-largo'),
        errori(p['errori']),
        box('Prova tu','<p>'+e(v['caso'])+'</p><p>'+e(v['richiesta'])+'</p><p>'+icona('lampada')+'<strong>Indizio:</strong> '+e(v['indizio'])+'</p>'),
        box('Soluzione','<p>'+e(v['soluzione'])+'</p>','soluzione-capovolta appunti-largo'),
    ])


def genera(p):
    if not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',p['slug']):
        raise ValueError('Slug non valido.')
    if p['modello'] not in ('concetto','procedura'):
        raise ValueError('Modello non valido.')
    corpo=concetto(p) if p['modello']=='concetto' else procedura(p)
    note=''.join('<span class="appunti-nota">'+e(t)+'</span>' for t in p.get('note',[]))
    fonti=' · '.join(link(v) for v in p['fonti'])
    return f'''<!DOCTYPE html>
<html lang="it" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(p['titolo'])} — Appunti illustrati · Secondaria II</title>
  <meta name="description" content="{e(p['domanda_guida'])} Un foglio A4 di ripasso illustrato.">
  <link rel="canonical" href="https://www.protezionecivilegenzano.it{BASE}appunti-{p['slug']}-secondaria2/">
  <link rel="icon" href="/images/favicon.ico">
  <link rel="stylesheet" href="{BASE}assets/scheda-print.css">
</head>
<body>
  <nav class="scheda-toolbar no-print" aria-label="Scheda stampabile">
    <a href="{BASE}">Torna alle schede</a>
    <span>Per stampare: menu del browser → Stampa, oppure Ctrl+P / Cmd+P.</span>
  </nav>
  <article class="scheda-page">
    <link rel="stylesheet" href="{BASE}assets/appunti.css">
    <div class="appunti appunti-{p['modello']}">
      <p class="appunti-etichetta">Appunti illustrati · Protezione civile · Secondaria di II grado</p>
      <header class="appunti-testata">
        <div>
          <h1>{e(p['titolo'])}</h1>
          <svg class="appunti-pennello" viewBox="0 0 300 16" aria-hidden="true"><path d="M4 10Q100 0 295 7L287 13Q120 7 9 15Z"/></svg>
          <p class="appunti-domanda">{e(p['domanda_guida'])}</p>
          <div class="appunti-note">{note}</div>
        </div>
        <img class="appunti-apertura" src="{url(p['disegno']['percorso'])}" alt="{e(p['disegno']['alt'])}" width="600" height="360">
      </header>
      <div class="appunti-griglia">
{corpo}
      </div>
      <div class="appunti-fonti">
        <p><strong>Fonti:</strong> {fonti}.</p>
        <p>{link(p['manuale'])} · <strong>Approfondisci:</strong> {link(p['approfondisci'])}.</p>
        <p>Testi e disegni: Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma, licenza CC BY 4.0</p>
      </div>
      <footer class="scheda-footer">
        <span class="scheda-site">protezionecivilegenzano.it</span>
        <span>Appunti illustrati · Secondaria II · Rev. 16 ottobre 2026</span>
      </footer>
    </div>
  </article>
</body>
</html>
'''


def main():
    ap=argparse.ArgumentParser(description='Compone e controlla gli appunti illustrati.')
    ap.add_argument('--check',action='store_true')
    args=ap.parse_args()
    pagine=json.loads((ROOT/'data/appunti_illustrati.json').read_text(encoding='utf-8'))
    risultati=[]; slugs=set()
    for p in pagine:
        testo=genera(p)
        if p['slug'] in slugs:
            raise ValueError('Slug duplicato.')
        slugs.add(p['slug'])
        risultati.append((ROOT/'static'/BASE.lstrip('/')/f'appunti-{p["slug"]}-secondaria2/index.html',testo))
    diversi=[]
    for f,testo in risultati:
        if args.check:
            if not f.exists() or f.read_bytes()!=testo.encode('utf-8'):
                diversi.append(str(f.relative_to(ROOT)))
        else:
            f.parent.mkdir(parents=True,exist_ok=True)
            f.write_text(testo,encoding='utf-8',newline='\n')
    if diversi:
        print('Pagine non allineate:\n'+'\n'.join(diversi)); return 1
    print('Appunti illustrati: '+('verifica completata.' if args.check else 'pagine aggiornate.'))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
