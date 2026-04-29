#!/usr/bin/env bash
# Wrapper di compatibilita' che invoca scripts/applica-fascia-foto.py.
# La logica di composizione è stata riscritta in Python+Pillow per essere
# cross-platform (no dipendenza fragile da ImageMagick v6/v7 + delegate WebP
# + policy.xml + font discovery).
#
# Uso:
#   bash scripts/applica-fascia-foto.sh <src.jpg> <nome-output-senza-ext>
#
# Vedi scripts/applica-fascia-foto.py per la logica completa.

set -euo pipefail

SRC="${1:?specifica il file sorgente}"
NAME="${2:?specifica il nome di output (senza estensione)}"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec python3 "$ROOT/scripts/applica-fascia-foto.py" "$SRC" "$NAME"
