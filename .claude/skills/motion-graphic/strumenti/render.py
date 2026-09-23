#!/usr/bin/env python3
"""Rende una motion graphic in uno o più formati.

    python3 .claude/skills/motion-graphic/strumenti/render.py <nome> [opzioni]

Opzioni:
  --formati 9x16,4x5,1x1,16x9   formati da produrre (predefinito: 9x16)
  --provini                     solo i fogli di provini (fotogrammi chiave), niente video
  --sito AAAA-MM-GG-slug        copia versioni web, poster e sottotitoli in static/video/

Per ogni formato scrive in motion/out/<nome>/:
  <nome>-<fmt>.mp4        MASTER per i social: 1080 px sul lato corto (1920x1080 il 16:9),
                          H.264 High 4.1, 30 fps, yuv420p bt709, audio (voce o muto), faststart
  <nome>-<fmt>-web.mp4    versione per il SITO: 720 px sul lato corto, H.264 Main 3.1,
                          audio sempre presente, faststart (il formato che il sito riproduce bene)
  <nome>-<fmt>-poster.webp  anteprima al secondo POSTER_T
  provini-<fmt>.png       fotogrammi chiave dalla pagina (prima del video)
  verifica-<fmt>.png      tre fotogrammi estratti dall'MP4 finito
  <nome>.vtt              sottotitoli WebVTT, se c'è la voce
  voce.mp3                traccia voce montata, se ci sono motion/voce/<nome>/line_*.wav;
                          in alternativa si usa motion/voce/<nome>/voce.mp3 (traccia già pronta)
"""
import argparse, io, json, shutil, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import build, traccia_voce, MOTION, ROOT  # noqa: E402

FORMATI = {"9x16": (1080, 1920), "4x5": (1080, 1350), "1x1": (1080, 1080), "16x9": (1920, 1080)}
WEB = {"9x16": (720, 1280), "4x5": (720, 900), "1x1": (720, 720), "16x9": (1280, 720)}
FPS = 30
CHROME = Path("/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
BT709 = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709"]


def ffmpeg_exe():
    f = shutil.which("ffmpeg")
    if f:
        return f
    try:
        import imageio_ffmpeg
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "imageio-ffmpeg"], check=True)
        import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


FF = None


def ff(*args):
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def browser(p):
    opts = dict(args=["--force-color-profile=srgb", "--font-render-hinting=none", "--disable-lcd-text"])
    if CHROME.exists():
        opts["executable_path"] = str(CHROME)
    return p.chromium.launch(**opts)


def foglio(immagini, etichette, dest, colonne=4):
    from PIL import Image, ImageDraw
    w0, h0 = immagini[0].size
    sc = 360 / w0
    tw, th = int(w0 * sc), int(h0 * sc)
    righe = (len(immagini) + colonne - 1) // colonne
    sheet = Image.new("RGB", (colonne * (tw + 16) + 16, righe * (th + 44) + 16), "#222")
    d = ImageDraw.Draw(sheet)
    for i, (im, et) in enumerate(zip(immagini, etichette)):
        x, y = 16 + (i % colonne) * (tw + 16), 16 + (i // colonne) * (th + 44)
        sheet.paste(im.convert("RGB").resize((tw, th)), (x, y + 28))
        d.text((x, y + 6), et, fill="#fff")
    sheet.save(dest)
    print(f"[provini] {dest.relative_to(ROOT)}")


def monta_voce(nome, voice_at, total, out):
    cartella = MOTION / "voce" / nome
    righe = [(k, cartella / f"line_{k}.wav") for k in range(len(voice_at))]
    righe = [(k, f) for k, f in righe if f.exists() and voice_at[k] is not None]
    if not righe:
        return None
    ins, filt = [], []
    for j, (k, f) in enumerate(righe):
        ins += ["-i", str(f)]
        ms = int(round(voice_at[k] * 1000))
        filt.append(f"[{j}:a]aformat=sample_rates=44100:channel_layouts=mono,adelay={ms}|{ms}[a{j}]")
    mix = "".join(f"[a{j}]" for j in range(len(righe)))
    filt.append(f"{mix}amix=inputs={len(righe)}:normalize=0,apad,atrim=0:{total:.3f},"
                f"loudnorm=I=-16:TP=-1.5[out]")
    mp3 = out / "voce.mp3"
    ff(*ins, "-filter_complex", ";".join(filt), "-map", "[out]", "-ar", "44100",
       "-c:a", "libmp3lame", "-b:a", "96k", str(mp3))
    print(f"[voce] {mp3.relative_to(ROOT)}")
    return mp3


def vtt(subs, dest):
    def ts(s):
        h, r = divmod(s, 3600)
        m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"
    righe = ["WEBVTT", ""]
    for i, s in enumerate(subs, 1):
        righe += [str(i), f"{ts(s['da'])} --> {ts(s['a'])}", s["testo"], ""]
    dest.write_text("\n".join(righe), encoding="utf-8")
    print(f"[vtt] {dest.relative_to(ROOT)}")


def main():
    global FF
    ap = argparse.ArgumentParser()
    ap.add_argument("nome")
    ap.add_argument("--formati", default="9x16")
    ap.add_argument("--provini", action="store_true")
    ap.add_argument("--sito")
    a = ap.parse_args()
    formati = [f.strip() for f in a.formati.split(",") if f.strip()]
    for f in formati:
        if f not in FORMATI:
            sys.exit(f"Formato sconosciuto: {f} (validi: {', '.join(FORMATI)})")
    FF = ffmpeg_exe()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "playwright", "pillow"], check=True)
        from playwright.sync_api import sync_playwright
    from PIL import Image

    out = MOTION / "out" / a.nome
    out.mkdir(parents=True, exist_ok=True)
    html = build(a.nome)
    voce_mp3 = None
    with sync_playwright() as p:
        b = browser(p)
        for fmt in formati:
            W, H = FORMATI[fmt]
            pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
            pg.goto(html.as_uri() + f"?render=1&fmt={fmt}")
            pg.wait_for_function("window.__ready === true", timeout=30000)
            info = pg.evaluate("({T:window.TOTAL,K:window.KEYFRAMES||[],P:window.POSTER_T||0,"
                               "V:window.VOICE_AT||[],S:window.SUBS||[]})")
            total = info["T"]
            if not info["K"]:  # pagina senza KEYFRAMES: otto istanti equidistanti
                info["K"] = [round(total * i / 8, 2) for i in range(8)]
            # 1. provini
            shots, lab = [], []
            for t in info["K"]:
                pg.evaluate(f"window.renderFrame({t})")
                shots.append(Image.open(io.BytesIO(pg.screenshot(type="png"))))
                lab.append(f"{fmt}  t={t:.2f}s")
            foglio(shots, lab, out / f"provini-{fmt}.png")
            if a.provini:
                pg.close()
                continue
            # 2. poster
            pg.evaluate(f"window.renderFrame({info['P']})")
            Image.open(io.BytesIO(pg.screenshot(type="png"))).convert("RGB").resize(
                WEB[fmt]).save(out / f"{a.nome}-{fmt}-poster.webp", quality=82)
            # 3. fotogrammi -> video muto
            muto = out / f".{fmt}-muto.mp4"
            n = round(total * FPS) + 1
            print(f"[render] {fmt}: {n} fotogrammi ({total:.1f} s)")
            proc = subprocess.Popen([FF, "-hide_banner", "-loglevel", "error", "-y",
                                     "-f", "image2pipe", "-framerate", str(FPS), "-c:v", "png", "-i", "-",
                                     "-vf", "scale=in_range=full:out_range=tv:out_color_matrix=bt709,format=yuv420p",
                                     "-c:v", "libx264", "-preset", "slow", "-crf", "17",
                                     "-profile:v", "high", "-level", "4.1", *BT709,
                                     "-movflags", "+faststart", str(muto)], stdin=subprocess.PIPE)
            for i in range(n):
                pg.evaluate(f"window.renderFrame({i / FPS})")
                proc.stdin.write(pg.screenshot(type="png"))
                if i % 150 == 0:
                    print(f"  {i}/{n}", flush=True)
            proc.stdin.close()
            if proc.wait():
                sys.exit("ffmpeg ha restituito un errore")
            # 4. audio: voce montata oppure traccia muta
            if voce_mp3 is None and info["V"]:
                voce_mp3 = monta_voce(a.nome, info["V"], total, out)
            if voce_mp3 is None:  # traccia già pronta (es. registrazione umana)
                voce_mp3 = traccia_voce(a.nome)
            if voce_mp3:
                audio = ["-i", str(voce_mp3)]
            else:
                audio = ["-f", "lavfi", "-t", f"{total:.3f}", "-i", "anullsrc=r=44100:cl=mono"]
            master = out / f"{a.nome}-{fmt}.mp4"
            ff("-i", str(muto), *audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
               "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", str(master))
            ww, wh = WEB[fmt]
            web = out / f"{a.nome}-{fmt}-web.mp4"
            ff("-i", str(master), "-vf", f"scale={ww}:{wh}:flags=lanczos,format=yuv420p",
               "-c:v", "libx264", "-preset", "slow", "-crf", "23", "-profile:v", "main", "-level", "3.1",
               *BT709, "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(web))
            muto.unlink()
            # 5. verifica sul file finito
            prove = []
            for frac in (0.25, 0.5, 0.9):
                buf = subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-ss", f"{total * frac:.2f}",
                                      "-i", str(master), "-frames:v", "1", "-f", "image2pipe", "-c:v", "png", "-"],
                                     check=True, capture_output=True).stdout
                prove.append(Image.open(io.BytesIO(buf)))
            foglio(prove, [f"MP4 {fmt} {int(f * 100)}%" for f in (0.25, 0.5, 0.9)],
                   out / f"verifica-{fmt}.png", colonne=3)
            for f in (master, web):
                print(f"[mp4] {f.relative_to(ROOT)}  {f.stat().st_size / 1e6:.1f} MB")
            if info["S"] and not (out / f"{a.nome}.vtt").exists():
                vtt(info["S"], out / f"{a.nome}.vtt")
            pg.close()
        b.close()
    if voce_mp3 and voce_mp3.parent == out:
        build(a.nome)  # la pagina autonoma incorpora ora anche l'audio
    if a.sito and not a.provini:
        dest = ROOT / "static" / "video"
        for fmt in formati:
            suf = "" if fmt == "9x16" else f"-{fmt}"
            shutil.copy(out / f"{a.nome}-{fmt}-web.mp4", dest / f"{a.sito}{suf}.mp4")
            shutil.copy(out / f"{a.nome}-{fmt}-poster.webp", dest / f"{a.sito}{suf}-poster.webp")
            print(f"[sito] static/video/{a.sito}{suf}.mp4 (+ poster)")
        if (out / f"{a.nome}.vtt").exists():
            shutil.copy(out / f"{a.nome}.vtt", dest / f"{a.sito}.vtt")
            print(f"[sito] static/video/{a.sito}.vtt")


if __name__ == "__main__":
    main()
