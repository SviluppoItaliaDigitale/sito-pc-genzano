#!/usr/bin/env python3
"""
Estende public/index.json con le pagine HTML statiche del sito che Hugo
NON indicizza nativamente — quelle che vivono in static/ come file HTML
standalone (giochi, schede stampabili, kit calamità bambini, abili a
proteggere, formazionepc, quizpc, storie e racconti).

Lo script va eseguito DOPO `hugo --minify`, una volta per ciascuna delle
due build (Aruba + GitHub Pages). Ricava il baseURL dalle voci già
presenti nell'index e mantiene il formato JSON identico ai record Hugo.

Uso:
    python3 scripts/aggiungi-pagine-statiche-al-cerca.py

Output: sovrascrive public/index.json con voci Hugo + voci statiche.
Idempotente: se già eseguito, non duplica i record.
"""
import html as html_module
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

PUBLIC_DIR = Path('public')
INDEX_FILE = PUBLIC_DIR / 'index.json'

# Cartelle (sotto public/) che contengono HTML statici da indicizzare.
# Whitelist esplicita: evita di indicizzare file legacy o sistema (404,
# sitemap, googleXXXX.html di verifica).
SCAN_DIRS = [
    'giochi',
    'formazionepc',
    'quizpc',
    'abili-a-proteggere',
    'formazione/schede-stampabili',
    'formazione/storie-e-racconti',
]
# Le cartelle kit-calamita-* sono dinamiche, le scopro a runtime
KIT_CALAMITA_GLOB = 'formazione/kit-calamita-*'

# File da escludere anche dentro le cartelle whitelist
EXCLUDE_FILES = {
    '404.html',
    'sitemap.html',
}

# Estrai title da un HTML
TITLE_RE = re.compile(r'<title[^>]*>(.*?)</title>', re.DOTALL | re.IGNORECASE)
META_DESC_RE = re.compile(
    r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']*)["\']',
    re.IGNORECASE,
)
BODY_RE = re.compile(r'<body[^>]*>(.*?)</body>', re.DOTALL | re.IGNORECASE)
DROP_TAGS_RE = re.compile(
    r'<(script|style|nav|header|footer|aside|form|noscript|svg)\b[^>]*>.*?</\1>',
    re.DOTALL | re.IGNORECASE,
)
ANY_TAG_RE = re.compile(r'<[^>]+>')
WHITESPACE_RE = re.compile(r'\s+')


def extract_title(html_text: str) -> str:
    m = TITLE_RE.search(html_text)
    if not m:
        return ''
    raw = m.group(1).strip()
    raw = html_module.unescape(raw)
    # Tronca eventuali suffissi tipo " — Protezione Civile Genzano"
    return raw[:150]


def extract_description(html_text: str) -> str:
    m = META_DESC_RE.search(html_text)
    if not m:
        return ''
    return html_module.unescape(m.group(1).strip())[:300]


def extract_text(html_text: str, max_len: int = 1500) -> str:
    """Estrae testo leggibile dalla <body>, rimuovendo script/style/nav/footer
    e tag HTML."""
    body_match = BODY_RE.search(html_text)
    body = body_match.group(1) if body_match else html_text
    # Rimuovi blocchi non-contenuto
    body = DROP_TAGS_RE.sub(' ', body)
    # Rimuovi tutti gli altri tag
    text = ANY_TAG_RE.sub(' ', body)
    # Decode entità HTML
    text = html_module.unescape(text)
    # Pulizia whitespace
    text = WHITESPACE_RE.sub(' ', text).strip()
    return text[:max_len]


def derive_base_url(existing_records: list) -> str:
    """Ricava il baseURL dell'attuale build (Aruba o GitHub Pages) dalle
    voci già presenti nell'index.json di Hugo."""
    if not existing_records:
        return 'https://www.protezionecivilegenzano.it/'
    sample = existing_records[0]['url']
    parsed = urlparse(sample)
    # Trova la parte di path prima del primo segmento "vero" del contenuto
    # Per https://sviluppoitaliadigitale.github.io/sito-pc-genzano/foo/
    #  → baseURL = https://sviluppoitaliadigitale.github.io/sito-pc-genzano/
    # Per https://www.protezionecivilegenzano.it/foo/
    #  → baseURL = https://www.protezionecivilegenzano.it/
    parts = parsed.path.strip('/').split('/')
    # Se il primo segmento è "sito-pc-genzano" (GitHub Pages), tienilo
    if parts and parts[0] == 'sito-pc-genzano':
        return f'{parsed.scheme}://{parsed.netloc}/sito-pc-genzano/'
    return f'{parsed.scheme}://{parsed.netloc}/'


def url_path_for_file(file_path: Path) -> str:
    """Ritorna il path URL relativo a public/ per il file dato.
    Esempi:
      public/giochi/infanzia/tartaruga-saggia/index.html → /giochi/infanzia/tartaruga-saggia/
      public/formazionepc/assist_01_accoglienza.html    → /formazionepc/assist_01_accoglienza.html
    """
    rel = file_path.relative_to(PUBLIC_DIR).as_posix()
    if rel.endswith('/index.html'):
        return '/' + rel[: -len('index.html')]
    if rel == 'index.html':
        return '/'
    return '/' + rel


def existing_url_paths(records: list, base_url: str) -> set:
    """Set di path URL (es. '/contatti/') già coperti dai record Hugo."""
    base_path = urlparse(base_url).path  # es. '/sito-pc-genzano/' o '/'
    seen = set()
    for r in records:
        u = urlparse(r['url']).path
        # Strip baseURL path prefix per ottenere il path "relativo al sito"
        if base_path != '/' and u.startswith(base_path):
            u = '/' + u[len(base_path):]
        seen.add(u)
    return seen


def section_for_path(path: str) -> str:
    """Ricava la 'section' (prima cartella) dall'URL path."""
    parts = path.strip('/').split('/')
    return parts[0] if parts and parts[0] else 'home'


def collect_static_dirs() -> list:
    """Restituisce le cartelle (relative a public/) da scansionare."""
    dirs = list(SCAN_DIRS)
    # Aggiungi tutte le cartelle kit-calamita-* esistenti in public/
    for p in PUBLIC_DIR.glob(KIT_CALAMITA_GLOB):
        if p.is_dir():
            dirs.append(p.relative_to(PUBLIC_DIR).as_posix())
    return dirs


def main():
    if not INDEX_FILE.exists():
        print(f'ERRORE: {INDEX_FILE} non esiste. Esegui prima hugo --minify.')
        sys.exit(1)

    records = json.loads(INDEX_FILE.read_text(encoding='utf-8'))
    initial_count = len(records)
    print(f'Voci Hugo già indicizzate: {initial_count}')

    base_url = derive_base_url(records)
    print(f'Base URL ricavato: {base_url}')

    seen_paths = existing_url_paths(records, base_url)

    static_dirs = collect_static_dirs()
    print(f'Scansione di {len(static_dirs)} cartelle statiche…')

    added = 0
    for d in static_dirs:
        full_dir = PUBLIC_DIR / d
        if not full_dir.exists():
            continue
        for html_file in full_dir.rglob('*.html'):
            if html_file.name in EXCLUDE_FILES:
                continue
            path = url_path_for_file(html_file)
            if path in seen_paths:
                continue  # già indicizzato da Hugo

            try:
                content = html_file.read_text(encoding='utf-8', errors='ignore')
            except Exception as e:
                print(f'  SKIP {html_file}: {e}')
                continue

            title = extract_title(content)
            if not title:
                continue  # senza titolo non vale la pena indicizzare
            description = extract_description(content)
            text = extract_text(content)

            record = {
                'title': title,
                'url': base_url.rstrip('/') + path,
                'content': text,
                'section': section_for_path(path),
            }
            if description:
                record['description'] = description

            records.append(record)
            seen_paths.add(path)
            added += 1

    if added == 0:
        print('Nessuna nuova pagina statica da aggiungere (idempotente).')
    else:
        INDEX_FILE.write_text(
            json.dumps(records, ensure_ascii=False, separators=(',', ':')),
            encoding='utf-8',
        )
        print(f'Aggiunte {added} pagine statiche all\'indice.')
        print(f'Totale voci nell\'indice: {len(records)} (prima: {initial_count})')


if __name__ == '__main__':
    main()
