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

Dall'11/10/2026 c'è anche la MAPPA DEI CAMBIAMENTI: di ogni passaggio si
conserva la misura in decibel (PNG a 60 m, quantizzato a 0,25 dB) e il nuovo
passaggio si confronta con il più recente che ha la STESSA orbita relativa e la
stessa direzione: senza correzione del rilievo, due orbite diverse guardano i
versanti da angoli diversi e il confronto non avrebbe senso. Dove il segnale cala
di almeno SOGLIA_DB (superficie diventata liscia: acqua ferma, campo allagato) il
pixel è un candidato «acqua nuova»; dove sale, qualcosa di ruvido o metallico è
comparso. Sono indizi da verificare: anche pioggia, vento sui laghi e arature
cambiano il radar, e la pagina lo dice.

Scrive:
- static/images/sentinel/sentinel1-genzano.webp (ultima scena),
  sentinel1-genzano-prima.webp (la precedente), sentinel1-genzano-cambi.webp
  (mappa dei cambiamenti) e sentinel1-genzano-db-AAAAMMGGTHHMM.png (misure in
  decibel degli ultimi passaggi): stanno nella release «immagini-meteo», non
  in git (scripts/immagini-meteo-release.py);
- static/open-data/copernicus-sentinel1.json (in git): scena, satellite, orbita,
  riquadro dell'immagine in gradi per sovrapporla alla cartina, lo storico dei
  passaggi conservati e il blocco `cambi`.

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
RISOLUZIONE_M = 30.0      # 1000 x 1000 pixel: a 20 m il WebP pesava 1 MB (primo giro del 10/10/2026),
                          # troppo per un telefono in emergenza; a 30 m i laghi e i versanti si leggono uguali
GIORNI = 12
GIORNI_STORICO = 40       # misure in decibel conservate per il confronto a parita' di orbita (ciclo di 12 giorni)
STORICO_MAX = 8
DB_PX = 750               # 40 m: basta per un campo allagato, e il PNG pesa qualche centinaio di KB
DB_OFFSET, DB_PASSO = 20.0, 0.25  # quantizzazione: valore = DB_OFFSET + byte * DB_PASSO (20...83,75 dB)
SOGLIA_DB = 3.0           # variazione minima perche' un pixel conti come cambiato
FILTRO_PX = 5             # media mobile 5x5 (300 m) prima del confronto: il radar e' rumoroso (speckle)


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
    Image.fromarray(out, "L").save(dest, "WEBP", quality=72, method=6)
    s, w = gradi(xmin, ymin)
    n, e = gradi(xmax, ymax)
    return {"sud": round(s, 5), "ovest": round(w, 5), "nord": round(n, 5), "est": round(e, 5),
            "pixel": lato, "validi_pct": round(float(valido.mean() * 100)), "db_min": round(float(lo), 1), "db_max": round(float(hi), 1),
            "db": db}


# ------------------------------------------------- misure in decibel e cambiamenti
def riduci(a, lato: int):
    """Media a blocchi fino a lato x lato (nan ignorati)."""
    import numpy as np

    f = a.shape[0] // lato
    if f <= 1:
        return a
    b = a[:lato * f, :lato * f].reshape(lato, f, lato, f)
    ok = np.isfinite(b)
    somma = np.where(ok, b, 0).sum(axis=(1, 3))
    conto = ok.sum(axis=(1, 3))
    with np.errstate(invalid="ignore", divide="ignore"):
        m = somma / conto
    m[conto == 0] = np.nan
    return m


def salva_db(db, dest: Path) -> None:
    """PNG a 8 bit senza perdita: 0 = nessun dato, altrimenti DB_OFFSET + byte * DB_PASSO."""
    import numpy as np
    from PIL import Image

    r = riduci(db, DB_PX)
    q = np.clip(np.round((r - DB_OFFSET) / DB_PASSO), 1, 255)
    q = np.where(np.isfinite(r), q, 0).astype("uint8")
    Image.fromarray(q, "L").save(dest, "PNG", optimize=True)


def leggi_db(src: Path):
    import numpy as np
    from PIL import Image

    q = np.asarray(Image.open(src).convert("L"), dtype="float32")
    db = DB_OFFSET + q * DB_PASSO
    db[q == 0] = np.nan
    return db


def liscia(a, n: int):
    """Media mobile n x n (nan ignorati), con le somme cumulate: niente scipy."""
    import numpy as np

    ok = np.isfinite(a).astype("float32")
    v = np.nan_to_num(a, nan=0.0)
    r = n // 2
    def box(x):
        c = np.pad(x, r + 1)[:-1, :-1].cumsum(0).cumsum(1)
        return c[n:, n:] - c[:-n, n:] - c[n:, :-n] + c[:-n, :-n]
    somma, conto = box(v), box(ok)
    with np.errstate(invalid="ignore", divide="ignore"):
        m = somma / conto
    m[conto < n * n * 0.5] = np.nan
    return m


def cambiamenti(prima_png: Path, dopo_png: Path, dest: Path) -> dict:
    """Mappa dei cambiamenti fra due passaggi sulla stessa orbita (stessa geometria)."""
    import numpy as np
    from PIL import Image

    a, b = liscia(leggi_db(prima_png), FILTRO_PX), liscia(leggi_db(dopo_png), FILTRO_PX)
    if a.shape != b.shape:
        raise RuntimeError(f"misure di dimensione diversa ({a.shape} e {b.shape})")
    metri_px = 2 * MEZZO_LATO_KM * 1000 / a.shape[0]  # la superficie si misura sui pixel veri, non su una costante
    ettari_px = metri_px ** 2 / 10000
    v = np.isfinite(a) & np.isfinite(b)
    d = b - a
    # acqua nuova: segnale crollato E basso in assoluto (fra i piu' bassi della scena)
    basso = np.nanpercentile(b[v], 25) if v.any() else -np.inf
    scuro = v & (d <= -SOGLIA_DB) & (b <= basso)
    chiaro = v & (d >= SOGLIA_DB)
    rgba = np.zeros(v.shape + (4,), dtype="uint8")
    rgba[scuro] = (0, 90, 220, 210)
    rgba[chiaro] = (255, 140, 0, 190)
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".nuovo.webp")
    Image.fromarray(rgba, "RGBA").save(tmp, "WEBP", quality=75, method=6)
    tmp.replace(dest)
    return {"validi_pct": round(float(v.mean() * 100), 1), "acqua_nuova_ha": round(float(scuro.sum() * ettari_px)),
            "piu_riflettente_ha": round(float(chiaro.sum() * ettari_px)), "soglia_db": SOGLIA_DB,
            "filtro_m": round(FILTRO_PX * metri_px), "pixel_m": round(metri_px), "immagine": "/images/sentinel/" + dest.name}


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
        prec_blocco = {kk: prec[kk] for kk in ("id", "quando", "satellite", "orbita", "orbita_relativa", "riquadro") if kk in prec}
    else:
        prec_blocco = prec.get("precedente") or {}
    tmp.replace(dest)
    # misura in decibel di questo passaggio, conservata per i confronti futuri
    quando = p.get("datetime") or ""
    nome_db = "sentinel1-genzano-db-" + dt.datetime.fromisoformat(quando.replace("Z", "+00:00")).strftime("%Y%m%dT%H%M") + ".png" if quando else None
    storico = [r for r in (prec.get("storico") or []) if isinstance(r, dict) and r.get("db") and r.get("id") != f["id"]]
    if nome_db:
        salva_db(info.pop("db"), IMG_DIR / nome_db)
        voce = {"id": f["id"], "quando": quando, "satellite": str(p.get("platform", "")).replace("sentinel-", "Sentinel-").upper().replace("SENTINEL", "Sentinel"),
                "orbita": p.get("sat:orbit_state"), "orbita_relativa": p.get("sat:relative_orbit"), "db": "/images/sentinel/" + nome_db}
        storico = [voce] + storico
    else:
        info.pop("db", None)
    limite = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=GIORNI_STORICO)).strftime("%Y-%m-%dT%H:%M:%SZ")
    storico = [r for r in storico if (r.get("quando") or "") >= limite][:STORICO_MAX]
    tenuti = {Path(r["db"]).name for r in storico}
    for vecchio in IMG_DIR.glob("sentinel1-genzano-db-*.png"):
        if vecchio.name not in tenuti:
            vecchio.unlink()
            log(f"Tolta la misura piu' vecchia: {vecchio.name}")
    # confronto col passaggio precedente sulla STESSA orbita (stessa geometria di vista)
    cambi: dict | None = None
    gemello = next((r for r in storico[1:] if r.get("orbita_relativa") == p.get("sat:relative_orbit") and r.get("orbita") == p.get("sat:orbit_state")
                    and (IMG_DIR / Path(r["db"]).name).is_file()), None)
    if nome_db and gemello:
        try:
            cambi = dict(cambiamenti(IMG_DIR / Path(gemello["db"]).name, IMG_DIR / nome_db, IMG_DIR / "sentinel1-genzano-cambi.webp"),
                         prima=gemello["quando"], dopo=quando, satellite_prima=gemello.get("satellite"), orbita_relativa=p.get("sat:relative_orbit"))
            log(f"Cambiamenti rispetto al {gemello['quando'][:16]} (orbita {p.get('sat:relative_orbit')}): acqua nuova {cambi['acqua_nuova_ha']} ha, piu' riflettente {cambi['piu_riflettente_ha']} ha.")
        except Exception as e:  # noqa: BLE001
            log(f"Mappa dei cambiamenti non calcolata ({e}).")
    else:
        motivo = "nessun passaggio precedente sulla stessa orbita in archivio" if not gemello else "misura del passaggio precedente non disponibile"
        cambi = {"disponibile": False, "motivo": motivo, "dopo": quando, "orbita_relativa": p.get("sat:relative_orbit")}
        log(f"Cambiamenti non calcolabili: {motivo}.")
    out = {
        "_snapshot": {"generato": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "fonte": "Copernicus Data Space Ecosystem — Sentinel-1 GRD IW (COG), polarizzazione VV",
                      "attribuzione": f"Contiene dati Copernicus Sentinel modificati {dt.date.today().year}",
                      "nota": "finestra riproiettata con i punti di controllo del prodotto, senza correzione del rilievo"},
        "id": f["id"], "quando": p.get("datetime"),
        "satellite": str(p.get("platform", "")).replace("sentinel-", "Sentinel-").upper().replace("SENTINEL", "Sentinel"),
        "orbita": p.get("sat:orbit_state"), "orbita_relativa": p.get("sat:relative_orbit"), "modo": p.get("sar:instrument_mode"),
        "immagine": "/images/sentinel/sentinel1-genzano.webp", "riquadro": info,
        "precedente": dict(prec_blocco, immagine="/images/sentinel/sentinel1-genzano-prima.webp") if prec_blocco else None,
        "db_scala": {"offset": DB_OFFSET, "passo": DB_PASSO, "pixel": DB_PX, "nota": "valore in dB = offset + byte * passo; byte 0 = nessun dato"},
        "storico": storico,
        "cambi": cambi,
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    log(f"Radar Sentinel-1 scritto: {f['id']} ({info['validi_pct']}% di pixel validi, {info['db_min']}…{info['db_max']} dB).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
