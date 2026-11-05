"""Converte le righe ElevenLabs (mp3) in line_<k>.wav mono 16 bit e scrive durate.json, togliendo il silenzio iniziale e finale."""
import json, subprocess, sys, wave
from pathlib import Path
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
mp3 = sorted(src.glob("riga_*.mp3"), key=lambda p: int(p.stem.split("_")[1]))
for w in dst.glob("line_*.wav"): w.unlink()
filtro = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,"
          "areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse")
durate = []
for k, m in enumerate(mp3):
    out = dst / f"line_{k}.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(m), "-af", filtro, "-ac", "1", "-ar", "44100", "-sample_fmt", "s16", str(out)], check=True)
    with wave.open(str(out)) as w: d = round(w.getnframes() / w.getframerate(), 3)
    durate.append(d); print(out.name, d)
(dst / "durate.json").write_text(json.dumps(durate))
