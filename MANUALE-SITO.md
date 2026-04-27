# Manuale Operativo — Sito Protezione Civile Genzano di Roma

**Versione:** 2.4
**Ultimo aggiornamento manuale:** 2026-04-24
**Ultimo check linee guida AGID:** 2026-04-20
**Manuale operativo di design PA:** versione 2025.1
**Bootstrap Italia:** versione 2.17.3
**Writing Toolkit Designers Italia:** versione bozza corrente
**WCAG di riferimento:** 2.2 livello AA
**Hugo di riferimento:** 0.143.x extended

> Questo manuale viene verificato automaticamente ogni lunedì mattina dalla GitHub Action
> `aggiorna-manuale.yml`: se vengono rilevati cambiamenti nei documenti ufficiali AGID/Designers Italia
> o nuove versioni di Bootstrap Italia, viene aperta un'Issue sul repository con la checklist
> dei punti da verificare. Vedi **Parte 7** per dettagli.

> **Changelog 2.4 (2026-04-24)**
> - **Parte 4.8**: documentata la nuova struttura didattica completa dei **4 kit scuola** (`content/formazione/kit-scuola-*.md`) — ampliati dopo feedback positivi dei docenti che hanno richiesto maggiore chiarezza e completezza. Ogni kit include ora riferimenti normativi espliciti (L. 92/2019, Linee guida 2020/2024, art. 18 D.Lgs. 1/2018), obiettivi formalizzati (conoscenze/abilità/competenze chiave europee), tabelle per disciplina, rubriche di valutazione, schede fotocopiabili, adattamenti per BES/DSA/L2, raccordo con il Piano di Emergenza scolastico, coinvolgimento delle famiglie e FAQ del docente.
> - Per la secondaria II grado: aggiunto percorso **PCTO strutturato** (30-50h) e tre temi pluridisciplinari per l'**Esame di Stato**.
>
> **Changelog 2.3 (2026-04-22)**
> - **Parte 11**: aggiunto **X (Twitter)** come canale autonomo, completati i template per tutti i canali, generalizzata la checklist, aggiunto il **Referente comunicazione** e le regole contro engagement bait, gestione post con errore, archivio screenshot.
> - **Parte 12**: introdotto l'**holding statement** nei primi 15 minuti di emergenza, riscritti i template emergenziali in voce attiva, aggiunta la sezione sul ritorno alla normalità comunicativa.
> - Aggiunta **Parte 13** — Social Media Policy pubblica, con la pagina istituzionale collegata in `content/social-media-policy/`.
> - Dichiarata esplicitamente la licenza **CC BY 4.0** per i contenuti pubblicati sui canali social (coerente con le note legali del sito).
> - Corrette incongruenze interne: uso della voce attiva nei comunicati, coerenza cross-canale, rimozione riferimenti a script non esistenti.
>
> **Changelog 2.2 (2026-04-21)**
> - Aggiunta **Parte 11** — Testi per i social (Instagram, Facebook collegato, Telegram).
> - Aggiunta **Parte 12** — Comunicati stampa (tempo ordinario e tempo emergenziale).
> - Introdotta la **palette ufficiale di hashtag** e le formule di rimando al sito.
> - Definito il blocco firma istituzionale per i comunicati, con varianti per coordinatore e sindaco.
> - Stabilito che i comunicati stampa vengono archiviati come articoli in `content/comunicazioni/`.
>
> **Changelog 2.1 (2026-04-21)**
> - Aggiunta **Parte 8** — Modificare e cancellare contenuti (articoli, pagine, redirect).
> - Aggiunta **Parte 9** — File dati `data/` (modalità emergenza, allerta meteo, card rischi, ecc.).
> - Aggiunta **Parte 10** — GitHub Actions e automazioni (tutti gli 8 workflow documentati).
> - Documentato il comportamento del **render-link hook**: link interni verso pagine non ancora
>   buildate (articoli con data futura) vengono resi come testo inerte, non più come anchor rotti.
> - Aggiornato elenco rischi (9 card) e numeri utili nel riferimento.

---

## Indice

- [Parte 0 — Come usare questo manuale](#parte-0--come-usare-questo-manuale)
- [Parte 1 — Scrivere un articolo passo per passo](#parte-1--scrivere-un-articolo-passo-per-passo)
- [Parte 2 — Le regole AGID in dettaglio](#parte-2--le-regole-agid-in-dettaglio)
- [Parte 3 — Immagini per gli articoli](#parte-3--immagini-per-gli-articoli)
- [Parte 4 — Scrivere una pagina (diverso da articolo)](#parte-4--scrivere-una-pagina-diverso-da-articolo)
- [Parte 5 — Checklist pre-pubblicazione](#parte-5--checklist-pre-pubblicazione)
- [Parte 6 — Procedura di aggiornamento manuale](#parte-6--procedura-di-aggiornamento-manuale)
- [Parte 7 — Aggiornamento automatico settimanale](#parte-7--aggiornamento-automatico-settimanale)
- [Parte 8 — Modificare e cancellare contenuti](#parte-8--modificare-e-cancellare-contenuti)
- [Parte 9 — File dati `data/` e stati del sito](#parte-9--file-dati-data-e-stati-del-sito)
- [Parte 10 — GitHub Actions e automazioni](#parte-10--github-actions-e-automazioni)
- [Parte 11 — Testi per i social (Instagram, Facebook, X, Telegram)](#parte-11--testi-per-i-social-instagram-facebook-x-telegram)
- [Parte 12 — Comunicati stampa (tempo ordinario e tempo emergenziale)](#parte-12--comunicati-stampa-tempo-ordinario-e-tempo-emergenziale)
- [Parte 13 — Social Media Policy pubblica](#parte-13--social-media-policy-pubblica)
- [Appendici](#appendici)

---

## Parte 0 — Come usare questo manuale

### A chi è rivolto

- **Redattori umani** del sito (volontari del Gruppo che pubblicano contenuti).
- **AI assistenti** (Claude Code, ChatGPT, Gemini, Copilot) a cui si chiede di redigere articoli o pagine.
- **Chiunque** apra una Pull Request con modifiche a contenuti testuali o immagini.

### Come leggerlo la prima volta

1. Leggi **Parte 0** e **Parte 1** per capire come scrivere un articolo.
2. Scorri **Parte 2** per orientarti sulle regole AGID (puoi tornarci come riferimento).
3. Leggi **Parte 3** prima di preparare immagini.
4. Leggi **Parte 4** solo se devi creare una pagina (non un articolo).
5. Usa **Parte 5** come checklist pratica prima di ogni pubblicazione.

### Come usarlo con un'AI esterna (ChatGPT, Gemini, Claude.ai, ecc.)

Copia e incolla queste **tre parti** come prompt iniziale:

1. Tutta la **Parte 1** (procedura articolo)
2. Tutta la **Parte 2** (regole AGID)
3. La **checklist Parte 5**

Aggiungi poi la tua richiesta specifica. L'AI deve seguire **rigorosamente** queste istruzioni.

> **ISTRUZIONE PER L'AI:** Prima di redigere, verifica che le date di aggiornamento in cima al manuale
> siano recenti (meno di 3 mesi). Se sono più vecchie, avvisa l'utente che il manuale potrebbe essere
> obsoleto e suggerisci di aggiornarlo tramite Claude Code o attendendo il prossimo check automatico
> settimanale. Se l'utente conferma, prosegui con le regole attuali.

### Versioning

Il manuale segue [semantic versioning](https://semver.org/lang/it/):

- **Major** (es. 1.0 → 2.0): cambio strutturale, nuove sezioni corpose.
- **Minor** (es. 2.0 → 2.1): aggiunta di regole o esempi senza rompere l'esistente.
- **Patch** (es. 2.0 → 2.0.1): correzioni di refusi, aggiornamento link.

Le modifiche sono tracciate nei commit git (`git log MANUALE-SITO.md`).

---

## Parte 1 — Scrivere un articolo passo per passo

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

**`date`** — formato `AAAA-MM-GG`, **senza virgolette**, **senza orario**, **senza timezone**.

- ✅ `date: 2026-05-15`
- ❌ `date: "2026-05-15"` (stringa invece di data)
- ❌ `date: 2026-05-15T10:30:00Z` (formato con timezone — **causa esclusione dalla build Hugo**)
- ❌ `date: 15/05/2026` (formato europeo non supportato)

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

Un articolo ben strutturato ha **tre livelli**:

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

**Da mobile / app cloud:** la sandbox blocca i domini esterni. Lascia `image: ""` e aggiungi UN marker nel frontmatter:
```
# TODO-foto-wikipedia: bash scripts/foto-da-wikipedia.sh "Terremoto del Friuli del 1976" 2026-05-06-friuli-1976
# oppure
# TODO-foto-nasa: bash scripts/foto-da-nasa.sh "Vesuvius volcano" 2026-10-01-vesuvio-spazio
# oppure
# TODO-foto-usgs: bash scripts/foto-da-usgs.sh shakemap us10006g7d 2026-08-24-amatrice-shakemap
```

Al successivo push, il workflow `.github/workflows/scarica-foto-automatica.yml` rileva il marker (whitelist di sicurezza: solo i 3 script noti), esegue il download, popola `image:` + `image_credit:` + `image_source_url:`, rimuove il marker e ri-triggera il deploy. **Tutto automatico.** Se la foto non viene trovata, il workflow apre un'issue di follow-up.

**Per trovare un eventid USGS** (terremoti): cerca su `https://earthquake.usgs.gov/earthquakes/search/` per data/luogo, l'ID compare nell'URL della pagina evento.

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

- L'articolo non appare → controlla `draft: false` e formato data (`AAAA-MM-GG` senza timezone).
- L'immagine non si carica → controlla percorso e nome file (case-sensitive).
- I link interni non funzionano → usa URL relativi (`/contatti/` non `contatti/`).

### Passo 1.13 — Verifica con la checklist AGID

Vai a **Parte 5** e spunta ogni voce. Se qualcosa non è a posto, torna indietro.

### Passo 1.14 — Commit e push

```bash
git add content/comunicazioni/2026-05-15-tuo-articolo.md static/images/2026-05-15-tua-immagine.webp
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

## Parte 2 — Le regole AGID in dettaglio

Queste regole derivano dal **Writing Toolkit di Designers Italia**, dal **Manuale operativo
di design della PA** e dalle integrazioni specifiche per la Protezione Civile.

### 2.1 — I cinque principi del Writing Toolkit

1. **Scrivi per chi legge, non per chi ha scritto la norma.** L'utente non conosce il lessico
   interno della PA. Traduci.
2. **Dì prima le cose importanti.** La piramide rovesciata: conclusione in cima, dettagli
   dopo.
3. **Usa parole comuni.** "Casa" non "abitazione". "Paga" non "effettua il pagamento".
4. **Sii specifico.** "Entro il 15 giugno" non "prossimamente". "Piazza Tommaso Frasconi"
   non "nel centro cittadino".
5. **Rendi il testo scorrevole.** Frasi brevi, paragrafi brevi, titoli descrittivi,
   elenchi puntati.

### 2.2 — Lingua e tono

- **Lingua:** italiano corretto, contemporaneo, senza arcaismi ("ad uopo", "giusta delibera",
  "nelle more di").
- **Tono:** istituzionale, sobrio, rassicurante. Mai enfatico, mai minimizzante, mai
  commerciale.
- **Forma personale:** usa "tu" o "voi" quando ti rivolgi al cittadino, se il contesto lo
  permette. Evita "si prega di", "la S.V.", "il gentile utente".
- **Forma impersonale:** accettabile solo in comunicati ufficiali di routine (es. bandi,
  ordinanze).

### 2.3 — Lunghezza di frasi e paragrafi

| Regola | Dettaglio |
|---|---|
| Frase | Sotto le 20 parole (idealmente 12-15). |
| Paragrafo | 2-4 frasi, un concetto. |
| Testo totale | Articolo breve: 150-400 parole. Articolo lungo: 600-1200 parole. Oltre 1500: dividi in più articoli o sposta in pagina. |

**Come verificare la lunghezza media delle frasi** (opzionale):

Conta i punti nel testo, conta le parole, dividi. Se >20 parole/frase in media, accorcia.

### 2.4 — Voce attiva vs voce passiva

| Voce | Esempio | Quando usarla |
|---|---|---|
| Attiva | "**Scarica** il modulo" | Sempre preferita. Soggetto chiaro, verbo diretto. |
| Passiva | "Il modulo **può essere scaricato**" | Solo se il soggetto è irrilevante o sconosciuto. |

**Esercizio:** se puoi inserire "da [qualcuno]" dopo il verbo, è passiva. Trasformala in attiva.

| Passiva (da evitare) | Attiva (preferita) |
|---|---|
| "Il corso è tenuto dai volontari" | "I volontari tengono il corso" |
| "L'emergenza è gestita dal sindaco" | "Il sindaco gestisce l'emergenza" |
| "Il modulo deve essere compilato" | "Compila il modulo" |

### 2.5 — Nominalizzazioni

Le nominalizzazioni trasformano un verbo in sostantivo ("pagare" → "effettuare il pagamento"):
**evitale**.

| Nominalizzazione (evita) | Verbo diretto (usa) |
|---|---|
| "Effettuare il pagamento" | "Pagare" |
| "Procedere all'iscrizione" | "Iscriversi" |
| "Provvedere alla compilazione" | "Compilare" |
| "Dare comunicazione" | "Comunicare" |
| "Fare richiesta" | "Chiedere" |
| "Prendere visione" | "Leggere", "guardare" |

### 2.6 — Parole comuni vs tecnicismi

| Complesso (evita) | Semplice (usa) |
|---|---|
| Abitazione | Casa |
| Automezzo | Auto, furgone |
| Autorizzare | Permettere |
| Documentazione | Documenti |
| Fruire | Usare, avere |
| Inoltrare | Inviare |
| Modalità | Come, modo |
| Nominativo | Nome |
| Presentarsi | Venire, andare |
| Procedere | Fare, andare |
| Recarsi | Andare |
| Terapia | Cura |
| Ulteriore | Altro |

**Tecnicismi necessari:** ammessi se indispensabili, spiegati alla prima occorrenza.

Esempio:

> La trasmissione usa la modalità **NVIS** (Near Vertical Incidence Skywave, propagazione
> quasi verticale delle onde radio), utile per comunicazioni locali senza ripetitori.

### 2.7 — Parole straniere

- **Ammesse** se entrate nell'uso comune (computer, email, online, email, web, chat).
- **In corsivo** se tecniche o poco comuni (*briefing*, *debriefing*, *workshop*).
- **Non declinare** al plurale italiano: "i tablet" non "i tablets", "i file" non "i files".

### 2.8 — Acronimi e sigle

Principio: **evitali se puoi**. Se sono necessari:

1. Prima occorrenza: nome per esteso + acronimo tra parentesi.
2. Da lì in poi: solo l'acronimo.

**Esempio:**

> Il Centro Operativo Comunale (COC) è attivato dal sindaco.
> Il COC coordina le squadre operative sul territorio.

**Sigle senza scioglimento** (ammesse): PA, UE, IVA, SPID, PEC, RC auto.

**Sigle interne** (richiedono scioglimento): DPC (Dipartimento della Protezione Civile),
COC, NUE 112, VVF, CRI, AIB.

### 2.9 — Maiuscole e minuscole

**Regola generale AGID:** uso restrittivo delle maiuscole.

| Categoria | Corretto | Evitare |
|---|---|---|
| Cariche istituzionali | sindaco, assessore, ministro | Sindaco, Assessore, Ministro |
| Eccezioni (tradizione) | Presidente della Repubblica | presidente della Repubblica |
| Ministeri | Ministero della difesa | Ministero della Difesa |
| Dipartimenti | Dipartimento della protezione civile | Dipartimento della Protezione Civile |
| Giorni della settimana | lunedì, martedì | Lunedì, Martedì |
| Mesi | gennaio, febbraio | Gennaio, Febbraio |
| Nomi propri | Regione Lazio | REGIONE LAZIO |
| Nomi di legge | Legge 4/2004, Codice di Protezione Civile | LEGGE 4/2004 |

**Nel dubbio, minuscola.**

### 2.10 — Numeri

| Regola | Esempio |
|---|---|
| Da 1 a 9 nel testo | in lettere ("tre volontari") |
| Da 10 in su | in cifre ("25 volontari") |
| All'inizio di frase | sempre in lettere ("Venti volontari sono arrivati") |
| Grandi numeri | separatore puntuale ("1.200" non "1,200" né "1 200") |
| Separatore decimale | virgola ("2,5 metri") |
| Numeri romani | per leggi e secoli ("Titolo V", "XXI secolo") |

### 2.11 — Date e orari

**Date nel testo (rivolto al cittadino):**

- Esteso: "lunedì 15 maggio 2026"
- Medio: "15 maggio 2026"
- Mese in **minuscolo**.
- Niente "il gg/mm/aaaa".

**Date nei dati tecnici (tabelle, liste):**

- ISO: "2026-05-15"

**Orari:**

- Formato 24 ore: "09:30", "23:45"
- Senza zero iniziale nel parlato: "le 9", "le 23"
- "Dalle 9 alle 12" (niente trattino spaziato: "dalle 9 – alle 12")

### 2.12 — Numeri di telefono

Formato leggibile, a gruppi:

- Fisso italiano: **06 9362 600** o **06 9362600** (non "069362600")
- Cellulare: **+39 333 123 4567**
- Numero unico: **112** (tre cifre, nessun prefisso)

**Nel link `tel:`** (HTML): `tel:+39069362600` (senza spazi, con prefisso internazionale).

### 2.13 — Indirizzi

- Via/Piazza con iniziale maiuscola: "Via Sicilia", "Piazza Tommaso Frasconi"
- Civico con cifra: "Via Sicilia, 13-15"
- CAP e città: "00045 Genzano di Roma (RM)"
- Completo: "Via Sicilia, 13-15 — 00045 Genzano di Roma (RM)"

### 2.14 — Unità di misura

- Ambito tecnico: cifra + simbolo SI con spazio: "3 km", "25 °C", "100 kg"
- Ambito discorsivo: in lettere per quantità piccole: "tre chilometri", "venticinque gradi"
- Simbolo °C (Celsius): niente spazio prima del °, spazio prima della cifra: "25 °C" non
  "25°C" né "25 ° C"

### 2.15 — Link

**Regola d'oro:** il testo del link deve essere **descrittivo anche fuori contesto**.

| Buono | Cattivo |
|---|---|
| "Consulta il [bollettino del Centro Funzionale Regionale Lazio](url)" | "Consulta il bollettino [qui](url)" |
| "Scarica il [modulo di iscrizione (PDF, 120 KB)](url)" | "Scarica il modulo [cliccando qui](url)" |
| "Leggi l'[ordinanza sindacale 42/2026](url)" | "[Leggi di più](url)" |

**Link a documenti:** sempre indicare tipo e dimensione: `(PDF, 120 KB)`, `(DOCX, 50 KB)`.

**Link esterni:** segnalare se aprono nuova finestra (il render hook del sito lo fa automaticamente).

### 2.16 — Grassetto, corsivo, sottolineato

| Formato | Quando |
|---|---|
| **Grassetto** | Parola chiave o frase breve (max una riga) che vuoi risaltare. Mai paragrafi interi. |
| *Corsivo* | Titoli di opere, parole straniere non comuni, termini tecnici alla prima occorrenza, citazioni brevi. |
| Sottolineato | **Mai.** Online indica un link. Usa altri formati. |
| MAIUSCOLO | Mai in testo corrente. Solo sigle ammesse (PA, UE). |

### 2.17 — Elenchi puntati e numerati

**Puntati** (`-` o `*`): quando l'ordine non conta.

- Voci parallele (tutte sostantivi, o tutte azioni, o tutte descrizioni).
- Frasi brevi: niente punto finale se sono frammenti, punto finale se sono frasi complete.
- Almeno 3 voci. Sotto le 3 scrivi un paragrafo.

**Numerati** (`1.`, `2.`): quando l'ordine **conta** (procedure, passaggi, priorità).

**Divieti:**

- Non spezzare una frase continua in un elenco puntato (es. "Il gruppo è composto da: -
  volontari - autisti - responsabili"). Scrivi la frase.
- Niente elenchi a mezza pagina di una-parola.

### 2.18 — Tabelle

- Poche colonne (2-4 massimo su mobile).
- Poco testo per cella (sotto le 15 parole).
- Intestazioni di colonna chiare (prima riga in `**grassetto**`).
- Niente tabelle solo per "impaginare" (usa liste o sezioni).

### 2.19 — Citazioni e riferimenti normativi

**Citazioni testuali:** blockquote Markdown (`>`):

```markdown
> «Grazie all'acquisto e la consegna dei nuovi defibrillatori la Regione Lazio porta
> a compimento l'importante percorso avviato per rafforzare le competenze dei nostri
> volontari in materia di primo soccorso.»
>
> — *Pasquale Ciacciarelli, Assessore alla Protezione Civile della Regione Lazio*
```

**Riferimenti normativi:**

- **Spiega il contenuto** della norma in linguaggio semplice.
- Non citare articoli/commi nel corpo ("art. 20 comma 2...").
- Linka sempre a Normattiva o Gazzetta Ufficiale.

Esempio:

> La legge 4/2004 (Legge Stanca) stabilisce che i siti della pubblica amministrazione
> devono essere accessibili a tutte le persone, comprese quelle con disabilità.

Non:

> Ai sensi dell'art. 3, comma 1, lettera c) della Legge 9 gennaio 2004, n. 4 e ss.mm.ii.,
> in combinato disposto con il D.Lgs. 106/2018...

### 2.20 — Linguaggio inclusivo

- Evita il maschile "neutro" quando puoi: "le persone" > "gli uomini"; "chi si iscrive" >
  "l'iscritto".
- Niente asterischi, schwa (ə) o altre sperimentazioni grafiche: non accessibili agli
  screen reader e non previsti dalle linee guida AGID.
- Se devi nominare esplicitamente entrambi i generi, alterna o usa forme ellittiche:
  "volontari e volontarie", "chi è interessato".

### 2.21 — Accessibilità cognitiva

- **Titoli e sottotitoli** che descrivono il contenuto della sezione.
- **Prima le informazioni importanti**, poi i dettagli.
- **Feedback comprensibili** senza esperienza tecnica.
- **Consistenza**: usa sempre gli stessi nomi per le stesse cose (es. "squadra operativa"
  sempre, non alternato con "team operativo" o "gruppo operativo").

### 2.22 — Regole specifiche Protezione Civile

| Regola | Dettaglio |
|---|---|
| Allerte meteo | Solo dati del Centro Funzionale Regionale Lazio. Fonte sempre citata. |
| Codici colore | Verde, gialla, arancione, rossa. Non usare "massima allerta" per fenomeni ordinari. |
| Previsto vs in corso | "È previsto" (futuro) vs "è in corso" (presente). Non confondere. |
| Allerta vs emergenza | Allerta = preavviso, emergenza = evento in atto. |
| Numeri | Nel Lazio il cittadino chiama **solo il 112** (NUE). Altri riferimenti: 803 555 (Sala Operativa PC Lazio), 1530 (Guardia Costiera). |
| Tono | Calmo, informativo, rassicurante. Mai allarmistico. Mai minimizzante. |
| Autoprotezione | Per i comportamenti, cita sempre fonti ufficiali (DPC, Regione, Comune). |

---

## Parte 3 — Immagini per gli articoli

### 3.1 — Tipologie

| Tipo | Uso | Esempio |
|---|---|---|
| Foto originale | Resoconti attività, eventi, formazione | Foto dell'esercitazione, foto di gruppo |
| Foto di archivio | Articoli commemorativi, storici | Foto terremoto Aquila 2009 (da archivi pubblici) |
| Infografica | Articoli formativi, prevenzione | Triangolo del fuoco, kit di emergenza |
| Logo / Emblema | Articoli istituzionali | Logo DPC, logo Regione Lazio |
| Default | Articoli senza foto dedicata | `notizia-default.svg` (già in `static/images/`) |

### 3.2 — Diritti d'uso (obbligo)

Prima di pubblicare un'immagine, verifica che tu possa farlo:

- **Foto scattate da te o dal gruppo**: ✅ sempre OK.
- **Foto da banche immagini libere**: OK se sono **Creative Commons 0** (pubblico dominio)
  o CC BY (richiede attribuzione nel corpo dell'articolo).
- **Foto da siti istituzionali** (DPC, Regione, Comune): OK, con attribuzione.
- **Foto da Google Images, Facebook, stampa**: ❌ salvo che non sia chiaramente pubblicata
  con licenza libera. Rischio violazione copyright.

**Banche immagini consigliate (libere):**

- [Unsplash](https://unsplash.com) (CC0, attribuzione facoltativa)
- [Pexels](https://pexels.com) (CC0)
- [Pixabay](https://pixabay.com) (CC0)
- [Wikimedia Commons](https://commons.wikimedia.org) (varie licenze libere, sempre con attribuzione)

### 3.3 — Specifiche tecniche

| Parametro | Valore | Motivo |
|---|---|---|
| Formato | **WebP** (preferito), JPEG accettato, PNG per grafiche senza fotografia | WebP pesa il 30% meno di JPEG a pari qualità |
| Larghezza | **1200 px** (ideale), minimo 800 px | Standard Open Graph; non serve oltre 1200 su siti statici |
| Altezza | Automatica secondo proporzioni | |
| Proporzioni | **16:9** (1200×675) o **3:2** (1200×800), orizzontale | Compatibile con preview social |
| Dimensione file | **Max 200 KB** per WebP, max 300 KB per JPEG | Performance mobile |
| Risoluzione | 72 DPI (web) | Non serve più su monitor |
| Spazio colore | sRGB | Standard web |
| Nome file | `AAAA-MM-GG-descrizione-breve.webp`, minuscolo, trattini | Coerenza con articoli |
| Percorso | `static/images/` | Hugo serve tutto da qui |

**Da evitare:**

- File oltre 500 KB (anche in WebP): rallenta il caricamento su mobile.
- Nomi come `IMG_20260515_083042.webp` o `foto1.webp`: privi di contesto.
- PNG per fotografie: pesano 5-10 volte più di WebP.
- Immagini verticali (meno di 1:1): si troncano nelle preview.

### 3.4 — Come scattare una foto originale

Se fotografi tu o un collega:

- **Orizzontale** (landscape), smartphone ruotato.
- **Luce naturale** possibile. Evita controluce forte.
- **Soggetto centrale** o sulla regola dei terzi.
- **Inquadratura chiara**: non troppi elementi dispersivi.
- **Volti di persone**: chiedi il consenso per la pubblicazione online. Per minori, serve
  consenso scritto dei genitori.
- **Targhe automobili e volti non autorizzati**: offusca (strumento: GIMP, Photoshop, mobile app).

### 3.5 — Come cercare una foto libera

**Esempio: cerchi una foto di un pompiere in azione.**

1. Vai su [Unsplash](https://unsplash.com).
2. Cerca "firefighter action".
3. Apri un risultato, verifica la licenza (Unsplash License = utilizzo libero, anche commerciale).
4. Scarica la versione **Full resolution**.
5. Ridimensiona a 1200 px (vedi Passo 3.7).
6. Aggiungi la fascia blu (vedi 3.8).
7. Comprimi in WebP (vedi 3.9).

### 3.6 — Come editare: strumenti consigliati

Tre alternative, dalla più semplice alla più potente:

#### Canva (online, semplicissimo)

- Gratis con account: [canva.com](https://canva.com)
- Crea un design custom 1200×675 o 1200×800.
- Carica la tua foto, trascinala come sfondo.
- Usa il template "Fascia blu PC Genzano" se esistente, altrimenti creala (vedi 3.8).
- Scarica in PNG o JPG a qualità alta.

#### GIMP (desktop, gratis, potente)

- Gratis: [gimp.org](https://gimp.org)
- Apri la foto, `Immagine → Scala immagine` per portarla a 1200 px.
- Usa un template di fascia blu salvato in `.xcf` (modello GIMP), oppure crea un livello
  nuovo rettangolare in basso e riempilo di #003366.
- Esporta in WebP: `File → Esporta come → nome.webp`, qualità 80%.

#### Photoshop (desktop, a pagamento)

- Abbonamento Adobe Creative Cloud.
- Apri la foto, `Immagine → Dimensione immagine` per 1200 px.
- Usa un'azione registrata per applicare la fascia blu in un clic.
- Esporta con `File → Esporta → Salva per web → WebP`.

### 3.7 — Ridimensionare a 1200 px

#### GIMP

1. `Immagine → Scala immagine`.
2. Larghezza: **1200**, altezza si aggiorna automaticamente.
3. Interpolazione: **LoHalo** o **NoHalo** (ottima qualità).
4. `Scala`.

#### Riga di comando (ImageMagick)

```bash
# Installazione (Ubuntu/Debian)
sudo apt install imagemagick

# Ridimensionamento
convert originale.jpg -resize 1200x output.jpg
```

#### Online (caricare file, pochi clic)

- [Squoosh](https://squoosh.app) — Google, gratis, nessun account.

### 3.8 — Aggiungere la fascia blu istituzionale

Ogni immagine di copertina **deve** avere la fascia blu in basso. Identifica visivamente i
contenuti come ufficiali del Gruppo.

#### Specifiche della fascia

| Parametro | Valore |
|---|---|
| Posizione | In basso, a tutta larghezza |
| Altezza | **15-18% dell'altezza totale** (~105-125 px su immagine 1200×696) |
| Colore sfondo | `#003366` (variabile CSS `--pc-primary`) |
| Opacità sfondo | 85-90% |
| **Riga 1** | `PROTEZIONE CIVILE` |
| Font riga 1 | Sans-serif bold (Arial Black, Montserrat ExtraBold, DM Sans Bold) |
| Dimensione riga 1 | ~28-32 px (su immagine 1200 px larga) |
| Colore riga 1 | `#FFFFFF` |
| **Riga 2** | `Gruppo Comunale Volontari — Genzano di Roma` |
| Font riga 2 | Sans-serif regular (Arial, Montserrat, DM Sans) |
| Dimensione riga 2 | ~14-16 px |
| Colore riga 2 | `#FFFFFF`, opacità ~90% |
| **Logo** | `logo-pc-genzano.png` circolare |
| Dimensione logo | Altezza ~70-80 px, proporzionale |
| Posizione logo | Margine sinistro ~15 px, centrato verticalmente nella fascia |
| Posizione testo | A destra del logo, margine sinistro ~100 px dal bordo |

#### Schema visivo

```
+--------------------------------------------------+
|                                                  |
|              FOTO DELL'ARTICOLO                  |
|                                                  |
|                                                  |
+--------------------------------------------------+
| [LOGO]  PROTEZIONE CIVILE                       |
|         Gruppo Comunale Volontari — Genzano di R.|
+--------------------------------------------------+
  ^^^^    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  Logo    Testo bianco su sfondo #003366
```

#### Come applicarla: 3 metodi

##### Metodo 1 — Canva (più semplice)

1. Apri Canva, crea un design 1200×696.
2. Trascina la foto come sfondo, occupando l'intera area.
3. Aggiungi un **rettangolo** in basso: colore `#003366`, opacità 85%, altezza ~110 px.
4. Inserisci il logo (caricandolo come file personalizzato) a sinistra: altezza 75 px, margine
   sinistro 15 px.
5. Aggiungi testo "PROTEZIONE CIVILE" — bianco, bold, 30 pt.
6. Sotto: "Gruppo Comunale Volontari — Genzano di Roma" — bianco, regular, 15 pt.
7. Scarica in PNG alta qualità.
8. Converti in WebP (vedi 3.9).

##### Metodo 2 — GIMP

1. Apri la foto ridimensionata a 1200 px.
2. Crea un nuovo livello: `Livello → Nuovo livello`, tipo "Trasparenza".
3. Seleziona un rettangolo in basso con `Strumenti → Selezione rettangolare`, altezza ~110 px.
4. Riempi con colore `#003366` (strumento Riempimento).
5. Nel pannello livelli, imposta opacità 85%.
6. Inserisci il logo: `File → Apri come livelli → logo-pc-genzano.png`.
7. Ridimensiona il logo a altezza 75 px (`Livello → Scala livello`).
8. Spostalo a sinistra, centrato verticalmente nella fascia.
9. Aggiungi testo: `Strumenti → Testo`, scrivi "PROTEZIONE CIVILE", font Arial Bold 30 pt,
   bianco. Posizionalo a destra del logo.
10. Aggiungi secondo testo sotto: "Gruppo Comunale Volontari — Genzano di Roma", Arial Regular 15 pt.
11. `Immagine → Appiattisci immagine`.
12. `File → Esporta come → nome.webp` (qualità 80%).

##### Metodo 3 — AI generativa (prompt)

Se usi DALL-E, Midjourney, Canva AI, Photoshop Generative Fill:

> **Prompt:**
> "Aggiungi una fascia orizzontale in basso all'immagine, alta circa il 16% dell'altezza totale.
> Sfondo colore esadecimale #003366 con opacità 85%. A sinistra inserisci il logo circolare
> della Protezione Civile di Genzano di Roma (altezza ~75 px, margine sinistro ~15 px,
> centrato verticalmente). A destra del logo, testo bianco (#FFFFFF) su due righe:
> riga 1 'PROTEZIONE CIVILE' in grassetto maiuscolo grande (~30 px, font sans-serif bold),
> riga 2 'Gruppo Comunale Volontari — Genzano di Roma' in testo normale più piccolo
> (~15 px, font sans-serif regular). L'immagine finale deve essere 1200 px di larghezza
> proporzionata."

##### Metodo 4 — Script `applica-fascia-foto.sh` (raccomandato per le foto fornite dall'utente)

Per le **foto evento** (interventi, esercitazioni, formazione, ricorrenze) fornite in formato
grezzo (JPG/PNG/WebP), il repository include uno script riusabile che applica la fascia blu
in modo automatico e uniforme:

```bash
bash scripts/applica-fascia-foto.sh <file-sorgente> <nome-output-senza-estensione>
```

**Esempi reali:**

```bash
bash scripts/applica-fascia-foto.sh /home/utente/Scaricati/Zamberletti.jpg zamberletti-ritratto-istituzionale
bash scripts/applica-fascia-foto.sh /home/utente/Scaricati/Genzano-alto.jpg 2026-06-23-genzano-infiorata-aerea
```

**Cosa fa lo script:**

1. Ridimensiona la foto sorgente a **1200 px di larghezza** mantenendo il rapporto d'aspetto.
2. Aggiunge sotto la foto una **fascia blu `#003366` alta 100 px**.
3. Compone il **logo PC Genzano** (72×72) a sinistra e il testo istituzionale a due righe
   ("PROTEZIONE CIVILE" + "Gruppo Comunale Volontari — Genzano di Roma") a destra del logo.
4. Esporta come **WebP** qualità 85 (compressione `method=6`) in `static/images/<nome>.webp`.
5. Se il risultato supera i **200 KB** ricomprime automaticamente a qualità 75.

**Requisiti:**

- ImageMagick installato (`apt install imagemagick`).
- Il logo `static/images/logo-pc-genzano.png` deve essere presente (lo è già nel repository).
- I font Liberation (Liberation-Sans, Liberation-Sans-Bold) installati — di default sui sistemi
  Linux Ubuntu/Debian, normalmente disponibili via `apt install fonts-liberation`.

**Perché è raccomandato:**

- Uniformità grafica con tutte le foto precedenti (stessa fascia, stesso logo, stessa tipografia).
- Zero passaggi manuali in Canva/GIMP per il trattamento di routine.
- Nome file di output sotto controllo: passa un nome **diverso dallo slug dell'articolo**
  (vedi Parte 3.13) per evitare che `genera-cover.py` sovrascriva la foto con una copertina
  tipografica.

**Differenza con `scripts/genera-cover.py`:**

| Script | Quando usarlo | Input | Output |
|---|---|---|---|
| `genera-cover.py` | Copertine automatiche tipografiche (gradiente + titolo + badge) | Solo il file `.md` dell'articolo | `static/images/<slug>.webp` |
| `applica-fascia-foto.sh` | Foto evento reali fornite dall'utente | Foto sorgente + nome output | `static/images/<nome>.webp` |

### 3.9 — Convertire in WebP e comprimere

Target: **max 200 KB**.

#### Online (facile)

- [Squoosh](https://squoosh.app): trascina l'immagine, scegli WebP, qualità 75-80%,
  scarica.

#### Riga di comando

```bash
# Installazione
sudo apt install webp

# Conversione
cwebp -q 80 originale.png -o nome.webp

# Verifica dimensione
ls -lh nome.webp
```

Se la dimensione supera 200 KB:

```bash
cwebp -q 70 originale.png -o nome.webp
```

Scendi con la qualità fino a rientrare. Sotto q=60 la qualità inizia a calare visibilmente.

### 3.10 — Alt text (obbligatorio per ogni immagine)

L'alt text è il testo alternativo letto dagli screen reader e mostrato se l'immagine non
carica. È obbligatorio per **accessibilità**.

| Tipo immagine | Alt text |
|---|---|
| Foto informativa | Descrive il soggetto: "Volontari al lavoro nel campo di accoglienza di Fossa dopo il terremoto 2009" |
| Infografica | Descrive il dato principale: "Diagramma del triangolo del fuoco: combustibile, comburente, innesco" |
| Logo | Nome dell'ente: "Logo della Protezione Civile di Genzano di Roma" |
| Ritratto | Nome e ruolo: "Giuseppe Zamberletti, primo Ministro per la Protezione Civile" |
| Puramente decorativa | Alt vuoto: `alt=""` |

**Regole:**

- Mai "Immagine di...", "Foto di...", "Grafica che mostra...".
- Mai ridondante con la didascalia o il testo adiacente.
- Massimo ~120 caratteri.
- In italiano corretto (anche se l'immagine è di fonte estera).

**Nel frontmatter** (immagine di copertina): l'alt text viene generato automaticamente dal
titolo dell'articolo.

**Nel corpo** (immagini inline in Markdown):

```markdown
![Volontari al lavoro a Fossa dopo il terremoto 2009](/images/2009-04-fossa-volontari.webp)
```

Parentesi quadre = alt text, parentesi tonde = URL.

### 3.11 — Dove salvare nel repository

```
static/
└── images/
    ├── AAAA-MM-GG-descrizione-articolo.webp   ← immagini di copertina
    ├── logo-pc-genzano.png                     ← logo (non toccare)
    ├── notizia-default.svg                     ← fallback (non toccare)
    └── og-default.png                          ← OG di default (non toccare)
```

### 3.12 — Checklist immagine

- [ ] Formato WebP (preferito) o JPEG/PNG
- [ ] Larghezza 1200 px
- [ ] Proporzioni orizzontali (16:9 o 3:2)
- [ ] Dimensione file sotto 200 KB
- [ ] Fascia blu istituzionale presente
- [ ] Logo PC Genzano nella fascia
- [ ] Testo "PROTEZIONE CIVILE" + "Gruppo Comunale Volontari — Genzano di Roma"
- [ ] Nome file `AAAA-MM-GG-descrizione.webp`
- [ ] Salvata in `static/images/`
- [ ] Diritti di pubblicazione verificati
- [ ] Alt text definito (nel frontmatter o nel Markdown)

### 3.13 — Copertina automatica (tipografica) vs foto evento

Il sito distingue **due tipi** di immagine per articolo:

**1. Copertina automatica (tipografica)** — generata dallo script `scripts/genera-cover.py`
che produce una grafica istituzionale con gradiente blu, titolo dell'articolo, badge
colorato e fascia blu con logo. È associata automaticamente al frontmatter tramite
`scripts/aggiorna-image-frontmatter.py`. Nome file: identico allo slug dell'articolo,
es. `2026-04-15-frana-costone-nemi-chiusura-via-nemorense.webp`.

**2. Foto evento (contenuto redazionale)** — forniscono testimonianza fotografica reale
di un intervento, attività, formazione. Vanno sempre **inserite nel corpo dell'articolo**,
non sostituiscono la copertina.

Regole per le foto evento:
- Nome file: `AAAA-MM-GG-descrizione-specifica.webp`, con descrizione **diversa dallo slug**
  (così `genera-cover.py` non le sovrascrive).
- Devono comunque avere la **fascia blu istituzionale** (vedi Parte 3.8). Per trattarle in
  modo uniforme e rapido usa lo script `scripts/applica-fascia-foto.sh` (Parte 3.8, Metodo 4).
- Si inseriscono con lo shortcode `foto` — mai con markdown `![...]()` diretto.

### 3.14 — Shortcode `foto` (click per ingrandire)

Lo shortcode `foto` inserisce un'immagine nel corpo dell'articolo con click-per-ingrandire
accessibile da tastiera, `<figure>`/`<figcaption>` semantici, alt text obbligatorio e
didascalia opzionale.

**Sintassi:**

```go-html-template
{{< foto src="/images/AAAA-MM-GG-descrizione.webp"
         alt="Descrizione significativa dell'immagine per screen reader"
         caption="Didascalia visibile sotto la foto (opzionale)." >}}
```

**Parametri:**

| Parametro | Obbligatorio | Descrizione |
|---|---|---|
| `src` | sì | Percorso dell'immagine in `/images/...` |
| `alt` | sì | Testo alternativo per screen reader. Mai "immagine di..." |
| `caption` | no | Didascalia visibile. Supporta markdown inline. |

**Comportamento:**

- L'immagine è cliccabile: si apre a dimensione intera in una **nuova scheda**.
- Il link ha `aria-label` descrittivo per screen reader.
- `loading="lazy"` per performance.
- Responsive (`img-fluid` di Bootstrap Italia).
- Nessun JavaScript richiesto: funziona con tastiera, screen reader, e anche con JS
  disattivato.

**Esempio reale:**

```go-html-template
{{< foto src="/images/2026-04-20-incendio-cecchina-casolare-spegnimento.webp"
         alt="Casolare dopo le operazioni di spegnimento a Cecchina"
         caption="Il casolare dopo le operazioni di spegnimento e messa in sicurezza." >}}
```

**Quando usare lo shortcode vs markdown:**

- **Shortcode `foto`**: per tutte le foto evento (interventi, formazione, attività,
  ricorrenze con foto reali). Sempre.
- **Markdown `![alt](src)`**: solo per icone o immagini puramente decorative inline,
  quando non serve l'ingrandimento.

### 3.15 — Tipografia del corpo articolo (`.article-body` v7.2)

Le pagine `single` degli articoli avvolgono il contenuto in
`<article class="article-body">` (template `themes/flavour-pcgenzano/layouts/_default/single.html`).
Il blocco CSS **v7.2** in `themes/flavour-pcgenzano/static/css/custom.css` applica a questo
wrapper una tipografia istituzionale curata che non influisce su homepage, liste, card o widget.

**Cosa applica automaticamente:**

| Elemento | Trattamento |
|---|---|
| Base | `font-size: 1.05rem`, `line-height: 1.75`, colore `#1a1a1a` (contrasto massimo) |
| Primo paragrafo (`lede`) | `font-size: 1.15rem`, colore `#003366`, `font-weight: 500` |
| Capolettera | Prima lettera del primo paragrafo: `3rem`, blu `#003366`, float left |
| `<h2>` | Barra blu `3px` a sinistra, `margin-top: 2.5rem`, colore `#003366`, bold |
| `<h3>` / `<h4>` | Colore `#003366`, peso 600, spaziatura ridotta |
| `<ul>` / `<ol>` | `::marker` blu `#003366`, spaziatura voci `0.4rem` |
| `<blockquote>` | Bordo sinistro blu `4px`, sfondo `#f4f7fb`, corsivo, bordi arrotondati |
| `<figure>` | Max-width `640px`, ombra morbida `rgba(0,51,102,0.12)`, cornice sottile |
| `<figcaption>` | Corsivo blu `#003366`, centrato, `0.925rem` |
| `<a>` (non `.btn`) | Colore blu, `underline` 1 px, 2 px al hover/focus |
| `<table>` | Header blu `#003366` su bianco, zebra leggera `#f8f9fb`, border-collapse |
| `<hr>` | Sfumatura orizzontale blu (decorativa, utile prima di "Riferimenti") |
| `<code>` inline | Sfondo `#f4f7fb`, colore blu, padding 0.1×0.35rem |

**Regole di override integrate:**

- `@media (max-width: 768px)`: riduce il capolettera, comprime le spaziature degli H2, regola
  la dimensione della `lede`.
- `@media (prefers-reduced-motion: reduce)`: disattiva la transizione sull'underline dei link.
- `@media print`: azzera capolettera, ombre, gradienti e sfondi colorati. Mantiene la
  gerarchia visiva in bianco e nero con bordi grigi e colori neutri — il risultato stampato è
  leggibile e sobrio.

**Cosa devi fare tu come redattore:**

- **Niente**: la tipografia si applica automaticamente a qualsiasi articolo in `content/comunicazioni/`.
- **Non introdurre stili inline** nel Markdown (tipo `<span style="color:...">`): il tema li
  sovrascriverà o li renderà incoerenti con la linea visiva.
- **Non usare `<h1>` nel corpo**: il titolo pagina è già `<h1>`, il corpo parte da `<h2>`.
- **Il primo paragrafo conta**: per sfruttare il rendering della *lede* e del capolettera,
  fai in modo che il primo paragrafo sia un vero incipit di senso compiuto (almeno 2 frasi),
  non una singola parola o un'immagine.
- **I `<blockquote>`** sono per **citazioni testuali** (dichiarazioni ufficiali, estratti di
  norme, slogan istituzionali). Non per qualsiasi paragrafo da evidenziare.

**Compatibilità:**

- Conforme **WCAG 2.2 AA**: tutti i colori testo/sfondo superano il rapporto 4.5:1.
- Nessuna informazione veicolata solo dal colore.
- Rispetta `prefers-reduced-motion` e `prefers-contrast` (base Bootstrap Italia).
- Stampa pulita: header/navbar/footer sono già nascosti dal blocco `@media print` globale
  (vedi Parte 1.10).

### 3.16 — Pittogrammi (ISO 7010 + ARASAAC)

Il sito ha una **libreria di 171 pittogrammi standardizzati** per supportare la comprensione del testo a **bambini, anziani, persone con disabilità cognitive e parlanti italiano L2** (regola di accessibilità cognitiva, WCAG 2.2 — sezione 1.4 Distinguishable + 3.1 Readable).

**Cosa contiene la libreria:**

| Tipo | Cartella | Numero | Formato | Fonte / licenza |
|---|---|---|---|---|
| ISO 7010 (sicurezza standard) | `static/pittogrammi/iso7010/` | 46 | SVG vettoriale | Wikimedia Commons (PD-shape / CC0) |
| ARASAAC (comprensione cognitiva) | `static/pittogrammi/arasaac/` | 125 | PNG 500 px | ARASAAC, autore Sergio Palao, CC BY-NC-SA 4.0 |

ISO 7010 copre evacuazione (E*), antincendio (F*), avvertimento (W*), obbligo (M*), divieto (P*).
ARASAAC copre eventi e rischi naturali, azioni di autoprotezione, oggetti del kit di emergenza, persone, luoghi, segnali, veicoli e numeri utili.

**Re-download della libreria** (idempotente, scarica solo i mancanti):

```bash
bash scripts/scarica-pittogrammi.sh           # solo i mancanti
bash scripts/scarica-pittogrammi.sh --force   # ri-scarica tutto
```

Lo script ha un rate-limit di 1 secondo tra le richieste a Wikimedia per evitare ban temporanei.
Per aggiungere nuovi pittogrammi alla libreria, modifica gli array `ISO7010` e `ARASAAC` in cima allo script (formato `codice|nome-file|descrizione`).

**Uso negli articoli e nelle pagine — shortcode `pittogramma`:**

Uso block (figure centrata, con didascalia opzionale):

```go-html-template
{{< pittogramma src="/pittogrammi/arasaac/terremoto.png"
                alt="Pittogramma: terremoto"
                caption="Cosa fare in caso di terremoto"
                size="large" >}}
```

Uso inline (dentro una frase, dimensione adattata al testo):

```go-html-template
Chiama subito il {{< pittogramma src="/pittogrammi/arasaac/112.png" alt="numero 112" inline="true" >}} 112.
```

Parametri:
- `src` (**obbligatorio**) — percorso del pittogramma in `/pittogrammi/iso7010/...` o `/pittogrammi/arasaac/...`
- `alt` (**obbligatorio**) — testo alternativo significativo per screen reader. **Mai stringa vuota**: il pittogramma è esplicativo, non decorativo
- `caption` (opzionale, solo modalità block) — didascalia visibile sotto
- `inline="true"` — inserimento inline dentro una frase (default: block)
- `size` — `small` (48 px), `medium` (96 px, default), `large` (160 px), `xlarge` (240 px)

**Regole editoriali per l'uso dei pittogrammi:**

1. **Mai sostituire il testo con il solo pittogramma**: il pittogramma è di **supporto** alla comprensione, mai sostituto. WCAG 1.4.5 (Images of Text) e principio di leggibilità per L2.
2. **Un pittogramma per concetto chiave**, non come decorazione visiva continua. La sovrabbondanza riduce l'efficacia comunicativa per gli utenti che ne hanno davvero bisogno.
3. **Per segnali di sicurezza** (obblighi, divieti, avvertimenti formali): preferire i simboli **ISO 7010** (riconoscibili a livello internazionale).
4. **Per situazioni narrative o didattiche** rivolte a bambini: preferire **ARASAAC** (colore e tratto più immediati).
5. **Alt text sempre descrittivo**: mai "Immagine di...", "Pittogramma di..." in modo generico. Esempio buono: `alt="Persona che si nasconde sotto al tavolo in caso di terremoto"`.

**Attribuzioni — obbligatorie:**

- Il footer di tutte le pagine linka alla pagina **`/attribuzioni-pittogrammi/`** che riporta autori, licenze e fonti.
- ARASAAC è **CC BY-NC-SA 4.0**: le opere derivate (in particolare le **schede stampabili PDF** dei kit didattici) che includono pittogrammi ARASAAC ereditano automaticamente la stessa licenza CC BY-NC-SA 4.0.
- Quando produci una scheda stampabile che usa pittogrammi ARASAAC, indica nel piè di pagina della scheda: *"Pittogrammi: ARASAAC — Sergio Palao (CC BY-NC-SA 4.0). Distribuita con la stessa licenza."*

**Tecnica e accessibilità:**

- Lo shortcode emette `<img>` con `role="img"` e `loading="lazy"`, oppure `<figure>` con `<figcaption>` opzionale.
- CSS scoped in `themes/flavour-pcgenzano/static/css/custom.css` (sezione **PITTOGRAMMI v1.0**): dimensioni fisse, override mobile (large/xlarge ridotti su <576 px), mantenimento dei colori in stampa (i colori dei segnali ISO 7010 sono parte dell'informazione di sicurezza e non devono essere convertiti in scala di grigi).

---

## Parte 4 — Scrivere una pagina (diverso da articolo)

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

Il menu principale è organizzato come **mega-menu** (Opzione A) in `hugo.toml`: **6 voci di primo livello**, di cui 3 dropdown. La struttura è documentata in dettaglio in `.claude/rules/04-hugo-architecture.md` ma per l'uso quotidiano basta sapere questo.

**Struttura attuale:**

| Voce | Tipo | Contenuto |
|---|---|---|
| Home | diretta | `/` |
| Per il Cittadino ▾ | dropdown | Cosa Fare Adesso, Allerte Meteo, Rischi e Prevenzione, Cartografia, Numeri Utili, Piano Familiare |
| Formazione ▾ | dropdown | Corsi e percorsi scuola, Giochi, Glossario, Schede Stampabili |
| Volontariato ▾ | dropdown | Diventa Volontario, Chi Siamo, Normativa |
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
  weight = 5                    # ordine fra le 6 voci di primo livello
```

**Limite di sicurezza**: non superare 6-7 voci di primo livello per non rompere l'usabilità mobile.

**Pagine statiche (non Hugo)**: lo stesso menu è iniettato sulle 97 pagine HTML in `static/giochi/`, `static/quizpc/`, `static/formazionepc/`, `static/formazione/schede-stampabili/` tramite `static/app-shared/site-chrome.js`. Se modifichi `hugo.toml` e vuoi che il menu nuovo appaia anche lì, **aggiorna in parallelo `site-chrome.js`** (la struttura è la stessa, è una stringa JavaScript concatenata).

### 4.4.1 — Aggiungere l'indice della pagina (TOC)

Per pagine lunghe (oltre 8-10 H2 o oltre ~500 righe Markdown) aggiungi nel frontmatter:

```yaml
toc: true
```

Hugo genera automaticamente un indice cliccabile con badge numerati `01`, `02`, `03`… che porta alle sezioni `##` e `###`. Il bottone "Torna in cima" si trasforma in "Torna all'indice".

Il TOC funziona sia su `single.html` che su `list.html` (sezioni con `_index.md`). Pagine attualmente con TOC: tutte le 26 elencate in `04-hugo-architecture.md` (Formazione + 4 kit, Glossario, Piani, 9 sotto-rischi, Normativa + 7 Capi).

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
| `/formazione/` | `content/formazione/_index.md` | Include 4 kit scuola (vedi 4.8) |
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
| `/formazione/schede-stampabili/` | `static/formazione/schede-stampabili/` | 68 schede HTML A4 stampabili (di cui 10 colorabili) suddivise per fascia (infanzia/primaria/secondaria I/secondaria II) e disciplina (italiano, matematica, scienze, geografia, storia, ed. civica, giornalismo, diritto, economia, inglese) |
| `/english/` ... `/esperanto/` | `content/{lingua}/_index.md` | 7 hub linguistiche curate (vedi §4.11) |

### 4.8 — Kit didattici per le scuole (`content/formazione/kit-scuola-*.md`)

Il sito pubblica **quattro kit didattici** indirizzati alle scuole del territorio, uno per fascia d'età. Dopo un ciclo di feedback positivi dei docenti, i kit sono stati ampliati (aprile 2026) per rispondere alla richiesta di **maggiore chiarezza e profondità** sui temi di protezione civile.

| File | Fascia | Righe | Contenuti chiave |
|---|---|---|---|
| `kit-scuola-infanzia.md` | 3-6 anni | ~410 | Campi di Esperienza, 5 schede fotocopiabili, griglia di osservazione, percorso 4 × 30′ |
| `kit-scuola-primaria.md` | 6-11 anni | ~685 | Raccordo 9 discipline, 3 esperimenti, uscita sul territorio, rubrica 5 competenze |
| `kit-scuola-secondaria-primo-grado.md` | 11-14 anni | ~690 | UdA interdisciplinare, compito di realtà sul Piano di evacuazione, 5 metodologie didattiche |
| `kit-scuola-secondaria-secondo-grado.md` | 14-19 anni | ~800 | PCTO 30-50h, 3 progetti di classe, 3 temi per l'Esame di Stato, rubrica 7×5 livelli |

**Struttura comune a tutti e quattro i kit:**

1. **Riferimenti normativi e curricolari** — Legge 92/2019 (educazione civica), D.M. 35/2020 e Linee guida 2024, art. 18 D.Lgs. 1/2018 (obbligo di informazione e formazione), Indicazioni Nazionali 2012 / Nuovi Scenari 2018 / Nuovi Orientamenti 2024 (infanzia).
2. **Obiettivi di apprendimento formalizzati** — conoscenze, abilità, competenze chiave europee (Racc. UE 2018/C 189/01).
3. **Raccordo con le discipline** — tabella che associa a ciascuna disciplina i traguardi di competenza e gli agganci con il curricolo.
4. **Durata e tabella del percorso** — moduli con obiettivi, attività, materiali, tempi.
5. **Metodologie didattiche** — age-appropriate: gioco simbolico e routine per l'infanzia, laboratori per la primaria, flipped/cooperative/PBL/debate/service learning per le secondarie.
6. **Schede fotocopiabili** (infanzia e primaria) **o compiti di realtà / UdA** (secondarie).
7. **Rubrica di valutazione** — competenze × livelli (4 per infanzia/primaria/secondaria I; 5 livelli D/C/B/A/A+ per secondaria II).
8. **Adattamenti per l'inclusione** — DSA, BES, disabilità intellettiva/sensoriale/motoria, italiano L2, plusdotati.
9. **Raccordo con il Piano di Emergenza scolastico** — D.M. 26/08/1992, D.Lgs. 81/2008, DVR (secondaria II).
10. **Coinvolgimento delle famiglie** — lettere informative, compiti a casa, evento finale.
11. **FAQ del docente** — 7-9 domande frequenti con risposte operative.
12. **Fonti normative e bibliografia** — normativa citata + letture consigliate (Beck, Jonas, IPCC AR6 per le secondarie).

**Specifiche aggiuntive per fascia:**

- **Infanzia**: percorso in 4 incontri da 30′ (2h totali), Campi di Esperienza coinvolti (Il sé e l'altro; Il corpo e il movimento; Immagini, suoni, colori; I discorsi e le parole; La conoscenza del mondo), schede con il 112 e la "tartaruga" (posizione di riparo antisismica).
- **Primaria**: percorso in 6 moduli + laboratorio + valutazione = 8-10h, 3 esperimenti semplici (modellino frana, gelatina per la scossa sismica, triangolo del fuoco), uscita sul territorio nel raggio di 500m.
- **Secondaria I grado**: 6 moduli da 60′ + UdA "Conoscere il rischio del mio territorio" (12h + 3h lavoro autonomo), approfondimenti cross-disciplinari (Italiano: Buzzati/Calvino; Storia: da Messina 1908 ad Amatrice 2017; Arte: segnaletica D.Lgs. 81/2008; Tecnologia: IT-alert).
- **Secondaria II grado**: percorso fino a 70h totali, PCTO strutturato in 6 fasi con tutor interno/esterno, tre progetti di classe (A: analisi del Piano di evacuazione scolastico; B: mappatura del rischio di quartiere; C: mini campagna "Io non rischio"), tre temi pluridisciplinari per l'Esame di Stato (Rischio e responsabilità; Cambiamento climatico e territorio; Comunicazione, media e cittadinanza).

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

Il sito è scritto in **italiano**, ma offre **versioni curate dal Gruppo** in 7 lingue per turisti e residenti stranieri. La gestione è in due livelli:

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

La pagina `content/cartografia/_index.md` mostra in cima alla sezione una **mappa interattiva** con i 16 punti del Piano di Emergenza Comunale (10 Aree di Attesa, 2 Ammassamento Soccorritori, 4 Aree di Ricovero). La mappa è costruita su tre componenti:

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

---

## Parte 5 — Checklist pre-pubblicazione

### Checklist articolo

**Frontmatter:**

- [ ] `title` presente, chiaro, max ~80 caratteri
- [ ] `date` in formato `AAAA-MM-GG` senza virgolette e senza timezone
- [ ] `description` sotto i 160 caratteri
- [ ] `badge` uno dei valori dalla tabella o nuovo (riceverà colore automatico)
- [ ] `priorita` solo `"normale"` o `"urgente"`
- [ ] `autore` presente
- [ ] `image` o stringa vuota `""`
- [ ] `scadenza` compilata solo se serve, altrimenti `""`
- [ ] `area` compilata se rilevante
- [ ] `allegati` con titolo completo (tipo + dimensione) e URL corretto
- [ ] `draft: false` per pubblicare

**Testo:**

- [ ] Titolo descrittivo, non enfatico
- [ ] Apertura con il fatto principale in grassetto
- [ ] Gerarchia H2/H3 coerente (no salti H2→H4)
- [ ] Frasi sotto le 20 parole in media
- [ ] Voce attiva, pochi passivi
- [ ] Nessuna nominalizzazione evitabile
- [ ] Parole comuni, no burocratese
- [ ] Elenchi puntati per 3+ elementi paralleli
- [ ] Grassetto solo per parole chiave
- [ ] Link con testo descrittivo
- [ ] Numeri di telefono nel formato leggibile (06 9362 600)
- [ ] Date estese nel testo ("15 maggio 2026")
- [ ] Ortografia e grammatica verificate
- [ ] Accenti e apostrofi corretti

**Contenuto:**

- [ ] Fonti citate per dati meteo, allerte, rischi
- [ ] Numeri di emergenza verificati: nel Lazio solo **112** (NUE) per il cittadino, più 803 555 e 1530
- [ ] Nessuna informazione non verificata
- [ ] Linguaggio inclusivo

**Immagine:**

- [ ] Formato WebP, 1200 px, <200 KB
- [ ] Fascia blu con logo e testo istituzionale
- [ ] Nome file `AAAA-MM-GG-descrizione.webp`
- [ ] In `static/images/`
- [ ] Diritti d'uso verificati
- [ ] Alt text significativo

**Tecnica:**

- [ ] Nome file `AAAA-MM-GG-titolo-breve.md` in `content/comunicazioni/`
- [ ] `hugo server -D` non mostra errori
- [ ] Articolo visibile in home e in `/comunicazioni/`
- [ ] Link interni funzionano
- [ ] Mobile-friendly (testa la preview su schermo stretto)

### Checklist pagina

**Frontmatter:**

- [ ] `title` presente e chiaro
- [ ] `description` sotto i 160 caratteri
- [ ] `aliases` se la pagina sostituisce un URL storico
- [ ] `draft: false`

**Testo:** (come per articolo)

**Tecnica:**

- [ ] File in `content/<sezione>/` (`_index.md` per hub, `<slug>.md` per sotto-pagine)
- [ ] Se va nel menu: voce aggiunta in `hugo.toml` con peso corretto
- [ ] URL accessibile in locale (`hugo server`)

### Checklist immagine

Vedi Parte 3.12.

---

## Parte 6 — Procedura di aggiornamento manuale

### Fonti da monitorare

| Fonte | URL | Cosa verificare |
|---|---|---|
| Manuale operativo design PA | [docs.italia.it/italia/designers-italia/manuale-operativo-design-docs/](https://docs.italia.it/italia/designers-italia/manuale-operativo-design-docs/) | Versione, data ultima modifica |
| Writing Toolkit | [designers.italia.it/risorse-per-il-design/writing-toolkit/](https://designers.italia.it/risorse-per-il-design/writing-toolkit/) | Nuove regole di scrittura |
| Linee guida design | [docs.italia.it/italia/designers-italia/design-linee-guida-docs/](https://docs.italia.it/italia/designers-italia/design-linee-guida-docs/) | Versione |
| Bootstrap Italia | [github.com/italia/bootstrap-italia/releases](https://github.com/italia/bootstrap-italia/releases) | Ultima versione stabile |
| AGID Accessibilità | [agid.gov.it/it/design-servizi/accessibilita](https://agid.gov.it/it/design-servizi/accessibilita) | Aggiornamenti normativi |
| Form AGID | [form.agid.gov.it](https://form.agid.gov.it/) | Procedura dichiarazione |

### Quando aggiornare

1. **Automaticamente ogni lunedì** — la GitHub Action settimanale apre un'Issue con i
   documenti da ricontrollare.
2. **Ogni 3 mesi** — in ogni caso, revisione periodica anche senza Issue.
3. **Ad ogni nuova versione** di Bootstrap Italia o del Manuale operativo.
4. **Ad ogni modifica normativa** su accessibilità, privacy, PA digitale.

### Come aggiornare manualmente

1. Apri Claude Code nella cartella del sito.
2. Dì: *"Verifica se le linee guida AGID sono aggiornate e aggiorna il manuale di stile se
   necessario."*
3. Claude Code:
   - Verifica le fonti online.
   - Confronta con le versioni nel manuale.
   - Aggiorna `MANUALE-SITO.md`.
   - Aggiorna le regole in `.claude/rules/02-content-design-pa.md`.
   - Aggiorna eventuali archetype o template.
   - Commit e push.

### Istruzioni per AI esterne (auto-aggiornamento assistito)

> **ISTRUZIONE:** Se questo file ti viene fornito per redigere un articolo, controlla la
> data "Ultimo check linee guida AGID" in cima. Se è più vecchia di 3 mesi rispetto alla data
> odierna, avvisa l'utente con questo messaggio:
>
> *"Il manuale di stile potrebbe essere obsoleto (ultimo aggiornamento: [data]). Ti consiglio
> di aggiornarlo tramite Claude Code o di attendere il prossimo check automatico settimanale.
> Vuoi che prosegua comunque con le regole attuali?"*
>
> Se l'utente conferma, prosegui. Altrimenti, attendi l'aggiornamento.

---

## Parte 7 — Aggiornamento automatico settimanale

Il repository include una **GitHub Action** (`.github/workflows/aggiorna-manuale.yml`)
che ogni **lunedì alle 08:00** (ora italiana) verifica lo stato delle fonti ufficiali e
apre un'**Issue** sul repository con la checklist dei punti da controllare.

### Come funziona

1. La Action fetcha:
   - Le pagine principali di Designers Italia e AGID.
   - L'ultimo release tag di Bootstrap Italia via API GitHub.
2. Calcola un hash SHA-256 del contenuto.
3. Confronta con gli hash memorizzati in `.manuale/sources-hashes.json`.
4. Se qualche hash è cambiato (o se l'Issue settimanale non esiste), apre un'Issue con:
   - Lista delle fonti cambiate.
   - Nuova versione di Bootstrap Italia (se disponibile).
   - Checklist di punti da controllare nel manuale.
5. Aggiorna il file `.manuale/sources-hashes.json` con i nuovi hash.
6. Commit automatico del file hashes (solo quel file).

### Come agire sull'Issue

Quando ricevi la notifica dell'Issue settimanale:

1. Apri l'Issue: contiene link e checklist.
2. Apri Claude Code nella cartella del sito.
3. Dì: *"Aggiorna il manuale di stile con le novità dell'Issue #XX."*
4. Claude legge l'Issue, verifica le fonti, propone le modifiche.
5. Approva le modifiche.
6. Commit e push: l'Issue viene chiusa automaticamente se referenziata nel commit
   (`closes #XX`).

### Come disabilitare temporaneamente

Se non vuoi ricevere Issue settimanali per un periodo:

1. Apri `.github/workflows/aggiorna-manuale.yml`.
2. Commenta la sezione `schedule:` o rimuovi il trigger `schedule`.
3. Commit e push.

Per riattivare: ripristina la sezione.

### Esecuzione manuale

Puoi triggerare la Action a mano:

1. Vai su GitHub → Actions → "Aggiorna manuale di stile".
2. Clicca "Run workflow" → "Run workflow".
3. Attendi ~1 minuto. Se ci sono novità, apparirà una nuova Issue.

---

## Parte 8 — Modificare e cancellare contenuti

Questa parte documenta **come intervenire su contenuti già pubblicati**: correzioni, aggiornamenti, rimozioni, gestione URL storici. Ogni operazione ha effetti su SEO, link interni e cache: seguire le procedure previene pagine 404 e perdita di traffico.

### 8.1 — Modificare un articolo esistente

**Quando farlo:**
- correzione di errori di battitura, grammatica o fattuali;
- aggiornamento con nuovi sviluppi (allerta rientrata, esercitazione conclusa, ecc.);
- completamento di informazioni mancanti;
- aggiornamento allegati.

**Procedura:**

1. Individua l'articolo in `content/comunicazioni/AAAA-MM-GG-slug.md`.
2. Apri il file con un editor che preservi gli accenti UTF-8 e i line-ending Unix.
3. Modifica il contenuto. **Non modificare** `date` e `slug` a meno che non sia proprio necessario (vedi 8.3).
4. Se aggiungi contenuti sostanziali, aggiorna `description` in frontmatter (massimo 160 caratteri).
5. Se cambi la sostanza dell'articolo, aggiungi in coda al corpo un **blocco "Aggiornamento"** con data:

   ```markdown
   ---

   **Aggiornamento del 21 aprile 2026**

   Il testo precedente è stato corretto dopo una nuova comunicazione del Centro Funzionale Regionale.
   ```

6. Verifica in locale con `hugo server -D`.
7. Commit con messaggio chiaro: `Aggiornamento articolo <titolo breve>`.

**Cosa NON fare:**
- Non cambiare il titolo in modo drastico senza coordinarlo con chi ha linkato l'articolo altrove.
- Non eliminare campi frontmatter obbligatori (vedi Parte 1).
- Non aggiungere `draft: true` a un articolo già pubblicato: il cittadino vedrebbe il link rotto. Per ritirare un articolo, vedi 8.4.

### 8.2 — Modificare una pagina statica

Le pagine statiche (`content/<sezione>/_index.md` o sottopagine) si modificano come gli articoli, ma con alcune accortezze in più:

- **Navbar e menu**: se modifichi il titolo (`title`) di una sezione principale, controlla anche la voce di menu in `hugo.toml` (`[[menu.main]]`). I due devono combaciare.
- **Breadcrumb**: Hugo costruisce il breadcrumb dalla gerarchia dei file, non dal `title`. Se rinomini una cartella, aggiorni il breadcrumb di tutte le pagine figlie.
- **URL**: cambiare la cartella di una pagina statica ne cambia l'URL. Prima di farlo, leggi 8.5 sulla gestione degli alias.

### 8.3 — Rinominare un articolo o cambiarne la data

Lo slug di un articolo (la parte finale della URL) deriva dal nome del file, tolta l'estensione `.md`. Esempio: `2026-03-10-esercitazione-castelli.md` → `/comunicazioni/2026-03-10-esercitazione-castelli/`.

**Cambiare lo slug** è un'operazione **critica**: tutti i link esterni all'articolo (social, email, altri siti, motori di ricerca) puntano al vecchio URL. Dopo la rinomina, il vecchio URL restituisce 404.

**Procedura sicura per rinominare:**

1. Rinomina il file: `git mv content/comunicazioni/vecchio-nome.md content/comunicazioni/nuovo-nome.md`.
2. Apri il file rinominato e **aggiungi un alias** nel frontmatter verso il vecchio URL:

   ```yaml
   aliases:
     - /comunicazioni/2026-03-10-esercitazione-castelli/
   ```

3. Hugo genererà una pagina al vecchio URL che redireziona automaticamente al nuovo (redirect HTML con `<meta http-equiv="refresh">`).
4. Verifica in locale che sia il vecchio sia il nuovo URL funzionino.
5. Commit con messaggio: `Rinomina articolo <titolo>, alias di redirect mantenuto`.

**Cambiare la data** cambia lo slug solo se la data è parte del nome del file (ed è sempre il caso per gli articoli di questo sito). Stesse regole: `git mv` + `aliases`.

### 8.4 — Ritirare o cancellare un articolo

Tre scenari distinti, tre procedure diverse.

#### Scenario A — Articolo pubblicato per errore, da togliere subito

Se l'articolo contiene dati non verificati, un errore grave o è stato pubblicato su richiesta e poi revocato:

1. Apri il file in `content/comunicazioni/`.
2. Imposta `draft: true` nel frontmatter **oppure** imposta `expiryDate` a una data passata:

   ```yaml
   expiryDate: 2026-04-21
   ```

3. Commit: `Ritiro articolo <titolo> — motivo: ...`.
4. Al prossimo deploy l'articolo sparisce dal sito. L'URL inizia a restituire 404.

**Nota**: se l'URL era già stato condiviso, restituire 404 è il comportamento corretto (indica "non disponibile"). Non mettere al suo posto un articolo diverso.

#### Scenario B — Articolo obsoleto ma con valore storico

Quando un articolo è vecchio ma qualcuno potrebbe ancora arrivarci via link o motore di ricerca:

1. Lascialo pubblicato.
2. Aggiungi in cima al corpo un avviso:

   ```markdown
   > **Articolo di archivio del <data>.** Le informazioni operative contenute possono essere superate.
   > Per dati aggiornati consulta [Allerte Meteo](/allerte-meteo/) o [Rischi e Prevenzione](/rischi-prevenzione/).
   ```

3. Mantieni intatto il contenuto storico originale, con date e riferimenti dell'epoca.

#### Scenario C — Articolo da rimuovere completamente dal repository

Solo se non ha mai avuto valore o se contiene dati sensibili da eliminare per motivi di privacy/GDPR:

1. `git rm content/comunicazioni/AAAA-MM-GG-slug.md`.
2. Rimuovi anche l'immagine di copertina se non più usata: `git rm static/images/AAAA-MM-GG-slug.webp`.
3. Commit: `Rimozione articolo <titolo> — motivo: richiesta di cancellazione dati`.
4. **Sul sito pubblicato** l'URL restituirà 404 fino al prossimo deploy, poi il file sparirà del tutto.
5. Se c'è un rischio di richieste di cache (es. Google), considera un redirect 301 a un URL simile tramite `aliases:` su un articolo esistente coerente.

**Nota git**: il contenuto rimosso resta nella cronologia git del repository. Per dati che devono sparire anche dalla storia (solo in caso di reale necessità legale) serve `git filter-repo` o una procedura coordinata con GitHub Support: **non** è operazione da fare in autonomia.

### 8.5 — Gestione alias e redirect

Hugo gestisce i redirect lato client tramite il campo `aliases:` nel frontmatter. Quando imposti:

```yaml
aliases:
  - /vecchio-url/
  - /altro-vecchio-url/
```

Hugo genera, per ciascun alias, una pagina HTML minimale con:

```html
<meta http-equiv="refresh" content="0; url=/nuovo-url/">
```

Questo funziona su qualsiasi hosting statico (incluso Aruba) senza bisogno di configurare nulla lato server.

**Quando usare aliases:**
- rinomina di articolo o pagina (vedi 8.3);
- fusione di due pagine in una sola;
- cambio della struttura di una sezione (es. `/volontariato/` → `/diventa-volontario/`).

**Quando NON è il caso:**
- articoli eliminati per dati errati: non vuoi redirezionare a nulla, vuoi un 404 onesto;
- URL di test mai indicizzati.

### 8.6 — Link verso articoli futuri o non ancora pubblicati (render-link hook)

Il tema `flavour-pcgenzano` implementa un **render-link hook** personalizzato in `layouts/_default/_markup/render-link.html` (e copia speculare nel tema) che risolve un problema specifico: link Markdown interni verso pagine non ancora buildate (tipicamente articoli con `date` futura) venivano renderizzati come anchor HTML, restituendo 404 al cittadino.

**Comportamento attuale dell'hook:**

| Tipo di link | Resa HTML |
|---|---|
| Link interno `/...` verso **file statico** (estensione `.pdf`, `.webp`, `.jpg`, `.png`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.zip`, `.mp3`, `.mp4`, `.csv`, `.txt`, `.rtf`, `.svg`, `.gif`, `.jpeg`) | `<a href="/...">testo</a>` — anchor diretto, nessun lookup di pagina |
| Link interno `/...` verso pagina esistente | `<a href="/...">testo</a>` — anchor normale |
| Link interno `/...` verso pagina non trovata (né file statico) | `<span class="text-muted" title="Contenuto non ancora disponibile">testo</span>` — testo inerte |
| Link esterno `http://` o `https://` | `<a href="..." target="_blank" rel="noopener noreferrer">testo</a>` |
| Link `tel:` o `mailto:` | `<a href="..." safeURL>testo</a>` |
| Altri formati (ancore `#...`, relativi, ecc.) | anchor grezzo, nessun controllo |

**Conseguenze per chi scrive:**

- Puoi tranquillamente inserire link markdown verso articoli correlati **anche se non ancora pubblicati**: il giorno in cui l'articolo viene pubblicato, il link diventa attivo automaticamente al deploy successivo.
- I link verso **file statici** in `static/` (es. `/manuali/nome.pdf`, `/images/foto.webp`) sono sempre resi come anchor diretti: il controllo avviene per estensione, non via `site.GetPage`. Quindi un PDF in `static/manuali/` è cliccabile anche se non c'è una pagina Hugo con quell'URL.
- Se un lettore vede testo in grigio muto ("Contenuto non ancora disponibile") significa che l'articolo linkato non esiste (tipo, refuso nello slug, o articolo rimosso). Verifica con `hugo server -D`.
- I link esterni si aprono sempre in nuova scheda con `rel="noopener noreferrer"` per sicurezza.
- Frammenti (`#sezione`) e query string vengono ignorati nella lookup: l'hook controlla solo il path.

**Se devi estendere la lista di estensioni statiche**: modifica la variabile `$staticExts` (slice di stringhe) in entrambi i file `render-link.html` — quello in `layouts/` e quello in `themes/flavour-pcgenzano/layouts/`.

**Quando va aggiornato l'hook**: solo se cambia la struttura degli URL interni o si vuole modificare la modalità di fallback (es. tooltip, icona, classe CSS). Qualsiasi modifica va applicata **in entrambi i file** (`layouts/_default/_markup/render-link.html` e `themes/flavour-pcgenzano/layouts/_default/_markup/render-link.html`) per coerenza.

### 8.7 — Sostituzione immagini di copertina

Le immagini di copertina (in `static/images/AAAA-MM-GG-slug.webp`) possono essere sostituite in due modi.

**Modo A — Stessa versione, file aggiornato** (es. ritocco grafico della fascia blu):

1. Sovrascrivi il file esistente con la nuova versione (stesso nome).
2. `git add static/images/<nomefile>.webp`.
3. Commit: `Aggiornamento grafica copertina <titolo>`.

Non serve cambiare nulla nell'articolo: il path in frontmatter è invariato.

**Modo B — Immagine completamente diversa**:

1. Crea la nuova immagine seguendo le specifiche di Parte 3 (WebP, 1200px, fascia blu).
2. Nominala con lo stesso slug dell'articolo (`AAAA-MM-GG-slug.webp`).
3. `git rm` della vecchia, `git add` della nuova (se lo slug cambia).
4. Aggiorna `image:` nel frontmatter dell'articolo.
5. Verifica che `alt:` sia ancora coerente con la nuova immagine; se non lo è, riscrivilo.

**Cosa NON fare:**
- mai cambiare una foto di copertina che ritrae persone senza verificare il consenso al trattamento dell'immagine (GDPR);
- mai usare immagini da banche dati non libere senza licenza commerciale verificata;
- mai usare immagini generate da AI senza averlo esplicitato in didascalia o in nota editoriale (per trasparenza istituzionale).

---

## Parte 9 — File dati `data/` e stati del sito

I file nella cartella `data/` pilotano comportamenti dinamici del sito **senza toccare i template**. Questa è la strada preferita per aggiornare card, banner, numeri di emergenza, canali social. Tutti i file sono letti da Hugo a build time: modifiche richiedono un nuovo build per comparire online (automatico al push).

### 9.1 — Panoramica dei file dati

| File | Formato | Scopo |
|---|---|---|
| `emergenza.json` | JSON | Attiva/disattiva modalità emergenza sulla home |
| `allerta.json` | JSON | Livello allerta meteo corrente (verde / giallo / arancione / rossa) |
| `risk_cards.yaml` | YAML | 9 card della pagina Rischi e Prevenzione |
| `numeri_utili.yaml` | YAML | Numeri di emergenza mostrati in home, contatti, footer |
| `quick_links.yaml` | YAML | CTA del hero + "Cosa fare in caso di..." + servizi |
| `social_links.yaml` | YAML | Canali social + linktree |
| `codici_colore.yaml` | YAML | Descrizioni colori allertamento (pagina Allerte Meteo) |

Regola d'oro: **prima di creare un nuovo partial o template, verifica se la stessa cosa può essere fatta con un data file**. Questo mantiene il sito manutenibile da chi non conosce Hugo.

### 9.2 — `emergenza.json` (modalità emergenza home)

**Schema completo:**

```json
{
  "attiva": false,
  "tipo": "blu",
  "titolo": "",
  "descrizione": "",
  "link": "",
  "ultimo_aggiornamento": ""
}
```

**Campi:**
- `attiva` *(boolean, obbligatorio)*: `true` attiva la modalità emergenza; `false` la disattiva. Quando è `true` la homepage cambia layout: compare in alto il banner rosso e i numeri di emergenza, l'hero diventa compatto e le notizie scendono più in basso. Vedi `themes/flavour-pcgenzano/layouts/index.html`.
- `tipo` *(string)*: `blu` | `giallo` | `arancione` | `rosso`. Pilota il colore del banner. `rosso` = emergenza massima (terremoto, alluvione in corso, evacuazione). `blu` = informativa istituzionale.
- `titolo` *(string)*: breve, in maiuscoletto o frase istituzionale. Esempi accettabili: "EMERGENZA IN CORSO — RESTATE IN CASA", "EVENTO SISMICO — VERIFICHE IN CORSO".
- `descrizione` *(string)*: una o due frasi brevi. **Niente punto esclamativo**, niente allarmismo gratuito. Indica fonte e azione.
- `link` *(string, opzionale)*: URL a un articolo di dettaglio sul sito o a una pagina istituzionale. Se vuoto, il banner non mostra pulsante.
- `ultimo_aggiornamento` *(string)*: ISO date-time dell'ultimo aggiornamento del banner (compare in piccolo sul banner). Formato consigliato: `2026-04-21T14:30:00+02:00`.

#### Procedura — Attivare la modalità emergenza

1. **Verifica la fonte**: la decisione di attivare la modalità emergenza è del responsabile del Gruppo o del COC, non del redattore. Non attivare mai di propria iniziativa.
2. Apri `data/emergenza.json`.
3. Compila i campi:

   ```json
   {
     "attiva": true,
     "tipo": "arancione",
     "titolo": "ALLERTA METEO ARANCIONE SUI CASTELLI ROMANI",
     "descrizione": "Il Centro Funzionale Regionale prevede piogge intense fino alle 24:00 di mercoledi. Limitare gli spostamenti.",
     "link": "/comunicazioni/2026-04-21-allerta-arancione-castelli/",
     "ultimo_aggiornamento": "2026-04-21T09:15:00+02:00"
   }
   ```

4. Commit: `Attivazione modalità emergenza — allerta arancione`.
5. Push: il sito si aggiorna in 2–3 minuti.
6. **In parallelo**: pubblica l'articolo linkato (vedi Parte 1).

#### Procedura — Disattivare la modalità emergenza

1. Verifica con il responsabile che l'evento sia chiuso.
2. Apri `data/emergenza.json`.
3. Riporta `attiva` a `false`. Svuota gli altri campi (lascia `""` o `"blu"`), per non lasciare residui in repository:

   ```json
   {
     "attiva": false,
     "tipo": "blu",
     "titolo": "",
     "descrizione": "",
     "link": "",
     "ultimo_aggiornamento": ""
   }
   ```

4. Commit: `Chiusura modalità emergenza — allerta rientrata`.
5. Pubblica in parallelo un articolo di aggiornamento operativo ("allerta rientrata, nessuna criticità rilevata").

### 9.3 — `allerta.json` (banner allerta meteo)

**Schema:**

```json
{
  "livello": "verde",
  "titolo": "NESSUNA ALLERTA",
  "descrizione": "Non sono previsti fenomeni significativi sul nostro territorio.",
  "ultimo_aggiornamento": "2026-04-21"
}
```

**Campi:**
- `livello` *(string, obbligatorio)*: `verde` | `gialla` | `arancione` | `rossa`. Pilota colore della barra allerta in cima a ogni pagina.
- `titolo` *(string)*: es. "ALLERTA GIALLA SUI CASTELLI ROMANI".
- `descrizione` *(string)*: una frase sintetica.
- `ultimo_aggiornamento` *(string)*: data in formato `AAAA-MM-GG`.

**Aggiornamento automatico**: il workflow `check-allerta.yml` (vedi Parte 10) interroga il feed ufficiale DPC **ogni ora** e aggiorna `allerta.json` se il livello è cambiato. Nella maggior parte dei casi **non serve intervenire manualmente**.

**Aggiornamento manuale**: serve solo se l'automazione fallisce o se si vuole forzare un messaggio istituzionale specifico. Modifica il file, commit, push. **Nota**: al successivo ciclo orario il workflow sovrascriverà il tuo intervento con il valore letto dal feed DPC. Per evitarlo, disabilita temporaneamente il workflow (vedi 10.9).

**Fonte dati ufficiale**: CSV pubblicato dal Dipartimento Protezione Civile, mirror mantenuto da opendatasicilia: `https://raw.githubusercontent.com/opendatasicilia/DPC-bollettini-criticita-idrogeologica-idraulica/refs/heads/main/data/bollettini/bollettino-oggi-comuni-latest.csv`.

### 9.4 — `risk_cards.yaml` (Rischi e Prevenzione)

Contiene le 9 card mostrate nella pagina hub "Rischi e Prevenzione" e nella homepage. Ogni card rimanda a una sottopagina di `content/rischi-prevenzione/`.

**Schema di ogni card:**

```yaml
- id: "rischio-sismico"
  titolo: "Rischio Sismico"
  icona: "bi-tsunami"
  colore: "warning"
  classe_icona: "si-orange"
  descrizione_breve: "Cosa fare prima, durante e dopo un terremoto."
  peso: 1
```

**Campi:**
- `id`: slug della pagina di dettaglio (`/rischi-prevenzione/<id>/`). Deve esistere in `content/rischi-prevenzione/<id>/_index.md` o `<id>.md`.
- `titolo`: titolo card, coerente con l'H1 della pagina di dettaglio.
- `icona`: nome icona Bootstrap Italia (prefisso `bi-`). Vedi [icons.getbootstrap.com](https://icons.getbootstrap.com/).
- `colore`: variante Bootstrap (`primary`, `warning`, `danger`, `info`, `success`, `dark`). Pilota il bordo/sfondo della card.
- `classe_icona`: classe custom per colorare l'icona (`si-orange`, `si-blue`, `si-teal`, `si-green`, `si-dark`). Definite in `custom.css`.
- `descrizione_breve`: una frase max 100 caratteri.
- `peso`: intero, determina l'ordine di visualizzazione (1 = prima, 9 = ultima).

**Modifiche tipiche:**
- Aggiungere una card nuova: aggiungi blocco YAML + crea la pagina di dettaglio in `content/rischi-prevenzione/<id>.md`. Ricorda di aggiornare l'archivio e il menu se serve.
- Togliere una card: rimuovi il blocco + considera di lasciare la pagina di dettaglio come archivio (vedi 8.4 scenario B) o rimuoverla.
- Riordinare: modifica solo i `peso`.

### 9.5 — `numeri_utili.yaml` (numeri di emergenza)

**Regola chiave**: nel Lazio il **solo numero da comunicare al cittadino è il 112** (NUE). 115, 118, 1515 non sono più il riferimento. Qualunque AI che proponga di aggiungerli come "numeri da chiamare" va corretta.

**Struttura:**

```yaml
emergenza:      # Numeri in evidenza massima
  - numero: "112"
    nome: "Numero Unico Emergenza (NUE)"
    descrizione: "..."
    icona: "bi-telephone-fill"
    principale: true

utili:          # Numeri utili secondari
  - numero: "1530"
    nome: "Guardia Costiera"
    ...

locale:         # Numeri del Gruppo (MAI per emergenze)
  - numero: "+39 06 9362600"
    nome: "Segreteria Gruppo PC Genzano"
    ...
    nota: "NON per emergenze"
```

**Campi:**
- `numero`: formato leggibile con spaziature (`112`, `803 555`, `+39 06 9362600`).
- `nome`: ufficiale del servizio.
- `descrizione`: a cosa serve, una frase.
- `icona`: classe Bootstrap Italia.
- `principale`: se `true`, la card è in evidenza grafica maggiore.
- `nota` (opzionale): testo di avviso (tipicamente "NON per emergenze" per i numeri del Gruppo).

### 9.6 — `quick_links.yaml` (CTA hero + servizi)

Tre sezioni distinte:
- `principali`: pulsanti del hero homepage (tipicamente 3).
- `cosa_fare`: card "Cosa fare in caso di..." in homepage.
- `servizi`: card "Servizi per il cittadino".

Campi comuni: `titolo`, `url`, `icona` (Bootstrap Italia icon), `classe` o `classe_icona`, `descrizione`, opzionalmente `azione` (testo sul pulsante).

Regole:
- Ogni URL deve esistere come pagina nel sito (altrimenti il render-link hook mostra testo inerte solo in contenuti markdown, ma in questi partial i link sono generati direttamente: qui un URL inesistente produce un 404 vero).
- Mantieni numero card coerente con il layout (3 principali, 4 cosa_fare, 4 servizi è la configurazione testata).

### 9.7 — `social_links.yaml`

Lista `canali:` + singolo `linktree:`. Campi per canale: `nome`, `url`, `icona`, `classe_btn`, `aria_label`, `descrizione`.

Aggiungere un canale nuovo: aggiungi blocco + verifica che l'icona Bootstrap Italia esista (`bi-whatsapp`, `bi-youtube`, ecc.). Rimuovere un canale: togli il blocco; i partial che usano `range canali` si adattano.

### 9.8 — `codici_colore.yaml`

Pilota la pagina "Allerte Meteo" sezione "Significato dei colori". Ogni livello ha: `livello` (slug), `titolo`, `colore_bg`, `colore_testo`, `significato`, `cosa_fare`, `icona`. I colori sono coordinati con la palette ufficiale del sistema di allertamento nazionale.

**Non modificare** `colore_bg` e `colore_testo` senza ricontrollare il contrasto WCAG (≥ 4.5:1 testo normale).

### 9.9 — Validazione data files

Prima di commit, verifica:

- **JSON** (`emergenza.json`, `allerta.json`): formato valido. Errori di virgola o virgolette rompono il build. Usa un linter o `python3 -m json.tool < data/emergenza.json`.
- **YAML**: indentazione a 2 spazi, niente tab. Stringhe con caratteri speciali tra virgolette doppie. Usa `python3 -c "import yaml; yaml.safe_load(open('data/risk_cards.yaml'))"`.
- **Caratteri accentati**: sempre UTF-8, mai entità HTML (`è`, non `&egrave;`).

Un `data` rotto blocca `hugo --minify` e il deploy fallisce: il sito resta sulla versione precedente e il monitoring Actions mostra un fallimento rosso.

---

## Parte 10 — GitHub Actions e automazioni

Il repository ha **9 workflow** attivi che automatizzano deploy, controlli, aggiornamenti e audit. Ogni workflow vive in `.github/workflows/*.yml`. Tutti supportano l'esecuzione manuale tramite `workflow_dispatch` dalla tab Actions del repository.

### 10.1 — Panoramica

| Workflow | File | Trigger | Scopo |
|---|---|---|---|
| Build e Deploy | `deploy.yml` | push su `main`, manuale | Build Hugo, deploy Aruba (FTP), deploy GitHub Pages |
| Aggiornamento Allerta Meteo | `check-allerta.yml` | orario (cron `12 * * * *`), manuale | Legge feed DPC, aggiorna `data/allerta.json` |
| Pubblicazione programmata | `pubblica-programmata.yml` | giornaliero (06:00 UTC), manuale | Riavvia il deploy per pubblicare articoli a data futura |
| Audit Accessibilità | `lighthouse-audit.yml` | dopo ogni deploy, manuale | Lighthouse su home e 5 pagine chiave |
| Smoke test post-deploy | `smoke-test-post-deploy.yml` | dopo ogni deploy, manuale | Verifica live di 20 pagine + 7 lingue + 6 mini-app + 11 marker JS + 2 header sicurezza. Logica in `scripts/smoke-test-live.sh` |
| Aggiorna Bootstrap Italia | `update-bootstrap-italia.yml` | lunedì 06:00 UTC, manuale | Verifica nuove release Bootstrap Italia, apre PR |
| Aggiornamento MANUALE | `aggiorna-manuale.yml` | lunedì 06:00 UTC, manuale | Confronta hash fonti AGID/DI, apre Issue se cambiate |
| **Audit completo sito** | `audit-sito.yml` | lunedì 09:00 UTC, manuale | **38 sezioni**: contenuti (1-15) + codice/template (16-22) + governance docs (23-32) + audit aggiuntivo (33-37) + link critici normativa (38). Fuso da `coerenza-docs.yml` + `check-normativa-links.yml` il 26 aprile 2026 |
| Verifica link sito completo | `check-links-sito.yml` | lunedì 10:00 UTC, manuale | Crawl completo con **lychee**: tutti i link interni + esterni del sito, apre issue automatica su 404/drift |

### 10.2 — `deploy.yml` — Build e Deploy

**Trigger**: push su `main`, esecuzione manuale.

**Cosa fa:**
1. Checkout del repository (fetch-depth 0 per ottenere la storia completa).
2. Setup Hugo extended.
3. Build principale con `hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"` (per Aruba).
4. Build secondario con `hugo --minify --baseURL "https://sviluppoitaliadigitale.github.io/sito-pc-genzano/"` (per GitHub Pages).
5. Deploy FTP su Aruba usando i secret `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`.
6. Deploy su GitHub Pages tramite `actions/deploy-pages`.

**Durata tipica**: 2–4 minuti.

**Fallimenti comuni:**
- build Hugo rotto (frontmatter malformato, shortcode non definito, YAML data invalido): il commit va revertito o corretto subito;
- FTP timeout: retry automatico, altrimenti richiede intervento;
- secret scaduto: aggiornare nei Settings del repo.

**Come usarlo manualmente**: Actions → "🚀 Build e Deploy" → Run workflow. Utile per ripubblicare dopo aver corretto un secret o dopo un rollback DNS.

#### Cartelle protette (escluse dal deploy FTP)

Il workflow usa `SamKirkland/FTP-Deploy-Action` con `dangerous-clean-slate: false` e una lista di **esclusioni esplicite**: i file presenti in queste cartelle sul server Aruba **non vengono toccati** dal deploy (né aggiunti, né aggiornati, né rimossi). Sono aree gestite **direttamente sul server** — tipicamente con contenuto storico, caricamenti manuali via FTP o materiali legacy.

```yaml
exclude: |
  **/documenti/**
```

**Storico delle esclusioni (rimosse 24 aprile 2026):** fino al 24 aprile 2026 la lista escludeva anche `**/cartelli/**`, `**/giochi-bambini/**`, `**/formazionepc/**`, `**/quizpc/**`. Dopo l'incidente del cartello AR4 Salesiani — un audit lato utente ha rilevato che il file `ar4.png` era mancante sul server Aruba, ma non c'era modo di accorgersene dal repo perché la cartella era esclusa — queste esclusioni sono state rimosse per eliminare il drift tra repo e server. I cartelli sono stati recuperati dal backup settimanale e ora vivono nel repo come unica fonte di verità.

**Conseguenze operative:**

- Un file messo in `static/documenti/` **non viene caricato su Aruba**: rimane solo nel repository e nella build locale/GitHub Pages. La cartella resta gestita manualmente sul server perché contiene materiale ereditato dal sito precedente (pieghevoli, kit "Io Non Rischio", schede storiche) mai migrato nel repo.
- Per **nuovi PDF o allegati** da depositare via git, usa le cartelle consentite: `static/allegati/AAAA/`, `static/manuali/`, `static/comunicati/AAAA/`.
- Per **nuovi cartelli segnaletici** (aree di attesa, aree di ricovero, aree di ammassamento), usa `static/cartelli/`: ora deployano automaticamente.
- Se vuoi aggiornare un file in `static/documenti/`, devi caricarlo **manualmente via FTP** su Aruba, oppure migrare il contenuto in una cartella del repo e aggiornare i riferimenti.
- Vale lo stesso principio per eventuali cartelle aggiunte alla lista in futuro. Quando modifichi `deploy.yml`, aggiorna **anche questa tabella e la Parte 1.10** del manuale.

### 10.3 — `check-allerta.yml` — Aggiornamento allerta meteo

**Trigger**: cron orario (`12 * * * *`, minuto 12 per evitare picchi), esecuzione manuale.

**Cosa fa:**
1. Scarica il CSV ufficiale del Dipartimento Protezione Civile dal mirror opendatasicilia.
2. Cerca la riga di "Genzano di Roma".
3. Estrae il livello massimo tra `avviso_criticita`, `avviso_idrogeologico`, `avviso_temporali`, `avviso_idraulico`.
4. Se diverso dal livello corrente in `data/allerta.json`, aggiorna il file.
5. Commit automatico dal bot `github-actions[bot]` con messaggio `chore: aggiornamento allerta <livello>`.
6. Il commit su `main` ritriggera `deploy.yml`.

**Permessi**: `contents: write`.

**Quando NON intervenire manualmente**: mai, se non per test. L'automazione è affidabile e le modifiche umane vengono sovrascritte al ciclo successivo.

**Disattivazione temporanea**: commenta la sezione `schedule:` e lascia solo `workflow_dispatch:`. Esempio in caso di manutenzione straordinaria del feed DPC.

### 10.4 — `pubblica-programmata.yml` — Pubblicazione programmata

**Trigger**: cron giornaliero (`0 6 * * *` = 06:00 UTC = 08:00 CEST / 07:00 CET), esecuzione manuale.

**Cosa fa:**
1. Chiama via `workflow_dispatch` il workflow `deploy.yml`.

**Perché esiste**: Hugo esclude dal build gli articoli con `date` futura (comportamento default `buildFuture: false`). Al passaggio di mezzanotte, gli articoli del giorno diventano "pubblicabili" ma il sito resta fermo all'ultimo deploy finché non si fa un nuovo build. Questo workflow garantisce un build quotidiano alle 08:00 del mattino italiano: gli articoli con data = oggi entrano nel sito.

**Nota operativa**: se vuoi pubblicare un articolo **a un'ora specifica** diversa dalle 08:00, lancia manualmente `deploy.yml` dall'interfaccia Actions.

### 10.5 — `lighthouse-audit.yml` — Audit Accessibilità e Performance

**Trigger**: `workflow_run` dopo il successo di `deploy.yml`, esecuzione manuale.

**Cosa fa:**
1. Attende che GitHub Pages propaghi (pochi secondi).
2. Esegue Lighthouse CI su un set di URL chiave (home, rischi, allerte, contatti, un articolo recente).
3. Produce un report scaricabile come artifact.
4. Se i punteggi scendono sotto soglia (tipicamente 90 performance, 95 accessibilità, 100 best-practices), apre una Issue.

**Quando guardarlo**: quando un deploy produce una Issue di regressione. Le cause più frequenti sono immagini non ottimizzate, nuovi script bloccanti, contrasti troppo bassi.

### 10.6 — `update-bootstrap-italia.yml` — Aggiornamento Bootstrap Italia

**Trigger**: cron settimanale (lunedì 06:00 UTC), manuale.

**Cosa fa:**
1. Interroga la release più recente del repository `italia/bootstrap-italia`.
2. Confronta con la versione usata nel sito (nel template base `layouts/_default/baseof.html` o nel config).
3. Se c'è una nuova release, apre una PR con l'aggiornamento del riferimento CDN/asset e un commento con il changelog ufficiale.

**Permessi**: `contents: write`.

**Cosa fare quando apre una PR:**
1. Leggi il changelog della release (linkato nella PR).
2. Esegui `hugo server` in locale dopo il merge di prova per verificare che non ci siano breaking changes.
3. Testa manualmente: navbar, hero, card, form, alert, footer.
4. Lancia `lighthouse-audit.yml` manuale per confermare che accessibilità/performance non regrediscono.
5. Approva e fai merge.

**Quando rifiutare una PR**: major version bump (es. da 2.x a 3.x) richiede review completa del tema — non approvare automaticamente.

### 10.7 — `aggiorna-manuale.yml` — Verifica fonti AGID/Designers Italia

**Trigger**: cron settimanale (lunedì 06:00 UTC), manuale.

**Cosa fa:**
1. Scarica (con `curl`) le pagine ufficiali AGID / Designers Italia / Writing Toolkit / WCAG indicate nella configurazione del workflow.
2. Calcola hash SHA-256 del contenuto.
3. Confronta con gli hash salvati nel repository (commit precedente).
4. Se uno o più hash sono cambiati, apre una Issue con:
   - elenco delle pagine cambiate;
   - checklist di revisione ("confronta la sezione X del manuale con la nuova versione della pagina Y");
   - link alla pagina ufficiale aggiornata.

**Permessi**: `contents: write`, `issues: write`.

**Cosa fare quando apre una Issue:**
1. Apri la pagina ufficiale aggiornata.
2. Confronta con la Parte rilevante di `MANUALE-SITO.md` e con i file in `.claude/rules/`.
3. Aggiorna testo del manuale e/o delle regole se necessario.
4. Aggiorna il campo "Ultimo check linee guida AGID" in testa al manuale.
5. Commit + push, chiudi la Issue con un commento che cita il commit.

### 10.8 — `audit-sito.yml` — Audit completo settimanale (38 sezioni)

**Trigger**: cron settimanale (lunedì 09:00 UTC), manuale.

**Storia**: nato ad aprile 2026 con 15 controlli sui contenuti, esteso il 26 aprile 2026 a 32 controlli inglobando `coerenza-docs.yml` (lun 07:00). Lo stesso giorno esteso a 37 con il blocco "audit aggiuntivo" (mixed content, accessibility alt, coerenza traduzioni, hugo.toml ↔ data files, smoke test rendering) e a 38 inglobando anche `check-normativa-links.yml` (lun 08:00) come sezione 38 dedicata ai link critici con messaggi specifici. **Risultato: -2 workflow, 1 issue settimanale invece di 3, stessa copertura.**

**Cosa fa:** scansiona il sito completo per rilevare automaticamente la stessa classe di errori che emerse dagli audit manuali di aprile 2026 — COI 14°→15°, cartello AR4 mancante, citazioni di 115/118 come numero da chiamare, duplicate target paths sulle 7 lingue, articoli `draft:true` dimenticati con data passata, link interni a slug typo, residui di refactoring (CCV-MB, manuale lombardo), `/index.html` reintrodotti dopo il fix Chrome cache. Apre **una sola issue settimanale** se trova deviazioni.

**32 controlli effettuati** — divisi in 3 macro-aree:

#### Contenuti pubblicati (sezioni 1-15)
1. **COI** — riferimenti al 15° Centro Operativo Intercomunale (errore se grado diverso).
2. **NUE 112** — nessuna istruzione a chiamare 115/118/1515 (esclude usi legittimi tipo "ARES 118" come nome organizzazione, "Non chiamare il 115" didattico).
3. **Telefono istituzionale coerente** — cifre da `hugo.toml` confrontate con tutto il sito; `href="tel:"` senza spazi (RFC 3966 E.164).
4. **Sede e CAP** — warning su CAP ≠ `00045` accanto a "Genzano".
5. **Placeholder** — `TODO`, `TBD`, `FIXME`, `XXX`, `lorem ipsum`, `DA COMPLETARE`, template Go non espansi.
6. **File statici** — `src`, `href`, `url:` puntano a file esistenti in `static/`.
7. **Badge** — usati negli articoli devono essere in `badge.html` (case-insensitive).
8. **Anno articoli** — fuori `2020..anno_corrente+1` = typo.
9. **Allegati senza dimensione** (WCAG 3.3.5).
10. **Frasi AGID** — euristica: ≥3 frasi >40 parole = warning.
11. **Pagine `_index.md` con `draft:true`** (sparirebbero dal sito).
12. **Schede stampabili linkate** ma file HTML mancante.
13. **Modalità emergenza** attiva da troppo tempo (>14 giorni senza aggiornamento = probabile dimenticanza).
14. **Pagine legali con `dataUltimaRevisione` >18 mesi** (rivedere il contenuto).
15. **ID widget duplicati** nella stessa pagina (rompono il bottone "Carica").

#### Codice e template (sezioni 16-22)
16. **Hugo build pulito** — `hugo --minify --printPathWarnings` non emette warning di rilievo (es. duplicate target paths sulle 7 lingue come è successo ad aprile 2026).
17. **Articoli `draft:true`** — regola del progetto: nessun articolo in revisione, solo immediato o calendarizzato (`draft:false` + data futura).
18. **Link interni a slug inesistenti** — rileva typo o slug rinominati post-creazione (es. `chiamare-112-correttamente` vs `segnalare-emergenze-112-come-fare`).
19. **Sintassi JavaScript** — `node --check` su tutti i `.js` standalone in `static/` (giochi, quiz, scenari, mappa, abili-a-proteggere).
20. **Validità YAML workflow** — `python3 yaml.safe_load` su ogni `.github/workflows/*.yml` per intercettare il pattern velenoso heredoc-Python (vedi `.claude/rules/05-github-aruba-deploy.md` § "qualità YAML").
21. **Path assoluti nei template** — `href="/..."` hardcoded che funziona su Aruba ma è rotto su GitHub Pages (subpath). Tutti i path interni devono usare `relURL` / `absURL`.
22. **Residui di refactoring** — `/index.html`, `intercomunale lombarda`, `Imbersago`, `CCV-MB`, `Monza-Brianza`. Implementa la regola `.claude/rules/07-proattivita-coerenza.md`: dopo un fix di pattern, sweep continuo per evitare reintroduzioni.

#### Governance docs (sezioni 23-32)
23. **File di governance** esistenti (`CLAUDE.md`, `MANUALE-SITO.md`, `PIANO-EDITORIALE.md`, archetypes, 7 rule files).
24. **Import `@.claude/rules/*.md`** in `CLAUDE.md` puntano a file esistenti.
25. **Badge list coerente** fra `badge.html`, `CLAUDE.md`, `rule 02`, `archetypes/comunicazioni.md` (la fonte di verità è `badge.html`, le altre devono allinearsi).
26. **Formato data articoli** — solo `AAAA-MM-GG`, mai `AAAA-MM-DDTHH:MM:SSZ` (Hugo escluderebbe l'articolo dal build).
27. **Frontmatter completo** — campi obbligatori `title date description badge priorita autore draft` presenti in ogni articolo.
28. **Riferimenti incrociati** in `CLAUDE.md` verso `MANUALE-SITO.md`, `PIANO-EDITORIALE.md`, workflow `aggiorna-manuale.yml`.
29. **Pagine `_index.md` istituzionali** (19 pagine obbligatorie: privacy, note-legali, accessibilità, social-media-policy, contatti, ecc.).
30. **Shortcode `foto`** presente in `themes/.../shortcodes/` e documentato in `MANUALE-SITO.md` e `rule 02`.
31. **Script `scripts/export-contesto-ai.sh`** presente ed eseguibile (`chmod +x`).
32. **`dataUltimaRevisione`** sulle 4 pagine legali in formato `AAAA-MM-GG` tra virgolette.

#### Audit aggiuntivo (sezioni 33-37)
33. **Mixed content** — link `http://` esterni nelle pagine HTTPS (warning per browser moderni). Eccezioni note: `parcocastelliromani.it`, `idrografico.roma.it`, `zonesismiche.mi.ingv.it` (siti senza HTTPS lato fornitore).
34. **`image_alt` accessibility** (WCAG 1.1.1) — articoli con `image:` ma `image_alt` vuoto o mancante. Screen reader leggerebbero il filename.
35. **Coerenza dati istituzionali nelle 7 traduzioni** — pagine `content/{english,deutsch,espanol,francais,portugues,romana,esperanto}/numeri-utili/_index.md` devono contenere sede ("Sicilia"), CAP "00045", numero "112". Se uno manca = traduzione non aggiornata.
36. **Coerenza `hugo.toml` ↔ `data/numeri_utili.yaml`** — il telefono di sede in `hugo.toml` deve essere presente nel record "locale" del yaml (alimenta la card Numeri Utili).
37. **Smoke test rendering** — verifica che le 12 pagine critiche generate (`public/index.html`, `cosa-fare-adesso`, `numeri-utili`, `contatti`, `cartografia`, `assistente`, `comunicazioni`, `formazione`, `rischi-prevenzione`, `diventa-volontario`, `area-download`, `faq`) abbiano un `<h1>` (cattura rendering rotto / frontmatter sbagliato che Hugo non sempre segnala).
38. **Link critici (normativa, PDF locali, Normattiva)** — sentinella veloce con messaggi specifici sugli 8 link che, se cadono, vanno individuati subito perché compaiono in più pagine: 2 portali ufficiali (Lazio Agenzia PC, DPC normativa nazionale), 4 PDF locali sul server Aruba (Piano Emergenza Comunale, Ordinanza AIB 2025, Piano AIB Lazio, Piano Triennale Lazio) gestiti manualmente in `/documenti/`, 2 link Normattiva (D.Lgs. 1/2018 Codice PC, L. 353/2000 incendi boschivi). Lychee farà comunque il crawl completo lun 10:00 ma con output generico; questa sezione apre l'issue settimanale dell'audit con il nome del documento rotto. Sostituisce il workflow `check-normativa-links.yml` precedente (lun 08:00).

**Formato Issue:** report markdown con 38 sezioni numerate. `❌` = errore (da correggere prima del prossimo deploy), `⚠️` = warning (valutare se falso positivo). Label issue: `audit`, `qualità-testi`, `manutenzione`.

**Quando intervenire:** ogni volta che apre una Issue. Il workflow è tarato per essere conservativo (pochi falsi positivi). Se un warning ricorrente è un falso positivo legittimo (es. una citazione lunga, un articolo intenzionalmente con anno fuori range), aggiungi un'eccezione mirata al workflow così la segnalazione non si ripete.

**Perché esiste:** gli audit manuali di aprile 2026 hanno trovato errori che convivevano da tempo nel sito senza che nessuno se ne accorgesse (COI 14° nel footer, AR4 404, `href="tel:+39 06 9362600"` con spazi che alcuni browser mobile non onoravano, duplicate target paths sulle 7 lingue, link interni a slug typo che il render-link hook nascondeva graceful, `draft:true` con data passata mai pubblicato). Questo workflow evita che errori analoghi si sedimentino di nuovo.

### 10.9 — `check-links-sito.yml` — Verifica link sito completo

**Trigger:** lunedì ore 10:00 UTC, esecuzione manuale.

**Cosa fa:**
1. Build Hugo del sito con baseURL di produzione.
2. Esegue **lychee** (`lycheeverse/lychee-action@v2`, industry standard per link checking) su tutti i file `public/**/*.html` generati dal build.
3. Verifica ogni link presente nelle pagine: interni (anchor, path), esterni (widget, card hub, fonti), asset (PDF, immagini).
4. Con cache di 1 giorno (`--max-cache-age 1d`) per evitare di martellare i fornitori esterni settimana dopo settimana se un link è già stato verificato di recente.
5. Se trova link rotti, apre **automaticamente** una issue GitHub con label `manutenzione`, `link-rotti`, `automatico` e report markdown dettagliato (link rotto, codice HTTP, pagina che lo contiene).

**Accepted HTTP codes:** 200, 201, 204, 206, 301, 302, 307, 308, 403, 429. I codici 403 e 429 sono considerati OK perché alcuni siti PA bloccano bot di default ma il link funziona per utenti umani, e 429 è rate-limiting non rottura vera.

**Timeout:** 20s per URL, 3 retry con 5s di attesa (gestisce i siti PA italiani che sono spesso lenti).

**User-Agent personalizzato:** `Mozilla/5.0 (compatible; PCGenzanoLinkChecker/1.0; +https://www.protezionecivilegenzano.it/)` — identifica chiaramente il checker ai fornitori.

**Esclusioni:**
- `^tel:` — link telefonici
- `^mailto:` — email
- `^#` — anchor interni
- `github.io/sito-pc-genzano` — evita self-check verso la preview
- `localhost`, `127.0.0.1` — dev local

**Quando intervenire:** ogni volta che apre una Issue. La Issue contiene l'elenco esatto dei link rotti con codice HTTP e pagina sorgente. Correggi il link (spesso è un path rinominato dal fornitore) e commit.

**Perché esiste:** catturare drift dei link esterni. Esempio reale: aprile 2026, la hub `/strumenti/` è stata pubblicata con il link ANAS `/it/le-strade/viabilita-italia` che in poche ore è tornato 404 (URL obsoleta). L'utente ha trovato il problema a mano; questo workflow lo avrebbe catturato al primo run settimanale.

**Distinzione con `audit-sito.yml` sezione 38:** quest'ultima verifica gli **8 link critici** (Normattiva, DPC, Lazio normativi, PDF locali) con pre-pattern e messaggi dedicati alle 09:00 — sentinella veloce. Il check completo con lychee alle 10:00 è il **catch-all**: tutto il resto del sito (hub strumenti, widget, card, contenuti degli articoli, link PDF nei documenti). Girano 1 ora di distanza per non sovraccaricare il runner.

### 10.10 — Disabilitare temporaneamente un workflow

Due modi:

**Modo A — Interfaccia GitHub** (reversibile, nessun commit):
1. Vai su Actions.
2. Seleziona il workflow nella sidebar.
3. Menu "···" in alto a destra → "Disable workflow".
4. Per riabilitare: stesso menu, "Enable workflow".

**Modo B — Commento in YAML** (tracciato in git):
1. Apri il file `.github/workflows/<nome>.yml`.
2. Commenta la sezione `schedule:` con `#`.
3. Commit con messaggio chiaro ("Sospensione temporanea workflow X — motivo: ...").
4. Per riabilitare: rimuovi i commenti, commit, push.

Preferisci sempre Modo B per tracciabilità, salvo esigenze di emergenza.

### 10.11 — Leggere i log di un workflow

1. Actions → workflow interessato → seleziona run specifica.
2. Espandi il job e lo step che ha fallito.
3. Leggi dalla prima riga rossa o gialla.

**Errori tipici e come leggerli:**
- `Error: YAMLParseError` → data file rotto, vedi 9.9.
- `hugo: error: failed to render...` → template o frontmatter rotto; riga indicata in output.
- `ftp: 550 ...` → permessi o path errato su Aruba; controlla secret.
- `Hash mismatch` → stai aggiornando un file con conflitto; riesegui dopo pull.

### 10.12 — Aggiungere un nuovo workflow

Regole:
- Nome file descrittivo in kebab-case: `nome-azione.yml`.
- `name:` con emoji opzionale ma coerente con gli altri.
- Sempre supportare `workflow_dispatch` per test manuale.
- Dichiarare esplicitamente i `permissions:` minimi necessari.
- Usare action ufficiali o mantenute (`actions/checkout@v4`, `actions/setup-node@v4`, ecc.), pinnate a major version.
- Niente secret hardcoded. Usare `${{ secrets.NAME }}` con secret creati nei Settings del repository.
- Documentare il nuovo workflow in questa Parte 10 e in `CLAUDE.md` (sezione Automazioni).

---

## Parte 11 — Testi per i social (Instagram, Facebook, X, Telegram)

### 11.0 — In breve: cosa fare, cosa non fare

Prima di scrivere un post, queste sono le dieci regole sintetiche da tenere a mente. Il
dettaglio di ciascuna è nelle sezioni successive.

| ✅ Fare | ❌ Non fare |
|---|---|
| Tono formale ma umano, rivolto a persone reali | Tono finto-giovanile, slang, emoji decorativi |
| Fatti verificati, fonti citate, link al sito | Notizie non confermate, "pare che…", "sembra che…" |
| Voce attiva, frasi brevi, italiano corretto | Burocratese, passive inutili, frasi sopra 20 parole |
| Codici colore allerta secondo Regione Lazio | "Allerta massima" per fenomeni ordinari |
| Solo il 112 come numero di emergenza | 115 / 118 / 1515 come riferimento per il cittadino |
| Hashtag coerenti, istituzionali, in CamelCase | Hashtag di tendenza non pertinenti, in minuscolo fuso |
| Immagine con fascia blu e logo | Foto "grezze" dal campo senza trattamento istituzionale |
| Rimando esplicito al sito per approfondire | Informazioni operative solo nel post, senza archivio |
| Correzione trasparente con timestamp | Cancellazione silenziosa di un post con errore |
| Presìdio dichiarato onestamente nei limiti reali | Promessa di risposte H24 che non si possono garantire |

Le regole valgono per **tutti e quattro i canali** (Instagram, Facebook, X, Telegram). Le
differenze di formato, lunghezza e hashtag sono nelle sezioni dedicate a ciascun canale
(11.4, 11.5, 11.6, 11.7).

### 11.1 — A chi parliamo sui social

Il cittadino che ci segue sui social non è un tecnico della protezione civile. È un residente di
Genzano, un genitore, un volontario, un anziano che riceve il post inoltrato dal figlio, un insegnante
che vuole portare l'argomento in classe. Scriviamo pensando a tutti loro contemporaneamente.

Il tono è **formale ma umano**: siamo un'istituzione, non un'agenzia di marketing, ma parliamo con
persone vere. Niente slogan, niente enfasi, niente emoji decorativi. Sì al "voi" quando ci rivolgiamo
direttamente al pubblico, sì a periodi brevi ma in prosa, sì a rimandi chiari al sito per chi vuole
approfondire.

### 11.2 — Canali ufficiali

Il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma pubblica su:

- **Instagram**. Canale visuale, raggiunge un pubblico trasversale (volontari, famiglie, scuole).
  Fino a oggi è stato il canale di partenza per semplicità d'uso.
- **Facebook**. Canale storico della PA locale, raggiunge in particolare un pubblico adulto e
  anziano, molto rappresentativo del territorio di Genzano. Consente post più discorsivi, link
  cliccabili direttamente nel testo e la creazione di eventi pubblici.
- **X (Twitter)**. Canale di broadcast rapido, utile soprattutto per allerte e aggiornamenti
  operativi che devono raggiungere media e istituzioni. Il testo è sempre breve e contiene un
  link al sito.
- **Telegram** (canale broadcast). Serve per notifiche rapide, allerte meteo, aggiornamenti
  operativi rivolti alla cittadinanza iscritta al canale.

#### Relazione tra Instagram e Facebook

Instagram è tecnicamente collegato a Facebook tramite il cross-posting di Meta: un post
Instagram può essere pubblicato automaticamente anche sulla pagina Facebook. Per i contenuti
semplici (foto singola con didascalia breve) il cross-posting funziona bene. Però **Facebook e
Instagram non sono due facce dello stesso canale**: hanno pubblici, formati e abitudini diverse.

Quando si parte da **Instagram**, il post è pensato per la scorciatoia mobile, con caption breve,
immagine forte, hashtag a fine post. Il cross-post su Facebook è accettabile.

Quando si parte da **Facebook**, si può sfruttare il formato più lungo, il link cliccabile nel
testo, l'eventuale creazione di un evento pubblico, il tag ad altre pagine istituzionali
(Comune di Genzano, Regione Lazio). Il contenuto scritto per Facebook è **quasi sempre
migliore** sul suo canale nativo rispetto a un post Instagram cross-postato, soprattutto per
comunicati articolati, campagne di reclutamento, iniziative con programma esteso.

**Regola pratica**: il redattore sceglie il canale di partenza in base al tipo di contenuto,
non in base all'abitudine.

- Contenuto visuale forte, messaggio sintetico → parti da **Instagram**.
- Contenuto articolato, programma di eventi, testo lungo, link esteso → parti da **Facebook**.
- Se il contenuto vuole coprire bene entrambi i pubblici, scrivi **due versioni** (una per
  Facebook, una per Instagram) e disattiva il cross-posting per quel post.

Non abbiamo account LinkedIn, TikTok, YouTube: se verranno attivati, questa Parte andrà
aggiornata con le regole di piattaforma prima del primo post.

### 11.3 — Principi di scrittura social (coerenti con AGID)

Le regole AGID descritte nella **Parte 2** valgono anche qui, con alcuni adattamenti:

1. **Discorsivo, non schematico.** Niente elenchi a pallini dentro il post: raccontiamo in prosa,
   con due o tre periodi brevi. Gli elenchi funzionano sul sito, non su Instagram.
2. **Voce attiva, verbi concreti.** "Il Gruppo ha attivato una squadra" non "È stata disposta
   l'attivazione di una squadra".
3. **Frasi brevi.** Sotto le 20 parole quando possibile. Un pensiero per frase.
4. **Niente burocratese.** "Comportamenti di autoprotezione" sì, "misure comportamentali da porre
   in essere" no.
5. **Niente titoli schematici a effetto.** Evita formule tipo "⚠️ ATTENZIONE ⚠️" a inizio post:
   sul sito sono un abuso visivo, sui social sono grido. Apri con la notizia, non con l'allarme
   grafico.
6. **Sempre inclusivo.** "Cittadine e cittadini", "volontarie e volontari" quando la forma lo permette
   senza appesantire.
7. **Date e orari in forma estesa**: "martedì 21 aprile alle 10" non "21/04 h 10:00".
8. **Numeri di telefono leggibili**: "112" isolato, "06 1234 5678" con spazi.
9. **Fonte sempre esplicita** per previsioni o allerte: "secondo il Centro Funzionale Regionale
   del Lazio", "bollettino della Protezione Civile Lazio".
10. **Niente allarmismo, niente minimizzazione.** Il tono resta calmo anche in emergenza.

### 11.4 — Uso degli emoji

Gli emoji sui canali istituzionali sono ammessi **solo con funzione informativa**, mai decorativa.

| Emoji | Uso consentito |
|---|---|
| ⚠️ | Apre un'allerta meteo o rischio in corso. Uno solo, a inizio post. |
| 🌧️ 🌊 🔥 ❄️ 💨 | Identificano il fenomeno (pioggia, piene, incendi, neve, vento). Uno solo, accanto al titolo interno. |
| ℹ️ | Aggiornamento informativo, nessuna azione richiesta. |
| 📍 | Localizzazione (prima di un indirizzo o zona). |
| 📞 | Precede un numero di telefono. |
| 🗓️ | Precede una data di evento o scadenza. |

Non usare: cuori, pollici in su, applausi, fuochi d'artificio, faccine sorridenti, bandiere, megafoni
a raffica. Mai emoji nel primo rigo del titolo di un'allerta se non ⚠️.

### 11.5 — Regole per piattaforma

#### Instagram

- **Lunghezza consigliata della caption**: 80-150 parole. Massimo 2200 caratteri tecnici, ma oltre
  le 200 parole perdiamo il lettore mobile.
- **Prima riga (sotto la foto)**: deve reggere da sola come titolo. Instagram taglia dopo circa
  125 caratteri con "…altro". La notizia principale deve stare lì.
- **Hashtag**: da **5 a 8**, mai più di 10. Vanno in fondo al post, separati dal testo da una
  riga vuota, non mescolati dentro il discorso.
- **Menzioni**: `@comune.genzanodiroma` per il Comune, `@regionelazioofficial` per la Regione,
  `@protezionecivile` per il Dipartimento nazionale. Verifica sempre l'handle corrente prima di
  taggare: può cambiare.
- **Link nella caption**: Instagram non rende cliccabili i link nel testo. Rimanda con la formula
  *"Tutti i dettagli sul sito: protezionecivilegenzano.it"* e, se il post lo richiede, aggiorna
  il link in bio.
- **Storie**: ammesse per rilanci, eventi in corso, reminder. Le allerte devono restare anche
  come post permanenti, non solo storie.
- **Reel**: se si usano, aggiungere sempre i sottotitoli (accessibilità) e un alt-text.
- **Alt-text immagine**: obbligatorio, descrittivo. Vedi regola 11.8.

#### Facebook

- **Solo pagina ufficiale verificata**. Non pubblichiamo mai da gruppi Facebook, profili
  personali, pagine sussidiarie o pagine non verificate. L'identità istituzionale del Gruppo
  deve essere inequivocabile.
- **Lunghezza consigliata**: 80-300 parole. Facebook premia i post discorsivi e legge bene anche
  testi più articolati (massimo 500 parole per comunicati strutturati). Niente limiti bloccanti
  fino a 63.206 caratteri, ma oltre le 500 parole meglio passare a un articolo sul sito con
  rimando.
- **Prima riga**: deve funzionare come occhiello informativo. Facebook non tronca come Instagram,
  ma il lettore scorre rapidamente: la notizia principale va nelle prime due righe.
- **Link**: **cliccabili** direttamente nella caption e Facebook genera l'anteprima Open Graph
  dell'articolo del sito. Metti sempre il link all'articolo `content/comunicazioni/` dopo il
  corpo del testo, non prima: il link pulito senza decorazioni dà un'anteprima più ordinata.
- **Hashtag**: da **2 a 3**, mai più di 5. Su Facebook gli hashtag sono meno efficaci rispetto a
  Instagram e un'alta concentrazione fa "spam". Palette base ridotta:
  `#ProtezioneCivileGenzano #GenzanoDiRoma` + al massimo un hashtag tematico.
- **Menzioni pagine**: usa `@ComuneDiGenzano`, `@RegioneLazio`, `@ProtezioneCivile` (verifica
  l'handle corrente della pagina prima di taggare). Le menzioni creano link attivi alla pagina
  citata.
- **Eventi Facebook**: per formazione, esercitazioni aperte al pubblico, campagne di reclutamento
  con scadenza, crea un **evento Facebook** collegato al post, con data, luogo, descrizione
  completa e link al sito. Non sostituisce il post, lo affianca.
- **Programma e liste**: su Facebook l'elenco puntato è più tollerato rispetto a Instagram
  (lettori adulti, lettura più lenta). Ammesso per programmi di evento o step di iscrizione,
  ma tenere il corpo principale discorsivo.
- **Foto multiple**: Facebook supporta bene gli album. Per un'esercitazione o un evento concluso,
  un album con 4-10 foto (tutte con fascia blu) è più efficace di una singola foto.
- **Alt-text immagine**: obbligatorio. Lo strumento di Facebook lo chiede esplicitamente.
- **Commenti**: rispondere sempre ai commenti con domande concrete dei cittadini, con tono
  istituzionale. Non rispondere a commenti polemici o di parte.

#### Cross-posting Instagram → Facebook

Se un contenuto nasce su Instagram e si usa il cross-posting automatico:

- va bene per foto singole con caption breve e visuale forte;
- **non va bene** per contenuti che beneficerebbero del formato lungo di Facebook, del link
  cliccabile o di un evento collegato;
- in questi casi, disattivare il cross-posting e pubblicare due versioni separate.

#### X (Twitter)

- **Limite tecnico**: 280 caratteri per post nell'account free, che è quello istituzionale da
  preferire. Non puntiamo ai formati estesi Premium: il messaggio deve restare telegrafico.
- **Lunghezza consigliata**: 200-260 caratteri, lasciando margine per il link e gli hashtag.
- **Struttura**: notizia in apertura + una riga di istruzione o contesto + link al sito +
  hashtag. Niente introduzioni.
- **Link al sito**: obbligatorio in ogni post. X genera automaticamente l'anteprima (card Open
  Graph), che sul sito Hugo è già configurata correttamente.
- **Hashtag**: da **1 a 2**, mai più di 3. Sempre in CamelCase. Vanno a fine post, non dentro
  la frase.
- **Menzioni istituzionali**: `@RegioneLazio` per la Regione, `@DPCgov` per il Dipartimento
  nazionale, `@ComuneGenzano` per il Comune (verificare sempre l'handle corrente prima di
  taggare). Le menzioni consumano caratteri: usarle solo quando davvero informative.
- **Thread**: ammessi solo per comunicati emergenziali lunghi (cronaca in evoluzione). Massimo
  5 post per thread, numerati (1/5, 2/5…). Non usare i thread per attività ordinarie.
- **Immagini**: ogni post con contenuto rilevante accompagnato da immagine istituzionale con
  fascia blu (vedi Parte 3.8). Alt-text obbligatorio anche su X.
- **Nessun retweet senza commento** di fonti non istituzionali. I rilanci di allerte vanno solo
  da account ufficiali (Regione, DPC, Protezione Civile nazionale, 112).
- **Nessuna polemica o risposta a commenti polemici**: i commenti sui post istituzionali non si
  alimentano.

#### Telegram

- **Lunghezza consigliata**: 300-500 caratteri per le notifiche; fino a 1500 caratteri per
  comunicati più strutturati (limite tecnico: 4096).
- **Niente hashtag**: su Telegram i cittadini non li cercano. Se servono per archiviazione interna,
  usarne al massimo uno alla fine (es. `#AllertaMeteo`).
- **Link**: sono cliccabili e generano anteprima. Metti **sempre** il link al sito in fondo:
  `https://www.protezionecivilegenzano.it/comunicazioni/nome-articolo/`.
- **Formattazione**: Telegram supporta `**grassetto**`, `__corsivo__`, `` `codice` ``. Usare solo
  grassetto, solo per evidenziare il tipo di allerta e il codice colore.
- **Emoji**: stesse regole della 11.4. Telegram tollera meglio una sola icona di apertura.
- **Pin del messaggio**: le allerte arancioni e rosse vanno pinnate nel canale finché valide; al
  termine, rimuovere il pin e pubblicare un messaggio di chiusura evento.

### 11.6 — Hashtag ufficiali

Esiste una **palette base** da usare sempre (sul canale Instagram), più hashtag aggiuntivi scelti
di volta in volta in base al contenuto.

#### Palette base (da includere in ogni post Instagram)

- `#ProtezioneCivileGenzano`
- `#GenzanoDiRoma`
- `#ProtezioneCivile`

Questi tre identificano il mittente e il territorio: non vanno mai omessi. Sono scritti in CamelCase
(prima lettera di ogni parola maiuscola) per leggibilità anche con lettori di schermo.

#### Hashtag tematici (scegliere in base al contenuto, 2-5 in aggiunta ai base)

| Tema | Hashtag |
|---|---|
| Territorio Castelli Romani | `#CastelliRomani` `#ParcoCastelliRomani` |
| Allerta meteo | `#AllertaMeteo` `#AllertaMeteoLazio` `#MeteoLazio` |
| Rischio idrogeologico | `#RischioIdrogeologico` `#Maltempo` |
| Rischio incendi | `#IncendiBoschivi` `#RischioIncendi` `#CampagnaAIB` |
| Rischio sismico | `#RischioSismico` `#Terremoto` |
| Rischio neve/ghiaccio | `#Neve` `#Ghiaccio` `#EmergenzaNeve` |
| Volontariato e reclutamento | `#VolontariatoPC` `#DiventaVolontario` `#VolontariProtezioneCivile` |
| Formazione ed esercitazioni | `#FormazionePC` `#Esercitazione` `#AddestramentoPC` |
| Prevenzione e auto-protezione | `#AutoProtezione` `#IoNonRischio` `#Prevenzione` |
| Radiocomunicazioni | `#Radioamatori` `#Radiocomunicazioni` `#EmergencyRadio` |
| Istituzioni | `#RegioneLazio` `#ComuneDiGenzano` `#DipartimentoProtezioneCivile` |
| Eventi pubblici | `#ServizioCivile` `#AttivitàIstituzionali` |

#### Regole d'uso hashtag per piattaforma

- **Instagram** (con cross-post Facebook): totale fra 5 e 8, mai sopra 10. In fondo al post, dopo una riga vuota.
- **X (Twitter)**: da 1 a 2, mai sopra 3. In fondo al post, consumano caratteri preziosi.
- **Telegram**: nessun hashtag, oppure al massimo uno di servizio in fondo (es. `#AllertaMeteo`).

#### Regole d'uso hashtag (trasversali)

- **In CamelCase**: `#AllertaMeteoLazio` non `#allertameteolazio`. Gli screen reader leggono meglio.
- **Niente hashtag in inglese** se non sono nomi propri di iniziative (es. `#IoNonRischio`).
- **Niente hashtag generici svuotati** (`#italia`, `#news`, `#amazing`).
- **Niente hashtag politici o divisivi.**
- **Niente hashtag di trend** non pertinenti al messaggio istituzionale.

### 11.7 — Rimando al sito (formule standard)

Ogni post deve rimandare al sito. Varianti approvate, da alternare per non suonare ripetitivi:

- *"Aggiornamenti e tutti i dettagli sul sito: protezionecivilegenzano.it"*
- *"Trovate il comunicato completo su protezionecivilegenzano.it"*
- *"Per restare aggiornati consultate protezionecivilegenzano.it"*
- *"La scheda completa con le raccomandazioni di auto-protezione è sul nostro sito."*
- *"Il bollettino integrale e le mappe sono disponibili su protezionecivilegenzano.it"*

Su Telegram il link va reso cliccabile con l'URL esteso dell'articolo specifico.
Su Instagram, dove i link non sono cliccabili, citare solo il dominio e aggiornare il link in bio.

### 11.8 — Accessibilità social

- **Alt-text immagine obbligatorio** su Instagram e Facebook. Descrive il contenuto informativo
  della foto, non il mittente. Esempio: *"Volontari di protezione civile con pettorina arancione
  caricano sacchi di sabbia su un furgone bianco accanto al Lago di Nemi"*. Vedi Parte 3.10 per
  le regole generali di alt-text.
- **Hashtag in CamelCase** per i lettori di schermo.
- **Niente testo essenziale dentro l'immagine**: il messaggio informativo deve stare nella caption,
  non nella grafica. Le immagini con testo sono ammesse come rinforzo visivo, non come unico veicolo
  dell'informazione.
- **Sottotitoli sempre attivi** nei video e nei reel.
- **Contrasto**: se si usano card grafiche, contrasto minimo 4.5:1 su sfondo bianco.
- **Niente GIF animate o effetti lampeggianti** (rispetto di `prefers-reduced-motion` anche nella
  comunicazione social).

### 11.9 — Cosa NON pubblicare

#### Contenuti vietati

- Volti riconoscibili di cittadini o colleghi senza liberatoria esplicita.
- Targhe di veicoli privati.
- Dati sensibili (indirizzi di abitazioni coinvolte, nomi di infortunati, informazioni sanitarie).
- Numeri telefonici privati dei volontari.
- Foto operative che possano compromettere sicurezza o segreto istruttorio.
- Meme, frasi a effetto, battute.
- Commenti politici o di parte.
- Previsioni meteo non ufficiali, rilancio di post da pagine meteo amatoriali.
- Ringraziamenti generici a "tutti coloro che…": sempre specifici e verificati.
- Complimenti o critiche ad altre istituzioni.
- Contenuti allarmistici, enfatici o sensazionalistici.

#### Formule vietate (engagement bait)

Le seguenti formule sono tipiche del marketing e **non trovano posto** nella comunicazione
istituzionale del Gruppo:

- "Tagga un amico che…"
- "Condividete se siete d'accordo"
- "Scrivete SÌ nei commenti"
- "Mettete un cuore se vi è piaciuto"
- "Chi è con noi?"
- "Il primo che…"
- Richieste di emoji di reazione, sondaggi-gioco, quiz frivoli.

L'unica richiesta di azione ammessa al cittadino è informativa e utile: *"consultate il sito
per restare aggiornati"*, *"iscrivetevi al canale Telegram per gli aggiornamenti in tempo
reale"*, *"chiamate il 112 in caso di emergenza"*.

#### Mai tono finto-giovanile

La PA non deve rincorrere il lessico dei social per "sembrare accessibile". Usare abbreviazioni
da chat, slang, emoji esuberanti o tono scherzoso rompe la fiducia istituzionale. Si può essere
**umani senza smettere di essere istituzione**: è questo l'equilibrio del manuale.

### 11.9 bis — Gestione errori e post fuori controllo

Gli errori capitano. Una comunicazione istituzionale che sbaglia e **corregge in modo
trasparente** mantiene la fiducia dei cittadini; una che cancella silenziosamente un post la
perde.

#### Se un post contiene un errore fattuale

1. **Non cancellare** il post originale (a meno che contenga dati sensibili o errori gravi non
   correggibili).
2. **Modificare** il post originale (Facebook e Telegram consentono la modifica; Instagram e X
   consentono la modifica con limiti di tempo), aggiungendo in apertura la formula:
   *"Aggiornamento delle ore HH:MM: la versione precedente indicava erroneamente […]. La
   versione corretta è la seguente."*
3. Se la modifica non è possibile, **pubblicare un secondo post di correzione** che rimanda al
   primo e chiarisce cosa cambia.
4. **Segnalare** la correzione sugli altri canali dove il contenuto era stato replicato.
5. **Archiviare** uno screenshot della versione originale errata e della versione corretta in
   `static/archivio-social/AAAA/` (vedi 11.17).

#### Se un post genera polemica o viene distorto

1. **Non rispondere di impulso** ai commenti polemici. La pagina istituzionale non si difende,
   chiarisce i fatti quando necessario.
2. **Non cancellare** i commenti critici se non violano la netiquette (vedi Parte 13).
3. **Rimuovere** invece i commenti che violano la netiquette, senza spiegazioni polemiche.
4. Se nasce una narrazione distorta, **pubblicare un chiarimento** basato sui fatti, non
   sull'emozione.
5. **Coinvolgere** il Coordinatore (e, se necessario, il Comune) prima di reagire
   pubblicamente a situazioni critiche.

#### Se un contenuto deve essere ritirato

Esempio: una notizia che si rivela errata, un'iniziativa cancellata, un dato poi rivisto.

1. Pubblicare un post di **ritiro esplicito**: *"La comunicazione del HH:MM sul tema [X] è
   superata. La situazione aggiornata è […]"*.
2. Aggiornare l'articolo corrispondente sul sito con una nota di superamento in cima.
3. Lasciare visibile la cronologia: la trasparenza vale più della pulizia.

### 11.10 — Ruoli e flusso di approvazione

#### Ruoli istituzionali

Il **DL 25/2025 convertito in Legge 69/2025** ha formalizzato nella PA il ruolo del Social Media
e Digital Manager. Per il nostro contesto (ente del terzo settore iscritto al RUNTS), il ruolo è
adattato nel profilo del **Referente comunicazione**, designato dal Coordinatore del Gruppo.

| Ruolo | Responsabilità |
|---|---|
| **Coordinatore del Gruppo** | Approvazione finale dei contenuti sensibili (allerte, comunicati stampa, post in emergenza), responsabilità dei virgolettati istituzionali, interlocuzione con Sindaco e Comune. |
| **Referente comunicazione** | Coordina la redazione di articoli, post social e comunicati stampa. Applica la checklist 11.12, cura la pianificazione editoriale (vedi `PIANO-EDITORIALE.md`), presidia la netiquette pubblicata. |
| **Redattori volontari** | Producono le bozze, inseriscono gli allegati, applicano la fascia blu alle immagini. |
| **Pubblicatore** | Chi ha le credenziali dei canali. Pubblica solo bozze già approvate. |
| **Sala operativa** | In emergenza, unifica i ruoli di redazione, verifica e pubblicazione. |

In piccoli gruppi uno stesso volontario può ricoprire più ruoli: l'importante è che per ogni
contenuto sia chiaro **chi lo ha scritto** e **chi lo ha approvato** prima della pubblicazione.

#### Flusso ordinario

1. **Chi scrive**: un volontario redige la bozza in un documento condiviso (non direttamente
   nell'app social).
2. **Chi verifica**: il Referente comunicazione legge la bozza e applica la **checklist 11.12**.
3. **Chi approva** (quando necessario): il Coordinatore dà l'OK sui contenuti sensibili.
4. **Chi pubblica**: chi ha le credenziali del canale, dopo le approvazioni previste. Mai
   pubblicare una bozza non verificata "per velocità".
5. **Archiviazione**: i post importanti (allerte, comunicati, eventi) restano anche come
   articolo sul sito (`content/comunicazioni/`) e come screenshot archiviato (vedi 11.17) per
   garantirne la reperibilità e la paternità nel tempo.

#### Flusso in emergenza

Il flusso si comprime: Sala operativa e Coordinatore (o chi ne fa le veci) possono coincidere
con chi scrive, verifica e pubblica. La regola dei contenuti **non cambia**: niente dati non
verificati, niente stime non confermate, niente promesse. La velocità si ottiene semplificando
la catena di approvazione, non saltando i controlli sostanziali.

### 11.11 — Template per tipo di contenuto

I template che seguono sono esempi operativi. Vanno sempre adattati al contesto reale, mai copiati
a scatola chiusa.

#### Template 1 — Allerta meteo (livello giallo/arancione/rosso)

**Instagram** (caption) — la stessa caption funziona bene anche come cross-post Facebook per contenuti sintetici come questo:

> ⚠️ Allerta meteo arancione sui Castelli Romani per martedì 21 aprile.
>
> Il Centro Funzionale Regionale del Lazio ha emesso un'allerta arancione per rischio
> idrogeologico sulla zona dei Castelli Romani. Sono previste piogge intense e possibili
> allagamenti nelle ore pomeridiane.
>
> Se possibile rimanete in casa durante i fenomeni più intensi. Non sostate in sottopassi o
> aree a rischio allagamento. In caso di emergenza chiamate il 112.
>
> Il bollettino completo e le raccomandazioni di auto-protezione sono su
> protezionecivilegenzano.it
>
> #ProtezioneCivileGenzano #GenzanoDiRoma #ProtezioneCivile #AllertaMeteoLazio
> #RischioIdrogeologico #CastelliRomani #RegioneLazio

**X (Twitter)**:

> ⚠️ Allerta meteo arancione sui Castelli Romani per martedì 21 aprile. Piogge intense e
> rischio allagamenti nel pomeriggio. Non sostate in sottopassi. In emergenza: 112.
>
> Bollettino: https://www.protezionecivilegenzano.it/comunicazioni/allerta-meteo-21-aprile-2026/
>
> #AllertaMeteoLazio #CastelliRomani

**Telegram**:

> ⚠️ **Allerta meteo arancione** — martedì 21 aprile
>
> Il Centro Funzionale Regionale del Lazio segnala rischio idrogeologico sulla zona dei
> Castelli Romani. Piogge intense e possibili allagamenti nel pomeriggio.
>
> Restate in casa durante i fenomeni più intensi. Non sostate in sottopassi o aree a rischio
> allagamento. In caso di emergenza: 📞 112.
>
> Bollettino completo: https://www.protezionecivilegenzano.it/comunicazioni/allerta-meteo-21-aprile-2026/

#### Template 2 — Evento formativo o esercitazione

**Instagram** (con cross-post Facebook accettabile per questo contenuto sintetico):

> 🗓️ Sabato 10 maggio il Gruppo Comunale Volontari partecipa all'esercitazione regionale
> "Castelli Sicuri 2026" insieme alla Regione Lazio e ai comuni dei Castelli Romani.
>
> L'esercitazione simula una scossa sismica di magnitudo moderata e prevede l'attivazione
> delle procedure di assistenza alla popolazione, la gestione delle aree di attesa e le
> comunicazioni radio tra sale operative.
>
> L'area interessata sarà il centro storico di Genzano dalle 9 alle 13. Nessun disagio per
> la cittadinanza.
>
> Programma completo su protezionecivilegenzano.it
>
> #ProtezioneCivileGenzano #GenzanoDiRoma #ProtezioneCivile #Esercitazione #FormazionePC
> #CastelliRomani #RischioSismico

**Facebook** (versione estesa con evento collegato — consigliata per esercitazioni pubbliche):

> Sabato 10 maggio il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
> partecipa all'esercitazione regionale "Castelli Sicuri 2026" insieme a @RegioneLazio e
> ai comuni dei Castelli Romani.
>
> L'esercitazione simula una scossa sismica di magnitudo moderata. Le squadre dei
> volontari testeranno le procedure di assistenza alla popolazione, la gestione delle aree
> di attesa e le comunicazioni radio tra sale operative. L'iniziativa rientra nel
> programma regionale di preparazione al rischio sismico.
>
> L'area interessata è il centro storico di Genzano, dalle 9 alle 13 di sabato 10 maggio.
> Non sono previsti disagi per la cittadinanza: le attività si svolgono in modo
> coordinato con la Polizia Locale.
>
> Il programma completo e le mappe dei punti di prova sono sul sito:
> https://www.protezionecivilegenzano.it/comunicazioni/esercitazione-castelli-sicuri-2026/
>
> #ProtezioneCivileGenzano #GenzanoDiRoma #CastelliRomani

> *Consiglio operativo: collega al post un **evento Facebook** con data/ora, luogo e link
> al sito. I commenti sono moderati secondo la netiquette pubblicata su
> protezionecivilegenzano.it/social-media-policy.*

**X (Twitter)**:

> 🗓️ Sabato 10 maggio il Gruppo Volontari PC Genzano partecipa all'esercitazione
> regionale "Castelli Sicuri 2026". Centro storico, ore 9-13. Nessun disagio per i
> cittadini.
>
> Programma: https://www.protezionecivilegenzano.it/comunicazioni/esercitazione-castelli-sicuri-2026/
>
> #Esercitazione #CastelliRomani

**Telegram** (facoltativo per eventi formativi, utile come reminder 48 ore prima):

> 🗓️ **Reminder** — esercitazione "Castelli Sicuri 2026"
>
> Sabato 10 maggio, dalle 9 alle 13, il Gruppo Comunale Volontari partecipa
> all'esercitazione sismica regionale nel centro storico di Genzano. Attività coordinate
> con la Polizia Locale, nessun disagio previsto per i cittadini.
>
> Programma completo: https://www.protezionecivilegenzano.it/comunicazioni/esercitazione-castelli-sicuri-2026/

#### Template 3 — Reclutamento volontari

**Instagram** (versione sintetica):

> Il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma cerca nuove
> volontarie e nuovi volontari.
>
> Non servono competenze tecniche: la formazione è interna e gratuita. Serve tempo, spirito
> di servizio e voglia di imparare. Si parte con il corso base, si prosegue con
> specializzazioni a scelta (radio, logistica, avvistamento incendi, protezione sismica).
>
> Informazioni e modulo di iscrizione su protezionecivilegenzano.it alla pagina
> "Diventa volontario".
>
> #ProtezioneCivileGenzano #GenzanoDiRoma #ProtezioneCivile #VolontariatoPC
> #DiventaVolontario #CastelliRomani

**Facebook** (versione estesa con link cliccabile e tag istituzionale — disattivare il
cross-posting da Instagram per pubblicare questa variante):

> Il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma cerca nuove
> volontarie e nuovi volontari per il 2026.
>
> Unirsi al Gruppo significa dedicare parte del proprio tempo alla propria comunità, in
> attività che vanno dall'assistenza alla popolazione durante le emergenze alla prevenzione,
> alla formazione, al presidio del territorio. Non servono competenze tecniche di partenza:
> la formazione è gratuita, interna e accompagna la persona dall'ingresso fino alla
> specializzazione.
>
> Il percorso inizia con il corso base (dodici lezioni serali), prosegue con esercitazioni
> pratiche e consente di scegliere una specializzazione fra radiocomunicazioni, logistica,
> avvistamento antincendio, assistenza alla popolazione. Il Gruppo opera sul territorio di
> Genzano e collabora con @ComuneDiGenzano, @RegioneLazio e le altre protezioni civili dei
> Castelli Romani.
>
> Possono iscriversi residenti maggiorenni. Le iscrizioni si chiudono il 30 aprile 2026.
>
> Tutte le informazioni, i requisiti e il modulo di iscrizione sono qui:
> https://www.protezionecivilegenzano.it/diventa-volontario/
>
> #ProtezioneCivileGenzano #GenzanoDiRoma #VolontariatoPC

> *Consiglio operativo: a questo post va collegato un **evento Facebook** con data di chiusura
> iscrizioni (30 aprile 2026), luogo (sede comunale), descrizione breve e link al sito. L'evento
> moltiplica la visibilità e genera reminder automatici ai cittadini interessati.*

#### Template 4 — Aggiornamento operativo (post-evento)

**Instagram**:

> Si è conclusa alle 22 di ieri l'attivazione del Gruppo Comunale Volontari per il
> maltempo che ha interessato Genzano nella giornata di lunedì.
>
> Sei volontari hanno presidiato le aree più esposte di via Nemorense e via dei Laghi,
> supportando la Polizia Locale nella chiusura temporanea di un tratto stradale allagato.
> Nessuna persona coinvolta, nessun danno rilevante alle abitazioni.
>
> Grazie a chi era in strada e a chi, da casa, ha seguito le raccomandazioni di auto-protezione.
>
> Il resoconto completo dell'attivazione è su protezionecivilegenzano.it
>
> #ProtezioneCivileGenzano #GenzanoDiRoma #ProtezioneCivile #Maltempo #RischioIdrogeologico
> #CastelliRomani

**Facebook** (versione dedicata, formato discorsivo esteso):

> Si è conclusa alle 22 di ieri, lunedì 20 aprile, l'attivazione straordinaria del
> Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma avviata alle 13:15
> per il maltempo che ha interessato il territorio comunale nella giornata.
>
> Sei volontari su due squadre operative hanno presidiato le aree più esposte — via
> Nemorense e via dei Laghi — supportando la Polizia Locale nella chiusura temporanea
> di un tratto stradale interessato da allagamento. Il tratto è stato riaperto alle 20:30
> al termine delle operazioni di ripristino.
>
> Sulla base delle segnalazioni pervenute alla Sala operativa entro le 22, non si
> registrano persone coinvolte né danni rilevanti alle abitazioni.
>
> Un ringraziamento ai volontari che sono stati in strada, alla @PoliziaLocaleGenzano
> e a tutti i cittadini che hanno seguito le raccomandazioni di auto-protezione limitando
> gli spostamenti non necessari.
>
> Il resoconto completo dell'attivazione — con cronologia, forze coinvolte e numeri —
> è disponibile su https://www.protezionecivilegenzano.it/comunicazioni/resoconto-maltempo-20-aprile-2026/
>
> I commenti sono moderati secondo la netiquette pubblicata su
> protezionecivilegenzano.it/social-media-policy
>
> #ProtezioneCivileGenzano #GenzanoDiRoma #Maltempo

**X (Twitter)**:

> ℹ️ Conclusa alle 22 l'attivazione del Gruppo Comunale Volontari per il maltempo a Genzano.
> Sei volontari in strada a supporto della Polizia Locale. Nessuna persona coinvolta.
>
> Resoconto: https://www.protezionecivilegenzano.it/comunicazioni/resoconto-maltempo-20-aprile-2026/
>
> #Maltempo #CastelliRomani

**Telegram** (versione breve):

> ℹ️ **Attivazione conclusa** — maltempo del 20 aprile
>
> Alle 22 di ieri si è chiusa l'attivazione del Gruppo Comunale Volontari. Sei volontari
> hanno presidiato via Nemorense e via dei Laghi a supporto della Polizia Locale. Nessuna
> persona coinvolta, nessun danno rilevante.
>
> Resoconto completo: https://www.protezionecivilegenzano.it/comunicazioni/resoconto-maltempo-20-aprile-2026/

#### Template 5 — Prevenzione stagionale

**Instagram** (con cross-post Facebook):

> Da giugno a settembre nel Lazio è periodo di massima pericolosità per gli incendi
> boschivi. La campagna AIB (Anti Incendi Boschivi) della Regione Lazio è attiva.
>
> Cosa può fare ogni cittadino: non accendere fuochi all'aperto nei boschi e nelle aree
> adiacenti, non abbandonare mozziconi di sigaretta, mantenere pulita la fascia intorno
> alle abitazioni isolate. Se vedete un principio di incendio, chiamate subito il 112:
> la centrale attiverà vigili del fuoco e squadre AIB.
>
> Tutte le raccomandazioni della campagna AIB sono sul nostro sito.
>
> #ProtezioneCivileGenzano #GenzanoDiRoma #ProtezioneCivile #CampagnaAIB
> #IncendiBoschivi #AutoProtezione #RegioneLazio

**Facebook** (versione estesa consigliata per approfondimenti stagionali):

> Da giugno a settembre nel Lazio è periodo di massima pericolosità per gli incendi
> boschivi. La campagna AIB (Anti Incendi Boschivi) della @RegioneLazio è attiva su
> tutto il territorio regionale, Castelli Romani compresi.
>
> Gli incendi boschivi in questo periodo hanno quasi sempre origine umana: un
> comportamento scorretto può innescare un evento che mette in pericolo la vita, i
> boschi e le abitazioni. Le regole di comportamento sono semplici e sono valide per
> chiunque frequenti aree verdi. Non accendere fuochi all'aperto nei boschi e nelle
> aree adiacenti. Non abbandonare mozziconi di sigaretta. Mantenere pulita la fascia
> intorno alle abitazioni isolate eliminando erba secca e materiali infiammabili. Non
> bruciare residui agricoli nel periodo a rischio.
>
> Se vedi un principio di incendio, chiama subito il **112**: la centrale unica di
> emergenza attiverà i vigili del fuoco e le squadre AIB regionali.
>
> Tutte le raccomandazioni della campagna AIB e la mappa delle zone a rischio sono qui:
> https://www.protezionecivilegenzano.it/rischi-prevenzione/rischio-incendi/
>
> #ProtezioneCivileGenzano #GenzanoDiRoma #CampagnaAIB

**X (Twitter)**:

> 🔥 Campagna AIB 2026 attiva nel Lazio da giugno a settembre. Non accendere fuochi nei
> boschi, non abbandonare mozziconi, tieni pulita l'area intorno a casa. Se vedi un
> incendio: 112.
>
> Dettagli: https://www.protezionecivilegenzano.it/rischi-prevenzione/rischio-incendi/
>
> #CampagnaAIB #IncendiBoschivi

**Telegram** (facoltativo all'avvio stagione o durante ondate di calore):

> 🔥 **Campagna AIB 2026 — attenzione agli incendi boschivi**
>
> Da giugno a settembre il rischio è al massimo. Non accendere fuochi nei boschi, non
> abbandonare mozziconi, mantieni pulita la fascia intorno alle abitazioni isolate. Se
> vedi un principio di incendio chiama il 📞 112.
>
> Tutte le raccomandazioni: https://www.protezionecivilegenzano.it/rischi-prevenzione/rischio-incendi/

### 11.12 — Checklist pre-pubblicazione social

Controlli comuni a tutti i canali:

- [ ] Il post ha una notizia chiara nella prima riga?
- [ ] Il tono è formale-umano, senza burocratese né enfasi?
- [ ] Verbi attivi, frasi brevi, italiano corretto?
- [ ] Date in forma estesa, numeri di telefono leggibili?
- [ ] Fonte dell'informazione esplicita (quando allerta o previsione)?
- [ ] Niente numeri di emergenza diversi dal 112 come numero da chiamare?
- [ ] Rimando al sito presente e corretto?
- [ ] Alt-text dell'immagine compilato e descrittivo?
- [ ] Immagine con fascia blu istituzionale (Parte 3.8)?
- [ ] Nessun volto o targa riconoscibile senza liberatoria?
- [ ] Emoji solo funzionali (11.4)?
- [ ] Nessun hashtag in inglese, politico, generico, di trend?
- [ ] Nessuna formula di engagement bait ("tagga un amico", "condividi se…")?
- [ ] Hashtag in CamelCase?
- [ ] Il Referente comunicazione o il Coordinatore hanno approvato la bozza?

Controlli specifici per canale:

- [ ] **Instagram**: 80-150 parole, prima riga sotto 125 caratteri, 5-8 hashtag a fine post (palette base presente), link in bio aggiornato se necessario.
- [ ] **Facebook**: 80-300 parole (fino a 500 per contenuti strutturati), 2-3 hashtag, link cliccabile al sito, eventuale evento collegato per iniziative con scadenza, pubblicato dalla pagina ufficiale verificata (mai da un gruppo).
- [ ] **X (Twitter)**: sotto 280 caratteri (200-260 consigliati), 1-2 hashtag, link al sito nel post.
- [ ] **Telegram**: 300-500 caratteri, nessun hashtag (o uno solo di servizio), link cliccabile completo all'articolo del sito.

Se il post è un'allerta o un comunicato di emergenza:

- [ ] Il contenuto è anche sul sito come articolo (`content/comunicazioni/`)?
- [ ] Il livello di allerta è quello ufficiale del Centro Funzionale Regionale?
- [ ] Sul canale Telegram il messaggio è pinnato fino a termine dell'evento?
- [ ] Screenshot del post archiviato in `static/archivio-social/AAAA/` (vedi 11.17)?

### 11.13 — Blocco firma per post istituzionali

I post social non necessitano di una firma: il profilo parla per sé. Ma se un post contiene un
virgolettato, la firma va esplicitata dentro il testo, non in fondo:

> *"Ringraziamo la cittadinanza per la collaborazione durante l'attivazione di ieri" —
> Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.*

Per virgolettati attribuiti personalmente: vedi **Parte 12.6** (regole comuni a stampa e social).

### 11.14 — Allegati, immagini e file forniti dall'utente

Quando chi redige (o chi chiede a un'AI di redigere) fornisce insieme al testo **immagini, PDF,
documenti o altri file**, questi vanno **sempre integrati** nell'articolo o nel post secondo le
regole del manuale. Non vanno né ignorati né lasciati senza trattamento.

#### Immagini fornite

Ogni immagine fornita per un articolo o un post social va:

1. **Ridimensionata** a 1200 px di larghezza (Parte 3.7).
2. **Trattata con la fascia blu istituzionale** (`#003366`, logo, scritta "PROTEZIONE CIVILE /
   Gruppo Comunale Volontari — Genzano di Roma"). Vedi **Parte 3.8** per le specifiche complete
   e la procedura passo-passo.
3. **Convertita in WebP** e compressa sotto i 200 KB (Parte 3.9).
4. **Salvata** in `static/images/` con naming `AAAA-MM-GG-descrizione-breve.webp` (Parte 3.11).
5. **Dotata di alt-text significativo** sia sul sito (frontmatter `image:` e campo `alt`) sia
   nei post social (campo alt-text della piattaforma). Vedi Parte 3.10.

Nessun articolo e nessun post social con immagine va pubblicato con una foto **senza fascia blu**.
Se l'immagine originale fornita dall'utente è già "pulita" (ha già fascia e logo), va comunque
verificata: contrasto, leggibilità del logo, correttezza della dicitura. Se l'immagine non può
essere trattata (es. infografica tecnica con layout complesso), va affiancata da una seconda
immagine istituzionale con fascia usata come copertina.

#### PDF e documenti forniti

Ogni PDF o documento fornito per un articolo va:

1. **Rinominato** in formato leggibile: `AAAA-MM-GG-descrizione-breve.pdf` (niente spazi,
   niente caratteri accentati, niente maiuscole casuali).
2. **Salvato** nella cartella appropriata:
   - `static/allegati/AAAA/` per allegati di articoli ordinari.
   - `static/comunicati/AAAA/` per versioni PDF firmate di comunicati stampa (Parte 12.8).
   - `static/manuali/` per manuali tecnici permanenti citati da più articoli (es. manuale FIC, Libro Risparmio Barilla, manuale Caritas-Banco Alimentare).
   - **Non usare** `static/documenti/`, `static/cartelli/`, `static/giochi-bambini/`, `static/formazionepc/`, `static/quizpc/`: sono cartelle **escluse dal deploy FTP** (vedi Parte 10.2 — Cartelle protette lato server). Un file messo lì non verrebbe mai caricato su Aruba.
3. **Linkato** nel frontmatter dell'articolo attraverso il campo `allegati:`, con titolo
   leggibile, dimensione del file e tipo. Vedi **Parte 1.10**.
4. **Verificato**: peso ragionevole (preferibilmente sotto 2 MB), PDF accessibile (testo
   selezionabile, non solo immagine), titolo e metadati del PDF coerenti con il contenuto.
5. **Citato nel testo dell'articolo** con la formula *"Ordinanza sindacale (PDF, 120 KB)"* o
   equivalente, non come link anonimo. Vedi regola AGID 2.15 sui link.

Nei post social i PDF non vengono caricati direttamente: vanno lasciati sul sito e richiamati
tramite il rimando *"Documento completo su protezionecivilegenzano.it"*.

#### Altri file (video, audio, dataset)

- **Video brevi** (clip da una dashcam, da uno smartphone durante un'esercitazione): vanno
  convertiti in formato MP4 H.264, peso ragionevole per il web, con sottotitoli se contengono
  parlato. Su Instagram usabili come Reel, su X come clip nativi, su Telegram come video inline.
- **Audio** (interviste radio, podcast): da evitare come unico canale informativo; se usati,
  sempre accompagnati da trascrizione scritta per accessibilità.
- **Dataset** (fogli di calcolo, GeoJSON, dati di attivazione): non si pubblicano sui social.
  Si pubblicano sul sito, eventualmente in una pagina dedicata, con licenza e metadati chiari.

#### Regola operativa per l'AI redattrice

Se chi chiede la redazione fornisce uno o più file insieme al testo, l'AI (o il redattore
umano) deve:

1. **Riconoscere** tutti i file forniti e chiedere conferma se il loro ruolo non è chiaro
   (*"Questa foto è la copertina dell'articolo o un allegato interno?"*).
2. **Applicare** automaticamente tutti i trattamenti previsti sopra (fascia blu sulle immagini,
   rinomina dei PDF, alt-text significativo).
3. **Integrare** i file nel frontmatter e nel corpo dell'articolo/post.
4. **Dichiarare** esplicitamente nella risposta quali file ha trattato e come (es.: *"Ho
   applicato la fascia blu alla foto, l'ho convertita in WebP e salvata come
   `2026-04-21-intervento-maltempo.webp`. L'ordinanza sindacale è stata rinominata in
   `2026-04-21-ordinanza-chiusura-via-nemorense.pdf` e aggiunta al campo `allegati:`"*).

### 11.15 — Cross-pubblicazione fra sito e canali social

Un contenuto istituzionale vive raramente su un solo canale. Quando si produce una
comunicazione, bisogna chiedersi **su quali canali va** e produrre **versioni coerenti ma
adattate** a ciascuno.

#### Regola operativa

Quando il redattore (umano o AI) riceve la richiesta di produrre **un articolo per il sito**,
deve chiedere se serve anche la versione per **Instagram**, **Facebook**, **X (Twitter)** e/o
**Telegram**.

Quando il redattore riceve la richiesta di produrre **un post per un social** (es. Instagram),
deve chiedere se serve anche:

- la versione per **gli altri social** attivi (Facebook, X, Telegram);
- la versione **articolo sul sito** (`content/comunicazioni/`), che è sempre raccomandata per
  contenuti che devono essere reperibili nel tempo (allerte, comunicati, eventi, formazione,
  reclutamento).

Instagram e Facebook vanno considerati **due canali distinti**, anche se tecnicamente collegati
dal cross-posting. Il redattore decide se scrivere **una sola versione** (da pubblicare su
entrambi con cross-posting) o **due versioni separate**. Due versioni separate sono consigliate
quando Facebook può sfruttare il formato lungo, il link cliccabile o un evento pubblico (vedi
**11.5 — Facebook**).

La domanda va posta **in apertura**, prima di redigere il testo, in modo che le versioni siano
scritte in parallelo e coerenti fra loro (non traduzioni successive).

Esempio di domanda:

> *"Questo contenuto lo scriviamo solo per Instagram oppure anche come articolo sul sito, post
> su X e messaggio Telegram? Le versioni le posso preparare tutte insieme."*

#### Matrice cross-canale consigliata

| Tipo di contenuto | Sito | Instagram | Facebook | X | Telegram |
|---|---|---|---|---|---|
| Allerta meteo (gialla/arancione/rossa) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Comunicato emergenziale | ✅ | ✅ | ✅ | ✅ | ✅ |
| Aggiornamento operativo post-evento | ✅ | ✅ | ✅ | ✅ | ✅ |
| Esercitazione, formazione, corso | ✅ | ✅ | ✅ (+evento) | facoltativo | facoltativo |
| Reclutamento volontari | ✅ | ✅ | ✅ (+evento) | facoltativo | facoltativo |
| Prevenzione stagionale | ✅ | ✅ | ✅ | facoltativo | facoltativo |
| Ringraziamenti, celebrazioni | facoltativo | ✅ | ✅ | no | no |
| Album foto di un evento concluso | ✅ | carosello | ✅ (album) | no | no |
| Storie dietro le quinte | no | ✅ | facoltativo | no | no |
| Documenti istituzionali (piani, regolamenti) | ✅ | no | ✅ (link) | no | no |

Le colonne **non** si riempiono con lo stesso testo. Si adattano:

- Sul sito: versione completa, discorsiva, con frontmatter, immagine con fascia blu, allegati.
- Su Instagram: versione di 80-150 parole, con immagine, 5-8 hashtag, rimando al sito.
- Su Facebook: versione di 80-300 parole (fino a 500 per contenuti strutturati), link cliccabile
  nel testo, 2-3 hashtag, eventuale evento collegato, eventuale album foto.
- Su X: versione di 200-260 caratteri, con link, 1-2 hashtag.
- Su Telegram: versione di 300-500 caratteri, con link cliccabile, senza hashtag.

I fatti, le fonti, le fonti di allerta, i numeri, le date restano **identici** su tutti i canali.

#### Ordine di pubblicazione

Per contenuti ordinari: prima l'articolo sul sito, poi i post social (così i rimandi al sito
puntano a una pagina esistente).

Per contenuti emergenziali: come da **Parte 12.12**, Telegram è il primo canale (entro 10
minuti), sito entro 20 minuti, Instagram/Facebook/X entro 30 minuti, mail stampa entro 30
minuti. L'articolo sul sito viene comunque pubblicato rapidamente perché è la "fonte unica"
citata in tutti gli altri canali.

### 11.16 — Licenza dei contenuti social

Tutti i contenuti testuali, fotografici e grafici pubblicati sui canali social del Gruppo
(Instagram, Facebook, X, Telegram) sono rilasciati, ove non diversamente indicato, con licenza
**Creative Commons Attribuzione 4.0 Internazionale (CC BY 4.0)**, coerentemente con quanto
dichiarato per il sito (vedi pagina [Note legali](/note-legali/) e `content/note-legali/_index.md`).

Questo significa che chiunque può:

- riprendere il contenuto (testo, foto, infografica) su altri canali, anche commerciali;
- modificarlo o adattarlo;
- citarlo in articoli, tesi, materiali formativi.

A condizione di:

- **attribuire** la paternità al *Gruppo Comunale Volontari di Protezione Civile di Genzano di
  Roma*, con link a `https://www.protezionecivilegenzano.it/`;
- **non alterare i fatti** comunicati (numeri, fonti, codici colore di allerta);
- **non presentare** l'adattamento come comunicazione ufficiale del Gruppo se modifica la
  sostanza del messaggio.

Fanno eccezione:

- **fotografie con persone riconoscibili**: soggette a liberatoria individuale, non ridistribuibili;
- **loghi e identità visiva** del Gruppo, del Comune, del Dipartimento di Protezione Civile:
  protetti da diritti specifici, non rilasciati in CC BY;
- **materiali di terzi** (es. infografiche DPC, ISPRA, INGV) citati con attribuzione alla fonte
  originaria, che mantiene la propria licenza.

Nei post che rilanciano comunicati stampa o documenti istituzionali, inserire il rimando:

> *"Testo completo e licenza su protezionecivilegenzano.it/note-legali/"*

### 11.17 — Archivio screenshot post importanti

Per garantire la tracciabilità e la verificabilità della comunicazione social, tutti i post
classificabili come **istituzionali rilevanti** vengono archiviati in forma di screenshot
all'interno del repository del sito.

#### Cosa archiviare

- Tutti i post di **allerta meteo** (giallo, arancione, rosso) e di **emergenza**.
- Tutti i **comunicati ufficiali** (rilancio social di un comunicato stampa, della Parte 12).
- Tutti gli **aggiornamenti operativi** durante un evento.
- Tutti i post che **citano numeri di emergenza**, orari di servizi o istruzioni di
  autoprotezione.
- Tutti i post **successivamente corretti o ritirati** (sia la versione originale sia la
  correzione — vedi **11.9 bis — Gestione errori e post fuori controllo**).

Non serve archiviare: auguri, ringraziamenti generici, rilanci di attività ordinarie senza
informazioni operative.

#### Dove archiviare

```
static/archivio-social/
├── 2026/
│   ├── 2026-04-21-allerta-gialla-ig-post.png
│   ├── 2026-04-21-allerta-gialla-fb-post.png
│   ├── 2026-04-21-allerta-gialla-x-post.png
│   ├── 2026-04-21-allerta-gialla-tg-post.png
│   └── 2026-04-21-allerta-gialla-correzione-ig.png
└── 2027/
```

Convenzione di naming: `AAAA-MM-GG-argomento-canale-post.png`.

- `argomento`: breve, in kebab-case (es. `allerta-gialla-idro`, `emergenza-incendio-cecchina`).
- `canale`: `ig` (Instagram), `fb` (Facebook), `x` (X / Twitter), `tg` (Telegram).
- `post`: il tipo di artefatto (`post`, `storia`, `reel`, `evento`, `correzione`).

#### Formato

- PNG a piena risoluzione (niente JPEG, per non perdere dettaglio del testo).
- Screenshot che includa: nome account, orario di pubblicazione visibile, corpo del post,
  immagine, hashtag.
- Se il post è una correzione, catturare **sia la correzione sia un riferimento temporale**
  (es. badge "modificato alle…" se la piattaforma lo mostra).

#### Chi archivia

Il pubblicatore (vedi **11.10 — Ruoli e flusso di approvazione**) esegue lo screenshot entro
**due ore** dalla pubblicazione e lo committa al repository con il messaggio:

```
Archivio social: [argomento] del [data] — [canale]
```

#### Durata di conservazione

Gli screenshot restano nel repository **a tempo indeterminato**, come memoria istituzionale.
Non si eliminano neanche se il post corrispondente viene rimosso dal canale: la rimozione
viene invece annotata in un file `README.md` nella cartella dell'anno, con motivazione e data.

---

## Parte 12 — Comunicati stampa (tempo ordinario e tempo emergenziale)

### 12.1 — A cosa serve un comunicato stampa

Il comunicato stampa è lo strumento con cui il Gruppo comunica ufficialmente con i media. Nasce
per essere:

- **Ripreso** dai giornalisti anche senza riscrittura.
- **Archiviato** come documento istituzionale verificabile.
- **Condiviso** con altri enti (Comune, Regione, Prefettura, altre protezioni civili).
- **Pubblicato** sul sito del Gruppo come articolo, per essere consultabile dai cittadini.

Per questo motivo il comunicato ha una forma più rigorosa di un post social e una struttura
più asciutta di un articolo divulgativo. È un testo che deve resistere al taglia-e-incolla
del giornalista.

### 12.2 — Due tipologie

| Tipo | Quando | Tempi di redazione | Canali |
|---|---|---|---|
| **Comunicato ordinario** | Attività istituzionali, eventi, formazione, reclutamento, bilanci, anniversari, ringraziamenti | Ore o giorni | Mail a testate, sito, social |
| **Comunicato emergenziale** | Evento in corso o appena concluso: maltempo, incendio, sisma, attivazione straordinaria | Minuti | Mail a testate, sito, social, Telegram |

Le due tipologie hanno struttura simile ma tono e tempi diversi. Un comunicato emergenziale scritto
con ritmo ordinario arriva tardi; un comunicato ordinario scritto con ritmo emergenziale suona
allarmistico.

### 12.3 — Struttura del comunicato ordinario

Ogni comunicato ordinario contiene, in quest'ordine:

1. **Intestazione istituzionale** — nome completo del Gruppo e dicitura "Comunicato stampa".
2. **Data e luogo di emissione** — "Genzano di Roma, 21 aprile 2026".
3. **Occhiello** (opzionale, una riga) — inquadra il tema. Es.: *"Protezione civile e territorio"*.
4. **Titolo** — informativo, non promozionale. Max 80 caratteri. Es.: *"Il Gruppo Comunale Volontari
   apre le iscrizioni al corso base 2026"*.
5. **Sottotitolo** (opzionale, una riga) — aggiunge un'informazione concreta. Es.: *"Dodici lezioni
   serali da maggio a luglio, iscrizioni entro il 30 aprile."*
6. **Lead (primo paragrafo)** — risponde alle 5W classiche: chi, cosa, dove, quando, perché.
   Max 60 parole.
7. **Corpo** — 2-4 paragrafi discorsivi. Dettagli, contesto, virgolettati.
8. **Virgolettato istituzionale** (facoltativo ma consigliato) — vedi 12.6.
9. **Chiusura con riferimenti** — rimando al sito, eventuali allegati, scadenze.
10. **Blocco firma** — vedi 12.7.
11. **Note per la redazione** (facoltativo) — informazioni operative per il giornalista (disponibilità
    del Coordinatore per interviste, presenza di materiale fotografico, orari di un evento).

Lunghezza complessiva consigliata: **300-500 parole**. Mai sopra 800.

### 12.4 — Struttura del comunicato emergenziale

In emergenza la priorità è far arrivare **fatti verificati** nel minor tempo possibile. La struttura
si semplifica:

1. **Intestazione** — nome del Gruppo e dicitura "Comunicato stampa — Emergenza in corso" (o
   "Comunicato stampa — Aggiornamento emergenza").
2. **Timestamp preciso** — "Genzano di Roma, 21 aprile 2026, ore 14:30". L'orario serve al
   giornalista per datare l'informazione.
3. **Apertura standardizzata** — *"Il Gruppo Comunale Volontari di Protezione Civile di Genzano
   di Roma comunica che…"*. Questa formula rende subito chiaro che è una comunicazione ufficiale.
4. **Cosa è successo / sta succedendo** — in un solo paragrafo breve, solo fatti verificati.
   Niente stime, niente congetture, niente aggettivi.
5. **Dove** — area o vie interessate, con precisione.
6. **Quando** — orario di inizio evento e orario attuale.
7. **Chi è stato attivato** — forze in campo (Gruppo volontari, Polizia Locale, Vigili del Fuoco,
   ASL, ecc.) senza millantare.
8. **Istruzioni ai cittadini** — cosa fare, cosa evitare, sempre rinviando al 112 per emergenze.
9. **Rimando al sito** — *"Gli aggiornamenti vengono pubblicati in tempo reale su
   protezionecivilegenzano.it e sul canale Telegram."*
10. **Blocco firma**.
11. **Prossimo aggiornamento** — quando verrà diffuso il prossimo comunicato (es. *"Prossimo
    aggiornamento alle ore 17:00 o in caso di variazioni significative"*).

Lunghezza consigliata: **150-300 parole**. In emergenza il meno è più.

### 12.4 bis — Holding statement (dichiarazione dei primi 15 minuti)

Nei primi 15 minuti di un evento in corso non si dispone ancora di un quadro verificato dei
fatti, ma **il silenzio istituzionale alimenta il rumore sui canali non ufficiali**. In questo
intervallo si pubblica una dichiarazione di 40-60 parole — il *holding statement* — che fa
tre cose soltanto:

1. **Riconoscere** che un evento è in corso (senza descriverlo se non è ancora chiaro).
2. **Dichiarare** che il Gruppo e le autorità competenti sono attivati.
3. **Rimandare** ai canali ufficiali per gli aggiornamenti verificati.

Il holding statement **non** anticipa cause, numeri, vittime, zone precise, o valutazioni. Se
non si sa, si dice che non si sa ancora.

#### Template holding statement — primi 15 minuti

```
[Genzano di Roma, DD mese AAAA, ore HH:MM]

Il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma conferma di avere
attivato le procedure di intervento per un evento in corso sul territorio comunale. È in
corso il coordinamento con le autorità competenti. I primi aggiornamenti verificati saranno
pubblicati entro [orario preciso, tipicamente 30-60 minuti] sul sito
protezionecivilegenzano.it e sul canale Telegram ufficiale.

Per emergenze: 112.
```

(50 parole circa.)

Il holding statement va pubblicato **su tutti i canali** simultaneamente (sito, Telegram,
Facebook, Instagram, X) entro 15 minuti dalla presa in carico dell'evento, anche se i dati
operativi mancano ancora. Il primo aggiornamento strutturato — Template B di 12.10 — arriva
dopo, quando i fatti sono verificati.

Se l'evento si chiarisce rapidamente (falso allarme, rientro, intervento minore), il
holding statement viene superato direttamente dal comunicato completo.

### 12.5 — Regole di linguaggio in emergenza

Queste regole sono vincolanti e non negoziabili.

- **Niente aggettivi enfatici**: no *"drammatico", "terribile", "gravissimo"*. Sì *"l'evento
  coinvolge", "è in corso", "sono previsti"*.
- **Niente stime non verificate**: *"alcune decine di abitazioni"* si dice solo dopo conferma
  operativa. Meglio *"al momento sono in corso le verifiche sul numero di abitazioni coinvolte"*.
- **Niente numeri non confermati di persone**: non pubblicare mai un conteggio di feriti, sfollati
  o vittime prima della conferma degli enti competenti (112, ASL, Prefettura, sindaco).
- **Niente previsioni non ufficiali**: solo bollettini del Centro Funzionale Regionale Lazio,
  Dipartimento di Protezione Civile, ARPA Lazio.
- **Distinguere "previsto" da "in corso"**: sono due realtà diverse per il cittadino.
- **Sempre il 112** come unico numero di emergenza da comunicare al cittadino. Non 115, 118, 1515.
  (Vedi regola `.claude/rules/06-protezione-civile-scientifica.md`.)
- **Niente accuse o polemiche**: il comunicato riporta fatti, non posizioni.
- **Niente promesse**: no *"risolveremo entro sera"*. Sì *"le operazioni proseguono fino al
  ripristino della sicurezza"*.
- **Privacy assoluta**: nessun nome di persona coinvolta, nessun indirizzo specifico di abitazione,
  nessun dato sanitario.

### 12.6 — Virgolettati

I virgolettati rendono il comunicato più "vivo" per la stampa e sono spesso ripresi integralmente.
Regole:

- **Sempre attribuiti** a una persona con nome e ruolo. *"Ha dichiarato il Coordinatore del Gruppo
  Comunale Volontari Mario Rossi."*
- **Verificati con l'interessato prima dell'invio**. Mai virgolettare a memoria.
- **Brevi**: 1-3 frasi, complessivamente sotto le 60 parole.
- **In italiano corretto**: anche un virgolettato va revisionato prima della pubblicazione.
- **Mai polemici o politici**.
- **In emergenza**: il virgolettato è facoltativo e spesso sconsigliato; il tempo va al fatto.

Chi può essere virgolettato:

- **Coordinatore del Gruppo Comunale Volontari** — su attività operative e organizzative del Gruppo.
- **Sindaco di Genzano di Roma** — su decisioni di competenza comunale (ordinanze, chiusure,
  attivazione COC). Da concordare con l'Ufficio comunicazione del Comune.
- **Assessore delegato alla protezione civile** — su linee di indirizzo.
- **Dirigenti regionali o del Dipartimento** — solo se autorizzati e previa verifica.

### 12.7 — Blocco firma istituzionale

Il blocco firma standard, a chiusura di ogni comunicato, è:

```
— — —

Gruppo Comunale Volontari di Protezione Civile
Comune di Genzano di Roma

Sito: https://www.protezionecivilegenzano.it/
Canale Telegram: [inserire link ufficiale]
Instagram: [inserire handle ufficiale]

Contatti per la stampa: [indirizzo email ufficiale da definire]
```

#### Varianti

**Comunicato su attività operative o decisioni del Gruppo**:

```
— — —

Il Coordinatore
Gruppo Comunale Volontari di Protezione Civile
Comune di Genzano di Roma
```

**Comunicato su decisioni di competenza comunale (ordinanze, COC, chiusure strade)**:

```
— — —

Il Sindaco del Comune di Genzano di Roma
Il Coordinatore del Gruppo Comunale Volontari di Protezione Civile
```

**Comunicato emergenziale**:

```
— — —

Sala operativa del Gruppo Comunale Volontari di Protezione Civile
Comune di Genzano di Roma

Contatti per la stampa: [indirizzo email ufficiale]
Prossimo aggiornamento: [orario previsto]
```

Il nome del Coordinatore in carica e del Sindaco si inseriscono solo quando richiesto
esplicitamente: i ruoli cambiano nel tempo, la firma istituzionale resta stabile.

### 12.8 — Archiviazione e pubblicazione

Ogni comunicato stampa viene pubblicato **anche come articolo sul sito**, nella cartella
`content/comunicazioni/`.

Regole di archiviazione:

- **Nome del file**: `AAAA-MM-GG-cs-breve-descrizione.md`. Il prefisso `cs-` identifica i
  comunicati stampa rispetto agli altri articoli.
- **Badge**: `Comunicazione` per comunicati ordinari; `Emergenza` o `Allerta` per quelli
  emergenziali (in coerenza con la palette categorie in `.claude/rules/02-content-design-pa.md`).
- **Priorità**: `normale` per ordinari; `urgente` per emergenziali.
- **Scadenza**: per comunicati legati a eventi con data (es. iscrizioni, esercitazioni), indicare
  la data di scadenza. Dopo quella data l'articolo resta ma esce dai rilievi in homepage.
- **Frontmatter**: tutti i campi obbligatori dell'archetipo `comunicazioni.md`. Vedi **Parte 1.4**.
- **Allegati**: se esiste una versione PDF firmata del comunicato inviata alla stampa, va caricata
  in `static/comunicati/AAAA/` e linkata nel campo `allegati:` del frontmatter.
- **Immagine di copertina**: si applica la fascia blu istituzionale come per ogni articolo. Vedi
  **Parte 3.8**.

### 12.9 — Distribuzione ai media

- Destinatari: testate locali dei Castelli Romani, testate regionali, uffici stampa di Comune,
  Regione, Dipartimento di Protezione Civile. L'elenco specifico non è fissato nel manuale perché
  le testate cambiano nel tempo: viene mantenuto in un foglio di lavoro separato condiviso con
  il Coordinatore.
- Formato di invio: testo nel corpo della mail + PDF firmato in allegato + immagine di copertina
  a bassa risoluzione.
- Oggetto mail: per ordinario, *"Comunicato stampa — [titolo breve] — Protezione Civile Genzano"*;
  per emergenziale, *"COMUNICATO URGENTE — [tema] — Protezione Civile Genzano"*.
- Mittente: indirizzo email istituzionale del Gruppo, mai indirizzi personali dei volontari.

### 12.10 — Template operativi

#### Template A — Comunicato ordinario (esempio: apertura iscrizioni corso base)

```
Gruppo Comunale Volontari di Protezione Civile
Comune di Genzano di Roma

COMUNICATO STAMPA

Genzano di Roma, 21 aprile 2026

Protezione civile e formazione

Il Gruppo Comunale Volontari apre le iscrizioni al corso base 2026

Dodici lezioni serali da maggio a luglio, iscrizioni entro il 30 aprile.

Da lunedì 5 maggio prende il via il corso base per nuove volontarie e nuovi
volontari del Gruppo Comunale di Protezione Civile di Genzano di Roma. Il
percorso formativo, gratuito e aperto a residenti maggiorenni, si svolge nella
sede comunale di via […] e dura dodici lezioni serali, fino al 24 luglio.

Il corso affronta i fondamenti del sistema nazionale di protezione civile, i
principali rischi del territorio dei Castelli Romani (idrogeologico, incendi
boschivi, sismico) e le procedure operative di base. Al termine del corso, le
persone formate potranno scegliere una specializzazione fra radiocomunicazioni,
logistica, avvistamento antincendio e assistenza alla popolazione.

"Il corso base è il punto di ingresso nel Gruppo: non chiede competenze
tecniche preliminari, ma impegno e costanza" — ha dichiarato il Coordinatore
del Gruppo Comunale Volontari.

Le iscrizioni si chiudono il 30 aprile 2026. Il modulo e il programma completo
sono disponibili sul sito protezionecivilegenzano.it alla pagina
"Diventa volontario".

— — —

Il Coordinatore
Gruppo Comunale Volontari di Protezione Civile
Comune di Genzano di Roma

Sito: https://www.protezionecivilegenzano.it/
Contatti per la stampa: [indirizzo email ufficiale]

Note per la redazione: è disponibile materiale fotografico di precedenti
edizioni del corso. Il Coordinatore è disponibile per interviste previo
accordo telefonico.
```

#### Template B — Comunicato emergenziale (esempio: attivazione per maltempo)

```
Gruppo Comunale Volontari di Protezione Civile
Comune di Genzano di Roma

COMUNICATO STAMPA — Emergenza in corso

Genzano di Roma, 21 aprile 2026, ore 14:30

Il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma comunica
di avere attivato alle ore 13:15 le proprie squadre operative a seguito delle
precipitazioni intense in corso sul territorio comunale.

Due squadre del Gruppo stanno presidiando via Nemorense e via dei Laghi a
supporto della Polizia Locale, che ha chiuso temporaneamente un tratto di via
Nemorense per allagamento.

L'allerta meteo diramata dal Centro Funzionale Regionale del Lazio per la
giornata odierna è di livello arancione per rischio idrogeologico sulla zona
dei Castelli Romani.

Si raccomanda alla cittadinanza di limitare gli spostamenti non necessari, di
non sostare in sottopassi o aree soggette ad allagamento e di non avvicinarsi
a corsi d'acqua o tombini in esondazione. Per emergenze chiamare il 112.

Gli aggiornamenti vengono pubblicati in tempo reale su
protezionecivilegenzano.it e sul canale Telegram del Gruppo.

— — —

Sala operativa del Gruppo Comunale Volontari di Protezione Civile
Comune di Genzano di Roma

Contatti per la stampa: [indirizzo email ufficiale]
Prossimo aggiornamento: ore 17:00 o in caso di variazioni significative.
```

#### Template C — Aggiornamento emergenziale (evoluzione o chiusura)

```
Gruppo Comunale Volontari di Protezione Civile
Comune di Genzano di Roma

COMUNICATO STAMPA — Aggiornamento emergenza

Genzano di Roma, 21 aprile 2026, ore 22:00

Il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma comunica
che alle ore 21:45 si è conclusa l'attivazione straordinaria avviata alle
13:15 per il maltempo che ha interessato il territorio comunale nella giornata
odierna.

Durante l'attivazione sono stati impiegati sei volontari in due squadre
operative, a supporto della Polizia Locale per la chiusura temporanea di un
tratto di via Nemorense. Il tratto è stato riaperto alle 20:30 dopo il
ripristino delle condizioni di sicurezza.

Non si registrano persone coinvolte. Non si registrano danni rilevanti alle
abitazioni sulla base delle segnalazioni pervenute alle ore 22:00.

Il resoconto completo dell'attivazione sarà pubblicato nelle prossime ore sul
sito protezionecivilegenzano.it

— — —

Sala operativa del Gruppo Comunale Volontari di Protezione Civile
Comune di Genzano di Roma

Contatti per la stampa: [indirizzo email ufficiale]
```

### 12.11 — Checklist pre-invio comunicato stampa

Prima di inviare il comunicato alla stampa e pubblicarlo sul sito:

- [ ] Intestazione istituzionale completa e corretta?
- [ ] Data (ed eventuale orario) precisa e in forma estesa?
- [ ] Titolo informativo, sotto 80 caratteri?
- [ ] Lead risponde alle 5W entro le prime 60 parole?
- [ ] Frasi brevi, voce attiva, italiano corretto?
- [ ] Niente burocratese, niente aggettivi enfatici, niente slogan?
- [ ] Tutti i fatti sono verificati con almeno una fonte operativa?
- [ ] Eventuale virgolettato attribuito, concordato con l'interessato, entro 60 parole?
- [ ] Nessun dato sensibile (nomi di persone coinvolte, indirizzi, salute)?
- [ ] Il 112 è l'unico numero di emergenza citato per il cittadino?
- [ ] La fonte dell'allerta è esplicita (se pertinente)?
- [ ] Rimando al sito presente e corretto?
- [ ] Blocco firma adeguato al contenuto (ordinario / emergenziale / ordinanza)?
- [ ] Se emergenziale: indicato l'orario del prossimo aggiornamento?
- [ ] Versione articolo sul sito (`content/comunicazioni/`) pronta e coerente con il testo del comunicato?
- [ ] Eventuale allegato PDF firmato caricato in `static/comunicati/`?
- [ ] Coordinatore (o Sala operativa, in emergenza) ha approvato la versione finale?

### 12.12 — Integrazione con i social

Ogni comunicato stampa genera **automaticamente** tre output social coordinati:

1. **Articolo sul sito** in `content/comunicazioni/`, versione completa e navigabile.
2. **Post Instagram**, versione breve visuale secondo i template della **Parte 11.11**, con
   rimando al sito.
3. **Post Facebook**, versione discorsiva più estesa con link cliccabile all'articolo del sito
   (su Facebook il formato consente di riportare il comunicato quasi integralmente).
4. **Post X (Twitter)**, versione telegrafica (200-260 caratteri) con link al sito e hashtag
   essenziali.
5. **Messaggio Telegram**, versione compatta con link cliccabile all'articolo del sito.

Le cinque versioni non sono identiche: sono riscritte per il canale ma conservano gli stessi
fatti, lo stesso tono, la stessa fonte. Non si tratta mai di versioni contraddittorie.

Per i comunicati emergenziali, il ritmo di pubblicazione è:

- **Telegram entro 10 minuti** dall'evento (notifica rapida al canale iscritti).
- **X (Twitter) entro 15 minuti** (raggiunge media e istituzioni).
- **Articolo sul sito entro 20 minuti** (versione estesa consultabile).
- **Instagram entro 30 minuti** (versione visuale).
- **Facebook entro 30 minuti** (versione estesa con link al sito cliccabile, eventualmente
  taggando le pagine istituzionali coinvolte).
- **Mail stampa entro 30 minuti**.

In caso di evento molto rapido, l'ordine può essere compresso ma non invertito: Telegram e X
sono sempre i primi canali.

### 12.13 — Allegati ai comunicati

Ai comunicati stampa si applicano le stesse regole su allegati e immagini descritte in
**Parte 11.14**:

- **Immagine di copertina**: sempre con fascia blu istituzionale (Parte 3.8), WebP, 1200 px,
  sotto 200 KB, salvata in `static/images/`.
- **PDF firmato del comunicato** (quando esiste la versione firmata inviata alla stampa):
  salvato in `static/comunicati/AAAA/`, con naming `AAAA-MM-GG-cs-descrizione-breve.pdf`, e
  linkato nel campo `allegati:` dell'articolo che archivia il comunicato sul sito.
- **Allegati informativi** (ordinanze, bollettini, piani di emergenza citati): salvati in
  `static/allegati/AAAA/`, rinominati in modo leggibile, linkati nel frontmatter e citati nel
  testo con dimensione del file.
- **Foto aggiuntive** (es. foto di un intervento): tutte ridimensionate e dotate di fascia blu;
  inserite nell'articolo come galleria o immagini di corpo.

Se il comunicato è emergenziale e chi lo redige riceve immagini dal campo operativo (via radio,
via messaggistica), queste vanno trattate **prima della pubblicazione**, non dopo. Nessuna foto
non istituzionale (cioè senza fascia blu e logo) deve finire sui canali ufficiali.

### 12.14 — Ritorno alla normalità comunicativa

Chiudere bene una fase di emergenza è importante quanto aprirla. Quando l'evento si conclude,
il Gruppo deve comunicare in modo chiaro che **si rientra in fase ordinaria**, per non lasciare
i cittadini in uno stato di allerta percepita che non corrisponde più alla realtà operativa.

#### Cosa fare quando l'emergenza si chiude

1. **Comunicato di chiusura** (Template C di 12.10) — entro 30 minuti dalla fine delle operazioni,
   anche se breve.
2. **Aggiornamento sul sito** — il banner di emergenza (`data/emergenza.json`, campo `attiva`)
   viene riportato a `false`. Eventuale allerta meteo (`data/allerta.json`) riallineata al livello
   reale (verde se non c'è più allerta).
3. **Messaggio Telegram di chiusura** — ripin-ato al posto del messaggio di allerta iniziale.
   Dopo 24 ore, l'unpin del messaggio di emergenza restituisce il canale all'uso ordinario.
4. **Post di chiusura** su Instagram, Facebook e X — brevissimo, con rimando al sito:

   > *"L'attivazione di oggi si è conclusa alle [orario]. Il dettaglio su
   > protezionecivilegenzano.it. Grazie ai volontari, alle forze coinvolte e alla cittadinanza."*

5. **Ringraziamento separato** — eventuale post dedicato ai volontari e alle forze coinvolte,
   pubblicato **nelle 24 ore successive** alla chiusura, mai contestualmente al comunicato di
   chiusura (si perde la funzione operativa dell'informazione).
6. **Resoconto operativo** — articolo sul sito entro 7 giorni, con: cronologia, forze impiegate,
   risorse, lezioni apprese. Utile come memoria istituzionale e materiale per la comunicazione
   del Gruppo nei mesi successivi.

#### Errori tipici da evitare

- Lasciare il banner di emergenza attivo sul sito per giorni dopo la chiusura operativa.
- Continuare a pubblicare "aggiornamenti" quando non ci sono più fatti nuovi: il silenzio
  informato è meglio del rumore per tenere alto l'engagement.
- Mescolare la chiusura dell'emergenza con ringraziamenti lunghi o contenuti celebrativi: il
  cittadino vuole sapere se può tornare alla normalità, non leggere elogi.
- Chiudere sui social ma dimenticare di riallineare il sito (o viceversa): la coerenza
  cross-canale è un indicatore di affidabilità istituzionale.

#### Note SEO e dati strutturati

Gli articoli di tipo comunicato stampa pubblicati su `content/comunicazioni/` beneficiano
dell'inserimento di metadati **schema.org / JSON-LD** di tipo `NewsArticle` (o
`GovernmentNotice` per comunicati ufficiali), nell'`head` del template `single.html`, con
campi `headline`, `datePublished`, `dateModified`, `author` (Organization: Gruppo Comunale
Volontari…), `publisher`, `image`. Questo migliora la ripresa da parte degli aggregatori di
Google News e facilita il riconoscimento dei contenuti istituzionali dai motori di ricerca.

Il dettaglio tecnico dell'integrazione va discusso con lo sviluppatore del tema, ma il
manuale prescrive che ogni comunicato debba essere accompagnato da questi metadati a partire
dalla prima pubblicazione utile.

---

## Parte 13 — Social Media Policy pubblica

### 13.1 — A cosa serve la Social Media Policy

La Social Media Policy è il documento pubblico che spiega ai cittadini **come si comporta** il
Gruppo sui propri canali social, **cosa chiede** a chi commenta o scrive, e **quali limiti**
pone alla comunicazione digitale. È una promessa di trasparenza: il cittadino sa in anticipo
cosa aspettarsi e può valutare se il comportamento dell'istituzione è coerente con quanto
dichiarato.

Il documento copre due ambiti:

- **Social Media Policy esterna** (*netiquette*) — le regole di comportamento attese da chi
  interagisce con i canali del Gruppo. È pubblicata su
  [`/social-media-policy/`](/social-media-policy/) del sito ed è linkata in ciascuna biografia
  di canale.
- **Social Media Policy interna** — le regole operative per i volontari, i redattori e il
  pubblicatore. È documentata **in questo manuale** (Parte 11 e Parte 12).

### 13.2 — Principi

La policy pubblica si fonda su tre principi semplici, coerenti con le linee guida per la
comunicazione digitale della PA:

1. **Chiarezza** — il cittadino deve sapere chi parla, in che nome, con quali orari e con
   quali limiti. Niente finzioni di presidio H24 se non è vero.
2. **Rispetto** — il confronto sulle pagine istituzionali è benvenuto, le offese personali e le
   violazioni di legge non lo sono. I criteri di moderazione sono pubblici.
3. **Trasparenza** — gli errori si correggono in modo visibile (**11.9 bis**). La cancellazione
   silenziosa non appartiene a una comunicazione pubblica istituzionale.

### 13.3 — Contenuti obbligatori della pagina /social-media-policy

La pagina pubblica deve contenere, come minimo:

- **Elenco dei canali ufficiali** con link diretti e handle, indicando per ciascuno se
  verificato dalla piattaforma.
- **Chi scrive**: il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma, con
  citazione esplicita della natura istituzionale.
- **Orari di presìdio dichiarati onestamente**: indicare la fascia in cui i messaggi e i
  commenti vengono tipicamente letti (es. *"Lun-ven 9-18, in emergenza h24 sul canale
  Telegram; per le emergenze il canale unico è il 112"*). Non promettere H24 su tutti i
  canali se non è sostenibile da una struttura di volontariato.
- **Tipi di contenuti pubblicati**: informazioni istituzionali, allerte meteo, comunicati,
  aggiornamenti operativi, formazione, reclutamento volontari, prevenzione.
- **Licenza dei contenuti**: Creative Commons Attribuzione 4.0 Internazionale (CC BY 4.0),
  coerente con la pagina [Note legali](/note-legali/). Con le eccezioni della 11.16.
- **Netiquette per i commenti**: cosa è accettato, cosa viene moderato.
- **Criteri di moderazione**: quando un commento viene nascosto o rimosso, e come si fa
  ricorso.
- **Gestione degli errori**: rimando a 11.9 bis del manuale operativo, con sintesi per il
  cittadino (*"Se sbagliamo un post, lo modifichiamo con un timestamp visibile e lo diciamo
  chiaramente. Non cancelliamo in silenzio"*).
- **Responsabilità editoriale**: chi firma la comunicazione (Gruppo + Coordinatore + Comune).
- **Canale di contatto per segnalazioni** sulla policy stessa (email istituzionale).

### 13.4 — Netiquette per i commenti

Sono **benvenuti** sui nostri canali i commenti che:

- **chiedono informazioni** sui contenuti pubblicati;
- **segnalano errori** o imprecisioni, così che possiamo correggere;
- **condividono esperienze** utili alla comunità;
- **esprimono critiche** argomentate, anche severe, sull'operato del Gruppo o delle istituzioni.

Sono **moderati** (nascosti o rimossi) i commenti che:

- contengono **insulti**, **minacce**, **linguaggio d'odio** o discriminazioni;
- diffondono **informazioni false** su rischi, allerte, emergenze in corso;
- contengono **dati personali** di terzi (nomi, indirizzi, targhe, numeri di telefono) senza
  consenso;
- sono **spam**, promozione commerciale, catene o contenuti fuori tema ripetuti;
- sono **minacce** a persone o istituzioni;
- fanno **propaganda politica**, elettorale o di parte (il Gruppo è un ente di volontariato,
  non un soggetto politico).

I criteri di moderazione sono applicati nello stesso modo a tutti, indipendentemente dalla
posizione espressa.

### 13.5 — Ricorso

Chi ritiene che un proprio commento sia stato moderato ingiustamente può scrivere
all'indirizzo istituzionale del Gruppo (da pubblicare sulla pagina). La Sala comunicazione
rivede la decisione entro sette giorni lavorativi.

### 13.6 — Cosa NON facciamo

Per trasparenza verso il cittadino, esplicitiamo anche ciò che il Gruppo **non fa** sui
propri canali:

- Non seguiamo account personali o politici.
- Non accettiamo pubblicità a pagamento, non promuoviamo prodotti o servizi commerciali.
- Non pubblichiamo foto o video di persone coinvolte in eventi di emergenza senza
  liberatoria.
- Non diffondiamo previsioni meteo da fonti non istituzionali.
- Non rispondiamo in privato su emergenze in corso: in quel caso il canale unico è il 112.
- Non siamo un servizio di emergenza: il servizio è il 112.

### 13.7 — Aggiornamenti della policy

La Social Media Policy pubblica viene rivista almeno una volta l'anno, in corrispondenza
della verifica periodica delle linee guida AGID / Designers Italia descritta nella Parte 13
di questo manuale (v. workflow `.github/workflows/aggiorna-manuale.yml`). Ogni revisione
viene annotata nel changelog in cima al manuale e nella pagina pubblica con la formula
*"Versione aggiornata al DD/MM/AAAA"*.

### 13.8 — Coerenza con la normativa

La presente policy è redatta in coerenza con:

- **Linee guida per la comunicazione digitale della PA** (AGID / Dipartimento per la
  Trasformazione digitale).
- **Decreto-legge 14 marzo 2025 n. 25**, convertito con modificazioni dalla **Legge 9 maggio
  2025 n. 69**, che disciplina il ruolo del *Social Media Manager* e del *Digital Manager*
  nella PA (vedi **11.10 — Ruoli e flusso di approvazione**).
- **Regolamento UE 2016/679 (GDPR)** per la gestione dei dati personali eventualmente emersi
  dai commenti.
- **Legge 4/2004 (Stanca)** e **Direttiva UE 2016/2102** sull'accessibilità dei contenuti
  digitali della PA.
- **Codice dell'amministrazione digitale** (D.Lgs. 82/2005 e successive modificazioni).
- **D.Lgs. 1/2018** (Codice della Protezione Civile) per il quadro di riferimento operativo.

---

## Appendici

### Appendice A — Colori del sito

| Variabile CSS | Valore | Uso |
|---|---|---|
| `--pc-primary` | `#003366` | Blu istituzionale principale, fascia immagini |
| `--pc-primary-dark` | `#00244d` | Variante scura |
| `--pc-primary-light` | `#004080` | Variante chiara |
| `--pc-secondary` | `#FF6600` | Arancione accento |
| `--pc-accent` | `#009246` | Verde |
| `--pc-danger` | `#d9364f` | Rosso emergenze |
| `--pc-warning` | `#FFC107` | Giallo allerta |

### Appendice B — Struttura delle cartelle

```
sito-pc-genzano/
├── archetypes/                     Template frontmatter per nuovi articoli/pagine
├── content/
│   ├── comunicazioni/              Articoli (Parte 1)
│   └── <altre-sezioni>/            Pagine statiche (Parte 4)
├── data/                           File dati: allerta.json, emergenza.json, numeri_utili.yaml, ecc.
├── static/
│   ├── images/                     Immagini (Parte 3)
│   ├── documenti/                  PDF e allegati
│   ├── giochi/                     Giochi interattivi (standalone)
│   ├── cartelli/                   Immagini cartelli area emergenza
│   └── app-shared/                 site-chrome.js (header/footer per pagine standalone)
├── themes/flavour-pcgenzano/       Tema custom, modificabile
│   ├── layouts/                    Template Hugo
│   └── static/css/                 CSS custom
├── layouts/                        Override locali (shadowing del tema)
├── .claude/rules/                  Regole per Claude Code
├── .github/workflows/              GitHub Actions (deploy, aggiornamento manuale)
├── hugo.toml                       Configurazione Hugo
├── CLAUDE.md                       Istruzioni per Claude Code
└── MANUALE-SITO.md                 Questo file
```

### Appendice C — Comandi rapidi

```bash
# Avviare il sito in locale (solo contenuti pubblicati)
hugo server

# Avviare il sito in locale (mostra anche le bozze)
hugo server -D

# Nuovo articolo
hugo new comunicazioni/AAAA-MM-GG-titolo-breve.md

# Build di produzione (verifica pre-push)
hugo --minify

# Build con baseURL di produzione (Aruba)
hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"

# Commit e push (pubblica)
git add .
git commit -m "descrizione breve"
git push origin main

# Rollback dell'ultimo commit (se qualcosa è andato storto)
git revert HEAD
git push origin main

# Lanciare il check manuale del manuale
gh workflow run aggiorna-manuale.yml
```

### Appendice D — Glossario

| Termine | Significato |
|---|---|
| **AGID** | Agenzia per l'Italia Digitale |
| **AIB** | Antincendio Boschivo |
| **ARPA** | Agenzia Regionale per la Protezione Ambientale |
| **Bootstrap Italia** | Framework CSS/JS ufficiale per siti PA italiani |
| **COC** | Centro Operativo Comunale |
| **CSS** | Cascading Style Sheets — linguaggio per lo stile delle pagine web |
| **DPC** | Dipartimento della Protezione Civile |
| **ETS** | Ente del Terzo Settore |
| **Fepivol** | Coordinamento regionale volontari PC Lazio |
| **Frontmatter** | Intestazione YAML in cima a ogni file `.md`, contiene metadati |
| **Hugo** | Generatore di siti statici usato per questo sito |
| **Markdown** | Linguaggio leggero di formattazione del testo (`**grassetto**`, `# Titolo`) |
| **NUE** | Numero Unico di Emergenza (il 112) |
| **OG (Open Graph)** | Metadata per le anteprime su social (Facebook, LinkedIn, ecc.) |
| **RUNTS** | Registro Unico Nazionale Terzo Settore |
| **SEO** | Search Engine Optimization |
| **Slug** | Versione URL-friendly di un titolo (`titolo-dell-articolo`) |
| **WCAG** | Web Content Accessibility Guidelines |
| **WebP** | Formato immagine moderno, più leggero di JPEG/PNG |

### Appendice E — Template pronti

Copia e incolla nel tuo nuovo file.

#### Template articolo breve (avviso o comunicazione)

```markdown
---
title: "Titolo breve e chiaro"
date: 2026-05-15
description: "Sommario in max 160 caratteri. Dice il fatto principale."
badge: "Avviso"
priorita: "normale"
autore: "Gruppo Comunale Volontari PC Genzano"
image: ""
scadenza: ""
area: "Comune di Genzano di Roma"
allegati: []
draft: false
---

**Apertura in grassetto con il fatto principale.** Chi, cosa, dove, quando.

## Cosa succede

Descrizione breve.

## Cosa fare

- Prima azione.
- Seconda azione.
- Terza azione.

## Informazioni

Per chiedere informazioni: 06 9362 600 (segreteria).
```

#### Template articolo lungo (formazione o approfondimento)

```markdown
---
title: "Titolo descrittivo (max 80 caratteri)"
date: 2026-05-15
description: "Sommario SEO in max 160 caratteri."
badge: "Prevenzione"
priorita: "normale"
autore: "Gruppo Comunale Volontari PC Genzano"
image: "/images/2026-05-15-descrizione.webp"
scadenza: ""
area: "Comune di Genzano di Roma"
allegati:
  - titolo: "Checklist PDF (120 KB)"
    url: "/documenti/checklist.pdf"
draft: false
---

**Apertura forte in grassetto.** Il fatto principale in una frase chiara.

---

## Contesto

Breve inquadramento storico o normativo.

---

## Punto principale 1

Paragrafo esplicativo. Frasi brevi, concetti chiari.

## Punto principale 2

Altro paragrafo.

---

## Cosa puoi fare tu

- Azione concreta 1.
- Azione concreta 2.
- Azione concreta 3.

---

## Numeri utili

- **112** — Numero unico di emergenza
- **06 9362 600** — Segreteria del Gruppo (informazioni non urgenti)

---

*Il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma promuove la cultura
della prevenzione sul territorio.*
```

#### Template comunicato di emergenza

```markdown
---
title: "EMERGENZA: [descrizione breve]"
date: 2026-05-15
description: "Descrizione dell'emergenza in atto, con area e comportamenti da adottare."
badge: "Emergenza"
priorita: "urgente"
autore: "Gruppo Comunale Volontari PC Genzano"
image: ""
scadenza: ""
area: "Zona interessata"
allegati: []
draft: false
---

**In corso una situazione di emergenza in [zona].** [Una frase con il fatto principale.]

## Cosa sta succedendo

Descrizione fattuale, senza allarmismo. Solo informazioni verificate.

## Cosa fare subito

1. Azione immediata 1.
2. Azione immediata 2.
3. Chiama il **112** se vedi persone in pericolo.

## Aree interessate

- Zona 1
- Zona 2

## Aggiornamenti

Questo articolo viene aggiornato in tempo reale. Ultimo aggiornamento: ore HH:MM.

---

*Il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma è attivo sul
territorio. Per emergenze chiama sempre il **112**.*
```

#### Template pagina

```markdown
---
title: "Titolo della pagina"
description: "Sommario SEO (max 160 caratteri)."
draft: false
---

Breve introduzione di una-due frasi.

## Sezione principale 1

Contenuto.

## Sezione principale 2

Contenuto.

## Contatti

Per informazioni su questa pagina: 06 9362 600 o [segreteria@protezionecivilegenzano.it](mailto:segreteria@protezionecivilegenzano.it).
```

### Appendice F — Errori comuni e come evitarli

| Errore | Conseguenza | Come evitarlo |
|---|---|---|
| `date: 2026-05-15T10:00:00Z` | Articolo escluso dalla build | Usa solo `date: 2026-05-15` |
| `draft: true` dimenticato | Articolo non pubblicato | Metti `draft: false` prima del push |
| Description > 160 caratteri | Troncata in Google/social | Verifica con `echo "..." | wc -m` |
| Badge inventato | Colore random (potrebbe cozzare) | Usa la tabella del Passo 1.2 |
| Immagine senza fascia blu | Incoerenza visiva | Segui Parte 3.8 |
| Immagine > 1 MB | Lentezza caricamento | Comprimi in WebP, max 200 KB |
| `+39069362600` nel testo | Illeggibile | Scrivi `06 9362 600` |
| "Cliccate qui" come link | Accessibilità violata | Testo descrittivo del link |
| H1 nel corpo | Gerarchia SEO rotta | H1 solo nel frontmatter, usa H2 nel corpo |
| Alt text "Foto di..." | Screen reader ridondante | Descrivi il contenuto, non il formato |
| `.docx` o `.pages` come allegato | Non tutti possono aprirli | Esporta sempre in PDF |
| Push con build rotto | Sito non aggiornato | Fai `hugo --minify` locale prima del push |

### Appendice G — Risorse esterne ufficiali

**Linee guida AGID e Designers Italia:**

- [designers.italia.it](https://designers.italia.it)
- [docs.italia.it/italia/designers-italia/](https://docs.italia.it/italia/designers-italia/)
- [Writing Toolkit](https://designers.italia.it/risorse-per-il-design/writing-toolkit/)
- [Manuale operativo design PA](https://docs.italia.it/italia/designers-italia/manuale-operativo-design-docs/)
- [Linee guida accessibilità AGID](https://www.agid.gov.it/it/design-servizi/accessibilita)

**Protezione civile:**

- [Dipartimento della Protezione Civile](https://www.protezionecivile.gov.it/)
- [Agenzia Regionale di Protezione Civile Lazio](https://www.regione.lazio.it/cittadini/protezione-civile)
- [Centro Funzionale Regionale Lazio](https://www.regione.lazio.it/rl/centrofunzionale/)
- [IT-alert](https://www.it-alert.it/)

**Framework e strumenti:**

- [Bootstrap Italia](https://italia.github.io/bootstrap-italia/)
- [Hugo](https://gohugo.io/)
- [GitHub Actions per Hugo](https://github.com/peaceiris/actions-hugo)

**Strumenti per immagini:**

- [Squoosh](https://squoosh.app) — conversione e compressione
- [Canva](https://canva.com) — editor online
- [GIMP](https://gimp.org) — editor desktop gratuito
- [Unsplash](https://unsplash.com) — foto libere CC0
- [Pexels](https://pexels.com) — foto libere CC0

**Verifica accessibilità:**

- [WAVE](https://wave.webaim.org/) — validatore accessibilità
- [Lighthouse](https://developer.chrome.com/docs/lighthouse/) — incluso in Chrome DevTools
- [axe DevTools](https://www.deque.com/axe/devtools/) — estensione browser

**Verifica SEO:**

- [Google Search Console](https://search.google.com/search-console)
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)

---

*Fine del manuale. Per domande non coperte qui, apri un'Issue sul repository o contatta
il Chief Digital Officer del Gruppo.*
