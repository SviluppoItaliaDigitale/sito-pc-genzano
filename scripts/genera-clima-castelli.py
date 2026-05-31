#!/usr/bin/env python3
"""Genera i dataset climatici pre-cotti per il Laboratorio meteo.

Scarica le serie storiche giornaliere (rianalisi ERA5 via Open-Meteo, CC BY 4.0 —
stessa famiglia di dati del Copernicus Climate Data Store) per Genzano di Roma,
le aggrega in dataset didattici e scrive:
  - static/open-data/clima-<slug>.json   (forma attesa dal renderer JS)
  - static/open-data/clima-manifest.json (indice degli esempi pronti)

Output JSON: { titolo, sottotitolo?, tipo: 'line'|'bar', unita, x[], serie[] }
Eseguibile in locale (rete) o in CI. Stdlib pura, nessuna dipendenza.
"""
import json
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "static" / "open-data"
ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"

# Genzano di Roma (centro abitato)
LAT, LON = 41.7085, 12.6916
ANNO_DA, ANNO_A = 2005, 2025  # anni interi disponibili nell'archivio ERA5

FONTE = "Rianalisi ERA5 via Open-Meteo (CC BY 4.0), allineata al Copernicus Climate Data Store."


def scarica():
    q = urllib.parse.urlencode({
        "latitude": LAT, "longitude": LON,
        "start_date": f"{ANNO_DA}-01-01", "end_date": f"{ANNO_A}-12-31",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "Europe/Rome",
    })
    url = f"{ARCHIVE}?{q}"
    print(f"GET {url}", file=sys.stderr)
    with urllib.request.urlopen(url, timeout=120) as r:
        return json.load(r)["daily"]


def media(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 1) if xs else None


def aggrega(d):
    """Ritorna strutture per anno e per mese (anno 2025)."""
    per_anno_tmax = defaultdict(list)
    per_anno_prec = defaultdict(list)
    per_anno_caldo = defaultdict(int)   # giorni con tmax >= 35
    per_anno_lug_tmax = defaultdict(list)
    mese_2025_max = defaultdict(list)
    mese_2025_min = defaultdict(list)

    for i, t in enumerate(d["time"]):
        anno, mese = int(t[:4]), int(t[5:7])
        tmax = d["temperature_2m_max"][i]
        tmin = d["temperature_2m_min"][i]
        prec = d["precipitation_sum"][i]
        if tmax is not None:
            per_anno_tmax[anno].append(tmax)
            if tmax >= 35:
                per_anno_caldo[anno] += 1
            if mese == 7:
                per_anno_lug_tmax[anno].append(tmax)
        if prec is not None:
            per_anno_prec[anno].append(prec)
        if anno == 2025:
            if tmax is not None:
                mese_2025_max[mese].append(tmax)
            if tmin is not None:
                mese_2025_min[mese].append(tmin)

    anni = list(range(ANNO_DA, ANNO_A + 1))
    return {
        "anni": anni,
        "lug_tmax": [media(per_anno_lug_tmax[a]) for a in anni],
        "prec_annua": [round(sum(per_anno_prec[a]), 0) if per_anno_prec[a] else None for a in anni],
        "giorni_caldo": [per_anno_caldo[a] for a in anni],
        "mesi": list(range(1, 13)),
        "mese_max": [media(mese_2025_max[m]) for m in range(1, 13)],
        "mese_min": [media(mese_2025_min[m]) for m in range(1, 13)],
    }


MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
        "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]


def scrivi(slug, payload):
    payload["fonte"] = FONTE
    (OUTDIR / f"clima-{slug}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  scritto clima-{slug}.json", file=sys.stderr)


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    g = aggrega(scarica())
    anni = [str(a) for a in g["anni"]]

    scrivi("luglio-temperature-genzano", {
        "titolo": f"Le estati a Genzano si scaldano? — luglio {ANNO_DA}–{ANNO_A}",
        "sottotitolo": "Temperatura massima media del mese di luglio",
        "tipo": "line", "unita": "°C", "x": anni,
        "serie": [{"nome": "Massima media di luglio", "colore": "#c1121f", "tratto": "solid",
                   "valori": g["lug_tmax"]}],
    })

    scrivi("pioggia-annuale-genzano", {
        "titolo": f"Quanta pioggia ogni anno a Genzano — {ANNO_DA}–{ANNO_A}",
        "sottotitolo": "Totale annuale di precipitazione",
        "tipo": "bar", "unita": "mm", "x": anni,
        "serie": [{"nome": "Pioggia annua", "colore": "#003366", "tratto": "solid",
                   "valori": g["prec_annua"]}],
    })

    scrivi("giorni-molto-caldi-genzano", {
        "titolo": f"Le giornate molto calde a Genzano — {ANNO_DA}–{ANNO_A}",
        "sottotitolo": "Numero di giorni con temperatura massima di almeno 35 °C",
        "tipo": "bar", "unita": "giorni", "x": anni,
        "serie": [{"nome": "Giorni ≥ 35 °C", "colore": "#b45309", "tratto": "solid",
                   "valori": g["giorni_caldo"]}],
    })

    scrivi("anno-temperature-genzano", {
        "titolo": "Un anno di temperature a Genzano — 2025",
        "sottotitolo": "Media mensile delle massime e delle minime",
        "tipo": "line", "unita": "°C", "x": MESI,
        "serie": [
            {"nome": "Massima media", "colore": "#c1121f", "tratto": "solid", "valori": g["mese_max"]},
            {"nome": "Minima media", "colore": "#0369a1", "tratto": "dash", "valori": g["mese_min"]},
        ],
    })

    manifest = [
        {"titolo": "Estati sempre più calde?", "file": "clima-luglio-temperature-genzano.json",
         "descr": "Temperatura massima media di luglio a Genzano, dal 2005 a oggi."},
        {"titolo": "La pioggia anno per anno", "file": "clima-pioggia-annuale-genzano.json",
         "descr": "Totale di pioggia caduta ogni anno a Genzano."},
        {"titolo": "Le giornate molto calde", "file": "clima-giorni-molto-caldi-genzano.json",
         "descr": "Quanti giorni all'anno superano i 35 °C a Genzano."},
        {"titolo": "Un anno di temperature", "file": "clima-anno-temperature-genzano.json",
         "descr": "Massime e minime mese per mese a Genzano nel 2025."},
    ]
    (OUTDIR / "clima-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("  scritto clima-manifest.json", file=sys.stderr)
    print("Fatto.", file=sys.stderr)


if __name__ == "__main__":
    main()
