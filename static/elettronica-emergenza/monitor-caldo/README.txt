MONITOR DEL CALDO PER TENDE E SALE D'ATTESA CON ESP32
Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
Istruzioni complete: https://www.protezionecivilegenzano.it/elettronica-emergenza/monitor-caldo/

ATTENZIONE
- Dispositivo non certificato: segnala un'anomalia da verificare, non un
  allarme, e non dice che un ambiente e' sicuro.
- Non da' consigli sanitari. Per il caldo segui le indicazioni del Ministero
  della Salute: https://www.salute.gov.it/new/it/tema/ondate-di-calore/
- Non sostituisce i bollettini del Ministero, il parere di un medico ne' il
  112. Se una persona sta male, chiama il 112.
- Le fasce sono quelle del National Weather Service statunitense, valgono
  all'ombra e con poco vento e non coincidono con i livelli dei bollettini
  italiani.
- Mai collegamenti alla rete a 230 V: alimentatore USB certificato o power bank.
- La pagina web funziona solo nella rete locale: non aprirla su internet
  dal router. Il dispositivo non raccoglie dati sulle persone.

FILE
- monitor-caldo.ino      sketch per ESP32
- config.h               impostazioni: pin, indirizzo del sensore, misure, isteresi, Wi-Fi
- segreti.h.esempio      modello per i dati del Wi-Fi
- custodia-monitor-caldo.scad             modello della custodia (OpenSCAD)
- custodia-monitor-caldo-scatola.stl      scatola (PETG)
- custodia-monitor-caldo-coperchio.stl    coperchio con 3 fori per i LED (PETG)
- custodia-monitor-caldo-guarnizione.stl  guarnizione (TPU)
- LICENZA-EUPL-1.2.txt   si scarica dalla pagina del progetto

COLLEGAMENTI (ESP32 classico)
- Sensore SHT40, SHT41 o SHT45 (versione AD1B, indirizzo 0x44): VCC a 3V3
  (mai a 5V), GND a GND, SDA a GPIO 21, SCL a GPIO 22. Il sensore sta fuori
  dalla scatola, su un cavo di circa 30 cm.
- LED giallo a GPIO 25, arancione a GPIO 26, rosso a GPIO 27, ognuno con una
  resistenza da 330 ohm; i piedini corti a GND.

COSA DICONO I LED
- nessuno: indice di calore sotto 26,7 C
- 1 LED: da 26,7 C (fascia NWS "Caution")
- 2 LED: da 32,2 C ("Extreme Caution")
- 3 LED fissi: da 39,4 C ("Danger")
- 3 LED che lampeggiano: da 51,7 C ("Extreme Danger")
- solo il LED centrale, un lampo ogni 2 secondi: sensore da controllare
Dalla prima fascia in su e' un'anomalia da verificare: chi la vede controlla
e avvisa il responsabile della struttura.

COME SI CARICA
1. Metti monitor-caldo.ino, config.h e segreti.h.esempio in una cartella
   chiamata monitor-caldo.
2. Copia segreti.h.esempio con il nome segreti.h e scrivi nome e password
   del Wi-Fi. Non condividere mai segreti.h.
   Senza Wi-Fi: metti USA_WIFI false in config.h (segreti.h non serve).
3. Pacchetto "esp32" di Espressif, scheda "ESP32 Dev Module". Con arduino-cli:
     arduino-cli compile --fqbn esp32:esp32:esp32 monitor-caldo
     arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32 monitor-caldo
4. Il monitor seriale (115200 baud) mostra l'indirizzo della pagina dei dati,
   per esempio http://192.168.1.50/ ; i dati grezzi sono in /dati.json.
Nessuna libreria esterna: Wire, WiFi e WebServer fanno parte del pacchetto esp32.
Lo sketch compila con il pacchetto esp32 versione 4.0.0, con e senza Wi-Fi
(prova del 24/11/2026). Non e' ancora stato provato su un dispositivo vero.

CALCOLO
Indice di calore con il metodo del National Weather Service (pagina "The Heat
Index Equation" del Weather Prediction Center): formula semplice, poi
regressione di Rothfusz con le correzioni per umidita' sotto il 13 % e sopra
l'85 %. Lettura del sensore secondo la scheda tecnica Sensirion SHT4x
(comando 0xFD, controllo CRC-8).

LICENZE
Codice: EUPL 1.2. Testi e modello della custodia: CC BY-NC-SA 4.0.
Pacchetto esp32 di Espressif: licenza LGPL 2.1, usato come strumento.
