RICEVITORE DI AEREI ED ELICOTTERI ADS-B CON RASPBERRY PI
Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
Istruzioni complete: https://www.protezionecivilegenzano.it/elettronica-emergenza/ricevitore-adsb/

ATTENZIONE
- Solo ricezione: il ricevitore non trasmette nulla.
- Non tutti trasmettono l'ADS-B: l'obbligo europeo vale solo per gli aerei
  ad ala fissa oltre 5.700 kg o 250 nodi. Se un elicottero non compare
  sulla mappa, non vuol dire che non c'e'.
- Prima di far volare un drone valgono le regole ENAC e le zone di D-Flight:
  il ricevitore e' un aiuto in piu', non le sostituisce.
- La mappa mostra un'anomalia da verificare, mai un allarme. Emergenze: 112.
- Usa la chiavetta solo per i segnali ADS-B, mai per comunicazioni riservate.
- Non pubblicare le posizioni dei mezzi di soccorso durante un intervento.
- Alimentatore ufficiale del Raspberry Pi. Mai collegamenti alla rete
  a 230 V fatti a mano.
- La mappa resta nella rete della sede: non aprirla su internet dal router.

FILE
- installa-ricevitore.sh  scarica dalla fonte ufficiale lo script di
                          installazione di readsb e tar1090, lo mostra
                          (impronta SHA-256 e indirizzi) e lo esegue
- LICENZA-EUPL-1.2.txt    si scarica dalla pagina del progetto

CHE COSA SERVE
- Raspberry Pi (per esempio Raspberry Pi 4) con Raspberry Pi OS, dedicato.
- Chiavetta RTL-SDR (per esempio RTL-SDR Blog V4), prolunga USB.
- Antenna per 1090 MHz. Filtro con amplificatore: facoltativo.

ANTENNA A QUARTO D'ONDA
  lunghezza d'onda = 299.792.458 m/s / 1.090.000.000 Hz = 0,275 m
  quarto d'onda    = 0,275 m / 4 = 68,8 mm
Stilo verticale da 68,8 mm e quattro radiali della stessa lunghezza su un
connettore da pannello. Fili nell'aria: niente fattore di velocita'.
Taglia qualche millimetro in piu' e accorcia guardando la ricezione.

PASSI
1. Prepara la microSD con Raspberry Pi Imager e Raspberry Pi OS.
2. Solo con la chiavetta RTL-SDR Blog V4: installa prima il driver
   aggiornato, istruzioni su https://www.rtl-sdr.com/V4/
   (metodo per i pacchetti Debian).
3. Collega la chiavetta e lancia:
     bash installa-ricevitore.sh
   Per leggere lo script ufficiale prima di installarlo:
     bash installa-ricevitore.sh --solo-scarica
4. Posizione della sede (facoltativa), anche dopo:
     sudo readsb-set-location LATITUDINE LONGITUDINE
5. Se e' il primo programma per SDR sul Raspberry Pi:  sudo reboot
6. Apri da un computer della stessa rete:
     http://INDIRIZZO-DEL-RASPBERRY/tar1090
   Se non si apre:  sudo apt install -y lighttpd  e rilancia l'installazione.
   Registro:        sudo journalctl --no-pager -u readsb

NOTE
- L'installazione toglie altri decodificatori gia' presenti: la chiavetta
  la usa un solo programma.
- Nessun invio dei dati a servizi esterni e nessun aggiornamento automatico
  (script ufficiale letto il 24/11/2026). Aggiornamenti a mano, rilanciando
  lo script dopo averlo letto.
- Non installare programmi di condivisione dei dati (OpenSky, Flightradar24
  e simili) se non lo avete deciso insieme.

LEGGE
Codice delle comunicazioni elettroniche, d.lgs. 259/2003, art. 105, comma 2,
lettera b): sono di libero uso gli apparati radioelettrici solo riceventi
per i quali non sono previste assegnazione di frequenze e protezione.

LICENZE
installa-ricevitore.sh: EUPL 1.2. Testi: CC BY-NC-SA 4.0.
Programmi di terzi, scaricati dalle loro fonti e non copiati qui:
  readsb (wiedehopf, Matthias Wirth): GPL versione 3 o successive
  tar1090 (wiedehopf, Matthias Wirth): GPL versione 2 o successive
  adsb-scripts (wiedehopf): MIT
