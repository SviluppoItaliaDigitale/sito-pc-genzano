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

# Domini istituzionali. Due livelli, entrambi da tenere aggiornati quando il
# sito comincia a citare un ente nuovo (revisione del 26/09/2026: la prima
# versione lasciava fuori Vigili del Fuoco, ARPA Lazio, ASL Roma 6, INAIL).
#
# 1) Suffissi e schemi che identificano da soli un soggetto pubblico.
SCHEMI_PUBBLICI = re.compile(
    r"(\.gov\.it|\.europa\.eu|\.gov|\.gov\.uk|\.int|\.un\.org|^un\.org|\.edu\.it"
    r"|(^|\.)regione\.[a-z-]+\.it|(^|\.)provincia\.[a-z-]+\.it"
    r"|(^|\.)comune\.[a-z-]+\.[a-z.]+|(^|\.)protezionecivile\.[a-z-]+\.it"
    r"|(^|\.)(asl|ausl|ats|asst|aou|arpa|areu)[a-z0-9-]*\.[a-z.]*it)$"
)
# 2) Enti pubblici con dominio proprio, che nessuno schema riconosce.
#    Vale anche per i sottodomini (es. opendata.vigilfuoco.it).
ENTI_PUBBLICI = {
    # Stato, organi e autorità
    "normattiva.it", "gazzettaufficiale.it", "camera.it", "senato.it",
    "quirinale.it", "cortecostituzionale.it", "garanteprivacy.it", "arera.it",
    "designers.italia.it", "prefettura.it", "beniculturali.it", "minambiente.it",
    # Protezione civile e soccorso
    "protezionecivile.it", "iononrischio.it", "it-alert.it", "vigilfuoco.it",
    "112lazio.it", "areu.lombardia.it", "commissariatodips.it",
    # Forze dell'ordine e Difesa
    "poliziadistato.it", "carabinieri.it", "meteoam.it",
    # Enti di ricerca e agenzie
    "ingv.it", "cnr.it", "istat.it", "iss.it", "isprambiente.it", "snpambiente.it",
    "enea.it", "inaf.it", "asi.it", "isinucleare.it", "agenziaitaliameteo.it",
    "inail.it", "inps.it", "centronazionalesangue.it",
    # Territorio
    "arpalazio.it", "aslroma6.it", "cittametropolitanaroma.it",
    "parcocastelliromani.it", "parchilazio.it",
    "autoritadistrettoappenninocentrale.it", "autoritabacino.it",
}


def istituzionale(host: str) -> bool:
    host = host.lower().removeprefix("www.")
    if SCHEMI_PUBBLICI.search(host):
        return True
    return any(host == d or host.endswith("." + d) for d in ENTI_PUBBLICI)


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
        if istituzionale(host):
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
