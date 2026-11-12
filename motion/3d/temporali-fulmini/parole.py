#!/usr/bin/env python3
# parole.py: ricava i tempi delle parole dalle registrazioni già approvate della voce (motion/voce/temporali-fulmini/line_N.wav)
# e li scrive in parole.json. Non genera audio. Uso: python parole.py CARTELLA_SKILL (quella che contiene colonna-sonora).
import json, sys, wave
from pathlib import Path
sys.path.insert(0, str(Path(sys.argv[1]) / 'colonna-sonora' / 'scripts'))
import voce as V
qui = Path(__file__).resolve().parent
VOCE = qui.parents[1] / 'voce' / 'temporali-fulmini'
asr = V.trascrittore()
out = []
for k, (testo, bersagli, schermo) in enumerate(V.leggi_frasi(qui / 'frasi.txt')):
    f = VOCE / f'line_{k}.wav'
    a = V.decodifica(f)
    durata = len(a) / V.SR
    sentito, tempi = V.ascolta(asr, a)
    par = V.tempi_parole(testo, tempi, durata)
    uno_a_uno = len(tempi) == len(testo.split())
    if schermo != testo:
        par = V.tempi_schermo(schermo, par, durata)
    out.append(dict(n=k, file=f'line_{k}.wav', durata=round(durata, 3), testo=schermo, sentito=sentito, uno_a_uno=uno_a_uno, parole=par))
    print(k, round(durata, 3), uno_a_uno, sentito)
(qui / 'parole.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
