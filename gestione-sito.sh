#!/bin/bash
# ============================================================
# GESTIONE SITO — Protezione Civile Genzano di Roma
# v2.9 — 9 maggio 2026
# Changelog v2.9:
#   - voce 21: aggiunto git pull --ff-only automatico all'inizio.
#     Recupera modifiche fatte da altre sessioni (mobile/cloud)
#     prima di rigenerare il contesto, così il file su Scrivania
#     riflette sempre lo stato di GitHub. Se ci sono conflitti
#     o modifiche locali pending, avvisa ma procede col locale.
#
# Changelog v2.8 (9 maggio 2026):
#   - voce 21 "Esporta contesto per altra AI" ora chiede QUALE
#     AI userai (Gemini / ChatGPT / Claude web) e adatta la
#     procedura ai limiti di contesto di ognuna:
#       Gemini (2M token)   → FULL via paste
#       ChatGPT (128k tok)  → SLIM via paste, OPPURE FULL come
#                             allegato drag-drop dalla Scrivania
#       Claude web (200k)   → FULL via paste
#   - export-contesto-ai.sh nel repo ora supporta flag --slim
#     che genera CONTESTO-AI-slim.md (~250 KB / ~64k token):
#     solo regole editoriali (01,02,03,06,07) + README + CLAUDE
#     + PIANO + memorie. Esclude rules tecniche (04*/05/08),
#     manuale split, workflow YAML, scripts. Stessa efficienza
#     per la scrittura testi, ma sta in ChatGPT Plus.
#
# Changelog v2.7 (9 maggio 2026):
#   - rimossa sezione BOZZE (voci 5-8) coerentemente con la
#     regola progetto "niente articoli in revisione"
#   - voce 1 "Crea nuova comunicazione": tolta la scelta
#     bozza/pubblicata; gli articoli sono SEMPRE draft:false
#   - rimossa la voce "Test sito con bozze visibili"
#   - aggiunta voce 21 "Esporta contesto per altra AI"
#   - menu rinumerato: ora 23 voci attive (era 27)
#
# Changelog v2.6 (9 maggio 2026):
#   - menu: ogni voce ha una descrizione tra parentesi
#   - sezione LINK RAPIDI: split su righe singole per coerenza
#
# Changelog v2.5 (26 aprile 2026):
#   - voce 7 "Pubblica bozza": rispetta la calendarizzazione
#   - voce 24: ActivePager → Smoke test sito live
#   - voce 26 "Struttura sito": aggiornata
#   - voce 27 "Guida pubblicazione": link a MANUALE-SITO.md
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

lista_comunicazioni() {
  local files=()
  for f in "$CONTENT_DIR/comunicazioni/"*.md; do
    [ "$(basename "$f")" = "_index.md" ] && continue
    [ ! -f "$f" ] && continue
    files+=("$(basename "$f")")
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
  echo "║   v2.9 — $(date '+%d/%m/%Y %H:%M')                              ║"
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
  echo ""

  echo -e "${CYAN}── COMUNICAZIONI ──${NC}"
  echo "  1) Crea nuova comunicazione         (nuovo articolo guidato — sempre pubblicato)"
  echo "  2) Crea comunicazione da file Word  (mostra i comandi pandoc per convertire un .docx)"
  echo "  3) Modifica comunicazione           (apre con nano un articolo del sito)"
  echo "  4) Elimina comunicazione            (cancella definitivamente un articolo)"
  echo ""
  echo -e "${CYAN}── PAGINE ──${NC}"
  echo "  5) Modifica qualsiasi pagina        (apre con nano una pagina del sito, escluse le comunicazioni)"
  echo "  6) Crea nuova pagina                (genera content/<sezione>/_index.md con frontmatter base)"
  echo "  7) Elimina pagina                   (cancella una pagina del sito — attento alle pagine principali)"
  echo ""
  echo -e "${CYAN}── EMERGENZA ──${NC}"
  echo "  8) Attiva emergenza                 (mostra il banner rosso in homepage e attiva la modalità)"
  echo "  9) Modifica emergenza attiva        (apre data/emergenza.json con nano per ritoccare i testi)"
  echo " 10) Sospendi emergenza               (nasconde il banner; i dati restano per riattivarla dopo)"
  echo ""
  echo -e "${CYAN}── ALLERTA METEO ──${NC}"
  echo " 11) Imposta livello allerta          (scrive data/allerta.json: verde / giallo / arancione / rossa)"
  echo ""
  echo -e "${CYAN}── PUBBLICA E TESTA ──${NC}"
  echo " 12) Test sito in locale              (hugo server su http://localhost:1313)"
  echo " 13) Pubblica modifiche online        (git add+commit+push → deploy Aruba in 2-3 minuti)"
  echo " 14) Stato repository                 (git status + ultimi 10 commit)"
  echo ""
  echo -e "${CYAN}── LINK RAPIDI ──${NC}"
  echo " 15) Sito produzione                  (apre https://www.protezionecivilegenzano.it/)"
  echo " 16) GitHub Actions                   (stato dei deploy e dei workflow automatici)"
  echo " 17) Repository GitHub                (codice sorgente del sito)"
  echo " 18) Bollettino Lazio                 (Centro Funzionale Regionale: allerte ufficiali)"
  echo " 19) Smoke test sito                  (verifica che le pagine principali rispondano 200 OK)"
  echo " 20) Avvia Claude Code                (lancia l'assistente AI in questo progetto, /exit per tornare)"
  echo ""
  echo -e "${CYAN}── ALTRE AI (Gemini, ChatGPT, Claude web) ──${NC}"
  echo " 21) Esporta contesto per altra AI    (scegli AI → genera + copia in appunti + apre il sito)"
  echo ""
  echo -e "${CYAN}── SOCIAL (assistito, human-in-the-loop) ──${NC}"
  echo " 24) Pubblica bozze social di un articolo  (apre 4 tab + appunti, tu fai Ctrl+V e Pubblica)"
  echo " 25) Stato opencli                         (verifica daemon + estensione Chrome + livello B)"
  echo ""
  echo -e "${CYAN}── SLIDE E PDF (open-design, locale) ──${NC}"
  echo " 26) Avvia open-design (web UI locale)     (slide deck, brochure, mockup per formazione/scuole)"
  echo ""
  echo -e "${CYAN}── GUIDE ──${NC}"
  echo " 22) Struttura del sito               (panoramica menu, badge, workflow, data files)"
  echo " 23) Guida pubblicazione              (apre MANUALE-SITO.md con less)"
  echo ""
  echo -e "${YELLOW}  0) Esci${NC}                              (chiude il menu e torna al terminale)"
  echo ""
}

# ══════════════════════════════════════════
mostra_menu
echo -ne "${BOLD}Scegli [0-23]: ${NC}"
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
    echo -e "Per mandarlo online: opzione ${BOLD}13${NC}."
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
# 5) MODIFICA QUALSIASI PAGINA
# ══════════════════════════════════════════
5)
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
# 6) CREA PAGINA
# ══════════════════════════════════════════
6)
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
# 7) ELIMINA PAGINA
# ══════════════════════════════════════════
7)
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
# 8) ATTIVA EMERGENZA
# ══════════════════════════════════════════
8)
  echo ""
  echo -e "${RED}══ Attiva emergenza ══${NC}"
  echo ""
  titolo_esistente=""; attiva_esistente="False"
  if [ -f "$DATA_DIR/emergenza.json" ]; then
    titolo_esistente=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('titolo',''))" 2>/dev/null)
    attiva_esistente=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('attiva',False))" 2>/dev/null)
  fi

  if [ "$attiva_esistente" = "True" ]; then
    echo -e "${YELLOW}Già attiva! Usa 9 per modificare o 10 per sospendere.${NC}"
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
      echo -e "${GREEN}RIATTIVATA! Per pubblicare: opzione 13.${NC}"
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
  echo -e "${GREEN}ATTIVATA! Per pubblicare: opzione 13.${NC}"
  ;;

# ══════════════════════════════════════════
# 9) MODIFICA EMERGENZA
# ══════════════════════════════════════════
9)
  echo ""; cat "$DATA_DIR/emergenza.json"; echo ""
  echo -e "${YELLOW}Salva: Ctrl+O → INVIO — Esci: Ctrl+X${NC}"
  read -p "INVIO..."; nano "$DATA_DIR/emergenza.json"
  ;;

# ══════════════════════════════════════════
# 10) SOSPENDI EMERGENZA
# ══════════════════════════════════════════
10)
  echo ""
  attiva_em=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('attiva',False))" 2>/dev/null)
  if [ "$attiva_em" != "True" ]; then echo "Non attiva."; read -p "INVIO..."; exec bash "$0"; fi
  titolo_em=$(python3 -c "import json;d=json.load(open('$DATA_DIR/emergenza.json'));print(d.get('titolo',''))" 2>/dev/null)
  echo -e "Sospendere: ${BOLD}$titolo_em${NC}?"
  echo -e "${YELLOW}I dati restano. Riattivabile con opzione 8.${NC}"
  read -p "Confermi? [S/n]: " conf
  if [ "$conf" != "n" ] && [ "$conf" != "N" ]; then
    python3 -c "
import json
with open('$DATA_DIR/emergenza.json','r') as f: d=json.load(f)
d['attiva']=False
with open('$DATA_DIR/emergenza.json','w') as f: json.dump(d,f,indent=2,ensure_ascii=False)"
    echo -e "${GREEN}SOSPESA. Per pubblicare: opzione 13.${NC}"
  else echo "Annullato."; fi
  ;;

# ══════════════════════════════════════════
# 11) ALLERTA
# ══════════════════════════════════════════
11)
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
# 12) TEST SITO IN LOCALE
# ══════════════════════════════════════════
12)
  echo -e "Browser: ${BOLD}http://localhost:1313/${NC}  Ferma: ${BOLD}Ctrl+C${NC}"
  read -p "INVIO per avviare..."
  cd "$SITO_DIR" && hugo server
  ;;

# ══════════════════════════════════════════
# 13) PUBBLICA
# ══════════════════════════════════════════
13)
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
# 14) STATO
# ══════════════════════════════════════════
14) cd "$SITO_DIR"; echo ""; git status; echo ""; echo -e "${BOLD}Ultime 10:${NC}"; git log --oneline -10 ;;

# ══════════════════════════════════════════
# 15-20) LINK RAPIDI
# ══════════════════════════════════════════
15) xdg-open "https://www.protezionecivilegenzano.it/" 2>/dev/null || echo "protezionecivilegenzano.it" ;;
16) xdg-open "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions" 2>/dev/null ;;
17) xdg-open "https://github.com/SviluppoItaliaDigitale/sito-pc-genzano" 2>/dev/null ;;
18) xdg-open "https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini-allertamenti" 2>/dev/null ;;
19)
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
20)
  echo ""
  echo "Avvio Claude Code nel progetto Sito PC Genzano..."
  echo "(per uscire scrivi /exit, tornerai a questo menu)"
  echo ""
  cd ~/sito-pc-genzano && claude
  ;;

# ══════════════════════════════════════════
# 21) ESPORTA CONTESTO PER ALTRA AI
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
21)
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
      echo "     - per rifinitura tecnica: voce 20 (Avvia Claude Code)"
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
# 22) STRUTTURA
# ══════════════════════════════════════════
22)
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
  echo "Accessibilità e Supporti: Abili a Proteggere, Facile da Leggere"
  echo "Volontariato: Diventa Volontario, Chi Siamo"
  echo "Risorse: FAQ, Strumenti, Area Download, Normativa, Glossario,"
  echo "         Standard ISO, Mappa del Sito"
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
# 23) GUIDA
# ══════════════════════════════════════════
23)
  if [ -f "$SITO_DIR/MANUALE-SITO.md" ]; then
    less "$SITO_DIR/MANUALE-SITO.md"
  elif [ -f "$SITO_DIR/CLAUDE.md" ]; then
    less "$SITO_DIR/CLAUDE.md"
  else
    echo -e "${RED}MANUALE-SITO.md non trovato in $SITO_DIR.${NC}"
  fi
  ;;


24)
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

25)
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

26)
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

0) echo -e "\n${GREEN}Arrivederci!${NC}"; exit 0 ;;
*) echo -e "\n${RED}Non valida.${NC}" ;;
esac

echo ""
read -p "Premi INVIO per tornare al menu..."
exec bash "$0"
