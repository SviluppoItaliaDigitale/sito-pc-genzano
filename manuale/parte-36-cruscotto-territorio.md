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

La **Sala situazioni** (`static/monitor/index.html`, pagina HTML statica fuori da Hugo, aperta in nuova scheda dal cruscotto e da `/strumenti/`) mostra le stesse fonti del cruscotto su un'unica schermata scura con mappa a tutta pagina, pensata per lo schermo della sede. È organizzata a **viste** — MIA SALA, ALLERTA, SISMICO, METEO, CARTE, WINDY, TRAFFICO, NAVI, RADIO, SATELLITI, ARIA·MARE, EMERGENZE, REGISTRO — ciascuna con il proprio hash per il deep-link (`/monitor/#radio`) e configurazione della postazione salvata solo in `localStorage`, cioè su quel dispositivo e basta. I **tasti da 1 a 9** aprono, in quest'ordine, **ALLERTA, SISMICO, METEO, CARTE, WINDY, TRAFFICO, ARIA·MARE, EMERGENZE, REGISTRO**: non seguono la posizione nella barra, e MIA SALA, NAVI, RADIO e SATELLITI si aprono col mouse o con l'indirizzo.

Quattro viste sono state aggiunte il 22 settembre 2026 e meritano una riga ciascuna.

- **MIA SALA** — le schede scelte da chi guarda, nell'ordine che vuole, anche prese da viste diverse. La stellina per aggiungere compare sulle schede delle viste che la Mia Sala sa ricostruire — ALLERTA, SISMICO, METEO, ARIA·MARE, EMERGENZE, SATELLITI, REGISTRO — e non su quelle che incorporano una mappa di terzi o una tela (WINDY, TRAFFICO, NAVI, RADIO, CARTE), che non si possono duplicare. Nella Mia Sala la scheda si sposta con le frecce ▲ ▼ e si toglie con ✕: sono pulsanti e non trascinamento, perché il trascinamento da solo esclude chi usa la tastiera o ha poca precisione nel gesto. Se una scheda scelta al momento non ha dati, la Mia Sala lo dice in una riga e la rimette al suo posto appena la fonte torna, senza bisogno di cambiare vista.
- **TRAFFICO** — la mappa di Waze con code e segnalazioni, che si carica solo se la si chiede. 🔴 Le segnalazioni **vengono dagli automobilisti e non sono ufficiali**: le chiusure che fanno fede sono di Polizia Locale, Comune e Anas, e il Gruppo non regola il traffico (Circolare DPC del 6 agosto 2018).
- **NAVI** — la mappa delle navi in tempo reale al largo del Lazio, con quattro livelli di zoom dal litorale al Mediterraneo. 🔴 L'**AIS non è un censimento di ciò che naviga**: lo trasmettono i mercantili sopra una certa stazza, i passeggeri e chi lo monta per scelta, mentre pescherecci piccoli, diporto e molti mezzi di Stato non compaiono. Per le emergenze in mare il numero è **1530**, Guardia Costiera.
- **SATELLITI** — dove sono adesso i satelliti in orbita e quali passano sopra Genzano, con un filtro per quelli che servono alla protezione civile: il ripetitore COSPAS-SARSAT dei radiofari di emergenza, i satelliti meteorologici, quelli di osservazione da cui nascono le mappe Copernicus, le stazioni spaziali, i satelliti radioamatoriali. 🔴 Le posizioni **si calcolano qui**, con il modello orbitale standard, partendo dalle effemeridi pubbliche di CelesTrak: nessun servizio di tracciamento esterno sa che cosa si sta guardando. Si ricalcolano da sole ogni quindici secondi — in orbita bassa un satellite percorre quasi otto chilometri al secondo — e la scheda scrive l'ora dell'ultimo calcolo. Toccando una riga si aprono i prossimi passaggi su Genzano: ora di inizio, altezza massima, direzione in parole, durata. Il catalogo completo (circa sedicimila oggetti, 2,7 MB) si scarica solo se lo si chiede.

**Gli aerei in tempo reale** stanno nella vista EMERGENZE, scheda «Mezzi aerei nell'area»: posizione, quota, velocità e distanza da Genzano, **rinfrescate ogni venti secondi**, entro 463 km, più chiunque stia trasmettendo il codice di emergenza **7700** ovunque si trovi. La scheda dice sempre se sta mostrando la diretta oppure la fotografia di riserva, con l'ora: fra «adesso» e «un quarto d'ora fa», per un velivolo, ci sono decine di chilometri. Il collegamento diretto funziona sul sito pubblicato; sulla copia di prova su GitHub Pages resta la fotografia, e la scheda lo scrive.

🔴 **Che cosa NON dicono quei puntini.** L'ADS-B lo trasmette il velivolo: **molti mezzi di Stato non trasmettono affatto**, e l'assenza dalla mappa non significa assenza dal cielo. Essere in volo non significa essere in intervento. L'etichetta «antincendio» si basa sul tipo di velivolo dichiarato, non sulla missione: dice che è un Canadair, non che stia lanciando acqua. Per gli elicotteri di soccorso sanitario e i mezzi dei Vigili del fuoco fa fede sempre la sala operativa, mai questa pagina.

🔴 **Per le navi**, invece, la mappa resta quella del fornitore così com'è: il flusso di posizioni grezze si paga, quindi sul mare non si può filtrare né incrociare nulla con i nostri dati.

La vista **RADIO** (settembre 2026) permette l'**ascolto** delle bande radioamatoriali con **spettro e waterfall** tramite due ricevitori web **OpenWebRX+** incorporabili, selezionabili dal pannello: **IZ0FKE (Roma)**, `https://sdr.noantri.org/`, predefinito (8 SDR in parallelo al 19 settembre 2026: 80/40/20/10 m, 6 m, 2 m, 70 cm 430–434 MHz, CB, QO-100), e **I6IQX (Bucchianico, CH)**, `https://sdr-plus.i6iqx.it/`, per le gamme che il primo non ha (160, 60, 30, 17, 15, 12 m, PMR446). Il ricevitore è **integrato nella pagina** (nessun iframe): dopo il pulsante «Carica il ricevitore SDR» (click-to-load, come per Windy) la Sala apre un WebSocket verso il server OpenWebRX+ e disegna **spettro e waterfall** su due canvas nell'area principale, con l'**audio** riprodotto dalla pagina stessa; nella barra in alto ci sono VFO, S-meter, volume, audio/muto, squelch, zoom e «Ricollega». Un clic sullo spettro o sul waterfall sintonizza, la rotella cambia lo zoom. I ricevitori della zona raggiungibili solo in http (IU0REG Roma, WebSDR Roma4 di Fara in Sabina) non sono incorporabili in una pagina https e compaiono come link in nuova scheda, già sintonizzati sulla frequenza scelta. Il pannello laterale è il frontalino di sintonia:

- **Bande** raggruppate in HF (160–10 m), VHF (6 m, 2 m), UHF·satellite (70 cm, 23 cm, QO-100) e **uso libero** (CB 27 MHz, LPD 433, PMR446), ciascuna con i limiti «da … a …» in kHz/MHz, il segmento fonia e lo statuto in Italia (PNRF, D.M. 31 agosto 2022); il contrassegno ● indica le bande coperte dai profili SDR del ricevitore in uso (letti live da `status.json` quando il server espone il CORS, altrimenti dalla copia incorporata), e la riga indica quando una banda è coperta solo dall'altro ricevitore; il riquadro sotto la sintonia propone allora il pulsante «Passa a …».
- **Frequenze notevoli** per banda (centri di attività di emergenza IARU Regione 1, frequenze di chiamata, Rete Zamberletti, rete di emergenza metropolitana di Roma, APRS, ISS, QO-100, canali CB/PMR), con categoria colorata: un clic sintonizza.
- **Sintonia manuale**: frequenza in kHz (o MHz con la virgola, se il valore è sotto 1000) e modo LSB/USB/AM/FM/CW.
- **Trasmettere**: riquadro fisso che chiarisce che la pagina riceve soltanto, cosa serve per trasmettere (patente, autorizzazione generale, nominativo), gli strumenti via internet per chi ha il nominativo (EchoLink, Peanut, BrandMeister Hoseline per il solo ascolto DMR) e gli apparati di libero uso.

**Le funzioni del ricevitore, nella pagina (dal 19 settembre 2026).** Su richiesta dell'utente la Sala riproduce tutte le funzioni del ricevitore di IZ0FKE, che nel frattempo ne aveva aggiunte, senza aprire il suo sito:

- **Decoder dei modi digitali**: dal pannello «Decoder dei modi digitali (nel ricevitore)» si accende un decoder fra quelli che il server offre davvero (FT8, FT4, JT65, JT9, WSPR, FST4, Q65, MSK144, JS8Call, BPSK31/63, RTTY, SITOR-B, NAVTEX, DSC, fax meteo, SSTV, CW, APRS/packet, AIS, POCSAG, ISM, HFDL, VDL2, ACARS, LoRa, Meshtastic, sonde…; le voci digitali DMR, D-Star, YSF, NXDN, M17 sono modi di ricezione e mostrano chi parla e verso chi). Sotto il waterfall compare il pannello dei messaggi decodificati con il waterfall del canale audio: un clic sposta il decoder dentro la banda passante (per BPSK, RTTY, CW). I messaggi FT8 riportano UTC, rapporto in dB, DT, frequenza, testo e Paese, con il nominativo cliccabile; le immagini SSTV e fax si formano riga per riga; le posizioni APRS, delle sonde e delle navi finiscono sulla **mappa della Sala** (pallini viola, popup con orario e commento, per due ore).
- **Dal ricevitore, per il profilo attivo**: i **segnalibri** dell'operatore (ripetitori e stazioni note, con distanza e stato) e le **frequenze dei modi digitali** del profilo, come pulsanti che sintonizzano (e accendono il decoder giusto); sullo spettro compaiono come segni gialli e viola, e in fondo il **piano delle bande** del ricevitore (nastro verde radioamatoriale, giallo broadcast).
- **Seconda riga della barra**: orologio **UTC** (i log radio sono in UTC); **passo di sintonia** (quello del profilo, modificabile; pulsanti ◀ ▶ o frecce della tastiera ← → e ↑ ↓ per dieci passi); **NR**, riduzione del rumore nel ricevitore con livello da −20 a +20 dB; **colori** del waterfall (tavolozza del ricevitore, teejeez, ha7ilm, ocean, eclipse, turbo, sala) e **livelli** (automatici, del ricevitore, manuali con MIN/MAX); **● REGISTRA**, che salva l'audio ascoltato in un file WAV sul dispositivo (al massimo dieci minuti, niente passa dal nostro server); **⟳ SCANNER**, che gira sui segnalibri scansionabili e sulle frequenze notevoli del profilo e si ferma dove c'è segnale sopra lo squelch (lo squelch aperto usa una soglia automatica); **🗺 MAPPA**, ricevitore nella metà bassa e mappa sopra, con l'audio che continua; stato del server (CPU, temperatura, ascoltatori sui posti disponibili, versione). Lo **squelch** si riallinea al valore consigliato dal profilo a ogni cambio di profilo (aperto se il profilo non ne indica uno).
- **Servizi dello stesso operatore**, in nuova scheda dal riquadro «Ricevitore»: cruscotto radioamatoriale, WEBCLX (DX cluster), terminale e gateway APRS, reti LoRa e Meshtastic, stazione TinyGS, mappa e file registrati del ricevitore. La **chat** del ricevitore non è integrata: il server la tiene spenta e una chat pubblica non moderata non ha posto su un sito istituzionale.
- **Da cellulare**: tutti i comandi hanno bersagli tattili di almeno 36 px (WCAG 2.5.8), la pagina non scorre in orizzontale, il ricevitore scorre in verticale (barre, spettro di 200 px, pannello decoder) così nulla resta tagliato; un tocco sullo spettro o sul waterfall sintonizza, i pulsanti − e + sostituiscono la rotella per lo zoom, «Pannello» apre il frontalino a tutto schermo. Verificato con Playwright in emulazione touch a 375 px.

**Come avviene la sintonia.** La Sala usa lo stesso protocollo del client web di OpenWebRX+ (implementazione originale, `RE` in `static/monitor/index.html`): handshake testuale, messaggi JSON (`config`, `profiles`, `modes`, `features`, `bands`, `dial_frequencies`, `bookmarks`, `smeter`, `secondary_config`, `secondary_demod`, `metadata`, stato del server…), frame binari col primo byte = tipo (1 spettro FFT, 2 audio, 3 FFT del canale audio per i decoder), spettro e audio compressi IMA ADPCM (l'audio con parole di sincronismo «SYNC»). Quando dal pannello si sceglie una frequenza, il motore verifica se cade nel profilo SDR attivo: se sì manda `dspcontrol` (offset, modo, banda passante, squelch); se no manda `selectprofile` con il profilo che la copre (coperture dai dati di `status.json` e imparate dai `config` ricevuti) e sintonizza appena il nuovo profilo è pronto. Il pannello lo dice con il riquadro «Profilo SDR: …», e i cambi di profilo sono distanziati di almeno 3 secondi perché il server bandisce chi li cambia di continuo. La prima versione (settembre 2026) passava la frequenza nell'hash di un iframe del ricevitore: funzionava solo dentro il profilo attivo, che all'apertura è sempre il 2 m, ed è stata sostituita il giorno stesso.

**Vincoli.** CSP: `connect-src` include `https://` e `wss://` di `sdr.noantri.org` e `sdr-plus.i6iqx.it` (WebSocket del ricevitore e `status.json`), `frame-src` gli stessi host per l'apertura del ricevitore completo (rule 05). L'audio usa un `ScriptProcessorNode` (nessun file esterno, compatibile con la CSP `script-src 'self'`). I ricevitori sono di terzi e condivisi (posti limitati; su I6IQX il profilo attivo è unico per tutti gli ascoltatori): la Sala non li sostituisce e non li controlla. **Solo ascolto**: da questa pagina non si trasmette. Base giuridica verificata su Normattiva: art. 134, comma 4, del Codice delle comunicazioni elettroniche (D.Lgs. 259/2003) — «È libera l'attività di solo ascolto sulla gamma di frequenze attribuita al servizio di radioamatore» — e art. 105, comma 2, lett. b (apparati solo riceventi di libero uso); trasmettere richiede autorizzazione generale, patente e nominativo (art. 134 e Allegato 26); CB in libero uso ex art. 105, comma 1, lett. p; PMR446 in libero uso (PNRF nota 101C, decisione ECC/DEC/(15)05). Le frequenze operative del Gruppo, assegnate al Comune dal Ministero, **non** sono in elenco. Salute delle fonti: `scripts/check-fonti-cruscotto.py` (workflow `controllo-fonti-cruscotto.yml`) verifica `status.json` di entrambi i ricevitori.
