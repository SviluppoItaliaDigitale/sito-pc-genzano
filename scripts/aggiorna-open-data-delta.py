#!/usr/bin/env python3
"""Aggiorna gli OPEN DATA degli interventi partendo da un export PARZIALE.

Complemento di genera-open-data-interventi.py, che ricalcola tutto da un
export CUMULATIVO (dall'adozione del gestionale). Quando l'export scaricato è
FILTRATO a un periodo (es. solo l'ultimo mese), quello script sovrascriverebbe
i totali pubblicati con un sottoinsieme, cancellando i mesi precedenti.

Questo script fa il contrario: prende i dataset GIÀ PUBBLICATI in
static/open-data/ e vi AGGIUNGE le sole righe nuove dell'export parziale
(il "delta"), con la stessa logica di aggregazione del generatore.

Uso:  python3 scripts/aggiorna-open-data-delta.py <export-parziale.xlsx> [--dry-run]
                                                   [--volontari-nuovi N]

Come riconosce le righe nuove
  - se il dataset pubblicato riporta `periodo.ultimo_numero` (es. "130/2026"),
    sono nuove le righe con numero di intervento maggiore: funziona anche se
    l'aggiornamento precedente si è fermato a metà giornata;
  - altrimenti (dataset generati prima di questa funzione) sono nuove le righe
    con Data Inizio successiva a `periodo.al`.

Indicatori NON additivi, trattati esplicitamente
  - "Automezzi impiegati (distinti)": il pubblicato non contiene le targhe;
    si conta come nuovo un automezzo la cui ETICHETTA (es. "M04 Evo (Pickup)")
    non compare nell'elenco automezzi-impiegati già pubblicato.
  - "Volontari con almeno un intervento": il pubblicato non contiene nomi. Un
    volontario delle righe nuove è considerato già conteggiato se compare anche
    in una riga PRECEDENTE dello stesso export parziale. Se qualcuno compare
    SOLO nelle righe nuove, lo script si ferma e chiede `--volontari-nuovi N`
    (quanti di loro sono davvero al primo intervento: lo sa solo chi conosce
    il Gruppo). Mai stimare: meglio fermarsi.
  - "Ore di intervento totali": il pubblicato è arrotondato al decimo; sommando
    il delta si eredita un'incertezza di ±0,1 h, che si azzera al primo export
    cumulativo. Documentato, non nascosto.

Guardie
  - se l'export copre già l'inizio del periodo pubblicato è CUMULATIVO: lo
    script rifiuta e rimanda a genera-open-data-interventi.py;
  - se non ci sono righe nuove non scrive nulla;
  - il file .xlsx NON va mai committato (contiene nomi).
"""
import argparse
import datetime
import importlib
import json
import os
import sys
from collections import Counter

try:
    import openpyxl
except ImportError:
    sys.exit("Serve openpyxl:  pip install --break-system-packages openpyxl")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
gen = importlib.import_module("genera-open-data-interventi")   # stessa logica
OUT = gen.OUT


def carica(nome):
    with open(os.path.join(OUT, nome + ".json"), encoding="utf-8") as fp:
        return json.load(fp)


def nomi(cella):
    return {n.strip() for n in str(cella or "").split("|") if n.strip()}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("xlsx", help="export PARZIALE del gestionale (.xlsx)")
    ap.add_argument("--dry-run", action="store_true",
                    help="mostra il delta e i nuovi totali senza scrivere")
    ap.add_argument("--volontari-nuovi", type=int, default=None,
                    help="quanti volontari delle righe nuove sono davvero al "
                         "primo intervento (richiesto solo se lo script lo chiede)")
    a = ap.parse_args()
    if not os.path.exists(a.xlsx):
        sys.exit(f"File non trovato: {a.xlsx}")

    # ---------- pubblicato ----------
    stat = carica("statistiche-interventi")
    tip_pub = carica("interventi-per-tipologia")
    mez_pub = carica("automezzi-impiegati")
    vol_pub = carica("statistiche-volontari")
    periodo = stat["periodo"]
    dal_pub = datetime.date.fromisoformat(periodo["dal"])
    al_pub = datetime.date.fromisoformat(periodo["al"])
    ultimo_pub = periodo.get("ultimo_numero")
    print(f"Pubblicato: dal {dal_pub} al {al_pub}"
          + (f", ultimo intervento {ultimo_pub}" if ultimo_pub else "")
          + f" — {stat['dati']['Interventi registrati']} interventi")

    # ---------- export ----------
    wb = openpyxl.load_workbook(a.xlsx, read_only=True, data_only=True)
    ws = wb["Interventi"]
    rows = list(ws.iter_rows(values_only=True))
    idx = {h: i for i, h in enumerate(rows[0]) if h}

    def col(r, name):
        i = idx.get(name)
        return r[i] if i is not None and i < len(r) else None

    data = [r for r in rows[1:] if col(r, "Numero") not in (None, "")]
    date_exp = [d for d in (gen.parse_data_it(col(r, "Data Inizio")) for r in data) if d]
    if not date_exp:
        sys.exit("Nessuna data leggibile nell'export.")
    print(f"Export: {os.path.basename(a.xlsx)} — {len(data)} righe, "
          f"dal {min(date_exp)} al {max(date_exp)}")

    if min(date_exp) <= dal_pub:
        sys.exit("L'export copre già l'inizio del periodo pubblicato: è CUMULATIVO.\n"
                 "Usa scripts/genera-open-data-interventi.py, che ricalcola tutto.")

    # ---------- righe nuove ----------
    if ultimo_pub and gen.chiave_numero(ultimo_pub):
        soglia = gen.chiave_numero(ultimo_pub)
        nuove = [r for r in data
                 if (gen.chiave_numero(col(r, "Numero")) or (0, 0)) > soglia]
        criterio = f"numero > {ultimo_pub}"
    else:
        nuove = [r for r in data
                 if (gen.parse_data_it(col(r, "Data Inizio")) or dal_pub) > al_pub]
        criterio = f"data > {al_pub} (dataset senza ultimo_numero)"
    vecchie = [r for r in data if r not in nuove]
    print(f"Righe nuove ({criterio}): {len(nuove)}")
    if not nuove:
        print("Niente da aggiungere: dataset già aggiornato.")
        return
    for r in nuove:
        print(f"  - {col(r, 'Numero')}  {col(r, 'Data Inizio')}  "
              f"{col(r, 'Tipologia evento') or col(r, 'Motivo')}")

    # ---------- delta ----------
    d_min = sum(gen.minuti(col(r, "Durata")) for r in nuove)
    d_km = 0.0
    for r in nuove:
        ini = [float(t) for t in __import__("re").findall(
            r"\d+(?:[.,]\d+)?", str(col(r, "Km iniziali") or "").replace(",", "."))]
        fin = [float(t) for t in __import__("re").findall(
            r"\d+(?:[.,]\d+)?", str(col(r, "Km finali") or "").replace(",", "."))]
        for x, y in zip(ini, fin):
            if y >= x:
                d_km += y - x
    d_tip = Counter()
    d_veic = Counter()
    d_con_mezzo = 0
    for r in nuove:
        t = str(col(r, "Tipologia evento") or "").strip()
        if t in ("", "-", "None"):
            t = " ".join(str(col(r, "Motivo") or "").split())
        d_tip[t or "Non classificato"] += 1
        mezzi = gen.automezzi(col(r, "Veicoli"))
        if mezzi:
            d_con_mezzo += 1
            for et in {e for e, _ in mezzi}:
                d_veic[et] += 1
    d_presenze = sum(len(nomi(col(r, "Utenti"))) for r in nuove)

    # automezzi distinti: etichette mai viste nel pubblicato
    etichette_pub = {x["automezzo"] for x in mez_pub["dati"]}
    veic_nuovi = sorted(set(d_veic) - etichette_pub)

    # volontari: chi compare SOLO nelle righe nuove?
    nomi_nuove = set().union(*[nomi(col(r, "Utenti")) for r in nuove])
    nomi_vecchie = set().union(*[nomi(col(r, "Utenti")) for r in vecchie]) if vecchie else set()
    mai_visti = sorted(nomi_nuove - nomi_vecchie)
    if mai_visti and a.volontari_nuovi is None:
        sys.exit(f"\n{len(mai_visti)} volontari compaiono SOLO nelle righe nuove e non "
                 f"altrove in questo export: non posso sapere se erano già conteggiati.\n"
                 f"Rilancia con --volontari-nuovi N (quanti sono davvero al primo "
                 f"intervento; 0 se erano già attivi prima del periodo dell'export).")
    vol_nuovi = a.volontari_nuovi or 0

    # ---------- nuovi totali ----------
    v = stat["dati"]
    ore = round(v["Ore di intervento totali"] + d_min / 60, 1)
    al_new = max(max(date_exp), al_pub)
    ultimo_new = gen.ultimo_numero(nuove, col)
    periodo_new = {"dal": periodo["dal"], "al": al_new.isoformat(),
                   "ultimo_numero": ultimo_new}
    label = (f"dal {dal_pub.day} {gen.MESI_NOME[dal_pub.month]} {dal_pub.year} "
             f"al {al_new.day} {gen.MESI_NOME[al_new.month]} {al_new.year}")

    stat_new = [
        ("Periodo (provvisorio)", label),
        ("Interventi registrati", v["Interventi registrati"] + len(nuove)),
        ("Interventi con automezzo", v["Interventi con automezzo"] + d_con_mezzo),
        ("Automezzi impiegati (distinti)", v["Automezzi impiegati (distinti)"] + len(veic_nuovi)),
        ("Ore di intervento totali", ore),
        ("Chilometri percorsi totali", v["Chilometri percorsi totali"] + int(d_km)),
    ]
    tip = {x["tipologia"]: x["numero_interventi"] for x in tip_pub["dati"]}
    for k, n in d_tip.items():
        tip[k] = tip.get(k, 0) + n
    mez = {x["automezzo"]: x["interventi"] for x in mez_pub["dati"]}
    for k, n in d_veic.items():
        mez[k] = mez.get(k, 0) + n
    vv = vol_pub["dati"]
    vol_new = [
        ("Volontari con almeno un intervento", vv["Volontari con almeno un intervento"] + vol_nuovi),
        ("Presenze dei volontari agli interventi", vv["Presenze dei volontari agli interventi"] + d_presenze),
    ]

    print("\nDelta e nuovi totali:")
    for (k, nuovo), vecchio in zip(stat_new[1:], list(v.values())[1:]):
        print(f"  {k:<32} {vecchio:>8} -> {nuovo}")
    for k, nuovo in vol_new:
        print(f"  {k:<32} {vv[k]:>8} -> {nuovo}")
    print(f"  tipologie: {dict(d_tip)}")
    print(f"  automezzi: {dict(d_veic)}" + (f"  (NUOVI: {veic_nuovi})" if veic_nuovi else ""))
    if mai_visti:
        print(f"  volontari visti solo nelle righe nuove: {len(mai_visti)} "
              f"-> conteggiati come nuovi: {vol_nuovi}")
    print("  nota: le ore ereditano ±0,1 h di arrotondamento dal totale pubblicato.")

    if a.dry_run:
        print("\n--dry-run: nessun file scritto.")
        return

    gen.write_kv("statistiche-interventi", stat_new, periodo_new)
    gen.write_rows("interventi-per-tipologia", ["tipologia", "numero_interventi"],
                   sorted(([k, n] for k, n in tip.items()), key=lambda x: -x[1]), periodo_new)
    gen.write_rows("automezzi-impiegati", ["automezzo", "interventi"],
                   sorted(([k, n] for k, n in mez.items()), key=lambda x: -x[1]), periodo_new)
    gen.write_kv("statistiche-volontari", vol_new, periodo_new)
    print("\nDataset aggiornati per delta. Il file .xlsx NON va committato.")


if __name__ == "__main__":
    main()
