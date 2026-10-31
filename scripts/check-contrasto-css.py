#!/usr/bin/env python3
"""Contrasto delle coppie testo/sfondo dichiarate nella stessa regola CSS.

axe-core non sa calcolare il contrasto quando dietro c'è un gradiente o un'immagine
e lo segnala come «incompleto», che nel gate non blocca: così il pulsante «Allerte
Meteo» della home (bianco su #FF6600, 2,94:1) è rimasto online fino all'audit
esterno del 31/10/2026 (A03). Questo controllo legge i fogli di stile e, per ogni
regola che dichiara sia `color` sia uno sfondo a tinta unita, calcola il rapporto
WCAG (variabili di :root risolte, alfa ignorata: in quel caso la regola si salta).

Uso: python3 scripts/check-contrasto-css.py [FILE.css ...]
Esce con 1 se una coppia è sotto 4,5:1. Un'eccezione motivata si dichiara con il
commento /* contrasto-ok: motivo */ dentro la regola.
"""
import re
import sys
from pathlib import Path

FILE_PREDEFINITI = [
    "themes/flavour-pcgenzano/static/css/custom.css",
    "static/app-shared/app-common.css",
    "themes/flavour-pcgenzano/static/css/a11y-toolbar.css",
]
SOGLIA = 4.5
NOMI = {"white": "ffffff", "black": "000000"}


def esadecimale(valore, variabili):
    v = valore.strip().lower()
    v = re.sub(r"\s*!important\s*$", "", v)
    m = re.fullmatch(r"var\((--[\w-]+)(?:\s*,\s*([^)]+))?\)", v)
    if m:
        v = variabili.get(m.group(1), (m.group(2) or "").strip())
        return esadecimale(v, variabili) if v else None
    if v in NOMI:
        return NOMI[v]
    m = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{6})", v)
    if not m:
        return None
    h = m.group(1)
    return "".join(c * 2 for c in h) if len(h) == 3 else h


def luminanza(h):
    canali = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    canali = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canali]
    return 0.2126 * canali[0] + 0.7152 * canali[1] + 0.0722 * canali[2]


def rapporto(a, b):
    la, lb = luminanza(a), luminanza(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


def controlla(percorso):
    testo = Path(percorso).read_text(encoding="utf-8")
    variabili = {}
    for m in re.finditer(r":root\s*\{([^{}]*)\}", testo):
        for nome, val in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", m.group(1)):
            variabili.setdefault(nome, val.strip())
    errori = []
    for m in re.finditer(r"([^{}]+)\{([^{}]*)\}", testo):
        selettore, corpo = m.group(1).strip(), m.group(2)
        if "contrasto-ok" in corpo:
            continue
        senza_commenti = re.sub(r"/\*.*?\*/", "", corpo, flags=re.S)
        colore = re.search(r"(?:^|[;\s])color\s*:\s*([^;]+)", senza_commenti)
        sfondo = re.search(r"background(?:-color)?\s*:\s*([^;]+)", senza_commenti)
        if not colore or not sfondo:
            continue
        fg = esadecimale(colore.group(1), variabili)
        bg = esadecimale(sfondo.group(1), variabili)
        if not fg or not bg:
            continue
        r = rapporto(fg, bg)
        if r < SOGLIA:
            riga = testo[: m.start(2)].count("\n") + 1
            sel = re.sub(r"\s+", " ", re.sub(r"/\*.*?\*/", "", selettore, flags=re.S)).strip()
            errori.append(f"{percorso}:{riga}: {sel[:90]} → #{fg} su #{bg} = {r:.2f}:1")
    return errori


def main():
    file = sys.argv[1:] or [f for f in FILE_PREDEFINITI if Path(f).exists()]
    errori = []
    for f in file:
        errori += controlla(f)
    for e in errori:
        print(e)
    print(f"{len(errori)} coppie sotto {SOGLIA}:1 in {len(file)} file.")
    return 1 if errori else 0


if __name__ == "__main__":
    sys.exit(main())
