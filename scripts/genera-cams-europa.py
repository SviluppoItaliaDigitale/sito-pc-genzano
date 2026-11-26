#!/usr/bin/env python3
"""Snapshot self-hosted della qualità dell'aria europea (modello Copernicus CAMS).

Perché esiste
-------------
Fino al 26/11/2026 la scheda «Aria Europa (CAMS)» del cruscotto leggeva le mappe dal
servizio WMS pubblico di ECMWF (`eccharts.ecmwf.int/wms/?token=public`). ECMWF ha
disattivato quel token («Access token disabled», HTTP 403), quindi la scheda restava
vuota (issue #2064). Open-Meteo pubblica gratis, con licenza CC BY 4.0, le stesse
previsioni europee CAMS (dominio `cams_europe`, circa 11 km): questo script le scarica
su una griglia regolare (1,5° × 2°) e le salva in `static/open-data/cams-europa.json`, che la
scheda legge in same-origin e disegna come celle colorate sulla mappa.

Comportamento
-------------
- Griglia 1,5° di latitudine × 2° di longitudine su 34-62 N, 12 O-36 E (circa 500 punti).
- Passi ogni 6 ore per 84 ore dal primo istante della previsione.
- Valori in µg/m³ moltiplicati per 10 e arrotondati (interi): file più leggero.
- Lo snapshot si rinnova al massimo ogni 11 ore: CAMS pubblica due volte al giorno e ogni
  riscrittura è un commit da circa 100 KB, quindi di più farebbe crescere il repository
  senza dati nuovi.
- Se la fonte non risponde, o risponde in modo incompleto, **lo snapshot esistente
  resta invariato** ed esce con codice 0: mai un deploy rotto né dati azzerati.

Uso: python3 scripts/genera-cams-europa.py [--forza]
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://air-quality-api.open-meteo.com/v1/air-quality"
OUT = Path(__file__).resolve().parent.parent / "static" / "open-data" / "cams-europa.json"
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/)"

LAT0, LAT1, DLAT = 34, 62, 1.5
LON0, LON1, DLON = -12.0, 36.0, 2.0
PASSO_ORE = 6
ORE_MAX = 84
BLOCCO = 100  # coordinate per richiesta
VARIABILI = [  # (chiave nello snapshot, variabile Open-Meteo)
    ("pm2p5", "pm2_5"),
    ("pm10", "pm10"),
    ("o3", "ozone"),
    ("no2", "nitrogen_dioxide"),
    ("so2", "sulphur_dioxide"),
    ("dust", "dust"),
]
ETA_MINIMA_ORE = 11.0


def griglia() -> tuple[list[float], list[float]]:
    lats, lons = [], []
    i = 0
    while LAT0 + i * DLAT <= LAT1 + 1e-9:
        lats.append(round(LAT0 + i * DLAT, 4))
        i += 1
    j = 0
    while LON0 + j * DLON <= LON1 + 1e-9:
        lons.append(round(LON0 + j * DLON, 4))
        j += 1
    return lats, lons


def richiedi(punti: list[tuple[float, float]]) -> list[dict]:
    params = (
        f"latitude={','.join(str(p[0]) for p in punti)}"
        f"&longitude={','.join(str(p[1]) for p in punti)}"
        f"&hourly={','.join(v for _, v in VARIABILI)}"
        "&forecast_days=5&domains=cams_europe&timezone=UTC"
    )
    ultimo: Exception | None = None
    for tentativo in range(3):
        try:
            req = urllib.request.Request(f"{API}?{params}", headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                dati = json.load(r)
            if isinstance(dati, dict):
                dati = [dati]
            if not isinstance(dati, list) or len(dati) != len(punti):
                raise ValueError("numero di punti restituiti diverso da quelli chiesti")
            return dati
        except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError, OSError) as e:
            ultimo = e
            time.sleep(8 * (tentativo + 1))
    raise RuntimeError(str(ultimo))


def scarica() -> dict:
    lats, lons = griglia()
    punti = [(la, lo) for la in lats for lo in lons]
    risposte: list[dict] = []
    for i in range(0, len(punti), BLOCCO):
        risposte.extend(richiedi(punti[i:i + BLOCCO]))
        time.sleep(1.5)

    tempi = risposte[0]["hourly"]["time"]
    # Istanti da tenere: dal primo disponibile, ogni PASSO_ORE, fino a ORE_MAX.
    idx = [k for k in range(0, min(len(tempi), ORE_MAX + 1), PASSO_ORE)]
    if len(idx) < 3:
        raise ValueError("previsione troppo corta")

    valori: dict[str, list[list[int]]] = {c: [] for c, _ in VARIABILI}
    for chiave, var in VARIABILI:
        for k in idx:
            riga = []
            for r in risposte:
                v = r["hourly"][var][k]
                riga.append(-1 if v is None else int(round(float(v) * 10)))
            valori[chiave].append(riga)

    # Una variabile quasi tutta vuota è una risposta rotta, non un dato.
    for chiave, passi in valori.items():
        tot = sum(len(p) for p in passi)
        vuoti = sum(1 for p in passi for v in p if v < 0)
        if tot == 0 or vuoti / tot > 0.2:
            raise ValueError(f"variabile {chiave}: {vuoti}/{tot} valori mancanti")

    return {
        "_snapshot": {
            "generato": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "fonte": API,
            "modello": "Copernicus Atmosphere Monitoring Service (CAMS) Europa, via Open-Meteo",
            "licenza": "CC BY 4.0 (Open-Meteo); dati CAMS: Copernicus, licenza aperta",
            "nota": "Valori in µg/m³ moltiplicati per 10; -1 = dato mancante. "
                    "Celle ordinate per latitudine crescente, poi longitudine crescente.",
        },
        "unita": "µg/m³ ×10",
        "lat": lats,
        "lon": lons,
        "tempi": [tempi[k] + "Z" for k in idx],
        "valori": valori,
    }


def eta_ore(t: str) -> float | None:
    try:
        gen = json.loads(t)["_snapshot"]["generato"]
        return (datetime.now(timezone.utc) - datetime.fromisoformat(gen)).total_seconds() / 3600
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--forza", action="store_true", help="ignora l'età minima dello snapshot")
    args = ap.parse_args()

    precedente = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    if precedente and not args.forza:
        eta = eta_ore(precedente)
        if eta is not None and eta < ETA_MINIMA_ORE:
            print(f"[ok] CAMS Europa: snapshot di {eta:.1f} h fa, nessun nuovo scarico.")
            return 0

    try:
        payload = scarica()
    except (RuntimeError, ValueError, KeyError, IndexError) as e:
        esistente = "presente" if OUT.exists() else "assente"
        print(f"[warn] CAMS Europa non scaricabile ({e}); snapshot {esistente} lasciato invariato.")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    n = len(payload["lat"]) * len(payload["lon"])
    print(f"[ok] CAMS Europa aggiornato: {n} punti × {len(payload['tempi'])} istanti → "
          f"{OUT.relative_to(OUT.parents[2])} ({OUT.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
