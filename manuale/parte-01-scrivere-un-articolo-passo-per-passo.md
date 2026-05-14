_[Indice manuale](README.md)_

# Parte 1 — Scrivere un articolo passo per passo

Un articolo va nella cartella `content/comunicazioni/` e appare nella sezione "Comunicazioni"
del sito, in home come notizia recente, e negli RSS. Se devi creare una **pagina statica** (es.
"Dove siamo", "Cosa facciamo"), vai direttamente alla **Parte 4**.

### Passo 1.1 — Decidi se è davvero un articolo

Un articolo è giustificato se risponde a una di queste domande:

- C'è un **fatto nuovo** (allerta, evento, esercitazione, notizia del gruppo)?
- C'è un **contenuto formativo** stagionale o legato a un'occorrenza (anniversario, campagna)?
- C'è un **approfondimento** su un rischio o su una buona pratica?

Se il contenuto è **permanente** (es. "come prepararsi a un terremoto", inteso come guida
evergreen), probabilmente va in una **pagina statica** sotto `/rischi-prevenzione/`, non in
un articolo.

### Passo 1.2 — Scegli la categoria (badge)

Il badge determina il colore e l'etichetta visibile. Scegli in base al contenuto, non alla
"vibe" che vuoi dare:

| Badge | Quando usarlo | Esempio |
|---|---|---|
| `Allerta` | Allerta meteo o rischio in corso, con livello e area precisi | "Allerta arancione per vento forte domani" |
| `Avviso` | Avvisi operativi non critici | "Chiusura Via Sicilia per esercitazione domenica" |
| `Comunicazione` | Aggiornamento istituzionale o organizzativo | "Nuova sede operativa dal 1° giugno" |
| `Attività` | Resoconto di un'attività del gruppo | "Weekend di pulizia sentieri ai Castelli" |
| `Formazione` | Corsi, attestazioni, percorsi formativi | "Corso BLSD: consegnato il defibrillatore" |
| `Evento` | Eventi pubblici | "Io Non Rischio 2026 in piazza" |
| `Volontariato` | Promozione, iscrizioni, testimonianze | "Terremoto Aquila: il ricordo dei volontari" |
| `Radiocomunicazioni` | Frequenze, reti radio, radioamatori | "Attivata rete Zamberletti per esercitazione" |
| `Prevenzione` | Buone pratiche evergreen | "Triangolo del fuoco: come prevenire gli incendi" |
| `Esercitazione` | Esercitazioni programmate o concluse | "Esercitazione sismica 15 maggio" |
| `Aggiornamento` | Aggiornamenti normativi o procedurali | "Nuovo gestionale ActivePager dal 1° aprile" |
| `Informazione` | Informazioni generiche | "Il calendario DPC 2026 è online" |
| `Emergenza` | Comunicazioni **durante** un'emergenza in atto | "Squadre attivate per alluvione Via Appia" |

**Regola d'oro:** una sola categoria per articolo. Se è ambiguo, scegli la più **operativa**
(quella che dice al lettore cosa fare).

**Palette dei colori** (contrasto WCAG AA ≥ 4.5:1 su bianco). Ogni badge ha una tinta dedicata,
applicata sia al tag dell'articolo sia al pulsante di filtro nella pagina di archivio:

- Allerta `#d9364f` · Emergenza `#7f1d1d` · Avviso `#b45309` · Evento `#c026d3`
- Comunicazione `#003366` · Radiocomunicazioni `#0369a1` · Informazione `#0284c7`
- Prevenzione `#15803d` · Esercitazione `#ea580c` · Aggiornamento `#4338ca`
- Formazione `#7c3aed` · Volontariato `#b45309` · Attività `#0891b2`

Se crei un badge nuovo (non in lista), riceve un colore automatico deterministico da una palette
accessibile di 16 tinte (vedi `themes/flavour-pcgenzano/layouts/partials/badge.html`).

### Passo 1.3 — Crea il file con Hugo

Apri il terminale nella cartella del sito (`~/sito-pc-genzano`) e lancia:

```bash
hugo new comunicazioni/AAAA-MM-GG-titolo-breve.md
```

**Esempio:**

```bash
hugo new comunicazioni/2026-05-15-esercitazione-sismica-genzano.md
```

Hugo crea il file con il frontmatter base già compilato dall'archetype.

**Regole del nome file:**

- Prefisso data obbligatorio: `AAAA-MM-GG-`
- Slug breve: massimo 6-7 parole, minuscolo, separate da trattini.
- Niente accenti, apostrofi, lettere maiuscole, spazi, caratteri speciali.
- Niente articoli o preposizioni inutili (`il`, `la`, `di`, `del`).

| Buono | Cattivo | Perché |
|---|---|---|
| `2026-05-15-esercitazione-sismica.md` | `Esercitazione sismica 15 maggio.md` | Spazi, maiuscole, niente data prefisso |
| `2026-05-15-allerta-arancione-vento.md` | `2026-05-15-allerta-meteo-arancione-per-vento-forte-previsto-domani.md` | Troppo lungo |
| `2026-05-15-io-non-rischio.md` | `2026-05-15-L'evento-Io-Non-Rischio.md` | Apostrofo, maiuscole, articoli |

### Passo 1.4 — Compila il frontmatter

Il frontmatter è la sezione tra `---` all'inizio del file. Ogni campo ha un ruolo preciso.

**Template di partenza:**

```yaml
---
title: "Titolo chiaro e informativo (max 80 caratteri)"
date: 2026-05-15
description: "Sommario breve: max 160 caratteri, utile per SEO e anteprima social."
badge: "Comunicazione"
priorita: "normale"
autore: "Gruppo Comunale Volontari PC Genzano"
image: "/images/2026-05-15-nome-descrittivo.webp"
scadenza: ""
area: "Comune di Genzano di Roma"
allegati: []
draft: false
---
```

#### Campo per campo

**`title`** — stringa tra virgolette, massimo ~80 caratteri.

- Descrive **cosa** c'è nell'articolo, non lo vende.
- Evita punto esclamativo, puntini di sospensione, emoji, maiuscole artificiose.
- Niente "Incredibile...", "Scopri...", "Non perdere...".

✅ `"Calendario del Dipartimento della Protezione Civile 2026"`
❌ `"Scopri l'incredibile calendario 2026 del Dipartimento! 🎉"`

**`date`** — schema dipendente dal numero di articoli/giorno.

**Caso A (default, 1 articolo/giorno)**: formato semplice `AAAA-MM-GG`, **senza virgolette**, **senza orario**.

- ✅ `date: 2026-05-15`
- ❌ `date: "2026-05-15"` (stringa invece di data)
- ❌ `date: 15/05/2026` (formato europeo non supportato)

**Caso B (2+ articoli nello stesso giorno)**: formato ISO 8601 con orario crescente per ogni articolo, in ordine di pubblicazione (l'ultimo scritto ha l'orario maggiore e finisce in cima all'archivio).

- ✅ 1° articolo del giorno: `date: 2026-05-15T00:01:00+02:00`
- ✅ 2° articolo: `date: 2026-05-15T00:02:00+02:00`
- ✅ 3° articolo: `date: 2026-05-15T00:03:00+02:00`
- ❌ `date: 2026-05-15T10:30:00Z` (timezone UTC `Z`: usa sempre `+02:00`)
- ❌ `date: 2026-05-15T16:00:00+02:00` (orario "alto": se è il giorno corrente e Hugo gira prima delle 14:00 UTC, l'articolo è "futuro" e non appare nel build fino al rebuild successivo)

**Perché orari "minimi" (00:01, 00:02, …):**
L'orario non viene mostrato all'utente (il template renderizza solo "15 maggio 2026"). Serve esclusivamente come tie-break per l'ordering Hugo Date desc. Orari piccoli garantiscono che gli articoli del giorno corrente non risultino "futuri".

**Fix retroattivo automatico:**
Se ti accorgi a posteriori di aver pubblicato 2 articoli stessa giornata con `date` solo-data, lancia `python3 scripts/fix-ordering-articoli-stesso-giorno.py` — è idempotente, legge l'ordine git first-commit di ciascun file e assegna orari `00:01, 00:02, …` rispettando l'ordine reale di pubblicazione.

**`description`** — sommario, **massimo 160 caratteri** (incluse spaziature).

- Autosufficiente: deve aver senso anche fuori contesto (Google, WhatsApp, Facebook).
- Prima frase = risposta alla domanda "di cosa parla?".
- Niente "In questo articolo parliamo di..." (parla del contenuto, non dell'articolo).

**Come verificare la lunghezza:**

```bash
echo "La tua description qui" | wc -m
```

Se supera 160 **accorcia**. Non c'è alternativa.

**`badge`** — una stringa tra virgolette, scelta dalla tabella del Passo 1.2.

- Se usi un badge nuovo (non in lista), il sito gli assegna un colore automatico generato dall'hash del nome.
- Lo stesso nome produrrà sempre lo stesso colore, quindi puoi introdurre nuove categorie.

**`priorita`** — solo due valori ammessi: `"normale"` oppure `"urgente"`.

- `"urgente"` aggiunge un bordo rosso e un'etichetta URGENTE.
- **Non esistono** `"alta"`, `"bassa"`, `"critica"`, `"media"`.

**`autore`** — di default `"Gruppo Comunale Volontari PC Genzano"`. Se l'articolo ha un
autore ospite (es. un esperto esterno), puoi sovrascrivere: `"Dott. Mario Rossi, geologo"`.

**`image`** — percorso relativo dell'immagine di copertina. Vedi **Parte 3** per le specifiche.

- Se non hai un'immagine, lascia `image: ""` (stringa vuota). Il sito userà un'immagine di
  default con il logo del gruppo.
- Percorsi validi:
  - `/images/nome.webp` (file in `static/images/nome.webp`)
  - `""` (nessuna immagine)

**`scadenza`** — data in formato `AAAA-MM-GG` oppure stringa vuota `""`.

- Compilala **solo** se l'articolo ha un limite temporale reale (evento, iscrizione, avviso
  temporaneo).
- Dopo la data di scadenza, il sito mostra un avviso "Comunicazione scaduta" in cima
  all'articolo.
- Esempi sensati: scadenza iscrizioni a un corso, fine di una campagna, data limite per
  un'ordinanza.

**`area`** — zona geografica rilevante. Aiuta il lettore a capire se lo riguarda.

- Es: `"Comune di Genzano di Roma"`, `"Castelli Romani"`, `"Provincia di Roma"`,
  `"Regione Lazio"`, `"Territorio nazionale"`, `"Comune di Fossa (AQ)"`.
- Vuoto (`""`) se non geografico.

**`allegati`** — lista di PDF o documenti scaricabili. Due formati:

```yaml
# Nessun allegato
allegati: []

# Con allegati
allegati:
  - titolo: "Ordinanza sindacale n. 42/2026 (PDF, 120 KB)"
    url: "/allegati/2026/ordinanza-42-2026.pdf"
  - titolo: "Mappa aree di attesa (PDF, 1,2 MB)"
    url: "/allegati/2026/mappa-aree-attesa.pdf"
```

- Il `titolo` deve indicare **tipo** (PDF, ODT, DOCX) e **dimensione** del file.
- L'`url` è il percorso relativo del file, risolto rispetto alla root del sito. Deposita il file in `static/<cartella>/nome.pdf` e l'URL sarà `/<cartella>/nome.pdf`.
- Per nuovi PDF depositati via git il percorso canonico è **`static/allegati/AAAA/`** (allegati di articoli) o **`static/manuali/`** (manuali tecnici permanenti). **Non** usare `static/documenti/` per file depositati via git: è escluso dal deploy FTP (vedi Parte 10.2 — Cartelle protette).
- Per PDF esterni (es. dipartimento): URL completo `https://...`.

**`draft`** — `true` o `false` (senza virgolette).

- `true` → bozza, visibile solo in `hugo server -D`, esclusa dalla pubblicazione.
- `false` → pubblicato al prossimo push su `main`.

### Passo 1.5 — Scrivi il titolo (dentro il frontmatter)

Un buon titolo di articolo istituzionale risponde a:

1. **Cosa è successo / che cos'è?** (il fatto, non l'opinione)
2. **Dove / quando?** (se rilevante)
3. **Perché mi riguarda?** (implicito ma guidante)

**Formule consigliate:**

- Cosa + dove: `"Allerta arancione per vento forte sui Castelli"`
- Evento + anno: `"Io Non Rischio 2026 in piazza a Genzano"`
- Tema + azione: `"Come prepararsi a un terremoto: la guida per le famiglie"`
- Resoconto + fatto: `"Consegnato il defibrillatore della Regione Lazio"`

**Titoli da evitare:**

| Cattivo | Perché | Migliore |
|---|---|---|
| `"NEWS: allerta meteo"` | Non dice quale allerta, è generico | `"Allerta gialla per temporali domani"` |
| `"Grande successo per l'evento!"` | Enfatico, non informativo | `"Io Non Rischio 2026: oltre 200 visitatori"` |
| `"Un momento importante"` | Vuoto di contenuto | `"Consegnato il defibrillatore della Regione Lazio"` |

### Passo 1.6 — Scrivi la description

La description è il **biglietto da visita** dell'articolo su Google, WhatsApp, Facebook,
Telegram. Ha solo **160 caratteri** per convincere il lettore ad aprirlo.

**Struttura consigliata:**

1. **Primo 1/3**: il fatto principale (chi, cosa).
2. **Secondo 1/3**: la specifica rilevante (quando, dove).
3. **Ultimo 1/3**: cosa trova leggendo (o perché lo riguarda).

**Esempio su 160 caratteri:**

> *"Il 16 marzo 2026 la Regione Lazio ha consegnato 100 defibrillatori ai gruppi di Protezione Civile del territorio. Anche il nostro Gruppo è tra i beneficiari."*

(158 caratteri, verifica con `wc -m`.)

**Errori comuni:**

- Description uguale al titolo → spreco.
- Description che inizia con "In questo articolo..." → metalinguaggio, parla del contenuto.
- Description troncata a metà frase → conta i caratteri prima.

### Passo 1.7 — Struttura il corpo dell'articolo

Un articolo ben strutturato ha **Livelli**:

1. **Apertura** (1-2 frasi): il fatto principale, in grassetto la parte più importante.
2. **Corpo** con sotto-sezioni `## Titolo sezione` (H2).
3. **Chiusura** (facoltativa): numeri utili, prossimi passi, fonti.

**Gerarchia titoli nel corpo:**

- `H1` è **solo il titolo** dell'articolo (lo genera Hugo dal frontmatter). Non usarlo nel corpo.
- `H2` → sezioni principali (`## Cosa succede`, `## Cosa fare`, `## Chi contattare`).
- `H3` → sotto-sezioni dentro un H2.
- `H4` → raramente, solo se davvero serve.

**Non saltare livelli** (H2 → H4): è un errore di accessibilità.

**Apertura efficace:**

```markdown
**Domenica 20 aprile, dalle 9:00 alle 12:00, Via Sicilia sarà chiusa al traffico**
per consentire lo svolgimento di un'esercitazione del Gruppo Comunale Volontari di
Protezione Civile.
```

Il lettore capisce **cosa/quando/dove** nella prima frase.

### Passo 1.8 — Scrivi il corpo seguendo le regole AGID

Rileggi la **Parte 2** per la lista completa. In sintesi:

- Frasi brevi (**sotto le 20 parole**).
- Voce **attiva**.
- Parole **comuni** (casa > abitazione, paga > effettua il pagamento).
- Verbi **diretti** rivolti al cittadino ("chiama", "scarica", "consulta").
- **Un concetto per paragrafo**.
- **Elenchi puntati** per 3+ elementi paralleli.
- **Grassetto** solo per parole chiave (non frasi intere).
- **Link** con testo descrittivo (mai "clicca qui").
- Numeri di emergenza **sempre verificati**. Nel Lazio il riferimento per il cittadino è il **112** (NUE), unico numero di emergenza. Citare inoltre **803 555** (Sala Operativa PC Lazio) e **1530** (Guardia Costiera).

### Passo 1.9 — Aggiungi le fonti e i riferimenti

Se l'articolo cita dati, allerte, leggi, bollettini:

- **Nomina la fonte** nel testo: "*secondo il bollettino del Centro Funzionale Regionale Lazio*".
- **Linka la fonte** con testo descrittivo.
- Per norme: linka [Normattiva](https://www.normattiva.it/) o la Gazzetta Ufficiale.
- Per dati meteo: solo fonti istituzionali (ARPA Lazio, Centro Funzionale, Protezione Civile nazionale).

**Divieto:** non citare social media o fonti non istituzionali come prova di fatti.

### Passo 1.10 — Aggiungi gli allegati

Se hai PDF o documenti:

1. Metti il file nella cartella `static/` appropriata:
   - `static/allegati/AAAA/` — allegati specifici di un articolo (ordinanze, mappe, moduli).
   - `static/manuali/` — manuali tecnici permanenti citati da più articoli (es. manuale FIC, Libro Risparmio Barilla).
   - **Non** usare `static/documenti/`, `static/cartelli/`, `static/giochi-bambini/`, `static/formazionepc/`, `static/quizpc/` per file depositati via git: queste cartelle sono **escluse dal deploy FTP** (vedi Parte 10.2 — Cartelle protette) e i nuovi file non arriverebbero su Aruba. Sono riservate a contenuto gestito direttamente sul server.
2. Aggiungi alla lista `allegati:` del frontmatter (vedi Passo 1.4).
3. **Non linkare direttamente il PDF nel corpo** a meno che non sia un riferimento breve:
   il sito genera automaticamente la sezione "Allegati" a fine pagina.

**Dimensioni ragionevoli:**

- Sotto 2 MB per un PDF di testo.
- Sotto 5 MB per un PDF con mappe o foto.
- Sopra 5 MB: comprimi il PDF prima (strumenti gratuiti: [ILovePDF](https://www.ilovepdf.com/), GhostScript).

### Passo 1.11 — Prepara l'immagine

Leggi tutta la **Parte 3**. In sintesi:

1. Scegli o crea l'immagine (foto originale, infografica, logo).
2. Ridimensiona a **1200px di larghezza**.
3. Aggiungi la **fascia blu istituzionale** in basso.
4. Esporta in **WebP**, qualità 80%, **max 200 KB**.
5. Salva in `static/images/AAAA-MM-GG-descrizione.webp`.
6. Aggiorna il campo `image:` nel frontmatter.

**Scorciatoia: foto automatica da fonti libere (anche da mobile).** Tre fonti supportate, tutte con licenze libere e attribuzione gestita automaticamente.

| Fonte | Quando usarla | Esempio |
|---|---|---|
| **Wikipedia** | Eventi storici, persone, opere, organizzazioni | Terremoti famosi, alluvioni, ritratti istituzionali |
| **NASA** | Fenomeni globali visti dallo spazio | Uragani, eruzioni vulcaniche, ondata calore |
| **USGS** | ShakeMap di un terremoto specifico | Mappa intensità Mercalli per articoli sismici |

**Da PC:** esegui direttamente lo script che ti serve:
```bash
bash scripts/foto-da-wikipedia.sh "Terremoto del Friuli del 1976" 2026-05-06-friuli-1976
bash scripts/foto-da-nasa.sh      "Etna eruption"                  2026-08-12-etna
bash scripts/foto-da-usgs.sh      shakemap us10006g7d              2026-08-24-amatrice-shakemap
```

Tutti gli script: scaricano in alta risoluzione, applicano la fascia blu istituzionale, salvano in `static/images/<slug>.webp` (max ~200 KB), stampano autore + licenza + URL origine da citare in didascalia.

**Da mobile / app cloud:** la sandbox blocca i domini esterni. Soluzione: lascia `image: ""` e chiedi a Claude in italiano (es. *"trovami una foto gratuita di terremoto Friuli per l'articolo X"*). L'agent `pc-image-fixer` (Parte 19) cerca su Wikipedia/NASA/USGS via WebFetch + scarica + applica fascia blu + inserisce shortcode `{{< foto >}}` **inline nel corpo articolo** (mai nel banner — vedi più sotto).

> ⚠️ **Marker `# TODO-foto-*` BANDITO dal 3 maggio 2026.** Il marker scritto nel corpo Markdown veniva renderizzato da Hugo come `<h1>` finché il workflow non lo rimuoveva, e se `deploy.yml` finiva prima del workflow CI il sito andava live col marker H1 visibile al posto del titolo (incidente reale). Inoltre il workflow popolava `image:` con la foto, sovrascrivendo il banner col titolo. Vedi CLAUDE.md punto 9 per dettagli.

**Per trovare un eventid USGS** (terremoti): cerca su `https://earthquake.usgs.gov/earthquakes/search/` per data/luogo, l'ID compare nell'URL della pagina evento.

**Banner col titolo intoccabile.** Il banner dell'articolo (campo `image:`) deve **sempre** mostrare la cover tipografica col titolo. Mai una foto reale. Le foto vanno **sempre nel corpo** come `{{< foto >}}`. La cover tipografica serve a 3 scopi:
1. Banner istituzionale dell'articolo (riconoscibile)
2. Anteprima Open Graph quando il link è condiviso su WhatsApp/Telegram/FB/X/LinkedIn
3. Fallback in emergenza (pagina lite `/emergenza/`)

**Cover tipografica automatica come fallback**. Se non aggiungi foto, lo script `auto-cover-mancanti.py` (chiamato dal workflow `scarica-foto-automatica.yml` step 2) genera automaticamente una **cover tipografica istituzionale** (gradiente blu, titolo dell'articolo, fascia con logo) in `static/images/<slug>.webp` e popola il frontmatter. Lo script è sicuro: **non sovrascrive mai** una foto utente custom (es. `image: "/images/foto-evento-mio.webp"`). E rigenera anche se per errore il file viene cancellato. Risultato: nessun articolo finisce mai online senza banner.

**Livelli di fallback in cascata per il banner**:
1. **Cover tipografica istituzionale** col titolo — gradiente blu generato automaticamente (sempre)
2. **Default SVG generico** — fallback estremo se la cover non si genera (`images/notizia-default.svg`)

### Passo 1.12 — Test locale con Hugo

Prima di pubblicare, testa in locale:

```bash
cd ~/sito-pc-genzano
hugo server -D
```

Apri `http://localhost:1313` nel browser:

- Verifica che l'articolo appaia in home e nella sezione Comunicazioni.
- Verifica che il badge abbia il colore giusto.
- Verifica che l'immagine si carichi e abbia la fascia blu.
- Verifica che la description appaia nell'anteprima.
- Verifica i link cliccandoli: devono portare dove ti aspetti.

**Errori frequenti:**

- L'articolo non appare → controlla `draft: false` e formato data (`AAAA-MM-GG` per giornata singola, oppure `AAAA-MM-GGT00:0N:00+02:00` se ci sono 2+ articoli stessa giornata; mai `Z` come timezone).
- L'immagine non si carica → controlla percorso e nome file (case-sensitive).
- I link interni non funzionano → usa URL relativi (`/contatti/` non `contatti/`).

### Passo 1.13 — Verifica con la checklist AGID

Vai a **Parte 5** e spunta ogni voce. Se qualcosa non è a posto, torna indietro.

> 🤖 **Se stai lavorando con Claude Code (CLI desktop, app mobile, sessione cloud, agent GitHub):** prima del `git add` Claude **deve obbligatoriamente** invocare l'agent `pc-article-reviewer` sul file appena scritto. Il gate è codificato in `CLAUDE.md` § *"Auto-gate AGID prima del commit di un nuovo articolo"* e in `.claude/rules/02-content-design-pa.md` § *"Auto-gate AGID prima del commit"*. Solo dopo il via libera dell'agent (o dopo l'applicazione dei suoi fix) si procede al commit. Il gate vale anche per un singolo articolo. Eccezione: se chiedi esplicitamente un **registro non-AGID** (comunicato stampa, lettera istituzionale, paper scientifico, qualsiasi altro genere a tua richiesta esplicita), il gate è sospeso per quel documento — vedi **Parte 12** per i comunicati stampa.

### Passo 1.13-bis — Genera il QR code dell'articolo

Ogni articolo ha un **QR code** scaricabile e stampabile (bottone "Scarica QR" accanto a "Stampa"), utile per le affissioni in bacheca, sedi e info-point. Dopo aver creato il file dell'articolo, genera il QR con:

```bash
python3 scripts/genera-qr-articoli.py
```

Lo script è **idempotente**: genera solo i QR mancanti, salta quelli già presenti. Produce `static/qr/<nome-file>.png` e `.svg`. Se è la prima volta, installa la dipendenza con `pip install --break-system-packages segno`. I file `static/qr/` vanno aggiunti al commit (Passo 1.14). Se salti questo passo l'articolo si pubblica lo stesso: semplicemente il bottone "Scarica QR" non appare finché il QR non viene generato (il partial si auto-nasconde).

### Passo 1.13-ter — Aggiorna l'indice di ricerca

Il sito ha una **ricerca full-text** (icona ricerca nella navbar o scorciatoia <kbd>Ctrl</kbd>+<kbd>K</kbd>) basata su [Pagefind](https://pagefind.app). L'indice è una fotografia del sito: copre solo gli articoli **già pubblicati** al momento della generazione. Per far comparire i nuovi articoli nei risultati, rigenera l'indice con:

```bash
bash scripts/genera-indice-ricerca.sh
```

Lo script ricostruisce il sito, lo indicizza e aggiorna `static/pagefind/` (da aggiungere al commit). Non è obbligatorio a ogni articolo: l'articolo si pubblica e resta raggiungibile da menu, archivio e link interni anche senza re-indicizzazione — semplicemente non compare nella ricerca finché non rigeneri. **Abitudine consigliata: rigenera una volta a settimana** o dopo aver pubblicato un blocco di articoli. Richiede `npx` (Node.js); Pagefind viene scaricato al volo, niente `node_modules` nel repo.

### Passo 1.14 — Commit e push

```bash
git add content/comunicazioni/2026-05-15-tuo-articolo.md static/images/2026-05-15-tua-immagine.webp static/qr/2026-05-15-tuo-articolo.png static/qr/2026-05-15-tuo-articolo.svg
git commit -m "Articolo: titolo breve dell'articolo"
git push origin main
```

Il push attiva la GitHub Action che:

1. Builda il sito con Hugo.
2. Lo carica via FTP su Aruba (`www.protezionecivilegenzano.it`).
3. Lo pubblica su GitHub Pages (preview).

**Verifica dopo 2-3 minuti:**

- Apri https://www.protezionecivilegenzano.it/ e controlla che l'articolo sia online.
- Apri la tab "Actions" su GitHub: il build deve essere **verde**. Se è rosso, apri il log
  e leggi l'errore.

### Passo 1.15 — Condividi (opzionale)

Se l'articolo è rilevante:

- Condividilo sul canale Telegram ufficiale.
- Pubblicalo su Facebook e Instagram con un estratto.
- Per articoli urgenti, fai un broadcast sui canali ufficiali.

---

_[Indice manuale](README.md)_

[← Parte 00 — Come usare questo manuale](parte-00-come-usare-questo-manuale.md) · [↑ Indice](README.md) · [Parte 02 — Le regole AGID in dettaglio →](parte-02-le-regole-agid-in-dettaglio.md)
