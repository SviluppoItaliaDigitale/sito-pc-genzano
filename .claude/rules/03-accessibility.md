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

## Pittogrammi standardizzati ISO 7010 e ARASAAC

Il sito ha una **libreria di pittogrammi standardizzati** disponibile via shortcode `{{< pittogramma >}}` per affiancare i testi e renderli comprensibili anche a bambini, persone straniere, persone con disabilità cognitive, anziani.

**Due librerie:**
- **ISO 7010** — pittogrammi internazionali di sicurezza (PD/CC0). In `static/pittogrammi/iso7010/`. Codici W (warning), P (prohibition), M (mandatory), E (escape/safe condition), F (fire).
- **ARASAAC** — pittogrammi AAC per disabilità cognitive (CC BY-NC-SA 4.0, attribuzione obbligatoria). In `static/pittogrammi/arasaac/`. Si usano principalmente nella pagina `/facile-da-leggere/`.

**Catalogo pubblico:** `/pittogrammi/`. **Download script:** `scripts/scarica-pittogrammi.sh` (idempotente, scarica solo i mancanti; usa `--force` per ri-scaricare tutto).

**Regole operative:**
- Il pittogramma **non sostituisce mai il testo**: è un complemento. L'attributo `alt` deve sempre essere testuale e equivalente (WCAG 1.1.1).
- I pittogrammi sono marcati **funzionali**, non decorativi: restano visibili anche con la preferenza "Nascondi immagini" del toolbar di accessibilità.
- Massimo 3-4 pittogrammi per pagina (evitare sovraccarico visivo).
- Per ARASAAC è obbligatoria l'attribuzione su ogni pagina che li usa.

Documentazione completa: `MANUALE-SITO.md` Parte 3.16.

## Strumenti di Accessibilità (toolbar utente)

Il sito ha un **toolbar di accessibilità** nativo, presente su tutte le pagine come bottone rotondo blu (FAB) in basso a sinistra. Apre un dialog con preferenze di lettura: dimensione testo (4 livelli), allineamento, carattere ad alta leggibilità, spaziatura ampia, contrasto (alto/invertito), scala di grigi, nascondi immagini decorative, pausa animazioni, evidenzia link, cursore grande. Le preferenze sono salvate in `localStorage` e applicate come classi `html.a11y-*`.

Per la struttura dei file, le regole di estensione e i divieti operativi vedi `04-hugo-architecture.md` sezione "Strumenti di Accessibilità".

**Principio:** il toolbar è uno strumento di **preferenze utente** sopra a un sito **già conforme WCAG 2.2 AA**. Non sostituisce l'accessibilità nativa: la integra. **Non è un overlay commerciale** (tipo AccessiBe, UserWay, Equally AI), che il W3C-WAI e le associazioni delle persone con disabilità sconsigliano perché mascherano problemi invece di risolverli.

**Regole operative:**

- Quando si modifica un componente del sito, controllare che funzioni anche con il toolbar attivo: in particolare con **contrasto invertito** (sfondo nero, testo bianco), **scala di grigi**, **immagini nascoste** e **pausa animazioni**.
- Le icone funzionali (Bootstrap Icons) restano visibili anche con "Nascondi immagini" attivo: solo `<img>`, `<picture>`, `<video>`, `<iframe>` e SVG decorativi sono nascosti.
- Il FAB ha posizione **bottom-left** per non collidere con `back-to-top` (right) né con `sos-112` (right su mobile). Mantenere questa convenzione.
- La pagina pubblica `/accessibilita/` descrive il toolbar al cittadino e va tenuta allineata se si aggiungono o tolgono funzioni.

## Divieti

- Non eliminare il focus outline senza fornire un'alternativa visibile equivalente.
- Non lasciare immagini senza attributo alt (nemmeno nelle immagini decorative: usa `alt=""`).
- Non usare tabelle per il layout.
- Non affidarsi solo a JavaScript per funzionalità critiche senza fallback.
- Non introdurre componenti dinamici senza test da tastiera.
