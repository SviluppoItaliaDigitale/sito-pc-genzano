#!/usr/bin/env bash
# Rende Bootstrap Italia leggibile dai browser vecchi delle lavagne interattive (LIM) e dei PC di scuola:
# trascrive il bundle con esbuild (target Chrome 64) e aggiunge globalThis, che Chrome < 71 non ha.
#
# Perché: Bootstrap Italia 2.x usa optional chaining e campi statici di classe (Chrome 80+). Su un
# browser più vecchio il bundle non si avvia e nel sito non funzionano menu, finestre, caroselli,
# accordion. Verificato l'01/11/2026 con Chromium 69 (lavagne Android 9): menu che non si aprono.
#
# Uso: bash scripts/js-compatibile-lim.sh            (salta se il file è già trascritto)
#      bash scripts/js-compatibile-lim.sh --check    (esce 1 se il file non è trascritto)
# Lo esegue update-bootstrap-italia.yml dopo ogni aggiornamento; validate-pr.yml ne controlla l'esito
# con scripts/check-sintassi-js.cjs.
set -euo pipefail
cd "$(dirname "$0")/.."
F=static/vendor/bootstrap-italia/js/bootstrap-italia.bundle.min.js
ESBUILD=esbuild@0.24.0
SEGNO='/* compatibile-lim: esbuild 0.24.0, target chrome64 */'

if head -c 200 "$F" | grep -q 'compatibile-lim'; then
  echo "✓ $F è già la versione compatibile con i browser delle LIM."
  exit 0
fi
if [ "${1:-}" = "--check" ]; then
  echo "::error::$F non è trascritto: esegui bash scripts/js-compatibile-lim.sh e committa." >&2
  exit 1
fi
TMP=$(mktemp)
npx -y "$ESBUILD" "$F" --target=chrome64 --minify --legal-comments=none --log-level=warning \
  --banner:js="$SEGNO"'typeof globalThis>"u"&&(self.globalThis=self);' --outfile="$TMP"
mv "$TMP" "$F"
echo "✓ $F trascritto per i browser delle LIM ($(wc -c < "$F") byte)."
