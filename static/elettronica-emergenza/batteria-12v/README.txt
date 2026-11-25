CONTROLLO DELLA BATTERIA A 12 V CON ESP32
Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
Istruzioni complete: https://www.protezionecivilegenzano.it/elettronica-emergenza/batteria-12v/

ATTENZIONE
- Dispositivo non certificato: una tensione bassa e' un'anomalia da verificare
  con un multimetro o un tester. Non sostituisce la manutenzione ne' il 112.
- Solo lato 12 V in corrente continua. Mai collegamenti alla rete a 230 V ne'
  all'uscita a 230 V del gruppo elettrogeno.
- Fusibile da 1 A sul filo positivo, subito accanto al morsetto della batteria.
  Inserisci il fusibile solo a collegamenti finiti; toglilo prima di
  mettere mano ai fili.
- La stima della carica vale solo a riposo: batteria senza carica ne' scarica
  da almeno 6 ore (meglio 24), carichi staccati. Con il motore acceso o il
  caricabatterie collegato non vale. Tabella per batterie al piombo a
  elettrolito liquido: AGM, gel, calcio e litio hanno tensioni diverse.
- Per collegare la scheda al computer via USB (caricamento, seriale) togli
  prima il fusibile: due alimentazioni a 5 V insieme possono far rientrare
  corrente nella porta USB del computer.
- La scheda consuma dalla batteria (stima: intorno a 1 Ah al giorno con il
  Wi-Fi). Misura il consumo vero. Su un mezzo fermo a lungo collegala solo
  con un mantenitore di carica, oppure staccala.
- Non mettere la scatola sopra la batteria. Sui mezzi del Gruppo chiedi prima
  a chi ne cura la manutenzione.
- La pagina web funziona solo nella rete locale: non aprirla su internet.

FILE
- batteria-12v.ino     sketch per ESP32
- config.h             impostazioni: pin, partitore, taratura, soglie, Wi-Fi
- calcoli.h            calcoli: tensione, mediana, stima della carica, soglia
- segreti.h.esempio    modello per i dati del Wi-Fi
- custodia-batteria-12v.scad             modello della custodia (OpenSCAD)
- custodia-batteria-12v-scatola.stl      scatola (ASA o PETG)
- custodia-batteria-12v-coperchio.stl    coperchio con foro per il LED
- custodia-batteria-12v-guarnizione.stl  guarnizione (TPU)
- LICENZA-EUPL-1.2.txt  si scarica dalla pagina del progetto

COLLEGAMENTI
- + batteria -> fusibile 1 A -> ingresso + del convertitore 12 V -> 5 V
                             -> resistenza 100 kohm -> GPIO 34
- GPIO 34 -> resistenza 15 kohm -> GND ; condensatore 100 nF fra GPIO 34 e GND
- - batteria -> ingresso - del convertitore e GND dell'ESP32
- Uscita USB del convertitore -> presa USB dell'ESP32
- GPIO 26 -> resistenza 330 ohm -> LED -> GND
Con 100 kohm e 15 kohm la misura precisa arriva a circa 18,7 V di batteria;
il pin regge al massimo 3,6 V, cioe' circa 27,6 V di batteria.

COME SI CARICA
1. Metti batteria-12v.ino, config.h, calcoli.h e segreti.h.esempio in una
   cartella chiamata batteria-12v.
2. Copia segreti.h.esempio con il nome segreti.h e scrivi nome e password
   del Wi-Fi. Non condividere mai segreti.h.
   Senza Wi-Fi: metti USA_WIFI false in config.h (segreti.h non serve).
3. Pacchetto "esp32" di Espressif, scheda "ESP32 Dev Module". Con arduino-cli:
     arduino-cli compile --fqbn esp32:esp32:esp32 batteria-12v
     arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32 batteria-12v
4. Il monitor seriale (115200 baud) mostra l'indirizzo della pagina dei dati,
   per esempio http://192.168.1.50/ ; i dati grezzi sono in /dati.json.
Nessuna libreria esterna: WiFi e WebServer fanno parte del pacchetto esp32.
Lo sketch compila con il pacchetto esp32 versione 4.0.0, con e senza Wi-Fi
(prova del 24/11/2026). Non ancora provato su una batteria vera: fai prima
la prova al banco con un alimentatore regolabile.

TARATURA (CORREZIONE in config.h)
1. Misura la tensione ai morsetti con un multimetro.
2. Leggi nello stesso momento la tensione sulla pagina o sulla seriale.
3. CORREZIONE = tensione del multimetro / tensione della scheda.
Ripeti con la batteria in carica (circa 14 V) e, se serve, usa la media.
Senza taratura l'errore puo' superare mezzo volt.

SOGLIE (config.h)
- SOGLIA_BASSA_V 12,10 V (50% a riposo nella tabella Trojan Battery):
  LED acceso dopo un minuto sotto soglia, spento sopra 12,30 V.
- TENSIONE_SONNO_V 11,80 V: sotto, per un minuto, la scheda dorme 60 minuti
  per non scaricare ancora la batteria. 0 = mai.

LICENZE
Codice: EUPL 1.2. Testi e modello della custodia: CC BY-NC-SA 4.0.
Pacchetto esp32 di Espressif: licenza LGPL 2.1, usato come strumento.
