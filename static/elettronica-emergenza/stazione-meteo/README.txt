STAZIONE METEO CON ESP32: TEMPERATURA, UMIDITA', PRESSIONE E VENTO
Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
Istruzioni complete: https://www.protezionecivilegenzano.it/elettronica-emergenza/stazione-meteo/

ATTENZIONE
- Dispositivo non certificato: le misure servono a osservare il tempo sul posto.
- Non sostituisce le stazioni della rete regionale, i bollettini del Centro
  Funzionale ne' il 112. Se c'e' pericolo per le persone, chiama il 112.
- La pressione e' quella alla quota della stazione, non riportata al livello
  del mare.
- Mai collegamenti alla rete a 230 V: alimentatore USB certificato.
- La pagina web funziona solo nella rete locale: non aprirla su internet
  dal router.
- Per la pioggia c'e' il progetto a parte del pluviometro:
  https://www.protezionecivilegenzano.it/elettronica-emergenza/pluviometro/

FILE
- stazione-meteo.ino     sketch per ESP32
- config.h               impostazioni: pin, indirizzo del BME280, taratura del vento, Wi-Fi
- segreti.h.esempio      modello per i dati del Wi-Fi
- schermo-solare.scad                  modello dello schermo solare (OpenSCAD)
- schermo-solare-base.stl              base con tubo per il cavo e staffa
- schermo-solare-piatto.stl            piatto (stampane 5)
- schermo-solare-cappello.stl          cappello
- custodia-stazione-meteo.scad             modello della scatola (OpenSCAD)
- custodia-stazione-meteo-scatola.stl      scatola (ASA)
- custodia-stazione-meteo-coperchio.stl    coperchio (ASA)
- custodia-stazione-meteo-guarnizione.stl  guarnizione (TPU)
- LICENZA-EUPL-1.2.txt   si scarica dalla pagina del progetto

COLLEGAMENTI (ESP32 classico)
- BME280: VCC a 3V3 (mai a 5V), GND a GND, SDA a GPIO 21, SCL a GPIO 22.
  SDO a GND = indirizzo 0x76, SDO a 3V3 = indirizzo 0x77 (non lasciarlo
  scollegato se il modulo non lo collega gia').
- Anemometro: un filo a GPIO 27, l'altro a GND; resistenza da 10 kohm fra
  GPIO 27 e 3V3.

COME SI CARICA
1. Metti stazione-meteo.ino, config.h e segreti.h.esempio in una cartella
   chiamata stazione-meteo.
2. Copia segreti.h.esempio con il nome segreti.h e scrivi nome e password
   del Wi-Fi. Non condividere mai segreti.h.
   Senza Wi-Fi: metti USA_WIFI false in config.h (segreti.h non serve).
3. Pacchetto "esp32" di Espressif, scheda "ESP32 Dev Module". Con arduino-cli:
     arduino-cli compile --fqbn esp32:esp32:esp32 stazione-meteo
     arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32 stazione-meteo
4. Il monitor seriale (115200 baud) mostra l'indirizzo della pagina dei dati,
   per esempio http://192.168.1.50/ ; i dati grezzi sono in /dati.json.
Nessuna libreria esterna: Wire, WiFi e WebServer fanno parte del pacchetto esp32.
Lo sketch compila con il pacchetto esp32 versione 4.0.0, con e senza Wi-Fi
(prova del 24/11/2026). Non e' ancora stato provato su un dispositivo vero.

TARATURA DEL VENTO (KMH_PER_HZ in config.h)
- Se la scheda tecnica del tuo anemometro dice quanti km/h corrispondono a
  una chiusura del contatto al secondo, scrivi quel valore.
- Altrimenti: monta l'anemometro accanto a un anemometro di riferimento
  tarato, annota per 10 minuti la velocita' media del riferimento (km/h) e
  il valore vento_hz_media_1min di /dati.json, e dividi i km/h per gli
  impulsi al secondo. Ripeti in tre giornate e usa la media.
Con KMH_PER_HZ = 0 lo sketch mostra solo gli impulsi al secondo.

SCHERMO SOLARE
- Stampa base, 5 piatti e cappello in ASA bianco, senza supporti, con il
  bordo largo sul piatto della stampante.
- Tre barre filettate M5 in acciaio inox di circa 20 cm, dadi sopra e sotto.
- Il cavo del BME280 sale nel tubo centrale della base; lega il modulo in
  cima al tubo con una fascetta.

LICENZE
Codice: EUPL 1.2. Testi, schermo solare e scatola: CC BY-NC-SA 4.0.
Pacchetto esp32 di Espressif: licenza LGPL 2.1, usato come strumento.
