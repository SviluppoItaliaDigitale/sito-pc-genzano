#!/usr/bin/env python3
"""Controllo della navigazione: assistente virtuale e mappa del sito.

Verifica che l'assistente virtuale (layouts/assistente/list.html) e la
mappa del sito (content/mappa-sito/_index.md) portino a ogni voce del
menu principale e del piè di pagina (hugo.toml), che l'albero
dell'assistente sia integro (identificativi unici, ogni «next» porta a una
risposta esistente, ogni risposta si raggiunge dall'inizio) e, con
--public, che ogni collegamento interno dei due porti a una pagina
esistente della build, ancora compresa.

Nasce il 06/10/2026: all'assistente mancavano 19 voci del menu e due
collegamenti portavano a pagine inesistenti; alla mappa ne mancavano 7.
Gira in validate-pr.yml, bloccante.

Uso:
    python3 scripts/check-navigazione.py                 # copertura e albero
    python3 scripts/check-navigazione.py --public public # anche i collegamenti
Exit code: 0 se tutto è a posto, 1 se c'è almeno un errore.
"""
import argparse
import html
import re
import sys
import tomllib
from collections import deque
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
ASSISTENTE = RADICE / "themes/flavour-pcgenzano/layouts/assistente/list.html"
MAPPA = RADICE / "content/mappa-sito/_index.md"
HUGO = RADICE / "hugo.toml"

# Voci che non hanno senso come destinazione in uno dei due strumenti.
ESCLUSE = {
    "assistente": {"/", "/assistente/"},
    "mappa": {"/", "/mappa-sito/"},
}


def norm(url):
    """Percorso senza query e senza frammento, con la barra finale."""
    url = url.split("#", 1)[0].split("?", 1)[0]
    if url and not url.endswith("/") and "." not in url.rsplit("/", 1)[-1]:
        url += "/"
    return url


def voci_menu():
    dati = tomllib.loads(HUGO.read_text(encoding="utf-8"))
    voci = []
    for nome in ("main", "footer"):
        for voce in dati.get("menus", {}).get(nome, []):
            url = voce.get("url")
            if url and url.startswith("/"):
                voci.append((nome, voce.get("name", ""), norm(url)))
    return voci


def url_assistente(testo):
    return re.findall(r"url:\s*'(/[^']*)'", testo)


def url_mappa(testo):
    return [u for u in re.findall(r'(?:href="|\]\()(/[^")\s]*)', testo) if not u.startswith("//")]


def nodi_assistente(testo):
    corpo = testo[testo.index("var NODES = {"):]
    return set(re.findall(r"^    ([a-z_0-9]+): \{", corpo, re.M))


def controlla_albero(testo, errori):
    corpo = testo[testo.index("var NODES = {"):]
    ids = re.findall(r"^    ([a-z_0-9]+): \{", corpo, re.M)
    doppi = sorted({i for i in ids if ids.count(i) > 1})
    for i in doppi:
        errori.append(f"assistente: il nodo «{i}» è definito più volte")
    # «next» di ogni nodo: si taglia il testo fra un nodo e il successivo
    posizioni = [(m.group(1), m.start()) for m in re.finditer(r"^    ([a-z_0-9]+): \{", corpo, re.M)]
    figli = {}
    for k, (nodo, inizio) in enumerate(posizioni):
        fine = posizioni[k + 1][1] if k + 1 < len(posizioni) else len(corpo)
        figli[nodo] = re.findall(r"next:\s*'([a-z_0-9]+)'", corpo[inizio:fine])
    for nodo, lista in figli.items():
        for f in lista:
            if f not in figli:
                errori.append(f"assistente: «{nodo}» porta a «{f}», che non esiste")
    if "start" not in figli:
        errori.append("assistente: manca il nodo «start»")
        return
    visti, coda = {"start"}, deque(["start"])
    while coda:
        for f in figli.get(coda.popleft(), []):
            if f in figli and f not in visti:
                visti.add(f)
                coda.append(f)
    for nodo in sorted(set(figli) - visti):
        errori.append(f"assistente: il nodo «{nodo}» non si raggiunge da nessuna scelta")


def controlla_copertura(nome, presenti, errori):
    presenti = {norm(u) for u in presenti}
    for menu, voce, url in voci_menu():
        if url in ESCLUSE[nome] or url in presenti:
            continue
        dove = "menu" if menu == "main" else "piè di pagina"
        errori.append(f"{nome}: manca la voce del {dove} «{voce}» ({url})")


def controlla_collegamenti(nome, urls, public, errori, nodi=()):
    """I frammenti di /assistente/ sono risposte dell'assistente, non ancore."""
    cache = {}
    for url in sorted(set(urls)):
        percorso = norm(url)
        file = public / percorso.lstrip("/")
        if percorso.endswith("/"):
            file = file / "index.html"
        if not file.exists():
            errori.append(f"{nome}: il collegamento {url} porta a una pagina che non esiste")
            continue
        if percorso == "/assistente/" and "#" in url:
            if url.split("#", 1)[1] not in nodi:
                errori.append(f"{nome}: il collegamento {url} porta a una risposta dell'assistente che non esiste")
            continue
        if "#" in url and file.suffix == ".html":
            frammento = html.unescape(url.split("#", 1)[1])
            if file not in cache:
                cache[file] = set(re.findall(r'\bid=["\']?([^"\'\s>]+)', file.read_text(encoding="utf-8", errors="replace")))
            if frammento and frammento not in cache[file]:
                errori.append(f"{nome}: il collegamento {url} punta a un'ancora che non esiste")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--public", type=Path, help="cartella della build Hugo, per verificare i collegamenti")
    args = parser.parse_args()

    errori = []
    testo_a = ASSISTENTE.read_text(encoding="utf-8")
    testo_m = MAPPA.read_text(encoding="utf-8")
    controlla_albero(testo_a, errori)
    controlla_copertura("assistente", url_assistente(testo_a), errori)
    controlla_copertura("mappa", url_mappa(testo_m), errori)
    if args.public:
        nodi = nodi_assistente(testo_a)
        controlla_collegamenti("assistente", url_assistente(testo_a), args.public, errori, nodi)
        controlla_collegamenti("mappa", url_mappa(testo_m), args.public, errori, nodi)

    if errori:
        print(f"❌ {len(errori)} problemi di navigazione:")
        for e in errori:
            print("  -", e)
        print("\nOgni voce di menu nuova va aggiunta anche all'assistente virtuale "
              "(themes/flavour-pcgenzano/layouts/assistente/list.html) e alla mappa del sito "
              "(content/mappa-sito/_index.md).")
        return 1
    print("✅ Assistente virtuale e mappa del sito coprono tutte le voci del menu"
          + (", e ogni collegamento porta a una pagina esistente." if args.public else "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
