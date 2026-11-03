# rombo.py — rombo della scossa fatto in codice (rumore filtrato + sub), con l'inviluppo uguale alla scossa della pagina.
# Uso: /root/.venv-voce/bin/python rombo.py  → audio/rombo1.wav e audio/rombo2.wav (tempi della versione 2).
import json, numpy as np, scipy.signal as sg, scipy.io.wavfile as wf
SR = 44100
S = json.load(open('sottotitoli.json'))
def parola(k, w, n=0):
    c = 0
    for p in S[k]['parole']:
        a = ''.join(ch for ch in p['w'].lower() if ch.isalnum())
        if a == w or (a.startswith(w) and len(w) > 3):
            if c == n: return p['t0']
            c += 1
    raise SystemExit(f'parola {w} non trovata nella scena {k}')
sc = json.load(open('tempi.json'))['scene']
S4 = sc[4]['inizio']
lis = lambda u: np.clip(u, 0, 1) ** 2 * (3 - 2 * np.clip(u, 0, 1))
prog = lambda t, a, d: np.clip((t - a) / d, 0, 1)
def suono(dur, env, seme):
    rng = np.random.default_rng(seme); n = int(dur * SR); t = np.arange(n) / SR
    b, a = sg.butter(2, 110 / (SR / 2)); basso = sg.lfilter(b, a, rng.standard_normal(n)); basso /= np.abs(basso).max()
    b2, a2 = sg.butter(2, [180 / (SR / 2), 900 / (SR / 2)], 'band'); medio = sg.lfilter(b2, a2, rng.standard_normal(n)); medio /= np.abs(medio).max()
    tremolio = .6 + .4 * np.abs(np.sin(t * 2 * np.pi * 7.3)) * (.7 + .3 * np.sin(t * 2 * np.pi * 1.1))
    sub = np.sin(2 * np.pi * 34 * t + 3 * np.sin(2 * np.pi * .7 * t))
    x = (.75 * basso + .35 * sub + .18 * medio * tremolio) * env(t)
    return (x / np.abs(x).max() * .8).astype(np.float32)
s1 = parola(2, 'arriva') - .5; incl = parola(2, 'inclina'); tiene = parola(4, 'tiene')
def env1(t):
    T = t + s1
    lv = 1 + (.55 - 1) * lis(prog(T, incl + 1.4, 1.5)); lv = lv + (.3 - lv) * lis(prog(T, S4 - .3, 1.0))
    return lis(prog(T, s1, .8)) * lv * (1 - lis(prog(T, tiene + 1.6, 2.4)))
s2 = parola(14, 'arriva') - .3
env2 = lambda t: lis(prog(t + s2, s2, .6)) * (1 - lis(prog(t + s2, s2 + 3.6, 1.8)))
wf.write('audio/rombo1.wav', SR, suono(tiene + 4.2 - s1, env1, 1))
wf.write('audio/rombo2.wav', SR, suono(5.6, env2, 2))
json.dump({'scossa1': s1, 'fine1': tiene + 4.2, 'scossa2': s2}, open('audio/rombi.json', 'w'))
print('rombo1', round(s1, 2), '→', round(tiene + 4.2, 2), '· rombo2', round(s2, 2))
