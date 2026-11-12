#!/usr/bin/env python3
# ritmo.py: decide i tempi del video 3D su IT-alert partendo dalle registrazioni già approvate (parole.json, scritto da
# parole.py) e scrive tempi.json (scene, inizio della voce, istanti degli eventi), sottotitoli.json (frasi a pezzi,
# parole a tempo) e colonna.json (voce, musica, effetti). Non genera audio. Idempotente: python3 ritmo.py
import json, re
from pathlib import Path
qui = Path(__file__).resolve().parent
parole = json.loads((qui / 'parole.json').read_text(encoding='utf-8'))

# attesa prima della voce e durata di ogni scena: in 3D le scene durano più della frase (voli, comparse, letture)
PRIMA = [0.45, 0.45, 4.10, 0.45, 0.60, 0.90, 0.90]
DURATA = [8.3, 8.7, 11.2, 13.7, 9.7, 9.9, 11.1]
S, V, t = [], [], 0.0
for k, f in enumerate(parole):
    assert DURATA[k] >= PRIMA[k] + f['durata'] + 0.4, f'scena {k} troppo corta per la sua frase'
    S.append(round(t, 2)); V.append(round(t + PRIMA[k], 2)); t += DURATA[k]
TOT = round(t, 2)
r = lambda x: round(x, 2)

# istanti degli eventi (secondi dall'inizio): li legge la pagina, e da qui vengono gli effetti sonori
E = dict(
    tuffo=3.9, telefono=4.0, avviso1=5.75, avviso1_fine=7.7,
    s1_arrivo=S[1] + 1.7, onde=S[1] + 1.5, orbita_fine=V[1] + 3.4, card_app=V[1] + 4.35, card_iscr=V[1] + 5.40,
    s1_fine=S[2] - 0.4,
    gru_fine=S[2] + 1.9, avviso2=S[2] + 2.0, avviso2_fine=S[2] + 4.0, card_suono=V[2] + 0.7, card_suono_fine=V[2] + 2.6,
    zoom_da=V[2] + 2.8, zoom_a=V[2] + 3.6, righe_da=V[2] + 3.4, cerchia=V[2] + 5.15, card_italert=V[2] + 5.25,
    s2_fine=S[3] - 0.4,
    m_arr=[V[3] + 1.55, V[3] + 4.65, V[3] + 6.35, V[3] + 7.95], m_par=[V[3] + 4.1, V[3] + 5.8, V[3] + 7.4],
    tutti_da=V[3] + 9.75, tutti_a=V[3] + 10.95,
    no_arrivo=S[4] + 1.1, pan1=V[4] + 0.5, no1=V[4] + 1.05, pan2=V[4] + 1.85, no2=V[4] + 2.45,
    col_da=V[4] + 2.85, col_a=V[4] + 3.8, colori=V[4] + 3.85, card_sito=V[4] + 5.0, s4_fine=S[5] - 0.4,
    p1_arr=S[5] + 1.1, p1=V[5] + 0.85, p2_da=V[5] + 1.45, p2_a=V[5] + 1.95, leggi_da=V[5] + 2.0, leggi_a=V[5] + 3.0,
    p3_da=V[5] + 3.0, p3_a=V[5] + 3.5, passi_da=V[5] + 5.5, passi_a=V[5] + 6.6,
    test_arr=S[6] + 0.9, test_msg=S[6] + 1.05, test_cerchia=V[6] + 1.4, card_test=V[6] + 2.2, card_test_fine=V[6] + 4.55,
    n112_da=V[6] + 4.6, n112_a=V[6] + 5.5, card_fine=V[6] + 6.9,
)
E = {k: ([r(x) for x in v] if isinstance(v, list) else r(v)) for k, v in E.items()}
scene = [dict(inizio=S[k], durata=DURATA[k]) for k in range(len(S))]
(qui / 'tempi.json').write_text(json.dumps(dict(scene=scene, voce=V, eventi=E, totale=TOT), indent=1), encoding='utf-8')

# sottotitoli: ogni frase a pezzi (frasi intere; i pezzi lunghi anche alla virgola), con le parole a tempo
def pezzi(P):
    tagli, n = [], 0
    for i, p in enumerate(P[:-1]):
        n += len(p['w']) + 1
        resto = sum(len(q['w']) + 1 for q in P[i + 1:])
        if re.search(r'[.:;?!]$', p['w']) and n >= 25 and resto >= 25:
            tagli.append(i + 1); n = 0
    out, da = [], 0
    for a in tagli + [len(P)]:
        out.append(P[da:a]); da = a
    fine = []
    for q in out:                                   # un pezzo oltre 95 caratteri si divide alla virgola più centrale
        testo = ' '.join(x['w'] for x in q)
        virgole = [i + 1 for i, x in enumerate(q[:-1]) if x['w'].endswith(',')]
        if len(testo) > 95 and virgole:
            meta = len(testo) / 2
            m = min(virgole, key=lambda i: abs(len(' '.join(x['w'] for x in q[:i])) - meta))
            fine += [q[:m], q[m:]]
        else:
            fine.append(q)
    return fine

sott = []
for k, f in enumerate(parole):
    Q = pezzi(f['parole'])
    for j, q in enumerate(Q):
        inizio = V[k] + q[0]['t0']
        fine = V[k] + Q[j + 1][0]['t0'] - 0.02 if j + 1 < len(Q) else V[k] + f['durata'] + 0.25
        sott.append(dict(inizio=r(inizio), fine=r(fine), scena=k, testo=' '.join(x['w'] for x in q),
                         parole=[dict(w=x['w'], t0=round(V[k] + x['t0'], 3), t1=round(V[k] + x['t1'], 3)) for x in q]))
(qui / 'sottotitoli.json').write_text(json.dumps(sott, ensure_ascii=False, indent=1), encoding='utf-8')

# colonna sonora: la voce già registrata, la musica già scelta, gli effetti sugli eventi dell'immagine
SUONI = '../../.cache/suoni/'
col = dict(
    durata=TOT,
    voce=[dict(file=f'../../voce/it-alert/line_{k}.wav', inizio=V[k]) for k in range(len(V))],
    musica=[dict(file=SUONI + 'voice-over-under.mp3', inizio=0, fine=TOT, da=0, entrata=1.5, uscita=3.0)],
    effetti=[],
)
def colpo(nome, evento=None, inizio=None, volume=0):
    e = dict(file=SUONI + nome, tipo='colpo', volume=volume)
    if evento is not None: e['evento'] = r(evento)
    else: e['inizio'] = r(inizio)
    col['effetti'].append(e)
# avviso generico sul telefono (scene 1 e 3), nelle pause della voce
colpo('avviso.wav', inizio=E['avviso1']); colpo('avviso.wav', inizio=E['avviso2'])
# fruscio sui voli della telecamera: il punto più forte cade a metà del volo
for a, b in [(1.6, E['tuffo']), (S[1], E['s1_arrivo']), (S[2], E['gru_fine']), (S[3], E['m_arr'][0]),
             (S[4], E['no_arrivo']), (E['col_da'], E['col_a']), (S[5], E['p1_arr']), (S[6], E['test_arr']),
             (E['n112_da'], E['n112_a'])]:
    colpo('passaggio.wav', evento=(a + b) / 2, volume=-3)
# pop sulle schede e sulle comparse dei modellini
for x in [E['card_app'], E['card_iscr']] + E['m_arr'] + [E['no1'], E['no2'], E['card_sito'], E['p1'], E['p3_a'],
                                                         E['n112_a'], E['card_fine']]:
    colpo('pop.wav', evento=x, volume=-2)
col['effetti'].sort(key=lambda e: e.get('evento', e.get('inizio')))
col['crediti'] = ['Musica: «Voice Over Under» di Kevin MacLeod (incompetech.com), licenza CC BY 4.0 '
                  '(creativecommons.org/licenses/by/4.0)']
(qui / 'colonna.json').write_text(json.dumps(col, ensure_ascii=False, indent=1), encoding='utf-8')
print('totale', TOT, 'scene', S, 'voce', V)
for s in sott: print(' ', s['inizio'], s['fine'], len(s['testo']), s['testo'])
