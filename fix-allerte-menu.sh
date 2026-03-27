#!/bin/bash
# ============================================================
# FIX STATISTICHE + MENU ALLERTE + AUTOMAZIONE MIGLIORATA
# Esegui con: bash fix-allerte-menu.sh
# ============================================================

set -e
cd ~/sito-pc-genzano

echo "📥 Pull..."
git pull --rebase 2>/dev/null || git pull 2>/dev/null || true

# ── 1. FIX ETICHETTE STATISTICHE ──
echo "📊 Fix etichette statistiche..."
sed -i 's/>Anni<\/span>/>Anni di Attivita<\/span>/' themes/flavour-pcgenzano/layouts/index.html
sed -i 's/>Automezzi<\/span>/>Automezzi Operativi<\/span>/' themes/flavour-pcgenzano/layouts/index.html
sed -i 's/>Emergenze<\/span>/>Emergenze Nazionali<\/span>/' themes/flavour-pcgenzano/layouts/index.html
sed -i "s/>Giorni l'anno<\/span>/>Giorni di Operativita<\/span>/" themes/flavour-pcgenzano/layouts/index.html

# ── 2. AGGIORNA MENU GESTIONE CON OPZIONE ALLERTE ──
echo "📋 Aggiornamento menu gestione sito..."
cat > ~/gestione-sito.sh << 'SCRIPTEOF'
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
  echo "  📰 CONTENUTI"
  echo "   1) Pubblica una nuova notizia"
  echo "   2) Pubblica notizia da file Word"
  echo "   3) Modifica una pagina del sito"
  echo ""
  echo "  🌦️ ALLERTA METEO"
  echo "   4) Modifica livello allerta"
  echo ""
  echo "  🔧 MANUTENZIONE"
  echo "   5) Testa il sito in locale"
  echo "   6) Pubblica modifiche manuali"
  echo "   7) Scarica aggiornamenti dal server"
  echo ""
  echo "  📊 INFO"
  echo "   8) Vedi ultime modifiche"
  echo "   9) Apri il sito online"
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
      cd ~/sito-pc-genzano
      git pull --rebase 2>/dev/null || git pull 2>/dev/null || true
      echo ""
      echo "  ============================================"
      echo "  🌦️ MODIFICA LIVELLO ALLERTA METEO"
      echo "  ============================================"
      echo ""
      echo "  Stato attuale:"
      echo "  ──────────────────────────────────────"
      if [ -f data/allerta.json ]; then
        CURRENT=$(python3 -c "import json; d=json.load(open('data/allerta.json')); print(f\"  Livello: {d['livello'].upper()}\n  Titolo: {d['titolo']}\n  Ultimo check: {d.get('ultimo_check','N/A')}\")" 2>/dev/null || echo "  (errore lettura)")
        echo "$CURRENT"
      fi
      echo "  ──────────────────────────────────────"
      echo ""
      echo "  Scegli il nuovo livello:"
      echo "  🟢 1) VERDE — Nessuna allerta"
      echo "  🟡 2) GIALLA — Criticita ordinaria"
      echo "  🟠 3) ARANCIONE — Criticita moderata"
      echo "  🔴 4) ROSSA — Criticita elevata"
      echo ""
      echo "   0) Annulla"
      echo ""
      echo -n "  Scegli: "
      read -r LIV

      case $LIV in
        1) LIVELLO="verde"; TITOLO="NESSUNA ALLERTA"; DESC="Non sono previsti fenomeni significativi sul nostro territorio." ;;
        2) LIVELLO="gialla"; TITOLO="ALLERTA GIALLA"; DESC="" ;;
        3) LIVELLO="arancione"; TITOLO="ALLERTA ARANCIONE"; DESC="" ;;
        4) LIVELLO="rossa"; TITOLO="ALLERTA ROSSA"; DESC="" ;;
        0) echo "  Annullato."; echo "Premi Invio..."; read -r; continue ;;
        *) echo "  ❌ Scelta non valida!"; echo "Premi Invio..."; read -r; continue ;;
      esac

      if [ "$LIVELLO" != "verde" ] && [ -z "$DESC" ]; then
        echo ""
        echo "  📝 Descrizione breve dell'allerta:"
        echo "  (es: Previste piogge intense e temporali dalle 14:00)"
        read -r DESC
        if [ -z "$DESC" ]; then
          case $LIVELLO in
            gialla) DESC="Criticita ordinaria. Possibili fenomeni localizzati di intensita moderata. Prestare attenzione." ;;
            arancione) DESC="Criticita moderata. Fenomeni diffusi e potenzialmente pericolosi. Limitare gli spostamenti." ;;
            rossa) DESC="Criticita elevata. Fenomeni molto intensi. Seguire le indicazioni delle autorita." ;;
          esac
        fi
      fi

      NOW=$(date "+%d/%m/%Y %H:%M")
      cat > data/allerta.json << JSONEOF
{
  "livello": "$LIVELLO",
  "titolo": "$TITOLO",
  "descrizione": "$DESC",
  "zona": "F - Bacini Costieri Sud / D - Bacini di Roma",
  "aggiornamento": "Aggiornamento manuale",
  "ultimo_check": "$NOW"
}
JSONEOF

      echo ""
      echo "  ✅ Allerta aggiornata a: $TITOLO"
      echo ""
      echo "  🚀 Pubblicare subito? (s/n)"
      read -r PUBBLICA
      if [ "$PUBBLICA" = "s" ] || [ "$PUBBLICA" = "S" ]; then
        git add -A
        git commit -m "🌦️ Allerta manuale: $TITOLO ($NOW)"
        git push
        echo "  ✅ Pubblicato! Online tra 2-3 minuti."
      fi
      echo "Premi Invio per tornare al menu..."
      read -r
      ;;
    5)
      echo ""
      echo "  🌐 Avvio server locale..."
      echo "  Apri http://localhost:1313/ nel browser"
      echo "  Premi Ctrl+C per fermare."
      echo ""
      cd ~/sito-pc-genzano && hugo server -D
      echo "Premi Invio per tornare al menu..."
      read -r
      ;;
    6)
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
    7)
      cd ~/sito-pc-genzano
      echo ""
      git pull --rebase 2>/dev/null || git pull
      echo "  ✅ Aggiornato!"
      echo "Premi Invio per tornare al menu..."
      read -r
      ;;
    8)
      cd ~/sito-pc-genzano
      echo ""
      echo "  📋 Ultime 10 modifiche:"
      echo "  ──────────────────────────────────────"
      git log --oneline -10
      echo "  ──────────────────────────────────────"
      echo "Premi Invio per tornare al menu..."
      read -r
      ;;
    9)
      xdg-open "https://sviluppoitaliadigitale.github.io/sito-pc-genzano/" 2>/dev/null || echo "  Apri: https://sviluppoitaliadigitale.github.io/sito-pc-genzano/"
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
SCRIPTEOF
chmod +x ~/gestione-sito.sh

# ── 3. WORKFLOW ALLERTE MIGLIORATO ──
echo "🌦️ Aggiornamento workflow allerte con DPC testo + API..."
cat > .github/workflows/check-allerta.yml << 'YAMLEOF'
name: "🌦️ Controlla Allerta Meteo"

on:
  schedule:
    # Ogni 6 ore: 02:00, 08:00, 14:00, 20:00 ora italiana
    - cron: '0 0,6,12,18 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  check-allerta:
    runs-on: ubuntu-latest
    steps:
      - name: "📥 Checkout"
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: "🌦️ Controlla allerta per Genzano di Roma"
        id: allerta
        run: |
          echo "🔍 Controllo allerte meteo per Genzano di Roma..."
          echo "   Fonti: DPC Bollettino Nazionale + API allertameteo.app"
          echo ""

          NOW=$(TZ="Europe/Rome" date "+%d/%m/%Y %H:%M")
          LIVELLO="verde"
          TITOLO="NESSUNA ALLERTA"
          DESC="Non sono previsti fenomeni significativi sul nostro territorio."
          FONTE=""

          # ── FONTE 1: API allertameteo.app (dati DPC per comune) ──
          echo "📡 Fonte 1: API allertameteo.app..."
          API_RESP=$(curl -sL --max-time 15 "https://allertameteo.app/api/alert/genzano-di-roma" 2>/dev/null || echo "")

          if echo "$API_RESP" | python3 -c "
          import sys, json
          try:
              data = json.load(sys.stdin)
              # Cerca il livello massimo tra oggi e domani
              max_level = 'verde'
              levels = {'verde':0, 'gialla':1, 'arancione':2, 'rossa':3}
              for day in ['oggi','domani','today','tomorrow']:
                  if day in data:
                      for risk_type in data[day]:
                          level = data[day][risk_type].get('level','') if isinstance(data[day][risk_type], dict) else str(data[day][risk_type])
                          level = level.lower().strip()
                          if level in levels and levels.get(level,0) > levels.get(max_level,0):
                              max_level = level
              print(max_level)
          except:
              print('errore')
          " 2>/dev/null | grep -qvE "errore|verde"; then
            API_LEVEL=$(echo "$API_RESP" | python3 -c "
          import sys, json
          try:
              data = json.load(sys.stdin)
              max_level = 'verde'
              levels = {'verde':0, 'gialla':1, 'arancione':2, 'rossa':3}
              for day in ['oggi','domani','today','tomorrow']:
                  if day in data:
                      for risk_type in data[day]:
                          level = data[day][risk_type].get('level','') if isinstance(data[day][risk_type], dict) else str(data[day][risk_type])
                          level = level.lower().strip()
                          if level in levels and levels.get(level,0) > levels.get(max_level,0):
                              max_level = level
              print(max_level)
          except:
              print('verde')
          " 2>/dev/null)
            if [ -n "$API_LEVEL" ] && [ "$API_LEVEL" != "verde" ]; then
              LIVELLO="$API_LEVEL"
              FONTE="allertameteo.app API"
              echo "   ⚠️ Trovata allerta $LIVELLO da API"
            else
              echo "   ✅ API: nessuna allerta"
            fi
          else
            echo "   ℹ️ API non disponibile o nessuna allerta"
          fi

          # ── FONTE 2: Pagina DPC bollettino testo ──
          echo "📡 Fonte 2: DPC bollettino nazionale (testo HTML)..."
          DPC_PAGE=$(curl -sL --max-time 15 "https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-criticita/" 2>/dev/null || echo "")

          if [ -n "$DPC_PAGE" ]; then
            # Cerca "Lazio" nel testo del bollettino
            LAZIO_SECTION=$(echo "$DPC_PAGE" | grep -i "lazio" || echo "")
            if [ -n "$LAZIO_SECTION" ]; then
              echo "   Trovata menzione Lazio nel bollettino"
              # Controlla i livelli nel contesto del Lazio
              # Il bollettino elenca le regioni sotto ogni livello di criticità
              if echo "$DPC_PAGE" | grep -B5 -i "lazio" | grep -qi "ELEVATA CRITICITA\|ALLERTA ROSSA"; then
                if [ "$(echo "rossa" | awk '{print length}')" -gt 0 ]; then
                  LIVELLO="rossa"
                  FONTE="DPC Bollettino Nazionale"
                fi
              elif echo "$DPC_PAGE" | grep -B5 -i "lazio" | grep -qi "MODERATA CRITICITA\|ALLERTA ARANCIONE"; then
                if [ "$LIVELLO" != "rossa" ]; then
                  LIVELLO="arancione"
                  FONTE="DPC Bollettino Nazionale"
                fi
              elif echo "$DPC_PAGE" | grep -B5 -i "lazio" | grep -qi "ORDINARIA CRITICITA\|ALLERTA GIALLA"; then
                if [ "$LIVELLO" = "verde" ]; then
                  LIVELLO="gialla"
                  FONTE="DPC Bollettino Nazionale"
                fi
              fi
            else
              echo "   ✅ DPC: nessuna menzione Lazio"
            fi
          else
            echo "   ⚠️ Pagina DPC non raggiungibile"
          fi

          # ── FONTE 3: Pagina Regione Lazio (fallback) ──
          echo "📡 Fonte 3: Regione Lazio (fallback)..."
          LAZIO_PAGE=$(curl -sL --max-time 15 "https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" 2>/dev/null || echo "")
          if [ -n "$LAZIO_PAGE" ]; then
            if echo "$LAZIO_PAGE" | grep -qi "rossa.*\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\)" || \
               echo "$LAZIO_PAGE" | grep -qi "\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\).*rossa"; then
              LIVELLO="rossa"; FONTE="Regione Lazio"
            elif echo "$LAZIO_PAGE" | grep -qi "arancione.*\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\)" || \
                 echo "$LAZIO_PAGE" | grep -qi "\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\).*arancione"; then
              if [ "$LIVELLO" != "rossa" ]; then LIVELLO="arancione"; FONTE="Regione Lazio"; fi
            elif echo "$LAZIO_PAGE" | grep -qi "gialla.*\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\|tutte le zone\)" || \
                 echo "$LAZIO_PAGE" | grep -qi "\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\|tutte le zone\).*gialla"; then
              if [ "$LIVELLO" = "verde" ]; then LIVELLO="gialla"; FONTE="Regione Lazio"; fi
            fi
          fi

          # Imposta titolo e descrizione
          case $LIVELLO in
            verde) TITOLO="NESSUNA ALLERTA"; DESC="Non sono previsti fenomeni significativi sul nostro territorio." ;;
            gialla) TITOLO="ALLERTA GIALLA"; DESC="Criticita ordinaria. Possibili fenomeni localizzati di intensita moderata. Prestare attenzione." ;;
            arancione) TITOLO="ALLERTA ARANCIONE"; DESC="Criticita moderata. Fenomeni diffusi e potenzialmente pericolosi. Limitare gli spostamenti." ;;
            rossa) TITOLO="ALLERTA ROSSA"; DESC="Criticita elevata. Fenomeni molto intensi. Seguire le indicazioni delle autorita." ;;
          esac

          echo ""
          echo "📊 RISULTATO: $TITOLO"
          [ -n "$FONTE" ] && echo "   Fonte: $FONTE"

          echo "livello=$LIVELLO" >> $GITHUB_OUTPUT
          echo "titolo=$TITOLO" >> $GITHUB_OUTPUT
          echo "desc=$DESC" >> $GITHUB_OUTPUT
          echo "now=$NOW" >> $GITHUB_OUTPUT
          echo "fonte=${FONTE:-controllo automatico}" >> $GITHUB_OUTPUT

      - name: "📝 Aggiorna file dati allerta"
        run: |
          cat > data/allerta.json << JSONEOF
          {
            "livello": "${{ steps.allerta.outputs.livello }}",
            "titolo": "${{ steps.allerta.outputs.titolo }}",
            "descrizione": "${{ steps.allerta.outputs.desc }}",
            "zona": "F - Bacini Costieri Sud / D - Bacini di Roma",
            "aggiornamento": "Fonte: ${{ steps.allerta.outputs.fonte }}",
            "ultimo_check": "${{ steps.allerta.outputs.now }}"
          }
          JSONEOF

      - name: "📤 Commit e Push se cambiato"
        run: |
          git config --local user.email "github-actions[bot]@users.noreply.github.com"
          git config --local user.name "GitHub Actions Bot"
          git add data/allerta.json
          if git diff --cached --quiet; then
            echo "✅ Nessuna modifica."
          else
            git commit -m "🌦️ Allerta: ${{ steps.allerta.outputs.titolo }} (${{ steps.allerta.outputs.now }})"
            git push
          fi

      - name: "📊 Riepilogo"
        if: always()
        run: |
          echo "## 🌦️ Controllo Allerta Meteo" >> $GITHUB_STEP_SUMMARY
          echo "| Info | Valore |" >> $GITHUB_STEP_SUMMARY
          echo "|---|---|" >> $GITHUB_STEP_SUMMARY
          echo "| Livello | **${{ steps.allerta.outputs.titolo }}** |" >> $GITHUB_STEP_SUMMARY
          echo "| Fonte | ${{ steps.allerta.outputs.fonte }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Zona | F + D (Genzano di Roma) |" >> $GITHUB_STEP_SUMMARY
          echo "| Controllo | ${{ steps.allerta.outputs.now }} |" >> $GITHUB_STEP_SUMMARY
YAMLEOF

# ── 4. COMMIT E PUSH ──
echo "📤 Pubblicazione..."
git add -A
git commit -m "🌦️ Fix stat labels + menu allerte + automazione DPC migliorata (3 fonti)"
git push

echo ""
echo "============================================"
echo "  ✅ AGGIORNAMENTO COMPLETATO!"
echo "============================================"
echo ""
echo "  STATISTICHE: etichette corrette"
echo ""
echo "  MENU (bash ~/gestione-sito.sh):"
echo "  Opzione 4 = Modifica livello allerta"
echo "  Ti chiede il colore e la descrizione,"
echo "  poi pubblica automaticamente."
echo ""
echo "  AUTOMAZIONE ALLERTE (3 fonti):"
echo "  1) allertameteo.app — API con dati DPC per comune"
echo "  2) mappe.protezionecivile.gov.it — bollettino testo"
echo "  3) protezionecivile.regione.lazio.it — fallback"
echo "  Controlla ogni 6 ore, usa il livello piu alto."
echo "============================================"
