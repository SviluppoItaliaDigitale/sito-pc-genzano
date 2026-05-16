#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
genera-qr-articoli.py — Generatore QR code per gli articoli del sito.

Per ogni articolo in content/comunicazioni/*.md (e opzionalmente altre sezioni)
genera due file in static/qr/:
  - <basename>.png  → raster 600x600, alta correzione errori (per stampa rapida)
  - <basename>.svg  → vettoriale, infinitamente scalabile (per poster A1/A2)

Il QR codifica l'URL pubblico dell'articolo (default protezionecivilegenzano.it).

Uso:
  python3 scripts/genera-qr-articoli.py                      # tutti i comunicati nuovi
  python3 scripts/genera-qr-articoli.py --force              # rigenera tutto
  python3 scripts/genera-qr-articoli.py --only 2026-05-14    # solo file che matchano
  python3 scripts/genera-qr-articoli.py --sezione standard-iso \\
          --url-prefix https://www.protezionecivilegenzano.it/standard-iso/

Dipendenze (una sola volta):
  pip install --break-system-packages segno pyyaml

Idempotente: skip dei file già esistenti salvo --force.
Compatibile con il workflow Hugo: i file in static/qr/ sono serviti da /qr/<base>.png.

Autore: Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
Uso: interno al repository sito-pc-genzano.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import segno
except ImportError:
    sys.stderr.write(
        "ERRORE: manca la libreria 'segno'.\n"
        "Installa con: pip install --break-system-packages segno pyyaml\n"
    )
    sys.exit(1)

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "ERRORE: manca la libreria 'pyyaml'.\n"
        "Installa con: pip install --break-system-packages segno pyyaml\n"
    )
    sys.exit(1)


# ─────────────────────────────────────────────────────────────────────────────
# Configurazione
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_URL_BASE = "https://www.protezionecivilegenzano.it"
# Default vuoto = processa TUTTE le sezioni di content/ (modalità completa,
# allineata alla scelta del 16/05/2026 di mostrare il QR su tutte le pagine).
# Specificare --sezione X per filtrare a una sola sezione.
DEFAULT_SEZIONE = ""

# Sezioni escluse di default per evitare conflitti di naming.
# Le 7 traduzioni multilingua hanno _index.md con nomi sezione identici
# alla versione italiana (es. content/english/cosa-fare-adesso/_index.md
# vs content/cosa-fare-adesso/_index.md → entrambi userebbero
# "cosa-fare-adesso" come basename del QR). Le traduzioni sono pagine
# secondarie con valore marginale per il QR (chi le legge bilingue ha
# già scansionato l'URL italiano). Saltate per default.
EXCLUDED_SECTIONS = frozenset({
    "english", "francais", "deutsch",
    "espanol", "portugues", "romana", "esperanto",
})

# Colori istituzionali: il QR funziona meglio in nero su bianco per scanner
# economici. Mantieni questi default salvo richiesta esplicita.
QR_DARK = "#003366"   # blu PC Genzano (alto contrasto su bianco)
QR_LIGHT = "#FFFFFF"  # sfondo bianco

# Dimensione PNG output (lato in pixel). 600px è il sweet spot tra
# qualità di stampa (300dpi → 5cm di lato leggibili) e peso file (~10-20 KB).
PNG_SIZE = 600

# Error correction level "H" → fino a 30% del QR può essere danneggiato/coperto
# senza perdita di leggibilità. Necessario per stampa su carta porosa,
# affissioni esterne, e futura sovrapposizione del logo PC al centro.
ERROR_LEVEL = "H"

# Regex per riconoscere il frontmatter YAML in testa al file markdown
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


# ─────────────────────────────────────────────────────────────────────────────
# Funzioni di supporto
# ─────────────────────────────────────────────────────────────────────────────

def estrai_frontmatter(testo_md: str) -> dict:
    """Estrae il dict YAML dal frontmatter di un file markdown. Vuoto se assente."""
    match = FRONTMATTER_RE.match(testo_md)
    if not match:
        return {}
    try:
        data = yaml.safe_load(match.group(1)) or {}
        return data if isinstance(data, dict) else {}
    except yaml.YAMLError as exc:
        sys.stderr.write(f"  ⚠ frontmatter YAML non valido: {exc}\n")
        return {}


def deriva_slug(file_md: Path, frontmatter: dict) -> str:
    """
    Ritorna lo slug URL dell'articolo.

    Priorità:
      1. frontmatter.slug se esplicito
      2. frontmatter.url se esplicito (estrae l'ultimo segmento)
      3. nome file senza estensione (default Hugo: 'AAAA-MM-GG-titolo')
    """
    if isinstance(frontmatter.get("slug"), str) and frontmatter["slug"].strip():
        return frontmatter["slug"].strip("/")

    url_fm = frontmatter.get("url")
    if isinstance(url_fm, str) and url_fm.strip():
        return url_fm.strip("/").rsplit("/", 1)[-1]

    return file_md.stem


def costruisci_url(url_prefix: str, slug: str) -> str:
    """Compone l'URL finale, garantendo slash di chiusura (canonico Hugo)."""
    prefix = url_prefix.rstrip("/") + "/"
    return f"{prefix}{slug.strip('/')}/"


def deriva_target(md_path: Path, content_root: Path, url_base: str) -> tuple[str, str]:
    """Per un file .md sotto content/ ritorna (basename_qr, url_pubblico).

    Logica di naming (allineata al partial qr-articolo.html):
      - content/_index.md                       → ("home", url_base + "/")
      - content/<sez>/_index.md                 → ("<sez>", url_base + "/<sez>/")
      - content/<sez>/<nome>.md                 → ("<nome>", url_base + "/<sez>/<nome>/")
      - content/<sez>/<sub>/<nome>.md           → ("<nome>", url_base + "/<sez>/<sub>/<nome>/")

    Storia: il 16/05/2026 l'utente ha chiesto QR su tutte le pagine, non solo
    /comunicazioni/. Naming uniformato col partial Hugo per coerenza.
    """
    rel = md_path.relative_to(content_root)
    parent = rel.parent
    base_url = url_base.rstrip("/")
    if rel.name == "_index.md":
        if str(parent) in (".", ""):
            return ("home", base_url + "/")
        section_name = parent.name
        path_str = str(parent).replace("\\", "/")
        return (section_name, f"{base_url}/{path_str}/")
    basename = md_path.stem
    path_str = str(rel.with_suffix("")).replace("\\", "/")
    return (basename, f"{base_url}/{path_str}/")


def genera_qr_png(url: str, output_path: Path) -> None:
    """Genera il QR in formato PNG raster."""
    qr = segno.make(url, error=ERROR_LEVEL)
    # scale ≈ PNG_SIZE / (modulo + bordo*2). Per dimensione costante usiamo
    # 'border' fisso a 4 moduli (standard ISO/IEC 18004) e ricalcoliamo scale.
    moduli_totali = qr.symbol_size(border=4)[0]
    scale = max(1, PNG_SIZE // moduli_totali)
    qr.save(
        str(output_path),
        kind="png",
        scale=scale,
        border=4,
        dark=QR_DARK,
        light=QR_LIGHT,
    )


def genera_qr_svg(url: str, output_path: Path) -> None:
    """Genera il QR in formato SVG vettoriale."""
    qr = segno.make(url, error=ERROR_LEVEL)
    qr.save(
        str(output_path),
        kind="svg",
        scale=10,            # in SVG è quasi irrilevante (vettoriale)
        border=4,
        dark=QR_DARK,
        light=QR_LIGHT,
        xmldecl=True,
        svgns=True,
        title="QR code articolo PC Genzano",
        desc=f"QR per {url}",
        omitsize=False,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genera QR code (PNG+SVG) per gli articoli del sito PC Genzano.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--sezione",
        default=DEFAULT_SEZIONE,
        help="Sezione content/ da processare (default: vuoto = TUTTE le sezioni). "
             "Esempio: --sezione comunicazioni per limitare ai soli articoli.",
    )
    parser.add_argument(
        "--url-base",
        default=DEFAULT_URL_BASE,
        help="Base URL del sito (default: %(default)s). Lo slug viene derivato "
             "automaticamente dal path del file .md.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rigenera anche i QR già esistenti.",
    )
    parser.add_argument(
        "--only",
        default=None,
        help="Processa solo i file che contengono questa stringa nel nome.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Mostra cosa farebbe senza scrivere file.",
    )
    args = parser.parse_args()

    # Risolve la root del repo (assume script in scripts/, root = parent)
    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent
    content_root = repo_root / "content"
    output_dir = repo_root / "static" / "qr"

    if not content_root.is_dir():
        sys.stderr.write(f"ERRORE: cartella non trovata: {content_root}\n")
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)

    # Trova tutti i .md sotto content/ (ricorsivo). Include _index.md (sezioni)
    # ed esclude solo file in subcartelle considerate "non Hugo" (zero per il
    # nostro repo, ma futuro-safe).
    if args.sezione:
        sezione_dir = content_root / args.sezione
        if not sezione_dir.is_dir():
            sys.stderr.write(f"ERRORE: sezione non trovata: {sezione_dir}\n")
            return 1
        file_md_iter = sezione_dir.rglob("*.md")
    else:
        file_md_iter = content_root.rglob("*.md")

    # Filtra le sezioni escluse (multilingua) — top-level sezione del path
    # relativo determina se l'intero sottoalbero è escluso.
    def _is_excluded(md: Path) -> bool:
        try:
            rel = md.relative_to(content_root)
        except ValueError:
            return False
        first = rel.parts[0] if rel.parts else ""
        return first in EXCLUDED_SECTIONS

    file_md = sorted(f for f in file_md_iter if not _is_excluded(f))

    if args.only:
        file_md = [f for f in file_md if args.only in f.name]

    if not file_md:
        print(f"Nessun file da processare (filtro: {args.only or 'nessuno'}).")
        return 0

    print(f"📂 Scope: {args.sezione or 'tutte le sezioni'}")
    print(f"🌐 URL base: {args.url_base}")
    print(f"📦 Output: {output_dir.relative_to(repo_root)}/")
    print(f"📄 File trovati: {len(file_md)}")
    print()

    generati = 0
    saltati = 0
    errori = 0
    visti = set()  # detect conflitti di naming

    for md_path in file_md:
        try:
            base_name, url = deriva_target(md_path, content_root, args.url_base)
        except ValueError as exc:
            sys.stderr.write(f"  ✗ {md_path}: {exc}\n")
            errori += 1
            continue

        # Avvisa se due file producono lo stesso basename (potenziale conflitto)
        if base_name in visti:
            sys.stderr.write(
                f"  ⚠ conflitto naming: '{base_name}' già usato (file: {md_path})\n"
            )
        visti.add(base_name)

        png_path = output_dir / f"{base_name}.png"
        svg_path = output_dir / f"{base_name}.svg"

        # Skip se entrambi esistono e non --force
        if not args.force and png_path.exists() and svg_path.exists():
            saltati += 1
            continue

        if args.dry_run:
            print(f"  • [dry-run] {base_name} → {url}")
            generati += 1
            continue

        try:
            genera_qr_png(url, png_path)
            genera_qr_svg(url, svg_path)
            print(f"  ✓ {base_name} → {url}")
            generati += 1
        except Exception as exc:  # noqa: BLE001 — vogliamo continuare
            sys.stderr.write(f"  ✗ {base_name}: {exc}\n")
            errori += 1

    print()
    print(f"🎯 Generati: {generati}  •  Saltati (già presenti): {saltati}  •  Errori: {errori}")
    return 0 if errori == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
