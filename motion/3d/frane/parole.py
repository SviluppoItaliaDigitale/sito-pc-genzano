#!/usr/bin/env python3
# parole.py: ricava i tempi delle parole dalle registrazioni già approvate della voce (motion/voce/frane/line_N.wav)
# e li scrive in parole.json. Non genera audio. Le parole sentite si allineano a quelle scritte: dove coincidono si
# prende il tempo sentito, in mezzo si divide in proporzione alla lunghezza.
# Uso: python parole.py CARTELLA_SKILL (quella che contiene colonna-sonora), con un Python che ha faster-whisper.
import difflib, json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(sys.argv[1]) / 'colonna-sonora' / 'scripts'))
import voce as V
qui = Path(__file__).resolve().parent
VOCE = qui.parents[1] / 'voce' / 'frane'
asr = V.trascrittore()


def sentite(a):
    a16 = np.interp(np.arange(0, len(a), V.SR / 16000), np.arange(len(a)), a).astype(np.float32)
    segs, _ = asr.transcribe(a16, language='it', beam_size=5, temperature=0.0, vad_filter=False,
                             condition_on_previous_text=False, word_timestamps=True)
    return [(w.word.strip(), float(w.start), float(w.end)) for s in segs for w in (s.words or [])]


def allinea(scritte, udite, durata):
    ns, nu = [V.parole(w) for w in scritte], [V.parole(w) for w, _, _ in udite]
    tempi = [None] * len(scritte)
    for a, b, n in difflib.SequenceMatcher(None, ns, nu, autojunk=False).get_matching_blocks():
        for k in range(n):
            tempi[a + k] = (udite[b + k][1], udite[b + k][2])
    out, i = [], 0
    while i < len(scritte):
        if tempi[i]:
            i += 1
            continue
        j = i
        while j < len(scritte) and not tempi[j]:
            j += 1
        t0 = tempi[i - 1][1] if i else (udite[0][1] if udite else 0.0)
        t1 = tempi[j][0] if j < len(scritte) else (udite[-1][2] if udite else durata)
        pesi = np.array([len(w) + 1 for w in scritte[i:j]], float)
        bordi = t0 + (t1 - t0) * np.concatenate([[0], np.cumsum(pesi)]) / pesi.sum()
        for k in range(i, j):
            tempi[k] = (float(bordi[k - i]), float(bordi[k - i + 1]))
        i = j
    return [dict(w=w, t0=round(a, 3), t1=round(b, 3)) for w, (a, b) in zip(scritte, tempi)]


out = []
for k, (testo, bersagli, schermo) in enumerate(V.leggi_frasi(qui / 'frasi.txt')):
    f = VOCE / f'line_{k}.wav'
    a = V.decodifica(f)
    durata = len(a) / V.SR
    ud = sentite(a)
    par = allinea(testo.split(), ud, durata)
    if schermo != testo:
        par = V.tempi_schermo(schermo, par, durata)
    uguali = sum(1 for p, q in zip(testo.split(), par) if True)
    out.append(dict(n=k, file=f'line_{k}.wav', durata=round(durata, 3), testo=schermo,
                    sentito=' '.join(w for w, _, _ in ud), parole=par))
    print(k, round(durata, 3), ' '.join('%s@%.2f' % (p['w'], p['t0']) for p in par))
(qui / 'parole.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
