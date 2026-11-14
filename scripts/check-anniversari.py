#!/usr/bin/env python3
"""Controlla che le ricorrenze di protezione civile escano nel loro giorno.

Legge data/anniversari.yaml (la fonte unica delle ricorrenze) e gli articoli di
content/comunicazioni/. Nato il 14/11/2026: l'articolo sul Polesine era
programmato per il giorno dopo l'anniversario, e la tabella degli anniversari del
piano editoriale aveva date sbagliate.

Segnala:
  MANCA      una ricorrenza entro la finestra (default 45 giorni) senza un articolo
             in uscita in uno dei suoi giorni, nell'anno di quella ricorrenza;
  FUORI DATA un articolo di ricorrenza (riconosciuto dalla «chiave») che esce o è
             programmato fra 1 e 20 giorni lontano dal giorno della ricorrenza;
  NON IN CAL un articolo con un evento storico datato nel titolo («14 novembre
             1951») che nessuna voce del calendario riconosce (solo con --tutto).

Uso:
  python3 scripts/check-anniversari.py                # prossimi 45 giorni
  python3 scripts/check-anniversari.py --giorni 90
  python3 scripts/check-anniversari.py --tutto        # anche archivio e titoli non registrati
  python3 scripts/check-anniversari.py --markdown     # rapporto per la issue
Exit code: numero di MANCA e di FUORI DATA futuri (0 = tutto a posto).
Gli articoli già usciti fuori data si segnalano solo con --tutto e non contano
nell'exit code: non si possono più spostare.
"""
import argparse
import datetime as dt
import glob
import os
import re
import sys
from zoneinfo import ZoneInfo

import yaml

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAL = os.path.join(RADICE, "data", "anniversari.yaml")
ART = os.path.join(RADICE, "content", "comunicazioni")
OGGI = dt.datetime.now(ZoneInfo("Europe/Rome")).date()
MESI = ("gennaio febbraio marzo aprile maggio giugno luglio agosto settembre "
        "ottobre novembre dicembre").split()
RE_EVENTO = re.compile(r"\b(\d{1,2})(?:°)?(?:\s*[-–]\s*\d{1,2})?\s+(" + "|".join(MESI)
                       + r")\s+(1[5-9]\d\d|20[0-4]\d)\b", re.I)


def leggi_articoli():
    articoli = []
    for f in sorted(glob.glob(os.path.join(ART, "*.md"))):
        nome = os.path.basename(f)[:-3]
        if nome.endswith("-facile") or not re.match(r"\d{4}-\d\d-\d\d-", nome):
            continue
        testo = open(f, encoding="utf-8").read()
        m = re.search(r"^date:\s*\"?(\d{4}-\d\d-\d\d)", testo, re.M)
        if not m:
            continue
        t = re.search(r"^title:\s*\"?(.*?)\"?\s*$", testo, re.M)
        articoli.append({"slug": nome[11:], "file": nome,
                         "data": dt.date.fromisoformat(m.group(1)),
                         "titolo": t.group(1) if t else ""})
    return articoli


def giorno(anno, mmgg):
    m, g = map(int, mmgg.split("-"))
    try:
        return dt.date(anno, m, g)
    except ValueError:  # 29 febbraio
        return dt.date(anno, m, 28)


def prossima(voce, da):
    """Prima occorrenza della ricorrenza da 'da' in poi (con i suoi giorni)."""
    for anno in (da.year, da.year + 1):
        giorni = [giorno(anno, x) for x in voce["giorni"]]
        if max(giorni) >= da:
            return giorni
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--giorni", type=int, default=45)
    ap.add_argument("--tutto", action="store_true")
    ap.add_argument("--markdown", action="store_true")
    a = ap.parse_args()

    voci = yaml.safe_load(open(CAL, encoding="utf-8"))["ricorrenze"]
    articoli = leggi_articoli()
    manca, fuori, fuori_passati, non_reg = [], [], [], []

    for v in voci:
        rx = re.compile(v["chiave"])
        suoi = [x for x in articoli if rx.search(x["slug"])]
        # Articoli della voce lontani 1-20 giorni da un giorno della ricorrenza.
        for x in suoi:
            gg = [giorno(x["data"].year, d) for d in v["giorni"]]
            scarto = min(abs((x["data"] - d).days) for d in gg)
            if 1 <= scarto <= 20:
                riga = (x, v, scarto)
                (fuori if x["data"] >= OGGI else fuori_passati).append(riga)
        # Ricorrenza entro la finestra senza articolo nel suo giorno.
        gg = prossima(v, OGGI)
        if gg and (min(gg) - OGGI).days <= a.giorni:
            if not any(x["data"] in gg for x in suoi):
                manca.append((v, gg))

    if a.tutto:
        chiavi = [re.compile(v["chiave"]) for v in voci]
        for x in articoli:
            m = RE_EVENTO.search(x["titolo"])
            if m and int(m.group(3)) < x["data"].year and not any(c.search(x["slug"]) for c in chiavi):
                non_reg.append(x)

    def gtesto(d):
        return f"{d.day} {MESI[d.month - 1]} {d.year}"

    out = []
    for v, gg in sorted(manca, key=lambda r: r[1][0]):
        out.append(f"MANCA      {gtesto(gg[0])}: {v['evento']} ({v['anno']}), nessun articolo in uscita quel giorno")
    for x, v, s in sorted(fuori, key=lambda r: r[0]["data"]):
        out.append(f"FUORI DATA {x['file']}: {v['evento']} ricorre il {' o '.join(v['giorni'])}, l'articolo esce {s} giorni lontano")
    if a.tutto:
        for x, v, s in sorted(fuori_passati, key=lambda r: r[0]["data"]):
            out.append(f"già uscito {x['file']}: {s} giorni lontano dalla ricorrenza ({v['evento']})")
        for x in non_reg:
            out.append(f"NON IN CAL {x['file']}: «{x['titolo'][:80]}» non è in data/anniversari.yaml")

    if a.markdown:
        print(f"Controllo del {gtesto(OGGI)}, finestra di {a.giorni} giorni.\n")
        print("\n".join(f"- {r}" for r in out) if out else "Nessun problema: ogni ricorrenza della finestra ha il suo articolo nel suo giorno.")
    else:
        print("\n".join(out) if out else f"OK: {len(voci)} ricorrenze, nessuna mancante nei prossimi {a.giorni} giorni, nessuna fuori data.")
    return len(manca) + len(fuori)


if __name__ == "__main__":
    sys.exit(min(main(), 100))
