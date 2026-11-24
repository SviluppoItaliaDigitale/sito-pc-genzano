---
title: "Sensore del livello dell'acqua per un fosso o un sottopasso"
description: "Un ESP32 e un sensore a ultrasuoni impermeabile misurano l'acqua in un fosso o in un sottopasso e accendono un LED con un cicalino quando supera una soglia."
date: 2026-11-24
dataUltimaRevisione: "2026-11-24"
image: ""
tts: true
---

Questo dispositivo misura ogni pochi minuti la distanza fra un sensore montato in alto e la superficie dell'acqua. Ne ricava il livello e, quando supera la soglia che hai scelto, accende un LED e un cicalino sul posto. Serve a chi tiene d'occhio un punto critico, per esempio un fosso che esce dagli argini o un sottopasso che si allaga, e vuole accorgersene prima di passarci.

## Limiti e avvertenze

- È un dispositivo **non certificato**: segnala un'**anomalia da verificare**, non un allarme. Chi la vede va a controllare o avvisa chi di dovere con i canali ufficiali.
- Non sostituisce le allerte del Centro Funzionale della Regione Lazio, gli idrometri della rete regionale, IT-alert né il **112**. Se c'è pericolo per le persone, chiama il 112.
- Il segnale è solo locale: LED e cicalino si vedono e si sentono vicino al dispositivo. Non manda messaggi a distanza.
- Il sensore non misura sotto circa 20 cm e può sbagliare con schiuma, rami o pioggia fitta sotto la sonda. Una misura non valida non cambia lo stato: il dispositivo riprova dopo.
- **Mai collegamenti alla rete a 230 V.** Alimentalo con un power bank o un alimentatore USB certificato. Alcuni power bank si spengono quando il consumo è basso: prova il tuo per qualche giorno.
- Per installarlo su un argine, un palo o un muro serve il permesso di chi gestisce il luogo, di solito il Comune.

## Componenti

| Quantità | Componente | Note |
|---|---|---|
| 1 | Scheda di sviluppo ESP32 con modulo ESP32-WROOM-32 | per esempio ESP32-DevKitC di Espressif o un'altra equivalente |
| 1 | Sensore a ultrasuoni impermeabile JSN-SR04T, versione 3.0 | sonda con cavo e scheda di controllo |
| 1 | LED rosso o giallo da 5 mm | |
| 1 | Resistenza da 330 Ω | per il LED |
| 1 | Modulo cicalino attivo da 3,3 V con transistor | facoltativo |
| 1 | Basetta millefori e cavetti | |
| 1 | Power bank USB o alimentatore USB certificato, con cavo | |
| 2 | Pressacavi PG7 | uno per la sonda, uno per l'alimentazione |
| 4 | Viti M3 in acciaio inox | per il coperchio |
| 1 | Custodia stampata in 3D | file più sotto |
| 1 | Staffa o supporto per la sonda | la sonda guarda verso il basso, in verticale |

Usa la versione 3.0 del modulo JSN-SR04T, scritta sulla sua scheda: la scheda tecnica ammette un'alimentazione da 3,0 a 5,5 V, quindi a 3,3 V il segnale Echo resta a 3,3 V, come vuole l'ESP32. Con un'altra versione leggi la sua scheda tecnica. Se va alimentata a 5 V, abbassa il segnale Echo a 3,3 V con un partitore: 1 kΩ dal modulo al pin, 2 kΩ dal pin a GND.

## Collegamenti

| Da | A (ESP32) |
|---|---|
| JSN-SR04T, pin 5V o VCC | 3V3 |
| JSN-SR04T, pin Trig | GPIO 25 |
| JSN-SR04T, pin Echo | GPIO 34 |
| JSN-SR04T, pin GND | GND |
| LED, piedino lungo (anodo), attraverso la resistenza da 330 Ω | GPIO 27 |
| LED, piedino corto (catodo) | GND |
| Cicalino, ingresso del segnale | GPIO 26 |
| Cicalino, VCC e GND | 3V3 e GND |

Il GPIO 34 dell'ESP32 è solo un ingresso: va bene per Echo. I pin si cambiano in `config.h`.

## Montaggio

1. **Prova al banco.** Collega tutto su una basetta, carica lo sketch e apri il monitor seriale a 115200 baud. Punta la sonda verso un secchio d'acqua e controlla le distanze con un metro.
2. **Taratura.** Sul posto, a secco, misura con un metro la distanza fra la faccia della sonda e il fondo. Scrivila in `ALTEZZA_SENSORE_CM`. Scegli con chi gestisce il luogo il livello d'acqua da segnalare e scrivilo in `SOGLIA_LIVELLO_CM`. La sonda deve stare almeno 21 cm sopra la soglia.
3. **Isteresi.** `ISTERESI_CM` dice di quanto deve scendere il livello per tornare normale. Evita che il LED si accenda e si spenga di continuo con le piccole onde.
4. **Custodia.** Stampa scatola, coperchio e guarnizione. Fai passare il cavo della sonda e quello dell'alimentazione nei pressacavi e monta la scatola con i pressacavi **verso il basso**: l'acqua scorre via invece di fermarsi.
5. **Fissaggio.** Fissa la sonda in verticale, sopra il punto più basso, lontana da pareti e rami. La custodia sta più in alto, fuori dalla portata dell'acqua.
6. **Prova di una settimana.** Metti accanto un'asta graduata e confronta le letture prima di fidarti del dispositivo.

### Che cosa dice il LED

| Segnale | Significato |
|---|---|
| Un lampo breve a ogni misura | Il dispositivo è acceso e misura |
| Tre lampi lunghi con il cicalino, a ogni misura | Anomalia da verificare: il livello ha superato la soglia |
| Cinque lampi rapidi | Sensore da controllare: niente misure valide da tre risvegli |
| Due lampi lunghi | Taratura mancante in `config.h` |

Fra una misura e l'altra la scheda dorme per risparmiare batteria: 5 minuti in condizioni normali, 1 minuto durante un'anomalia. Quanto dura la batteria dipende dalla scheda e dal power bank: misura il consumo e prova sul campo.

## File da scaricare

- [livello-acqua.ino](/elettronica-emergenza/livello-acqua/livello-acqua.ino), lo sketch.
- [config.h](/elettronica-emergenza/livello-acqua/config.h), le impostazioni: pin, taratura, tempi.
- [README.txt](/elettronica-emergenza/livello-acqua/README.txt), le istruzioni brevi.
- [Scatola](/elettronica-emergenza/livello-acqua/custodia-livello-acqua-scatola.stl), [coperchio](/elettronica-emergenza/livello-acqua/custodia-livello-acqua-coperchio.stl) e [guarnizione](/elettronica-emergenza/livello-acqua/custodia-livello-acqua-guarnizione.stl) della custodia (STL).
- [Modello della custodia](/elettronica-emergenza/livello-acqua/custodia-livello-acqua.scad) per OpenSCAD, da modificare.
- [Testo della licenza EUPL 1.2](/elettronica-emergenza/LICENZA-EUPL-1.2.txt).

Metti `livello-acqua.ino` e `config.h` in una cartella chiamata `livello-acqua`. Scegli la scheda «ESP32 Dev Module» e carica lo sketch. Non servono librerie esterne: lo sketch compila con il pacchetto esp32 di Espressif versione 4.0.0, prova del 24 novembre 2026.

La custodia esterna misura circa 134 × 61 × 40 mm, alette comprese. Scatola e coperchio vanno in ASA, o in PETG se il dispositivo sta al riparo; la guarnizione in TPU. Nessuna parte chiede supporti: stampa la scatola con il fondo sul piatto e il coperchio con la faccia piana sul piatto.

## Fonti

Verificate il 24 novembre 2026.

- Scheda tecnica del modulo JSN-SR04T versione 3.0: alimentazione da 3,0 a 5,5 V, distanza da 20 a 600 cm, impulso di comando di almeno 10 microsecondi.
- Espressif, [GPIO dell'ESP32](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/gpio.html): i GPIO da 34 a 39 sono solo ingressi.
- Espressif, [installazione del pacchetto Arduino-ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html).
- Arduino, [arduino-cli](https://arduino.github.io/arduino-cli/latest/).

Codice con licenza EUPL 1.2, testi e modello della custodia con licenza CC BY-NC-SA 4.0. Gli altri progetti sono nella pagina [Elettronica per l'emergenza](/elettronica-emergenza/).
