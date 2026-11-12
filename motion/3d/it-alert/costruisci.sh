#!/bin/bash
# costruisci.sh: pagina autonoma del video 3D su IT-alert (rilievo e terre in motion/out/it-alert-3d/dati, da rilievo.py).
# Uso: bash costruisci.sh CARTELLA_SKILL (quella che contiene video-3d)
set -e
qui="$(cd "$(dirname "$0")" && pwd)"; out="$qui/../../out/it-alert-3d"
mkdir -p "$out/dist"
python3 "$1/video-3d/scripts/costruisci.py" "$qui/it-alert.src.html" --uscita "$out/dist/it-alert.html" --ente pc-genzano \
  --rilievo "$out/dati/rilievo.json" --dato terre="$out/dati/terre.json" --dato tempi="$qui/tempi.json" \
  --dato sottotitoli="$qui/sottotitoli.json"
