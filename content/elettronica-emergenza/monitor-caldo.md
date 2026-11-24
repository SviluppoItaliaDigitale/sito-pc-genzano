---
title: "Monitor del caldo per tende e sale d'attesa"
description: "Un ESP32 misura temperatura e umidità in una tenda o in una sala d'attesa, calcola l'indice di calore e accende uno, due o tre LED."
date: 2026-11-24
dataUltimaRevisione: "2026-11-24"
image: ""
tts: true
---

In una tenda al sole o in una sala d'attesa affollata l'aria si scalda in fretta, e chi gestisce la struttura non sempre se ne accorge. Questo dispositivo misura temperatura e umidità con un sensore Sensirion SHT4x e calcola l'indice di calore, cioè la temperatura percepita quando all'aria calda si aggiunge l'umidità. Usa il metodo del National Weather Service, il servizio meteorologico nazionale degli Stati Uniti, e ne riprende le quattro fasce. Dalla prima fascia in su accende i LED e mostra un'**anomalia da verificare** su una pagina nella rete locale: chi la vede controlla la situazione e avvisa il responsabile della struttura.

## Limiti e avvertenze

- È un dispositivo **non certificato**: segnala un'anomalia da verificare, non un allarme, e non dice che un ambiente è sicuro.
- Non dà consigli sanitari. Per sapere come proteggersi dal caldo segui le indicazioni del Ministero della Salute: i [dieci consigli utili](https://www.salute.gov.it/new/it/tema/ondate-di-calore/dieci-consigli-utili/) e i [bollettini sulle ondate di calore](https://www.salute.gov.it/new/it/tema/ondate-di-calore/bollettini-sulle-ondate-di-calore-0/). Il bollettino più vicino a Genzano è quello di Roma.
- Non sostituisce i bollettini del Ministero, il parere di un medico né il **112**. Se una persona sta male, chiama il 112.
- Le fasce sono quelle del National Weather Service e non coincidono con i livelli dei bollettini italiani. Valgono all'ombra e con poco vento: al sole diretto l'indice reale può essere più alto, fino a circa 8 °C secondo il NWS.
- La formula usata dal NWS non vale per combinazioni estreme di temperatura e umidità, fuori dai dati su cui è stata costruita.
- La pagina dei dati funziona solo nella rete locale. Non aprirla su internet dal router.
- **Mai collegamenti alla rete a 230 V.** Alimentalo con un alimentatore USB certificato o con un power bank.
- Il dispositivo non raccoglie dati sulle persone: misura solo l'aria.

## Le fasce e i LED

| LED accesi | Indice di calore | Fascia del NWS |
|---|---|---|
| Nessuno | sotto 26,7 °C | sotto la prima fascia |
| 1 LED, giallo | da 26,7 °C | Caution (attenzione) |
| 2 LED, giallo e arancione | da 32,2 °C | Extreme Caution (estrema attenzione) |
| 3 LED fissi | da 39,4 °C | Danger (pericolo) |
| 3 LED che lampeggiano una volta al secondo | da 51,7 °C | Extreme Danger (pericolo estremo) |
| Solo il LED centrale, un lampo ogni 2 secondi | | sensore da controllare: nessuna misura valida |

I limiti in gradi Celsius sono la conversione di quelli del NWS in gradi Fahrenheit: 80, 90, 103 e 125 °F. Conta il numero dei LED accesi, non solo il colore: la fascia si legge anche da chi non distingue i colori. Per tornare alla fascia più bassa l'indice deve scendere di almeno 0,5 °C sotto il limite, così i LED non si accendono e spengono di continuo. All'accensione i tre LED si accendono uno per volta: è la prova.

## Componenti

| Quantità | Componente | Note |
|---|---|---|
| 1 | Scheda di sviluppo ESP32 con modulo ESP32-WROOM-32 | per esempio ESP32-DevKitC di Espressif o un'altra equivalente |
| 1 | Modulo con sensore Sensirion SHT40, SHT41 o SHT45 su I2C, alimentato a 3,3 V | versione «AD1B», indirizzo 0x44 |
| 3 | LED da 5 mm: giallo, arancione, rosso | |
| 3 | Resistenze da 330 Ω | una per LED |
| 2 | Resistenze da 4,7 kΩ | solo se il modulo del sensore non ha già le resistenze sul bus I2C |
| 1 | Cavo a quattro fili, lungo circa 30 cm | porta il sensore fuori dalla scatola |
| 1 | Alimentatore USB certificato o power bank, con cavo | alcuni power bank si spengono da soli quando il consumo è basso: scegline uno che resta acceso o usa l'alimentatore |
| 2 | Pressacavi PG7 | cavo del sensore e alimentazione |
| 4 | Viti M3 in acciaio inox | per il coperchio |
| 1 | Custodia stampata in 3D | file più sotto |

Abbiamo scelto la famiglia SHT4x perché misura l'umidità con meno errore del BME280 usato nella [stazione meteo](/elettronica-emergenza/stazione-meteo/): circa 1,8 punti percentuali contro 3, secondo le schede tecniche. Nell'indice di calore l'umidità pesa molto. Il sensore funziona da 1,08 a 3,6 V: collegalo al pin 3V3, mai al pin 5V, a meno che il modulo non abbia un suo regolatore scritto nella scheda del venditore.

## Collegamenti

| Da | A (ESP32) |
|---|---|
| Sensore, pin VCC o VIN | 3V3 |
| Sensore, pin GND | GND |
| Sensore, pin SDA | GPIO 21 |
| Sensore, pin SCL | GPIO 22 |
| LED giallo, piedino lungo (anodo), attraverso una resistenza da 330 Ω | GPIO 25 |
| LED arancione, piedino lungo, attraverso una resistenza da 330 Ω | GPIO 26 |
| LED rosso, piedino lungo, attraverso una resistenza da 330 Ω | GPIO 27 |
| Piedini corti (catodi) dei tre LED | GND |
| Resistenze da 4,7 kΩ, se servono | una fra SDA e 3V3, una fra SCL e 3V3 |

Il sensore sta fuori dalla scatola, all'estremità del cavo: dentro, il calore della scheda falserebbe la misura. I pin e l'indirizzo si cambiano in `config.h`.

## Come misura

Ogni 10 secondi lo sketch chiede una misura al sensore e ne controlla la somma di verifica: una lettura rovinata viene scartata. Calcola l'indice sulla mediana delle ultime cinque misure, così un valore storto non cambia lo stato dei LED. Dopo tre letture fallite di fila segnala «sensore da controllare».

Il calcolo segue la pagina del NWS. Prima c'è una formula semplice. Il suo risultato si fa in media con la temperatura: se la media resta sotto 80 °F, cioè 26,7 °C, l'indice è quella media; altrimenti si passa alla regressione di Rothfusz, con due correzioni: una per l'umidità sotto il 13 % e una per l'umidità sopra l'85 %. Lo sketch è stato provato al banco su oltre 28 000 combinazioni di temperatura e umidità: dà gli stessi valori di un calcolo di controllo separato. Riproduce anche i due esempi della pagina del NWS di Amarillo: con 100 °F e 55 % di umidità l'indice è 124 °F, con 100 °F e 15 % è 96 °F.

## Montaggio

1. **Prova al banco.** Collega sensore e LED, carica lo sketch e apri il monitor seriale a 115200 baud. All'accensione i tre LED si accendono uno per volta. Poi compaiono temperatura, umidità e indice. Scalda il sensore con le dita: i valori devono salire.
2. **Wi-Fi.** Copia `segreti.h.esempio` con il nome `segreti.h` e scrivi nome e password della rete. Senza Wi-Fi metti `USA_WIFI false` in `config.h`: restano i LED e il monitor seriale.
3. **Custodia.** Stampa scatola, coperchio e guarnizione. Infila i LED nei tre fori del coperchio, nell'ordine giallo, arancione, rosso, e fissali con una goccia di colla a caldo. Fai uscire il cavo del sensore e quello dell'alimentazione dai pressacavi.
4. **Posizione del sensore.** Mettilo all'altezza dove stanno le persone, all'ombra, lontano da stufe, lampade, finestre al sole, condizionatori e dal contatto diretto con le persone.
5. **Posizione dei LED.** Metti la scatola dove chi presidia la struttura la vede bene.
6. **Controllo.** Il monitor seriale scrive l'indirizzo della pagina, per esempio `http://192.168.1.50/`. Aprilo da un telefono collegato alla stessa rete. I dati grezzi sono in `/dati.json`.
7. **Prova di confronto.** Prima di usarlo, confronta per qualche ora temperatura e umidità con un termoigrometro di riferimento messo accanto.

## Che cosa fare quando si accendono i LED

Il dispositivo non dà istruzioni. Chi lo installa decide prima, con il responsabile della struttura, chi controlla i LED e chi avvisa quando si accendono. I comportamenti da tenere con il caldo sono quelli indicati dal Ministero della Salute; se una persona sta male si chiama il **112**.

## File da scaricare

- [monitor-caldo.ino](/elettronica-emergenza/monitor-caldo/monitor-caldo.ino), lo sketch.
- [config.h](/elettronica-emergenza/monitor-caldo/config.h), le impostazioni: pin, indirizzo del sensore, misure, isteresi, Wi-Fi.
- [segreti.h.esempio](/elettronica-emergenza/monitor-caldo/segreti.h.esempio), il modello per i dati del Wi-Fi.
- [README.txt](/elettronica-emergenza/monitor-caldo/README.txt), le istruzioni brevi.
- [Scatola](/elettronica-emergenza/monitor-caldo/custodia-monitor-caldo-scatola.stl), [coperchio](/elettronica-emergenza/monitor-caldo/custodia-monitor-caldo-coperchio.stl) e [guarnizione](/elettronica-emergenza/monitor-caldo/custodia-monitor-caldo-guarnizione.stl) della custodia (STL).
- [Modello della custodia](/elettronica-emergenza/monitor-caldo/custodia-monitor-caldo.scad) per OpenSCAD, da modificare.
- [Testo della licenza EUPL 1.2](/elettronica-emergenza/LICENZA-EUPL-1.2.txt).

Metti i file dello sketch in una cartella chiamata `monitor-caldo` e scegli la scheda «ESP32 Dev Module». Non servono librerie esterne: I2C, Wi-Fi e pagina web fanno parte del pacchetto esp32 di Espressif. Lo sketch compila con la versione 4.0.0 del pacchetto, con e senza Wi-Fi, prova del 24 novembre 2026. Non è ancora stato provato su un dispositivo vero.

La custodia esterna misura circa 114 × 56 × 35 mm, alette comprese. Il coperchio ha tre fori da 5,2 mm per i LED: allargali o stringili in `custodia-monitor-caldo.scad` se i tuoi LED non entrano. Al chiuso basta il PETG; la guarnizione va in TPU. Nessuna parte chiede supporti.

## Fonti

Verificate il 24 novembre 2026.

- National Weather Service, Weather Prediction Center, [The Heat Index Equation](https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml): formula semplice, regressione di Rothfusz (NWS Technical Attachment SR 90-23, 1990), correzioni per umidità sotto il 13 % e sopra l'85 %, limiti di validità.
- National Weather Service, ufficio di Amarillo, [Heat Index](https://www.weather.gov/ama/heatindex): fasce Caution, Extreme Caution, Danger ed Extreme Danger, esempi di calcolo, valori riferiti all'ombra e fino a 15 °F in più al sole diretto.
- National Weather Service, [Heat Index](https://www.weather.gov/safety/heat-index): indice pensato per l'ombra e il vento debole.
- Sensirion, [scheda tecnica SHT4x](https://sensirion.com/media/documents/33FD6951/6A7C10A0/HT_DS_Datasheet_SHT4x_V7.3.pdf), versione 7.3, giugno 2026: alimentazione da 1,08 a 3,6 V, indirizzo 0x44 delle versioni AD1B, precisione dell'umidità, tempi di misura (capitolo 3.1), somma di verifica CRC-8 (capitolo 4.4), comando 0xFD (capitolo 4.5), conversione dei valori (capitolo 4.6).
- Bosch Sensortec, [scheda tecnica del BME280](https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bme280-ds002.pdf), revisione 1.24: precisione dell'umidità di ±3 punti percentuali, per il confronto.
- Ministero della Salute, [Ondate di calore](https://www.salute.gov.it/new/it/tema/ondate-di-calore/), [Dieci consigli utili](https://www.salute.gov.it/new/it/tema/ondate-di-calore/dieci-consigli-utili/) e [Bollettini sulle ondate di calore](https://www.salute.gov.it/new/it/tema/ondate-di-calore/bollettini-sulle-ondate-di-calore-0/): bollettini giornalieri per 27 città, fra cui Roma.
- Espressif, [pin I2C predefiniti del pacchetto Arduino-ESP32 4.0.0](https://github.com/espressif/arduino-esp32/blob/4.0.0/variants/esp32/pins_arduino.h): SDA su GPIO 21, SCL su GPIO 22.
- Espressif, [installazione del pacchetto Arduino-ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html).
- Arduino, [arduino-cli](https://arduino.github.io/arduino-cli/latest/).

Codice con licenza EUPL 1.2, testi e modello della custodia con licenza CC BY-NC-SA 4.0. Gli altri progetti sono nella pagina [Elettronica per l'emergenza](/elettronica-emergenza/).
