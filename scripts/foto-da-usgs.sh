#!/usr/bin/env bash
# Scarica una mappa di intensita (ShakeMap) da USGS Earthquake Hazards
# Program per un evento sismico specifico. Le ShakeMap USGS sono pubblicate
# nel pubblico dominio (lavoro del governo federale USA).
#
# Uso:
#   bash scripts/foto-da-usgs.sh shakemap <eventid> <nome-output>
#
# Per trovare eventid: cerca il terremoto su
#   https://earthquake.usgs.gov/earthquakes/search/
# ID compare nell URL della pagina evento, es:
#   .../eventpage/usp000hf28/executive  ->  eventid = usp000hf28
#
# Esempi:
#   bash scripts/foto-da-usgs.sh shakemap usp000hf28 2026-04-06-l-aquila-shakemap
#     (Terremoto L Aquila 6 aprile 2009)
#   bash scripts/foto-da-usgs.sh shakemap us20007z80 2026-08-24-amatrice-shakemap
#     (Terremoto Centro Italia Amatrice 24 agosto 2016)
#
# Output: static/images/<nome>.webp (1200px, fascia blu, max 200 KB)

set -euo pipefail

MODE="${1:?usa 'shakemap' come primo argomento}"
EVENTID="${2:?specifica eventid USGS (es. usp000hf28)}"
NAME="${3:?specifica il nome di output (senza estensione)}"

if [ "$MODE" != "shakemap" ]; then
  echo "[error] modalita non supportata: $MODE (solo 'shakemap')" >&2
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APPLY_BAND="$ROOT/scripts/applica-fascia-foto.sh"

for cmd in curl jq; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "[error] manca: $cmd" >&2; exit 1; }
done

UA="PCGenzanoBot/1.0 (https://www.protezionecivilegenzano.it; segreteria@protezionecivilegenzano.it)"

echo "[info] Cerco ShakeMap USGS per evento ${EVENTID}"

EVENT_JSON=$(curl -sS -A "$UA" \
  "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&eventid=${EVENTID}")

# Verifica che il geojson abbia properties
TITLE=$(echo "$EVENT_JSON" | jq -r '.properties.title // empty')
if [ -z "$TITLE" ]; then
  echo "[error] Evento ${EVENTID} non trovato su USGS." >&2
  echo "        Verifica eventid su https://earthquake.usgs.gov/earthquakes/search/" >&2
  exit 2
fi
echo "[info] Evento: ${TITLE}"

# Cerca la ShakeMap intensity image (graceful: se non c'e' shakemap, esce pulito)
SHAKEMAP_URL=$(echo "$EVENT_JSON" | jq -r '
  if (.properties.products.shakemap // empty) | length > 0 then
    .properties.products.shakemap[0].contents
    | with_entries(select(.key | test("intensity\\.jpg$|intensity_overlay\\.jpg$|tvmap\\.jpg$")))
    | to_entries
    | (if length > 0 then .[0].value.url else empty end)
  else empty end')

# Fallback: prova chiave standard "download/intensity.jpg"
if [ -z "$SHAKEMAP_URL" ]; then
  SHAKEMAP_URL=$(echo "$EVENT_JSON" | jq -r '
    .properties.products.shakemap[0].contents["download/intensity.jpg"].url // empty' 2>/dev/null || true)
fi

if [ -z "$SHAKEMAP_URL" ]; then
  echo "[error] Nessuna ShakeMap disponibile per ${EVENTID}." >&2
  echo "        Eventi minori potrebbero non avere ShakeMap. Prova con un altro evento." >&2
  exit 3
fi

TMP_IMG="$(mktemp --suffix=.jpg)"
trap 'rm -f "$TMP_IMG"' EXIT

echo "[info] Scarico ${SHAKEMAP_URL}"
curl -sS -A "$UA" -L -o "$TMP_IMG" "$SHAKEMAP_URL"

bash "$APPLY_BAND" "$TMP_IMG" "$NAME"

EVENT_PAGE="https://earthquake.usgs.gov/earthquakes/eventpage/${EVENTID}/shakemap"
echo ""
echo "─── ShakeMap USGS applicata correttamente ───"
echo "  File:     static/images/${NAME}.webp"
echo "  Origine:  ${EVENT_PAGE}"
echo "  Autore:   USGS Earthquake Hazards Program"
echo "  Licenza:  Public domain (US Geological Survey)"
echo "  Evento:   ${TITLE}"
echo ""
echo "Importante: cita SEMPRE 'USGS' nella didascalia. Le ShakeMap rappresentano"
echo "l'intensita osservata/stimata in scala MMI (Mercalli Modificata)."
