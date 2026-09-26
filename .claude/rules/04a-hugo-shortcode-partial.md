# Hugo — Shortcode, Render Hook, Partial

Questo file raccoglie gli **shortcode**, i **render hook Markdown** e i **partial** del tema. Per la struttura del progetto, le regole Hugo fondamentali e i comandi vedi `04-hugo-architecture.md`. Per template, CSS, menu di navigazione e UX vedi `04b-hugo-template-css.md`.

## Shortcode `foto` (immagini nel corpo degli articoli)

Il tema definisce due shortcode: `foto` (foto evento) e `pittogramma` (simboli).

```go-html-template
{{< foto src="/images/AAAA-MM-GG-descrizione.webp"
         alt="Testo alternativo per screen reader"
         caption="Didascalia opzionale" >}}
```

Produce `<figure>` con: immagine cliccabile (apre a dimensione intera in nuova scheda) + `aria-label` sul link ("Apri a dimensione intera: {alt}"), `<figcaption>` opzionale (markdown inline), `loading="lazy"`, responsive (`img-fluid`), funziona senza JS. `src` e `alt` **obbligatori** (mancanza = errore build Hugo).

## Shortcode `pittogramma` (simboli ISO 7010 e ARASAAC)

Inserisce pittogrammi standardizzati per supportare la comprensione del testo a bambini, anziani, persone con disabilità cognitive e parlanti italiano L2 (regola 03 — accessibilità cognitiva).

Uso block (figure centrata con caption opzionale):
```go-html-template
{{< pittogramma src="/pittogrammi/arasaac/terremoto.png"
                alt="Pittogramma: terremoto"
                caption="Cosa fare in caso di terremoto"
                size="large" >}}
```

Uso inline (dentro una frase):
```go-html-template
Chiama il {{< pittogramma src="/pittogrammi/arasaac/112.png" alt="numero 112" inline="true" >}} 112.
```

Parametri:
- `src` (obbligatorio) — percorso pittogramma in `/pittogrammi/iso7010/` o `/pittogrammi/arasaac/`
- `alt` (obbligatorio) — testo alternativo significativo per screen reader (mai stringa vuota: il pittogramma non è decorativo, è esplicativo)
- `caption` (opzionale, solo block) — didascalia visibile sotto
- `inline="true"` — inserimento inline dentro una frase (default: block)
- `size` — `small` (48px) | `medium` (96px, default) | `large` (160px) | `xlarge` (240px)

Produce `<img>` con `role="img"` e `loading="lazy"`, oppure `<figure>` con caption opzionale. CSS scoped in `custom.css` (sezione **PITTOGRAMMI v1.0**) con dimensioni fisse, override mobile (large/xlarge ridotti su <576px), mantenimento colori in stampa (i colori dei segnali ISO 7010 sono parte dell'informazione di sicurezza e non devono essere convertiti in scala di grigi).

**Libreria** (3.3 MB): `static/pittogrammi/iso7010/*.svg` — 46 segnali standard (E* evacuazione, F* antincendio, W* avvertimento, M* obbligo, P* divieto), vettoriali; `static/pittogrammi/arasaac/*.png` — simboli (rischi, autoprotezione, kit, persone, luoghi, veicoli, numeri utili), bitmap 500px. **Re-download**: `bash scripts/scarica-pittogrammi.sh` (idempotente, `--force` per tutto; rate-limit 1s su Wikimedia per evitare ban).

**Attribuzione (obbligatoria):** pagina `/attribuzioni-pittogrammi/` dal footer di tutte le pagine. ARASAAC è CC BY-NC-SA 4.0: le opere derivate (es. **schede stampabili PDF** dei kit) ereditano la stessa licenza. ISO 7010 da Wikimedia: PD-shape/CC0, attribuzione di cortesia.

**Uso editoriale:** il pittogramma è **supporto**, mai sostituto del testo (WCAG 1.4.5); uno per concetto chiave, non decorazione continua; ISO 7010 (P/W/M/F) per obblighi/divieti formali, ARASAAC per situazioni narrative/didattiche per bambini.

## Shortcode `cosa-non-fare` (box divieti per pagine rischio)

Box rosso bordato (`#c1121f`) con icona divieto che evidenzia visivamente i comportamenti DA EVITARE. Aumenta l'efficacia della comunicazione del rischio rispetto ai "non" dispersi nel testo. Usato sulle 7 pagine `/rischi-prevenzione/*`.

```go-html-template
{{< cosa-non-fare titolo="Cosa NON fare in caso di terremoto" >}}
- **Non correre fuori durante la scossa**
- **Non usare gli ascensori**
- **Non usare il telefono per curiosità**
{{< /cosa-non-fare >}}
```

Parametro `titolo` opzionale (default: "Cosa NON fare"). Contenuto Markdown standard. Output: `<div role="region" aria-label="...">` con header colorato + body in lista. Contrasto WCAG AA: testo `#7f1d1d` su `#fff5f5` = 7.7:1. CSS scoped sezione **COSA NON FARE v1.0** in `custom.css`. In stampa diventa nero su bianco mantenendo gerarchia visiva con `page-break-inside: avoid`.

## Shortcode `chi-chiamare` (chiusura standard pagine rischio)

Sezione finale uniforme delle 7 pagine `/rischi-prevenzione/*`: tabella accessibile (`<caption>` + `<th scope="col">`) con i numeri da chiamare per livello di gravità + nota istituzionale che chiarisce la modalità di attivazione del Gruppo.

```go-html-template
{{< chi-chiamare >}}
```

Nessun parametro. Produce un `<section aria-labelledby>` con:
- `<h2>` "Chi chiamare"
- Tabella `caption + thead + tbody`: 3 righe (vita in pericolo → 112, pericolo concreto → 112, segnalazione non urgente → 803 555 Sala Operativa PC Lazio)
- `<a href="tel:112">` su ogni occorrenza del 112 con stile `.chi-chiamare-call` rosso istituzionale + focus visibile (WCAG 2.4.7)
- Alert role=note che chiarisce: *"Il Gruppo Comunale Volontari di PC Genzano non può essere attivato direttamente dai cittadini"* — coerente con regola `06-protezione-civile-scientifica.md` e con le pagine `/contatti/` e `/numeri-utili/`.

CSS scoped sezione **CHI CHIAMARE BOX v1.0** in `custom.css`. In stampa il numero 112 resta nero con underline.

**Struttura uniforme finale delle pagine rischio**: dopo l'introduzione "Perché è rilevante sul nostro territorio" e gli eventuali "Segnali e situazioni tipiche", ogni pagina ha l'ordine fisso **Cosa fare PRIMA → Cosa fare DURANTE → Cosa fare DOPO → `cosa-non-fare` → `chi-chiamare`**. Modello di riferimento per nuovi rischi che dovessero essere aggiunti in futuro.

## Shortcode `link-card` (griglia di card link nei contenuti)

Card link visibile (icona + titolo + descrizione) per griglie di consultazione dentro le pagine markdown, in alternativa all'elenco puntato anonimo. Nato per la sezione "Pagine di consultazione rapida" dell'hub `/rischi-prevenzione/` (la scheda scuolabus non si trovava in un bullet — maggio 2026).

```go-html-template
<div class="consulta-rapida">
{{</* link-card url="/rischi-prevenzione/sicurezza-scuolabus/" icon="bi-bus-front" titolo="Sicurezza sullo scuolabus" desc="Cosa fare in emergenza durante il tragitto." */>}}
... altre card ...
</div>
```

- Parametri: `url` (path interno), `icon` (classe Bootstrap Icons), `titolo`, `desc`. Tutti obbligatori.
- **Subpath GitHub Pages**: il template fa `.Get "url" | strings.TrimPrefix "/" | relURL` (stesso pattern del render-link hook), così i link funzionano sia su Aruba (root) sia su GitHub Pages (`/sito-pc-genzano/`). Scrivere `url` con leading slash.
- Le card vanno avvolte in `<div class="consulta-rapida">` (raw HTML nel markdown), senza righe vuote tra gli shortcode. CSS scoped sezione **CARD CONSULTAZIONE RAPIDA v1.0** in `custom.css` (hover lift, focus visibile `#ffbe2e`, `prefers-reduced-motion` + `a11y-pause-anim`, stampa).

## Shortcode card di /chi-siamo/ — `mezzo-card`, `affiliazione-card`, `card-istituzionale` (luglio 2026)

Tre shortcode nati dall'**audit esterno del 15/07/2026, punto 7 "ridurre l'HTML grezzo nei contenuti Markdown"**: sostituiscono i blocchi HTML Bootstrap ripetuti (con `style=""` inline) di `content/chi-siamo/_index.md`. Producono lo **stesso markup Bootstrap Italia** dei blocchi originali; l'unico cambio è l'`<img>` dei loghi, che usa le utility `d-block mx-auto mb-3` + attributi `width`/`height` al posto dello style inline (resa identica). Si usano **dentro un wrapper `<div class="row ...">` raw, senza righe vuote tra le card** (stesso pattern di `link-card`).

- **`mezzo-card`** (self-closing) — card mezzo/attrezzatura per la griglia "Mezzi e attrezzature principali". Parametri: `nome` e `descrizione` obbligatori; `icona` (default `bi-truck`), `colore` (utility BI dell'icona, default `primary`), `corsivo="true"` per i mezzi in allestimento. Il `nome` resta la fonte canonica delle denominazioni tecniche dei mezzi (rule 02 § "Nomi dei nostri mezzi").
  ```go-html-template
  {{</* mezzo-card colore="danger" nome="Mercedes Actros" descrizione="Autobotte con impianto antincendio da 14.000 litri e distribuzione di acqua potabile." */>}}
  ```
- **`affiliazione-card`** (con inner) — card con logo per "Affiliazioni e riconoscimenti" e "Accreditamenti". Parametri: `logo` (path con leading slash, subpath-safe via `strings.TrimPrefix "/" | relURL`), `alt`, `titolo` obbligatori; `icona` (default `bi-award`), `bordo` (`primary` default, oppure valore CSS es. `var(--pc-secondary)`, `#15803d`), `larghezza`/`altezza` del logo (default `96px`; `larghezza="auto"` per loghi non quadrati). L'inner contiene i paragrafi descrittivi (HTML/Markdown). 🔴 Vincolo Reg. (UE) 2021/888: nella card del Quality Label ESC il codice `E10435833` resta nel testo inner — lo shortcode migra solo il markup, mai i testi.
- **`card-istituzionale`** (con inner) — card con barra colorata a sinistra (`border-start border-4`) per "Riferimenti istituzionali" (titolo `h6`, default) e "Settori operativi" (`classe="h5"`). Parametri: `titolo` e `icona` obbligatori; `classe` (`h6`|`h5`), `colore` (utility BI dell'icona, default `primary`), `bordo` (come sopra).

⚠️ Nota implementativa: l'inner è reso con `.Page.RenderString (dict "display" "block")` e **non** con `markdownify`, perché `markdownify` fa l'unwrap del `<p>` quando l'inner è un solo paragrafo (perdendo i margini del paragrafo nella card). Nessuna CSS aggiunta: bordi e dimensioni variabili sono parametri emessi dal template, il centraggio logo usa utility BI esistenti.

## Componenti Bootstrap Italia — `callout`, `passi`, `timeline`, `galleria` (maggio 2026)

Quattro shortcode di contenuto, AGID/WCAG, applicabili a contenuto già esistente per migliorarne lettura e orientamento.

- **`callout`** — box nota del design system: **usa il componente NATIVO Bootstrap Italia** (`.callout .note/.warning/.danger/.success` + `.callout-inner` + `.callout-title` con icona dallo sprite BI `vendor/bootstrap-italia/svg/sprites.svg`). API autore: `{{</* callout tipo="info|avviso|pericolo|ok" titolo="…" */>}} testo markdown {{</* /callout */>}}` (mappa: info→note, avviso→warning, pericolo→danger, ok→success). 🔴 **Non creare CSS `.callout` custom**: collide col bundle BI (incidente: titolo con `margin-bottom:2.222rem` ereditato). Nessuna CSS custom per il callout.
- **`passi`** (stepper) — avvolge una **lista ordinata Markdown** e la rende con pallini numerati (CSS counter su `<ol>` reale → ordine annunciato dagli screen reader). `{{</* passi titolo="…" */>}}` … lista `1. 2. 3.` … `{{</* /passi */>}}`. CSS sezione **PASSI / STEPPER v1.0**.
- **`timeline`** — avvolge una **lista Markdown** (un evento per voce, di norma `**data/titolo** — testo`) e la rende come linea del tempo verticale con marcatori. CSS sezione **TIMELINE v1.0**.
- **`galleria`** (carosello) — per articoli con **≥4 foto**: avvolge più `{{</* foto */>}}` in un carosello accessibile, **solo avanzamento manuale** (mai autoplay — WCAG 2.2.2), scroll-snap + pulsanti prev/next con `aria-label` disabilitati ai bordi, `static/js/galleria.js` idempotente. CSS sezione **GALLERIA v1.0**.

Utility correlate in `custom.css`: **`.pc-spinner`** (indicatore di caricamento, rispetta `prefers-reduced-motion` + `a11y-pause-anim`; cablato negli stati di caricamento del Laboratorio meteo) e **`.table-sticky`** (intestazione tabella sticky per tabelloni lunghi, `max-height:70vh`).

## Shortcode CAA — `caa-tabella` / `caa-voce` (tabelle di Comunicazione Aumentativa Alternativa, giugno 2026)

Due shortcode per le **tabelle di Comunicazione Aumentativa Alternativa (CAA)**: una griglia di pittogrammi ARASAAC + parola che una persona con **afasia, disabilità cognitiva, non parlante italiano, bambino o anziano in stress** può **indicare** per comunicare in emergenza quando non riesce a parlare. Supporto, mai sostituto del testo (WCAG 1.4.5). Usati nella pagina `/tabelle-comunicazione/` (`content/tabelle-comunicazione/_index.md`), voce di menu sotto **Accessibilità e Supporti**.

- **`caa-tabella`** (wrapper, accetta inner): avvolge una griglia di `caa-voce`. Parametri: `titolo` (consigliato → `<h3 class="caa-board-title">` + `aria-label="Tabella di comunicazione: …"`), `id` (opzionale, ancora HTML — **usato solo se passato esplicitamente**, perché le ancore stanno già sugli H2 della pagina e un id auto-derivato creerebbe duplicati). Markup: `<section class="caa-board">` → `<div class="caa-grid">`.
- **`caa-voce`** (cella, dentro `caa-tabella`): parametri **obbligatori** `src` (pittogramma in `/pittogrammi/arasaac/…`) e `parola` (testo sotto il simbolo **e** `alt`); se manca uno dei due, `errorf` blocca la build. Il leading `/` di `src` è strippato (`strings.TrimPrefix` + `relURL`) per il subpath GitHub Pages. Markup: `<figure class="caa-cell">` con `<img class="caa-cell-img" loading="lazy" decoding="async">` + `<figcaption class="caa-cell-label">`.

```go-html-template
{{< caa-tabella titolo="Ho bisogno di" >}}
{{< caa-voce src="/pittogrammi/arasaac/acqua.png" parola="Acqua" >}}
{{< caa-voce src="/pittogrammi/arasaac/cibo.png" parola="Cibo" >}}
{{< /caa-tabella >}}
```

CSS sezione **TABELLE DI COMUNICAZIONE CAA v1.0** in `custom.css`: `.caa-grid` è CSS Grid responsive (`auto-fill, minmax(130px,1fr)`; 100px su mobile; 4 colonne in stampa), `.caa-board` ha `break-inside: avoid` (ogni tabella su una pagina A4), `.caa-cell` bordo 2px `#003366` + immagine `aspect-ratio 1/1 object-fit:contain`. 🔴 **Accessibilità**: i pittogrammi CAA **restano visibili anche con "Nascondi immagini"** del toolbar (`html.a11y-hide-images img.caa-cell-img { visibility: visible !important }`) perché qui sono **contenuto**, non decorazione. Attribuzione ARASAAC obbligatoria (CC BY-NC-SA 4.0, ereditata dalle tabelle stampate). Vedi `manuale/parte-40-comunicazione-emergenza-accessibile.md`.

## Shortcode `scheda-terremoto` (scheda dettaglio evento sismico)

`themes/flavour-pcgenzano/layouts/shortcodes/scheda-terremoto.html` rende la **scheda di dettaglio di un singolo terremoto** sul modello della pagina evento di `terremoti.ingv.it`. Usato dalla pagina `content/cruscotto/terremoto.md` (URL `/cruscotto/terremoto/`), che riceve l'ID evento via **hash** (`#46107472`) o query (`?event=46107472`).

- **Dati live INGV FDSN** (CORS aperto, fetch dal browser, niente widget di terzi): GeoJSON (`?eventid=<id>&format=geojson`) per il riepilogo; QuakeML (`&includeallmagnitudes=true&includeallorigins=true&includearrivals=false`) per le magnitudo/origini multiple. L'ID evento INGV è in `properties.eventId`; coordinate GeoJSON `[lon, lat, prof]`.
- **Tab accessibili** (pattern ARIA tablist, frecce/Home/End, roving tabindex): Dati evento (mappa epicentro **a piena larghezza** Leaflet self-hosted + griglia parametri `.eq-dati-grid` sotto) · Localizzazioni e magnitudo · Meccanismo di sorgente · Impatto · Sismicità (FDSN bbox ~50 km, ultimi 30 gg) · Cosa fare (autoprotezione sismica + link a `/rischi-prevenzione/rischio-sismico/`) · Download.
- **Prodotti scientifici INGV non ricalcolati** (vincolo: siamo associazione di volontariato, non ente sismologico — coerente con lo schema `Organization`): ShakeMap e meccanismo focale sono **embed ufficiali con attribuzione CC BY-SA** se esistono (img con `onerror` → fallback), altrimenti **deep-link** alla scheda INGV. Per eventi profondi/offshore questi prodotti spesso non esistono.
- **Condivisione/stampa/QR** dal chrome standard di pagina (`page-tools.html`); il tab Download offre QuakeML/GeoJSON + scheda ufficiale INGV.
- CSS scoped in un blocco `<style>` interno allo shortcode (sezione **SCHEDA TERREMOTO v1.0**). La pagina ha `tts: false`, `indice: false`, `build.list: never` (non in liste/RSS/sitemap: è una pagina-strumento che richiede l'hash).
- **Collegamento dal cruscotto**: `dashboard-terremoti.html` cattura `properties.eventId` e linka ogni riga (cella "Zona") e popup mappa a `/cruscotto/terremoto/#<id>` (URL via `relURL | jsonify`).

🔴 **Filtro eventi italiani (`isItaliano`) in `dashboard-terremoti.html`**: l'API INGV chiude il `place` con la provincia tra parentesi, a volte come **sigla** `(CS)`, a volte come **nome esteso** `(Cosenza)`/`(Reggio Calabria)` (tipico degli eventi offshore). Il filtro accetta entrambi (set `PROVINCE_IT` sigle + `PROVINCE_NOMI` nomi estesi) + mari/coste italiane. **Non restringere a sole sigle**: il 1° giugno 2026 un M6.2 "Costa Calabra nord-occidentale (Cosenza)" non compariva perché il filtro accettava solo `(CS)`.

## Leaflet una sola volta per pagina (settembre 2026)

I quattordici shortcode che montano una mappa (`dashboard-terremoti`, `dashboard-incendi`, `dashboard-satellite`, `dashboard-cams`, i quattro `dashboard-italiameteo-*`, `mappa-aree`, `mappa-punto`, `mappa-territorio`, `radar-dpc`, `scheda-terremoto`) includono `vendor/leaflet/leaflet.css` e `leaflet.js` dietro la stessa guardia di `pc-fetch-cache.js`:

```go-html-template
{{ if not (.Page.Store.Get "leafletJs") }}{{ .Page.Store.Set "leafletJs" true }}<script src="{{ $leafletJS }}" crossorigin=""></script>{{ end }}
```

Fino al 14/09/2026 ogni scheda ripeteva link e script: il cruscotto ne conteneva **dieci copie**, e poiché la cache è disattivata (rule 05 — istruzione dell'utente del 12/09/2026) erano dieci scaricamenti veri a ogni visita. L'init inline di ciascuna scheda resta al suo posto e trova `L` già definito, perché gli script classici eseguono in ordine di documento. 🔴 **Un nuovo shortcode con mappa nasce con la guardia**: senza, il conteggio riparte. Verifica: `grep -c '<script src=[^>]*leaflet' public/cruscotto/index.html` deve dare 1.

## Cruscotto — fallback "ultimo dato valido" (`pc-fetch-cache.js`, luglio 2026)

Le 6 schede dati del cruscotto che fanno fetch JSON a runtime (`dashboard-terremoti`, `dashboard-vulcani`, `dashboard-aria`, `dashboard-mare`, `dashboard-ems`, `dashboard-italiameteo-osservazioni`) usano l'helper **`static/js/pc-fetch-cache.js`** (`window.pcCache`: `salva`/`leggi`/`frase`): a ogni fetch riuscito il payload è salvato in `localStorage` (`pcgz-cache:<chiave>`); se la fonte esterna non risponde (tipico durante una crisi su vasta scala), la scheda mostra **l'ultimo dato valido** (max 48h, 72h per EMS) con la riga di stato onesta *"Fonte al momento non raggiungibile — dati dell'ultimo aggiornamento riuscito: GG/MM alle HH:MM"* — mai spacciato per attuale (rule 06) — e continua a ritentare. L'helper è incluso una sola volta per pagina via guardia `.Page.Store "pcCacheJs"` in testa a ciascuno shortcode; ogni uso è protetto da `if(window.pcCache)` quindi le schede funzionano anche senza helper. Le schede a sola immagine (radar/satellite/ECMWF/incendi/CAMS) sono escluse: senza la fonte non c'è immagine da mostrare e i WebP ECMWF sono già self-hosted. Nato dall'audit esterno del 10/07/2026 (raccomandazione "caching aggressivo dei dati con fallback locale").

## Sala situazioni `/monitor/` — la cartina è della vista (23/09/2026)

🔴 **Richiesta dell'utente**: *«quando entro in un tab voglio che mi venga fatto vedere quel tipo di dato specifico e non tutti i dati degli altri tab»*, e *«il menù previsioni ICON-2I con i due bottoni sopra e sotto non deve stare dentro la cartina ma nei menù laterali»*. Fino a quel giorno la barra in alto mescolava nella stessa riga i **tab** (viste) e i **livelli di cartina** (ZONE, RADAR, SISMI, VOLO, ORBITE…), che sembravano tab anche loro: l'utente apriva «VOLO» aspettandosi i filtri degli aerei (che stanno nel pannello EMERGENZE) e in SATELLITI vedeva sismi e zone di allerta ma **nessun satellite**, perché il livello ORBITE era spento e il suo pulsante stava fuori schermo a destra (la freccia contava solo i tab). Il tab non toccava mai la cartina.

**Modello attuale — ogni livello appartiene a UNA vista** (`VISTA_DI` nel sorgente): `zone`→ALLERTA · `radar`, `blitz`, `prev` (campo ICON-2I)→METEO · `mareo`→ARIA·MARE · `qk`→SISMICO · `volo`, `fire`, `fwi`→EMERGENZE · `sat`→CARTE · `orb`→SATELLITI. WINDY, TRAFFICO, NAVI, RADIO, REGISTRO e MIA SALA non hanno livelli.

- **Nella barra restano solo i tab.** I livelli stanno nella striscia **SULLA CARTINA** in testa al pannello della loro vista (`#sideMap`, un gruppo `.smGrp[data-per=<vista>]` per vista; `sideMapSync()` mostra quello della vista aperta e allinea `aria-pressed` a `S.layers`). Gli elementi sono fissi nel documento, non rigenerati a ogni `render()`: chi ha il fuoco su una pastiglia non lo perde. **OGGI/DOMANI** (`#dayTgl`) sta nella striscia di ALLERTA, i due menu **ICON-2I** (`#prevCtl`, con la legenda `#prevLegBox`) in quella di METEO: niente più controlli galleggianti sulla cartina.
- **Un livello è visibile se è acceso nella sua vista E la sua vista è aperta** (`layerVis(k)`; per ICON-2I `prevVis()`). `setView()` richiama `applyLayers()` a ogni cambio, quindi entrando in SATELLITI i satelliti si caricano e si disegnano da soli, in SISMICO restano solo i sismi, in ALLERTA solo le zone. 🔴 Ogni lettura dello stato di un livello passa da `layerVis`, mai da `S.layers.k` direttamente: `S.layers.k` è la *scelta* dentro la vista, non ciò che è sulla cartina (radar, fulmini/WebSocket, ticker, `ORB_TICK`, `worldMode` usano tutti `layerVis`, così il collegamento Blitzortung si chiude uscendo da METEO e i satelliti non si ricalcolano quando nessuno li guarda).
- **`⧉ SOLO LA VISTA`** (`#soloBtn`, in coda ai tab, `aria-pressed`, persistito in `S.solo`): acceso di default. Spento = **composizione libera**: i livelli accesi nelle altre viste restano sulla cartina anche cambiando vista (radar + zone insieme). Si nasconde in modalità muro con la striscia (`body.muro #nav #soloBtn, body.muro #sideMap`).
- **La legenda è dinamica** (`legendUpd()`, tabella `LEGENDA`): elenca solo i livelli davvero visibili adesso, con gli stessi colori dei marcatori, e scrive «NESSUN LIVELLO ACCESO IN QUESTA VISTA» quando la cartina è vuota. Fondo quasi pieno (`.97`), così il contrasto non dipende dalla tessera sotto.
- **Default dei livelli**: acceso ciò che la vista è fatta per mostrare (zone, radar, sismi, mareografi, mezzi aerei, fuochi, satellite NASA, orbite); spenti solo i fulmini (aprono un WebSocket) e AIB previsionale (scala di colori confondibile con l'allerta). 🔴 I **livelli** salvati **prima** del 23/09/2026 (`pcgz-monitor-cfg` senza `v:2`) non si riprendono e tornano ai default (le altre scelte — vista, filtri, radio — sì): avevano orbite, aerei e mareografi spenti per non averli mai trovati.
- **Tasto R** (radar; si spegne con ⌨ TASTI RAPIDI, § MIA SALA): con SOLO LA VISTA acceso, da un'altra vista porta in METEO **con il radar acceso** (non lo inverte: partendo dal default acceso lo avrebbe spento proprio mentre apriva la vista, rilievo di revisione del 23/09/2026); dentro METEO, o a composizione libera, lo accende e lo spegne.
- 🔴 **In modalità mondo (EMERGENZE) i sismi INGV stanno già nel layer mondo**: `applyLayers()` non riaggiunge `qkLayer` finché `worldLayer` è sulla cartina (prima un clic sul livello li raddoppiava).
- Le frecce del menu contano **tutte** le voci fuori dal riquadro (tab e interruttore), non solo i tab.
- 🔴 **EMERGENZE ha DUE scale** (`#emsScala` nella striscia, `S.emsScala` persistito, `emsScalaSet()`): **AREA 400 KM** (default: Genzano a zoom 6 con le tessere OSM, dove aerei, fuochi e pronto soccorso si leggono) e **MONDO** (planisfero a zoom 2 senza tessere, confini Natural Earth, per GDACS ed EMS nel mondo). Rilievo di revisione del 23/09/2026: a zoom mondo i mezzi aerei entro 400 km erano un grumo illeggibile, e la vista riportava al planisfero a ogni ingresso. I marcatori del mondo restano in entrambe le scale; `worldMode()` passa da `emsScalaVista()`/`emsScalaSfondo()`, mai da coordinate scritte a mano. 🔴 `ensureWorldGeo()` aggiunge i confini solo se la scala è **ancora** MONDO quando il file arriva: chi passa ad AREA mentre il caricamento è in corso non deve ritrovarsi i continenti sopra le tessere (gara riprodotta nel test trattenendo la richiesta).
- **Etichette e legenda stanno in una colonna** (`#mapInfo`, in basso a sinistra): coordinate, fulmini, radar e legenda si spingono a vicenda invece di sovrapporsi quando la legenda cresce. L'etichetta galleggiante del mondo (`#worldLbl`) non esiste più: si sovrapponeva al riquadro delle fonti, e le sue voci (GDACS per livello, EMS, sismi per magnitudo, vulcani) stanno in `LEGENDA.mondo`, che `legendUpd()` elenca quando la cartina è in modalità mondo. I 22 px in fondo restano all'attribuzione OpenStreetMap.
- **Il pannello chiuso è anche invisibile** (`visibility:hidden` con transizione ritardata, su `body.side-closed #side` e sul pannello mobile): un pannello solo traslato fuori schermo restava nell'ordine di Tab (WCAG 2.4.3). `pannelloApri(on)` tiene allineato `aria-expanded` su `#sideTgl` e, chiudendo, **riporta il fuoco al pulsante PANNELLO** se stava dentro il pannello (un elemento a fuoco che diventa invisibile lo perde in silenzio, rilievo di revisione); su telefono una pastiglia, la scala o OGGI/DOMANI **chiudono il pannello** dopo il comando (`pannelloMobileChiudi()`), perché il pannello copre la cartina e l'effetto va visto subito — i due menu ICON-2I no, sono in fila.
- **Striscia accessibile**: ogni gruppo `.smGrp` è `role="group"` con `aria-labelledby` sulla propria etichetta SULLA CARTINA, i glifi `.ic` sono `aria-hidden`, le pastiglie spente e i menu ICON-2I hanno bordo `--dim` (un bordo a 1,1:1 è invisibile, § MIA SALA), OGGI/DOMANI e AREA/MONDO condividono la classe `.segm`; tutti i bersagli sono ≥ 24 px, compresi i marcatori degli aerei (`.acHit` 24 × 24 attorno al glifo da 15 px: su un telefono un aereo da 16 px non si prendeva).
- **Satelliti: dopo un guasto di CelesTrak non si ritenta a ogni cambio vista** (`S.orb.ultimoTentativo`, 5 minuti): `applyLayers()` gira a ogni `setView()`, e ogni tentativo automatico sono 11 richieste; la riprova esplicita resta ai pulsanti della scheda. Sempre in `applyLayers()`: `applyPrev()` chiama `setParams` (che ridisegna tutte le tessere) solo se campo o orizzonte ICON-2I sono cambiati, e `radarStamp()` si rilegge solo quando il radar si accende.

**Verificato con Playwright** (Chromium, 1280 e 375, effemeridi CelesTrak e tessere OSM riprodotte in locale): 93 controlli sui cambi di vista, composizione libera, scala AREA/MONDO, persistenza al ricarico, ritorno dal mondo, tastiera, pannello mobile, muro, guasto di CelesTrak; axe senza rilievi. ⚠️ I **marcatori geografici** (aerei, stella di Genzano) possono stare a meno di 24 px l'uno dall'altro quando due mezzi sono vicini nel cielo: è l'eccezione «essenziale» di WCAG 2.5.8 (la posizione è l'informazione) e il test li dichiara a parte invece di contarli, perché dipendono dallo snapshot del momento. Un livello nuovo nasce con la sua vista in `VISTA_DI`, la pastiglia nel gruppo giusto di `#sideMap`, la voce in `LEGENDA` e in `LEG_ORDINE`, la riga `on(...)` in `applyLayers()` e il default in `S.layers`: senza uno dei sei, o non si accende, o non si spiega.

## Sala situazioni `/monitor/` — fonti dati aggiunte il 22/09/2026

Sei fonti nuove, divise per come si raggiungono. **La discriminante è il CORS**: si verifica sempre prima di scrivere codice, con `curl -sI -H "Origin: https://www.protezionecivilegenzano.it" <url> | grep -i access-control`.

**Lette direttamente dal browser (CORS aperto, nessuna chiave):**

| Fonte | Vista | Note |
|---|---|---|
| **Mareografi IOC/UNESCO** (`www.ioc-sealevelmonitoring.org`) | ARIA·MARE | Anzio `AZ42`, Civitavecchia `CI20`, Gaeta `GA37`. Campionamento continuo, ritardo di pochi minuti. 🔴 `slevel` è lo **scostamento dallo zero della stazione**, non una quota assoluta: si mostra in cm con la **variazione nell'ora**, che è il dato operativo (storm surge, acqua alta, ritiro anomalo). Oltre 45 minuti di età il valore non si mostra più come attuale. |
| **EMSC** (`www.seismicportal.eu`) | SISMICO | M3.5+ euro-mediterranei, **Italia esclusa di proposito**: lì fa fede INGV e mostrare lo stesso sisma con due magnitudo diverse confonderebbe. Copre la fascia M3.5–4.5 che il feed mondiale USGS non porta. |
| **Open-Meteo** (host già in CSP) | METEO | Scheda «Indici di rischio»: UV, **umidità del suolo** (precursore di inneschi e risposta alle piogge), neve al suolo, umidità dell'aria. |

**Lette da snapshot committato** (`aggiorna-dati-sala.yml`, ogni 15 min), perché la fonte non espone il CORS:

| Fonte | Script | Vista | Note |
|---|---|---|---|
| **adsb.fi** | `genera-volo-soccorso.py` | EMERGENZE | **Tutti** i velivoli entro 400 km da Genzano (`RAGGIO_AREA`, una costante da alzare per allargare) più antincendio ed emergenze su tutta l'Italia. Filtri nell'elenco: tutti / antincendio / elicotteri / emergenze / bassa quota. |
| **MeteoAlarm** (EUMETNET) | `genera-meteoalarm.py` | ALLERTA | Quadro delle altre regioni. 🔴 **Non sostituisce mai il bollettino DPC**: per Genzano fa fede la Zona F, e la scheda lo dice nell'intestazione. |
| **NASA FIRMS** | `genera-incendi-firms.py` | EMERGENZE | Punti caldi da satellite. **Richiede il segreto `FIRMS_MAP_KEY`**: senza, lo script non scrive nulla e la scheda non compare — mai dati di riempimento. |

**Meteo spaziale e radiosonde nella vista RADIO (22/09/2026)** — due schede lette **direttamente dal browser**, CORS aperto e nessuna chiave: **NOAA SWPC** (`services.swpc.noaa.gov`, indice Kp e brillamenti solari) e **SondeHub** (`api.v2.sondehub.org`, palloni meteo in volo con quota e distanza da Genzano). Stanno lì perché non sono curiosità: il Kp misura il disturbo geomagnetico e i brillamenti di classe M o X producono blackout radio in HF, cioè dicono quanto saranno affidabili i collegamenti a lunga distanza in emergenza; le radiosonde dicono che cosa sta volando sopra di noi e su quale frequenza. 🔴 **Non si scrive che si ricevono «con il ricevitore di questa pagina»**: trasmettono nel segmento 400,15–406 MHz degli ausili meteorologici, e i profili dei due SDR incorporati partono da ~430 MHz (`radioProf` accetta solo `|f − centro| ≤ banda/2`), quindi non li coprono — verificato per calcolo il 22/09/2026, dopo che la prima stesura affermava il contrario. La frequenza mostrata è quella **trasmessa dal pallone** (campo `frequency` della fonte), mai una stima nostra.

🔴 **Le letture dirette invecchiano come gli snapshot.** Se una di queste fonti risponde una volta e poi smette, il `catch` lascia i dati in memoria e la scheda continuerebbe a mostrarli come attuali: la guardia è `direttoVecchio(S.last.<chiave>)` con soglia `DIRETTO_MAX_AGE` (45 min), gemella di `snapVecchio`/`SNAP_MAX_AGE` per gli snapshot, che aggiunge «NON AGGIORNATO» al titolo e la riga `.staleNota` con l'ora dell'ultima lettura riuscita. Per le radiosonde vale in più `SONDA_MAX_AGE` (30 min sul singolo frame): la finestra chiesta alla fonte è di tre ore e conterrebbe anche palloni che non trasmettono più. Per lo stesso motivo il titolo dice «ultima telemetria» e non «in volo»: dalla telemetria si sa dove stava il pallone e quando, non se stia ancora salendo. Entrambi gli host vanno in `connect-src`.

**Filtri dei mezzi aerei (22/09/2026)** — due file di pastiglie: la prima per **situazione** (tutti, antincendio, emergenze, bassa quota), la seconda per **categoria**, ricavata dinamicamente dallo snapshot con `voloCategorie()` invece di essere elencata a priori. Le categorie sono la *emitter category* ADS-B trasmessa dal velivolo, quindi compaiono tutte e solo quelle realmente presenti; il filtro per categoria usa il prefisso `cat:`. 🔴 **«TUTTI» resta sempre la prima pastiglia**: qualunque filtro si applichi, si deve poter tornare all'intero traffico con un clic.

**Vista TRAFFICO (22/09/2026)** — mappa live incorporata da `embed.waze.com/it/iframe`, con lo stesso **click-to-load** di Windy: il server di terzi è contattato solo su richiesta esplicita, mai al caricamento della pagina. Quattro livelli di zoom (Genzano, Castelli, Lazio, Centro Italia). Nessuna chiave, nessuna ingestione di dati, nessun reverse engineering: è l'endpoint di incorporamento che Waze pubblica apposta. 🔴 **Le segnalazioni vengono dagli utenti e non sono ufficiali**: la nota lo dice e ricorda che le chiusure che fanno fede sono di Polizia Locale, Comune e Anas, e che il Gruppo non regola il traffico (Circolare DPC 6 agosto 2018). Richiede `embed.waze.com` in `frame-src` della CSP.

**Traffico — perché non si ingeriscono i dati.** Provate il 22/09/2026: CCISS (MIT) non espone un feed raggiungibile, Anas non ha API pubblica, `api.luceverde.it` esiste ma non è documentata — reverse-engineerizzare l'API privata di un terzo su un sito istituzionale non è una strada accettabile, né per la licenza né per la tenuta nel tempo. TomTom e HERE richiedono chiave e vincolano la resa alla loro cartografia. Waze for Cities darebbe un feed vero di code e segnalazioni, ma presuppone un accordo del **Comune**: è la strada da percorrere se un giorno servisse il dato grezzo invece della mappa.

**Livelli di cartina** (dal 23/09/2026 nella striscia SULLA CARTINA del pannello della vista, non più nella barra): **MEZZI AEREI** (EMERGENZE) disegna i velivoli del filtro attivo (freccia orientata sulla rotta trasmessa per gli aerei, simbolo diverso per gli elicotteri, che una prua non la mostrano) e **MAREOGRAFI** (ARIA·MARE) le tre stazioni mareografiche. Elenco e cartina mostrano **sempre la stessa selezione**: il clic su una pastiglia di filtro rigenera entrambi.

🔴 **Peso sul repository:** `volo-soccorso.json` è riscritto e committato **ogni 15 minuti** e cambia sempre, perché cambiano le posizioni. Per questo si scrive compatto (`separators=(",",":")`) e il perimetro è l'area, non l'Italia intera: a 400 km sono ~55 KB per commit, con l'Italia intera sarebbero oltre 110 KB, cioè alcuni GB l'anno di crescita per un dato che a una sala di Genzano non serve.

🔴 **Frecce del menu dei pannelli:** non bastava una chevron sul bordo, perché non comunica che il menu continua. Ora `navArrUpd()` conta i pulsanti della barra (tab e interruttore SOLO LA VISTA) davvero fuori dal riquadro e lo scrive nella freccia (**«‹ 3»**, **«› 4»**), aggiornando anche l'`aria-label`. Al primo accesso la freccia destra lampeggia tre volte (`.hint`), una sola volta per dispositivo (`localStorage` `pcgz-monitor-nav-visto`), e il richiamo rispetta `prefers-reduced-motion` e il fermo-animazioni della barra accessibilità.

🔴 **Tre regole imparate costruendole, da non ripetere:**

1. **Un filtro per tipo di velivolo va guardato prima di fidarsene.** La prima esecuzione ha etichettato «antincendio» un `AT-802` a 400 ft sopra la Slovenia: era un aereo **agricolo** in irrorazione. Ora la lista `MODELLI_AIB` contiene solo airframe a impiego esclusivamente antincendio (Canadair, AT-802**F**/Fire Boss, S-64, BE-200) e c'è un riquadro geografico sull'Italia, perché i cerchi di raccolta sbordano su Slovenia, Croazia, Corsica e Tunisia.
2. **Un avviso scaduto non è un avviso.** Il feed MeteoAlarm continua a esporre gli avvisi per un po' dopo la fine della validità. Si filtrano **due volte**: nello script e di nuovo nel browser, perché fra uno snapshot e l'altro passano 15 minuti. Stessa logica della barra allerta in homepage (rule 09 § 15).
3. **Un punto caldo non è un incendio.** FIRMS rileva anomalie termiche: possono essere fiaccole industriali, bruciature agricole o falsi positivi. Il campo `confidence` della fonte si riporta tale e quale invece di tradurlo in una certezza che non ha.
4. **Un riquadro di coordinate non è un paese.** Il `AREA` chiesto a FIRMS (6,4–18,8 E / 35,2–47,2 N) contiene Corsica, Slovenia, Croazia, Bosnia, Montenegro e la punta della Tunisia: col **primo dato reale**, il 22/09/2026, **28 punti su 99 erano fuori dai confini italiani**, mentre il titolo della scheda diceva «— ITALIA». Stesso inciampo già visto sul riquadro dei mezzi aerei. La scheda ora dice «Italia e paesi vicini», lo ripete in nota, e affianca al totale il numero che serve a una sala di Genzano: **la distanza del punto più vicino**. Quella distanza resta di colore neutro — da sola non dice gravità (il più vicino può essere un'anomalia da 2 MW), il segnale di allarme sta sulla potenza radiativa.
5. **Una scheda si giudica solo quando si accende.** La scheda dei punti caldi è rimasta spenta dalla sua scrittura fino all'arrivo della chiave: entrambi i difetti sopra sono emersi nel minuto in cui ha mostrato dati veri. Quando una scheda dipende da un segreto o da una fonte non ancora attiva, **si rilegge da capo al primo dato reale**, non si dà per verificata perché il codice sembrava giusto.

## Sala situazioni `/monitor/` — vista SATELLITI (orbite calcolate in pagina, 22/09/2026)

Richiesta dell'utente: *«voglio sapere tutti i satelliti, con filtro per quelli ambito protezione civile e tutti i filtri possibili»*. Vista `data-v="orb"` (slug `satelliti`) + layer di cartina `data-l="orb"` (pastiglia ORBITE nella striscia SULLA CARTINA del pannello, dal 23/09/2026; 🔴 **non** `sat`, già usato dalle immagini satellitari EUMETSAT).

**Le posizioni si CALCOLANO, non si riprendono.** Le effemeridi (TLE) vengono da **CelesTrak** (CORS aperto, verificato), e la posizione è propagata nella pagina con **SGP4** — `static/vendor/satellite/satellite.min.js`, satellite.js 6.0.0 UMD, MIT, 24 KB, vendorizzata come Leaflet perché la CSP non ammette script di terzi. Nessun servizio esterno sa che cosa si sta guardando. Verificato il 22/09/2026 contro una fonte indipendente sulla ISS: **0,4 km di scarto in orizzontale, 0,0 in quota** su un oggetto a 27.600 km/h; e per costellazione — Meteosat 35.78x km (quota geostazionaria esatta), GPS 20.200, Galileo 23.220, GLONASS 19.190, BeiDou 21.500, ISS 425.

🔴 **La 6.0.0 e non la 7.x**: la 7 è a moduli ES con una parte WebAssembly e richiederebbe un passaggio di compilazione che il sito non ha. Dettagli e procedura di aggiornamento in `static/vendor/satellite/README.md`.

**I gruppi sono della fonte, non nostri.** Il filtro «protezione civile» è l'**unione di gruppi CelesTrak**, non un'etichetta inventata: `sarsat` (83 oggetti — GPS, Galileo, GOES e Meteosat che **portano il ripetitore COSPAS-SARSAT** per i radiofari di emergenza a 406 MHz), `dmc` (9 — Disaster Monitoring Constellation), `weather` (71), `goes` (6), `resource` (167 — da queste immagini nascono le mappe Copernicus EMS già in pagina), `stations` (20), `amateur` (95). Aggiungere un gruppo = una riga in `ORB_GRUPPI` con la sua descrizione; le pastiglie compaiono **solo per i gruppi realmente caricati** (`orbGruppiPresenti()`), come per le categorie degli aerei.

**Filtri**, tre file di pastiglie: insieme (🔴 **TUTTI sempre per primo e sempre disponibile** · protezione civile · sopra l'orizzonte · visibili a occhio nudo), gruppo della fonte, fascia di orbita (bassa/media/geostazionaria/alta, soglie LEO/MEO/GEO).

**«Visibili a occhio nudo» è calcolato, non supposto**: satellite illuminato dal Sole (prova del cilindro d'ombra su `sunPos`), osservatore sotto il crepuscolo civile (Sole a meno di −6°) **e appartenenza al gruppo `visual` della fonte**. 🔴 Le prime due condizioni da sole **non** bastano: dicono che il satellite *potrebbe* riflettere luce verso di noi, non che sia abbastanza luminoso — un cubesat o un satellite di navigazione le soddisfa restando invisibile a occhio nudo (47 oggetti contati invece di 2, rilievo di revisione del 22/09/2026). La magnitudine apparente calcolata sarebbe più precisa, ma richiede sezione trasversale e albedo per oggetto, dati che CelesTrak non pubblica: stimarli significherebbe presentare come misura un numero inventato. 🔴 `sunPos` vuole una **data giuliana** (`satellite.jday`), non un `Date`: passandogli un `Date` restituisce valori senza senso (declinazione 71°) e la prova dell'ombra dà zero illuminati a ogni ora. Verificato: declinazione 0,00° all'equinozio, e il modello riproduce da solo che i satelliti si vedano **solo intorno all'alba e al tramonto** (di giorno tutti illuminati, a notte piena nessuno).

🔴 **Il peso decide il comportamento.** Il catalogo `active` è di **~16.000 oggetti e 2,7 MB**: non si scarica all'apertura. All'ingresso si caricano i gruppi selezionati (~620 oggetti, ~90 KB) e il catalogo intero arriva solo su richiesta esplicita, **click-to-load** come Windy, Waze e il ricevitore radio. Le TLE stanno in `localStorage` per 6 ore (`pcgz-tle:<gruppo>`): CelesTrak **chiede espressamente** di non riscaricare le stesse effemeridi a ogni visita. Il calcolo non è il collo di bottiglia: 16.118 oggetti propagati in **59 ms nel browser**.

🔴 **Tre cose che si imparano solo guardando il risultato:**
1. **L'età delle effemeridi si misura sulla mediana, non sul caso peggiore.** Con il minimo bastavano **2 TLE su 717** (lo 0,3%) a far comparire l'avviso per tutte: rumore che si impara a ignorare. Ora si mostra la mediana come dato (0,6 giorni nel campione) e si avvisa solo se oltre il 5% supera la settimana. Alcune epoche sono **nel futuro** — la fonte pubblica anche elementi previsti — quindi l'età si prende in valore assoluto.
2. **Il punto sulla cartina è la verticale a terra, non il posto da cui si vede.** Un satellite a ventimila chilometri è sopra l'orizzonte di Genzano anche col punto sul Sahara: la nota lo dice, altrimenti la mappa si legge al contrario.
3. **Con «tutti» la cartina disegna solo il selezionato sopra l'orizzonte**, al massimo 400 punti (`ORB_MAX_MAPPA`): 16.000 pallini non sono una mappa. L'elenco mostra i 25 più alti e dichiara quanti sono in tutto.

**Filtri geografici e passaggi (22/09/2026, seconda richiesta dell'utente).** Due filtri per area (`a:it`, `a:eu` — riquadri di coordinate, quindi contengono anche i vicini, e la scheda lo dice). 🔴 **Coi filtri per area NON si scarta chi sta sotto l'orizzonte**: la domanda è «chi passa sull'area», non «chi vedo da Genzano» — un satellite sopra la Norvegia è sopra l'Europa anche se da qui non si alza. 🔴 **Sopra il riquadro italiano c'è spesso UN satellite solo**: sotto `MIN_AREA` (8) la scheda aggiunge una sezione **dichiarata** «fuori dal riquadro, i più vicini», mai mescolata di nascosto alla prima.

**Passaggi al tocco.** Ogni riga è un pulsante (`role="button"`, `tabindex=0`, Invio/Spazio): apre una scheda con i **prossimi passaggi sopra Genzano** (inizio, altezza massima, direzione in parole, durata) e **quando sorvola il riquadro italiano**. Calcolo in `orbPassaggi()`: passi di 30 s per 48 ore, ~5.800 propagazioni, **20 ms** per satellite — si fa al volo, niente da precalcolare. 🔴 Un **geostazionario non «passa»**: sta fermo rispetto a terra, ed è sopra l'orizzonte sempre o mai. Va detto a parole, non lasciato come elenco vuoto. ⚠️ Verifica di un dubbio: un GPS fa **3 intervalli in 48 ore**, non 8 — la traccia a terra si ripete ogni **giorno siderale** e delle due orbite quotidiane una passa dall'altra parte del pianeta. Confermato con un calcolo indipendente prima di toccare il codice.

🔴 **Tre difetti che la revisione ha trovato dopo la pubblicazione (22/09/2026)**, tutti nati dallo stesso errore di fondo: aver verificato che il *primo* calcolo fosse giusto senza verificare che continuasse a esserlo.

1. **Le posizioni non si ricalcolavano.** `orbCalcola()` era richiamato solo dal caricamento e come ripiego `S.orb.calc||orbCalcola()`: né `refreshAll()` né alcun temporizzatore lo rifaceva, quindi a monitor aperto la scheda diceva «adesso» mostrando l'istante di apertura. In orbita bassa sono **7,8 km al secondo**: dopo dieci minuti il dato è sbagliato di migliaia di chilometri. Ora c'è `ORB_TICK` (15 s) con quattro guardie, tutte necessarie: **scheda nascosta** (`document.hidden`) → fermo; **vista chiusa e livello spento** → fermo, perché nessuno sta guardando; **fuoco da tastiera dentro il pannello** → si calcola ma non si ridisegna, altrimenti a chi naviga con Tab il fuoco sparisce di sotto alle dita; la **cartina** si ridisegna sempre. Un riquadro dichiara l'ora dell'ultimo calcolo: un dato che si rinfresca da solo va **datato**, non presentato come perpetuo.
2. **Un gruppo caduto spariva in silenzio.** L'errore era mostrato solo se `S.orb.recs` era vuoto, quindi con dati già in memoria il guasto non compariva e i conteggi restavano incompleti senza modo di accorgersene né di riprovare. Ora `S.orb.falliti` tiene i gruppi caduti, la `.staleNota` li dichiara **col nome che il lettore vede sulle pastiglie** (`orbEtichetta`: «SOCCORSO», non `sarsat`) e un pulsante riprova **solo quelli**. 🔴 La riprova deve ricordare che cosa è stato **chiesto** (`S.orb.chiesto`), non che cosa è riuscito: `tutti` resta falso proprio quando è `active` a non arrivare.
3. **«Catalogo completo» si dichiarava per il solo fatto di averlo chiesto**, etichettando dati parziali come completi e facendo sparire il pulsante per ritentare. 🔴 E la **prima correzione sbagliava ancora**: contava le effemeridi *aggiunte*, così una riprova che ritrovava ciò che era già in memoria risultava fallita. Si contano quelle **presenti nello scarico** (`orbConta`, indipendente dalla deduplicazione) con la soglia `ORB_MIN_CATALOGO`, che distingue il catalogo vero da una risposta troncata. Lezione generale: il successo di uno scarico si misura su **ciò che è arrivato**, mai sulla differenza rispetto a ciò che si aveva.

⚠️ **Il banco di prova sono le effemeridi vere riprodotte in locale** (`pg.route` su `celestrak.org` con i file dei gruppi, catalogo `active` compreso), non un campione sintetico: la quarta prova — riprova del catalogo dopo un guasto — è proprio quella che ha svelato l'errore del punto 3, e con un campione finto di 489 oggetti dava un falso allarme. Prove da rifare toccando questa vista: movimento reale fra due tick, guardie di stop (nascosta/vista/livello/fuoco), quattro scenari di guasto, axe su tutte le viste a 1280 e 375.

## Sala situazioni `/monitor/` — il bollettino DPC non si chiede più all'API di GitHub (22/09/2026)

🔴 Nel repository ufficiale `pcm-dpc/DPC-Bollettini-Criticita-Idrogeologica-Idraulica` i bollettini si chiamano **col minuto reale di pubblicazione** (`files/20260922_1421.json`): non esiste nessun file con nome stabile da chiamare — l'unico è `files/all/latest_all.zip`, un archivio che il browser non può aprire. Per sapere qual è l'ultimo bisogna leggere l'elenco dei commit dall'**API di GitHub**, che senza credenziali dà **60 richieste l'ora per indirizzo IP**, condivise da tutti quelli che escono dalla stessa rete; `findStamp()` ne consumava fino a **nove per caricamento** (1 per l'elenco + 1 per ogni commit ispezionato). In sede, con più postazioni sullo stesso IP, la scheda si spegne e la cartina delle zone resta senza colori.

🔴 **Il timbro si ricava dal mirror opendatasicilia, non dall'API.** È la stessa fonte che il sito usa già per la barra di allerta (`scripts/check-allerta.py`): quel repository ripubblica i bollettini DPC in CSV con **nomi di file fissi** — `data/bollettini/bollettino-oggi-zone-latest.csv`, 63 KB — e dentro c'è `data_pubblicazione`, che corrisponde **esattamente** al timbro del file ufficiale (`2026-09-22T14:21:59` ↔ `20260922_1421`). ⚠️ Verificato su **sei giorni consecutivi** (17→22 settembre 2026) prima di fidarsene: sei timbri su sei coincidono e sei file ufficiali rispondono 200. Non è una coincidenza da dare per scontata — è l'unica ragione per cui questa strada è lecita, e se un giorno il mirror cambiasse schema il controllo se ne accorge.

Dal 22/09/2026 quindi: **`scripts/genera-dpc-bollettino.py`** (step di `aggiorna-dati-sala.yml`, ogni 15 minuti) ricava il timbro dal mirror, **verifica sulla fonte ufficiale che la terna sia completa** e scrive `static/open-data/dpc-bollettino.json` con `stamp` e `name`; `findStamp()` legge quello con **una richiesta sola e senza quota**. Le due carte topojson restano su `raw.githubusercontent.com` del **repository ufficiale**: il mirror serve solo a sapere QUALE bollettino è quello corrente, il contenuto resta del Dipartimento (rule 06, gerarchia delle fonti). L'API di GitHub resta come **ripiego di secondo livello**, se il mirror non risponde.

- 🔴 **Lo snapshot va anche nel `git add` del workflow**, non solo nel passo che lo genera. Il 23/09/2026, al primo controllo del giorno dopo, `dpc-bollettino.json` risultava **assente dalla riga `git add`** di `aggiorna-dati-sala.yml`: lo script lo riscriveva e il `checkout` del run successivo buttava via la modifica, quindi il timbro sarebbe rimasto congelato al 22/09 **per sempre** e la Sala avrebbe mostrato il bollettino di ieri come quello di oggi (proprio il dato vecchio spacciato per attuale che la rule 06 vieta). Il difetto era invisibile finché il bollettino non cambiava: il log diceva «invariato» ed era vero. ⚠️ **Aggiungendo uno snapshot nuovo si toccano DUE punti** — il passo che lo genera e la riga che lo committa — e la prova è banale: si cambia un valore a mano, si esegue la stessa `git add` del workflow e si guarda `git diff --cached --name-only`.
- 🔴 **Il vantaggio non è solo la quota**: non dipendendo dall'API, lo script si può provare *davvero* in qualunque ambiente — la versione precedente non era collaudabile dove `api.github.com` è filtrato, e questa è stata verificata end-to-end compresi i due percorsi di guasto (mirror giù → ripiego; CSV con schema cambiato → si dichiara e non si scrive).
- Il controllo periodico (`chk_dpc_bollettino` in `check-fonti-cruscotto.py`) verifica **sia** che il bollettino indicato esista ancora sulla fonte ufficiale **sia** che il mirror del timbro risponda: se il mirror muore si resta sul ripiego con la quota per IP, e va saputo prima.

- 🔴 **Fail-safe come gli altri snapshot**: fonte muta → file lasciato com'era, exit 0. E una risposta che si legge ma non contiene nessun timbro riconoscibile **non è un dato**: significa schema cambiato, quindi si lascia il file e si dichiara l'anomalia invece di scrivere uno snapshot nullo (stessa lezione di adsb.lol, § "MEZZI AEREI").
- Lo script verifica che esista la **terna completa** (`<stamp>.json` + `topojson/<stamp>_today.json` + `_tomorrow.json`): senza le due carte la cartina resterebbe vuota.
- `--stamp AAAAMMGG_HHMM` serve per il primo innesco e per un ripristino a mano; il timbro si **legge sulla fonte**, non si inventa.
- Fonte sorvegliata da `check-fonti-cruscotto.py` (`chk_dpc_bollettino`): controlla che il bollettino indicato dallo snapshot esista ancora sulla fonte — se non esiste, lo snapshot è fermo o il DPC ha cambiato schema.

⚠️ **Una fonte mai interrogata non è una fonte che non risponde.** Nella scheda STATO FONTI la riga STAZIONI diceva «N/D — NESSUNA RISPOSTA» anche quando nessuno aveva ancora aperto la vista METEO (è lì che `loadObs()` parte): mostrava come guasto qualcosa che nessuno aveva chiesto. Ora quel caso si distingue — **«IN ATTESA — NON ANCORA RICHIESTA»**, in `--dim` e non in giallo. Una riga nuova che si carica pigramente eredita il comportamento da sola.

## Sala situazioni `/monitor/` — MIA SALA: schede scelte e ordinate (22/09/2026)

Richiesta dell'utente: poter **personalizzare la posizione delle schede** e **vederne più di una insieme**. Vista `data-v="mia"` (slug `mia-sala`), prima nella barra.

🔴 **La barra è ordinata per TIPOLOGIA, e i tasti 1-9 seguono la barra (22/09/2026).** Richiesta dell'utente: *«voglio che metti in ordine per tipologia i tab… tranne ovviamente la prima scheda personalizzata»*. Ordine: **MIA SALA** (sempre prima, fuori dalle famiglie) │ *previsione e condizioni* **ALLERTA · METEO · ARIA·MARE** │ *eventi in corso* **SISMICO · EMERGENZE · TRAFFICO** │ *osservazione* **CARTE · WINDY · SATELLITI · NAVI** │ *sala* **RADIO · REGISTRO** │ interruttori **⌨ TASTI RAPIDI** e **⧉ SOLO LA VISTA** (dal 23/09/2026 i livelli di cartina non stanno più nella barra ma nella striscia del pannello, § «la cartina è della vista»). Le famiglie seguono il ciclo del rischio della rule 06 (che cosa è previsto → che cosa sta succedendo → con che cosa lo guardo → che cosa fa la sala) e sono separate da `<span class="sep">`; **l'alfabetico è stato scartato**: in emergenza non si cerca una voce per iniziale, si cerca la famiglia, e metterebbe ALLERTA accanto ad ARIA·MARE e CARTE accanto a EMERGENZE.

- 🔴 **Il separatore prima dell'interruttore SOLO LA VISTA ha una classe sua** (`sep sepLay`): in modalità muro si nasconde **solo quello**, insieme all'interruttore, non i separatori fra le famiglie di viste.
- 🔴 **I tasti 1-9 leggono il DOM** (`document.querySelectorAll("#nav button[data-v]")[n-1]`), quindi **il tasto N apre l'N-esimo tab**, MIA SALA compresa. Fino al 22/09/2026 erano una lista scritta a parte (`const order=[...]`) che **non coincideva** con l'ordine visibile: imparabile solo a memoria e destinata a divergere a ogni riordino. Ora non possono più separarsi. Restano 1-9 perché la condizione è `e.key>="1"&&e.key<="9"`: SATELLITI, NAVI, RADIO e REGISTRO si aprono col clic. ⚠️ Chi riordina la barra **sposta anche le scorciatoie**, ed è voluto — ma chi usa la sala in sede ha la memoria delle dita: un riordino si concorda, non si fa di passaggio. 🔴 **Le scorciatoie a tasto singolo si possono spegnere** (dal 23/09/2026, richiesta dell'utente): l'interruttore **⌨ TASTI RAPIDI** nella barra (`#tastiBtn`, `aria-pressed`, `S.tasti` persistito in `pcgz-monitor-cfg`, `tastiSet()`) disattiva 1-9 e R con una sola guardia in testa al gestore `keydown`. È il meccanismo che WCAG 2.2 chiede al criterio **2.1.4 «Character Key Shortcuts»**: chi detta col riconoscimento vocale o usa un ausilio che manda tasti per sbaglio si ritroverebbe la vista cambiata senza volerlo. Le frecce della sintonia radio non sono caratteri stampabili e restano fuori dal criterio. Il suggerimento «(tasto R)» sulla pastiglia del radar compare solo con le scorciatoie accese. Il pulsante resta visibile anche in modalità muro (i tasti 1-9 lì funzionano), quindi sta **prima** del separatore `sepLay`, che si nasconde col solo SOLO LA VISTA.
- La rotazione video-wall (`▶ CICLO`) segue le stesse famiglie, saltando le viste di lavoro (WINDY, RADIO, REGISTRO, e i riquadri di terzi). 🔴 **Dal 23/09/2026 qualunque scelta manuale di vista spegne il ciclo** (`setView(v,fromHash,daCiclo)`: solo il temporizzatore passa `daCiclo=true`; clic sui tab, tasti 1-9 e indirizzo lo fermano, e `cicloSet(false)` riporta il pulsante a «▶ CICLO»). Prima il ciclo continuava anche dopo che l'operatore aveva aperto RADIO o NAVI, e dopo 45 secondi la Sala saltava ad ALLERTA da sola: le segnalazioni erano «la radio si stacca senza aver toccato nulla», «il tab navi si disconnette», «alcuni tab mi fanno uscire fuori». Nel secondo screenshot dell'utente il pulsante diceva «⏸ CICLO ON». Un automatismo che toglie il comando a chi lo ha appena preso è un difetto, non una funzione: chi sceglie una vista ha la vista finché non ne sceglie un'altra.

🔴 **Pulsanti, non trascinamento.** WCAG 2.2 criterio **2.5.7 «Dragging Movements»** impone un'alternativa a singolo puntamento per ogni azione fatta trascinando, e questo repository ha il gate `pa11y-ci` **bloccante**. Col trascinamento i pulsanti andrebbero scritti comunque: si parte da quelli (**☆ MIA SALA** per scegliere, ▲ ▼ per ordinare, ✕ per togliere), che funzionano da tastiera e col dito. Il trascinamento resta un'aggiunta possibile, mai un sostituto.

🔴 **Un glifo nudo non è un comando (22/09/2026).** Il pulsante per aggiungere era una **☆ sola**, 13 px, colore `--dim`, appoggiata nell'intestazione della scheda: misurata **15,7 × 28 px**, sotto i 24 px minimi del criterio **WCAG 2.2 AA 2.5.8 «Target Size»**, e visivamente indistinguibile da una decorazione. L'utente che aveva chiesto la Mia Sala non l'ha riconosciuta e ha domandato se le schede si trascinassero dentro: quando chi ha commissionato una funzione non trova il comando, il problema è il comando. Ora è una pastiglia **☆ MIA SALA** con la parola scritta, bordo `--dim` visibile (5,23:1, sopra i 3:1 di WCAG 1.4.11), **77 × 42 px**; `aria-pressed` e `aria-label` cambiano fra «Aggiungi» e «Togli». Il glifo è `aria-hidden`, così chi usa lo screen reader non si sente leggere «stella bianca».

🔴 **I tab dicono quali viste sono nella Mia Sala (22/09/2026).** Richiesta di chi la usa: *«fai in modo che anche chi lo vede dai tab abbia una colorazione leggermente diversa… così di primo impatto vedo quali tab ho inserito anche stando dentro un tab non selezionato»*. `miaTab()`, richiamata a ogni `render()`, marca i pulsanti `[data-v]` delle viste da cui hai preso almeno una scheda: **filetto giallo in alto** (`inset 0 2px 0 var(--gia)`) e testo più caldo. 🔴 Le due informazioni non si confondono perché usano **bordi diversi**: riga **ciano in basso** = vista aperta (`.act`, già esistente), riga **gialla in alto** = vista presente nella Mia Sala; su un tab che è entrambe le cose si vedono insieme. 🔴 **Il colore non basta** (WCAG 1.4.1): accanto al nome compare una **★** in un `<span aria-hidden>` e il `title` del pulsante dice quante schede sono («2 schede nella Mia Sala»), conservando il titolo originale in `data-tit`. Il tab MIA SALA non si marca da sé.

🔴 **La Mia Sala va a MURO, non in colonna (22/09/2026).** *«I ragazzi vogliono che in contemporanea vedono le varie schede su un'unica pagina: è questo il senso della mia sala»*. Nel pannello laterale da 380 px le schede si scorrono **una per volta**, che è l'opposto. Da **900 px** in su `render()` mette `body.muro`: il pannello prende tutta la larghezza (`#side{left:0;width:auto}`) e `#feed` passa a `columns:340px`. Sotto i 900 px resta la colonna — su un telefono «insieme» non esiste.

- 🔴 **Colonne (`columns`), non griglia.** Con `grid` l'altezza di ogni riga è quella della scheda più alta: sotto una scheda corta resta un buco grande quanto la differenza (su 1920 px erano centinaia di pixel vuoti, verificato). Le colonne impaginano come un giornale e riempiono davvero; `break-inside:avoid` tiene intera ogni scheda. L'ordine diventa **per colonna**: prima scheda in alto a sinistra, ultima in basso a destra, e le frecce ▲ ▼ si muovono in quella sequenza.
- ⚠️ **Le colonne si riempiono in base a quante schede ci sono.** Il bilanciamento del browser cerca l'altezza minima, quindi con poche schede su un monitor molto largo alcune colonne restano vuote a destra: non è un difetto, è che la sala ha poco dentro. Le schede restano larghe ~340-420 px, la misura per cui sono disegnate: allargarle a 600 px spanderebbe righe e tabelle.
- 🔴 **La cartina non si spegne, si copre.** `#side` è opaco e sta sopra: niente `display:none` su `#map`, che costringerebbe Leaflet a rimisurarsi al ritorno.
- 🔴 **In modalità muro i livelli di cartina si nascondono** (dal 23/09/2026 `body.muro #sideMap` e `body.muro #nav #soloBtn`, prima `body.muro #nav [data-l]`): la cartina è coperta, e un comando che non produce nulla è un invito a sbagliare — la stessa regola per cui la stellina non compare dove la Mia Sala non sa ricostruire la scheda. `render()` richiama `navArrUpd()` perché le frecce del menu contano ciò che resta fuori dal riquadro.

🔴 **La Mia Sala si prova riempiendola, non con una scheda sola (22/09/2026).** Aggiunta e rimozione di una scheda funzionavano, e il difetto è comparso solo mettendocene sei prese da viste diverse: nell'intestazione i comandi ▲ ▼ ✕ sono un **terzo** elemento accanto a titolo e sottotitolo, e in un flex in riga il titolo — che è **testo nudo**, quindi un elemento anonimo che si stringe prima di tutti — si spezzava in colonna su tre righe («ALTRE REGIONI — AVVISI / METEO / ALARM»). Rimedio in due mosse: il titolo va in un `<b class="wxT">` suo (`miaTitoloBox`), e l'intestazione che porta comandi prende la classe `wxHdCmd` e diventa una **griglia a due righe** — titolo a tutta larghezza, sottotitolo sotto, comandi a destra di entrambi. 🔴 `miaId` continua a produrre **lo stesso identificatore di prima** (`miaTesto` legge indifferentemente il `.wxT` o i nodi di testo): gli id sono già salvati nei browser delle persone, cambiarli svuoterebbe la Mia Sala di chi l'aveva già composta.

⚠️ **I pulsantini ▲ ▼ ✕ avevano il bordo a 1,1:1**, cioè invisibile: stesso difetto della stellina, trovato guardando la stessa schermata. Portati a `--dim` (5,2:1) e a 29 × 26 px.

🔴 **Lo stato vuoto usa l'idioma grafico della Sala, non paragrafi in fila.** Prima erano cinque `<p>` uno sotto l'altro, e l'utente lo ha bocciato: *«non mi piace come hai graficamente impostato i testi»*. Ora sono tre riquadri numerati `.miaBox` — cornice sottile `--line` più **filetto colorato di 3 px a sinistra** (ciano, giallo, verde) e titolino in monospazio — che è lo stesso stilema di `.rstep`, `.ems` e `.stato` già usati in pagina; le viste sono **pastiglie** `.miaVp` (piene quelle raccoglibili, tratteggiate e in `--dim` quelle escluse) invece di un elenco in grassetto dentro una frase. Contrasti calcolati su `#0a1826`: `--cyn` 9,20:1 · `--gia` 12,70:1 · `--grn` 10,41:1 · `--tx` 12,51:1 · `--dim` 5,11:1. **Una fila di riquadri nuova si scrive con `.miaBox` e `--bc`**, non con classi inventate: è la stessa regola già imparata con `.vfPill`.

⚠️ **Lo stato vuoto della Mia Sala deve dire DOVE sono le stelline.** Diceva «apri una vista qualsiasi», ma il pulsante c'è solo nelle **sette** viste di `MIA_FN`: chi apriva WINDY o NAVI non lo trovava e concludeva che la funzione fosse rotta. Ora le elenca per nome e spiega perché le altre non ce l'hanno.

🔴 **Come si raccolgono le schede senza riscrivere ogni vista.** `miaRaccogli(vista)` punta **temporaneamente** `feed` a un contenitore staccato dal documento, chiama la funzione della vista, riprende le `.wx` prodotte e rimette tutto a posto (titolo del pannello compreso, altrimenti la Mia Sala eredita il nome dell'ultima vista raccolta). Per questo `feed` è `let` e non `const`. Conseguenza voluta: **una scheda nuova diventa selezionabile da sola**, senza che nessuno debba ricordarsene — stesso principio delle pastiglie ricavate dai dati.

- **Identificatore stabile**: `vista|titolo`, dove il titolo è il testo dell'`h3` **escluso** lo `<span>` (che contiene i conteggi variabili). Memoria locale in `pcgz-monitor-mia-sala`, per dispositivo, mai inviata altrove.
- **Viste raccoglibili** in `MIA_VISTE`/`MIA_FN`: escluse quelle che incorporano un riquadro di terzi o una tela (Windy, traffico, navi, radio, carte) — non sono schede, e duplicarle aprirebbe due volte lo stesso servizio esterno. 🔴 **`miaDecora` non mette la stellina dove `MIA_FN` non arriva** (`if(!MIA_FN[vista])return`): fino al 22/09/2026 la metteva ovunque, e una scheda scelta da una vista esclusa restava per sempre «al momento non disponibile». Una stellina che si preme e non porta a nulla è un invito a sbagliare: si toglie il comando, non si scrive l'avvertenza. **Aggiungendo una vista a `MIA_FN` la stellina compare da sola**, senza toccare altro.
- ⚠️ **Nella Mia Sala il battito dei satelliti non corre** (`ORB_TICK` si attiva solo a vista `orb` aperta o livello acceso): una scheda dei satelliti tenuta lì si ricalcola quando `viewMia()` la ricostruisce, cioè al ritorno di un caricamento, non ogni quindici secondi. Resta onesta perché scrive l'ora dell'ultimo calcolo; se un giorno la si vuole viva anche lì, si allarga la condizione del battito, tenendo conto che ogni giro ricostruirebbe il pannello.
- **`data-nomia="1"`** su una scheda la rende non selezionabile: serve per le schede di **dettaglio** che dipendono da una selezione (i passaggi di un satellite), che altrimenti sparirebbero dalla Mia Sala.
- Una scheda scelta che al momento non c'è (la sua fonte non ha dati) **non fa sparire nulla**: la Mia Sala lo dice in una riga e la scheda torna al suo posto appena la fonte risponde. 🔴 Perché torni davvero serve che i caricamenti ridisegnino **anche** la Mia Sala: `rendSe(vista)` (ridisegna se si è in quella vista **o** in `mia`) sostituisce `if(S.view==="<vista>")render()` nei caricamenti delle sette viste raccoglibili. Prima del 22/09/2026 ognuno ridisegnava solo la propria, e restando in Mia Sala la riga di indisponibilità sopravviveva al ritorno dei dati finché non si cambiava vista e si tornava indietro. I caricamenti della RADIO restano com'erano: in Mia Sala non può comparire. **Un caricamento nuovo per una vista raccoglibile chiude con `rendSe`**, non con il confronto diretto.

**Filtri: uno stile solo per tutta la pagina.** 🔴 `.vfPill`/`.voloFiltri` erano stati usati **senza scriverne il CSS**: il browser rendeva i pulsanti col suo default — fondo bianco, nessuna spaziatura — ed era andato live così (segnalato dall'utente: «questo sfondo bianco e tutti appiccicati non è il massimo»). Sono stati **eliminati** in favore di `.fchip`/`.fchips`, che già esistevano ed erano stilati, migliorati con forma a pastiglia, più aria e le file **etichettate** (`.filtriGruppo`/`.filtriTit`): tre file di pastiglie senza titolo non dicono che cosa distinguano. Chi aggiunge una fila di filtri usa queste classi; non se ne inventano altre. Il contrasto dei testi secondari è stato **calcolato**, non stimato: `--dim` dava 3,91:1 e 4,16:1, sotto il livello AA, quindi per contatori e titoli di fila si usa `#709080` (5,2:1 e 5,6:1).

CSP: `celestrak.org` in `connect-src` (rule 05). Fonte da aggiungere a `check-fonti-cruscotto.py`.

## Sala situazioni `/monitor/` — vista NAVI, e perché gli aerei non si possono incorporare (22/09/2026)

Richiesta dell'utente: *«per gli aerei e navi utilizza i software online, perché non possiamo permetterci nessun tipo di hardware o di acquistare le licenze. Devi praticamente fare come Flightradar o MarineTraffic»*.

**Navi: si può, e si fa.** Vista `data-v="mar"` (slug `navi`): mappa AIS di **VesselFinder**, che l'incorporamento lo **pubblica apposta** (pagina `/embed` del loro sito) — permesso per pubblicazione, nessuna chiave, nessun costo. Click-to-load come Windy e Waze.

🔴 **Si usa l'iframe, non il loro `<script>`.** Il codice che pubblicano è uno script che costruisce un iframe verso `/aismap` col parametro **`ra`** (l'indirizzo della pagina ospite: è così che autorizzano l'incorporamento — senza, l'endpoint risponde «Forbidden»). Qui si costruisce direttamente quell'iframe: è l'uso previsto, e tiene il codice di terzi **fuori dalla nostra origine**, dove avrebbe accesso pieno alla pagina. La CSP del sito non ammette script di terze parti, e questa non fa eccezione: `www.vesselfinder.com` va in **`frame-src`**, mai in `script-src`.

🔴 **L'AIS non è un censimento di ciò che naviga**: lo trasmettono i mercantili sopra una certa stazza, i passeggeri e chi lo monta per scelta; pescherecci piccoli, diporto e molti mezzi di Stato non compaiono, e la copertura dipende dalle stazioni riceventi a terra. La scheda lo dice, e rimanda alla Guardia Costiera (1530) per le emergenze in mare.

🔴 **Chiudere un riquadro di terzi: `src=""` NON basta.** Il browser lo risolve sull'indirizzo della pagina corrente e il contenuto resta caricato (verificato il 22/09/2026). Serve **`about:blank`** — costante `VUOTO`, applicata anche alle viste Windy e traffico, che avevano lo stesso difetto. Verifica: dopo la chiusura nessun riquadro figlio deve avere l'URL del terzo.

🔴 **La mappa incorporata si può, il dato grezzo no: sono due cose diverse.** La vista NAVI mostra la **mappa di VesselFinder dentro un riquadro**, cosa che loro consentono gratuitamente per la pubblicazione. Il **flusso AIS grezzo** — le posizioni delle navi da ingerire e disegnare sulla nostra cartina, come si fa con i mezzi aerei — quello **non è gratuito né disponibile**: AISHub lo concede solo a chi contribuisce con un proprio ricevitore, MarineTraffic e VesselFinder lo vendono. Verificato il 22/09/2026. Conseguenza pratica: sul mare **non si può filtrare, evidenziare o incrociare nulla** con i nostri dati, perché le navi non passano da noi — si guarda la loro mappa così com'è. Se un giorno il Gruppo installasse un ricevitore AIS, la strada del dato grezzo si aprirebbe.

⚠️ **Da non confondere leggendo in fretta:** «VesselFinder è a pagamento» (vero del **dato**) e «l'incorporamento di VesselFinder è gratuito e permesso» (vero della **mappa**) convivono, e la prima stesura di questa sezione le accostava senza distinguerle — una sessione futura poteva leggerne una e smontare la vista NAVI credendola non consentita. Segnalato in revisione il 22/09/2026.

**Aerei: nessuna via libera e lecita esiste.** Verificato uno per uno il 22/09/2026, prima di scrivere codice:

| servizio | incorporabile? | esito |
|---|---|---|
| **Flightradar24** | ❌ | `X-Frame-Options: SAMEORIGIN` su `/simple` e `/simple_index.php` |
| **Plane Finder** | ❌ | `SAMEORIGIN` |
| **adsb.fi** (globe) | ❌ | `SAMEORIGIN` |
| **airplanes.live** (globe) | ❌ | `SAMEORIGIN` |
| **RadarBox / AirNav** | ❌ | nessuna intestazione, ma reindirizza ad `airnavradar.com` che *refused to connect* |
| **ADS-B Exchange** | ⚠️ tecnicamente **sì** | **vietato dalle condizioni**: l'Acceptable Use Policy proibisce di «pubblicare, rivendere, trasmettere, diffondere il servizio» (§6.9), di «consentire l'accesso a chiunque non sia un utente autorizzato» (§6.7) e ogni uso «non esplicitamente permesso» (§6.8) |
| **MarineTraffic** | ❌ | `SAMEORIGIN` (per le navi si usa VesselFinder) |

Il caso ADS-B Exchange è quello da ricordare: **si carica benissimo in un iframe** (provato: 222 aerei sull'Italia centrale, 12.354 in totale) e sarebbe bastato incorporarlo. È lecito che manchi, non tecnico. **Non si incorpora.**

**Gli aerei in diretta si fanno con un ponte sul nostro server (22/09/2026).** Richiesta dell'utente: *«serve per forza vedere in che posizione sono durante un'emergenza»*. Poiché la mappa altrui non si può incorporare e la fonte non si può chiamare dal browser, la Sala legge **`static/api/aerei.php`**, che sta sul nostro dominio ed è quindi stessa origine: la CSP non cambia (`connect-src 'self'` copre già), nessun servizio di terzi viene contattato dal browser, nessun account nuovo. 🔴 È **l'unica eccezione** alla regola del sito statico, dichiarata per esteso in rule 05 § "L'unica eccezione al sito statico".

🔴 **Fonte adsb.lol, non adsb.fi, ed è una questione di licenza.** adsb.fi scrive *«open data is for personal, non-commercial use only»*: un sito istituzionale pubblico «personale» non è. adsb.lol pubblica tutto sotto **ODbL 1.0** — la stessa di OpenStreetMap — che la ridistribuzione la consente a chiunque, con **attribuzione obbligatoria** (sta nella scheda e nel JSON, non si toglie). Spostata sulla stessa fonte anche la fotografia, così non convivono due licenze diverse per lo stesso dato. `airplanes.live` resta esclusa: la sua API richiede autorizzazione scritta preventiva.

🔴 **La classificazione va per DESIGNATORE ICAO, e i codici si verificano.** adsb.lol non manda la descrizione testuale del modello (campo `desc` di adsb.fi): manda `t`, il designatore. Le regole stanno in **`static/api/volo-classificazione.json`**, letto sia dal ponte PHP sia dal generatore Python, perché scritte due volte prima o poi divergono. Verifica fatta interrogando la fonte per tipo, non a memoria:
- `CL2T` ✅ **confermato**: ha restituito **I-DPCE** (flotta del Dipartimento) e **F-ZBEU «PELIC42»** (Sécurité Civile francese). È il Canadair.
- `S64` ✅ confermato (Erickson Aircrane).
- `AT8T` ❌ **escluso**: lo stesso codice copre l'AT-802F antincendio **e** l'AT-802 agricolo, che la fonte non distingue.
- `CL41` ❌ escluso: rischia di indicare il CT-114 Tutor, non il CL-415.
- `BE20` ❌ **escluso, e istruttivo**: interrogandolo sono tornati **73 Beechcraft King Air**. Se fosse stato preso per il Beriev Be-200, settantatré aerei d'affari sarebbero diventati bombardieri d'acqua. **Un designatore non verificato non si aggiunge**: un codice sbagliato etichetta male centinaia di velivoli tutti insieme.

🔴 **Due cadenze e due nomi.** In diretta si rinfresca ogni **20 secondi** (a 400 nodi sono quasi 4 km) e la scheda dice «IN DIRETTA» con l'ora della lettura; sulla fotografia si resta a 5 minuti e la scheda dice «FOTOGRAFIA». Fermo a scheda nascosta. **La scheda deve sempre dire quale delle due sta mostrando**: fra «adesso» e «un quarto d'ora fa», per un velivolo, ci sono decine di chilometri.

⚠️ **Una risposta che si legge ma è vuota non è un dato.** Passando da adsb.fi (chiave `aircraft`) ad adsb.lol (chiave `ac`), il generatore ha letto la fonte, non ha trovato nulla e ha **sovrascritto una fotografia buona con una vuota**, senza che nulla segnalasse il guasto: il fail-safe copriva le eccezioni, non il silenzio. Ora c'è una guardia esplicita — sopra l'Italia centrale zero velivoli significa schema cambiato, non cielo vuoto — e lo stesso controllo è in `check-fonti-cruscotto.py`.

## Sala situazioni `/monitor/` — la legenda che si stirava (22/09/2026)

Segnalato dall'utente da telefono: alla prima apertura una **striscia verticale** occupava il lato destro dello schermo. Era la legenda del campo previsionale ICON-2I (`#prevLeg`).

🔴 **Un'immagine stretta dentro un flex in colonna si stira, e l'altezza segue.** `#prevCtl` (dal 23/09/2026 dentro la striscia SULLA CARTINA del pannello METEO, non più sulla cartina: la regola vale uguale) è `display:flex;flex-direction:column`, quindi per impostazione predefinita (`align-items:stretch`) allarga i figli alla larghezza del riquadro. Le legende di ItaliaMeteo sono alte e strettissime — la temperatura è **22 × 894 px** — e stirata a 132 px diventava alta **5285 px**: quasi sei schermate, col riquadro che partiva 4578 px sopra il bordo superiore. Misurato in browser, non dedotto. Rimedio: `align-self:start` per la larghezza vera, più un riquadro `#prevLegBox` con tetto d'altezza (`min(38vh,300px)`, `min(32vh,240px)` su telefono) che **scorre** invece di rimpicciolire la scala a filo illeggibile. Da 586% a 35% dell'altezza schermo.

🔴 **Un'area che scorre dev'essere raggiungibile da tastiera** (`tabindex="0"` + `role="group"` + `aria-label` + fuoco visibile): axe la segnala come `scrollable-region-focusable`, ed è una violazione che il rimedio stesso introduce se non ci si pensa. Trovata eseguendo axe sulla pagina, che **non è nel campione di `pa11y-ci`**: su questa pagina il controllo è a carico di chi la tocca.

⚠️ La legenda è accesa dal menu del campo previsionale, e quella scelta è **persistita** in `pcgz-monitor-cfg`: per questo ricompariva «alla prima apertura» di ogni visita successiva, non una volta sola.

## Sala situazioni `/monitor/` — pronto soccorso in diretta (22/09/2026)

Richiesta dell'utente, ripetuta: *«non riesci proprio a mettere online i dati? sempre per questione di utilizzo in emergenza»*. Scheda in testa alla vista **EMERGENZE**: i dieci pronto soccorso più vicini a Genzano, con quante persone sono in attesa e per quale codice di triage. Dato della **Regione Lazio** (CC BY 4.0), letto attraverso il ponte `static/api/pronto-soccorso.php`.

🔴 **Non è una guida per scegliere l'ospedale, e la scheda lo dice per prima cosa.** In emergenza si chiama il **112**: è la centrale che decide dove portare la persona, in base alle sue condizioni e alle specialità disponibili, e un codice grave non fa la fila. Questi numeri dicono il **carico** sulle strutture del territorio a chi presidia la sala, non dove conviene andare. Se un giorno qualcuno volesse togliere quell'avvertenza per far spazio, è il contrario di quello che serve: il rischio vero di questo dato è che un cittadino si metta in auto verso il pronto soccorso che sembra più sgombro.

🔴 **Perché serve il ponte.** Il servizio risponde **400** quando la richiesta porta l'intestazione `Origin` — cioè proprio quando parte da una pagina web di un altro sito. Verificato il 22/09/2026 con GET e con OPTIONS: senza `Origin` risponde 200, con `Origin` no. Non è il solito «manca il CORS»: è un rifiuto attivo, e nessun accorgimento lato pagina lo aggira.

🔴 **Il riuso è previsto dalla fonte**, non solo tollerato: il dato è pubblicato come open data («Pronto Soccorso - Accessi in tempo reale», `dati.lazio.it`) sotto CC BY 4.0, e la Regione invita espressamente a costruirci applicazioni — una sul pronto soccorso esiste già nella sua vetrina. L'attribuzione sta nella scheda e dentro la risposta del ponte: non si toglie.

**Tre cose imparate trovandolo, che fanno risparmiare mezza giornata:**

1. **Il catalogo open data non è il servizio.** La risorsa su `dati.lazio.it` è un CSV fermo al **31 luglio 2021** con frequenza dichiarata «ANNUAL», e guardando solo quella si conclude — come era stato concluso — che il dato in tempo reale non esista. Esiste: vive nel portale, non nel catalogo. **Quando una fonte ha un sito o un'app che mostrano il dato aggiornato, dietro c'è un endpoint**, e la scheda del catalogo non dice nulla su di esso.
2. **`006` è il pronto soccorso, `009` è lo studio medico.** L'indirizzo pubblico del portlet contiene `facilityTypeIds=009`, e prenderlo per buono fa interrogare gli studi medici: il primo elenco tornava «STUDIO MEDICO di…». I codici veri si leggono da `/facility/structures/healthcare-facility-type`.
3. **La geometria è `{latitude, longitude}`**, non un array `coordinates` in stile GeoJSON: leggendola come GeoJSON tutte le distanze vengono nulle e l'ordinamento per vicinanza sparisce senza errori.

**Endpoint** (base `https://server.salutelazio.it/server/external-services`): `/facilities/structures/list` per l'elenco (vuole il riquadro `westLng/southLat/eastLng/northLat`, `zoom`, `lang`, `page`, `limit`, più `facilityTypeIds`), `/facilities/structures/emergency-status?facilityId=<PS…>` per lo stato. Nessuna chiave, nessuna autenticazione. Copia locale nel ponte: 60 s per lo stato, 6 h per l'elenco degli ospedali, così cento visitatori restano poche richieste al minuto.

**Resa.** Una riga per ospedale: nome (senza il prefisso «Pronto Soccorso», ripetuto dieci volte non informa), distanza da Genzano, totale in attesa, e una pastiglia per ogni codice con pazienti. 🔴 **Il colore del triage sta solo sul bordo e sul pallino, mai sul testo**: l'etichetta è scritta a parole («Urgenza Differibile 6») perché l'informazione non passi dal solo colore (WCAG 1.4.1), e il testo resta `--tx` a 12,79:1. Una struttura che non risponde mostra **«—» e «stato non disponibile»**, mai `0`: zero in attesa e dato mancante sono informazioni opposte. Contrasti calcolati, non stimati: `--dim` 5,23:1, accento del 112 11,05:1, i colori della fonte fra 3,57:1 e 18,34:1 come elementi grafici.

**Battito** 60 s, fermo a scheda nascosta. Fuori da Aruba il PHP non gira e la scheda si spegne dichiarandolo: per questo dato **non esiste fotografia di ripiego**, perché un carico di pronto soccorso di un quarto d'ora fa è già un'altra cosa e di ieri non significa niente. Fonte sorvegliata da `check-fonti-cruscotto.py` (controlla che tornino i gruppi di triage, non solo che risponda).

## Sala situazioni `/monitor/` — vista RADIO (ascolto SDR, settembre 2026)

`static/monitor/index.html` (pagina statica a viste, fuori da Hugo) ha la vista **RADIO** (`data-v="rad"`, hash `#radio`; nessuna scorciatoia da tastiera — è il dodicesimo tab e i tasti arrivano al nono): ascolto delle bande radioamatoriali con **spettro, waterfall e audio nella pagina**: la Sala è un **client WebSocket** del server OpenWebRX+ (motore `RE`: `reOpen/reApply/reOnBin`, codec `PcAdpcm`, canvas `#rxSpec`/`#rxWf`, barra `#rxBar`) verso due ricevitori (`RADIO_RX`: IZ0FKE Roma `https://sdr.noantri.org/`, predefinito, 8 SDR in parallelo al 19/09/2026 (2 m, 10/40/20/80 m, 6 m, 70 cm su due profili, QO-100); I6IQX Bucchianico `https://sdr-plus.i6iqx.it/` per 160/60/30/17/15/12 m e PMR446; `radioSetRx()` cambia server e ricollega), click-to-load come `#windyWrap` (wrapper `#radioWrap`, `S.radio`, `radioSync()`), con pannello laterale di sintonia: gruppi HF/VHF/UHF/uso libero, bande con limiti «da … a …» (`RADIO_BANDE`, kHz, IARU R1 + PNRF), frequenze notevoli (`RADIO_PRESET`), sintonia manuale, selettore del ricevitore, link ai ricevitori solo-http della zona (`RADIO_LINK`, mai in iframe: mixed content), riquadro «e per trasmettere?». Regole:

- **Sintonia via protocollo**: `radioTune()` → `reApply()`: se la frequenza cade nel profilo attivo (`|f − centro| ≤ banda/2`) manda `dspcontrol` (offset, modo, banda passante dal messaggio `modes`, squelch); altrimenti `selectprofile` col profilo che la copre (`reProfFor()`: coperture da `status.json` + imparate dai `config`) e ritenta alla nuova `config`. Cambi di profilo distanziati ≥3 s (il server bandisce i "profile-scanning robots"). 🔴 **Non tornare all'iframe**: l'hash `#freq=` funziona solo nel profilo attivo (sempre il 2 m all'apertura) — è il difetto della prima versione, sostituita il 03/09/2026. Il link «Nuova scheda» resta per il ricevitore completo.
- **Flusso binario**: byte 0 = tipo (1 FFT, 2 audio); FFT ADPCM senza sincronismo (codec azzerato a ogni frame, primi 10 valori da scartare, valori/100 = dB); audio ADPCM con «SYNC» + indice/predittore, ricampionato a `AudioContext.sampleRate` e riprodotto via `ScriptProcessorNode` (niente file esterni per la CSP). Livelli del waterfall automatici (percentili smorzati), S-meter = 10·log10 del valore lineare del server. Test locale possibile con una cattura reale del flusso e un server di replay `ws` (procedura nella PR di correzione del 03/09/2026).
- **Profili live**: `radioLive()` legge `status.json` (CORS aperto su IZ0FKE, assente su I6IQX → resta la copia incorporata) e aggiorna `profili` del ricevitore in uso; `radioProf(hz, rx)`/`radioAltRx(hz)` decidono copertura e suggerimento «Passa a …». CSP: entrambi gli host in `connect-src` (`https://` per status.json **e** `wss://` per il WebSocket) e in `frame-src` (rule 05). Fonti monitorate da `check-fonti-cruscotto.py`.
- **Riconnessione automatica (23/09/2026)**: se il WebSocket si chiude senza che lo abbiamo chiesto noi e il ricevitore è acceso, `ws.onclose` ritenta `reOpen()` al massimo 5 volte con attesa crescente (3, 6, 12, 24, 30 s; contatore `RE.retry`, azzerato quando il ricevitore parte davvero), mai dopo un messaggio `backoff` del server (`RE.noRetry`) e mai su una chiusura nostra (`reClose` azzera `onclose` e il timer `RE.retryT`); esaurite le prove, torna «premi RICOLLEGA». È ciò che fa il client ufficiale di OpenWebRX; prima il ricevitore lasciato acceso in sala restava muto al primo inciampo di rete.
- **Solo ascolto**: nessuna funzione di trasmissione, mai; il riquadro legale resta, con le citazioni verificate su Normattiva (art. 134 c. 4 ascolto libero; art. 134 + All. 26 per trasmettere; art. 105 c. 1 lett. p CB; PMR446 PNRF nota 101C). Le frequenze del Gruppo assegnate dal MIMIT **non** si pubblicano.
- **Dati**: bande e frequenze notevoli con fonte (IARU R1, PNRF MIMIT, AMSAT-DL per QO-100, articoli del sito per Rete Zamberletti e rete metropolitana di Roma). Aggiungere un preset = una riga in `RADIO_PRESET` con banda, kHz, modo, categoria e fonte verificata; niente frequenze "sentite dire".
- **Funzioni del ricevitore nella pagina (19/09/2026)** — richiesta dell'utente: *«inserisci tutte le loro funzionalità nel nostro monitor»*. La Sala gestisce ora tutti i messaggi del protocollo che il client di OpenWebRX+ v1.2.117 gestisce, verificati con una cattura reale del flusso: `modes` (elenco completo, con `type` analog/digimode, `requirements`, `underlying`, `bandpass`) + `features` (capacità installate sul server: i modi si offrono solo se i requisiti sono soddisfatti) → select del modo e del decoder nel pannello; `bands` → nastro del piano delle bande in fondo allo spettro (colore per `tags`); `dial_frequencies` → segni viola e pulsanti «frequenze dei modi digitali del profilo»; `bookmarks` → segni gialli sulla scala + elenco cliccabile (etichette diradate: si scrive solo quella che non si sovrappone alla precedente); `secondary_config` (`secondary_fft_size`, `if_samp_rate`) + frame binario **tipo 3** (FFT secondaria, ADPCM come lo spettro) → waterfall del canale audio nel pannello decoder, clic = `secondary_offset_freq`; `secondary_demod` → pannello dei messaggi decodificati (tabelle per famiglia: WSJT FT8/FT4/JT65/JT9/WSPR/FST4/Q65/MSK144/JS8 con nominativo linkato a `callsign_url` del server; packet APRS/AIS/sonde/QO-100 con posizione sulla mappa; POCSAG/Page; DSC; HFDL/VDL2/ACARS; ISM/WMBUS; SSTV e fax come canvas riga per riga da pixel BGR base64; Meshtastic/LoRa/SelCall/EAS/skimmer come coppie chiave/valore; **stringa** = testo grezzo di BPSK/RTTY/CW/NAVTEX/SITOR in un `<pre>`); `metadata` (DMR/D-Star/YSF/NXDN/M17: chi parla, verso chi, slot/TG, GPS se presente) → riga `#rxMeta`; `cpuusage`/`temperature`/`battery`/`clients` (+ `max_clients` dal config) → riga `#rxSrv`; `log_message`/`backoff` → stato. Comandi verso il server: `dspcontrol` con `secondary_mod` (o `false` per spegnere il decoder) e `secondary_offset_freq`; `mod:"empty"` per i decoder con `underlying: ["empty"]` (ISM, LoRa, Meshtastic, skimmer: niente audio); riduzione del rumore con `connectionproperties {nr_enabled, nr_threshold}` (−20…+20 dB). Lato client: passo di sintonia (`tuning_step` del profilo, modificabile; frecce ◀ ▶ e tastiera ← → ↑ ↓ quando la vista RADIO è attiva e il fuoco non è in un campo), tavolozze del waterfall (`waterfall_colors` del ricevitore + teejeez/ha7ilm/ocean/eclipse/turbo/sala) e livelli (auto = percentili; ricevitore = `waterfall_levels` del profilo; manuali), **registrazione WAV** sul dispositivo (PCM 16 bit mono alla frequenza audio del ricevitore, Blob + `<a download>`, massimo 10 minuti, solo se `allow_audio_recording`), **scanner** sui segnalibri `scannable` e sulle frequenze notevoli analogiche del profilo (livello = massimo della FFT ±2 bin smorzato; soglia = squelch − 13 dB come nel client del ricevitore, con squelch aperto = livello alto del waterfall − 12 dB; si ferma finché il segnale resta sopra soglia), **modalità mappa** (`#radioWrap.split`: ricevitore nella metà bassa, mappa sopra con il layer `radioAprsLayer` delle posizioni decodificate, che restano in tutte le viste per 2 ore), orologio UTC. 🔴 **Squelch**: ogni `config` che porta la chiave `initial_squelch_level` reimposta il cursore (valore `null` = −150, aperto), come fa il client del ricevitore: senza questa regola il −52 dB del profilo VHF resta applicato all'HF e ammutolisce tutto. Non integrata la **chat** del ricevitore: il server la tiene spenta (`allow_chat: false`) e una chat pubblica non moderata non ha posto su un sito istituzionale. I link ai servizi dello stesso operatore (cruscotto radioamatoriale, WEBCLX, terminale e gateway APRS, LoRa, Meshtastic, TinyGS, mappa, file registrati) stanno in `RADIO_RX.noantri.strumenti` e si aprono in nuova scheda: nessun host nuovo nella CSP.
- **Test in locale senza il ricevitore**: si registra il flusso reale (frame testuali e binari con l'istante di arrivo, dopo l'handshake e un eventuale `selectprofile`/`dspcontrol`), lo si riproduce con un piccolo server `ws` sulla stessa cadenza e si apre la Sala con `window.PCGZ_RADIO_WS_OVERRIDE="ws://127.0.0.1:8765/ws/"` (init script di Playwright): decoder, scanner, registrazione e mappa si verificano così, screenshot a 1280 e 375 letti davvero. Il server di replay ignora ciò che il client manda.
- La configurazione (ricevitore, frequenza, modo, decoder, gruppo, banda, modalità mappa, tavolozza, livelli, riduzione del rumore, passo) è persistita in `pcgz-monitor-cfg` (valori validati al ripristino); l'accensione del ricevitore no (click-to-load esplicito). Documentazione utente: `manuale/parte-36` § 36.8.

## Partial `indice-pagina` — indice di pagina con scrollspy (site-wide)

`themes/flavour-pcgenzano/layouts/partials/indice-pagina.html` produce l'**indice "In questa pagina"** (navscroll Bootstrap Italia semplificato): elenco da `.TableOfContents`, sticky a sinistra su desktop (colonna 2-col in `_default/single.html` e `_default/list.html`), accordion collassabile su mobile. `static/js/indice-pagina.js` evidenzia la sezione corrente mentre si scorre (scrollspy → `.active` + `aria-current` sui link). CSS sezione **INDICE DI PAGINA v1.0**.

- **Gate site-wide**: compare automaticamente sulle pagine con `len .Fragments.Identifiers >= 3` (≥3 heading). ⚠️ Non usare `len .Fragments.Headings` (top-level): in Hugo 0.154 risultava inaffidabile (tornava 1).
- **Opt-out**: `indice: false` oppure `toc: false` nel frontmatter.
- **Escluse** (pagine-strumento): `cruscotto`, `laboratorio-meteo`, `cerca`, `emergenza`, `lanterna`, `mappa-sito`, `attribuzioni-pittogrammi` (più `comunicazioni` su list.html).
- Sostituisce il vecchio TOC in `<details>` (rimosso da single.html/list.html). Mantiene `id="indice"` per il back-to-top contestuale.

## Partial `barra-lettura` — barra di avanzamento lettura (luglio 2026)

`themes/flavour-pcgenzano/layouts/partials/barra-lettura.html` + `static/js/barra-lettura.js` + CSS sezione **BARRA AVANZAMENTO LETTURA v1.0**: barra sottile blu istituzionale (4px, `#003366`) fissa in cima al viewport che si riempie con lo scorrimento del corpo dell'articolo (pattern Salute Lazio mobile). Il partial riceve `(dict "selector" ".article-body")` — il selettore del contenuto da misurare — ed è chiamato dentro il gate del box strumenti (`$ttsEnabled` + `WordCount > 30`) in `_default/single.html` (`.article-body`) e `manuale/single.html` (`.manuale-body`). **Solo template single**, mai list (misurerebbe il solo intro). JS: scroll listener passivo + rAF, `transform: scaleX` compositor-only, `aria-valuenow` a passi del 5%. Dettagli accessibilità in `03-accessibility.md` § "Barra avanzamento lettura".

## Adozione catalogo Bootstrap Italia — luglio 2026 (audit componenti)

Esito dell'audit sistematico del catalogo BI 2.18.1 (richiesta utente 10/07/2026). Componenti aggiunti:

- **BottomNav** — partial `bottom-nav.html`, incluso da `baseof.html` (guardia `ne .Type "emergenza"`): barra azioni rapide fissa in basso SOLO <992px (stessa soglia del SOS-112) con Emergenza / Allerte / Numeri / Cerca, stato attivo per sezione. `body.has-bottomnav` (classe impostata in baseof) rialza i pulsanti flottanti (SOS, Assistente, a11y-fab, torna-su) sopra la barra. 🔴 **Speculare in `static/app-shared/site-chrome.js`** (`BOTTOMNAV_HTML` + `injectBottomNav()`): ogni modifica alle voci va replicata (vincolo chrome, rule 04b). CSS sezione **BOTTOM NAV v1.0** (varianti contrasto a11y incluse).
- **Video Player** (`data-bs-video` + video.js) — shortcode `video` (`src` obbligatorio, `poster`/`titolo`/`caption` opzionali) per video locali self-hosted. Il runtime `static/vendor/videojs/video.min.js` (v8, vendorizzato da npm, licenza Apache-2.0 nel folder) è caricato da baseof SOLO sulle pagine che usano lo shortcode (flag `.Page.Store "usaVideoPlayer"`), PRIMA del bundle BI che aggancia `window.videojs`. Usato dai 2 video della campagna Regione Lazio.
- **Forward** — freccia di avanzamento nel hero homepage (solo modalità ordinaria) verso l'ancora `#dopo-hero`. CSS sezione **FORWARD v1.0**.
- **Torna indietro** — partial `torna-indietro.html` in fondo alle single (via `_default/single.html`, `rischi-prevenzione/single.html`, `pittogrammi/single.html`): link deterministico alla sezione padre (mai `history.back()`). Auto-protettivo: niente su comunicazioni (ha già il suo link) né su pagine figlie della home. CSS **TORNA INDIETRO v1.0**.
- **Avatar** — iniziali (componente Avatar BI, `aria-hidden`) accanto ai nomi del Consiglio direttivo in `/chi-siamo/`. CSS **AVATAR DIRETTIVO v1.0**.
- **Notifiche (toast)** — `static/js/pc-notifiche.js` espone `window.pcNotifica(titolo, testo, tipo)` (markup `.notification` BI, `role=alert`, chiusura X/ESC/8s, nessuna animazione). Agganciato a: salvataggio piano offline (`/piano-familiare/`) e attivazione notifiche allerta (`notifiche-allerta.js`). CSS **PC-TOAST v1.0**.

**Esclusi con motivo** (decisione utente + audit): widget valutazione pagina e Rating (rifiutati dall'utente); Sections (duplicherebbe il sistema di sezioni custom della homepage); Chips (duplicato delle filter-pills); Tooltip (inaffidabili su touch); form/upload/transfer/datepicker (nessun backend); avatar/dimmer/overlay/affix/thumbnav/sidebar (pattern da portale applicativo).

## Render hook tabelle (`_markup/render-table.html`)

Tutte le tabelle Markdown del sito sono rese dal hook `themes/flavour-pcgenzano/layouts/_default/_markup/render-table.html`. Comportamento:

- **`<th scope="col">` automatico** su ogni cella di intestazione (riga in `<thead>`). Migliora il riconoscimento da screen reader e rispetta WCAG 1.3.1 (Info and Relationships). Nessun editing manuale per pagina: si applica a tutte le tabelle Markdown del sito (oltre 400 `<th>` gestiti automaticamente).
- **Wrapping automatico in `.table-responsive`** Bootstrap Italia per scroll orizzontale su mobile sulle tabelle larghe.
- **Allineamento colonne** preservato dal Markdown (`:---`, `---:`, `:---:`) → reso come `style="text-align: ..."` sulle celle.
- **`<caption>` opzionale** via `Attributes.caption` o `Attributes.title`. **Importante**: la sintassi attribute block di Goldmark `{caption="..."}` **non si applica** alle tabelle Markdown in Hugo (limitazione del parser). Per aggiungere una caption a una tabella specifica, **convertire la tabella in HTML diretto** dentro Markdown:

```html
<div class="table-responsive">
<table>
<caption>Testo descrittivo della tabella</caption>
<thead>
<tr><th scope="col">Colonna A</th><th scope="col">Colonna B</th></tr>
</thead>
<tbody>
<tr><td>...</td><td>...</td></tr>
</tbody>
</table>
</div>
```

Tabelle landing già convertite con caption: `/contatti/`, `/numeri-utili/`, `/chi-siamo/` (con `caption.visually-hidden` perché c'è già un card-header sopra). Per le altre 50+ tabelle la caption non serve: il `<th scope="col">` automatico basta per WCAG, perché ogni tabella è preceduta da un `<h2>`/`<h3>` che la descrive.

CSS scoped sezione **TABLE CAPTION v1.0** in `custom.css`: italico blu istituzionale, allineato a sinistra; helper `.visually-hidden` per caption screen reader-only (nasconde visivamente ma resta accessibile).

**Aggiornamento `hugo.toml`**: il render hook richiede Hugo ≥ 0.142.0. Il file `hugo.toml` ora ha `[markup.goldmark.parser.attribute]` con `block = true` e `title = true` abilitati per uso futuro su altri block element (le tabelle non li usano).

## Render-link hook (link Markdown nel corpo)

Il tema personalizza il rendering dei link Markdown tramite `layouts/_default/_markup/render-link.html` (copia speculare in `themes/flavour-pcgenzano/layouts/_default/_markup/render-link.html`). Comportamento:

- **Link interno `/...` che termina con estensione di file statico** (`.pdf`, `.webp`, `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.zip`, `.mp3`, `.mp4`, `.csv`, `.json`, `.txt`, `.rtf`, `.html`, `.htm`): reso come `<a>` diretto. Serve per linkare file in `static/manuali/`, `static/allegati/`, `static/images/`, `static/open-data/` e micro-siti HTML autonomi in `static/quizpc/`, `static/formazionepc/`, `static/giochi/` senza che il controllo `site.GetPage` li marchi come "non disponibili".
- **Link interno `/.../` (path che termina con `/`) verso cartella con `static/<path>/index.html`**: il hook fa `fileExists "static/<path>/index.html"` e se esiste lo tratta come statico. Serve per scrivere `[Giochi](/giochi/)` senza dover specificare `/index.html`.
- **Link interno `/...` verso pagina Hugo esistente**: `<a>` normale.
- **Link interno `/...` verso pagina non trovata** (e non file statico): `<span class="text-muted" title="Contenuto non ancora disponibile">` — consente di linkare articoli non ancora pubblicati che si attiveranno automaticamente al deploy successivo.
- **Link esterno `http(s)://`**: `<a target="_blank" rel="noopener noreferrer">`.
- **`mailto:` / `tel:`**: `<a>` con `safeURL`.

**Subpath GitHub Pages e `relURL`**: il hook strippa il leading `/` dal link prima di passarlo a `relURL`. Hugo `relURL` **non** aggiunge il subpath del baseURL ai path che iniziano con `/`: `relURL "/foo"` resta `/foo`, mentre `relURL "foo"` diventa `/sito-pc-genzano/foo`. Senza questo strip, tutti i link interni del markdown (che per convenzione scriviamo con leading `/`) funzionerebbero su Aruba (baseURL root) ma sarebbero rotti su GitHub Pages (baseURL con subpath `/sito-pc-genzano/`). Se modifichi il hook, mantieni la riga `$relLink := strings.TrimPrefix "/" $link` e usa `$relLink | relURL` in tutti i branch interni.

Se estendi la lista di estensioni statiche o modifichi il comportamento di `relURL`, aggiorna **entrambi** i file `render-link.html` (progetto e tema) per mantenere la coerenza.

## FAQ accordion (`.faq-item` su `<details>`)

Per ridurre muri di testo in pagine con molte domande/risposte (es. `/allerte-meteo/`, `/faq/`), il sito ha una classe `.faq-item` che stilizza l'elemento HTML nativo `<details>`/`<summary>` come accordion accessibile.

```html
<details class="faq-item">
<summary><strong>Domanda concisa</strong></summary>

Risposta in Markdown standard. Bullet, link, **enfasi**.

</details>
```

Caratteristiche:
- **Semantica nativa**: zero JS, zero ARIA hand-rolled. Lettura corretta da screen reader, navigazione tastiera nativa (Enter/Space su `<summary>`).
- **Chevron CSS-only** (border + transform): nessuna icona da caricare, nessun JS di animazione.
- **Focus visibile WCAG 2.4.7** (outline `#ffbe2e` 3px su `<summary>`).
- **Override stampa**: tutti i `<details>` aperti automaticamente con `display: block !important`, niente icona chevron — il documento stampato include sempre tutto il contenuto.
- **Override mobile** (≤576px): padding ridotto.

CSS scoped sezione **FAQ ACCORDION v1.0** in `custom.css`. Quando si introduce un nuovo accordion FAQ, riutilizzare questa classe: non servono varianti nuove.

## Share buttons (`partials/page-tools.html` + `js/share.js`)

Riga di icone in fondo a ogni articolo e a tutte le pagine che includono il partial `page-tools.html` (cioè: `_default/single.html`, `rischi-prevenzione/single.html`, `pittogrammi/single.html`). Permette al cittadino di condividere il contenuto su WhatsApp, Telegram, Facebook, X (Twitter), LinkedIn, Email, oppure di copiare il link, oppure di usare la condivisione nativa del sistema operativo (Web Share API).

**Architettura privacy-first:**

- **Solo link "share intent" HTML standard** (`https://wa.me/?text=...`, `https://t.me/share/url?url=...`, ecc.): nessun SDK social, niente tracker/cookie di terzi. Conforme **AGID** + **GDPR** senza consent banner aggiuntivo.
- **Web Share API** (`navigator.share()`) per "Altre app": apre il selettore di app dell'OS, auto-nascosto via JS se l'API manca (desktop).
- **Clipboard API** (`navigator.clipboard.writeText()`) per "Copia link", fallback `document.execCommand('copy')`. Feedback: classe `.copied` + icona check + aria-label "Link copiato negli appunti" per 2s.

**Bottoni in ordine** (HTML in `page-tools.html`): WhatsApp (`bi-whatsapp`, hover `#25d366`), Telegram (`bi-telegram`, `#229ed9`), Facebook (`bi-facebook`, `#1877f2`), X (`bi-twitter-x`, `#000`), LinkedIn (`bi-linkedin`, `#0a66c2`), Email (`bi-envelope`, `mailto:?subject=...&body=...`), Copia link (`bi-link-45deg`, Clipboard API + feedback verde), Condividi nativo (`bi-three-dots`, Web Share API mobile, auto-nascosto su desktop).

**Accessibilità:** `aria-label` descrittivo + testo `.visually-hidden` accanto all'icona per ogni bottone (screen reader leggono entrambi); `target="_blank" rel="noopener noreferrer"` sui link esterni; focus outline `#ffbe2e` 3px; `prefers-reduced-motion` disattiva l'hover lift `translateY(-2px)`.

**Stampa:** la riga share è nascosta automaticamente da `@media print` (sia globale sia locale per ridondanza).

**Mobile:** bottoni rimpiccioliti a 36px e label "Condividi:" su riga propria. Il bottone "Condividi nativo" è particolarmente utile su mobile.

CSS scoped sezione **SHARE BUTTONS v1.0** in `custom.css`. JS in `static/js/share.js` (caricato `defer` da `baseof.html`). Quando si modifica la lista delle piattaforme, aggiornare entrambi i blocchi (HTML + CSS hover colors).

## Striscia pittogrammi (`.kit-pittogrammi-row`)

Riga visiva di pittogrammi inline ARASAAC per dare un colpo d'occhio immediato a una pagina lista (es. `/rischi-prevenzione/kit-emergenza/`). Layout flex centrato, gap responsive, sfondo azzurrino istituzionale.

```html
<div class="kit-pittogrammi-row" role="img" aria-label="Componenti essenziali del kit di emergenza: zaino, acqua, cibo, torcia, radio, medicine, documenti, fischietto">
{{< pittogramma src="/pittogrammi/arasaac/zaino.png" alt="Zaino" size="small" inline="true" >}}
{{< pittogramma src="/pittogrammi/arasaac/acqua.png" alt="Acqua" size="small" inline="true" >}}
{{< pittogramma src="/pittogrammi/arasaac/cibo.png" alt="Cibo" size="small" inline="true" >}}
{{< pittogramma src="/pittogrammi/arasaac/torcia.png" alt="Torcia" size="small" inline="true" >}}
</div>
```

Regole:
- **`role="img"` + `aria-label` complessivo** sul wrapper: gli screen reader leggono la striscia come **una sola immagine descrittiva** invece di leggere ogni `alt` singolo. WCAG 1.1.1 conforme.
- Pittogrammi all'interno con `size="small"` (48px) e `inline="true"` per evitare il layout `<figure>` block default.
- Su mobile (≤576px) gap ridotto + padding ridotto.
- In stampa lo sfondo diventa bianco e il bordo nero, `page-break-inside: avoid`.

CSS scoped sezione **STRISCIA PITTOGRAMMI v1.0** in `custom.css`.

## Modal SOS-112 esteso (`partials/sos-112.html`)

Vedi `CLAUDE.md` sezione "Modal SOS-112" per la sintesi. Il modal di conferma chiamata 112 ha **3 azioni**: Annulla (focus iniziale, ENTER sicuro), "Cosa devo fare?" (link a `/assistente/`, bottone outline blu istituzionale), "Sì, chiama il 112" (bottone rosso primario, `<a href="tel:112">`).

Note operative:
- L'href dell'assistente passa per `{{ "assistente/" | relURL }}` per compatibilità Aruba/GitHub Pages.
- Il focus trap JS rileva tutti i `[href]` e bottoni: il nuovo `<a id="sos-modal-guide">` viene incluso automaticamente nel ciclo Tab/Shift+Tab.
- CSS scoped: `.sos-modal-btn-guide` (outline blu) + `.sos-modal-alt` (nota informativa azzurra prima dei bottoni). Sezione esistente del modal in `custom.css`.

Se un domani serve aggiungere una **quarta azione** (ipotesi: "Numeri utili"), aggiungere prima del bottone "Cosa devo fare?" — non distruggere l'ordine: sequenza visiva column-reverse su mobile (Call → Cosa fare → Annulla dall'alto al basso) e row su desktop (Annulla → Cosa fare → Call da sinistra a destra), che è la gerarchia di azione corretta.

## Shortcode `pagina-emergenza-lite` (pagina `/emergenza/`)

Rende la pagina `/emergenza/` **ultra-leggera** (44 KB vs 64 KB homepage). Legge `data/allerta.json` + `data/emergenza.json` al build. Zero widget esterni, CSS inline ~3KB, niente Bootstrap né JS. Usato solo da `content/emergenza/_index.md`.

**Contenuto in ordine di priorità:** (1) banner emergenza dinamico (se attiva), (2) 112 grande con `tel:112`, (3) stato allerta meteo colorato (build), (4) 4 numeri essenziali, (5) 6 azioni "cosa fare ora", (6) 7 link rapidi al sito.

Aliases: `/lite/`, `/emergenza-essenziale/`. Linkata dal footer. Caso d'uso: rete satura/lenta in emergenza, dispositivi vecchi, mobile.

## Partial `leggi-ad-alta-voce` (TTS Web Speech API)

Vedi regola `03-accessibility.md` sezione TTS per dettagli. Sintesi: opt-in via frontmatter `tts: true`, attivo su 12 pagine essenziali, voce italiana di default, fallback graceful, accessibile da tastiera. Componente in `partials/leggi-ad-alta-voce.html`, CSS in `custom.css` sezione **TTS v1.0**.

## Partial `article-cover` (copertina con didascalia credit)

Le copertine degli articoli sono renderizzate dal partial `themes/flavour-pcgenzano/layouts/partials/article-cover.html`, chiamato da `_default/single.html` per `content/comunicazioni/*.md`.

Comportamento del partial:
- Se `.Params.image` presente: produce un `<figure>` con `<img>` e (opzionale) `<figcaption>`.
- Se `.Params.image` assente: fallback su `images/notizia-default.svg` (no caption, `aria-hidden="true"`).
- Se `.Params.image_credit` o `.Params.image_source_url` presenti: aggiunge la `<figcaption class="article-cover-credit">` con icona camera, testo credit e link "Fonte originale" (target=_blank, rel=noopener, aria-label esplicito).

Stile in `custom.css` sezione **ARTICLE COVER v1.0**: testo piccolo (0.82rem), italic, allineato a destra, link blu istituzionale. Su mobile: text-align left, font 0.78rem. In stampa: colori convertiti in nero, link che si espande con URL completo (per la riproducibilità del documento stampato).

**Quando si popola `image_credit`**: solo casi storici (il marker `# TODO-foto-wikipedia` che lo popolava è bandito dal 3 maggio 2026, CLAUDE.md punto 9 — le foto da fonti ufficiali vanno inline come `{{< foto >}}` con caption autore+licenza, NON nel banner). La cover tipografica di `auto-cover-mancanti.py` non lo popola (è opera nostra).

Esempio frontmatter completo:
```yaml
image: "/images/2026-11-23-irpinia-1980.webp"
image_alt: "ShakeMap del terremoto dell'Irpinia 1980"
image_credit: "USGS — Public domain — via Wikimedia Commons"
image_source_url: "https://commons.wikimedia.org/wiki/File:USGS_..."
```

Compatibilità retroattiva: gli articoli pre-esistenti senza `image_credit` continuano a funzionare normalmente (il `<figcaption>` non viene reso).

## Articoli prev/next + correlati (partials)

Due partial standardizzati che `_default/single.html` chiama automaticamente per ogni articolo della sezione `/comunicazioni/`:

1. **`partials/articolo-navigazione.html`** — riga «Articolo più recente / Articolo precedente» basata su `.PrevInSection` / `.NextInSection`. Niente parametri: si attiva su qualsiasi pagina `.IsPage` con un `.Section` >= 2 articoli. Riusabile su nuove sezioni archivio future.

2. **`partials/articoli-correlati.html`** — sezione «Leggi anche» con card di articoli con stesso `badge` dell'articolo corrente, ordinate per data decrescente. Esclude l'articolo corrente, le versioni facili e i contenuti d'archivio (`archiviato: true`). Mostra immagine cover + data + titolo + descrizione.

## Partial `banner-archiviato` (contenuti d'archivio, dal 30/08/2026)

`partials/banner-archiviato.html`, incluso da `_default/single.html` prima del toggle versione facile: sugli articoli con **`archiviato: true`** nel frontmatter mostra un alert sobrio *"Contenuto d'archivio"* che chiarisce al lettore che l'articolo si riferisce a un evento o avviso concluso e resta online per documentazione (link alle ultime comunicazioni). Il flag `archiviato` era già usato dagli script di freschezza (`check-freshness.py`, rule 10); da questa data ha anche resa visiva ed esclude l'articolo dai correlati. Si usa per **annunci di servizio scaduti** (eventi conclusi, corsi chiusi, avvisi superati), **mai** per i resoconti di attività/interventi del Gruppo, che sono memoria storica e restano articoli normali. Alert Bootstrap Italia standard, nessuna CSS dedicata.

CSS in `custom.css` (sezioni "ARTICOLO PREV/NEXT v1.0" e "ARTICOLI CORRELATI v1.0"):
- Hover lift `translateY(-2px)`, ombra blu istituzionale
- Focus visibile `outline: 3px solid #ffbe2e` (WCAG 2.4.7)
- Nascosti in stampa via `@media print`

Quando aggiungi una nuova sezione paginata (es. `/news-tecniche/`), nel suo `single.html` (o aggiornando la condizione in `_default/single.html`) basta chiamare i 2 partial — funzionano automaticamente.

## Assistente guidato (`/assistente/`)

Pagina interattiva che guida il cittadino con domande semplici fino a una risposta di autoprotezione. È un **albero decisionale deterministico in JavaScript puro** (nessun LLM, nessuna API runtime), coerente con il vincolo di sito statico Hugo e con la responsabilità istituzionale di non dare indicazioni generate in emergenza.

- **Contenuto**: `content/assistente/_index.md` (solo frontmatter — `type: "assistente"`, `layout: "list"`).
- **Logica/dati**: `themes/flavour-pcgenzano/layouts/assistente/list.html`. Oggetto `NODES` (~30 nodi: terremoto, incendio, gas, allerta meteo, allagamento, volontario, numeri utili, IT-alert). Nodo: `{ kind: 'question'|'answer', title, prompt?, options?, body?, bullets?, emergency?, links? }`.
- **Subpath**: link interni via `window.SITO_BASEURL` (`{{ "" | relURL }}`) per Aruba + GitHub Pages.
- **Accessibilità**: `aria-live="polite"`, focus sul `<h2>` ad ogni render, tastiera nativa, banner rosso 112, fallback `<noscript>`.
- **Deep link**: stato in `location.hash` (es. `/assistente/#terremoto_casa`). **Homepage**: card "Cosa devo fare?" in `data/quick_links.yaml` → `servizi[0]`.

**Per aggiungere un nuovo percorso**: aggiungere un nodo `question` collegato da `start.options`, poi le relative `answer` referenziate da `options[n].next`. Rispettare il criterio `emergency: true` solo per situazioni operative reali (coerenza con regola `06-protezione-civile-scientifica.md` sul tono di comunicazione del rischio). Ogni nodo `answer` può avere un `pittogramma` opzionale (es. `'arasaac/terremoto.png'`) renderizzato come `<figure>` accessibile sopra il corpo della risposta.

## Partial `structured-data` (JSON-LD Schema.org)

`themes/flavour-pcgenzano/layouts/partials/structured-data.html` inietta il blocco `<script type="application/ld+json">` con i dati strutturati Schema.org per i motori di ricerca e gli assistenti vocali.

**Schema attivi:** Organization+NGO, ContactPoint, WebSite (con SearchAction), BreadcrumbList, Article (per `/comunicazioni/`), Event (aggiuntivo per `badge: Evento` con location Place + organizer), FAQPage (per `/faq/` **e** per qualunque pagina con frontmatter `faq_schema: true`, vedi sotto), HowTo (per pagine `/rischi-prevenzione/*` con frontmatter `howto_prima` / `howto_durante` / `howto_dopo` — vedi sotto), WebPage (default), Question/Answer, HowToStep, ImageObject, PostalAddress, GeoCoordinates, City.

**HowTo per pagine rischio — 8 pagine già coperte.** Da maggio 2026 le 8 pagine `/rischi-prevenzione/*` con struttura PRIMA/DURANTE/DOPO sono **tutte** coperte da `HowTo` (`rischio-sismico`, `rischio-idrogeologico`, `rischio-incendio`, `rischio-vulcanico`, `ondate-di-calore`, `blackout`, `vento-forte`, `temporali-intensi`). Per nuove pagine rischio, il blocco HowTo si attiva con 3 campi frontmatter:

```yaml
howto_prima: "Riassunto in 1-3 frasi delle azioni preventive da fare prima dell'evento."
howto_durante: "Riassunto in 1-3 frasi delle azioni immediate da fare durante l'evento."
howto_dopo: "Riassunto in 1-3 frasi delle azioni di recupero da fare dopo l'evento."
```

Il partial controlla `if and .Params.howto_prima .Params.howto_durante .Params.howto_dopo` — il blocco HowTo viene emesso **solo** se tutti e tre i campi sono presenti. Pagine senza i campi continuano ad avere solo `WebPage` + `BreadcrumbList` (nessuna regressione).

**`totalTime`** calcolato come `ReadingTime × 1.5` minuti (lettura → applicazione pratica), minimo 5 minuti. **`url` di ciascun HowToStep** punta al frammento `#cosa-fare-prima` / `#cosa-fare-durante` / `#cosa-fare-dopo` della pagina, ancore presenti su tutte le pagine rischio per la struttura uniforme già documentata in `rule 06-protezione-civile-scientifica.md`.

⚠️ **Sintassi obbligatoria `| jsonify | safeJS`** per ogni campo testuale dentro `<script type="application/ld+json">`. Hugo applica un **secondo escape JS contestuale** alle stringhe dentro `<script>`, e il solo `| jsonify` produce doppio escape (es. `name: "\"Foo\""`). Aggiungere `| safeJS` dopo `| jsonify` impedisce il secondo escape e produce JSON valido. Vale anche per gli apostrofi italiani (es. "L'unica difesa"). Testato con `validator.schema.org` post-fix del 12 maggio 2026.

**FAQPage opt-in dagli accordion (oltre a `/faq/`).** Pagine con accordion `<details class="faq-item">` espongono **FAQPage** aggiungendo `faq_schema: true`: il partial estrae con `findRESubmatch` domanda (`<summary>`) + risposta e genera JSON-LD (`| plainify | htmlUnescape | jsonify | safeJS`). **Opt-in** apposta, per non marcare come FAQ accordion di altri contenuti (es. moduli corso). Attivo su `/allerte-meteo/` e `/area-volontari/`; `/faq/` ha la sua lista curata a mano.

**Importante — vincolo di tipo Organization:** marcata `["Organization", "NGO"]`, **NON** `GovernmentOrganization` né `EmergencyService`. Il Gruppo è OdV, non ente pubblico né servizio chiamabile: quei tipi indurrebbero Google/assistenti vocali a presentarlo come servizio chiamabile, contro la regola "in emergenza chiama il 112". Quando estendi gli schema, evita tipi che confondano OdV con ente pubblico/servizio di emergenza; verifica con [Google Rich Results Test](https://search.google.com/test/rich-results) e [Schema.org validator](https://validator.schema.org/).

## Partial `jsonld-copyright` + script `copy-attribution.js` (tutela proprietà intellettuale, agosto 2026)

Due componenti che riflettono e rafforzano la licenza dichiarata in `/note-legali/` (**CC BY 4.0**, "salvo diversa indicazione"):

- **`partials/jsonld-copyright.html`** (incluso da `baseof.html` subito dopo `structured-data.html`) — emette su **ogni pagina** un blocco JSON-LD di **paternità e licenza** (il ramo `Article` include anche **`speakable`** — SpeakableSpecification su `h1` + primo paragrafo — per gli assistenti vocali): `Article` per le pagine con data reale (comunicazioni, capitoli del manuale, dossier), `WebPage` per le pagine statiche/di sezione e la homepage. Campi: `headline`, `url` (produzione), `datePublished`/`dateModified` (omessi se assenti), `author` + `copyrightHolder` (Organization "Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma"), `license` (default CC BY 4.0), `inLanguage` (`it-IT`, oppure il `language:` del frontmatter per le pagine tradotte). **Override per pagina** dal frontmatter: `license: "https://..."` sostituisce la licenza; `license: none` omette il campo (il "salvo diversa indicazione"). 🔴 **Fonte unica dell'entità di pagina**: i vecchi blocchi `Article` (comunicazioni) e `WebPage` generico di `structured-data.html` sono stati ritirati per non duplicare le entità agli occhi dei validatori — là restano Organization/NGO, WebSite, Event, FAQPage, HowTo e BreadcrumbList. Non reintrodurli. Sintassi `| jsonify | safeJS` obbligatoria per i campi testuali (stessa regola di structured-data).
- **`static/js/copy-attribution.js`** (tema, caricato `defer` da `baseof.html`) — quando l'utente **copia più di 120 caratteri** di testo dalla pagina, appende alla clipboard (versione `text/plain`) il blocco fonte: em dash, "Fonte: Gruppo Comunale…", URL della pagina senza query string + "licenza CC BY 4.0 (attribuzione obbligatoria)". Preserva la versione `text/html` della selezione (fonte come `<p>` finale con link) per chi incolla in editor rich text. **Non si attiva** dentro `input`, `textarea`, `contenteditable`, `pre`/`code` o elementi con `data-no-attribution`; qualunque errore → copia nativa intatta (mai bloccare la copia). I pulsanti "Copia link" (share.js, condividi-cartina.js) usano `navigator.clipboard.writeText`, che non passa dall'evento `copy`: continuano a copiare solo l'URL pulito (il fallback `execCommand` di share.js usa una textarea → esclusa comunque). Zero DOM, zero impatto screen reader. Anche le pagine HTML statiche fuori da Hugo **che caricano `site-chrome.js`** (giochi, quizpc, formazionepc, abili-a-proteggere, hub/cataloghi delle schede) lo ricevono via `injectCopyAttribution()` (guardia idempotente `script[data-copy-attribution]`, stesso pattern della toolbar a11y). Le **singole schede A4 stampabili** non caricano JS per design (documenti da stampare, già CC BY-NC-SA con attribuzione in banda stampa): restano escluse. Lo script legge la **licenza effettiva della pagina dal JSON-LD** di `jsonld-copyright.html` (rispetta `license:` custom e `license: none` → nessuna attribuzione) e, se la selezione HTML include pittogrammi ARASAAC, dichiara per quelli la licenza corretta CC BY-NC-SA 4.0 con link a `/attribuzioni-pittogrammi/`.

## Partial `speculation-rules` + OpenSearch + TDMRep (agosto 2026)

- **`partials/speculation-rules.html`** — blocco `<script type="speculationrules">` incluso da `baseof.html` **solo su `.IsHome`**: prefetch delle 4 pagine critiche di emergenza (cosa-fare-adesso, numeri-utili, emergenza, allerte-meteo). Progressive enhancement puro (browser senza supporto lo ignorano); **solo prefetch, mai prerender**. URL via `relURL | jsonify | safeJS` (subpath GitHub Pages).
- **`static/opensearch.xml`** — descrittore OpenSearch della ricerca interna (template `/cerca/?q={searchTerms}`), dichiarato in `baseof.html` con `<link rel="search">`. La pagina `/cerca/` (`layouts/cerca/list.html`) legge `?q=` e lancia `ui.triggerSearch(q)` — stesso flusso usato dal form della pagina 404.
- **`partials/preconnect-dati.html`** — `<link rel="preconnect" crossorigin>` verso gli host dei fetch dati, **scoped per sezione** (`cruscotto`: INGV FDSN, Open-Meteo forecast/marine/air, MeteoHub, radar DPC; `laboratorio-meteo`: Open-Meteo archive). Incluso da `baseof.html`. 🔴 Gli host devono restare un sottoinsieme della `connect-src` della CSP (rule 05); mai site-wide (ogni preconnect apre una connessione reale).
- **`static/.well-known/tdmrep.json`** — TDM Reservation Protocol (W3C / Direttiva UE 2019/790 art. 4): **riserva con licenza offerta**: `tdm-reservation: 1` riserva i diritti di text and data mining e `tdm-policy` indica le condizioni alle quali è consentito, cioè `/note-legali/` (CC BY 4.0, attribuzione). Non è un'assenza di riserva: quella si dichiara col valore 0 (audit 25/09/2026, F30). Speculare agli header `TDM-Reservation`/`TDM-Policy` in `.htaccess` (rule 05).

## Partial `meta-social` (Open Graph + Twitter Card)

Tutti i meta tag che controllano l'**anteprima** dei link quando vengono condivisi su WhatsApp, Telegram, Facebook, X, LinkedIn, Slack, ecc. sono in `themes/flavour-pcgenzano/layouts/partials/meta-social.html` (chiamato da `baseof.html`). Include:

- **Open Graph base**: `og:title`, `og:description`, `og:type` (`article` per `.IsPage`, `website` altrove), `og:url`, `og:locale=it_IT`, `og:site_name`.
- **OG image**: `og:image`, `og:image:secure_url`, `og:image:type` (da estensione: `.webp`/`.png`/`.svg`/`.gif`/default `.jpg`), `og:image:width=1200`, `og:image:height=630`, `og:image:alt` (da `image_alt` o titolo).
- **Article** (solo `.IsPage`): `article:published_time`/`:modified_time` (ISO 8601), `:author`, `:section` (dal badge), `:tag` (sui tags).
- **Twitter Card**: `twitter:card=summary_large_image`, `:title`, `:description`, `:image`, `:image:alt`. Opzionale `twitter:site` se in `[params] twitterSite` di `hugo.toml`.

Default senza copertina: `static/images/og-default.png` 1200×630 nel tema.

**Cache delle anteprime**: le piattaforme social cachano le anteprime (Facebook/X possono cachare per ore o giorni). Se modifichi la copertina di un articolo, l'anteprima si aggiorna **solo dopo che la piattaforma ricontrolla**. Per forzare il refresh: [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/) e [Twitter Card Validator](https://cards-dev.twitter.com/validator).

## Partial della roadmap (maggio 2026)

Partial aggiunti con le iniziative della roadmap. Tutti auto-protettivi (renderizzano solo quando hanno senso) e inclusi dai template `_default`.

- **`qr-articolo.html`** (idea #6) — bottone "Scarica QR" + `<dialog>` con il QR dell'articolo. Si attiva solo se esiste `static/qr/<slug>.png|svg` (generati da `scripts/genera-qr-articoli.py`). Incluso in `page-tools.html`. CSS § QR ARTICOLO v1.0.
- **`ricerca-modal.html`** (idea #24) — modal di ricerca full-text Pagefind, apertura da icona navbar e da `Ctrl+K`. `pagefind-ui` caricato in lazy alla prima apertura. Incluso in `baseof.html`. Indice generato in CI da `deploy.yml` (`npx pagefind --site public`, artefatto di build MAI committato — dal 15/07/2026 `static/pagefind/` è in `.gitignore`); in locale `scripts/genera-indice-ricerca.sh` per provare la ricerca con `hugo server`. CSS § RICERCA PAGEFIND v1.0. La pagina `/cerca/` (`layouts/cerca/list.html`) usa lo stesso motore.

  🔴 **Pagine statiche e `data-pagefind-body` (13/09/2026).** `baseof.html` marca il `<main>` con `data-pagefind-body`; per Pagefind quel marcatore è **esclusivo**: se anche una sola pagina lo porta, vengono indicizzate **solo** le pagine che lo hanno. Le pagine HTML autonome di `static/` — schede stampabili, giochi, kit calamità, storie, quizpc, formazionepc, abili-a-proteggere — non lo hanno mai avuto e quindi **non sono mai comparse nella ricerca** (né in `/cerca/` né in Ctrl+K), pur essendo online e linkate: 625 pagine su 1.525 erano fuori dall'indice. Dal 13/09/2026 lo step `scripts/prepara-statiche-per-pagefind.py` gira in `deploy.yml` **prima** di ciascuno dei due `npx pagefind`, aggiunge il marcatore al `<body>` di quelle pagine **in `public/`** (i sorgenti in `static/` non si toccano, così una scheda nuova è indicizzata senza che nessuno se ne ricordi) e marca `data-pagefind-ignore` sulle barre di servizio (`.no-print`, `.scheda-toolbar`, `.storia-toolbar`) perché non finiscano negli estratti. Lo stesso passaggio è nello script locale `scripts/genera-indice-ricerca.sh`. **Se aggiungi una famiglia nuova di pagine statiche, aggiungila a `SCAN_DIRS`** in quello script e in `aggiungi-pagine-statiche-al-cerca.py` (che alimenta `index.json`), altrimenti resta invisibile alla ricerca.
- **`lis-badge.html`** (idea #10) — badge "Disponibile in LIS". **Due modalità** (v2.0): (1) **preferita `lis_section: "<famiglia>"`** → badge *"N video LIS disponibili"* che linka a `/lis/#<famiglia>`; usa il registro `data/lis.yaml` v2.0 (59 video LIS di "Io non rischio"/DPC + "Abili a Proteggere"/Europe Consulting in 10 famiglie); privacy-first (niente embed YouTube). Incluso in `_default/single.html`, `_default/list.html`, `rischi-prevenzione/single.html`. Famiglie: `rischio-{sismico,vulcanico,idrogeologico,incendio}`, `maremoto`, `allerte-meteo`, `gestione-emergenza`, `pianificazione`, `aree-emergenza`, `kit-emergenza`. (2) **legacy `lis_video: "<id>"`** → dialog popup video self-hosted/YouTube + trascrizione (retrocompat). CSS § LIS v2.0. **Aggiornamento**: workflow `check-video-lis.yml` (lun 11:23 UTC, `scripts/check-nuovi-video-lis.py`) apre issue sui nuovi video LIS con famiglia suggerita.

Layout di pagina della roadmap (`layouts/<sezione>/`): `stato-sistema/list.html` (#25), `storia/list.html` (#8), `lis/list.html` (#10), `lanterna/list.html` (#4, standalone — NON usa `baseof.html`), `quiz-preparazione/list.html` (#7), `podcast/{list,single,rss.xml}` (#22), `articoli-da-ascoltare/list.html` (#22, ex `podcast/`), `allerta-stato/list.json` (#2, endpoint JSON). Script: `genera-qr-articoli.py`, `genera-indice-ricerca.sh`, `backup-documenti-aruba.py`. JS: `notifiche-allerta.js` (#2), `glossario-pagina.js` (#21), `quiz-preparazione.js` (#7), `static/giochi/assets/js/arena.js` (#11).

## Dossier interattivi — sezione `/dossier/` + 9 shortcode `dossier-*`

I **dossier interattivi** (`content/dossier/`, URL `/dossier/`) sono racconti visivi *scrollytelling* a tema scuro "spazio", **full-bleed** e accessibili (WCAG 2.2 AA). Sono un **"motore" riusabile**: l'impianto è scritto una volta, **ogni nuovo dossier è un singolo file Markdown** in `content/dossier/<slug>.md`. Guida operativa completa: `manuale/parte-39-dossier-interattivi.md`.

**Architettura:** layout `layouts/dossier/single.html` (definisce `main`, carica `static/css/dossier.css`, rende barra di avanzamento + pallini dai `sezioni` del frontmatter + `{{ .Content }}` + sezione condivisione, poi `static/js/dossier.js`); landing `layouts/dossier/list.html` (griglia card, CSS `static/css/dossier-list.css`); box homepage `partials/dossier-home.html` (dossier più recente, CSS `static/css/dossier-home.css`, inserito in `index.html` modalità normale fra `cruscotto-home` e `services`). Il full-bleed si ottiene con `main:has(> .dossier){padding:0}` in `dossier.css`.

**I 9 shortcode** (`layouts/shortcodes/dossier-*.html`):

- `dossier-hero` — apertura a tutto schermo (`id`, `image`, `alt`, `eyebrow`, `title` con `<br>`, `sub`, `credito`).
- `dossier-scena` — sezione con sfondo immagine + pannello in vetro; `align="left|right|top"` (con `top` immagine grande centrata); `id`/`image`/`alt`/`kicker`/`title`/`credito` + corpo Markdown. Il pannello ha classe `reveal` (comparsa al viewport).
- `dossier-dati` + `dossier-dato` — numeri che si animano (count-up). `dossier-dato`: `to`/`unita`/`label`, oppure `da="ANNO"` per anni **dinamici** (`{{ sub now.Year (int ...) }}`) — evita dati che invecchiano.
- `dossier-confronto` — slider prima/dopo (due immagini, cursore trascinabile, tastiera): `titolo`/`testo`/`base`/`baseAlt`/`baseLab`/`top`/`topAlt`/`topLab`/`ratio`/`cap`.
- `dossier-hotspot` + `dossier-punto` — immagine grande con punti cliccabili (popover). `dossier-punto`: `x`/`y` (% sull'immagine) + `titolo` + corpo Markdown. I popover si **capovolgono** da soli (alto/basso/sinistra/destra, logica in `dossier.js`) per non uscire dallo schermo; i punti compaiono "a cascata" quando l'immagine entra (`.dossier-hotspot.is-revealed`).
- `dossier-chiusura` — finale con titolo + testo + fino a 2 CTA (`cta1`/`cta1url`, `cta2`/`cta2url`).
- `dossier-fonti` — crediti/fonti (Markdown).

🔴 **Subpath GitHub Pages:** ogni immagine passa per `strings.TrimPrefix "/" | relURL` (vale per gli shortcode, per `dossier-home.html` e per `dossier/list.html`). Non usare `relURL` su path con leading slash: romperebbe su GitHub Pages.

🔴 **Animazioni:** sono molte (Ken Burns, parallasse, ingresso direzionale dei pannelli, cascata dei punti hotspot, cielo stellato + nebulosa dietro le sezioni scure, stelle cadenti, anelli orbitanti, riflesso sui numeri, micro-interazioni). **Tutte** disattivate da `@media (prefers-reduced-motion: reduce)` **e** da `html.a11y-pause-anim` (toggle "Pausa animazioni" del toolbar). Il dossier resta leggibile e usabile senza animazioni (popover da tastiera Invio/Spazio/Esc, slider `input[type=range]` nativo). Sezioni CSS: `dossier.css` v1.0→v1.3.

🔴 **Immagini:** solo con **licenza chiara** (NASA pubblico dominio, Copernicus/ESA CC BY, autori con CC) e **credito onesto** in `credito`/`cap`/`fonti`. Mai attribuire un'immagine al satellite sbagliato né spacciarla per un'altra. Asset in `static/images/dossier/` (WebP).

**Frontmatter di un dossier:** `type: "dossier"`, `title`, `description`, `image` (cover per social/landing), `tts: false`, `indice: false`, `sezioni: [{ id, label }, ...]` (un punto per `id` di sezione, per la navigazione a pallini). **Menu:** voce "Dossier interattivi" → `/dossier/` sotto **Risorse** in `hugo.toml` **e** `static/app-shared/site-chrome.js` (tenere sincronizzati).
