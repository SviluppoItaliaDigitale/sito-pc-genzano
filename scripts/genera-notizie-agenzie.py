#!/usr/bin/env python3
"""Snapshot self-hosted delle ultime notizie delle agenzie di stampa
(ANSA, Adnkronos) per la barra NOTIZIE della Sala situazioni (/monitor/).

Perché esiste
-------------
I feed RSS delle agenzie non espongono CORS ai browser: la pagina non può
leggerli direttamente. Stesso pattern degli snapshot EMS e GDACS: il download
avviene qui in CI e il file statico `static/open-data/notizie-agenzie.json`
viene letto in same-origin. Contenuto: solo titolo, link alla fonte, orario e
nome della testata (uso standard dei feed RSS pubblici, con attribuzione).

Comportamento
-------------
- Ogni feed è indipendente: se uno fallisce si usa il resto.
- Se falliscono tutti: snapshot esistente lasciato invariato, exit 0.

Uso: python3 scripts/genera-notizie-agenzie.py
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

FEEDS = [
    ("ANSA", "https://www.ansa.it/sito/ansait_rss.xml"),
    ("ANSA CRONACA", "https://www.ansa.it/sito/notizie/cronaca/cronaca_rss.xml"),
    ("ADNKRONOS", "https://www.adnkronos.com/RSS_PrimaPagina.xml"),
]
OUT = Path(__file__).resolve().parent.parent / "static" / "open-data" / "notizie-agenzie.json"
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/)"
MAX_TOTALE = 30


def leggi_feed(fonte: str, url: str) -> list[dict]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        root = ET.fromstring(r.read())
    out = []
    for item in root.iter("item"):
        titolo = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not titolo or not link.startswith("http"):
            continue
        ts = None
        pub = item.findtext("pubDate")
        if pub:
            try:
                ts = parsedate_to_datetime(pub).astimezone(timezone.utc).isoformat(timespec="seconds")
            except Exception:
                ts = None
        out.append({"fonte": fonte, "titolo": titolo, "url": link, "data": ts})
    return out


def main() -> int:
    notizie: list[dict] = []
    ok_feed = 0
    for fonte, url in FEEDS:
        try:
            voci = leggi_feed(fonte, url)
            notizie.extend(voci)
            ok_feed += 1
            print(f"[ok] {fonte}: {len(voci)} titoli")
        except (urllib.error.URLError, TimeoutError, ET.ParseError, OSError) as e:
            print(f"[warn] {fonte} non leggibile ({e}); si prosegue con gli altri feed.")

    if not ok_feed:
        esistente = "presente" if OUT.exists() else "assente"
        print(f"[warn] Nessun feed leggibile; snapshot {esistente} lasciato invariato.")
        return 0

    # dedup per URL, ordina per data decrescente (le voci senza data in coda)
    visti: set[str] = set()
    uniche = []
    for n in notizie:
        if n["url"] in visti:
            continue
        visti.add(n["url"])
        uniche.append(n)
    uniche.sort(key=lambda n: n["data"] or "", reverse=True)
    uniche = uniche[:MAX_TOTALE]

    payload = {
        "_snapshot": {
            "generato": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "fonti": [u for _, u in FEEDS],
            "nota": "Titoli e link dai feed RSS pubblici delle agenzie, con attribuzione. Copia locale per lettura same-origin dalla Sala situazioni.",
        },
        "count": len(uniche),
        "notizie": uniche,
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
        print(f"[ok] Notizie invariate: {len(uniche)} titoli da {ok_feed} feed.")
        return 0

    OUT.write_text(nuovo, encoding="utf-8")
    print(f"[ok] Notizie aggiornate: {len(uniche)} titoli da {ok_feed} feed → {OUT.relative_to(OUT.parents[2])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
