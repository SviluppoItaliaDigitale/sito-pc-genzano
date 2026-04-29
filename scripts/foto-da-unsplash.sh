#!/usr/bin/env bash
# Scarica un'immagine da Unsplash (Unsplash License: uso commerciale e
# istituzionale OK, attribuzione non obbligatoria ma "encouraged"). Applica
# la fascia istituzionale del sito.
#
# Uso:
#   bash scripts/foto-da-unsplash.sh "QUERY" <nome-output>
#
# Esempi:
#   bash scripts/foto-da-unsplash.sh "rescue volunteer"   2026-09-15-volontariato
#   bash scripts/foto-da-unsplash.sh "first aid kit"      2026-09-20-primo-soccorso
#
# Output: static/images/<nome-output>.webp (1200px, fascia blu, max 200 KB)
#         + stampa fonte/autore/licenza per la didascalia.
#
# Richiede:
#   - UNSPLASH_ACCESS_KEY in env (gratuita: https://unsplash.com/developers)
#     50 req/h in modalità demo.
#   - curl, jq, python3
#
# Licenza Unsplash: https://unsplash.com/license
# - Uso commerciale e personale OK (anche siti istituzionali PA).
# - Modifiche OK.
# - NON vendere foto invariate o ricreare un servizio simile a Unsplash.
# - Attribuzione "encouraged" — non obbligatoria ma cortesia verso autori.

set -euo pipefail

QUERY="${1:?specifica una query di ricerca tra virgolette}"
NAME="${2:?specifica il nome di output (senza estensione)}"

if [ -z "${UNSPLASH_ACCESS_KEY:-}" ]; then
  echo "[error] Manca UNSPLASH_ACCESS_KEY. Registra un'app gratuita su:" >&2
  echo "        https://unsplash.com/developers" >&2
  echo "        Poi: export UNSPLASH_ACCESS_KEY='la-tua-access-key'" >&2
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APPLY_BAND="$ROOT/scripts/applica-fascia-foto.sh"

for cmd in curl jq python3; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "[error] manca: $cmd" >&2; exit 1; }
done

UA="PCGenzanoBot/1.0 (https://www.protezionecivilegenzano.it)"
QUERY_ENC=$(python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$QUERY")

echo "[info] Cerco su Unsplash: ${QUERY}"

SEARCH=$(curl -sS -A "$UA" \
  -H "Authorization: Client-ID $UNSPLASH_ACCESS_KEY" \
  "https://api.unsplash.com/search/photos?query=${QUERY_ENC}&per_page=1&orientation=landscape")

URL=$(echo "$SEARCH" | jq -r '.results[0].urls.regular // empty')
PHOTOG=$(echo "$SEARCH" | jq -r '.results[0].user.name // "Unsplash"')
PHOTOG_USERNAME=$(echo "$SEARCH" | jq -r '.results[0].user.username // empty')
PHOTO_URL=$(echo "$SEARCH" | jq -r '.results[0].links.html // empty')
DOWNLOAD_TRACK=$(echo "$SEARCH" | jq -r '.results[0].links.download_location // empty')

if [ -z "$URL" ]; then
  echo "[error] Nessun risultato Unsplash per '${QUERY}'." >&2
  exit 3
fi

echo "[info] Trovato: foto di $PHOTOG (@$PHOTOG_USERNAME)"
echo "[info] URL sorgente: $URL"

# Notifica Unsplash del download (richiesto dalle linee guida API)
if [ -n "$DOWNLOAD_TRACK" ]; then
  curl -sS -A "$UA" -H "Authorization: Client-ID $UNSPLASH_ACCESS_KEY" \
    "$DOWNLOAD_TRACK" >/dev/null || true
fi

TMP="/tmp/unsplash-${NAME}.jpg"
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
echo "  Foto di ${PHOTOG} su Unsplash (licenza Unsplash)."
echo ""
echo "Nel frontmatter:"
echo "  image_credit: \"Foto di ${PHOTOG} — Unsplash License — unsplash.com/@${PHOTOG_USERNAME}\""
echo "  image_source_url: \"${PHOTO_URL}\""
echo "================================================================"
