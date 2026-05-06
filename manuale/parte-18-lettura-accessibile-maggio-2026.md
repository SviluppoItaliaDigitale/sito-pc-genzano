_[Indice manuale](README.md)_

# Parte 18 — Lettura accessibile per fasce deboli (maggio 2026)

### 18.1 Perché esiste

A maggio 2026 abbiamo esteso gli strumenti di lettura del sito per coprire in modo
sistematico **anziani, dislessici, parlanti italiano L2, bambini in lettura lenta
e persone in stress da emergenza**. Prima esisteva un bottone TTS attivo solo su
21 pagine (opt-in con `tts: true`); ora il sostegno alla lettura è **default ON
su tutto il sito** e si compone di **cinque strumenti integrati**:

1. **Bottone TTS "Leggi ad alta voce"** su tutte le pagine
2. **Velocità regolabile** (lento / normale / veloce)
3. **Tempo di lettura stimato** sopra ogni articolo
4. **Sillabazione automatica** del testo
5. **Glossario inline con popover** sulla prima occorrenza dei termini PC

Tutti e cinque sono nativi del browser, gratuiti, senza dipendenze esterne, niente
API a pagamento. Niente overlay commerciali (AccessiBe, UserWay, Equally AI), che
il W3C-WAI sconsiglia perché mascherano problemi invece di risolverli.

> **Storico — feature rimossa il 2 maggio 2026.** Inizialmente la lista
> includeva un sesto strumento, il **toggle "Segui parole"** che evidenziava
> la parola in lettura via `SpeechSynthesisUtterance.onboundary 'word'`.
> È stato rimosso perché Chrome/Edge con voci cloud Google (default per la
> maggioranza degli utenti italiani) non emettono mai quell'evento, e Safari
> iOS lo emette in modo intermittente — il toggle era invisibile per ~70%
> degli utenti. Vedi § 18.5 e § 18.12 per i dettagli del bug e perché non
> era recuperabile con compromessi accettabili.

---

### 18.2 Cosa vede il cittadino

Su ogni pagina del sito (esclusa la blacklist legali/tecniche) compare in cima al
contenuto:

- una pillola **"Lettura: ~3 minuti"**
- un bottone **"Leggi ad alta voce"** con icona altoparlante
- un selettore **velocità** (Lento / Normale / Veloce — segmented control)

Cliccando il bottone, la voce italiana del browser legge l'articolo.

Inoltre, quando il cittadino legge il testo da solo, alla **prima occorrenza** di
ogni sigla o termine specialistico (es. **DPC**, **COC**, **AeDES**, **IT-alert**,
**CFR**) il termine appare **sottolineato tratteggiato in blu** con accanto una
piccola icona ⓘ. Cliccando o tappando si apre un riquadro con la **definizione
breve in italiano AGID** + link "Scopri di più nel glossario".

---

### 18.3 Cosa è attivo, cosa è escluso

**Default ON** su tutte le pagine Hugo (single + list) con almeno 30 parole di
contenuto.

**Pagine escluse** (blacklist hard-coded nei template):

| Pagina | Motivo |
|---|---|
| `/privacy/` | Pagina legale, non utile da leggere ad alta voce |
| `/note-legali/` | Idem |
| `/accessibilita/` | Idem |
| `/social-media-policy/` | Idem |
| `/mappa-sito/` | Tecnica, è solo un elenco di link |
| `/attribuzioni-pittogrammi/` | Tecnica |
| `/cerca/` | Funzionale (motore di ricerca) |
| `/comunicazioni/` | Pagina di archivio: solo card di articoli, niente prosa da leggere |
| `/glossario/` | Auto-esclusa: se il glossario inline si attivasse qui, ci sarebbe un popover su ogni voce — sarebbe ridondante |

**Per disattivare TTS + glossario su una specifica pagina**, aggiungere nel
frontmatter:

```yaml
tts: false
```

Il flag vale **per entrambi i sistemi** (TTS e glossario): sono accoppiati
intenzionalmente per coerenza UX.

---

### 18.4 Velocità di lettura

Tre opzioni:

| Etichetta | Rate | Quando usare |
|---|---|---|
| **Lento** | 0.75x | Anziani, bambini, italiano L2, primo ascolto di un testo nuovo |
| **Normale** | 0.95x | Default — lievemente più lento del default browser per chiarezza |
| **Veloce** | 1.15x | Chi conosce già il contenuto, ripasso, navigazione veloce |

La scelta è **persistita in `localStorage`** (chiave `pcgenzano-tts-rate`): vale
per tutte le pagine del sito, anche dopo la chiusura del browser.

Cambiare velocità **mentre la lettura è in corso** ferma la lettura e la fa
ripartire dall'inizio alla nuova velocità (Web Speech API non permette di
cambiare il rate "al volo" su un'utterance già in corso).

---

### 18.5 Toggle "Segui parole" — RIMOSSO il 2 maggio 2026

La feature evidenziava la parola in lettura via `<mark class="tts-word-mark">`,
sincronizzata col TTS tramite `SpeechSynthesisUtterance.onboundary 'word'`.

**Perché è stata rimossa:** la Web Speech API specifica che `onboundary` debba
essere emesso ad ogni boundary di parola, ma nella pratica:

- **Chrome desktop / Android con voci cloud Google** (default per la maggioranza
  degli utenti italiani): l'evento `word` non viene **mai** emesso. Bug Chromium
  noto: <https://issues.chromium.org/issues/40195928>
- **Edge** (Chromium): stesso bug.
- **Safari iOS**: emette in modo intermittente, spesso fallisce dopo poche righe.
- **Firefox + voce sistema italiana** e **Safari macOS + voce locale Alice**:
  funzionavano correttamente, ma rappresentano una minoranza degli utenti.

Il fallback graceful (timer 2.5s che disattiva l'highlight se nessun evento
arriva) faceva sì che, per la maggioranza dei nostri utenti, **il toggle fosse
cosmetico**: cambiava colore al click ma le parole non venivano mai evidenziate.
Esperienza incoerente e silenziosamente rotta, peggio di non avere la feature.

**Soluzioni teoriche valutate:**

- *Forzare voci locali (`localService === true`)*: su Linux/Android di solito
  non c'è una voce italiana locale → silenzio totale. Su Mac/Windows ci sono ma
  con qualità peggiore della voce Google. Trade-off scartato.
- *Calcolare i timing word-by-word in JavaScript* (approssimazione client-side):
  desincronizzato in pochi secondi, peggiora invece di aiutare.

**Cosa è rimasto:** il bottone "Leggi ad alta voce" e il selettore velocità
funzionano cross-browser senza problemi e restano. Il toggle e tutta la logica
correlata (`tts-follow-btn`, `tts-word-mark`, `buildTextMap`, `highlightWord`,
`onboundary`, fallback timer) sono stati rimossi dal partial
`leggi-ad-alta-voce.html` (v3.1 → v4.0) e dal CSS `custom.css`.

---

### 18.6 Tempo di lettura

Sopra il contenuto compare una pillola "Lettura: ~N minuti" calcolata da Hugo
con `.ReadingTime` (200 parole al minuto, valore standard PA).

| Pagina lunga (1000 parole) | "Lettura: ~5 minuti" |
| Articolo breve (200 parole) | "Lettura: ~1 minuto" |
| Frase singola (<30 parole) | Nessuna pillola (sotto soglia) |

**Beneficio:** riduce l'**ansia da muro di testo** in anziani, dislessici, L2.
Chi guarda la pagina sa subito quanto tempo gli serve e si organizza.

Calcolo automatico, nessuna configurazione editoriale richiesta.

---

### 18.7 Sillabazione automatica

CSS `hyphens: auto` applicato a `.article-body` e `.list-intro-content` con regole
italiane (lingua dichiarata in `<html lang="it">`). Il browser spezza
automaticamente le parole lunghe a fine riga.

**Esempio**:

| Senza sillabazione | Con sillabazione |
|---|---|
| `Comunicazione di emergenza` <br> `tempestiva` | `Comunicazio-` <br> `ne di emergenza tempestiva` |

**Beneficio:** riduce lo "scoglione" cognitivo di parole troncate brutalmente a
fine riga, migliora il ritmo di lettura per dislessici e L2.

**Esclusioni automatiche:** `<pre>`, `<code>`, `<table>` non vengono mai sillabati
(toponimi, codice, dati tabellari devono restare interi). Per casi speciali
(marchi, nomi propri) si può aggiungere la classe `.no-hyphens` al singolo elemento.

**Compatibilità:** Chrome 88+, Firefox 43+, Safari 5.1+. Browser più vecchi:
fallback al rendering standard senza sillabazione (zero regressione).

---

### 18.8 Glossario inline con popover

**File dati:** `data/glossario.yaml` — fonte unica delle voci (82 voci al
2026-05-06: cresciuto da 61 con audit empirico delle sigle PC ricorrenti
nei contenuti — vedi sessione consolidamento documentata in Parte 21).

**Schema di una voce:**

```yaml
- id: coc                                 # anchor univoco
  termine: "COC"                          # forma canonica visibile
  varianti:                               # tutte le forme da matchare
    - "COC"
    - "Centro Operativo Comunale"
  definizione: "Centro Operativo Comunale: la sala operativa che il Sindaco attiva per gestire un'emergenza sul territorio comunale."
  link: "/glossario/#coc-centro-operativo-comunale"
```

**Cosa succede al caricamento pagina:**

1. Hugo inietta il YAML come JSON in `window.PCGENZANO_GLOSSARIO`.
2. `static/js/glossario-inline.js` costruisce una mega-regex con tutte le varianti
   (ordinata per lunghezza decrescente: "Centro Operativo Comunale" vince su
   "COC" se entrambe sarebbero catturate).
3. Scansiona `.article-body` e `.list-intro-content` (O(N) sulla lunghezza del
   testo).
4. Sostituisce **solo la prima occorrenza** di ogni voce con
   `<button class="gloss-term">termine ⓘ</button>` + `<span class="gloss-popover">`
   nascosto.
5. Il bottone apre il popover su click/tap o hover (desktop).

**Esclusioni dal match:** `<a>`, `<button>`, `<code>`, `<pre>`, `<h1>`, `<kbd>`,
elementi con `aria-hidden="true"`, classi `.no-gloss`, `.tts-wrapper`,
`.gloss-term`. Niente collisioni con link esistenti, codice, intestazioni.

**Solo prima occorrenza:** se un termine appare 10 volte in un articolo, viene
sottolineato solo la prima. Il cittadino lo riconosce subito, non riceve rumore
visivo continuo.

---

### 18.9 Aggiungere o modificare voci nel glossario

**Per aggiungere una nuova voce:**

1. Apri `data/glossario.yaml`
2. Aggiungi un nuovo blocco rispettando lo schema:

```yaml
- id: identificatore-univoco-minuscolo
  termine: "Termine come appare canonicamente"
  varianti:
    - "Sigla"
    - "Espansione completa"
    - "Eventuale plurale"
  definizione: "1-2 frasi AGID, voce attiva, frasi <20 parole, max ~200 caratteri."
  link: "/glossario/#anchor-nel-glossario-completo"
```

3. Salva, committa, pubblica. Al prossimo build il glossario inline lo prende
   automaticamente.

**Per modificare una definizione:** editare in loco la voce, ricommittare. Niente
più nulla.

**Vincoli redazionali (regola 02-content-design-pa):**

- Frasi brevi (<20 parole), voce attiva, niente burocratese
- Max ~200 caratteri (sta nel popover senza scrollbar)
- Niente definizioni-pubblicità ("il nostro Gruppo è leader di…")
- Stile didattico-istituzionale, lo stesso del glossario completo
  `content/glossario/_index.md`

---

### 18.10 Vincoli di copyright (importantissimo)

Le definizioni nel `data/glossario.yaml` sono **parafrasi originali del Gruppo
Comunale**, basate su:

- ✅ **Glossario interno** `content/glossario/_index.md` (già di nostra penna, libero)
- ✅ **Glossario DPC pubblico** (`protezionecivile.gov.it`): opera della PA
  italiana, non proteggibile per copyright (art. 5 L. 633/1941)
- ✅ **Wikipedia in italiano** (CC BY-SA 4.0): riproducibile con attribuzione e
  licenza derivata uguale, ma di norma riformuliamo per stile AGID
- ❌ **Treccani**: testi protetti da copyright (Istituto dell'Enciclopedia
  Italiana). Mai copia-incolla, nemmeno parziale. Solo brevi citazioni
  virgolettate con fonte sono coperte dall'art. 70 L. 633/1941, ma anche in
  questo caso preferiamo parafrasare per stile editoriale uniforme

**Regola operativa:** se durante la stesura consulti Treccani come riferimento,
**riscrivi con parole tue** in stile AGID. La definizione concettuale è un fatto
(non proteggibile), l'espressione testuale Treccani è proteggibile.

---

### 18.11 Compatibilità browser

La sintesi vocale del sito sfrutta la **Web Speech API** del browser. Funziona
su tutti i browser principali, ma alcuni browser orientati alla privacy la
disattivano di proposito per impedire il fingerprinting (la lista delle voci
installate sul SO è una superficie identificativa unica per ogni utente).

| Browser | Lettura vocale | Note |
|---|---|---|
| Google Chrome (desktop, Android) | ✅ funziona | Voci di sistema |
| Mozilla Firefox (desktop, Android) | ✅ funziona | Voci di sistema |
| Apple Safari (macOS) | ✅ funziona | Voci di sistema |
| Apple Safari (iPhone, iPad) | ✅ funziona | Voci di sistema |
| Microsoft Edge | ✅ funziona | Voci di sistema |
| Samsung Internet, Opera, Vivaldi | ✅ funziona | Comportamento Chromium |
| **Tor Browser** | ❌ disabilitata sempre | Scelta di privacy del Tor Project |
| **LibreWolf** | ❌ disabilitata di default | Configurabile dall'utente |
| **Brave** con Shields al massimo | ❌ disabilitata | Scelta di privacy |

**Comportamento del sito:** al caricamento, se `speechSynthesis.getVoices()`
ritorna lista vuota dopo `voiceschanged` o entro 1,8 secondi, il bottone
"Leggi ad alta voce" viene **sostituito automaticamente** da un riquadro
informativo che spiega:

> *"Lettura vocale non disponibile in questo browser. Alcuni browser
> orientati alla privacy (Tor Browser, LibreWolf, Brave con scudo massimo)
> disattivano la sintesi vocale per impedire il riconoscimento del visitatore.
> La funzione resta attiva su Chrome, Firefox, Safari ed Edge."*

Niente errore in console, niente alert popup. L'utente capisce subito che
**non è un difetto del nostro sito** ma una scelta del suo browser. CSS
scoped sezione **TTS FALLBACK v1.0** in `custom.css` (riquadro azzurrino
istituzionale, coerente con popover glossario).

**Per testare il fallback in locale**: aprire la pagina con Tor Browser
oppure simulare disabilitando l'API in DevTools:
```js
Object.defineProperty(window, 'speechSynthesis', { get: () => undefined });
location.reload();
```

---

### 18.12 (sezione storica) — Bug Safari iOS sul "Segui parole"

> Sezione conservata come traccia storica. La feature "Segui parole" è stata
> rimossa il 2 maggio 2026, vedi § 18.5 per le motivazioni complete. Il bug
> Safari iOS qui descritto è uno dei tre fattori che hanno portato alla
> rimozione (insieme al bug Chrome/Edge con voci cloud Google e all'assenza
> di soluzioni di compromesso accettabili).

Su **Safari per iPhone e iPad** il sistema operativo ha un bug noto e
documentato: l'evento `SpeechSynthesisUtterance.onboundary`
(`event.name === 'word'`) **non viene sparato in modo affidabile**:

- A volte non spara mai
- A volte spara solo eventi `sentence` (a livello di frase), non `word`
- A volte spara con offset `charIndex` errato

Il bug è di **WebKit/Apple**, documentato sul WebKit Bugzilla e sui forum
sviluppatori Apple da diversi anni. **Apple non ha ancora fornito un fix
nel momento in cui abbiamo deciso di rimuovere la feature.**

---

### 18.13 Compatibilità con la toolbar di accessibilità

Tutti e sei gli strumenti rispettano le preferenze utente della toolbar:

| Preferenza utente | Comportamento |
|---|---|
| Contrasto invertito | TTS button blu, popover su nero, highlight giallo brillante |
| Alto contrasto | Bordi neri spessi, popover bianco con bordo nero |
| Scala di grigi | Highlight grigio scuro che resta leggibile |
| Pausa animazioni (`prefers-reduced-motion`) | Niente pulse del bottone, niente smooth scroll |
| Dimensione testo +10/+25/+50% | Tutti i componenti scalano in `rem` |
| Carattere ad alta leggibilità | Si applica anche a TTS button e popover |
| Spaziatura ampia | Popover mantiene leggibilità |

Quando si modifica un componente di lettura, **testare sempre con la toolbar
attiva** — in particolare contrasto invertito + reduced-motion.

---

### 18.14 Comportamento in stampa

Tutti i controlli di lettura **scompaiono in stampa**:

- Bottone TTS e selettore velocità → `display: none`
- Tempo di lettura → `display: none`
- Glossario inline → bottoni tornano testo normale, popover sparisce

Stampato, l'articolo è pulito come prima.

---

### 18.15 File coinvolti (architettura tecnica)

| File | Ruolo |
|---|---|
| `data/glossario.yaml` | Voci del glossario (61 al maggio 2026) |
| `static/js/glossario-inline.js` | Parser DOM + popover accessibile |
| `themes/flavour-pcgenzano/layouts/partials/glossario-inline.html` | Inietta JSON Hugo → JS browser |
| `themes/flavour-pcgenzano/layouts/partials/leggi-ad-alta-voce.html` | TTS partial v4.0 (velocità + bottone lettura, niente word highlight) |
| `themes/flavour-pcgenzano/layouts/_default/single.html` | Blacklist + tempo lettura + include partial |
| `themes/flavour-pcgenzano/layouts/_default/list.html` | Idem per list page |
| `themes/flavour-pcgenzano/static/css/custom.css` | 4 sezioni CSS: TTS v2.0, TEMPO DI LETTURA v1.0, SILLABAZIONE v1.0, GLOSSARIO INLINE v1.0 (TTS WORD HIGHLIGHT rimossa il 2 maggio 2026 con la feature "Segui parole") |
| `.claude/rules/03-accessibility.md` | Regola tecnica per Claude Code |

---

### 18.16 Quando NON usare questi strumenti

- **Pagine legali** (privacy, note legali, accessibilità, social-media-policy):
  hanno un linguaggio giuridico denso che non beneficia della lettura ad alta voce
  (TTS le legge male) e contengono già tutti i termini in chiaro (niente sigle).
- **Pagine tecniche/funzionali** (mappa sito, attribuzioni-pittogrammi, cerca):
  non hanno prosa da leggere, sono elenchi o motori di ricerca.
- **Singoli articoli con contenuto poetico, narrativo, o con molte virgolette**
  dove TTS+glossario popolerebbero in modo fuorviante: aggiungere `tts: false`
  nel frontmatter.

---

### 18.17 Domande frequenti redazionali

**D: Devo aggiungere `tts: true` ai miei nuovi articoli?**
R: No. Il TTS è ON di default. Il flag `tts: true` non serve più (e non fa danni
se resta in articoli vecchi).

**D: Voglio aggiungere "Codice della Strada" al glossario inline. Va bene?**
R: Solo se è un termine ricorrente in articoli del nostro sito e c'è una voce
nel `content/glossario/_index.md`. Altrimenti no: il glossario inline serve a
sigle e termini PC specialistici, non a vocabolario generico.

**D: Posso avere un glossario diverso per articoli di emergenza vs articoli
educativi?**
R: No, è uno solo. La differenziazione si fa con `tts: false` se proprio una
pagina specifica deve essere "pulita".

**D: Come testo le definizioni nuove?**
R: `hugo server`, apri qualsiasi articolo che contenga la sigla, verifica che
il popover si apra cliccando, che il testo sia leggibile, che il link
"Scopri di più" porti alla voce giusta del glossario.

**D: Ho aggiunto una sigla ma non viene evidenziata nel mio articolo. Perché?**
R: Verifica che (a) la sigla appaia nel testo dell'articolo (non solo nel titolo
o frontmatter), (b) non sia dentro un link, codice, o intestazione H1, (c) sia
la prima occorrenza nella pagina (non la seconda o successive), (d) il match
case sia coperto dalle `varianti` (es. "covid" e "COVID" sono due varianti se
il testo le scrive così), (e) il build Hugo sia stato rilanciato.

---

_[Indice manuale](README.md)_
