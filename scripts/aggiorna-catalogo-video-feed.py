#!/usr/bin/env python3
"""Aggiorna il catalogo video con i video RECENTI dei canali monitorati,
letti dai feed RSS/Atom ufficiali di YouTube (ultimi ~15 video per canale).

Perché esiste (02/09/2026): il catalogo completo (scripts/scrape-catalogo-video.py,
yt-dlp) viene rifatto solo il 1° del mese. Un video pubblicato il giorno dopo
la scansione restava invisibile al cross-match per quasi un mese — è successo
con il video Geopop sul crollo del ghiacciaio in Nepal (uscito il 01/09/2026
poche ore dopo la scansione, mentre l'articolo era del 27/08). Questo script
gira ogni settimana (workflow aggiorna-video-feed.yml) e aggiunge al catalogo
solo i video nuovi; la scansione mensile resta la fonte completa e riallinea
tutto (stesso formato delle voci, stesse chiavi "<canale>-<id>").

Nessuna dipendenza oltre a PyYAML: i feed sono XML pubblici, senza API key
né yt-dlp. Fail-safe: un canale che non risponde viene saltato, lo script
esce sempre 0 e non tocca il file se non c'è nulla da aggiungere.

Uso:
    python3 scripts/aggiorna-catalogo-video-feed.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

# ID canale YouTube (UC…) per ogni chiave di CANALI in scrape-catalogo-video.py.
# Risolti il 02/09/2026 dal campo "externalId" della pagina del canale.
# Se un canale nuovo viene aggiunto a CANALI senza ID qui, lo script lo
# risolve al volo dalla pagina dell'handle (fallback) e lo segnala nel log:
# aggiungerlo qui per non dipendere dal parsing HTML di YouTube.
CHANNEL_IDS = {
    "io-non-rischio": "UCdOg4quMoJDjQIkopcXkqCQ",
    "dpc-gov": "UC4fru33Tzpu0UhCIHChiNFA",
    "abili-a-proteggere": "UCjsiExhgS_2oL5dMwUsgd0Q",
    "ingv-terremoti": "UCWcylY2YDfioFmDAULj3vgA",
    "ingv-vulcani": "UC3GnD1b5hO8a-ag0yKr_uqw",
    "italiameteo": "UCY2a2x_PLS6yLS-evf388Hw",
    "cima-foundation": "UCkhCF802IPdLpBAwxLrThlA",
    "cnsas": "UCQ6mw4hI7xIk592QuX1xa_A",
    "solarino-sismologo": "UCLVbUqNTO5VJ0BR4dCsAyuA",
    "geopop": "UCx7EWheHmjCW3vX8K2d09vg",
    "natgeo-italia": "UCvXSSoQm3NOwYlPYy8qdGnA",
    "rai-cultura": "UCDLYMJX6al0okaalt5yAEFA",
    "cicap": "UCgTILSw1wFmJ5JjRqAM-N_g",
    "link4universe": "UCHRTziAevLPgAE9Y5VhSs5g",
    "wired-italia": "UCEn99hD6NygfFa5W8MW0M0A",
    "rai-news": "UCxqR9g_1XlnfrqwHK9viwCw",
    "cmcc": "UCC9Z2ICMKAz6C0p2fbwN-3g",
    "dario-bressanini": "UCJphwa8Wsgzsm1zJS4sm-mA",
}

FEED_URL = "https://www.youtube.com/feeds/videos.xml?channel_id={cid}"
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/)"


def http_get(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "it"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def risolvi_channel_id(handle_url: str) -> str | None:
    """Fallback: legge l'ID canale dalla pagina dell'handle (campo externalId)."""
    try:
        html = http_get(handle_url.replace("/videos", "")).decode("utf-8", "ignore")
    except Exception:
        return None
    m = re.search(r'"externalId":"(UC[\w-]{22})"', html)
    return m.group(1) if m else None


def leggi_feed(cid: str) -> list[dict]:
    """Ritorna [{id, titolo, url}] dei video presenti nel feed del canale."""
    root = ET.fromstring(http_get(FEED_URL.format(cid=cid)))
    out = []
    for e in root.findall("a:entry", NS):
        vid = e.findtext("yt:videoId", namespaces=NS)
        titolo = (e.findtext("a:title", namespaces=NS) or "").strip()
        if vid and titolo:
            out.append({"id": vid, "titolo": titolo, "url": f"https://youtu.be/{vid}"})
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--catalogo", default="data/video_dpc_catalogo.yaml")
    p.add_argument("--dry-run", action="store_true", help="Non scrivere il file")
    args = p.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    path = repo_root / args.catalogo
    raw = path.read_text(encoding="utf-8")
    header = raw[: raw.index("canali:")]
    catalogo = yaml.safe_load(raw)
    canali = catalogo["canali"]
    videos = catalogo["video"]
    noti = {v["id"] for v in videos.values()}

    aggiunti_tot = 0
    for chiave, meta in canali.items():
        cid = CHANNEL_IDS.get(chiave) or risolvi_channel_id(meta.get("url", ""))
        if not cid:
            print(f"  [salto] {chiave}: ID canale non risolto (aggiungerlo a CHANNEL_IDS)", file=sys.stderr)
            continue
        if chiave not in CHANNEL_IDS:
            print(f"  [nota] {chiave}: ID {cid} risolto al volo — aggiungerlo a CHANNEL_IDS", file=sys.stderr)
        try:
            recenti = leggi_feed(cid)
        except Exception as e:  # rete, XML, HTTP: il canale si salta, il resto prosegue
            print(f"  [salto] {chiave}: feed non leggibile ({e})", file=sys.stderr)
            continue
        nuovi = [v for v in recenti if v["id"] not in noti]
        for v in nuovi:
            videos[f"{chiave}-{v['id']}"] = {"canale": chiave, "id": v["id"], "titolo": v["titolo"], "url": v["url"]}
            noti.add(v["id"])
            print(f"  + {chiave}: {v['titolo'][:90]}", file=sys.stderr)
        if nuovi:
            meta["video_count"] = int(meta.get("video_count", 0)) + len(nuovi)
        aggiunti_tot += len(nuovi)

    print(f"\nVideo nuovi dal feed: {aggiunti_tot} (catalogo: {len(videos)} video)", file=sys.stderr)
    if not aggiunti_tot or args.dry_run:
        return 0

    header = re.sub(r"# Totale: \d+ video", f"# Totale: {len(videos)} video", header)
    with open(path, "w", encoding="utf-8") as f:
        f.write(header)
        yaml.safe_dump({"canali": canali, "video": videos}, f, allow_unicode=True, sort_keys=True, width=120)
    print(f"✓ Scritto {path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
