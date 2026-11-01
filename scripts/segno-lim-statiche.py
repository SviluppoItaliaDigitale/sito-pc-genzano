#!/usr/bin/env python3
"""
Mette «Pronto per la LIM» nella barra in alto delle schede stampabili e delle storie,
che non caricano JavaScript (regola .claude/rules/lim-scuole.md, 01/11/2026).

Il segno è un link a /lim/ con la classe scheda-lim, prima del pulsante di stampa; la barra
non si stampa (no-print), quindi fogli e pacchetti «Stampa tutto» non cambiano. Le pagine di
rimando (meta refresh) e i pacchetti sono esclusi. Giochi, quiz, Abili a proteggere e gli
indici delle schede e delle storie lo ricevono da site-chrome.js, le pagine Hugo dal partial
lim-pronto.html (elenco in data/lim.yaml).

Uso: python3 scripts/segno-lim-statiche.py            aggiunge il segno dove manca
     python3 scripts/segno-lim-statiche.py --check    esce 1 se manca da qualche pagina
Idempotente. Lo controlla validate-pr.yml: una scheda o una storia nuova (anche rigenerata
da uno script di scripts/schede-didattiche/) senza il segno ferma la PR.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
FAMIGLIE = {
    "static/formazione/schede-stampabili": ("scheda-toolbar", "scheda-lim"),
    "static/formazione/storie-e-racconti": ("storia-toolbar", "storia-lim scheda-lim"),
}
TITOLO = ("Si usa col dito sulla lavagna interattiva della classe, anche a schermo intero, "
          "e funziona sui browser delle lavagne meno recenti")


def segno(classe: str) -> str:
    return (f'<a class="{classe}" href="/lim/" title="{TITOLO}">'
            f'Pronto per la LIM</a>\n    ')


def main() -> int:
    controlla = "--check" in sys.argv
    mancanti, aggiunti = [], 0
    for cartella, (barra, classe) in FAMIGLIE.items():
        for f in sorted((RADICE / cartella).rglob("index.html")):
            rel = f.relative_to(RADICE).as_posix()
            if "/pacchetti/" in rel or f.parent == RADICE / cartella:
                continue  # pacchetti «Stampa tutto»; l'indice lo riceve da site-chrome.js
            testo = f.read_text(encoding="utf-8")
            if 'http-equiv="refresh"' in testo or f'class="{barra}' not in testo:
                continue  # pagina di rimando, o senza barra
            if "scheda-lim" in testo:
                continue
            if controlla:
                mancanti.append(rel)
                continue
            m = re.search(rf'<div class="{barra}[^"]*">(.*?)</div>', testo, re.S)
            if not m:
                mancanti.append(rel)
                continue
            dentro = m.group(1)
            b = dentro.find("<button")
            nuovo = dentro[:b] + segno(classe) + dentro[b:] if b >= 0 else dentro.rstrip() + "\n    " + segno(classe).rstrip() + "\n  "
            testo = testo[:m.start(1)] + nuovo + testo[m.end(1):]
            f.write_text(testo, encoding="utf-8")
            aggiunti += 1
    if controlla:
        if mancanti:
            print(f"❌ {len(mancanti)} schede o storie senza «Pronto per la LIM»: esegui "
                  "python3 scripts/segno-lim-statiche.py e committa.")
            for r in mancanti[:30]:
                print("  - " + r)
            return 1
        print("✅ Tutte le schede e le storie hanno «Pronto per la LIM» nella barra in alto.")
        return 0
    if mancanti:
        print(f"⚠️ Barra non riconosciuta in {len(mancanti)} pagine: " + ", ".join(mancanti[:10]))
    print(f"Aggiunto «Pronto per la LIM» a {aggiunti} pagine.")
    return 1 if mancanti else 0


if __name__ == "__main__":
    sys.exit(main())
