#!/bin/bash
# ============================================================
# STRUMENTI DI PUBBLICAZIONE + FIX ALLERTE OGNI 6 ORE
# Esegui con: bash strumenti-pubblicazione.sh
# ============================================================

set -e
cd ~/sito-pc-genzano

echo "📥 Pull..."
git pull --rebase 2>/dev/null || git pull 2>/dev/null || true

# ── 1. SCRIPT INTERATTIVO PER NUOVI ARTICOLI ──
echo "📝 Creazione script pubblica-notizia..."
cat > ~/pubblica-notizia.sh << 'SCRIPTEOF'
#!/bin/bash
# ============================================================
# PUBBLICA NOTIZIA — Script Interattivo
# Uso: bash ~/pubblica-notizia.sh
# ============================================================

cd ~/sito-pc-genzano
git pull --rebase 2>/dev/null || git pull 2>/dev/null || true

echo ""
echo "============================================"
echo "  📰 PUBBLICA UNA NUOVA NOTIZIA"
echo "  Protezione Civile Genzano di Roma"
echo "============================================"
echo ""

# Data
DATA_OGGI=$(date +%Y-%m-%d)
echo "📅 Data di pubblicazione (premi Invio per oggi: $DATA_OGGI):"
read -r DATA_INPUT
DATA=${DATA_INPUT:-$DATA_OGGI}

# Titolo
echo ""
echo "📌 Titolo della notizia:"
read -r TITOLO
if [ -z "$TITOLO" ]; then
  echo "❌ Il titolo è obbligatorio!"
  exit 1
fi

# Categoria
echo ""
echo "🏷️ Categoria (scegli un numero):"
echo "  1) Allerta"
echo "  2) Avviso"
echo "  3) Evento"
echo "  4) Comunicazione"
read -r CAT_NUM
case $CAT_NUM in
  1) BADGE="Allerta" ;;
  2) BADGE="Avviso" ;;
  3) BADGE="Evento" ;;
  *) BADGE="Comunicazione" ;;
esac

# Descrizione breve
echo ""
echo "📝 Descrizione breve (1-2 righe, per l'anteprima):"
read -r DESCRIZIONE

# Testo completo
echo ""
echo "📄 Testo completo della notizia."
echo "   Puoi scrivere su più righe. Quando hai finito, scrivi FINE su una riga vuota."
echo "   Per andare a capo lascia una riga vuota (doppio Invio)."
echo "   ──────────────────────────────────────"
TESTO=""
while IFS= read -r LINEA; do
  if [ "$LINEA" = "FINE" ]; then
    break
  fi
  TESTO="$TESTO$LINEA
"
done

# Immagine
echo ""
echo "🖼️ Vuoi aggiungere una foto? (s/n)"
read -r FOTO_RISPOSTA
IMMAGINE_PATH=""
if [ "$FOTO_RISPOSTA" = "s" ] || [ "$FOTO_RISPOSTA" = "S" ]; then
  echo "   Trascina il file immagine nel terminale oppure scrivi il percorso completo:"
  read -r FOTO_INPUT
  # Rimuovi eventuali apici
  FOTO_INPUT=$(echo "$FOTO_INPUT" | tr -d "'\"")
  if [ -f "$FOTO_INPUT" ]; then
    # Crea nome file pulito
    ESTENSIONE="${FOTO_INPUT##*.}"
    NOME_FILE_SLUG=$(echo "$TITOLO" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
    NOME_IMMAGINE="${DATA}-${NOME_FILE_SLUG}.${ESTENSIONE}"
    # Copia nella cartella immagini
    mkdir -p static/images/notizie
    cp "$FOTO_INPUT" "static/images/notizie/$NOME_IMMAGINE"
    IMMAGINE_PATH="/images/notizie/$NOME_IMMAGINE"
    echo "   ✅ Foto copiata: $NOME_IMMAGINE"
  else
    echo "   ⚠️ File non trovato, continuo senza foto."
  fi
fi

# Genera slug dal titolo
SLUG=$(echo "$TITOLO" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | head -c 50)
FILENAME="content/comunicazioni/${DATA}-${SLUG}.md"

# Crea il file markdown
echo "---" > "$FILENAME"
echo "title: \"$TITOLO\"" >> "$FILENAME"
echo "date: $DATA" >> "$FILENAME"
echo "badge: \"$BADGE\"" >> "$FILENAME"
echo "description: \"$DESCRIZIONE\"" >> "$FILENAME"
if [ -n "$IMMAGINE_PATH" ]; then
  echo "image: \"$IMMAGINE_PATH\"" >> "$FILENAME"
fi
echo "---" >> "$FILENAME"
echo "" >> "$FILENAME"
echo "$TESTO" >> "$FILENAME"

echo ""
echo "📄 File creato: $FILENAME"
echo ""

# Anteprima
echo "──────────────────────────────────────"
echo "ANTEPRIMA:"
echo "──────────────────────────────────────"
cat "$FILENAME"
echo "──────────────────────────────────────"
echo ""

# Pubblicazione
echo "🚀 Vuoi pubblicare subito? (s/n)"
read -r PUBBLICA
if [ "$PUBBLICA" = "s" ] || [ "$PUBBLICA" = "S" ]; then
  git add -A
  git commit -m "📰 Nuova notizia: $TITOLO"
  git push
  echo ""
  echo "✅ NOTIZIA PUBBLICATA!"
  echo "   Sarà online tra 2-3 minuti su:"
  echo "   https://sviluppoitaliadigitale.github.io/sito-pc-genzano/comunicazioni/"
else
  echo ""
  echo "📋 Notizia salvata in locale. Per pubblicarla dopo:"
  echo "   cd ~/sito-pc-genzano"
  echo "   git add -A && git commit -m \"Nuova notizia\" && git push"
fi

echo ""
echo "============================================"
SCRIPTEOF
chmod +x ~/pubblica-notizia.sh

# ── 2. SCRIPT PER PUBBLICARE DA FILE WORD ──
echo "📄 Creazione script pubblica-da-word..."
cat > ~/pubblica-da-word.sh << 'SCRIPTEOF'
#!/bin/bash
# ============================================================
# PUBBLICA DA WORD — Converte .docx in notizia Hugo
# Uso: bash ~/pubblica-da-word.sh documento.docx
# ============================================================

# Verifica pandoc
if ! command -v pandoc &>/dev/null; then
  echo "📦 Installazione di pandoc (serve per convertire Word)..."
  sudo apt install pandoc -y
fi

if [ -z "$1" ]; then
  echo "❌ Uso: bash ~/pubblica-da-word.sh percorso/al/documento.docx"
  echo ""
  echo "   Esempio: bash ~/pubblica-da-word.sh ~/Scaricati/notizia.docx"
  exit 1
fi

DOCX="$1"
if [ ! -f "$DOCX" ]; then
  echo "❌ File non trovato: $DOCX"
  exit 1
fi

cd ~/sito-pc-genzano
git pull --rebase 2>/dev/null || git pull 2>/dev/null || true

DATA_OGGI=$(date +%Y-%m-%d)

# Estrai il testo dal Word
echo "📄 Conversione del documento Word..."
MARKDOWN=$(pandoc "$DOCX" -t markdown --wrap=none 2>/dev/null)

# Estrai il titolo (prima riga che inizia con #, oppure la prima riga)
TITOLO=$(echo "$MARKDOWN" | grep -m1 '^#' | sed 's/^#\+\s*//')
if [ -z "$TITOLO" ]; then
  TITOLO=$(echo "$MARKDOWN" | head -1)
fi

echo ""
echo "📌 Titolo trovato: $TITOLO"
echo "   Premi Invio per confermare o scrivi un titolo diverso:"
read -r TITOLO_INPUT
TITOLO=${TITOLO_INPUT:-$TITOLO}

# Categoria
echo ""
echo "🏷️ Categoria: 1) Allerta  2) Avviso  3) Evento  4) Comunicazione"
read -r CAT_NUM
case $CAT_NUM in
  1) BADGE="Allerta" ;;
  2) BADGE="Avviso" ;;
  3) BADGE="Evento" ;;
  *) BADGE="Comunicazione" ;;
esac

# Descrizione
DESCRIZIONE=$(echo "$MARKDOWN" | grep -v '^#' | head -3 | tr '\n' ' ' | head -c 150)
echo ""
echo "📝 Descrizione breve (Invio per usare questa):"
echo "   $DESCRIZIONE"
read -r DESC_INPUT
DESCRIZIONE=${DESC_INPUT:-$DESCRIZIONE}

# Estrai immagini dal Word
echo ""
echo "🖼️ Estrazione immagini dal documento..."
mkdir -p /tmp/word-images
mkdir -p static/images/notizie
pandoc "$DOCX" -t markdown --extract-media=/tmp/word-images --wrap=none > /dev/null 2>&1

SLUG=$(echo "$TITOLO" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | head -c 50)
IMMAGINE_PATH=""

# Copia le immagini trovate
IMG_COUNT=0
for IMG in /tmp/word-images/media/*; do
  if [ -f "$IMG" ]; then
    ESTENSIONE="${IMG##*.}"
    NOME_IMG="${DATA_OGGI}-${SLUG}-${IMG_COUNT}.${ESTENSIONE}"
    cp "$IMG" "static/images/notizie/$NOME_IMG"
    if [ $IMG_COUNT -eq 0 ]; then
      IMMAGINE_PATH="/images/notizie/$NOME_IMG"
    fi
    IMG_COUNT=$((IMG_COUNT + 1))
    echo "   ✅ Immagine copiata: $NOME_IMG"
  fi
done

if [ $IMG_COUNT -eq 0 ]; then
  echo "   Nessuna immagine trovata nel documento."
fi

# Rimuovi il titolo dal contenuto (già nel front matter)
CONTENUTO=$(echo "$MARKDOWN" | sed '1{/^#/d}')

# Crea il file
FILENAME="content/comunicazioni/${DATA_OGGI}-${SLUG}.md"
echo "---" > "$FILENAME"
echo "title: \"$TITOLO\"" >> "$FILENAME"
echo "date: $DATA_OGGI" >> "$FILENAME"
echo "badge: \"$BADGE\"" >> "$FILENAME"
echo "description: \"$DESCRIZIONE\"" >> "$FILENAME"
if [ -n "$IMMAGINE_PATH" ]; then
  echo "image: \"$IMMAGINE_PATH\"" >> "$FILENAME"
fi
echo "---" >> "$FILENAME"
echo "" >> "$FILENAME"
echo "$CONTENUTO" >> "$FILENAME"

# Pulizia
rm -rf /tmp/word-images

echo ""
echo "📄 File creato: $FILENAME"
echo ""
echo "🚀 Vuoi pubblicare subito? (s/n)"
read -r PUBBLICA
if [ "$PUBBLICA" = "s" ] || [ "$PUBBLICA" = "S" ]; then
  git add -A
  git commit -m "📰 Nuova notizia da Word: $TITOLO"
  git push
  echo "✅ PUBBLICATA! Online tra 2-3 minuti."
else
  echo "📋 Salvata in locale."
fi

echo ""
SCRIPTEOF
chmod +x ~/pubblica-da-word.sh

# ── 3. GUIDA RAPIDA PUBBLICAZIONE DA GITHUB.COM ──
echo "📖 Creazione guida pubblicazione da browser..."
cat > ~/GUIDA-PUBBLICAZIONE.txt << 'GUIDEEOF'
============================================================
 GUIDA RAPIDA — Come pubblicare notizie
 Protezione Civile Genzano di Roma
============================================================

HAI 3 MODI PER PUBBLICARE UNA NOTIZIA:

────────────────────────────────────────
METODO 1: SCRIPT INTERATTIVO (dal PC)
────────────────────────────────────────
Apri il terminale e scrivi:

  bash ~/pubblica-notizia.sh

Lo script ti chiederà:
  - Data (o usa quella di oggi)
  - Titolo
  - Categoria (Allerta/Avviso/Evento/Comunicazione)
  - Descrizione breve
  - Testo completo (scrivi FINE quando hai finito)
  - Se vuoi aggiungere una foto
  - Se vuoi pubblicare subito

────────────────────────────────────────
METODO 2: DA FILE WORD (dal PC)
────────────────────────────────────────
1. Scrivi la notizia in Word/LibreOffice Writer
2. Il TITOLO deve essere la prima riga (in grassetto o come Titolo)
3. Inserisci le immagini nel documento
4. Salva come .docx
5. Apri il terminale e scrivi:

  bash ~/pubblica-da-word.sh ~/Scaricati/nome-file.docx

Lo script:
  - Converte il Word in Markdown
  - Estrae le immagini automaticamente
  - Ti chiede conferma del titolo e della categoria
  - Pubblica tutto

────────────────────────────────────────
METODO 3: DA GITHUB.COM (da qualsiasi dispositivo)
────────────────────────────────────────
1. Vai su: https://github.com/SviluppoItaliaDigitale/sito-pc-genzano
2. Clicca sulla cartella "content" > "comunicazioni"
3. Clicca "Add file" > "Create new file"
4. Come nome file scrivi: AAAA-MM-GG-titolo-notizia.md
   (es: 2026-03-27-esercitazione-primavera.md)
5. Nel contenuto scrivi:

---
title: "Titolo della notizia"
date: 2026-03-27
badge: "Comunicazione"
description: "Breve descrizione."
---

Testo della notizia qui.

Puoi usare **grassetto** e *corsivo*.

6. Clicca "Commit changes" > "Commit changes"
7. Il sito si aggiorna da solo in 2-3 minuti!

────────────────────────────────────────
COME AGGIUNGERE UNA FOTO PERSONALIZZATA
────────────────────────────────────────
Se non metti una foto, viene usata l'immagine di default blu.
Per aggiungere una foto personalizzata:

1. Copia la foto in: ~/sito-pc-genzano/static/images/notizie/
2. Nel front matter della notizia aggiungi:
   image: "/images/notizie/nome-foto.jpg"

Oppure usa lo script pubblica-notizia.sh che lo fa automaticamente!

────────────────────────────────────────
COMANDI UTILI DA RICORDARE
────────────────────────────────────────
  bash ~/pubblica-notizia.sh     → Pubblica notizia interattiva
  bash ~/pubblica-da-word.sh X   → Pubblica da file Word
  cd ~/sito-pc-genzano           → Vai alla cartella del sito
  hugo server                    → Testa il sito in locale
  git add -A && git commit -m "msg" && git push  → Pubblica manualmente

============================================================
GUIDEEOF

# ── 4. AGGIORNAMENTO ALLERTE OGNI 6 ORE ──
echo "🌦️ Aggiornamento workflow allerte a ogni 6 ore..."
cat > .github/workflows/check-allerta.yml << 'YAMLEOF'
name: "🌦️ Controlla Allerta Meteo"

on:
  schedule:
    # Ogni 6 ore: 00:00, 06:00, 12:00, 18:00 UTC
    # Corrispondono a: 02:00, 08:00, 14:00, 20:00 ora italiana (CEST)
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

      - name: "🌦️ Controlla bollettino Regione Lazio"
        id: allerta
        run: |
          echo "🔍 Scaricamento bollettini..."
          PAGE=$(curl -sL "https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" 2>/dev/null || echo "")
          PAGE2=$(curl -sL "https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini/criticita-idrogeologica-idraulica" 2>/dev/null || echo "")
          DPC=$(curl -sL "https://www.protezionecivile.gov.it/it/bollettino-di-criticita" 2>/dev/null || echo "")
          COMBINED="$PAGE $PAGE2 $DPC"
          NOW=$(TZ="Europe/Rome" date "+%d/%m/%Y %H:%M")
          LIVELLO="verde"
          TITOLO="NESSUNA ALLERTA"
          DESC="Non sono previsti fenomeni significativi sul nostro territorio."
          if echo "$COMBINED" | grep -qi "rossa.*\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\)" || \
             echo "$COMBINED" | grep -qi "\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\).*rossa"; then
            LIVELLO="rossa"
            TITOLO="ALLERTA ROSSA"
            DESC="Criticità elevata. Fenomeni molto intensi con elevata probabilità di danni gravi. Seguire le indicazioni delle autorità."
          elif echo "$COMBINED" | grep -qi "arancione.*\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\)" || \
               echo "$COMBINED" | grep -qi "\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\).*arancione"; then
            LIVELLO="arancione"
            TITOLO="ALLERTA ARANCIONE"
            DESC="Criticità moderata. Fenomeni diffusi e potenzialmente pericolosi. Limitare gli spostamenti."
          elif echo "$COMBINED" | grep -qi "gialla.*\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\|tutte le zone\)" || \
               echo "$COMBINED" | grep -qi "\(zona.*[DF]\|bacini.*costieri.*sud\|bacini.*roma\|tutte le zone\).*gialla" || \
               echo "$COMBINED" | grep -qi "allerta gialla.*lazio"; then
            LIVELLO="gialla"
            TITOLO="ALLERTA GIALLA"
            DESC="Criticità ordinaria. Possibili fenomeni localizzati di intensità moderata. Prestare attenzione."
          fi
          echo "📊 Risultato: $TITOLO"
          echo "livello=$LIVELLO" >> $GITHUB_OUTPUT
          echo "titolo=$TITOLO" >> $GITHUB_OUTPUT
          echo "desc=$DESC" >> $GITHUB_OUTPUT
          echo "now=$NOW" >> $GITHUB_OUTPUT

      - name: "📝 Aggiorna file dati allerta"
        run: |
          cat > data/allerta.json << JSONEOF
          {
            "livello": "${{ steps.allerta.outputs.livello }}",
            "titolo": "${{ steps.allerta.outputs.titolo }}",
            "descrizione": "${{ steps.allerta.outputs.desc }}",
            "zona": "F - Bacini Costieri Sud / D - Bacini di Roma",
            "aggiornamento": "Controllo automatico ogni 6 ore",
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
          echo "| Zona | F + D (Genzano di Roma) |" >> $GITHUB_STEP_SUMMARY
          echo "| Controllo | ${{ steps.allerta.outputs.now }} |" >> $GITHUB_STEP_SUMMARY
          echo "| Prossimo | Tra 6 ore |" >> $GITHUB_STEP_SUMMARY
YAMLEOF

# ── 5. CARTELLA PER FOTO NOTIZIE ──
mkdir -p static/images/notizie

# ── 6. COMMIT E PUSH ──
echo ""
echo "📤 Salvataggio e pubblicazione..."
git add -A
git commit -m "📰 Strumenti pubblicazione notizie + allerte ogni 6 ore"
git push

echo ""
echo "============================================"
echo "  ✅ TUTTO INSTALLATO!"
echo "============================================"
echo ""
echo "  📰 PUBBLICARE UNA NOTIZIA:"
echo "     bash ~/pubblica-notizia.sh"
echo ""
echo "  📄 PUBBLICARE DA FILE WORD:"
echo "     bash ~/pubblica-da-word.sh ~/Scaricati/notizia.docx"
echo ""
echo "  📖 GUIDA COMPLETA:"
echo "     cat ~/GUIDA-PUBBLICAZIONE.txt"
echo ""
echo "  🌦️ ALLERTE: ora controllate ogni 6 ore"
echo "     (02:00, 08:00, 14:00, 20:00 ora italiana)"
echo "============================================"
