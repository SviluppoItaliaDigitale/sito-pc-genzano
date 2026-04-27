#!/usr/bin/env bash
# Scarica le foto di CORPO per l'articolo scout-PC del 23 aprile 2026.
#
# Eseguire UNA VOLTA su macchina con rete libera (laptop, desktop).
# NON gira nella sandbox di Claude Code cloud.
#
# Output: 4 file .webp in static/images/ con fascia blu istituzionale.
#
# Dipendenze: curl, jq, python3, magick (ImageMagick 7).
# Se manca magick: sudo apt install imagemagick
#
# Dopo l'esecuzione:
#   git add static/images/2026-04-23-*.webp
#   git commit -m "Foto corpo articolo scout-PC"
#   git push

set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> Scarico foto di corpo per articolo scout-PC del 23 aprile..."
echo ""

# 1. Alluvione Firenze 1966 — pagina Wikipedia inglese ha buone foto storiche
echo "[1/4] Alluvione Firenze 1966..."
bash scripts/foto-da-wikipedia.sh \
  "1966 flood of the Arno" \
  "2026-04-23-firenze-alluvione-1966-angeli-fango" \
  en || echo "  ⚠️  Fallito — aggiungere manualmente"
echo ""

# 2. Terremoto Friuli 1976 — pagina italiana
echo "[2/4] Terremoto Friuli 1976..."
bash scripts/foto-da-wikipedia.sh \
  "Terremoto del Friuli del 1976" \
  "2026-04-23-friuli-1976-terremoto-gemona" \
  it || echo "  ⚠️  Fallito — aggiungere manualmente"
echo ""

# 3. Robert Baden-Powell — fondatore degli scout
echo "[3/4] Robert Baden-Powell..."
bash scripts/foto-da-wikipedia.sh \
  "Robert Baden-Powell, 1st Baron Baden-Powell" \
  "2026-04-23-baden-powell-fondatore-scout" \
  en || echo "  ⚠️  Fallito — aggiungere manualmente"
echo ""

# 4. Terremoto L'Aquila 2009 — pagina italiana, ShakeMap o foto
echo "[4/4] Terremoto L'Aquila 2009..."
bash scripts/foto-da-wikipedia.sh \
  "Terremoto dell'Aquila del 2009" \
  "2026-04-23-aquila-2009-terremoto" \
  it || echo "  ⚠️  Fallito — aggiungere manualmente"
echo ""

echo "==> Fatto."
echo ""
echo "File generati in static/images/:"
ls -lh static/images/2026-04-23-*.webp 2>/dev/null || echo "  (nessuno — verifica errori sopra)"
echo ""
echo "Per pubblicare:"
echo "  git add static/images/2026-04-23-*.webp"
echo "  git commit -m 'Foto corpo articolo scout-PC'"
echo "  git push"
