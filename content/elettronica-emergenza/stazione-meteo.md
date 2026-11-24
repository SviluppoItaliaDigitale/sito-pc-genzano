---
title: "Stazione meteo con ESP32: temperatura, umidità, pressione e vento"
description: "Un ESP32 legge un sensore BME280 e un anemometro a coppe e mostra temperatura, umidità, pressione e vento su una pagina nella rete della sede."
date: 2026-11-24
dataUltimaRevisione: "2026-11-24"
image: ""
tts: true
---

Questa stazione misura temperatura, umidità relativa e pressione dell'aria con un sensore BME280 di Bosch, e la velocità del vento con un anemometro a coppe. Il sensore sta dentro uno schermo solare stampato in 3D, fatto di piatti impilati: lascia passare l'aria e ripara dal sole e dalla pioggia. L'anemometro gira con il vento e a ogni giro un magnete chiude per un attimo un contatto reed, cioè un interruttore che si chiude vicino a un magnete. L'ESP32 conta questi impulsi e mostra tutti i dati su una pagina nella rete della sede.

Per la pioggia c'è un progetto a parte: il [pluviometro a bascula](/elettronica-emergenza/pluviometro/). Puoi montarlo sullo stesso palo, con la sua scheda.

## Limiti e avvertenze

- È un dispositivo **non certificato**: le misure servono a osservare il tempo sul posto. Non sostituiscono le stazioni della rete regionale, i bollettini del Centro Funzionale della Regione Lazio né il **112**.
- Lo schermo solare riduce l'effetto del sole sul sensore ma non lo toglie del tutto. Prima di fidarti delle temperature, confrontale per qualche giorno con una stazione ufficiale vicina.
- La pressione è quella misurata alla quota della stazione. Non è riportata al livello del mare, quindi non si confronta direttamente con i valori delle carte e dei bollettini.
- Senza taratura il dispositivo mostra il vento solo come impulsi al secondo. I chilometri all'ora per impulso si prendono dalla scheda tecnica del tuo anemometro o si misurano: non si copiano da un altro modello.
- La pagina dei dati funziona solo nella rete locale della sede. Non aprirla su internet dal router.
- **Mai collegamenti alla rete a 230 V.** La scheda resta accesa sempre, perché deve contare ogni giro dell'anemometro: alimentala con un alimentatore USB certificato.
- Per installarla su un palo o un tetto serve il permesso di chi gestisce il luogo.

## Componenti

| Quantità | Componente | Note |
|---|---|---|
| 1 | Scheda di sviluppo ESP32 con modulo ESP32-WROOM-32 | per esempio ESP32-DevKitC di Espressif o un'altra equivalente |
| 1 | Modulo con sensore Bosch BME280 su I2C, alimentato a 3,3 V | controlla che sia un BME280 e non un BMP280, che non misura l'umidità |
| 1 | Anemometro a coppe con contatto reed a due fili | si trova come ricambio per stazioni meteo, anche in kit |
| 1 | Resistenza da 10 kΩ | per il contatto dell'anemometro, consigliata con un cavo lungo |
| 2 | Resistenze da 4,7 kΩ | solo se il modulo BME280 non ha già le resistenze sul bus I2C |
| 1 | Cavo a quattro fili | dal BME280 alla scatola, il più corto possibile |
| 1 | Cavo a due fili | dall'anemometro alla scatola |
| 1 | Alimentatore USB certificato, con cavo | |
| 3 | Pressacavi PG7 | BME280, anemometro, alimentazione |
| 4 | Viti M3 in acciaio inox | per il coperchio della scatola |
| 3 | Barre filettate M5 in acciaio inox, con 6 dadi | per lo schermo solare, lunghe circa 20 cm |
| 1 | Scatola dell'elettronica e schermo solare stampati in 3D | file più sotto |

Il BME280 funziona da 1,71 a 3,6 V: collegalo al pin 3V3 dell'ESP32, mai al pin 5V, a meno che il modulo non abbia un suo regolatore scritto nella scheda del venditore.

## Collegamenti

| Da | A (ESP32) |
|---|---|
| BME280, pin VCC o VIN | 3V3 |
| BME280, pin GND | GND |
| BME280, pin SDA | GPIO 21 |
| BME280, pin SCL | GPIO 22 |
| BME280, pin SDO (se c'è) | GND per l'indirizzo 0x76, 3V3 per l'indirizzo 0x77 |
| Anemometro, primo filo | GPIO 27 |
| Anemometro, secondo filo | GND |
| Resistenza da 10 kΩ | fra GPIO 27 e 3V3 |
| Resistenze da 4,7 kΩ, se servono | una fra SDA e 3V3, una fra SCL e 3V3 |

Il pin SDO del BME280 non va lasciato scollegato: senza collegamento l'indirizzo non è definito. Molti moduli lo collegano già sulla scheda. Lo sketch prova da solo prima 0x76 e poi 0x77. Se hai l'anemometro del kit SparkFun SEN-15901, il contatto è sui due fili centrali del connettore RJ11 (piedini 2 e 3). I pin si cambiano in `config.h`.

## Come misura

- **Temperatura, umidità e pressione.** Una misura al minuto, con il sensore che dorme fra una misura e l'altra. Sono le impostazioni che Bosch consiglia per il monitoraggio meteo: il sensore si scalda meno e la temperatura resta più vicina a quella dell'aria. I valori grezzi diventano gradi, percentuale e ettopascal con le formule di compensazione della scheda tecnica e i parametri di taratura che Bosch scrive in ogni sensore.
- **Vento.** Lo sketch conta gli impulsi a blocchi di 3 secondi. Mostra la media dell'ultimo minuto e il valore più alto su 3 secondi nell'ultima ora.

Con le prove al banco, le formule dello sketch danno gli stessi valori delle formule in virgola mobile della scheda tecnica: al massimo 0,01 °C, 0,5 Pa e 0,01 punti percentuali di umidità di differenza.

## Taratura del vento

Se la scheda tecnica del tuo anemometro dà il valore, scrivilo in `KMH_PER_HZ` in `config.h`. Per esempio la scheda del kit SparkFun SEN-15901, nella parte in inglese, dice che 2,4 km/h fanno chiudere il contatto una volta al secondo: in quel caso scrivi `2.4f`. La stessa scheda, nella parte in cinese, riporta un altro valore: anche con quel kit conviene fare la prova qui sotto.

Se il valore manca, misuralo così:

1. Monta l'anemometro accanto a un anemometro di riferimento tarato, alla stessa altezza e lontano da ostacoli.
2. In una giornata con vento regolare, annota per 10 minuti la velocità media del riferimento in km/h e gli impulsi al secondo della stazione, dal campo `vento_hz_media_1min` di `/dati.json`.
3. Dividi i km/h del riferimento per gli impulsi al secondo e scrivi il risultato in `KMH_PER_HZ`.

Ripeti la prova in tre giornate diverse e usa la media.

## Montaggio

1. **Prova al banco.** Collega BME280 e anemometro, carica lo sketch e apri il monitor seriale a 115200 baud. Controlla che la temperatura sia plausibile. Fai girare le coppe con un dito: gli impulsi devono crescere.
2. **Wi-Fi.** Copia `segreti.h.esempio` con il nome `segreti.h` e scrivi nome e password della rete. Senza Wi-Fi metti `USA_WIFI false` in `config.h`: i dati escono solo sul monitor seriale.
3. **Schermo solare.** Stampa la base, cinque piatti e il cappello. Infila le tre barre filettate nei fori della base e blocca con un dado sotto. Fai salire il cavo del BME280 dentro il tubo centrale della base e lega il modulo in cima al tubo con una fascetta, con il sensore verso il basso. Poi infila i piatti uno sopra l'altro e chiudi con il cappello e tre dadi.
4. **Scatola.** Stampa scatola, coperchio e guarnizione. Fai passare i tre cavi nei pressacavi e monta la scatola con i pressacavi verso il basso, poco sotto lo schermo, così il cavo del sensore resta corto.
5. **Installazione.** Fissa lo schermo con la staffa della base, lontano da muri, tetti e superfici che si scaldano al sole. Metti l'anemometro più in alto possibile, libero da ostacoli in ogni direzione.
6. **Controllo.** Il monitor seriale scrive l'indirizzo della pagina, per esempio `http://192.168.1.50/`. Aprilo da un telefono collegato alla stessa rete. I dati grezzi sono in `/dati.json`.
7. **Prova di una settimana.** Confronta temperatura, umidità e vento con una stazione ufficiale vicina prima di usare i dati.

Se la misura del BME280 non riesce, la pagina scrive «sensore da controllare» e lo sketch riprova al minuto successivo. Spegnendo la scheda, i valori del vento ripartono da zero.

## File da scaricare

- [stazione-meteo.ino](/elettronica-emergenza/stazione-meteo/stazione-meteo.ino), lo sketch.
- [config.h](/elettronica-emergenza/stazione-meteo/config.h), le impostazioni: pin, indirizzo del sensore, taratura del vento, Wi-Fi.
- [segreti.h.esempio](/elettronica-emergenza/stazione-meteo/segreti.h.esempio), il modello per i dati del Wi-Fi.
- [README.txt](/elettronica-emergenza/stazione-meteo/README.txt), le istruzioni brevi.
- [Base](/elettronica-emergenza/stazione-meteo/schermo-solare-base.stl), [piatto](/elettronica-emergenza/stazione-meteo/schermo-solare-piatto.stl) e [cappello](/elettronica-emergenza/stazione-meteo/schermo-solare-cappello.stl) dello schermo solare (STL).
- [Modello dello schermo solare](/elettronica-emergenza/stazione-meteo/schermo-solare.scad) per OpenSCAD, da modificare.
- [Scatola](/elettronica-emergenza/stazione-meteo/custodia-stazione-meteo-scatola.stl), [coperchio](/elettronica-emergenza/stazione-meteo/custodia-stazione-meteo-coperchio.stl) e [guarnizione](/elettronica-emergenza/stazione-meteo/custodia-stazione-meteo-guarnizione.stl) della scatola dell'elettronica (STL).
- [Modello della scatola](/elettronica-emergenza/stazione-meteo/custodia-stazione-meteo.scad) per OpenSCAD, da modificare.
- [Testo della licenza EUPL 1.2](/elettronica-emergenza/LICENZA-EUPL-1.2.txt).

Metti i file dello sketch in una cartella chiamata `stazione-meteo` e scegli la scheda «ESP32 Dev Module». Non servono librerie esterne: I2C, Wi-Fi e pagina web fanno parte del pacchetto esp32 di Espressif. Lo sketch compila con la versione 4.0.0 del pacchetto, con e senza Wi-Fi, prova del 24 novembre 2026. Non è ancora stato provato su un dispositivo vero.

Lo schermo solare montato con cinque piatti misura circa 17 cm di altezza e 13 cm di larghezza, staffa esclusa. I piatti hanno pareti a 45 gradi e si stampano senza supporti, con il bordo largo sul piatto della stampante; il cappello si stampa allo stesso modo. Stampa lo schermo in ASA bianco, che regge il sole. La scatola dell'elettronica misura circa 119 × 56 × 35 mm, alette comprese: scatola e coperchio in ASA, guarnizione in TPU. Nessuna parte chiede supporti.

## Fonti

Verificate il 24 novembre 2026.

- Bosch Sensortec, [scheda tecnica del BME280](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf), documento BST-BME280-DS001-24, revisione 1.24: alimentazione da 1,71 a 3,6 V (capitolo 1.1), impostazioni per il monitoraggio meteo (capitolo 3.5.1), formule di compensazione (capitolo 4.2.3 e appendice 8.1), registri e identificativo 0x60 (capitolo 5), indirizzi I2C 0x76 e 0x77 (capitolo 6.2), resistenze di pull-up da 4,7 kΩ (capitolo 7.2).
- SparkFun, [scheda del kit Weather Meter SEN-15901](https://cdn.sparkfun.com/assets/d/1/e/0/6/DS-15901-Weather_Meter.pdf): anemometro con contatto reed, 2,4 km/h per una chiusura al secondo nella parte in inglese.
- Espressif, [pin I2C predefiniti del pacchetto Arduino-ESP32 4.0.0](https://github.com/espressif/arduino-esp32/blob/4.0.0/variants/esp32/pins_arduino.h): SDA su GPIO 21, SCL su GPIO 22.
- Espressif, [GPIO dell'ESP32](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/gpio.html).
- Espressif, [installazione del pacchetto Arduino-ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html).
- Arduino, [arduino-cli](https://arduino.github.io/arduino-cli/latest/).

Codice con licenza EUPL 1.2, testi e modelli dello schermo e della scatola con licenza CC BY-NC-SA 4.0. Gli altri progetti sono nella pagina [Elettronica per l'emergenza](/elettronica-emergenza/).
