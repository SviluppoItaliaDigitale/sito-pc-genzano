#!/bin/bash
# ============================================================
# GESTIONE SITO — Protezione Civile Genzano di Roma
# v2.2 — Aprile 2026
# ============================================================

SITO_DIR="$HOME/sito-pc-genzano"
CONTENT_DIR="$SITO_DIR/content"
DATA_DIR="$SITO_DIR/data"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

mostra_menu() {
  clear
  echo -e "${BLUE}${BOLD}"
  echo "╔══════════════════════════════════════════════════════════╗"
  echo "║   GESTIONE SITO — Protezione Civile Genzano di Roma    ║"
  echo "║   v2.2 — $(date '+%d/%m/%Y %H:%M')                              ║"
  echo "╚══════════════════════════════════════════════════════════╝"
  echo -e "${NC}"

  # Stato emergenza
  if [ -f "$DATA_DIR/emergenza.json" ]; then
    stato_em=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print('ATTIVA — '+d.get('titolo','') if d.get('attiva') else 'disattivata')" 2>/dev/null)
    if echo "$stato_em" | grep -q "ATTIVA"; then
      echo -e "  ${RED}${BOLD}⚠ EMERGENZA: $stato_em${NC}"
    else
      echo -e "  Emergenza: $stato_em"
    fi
    echo ""
  fi

  echo -e "${CYAN}── COMUNICAZIONI ──${NC}"
  echo "  1) Crea nuova comunicazione"
  echo "  2) Crea comunicazione da file Word"
  echo "  3) Modifica comunicazione"
  echo "  4) Elimina comunicazione"
  echo ""
  echo -e "${CYAN}── PAGINE ──${NC}"
  echo "  5) Crea nuova pagina"
  echo "  6) Modifica pagina"
  echo "  7) Modifica pagina rischio"
  echo "  8) Elimina pagina"
  echo ""
  echo -e "${CYAN}── EMERGENZA ──${NC}"
  echo "  9) Attiva emergenza"
  echo " 10) Modifica emergenza attiva"
  echo " 11) Sospendi emergenza (mantiene i dati)"
  echo ""
  echo -e "${CYAN}── ALLERTA METEO ──${NC}"
  echo " 12) Imposta livello allerta"
  echo ""
  echo -e "${CYAN}── PUBBLICA E TESTA ──${NC}"
  echo " 13) Test sito in locale"
  echo " 14) Pubblica modifiche online"
  echo " 15) Stato repository"
  echo ""
  echo -e "${CYAN}── LINK RAPIDI ──${NC}"
  echo " 16) Sito produzione    17) GitHub Actions"
  echo " 18) Repository GitHub  19) Bollettino Lazio"
  echo " 20) ActivePager        21) Claude AI"
  echo ""
  echo -e "${CYAN}── GUIDE ──${NC}"
  echo " 22) Struttura del sito"
  echo " 23) Guida pubblicazione"
  echo ""
  echo -e "${YELLOW}  0) Esci${NC}"
  echo ""
}

# ══════════════════════════════════════════
mostra_menu
echo -ne "${BOLD}Scegli [0-23]: ${NC}"
read scelta

case $scelta in

# ══════════════════════════════════════════
# 1) CREA COMUNICAZIONE
# ══════════════════════════════════════════
1)
  echo ""
  echo -e "${GREEN}══ Nuova comunicazione ══${NC}"
  echo ""
  echo -e "${YELLOW}Puoi usare le frecce ← → per muovere il cursore in ogni campo.${NC}"
  echo ""

  echo -e "${BOLD}Titolo:${NC}"
  read -e -p "> " titolo
  if [ -z "$titolo" ]; then
    echo -e "${RED}Errore: il titolo è obbligatorio.${NC}"
    read -p "Premi INVIO..."; exec bash "$0"
  fi

  echo ""
  echo -e "${BOLD}Tipo:${NC}"
  echo "  1) Comunicazione   2) Allerta   3) Avviso    4) Evento"
  echo "  5) Formazione      6) Attività  7) Volontariato"
  read -p "Scegli [1-7, default 1]: " bn
  case $bn in 2) badge="Allerta";; 3) badge="Avviso";; 4) badge="Evento";; 5) badge="Formazione";; 6) badge="Attività";; 7) badge="Volontariato";; *) badge="Comunicazione";; esac

  echo ""
  echo -e "${BOLD}Priorità:${NC}  1) Normale   2) Urgente"
  read -p "Scegli [1-2, default 1]: " pn
  [ "$pn" = "2" ] && priorita="urgente" || priorita="normale"

  echo ""
  echo -e "${BOLD}Descrizione breve (appare nelle anteprime):${NC}"
  read -e -p "> " desc

  echo ""
  echo -e "${BOLD}Autore:${NC}"
  read -e -p "> " -i "Gruppo Comunale Volontari PC Genzano" autore

  echo ""
  echo -e "${BOLD}Area interessata (opzionale, es. Tutto il territorio comunale):${NC}"
  read -e -p "> " area

  echo ""
  echo -e "${BOLD}Data scadenza (opzionale, formato AAAA-MM-GG):${NC}"
  read -e -p "> " scadenza

  echo ""
  echo -e "${BOLD}Immagine (opzionale, es. /images/foto.jpg):${NC}"
  read -e -p "> " image

  slug=$(echo "$titolo" | tr '[:upper:]' '[:lower:]' | sed 's/à/a/g;s/è/e/g;s/é/e/g;s/ì/i/g;s/ò/o/g;s/ù/u/g' | sed 's/ /-/g;s/[^a-z0-9-]//g;s/--*/-/g;s/^-//;s/-$//')
  data=$(date +%Y-%m-%d)
  file="$CONTENT_DIR/comunicazioni/${data}-${slug}.md"

  cat > "$file" << EOF
---
title: "$titolo"
date: $data
badge: "$badge"
priorita: "$priorita"
autore: "$autore"
description: "$desc"
image: "$image"
area: "$area"
scadenza: "$scadenza"
allegati: []
draft: false
---

Scrivi qui il contenuto della comunicazione.
EOF

  echo ""
  echo -e "${GREEN}════════════════════════════════════════${NC}"
  echo -e "${GREEN}Comunicazione creata!${NC}"
  echo -e "${GREEN}════════════════════════════════════════${NC}"
  echo ""
  echo -e "File: ${BOLD}$file${NC}"
  echo ""
  echo -e "Prossimi passi:"
  echo -e "  1. Scrivi il contenuto:  ${BOLD}nano $file${NC}"
  echo -e "     (salva: Ctrl+O poi INVIO, esci: Ctrl+X)"
  echo -e "  2. Testa in locale:      ${BOLD}cd ~/sito-pc-genzano && hugo server${NC}"
  echo -e "  3. Pubblica:             usa opzione 14 del menu"
  echo ""
  read -p "Aprire il file adesso con nano? [S/n]: " apri
  [ "$apri" != "n" ] && [ "$apri" != "N" ] && nano "$file"
  ;;

# ══════════════════════════════════════════
# 2) DA WORD
# ══════════════════════════════════════════
2)
  echo ""
  echo -e "${GREEN}══ Comunicazione da file Word ══${NC}"
  echo ""
  if [ -f "$HOME/pubblica-da-word.sh" ]; then
    bash "$HOME/pubblica-da-word.sh"
  else
    echo "Comandi da eseguire:"
    echo ""
    echo "  1. Converti il file Word:"
    echo -e "     ${BOLD}pandoc nomefile.docx -t markdown -o articolo.md${NC}"
    echo ""
    echo "  2. Rimuovi backslash dagli apostrofi:"
    echo -e "     ${BOLD}sed -i \"s/\\\\\\\\'/'/g\" articolo.md${NC}"
    echo ""
    echo "  3. Aggiungi il frontmatter in cima (usa opzione 1 del menu per creare"
    echo "     il file con tutti i campi, poi incolla il contenuto convertito)"
  fi
  ;;

# ══════════════════════════════════════════
# 3) MODIFICA COMUNICAZIONE
# ══════════════════════════════════════════
3)
  echo ""
  echo -e "${GREEN}══ Modifica comunicazione ══${NC}"
  echo ""
  files=($(ls -1 "$CONTENT_DIR/comunicazioni/" | grep -v "_index"))
  if [ ${#files[@]} -eq 0 ]; then
    echo "Nessuna comunicazione trovata."
  else
    for i in "${!files[@]}"; do
      echo "  $((i+1))) ${files[$i]}"
    done
    echo ""
    read -p "Numero da modificare: " num
    idx=$((num-1))
    if [ $idx -ge 0 ] && [ $idx -lt ${#files[@]} ]; then
      echo ""
      echo -e "${YELLOW}Salva: Ctrl+O poi INVIO — Esci: Ctrl+X${NC}"
      read -p "Premi INVIO per aprire..."
      nano "$CONTENT_DIR/comunicazioni/${files[$idx]}"
    else
      echo -e "${RED}Selezione non valida.${NC}"
    fi
  fi
  ;;

# ══════════════════════════════════════════
# 4) ELIMINA COMUNICAZIONE
# ══════════════════════════════════════════
4)
  echo ""
  echo -e "${RED}══ Elimina comunicazione ══${NC}"
  echo ""
  files=($(ls -1 "$CONTENT_DIR/comunicazioni/" | grep -v "_index"))
  if [ ${#files[@]} -eq 0 ]; then
    echo "Nessuna comunicazione trovata."
  else
    for i in "${!files[@]}"; do
      echo "  $((i+1))) ${files[$i]}"
    done
    echo ""
    read -p "Numero da eliminare: " num
    idx=$((num-1))
    if [ $idx -ge 0 ] && [ $idx -lt ${#files[@]} ]; then
      echo ""
      echo -e "${RED}Stai per eliminare: ${files[$idx]}${NC}"
      read -p "Scrivi 'elimina' per confermare: " conf
      if [ "$conf" = "elimina" ]; then
        rm "$CONTENT_DIR/comunicazioni/${files[$idx]}"
        echo -e "${GREEN}Eliminato.${NC}"
      else
        echo "Annullato."
      fi
    else
      echo -e "${RED}Selezione non valida.${NC}"
    fi
  fi
  ;;

# ══════════════════════════════════════════
# 5) CREA PAGINA
# ══════════════════════════════════════════
5)
  echo ""
  echo -e "${GREEN}══ Crea nuova pagina ══${NC}"
  echo ""
  echo -e "${BOLD}Nome della sezione (diventerà l'URL, es. 'avvisi-neve'):${NC}"
  echo -e "${YELLOW}Usa lettere minuscole e trattini, niente spazi o accenti.${NC}"
  read -e -p "> " sezione
  if [ -z "$sezione" ]; then
    echo -e "${RED}Errore: il nome è obbligatorio.${NC}"
    read -p "Premi INVIO..."; exec bash "$0"
  fi

  echo ""
  echo -e "${BOLD}Titolo della pagina (come apparirà sul sito):${NC}"
  read -e -p "> " titolo

  echo ""
  echo -e "${BOLD}Descrizione breve:${NC}"
  read -e -p "> " desc

  mkdir -p "$CONTENT_DIR/$sezione"
  cat > "$CONTENT_DIR/$sezione/_index.md" << EOF
---
title: "$titolo"
description: "$desc"
layout: "single"
---

Scrivi qui il contenuto della pagina.
EOF

  echo ""
  echo -e "${GREEN}Pagina creata: content/$sezione/_index.md${NC}"
  echo -e "URL: /$sezione/"
  echo ""
  read -p "Aprire il file con nano? [S/n]: " apri
  [ "$apri" != "n" ] && [ "$apri" != "N" ] && nano "$CONTENT_DIR/$sezione/_index.md"
  ;;

# ══════════════════════════════════════════
# 6) MODIFICA PAGINA
# ══════════════════════════════════════════
6)
  echo ""
  echo -e "${GREEN}══ Modifica pagina ══${NC}"
  echo ""
  pagine=()
  nomi=()
  while IFS= read -r f; do
    sez=$(echo "$f" | sed "s|$CONTENT_DIR/||;s|/_index.md||")
    pagine+=("$f")
    nomi+=("$sez")
  done < <(find "$CONTENT_DIR" -maxdepth 2 -name "_index.md" | sort)

  for i in "${!nomi[@]}"; do
    echo "  $((i+1))) ${nomi[$i]}"
  done
  echo ""
  read -p "Numero da modificare: " num
  idx=$((num-1))
  if [ $idx -ge 0 ] && [ $idx -lt ${#pagine[@]} ]; then
    echo ""
    echo -e "${YELLOW}Salva: Ctrl+O poi INVIO — Esci: Ctrl+X${NC}"
    read -p "Premi INVIO per aprire..."
    nano "${pagine[$idx]}"
  else
    echo -e "${RED}Selezione non valida.${NC}"
  fi
  ;;

# ══════════════════════════════════════════
# 7) MODIFICA PAGINA RISCHIO
# ══════════════════════════════════════════
7)
  echo ""
  echo -e "${GREEN}══ Modifica pagina rischio ══${NC}"
  echo ""
  files=($(ls -1 "$CONTENT_DIR/rischi-prevenzione/" | grep -v "_index"))
  for i in "${!files[@]}"; do
    echo "  $((i+1))) ${files[$i]}"
  done
  echo ""
  read -p "Numero da modificare: " num
  idx=$((num-1))
  if [ $idx -ge 0 ] && [ $idx -lt ${#files[@]} ]; then
    echo ""
    echo -e "${YELLOW}Salva: Ctrl+O poi INVIO — Esci: Ctrl+X${NC}"
    read -p "Premi INVIO per aprire..."
    nano "$CONTENT_DIR/rischi-prevenzione/${files[$idx]}"
  else
    echo -e "${RED}Selezione non valida.${NC}"
  fi
  ;;

# ══════════════════════════════════════════
# 8) ELIMINA PAGINA
# ══════════════════════════════════════════
8)
  echo ""
  echo -e "${RED}══ Elimina pagina ══${NC}"
  echo ""
  echo -e "${YELLOW}ATTENZIONE: le pagine principali del sito (chi-siamo, contatti, ecc.)${NC}"
  echo -e "${YELLOW}non dovrebbero essere eliminate. Usa questa funzione solo per pagine${NC}"
  echo -e "${YELLOW}che hai creato tu e che non servono più.${NC}"
  echo ""

  pagine=()
  nomi=()
  while IFS= read -r f; do
    sez=$(echo "$f" | sed "s|$CONTENT_DIR/||;s|/_index.md||")
    pagine+=("$f")
    nomi+=("$sez")
  done < <(find "$CONTENT_DIR" -maxdepth 2 -name "_index.md" | sort)

  for i in "${!nomi[@]}"; do
    echo "  $((i+1))) ${nomi[$i]}"
  done
  echo ""
  read -p "Numero da eliminare: " num
  idx=$((num-1))
  if [ $idx -ge 0 ] && [ $idx -lt ${#pagine[@]} ]; then
    echo ""
    echo -e "${RED}Stai per eliminare: ${nomi[$idx]}${NC}"
    read -p "Scrivi 'elimina' per confermare: " conf
    if [ "$conf" = "elimina" ]; then
      rm -rf "$CONTENT_DIR/${nomi[$idx]}"
      echo -e "${GREEN}Eliminato.${NC}"
    else
      echo "Annullato."
    fi
  else
    echo -e "${RED}Selezione non valida.${NC}"
  fi
  ;;

# ══════════════════════════════════════════
# 9) ATTIVA EMERGENZA
# ══════════════════════════════════════════
9)
  echo ""
  echo -e "${RED}══ Attiva emergenza ══${NC}"
  echo ""

  # Controlla se c'è un'emergenza sospesa da riattivare
  titolo_esistente=""
  if [ -f "$DATA_DIR/emergenza.json" ]; then
    titolo_esistente=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('titolo',''))" 2>/dev/null)
    attiva_esistente=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('attiva',False))" 2>/dev/null)
  fi

  if [ "$attiva_esistente" = "True" ]; then
    echo -e "${YELLOW}L'emergenza è già attiva!${NC}"
    echo "Usa opzione 10 per modificarla o 11 per sospenderla."
    read -p "Premi INVIO..."; exec bash "$0"
  fi

  if [ -n "$titolo_esistente" ] && [ "$titolo_esistente" != "" ]; then
    echo -e "Trovata emergenza sospesa: ${BOLD}$titolo_esistente${NC}"
    echo ""
    echo "  1) Riattiva questa emergenza"
    echo "  2) Crea una nuova emergenza"
    read -p "Scegli [1-2]: " riattiva

    if [ "$riattiva" = "1" ]; then
      python3 -c "
import json
with open('$DATA_DIR/emergenza.json','r') as f: d=json.load(f)
d['attiva']=True
d['ultimo_aggiornamento']='$(date -Is)'
with open('$DATA_DIR/emergenza.json','w') as f: json.dump(d,f,indent=2,ensure_ascii=False)
"
      echo ""
      echo -e "${GREEN}════════════════════════════════════════${NC}"
      echo -e "${GREEN}Emergenza RIATTIVATA: $titolo_esistente${NC}"
      echo -e "${GREEN}════════════════════════════════════════${NC}"
      echo ""
      echo -e "La homepage è in modalità emergenza."
      echo -e "Per rendere visibile online: usa opzione ${BOLD}14${NC} del menu."
      read -p "Premi INVIO..."; exec bash "$0"
    fi
  fi

  # Nuova emergenza
  echo -e "${YELLOW}ATTENZIONE: la homepage si riorganizzerà in modalità emergenza.${NC}"
  echo ""

  echo "Colore del banner:"
  echo "  1) Blu    2) Azzurro  3) Verde   4) Giallo"
  echo "  5) Arancione  6) Rosso  7) Viola"
  read -p "Scegli [1-7]: " tn
  case $tn in 1) tipo="blu";; 2) tipo="azzurro";; 3) tipo="verde";; 4) tipo="giallo";; 5) tipo="arancione";; 6) tipo="rosso";; 7) tipo="viola";; *) tipo="blu";; esac

  echo ""
  echo -e "${BOLD}Titolo del banner:${NC}"
  read -e -p "> " titolo

  echo ""
  echo -e "${BOLD}Descrizione (cosa sta succedendo):${NC}"
  read -e -p "> " desc

  echo ""
  echo -e "${BOLD}Link per maggiori informazioni (opzionale):${NC}"
  read -e -p "> " link

  cat > "$DATA_DIR/emergenza.json" << EOF
{
  "attiva": true,
  "tipo": "$tipo",
  "titolo": "$titolo",
  "descrizione": "$desc",
  "link": "$link",
  "ultimo_aggiornamento": "$(date -Is)"
}
EOF

  echo ""
  echo -e "${GREEN}════════════════════════════════════════${NC}"
  echo -e "${GREEN}Emergenza ATTIVATA${NC}"
  echo -e "${GREEN}════════════════════════════════════════${NC}"
  echo ""
  echo -e "Per rendere visibile online: usa opzione ${BOLD}14${NC} del menu."
  ;;

# ══════════════════════════════════════════
# 10) MODIFICA EMERGENZA
# ══════════════════════════════════════════
10)
  echo ""
  echo -e "${YELLOW}══ Modifica emergenza attiva ══${NC}"
  echo ""
  if [ -f "$DATA_DIR/emergenza.json" ]; then
    echo "Contenuto attuale:"
    echo ""
    cat "$DATA_DIR/emergenza.json"
    echo ""
    echo -e "${YELLOW}Salva: Ctrl+O poi INVIO — Esci: Ctrl+X${NC}"
    read -p "Premi INVIO per aprire il file..."
    nano "$DATA_DIR/emergenza.json"
  else
    echo "Nessun file emergenza trovato."
  fi
  ;;

# ══════════════════════════════════════════
# 11) SOSPENDI EMERGENZA
# ══════════════════════════════════════════
11)
  echo ""
  echo -e "${YELLOW}══ Sospendi emergenza ══${NC}"
  echo ""

  if [ -f "$DATA_DIR/emergenza.json" ]; then
    titolo_em=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('titolo',''))" 2>/dev/null)
    attiva_em=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('attiva',False))" 2>/dev/null)

    if [ "$attiva_em" != "True" ]; then
      echo "L'emergenza non è attiva al momento."
      read -p "Premi INVIO..."; exec bash "$0"
    fi

    echo -e "Emergenza attuale: ${BOLD}$titolo_em${NC}"
    echo ""
    echo -e "${YELLOW}L'emergenza verrà SOSPESA ma i dati restano salvati.${NC}"
    echo -e "${YELLOW}Potrai riattivare la stessa emergenza con l'opzione 9.${NC}"
    echo ""
    read -p "Confermi la sospensione? [S/n]: " conf

    if [ "$conf" = "n" ] || [ "$conf" = "N" ]; then
      echo "Annullato."
    else
      python3 -c "
import json
with open('$DATA_DIR/emergenza.json','r') as f: d=json.load(f)
d['attiva']=False
with open('$DATA_DIR/emergenza.json','w') as f: json.dump(d,f,indent=2,ensure_ascii=False)
"
      echo ""
      echo -e "${GREEN}════════════════════════════════════════${NC}"
      echo -e "${GREEN}Emergenza SOSPESA${NC}"
      echo -e "${GREEN}════════════════════════════════════════${NC}"
      echo ""
      echo "La homepage è tornata in modalità ordinaria."
      echo "I dati dell'emergenza sono conservati."
      echo -e "Per rendere visibile online: usa opzione ${BOLD}14${NC} del menu."
    fi
  else
    echo "Nessun file emergenza trovato."
  fi
  ;;

# ══════════════════════════════════════════
# 12) ALLERTA METEO
# ══════════════════════════════════════════
12)
  echo ""
  echo -e "${YELLOW}══ Imposta allerta meteo ══${NC}"
  echo ""
  echo "  1) Verde — Nessuna allerta"
  echo "  2) Gialla — Attenzione"
  echo "  3) Arancione — Preallarme"
  echo "  4) Rossa — Allarme"
  echo ""
  read -p "Scegli [1-4]: " ln
  case $ln in
    1) livello="verde"; titolo="NESSUNA ALLERTA"; desc="Non sono previsti fenomeni significativi sul nostro territorio.";;
    2) livello="gialla"; titolo="ALLERTA GIALLA"; desc="Criticità ordinaria. Prestare attenzione.";;
    3) livello="arancione"; titolo="ALLERTA ARANCIONE"; desc="Criticità moderata. Limitare gli spostamenti.";;
    4) livello="rossa"; titolo="ALLERTA ROSSA"; desc="Criticità elevata. Seguire le indicazioni delle autorità.";;
    *) echo -e "${RED}Scelta non valida.${NC}"; read -p "Premi INVIO..."; exec bash "$0";;
  esac

  cat > "$DATA_DIR/allerta.json" << EOF
{
  "livello": "$livello",
  "titolo": "$titolo",
  "descrizione": "$desc",
  "ultimo_aggiornamento": "$(date -Is)"
}
EOF
  echo ""
  echo -e "${GREEN}Allerta impostata: $titolo${NC}"
  echo "Il CSV del DPC sovrascrive dopo 24 ore."
  ;;

# ══════════════════════════════════════════
# 13) TEST LOCALE
# ══════════════════════════════════════════
13)
  echo ""
  echo -e "${GREEN}══ Test locale ══${NC}"
  echo ""
  echo -e "Apri nel browser: ${BOLD}http://localhost:1313/${NC}"
  echo -e "Per fermare: ${BOLD}Ctrl+C${NC}"
  echo ""
  read -p "Premi INVIO per avviare..."
  cd "$SITO_DIR" && hugo server -D
  ;;

# ══════════════════════════════════════════
# 14) PUBBLICA
# ══════════════════════════════════════════
14)
  echo ""
  echo -e "${GREEN}══ Pubblica modifiche online ══${NC}"
  echo ""
  cd "$SITO_DIR"
  echo -e "${BOLD}File modificati:${NC}"
  git status --short
  echo ""

  modifiche=$(git status --short | wc -l)
  if [ "$modifiche" -eq 0 ]; then
    echo "Nessuna modifica da pubblicare."
    read -p "Premi INVIO..."; exec bash "$0"
  fi

  read -p "Procedere con la pubblicazione? [S/n]: " conf
  [ "$conf" = "n" ] || [ "$conf" = "N" ] && { echo "Annullato."; read -p "Premi INVIO..."; exec bash "$0"; }

  echo ""
  echo -e "${BOLD}Descrizione delle modifiche:${NC}"
  read -e -p "> " -i "Aggiornamento contenuti" msg

  echo ""
  echo "Pubblicazione in corso..."
  git add .
  git commit -m "$msg"
  git push

  if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}Pubblicato!${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo ""
    echo "I siti saranno aggiornati entro 2-3 minuti."
    echo "Controlla: https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions"
    echo ""
    echo -e "${YELLOW}Dopo 3 minuti, apri il sito e premi Ctrl+F5 per vedere le modifiche.${NC}"
  else
    echo ""
    echo -e "${RED}Errore durante il push!${NC}"
    echo "Prova a eseguire: git pull --rebase && git push"
  fi
  ;;

# ══════════════════════════════════════════
# 15) STATO
# ══════════════════════════════════════════
15)
  echo ""
  echo -e "${GREEN}══ Stato repository ══${NC}"
  echo ""
  cd "$SITO_DIR"
  git status
  echo ""
  echo -e "${BOLD}Ultime 10 modifiche:${NC}"
  git log --oneline -10
  ;;

# ══════════════════════════════════════════
# 16-21) LINK RAPIDI
# ══════════════════════════════════════════
16) xdg-open "https://www.protezionecivilegenzano.it/" 2>/dev/null || echo "https://www.protezionecivilegenzano.it/" ;;
17) xdg-open "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions" 2>/dev/null || echo "Vai su github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions" ;;
18) xdg-open "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano" 2>/dev/null || echo "Vai su github.com/SviluppoItaliaDigitale/sito-pc-genzano" ;;
19) xdg-open "https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" 2>/dev/null || echo "Vai su protezionecivile.regione.lazio.it" ;;
20) xdg-open "https://activepager.com/auth/login" 2>/dev/null || echo "https://activepager.com/auth/login" ;;
21) xdg-open "https://claude.ai" 2>/dev/null || echo "https://claude.ai" ;;

# ══════════════════════════════════════════
# 22) STRUTTURA
# ══════════════════════════════════════════
22)
  echo ""
  echo -e "${GREEN}══ Struttura del sito ══${NC}"
  echo ""
  echo -e "${BOLD}MENU PRINCIPALE:${NC}"
  echo "  Home | Chi Siamo | Rischi e Prevenzione | Allerte Meteo"
  echo "  Comunicazioni | Diventa Volontario | Contatti"
  echo ""
  echo -e "${BOLD}PAGINE RISCHIO (9):${NC}"
  echo "  rischio-sismico | rischio-idrogeologico | rischio-incendio"
  echo "  vento-forte | temporali-intensi | ondate-di-calore"
  echo "  blackout | kit-emergenza | persone-necessita-specifiche"
  echo ""
  echo -e "${BOLD}ALTRE SEZIONI:${NC}"
  echo "  piano-emergenza | piano-familiare | cartografia | area-download"
  echo "  cosa-fare-adesso | numeri-utili | faq | formazione | siti-utili"
  echo ""
  echo -e "${BOLD}DATA FILES:${NC}"
  echo "  allerta.json | emergenza.json | numeri_utili.yaml"
  echo "  quick_links.yaml | risk_cards.yaml | social_links.yaml"
  echo ""
  echo -e "${BOLD}BADGE COMUNICAZIONI:${NC}"
  echo "  Allerta | Avviso | Comunicazione | Attività"
  echo "  Formazione | Evento | Volontariato"
  echo ""
  echo -e "${BOLD}PARAMETRI ARTICOLI:${NC}"
  echo "  title, date, badge, description (obbligatori)"
  echo "  priorita, autore, image, area, scadenza, allegati (opzionali)"
  ;;

# ══════════════════════════════════════════
# 23) GUIDA
# ══════════════════════════════════════════
23)
  echo ""
  if [ -f "$SITO_DIR/GUIDA-UPLOAD-V2.md" ]; then
    less "$SITO_DIR/GUIDA-UPLOAD-V2.md"
  elif [ -f "$HOME/GUIDA-PUBBLICAZIONE.txt" ]; then
    less "$HOME/GUIDA-PUBBLICAZIONE.txt"
  else
    echo "File guida non trovato."
  fi
  ;;

# ══════════════════════════════════════════
# 0) ESCI
# ══════════════════════════════════════════
0)
  echo -e "\n${GREEN}Arrivederci!${NC}"
  exit 0
  ;;

*)
  echo -e "\n${RED}Opzione non valida.${NC}"
  ;;

esac

echo ""
read -p "Premi INVIO per tornare al menu..."
exec bash "$0"
