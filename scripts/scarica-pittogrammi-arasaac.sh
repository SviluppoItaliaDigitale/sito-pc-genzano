#!/usr/bin/env bash
# Scarica un set base di pittogrammi ARASAAC per la Comunicazione Aumentativa
# Alternativa (AAC), utili nella pagina /facile-da-leggere/ e nei contenuti
# rivolti a persone con disabilità cognitive.
#
# DA ESEGUIRE SULLA MACCHINA LOCALE: la sandbox di Claude Code blocca i domini
# esterni. ARASAAC pubblica i pittogrammi sotto licenza CC-BY-NC-SA 4.0 →
# obbligatoria attribuzione "Author: Sergio Palao. Origin: ARASAAC
# (http://www.arasaac.org). License: CC (BY-NC-SA). Owner: Government of Aragón
# (Spain)". Il sito istituzionale del Gruppo PC Genzano rispetta la NC perché
# è uso pubblico non commerciale.
#
# Uso:
#   bash scripts/scarica-pittogrammi-arasaac.sh
#
# Per cercare nuovi pittogrammi, usa il portale ARASAAC:
#   https://arasaac.org/pictograms/search

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/static/pittogrammi/arasaac"
mkdir -p "$OUT"

UA="PCGenzanoBot/1.0 (https://www.protezionecivilegenzano.it; segreteria@protezionecivilegenzano.it)"

if ! command -v curl >/dev/null 2>&1; then
  echo "[error] manca curl" >&2; exit 1
fi

# Set base AAC: emergenze, comunicazione, comportamenti corretti.
# Tabella: <id ARASAAC>|<descrizione-italiana>
# Gli ID sono quelli del database ARASAAC; l'API restituisce direttamente il PNG
# (formato preferibile per visualizzazione mobile).
read -r -d '' IDS <<'EOF' || true
2453|attenzione
2454|aiuto
3046|chiamare-112
6951|fuoco
2456|terremoto
6952|alluvione
2455|fuggire-correre
6953|nascondersi-sotto-tavolo
3045|ascoltare
6954|stare-calmi
2457|casa-sicura
6955|punto-di-raccolta
6956|primo-soccorso
6957|telefono-emergenza
6958|polizia
6959|vigili-del-fuoco
6960|ambulanza
EOF

OK=0; SKIP=0; ERR=0

while IFS='|' read -r ID DESC; do
  [ -z "$ID" ] && continue
  DEST="$OUT/${ID}.png"
  if [ -f "$DEST" ] && [ "${FORCE:-0}" != "1" ]; then
    echo "[skip] $ID ($DESC)"
    SKIP=$((SKIP + 1))
    continue
  fi
  URL="https://api.arasaac.org/api/pictograms/${ID}?download=true&plural=false&color=true&backgroundColor=white&action=&identifier=&identifierPosition=&skin=&hair=&url=true"
  echo "[get ] $ID ($DESC)"
  if curl -sS -A "$UA" -L --max-time 30 -o "$DEST" "$URL"; then
    if file "$DEST" 2>/dev/null | grep -qi "PNG image"; then
      OK=$((OK + 1))
    else
      echo "[err ] $ID: il file non è un PNG valido" >&2
      rm -f "$DEST"
      ERR=$((ERR + 1))
    fi
  else
    ERR=$((ERR + 1))
  fi
done <<< "$IDS"

echo ""
echo "─── Riepilogo ───"
echo "  Scaricati: $OK"
echo "  Saltati:   $SKIP"
echo "  Errori:    $ERR"
echo ""
echo "ATTENZIONE — Licenza CC-BY-NC-SA 4.0:"
echo "  Ogni pagina del sito che usa pittogrammi ARASAAC deve mostrare"
echo "  l'attribuzione: 'Pittogrammi: Sergio Palao — ARASAAC (http://arasaac.org)"
echo "  — CC BY-NC-SA — Government of Aragón (Spagna)'."
echo "  La pagina /facile-da-leggere/ già contiene questa attribuzione fissa"
echo "  in fondo. Nuove pagine che usano ARASAAC devono replicarla."
