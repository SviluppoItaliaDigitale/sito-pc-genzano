#!/usr/bin/env python3
"""Snapshot degli hotspot termici NASA FIRMS sull'Italia (incendi attivi da satellite).

FIRMS (Fire Information for Resource Management System) pubblica i punti caldi
rilevati dai sensori VIIRS e MODIS poche ore dopo il passaggio del satellite.
Complementa EFFIS, già presente nel cruscotto come layer cartografico: qui si
ottiene l'elenco numerico dei punti, con potenza radiativa e affidabilità.

🔴 CHIAVE OBBLIGATORIA — l'API richiede una MAP_KEY gratuita, da richiedere su
https://firms.modaps.eosdis.nasa.gov/api/area/ e da mettere nel segreto del
repository FIRMS_MAP_KEY. SENZA CHIAVE QUESTO SCRIPT NON SCRIVE NULLA ed esce 0:
la scheda della Sala situazioni resta semplicemente spenta. Non esistono dati di
riempimento, perché un punto d'incendio inventato è peggio di una scheda vuota.

🔴 ONESTÀ DEL DATO — un hotspot NON è un incendio confermato. È una anomalia
termica rilevata dallo spazio: può essere un incendio boschivo, ma anche una
fiaccola industriale, un forno, una bruciatura agricola o un falso positivo su
superfici molto calde. La scheda lo dice, e il campo "affidabilita" della fonte
viene riportato tale e quale invece di essere nascosto.

Fail-safe: qualunque errore lascia lo snapshot invariato ed esce 0.
"""
from __future__ import annotations

import csv
import io as _io
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/)"
USCITA = pathlib.Path(__file__).resolve().parent.parent / "static" / "open-data" / "incendi-firms.json"
# Riquadro dell'Italia: ovest,sud,est,nord (come vuole l'API).
AREA = "6.4,35.2,18.8,47.2"
SENSORI = ("VIIRS_SNPP_NRT", "VIIRS_NOAA20_NRT")
GIORNI = 1  # solo le ultime 24 ore: oltre non è più "tempo reale"
BASE = "https://firms.modaps.eosdis.nasa.gov/api/area/csv/{key}/{sensore}/{area}/{giorni}"


def ora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def scarica(url: str, tentativi: int = 2) -> str:
    ultimo = None
    for n in range(tentativi):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            ultimo = e
            if n < tentativi - 1:
                time.sleep(3)
    raise RuntimeError(f"FIRMS non raggiungibile: {ultimo}")


def num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def main() -> int:
    chiave = (os.environ.get("FIRMS_MAP_KEY") or "").strip()
    if not chiave:
        print("[salto] FIRMS_MAP_KEY non configurata: nessuno snapshot scritto, "
              "la scheda resta spenta (nessun dato di riempimento).", file=sys.stderr)
        return 0

    punti, sensori_ok = [], []
    for sensore in SENSORI:
        url = BASE.format(key=chiave, sensore=sensore, area=AREA, giorni=GIORNI)
        try:
            testo = scarica(url)
        except RuntimeError as e:
            print(f"[avviso] {sensore}: {e}", file=sys.stderr)
            continue
        if "Invalid MAP_KEY" in testo or testo.lstrip().startswith("<"):
            print(f"[avviso] {sensore}: chiave rifiutata dalla fonte.", file=sys.stderr)
            continue
        righe = list(csv.DictReader(_io.StringIO(testo)))
        sensori_ok.append(sensore)
        for r in righe:
            la, lo = num(r.get("latitude")), num(r.get("longitude"))
            if la is None or lo is None:
                continue
            punti.append({
                "lat": round(la, 4),
                "lon": round(lo, 4),
                "data": r.get("acq_date") or "",
                "ora_utc": r.get("acq_time") or "",
                "sensore": r.get("instrument") or sensore,
                "satellite": r.get("satellite") or "",
                # "confidence" VIIRS e' testuale (low/nominal/high): si riporta
                # tale e quale, senza tradurla in una certezza che non ha.
                "affidabilita": r.get("confidence") or "",
                "potenza_radiativa_mw": num(r.get("frp")),
                "giorno_notte": r.get("daynight") or "",
            })
        time.sleep(1)

    if not sensori_ok:
        print("[fail-safe] nessun sensore raggiungibile: snapshot lasciato invariato.", file=sys.stderr)
        return 0

    punti.sort(key=lambda p: (p["data"], p["ora_utc"]), reverse=True)
    dati = {
        "_snapshot": {
            "generato": ora(),
            "fonte": "NASA FIRMS — VIIRS (Suomi-NPP e NOAA-20), dati near real-time",
            "fonte_url": "https://firms.modaps.eosdis.nasa.gov/",
            "sensori": sensori_ok,
            "finestra_ore": GIORNI * 24,
            "punti": len(punti),
            "avvertenza": (
                "Un punto caldo non è un incendio confermato: è un'anomalia termica "
                "vista dal satellite, che può essere anche una fiaccola industriale, "
                "una bruciatura agricola o un falso positivo. La segnalazione al 112 "
                "vale su ciò che si vede a terra, non su questa mappa."
            ),
        },
        "punti": punti[:400],
    }

    USCITA.parent.mkdir(parents=True, exist_ok=True)
    if USCITA.exists():
        try:
            if json.loads(USCITA.read_text(encoding="utf-8")).get("punti") == dati["punti"]:
                print(f"Nessuna variazione ({len(punti)} punti): file invariato.")
                return 0
        except ValueError:
            pass
    USCITA.write_text(json.dumps(dati, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Scritto {USCITA.name}: {len(punti)} punti caldi nelle ultime {GIORNI*24} ore "
          f"({', '.join(sensori_ok)}).")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"[fail-safe] errore non previsto, snapshot invariato: {e}", file=sys.stderr)
        sys.exit(0)
