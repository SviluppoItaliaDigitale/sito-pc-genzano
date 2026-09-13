#!/usr/bin/env python3
"""
Rende indicizzabili da Pagefind le pagine HTML statiche del sito.

Il tema marca il contenuto delle pagine Hugo con `data-pagefind-body` sul
<main> (baseof.html). Per Pagefind quel marcatore è esclusivo: se anche una
sola pagina lo porta, vengono indicizzate SOLO le pagine che lo hanno. Le
pagine statiche che vivono in static/ come file HTML autonomi — le schede
stampabili, i giochi, i kit calamità, le storie, quizpc, formazionepc,
abili-a-proteggere — non lo hanno mai avuto e quindi non sono mai comparse
nella ricerca del sito (Ctrl+K e /cerca/), pur essendo online e linkate.

Questo script gira DOPO `hugo --minify` e PRIMA di `npx pagefind`, una volta
per ciascuna delle due build (Aruba + GitHub Pages), e lavora solo su
public/: i sorgenti in static/ non si toccano, così una scheda nuova è
indicizzata senza che nessuno debba ricordarsi di marcarla.

Cosa fa su ogni file:
  1. aggiunge `data-pagefind-body` al <body>, se non c'è già un marcatore;
  2. aggiunge `data-pagefind-ignore` alle barre strumenti non stampabili
     (.no-print, .scheda-toolbar, .storia-toolbar) e ai contenitori che il
     chrome riempie via JavaScript, perché non finiscano negli estratti.

Uso:
    python3 scripts/prepara-statiche-per-pagefind.py [--dry-run]

Idempotente: rieseguirlo non cambia nulla.
"""
import re
import sys
from pathlib import Path

PUBLIC_DIR = Path('public')

# Stessa whitelist di aggiungi-pagine-statiche-al-cerca.py: le famiglie di
# pagine HTML autonome che Hugo non genera ma che il sito pubblica.
SCAN_DIRS = [
    'giochi',
    'formazionepc',
    'quizpc',
    'abili-a-proteggere',
    'formazione/schede-stampabili',
    'formazione/storie-e-racconti',
]
KIT_CALAMITA_GLOB = 'formazione/kit-calamita-*'

EXCLUDE_FILES = {'404.html', 'sitemap.html'}

BODY_RE = re.compile(r'<body(?![^>]*\bdata-pagefind-body\b)([^>]*)>', re.IGNORECASE)
HA_MARCATORE_RE = re.compile(r'\bdata-pagefind-body\b', re.IGNORECASE)

# Elementi di servizio da escludere dagli estratti della ricerca.
CLASSI_DA_IGNORARE = ('no-print', 'scheda-toolbar', 'storia-toolbar')
APERTURA_RE = re.compile(r'<(div|nav|header|footer|section|aside)\b([^>]*)>', re.IGNORECASE)


def file_da_trattare():
    visti = set()
    cartelle = list(SCAN_DIRS)
    for kit in sorted(PUBLIC_DIR.glob(KIT_CALAMITA_GLOB)):
        if kit.is_dir():
            cartelle.append(kit.relative_to(PUBLIC_DIR).as_posix())
    for rel in cartelle:
        base = PUBLIC_DIR / rel
        if not base.is_dir():
            continue
        for f in sorted(base.rglob('*.html')):
            if f.name in EXCLUDE_FILES or f in visti:
                continue
            visti.add(f)
            yield f


def ignora_barre(testo: str) -> tuple[str, int]:
    """Marca con data-pagefind-ignore le barre strumenti di servizio."""
    contatore = 0

    def sostituisci(m):
        nonlocal contatore
        tag, attributi = m.group(1), m.group(2)
        if 'data-pagefind-ignore' in attributi.lower():
            return m.group(0)
        classe = re.search(r'class=["\']([^"\']*)["\']', attributi, re.IGNORECASE)
        if not classe:
            return m.group(0)
        valori = classe.group(1).split()
        if not any(c in valori for c in CLASSI_DA_IGNORARE):
            return m.group(0)
        contatore += 1
        return f'<{tag}{attributi} data-pagefind-ignore>'

    return APERTURA_RE.sub(sostituisci, testo), contatore


def main() -> int:
    prova = '--dry-run' in sys.argv
    if not PUBLIC_DIR.is_dir():
        print('public/ non esiste: esegui prima `hugo --minify`.', file=sys.stderr)
        return 1

    marcati = gia_a_posto = barre = 0
    for f in file_da_trattare():
        testo = f.read_text(encoding='utf-8', errors='replace')
        originale = testo
        if HA_MARCATORE_RE.search(testo):
            gia_a_posto += 1
        else:
            testo, n = BODY_RE.subn(r'<body\1 data-pagefind-body>', testo, count=1)
            if n:
                marcati += 1
            else:
                # Nessun <body>: è un frammento, non una pagina. Si salta.
                continue
        testo, n_barre = ignora_barre(testo)
        barre += n_barre
        if testo != originale and not prova:
            f.write_text(testo, encoding='utf-8')

    print(f'Pagine statiche marcate per la ricerca: {marcati}'
          f' (già a posto: {gia_a_posto}); barre di servizio escluse: {barre}')
    if prova:
        print('(prova a vuoto: nessun file scritto)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
