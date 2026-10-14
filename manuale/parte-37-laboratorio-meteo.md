# Parte 37 — Laboratorio meteo (costruttore di grafici climatici)

Il **Laboratorio meteo** (`/laboratorio-meteo/`, alias `/esplora-meteo/`, `/dati-meteo/`) è uno strumento di **alfabetizzazione ai dati**: il cittadino o lo studente sceglie un luogo dei Castelli Romani, un periodo e una variabile (temperatura, pioggia, vento) e **costruisce il grafico** dei dati meteo veri, con accanto la tabella dei dati e il download CSV. È pensato anche per le scuole (voce di menu sotto "Per le scuole").

I dati storici sono le rianalisi **ERA5-Land** (temperature, cella di circa 11 km) ed **ERA5** (pioggia e vento, circa 25 km) del Copernicus Climate Change Service dell'Unione Europea, servite da Open-Meteo con il modello **`era5_seamless`**: una serie calcolata allo stesso modo per tutti gli anni, quindi confrontabile da un decennio all'altro. Sono dati **indicativi a scopo didattico**: per le previsioni puntuali c'è la scheda Meteo del cruscotto, per le allerte vale il Centro Funzionale Regionale del Lazio.

🔴 **Il modello va sempre scritto nella richiesta (dal 14/10/2026).** Senza il parametro `models`, l'archivio di Open-Meteo usa il «miglior modello disponibile», che dal 2017 è il modello operativo IFS dell'ECMWF (9 km) e prima è la rianalisi: la serie cambia fonte a metà e due decenni non si possono confrontare. Con quella serie mista luglio risultava più caldo di 2,5 °C fra il 2005-2014 e il 2016-2025 invece di 1,6, e i giorni con 35 °C «comparivano» nel 2017. `era5_seamless` restituisce per gli anni prima del 2017 gli stessi valori di prima: la correzione riguarda solo gli anni successivi.

## 37.1 I due motori (impianto ibrido)

1. **Costruttore live** — il browser interroga Open-Meteo **al clic** dell'utente su "Crea il grafico". Per i periodi recenti (inizio entro ~90 giorni) usa l'endpoint `forecast` (che copre i dati **fino a ieri**, e la scheda lo dichiara sotto il grafico: «serie recente, non rianalisi»); per le serie storiche usa l'archivio (`archive-api.open-meteo.com`) con `models=era5_seamless` (costante `MODELLO_STORICO` in `laboratorio-meteo.js`). La rianalisi arriva a circa cinque giorni fa: se gli ultimi giorni del periodo scelto non ci sono ancora, il grafico lo scrive invece di disegnare zeri. Il passaggio fra i due endpoint è automatico in base al periodo scelto. Default: ultimi 30 giorni **fino a ieri** (non oggi, che sarebbe una previsione parziale).
2. **Esempi pronti** — quattro dataset climatici di Genzano, già preparati: temperatura di luglio anno per anno, pioggia annua, **giornate con massima di almeno 30 °C**, profilo mensile dell'ultimo anno. Sono file statici in `static/open-data/clima-*.json` con indice `clima-manifest.json`. Fino al 14/10/2026 il terzo esempio contava i giorni da 35 °C: sui dati omogenei a Genzano sono rarissimi (due in vent'anni, entrambi nel 2017) e il grafico non mostrava nulla. Il file `clima-giorni-molto-caldi-genzano.json` (soglia 35 °C) resta fra i dati aperti, corretto, per chi lo usa al suo indirizzo.

## 37.2 File coinvolti

| File | Ruolo |
|---|---|
| `content/laboratorio-meteo/_index.md` | Pagina (`layout: "list"`, `tts: false`, `toc: false`) |
| `themes/flavour-pcgenzano/layouts/laboratorio-meteo/list.html` | Layout: form, esempi, output (grafico + tabella) |
| `static/js/laboratorio-meteo.js` | Motore: fetch Open-Meteo, **renderer SVG vanilla** (niente librerie/CDN), tabella dati, CSV, loader esempi |
| `scripts/genera-clima-castelli.py` | Genera i dataset pre-cotti (stdlib, `models=era5_seamless`) |
| `data/mappe_raccontate.yaml` (gruppo `laboratorio`) | Spiegazione a parole di ogni esempio e di ogni variabile del costruttore (vedi 37.3-bis) |
| `themes/flavour-pcgenzano/layouts/partials/mappa-raccontata.html` | Markup comune dei riquadri «Spiegazione a parole», condiviso con il cruscotto |
| `scripts/genera-grafici-clima-dossier.py` | Grafici del dossier «Il clima che cambia i rischi», dagli stessi dataset |
| `.github/workflows/clima-castelli.yml` | Rigenera i dataset ogni mese (vedi 37.4) |
| CSS `custom.css` § **LABORATORIO METEO v1.0** | Stile form, esempi, grafico, tabella |

Il renderer è **SVG fatto in casa** (nessuna libreria grafica, nessun CDN): linee con punti marcati, barre, etichette di valore quando i punti sono pochi, e un **tooltip interattivo** (mouse/tocco/frecce della tastiera) che mostra "giorno: valore" per ogni serie. Le etichette dell'asse X sono allineate ai dati (le barre hanno l'anno sotto ciascuna; prima/ultima etichetta non troncate).

## 37.3 Accessibilità e privacy

- **WCAG 1.1.1 / 1.4.1**: ogni grafico ha **sempre** la tabella dati equivalente (intestazioni `scope="col"`) e le serie si distinguono per **colore *e* tratto** (linea continua/tratteggiata), mai solo colore. Download CSV per chi preferisce i numeri.
- **Tastiera**: il grafico è focalizzabile, le frecce ←→ scorrono i valori uno per uno (annuncio via `aria-live`).
- **Privacy**: la connessione a `open-meteo.com` avviene **solo su richiesta** dell'utente (clic), senza cookie né tracciamento. Gli esempi pronti usano dati già sul nostro sito (zero connessioni esterne). Dichiarato nella pagina `/privacy/` § "Laboratorio meteo". L'host `archive-api.open-meteo.com` è in whitelist `connect-src` del `.htaccess`.

## 37.3-bis Spiegazione a parole sotto ogni grafico (dal 14/10/2026)

Sotto ogni grafico c'è un riquadro apribile «Spiegazione a parole» (proposta 1 della roadmap, «Atlante delle mappe spiegate»), come sotto le schede del cruscotto: in breve, che cosa mostra, colori e simboli, ogni quanto si aggiorna, che cosa non dice, fonte.

- I testi stanno in `data/mappe_raccontate.yaml`, gruppo `laboratorio`: una voce per esempio pronto (campo `esempio`, il nome del file del manifest) e una per variabile del costruttore (campo `variabile`: `temperatura`, `pioggia`, `vento`).
- Il layout scrive tutti i riquadri, nascosti, sotto il grafico (`#lab-raccontate`); `mostraSpiegazione(chiave)` in `laboratorio-meteo.js` mostra quello del grafico disegnato (chiave `ex:<file>` per un esempio, `v:<variabile>` per il costruttore) e nasconde il blocco durante il caricamento e in caso di errore.
- La pagina `/cruscotto/mappe-raccontate/` («Le mappe e i grafici spiegati a parole») raccoglie anche questi testi, nella sezione `#laboratorio-meteo`, con lo shortcode `{{< mappa-raccontata gruppo="laboratorio" id="…" pagina="true" >}}` e un collegamento che apre il grafico nel Laboratorio (`?ex=<file>` oppure `?v=<variabile>`).
- `scripts/check-mappe-raccontate.py` (bloccante su PR) controlla che ogni esempio del manifest e ogni opzione del menu delle variabili abbiano la loro voce completa, con lo stesso titolo e nello stesso ordine, e che la pagina abbia una sezione per ciascuna.
- 🔴 **Chi cambia un esempio o una variabile aggiorna la sua voce nella stessa modifica**: soglia, fonte, periodo, colori. Un riquadro che descrive un grafico diverso da quello disegnato è peggio di nessun riquadro.

## 37.4 Aggiornamento automatico degli esempi

Lo script `genera-clima-castelli.py` calcola **da solo l'ultimo anno solare completo** (+ 20 anni indietro), con dieci giorni di margine: il giro del 1° gennaio resta sull'anno prima, perché la rianalisi non ha ancora gli ultimi giorni di dicembre, e l'anno appena finito entra con il giro di febbraio. Gli esempi si estendono con gli anni senza intervento. Il workflow `clima-castelli.yml` (1° del mese) lo rilancia, rigenera `static/open-data/clima-*.json`, committa `[skip-clima]` se cambiano e lascia il deploy a `deploy-coalescer.yml` (dati non urgenti). I grafici del dossier «Il clima che cambia i rischi» non si rigenerano da soli: dopo una rigenerazione che cambia le medie, si rilancia `scripts/genera-grafici-clima-dossier.py` e si riallineano i numeri scritti nel dossier, nella pagina «Clima e protezione civile» e nelle due schede sulla siccità (`check-dati-schede.py` controlla le tabelle delle schede). Il **costruttore live**, invece, è sempre aggiornato per definizione (scarica i dati freschi a ogni richiesta).

## 37.5 Aggiungere un esempio pre-cotto

1. Aggiungi l'aggregazione in `genera-clima-castelli.py` (i dataset escono nella forma attesa dal renderer: `{ titolo, sottotitolo?, tipo: "line"|"bar", unita, x[], serie[] }`).
2. Aggiungi la voce al manifest scritto dallo script (`{ titolo, file, descr }`), non a mano in `clima-manifest.json`: lo script lo riscrive a ogni giro.
3. Aggiungi la spiegazione a parole in `data/mappe_raccontate.yaml` (gruppo `laboratorio`, campo `esempio` uguale al nome del file, titolo uguale a quello del manifest) e la sezione corrispondente in `content/cruscotto/mappe-raccontate.md`, nello stesso ordine del manifest.
4. Aggiungi il file alla lista di verifica di `clima-castelli.yml`.
5. Esegui lo script (serve rete verso Open-Meteo) e `python3 scripts/check-mappe-raccontate.py`, poi committa.

## 37.6 Cosa non fare

- Non sostituire il renderer SVG con una libreria via CDN (rompe privacy/self-hosting e sobrietà AGID).
- Non spingere il limite a "oggi": il dato odierno è una previsione parziale che cambia in giornata. Ci si ferma a ieri.
- Non presentare i dati come previsione ufficiale: restano indicativi/didattici.
- Non togliere `models=era5_seamless` dalle richieste all'archivio (script e JavaScript): la serie tornerebbe a cambiare fonte nel 2017 (vedi in testa al capitolo).
- Non scrivere nei testi che i dati sono «misurati» a Genzano: sono una ricostruzione su una cella di qualche chilometro, non le letture di una stazione.
