#!/usr/bin/env python3
"""Aggiunge il link canonical alle pagine HTML autonome di `static/`.

Le pagine generate da Hugo hanno già il canonical dal tema. Le pagine statiche
— schede stampabili, giochi, kit, storie, quizpc, formazionepc,
abili-a-proteggere, moduli per le scuole — no: al 14/09/2026 ce l'avevano 2 file su 393. Senza
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

    python3 scripts/aggiungi-canonical-statiche.py [--dry-run]

`--check` non scrive nulla ed esce con 1 se qualche pagina è senza canonical:
serve in CI per non far scivolare indietro le famiglie nuove. Esce con 1 anche
se una pagina indicizzabile di `static/` non appartiene a nessuna famiglia, e
con `--sitemap public/sitemap.xml` se una pagina con il canonical manca dalla
mappa per i motori. Nasce il 21/10/2026: la famiglia dei kit calamità puntava
alla cartella del foglio di stile (kit-calamita-shared), le 143 schede dei kit
erano rimaste senza canonical e il controllo passava lo stesso.

    python3 scripts/aggiungi-canonical-statiche.py --check [--sitemap public/sitemap.xml]
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
    "formazione/kit-calamita-*",  # una cartella per categoria (animali, anziani, bambini…)
    "formazione/storie-e-racconti",
    "giochi",
    "quizpc",
    "formazionepc",
    "abili-a-proteggere",
    "monitor",
    "scuole",  # moduli per le scuole (liberatoria, circolare, convenzione PCTO…), dal 21/10/2026
]

HA_CANONICAL = re.compile(r'<link[^>]+rel=["\']canonical["\']', re.I)
# Le pagine marcate noindex (i pacchetti «Stampa tutto», che raccolgono schede
# già indicizzate una per una) non hanno bisogno di un URL preferito: ai motori
# stiamo già dicendo di non indicizzarle, e un canonical su una pagina noindex
# è un'istruzione che si contraddice.
NOINDEX = re.compile(r'<meta[^>]+name=["\']robots["\'][^>]*content=["\'][^"\']*noindex', re.I)
# Le pagine che rimandano a un altro indirizzo (schede ritirate, vecchi giochi)
RIMANDO = re.compile(r'<meta[^>]+http-equiv=["\']refresh["\']', re.I)
URL_CANONICAL = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)', re.I)
# Il canonical va dopo il titolo, prima dei fogli di stile: è la posizione che
# usa il tema Hugo, così i due tipi di pagina si leggono allo stesso modo.
DOPO = re.compile(r"(<title>.*?</title>\s*\n)", re.S | re.I)
DOPO_FALLBACK = re.compile(r"(<meta\s+charset=[^>]*>\s*\n)", re.I)
# Molte schede dei kit hanno il <head> su una riga sola: lì il canonical va
# subito dopo </title>, sulla stessa riga.
TITOLO = re.compile(r"(<title>.*?</title>)", re.S | re.I)


def url_di(path: Path) -> str:
    rel = path.relative_to(STATIC).as_posix()
    if rel.endswith("/index.html"):
        rel = rel[: -len("index.html")]
    elif rel == "index.html":
        rel = ""
    return f"{BASE}/{rel}"


def pagine():
    # una famiglia può essere un modello di cartella (formazione/kit-calamita-*)
    for fam in FAMIGLIE:
        for base in sorted(STATIC.glob(fam)):
            if base.is_dir():
                yield from sorted(base.rglob("*.html"))


def indicizzabile(testo: str) -> bool:
    """Una pagina vera (ha il <head>), né noindex né un rimando a un altro indirizzo."""
    return "<head" in testo.lower() and not NOINDEX.search(testo) and not RIMANDO.search(testo)


def fuori_dalle_famiglie() -> list[str]:
    """Pagine indicizzabili di static/ che nessuna famiglia elenca."""
    dentro = set(pagine())
    fuori = []
    for p in sorted(STATIC.rglob("*.html")):
        if p in dentro or "vendor" in p.relative_to(STATIC).parts:
            continue
        if indicizzabile(p.read_text(encoding="utf-8", errors="replace")):
            fuori.append(p.relative_to(ROOT).as_posix())
    return fuori


def assenti_dalla_mappa(sitemap: Path) -> list[str]:
    """Pagine con il canonical il cui indirizzo non compare nella mappa per i motori."""
    indirizzi = set(re.findall(r"<loc>([^<]+)</loc>", sitemap.read_text(encoding="utf-8")))
    assenti = []
    for p in pagine():
        testo = p.read_text(encoding="utf-8", errors="replace")
        m = URL_CANONICAL.search(testo)
        if m and indicizzabile(testo) and m.group(1) not in indirizzi:
            assenti.append(f"{p.relative_to(ROOT).as_posix()} ({m.group(1)})")
    return assenti


def main() -> int:
    solo_check = "--check" in sys.argv
    prova = "--dry-run" in sys.argv
    sitemap = None
    if "--sitemap" in sys.argv:
        i = sys.argv.index("--sitemap")
        if i + 1 >= len(sys.argv) or not Path(sys.argv[i + 1]).is_file():
            print("--sitemap vuole il percorso di una sitemap.xml esistente", file=sys.stderr)
            return 2
        sitemap = Path(sys.argv[i + 1])
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
            nuovo, n = TITOLO.subn(lambda m: m.group(1) + riga.strip(), testo, count=1)
        if n == 0:
            mancanti.append(p.relative_to(ROOT).as_posix())
            continue
        if not prova:
            p.write_text(nuovo, encoding="utf-8")
        aggiunte += 1

    if solo_check:
        esito = 0
        if mancanti:
            print(f"❌ {len(mancanti)} pagine statiche senza canonical:")
            for m in mancanti[:20]:
                print("   -", m)
            if len(mancanti) > 20:
                print(f"   … e altre {len(mancanti) - 20}")
            print("\nRimedio: python3 scripts/aggiungi-canonical-statiche.py")
            esito = 1
        fuori = fuori_dalle_famiglie()
        if fuori:
            print(f"❌ {len(fuori)} pagine indicizzabili di static/ fuori da ogni famiglia:")
            for m in fuori[:20]:
                print("   -", m)
            if len(fuori) > 20:
                print(f"   … e altre {len(fuori) - 20}")
            print("\nRimedio: aggiungi la loro cartella a FAMIGLIE in questo script e, se devono\n"
                  "comparire nella ricerca e nei motori, a prepara-statiche-per-pagefind.py,\n"
                  "aggiungi-pagine-statiche-al-cerca.py e alla mappa per i motori del tema.")
            esito = 1
        if sitemap:
            assenti = assenti_dalla_mappa(sitemap)
            if assenti:
                print(f"❌ {len(assenti)} pagine statiche con il canonical assenti dalla mappa per i motori:")
                for m in assenti[:20]:
                    print("   -", m)
                if len(assenti) > 20:
                    print(f"   … e altre {len(assenti) - 20}")
                print("\nRimedio: aggiungi la famiglia a themes/flavour-pcgenzano/layouts/_default/sitemap.xml")
                esito = 1
        if esito == 0:
            print(f"✅ Canonical presente su tutte le pagine statiche ({gia} file); nessuna pagina "
                  "fuori dalle famiglie" + ("; tutte nella mappa per i motori." if sitemap else "."))
        return esito

    print(f"Canonical aggiunto a {aggiunte} pagine; già presente su {gia}.")
    if mancanti:
        print(f"⚠ {len(mancanti)} senza un punto d'inserimento nel <head>:", file=sys.stderr)
        for m in mancanti:
            print("   -", m, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
