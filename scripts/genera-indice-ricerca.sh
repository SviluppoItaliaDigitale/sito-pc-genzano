#!/usr/bin/env bash
#
# genera-indice-ricerca.sh — Genera l'indice di ricerca full-text Pagefind.
#
# Perché esiste
# -------------
# Il sito usa Pagefind (https://pagefind.app) per la ricerca interna full-text:
# modal accessibile, scorciatoia Ctrl+K, copre le 7 traduzioni, snippet
# evidenziati. Pagefind indicizza il sito GIÀ COSTRUITO (`public/`), quindi
# l'indice non può essere generato dentro `deploy.yml` (vincolo: deploy.yml
# è intoccabile). Questo script lo genera in locale e lo deposita in
# `static/pagefind/`, che Hugo serve come asset statico al deploy successivo.
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
# L'indice è una fotografia: copre solo gli articoli PUBBLICATI al momento
# della generazione. Gli articoli calendarizzati entrano nell'indice solo
# alla ri-esecuzione dello script. Rilancialo dopo aver pubblicato nuovi
# articoli o, come abitudine, una volta a settimana. Un articolo non ancora
# indicizzato resta comunque raggiungibile da menu, archivio e link interni:
# semplicemente non compare nei risultati di ricerca finché non rigeneri.
#
# Dipendenze: Hugo (già richiesto dal progetto) + npx (Node.js). Pagefind è
# scaricato al volo da npx con versione pinnata — niente node_modules nel repo.

set -euo pipefail

# Versione Pagefind pinnata: "latest" è fragile (una release può cambiare
# comportamento senza preavviso). Aggiornare di proposito, testando.
PAGEFIND_VERSION="1.5.2"

cd "$(dirname "$0")/.."
ROOT="$(pwd)"

echo "1/3 · Build Hugo →  public/"
hugo --minify --quiet

echo "2/3 · Indicizzazione Pagefind ${PAGEFIND_VERSION} →  public/pagefind/"
npx -y "pagefind@${PAGEFIND_VERSION}" --site public

echo "3/3 · Copia indice →  static/pagefind/"
rm -rf "${ROOT}/static/pagefind"
cp -r "${ROOT}/public/pagefind" "${ROOT}/static/pagefind"

echo
echo "Fatto. Indice aggiornato in static/pagefind/ ($(du -sh "${ROOT}/static/pagefind" | cut -f1))."
echo "Aggiungilo al commit:  git add static/pagefind/"
