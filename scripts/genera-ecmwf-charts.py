#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
genera-ecmwf-charts.py — Scarica e auto-ospita le carte di previsione ECMWF OpenCharts.

Le OpenCharts (https://charts.ecmwf.int/) sono un catalogo di mappe di previsione
del Centro europeo per le previsioni meteo a medio termine (ECMWF). Dal 1° ottobre
2025 l'intero catalogo è dato pienamente aperto con licenza Creative Commons CC BY 4.0,
senza chiave API e senza costi (https://www.ecmwf.int/en/forecasts/datasets/open-data).

Questo script scarica un sottoinsieme curato di carte sinottiche europee a medio termine
tramite l'OpenCharts API pubblica, le converte in WebP e le auto-ospita nel repo
(privacy-first: nessun embed di terzi nel browser del cittadino). Stesso pattern dei
generatori meteo-* (Open-Meteo) già nel sito.

A differenza delle schede locali (Open-Meteo/ItaliaMeteo/ARPA), che danno il dettaglio
puntuale su Genzano e il Lazio, qui si mostra il QUADRO SINOTTICO EUROPEO A MEDIO TERMINE:
ogni carta è una vera PREVISIONE a +72 ore (~3 giorni), non l'analisi attuale. Il passo
di previsione è configurabile (GIORNI_AVANTI); se il passo non è disponibile per un
prodotto, lo script ripiega graziosamente sull'ultima carta disponibile (analisi +0h).

Attribuzione obbligatoria CC BY 4.0: ogni carta è mostrata con il credito
"based on data and products of the European Centre for Medium-Range Weather Forecasts
(ECMWF), CC BY 4.0".

API: GET https://charts.ecmwf.int/opencharts-api/v1/products/<slug>/?projection=...&valid_time=...
     → JSON con data.link.href = URL del PNG renderizzato e data.attributes.description
       = "Base time: ... Valid time: ... (+Xh) Area : Europe".

Output:
  - static/images/ecmwf/<slug>.webp   una carta per prodotto (passo di previsione scelto)
  - data/ecmwf_charts.json            metadati (titolo, valid time, corsa, aggiornamento)

Uso:
  python3 scripts/genera-ecmwf-charts.py [--dry-run]

Exit code:
  0  almeno una carta scaricata/aggiornata con successo (o nessuna modifica)
  1  errore: nessuna carta scaricabile (il workflow apre un'issue)

Dipendenze: solo stdlib + Pillow (python3-pil).
"""

import io
import json
import os
import re
import ssl
import sys
import time
import datetime
import urllib.request
import urllib.error

from PIL import Image

API_BASE = "https://charts.ecmwf.int/opencharts-api/v1/products/"
# Proiezione europea del catalogo OpenCharts (centra la carta su Europa/Mediterraneo).
PROJECTION = "opencharts_europe"
# Orizzonte di previsione mostrato (giorni avanti). +72h è un classico medio termine:
# abbastanza lontano da essere "previsione" utile, abbastanza vicino da essere affidabile.
GIORNI_AVANTI = 3

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO, "static", "images", "ecmwf")
OUT_JSON = os.path.join(REPO, "data", "ecmwf_charts.json")

# Sottoinsieme curato di prodotti a medio termine, scelti per pertinenza alla
# protezione civile (quadro sinottico europeo, non bollettino locale). Slug
# confermati dal catalogo OpenCharts ECMWF.
PRODOTTI = [
    {
        "slug": "medium-mslp-wind850",
        "titolo": "Pressione e vento",
        "descr": "Pressione al livello del mare e vento a 850 hPa: la classica carta "
                 "sinottica con cicloni, anticicloni e flusso delle correnti.",
        "icona": "bi-hurricane",
    },
    {
        "slug": "medium-2mt-wind30",
        "titolo": "Temperatura e vento",
        "descr": "Temperatura a 2 metri dal suolo e vento a 30 metri: caldo, freddo "
                 "e ventilazione previsti sull'Europa.",
        "icona": "bi-thermometer-half",
    },
    {
        "slug": "medium-precipitation-type",
        "titolo": "Precipitazioni",
        "descr": "Tipo e intensità di precipitazione prevista (pioggia, neve, "
                 "gelicidio): dove e quando è atteso il maltempo.",
        "icona": "bi-cloud-rain-heavy",
    },
    {
        "slug": "medium-cape-cin",
        "titolo": "Temporali (CAPE/CIN)",
        "descr": "Energia potenziale convettiva (CAPE) e inibizione (CIN): "
                 "indicatori del rischio di temporali forti e fenomeni convettivi.",
        "icona": "bi-cloud-lightning-rain",
    },
]

USER_AGENT = ("ProtezioneCivileGenzano/1.0 (+https://www.protezionecivilegenzano.it/) "
              "OpenCharts self-host")
TIMEOUT = 60

# Contesto SSL standard (le runner GitHub Actions hanno il CA store completo).
_CTX = ssl.create_default_context()

_GIORNI = {"Mon": "lunedì", "Tue": "martedì", "Wed": "mercoledì", "Thu": "giovedì",
           "Fri": "venerdì", "Sat": "sabato", "Sun": "domenica"}
_MESI = {"Jan": "gennaio", "Feb": "febbraio", "Mar": "marzo", "Apr": "aprile",
         "May": "maggio", "Jun": "giugno", "Jul": "luglio", "Aug": "agosto",
         "Sep": "settembre", "Oct": "ottobre", "Nov": "novembre", "Dec": "dicembre"}

# "Sun 31 May 2026 00 UTC" → ("domenica 31 maggio 2026, 00 UTC")
_DATE_RE = r"(\w{3})\s+(\d{1,2})\s+(\w{3})\s+(\d{4})\s+(\d{2})\s+UTC"


def _ita_data(m):
    dow, day, mon, year, hh = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
    return "{} {} {} {}, {} UTC".format(
        _GIORNI.get(dow, dow), int(day), _MESI.get(mon, mon), year, hh)


def parse_descrizione(desc):
    """Estrae (corsa_italiana, valido_italiano, passo) dalla descrizione OpenCharts.

    Es. "Base time: Sun 31 May 2026 00 UTC Valid time: Wed 03 Jun 2026 00 UTC (+72h) ..."
    → ("domenica 31 maggio 2026, 00 UTC", "mercoledì 3 giugno 2026, 00 UTC", "+72h").
    Restituisce stringhe vuote per i campi non trovati (mai solleva).
    """
    corsa = valido = passo = ""
    mb = re.search(r"Base time:\s*" + _DATE_RE, desc or "")
    if mb:
        corsa = _ita_data(mb)
    mv = re.search(r"Valid time:\s*" + _DATE_RE + r"\s*\(([+-]\d+h)\)", desc or "")
    if mv:
        valido = _ita_data(mv)
        passo = mv.group(6)
    return corsa, valido, passo


def target_valid_time(now_utc, giorni=GIORNI_AVANTI):
    """Valid time bersaglio: 00:00 UTC di `giorni` giorni avanti (formato ISO Z).

    Ancorato alle 00:00 UTC: lo scarto dalla corsa più recente (00/06/12/18 Z) è
    sempre un multiplo di 12 ore, quindi un passo previsionale standard sempre
    disponibile per i prodotti medium di OpenCharts.
    """
    t = now_utc.replace(hour=0, minute=0, second=0, microsecond=0) \
        + datetime.timedelta(days=giorni)
    return t.strftime("%Y-%m-%dT%H:00:00Z")


def _get(url, accept="application/json"):
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": accept,
    })
    # Retry sugli errori di rete transitori dei runner CI (DNS, timeout, 5xx):
    # 3 tentativi con attesa crescente. I 4xx non si ritentano (non transitori).
    for tentativo in range(3):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT, context=_CTX) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code < 500 or tentativo == 2:
                raise
        except (urllib.error.URLError, OSError):
            if tentativo == 2:
                raise
        attesa = 15 * (tentativo + 1)
        print(f"[retry] errore di rete, riprovo tra {attesa}s: {url[:90]}", file=sys.stderr)
        time.sleep(attesa)


def risolvi_immagine(slug, valid_time=None):
    """Interroga l'OpenCharts API e restituisce (href_png, meta) o (None, errore).

    Prova prima il passo di previsione richiesto (valid_time); se non è disponibile
    ripiega sull'ultima carta del prodotto (analisi +0h). `meta` contiene la
    descrizione testuale ECMWF (base/valid time) per le etichette oneste.
    """
    candidati = []
    if valid_time:
        candidati.append("{}{}/?projection={}&valid_time={}".format(
            API_BASE, slug, PROJECTION, valid_time))
    candidati.append("{}{}/?projection={}".format(API_BASE, slug, PROJECTION))
    candidati.append("{}{}/".format(API_BASE, slug))
    ultimo_err = None
    for url in candidati:
        try:
            raw = _get(url)
            doc = json.loads(raw.decode("utf-8"))
            data = doc.get("data") or {}
            link = data.get("link") or {}
            href = link.get("href")
            if href:
                attrs = data.get("attributes") or {}
                meta = {
                    "titolo_api": attrs.get("title") or "",
                    "descrizione": attrs.get("description") or "",
                    "copyright": (doc.get("meta") or {}).get("copyright") or "",
                }
                return href, meta
            ultimo_err = "JSON senza data.link.href ({})".format(url)
        except urllib.error.HTTPError as e:
            ultimo_err = "HTTP {} su {}".format(e.code, url)
        except Exception as e:  # noqa: BLE001
            ultimo_err = "{}: {} ({})".format(type(e).__name__, e, url)
    return None, ultimo_err


def scarica_webp(href, dest, dry_run=False):
    """Scarica il PNG, lo converte in WebP e lo scrive SOLO se è cambiato.

    ECMWF restituisce la stessa carta finché non esce una corsa nuova: confrontando
    i byte WebP con il file esistente, scriviamo (e committiamo, e ridepoyiamo) solo
    quando il dato è davvero nuovo. Restituisce True se il file è stato (ri)scritto.
    """
    png = _get(href, accept="image/png,*/*")
    img = Image.open(io.BytesIO(png))
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")
    # Le carte ECMWF sono ~1000-1600px: nessun upscaling, eventuale downscale soft.
    max_w = 1600
    if img.width > max_w:
        h = round(img.height * max_w / img.width)
        img = img.resize((max_w, h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "WEBP", quality=90, method=6)
    nuovi = buf.getvalue()
    if os.path.exists(dest):
        with open(dest, "rb") as f:
            if f.read() == nuovi:
                return False  # carta invariata: nessuna corsa nuova
    if dry_run:
        return True
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "wb") as f:
        f.write(nuovi)
    return True


def main():
    dry_run = "--dry-run" in sys.argv
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_rome = now_utc.astimezone(datetime.timezone(datetime.timedelta(hours=2)))  # CEST
    stamp = now_rome.strftime("%Y-%m-%dT%H:%M")
    vt = target_valid_time(now_utc, GIORNI_AVANTI)

    carte = []
    corsa = ""  # corsa del modello (base time), dalla prima carta risolta
    ok = 0
    cambiate = 0
    errori = []

    for p in PRODOTTI:
        slug = p["slug"]
        href, meta = risolvi_immagine(slug, valid_time=vt)
        if not href:
            errori.append("{}: {}".format(slug, meta))
            print("[ko ] {} — {}".format(slug, meta), file=sys.stderr)
            continue
        dest = os.path.join(OUT_DIR, slug + ".webp")
        try:
            scritto = scarica_webp(href, dest, dry_run=dry_run)
            ok += 1
            if scritto:
                cambiate += 1
            c_corsa, valido, passo = parse_descrizione(meta.get("descrizione", ""))
            if c_corsa and not corsa:
                corsa = c_corsa
            carte.append({
                "slug": slug,
                "titolo": p["titolo"],
                "descr": p["descr"],
                "icona": p["icona"],
                "file": "/images/ecmwf/{}.webp".format(slug),
                "valido": valido,
                "passo": passo,
            })
            etich = "AGGIORNATA" if scritto else "invariata"
            print("[ok ] {} {} {} {}".format(
                slug, passo or "?", etich, "(dry-run)" if dry_run else ""))
        except Exception as e:  # noqa: BLE001
            errori.append("{}: download/convert {}".format(slug, e))
            print("[ko ] {} — download/convert: {}".format(slug, e), file=sys.stderr)

    if ok == 0:
        print("ERRORE: nessuna carta ECMWF scaricata.", file=sys.stderr)
        return 1

    # Riscrivi i metadati solo se qualcosa è cambiato, se il file manca, o se la
    # configurazione delle carte è diversa. Così il timestamp `aggiornato` (e il
    # deploy a valle) scattano solo quando ECMWF pubblica una corsa nuova.
    esistente = None
    if os.path.exists(OUT_JSON):
        try:
            esistente = json.load(open(OUT_JSON, encoding="utf-8"))
        except Exception:  # noqa: BLE001
            esistente = None

    nuovo_corpo = {"carte": carte, "corsa": corsa}
    vecchio_corpo = None
    if esistente is not None:
        vecchio_corpo = {"carte": esistente.get("carte"), "corsa": esistente.get("corsa")}
    config_diversa = (esistente is None) or (vecchio_corpo != nuovo_corpo)

    if cambiate or config_diversa:
        aggiornato = stamp if (cambiate or esistente is None) else esistente.get("aggiornato", stamp)
        meta_out = {
            "aggiornato": aggiornato,
            "corsa": corsa,
            "passo_giorni": GIORNI_AVANTI,
            "fonte": "ECMWF OpenCharts",
            "licenza": "CC BY 4.0",
            "attribuzione": ("based on data and products of the European Centre "
                             "for Medium-Range Weather Forecasts (ECMWF)"),
            "carte": carte,
        }
        if not dry_run:
            os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
            json.dump(meta_out, open(OUT_JSON, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=2)
        print("[meta] scritto ({}/{} carte aggiornate, corsa: {})".format(
            cambiate, ok, corsa or "?"))
    else:
        print("[meta] nessun cambiamento ({} carte invariate) — niente commit".format(ok))

    if errori:
        print("Avvisi: {} prodotti non scaricati: {}".format(len(errori), "; ".join(errori)),
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
