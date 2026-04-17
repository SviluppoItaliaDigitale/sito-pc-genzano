# Manuale Operativo — Sito Protezione Civile Genzano di Roma

**Versione:** 1.0
**Ultimo aggiornamento manuale:** 2026-04-18
**Ultimo check linee guida AGID:** 2026-04-18
**Manuale operativo di design PA:** versione 2025.1
**Bootstrap Italia:** versione 2.17.3
**Writing Toolkit Designers Italia:** versione bozza corrente

> Questo manuale deve essere verificato e aggiornato ogni volta che le linee guida AGID, Designers Italia o il Writing Toolkit vengono modificati. Vedi la sezione "Procedura di aggiornamento" in fondo.

---

## Parte 1 — Come scrivere un articolo

### Istruzioni per AI esterne

Se stai usando un'altra AI (ChatGPT, Gemini, ecc.) per scrivere un articolo, copia e incolla questa intera Parte 1 come prompt iniziale. L'AI deve seguire rigorosamente queste istruzioni.

> **ISTRUZIONE PER L'AI:** Prima di redigere l'articolo, verifica che le date di aggiornamento qui sopra siano recenti (meno di 3 mesi). Se sono più vecchie, avvisa l'utente che questo manuale potrebbe essere obsoleto e che deve essere aggiornato tramite Claude Code. Se le date sono recenti, prosegui con la redazione.

---

### Template frontmatter (copia e incolla)

```yaml
---
title: "Titolo chiaro e informativo (max 80 caratteri)"
date: 2026-04-18
description: "Sommario breve: max 160 caratteri, utile per SEO e anteprima social."

badge: "Comunicazione"
priorita: "normale"
autore: "Gruppo Comunale Volontari PC Genzano"
image: "/images/2026-04-18-nome-descrittivo.webp"
scadenza: ""
area: ""
allegati: []
draft: false
---
```

### Campi del frontmatter — spiegazione completa

| Campo | Obbligatorio | Valori / Formato | Note |
|---|---|---|---|
| `title` | Si | Testo, max ~80 caratteri | Chiaro, informativo, senza enfasi. Descrive il contenuto, non lo pubblicizza. |
| `date` | Si | `AAAA-MM-GG` (es. `2026-04-18`) | **MAI** usare il formato con orario/timezone (`2026-04-18T10:00:00Z`): causa l'esclusione dalla build. |
| `description` | Si | Testo, **max 160 caratteri** | Sommario per SEO e anteprima social. Deve essere autosufficiente. |
| `badge` | Si | Vedi tabella sotto | Categoria dell'articolo. Determina il colore del badge. |
| `priorita` | Si | `"normale"` oppure `"urgente"` | "urgente" aggiunge bordo rosso e badge URGENTE. **Non esistono altri valori** (non usare "alta", "bassa", ecc.). |
| `autore` | Si | Testo | Default: `"Gruppo Comunale Volontari PC Genzano"` |
| `image` | No | Percorso immagine o `""` | Es: `"/images/2026-04-18-nome.webp"`. Vedi sezione Immagini. |
| `scadenza` | No | `AAAA-MM-GG` o `""` | Se compilata, dopo questa data appare un avviso "Comunicazione scaduta". |
| `area` | No | Testo o `""` | Zona geografica: "Comune di Genzano di Roma", "Castelli Romani", "Territorio nazionale", ecc. |
| `allegati` | No | Lista YAML o `[]` | Formato: vedi esempio sotto. |
| `draft` | Si | `true` / `false` | `true` = bozza (non pubblicata), `false` = pubblicata. |

### Categorie badge disponibili

Queste categorie hanno un colore predefinito nel sito:

| Badge | Colore | Quando usarlo |
|---|---|---|
| `"Allerta"` | Rosso | Comunicazioni di allerta meteo o rischio in corso |
| `"Avviso"` | Giallo | Avvisi generali alla popolazione |
| `"Comunicazione"` | Blu scuro | Aggiornamenti istituzionali, notizie del gruppo |
| `"Attivita"` | Azzurro | Attivita ordinarie del gruppo |
| `"Formazione"` | Viola | Corsi, esercitazioni, aggiornamenti tecnici |
| `"Evento"` | Verde | Eventi, manifestazioni, giornate tematiche |
| `"Volontariato"` | Verde scuro | Promozione, iscrizioni, attivita del gruppo |
| `"Radiocomunicazioni"` | Blu medio | Comunicazioni radio, Rete Zamberletti, radioamatori |
| `"Prevenzione"` | Verde acqua | Comportamenti e buone pratiche di prevenzione |
| `"Esercitazione"` | Arancione scuro | Esercitazioni operative |
| `"Aggiornamento"` | Indaco | Aggiornamenti normativi o procedurali |
| `"Informazione"` | Blu chiaro | Contenuti informativi generali |
| `"Emergenza"` | Rosso | Comunicazioni durante emergenze in atto |

**Categorie nuove:** se usi un badge non presente in questa lista, il sito assegna automaticamente un colore dalla palette. Lo stesso nome produce sempre lo stesso colore.

### Esempio allegati

```yaml
allegati:
  - titolo: "Ordinanza sindacale n. 123/2026 (PDF, 240 KB)"
    url: "/documenti/ordinanza-123-2026.pdf"
  - titolo: "Mappa aree di attesa (PDF, 1,2 MB)"
    url: "/documenti/mappa-aree-attesa.pdf"
```

### Nome file dell'articolo

Il file deve chiamarsi: `AAAA-MM-GG-titolo-breve.md`

Esempio: `2026-04-18-esercitazione-antincendio-boschivo.md`

Va salvato nella cartella: `content/comunicazioni/`

---

## Parte 2 — Regole di scrittura (Manuale di Stile AGID integrato)

Queste regole derivano dal Writing Toolkit di Designers Italia, dal Manuale operativo di design della PA e dalle integrazioni specifiche per un sito di Protezione Civile.

### 2.1 — Principi generali

- Scrivi per cittadini reali: famiglie, anziani, volontari, scuole, persone fragili, utenti da mobile.
- Ogni testo deve aiutare a capire **cosa sta succedendo**, **cosa fare** e **dove trovare altre informazioni**.
- Il tono deve essere istituzionale, sobrio e rassicurante. Mai enfatico, promozionale o allarmistico.
- Dai una risposta concreta alle domande: chi, cosa, dove, come, quando.

### 2.2 — Frasi e paragrafi

| Regola | Dettaglio |
|---|---|
| Lunghezza frase | Tendenzialmente sotto le 20 parole. |
| Voce attiva | Sempre preferita. "Scarica il modulo" non "Il modulo puo essere scaricato". |
| Nominalizzazioni | Da evitare. "Paga" non "Effettua il pagamento". "Iscriviti" non "Procedi all'iscrizione". |
| Forma personale | Usa "tu" o "voi" quando ti rivolgi al cittadino. Evita forme impersonali ("si prega di..."). |
| Paragrafi | Brevi. Ogni paragrafo = un concetto. Ricorda che la maggior parte legge da telefono. |
| Informazioni superflue | Non aggiungerne. Vai dritto al punto. |

### 2.3 — Parole e lessico

| Regola | Esempio corretto | Esempio da evitare |
|---|---|---|
| Parole comuni | "casa" | "abitazione" |
| Verbi diretti | "chiama il 112" | "contatta il numero di emergenza" |
| No burocratese | "per chiedere" | "al fine di richiedere" |
| No arcaismi | eliminare del tutto | "ad uopo", "nelle more di", "giusta delibera" |
| Parole straniere | In corsivo se non comuni. Non declinare: "i tablet" non "i tablets". |
| Tecnicismi | Ammessi solo se necessari e spiegati. "NVIS (propagazione quasi verticale)" |

### 2.4 — Numeri, date e formati

| Elemento | Formato nel testo | Esempio |
|---|---|---|
| Date (rivolte al cittadino) | giorno mese anno, mese in minuscolo | "18 aprile 2026", "lunedi 18 aprile" |
| Date (frontmatter Hugo) | `AAAA-MM-GG` | `2026-04-18` |
| Orari (discorsivo) | In lettere | "le quattro e mezzo" |
| Orari (precisi) | Cifre con due punti | "23:59", "08:30" |
| Numeri di telefono | Raggruppati per leggibilita | "06 9362 600", "112" |
| Percentuali (testo) | Cifra + "per cento" | "il 3 per cento" |
| Percentuali (tabelle) | Simbolo % | "3%" |
| Indirizzi | Cifre per il civico | "Via Sicilia 13-15" |
| Unita di misura (tecnico) | Cifra + simbolo SI | "3 km", "25 °C" |
| Unita di misura (generico) | In lettere | "tre chilometri" |
| Separatore decimale | Virgola | "2,5 metri" |
| Numeri romani | Per leggi e secoli | "Titolo V", "XXI secolo" |
| Simboli & e % | Evitare nel testo corrente | Usa "e", "per cento" |

### 2.5 — Formattazione

| Elemento | Regola |
|---|---|
| **Grassetto** | Solo per parole chiave da evidenziare. Preferisci titoli ed elenchi per strutturare. |
| *Corsivo* | Solo per titoli di opere, parole straniere non comuni, termini tecnici alla prima occorrenza. |
| Sottolineato | **Mai** usarlo online: indica un link. |
| Elenchi puntati | Quando ci sono 3+ elementi paralleli. Non per frammentare testo continuo. |
| Elenchi numerati | Quando l'ordine conta (procedure, passaggi). |
| Link | Testo descrittivo, mai "clicca qui". Es: "consulta il [bollettino della Regione Lazio](url)". |
| Link a documenti | Indicare tipo e dimensione: "Ordinanza sindacale (PDF, 120 KB)". |
| Link esterni | Segnalare se aprono nuova finestra. |
| Tabelle | Poche colonne, poco testo. Devono funzionare su mobile. |

### 2.6 — Maiuscole e acronimi

| Regola | Esempio corretto | Esempio da evitare |
|---|---|---|
| Cariche istituzionali | sindaco, assessore, ministro | Sindaco, Assessore |
| Eccezioni | Presidente della Repubblica, Presidente del Consiglio | |
| Ministeri | Ministero della difesa | Ministero della Difesa |
| Dipartimenti | Dipartimento della protezione civile | Dipartimento della Protezione Civile |
| Acronimi | Evitarli se possibile. Se necessari: nome per esteso + acronimo tra parentesi alla prima occorrenza. | |
| Sigle comuni | PA, UE, IVA (ammesse senza scioglimento) | |
| Nomi di servizi | Nomi semplici e generici | Nomi di fantasia o marchi |

### 2.7 — Titoli degli articoli

- Descrittivi: dicono cosa contiene l'articolo.
- Non promozionali: niente "Scopri...", "Incredibile...", "Non perdere...".
- Max ~80 caratteri.
- Coerenti con il contenuto reale.

### 2.8 — Riferimenti normativi

- Spiega il contenuto della norma in linguaggio semplice.
- Non citare articoli e commi nel corpo del testo ("art. 20 comma 2...").
- Inserisci sempre il link alla norma su Normattiva o Gazzetta Ufficiale.
- Se necessario citare, usa una nota a parte.

### 2.9 — Regole specifiche per la Protezione Civile

| Regola | Dettaglio |
|---|---|
| Allerte meteo | Usa solo dati ufficiali del Centro Funzionale Regionale del Lazio. Indica sempre la fonte. |
| Codici colore | Verde, gialla, arancione, rossa. Non usare "massima allerta" per fenomeni ordinari. |
| Distingui sempre | "previsto" vs "in corso", "allerta" vs "emergenza", "informazione" vs "allertamento". |
| Numeri di emergenza | 112 (NUE), 115 (VVF), 118 (sanitaria), 1515 (incendi boschivi). Sempre verificati. |
| Tono | Calmo, informativo, rassicurante. Mai allarmistico. Mai minimizzante se il rischio e reale. |
| Fonti | Citare sempre: "secondo il bollettino del Centro Funzionale Regionale Lazio". |
| Comportamenti | Per autoprotezione, citare fonti ufficiali (DPC, Regione, Comune). |

---

## Parte 3 — Immagini per gli articoli

### 3.1 — Specifiche tecniche

| Parametro | Valore |
|---|---|
| Formato | **WebP** (preferito), JPEG accettato |
| Larghezza | **1200 px** (ideale), minimo 800 px |
| Proporzioni | 16:9 o 3:2 (orizzontale) |
| Dimensione file | Max **200 KB** per WebP, max 300 KB per JPEG |
| Risoluzione | 72 DPI (web) |
| Nome file | `AAAA-MM-GG-descrizione-breve.webp` |
| Percorso | Salvare in `static/images/` |

### 3.2 — Fascia blu istituzionale (obbligatoria)

Ogni immagine di copertina degli articoli deve avere una **fascia blu in basso** con il branding del gruppo. Questa fascia identifica visivamente i contenuti come ufficiali della Protezione Civile di Genzano.

#### Specifiche della fascia

| Parametro | Valore |
|---|---|
| Posizione | In basso, a tutta larghezza |
| Altezza fascia | Circa **15-18% dell'altezza totale** dell'immagine (~105-125 px su immagine 1200x696) |
| Colore sfondo | `#003366` (blu istituzionale PC Genzano, variabile CSS `--pc-primary`) |
| Opacita sfondo | 85-90% (leggera trasparenza per integrare con la foto) |
| **Testo riga 1** | `PROTEZIONE CIVILE` |
| Font riga 1 | Sans-serif bold (Arial Black, Montserrat ExtraBold, o equivalente) |
| Dimensione riga 1 | ~28-32 px su immagine 1200px di larghezza |
| Colore riga 1 | `#FFFFFF` bianco |
| **Testo riga 2** | `Gruppo Comunale Volontari — Genzano di Roma` |
| Font riga 2 | Sans-serif regular (Arial, Montserrat, o equivalente) |
| Dimensione riga 2 | ~14-16 px su immagine 1200px di larghezza |
| Colore riga 2 | `#FFFFFF` bianco, opacita ~90% |
| **Logo** | Logo circolare PC Genzano (`logo-pc-genzano.png`) posizionato a sinistra nella fascia |
| Dimensione logo | ~70-80 px di altezza, proporzionale |
| Posizione logo | Margine sinistro ~15 px, centrato verticalmente nella fascia |
| Posizione testo | A destra del logo, con margine sinistro ~100 px dal bordo |

#### Esempio visivo (riferimento: immagine Zamberletti)

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

#### Istruzioni per generare la fascia con un'altra AI

Se usi un'AI generativa (DALL-E, Midjourney, Canva AI, ecc.) o un editor grafico:

> **Prompt per generare/aggiungere la fascia:**
> "Aggiungi una fascia orizzontale in basso all'immagine. Sfondo colore esadecimale #003366 con opacita 85-90%, altezza circa 15-18% dell'immagine. A sinistra inserisci il logo circolare della Protezione Civile di Genzano di Roma (file: logo-pc-genzano.png, altezza ~75px). A destra del logo, testo bianco (#FFFFFF) su due righe: riga 1 'PROTEZIONE CIVILE' in grassetto maiuscolo grande (~30px), riga 2 'Gruppo Comunale Volontari — Genzano di Roma' in testo normale piu piccolo (~15px). Font sans-serif (Montserrat, Arial o simile)."

Se usi **Canva** manualmente:
1. Apri l'immagine (1200x696 px o simile)
2. Aggiungi un rettangolo in basso: colore #003366, opacita 85%, altezza ~110 px
3. Inserisci il logo `logo-pc-genzano.png` a sinistra (altezza 75 px)
4. Aggiungi testo "PROTEZIONE CIVILE" — bianco, grassetto, 28-32 pt
5. Sotto: "Gruppo Comunale Volontari — Genzano di Roma" — bianco, regular, 14-16 pt
6. Esporta in WebP, larghezza 1200 px, qualita 80%

### 3.3 — Alt text (testo alternativo)

Ogni immagine nel corpo dell'articolo deve avere un alt text significativo:

| Tipo immagine | Alt text |
|---|---|
| Foto informativa | Descrive il contenuto: "Giuseppe Zamberletti, primo Ministro per la Protezione Civile" |
| Infografica | Descrive il dato chiave: "Diagramma del triangolo del fuoco con i tre elementi" |
| Decorativa | Alt vuoto: `alt=""` |
| Mai | "Immagine di...", "Foto di...", testo generico |

### 3.4 — Immagine nel frontmatter

```yaml
image: "/images/2026-04-18-nome-descrittivo.webp"
```

Nel corpo dell'articolo (Markdown):
```markdown
![Descrizione significativa dell'immagine](/images/2026-04-18-nome-descrittivo.webp)
```

---

## Parte 4 — Struttura tipo di un articolo

### Articolo breve (comunicazione, avviso)

```markdown
---
title: "Chiusura temporanea Via Sicilia per esercitazione"
date: 2026-04-18
description: "Domenica 20 aprile Via Sicilia sara chiusa dalle 9 alle 12 per un'esercitazione di protezione civile."

badge: "Avviso"
priorita: "normale"
autore: "Gruppo Comunale Volontari PC Genzano"
image: "/images/2026-04-18-esercitazione-via-sicilia.webp"
scadenza: "2026-04-20"
area: "Comune di Genzano di Roma"
allegati: []
draft: false
---

**Domenica 20 aprile, dalle 9:00 alle 12:00, Via Sicilia sara temporaneamente
chiusa al traffico** per consentire lo svolgimento di un'esercitazione
del Gruppo Comunale Volontari di Protezione Civile.

## Cosa succede

L'esercitazione simulera uno scenario di evacuazione per rischio
idrogeologico. Saranno coinvolti circa 30 volontari e 5 automezzi.

## Cosa fare

- Evita Via Sicilia dalle 9 alle 12.
- Usa percorsi alternativi: Via Roma o Via Napoli.
- Non allarmarti se vedi mezzi di emergenza in movimento: e un'esercitazione.

## Informazioni

Per chiedere informazioni: 06 9362 600 (segreteria del Gruppo).
```

### Articolo lungo (formazione, approfondimento)

```markdown
---
title: "Come prepararsi a un terremoto: la guida per le famiglie"
date: 2026-04-18
description: "I comportamenti da adottare prima, durante e dopo una scossa
sismica per proteggere la tua famiglia."

badge: "Prevenzione"
priorita: "normale"
autore: "Gruppo Comunale Volontari PC Genzano"
image: "/images/2026-04-18-preparazione-terremoto.webp"
scadenza: ""
area: "Comune di Genzano di Roma"
allegati:
  - titolo: "Checklist preparazione sismica (PDF, 85 KB)"
    url: "/documenti/checklist-sismica.pdf"
draft: false
---

**Il Lazio e una regione a sismicita media.** Sapere come comportarsi
prima, durante e dopo una scossa puo fare la differenza.

---

## Prima della scossa

[Contenuto strutturato con sottotitoli, elenchi e paragrafi brevi]

---

## Durante la scossa

[...]

---

## Dopo la scossa

[...]

---

## Numeri utili

- **112** — Numero unico di emergenza
- **115** — Vigili del Fuoco
- **118** — Emergenza sanitaria

---

*Il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
promuove la cultura della prevenzione sul territorio.*
```

---

## Parte 5 — Checklist pre-pubblicazione

Prima di pubblicare un articolo, verifica:

- [ ] **Frontmatter completo**: tutti i campi obbligatori compilati
- [ ] **Data**: formato `AAAA-MM-GG`, mai con timezone
- [ ] **Description**: max 160 caratteri
- [ ] **Badge**: uno dei valori dalla tabella (o nuovo, che ricevera colore automatico)
- [ ] **Priorita**: solo `"normale"` o `"urgente"`
- [ ] **Titolo**: chiaro, informativo, max ~80 caratteri
- [ ] **Testo**: frasi brevi, voce attiva, no burocratese
- [ ] **Numeri di emergenza**: verificati (112, 115, 118, 1515)
- [ ] **Fonti**: citate per dati meteo, allerte, rischi
- [ ] **Link**: testo descrittivo, no "clicca qui"
- [ ] **Immagine**: formato WebP, 1200px, fascia blu, alt text
- [ ] **Ortografia e grammatica**: verificate
- [ ] **Nome file**: `AAAA-MM-GG-titolo-breve.md`
- [ ] **Draft**: impostato su `false` per pubblicare

---

## Parte 6 — Procedura di aggiornamento

### Fonti da monitorare

| Fonte | URL | Verificare |
|---|---|---|
| Manuale operativo di design PA | docs.italia.it/italia/designers-italia/manuale-operativo-design-docs/ | Versione e data |
| Writing Toolkit | docs.italia.it/italia/designers-italia/writing-toolkit/ | Versione e data |
| Bootstrap Italia | github.com/italia/bootstrap-italia/releases | Numero versione |
| Linee guida design | docs.italia.it/italia/designers-italia/design-linee-guida-docs/ | Versione |
| Linee guida accessibilita | agid.gov.it → sezione accessibilita | Aggiornamenti normativi |

### Quando aggiornare

1. **Ogni 3 mesi**: controllare le date di aggiornamento delle fonti sopra.
2. **Ad ogni nuova versione**: di Bootstrap Italia o del Manuale operativo.
3. **Ad ogni modifica normativa**: nuove norme su accessibilita, privacy, PA digitale.

### Come aggiornare

1. Aprire Claude Code nella cartella del sito.
2. Dire: "Verifica se le linee guida AGID sono aggiornate e aggiorna il manuale di stile se necessario."
3. Claude Code verifichera le fonti online, confrontera con le versioni nel manuale e aggiornera:
   - Questo file (`MANUALE-SITO.md`)
   - Le regole in `.claude/rules/02-content-design-pa.md`
   - Eventuali template o archetype modificati

### Istruzioni per AI esterne (auto-aggiornamento)

> **ISTRUZIONE:** Se questo file ti viene fornito per redigere un articolo, controlla la data "Ultimo check linee guida AGID" in cima. Se e piu vecchia di 3 mesi rispetto alla data odierna, avvisa l'utente con questo messaggio:
>
> "Il manuale di stile potrebbe essere obsoleto (ultimo aggiornamento: [data]). Ti consiglio di aggiornarlo tramite Claude Code prima di procedere. Vuoi che prosegua comunque con le regole attuali?"
>
> Se l'utente conferma, prosegui. Altrimenti, attendi l'aggiornamento.

---

## Appendice A — Colori del sito

| Variabile CSS | Valore | Uso |
|---|---|---|
| `--pc-primary` | `#003366` | Blu istituzionale principale, fascia immagini |
| `--pc-primary-dark` | `#00244d` | Variante scura |
| `--pc-primary-light` | `#004080` | Variante chiara |
| `--pc-secondary` | `#FF6600` | Arancione accento |
| `--pc-accent` | `#009246` | Verde |
| `--pc-danger` | `#d9364f` | Rosso emergenze |

## Appendice B — Struttura delle cartelle

```
content/comunicazioni/          ← Articoli qui
static/images/                  ← Immagini qui
static/documenti/               ← PDF e allegati qui
data/                           ← File dati (allerta, emergenza)
themes/flavour-pcgenzano/       ← Tema (non toccare senza Claude Code)
```

## Appendice C — Comandi rapidi

```bash
# Avviare il sito in locale (vedere bozze)
hugo server -D

# Pubblicare
git add . && git commit -m "descrizione" && git push
```
