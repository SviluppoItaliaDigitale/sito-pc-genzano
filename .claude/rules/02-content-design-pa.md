# Content Design PA

## Principi di scrittura

Scrivi sempre in italiano corretto, chiaro, sobrio e leggibile.
Evita burocratese, slogan vuoti, frasi troppo lunghe e tecnicismi inutili.
Scrivi pensando a cittadini reali: famiglie, anziani, volontari, scuole, persone fragili, utenti da mobile.
Ogni testo deve aiutare l'utente a capire cosa sta leggendo, cosa deve fare e dove trovare altre informazioni.

## Regole di struttura

- Titoli chiari e informativi (descrivono il contenuto, non lo pubblicizzano).
- Sottotitoli utili all'orientamento.
- Liste solo quando servono davvero, non per frammentare testo continuo.
- Call to action chiare, istituzionali, mai pressanti.
- Evita ripetizioni inutili tra titolo, occhiello e primo paragrafo.
- Mantieni coerenza tra titoli pagina, menu, breadcrumb e corpo del testo.

## Regole lessicali

- Voce attiva preferita alla passiva.
- Frasi brevi: tendenzialmente sotto le 20 parole.
- Usa "tu" o "voi" quando ti rivolgi direttamente al cittadino, se il contesto lo permette.
- Evita nominalizzazioni inutili ("effettuare il pagamento" → "pagare").
- Usa parole comuni al posto di tecnicismi quando possibile.
- Numeri di telefono: scrivi sempre in formato leggibile (es. 06 1234 5678).
- Date: scrivi in formato esteso quando rivolto ai cittadini (es. "martedì 6 aprile 2026"), usa AAAA-MM-GG solo nel frontmatter Hugo.

## Regola critica — formato data nel frontmatter Hugo

Nel frontmatter degli articoli usa SEMPRE il formato `AAAA-MM-GG` (esempio: `2026-04-06`).
NON usare MAI il formato con timezone (esempio: `2026-04-06T03:32:00Z`): causa l'esclusione dell'articolo dalla build Hugo.

## Regole editoriali

- Nessun contenuto ambiguo o non verificato.
- Nessun testo "che sembra giusto": deve essere realmente pubblicabile.
- Correggi i testi proposti dall'utente in modo conservativo, senza tradirne il significato.
- Verifica sempre ortografia, grammatica, punteggiatura e accenti.
- Se il testo originale non rispetta queste regole, riscrivilo prima di proporre pubblicazione.

## Frontmatter obbligatorio per gli articoli (comunicazioni/)

Ogni articolo deve avere tutti i campi previsti dall'archetipo:
- `title`: titolo chiaro e informativo
- `date`: formato AAAA-MM-GG
- `description`: breve sommario (massimo 160 caratteri, utile anche per SEO)
- `badge`: Allerta | Avviso | Comunicazione | Attività | Formazione | Evento | Volontariato
- `priorita`: normale | urgente
- `autore`: "Gruppo Comunale Volontari PC Genzano" (default)
- `image`: percorso immagine o stringa vuota
- `scadenza`: data di scadenza o stringa vuota
- `area`: zona geografica o stringa vuota
- `allegati`: lista di PDF o array vuoto `[]`
- `draft`: false (per articoli pubblicati)
