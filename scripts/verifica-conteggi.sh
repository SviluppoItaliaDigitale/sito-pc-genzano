#!/usr/bin/env bash
# verifica-conteggi.sh — controllo che i conteggi dichiarati sul sito
# (schede stampabili, giochi, attività Abili a Proteggere) corrispondano
# al numero reale di cartelle presenti.
#
# Uso:
#   bash scripts/verifica-conteggi.sh           # output completo + exit 0/1
#   bash scripts/verifica-conteggi.sh --quiet   # output solo se trova drift
#   bash scripts/verifica-conteggi.sh --strict  # exit 1 anche su warning
#
# Eseguito automaticamente:
# - All'inizio di ogni sessione di Claude Code via .claude/settings.json hook
#   SessionStart (vale per tutti i maintainer / nuovi cloni del repo)
# - Ogni lunedì in audit-sito.yml § 42 (catch-all CI)
#
# Specifiche memory: feedback_conteggi_per_fascia.md

set -u

REPO="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO" || exit 0

QUIET=0
STRICT=0
for arg in "$@"; do
  case "$arg" in
    --quiet) QUIET=1 ;;
    --strict) STRICT=1 ;;
  esac
done

DRIFT=0
WARN=0
REPORT=""

# ---------- Conta reale ----------
SCHEDE_DIR="static/formazione/schede-stampabili"
GIOCHI_DIR="static/giochi"
ABILI_DIR="static/abili-a-proteggere"

[ -d "$SCHEDE_DIR" ] || { echo "Skip verifica: $SCHEDE_DIR non trovato (forse non sei nel repo)"; exit 0; }

REAL_INF=$(ls "$SCHEDE_DIR" 2>/dev/null | grep -E '\-infanzia$' | wc -l)
REAL_PRI=$(ls "$SCHEDE_DIR" 2>/dev/null | grep -E '\-primaria$' | wc -l)
REAL_S1=$(ls "$SCHEDE_DIR" 2>/dev/null | grep -E '\-secondaria$' | wc -l)
REAL_S2=$(ls "$SCHEDE_DIR" 2>/dev/null | grep -E '\-secondaria2$' | wc -l)
REAL_S2_CASO=$(ls "$SCHEDE_DIR" 2>/dev/null | grep -E '^caso-.*-secondaria2$' | wc -l)
REAL_GEN=$(ls "$SCHEDE_DIR" 2>/dev/null | grep -vE '\-(infanzia|primaria|secondaria2?)$|^assets$|^index\.html$' | wc -l)
SCHEDE_TOT=$((REAL_INF + REAL_PRI + REAL_S1 + REAL_S2 + REAL_GEN))

GIOCHI_INF=$(ls "$GIOCHI_DIR/infanzia/" 2>/dev/null | grep -vE "^assets$|^index\.html$" | wc -l)
GIOCHI_PRI=$(ls "$GIOCHI_DIR/primaria/" 2>/dev/null | grep -vE "^assets$|^index\.html$" | wc -l)
GIOCHI_RAG=$(ls "$GIOCHI_DIR/ragazzi/" 2>/dev/null | grep -vE "^assets$|^index\.html$" | wc -l)
GIOCHI_TOT=$((GIOCHI_INF + GIOCHI_PRI + GIOCHI_RAG))

ABILI_TOT=$(find "$ABILI_DIR" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)

STORIE_DIR="static/formazione/storie-e-racconti"
STORIE_TOT=$(find "$STORIE_DIR" -mindepth 1 -maxdepth 1 -type d ! -name assets 2>/dev/null | wc -l)

# ---------- Funzione check ----------
# check_count <expected_real> <pattern_regex> <file> <descrizione>
check_count() {
  local expected="$1"
  local pattern="$2"
  local file="$3"
  local desc="$4"
  [ -f "$file" ] || return 0
  local match found
  # Prende il primo match, poi estrae SOLO il numero che inizia la stringa.
  match=$(grep -oE "$pattern" "$file" | head -1)
  found=$(echo "$match" | grep -oE "^[0-9]+" || true)
  if [ -n "$found" ] && [ "$found" != "$expected" ]; then
    REPORT="${REPORT}- DRIFT \`$file\` $desc: dichiara $found, reale $expected\n"
    DRIFT=$((DRIFT + 1))
  fi
}

# ---------- Check totali ----------
check_count "$SCHEDE_TOT" "[0-9]+ schede stampabili" \
  "themes/flavour-pcgenzano/layouts/assistente/list.html" "(totale schede)"
check_count "$SCHEDE_TOT" "[0-9]+ schede" \
  "static/formazione/schede-stampabili/index.html" "(meta description / lead)"
check_count "$SCHEDE_TOT" "[0-9]+ schede stampabili" \
  "content/faq/_index.md" "(faq materiale didattico)"
check_count "$SCHEDE_TOT" "[0-9]+ schede A4" \
  "content/mappa-sito/_index.md" "(card schede)"

check_count "$GIOCHI_TOT" "[0-9]+ giochi educativi" \
  "content/formazione/_index.md" "(totale giochi)"
check_count "$GIOCHI_TOT" "[0-9]+ giochi educativi" \
  "themes/flavour-pcgenzano/layouts/partials/games-cta.html" "(games-cta totale)"
check_count "$GIOCHI_TOT" "[0-9]+ giochi" \
  "themes/flavour-pcgenzano/layouts/assistente/list.html" "(assistente per le scuole)"
check_count "$GIOCHI_TOT" "[0-9]+ giochi educativi" \
  "content/faq/_index.md" "(faq giochi)"
check_count "$GIOCHI_TOT" "[0-9]+ giochi educativi" \
  "content/mappa-sito/_index.md" "(card giochi)"

check_count "$ABILI_TOT" "[0-9]+ attività accessibili" \
  "themes/flavour-pcgenzano/layouts/partials/games-cta.html" "(Abili a Proteggere CTA)"
check_count "$ABILI_TOT" "[0-9]+ attività accessibili" \
  "themes/flavour-pcgenzano/layouts/assistente/list.html" "(assistente Abili a Proteggere)"
check_count "$ABILI_TOT" "[0-9]+ attività accessibili" \
  "content/formazione/_index.md" "(formazione Abili a Proteggere)"
check_count "$ABILI_TOT" "[0-9]+ attività accessibili" \
  "content/faq/_index.md" "(faq Abili a Proteggere)"
check_count "$ABILI_TOT" "[0-9]+ attività accessibili" \
  "content/mappa-sito/_index.md" "(card Abili a Proteggere)"
check_count "$ABILI_TOT" "[0-9]+ attività disponibili" \
  "static/giochi/index.html" "(hub giochi card Abili a Proteggere)"

# Storie e racconti
check_count "$STORIE_TOT" "[0-9]+ storie e racconti" \
  "content/faq/_index.md" "(faq storie e racconti)"
check_count "$STORIE_TOT" "[0-9]+ fiabe e racconti" \
  "content/mappa-sito/_index.md" "(card storie e racconti)"
check_count "$STORIE_TOT" "[0-9]+ storie di qualità letteraria" \
  "content/formazione/_index.md" "(formazione storie)"

# ---------- Check per fascia (assistente) ----------
ASSIST="themes/flavour-pcgenzano/layouts/assistente/list.html"
if [ -f "$ASSIST" ]; then
  # Linee specifiche per fascia
  INF_DECL=$(grep -E "Per i bambini di 3-6 anni" "$ASSIST" | grep -oE "[0-9]+ schede" | head -1 | grep -oE "[0-9]+" || echo "")
  PRI_DECL=$(grep -E "Per gli alunni di 6-11 anni" "$ASSIST" | grep -oE "[0-9]+ schede" | head -1 | grep -oE "[0-9]+" || echo "")
  S1_DECL=$(grep -E "Per gli alunni di 11-14 anni" "$ASSIST" | grep -oE "[0-9]+ schede" | head -1 | grep -oE "[0-9]+" || echo "")
  S2_DECL=$(grep -E "Per gli studenti di 14-19 anni" "$ASSIST" | grep -oE "[0-9]+ schede" | head -1 | grep -oE "[0-9]+" || echo "")

  [ -n "$INF_DECL" ] && [ "$INF_DECL" != "$REAL_INF" ] && {
    REPORT="${REPORT}- DRIFT assistente Infanzia: dichiara $INF_DECL schede, reali $REAL_INF\n"
    DRIFT=$((DRIFT + 1))
  }
  [ -n "$PRI_DECL" ] && [ "$PRI_DECL" != "$REAL_PRI" ] && {
    REPORT="${REPORT}- DRIFT assistente Primaria: dichiara $PRI_DECL schede, reali $REAL_PRI\n"
    DRIFT=$((DRIFT + 1))
  }
  [ -n "$S1_DECL" ] && [ "$S1_DECL" != "$REAL_S1" ] && {
    REPORT="${REPORT}- DRIFT assistente Sec I: dichiara $S1_DECL schede, reali $REAL_S1\n"
    DRIFT=$((DRIFT + 1))
  }
  [ -n "$S2_DECL" ] && [ "$S2_DECL" != "$REAL_S2" ] && {
    REPORT="${REPORT}- DRIFT assistente Sec II: dichiara $S2_DECL schede, reali $REAL_S2\n"
    DRIFT=$((DRIFT + 1))
  }
fi

# Case study Sec II nel catalogo
CATALOGO="static/formazione/schede-stampabili/index.html"
if [ -f "$CATALOGO" ]; then
  CASO_DECL=$(grep -oE "[0-9]+ schede di analisi sistemica" "$CATALOGO" | head -1 | grep -oE "[0-9]+" || echo "")
  [ -n "$CASO_DECL" ] && [ "$CASO_DECL" != "$REAL_S2_CASO" ] && {
    REPORT="${REPORT}- DRIFT catalogo case study Sec II: dichiara $CASO_DECL, reali $REAL_S2_CASO\n"
    DRIFT=$((DRIFT + 1))
  }
fi

# ---------- Output ----------
if [ "$DRIFT" -gt 0 ]; then
  echo ""
  echo "⚠️  CONTEGGI SBAGLIATI sul sito ($DRIFT drift trovati):"
  echo ""
  printf "%b" "$REPORT"
  echo ""
  echo "Conta REALE da repo:"
  echo "  - Schede stampabili: $SCHEDE_TOT (Inf=$REAL_INF, Pri=$REAL_PRI, S1=$REAL_S1, S2=$REAL_S2 [di cui $REAL_S2_CASO case study], Gen=$REAL_GEN)"
  echo "  - Giochi educativi:  $GIOCHI_TOT (Inf=$GIOCHI_INF, Pri=$GIOCHI_PRI, Rag=$GIOCHI_RAG)"
  echo "  - Abili a Proteggere: $ABILI_TOT"
  echo "  - Storie e Racconti: $STORIE_TOT"
  echo ""
  echo "Aggiornare i contatori con i numeri reali sopra. Memory rule:"
  echo "  ~/.claude/projects/-home-iu0qvw-sito-pc-genzano/memory/feedback_conteggi_per_fascia.md"
  echo ""
  exit 1
elif [ "$QUIET" -eq 0 ]; then
  echo "✅ Conteggi schede/giochi/attività/storie coerenti col reale: schede=$SCHEDE_TOT, giochi=$GIOCHI_TOT, abili=$ABILI_TOT, storie=$STORIE_TOT"
fi

exit 0
