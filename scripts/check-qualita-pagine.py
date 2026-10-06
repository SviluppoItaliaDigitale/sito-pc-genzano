#!/usr/bin/env python3
"""
Controllo qualità delle pagine del sito compilato (public/), pagina per pagina.

Nasce il 06/10/2026 dalla proposta «controllo qualità prima della
pubblicazione». Gli altri controlli guardano un campione (axe su 11 pagine) o
un aspetto solo (ancore, canonical, JSON-LD); questo passa TUTTE le pagine HTML
e verifica le cose che un lettore nota per prime:

  Bloccanti (exit 1):
    - pagina senza <title> o con titolo vuoto;
    - pagina senza <h1>;
    - <img> senza attributo alt (WCAG 1.1.1: alt="" va bene per le immagini
      decorative, l'attributo assente no).
  Avvisi (non bloccano):
    - più di un <h1> nella stessa pagina (fuori dalle eccezioni dichiarate);
    - due pagine con lo stesso titolo (paginazioni escluse).

Si saltano le pagine di rimando (meta refresh), i file di verifica dei motori,
i pacchetti «Stampa tutto» (raccolte di schede, un h1 per scheda), pagefind e
vendor. Il contenuto dei <script> e degli <template> non conta: l'HTML scritto
dentro una stringa JavaScript non è un elemento della pagina.

Uso:
    python3 scripts/check-qualita-pagine.py [public]
Solo libreria standard.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

SALTA_CARTELLE = ("pagefind/", "vendor/", "formazione/schede-stampabili/pacchetti/")
# Pagine che hanno più di un h1 per costruzione.
PIU_H1_AMMESSI = {
    "manuale/versione-stampabile/index.html",  # il libro intero: un h1 per capitolo
}
PAGINAZIONE = re.compile(r"/page/\d+/index\.html$")


class Lettore(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.dentro_script = 0
        self.h1 = 0
        self.img_senza_alt: list[str] = []
        self.titolo: list[str] = []
        self.in_title = False
        self.refresh = False

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): v for k, v in attrs}
        if tag in ("script", "template", "noscript"):
            self.dentro_script += 1
            return
        if self.dentro_script:
            return
        if tag == "h1":
            self.h1 += 1
        elif tag == "img" and "alt" not in a:
            self.img_senza_alt.append(a.get("src") or "(senza src)")
        elif tag == "title":
            self.in_title = True
        elif tag == "meta" and (a.get("http-equiv") or "").lower() == "refresh":
            self.refresh = True

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag in ("script", "template", "noscript"):
            self.dentro_script -= 1

    def handle_endtag(self, tag):
        if tag in ("script", "template", "noscript") and self.dentro_script:
            self.dentro_script -= 1
        elif tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.titolo.append(data)


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "public")
    if not root.is_dir():
        print(f"{root}/ non esiste: esegui prima la build Hugo.", file=sys.stderr)
        return 2
    errori: list[str] = []
    avvisi: list[str] = []
    titoli: dict[str, list[str]] = defaultdict(list)
    pagine = 0
    for f in sorted(root.rglob("*.html")):
        rel = f.relative_to(root).as_posix()
        if rel.startswith(SALTA_CARTELLE) or re.fullmatch(r"google[0-9a-f]+\.html", rel):
            continue
        p = Lettore()
        p.feed(f.read_text(encoding="utf-8", errors="replace"))
        if p.refresh:
            continue
        pagine += 1
        titolo = " ".join("".join(p.titolo).split())
        if not titolo:
            errori.append(f"{rel}: manca il titolo della pagina (<title>)")
        elif not PAGINAZIONE.search(rel):
            titoli[titolo].append(rel)
        if p.h1 == 0:
            errori.append(f"{rel}: manca il titolo principale (<h1>)")
        elif p.h1 > 1 and rel not in PIU_H1_AMMESSI:
            avvisi.append(f"{rel}: {p.h1} titoli principali (<h1>), ne serve uno")
        for src in p.img_senza_alt:
            errori.append(f"{rel}: immagine senza testo alternativo (alt): {src[:90]}")
    for t, rels in titoli.items():
        if len(rels) > 1:
            avvisi.append(f"stesso titolo «{t[:80]}» su {len(rels)} pagine: " + ", ".join(rels[:4]))

    print(f"Pagine controllate: {pagine}")
    for a in avvisi:
        print(f"⚠️  {a}")
    for e in errori:
        print(f"❌ {e}")
    if errori:
        print(f"\n{len(errori)} errori bloccanti, {len(avvisi)} avvisi.")
        return 1
    print(f"✅ Nessun errore bloccante ({len(avvisi)} avvisi).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
