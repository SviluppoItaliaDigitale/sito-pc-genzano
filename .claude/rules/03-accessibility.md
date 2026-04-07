# Accessibilità

## Standard di riferimento

Il sito della PA deve rispettare almeno WCAG 2.2 livello AA.
Il riferimento normativo è la Legge Stanca (L. 4/2004) e il D.Lgs. 106/2018.
La dichiarazione di accessibilità è obbligatoria per i siti della PA.

## Checklist obbligatoria per ogni intervento

Per ogni modifica a template, layout o contenuto, verifica sempre:

### HTML semantico
- Uso corretto degli elementi HTML5 (header, nav, main, section, article, aside, footer)
- Gerarchia dei titoli corretta: un solo H1 per pagina, H2/H3 in ordine logico, nessun salto
- Landmark ARIA presenti e non ridondanti
- Skip link ("Vai al contenuto principale") presente e funzionante

### Navigazione e interazione
- Tutti gli elementi interattivi raggiungibili da tastiera (Tab, Shift+Tab, Enter, Spazio, frecce)
- Focus visibile e chiaramente percepibile (non eliminare outline senza sostituzione)
- Ordine di lettura/navigazione coerente con la struttura visiva
- Nessuna trappola da tastiera

### Immagini e media
- Alt text significativo per immagini informative (descrive il contenuto, non "immagine di...")
- Alt vuoto (`alt=""`) per immagini puramente decorative
- Nessuna informazione veicolata solo tramite immagini senza alternativa testuale
- Trascrizioni o sottotitoli per contenuti audio/video quando presenti

### Testo e contrasto
- Rapporto di contrasto minimo 4.5:1 per testo normale, 3:1 per testo grande (18pt+ o 14pt+ grassetto)
- Non affidarsi solo al colore per veicolare informazioni critiche (es. stato allerta)
- Dimensioni testo scalabili (usa rem/em, non px fissi)

### Form e controlli
- Ogni campo ha una `<label>` associata correttamente
- Errori descritti testualmente, non solo con colore o icona
- Messaggi di errore chiari e contestuali
- Attributi `autocomplete` dove opportuno

### Link e pulsanti
- Nessun link con testo generico ("clicca qui", "leggi", "scopri di più") senza contesto
- Icone-link o icone-pulsante con `aria-label` o `title` descrittivo
- Link a documenti: indicare tipo e dimensione (es. "Ordinanza sindacale (PDF, 120 KB)")
- Link che aprono nuova finestra: segnalarlo nel testo o con aria-label

### Componenti dinamici
- Componenti ARIA (modale, accordion, dropdown, tab) implementati con pattern corretti
- Aggiornamenti dinamici annunciati tramite aria-live quando necessario
- Nessun contenuto che lampeggi più di 3 volte al secondo

### Accessibilità cognitiva
- Istruzioni chiare e complete
- Feedback comprensibili anche senza esperienza tecnica
- Consistenza di navigazione e denominazione tra le pagine
- Evita animazioni aggressive o continue (rispetta `prefers-reduced-motion`)

## Regole specifiche per Bootstrap Italia

Bootstrap Italia è conforme a WCAG 2.1 AA. Usa i componenti nativi senza alterare le classi di accessibilità.
Non sovrascrivere CSS che gestiscono focus, contrasto o visibilità per screen reader.
Segui i pattern ufficiali del design system .italia per card, hero, alert, accordion, form.

## Divieti

- Non eliminare il focus outline senza fornire un'alternativa visibile equivalente.
- Non lasciare immagini senza attributo alt (nemmeno nelle immagini decorative: usa `alt=""`).
- Non usare tabelle per il layout.
- Non affidarsi solo a JavaScript per funzionalità critiche senza fallback.
- Non introdurre componenti dinamici senza test da tastiera.
