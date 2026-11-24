SENSORE DEL LIVELLO DELL'ACQUA PER UN FOSSO O UN SOTTOPASSO
Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
Istruzioni complete: https://www.protezionecivilegenzano.it/elettronica-emergenza/livello-acqua/

ATTENZIONE
- Dispositivo non certificato: segnala sul posto un'anomalia da verificare.
- Non sostituisce le allerte ufficiali, gli idrometri della rete regionale ne' il 112.
- Se c'e' pericolo per le persone, chiama il 112.
- Mai collegamenti alla rete a 230 V: alimentazione da power bank USB o da un
  alimentatore USB certificato.
- Per installarlo su un argine, un palo o un muro serve il permesso di chi
  gestisce il luogo.

FILE
- livello-acqua.ino      sketch per ESP32
- config.h               impostazioni: pin, taratura, soglia, tempi
- custodia-livello-acqua.scad             modello della custodia (OpenSCAD)
- custodia-livello-acqua-scatola.stl      scatola (ASA o PETG)
- custodia-livello-acqua-coperchio.stl    coperchio (ASA o PETG)
- custodia-livello-acqua-guarnizione.stl  guarnizione (TPU)
- LICENZA-EUPL-1.2.txt   si scarica dalla pagina del progetto

COME SI CARICA
1. Metti livello-acqua.ino e config.h in una cartella chiamata livello-acqua.
2. Installa Arduino IDE o arduino-cli e il pacchetto "esp32" di Espressif
   (indirizzo del gestore delle schede:
   https://espressif.github.io/arduino-esp32/package_esp32_index.json).
3. Scheda: "ESP32 Dev Module". Con arduino-cli:
     arduino-cli compile --fqbn esp32:esp32:esp32 livello-acqua
     arduino-cli upload -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32 livello-acqua
   (su Windows la porta e' del tipo COM4).
4. Apri il monitor seriale a 115200 baud per leggere le misure.
Nessuna libreria esterna: si usa solo il pacchetto della scheda.
Lo sketch compila con il pacchetto esp32 versione 4.0.0 (prova del 24/11/2026).

TARATURA (in config.h, in centimetri)
- ALTEZZA_SENSORE_CM: distanza dal sensore al fondo, misurata a secco.
- SOGLIA_LIVELLO_CM: livello dal fondo oltre il quale segnalare.
- ISTERESI_CM: di quanto deve scendere il livello per dirlo rientrato.
- Il sensore non misura sotto circa 20 cm: montalo almeno 21 cm sopra la soglia.
Finche' la taratura manca, il LED fa due lampi lunghi e non giudica nulla.

SEGNALI DEL LED
- un lampo breve a ogni misura: acceso e funzionante;
- tre lampi lunghi con il cicalino a ogni misura: anomalia da verificare;
- cinque lampi rapidi: sensore da controllare (nessuna misura valida);
- due lampi lunghi: taratura mancante.

PRIMA DI FIDARTI
Prova al banco con un secchio e un metro, poi una settimana sul posto
confrontando le letture con un'asta graduata.

LICENZE
Codice: EUPL 1.2. Testi e modello della custodia: CC BY-NC-SA 4.0.
Pacchetto esp32 di Espressif: licenza LGPL 2.1, usato come strumento.
