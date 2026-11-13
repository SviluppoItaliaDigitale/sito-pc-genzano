#!/usr/bin/env python3
"""Prove veloci del generatore delle mappe meteo professionali, senza rete.

Gira nel workflow `mappe-meteo-professionali.yml` prima del giro vero, e in
locale con `python3 scripts/prova-mappe-meteo-pro.py`. Ogni prova nasce da un
errore trovato (13/11/2026): chiedere a ECMWF un parametro che a quello step non
esiste fa fallire tutto il prelievo al suolo; una tavolozza con meno colori dei
livelli rompe il disegno; una carta senza disegnatore sparisce in silenzio.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

errori: list[str] = []


def verifica(cond: bool, msg: str) -> None:
    if not cond:
        errori.append(msg)


def main() -> int:
    from mappe_meteo_pro import disegna as d
    from mappe_meteo_pro.config import ORE_STANDARD, PRODOTTI
    from mappe_meteo_pro.prodotti import DISEGNATORI
    from mappe_meteo_pro.scarica import _ecmwf_raffica

    # Raffica IFS: 10fg fino a +90, 10fg3 oltre (indici Open Data del 13/11/2026).
    verifica(_ecmwf_raffica(0) == "10fg", "ECMWF +0: atteso 10fg")
    verifica(_ecmwf_raffica(90) == "10fg", "ECMWF +90: atteso 10fg")
    verifica(_ecmwf_raffica(96) == "10fg3", "ECMWF +96: atteso 10fg3")
    for ora in ORE_STANDARD:
        verifica(_ecmwf_raffica(ora) in ("10fg", "10fg3"), f"ECMWF +{ora}: parametro raffica non valido")

    for pid, meta in PRODOTTI.items():
        verifica(pid in DISEGNATORI, f"prodotto {pid} senza disegnatore")
        verifica(meta.get("gruppo", "esperti") in ("tutti", "esperti"), f"prodotto {pid}: gruppo non valido")
        verifica(bool(meta.get("richiede")), f"prodotto {pid}: campi richiesti mancanti")

    # Tavolozze a fasce: colori = intervalli (+1 per ogni estremo aperto).
    for nome, liv, cmap, estremi in (
        ("raffiche", d.LIV_RAFFICHE, d.CMAP_RAFFICHE, 1),
        ("pioggia totale", d.LIV_PIOGGIA_TOT, d.CMAP_PIOGGIA_TOT, 1),
        ("neve", d.LIV_NEVE, d.CMAP_NEVE, 1),
        ("nubi", d.LIV_NUBI, d.CMAP_NUBI, 0),
        ("pioggia 6 ore", d.LIV_PIOGGIA, d.CMAP_PIOGGIA, 1),
    ):
        verifica(cmap.N >= len(liv) - 1 + estremi, f"tavolozza {nome}: {cmap.N} colori per {len(liv)} livelli")

    if errori:
        print("Prove delle mappe meteo NON superate:")
        for e in errori:
            print(f"  - {e}")
        return 1
    print(f"Prove delle mappe meteo superate ({len(PRODOTTI)} carte).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
