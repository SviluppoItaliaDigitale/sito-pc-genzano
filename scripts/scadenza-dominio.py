#!/usr/bin/env python3
"""Giorni alla scadenza della registrazione del dominio .it del sito.

Interroga il servizio whois del registro italiano (whois.nic.it, porta 43;
il registro .it non pubblica un servizio RDAP nell'elenco IANA) e legge il
campo «Expire Date: AAAA-MM-GG». Stampa i giorni rimasti e la data; se il
registro non risponde o il campo manca stampa un avviso su stderr ed esce
con codice 1, senza mai far fallire chi lo chiama per un guasto di rete.

Uso: python3 scripts/scadenza-dominio.py [dominio]
Lo usa il controllo di salute giornaliero in aggiorna-stato-sistema.yml.
"""

import datetime as dt
import re
import socket
import sys

DOMINIO = "protezionecivilegenzano.it"
SERVER = "whois.nic.it"


def leggi_whois(dominio: str) -> str:
    with socket.create_connection((SERVER, 43), timeout=20) as s:
        s.sendall(dominio.encode("ascii") + b"\r\n")
        dati = b""
        while True:
            pezzo = s.recv(4096)
            if not pezzo:
                break
            dati += pezzo
    return dati.decode("utf-8", "replace")


def main() -> int:
    dominio = sys.argv[1] if len(sys.argv) > 1 else DOMINIO
    try:
        testo = leggi_whois(dominio)
    except OSError as e:
        print(f"whois non raggiungibile: {e}", file=sys.stderr)
        return 1
    m = re.search(r"^Expire Date:\s*(\d{4}-\d{2}-\d{2})", testo, re.M)
    if not m:
        print("campo Expire Date assente nella risposta del registro", file=sys.stderr)
        return 1
    scadenza = dt.date.fromisoformat(m.group(1))
    giorni = (scadenza - dt.date.today()).days
    print(f"{giorni} {scadenza.isoformat()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
