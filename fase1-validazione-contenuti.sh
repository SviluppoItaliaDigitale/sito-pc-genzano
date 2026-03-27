#!/bin/bash
# ============================================================
# FASE 1: Tool Validazione Contenuti + Checklist Designers Italia
# Esegui con: bash fase1-validazione-contenuti.sh
# ============================================================

set -e
cd ~/sito-pc-genzano

echo "📥 Pull..."
git pull --rebase 2>/dev/null || git pull 2>/dev/null || true

# ── 1. SCRIPT DI VALIDAZIONE CONTENUTI ──
echo "✅ Creazione validatore contenuti Designers Italia..."
cat > ~/valida-contenuto.sh << 'SCRIPTEOF'
#!/bin/bash
# ============================================================
# VALIDATORE CONTENUTI — Linee Guida Designers Italia
# Uso: bash ~/valida-contenuto.sh [file.md]
#      oppure: echo "testo" | bash ~/valida-contenuto.sh
#
# Controlla: linguaggio semplice, frasi corte, forme passive,
# termini burocratici, titoli, formattazione, accessibilità.
# ============================================================

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
BOLD='\033[1m'

ERRORI=0
AVVISI=0

errore() { echo -e "  ${RED}✗ ERRORE:${NC} $1"; ERRORI=$((ERRORI+1)); }
avviso() { echo -e "  ${YELLOW}⚠ AVVISO:${NC} $1"; AVVISI=$((AVVISI+1)); }
ok() { echo -e "  ${GREEN}✓${NC} $1"; }

echo ""
echo -e "${BOLD}============================================${NC}"
echo -e "${BOLD}  ✅ VALIDATORE CONTENUTI${NC}"
echo -e "${BOLD}  Linee Guida Designers Italia${NC}"
echo -e "${BOLD}============================================${NC}"
echo ""

# Leggi il testo
if [ -n "$1" ] && [ -f "$1" ]; then
  TESTO=$(cat "$1")
  echo -e "${BLUE}📄 Analisi file: $1${NC}"
elif [ ! -t 0 ]; then
  TESTO=$(cat)
  echo -e "${BLUE}📄 Analisi testo da input${NC}"
else
  echo "Uso: bash ~/valida-contenuto.sh file.md"
  echo "     echo 'testo' | bash ~/valida-contenuto.sh"
  exit 1
fi

# Separa front matter dal contenuto
CONTENUTO=$(echo "$TESTO" | sed -n '/^---$/,/^---$/!p' | sed '1{/^$/d}')
FRONT_MATTER=$(echo "$TESTO" | sed -n '/^---$/,/^---$/p')

echo ""
echo -e "${BOLD}── 1. STRUTTURA ──${NC}"

# Controlla titolo
TITOLO=$(echo "$FRONT_MATTER" | grep '^title:' | sed 's/title: *"\?\([^"]*\)"\?/\1/')
if [ -z "$TITOLO" ]; then
  errore "Titolo mancante nel front matter"
else
  TITOLO_LEN=${#TITOLO}
  if [ $TITOLO_LEN -gt 70 ]; then
    avviso "Titolo troppo lungo ($TITOLO_LEN car.). Max consigliato: 70 caratteri"
  elif [ $TITOLO_LEN -lt 10 ]; then
    avviso "Titolo troppo corto ($TITOLO_LEN car.). Sii piu descrittivo"
  else
    ok "Titolo OK ($TITOLO_LEN caratteri)"
  fi
fi

# Controlla descrizione
DESC=$(echo "$FRONT_MATTER" | grep '^description:' | sed 's/description: *"\?\([^"]*\)"\?/\1/')
if [ -z "$DESC" ]; then
  errore "Descrizione mancante. Aggiungi 'description:' nel front matter (max 160 car.)"
else
  DESC_LEN=${#DESC}
  if [ $DESC_LEN -gt 160 ]; then
    avviso "Descrizione troppo lunga ($DESC_LEN car.). Max consigliato: 160 caratteri per SEO"
  elif [ $DESC_LEN -lt 30 ]; then
    avviso "Descrizione troppo corta ($DESC_LEN car.). Sii piu informativo"
  else
    ok "Descrizione OK ($DESC_LEN caratteri)"
  fi
fi

# Controlla data
DATA=$(echo "$FRONT_MATTER" | grep '^date:' | sed 's/date: *//')
if [ -z "$DATA" ]; then
  errore "Data mancante nel front matter"
else
  ok "Data presente: $DATA"
fi

# Controlla badge
BADGE=$(echo "$FRONT_MATTER" | grep '^badge:' | sed 's/badge: *"\?\([^"]*\)"\?/\1/')
if [ -z "$BADGE" ]; then
  avviso "Badge/categoria mancante. Aggiungi: badge: \"Comunicazione\""
else
  ok "Categoria: $BADGE"
fi

echo ""
echo -e "${BOLD}── 2. LINGUAGGIO SEMPLICE ──${NC}"

# Controlla lunghezza frasi (max 25 parole)
FRASI_LUNGHE=0
while IFS= read -r FRASE; do
  # Salta righe vuote, intestazioni, link, HTML
  [ -z "$FRASE" ] && continue
  echo "$FRASE" | grep -qE '^#|^\-|^\*|^<|^\|' && continue
  PAROLE=$(echo "$FRASE" | wc -w)
  if [ "$PAROLE" -gt 25 ]; then
    FRASI_LUNGHE=$((FRASI_LUNGHE+1))
    if [ $FRASI_LUNGHE -le 3 ]; then
      avviso "Frase troppo lunga ($PAROLE parole): \"$(echo "$FRASE" | head -c 80)...\""
    fi
  fi
done <<< "$(echo "$CONTENUTO" | tr '.' '\n' | tr '!' '\n' | tr '?' '\n')"
if [ $FRASI_LUNGHE -gt 3 ]; then
  avviso "...e altre $((FRASI_LUNGHE-3)) frasi troppo lunghe (max 25 parole per frase)"
elif [ $FRASI_LUNGHE -eq 0 ]; then
  ok "Tutte le frasi hanno lunghezza adeguata"
fi

# Controlla forme passive
PASSIVE=$(echo "$CONTENUTO" | grep -oiE "(è stato|è stata|sono stati|sono state|viene effettuato|viene effettuata|vengono effettuati|vengono effettuate|verrà effettuato|sarà effettuato|è previsto che|si comunica che|si informa che|si avvisa che|si rende noto)" | wc -l)
if [ "$PASSIVE" -gt 0 ]; then
  avviso "Trovate $PASSIVE forme passive. Preferisci la forma attiva:"
  echo "$CONTENUTO" | grep -oiE "(è stato|è stata|sono stati|sono state|viene effettuato|viene effettuata|vengono effettuati|si comunica che|si informa che|si avvisa che)" | head -3 | while read -r P; do
    echo -e "    → \"$P\" → usa la forma attiva"
  done
else
  ok "Nessuna forma passiva problematica trovata"
fi

echo ""
echo -e "${BOLD}── 3. TERMINI BUROCRATICI ──${NC}"

# Lista termini burocratici da evitare (Guida al linguaggio PA)
BUROCRATICI=(
  "espletamento:completamento"
  "a tal fine:per questo"
  "di cui sopra:gia citato"
  "in ottemperanza:secondo"
  "ivi compreso:incluso"
  "all'uopo:per questo"
  "onde evitare:per evitare"
  "laddove:dove/quando"
  "qualora:se"
  "nonche:e anche"
  "codesto:questo"
  "siffatto:questo/tale"
  "altresì:anche/inoltre"
  "precipuo:principale"
  "porre in essere:fare/attuare"
  "dar luogo:causare/creare"
  "con la presente:con questa comunicazione"
  "in calce:in fondo"
  "in seno a:dentro/in"
  "per il tramite di:tramite/attraverso"
  "giusta:secondo (es. giusta delibera)"
  "atteso che:considerato che"
  "nelle more di:in attesa di"
)

BURO_TROVATI=0
for ENTRY in "${BUROCRATICI[@]}"; do
  TERMINE="${ENTRY%%:*}"
  ALTERNATIVA="${ENTRY##*:}"
  COUNT=$(echo "$CONTENUTO" | grep -oci "$TERMINE" || true)
  if [ "$COUNT" -gt 0 ]; then
    avviso "\"$TERMINE\" trovato $COUNT volta/e → usa: \"$ALTERNATIVA\""
    BURO_TROVATI=$((BURO_TROVATI+1))
  fi
done
if [ $BURO_TROVATI -eq 0 ]; then
  ok "Nessun termine burocratico trovato"
fi

echo ""
echo -e "${BOLD}── 4. FORMATTAZIONE ──${NC}"

# Controlla uso eccessivo di maiuscole
MAIUSC=$(echo "$CONTENUTO" | grep -oE '\b[A-Z]{4,}\b' | grep -v '^[A-Z]\{2,4\}$' | wc -l)
if [ "$MAIUSC" -gt 3 ]; then
  avviso "Trovate $MAIUSC parole TUTTE IN MAIUSCOLO. Usa il maiuscolo con moderazione"
else
  ok "Uso del maiuscolo adeguato"
fi

# Controlla lunghezza complessiva
PAROLE_TOTALI=$(echo "$CONTENUTO" | wc -w)
if [ "$PAROLE_TOTALI" -lt 30 ]; then
  avviso "Contenuto molto breve ($PAROLE_TOTALI parole). Valuta se aggiungere informazioni"
elif [ "$PAROLE_TOTALI" -gt 800 ]; then
  avviso "Contenuto lungo ($PAROLE_TOTALI parole). Valuta se spezzare in piu pagine"
else
  ok "Lunghezza contenuto adeguata ($PAROLE_TOTALI parole)"
fi

# Controlla presenza di intestazioni (struttura)
H2_COUNT=$(echo "$CONTENUTO" | grep -c '^## ' || true)
if [ "$PAROLE_TOTALI" -gt 200 ] && [ "$H2_COUNT" -eq 0 ]; then
  avviso "Contenuto lungo senza intestazioni. Usa ## per strutturare il testo"
else
  ok "Struttura del testo OK"
fi

echo ""
echo -e "${BOLD}── 5. ACCESSIBILITA E INCLUSIONE ──${NC}"

# Controlla link generici ("clicca qui", "leggi tutto")
LINK_GENERICI=$(echo "$CONTENUTO" | grep -oiE "\[clicca qui\]|\[leggi tutto\]|\[qui\]|\[link\]|\[apri\]" | wc -l)
if [ "$LINK_GENERICI" -gt 0 ]; then
  errore "Trovati $LINK_GENERICI link con testo generico (\"clicca qui\", \"leggi tutto\"). Usa testi descrittivi"
else
  ok "Link con testi descrittivi"
fi

# Controlla immagini senza alt (in markdown)
IMG_NO_ALT=$(echo "$CONTENUTO" | grep -oE '!\[\]' | wc -l)
if [ "$IMG_NO_ALT" -gt 0 ]; then
  errore "Trovate $IMG_NO_ALT immagini senza testo alternativo. Aggiungi descrizione in ![descrizione](url)"
else
  ok "Immagini con testo alternativo (o nessuna immagine)"
fi

# Controlla linguaggio non inclusivo
NON_INCLUSIVO=$(echo "$CONTENUTO" | grep -oiE "(il cittadino deve|l'utente deve|handicappato|portatore di handicap|invalido|diversamente abile)" | wc -l)
if [ "$NON_INCLUSIVO" -gt 0 ]; then
  avviso "Trovato linguaggio non inclusivo. Preferisci: \"le persone\", \"chi utilizza il servizio\", \"persona con disabilita\""
else
  ok "Linguaggio inclusivo OK"
fi

# ── RIEPILOGO ──
echo ""
echo -e "${BOLD}============================================${NC}"
if [ $ERRORI -eq 0 ] && [ $AVVISI -eq 0 ]; then
  echo -e "${GREEN}${BOLD}  ✅ CONTENUTO PERFETTO!${NC}"
  echo -e "${GREEN}  Conforme alle Linee Guida Designers Italia${NC}"
elif [ $ERRORI -eq 0 ]; then
  echo -e "${YELLOW}${BOLD}  ⚠ $AVVISI avvisi — Contenuto pubblicabile${NC}"
  echo -e "${YELLOW}  Valuta le migliorie suggerite sopra${NC}"
else
  echo -e "${RED}${BOLD}  ✗ $ERRORI errori + $AVVISI avvisi${NC}"
  echo -e "${RED}  Correggi gli errori prima di pubblicare${NC}"
fi
echo -e "${BOLD}============================================${NC}"
echo ""

# Ritorna codice di uscita
if [ $ERRORI -gt 0 ]; then
  exit 1
else
  exit 0
fi
SCRIPTEOF
chmod +x ~/valida-contenuto.sh

# ── 2. AGGIORNA SCRIPT PUBBLICA NOTIZIA CON VALIDAZIONE ──
echo "📰 Aggiornamento script pubblica-notizia con validazione..."
cat > ~/pubblica-notizia.sh << 'SCRIPTEOF'
#!/bin/bash
# ============================================================
# PUBBLICA NOTIZIA — con Validazione Designers Italia
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
echo "  💡 RICORDA le regole di scrittura:"
echo "  • Frasi brevi (max 25 parole)"
echo "  • Linguaggio semplice e diretto"
echo "  • Forma attiva (non 'è stato fatto' ma 'abbiamo fatto')"
echo "  • Evita termini burocratici"
echo ""

# Data
DATA_OGGI=$(date +%Y-%m-%d)
echo "📅 Data di pubblicazione (Invio per oggi: $DATA_OGGI):"
read -r DATA_INPUT
DATA=${DATA_INPUT:-$DATA_OGGI}

# Titolo
echo ""
echo "📌 Titolo della notizia (max 70 caratteri, chiaro e descrittivo):"
read -r TITOLO
if [ -z "$TITOLO" ]; then
  echo "❌ Il titolo è obbligatorio!"
  exit 1
fi
T_LEN=${#TITOLO}
if [ $T_LEN -gt 70 ]; then
  echo "  ⚠️ Titolo lungo ($T_LEN car.). Consigliato: max 70"
fi

# Categoria
echo ""
echo "🏷️ Categoria:"
echo "  1) Allerta       (emergenze, allerte meteo)"
echo "  2) Avviso        (avvisi importanti, scadenze)"
echo "  3) Evento        (manifestazioni, INR, campagne)"
echo "  4) Comunicazione (notizie generiche, formazione)"
read -r CAT_NUM
case $CAT_NUM in
  1) BADGE="Allerta" ;;
  2) BADGE="Avviso" ;;
  3) BADGE="Evento" ;;
  *) BADGE="Comunicazione" ;;
esac

# Descrizione breve
echo ""
echo "📝 Descrizione breve per l'anteprima (max 160 caratteri):"
echo "   Questa frase appare nelle card della home e nei motori di ricerca."
read -r DESCRIZIONE
D_LEN=${#DESCRIZIONE}
if [ $D_LEN -gt 160 ]; then
  echo "  ⚠️ Descrizione lunga ($D_LEN car.). Consigliato: max 160"
fi

# Testo completo
echo ""
echo "📄 Testo completo della notizia."
echo "   💡 Consigli Designers Italia:"
echo "   • Vai dritto al punto: la cosa piu importante prima"
echo "   • Una frase = un concetto"
echo "   • Usa ## per le intestazioni se il testo e lungo"
echo "   • Scrivi FINE su una riga vuota quando hai finito"
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
  echo "   Trascina il file immagine o scrivi il percorso:"
  read -r FOTO_INPUT
  FOTO_INPUT=$(echo "$FOTO_INPUT" | tr -d "'\"")
  if [ -f "$FOTO_INPUT" ]; then
    ESTENSIONE="${FOTO_INPUT##*.}"
    NOME_FILE_SLUG=$(echo "$TITOLO" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
    NOME_IMMAGINE="${DATA}-${NOME_FILE_SLUG}.${ESTENSIONE}"
    mkdir -p static/images/notizie
    cp "$FOTO_INPUT" "static/images/notizie/$NOME_IMMAGINE"
    IMMAGINE_PATH="/images/notizie/$NOME_IMMAGINE"
    echo "   ✅ Foto copiata: $NOME_IMMAGINE"
  else
    echo "   ⚠️ File non trovato, continuo senza foto."
  fi
fi

# Genera file
SLUG=$(echo "$TITOLO" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | head -c 50)
FILENAME="content/comunicazioni/${DATA}-${SLUG}.md"

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

# ── VALIDAZIONE AUTOMATICA ──
echo ""
echo "──────────────────────────────────────"
echo "  🔍 VALIDAZIONE CONTENUTO..."
echo "──────────────────────────────────────"
bash ~/valida-contenuto.sh "$FILENAME"
VALID_RESULT=$?

if [ $VALID_RESULT -ne 0 ]; then
  echo ""
  echo "  ⚠️ Ci sono errori da correggere."
  echo "  Vuoi modificare il file prima di pubblicare? (s/n)"
  read -r MODIFICA
  if [ "$MODIFICA" = "s" ] || [ "$MODIFICA" = "S" ]; then
    nano "$FILENAME"
    echo ""
    echo "  🔍 Ri-validazione..."
    bash ~/valida-contenuto.sh "$FILENAME"
  fi
fi

echo ""
echo "🚀 Vuoi pubblicare? (s/n)"
read -r PUBBLICA
if [ "$PUBBLICA" = "s" ] || [ "$PUBBLICA" = "S" ]; then
  git add -A
  git commit -m "📰 Nuova notizia: $TITOLO"
  git push
  echo ""
  echo "  ✅ NOTIZIA PUBBLICATA!"
  echo "  Online tra 2-3 minuti su:"
  echo "  https://sviluppoitaliadigitale.github.io/sito-pc-genzano/comunicazioni/"
else
  echo "  📋 Salvata in locale: $FILENAME"
fi
echo ""
SCRIPTEOF
chmod +x ~/pubblica-notizia.sh

# ── 3. CHECKLIST STAMPABILE ──
echo "📋 Creazione checklist Designers Italia..."
cat > ~/CHECKLIST-CONTENUTI.txt << 'CHECKEOF'
============================================================
 CHECKLIST CONTENUTI — Linee Guida Designers Italia
 Protezione Civile Genzano di Roma
============================================================

Prima di pubblicare qualsiasi contenuto, verifica questi punti.
Puoi anche usare il validatore automatico:
  bash ~/valida-contenuto.sh content/comunicazioni/nome-file.md

════════════════════════════════════════════════════════════

📌 TITOLO
  □ Chiaro e descrittivo (non generico)
  □ Max 70 caratteri
  □ Contiene le parole chiave principali
  □ Non usa maiuscole eccessive
  ✗ NO: "Comunicazione importante"
  ✓ SI: "Campagna antincendio 2025: turni e numeri utili"

📝 DESCRIZIONE (per anteprima e motori di ricerca)
  □ Max 160 caratteri
  □ Riassume il contenuto principale
  □ Contiene le informazioni essenziali
  ✗ NO: "Leggi la notizia"
  ✓ SI: "Dal 15 giugno parte la campagna AIB. Ecco i numeri da chiamare."

✍️ TESTO — LINGUAGGIO SEMPLICE
  □ Frasi brevi: max 25 parole per frase
  □ Un concetto per frase
  □ Forma attiva: "Abbiamo attivato" non "È stato attivato"
  □ Parole semplici: "fare" non "espletare"
  □ Vai dritto al punto: informazione principale nella prima frase
  □ Evita acronimi non spiegati (almeno la prima volta)

🚫 TERMINI DA EVITARE → ALTERNATIVA
  espletamento → completamento
  a tal fine → per questo
  di cui sopra → gia citato
  in ottemperanza → secondo
  onde evitare → per evitare
  qualora → se
  altresì → anche
  nonché → e anche
  porre in essere → fare, attuare
  nelle more di → in attesa di
  con la presente → con questa comunicazione
  si comunica che → [inizia direttamente con il contenuto]
  si informa che → [inizia direttamente con il contenuto]

📐 STRUTTURA
  □ Informazione piu importante in cima (piramide rovesciata)
  □ Usa intestazioni (## Titolo) per testi oltre 200 parole
  □ Usa elenchi puntati per liste di 3+ elementi
  □ Paragrafi brevi (max 3-4 frasi)

♿ ACCESSIBILITA
  □ Link con testo descrittivo (no "clicca qui")
  □ Immagini con testo alternativo
  □ Non usare solo il colore per trasmettere informazioni
  □ Linguaggio inclusivo ("le persone" non "il cittadino")

📅 FORMATTAZIONE (standard Designers Italia)
  □ Date: 15 giugno 2025 (giorno in cifre, mese in lettere)
  □ Orari: 14:00 (con due punti, senza spazi)
  □ Telefoni: +39 06 936 2600 (con prefisso e spazi)
  □ Numeri: usa le cifre per dati precisi
  □ Maiuscole: solo per nomi propri e inizio frase

🔄 PRIMA DI PUBBLICARE
  □ Rileggi tutto ad alta voce
  □ Chiedi: "Un cittadino capirebbe al primo colpo?"
  □ Esegui il validatore: bash ~/valida-contenuto.sh file.md
  □ Se il testo e complesso, incollalo nella chat con Claude
     per una revisione completa secondo le linee guida

============================================================
CHECKEOF

# ── 4. COMMIT ──
echo "📤 Pubblicazione..."
git add -A
git commit -m "✅ Fase 1: validatore contenuti Designers Italia + checklist + pubblica-notizia aggiornato"
git push

echo ""
echo "============================================"
echo "  ✅ FASE 1 COMPLETATA!"
echo "============================================"
echo ""
echo "  NUOVI STRUMENTI:"
echo ""
echo "  📋 Validatore contenuti:"
echo "     bash ~/valida-contenuto.sh file.md"
echo ""
echo "  📰 Pubblica notizia (ora con validazione):"
echo "     bash ~/pubblica-notizia.sh"
echo ""
echo "  📖 Checklist stampabile:"
echo "     cat ~/CHECKLIST-CONTENUTI.txt"
echo ""
echo "  💡 Per revisione completa di un testo:"
echo "     Incollalo nella chat con Claude!"
echo ""
echo "  🔧 Il menu principale (bash ~/gestione-sito.sh)"
echo "     usa gia lo script aggiornato."
echo "============================================"
