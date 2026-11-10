# Bollettino «Previsioni meteo per l'Italia»

Il file da aggiornare è `data/previsioni/bollettino.json`.
Questa guida sta in `docs/previsioni/` perché Hugo legge ogni file di `data/`
come dato strutturato e un README in quella cartella farebbe fallire la build.

La pagina [/cartina-meteo-italia/](https://www.protezionecivilegenzano.it/cartina-meteo-italia/)
usa il JSON in fase di pubblicazione (sito statico, senza backend).
Per far comparire un nuovo testo sul sito pubblicato occorre una pull request
che modifica questo file e il successivo deploy su `main`.

## Frequenza

Aggiornare il file ogni giorno, di norma al mattino, dopo aver consultato
almeno i modelli ECMWF IFS, DWD ICON e NCEP GFS tramite Open-Meteo.
Se la situazione cambia in modo netto (temporali, vento forte, nevicata,
svolta rispetto al bollettino precedente) si può emettere un aggiornamento
nello stesso giorno, cambiando `emesso_il`.

## Campi di `bollettino.json`

| Campo | Tipo | Obbligatorio | Significato |
|---|---|---|---|
| `versione` | numero intero | sì | Versione dello schema. Oggi è `1`. Aumentala solo se cambi la struttura. |
| `emesso_il` | stringa ISO 8601 con fuso | sì | Data e ora di emissione in fuso `Europe/Rome`, es. `2026-11-10T12:00:00+01:00`. |
| `validita_da` | data `AAAA-MM-GG` | sì | Primo giorno descritto. |
| `validita_a` | data `AAAA-MM-GG` | sì | Ultimo giorno descritto (di solito 4-5 giorni dopo `validita_da`). |
| `autore` | stringa | sì | Redattore interno del file. Non viene mostrato sulla pagina pubblica. |
| `modelli_consultati` | lista di stringhe | sì | Modelli usati per scrivere il testo, con risoluzione se utile. |
| `fonte_dati` | stringa | sì | Provenienza dei numeri (Open-Meteo e licenza). |
| `situazione_generale` | stringa | sì | Quadro sinottico in italiano chiaro, 4-8 frasi. Solo ciò che i modelli mostrano. |
| `giorni` | lista di oggetti | sì | Un oggetto per ogni giorno, in ordine di data. |
| `avvisi_e_note` | lista di stringhe | sì | Avvertenze, incertezze fra modelli, rinvio alle allerte ufficiali. Può essere vuota solo in casi eccezionali; il rinvio alle allerte ufficiali va tenuto. |

Ogni elemento di `giorni` ha:

| Campo | Tipo | Significato |
|---|---|---|
| `data` | `AAAA-MM-GG` | Giorno descritto. |
| `titolo` | stringa | Etichetta visibile, es. `Martedì 10 novembre`. |
| `aree` | oggetto | Testi per area. Chiavi previste: `nord`, `centro`, `sud`, `isole`, `lazio`. |

Le chiavi di `aree`:

- `nord` — Valle d'Aosta, Piemonte, Liguria, Lombardia, Trentino-Alto Adige, Veneto, Friuli Venezia Giulia, Emilia-Romagna
- `centro` — Toscana, Umbria, Marche, Lazio, Abruzzo (quadro regionale; il dettaglio locale sta in `lazio`)
- `sud` — Molise, Campania, Puglia, Basilicata, Calabria
- `isole` — Sicilia e Sardegna (e, se serve, le isole minori)
- `lazio` — Lazio e Castelli Romani, con un accenno a Genzano di Roma

Se un'area non ha nulla di distinto quel giorno, scrivi comunque una frase breve
(«Nessun fenomeno rilevante previsto.»), non lasciare la chiave vuota o assente.

## Regole di redazione

- Italiano chiaro, frasi brevi, niente tono allarmistico o commerciale.
- Descrivere solo ciò che i modelli mostrano. Se i modelli divergono, dirlo.
- Non assegnare i colori di allerta (verde, giallo, arancione, rosso):
  quelli spettano al Centro Funzionale Regionale e al sistema di allertamento.
  In `avvisi_e_note` rinviare sempre a [/allerte-meteo/](https://www.protezionecivilegenzano.it/allerte-meteo/)
  e, in emergenza, al 112.
- Temperature in °C, precipitazioni in mm, vento in km/h. Arrotondare in modo leggibile
  (interi o un decimale al massimo).
- Non inserire nomi di persone, recapiti privati o dati personali.
- Non citare nel testo pubblico il nome di strumenti di intelligenza artificiale.

## Controlli prima di pubblicare

1. JSON valido (`python3 -m json.tool data/previsioni/bollettino.json`).
2. Date coerenti: `validita_da` e `validita_a` coprono tutte le `giorni[].data`.
3. Tutte le cinque chiavi di `aree` presenti in ogni giorno.
4. Il testo non contraddice i numeri dei modelli consultati quel giorno.

La cartina interattiva e le schede delle città non stanno in questo file:
le aggiorna il browser, in diretta, da Open-Meteo.
