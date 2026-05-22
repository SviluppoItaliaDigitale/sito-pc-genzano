#!/bin/bash
# ============================================================
# GESTIONE SITO — Protezione Civile Genzano di Roma
# v3.0 — 22 maggio 2026
# Changelog v3.0:
#   - REINTRODOTTA la sezione BOZZE (voci 5-8): Crea, Modifica,
#     Pubblica, Elimina. Architettura NUOVA rispetto al passato:
#     le bozze NON stanno più in content/ con draft:true (pattern
#     vietato dalla regola di progetto, le bozze si accumulavano
#     dimenticate e rischiavano di andare live). Ora vivono nella
#     cartella bozze/ alla radice del repo, che Hugo NON costruisce
#     mai (come riferimenti-interni/) → zero rischio di pubblicazione
#     accidentale. "Pubblica bozza" sposta il file in
#     content/comunicazioni/<data>-<slug>.md con draft:false.
#   - MENU RIORDINATO E RINUMERATO da 1 a 30 in ordine coerente:
#     prima la numerazione saltava (24/25/26 dopo 21, GUIDE a 22/23,
#     prompt "[0-23]" mentre esistevano voci fino a 26).
#   - Aggiunto contatore "📝 Bozze in lavorazione: N" nell'header.
#   - Aggiornati i riferimenti incrociati tra voci (es. "per
#     pubblicare: voce 17") alla nuova numerazione.
#
# Changelog v2.9 (9 maggio 2026):
#   - voce contesto AI: git pull --ff-only automatico all'inizio.
# Changelog v2.8 (9 maggio 2026):
#   - export contesto AI adattato ai limiti di Gemini/ChatGPT/Claude.
# Changelog v2.7 (9 maggio 2026):
#   - rimossa sezione BOZZE (regola "niente articoli in revisione").
#     [Ripristinata in v3.0 con architettura fuori da content/.]
# Changelog v2.6/2.5 (apr-mag 2026):
#   - descrizioni voci, smoke test, struttura sito, guida.
# ============================================================

SITO_DIR="$HOME/sito-pc-genzano"
CONTENT_DIR="$SITO_DIR/content"
DATA_DIR="$SITO_DIR/data"
BOZZE_DIR="$SITO_DIR/bozze"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

lista_comunicazioni() {
  local files=()
  for f in "$CONTENT_DIR/comunicazioni/"*.md; do
    [ "$(basename "$f")" = "_index.md" ] && continue
    [ ! -f "$f" ] && continue
    files+=("$(basename "$f")")
  done
  echo "${files[@]}"
}

# Funzione: lista delle bozze (file in bozze/, escluso README)
lista_bozze() {
  local files=()
  for f in "$BOZZE_DIR/"*.md; do
    [ ! -f "$f" ] && continue
    [ "$(basename "$f")" = "README.md" ] && continue
    files+=("$(basename "$f")")
  done
  echo "${files[@]}"
}

# Funzione: conta le bozze in lavorazione (per l'header del menu)
conta_bozze() {
  local count=0
  for f in "$BOZZE_DIR/"*.md; do
    [ ! -f "$f" ] && continue
    [ "$(basename "$f")" = "README.md" ] && continue
    count=$((count+1))
  done
  echo "$count"
}

# Funzione: mostra TUTTE le pagine del sito (index + sottopagine)
lista_tutte_pagine() {
  find "$CONTENT_DIR" -name "*.md" ! -path "*/comunicazioni/*" | sort
}

mostra_menu() {
  clear
  echo -e "${BLUE}${BOLD}"
  echo "╔══════════════════════════════════════════════════════════╗"
  echo "║   GESTIONE SITO — Protezione Civile Genzano di Roma    ║"
  echo "║   v3.0 — $(date '+%d/%m/%Y %H:%M')                              ║"
  echo "╚══════════════════════════════════════════════════════════╝"
  echo -e "${NC}"

  if [ -f "$DATA_DIR/emergenza.json" ]; then
    stato_em=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print('ATTIVA — '+d.get('titolo','') if d.get('attiva') else 'sospesa' if d.get('titolo','') else 'disattivata')" 2>/dev/null)
    if echo "$stato_em" | grep -q "ATTIVA"; then
      echo -e "  ${RED}${BOLD}⚠ EMERGENZA: $stato_em${NC}"
    else
      echo -e "  Emergenza: $stato_em"
    fi
  fi
  nbozze=$(conta_bozze)
  [ "$nbozze" -gt 0 ] && echo -e "  ${YELLOW}📝 Bozze in lavorazione: $nbozze${NC}"
  echo ""

  echo -e "${CYAN}── COMUNICAZIONI ──${NC}"
  echo "  1) Crea nuova comunicazione         (nuovo articolo guidato — pubblicato o calendarizzato)"
  echo "  2) Crea comunicazione da file Word  (mostra i comandi pandoc per convertire un .docx)"
  echo "  3) Modifica comunicazione           (apre con nano un articolo del sito)"
  echo "  4) Elimina comunicazione            (cancella definitivamente un articolo)"
  echo ""
  echo -e "${CYAN}── BOZZE (lavori in corso, mai online) ──${NC}"
  echo "  5) Crea bozza                       (scrivi con calma in bozze/, fuori dal sito)"
  echo "  6) Modifica bozza                   (apre con nano una bozza esistente)"
  echo "  7) Pubblica bozza                   (sposta la bozza in comunicazioni/ con la data scelta)"
  echo "  8) Elimina bozza                    (cancella una bozza in lavorazione)"
  echo ""
  echo -e "${CYAN}── PAGINE ──${NC}"
  echo "  9) Modifica qualsiasi pagina        (apre con nano una pagina del sito, escluse le comunicazioni)"
  echo " 10) Crea nuova pagina                (genera content/<sezione>/_index.md con frontmatter base)"
  echo " 11) Elimina pagina                   (cancella una pagina del sito — attento alle pagine principali)"
  echo ""
  echo -e "${CYAN}── EMERGENZA ──${NC}"
  echo " 12) Attiva emergenza                 (mostra il banner rosso in homepage e attiva la modalità)"
  echo " 13) Modifica emergenza attiva        (apre data/emergenza.json con nano per ritoccare i testi)"
  echo " 14) Sospendi emergenza               (nasconde il banner; i dati restano per riattivarla dopo)"
  echo ""
  echo -e "${CYAN}── ALLERTA METEO ──${NC}"
  echo " 15) Imposta livello allerta          (scrive data/allerta.json: verde / gialla / arancione / rossa)"
  echo ""
  echo -e "${CYAN}── PUBBLICA E TESTA ──${NC}"
  echo " 16) Test sito in locale              (hugo server su http://localhost:1313)"
  echo " 17) Pubblica modifiche online        (git add+commit+push → deploy Aruba in 2-3 minuti)"
  echo " 18) Stato repository                 (git status + ultimi 10 commit)"
  echo ""
  echo -e "${CYAN}── LINK RAPIDI ──${NC}"
  echo " 19) Sito produzione                  (apre https://www.protezionecivilegenzano.it/)"
  echo " 20) GitHub Actions                   (stato dei deploy e dei workflow automatici)"
  echo " 21) Repository GitHub                (codice sorgente del sito)"
  echo " 22) Bollettino Lazio                 (Centro Funzionale Regionale: allerte ufficiali)"
  echo " 23) Smoke test sito                  (verifica che le pagine principali rispondano 200 OK)"
  echo " 24) Avvia Claude Code                (lancia l'assistente AI in questo progetto, /exit per tornare)"
  echo ""
  echo -e "${CYAN}── ALTRE AI (Gemini, ChatGPT, Claude web) ──${NC}"
  echo " 25) Esporta contesto per altra AI    (scegli AI → genera + copia in appunti + apre il sito)"
  echo ""
  echo -e "${CYAN}── SOCIAL (assistito, human-in-the-loop) ──${NC}"
  echo " 26) Pubblica bozze social di un articolo  (apre 4 tab + appunti, tu fai Ctrl+V e Pubblica)"
  echo " 27) Stato opencli                         (verifica daemon + estensione Chrome + livello B)"
  echo ""
  echo -e "${CYAN}── SLIDE E PDF (open-design, locale) ──${NC}"
  echo " 28) Avvia open-design (web UI locale)     (slide deck, brochure, mockup per formazione/scuole)"
  echo ""
  echo -e "${CYAN}── GUIDE ──${NC}"
  echo " 29) Struttura del sito               (panoramica menu, badge, workflow, data files)"
  echo " 30) Guida pubblicazione              (apre MANUALE-SITO.md con less)"
  echo ""
  echo -e "${YELLOW}  0) Esci${NC}                              (chiude il menu e torna al terminale)"
  echo ""
}

# ══════════════════════════════════════════
mostra_menu
echo -ne "${BOLD}Scegli [0-30]: ${NC}"
read scelta

case $scelta in

# ══════════════════════════════════════════
# 1) CREA COMUNICAZIONE (sempre draft:false)
# ══════════════════════════════════════════
1)
  echo ""
  echo -e "${GREEN}══ Nuova comunicazione ══${NC}"
  echo ""
  echo -e "${YELLOW}Nota: gli articoli sono sempre pubblicati (draft:false).${NC}"
  echo -e "${YELLOW}Per pubblicare in futuro, scegli una data avanti nel tempo.${NC}"
  echo -e "${YELLOW}Se vuoi solo abbozzarlo senza mandarlo online, usa la voce 5 (Crea bozza).${NC}"
  echo ""
  echo -e "${YELLOW}Puoi usare le frecce ← → per muovere il cursore.${NC}"
  echo ""

  echo -e "${BOLD}Titolo:${NC}"
  read -e -p "> " titolo
  [ -z "$titolo" ] && { echo -e "${RED}Titolo obbligatorio.${NC}"; read -p "Premi INVIO..."; exec bash "$0"; }

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

  echo -e "${BOLD}Descrizione breve:${NC}"
  read -e -p "> " desc

  echo -e "${BOLD}Autore:${NC}"
  read -e -p "> " -i "Gruppo Comunale Volontari PC Genzano" autore

  echo -e "${BOLD}Area interessata (opzionale):${NC}"
  read -e -p "> " area

  echo -e "${BOLD}Data scadenza (opzionale, AAAA-MM-GG):${NC}"
  read -e -p "> " scadenza

  echo -e "${BOLD}Immagine (opzionale, lascia vuoto per cover automatica):${NC}"
  read -e -p "> " image

  echo ""
  echo -e "${BOLD}Data di pubblicazione:${NC}"
  echo -e "${YELLOW}  - INVIO per pubblicare oggi"
  echo -e "  - AAAA-MM-GG futura per calendarizzare (auto-pubblicata quel giorno)${NC}"
  read -e -p "> " data_input
  if [ -z "$data_input" ]; then
    data=$(date +%Y-%m-%d)
  else
    data="$data_input"
  fi

  slug=$(echo "$titolo" | tr '[:upper:]' '[:lower:]' | sed 's/à/a/g;s/è/e/g;s/é/e/g;s/ì/i/g;s/ò/o/g;s/ù/u/g' | sed 's/ /-/g;s/[^a-z0-9-]//g;s/--*/-/g;s/^-//;s/-$//')
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
  oggi=$(date +%Y-%m-%d)
  if [ "$data" \> "$oggi" ]; then
    echo -e "${GREEN}Articolo CALENDARIZZATO per $data.${NC}"
    echo -e "Andrà online automaticamente quel giorno (workflow pubblica-programmata)."
  else
    echo -e "${GREEN}Articolo PUBBLICATO (data: $data).${NC}"
    echo -e "Per mandarlo online: opzione ${BOLD}17${NC}."
  fi
  echo -e "File: ${BOLD}$file${NC}"
  echo ""
  read -p "Aprire con nano? [S/n]: " apri
  [ "$apri" != "n" ] && [ "$apri" != "N" ] && nano "$file"
  ;;

# ══════════════════════════════════════════
# 2) DA WORD
# ══════════════════════════════════════════
2)
  echo ""
  echo "Comandi da eseguire:"
  echo -e "  1. ${BOLD}pandoc nomefile.docx -t markdown -o articolo.md${NC}"
  echo -e "  2. ${BOLD}sed -i \"s/\\\\\\\\'/'/g\" articolo.md${NC}"
  echo "  3. Usa opzione 1 (o 5 per una bozza) per creare il file, poi incolla il contenuto."
  ;;

# ══════════════════════════════════════════
# 3) MODIFICA COMUNICAZIONE
# ══════════════════════════════════════════
3)
  echo ""
  echo -e "${GREEN}══ Modifica comunicazione ══${NC}"
  echo ""
  IFS=' ' read -ra files <<< "$(lista_comunicazioni)"
  if [ ${#files[@]} -eq 0 ]; then echo "Nessuna comunicazione."
  else
    for i in "${!files[@]}"; do echo "  $((i+1))) ${files[$i]}"; done
    echo ""
    read -p "Numero: " num; idx=$((num-1))
    if [ $idx -ge 0 ] && [ $idx -lt ${#files[@]} ]; then
      echo -e "${YELLOW}Salva: Ctrl+O → INVIO — Esci: Ctrl+X${NC}"
      read -p "Premi INVIO..."
      nano "$CONTENT_DIR/comunicazioni/${files[$idx]}"
    else echo -e "${RED}Non valida.${NC}"; fi
  fi
  ;;

# ══════════════════════════════════════════
# 4) ELIMINA COMUNICAZIONE
# ══════════════════════════════════════════
4)
  echo ""
  echo -e "${RED}══ Elimina comunicazione ══${NC}"
  echo ""
  IFS=' ' read -ra files <<< "$(lista_comunicazioni)"
  if [ ${#files[@]} -eq 0 ]; then echo "Nessuna comunicazione."
  else
    for i in "${!files[@]}"; do echo "  $((i+1))) ${files[$i]}"; done
    echo ""
    read -p "Numero: " num; idx=$((num-1))
    if [ $idx -ge 0 ] && [ $idx -lt ${#files[@]} ]; then
      echo -e "${RED}Eliminare: ${files[$idx]}?${NC}"
      read -p "Scrivi 'elimina': " conf
      [ "$conf" = "elimina" ] && { rm "$CONTENT_DIR/comunicazioni/${files[$idx]}"; echo -e "${GREEN}Eliminato.${NC}"; } || echo "Annullato."
    else echo -e "${RED}Non valida.${NC}"; fi
  fi
  ;;

# ══════════════════════════════════════════
# 5) CREA BOZZA (in bozze/, fuori dal sito)
# ══════════════════════════════════════════
5)
  echo ""
  echo -e "${GREEN}══ Nuova bozza ══${NC}"
  echo ""
  echo -e "${YELLOW}Le bozze restano in bozze/ (fuori dal sito): non vanno MAI online${NC}"
  echo -e "${YELLOW}finché non le pubblichi con la voce 7 (Pubblica bozza).${NC}"
  echo ""
  mkdir -p "$BOZZE_DIR"

  echo -e "${BOLD}Titolo:${NC}"
  read -e -p "> " titolo
  [ -z "$titolo" ] && { echo -e "${RED}Titolo obbligatorio.${NC}"; read -p "Premi INVIO..."; exec bash "$0"; }

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

  echo -e "${BOLD}Descrizione breve:${NC}"
  read -e -p "> " desc

  echo -e "${BOLD}Autore:${NC}"
  read -e -p "> " -i "Gruppo Comunale Volontari PC Genzano" autore

  echo -e "${BOLD}Area interessata (opzionale):${NC}"
  read -e -p "> " area

  slug=$(echo "$titolo" | tr '[:upper:]' '[:lower:]' | sed 's/à/a/g;s/è/e/g;s/é/e/g;s/ì/i/g;s/ò/o/g;s/ù/u/g' | sed 's/ /-/g;s/[^a-z0-9-]//g;s/--*/-/g;s/^-//;s/-$//')
  [ -z "$slug" ] && slug="bozza-$(date +%Y%m%d-%H%M%S)"
  file="$BOZZE_DIR/${slug}.md"

  if [ -f "$file" ]; then
    echo ""
    echo -e "${YELLOW}Esiste già una bozza con questo nome: ${slug}.md${NC}"
    read -p "Sovrascrivere? [s/N]: " sov
    [ "$sov" != "s" ] && [ "$sov" != "S" ] && { echo "Annullato."; read -p "Premi INVIO..."; exec bash "$0"; }
  fi

  cat > "$file" << EOF
---
title: "$titolo"
date: $(date +%Y-%m-%d)
badge: "$badge"
priorita: "$priorita"
autore: "$autore"
description: "$desc"
image: ""
area: "$area"
scadenza: ""
allegati: []
draft: false
---

Scrivi qui il contenuto della comunicazione.
EOF

  echo ""
  echo -e "${GREEN}Bozza creata: bozze/${slug}.md${NC}"
  echo -e "${YELLOW}Non è online. Quando è pronta: voce 7 (Pubblica bozza).${NC}"
  echo -e "${YELLOW}La data verrà scelta al momento della pubblicazione.${NC}"
  echo ""
  read -p "Aprire con nano? [S/n]: " apri
  [ "$apri" != "n" ] && [ "$apri" != "N" ] && nano "$file"
  ;;

# ══════════════════════════════════════════
# 6) MODIFICA BOZZA
# ══════════════════════════════════════════
6)
  echo ""
  echo -e "${GREEN}══ Modifica bozza ══${NC}"
  echo ""
  IFS=' ' read -ra files <<< "$(lista_bozze)"
  if [ ${#files[@]} -eq 0 ]; then echo "Nessuna bozza in lavorazione. Creane una con la voce 5."
  else
    for i in "${!files[@]}"; do echo "  $((i+1))) ${files[$i]}"; done
    echo ""
    read -p "Numero: " num; idx=$((num-1))
    if [ $idx -ge 0 ] && [ $idx -lt ${#files[@]} ]; then
      echo -e "${YELLOW}Salva: Ctrl+O → INVIO — Esci: Ctrl+X${NC}"
      read -p "Premi INVIO..."
      nano "$BOZZE_DIR/${files[$idx]}"
    else echo -e "${RED}Non valida.${NC}"; fi
  fi
  ;;

# ══════════════════════════════════════════
# 7) PUBBLICA BOZZA (sposta in content/comunicazioni)
# ══════════════════════════════════════════
7)
  echo ""
  echo -e "${GREEN}══ Pubblica bozza ══${NC}"
  echo ""
  IFS=' ' read -ra files <<< "$(lista_bozze)"
  if [ ${#files[@]} -eq 0 ]; then echo "Nessuna bozza da pubblicare. Creane una con la voce 5."; read -p "Premi INVIO..."; exec bash "$0"; fi
  for i in "${!files[@]}"; do echo "  $((i+1))) ${files[$i]}"; done
  echo ""
  read -p "Numero: " num; idx=$((num-1))
  if [ $idx -lt 0 ] || [ $idx -ge ${#files[@]} ]; then echo -e "${RED}Non valida.${NC}"; read -p "Premi INVIO..."; exec bash "$0"; fi

  bozza="${files[$idx]}"
  slug="${bozza%.md}"
  # togli eventuale prefisso data dal nome della bozza, se l'utente l'ha messo
  slug=$(echo "$slug" | sed 's/^[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}-//')

  echo ""
  echo -e "${BOLD}Data di pubblicazione:${NC}"
  echo -e "${YELLOW}  - INVIO per pubblicare oggi"
  echo -e "  - AAAA-MM-GG futura per calendarizzare (auto-pubblicata quel giorno)${NC}"
  read -e -p "> " data_input
  if [ -z "$data_input" ]; then
    data=$(date +%Y-%m-%d)
  else
    if ! echo "$data_input" | grep -qE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'; then
      echo -e "${RED}Formato data non valido (serve AAAA-MM-GG).${NC}"; read -p "Premi INVIO..."; exec bash "$0"
    fi
    data="$data_input"
  fi

  dest="$CONTENT_DIR/comunicazioni/${data}-${slug}.md"
  if [ -f "$dest" ]; then
    echo -e "${RED}Esiste già un articolo: ${data}-${slug}.md${NC}"
    read -p "Sovrascrivere? [s/N]: " sov
    [ "$sov" != "s" ] && [ "$sov" != "S" ] && { echo "Annullato."; read -p "Premi INVIO..."; exec bash "$0"; }
  fi

  # allinea il campo date e assicura draft:false nel frontmatter
  sed -i "s/^date:.*/date: $data/" "$BOZZE_DIR/$bozza"
  sed -i "s/^draft:.*/draft: false/" "$BOZZE_DIR/$bozza"

  mv "$BOZZE_DIR/$bozza" "$dest"

  echo ""
  oggi=$(date +%Y-%m-%d)
  if [ "$data" \> "$oggi" ]; then
    echo -e "${GREEN}Bozza CALENDARIZZATA per $data.${NC}"
    echo -e "Andrà online automaticamente quel giorno (workflow pubblica-programmata)."
  else
    echo -e "${GREEN}Bozza PUBBLICATA (data: $data).${NC}"
  fi
  echo -e "Articolo: ${BOLD}content/comunicazioni/${data}-${slug}.md${NC}"
  echo -e "${YELLOW}Per mandarlo online sul sito: voce 17 (Pubblica modifiche online).${NC}"
  echo ""
  read -p "Aprire l'articolo con nano per una rilettura? [s/N]: " apri
  [ "$apri" = "s" ] || [ "$apri" = "S" ] && nano "$dest"
  ;;

# ══════════════════════════════════════════
# 8) ELIMINA BOZZA
# ══════════════════════════════════════════
8)
  echo ""
  echo -e "${RED}══ Elimina bozza ══${NC}"
  echo ""
  IFS=' ' read -ra files <<< "$(lista_bozze)"
  if [ ${#files[@]} -eq 0 ]; then echo "Nessuna bozza."
  else
    for i in "${!files[@]}"; do echo "  $((i+1))) ${files[$i]}"; done
    echo ""
    read -p "Numero: " num; idx=$((num-1))
    if [ $idx -ge 0 ] && [ $idx -lt ${#files[@]} ]; then
      echo -e "${RED}Eliminare la bozza: ${files[$idx]}?${NC}"
      read -p "Scrivi 'elimina': " conf
      [ "$conf" = "elimina" ] && { rm "$BOZZE_DIR/${files[$idx]}"; echo -e "${GREEN}Eliminata.${NC}"; } || echo "Annullato."
    else echo -e "${RED}Non valida.${NC}"; fi
  fi
  ;;

# ══════════════════════════════════════════
# 9) MODIFICA QUALSIASI PAGINA
# ══════════════════════════════════════════
9)
  echo ""
  echo -e "${GREEN}══ Modifica pagina ══${NC}"
  echo ""
  echo -e "${BOLD}Tutte le pagine del sito:${NC}"
  echo ""
  pagine=()
  nomi=()
  while IFS= read -r f; do
    relpath=$(echo "$f" | sed "s|$CONTENT_DIR/||")
    pagine+=("$f")
    nomi+=("$relpath")
  done < <(lista_tutte_pagine)

  for i in "${!nomi[@]}"; do
    echo "  $((i+1))) ${nomi[$i]}"
  done
  echo ""
  read -p "Numero: " num; idx=$((num-1))
  if [ $idx -ge 0 ] && [ $idx -lt ${#pagine[@]} ]; then
    echo ""
    echo -e "Apro: ${BOLD}${nomi[$idx]}${NC}"
    echo -e "${YELLOW}Salva: Ctrl+O → INVIO — Esci: Ctrl+X${NC}"
    read -p "Premi INVIO..."
    nano "${pagine[$idx]}"
  else
    echo -e "${RED}Selezione non valida.${NC}"
  fi
  ;;

# ══════════════════════════════════════════
# 10) CREA PAGINA
# ══════════════════════════════════════════
10)
  echo ""
  echo -e "${GREEN}══ Crea nuova pagina ══${NC}"
  echo ""
  echo -e "${BOLD}Nome sezione (URL, es. 'avvisi-neve'):${NC}"
  echo -e "${YELLOW}Minuscole e trattini, no spazi no accenti.${NC}"
  read -e -p "> " sezione
  [ -z "$sezione" ] && { echo -e "${RED}Nome obbligatorio.${NC}"; read -p "INVIO..."; exec bash "$0"; }

  echo -e "${BOLD}Titolo:${NC}"
  read -e -p "> " titolo

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
  echo -e "${GREEN}Creata: content/$sezione/_index.md → URL: /$sezione/${NC}"
  read -p "Aprire con nano? [S/n]: " apri
  [ "$apri" != "n" ] && [ "$apri" != "N" ] && nano "$CONTENT_DIR/$sezione/_index.md"
  ;;

# ══════════════════════════════════════════
# 11) ELIMINA PAGINA
# ══════════════════════════════════════════
11)
  echo ""
  echo -e "${RED}══ Elimina pagina ══${NC}"
  echo -e "${YELLOW}Non eliminare le pagine principali del sito!${NC}"
  echo ""
  pagine=(); nomi=()
  while IFS= read -r f; do
    relpath=$(echo "$f" | sed "s|$CONTENT_DIR/||")
    pagine+=("$f"); nomi+=("$relpath")
  done < <(lista_tutte_pagine)
  for i in "${!nomi[@]}"; do echo "  $((i+1))) ${nomi[$i]}"; done
  echo ""
  read -p "Numero: " num; idx=$((num-1))
  if [ $idx -ge 0 ] && [ $idx -lt ${#pagine[@]} ]; then
    echo -e "${RED}Eliminare: ${nomi[$idx]}?${NC}"
    read -p "Scrivi 'elimina': " conf
    if [ "$conf" = "elimina" ]; then
      rm -f "${pagine[$idx]}"
      dir=$(dirname "${pagine[$idx]}")
      [ -d "$dir" ] && [ -z "$(ls -A "$dir")" ] && rmdir "$dir"
      echo -e "${GREEN}Eliminato.${NC}"
    else echo "Annullato."; fi
  else echo -e "${RED}Non valida.${NC}"; fi
  ;;

# ══════════════════════════════════════════
# 12) ATTIVA EMERGENZA
# ══════════════════════════════════════════
12)
  echo ""
  echo -e "${RED}══ Attiva emergenza ══${NC}"
  echo ""
  titolo_esistente=""; attiva_esistente="False"
  if [ -f "$DATA_DIR/emergenza.json" ]; then
    titolo_esistente=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('titolo',''))" 2>/dev/null)
    attiva_esistente=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('attiva',False))" 2>/dev/null)
  fi

  if [ "$attiva_esistente" = "True" ]; then
    echo -e "${YELLOW}Già attiva! Usa 13 per modificare o 14 per sospendere.${NC}"
    read -p "INVIO..."; exec bash "$0"
  fi

  if [ -n "$titolo_esistente" ] && [ "$titolo_esistente" != "" ]; then
    echo -e "Sospesa trovata: ${BOLD}$titolo_esistente${NC}"
    echo "  1) Riattiva questa   2) Creane una nuova"
    read -p "Scegli [1-2]: " riattiva
    if [ "$riattiva" = "1" ]; then
      python3 -c "
import json
with open('$DATA_DIR/emergenza.json','r') as f: d=json.load(f)
d['attiva']=True; d['ultimo_aggiornamento']='$(date -Is)'
with open('$DATA_DIR/emergenza.json','w') as f: json.dump(d,f,indent=2,ensure_ascii=False)"
      echo -e "${GREEN}RIATTIVATA! Per pubblicare: opzione 17.${NC}"
      read -p "INVIO..."; exec bash "$0"
    fi
  fi

  echo "Colore:  1)Blu 2)Azzurro 3)Verde 4)Giallo 5)Arancione 6)Rosso 7)Viola"
  read -p "Scegli [1-7]: " tn
  case $tn in 1)tipo="blu";;2)tipo="azzurro";;3)tipo="verde";;4)tipo="giallo";;5)tipo="arancione";;6)tipo="rosso";;7)tipo="viola";;*)tipo="blu";;esac

  echo -e "${BOLD}Titolo:${NC}"; read -e -p "> " titolo
  echo -e "${BOLD}Descrizione:${NC}"; read -e -p "> " desc
  echo -e "${BOLD}Link (opzionale):${NC}"; read -e -p "> " link

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
  echo -e "${GREEN}ATTIVATA! Per pubblicare: opzione 17.${NC}"
  ;;

# ══════════════════════════════════════════
# 13) MODIFICA EMERGENZA
# ══════════════════════════════════════════
13)
  echo ""; cat "$DATA_DIR/emergenza.json"; echo ""
  echo -e "${YELLOW}Salva: Ctrl+O → INVIO — Esci: Ctrl+X${NC}"
  read -p "INVIO..."; nano "$DATA_DIR/emergenza.json"
  ;;

# ══════════════════════════════════════════
# 14) SOSPENDI EMERGENZA
# ══════════════════════════════════════════
14)
  echo ""
  attiva_em=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('attiva',False))" 2>/dev/null)
  if [ "$attiva_em" != "True" ]; then echo "Non attiva."; read -p "INVIO..."; exec bash "$0"; fi
  titolo_em=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('titolo',''))" 2>/dev/null)
  echo -e "Sospendere: ${BOLD}$titolo_em${NC}?"
  echo -e "${YELLOW}I dati restano. Riattivabile con opzione 12.${NC}"
  read -p "Confermi? [S/n]: " conf
  if [ "$conf" != "n" ] && [ "$conf" != "N" ]; then
    python3 -c "
import json
with open('$DATA_DIR/emergenza.json','r') as f: d=json.load(f)
d['attiva']=False
with open('$DATA_DIR/emergenza.json','w') as f: json.dump(d,f,indent=2,ensure_ascii=False)"
    echo -e "${GREEN}SOSPESA. Per pubblicare: opzione 17.${NC}"
  else echo "Annullato."; fi
  ;;

# ══════════════════════════════════════════
# 15) ALLERTA
# ══════════════════════════════════════════
15)
  echo ""
  echo "  1) Verde   2) Gialla   3) Arancione   4) Rossa"
  read -p "Scegli [1-4]: " ln
  case $ln in
    1) livello="verde";titolo="NESSUNA ALLERTA";desc="Non sono previsti fenomeni significativi sul nostro territorio.";;
    2) livello="gialla";titolo="ALLERTA GIALLA";desc="Criticità ordinaria. Prestare attenzione.";;
    3) livello="arancione";titolo="ALLERTA ARANCIONE";desc="Criticità moderata. Limitare gli spostamenti.";;
    4) livello="rossa";titolo="ALLERTA ROSSA";desc="Criticità elevata. Seguire le indicazioni delle autorità.";;
    *) echo -e "${RED}Non valida.${NC}"; read -p "INVIO..."; exec bash "$0";;
  esac
  cat > "$DATA_DIR/allerta.json" << EOF
{
  "livello": "$livello",
  "titolo": "$titolo",
  "descrizione": "$desc",
  "ultimo_aggiornamento": "$(date -Is)"
}
EOF
  echo -e "${GREEN}Allerta: $titolo${NC}"
  ;;

# ══════════════════════════════════════════
# 16) TEST SITO IN LOCALE
# ══════════════════════════════════════════
16)
  echo -e "Browser: ${BOLD}http://localhost:1313/${NC}  Ferma: ${BOLD}Ctrl+C${NC}"
  read -p "INVIO per avviare..."
  cd "$SITO_DIR" && hugo server
  ;;

# ══════════════════════════════════════════
# 17) PUBBLICA
# ══════════════════════════════════════════
17)
  echo ""
  cd "$SITO_DIR"
  echo -e "${BOLD}File modificati:${NC}"
  git status --short
  echo ""
  modifiche=$(git status --short | wc -l)
  [ "$modifiche" -eq 0 ] && { echo "Nessuna modifica."; read -p "INVIO..."; exec bash "$0"; }

  read -p "Procedere? [S/n]: " conf
  [ "$conf" = "n" ] || [ "$conf" = "N" ] && { echo "Annullato."; read -p "INVIO..."; exec bash "$0"; }

  echo -e "${BOLD}Descrizione:${NC}"
  read -e -p "> " -i "Aggiornamento contenuti" msg

  git add . && git commit -m "$msg" && git push
  if [ $? -eq 0 ]; then
    echo -e "${GREEN}Pubblicato! Siti aggiornati entro 2-3 min.${NC}"
    echo -e "${YELLOW}Apri il sito e premi Ctrl+F5 per vedere le modifiche.${NC}"
  else
    echo -e "${RED}Errore! Prova: git pull --rebase && git push${NC}"
  fi
  ;;

# ══════════════════════════════════════════
# 18) STATO
# ══════════════════════════════════════════
18) cd "$SITO_DIR"; echo ""; git status; echo ""; echo -e "${BOLD}Ultime 10:${NC}"; git log --oneline -10 ;;

# ══════════════════════════════════════════
# 19-24) LINK RAPIDI
# ══════════════════════════════════════════
19) xdg-open "https://www.protezionecivilegenzano.it/" 2>/dev/null || echo "protezionecivilegenzano.it" ;;
20) xdg-open "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions" 2>/dev/null ;;
21) xdg-open "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano" 2>/dev/null ;;
22) xdg-open "https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" 2>/dev/null ;;
23)
  if [ -x "$SITO_DIR/scripts/smoke-test-live.sh" ]; then
    echo ""
    echo -e "${CYAN}══ Smoke test sito live ══${NC}"
    bash "$SITO_DIR/scripts/smoke-test-live.sh"
    echo ""
    read -p "Premi INVIO per tornare al menu..."
  else
    echo -e "${RED}Script smoke-test-live.sh non trovato in $SITO_DIR/scripts/.${NC}"
  fi
  ;;
24)
  echo ""
  echo "Avvio Claude Code nel progetto Sito PC Genzano..."
  echo "(per uscire scrivi /exit, tornerai a questo menu)"
  echo ""
  cd ~/sito-pc-genzano && claude
  ;;

# ══════════════════════════════════════════
# 25) ESPORTA CONTESTO PER ALTRA AI
#     (Gemini, ChatGPT, Claude web)
#
# Ogni AI ha un limite di contesto diverso, quindi la procedura
# si adatta in base alla tua scelta:
#   - Gemini: 2M token → versione FULL (~810 KB) via paste
#   - ChatGPT Plus: 128k token → versione SLIM (~250 KB) via paste,
#                   OPPURE FULL via allegato (drag-drop dalla
#                   Scrivania, ChatGPT usa RAG interno)
#   - Claude web Pro: 200k token → versione FULL via paste
# ══════════════════════════════════════════
25)
  echo ""
  echo -e "${GREEN}══ Esporta contesto per altra AI ══${NC}"
  echo ""
  cd "$SITO_DIR"

  if [ ! -x "scripts/export-contesto-ai.sh" ]; then
    echo -e "${RED}Errore: scripts/export-contesto-ai.sh non trovato.${NC}"
    read -p "INVIO..."; exec bash "$0"
  fi

  # Sincronizza il repo con GitHub: serve a recuperare modifiche
  # fatte da altre sessioni (mobile/cloud) o da altri device.
  # --ff-only: fast-forward only, fallisce in caso di conflitti
  # invece di fare merge automatici (sicuro). Se fallisce
  # l'utente viene avvisato ma lo script continua con il
  # contenuto locale.
  echo -e "${CYAN}Sincronizzo il repo con GitHub (recupero modifiche da altri device)...${NC}"
  PULL_OUTPUT=$(git pull --ff-only 2>&1)
  PULL_EXIT=$?
  if [ $PULL_EXIT -eq 0 ]; then
    if echo "$PULL_OUTPUT" | grep -q "Already up to date\|Già aggiornato"; then
      echo -e "${GREEN}✓ Repo già aggiornato.${NC}"
    else
      echo -e "${GREEN}✓ Repo sincronizzato con GitHub:${NC}"
      echo "$PULL_OUTPUT" | tail -5 | sed 's/^/    /'
    fi
  else
    echo -e "${YELLOW}⚠ git pull fallito (modifiche locali pending o conflitti).${NC}"
    echo -e "${YELLOW}  Procedo col contenuto LOCALE corrente — potrebbe non riflettere${NC}"
    echo -e "${YELLOW}  modifiche fatte da mobile/cloud. Risolvi manualmente se serve.${NC}"
    echo "$PULL_OUTPUT" | tail -3 | sed 's/^/    /'
  fi
  echo ""

  echo -e "${BOLD}Quale AI userai per scrivere il testo?${NC}"
  echo ""
  echo "  1) Gemini       (raccomandato — 2M token, gestisce tutto in paste)"
  echo "  2) ChatGPT Plus (limite 128k token — useremo SLIM in paste"
  echo "                   oppure FULL come allegato drag-drop)"
  echo "  3) Claude web   (Pro consigliato — 200k token in paste)"
  echo ""
  read -p "Scegli [1-3, default 1]: " ai_scelta

  case $ai_scelta in
    2)
      AI_NOME="ChatGPT"
      AI_URL="https://chat.openai.com/"
      MODE="slim"
      ;;
    3)
      AI_NOME="Claude web"
      AI_URL="https://claude.ai/"
      MODE="full"
      ;;
    *)
      AI_NOME="Gemini"
      AI_URL="https://gemini.google.com/"
      MODE="full"
      ;;
  esac

  echo ""
  echo -e "${CYAN}AI scelta: $AI_NOME — modalità $MODE${NC}"
  echo "Generazione contesto in corso..."

  if [ "$MODE" = "slim" ]; then
    bash scripts/export-contesto-ai.sh --slim > /dev/null 2>&1
    SOURCE_FILE="CONTESTO-AI-slim.md"
  else
    bash scripts/export-contesto-ai.sh > /dev/null 2>&1
    SOURCE_FILE="CONTESTO-AI.md"
  fi

  if [ ! -f "$SOURCE_FILE" ]; then
    echo -e "${RED}Errore: $SOURCE_FILE non generato.${NC}"
    read -p "INVIO..."; exec bash "$0"
  fi

  COMBINED="/tmp/pcgenzano-contesto-per-ai.md"
  if [ -f "scripts/prompt-istruzioni-ai.md" ]; then
    cat "scripts/prompt-istruzioni-ai.md" "$SOURCE_FILE" > "$COMBINED"
  else
    cp "$SOURCE_FILE" "$COMBINED"
  fi

  KB=$(du -k "$COMBINED" 2>/dev/null | cut -f1)
  LINES=$(wc -l < "$COMBINED" 2>/dev/null)
  TOKEN_STIMA=$(($(wc -c < "$COMBINED") / 4))
  echo ""
  echo -e "${GREEN}✓ File pronto per paste: $COMBINED${NC}"
  echo "   Dimensione: ${KB} KB · ${LINES} righe · ~${TOKEN_STIMA} token stimati"

  # Per ChatGPT genera anche FULL su Scrivania per drag-drop come allegato
  FULL_DEST=""
  if [ "$AI_NOME" = "ChatGPT" ]; then
    echo ""
    echo -e "${CYAN}Genero anche versione FULL per allegato (drag-drop in chat)...${NC}"
    bash scripts/export-contesto-ai.sh > /dev/null 2>&1

    if [ -d "$HOME/Scrivania" ]; then
      FULL_DEST="$HOME/Scrivania/contesto-pc-genzano-completo.md"
    elif [ -d "$HOME/Desktop" ]; then
      FULL_DEST="$HOME/Desktop/contesto-pc-genzano-completo.md"
    else
      FULL_DEST="$HOME/contesto-pc-genzano-completo.md"
    fi

    cat "scripts/prompt-istruzioni-ai.md" "CONTESTO-AI.md" > "$FULL_DEST" 2>/dev/null
    if [ -f "$FULL_DEST" ]; then
      KB_FULL=$(du -k "$FULL_DEST" 2>/dev/null | cut -f1)
      echo -e "${GREEN}✓ Versione FULL su: $FULL_DEST${NC}"
      echo "   Dimensione: ${KB_FULL} KB (trascinala in chat ChatGPT come allegato)"
    fi
  fi

  # Copia SLIM/FULL (a seconda dell'AI) negli appunti
  echo ""
  CLIP_OK=0
  if command -v xclip >/dev/null 2>&1; then
    if xclip -selection clipboard < "$COMBINED" 2>/dev/null; then
      CLIP_OK=1
      echo -e "${GREEN}✓ Versione $MODE copiata negli appunti (xclip).${NC}"
    fi
  elif command -v wl-copy >/dev/null 2>&1; then
    if wl-copy < "$COMBINED" 2>/dev/null; then
      CLIP_OK=1
      echo -e "${GREEN}✓ Versione $MODE copiata negli appunti (wl-copy).${NC}"
    fi
  elif command -v termux-clipboard-set >/dev/null 2>&1; then
    if termux-clipboard-set < "$COMBINED" 2>/dev/null; then
      CLIP_OK=1
      echo -e "${GREEN}✓ Versione $MODE copiata negli appunti (Termux).${NC}"
    fi
  fi

  if [ "$CLIP_OK" -eq 0 ]; then
    echo -e "${YELLOW}⚠ Tool clipboard non disponibile.${NC}"
    echo -e "  Apri manualmente: ${BOLD}$COMBINED${NC}"
    echo -e "  Linux desktop: ${BOLD}sudo apt install xclip${NC}"
    echo -e "  Wayland:       ${BOLD}sudo apt install wl-clipboard${NC}"
    echo -e "  Termux:        ${BOLD}pkg install termux-api${NC}"
  fi

  # Istruzioni specifiche per ogni AI
  echo ""
  echo -e "${BOLD}── Cosa fare adesso su $AI_NOME ──${NC}"
  echo ""
  case $AI_NOME in
    Gemini)
      echo "  1) Apri $AI_URL"
      echo "  2) Apri una NUOVA chat"
      echo "  3) Premi Ctrl+V e poi INVIO"
      echo "  4) Gemini risponderà: 'Ho letto il contesto, dimmi cosa serve'"
      echo "  5) Scrivi la richiesta, es:"
      echo -e "     ${CYAN}\"Scrivimi un articolo sul rischio incendio per giugno 2026\"${NC}"
      echo "  6) Copia la risposta e:"
      echo "     - per pubblicarla: voce 1 (Crea comunicazione)"
      echo "     - per abbozzarla con calma: voce 5 (Crea bozza)"
      echo "     - per rifinitura tecnica: voce 24 (Avvia Claude Code)"
      ;;
    ChatGPT)
      echo -e "  ${BOLD}HAI DUE STRADE — scegli quella che ti viene comoda${NC}"
      echo ""
      echo -e "  ${BOLD}A) Paste versione SLIM (semplice, sta in 64k token)${NC}"
      echo "     1) Apri $AI_URL"
      echo "     2) Apri una NUOVA chat"
      echo "     3) Ctrl+V nella casella e INVIO"
      echo "     4) ChatGPT risponderà 'Ho letto, dimmi cosa serve'"
      echo "     5) Scrivi la richiesta operativa"
      echo ""
      echo -e "  ${BOLD}B) Allegato versione FULL (più completa, via RAG)${NC}"
      echo "     1) Apri $AI_URL"
      echo "     2) Apri una NUOVA chat"
      echo "     3) Trascina questo file dentro la casella di input:"
      echo -e "        ${BOLD}$FULL_DEST${NC}"
      echo "        (oppure usa l'icona graffetta 📎 in basso a sinistra)"
      echo "     4) Scrivi: 'Leggi il file allegato e comportati come da"
      echo "        system prompt iniziale'"
      echo "     5) ChatGPT processa via RAG e ha tutto il contesto"
      ;;
    "Claude web")
      echo "  1) Apri $AI_URL"
      echo "  2) Apri una NUOVA chat (Pro consigliato per contesto pieno)"
      echo "  3) Premi Ctrl+V e poi INVIO"
      echo "  4) Claude risponderà 'Ho letto il contesto, dimmi cosa serve'"
      echo "  5) Scrivi la richiesta operativa"
      ;;
  esac

  echo ""
  read -p "Aprire $AI_NOME nel browser? [S/n]: " apri
  if [ "$apri" != "n" ] && [ "$apri" != "N" ]; then
    if command -v xdg-open >/dev/null 2>&1; then
      xdg-open "$AI_URL" 2>/dev/null
    elif command -v termux-open-url >/dev/null 2>&1; then
      termux-open-url "$AI_URL"
    else
      echo -e "${YELLOW}Apri manualmente: $AI_URL${NC}"
    fi
  fi
  ;;

# ══════════════════════════════════════════
# 26) SOCIAL — PUBBLICA BOZZE (assistito)
# ══════════════════════════════════════════
26)
  echo -e "\n${CYAN}── PUBBLICA BOZZE SOCIAL (assistito) ──${NC}"
  echo "Mostra ultime bozze disponibili in social-bozze/:"
  find "$SITO_DIR/social-bozze" -maxdepth 3 -mindepth 3 -type d 2>/dev/null \
    | sort -r | head -8 | sed 's|.*/||; s|^|  - |'
  echo ""
  read -rp "Slug articolo (es. 2026-05-18-titolo): " slug
  if [ -z "$slug" ]; then
    echo -e "${RED}Slug vuoto. Annullato.${NC}"
  else
    bash "$SITO_DIR/scripts/pubblica-social-assistito.sh" "$slug"
  fi
  ;;

# ══════════════════════════════════════════
# 27) STATO OPENCLI
# ══════════════════════════════════════════
27)
  echo -e "\n${CYAN}── STATO OPENCLI ──${NC}"
  if command -v opencli >/dev/null 2>&1; then
    echo "Versione CLI: $(opencli --version 2>&1)"
    echo ""
    opencli doctor 2>&1 | head -15
    echo ""
    echo -e "${CYAN}── LIVELLO B (pubblicazione social automatica con freno) ──${NC}"
    if [ -f "$SITO_DIR/scripts/pubblica-social-livello-b.sh" ]; then
      if head -25 "$SITO_DIR/scripts/pubblica-social-livello-b.sh" | grep -q "STANDBY"; then
        echo -e "${YELLOW}Stato: STANDBY (preparato ma non attivo)${NC}"
        echo "  Per attivarlo: rimuovi il blocco STANDBY GUARD nell'header del file."
      else
        echo -e "${GREEN}Stato: ATTIVO${NC}"
      fi
    else
      echo -e "${RED}Script Livello B non trovato.${NC}"
    fi
  else
    echo -e "${RED}opencli non installato. Installa con:${NC}"
    echo "  npm install -g @jackwener/opencli"
  fi
  ;;

# ══════════════════════════════════════════
# 28) OPEN-DESIGN (slide / PDF / mockup)
# ══════════════════════════════════════════
28)
  echo -e "\n${CYAN}── OPEN-DESIGN (web UI locale per slide/PDF/mockup) ──${NC}"
  if [ ! -d "$HOME/open-design" ]; then
    echo -e "${RED}open-design non installato in ~/open-design/${NC}"
    echo "Installa con:"
    echo "  cd ~ && git clone https://github.com/nexu-io/open-design.git"
    echo "  cd ~/open-design && corepack pnpm install"
  else
    echo "Avvio open-design in modalità web (Ctrl+C per chiudere)..."
    echo "L'URL della UI compare nella console qui sotto."
    echo ""
    cd "$HOME/open-design" && corepack pnpm tools-dev run web
  fi
  ;;

# ══════════════════════════════════════════
# 29) STRUTTURA
# ══════════════════════════════════════════
29)
  echo ""
  echo -e "${BOLD}STRUTTURA SITO${NC}"
  echo ""
  echo "Menu (8 voci, 5 dropdown):"
  echo "  Home | Per il Cittadino ▾ | Per le scuole ▾ | Accessibilità e Supporti ▾"
  echo "  Volontariato ▾ | Risorse ▾ | Comunicazioni | Contatti"
  echo ""
  echo "Per il Cittadino: Cosa Fare Adesso, Allerte Meteo, Rischi e Prevenzione,"
  echo "                  Cartografia, Numeri Utili, Piano Familiare,"
  echo "                  Kit pronti per situazioni vulnerabili"
  echo "Per le scuole: Kit per le scuole, Percorsi didattici, Schede stampabili,"
  echo "               Per i docenti, Storie e Racconti, Giochi della Sicurezza"
  echo "Accessibilità e Supporti: Abili a Proteggere, Facile da Leggere, Contenuti in LIS"
  echo "Volontariato: Diventa Volontario, Chi Siamo"
  echo "Risorse: FAQ, Glossario, Area Download, Normativa, Strumenti, Audio e podcast"
  echo ""
  echo "Rischi (9): sismico, idrogeologico, incendio, vento, temporali,"
  echo "            calore, blackout, kit-emergenza, necessità-specifiche"
  echo ""
  echo "Lingue (7): english, deutsch, espanol, francais, portugues,"
  echo "  romana, esperanto"
  echo ""
  echo "Data files: allerta.json, emergenza.json, numeri_utili.yaml,"
  echo "  quick_links.yaml, risk_cards.yaml, social_links.yaml,"
  echo "  codici_colore.yaml"
  echo ""
  echo "Badge (13 categorie con colore dedicato):"
  echo "  Allerta | Avviso | Comunicazione | Attività | Formazione |"
  echo "  Evento | Volontariato | Radiocomunicazioni | Prevenzione |"
  echo "  Esercitazione | Aggiornamento | Informazione | Emergenza"
  echo ""
  echo "Frontmatter articoli (campi):"
  echo "  title, date (AAAA-MM-GG), description, badge, priorita, autore,"
  echo "  image, image_alt, area, scadenza, allegati, draft (sempre false)"
  echo ""
  echo "Bozze (lavori in corso):"
  echo "  cartella bozze/ alla radice del repo — Hugo NON la costruisce,"
  echo "  quindi le bozze non vanno mai online finché non le pubblichi"
  echo "  (voce 7): vengono spostate in content/comunicazioni/<data>-<slug>.md"
  echo ""
  echo "Shortcode foto (per immagini nel corpo):"
  echo "  {{< foto src=\"/images/X.webp\" alt=\"...\" caption=\"...\" >}}"
  echo ""
  echo "Automazioni GitHub Actions principali:"
  echo "  deploy.yml (push), check-allerta.yml (orario),"
  echo "  pubblica-programmata.yml (06:00 daily),"
  echo "  audit-sito.yml (lun 09:00), check-links-sito.yml (lun 10:00),"
  echo "  smoke-test-post-deploy.yml, lighthouse-audit.yml,"
  echo "  genera-social-bozze.yml (a ogni push articolo)"
  ;;

# ══════════════════════════════════════════
# 30) GUIDA
# ══════════════════════════════════════════
30)
  if [ -f "$SITO_DIR/MANUALE-SITO.md" ]; then
    less "$SITO_DIR/MANUALE-SITO.md"
  elif [ -f "$SITO_DIR/CLAUDE.md" ]; then
    less "$SITO_DIR/CLAUDE.md"
  else
    echo -e "${RED}MANUALE-SITO.md non trovato in $SITO_DIR.${NC}"
  fi
  ;;

0) echo -e "\n${GREEN}Arrivederci!${NC}"; exit 0 ;;
*) echo -e "\n${RED}Non valida.${NC}" ;;
esac

echo ""
read -p "Premi INVIO per tornare al menu..."
exec bash "$0"
