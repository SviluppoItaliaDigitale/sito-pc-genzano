#!/usr/bin/env bash
# Smoke test del sito live: verifica HTTP status e contenuti chiave
# delle pagine critiche dopo ogni deploy. Riproducibile.
#
# Uso:
#   bash scripts/smoke-test-live.sh
#   bash scripts/smoke-test-live.sh --base https://altro-host.it
#
# Exit code 0 se tutto OK, 1 se trova problemi.

set -u

BASE="${1:-}"
[ "$BASE" = "--base" ] && BASE="$2"
[ -z "$BASE" ] && BASE="https://www.protezionecivilegenzano.it"

ERRORS=0

ok()  { echo "✅ $1"; }
err() { echo "❌ $1"; ERRORS=$((ERRORS+1)); }

fetch() { curl -s --max-time 15 "$1" 2>/dev/null; }
status() { curl -s -o /dev/null -w "%{http_code}" --max-time 15 "$1" 2>/dev/null; }

echo "=== Smoke test live: $BASE ==="
echo ""

# 1. HTTP 200 sulle pagine principali
echo "## 1. Status HTTP pagine principali"
for path in "/" "/cartografia/" "/quizpc/" "/giochi/" "/assistente/" \
            "/comunicazioni/" "/cosa-fare-adesso/" "/numeri-utili/" \
            "/contatti/" "/formazionepc/" "/abili-a-proteggere/" \
            "/cerca/" "/area-download/" "/formazione/" "/faq/" \
            "/rischi-prevenzione/" "/diventa-volontario/" \
            "/piano-emergenza/" "/piano-familiare/" "/glossario/"; do
  s=$(status "$BASE$path")
  if [ "$s" = "200" ]; then
    ok "$path → $s"
  else
    err "$path → $s"
  fi
done

# 2. Lingue (7 traduzioni)
echo ""
echo "## 2. Pagine di lingua"
for lang in en de es fr pt ro eo; do
  s=$(status "$BASE/$lang/")
  [ "$s" = "200" ] && ok "/$lang/ → $s" || err "/$lang/ → $s"
done

# 3. Mini-app statiche (sub-routes)
echo ""
echo "## 3. Mini-app statiche"
for path in "/giochi/infanzia/tartaruga-saggia/" "/giochi/primaria/" \
            "/giochi/ragazzi/" "/abili-a-proteggere/chiama-112/" \
            "/formazione/schede-stampabili/" "/formazione/kit-scuola-infanzia/"; do
  s=$(status "$BASE$path")
  [ "$s" = "200" ] && ok "$path → $s" || err "$path → $s"
done

# 4. Marker JS/HTML chiave (contenuti specifici)
echo ""
echo "## 4. Marker JS/HTML chiave"

HTML=$(fetch "$BASE/assistente/")
[ "$(echo "$HTML" | grep -c 'assistente-app')" -ge 1 ] && ok "Assistente: container app presente" || err "Assistente: manca container"
[ "$(echo "$HTML" | grep -oE "Sento una scossa|Vedo fumo|odore di gas|allerta meteo attiva|allagamento|diventare volontario|numero utile|IT-alert" | sort -u | wc -l)" = "8" ] && ok "Assistente: tutti gli 8 percorsi presenti" || err "Assistente: percorsi mancanti"

HTML=$(fetch "$BASE/cartografia/")
[ "$(echo "$HTML" | grep -c 'leaflet')" -ge 1 ] && ok "Cartografia: Leaflet caricato" || err "Cartografia: Leaflet mancante"
[ "$(echo "$HTML" | grep -c 'dati-aree-emergenza')" -ge 1 ] && ok "Cartografia: dati aree JSON presenti" || err "Cartografia: dati JSON mancanti"

HTML=$(fetch "$BASE/numeri-utili/")
[ "$(echo "$HTML" | grep -oE '\b112\b' | wc -l)" -ge 1 ] && ok "Numeri utili: 112 presente" || err "Numeri utili: 112 mancante"
[ "$(echo "$HTML" | grep -ciE 'chiama[rt]?e? il (115|118|1515)')" = "0" ] && ok "Numeri utili: nessun 115/118/1515 imperativo" || err "Numeri utili: c'è 115/118/1515 da chiamare"

HTML=$(fetch "$BASE/area-download/")
[ "$(echo "$HTML" | grep -c 'Piano_AIB_Lazio.pdf')" -ge 1 ] && ok "Area download: link Piano AIB presente" || err "Area download: link Piano AIB mancante"
[ "$(echo "$HTML" | grep -c 'Piano_Emergenza_Comunale_PC_Genzano.pdf')" -ge 1 ] && ok "Area download: Piano Emergenza Comunale presente" || err "Area download: Piano Emergenza mancante"

HTML=$(fetch "$BASE/quizpc/")
echo "$HTML" | grep -q "Quiz Formativo" && ok "Quiz: H1 presente" || err "Quiz: H1 mancante"

HTML=$(fetch "$BASE/formazionepc/")
echo "$HTML" | grep -q "Piattaforma Formativa" && ok "Formazione PC: H1 presente" || err "Formazione PC: H1 mancante"

HTML=$(fetch "$BASE/abili-a-proteggere/")
echo "$HTML" | grep -q "Abili a Proteggere" && ok "Abili a Proteggere: H1 presente" || err "Abili a Proteggere: H1 mancante"

# 5. Header sicurezza
echo ""
echo "## 5. Header HTTP sicurezza"
HEADERS=$(curl -sI --max-time 10 "$BASE/" 2>/dev/null)
echo "$HEADERS" | grep -qi "permissions-policy" && ok "Permissions-Policy presente" || err "Permissions-Policy mancante"
echo "$HEADERS" | grep -qi "x-content-type-options" && ok "X-Content-Type-Options presente" || err "X-Content-Type-Options mancante"

# Esito
echo ""
echo "=================================="
if [ "$ERRORS" = "0" ]; then
  echo "✅ Smoke test PASSATO. Tutti i controlli OK."
  exit 0
else
  echo "❌ Smoke test FALLITO. $ERRORS errori trovati."
  exit 1
fi
