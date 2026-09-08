#!/usr/bin/env python3
"""
Coerenza fra le tabelle di dati nelle schede stampabili e i dataset aperti.

Nasce dall'audit esterno del 06/09/2026 (rilievo F07): la scheda sul clima
per le superiori riportava valori diversi dal dataset che dichiarava di usare
(2024: 922 mm contro 1078; 2025: 846 contro 1206; 2020 "n.d." contro 1178),
con media, minimi e conclusioni sbagliate di conseguenza.

Regola: una scheda che cita un file /open-data/<nome>.json deve riportare,
per ogni anno presente nelle sue tabelle, esattamente il valore del dataset
(arrotondato all'intero). Le tabelle sono lette riga per riga: ogni cella
con un anno del dataset "apre" un gruppo, e le celle numeriche che seguono
fino all'anno successivo appartengono a quel gruppo; il valore atteso deve
comparire fra quelle celle.

Uso:
  python3 scripts/check-dati-schede.py [--schede static/formazione/schede-stampabili]
Exit code = numero di discrepanze.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OPEN_DATA = ROOT / "static" / "open-data"

RE_JSON = re.compile(r"/open-data/([a-z0-9-]+\.json)")
RE_ROW = re.compile(r"<tr[^>]*>(.*?)</tr>", re.S | re.I)
RE_CELL = re.compile(r"<t[dh][^>]*>(.*?)</t[dh]>", re.S | re.I)
RE_TAG = re.compile(r"<[^>]+>")


def celle(riga_html: str) -> list[str]:
    return [RE_TAG.sub("", c).replace("\xa0", " ").strip() for c in RE_CELL.findall(riga_html)]


def numero(cella: str) -> int | None:
    t = cella.replace(".", "").replace(" ", "").replace(",", ".")
    try:
        return int(round(float(t)))
    except ValueError:
        return None


def carica_dataset(nome: str) -> dict[str, int] | None:
    path = OPEN_DATA / nome
    if not path.exists():
        return None
    d = json.loads(path.read_text(encoding="utf-8"))
    x = d.get("x")
    serie = d.get("serie") or []
    if not x or not serie or "valori" not in serie[0]:
        return None
    return {str(k): int(round(float(v))) for k, v in zip(x, serie[0]["valori"]) if v is not None}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--schede", default="static/formazione/schede-stampabili")
    args = ap.parse_args()

    errori: list[str] = []
    n_schede = 0
    n_confronti = 0

    for index in sorted((ROOT / args.schede).glob("*/index.html")):
        html = index.read_text(encoding="utf-8")
        dataset_citati = sorted(set(RE_JSON.findall(html)))
        if not dataset_citati:
            continue
        n_schede += 1
        rel = index.relative_to(ROOT)
        datasets = {n: carica_dataset(n) for n in dataset_citati}
        for nome, valori in datasets.items():
            if valori is None:
                errori.append(f"{rel}: cita /open-data/{nome} ma il file manca o non ha la forma x/serie")
        datasets = {n: v for n, v in datasets.items() if v}
        if not datasets:
            continue
        anni = set().union(*[set(v) for v in datasets.values()])

        for riga in RE_ROW.findall(html):
            cs = celle(riga)
            gruppi: list[tuple[str, list[int]]] = []
            for c in cs:
                if c in anni:
                    gruppi.append((c, []))
                elif gruppi:
                    n = numero(c)
                    if n is not None:
                        gruppi[-1][1].append(n)
            for anno, numeri in gruppi:
                if not numeri:
                    continue
                for nome, valori in datasets.items():
                    if anno not in valori:
                        continue
                    n_confronti += 1
                    atteso = valori[anno]
                    if atteso not in numeri:
                        errori.append(
                            f"{rel}: anno {anno} → nella riga ci sono {numeri}, ma /open-data/{nome} dice {atteso}"
                        )

    print(f"Schede che citano dataset: {n_schede}; confronti eseguiti: {n_confronti}")
    if errori:
        print(f"\n❌ {len(errori)} discrepanze fra schede e dataset:")
        for e in errori:
            print(f"  - {e}")
    else:
        print("✅ Tutti i valori annuali delle schede coincidono con i dataset aperti citati.")
    return len(errori)


if __name__ == "__main__":
    sys.exit(main())
