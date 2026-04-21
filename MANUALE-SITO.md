# Manuale Operativo — Sito Protezione Civile Genzano di Roma

**Versione:** 2.1
**Ultimo aggiornamento manuale:** 2026-04-21
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
    url: "/documenti/ordinanza-42-2026.pdf"
  - titolo: "Mappa aree di attesa (PDF, 1,2 MB)"
    url: "/documenti/mappa-aree-attesa.pdf"
```

- Il `titolo` deve indicare **tipo** (PDF, ODT, DOCX) e **dimensione** del file.
- L'`url` è il percorso relativo (se il PDF è in `static/documenti/`, l'URL è `/documenti/...`).
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

1. Metti il file in `static/documenti/` (es. `static/documenti/ordinanza-42-2026.pdf`).
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

Se la pagina deve apparire nella navbar, modifica `hugo.toml`:

```toml
[[menus.main]]
  name = "Nome nel menu"
  url = "/url-pagina/"
  weight = 10
```

`weight` determina l'ordine (più basso = più a sinistra). Valori attuali:

| Peso | Voce |
|---|---|
| 1 | Home |
| 2 | Chi Siamo |
| 3 | Rischi e Prevenzione |
| 4 | Allerte Meteo |
| 5 | Comunicazioni |
| 6 | Formazione |
| 7 | Giochi |
| 8 | Diventa Volontario |
| 9 | Contatti |

Per inserire una voce tra due esistenti, aumenta il peso di quelle che devono stare a
destra.

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

### 4.6 — Pagine esistenti sul sito

| URL | File | Note |
|---|---|---|
| `/` | `layouts/index.html` | Homepage dinamica (normale/emergenza) |
| `/chi-siamo/` | `content/chi-siamo/_index.md` | |
| `/rischi-prevenzione/` | `content/rischi-prevenzione/_index.md` | Hub + 9 sotto-pagine |
| `/allerte-meteo/` | `content/allerte-meteo/_index.md` | |
| `/comunicazioni/` | Generata da Hugo | Elenco articoli |
| `/formazione/` | `content/formazione/_index.md` | Include 4 kit scuola |
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
| Link interno `/...` verso pagina esistente | `<a href="/...">testo</a>` — anchor normale |
| Link interno `/...` verso pagina non trovata | `<span class="text-muted" title="Contenuto non ancora disponibile">testo</span>` — testo inerte |
| Link esterno `http://` o `https://` | `<a href="..." target="_blank" rel="noopener noreferrer">testo</a>` |
| Link `tel:` o `mailto:` | `<a href="..." safeURL>testo</a>` |
| Altri formati (ancore `#...`, relativi, ecc.) | anchor grezzo, nessun controllo |

**Conseguenze per chi scrive:**

- Puoi tranquillamente inserire link markdown verso articoli correlati **anche se non ancora pubblicati**: il giorno in cui l'articolo viene pubblicato, il link diventa attivo automaticamente al deploy successivo.
- Se un lettore vede testo in grigio muto ("Contenuto non ancora disponibile") significa che l'articolo linkato non esiste (tipo, refuso nello slug, o articolo rimosso). Verifica con `hugo server -D`.
- I link esterni si aprono sempre in nuova scheda con `rel="noopener noreferrer"` per sicurezza.
- Frammenti (`#sezione`) e query string vengono ignorati nella lookup: l'hook controlla solo il path.

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

Il repository ha **8 workflow** attivi che automatizzano deploy, controlli, aggiornamenti e audit. Ogni workflow vive in `.github/workflows/*.yml`. Tutti supportano l'esecuzione manuale tramite `workflow_dispatch` dalla tab Actions del repository.

### 10.1 — Panoramica

| Workflow | File | Trigger | Scopo |
|---|---|---|---|
| Build e Deploy | `deploy.yml` | push su `main`, manuale | Build Hugo, deploy Aruba (FTP), deploy GitHub Pages |
| Aggiornamento Allerta Meteo | `check-allerta.yml` | orario (cron `12 * * * *`), manuale | Legge feed DPC, aggiorna `data/allerta.json` |
| Pubblicazione programmata | `pubblica-programmata.yml` | giornaliero (06:00 UTC), manuale | Riavvia il deploy per pubblicare articoli a data futura |
| Verifica link normativa | `check-normativa-links.yml` | 1° del mese (08:00 UTC), manuale | Controlla raggiungibilità portali normativi |
| Audit Accessibilità | `lighthouse-audit.yml` | dopo ogni deploy, manuale | Lighthouse su home e 5 pagine chiave |
| Aggiorna Bootstrap Italia | `update-bootstrap-italia.yml` | lunedì 06:00 UTC, manuale | Verifica nuove release Bootstrap Italia, apre PR |
| Aggiornamento MANUALE | `aggiorna-manuale.yml` | lunedì 06:00 UTC, manuale | Confronta hash fonti AGID/DI, apre Issue se cambiate |
| Coerenza documentazione | `coerenza-docs.yml` | 1° del mese (07:00 UTC), manuale | Verifica coerenza tra CLAUDE.md, archetype, regole, badge |

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

### 10.5 — `check-normativa-links.yml` — Verifica link normativa

**Trigger**: cron mensile (`0 8 1 * *` = 1° del mese alle 08:00 UTC), esecuzione manuale.

**Cosa fa:**
1. Verifica raggiungibilità (HTTP 2xx/3xx) di una lista curata di URL normativi (normattiva.it, agid.gov.it, designers.italia.it, protezionecivile.gov.it, regione.lazio.it, ecc.).
2. Se uno o più URL falliscono, apre una Issue con la lista dei link rotti.

**Quando guardarlo**: solo se arriva una Issue dal bot. La Issue conterrà i link da aggiornare nel sito (tipicamente su `riferimenti-normativi.md` o su pagine di servizio).

### 10.6 — `lighthouse-audit.yml` — Audit Accessibilità e Performance

**Trigger**: `workflow_run` dopo il successo di `deploy.yml`, esecuzione manuale.

**Cosa fa:**
1. Attende che GitHub Pages propaghi (pochi secondi).
2. Esegue Lighthouse CI su un set di URL chiave (home, rischi, allerte, contatti, un articolo recente).
3. Produce un report scaricabile come artifact.
4. Se i punteggi scendono sotto soglia (tipicamente 90 performance, 95 accessibilità, 100 best-practices), apre una Issue.

**Quando guardarlo**: quando un deploy produce una Issue di regressione. Le cause più frequenti sono immagini non ottimizzate, nuovi script bloccanti, contrasti troppo bassi.

### 10.7 — `update-bootstrap-italia.yml` — Aggiornamento Bootstrap Italia

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

### 10.8 — `aggiorna-manuale.yml` — Verifica fonti AGID/Designers Italia

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

### 10.9 — `coerenza-docs.yml` — Coerenza documentazione interna

**Trigger**: cron mensile (1° del mese 07:00 UTC), manuale.

**Cosa fa:**
1. Legge `CLAUDE.md`, `archetypes/comunicazioni.md`, `.claude/rules/*.md`, `MANUALE-SITO.md`, `PIANO-EDITORIALE.md`, `themes/flavour-pcgenzano/layouts/partials/badge.html`.
2. Verifica coerenza interna: le categorie badge elencate in `CLAUDE.md` combaciano con quelle dell'archetype? La palette hex combacia con `custom.css`? I riferimenti tra file non sono rotti?
3. Se trova deviazioni, apre una Issue con la lista puntuale.

**Quando intervenire**: sempre che apra una Issue. La coerenza tra questi file è critica per l'affidabilità delle AI che li usano come guida.

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
