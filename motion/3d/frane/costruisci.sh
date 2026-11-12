#!/bin/bash
# costruisci.sh: pagina autonoma del video in motion/out/frane-3d/dist (three.js, motore, impaginazione, font, dati).
# Uso: bash costruisci.sh CARTELLA_SKILL (quella che contiene video-3d)
set -e
qui="$(cd "$(dirname "$0")" && pwd)"; out="$qui/../../out/frane-3d"
mkdir -p "$out/dist"
python3 "$1/video-3d/scripts/costruisci.py" "$qui/frane.src.html" --uscita "$out/dist/frane-3d.html" --ente pc-genzano \
  --rilievo "$out/dati/rilievo.json" --dato tempi="$qui/tempi.json" --dato sottotitoli="$qui/sottotitoli.json"
