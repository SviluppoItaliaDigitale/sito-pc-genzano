#!/usr/bin/env python3
# vtt.py: sottotitoli WebVTT e trascrizione del video dai tempi veri delle parole (sottotitoli.json di ritmo.py).
# Le frasi lunghe si dividono alla fine di ogni periodo. Uso: python3 vtt.py CARTELLA_USCITA
import json, re, sys
from pathlib import Path
qui = Path(__file__).resolve().parent
out = Path(sys.argv[1])
def tc(t):
    h, r = divmod(max(0, t), 3600); m, s = divmod(r, 60)
    return f'{int(h):02d}:{int(m):02d}:{s:06.3f}'
righe, n = ['WEBVTT', ''], 0
frasi = json.load(open(qui / 'sottotitoli.json'))
for f in frasi:
    P, da = f['parole'], 0
    for i, p in enumerate(P):
        if re.search(r'[.:?!]$', p['w']) or i == len(P) - 1:
            if i < len(P) - 1 and i - da < 2:
                continue
            n += 1
            fine = f['fine'] if i == len(P) - 1 else P[i + 1]['t0'] - 0.05
            righe += [str(n), f"{tc(P[da]['t0'])} --> {tc(fine)}", ' '.join(q['w'] for q in P[da:i + 1]), '']
            da = i + 1
(out / 'frane-3d.vtt').write_text('\n'.join(righe), encoding='utf-8')
(out / 'frane-3d-trascrizione.txt').write_text('\n'.join(f['testo'] for f in frasi) + '\n', encoding='utf-8')
print(n, 'battute')
