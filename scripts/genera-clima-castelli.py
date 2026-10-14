#!/usr/bin/env python3
"""Genera i dataset climatici pre-cotti per il Laboratorio meteo.

Scarica le serie storiche giornaliere per Genzano di Roma (rianalisi ERA5-Land per
le temperature ed ERA5 per la pioggia, del Copernicus Climate Change Service, via
Open-Meteo, CC BY 4.0), le aggrega in dataset didattici e scrive:
  - static/open-data/clima-<slug>.json   (forma attesa dal renderer JS)
  - static/open-data/clima-manifest.json (indice degli esempi pronti)

Output JSON: { titolo, sottotitolo?, tipo: 'line'|'bar', unita, x[], serie[] }
Eseguibile in locale (rete) o in CI. Stdlib pura, nessuna dipendenza.

🔴 Il modello si chiede sempre (MODELLO): senza, l'archivio di Open-Meteo usa il
«best match», che fino al 2016 dà ERA5-Land ed ERA5 e dal 2017 il modello IFS
dell'ECMWF, più caldo e più piovoso a Genzano. Una serie che cambia fonte a metà
non è omogenea e mostra tendenze che sono solo il cambio di modello: verificato il
14/10/2026 confrontando i singoli modelli: prima della correzione l'aumento di
luglio fra i decenni 2005-2014 e 2016-2025 risultava di 2,5 °C invece di 1,6 e i
giorni a 35 °C «comparivano» nel 2017. «era5_seamless» dà ERA5-Land per le temperature ed ERA5 per pioggia e
vento, uguale per tutto il periodo, e coincide con i valori di prima fino al 2016.
"""
import datetime
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTDIR = ROOT / "static" / "open-data"
ARCHIVE = "https://archive-api.open-meteo.com/v1/archive"

# Genzano di Roma (centro abitato)
LAT, LON = 41.7085, 12.6916
# Rianalisi omogenea per tutto il periodo: vedi la nota in testa al file.
MODELLO = "era5_seamless"
# Ultimo anno solare completo (l'archivio ERA5 è affidabile fino all'anno scorso),
# e finestra di 20 anni indietro. Calcolato dinamicamente: a un refresh periodico
# i dataset si estendono da soli all'ultimo anno disponibile.
# Ultimo anno solare completo, con dieci giorni di margine: la rianalisi arriva a
# circa cinque giorni fa, e il giro del 1° gennaio troverebbe gli ultimi giorni di
# dicembre ancora vuoti (totali dell'anno sottostimati fino a febbraio).
ANNO_A = (datetime.date.today() - datetime.timedelta(days=10)).year - 1
ANNO_DA = ANNO_A - 20

FONTE = ("Rianalisi ERA5-Land per le temperature ed ERA5 per la pioggia, del Copernicus Climate "
         "Change Service, via Open-Meteo (modello era5_seamless, CC BY 4.0).")


def scarica():
    q = urllib.parse.urlencode({
        "latitude": LAT, "longitude": LON,
        "start_date": f"{ANNO_DA}-01-01", "end_date": f"{ANNO_A}-12-31",
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "Europe/Rome",
        "models": MODELLO,
    })
    url = f"{ARCHIVE}?{q}"
    print(f"GET {url}", file=sys.stderr)
    # Retry sugli errori di rete transitori dei runner CI (DNS, timeout, 5xx) e sul
    # 429 (troppe richieste dallo stesso indirizzo, frequente sulle reti condivise):
    # 5 tentativi con attesa crescente. Gli altri 4xx non si ritentano.
    for tentativo in range(5):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                return json.load(r)["daily"]
        except urllib.error.HTTPError as e:
            if (e.code < 500 and e.code != 429) or tentativo == 4:
                raise
        except (urllib.error.URLError, OSError):
            if tentativo == 4:
                raise
        attesa = 20 * (tentativo + 1)
        print(f"[retry] errore di rete, riprovo tra {attesa}s", file=sys.stderr)
        time.sleep(attesa)


def media(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 1) if xs else None


def aggrega(d):
    """Ritorna strutture per anno e per mese (anno 2025)."""
    per_anno_tmax = defaultdict(list)
    per_anno_prec = defaultdict(list)
    per_anno_caldo = defaultdict(int)   # giorni con tmax >= 35
    per_anno_30 = defaultdict(int)      # giorni con tmax >= 30
    per_anno_lug_tmax = defaultdict(list)
    mese_ult_max = defaultdict(list)   # mesi dell'ultimo anno completo (ANNO_A)
    mese_ult_min = defaultdict(list)

    for i, t in enumerate(d["time"]):
        anno, mese = int(t[:4]), int(t[5:7])
        tmax = d["temperature_2m_max"][i]
        tmin = d["temperature_2m_min"][i]
        prec = d["precipitation_sum"][i]
        if tmax is not None:
            per_anno_tmax[anno].append(tmax)
            if tmax >= 35:
                per_anno_caldo[anno] += 1
            if tmax >= 30:
                per_anno_30[anno] += 1
            if mese == 7:
                per_anno_lug_tmax[anno].append(tmax)
        if prec is not None:
            per_anno_prec[anno].append(prec)
        if anno == ANNO_A:
            if tmax is not None:
                mese_ult_max[mese].append(tmax)
            if tmin is not None:
                mese_ult_min[mese].append(tmin)

    anni = list(range(ANNO_DA, ANNO_A + 1))
    return {
        "anni": anni,
        "lug_tmax": [media(per_anno_lug_tmax[a]) for a in anni],
        "prec_annua": [round(sum(per_anno_prec[a]), 0) if per_anno_prec[a] else None for a in anni],
        "giorni_caldo": [per_anno_caldo[a] for a in anni],
        "giorni_30": [per_anno_30[a] for a in anni],
        "mesi": list(range(1, 13)),
        "mese_max": [media(mese_ult_max[m]) for m in range(1, 13)],
        "mese_min": [media(mese_ult_min[m]) for m in range(1, 13)],
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

    # Esempio del Laboratorio dal 14/10/2026: nella cella della rianalisi, che sta a
    # 468 m e smussa i picchi, i 35 °C non si raggiungono quasi mai (2 giorni nel
    # 2017 in vent'anni); la soglia dei 30 °C mostra invece come cambiano le estati.
    # Il file dei 35 °C resta fra i dati aperti con lo stesso indirizzo.
    scrivi("giorni-30-gradi-genzano", {
        "titolo": f"Le giornate da 30 °C a Genzano — {ANNO_DA}–{ANNO_A}",
        "sottotitolo": "Numero di giorni con temperatura massima di almeno 30 °C",
        "tipo": "bar", "unita": "giorni", "x": anni,
        "serie": [{"nome": "Giorni con almeno 30 °C", "colore": "#b45309", "tratto": "solid",
                   "valori": g["giorni_30"]}],
    })

    scrivi("anno-temperature-genzano", {
        "titolo": f"Un anno di temperature a Genzano — {ANNO_A}",
        "sottotitolo": "Media mensile delle massime e delle minime",
        "tipo": "line", "unita": "°C", "x": MESI,
        "serie": [
            {"nome": "Massima media", "colore": "#c1121f", "tratto": "solid", "valori": g["mese_max"]},
            {"nome": "Minima media", "colore": "#0369a1", "tratto": "dash", "valori": g["mese_min"]},
        ],
    })

    manifest = [
        {"titolo": "Estati sempre più calde?", "file": "clima-luglio-temperature-genzano.json",
         "descr": f"Temperatura massima media di luglio a Genzano, dal {ANNO_DA} al {ANNO_A}."},
        {"titolo": "La pioggia anno per anno", "file": "clima-pioggia-annuale-genzano.json",
         "descr": "Totale di pioggia caduta ogni anno a Genzano."},
        {"titolo": "Le giornate da 30 °C", "file": "clima-giorni-30-gradi-genzano.json",
         "descr": "Quanti giorni all'anno la massima arriva ad almeno 30 °C a Genzano."},
        {"titolo": "Un anno di temperature", "file": "clima-anno-temperature-genzano.json",
         "descr": f"Massime e minime mese per mese a Genzano nel {ANNO_A}."},
    ]
    (OUTDIR / "clima-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print("  scritto clima-manifest.json", file=sys.stderr)
    print("Fatto.", file=sys.stderr)


if __name__ == "__main__":
    main()
