#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pubblica-notebooklm-output.py — Legge la drop zone con gli output di
NotebookLM scaricati dall'utente e li pubblica sul sito.

Workflow per l'utente:
  1. Apre NotebookLM con il pacchetto pronto in ~/Scrivania/notebooklm-pacchetti/<tema>/
  2. Genera podcast / infografica / presentazione / quiz / flashcard
  3. Scarica i file e li trascina in ~/Scrivania/notebooklm-output/<tema>/
     con nomi standard: podcast.mp3, infografica.png, presentazione.pptx,
     quiz.txt o quiz.json, flashcard.pdf
  4. Lancia questo script:
       python3 scripts/pubblica-notebooklm-output.py rischio-sismico

Cosa fa lo script:
  - Sposta i file in static/ con naming canonico
  - Aggiunge le voci a data/risorse_pronte.yaml
  - Stampa l'elenco delle modifiche + suggerimento per commit

Idempotente sui file static (sovrascrive se ri-pubblichi lo stesso tema con
output nuovi). Per data/risorse_pronte.yaml de-duplica per id univoco.
"""

from __future__ import annotations
import argparse
import os
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write(
        "ERRORE: manca pyyaml. Installa con:\n"
        "  pip install --break-system-packages pyyaml\n"
    )
    sys.exit(1)

HOME = Path.home()
OUTPUT_DIR = HOME / "Scrivania" / "notebooklm-output"
REPO_ROOT = Path(__file__).resolve().parent.parent
STATIC = REPO_ROOT / "static"
DATA_FILE = REPO_ROOT / "data" / "risorse_pronte.yaml"

# Mapping nome file scaricato → (tipo, cartella static, estensione canonica).
# Per il podcast NotebookLM scarica .m4a (AAC). Lo accettiamo nativamente:
# il browser HTML5 audio lo riproduce, è più piccolo dell'MP3 a parità di
# qualità. Hugo serve i file static tali e quali, niente conversione.
MAPPING_FILE = {
    "podcast.mp3":        ("podcast",         "podcast/episodi",  ".mp3"),
    "podcast.m4a":        ("podcast",         "podcast/episodi",  ".m4a"),
    "podcast.ogg":        ("podcast",         "podcast/episodi",  ".ogg"),
    "infografica.png":    ("infografica",     "infografiche",     ".png"),
    "infografica.jpg":    ("infografica",     "infografiche",     ".jpg"),
    "infografica.webp":   ("infografica",     "infografiche",     ".webp"),
    "presentazione.pptx": ("presentazione",   "presentazioni",    ".pptx"),
    "presentazione.pdf":  ("presentazione-pdf", "presentazioni",  ".pdf"),
    "quiz.txt":           ("quiz",            "risorse-quiz",     ".txt"),
    "quiz.json":          ("quiz",            "risorse-quiz",     ".json"),
    "flashcard.pdf":      ("flashcard",       "flashcard",        ".pdf"),
    "mappa.png":          ("mappa-mentale",   "mappe-mentali",    ".png"),
    "mappa.svg":          ("mappa-mentale",   "mappe-mentali",    ".svg"),
}

# Descrizioni per tipo (usate quando l'utente non fornisce descrizione custom)
DESC_TIPO = {
    "podcast":         "Podcast audio (dialogo fra due voci AI) sul tema. Ascoltabile online o scaricabile per ascolto offline.",
    "infografica":     "Infografica formato quadrato pronta per condivisione social, stampa A4 e affissione in bacheca.",
    "presentazione":   "Presentazione PowerPoint per docenti: 15 slide per un'ora di Educazione Civica in classe (formato modificabile).",
    "presentazione-pdf": "Stessa presentazione in formato PDF: apribile su qualsiasi dispositivo senza PowerPoint.",
    "quiz":            "Quiz a 10 domande a risposta multipla con difficoltà progressiva. Da usare in aula o in autoverifica.",
    "flashcard":       "Mazzo di 20 flashcard domanda/risposta in formato PDF stampabile per studio individuale o di gruppo.",
    "mappa-mentale":   "Mappa mentale visuale per orientarsi rapidamente sull'argomento.",
}

ICONA_TIPO = {
    "podcast":         "bi-headphones",
    "infografica":     "bi-image",
    "presentazione":   "bi-file-earmark-slides",
    "presentazione-pdf": "bi-file-earmark-pdf",
    "quiz":            "bi-check2-square",
    "flashcard":       "bi-card-list",
    "mappa-mentale":   "bi-diagram-3",
}

# Titolo personalizzato per tipo (sovrascrive il default "Tipo: Titolo tema")
TITOLO_TIPO = {
    "presentazione-pdf": "Presentazione (PDF)",
}


def carica_data_temi() -> dict:
    """Restituisce {slug: dict_tema} da data/risorse_pronte.yaml."""
    if not DATA_FILE.exists():
        sys.stderr.write(f"ERRORE: {DATA_FILE} non esiste.\n")
        sys.exit(1)
    contenuto = yaml.safe_load(DATA_FILE.read_text(encoding="utf-8")) or {}
    temi = {t["slug"]: t for t in contenuto.get("temi", [])}
    return contenuto, temi


def umano_dimensione(bytes_n: int) -> str:
    """Formatta dimensione file in KB / MB."""
    if bytes_n < 1024:
        return f"{bytes_n} B"
    if bytes_n < 1024 * 1024:
        return f"{bytes_n / 1024:.0f} KB"
    return f"{bytes_n / (1024 * 1024):.1f} MB"


def durata_audio(path: Path) -> str:
    """Restituisce durata MP3/audio come 'MM:SS' usando ffprobe se disponibile."""
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
            capture_output=True, text=True, timeout=10,
        )
        if out.returncode == 0:
            secondi = float(out.stdout.strip())
            mm = int(secondi // 60)
            ss = int(secondi % 60)
            return f"{mm} min {ss:02d} sec"
    except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
        pass
    return ""


def pubblica_tema(tema_slug: str, dry_run: bool = False) -> int:
    """Processa la drop zone di un tema. Ritorna numero di file pubblicati."""
    contenuto, temi = carica_data_temi()
    if tema_slug not in temi:
        sys.stderr.write(
            f"ERRORE: tema '{tema_slug}' non in data/risorse_pronte.yaml.\n"
            f"Temi disponibili: {', '.join(temi.keys())}\n"
        )
        return -1

    tema_info = temi[tema_slug]
    drop_dir = OUTPUT_DIR / tema_slug
    if not drop_dir.is_dir():
        sys.stderr.write(f"ERRORE: cartella drop zone non trovata: {drop_dir}\n")
        return -1

    # File già esistenti in `materiali` — usati per dedup su id
    materiali_esistenti = contenuto.get("materiali") or []
    if materiali_esistenti is None:
        materiali_esistenti = []
    ids_esistenti = {m.get("id") for m in materiali_esistenti}

    oggi = date.today().isoformat()
    pubblicati = 0
    nuove_voci = []

    for nome_file, (tipo, sub_static, ext) in MAPPING_FILE.items():
        src = drop_dir / nome_file
        if not src.exists():
            continue

        # Naming canonico: <data>-<tema>-<tipo>.<ext> per non sovrascrivere
        # versioni vecchie. Per podcast lo metto in /podcast/episodi/ in
        # formato compatibile con feed RSS Hugo.
        dest_dir = STATIC / sub_static
        dest_name = f"{oggi}-{tema_slug}-{tipo}{ext}"
        dest = dest_dir / dest_name

        if dry_run:
            print(f"  [dry-run] {src.name} → {dest.relative_to(REPO_ROOT)}")
            continue

        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        os.chmod(dest, 0o644)
        print(f"  ✓ {src.name:25s} → {dest.relative_to(REPO_ROOT)}")
        pubblicati += 1

        # Costruisci voce yaml
        voce_id = f"{tema_slug}-{tipo}-{oggi}"
        if voce_id in ids_esistenti:
            # Aggiorna esistente (sovrascrive) invece di duplicare
            materiali_esistenti = [m for m in materiali_esistenti if m.get("id") != voce_id]

        titolo_base = TITOLO_TIPO.get(tipo, tipo.capitalize())
        voce = {
            "id": voce_id,
            "tema": tema_slug,
            "tema_titolo": tema_info["titolo"],
            "tipo": tipo,
            "titolo": f"{titolo_base}: {tema_info['titolo']}",
            "descrizione": DESC_TIPO.get(tipo, "Materiale di approfondimento."),
            "file_url": f"/{sub_static}/{dest_name}",
            "dimensione": umano_dimensione(dest.stat().st_size),
            "data_pubblicazione": oggi,
            "licenza": "CC BY-NC-SA 4.0",
        }

        if tipo == "podcast":
            d = durata_audio(dest)
            if d:
                voce["durata"] = d

        nuove_voci.append(voce)

    if dry_run:
        print(f"\n[dry-run] {len(nuove_voci) if not dry_run else 'N'} voci sarebbero aggiunte a {DATA_FILE.relative_to(REPO_ROOT)}")
        return pubblicati

    if not nuove_voci:
        print(f"  ⚠ Nessun file trovato in {drop_dir}.")
        print(f"     Devi trascinarci dentro almeno uno dei file:")
        for f in MAPPING_FILE.keys():
            print(f"       - {f}")
        return 0

    # Salva yaml aggiornato
    contenuto["materiali"] = materiali_esistenti + nuove_voci
    # Scrivi con stile YAML pulito: indent 2, key order preserved
    DATA_FILE.write_text(
        yaml.safe_dump(contenuto, allow_unicode=True, sort_keys=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n📝 {DATA_FILE.relative_to(REPO_ROOT)}: aggiunte {len(nuove_voci)} voci.")

    print(f"\n📦 Pubblicati {pubblicati} file per tema '{tema_slug}'.")
    print(f"\n➡ Prossimi passi:")
    print(f"   1. Verifica con: hugo --quiet --minify")
    print(f"   2. Commit + push:")
    print(f"      git add -A && git commit -m 'Risorse pronte: pubblicati {pubblicati} materiali tema {tema_slug}' && git push")
    print(f"\n💡 Puoi svuotare la drop zone {drop_dir} se non ti serve più.")

    return pubblicati


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pubblica gli output di NotebookLM dalla drop zone al sito.",
    )
    parser.add_argument(
        "tema",
        nargs="?",
        help="Slug del tema da pubblicare (es. rischio-sismico). Lascia vuoto per --lista.",
    )
    parser.add_argument(
        "--lista", action="store_true",
        help="Elenca temi disponibili e contenuto drop zone.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Mostra cosa farebbe senza scrivere.",
    )
    args = parser.parse_args()

    contenuto, temi = carica_data_temi()

    if args.lista or not args.tema:
        print("Temi disponibili (e file presenti in drop zone):\n")
        for slug, info in temi.items():
            drop = OUTPUT_DIR / slug
            files = sorted(f.name for f in drop.iterdir() if f.is_file()) if drop.exists() else []
            file_str = ", ".join(files) if files else "(vuota)"
            print(f"  {slug:30s} — {info['titolo']}")
            print(f"     drop zone: {file_str}")
        print(f"\nUso: python3 {Path(__file__).name} <slug>")
        return 0

    return 0 if pubblica_tema(args.tema, dry_run=args.dry_run) >= 0 else 1


if __name__ == "__main__":
    sys.exit(main())
