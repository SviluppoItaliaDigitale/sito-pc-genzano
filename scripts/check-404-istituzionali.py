#!/usr/bin/env python3
"""Legge il rapporto markdown di lychee e fallisce se un link verso un dominio
istituzionale risponde 404 o 410.

Perché: il crawl settimanale di check-links-sito.yml gira con `fail: false`,
perché molti errori esterni sono passeggeri (timeout, 5xx, anti-bot). Un 404
di un ente pubblico invece è quasi sempre una pagina spostata: il cittadino
che segue il link dal nostro sito trova una pagina d'errore dove gli avevamo
promesso la fonte ufficiale. Audit esterno del 25/09/2026, rilievo F13: 58 URL
in 404, 26 verso il Dipartimento della Protezione Civile.

Uso:  python3 scripts/check-404-istituzionali.py lychee-report.md
Exit: 0 se nessun 404 istituzionale, 1 altrimenti (elenco su stdout).
"""
import re
import sys
from urllib.parse import urlparse

# Domini istituzionali: enti pubblici italiani, UE e organismi internazionali.
ISTITUZIONALI = re.compile(
    r"(\.gov\.it|\.europa\.eu|\.gov|\.gov\.uk|\.int|\.un\.org|^un\.org"
    r"|regione\.[a-z-]+\.it|\.regione\.[a-z-]+\.it|comune\.[a-z-]+\.[a-z.]+"
    r"|ingv\.it|cnr\.it|istat\.it|normattiva\.it|gazzettaufficiale\.it"
    r"|camera\.it|senato\.it|quirinale\.it|cortecostituzionale\.it"
    r"|protezionecivile\.it|iononrischio\.it|it-alert\.it)$"
)
RIGA = re.compile(r"\[(404|410)\][^\n]*?(https?://[^\s<>|)\]]+)")


def main(percorso: str) -> int:
    try:
        testo = open(percorso, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"Rapporto {percorso} assente: nulla da controllare.")
        return 0
    trovati = []
    for codice, url in RIGA.findall(testo):
        host = (urlparse(url).hostname or "").lower()
        if ISTITUZIONALI.search(host):
            trovati.append((codice, url))
    trovati = sorted(set(trovati))
    if not trovati:
        print("Nessun 404 verso domini istituzionali.")
        return 0
    print(f"{len(trovati)} link istituzionali in 404/410:")
    for codice, url in trovati:
        print(f"  {codice}  {url}")
    print("\nCerca la pagina attuale sul sito dell'ente, verificala e sostituisci"
          " l'URL nei file sorgente (content/, static/, themes/, data/).")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "lychee-report.md"))
