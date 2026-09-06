#!/usr/bin/env python3
"""
Integrità dei file binari pubblicati (immagini, icone, PDF, ZIP, JSON, SVG).

Nasce dall'audit esterno del 06/09/2026: la favicon.ico era un file da
0 byte (F18) e un PNG dell'archivio storico aveva lo stream corrotto (F19).
Nessun controllo del sito guardava dentro i file: questo lo fa.

Controlli:
  - file da 0 byte in static/ (eccetto .gitkeep e simili) → errore;
  - immagini raster (png/jpg/jpeg/webp/gif/ico) decodificabili con Pillow
    (verify + load) → errore se corrotte;
  - SVG parsabili come XML → errore;
  - ZIP con testzip() pulito → errore;
  - JSON parsabili → errore;
  - PDF apribili con pypdf (se installato) → errore se illeggibili; in più
    inventario informativo: pagine, struttura di tag (/StructTreeRoot,
    prerequisito PDF/UA), testo estraibile nelle prime pagine.

Uso:
  python3 scripts/check-integrita-asset.py [--radice static] [--pdf-report FILE.md]
Exit code = numero di errori.
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parent.parent

IMMAGINI = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".ico"}
IGNORA_NOMI = {".gitkeep", ".nojekyll", ".htaccess"}
IGNORA_DIR = {"pagefind", "node_modules"}


def controlla_immagine(path: Path) -> str | None:
    try:
        from PIL import Image
    except ImportError:
        return None  # senza Pillow non si giudica
    try:
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            im.load()
    except Exception as e:  # noqa: BLE001
        return f"immagine non decodificabile ({e.__class__.__name__}: {e})"
    return None


def controlla_pdf(path: Path) -> tuple[str | None, dict | None]:
    try:
        from pypdf import PdfReader
    except BaseException:  # noqa: BLE001 — ImportError, ma anche i panic dei binding nativi
        return None, None
    try:
        reader = PdfReader(str(path))
        n = len(reader.pages)
        radice = reader.trailer["/Root"]
        taggato = "/StructTreeRoot" in radice
        testo = 0
        for pagina in reader.pages[:3]:
            try:
                testo += len((pagina.extract_text() or "").strip())
            except Exception:  # noqa: BLE001
                pass
        return None, {"pagine": n, "tag": taggato, "testo": testo > 0}
    except Exception as e:  # noqa: BLE001
        return f"PDF non leggibile ({e.__class__.__name__}: {e})", None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--radice", default="static", help="cartella da controllare (default: static)")
    ap.add_argument("--pdf-report", help="scrive l'inventario dei PDF in Markdown")
    args = ap.parse_args()

    radice = ROOT / args.radice
    errori: list[str] = []
    pdf_rows: list[tuple[str, dict]] = []
    n_file = 0

    for path in sorted(radice.rglob("*")):
        if not path.is_file():
            continue
        if any(part in IGNORA_DIR for part in path.parts):
            continue
        if path.name in IGNORA_NOMI:
            continue
        n_file += 1
        rel = path.relative_to(ROOT)
        if path.stat().st_size == 0:
            errori.append(f"{rel}: file vuoto (0 byte)")
            continue
        ext = path.suffix.lower()
        if ext in IMMAGINI:
            e = controlla_immagine(path)
            if e:
                errori.append(f"{rel}: {e}")
        elif ext == ".svg":
            try:
                ElementTree.parse(path)
            except ElementTree.ParseError as e:
                errori.append(f"{rel}: SVG non parsabile ({e})")
        elif ext == ".zip":
            try:
                with zipfile.ZipFile(path) as zf:
                    guasto = zf.testzip()
                if guasto:
                    errori.append(f"{rel}: ZIP con voce corrotta ({guasto})")
            except zipfile.BadZipFile as e:
                errori.append(f"{rel}: ZIP non valido ({e})")
        elif ext == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                errori.append(f"{rel}: JSON non valido ({e})")
        elif ext == ".pdf":
            e, info = controlla_pdf(path)
            if e:
                errori.append(f"{rel}: {e}")
            elif info:
                pdf_rows.append((str(rel), info))

    print(f"File controllati: {n_file}")
    if pdf_rows:
        senza_tag = sum(1 for _, i in pdf_rows if not i["tag"])
        senza_testo = sum(1 for _, i in pdf_rows if not i["testo"])
        print(f"PDF: {len(pdf_rows)} letti, {senza_tag} senza struttura di tag, {senza_testo} senza testo estraibile (informativo)")
        if args.pdf_report:
            righe = ["| PDF | Pagine | Tag (PDF/UA) | Testo estraibile |", "|---|---|---|---|"]
            for rel, i in pdf_rows:
                righe.append(f"| `{rel}` | {i['pagine']} | {'✅' if i['tag'] else '❌'} | {'✅' if i['testo'] else '❌'} |")
            Path(args.pdf_report).write_text("\n".join(righe) + "\n", encoding="utf-8")
    if errori:
        print(f"\n❌ {len(errori)} errori di integrità:")
        for e in errori:
            print(f"  - {e}")
    else:
        print("✅ Nessun file vuoto o corrotto.")
    return len(errori)


if __name__ == "__main__":
    sys.exit(main())
