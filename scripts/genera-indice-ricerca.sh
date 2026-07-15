#!/usr/bin/env bash
#
# genera-indice-ricerca.sh — Genera l'indice di ricerca full-text Pagefind.
#
# Perché esiste
# -------------
# Il sito usa Pagefind (https://pagefind.app) per la ricerca interna full-text:
# modal accessibile, scorciatoia Ctrl+K, copre le 7 traduzioni, snippet
# evidenziati. Dal 15/07/2026 l'indice è un ARTEFATTO DI BUILD: lo genera
# deploy.yml in CI (npx pagefind --site public) a ogni deploy e NON è più
# committato (static/pagefind/ è in .gitignore — prima pesava ~432 MB /
# ~18.000 file versionati). Questo script serve SOLO in locale: rigenera
# l'indice in static/pagefind/ così `hugo server` ha la ricerca funzionante
# durante lo sviluppo.
#
# Uso
# ---
#   bash scripts/genera-indice-ricerca.sh
#
# Cosa fa
# -------
#   1. Build del sito con Hugo in `public/`.
#   2. Indicizzazione Pagefind di `public/` → `public/pagefind/`.
#   3. Copia di `public/pagefind/` in `static/pagefind/` (da committare).
#
# Quando rilanciarlo
# ------------------
# Solo per lo sviluppo locale, quando vuoi provare la ricerca con `hugo
# server`. In produzione non serve mai: l'indice live è rigenerato fresco
# da deploy.yml a ogni deploy, sempre allineato ai contenuti pubblicati.
#
# Dipendenze: Hugo (già richiesto dal progetto) + npx (Node.js). Pagefind è
# scaricato al volo da npx con versione pinnata — niente node_modules nel repo.

set -euo pipefail

# Versione Pagefind pinnata: "latest" è fragile (una release può cambiare
# comportamento senza preavviso). Aggiornare di proposito, testando, e IN
# COPPIA con la stessa versione negli step "Genera indice Pagefind" di
# .github/workflows/deploy.yml.
PAGEFIND_VERSION="1.5.2"

cd "$(dirname "$0")/.."
ROOT="$(pwd)"

echo "1/3 · Build Hugo →  public/"
hugo --minify --quiet

echo "2/3 · Indicizzazione Pagefind ${PAGEFIND_VERSION} →  public/pagefind/"
npx -y "pagefind@${PAGEFIND_VERSION}" --site public

echo "3/3 · Copia indice →  static/pagefind/ (solo per hugo server locale)"
rm -rf "${ROOT}/static/pagefind"
cp -r "${ROOT}/public/pagefind" "${ROOT}/static/pagefind"

echo
echo "Fatto. Indice locale in static/pagefind/ ($(du -sh "${ROOT}/static/pagefind" | cut -f1))."
echo "NON va committato: static/pagefind/ è in .gitignore (in produzione lo genera deploy.yml)."
