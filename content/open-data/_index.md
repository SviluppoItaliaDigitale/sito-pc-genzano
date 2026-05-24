---
title: "Open data"
description: "Dataset aperti delle attività del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma in formato CSV e JSON, riusabili sotto licenza CC BY 4.0."
layout: "single"
toc: true
tts: true
dataUltimaRevisione: "2026-05-24"
---

Il **Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma** pubblica i dati delle proprie attività in **formato aperto** (CSV + JSON), riusabili da chiunque sotto **licenza Creative Commons BY 4.0** ai sensi del **D.Lgs. 36/2006** ("Codice di riutilizzo dell'informazione del settore pubblico") e della direttiva **(UE) 2019/1024** sui dati aperti.

## Dataset disponibili

I seguenti dataset sono pubblicati **ora**, con dati reali e verificati, in formato **CSV** e **JSON**. Ogni file è scaricabile e riutilizzabile sotto licenza CC BY 4.0 (vedi sezione *Licenza*).

| Dataset | Contenuto | Record | Scarica |
|---|---|---|---|
| **Aree di emergenza** | Aree di attesa della popolazione e di ammassamento soccorritori del Piano comunale, con coordinate GPS verificate sul campo | 16 | [CSV](/open-data/aree-emergenza.csv) · [JSON](/open-data/aree-emergenza.json) |
| **Numeri utili di emergenza** | Numeri di emergenza validi nel Lazio | 2 | [CSV](/open-data/numeri-utili-emergenza.csv) · [JSON](/open-data/numeri-utili-emergenza.json) |
| **Codici colore allerta** | Significato e comportamenti dei livelli di allerta meteo della Regione Lazio | 4 | [CSV](/open-data/codici-colore-allerta.csv) · [JSON](/open-data/codici-colore-allerta.json) |
| **Timeline storica del rischio** | Eventi geologici, sismici, idrogeologici, normativi dei Castelli Romani, ognuno con fonte istituzionale | 12 | [CSV](/open-data/eventi-storici-castelli-romani.csv) · [JSON](/open-data/eventi-storici-castelli-romani.json) |

> Il dataset **Aree di emergenza** è il riferimento per altri Comuni, enti e applicazioni di terzi: contiene le coordinate GPS, verificate sul campo, dei punti del Piano comunale (aree di attesa della popolazione e aree di ammassamento dei soccorritori).

I file sono rigenerati dallo script `scripts/genera-open-data.py` a partire dai dati strutturati del sito.

### Statistiche operative del Gruppo (dati provvisori)

> ⚠️ **Dati provvisori.** Queste statistiche sono censite **solo a partire dall'adozione del nuovo sistema gestionale (aprile 2026)**: **non coprono l'intero anno** e non includono i mesi precedenti. Sono **aggregate e anonime** — nessun nome, nessun indirizzo, nessun dato personale. Si aggiornano a ogni nuovo export del gestionale.

{{< statistiche-attivita >}}

Periodo coperto: **dal 4 aprile 2026**. I dati sono **generati automaticamente** dall'export del gestionale, che **resta riservato e non viene pubblicato** perché contiene dati personali: il sito ne espone solo i numeri aggregati.

**Scarica i dati grezzi:**

- Statistiche interventi — [CSV](/open-data/statistiche-interventi.csv) · [JSON](/open-data/statistiche-interventi.json)
- Interventi per tipologia — [CSV](/open-data/interventi-per-tipologia.csv) · [JSON](/open-data/interventi-per-tipologia.json)
- Automezzi impiegati (senza targhe) — [CSV](/open-data/automezzi-impiegati.csv) · [JSON](/open-data/automezzi-impiegati.json)
- Statistiche volontari — [CSV](/open-data/statistiche-volontari.csv) · [JSON](/open-data/statistiche-volontari.json)

### In preparazione

Le **statistiche aggregate** di interventi e volontari sono già pubblicate sopra (in forma provvisoria) e si aggiornano a ogni nuovo export del gestionale.

I dataset su **defibrillatori (DAE)** e **idranti antincendio** saranno pubblicati **solo dopo** la ricezione dei dati ufficiali da ASL Roma 6 (Centrale 118) e dal Comando provinciale dei Vigili del Fuoco: il sito non pubblica posizioni non verificate.

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
| `aree-emergenza.{csv,json}` | a ogni variazione del Piano comunale | **pubblicato** |
| `numeri-utili-emergenza.{csv,json}` | a ogni variazione | **pubblicato** |
| `codici-colore-allerta.{csv,json}` | a ogni variazione | **pubblicato** |
| `eventi-storici-castelli-romani.{csv,json}` | a ogni nuovo evento documentato | **pubblicato** |
| `statistiche-interventi.{csv,json}` | a ogni export del gestionale | **pubblicato (provvisorio)** |
| `interventi-per-tipologia.{csv,json}` | a ogni export del gestionale | **pubblicato (provvisorio)** |
| `automezzi-impiegati.{csv,json}` | a ogni export del gestionale | **pubblicato (provvisorio)** |
| `statistiche-volontari.{csv,json}` | a ogni export del gestionale | **pubblicato (provvisorio)** |
| `esercitazioni-AAAA.csv` | trimestrale | in predisposizione |
| `formazione-AAAA.csv` | trimestrale | in predisposizione |
| `dotazioni.csv` | semestrale | in predisposizione |

## Strumenti di consultazione

Per chi vuole consultare i dati senza scaricare i file:

- **CSV**: apribile con qualsiasi foglio elettronico (Excel, LibreOffice Calc, Numbers, Google Sheets) o editor di testo.
- **JSON**: parsabile con qualsiasi linguaggio di programmazione moderno (Python, JavaScript, R, ecc.).
- **Cruscotto del territorio**: per i dati di rischio in tempo reale (terremoti, vulcani, radar pioggia, satellite, meteo, allerta, incendi, aria e mare) il sito offre il [cruscotto del territorio](/cruscotto/), che legge le fonti ufficiali e aperte direttamente nel browser.
- **Visualizzazioni personali**: per elaborazioni grafiche dei file CSV/JSON scaricabili da questa pagina, puoi usare strumenti come [Datawrapper](https://www.datawrapper.de/), [Flourish](https://flourish.studio/), [Tableau Public](https://public.tableau.com/) o tool open source.

## Hai bisogno di un dataset specifico?

Se hai un'esigenza particolare (ricerca accademica, articolo giornalistico, comparazione tra Comuni, tesi universitaria), scrivici: <segreteria@protezionecivilegenzano.it>.

## Dati aperti di altri enti

Oltre ai dataset del Gruppo, queste sono le fonti aperte ufficiali utili per inquadrare i dati locali nel contesto regionale e nazionale.

### Soccorso, rischi ed emergenze

- **[Open Data dei Vigili del Fuoco](https://opendata.vigilfuoco.it/)** — statistiche e dataset del Corpo Nazionale sugli interventi di soccorso.
- **[INGV — terremoti](https://terremoti.ingv.it/)** — eventi sismici in tempo reale (servizio FDSN, open data). Alimentano le schede *Terremoti* e *Vulcani* del nostro [cruscotto del territorio](/cruscotto/).
- **[EFFIS — Copernicus](https://forest-fire.emergency.copernicus.eu/)** — incendi boschivi in Europa (focolai da satellite, aree bruciate). Stessa fonte della scheda *Incendi* del [cruscotto](/cruscotto/).
- **[ARPA Lazio — Qualità dell'aria](https://qa.arpalazio.net/)** — mappe ufficiali di previsione di PM10, NO₂, ozono e polveri sahariane per il Lazio. Stessa fonte della scheda *Aria* del [cruscotto](/cruscotto/).

### Catalogo nazionale

Il portale **[dati.gov.it](https://www.dati.gov.it/)** è il catalogo nazionale dei dati aperti della Pubblica Amministrazione: non è un singolo archivio, ma l'**indice** da cui partire per trovare i dataset di ministeri, regioni e comuni. Per la protezione civile sono utili le ricerche per parole chiave come *"protezione civile"*, *"rischio idrogeologico"*, *"aree di emergenza"*, *"frane"* e *"alluvioni"*.

A livello regionale, il riferimento è **[dati.lazio.it](https://dati.lazio.it/)**, il portale open data della Regione Lazio.

### Statistica ufficiale (ISTAT)

L'**[ISTAT](https://www.istat.it/dati/open-data/)** pubblica le statistiche ufficiali in formato aperto (popolazione, famiglie, edifici, censimenti), consultabili anche dal portale **[esploradati.istat.it](https://esploradati.istat.it/)**. Sono la base per la pianificazione di protezione civile sulle **persone fragili**: la popolazione per fascia d'età aiuta a stimare quante persone potrebbero aver bisogno di assistenza in un'evacuazione, e gli edifici per epoca di costruzione aiutano a valutare la vulnerabilità sismica.

#### Genzano di Roma in cifre (fonte ISTAT)

<div class="table-responsive">
<table>
<caption>Dati statistici di base del Comune di Genzano di Roma, fonte ISTAT</caption>
<thead>
<tr><th scope="col">Indicatore</th><th scope="col">Valore</th><th scope="col">Riferimento</th></tr>
</thead>
<tbody>
<tr><td>Popolazione residente</td><td>22.865 abitanti</td><td>ISTAT, 1° gennaio 2023</td></tr>
<tr><td>Superficie comunale</td><td>17,9 km²</td><td>ISTAT</td></tr>
<tr><td>Altitudine del centro</td><td>435 m s.l.m.</td><td>—</td></tr>
</tbody>
</table>
</div>

> Per i dati aggiornati e di dettaglio (popolazione per fascia d'età, per sezione di censimento, edifici), consulta il portale [ISTAT](https://esploradati.istat.it/). I numeri qui riportati sono l'ultimo dato consolidato disponibile e servono come riferimento di pianificazione, non come anagrafe in tempo reale.

## Vedi anche

- [Trasparenza](/trasparenza/) — quadro istituzionale e documenti
- [Comunicazioni](/comunicazioni/) — narrativa delle attività in formato giornalistico
- [Area download](/area-download/) — documenti normativi e manuali
- [Privacy](/privacy/) — politica di protezione dati
- [Accessibilità](/accessibilita/) — dichiarazione AGID
- [Metodo editoriale](/metodo-editoriale/) — fonti, verifica e aggiornamento dei contenuti
