---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
description: ""

# ── TIPO DI COMUNICAZIONE ──
# Badge visivo: Allerta | Avviso | Comunicazione | Attività | Formazione | Evento | Volontariato
badge: "Comunicazione"

# ── PRIORITÀ ──
# urgente = bordo rosso e posizione in evidenza | normale = aspetto standard
priorita: "normale"

# ── AUTORE ──
# Chi ha scritto o approvato la comunicazione
autore: "Gruppo Comunale Volontari PC Genzano"

# ── IMMAGINE ──
# Percorso immagine di copertina (opzionale)
# Es: /images/nome-immagine.jpg
image: ""

# ── SCADENZA ──
# Data dopo la quale la comunicazione non è più attuale (opzionale)
# Formato: 2026-12-31
# Se compilata, compare un avviso "Comunicazione scaduta" dopo questa data
scadenza: ""

# ── AREA INTERESSATA ──
# Zona geografica a cui si riferisce (opzionale)
# Es: "Tutto il territorio comunale", "Zona centro", "Frazione Landi"
area: ""

# ── ALLEGATI ──
# Lista di file PDF allegati (opzionale)
# Es:
# allegati:
#   - titolo: "Ordinanza sindacale"
#     url: "/documenti/ordinanza.pdf"
allegati: []

# ── IMPOSTAZIONI ──
draft: false
---

Scrivi qui il contenuto della comunicazione.
