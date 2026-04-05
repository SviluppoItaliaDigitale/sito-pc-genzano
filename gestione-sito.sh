#!/bin/bash
# ============================================================
# GESTIONE SITO — Protezione Civile Genzano di Roma
# v2.4 — Aprile 2026
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

conta_bozze() {
  local count=0
  for f in "$CONTENT_DIR/comunicazioni/"*.md; do
    [ "$(basename "$f")" = "_index.md" ] && continue
    [ ! -f "$f" ] && continue
    grep -q "^draft: true" "$f" 2>/dev/null && count=$((count+1))
  done
  echo $count
}

lista_comunicazioni() {
  local tipo=$1
  local files=()
  for f in "$CONTENT_DIR/comunicazioni/"*.md; do
    [ "$(basename "$f")" = "_index.md" ] && continue
    [ ! -f "$f" ] && continue
    if [ "$tipo" = "draft" ]; then
      grep -q "^draft: true" "$f" 2>/dev/null && files+=("$(basename "$f")")
    else
      grep -q "^draft: true" "$f" 2>/dev/null || files+=("$(basename "$f")")
    fi
  done
  echo "${files[@]}"
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
  echo "║   v2.4 — $(date '+%d/%m/%Y %H:%M')                              ║"
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
  [ "$nbozze" -gt 0 ] && echo -e "  ${YELLOW}📝 Bozze in attesa: $nbozze${NC}"
  echo ""

  echo -e "${CYAN}── COMUNICAZIONI ──${NC}"
  echo "  1) Crea nuova comunicazione"
  echo "  2) Crea comunicazione da file Word"
  echo "  3) Modifica comunicazione pubblicata"
  echo "  4) Elimina comunicazione pubblicata"
  echo ""
  echo -e "${CYAN}── BOZZE ──${NC}"
  echo "  5) Vedi bozze in attesa"
  echo "  6) Modifica bozza"
  echo "  7) Pubblica bozza"
  echo "  8) Elimina bozza"
  echo ""
  echo -e "${CYAN}── PAGINE ──${NC}"
  echo "  9) Modifica qualsiasi pagina"
  echo " 10) Crea nuova pagina"
  echo " 11) Elimina pagina"
  echo ""
  echo -e "${CYAN}── EMERGENZA ──${NC}"
  echo " 12) Attiva emergenza"
  echo " 13) Modifica emergenza attiva"
  echo " 14) Sospendi emergenza (mantiene i dati)"
  echo ""
  echo -e "${CYAN}── ALLERTA METEO ──${NC}"
  echo " 15) Imposta livello allerta"
  echo ""
  echo -e "${CYAN}── PUBBLICA E TESTA ──${NC}"
  echo " 16) Test sito in locale"
  echo " 17) Test sito con bozze visibili"
  echo " 18) Pubblica modifiche online"
  echo " 19) Stato repository"
  echo ""
  echo -e "${CYAN}── LINK RAPIDI ──${NC}"
  echo " 20) Sito produzione    21) GitHub Actions"
  echo " 22) Repository GitHub  23) Bollettino Lazio"
  echo " 24) ActivePager        25) Claude AI"
  echo ""
  echo -e "${CYAN}── GUIDE ──${NC}"
  echo " 26) Struttura del sito"
  echo " 27) Guida pubblicazione"
  echo ""
  echo -e "${YELLOW}  0) Esci${NC}"
  echo ""
}

# ══════════════════════════════════════════
mostra_menu
echo -ne "${BOLD}Scegli [0-27]: ${NC}"
read scelta

case $scelta in

# ══════════════════════════════════════════
# 1) CREA COMUNICAZIONE
# ══════════════════════════════════════════
1)
  echo ""
  echo -e "${GREEN}══ Nuova comunicazione ══${NC}"
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

  echo -e "${BOLD}Immagine (opzionale, es. /images/foto.jpg):${NC}"
  read -e -p "> " image

  echo ""
  echo -e "${BOLD}Salvare come:${NC}"
  echo "  1) Bozza — la scrivi con calma, non va online"
  echo "  2) Pubblicata — pronta per andare online"
  read -p "Scegli [1-2, default 1]: " ds
  [ "$ds" = "2" ] && draft_val="false" || draft_val="true"

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
draft: $draft_val
---

Scrivi qui il contenuto della comunicazione.
EOF

  echo ""
  if [ "$draft_val" = "true" ]; then
    echo -e "${YELLOW}Salvata come BOZZA. Non andrà online.${NC}"
    echo -e "Per pubblicarla: opzione ${BOLD}7${NC}"
  else
    echo -e "${GREEN}Salvata come PUBBLICATA.${NC}"
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
  echo "  3. Usa opzione 1 per creare il file, poi incolla il contenuto."
  ;;

# ══════════════════════════════════════════
# 3) MODIFICA COMUNICAZIONE PUBBLICATA
# ══════════════════════════════════════════
3)
  echo ""
  echo -e "${GREEN}══ Modifica comunicazione pubblicata ══${NC}"
  echo ""
  IFS=' ' read -ra files <<< "$(lista_comunicazioni published)"
  if [ ${#files[@]} -eq 0 ]; then echo "Nessuna comunicazione pubblicata."
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
  IFS=' ' read -ra files <<< "$(lista_comunicazioni published)"
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
# 5) VEDI BOZZE
# ══════════════════════════════════════════
5)
  echo ""
  echo -e "${YELLOW}══ Bozze in attesa ══${NC}"
  echo ""
  IFS=' ' read -ra files <<< "$(lista_comunicazioni draft)"
  if [ ${#files[@]} -eq 0 ]; then
    echo "Nessuna bozza. Usa opzione 1 per crearne una."
  else
    for i in "${!files[@]}"; do
      titolo_b=$(grep "^title:" "$CONTENT_DIR/comunicazioni/${files[$i]}" 2>/dev/null | head -1 | sed 's/^title: *"//;s/"$//')
      echo -e "  $((i+1))) ${files[$i]}  ${CYAN}→ $titolo_b${NC}"
    done
  fi
  ;;

# ══════════════════════════════════════════
# 6) MODIFICA BOZZA
# ══════════════════════════════════════════
6)
  echo ""
  IFS=' ' read -ra files <<< "$(lista_comunicazioni draft)"
  if [ ${#files[@]} -eq 0 ]; then echo "Nessuna bozza."
  else
    for i in "${!files[@]}"; do
      titolo_b=$(grep "^title:" "$CONTENT_DIR/comunicazioni/${files[$i]}" 2>/dev/null | head -1 | sed 's/^title: *"//;s/"$//')
      echo -e "  $((i+1))) ${CYAN}$titolo_b${NC}  (${files[$i]})"
    done
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
# 7) PUBBLICA BOZZA
# ══════════════════════════════════════════
7)
  echo ""
  echo -e "${GREEN}══ Pubblica bozza ══${NC}"
  echo ""
  IFS=' ' read -ra files <<< "$(lista_comunicazioni draft)"
  if [ ${#files[@]} -eq 0 ]; then echo "Nessuna bozza."
  else
    for i in "${!files[@]}"; do
      titolo_b=$(grep "^title:" "$CONTENT_DIR/comunicazioni/${files[$i]}" 2>/dev/null | head -1 | sed 's/^title: *"//;s/"$//')
      echo -e "  $((i+1))) ${CYAN}$titolo_b${NC}"
    done
    echo ""
    read -p "Numero da pubblicare: " num; idx=$((num-1))
    if [ $idx -ge 0 ] && [ $idx -lt ${#files[@]} ]; then
      read -p "Confermi? [S/n]: " conf
      if [ "$conf" != "n" ] && [ "$conf" != "N" ]; then
        filepath="$CONTENT_DIR/comunicazioni/${files[$idx]}"
        sed -i 's/^draft: true/draft: false/' "$filepath"
        sed -i "s/^date: .*/date: $(date +%Y-%m-%d)/" "$filepath"
        echo -e "${GREEN}Bozza PUBBLICATA! Per metterla online: opzione 18.${NC}"
      else echo "Annullato."; fi
    else echo -e "${RED}Non valida.${NC}"; fi
  fi
  ;;

# ══════════════════════════════════════════
# 8) ELIMINA BOZZA
# ══════════════════════════════════════════
8)
  echo ""
  IFS=' ' read -ra files <<< "$(lista_comunicazioni draft)"
  if [ ${#files[@]} -eq 0 ]; then echo "Nessuna bozza."
  else
    for i in "${!files[@]}"; do
      titolo_b=$(grep "^title:" "$CONTENT_DIR/comunicazioni/${files[$i]}" 2>/dev/null | head -1 | sed 's/^title: *"//;s/"$//')
      echo -e "  $((i+1))) ${CYAN}$titolo_b${NC}"
    done
    echo ""
    read -p "Numero: " num; idx=$((num-1))
    if [ $idx -ge 0 ] && [ $idx -lt ${#files[@]} ]; then
      read -p "Scrivi 'elimina': " conf
      [ "$conf" = "elimina" ] && { rm "$CONTENT_DIR/comunicazioni/${files[$idx]}"; echo -e "${GREEN}Eliminata.${NC}"; } || echo "Annullato."
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
      # Se era un _index.md e la cartella è vuota, rimuovi anche la cartella
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
      echo -e "${GREEN}RIATTIVATA! Per pubblicare: opzione 18.${NC}"
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
  echo -e "${GREEN}ATTIVATA! Per pubblicare: opzione 18.${NC}"
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
    echo -e "${GREEN}SOSPESA. Per pubblicare: opzione 18.${NC}"
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
# 16) TEST (senza bozze)
# ══════════════════════════════════════════
16)
  echo -e "Browser: ${BOLD}http://localhost:1313/${NC}  Ferma: ${BOLD}Ctrl+C${NC}"
  read -p "INVIO per avviare..."
  cd "$SITO_DIR" && hugo server
  ;;

# ══════════════════════════════════════════
# 17) TEST CON BOZZE
# ══════════════════════════════════════════
17)
  echo -e "${YELLOW}Le bozze saranno visibili solo in questo test.${NC}"
  echo -e "Browser: ${BOLD}http://localhost:1313/${NC}  Ferma: ${BOLD}Ctrl+C${NC}"
  read -p "INVIO per avviare..."
  cd "$SITO_DIR" && hugo server -D
  ;;

# ══════════════════════════════════════════
# 18) PUBBLICA
# ══════════════════════════════════════════
18)
  echo ""
  cd "$SITO_DIR"
  echo -e "${BOLD}File modificati:${NC}"
  git status --short
  echo ""
  modifiche=$(git status --short | wc -l)
  [ "$modifiche" -eq 0 ] && { echo "Nessuna modifica."; read -p "INVIO..."; exec bash "$0"; }

  nbozze=$(conta_bozze)
  [ "$nbozze" -gt 0 ] && echo -e "${YELLOW}Ci sono $nbozze bozze — non andranno online.${NC}" && echo ""

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
# 19) STATO
# ══════════════════════════════════════════
19) cd "$SITO_DIR"; echo ""; git status; echo ""; echo -e "${BOLD}Ultime 10:${NC}"; git log --oneline -10 ;;

# ══════════════════════════════════════════
# 20-25) LINK
# ══════════════════════════════════════════
20) xdg-open "https://www.protezionecivilegenzano.it/" 2>/dev/null || echo "protezionecivilegenzano.it" ;;
21) xdg-open "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions" 2>/dev/null ;;
22) xdg-open "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano" 2>/dev/null ;;
23) xdg-open "https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" 2>/dev/null ;;
24) xdg-open "https://activepager.com/auth/login" 2>/dev/null || echo "activepager.com" ;;
25) xdg-open "https://claude.ai" 2>/dev/null || echo "claude.ai" ;;

# ══════════════════════════════════════════
# 26) STRUTTURA
# ══════════════════════════════════════════
26)
  echo ""
  echo -e "${BOLD}STRUTTURA SITO${NC}"
  echo ""
  echo "Menu: Home | Chi Siamo | Rischi e Prevenzione | Allerte Meteo"
  echo "      Comunicazioni | Diventa Volontario | Contatti"
  echo ""
  echo "Rischi (9): sismico, idrogeologico, incendio, vento, temporali,"
  echo "            calore, blackout, kit-emergenza, necessità-specifiche"
  echo ""
  echo "Altre: piano-emergenza, piano-familiare, cartografia, area-download,"
  echo "       cosa-fare-adesso, numeri-utili, faq, formazione, siti-utili"
  echo ""
  echo "Data: allerta.json, emergenza.json, numeri_utili.yaml,"
  echo "      quick_links.yaml, risk_cards.yaml, social_links.yaml"
  echo ""
  echo "Badge: Allerta|Avviso|Comunicazione|Attività|Formazione|Evento|Volontariato"
  echo ""
  echo "Articoli: title, date, badge, description, priorita, autore,"
  echo "          image, area, scadenza, allegati, draft"
  ;;

# ══════════════════════════════════════════
# 27) GUIDA
# ══════════════════════════════════════════
27)
  [ -f "$SITO_DIR/GUIDA-UPLOAD-V2.md" ] && less "$SITO_DIR/GUIDA-UPLOAD-V2.md" || echo "Non trovata."
  ;;

0) echo -e "\n${GREEN}Arrivederci!${NC}"; exit 0 ;;
*) echo -e "\n${RED}Non valida.${NC}" ;;
esac

echo ""
read -p "Premi INVIO per tornare al menu..."
exec bash "$0"
