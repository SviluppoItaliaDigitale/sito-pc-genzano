#!/usr/bin/env python3
"""Misure Sentinel-3 da Copernicus per il cruscotto: temperatura del suolo e fuochi.

Le immagini Sentinel-3 arrivano al cruscotto dal WMS di EUMETSAT senza chiave;
i NUMERI invece stanno nell'archivio del Copernicus Data Space Ecosystem, che
richiede un account (gratuito) e chiavi S3 di sola lettura. Questo script, che
gira in GitHub Actions con le chiavi nei segreti, scrive uno snapshot che il
browser legge dalla stessa origine:

    static/open-data/copernicus-sentinel3.json

Contenuto:
- `suolo`: temperatura della superficie a Genzano (prodotto SLSTR L2 LST, in
  gradi), una riga per passaggio delle ultime 36 ore, con nuvola/sereno,
  giorno/notte e satellite;
- `fuochi`: fuochi attivi rilevati nel Lazio e dintorni (prodotto SLSTR L2 FRP,
  potenza radiativa in MW), con distanza da Genzano.

Uso:
    python3 scripts/genera-copernicus-sentinel3.py            # snapshot
    python3 scripts/genera-copernicus-sentinel3.py --verifica # solo accesso S3
    python3 scripts/genera-copernicus-sentinel3.py --esplora  # stampa struttura dei file

Chiavi in CDSE_S3_ACCESS_KEY / CDSE_S3_SECRET_KEY. Senza chiavi non scrive nulla
ed esce 0 (la scheda resta spenta, mai dati di riempimento). Fail-safe: fonte
giù = file invariato, exit 0. Licenza dei dati: Copernicus Sentinel, libera con
attribuzione «Contiene dati Copernicus Sentinel modificati [anno]».
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import json
import math
import os
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "static" / "open-data" / "copernicus-sentinel3.json"
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/)"
STAC = "https://stac.dataspace.copernicus.eu/v1/search"
S3_ENDPOINT = "https://eodata.dataspace.copernicus.eu"
BUCKET = "eodata"
GENZANO = (41.7085, 12.6916)
# riquadro del Lazio e dintorni per i fuochi (lon_min, lat_min, lon_max, lat_max)
BBOX_LAZIO = (11.4, 40.7, 14.1, 42.9)
# riquadro stretto su Genzano per la temperatura
BBOX_GENZANO = (12.59, 41.61, 12.79, 41.81)
ORE = 36


def log(msg: str) -> None:
    print(msg, flush=True)


def chiavi() -> tuple[str, str] | None:
    a, s = os.environ.get("CDSE_S3_ACCESS_KEY", "").strip(), os.environ.get("CDSE_S3_SECRET_KEY", "").strip()
    return (a, s) if a and s else None


def s3_client(ak: str, sk: str):
    import boto3  # importato qui: in locale senza chiavi non serve

    return boto3.client("s3", endpoint_url=S3_ENDPOINT, aws_access_key_id=ak, aws_secret_access_key=sk,
                        region_name="default")


def stac(coll: str, bbox: tuple, ore: int, n: int = 20) -> list[dict]:
    a = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=ore)).strftime("%Y-%m-%dT%H:%M:%SZ")
    q = urllib.parse.urlencode({"collections": coll, "bbox": ",".join(map(str, bbox)),
                                "datetime": a + "/..", "limit": n})
    req = urllib.request.Request(STAC + "?" + q, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        d = json.load(r)
    feats = d.get("features", []) if isinstance(d, dict) else []
    feats.sort(key=lambda f: f.get("properties", {}).get("datetime", ""), reverse=True)
    return feats


def chiave_s3(href: str) -> str:
    # s3://eodata/Sentinel-3/... -> Sentinel-3/...
    assert href.startswith("s3://" + BUCKET + "/"), href
    return href[len("s3://" + BUCKET + "/"):]


def scarica(s3, href: str, dest: Path) -> Path:
    s3.download_file(BUCKET, chiave_s3(href), str(dest))
    return dest


def dist_km(lat: float, lon: float) -> float:
    p1, p2 = math.radians(GENZANO[0]), math.radians(lat)
    dl = math.radians(lon - GENZANO[1])
    return 6371 * math.acos(min(1.0, math.sin(p1) * math.sin(p2) + math.cos(p1) * math.cos(p2) * math.cos(dl)))


def rosa(lat: float, lon: float) -> str:
    ang = math.degrees(math.atan2(math.radians(lon - GENZANO[1]) * math.cos(math.radians(GENZANO[0])),
                                  math.radians(lat - GENZANO[0])))
    return ["nord", "nord-est", "est", "sud-est", "sud", "sud-ovest", "ovest", "nord-ovest"][round((ang % 360) / 45) % 8]


# ---------------------------------------------------------------- temperatura
def lst_genzano(s3, feat: dict, tmp: Path) -> dict | None:
    """Temperatura della superficie nel pixel SLSTR più vicino a Genzano."""
    import netCDF4
    import numpy as np

    a = feat.get("assets", {})
    need = {k: a.get(k, {}).get("href") for k in ("LST_in", "geodetic_in", "flags_in")}
    if not all(need.values()):
        return None
    files = {k: scarica(s3, h, tmp / (feat["id"] + "-" + k + ".nc")) for k, h in need.items()}
    with netCDF4.Dataset(files["geodetic_in"]) as g:
        lat, lon = g["latitude_in"][:], g["longitude_in"][:]
    d2 = (lat - GENZANO[0]) ** 2 + ((lon - GENZANO[1]) * math.cos(math.radians(GENZANO[0]))) ** 2
    d2 = np.ma.filled(d2, np.inf)
    i, j = np.unravel_index(int(np.argmin(d2)), d2.shape)
    if math.sqrt(float(d2[i, j])) * 111 > 3:  # il pixel più vicino è a più di 3 km: la scena non copre Genzano
        return None
    with netCDF4.Dataset(files["LST_in"]) as f:
        lst = f["LST"]
        fin = np.ma.filled(lst[max(0, i - 1):i + 2, max(0, j - 1):j + 2].astype(float), np.nan)
        val = float(lst[i, j]) if not np.ma.is_masked(lst[i, j]) else float("nan")
    with netCDF4.Dataset(files["flags_in"]) as f:
        conf = int(f["confidence_in"][i, j]) if "confidence_in" in f.variables else 0
        cloud = int(f["cloud_in"][i, j]) if "cloud_in" in f.variables else 0
        # bit del campo confidence_in (SLSTR L2 LST): 10 = giorno, 14 = summary_cloud
        giorno = bool(conf & (1 << 10))
        nuvola = bool(conf & (1 << 14)) or (cloud != 0)
    mediana = float(np.nanmedian(fin)) if np.isfinite(fin).any() else float("nan")
    p = feat.get("properties", {})
    return {
        "quando": p.get("datetime"),
        "satellite": str(p.get("platform", "")).replace("sentinel-", "Sentinel-").upper().replace("SENTINEL", "Sentinel"),
        "gradi": None if (not math.isfinite(val) or nuvola) else round(val - 273.15, 1),
        "gradi_intorno": None if (not math.isfinite(mediana) or nuvola) else round(mediana - 273.15, 1),
        "nuvola": nuvola,
        "giorno": giorno,
        "distanza_pixel_km": round(math.sqrt(float(d2[i, j])) * 111, 1),
    }


# ---------------------------------------------------------------------- fuochi
def frp_scene(s3, feat: dict, tmp: Path) -> list[dict]:
    """Fuochi attivi di una scena FRP, dai CSV (pochi KB), dentro il riquadro."""
    a = feat.get("assets", {})
    out: list[dict] = []
    p = feat.get("properties", {})
    sat = str(p.get("platform", "")).replace("sentinel-", "Sentinel-").upper().replace("SENTINEL", "Sentinel")
    for nome in ("FRP_MWIR1km_STANDARD_CSV", "FRP_SWIR500m_CSV"):
        href = a.get(nome, {}).get("href")
        if not href:
            continue
        f = scarica(s3, href, tmp / (feat["id"] + "-" + nome + ".csv"))
        # il CSV apre con righe di commento «#…» e una riga vuota, poi l'intestazione:
        # lat(deg),lon(deg),day,time,D/N,FRP(MW),FRPerr(MW),used_channel,confidence(%),…
        # (verificato sul prodotto del 10/10/2026)
        txt = "\n".join(l for l in f.read_text(encoding="utf-8", errors="replace").splitlines()
                        if l.strip() and not l.startswith("#"))
        righe = list(csv.DictReader(io.StringIO(txt)))
        for r in righe:
            k = {x.strip().lower(): x for x in r.keys()}
            try:
                lat = float(r[k[next(c for c in k if c.startswith("lat"))]])
                lon = float(r[k[next(c for c in k if c.startswith("lon"))]])
            except (StopIteration, KeyError, ValueError):
                continue
            if not (BBOX_LAZIO[0] <= lon <= BBOX_LAZIO[2] and BBOX_LAZIO[1] <= lat <= BBOX_LAZIO[3]):
                continue
            frp = conf = None
            for c in k:
                if c.startswith("frp") and "err" not in c and "unc" not in c:
                    try:
                        frp = round(float(r[k[c]]), 1)
                    except ValueError:
                        pass
                    break
            for c in k:
                if c.startswith("confidence("):
                    try:
                        conf = round(float(r[k[c]]))
                    except ValueError:
                        pass
                    break
            quando = p.get("datetime")
            if k.get("day") and k.get("time"):
                try:
                    quando = dt.datetime.strptime(r[k["day"]].strip() + " " + r[k["time"]].strip(), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    pass
            out.append({"lat": round(lat, 4), "lon": round(lon, 4), "mw": frp, "confidenza": conf,
                        "canale": "SWIR 500 m" if "SWIR" in nome else "MWIR 1 km",
                        "quando": quando, "satellite": sat,
                        "distanza_km": round(dist_km(lat, lon)), "direzione": rosa(lat, lon)})
    return out


# ---------------------------------------------------------------------- main
def esplora(s3) -> int:
    import netCDF4

    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        for coll, bbox in (("sentinel-3-sl-2-lst-nrt", BBOX_GENZANO), ("sentinel-3-sl-2-frp-nrt", BBOX_LAZIO)):
            feats = stac(coll, bbox, 48, 1)
            log(f"== {coll}: {len(feats)} scene")
            if not feats:
                continue
            f = feats[0]
            log("id " + f["id"])
            for k, a in f.get("assets", {}).items():
                h = a.get("href", "")
                if not h.startswith("s3://") or (a.get("file:size") or 0) > 12_000_000:
                    continue
                dest = scarica(s3, h, tmp / (k + Path(h).suffix))
                log(f"-- {k}: {dest.stat().st_size} byte")
                if dest.suffix == ".nc":
                    with netCDF4.Dataset(dest) as ds:
                        for v, var in ds.variables.items():
                            log(f"   {v} {var.dimensions} {var.dtype} " + " ".join(
                                f"{at}={getattr(var, at)!r}"[:120] for at in ("units", "flag_masks", "flag_meanings") if hasattr(var, at)))
                elif dest.suffix in (".csv", ".txt"):
                    log(dest.read_text(encoding="utf-8", errors="replace")[:1500])
    return 0


def main() -> int:
    k = chiavi()
    if not k:
        log("Chiavi Copernicus assenti (CDSE_S3_ACCESS_KEY/CDSE_S3_SECRET_KEY): nessuno snapshot scritto.")
        return 0
    try:
        s3 = s3_client(*k)
        if "--verifica" in sys.argv:
            r = s3.list_objects_v2(Bucket=BUCKET, Prefix="Sentinel-3/SLSTR/SL_2_LST___/" + dt.datetime.now(dt.timezone.utc).strftime("%Y/%m/%d/"), MaxKeys=3)
            n = r.get("KeyCount", 0)
            log(f"Accesso S3 riuscito: {n} oggetti letti nel prefisso di oggi.")
            return 0 if n else 1
        if "--esplora" in sys.argv:
            return esplora(s3)
        suolo, fuochi, scene_frp = [], [], 0
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            for f in stac("sentinel-3-sl-2-lst-nrt", BBOX_GENZANO, ORE, 8):
                try:
                    r = lst_genzano(s3, f, tmp)
                except Exception as e:  # noqa: BLE001
                    log(f"LST {f.get('id')}: {e}")
                    continue
                if r:
                    suolo.append(r)
            for f in stac("sentinel-3-sl-2-frp-nrt", BBOX_LAZIO, ORE, 12):
                try:
                    fuochi += frp_scene(s3, f, tmp)
                    scene_frp += 1
                except Exception as e:  # noqa: BLE001
                    log(f"FRP {f.get('id')}: {e}")
        if not suolo and not scene_frp:
            log("Nessuna scena letta: snapshot lasciato com'era.")
            return 0
        # Lo stesso fuoco compare sia nel CSV MWIR (1 km) sia in quello SWIR (500 m):
        # si tiene una riga per punto (griglia di ~1 km, stesso passaggio), preferendo
        # la rilevazione MWIR, che e' lo schema standard del prodotto.
        unici: dict[tuple, dict] = {}
        for f in sorted(fuochi, key=lambda x: 0 if x["canale"].startswith("MWIR") else 1):
            k = (round(f["lat"], 2), round(f["lon"], 2), (f["quando"] or "")[:13])
            unici.setdefault(k, f)
        fuochi = list(unici.values())
        # Nessuna scena FRP letta (fonte muta solo su quel prodotto): si conserva il
        # blocco dei fuochi dello snapshot precedente invece di dichiarare «nessun
        # fuoco», che sarebbe un'assenza inventata.
        blocco_fuochi = {"scene": scene_frp, "punti": fuochi, "riquadro": BBOX_LAZIO}
        if scene_frp == 0 and OUT.is_file():
            try:
                prec = json.loads(OUT.read_text(encoding="utf-8")).get("fuochi")
                if isinstance(prec, dict) and prec.get("scene"):
                    blocco_fuochi = dict(prec, conservato_da=json.loads(OUT.read_text(encoding="utf-8")).get("_snapshot", {}).get("generato"))
                    log("Nessuna scena FRP letta: conservato il blocco dei fuochi precedente.")
            except (OSError, ValueError):
                pass
        fuochi.sort(key=lambda x: x["distanza_km"])
        out = {
            "_snapshot": {"generato": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                          "fonte": "Copernicus Data Space Ecosystem — Sentinel-3 SLSTR L2 LST e FRP (NRT)",
                          "attribuzione": f"Contiene dati Copernicus Sentinel modificati {dt.date.today().year}",
                          "finestra_ore": ORE},
            "suolo": suolo,
            "fuochi": blocco_fuochi,
        }
        OUT.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
        log(f"Snapshot scritto: {len(suolo)} letture di temperatura, {len(fuochi)} fuochi in {scene_frp} scene.")
        return 0
    except Exception as e:  # noqa: BLE001
        log(f"Copernicus non raggiungibile o chiavi non valide: {e}. File lasciato com'era.")
        return 0 if "--verifica" not in sys.argv else 1


if __name__ == "__main__":
    sys.exit(main())
