#!/usr/bin/env python3
# vtt.py: scrive i sottotitoli WebVTT del video partendo da sottotitoli.json (ritmo.py): una battuta per frase,
# spezzata alla punteggiatura quando supera i 60 caratteri. Uso: python3 vtt.py USCITA.vtt
import json, re, sys
from pathlib import Path
qui = Path(__file__).resolve().parent
sott = json.loads((qui / 'sottotitoli.json').read_text(encoding='utf-8'))
def ora(t):
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f'{int(h):02d}:{int(m):02d}:{s:06.3f}'
battute = []
for f in sott:
    P, da = f['parole'], 0
    for i, p in enumerate(P):
        lungo = len(' '.join(q['w'] for q in P[da:i + 1]))
        fine_frase = re.search(r'[.;?!]$', p['w']) is not None or (p['w'].endswith(':') and lungo > 20)
        resto = len(' '.join(q['w'] for q in P[i + 1:]))
        if i == len(P) - 1 or (fine_frase and resto > 12) or (p['w'].endswith(',') and lungo > 42 and resto > 20):
            t1 = f['fine'] if i == len(P) - 1 else P[i + 1]['t0'] - .04
            battute.append((P[da]['t0'], t1, ' '.join(q['w'] for q in P[da:i + 1])))
            da = i + 1
righe = ['WEBVTT', '']
for n, (a, b, testo) in enumerate(battute, 1):
    righe += [str(n), f'{ora(a)} --> {ora(b)}', testo, '']
Path(sys.argv[1]).write_text('\n'.join(righe), encoding='utf-8')
print(len(battute), 'battute')
