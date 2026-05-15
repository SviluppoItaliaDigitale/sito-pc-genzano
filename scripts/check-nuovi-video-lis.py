#!/usr/bin/env python3
"""
check-nuovi-video-lis.py — Verifica periodica nuovi video LIS sui canali
istituzionali monitorati:
  - "Io non rischio" (DPC + ANPAS + INGV + RELUIS + CIMA) — campagna nazionale
  - "Dipartimento della Protezione Civile (DPCgov)" — canale ufficiale PCM
  - "Abili a Proteggere" (Cooperativa Sociale Europe Consulting)

Logica:
  1. Carica data/lis.yaml e estrae i youtube_url già integrati nel sito.
  2. Fetcha:
     - Feed RSS del canale Io non rischio (15 video più recenti)
     - Feed RSS della playlist LIS DPC (12 storici)
     - Feed RSS della playlist L'attimo decisivo (lezioni)
     - Feed RSS del canale DPCgov (15 video più recenti, filtra LIS)
     - HTML scrape del canale Abili a Proteggere (tutto, ~30 video)
  3. Filtra solo i video LIS plausibili (heuristica: titolo contiene "LIS",
     "Glossario", "lingua dei segni", oppure è nella playlist LIS dichiarata).
  4. Calcola differenza: video_id YouTube nuovi non in data/lis.yaml.
  5. Stampa report; se eseguito da GitHub Actions, output formattato per
     creazione issue automatica.

Uso locale: python3 scripts/check-nuovi-video-lis.py
Uso CI: invocato da .github/workflows/check-video-lis.yml ogni lunedì.
"""

import os
import re
import sys
import yaml
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

# Canali e playlist da monitorare
CHANNEL_INR = "UCdOg4quMoJDjQIkopcXkqCQ"       # Io non rischio (DPC + ANPAS + INGV + RELUIS + CIMA)
CHANNEL_DPCGOV = "UC4fru33Tzpu0UhCIHChiNFA"    # Dipartimento Protezione Civile (PCM) — canale ufficiale
CHANNEL_AAP = "UCjsiExhgS_2oL5dMwUsgd0Q"       # Abili a Proteggere (Europe Consulting)
PLAYLIST_LIS_DPC = "PLyRppYk2-sTIDs7RX-2C0pB1ZmgtA0yMo"     # Materiali LIS ufficiali
PLAYLIST_ATTIMO = "PLyRppYk2-sTKsMmo7PNnOabYpz2paC77V"      # Videolezioni L'attimo decisivo

# Header HTTP per bypassare il consent banner YouTube
HEADERS = {
    "Cookie": "CONSENT=YES+cb.20210328-17-p0.it+FX+000; SOCS=CAISEwgDEgk0NzU4NjE0MDgaAml0IAEaBgiArJW5Bg",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
}

NS = {
    "a": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


def fetch(url: str, timeout: int = 15) -> bytes:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def parse_feed(xml_bytes: bytes) -> list[dict]:
    """Parse YouTube Atom RSS feed; return list of {videoId, title, published}."""
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return []
    out = []
    for e in root.findall("a:entry", NS):
        title_el = e.find("a:title", NS)
        vid_el = e.find("yt:videoId", NS)
        pub_el = e.find("a:published", NS)
        if vid_el is None or title_el is None:
            continue
        out.append({
            "videoId": vid_el.text,
            "title": title_el.text or "",
            "published": (pub_el.text or "")[:10] if pub_el is not None else "",
            "source": "feed",
        })
    return out


def scrape_channel_videos(channel_handle_url: str) -> list[dict]:
    """Scrape /videos page of a YouTube channel; return list of {videoId, title}."""
    try:
        html = fetch(channel_handle_url).decode("utf-8", errors="replace")
    except urllib.error.URLError:
        return []
    # Find all videoIds; pair each unique with the nearest 'Glossario in LIS:' title
    vids_pos = [(m.group(1), m.start()) for m in re.finditer(r'"videoId":"([A-Za-z0-9_-]{11})"', html)]
    titles_pos = [(m.group(1).strip('"').strip(), m.start())
                  for m in re.finditer(r'(Glossario in LIS[^"]+|[Ii]o non rischio[^"]+)', html)]
    pairs = {}
    for title, tpos in titles_pos:
        if title in pairs:
            continue
        prev = [v for v, p in vids_pos if p < tpos]
        if prev:
            pairs[title.strip()] = prev[-1]
    return [{"videoId": v, "title": t, "published": "", "source": "scrape"}
            for t, v in pairs.items()]


def extract_existing_video_ids(lis_yaml_path: str) -> set[str]:
    """Estrae i 11-char videoId YouTube già presenti in data/lis.yaml."""
    with open(lis_yaml_path) as f:
        data = yaml.safe_load(f)
    ids = set()
    for v in (data.get("video") or {}).values():
        url = (v.get("youtube_url") or "").strip()
        m = re.search(r"youtu\.be/([A-Za-z0-9_-]{11})|youtube\.com/watch\?v=([A-Za-z0-9_-]{11})", url)
        if m:
            ids.add(m.group(1) or m.group(2))
    return ids


def is_lis_plausible(title: str) -> bool:
    """Heuristic: does this title look like a LIS video?

    Usa word boundary su "LIS" per evitare falsi positivi (nomi come Elisa,
    Felisia, sigle come PLIS, BLIS che contengono "LIS" come sottostringa).
    """
    if re.search(r"\bLIS\b", title):
        return True
    t = title.lower()
    return any(k in t for k in ("lingua dei segni", "lingua italiana dei segni",
                                 "in segni", "glossario in lis"))


def main() -> int:
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lis_yaml = os.path.join(repo_root, "data", "lis.yaml")

    existing = extract_existing_video_ids(lis_yaml)
    print(f"Video LIS già integrati nel sito: {len(existing)}", file=sys.stderr)

    candidates: list[dict] = []

    # 1) Feed playlist LIS ufficiale DPC (tutti i video sono LIS per definizione)
    try:
        feed = parse_feed(fetch(f"https://www.youtube.com/feeds/videos.xml?playlist_id={PLAYLIST_LIS_DPC}"))
        for v in feed:
            v["channel"] = "io-non-rischio (playlist LIS ufficiale)"
            v["is_lis"] = True
            candidates.append(v)
        print(f"  Playlist LIS DPC: {len(feed)} video", file=sys.stderr)
    except Exception as e:
        print(f"  Errore playlist LIS DPC: {e}", file=sys.stderr)

    # 2) Feed playlist L'attimo decisivo (lezioni con LIS in sovrimpressione)
    try:
        feed = parse_feed(fetch(f"https://www.youtube.com/feeds/videos.xml?playlist_id={PLAYLIST_ATTIMO}"))
        for v in feed:
            v["channel"] = "io-non-rischio (playlist L'attimo decisivo)"
            v["is_lis"] = True  # confermato dall'utente: tutti hanno interprete LIS in sovrimpressione
            candidates.append(v)
        print(f"  Playlist L'attimo decisivo: {len(feed)} video", file=sys.stderr)
    except Exception as e:
        print(f"  Errore playlist L'attimo decisivo: {e}", file=sys.stderr)

    # 3) Feed canale Io non rischio (filtra per LIS nel titolo: Stromboli LIS ecc.)
    try:
        feed = parse_feed(fetch(f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_INR}"))
        for v in feed:
            v["channel"] = "io-non-rischio (canale)"
            v["is_lis"] = is_lis_plausible(v["title"])
            candidates.append(v)
        print(f"  Canale Io non rischio: {len(feed)} video (di cui LIS plausibili: {sum(1 for v in feed if is_lis_plausible(v['title']))})", file=sys.stderr)
    except Exception as e:
        print(f"  Errore canale Io non rischio: {e}", file=sys.stderr)

    # 4) Feed canale DPCgov (ufficiale PCM) — filtra per LIS nel titolo.
    # Il canale non ha playlist LIS dedicata, ma occasionalmente pubblica
    # video con interprete LIS (eventi istituzionali, conferenze stampa).
    try:
        feed = parse_feed(fetch(f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_DPCGOV}"))
        for v in feed:
            v["channel"] = "dpcgov (canale ufficiale DPC-PCM)"
            v["is_lis"] = is_lis_plausible(v["title"])
            candidates.append(v)
        print(f"  Canale DPCgov: {len(feed)} video (di cui LIS plausibili: {sum(1 for v in feed if is_lis_plausible(v['title']))})", file=sys.stderr)
    except Exception as e:
        print(f"  Errore canale DPCgov: {e}", file=sys.stderr)

    # 5) Canale Abili a Proteggere (HTML scrape) — tutti i Glossario in LIS
    try:
        scraped = scrape_channel_videos("https://www.youtube.com/@abiliaproteggere4520/videos")
        for v in scraped:
            v["channel"] = "abili-a-proteggere"
            v["is_lis"] = is_lis_plausible(v["title"])
        candidates.extend(scraped)
        print(f"  Canale Abili a Proteggere: {len(scraped)} video", file=sys.stderr)
    except Exception as e:
        print(f"  Errore canale Abili a Proteggere: {e}", file=sys.stderr)

    # Dedup per videoId (alcuni video appaiono in più feed)
    seen_ids = set()
    unique = []
    for c in candidates:
        if c["videoId"] in seen_ids:
            continue
        seen_ids.add(c["videoId"])
        unique.append(c)

    # Filtra: solo LIS plausibili, e non già nel sito
    nuovi_lis = [c for c in unique if c.get("is_lis") and c["videoId"] not in existing]

    print(f"\nCandidati LIS totali scoperti: {sum(1 for c in unique if c.get('is_lis'))}", file=sys.stderr)
    print(f"Nuovi da integrare (non in data/lis.yaml): {len(nuovi_lis)}", file=sys.stderr)

    # Output stdout: report leggibile + JSON-ish per CI
    if not nuovi_lis:
        print("OK_NO_NEW_VIDEOS")
        print("Nessun nuovo video LIS rilevato dai canali monitorati.")
        return 0

    print("NEW_VIDEOS_FOUND")
    print(f"Nuovi video LIS rilevati: {len(nuovi_lis)}")
    print()
    for v in sorted(nuovi_lis, key=lambda x: (x.get("channel", ""), x.get("published", ""))):
        ch = v.get("channel", "?")
        pub = v.get("published", "")
        print(f"- **{v['title']}**")
        print(f"  - Canale: {ch}")
        if pub:
            print(f"  - Pubblicato: {pub}")
        print(f"  - URL: https://youtu.be/{v['videoId']}")
        # Suggerimento famiglia tematica basato sul titolo
        suggested = suggest_family(v["title"])
        if suggested:
            print(f"  - Famiglia suggerita: `{suggested}`")
        print()

    return 0


def suggest_family(title: str) -> str:
    """Heuristic mapping: title → famiglia tematica in data/lis.yaml."""
    t = title.lower()
    mapping = [
        ("terremoto", "rischio-sismico"),
        ("sismic", "rischio-sismico"),
        ("epicentr", "rischio-sismico"),
        ("magnitud", "rischio-sismico"),
        ("vulcan", "rischio-vulcanico"),
        ("eruzion", "rischio-vulcanico"),
        ("bradisism", "rischio-vulcanico"),
        ("fumarol", "rischio-vulcanico"),
        ("stromboli", "rischio-vulcanico"),
        ("campi flegrei", "rischio-vulcanico"),
        ("alluvion", "rischio-idrogeologico"),
        ("idrogeolog", "rischio-idrogeologico"),
        ("inondazion", "rischio-idrogeologico"),
        ("frana", "rischio-idrogeologico"),
        ("incendi", "rischio-incendio"),
        ("boschiv", "rischio-incendio"),
        ("aib", "rischio-incendio"),
        ("maremoto", "maremoto"),
        ("tsunami", "maremoto"),
        ("allerta", "allerte-meteo"),
        ("bollettino", "allerte-meteo"),
        ("centro funzional", "allerte-meteo"),
        ("centro operativo", "gestione-emergenza"),
        ("comitato operativ", "gestione-emergenza"),
        ("sala operativ", "gestione-emergenza"),
        ("sala situazion", "gestione-emergenza"),
        ("dicomac", "gestione-emergenza"),
        ("strutture operativ", "gestione-emergenza"),
        ("funzioni di supporto", "gestione-emergenza"),
        ("pianificaz", "pianificazione"),
        ("esercitaz", "pianificazione"),
        ("colonna mobile", "pianificazione"),
        ("aree di", "aree-emergenza"),
        ("aree d", "aree-emergenza"),
        ("kit", "kit-emergenza"),
    ]
    for k, fam in mapping:
        if k in t:
            return fam
    return ""


if __name__ == "__main__":
    sys.exit(main())
