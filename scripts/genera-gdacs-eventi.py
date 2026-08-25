#!/usr/bin/env python3
"""Snapshot self-hosted delle allerte globali GDACS (Global Disaster Alert
and Coordination System, ONU/Commissione europea).

Perché esiste
-------------
La Sala situazioni (/monitor/) mostra le allerte disastri a scala mondiale
accanto alle attivazioni Copernicus EMS. L'API pubblica di GDACS non espone
in modo affidabile gli header CORS ai browser, quindi — stesso pattern dello
snapshot EMS (scripts/genera-ems-attivazioni.py) — il download avviene qui in
CI e il file statico `static/open-data/gdacs-eventi.json` viene letto dalla
pagina in same-origin.

Comportamento
-------------
- Se il download riesce: riscrive lo snapshot (campi essenziali degli eventi
  correnti + blocco `_snapshot` con orario e fonte).
- Se fallisce: lascia intatto lo snapshot esistente ed esce 0 — mai un deploy
  rotto per una fonte terza, mai dati azzerati.

Uso: python3 scripts/genera-gdacs-eventi.py
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/EVENTS4APP"
OUT = Path(__file__).resolve().parent.parent / "static" / "open-data" / "gdacs-eventi.json"
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/)"
CAMPI = (
    "eventid", "episodeid", "eventtype", "eventname", "name", "description",
    "alertlevel", "country", "fromdate", "todate", "datemodified", "iso3",
)


def scarica() -> list[dict]:
    req = urllib.request.Request(API, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        dati = json.load(r)
    feats = dati.get("features")
    if not isinstance(feats, list):
        raise ValueError("risposta senza campo 'features'")
    eventi = []
    for f in feats:
        p = f.get("properties", f) or {}
        e = {k: p.get(k) for k in CAMPI if p.get(k) not in (None, "")}
        sev = p.get("severitydata")
        if isinstance(sev, dict) and sev.get("severitytext"):
            e["severitytext"] = sev.get("severitytext")
        geom = f.get("geometry") or {}
        coords = geom.get("coordinates")
        if isinstance(coords, list) and len(coords) >= 2 and all(
            isinstance(c, (int, float)) for c in coords[:2]
        ):
            e["lon"], e["lat"] = coords[0], coords[1]
        if e.get("eventid"):
            eventi.append(e)
    return eventi


def main() -> int:
    try:
        eventi = scarica()
    except (urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError, OSError) as e:
        esistente = "presente" if OUT.exists() else "assente"
        print(f"[warn] GDACS non scaricabile ({e}); snapshot {esistente} lasciato invariato.")
        return 0

    rilevanti = sum(1 for e in eventi if str(e.get("alertlevel", "")).lower() in ("orange", "red"))
    payload = {
        "_snapshot": {
            "generato": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "fonte": API,
            "licenza": "GDACS — Global Disaster Alert and Coordination System (dati pubblici UE/ONU)",
            "nota": "Copia locale per lettura same-origin dalla Sala situazioni.",
        },
        "count": len(eventi),
        "events": eventi,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    precedente = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    nuovo = json.dumps(payload, ensure_ascii=False, indent=1, sort_keys=True) + "\n"

    def senza_ts(t: str) -> str:
        try:
            d = json.loads(t)
            d.pop("_snapshot", None)
            return json.dumps(d, ensure_ascii=False, sort_keys=True)
        except Exception:
            return t

    if precedente and senza_ts(precedente) == senza_ts(nuovo):
        print(f"[ok] GDACS invariato: {len(eventi)} eventi ({rilevanti} orange/red).")
        return 0

    OUT.write_text(nuovo, encoding="utf-8")
    print(f"[ok] GDACS aggiornato: {len(eventi)} eventi ({rilevanti} orange/red) → {OUT.relative_to(OUT.parents[2])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
