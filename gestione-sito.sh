#!/bin/bash
# ============================================================
# GESTIONE SITO — Protezione Civile Genzano di Roma
# Menu principale per la gestione del sito web
# Versione 2.1 — Aprile 2026
#
# NOTA: tutti i campi di testo usano "read -e" che permette
# di muovere il cursore con le frecce, Home, Fine, Canc, ecc.
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
NC='\033[0m'

mostra_menu() {
  clear
  echo -e "${BLUE}${BOLD}"
  echo "╔══════════════════════════════════════════════════════════╗"
  echo "║   GESTIONE SITO — Protezione Civile Genzano di Roma    ║"
  echo "║   v2.1 — $(date '+%d/%m/%Y %H:%M')                              ║"
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
}

# ── Mostra menu e chiedi scelta ──
mostra_menu
echo -ne "${BOLD}Scegli un'opzione [0-25]: ${NC}"
read scelta

case $scelta in

# ══════════════════════════════════════════
# 1) PUBBLICA NUOVA COMUNICAZIONE
# ══════════════════════════════════════════
1)
  echo ""
  echo -e "${GREEN}══ Nuova comunicazione ══${NC}"
  echo ""

  # Titolo
  echo -e "${BOLD}Titolo della comunicazione:${NC}"
  echo -e "${YELLOW}  (puoi usare le frecce per correggere)${NC}"
  read -e -p "> " titolo
  if [ -z "$titolo" ]; then
    echo -e "${RED}Errore: il titolo è obbligatorio.${NC}"
    read -p "Premi INVIO per tornare al menu..."
    exec bash "$0"
  fi

  # Badge
  echo ""
  echo -e "${BOLD}Tipo di comunicazione:${NC}"
  echo "  1) Comunicazione (default)"
  echo "  2) Allerta"
  echo "  3) Avviso"
  echo "  4) Evento"
  echo "  5) Formazione"
  echo "  6) Attività"
  echo "  7) Volontariato"
  read -p "Scegli [1-7, default 1]: " badge_num
  case $badge_num in
    2) badge="Allerta";;
    3) badge="Avviso";;
    4) badge="Evento";;
    5) badge="Formazione";;
    6) badge="Attività";;
    7) badge="Volontariato";;
    *) badge="Comunicazione";;
  esac

  # Priorità
  echo ""
  echo -e "${BOLD}Priorità:${NC}"
  echo "  1) Normale (default)"
  echo "  2) Urgente (bordo rosso + badge URGENTE)"
  read -p "Scegli [1-2, default 1]: " prio_num
  if [ "$prio_num" = "2" ]; then
    priorita="urgente"
  else
    priorita="normale"
  fi

  # Descrizione
  echo ""
  echo -e "${BOLD}Descrizione breve (1-2 righe, appare nelle anteprime):${NC}"
  read -e -p "> " desc

  # Autore
  echo ""
  echo -e "${BOLD}Autore (chi ha scritto o approvato):${NC}"
  read -e -p "> " -i "Gruppo Comunale Volontari PC Genzano" autore
  autore=${autore:-"Gruppo Comunale Volontari PC Genzano"}

  # Area
  echo ""
  echo -e "${BOLD}Area interessata (opzionale, es. 'Tutto il territorio comunale'):${NC}"
  read -e -p "> " area

  # Scadenza
  echo ""
  echo -e "${BOLD}Data di scadenza (opzionale, formato AAAA-MM-GG, es. 2026-04-10):${NC}"
  echo -e "${YELLOW}  Dopo questa data comparirà 'Comunicazione scaduta'. Lascia vuoto se non scade.${NC}"
  read -e -p "> " scadenza

  # Immagine
  echo ""
  echo -e "${BOLD}Immagine (opzionale, es. /images/foto.jpg):${NC}"
  echo -e "${YELLOW}  L'immagine deve essere nella cartella static/images/${NC}"
  read -e -p "> " image

  # Crea slug e file
  slug=$(echo "$titolo" | tr '[:upper:]' '[:lower:]' | \
         sed 's/à/a/g; s/è/e/g; s/é/e/g; s/ì/i/g; s/ò/o/g; s/ù/u/g' | \
         sed 's/ /-/g; s/[^a-z0-9-]//g; s/--*/-/g; s/^-//; s/-$//')
  data=$(date +%Y-%m-%d)
  file="$CONTENT_DIR/comunicazioni/${data}-${slug}.md"

  # Scrivi il file
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
Puoi usare il formato Markdown:

## Sottotitolo

Testo del paragrafo.

- Elenco puntato
- Altro punto

**Testo in grassetto** e *testo in corsivo*.
EOF

  echo ""
  echo -e "${GREEN}════════════════════════════════════════${NC}"
  echo -e "${GREEN}File creato con successo!${NC}"
  echo -e "${GREEN}════════════════════════════════════════${NC}"
  echo ""
  echo -e "File: ${BOLD}$file${NC}"
  echo ""
  echo -e "Cosa fare adesso:"
  echo -e "  1. Apri il file per scrivere il contenuto:"
  echo -e "     ${BOLD}nano $file${NC}"
  echo ""
  echo -e "  2. Quando hai finito, salva con ${BOLD}Ctrl+O${NC} e esci con ${BOLD}Ctrl+X${NC}"
  echo ""
  echo -e "  3. Testa in locale:"
  echo -e "     ${BOLD}cd ~/sito-pc-genzano && hugo server${NC}"
  echo ""
  echo -e "  4. Se tutto ok, pubblica:"
  echo -e "     ${BOLD}cd ~/sito-pc-genzano && git add . && git commit -m \"Nuovo articolo: $titolo\" && git push${NC}"
  echo ""
  echo -ne "Vuoi aprire il file adesso con nano? [S/n]: "
  read apri
  if [ "$apri" != "n" ] && [ "$apri" != "N" ]; then
    nano "$file"
  fi
  ;;

# ══════════════════════════════════════════
# 2) PUBBLICA DA FILE WORD
# ══════════════════════════════════════════
2)
  echo ""
  echo -e "${GREEN}══ Pubblica da file Word ══${NC}"
  echo ""
  if [ -f "$HOME/pubblica-da-word.sh" ]; then
    bash "$HOME/pubblica-da-word.sh"
  else
    echo "Per convertire un file Word in Markdown:"
    echo ""
    echo -e "  1. Copia il file .docx nella tua home directory"
    echo ""
    echo -e "  2. Converti con pandoc:"
    echo -e "     ${BOLD}pandoc nomefile.docx -t markdown -o articolo.md${NC}"
    echo ""
    echo -e "  3. Rimuovi i backslash dagli apostrofi:"
    echo -e "     ${BOLD}sed -i \"s/\\\\\\\\'/'/g\" articolo.md${NC}"
    echo ""
    echo -e "  4. Aggiungi il frontmatter in cima al file (titolo, data, badge, ecc.)"
    echo ""
    echo -e "  5. Sposta il file nella cartella comunicazioni:"
    echo -e "     ${BOLD}mv articolo.md ~/sito-pc-genzano/content/comunicazioni/$(date +%Y-%m-%d)-titolo.md${NC}"
  fi
  ;;

# ══════════════════════════════════════════
# 3) MODIFICA COMUNICAZIONE
# ══════════════════════════════════════════
3)
  echo ""
  echo -e "${GREEN}══ Modifica comunicazione ══${NC}"
  echo ""
  echo "Comunicazioni disponibili:"
  echo ""
  ls -1 "$CONTENT_DIR/comunicazioni/" | grep -v "_index" | nl -ba
  echo ""
  read -p "Numero da modificare: " num
  file=$(ls -1 "$CONTENT_DIR/comunicazioni/" | grep -v "_index" | sed -n "${num}p")
  if [ -n "$file" ]; then
    echo ""
    echo -e "Apro: ${BOLD}$file${NC}"
    echo -e "${YELLOW}Ricorda: salva con Ctrl+O, esci con Ctrl+X${NC}"
    echo ""
    read -p "Premi INVIO per aprire..."
    nano "$CONTENT_DIR/comunicazioni/$file"
  else
    echo -e "${RED}Selezione non valida.${NC}"
  fi
  ;;

# ══════════════════════════════════════════
# 4) ELIMINA COMUNICAZIONE
# ══════════════════════════════════════════
4)
  echo ""
  echo -e "${RED}══ Elimina comunicazione ══${NC}"
  echo ""
  echo "Comunicazioni disponibili:"
  echo ""
  ls -1 "$CONTENT_DIR/comunicazioni/" | grep -v "_index" | nl -ba
  echo ""
  read -p "Numero da eliminare: " num
  file=$(ls -1 "$CONTENT_DIR/comunicazioni/" | grep -v "_index" | sed -n "${num}p")
  if [ -n "$file" ]; then
    echo ""
    echo -e "${RED}Stai per eliminare: $file${NC}"
    read -p "Sei sicuro? Scrivi 'elimina' per confermare: " conf
    if [ "$conf" = "elimina" ]; then
      rm "$CONTENT_DIR/comunicazioni/$file"
      echo -e "${GREEN}Eliminato.${NC}"
    else
      echo "Operazione annullata."
    fi
  else
    echo -e "${RED}Selezione non valida.${NC}"
  fi
  ;;

# ══════════════════════════════════════════
# 5) MODIFICA PAGINA
# ══════════════════════════════════════════
5)
  echo ""
  echo -e "${GREEN}══ Modifica pagina ══${NC}"
  echo ""
  echo "Pagine disponibili:"
  echo ""
  i=1
  pagine=()
  while IFS= read -r f; do
    sezione=$(echo "$f" | sed "s|$CONTENT_DIR/||" | sed 's|/_index.md||')
    echo "  $i) $sezione"
    pagine+=("$f")
    i=$((i+1))
  done < <(find "$CONTENT_DIR" -maxdepth 2 -name "_index.md" | sort)
  echo ""
  read -p "Numero da modificare: " num
  idx=$((num-1))
  if [ $idx -ge 0 ] && [ $idx -lt ${#pagine[@]} ]; then
    file="${pagine[$idx]}"
    echo ""
    echo -e "Apro: ${BOLD}$file${NC}"
    echo -e "${YELLOW}Ricorda: salva con Ctrl+O, esci con Ctrl+X${NC}"
    echo ""
    read -p "Premi INVIO per aprire..."
    nano "$file"
  else
    echo -e "${RED}Selezione non valida.${NC}"
  fi
  ;;

# ══════════════════════════════════════════
# 6) MODIFICA PAGINA RISCHIO
# ══════════════════════════════════════════
6)
  echo ""
  echo -e "${GREEN}══ Modifica pagina rischio ══${NC}"
  echo ""
  echo "Pagine rischio disponibili:"
  echo ""
  ls -1 "$CONTENT_DIR/rischi-prevenzione/" | grep -v "_index" | nl -ba
  echo ""
  read -p "Numero da modificare: " num
  file=$(ls -1 "$CONTENT_DIR/rischi-prevenzione/" | grep -v "_index" | sed -n "${num}p")
  if [ -n "$file" ]; then
    echo ""
    echo -e "Apro: ${BOLD}$file${NC}"
    echo -e "${YELLOW}Ricorda: salva con Ctrl+O, esci con Ctrl+X${NC}"
    echo ""
    read -p "Premi INVIO per aprire..."
    nano "$CONTENT_DIR/rischi-prevenzione/$file"
  else
    echo -e "${RED}Selezione non valida.${NC}"
  fi
  ;;

# ══════════════════════════════════════════
# 7) ALLERTA METEO
# ══════════════════════════════════════════
7)
  echo ""
  echo -e "${YELLOW}══ Imposta allerta meteo ══${NC}"
  echo ""
  echo "Livelli disponibili:"
  echo "  1) Verde — Nessuna allerta"
  echo "  2) Gialla — Attenzione"
  echo "  3) Arancione — Preallarme"
  echo "  4) Rossa — Allarme"
  echo ""
  read -p "Scegli [1-4]: " liv_num
  case $liv_num in
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
  echo ""
  echo "NOTA: il dato CSV del DPC ha priorità e sovrascrive"
  echo "questa impostazione manuale dopo 24 ore."
  ;;

# ══════════════════════════════════════════
# 8) PUBBLICA BANNER EMERGENZA
# ══════════════════════════════════════════
8)
  echo ""
  echo -e "${RED}══ Pubblica banner emergenza ══${NC}"
  echo ""
  echo -e "${YELLOW}ATTENZIONE: attivare l'emergenza riorganizza la homepage.${NC}"
  echo -e "${YELLOW}Il blocco 'Cosa fare adesso' comparirà in alto.${NC}"
  echo ""

  echo "Colore del banner:"
  echo "  1) Blu"
  echo "  2) Azzurro"
  echo "  3) Verde"
  echo "  4) Giallo"
  echo "  5) Arancione"
  echo "  6) Rosso"
  echo "  7) Viola"
  read -p "Scegli [1-7]: " tipo_num
  case $tipo_num in
    1) tipo="blu";; 2) tipo="azzurro";; 3) tipo="verde";; 4) tipo="giallo";;
    5) tipo="arancione";; 6) tipo="rosso";; 7) tipo="viola";; *) tipo="blu";;
  esac

  echo ""
  echo -e "${BOLD}Titolo del banner:${NC}"
  read -e -p "> " titolo

  echo ""
  echo -e "${BOLD}Descrizione (cosa sta succedendo):${NC}"
  read -e -p "> " desc

  echo ""
  echo -e "${BOLD}Link per maggiori informazioni (opzionale, lascia vuoto se non c'è):${NC}"
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
  echo -e "${GREEN}Banner emergenza ATTIVATO${NC}"
  echo -e "${GREEN}════════════════════════════════════════${NC}"
  echo ""
  echo "Per rendere visibile online:"
  echo -e "  ${BOLD}cd ~/sito-pc-genzano && git add . && git commit -m \"Emergenza attivata\" && git push${NC}"
  ;;

# ══════════════════════════════════════════
# 9) MODIFICA BANNER EMERGENZA
# ══════════════════════════════════════════
9)
  echo ""
  echo -e "${YELLOW}══ Modifica banner emergenza ══${NC}"
  echo ""
  echo "Contenuto attuale:"
  echo ""
  cat "$DATA_DIR/emergenza.json"
  echo ""
  echo -e "${YELLOW}Ricorda: salva con Ctrl+O, esci con Ctrl+X${NC}"
  read -p "Premi INVIO per aprire il file..."
  nano "$DATA_DIR/emergenza.json"
  ;;

# ══════════════════════════════════════════
# 10) REVOCA EMERGENZA
# ══════════════════════════════════════════
10)
  echo ""
  echo -e "${GREEN}══ Revoca banner emergenza ══${NC}"
  echo ""
  read -p "Confermi la disattivazione del banner? [S/n]: " conf
  if [ "$conf" = "n" ] || [ "$conf" = "N" ]; then
    echo "Operazione annullata."
  else
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
    echo ""
    echo -e "${GREEN}Banner emergenza DISATTIVATO.${NC}"
    echo -e "La homepage è tornata in modalità ordinaria."
    echo ""
    echo "Per rendere visibile online:"
    echo -e "  ${BOLD}cd ~/sito-pc-genzano && git add . && git commit -m \"Emergenza revocata\" && git push${NC}"
  fi
  ;;

# ══════════════════════════════════════════
# 11-12) STRUMENTI
# ══════════════════════════════════════════
11)
  echo ""
  echo -e "${GREEN}Apro Claude AI nel browser...${NC}"
  xdg-open "https://claude.ai" 2>/dev/null || echo "Vai su https://claude.ai"
  ;;

12)
  echo ""
  echo -e "${GREEN}Validatore Designers Italia...${NC}"
  if [ -f "$HOME/valida-contenuto.sh" ]; then
    bash "$HOME/valida-contenuto.sh"
  else
    xdg-open "https://designers.italia.it/modello/comuni/" 2>/dev/null || echo "Vai su https://designers.italia.it/modello/comuni/"
  fi
  ;;

# ══════════════════════════════════════════
# 13) TEST LOCALE
# ══════════════════════════════════════════
13)
  echo ""
  echo -e "${GREEN}══ Test locale ══${NC}"
  echo ""
  echo -e "Avvio il server locale Hugo."
  echo -e "Quando è pronto, apri nel browser: ${BOLD}http://localhost:1313/${NC}"
  echo -e "Per fermare il server: premi ${BOLD}Ctrl+C${NC}"
  echo ""
  read -p "Premi INVIO per avviare..."
  cd "$SITO_DIR"
  hugo server -D
  ;;

# ══════════════════════════════════════════
# 14) PUBBLICA MODIFICHE
# ══════════════════════════════════════════
14)
  echo ""
  echo -e "${GREEN}══ Pubblica modifiche online ══${NC}"
  echo ""
  cd "$SITO_DIR"

  # Mostra cosa è cambiato
  echo -e "${BOLD}File modificati:${NC}"
  git status --short
  echo ""

  # Chiedi conferma
  read -p "Vuoi procedere con la pubblicazione? [S/n]: " conf
  if [ "$conf" = "n" ] || [ "$conf" = "N" ]; then
    echo "Operazione annullata."
    read -p "Premi INVIO per tornare al menu..."
    exec bash "$0"
  fi

  # Messaggio di commit
  echo ""
  echo -e "${BOLD}Descrizione delle modifiche (es. 'Aggiornamento notizia'):${NC}"
  read -e -p "> " -i "Aggiornamento contenuti" msg
  msg=${msg:-"Aggiornamento contenuti"}

  echo ""
  echo "Pubblicazione in corso..."
  echo ""

  git add .
  git commit -m "$msg"
  git push

  echo ""
  echo -e "${GREEN}════════════════════════════════════════${NC}"
  echo -e "${GREEN}Pubblicato con successo!${NC}"
  echo -e "${GREEN}════════════════════════════════════════${NC}"
  echo ""
  echo "GitHub Actions sta aggiornando i siti."
  echo "Controlla lo stato su:"
  echo "  https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions"
  echo ""
  echo "I siti saranno aggiornati entro 2-3 minuti."
  ;;

# ══════════════════════════════════════════
# 15-17) MANUTENZIONE
# ══════════════════════════════════════════
15)
  echo ""
  echo -e "${GREEN}══ Aggiorna dipendenze ══${NC}"
  echo ""
  cd "$SITO_DIR"
  echo -n "Versione Bootstrap Italia attuale: "
  cat .bootstrap-italia-version 2>/dev/null || echo "Non trovata"
  echo ""
  echo "Il workflow controlla automaticamente ogni lunedì."
  echo "Per forzare: vai su GitHub Actions e lancia manualmente"
  echo "il workflow 'update-bootstrap-italia'."
  ;;

16)
  echo ""
  echo -e "${GREEN}══ Ultime 15 modifiche ══${NC}"
  echo ""
  cd "$SITO_DIR"
  git log --oneline -15
  ;;

17)
  echo ""
  echo -e "${GREEN}══ Stato repository ══${NC}"
  echo ""
  cd "$SITO_DIR"
  git status
  ;;

# ══════════════════════════════════════════
# 18-22) LINK RAPIDI
# ══════════════════════════════════════════
18) xdg-open "https://www.protezionecivilegenzano.it/" 2>/dev/null || echo "https://www.protezionecivilegenzano.it/" ;;
19) xdg-open "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions" 2>/dev/null || echo "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions" ;;
20) xdg-open "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano" 2>/dev/null || echo "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano" ;;
21) xdg-open "https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" 2>/dev/null || echo "Vai su protezionecivile.regione.lazio.it" ;;
22) xdg-open "https://activepager.com/auth/login" 2>/dev/null || echo "https://activepager.com/auth/login" ;;

# ══════════════════════════════════════════
# 23-25) GUIDE
# ══════════════════════════════════════════
23)
  echo ""
  echo -e "${GREEN}══ Guida alla pubblicazione ══${NC}"
  echo ""
  if [ -f "$HOME/GUIDA-PUBBLICAZIONE.txt" ]; then
    less "$HOME/GUIDA-PUBBLICAZIONE.txt"
  elif [ -f "$SITO_DIR/GUIDA-UPLOAD-V2.md" ]; then
    less "$SITO_DIR/GUIDA-UPLOAD-V2.md"
  else
    echo "File guida non trovato."
  fi
  ;;

24)
  echo ""
  echo -e "${GREEN}══ Checklist contenuti ══${NC}"
  echo ""
  if [ -f "$HOME/CHECKLIST-CONTENUTI.txt" ]; then
    less "$HOME/CHECKLIST-CONTENUTI.txt"
  else
    echo "Checklist rapida per ogni comunicazione:"
    echo ""
    echo "  [ ] Titolo chiaro e descrittivo"
    echo "  [ ] Data corretta"
    echo "  [ ] Badge corretto (Allerta/Avviso/Comunicazione/ecc.)"
    echo "  [ ] Descrizione breve compilata"
    echo "  [ ] Autore indicato"
    echo "  [ ] Testo senza errori"
    echo "  [ ] Link funzionanti"
    echo "  [ ] Immagine (se presente) in static/images/"
    echo "  [ ] Scadenza impostata (se la notizia è temporanea)"
    echo "  [ ] Test locale eseguito (hugo server)"
  fi
  ;;

25)
  echo ""
  echo -e "${GREEN}══ Struttura del sito ══${NC}"
  echo ""
  echo -e "${BOLD}MENU PRINCIPALE (7 voci):${NC}"
  echo "  Home | Chi Siamo | Rischi e Prevenzione | Allerte Meteo"
  echo "  Comunicazioni | Diventa Volontario | Contatti"
  echo ""
  echo -e "${BOLD}SEZIONI CONTENUTO:${NC}"
  echo "  content/chi-siamo/           — Chi Siamo"
  echo "  content/rischi-prevenzione/   — Hub 9 pagine rischio"
  echo "    rischio-sismico.md"
  echo "    rischio-idrogeologico.md"
  echo "    rischio-incendio.md"
  echo "    vento-forte.md"
  echo "    temporali-intensi.md"
  echo "    ondate-di-calore.md"
  echo "    blackout.md"
  echo "    kit-emergenza.md"
  echo "    persone-necessita-specifiche.md"
  echo "  content/allerte-meteo/        — Sistema allertamento"
  echo "  content/comunicazioni/        — Articoli e notizie"
  echo "  content/diventa-volontario/   — Reclutamento"
  echo "  content/contatti/             — Recapiti e sede"
  echo "  content/piano-emergenza/      — Piano Comunale"
  echo "  content/piano-familiare/      — Form interattivo"
  echo "  content/cartografia/          — Aree emergenza"
  echo "  content/area-download/        — Documenti PDF"
  echo "  content/cosa-fare-adesso/     — Azioni immediate"
  echo "  content/numeri-utili/         — Tutti i numeri"
  echo "  content/faq/                  — Domande frequenti"
  echo "  content/formazione/           — Corsi e scuole"
  echo "  content/siti-utili/           — Link esterni"
  echo ""
  echo -e "${BOLD}DATA FILES (dati semi-dinamici):${NC}"
  echo "  data/allerta.json             — Stato allerta"
  echo "  data/emergenza.json           — Banner emergenza"
  echo "  data/numeri_utili.yaml        — Numeri telefono"
  echo "  data/quick_links.yaml         — Link rapidi homepage"
  echo "  data/risk_cards.yaml          — Card rischi"
  echo "  data/social_links.yaml        — Social"
  echo "  data/codici_colore.yaml       — Codici allerta"
  echo ""
  echo -e "${BOLD}BADGE COMUNICAZIONI:${NC}"
  echo "  Allerta | Avviso | Comunicazione | Attività"
  echo "  Formazione | Evento | Volontariato"
  echo ""
  echo -e "${BOLD}PARAMETRI ARTICOLI:${NC}"
  echo "  title       — Titolo (obbligatorio)"
  echo "  date        — Data pubblicazione (obbligatorio)"
  echo "  badge       — Tipo comunicazione (obbligatorio)"
  echo "  description — Breve descrizione (obbligatorio)"
  echo "  priorita    — 'normale' o 'urgente'"
  echo "  autore      — Chi ha scritto/approvato"
  echo "  image       — Immagine copertina"
  echo "  area        — Zona geografica interessata"
  echo "  scadenza    — Data dopo la quale è 'scaduta'"
  echo "  allegati    — Lista PDF allegati"
  ;;

# ══════════════════════════════════════════
# 0) ESCI
# ══════════════════════════════════════════
0)
  echo ""
  echo -e "${GREEN}Arrivederci!${NC}"
  exit 0
  ;;

*)
  echo ""
  echo -e "${RED}Opzione non valida. Riprova.${NC}"
  ;;

esac

echo ""
read -p "Premi INVIO per tornare al menu..."
exec bash "$0"
