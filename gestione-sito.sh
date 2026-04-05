#!/bin/bash
# ============================================================
# GESTIONE SITO — Protezione Civile Genzano di Roma
# v2.3 — Aprile 2026
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

# Funzione per contare le bozze
conta_bozze() {
  local count=0
  for f in "$CONTENT_DIR/comunicazioni/"*.md; do
    [ "$(basename "$f")" = "_index.md" ] && continue
    [ ! -f "$f" ] && continue
    if grep -q "^draft: true" "$f" 2>/dev/null; then
      count=$((count+1))
    fi
  done
  echo $count
}

mostra_menu() {
  clear
  echo -e "${BLUE}${BOLD}"
  echo "╔══════════════════════════════════════════════════════════╗"
  echo "║   GESTIONE SITO — Protezione Civile Genzano di Roma    ║"
  echo "║   v2.3 — $(date '+%d/%m/%Y %H:%M')                              ║"
  echo "╚══════════════════════════════════════════════════════════╝"
  echo -e "${NC}"

  # Stato emergenza
  if [ -f "$DATA_DIR/emergenza.json" ]; then
    stato_em=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print('ATTIVA — '+d.get('titolo','') if d.get('attiva') else 'sospesa' if d.get('titolo','') else 'disattivata')" 2>/dev/null)
    if echo "$stato_em" | grep -q "ATTIVA"; then
      echo -e "  ${RED}${BOLD}⚠ EMERGENZA: $stato_em${NC}"
    else
      echo -e "  Emergenza: $stato_em"
    fi
  fi

  # Conta bozze
  nbozze=$(conta_bozze)
  if [ "$nbozze" -gt 0 ]; then
    echo -e "  ${YELLOW}📝 Bozze in attesa: $nbozze${NC}"
  fi
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
  echo "  9) Crea nuova pagina"
  echo " 10) Modifica pagina"
  echo " 11) Modifica pagina rischio"
  echo " 12) Elimina pagina"
  echo ""
  echo -e "${CYAN}── EMERGENZA ──${NC}"
  echo " 13) Attiva emergenza"
  echo " 14) Modifica emergenza attiva"
  echo " 15) Sospendi emergenza (mantiene i dati)"
  echo ""
  echo -e "${CYAN}── ALLERTA METEO ──${NC}"
  echo " 16) Imposta livello allerta"
  echo ""
  echo -e "${CYAN}── PUBBLICA E TESTA ──${NC}"
  echo " 17) Test sito in locale"
  echo " 18) Test sito con bozze visibili"
  echo " 19) Pubblica modifiche online"
  echo " 20) Stato repository"
  echo ""
  echo -e "${CYAN}── LINK RAPIDI ──${NC}"
  echo " 21) Sito produzione    22) GitHub Actions"
  echo " 23) Repository GitHub  24) Bollettino Lazio"
  echo " 25) ActivePager        26) Claude AI"
  echo ""
  echo -e "${CYAN}── GUIDE ──${NC}"
  echo " 27) Struttura del sito"
  echo " 28) Guida pubblicazione"
  echo ""
  echo -e "${YELLOW}  0) Esci${NC}"
  echo ""
}

# Funzione: lista file comunicazioni (escluso _index), filtra per draft/published
# $1 = "draft" o "published"
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

# ══════════════════════════════════════════
mostra_menu
echo -ne "${BOLD}Scegli [0-28]: ${NC}"
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
  echo -e "${BOLD}Area interessata (opzionale):${NC}"
  read -e -p "> " area

  echo ""
  echo -e "${BOLD}Data scadenza (opzionale, AAAA-MM-GG):${NC}"
  read -e -p "> " scadenza

  echo ""
  echo -e "${BOLD}Immagine (opzionale, es. /images/foto.jpg):${NC}"
  read -e -p "> " image

  echo ""
  echo -e "${BOLD}Salvare come:${NC}"
  echo "  1) Bozza — la scrivi dopo con calma, non va online"
  echo "  2) Pubblicata — pronta per andare online"
  read -p "Scegli [1-2, default 1]: " draft_scelta
  [ "$draft_scelta" = "2" ] && draft_val="false" || draft_val="true"

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
  echo -e "${GREEN}════════════════════════════════════════${NC}"
  if [ "$draft_val" = "true" ]; then
    echo -e "${YELLOW}Comunicazione salvata come BOZZA.${NC}"
    echo -e "${YELLOW}Non andrà online finché non la pubblichi (opzione 7).${NC}"
  else
    echo -e "${GREEN}Comunicazione salvata come PUBBLICATA.${NC}"
    echo -e "${GREEN}Andrà online al prossimo push (opzione 19).${NC}"
  fi
  echo -e "${GREEN}════════════════════════════════════════${NC}"
  echo ""
  echo -e "File: ${BOLD}$file${NC}"
  echo ""
  echo -e "Prossimi passi:"
  echo -e "  1. Scrivi il contenuto:   ${BOLD}nano $file${NC}"
  echo -e "     (salva: Ctrl+O → INVIO, esci: Ctrl+X)"
  if [ "$draft_val" = "true" ]; then
    echo -e "  2. Quando è pronta:      usa opzione ${BOLD}7${NC} del menu per pubblicarla"
  fi
  echo -e "  3. Testa in locale:       usa opzione ${BOLD}17${NC} del menu"
  echo -e "  4. Metti online:          usa opzione ${BOLD}19${NC} del menu"
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
    echo "  3. Usa opzione 1 del menu per creare il file con tutti i campi,"
    echo "     poi incolla il contenuto convertito."
  fi
  ;;

# ══════════════════════════════════════════
# 3) MODIFICA COMUNICAZIONE PUBBLICATA
# ══════════════════════════════════════════
3)
  echo ""
  echo -e "${GREEN}══ Modifica comunicazione pubblicata ══${NC}"
  echo ""
  IFS=' ' read -ra files <<< "$(lista_comunicazioni published)"
  if [ ${#files[@]} -eq 0 ]; then
    echo "Nessuna comunicazione pubblicata trovata."
  else
    for i in "${!files[@]}"; do
      echo "  $((i+1))) ${files[$i]}"
    done
    echo ""
    read -p "Numero da modificare: " num
    idx=$((num-1))
    if [ $idx -ge 0 ] && [ $idx -lt ${#files[@]} ]; then
      echo ""
      echo -e "${YELLOW}Salva: Ctrl+O → INVIO — Esci: Ctrl+X${NC}"
      read -p "Premi INVIO per aprire..."
      nano "$CONTENT_DIR/comunicazioni/${files[$idx]}"
    else
      echo -e "${RED}Selezione non valida.${NC}"
    fi
  fi
  ;;

# ══════════════════════════════════════════
# 4) ELIMINA COMUNICAZIONE PUBBLICATA
# ══════════════════════════════════════════
4)
  echo ""
  echo -e "${RED}══ Elimina comunicazione pubblicata ══${NC}"
  echo ""
  IFS=' ' read -ra files <<< "$(lista_comunicazioni published)"
  if [ ${#files[@]} -eq 0 ]; then
    echo "Nessuna comunicazione pubblicata trovata."
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
# 5) VEDI BOZZE
# ══════════════════════════════════════════
5)
  echo ""
  echo -e "${YELLOW}══ Bozze in attesa ══${NC}"
  echo ""
  IFS=' ' read -ra files <<< "$(lista_comunicazioni draft)"
  if [ ${#files[@]} -eq 0 ]; then
    echo "Nessuna bozza trovata."
    echo ""
    echo "Per creare una nuova comunicazione come bozza, usa l'opzione 1."
  else
    echo "Bozze trovate: ${#files[@]}"
    echo ""
    for i in "${!files[@]}"; do
      titolo_bozza=$(grep "^title:" "$CONTENT_DIR/comunicazioni/${files[$i]}" | head -1 | sed 's/^title: *"//;s/"$//')
      echo -e "  $((i+1))) ${files[$i]}"
      echo -e "      ${CYAN}→ $titolo_bozza${NC}"
    done
    echo ""
    echo "Per modificare una bozza:    opzione 6"
    echo "Per pubblicare una bozza:    opzione 7"
    echo "Per eliminare una bozza:     opzione 8"
  fi
  ;;

# ══════════════════════════════════════════
# 6) MODIFICA BOZZA
# ══════════════════════════════════════════
6)
  echo ""
  echo -e "${YELLOW}══ Modifica bozza ══${NC}"
  echo ""
  IFS=' ' read -ra files <<< "$(lista_comunicazioni draft)"
  if [ ${#files[@]} -eq 0 ]; then
    echo "Nessuna bozza trovata."
  else
    for i in "${!files[@]}"; do
      titolo_bozza=$(grep "^title:" "$CONTENT_DIR/comunicazioni/${files[$i]}" | head -1 | sed 's/^title: *"//;s/"$//')
      echo -e "  $((i+1))) ${files[$i]}  ${CYAN}→ $titolo_bozza${NC}"
    done
    echo ""
    read -p "Numero da modificare: " num
    idx=$((num-1))
    if [ $idx -ge 0 ] && [ $idx -lt ${#files[@]} ]; then
      echo ""
      echo -e "${YELLOW}Salva: Ctrl+O → INVIO — Esci: Ctrl+X${NC}"
      read -p "Premi INVIO per aprire..."
      nano "$CONTENT_DIR/comunicazioni/${files[$idx]}"
    else
      echo -e "${RED}Selezione non valida.${NC}"
    fi
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
  if [ ${#files[@]} -eq 0 ]; then
    echo "Nessuna bozza trovata."
  else
    for i in "${!files[@]}"; do
      titolo_bozza=$(grep "^title:" "$CONTENT_DIR/comunicazioni/${files[$i]}" | head -1 | sed 's/^title: *"//;s/"$//')
      echo -e "  $((i+1))) ${files[$i]}  ${CYAN}→ $titolo_bozza${NC}"
    done
    echo ""
    read -p "Numero da pubblicare: " num
    idx=$((num-1))
    if [ $idx -ge 0 ] && [ $idx -lt ${#files[@]} ]; then
      filepath="$CONTENT_DIR/comunicazioni/${files[$idx]}"
      echo ""
      echo -e "Stai per pubblicare: ${BOLD}${files[$idx]}${NC}"
      echo "La comunicazione diventerà visibile sul sito al prossimo push."
      echo ""
      read -p "Confermi? [S/n]: " conf
      if [ "$conf" != "n" ] && [ "$conf" != "N" ]; then
        sed -i 's/^draft: true/draft: false/' "$filepath"
        # Aggiorna anche la data alla data odierna
        data_oggi=$(date +%Y-%m-%d)
        sed -i "s/^date: .*/date: $data_oggi/" "$filepath"
        echo ""
        echo -e "${GREEN}════════════════════════════════════════${NC}"
        echo -e "${GREEN}Bozza PUBBLICATA!${NC}"
        echo -e "${GREEN}════════════════════════════════════════${NC}"
        echo ""
        echo -e "Data aggiornata a: $data_oggi"
        echo -e "Per metterla online: usa opzione ${BOLD}19${NC} del menu."
      else
        echo "Annullato."
      fi
    else
      echo -e "${RED}Selezione non valida.${NC}"
    fi
  fi
  ;;

# ══════════════════════════════════════════
# 8) ELIMINA BOZZA
# ══════════════════════════════════════════
8)
  echo ""
  echo -e "${RED}══ Elimina bozza ══${NC}"
  echo ""
  IFS=' ' read -ra files <<< "$(lista_comunicazioni draft)"
  if [ ${#files[@]} -eq 0 ]; then
    echo "Nessuna bozza trovata."
  else
    for i in "${!files[@]}"; do
      titolo_bozza=$(grep "^title:" "$CONTENT_DIR/comunicazioni/${files[$i]}" | head -1 | sed 's/^title: *"//;s/"$//')
      echo -e "  $((i+1))) ${files[$i]}  ${CYAN}→ $titolo_bozza${NC}"
    done
    echo ""
    read -p "Numero da eliminare: " num
    idx=$((num-1))
    if [ $idx -ge 0 ] && [ $idx -lt ${#files[@]} ]; then
      echo ""
      echo -e "${RED}Stai per eliminare la bozza: ${files[$idx]}${NC}"
      read -p "Scrivi 'elimina' per confermare: " conf
      if [ "$conf" = "elimina" ]; then
        rm "$CONTENT_DIR/comunicazioni/${files[$idx]}"
        echo -e "${GREEN}Bozza eliminata.${NC}"
      else
        echo "Annullato."
      fi
    else
      echo -e "${RED}Selezione non valida.${NC}"
    fi
  fi
  ;;

# ══════════════════════════════════════════
# 9) CREA PAGINA
# ══════════════════════════════════════════
9)
  echo ""
  echo -e "${GREEN}══ Crea nuova pagina ══${NC}"
  echo ""
  echo -e "${BOLD}Nome della sezione (diventerà l'URL, es. 'avvisi-neve'):${NC}"
  echo -e "${YELLOW}Usa lettere minuscole e trattini, niente spazi o accenti.${NC}"
  read -e -p "> " sezione
  [ -z "$sezione" ] && { echo -e "${RED}Nome obbligatorio.${NC}"; read -p "Premi INVIO..."; exec bash "$0"; }

  echo ""
  echo -e "${BOLD}Titolo:${NC}"
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
  read -p "Aprire con nano? [S/n]: " apri
  [ "$apri" != "n" ] && [ "$apri" != "N" ] && nano "$CONTENT_DIR/$sezione/_index.md"
  ;;

# ══════════════════════════════════════════
# 10) MODIFICA PAGINA
# ══════════════════════════════════════════
10)
  echo ""
  echo -e "${GREEN}══ Modifica pagina ══${NC}"
  echo ""
  pagine=(); nomi=()
  while IFS= read -r f; do
    sez=$(echo "$f" | sed "s|$CONTENT_DIR/||;s|/_index.md||")
    pagine+=("$f"); nomi+=("$sez")
  done < <(find "$CONTENT_DIR" -maxdepth 2 -name "_index.md" | sort)
  for i in "${!nomi[@]}"; do echo "  $((i+1))) ${nomi[$i]}"; done
  echo ""
  read -p "Numero: " num; idx=$((num-1))
  if [ $idx -ge 0 ] && [ $idx -lt ${#pagine[@]} ]; then
    echo -e "${YELLOW}Salva: Ctrl+O → INVIO — Esci: Ctrl+X${NC}"
    read -p "Premi INVIO per aprire..."
    nano "${pagine[$idx]}"
  else echo -e "${RED}Selezione non valida.${NC}"; fi
  ;;

# ══════════════════════════════════════════
# 11) MODIFICA PAGINA RISCHIO
# ══════════════════════════════════════════
11)
  echo ""
  echo -e "${GREEN}══ Modifica pagina rischio ══${NC}"
  echo ""
  files=($(ls -1 "$CONTENT_DIR/rischi-prevenzione/" | grep -v "_index"))
  for i in "${!files[@]}"; do echo "  $((i+1))) ${files[$i]}"; done
  echo ""
  read -p "Numero: " num; idx=$((num-1))
  if [ $idx -ge 0 ] && [ $idx -lt ${#files[@]} ]; then
    echo -e "${YELLOW}Salva: Ctrl+O → INVIO — Esci: Ctrl+X${NC}"
    read -p "Premi INVIO per aprire..."
    nano "$CONTENT_DIR/rischi-prevenzione/${files[$idx]}"
  else echo -e "${RED}Selezione non valida.${NC}"; fi
  ;;

# ══════════════════════════════════════════
# 12) ELIMINA PAGINA
# ══════════════════════════════════════════
12)
  echo ""
  echo -e "${RED}══ Elimina pagina ══${NC}"
  echo ""
  echo -e "${YELLOW}Non eliminare le pagine principali del sito!${NC}"
  echo ""
  pagine=(); nomi=()
  while IFS= read -r f; do
    sez=$(echo "$f" | sed "s|$CONTENT_DIR/||;s|/_index.md||")
    pagine+=("$f"); nomi+=("$sez")
  done < <(find "$CONTENT_DIR" -maxdepth 2 -name "_index.md" | sort)
  for i in "${!nomi[@]}"; do echo "  $((i+1))) ${nomi[$i]}"; done
  echo ""
  read -p "Numero da eliminare: " num; idx=$((num-1))
  if [ $idx -ge 0 ] && [ $idx -lt ${#pagine[@]} ]; then
    echo -e "${RED}Stai per eliminare: ${nomi[$idx]}${NC}"
    read -p "Scrivi 'elimina' per confermare: " conf
    [ "$conf" = "elimina" ] && { rm -rf "$CONTENT_DIR/${nomi[$idx]}"; echo -e "${GREEN}Eliminato.${NC}"; } || echo "Annullato."
  else echo -e "${RED}Selezione non valida.${NC}"; fi
  ;;

# ══════════════════════════════════════════
# 13) ATTIVA EMERGENZA
# ══════════════════════════════════════════
13)
  echo ""
  echo -e "${RED}══ Attiva emergenza ══${NC}"
  echo ""

  titolo_esistente=""
  attiva_esistente="False"
  if [ -f "$DATA_DIR/emergenza.json" ]; then
    titolo_esistente=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('titolo',''))" 2>/dev/null)
    attiva_esistente=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('attiva',False))" 2>/dev/null)
  fi

  if [ "$attiva_esistente" = "True" ]; then
    echo -e "${YELLOW}L'emergenza è già attiva!${NC}"
    echo "Usa opzione 14 per modificarla o 15 per sospenderla."
    read -p "Premi INVIO..."; exec bash "$0"
  fi

  if [ -n "$titolo_esistente" ] && [ "$titolo_esistente" != "" ]; then
    echo -e "Emergenza sospesa trovata: ${BOLD}$titolo_esistente${NC}"
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
      echo -e "${GREEN}Emergenza RIATTIVATA!${NC}"
      echo -e "Per rendere visibile: opzione ${BOLD}19${NC}."
      read -p "Premi INVIO..."; exec bash "$0"
    fi
  fi

  echo -e "${YELLOW}La homepage si riorganizzerà in modalità emergenza.${NC}"
  echo ""
  echo "Colore:  1) Blu  2) Azzurro  3) Verde  4) Giallo  5) Arancione  6) Rosso  7) Viola"
  read -p "Scegli [1-7]: " tn
  case $tn in 1) tipo="blu";; 2) tipo="azzurro";; 3) tipo="verde";; 4) tipo="giallo";; 5) tipo="arancione";; 6) tipo="rosso";; 7) tipo="viola";; *) tipo="blu";; esac

  echo ""; echo -e "${BOLD}Titolo:${NC}"; read -e -p "> " titolo
  echo ""; echo -e "${BOLD}Descrizione:${NC}"; read -e -p "> " desc
  echo ""; echo -e "${BOLD}Link (opzionale):${NC}"; read -e -p "> " link

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
  echo -e "${GREEN}Emergenza ATTIVATA! Per rendere visibile: opzione 19.${NC}"
  ;;

# ══════════════════════════════════════════
# 14) MODIFICA EMERGENZA
# ══════════════════════════════════════════
14)
  echo ""
  echo -e "${YELLOW}══ Modifica emergenza ══${NC}"
  echo ""; cat "$DATA_DIR/emergenza.json"; echo ""
  echo -e "${YELLOW}Salva: Ctrl+O → INVIO — Esci: Ctrl+X${NC}"
  read -p "Premi INVIO per aprire..."
  nano "$DATA_DIR/emergenza.json"
  ;;

# ══════════════════════════════════════════
# 15) SOSPENDI EMERGENZA
# ══════════════════════════════════════════
15)
  echo ""
  echo -e "${YELLOW}══ Sospendi emergenza ══${NC}"
  echo ""
  attiva_em=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('attiva',False))" 2>/dev/null)
  if [ "$attiva_em" != "True" ]; then
    echo "L'emergenza non è attiva."
    read -p "Premi INVIO..."; exec bash "$0"
  fi
  titolo_em=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('titolo',''))" 2>/dev/null)
  echo -e "Emergenza: ${BOLD}$titolo_em${NC}"
  echo -e "${YELLOW}I dati restano salvati. Potrai riattivare con opzione 13.${NC}"
  echo ""
  read -p "Confermi sospensione? [S/n]: " conf
  if [ "$conf" != "n" ] && [ "$conf" != "N" ]; then
    python3 -c "
import json
with open('$DATA_DIR/emergenza.json','r') as f: d=json.load(f)
d['attiva']=False
with open('$DATA_DIR/emergenza.json','w') as f: json.dump(d,f,indent=2,ensure_ascii=False)
"
    echo -e "${GREEN}Emergenza SOSPESA. Homepage in modalità ordinaria.${NC}"
    echo -e "Per rendere visibile: opzione ${BOLD}19${NC}."
  else echo "Annullato."; fi
  ;;

# ══════════════════════════════════════════
# 16) ALLERTA
# ══════════════════════════════════════════
16)
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
    *) echo -e "${RED}Non valida.${NC}"; read -p "Premi INVIO..."; exec bash "$0";;
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
# 17) TEST LOCALE (senza bozze)
# ══════════════════════════════════════════
17)
  echo ""
  echo -e "${GREEN}══ Test locale (solo contenuti pubblicati) ══${NC}"
  echo ""
  echo -e "Browser: ${BOLD}http://localhost:1313/${NC}"
  echo -e "Ferma: ${BOLD}Ctrl+C${NC}"
  echo ""
  read -p "Premi INVIO per avviare..."
  cd "$SITO_DIR" && hugo server
  ;;

# ══════════════════════════════════════════
# 18) TEST CON BOZZE
# ══════════════════════════════════════════
18)
  echo ""
  echo -e "${YELLOW}══ Test locale (bozze visibili) ══${NC}"
  echo ""
  echo -e "${YELLOW}Le bozze saranno visibili solo in questo test, NON andranno online.${NC}"
  echo -e "Browser: ${BOLD}http://localhost:1313/${NC}"
  echo -e "Ferma: ${BOLD}Ctrl+C${NC}"
  echo ""
  read -p "Premi INVIO per avviare..."
  cd "$SITO_DIR" && hugo server -D
  ;;

# ══════════════════════════════════════════
# 19) PUBBLICA
# ══════════════════════════════════════════
19)
  echo ""
  echo -e "${GREEN}══ Pubblica modifiche online ══${NC}"
  echo ""
  cd "$SITO_DIR"
  echo -e "${BOLD}File modificati:${NC}"
  git status --short
  echo ""
  modifiche=$(git status --short | wc -l)
  [ "$modifiche" -eq 0 ] && { echo "Nessuna modifica."; read -p "Premi INVIO..."; exec bash "$0"; }

  # Avvisa se ci sono bozze
  nbozze=$(conta_bozze)
  if [ "$nbozze" -gt 0 ]; then
    echo -e "${YELLOW}Nota: ci sono $nbozze bozze. NON andranno online (è corretto così).${NC}"
    echo ""
  fi

  read -p "Procedere? [S/n]: " conf
  [ "$conf" = "n" ] || [ "$conf" = "N" ] && { echo "Annullato."; read -p "Premi INVIO..."; exec bash "$0"; }

  echo -e "${BOLD}Descrizione modifiche:${NC}"
  read -e -p "> " -i "Aggiornamento contenuti" msg

  echo ""; echo "Pubblicazione..."
  git add . && git commit -m "$msg" && git push

  if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}Pubblicato! Siti aggiornati entro 2-3 minuti.${NC}"
    echo -e "${YELLOW}Dopo 3 min, apri il sito e premi Ctrl+F5.${NC}"
  else
    echo -e "${RED}Errore! Prova: git pull --rebase && git push${NC}"
  fi
  ;;

# ══════════════════════════════════════════
# 20) STATO
# ══════════════════════════════════════════
20)
  echo ""; cd "$SITO_DIR"; git status; echo ""; echo -e "${BOLD}Ultime 10:${NC}"; git log --oneline -10
  ;;

# ══════════════════════════════════════════
# 21-26) LINK
# ══════════════════════════════════════════
21) xdg-open "https://www.protezionecivilegenzano.it/" 2>/dev/null || echo "https://www.protezionecivilegenzano.it/" ;;
22) xdg-open "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions" 2>/dev/null || echo "github.com actions" ;;
23) xdg-open "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano" 2>/dev/null || echo "github.com repo" ;;
24) xdg-open "https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" 2>/dev/null ;;
25) xdg-open "https://activepager.com/auth/login" 2>/dev/null || echo "activepager.com" ;;
26) xdg-open "https://claude.ai" 2>/dev/null || echo "claude.ai" ;;

# ══════════════════════════════════════════
# 27) STRUTTURA
# ══════════════════════════════════════════
27)
  echo ""
  echo -e "${BOLD}STRUTTURA DEL SITO${NC}"
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
  echo "Articoli: title, date, badge, description (obbligatori)"
  echo "          priorita, autore, image, area, scadenza, allegati, draft"
  ;;

# ══════════════════════════════════════════
# 28) GUIDA
# ══════════════════════════════════════════
28)
  [ -f "$SITO_DIR/GUIDA-UPLOAD-V2.md" ] && less "$SITO_DIR/GUIDA-UPLOAD-V2.md" || echo "Guida non trovata."
  ;;

0) echo -e "\n${GREEN}Arrivederci!${NC}"; exit 0 ;;
*) echo -e "\n${RED}Opzione non valida.${NC}" ;;
esac

echo ""
read -p "Premi INVIO per tornare al menu..."
exec bash "$0"
