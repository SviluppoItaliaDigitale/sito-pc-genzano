#!/usr/bin/env python3
"""Controlla che le righe statiche della matrice «Stato del territorio» siano verificate di recente.

La pagina /stato-del-territorio/ (data/stato_territorio.yaml, shortcode matrice-territorio)
marca «verifica da rinnovare» le righe statiche verificate più di 60 giorni fa. Nato il
14/11/2026: quattro righe erano ferme al 14/09 e nessun controllo lo aveva segnalato prima
che lo vedesse l'utente. Questo script avvisa PRIMA della scadenza (soglia predefinita 50
giorni), così la riverifica si fa mentre la pagina è ancora in regola.

Uso:  python3 scripts/check-stato-territorio.py [--giorni 50]
Exit code: numero di righe da riverificare (0 = tutto a posto), 100 = file illeggibile.
Solo libreria standard: legge il YAML con espressioni regolari (campi id, dinamico, verificato).
"""
import argparse
import datetime as dt
import os
import re
import sys
from zoneinfo import ZoneInfo

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE = os.path.join(RADICE, "data", "stato_territorio.yaml")
SCADENZA = 60  # la soglia dello shortcode matrice-territorio


def righe(testo):
    blocchi = re.split(r"^\s*-\s+id:\s*", testo, flags=re.M)[1:]
    for b in blocchi:
        rid = b.split("\n", 1)[0].strip().strip('"')
        dinamico = re.search(r"^\s*dinamico:\s*\"?([\w-]+)", b, re.M)
        ver = re.search(r"^\s*verificato:\s*\"?(\d{4}-\d\d-\d\d)", b, re.M)
        yield rid, dinamico.group(1) if dinamico else None, ver.group(1) if ver else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--giorni", type=int, default=50)
    a = ap.parse_args()
    try:
        testo = open(FILE, encoding="utf-8").read()
    except OSError as e:
        print(f"ERRORE: {FILE} non si legge ({e})")
        return 100
    oggi = dt.datetime.now(ZoneInfo("Europe/Rome")).date()
    da_fare, n = [], 0
    for rid, dinamico, ver in righe(testo):
        n += 1
        if dinamico == "allerta":
            continue  # si ridata da sola dai dati dell'allerta
        if not ver:
            da_fare.append(f"  - {rid}: manca il campo «verificato»")
            continue
        eta = (oggi - dt.date.fromisoformat(ver)).days
        if eta > a.giorni:
            stato = "già marcata «verifica da rinnovare»" if eta > SCADENZA else f"scade fra {SCADENZA - eta} giorni"
            da_fare.append(f"  - {rid}: verificata il {ver}, {eta} giorni fa ({stato})")
    if n == 0:
        print("ERRORE: nessuna riga trovata in data/stato_territorio.yaml")
        return 100
    if da_fare:
        print(f"Righe di /stato-del-territorio/ da riverificare sulle fonti (soglia {a.giorni} giorni):")
        print("\n".join(da_fare))
    else:
        print(f"OK: {n} righe, nessuna verificata da più di {a.giorni} giorni.")
    return len(da_fare)


if __name__ == "__main__":
    sys.exit(min(main(), 100))
