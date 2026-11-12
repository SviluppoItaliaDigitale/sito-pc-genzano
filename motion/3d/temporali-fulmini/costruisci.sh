#!/bin/bash
# costruisci.sh: tempi → pagina autonoma. Uso: bash costruisci.sh CARTELLA_SKILL [CARTELLA_USCITA]
# (CARTELLA_SKILL contiene video-3d e motion-pc-genzano; l'uscita predefinita è motion/out/temporali-fulmini-3d, fuori da git)
set -e
cd "$(dirname "$0")"
S="$1"; O="${2:-../../out/temporali-fulmini-3d}"
mkdir -p "$O/dati" "$O/dist"
python3 ritmo.py
[ -f "$O/dati/rilievo.json" ] || python3 "$S/video-3d/scripts/rilievo.py" --bbox 41.66,12.58,41.80,12.78 --griglia 256 --uscita "$O/dati/rilievo.json"
python3 "$S/video-3d/scripts/costruisci.py" temporali-fulmini.src.html --uscita "$O/dist/temporali-fulmini-3d.html" --ente pc-genzano \
  --rilievo "$O/dati/rilievo.json" --dato tempi=tempi.json --dato sottotitoli=sottotitoli.json
