#!/bin/bash
# ============================================================
# MODIFICA PAGINA — Script Interattivo
# Uso: bash ~/modifica-pagina.sh
# ============================================================

cd ~/sito-pc-genzano
git pull --rebase 2>/dev/null || git pull 2>/dev/null || true

echo ""
echo "============================================"
echo "  ✏️  MODIFICA UNA PAGINA DEL SITO"
echo "  Protezione Civile Genzano di Roma"
echo "============================================"
echo ""
echo "  Quale pagina vuoi modificare?"
echo ""
echo "  ── PAGINE PRINCIPALI ──"
echo "   1) Home"
echo "   2) Chi Siamo"
echo "   3) Diventa Volontario"
echo "   4) Contatti"
echo ""
echo "  ── RISCHI E PREVENZIONE ──"
echo "   5) Rischi e Prevenzione (pagina principale)"
echo "   6) Rischio Incendio"
echo "   7) Rischio Idrogeologico"
echo "   8) Rischio Sismico"
echo ""
echo "  ── ALLERTE E PIANIFICAZIONE ──"
echo "   9) Allerte Meteo"
echo "  10) Piano di Emergenza"
echo "  11) Piano Familiare"
echo "  12) Cartografia Operativa"
echo ""
echo "  ── DOCUMENTI E RISORSE ──"
echo "  13) Area Download"
echo "  14) Siti Utili"
echo "  15) Comunicazioni (pagina principale)"
echo ""
echo "  ── PAGINE LEGALI ──"
echo "  16) Note Legali"
echo "  17) Privacy e Cookie"
echo "  18) Accessibilita"
echo ""
echo "  ── ALTRO ──"
echo "  19) Cerca (pagina di ricerca)"
echo "   0) Esci"
echo ""
echo -n "  Scegli il numero: "
read -r SCELTA

case $SCELTA in
  1)  FILE="content/_index.md"; NOME="Home" ;;
  2)  FILE="content/chi-siamo/_index.md"; NOME="Chi Siamo" ;;
  3)  FILE="content/diventa-volontario/_index.md"; NOME="Diventa Volontario" ;;
  4)  FILE="content/contatti/_index.md"; NOME="Contatti" ;;
  5)  FILE="content/rischi-prevenzione/_index.md"; NOME="Rischi e Prevenzione" ;;
  6)  FILE="content/rischi-prevenzione/rischio-incendio.md"; NOME="Rischio Incendio" ;;
  7)  FILE="content/rischi-prevenzione/rischio-idrogeologico.md"; NOME="Rischio Idrogeologico" ;;
  8)  FILE="content/rischi-prevenzione/rischio-sismico.md"; NOME="Rischio Sismico" ;;
  9)  FILE="content/allerte-meteo/_index.md"; NOME="Allerte Meteo" ;;
  10) FILE="content/piano-emergenza/_index.md"; NOME="Piano di Emergenza" ;;
  11) FILE="content/piano-familiare/_index.md"; NOME="Piano Familiare" ;;
  12) FILE="content/cartografia/_index.md"; NOME="Cartografia Operativa" ;;
  13) FILE="content/area-download/_index.md"; NOME="Area Download" ;;
  14) FILE="content/siti-utili/_index.md"; NOME="Siti Utili" ;;
  15) FILE="content/comunicazioni/_index.md"; NOME="Comunicazioni" ;;
  16) FILE="content/note-legali/_index.md"; NOME="Note Legali" ;;
  17) FILE="content/privacy/_index.md"; NOME="Privacy e Cookie" ;;
  18) FILE="content/accessibilita/_index.md"; NOME="Accessibilita" ;;
  19) FILE="content/cerca/_index.md"; NOME="Cerca" ;;
  0)  echo "Arrivederci!"; exit 0 ;;
  *)  echo "❌ Scelta non valida!"; exit 1 ;;
esac

echo ""
echo "──────────────────────────────────────"
echo "  📄 Apertura: $NOME"
echo "  📁 File: $FILE"
echo "──────────────────────────────────────"
echo ""

if [ ! -f "$FILE" ]; then
  echo "❌ File non trovato: $FILE"
  exit 1
fi

# Scegli editor
EDITOR_CMD=""
if command -v code &>/dev/null; then
  echo "  Quale editor vuoi usare?"
  echo "  1) Visual Studio Code (grafico)"
  echo "  2) nano (terminale)"
  echo "  3) gedit (blocco note grafico)"
  echo -n "  Scegli: "
  read -r EDITOR_SCELTA
  case $EDITOR_SCELTA in
    1) EDITOR_CMD="code" ;;
    2) EDITOR_CMD="nano" ;;
    3) EDITOR_CMD="gedit" ;;
    *) EDITOR_CMD="nano" ;;
  esac
else
  echo "  Quale editor vuoi usare?"
  echo "  1) nano (terminale)"
  echo "  2) gedit (blocco note grafico)"
  echo -n "  Scegli: "
  read -r EDITOR_SCELTA
  case $EDITOR_SCELTA in
    1) EDITOR_CMD="nano" ;;
    2) EDITOR_CMD="gedit" ;;
    *) EDITOR_CMD="nano" ;;
  esac
fi

echo ""
echo "  📝 Apertura con $EDITOR_CMD..."
echo ""
echo "  ╔════════════════════════════════════════╗"
echo "  ║  GUIDA RAPIDA MARKDOWN:                ║"
echo "  ║                                        ║"
echo "  ║  # Titolo grande                       ║"
echo "  ║  ## Sottotitolo                        ║"
echo "  ║  ### Sotto-sottotitolo                 ║"
echo "  ║  **grassetto**                         ║"
echo "  ║  *corsivo*                             ║"
echo "  ║  [testo link](https://url.com)         ║"
echo "  ║  - elenco puntato                      ║"
echo "  ║  1. elenco numerato                    ║"
echo "  ║                                        ║"
echo "  ║  Per nano: Ctrl+O salva, Ctrl+X esci   ║"
echo "  ╚════════════════════════════════════════╝"
echo ""

# Apri l'editor
if [ "$EDITOR_CMD" = "code" ]; then
  code "$FILE"
  echo "  Il file è aperto in VS Code."
  echo "  Quando hai finito di modificare, torna qui."
elif [ "$EDITOR_CMD" = "gedit" ]; then
  gedit "$FILE" &
  echo "  Il file è aperto in gedit."
  echo "  Quando hai finito di modificare, salva e torna qui."
else
  nano "$FILE"
fi

echo ""
echo "──────────────────────────────────────"
echo ""

# Verifica se ci sono modifiche
if git diff --quiet "$FILE" 2>/dev/null && git diff --cached --quiet "$FILE" 2>/dev/null; then
  echo "  ℹ️  Nessuna modifica rilevata."
  echo "  Se hai modificato con un editor grafico, premi Invio dopo aver salvato."
  read -r ATTESA
fi

# Controlla di nuovo
if ! git diff --quiet 2>/dev/null || ! git diff --cached --quiet 2>/dev/null; then
  echo "  📋 Modifiche rilevate!"
  echo ""
  echo "  Vuoi vedere un'anteprima in locale prima di pubblicare? (s/n)"
  read -r ANTEPRIMA
  if [ "$ANTEPRIMA" = "s" ] || [ "$ANTEPRIMA" = "S" ]; then
    echo ""
    echo "  🌐 Avvio server locale..."
    echo "  Apri http://localhost:1313/ nel browser"
    echo "  Premi Ctrl+C per fermare e tornare qui."
    echo ""
    hugo server -D 2>/dev/null
  fi

  echo ""
  echo "  🚀 Vuoi pubblicare le modifiche online? (s/n)"
  read -r PUBBLICA
  if [ "$PUBBLICA" = "s" ] || [ "$PUBBLICA" = "S" ]; then
    git add -A
    git commit -m "✏️ Aggiornata pagina: $NOME"
    git push
    echo ""
    echo "  ✅ MODIFICHE PUBBLICATE!"
    echo "  Il sito si aggiornera tra 2-3 minuti."
    echo "  https://sviluppoitaliadigitale.github.io/sito-pc-genzano/"
  else
    echo ""
    echo "  📋 Modifiche salvate in locale."
    echo "  Per pubblicare dopo:"
    echo "  cd ~/sito-pc-genzano && git add -A && git commit -m \"Aggiornamento\" && git push"
  fi
else
  echo "  ℹ️  Nessuna modifica da pubblicare."
fi

echo ""
echo "  Vuoi modificare un'altra pagina? (s/n)"
read -r ALTRA
if [ "$ALTRA" = "s" ] || [ "$ALTRA" = "S" ]; then
  exec bash ~/modifica-pagina.sh
fi

echo ""
echo "============================================"
echo "  Arrivederci! 73 de IU0QVW"
echo "============================================"
