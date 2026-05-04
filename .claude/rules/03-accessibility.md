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
- Pochi pittogrammi per pagina, per evitare sovraccarico visivo.
- Per ARASAAC è obbligatoria l'attribuzione su ogni pagina che li usa.

Documentazione completa: `MANUALE-SITO.md` Parte 3.16.

## Strumenti di Accessibilità (toolbar utente)

Il sito ha un **toolbar di accessibilità** nativo, presente su tutte le pagine come bottone rotondo blu (FAB) in basso a sinistra. Apre un dialog con preferenze di lettura: dimensione testo (livelli), allineamento, carattere ad alta leggibilità, spaziatura ampia, contrasto (alto/invertito), scala di grigi, nascondi immagini decorative, pausa animazioni, evidenzia link, cursore grande, **nascondi pulsanti flottanti** (Assistente virtuale + SOS 112, utile da mobile dove possono coprire il testo). Le preferenze sono salvate in `localStorage` e applicate come classi `html.a11y-*`.

Per la struttura dei file, le regole di estensione e i divieti operativi vedi `04b-hugo-template-css.md` sezione "Strumenti di Accessibilità".

**Principio:** il toolbar è uno strumento di **preferenze utente** sopra a un sito **già conforme WCAG 2.2 AA**. Non sostituisce l'accessibilità nativa: la integra. **Non è un overlay commerciale** (tipo AccessiBe, UserWay, Equally AI), che il W3C-WAI e le associazioni delle persone con disabilità sconsigliano perché mascherano problemi invece di risolverli.

**Regole operative:**

- Quando si modifica un componente del sito, controllare che funzioni anche con il toolbar attivo: in particolare con **contrasto invertito** (sfondo nero, testo bianco), **scala di grigi**, **immagini nascoste** e **pausa animazioni**.
- Le icone funzionali (Bootstrap Icons) restano visibili anche con "Nascondi immagini" attivo: solo `<img>`, `<picture>`, `<video>`, `<iframe>` e SVG decorativi sono nascosti.
- Il FAB ha posizione **bottom-left** per non collidere con `back-to-top` (right) né con `sos-112` (right su mobile). Mantenere questa convenzione.
- La pagina pubblica `/accessibilita/` descrive il toolbar al cittadino e va tenuta allineata se si aggiungono o tolgono funzioni.

## TTS "Leggi ad alta voce" (Web Speech API)

Il sito usa la **Web Speech API browser-native** in tre contesti distinti, tutti basati sullo stesso paradigma (`window.speechSynthesis` + `SpeechSynthesisUtterance`, voce italiana, niente file MP3, niente API key esterne, niente costi). Il W3C-WAI raccomanda questa scelta per la PA al posto degli overlay commerciali (AccessiBe, UserWay, Equally AI), che mascherano problemi invece di risolverli.

### 1. TTS pagine Hugo (partial `leggi-ad-alta-voce.html`) — default ON con blacklist

Pulsante "Leggi ad alta voce" inserito automaticamente in cima al contenuto di **tutte le pagine** del sito (single + list page con contenuto editoriale > 30 parole). Include un **selettore di velocità** (lento 0.75x / normale 0.95x / veloce 1.15x) persistito in `localStorage` (chiave `pcgenzano-tts-rate`). Componente in `themes/flavour-pcgenzano/layouts/partials/leggi-ad-alta-voce.html` (v2.0).

**Default ON** — la logica è invertita rispetto alla v1 (era opt-in via `tts: true`). Da maggio 2026 il bottone appare **ovunque** tranne dove esplicitamente escluso da:

1. **Blacklist hard-coded nel template** (`single.html` + `list.html`):
   - `/privacy/`, `/note-legali/`, `/accessibilita/`, `/social-media-policy/` — pagine legali
   - `/mappa-sito/`, `/attribuzioni-pittogrammi/`, `/cerca/` — pagine tecniche/funzionali
2. **Frontmatter opt-out**: aggiungere `tts: false` a una pagina specifica.
3. **Soglia minima**: pagine con `WordCount ≤ 30` non mostrano il bottone (titolo o pagina ponte priva di contenuto).

Why: il TTS è uno strumento di accessibilità trasversale per anziani, dislessici, italiano L2, bambini in lettura lenta, persone in stress da emergenza. Lasciarlo opt-in significava averlo solo sul ~20% delle pagine (22 pagine su 100+). La blacklist mantiene comunque escluse pagine dove la lettura ad alta voce non è utile (cookie/privacy notice, mappa-sito tecnica, motore di ricerca).

### 2. TTS dentro il "Coach" dei giochi (`giochi/assets/js/coach.js`)

Bottone "🔊 Ascolta i consigli" dentro il dialog del bottone "Consigli per giocare" (presente su tutti i giochi statici di `static/giochi/`). Legge ad alta voce: titolo dialog + regola del gioco + bullet "Come si gioca". Variante mini "🔊 Ascolta" anche nei suggerimenti contestuali sull'errore (Layer 3). API esposta: `window.GameCoach.{speak, stopSpeaking, ttsSupported}`.

### 3. TTS sulle fiabe e storie (`formazione/storie-e-racconti/assets/tts-storia.js`)

Bottone "🔊 Ascolta" nella `.storia-toolbar` di tutte le fiabe in `static/formazione/storie-e-racconti/`. Modulo standalone auto-iniettato (basta includere il `<script>` nell'index.html della storia). Legge `.storia-titolo-principale` + `.storia-corpo`, spezzando il testo in chunk di ~200 caratteri per evitare cut-off su fiabe lunghe (lettura ~4 minuti).

### Caratteristiche accessibilità (comuni ai tre contesti)

- ARIA: `role=button` o `<button>` nativo, `aria-pressed` o `aria-label` dinamico (idle/speaking), `aria-live=polite` per stato annunciato a screen reader.
- Tastiera: bottone nativo, attivabile con Enter/Space, focus visibile (`outline 3px #ffbe2e`). Anche i radio del selettore velocità sono tastiera-navigabili.
- Voce italiana: priorità `it-IT`, fallback qualsiasi voce con `lang.startsWith("it")`, fallback voce default browser.
- Velocità: tre opzioni (**0.75x lento / 0.95x normale / 1.15x veloce**) selezionabili dall'utente accanto al bottone. Persistite in `localStorage` (chiave `pcgenzano-tts-rate`) — la scelta vale per tutte le pagine. Default normale.
- **Toggle "Segui parole" — RIMOSSO il 2 maggio 2026.** La feature dipendeva da `SpeechSynthesisUtterance.onboundary` con `event.name === 'word'`. Bug noto: Chrome/Edge con voci cloud Google (default) **non emettono mai** l'evento (vedi [chromium #40195928](https://issues.chromium.org/issues/40195928)); Safari iOS lo emette in modo intermittente. Per la maggioranza degli utenti italiani (Chrome desktop/Android, Safari iOS) il toggle era invisibile: cambiava colore al click ma le parole non venivano mai evidenziate. Soluzioni teoriche valutate e scartate: forzare voci locali (qualità peggiore o assenti su Linux/Android), calcolo timing client-side (desincronizzato in pochi secondi). Il file partial è ora v4.0 senza la feature, CSS `tts-word-mark` rimosso, doc allineata.
- Stati visivi distinti: idle (outline), speaking (riempito + animazione pulse, rispetta `prefers-reduced-motion`).
- Stop automatico su: page unload, dialog close, ESC, click su altro bottone TTS.
- Fallback graceful: se browser senza Web Speech API, bottone nascosto via `ttsSupported()`.

**Caso d'uso target:** anziani con vista debole, persone in stress/emergenza, parlanti italiano L2, bambini che leggono lentamente, utenti con dislessia.

**Regole operative:**
- Per le **pagine Hugo**: niente da fare. Il TTS è ON di default. Per **disattivarlo** su una pagina specifica aggiungere `tts: false` nel frontmatter. Per **escludere una nuova categoria** (es. nuove pagine legali future) aggiungere il path alla blacklist `$ttsBlacklist` in `single.html` e `list.html`.
- Per **giochi statici**: il TTS dentro il coach è già attivo via `coach.js` su tutti i giochi con `data-coach-game` sul `<body>` — niente da fare manualmente.
- Per **nuove storie/racconti**: includere `<script src="/formazione/storie-e-racconti/assets/tts-storia.js" defer></script>` prima di `</body>` nell'index.html della storia. Il modulo trova `.storia-toolbar` e inietta il bottone.
- **Non aggiungere altri TTS provider** (es. Google Cloud TTS, AWS Polly) che richiedono API key/costo: Web Speech API browser è gratuita, sempre aggiornata col testo, e raccomandata da W3C-WAI per PA.

## Tempo di lettura stimato (`reading-time`)

In cima a ogni pagina con `WordCount > 30` (e non in blacklist TTS) compare un'etichetta discreta del tipo *"Lettura: ~3 minuti"*, calcolata da Hugo con `.ReadingTime` (200 parole/min). Riduce l'ansia da "muro di testo" per anziani, dislessici, italiano L2 e persone che leggono lentamente — chi guarda la pagina sa subito quanto tempo gli serve.

Implementata in `_default/single.html` e `_default/list.html` con la stessa condizione del TTS. CSS scoped sezione **TEMPO DI LETTURA v1.0** in `custom.css`: pill arrotondata azzurro istituzionale, font 0.88rem, nascosta in stampa.

Niente da configurare per pagina: è automatica. Per disattivarla su un caso specifico, condivide la condizione del TTS — `tts: false` la nasconde insieme al bottone.

## Sillabazione automatica (`hyphens: auto`)

Il corpo articolo (`.article-body` su single.html, `.list-intro-content` su list.html) ha sillabazione automatica attivata via CSS `hyphens: auto` con regole italiane (lingua dichiarata in `<html lang="it">`). Beneficio cognitivo per **dislessici e parlanti italiano L2**: meno parole lunghe spezzate brutalmente a fine riga, ritmo di lettura più uniforme.

CSS scoped sezione **SILLABAZIONE AUTOMATICA v1.0** in `custom.css`. Esclusioni tecniche automatiche: `<pre>`, `<code>`, `<table>`, classe utility `.no-hyphens` per casi speciali (toponimi, marchi).

Compatibilità: Chrome 88+, Firefox 43+, Safari 5.1+ (tutti i browser moderni). Su browser senza supporto, il fallback è il rendering standard senza sillabazione (zero regressione).

## Glossario inline con popover

Il sito ha una libreria di voci di glossario (sigle e termini specialistici PC) che il browser **sostituisce automaticamente** alla **prima occorrenza** in ogni pagina con un bottone cliccabile + popover accessibile (definizione breve di 1-2 frasi + link al glossario completo). Aiuta cittadini non tecnici, anziani, italiano L2 e persone in stress da emergenza che incontrano sigle come **DPC**, **COC**, **AeDES**, **IT-alert**, **CFR** senza sapere cosa significhino.

**Architettura:**
- `data/glossario.yaml` — fonte unica delle voci. Ogni voce: `id`, `termine`, `varianti` (lista di forme da matchare), `definizione` (1-2 frasi AGID, max ~200 caratteri), `link` (URL della voce completa nel `/glossario/`).
- `static/js/glossario-inline.js` — al `DOMContentLoaded` scansiona `.article-body` e `.list-intro-content`, costruisce una mega-regex con tutte le varianti (ordinata per lunghezza decrescente per priorità), sostituisce la **prima occorrenza** di ogni termine con `<button class="gloss-term">termine ⓘ</button>` + `<span class="gloss-popover" role="tooltip" hidden>`. Scansione O(N) sulla lunghezza del testo.
- `themes/flavour-pcgenzano/layouts/partials/glossario-inline.html` — inietta `window.PCGENZANO_GLOSSARIO` come JSON statico al build (passa i `link` per `relURL` per compatibilità subpath GitHub Pages) e carica il JS con `defer`.
- CSS scoped sezione **GLOSSARIO INLINE v1.0** in `custom.css`: termine sottolineato tratteggiato blu istituzionale + icona `ⓘ`, popover con triangolino, varianti per toolbar a11y (contrasto invertito, alto contrasto), nascosto in stampa.

**Vincoli di copyright:** le definizioni sono **parafrasi originali** del Gruppo Comunale, basate sul glossario interno `content/glossario/_index.md` (già di sua penna) e sul glossario DPC pubblico (opera della PA italiana → libera, art. 5 L. 633/1941). **Mai copiare da Treccani** o altre opere protette: solo definizioni nostre, anche quando consultate come riferimento. Cf. policy concordata maggio 2026.

**Esclusioni dal match:** il JS salta i nodi dentro `<a>`, `<button>`, `<code>`, `<pre>`, `<h1>`, `<kbd>`, `[aria-hidden="true"]`, `.no-gloss`, `.tts-wrapper`, `.gloss-term`. Così non si sovrappone a link esistenti, codice, intestazioni di pagina, o altri bottoni. Inoltre solo la **prima occorrenza** di ogni termine viene sostituita: niente rumore visivo se "DPC" appare 10 volte in un articolo.

**Pagine escluse (blacklist nel template, identica a TTS):** `/privacy/`, `/note-legali/`, `/accessibilita/`, `/social-media-policy/`, `/mappa-sito/`, `/attribuzioni-pittogrammi/`, `/cerca/`, `/comunicazioni/` (list), `/glossario/` (auto-esclusa per non popolare popover sui termini del glossario stesso). Per disattivare su una singola pagina: `tts: false` nel frontmatter (la condizione è la stessa del TTS).

**Accessibilità del popover:**
- Tastiera: bottone nativo, **Enter/Space** apre, **ESC** chiude (con focus che torna al button), **Tab** esce normalmente (non c'è focus trap, è un popover non-modal).
- ARIA: `aria-expanded` sul button, `aria-describedby` che punta al popover, `role="tooltip"` sul popover, `aria-label` esplicito sul link "Scopri di più nel glossario".
- Mouse: hover su desktop con `pointer:fine` (no hover su touch), click ovunque chiude (delegato).
- Scroll: chiude i popover quando l'utente scrolla, perché la posizione assoluta non li segue.
- Stampa: il bottone torna a testo normale, il popover sparisce.

**Quando aggiungere voci al glossario:**
- Sigle PC ricorrenti che il cittadino non riconosce (DPC, COC, COI, AeDES, AIB, IT-alert, NUE, CFR…).
- Termini tecnici che cambiano significato fra linguaggio comune e tecnico (allerta vs emergenza, magnitudo vs intensità, vulnerabilità vs pericolosità).
- Sigle giuridiche e normative (D.Lgs. 1/2018, OdV, ETS, DPCM, TUSL).

**Regole operative:**
- Aggiungere una voce: editare `data/glossario.yaml` con id univoco, varianti complete (sigla + espansione + plurali), definizione AGID. Niente più nulla — il prossimo build la prende automaticamente.
- Disattivare il glossario su una pagina specifica (es. articolo poetico, schede di servizio): `tts: false` nel frontmatter (esclude TTS + glossario insieme — sono accoppiati intenzionalmente, hanno la stessa logica di blacklist).
- **Evitare definizioni-pubblicità** (mai *"il nostro Gruppo è esperto di X"*): la definizione deve essere **didattica** e **istituzionale**, lo stesso principio del glossario `content/glossario/_index.md`.

Specifiche complete in `MANUALE-SITO.md` (futura parte) e nella regola `02-content-design-pa.md` § "Vocabolario PA".

## Coach dei giochi — onboarding e teoria di rinforzo

Tutti i giochi statici in `static/giochi/{infanzia,primaria,ragazzi}/` hanno un sistema condiviso di **onboarding** + **teoria di rinforzo** che riduce l'abbandono dei bambini che non hanno nozioni di base e rispondono a caso. Ispirato a "Io non rischio" del DPC e alla regola AGID di accessibilità cognitiva.

**Architettura:**
- `static/giochi/assets/css/coach.css` — styling (bottone trigger inline, dialog modale accessibile, suggerimento contestuale, bottone TTS).
- `static/giochi/assets/js/coach.js` — modulo IIFE con manifest dei giochi + dialog accessibile (`role=dialog`, `aria-modal`, focus trap, ESC, click-outside) + hint contestuale + TTS Web Speech API. Auto-init via attributo `data-coach-game="<id>"` sul `<body>` di ogni gioco.

**Tre layer:**

1. **Bottone "💡 Consigli per giocare"** sotto il titolo di ogni gioco. Click → dialog con: regola in 1 frase, "Come si gioca" in bullet, link "Approfondisci sul sito" alla teoria. Tre varianti visive per fascia (rosso infanzia, verde primaria, blu ragazzi).
2. **TTS audio** nel dialog ("🔊 Ascolta i consigli") — vedi sezione TTS sopra.
3. **Hint contestuale su errore**: quando il bambino sbaglia, accanto al bottone "Consigli" appare un riquadro giallo con suggerimento mirato + link "Scopri perché →". API: `window.GameCoach.hint(testo, urlOpz)` chiamata dai singoli giochi nel callback wrong-answer; `clearHint()` su risposta corretta o passaggio a domanda successiva.

**Manifest dei contenuti** in `coach.js` (~voci, 1 per gioco). Ogni voce ha:
- `fascia: 'infanzia' | 'primaria' | 'ragazzi'`
- `titolo`, `regola` (1 frase, italiano AGID)
- `come` (3-6 bullet operativi, voce attiva, frasi <20 parole)
- `teoria` (array di `{titolo, url}` che puntano a pagine già pubblicate sul sito — niente nuova teoria scritta)

**Regole operative:**
- Per **aggiungere un nuovo gioco**: includere `<link rel="stylesheet" href="/giochi/assets/css/coach.css">` + `<script src="/giochi/assets/js/coach.js" defer></script>` + `<body data-coach-game="<id-univoco>">` + voce nel manifest `CONTENUTI` di `coach.js`.
- Per **modificare i consigli** di un gioco esistente: editare la voce nel manifest. Niente cambi al gioco.
- Per **agganciare hint contestuale Layer 3** in un gioco: nel callback wrong-answer, chiamare `if (window.GameCoach && window.GameCoach.hint) { window.GameCoach.hint('testo breve', '/url-teoria/'); }`. Su risposta corretta o nuovo turno, chiamare `clearHint()`.
- I link teoria devono **sempre** puntare a pagine già pubblicate (`content/<slug>/_index.md` o `content/<slug>.md` esistente) — verificato pre-commit.

Specifiche complete di implementazione e mapping per fascia in `MANUALE-SITO.md` Parte 16.

## Pattern di design dei giochi (consolidato maggio 2026)

Dopo l'audit completo del catalogo (giochi rifatti tra aprile e maggio 2026), 4 pattern trasversali si sono dimostrati efficaci e vanno applicati a ogni gioco nuovo o modificato.

### 1. Pool randomizzato + estrazione N

Il pool dei dati (domande, scenari, scene, parole, eventi) deve essere **almeno 2× la quantità mostrata in una singola partita**. Ogni partita estrae `N` random dal pool. Implementazione tipo:

```js
const POOL = [/* 14-24 voci */];
function pescaPartita(){
  const arr = POOL.slice();
  for (let i = arr.length - 1; i > 0; i--){
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr.slice(0, N_PARTITA);
}
```

Why: dopo 1 partita il bambino non deve memorizzare la sequenza. Pool 14 → 6 random ad esempio garantisce ~2.500 combinazioni distinte.

### 2. Spiegazione del PERCHÉ dopo ogni risposta

Ogni voce dei dati ha un campo testuale didattico (`explain`, `perche`, `tip`, `azione`, `motivo`, `spiega` — il nome varia per gioco ma il pattern è lo stesso): 1-2 frasi che dicono **perché** una risposta è giusta o **cosa fare** quando si sente quel suono / si vede quel cartello / si abbina quel concetto. Mostrato nel feedback dopo la scelta del giocatore.

Why: il gioco deve **lasciare qualcosa nel cervello del bambino**, non essere solo decorativo. Un "Bravo!" senza spiegazione non insegna nulla; un "Bravo! perché..." sì.

### 3. Scoring graduato 0/1/3 per scelte ambigue

Per giochi con scelte multiple di qualità diversa (non solo giusto/sbagliato): dare 3 punti alla scelta ottima, 1 alla scelta accettabile-ma-non-ideale, 0 alla scelta sbagliata. Vedi `chiamata-112`, `scelte-difficili`, `cosa-faccio-se`.

Why: in PC molte situazioni hanno una "via giusta" e diverse "vie meno peggio". Il binario giusto/sbagliato perde sfumature.

### 4. Branching parziale di recupero (per giochi a scelte multiple)

Quando un giocatore sbaglia 2+ volte consecutive nello stesso scenario, mostrare un **mini-recupero**: overlay con i 3-4 punti chiave dello scenario, prima di lasciare proseguire. Vedi `cosa-faccio-se` (PAUSA_PUNTI dictionary + `consecutiveErrors` counter + overlay `.pausa-overlay`).

Why: quando un bambino sbaglia ripetutamente sta perdendo il filo. Una pausa esplicativa lo rimette in carreggiata invece di lasciarlo accumulare errori e rinunciare.

### Pattern bonus: cascata di icone vettoriali

Quando un gioco ha bisogno di icone, usa la **cascata di scelta** in ordine:

1. **ISO 7010** (`static/pittogrammi/iso7010/`, 46 SVG ufficiali): per segnali di sicurezza standard. Esempio: estintore, uscita-emergenza, vietato-fumare, casco-protettivo. Coerenza didattica: il bambino vede i segnali REALI che troverà a scuola, in cantiere, al supermercato.
2. **ARASAAC** (`static/pittogrammi/arasaac/`, 125 PNG, CC BY-NC-SA): per concetti narrativi/didattici (azioni, persone, oggetti) dove ISO 7010 non ha un segnale. Esempio: ascensore, cibo, terremoto, persona-anziana.
3. **Bootstrap Icons** (caricato via CDN su tutti i giochi, 2000+ icone, MIT): per icone UI funzionali (badge, frecce, pulsanti, indicatori). Esempio: `bi-fire`, `bi-water`, `bi-shield-check`.
4. **Emoji unicode**: ultimo fallback per concetti che le 3 librerie sopra non coprono. Esempio: 🐱 gatto sull'albero in tartaruga-saggia. Mai per segnali di sicurezza ufficiali (devono essere ISO).

Riferimento concreto: `cartelli-pericolo` ha le domande UNI 7010 con `iso:` che punta al pittogramma ISO ufficiale (vedi PR di maggio 2026); `memory` (primaria) usa ISO 7010 al 100% perché il gioco tratta proprio segnali di sicurezza.

Per ARASAAC ricordare l'attribuzione obbligatoria CC BY-NC-SA 4.0 (pagina `/attribuzioni-pittogrammi/`).

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
