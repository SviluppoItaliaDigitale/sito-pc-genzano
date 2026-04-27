#!/usr/bin/env bash
# Applica la fascia blu istituzionale a una foto esistente.
# Input: file sorgente (JPG/PNG/WebP) + nome di output (senza estensione).
# Output: WebP 1200px in static/images/<nome>.webp con fascia blu in basso,
# logo, testo "PROTEZIONE CIVILE / Gruppo Comunale Volontari — Genzano di Roma".
#
# Uso:
#   bash scripts/applica-fascia-foto.sh <src.jpg> <nome-output-senza-ext>
#
# Esempi:
#   bash scripts/applica-fascia-foto.sh /home/iu0qvw/Scaricati/Zamberletti.jpg zamberletti-ritratto
#   bash scripts/applica-fascia-foto.sh /home/iu0qvw/Scaricati/Genzano-alto.jpg 2026-06-23-genzano-infiorata-aerea

set -euo pipefail

# Fallback ImageMagick: usa 'magick' (v7) se disponibile, altrimenti
# 'convert' (v6) — utile per i runner GitHub Actions che hanno solo v6.
if ! command -v magick >/dev/null 2>&1; then
  if command -v convert >/dev/null 2>&1; then
    magick() { convert "$@"; }
    identify() { command identify "$@"; }
    export -f magick
  else
    echo "[error] manca ImageMagick (ne' 'magick' v7 ne' 'convert' v6)" >&2
    exit 1
  fi
fi

SRC="${1:?specifica il file sorgente}"
NAME="${2:?specifica il nome di output (senza estensione)}"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOGO="$ROOT/static/images/logo-pc-genzano.png"
OUT="$ROOT/static/images/${NAME}.webp"

W=1200
BAND_H=100
PRIMARY="#003366"

if [ ! -f "$SRC" ]; then
  echo "[error] sorgente non trovata: $SRC" >&2
  exit 1
fi
if [ ! -f "$LOGO" ]; then
  echo "[error] logo non trovato: $LOGO" >&2
  exit 1
fi

# 1) Ridimensiona la foto a larghezza $W (mantieni aspect ratio)
TMP_PHOTO="$(mktemp --suffix=.png)"
trap 'rm -f "$TMP_PHOTO"' EXIT

magick "$SRC" -resize "${W}x" -quality 90 "$TMP_PHOTO"

# Altezza effettiva dopo resize
# Uso sempre 'identify' standalone: e' disponibile sia in v6 sia in v7.
# Evito 'magick identify' perche' su v6 il fallback diventa
# 'convert identify' che fallisce con "no decode delegate".
PH=$(identify -format "%h" "$TMP_PHOTO")
TOTAL_H=$((PH + BAND_H))

# 2) Componi: foto sopra + fascia blu sotto con logo a SINISTRA + testo a destra del logo
magick \
  -size "${W}x${TOTAL_H}" xc:"$PRIMARY" \
  \( "$TMP_PHOTO" \) -gravity North -composite \
  -fill "rgba(255,255,255,0.25)" \
  -draw "rectangle 0,${PH} ${W},$((PH + 2))" \
  -gravity NorthWest \
  \( "$LOGO" -resize "72x72" \) -geometry "+90+$((PH + 15))" -composite \
  -fill "#ffffff" \
  -font "Liberation-Sans-Bold" -pointsize 26 \
  -annotate "+180+$((PH + 22))" "PROTEZIONE CIVILE" \
  -fill "rgba(255,255,255,0.90)" \
  -font "Liberation-Sans" -pointsize 16 \
  -annotate "+180+$((PH + 60))" "Gruppo Comunale Volontari — Genzano di Roma" \
  -quality 85 \
  -define webp:method=6 \
  "$OUT"

# 3) Se > 200 KB, ricomprimi progressivamente (per immagini molto grandi
#    una sola riduzione di qualita' non basta — riduco qualita' a step)
SIZE_KB=$(( $(stat -c%s "$OUT") / 1024 ))
for Q in 75 60 50 40 30; do
  [ "$SIZE_KB" -le 200 ] && break
  magick "$OUT" -quality "$Q" -define webp:method=6 "$OUT"
  SIZE_KB=$(( $(stat -c%s "$OUT") / 1024 ))
done
# Se ancora troppo grande (immagine altissima risoluzione), riduci larghezza
# in modo progressivo: 1000 -> 900 -> 800 -> 700 px
for NEW_W in 1000 900 800 700; do
  [ "$SIZE_KB" -le 200 ] && break
  magick "$OUT" -resize "${NEW_W}x" -quality 75 -define webp:method=6 "$OUT"
  SIZE_KB=$(( $(stat -c%s "$OUT") / 1024 ))
done

echo "[ok] $(basename "$OUT")  (${SIZE_KB} KB, ${W}x${TOTAL_H}px)"
