#!/usr/bin/env python3
"""
Le date di ultima modifica (GitInfo) della build sono quelle di sempre?

Dall'11/11/2026 deploy.yml scarica la storia di git senza i contenuti dei
file vecchi (`filter: blob:none`), per un checkout più rapido. Hugo legge le
date con `git log --name-only` e `diff.renames=0`, che non ha bisogno di quei
contenuti; se un giorno non fosse più così, le date `lastmod` cambierebbero
in massa e ogni pagina verrebbe ricaricata. Questo controllo confronta la
sitemap della build con quella servita dal sito: se cambiano le date di
molte pagine insieme, lo dice nel riepilogo del run (avviso, non blocca).

Uso: python3 scripts/controlla-lastmod.py public/sitemap.xml [--soglia 40]
Solo Python standard. Exit 0 sempre (salvo errori d'uso).
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from pathlib import Path

URL = "https://www.protezionecivilegenzano.it/sitemap.xml"


def date(xml: str) -> dict[str, str]:
    voci = re.findall(r"<url>(.*?)</url>", xml, re.S)
    out = {}
    for v in voci:
        loc = re.search(r"<loc>(.*?)</loc>", v)
        lm = re.search(r"<lastmod>(.*?)</lastmod>", v)
        if loc and lm:
            out[loc.group(1).strip()] = lm.group(1).strip()
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sitemap")
    ap.add_argument("--url", default=URL)
    ap.add_argument("--soglia", type=int, default=40)
    a = ap.parse_args()
    locale = date(Path(a.sitemap).read_text(encoding="utf-8"))
    try:
        req = urllib.request.Request(a.url, headers={"User-Agent": "PCGenzanoControlloLastmod/1.0", "Cache-Control": "no-cache"})
        with urllib.request.urlopen(req, timeout=30) as r:
            servita = date(r.read().decode("utf-8", "replace"))
    except Exception as e:  # il sito che non risponde non è affare di questo controllo
        print(f"ℹ️  Sitemap servita non leggibile ({type(e).__name__}): confronto saltato.")
        return 0
    comuni = [u for u in locale if u in servita]
    diverse = [u for u in comuni if locale[u] != servita[u]]
    print(f"Date di ultima modifica: {len(diverse)} diverse su {len(comuni)} pagine in comune.")
    if len(diverse) > a.soglia:
        print(f"::warning::{len(diverse)} pagine hanno una data di ultima modifica diversa dalla sitemap servita: "
              "controllare che GitInfo legga ancora la storia di git (checkout con filter: blob:none).")
        for u in diverse[:10]:
            print(f"  {u}: {servita[u]} → {locale[u]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
