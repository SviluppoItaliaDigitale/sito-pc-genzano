# Parte 37 — Laboratorio meteo (costruttore di grafici climatici)

Il **Laboratorio meteo** (`/laboratorio-meteo/`, alias `/esplora-meteo/`, `/dati-meteo/`) è uno strumento di **alfabetizzazione ai dati**: il cittadino o lo studente sceglie un luogo dei Castelli Romani, un periodo e una variabile (temperatura, pioggia, vento) e **costruisce il grafico** dei dati meteo veri, con accanto la tabella dei dati e il download CSV. È pensato anche per le scuole (voce di menu sotto "Per le scuole").

I dati storici sono la **rianalisi ERA5** servita da Open-Meteo — la stessa famiglia di dati del Copernicus Climate Data Store (CDS) dell'Unione Europea. Sono dati **indicativi a scopo didattico**: per le previsioni puntuali c'è la scheda Meteo del cruscotto, per le allerte vale il Centro Funzionale Regionale del Lazio.

## 37.1 I due motori (impianto ibrido)

1. **Costruttore live** — il browser interroga Open-Meteo **al clic** dell'utente su "Crea il grafico". Per i periodi recenti (inizio entro ~90 giorni) usa l'endpoint `forecast` (che copre i dati **fino a ieri**); per le serie storiche lunghe usa l'archivio ERA5 (`archive-api.open-meteo.com`, latenza ~5 giorni). Il passaggio fra i due è automatico in base al periodo scelto. Default: ultimi 30 giorni **fino a ieri** (non oggi, che sarebbe una previsione parziale).
2. **Esempi pronti** (la parte "CDS" dell'ibrido) — 4 dataset climatici curati di Genzano, già preparati: temperatura di luglio anno per anno, pioggia annua, giorni con massima ≥35 °C, profilo mensile dell'ultimo anno. Sono file statici in `static/open-data/clima-*.json` con indice `clima-manifest.json`.

## 37.2 File coinvolti

| File | Ruolo |
|---|---|
| `content/laboratorio-meteo/_index.md` | Pagina (`layout: "list"`, `tts: false`, `toc: false`) |
| `themes/flavour-pcgenzano/layouts/laboratorio-meteo/list.html` | Layout: form, esempi, output (grafico + tabella) |
| `static/js/laboratorio-meteo.js` | Motore: fetch Open-Meteo, **renderer SVG vanilla** (niente librerie/CDN), tabella dati, CSV, loader esempi |
| `scripts/genera-clima-castelli.py` | Genera i dataset pre-cotti (stdlib) |
| `.github/workflows/clima-castelli.yml` | Rigenera i dataset ogni mese (vedi 37.4) |
| CSS `custom.css` § **LABORATORIO METEO v1.0** | Stile form, esempi, grafico, tabella |

Il renderer è **SVG fatto in casa** (nessuna libreria grafica, nessun CDN): linee con punti marcati, barre, etichette di valore quando i punti sono pochi, e un **tooltip interattivo** (mouse/tocco/frecce della tastiera) che mostra "giorno: valore" per ogni serie. Le etichette dell'asse X sono allineate ai dati (le barre hanno l'anno sotto ciascuna; prima/ultima etichetta non troncate).

## 37.3 Accessibilità e privacy

- **WCAG 1.1.1 / 1.4.1**: ogni grafico ha **sempre** la tabella dati equivalente (intestazioni `scope="col"`) e le serie si distinguono per **colore *e* tratto** (linea continua/tratteggiata), mai solo colore. Download CSV per chi preferisce i numeri.
- **Tastiera**: il grafico è focalizzabile, le frecce ←→ scorrono i valori uno per uno (annuncio via `aria-live`).
- **Privacy**: la connessione a `open-meteo.com` avviene **solo su richiesta** dell'utente (clic), senza cookie né tracciamento. Gli esempi pronti usano dati già sul nostro sito (zero connessioni esterne). Dichiarato nella pagina `/privacy/` § "Laboratorio meteo". L'host `archive-api.open-meteo.com` è in whitelist `connect-src` del `.htaccess`.

## 37.4 Aggiornamento automatico degli esempi

Lo script `genera-clima-castelli.py` calcola **da solo l'ultimo anno solare completo** (+ 20 anni indietro), quindi gli esempi si estendono con gli anni senza intervento. Il workflow `clima-castelli.yml` (1° del mese) lo rilancia, rigenera `static/open-data/clima-*.json`, committa `[skip-clima]` se cambiano e ri-triggera `deploy.yml`. Il **costruttore live**, invece, è sempre aggiornato per definizione (scarica i dati freschi a ogni richiesta).

## 37.5 Aggiungere un esempio pre-cotto

1. Aggiungi l'aggregazione in `genera-clima-castelli.py` (i dataset escono nella forma attesa dal renderer: `{ titolo, sottotitolo?, tipo: "line"|"bar", unita, x[], serie[] }`).
2. Aggiungi la voce a `clima-manifest.json` (`{ titolo, file, descr }`).
3. Esegui lo script (serve rete verso Open-Meteo) e committa i `clima-*.json`.

## 37.6 Cosa non fare

- Non sostituire il renderer SVG con una libreria via CDN (rompe privacy/self-hosting e sobrietà AGID).
- Non spingere il limite a "oggi": il dato odierno è una previsione parziale che cambia in giornata. Ci si ferma a ieri.
- Non presentare i dati come previsione ufficiale: restano indicativi/didattici.
