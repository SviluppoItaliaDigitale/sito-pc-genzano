#!/usr/bin/env python3
# ritmo.py: tempi della versione 3D. La voce è quella già approvata (motion/voce/temporali-fulmini/line_N.wav): qui non si
# genera audio. Da parole.json (parole.py) calcola l'inizio di ogni scena (PRIMA + frase + DOPO: in 3D le scene durano di
# più per i movimenti di telecamera), gli istanti degli eventi (fulmini, voli, schede) e scrive tempi.json,
# sottotitoli.json e colonna.json (voce, musica, effetti). Idempotente: riparte ogni volta da parole.json.
import json, re, unicodedata
from pathlib import Path
qui = Path(__file__).resolve().parent
PRIMA = [2.6, 1.3, 1.0, 1.1, 1.1, 2.2, 1.9]      # secondi di immagine prima della frase
DOPO = [1.4, 1.2, 2.6, 1.5, 1.5, 2.3, 3.6]       # secondi dopo la frase
VOCE = '../../voce/temporali-fulmini/'
SUONI = '../../.cache/suoni/'
frasi = json.loads((qui / 'parole.json').read_text(encoding='utf-8'))
t, scene, sott, voce = 0.0, [], [], []
for k, f in enumerate(frasi):
    d = round(PRIMA[k] + f['durata'] + DOPO[k], 2)
    v0 = round(t + PRIMA[k], 3)
    scene.append({'inizio': round(t, 2), 'durata': d, 'voce': v0})
    sott.append({'inizio': v0, 'fine': round(v0 + f['durata'], 3), 'testo': f['testo'],
                 'parole': [{'w': p['w'], 't0': round(v0 + p['t0'], 3), 't1': round(v0 + p['t1'], 3)} for p in f['parole']]})
    voce.append({'file': VOCE + f['file'], 'inizio': v0})
    t = round(t + d, 2)
totale = t
S = lambda k: scene[k]['inizio']
E = lambda k: round(scene[k]['inizio'] + scene[k]['durata'], 2)
def norma(w):
    w = unicodedata.normalize('NFC', w.lower())
    return re.sub(r'[^\w]+', '', w)
def parola(k, w, n=0):
    c = 0
    for p in sott[k]['parole']:
        if norma(p['w']) == norma(w) or (len(norma(w)) > 3 and norma(p['w']).startswith(norma(w))):
            if c == n: return p['t0']
            c += 1
    raise SystemExit(f'parola «{w}» non trovata nella frase {k}')
r = lambda x: round(x, 2)
# ---- eventi: la pagina li legge da tempi.json, la colonna sonora dagli stessi numeri
ev = {
    'tuffo': r(S(0) + 1.5),                              # metà del tuffo sul rilievo
    'lampo0': r(parola(0, 'poco') - 0.15),               # primo fulmine
    'lampo2': r(S(2) + 0.3),                             # fulmine lontano: si vede prima di sentirlo
    'tuono2': r(parola(2, 'tuono') - 0.55),              # il tuono arriva a Genzano con il primo anello
    'zoom': r(parola(2, 'raggiungi') + 0.1),             # partenza dello zoom verso l'edificio
    'entra': r(E(2) - 1.25),                             # passaggio dal rilievo al plastico
    'lampo4': r(parola(4, 'colpiscono') + 0.15),         # il fulmine cade sull'albero
    'apre': r(S(5) + 0.25),                              # la casa si apre (vista esplosa)
    'esce': r(S(6) + 0.75),                              # ritorno al rilievo
    'lampo6': r(S(6) + 1.75),                            # ultimo fulmine, lontano
}
json.dump({'scene': scene, 'totale': totale, 'eventi': ev}, open(qui / 'tempi.json', 'w'), indent=1)
json.dump(sott, open(qui / 'sottotitoli.json', 'w'), ensure_ascii=False, indent=1)
tuono = lambda t0, vol: {'file': SUONI + 'tuono.wav', 'inizio': r(t0), 'fine': r(t0 + 4.5), 'tipo': 'ambiente', 'entrata': 0.02, 'uscita': 1.2, 'volume': vol}
passaggio = lambda t0, vol=-3: {'file': SUONI + 'passaggio.wav', 'evento': r(t0), 'tipo': 'colpo', 'volume': vol}
pop = lambda t0, vol=-4: {'file': SUONI + 'pop.wav', 'evento': r(t0), 'tipo': 'colpo', 'volume': vol}
effetti = [
    {'file': SUONI + 'vento-lungo.wav', 'inizio': 0.0, 'fine': r(ev['lampo0'] + 0.5), 'tipo': 'ambiente', 'entrata': 0.6, 'uscita': 1.5},
    passaggio(ev['tuffo']),
    tuono(ev['lampo0'], 0),
    {'file': SUONI + 'pioggia-lunga.wav', 'inizio': r(ev['lampo0'] + 0.2), 'fine': r(S(3) + 16), 'tipo': 'ambiente', 'entrata': 1.5, 'uscita': 1.0},
    pop(parola(1, 'previsioni') + 0.15),
    pop(parola(1, 'scuro') + 0.3),
    tuono(ev['tuono2'], 0),
    pop(parola(2, 'pericolo') + 0.1),
    passaggio(ev['entra']),
    pop(parola(3, 'edificio') + 0.2),
    pop(parola(3, "l'automobile") + 0.5),
    pop(parola(3, 'riparano') + 0.2),
    {'file': SUONI + 'pioggia-lunga.wav', 'inizio': r(S(3) + 15), 'fine': r(ev['esce'] + 3.2), 'tipo': 'ambiente', 'entrata': 1.0, 'uscita': 3.0},
    passaggio(S(4) + 0.5, -5),
    tuono(ev['lampo4'], 0),
    pop(parola(4, 'pali') + 0.1, -6),
    pop(parola(4, 'tralicci') + 0.1, -6),
    pop(parola(4, 'recinzioni') + 0.1, -6),
    pop(parola(4, "dall'acqua") + 0.1, -6),
    passaggio(ev['apre'] + 0.5),
    pop(parola(5, 'finestre') + 0.45),
    pop(parola(5, 'spine') + 0.3),
    pop(parola(5, 'fisso') + 0.3),
    pop(parola(5, 'piatti') + 0.5),
    passaggio(ev['esce']),
    tuono(ev['lampo6'], -6),
    pop(parola(6, '30') + 0.05),
    pop(parola(6, '112') + 0.05, -2),
]
effetti.sort(key=lambda e: e.get('evento', e.get('inizio')))
colonna = {'durata': totale, 'voce': voce, 'scene': [{'inizio': s['inizio'], 'durata': s['durata']} for s in scene],
           'musica': [{'file': SUONI + 'light-thought-var-1.mp3', 'inizio': 0, 'fine': totale, 'da': 0, 'entrata': 1.2, 'uscita': 3.0}],
           'effetti': effetti}
json.dump(colonna, open(qui / 'colonna.json', 'w'), ensure_ascii=False, indent=1)
print('totale', totale, [s['inizio'] for s in scene]); print(ev)
