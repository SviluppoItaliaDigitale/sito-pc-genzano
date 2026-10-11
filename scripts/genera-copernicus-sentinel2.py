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

Dall'11/10/2026, per ogni scena si calcolano anche tre INDICI dalle bande del
prodotto (rosso, verde, infrarosso vicino a 10 m; infrarosso a onde corte a
20 m), con le nuvole mascherate dalla SCL:
- NDVI (vegetazione): quanto è verde e viva la vegetazione;
- NDWI (acqua): acqua in superficie (laghi, allagamenti, campi sommersi);
- NBR (aree bruciate): l'indice con cui EFFIS e USGS mappano gli incendi.
Fra la scena più recente e la precedente si calcola la MAPPA DEI CAMBIAMENTI:
bruciato (dNBR ≥ SOGLIA_DNBR, severità almeno moderata-bassa secondo la scala
USGS), vegetazione persa (NDVI in calo di almeno SOGLIA_DNDVI), acqua nuova
(NDWI che passa da negativo a positivo), con le superfici in ettari. Sono
candidati da verificare sul posto, non certezze: fra due scene cambiano anche
stagione, luce e umidità del suolo, e la pagina lo dice.

Scrive:
- static/images/sentinel/sentinel2-genzano-AAAAMMGG.webp per le ultime MAX_SCENE
  scene utili (release «immagini-meteo», non git: scripts/immagini-meteo-release.py),
  più sentinel2-genzano-AAAAMMGG-{ndvi,ndwi,nbr}.webp (indici colorati, con
  trasparenza dove nuvole o dati mancanti) e sentinel2-genzano-cambi.webp;
- static/open-data/copernicus-sentinel2.json (in git): elenco delle scene con
  data, satellite, nuvole sulla finestra, riquadro in gradi per la cartina,
  medie degli indici per scena e il blocco `cambi`.

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
SCL_VALIDI = (4, 5, 6, 11)  # per gli indici: vegetazione, suolo nudo, acqua, neve (gli altri sono dubbi)
MARGINE_NUVOLE_PX = 6      # 120 m attorno a nuvole e ombre, che la SCL sottostima ai bordi
INDICI_PX = 800            # 20 m: la banda a onde corte (B12) del prodotto e' a 20 m
BANDE = {"red": "B04", "green": "B03", "nir": "B08", "swir22": "B12"}
ETTARI_PIXEL = (2 * MEZZO_LATO_KM * 1000 / INDICI_PX) ** 2 / 10000  # 0,04 ha a 20 m
SOGLIA_DNBR = 0.27         # USGS FIREMON / EFFIS: da qui in su severita' almeno moderata-bassa
SOGLIA_DNDVI = -0.20       # calo di vegetazione marcato (non stagionale)
CAMBI_MAX_GIORNI = 20      # oltre, fra due scene cambiano stagione e colture: il confronto non si fa
SOGLIA_NDWI_ACQUA = 0.0    # McFeeters: sopra lo zero e' acqua in superficie
INDICI_BACKFILL = 3        # scene gia' in archivio senza indici da completare per giro
# tappe di colore (valore -> rgb) per le immagini degli indici
TAPPE = {
    "ndvi": [(-0.2, (120, 80, 40)), (0.1, (230, 210, 150)), (0.3, (170, 200, 60)), (0.6, (30, 130, 20)), (0.9, (0, 50, 0))],
    # acqua: la terra resta quasi trasparente (quarta componente = opacita'), cosi' sotto si vede la scena
    "ndwi": [(-0.5, (200, 170, 120, 60)), (-0.1, (235, 235, 225, 60)), (0.1, (120, 180, 230, 230)), (0.5, (0, 40, 150, 240))],
    "nbr": [(-0.5, (130, 0, 20)), (-0.2, (220, 80, 20)), (0.1, (240, 220, 120)), (0.4, (90, 170, 60)), (0.8, (0, 70, 20))],
}


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


def scala_banda(f: dict, chiave: str) -> tuple[float, float]:
    """scale/offset della banda dal catalogo.

    Dal processing baseline 04.00 i prodotti L2A portano un offset di -0,1 sulla
    riflettanza, dichiarato in raster:bands; i COG di Earth Search pero' lo hanno
    GIA' APPLICATO (proprieta' earthsearch:boa_offset_applied) e in quel caso non
    va sottratto di nuovo: con l'offset doppio il lago Albano usciva con riflettanza
    negativa e l'NDVI medio della finestra era 0,85 (verificato l'11/10/2026).
    """
    b = (f.get("assets", {}).get(chiave, {}).get("raster:bands") or [{}])[0]
    offset = 0.0 if f.get("properties", {}).get("earthsearch:boa_offset_applied") else float(b.get("offset") or 0.0)
    return float(b.get("scale") or 0.0001), offset


def riflettanza(tiles: list[dict], chiave: str):
    """Riflettanza (0..1) di una banda sulla finestra a INDICI_PX; nan dove manca il dato."""
    import numpy as np
    from rasterio.enums import Resampling

    a, _ = componi(tiles, chiave, INDICI_PX, Resampling.bilinear)
    sc, off = scala_banda(tiles[0], chiave)
    r = a[0].astype("float32") * sc + off
    r[a[0] == 0] = np.nan
    return r


def dilata(m, n: int):
    """Allarga una maschera booleana di n pixel (8 vicini), senza scipy."""
    import numpy as np

    out = m.copy()
    for _ in range(n):
        p = np.pad(out, 1)
        out = (p[:-2, :-2] | p[:-2, 1:-1] | p[:-2, 2:] | p[1:-1, :-2] | p[1:-1, 1:-1] | p[1:-1, 2:]
               | p[2:, :-2] | p[2:, 1:-1] | p[2:, 2:])
    return out


def indici(tiles: list[dict], scl):
    """NDVI, NDWI e NBR (float32, nan dove nuvole, ombre o dati mancanti) sulla finestra.

    Si tengono solo i pixel che la SCL classifica con certezza (vegetazione, suolo,
    acqua, neve) e si scarta una fascia di MARGINE_NUVOLE_PX attorno a tutto il resto:
    ai bordi delle nuvole e delle ombre la maschera del prodotto e' ottimista, e
    senza margine la mappa dei cambiamenti disegnava «bruciato» il contorno di ogni
    cumulo (prima prova dell'11/10/2026: 977 ha bruciati in due giorni).
    """
    import numpy as np

    valido = np.isin(scl, SCL_VALIDI) & ~dilata(~np.isin(scl, SCL_VALIDI), MARGINE_NUVOLE_PX)
    b = {k: riflettanza(tiles, k) for k in BANDE}

    def nd(x, y):
        with np.errstate(divide="ignore", invalid="ignore"):
            r = (x - y) / (x + y)
        r = np.clip(r, -1, 1).astype("float32")
        r[~valido | ~np.isfinite(r)] = np.nan
        return r

    return {"ndvi": nd(b["nir"], b["red"]), "ndwi": nd(b["green"], b["nir"]), "nbr": nd(b["nir"], b["swir22"])}


def colora(v, tappe):
    """Immagine RGBA uint8: colore interpolato fra le tappe, trasparente dove nan."""
    import numpy as np

    xs = np.array([t[0] for t in tappe], dtype="float32")
    out = np.zeros(v.shape + (4,), dtype="uint8")
    ok = np.isfinite(v)
    vv = np.nan_to_num(v, nan=0.0)
    for c in range(4):
        ys = np.array([(t[1] + (230,))[c] for t in tappe], dtype="float32")
        out[..., c] = np.where(ok, np.interp(vv, xs, ys), 0).astype("uint8")
    return out


def salva_rgba(arr, dest: Path) -> None:
    from PIL import Image

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".nuovo.webp")
    Image.fromarray(arr).save(tmp, "WEBP", quality=75, method=6)
    tmp.replace(dest)


def riassunto_indici(ix: dict) -> dict:
    import numpy as np

    v = np.isfinite(ix["ndvi"])
    out = {"validi_pct": round(float(v.mean() * 100), 1)}
    if v.any():
        out["ndvi_medio"] = round(float(np.nanmean(ix["ndvi"])), 3)
        out["nbr_medio"] = round(float(np.nanmean(ix["nbr"])), 3)
        out["acqua_pct"] = round(float((ix["ndwi"][v] > SOGLIA_NDWI_ACQUA).mean() * 100), 1)
        out["acqua_ha"] = round(float((ix["ndwi"][v] > SOGLIA_NDWI_ACQUA).sum() * ETTARI_PIXEL))
    return out


def scrivi_indici(ix: dict, giorno: str) -> dict:
    """Le tre immagini colorate di una scena; ritorna il blocco `indici` per il JSON."""
    base = f"sentinel2-genzano-{giorno.replace('-', '')}"
    imgs = {}
    for k in ("ndvi", "ndwi", "nbr"):
        dest = IMG_DIR / f"{base}-{k}.webp"
        salva_rgba(colora(ix[k], TAPPE[k]), dest)
        imgs[k] = "/images/sentinel/" + dest.name
    return dict(riassunto_indici(ix), pixel=INDICI_PX, immagini=imgs)


def cambiamenti(prima: dict, dopo: dict, g_prima: str, g_dopo: str) -> dict:
    """Mappa dei cambiamenti fra due scene (stessa finestra, stesse soglie per tutti)."""
    import numpy as np

    v = np.isfinite(prima["nbr"]) & np.isfinite(dopo["nbr"]) & np.isfinite(prima["ndwi"]) & np.isfinite(dopo["ndwi"])
    dnbr = prima["nbr"] - dopo["nbr"]
    dndvi = dopo["ndvi"] - prima["ndvi"]
    # bruciato: NBR crollato E negativo dopo E vegetazione calata (un campo arato o
    # raccolto resta con NBR attorno allo zero: rilievo di revisione dell'11/10/2026)
    bruciato = v & (dnbr >= SOGLIA_DNBR) & (dopo["nbr"] < 0.0) & (dndvi <= -0.15)
    acqua = v & (dopo["ndwi"] > 0.1) & (prima["ndwi"] < SOGLIA_NDWI_ACQUA) & ~bruciato
    veg = v & (dndvi <= SOGLIA_DNDVI) & (dopo["ndvi"] < 0.4) & ~bruciato & ~acqua
    rgba = np.zeros(v.shape + (4,), dtype="uint8")
    rgba[bruciato] = (200, 20, 20, 210)
    rgba[veg] = (255, 140, 0, 190)
    rgba[acqua] = (0, 90, 220, 210)
    dest = IMG_DIR / "sentinel2-genzano-cambi.webp"
    salva_rgba(rgba, dest)
    return {"prima": g_prima, "dopo": g_dopo, "validi_pct": round(float(v.mean() * 100), 1),
            "bruciato_ha": round(float(bruciato.sum() * ETTARI_PIXEL)),
            "vegetazione_persa_ha": round(float(veg.sum() * ETTARI_PIXEL)),
            "acqua_nuova_ha": round(float(acqua.sum() * ETTARI_PIXEL)),
            "soglie": {"dnbr": SOGLIA_DNBR, "nbr_dopo_max": 0.0, "dndvi_bruciato": -0.15, "dndvi": SOGLIA_DNDVI, "ndwi_acqua": 0.1, "giorni_max": CAMBI_MAX_GIORNI},
            "immagine": "/images/sentinel/" + dest.name}


def elabora(feats: list[dict], dest: Path) -> dict:
    import numpy as np
    from PIL import Image
    from rasterio.enums import Resampling

    scl, usati = componi(feats, "scl", INDICI_PX, Resampling.nearest)
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
    ix = indici(feats, scl)  # prima di scrivere: se le bande non si leggono non resta una WebP orfana
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".nuovo.webp")
    Image.fromarray(np.moveaxis(rgb[:3], 0, -1).astype("uint8")).save(tmp, "WEBP", quality=80, method=6)
    tmp.replace(dest)
    return {"nuvole_pct": round(nuvole), "scartata": False, "pixel": lato, "tile": usati,
            "coperta_pct": round(float(valido.mean() * 100), 1), "indici": ix}


def indici_scena(feats: list[dict]):
    """Indici di una scena gia' in archivio (si rileggono le bande, qualche secondo)."""
    from rasterio.enums import Resampling

    scl, _ = componi(feats, "scl", INDICI_PX, Resampling.nearest)
    return indici(feats, scl[0])


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
    arrays: dict[str, dict] = {}  # giorno -> indici in memoria, per la mappa dei cambiamenti
    per_giorno = {t[0]["properties"]["datetime"][:10]: t for t in feats}
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
        arrays[g] = info["indici"]
        scene[g] = {"id": f["id"], "tile": info["tile"], "giorno": g, "quando": p["datetime"],
                    "satellite": str(p.get("platform", "")).replace("sentinel-", "Sentinel-").upper().replace("SENTINEL", "Sentinel"),
                    "nuvole_pct": info["nuvole_pct"], "nuvole_scena_pct": round(float(p.get("eo:cloud_cover") or 0)),
                    "coperta_pct": info["coperta_pct"], "immagine": "/images/sentinel/" + dest.name,
                    "indici": scrivi_indici(info["indici"], g)}
        log(f"Scena del {g} scritta da {', '.join(info['tile'])}: finestra coperta al {info['coperta_pct']}%, nuvole sul {info['nuvole_pct']}%, NDVI medio {scene[g]['indici'].get('ndvi_medio')}.")
    ordinate = [scene[g] for g in sorted(scene, reverse=True)][:massimo]
    # scene gia' in archivio senza indici (archivio nato prima dell'11/10/2026, o
    # un giro interrotto): si completano poche per volta, le piu' recenti prima
    completate = 0
    for sc in ordinate:
        g = sc["giorno"]
        if completate >= INDICI_BACKFILL:
            break
        manca = not sc.get("indici") or not all((IMG_DIR / Path(x).name).is_file() for x in sc["indici"].get("immagini", {}).values())
        if manca and g in per_giorno:
            try:
                arrays[g] = indici_scena(per_giorno[g])
                sc["indici"] = scrivi_indici(arrays[g], g)
                completate += 1
                log(f"Indici calcolati per la scena del {g} gia' in archivio.")
            except Exception as e:  # noqa: BLE001
                log(f"Indici della scena del {g} non calcolati ({e}): si riprova al giro dopo.")
    tenute = {Path(s["immagine"]).name for s in ordinate}
    tenute |= {Path(x).name for s in ordinate for x in (s.get("indici") or {}).get("immagini", {}).values()}
    for vecchio in glob.glob(str(IMG_DIR / "sentinel2-genzano-*.webp")):
        if Path(vecchio).name not in tenute and re.fullmatch(r"sentinel2-genzano-\d{8}(-ndvi|-ndwi|-nbr)?\.webp", Path(vecchio).name):
            os.remove(vecchio)
            log(f"Tolta la scena piu' vecchia: {Path(vecchio).name}")
    if not ordinate:
        log("Nessuna scena utile (tutte nuvolose o non leggibili): nessun file scritto.")
        return 0
    # mappa dei cambiamenti fra le due scene piu' recenti, rifatta quando cambia la coppia
    cambi = prec.get("cambi") if isinstance(prec.get("cambi"), dict) else None
    coppia = [s["giorno"] for s in ordinate[:2]]
    distanza = (dt.date.fromisoformat(coppia[0]) - dt.date.fromisoformat(coppia[1])).days if len(coppia) == 2 else None
    if distanza is not None and distanza > CAMBI_MAX_GIORNI:
        cambi = {"disponibile": False, "prima": coppia[1], "dopo": coppia[0], "giorni": distanza,
                 "motivo": f"le due scene distano {distanza} giorni: oltre {CAMBI_MAX_GIORNI} cambiano stagione e colture, il confronto non si fa"}
        if (IMG_DIR / "sentinel2-genzano-cambi.webp").is_file():
            os.remove(IMG_DIR / "sentinel2-genzano-cambi.webp")
    elif len(coppia) == 2 and (forza or not cambi or [cambi.get("prima"), cambi.get("dopo")] != [coppia[1], coppia[0]]
                               or not (IMG_DIR / "sentinel2-genzano-cambi.webp").is_file()):
        try:
            for g in coppia:
                if g not in arrays:
                    arrays[g] = indici_scena(per_giorno[g])
            cambi = dict(cambiamenti(arrays[coppia[1]], arrays[coppia[0]], coppia[1], coppia[0]), giorni=distanza)
            log(f"Cambiamenti {coppia[1]} -> {coppia[0]}: bruciato {cambi['bruciato_ha']} ha, vegetazione persa {cambi['vegetazione_persa_ha']} ha, acqua nuova {cambi['acqua_nuova_ha']} ha.")
        except Exception as e:  # noqa: BLE001
            log(f"Mappa dei cambiamenti non calcolata ({e}): si riprova al giro dopo.")
            if cambi and [cambi.get("prima"), cambi.get("dopo")] != [coppia[1], coppia[0]]:
                cambi = None  # una mappa di un'altra coppia non si spaccia per questa
    elif len(coppia) < 2:
        cambi = None
    if cambi and cambi.get("immagine") and not (IMG_DIR / Path(cambi["immagine"]).name).is_file():
        cambi = None  # il JSON non deve puntare a un'immagine che non c'e'
    if nuove == 0 and completate == 0 and not forza and [s["giorno"] for s in prec.get("scene", [])] == [s["giorno"] for s in ordinate] and cambi == prec.get("cambi"):
        log("Nessuna scena nuova: file invariati.")
        return 0
    xmin, ymin, xmax, ymax = riquadro_3857()
    s, w = gradi(xmin, ymin)
    n, e = gradi(xmax, ymax)
    out = {
        "_snapshot": {"generato": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                      "fonte": "Sentinel-2 L2A a colori naturali (TCI, 10 m), archivio Cloud Optimized GeoTIFF su AWS Open Data, catalogo Earth Search (Element 84)",
                      "attribuzione": f"Contiene dati Copernicus Sentinel modificati {dt.date.today().year}",
                      "nota": "nuvole_pct e' la copertura calcolata sulla finestra dalla maschera SCL del prodotto; nuvole_scena_pct e' la stima della scena intera; i cambiamenti sono candidati da verificare, non certezze"},
        "riquadro": {"sud": round(s, 5), "ovest": round(w, 5), "nord": round(n, 5), "est": round(e, 5)},
        "risoluzione_m": RISOLUZIONE_M, "pixel": int(round(2 * MEZZO_LATO_KM * 1000 / RISOLUZIONE_M)),
        "scene": ordinate,
        "indici_nota": "NDVI, NDWI e NBR calcolati dalle bande L2A a 20 m con le nuvole mascherate dalla SCL; medie sui soli pixel validi",
        "cambi": cambi,
        # le date nuvolose si ricordano per tutta la finestra del catalogo, altrimenti
        # ogni giro rileggerebbe la maschera SCL delle stesse scene scartate
        "scartate": sorted(x for x in scartate if x >= (dt.date.today() - dt.timedelta(days=GIORNI)).isoformat())[-40:],
    }
    OUT_JSON.write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")) + "\n", encoding="utf-8")
    log(f"Sentinel-2: {len(ordinate)} scene in archivio, {nuove} nuove ({ordinate[0]['giorno']} la piu' recente).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
