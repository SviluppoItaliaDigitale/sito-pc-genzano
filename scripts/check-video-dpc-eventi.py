#!/usr/bin/env python3
"""
check-video-dpc-eventi.py — Verifica periodica di video DPC potenzialmente
integrabili in articoli/pagine del sito.

Logica:
  1. Scarica le playlist tematiche del canale DPCgov (PCM) — scrape HTML.
  2. Scarica i 15 video più recenti del feed canale (eventuali nuove uscite).
  3. Estrae keywords significative da titoli (escludendo stop-words italiani
     e date 4-cifre tipo "2024").
  4. Scansiona content/**/*.md del sito ed estrae keywords da frontmatter
     (title + description) + primo H2 del corpo.
  5. Calcola overlap: ogni elemento DPC riceve un punteggio sui contenuti
     del sito che condividono ≥2 keywords significative.
  6. Stampa report ordinato per forza del match; in CI produce body issue
     con suggerimenti di abbinamento (la decisione di integrare resta umana).

Si esclude qualsiasi LIS: quelli sono già coperti da check-nuovi-video-lis.py.

Uso locale: python3 scripts/check-video-dpc-eventi.py
Uso CI: invocato da .github/workflows/check-video-dpc-eventi.yml.
"""

import os
import re
import sys
import json
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path
from collections import defaultdict

CHANNEL_DPC = "UC4fru33Tzpu0UhCIHChiNFA"  # Dipartimento Protezione Civile (PCM)

HEADERS = {
    "Cookie": "CONSENT=YES+cb.20210328-17-p0.it+FX+000",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "it-IT,it;q=0.9",
}
NS = {
    "a": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
}

# Stop-words italiane (articoli, preposizioni, congiunzioni, parole di servizio)
STOPWORDS_IT = set("""
a ad ai al alla alle allo anche b c che chi ci con d da dai dal dalla dalle dei del
della delle dello di dove e ed essere fa fra gli ha hai hanno ho i il in la le lo
ma mi nei nel nella nelle nello noi non o per più poi qua qual quale quali
quando quanta quante quanti quanto quel quella quelle quelli quello questa queste
questi questo se senza si siamo sia sono su sua sue sugli sui sul sull sulla sulle
sullo suo suoi sta stati stato te ti tra tu tua tue tuoi tuoi tutta tutte tutti
tutto un una uno vi via voi ho s te tu un ti se mi io io noi voi le la lo loro
chi cui ma se anche già più ancora come così solo tutto tutte ogni dove quando
2018 2019 2020 2021 2022 2023 2024 2025 2026 2027 ed video del giornata convegno
edizione progetto presentazione conferenza diretta speciale incontra incontro racconta
salone internazionale libro turino punto attività attivita prima dopo durante intervento
incontri ascolta tappa stati generali confronto temi tema tavolo dal nazionale nazionali
italia italiana italiano dipartimento protezione civile pc dpc ditta srl ente
""".split())

# Le pagine del sito che vogliamo cross-referenziare. Tutto sotto content/.
# Si esclude content/comunicazioni/ — sono troppi articoli e troppo episodici
# (l'utente probabilmente vuole match con pagine tematiche stabili). Cambia
# CONTENT_SUBDIRS se vuoi includere anche le comunicazioni.
CONTENT_SUBDIRS = [
    "rischi-prevenzione",
    "formazione",
    "diventa-volontario",
    "chi-siamo",
    "piano-emergenza",
    "piano-familiare",
    "allerte-meteo",
    "cartografia",
    "numeri-utili",
    "lis",
    "abili-a-proteggere",
    "faq",
    "glossario",
    "storia",
    "trasparenza",
    "standard-iso",
]


def fetch(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_dpc_playlists() -> list[dict]:
    """Scrape /@DPCgov/playlists → list of {title, playlistId}."""
    try:
        html = fetch("https://www.youtube.com/@DPCgov/playlists").decode("utf-8", errors="replace")
    except Exception as e:
        print(f"  Errore scrape playlist DPC: {e}", file=sys.stderr)
        return []
    pids = sorted(set(re.findall(r'"playlistId":"(PLaLgDI0rVT4[A-Za-z0-9_-]+)"', html)))
    out = []
    for pid in pids:
        try:
            xml_bytes = fetch(f"https://www.youtube.com/feeds/videos.xml?playlist_id={pid}", timeout=8)
            root = ET.fromstring(xml_bytes)
            title_el = root.find("a:title", NS)
            title = title_el.text if title_el is not None else f"Playlist {pid}"
            out.append({"kind": "playlist", "title": title, "id": pid,
                        "url": f"https://www.youtube.com/playlist?list={pid}"})
        except Exception:
            continue
    return out


def fetch_dpc_recent_videos() -> list[dict]:
    """Feed RSS del canale DPC: 15 video più recenti."""
    try:
        xml_bytes = fetch(f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_DPC}")
        root = ET.fromstring(xml_bytes)
    except Exception as e:
        print(f"  Errore feed canale DPC: {e}", file=sys.stderr)
        return []
    out = []
    for e in root.findall("a:entry", NS):
        t = e.find("a:title", NS)
        v = e.find("yt:videoId", NS)
        p = e.find("a:published", NS)
        if t is not None and v is not None:
            out.append({
                "kind": "video",
                "title": t.text or "",
                "id": v.text,
                "url": f"https://youtu.be/{v.text}",
                "published": (p.text or "")[:10] if p is not None else "",
            })
    return out


def tokenize(text: str) -> set[str]:
    """Tokenize: lowercase, alpha only, len >= 4, no stop-words."""
    text = text.lower()
    # Sostituisce caratteri non alphanumerici con spazi
    text = re.sub(r"[^a-zàèéìòùù\s]", " ", text)
    tokens = text.split()
    return {t for t in tokens if len(t) >= 4 and t not in STOPWORDS_IT}


def extract_text_for_keywords(path: Path) -> str:
    """Return a concatenation of title + description + all H2/H3 + first 3000
    chars of body — used to build keyword index for the file."""
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    m = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not m:
        return ""
    fm_text, body = m.group(1), m.group(2)
    parts = []
    for line in fm_text.splitlines():
        s = line.strip()
        if s.startswith("title:"):
            parts.append(s[6:].strip().strip('"\''))
        elif s.startswith("description:"):
            parts.append(s[12:].strip().strip('"\''))
    # All H2 / H3
    for h in re.findall(r"^##+\s+(.+)$", body, re.MULTILINE):
        parts.append(h.strip())
    # First 3000 chars of body (escluso frontmatter, escluso shortcode)
    body_clean = re.sub(r"\{\{<[^>]*>\}\}", " ", body)
    parts.append(body_clean[:3000])
    return " ".join(parts)


def extract_title(path: Path) -> str:
    """Quick title extraction for display."""
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not m:
        return ""
    for line in m.group(1).splitlines():
        s = line.strip()
        if s.startswith("title:"):
            return s[6:].strip().strip('"\'')
    return ""


def scan_site_content(repo_root: Path) -> list[dict]:
    """Scan content subdirs (incluso comunicazioni). Return list of
    {path, title, url, keywords}."""
    out = []
    content_root = repo_root / "content"
    for sub in CONTENT_SUBDIRS:
        d = content_root / sub
        if not d.exists():
            continue
        for md in d.rglob("*.md"):
            title = extract_title(md)
            text = extract_text_for_keywords(md)
            kw = tokenize(text)
            if len(kw) < 3:
                continue
            rel = md.relative_to(content_root)
            url_path = str(rel).replace("_index.md", "").rstrip(".md")
            if url_path.endswith(".md"):
                url_path = url_path[:-3]
            url = "/" + url_path.rstrip("/") + "/"
            out.append({
                "path": str(rel),
                "title": title,
                "url": url,
                "keywords": kw,
            })
    return out


def build_idf(site_index: list[dict]) -> dict[str, float]:
    """Calcola la document frequency di ciascuna keyword. Le keyword
    che appaiono in molti file (>30%) sono considerate troppo generiche
    e penalizzate (peso 0.3); le altre hanno peso 1.0."""
    n = len(site_index)
    df = defaultdict(int)
    for s in site_index:
        for k in s["keywords"]:
            df[k] += 1
    weights = {}
    threshold_generic = max(2, int(0.20 * n))   # parole in >20% file = generiche
    threshold_common  = max(2, int(0.10 * n))   # parole in >10% file = comuni
    for k, count in df.items():
        if count > threshold_generic:
            weights[k] = 0.2
        elif count > threshold_common:
            weights[k] = 0.6
        else:
            weights[k] = 1.0
    return weights


def find_matches(dpc_items: list[dict], site_index: list[dict],
                 min_score: float = 2.0) -> list[dict]:
    """Cross-match: punteggio = somma dei pesi IDF delle keyword in comune.
    Una keyword 'specifica' vale 1.0; una 'generica' (presente in >30% delle
    pagine del sito) vale 0.3. Match validi: punteggio >= min_score."""
    weights = build_idf(site_index)
    results = []
    for item in dpc_items:
        ikw = tokenize(item["title"])
        if not ikw:
            continue
        for site in site_index:
            overlap = ikw & site["keywords"]
            if not overlap:
                continue
            score = sum(weights.get(k, 1.0) for k in overlap)
            if score >= min_score:
                # Distingui keyword specifiche (peso 1.0) da generiche (0.3)
                specifiche = sorted(k for k in overlap if weights.get(k, 1.0) >= 1.0)
                generiche = sorted(k for k in overlap if weights.get(k, 1.0) < 1.0)
                results.append({
                    "dpc_kind": item["kind"],
                    "dpc_title": item["title"],
                    "dpc_url": item["url"],
                    "site_title": site["title"],
                    "site_url": site["url"],
                    "site_path": site["path"],
                    "specifiche": specifiche,
                    "generiche": generiche,
                    "score": round(score, 2),
                })
    results.sort(key=lambda x: (-x["score"], x["site_url"], x["dpc_title"]))
    return results


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent

    print("Scarico playlist canale DPCgov…", file=sys.stderr)
    playlists = fetch_dpc_playlists()
    print(f"  trovate {len(playlists)} playlist", file=sys.stderr)

    print("Scarico video recenti canale DPCgov…", file=sys.stderr)
    videos = fetch_dpc_recent_videos()
    print(f"  trovati {len(videos)} video", file=sys.stderr)

    dpc_items = playlists + videos

    print("Scansiono content del sito…", file=sys.stderr)
    site_index = scan_site_content(repo_root)
    print(f"  trovati {len(site_index)} file Markdown analizzati", file=sys.stderr)

    matches = find_matches(dpc_items, site_index, min_score=1.8)

    print(f"\nMatch trovati (score >= 1.8): {len(matches)}", file=sys.stderr)

    if not matches:
        print("OK_NO_MATCHES")
        print("Nessun video o playlist DPC ha overlap significativo con i contenuti del sito.")
        return 0

    print("MATCHES_FOUND")
    print(f"Suggerimenti di integrazione video DPC → contenuti del sito: {len(matches)}")
    print()

    # Group by dpc item to avoid noise
    by_dpc = defaultdict(list)
    for m in matches:
        by_dpc[(m["dpc_title"], m["dpc_url"], m["dpc_kind"])].append(m)

    for (title, url, kind), mlist in by_dpc.items():
        emoji = "📺" if kind == "playlist" else "🎬"
        print(f"### {emoji} {title}")
        print(f"- URL: {url}")
        print(f"- Tipo: {kind}")
        print(f"- Possibili abbinamenti sul sito:")
        for m in mlist[:5]:  # top 5 per item
            kw_parts = []
            if m["specifiche"]:
                kw_parts.append("specifiche: " + ", ".join(f"`{k}`" for k in m["specifiche"]))
            if m["generiche"]:
                kw_parts.append("generiche: " + ", ".join(f"`{k}`" for k in m["generiche"]))
            kw_str = " · ".join(kw_parts)
            print(f"  - **[{m['site_title']}]({m['site_url']})** "
                  f"(`{m['site_path']}`) — {kw_str} (score: {m['score']})")
        if len(mlist) > 5:
            print(f"  - …e altri {len(mlist) - 5} match minori")
        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
