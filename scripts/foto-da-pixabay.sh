#!/usr/bin/env bash
# Scarica un'immagine da Pixabay (Pixabay Content License: uso commerciale e
# istituzionale OK, attribuzione non obbligatoria). Applica la fascia
# istituzionale del sito.
#
# Uso:
#   bash scripts/foto-da-pixabay.sh "QUERY" <nome-output>
#
# Esempi:
#   bash scripts/foto-da-pixabay.sh "ambulance emergency" 2026-09-10-118
#   bash scripts/foto-da-pixabay.sh "mountain hiking"     2026-09-15-escursionismo
#
# Output: static/images/<nome-output>.webp (1200px, fascia blu, max 200 KB)
#         + stampa fonte/autore/licenza per la didascalia.
#
# Richiede:
#   - PIXABAY_API_KEY in env (gratuita: https://pixabay.com/api/docs/)
#   - curl, jq, python3
#
# Licenza Pixabay Content: https://pixabay.com/service/license-summary/
# - Uso commerciale e personale OK (anche siti istituzionali PA).
# - Modifiche OK. Attribuzione non richiesta.
# - NON ridistribuire la collezione, NON usare per persone identificabili in
#   contesti negativi/controversi senza permesso del soggetto.

set -euo pipefail

QUERY="${1:?specifica una query di ricerca tra virgolette}"
NAME="${2:?specifica il nome di output (senza estensione)}"

if [ -z "${PIXABAY_API_KEY:-}" ]; then
  echo "[error] Manca PIXABAY_API_KEY. Crea una API key gratuita su:" >&2
  echo "        https://pixabay.com/api/docs/" >&2
  echo "        Poi: export PIXABAY_API_KEY='la-tua-chiave'" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APPLY_BAND="$ROOT/scripts/applica-fascia-foto.sh"

for cmd in curl jq python3; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "[error] manca: $cmd" >&2; exit 1; }
done

UA="PCGenzanoBot/1.0 (https://www.protezionecivilegenzano.it)"
QUERY_ENC=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$QUERY")

echo "[info] Cerco su Pixabay: ${QUERY}"

SEARCH=$(curl -sS -A "$UA" \
  "https://pixabay.com/api/?key=${PIXABAY_API_KEY}&q=${QUERY_ENC}&image_type=photo&orientation=horizontal&per_page=3&safesearch=true")

URL=$(echo "$SEARCH" | jq -r '.hits[0].largeImageURL // .hits[0].webformatURL // empty')
PHOTOG=$(echo "$SEARCH" | jq -r '.hits[0].user // "Pixabay"')
PAGE_URL=$(echo "$SEARCH" | jq -r '.hits[0].pageURL // empty')

if [ -z "$URL" ]; then
  echo "[error] Nessun risultato Pixabay per '${QUERY}'." >&2
  exit 3
fi

echo "[info] Trovato: foto di $PHOTOG"
echo "[info] URL sorgente: $URL"

TMP="/tmp/pixabay-${NAME}.jpg"
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
echo "  Foto di ${PHOTOG} su Pixabay (Pixabay Content License)."
echo ""
echo "Nel frontmatter:"
echo "  image_credit: \"Foto di ${PHOTOG} — Pixabay Content License — pixabay.com\""
echo "  image_source_url: \"${PAGE_URL}\""
echo "================================================================"
