---
title: "Pluviometro a bascula con ESP32"
description: "Un ESP32 conta i ribaltamenti di un pluviometro a bascula e mostra la pioggia dell'ultima ora su una pagina nella rete della sede."
date: 2026-11-24
dataUltimaRevisione: "2026-11-24"
image: ""
tts: true
---

Un pluviometro a bascula raccoglie la pioggia con un imbuto e la fa cadere in una piccola vaschetta a due lati. Quando un lato è pieno, la vaschetta si ribalta e un magnete chiude per un attimo un contatto reed, cioè un interruttore che si chiude vicino a un magnete. L'ESP32 conta questi ribaltamenti. Con la taratura li trasforma in millimetri di pioggia e mostra quanta ne è caduta nell'ultima ora.

## Limiti e avvertenze

- È un dispositivo **non certificato**: le misure servono a osservare la pioggia sul posto. Non sostituiscono le stazioni della rete regionale, i bollettini del Centro Funzionale della Regione Lazio né il **112**.
- La soglia facoltativa accende un LED: è una **pioggia intensa da verificare**, non un'allerta.
- Senza taratura il dispositivo conta solo i ribaltamenti e non calcola i millimetri. I millimetri per ribaltamento non si copiano da un altro pluviometro: si misurano sul tuo.
- La pagina dei dati funziona solo nella rete locale della sede. Non aprirla su internet dal router.
- **Mai collegamenti alla rete a 230 V.** La scheda resta accesa sempre, perché deve contare ogni ribaltamento: alimentala con un alimentatore USB certificato, in un locale o in una scatola al riparo.

## Componenti

| Quantità | Componente | Note |
|---|---|---|
| 1 | Scheda di sviluppo ESP32 con modulo ESP32-WROOM-32 | per esempio ESP32-DevKitC di Espressif o una equivalente |
| 1 | Pluviometro a bascula con contatto reed a due fili | si trova come ricambio per stazioni meteo |
| 1 | Resistenza da 10 kΩ | consigliata con un cavo lungo |
| 1 | Condensatore da 100 nF | facoltativo, riduce i disturbi sul cavo |
| 1 | LED e resistenza da 330 Ω | per la soglia facoltativa |
| 1 | Cavo a due fili | dal pluviometro alla scatola |
| 1 | Alimentatore USB certificato, con cavo | |
| 2 | Pressacavi PG7 | uno per il cavo del contatto, uno per l'alimentazione |
| 4 | Viti M3 in acciaio inox | per il coperchio |
| 1 | Custodia stampata in 3D | file più sotto |

## Collegamenti

| Da | A (ESP32) |
|---|---|
| Contatto reed, primo filo | GPIO 27 |
| Contatto reed, secondo filo | GND |
| Resistenza da 10 kΩ | fra GPIO 27 e 3V3 |
| Condensatore da 100 nF | fra GPIO 27 e GND, vicino alla scheda |
| LED, piedino lungo (anodo), attraverso la resistenza da 330 Ω | GPIO 26 |
| LED, piedino corto (catodo) | GND |

Lo sketch attiva anche la resistenza interna del pin. Quella esterna da 10 kΩ rende il segnale più stabile quando il cavo è lungo. I pin si cambiano in `config.h`.

## Taratura

1. Misura il diametro interno dell'imbuto in millimetri e calcola l'area: area (mm²) = 3,1416 × (diametro ÷ 2) × (diametro ÷ 2).
2. Versa lentamente, goccia a goccia, un volume noto d'acqua, per esempio 100 ml con un cilindro graduato. Conta i ribaltamenti sul monitor seriale.
3. Calcola i millimetri versati: volume in ml × 1000 ÷ area in mm².
4. Dividi i millimetri versati per i ribaltamenti contati e scrivi il risultato in `MM_PER_SCATTO`.

Ripeti la prova tre volte e usa la media. Con un imbuto di 110 mm di diametro, per esempio, 100 ml d'acqua corrispondono a circa 10,5 mm di pioggia.

## Montaggio

1. **Prova al banco.** Collega il contatto, carica lo sketch e apri il monitor seriale a 115200 baud. Fai ribaltare la vaschetta con un dito: ogni ribaltamento deve contare una volta sola. Se ne conta due, aumenta `ANTIRIMBALZO_MS` in `config.h`.
2. **Wi-Fi.** Copia `segreti.h.esempio` con il nome `segreti.h` e scrivi nome e password della rete. Senza Wi-Fi metti `USA_WIFI false` in `config.h`: i dati escono solo sul monitor seriale.
3. **Taratura.** Segui i passi qui sopra e scrivi `MM_PER_SCATTO`.
4. **Installazione.** Metti il pluviometro in piano, lontano da muri, alberi e grondaie, con l'imbuto libero verso il cielo. Porta il cavo fino alla scatola dell'ESP32 e monta la scatola con i pressacavi verso il basso.
5. **Controllo.** Il monitor seriale scrive l'indirizzo della pagina, per esempio `http://192.168.1.50/`. Aprilo da un telefono collegato alla stessa rete. I dati grezzi sono in `/dati.json`.

Ogni minuto lo sketch scrive sulla seriale i ribaltamenti e i millimetri dall'accensione e dell'ultima ora. Spegnendo la scheda i conteggi ripartono da zero.

## File da scaricare

- [pluviometro.ino](/elettronica-emergenza/pluviometro/pluviometro.ino), lo sketch.
- [config.h](/elettronica-emergenza/pluviometro/config.h), le impostazioni: pin, taratura, antirimbalzo, soglia, Wi-Fi.
- [segreti.h.esempio](/elettronica-emergenza/pluviometro/segreti.h.esempio), il modello per i dati del Wi-Fi.
- [README.txt](/elettronica-emergenza/pluviometro/README.txt), le istruzioni brevi.
- [Scatola](/elettronica-emergenza/pluviometro/custodia-pluviometro-scatola.stl), [coperchio](/elettronica-emergenza/pluviometro/custodia-pluviometro-coperchio.stl) e [guarnizione](/elettronica-emergenza/pluviometro/custodia-pluviometro-guarnizione.stl) della custodia (STL).
- [Modello della custodia](/elettronica-emergenza/pluviometro/custodia-pluviometro.scad) per OpenSCAD, da modificare.
- [Testo della licenza EUPL 1.2](/elettronica-emergenza/LICENZA-EUPL-1.2.txt).

Metti i file in una cartella chiamata `pluviometro` e scegli la scheda «ESP32 Dev Module». Non servono librerie esterne: Wi-Fi e pagina web fanno parte del pacchetto esp32 di Espressif. Lo sketch compila con la versione 4.0.0 del pacchetto, con e senza Wi-Fi, prova del 24 novembre 2026.

La custodia esterna misura circa 114 × 56 × 35 mm, alette comprese. Scatola e coperchio vanno in ASA, o in PETG se la scatola sta al riparo; la guarnizione in TPU. Nessuna parte chiede supporti.

## Fonti

Verificate il 24 novembre 2026.

- Espressif, [GPIO dell'ESP32](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/gpio.html).
- Espressif, [installazione del pacchetto Arduino-ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html).
- Arduino, [arduino-cli](https://arduino.github.io/arduino-cli/latest/).

Codice con licenza EUPL 1.2, testi e modello della custodia con licenza CC BY-NC-SA 4.0. Gli altri progetti sono nella pagina [Elettronica per l'emergenza](/elettronica-emergenza/).
