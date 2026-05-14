---
title: "Open data"
description: "Dataset aperti delle attività del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma in formato CSV e JSON, riusabili sotto licenza CC BY 4.0."
layout: "single"
toc: true
tts: true
dataUltimaRevisione: "2026-05-15"
---

Il **Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma** pubblica i dati delle proprie attività in **formato aperto** (CSV + JSON), riusabili da chiunque sotto **licenza Creative Commons BY 4.0** ai sensi del **D.Lgs. 36/2006** ("Codice di riutilizzo dell'informazione del settore pubblico") e della direttiva **(UE) 2019/1024** sui dati aperti.

## Stato attuale

Questa pagina è la **piattaforma di pubblicazione** dei dataset, predisposta secondo lo schema sotto descritto. **I file CSV/JSON saranno pubblicati progressivamente** man mano che il Gruppo completerà la trasformazione del registro interno (cartaceo + foglio elettronico) in formato aperto strutturato.

## Schema dei dataset

### 1. Interventi operativi

**File**: `interventi-AAAA.csv`

| Campo | Tipo | Descrizione |
|---|---|---|
| `data` | data ISO 8601 | giorno dell'intervento (AAAA-MM-GG) |
| `tipo` | enum | `allerta-meteo`, `incendio-boschivo`, `dispersione-persona`, `assistenza-evacuazione`, `supporto-evento`, `formazione-cittadini`, `altro` |
| `descrizione_breve` | testo | sintesi 1-2 frasi (mai dati personali, mai indirizzi specifici) |
| `durata_ore` | numero | durata totale dell'intervento |
| `volontari_impiegati` | numero intero | numero volontari attivati |
| `mezzi_impiegati` | testo | es. "1 fuoristrada, 1 autobotte" |
| `coordinamento` | enum | `gruppo`, `coi`, `regione`, `dpc` |
| `localita` | testo | macro-area (es. "Centro storico", "Zona industriale", "Crateri") — **mai indirizzi precisi che identifichino persone** |

### 2. Ore di volontariato

**File**: `ore-volontariato-AAAA.csv`

| Campo | Tipo | Descrizione |
|---|---|---|
| `mese` | enum | `01`-`12` |
| `anno` | numero intero | AAAA |
| `ore_totali` | numero | somma delle ore dichiarate dai volontari nel mese |
| `attivita_n` | numero intero | numero di attività distinte nel mese |
| `volontari_attivi` | numero intero | volontari con almeno 1 ora nel mese |

### 3. Esercitazioni

**File**: `esercitazioni-AAAA.csv`

| Campo | Tipo | Descrizione |
|---|---|---|
| `data` | data ISO 8601 | |
| `titolo` | testo | nome dell'esercitazione |
| `tipo_rischio_simulato` | enum | `sismico`, `idrogeologico`, `incendio-boschivo`, `comunicazione-emergenza`, `radio`, `multi-rischio` |
| `partecipanti_volontari` | numero intero | |
| `partecipanti_cittadini` | numero intero | |
| `enti_coordinati` | testo | es. "Comune, ASL Roma 6, Croce Rossa, AVIS" |
| `durata_ore` | numero | |

### 4. Formazione

**File**: `formazione-AAAA.csv`

| Campo | Tipo | Descrizione |
|---|---|---|
| `data` | data ISO 8601 | |
| `titolo_corso` | testo | |
| `categoria` | enum | `BLSD`, `radiocomunicazioni`, `AIB`, `cartografia-GIS`, `psicologia-emergenza`, `altro` |
| `ore` | numero | |
| `formatori` | testo | enti/persone formatrici (cognome formatori solo se persone fisiche autorizzate alla pubblicazione) |
| `partecipanti` | numero intero | |

### 5. Risorse e dotazioni

**File**: `dotazioni.csv` (versione corrente, con timestamp)

| Campo | Tipo | Descrizione |
|---|---|---|
| `categoria` | enum | `mezzi`, `radio`, `attrezzature-AIB`, `attrezzature-NBCR`, `kit-medici`, `gruppi-elettrogeni`, `altro` |
| `descrizione` | testo | |
| `quantita` | numero intero | |
| `stato` | enum | `operativo`, `manutenzione`, `da-sostituire` |

## Licenza

Tutti i dataset pubblicati su questa pagina sono rilasciati sotto **licenza Creative Commons Attribuzione 4.0 Internazionale (CC BY 4.0)**.

Sei libero di:

- **Condividere** — copiare e ridistribuire il materiale con qualsiasi mezzo e formato
- **Adattare** — remixare, trasformare e basarti su questi dati per qualsiasi scopo, anche commerciale

A condizione che:

- **Attribuisca** la fonte: *"Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma — www.protezionecivilegenzano.it — CC BY 4.0"*
- **Indichi** se hai modificato il materiale
- **Non insinui** che il Gruppo o il Comune approvino il tuo riutilizzo specifico

Testo completo della licenza: <https://creativecommons.org/licenses/by/4.0/deed.it>

## Privacy e anonimizzazione

I dataset sono **anonimi per costruzione**. Non sono pubblicati:

- Nomi e cognomi di persone fisiche assistite o coinvolte negli interventi.
- Indirizzi precisi che permettano di identificare singole abitazioni.
- Targhe veicoli, codici fiscali, dati sanitari.
- Identità di volontari minorenni o di volontari che non abbiano firmato il consenso al trattamento dati.

Eventuali microdati sensibili sono **aggregati** a livello mensile o di macro-area territoriale.

## Frequenza di aggiornamento

| Dataset | Frequenza | Stato |
|---|---|---|
| `interventi-AAAA.csv` | mensile | in predisposizione |
| `ore-volontariato-AAAA.csv` | mensile | in predisposizione |
| `esercitazioni-AAAA.csv` | trimestrale | in predisposizione |
| `formazione-AAAA.csv` | trimestrale | in predisposizione |
| `dotazioni.csv` | semestrale | in predisposizione |

## Strumenti di consultazione

Per chi vuole consultare i dati senza scaricare i file:

- **CSV**: apribile con qualsiasi foglio elettronico (Excel, LibreOffice Calc, Numbers, Google Sheets) o editor di testo.
- **JSON**: parsabile con qualsiasi linguaggio di programmazione moderno (Python, JavaScript, R, ecc.).
- **Visualizzazioni dashboard**: il sito non offre dashboard interattive (scelta di sobrietà istituzionale). Se vuoi visualizzare i dati graficamente, scaricali e usa strumenti come [Datawrapper](https://www.datawrapper.de/), [Flourish](https://flourish.studio/), [Tableau Public](https://public.tableau.com/) o tool open source.

## Hai bisogno di un dataset specifico?

Se hai un'esigenza particolare (ricerca accademica, articolo giornalistico, comparazione tra Comuni, tesi universitaria), scrivici: <segreteria@protezionecivilegenzano.it>.

## Vedi anche

- [Trasparenza](/trasparenza/) — quadro istituzionale e documenti
- [Comunicazioni](/comunicazioni/) — narrativa delle attività in formato giornalistico
- [Area download](/area-download/) — documenti normativi e manuali
- [Privacy](/privacy/) — politica di protezione dati
- [Accessibilità](/accessibilita/) — dichiarazione AGID
