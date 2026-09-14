#!/usr/bin/env python3
"""Aggiunge il link canonical alle pagine HTML autonome di `static/`.

Le pagine generate da Hugo hanno già il canonical dal tema. Le pagine statiche
— schede stampabili, giochi, kit, storie, quizpc, formazionepc,
abili-a-proteggere — no: al 14/09/2026 ce l'avevano 2 file su 393. Senza
canonical lo stesso foglio è raggiungibile a indirizzi diversi (produzione
Aruba, copia GitHub Pages, varianti con `?stampa=1` o con parametri di
tracciamento aggiunti da chi condivide il link) e per un motore di ricerca
sono pagine distinte che si fanno concorrenza.

L'URL preferito è sempre quello di produzione: la copia su GitHub Pages
rimanda a quella, non viceversa.

Lo script è idempotente: se il canonical c'è già, non lo tocca — nemmeno
quando punta altrove, perché le due cartelle delle schede ritirate
(pronto-soccorso-infanzia, sicurezza-in-casa-infanzia) contengono un
reindirizzamento all'indice e il loro canonical deve restare quello.

    python3 scripts/aggiungi-canonical-statiche.py [--check] [--dry-run]

`--check` non scrive nulla ed esce con 1 se qualche pagina è senza canonical:
serve in CI per non far scivolare indietro le famiglie nuove.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "static"
BASE = "https://www.protezionecivilegenzano.it"

# Le famiglie di pagine autonome. Aggiungendone una nuova, va aggiunta qui:
# è lo stesso vincolo di `prepara-statiche-per-pagefind.py`, e per la stessa
# ragione — una famiglia che nessuno elenca resta fuori dai controlli.
FAMIGLIE = [
    "formazione/schede-stampabili",
    "formazione/kit-calamita-shared",
    "formazione/storie-e-racconti",
    "giochi",
    "quizpc",
    "formazionepc",
    "abili-a-proteggere",
    "monitor",
]

HA_CANONICAL = re.compile(r'<link[^>]+rel=["\']canonical["\']', re.I)
# Le pagine marcate noindex (i pacchetti «Stampa tutto», che raccolgono schede
# già indicizzate una per una) non hanno bisogno di un URL preferito: ai motori
# stiamo già dicendo di non indicizzarle, e un canonical su una pagina noindex
# è un'istruzione che si contraddice.
NOINDEX = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)
# Il canonical va dopo il titolo, prima dei fogli di stile: è la posizione che
# usa il tema Hugo, così i due tipi di pagina si leggono allo stesso modo.
DOPO = re.compile(r"(<title>.*?</title>\s*\n)", re.S | re.I)
DOPO_FALLBACK = re.compile(r"(<meta\s+charset=[^>]*>\s*\n)", re.I)


def url_di(path: Path) -> str:
    rel = path.relative_to(STATIC).as_posix()
    if rel.endswith("/index.html"):
        rel = rel[: -len("index.html")]
    elif rel == "index.html":
        rel = ""
    return f"{BASE}/{rel}"


def pagine():
    for fam in FAMIGLIE:
        base = STATIC / fam
        if not base.exists():
            continue
        for p in sorted(base.rglob("*.html")):
            yield p


def main() -> int:
    solo_check = "--check" in sys.argv
    prova = "--dry-run" in sys.argv
    mancanti, aggiunte, gia = [], 0, 0

    for p in pagine():
        testo = p.read_text(encoding="utf-8", errors="replace")
        if "<head" not in testo.lower():
            continue  # frammento, non una pagina
        if NOINDEX.search(testo):
            continue
        if HA_CANONICAL.search(testo):
            gia += 1
            continue
        if solo_check:
            mancanti.append(p.relative_to(ROOT).as_posix())
            continue

        riga = f'  <link rel="canonical" href="{url_di(p)}">\n'
        nuovo, n = DOPO.subn(lambda m: m.group(1) + riga, testo, count=1)
        if n == 0:
            nuovo, n = DOPO_FALLBACK.subn(lambda m: m.group(1) + riga, testo, count=1)
        if n == 0:
            mancanti.append(p.relative_to(ROOT).as_posix())
            continue
        if not prova:
            p.write_text(nuovo, encoding="utf-8")
        aggiunte += 1

    if solo_check:
        if mancanti:
            print(f"❌ {len(mancanti)} pagine statiche senza canonical:")
            for m in mancanti[:20]:
                print("   -", m)
            if len(mancanti) > 20:
                print(f"   … e altre {len(mancanti) - 20}")
            print("\nRimedio: python3 scripts/aggiungi-canonical-statiche.py")
            return 1
        print(f"✅ Canonical presente su tutte le pagine statiche ({gia} file).")
        return 0

    print(f"Canonical aggiunto a {aggiunte} pagine; già presente su {gia}.")
    if mancanti:
        print(f"⚠ {len(mancanti)} senza un punto d'inserimento nel <head>:", file=sys.stderr)
        for m in mancanti:
            print("   -", m, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
