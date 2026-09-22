#!/usr/bin/env python3
"""Snapshot del traffico aereo sull'area di interesse e dei mezzi di rilievo operativo.

Perché uno snapshot e non una lettura diretta dal browser: NESSUNA fonte ADS-B
pubblica espone le intestazioni CORS. Provate il 22/09/2026: adsb.fi e adsb.lol
rispondono 200 con dati veri ma senza CORS, adsb.one e airplanes.live rifiutano
(403), OpenSky limita il CORS al proprio dominio. Il server non ha quel vincolo,
committa il JSON e la Sala lo legge da raw.githubusercontent.com — stesso pattern
di GDACS, Copernicus EMS e notizie delle agenzie.

Perché NON si usa OpenSky nemmeno come alternativa: i suoi "state vector" non
contengono il tipo di velivolo, quindi non reggono nessuno dei filtri qui sotto.

🔴 QUESTO NON È UN TRACCIAMENTO IN TEMPO REALE, ed è scritto anche nella scheda.
Lo snapshot si rigenera ogni 15 minuti: un velivolo di linea in quel tempo percorre
oltre 100 km. Serve a rispondere a domande come «c'è un Canadair al lavoro?», «gira
un elicottero basso sulla zona?», «qualcuno sta dichiarando un'emergenza?», non a
seguire un volo minuto per minuto.

🔴 ONESTÀ DEL DATO — ogni campo è trasmesso dal velivolo o dichiarato dalla banca
dati della fonte; nessuna deduzione sulla missione in corso:
  - "categoria": emitter category ADS-B trasmessa dal velivolo (A7 = elicottero,
    verificato per controprova sui modelli).
  - "antincendio": filtro sul MODELLO leggibile, limitato agli airframe a impiego
    esclusivamente antincendio (vedi MODELLI_AIB).
  - "emergenza": codice trasmesso (7700/7600/7500) o campo emergency.
Essere in volo NON implica un intervento in corso, e la copertura ADS-B non è totale:
molti mezzi di Stato non trasmettono affatto.

PERIMETRO — si tengono tutti i velivoli entro RAGGIO_AREA da Genzano (orizzonte
operativo realistico) e, fino a RAGGIO_NOTEVOLI, quelli di rilievo operativo. Il
criterio è sempre la distanza: non si afferma mai che un velivolo sia "sull'Italia",
perché un riquadro di coordinate non sa dove finisce uno Stato. È una
scelta di peso: l'elenco viene committato ogni 15 minuti e tenere l'intera Italia
farebbe crescere il repository di alcuni GB l'anno. Per allargare basta alzare
RAGGIO_AREA.

Fail-safe: qualunque errore lascia lo snapshot invariato ed esce 0.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

FONTE = "https://opendata.adsb.fi/api/v2/lat/{lat}/lon/{lon}/dist/{dist}"
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/)"
USCITA = pathlib.Path(__file__).resolve().parent.parent / "static" / "open-data" / "volo-soccorso.json"

GENZANO = (41.7085, 12.6916)
RAGGIO_AREA = 400          # km: area tenuta per intero
MAX_ELENCO = 700           # tetto difensivo sulla dimensione del file

CERCHI = [(45.5, 10.0, 250), (42.0, 12.5, 250), (37.5, 14.5, 250)]

# Modelli a impiego esclusivamente antincendio: nessuno è un velivolo privato o
# generalista. Confronto per sottostringa sul campo "desc" della fonte, così il
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
#   - CH-47 Chinook: trasporto pesante militare che CONCORRE all'antincendio ma
#     normalmente fa altro; dedurre la missione dal tipo non è lecito.
#   Gli elicotteri generalisti non sono "soccorso": sono elicotteri, e come tali
#   compaiono nella categoria trasmessa, senza etichette che non ci competono.

# 🔴 NIENTE AFFERMAZIONI SUL PAESE. La versione precedente usava un riquadro
# lat/lon "dell'Italia" e il commento sosteneva che escludesse Slovenia, Croazia,
# Corsica e Tunisia: era FALSO, quel rettangolo contiene Lubiana, Zagabria, Nizza
# e Tunisi (rilievo colto in revisione il 22/09/2026 e verificato con i calcoli).
# Un rettangolo non sa dove finisce uno Stato, e disegnare un poligono d'Italia a
# memoria sarebbe stato inventare coordinate. Si usa quindi l'unico criterio che
# si può affermare con esattezza: la DISTANZA da Genzano. Tutte le etichette
# parlano di distanza, mai di territorio nazionale.
RAGGIO_NOTEVOLI = 800     # km: entro cui si tengono anche antincendio ed emergenze

EMERGENZE = {"7700": "guasto grave a bordo", "7600": "radio in avaria", "7500": "dirottamento"}
# Emitter category ADS-B (standard DO-260B), resa leggibile.
CATEGORIE = {
    "A0": "non dichiarata", "A1": "aereo leggero", "A2": "aereo piccolo",
    "A3": "aereo medio", "A4": "aereo pesante", "A5": "aereo molto pesante",
    "A6": "alte prestazioni", "A7": "elicottero",
    "B1": "aliante", "B2": "più leggero dell'aria", "B3": "paracadutista",
    "B4": "ultraleggero", "B6": "a pilotaggio remoto", "B7": "veicolo spaziale",
}
QUOTA_BASSA_FT = 2000


def ora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def km(a, b) -> float:
    R, p = 6371.0, math.pi / 180
    x, y = (b[0] - a[0]) * p, (b[1] - a[1]) * p
    h = math.sin(x / 2) ** 2 + math.cos(a[0] * p) * math.cos(b[0] * p) * math.sin(y / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def scarica(url: str, tentativi: int = 2):
    """Tentativi e attese volutamente contenuti: questo script gira insieme ad
    altri cinque dentro un solo job, e tre ritentativi da 45 s per ciascuno dei
    tre cerchi mangerebbero da soli l'intero tetto di tempo, facendo fallire il
    commit degli snapshot che erano riusciti (rilievo colto in revisione)."""
    ultimo = None
    for n in range(tentativi):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except (urllib.error.URLError, TimeoutError, ValueError, OSError) as e:
            ultimo = e
            if n < tentativi - 1:
                time.sleep(3)
    raise RuntimeError(f"fonte non raggiungibile: {ultimo}")


def num(v):
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return f if f == f else None


def scheda(a: dict):
    la, lo = num(a.get("lat")), num(a.get("lon"))
    if la is None or lo is None:
        return None
    dist = km(GENZANO, (la, lo))
    if dist > RAGGIO_NOTEVOLI:
        return None
    a_terra = str(a.get("alt_baro")) == "ground"
    quota = 0 if a_terra else num(a.get("alt_baro"))
    cat = str(a.get("category") or "")
    desc = str(a.get("desc") or "").upper()
    sq = str(a.get("squawk") or "")
    em = str(a.get("emergency") or "").lower()

    etichette = []
    if any(m in desc for m in MODELLI_AIB):
        etichette.append("antincendio")
    if cat == "A7":
        etichette.append("elicottero")
    if sq in EMERGENZE or (em and em not in ("none", "no", "null")):
        etichette.append("emergenza")
    if quota is not None and quota <= QUOTA_BASSA_FT and not a_terra:
        etichette.append("bassa-quota")

    v = {
        "hex": a.get("hex"),
        "immatricolazione": a.get("r") or None,
        "volo": (a.get("flight") or "").strip() or None,
        "modello": a.get("desc") or None,
        "tipo_icao": a.get("t") or None,
        "categoria": CATEGORIE.get(cat, "non dichiarata"),
        "lat": round(la, 3),
        "lon": round(lo, 3),
        "quota_ft": quota,
        "a_terra": a_terra,
        "velocita_kt": num(a.get("gs")),
        "rotta": num(a.get("dir")) if a.get("dir") is not None else num(a.get("track")),
        "km_da_genzano": round(dist),
        "etichette": etichette,
    }
    if "emergenza" in etichette:
        v["motivo"] = EMERGENZE.get(sq, "codice di emergenza «" + em + "»")
    return v


def main() -> int:
    grezzi = {}
    raggiunti = 0
    for lat, lon, dist in CERCHI:
        try:
            d = scarica(FONTE.format(lat=lat, lon=lon, dist=dist))
        except RuntimeError as e:
            print("[avviso] cerchio %s,%s: %s" % (lat, lon, e), file=sys.stderr)
            continue
        raggiunti += 1
        for a in d.get("aircraft") or []:
            h = a.get("hex")
            if h:
                grezzi.setdefault(h, a)
        time.sleep(1.2)  # la fonte è comunitaria: non la si martella

    if not raggiunti:
        print("[fail-safe] nessun cerchio raggiungibile: snapshot lasciato invariato.", file=sys.stderr)
        return 0

    tutti = [v for v in (scheda(a) for a in grezzi.values()) if v]
    # Entro RAGGIO_AREA si tiene tutto; fino a RAGGIO_NOTEVOLI solo cio' che ha
    # rilievo operativo. Oltre, gia' scartato in scheda().
    notevoli = {"antincendio", "emergenza"}
    elenco = [v for v in tutti
              if v["km_da_genzano"] <= RAGGIO_AREA or (notevoli & set(v["etichette"]))]
    elenco.sort(key=lambda v: v["km_da_genzano"])
    troncato = len(elenco) > MAX_ELENCO
    elenco = elenco[:MAX_ELENCO]

    conteggi = {
        "totale": len(elenco),
        "antincendio": sum(1 for v in elenco if "antincendio" in v["etichette"]),
        "elicotteri": sum(1 for v in elenco if "elicottero" in v["etichette"]),
        "emergenze": sum(1 for v in elenco if "emergenza" in v["etichette"]),
        "bassa_quota": sum(1 for v in elenco if "bassa-quota" in v["etichette"]),
    }

    dati = {
        "_snapshot": {
            "generato": ora(),
            "fonte": "adsb.fi — rete comunitaria di riceventi ADS-B",
            "fonte_url": "https://adsb.fi/",
            "perimetro": ("tutti i velivoli entro %d km da Genzano; antincendio ed "
                          "emergenze fino a %d km. Il criterio è la distanza, non il "
                          "territorio di uno Stato." % (RAGGIO_AREA, RAGGIO_NOTEVOLI)),
            "raggio_notevoli_km": RAGGIO_NOTEVOLI,
            "raggio_area_km": RAGGIO_AREA,
            "velivoli_osservati": len(grezzi),
            "cerchi_raggiunti": "%d/%d" % (raggiunti, len(CERCHI)),
            "troncato": troncato,
            "conteggi": conteggi,
            "avvertenza": (
                "Non è un tracciamento in tempo reale: lo snapshot si rigenera ogni "
                "15 minuti e in quel tempo un velivolo percorre molta strada. Essere "
                "in volo non implica un intervento in corso; la copertura ADS-B non è "
                "totale e molti mezzi di Stato non trasmettono."
            ),
        },
        "velivoli": elenco,
    }

    USCITA.parent.mkdir(parents=True, exist_ok=True)
    if USCITA.exists():
        try:
            if json.loads(USCITA.read_text(encoding="utf-8")).get("velivoli") == elenco:
                print("Nessuna variazione (%d velivoli): file invariato." % len(elenco))
                return 0
        except ValueError:
            pass
    # Scrittura compatta: il file e' riscritto ogni 15 minuti e committato, quindi
    # ogni KB risparmiato e' crescita del repository evitata. Resta JSON valido.
    USCITA.write_text(json.dumps(dati, ensure_ascii=False, separators=(",", ":")) + "\n",
                      encoding="utf-8")
    print("Scritto %s: %d velivoli (%d antincendio, %d elicotteri, %d emergenze, "
          "%d a bassa quota) su %d osservati."
          % (USCITA.name, len(elenco), conteggi["antincendio"], conteggi["elicotteri"],
             conteggi["emergenze"], conteggi["bassa_quota"], len(grezzi)))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("[fail-safe] errore non previsto, snapshot invariato: %s" % e, file=sys.stderr)
        sys.exit(0)
