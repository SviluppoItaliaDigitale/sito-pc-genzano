#!/usr/bin/env python3
"""Genera i dataset aperti (CSV + JSON, CC BY 4.0) da data/*.yaml.

Pubblica SOLO i dataset con dati reali e verificati. I file con dati
mancanti (dae.yaml, idranti.yaml: scheletri in attesa dei dati ufficiali
ASL Roma 6 / Comando VVF) NON vengono esportati: niente dati fittizi
(vincolo permanente CLAUDE.md — pubblicare posizioni inventate di
defibrillatori o idranti sarebbe pericoloso oltre che scorretto).

Output: static/open-data/<nome>.csv e <nome>.json
URL pubblici: /open-data/<nome>.csv e /open-data/<nome>.json
Idempotente: riscrive i file ad ogni esecuzione.

Uso: python3 scripts/genera-open-data.py
"""
import csv
import json
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
    },
    {
        "src": "numeri_utili.yaml", "key": "emergenza", "out": "numeri-utili-emergenza",
        "fields": ["numero", "nome", "descrizione", "principale"],
        "title": "Numeri utili di emergenza (validi nel Lazio)",
    },
    {
        "src": "codici_colore.yaml", "key": "codici", "out": "codici-colore-allerta",
        "fields": ["livello", "titolo", "significato", "cosa_fare", "colore_bg"],
        "title": "Codici colore dell'allerta meteo (Regione Lazio)",
    },
    {
        "src": "eventi_storici.yaml", "key": "eventi", "out": "eventi-storici-castelli-romani",
        "fields": ["ordine", "anno", "tipo", "titolo", "luogo",
                   "descrizione", "lezione", "fonte", "fonte_url"],
        "title": "Timeline storica del rischio nei Castelli Romani",
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


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    written = []
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
        print(f"[ok] {ds['out']}: {len(rows)} record -> CSV + JSON")

    if not written:
        print("Nessun dataset con dati reali da esportare.", file=sys.stderr)
        return 0

    print(f"\nDataset pubblicati: {len(written)} "
          f"({sum(n for _, n, _ in written)} record totali) in {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
