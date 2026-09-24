#!/usr/bin/env python3
"""Genera la voce fuori campo con Piper TTS (voce it_IT-paola-medium).

    python3 .claude/skills/motion-graphic/strumenti/voce.py <nome> [--length-scale 1.08]

Legge  motion/voce/<nome>/testi.txt   una riga per scena, nello stesso ordine
                                       di CONFIG.scene; "-" = scena senza voce.
Scrive motion/voce/<nome>/line_<k>.wav (non committati)
       motion/voce/<nome>/durate.json  durata in secondi di ogni frase (null = nessuna)

Regole di scrittura dei testi: numeri in lettere, parole inglesi scritte a
orecchio («pàuer banc»), una frase per scena. L'audio NON si può ascoltare
da qui: chiedere sempre all'utente di verificare la pronuncia.
"""
import argparse, json, subprocess, sys, urllib.request, wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MOTION = ROOT / "motion"
PIPER = MOTION / ".cache" / "piper"
BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main/it/it_IT/paola/medium/"
MODELLO = "it_IT-paola-medium.onnx"


def assicura_piper():
    try:
        import piper  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages",
                        "piper-tts"], check=True)
    PIPER.mkdir(parents=True, exist_ok=True)
    for f in (MODELLO, MODELLO + ".json"):
        if not (PIPER / f).exists():
            print(f"[voce] scarico {f}")
            urllib.request.urlretrieve(BASE + f, PIPER / f)
    return PIPER / MODELLO


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nome")
    ap.add_argument("--length-scale", default="1.08")
    a = ap.parse_args()
    cartella = MOTION / "voce" / a.nome
    testi = cartella / "testi.txt"
    if not testi.exists():
        sys.exit(f"Manca {testi}: una riga per scena, '-' per le scene senza voce")
    modello = assicura_piper()
    durate = []
    for k, riga in enumerate(testi.read_text(encoding="utf-8").splitlines()):
        riga = riga.strip()
        wav = cartella / f"line_{k}.wav"
        if not riga or riga == "-":
            durate.append(None)
            wav.unlink(missing_ok=True)
            continue
        subprocess.run([sys.executable, "-m", "piper", "-m", str(modello),
                        "--length-scale", a.length_scale, "--sentence-silence", "0.35",
                        "-f", str(wav)], input=riga, text=True, check=True,
                       capture_output=True)
        with wave.open(str(wav)) as w:
            d = round(w.getnframes() / w.getframerate(), 3)
        durate.append(d)
        print(f"[voce] scena {k}: {d:.2f} s  «{riga}»")
    (cartella / "durate.json").write_text(json.dumps(durate))
    print(f"[voce] durate in {(cartella / 'durate.json').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
