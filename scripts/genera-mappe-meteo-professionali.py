#!/usr/bin/env python3
"""Genera le mappe meteo professionali per l'Italia (dati aperti GFS, ECMWF, ICON-EU).

Uso:
    python3 scripts/genera-mappe-meteo-professionali.py --anteprima --domini italia
    python3 scripts/genera-mappe-meteo-professionali.py --modelli gfs,ecmwf,icon-eu \\
        --domini italia,europa --ore standard --pubblica

I file generati NON vanno committati su main: si pubblicano sul ramo orfano
`mappe-meteo-dati` (un solo commit, storia azzerata) e la pagina li legge da
raw.githubusercontent.com. Così il deploy del sito non parte a ogni corsa.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mappe_meteo_pro.cli import main

if __name__ == "__main__":
    sys.exit(main())
