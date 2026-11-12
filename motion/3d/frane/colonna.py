#!/usr/bin/env python3
# colonna.py: completa colonna.json (musica ed effetti) per mixa.py della skill colonna-sonora. Gli istanti degli
# effetti non si scrivono a mano: si leggono dalla pagina costruita (window.EVENTI), così cadono sull'immagine.
# Non genera audio: usa la voce approvata e i suoni già in motion/.cache/suoni.
# Uso: python3 colonna.py PAGINA_COSTRUITA.html   (dopo ritmo.py e costruisci.sh)
import glob, json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
qui = Path(__file__).resolve().parent
SUONI = '../../.cache/suoni/'
pagina = Path(sys.argv[1]).resolve()
chrome = sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux*/chrome'))
with sync_playwright() as pw:
    b = pw.chromium.launch(**({'executable_path': chrome[-1]} if chrome else {}),
                           args=['--use-angle=swiftshader-webgl', '--enable-unsafe-swiftshader', '--no-sandbox'])
    p = b.new_page()
    p.goto(pagina.as_uri() + '?render=1')
    p.wait_for_function('window.__ready === true', timeout=120000)
    ev = p.evaluate('window.EVENTI')
    b.close()
(qui / 'eventi.json').write_text(json.dumps(ev, indent=1), encoding='utf-8')
col = json.load(open(qui / 'colonna.json'))
tot = col['durata']
eff = []
for a, b_, vol in ev['frane']:                       # rombo di terra e sassi su ogni movimento di frana
    eff.append({'file': SUONI + 'frana.wav', 'tipo': 'ambiente', 'inizio': round(a, 3), 'fine': round(min(b_, tot), 3),
                'entrata': 0.25, 'uscita': 0.9, 'volume': vol})
for a, b_ in ev['pioggia']:                          # la pioggia è l'ambiente delle scene bagnate
    eff.append({'file': SUONI + 'pioggia-lunga.wav', 'tipo': 'ambiente', 'inizio': round(a, 3), 'fine': round(b_, 3),
                'entrata': 1.0, 'uscita': 1.5})
colpi = [(round(t, 3), 'passaggio.wav', -2) for t in ev['passaggi']]
for t in sorted(ev['schede']):                       # un pop per scheda, mai a meno di 0,35 s da un altro colpo
    if all(abs(t - c[0]) >= 0.35 for c in colpi):
        colpi.append((round(t, 3), 'pop.wav', -3))
for t, f, vol in sorted(colpi):
    e = {'file': SUONI + f, 'tipo': 'colpo', 'volume': vol}
    e['evento' if f == 'passaggio.wav' else 'inizio'] = t
    eff.append(e)
col['effetti'] = eff
col['musica'] = [{'file': SUONI + 'on-my-way.mp3', 'inizio': 0, 'fine': tot, 'da': 0, 'entrata': 1.2, 'uscita': 3.0}]
json.dump(col, open(qui / 'colonna.json', 'w'), ensure_ascii=False, indent=1)
print(len(eff), 'effetti;', 'cartello di chiusura a', round(ev['cartello'], 2), 's')
