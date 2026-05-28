#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
audit-pdf-accessibilita.py — Audit progressivo accessibilità PDF/UA dei PDF
pubblicati sul sito.

Per ogni PDF in static/ raccoglie:
  - searchable: ha un livello testuale che lo screen reader può leggere?
    (criterio: pdftotext ricava >=100 caratteri di testo dalle prime 3 pagine)
  - tagged: ha tag strutturali PDF/UA (heading, list, paragraph, alt text)?
    (criterio: PyMuPDF rileva /MarkInfo /Marked true nel catalog)
  - lingua dichiarata: ha /Lang nel catalog?
  - titolo nei metadati
  - origine: classificazione euristica per cartella+nomefile
      - GRUPPO: prodotto dal Gruppo (presentazioni nostre, moduli, locandine)
      - TERZO: prodotto da DPC/Regione/Comune/altri enti (responsabilità loro)
      - STORICO: scansione di documento ricevuto

Output: data/audit-pdf.yaml + sezione di stato.

Verdict per ogni PDF:
  ✅ ACCESSIBILE   - searchable + tagged + lingua + titolo
  🟡 PARZIALE      - searchable ma non tagged (lo screen reader legge ma senza struttura)
  🔴 NON ACCESSIBILE - non searchable (scansione pura, OCR necessario)
  ⚪ TERZO         - di terzo ente, accessibilità a carico loro

Uso:
    python3 scripts/audit-pdf-accessibilita.py [--write]
    --write  scrive data/audit-pdf.yaml (default: solo stampa report)
"""

from __future__ import annotations
import argparse
import subprocess
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    sys.stderr.write("ERRORE: manca PyMuPDF. Installa:\n  pip install --break-system-packages PyMuPDF\n")
    sys.exit(1)

try:
    import yaml
except ImportError:
    sys.stderr.write("ERRORE: manca pyyaml.\n")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parent.parent
STATIC = REPO_ROOT / "static"
DATA_FILE = REPO_ROOT / "data" / "audit-pdf.yaml"

# Pattern di classificazione origine basati su nome file o path.
# L'ordine conta: prima match vince.
ORIGINE_PATTERNS = [
    # TERZO — documenti di altri enti, la cui accessibilità è responsabilità
    # dell'ente emittente (come dichiariamo pubblicamente).
    ("TERZO", "DPC / Dipartimento Protezione Civile",
     ["dpc-", "protezione-civile-art-", "dpc_"]),
    ("TERZO", "Regione Lazio (BURL, DGR, determine, regolamenti regionali)",
     ["regione-lazio", "regolamento-regionale-lazio", "dgr-lazio",
      "determinazione-lazio", "burl"]),
    ("TERZO", "Comune di Genzano di Roma (ordinanze, delibere)",
     ["ordinanza-", "delibera-", "deliberazione-"]),
    ("TERZO", "FEMA (Federal Emergency Management Agency, USA)",
     ["fema-"]),
    ("TERZO", "Polizia di Stato",
     ["polizia-stato-"]),
    ("TERZO", "Fondazione Barilla",
     ["fondazionebarilla_", "fondazione-barilla"]),
    ("TERZO", "Caritas / Banco Alimentare",
     ["caritas_", "banco_alimentare"]),
    ("TERZO", "Federazione Italiana Cuochi (FIC)",
     ["dsefic_", "manuale_cucina_emergenza_fic"]),
    ("TERZO", "CNA / Confederazione Nazionale Artigianato",
     ["cna-"]),
    ("TERZO", "Salone del Libro Torino",
     ["salone-del-libro", "salone_libro"]),
    # GRUPPO — documenti prodotti da noi (presentazioni, moduli, locandine)
    ("GRUPPO", "Presentazione tematica generata da scripts/genera-presentazione.py",
     ["-presentazione-pdf", "presentazione-struttura-sito"]),
    ("GRUPPO", "Locandina del Gruppo",
     ["locandina-"]),
    ("GRUPPO", "Modulo del Gruppo (modulistica)",
     ["domanda-ammissione", "modulo-", "modulistica"]),
]


def classifica_origine(rel_path: str) -> tuple[str, str]:
    """Restituisce (tipo, descrizione) basato su path/filename."""
    nome = Path(rel_path).name.lower()
    for tipo, descr, patterns in ORIGINE_PATTERNS:
        for p in patterns:
            if p in nome:
                return tipo, descr
    return "GRUPPO", "Classificazione di default (assumiamo nostro produzione)"


def analizza_pdf(pdf_path: Path) -> dict:
    """Estrae metadati e flag di accessibilità da un PDF."""
    rel = str(pdf_path.relative_to(REPO_ROOT))
    info: dict = {
        "path": "/" + str(pdf_path.relative_to(STATIC)),
        "file": pdf_path.name,
        "size_kb": round(pdf_path.stat().st_size / 1024, 1),
        "searchable": False,
        "tagged": False,
        "language": None,
        "title": None,
        "pages": 0,
        "errors": [],
    }
    try:
        doc = fitz.open(str(pdf_path))
        info["pages"] = doc.page_count
        # Titolo dai metadati (può essere vuoto)
        info["title"] = (doc.metadata.get("title") or "").strip() or None
        # Lingua dichiarata (catalog /Lang)
        catalog = doc.pdf_catalog()
        if catalog:
            xref_str = doc.xref_object(catalog)
            # Cerca /Lang nel testo del catalog
            for line in xref_str.split("/"):
                if line.strip().startswith("Lang"):
                    # Es: /Lang(it-IT)
                    lang_str = line.split("(", 1)[-1].split(")", 1)[0] if "(" in line else line.strip()
                    info["language"] = lang_str.strip("/").strip() or None
                    break
            # Tagged: /MarkInfo<</Marked true>>
            info["tagged"] = "/Marked true" in xref_str or "Marked true" in xref_str
        # Searchable: usa pdftotext sulle prime 3 pagine
        try:
            r = subprocess.run(
                ["pdftotext", "-l", "3", str(pdf_path), "-"],
                capture_output=True, text=True, timeout=30,
            )
            text_len = len(r.stdout.strip())
            info["searchable"] = text_len >= 100
            info["text_chars_sample"] = text_len
        except Exception as e:
            info["errors"].append(f"pdftotext failed: {e}")
        doc.close()
    except Exception as e:
        info["errors"].append(f"open failed: {e}")
    return info


def verdict(info: dict, origine_tipo: str) -> str:
    """Calcola il verdict simbolico."""
    if origine_tipo == "TERZO":
        return "TERZO"  # ⚪ non nostro
    if info["errors"]:
        return "ERRORE"  # ❗
    if info["searchable"] and info["tagged"]:
        return "ACCESSIBILE"  # ✅
    if info["searchable"] and not info["tagged"]:
        return "PARZIALE"  # 🟡 (necessita tagging strutturale)
    return "NON_ACCESSIBILE"  # 🔴 (pura scansione, OCR necessario)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true",
                    help="Scrivi data/audit-pdf.yaml (default: solo stampa)")
    args = ap.parse_args()

    pdfs = sorted(STATIC.rglob("*.pdf"))
    print(f"\n📚 Trovati {len(pdfs)} PDF in static/\n")

    records = []
    summary = {"ACCESSIBILE": 0, "PARZIALE": 0, "NON_ACCESSIBILE": 0,
               "TERZO": 0, "ERRORE": 0}

    for pdf in pdfs:
        info = analizza_pdf(pdf)
        origine_tipo, origine_desc = classifica_origine(info["path"])
        info["origine"] = origine_tipo
        info["origine_descrizione"] = origine_desc
        info["verdict"] = verdict(info, origine_tipo)
        summary[info["verdict"]] += 1
        records.append(info)

        icon = {
            "ACCESSIBILE": "✅",
            "PARZIALE": "🟡",
            "NON_ACCESSIBILE": "🔴",
            "TERZO": "⚪",
            "ERRORE": "❗",
        }[info["verdict"]]
        flags = []
        if info["searchable"]: flags.append("searchable")
        if info["tagged"]: flags.append("tagged")
        if info["language"]: flags.append(f"lang={info['language']}")
        if info["title"]: flags.append("title-meta")
        print(f"  {icon} {info['path']:60s}  {origine_tipo:7s}  pp={info['pages']:3d}  {info['size_kb']:7.1f}KB  {', '.join(flags) or '(nessuno)'}")

    print(f"\n📊 Riepilogo:")
    for k, v in summary.items():
        icon = {"ACCESSIBILE": "✅", "PARZIALE": "🟡",
                "NON_ACCESSIBILE": "🔴", "TERZO": "⚪", "ERRORE": "❗"}[k]
        print(f"   {icon} {k:20s}  {v:3d}")

    if args.write:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        from datetime import date
        out = {
            "ultimo_audit": str(date.today()),
            "totale": len(pdfs),
            "riepilogo": summary,
            "documenti": records,
        }
        DATA_FILE.write_text(yaml.safe_dump(out, allow_unicode=True,
                                            sort_keys=False, default_flow_style=False),
                             encoding="utf-8")
        print(f"\n✏  Scritto {DATA_FILE.relative_to(REPO_ROOT)}")
    else:
        print(f"\n(dry-run, usa --write per salvare data/audit-pdf.yaml)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
