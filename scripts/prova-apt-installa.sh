#!/usr/bin/env bash
# Prove di scripts/apt-installa.sh senza rete e senza toccare il sistema: sudo, apt-get, dpkg e dpkg-query
# sono sostituiti da finti comandi in una cartella temporanea. Gira su ogni pull request (validate-pr.yml).
#
# Nasce dalla revisione dell'11/11/2026: con 240 secondi, un primo `apt-get update` appeso sui server
# predefiniti consumava tutto il tempo e a mirror alternativi e cache restava 1 secondo.
set -uo pipefail

QUI="$(cd "$(dirname "$0")" && pwd)"
ESITI=0
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

prepara() {
  # $1: "appeso" (i server predefiniti non rispondono mai) o "ok" (rispondono)
  rm -rf "$TMP/bin" "$TMP/stato" "$TMP/cache" "$TMP/out"
  mkdir -p "$TMP/bin" "$TMP/stato" "$TMP/cache"
  : > "$TMP/out"
  [ "$1" = "ok" ] && touch "$TMP/stato/predefiniti-ok"
  cat > "$TMP/bin/sudo" <<'EOF'
#!/usr/bin/env bash
case "$1" in
  tee) cat > /dev/null; touch "$STATO/mirror"; exit 0 ;;   # sorgenti cambiate: da qui rispondono i mirror
  mv|cp|rm|chown) exit 0 ;;
  *) exec "$@" ;;
esac
EOF
  cat > "$TMP/bin/apt-get" <<'EOF'
#!/usr/bin/env bash
cmd=""
for a in "$@"; do case "$a" in update|install|autoclean) cmd="$a" ;; esac; done
risponde() { [ -f "$STATO/predefiniti-ok" ] || [ -f "$STATO/mirror" ]; }
case "$cmd" in
  update) if risponde; then sleep 2; exit 0; fi; echo "0% [Connecting to archive.ubuntu.com]"; sleep 1000 ;;
  install) if risponde; then sleep 2; touch "$STATO/installato"; exit 0; fi; exit 100 ;;
  *) exit 0 ;;
esac
EOF
  printf '#!/usr/bin/env bash\nexit 0\n' > "$TMP/bin/dpkg"
  printf '#!/usr/bin/env bash\n[ -f "$STATO/installato" ] && printf "install ok installed"\nexit 0\n' > "$TMP/bin/dpkg-query"
  chmod +x "$TMP/bin/"*
}

prova() {
  # $1 nome, $2 situazione, $3 fonte attesa, $4 codice atteso, $5 secondi massimi
  prepara "$2"
  local inizio=$SECONDS rc
  PATH="$TMP/bin:$PATH" STATO="$TMP/stato" APT_DEB_CACHE="$TMP/cache" GITHUB_OUTPUT="$TMP/out" \
    APT_TEMPO_MASSIMO=20 bash "$QUI/apt-installa.sh" pacchetto-finto >/dev/null 2>&1
  rc=$?
  local durata=$(( SECONDS - inizio )) fonte
  fonte="$(sed -n 's/^fonte=//p' "$TMP/out" | tail -n 1)"
  if [ "$fonte" = "$3" ] && [ "$rc" -eq "$4" ] && [ "$durata" -le "$5" ]; then
    echo "✓ $1 (fonte=$fonte, uscita $rc, $durata s)"
  else
    echo "✗ $1: atteso fonte=$3 uscita $4 entro $5 s, ottenuto fonte=$fonte uscita $rc in $durata s"
    ESITI=1
  fi
}

prova "server predefiniti che rispondono" ok server-predefiniti 0 10
prova "server predefiniti appesi: i mirror hanno ancora il loro tempo" appeso mirror-alternativo 0 20

exit "$ESITI"
