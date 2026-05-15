#!/usr/bin/env python3
"""
genera-video-correlati.py — Cross-match algoritmico fra il catalogo completo
dei video DPC/AaP (data/video_dpc_catalogo.yaml) e tutti i contenuti del
sito. Salva il risultato in data/video_correlati.yaml.

Per ogni pagina/articolo:
  - calcola le keyword significative (frontmatter + corpo)
  - cerca i video del catalogo che condividono >= N keyword pesate (IDF)
  - mantiene i top K video (default: 4) ordinati per score

Esclude i video che sono già presenti in data/lis.yaml (sono mostrati
tramite il badge LIS contestuale: evitiamo duplicazione visiva).

Il file generato è letto dal partial Hugo `video-correlati.html` che
renderizza in fondo agli articoli una sezione "Approfondimenti video"
con link esterni privacy-first (niente embed).

Uso: python3 scripts/genera-video-correlati.py [--max-per-page N] [--min-score F]
"""

import re
import sys
import yaml
import argparse
from pathlib import Path
from collections import defaultdict

STOPWORDS_IT = set("""
a ad ai al alla alle allo anche b c che chi ci con d da dai dal dalla dalle dei del
della delle dello di dove e ed essere fa fra gli ha hai hanno ho i il in la le lo
ma mi nei nel nella nelle nello noi non o per più poi qua qual quale quali
quando quanta quante quanti quanto quel quella quelle quelli quello questa queste
questi questo se senza si siamo sia sono su sua sue sugli sui sul sull sulla sulle
sullo suo suoi sta stati stato te ti tra tu tua tue tuoi tutta tutte tutti tutto
un una uno vi via voi cui ma anche già più ancora come così solo ogni quando
2018 2019 2020 2021 2022 2023 2024 2025 2026 2027 ed del giornata convegno
edizione progetto presentazione conferenza diretta speciale incontra incontro racconta
salone internazionale libro torino punto attività attivita prima dopo durante intervento
incontri ascolta tappa stati generali confronto temi tema tavolo nazionale nazionali
italia italiana italiano dipartimento protezione civile pc dpc ente glossario
serie episodi video cosa fare sapere come dove quando perché perche
spiega capire significato termine termini parola parole pagina pagine sito
nuovo nuova nuovi nuove sicurezza articolo articoli volontari volontariato
gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre
dicembre notte giorno giorni mese mesi anno anni mattina pomeriggio sera notte
ieri oggi domani lunedì martedì mercoledì giovedì venerdì sabato domenica
attivazione gestione presentazione interno esterno""".split())

# Pagine del sito da escludere dal cross-match (non avrebbe senso linkare
# video correlati a pagine legali, tecniche, di servizio).
SKIP_PAGE_PATTERNS = [
    r"^/?privacy/?$",
    r"^/?note-legali/?$",
    r"^/?accessibilita/?$",
    r"^/?social-media-policy/?$",
    r"^/?mappa-sito/?$",
    r"^/?attribuzioni-pittogrammi/?$",
    r"^/?cerca/?$",
    r"^/?stato-sistema/?$",
    r"^/?feed-rss/?$",
    r"^/?siti-utili/?$",
    r"^/?trasparenza/?$",
    r"^/?open-data/?$",
    r"^/?podcast/?",   # ha già contenuti audio
    r"^/?articoli-da-ascoltare/?$",
    r"^/?audio-e-podcast/?$",
    r"^/?lis/?$",       # è la pagina hub LIS, ha già tutto
    r"^/?assistente/?$",
    r"^/?english/", r"^/?francais/", r"^/?deutsch/", r"^/?espanol/",
    r"^/?portugues/", r"^/?romana/", r"^/?esperanto/",  # traduzioni
    r"^/?formazione/?$",  # hub formazione (ne ha già molti link nei kit)
]


def tokenize(text: str) -> set[str]:
    """Estrae keywords da text. Include:
       - parole lunghe ≥4 caratteri (es. "terremoto", "alluvione")
       - sigle maiuscole 3+ caratteri (es. "COC", "DPC", "ASL", "INGV")
       Esclude stop-words italiane."""
    # 1) Sigle maiuscole (preservate dal testo originale)
    sigle = {s.lower() for s in re.findall(r"\b[A-Z]{3,}\b", text)}
    # 2) Parole lowercase ≥4 char
    t = text.lower()
    t = re.sub(r"[^a-zàèéìòùù\s]", " ", t)
    parole = {w for w in t.split() if len(w) >= 4 and w not in STOPWORDS_IT}
    return parole | sigle


def extract_page_data(path: Path) -> dict:
    """Return {title, title_kw, desc_kw, body_kw} with separated keyword sets."""
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}
    m = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not m:
        return {}
    fm_text, body = m.group(1), m.group(2)
    title = ""
    desc = ""
    for line in fm_text.splitlines():
        s = line.strip()
        if s.startswith("title:") and not title:
            title = s[6:].strip().strip('"\'')
        elif s.startswith("description:"):
            desc = s[12:].strip().strip('"\'')
    headings = " ".join(re.findall(r"^##+\s+(.+)$", body, re.MULTILINE))
    body_clean = re.sub(r"\{\{<[^>]*>\}\}", " ", body)[:3000]
    return {
        "title": title,
        "title_kw": tokenize(title),
        "desc_kw": tokenize(desc) - tokenize(title),         # solo nuove rispetto al title
        "body_kw": tokenize(headings + " " + body_clean) - tokenize(title) - tokenize(desc),
    }


def build_url(content_root: Path, md_path: Path) -> str:
    rel = md_path.relative_to(content_root)
    s = str(rel)
    # Drop _index.md → directory URL
    if s.endswith("_index.md"):
        s = s[:-len("_index.md")]
    elif s.endswith(".md"):
        s = s[:-3] + "/"
    # Normalize
    return "/" + s.strip("/") + ("" if s == "" else "/")


def build_key(content_root: Path, md_path: Path) -> str:
    """Stable key per il lookup Hugo: path relativo a content/, senza
    estensione .md né suffisso /_index. Esempio:
       content/rischi-prevenzione/rischio-sismico.md
       → 'rischi-prevenzione/rischio-sismico'
       content/rischi-prevenzione/kit-emergenza/_index.md
       → 'rischi-prevenzione/kit-emergenza'"""
    rel = md_path.relative_to(content_root)
    s = str(rel)
    if s.endswith("/_index.md"):
        s = s[:-len("/_index.md")]
    elif s == "_index.md":
        s = ""
    elif s.endswith(".md"):
        s = s[:-3]
    return s


def page_excluded(url: str) -> bool:
    for pat in SKIP_PAGE_PATTERNS:
        if re.match(pat, url):
            return True
    return False


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--max-per-page", type=int, default=4,
                   help="Max video correlati per pagina (default: 4)")
    p.add_argument("--min-score", type=float, default=2.5,
                   help="Punteggio minimo per accettare un match (default: 2.5)")
    p.add_argument("--output", default="data/video_correlati.yaml")
    args = p.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    content_root = repo_root / "content"

    # Carica catalogo video
    with open(repo_root / "data" / "video_dpc_catalogo.yaml") as f:
        catalogo = yaml.safe_load(f)
    videos = catalogo["video"]
    print(f"Catalogo: {len(videos)} video totali", file=sys.stderr)

    # Carica registry LIS per marcare i video LIS nel risultato (NON per
    # escluderli: un video LIS pertinente al contesto specifico di un
    # articolo è prezioso anche se il badge LIS è già presente sulla
    # pagina madre del rischio. Cf. caso articolo "Centro Operativo
    # Comunale COC" — il video LIS specifico sul COC va integrato).
    with open(repo_root / "data" / "lis.yaml") as f:
        lis_data = yaml.safe_load(f)
    lis_video_ids = set()
    for v in (lis_data.get("video") or {}).values():
        url = v.get("youtube_url", "")
        m = re.search(r"youtu\.be/([A-Za-z0-9_-]{11})", url)
        if m:
            lis_video_ids.add(m.group(1))
    print(f"Video LIS marcati: {len(lis_video_ids)} (inclusi nel cross-match)", file=sys.stderr)

    # Scansiona contenuti sito
    pages = []
    for md in content_root.rglob("*.md"):
        url = build_url(content_root, md)
        if page_excluded(url):
            continue
        pd = extract_page_data(md)
        if not pd or not pd.get("title"):
            continue
        all_kw = pd["title_kw"] | pd["desc_kw"] | pd["body_kw"]
        if len(all_kw) < 5:
            continue
        pages.append({
            "key": build_key(content_root, md),
            "url": url,
            "title": pd["title"],
            "title_kw": pd["title_kw"],
            "desc_kw": pd["desc_kw"],
            "body_kw": pd["body_kw"],
            "all_kw": all_kw,
        })
    print(f"Pagine sito analizzate: {len(pages)}", file=sys.stderr)

    # Costruisci IDF dei video (frequenza delle keyword nei titoli video)
    video_keywords = {}
    for key, v in videos.items():
        kw = tokenize(v["titolo"])
        if not kw:
            continue
        video_keywords[key] = {
            "v": v,
            "kw": kw,
            "is_lis": v["id"] in lis_video_ids,
        }
    print(f"Video candidati: {len(video_keywords)}", file=sys.stderr)

    # IDF su pagine sito: parole molto frequenti = peso 0.2
    df = defaultdict(int)
    for p in pages:
        for k in p["all_kw"]:
            df[k] += 1
    n_pages = len(pages)
    weights = {}
    th_generic = max(2, int(0.20 * n_pages))
    th_common = max(2, int(0.10 * n_pages))
    for k, c in df.items():
        if c > th_generic:
            weights[k] = 0.2
        elif c > th_common:
            weights[k] = 0.6
        else:
            weights[k] = 1.0

    # Cross-match con pesi posizionali: title × 3, desc × 2, body × 1.
    # Vincolo: almeno una keyword in overlap deve essere nel titolo o nella
    # description della pagina E avere peso IDF >= 0.7 (cioè non super-generica).
    results = {}
    for page in pages:
        candidates = []
        title_desc_kw = page["title_kw"] | page["desc_kw"]
        for vkey, vdata in video_keywords.items():
            overlap = page["all_kw"] & vdata["kw"]
            if not overlap:
                continue
            # Vincolo qualità: almeno una keyword "ancorata" al titolo/desc
            # della pagina. Accetto anche peso IDF moderato (>= 0.5) per
            # consentire match su frasi tecniche con parole comuni nel sito
            # (es. "Centro Operativo Comunale" dove tutte le parole sono
            # frequenti ma il match è genuino sulla terminologia tecnica).
            anchored = [k for k in overlap
                        if k in title_desc_kw and weights.get(k, 1.0) >= 0.5]
            if not anchored:
                continue
            # Score posizionale: title × 3, desc × 2, body × 1
            score = 0.0
            for k in overlap:
                w = weights.get(k, 1.0)
                if k in page["title_kw"]:
                    score += w * 3.0
                elif k in page["desc_kw"]:
                    score += w * 2.0
                else:
                    score += w * 1.0
            if score < args.min_score:
                continue
            candidates.append({
                "id": vdata["v"]["id"],
                "titolo": vdata["v"]["titolo"],
                "url": vdata["v"]["url"],
                "canale": vdata["v"]["canale"],
                "score": round(score, 2),
                "overlap": sorted(overlap),
                "anchored": sorted(anchored),
                "is_lis": vdata["is_lis"],
            })
        candidates.sort(key=lambda x: -x["score"])
        top = candidates[: args.max_per_page]
        if top:
            results[page["key"]] = {
                "title": page["title"],
                "url": page["url"],
                "video": top,
            }

    # Stats
    n_pages_with_video = len(results)
    n_video_unique = len({v["id"] for r in results.values() for v in r["video"]})
    total_links = sum(len(r["video"]) for r in results.values())
    print(f"\nRisultato:", file=sys.stderr)
    print(f"  Pagine con almeno 1 video correlato: {n_pages_with_video}", file=sys.stderr)
    print(f"  Video unici usati: {n_video_unique}", file=sys.stderr)
    print(f"  Link video totali: {total_links}", file=sys.stderr)

    # Lookup canale per metadata di attribuzione
    canali = catalogo["canali"]

    out_path = repo_root / args.output
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# Mappa pagina del sito → video correlati pertinenti.\n")
        f.write(f"# Generato da scripts/genera-video-correlati.py via cross-match\n")
        f.write(f"# algoritmico (IDF-weighted) sul catalogo data/video_dpc_catalogo.yaml.\n")
        f.write(f"#\n")
        f.write(f"# Usato dal partial Hugo `video-correlati.html` per renderizzare la\n")
        f.write(f"# sezione 'Approfondimenti video' in fondo agli articoli pertinenti.\n")
        f.write(f"#\n")
        f.write(f"# Pagine coperte: {n_pages_with_video} / Video unici usati: {n_video_unique} /\n")
        f.write(f"# Link totali: {total_links} (max {args.max_per_page} per pagina,\n")
        f.write(f"# soglia score >= {args.min_score}).\n\n")
        yaml.safe_dump({"canali": canali, "pagine": results},
                       f, allow_unicode=True, sort_keys=True, width=120)
    print(f"\n✓ Scritto {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
