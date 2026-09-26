#!/usr/bin/env bash
# Guardia anti-stale: verifica che le pagine live su Aruba servano TUTTE la
# stessa build, e che sia recente. Rileva il "drift di generazioni" — il bug
# per cui su Aruba convivevano pagine di build diverse (chi-siamo di aprile,
# allerte-meteo di maggio, home di luglio) perché il sync-state FTP salta
# alcuni file.
#
# Come funziona: legge il fingerprint <meta name="pc-build-sha"> di N pagine
# campione, con cache-buster + header no-cache per bypassare le cache
# intermedie, e l'orario dell'ultima build da /build-info.js (output format
# BUILDINFO di Hugo: `window.SITE_BUILD_TIME = "<ISO 8601>"`, un solo file
# per deploy — dal 25/09/2026 le pagine non portano più la meta
# pc-build-time: l'orario sta in un file solo, non in ogni pagina). Poi:
#   - se le pagine servono >1 SHA distinto  → DRIFT (file stantii) → FALLISCE
#   - se una pagina non ha affatto la meta   → build pre-guardia stantia → FALLISCE
#   - se una pagina non risponde 200         → FALLISCE
#   - se /build-info.js è troppo vecchio (default 12h) → FROZEN → FALLISCE
# Ripete il campionamento (retry) per assorbire il ritardo di propagazione
# subito dopo un deploy: si ferma appena tutto è coerente e recente.
#
# Uso:
#   scripts/verifica-fingerprint-live.sh                     # verifica live
#   scripts/verifica-fingerprint-live.sh --sha 1a2b3c4       # SHA atteso (info)
#   scripts/verifica-fingerprint-live.sh --base https://... --retries 6 --wait 60 --stale-hours 12
#   scripts/verifica-fingerprint-live.sh --diagnostica       # stampa solo i fingerprint
#
# Exit code 0 se tutto allineato, 1 se rileva drift/staleness/errori.

set -u

BASE="https://www.protezionecivilegenzano.it"
EXPECTED_SHA=""
RETRIES=6
WAIT=60
STALE_HOURS=12
DIAG=false

while [ $# -gt 0 ]; do
  case "$1" in
    --base)         BASE="$2"; shift 2 ;;
    --sha)          EXPECTED_SHA="$2"; shift 2 ;;
    --retries)      RETRIES="$2"; shift 2 ;;
    --wait)         WAIT="$2"; shift 2 ;;
    --stale-hours)  STALE_HOURS="$2"; shift 2 ;;
    --diagnostica)  DIAG=true; shift ;;
    *) echo "Argomento sconosciuto: $1" >&2; exit 2 ;;
  esac
done
BASE="${BASE%/}"

# Solo pagine RESE DA HUGO CON baseof.html (che inietta la meta pc-build-sha).
# Set = pagine ad alto traffico + quelle storicamente andate stantie (rule 05 § 43).
# ESCLUSE le pagine STANDALONE che NON usano baseof.html e quindi non possono
# avere la meta di build (segnalarle sarebbe un falso positivo):
#   /emergenza/ → layout emergenza/single.html standalone ultra-leggero (no baseof)
#   /lanterna/  → standalone, non usa baseof
# Anche le mini-app statiche sotto static/ sono escluse (chrome iniettato lato client).
PAGES="/ /allerte-meteo/ /chi-siamo/ /numeri-utili/ /contatti/ \
       /cosa-fare-adesso/ /rischi-prevenzione/ /accessibilita/ \
       /diventa-volontario/ /area-download/ /formazione/ /comunicazioni/ \
       /piano-emergenza/ /faq/ /glossario/"

# Estrae il valore di content="" dalla meta pc-build-sha,
# indipendente dall'ordine degli attributi (Hugo minify può riordinarli).
_meta() {
  # $1 = html, $2 = nome meta → stampa il content (vuoto se assente)
  printf '%s' "$1" | tr '>' '\n' | grep "$2" | head -1 \
    | grep -oE 'content="[^"]*"' | head -1 | sed -E 's/content="([^"]*)"/\1/'
}

fetch_fp() {
  # $1 = path → stampa "http_status|sha"
  local path="$1" cb html status sha
  cb="cb=$(date +%s)$RANDOM"
  html=$(curl -s --max-time 20 \
              -H 'Cache-Control: no-cache' -H 'Pragma: no-cache' \
              "$BASE$path?$cb" 2>/dev/null)
  status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 20 \
              -H 'Cache-Control: no-cache' -H 'Pragma: no-cache' \
              "$BASE$path?$cb" 2>/dev/null)
  sha=$(_meta "$html" 'pc-build-sha')
  printf '%s|%s' "${status:-000}" "${sha:-MANCANTE}"
}

# Orario dell'ultima build servita: /build-info.js (BUILDINFO, un file solo).
fetch_build_time() {
  local cb js
  cb="cb=$(date +%s)$RANDOM"
  js=$(curl -s --max-time 20 \
            -H 'Cache-Control: no-cache' -H 'Pragma: no-cache' \
            "$BASE/build-info.js?$cb" 2>/dev/null)
  printf '%s' "$js" | grep -oE 'SITE_BUILD_TIME *= *"[^"]*"' | head -1 \
    | sed -E 's/.*"([^"]*)"/\1/'
  printf '|'
  printf '%s' "$js" | grep -oE 'SITE_BUILD_SHA *= *"[^"]*"' | head -1 \
    | sed -E 's/.*"([^"]*)"/\1/'
}

echo "=== Verifica fingerprint build live: $BASE ==="
[ -n "$EXPECTED_SHA" ] && echo "SHA atteso (deploy che ha triggerato): $EXPECTED_SHA"
echo ""

PENDING="$PAGES"
attempt=0
declare -A SHA_OF STATUS_OF

while :; do
  attempt=$((attempt+1))
  NEXT_PENDING=""
  for path in $PENDING; do
    IFS='|' read -r st sha <<< "$(fetch_fp "$path")"
    STATUS_OF[$path]="$st"; SHA_OF[$path]="$sha"
    if [ "$st" = "200" ] && [ "$sha" != "MANCANTE" ] && [ -n "$sha" ]; then
      : # risolto per questa pagina
    else
      NEXT_PENDING="$NEXT_PENDING $path"
    fi
  done
  PENDING="$(echo "$NEXT_PENDING" | xargs 2>/dev/null || true)"
  [ "$DIAG" = "true" ] && break
  # Ferma i retry se tutte hanno risposto E c'è un solo SHA distinto
  if [ -z "$PENDING" ]; then
    DISTINCT=$(for p in $PAGES; do echo "${SHA_OF[$p]}"; done | sort -u | wc -l | tr -d ' ')
    [ "$DISTINCT" = "1" ] && break
  fi
  if [ "$attempt" -ge "$RETRIES" ]; then break; fi
  echo "Tentativo $attempt: non ancora coerente, attendo ${WAIT}s (propagazione)…"
  sleep "$WAIT"
done

echo ""
echo "## Fingerprint rilevati"
for path in $PAGES; do
  printf '  %-24s status=%s  sha=%s\n' "$path" "${STATUS_OF[$path]}" "${SHA_OF[$path]}"
done
BUILD_INFO="$(fetch_build_time)"
BUILD_TIME="${BUILD_INFO%%|*}"
BUILD_SHA="${BUILD_INFO#*|}"
echo "  build-info.js: ultima build ${BUILD_TIME:-NON LEGGIBILE}"

if [ "$DIAG" = "true" ]; then
  echo ""
  echo "(modalità diagnostica: nessun giudizio)"
  exit 0
fi

# ── Valutazione ──────────────────────────────────────────────────────────
ERRORS=0
STALE_PAGES=""
MISSING_PAGES=""
DOWN_PAGES=""

for path in $PAGES; do
  st="${STATUS_OF[$path]}"; sha="${SHA_OF[$path]}"
  if [ "$st" != "200" ]; then DOWN_PAGES="$DOWN_PAGES $path($st)"; ERRORS=$((ERRORS+1)); continue; fi
  if [ "$sha" = "MANCANTE" ] || [ -z "$sha" ]; then MISSING_PAGES="$MISSING_PAGES $path"; ERRORS=$((ERRORS+1)); fi
done

# SHA distinti fra le pagine raggiungibili con meta presente
DISTINCT_LIST=$(for p in $PAGES; do
  [ "${STATUS_OF[$p]}" = "200" ] && [ "${SHA_OF[$p]}" != "MANCANTE" ] && [ -n "${SHA_OF[$p]}" ] && echo "${SHA_OF[$p]}"
done | sort | uniq -c | sort -rn)
N_DISTINCT=$(printf '%s\n' "$DISTINCT_LIST" | grep -c . || true)

echo ""
echo "## Esito"
[ -n "$DOWN_PAGES" ]    && echo "❌ Pagine non raggiungibili (≠200):$DOWN_PAGES"
[ -n "$MISSING_PAGES" ] && echo "❌ Pagine SENZA meta pc-build-sha (build pre-guardia = stantia):$MISSING_PAGES"

if [ "${N_DISTINCT:-0}" -gt 1 ]; then
  ERRORS=$((ERRORS+1))
  echo "❌ DRIFT DI GENERAZIONI: le pagine servono $N_DISTINCT build diverse su Aruba."
  echo "   Conteggio per SHA (occorrenze  sha):"
  printf '%s\n' "$DISTINCT_LIST" | sed 's/^/     /'
  # SHA di minoranza = quelli in ritardo
  MAJORITY=$(printf '%s\n' "$DISTINCT_LIST" | head -1 | awk '{print $2}')
  echo "   Build corrente prevalente: $MAJORITY. Pagine in ritardo:"
  for p in $PAGES; do
    [ "${STATUS_OF[$p]}" = "200" ] && [ "${SHA_OF[$p]}" != "MANCANTE" ] && [ "${SHA_OF[$p]}" != "$MAJORITY" ] \
      && echo "     $p → ${SHA_OF[$p]}"
  done
fi

# Freschezza: l'ultima build servita (/build-info.js) deve essere entro STALE_HOURS.
NEWEST_TS=0
[ -n "$BUILD_TIME" ] && NEWEST_TS=$(date -u -d "$BUILD_TIME" +%s 2>/dev/null || echo 0)
if [ "$NEWEST_TS" -gt 0 ]; then
  AGE_H=$(( ($(date -u +%s) - NEWEST_TS) / 3600 ))
  echo "ℹ️  Ultima build servita (build-info.js): $BUILD_TIME (${AGE_H}h fa)"
  if [ "$AGE_H" -gt "$STALE_HOURS" ]; then
    ERRORS=$((ERRORS+1))
    echo "❌ SITO CONGELATO: l'ultima build servita ha ${AGE_H}h (> ${STALE_HOURS}h). Deploy fermo o upload FTP bloccato."
  fi
else
  echo "⚠️  /build-info.js non leggibile: freschezza della build non verificabile in questo giro."
fi

LIVE_SHA=$(printf '%s\n' "$DISTINCT_LIST" | head -1 | awk '{print $2}')

# L'orario di build-info.js vale per le pagine solo se è della stessa build:
# un upload che aggiorna build-info.js ma nessun HTML campione lascerebbe
# pagine tutte coerenti fra loro, ferme alla build prima, con un orario
# fresco. Il confronto dello SHA lo intercetta (revisione del 26/09/2026).
if [ -n "$BUILD_SHA" ] && [ -n "$LIVE_SHA" ] && [ "$BUILD_SHA" != "$LIVE_SHA" ]; then
  ERRORS=$((ERRORS+1))
  echo "❌ BUILD NON ALLINEATA: build-info.js è della build $BUILD_SHA, le pagine campione della $LIVE_SHA."
  echo "   L'orario di build-info.js non descrive le pagine servite: upload FTP incompleto o fermo."
elif [ -z "$BUILD_SHA" ] && [ -n "$BUILD_TIME" ]; then
  echo "ℹ️  build-info.js senza SHA (build precedente al 26/09/2026): confronto con le pagine non possibile in questo giro."
fi
[ -n "$EXPECTED_SHA" ] && [ -n "$LIVE_SHA" ] && [ "$EXPECTED_SHA" != "$LIVE_SHA" ] \
  && echo "ℹ️  SHA live ($LIVE_SHA) ≠ SHA atteso ($EXPECTED_SHA): può essere un deploy successivo (non è di per sé un errore)."

echo ""
echo "=================================="
if [ "$ERRORS" = "0" ]; then
  echo "✅ Tutte le pagine campione servono la stessa build recente. Nessun drift."
  exit 0
else
  echo "❌ Guardia anti-stale: $ERRORS problema/i. Rimedio MIRATO sulle pagine in ritardo (cache-bust del sorgente _index.md o cancellazione del file lato server, rule 05): MAI il bump di state-name in deploy.yml (re-upload integrale che non completa e congela il sito, 03/07/2026)."
  exit 1
fi
