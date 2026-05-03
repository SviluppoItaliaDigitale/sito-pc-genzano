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

# ── IMMAGINE BANNER (cover tipografica con titolo) ──
# LASCIA `image: ""` vuoto. Lo script `auto-cover-mancanti.py` genera
# automaticamente la cover tipografica istituzionale (gradiente blu +
# titolo + badge categoria + fascia con logo) prima del deploy e popola
# `image:` + `image_alt:`. La cover serve per:
#   1. Banner dell'articolo (riconoscibile, sempre col titolo)
#   2. Anteprima Open Graph quando l'URL è condiviso su WhatsApp /
#      Telegram / Facebook / X / LinkedIn
#   3. Fallback in caso di emergenza (pagina lite /emergenza/)
#
# REGOLA INTOCCABILE: il banner mostra SEMPRE il titolo. Le foto
# (utente, Wikipedia, NASA, USGS, stock) vanno SEMPRE nel corpo
# articolo come {{< foto src="..." alt="..." caption="..." >}}, MAI
# nel campo image: del frontmatter. Vedi CLAUDE.md punto 9.
#
# Per inserire foto da fonti ufficiali (Wikipedia/NASA/USGS/NOAA/stock)
# inline nel corpo: chiedi a Claude in italiano naturale (es. "trovami
# una foto gratuita per questo articolo" o "ecco una foto, mettila
# nell'articolo") — l'agent pc-image-fixer fa WebFetch + scarica + fascia
# blu + shortcode {{< foto >}} inline. Mai usare il marker # TODO-foto-*
# (bandito: vedi CLAUDE.md punto 9 e .claude/agents/pc-image-fixer.md).
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

<!--
Per inserire foto evento nel corpo dell'articolo usa SEMPRE lo shortcode foto
(click per ingrandire accessibile, figure/figcaption, alt obbligatorio).
Non usare markdown ![...]() diretto per le foto evento.

Esempio:
{{< foto src="/images/2026-04-20-descrizione.webp"
         alt="Descrizione significativa per screen reader"
         caption="Didascalia opzionale." >}}

Specifiche: MANUALE-SITO.md Parte 3.14
-->

