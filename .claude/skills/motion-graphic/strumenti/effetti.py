#!/usr/bin/env python3
"""Effetti sonori gratuiti fatti in codice (solo numpy), per i video quando non si possono generare altrove.
Uso: python3 effetti.py CARTELLA  → scrive tuono, vento, pioggia, frana, avviso, pop, passaggio (WAV 48 kHz mono).

Sono suoni originali, sintetizzati da rumore filtrato e toni: nessun file di terzi, nessuna licenza da citare.
Deterministici (seme fisso): lo stesso comando dà sempre gli stessi file. Il livello lo decide il mix.
"""
import sys
import wave
from pathlib import Path

import numpy as np

SR = 48000


def rumore(n, seme):
    return np.random.default_rng(seme).standard_normal(n)


def passa(x, basso=None, alto=None):
    """Filtro in frequenza: tiene la banda fra `basso` e `alto` (Hz), con bordi morbidi."""
    f = np.fft.rfftfreq(len(x), 1 / SR)
    g = np.ones_like(f)
    if basso:
        g *= 1 / (1 + (basso / np.maximum(f, 1e-6)) ** 4)
    if alto:
        g *= 1 / (1 + (f / alto) ** 4)
    return np.fft.irfft(np.fft.rfft(x) * g, len(x))


def inviluppo(n, attacco, rilascio):
    t = np.arange(n) / SR
    d = n / SR
    e = np.minimum(1, t / max(attacco, 1e-4)) * np.minimum(1, (d - t) / max(rilascio, 1e-4))
    return np.clip(e, 0, 1)


def norma(x, picco=0.7):
    return x / (np.max(np.abs(x)) + 1e-9) * picco


def tuono(d=4.5):
    n = int(d * SR)
    t = np.arange(n) / SR
    x = passa(rumore(n, 11), basso=25, alto=160)
    # rimbombo: tre ondate che si spengono
    e = np.exp(-t * 1.1) + 0.6 * np.exp(-((t - 0.9) ** 2) / 0.08) + 0.4 * np.exp(-((t - 1.9) ** 2) / 0.2)
    schiocco = passa(rumore(n, 12), basso=200, alto=1800) * np.exp(-t * 14) * 0.35
    return norma((x * e + schiocco) * inviluppo(n, 0.02, 1.2))


def vento(d=8.0):
    n = int(d * SR)
    t = np.arange(n) / SR
    raffica = 0.55 + 0.45 * np.sin(2 * np.pi * 0.21 * t + 0.6) * np.sin(2 * np.pi * 0.07 * t + 1.3)
    basso = passa(rumore(n, 21), basso=90, alto=500)
    fischio = passa(rumore(n, 22), basso=500, alto=1400) * (0.3 + 0.7 * raffica ** 2) * 0.5
    return norma((basso * raffica + fischio) * inviluppo(n, 1.2, 1.5), 0.6)


def pioggia(d=8.0):
    n = int(d * SR)
    x = passa(rumore(n, 31), basso=1500, alto=9000)
    gocce = np.zeros(n)
    rng = np.random.default_rng(32)
    for p in rng.integers(0, n - 400, int(d * 60)):
        gocce[p:p + 300] += np.exp(-np.arange(300) / 40) * rng.uniform(0.2, 1)
    return norma((x * 0.6 + passa(gocce, basso=800, alto=5000) * 0.8) * inviluppo(n, 1.0, 1.5), 0.5)


def frana(d=4.5):
    n = int(d * SR)
    t = np.arange(n) / SR
    rombo = passa(rumore(n, 41), basso=30, alto=220) * (0.4 + 0.6 * np.exp(-((t - 1.6) ** 2) / 1.2))
    sassi = np.zeros(n)
    rng = np.random.default_rng(42)
    for p in rng.integers(int(0.3 * SR), n - 3000, 70):
        k = rng.integers(600, 2400)
        sassi[p:p + k] += rumore(k, int(p)) * np.exp(-np.arange(k) / (k / 5)) * rng.uniform(0.2, 0.9)
    sassi = passa(sassi, basso=300, alto=3500) * 0.35
    return norma((rombo + sassi) * inviluppo(n, 0.5, 1.4))


def avviso(d=2.4):
    """Avviso generico sul telefono: due toni brevi e una vibrazione. Non imita nessun segnale ufficiale."""
    n = int(d * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for t0, f in ((0.05, 880), (0.38, 1175)):
        m = (t >= t0) & (t < t0 + 0.24)
        tt = t[m] - t0
        x[m] += np.sin(2 * np.pi * f * tt) * np.minimum(1, tt / 0.01) * np.exp(-tt * 6)
    m = (t >= 0.9) & (t < 1.9)
    tt = t[m] - 0.9
    x[m] += 0.5 * np.sin(2 * np.pi * 150 * tt) * (np.sin(2 * np.pi * 14 * tt) > 0) * np.minimum(1, (1.0 - tt) / 0.1)
    return norma(x, 0.6)


def pop(d=0.35):
    n = int(d * SR)
    t = np.arange(n) / SR
    f = 520 + 380 * np.exp(-t * 30)
    return norma(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 16) * np.minimum(1, t / 0.004), 0.6)


def passaggio(d=1.0):
    n = int(d * SR)
    t = np.arange(n) / SR
    x = passa(rumore(n, 71), basso=400, alto=5000)
    e = np.exp(-((t - 0.45) ** 2) / 0.03)
    return norma(x * e, 0.5)


EFFETTI = {"tuono": tuono, "vento": vento, "pioggia": pioggia, "frana": frana,
           "avviso": avviso, "pop": pop, "passaggio": passaggio}


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    for nome, fn in EFFETTI.items():
        x = np.clip(fn(), -1, 1)
        with wave.open(str(dest / f"{nome}.wav"), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(SR)
            w.writeframes((x * 32767).astype("<i2").tobytes())
        print(f"{nome}.wav  {len(x) / SR:.2f} s")


if __name__ == "__main__":
    main()
