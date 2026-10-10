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
MEZZO_LATO_KM = 8.0       # 16 km di lato (laghi Albano e Nemi compresi); a cavallo del confine fra i tile 33TUG e 33TTG
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
    def copre(f: dict) -> float:
        """Quanta parte della finestra sta dentro il riquadro del tile (0..1)."""
        b = f.get("bbox") or [0, 0, 0, 0]
        return max(0.0, min(b[2], e) - max(b[0], o)) * max(0.0, min(b[3], n) - max(b[1], s)) / ((e - o) * (n - s))

    buone = [f for f in d.get("features", [])
             if len(f.get("bbox") or []) == 4 and copre(f) > 0
             and f.get("assets", {}).get("visual", {}).get("href", "").startswith("https://")
             and f.get("assets", {}).get("scl", {}).get("href")]
    # Per giorno, tutti i tile dello stesso passaggio che toccano la finestra, dal
    # piu' coprente in giu': la finestra di 16 km cade sul confine occidentale
    # del tile 33TUG (E = 300.000 m UTM, rilievo di revisione del 10/10/2026),
    # quindi un tile solo lascia sempre una striscia senza dati e si compone con
    # il vicino (33TTG). I riprocessamenti dello stesso tile (_0, _1) restano in
    # elenco: se il primo non copre, il secondo riempie.
    per_giorno: dict[str, list[dict]] = {}
    for f in buone:
        per_giorno.setdefault(f["properties"]["datetime"][:10], []).append(f)
    for lst in per_giorno.values():
        lst.sort(key=copre, reverse=True)
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


def componi(feats: list[dict], chiave: str, lato: int, resampling):
    """Legge la finestra dal primo tile e riempie i pixel senza dati (0) con i tile successivi."""
    import numpy as np

    out = None
    usati = []
    for f in feats:
        a = leggi(f["assets"][chiave]["href"], lato, resampling)
        if out is None:
            out, usati = a, [f["id"]]
        else:
            vuoto = np.all(out == 0, axis=0)
            if not vuoto.any():
                break
            out[:, vuoto] = a[:, vuoto]
            usati.append(f["id"])
        if not np.all(out == 0, axis=0).any():
            break
    return out, usati


def elabora(feats: list[dict], dest: Path) -> dict:
    import numpy as np
    from PIL import Image
    from rasterio.enums import Resampling

    scl, usati = componi(feats, "scl", 800, Resampling.nearest)
    scl = scl[0]
    valido = scl > 0
    if valido.mean() < 0.9:
        raise RuntimeError(f"finestra coperta solo al {valido.mean() * 100:.0f}% ({', '.join(usati)})")
    nuvole = float(np.isin(scl, SCL_NUVOLE)[valido].mean() * 100)
    if nuvole > NUVOLE_MAX:
        return {"nuvole_pct": round(nuvole), "scartata": True, "tile": usati}
    lato = int(round(2 * MEZZO_LATO_KM * 1000 / RISOLUZIONE_M))
    rgb, usati = componi(feats, "visual", lato, Resampling.bilinear)
    if rgb.shape[0] < 3:
        raise RuntimeError("immagine a colori con meno di 3 bande")
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".nuovo.webp")
    Image.fromarray(np.moveaxis(rgb[:3], 0, -1).astype("uint8"), "RGB").save(tmp, "WEBP", quality=80, method=6)
    tmp.replace(dest)
    return {"nuvole_pct": round(nuvole), "scartata": False, "pixel": lato, "tile": usati,
            "coperta_pct": round(float(valido.mean() * 100), 1)}


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
    for tiles in feats:
        f = tiles[0]
        p = f["properties"]
        g = p["datetime"][:10]
        if len(scene) >= massimo and all(x >= g for x in scene):
            break  # le scene piu' vecchie non entrerebbero comunque
        if g in scene or (g in scartate and not forza):
            continue
        dest = IMG_DIR / f"sentinel2-genzano-{g.replace('-', '')}.webp"
        try:
            info = elabora(tiles, dest)
        except Exception as e:  # noqa: BLE001
            log(f"Scena del {g} non letta ({e}): si riprova al giro dopo.")
            continue
        if info["scartata"]:
            log(f"Scena del {g} ({', '.join(info['tile'])}): nuvole sul {info['nuvole_pct']}% della finestra, non si tiene.")
            scartate.add(g)
            continue
        nuove += 1
        scene[g] = {"id": f["id"], "tile": info["tile"], "giorno": g, "quando": p["datetime"],
                    "satellite": str(p.get("platform", "")).replace("sentinel-", "Sentinel-").upper().replace("SENTINEL", "Sentinel"),
                    "nuvole_pct": info["nuvole_pct"], "nuvole_scena_pct": round(float(p.get("eo:cloud_cover") or 0)),
                    "coperta_pct": info["coperta_pct"], "immagine": "/images/sentinel/" + dest.name}
        log(f"Scena del {g} scritta da {', '.join(info['tile'])}: finestra coperta al {info['coperta_pct']}%, nuvole sul {info['nuvole_pct']}%.")
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
