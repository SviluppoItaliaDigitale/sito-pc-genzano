#!/usr/bin/env python3
# ritmo.py: dai tempi delle parole (parole.json, voce già approvata) calcola le scene del video 3D, che durano più
# della frase per lasciare spazio ai movimenti di telecamera, e scrive tempi.json, sottotitoli.json e la parte voce
# di colonna.json. Idempotente. Uso: python3 ritmo.py
import json
from pathlib import Path
qui = Path(__file__).resolve().parent
PRIMA = [0.45, 0.45, 0.60, 0.45, 0.45, 1.00, 0.80]      # attesa prima della voce in ogni scena
EXTRA = [1.20, 1.20, 0.70, 1.20, 1.70, 0.50, 3.60]      # secondi in più per telecamera e chiusura
DOPO = 0.75
VOCE = '../../voce/frane/'
par = json.load(open(qui / 'parole.json'))
t, scene, sott, voce = 0.0, [], [], []
for k, v in enumerate(par):
    d = round(PRIMA[k] + v['durata'] + DOPO + EXTRA[k], 2)
    t0 = round(t + PRIMA[k], 3)
    scene.append({'inizio': round(t, 2), 'durata': d})
    voce.append({'file': VOCE + v['file'], 'inizio': t0})
    sott.append({'inizio': t0, 'fine': round(t0 + v['durata'], 3), 'testo': v['testo'],
                 'parole': [{'w': p['w'], 't0': round(t0 + p['t0'], 3), 't1': round(t0 + p['t1'], 3)} for p in v['parole']]})
    t = round(t + d, 2)
json.dump({'scene': scene, 'totale': t}, open(qui / 'tempi.json', 'w'), indent=1)
json.dump(sott, open(qui / 'sottotitoli.json', 'w'), ensure_ascii=False, indent=1)
f = qui / 'colonna.json'
col = json.load(open(f)) if f.exists() else {}
col.update({'voce': voce, 'durata': t, 'scene': scene})
json.dump(col, open(f, 'w'), ensure_ascii=False, indent=1)
print('totale', t, [s['inizio'] for s in scene])
