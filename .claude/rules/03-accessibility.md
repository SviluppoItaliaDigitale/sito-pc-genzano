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

## TTS "Leggi ad alta voce" (Web Speech API)

Pulsante che usa `window.speechSynthesis` per leggere il contenuto della pagina in italiano. Componente in `themes/flavour-pcgenzano/layouts/partials/leggi-ad-alta-voce.html`. Opt-in via frontmatter `tts: true`. Attivo su 12 pagine essenziali (cosa-fare-adesso, numeri-utili, facile-da-leggere, allerte-meteo, piano-familiare + 7 sotto-pagine rischi-prevenzione).

**Caratteristiche accessibilità:**
- ARIA: `role=button`, `aria-pressed` dinamico, `aria-label` che cambia con lo stato (idle/reading/paused), `aria-live=polite` per stato annunciato a screen reader
- Tastiera: bottone nativo, attivabile con Enter/Space, focus visibile (`outline 3px #ffbe2e`)
- Voce italiana: priorità `it-IT`, fallback qualsiasi voce italiana, fallback voce default browser
- Velocità: 0.95x default per chiarezza (più lento del default)
- Stati visivi distinti: idle (outline blu), reading (riempito blu + animazione pulse rispettosa di `prefers-reduced-motion`), paused (outline blu + icona play)
- Esclude da lettura: script, style, code blocks, elementi `aria-hidden`, pittogrammi (sostituiti dalla `caption`)
- Fallback graceful: se browser senza Web Speech API, bottone nascosto via JS

**Caso d'uso target:** anziani con vista debole, persone in stress/emergenza, parlanti italiano L2, bambini che leggono lentamente, utenti con dislessia.

**Regole operative:**
- Per attivare TTS su una nuova pagina: aggiungere `tts: true` nel frontmatter (opt-in esplicito, non automatico)
- Non attivare TTS su pagine legali (privacy, note legali, accessibilità) o tecniche (mappa sito, attribuzioni) — non utili da leggere ad alta voce
- Non aggiungere altri TTS provider (es. Google Cloud TTS, AWS Polly) che richiedono API key/costo: Web Speech API browser è gratuita e sufficiente

## Accessibilità dei post sui social media

Quando il Gruppo pubblica sui canali social istituzionali (Instagram, Facebook, X, Telegram), valgono regole di accessibilità specifiche allineate al **CWA draft CEN/CENELEC** *Guidelines for effective social media messages in crisis and emergency situations* e alla norma **ISO 22329:2021**, complementari al manuale AGID:

- **Alt text obbligatorio** per ogni immagine, infografica, mappa pubblicata. Mai stringa vuota, mai *"Immagine di…"*, mai testo decorativo. L'alt text deve essere equivalente al contenuto informativo dell'immagine (WCAG 1.1.1).
- **Massimo due emoji per post**, e mai con funzione informativa critica. Gli screen reader leggono le emoji come stringhe lunghe e talvolta confuse (*"Faccia che sorride con cuore"*) e non sono universalmente comprensibili.
- **Niente testo dentro l'immagine come unica fonte**: ogni informazione importante è anche nel **testo del post**. L'immagine è ridondanza grafica, non veicolo unico (WCAG 1.4.5 — *Images of Text*).
- **Niente caratteri Unicode decorativi** (`𝐁𝐎𝐋𝐃`, `𝓢𝓬𝓻𝓲𝓹𝓽`, `🅢🅢🅒`, ecc.). Gli screen reader li leggono come *"matematica grassetto B, matematica grassetto O…"* — illeggibili. Usa solo italiano standard. Per enfasi: maiuscole iniziali e parole-chiave, non Unicode.
- **Niente maiuscole continue** in titoli o frasi intere: gli screen reader le leggono come URLA. Usa **Maiuscole iniziali** o **grassetto** dove disponibile.
- **Non solo colore** per il livello di allerta. Il rosso e l'arancione non sono distinguibili da utenti con daltonismo (deuteranopia, protanopia): aggiungere sempre il livello scritto in chiaro nel testo (*"Allerta arancione"*, non solo cerchio arancione nell'immagine).
- **Lingua chiara**: frasi brevi, voce attiva, niente burocratese — coerentemente con il manuale di stile AGID.
- **Lingua dichiarata**: i post in lingua diversa dall'italiano (es. testo bilingue per turisti, eventi internazionali) devono dichiararlo esplicitamente all'inizio (*"In English below"*).

Le specifiche complete sono in `MANUALE-SITO.md` Parte 13.7.5. La pagina pubblica `/social-media-policy/` espone questi principi al cittadino.

## Tabelle accessibili (render hook automatico)

Tutte le tabelle Markdown del sito sono rese dal hook `themes/flavour-pcgenzano/layouts/_default/_markup/render-table.html` che applica automaticamente:

- **`<th scope="col">`** su ogni cella di intestazione (riga `<thead>`) — WCAG 1.3.1 (Info and Relationships).
- **Wrapping in `.table-responsive`** Bootstrap Italia per scroll orizzontale su mobile.
- **Allineamento colonne** preservato dal Markdown (`:---`, `---:`, `:---:`).

**Niente da fare manualmente per ogni tabella**: oltre 400 `<th>` del sito sono gestiti automaticamente. Quando si scrive una nuova tabella in Markdown si usa la sintassi standard:

```markdown
| Numero | Servizio | Quando chiamare |
|---|---|---|
| 112 | NUE | Qualsiasi emergenza |
```

### Quando aggiungere `<caption>` esplicito

Per le **tabelle landing critiche** (`/contatti/`, `/numeri-utili/`, `/chi-siamo/`, eventuali nuove `/cartografia/`) è raccomandato un `<caption>` esplicito che descriva lo scopo della tabella (WCAG 2.4.6 Headings and Labels).

L'attribute syntax di Goldmark `{caption="..."}` **non funziona** sulle tabelle Markdown in Hugo (limitazione del parser). Soluzione: convertire la tabella in **HTML diretto** dentro il file Markdown:

```html
<div class="table-responsive">
<table>
<caption>Numeri di emergenza validi nel Lazio: quale chiamare e in quali casi</caption>
<thead>
<tr><th scope="col">Numero</th><th scope="col">Servizio</th></tr>
</thead>
<tbody>
<tr><td><strong>112</strong></td><td>Numero Unico Emergenze</td></tr>
</tbody>
</table>
</div>
```

Per tabelle in cui il `<caption>` sarebbe ridondante visivamente (es. c'è già un card-header sopra che dice la stessa cosa), usare `class="visually-hidden"` sul caption: nasconde visivamente ma resta accessibile a screen reader e crawler.

CSS scoped sezione **TABLE CAPTION v1.0** in `custom.css` con helper `.visually-hidden` integrato.

### Struttura uniforme delle pagine rischio

Le 7 pagine `/rischi-prevenzione/*` (sismico, idrogeologico, incendio, vento, temporali, blackout, ondate calore) hanno **struttura uniforme** rilevante per accessibilità cognitiva:

1. **Perché è rilevante sul nostro territorio** (contesto)
2. **Cosa fare PRIMA** (preparazione, voce attiva, bullet)
3. **Cosa fare DURANTE** (azione immediata, bullet)
4. **Cosa fare DOPO** (recupero, bullet)
5. **Cosa NON fare** (shortcode `cosa-non-fare`, box rosso)
6. **Chi chiamare** (shortcode `chi-chiamare`, tabella accessibile)

L'ordine fisso permette al cittadino in stress (e allo screen reader user) di **navigare prevedibilmente** tra le 7 pagine: trova sempre le stesse sezioni nello stesso ordine. Coerenza WCAG 3.2.3 (Consistent Navigation) e 3.2.4 (Consistent Identification) applicate al contenuto.

## Divieti

- Non eliminare il focus outline senza fornire un'alternativa visibile equivalente.
- Non lasciare immagini senza attributo alt (nemmeno nelle immagini decorative: usa `alt=""`).
- Non usare tabelle per il layout.
- Non affidarsi solo a JavaScript per funzionalità critiche senza fallback.
- Non introdurre componenti dinamici senza test da tastiera.
