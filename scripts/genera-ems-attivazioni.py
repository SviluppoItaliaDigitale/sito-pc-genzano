#!/usr/bin/env python3
"""Snapshot self-hosted delle attivazioni Copernicus EMS Rapid Mapping.

Perché esiste
-------------
L'API pubblica `rapidmapping.emergency.copernicus.eu/backend/dashboard-api/`
risponde 200 ma **non espone più l'header `Access-Control-Allow-Origin`**
(verificato il 24/08/2026): dal browser la fetch della scheda EMS del cruscotto
viene bloccata dalla same-origin policy e la scheda falliva in silenzio,
mostrando "Errore caricamento" (o l'ultimo dato in cache locale, se presente).

Il server non ha questo limite: il CORS riguarda solo i browser. Questo script
gira nella pipeline di deploy, scarica l'elenco e lo salva come file statico in
`static/open-data/ems-attivazioni.json`, che la scheda legge in same-origin.

Comportamento
-------------
- Se il download riesce: riscrive lo snapshot (schema identico all'API, più un
  blocco `_snapshot` con l'orario di generazione e la fonte).
- Se fallisce: **lascia intatto lo snapshot esistente** ed esce con codice 0,
  così un'API momentaneamente giù non azzera i dati né rompe il deploy.

Uso: python3 scripts/genera-ems-attivazioni.py [--limit 50]
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations-info/"
OUT = Path(__file__).resolve().parent.parent / "static" / "open-data" / "ems-attivazioni.json"
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/)"
CAMPI = (
    "code", "name", "category", "countries", "eventTime", "activationTime",
    "lastUpdate", "closed", "centroid", "n_aois", "n_products", "gdacsId",
)


def scarica(limit: int) -> list[dict]:
    req = urllib.request.Request(f"{API}?limit={limit}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        dati = json.load(r)
    risultati = dati.get("results")
    if not isinstance(risultati, list):
        raise ValueError("risposta senza campo 'results'")
    return risultati


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--limit", type=int, default=50, help="attivazioni da richiedere (default: 50)")
    args = ap.parse_args()

    try:
        risultati = scarica(args.limit)
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError, OSError) as e:
        esistente = "presente" if OUT.exists() else "assente"
        print(f"[warn] EMS non scaricabile ({e}); snapshot {esistente} lasciato invariato.")
        return 0

    snellite = [{k: a.get(k) for k in CAMPI if k in a} for a in risultati]
    aperte = sum(1 for a in snellite if not a.get("closed"))
    payload = {
        "_snapshot": {
            "generato": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "fonte": API,
            "licenza": "Copernicus Emergency Management Service — dati pubblici",
            "nota": "Copia locale: l'API non espone CORS, il browser non può leggerla direttamente.",
        },
        "count": len(snellite),
        "results": snellite,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    precedente = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    nuovo = json.dumps(payload, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    # confronto senza il timestamp: evita commit a vuoto quando i dati non cambiano
    def senza_ts(t: str) -> str:
        try:
            d = json.loads(t)
            d.pop("_snapshot", None)
            return json.dumps(d, ensure_ascii=False, sort_keys=True)
        except Exception:
            return t

    if precedente and senza_ts(precedente) == senza_ts(nuovo):
        print(f"[ok] EMS invariato: {len(snellite)} attivazioni ({aperte} aperte).")
        return 0

    OUT.write_text(nuovo, encoding="utf-8")
    print(f"[ok] EMS aggiornato: {len(snellite)} attivazioni ({aperte} aperte) → {OUT.relative_to(OUT.parents[2])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
