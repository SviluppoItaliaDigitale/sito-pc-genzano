#!/bin/bash
# pubblica-social-livello-b.sh
# ────────────────────────────────────────────────────────────────
# 🟡 SCRIPT IN STANDBY — NON ATTIVO
#
# Variante Livello B della pubblicazione social-assistita:
# usa opencli browser primitives (fill, upload) per COMPILARE
# automaticamente i campi testo e caricare le immagini sui 4 social,
# fermandosi PRIMA del click "Pubblica" (sempre umano).
#
# Più automazione del Livello A, ma fragile: i selettori CSS dei
# campi di compose su X/Facebook/Instagram cambiano ogni 3-6 mesi
# e quando cambiano lo script smette di funzionare finché qualcuno
# non aggiorna gli scopo.
#
# Attivazione: rimuovere il blocco "STANDBY GUARD" in fondo a questo
# header e completare i selettori CSS verificati al momento.
#
# Vincolo permanente: in fondo c'è SEMPRE un controllo umano (non
# clicca mai "Pubblica" in autonomia, in ogni revisione futura).
# ────────────────────────────────────────────────────────────────

set -euo pipefail

# ──────────────────────────────────────────────────────────────
# STANDBY GUARD — rimuovere le 4 righe sotto per attivare
# ──────────────────────────────────────────────────────────────
echo "[STANDBY] Lo script Livello B è preparato ma NON attivo." >&2
echo "          Vedi header del file per le istruzioni di attivazione." >&2
echo "          Per ora usa il Livello A: scripts/pubblica-social-assistito.sh" >&2
exit 0

# ──────────────────────────────────────────────────────────────
# SOTTO QUESTO PUNTO IL CODICE È PREPARATO MA INERTE.
# Verifica selettori CSS al momento dell'attivazione (browser DevTools
# su x.com/compose/post, facebook.com pagina, instagram.com).
# ──────────────────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BOZZE_DIR="$REPO_ROOT/social-bozze"

# Selettori CSS — verificare prima di attivare (data ultima verifica: __NEVER__)
SEL_X_TEXTAREA='div[data-testid="tweetTextarea_0"]'
SEL_X_IMG_INPUT='input[data-testid="fileInput"]'
SEL_FB_CREATE_POST_TRIGGER='[aria-label="Crea post"]'
SEL_FB_TEXTAREA='div[role="textbox"][contenteditable="true"]'
SEL_IG_CREATE_TRIGGER='svg[aria-label="Nuovo post"]'
SEL_IG_TEXTAREA='div[role="textbox"][aria-label="Scrivi una didascalia..."]'
SEL_TG_MESSAGE_INPUT='div[contenteditable="true"].input-message-input'

URL_X_COMPOSE="https://x.com/compose/post"
URL_FB_PAGE="https://www.facebook.com/protezionecivilegenzanodiroma"
URL_IG_PAGE="https://www.instagram.com/protezionecivilegenzano/"
URL_TG_CANALE="https://web.telegram.org/k/#@pcalfagenzano"

# Verifica opencli + estensione attivi
require_opencli() {
  if ! command -v opencli >/dev/null 2>&1; then
    echo "[errore] opencli non installato. npm install -g @jackwener/opencli"
    exit 3
  fi
  if ! opencli doctor 2>&1 | grep -q "Connectivity: connected"; then
    echo "[errore] opencli daemon/estensione non connessi. Lancia:"
    echo "  opencli doctor"
    exit 4
  fi
}

# Trova cartella bozze (stessa logica del Livello A)
find_bozze_dir() {
  local arg="$1"
  if [ -d "$arg" ]; then realpath "$arg"; return 0; fi
  if [ -d "$REPO_ROOT/$arg" ]; then realpath "$REPO_ROOT/$arg"; return 0; fi
  if [[ "$arg" =~ ^([0-9]{4})-([0-9]{2})-[0-9]{2} ]]; then
    local anno="${BASH_REMATCH[1]}" mese="${BASH_REMATCH[2]}"
    local c="$BOZZE_DIR/$anno/$mese/$arg"
    [ -d "$c" ] && { realpath "$c"; return 0; }
  fi
  local m
  m=$(find "$BOZZE_DIR" -maxdepth 4 -type d -name "*$arg*" 2>/dev/null | head -1)
  [ -n "$m" ] && { realpath "$m"; return 0; }
  return 1
}

# ──────────────────────────────────────────────────────────────
# Funzioni di compose per piattaforma — fermarsi PRIMA del click pubblica
# ──────────────────────────────────────────────────────────────
compose_x() {
  local text_file="$1"
  echo "→ X: apro compose e riempo il campo..."
  opencli browser open "$URL_X_COMPOSE"
  opencli browser wait --selector "$SEL_X_TEXTAREA" --timeout 10000
  opencli browser fill --selector "$SEL_X_TEXTAREA" --value "$(cat "$text_file")"
  # NON cliccare "Posta". L'utente lo fa manualmente.
  echo "  ✓ X compilato. Vai sul tab X e click 'Posta' quando pronto."
}

compose_facebook() {
  local text_file="$1"
  echo "→ Facebook: apro pagina e creo post..."
  opencli browser open "$URL_FB_PAGE"
  opencli browser click --selector "$SEL_FB_CREATE_POST_TRIGGER"
  opencli browser wait --selector "$SEL_FB_TEXTAREA" --timeout 10000
  opencli browser type --selector "$SEL_FB_TEXTAREA" --value "$(cat "$text_file")"
  echo "  ✓ Facebook compilato. Click 'Pubblica' manualmente."
}

compose_instagram() {
  local text_file="$1"
  local img_dir="$2"
  echo "→ Instagram: apro pagina e avvio nuovo post..."
  opencli browser open "$URL_IG_PAGE"
  opencli browser click --selector "$SEL_IG_CREATE_TRIGGER"
  # Upload immagini IG (carosello)
  for img in "$img_dir"/instagram-post-*.jpg "$img_dir"/instagram-post.jpg; do
    [ -f "$img" ] && opencli browser upload --file "$img"
  done
  opencli browser wait --selector "$SEL_IG_TEXTAREA" --timeout 15000
  opencli browser type --selector "$SEL_IG_TEXTAREA" --value "$(cat "$text_file")"
  echo "  ✓ IG compilato. Click 'Condividi' manualmente."
}

compose_telegram() {
  local text_file="$1"
  echo "→ Telegram: apro canale e riempo il messaggio..."
  opencli browser open "$URL_TG_CANALE"
  opencli browser wait --selector "$SEL_TG_MESSAGE_INPUT" --timeout 10000
  opencli browser fill --selector "$SEL_TG_MESSAGE_INPUT" --value "$(cat "$text_file")"
  echo "  ✓ Telegram compilato. INVIO per pubblicare manualmente."
}

# ──────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────
if [ $# -lt 1 ]; then
  echo "Uso: $0 <slug-articolo>"
  exit 1
fi

require_opencli

DIR=$(find_bozze_dir "$1") || { echo "[errore] bozze non trovate"; exit 2; }
echo "→ Bozze: $DIR"

[ -f "$DIR/x.txt" ]        && compose_x        "$DIR/x.txt"
[ -f "$DIR/facebook.txt" ] && compose_facebook "$DIR/facebook.txt"
[ -f "$DIR/instagram.txt" ] && compose_instagram "$DIR/instagram.txt" "$DIR"
[ -f "$DIR/telegram.txt" ] && compose_telegram "$DIR/telegram.txt"

echo
echo "Tutte e 4 le bozze sono compilate. Vai tab per tab e clicca 'Pubblica'."
