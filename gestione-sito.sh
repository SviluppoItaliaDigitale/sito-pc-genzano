#!/bin/bash
# ============================================================
# GESTIONE SITO — Protezione Civile Genzano di Roma
# Menu principale per la gestione del sito web
# Versione 2.0 — Aprile 2026
# ============================================================

SITO_DIR="$HOME/sito-pc-genzano"
CONTENT_DIR="$SITO_DIR/content"
DATA_DIR="$SITO_DIR/data"

# Colori
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m' # No Color

clear
echo -e "${BLUE}${BOLD}"
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   GESTIONE SITO — Protezione Civile Genzano di Roma    ║"
echo "║   v2.0 — $(date '+%d/%m/%Y %H:%M')                              ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}── ARTICOLI E COMUNICAZIONI ──${NC}"
echo "  1) Pubblica nuova comunicazione"
echo "  2) Pubblica comunicazione da file Word"
echo "  3) Modifica comunicazione esistente"
echo "  4) Elimina comunicazione"
echo ""
echo -e "${CYAN}── PAGINE DEL SITO ──${NC}"
echo "  5) Modifica pagina esistente"
echo "  6) Modifica pagina rischio (Rischi e Prevenzione)"
echo ""
echo -e "${CYAN}── ALLERTA METEO ──${NC}"
echo "  7) Imposta livello allerta manuale"
echo ""
echo -e "${CYAN}── EMERGENZA ──${NC}"
echo "  8) Pubblica banner emergenza"
echo "  9) Modifica banner emergenza"
echo " 10) Revoca banner emergenza"
echo ""
echo -e "${CYAN}── STRUMENTI ──${NC}"
echo " 11) Apri AI Claude per assistenza"
echo " 12) Validatore contenuti Designers Italia"
echo ""
echo -e "${CYAN}── MANUTENZIONE ──${NC}"
echo " 13) Test sito in locale (hugo server)"
echo " 14) Pubblica modifiche (git push)"
echo " 15) Aggiorna dipendenze (Bootstrap Italia)"
echo " 16) Ultime modifiche (git log)"
echo " 17) Stato del repository (git status)"
echo ""
echo -e "${CYAN}── LINK RAPIDI ──${NC}"
echo " 18) Apri sito produzione (Aruba)"
echo " 19) Apri GitHub Actions"
echo " 20) Apri repository GitHub"
echo " 21) Apri bollettino Regione Lazio"
echo " 22) Apri gestionale ActivePager"
echo ""
echo -e "${CYAN}── GUIDE ──${NC}"
echo " 23) Guida alla pubblicazione"
echo " 24) Checklist contenuti"
echo " 25) Struttura del sito (mappa file)"
echo ""
echo -e "${YELLOW}  0) Esci${NC}"
echo ""
echo -ne "${BOLD}Scegli un'opzione [0-25]: ${NC}"
read scelta

case $scelta in

# ── ARTICOLI ──

1)
  echo -e "\n${GREEN}── Nuova comunicazione ──${NC}"
  if [ -f "$HOME/pubblica-notizia.sh" ]; then
    bash "$HOME/pubblica-notizia.sh"
  else
    echo -e "${YELLOW}Creazione manuale:${NC}"
    echo -ne "Titolo: "; read titolo
    echo -ne "Badge [Comunicazione/Allerta/Avviso/Evento/Formazione/Attività/Volontariato]: "; read badge
    badge=${badge:-Comunicazione}
    echo -ne "Descrizione breve: "; read desc

    slug=$(echo "$titolo" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g; s/[^a-z0-9-]//g')
    data=$(date +%Y-%m-%d)
    file="$CONTENT_DIR/comunicazioni/${data}-${slug}.md"

    cat > "$file" << EOF
---
title: "$titolo"
date: $data
badge: "$badge"
description: "$desc"
image: ""
---

Scrivi qui il contenuto della comunicazione.
EOF
    echo -e "${GREEN}File creato: $file${NC}"
    echo -e "Aprilo con: ${BOLD}nano $file${NC}"
  fi
  ;;

2)
  echo -e "\n${GREEN}── Pubblica da file Word ──${NC}"
  if [ -f "$HOME/pubblica-da-word.sh" ]; then
    bash "$HOME/pubblica-da-word.sh"
  else
    echo "Script pubblica-da-word.sh non trovato."
    echo "Usa pandoc manualmente: pandoc file.docx -t markdown -o output.md"
    echo "ATTENZIONE: rimuovi i backslash dagli apostrofi con:"
    echo "  sed -i \"s/\\\\\\\\'/'/g\" output.md"
  fi
  ;;

3)
  echo -e "\n${GREEN}── Modifica comunicazione ──${NC}"
  echo "Comunicazioni disponibili:"
  echo ""
  ls -1 "$CONTENT_DIR/comunicazioni/" | grep -v "_index" | nl
  echo ""
  echo -ne "Numero da modificare: "; read num
  file=$(ls -1 "$CONTENT_DIR/comunicazioni/" | grep -v "_index" | sed -n "${num}p")
  if [ -n "$file" ]; then
    nano "$CONTENT_DIR/comunicazioni/$file"
  else
    echo "Selezione non valida."
  fi
  ;;

4)
  echo -e "\n${RED}── Elimina comunicazione ──${NC}"
  echo "Comunicazioni disponibili:"
  echo ""
  ls -1 "$CONTENT_DIR/comunicazioni/" | grep -v "_index" | nl
  echo ""
  echo -ne "Numero da eliminare: "; read num
  file=$(ls -1 "$CONTENT_DIR/comunicazioni/" | grep -v "_index" | sed -n "${num}p")
  if [ -n "$file" ]; then
    echo -ne "${RED}Confermi eliminazione di $file? [s/N]: ${NC}"; read conf
    if [ "$conf" = "s" ] || [ "$conf" = "S" ]; then
      rm "$CONTENT_DIR/comunicazioni/$file"
      echo -e "${GREEN}Eliminato.${NC}"
    fi
  fi
  ;;

# ── PAGINE ──

5)
  echo -e "\n${GREEN}── Modifica pagina ──${NC}"
  echo "Pagine disponibili:"
  echo ""
  i=1
  for f in $(find "$CONTENT_DIR" -maxdepth 2 -name "_index.md" | sort); do
    sezione=$(echo "$f" | sed "s|$CONTENT_DIR/||" | sed 's|/_index.md||')
    echo "  $i) $sezione"
    i=$((i+1))
  done
  echo ""
  echo -ne "Numero da modificare: "; read num
  file=$(find "$CONTENT_DIR" -maxdepth 2 -name "_index.md" | sort | sed -n "${num}p")
  if [ -n "$file" ]; then
    nano "$file"
  else
    echo "Selezione non valida."
  fi
  ;;

6)
  echo -e "\n${GREEN}── Modifica pagina rischio ──${NC}"
  echo "Pagine rischio disponibili:"
  echo ""
  ls -1 "$CONTENT_DIR/rischi-prevenzione/" | grep -v "_index" | nl
  echo ""
  echo -ne "Numero da modificare: "; read num
  file=$(ls -1 "$CONTENT_DIR/rischi-prevenzione/" | grep -v "_index" | sed -n "${num}p")
  if [ -n "$file" ]; then
    nano "$CONTENT_DIR/rischi-prevenzione/$file"
  else
    echo "Selezione non valida."
  fi
  ;;

# ── ALLERTA ──

7)
  echo -e "\n${YELLOW}── Imposta allerta meteo ──${NC}"
  echo "Livelli: verde, gialla, arancione, rossa"
  echo -ne "Livello: "; read livello
  livello=${livello:-verde}

  case $livello in
    verde) titolo="NESSUNA ALLERTA"; desc="Non sono previsti fenomeni significativi sul nostro territorio.";;
    gialla) titolo="ALLERTA GIALLA"; desc="Criticità ordinaria. Prestare attenzione.";;
    arancione) titolo="ALLERTA ARANCIONE"; desc="Criticità moderata. Limitare gli spostamenti.";;
    rossa) titolo="ALLERTA ROSSA"; desc="Criticità elevata. Seguire le indicazioni delle autorità.";;
    *) echo "Livello non valido."; exit 1;;
  esac

  cat > "$DATA_DIR/allerta.json" << EOF
{
  "livello": "$livello",
  "titolo": "$titolo",
  "descrizione": "$desc",
  "ultimo_aggiornamento": "$(date -Is)"
}
EOF
  echo -e "${GREEN}Allerta impostata: $titolo${NC}"
  echo "NOTA: sul sito il dato CSV del DPC ha priorità dopo 24 ore."
  ;;

# ── EMERGENZA ──

8)
  echo -e "\n${RED}── Pubblica banner emergenza ──${NC}"
  echo "Tipi colore: blu, azzurro, verde, giallo, arancione, rosso, viola"
  echo -ne "Tipo colore: "; read tipo
  tipo=${tipo:-blu}
  echo -ne "Titolo: "; read titolo
  echo -ne "Descrizione: "; read desc
  echo -ne "Link (vuoto se nessuno): "; read link

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
  echo -e "${GREEN}Banner emergenza ATTIVATO${NC}"
  echo -e "${YELLOW}IMPORTANTE: In modalità emergenza la homepage si riorganizza automaticamente.${NC}"
  ;;

9)
  echo -e "\n${YELLOW}── Modifica banner emergenza ──${NC}"
  nano "$DATA_DIR/emergenza.json"
  ;;

10)
  echo -e "\n${GREEN}── Revoca banner emergenza ──${NC}"
  cat > "$DATA_DIR/emergenza.json" << EOF
{
  "attiva": false,
  "tipo": "blu",
  "titolo": "",
  "descrizione": "",
  "link": "",
  "ultimo_aggiornamento": ""
}
EOF
  echo -e "${GREEN}Banner emergenza DISATTIVATO. Homepage tornata in modalità ordinaria.${NC}"
  ;;

# ── STRUMENTI ──

11)
  echo -e "\n${GREEN}Apro Claude AI...${NC}"
  if [ -f "$HOME/correggi-con-ai.sh" ]; then
    bash "$HOME/correggi-con-ai.sh"
  else
    xdg-open "https://claude.ai" 2>/dev/null || echo "Vai su https://claude.ai"
  fi
  ;;

12)
  echo -e "\n${GREEN}Validatore Designers Italia...${NC}"
  if [ -f "$HOME/valida-contenuto.sh" ]; then
    bash "$HOME/valida-contenuto.sh"
  else
    echo "Script non trovato. Usa il validatore online:"
    echo "https://designers.italia.it/modello/comuni/"
  fi
  ;;

# ── MANUTENZIONE ──

13)
  echo -e "\n${GREEN}── Test locale ──${NC}"
  cd "$SITO_DIR"
  echo "Avvio hugo server... (Ctrl+C per fermare)"
  echo "Apri http://localhost:1313/ nel browser"
  hugo server -D
  ;;

14)
  echo -e "\n${GREEN}── Pubblica modifiche ──${NC}"
  cd "$SITO_DIR"
  echo "Stato attuale:"
  git status --short
  echo ""
  echo -ne "Messaggio di commit: "; read msg
  msg=${msg:-"Aggiornamento contenuti"}
  git add .
  git commit -m "$msg"
  git push
  echo -e "\n${GREEN}Pubblicato! GitHub Actions eseguirà il deploy su Aruba e GitHub Pages.${NC}"
  echo "Controlla lo stato su: https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions"
  ;;

15)
  echo -e "\n${GREEN}── Aggiorna dipendenze ──${NC}"
  cd "$SITO_DIR"
  echo "Versione Bootstrap Italia attuale:"
  cat .bootstrap-italia-version 2>/dev/null || echo "Non trovata"
  echo ""
  echo "Il workflow update-bootstrap-italia.yml controlla ogni lunedì."
  echo "Per forzare: vai su GitHub Actions e lancia manualmente il workflow."
  ;;

16)
  echo -e "\n${GREEN}── Ultime modifiche ──${NC}"
  cd "$SITO_DIR"
  git log --oneline -15
  ;;

17)
  echo -e "\n${GREEN}── Stato repository ──${NC}"
  cd "$SITO_DIR"
  git status
  ;;

# ── LINK RAPIDI ──

18) xdg-open "https://www.protezionecivilegenzano.it/" 2>/dev/null || echo "https://www.protezionecivilegenzano.it/" ;;
19) xdg-open "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions" 2>/dev/null || echo "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions" ;;
20) xdg-open "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano" 2>/dev/null || echo "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano" ;;
21) xdg-open "https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" 2>/dev/null || echo "https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" ;;
22) xdg-open "https://activepager.com/auth/login" 2>/dev/null || echo "https://activepager.com/auth/login" ;;

# ── GUIDE ──

23)
  echo -e "\n${GREEN}── Guida alla pubblicazione ──${NC}"
  if [ -f "$HOME/GUIDA-PUBBLICAZIONE.txt" ]; then
    less "$HOME/GUIDA-PUBBLICAZIONE.txt"
  else
    echo "File guida non trovato."
  fi
  ;;

24)
  echo -e "\n${GREEN}── Checklist contenuti ──${NC}"
  if [ -f "$HOME/CHECKLIST-CONTENUTI.txt" ]; then
    less "$HOME/CHECKLIST-CONTENUTI.txt"
  else
    echo "File checklist non trovato."
  fi
  ;;

25)
  echo -e "\n${GREEN}── Struttura del sito ──${NC}"
  echo ""
  echo "SEZIONI PRINCIPALI (menu):"
  echo "  content/chi-siamo/         — Chi Siamo"
  echo "  content/rischi-prevenzione/ — Hub 9 pagine rischio"
  echo "  content/allerte-meteo/     — Sistema allertamento"
  echo "  content/comunicazioni/     — Articoli e notizie"
  echo "  content/diventa-volontario/ — Reclutamento"
  echo "  content/contatti/          — Recapiti e sede"
  echo ""
  echo "SEZIONI TRASVERSALI:"
  echo "  content/piano-emergenza/   — Piano Comunale"
  echo "  content/piano-familiare/   — Form interattivo"
  echo "  content/cartografia/       — Aree emergenza"
  echo "  content/area-download/     — Documenti PDF"
  echo "  content/cosa-fare-adesso/  — Azioni immediate"
  echo "  content/numeri-utili/      — Tutti i numeri"
  echo "  content/faq/               — Domande frequenti"
  echo "  content/formazione/        — Corsi e scuole"
  echo "  content/siti-utili/        — Link esterni"
  echo ""
  echo "DATA FILES (dati semi-dinamici):"
  echo "  data/allerta.json          — Stato allerta"
  echo "  data/emergenza.json        — Banner emergenza"
  echo "  data/numeri_utili.yaml     — Numeri telefono"
  echo "  data/quick_links.yaml      — Link rapidi homepage"
  echo "  data/risk_cards.yaml       — Card rischi"
  echo "  data/social_links.yaml     — Social"
  echo "  data/codici_colore.yaml    — Codici allerta"
  echo ""
  echo "BADGE COMUNICAZIONI:"
  echo "  Allerta | Avviso | Comunicazione | Attività"
  echo "  Formazione | Evento | Volontariato"
  ;;

0)
  echo -e "\n${GREEN}Arrivederci!${NC}"
  exit 0
  ;;

*)
  echo -e "\n${RED}Opzione non valida.${NC}"
  ;;

esac

echo ""
echo -ne "${BOLD}Premi INVIO per tornare al menu...${NC}"
read
exec bash "$0"
