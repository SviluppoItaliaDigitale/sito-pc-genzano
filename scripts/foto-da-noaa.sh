#!/usr/bin/env bash
# Scarica un'immagine NOAA (uragani, ondate calore, satellite, fenomeni meteo
# globali) da un URL diretto. Le immagini NOAA sono Public Domain (lavoro del
# governo federale USA) salvo eccezioni esplicitamente segnalate sulla pagina
# di origine.
#
# A differenza di Wikipedia/NASA, NOAA non espone una API JSON unificata per
# la ricerca immagini. L'utente deve fornire l'URL diretto della foto trovata
# su una delle fonti seguenti:
#
#   - https://www.photolib.noaa.gov/        (NOAA Photo Library)
#   - https://www.weather.gov/               (NWS - immagini avvisi meteo)
#   - https://www.star.nesdis.noaa.gov/      (NESDIS - satellite GOES)
#   - https://oceanservice.noaa.gov/         (Ocean Service - mareografi)
#   - https://www.nhc.noaa.gov/              (National Hurricane Center)
#
# Uso:
#   bash scripts/foto-da-noaa.sh "URL diretto immagine" "Descrizione/contesto" <nome-output>
#
# Esempi:
#   bash scripts/foto-da-noaa.sh \
#     "https://www.nhc.noaa.gov/archive/2005/KATRINA/track.gif" \
#     "Traccia uragano Katrina (NHC NOAA)" \
#     2026-08-29-katrina-traccia
#
#   bash scripts/foto-da-noaa.sh \
#     "https://www.star.nesdis.noaa.gov/GOES/conus/...goesfull_disk.jpg" \
#     "Mosaico satellitare GOES (NOAA NESDIS)" \
#     2026-07-15-goes-mosaico
#
# Output: static/images/<nome>.webp (1200px, fascia blu, max ~200 KB)

set -euo pipefail

URL="${1:?specifica URL diretto immagine NOAA}"
DESC="${2:?specifica una descrizione/contesto della foto}"
NAME="${3:?specifica il nome di output (senza estensione)}"

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APPLY_BAND="$ROOT/scripts/applica-fascia-foto.sh"

for cmd in curl; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "[error] manca: $cmd" >&2; exit 1; }
done

# Verifica che l'URL sia di un dominio NOAA noto (sicurezza minima).
# Domini accettati: *.noaa.gov + weather.gov (NWS, parte di NOAA)
if ! echo "$URL" | grep -qE '^https?://([a-z0-9-]+\.)?(noaa\.gov|weather\.gov)(/|$)'; then
  echo "[warn] URL non riconosciuto come dominio NOAA: $URL" >&2
  echo "        Per procedere comunque, esegui con FORCE=1." >&2
  if [ "${FORCE:-0}" != "1" ]; then
    exit 2
  fi
fi

UA="PCGenzanoBot/1.0 (https://www.protezionecivilegenzano.it; segreteria@protezionecivilegenzano.it)"

# Estrai estensione presunta dal URL (jpg, png, gif, webp)
EXT=$(echo "$URL" | grep -oE '\.(jpg|jpeg|png|gif|webp)([?#]|$)' | head -1 | sed -E 's/^\.([a-z]+).*/\1/')
EXT="${EXT:-jpg}"

TMP_IMG="$(mktemp --suffix=.${EXT})"
trap 'rm -f "$TMP_IMG"' EXIT

echo "[info] Scarico ${URL}"
if ! curl -sSf -A "$UA" -L -o "$TMP_IMG" "$URL"; then
  echo "[error] Download fallito da NOAA per: $URL" >&2
  exit 3
fi

# Verifica che il file scaricato sia un'immagine valida
if ! file "$TMP_IMG" | grep -qE 'image data|JPEG|PNG|GIF|WebP'; then
  echo "[error] Il file scaricato non è un'immagine valida (forse pagina HTML?)" >&2
  echo "        Verifica l'URL diretto dell'immagine, non della pagina che la contiene." >&2
  exit 4
fi

bash "$APPLY_BAND" "$TMP_IMG" "$NAME"

echo ""
echo "─── Foto NOAA applicata correttamente ───"
echo "  File:     static/images/${NAME}.webp"
echo "  Origine:  ${URL}"
echo "  Autore:   NOAA"
echo "  Licenza:  Public domain (NOAA - US Federal)"
echo "  Note:     ${DESC}"
echo ""
echo "Importante: cita SEMPRE 'NOAA' nella didascalia dell'articolo."
echo "Se l'immagine specifica ha attribuzione diversa sulla pagina di origine,"
echo "aggiungi anche quella (es. 'NOAA NHC', 'NOAA NESDIS', 'NWS')."
