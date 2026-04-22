---
title: "{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
description: ""

# ── TIPO DI COMUNICAZIONE ──
# Badge visivo (13 categorie con colore dedicato — altre categorie ricevono un colore automatico):
# Allerta | Avviso | Comunicazione | Attività | Formazione | Evento | Volontariato |
# Radiocomunicazioni | Prevenzione | Esercitazione | Aggiornamento | Informazione | Emergenza
badge: "Comunicazione"

# ── PRIORITÀ ──
# urgente = bordo rosso e posizione in evidenza | normale = aspetto standard
priorita: "normale"

# ── AUTORE ──
# Chi ha scritto o approvato la comunicazione
autore: "Gruppo Comunale Volontari PC Genzano"

# ── IMMAGINE ──
# Percorso immagine di copertina (opzionale)
# Formato: WebP, 1200px larghezza, max 200 KB
# Deve includere la fascia blu istituzionale (#003366) con logo + testo ufficiale
# Specifiche complete: MANUALE-SITO.md — Parte 3
# Es: /images/2026-04-20-titolo.webp
image: ""

# ── TESTO ALTERNATIVO IMMAGINE (a11y) ──
# Descrive cosa si vede nell'immagine per chi usa screen reader.
# Non ripetere il titolo: descrivi il contenuto visivo.
# Se vuoto, viene usato il titolo come fallback.
image_alt: ""

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
# Il campo `dimensione` è opzionale ma raccomandato (WCAG 3.3.5 Help).
# Es:
# allegati:
#   - titolo: "Ordinanza sindacale"
#     url: "/documenti/ordinanza.pdf"
#     dimensione: "120 KB"
allegati: []

# ── IMPOSTAZIONI ──
draft: false
---

Scrivi qui il contenuto della comunicazione.
