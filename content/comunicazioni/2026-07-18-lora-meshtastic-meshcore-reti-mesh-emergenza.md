---
title: "LoRa, Meshtastic e le altre reti mesh: comunicare quando Internet e telefoni non funzionano"
date: 2026-07-18T00:02:00+02:00
description: "Cosa sono LoRa, Meshtastic, MeshCore e Reticulum, come si confrontano con APRS, Winlink e il satellite, e cosa significano per la protezione civile."
badge: "Radiocomunicazioni"
priorita: "normale"
autore: "Gruppo Comunale Volontari PC Genzano"
image: "/images/2026-07-18-lora-meshtastic-meshcore-reti-mesh-emergenza.webp"
image_alt: "Cover dell'articolo: LoRa, Meshtastic e le altre reti mesh: comunicare quando Internet e telefoni non funzionano"
scadenza: ""
area: ""
allegati: []
draft: false
social_citazione: "Quando cadono le reti ordinarie serve un canale che funzioni da solo: le reti mesh nascono esattamente per questo"
social_punti:
  - "LoRa: radio a lungo raggio sulla banda libera 868 MHz, senza licenza né abbonamenti"
  - "Meshtastic e MeshCore: reti mesh che si costruiscono da sole, messaggi e posizioni GPS senza Internet"
  - "APRS e Winlink: le alternative storiche dei radioamatori, con licenza"
  - "In emergenza il canale per chiedere soccorso resta sempre il 112"
---

Un blackout esteso, un terremoto, una rete cellulare satura: quando le comunicazioni ordinarie si fermano, chi ha un canale radio indipendente continua a parlare. È il principio su cui lavorano da un secolo i radioamatori. Oggi una nuova generazione di tecnologie a basso costo — **LoRa, Meshtastic, MeshCore, Reticulum** — porta lo stesso principio alla portata di tutti. In questo articolo le presentiamo una per una, insieme alle alternative storiche e satellitari, e spieghiamo cosa significano per la protezione civile.

## LoRa: la tecnologia di base

**LoRa** (da *Long Range*) è una tecnica di trasmissione radio pensata per mandare **piccole quantità di dati molto lontano, consumando pochissimo**. In Europa usa la banda libera dei **868 MHz**: chiunque può trasmettere **senza licenza e senza abbonamenti**, entro i limiti di potenza previsti (25 milliwatt, meno di un centesimo di un telefonino). La portata tipica è di **5-15 chilometri in linea d'aria**, e molto di più tra punti elevati.

Il rovescio della medaglia: la banda è strettissima. Niente voce, niente foto, niente video — solo **brevi messaggi di testo, coordinate GPS e piccoli dati di telemetria**. Per l'emergenza, però, spesso basta esattamente questo.

## Meshtastic: la rete che si costruisce da sola

**Meshtastic** è un progetto **open source** che trasforma un piccolo modulo radio LoRa (costo indicativo: 30-40 euro) in un nodo di una **rete mesh**. Il principio è semplice: ogni nodo ritrasmette i messaggi degli altri. Non servono ripetitori, SIM o Internet: **la rete è fatta solo dai dispositivi dei partecipanti**, e più nodi ci sono, più la copertura si estende.

Dal telefono, collegato al modulo via Bluetooth, si inviano **messaggi di testo e la propria posizione GPS**, protetti da **crittografia AES-256**. Ogni messaggio viene rilanciato di nodo in nodo per un massimo di 3-7 "salti". È la soluzione più semplice e con la community più grande: perfetta per iniziare, per squadre sul territorio e per reti di quartiere di dimensioni contenute.

## MeshCore: l'alternativa per le reti grandi

**MeshCore** è il concorrente più recente, e gira **sugli stessi identici moduli** di Meshtastic (i due sistemi però non comunicano tra loro: bisogna scegliere). La differenza è nel modo di instradare i messaggi. Meshtastic "inonda" la rete: ogni nodo ripete tutto, il che è semplice ma affolla le frequenze quando i nodi diventano tanti. MeshCore invece **impara il percorso** verso il destinatario e poi instrada i messaggi solo lungo quella strada, con catene fino a **64 salti**.

MeshCore distingue anche i ruoli dei nodi: il dispositivo personale, il **ripetitore puro** da collocare in punti alti e il **Room Server**, che ospita chat di gruppo persistenti — chi si collega più tardi ritrova i messaggi. In sintesi: Meshtastic vince per semplicità e diffusione, MeshCore per efficienza sulle **reti permanenti di scala urbana**. Le community italiane (come il progetto MeshItaly) stanno sperimentando entrambe.

## Reticulum: la rete cifrata che viaggia su qualsiasi mezzo

**Reticulum** è un progetto ancora diverso: non un firmware per radio LoRa, ma un **intero stack di rete crittografico** costruito da zero, open source. È pensato per funzionare **in condizioni estreme** — bassissima larghezza di banda, latenze altissime, infrastrutture distrutte. La cifratura end-to-end non è un'aggiunta: è il fondamento del progetto.

La sua forza è l'**indipendenza dal mezzo trasmissivo**: la stessa rete può viaggiare su radio LoRa (tramite i ricetrasmettitori aperti *RNode*), packet radio amatoriale, WiFi o qualunque collegamento disponibile, cucendo insieme pezzi di rete diversi. È lo strumento più potente e più di nicchia dei tre: richiede più competenza, ma è la frontiera della resilienza.

## LoRaWAN: stessa radio, un altro scopo

Attenzione a non confondere le reti mesh con **LoRaWAN**, che usa la stessa modulazione LoRa ma con un'architettura opposta: **a stella**, con **gateway collegati a Internet** che raccolgono i dati di migliaia di sensori. È lo standard dell'**Internet delle cose** — contatori, centraline meteo, sensori di livello dei fiumi — ed è preziosissimo per il monitoraggio del territorio. Ma se cade Internet, cadono anche i gateway: **non è pensato per la messaggistica d'emergenza tra persone**.

## Le alternative storiche: APRS e Winlink

Il mondo radioamatoriale offre da decenni servizi analoghi, più maturi e con portate superiori. Il prezzo è una **licenza**: in Italia serve superare l'esame per la patente di radioamatore e ottenere il nominativo dal Ministero.

- **APRS** (*Automatic Packet Reporting System*), ideato dal radioamatore Bob Bruninga nei primi anni Novanta, trasmette **posizioni, dati meteo e brevi messaggi** sulla frequenza convenzionale europea di **144,800 MHz**. I dati si visualizzano in tempo reale su mappe. È nato proprio come ausilio alla protezione civile nelle catastrofi, e una rete di ripetitori digitali (*digipeater*) lo copre da anni su gran parte del territorio.
- **Winlink** permette di inviare e ricevere **email via radio**, anche a grandissima distanza sulle onde corte, senza alcuna infrastruttura Internet locale: è lo standard delle reti di emergenza radioamatoriali di mezzo mondo.

Rispetto alle reti mesh LoRa: più potenza, più portata, più storia operativa — ma serve formazione, esame e disciplina radio. I due mondi oggi si stanno persino incontrando (esistono ponti LoRa-APRS gestiti da radioamatori).

## La messaggistica satellitare

Ultima famiglia: i canali che scavalcano completamente le reti terrestri. I **comunicatori satellitari** portatili (come i Garmin inReach, sulla rete Iridium) permettono messaggi e SOS da qualunque punto del pianeta, con abbonamento. E dagli **iPhone 14** in poi la funzione **"SOS emergenze via satellite"** è disponibile anche in Italia (da marzo 2023). Senza copertura cellulare, il telefono guida l'utente a puntare il satellite e inoltra la richiesta di soccorso. Servono cielo aperto e, a regime, servizi commerciali — ma per l'escursionista isolato è già oggi un'ancora di salvezza concreta.

## Cosa serve per provare, in pratica

Per sperimentare una rete mesh LoRa bastano pochi elementi e una spesa contenuta:

- **Un modulo LoRa in versione europea (868 MHz)** per ciascun partecipante. Le opzioni più diffuse:
  - **Heltec V3**: il punto d'ingresso più economico, circa 25-35 euro, con piccolo schermo OLED.
  - **LILYGO T-Beam o T-Echo**: con GPS integrato, per chi vuole condividere la posizione.
  - **RAK WisBlock**: bassissimi consumi, ideale per nodi fissi alimentati a pannello solare.
  - **SenseCAP di Seeed**: già assemblati con custodia, per chi non vuole saldare o stampare scatole.
- **Un'antenna per gli 868 MHz** (quasi sempre inclusa) e una batteria o powerbank.
- **Uno smartphone** con l'app gratuita **Meshtastic** (Android e iOS), che si collega al modulo via Bluetooth.

**Dove si compra:** dai negozi online ufficiali dei produttori (Heltec, LILYGO, Seeed Studio, RAK Wireless) o dai grandi marketplace. L'unica avvertenza importante: verificare che il venditore dichiari la **versione 868 MHz (EU868)**. I moduli a 915 MHz sono per il mercato americano e in Italia non si possono usare.

**La configurazione** richiede una mezz'ora la prima volta. Si carica il firmware dal browser con lo strumento ufficiale del progetto e si imposta la **regione EU_868** (obbligatoria: applica automaticamente i limiti di trasmissione europei). Poi si dà un nome al nodo e si crea un canale cifrato da condividere con il proprio gruppo.

Due accorgimenti da chi lo fa da tempo. Mai accendere il modulo senza antenna collegata: si danneggia lo stadio radio. Meglio collocare i nodi più in alto possibile — la portata si gioca tutta sulla visibilità.

**I tutorial non mancano**, anche in italiano. La documentazione ufficiale del progetto è in inglese, ma le community italiane pubblicano guide passo-passo in italiano: il primo nodo, la scelta dell'hardware e la mappa dei nodi già attivi (i link sono in fondo all'articolo).

## Cosa significa per la protezione civile

Per un Gruppo come il nostro queste tecnologie **non sostituiscono** le radiocomunicazioni istituzionali — le reti regionali, i collegamenti con la [catena di comando](/comunicazioni/2026-04-16-catena-comunicazioni-protezione-civile-dpc-cor-com-coc/), gli apparati in dotazione. Aprono però possibilità nuove: telemetria a basso costo, tracciamento delle squadre, canali di riserva quando tutto il resto tace. Per i cittadini rappresentano invece una forma moderna di **autoprotezione organizzata**, nello spirito dei "gruppi di quartiere" che si preparano prima dell'emergenza.

Un paletto però resta fisso: **per chiedere soccorso si chiama il 112**, finché un qualsiasi canale ordinario funziona. Le reti mesh sono un complemento per quando i canali ordinari non ci sono più — non una scorciatoia per saltare il sistema di soccorso.

## Per approfondire

**Sul nostro sito:**

- [Le radiocomunicazioni di base per i volontari di protezione civile](/comunicazioni/2026-06-27-radiocomunicazioni-base-volontari-pc/)
- [Radiocomunicazioni in emergenza: il ruolo dei volontari](/comunicazioni/2026-05-03-radiocomunicazioni-emergenza-volontari/)
- [Rischio blackout: cosa fare quando manca tutto](/rischi-prevenzione/blackout/)

**Fonti e progetti (in inglese, salvo dove indicato):**

- [Meshtastic — sito ufficiale del progetto](https://meshtastic.org/)
- [Reticulum Network — documentazione ufficiale](https://reticulum.network/)
- [LoRa Alliance — lo standard LoRaWAN](https://lora-alliance.org/)
- [Winlink — email via radio](https://www.winlink.org/)
- [MeshItaly — la community italiana delle reti mesh LoRa (in italiano)](https://meshitaly.it/learn)
- [Meshtastic Italia — guide, mappa dei nodi e community (in italiano)](https://www.meshtasticitalia.it/)
- [Meshtastic — documentazione ufficiale e primi passi](https://meshtastic.org/docs/)
- [Apple — SOS emergenze via satellite](https://support.apple.com/it-it/101573)
