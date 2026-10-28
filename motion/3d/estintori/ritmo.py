#!/usr/bin/env python3
# ritmo.py: aggiunge a ogni scena qualche decimo per le animazioni (vista esplosa, spostamenti, spegnimenti)
# e riscrive tempi.json, colonna.json (voce) e sottotitoli.json spostati di conseguenza. Idempotente: parte da voce.json.
import json
EXTRA = [0.6, 1.4, 1.4, 0.4, 1.0, 0.8, 1.0, 0.8, 1.0, 0.8, 0.8, 0.8, 1.0, 1.0, 0.8, 2.2]
PRIMA, DOPO = 0.45, 0.75
voce = json.load(open('voce/voce.json'))
sott = json.load(open('sottotitoli.json'))
col = json.load(open('colonna.json'))
t, scene = 0.0, []
for k, v in enumerate(voce):
    d = round(PRIMA + v['durata'] + DOPO + EXTRA[k], 2)
    scene.append({'inizio': round(t, 2), 'durata': d})
    t += d
# vecchi inizi della voce (da colonna), nuovi = inizio scena + PRIMA
for k, s in enumerate(scene):
    nuovo = s['inizio'] + PRIMA
    vecchio = sott[k]['inizio']
    dt = nuovo - vecchio
    sott[k]['inizio'] = round(sott[k]['inizio'] + dt, 3); sott[k]['fine'] = round(sott[k]['fine'] + dt, 3)
    for p in sott[k].get('parole', []):
        p['t0'] = round(p['t0'] + dt, 3); p['t1'] = round(p['t1'] + dt, 3)
    col['voce'][k]['inizio'] = round(nuovo, 3)
if 'scene' in col: col['scene'] = scene        # anche le scene della colonna seguono i tempi nuovi
json.dump({'scene': scene, 'totale': round(t, 2)}, open('tempi.json', 'w'), indent=1)
json.dump(sott, open('sottotitoli.json', 'w'), ensure_ascii=False, indent=1)
json.dump(col, open('colonna.json', 'w'), ensure_ascii=False, indent=1)
print('totale', round(t, 2), [s['inizio'] for s in scene])
