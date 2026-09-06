#!/usr/bin/env python3
"""
Ancore interne e link speciali nell'HTML generato (public/).

Nasce dall'audit esterno del 06/09/2026 (rilievi F16 e F21): 17 rimandi a
frammenti (#kit-casa, #disponibilita-pcto, #inclusione-e-accessibilita…)
puntavano a id che i titoli non generano più (Hugo conserva le lettere
accentate negli id automatici), e il corpo dell'e-mail di condivisione era
codificato due volte (%250A). Il controllo dei link (lychee) non verifica
i frammenti: questo script sì.

Controlli sull'output della build:
  - ogni href con #frammento verso una pagina del sito deve trovare un
    elemento con quell'id (o <a name>) nella pagina di destinazione;
  - i link mailto: non devono contenere sequenze codificate due volte (%25XX).

Esclusi: frammenti-parametro (contengono "=", solo numerici, o sulle pagine
strumento che leggono l'hash via JavaScript: cruscotto/terremoto, monitor,
assistente, lanterna) e destinazioni inesistenti (le copre lychee).

Uso:
  python3 scripts/check-ancore.py public [--base-path /sito-pc-genzano]
Exit code = numero di errori.
"""

from __future__ import annotations

import argparse
import posixpath
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

PAGINE_HASH_JS = ("/cruscotto/terremoto/", "/monitor/", "/assistente/", "/lanterna/", "/cerca/", "/comunicazioni/")


class Raccoglitore(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        d = dict(attrs)
        if d.get("id"):
            self.ids.add(d["id"])
        if tag == "a" and d.get("name"):
            self.ids.add(d["name"])
        if tag == "a" and d.get("href"):
            self.hrefs.append(d["href"])


def indicizza(public: Path) -> dict[str, Raccoglitore]:
    pagine: dict[str, Raccoglitore] = {}
    for html in public.rglob("*.html"):
        r = Raccoglitore()
        try:
            r.feed(html.read_text(encoding="utf-8", errors="replace"))
        except Exception:  # noqa: BLE001
            continue
        pagine[str(html.relative_to(public))] = r
    return pagine


def normalizza_destinazione(href_path: str, pagina_corrente: str, base_path: str) -> str | None:
    """Ritorna il percorso relativo a public/ del file HTML di destinazione."""
    if not href_path:
        return pagina_corrente
    if href_path.startswith("/"):
        p = href_path
        if base_path and p.startswith(base_path + "/"):
            p = p[len(base_path):]
        elif base_path and p == base_path:
            p = "/"
    else:
        p = posixpath.normpath(posixpath.join("/" + posixpath.dirname(pagina_corrente), href_path))
    p = unquote(p)
    if p.endswith("/"):
        p += "index.html"
    elif not p.endswith(".html"):
        p += "/index.html"
    return p.lstrip("/")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("public", help="cartella dell'output Hugo")
    ap.add_argument("--base-path", default="/sito-pc-genzano", help="sottopercorso del baseURL da scartare (GitHub Pages)")
    args = ap.parse_args()

    public = Path(args.public)
    pagine = indicizza(public)
    errori: list[str] = []
    verificati = 0
    visti: set[tuple[str, str]] = set()

    for nome, r in pagine.items():
        for href in r.hrefs:
            if href.startswith("mailto:"):
                if re.search(r"%25[0-9A-Fa-f]{2}", href):
                    chiave = (nome, "mailto")
                    if chiave not in visti:
                        visti.add(chiave)
                        errori.append(f"{nome}: link mailto codificato due volte ({href[:80]}…)")
                continue
            if "#" not in href or href.startswith(("http://", "https://", "tel:", "javascript:")):
                continue
            parti = urlsplit(href)
            frammento = unquote(parti.fragment)
            if not frammento or "=" in frammento or frammento.isdigit():
                continue
            dest = normalizza_destinazione(parti.path, nome, args.base_path)
            if dest is None:
                continue
            if any(("/" + dest).startswith(p) or ("/" + dest).replace("index.html", "") == p for p in PAGINE_HASH_JS):
                continue
            target = pagine.get(dest)
            if target is None:
                continue  # pagina inesistente: la segnala lychee
            verificati += 1
            if frammento not in target.ids:
                chiave = (dest, frammento)
                if chiave not in visti:
                    visti.add(chiave)
                    errori.append(f"{nome} → {href}: nessun id \"{frammento}\" in {dest}")

    print(f"Pagine indicizzate: {len(pagine)}; ancore verificate: {verificati}")
    if errori:
        print(f"\n❌ {len(errori)} ancore o link speciali difettosi:")
        for e in errori:
            print(f"  - {e}")
    else:
        print("✅ Tutte le ancore interne puntano a un id esistente; nessun mailto codificato due volte.")
    return len(errori)


if __name__ == "__main__":
    sys.exit(main())
