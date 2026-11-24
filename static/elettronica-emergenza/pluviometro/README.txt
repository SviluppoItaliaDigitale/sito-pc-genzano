PLUVIOMETRO A BASCULA CON ESP32
Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
Istruzioni complete: https://www.protezionecivilegenzano.it/elettronica-emergenza/pluviometro/

ATTENZIONE
- Dispositivo non certificato: le misure servono a osservare la pioggia sul posto.
- Non sostituisce le stazioni della rete regionale, i bollettini del Centro
  Funzionale ne' il 112. Se c'e' pericolo per le persone, chiama il 112.
- Mai collegamenti alla rete a 230 V: alimentatore USB certificato.
- La pagina web funziona solo nella rete locale: non aprirla su internet
  dal router.

FILE
- pluviometro.ino        sketch per ESP32
- config.h               impostazioni: pin, taratura, antirimbalzo, soglia, Wi-Fi
- segreti.h.esempio      modello per i dati del Wi-Fi
- custodia-pluviometro.scad             modello della custodia (OpenSCAD)
- custodia-pluviometro-scatola.stl      scatola (ASA o PETG)
- custodia-pluviometro-coperchio.stl    coperchio (ASA o PETG)
- custodia-pluviometro-guarnizione.stl  guarnizione (TPU)
- LICENZA-EUPL-1.2.txt   si scarica dalla pagina del progetto

COME SI CARICA
1. Metti pluviometro.ino, config.h e segreti.h.esempio in una cartella
   chiamata pluviometro.
2. Copia segreti.h.esempio con il nome segreti.h e scrivi nome e password
   del Wi-Fi. Non condividere mai segreti.h.
   Senza Wi-Fi: metti USA_WIFI false in config.h (segreti.h non serve).
3. Pacchetto "esp32" di Espressif, scheda "ESP32 Dev Module". Con arduino-cli:
     arduino-cli compile --fqbn esp32:esp32:esp32 pluviometro
     arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32 pluviometro
4. Il monitor seriale (115200 baud) mostra l'indirizzo della pagina dei dati,
   per esempio http://192.168.1.50/ ; i dati grezzi sono in /dati.json.
Nessuna libreria esterna: WiFi e WebServer fanno parte del pacchetto esp32.
Lo sketch compila con il pacchetto esp32 versione 4.0.0 (prova del 24/11/2026).

TARATURA (MM_PER_SCATTO in config.h)
1. Misura il diametro interno dell'imbuto in millimetri e calcola l'area:
   area (mm2) = 3,1416 x (diametro / 2) x (diametro / 2).
2. Versa lentamente, goccia a goccia, un volume noto d'acqua, per esempio
   100 ml con un cilindro graduato, e conta i ribaltamenti (sul monitor seriale).
3. Millimetri di pioggia versati = volume (ml) x 1000 / area (mm2).
4. MM_PER_SCATTO = millimetri versati / ribaltamenti contati.
Ripeti la prova tre volte e usa la media. Senza taratura lo sketch conta
solo i ribaltamenti e non calcola i millimetri.

LICENZE
Codice: EUPL 1.2. Testi e modello della custodia: CC BY-NC-SA 4.0.
Pacchetto esp32 di Espressif: licenza LGPL 2.1, usato come strumento.
