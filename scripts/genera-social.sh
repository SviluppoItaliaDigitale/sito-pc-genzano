#!/usr/bin/env bash
# Wrapper rapido per generare bozze social di un articolo.
#
# Uso:
#   bash scripts/genera-social.sh content/comunicazioni/2026-04-20-articolo.md
#   bash scripts/genera-social.sh --all
#   bash scripts/genera-social.sh --since 2026-04-01
#   bash scripts/genera-social.sh --dry-run content/comunicazioni/<file>.md
#
# Cosa fa, per ogni articolo:
#   1) chiama scripts/genera-social.py (Gemini) -> 4 file .txt in social-bozze/AAAA/MM/<slug>/
#   2) chiama scripts/genera-immagini-social.py (Pillow) -> .webp nella STESSA cartella
#      social-bozze/AAAA/MM/<slug>/ (instagram-post*.webp + instagram-story.webp)
#
# Variabili richieste:
#   GEMINI_API_KEY  (vedi README-social.md per setup)

set -e
cd "$(dirname "$0")/.."

if [ -z "$GEMINI_API_KEY" ]; then
  echo "ERRORE: GEMINI_API_KEY non impostata."
  echo "Aggiungi 'export GEMINI_API_KEY=la-tua-chiave' a ~/.bashrc e fai 'source ~/.bashrc'."
  exit 2
fi

echo "=== 1/2: Genero bozze testuali (Gemini API) ==="
python3 scripts/genera-social.py "$@"

# Se siamo in dry-run o l'utente ha passato --since/--all senza un singolo articolo
# generiamo le immagini per gli stessi articoli.
echo ""
echo "=== 2/2: Genero immagini Instagram (post + story) ==="
# Se è --dry-run salto le immagini (non c'è punto a fare PNG di prova)
case " $* " in
  *" --dry-run "*)
    echo "  (saltato per --dry-run)"
    ;;
  *)
    # Passa gli stessi argomenti a parte --dry-run
    python3 scripts/genera-immagini-social.py "$@"
    ;;
esac

echo ""
echo "✅ Fatto. Tutto (testi + immagini) in: social-bozze/AAAA/MM/<slug>/"
