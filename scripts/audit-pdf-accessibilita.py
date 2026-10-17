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
  ✅ ACCESSIBILE   - searchable + tagged + lingua coerente + titolo nei metadati
                     (controlli superati, non una certificazione PDF/UA)
  🟡 PARZIALE      - searchable, ma senza tag, senza titolo o con lingua
                     mancante o diversa da quella del documento
  🔴 NON ACCESSIBILE - non searchable (scansione pura, OCR necessario)
  ⚪ TERZO         - di terzo ente, accessibilità a carico loro

Uso:
    python3 scripts/audit-pdf-accessibilita.py [--write]
    python3 scripts/audit-pdf-accessibilita.py --check-inventario
    --write             scrive data/audit-pdf.yaml (default: solo stampa report)
    --check-inventario  confronta data/audit-pdf.yaml con i PDF in static/
                        (aggiunti, tolti, sostituiti); exit = differenze.
                        Non serve PyMuPDF. Gira su ogni PR (validate-pr.yml).

Dal 17/10/2026 (audit esterno, rilievi R9 e R10): il verdetto ACCESSIBILE
chiede anche titolo e lingua coerente, come diceva questa descrizione e il
codice non faceva; e l'inventario non può più restare indietro rispetto ai
PDF pubblicati.
"""

from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

fitz = None  # PyMuPDF, caricato solo quando serve analizzare i PDF


def carica_fitz():
    global fitz
    try:
        import fitz as _fitz  # PyMuPDF
    except ImportError:
        sys.stderr.write("ERRORE: manca PyMuPDF. Installa:\n  pip install --break-system-packages PyMuPDF\n")
        sys.exit(1)
    fitz = _fitz

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
      "determinazione-lazio", "burl", "determinazione-g1"]),
    ("TERZO", "Comune di Genzano di Roma (ordinanze, delibere)",
     ["ordinanza-", "delibera-", "deliberazione-",
      # avviso, determinazione e modulo del Comune per i volontari civici (ottobre 2026)
      "volontari-civici-genzano"]),
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
    ("TERZO", "ISPRA — Servizio Geologico d'Italia (Carta geologica CARG, CC BY 4.0)",
     ["carg-foglio-", "ispra-"]),
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


def impronta(pdf_path: Path) -> str:
    """sha256 del file: riconosce un PDF sostituito anche a parità di peso."""
    import hashlib
    return hashlib.sha256(pdf_path.read_bytes()).hexdigest()


def analizza_pdf(pdf_path: Path) -> dict:
    """Estrae metadati e flag di accessibilità da un PDF."""
    rel = str(pdf_path.relative_to(REPO_ROOT))
    info: dict = {
        "path": "/" + str(pdf_path.relative_to(STATIC)),
        "file": pdf_path.name,
        "size_kb": round(pdf_path.stat().st_size / 1024, 1),
        "sha256": impronta(pdf_path),
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
            # Tagged secondo PDF/UA (ISO 14289-1): servono INSIEME l'albero dei
            # tag (/StructTreeRoot) e la dichiarazione /MarkInfo<</Marked true>>.
            # Il /MarkInfo può essere un riferimento indiretto (/MarkInfo 12 0 R):
            # cercare la stringa "Marked true" dentro il catalog non lo vede e il
            # documento risulta non taggato pur essendolo. È successo con due PDF
            # nostri (il programma del Salone del libro e la delibera di
            # costituzione del Gruppo), che la dichiarazione di accessibilità
            # contava fra i non taggati: 44 invece di 42 (corretto il 14/09/2026).
            albero = "/StructTreeRoot" in xref_str
            marcato = False
            for pezzo in xref_str.split("/MarkInfo")[1:]:
                testa = pezzo.lstrip()
                if testa.startswith("<<"):
                    marcato = "Marked true" in testa.split(">>", 1)[0]
                else:  # riferimento indiretto: /MarkInfo 12 0 R
                    numero = testa.split()
                    if numero and numero[0].isdigit():
                        try:
                            marcato = "Marked true" in doc.xref_object(int(numero[0]))
                        except Exception:  # noqa: BLE001
                            marcato = False
                break
            info["tagged"] = albero and marcato
        # Searchable: il testo delle prime 3 pagine lo estrae PyMuPDF, che ha già
        # il documento aperto. Prima si invocava `pdftotext` di poppler: dove il
        # binario manca — questo container, per esempio — tutti i PDF nostri
        # risultavano in ERRORE e la tabella pubblicata diceva il falso
        # (audit 14/09/2026). Un controllo che dipende da un programma esterno
        # non installato non è un controllo.
        try:
            estratto = []
            for n in range(min(3, doc.page_count)):
                estratto.append(doc[n].get_text())
            text_len = len("".join(estratto).strip())
            info["searchable"] = text_len >= 100
            info["text_chars_sample"] = text_len
        except Exception as e:
            info["errors"].append(f"estrazione testo fallita: {e}")
        doc.close()
    except Exception as e:
        info["errors"].append(f"open failed: {e}")
    return info


LINGUA_DA_NOME = re.compile(r"[-_](en|fr|de|es|pt|ro|ar|eo|uk|zh|sq)(?:[-_.]|$)", re.I)


def lingua_coerente(info: dict) -> bool:
    """La lingua dichiarata corrisponde a quella del documento.

    Di norma i nostri PDF sono in italiano; una lingua diversa è ammessa se il
    nome del file la indica (es. poster-emergenza-en.pdf)."""
    lang = (info.get("language") or "").lower()
    if not lang:
        return False
    m = LINGUA_DA_NOME.search(Path(info["path"]).stem)
    attesa = m.group(1).lower() if m else "it"
    return lang.split("-")[0] == attesa


def check_inventario() -> int:
    """Confronta l'inventario con i PDF presenti in static/."""
    dati = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8")) or {}
    inv = {d["path"]: d for d in dati.get("documenti", [])}
    presenti = {}
    for pdf in STATIC.rglob("*.pdf"):
        presenti["/" + pdf.relative_to(STATIC).as_posix()] = impronta(pdf)
    diff = 0
    for path in sorted(set(presenti) - set(inv)):
        print(f"  manca nell'inventario: {path}")
        diff += 1
    for path in sorted(set(inv) - set(presenti)):
        print(f"  nell'inventario ma non più pubblicato: {path}")
        diff += 1
    for path in sorted(set(inv) & set(presenti)):
        # l'impronta e non il peso: una correzione dei soli metadati può
        # lasciare il file della stessa dimensione
        if inv[path].get("sha256") != presenti[path]:
            print(f"  sostituito (impronta diversa): {path}")
            diff += 1
    if dati.get("totale") != len(presenti):
        print(f"  totale dichiarato {dati.get('totale')}, PDF presenti {len(presenti)}")
        diff += 1
    if diff:
        print(f"\n{diff} differenza/e fra data/audit-pdf.yaml e i PDF in static/."
              "\nRigenera con: python3 scripts/audit-pdf-accessibilita.py --write")
    else:
        print(f"Inventario PDF allineato: {len(presenti)} file.")
    return min(diff, 255)


def verdict(info: dict, origine_tipo: str) -> str:
    """Calcola il verdict simbolico."""
    if origine_tipo == "TERZO":
        return "TERZO"  # ⚪ non nostro
    if info["errors"]:
        return "ERRORE"  # ❗
    if info["searchable"] and info["tagged"] and info["title"] and lingua_coerente(info):
        return "ACCESSIBILE"  # ✅
    if info["searchable"]:
        # testo leggibile ma manca almeno uno fra tag, titolo e lingua giusta
        return "PARZIALE"  # 🟡
    return "NON_ACCESSIBILE"  # 🔴 (pura scansione, OCR necessario)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--write", action="store_true",
                    help="Scrivi data/audit-pdf.yaml (default: solo stampa)")
    ap.add_argument("--check-inventario", action="store_true",
                    help="Confronta l'inventario con i PDF in static/ (senza PyMuPDF)")
    args = ap.parse_args()
    if args.check_inventario:
        return check_inventario()
    carica_fitz()

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
