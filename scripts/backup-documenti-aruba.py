#!/usr/bin/env python3
"""
backup-documenti-aruba.py

Scarica i documenti istituzionali che il sito serve da URL assoluti
`www.protezionecivilegenzano.it` MA che NON sono presenti nel repo git
(vivono solo sul server Aruba: /area-download/normativa/, /documenti/download/).

Perché esiste
-------------
Circa 29 PDF — incluso il **Piano di Emergenza Comunale** — sono linkati dal
sito ma non hanno copia nel repo. `controllo-documenti.py` controlla solo i
file dentro al repo, quindi questi non sono coperti da nulla. Una perdita dati
su Aruba, una migrazione hosting o una cancellazione manuale li distruggerebbe
senza possibilità di recupero. Precedente: incidente AR4 Salesiani (rule 05).
Questo script produce la copia di sicurezza che il workflow
`backup-documenti-aruba.yml` pubblica come GitHub Release.

Uso
---
  python3 scripts/backup-documenti-aruba.py [--dry-run] [--out DIR]

  --dry-run : solo richiesta HEAD, verifica che gli URL rispondano 200,
              non scarica i file (utile per test rapidi).
  --out DIR : cartella di staging (default: backup-aruba/).

Output
------
  - DIR/<file>...     i file scaricati e verificati
  - DIR/MANIFEST.md   inventario: nome, dimensione, sha256, URL, data
  Exit 0 se tutti i file sono OK, 1 se almeno uno ha fallito download/verifica.

La lista degli URL è DERIVATA dal contenuto del sito (`content/**/*.md`): ogni
link assoluto a protezionecivilegenzano.it verso un file la cui copia locale
`static/<path>` NON esiste è un file "solo-Aruba" da backuppare. Così se in
futuro aggiungi un nuovo PDF server-side, il backup lo prende automaticamente.
"""
import argparse
import datetime
import glob
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOST = "www.protezionecivilegenzano.it"
FILE_EXTS = (".pdf", ".zip", ".png", ".jpg", ".jpeg")
LINK_RE = re.compile(r'\]\((https?://[^)\s]+)\)')


def trova_url_solo_aruba() -> list[str]:
    """Deriva dai contenuti gli URL assoluti a file ospitati solo su Aruba."""
    trovati: dict[str, None] = {}
    for md in glob.glob(str(ROOT / "content" / "**" / "*.md"), recursive=True):
        testo = Path(md).read_text(encoding="utf-8")
        for url in LINK_RE.findall(testo):
            base = url.split("#")[0].split("?")[0]
            if HOST not in base:
                continue
            if not base.lower().endswith(FILE_EXTS):
                continue
            path = base.split(HOST, 1)[1]
            # se esiste la copia locale nel repo, NON è un file solo-Aruba
            if (ROOT / "static" / path.lstrip("/")).is_file():
                continue
            trovati[base] = None
    return sorted(trovati)


def head(url: str) -> tuple[int | None, int | None]:
    """Ritorna (status_code, content_length) via richiesta HEAD."""
    try:
        out = subprocess.run(
            ["curl", "-sIL", "--max-time", "30", url],
            capture_output=True, text=True, timeout=40,
        ).stdout
        status = re.findall(r"HTTP/[\d.]+\s+(\d+)", out)
        length = re.findall(r"(?i)content-length:\s*(\d+)", out)
        return (int(status[-1]) if status else None,
                int(length[-1]) if length else None)
    except Exception:
        return None, None


def scarica(url: str, dest: Path) -> bool:
    """Scarica url in dest. Ritorna True se il download riesce."""
    try:
        r = subprocess.run(
            ["curl", "-sL", "--max-time", "300", "--fail", "-o", str(dest), url],
            capture_output=True, text=True, timeout=360,
        )
        return r.returncode == 0 and dest.is_file() and dest.stat().st_size > 0
    except Exception:
        return False


def verifica(dest: Path) -> str | None:
    """Verifica integrità minima. Ritorna None se OK, altrimenti il motivo."""
    if not dest.is_file() or dest.stat().st_size == 0:
        return "file vuoto o assente"
    if dest.suffix.lower() == ".pdf":
        with open(dest, "rb") as f:
            if f.read(5) != b"%PDF-":
                return "header PDF non valido (%PDF- atteso)"
    if dest.suffix.lower() == ".zip":
        with open(dest, "rb") as f:
            if f.read(2) != b"PK":
                return "header ZIP non valido"
    return None


def sha256(dest: Path) -> str:
    h = hashlib.sha256()
    with open(dest, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def fmt_size(b: int) -> str:
    if b < 1024 * 1024:
        return f"{round(b / 1024)} KB"
    return f"{b / 1048576:.1f}".replace(".", ",") + " MB"


def main() -> int:
    ap = argparse.ArgumentParser(description="Backup file solo-Aruba")
    ap.add_argument("--dry-run", action="store_true",
                    help="solo HEAD, non scarica")
    ap.add_argument("--out", default="backup-aruba",
                    help="cartella di staging (default: backup-aruba/)")
    args = ap.parse_args()

    urls = trova_url_solo_aruba()
    print(f"File solo-Aruba derivati dai contenuti: {len(urls)}\n")
    if not urls:
        print("Nessun file solo-Aruba trovato. Niente da backuppare.")
        return 0

    out_dir = ROOT / args.out
    if not args.dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    ok: list[tuple[str, Path, int, str]] = []
    falliti: list[tuple[str, str]] = []

    for url in urls:
        nome = url.rsplit("/", 1)[-1]
        if args.dry_run:
            status, length = head(url)
            if status == 200:
                size = fmt_size(length) if length else "?"
                print(f"  OK    {status}  {size:>10}  {nome}")
                ok.append((url, Path(nome), length or 0, ""))
            else:
                print(f"  FAIL  {status}  {nome}")
                falliti.append((url, f"HTTP {status}"))
            continue

        dest = out_dir / nome
        if not scarica(url, dest):
            print(f"  FAIL  download  {nome}")
            falliti.append((url, "download fallito"))
            dest.unlink(missing_ok=True)
            continue
        motivo = verifica(dest)
        if motivo:
            print(f"  FAIL  verifica  {nome}  ({motivo})")
            falliti.append((url, motivo))
            dest.unlink(missing_ok=True)
            continue
        digest = sha256(dest)
        size = dest.stat().st_size
        print(f"  OK    {fmt_size(size):>10}  {nome}")
        ok.append((url, dest, size, digest))

    # MANIFEST
    oggi = datetime.date.today().isoformat()
    righe = [
        "# Backup documenti solo-Aruba — MANIFEST",
        "",
        f"Generato il **{oggi}** da `scripts/backup-documenti-aruba.py`.",
        "",
        "Copia di sicurezza dei documenti istituzionali che il sito serve da "
        "URL assoluti `www.protezionecivilegenzano.it` ma che non hanno copia "
        "nel repo git (vivono solo sul server Aruba).",
        "",
        f"- File verificati e salvati: **{len(ok)}**",
        f"- File falliti: **{len(falliti)}**",
        "",
        "## File nel backup",
        "",
        "| File | Dimensione | SHA-256 | URL di origine |",
        "|---|---|---|---|",
    ]
    for url, dest, size, digest in ok:
        nome = url.rsplit("/", 1)[-1]
        d = digest[:16] + "…" if digest else "(dry-run)"
        righe.append(f"| {nome} | {fmt_size(size) if size else '?'} | `{d}` | {url} |")
    if falliti:
        righe += ["", "## File falliti (NON nel backup di questo run)", ""]
        for url, motivo in falliti:
            righe.append(f"- `{url}` — {motivo}")
        righe += [
            "",
            "> I file falliti mantengono la copia del backup precedente nella "
            "Release (il workflow non sovrascrive ciò che non è stato "
            "ri-scaricato con successo).",
        ]
    manifest = "\n".join(righe) + "\n"

    if args.dry_run:
        print("\n--- MANIFEST (dry-run, non salvato) ---")
        print(manifest)
    else:
        (out_dir / "MANIFEST.md").write_text(manifest, encoding="utf-8")
        print(f"\nManifest scritto in {out_dir / 'MANIFEST.md'}")

    print(f"\nRiepilogo: {len(ok)} OK, {len(falliti)} falliti")
    return 1 if falliti else 0


if __name__ == "__main__":
    sys.exit(main())
