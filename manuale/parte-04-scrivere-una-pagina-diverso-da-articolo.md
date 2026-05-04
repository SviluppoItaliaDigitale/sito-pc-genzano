_[Indice manuale](README.md)_

# Parte 4 — Scrivere una pagina (diverso da articolo)

Una **pagina** è un contenuto permanente (es. "Chi siamo", "Piano di Emergenza", "Numeri
utili"). Non ha data di pubblicazione, non va in home tra le notizie, non ha badge.

### 4.1 — Quando creare una pagina invece di un articolo

Crea una **pagina** se:

- Il contenuto è **permanente** o rivisto periodicamente (non "notizia").
- Deve essere **linkabile dalla navbar** o dal footer.
- Serve come **riferimento** (numeri utili, procedure, contatti).

Crea un **articolo** se:

- Il contenuto è **datato** (riferito a un evento, una scadenza, un'occorrenza).
- Va in **cronologia** (Comunicazioni).

### 4.2 — Struttura delle cartelle per le pagine

```
content/
├── chi-siamo/
│   └── _index.md          ← pagina /chi-siamo/
├── numeri-utili/
│   └── _index.md          ← pagina /numeri-utili/
├── rischi-prevenzione/
│   ├── _index.md          ← pagina hub /rischi-prevenzione/
│   ├── rischio-sismico.md ← sotto-pagina /rischi-prevenzione/rischio-sismico/
│   └── rischio-idrogeologico.md
└── comunicazioni/         ← articoli, vedi Parte 1
```

**Regole:**

- Pagina principale di una sezione: cartella con `_index.md`.
- Sotto-pagina semplice: file `.md` nella cartella del genitore.
- Nome cartella = slug URL: `chi-siamo` → `/chi-siamo/`.

### 4.3 — Frontmatter della pagina

```yaml
---
title: "Titolo della pagina"
description: "Sommario per SEO (max 160 caratteri)."
layout: "single"      # opzionale: forza un layout specifico
aliases:              # opzionale: redirect da URL vecchi
  - /vecchia-url.html
draft: false
---
```

**Differenze dall'articolo:**

- **No** `date` (o, se c'è, non viene mostrata).
- **No** `badge`, `priorita`, `scadenza`, `area`, `allegati` (salvo uso speciale).
- **Sì** `aliases` per gestire redirect da URL storici.
- **Sì** `layout` se serve un layout non-default (raramente).

### 4.4 — Aggiungere la pagina al menu principale

Il menu principale è organizzato come **mega-menu** (Opzione A) in `hugo.toml`: **Voci di primo livello**, di cui 4 dropdown. La struttura è documentata in dettaglio in `.claude/rules/04b-hugo-template-css.md` ma per l'uso quotidiano basta sapere questo.

**Struttura attuale:**

| Voce | Tipo | Contenuto |
|---|---|---|
| Home | diretta | `/` |
| Per il Cittadino ▾ | dropdown | Cosa Fare Adesso, Allerte Meteo, Rischi e Prevenzione, Cartografia, Numeri Utili, Piano Familiare, Kit pronti per situazioni vulnerabili |
| Per le scuole ▾ | dropdown | Kit per le scuole, Percorsi didattici pronti, Schede didattiche stampabili, Per i docenti — Ed. Civica, Storie e Racconti, Giochi della Sicurezza |
| Accessibilità e Supporti ▾ | dropdown | Abili a Proteggere, Facile da Leggere |
| Volontariato ▾ | dropdown | Diventa Volontario, Chi Siamo |
| Risorse ▾ | dropdown | FAQ, Strumenti in Tempo Reale, Area Download, Normativa, Glossario, Mappa del Sito |
| Comunicazioni | diretta | `/comunicazioni/` |
| Contatti | diretta | `/contatti/` |

**Per aggiungere una voce a un dropdown esistente** (caso più comune):

```toml
[[menus.main]]
  name = "Nuova Voce"
  url = "/nuova-voce/"
  parent = "per-il-cittadino"   # oppure: formazione, volontariato
  weight = 7                    # ordine all'interno del dropdown
```

**Per aggiungere una voce diretta di primo livello** (raro: solo se è un'azione fondamentale):

```toml
[[menus.main]]
  name = "Nome nel menu"
  url = "/url-pagina/"
  weight = 5                    # ordine fra le voci di primo livello
```

**Limite di sicurezza**: non superare 6-7 voci di primo livello per non rompere l'usabilità mobile.

**Pagine statiche (non Hugo)**: lo stesso menu è iniettato sulle 97 pagine HTML in `static/giochi/`, `static/quizpc/`, `static/formazionepc/`, `static/formazione/schede-stampabili/` tramite `static/app-shared/site-chrome.js`. Se modifichi `hugo.toml` e vuoi che il menu nuovo appaia anche lì, **aggiorna in parallelo `site-chrome.js`** (la struttura è la stessa, è una stringa JavaScript concatenata).

### 4.4.1 — Aggiungere l'indice della pagina (TOC)

Per pagine lunghe (oltre 8-10 H2 o oltre ~500 righe Markdown) aggiungi nel frontmatter:

```yaml
toc: true
```

Hugo genera automaticamente un indice cliccabile con badge numerati `01`, `02`, `03`… che porta alle sezioni `##` e `###`. Il bottone "Torna in cima" si trasforma in "Torna all'indice".

Il TOC funziona sia su `single.html` che su `list.html` (sezioni con `_index.md`). Pagine attualmente con TOC: tutte le 26 elencate in `04b-hugo-template-css.md` (Formazione + kit, Glossario, Piani, 9 sotto-rischi, Normativa + 7 Capi).

Non attivare `toc: true` su pagine con meno di 4 H2: l'indice diventa visivamente sproporzionato.

### 4.4.2 — Bottone "Facile da leggere" e slim-header

Lo slim-header in alto a destra contiene un **bottone giallo "Facile da leggere"** che porta a `/facile-da-leggere/` (versione semplificata del sito per persone con difficoltà di lettura). È visibile su ogni pagina, sia Hugo che statica. Il colore giallo (`#ffd60a` su blu `#003366`) è scelto per essere immediatamente riconoscibile come supporto accessibilità — non modificarlo senza valutare l'impatto WCAG.

Sotto il bottone "Area Volontari" sono presenti i social. Il navbar-brand "Comune di Genzano di Roma" a sinistra è stato rimosso (era duplicato dalla prima voce della link-list); il riferimento al Comune resta nella link-list di enti istituzionali (Comune, DPC, Regione Lazio).

Se la pagina deve apparire nel **footer**, usa `[[menus.footer]]` invece di `[[menus.main]]`.

### 4.5 — Esempio completo: creare una pagina

Voglio creare una pagina `/mezzi/` che elenca i mezzi operativi del gruppo.

**Passi:**

1. Crea cartella e file:

   ```bash
   mkdir content/mezzi
   touch content/mezzi/_index.md
   ```

2. Compila il frontmatter e il corpo:

   ```markdown
   ---
   title: "I nostri mezzi operativi"
   description: "Elenco dei mezzi in dotazione al Gruppo Comunale Volontari: furgoni, pick-up, moduli AIB."
   draft: false
   ---

   Il Gruppo dispone di sei mezzi operativi per le attività sul territorio.

   ## Mezzi di trasporto

   - **Furgone 9 posti** — Trasporto volontari alle esercitazioni e interventi.
   - **Pick-up 4x4** — Accesso a strade accidentate durante emergenze AIB.
   - **Auto di servizio** — Spostamenti di coordinamento.

   ## Moduli AIB

   - **Modulo AIB da 400 litri** — Antincendio boschivo, montato sul pick-up.
   - **Moduli manichette e lance** — Supporto ai Vigili del Fuoco.

   ## Radio comunicazioni

   Tutti i mezzi sono dotati di radio ricetrasmittenti VHF, collegati al ponte ripetitore
   del gruppo.
   ```

3. (Opzionale) Aggiungi la voce nel menu `hugo.toml`:

   ```toml
   [[menus.main]]
     name = "Mezzi"
     url = "/mezzi/"
     weight = 10
   ```

4. Test locale:

   ```bash
   hugo server
   # Apri http://localhost:1313/mezzi/
   ```

5. Commit e push:

   ```bash
   git add content/mezzi/ hugo.toml
   git commit -m "Nuova pagina: I nostri mezzi operativi"
   git push origin main
   ```

### 4.6 — Pagine legali e istituzionali: campo `dataUltimaRevisione`

Quattro pagine hanno un trattamento speciale perché devono mostrare al cittadino l'**ultima revisione esplicita** (non automatica da git):

| Pagina | File |
|---|---|
| Privacy e Cookie Policy | `content/privacy/_index.md` |
| Note Legali | `content/note-legali/_index.md` |
| Dichiarazione di Accessibilità | `content/accessibilita/_index.md` |
| Social Media Policy | `content/social-media-policy/_index.md` |

**Frontmatter obbligatorio** per queste pagine:

```yaml
---
title: "…"
description: "…"
layout: "single"
dataUltimaRevisione: "2026-04-22"   # AAAA-MM-GG
---
```

Il template `single.html` del tema mostra questa data come **box evidente** in cima al contenuto:

> 🕑 **Pagina rivista il martedì 22 aprile 2026.**

**Regole operative:**

- Aggiorna `dataUltimaRevisione` **ogni volta** che cambi contenuto sostanziale (non per refusi o link morti).
- **Non scrivere** date di revisione nel corpo del testo (tipo "Ultimo aggiornamento: Marzo 2026"): il riferimento è unico e vive nel frontmatter.
- Il workflow `audit-sito.yml` (sezione 32, lun 09:00 UTC) verifica ogni lunedì che le 4 pagine abbiano il campo impostato e in formato corretto.
- La `.Lastmod` automatica di Hugo (git-based) viene **omessa** sulle pagine che hanno `dataUltimaRevisione`: lo controlla il partial `page-tools.html`.

**Perché non usare la data automatica da git?** Le pagine legali cambiano raramente e la data di revisione ha valore giuridico-istituzionale: deve essere sotto controllo editoriale esplicito, non dipendere da un commit git che può riguardare anche modifiche minime (refusi, link aggiornati).

### 4.7 — Pagine esistenti sul sito

| URL | File | Note |
|---|---|---|
| `/` | `layouts/index.html` | Homepage dinamica (normale/emergenza) |
| `/chi-siamo/` | `content/chi-siamo/_index.md` | |
| `/rischi-prevenzione/` | `content/rischi-prevenzione/_index.md` | Hub + 9 sotto-pagine |
| `/allerte-meteo/` | `content/allerte-meteo/_index.md` | Widget Windy + Radar DPC (click-to-load) — vedi 4.9 |
| `/strumenti/` | `content/strumenti/_index.md` | **Hub strumenti consultazione in tempo reale** — vedi 4.10 |
| `/comunicazioni/` | Generata da Hugo | Elenco articoli |
| `/formazione/` | `content/formazione/_index.md` | Include kit scuola (vedi 4.8) |
| `/giochi/` | `static/giochi/index.html` | **Standalone**, non Hugo content |
| `/diventa-volontario/` | `content/diventa-volontario/_index.md` | |
| `/contatti/` | `content/contatti/_index.md` | |
| `/numeri-utili/` | `content/numeri-utili/_index.md` | |
| `/piano-emergenza/` | `content/piano-emergenza/_index.md` | |
| `/piano-familiare/` | `content/piano-familiare/_index.md` + JS | Compilabile client-side |
| `/cartografia/` | `content/cartografia/_index.md` | Cartografia operativa |
| `/cerca/` | `content/cerca/_index.md` | Ricerca interna |
| `/faq/` | `content/faq/_index.md` | Schema FAQ + JSON-LD |
| `/accessibilita/` | `content/accessibilita/_index.md` | Dichiarazione AGID |
| `/privacy/` | `content/privacy/_index.md` | |
| `/note-legali/` | `content/note-legali/_index.md` | |
| `/siti-utili/` | `content/siti-utili/_index.md` | |
| `/glossario/` | `content/glossario/_index.md` | Glossario PC: 50+ termini tecnici A-Z |
| `/strumenti/` | `content/strumenti/_index.md` | Hub strumenti consultazione (12+ widget/link) |
| `/mappa-sito/` | `content/mappa-sito/_index.md` | Mappa del sito con card per macro-aree |
| `/facile-da-leggere/` | `content/facile-da-leggere/_index.md` | Versione cognitiva-friendly (D.Lgs. 62/2024) |
| `/formazione/schede-stampabili/` | `static/formazione/schede-stampabili/` | schede HTML A4 stampabili (di cui 10 colorabili, 14 col curricolo a spirale 6-19 anni, case study delle maxi-emergenze italiane in 12 Primaria + 12 Sec I + 14 Sec II, e 4 rubriche valutative ed. civica) suddivise per fascia (infanzia/primaria/secondaria I/secondaria II) e disciplina (italiano, matematica, scienze, geografia, storia, ed. civica, giornalismo, diritto, economia, inglese) |
| `/formazione/storie-e-racconti/` | `static/formazione/storie-e-racconti/` | storie e racconti di qualità letteraria per bambini 3-11 anni (6 per fascia infanzia con Tina la Tartaruga + 6 per primaria 6-8 con Flavio/Flavia protagonisti e attimo decisivo + 6 per primaria 9-11 più letterarie). Ogni storia ha box "Cosa abbiamo imparato", domande per parlarne insieme e sezione "Per il/la docente" con obiettivi, competenze chiave europee, attività in classe e riferimenti curricolari (IN 2012, L. 92/2019, D.Lgs. 1/2018, DPC). |
| `/english/` ... `/esperanto/` | `content/{lingua}/_index.md` | 7 hub linguistiche curate (vedi §4.11) |

### 4.8 — Kit didattici per le scuole (`content/formazione/kit-scuola-*.md`)

Il sito pubblica **Kit didattici** indirizzati alle scuole del territorio, uno per fascia d'età. Dopo un ciclo di feedback positivi dei docenti, i kit sono stati ampliati (aprile 2026) per rispondere alla richiesta di **maggiore chiarezza e profondità** sui temi di protezione civile.

| File | Fascia | Righe | Contenuti chiave |
|---|---|---|---|
| `kit-scuola-infanzia.md` | 3-6 anni | ~410 | Campi di Esperienza, schede fotocopiabili dedicate (10 da colorare + attività), griglia di osservazione, percorso 4 × 30′ |
| `kit-scuola-primaria.md` | 6-11 anni | ~685 | Raccordo 9 discipline, schede fotocopiabili dedicate, esperimenti, uscita sul territorio, rubrica 5 competenze |
| `kit-scuola-secondaria-primo-grado.md` | 11-14 anni | ~690 | UdA interdisciplinare, schede fotocopiabili dedicate, compito di realtà sul Piano di evacuazione, 5 metodologie didattiche |
| `kit-scuola-secondaria-secondo-grado.md` | 14-19 anni | ~800 | PCTO 30-50h, schede fotocopiabili dedicate (15 curriculari + case study), 3 progetti di classe, temi per l'Esame di Stato, rubrica 7×livelli |

**Struttura comune a tutti e quattro i kit:**

1. **Riferimenti normativi e curricolari** — Legge 92/2019 (educazione civica), D.M. 35/2020 e Linee guida 2024, art. 18 D.Lgs. 1/2018 (obbligo di informazione e formazione), Indicazioni Nazionali 2012 / Nuovi Scenari 2018 / Nuovi Orientamenti 2024 (infanzia).
2. **Obiettivi di apprendimento formalizzati** — conoscenze, abilità, competenze chiave europee (Racc. UE 2018/C 189/01).
3. **Raccordo con le discipline** — tabella che associa a ciascuna disciplina i traguardi di competenza e gli agganci con il curricolo.
4. **Durata e tabella del percorso** — moduli con obiettivi, attività, materiali, tempi.
5. **Metodologie didattiche** — age-appropriate: gioco simbolico e routine per l'infanzia, laboratori per la primaria, flipped/cooperative/PBL/debate/service learning per le secondarie.
6. **Schede fotocopiabili** (infanzia e primaria) **o compiti di realtà / UdA** (secondarie).
7. **Rubrica di valutazione** — competenze × livelli (4 per infanzia/primaria/secondaria I; livelli D/C/B/A/A+ per secondaria II).
8. **Adattamenti per l'inclusione** — DSA, BES, disabilità intellettiva/sensoriale/motoria, italiano L2, plusdotati.
9. **Raccordo con il Piano di Emergenza scolastico** — D.M. 26/08/1992, D.Lgs. 81/2008, DVR (secondaria II).
10. **Coinvolgimento delle famiglie** — lettere informative, compiti a casa, evento finale.
11. **FAQ del docente** — 7-9 domande frequenti con risposte operative.
12. **Fonti normative e bibliografia** — normativa citata + letture consigliate (Beck, Jonas, IPCC AR6 per le secondarie).

**Specifiche aggiuntive per fascia:**

- **Infanzia**: percorso in 4 incontri da 30′ (2h totali), Campi di Esperienza coinvolti (Il sé e l'altro; Il corpo e il movimento; Immagini, suoni, colori; I discorsi e le parole; La conoscenza del mondo), schede con il 112 e la "tartaruga" (posizione di riparo antisismica).
- **Primaria**: percorso in moduli + laboratorio + valutazione = 8-10h, esperimenti semplici (modellino frana, gelatina per la scossa sismica, triangolo del fuoco), uscita sul territorio nel raggio di 500m.
- **Secondaria I grado**: moduli da 60′ + UdA "Conoscere il rischio del mio territorio" (12h + 3h lavoro autonomo), approfondimenti cross-disciplinari (Italiano: Buzzati/Calvino; Storia: da Messina 1908 ad Amatrice 2017; Arte: segnaletica D.Lgs. 81/2008; Tecnologia: IT-alert).
- **Secondaria II grado**: percorso fino a 70h totali, PCTO strutturato in 6 fasi con tutor interno/esterno, tre progetti di classe (A: analisi del Piano di evacuazione scolastico; B: mappatura del rischio di quartiere; C: mini campagna "Io non rischio"), temi pluridisciplinari per l'Esame di Stato (Rischio e responsabilità; Cambiamento climatico e territorio; Comunicazione, media e cittadinanza).

**Quando modificare un kit:**

- Se la normativa scolastica cambia (es. nuove Linee guida sull'educazione civica): aggiornare la sezione 1 di tutti e quattro i kit coerentemente.
- Se cambia il Piano di Emergenza del Comune o della singola scuola: aggiornare il raccordo nella sezione 9.
- Se un docente segnala un'esperienza d'uso: valutare se aggiungere una "Scheda esperienza" come esempio nella FAQ.
- Ogni modifica sostanziale ai kit va annotata nel changelog all'inizio del manuale.

**Non usare i kit come articoli di cronaca.** I kit sono pagine operative durevoli: non inserire nei kit date di singole iniziative o riferimenti a eventi specifici, ma linkare gli articoli in `content/comunicazioni/` dove necessario.

### 4.9 — Widget esterni click-to-load (Windy, INGV)

Il sito incorpora alcuni widget forniti da servizi esterni (mappe meteo, mappe sismiche) seguendo un pattern unico e riusabile: **click-to-load consensuale**. L'iframe non si carica automaticamente; l'utente vede un placeholder blu istituzionale con pulsante e, solo dopo il click, il browser riceve risorse dal server esterno. Questo approccio garantisce privacy-by-design (nessun cookie di terze parti al primo accesso), rispetta il GDPR e allinea il comportamento di tutti i widget esterni del sito.

Quando l'iframe è caricato, sopra di esso compare una **toolbar blu** con il titolo del widget e un bottone **"Chiudi mappa"** che riporta al placeholder originale. Questo è essenziale su mobile: l'iframe altrimenti cattura il touch (la mappa Windy/INGV interpreta lo swipe come pan) e l'utente non riesce più a scrollare la pagina sotto. Cliccando "Chiudi mappa" l'iframe viene rimosso, il placeholder viene ripristinato e si può tornare a navigare la pagina.

#### Widget attualmente pubblicati

| Widget | Fornitore | Pagine | Fonte ufficiale |
|---|---|---|---|
| Mappa meteo | **Windy.com** (Windyty, SE) | Home, [Allerte Meteo](/allerte-meteo/), [Strumenti](/strumenti/) | Strumento di consultazione: fonte ufficiale resta Centro Funzionale Regione Lazio |
| Mappa sismica | **INGV** (Istituto Nazionale di Geofisica e Vulcanologia, ente pubblico di ricerca italiano) | Home, [Rischio Sismico](/rischi-prevenzione/rischio-sismico/), [Strumenti](/strumenti/) | INGV è la fonte scientifica ufficiale italiana per la sismologia |
| Radar DPC | **Dipartimento della Protezione Civile** (ente pubblico italiano) | [Allerte Meteo](/allerte-meteo/), [Strumenti](/strumenti/) | Fonte istituzionale italiana per la sorveglianza meteo-idrologica |
| Fulmini | **Blitzortung / Lightning Maps** (rete volontaria internazionale) | [Temporali Intensi](/rischi-prevenzione/temporali-intensi/), [Strumenti](/strumenti/) | Rete scientifica volontaria, non istituzionale |
| Previsione meteo | **Aeronautica Militare** (Servizio Meteorologico Nazionale, Ministero Difesa) | [Allerte Meteo](/allerte-meteo/), [Strumenti](/strumenti/) | Fonte istituzionale italiana per le previsioni meteo |

#### Architettura del codice (DRY, un'unica fonte di verità)

- **Partial Hugo**: `themes/flavour-pcgenzano/layouts/partials/external-widget.html` — riceve un dict di parametri (`src`, `title`, `placeholderTitle`, `placeholderDesc`, `icon`, `btnLabel`, `altUrl`, `altLabel`, `fallbackText`, `widgetId`) e produce l'intero markup accessibile (`<section>` + placeholder + noscript + print fallback).
- **Shortcode Markdown**: `themes/flavour-pcgenzano/layouts/shortcodes/external-widget.html` — wrapper del partial utilizzabile direttamente dai file `.md` di contenuto con sintassi `{{</* external-widget ... */>}}`.
- **JavaScript**: `themes/flavour-pcgenzano/static/js/ext-widgets.js` — incluso globalmente in `baseof.html` con `defer`, scorre tutti i `.ext-widget-placeholder` presenti nella pagina e aggancia il click handler via class selector (no ID → supporta più istanze senza collisioni WCAG 4.1.1).
- **CSS**: `themes/flavour-pcgenzano/static/css/custom.css`, blocco "Widget esterni click-to-load". Include layout base, variante `.ext-widget-grid` a due colonne per l'homepage, override per mobile, `prefers-reduced-motion` e stampa.

#### Come aggiungere un nuovo widget esterno

**Da un file Markdown** (pagina di contenuto):

```markdown
{{</* external-widget
    src="https://..."
    title="Titolo descrittivo per lettori schermo"
    placeholderTitle="Titolo grande sul placeholder"
    placeholderDesc="Descrizione (accetta <strong>HTML</strong>)"
    icon="bi-cloud-rain-heavy"
    btnLabel="Carica il contenuto"
    altUrl="https://..."
    altLabel="Link alternativo"
    fallbackText="Testo mostrato su stampa"
    widgetId="slug-univoco" */>}}
```

**Da un template Hugo** (es. homepage):

```go-html-template
{{ partial "external-widget.html" (dict
  "src"              "https://..."
  "title"            "..."
  "placeholderTitle" "..."
  "placeholderDesc"  "..."
  "icon"             "bi-..."
  "btnLabel"         "..."
  "altUrl"           "https://..."
  "altLabel"         "..."
  "fallbackText"     "..."
  "widgetId"         "home-slug-univoco"
) }}
```

#### Regole di conformità (non violare)

1. **Ogni nuovo widget esterno va sempre dichiarato** in `content/privacy/_index.md` (tabella "Cookie di terze parti") e in `content/accessibilita/_index.md` (sezione "Contenuti di terze parti"). Aggiornare anche `dataUltimaRevisione`.
2. **Accessibilità WCAG 2.2 AA**: `<iframe>` sempre con `title`, `loading="lazy"`, `referrerpolicy="no-referrer-when-downgrade"`, focus trasferito dopo il click per annuncio screen reader, `<noscript>` con link alternativo, fallback stampa testuale.
3. **Disclaimer di fonte** (regola 06): sopra al widget scrivere chiaramente se la fonte è istituzionale (INGV, DPC) o uno strumento di consultazione non ufficiale (Windy). Per gli strumenti non ufficiali, ribadire che "non sostituisce il bollettino ufficiale".
4. **Nessun ID duplicato**: il `widgetId` di ogni istanza deve essere univoco nell'intera pagina. In home, prefissare con `home-` (es. `home-meteo-windy`) per distinguerlo dall'istanza nella pagina dedicata.
5. **Non caricare l'iframe al primo accesso**: il pattern click-to-load è vincolante. Un iframe che si carica automaticamente installerebbe cookie di terze parti senza consenso, violando privacy-by-design.
6. **Nessun iframe al di fuori del partial**: per coerenza, tutti gli iframe di terze parti passano per `partials/external-widget.html`. Non duplicare HTML/JS nei singoli file.

#### In modalità emergenza (homepage)

La sezione "Monitoraggio in tempo reale" in home compare **solo in modalità ordinaria**. Quando `data/emergenza.json` ha `attiva: true`, la homepage entra in emergency layout dove la priorità sono banner + numeri + azioni immediate: i widget non sono visibili in quel caso per non distrarre dai contenuti prioritari. Vedi `themes/flavour-pcgenzano/layouts/index.html`.

#### Parametri di centraggio geografico

| Widget | Parametri chiave | Note |
|---|---|---|
| Windy | `lat=41.6919`, `lon=12.6928`, `zoom=12`, `overlay=radar`, `height=600` | Genzano di Roma stretto, radar meteo di default |
| INGV | nessuno (URL fisso `https://terremoti.ingv.it/`) | Mostra tutta Italia; filtri magnitudo/periodo gestiti dall'utente dal menu INGV |
| Radar DPC | nessuno (URL fisso `https://mappe.protezionecivile.it/`) | Mosaico nazionale; zoom/pan utente |
| Blitzortung | `#8/41.6919/12.6928` nell'hash URL | Centro mappa su Genzano, zoom 8 (Lazio intero visibile) |

### 4.10 — Hub strumenti di consultazione (`/strumenti/`)

La pagina **Strumenti in tempo reale** è un hub unico che elenca tutti gli strumenti online utili per il monitoraggio del territorio: meteo, sismico, idrogeologico, incendi, qualità dell'aria, viabilità, emergenze. Esiste per dare al cittadino un singolo punto di accesso invece di disperdere i link su molte pagine.

#### Due tipi di strumento

1. **Widget incorporati**: lo strumento è embeddato sul nostro sito con il pattern click-to-load (§4.9). La card nell'hub ha il bottone **"Apri widget sul sito"** e porta all'ancora della pagina dove vive il widget (es. `/allerte-meteo/#meteo-windy`).
2. **Link esterni**: lo strumento non consente l'iframe (X-Frame-Options blocca) o non ha senso incorporarlo. La card nell'hub ha il bottone **"Apri sito ufficiale"** e apre la pagina del fornitore in una nuova scheda con `rel="noopener noreferrer"`.

#### Come è fatto

- **Markdown**: `content/strumenti/_index.md` — contiene le card raggruppate per categoria.
- **Shortcode**: `themes/flavour-pcgenzano/layouts/shortcodes/tool-card.html` — rende una singola card.
- **Parametri dello shortcode** `{{</* tool-card */>}}`: `nome`, `fonte`, `icona` (Bootstrap Icon), `descrizione`, `tipoFonte` (`istituzionale` | `consultazione`), `tipoAccesso` (`widget` | `sito`), `url`.
- **Badge automatico**: la card mostra un badge verde "Fonte istituzionale" se `tipoFonte=istituzionale`, un badge ambra "Strumento di consultazione" se `tipoFonte=consultazione`.
- **CTA automatico**: la card mostra "Apri widget sul sito" (stile filled) se `tipoAccesso=widget`, "Apri sito ufficiale" (stile outline) se `tipoAccesso=sito`.

#### Come aggiungere un nuovo strumento

**Caso A — Lo strumento consente l'iframe:**
1. Verifica con `curl -sI ... | grep -i x-frame` che non sia bloccato.
2. Aggiungi il widget iframe sulla pagina tematica appropriata con `{{</* external-widget */>}}` (vedi §4.9).
3. Nella `content/strumenti/_index.md` aggiungi una card nella categoria giusta con `tipoAccesso="widget"` e `url="/pagina-tematica/#anchor-widget"`.

**Caso B — Lo strumento NON consente l'iframe:**
1. Nella `content/strumenti/_index.md` aggiungi una card nella categoria giusta con `tipoAccesso="sito"` e `url="https://sito-ufficiale.esempio/"`.
2. Non serve nessun altro file.

**In entrambi i casi**, aggiorna:
- `content/privacy/_index.md` (tabella Cookie di terze parti o elenco link esterni)
- `content/accessibilita/_index.md` (sezione Contenuti di terze parti)
- `dataUltimaRevisione` delle due pagine sopra

#### Verifica X-Frame-Options prima di scegliere iframe

```bash
curl -sI -L -A "Mozilla/5.0" https://URL/ | grep -iE "x-frame-options|frame-ancestors"
```

Interpretazione:
- **Nessuna riga in output** → iframe consentito da terzi → caso A
- `X-Frame-Options: DENY` → iframe vietato da tutti → caso B
- `X-Frame-Options: SAMEORIGIN` → solo il sito stesso può iframarsi → caso B
- `Content-Security-Policy: ... frame-ancestors 'none'` → come DENY → caso B
- `Content-Security-Policy: ... frame-ancestors 'self' <host>` → iframe consentito solo a `<host>` → caso B se noi non siamo in quella lista

#### CTA in homepage

La sezione **Servizi per il cittadino** in homepage (`data/quick_links.yaml` → `servizi`) include una voce "Strumenti in Tempo Reale" che punta a `/strumenti/`. Quando aggiungi un nuovo strumento all'hub non serve modificare la home: il link è già presente.

### 4.11 — Versioni multilingua (selettore + hub linguistiche)

Il sito è scritto in **italiano**, ma offre **versioni curate dal Gruppo** in 7 lingue per turisti e residenti stranieri. La gestione è in livelli:

**1. Selettore lingue globale** — partial `themes/flavour-pcgenzano/layouts/partials/language-selector.html`

Bottone fisso in alto a destra (`position: fixed; top: 0.8rem; right: 0.8rem; z-index: 9999`) con icona traduzione e codice lingua. Click apre un modal accessibile (focus trap, ESC chiude) con:

- **Sezione "Versioni curate"**: link diretti alle 8 hub linguistiche (IT + 7 traduzioni)
- **Sezione "Traduzione automatica"**: passa il sito al proxy Google Translate `*.translate.goog` per FR/DE/ES/AR/ZH/JA/RU. Disclaimer chiaro: traduzioni approssimative, non istituzionali.

**2. Hub linguistiche curate** (`content/{lingua}/_index.md`)

| Lingua | URL | Aliases |
|---|---|---|
| English | `/english/` | `/en/`, `/en/index.html` |
| Français | `/francais/` | `/fr/`, `/fr/index.html` |
| Deutsch | `/deutsch/` | `/de/`, `/de/index.html` |
| Español | `/espanol/` | `/es/`, `/es/index.html` |
| Português | `/portugues/` | `/pt/`, `/pt/index.html` |
| Română | `/romana/` | `/ro/`, `/ro/index.html` |
| Esperanto | `/esperanto/` | `/eo/`, `/eo/index.html` |

Ogni hub è una pagina di sintesi con: numero 112, comportamenti per i 5 rischi principali, kit emergenza, IT-alert, mappa aree di attesa, contatti.

**3. Sotto-pagine essenziali tradotte**

In ogni lingua sono presenti 3 sotto-pagine dettagliate:

- `/{lingua}/numeri-utili/` — Numeri di emergenza
- `/{lingua}/cosa-fare-adesso/` — Comportamenti per ogni tipo di rischio
- `/{lingua}/piano-familiare/` — Template di piano familiare (mini-guida + checklist)

Slug delle sotto-pagine **mantenuti in italiano** per coerenza URL.

**Limiti dichiarati:**

- Le sotto-pagine tradotte coprono **3 pagine essenziali** per lingua (totale 21 file). Per il resto del sito, l'utente straniero usa il selettore "Traduzione automatica" che apre Google Translate.
- L'**Esperanto** è dichiarato come "best effort, non revisionato da denaska parolanto".
- **AR, ZH, JA, RU**: non abbiamo versioni curate, solo Google Translate (limite di competenza linguistica del Gruppo).

**Quando aggiungere una nuova lingua curata:**

1. Crea `content/{slug-lingua}/_index.md` (slug latino: `cinese`, `russo`, ecc. — niente caratteri non-latini).
2. Frontmatter con `aliases` per il codice ISO breve (`/zh/`, `/ru/`).
3. Stesso template visivo delle hub esistenti (CSS classes `.en-card`, `.en-tel`, `.en-list`).
4. Aggiungi al partial `language-selector.html` nella sezione "Versioni curate".
5. Aggiorna privacy + accessibilità.

### 4.12 — Mappa del Sito (`/mappa-sito/`)

Pagina hub di navigazione che raccoglie tutte le sezioni del sito divise per macro-area (servizi, allerte, rischi, formazione, comunicazioni, gruppo, strumenti, accessibilità, legali). Layout a card colorate (border-left per categoria), icone Bootstrap.

Linkata da:
- Footer (`hugo.toml` → `[[menus.footer]]`) come 5a voce
- Homepage `data/quick_links.yaml` → `servizi` come 7a card
- Aliases `/sitemap.html` e `/mappa/`

**Quando aggiornare la mappa-sito:**

Quando crei una nuova pagina top-level (es. `/glossario/`, `/strumenti/`), aggiungi una card alla sezione tematica corrispondente. Le pagine secondarie (sotto-categorie, articoli) NON vanno nella mappa-sito: quella è solo un indice di alto livello.

### 4.13 — Bottone SOS 112 (`partials/sos-112.html`)

Bottone fisso in basso a destra **solo su mobile e tablet** (su desktop nascosto perché il telefono non chiama). Click apre un modal di conferma (focus iniziale su "Annulla" per evitare chiamate accidentali). Solo dopo la conferma esplicita parte la chiamata `tel:112`.

Caratteristiche tecniche:
- `position: fixed; bottom: 1.2rem; right: 1.2rem; z-index: 10000`
- `display: none` di default, `display: flex !important` con media query `(max-width: 991.98px)`
- Animazione "pulse" ogni 2.5s (disattivata in `prefers-reduced-motion`)
- Modal accessibile: `role="dialog"`, `aria-modal="true"`, focus trap, ESC chiude
- Modal ricorda art. 658 CP (chiamate scherzo punibili)

Inserito in `baseof.html` via `{{ partial "sos-112.html" . }}` — appare in tutte le pagine Hugo. NON appare nei giochi/app standalone (che hanno il proprio HTML, non baseof.html).

### 4.14 — Mappa interattiva delle aree di emergenza (`/cartografia/`)

La pagina `content/cartografia/_index.md` mostra in cima alla sezione una **mappa interattiva** con i 16 punti del Piano di Emergenza Comunale (Aree di Attesa, 2 Ammassamento Soccorritori, Aree di Ricovero). La mappa è costruita su tre componenti:

1. **Dati**: `data/aree_emergenza.yaml` — array di oggetti con `id`, `tipo` (AA/AS/AR), `nome`, `indirizzo`, `lat`, `lon`, `verified`.
2. **Shortcode**: `{{< mappa-aree >}}` definito in `themes/flavour-pcgenzano/layouts/shortcodes/mappa-aree.html` — incorpora CSS, JS, marker SVG colorati, popup con link a Google Maps + cartello segnaletico, filtri per tipologia, geolocalizzazione "Centra sulla mia posizione".
3. **Libreria**: Leaflet 1.9.4 self-hosted in `themes/flavour-pcgenzano/static/vendor/leaflet/` (CSS, JS, immagini marker). Nessun CDN esterno: tutto è servito dal nostro stesso dominio.

**Tile cartografiche**: OpenStreetMap (`tile.openstreetmap.org`). Le tile sono caricate al primo accesso alla pagina, senza cookie di profilazione, ma il fornitore vede l'IP dell'utente. Citato esplicitamente nella [Privacy Policy](/privacy/) sezione "Cartografia interattiva".

**Geolocalizzazione**: usa `navigator.geolocation.getCurrentPosition` del browser, dopo esplicito consenso. La posizione è elaborata localmente per centrare la mappa, mai inviata al nostro server. Il bottone è disattivato se il browser non supporta l'API.

**Marker e colori** (riprodotti come pallini nei popup):
- AA — Aree di Attesa: blu `#0d6efd`
- AS — Ammassamento Soccorritori: arancione `#ea580c`
- AR — Aree di Ricovero: verde `#198754`

**Coordinate verificate**: tutti i 16 pin sono ora `verified: true` con coordinate fornite e validate dal referente del Gruppo (aprile 2026). La pagina cartografia mostra comunque un avviso visibile "in fase di sviluppo" perché i pin restano oggetto di revisione e l'utente è invitato a riferirsi al PDF del Piano per le indicazioni operative ufficiali. Per correggere una coordinata: aprire `data/aree_emergenza.yaml`, aggiornare `lat`/`lon`, commit e push.

**Nota AR2 — Via Sicilia non Via Piemonte**: il documento ufficiale del Piano riporta il Campo Sportivo AR2 come "Via Piemonte", ma è un errore di redazione del Piano stesso: l'area è in Via Sicilia. Il sito riporta la denominazione corretta verificata sul campo, con una nota esplicita nelle tabelle. Se in futuro il Piano viene revisionato, allineare la nota.

**Accessibilità**:
- Map div con `role="application"` e `aria-label` esplicito.
- Tabelle complete sotto la mappa restano la fonte accessibile equivalente per chi non può usare il visualizzatore.
- Filtri tipologia sono `<button>` con `aria-pressed` toggle.
- Marker hanno `title` e `alt` con ID + nome + tipologia.
- `<noscript>` rimanda alle tabelle se JavaScript è disattivato.
- Scroll wheel zoom disabilitato di default (si attiva al focus della mappa) per non bloccare lo scroll della pagina su mobile.

**Aggiungere un nuovo punto**:

```yaml
# In data/aree_emergenza.yaml
- id: AA11
  tipo: AA
  nome: "Nuova area"
  indirizzo: "Via Esempio, snc"
  lat: 41.7000000
  lon: 12.6900000
  verified: true
```

Ricordarsi di aggiungere anche la riga corrispondente nelle tabelle di `content/cartografia/_index.md` (le tabelle restano fonte accessibile e il PDF del Piano va aggiornato manualmente).

### 4.10 — Pulsante "Leggi ad alta voce" (TTS) sulle pagine essenziali

Le pagine essenziali per il cittadino possono attivare un pulsante **"Leggi ad alta voce"** che usa la sintesi vocale del browser per leggere il contenuto in italiano.

**Per attivarlo su una pagina nuova:**
- Aggiungere `tts: true` nel frontmatter dell'articolo o `_index.md`.

**Quando attivarlo:**
- ✅ Pagine operative consultate in emergenza (cosa fare, numeri utili, allerte)
- ✅ Pagine per fragili (facile da leggere, kit didattici)
- ❌ Pagine legali (privacy, note legali, accessibilità) — non utili da leggere
- ❌ Pagine tecniche (mappa sito, attribuzioni) — solo elenchi di link

Già attivo su 12 pagine: `/cosa-fare-adesso/`, `/numeri-utili/`, `/facile-da-leggere/`, `/allerte-meteo/`, `/piano-familiare/` + 7 sotto-pagine `/rischi-prevenzione/*`.

**Caso d'uso:** anziani con vista debole, persone in stress, parlanti italiano L2, bambini, utenti con dislessia.

### 4.11 — Box "Cosa NON fare" per pagine rischio

Per evidenziare i comportamenti DA EVITARE (più efficace di "non" sparsi nel testo), usare lo shortcode:

```markdown
{{</* cosa-non-fare titolo="Cosa NON fare in caso di terremoto" */>}}
- **Non correre fuori durante la scossa**: la maggior parte delle vittime è colpita da calcinacci
- **Non usare gli ascensori**: possono bloccarsi
- **Non rientrare in edifici danneggiati** per recuperare oggetti
{{</* /cosa-non-fare */>}}
```

Parametro `titolo` opzionale (default: "Cosa NON fare"). Output: box rosso bordato con icona divieto, contrasto WCAG AA. In stampa diventa nero su bianco. Già attivo nelle 7 pagine `/rischi-prevenzione/*`.

**Quando aggiungerlo:**
- ✅ Pagine rischi specifici (sismico, alluvione, incendio, ecc.)
- ✅ Articoli su autoprotezione che includono divieti chiari
- ❌ Articoli generici / di servizio

### 4.12 — Pagina `/emergenza/` ultra-leggera per banda debole

Esiste una pagina dedicata `/emergenza/` (44 KB vs 64 KB della homepage) per consultazione rapida quando la rete è satura. Aliases: `/lite/`, `/emergenza-essenziale/`. Linkata dal footer.

Contenuto in ordine di priorità: banner emergenza (se attivo), 112 grande, stato allerta meteo dinamico colorato, 4 numeri essenziali, 6 azioni "cosa fare ora", 7 link rapidi.

**Manutenzione:** la pagina è statica e si aggiorna automaticamente con i dati di `data/allerta.json` e `data/emergenza.json`. Per modificare i numeri o le azioni: editare lo shortcode `themes/flavour-pcgenzano/layouts/shortcodes/pagina-emergenza-lite.html`.

**Quando segnalarla:** in fase di emergenza dichiarata, è la pagina da diffondere via canali social/SMS perché si carica anche con rete debolissima.

---

_[Indice manuale](README.md)_

[← Parte 03 — Immagini per gli articoli](parte-03-immagini-per-gli-articoli.md) · [↑ Indice](README.md) · [Parte 05 — Checklist pre-pubblicazione →](parte-05-checklist-pre-pubblicazione.md)
