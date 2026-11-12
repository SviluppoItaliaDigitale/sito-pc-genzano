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
DURATA = [9.1, 9.1, 12.4, 14.6, 9.6, 10.5, 11.3]
S, V, t = [], [], 0.0
for k, f in enumerate(parole):
    assert DURATA[k] >= PRIMA[k] + f['durata'] + 0.4, f'scena {k} troppo corta per la sua frase'
    S.append(round(t, 2)); V.append(round(t + PRIMA[k], 2)); t += DURATA[k]
TOT = round(t, 2)
r = lambda x: round(x, 2)
norma = lambda x: re.sub(r'[^a-zà-ù0-9]', '', x.lower())
def w(k, parola, n=0):                              # istante (dall'inizio del video) in cui la voce dice la parola
    trovate = [p['t0'] for p in parole[k]['parole'] if norma(p['w']) == norma(parola)]
    return V[k] + trovate[n]
fine_voce = lambda k: V[k] + parole[k]['durata']

# istanti degli eventi (secondi dall'inizio): li legge la pagina, e da qui vengono gli effetti sonori
E = dict(
    tuffo=3.9, telefono=4.0, avviso1=fine_voce(0) + 0.25, avviso1_fine=fine_voce(0) + 2.2,
    s1_arrivo=S[1] + 1.7, onde=S[1] + 1.5, orbita_fine=w(1, 'Non') - 0.15, card_app=w(1, "un'app") - 0.15,
    card_iscr=w(1, 'non', 1), s1_fine=S[2] - 0.4,
    gru_fine=S[2] + 1.9, avviso2=S[2] + 2.0, avviso2_fine=S[2] + 4.0, card_suono=w(2, 'suono') - 0.15,
    card_suono_fine=w(2, 'sullo') - 0.4, zoom_da=w(2, 'sullo') - 0.2, zoom_a=w(2, 'sullo') + 0.6, righe_da=w(2, 'compare') - 0.1,
    cerchia=w(2, 'IT-alert') - 0.15, card_italert=w(2, 'IT-alert') - 0.05, s2_fine=S[3] - 0.4,
    m_largo=S[3] + 0.95, m_via=w(3, 'un') - 0.75,
    m_arr=[w(3, 'un') - 0.05, w(3, 'un', 1) + 0.1, w(3, 'il') + 0.05, w(3, "l'attività") + 0.02],
    m_par=[w(3, 'un', 1) - 0.45, w(3, 'il') - 0.5, w(3, "l'attività") - 0.53],
    tutti_da=fine_voce(3) + 0.4, tutti_a=fine_voce(3) + 1.6,
    no_arrivo=S[4] + 0.8, pan1=V[4] + 0.3, no1=w(4, 'terremoti') + 0.25, pan2=w(4, 'nemmeno'), no2=w(4, 'meteo') + 0.05,
    col_da=w(4, 'Per', 2) - 0.3, col_a=w(4, 'Per', 2) + 0.65, colori=w(4, 'Per', 2) + 0.7, card_sito=w(4, 'sul') - 0.12, s4_fine=S[5] - 0.4,
    p1_arr=S[5] + 0.8, p1=w(5, 'fermati') - 0.5, p1_eti=w(5, 'fermati') - 0.12, p2_da=w(5, 'leggi') - 0.25, p2_a=w(5, 'leggi') + 0.25,
    leggi_da=w(5, 'leggi') + 0.3, leggi_a=w(5, 'Poi') - 0.4, p3_da=w(5, 'Poi') - 0.2, p3_a=w(5, 'Poi') + 0.3,
    passi_da=fine_voce(5) + 0.25, passi_a=fine_voce(5) + 1.35,
    test_arr=S[6] + 0.9, test_msg=S[6] + 1.05, test_cerchia=w(6, 'TEST') - 0.1, card_test=w(6, 'è') - 0.05,
    card_test_fine=w(6, 'In') - 0.2, n112_da=w(6, 'In') + 0.25, n112_a=w(6, '112') - 0.15, card_fine=fine_voce(6) + 0.35,
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
for a, b in [(1.6, E['tuffo']), (S[1], E['s1_arrivo']), (S[2], E['gru_fine']), (S[3], E['m_largo']),
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
