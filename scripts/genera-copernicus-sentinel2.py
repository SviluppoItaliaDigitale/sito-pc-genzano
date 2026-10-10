#!/usr/bin/env python3
"""Sentinel-2 a 10 m su Genzano: le ultime scene a colori naturali, ritagliate.

Serve al confronto «prima e dopo» del cruscotto alla scala dei singoli edifici,
dei campi e delle strade (10 m per pixel), dove Sentinel-3 (300 m) e VIIRS
(750 m) mostrano solo macchie. Le immagini vengono dall'archivio pubblico
Sentinel-2 L2A in formato Cloud Optimized GeoTIFF ospitato sul programma AWS
Open Data (catalogo Earth Search di Element 84): si legge con GDAL SOLO la
finestra che serve (16 km attorno a Genzano), senza chiavi né account, qualche
secondo per scena. Dati Copernicus Sentinel, licenza libera con attribuzione.

Per ogni scena nuova si calcola la nuvolosità SULLA FINESTRA dalla maschera di
classificazione del prodotto (SCL, 20 m): è il dato che serve, non la stima
della scena intera (110 km di lato), che può dire «sereno» con Genzano sotto
un cumulo. Le scene coperte oltre l'85% non si tengono: non mostrerebbero nulla.

Scrive:
- static/images/sentinel/sentinel2-genzano-AAAAMMGG.webp per le ultime MAX_SCENE
  scene utili (release «immagini-meteo», non git: scripts/immagini-meteo-release.py);
- static/open-data/copernicus-sentinel2.json (in git): elenco delle scene con
  data, satellite, nuvole sulla finestra, riquadro in gradi per la cartina.

Uso: python3 scripts/genera-copernicus-sentinel2.py [--forza] [--max N]
Fail-safe: catalogo giù = file invariati, exit 0; una scena che non si legge
si salta e si riprova al giro dopo.
"""
from __future__ import annotations

import datetime as dt
import glob
import json
import math
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
IMG_DIR = REPO / "static" / "images" / "sentinel"
OUT_JSON = REPO / "static" / "open-data" / "copernicus-sentinel2.json"
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/)"
STAC = "https://earth-search.aws.element84.com/v1/search"
GENZANO = (41.7085, 12.6916)
MEZZO_LATO_KM = 8.0       # 16 km di lato: dentro il solo tile 33TUG (laghi Albano e Nemi compresi)
RISOLUZIONE_M = 10.0      # 1600 x 1600 pixel, WebP di circa 450 KB
GIORNI = 60
MAX_SCENE = 8
NUVOLE_MAX = 85           # oltre, la scena non si tiene
SCL_NUVOLE = (3, 8, 9, 10)  # ombra di nuvola, nuvola media, nuvola alta, cirri sottili


def log(m: str) -> None:
    print(m, flush=True)


def riquadro_gradi() -> tuple[float, float, float, float]:
    """(ovest, sud, est, nord) della finestra, in gradi."""
    dlat = MEZZO_LATO_KM / 111.32
    dlon = MEZZO_LATO_KM / (111.32 * math.cos(math.radians(GENZANO[0])))
    return (GENZANO[1] - dlon, GENZANO[0] - dlat, GENZANO[1] + dlon, GENZANO[0] + dlat)


def riquadro_3857() -> tuple[float, float, float, float]:
    R = 6378137.0
    x = math.radians(GENZANO[1]) * R
    y = math.log(math.tan(math.pi / 4 + math.radians(GENZANO[0]) / 2)) * R
    d = MEZZO_LATO_KM * 1000 / math.cos(math.radians(GENZANO[0]))
    return (x - d, y - d, x + d, y + d)


def gradi(x: float, y: float) -> tuple[float, float]:
    R = 6378137.0
    return math.degrees(2 * math.atan(math.exp(y / R)) - math.pi / 2), math.degrees(x / R)


def stac_s2() -> list[dict]:
    o, s, e, n = riquadro_gradi()
    da = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=GIORNI)).strftime("%Y-%m-%dT%H:%M:%SZ")
    q = urllib.parse.urlencode({"collections": "sentinel-2-l2a", "bbox": f"{o:.4f},{s:.4f},{e:.4f},{n:.4f}",
                                "datetime": da + "/..", "limit": 100, "sortby": "-properties.datetime"})
    req = urllib.request.Request(STAC + "?" + q, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    buone = []
    for f in d.get("features", []):
        b = f.get("bbox") or []
        a = f.get("assets", {})
        # solo i tile che contengono l'intera finestra: una scena tagliata a metà
        # lascerebbe una fascia nera che sembra un dato
        if len(b) == 4 and b[0] <= o and b[1] <= s and b[2] >= e and b[3] >= n \
                and a.get("visual", {}).get("href", "").startswith("https://") and a.get("scl", {}).get("href"):
            buone.append(f)
    # una scena per giorno (lo stesso passaggio sta in più tile/riprocessamenti)
    per_giorno: dict[str, dict] = {}
    for f in buone:
        g = f["properties"]["datetime"][:10]
        per_giorno.setdefault(g, f)
    return [per_giorno[g] for g in sorted(per_giorno, reverse=True)]


def leggi(href: str, lato: int, resampling):
    import rasterio
    from rasterio.transform import from_bounds
    from rasterio.vrt import WarpedVRT

    xmin, ymin, xmax, ymax = riquadro_3857()
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif",
                      GDAL_HTTP_USERAGENT=UA, GDAL_HTTP_MAX_RETRY="3", GDAL_HTTP_RETRY_DELAY="5"):
        with rasterio.open("/vsicurl/" + href if href.startswith("https://") else href) as src:
            with WarpedVRT(src, crs="EPSG:3857", transform=from_bounds(xmin, ymin, xmax, ymax, lato, lato),
                           width=lato, height=lato, resampling=resampling) as vrt:
                return vrt.read()


def elabora(f: dict, dest: Path) -> dict:
    import numpy as np
    from PIL import Image
    from rasterio.enums import Resampling

    a = f["assets"]
    scl = leggi(a["scl"]["href"], 800, Resampling.nearest)[0]
    valido = scl > 0
    if valido.mean() < 0.9:
        raise RuntimeError(f"finestra coperta solo al {valido.mean() * 100:.0f}%")
    nuvole = float(np.isin(scl, SCL_NUVOLE)[valido].mean() * 100)
    if nuvole > NUVOLE_MAX:
        return {"nuvole_pct": round(nuvole), "scartata": True}
    lato = int(round(2 * MEZZO_LATO_KM * 1000 / RISOLUZIONE_M))
    rgb = leggi(a["visual"]["href"], lato, Resampling.bilinear)
    if rgb.shape[0] < 3:
        raise RuntimeError("immagine a colori con meno di 3 bande")
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".nuovo.webp")
    Image.fromarray(np.moveaxis(rgb[:3], 0, -1).astype("uint8"), "RGB").save(tmp, "WEBP", quality=80, method=6)
    tmp.replace(dest)
    return {"nuvole_pct": round(nuvole), "scartata": False, "pixel": lato}


def main() -> int:
    forza = "--forza" in sys.argv
    massimo = MAX_SCENE
    if "--max" in sys.argv:
        massimo = int(sys.argv[sys.argv.index("--max") + 1])
    try:
        feats = stac_s2()
    except Exception as e:  # noqa: BLE001
        log(f"Catalogo Earth Search non raggiungibile: {e}. File lasciati com'erano.")
        return 0
    if not feats:
        log("Nessuna scena Sentinel-2 completa su Genzano negli ultimi giorni.")
        return 0
    prec: dict = {}
    if OUT_JSON.is_file() and not forza:
        try:
            prec = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        except ValueError:
            prec = {}
    gia = {s["giorno"]: s for s in prec.get("scene", []) if (IMG_DIR / Path(s["immagine"]).name).is_file()}
    scartate = set(prec.get("scartate", []))
    scene = dict(gia)
    nuove = 0
    for f in feats:
        if len(scene) >= massimo and all(g >= f["properties"]["datetime"][:10] for g in scene):
            break  # le scene piu' vecchie non entrerebbero comunque
        p = f["properties"]
        g = p["datetime"][:10]
        if g in scene or (g in scartate and not forza):
            continue
        dest = IMG_DIR / f"sentinel2-genzano-{g.replace('-', '')}.webp"
        try:
            info = elabora(f, dest)
        except Exception as e:  # noqa: BLE001
            log(f"Scena {f['id']} non letta ({e}): si riprova al giro dopo.")
            continue
        if info["scartata"]:
            log(f"Scena {f['id']}: nuvole sul {info['nuvole_pct']}% della finestra, non si tiene.")
            scartate.add(g)
            continue
        nuove += 1
        scene[g] = {"id": f["id"], "giorno": g, "quando": p["datetime"],
                    "satellite": str(p.get("platform", "")).replace("sentinel-", "Sentinel-").upper().replace("SENTINEL", "Sentinel"),
                    "nuvole_pct": info["nuvole_pct"], "nuvole_scena_pct": round(float(p.get("eo:cloud_cover") or 0)),
                    "immagine": "/images/sentinel/" + dest.name}
        log(f"Scena {f['id']} scritta: nuvole sul {info['nuvole_pct']}% della finestra.")
    ordinate = [scene[g] for g in sorted(scene, reverse=True)][:massimo]
    tenute = {Path(s["immagine"]).name for s in ordinate}
    for vecchio in glob.glob(str(IMG_DIR / "sentinel2-genzano-*.webp")):
        if Path(vecchio).name not in tenute and re.fullmatch(r"sentinel2-genzano-\d{8}\.webp", Path(vecchio).name):
            os.remove(vecchio)
            log(f"Tolta la scena piu' vecchia: {Path(vecchio).name}")
    if not ordinate:
        log("Nessuna scena utile (tutte nuvolose o non leggibili): nessun file scritto.")
        return 0
    if nuove == 0 and not forza and [s["giorno"] for s in prec.get("scene", [])] == [s["giorno"] for s in ordinate]:
        log("Nessuna scena nuova: file invariati.")
        return 0
    xmin, ymin, xmax, ymax = riquadro_3857()
    s, w = gradi(xmin, ymin)
    n, e = gradi(xmax, ymax)
    out = {
        "_snapshot": {"generato": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "fonte": "Sentinel-2 L2A a colori naturali (TCI, 10 m), archivio Cloud Optimized GeoTIFF su AWS Open Data, catalogo Earth Search (Element 84)",
                      "attribuzione": f"Contiene dati Copernicus Sentinel modificati {dt.date.today().year}",
                      "nota": "nuvole_pct e' la copertura calcolata sulla finestra dalla maschera SCL del prodotto; nuvole_scena_pct e' la stima della scena intera"},
        "riquadro": {"sud": round(s, 5), "ovest": round(w, 5), "nord": round(n, 5), "est": round(e, 5)},
        "risoluzione_m": RISOLUZIONE_M, "pixel": int(round(2 * MEZZO_LATO_KM * 1000 / RISOLUZIONE_M)),
        "scene": ordinate,
        # le date nuvolose si ricordano per tutta la finestra del catalogo, altrimenti
        # ogni giro rileggerebbe la maschera SCL delle stesse scene scartate
        "scartate": sorted(x for x in scartate if x >= (dt.date.today() - dt.timedelta(days=GIORNI)).isoformat())[-40:],
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    log(f"Sentinel-2: {len(ordinate)} scene in archivio, {nuove} nuove ({ordinate[0]['giorno']} la piu' recente).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
