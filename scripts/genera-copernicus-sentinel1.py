#!/usr/bin/env python3
"""Radar Sentinel-1 su Genzano: l'ultima immagine, ritagliata, per il cruscotto.

Il radar di Sentinel-1 vede attraverso le nuvole e di notte, e l'acqua ferma
appare scura: è lo strumento con cui Copernicus EMS mappa le aree allagate.
Nell'archivio del Copernicus Data Space Ecosystem i prodotti GRD stanno in
formato Cloud Optimized GeoTIFF (circa 500 MB l'uno): con GDAL via S3 si legge
SOLO la finestra che serve (un riquadro di 30 km attorno a Genzano, a 20 m),
senza scaricare il file intero. Il prodotto GRD è georiferito con punti di
controllo, non con una griglia regolare: la finestra si ottiene riproiettando
in Web Mercator con quei punti (ordine 1), senza correzione del rilievo — sui
Colli Albani i versanti appaiono un po' deformati, e la pagina lo dice.

Scrive:
- static/images/sentinel/sentinel1-genzano.webp (ultima scena) e
  static/images/sentinel/sentinel1-genzano-prima.webp (la precedente): stanno
  nella release «immagini-meteo», non in git (scripts/immagini-meteo-release.py);
- static/open-data/copernicus-sentinel1.json (in git): scena, satellite, orbita,
  riquadro dell'immagine in gradi per sovrapporla alla cartina.

Uso: python3 scripts/genera-copernicus-sentinel1.py [--forza]
Chiavi in CDSE_S3_ACCESS_KEY / CDSE_S3_SECRET_KEY: senza, non scrive nulla ed
esce 0. Fonte giù = file invariati, exit 0. Dati Copernicus Sentinel, licenza
libera con attribuzione.
"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
IMG_DIR = REPO / "static" / "images" / "sentinel"
OUT_JSON = REPO / "static" / "open-data" / "copernicus-sentinel1.json"
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/)"
STAC = "https://stac.dataspace.copernicus.eu/v1/search"
GENZANO = (41.7085, 12.6916)
MEZZO_LATO_KM = 15.0      # riquadro di 30 km di lato
RISOLUZIONE_M = 20.0      # 1500 x 1500 pixel
GIORNI = 12


def log(m: str) -> None:
    print(m, flush=True)


def chiavi() -> tuple[str, str] | None:
    a, s = os.environ.get("CDSE_S3_ACCESS_KEY", "").strip(), os.environ.get("CDSE_S3_SECRET_KEY", "").strip()
    return (a, s) if a and s else None


def stac_s1() -> list[dict]:
    a = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=GIORNI)).strftime("%Y-%m-%dT%H:%M:%SZ")
    q = urllib.parse.urlencode({"collections": "sentinel-1-grd", "bbox": "12.59,41.61,12.79,41.81",
                                "datetime": a + "/..", "limit": 6})
    req = urllib.request.Request(STAC + "?" + q, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    feats = [f for f in d.get("features", []) if f.get("assets", {}).get("vv", {}).get("href", "").startswith("s3://")]
    feats.sort(key=lambda f: f["properties"].get("datetime", ""), reverse=True)
    return feats


def riquadro_3857() -> tuple[float, float, float, float]:
    """Riquadro di 30 km attorno a Genzano in EPSG:3857 (xmin, ymin, xmax, ymax)."""
    R = 6378137.0
    x = math.radians(GENZANO[1]) * R
    y = math.log(math.tan(math.pi / 4 + math.radians(GENZANO[0]) / 2)) * R
    # in Web Mercator le distanze sono dilatate di 1/cos(lat)
    d = MEZZO_LATO_KM * 1000 / math.cos(math.radians(GENZANO[0]))
    return (x - d, y - d, x + d, y + d)


def gradi(x: float, y: float) -> tuple[float, float]:
    R = 6378137.0
    lon = math.degrees(x / R)
    lat = math.degrees(2 * math.atan(math.exp(y / R)) - math.pi / 2)
    return lat, lon


def ritaglia(href: str, ak: str, sk: str, dest: Path) -> dict:
    import numpy as np
    import rasterio
    from PIL import Image
    from rasterio.enums import Resampling
    from rasterio.transform import from_bounds, from_gcps
    from rasterio.vrt import WarpedVRT

    xmin, ymin, xmax, ymax = riquadro_3857()
    lato = int(round((xmax - xmin) / (RISOLUZIONE_M / math.cos(math.radians(GENZANO[0])))))
    vsis3 = "/vsis3/" + href[len("s3://"):] if href.startswith("s3://") else href  # percorso locale per le prove
    # rasterio non accetta le opzioni AWS_* in Env(): GDAL le legge dall'ambiente.
    # Endpoint S3 di Copernicus in stile «path» (niente virtual hosting).
    if href.startswith("s3://"):
        os.environ.update(AWS_S3_ENDPOINT="eodata.dataspace.copernicus.eu", AWS_VIRTUAL_HOSTING="FALSE", AWS_HTTPS="YES",
                          AWS_ACCESS_KEY_ID=ak, AWS_SECRET_ACCESS_KEY=sk, AWS_REGION="default", AWS_DEFAULT_REGION="default")
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR", CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tiff,.tif"):
        with rasterio.open(vsis3) as src:
            gcps, gcps_crs = src.gcps
            extra = {}
            if gcps:
                # Il GRD e' georiferito solo con punti di controllo, e WarpedVRT da solo
                # non li usa (verificato: restituisce un valore costante). Si ricava una
                # trasformazione affine dai soli punti VICINI a Genzano (entro ~40 km, almeno
                # 6), cosi' l'errore della proiezione a terra, che su una scena di 250 km
                # vale chilometri, resta nell'ordine delle decine di metri sulla finestra.
                vicini = sorted(gcps, key=lambda g: (g.y - GENZANO[0]) ** 2 + ((g.x - GENZANO[1]) * 0.75) ** 2)
                scelti = [g for g in vicini if abs(g.y - GENZANO[0]) < 0.36 and abs(g.x - GENZANO[1]) < 0.48]
                if len(scelti) < 6:
                    scelti = vicini[:12]
                extra = {"src_crs": gcps_crs or "EPSG:4326", "src_transform": from_gcps(scelti)}
            elif src.transform.is_identity:
                raise RuntimeError("prodotto senza georiferimento")
            with WarpedVRT(src, crs="EPSG:3857", transform=from_bounds(xmin, ymin, xmax, ymax, lato, lato),
                           width=lato, height=lato, resampling=Resampling.average, src_nodata=0, nodata=0, **extra) as vrt:
                a = vrt.read(1).astype("float32")
    valido = a > 0
    if valido.sum() < 0.2 * a.size:
        raise RuntimeError(f"finestra quasi vuota ({valido.mean() * 100:.0f}% di pixel validi)")
    db = np.full(a.shape, np.nan, dtype="float32")
    db[valido] = 20 * np.log10(a[valido])
    lo, hi = np.nanpercentile(db, 2), np.nanpercentile(db, 98)
    img = np.clip((db - lo) / max(hi - lo, 1e-6), 0, 1)
    img = np.nan_to_num(img, nan=0.0)
    out = (img * 255).astype("uint8")
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    Image.fromarray(out, "L").save(dest, "WEBP", quality=80, method=6)
    s, w = gradi(xmin, ymin)
    n, e = gradi(xmax, ymax)
    return {"sud": round(s, 5), "ovest": round(w, 5), "nord": round(n, 5), "est": round(e, 5),
            "pixel": lato, "validi_pct": round(float(valido.mean() * 100)), "db_min": round(float(lo), 1), "db_max": round(float(hi), 1)}


def main() -> int:
    k = chiavi()
    if not k:
        log("Chiavi Copernicus assenti: nessuna immagine radar scritta.")
        return 0
    try:
        feats = stac_s1()
    except Exception as e:  # noqa: BLE001
        log(f"Catalogo Copernicus non raggiungibile: {e}. File lasciati com'erano.")
        return 0
    if not feats:
        log("Nessuna scena Sentinel-1 su Genzano negli ultimi giorni.")
        return 0
    f = feats[0]
    p = f["properties"]
    prec = {}
    if OUT_JSON.is_file():
        try:
            prec = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        except ValueError:
            prec = {}
    if prec.get("id") == f["id"] and "--forza" not in sys.argv and (IMG_DIR / "sentinel1-genzano.webp").is_file():
        log("Ultima scena già elaborata: " + f["id"])
        return 0
    dest = IMG_DIR / "sentinel1-genzano.webp"
    try:
        tmp = IMG_DIR / "sentinel1-genzano.nuovo.webp"
        info = ritaglia(f["assets"]["vv"]["href"], k[0], k[1], tmp)
    except Exception as e:  # noqa: BLE001
        log(f"Ritaglio non riuscito ({f['id']}): {e}. File lasciati com'erano.")
        return 0
    # l'immagine precedente diventa il «prima» del confronto a 10 m... 20 m
    if dest.is_file() and prec.get("id") and prec.get("id") != f["id"]:
        dest.replace(IMG_DIR / "sentinel1-genzano-prima.webp")
        prec_blocco = {kk: prec[kk] for kk in ("id", "quando", "satellite", "orbita", "riquadro") if kk in prec}
    else:
        prec_blocco = prec.get("precedente") or {}
    tmp.replace(dest)
    out = {
        "_snapshot": {"generato": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "fonte": "Copernicus Data Space Ecosystem — Sentinel-1 GRD IW (COG), polarizzazione VV",
                      "attribuzione": f"Contiene dati Copernicus Sentinel modificati {dt.date.today().year}",
                      "nota": "finestra riproiettata con i punti di controllo del prodotto, senza correzione del rilievo"},
        "id": f["id"], "quando": p.get("datetime"),
        "satellite": str(p.get("platform", "")).replace("sentinel-", "Sentinel-").upper().replace("SENTINEL", "Sentinel"),
        "orbita": p.get("sat:orbit_state"), "modo": p.get("sar:instrument_mode"),
        "immagine": "/images/sentinel/sentinel1-genzano.webp", "riquadro": info,
        "precedente": dict(prec_blocco, immagine="/images/sentinel/sentinel1-genzano-prima.webp") if prec_blocco else None,
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    log(f"Radar Sentinel-1 scritto: {f['id']} ({info['validi_pct']}% di pixel validi, {info['db_min']}…{info['db_max']} dB).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
