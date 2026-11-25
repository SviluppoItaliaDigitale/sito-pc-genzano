---
title: "Sismografo Raspberry Shake in sede o a scuola"
description: "Come installare un Raspberry Shake, il sismografo in kit da montare su un Raspberry Pi, in sede o in una scuola: modello, posizione, rete e dati."
date: 2026-11-24
dataUltimaRevisione: "2026-11-24"
image: ""
tts: true
---

Il Raspberry Shake è un piccolo sismografo: un geofono, cioè un sensore che trasforma il movimento del suolo in un segnale elettrico, collegato a una scheda che si monta su un Raspberry Pi. Registra di continuo le vibrazioni del pavimento e le mostra in una pagina web nella rete della sede. Se vuoi, invia i dati alla rete mondiale dei Raspberry Shake e la tua stazione compare sulla mappa pubblica Station View.

In questa pagina spieghiamo come installare il kit del produttore. Non c'è codice da scrivere: il programma è già nell'immagine ufficiale della scheda microSD.

È uno strumento adatto anche alle scuole. L'Istituto Nazionale di Geofisica e Vulcanologia (INGV), con l'Osservatorio Etneo e l'Università di Catania, ha installato modelli RS3D in cinque scuole superiori della Sicilia sud-orientale, a Catania, Acireale, Adrano, Siracusa e Modica, per un osservatorio sismico scolastico ([poster AS25-1204](https://raspberryshake.org/wp-content/uploads/PosterAS25-1204_compressed.pdf)).

## Limiti e avvertenze

- Il Raspberry Shake **non fa parte della rete sismica ufficiale**. Per sapere se c'è stato un terremoto, dove e di che magnitudo, fanno fede i dati dell'INGV su [terremoti.ingv.it](https://terremoti.ingv.it/).
- **Non dà allarmi** e non avvisa prima di un terremoto. Un segnale forte sul grafico è un'**anomalia da verificare**: può essere un camion, una porta sbattuta o una persona che cammina vicino.
- Il produttore lo descrive come uno strumento per i movimenti deboli: con una scossa forte vicina il segnale può andare fuori scala.
- Non sostituisce il **112** né le indicazioni delle autorità. Durante una scossa non avvicinarti allo strumento: proteggiti.
- **Mai collegamenti alla rete a 230 V** fatti da te: usa l'alimentatore ufficiale del Raspberry Pi.
- Per installarlo in una scuola o in un edificio pubblico serve il permesso di chi lo gestisce, e il tecnico della rete deve aprire le porte elencate più sotto.

## Quale modello scegliere

| Modello | Sensori | Per che cosa |
|---|---|---|
| RS1D | 1 geofono verticale da 4,5 Hz | il più semplice: movimento verticale del suolo |
| RS3D | 3 geofoni da 4,5 Hz | movimento in tre direzioni, il modello usato nelle scuole del progetto INGV |
| RS4D | 1 geofono da 4,5 Hz e 3 accelerometri MEMS | movimento verticale più accelerazione in tre direzioni |
| RS&BOOM | 1 geofono da 4,5 Hz e 1 sensore di infrasuoni | movimento verticale più variazioni di pressione dell'aria |

Ogni modello esiste in versione pronta all'uso e in kit da montare (DIY, «fai da te»). Per una sede o una classe che comincia, l'RS1D basta. L'RS3D permette di vedere da che direzione arrivano le onde.

## Componenti

| Quantità | Componente | Note |
|---|---|---|
| 1 | Kit Raspberry Shake del modello scelto | scheda e geofono del produttore, con la sua custodia |
| 1 | Raspberry Pi 3 Model B, 3 Model B+ oppure 4 Model B | il produttore consiglia il 3 Model B; il Raspberry Pi 5 e i modelli Zero **non** sono supportati |
| 1 | Scheda microSD da almeno 8 GB | di tipo «endurance» o industriale (MLC o SLC), non una scheda comune |
| 1 | Alimentatore ufficiale del Raspberry Pi | almeno 5,1 V e 2,5 A per il Pi 3, 5,1 V e 3,0 A per il Pi 4 |
| 1 | Cavo di rete Ethernet | fino al router o a una presa di rete della sede |
| 1 | Livella a bolla | per mettere lo strumento in piano |
| 1 | Bussola | solo per RS3D e RS4D, per orientarli verso nord |
| 1 | Gruppo di continuità piccolo (UPS) | consigliato dal produttore: protegge la scheda microSD dagli sbalzi e dai blackout brevi |

## Collegamenti

| Da | A |
|---|---|
| Scheda Raspberry Shake | connettore GPIO del Raspberry Pi, ben allineata su tutti i piedini |
| Morsetto «+» del geofono (cavo grigio) | morsetto «+» della scheda Raspberry Shake |
| Geofoni orizzontali dell'RS3D (cavi rosso e verde) | morsetti della scheda, sempre «+» con «+» |
| Porta Ethernet del Raspberry Pi | router o presa di rete, non il computer |
| Alimentatore ufficiale | ingresso di alimentazione del Raspberry Pi, **per ultimo** |

L'ingresso del geofono è sensibile alle scariche elettrostatiche: prima di toccare la scheda, scarica le mani toccando un oggetto metallico collegato a terra. Non schiacciare i cavi del geofono quando chiudi la custodia. Con il Raspberry Pi 3 Model B+ o 4 Model B può servire tagliare i piedini del connettore PoE, che impediscono alla scheda di appoggiarsi bene.

## Montaggio

1. **Scheda microSD.** Scarica l'archivio `raspishake-release` dalla [pagina delle versioni ufficiali](https://gitlab.com/raspberryShake-public/raspshake-sd-img/-/releases). Formatta la scheda in FAT32 (exFAT da 64 GB in su) ed estrai tutto il contenuto dell'archivio direttamente sulla scheda. Ci vuole circa un minuto e mezzo.
2. **Assemblaggio.** Monta la scheda Raspberry Shake sul Raspberry Pi e collega il geofono come nella tabella. Chiudi la custodia: le viti e i piedini vanno stretti solo a mano, perché la plastica si spana.
3. **Posizione.** Scegli il punto più tranquillo dell'edificio: il pavimento nudo del piano più basso, meglio un massetto di cemento vicino a un muro portante. Niente moquette, scrivanie o davanzali. Stai lontano da passaggi di persone e veicoli, lavatrici, condizionatori, caldaie, correnti d'aria e apparecchi Wi-Fi.
4. **Livellamento.** Regola i piedini finché la bolla è al centro del cerchio. Secondo il produttore la bolla al centro corrisponde a circa mezzo grado, e fino a 3° di inclinazione il segnale non cambia in modo apprezzabile.
5. **Orientamento.** Per RS3D e RS4D usa la bussola: la freccia del nord stampata sulla scheda deve guardare verso nord.
6. **Rete e accensione.** Collega prima il cavo di rete, poi l'alimentatore. Usa il cavo: il Wi-Fi peggiora la qualità dei dati. Alla prima accensione lo strumento si aggiorna da solo da internet e resta irraggiungibile per 10-20 minuti.
7. **Configurazione.** Da un computer della stessa rete apri [http://rs.local/](http://rs.local/), meglio con Google Chrome. Se la pagina non si apre, cerca l'indirizzo IP dello strumento nel pannello del router. Il nome utente predefinito è `myshake` e la password `shakeme`: **cambiala subito**.
8. **Posizione e invio dei dati.** In Impostazioni indica dove sta lo strumento, a livello di edificio. Se decidi di condividere i dati, attiva l'invio alla rete del produttore. Sulla mappa pubblica la posizione viene spostata di proposito di qualche centinaio di metri, per riservatezza. Salva e riavvia.
9. **Controllo.** Se hai attivato l'invio dei dati, entro un'ora la stazione compare nell'app ShakeNet e la puoi cercare sulla mappa [Station View](https://stationview.raspberryshake.org/). In sede vedi il grafico delle ultime ore su `http://rs.local/heli`.

Per spegnere lo strumento usa sempre il comando della pagina di configurazione. Staccare la spina può rovinare la scheda microSD.

## Rete in sede o a scuola

Nelle reti con firewall, come quelle delle scuole e degli uffici, il tecnico deve permettere allo strumento queste connessioni in uscita:

| Servizio | Porta |
|---|---|
| Ora esatta (NTP), in entrata e in uscita | 123 UDP |
| Dati continui verso raspberryshakedata.com | 55555 TCP |
| Dati descrittivi all'avvio, verso raspberryshakedata.com | 55556 TCP |
| Aggiornamenti del sistema | 22 e 443 |
| Siti di raspberryshake.org | 443 TCP |
| Station View, grafici ed eventi | 8079 e 18082 TCP |
| Programma Swarm, verso data.raspberryshake.org | 16022 TCP |
| Nomi dei siti (DNS), se la rete non lo offre già | 53 |

Il produttore consiglia di dare al tecnico l'indirizzo MAC o l'indirizzo IP dello strumento, così può autorizzarlo nella rete.

## I dati

- **Grafico in sede.** `http://rs.local/heli` mostra il tracciato delle ultime ore.
- **Scaricare i dati.** Nella pagina di configurazione, menu Azioni, poi Download e Dati. Lo strumento tiene per 7 giorni le registrazioni continue in file giornalieri in formato miniSEED, il formato standard dei dati sismici, di circa 15 MB per canale. Il periodo si cambia nelle impostazioni.
- **Programma Swarm.** Dal menu Azioni scarichi Swarm, un programma per vedere e studiare il segnale in diretta da un computer della rete.
- **Station View e ShakeNet.** Con l'invio dei dati attivo, vedi la tua stazione e quelle degli altri sulla mappa mondiale e nell'app per telefono.

Lo strumento registra solo vibrazioni del suolo. Non raccoglie dati personali: l'unico dato da valutare è la posizione dell'edificio, che sulla mappa pubblica è approssimata.

## In classe

Il poster del progetto INGV descrive le attività con gli studenti: leggere i sismogrammi registrati dalla stazione della scuola, lezioni sulle onde sismiche e sulla pericolosità, gestione dei dati con programmi aperti, piccoli esperimenti sulla propagazione delle onde. Un'attività semplice: fai saltare la classe tutta insieme a qualche metro dallo strumento e guardate il segnale su `rs.local/heli`. Poi confrontate il tracciato di un terremoto lontano con l'elenco dell'INGV.

## File da scaricare

- [README.txt](/elettronica-emergenza/sismografo-raspberry-shake/README.txt), le istruzioni brevi.

Il programma dello strumento non si scarica da qui: si usa solo l'immagine ufficiale del produttore, dalla sua pagina delle versioni.

Le istruzioni vengono dal manuale e dalla guida rapida del produttore, lette il 24 novembre 2026. Non le abbiamo ancora provate su uno strumento vero.

## Fonti

Verificate il 24 novembre 2026.

- Raspberry Shake, [modelli e sensori](https://raspberryshake.org/products/).
- Raspberry Shake, manuale: [guida rapida](https://manual.raspberryshake.org/quickstart.html), [guida rapida in PDF](https://raspberryshake.org/wp-content/uploads/RaspberryShake-QS-latest.pdf), [montaggio del kit](https://manual.raspberryshake.org/assembly.html), [scheda microSD](https://manual.raspberryshake.org/burnSD.html), [caratteristiche tecniche](https://manual.raspberryshake.org/specifications.html), [porte del firewall](https://manual.raspberryshake.org/firewallIssues.html), [scaricare i dati](https://manual.raspberryshake.org/download.html), [Station View e app](https://manual.raspberryshake.org/webServices.html), [domande frequenti](https://manual.raspberryshake.org/FAQ.html).
- Raspberry Shake, [kit da montare](https://raspberryshake.org/learn-support/diy-tutorials/) e [immagine ufficiale della scheda microSD](https://gitlab.com/raspberryShake-public/raspshake-sd-img/-/releases).
- G. Tusa e altri, INGV Osservatorio Etneo e Università di Catania, [Development of a School Seismic Observatory in Southeastern Sicily Using Raspberry Shake Stations](https://raspberryshake.org/wp-content/uploads/PosterAS25-1204_compressed.pdf), poster AS25-1204, dalla pagina dei [poster scientifici](https://raspberryshake.org/news/scientific-posters/).
- INGV, [lista dei terremoti aggiornata in tempo reale](https://terremoti.ingv.it/).

Testi con licenza CC BY-NC-SA 4.0. Il programma e l'immagine della scheda sono del produttore, con le sue licenze. Gli altri progetti sono nella pagina [Elettronica per l'emergenza](/elettronica-emergenza/).
