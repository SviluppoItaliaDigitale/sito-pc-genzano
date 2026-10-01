#!/usr/bin/env python3
"""
Manifesto della build: l'impronta sha256 di ogni file del sito costruito.

Scrive public/build-manifest.json con, per ogni file di public/, l'impronta
del suo contenuto. È il riferimento con cui scripts/verifica-deploy-aruba.py
confronta le pagine servite dal sito: una pagina il cui contenuto non
coincide con il manifesto è rimasta vecchia su Aruba, qualunque sia il
motivo (caricamento FTP interrotto, stato di sincronizzazione sbagliato,
file toccato a mano sul server).

Nasce il 01/10/2026 al posto della meta <meta name="pc-build-sha"> che ogni
pagina portava: quella cambiava a ogni commit e costringeva a ricaricare
~1.100 pagine a ogni deploy (17 minuti anche per un articolo solo). Il
manifesto è un file solo, e dice di più: non «quale build», ma «esattamente
quale contenuto».

Esclusi: le sottocartelle di pagefind/ (migliaia di frammenti con nome già
derivato dal contenuto), documenti/ (cartella gestita a mano su Aruba, fuori
dal deploy) e i file di stato del caricamento FTP.

Uso:
  python3 scripts/genera-manifest-build.py [public]
Solo Python standard.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOME = "build-manifest.json"


def escluso(rel: str) -> bool:
    parti = rel.split("/")
    if rel == NOME:
        return True
    if parti[0] == "documenti":
        return True
    if parti[0] == "pagefind" and len(parti) > 2:
        return True
    if parti[-1].startswith(".ftp-deploy-sync-state"):
        return True
    return False


def impronta(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for blocco in iter(lambda: f.read(1 << 20), b""):
            h.update(blocco)
    return h.hexdigest()


def main(argv: list[str]) -> int:
    public = Path(argv[0] if argv else "public")
    if not public.is_dir():
        print(f"Cartella {public} non trovata: costruire prima il sito.", file=sys.stderr)
        return 2
    buildinfo = {}
    bi = ROOT / "data" / "buildinfo.json"
    if bi.is_file():
        try:
            buildinfo = json.loads(bi.read_text(encoding="utf-8"))
        except ValueError:
            buildinfo = {}
    file: dict[str, str] = {}
    for p in sorted(public.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(public).as_posix()
        if escluso(rel):
            continue
        file[rel] = impronta(p)
    manifesto = {
        "versione": 1,
        "sha": buildinfo.get("sha", "dev"),
        "time": buildinfo.get("time", ""),
        "n_file": len(file),
        "file": file,
    }
    (public / NOME).write_text(json.dumps(manifesto, indent=0, sort_keys=False, ensure_ascii=True) + "\n",
                               encoding="utf-8")
    print(f"{NOME}: {len(file)} file, build {manifesto['sha']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
