#!/usr/bin/env python3
"""Valida i blocchi JSON-LD dell'output di build Hugo (gate PR).

Protegge il livello di dati strutturati del sito — in particolare il
blocco di paternità/licenza di jsonld-copyright.html (fonte unica
dell'entità di pagina Article/WebPage, agosto 2026) — dalle regressioni
di template: l'escaping dentro <script type="application/ld+json"> è
delicato (serve `| jsonify | safeJS`, incidente del doppio escape del
12 maggio 2026) e un errore produce JSON non parsabile che i validatori
Google scartano in silenzio.

Per ogni pagina del campione verifica che:
  1. ogni blocco <script type="application/ld+json"> sia JSON parsabile;
  2. esista almeno un blocco con `copyrightHolder` (il JSON-LD di
     paternità: se sparisce, la tutela IP è regredita).

Uso:  python3 scripts/check-jsonld.py [dir-build]   (default: public)
Exit code = numero di pagine con problemi. Solo stdlib.
"""
import glob
import json
import re
import sys

BUILD_DIR = sys.argv[1] if len(sys.argv) > 1 else "public"

# Campione: home, pagina statica, FAQ (FAQPage), articoli (Article, i 2
# più recenti), manuale (Article accademico), traduzione (inLanguage).
# /lanterna/ è esclusa by design (standalone, non usa baseof.html).
def campione():
    pagine = [
        f"{BUILD_DIR}/index.html",
        f"{BUILD_DIR}/chi-siamo/index.html",
        f"{BUILD_DIR}/faq/index.html",
        f"{BUILD_DIR}/facile-da-leggere/en/index.html",
    ]
    articoli = sorted(glob.glob(f"{BUILD_DIR}/comunicazioni/2*/index.html"))
    pagine += articoli[-2:]
    manuale = sorted(glob.glob(f"{BUILD_DIR}/manuale/0*/index.html"))
    pagine += manuale[:1]
    return pagine

# Il minificatore Hugo può togliere le virgolette dell'attributo type.
RX_LDJSON = re.compile(
    r'<script type="?application/ld\+json"?>(.*?)</script>', re.S
)

def main():
    errori = 0
    for pagina in campione():
        try:
            html = open(pagina, encoding="utf-8").read()
        except OSError as e:
            print(f"[FAIL] {pagina}: pagina attesa nel campione ma assente ({e})")
            errori += 1
            continue
        blocchi = RX_LDJSON.findall(html)
        problemi = []
        con_paternita = False
        for i, blocco in enumerate(blocchi, 1):
            try:
                dati = json.loads(blocco)
            except json.JSONDecodeError as e:
                problemi.append(f"blocco {i}: JSON non parsabile ({e})")
                continue
            if isinstance(dati, dict) and "copyrightHolder" in dati:
                con_paternita = True
        if not blocchi:
            problemi.append("nessun blocco JSON-LD trovato")
        elif not con_paternita:
            problemi.append(
                "manca il blocco di paternità (copyrightHolder) — "
                "regressione di jsonld-copyright.html"
            )
        rel = pagina.replace(BUILD_DIR, "") or "/"
        if problemi:
            errori += 1
            print(f"[FAIL] {rel}")
            for p in problemi:
                print(f"       - {p}")
        else:
            print(f"[ok]   {rel}  ({len(blocchi)} blocchi JSON-LD validi, paternità presente)")
    if errori:
        print(f"\nJSON-LD: {errori} pagine con problemi.")
    else:
        print("\nJSON-LD: tutti i blocchi del campione sono validi.")
    return errori

if __name__ == "__main__":
    sys.exit(main())
