#!/bin/bash
# ============================================================
# GESTIONE SITO — Menu Principale
# Uso: bash ~/gestione-sito.sh
# ============================================================

while true; do
  clear
  echo "============================================"
  echo "  🏛️  GESTIONE SITO WEB"
  echo "  Protezione Civile Genzano di Roma"
  echo "============================================"
  echo ""
  echo "  Cosa vuoi fare?"
  echo ""
  echo "  📰 CONTENUTI"
  echo "   1) Pubblica una nuova notizia"
  echo "   2) Pubblica notizia da file Word"
  echo "   3) Modifica una pagina del sito"
  echo ""
  echo "  🔧 MANUTENZIONE"
  echo "   4) Testa il sito in locale"
  echo "   5) Pubblica modifiche manuali"
  echo "   6) Scarica aggiornamenti dal server"
  echo ""
  echo "  📊 INFO"
  echo "   7) Vedi ultime modifiche"
  echo "   8) Apri il sito online"
  echo "   9) Apri GitHub Actions"
  echo ""
  echo "   0) Esci"
  echo ""
  echo -n "  Scegli: "
  read -r SCELTA

  case $SCELTA in
    1)
      bash ~/pubblica-notizia.sh
      echo "Premi Invio per tornare al menu..."
      read -r
      ;;
    2)
      echo ""
      echo "  Trascina il file Word qui oppure scrivi il percorso:"
      read -r WORD_FILE
      WORD_FILE=$(echo "$WORD_FILE" | tr -d "'\"")
      if [ -f "$WORD_FILE" ]; then
        bash ~/pubblica-da-word.sh "$WORD_FILE"
      else
        echo "  ❌ File non trovato: $WORD_FILE"
      fi
      echo "Premi Invio per tornare al menu..."
      read -r
      ;;
    3)
      bash ~/modifica-pagina.sh
      echo "Premi Invio per tornare al menu..."
      read -r
      ;;
    4)
      echo ""
      echo "  🌐 Avvio server locale..."
      echo "  Apri http://localhost:1313/ nel browser"
      echo "  Premi Ctrl+C per fermare."
      echo ""
      cd ~/sito-pc-genzano && hugo server -D
      echo "Premi Invio per tornare al menu..."
      read -r
      ;;
    5)
      cd ~/sito-pc-genzano
      echo ""
      if git diff --quiet && git diff --cached --quiet; then
        echo "  ℹ️  Nessuna modifica da pubblicare."
      else
        echo "  📋 Modifiche trovate:"
        git status --short
        echo ""
        echo "  Messaggio per il salvataggio:"
        read -r MSG
        MSG=${MSG:-"Aggiornamento sito"}
        git add -A && git commit -m "$MSG" && git push
        echo "  ✅ Pubblicato!"
      fi
      echo "Premi Invio per tornare al menu..."
      read -r
      ;;
    6)
      cd ~/sito-pc-genzano
      echo ""
      git pull --rebase 2>/dev/null || git pull
      echo "  ✅ Aggiornato!"
      echo "Premi Invio per tornare al menu..."
      read -r
      ;;
    7)
      cd ~/sito-pc-genzano
      echo ""
      echo "  📋 Ultime 10 modifiche:"
      echo "  ──────────────────────────────────────"
      git log --oneline -10
      echo "  ──────────────────────────────────────"
      echo "Premi Invio per tornare al menu..."
      read -r
      ;;
    8)
      xdg-open "https://sviluppoitaliadigitale.github.io/sito-pc-genzano/" 2>/dev/null || echo "  Apri nel browser: https://sviluppoitaliadigitale.github.io/sito-pc-genzano/"
      echo "Premi Invio per tornare al menu..."
      read -r
      ;;
    9)
      xdg-open "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions" 2>/dev/null || echo "  Apri nel browser: https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions"
      echo "Premi Invio per tornare al menu..."
      read -r
      ;;
    0)
      echo ""
      echo "  Arrivederci! 73 de IU0QVW"
      echo ""
      exit 0
      ;;
    *)
      echo "  ❌ Scelta non valida!"
      sleep 1
      ;;
  esac
done
