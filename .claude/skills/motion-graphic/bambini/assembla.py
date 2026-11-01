"""Assembla un video per bambini dallo stampo comune (base.html + icone.js) e dai pezzi del video.
Uso: python3 assembla.py <nome-sorgente> <prefisso-pezzi> "<titolo>"  → scrive motion/src/<nome>.src.html"""
import sys
from pathlib import Path
K = Path(__file__).resolve().parent
RADICE = K.parents[3]
nome, pref, titolo = sys.argv[1], sys.argv[2], sys.argv[3]
t = (K / "base.html").read_text()
t = t.replace("@@TITOLO", titolo)
t = t.replace("//@@CONFIG", (K / "pezzi" / f"{pref}-cfg.js").read_text())
t = t.replace("//@@DISEGNI", (K / "icone.js").read_text() + "\n" + (K / "pezzi" / f"{pref}-dis.js").read_text())
t = t.replace("//@@ANIM", (K / "pezzi" / f"{pref}-anim.js").read_text())
(RADICE / "motion" / "src" / f"{nome}.src.html").write_text(t)
print("scritto", nome)
