---
title: "Elettronica per l'emergenza"
description: "Progetti con Arduino, ESP32 e Raspberry Pi per i volontari di protezione civile: sensori, radio e schermi da costruire con pochi componenti, con codice, istruzioni e custodia da stampare."
layout: "single"
date: 2026-11-24
dataUltimaRevisione: "2026-11-24"
image: ""
tts: true
---

Progetti con Arduino, ESP32 e Raspberry Pi per i volontari del Gruppo e di altre associazioni. Sono piccoli dispositivi che si costruiscono con componenti comuni: un sensore per tenere d'occhio un fosso, una stazione meteo, una radio per i messaggi della squadra, uno schermo con l'allerta in sede, un sismografo per la scuola. Per ognuno trovi a che cosa serve, i limiti, i componenti, i collegamenti, i passi di montaggio e i file da scaricare.

<div class="alert alert-warning" role="note">
<p class="mb-2"><strong>Prima di cominciare, leggi qui.</strong></p>
<ul class="mb-0">
<li>Sono dispositivi <strong>non certificati</strong>. Segnalano un'anomalia da verificare: non danno allarmi e non dicono a nessuno che cosa fare.</li>
<li>Non sostituiscono le allerte ufficiali del Centro Funzionale della Regione Lazio, IT-alert, le reti di misura degli enti né il <strong>112</strong>. Se c'è pericolo per le persone, chiama il 112.</li>
<li><strong>Mai collegamenti alla rete elettrica a 230 V</strong> fatti da te: usa batterie, power bank o alimentatori USB certificati.</li>
<li>Per installare un dispositivo su un argine, un palo o un edificio serve il permesso di chi gestisce quel luogo.</li>
</ul>
</div>

## I progetti

| Progetto | A che cosa serve | Scheda | File |
|---|---|---|---|
| [Sensore del livello dell'acqua](/elettronica-emergenza/livello-acqua/) | Misura l'acqua in un fosso o in un sottopasso e accende un LED con un cicalino quando supera una soglia | ESP32 | sketch, custodia |
| [Pluviometro a bascula](/elettronica-emergenza/pluviometro/) | Conta la pioggia caduta e mostra i millimetri dell'ultima ora su una pagina nella rete della sede | ESP32 | sketch, custodia |
| [Nodo Meshtastic per la squadra](/elettronica-emergenza/nodo-meshtastic/) | Messaggi brevi fra volontari anche dove il telefono non prende, con un canale privato | scheda LoRa | script, custodia |
| [Schermo dell'allerta in sede](/elettronica-emergenza/schermo-allerta/) | Mostra a tutto schermo il livello di allerta pubblicato dal sito, con l'ora del controllo | Raspberry Pi | programma Python |
| [Stazione meteo](/elettronica-emergenza/stazione-meteo/) | Temperatura, umidità, pressione e vento su una pagina nella rete della sede, con lo schermo solare da stampare | ESP32 | sketch, custodia |
| [Monitor del caldo](/elettronica-emergenza/monitor-caldo/) | Calcola l'indice di calore in una tenda o in una sala d'attesa e lo mostra con tre LED | ESP32 | sketch, custodia |
| [Controllo della batteria a 12 V](/elettronica-emergenza/batteria-12v/) | Misura la batteria di un mezzo o di un gruppo elettrogeno e segnala una tensione bassa da verificare | ESP32 | sketch, custodia |
| [Posizione dei mezzi con Meshtastic](/elettronica-emergenza/posizione-mezzi-meshtastic/) | Il nodo sul mezzo invia la posizione sul canale privato della squadra, solo durante il servizio | scheda LoRa con GPS | script |
| [Sismografo Raspberry Shake](/elettronica-emergenza/sismografo-raspberry-shake/) | Come installare il sismografo in kit in sede o in una scuola e leggerne i dati | Raspberry Pi | istruzioni |
| [Ricevitore di aerei ed elicotteri](/elettronica-emergenza/ricevitore-adsb/) | Riceve i segnali ADS-B a 1090 MHz e mostra il traffico aereo vicino, in sola ricezione | Raspberry Pi | script |

## Che cosa ti serve

- Un computer con Windows, macOS o Linux e un cavo USB adatto alla scheda.
- Per le schede ESP32, il programma gratuito [Arduino IDE](https://www.arduino.cc/en/software/) oppure arduino-cli, con il pacchetto delle schede di Espressif: le istruzioni sono nella [guida ufficiale di installazione](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html).
- Per le custodie, una stampante 3D oppure un servizio di stampa online. Come ordinare un oggetto senza avere una stampante lo spieghiamo nella pagina [Stampa 3D](/stampa-3d/).
- Un saldatore e un multimetro aiutano, ma per i primi prototipi bastano cavetti con i connettori a innesto.

## Come sono fatti i file

Ogni progetto ha una cartella con un file `README.txt` di istruzioni brevi. I file si aprono con un editor di testo.

- **Sketch per ESP32** (`.ino` e `config.h`): le impostazioni stanno tutte in `config.h`. Gli sketch compilano con il pacchetto esp32 di Espressif versione 4.0.0 e non usano librerie esterne.
- **Password e chiavi**: non sono mai nei file che scarichi. Dove servono c'è un file di esempio, da copiare e completare sul tuo computer. Non condividere mai la copia con i tuoi dati.
- **Custodie**: per ogni custodia ci sono tre file STL (scatola, coperchio, guarnizione) e il modello OpenSCAD, da modificare con il programma gratuito [OpenSCAD](https://openscad.org/). Stampa scatola e coperchio in ASA, o in PETG se il dispositivo sta al riparo; la guarnizione in TPU. Non usare il PLA all'aperto: con il sole si deforma.

## Licenze

- Il **codice** (sketch, script e programmi) ha la licenza [EUPL 1.2](https://eur-lex.europa.eu/legal-content/IT/TXT/?uri=CELEX:32017D0863), la licenza open source dell'Unione europea, come i componenti dell'[Open Kit](/open-kit/). Il testo è nel file [LICENZA-EUPL-1.2.txt](/elettronica-emergenza/LICENZA-EUPL-1.2.txt).
- I **testi** e i **modelli delle custodie** hanno la licenza del sito, [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.it): puoi usarli e modificarli citando il Gruppo, senza scopo commerciale.
- Programmi e pacchetti di altri (pacchetto esp32 di Espressif, firmware e programma Meshtastic, Raspberry Pi OS) si usano così come sono, con le loro licenze, e si scaricano dalle loro fonti.

I dettagli sono nelle [note legali](/note-legali/#licenza-dei-contenuti). Se costruisci uno di questi dispositivi o lo migliori, [scrivici](/contatti/).
