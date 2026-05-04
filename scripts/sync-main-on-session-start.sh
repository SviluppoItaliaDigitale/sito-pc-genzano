#!/usr/bin/env bash
# sync-main-on-session-start.sh
#
# Riallinea il branch `main` locale a `origin/main` all'avvio della sessione
# Claude Code. Esiste per ovviare al pattern delle sessioni cloud/mobile in
# cui il clone parte da uno stato pre-squash di `main`: la storia su
# `origin/main` e' gia' stata squashata (es. PR #93 a maggio 2026), ma il
# `main` locale contiene ancora i 50 commit individuali pre-squash. Lo
# stop-hook `stop-hook-git-check.sh` lo segnala come "50 commit non pushati"
# e impedisce di chiudere il turno.
#
# Comportamento difensivo (in ordine):
#   1. Esce silenziosamente se non siamo in un repo git
#   2. Esce silenziosamente se non esiste il remote 'origin'
#   3. Esce silenziosamente se NON siamo sul branch 'main'
#      (i feature branch claude/* possono avere lavoro non pushato)
#   4. Esce silenziosamente se ci sono modifiche non committate
#      (non vogliamo mai distruggere lavoro in corso)
#   5. git fetch origin main (timeout 10s)
#   6. Se main locale == origin/main -> esce silenziosamente
#   7. Altrimenti: git reset --hard origin/main e stampa una riga di log
#
# Tutti i print vanno su stderr, JSON-free, una riga sola.
# Stdout resta vuoto: SessionStart hook non si aspetta JSON di controllo.
#
# Per disabilitare temporaneamente: PCGENZANO_SKIP_SYNC=1 nell'env.

set -u

# Esci silenziosamente se opt-out esplicito
[ "${PCGENZANO_SKIP_SYNC:-}" = "1" ] && exit 0

# Vai nella root del repo (lo script puo' essere chiamato da qualsiasi cwd)
ROOT="$(cd "$(dirname "$0")/.." 2>/dev/null && pwd)" || exit 0
cd "$ROOT" 2>/dev/null || exit 0

# 1. Siamo in un repo git?
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || exit 0

# 2. Esiste il remote origin?
git remote get-url origin >/dev/null 2>&1 || exit 0

# 3. Branch corrente
BRANCH="$(git rev-parse --abbrev-ref HEAD 2>/dev/null)" || exit 0
[ "$BRANCH" = "main" ] || exit 0

# 4. Working tree pulito?
if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
  exit 0
fi

# 5. Fetch (timeout di sicurezza: 10s)
timeout 10 git fetch --quiet origin main 2>/dev/null || exit 0

# 6. Confronto SHA
LOCAL_SHA="$(git rev-parse HEAD 2>/dev/null)"
REMOTE_SHA="$(git rev-parse origin/main 2>/dev/null)"
[ -n "$LOCAL_SHA" ] && [ -n "$REMOTE_SHA" ] || exit 0
[ "$LOCAL_SHA" = "$REMOTE_SHA" ] && exit 0

# 7. Sync: count commits divergenti per messaggio diagnostico
AHEAD="$(git rev-list --count origin/main..HEAD 2>/dev/null || echo "?")"
BEHIND="$(git rev-list --count HEAD..origin/main 2>/dev/null || echo "?")"

git reset --hard --quiet origin/main 2>/dev/null || exit 0

# Una riga di log su stderr (visibile all'utente, niente rumore se nulla cambia)
echo "[sync-main] Riallineato main locale a origin/main (era ${AHEAD} avanti, ${BEHIND} indietro). HEAD ora: $(git rev-parse --short origin/main)" >&2

exit 0
