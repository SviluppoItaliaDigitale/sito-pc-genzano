#!/usr/bin/env python3
"""Snapshot dei mezzi aerei antincendio e delle emergenze dichiarate in volo sull'Italia.

Perché uno snapshot e non una lettura diretta dal browser: adsb.fi risponde 200 con
dati veri ma NON espone le intestazioni CORS (verificato 22/09/2026), quindi la
same-origin policy blocca la fetch dalla Sala situazioni. Stesso pattern già usato
per GDACS, Copernicus EMS e le notizie delle agenzie: il server non ha quel vincolo,
committa il JSON e la Sala lo legge da raw.githubusercontent.com.

Perché NON si usa OpenSky come fonte alternativa: i suoi "state vector" non
contengono il tipo di velivolo, quindi non permettono di distinguere un Canadair da
un aereo di linea. Una fonte che non può rispondere alla domanda non è un fallback:
se adsb.fi non risponde lo snapshot resta quello di prima e la Sala mostra l'età.

🔴 ONESTÀ DEL DATO — i due elenchi contengono solo fatti trasmessi dal velivolo o
dichiarati dalla banca dati della fonte:
  - "antincendio": filtro sul MODELLO leggibile (campo desc), limitato agli
    airframe il cui unico impiego è l'antincendio. Sono esclusi gli elicotteri
    generalisti (AW139, AS350...), in gran parte privati, i trasporti militari che
    solo concorrono all'antincendio (CH-47) e l'AT-802 agricolo: vedi la nota sulla
    lista MODELLI_AIB, nata da un falso positivo reale.
  - "emergenze": il velivolo sta trasmettendo un codice di emergenza (7700 guasto
    grave, 7600 radio in avaria, 7500 dirottamento) oppure il campo emergency.
Essere in volo NON implica un intervento in corso: lo dice la nota della scheda.

Fail-safe: qualunque errore lascia lo snapshot invariato ed esce 0 — una fonte
terza che cade non deve mai rompere un deploy.
"""
from __future__ import annotations

import json
import pathlib
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

FONTE = "https://opendata.adsb.fi/api/v2/lat/{lat}/lon/{lon}/dist/{dist}"
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/)"
USCITA = pathlib.Path(__file__).resolve().parent.parent / "static" / "open-data" / "volo-soccorso.json"

# Tre cerchi che coprono la penisola e le isole maggiori (raggio massimo consentito
# dall'API: 250 NM). La sovrapposizione è voluta, il dedup è sul codice ICAO 24 bit.
CERCHI = [(45.5, 10.0, 250), (42.0, 12.5, 250), (37.5, 14.5, 250)]

# Modelli il cui impiego è antincendio o soccorso pesante: nessuno di questi è un
# velivolo privato. Confronto per sottostringa sul campo "desc" della fonte, così il
# criterio resta leggibile e verificabile da chiunque apra il file.
MODELLI_AIB = (
    "CL-215", "CL-415", "CL-515",      # Canadair, flotta di Stato antincendio
    "AT-802F", "FIRE BOSS",             # SOLO la variante antincendio dell'Air Tractor
    "S-64", "S64",                      # Erickson Aircrane
    "BE-200",                           # Beriev anfibio
)
# 🔴 Esclusi di proposito, imparato guardando il primo risultato reale (22/09/2026):
#   - "AT-802" liscio: è l'AIR TRACTOR agricolo. La prima esecuzione ha agganciato
#     un S5-BZT a 400 ft e 89 kt sopra la Slovenia, cioè un'irrorazione agricola.
#     Chiamarlo "antincendio" sarebbe stata esattamente l'invenzione da evitare.
#   - CH-47 Chinook: è un trasporto pesante militare che CONCORRE all'antincendio
#     ma normalmente fa altro; dedurre la missione dal tipo non è lecito.
#   - Elicotteri generalisti (AW139, AS350, ecc.): in gran parte privati.

# Riquadro dell'Italia e dei mari circostanti. I cerchi di raccolta sbordano su
# Slovenia, Croazia, Corsica e Tunisia: senza questo filtro la Sala mostrerebbe
# velivoli esteri in una scheda che parla del territorio nazionale.
IT_LAT = (35.2, 47.2)
IT_LON = (6.4, 18.8)


def in_italia(v: dict) -> bool:
    la, lo = v.get("lat"), v.get("lon")
    return (la is not None and lo is not None
            and IT_LAT[0] <= la <= IT_LAT[1] and IT_LON[0] <= lo <= IT_LON[1])
EMERGENZE = {"7700": "guasto grave a bordo", "7600": "radio in avaria", "7500": "dirottamento"}


def ora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def scarica(url: str, tentativi: int = 3):
    ultimo = None
    for n in range(tentativi):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as e:
            ultimo = e
            if n < tentativi - 1:
                time.sleep(4 * (n + 1))
    raise RuntimeError(f"fonte non raggiungibile: {ultimo}")


def num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if f == f else None  # scarta NaN


def scheda(a: dict) -> dict:
    """Solo campi che la fonte dichiara, nessun calcolo interpretativo."""
    return {
        "hex": a.get("hex"),
        "immatricolazione": a.get("r") or None,
        "volo": (a.get("flight") or "").strip() or None,
        "modello": a.get("desc") or None,
        "tipo_icao": a.get("t") or None,
        "lat": num(a.get("lat")),
        "lon": num(a.get("lon")),
        "quota_ft": num(a.get("alt_baro")) if str(a.get("alt_baro")) != "ground" else 0,
        "a_terra": str(a.get("alt_baro")) == "ground",
        "velocita_kt": num(a.get("gs")),
        "squawk": a.get("squawk") or None,
    }


def main() -> int:
    velivoli: dict[str, dict] = {}
    raggiunti = 0
    for lat, lon, dist in CERCHI:
        try:
            d = scarica(FONTE.format(lat=lat, lon=lon, dist=dist))
        except RuntimeError as e:
            print(f"[avviso] cerchio {lat},{lon}: {e}", file=sys.stderr)
            continue
        raggiunti += 1
        for a in d.get("aircraft") or []:
            h = a.get("hex")
            if h:
                velivoli.setdefault(h, a)
        time.sleep(1.2)  # la fonte è comunitaria: non la si martella

    if not raggiunti:
        print("[fail-safe] nessun cerchio raggiungibile: snapshot lasciato invariato.", file=sys.stderr)
        return 0

    aib, emg = [], []
    for a in velivoli.values():
        desc = str(a.get("desc") or "").upper()
        v = scheda(a)
        if not in_italia(v):
            continue
        if any(m in desc for m in MODELLI_AIB):
            aib.append(v)
        sq = str(a.get("squawk") or "")
        em = str(a.get("emergency") or "").lower()
        if sq in EMERGENZE or (em and em not in ("none", "no", "null")):
            e = dict(v)
            e["motivo"] = EMERGENZE.get(sq, f"codice di emergenza «{em}»")
            emg.append(e)

    aib.sort(key=lambda v: (v["immatricolazione"] or v["hex"] or ""))
    emg.sort(key=lambda v: (v["immatricolazione"] or v["hex"] or ""))

    dati = {
        "_snapshot": {
            "generato": ora(),
            "fonte": "adsb.fi — rete comunitaria di riceventi ADS-B",
            "fonte_url": "https://adsb.fi/",
            "copertura": "Italia e mari circostanti; velivoli fuori dal riquadro nazionale esclusi",
            "velivoli_osservati": len(velivoli),
            "cerchi_raggiunti": f"{raggiunti}/{len(CERCHI)}",
            "avvertenza": (
                "Essere in volo non implica un intervento in corso. Il modello è quello "
                "dichiarato dalla banca dati della fonte; la copertura ADS-B non è totale."
            ),
        },
        "antincendio": aib,
        "emergenze": emg,
    }

    USCITA.parent.mkdir(parents=True, exist_ok=True)
    precedente = None
    if USCITA.exists():
        try:
            precedente = json.loads(USCITA.read_text(encoding="utf-8"))
        except ValueError:
            precedente = None
    if precedente and precedente.get("antincendio") == aib and precedente.get("emergenze") == emg:
        print(f"Nessuna variazione ({len(aib)} antincendio, {len(emg)} emergenze): file invariato.")
        return 0

    USCITA.write_text(json.dumps(dati, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Scritto {USCITA.name}: {len(aib)} mezzi antincendio, {len(emg)} emergenze "
          f"su {len(velivoli)} velivoli osservati.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # fail-safe assoluto: mai rompere il deploy per una fonte terza
        print(f"[fail-safe] errore non previsto, snapshot invariato: {e}", file=sys.stderr)
        sys.exit(0)
