#!/usr/bin/env python3
"""Genera i dataset aperti (CSV + JSON, CC BY 4.0) da data/*.yaml.

Pubblica SOLO i dataset con dati reali e verificati. I file con dati
mancanti (dae.yaml, idranti.yaml: scheletri in attesa dei dati ufficiali
ASL Roma 6 / Comando VVF) NON vengono esportati: niente dati fittizi
(vincolo permanente CLAUDE.md — pubblicare posizioni inventate di
defibrillatori o idranti sarebbe pericoloso oltre che scorretto).

Output: static/open-data/<nome>.csv e <nome>.json, più catalogo.json con
titolo, licenza, fonte e data di aggiornamento di ciascun dataset. I file di
dati restano array semplici (chi li riusa non deve cambiare nulla): i
metadati stanno nel catalogo (audit esterno 25/09/2026, rilievo F28).
URL pubblici: /open-data/<nome>.csv, /open-data/<nome>.json, /open-data/catalogo.json
Idempotente: riscrive i file ad ogni esecuzione.

Uso: python3 scripts/genera-open-data.py
"""
import csv
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "static" / "open-data"

# Per ogni dataset: file sorgente, chiave nel YAML, basename di output,
# campi (in ordine) da esportare, titolo descrittivo per la pagina.
# Esportati SOLO i campi-dato; si escludono i campi di sola presentazione
# (icone Bootstrap) perché non sono informazione riusabile.
DATASETS = [
    {
        "src": "aree_emergenza.yaml", "key": "aree", "out": "aree-emergenza",
        "fields": ["id", "tipo", "nome", "indirizzo", "lat", "lon", "verified"],
        "title": "Aree di emergenza del Piano comunale di Protezione Civile",
        "descrizione": "Aree di attesa della popolazione (AA), aree di ricovero (AR) "
                       "e aree di ammassamento dei soccorritori (AS), con coordinate GPS.",
        "fonte": "Piano di Protezione Civile del Comune di Genzano di Roma; coordinate "
                 "verificate sul campo dal Gruppo Comunale Volontari di Protezione Civile.",
    },
    {
        "src": "numeri_utili.yaml", "key": "emergenza", "out": "numeri-utili-emergenza",
        "fields": ["numero", "nome", "descrizione", "principale"],
        "title": "Numeri utili di emergenza (validi nel Lazio)",
        "descrizione": "Numeri da chiamare in emergenza nel Lazio.",
        "fonte": "Regione Lazio (Numero Unico Emergenza 112) e Agenzia regionale di "
                 "Protezione Civile del Lazio (Sala Operativa, 803 555).",
    },
    {
        "src": "codici_colore.yaml", "key": "codici", "out": "codici-colore-allerta",
        "fields": ["livello", "titolo", "significato", "cosa_fare", "colore_bg"],
        "title": "Codici colore dell'allerta meteo (Regione Lazio)",
        "descrizione": "Significato dei livelli di allerta verde, giallo, arancione e rosso "
                       "e comportamenti raccomandati.",
        "fonte": "Dipartimento della Protezione Civile e Centro Funzionale Regionale del "
                 "Lazio (sistema di allertamento meteo-idrogeologico).",
    },
    {
        "src": "eventi_storici.yaml", "key": "eventi", "out": "eventi-storici-castelli-romani",
        "fields": ["ordine", "anno", "tipo", "titolo", "luogo",
                   "descrizione", "lezione", "fonte", "fonte_url"],
        "title": "Timeline storica del rischio nei Castelli Romani",
        "descrizione": "Eventi geologici, sismici, idrogeologici e normativi che riguardano "
                       "i Castelli Romani.",
        "fonte": "Fonti istituzionali indicate per ciascun evento nei campi fonte e fonte_url.",
    },
]


def _norm_str(v: str) -> str:
    """Collassa whitespace e a-capo (le descrizioni YAML sono multilinea)."""
    return " ".join(v.split())


def _csv_value(v):
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, str):
        return _norm_str(v)
    return v


def _json_value(v):
    if v is None:
        return ""
    if isinstance(v, str):
        return _norm_str(v)
    return v  # bool / int / float restano nativi (lat, lon, ordine)


LICENZA = {"nome": "CC BY 4.0",
           "url": "https://creativecommons.org/licenses/by/4.0/deed.it"}
TITOLARE = "Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma"


def _aggiornato_il(src: Path) -> str:
    """Data dell'ultimo commit del file sorgente: stabile fra un'esecuzione e
    l'altra, così il catalogo cambia solo quando cambiano i dati."""
    try:
        out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(src)],
                             cwd=ROOT, capture_output=True, text=True, check=True)
        if out.stdout.strip():
            return out.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        pass
    return dt.date.today().isoformat()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    written = []
    catalogo = []
    for ds in DATASETS:
        src = DATA / ds["src"]
        if not src.exists():
            print(f"[skip] {ds['src']}: file assente", file=sys.stderr)
            continue
        data = yaml.safe_load(src.read_text(encoding="utf-8")) or {}
        rows = data.get(ds["key"]) or []
        if not rows:
            print(f"[skip] {ds['src']}: nessun dato reale (scheletro vuoto)",
                  file=sys.stderr)
            continue
        fields = ds["fields"]

        csv_path = OUT / f"{ds['out']}.csv"
        with csv_path.open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(fields)
            for r in rows:
                w.writerow([_csv_value(r.get(k)) for k in fields])

        json_path = OUT / f"{ds['out']}.json"
        recs = [{k: _json_value(r.get(k)) for k in fields} for r in rows]
        json_path.write_text(
            json.dumps(recs, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8")

        written.append((ds["out"], len(rows), ds["title"]))
        catalogo.append({
            "id": ds["out"],
            "titolo": ds["title"],
            "descrizione": ds["descrizione"],
            "fonte": ds["fonte"],
            "titolare": TITOLARE,
            "licenza": LICENZA,
            "aggiornato_il": _aggiornato_il(src),
            "record": len(rows),
            "campi": fields,
            "file": {"csv": f"/open-data/{ds['out']}.csv",
                     "json": f"/open-data/{ds['out']}.json"},
        })
        print(f"[ok] {ds['out']}: {len(rows)} record -> CSV + JSON")

    if not written:
        print("Nessun dataset con dati reali da esportare.", file=sys.stderr)
        return 0

    (OUT / "catalogo.json").write_text(
        json.dumps({"titolare": TITOLARE, "licenza": LICENZA, "dataset": catalogo},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("[ok] catalogo.json: metadati di licenza, fonte e aggiornamento")

    print(f"\nDataset pubblicati: {len(written)} "
          f"({sum(n for _, n, _ in written)} record totali) in {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
