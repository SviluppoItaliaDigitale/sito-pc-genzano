#!/usr/bin/env bash
# Scarica i pittogrammi ISO 7010 da Wikimedia Commons (PD-self / CC0).
# DA ESEGUIRE SULLA MACCHINA LOCALE: la sandbox di Claude Code blocca i domini
# esterni. Non serve sulla macchina di sviluppo che ha rete libera.
#
# I file finiscono in static/pittogrammi/iso7010/ con nome
# "<CODICE>-<descrizione-breve>.svg".
#
# Uso:
#   bash scripts/scarica-pittogrammi-iso7010.sh
#
# Per aggiungere altri pittogrammi: copia una riga della tabella sotto e
# cambia codice/nome/url. La fonte ufficiale è la pagina Wikimedia Commons
# "Category:ISO 7010 safety signs" (e sotto-categorie):
#   https://commons.wikimedia.org/wiki/Category:ISO_7010_safety_signs

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/static/pittogrammi/iso7010"
mkdir -p "$OUT"

UA="PCGenzanoBot/1.0 (https://www.protezionecivilegenzano.it; segreteria@protezionecivilegenzano.it)"

if ! command -v curl >/dev/null 2>&1; then
  echo "[error] manca curl" >&2; exit 1
fi

# Tabella: <codice>|<nome-file-output>|<url Wikimedia (versione SVG)>
# I codici sono quelli della norma ISO 7010 (standard internazionale).
# Le URL puntano alla versione SVG canonica su upload.wikimedia.org.
read -r -d '' TABELLA <<'EOF' || true
W001|W001-pericolo-generale|https://upload.wikimedia.org/wikipedia/commons/c/c6/ISO_7010_W001.svg
W002|W002-esplosivo|https://upload.wikimedia.org/wikipedia/commons/0/01/ISO_7010_W002.svg
W003|W003-radioattivo|https://upload.wikimedia.org/wikipedia/commons/0/0d/ISO_7010_W003.svg
W004|W004-laser|https://upload.wikimedia.org/wikipedia/commons/d/d6/ISO_7010_W004.svg
W009|W009-rischio-biologico|https://upload.wikimedia.org/wikipedia/commons/8/87/ISO_7010_W009.svg
W012|W012-tensione-elettrica|https://upload.wikimedia.org/wikipedia/commons/4/4a/ISO_7010_W012.svg
W016|W016-tossico|https://upload.wikimedia.org/wikipedia/commons/3/3a/ISO_7010_W016.svg
W021|W021-fiamma-infiammabile|https://upload.wikimedia.org/wikipedia/commons/9/95/ISO_7010_W021.svg
W026|W026-batteria|https://upload.wikimedia.org/wikipedia/commons/6/65/ISO_7010_W026.svg
W037|W037-rumore-forte|https://upload.wikimedia.org/wikipedia/commons/4/40/ISO_7010_W038.svg
W038|W038-frana|https://upload.wikimedia.org/wikipedia/commons/8/8e/ISO_7010_W038.svg
M001|M001-obbligo-generale|https://upload.wikimedia.org/wikipedia/commons/d/d2/ISO_7010_M001.svg
M002|M002-leggi-istruzioni|https://upload.wikimedia.org/wikipedia/commons/8/8a/ISO_7010_M002.svg
P001|P001-divieto-generale|https://upload.wikimedia.org/wikipedia/commons/5/56/ISO_7010_P001.svg
P002|P002-divieto-fumare|https://upload.wikimedia.org/wikipedia/commons/3/3d/ISO_7010_P002.svg
E001|E001-uscita-emergenza-sx|https://upload.wikimedia.org/wikipedia/commons/9/96/ISO_7010_E001.svg
E002|E002-uscita-emergenza-dx|https://upload.wikimedia.org/wikipedia/commons/c/c0/ISO_7010_E002.svg
E003|E003-pronto-soccorso|https://upload.wikimedia.org/wikipedia/commons/3/3e/ISO_7010_E003.svg
E004|E004-telefono-emergenza|https://upload.wikimedia.org/wikipedia/commons/c/c8/ISO_7010_E004.svg
E007|E007-punto-raccolta|https://upload.wikimedia.org/wikipedia/commons/0/02/ISO_7010_E007.svg
E009|E009-medico|https://upload.wikimedia.org/wikipedia/commons/9/9a/ISO_7010_E009.svg
E011|E011-acqua-potabile|https://upload.wikimedia.org/wikipedia/commons/4/40/ISO_7010_E011.svg
F001|F001-estintore|https://upload.wikimedia.org/wikipedia/commons/3/3a/ISO_7010_F001.svg
F002|F002-idrante|https://upload.wikimedia.org/wikipedia/commons/4/45/ISO_7010_F002.svg
F004|F004-presidi-antincendio|https://upload.wikimedia.org/wikipedia/commons/9/97/ISO_7010_F004.svg
F005|F005-allarme-incendio|https://upload.wikimedia.org/wikipedia/commons/3/35/ISO_7010_F005.svg
EOF

OK=0; SKIP=0; ERR=0

while IFS='|' read -r CODICE NOME URL; do
  [ -z "$CODICE" ] && continue
  DEST="$OUT/${NOME}.svg"
  # se il file esiste già (es. perché creato a mano), salta a meno che FORCE=1
  if [ -f "$DEST" ] && [ "${FORCE:-0}" != "1" ]; then
    echo "[skip] $NOME (esiste già; FORCE=1 per sovrascrivere)"
    SKIP=$((SKIP + 1))
    continue
  fi
  echo "[get ] $CODICE → $(basename "$DEST")"
  if curl -sS -A "$UA" -L --max-time 30 -o "$DEST" "$URL"; then
    if grep -q "<svg" "$DEST" 2>/dev/null; then
      OK=$((OK + 1))
    else
      echo "[err ] $CODICE: il file scaricato non sembra un SVG" >&2
      rm -f "$DEST"
      ERR=$((ERR + 1))
    fi
  else
    echo "[err ] $CODICE: download fallito" >&2
    ERR=$((ERR + 1))
  fi
done <<< "$TABELLA"

echo ""
echo "─── Riepilogo ───"
echo "  Scaricati: $OK"
echo "  Saltati:   $SKIP (già presenti)"
echo "  Errori:    $ERR"
echo ""
echo "Licenza: tutti i pittogrammi ISO 7010 su Wikimedia Commons sono in"
echo "PD-self / CC0 (i pittogrammi della norma sono di pubblico dominio)."
echo "Se aggiungi nuovi pittogrammi al sito tramite shortcode {{< pittogramma >}}"
echo "non serve attribuzione visibile, ma il riferimento alla norma ISO 7010"
echo "è sempre opportuno."
