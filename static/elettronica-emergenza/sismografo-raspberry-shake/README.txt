SISMOGRAFO RASPBERRY SHAKE IN SEDE O A SCUOLA
Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
Istruzioni complete: https://www.protezionecivilegenzano.it/elettronica-emergenza/sismografo-raspberry-shake/

ATTENZIONE
- Non fa parte della rete sismica ufficiale. Per sapere se c'e' stato un
  terremoto fanno fede i dati dell'INGV: https://terremoti.ingv.it/
- Non da' allarmi e non avvisa prima di un terremoto. Un segnale forte e'
  un'anomalia da verificare (camion, porte, passi vicini).
- Non sostituisce il 112 ne' le indicazioni delle autorita'.
- Alimentatore ufficiale del Raspberry Pi. Mai collegamenti alla rete
  a 230 V fatti a mano.
- Spegni sempre dalla pagina di configurazione: staccare la spina puo'
  rovinare la scheda microSD.

CHE COSA SERVE
- Kit Raspberry Shake (RS1D, RS3D, RS4D o RS&BOOM) con scheda e geofono.
- Raspberry Pi 3 Model B (consigliato), 3 Model B+ o 4 Model B. Il Pi 5 e i
  modelli Zero non sono supportati.
- microSD da almeno 8 GB di tipo "endurance" o industriale (MLC o SLC).
- Alimentatore ufficiale: 5,1 V e 2,5 A (Pi 3) oppure 5,1 V e 3,0 A (Pi 4).
- Cavo di rete Ethernet, livella a bolla, bussola (solo RS3D e RS4D).
- Consigliato: un piccolo gruppo di continuita' (UPS).

PASSI
1. Scarica l'archivio raspishake-release dalla pagina ufficiale:
   https://gitlab.com/raspberryShake-public/raspshake-sd-img/-/releases
   Formatta la microSD in FAT32 (exFAT da 64 GB in su) ed estrai tutto
   l'archivio direttamente sulla scheda.
2. Monta la scheda Raspberry Shake sul connettore GPIO del Raspberry Pi.
   Geofono: "+" con "+" (cavo grigio; per l'RS3D anche rosso e verde).
   Scarica le mani su un oggetto metallico prima di toccare la scheda.
   Viti e piedini della custodia: stretti solo a mano.
3. Posizione: pavimento nudo del piano piu' basso, meglio cemento vicino a
   un muro portante. Lontano da passaggi, macchine (lavatrici,
   condizionatori, caldaie), correnti d'aria e apparecchi Wi-Fi.
   Niente moquette, scrivanie o davanzali.
4. Livella: bolla al centro del cerchio (circa mezzo grado).
   RS3D e RS4D: freccia del nord della scheda verso nord, con la bussola.
5. Collega prima il cavo di rete, poi l'alimentatore. Niente Wi-Fi.
   La prima volta si aggiorna da solo: aspetta 10-20 minuti.
6. Apri http://rs.local/ da un computer della stessa rete.
   Utente myshake, password shakeme: CAMBIALA SUBITO.
7. In Impostazioni indica la posizione dell'edificio e, se decidi di
   condividere i dati, attiva l'invio alla rete del produttore.
   Sulla mappa pubblica la posizione e' spostata di qualche centinaio di
   metri per riservatezza. Salva e riavvia.
8. Grafico in sede: http://rs.local/heli
   Mappa mondiale: https://stationview.raspberryshake.org/

RETE CON FIREWALL (scuole, uffici): connessioni in uscita da permettere
  123 UDP (ora esatta, anche in entrata)
  55555 e 55556 TCP verso raspberryshakedata.com (dati)
  22 e 443 (aggiornamenti), 443 TCP verso raspberryshake.org
  8079 e 18082 TCP verso stationview.raspberryshake.org
  16022 TCP verso data.raspberryshake.org (programma Swarm)
  53 (DNS), se la rete non lo offre gia'
Dai al tecnico l'indirizzo MAC o IP dello strumento.

DATI
Le registrazioni restano sulla scheda per 7 giorni (modificabile), in file
giornalieri miniSEED di circa 15 MB per canale.
Si scaricano da http://rs.local/ : menu Azioni, Download, Dati.

LICENZE
Testi: CC BY-NC-SA 4.0. Programma e immagine della scheda: del produttore,
con le sue licenze, scaricati solo dalla sua pagina ufficiale.
