---
title: "Controllo della batteria a 12 V con ESP32"
description: "Un ESP32 misura la batteria a 12 V di un mezzo o di un gruppo elettrogeno e segnala con un LED una tensione bassa da verificare."
date: 2026-11-24
dataUltimaRevisione: "2026-11-24"
image: ""
tts: true
---

Una batteria che si scarica piano, su un mezzo fermo o su un gruppo elettrogeno di riserva, si scopre spesso solo quando serve. Questo progetto la tiene d'occhio. Un partitore resistivo, cioè due resistenze in serie, riduce la tensione della batteria a un valore che l'ESP32 può misurare con il suo ADC (convertitore analogico-digitale). La scheda calcola la tensione ogni 5 secondi, la mostra su una pagina nella rete della sede e accende un LED quando resta bassa per un minuto.

## Limiti e avvertenze

- È un dispositivo **non certificato**. Una tensione bassa è un'**anomalia da verificare**: controlla la batteria con un multimetro o un tester e, se serve, chiedi a chi cura la manutenzione del mezzo. Non sostituisce la manutenzione né il **112**.
- Si lavora **solo sul lato a 12 V** in corrente continua. **Mai collegamenti alla rete a 230 V** né all'uscita a 230 V del gruppo elettrogeno.
- La stima della carica vale **solo con la batteria a riposo**: nessuna carica e nessuna scarica da almeno 6 ore, meglio 24, e carichi staccati. Con il motore acceso, il gruppo in moto o un caricabatterie collegato la tensione sale e la stima non vale. Anche questo dispositivo assorbe un po' di corrente: la lettura resta un'indicazione.
- La tabella della carica è quella di un produttore per le sue batterie al piombo a elettrolito liquido. Per altre batterie, come quelle AGM, a gel, al calcio o al litio, le tensioni a riposo sono diverse e la stima non vale: usa i dati del loro produttore.
- Quando colleghi la scheda al computer con il cavo USB per caricare lo sketch o leggere la seriale, **scollega prima il convertitore** (togli il fusibile): su molte schede due alimentazioni a 5 V collegate insieme possono far rientrare corrente nella porta USB del computer.
- Senza taratura l'errore può superare mezzo volt: quasi la differenza fra una batteria piena, 12,73 V a riposo, e una a metà, 12,10 V. Fai sempre la taratura con un multimetro.
- La scheda consuma corrente dalla batteria che controlla. Con il Wi-Fi acceso il solo chip ESP32 assorbe da 95 a 100 mA a 3,3 V: dalla batteria a 12 V, con le perdite del convertitore, si stimano alcune decine di mA, intorno a 1 Ah al giorno. Misura il consumo vero. Su un mezzo fermo per settimane collegalo solo se la batteria è anche sotto un mantenitore di carica, oppure staccalo.
- Non mettere la scatola sopra la batteria: i produttori di impianti a batteria sconsigliano gli apparecchi elettronici sopra le batterie al piombo.
- Sui mezzi del Gruppo chiedi prima a chi ne cura la manutenzione. La pagina funziona solo nella rete locale: non aprirla su internet dal router.

## Componenti

| Quantità | Componente | Note |
|---|---|---|
| 1 | Scheda di sviluppo ESP32 con modulo ESP32-WROOM-32 | per esempio ESP32-DevKitC di Espressif o un'altra equivalente |
| 1 | Convertitore da 12 V a 5 V con uscita USB, per veicoli | ingresso almeno fino a 24 V: in equalizzazione la batteria arriva a 16,2 V |
| 1 | Cavo USB corto | dal convertitore alla scheda |
| 1 | Resistenza da 100 kΩ, tolleranza 1% | lato alto del partitore |
| 1 | Resistenza da 15 kΩ, tolleranza 1% | lato basso del partitore |
| 1 | Condensatore da 100 nF | riduce il rumore della misura |
| 1 | LED da 5 mm e resistenza da 330 Ω | per la tensione bassa |
| 1 | Portafusibile in linea con fusibile a lama da 1 A | sul filo positivo, vicino alla batteria |
| 1 | Cavo a due fili, rosso e nero, con due capicorda a occhiello | dalla batteria alla scatola |
| 1 | Pressacavo PG7 | per il cavo della batteria |
| 4 | Viti M3 in acciaio inox | per il coperchio |
| 1 | Multimetro | per la taratura |
| 1 | Custodia stampata in 3D | file più sotto |

## Collegamenti

| Da | A |
|---|---|
| Morsetto positivo (+) della batteria | portafusibile, il più vicino possibile al morsetto |
| Uscita del portafusibile, filo rosso | ingresso positivo del convertitore e resistenza da 100 kΩ |
| Altro capo della resistenza da 100 kΩ | GPIO 34 dell'ESP32 |
| Resistenza da 15 kΩ | fra GPIO 34 e GND |
| Condensatore da 100 nF | fra GPIO 34 e GND, vicino alla scheda |
| Morsetto negativo (−) della batteria, filo nero | ingresso negativo del convertitore e GND dell'ESP32 |
| Uscita USB del convertitore | presa USB dell'ESP32 |
| LED, piedino lungo (anodo), attraverso la resistenza da 330 Ω | GPIO 26 |
| LED, piedino corto (catodo) | GND |

Il fusibile protegge solo il cavo che viene dopo di lui: per questo va subito accanto al morsetto positivo. Inserisci il fusibile nel portafusibile **solo a collegamenti finiti**, e toglilo prima di mettere mano ai fili.

Con 100 kΩ e 15 kΩ al pin arriva circa 1/7,67 della tensione della batteria. Con l'attenuazione più alta l'ADC misura con precisione fino a circa 2,45 V sul pin, cioè fino a circa 18,7 V di batteria. Il pin regge al massimo 3,6 V, che corrispondono a circa 27,6 V di batteria. GPIO 34 appartiene all'ADC1, che funziona anche con il Wi-Fi acceso: l'ADC2 invece lo usa il Wi-Fi. I pin e i valori delle resistenze si cambiano in `config.h`.

## Taratura

1. Con la scheda accesa, misura la tensione ai morsetti della batteria con il multimetro.
2. Leggi nello stesso momento la tensione sulla pagina o sul monitor seriale.
3. Calcola: correzione = tensione del multimetro ÷ tensione della scheda. Per esempio 12,64 ÷ 12,48 = 1,013.
4. Scrivi il risultato in `CORREZIONE`, in `config.h`, e carica di nuovo lo sketch.

Ripeti il controllo con la batteria in carica, intorno a 14 V: se le due letture si discostano, usa la media delle due correzioni.

Lo sketch legge il pin con `analogReadMilliVolts()`, che restituisce millivolt già corretti con la taratura di fabbrica del chip. Fa 21 letture e usa la mediana, così un disturbo isolato non conta.

## Stato di carica a riposo

Questa è la tabella di Trojan Battery per una batteria al piombo da 12 V, con la tensione misurata a vuoto dopo almeno 6 ore di riposo. Lo sketch la usa per la stima.

| Carica | Tensione a riposo |
|---|---|
| 100% | 12,73 V |
| 90% | 12,62 V |
| 80% | 12,50 V |
| 70% | 12,37 V |
| 60% | 12,27 V |
| 50% | 12,10 V |
| 40% | 11,89 V |
| 30% | 11,81 V |
| 20% | 11,66 V |
| 10% | 11,51 V |

Il produttore consiglia di ricaricare la batteria quando la tabella indica il 70% o meno. La soglia predefinita del LED, 12,10 V, corrisponde al 50%. Si cambia in `config.h` con `SOGLIA_BASSA_V`.

## Come si comporta

- **Tensione bassa da verificare.** Se la tensione resta sotto la soglia per 12 misure di fila, cioè un minuto, il LED si accende e la pagina lo scrive. Un calo breve, come all'avviamento del motore, non basta. Il LED si spegne quando la tensione torna sopra la soglia più 0,2 V.
- **Riposo della scheda.** Sotto 11,80 V per un minuto la scheda va in sonno profondo per 60 minuti e poi rimisura, per non scaricare ancora la batteria. In sonno la pagina non risponde e il LED è spento: una pagina che non risponde può quindi voler dire una batteria molto scarica, da controllare subito. Con `TENSIONE_SONNO_V 0` in `config.h` la scheda non va mai in sonno.
- **Fuori scala.** Sopra circa 18,7 V la pagina avvisa che la misura non è precisa: controlla il partitore.

## Montaggio

1. **Prova al banco.** Collega il partitore a un alimentatore da banco regolabile al posto della batteria. Carica lo sketch e apri il monitor seriale a 115200 baud. Porta la tensione da 11 a 15 V e controlla le letture con il multimetro.
2. **Wi-Fi.** Copia `segreti.h.esempio` con il nome `segreti.h` e scrivi nome e password della rete. Senza Wi-Fi metti `USA_WIFI false` in `config.h`: i dati escono solo sul monitor seriale e la scheda consuma meno.
3. **Taratura.** Segui i passi qui sopra e scrivi `CORREZIONE`.
4. **Installazione.** Fissa la scatola in un punto asciutto, lontano dal motore e mai sopra la batteria, con il pressacavo verso il basso. Monta il portafusibile vicino al morsetto positivo e inserisci il fusibile solo alla fine.
5. **Controllo.** Il monitor seriale scrive l'indirizzo della pagina, per esempio `http://192.168.1.50/`. Aprilo da un telefono collegato alla stessa rete. I dati grezzi sono in `/dati.json`.

## File da scaricare

- [batteria-12v.ino](/elettronica-emergenza/batteria-12v/batteria-12v.ino), lo sketch.
- [config.h](/elettronica-emergenza/batteria-12v/config.h), le impostazioni: pin, partitore, taratura, soglie, Wi-Fi.
- [calcoli.h](/elettronica-emergenza/batteria-12v/calcoli.h), i calcoli: tensione, mediana, stima della carica, soglia.
- [segreti.h.esempio](/elettronica-emergenza/batteria-12v/segreti.h.esempio), il modello per i dati del Wi-Fi.
- [README.txt](/elettronica-emergenza/batteria-12v/README.txt), le istruzioni brevi.
- [Scatola](/elettronica-emergenza/batteria-12v/custodia-batteria-12v-scatola.stl), [coperchio](/elettronica-emergenza/batteria-12v/custodia-batteria-12v-coperchio.stl) e [guarnizione](/elettronica-emergenza/batteria-12v/custodia-batteria-12v-guarnizione.stl) della custodia (STL).
- [Modello della custodia](/elettronica-emergenza/batteria-12v/custodia-batteria-12v.scad) per OpenSCAD, da modificare.
- [Testo della licenza EUPL 1.2](/elettronica-emergenza/LICENZA-EUPL-1.2.txt).

Metti i file in una cartella chiamata `batteria-12v` e scegli la scheda «ESP32 Dev Module». Non servono librerie esterne: Wi-Fi e pagina web fanno parte del pacchetto esp32 di Espressif. Lo sketch compila con la versione 4.0.0 del pacchetto, con e senza Wi-Fi, prova del 24 novembre 2026. I calcoli sono stati provati sul computer con valori di prova. Il dispositivo non è stato ancora provato su una batteria vera: fai la prova al banco prima di installarlo.

La custodia esterna misura circa 134 × 61 × 35 mm, alette comprese. Il coperchio ha il foro per il LED da 5 mm, da fissare con una goccia di silicone. Scatola e coperchio vanno in ASA, o in PETG se la scatola sta al riparo; la guarnizione in TPU. Nessuna parte chiede supporti.

## Fonti

Verificate il 24 novembre 2026.

- Espressif, [ESP32 Series Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf), versione 5.3: GPIO 34 come ADC1_CH6 (tabella dei pin); differenze fino al 6% fra chip senza taratura e campo di 150-2450 mV con errore di 60 mV con l'attenuazione massima (tabella 4-4); tensione massima dei pin 3,6 V (tabelle 5-1 e 5-3); consumo da 95 a 100 mA con il Wi-Fi in ricezione (tabella 5-4).
- Espressif, [ADC nel pacchetto Arduino-ESP32](https://docs.espressif.com/projects/arduino-esp32/en/latest/api/adc.html): `analogReadMilliVolts()` e attenuazione.
- Espressif, [ADC in modalità oneshot](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/adc/adc_oneshot.html): l'ADC2 è usato anche dal Wi-Fi; [taratura dell'ADC](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/adc/adc_calibration.html): condensatore da 100 nF e più letture contro il rumore.
- Trojan Battery Company, [Battery maintenance](https://www.trojanbattery.com/battery-maintenance): tabella dello stato di carica a vuoto, riposo di almeno 6 ore, meglio 24, carichi staccati; tensioni di carica ed equalizzazione.
- Victron Energy, [Wiring Unlimited, cablaggio in corrente continua](https://victronenergy.com/media/pg/The_Wiring_Unlimited_book/en/dc-wiring.html): fusibile sul cavo positivo, scelto sul valore più basso fra cavo e utilizzatore; niente apparecchi elettronici sopra le batterie al piombo. Victron Energy, [installazione del BMV-712](https://www.victronenergy.com/media/pg/BMV-712_Smart/en/installation.html): cavo di misura con fusibile da 1 A al positivo della batteria.
- Arduino, [arduino-cli](https://arduino.github.io/arduino-cli/latest/).

Codice con licenza EUPL 1.2, testi e modello della custodia con licenza CC BY-NC-SA 4.0. Gli altri progetti sono nella pagina [Elettronica per l'emergenza](/elettronica-emergenza/).
