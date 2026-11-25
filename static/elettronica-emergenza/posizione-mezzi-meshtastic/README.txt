POSIZIONE DEI MEZZI CON MESHTASTIC
Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
Istruzioni complete: https://www.protezionecivilegenzano.it/elettronica-emergenza/posizione-mezzi-meshtastic/
Rete e canale SQUADRA: https://www.protezionecivilegenzano.it/elettronica-emergenza/nodo-meshtastic/

ATTENZIONE
- Aiuto in piu': non sostituisce le radio del Gruppo, la sala operativa ne'
  il 112. Una posizione mancante o vecchia e' un'anomalia da verificare con
  la radio.
- Mai accendere la radio senza antenna LoRa: il chip radio si puo' danneggiare.
- Banda 869,4-869,65 MHz: al massimo 500 mW e.r.p. e trasmissione per il 10%
  del tempo. Non attivare mai override_duty_cycle. Evita le schede da 1 W.
- La posizione di un mezzo e' un dato personale di chi lo guida:
  * solo durante il servizio, poi nodo spento o "bash posizione.sh spegni";
  * prima serve l'informativa ai volontari decisa dal Gruppo;
  * solo sui mezzi, mai sulle persone;
  * niente MQTT, niente mappe pubbliche (lo script li spegne);
  * nome del nodo = nome del mezzo, mai dell'autista.

FILE
- configura-mezzo.sh   configura il nodo del mezzo con il canale SQUADRA
- posizione.sh         spegne o riaccende l'invio della posizione
- LICENZA-EUPL-1.2.txt  si scarica dalla pagina del progetto

COME SI USA
1. Prepara la rete con configura-primo-nodo.sh (progetto nodo Meshtastic):
   crea il canale SQUADRA, secondo canale (indice 1).
2. Carica il firmware sulla scheda con GPS: https://flasher.meshtastic.org/
   Installa il programma: pip3 install --upgrade "meshtastic[cli]"
3. Antenna avvitata, radio collegata via USB:
     bash configura-mezzo.sh "PC Genzano Mezzo 01" M01 [porta]
   Incolla l'indirizzo dei canali quando lo chiede (non viene mostrato
   ne' salvato).
4. Controlla l'elenco finale: regione EU_868, ruolo TRACKER, MQTT spento,
   canale con indice 1 = SQUADRA. Prova con un breve giro del mezzo.
5. Fine servizio:    bash posizione.sh spegni  [porta]
   Nuovo servizio:   bash posizione.sh accendi [porta]

IMPOSTAZIONI (in testa a configura-mezzo.sh)
- PRECISIONE_SQUADRA=18      circa 91 m sul canale SQUADRA (32 = piena)
- INTERVALLO_FISSO_S=900     posizione almeno ogni 15 minuti
- DISTANZA_MINIMA_M=200      invio dopo 200 m di strada...
- INTERVALLO_MINIMO_S=120    ...ma non piu' spesso di ogni 2 minuti
- AGGIORNAMENTO_GPS_S=60     lettura del GPS ogni minuto
Canale pubblico: precisione 0, nessuna posizione. Uplink e downlink spenti
su entrambi i canali. Con molti mezzi allunga gli intervalli.
Se cambi PRECISIONE_SQUADRA, cambiala anche in posizione.sh.

Gli script non contengono chiavi. Provati al computer con una radio simulata,
non ancora su una radio vera: fai la prova prima del servizio.

LICENZE
Script: EUPL 1.2. Testi: CC BY-NC-SA 4.0.
Il programma meshtastic si usa cosi' com'e', con la sua licenza (GPL 3.0).
