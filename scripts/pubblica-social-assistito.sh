#!/bin/bash
# pubblica-social-assistito.sh
# ────────────────────────────────────────────────────────────────
# Human-in-the-loop per la pubblicazione delle bozze social.
#
# Apre 4 tab Chrome (X, Facebook, Instagram, Telegram) sui canali
# del Gruppo + porta in sequenza il testo di ciascuna bozza negli
# appunti di sistema. L'utente fa solo Ctrl+V e click "Pubblica".
#
# Niente pubblicazione automatica: scelta esplicita per rispettare
# la social-media-policy del Gruppo (ISO 22329 + CWA CEN/CENELEC +
# AGID) che richiede supervisione umana sui post istituzionali di
# Protezione Civile.
#
# Uso:
#   bash scripts/pubblica-social-assistito.sh <slug>
#   bash scripts/pubblica-social-assistito.sh social-bozze/AAAA/MM/<slug>/
#
# Dipendenze: google-chrome, xdg-open, xclip (o wl-copy/xsel/pbcopy).
# ────────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BOZZE_DIR="$REPO_ROOT/social-bozze"

# URL canali del Gruppo (da data/social_links.yaml)
URL_X_COMPOSE="https://x.com/compose/post"
URL_FB_PAGE="https://www.facebook.com/protezionecivilegenzanodiroma"
URL_IG_PAGE="https://www.instagram.com/protezionecivilegenzano/"
URL_TG_CANALE="https://web.telegram.org/k/#@pcalfagenzano"

# ──────────────────────────────────────────────────────────────
# Helper clipboard cross-platform
# ──────────────────────────────────────────────────────────────
copy_to_clipboard() {
  local text="$1"
  if command -v xclip >/dev/null 2>&1; then
    printf '%s' "$text" | xclip -selection clipboard
    return 0
  elif command -v wl-copy >/dev/null 2>&1; then
    printf '%s' "$text" | wl-copy
    return 0
  elif command -v xsel >/dev/null 2>&1; then
    printf '%s' "$text" | xsel --clipboard --input
    return 0
  elif command -v pbcopy >/dev/null 2>&1; then
    printf '%s' "$text" | pbcopy
    return 0
  fi
  return 1
}

# ──────────────────────────────────────────────────────────────
# Ricerca cartella bozze a partire da slug o path
# ──────────────────────────────────────────────────────────────
find_bozze_dir() {
  local arg="$1"
  # Path assoluto?
  if [ -d "$arg" ]; then
    realpath "$arg"; return 0
  fi
  # Path relativo dalla root?
  if [ -d "$REPO_ROOT/$arg" ]; then
    realpath "$REPO_ROOT/$arg"; return 0
  fi
  # Slug con prefisso data AAAA-MM-GG-...
  if [[ "$arg" =~ ^([0-9]{4})-([0-9]{2})-[0-9]{2} ]]; then
    local anno="${BASH_REMATCH[1]}"
    local mese="${BASH_REMATCH[2]}"
    local candidate="$BOZZE_DIR/$anno/$mese/$arg"
    if [ -d "$candidate" ]; then
      realpath "$candidate"; return 0
    fi
  fi
  # Ricerca fuzzy
  local match
  match=$(find "$BOZZE_DIR" -maxdepth 4 -type d -name "*$arg*" 2>/dev/null | head -1)
  if [ -n "$match" ]; then
    realpath "$match"; return 0
  fi
  return 1
}

# ──────────────────────────────────────────────────────────────
# Argomenti
# ──────────────────────────────────────────────────────────────
if [ $# -lt 1 ]; then
  echo "Uso: $0 <slug-articolo>"
  echo
  echo "Esempi:"
  echo "  $0 2026-05-18-attivita-formazione"
  echo "  $0 social-bozze/2026/05/2026-05-18-attivita-formazione"
  echo
  echo "Ultime bozze disponibili:"
  find "$BOZZE_DIR" -maxdepth 3 -mindepth 3 -type d 2>/dev/null \
    | sort -r | head -8 | sed 's|.*/||; s|^|  - |'
  exit 1
fi

DIR=$(find_bozze_dir "$1") || {
  echo "[errore] Cartella bozze non trovata per: $1"
  echo "         Cerco in: $BOZZE_DIR"
  exit 2
}

SLUG=$(basename "$DIR")

# ──────────────────────────────────────────────────────────────
# Verifica file presenti
# ──────────────────────────────────────────────────────────────
echo
echo "→ Bozze trovate: $DIR"
echo "→ Slug:          $SLUG"
echo
echo "→ File presenti:"
for f in x.txt facebook.txt instagram.txt telegram.txt; do
  if [ -f "$DIR/$f" ]; then
    local_size=$(wc -c < "$DIR/$f" 2>/dev/null || echo 0)
    echo "   ✓ $f (${local_size} byte)"
  else
    echo "   ✗ $f mancante"
  fi
done
echo "→ Immagini Instagram:"
find "$DIR" -maxdepth 1 -name 'instagram-*.jpg' -printf '   ✓ %f\n' 2>/dev/null \
  | sort || true

# ──────────────────────────────────────────────────────────────
# Conferma
# ──────────────────────────────────────────────────────────────
echo
read -rp "Apro i 4 tab social e il file manager? [y/N] " ok
[[ "$ok" =~ ^[yYsS]$ ]] || { echo "Annullato."; exit 0; }

# ──────────────────────────────────────────────────────────────
# Apertura tab + file manager
# ──────────────────────────────────────────────────────────────
echo
echo "→ Apertura tab Chrome sui 4 social..."
google-chrome --new-window "$URL_X_COMPOSE" >/dev/null 2>&1 & disown
sleep 1
google-chrome "$URL_FB_PAGE" >/dev/null 2>&1 & disown
sleep 0.5
google-chrome "$URL_IG_PAGE" >/dev/null 2>&1 & disown
sleep 0.5
google-chrome "$URL_TG_CANALE" >/dev/null 2>&1 & disown
sleep 1

echo "→ Apertura cartella immagini Instagram nel file manager..."
xdg-open "$DIR" >/dev/null 2>&1 & disown
sleep 1

# ──────────────────────────────────────────────────────────────
# Sequenza guidata di pubblicazione
# ──────────────────────────────────────────────────────────────
echo
echo "════════════════════════════════════════════════════════════════"
echo "  HUMAN-IN-THE-LOOP — 4 tab pronte, ti guido step by step"
echo "════════════════════════════════════════════════════════════════"

publish_step() {
  local n="$1" platform="$2" file="$3" instructions="$4"
  echo
  echo "──── [$n/4] $platform ──────────────────────────────────────────"
  if [ -f "$file" ]; then
    if copy_to_clipboard "$(cat "$file")"; then
      echo "  ✓ Testo $platform copiato negli APPUNTI."
    else
      echo "  ⚠ Niente tool clipboard. Apri il file e copia a mano:"
      echo "     $file"
    fi
  else
    echo "  ⚠ File $file mancante — salta o copia manualmente."
  fi
  echo
  echo "$instructions"
  echo
  read -rp "  [INVIO] quando hai pubblicato (o saltato) $platform... " _
}

publish_step 1 "X (Twitter)" "$DIR/x.txt" "  → Tab X compose già aperto.
  → Click nel campo testo → Ctrl+V → click 'Posta'.
  → Se serve immagine cover: drag dal file manager."

publish_step 2 "Facebook" "$DIR/facebook.txt" "  → Tab Facebook → pagina del Gruppo.
  → Click 'Crea post' → Ctrl+V nel campo testo.
  → Aggiungi foto/cover trascinando dal file manager.
  → Click 'Pubblica'."

publish_step 3 "Instagram" "$DIR/instagram.txt" "  → Tab Instagram → click '+' in alto (Crea).
  → DRAG delle immagini DAL FILE MANAGER:
     - SINGOLA: instagram-post.jpg
     - CAROSELLO: instagram-post-1.jpg … instagram-post-N.jpg
  → Per la STORY: post separato dopo, drag instagram-story.jpg.
  → Caption: Ctrl+V (già negli appunti).
  → Click 'Condividi'."

publish_step 4 "Telegram" "$DIR/telegram.txt" "  → Tab Telegram → canale del Gruppo (web.telegram.org).
  → Click sul campo 'Scrivi un messaggio' → Ctrl+V → INVIO.
  → Per immagini: drag dal file manager nel campo."

# ──────────────────────────────────────────────────────────────
# Fine
# ──────────────────────────────────────────────────────────────
echo
echo "════════════════════════════════════════════════════════════════"
echo "  Workflow completato. Verifica che i 4 post siano live e che"
echo "  l'articolo originale sia stato pubblicato sul sito."
echo "════════════════════════════════════════════════════════════════"
