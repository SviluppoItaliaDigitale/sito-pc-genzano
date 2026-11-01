#!/usr/bin/env python3
"""Mappa di Genzano di Roma per il gioco «Genzano si prepara».

Disegna in SVG il centro abitato (strade, edifici, verde, Lago di Nemi) dai
dati di OpenStreetMap (ODbL) e scrive accanto le coordinate dei luoghi del
gioco e delle aree di emergenza, prese da data/aree_emergenza.yaml.

Uso:
  python3 scripts/genera-mappa-gioco-genzano.py --scarica   # scarica OSM e genera
  python3 scripts/genera-mappa-gioco-genzano.py             # genera dalla copia già scaricata
  python3 scripts/genera-mappa-gioco-genzano.py --check     # luoghi.json allineato alle aree?

I dati OSM grezzi stanno in ~/.cache/pcgenzano-osm/ e non si committano.
"""
import argparse
import json
import math
import os
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

RADICE = Path(__file__).resolve().parent.parent
USCITA = RADICE / "static/giochi/genzano-si-prepara"
CACHE = Path(os.environ.get("PCGZ_OSM_CACHE", Path.home() / ".cache/pcgenzano-osm"))
AREE = RADICE / "data/aree_emergenza.yaml"

# Riquadro del centro abitato (gradi): ovest, sud, est, nord.
OVEST, SUD, EST, NORD = 12.672, 41.688, 12.708, 41.718
LARGHEZZA = 1000
LAT0 = math.radians((SUD + NORD) / 2)
SCALA = LARGHEZZA / ((EST - OVEST) * math.cos(LAT0))
ALTEZZA = round((NORD - SUD) * SCALA)

API = "https://api.openstreetmap.org/api/0.6"
UA = "PCGenzano/1.0 (https://www.protezionecivilegenzano.it/)"
# Relazioni intere: Lago di Nemi e confine comunale di Genzano.
RELAZIONI = {"lago": 2169086, "comune": 41478}

# Luoghi del gioco: punti veri della città, con il nome che hanno in OSM.
# Gli eventi dello scenario sono inventati; i luoghi no.
LUOGHI = {
    "casa":   {"nome": "Casa tua", "lat": 41.70990, "lon": 12.68560},
    "scuola": {"nome": "Scuola Giovanni Pascoli", "lat": 41.70959, "lon": 12.68891},
    "parco":  {"nome": "Parco Sforza-Cesarini", "lat": 41.70920, "lon": 12.69100},
    "strada": {"nome": "Una strada in discesa", "lat": 41.70150, "lon": 12.68050},
    "comune": {"nome": "Municipio", "lat": 41.70707, "lon": 12.69102},
    "lago":   {"nome": "Lago di Nemi", "lat": 41.71560, "lon": 12.70420},
}


def xy(lat, lon):
    x = (lon - OVEST) * math.cos(LAT0) * SCALA
    y = (NORD - lat) * SCALA
    return round(x, 1), round(y, 1)


def scarica(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for tentativo in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                dest.write_bytes(r.read())
            return
        except Exception as e:  # rete instabile: si riprova
            print(f"  tentativo {tentativo + 1} fallito: {e}", file=sys.stderr)
            time.sleep(5 * (tentativo + 1))
    sys.exit(f"Impossibile scaricare {url}")


def scarica_tutto():
    CACHE.mkdir(parents=True, exist_ok=True)
    scarica(f"{API}/map?bbox={OVEST},{SUD},{EST},{NORD}", CACHE / "centro.osm")
    for nome, rid in RELAZIONI.items():
        time.sleep(2)
        scarica(f"{API}/relation/{rid}/full", CACHE / f"{nome}.osm")


def leggi(file):
    radice = ET.parse(file).getroot()
    nodi = {n.get("id"): (float(n.get("lat")), float(n.get("lon"))) for n in radice.findall("node")}
    vie = {}
    for w in radice.findall("way"):
        tag = {t.get("k"): t.get("v") for t in w.findall("tag")}
        punti = [nodi[n.get("ref")] for n in w.findall("nd") if n.get("ref") in nodi]
        vie[w.get("id")] = (tag, punti)
    rel = []
    for r in radice.findall("relation"):
        tag = {t.get("k"): t.get("v") for t in r.findall("tag")}
        membri = [(m.get("ref"), m.get("role")) for m in r.findall("member") if m.get("type") == "way"]
        rel.append((tag, membri))
    return vie, rel


def anelli(membri, vie, ruolo="outer"):
    """Unisce le vie di una relazione in anelli chiusi."""
    pezzi = [list(vie[ref][1]) for ref, r in membri if r == ruolo and ref in vie and vie[ref][1]]
    chiusi = []
    while pezzi:
        anello = pezzi.pop(0)
        cambiato = True
        while anello[0] != anello[-1] and cambiato:
            cambiato = False
            for i, p in enumerate(pezzi):
                if p[0] == anello[-1]:
                    anello += p[1:]
                elif p[-1] == anello[-1]:
                    anello += p[::-1][1:]
                elif p[-1] == anello[0]:
                    anello = p + anello[1:]
                elif p[0] == anello[0]:
                    anello = p[::-1] + anello[1:]
                else:
                    continue
                pezzi.pop(i)
                cambiato = True
                break
        chiusi.append(anello)
    return chiusi


def semplifica(punti, tolleranza=0.6):
    """Douglas-Peucker sui punti già proiettati."""
    if len(punti) < 3:
        return punti
    a, b = punti[0], punti[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    norma = math.hypot(dx, dy) or 1e-9
    massimo, indice = 0, 0
    for i in range(1, len(punti) - 1):
        d = abs(dy * punti[i][0] - dx * punti[i][1] + b[0] * a[1] - b[1] * a[0]) / norma
        if d > massimo:
            massimo, indice = d, i
    if massimo > tolleranza:
        return semplifica(punti[: indice + 1], tolleranza)[:-1] + semplifica(punti[indice:], tolleranza)
    return [a, b]


def percorso(punti, chiuso=False, tolleranza=0.6):
    pts = [xy(*p) for p in punti]
    if chiuso and len(pts) > 3:
        # Un anello ha primo e ultimo punto uguali: si spezza nel punto più
        # lontano dall'inizio e si semplificano le due metà.
        lontano = max(range(len(pts)), key=lambda i: math.dist(pts[0], pts[i]))
        pts = semplifica(pts[: lontano + 1], tolleranza)[:-1] + semplifica(pts[lontano:], tolleranza)
        if len(pts) < 3:
            return ""
    else:
        pts = semplifica(pts, tolleranza)
    if len(pts) < 2:
        return ""
    d = "M" + " ".join(f"{x:g},{y:g}" for x, y in pts)
    return d + ("Z" if chiuso else "")


STRADE = {  # classe OSM -> (gruppo, ordine)
    "primary": "s1", "primary_link": "s1", "trunk": "s1",
    "secondary": "s2", "secondary_link": "s2",
    "tertiary": "s3", "tertiary_link": "s3",
    "unclassified": "s4", "residential": "s4", "living_street": "s4",
    "pedestrian": "s5", "service": "s6",
}
VERDE = {"park", "garden", "forest", "wood", "grass", "meadow", "orchard", "vineyard",
         "farmland", "scrub", "cemetery", "pitch", "recreation_ground"}


def genera():
    for f in ("centro.osm", "lago.osm", "comune.osm"):
        if not (CACHE / f).exists():
            sys.exit(f"Manca {CACHE / f}: esegui con --scarica")
    vie, _ = leggi(CACHE / "centro.osm")
    gruppi = {k: [] for k in ("verde", "edifici", "s6", "s5", "s4", "s3", "s2", "s1")}
    for tag, punti in vie.values():
        if len(punti) < 2:
            continue
        chiusa = punti[0] == punti[-1]
        if "building" in tag and chiusa:
            d = percorso(punti, True, 0.8)
            if d:
                gruppi["edifici"].append(d)
        elif chiusa and (tag.get("leisure") in VERDE or tag.get("landuse") in VERDE or tag.get("natural") in VERDE):
            d = percorso(punti, True, 1.0)
            if d:
                gruppi["verde"].append(d)
        elif tag.get("highway") in STRADE:
            d = percorso(punti, False, 0.7)
            if d:
                gruppi[STRADE[tag["highway"]]].append(d)

    lago_vie, lago_rel = leggi(CACHE / "lago.osm")
    lago = []
    for tag, membri in lago_rel:
        if tag.get("natural") == "water":
            lago += [percorso(a, True, 0.8) for a in anelli(membri, lago_vie)]
    com_vie, com_rel = leggi(CACHE / "comune.osm")
    confine = []
    for tag, membri in com_rel:
        if tag.get("boundary") == "administrative":
            confine += [percorso(a, True, 1.0) for a in anelli(membri, com_vie)]

    def blocco(classe, lista):
        return f'<path class="{classe}" d="{" ".join(lista)}"/>' if lista else ""

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LARGHEZZA} {ALTEZZA}" '
        f'role="img" aria-labelledby="t d">',
        "<title id=\"t\">Mappa del centro di Genzano di Roma</title>",
        "<desc id=\"d\">Strade, edifici, parchi e Lago di Nemi del centro abitato di Genzano di Roma. "
        "Dati © OpenStreetMap contributors, licenza ODbL.</desc>",
        "<style>"
        ".fondo{fill:#eef0e6}.verde{fill:#cfe3bf}.lago{fill:#9cc7e4;stroke:#6aa3cc;stroke-width:2}"
        ".edifici{fill:#d8d2c6;stroke:#c3bba9;stroke-width:.4}"
        ".s1,.s2,.s3,.s4,.s5,.s6{fill:none;stroke-linecap:round;stroke-linejoin:round}"
        ".s6{stroke:#fff;stroke-width:1.6}.s5{stroke:#f7f3ea;stroke-width:3}"
        ".s4{stroke:#fff;stroke-width:3.2}.s3{stroke:#fffbe8;stroke-width:5}"
        ".s2{stroke:#fbe3a6;stroke-width:6.5}.s1{stroke:#f4c46a;stroke-width:8}"
        ".bordo{fill:none;stroke:#8a7f9a;stroke-width:2.5;stroke-dasharray:10 6}"
        "</style>",
        f'<rect class="fondo" width="{LARGHEZZA}" height="{ALTEZZA}"/>',
        blocco("verde", gruppi["verde"]),
        blocco("lago", lago),
        blocco("bordo", confine),
        blocco("edifici", gruppi["edifici"]),
    ]
    for classe in ("s6", "s5", "s4", "s3", "s2", "s1"):
        svg.append(blocco(classe, gruppi[classe]))
    svg.append("</svg>")
    (USCITA / "mappa-genzano.svg").write_text("\n".join(x for x in svg if x) + "\n", encoding="utf-8")
    scrivi_luoghi()
    print(f"Mappa: {LARGHEZZA}×{ALTEZZA}, {len(gruppi['edifici'])} edifici, "
          f"{sum(len(gruppi[k]) for k in STRADE.values())} tratti di strada")


def luoghi_dati():
    aree = yaml.safe_load(AREE.read_text(encoding="utf-8"))["aree"]
    out = {"vista": [LARGHEZZA, ALTEZZA], "luoghi": {}, "aree": []}
    for k, v in LUOGHI.items():
        x, y = xy(v["lat"], v["lon"])
        out["luoghi"][k] = {"nome": v["nome"], "x": x, "y": y}
    for a in aree:
        x, y = xy(a["lat"], a["lon"])
        if 0 <= x <= LARGHEZZA and 0 <= y <= ALTEZZA:
            out["aree"].append({"id": a["id"], "tipo": a["tipo"], "nome": a["nome"],
                                "indirizzo": a["indirizzo"], "x": x, "y": y})
    return out


def testo_luoghi():
    return json.dumps(luoghi_dati(), ensure_ascii=False, indent=1) + "\n"


def scrivi_luoghi():
    (USCITA / "luoghi.json").write_text(testo_luoghi(), encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--scarica", action="store_true", help="scarica di nuovo i dati da OpenStreetMap")
    p.add_argument("--check", action="store_true", help="verifica che luoghi.json sia allineato")
    a = p.parse_args()
    if a.check:
        attuale = (USCITA / "luoghi.json").read_text(encoding="utf-8")
        if attuale != testo_luoghi():
            sys.exit("luoghi.json non coincide con data/aree_emergenza.yaml: "
                     "esegui python3 scripts/genera-mappa-gioco-genzano.py")
        print("luoghi.json allineato alle aree di emergenza")
        return
    if a.scarica:
        scarica_tutto()
    genera()


if __name__ == "__main__":
    main()
