#!/usr/bin/env bash
# Scarica un'immagine da NASA Image and Video Library (immagini sempre Public
# Domain, accreditate alla NASA). Applica la fascia istituzionale del sito.
#
# Uso:
#   bash scripts/foto-da-nasa.sh "QUERY" <nome-output>
#
# Esempi:
#   bash scripts/foto-da-nasa.sh "Etna eruption" 2026-08-12-etna-eruzione
#   bash scripts/foto-da-nasa.sh "Hurricane Katrina" 2026-08-29-katrina-uragano
#   bash scripts/foto-da-nasa.sh "Vesuvius from space" 2026-10-01-vesuvio-spazio
#
# Output: static/images/<nome-output>.webp (1200px, fascia blu, max 200 KB)
#         + stampa fonte/autore/licenza per la didascalia.

set -euo pipefail

QUERY="${1:?specifica una query di ricerca tra virgolette}"
NAME="${2:?specifica il nome di output (senza estensione)}"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APPLY_BAND="$ROOT/scripts/applica-fascia-foto.sh"

for cmd in curl jq python3; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "[error] manca: $cmd" >&2; exit 1; }
done

UA="PCGenzanoBot/1.0 (https://www.protezionecivilegenzano.it; segreteria@protezionecivilegenzano.it)"
QUERY_ENC=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$QUERY")

echo "[info] Cerco su NASA Images: ${QUERY}"

SEARCH=$(curl -sS -A "$UA" "https://images-api.nasa.gov/search?q=${QUERY_ENC}&media_type=image")
NASA_ID=$(echo "$SEARCH" | jq -r '.collection.items[0].data[0].nasa_id // empty')
TITLE=$(echo "$SEARCH" | jq -r '.collection.items[0].data[0].title // empty')
DESC=$(echo "$SEARCH" | jq -r '.collection.items[0].data[0].description // empty' | head -c 200)
CENTER=$(echo "$SEARCH" | jq -r '.collection.items[0].data[0].center // empty')
PHOTOG=$(echo "$SEARCH" | jq -r '.collection.items[0].data[0].photographer // empty')
SECONDARY=$(echo "$SEARCH" | jq -r '.collection.items[0].data[0].secondary_creator // empty')

if [ -z "$NASA_ID" ]; then
  echo "[error] Nessun risultato NASA per '${QUERY}'." >&2
  echo "        Prova con un'altra query (es. nomi inglesi: 'eruption', 'flood', 'wildfire')." >&2
  exit 2
fi

echo "[info] Trovato: ${TITLE} (id ${NASA_ID})"

# Recupera la lista degli asset (immagini in più formati)
ASSETS=$(curl -sS -A "$UA" "https://images-api.nasa.gov/asset/${NASA_ID}")
# Preferisci ~orig.jpg > ~large.jpg > qualunque .jpg
IMG_URL=$(echo "$ASSETS" | jq -r '
  .collection.items[].href
  | select(test("~orig\\.(jpg|jpeg|png)$"; "i"))' | head -1)
if [ -z "$IMG_URL" ]; then
  IMG_URL=$(echo "$ASSETS" | jq -r '
    .collection.items[].href
    | select(test("~large\\.(jpg|jpeg|png)$"; "i"))' | head -1)
fi
if [ -z "$IMG_URL" ]; then
  IMG_URL=$(echo "$ASSETS" | jq -r '
    .collection.items[].href
    | select(test("\\.(jpg|jpeg|png)$"; "i"))' | head -1)
fi

if [ -z "$IMG_URL" ]; then
  echo "[error] Nessun URL immagine valido nei NASA assets per ${NASA_ID}" >&2
  exit 3
fi

TMP_IMG="$(mktemp --suffix=.bin)"
trap 'rm -f "$TMP_IMG"' EXIT

echo "[info] Scarico ${IMG_URL}"
curl -sS -A "$UA" -L -o "$TMP_IMG" "$IMG_URL"

bash "$APPLY_BAND" "$TMP_IMG" "$NAME"

# Autore: photographer > secondary_creator > center > NASA
AUTHOR="${PHOTOG:-${SECONDARY:-${CENTER:-NASA}}}"
DETAILS_URL="https://images.nasa.gov/details/${NASA_ID}"

echo ""
echo "─── Foto NASA applicata correttamente ───"
echo "  File:     static/images/${NAME}.webp"
echo "  Origine:  ${DETAILS_URL}"
echo "  Autore:   ${AUTHOR}"
echo "  Licenza:  Public domain (NASA)"
echo "  Titolo:   ${TITLE}"
echo ""
echo "Importante: cita SEMPRE 'NASA' (e fotografo se noto) nella didascalia."
