---
title: "Episodio NN — Titolo dell'episodio"
date: {{ .Date }}
# Numero progressivo dell'episodio (intero). Usato per itunes:episode nel feed.
episodio: 0
# Descrizione breve (1 frase, ~150 caratteri) per l'elenco e per le anteprime.
description: ""
# Descrizione lunga: 2-4 frasi, compare nella pagina episodio e nel feed RSS.
descrizione_lunga: ""
# Durata dell'audio nel formato HH:MM:SS oppure MM:SS.
durata: ""
# URL del file MP3. Convenzione: caricarlo come asset di una GitHub Release
# del repo (2 GB gratis per release) e incollare qui l'URL diretto.
audio: ""
# Dimensione del file MP3 in byte (richiesta da iTunes per il tag enclosure).
# Si ottiene con:  curl -sIL "<url-mp3>" | grep -i content-length
audio_bytes: 0
# Copertina dell'episodio (opzionale): immagine quadrata con fascia blu.
# Se vuota, il feed e la pagina usano la copertina del podcast.
image: ""
image_alt: ""
autore: "Gruppo Comunale Volontari PC Genzano"
draft: false
---

<!-- TRASCRIZIONE COMPLETA dell'episodio.
     Obbligatoria: accessibilità (WCAG 1.2.1 / 1.2.2) + SEO. Scrivere il
     testo integrale di quanto detto nell'audio, con i nomi degli ospiti
     e i punti principali in grassetto. Linguaggio AGID. -->
