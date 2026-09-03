# Parte 36 — Cruscotto del territorio (schede dati in tempo reale)

Il **Cruscotto del territorio** (`/cruscotto/`, alias `/dashboard/`) raccoglie in un'unica pagina i dati di rischio del territorio, presi da **fonti ufficiali e aperte**. È pensato per il cittadino e per gli enti: un colpo d'occhio su terremoti, meteo, radar, satellite, allerta, incendi, aria e mare, senza dover saltare fra dieci siti diversi.

> I dati del cruscotto sono **indicativi**. Per le allerte valgono sempre i bollettini del Centro Funzionale Regionale del Lazio; in emergenza si chiama il **112**. Questo avviso è scritto in cima alla pagina e non va rimosso.

## 36.1 Com'è fatto

La pagina (`content/cruscotto/_index.md`, `layout: "single"`) è un **commutatore a schede** (`role="tablist"`): in alto una fila di pulsanti `.cruscotto-tab`, sotto i pannelli `.cruscotto-panel` (uno visibile per volta, gli altri `hidden`). Ogni scheda è uno **shortcode** dedicato `{{< dashboard-… >}}` nel tema (`themes/flavour-pcgenzano/layouts/shortcodes/`).

Sotto l'introduzione c'è un **richiamo al Laboratorio meteo** (box `.cruscotto-callout`) per chi vuole costruire grafici dei dati nel tempo (vedi Parte 37).

## 36.2 Le schede e le loro fonti

| Scheda | Shortcode | Fonte dati (aperta) |
|---|---|---|
| Terremoti | `dashboard-terremoti` | INGV (FDSN) |
| Vulcani | `dashboard-vulcani` | INGV |
| Radar pioggia | `dashboard-radar` | Radar-DPC (Dipartimento Protezione Civile) |
| Radar ItaliaMeteo | `dashboard-radar-im` | ItaliaMeteo / MeteoHub (Mistral) |
| Satellite (EUMETSAT) | `dashboard-satellite` | EUMETSAT |
| Satellite ItaliaMeteo | `dashboard-satellite-im` | ItaliaMeteo |
| Meteo | `dashboard-meteo` | Open-Meteo (modelli ECMWF) |
| Previsioni ItaliaMeteo | `dashboard-previsioni-im` | ItaliaMeteo (ICON-2I) |
| **Meteo Europa (ECMWF)** | `dashboard-ecmwf` | ECMWF OpenCharts (carte auto-ospitate, vedi 36.3) |
| Osservazioni ItaliaMeteo | `dashboard-italiameteo-osservazioni` | ItaliaMeteo (stazioni) |
| Allerta | `dashboard-allerta` | `data/allerta.json` (Centro Funzionale Lazio) |
| Incendi | `dashboard-incendi` | EFFIS |
| Aria e pollini | `dashboard-aria` | Open-Meteo Air Quality + ARPA Lazio |
| Aria Europa (CAMS) | `dashboard-aria-cams` | Copernicus CAMS (ECMWF) |
| Emergenze EU (EMS) | `dashboard-ems` | Copernicus EMS Rapid Mapping |
| Mare | `dashboard-mare` | Open-Meteo Marine |
| Mare ItaliaMeteo | `dashboard-mare-im` | ItaliaMeteo (onde WW3) |

**Principio privacy-first:** dove possibile niente iframe/embed di terzi nel browser; le carte statiche (ECMWF, cartina Lazio) sono **auto-ospitate** dopo essere state scaricate da workflow. Le chiamate dirette ad API aperte (INGV, Open-Meteo, radar DPC, EUMETSAT, CAMS, EMS, ItaliaMeteo) sono già in whitelist `connect-src` del `.htaccess` — se aggiungi una fonte nuova, aggiungi anche il suo host alla CSP.

## 36.3 Scheda "Meteo Europa (ECMWF)" — carte auto-ospitate

La scheda mostra carte sinottiche europee a medio termine (pressione/vento, temperatura/vento, precipitazioni, CAPE/CIN) prese dall'**OpenCharts API pubblica di ECMWF** (CC BY 4.0, nessuna API key). Non sono embed: il workflow `ecmwf-charts.yml` (4×/giorno) le scarica, le converte in WebP e le salva in `static/images/ecmwf/<slug>.webp`, con i metadati in `data/ecmwf_charts.json`. Lo shortcode `dashboard-ecmwf` legge il JSON e mostra ogni carta con la **data di validità della previsione** e il passo orario (es. +72h) — così si capisce *per quando* vale la carta, non solo quando è stata prelevata.

## 36.4 Monitoraggio automatico delle fonti

Le fonti esterne possono cambiare URL o cadere, lasciando una scheda vuota **senza** errore visibile. Per questo il workflow `controllo-fonti-cruscotto.yml` (lunedì) lancia `scripts/check-fonti-cruscotto.py`: pinga le ~16 fonti e apre un'issue (label `automazione + cruscotto`) se almeno una è giù. Eseguibile in locale: `python3 scripts/check-fonti-cruscotto.py` (exit code = numero fonti in errore).

## 36.5 Aggiungere o modificare una scheda

1. Crea/aggiorna lo shortcode `themes/flavour-pcgenzano/layouts/shortcodes/dashboard-<nome>.html`.
2. Aggiungi il pulsante `.cruscotto-tab` e il pannello `.cruscotto-panel` in `content/cruscotto/_index.md` (rispetta `role="tab"`/`role="tabpanel"`, `aria-controls`, `aria-selected`, `tabindex`).
3. Se la scheda chiama un'API esterna dal browser, aggiungi l'host a `connect-src` nel `.htaccess`.
4. Aggiungi la fonte a `scripts/check-fonti-cruscotto.py` perché venga monitorata.
5. **Verifica visiva** (CLAUDE.md § "Verifica visiva pre-commit su markup HTML"): è markup custom, va guardato con Playwright prima del commit.

## 36.6 Scheda di dettaglio del singolo terremoto (`/cruscotto/terremoto/`)

Dal cruscotto sismico ogni terremoto ha una **scheda di dettaglio** sul modello della pagina evento di `terremoti.ingv.it`. Si raggiunge cliccando la **zona** nella tabella del cruscotto (o "Scheda completa →" nel popup della mappa): l'URL è `/cruscotto/terremoto/#<id-evento-INGV>`.

La scheda (shortcode `scheda-terremoto`, pagina `content/cruscotto/terremoto.md`) prende i dati **live da INGV** (FDSN, dati aperti) e mostra tab accessibili: **Dati evento** (mappa dell'epicentro a piena larghezza + i parametri in griglia sotto), **Localizzazioni e magnitudo** (tutte le stime INGV, es. Mw e ML), **Meccanismo di sorgente**, **Impatto** (ShakeMap), **Sismicità** dell'area negli ultimi 30 giorni, **Cosa fare** (autoprotezione sismica), **Download**.

Principio: i prodotti scientifici dell'INGV (ShakeMap, meccanismo focale) **non vengono ricalcolati**: si mostrano le carte ufficiali con attribuzione quando esistono, altrimenti si rimanda alla scheda INGV. Per i terremoti profondi o lontani dalla costa questi prodotti spesso non sono elaborati, e la scheda lo dichiara. Condivisione, stampa e QR sono quelli standard di ogni pagina del sito.

> Nota tecnica: il cruscotto considera "italiano" un terremoto guardando la provincia tra parentesi nel nome località INGV, accettando sia la sigla `(CS)` sia il nome esteso `(Cosenza)`. Senza il nome esteso, gli eventi al largo (es. un M6.2 "Costa Calabra nord-occidentale (Cosenza)") sparirebbero dal cruscotto.

## 36.7 Cosa non fare

- Non trasformare il cruscotto in un bollettino ufficiale: resta **indicativo**, l'avviso 112/Centro Funzionale non si tocca.
- Non aggiungere embed con cookie di terze parti: rompe la promessa privacy-first e richiederebbe un banner di consenso.
- Non mettere l'indice di pagina/scrollspy qui: il cruscotto è una pagina-strumento, è già escluso dal gate dell'indice (Parte 38).

## 36.8 Sala situazioni (`/monitor/`) e vista RADIO — ascolto SDR delle bande radioamatoriali

La **Sala situazioni** (`static/monitor/index.html`, pagina HTML statica fuori da Hugo, aperta in nuova scheda dal cruscotto e da `/strumenti/`) mostra le stesse fonti del cruscotto su un'unica schermata scura con mappa a tutta pagina, pensata per lo schermo della sede. È organizzata a **viste** (ALLERTA, SISMICO, METEO, CARTE, WINDY, RADIO, ARIA·MARE, EMERGENZE, REGISTRO), ciascuna con il proprio hash per il deep-link (`/monitor/#radio`), scorciatoie da tastiera 1-9 e configurazione della postazione salvata solo in `localStorage`.

La vista **RADIO** (settembre 2026) permette l'**ascolto** delle bande radioamatoriali con **spettro e waterfall** tramite due ricevitori web **OpenWebRX+** incorporabili, selezionabili dal pannello: **IZ0FKE (Roma)**, `https://sdr.noantri.org/`, predefinito (9 SDR in parallelo: 40/30/20/15/10 m, 6 m, 2 m, 70 cm 430–434 MHz, CB, QO-100), e **I6IQX (Bucchianico, CH)**, `https://sdr-plus.i6iqx.it/`, per le gamme che il primo non ha (160, 80, 60, 17, 12 m, PMR446). Il ricevitore è **integrato nella pagina** (nessun iframe): dopo il pulsante «Carica il ricevitore SDR» (click-to-load, come per Windy) la Sala apre un WebSocket verso il server OpenWebRX+ e disegna **spettro e waterfall** su due canvas nell'area principale, con l'**audio** riprodotto dalla pagina stessa; nella barra in alto ci sono VFO, S-meter, volume, audio/muto, squelch, zoom e «Ricollega». Un clic sullo spettro o sul waterfall sintonizza, la rotella cambia lo zoom. I ricevitori della zona raggiungibili solo in http (IU0REG Roma, WebSDR Roma4 di Fara in Sabina) non sono incorporabili in una pagina https e compaiono come link in nuova scheda, già sintonizzati sulla frequenza scelta. Il pannello laterale è il frontalino di sintonia:

- **Bande** raggruppate in HF (160–10 m), VHF (6 m, 2 m), UHF·satellite (70 cm, 23 cm, QO-100) e **uso libero** (CB 27 MHz, LPD 433, PMR446), ciascuna con i limiti «da … a …» in kHz/MHz, il segmento fonia e lo statuto in Italia (PNRF, D.M. 31 agosto 2022); il contrassegno ● indica le bande coperte dai profili SDR del ricevitore in uso (letti live da `status.json` quando il server espone il CORS, altrimenti dalla copia incorporata), e la riga indica quando una banda è coperta solo dall'altro ricevitore; il riquadro sotto la sintonia propone allora il pulsante «Passa a …».
- **Frequenze notevoli** per banda (centri di attività di emergenza IARU Regione 1, frequenze di chiamata, Rete Zamberletti, rete di emergenza metropolitana di Roma, APRS, ISS, QO-100, canali CB/PMR), con categoria colorata: un clic sintonizza.
- **Sintonia manuale**: frequenza in kHz (o MHz con la virgola, se il valore è sotto 1000) e modo LSB/USB/AM/FM/CW.
- **Trasmettere**: riquadro fisso che chiarisce che la pagina riceve soltanto, cosa serve per trasmettere (patente, autorizzazione generale, nominativo), gli strumenti via internet per chi ha il nominativo (EchoLink, Peanut, BrandMeister Hoseline per il solo ascolto DMR) e gli apparati di libero uso.

**Come avviene la sintonia.** La Sala usa lo stesso protocollo del client web di OpenWebRX+ (implementazione originale, `RE` in `static/monitor/index.html`): handshake testuale, messaggi JSON (`config`, `profiles`, `modes`, `smeter`, `bookmarks`…), frame binari col primo byte = tipo (1 spettro FFT, 2 audio), spettro e audio compressi IMA ADPCM (l'audio con parole di sincronismo «SYNC»). Quando dal pannello si sceglie una frequenza, il motore verifica se cade nel profilo SDR attivo: se sì manda `dspcontrol` (offset, modo, banda passante, squelch); se no manda `selectprofile` con il profilo che la copre (coperture dai dati di `status.json` e imparate dai `config` ricevuti) e sintonizza appena il nuovo profilo è pronto. Il pannello lo dice con il riquadro «Profilo SDR: …», e i cambi di profilo sono distanziati di almeno 3 secondi perché il server bandisce chi li cambia di continuo. La prima versione (settembre 2026) passava la frequenza nell'hash di un iframe del ricevitore: funzionava solo dentro il profilo attivo, che all'apertura è sempre il 2 m, ed è stata sostituita il giorno stesso.

**Vincoli.** CSP: `connect-src` include `https://` e `wss://` di `sdr.noantri.org` e `sdr-plus.i6iqx.it` (WebSocket del ricevitore e `status.json`), `frame-src` gli stessi host per l'apertura del ricevitore completo (rule 05). L'audio usa un `ScriptProcessorNode` (nessun file esterno, compatibile con la CSP `script-src 'self'`). I ricevitori sono di terzi e condivisi (posti limitati; su I6IQX il profilo attivo è unico per tutti gli ascoltatori): la Sala non li sostituisce e non li controlla. **Solo ascolto**: da questa pagina non si trasmette. Base giuridica verificata su Normattiva: art. 134, comma 4, del Codice delle comunicazioni elettroniche (D.Lgs. 259/2003) — «È libera l'attività di solo ascolto sulla gamma di frequenze attribuita al servizio di radioamatore» — e art. 105, comma 2, lett. b (apparati solo riceventi di libero uso); trasmettere richiede autorizzazione generale, patente e nominativo (art. 134 e Allegato 26); CB in libero uso ex art. 105, comma 1, lett. p; PMR446 in libero uso (PNRF nota 101C, decisione ECC/DEC/(15)05). Le frequenze operative del Gruppo, assegnate al Comune dal Ministero, **non** sono in elenco. Salute delle fonti: `scripts/check-fonti-cruscotto.py` (workflow `controllo-fonti-cruscotto.yml`) verifica `status.json` di entrambi i ricevitori.
