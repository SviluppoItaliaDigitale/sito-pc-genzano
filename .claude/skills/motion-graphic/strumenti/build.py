#!/usr/bin/env python3
"""Costruisce la pagina autonoma di una motion graphic.

    python3 .claude/skills/motion-graphic/strumenti/build.py <nome>

Legge  motion/src/<nome>.src.html
Scrive motion/dist/<nome>.html  (font in base64, durate voce, audio in base64)

Segnaposto sostituiti nel sorgente:
  /*FONTS*/        -> @font-face di Titillium Web 400/600/700/900 e Roboto Mono 500/700
  /*DUR*/[]        -> durate delle frasi (motion/voce/<nome>/durate.json), se esiste
  /*AUDIO*/""      -> data URI della traccia voce, come stringa JS
  src="/*AUDIO*/"  -> data URI della traccia voce, come attributo di <audio>
                      (traccia: motion/out/<nome>/voce.mp3 montata da render.py,
                       altrimenti motion/voce/<nome>/voce.mp3 committata)

I font si scaricano una volta sola con `npm pack` in motion/.cache/fonts.
"""
import base64, json, subprocess, sys, tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MOTION = ROOT / "motion"
CACHE = MOTION / ".cache" / "fonts"
PACCHETTI = {"@fontsource/titillium-web": "titillium-web", "@fontsource/roboto-mono": "roboto-mono"}
PESI = [("Titillium Web", "titillium-web", [400, 600, 700, 900]),
        ("Roboto Mono", "roboto-mono", [500, 700])]


def font_file(slug, peso):
    f = CACHE / slug / "package" / "files" / f"{slug}-latin-{peso}-normal.woff2"
    if f.exists():
        return f
    CACHE.mkdir(parents=True, exist_ok=True)
    pkg = next(p for p, s in PACCHETTI.items() if s == slug)
    out = subprocess.run(["npm", "pack", "-s", pkg], cwd=CACHE, check=True,
                         capture_output=True, text=True).stdout.strip().splitlines()[-1]
    with tarfile.open(CACHE / out) as t:
        t.extractall(CACHE / slug)
    return f


def font_css():
    righe = []
    for famiglia, slug, pesi in PESI:
        for p in pesi:
            b64 = base64.b64encode(font_file(slug, p).read_bytes()).decode()
            righe.append(f"@font-face{{font-family:'{famiglia}';font-weight:{p};font-style:normal;"
                         f"font-display:block;src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
    return "\n".join(righe)


def traccia_voce(nome):
    for f in (MOTION / "out" / nome / "voce.mp3", MOTION / "voce" / nome / "voce.mp3"):
        if f.exists():
            return f
    return None


def build(nome):
    src = MOTION / "src" / f"{nome}.src.html"
    if not src.exists():
        sys.exit(f"Sorgente mancante: {src}")
    html = src.read_text(encoding="utf-8")
    if "/*FONTS*/" not in html:
        sys.exit("Nel sorgente manca il segnaposto /*FONTS*/")
    html = html.replace("/*FONTS*/", font_css(), 1)
    durate = MOTION / "voce" / nome / "durate.json"
    if durate.exists():
        html = html.replace("/*DUR*/[]", json.dumps(json.loads(durate.read_text())), 1)
    voce = traccia_voce(nome)
    if voce:
        uri = "data:audio/mpeg;base64," + base64.b64encode(voce.read_bytes()).decode()
        html = html.replace('/*AUDIO*/""', json.dumps(uri), 1).replace('src="/*AUDIO*/"', f'src="{uri}"', 1)
    dist = MOTION / "dist"
    dist.mkdir(parents=True, exist_ok=True)
    out = dist / f"{nome}.html"
    out.write_text(html, encoding="utf-8")
    print(f"[build] {out.relative_to(ROOT)}  ({out.stat().st_size // 1024} KB)")
    return out


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    build(sys.argv[1])
