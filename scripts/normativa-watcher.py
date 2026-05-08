#!/usr/bin/env python3
"""
normativa-watcher.py — sweep settimanale delle novità normative PC

Aggrega feed RSS istituzionali + Google News RSS filtrati per parole chiave
di Protezione Civile. Output: JSON con la lista delle novità degli ultimi 7
giorni, deduplicate per URL.

Fonti:
- Google News RSS — query mirate (canale primario, sempre disponibile)
- Feed RSS istituzionali noti (canale secondario, where existing)

Uso:
    python3 scripts/normativa-watcher.py [--days 7] [--out novita.json]

Dipendenze: feedparser, requests (entrambe stdlib-light).

Esce con codice 0 se OK (anche se zero hit), 1 su errore tecnico.
"""
import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from urllib.parse import quote_plus

try:
    import feedparser
except ImportError:
    print("ERROR: feedparser non installato. pip install feedparser", file=sys.stderr)
    sys.exit(1)


GOOGLE_NEWS_BASE = "https://news.google.com/rss/search?q={q}&hl=it&gl=IT&ceid=IT:it"

QUERIES_GOOGLE_NEWS = [
    # Query tematiche generali (canale primario)
    'protezione civile Lazio',
    'allerta meteo Lazio',
    'DPC ordinanza dipartimento protezione civile',
    'BURL Lazio protezione civile',
    'Regione Lazio decreto protezione civile',
    'Genzano di Roma protezione civile',
    'Castelli Romani allerta',
    'incendio boschivo Lazio',
    'rischio idrogeologico Castelli Romani',
    'IT-alert protezione civile',
    'volontariato protezione civile Lazio',
    'esercitazione protezione civile Lazio',

    # Query site: ad ALTO valore (tutto rilevante per PC)
    'site:normattiva.it protezione civile',
    'site:gazzettaufficiale.it protezione civile',
    'site:regione.lazio.it protezione civile',
    'site:consiglio.regione.lazio.it protezione civile',
    'site:protezionecivile.gov.it',
    'site:vigilfuoco.it Lazio OR Castelli OR Genzano',
    'site:arpalazio.it',
    'site:arsial.it incendio OR allerta',
    'site:irpi.cnr.it',
    'site:cmcc.it adattamento OR clima OR Italia',
    'site:isprambiente.gov.it rischio OR allerta',
    'site:iss.it ondata OR emergenza OR pandemia',
    'site:camera.it protezione civile',

    # Query site: a MEDIO valore (specifico PC)
    'site:corteconti.it protezione civile',
    'site:cortecostituzionale.it protezione civile',
    'site:governo.it protezione civile OR consiglio dei ministri PC',
    'site:mit.gov.it sicurezza OR rischio',
    'site:cultura.gov.it patrimonio emergenza',
    'site:interno.gov.it prefettura OR emergenza',
    'site:istat.it popolazione vulnerabile OR rischio',
    'site:carabinieri.it forestali OR incendio',
    'site:anpas.org',
    'site:cri.it Lazio OR Castelli',
    'site:salute.gov.it caldo OR ondata OR emergenza',
    'site:opencoesione.gov.it protezione civile',
]

FEEDS_ISTITUZIONALI = [
    {"nome": "TGR Lazio (RAI)", "url": "https://www.rainews.it/tgr/lazio/archivio.rss"},
]

KEYWORDS_FILTRO = [
    'protezione civile', 'pcgenzano', 'genzano',
    'allerta', 'allertamento', 'emergenza', 'criticità',
    'idrogeologico', 'idraulico', 'frana', 'frane', 'alluvione',
    'sisma', 'sismic', 'terremoto', 'scossa',
    'incendio', 'aib ', 'boschivo', 'boschivi',
    'temporal', 'vento forte', 'neve',
    'ondata di calore', 'caldo estremo',
    'blackout', 'interruzione',
    'evacuazione', 'soccorso',
    'volontariato', 'odv ', 'volontari',
    'it-alert', 'itl-alert',
    'dpc', 'dipartimento protezione civile',
    'castelli romani',
]


def normalizza(s: str) -> str:
    return (s or '').lower().strip()


def filtro_keyword(testo: str) -> bool:
    t = normalizza(testo)
    return any(kw in t for kw in KEYWORDS_FILTRO)


def parse_feed(url: str, fonte: str, days: int) -> list:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    out = []
    try:
        feed = feedparser.parse(url)
        if feed.bozo and not feed.entries:
            print(f"  [warn] feed non parsabile: {fonte} ({url})", file=sys.stderr)
            return out
        for entry in feed.entries[:50]:
            titolo = entry.get('title', '').strip()
            link = entry.get('link', '').strip()
            sommario = entry.get('summary', '').strip()
            published_parsed = entry.get('published_parsed') or entry.get('updated_parsed')
            if published_parsed:
                published = datetime(*published_parsed[:6], tzinfo=timezone.utc)
                if published < cutoff:
                    continue
                published_iso = published.isoformat()
            else:
                published_iso = None
            testo_completo = f"{titolo} {sommario}"
            if not filtro_keyword(testo_completo):
                continue
            out.append({
                "fonte": fonte,
                "titolo": titolo,
                "link": link,
                "published": published_iso,
                "sommario": sommario[:300],
            })
    except Exception as e:
        print(f"  [error] {fonte}: {e}", file=sys.stderr)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--days', type=int, default=7, help='Finestra temporale in giorni (default 7)')
    ap.add_argument('--out', default='-', help='File output JSON (default stdout)')
    args = ap.parse_args()

    print(f"[info] Sweep ultimi {args.days} giorni — {len(QUERIES_GOOGLE_NEWS)} query Google News + {len(FEEDS_ISTITUZIONALI)} feed istituzionali", file=sys.stderr)

    hits = []
    seen_links = set()

    for query in QUERIES_GOOGLE_NEWS:
        url = GOOGLE_NEWS_BASE.format(q=quote_plus(query))
        fonte = f"Google News: {query}"
        results = parse_feed(url, fonte, args.days)
        for r in results:
            if r['link'] in seen_links:
                continue
            seen_links.add(r['link'])
            hits.append(r)
        print(f"  [{len(results):3d}] {query}", file=sys.stderr)

    for f in FEEDS_ISTITUZIONALI:
        results = parse_feed(f['url'], f['nome'], args.days)
        for r in results:
            if r['link'] in seen_links:
                continue
            seen_links.add(r['link'])
            hits.append(r)
        print(f"  [{len(results):3d}] {f['nome']}", file=sys.stderr)

    hits.sort(key=lambda x: x.get('published') or '', reverse=True)

    print(f"[info] Totale: {len(hits)} novità uniche dopo dedup", file=sys.stderr)

    output = {
        "generato_il": datetime.now(timezone.utc).isoformat(),
        "finestra_giorni": args.days,
        "totale": len(hits),
        "novita": hits,
    }

    if args.out == '-':
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        with open(args.out, 'w', encoding='utf-8') as fh:
            json.dump(output, fh, ensure_ascii=False, indent=2)
        print(f"[info] Output scritto in {args.out}", file=sys.stderr)


if __name__ == '__main__':
    main()
