#!/usr/bin/env python3
# ritmo.py: decide i tempi del video 3D «Vento forte» partendo dalle parole della voce già registrata (parole.json,
# scritto da parole.py) e riscrive tempi.json (scene e istanti delle animazioni), sottotitoli.json e colonna.json
# (voce, musica, effetti). Non genera audio. Idempotente. Uso: python3 ritmo.py
import json, re
from pathlib import Path
qui = Path(__file__).resolve().parent
PAR = json.loads((qui / 'parole.json').read_text(encoding='utf-8'))
# pausa prima della voce e durata di ogni scena: in 3D servono alcuni secondi in più per i movimenti di telecamera
PRIMA = [1.5, .45, 1.2, .45, .45, .45, .45]
CODA = [1.0, 1.8, 3.1, 2.0, 2.0, 2.4, 3.6]
DOPO = 0.75
scene, voce, t = [], [], 0.0
for k, p in enumerate(PAR):
    d = round(PRIMA[k] + p['durata'] + DOPO + CODA[k], 2)
    scene.append({'inizio': round(t, 2), 'durata': d})
    voce.append(round(t + PRIMA[k], 3))
    t = round(t + d, 2)
TOT = t
S = lambda k: scene[k]['inizio']
E = lambda k: round(scene[k]['inizio'] + scene[k]['durata'], 2)
norma = lambda w: re.sub(r'[^\w]+', '', w.lower())
def parola(k, w, n=0):
    c = 0
    for p in PAR[k]['parole']:
        if norma(p['w']).startswith(norma(w)):
            if c == n: return round(voce[k] + p['t0'], 3)
            c += 1
    raise SystemExit(f'parola «{w}» non trovata nella frase {k}')

# istanti delle animazioni (gli stessi per la pagina e per gli effetti sonori)
ev = {
    # 0 apertura: tuffo sul rilievo, poi il quartiere
    'tuffo': 3.3, 'arrivo0': 4.6, 'rami': parola(0, 'rami'), 'tegole': parola(0, 'tegole'), 'vasi0': parola(0, 'vasi'),
    # 1 il balcone
    'arrivo1': S(1) + 1.6, 'riparo': parola(1, 'riparo'), 'fissa': parola(1, 'fissa'), 'vasi1': parola(1, 'vasi'),
    'davanzali': parola(1, 'davanzali'),
    # 2 allerta e parcheggio
    'arrivo2': S(2) + 1.1, 'allertaFine': S(2) + 3.0, 'carr2': S(2) + 3.1, 'auto': S(2) + 4.5, 'parte': S(2) + 5.5,
    'parcheggiata': S(2) + 7.3,
    # 3 in casa
    'arrivo3': S(3) + 1.5, 'resta': parola(3, 'resta'), 'chiudi': parola(3, 'chiudi'), 'stai3': parola(3, 'stai'),
    # 4 fuori
    'arrivo4': S(4) + 1.5, 'evita': parola(4, 'evita'), 'spezzano': parola(4, 'spezzano'),
    'volo4': parola(4, 'frequente') + .38, 'impalcature': parola(4, 'impalcature') + .08,
    'cartelloni': parola(4, 'cartelloni'), 'cornicioni': parola(4, 'cornicioni'),
    # 5 in strada
    'rallenta': parola(5, 'rallenta'), 'volo5': S(5) + 2.7, 'arrivo5': S(5) + 6.3,
    # 6 dopo
    'arrivo6': S(6) + 1.2, 'toccare': parola(6, 'non'), 'se': parola(6, 'Se'), 'chiama': parola(6, 'chiama'),
    'n112': parola(6, '112'),
}
ev = {k: round(v, 3) for k, v in ev.items()}
(qui / 'tempi.json').write_text(json.dumps({'scene': scene, 'totale': TOT, 'voce': voce, 'ev': ev}, indent=1), encoding='utf-8')

sott = []
for k, p in enumerate(PAR):
    sott.append({'inizio': voce[k], 'fine': round(voce[k] + p['durata'], 3), 'testo': p['testo'],
                 'parole': [{'w': q['w'], 't0': round(voce[k] + q['t0'], 3), 't1': round(voce[k] + q['t1'], 3)} for q in p['parole']]})
(qui / 'sottotitoli.json').write_text(json.dumps(sott, ensure_ascii=False, indent=1), encoding='utf-8')

# colonna sonora: voce, musica e effetti già presenti in motion/voce e motion/.cache/suoni (percorsi relativi a questo file)
SUONI = '../../.cache/suoni/'
vento = lambda a, b, vol=0: {'file': SUONI + 'vento-lungo.wav', 'inizio': round(a, 2), 'fine': round(b, 2), 'da': round(a % 30, 2),
                             'tipo': 'ambiente', 'entrata': .6, 'uscita': 1.2, 'volume': vol}
passaggio = lambda x, vol=-3: {'file': SUONI + 'passaggio.wav', 'evento': round(x, 2), 'tipo': 'colpo', 'volume': vol}
pop = lambda x, vol=-4: {'file': SUONI + 'pop.wav', 'evento': round(x, 2), 'tipo': 'colpo', 'volume': vol}
effetti = [
    vento(0, E(0) + .4),                               # raffiche sul rilievo e nel quartiere
    vento(ev['vasi1'] + 1.4, S(2) + .5, -4),           # le prime raffiche, a balcone già in ordine
    vento(S(3) + .2, S(5) - .1),                       # il vento soffia forte: in casa e fuori
    vento(S(5), E(5) - .3, -2),                        # raffiche sul viadotto
    passaggio(ev['tuffo']),                            # dal rilievo al quartiere
    passaggio(S(1) + .8), passaggio(S(2) + .55), passaggio(ev['carr2'] + .7, -5), passaggio(S(3) + .75),
    passaggio(S(4) + .75), passaggio(ev['volo4'] + .5), passaggio(S(5) + .05, -5), passaggio(ev['volo5'] + 1.6, -5),
    passaggio(S(6) + .5, -5),
    pop(ev['arrivo0'] + .12),                          # schede e segni
    pop(ev['riparo'] + 1.15), pop(ev['fissa'] + 1.5), pop(ev['davanzali'] + 1.0),
    pop(ev['arrivo2'] + .1), pop(ev['auto'] + .1), pop(ev['parcheggiata'] + .15),
    pop(ev['resta'] + .02 if ev['resta'] > ev['arrivo3'] + .1 else ev['arrivo3'] + .12), pop(ev['chiudi'] + 1.0), pop(ev['stai3'] + .55),
    pop(ev['evita'] + .15), pop(ev['impalcature'] + .05), pop(ev['cartelloni'] + .02), pop(ev['cornicioni'] + .02),
    pop(S(5) + .95), pop(ev['arrivo5'] + .12), pop(ev['arrivo5'] + .62),
    pop(ev['toccare'] + .05), pop(ev['se'] + .36), pop(ev['n112'] - .1, -2), pop(ev['n112'] + 1.55),
]
col = {
    'durata': TOT,
    'voce': [{'file': f'../../voce/vento-forte/line_{k}.wav', 'inizio': voce[k]} for k in range(len(PAR))],
    'musica': [{'file': SUONI + 'easy-lemon.mp3', 'inizio': 0, 'fine': TOT, 'da': 0, 'entrata': 1.2, 'uscita': 3.0}],
    'effetti': effetti,
    'crediti': 'Musica: «Easy Lemon» di Kevin MacLeod (incompetech.com), licenza CC BY 4.0 (creativecommons.org/licenses/by/4.0)',
}
(qui / 'colonna.json').write_text(json.dumps(col, ensure_ascii=False, indent=1), encoding='utf-8')
print('totale', TOT, [s['inizio'] for s in scene])
print(ev)
