#!/usr/bin/env python3
"""
Controllo dei dati canonici: lo stesso dato deve essere uguale in tutto il sito.

Legge data/dati_canonici.yaml (valore ufficiale, fonte e varianti sbagliate di
ogni dato) e cerca le varianti sbagliate nei sorgenti del sito: Markdown in
content/, dati YAML in data/, pagine e script statici in static/ e nei layout
del tema. Una variante conta solo se nel raggio di "finestra" caratteri compare
anche il "contesto" della regola (per esempio «Colli Albani»), così «20.000
anni» riferito a un altro vulcano non fa scattare nulla. Con "stessa_frase:
true" il contesto deve stare nella stessa frase della variante, con
"stesso_paragrafo: true" nello stesso paragrafo o elenco. Due eccezioni
per i casi legittimi: "salvo_se_frase" (la frase della variante parla di
altro, per esempio del Vesuvio) e "salvo_se_prima" (subito prima della
variante c'è una negazione: «Non devi chiamare il 118»).

Nasce il 01/10/2026: l'ultima eruzione dei Colli Albani compariva con tre
valori diversi e l'Osservatorio Vesuviano era indicato come ente di
sorveglianza. Gira su ogni pull request in validate-pr.yml.

Uso:
  python3 scripts/check-dati-canonici.py [file ...]
Senza argomenti controlla tutto il perimetro. Exit code = numero di varianti
trovate (0 = tutto allineato). Solo Python standard più PyYAML.
"""

from __future__ import annotations

import re
import sys
from fnmatch import fnmatch
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRO = ROOT / "data" / "dati_canonici.yaml"

PERIMETRO = [
    ("content", "*.md"),
    ("data", "*.yaml"),
    ("data", "*.yml"),
    ("static", "*.html"),
    ("static", "*.js"),
    ("themes/flavour-pcgenzano/layouts", "*.html"),
]

# File rigenerati da altri sorgenti (si correggono alla fonte), librerie di
# terzi, cataloghi importati e il registro stesso.
ESCLUSI = [
    "data/dati_canonici.yaml",
    "data/video_dpc_catalogo.yaml",
    "data/video_correlati.yaml",
    "static/formazione/schede-stampabili/pacchetti/*",
    "static/vendor/*",
    "static/open-data/*",
    "static/pagefind/*",
    "themes/flavour-pcgenzano/static/vendor/*",
]

# Solo i tag HTML veri (iniziano con lettera, «/» o «!»): gli shortcode Hugo
# «{{< nome attr="…" >}}» restano, perché i loro attributi sono testo pubblicato.
RE_TAG = re.compile(r"(?<!\{)<[A-Za-z/!][^>]*>")
RE_FINE_FRASE = re.compile(r"[.!?;]\s|\n\s*\n|\||\{\{[<%]|[>%]\}\}")
RE_FINE_PARAGRAFO = re.compile(r"\n\s*\n|\{\{[<%]|[>%]\}\}")


def tratto_intorno(testo: str, inizio: int, fine: int, confine: re.Pattern) -> tuple[int, int]:
    """Inizio e fine del tratto (frase o paragrafo) che contiene [inizio, fine)."""
    sinistra = max((m.end() for m in confine.finditer(testo, 0, inizio)), default=0)
    destra = confine.search(testo, fine)
    return sinistra, destra.start() if destra else len(testo)


def frase_intorno(testo: str, inizio: int, fine: int) -> str:
    """La frase che contiene il tratto [inizio, fine): dal segno di fine frase
    precedente al successivo (punto, punto e virgola, riga vuota, cella,
    confine di uno shortcode)."""
    a, b = tratto_intorno(testo, inizio, fine, RE_FINE_FRASE)
    return testo[a:b]


def testo_confrontabile(sorgente: str) -> str:
    """Toglie tag HTML ed enfasi Markdown senza spostare le posizioni."""
    pulito = RE_TAG.sub(lambda m: " " * len(m.group(0)), sorgente)
    return pulito.replace("*", " ").replace("\xa0", " ")


def file_del_perimetro() -> list[Path]:
    trovati: set[Path] = set()
    for cartella, schema in PERIMETRO:
        base = ROOT / cartella
        if base.is_dir():
            trovati.update(p for p in base.rglob(schema) if p.is_file())
    return sorted(trovati)


def escluso(rel: str, extra: list[str]) -> bool:
    return any(fnmatch(rel, schema) for schema in ESCLUSI + extra)


def main(argv: list[str]) -> int:
    registro = yaml.safe_load(REGISTRO.read_text(encoding="utf-8"))
    dati = registro.get("dati") or []

    if argv:
        files = [Path(a).resolve() for a in argv if Path(a).is_file()]
    else:
        files = file_del_perimetro()

    trovate = 0
    for percorso in files:
        try:
            rel = percorso.relative_to(ROOT).as_posix()
        except ValueError:
            continue
        sorgente = percorso.read_text(encoding="utf-8", errors="replace")
        testo = testo_confrontabile(sorgente)
        for dato in dati:
            if escluso(rel, dato.get("escludi") or []):
                continue
            for regola in dato.get("vietati") or []:
                contesto = regola.get("contesto")
                finestra = int(regola.get("finestra", 200))
                for m in re.finditer(regola["regex"], testo):
                    if contesto:
                        if regola.get("stessa_frase"):
                            intorno = frase_intorno(testo, m.start(), m.end())
                        elif regola.get("stesso_paragrafo"):
                            a, b = tratto_intorno(testo, m.start(), m.end(), RE_FINE_PARAGRAFO)
                            intorno = testo[a:b]
                        else:
                            intorno = testo[max(0, m.start() - finestra): m.end() + finestra]
                        if not re.search(contesto, intorno):
                            continue
                    salvo = regola.get("salvo_se_frase")
                    if salvo:
                        a, b = tratto_intorno(testo, m.start(), m.end(), RE_FINE_FRASE)
                        # La variante stessa non conta: «Osservatorio Vesuviano»
                        # contiene già la parola che renderebbe legittima la frase.
                        if re.search(salvo, testo[a: m.start()] + " " + testo[m.end(): b]):
                            continue
                    prima = regola.get("salvo_se_prima")
                    if prima:
                        a, _ = tratto_intorno(testo, m.start(), m.end(), RE_FINE_FRASE)
                        if re.search(prima, testo[a: m.start()], re.I):
                            continue
                    riga = testo.count("\n", 0, m.start()) + 1
                    estratto = " ".join(testo[max(0, m.start() - 60): m.end() + 60].split())
                    print(f"{rel}:{riga}: [{dato['id']}] «{m.group(0)}» — {regola['perche']}")
                    print(f"    … {estratto} …")
                    print(f"    valore canonico: {dato['valore']} (fonte: {dato['fonti'][0]['nome']})")
                    trovate += 1

    if trovate:
        print(f"\n{trovate} variante/i non allineate ai dati canonici di data/dati_canonici.yaml.")
    else:
        print(f"OK: {len(dati)} dati canonici, {len(files)} file controllati, nessuna variante sbagliata.")
    return min(trovate, 125)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
