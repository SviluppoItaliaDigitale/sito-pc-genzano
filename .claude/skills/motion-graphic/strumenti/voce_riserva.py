#!/usr/bin/env python3
"""Voce di riserva gratuita «Damien» (modello XTTS-v2, gira sulla macchina, senza crediti né limiti di quantità).
Uso: <python del venv> voce_riserva.py <nome> [--riprese 2]  → motion/out/<nome>/riprese/line_<N>_take_<T>.wav

Si usa SOLO quando la voce Luca non ha crediti (regola di Alessandro del 12/11/2026: Luca è sempre la prima voce).
Licenza del modello: Coqui Public Model License, solo uso non commerciale; vietati i video che producono entrate
(raccolte fondi, 5 per mille) e i progetti finanziati da contributi pubblici. Alessandro ha accettato le condizioni
il 12/11/2026 per i video non commerciali. Obbligo: la riga «Voce sintetica: modello distribuito con licenza Coqui
Public Model License (coqui.ai/cpml).» va nella descrizione del video sul sito e nei post social, mai dentro il video.

Installazione, una volta per sessione, in un ambiente virtuale fuori dal repository:
  python3 -m venv V && V/bin/pip install --extra-index-url https://download.pytorch.org/whl/cpu torch torchaudio
  V/bin/pip install "coqui-tts[codec]" six
Legge motion/voce/<nome>/testi.txt (una frase per riga). Le riprese si scelgono poi con voce.py della skill
colonna-sonora («scegli»), che tiene la più fedele al testo, e si portano in motion/voce/<nome>/line_<k>.wav.
"""
import argparse, os, sys, time
from pathlib import Path

RADICE = Path(__file__).resolve().parents[4]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nome")
    ap.add_argument("--riprese", type=int, default=2)
    ap.add_argument("--voce", default="Damien Black")
    a = ap.parse_args()
    if os.environ.get("COQUI_TOS_AGREED") != "1":
        sys.exit("Imposta COQUI_TOS_AGREED=1 solo se le condizioni non commerciali valgono per questo video "
                 "(vedi la nota in testa al file).")
    from TTS.api import TTS
    t = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
    out = RADICE / "motion" / "out" / a.nome / "riprese"
    out.mkdir(parents=True, exist_ok=True)
    righe = (RADICE / "motion" / "voce" / a.nome / "testi.txt").read_text(encoding="utf-8").strip().splitlines()
    for k, riga in enumerate(righe, 1):
        for r in range(1, a.riprese + 1):
            f = out / f"line_{k}_take_{r}.wav"
            if f.exists():
                continue
            t0 = time.time()
            t.tts_to_file(text=riga, speaker=a.voce, language="it", file_path=str(f))
            print(f.name, round(time.time() - t0, 1), "s", flush=True)


if __name__ == "__main__":
    main()
