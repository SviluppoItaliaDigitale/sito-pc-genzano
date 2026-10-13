#!/usr/bin/env python3
"""File .ics del «Calendario della prevenzione».

Legge data/calendario_prevenzione.yaml e scrive
static/calendario-prevenzione/calendario-prevenzione.ics, il file che la
pagina /calendario-prevenzione/ offre da scaricare o da sottoscrivere:

  - un promemoria per ogni mese, il primo sabato, con i gesti del mese;
  - i promemoria a data fissa (cambio dell'ora a marzo e a ottobre, Giornata
    internazionale per la riduzione del rischio di disastri).

Gli eventi durano un giorno intero, si ripetono ogni anno (RRULE) e hanno un
avviso alle 9 del mattino, come il promemoria del piano familiare. Il file è
deterministico: identificativi stabili e DTSTAMP preso dal campo «aggiornato»
del file dati, così due esecuzioni sugli stessi dati danno lo stesso file.
Scrittura secondo RFC 5545: righe CRLF ripiegate a 75 byte, testo con
caratteri speciali protetti.

Uso:
  python3 scripts/genera-calendario-prevenzione.py          # scrive il file
  python3 scripts/genera-calendario-prevenzione.py --check  # esce 1 se non è aggiornato
Richiede PyYAML. Nato il 14/10/2026 (proposta 20 della roadmap).
"""
from __future__ import annotations

import argparse
import calendar
import datetime as dt
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATI = ROOT / "data" / "calendario_prevenzione.yaml"
OUT = ROOT / "static" / "calendario-prevenzione" / "calendario-prevenzione.ics"
SITO = "https://www.protezionecivilegenzano.it"
PAGINA = SITO + "/calendario-prevenzione/"
DOMINIO_UID = "protezionecivilegenzano.it"
# Anno della prima occorrenza: gli eventi si ripetono ogni anno da qui.
ANNO_BASE = 2026
SABATO = 5
GIORNI_ICS = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]


def esc(testo: str) -> str:
    """Testo di una proprietà iCalendar (RFC 5545, 3.3.11)."""
    return (str(testo).replace("\\", "\\\\").replace(";", "\\;")
            .replace(",", "\\,").replace("\r\n", "\\n").replace("\n", "\\n"))


def ripiega(riga: str) -> str:
    """Righe di al massimo 75 byte, senza spezzare i caratteri UTF-8."""
    out, corrente, lung = [], "", 0
    for car in riga:
        b = len(car.encode("utf-8"))
        limite = 75 if not out else 74  # le righe di continuazione iniziano con uno spazio
        if lung + b > limite:
            out.append(corrente)
            corrente, lung = car, b
        else:
            corrente += car
            lung += b
    out.append(corrente)
    return "\r\n ".join(out)


def primo(anno: int, mese: int, giorno_settimana: int) -> dt.date:
    d = dt.date(anno, mese, 1)
    while d.weekday() != giorno_settimana:
        d += dt.timedelta(days=1)
    return d


def ultima_domenica(anno: int, mese: int) -> dt.date:
    d = dt.date(anno, mese, calendar.monthrange(anno, mese)[1])
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def url(pagina: str) -> str:
    return SITO + pagina if pagina.startswith("/") else pagina


def evento(uid: str, inizio: dt.date, rrule: str, titolo: str, descrizione: str,
           collegamento: str, avviso: str, stamp: str) -> list[str]:
    fine = inizio + dt.timedelta(days=1)
    return [
        "BEGIN:VEVENT",
        f"UID:{uid}@{DOMINIO_UID}",
        f"DTSTAMP:{stamp}",
        f"DTSTART;VALUE=DATE:{inizio:%Y%m%d}",
        f"DTEND;VALUE=DATE:{fine:%Y%m%d}",
        f"RRULE:{rrule}",
        f"SUMMARY:{esc(titolo)}",
        f"DESCRIPTION:{esc(descrizione)}",
        f"URL:{collegamento}",
        "TRANSP:TRANSPARENT",
        "BEGIN:VALARM",
        "ACTION:DISPLAY",
        f"DESCRIPTION:{esc(avviso)}",
        "TRIGGER:PT9H",
        "END:VALARM",
        "END:VEVENT",
    ]


def costruisci(dati: dict) -> str:
    aggiornato = dt.date.fromisoformat(str(dati["aggiornato"]))
    stamp = f"{aggiornato:%Y%m%d}T000000Z"
    righe = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Protezione Civile Genzano di Roma//Calendario della prevenzione//IT",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:" + esc("Calendario della prevenzione — Protezione Civile Genzano"),
        "X-WR-CALDESC:" + esc("Un promemoria al mese con i gesti di prevenzione per chi vive a "
                              "Genzano di Roma, più il controllo del kit al cambio dell'ora. "
                              "Calendario completo: " + PAGINA),
        "REFRESH-INTERVAL;VALUE=DURATION:P1W",
        "X-PUBLISHED-TTL:P1W",
    ]
    for n, mese in enumerate(dati["mesi"], start=1):
        gesti = "\n".join(f"- {g['testo']} {url(g['pagina'])}" for g in mese["gesti"])
        descr = (f"{mese['titolo']}.\n{gesti}\n\n"
                 f"Calendario completo: {PAGINA}#mese-{mese['id']}\n"
                 "In emergenza chiama il 112.")
        inizio = primo(ANNO_BASE, n, SABATO)
        righe += evento(
            uid=f"calendario-prevenzione-{mese['id']}",
            inizio=inizio,
            rrule=f"FREQ=YEARLY;BYMONTH={n};BYDAY=1{GIORNI_ICS[SABATO]}",
            titolo=f"Prevenzione di {mese['nome'].lower()}: {mese['titolo'][0].lower()}{mese['titolo'][1:]}",
            descrizione=descr,
            collegamento=f"{PAGINA}#mese-{mese['id']}",
            avviso=f"I gesti di prevenzione di {mese['nome'].lower()}",
            stamp=stamp,
        )
    for p in dati["promemoria"]:
        m = int(p["mese"])
        if p["giorno"] == "ultima-domenica":
            inizio = ultima_domenica(ANNO_BASE, m)
            rrule = f"FREQ=YEARLY;BYMONTH={m};BYDAY=-1SU"
        else:
            inizio = dt.date(ANNO_BASE, m, int(p["giorno"]))
            rrule = "FREQ=YEARLY"
        descr = f"{p['testo']}\n{p['etichetta']}: {url(p['pagina'])}\n\nIn emergenza chiama il 112."
        righe += evento(
            uid=f"calendario-prevenzione-{p['id']}",
            inizio=inizio,
            rrule=rrule,
            titolo=p["titolo"],
            descrizione=descr,
            collegamento=url(p["pagina"]),
            avviso=p["titolo"],
            stamp=stamp,
        )
    righe.append("END:VCALENDAR")
    return "".join(ripiega(r) + "\r\n" for r in righe)


def controlla(dati: dict) -> list[str]:
    """Campi obbligatori e pagine che devono esistere nel sito."""
    errori = []
    if len(dati.get("mesi", [])) != 12:
        errori.append("servono 12 mesi in ordine, da gennaio a dicembre")
    voci = [g for m in dati.get("mesi", []) for g in m.get("gesti", [])] + dati.get("promemoria", [])
    for v in voci:
        for campo in ("testo", "pagina", "etichetta"):
            if not v.get(campo):
                errori.append(f"voce senza «{campo}»: {v}")
        pagina = str(v.get("pagina", "")).split("#", 1)[0]
        if pagina.startswith("/"):
            percorso = pagina.strip("/")
            candidati = [ROOT / "content" / percorso / "_index.md",
                         ROOT / "content" / (percorso + ".md"),
                         ROOT / "static" / percorso / "index.html"]
            if not any(c.exists() for c in candidati):
                errori.append(f"pagina inesistente: {pagina}")
    for p in dati.get("promemoria", []):
        if p.get("giorno") != "ultima-domenica" and not str(p.get("giorno", "")).isdigit():
            errori.append(f"promemoria {p.get('id')}: «giorno» deve essere un numero o «ultima-domenica»")
    return errori


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="non scrive: esce 1 se il file non è aggiornato")
    args = ap.parse_args()

    dati = yaml.safe_load(DATI.read_text(encoding="utf-8"))
    errori = controlla(dati)
    if errori:
        for e in errori:
            print(f"ERRORE: {e}", file=sys.stderr)
        return 1
    testo = costruisci(dati)
    attuale = OUT.read_bytes().decode("utf-8") if OUT.exists() else ""
    if args.check:
        if attuale != testo:
            print("Il file del calendario non corrisponde a data/calendario_prevenzione.yaml: "
                  "esegui python3 scripts/genera-calendario-prevenzione.py e committa.", file=sys.stderr)
            return 1
        print("Calendario della prevenzione aggiornato.")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(testo.encode("utf-8"))
    print(f"Scritto {OUT.relative_to(ROOT)} ({len(testo.encode('utf-8'))} byte).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
