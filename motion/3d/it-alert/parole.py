#!/usr/bin/env python3
# parole.py: ricava i tempi delle parole dalle registrazioni già approvate della voce (motion/voce/it-alert/line_N.wav)
# e li scrive in parole.json (serve a ritmo.py per i sottotitoli a tempo). Non genera audio: ascolta soltanto.
# Uso: python parole.py CARTELLA_SKILL (quella che contiene colonna-sonora), con un Python che ha faster-whisper.
import difflib, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(sys.argv[1]) / 'colonna-sonora' / 'scripts'))
import voce as V
qui = Path(__file__).resolve().parent
VOCE = qui.parents[1] / 'voce' / 'it-alert'
asr = V.trascrittore()
norma = lambda w: V.parole(w).replace(' ', '')
out = []
for k, (testo, bersagli, schermo) in enumerate(V.leggi_frasi(qui / 'frasi.txt')):
    a = V.decodifica(VOCE / f'line_{k}.wav')
    durata = len(a) / V.SR
    a16 = np.interp(np.arange(0, len(a), V.SR / 16000), np.arange(len(a)), a).astype(np.float32)
    segs, _ = asr.transcribe(a16, language='it', beam_size=5, temperature=0.0, vad_filter=False,
                             condition_on_previous_text=False, word_timestamps=True)
    sentite = [(w.word.strip(), w.start, w.end) for s in segs for w in (s.words or [])]
    scritte = schermo.split()
    A, B = [norma(w) for w in scritte], [norma(w[0]) for w in sentite]
    tempi = [None] * len(scritte)
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if tag == 'equal':
            for d in range(i2 - i1):
                tempi[i1 + d] = (sentite[j1 + d][1], sentite[j1 + d][2])
        elif i2 > i1 and j2 > j1:            # parole sentite in modo diverso: il loro tempo si divide per lunghezza
            t0, t1 = sentite[j1][1], sentite[j2 - 1][2]
            pesi = np.array([len(w) + 1 for w in scritte[i1:i2]], float)
            b = t0 + (t1 - t0) * np.concatenate([[0], np.cumsum(pesi)]) / pesi.sum()
            for d in range(i2 - i1):
                tempi[i1 + d] = (float(b[d]), float(b[d + 1]))
    for i, t in enumerate(tempi):            # parole non sentite: fra la precedente e la successiva
        if t is None:
            prima = tempi[i - 1][1] if i and tempi[i - 1] else 0.0
            dopo = next((x[0] for x in tempi[i + 1:] if x), durata)
            tempi[i] = (prima, min(dopo, prima + 0.3))
    esatte = sum(1 for x, y in zip(A, B) if x == y) if len(A) == len(B) else None
    out.append(dict(n=k, file=f'line_{k}.wav', durata=round(durata, 3), testo=schermo,
                    sentito=' '.join(w[0] for w in sentite),
                    parole=[dict(w=w, t0=round(t[0], 3), t1=round(t[1], 3)) for w, t in zip(scritte, tempi)]))
    print(k, round(durata, 3), len(A), len(B), esatte)
(qui / 'parole.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
