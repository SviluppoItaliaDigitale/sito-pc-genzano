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

Attribuzione obbligatoria CC BY 4.0: ogni carta è mostrata con il credito
"Fonte: ECMWF — based on data and products of the European Centre for Medium-Range
Weather Forecasts (ECMWF), CC BY 4.0".

API: GET https://charts.ecmwf.int/opencharts-api/v1/products/<slug>/[?projection=...]
     → JSON con data["data"]["link"]["href"] = URL del PNG renderizzato.

Output:
  - static/images/ecmwf/<slug>.webp   una carta per prodotto (ultima corsa disponibile)
  - data/ecmwf_charts.json            metadati (titolo, orari, aggiornamento, cache-bust)

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
import ssl
import sys
import datetime
import urllib.request
import urllib.error

from PIL import Image

API_BASE = "https://charts.ecmwf.int/opencharts-api/v1/products/"
# Proiezione europea del catalogo OpenCharts (centra la carta su Europa/Mediterraneo).
PROJECTION = "opencharts_europe"

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


def _get(url, accept="application/json"):
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": accept,
    })
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=_CTX) as r:
        return r.read()


def risolvi_immagine(slug):
    """Interroga l'OpenCharts API e restituisce (href_png, meta) o (None, errore)."""
    candidati = [
        "{}{}/?projection={}".format(API_BASE, slug, PROJECTION),
        "{}{}/".format(API_BASE, slug),
    ]
    ultimo_err = None
    for url in candidati:
        try:
            raw = _get(url)
            doc = json.loads(raw.decode("utf-8"))
            data = doc.get("data") or {}
            link = data.get("link") or {}
            href = link.get("href")
            if href:
                meta = {
                    "titolo_api": data.get("title") or "",
                    "copyright": (doc.get("attributes") or {}).get("copyright")
                                 or data.get("copyright") or "",
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
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=2)))  # Europe/Rome (CEST)
    stamp = now.strftime("%Y-%m-%dT%H:%M")

    carte = []
    ok = 0
    cambiate = 0
    errori = []

    for p in PRODOTTI:
        slug = p["slug"]
        href, meta = risolvi_immagine(slug)
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
            carte.append({
                "slug": slug,
                "titolo": p["titolo"],
                "descr": p["descr"],
                "icona": p["icona"],
                "file": "/images/ecmwf/{}.webp".format(slug),
                "titolo_api": meta.get("titolo_api", ""),
            })
            etich = "AGGIORNATA" if scritto else "invariata"
            print("[ok ] {} {} {}".format(slug, etich, "(dry-run)" if dry_run else ""))
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

    config_diversa = (esistente is None) or (esistente.get("carte") != carte)
    if cambiate or config_diversa:
        aggiornato = stamp if (cambiate or esistente is None) else esistente.get("aggiornato", stamp)
        meta_out = {
            "aggiornato": aggiornato,
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
        print("[meta] scritto ({}/{} carte aggiornate)".format(cambiate, ok))
    else:
        print("[meta] nessun cambiamento ({} carte invariate) — niente commit".format(ok))

    if errori:
        print("Avvisi: {} prodotti non scaricati: {}".format(len(errori), "; ".join(errori)),
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
