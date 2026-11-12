#!/usr/bin/env python3
"""Monta voce, musica ed effetti sui video già resi da render.py, con la voce sempre in primo piano.

    python3 colonna.py <nome> --formati 9x16,16x9 [--sito AAAA-MM-GG-slug]

Legge  motion/voce/<nome>/durate.json e line_<k>.wav   (voce, una frase per scena)
       motion/voce/<nome>/suoni.json                    (musica ed effetti del video, vedi sotto)
       motion/out/<nome>/<nome>-<fmt>.mp4               (master di render.py)
Scrive motion/out/<nome>/colonna.json, mix.wav, mix.rapporto.json
       motion/out/<nome>/<nome>-<fmt>.mp4 e -web.mp4    (gli stessi file, con il mix al posto della sola voce)

suoni.json (tempi in secondi; "scena" parte da 0, "dopo" è il ritardo dall'inizio della scena):
  {"musica": {"file": "percorso/brano.mp3", "da": 0, "credito": "…"},
   "effetti": [{"file": "percorso/tuono.wav", "scena": 0, "dopo": 0.0, "tipo": "ambiente", "durata": 4},
               {"file": "percorso/pop.wav", "scena": 3, "dopo": 0.0, "tipo": "colpo"}]}
I percorsi relativi partono dalla cartella motion/. I tempi delle scene sono quelli dello stampo dei video
per la classe: ogni scena dura 0,45 s + la frase + 0,75 s.

Il mix lo fa mixa.py della skill colonna-sonora (livelli, controlli e volume finale -14 LUFS): si indica con
--mixa o con la variabile MIXA; serve un Python con numpy e scipy (--python o variabile PYTHON_MIX).
Se l'esito non è OK lo script si ferma: il video non si consegna.
"""
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MOTION = ROOT / "motion"
WEB = {"9x16": (720, 1280), "4x5": (720, 900), "1x1": (720, 720), "16x9": (1280, 720)}
BT709 = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]
PULITO = ["-map_metadata", "-1", "-fflags", "+bitexact"]


def ff(*a):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *a], check=True)


def percorso(p):
    p = Path(p)
    return p if p.is_absolute() else MOTION / p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nome")
    ap.add_argument("--formati", default="9x16")
    ap.add_argument("--sito")
    ap.add_argument("--mixa", default=os.environ.get("MIXA"))
    ap.add_argument("--python", default=os.environ.get("PYTHON_MIX", sys.executable))
    a = ap.parse_args()
    if not a.mixa or not Path(a.mixa).exists():
        sys.exit("Manca mixa.py della skill colonna-sonora: indicalo con --mixa o con la variabile MIXA.")
    voce, out = MOTION / "voce" / a.nome, MOTION / "out" / a.nome
    dur = json.loads((voce / "durate.json").read_text())
    suoni = json.loads((voce / "suoni.json").read_text())
    start, t = [], 0.0
    for d in dur:
        start.append(t)
        t += 0.45 + d + 0.75
    totale = round(t, 3)
    col = {"durata": totale,
           "voce": [{"file": str(voce / f"line_{k}.wav"), "inizio": round(s + 0.45, 3)} for k, s in enumerate(start)]}
    m = suoni["musica"]
    col["musica"] = [{"file": str(percorso(m["file"])), "inizio": 0, "fine": totale, "da": m.get("da", 0),
                      "entrata": m.get("entrata", 1.2), "uscita": m.get("uscita", 2.5)}]
    col["effetti"] = []
    for e in suoni["effetti"]:
        ini = round(start[e["scena"]] + e.get("dopo", 0), 3)
        v = {"file": str(percorso(e["file"])), "tipo": e.get("tipo", "colpo")}
        v["evento" if e.get("evento") else "inizio"] = ini
        if "durata" in e:
            v["fine" if v["tipo"] == "ambiente" else "durata"] = round(ini + e["durata"], 3) if v["tipo"] == "ambiente" else e["durata"]
        for k in ("entrata", "uscita", "volume"):
            if k in e:
                v[k] = e[k]
        col["effetti"].append(v)
    (out / "colonna.json").write_text(json.dumps(col, ensure_ascii=False, indent=1))
    r = subprocess.run([a.python, a.mixa, str(out / "colonna.json"), "--uscita", str(out / "mix.wav"),
                        "--rapporto", str(out / "mix.rapporto.json")], capture_output=True, text=True)
    print(r.stdout[-1500:], r.stderr[-800:])
    esito = "OK" if r.returncode == 0 else f"DA CONTROLLARE (codice {r.returncode})"
    if r.returncode:
        sys.exit(f"Mix non consegnabile: {esito}. Vedi {out / 'mix.rapporto.json'}")
    for fmt in [f.strip() for f in a.formati.split(",") if f.strip()]:
        master = out / f"{a.nome}-{fmt}.mp4"
        tmp = out / f".{fmt}-mix.mp4"
        ff("-i", str(master), "-i", str(out / "mix.wav"), "-map", "0:v", "-map", "1:a", "-c:v", "copy",
           "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", *PULITO, str(tmp))
        tmp.replace(master)
        w, h = WEB[fmt]
        web = out / f"{a.nome}-{fmt}-web.mp4"
        ff("-i", str(master), "-i", str(out / "mix.wav"), "-map", "0:v", "-map", "1:a",
           "-vf", f"scale={w}:{h}:flags=lanczos,format=yuv420p", "-c:v", "libx264", "-preset", "slow", "-crf", "23",
           "-profile:v", "main", "-level", "3.1", *BT709, "-bsf:v", "filter_units=remove_types=6",
           "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", *PULITO, str(web))
        print(f"[mix] {master.name} e {web.name}")
        if a.sito:
            suf = "" if fmt == "9x16" else f"-{fmt}"
            shutil.copy(web, ROOT / "static" / "video" / f"{a.sito}{suf}.mp4")
            print(f"[sito] static/video/{a.sito}{suf}.mp4")
    print(f"[mix] esito {esito}")


if __name__ == "__main__":
    main()
