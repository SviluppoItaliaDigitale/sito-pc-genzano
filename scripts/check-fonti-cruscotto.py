#!/usr/bin/env python3
"""Smoke-check delle fonti dati esterne del cruscotto (/cruscotto/).

Le schede del cruscotto leggono dati live da servizi di terzi (INGV, Open-Meteo,
DPC, EUMETSAT, NASA, EFFIS, ARPA Lazio, ItaliaMeteo/MeteoHub). Se uno di questi cambia endpoint o cade,
la scheda diventa vuota SENZA errore visibile. Questo script verifica ogni fonte
e stampa un report Markdown. Exit code = numero di fonti in errore (0 = tutto ok).

Solo stdlib: gira ovunque (locale + GitHub Actions) senza dipendenze.
Uso:  python3 scripts/check-fonti-cruscotto.py
"""
import json
import sys
import datetime
import urllib.request
import urllib.error

UA = "PCGenzano-cruscotto-healthcheck/1.0 (+https://www.protezionecivilegenzano.it)"
TIMEOUT = 30


def _get(url, expect_json=False, expect_image=False, accept=(200,)):
    """Ritorna (ok:bool, dettaglio:str, headers, body_or_json)."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            code = r.getcode()
            ctype = r.headers.get("Content-Type", "")
            lastmod = r.headers.get("Last-Modified", "")
            raw = r.read(200000)  # basta un assaggio
            if code not in accept:
                return False, f"HTTP {code}", lastmod, None
            if expect_image and not ctype.startswith("image"):
                return False, f"content-type «{ctype}» (atteso image)", lastmod, None
            if expect_json:
                try:
                    return True, f"HTTP {code}", lastmod, json.loads(raw.decode("utf-8", "replace"))
                except Exception as e:
                    return False, f"HTTP {code} ma JSON non valido ({e})", lastmod, None
            return True, f"HTTP {code}", lastmod, raw
    except urllib.error.HTTPError as e:
        if e.code in accept:
            return True, f"HTTP {e.code}", "", None
        return False, f"HTTP {e.code}", "", None
    except Exception as e:
        return False, f"{type(e).__name__}: {e}", "", None


def _utcnow():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)


def chk_ingv():
    frm = (_utcnow() - datetime.timedelta(days=7)).strftime("%Y-%m-%dT%H:%M:%S")
    url = ("https://webservices.ingv.it/fdsnws/event/1/query?starttime=" + frm +
           "&minmagnitude=2&minlatitude=35&maxlatitude=48&minlongitude=5&maxlongitude=20"
           "&format=geojson&orderby=time&limit=1")
    # 204 = nessun evento: il servizio è comunque su
    ok, det, _, _ = _get(url, expect_json=False, accept=(200, 204))
    return ok, det


def chk_openmeteo(kind, host, params):
    url = f"https://{host}/v1/{kind}?latitude=41.7085&longitude=12.6916&{params}"
    ok, det, _, j = _get(url, expect_json=True)
    if ok and isinstance(j, dict) and "current" not in j:
        return False, "manca il blocco «current» nella risposta"
    return ok, det


def chk_dpc_radar():
    ok, det, _, j = _get("https://radar-api.protezionecivile.it/findLastProductByType?type=SRI",
                         expect_json=True)
    if ok and not (isinstance(j, dict) and j.get("lastProducts")):
        return False, "manca «lastProducts» nella risposta"
    return ok, det


def chk_wms_getmap(layer, base):
    url = (base + "?service=WMS&request=GetMap&version=1.3.0&layers=" + layer +
           "&styles=&format=image/png&crs=EPSG:3857"
           "&bbox=556597,4163881,2226390,5780349&width=64&height=64")
    ok, det, _, _ = _get(url, expect_image=True)
    return ok, det


def chk_gibs():
    today = datetime.date.today().isoformat()
    url = ("https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/"
           "VIIRS_SNPP_CorrectedReflectance_TrueColor/default/" + today +
           "/GoogleMapsCompatible_Level9/4/5/8.jpg")
    ok, det, _, _ = _get(url, expect_image=True)
    return ok, det


def chk_arpa():
    url = "https://qa.arpalazio.net/img/qa/forecast/LAZIO/plots/mean_pm10_0.gif"
    ok, det, lastmod, _ = _get(url, expect_image=True)
    if ok and lastmod:
        try:
            dt = datetime.datetime.strptime(lastmod, "%a, %d %b %Y %H:%M:%S %Z")
            age_h = (_utcnow() - dt).total_seconds() / 3600
            if age_h > 96:
                return True, f"OK ma mappa ferma da {age_h/24:.1f} giorni (feed potenzialmente bloccato)"
            det += f" · aggiornata {age_h:.0f}h fa"
        except Exception:
            pass
    return ok, det


SORGENTI = [
    ("Terremoti — INGV FDSN", "Terremoti, Vulcani", chk_ingv),
    ("Meteo puntuale — Open-Meteo", "Meteo, cartine", lambda: chk_openmeteo("forecast", "api.open-meteo.com", "current=temperature_2m")),
    ("Aria — Open-Meteo Air Quality", "Aria e pollini", lambda: chk_openmeteo("air-quality", "air-quality-api.open-meteo.com", "current=european_aqi")),
    ("Mare — Open-Meteo Marine", "Mare", lambda: chk_openmeteo("marine", "marine-api.open-meteo.com", "current=wave_height")),
    ("Radar pioggia — DPC", "Radar pioggia", chk_dpc_radar),
    ("Satellite GeoColour — EUMETSAT", "Satellite", lambda: chk_wms_getmap("mtg_fd:rgb_geocolour", "https://view.eumetsat.int/geoserver/wms")),
    ("Satellite alta risoluzione — EUMETSAT", "Satellite", lambda: chk_wms_getmap("mtg_fd:vis06_hrfi", "https://view.eumetsat.int/geoserver/wms")),
    ("Satellite suolo — NASA GIBS", "Satellite", chk_gibs),
    ("Incendi — EFFIS/Copernicus", "Incendi", lambda: chk_wms_getmap("viirs.hs", "https://maps.effis.emergency.copernicus.eu/effis")),
    ("Qualità aria regionale — ARPA Lazio", "Aria e pollini", chk_arpa),
    ("Previsioni — ItaliaMeteo (ICON-2I)", "Previsioni ItaliaMeteo", lambda: chk_wms_getmap("meteohub:t2m-t2m", "https://maps.mistralportal.it/wms")),
    ("Mare onde — ItaliaMeteo (WW3)", "Mare ItaliaMeteo", lambda: chk_wms_getmap("meteohub:ww3_hs-hs", "https://maps.mistralportal.it/wms")),
]


def main():
    oggi = datetime.date.today().isoformat()
    righe, fails = [], 0
    for nome, scheda, fn in SORGENTI:
        try:
            ok, det = fn()
        except Exception as e:
            ok, det = False, f"{type(e).__name__}: {e}"
        if not ok:
            fails += 1
        icona = "✅" if ok else "❌"
        righe.append(f"| {icona} | {nome} | {scheda} | {det} |")

    print(f"# Salute delle fonti del cruscotto — {oggi}\n")
    if fails == 0:
        print("Tutte le fonti rispondono correttamente. ✅\n")
    else:
        print(f"⚠️ **{fails} fonte/i in errore.** La scheda corrispondente del "
              f"[cruscotto](https://www.protezionecivilegenzano.it/cruscotto/) "
              f"potrebbe risultare vuota. Verificare l'endpoint o aggiornare lo shortcode.\n")
    print("| Stato | Fonte | Scheda | Dettaglio |")
    print("|---|---|---|---|")
    print("\n".join(righe))
    print(f"\n_Controllo automatico `scripts/check-fonti-cruscotto.py`. "
          f"Un ❌ non implica sempre un guasto nostro: spesso è il servizio di terzi "
          f"temporaneamente giù. Se persiste, l'endpoint è cambiato._")
    return fails


if __name__ == "__main__":
    sys.exit(min(main(), 250))
