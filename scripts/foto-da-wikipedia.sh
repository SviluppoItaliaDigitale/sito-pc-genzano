#!/usr/bin/env bash
# Scarica l'immagine principale di una pagina Wikipedia, verifica la
# licenza (deve essere libera: CC0, PD, CC-BY, CC-BY-SA) e applica la
# fascia istituzionale del sito chiamando applica-fascia-foto.sh.
#
# DA ESEGUIRE SULLA MACCHINA LOCALE (richiede rete + ImageMagick + jq + curl).
#
# Uso:
#   bash scripts/foto-da-wikipedia.sh "Titolo Pagina" <nome-output> [lang=it]
#
# Esempi:
#   bash scripts/foto-da-wikipedia.sh "Alluvione di Sarno e Quindici del 1998" \
#        2026-05-05-sarno-frana-1998
#   bash scripts/foto-da-wikipedia.sh "1976 Friuli earthquake" \
#        2026-05-06-friuli-1976-terremoto en
#
# Output: static/images/<nome-output>.webp (1200px, fascia blu, max 200 KB)
#         + stampa licenza, autore, URL sorgente per documentazione interna.

set -euo pipefail

TITLE="${1:?specifica il titolo della pagina Wikipedia tra virgolette}"
NAME="${2:?specifica il nome di output (senza estensione)}"
LANG="${3:-it}"

# Encode del titolo per URL (spazi → %20, ecc.)
TITLE_ENC=$(python3 -c "import urllib.parse, sys; print(urllib.parse.quote(sys.argv[1]))" "$TITLE")

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APPLY_BAND="$ROOT/scripts/applica-fascia-foto.sh"

# Verifica dipendenze
for cmd in curl jq python3 magick; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[error] manca il comando richiesto: $cmd" >&2
    if [ "$cmd" = "magick" ]; then
      echo "        (ImageMagick 7. Su Ubuntu/Debian: 'apt install imagemagick')" >&2
    fi
    exit 1
  fi
done

UA="PCGenzanoBot/1.0 (https://www.protezionecivilegenzano.it; segreteria@protezionecivilegenzano.it)"
API="https://${LANG}.wikipedia.org/w/api.php"

echo "[info] Cerco l'immagine principale di: ${TITLE} (${LANG}.wikipedia.org)"

# 1) Recupera il "pageimage" (immagine principale, alta risoluzione)
PAGE_JSON=$(curl -sS -A "$UA" --get \
  --data-urlencode "action=query" \
  --data-urlencode "titles=${TITLE}" \
  --data-urlencode "prop=pageimages|pageprops" \
  --data-urlencode "format=json" \
  --data-urlencode "pithumbsize=1600" \
  --data-urlencode "pilicense=any" \
  "$API")

THUMB_URL=$(echo "$PAGE_JSON" | jq -r '.query.pages[].thumbnail.source // empty')
PAGE_IMG_NAME=$(echo "$PAGE_JSON" | jq -r '.query.pages[].pageimage // empty')

if [ -z "$THUMB_URL" ] || [ -z "$PAGE_IMG_NAME" ]; then
  echo "[error] Nessuna immagine principale trovata per '${TITLE}'." >&2
  echo "        Prova con un titolo diverso o lingua diversa (es: en)." >&2
  exit 2
fi

# Filtro automatico: scarta bandiere comunali e stemmi (SVG decorativi non
# pertinenti). Pattern tipici Wikipedia: "<Comune>-Bandiera.svg",
# "Flag_of_<Comune>.svg", "<Comune>-Stemma.svg".
case "$PAGE_IMG_NAME" in
  *Bandiera.svg|Flag_of_*|*-Stemma.svg|*Coat_of_arms*|*Stemma_di_*)
    echo "[error] Immagine principale è una bandiera/stemma comunale: '${PAGE_IMG_NAME}'." >&2
    echo "        Scartata automaticamente (non aggiunge valore narrativo all'articolo)." >&2
    echo "        Prova con un titolo più specifico (un monumento, una piazza, una vista)." >&2
    exit 4
    ;;
esac

# 2) Ottieni metadata di licenza/autore via imageinfo
META_JSON=$(curl -sS -A "$UA" --get \
  --data-urlencode "action=query" \
  --data-urlencode "titles=File:${PAGE_IMG_NAME}" \
  --data-urlencode "prop=imageinfo" \
  --data-urlencode "iiprop=extmetadata|url|user" \
  --data-urlencode "format=json" \
  "$API")

LICENSE=$(echo "$META_JSON" | jq -r '.query.pages[].imageinfo[0].extmetadata.LicenseShortName.value // empty')
ARTIST=$(echo "$META_JSON" | jq -r '.query.pages[].imageinfo[0].extmetadata.Artist.value // empty' \
          | sed -E 's|<[^>]+>||g' | tr -s ' ' | head -c 200)
DESCURL=$(echo "$META_JSON" | jq -r '.query.pages[].imageinfo[0].descriptionurl // empty')

# 3) Verifica licenza compatibile
LIC_OK=0
case "$LICENSE" in
  ""|"unknown") LIC_OK=0 ;;
  *Public*domain*|*PD*|*CC0*|*"CC BY"*|*"CC BY-SA"*|*"CC-BY"*|*"CC-BY-SA"*|*Attribution*|*ShareAlike*) LIC_OK=1 ;;
  *) LIC_OK=0 ;;
esac

if [ "$LIC_OK" -ne 1 ]; then
  echo "[warn] Licenza non chiaramente compatibile: '${LICENSE:-sconosciuta}'." >&2
  echo "        Verifica manualmente la pagina dell'immagine: ${DESCURL}" >&2
  echo "        Per procedere comunque, esegui con FORCE=1." >&2
  if [ "${FORCE:-0}" != "1" ]; then
    exit 3
  fi
fi

# 4) Scarica l'immagine in un file temporaneo
TMP_IMG="$(mktemp --suffix=.bin)"
trap 'rm -f "$TMP_IMG"' EXIT

echo "[info] Scarico ${THUMB_URL}"
curl -sS -A "$UA" -L -o "$TMP_IMG" "$THUMB_URL"

# 5) Applica la fascia blu
bash "$APPLY_BAND" "$TMP_IMG" "$NAME"

# 6) Riepilogo per documentazione interna
echo ""
echo "─── Foto applicata correttamente ───"
echo "  File:    static/images/${NAME}.webp"
echo "  Origine: ${DESCURL}"
echo "  Autore:  ${ARTIST:-(non specificato)}"
echo "  Licenza: ${LICENSE:-(non specificata)}"
echo ""
echo "Importante: cita SEMPRE la fonte e l'autore nella didascalia"
echo "dell'articolo (regola WCAG/AGID + crediti immagine)."
