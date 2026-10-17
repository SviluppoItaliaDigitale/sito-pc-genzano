#!/usr/bin/env python3
"""Smoke-check delle fonti dati esterne del cruscotto (/cruscotto/).

Le schede del cruscotto leggono dati live da servizi di terzi (INGV, Open-Meteo,
DPC, EUMETSAT, NASA, EFFIS/GWIS, ARPA Lazio, ItaliaMeteo/MeteoHub; la Sala situazioni
/monitor/ anche il ricevitore SDR OpenWebRX+ di IZ0FKE). Se uno di questi cambia endpoint o cade,
la scheda diventa vuota SENZA errore visibile. Questo script verifica ogni fonte
e stampa un report Markdown. Exit code = numero di fonti in errore (0 = tutto ok).

Dal 17/10/2026 controlla anche le fonti dei generatori di snapshot (NASA
FIRMS, feed delle agenzie, feed YouTube dei canali monitorati) e l'ETA' dei
dati committati (snapshot in static/open-data/, ultimo controllo dell'allerta,
timbro del bollettino DPC): i generatori sono fail-safe e non segnalano nulla,
quindi una fonte che cade o un workflow che smette di girare si vedono solo
qui (istruzione del 17/10/2026: i 404 e simili non si ignorano).

Solo stdlib: gira ovunque (locale + GitHub Actions) senza dipendenze.
Uso:  python3 scripts/check-fonti-cruscotto.py
Variabili facoltative:
  FIRMS_MAP_KEY          chiave NASA FIRMS (in CI viene dal segreto omonimo)
  CHECK_FONTI_RADICE     cartella da cui leggere static/ e data/ (per le prove)
"""
import re
import json
import time
import sys
import datetime
import urllib.request
import urllib.error
import urllib.parse
import ast
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from zoneinfo import ZoneInfo

UA = "PCGenzano-cruscotto-healthcheck/1.0 (+https://www.protezionecivilegenzano.it)"
TIMEOUT = 30


def _get(url, expect_json=False, expect_image=False, accept=(200,)):
    """Ritorna (ok:bool, dettaglio:str, headers, body_or_json).

    Timeout ed errori di connessione si ritentano due volte a 10 secondi di
    distanza prima di dichiarare la fonte guasta: il 17/10/2026 due server
    EUMETSAT, raggiungibili da qui, sono andati in timeout dal runner di
    GitHub e al giro successivo rispondevano. Una risposta HTTP (404, 500…)
    invece è definitiva e non si ritenta."""
    for tentativo in range(3):
        esito = _get_una_volta(url, expect_json, expect_image, accept)
        if esito[0] or not esito[1].startswith(("TimeoutError", "URLError", "ConnectionResetError", "RemoteDisconnected", "timeout")):
            return esito
        if tentativo < 2:
            time.sleep(10)
    return esito[0], f"{esito[1]} (3 tentativi)", esito[2], esito[3]


def _get_una_volta(url, expect_json, expect_image, accept):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            code = r.getcode()
            ctype = r.headers.get("Content-Type", "")
            lastmod = r.headers.get("Last-Modified", "")
            # Quando serve il JSON va letto INTERO: il sample da 200 KB
            # troncava la risposta delle osservazioni ItaliaMeteo (>200 KB)
            # producendo il falso positivo "JSON non valido / Unterminated
            # string" (issue #567, 10/06/2026). Cap difensivo a 20 MB.
            raw = r.read(20_000_000) if expect_json else r.read(200000)
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


def _radice():
    """Radice del repository da cui leggere snapshot e data file. Per le prove
    si punta a una copia con CHECK_FONTI_RADICE, senza toccare i file veri."""
    alt = os.environ.get("CHECK_FONTI_RADICE", "").strip()
    return Path(alt) if alt else Path(__file__).resolve().parent.parent


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


def chk_effis_focolai():
    # Scheda Incendi: focolai degli ultimi 7 giorni (MODIS + VIIRS) dal WMS GWIS del
    # servizio europeo Copernicus. Fino al 14/10/2026 la scheda chiedeva «viirs.hs» al
    # WMS EFFIS senza data, e il servizio rispondeva con la sua data predefinita, il
    # 1° gennaio 2020: l'immagine arrivava regolare e questo controllo era verde, ma i
    # punti erano di sei anni prima. Ora si chiede «all.hs.week», che non ha dimensione
    # temporale, e si controlla che l'immagine su Europa e Africa contenga davvero dei
    # punti: in una settimana i focolai ci sono sempre (savane africane), e
    # un'immagine trasparente pesa meno di 5 KB.
    url = ("https://maps.effis.emergency.copernicus.eu/gwis?service=WMS&request=GetMap"
           "&version=1.3.0&layers=all.hs.week&styles=&format=image/png&transparent=true"
           "&crs=EPSG:3857&bbox=-2226390,-4163881,6679169,8399738&width=512&height=512")
    ok, det, _, raw = _get(url, expect_image=True)
    if not ok:
        return ok, det
    if raw is None or len(raw) < 5000:
        return False, "immagine quasi vuota (%d byte): nessun focolaio in una settimana su Europa e Africa vuol dire un guasto della fonte" % (len(raw or b""))
    return True, det + ", %d KB di focolai" % (len(raw) // 1024)


def chk_sentinel3():
    # Mosaico Sentinel-3 OLCI del giorno (scheda satellite del cruscotto). Oltre a
    # rispondere deve essere FRESCO: su EUMETView un layer Copernicus (la SST
    # giornaliera) e' rimasto fermo per mesi rispondendo regolarmente. L'ultimo
    # passaggio sta nel default della dimensione time delle capabilities.
    ok, det = chk_wms_getmap("copernicus:daily_sentinel3ab_olci_l1_rgb_fulres",
                             "https://view.eumetsat.int/geoserver/wms")
    if not ok:
        return ok, det
    ok2, det2, _, raw = _get("https://view.eumetsat.int/geoserver/copernicus/"
                             "daily_sentinel3ab_olci_l1_rgb_fulres/ows?service=WMS"
                             "&request=GetCapabilities&version=1.3.0")
    if not ok2 or raw is None:
        return False, "immagine OK, capabilities non leggibili (" + det2 + ")"
    m = re.search(rb'<Dimension[^>]*name="time"[^>]*default="([^"]+)"', raw)
    if not m:
        return False, "immagine OK, ora dell'ultimo passaggio non trovata"
    try:
        t = datetime.datetime.fromisoformat(m.group(1).decode().replace("Z", "+00:00"))
    except ValueError:
        return False, "ora dell'ultimo passaggio illeggibile: " + m.group(1).decode()
    ore = (datetime.datetime.now(datetime.timezone.utc) - t).total_seconds() / 3600
    if ore > 72:
        return False, f"mosaico fermo da {ore / 24:.0f} giorni (ultimo passaggio {t:%d/%m/%Y})"
    return True, f"HTTP 200, ultimo passaggio {ore:.0f} ore fa"


def chk_stac_copernicus():
    # Catalogo STAC pubblico di Copernicus: scene OLCI di Sentinel-3 che coprono
    # Genzano, lette dal browser nel riquadro sotto la cartina Sentinel-3.
    # Oltre a rispondere deve avere scene recenti: Sentinel-3A e 3B insieme
    # passano di giorno quasi ogni giorno, tre giorni senza scene sono un guasto.
    a = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=72)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = ("https://stac.dataspace.copernicus.eu/v1/search?collections=sentinel-3-olci-1-efr-nrt"
           "&bbox=12.59,41.61,12.79,41.81&datetime=" + a + "/..&limit=5")
    ok, det, _, j = _get(url, expect_json=True)
    if not ok:
        return ok, det
    n = len(j.get("features", [])) if isinstance(j, dict) else 0
    if n == 0:
        return False, "HTTP 200 ma nessuna scena OLCI su Genzano nelle ultime 72 ore"
    return True, f"HTTP 200, {n} scene nelle ultime 72 ore"


def chk_earth_search_s2():
    # Catalogo Earth Search (Element 84, AWS Open Data) delle scene Sentinel-2 L2A
    # su Genzano, da cui genera-copernicus-sentinel2.py ritaglia le immagini a
    # 10 m. Un passaggio ogni 2-3 giorni e il prodotto esce il giorno dopo:
    # dieci giorni senza scene sono un guasto. Si prova anche l'archivio COG
    # con una richiesta parziale (i primi KB del primo file), perche' catalogo
    # e archivio sono due servizi diversi.
    a = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=10)).strftime("%Y-%m-%dT%H:%M:%SZ")
    url = ("https://earth-search.aws.element84.com/v1/search?collections=sentinel-2-l2a"
           "&bbox=12.60,41.64,12.78,41.78&datetime=" + a + "/..&limit=5&sortby=-properties.datetime")
    ok, det, _, j = _get(url, expect_json=True)
    if not ok:
        return ok, det
    feats = j.get("features", []) if isinstance(j, dict) else []
    if not feats:
        return False, "HTTP 200 ma nessuna scena Sentinel-2 su Genzano negli ultimi 10 giorni"
    href = feats[0].get("assets", {}).get("visual", {}).get("href", "")
    if not href.startswith("https://"):
        return False, "catalogo OK ma il primo elemento non ha l'immagine a colori (visual)"
    try:
        req = urllib.request.Request(href, headers={"User-Agent": UA, "Range": "bytes=0-1023"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            dati = r.read()
        if r.status not in (200, 206) or len(dati) < 100:
            return False, f"archivio COG: risposta {r.status} di {len(dati)} byte"
    except Exception as e:  # noqa: BLE001
        return False, f"catalogo OK ({len(feats)} scene), archivio COG non leggibile: {e}"
    return True, f"HTTP 200, {len(feats)} scene negli ultimi 10 giorni, archivio COG leggibile"


def chk_cams_eu():
    # CAMS Europe via WMS pubblico ECMWF (token=public). Bbox Italia, layer PM2.5.
    # Il server risponde HTTP 302 -> redirect al PNG renderizzato in CDN streaming.
    url = ("https://eccharts.ecmwf.int/wms/?token=public"
           "&service=wms&VERSION=1.3.0&LAYERS=composition_europe_pm2p5_forecast_surface"
           "&FORMAT=image/png&REQUEST=GetMap&CRS=EPSG:4326&BBOX=35,5,48,20&WIDTH=64&HEIGHT=64")
    ok, det, _, _ = _get(url, accept=(200, 302))
    return ok, det


def chk_ems_rapid():
    # Copernicus EMS Rapid Mapping public JSON API (no auth).
    # NB: dal 24/08/2026 l'API NON espone piu' Access-Control-Allow-Origin, quindi il
    # browser non puo' leggerla: la scheda del cruscotto usa lo snapshot self-hosted
    # static/open-data/ems-attivazioni.json, rigenerato lato server da deploy.yml
    # (scripts/genera-ems-attivazioni.py). Questo check verifica la fonte a monte:
    # se cade, lo snapshot smette di aggiornarsi (i dati restano, ma invecchiano).
    url = "https://rapidmapping.emergency.copernicus.eu/backend/dashboard-api/public-activations-info/?limit=1"
    ok, det, _, j = _get(url, expect_json=True)
    if ok and isinstance(j, dict) and "results" in j:
        return True, f"{det} · {j.get('count', '?')} attivazioni totali"
    return False, det if not ok else "Risposta JSON inattesa (manca 'results')"


def chk_dpc_bollettino():
    # Bollettino di criticita' DPC. Il repository ufficiale NON espone un file
    # con nome stabile (i bollettini si chiamano col minuto di pubblicazione,
    # 20260922_1421.json), quindi il timbro si risolve in CI e la Sala legge il
    # nostro snapshot static/open-data/dpc-bollettino.json. Qui si controlla che
    # il bollettino indicato dallo snapshot esista ancora sulla fonte: se non
    # esiste, lo snapshot e' fermo o il DPC ha cambiato schema dei nomi.
    p = _radice() / "static" / "open-data" / "dpc-bollettino.json"
    if not p.exists():
        return False, "snapshot dpc-bollettino.json assente"
    try:
        snap = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        return False, f"snapshot illeggibile: {e}"
    stamp = snap.get("stamp") or ""
    if not re.fullmatch(r"\d{8}_\d{4}", stamp):
        return False, f"timbro non valido nello snapshot: {stamp!r}"
    base = "https://raw.githubusercontent.com/pcm-dpc/DPC-Bollettini-Criticita-Idrogeologica-Idraulica/master/files/"
    for nome in (f"{stamp}.json", f"topojson/{stamp}_today.json", f"topojson/{stamp}_tomorrow.json"):
        ok, det, _, _ = _get(base + nome, expect_json=False)
        if not ok:
            return False, f"{nome} non raggiungibile ({det})"
    # il mirror da cui si ricava il timbro: se muore si resta sull'API di
    # ripiego, che ha una quota per IP — meglio saperlo prima
    mirror = ("https://raw.githubusercontent.com/opendatasicilia/"
              "DPC-bollettini-criticita-idrogeologica-idraulica/refs/heads/main/"
              "data/bollettini/bollettino-oggi-zone-latest.csv")
    ok, det, _, _ = _get(mirror, expect_json=False)
    if not ok:
        return False, f"bollettino {stamp} presente, ma il mirror del timbro non risponde ({det})"
    return True, f"bollettino {stamp} presente sulla fonte · mirror del timbro attivo"


def chk_gdacs():
    # GDACS (allerte disastri globali) — fonte a monte dello snapshot
    # static/open-data/gdacs-eventi.json rigenerato da deploy.yml
    # (scripts/genera-gdacs-eventi.py), letto dalla Sala situazioni /monitor/.
    url = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/EVENTS4APP"
    ok, det, _, j = _get(url, expect_json=True)
    if ok and isinstance(j, dict) and isinstance(j.get("features"), list):
        return True, f"{det} · {len(j['features'])} eventi correnti"
    return False, det if not ok else "Risposta JSON inattesa (manca 'features')"


def chk_gibs():
    # Il mosaico "best" VIIRS true-color ha ~2 giorni di latenza di elaborazione:
    # la data odierna e quella di ieri restituiscono sistematicamente 404 (verificato
    # 04/08/2026 su più tile). Stesso offset usato lato client in dashboard-satellite.html.
    giorno = (datetime.date.today() - datetime.timedelta(days=2)).isoformat()
    url = ("https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/"
           "VIIRS_SNPP_CorrectedReflectance_TrueColor/default/" + giorno +
           "/GoogleMapsCompatible_Level9/4/5/8.jpg")
    ok, det, _, _ = _get(url, expect_image=True)
    return ok, det


def chk_gibs_tematici():
    """Livelli tematici NASA GIBS della scheda satellite (dall'11/10/2026): per ciascuno
    si chiede DescribeDomains (come fa il browser per datare il mosaico) e si
    controlla che l'ultimo giorno del dominio non sia piu' vecchio di 7 giorni:
    un livello che risponde ma non si aggiorna e' una scheda ferma, non una scheda sana."""
    # (layer, tile matrix set, eta' massima in giorni): il composito NDVI a 8 giorni e'
    # datato all'inizio del periodo, quindi «fresco» vuol dire fino a 12 giorni
    livelli = (("VIIRS_Combined_Flood_3-Day", "GoogleMapsCompatible_Level9", 7),
               ("VIIRS_NOAA20_NDSI_Snow_Cover", "GoogleMapsCompatible_Level8", 7),
               ("SMAP_L4_Analyzed_Surface_Soil_Moisture", "GoogleMapsCompatible_Level6", 7),
               ("VIIRS_NOAA21_Land_Surface_Temp_Day", "GoogleMapsCompatible_Level7", 7),
               ("MODIS_Terra_NDVI_8Day", "GoogleMapsCompatible_Level9", 12),
               ("MODIS_Combined_Value_Added_AOD", "GoogleMapsCompatible_Level6", 7))
    guasti = []
    for layer, tms, max_giorni in livelli:
        url = ("https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/wmts.cgi?SERVICE=WMTS&REQUEST=DescribeDomains"
               "&VERSION=1.0.0&LAYER=" + layer + "&TILEMATRIXSET=" + tms)
        ok, det, _, body = _get(url)
        if not ok:
            guasti.append(layer + ": " + det)
            continue
        m = re.search(r"<Domain>([^<]*)</Domain>", (body or b"").decode("utf-8", "replace"))
        ultimo = (m.group(1).split(",")[-1].split("/")[1] if m and "/" in m.group(1).split(",")[-1]
                  else (m.group(1).split(",")[-1] if m else ""))[:10]
        try:
            eta = (datetime.date.today() - datetime.date.fromisoformat(ultimo)).days
        except ValueError:
            guasti.append(layer + ": dominio temporale non leggibile")
            continue
        if eta > max_giorni:
            guasti.append(layer + f": ultimo mosaico di {eta} giorni fa ({ultimo}, limite {max_giorni})")
    return (False, "; ".join(guasti)) if guasti else (True, f"{len(livelli)} livelli aggiornati entro il loro limite")


def chk_obs_italiameteo():
    """API osservazioni MeteoHub: stazioni al suolo (temperatura, licenza CC BY)."""
    now = _utcnow()
    end = now.replace(minute=59, second=0, microsecond=0)
    start = (now - datetime.timedelta(hours=3)).replace(minute=0, second=0, microsecond=0)
    fmt = "%Y-%m-%d %H:%M"
    q = ("reftime: >=" + start.strftime(fmt) + ",<=" + end.strftime(fmt) +
         ";product:B12101;license:CCBY_COMPLIANT;timerange:254,0,0;level:103,2000,0,0")
    url = ("https://meteohub.agenziaitaliameteo.it/api/observations?q=" +
           urllib.parse.quote(q, safe=":,;<>=") + "&reliabilityCheck=true&last=true")
    ok, det, _, j = _get(url, expect_json=True)
    if ok and not (isinstance(j, dict) and j.get("data")):
        return False, "risposta senza stazioni nel blocco «data»"
    if ok and isinstance(j, dict):
        det += f" · {len(j.get('data', []))} stazioni"
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


def chk_sdr_noantri():
    # Ricevitore SDR OpenWebRX+ di IZ0FKE (Roma), vista RADIO della Sala
    # situazioni /monitor/ (iframe click-to-load). status.json è pubblico e
    # con CORS aperto: la vista lo legge per elencare i profili SDR (bande)
    # disponibili. Se cade, il pannello resta sui profili incorporati ma lo
    # spettro non si carica.
    return _chk_owrx("https://sdr.noantri.org/status.json")


def chk_sdr_i6iqx():
    # Secondo ricevitore della vista RADIO (I6IQX, Bucchianico): copre 80/160/60 m e
    # PMR446 che il ricevitore romano non ha. status.json senza CORS: la vista usa
    # la copia incorporata dei profili, questo check verifica che sia online.
    return _chk_owrx("https://sdr-plus.i6iqx.it/status.json")


def _chk_owrx(url):
    ok, det, _, j = _get(url, expect_json=True)
    if ok and isinstance(j, dict) and isinstance(j.get("sdrs"), list):
        prof = sum(len(s.get("profiles") or []) for s in j["sdrs"] if isinstance(s, dict))
        rx = (j.get("receiver") or {}).get("name", "?")
        return True, f"{det} · {rx} · {len(j['sdrs'])} SDR / {prof} profili · {j.get('version', '')}"
    return False, det if not ok else "Risposta JSON inattesa (manca 'sdrs')"


def chk_ioc_mareografi():
    """Mareografi IOC/UNESCO: si controlla anche la FRESCHEZZA, perche' una
    stazione che risponde con dati di ieri e' inutile quanto una muta."""
    url = ("https://www.ioc-sealevelmonitoring.org/service.php"
           "?query=data&code=AZ42&period=0.05&format=json")
    ok, det, _, j = _get(url, expect_json=True)
    if not ok:
        return False, det
    if not isinstance(j, list) or not j:
        return False, "Risposta senza campioni per la stazione di Anzio"
    try:
        ultimo = datetime.datetime.strptime(j[-1]["stime"], "%Y-%m-%d %H:%M:%S")
        ultimo = ultimo.replace(tzinfo=datetime.timezone.utc)
        eta = (datetime.datetime.now(datetime.timezone.utc) - ultimo).total_seconds() / 60
    except (KeyError, ValueError, TypeError) as e:
        return False, f"Campo stime illeggibile: {e}"
    if eta > 90:
        return False, f"{det} · ultimo campione di {eta:.0f} minuti fa (stazione ferma)"
    return True, f"{det} · Anzio: {len(j)} campioni, ultimo {eta:.0f} min fa"


def chk_emsc():
    url = ("https://www.seismicportal.eu/fdsnws/event/1/query?format=json&limit=1"
           "&minmag=3&minlat=30&maxlat=50&minlon=-12&maxlon=40")
    ok, det, _, j = _get(url, expect_json=True)
    if ok and isinstance(j, dict) and j.get("features"):
        return True, f"{det} · {len(j['features'])} evento di prova"
    return False, det if not ok else "Risposta JSON inattesa (manca 'features')"


def chk_pronto_soccorso():
    """Stato dei pronto soccorso: servizio della Regione Lazio (CC BY 4.0).

    Si controlla l'endpoint che la Sala legge attraverso il ponte PHP, e non
    solo che risponda: si verifica che torni i GRUPPI di triage. Una risposta
    valida ma senza gruppi vorrebbe dire schema cambiato, e la scheda
    mostrerebbe ospedali tutti a zero — che e' l'informazione opposta a
    "dato non disponibile".

    Nota: il servizio risponde 400 alle richieste che portano un'intestazione
    Origin, ed e' la ragione per cui esiste il ponte; qui si interroga come lo
    interroga il server, cioe' senza Origin.
    """
    url = ("https://server.salutelazio.it/server/external-services/facilities/"
           "structures/emergency-status?facilityId=PS000000000000000008")  # PS Castelli, Ariccia
    ok, det, _, j = _get(url, expect_json=True)
    if not ok:
        return False, det
    if not isinstance(j, dict) or not isinstance(j.get("groups"), list) or not j["groups"]:
        return False, "Risposta JSON inattesa (manca 'groups'): schema cambiato?"
    return True, f"{det} · {len(j['groups'])} codici di triage"


def chk_adsb():
    """Fonte dei mezzi aerei: adsb.lol (ODbL). La chiave dei velivoli e' 'ac'.
    Si controlla anche che l'elenco non sia VUOTO: sopra l'Italia centrale non
    capita mai, e una risposta valida ma senza velivoli e' il sintomo di uno
    schema cambiato — e' successo il 22/09/2026 passando da adsb.fi, che usava
    'aircraft', e per poco una fotografia buona veniva sovrascritta con una
    vuota senza che nulla segnalasse il guasto."""
    ok, det, _, j = _get("https://api.adsb.lol/v2/point/42.0/12.5/250", expect_json=True)
    if not ok:
        return False, det
    if not isinstance(j, dict) or not isinstance(j.get("ac"), list):
        return False, "Risposta JSON inattesa (manca 'ac'): schema cambiato?"
    n = len(j["ac"])
    if n == 0:
        return False, f"{det} · nessun velivolo nel cerchio centrale: schema cambiato?"
    return True, f"{det} · {n} velivoli nel cerchio centrale"


def chk_meteoalarm():
    # _get ritorna (ok, dettaglio, last-modified, corpo): il corpo e' il QUARTO valore.
    ok, det, _, corpo = _get("https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-italy")
    if not ok:
        return False, det
    b = corpo if isinstance(corpo, bytes) else (corpo or "").encode()
    if b"<feed" not in b:
        return False, "Risposta non riconosciuta come feed Atom"
    return True, f"{det} · {b.count(b'<entry')} avvisi nel feed"


def chk_celestrak():
    # Effemeridi orbitali della vista SATELLITI. Si controlla un gruppo piccolo e
    # stabile (le stazioni spaziali): se risponde quello, risponde l'endpoint.
    # Non si scarica il catalogo completo, che è di 2,7 MB.
    # Due tentativi: CelesTrak chiude ogni tanto la connessione a freddo e un
    # solo colpo produrrebbe un falso allarme settimanale. Non si tocca _get,
    # che e' condiviso con le altre fonti.
    for tentativo in range(2):
        ok, det, _, corpo = _get(
            "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=TLE")
        if ok:
            break
        if tentativo == 0:
            time.sleep(5)
    if not ok:
        return False, f"{det} (due tentativi)"
    txt = corpo.decode("utf-8", "replace") if isinstance(corpo, bytes) else (corpo or "")
    if "Invalid query" in txt:
        return False, "La fonte non riconosce più il gruppo richiesto"
    righe = [r for r in txt.splitlines() if r.startswith("1 ")]
    if not righe:
        return False, "Nessuna effemeride nella risposta"
    return True, f"{det} · {len(righe)} oggetti nel gruppo stazioni"


def chk_pagina_regione(url, cartella):
    """Pagine dei bollettini della Regione Lazio: devono elencare almeno un PDF
    nella cartella attesa. Il 14/10/2026 i vecchi indirizzi su
    protezionecivile.regione.lazio.it rimandavano alla home della protezione
    civile regionale (200, nessun PDF) e due script dell'allerta (avvisi meteo e
    rischio incendi) smettevano di trovare i bollettini senza nessun errore."""
    ok, det, _, raw = _get(url)
    if not ok or raw is None:
        return False, det
    txt = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else str(raw)
    pdf = re.findall(r'href="[^"]*/sites/default/files/' + re.escape(cartella) +
                     r'/[^"]*\.pdf"', txt, re.IGNORECASE)
    if not pdf:
        return False, (f"{det}, ma nessun PDF in «{cartella}»: la pagina è cambiata "
                       "e lo script dell'allerta non trova più i bollettini")
    return True, f"{det} · {len(set(pdf))} PDF in elenco"


# ---------------------------------------------------------------------------
# Fonti dei generatori di snapshot (17/10/2026)
# ---------------------------------------------------------------------------

FIRMS_SENSORI = ("VIIRS_SNPP_NRT", "VIIRS_NOAA20_NRT", "VIIRS_NOAA21_NRT")
# Riquadro piccolo sul Lazio: basta a sapere se chiave e sensore rispondono,
# senza scaricare l'Italia intera (lo fa gia' il generatore ogni 15 minuti).
FIRMS_AREA_PROVA = "11.4,40.7,14.1,42.9"


def chk_firms():
    """NASA FIRMS, fonte di scripts/genera-incendi-firms.py. Il generatore e'
    fail-safe: con la chiave rifiutata o un sensore spento esce 0 e lo
    snapshot resta com'era. Qui si prova ogni sensore che il generatore usa,
    con la stessa chiave. La chiave non compare mai nel report: e' nell'URL."""
    chiave = (os.environ.get("FIRMS_MAP_KEY") or "").strip()
    if not chiave:
        if os.environ.get("GITHUB_ACTIONS") == "true":
            return False, ("segreto FIRMS_MAP_KEY non passato al controllo: "
                           "la fonte non si puo' verificare")
        return True, ("chiave non disponibile in questo ambiente: fonte non "
                      "interrogata, vale il controllo dell'eta' dello snapshot")
    ok_s, ko_s = [], []
    for sensore in FIRMS_SENSORI:
        url = ("https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
               f"{chiave}/{sensore}/{FIRMS_AREA_PROVA}/1")
        ok, det, _, raw = _get(url)
        det = det.replace(chiave, "***")
        txt = raw.decode("utf-8", "replace") if isinstance(raw, bytes) else ""
        if not ok:
            if det == "HTTP 400":
                det = "HTTP 400: la fonte rifiuta la chiave o non conosce piu' il sensore"
            ko_s.append(f"{sensore} ({det})")
        elif "Invalid MAP_KEY" in txt or "MAP_KEY is invalid" in txt:
            ko_s.append(f"{sensore} (chiave rifiutata o limite di richieste superato)")
        elif not txt.strip() or "latitude" not in txt.splitlines()[0]:
            ko_s.append(f"{sensore} (risposta non riconosciuta come CSV)")
        else:
            ok_s.append(sensore)
        time.sleep(1)
    if ko_s:
        return False, ("sensori in errore: " + "; ".join(ko_s) +
                       ". Se un sensore e' stato dismesso, toglierlo da SENSORI "
                       "in genera-incendi-firms.py")
    return True, f"{len(ok_s)} sensori su {len(FIRMS_SENSORI)} rispondono con la nostra chiave"


AGENZIE = (
    ("ANSA", "https://www.ansa.it/sito/ansait_rss.xml"),
    ("ANSA CRONACA", "https://www.ansa.it/sito/notizie/cronaca/cronaca_rss.xml"),
    ("ADNKRONOS", "https://www.adnkronos.com/RSS_PrimaPagina.xml"),
)


def chk_feed_rss(url):
    """Feed RSS delle agenzie (scripts/genera-notizie-agenzie.py). Il
    generatore va avanti con i feed che rispondono, quindi uno caduto non si
    nota dalle notizie in pagina: si controlla ciascuno."""
    ok, det, _, raw = _get(url)
    if not ok:
        return False, det
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        return False, f"{det} ma XML non leggibile ({e})"
    voci = [i for i in root.iter("item")
            if (i.findtext("title") or "").strip() and (i.findtext("link") or "").strip()]
    if not voci:
        return False, f"{det} ma nessuna notizia con titolo e link: formato cambiato?"
    return True, f"{det} · {len(voci)} notizie"


def _canali_youtube():
    """CHANNEL_IDS letto dal sorgente di aggiorna-catalogo-video-feed.py senza
    importarlo (richiederebbe PyYAML): un elenco solo, nessuna copia."""
    p = Path(__file__).resolve().parent / "aggiorna-catalogo-video-feed.py"
    albero = ast.parse(p.read_text(encoding="utf-8"))
    for nodo in albero.body:
        if isinstance(nodo, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "CHANNEL_IDS" for t in nodo.targets):
            return ast.literal_eval(nodo.value)
    raise ValueError("CHANNEL_IDS non trovato in aggiorna-catalogo-video-feed.py")


def chk_feed_youtube():
    """Feed Atom dei canali YouTube monitorati (aggiorna-catalogo-video-feed.py).
    YouTube risponde ogni tanto 404/500 a freddo su un feed sano: due tentativi
    per canale prima di contarlo in errore."""
    canali = _canali_youtube()
    ko = []
    for nome, cid in canali.items():
        url = f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}"
        esito = None
        for tentativo in range(2):
            ok, det, _, raw = _get(url)
            if ok and raw and b"<entry" in raw:
                esito = None
                break
            esito = det if not ok else "feed senza video"
            if tentativo == 0:
                time.sleep(3)
        if esito:
            ko.append(f"{nome} ({esito})")
    if ko:
        return False, f"{len(ko)} canali su {len(canali)} in errore: " + "; ".join(ko)
    return True, f"{len(canali)} canali su {len(canali)} rispondono"


# ---------------------------------------------------------------------------
# Eta' dei dati committati (17/10/2026)
# ---------------------------------------------------------------------------
# I generatori riscrivono uno snapshot SOLO quando i dati cambiano, quindi il
# campo `generato` e' l'ora dell'ultima variazione. Le soglie stanno sopra le
# pause piu' lunghe osservate dal 25/09 al 17/10/2026 (git log dei file):
# lo scheduler di GitHub fa partire aggiorna-dati-sala.yml a blocchi, con
# pause fino a ~10 ore anche se il cron e' ogni 15 minuti.
SNAPSHOT_ETA = (
    # file, ore massime, perche' quella soglia
    ("notizie-agenzie.json", 12, "cambia a ogni giro; pause osservate fino a ~10 h per lo scheduler"),
    ("volo-soccorso.json", 12, "cambia a ogni giro (posizioni); pause osservate fino a ~10 h"),
    ("gdacs-eventi.json", 24, "cambia quasi a ogni giro; pausa massima osservata ~10 h"),
    ("incendi-firms.json", 36, "nuovi passaggi VIIRS piu' volte al giorno; pausa massima osservata ~24 h"),
    ("meteoalarm-italia.json", 120, "nei periodi calmi resta uguale per giorni; pausa massima osservata ~30 h"),
    ("ems-attivazioni.json", 168, "le attivazioni Copernicus cambiano di rado; pausa massima osservata ~43 h"),
)


def _iso_utc(valore):
    t = datetime.datetime.fromisoformat(str(valore).replace("Z", "+00:00"))
    if t.tzinfo is None:
        raise ValueError(f"orario senza fuso: {valore!r}")
    return t.astimezone(datetime.timezone.utc)


def _ore_da(t):
    return (datetime.datetime.now(datetime.timezone.utc) - t).total_seconds() / 3600


def chk_eta_snapshot(nome, soglia_ore):
    p = _radice() / "static" / "open-data" / nome
    if not p.exists():
        return False, f"{nome} assente: il generatore non l'ha mai scritto o e' stato tolto"
    try:
        snap = json.loads(p.read_text(encoding="utf-8"))
        gen = _iso_utc(snap["_snapshot"]["generato"])
    except Exception as e:
        return False, f"campo _snapshot.generato illeggibile ({type(e).__name__}: {e}): schema cambiato?"
    ore = _ore_da(gen)
    quando = gen.astimezone(ZoneInfo("Europe/Rome")).strftime("%d/%m %H:%M")
    if ore > soglia_ore:
        return False, (f"fermo da {ore:.0f} h (ultimo dato {quando} ora italiana, soglia {soglia_ore} h): "
                       "aggiorna-dati-sala.yml non gira o la fonte non risponde")
    return True, f"ultimo dato {quando} ora italiana ({ore:.1f} h, soglia {soglia_ore} h)"


ALLERTA_SOGLIA_ORE = 8


def chk_eta_allerta():
    """data/allerta.json: `ultimo_controllo` si riscrive almeno ogni ~6 h
    (heartbeat di check-allerta.py a 5h45'); pausa massima osservata 5h56'.
    Oltre 8 ore la catena cron-job.org -> check-allerta.yml e' ferma e la
    barra in homepage mostra un'allerta non piu' verificata."""
    p = _radice() / "data" / "allerta.json"
    try:
        dati = json.loads(p.read_text(encoding="utf-8"))
        t = _iso_utc(dati["ultimo_controllo"])
    except Exception as e:
        return False, f"ultimo_controllo illeggibile ({type(e).__name__}: {e})"
    ore = _ore_da(t)
    quando = t.astimezone(ZoneInfo("Europe/Rome")).strftime("%d/%m %H:%M")
    if ore > ALLERTA_SOGLIA_ORE:
        return False, (f"ultimo controllo {quando} ora italiana, {ore:.0f} h fa (soglia "
                       f"{ALLERTA_SOGLIA_ORE} h): check-allerta.yml non committa piu'")
    return True, f"ultimo controllo {quando} ora italiana ({ore:.1f} h, soglia {ALLERTA_SOGLIA_ORE} h)"


DPC_SOGLIA_ORE = 36


def chk_eta_dpc():
    """Timbro del bollettino DPC nello snapshot. Il Dipartimento pubblica ogni
    giorno, di norma fra le 13:30 e le 16:30: dal 25/09 al 17/10/2026 la pausa
    piu' lunga fra due timbri e' stata ~25 h. Oltre 36 h manca almeno un
    bollettino: generatore fermo, mirror fermo o schema cambiato. Il timbro e'
    l'ora italiana di pubblicazione (20261016_1418)."""
    p = _radice() / "static" / "open-data" / "dpc-bollettino.json"
    try:
        stamp = json.loads(p.read_text(encoding="utf-8")).get("stamp") or ""
        t = datetime.datetime.strptime(stamp, "%Y%m%d_%H%M").replace(tzinfo=ZoneInfo("Europe/Rome"))
    except Exception as e:
        return False, f"timbro illeggibile ({type(e).__name__}: {e})"
    ore = _ore_da(t)
    if ore > DPC_SOGLIA_ORE:
        return False, (f"bollettino {stamp} vecchio di {ore:.0f} h (soglia {DPC_SOGLIA_ORE} h): "
                       "il DPC pubblica ogni giorno, lo snapshot non segue piu' la fonte")
    return True, f"bollettino {stamp}, {ore:.1f} h fa (soglia {DPC_SOGLIA_ORE} h)"


SORGENTI = [
    ("Terremoti — INGV FDSN", "Terremoti, Vulcani", chk_ingv),
    ("Meteo puntuale — Open-Meteo", "Meteo, cartine", lambda: chk_openmeteo("forecast", "api.open-meteo.com", "current=temperature_2m")),
    ("Aria — Open-Meteo Air Quality", "Aria e pollini", lambda: chk_openmeteo("air-quality", "air-quality-api.open-meteo.com", "current=european_aqi")),
    ("Mare — Open-Meteo Marine", "Mare", lambda: chk_openmeteo("marine", "marine-api.open-meteo.com", "current=wave_height")),
    ("Radar pioggia — DPC", "Radar pioggia", chk_dpc_radar),
    ("Satellite GeoColour — EUMETSAT", "Satellite", lambda: chk_wms_getmap("mtg_fd:rgb_geocolour", "https://view.eumetsat.int/geoserver/wms")),
    ("Satellite alta risoluzione — EUMETSAT", "Satellite", lambda: chk_wms_getmap("mtg_fd:vis06_hrfi", "https://view.eumetsat.int/geoserver/wms")),
    ("Satellite Sentinel-3 — Copernicus/EUMETSAT", "Satellite", chk_sentinel3),
    ("Catalogo scene Sentinel-3 — Copernicus STAC", "Satellite", chk_stac_copernicus),
    ("Scene Sentinel-2 — Earth Search/AWS Open Data", "Satellite", chk_earth_search_s2),
    ("Satellite suolo — NASA GIBS", "Satellite", chk_gibs),
    ("Livelli tematici (alluvioni, neve, suolo, vegetazione, aerosol) — NASA GIBS", "Satellite", chk_gibs_tematici),
    ("Incendi — GWIS/EFFIS Copernicus (focolai 7 giorni)", "Incendi", chk_effis_focolai),
    ("Qualità aria regionale — ARPA Lazio", "Aria e pollini", chk_arpa),
    ("Aria Europa — Copernicus CAMS (WMS ECMWF)", "Aria Europa (CAMS)", chk_cams_eu),
    ("Emergenze EU — Copernicus EMS Rapid Mapping", "Emergenze EU (EMS)", chk_ems_rapid),
    ("Allerte globali — GDACS", "Sala situazioni (GDACS)", chk_gdacs),
    ("Bollettino criticità DPC", "Sala situazioni (ALLERTA, cartina zone)", chk_dpc_bollettino),
    ("Ricevitore SDR — OpenWebRX+ IZ0FKE", "Sala situazioni (RADIO)", chk_sdr_noantri),
    ("Ricevitore SDR — OpenWebRX+ I6IQX", "Sala situazioni (RADIO)", chk_sdr_i6iqx),
    ("Previsioni — ItaliaMeteo (ICON-2I)", "Previsioni ItaliaMeteo", lambda: chk_wms_getmap("meteohub:t2m-t2m", "https://maps.mistralportal.it/wms")),
    ("Mare onde — ItaliaMeteo (WW3)", "Mare ItaliaMeteo", lambda: chk_wms_getmap("meteohub:ww3_hs-hs", "https://maps.mistralportal.it/wms")),
    ("Radar SRI — ItaliaMeteo", "Radar ItaliaMeteo", lambda: chk_wms_getmap("meteohub:radar-sri", "https://maps.mistralportal.it/wms")),
    ("Osservazioni stazioni — ItaliaMeteo", "Osservazioni ItaliaMeteo", chk_obs_italiameteo),
    ("Mareografi — IOC/UNESCO", "Sala situazioni (ARIA·MARE)", chk_ioc_mareografi),
    ("Sismi euro-mediterranei — EMSC", "Sala situazioni (SISMICO)", chk_emsc),
    ("Mezzi aerei — adsb.lol", "Sala situazioni (EMERGENZE)", chk_adsb),
    ("Pronto soccorso — Regione Lazio", "Sala situazioni (EMERGENZE)", chk_pronto_soccorso),
    ("Effemeridi orbitali — CelesTrak", "Sala situazioni (SATELLITI)", chk_celestrak),
    ("Avvisi europei — MeteoAlarm", "Sala situazioni (ALLERTA)", chk_meteoalarm),
    ("Allertamenti meteo — Regione Lazio (pagina dei PDF)", "Barra avvisi meteo in homepage",
     lambda: chk_pagina_regione("https://www.regione.lazio.it/protezione-civile/"
                                "centro-funzionale-regionale/bollettini-allertamenti",
                                "allertamentiregionali-allegati")),
    ("Bollettini incendi AIB — Regione Lazio (pagina dei PDF)", "Barra rischio incendi in homepage",
     lambda: chk_pagina_regione("https://www.regione.lazio.it/protezione-civile/"
                                "centro-funzionale-regionale/bollettini-rischi-incendi",
                                "rischio-incendi")),
    ("Bollettini di criticità — Regione Lazio (pagina dei PDF)", "Barra allerta in homepage",
     lambda: chk_pagina_regione("https://www.regione.lazio.it/protezione-civile/"
                                "centro-funzionale-regionale/bollettini-criticita-idrogeologica-idraulica",
                                "criticita-idrogeologica")),
    ("Punti caldi da satellite — NASA FIRMS (chiave e sensori)", "Sala situazioni (EMERGENZE)", chk_firms),
] + [
    (f"Notizie — feed {nome}", "Sala situazioni (barra NOTIZIE)", (lambda u=url: chk_feed_rss(u)))
    for nome, url in AGENZIE
] + [
    ("Video — feed YouTube dei canali monitorati", "Approfondimenti video", chk_feed_youtube),
] + [
    (f"Età snapshot — {nome}", "Sala situazioni", (lambda n=nome, o=ore: chk_eta_snapshot(n, o)))
    for nome, ore, _motivo in SNAPSHOT_ETA
] + [
    ("Età bollettino DPC — timbro dello snapshot", "Sala situazioni (ALLERTA, cartina zone)", chk_eta_dpc),
    ("Età allerta — ultimo_controllo di data/allerta.json", "Barra allerta in homepage, CAP", chk_eta_allerta),
]


def main():
    oggi = datetime.date.today().isoformat()
    righe, fails, guasti = [], 0, []
    for nome, scheda, fn in SORGENTI:
        try:
            ok, det = fn()
        except Exception as e:
            ok, det = False, f"{type(e).__name__}: {e}"
        if not ok:
            fails += 1
            guasti.append(nome)
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
    # Firma dei guasti (solo i nomi, non i dettagli che cambiano a ogni giro):
    # il workflow commenta la issue solo quando cambia, cosi' niente spam.
    print(f"\n<!-- firma-guasti: {' | '.join(sorted(guasti))} -->")
    return fails


if __name__ == "__main__":
    sys.exit(min(main(), 250))
