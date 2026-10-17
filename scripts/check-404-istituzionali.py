#!/usr/bin/env python3
"""Legge il rapporto markdown di lychee e fallisce se un link del sito risponde
404 o 410, qualunque sia il dominio. I link verso gli enti pubblici sono
elencati per primi, perché sono le fonti ufficiali promesse al cittadino.

Dal 17/10/2026 (istruzione dell'utente: «gli errori 404 e simili non devono
mai essere ignorati e devono essere risolti... vale per tutti i link del
sito») il run diventa rosso per ogni 404/410, non più solo per quelli
istituzionali: un link rotto verso un sito di terzi è comunque una promessa
non mantenuta. Timeout, 5xx e anti-bot restano fuori: sono passeggeri e li
riporta già l'issue di lychee.

Perché: il crawl settimanale di check-links-sito.yml gira con `fail: false`,
perché molti errori esterni sono passeggeri (timeout, 5xx, anti-bot). Un 404
di un ente pubblico invece è quasi sempre una pagina spostata: il cittadino
che segue il link dal nostro sito trova una pagina d'errore dove gli avevamo
promesso la fonte ufficiale. Audit esterno del 25/09/2026, rilievo F13: 58 URL
in 404, 26 verso il Dipartimento della Protezione Civile.

Uso:  python3 scripts/check-404-istituzionali.py lychee-report.md
Exit: 0 se nessun link in 404/410, 1 altrimenti (elenco su stdout), 2 se il
      rapporto manca (lychee non ha girato).
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
        # Un rapporto assente vuol dire che lychee non ha girato (argomenti
        # sbagliati, crash): il controllo non è stato fatto, non è «tutto ok».
        print(f"Rapporto {percorso} assente: il controllo dei link non è stato eseguito.")
        return 2
    trovati = sorted(set(RIGA.findall(testo)))
    if not trovati:
        print("Nessun link in 404/410.")
        return 0
    pubblici = [(c, u) for c, u in trovati if istituzionale((urlparse(u).hostname or "").lower())]
    altri = [t for t in trovati if t not in pubblici]
    print(f"{len(trovati)} link in 404/410 ({len(pubblici)} verso enti pubblici):")
    for titolo, gruppo in (("Enti pubblici", pubblici), ("Altri siti e pagine del sito", altri)):
        if gruppo:
            print(f"\n{titolo}:")
            for codice, url in gruppo:
                print(f"  {codice}  {url}")
    print("\nCerca la pagina attuale sulla fonte, verificala con una richiesta reale e"
          " sostituisci l'URL in tutti i file sorgente (content/, static/, themes/, data/);"
          " se la pagina non esiste più, punta alla sezione che la contiene o togli il"
          " link lasciando il testo.")
    return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "lychee-report.md"))
