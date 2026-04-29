#!/usr/bin/env bash
# Scarica un'immagine da Pexels (Pexels License: uso commerciale e istituzionale
# OK, attribuzione non obbligatoria ma gradita). Applica la fascia istituzionale
# del sito.
#
# Uso:
#   bash scripts/foto-da-pexels.sh "QUERY" <nome-output>
#
# Esempi:
#   bash scripts/foto-da-pexels.sh "fire firefighter"     2026-08-15-aib
#   bash scripts/foto-da-pexels.sh "mountain rescue team" 2026-09-10-soccorso
#   bash scripts/foto-da-pexels.sh "flood emergency"      2026-11-02-alluvione
#
# Output: static/images/<nome-output>.webp (1200px, fascia blu, max 200 KB)
#         + stampa fonte/autore/licenza per la didascalia.
#
# Richiede:
#   - PEXELS_API_KEY in env (gratuita: https://www.pexels.com/api/)
#   - curl, jq, python3
#
# Licenza Pexels: https://www.pexels.com/license/
# - Uso commerciale e personale OK (anche siti istituzionali PA).
# - Modifiche OK.
# - NON ridistribuire la collezione, NON usare per persone identificabili in
#   contesti negativi/controversi senza permesso del soggetto.

set -euo pipefail

QUERY="${1:?specifica una query di ricerca tra virgolette}"
NAME="${2:?specifica il nome di output (senza estensione)}"

if [ -z "${PEXELS_API_KEY:-}" ]; then
  echo "[error] Manca PEXELS_API_KEY. Crea una API key gratuita su:" >&2
  echo "        https://www.pexels.com/api/" >&2
  echo "        Poi: export PEXELS_API_KEY='la-tua-chiave' (o aggiungilo a ~/.bashrc)" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APPLY_BAND="$ROOT/scripts/applica-fascia-foto.sh"

for cmd in curl jq python3; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "[error] manca: $cmd" >&2; exit 1; }
done

UA="PCGenzanoBot/1.0 (https://www.protezionecivilegenzano.it)"
QUERY_ENC=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$QUERY")

echo "[info] Cerco su Pexels: ${QUERY}"

SEARCH=$(curl -sS -A "$UA" \
  -H "Authorization: $PEXELS_API_KEY" \
  "https://api.pexels.com/v1/search?query=${QUERY_ENC}&per_page=1&orientation=landscape")

URL=$(echo "$SEARCH" | jq -r '.photos[0].src.large2x // .photos[0].src.large // empty')
PHOTOG=$(echo "$SEARCH" | jq -r '.photos[0].photographer // "Pexels"')
PHOTOG_URL=$(echo "$SEARCH" | jq -r '.photos[0].photographer_url // empty')
PHOTO_URL=$(echo "$SEARCH" | jq -r '.photos[0].url // empty')

if [ -z "$URL" ]; then
  echo "[error] Nessun risultato Pexels per '${QUERY}'." >&2
  exit 3
fi

echo "[info] Trovato: foto di $PHOTOG"
echo "[info] URL sorgente: $URL"

TMP="/tmp/pexels-${NAME}.jpg"
curl -sS -A "$UA" -L -o "$TMP" "$URL"

if [ ! -s "$TMP" ]; then
  echo "[error] Download fallito da $URL" >&2
  exit 4
fi

bash "$APPLY_BAND" "$TMP" "$NAME"
rm -f "$TMP"

echo ""
echo "================================================================"
echo "✓ Foto pronta: static/images/${NAME}.webp"
echo "================================================================"
echo "Citazione per la didascalia o image_credit nel frontmatter:"
echo ""
echo "  Foto di ${PHOTOG} su Pexels (licenza Pexels)."
echo ""
echo "Nel frontmatter:"
echo "  image_credit: \"Foto di ${PHOTOG} — Pexels License — pexels.com\""
echo "  image_source_url: \"${PHOTO_URL}\""
echo "================================================================"
