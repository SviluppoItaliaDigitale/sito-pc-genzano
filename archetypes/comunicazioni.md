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

# ── DOWNLOAD AUTOMATICO FOTO DA FONTI LIBERE (opzionale) ──
# Se scrivi l'articolo da mobile / app cloud (sandbox blocca i domini esterni),
# lascia `image: ""` e aggiungi qui sotto UN marker TODO. Al prossimo push su
# main, il workflow `scarica-foto-automatica.yml` esegue il comando, scarica
# la foto, applica la fascia blu, popola image: + image_credit: +
# image_source_url:, rimuove la riga marker. Fonti supportate:
#
#   # TODO-foto-wikipedia: bash scripts/foto-da-wikipedia.sh "Titolo Wikipedia" slug-articolo [lang]
#   # TODO-foto-nasa:      bash scripts/foto-da-nasa.sh      "search query"     slug-articolo
#   # TODO-foto-usgs:      bash scripts/foto-da-usgs.sh      shakemap <eventid> slug-articolo
#
# Esempi:
#   # TODO-foto-wikipedia: bash scripts/foto-da-wikipedia.sh "Terremoto del Friuli del 1976" 2026-05-06-friuli-1976
#   # TODO-foto-nasa:      bash scripts/foto-da-nasa.sh      "Etna eruption"                  2026-08-12-etna
#   # TODO-foto-usgs:      bash scripts/foto-da-usgs.sh      shakemap us10006g7d              2026-08-24-amatrice-shakemap

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

