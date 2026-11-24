---
title: "Posizione dei mezzi con Meshtastic"
description: "Un nodo Meshtastic con GPS sul mezzo invia la posizione sul canale privato della squadra, solo durante il servizio e senza internet."
date: 2026-11-24
dataUltimaRevisione: "2026-11-24"
image: ""
tts: true
---

Durante un servizio lungo, come una ricerca o un presidio esteso, chi coordina vuole sapere dove sono i mezzi anche dove il telefono non prende. Un nodo Meshtastic con GPS, montato sul mezzo, invia la sua posizione via radio sul canale privato **SQUADRA**. Gli altri nodi della squadra la ricevono e l'app Meshtastic la mostra sulla mappa del telefono. Non servono rete cellulare né internet.

Questo progetto parte dal [nodo Meshtastic per la squadra](/elettronica-emergenza/nodo-meshtastic/): prima prepara la rete e il canale SQUADRA con quella pagina, poi configura i nodi dei mezzi con lo script di questa.

## Limiti e avvertenze

- È un aiuto in più. **Non sostituisce le radio del Gruppo**, la sala operativa né il **112**.
- La posizione può arrivare in ritardo o non arrivare: una posizione mancante o vecchia è un'**anomalia da verificare** con la radio, non la prova che il mezzo sia fermo o in difficoltà.
- **Non accendere mai la radio senza l'antenna LoRa avvitata**: il chip radio si può danneggiare.
- Il nodo si monta solo sui **mezzi**, mai sulle persone. Per sapere dove si trova un volontario si usa la radio.
- Valgono le regole della banda a 868 MHz descritte nella pagina del [nodo Meshtastic](/elettronica-emergenza/nodo-meshtastic/): regione EU_868, al massimo 500 mW e.r.p. e trasmissione per il 10% del tempo. **Non attivare mai `override_duty_cycle`**.

## La posizione è un dato personale

La posizione di un mezzo dice anche dove si trova chi lo guida. Il Regolamento europeo sulla protezione dei dati (GDPR) conta i dati relativi all'ubicazione fra i dati personali, chiede di trattare solo i dati necessari allo scopo e di informare le persone interessate. Per questo:

- **Usa la posizione solo durante il servizio.** A fine servizio spegni il nodo oppure esegui `bash posizione.sh spegni`.
- **Prima di usarla serve l'informativa ai volontari**, decisa dal Gruppo: scopo, chi vede le posizioni, per quanto tempo si conservano. Coinvolgi chi cura la privacy per il Gruppo o per il Comune prima di cominciare. Lo script non sostituisce questa decisione.
- **Niente MQTT e niente mappe pubbliche.** Con MQTT il nodo può inoltrare i messaggi a un server su internet, quello pubblico di Meshtastic se non ne indichi un altro. La funzione «map reporting» manda a quel server un rapporto non cifrato con nome, posizione e altri dati del nodo. Lo script spegne entrambe le cose e toglie il passaggio verso internet da tutti i canali.
- **Sul canale pubblico la posizione non esce mai**: lo script mette la precisione a 0, che per Meshtastic vuol dire nessuna posizione su quel canale.
- **Chiama il nodo con il nome del mezzo**, come «PC Genzano Mezzo 01», mai con il nome dell'autista: i nomi dei nodi li vede tutta la rete.
- **Precisione minima utile.** Lo script usa 18 bit sul canale SQUADRA, cioè circa 91 m: basta per sapere in che zona è il mezzo. Alza la precisione solo se il servizio lo richiede.

Se perdi un nodo o il QR del canale finisce dove non deve, crea una chiave nuova con `configura-primo-nodo.sh` del nodo Meshtastic e condividila di nuovo con tutti.

## Componenti

| Quantità per mezzo | Componente | Note |
|---|---|---|
| 1 | Scheda LoRa compatibile con Meshtastic, versione a 868 MHz, **con GPS** | per esempio una LilyGO T-Beam Supreme; controlla che sia nell'elenco dei dispositivi supportati |
| 1 | Antenna per 868 MHz | quella fornita va bene per cominciare |
| 1 | Alimentazione USB dal mezzo | presa USB del mezzo o adattatore certificato per la presa da 12 V |
| 1 | Cavo USB | lo stesso serve per configurare il nodo dal computer |
| 1 | Custodia | quella del produttore della scheda o la [custodia del nodo Meshtastic](/elettronica-emergenza/nodo-meshtastic/), se la scheda ci entra: misurala prima |

Evita le versioni della scheda da 1 W: sono fatte per trasmettere oltre i 500 mW e.r.p. ammessi nella banda.

## Collegamenti

| Da | A |
|---|---|
| Antenna LoRa | connettore d'antenna LoRa della scheda, **prima** di accenderla |
| Cavo USB | presa USB del mezzo, per l'uso; computer, per la configurazione |

Il GPS ha bisogno di vedere il cielo. Metti il nodo vicino a un finestrino o sotto il lunotto, fissato in modo che non si sposti in curva o in frenata e che non intralci la guida. Le batterie al litio soffrono il caldo e d'estate l'abitacolo al sole si scalda molto: se la scheda funziona dalla sola presa USB, nel mezzo tienila senza batteria.

## Come invia la posizione

Lo script dà al nodo il ruolo **TRACKER**, che la documentazione di Meshtastic descrive come pensato per seguire mezzi e cose, con priorità ai pacchetti di posizione; il nodo continua comunque a ripetere i messaggi degli altri. Il risparmio energetico resta spento, perché il nodo è alimentato dal mezzo.

| Impostazione | Valore dello script | Valore predefinito di Meshtastic |
|---|---|---|
| Lettura del GPS (1) | 60 secondi | ogni 2 minuti |
| Invio fisso (2) | 900 secondi, cioè 15 minuti | 15 minuti |
| Invio «intelligente» (3) | acceso | acceso |
| Strada minima fra due invii (4) | 200 m | 100 m |
| Tempo minimo fra due invii (5) | 120 secondi | 30 secondi |

Nomi delle impostazioni nella configurazione di Meshtastic:

1. `position.gps_update_interval`
2. `position.position_broadcast_secs`
3. `position.position_broadcast_smart_enabled`
4. `position.broadcast_smart_minimum_distance`
5. `position.broadcast_smart_minimum_interval_secs`

Con l'invio «intelligente» il nodo manda una posizione nuova quando il mezzo si è spostato di almeno 200 m, ma non più spesso di una volta ogni 2 minuti. Da fermo la manda comunque ogni 15 minuti. Gli intervalli sono più lunghi di quelli predefiniti per una ragione: ogni posizione occupa il canale radio di tutti i nodi che la ripetono e consuma una parte del loro 10% di tempo in aria. Con molti mezzi, allunga gli intervalli all'inizio dello script. Ogni nodo misura da sé l'uso del canale e il proprio tempo in aria e li invia con i dati del dispositivo.

## Configurazione

1. **Rete e canale.** Prepara il primo nodo con `configura-primo-nodo.sh` del [nodo Meshtastic](/elettronica-emergenza/nodo-meshtastic/). Il canale SQUADRA è il secondo canale, con indice 1.
2. **Firmware e programma.** Carica Meshtastic sulla scheda del mezzo con il [Meshtastic Web Flasher](https://flasher.meshtastic.org/) e installa il programma per il computer: `pip3 install --upgrade "meshtastic[cli]"`.
3. **Nodo del mezzo.** Con l'antenna avvitata e la radio collegata via USB, esegui `bash configura-mezzo.sh "PC Genzano Mezzo 01" M01`. Incolla l'indirizzo dei canali quando lo chiede: lo script non lo mostra e non lo salva. Imposta poi regione EU_868, limite del tempo in aria, ruolo TRACKER, MQTT spento, intervalli e precisione della posizione.
4. **Controllo.** Alla fine lo script mostra le impostazioni principali. Controlla regione, ruolo e che il canale con indice 1 sia SQUADRA. Se la tua rete ha un ordine dei canali diverso, cambia `INDICE_SQUADRA` in testa ai due script.
5. **Prova.** Esci con il mezzo per un breve giro e controlla dall'app di un altro nodo della squadra che la posizione arrivi. Annota dove non arriva.
6. **Fine servizio.** Spegni il nodo oppure esegui `bash posizione.sh spegni`. Al servizio successivo: `bash posizione.sh accendi`.

Le impostazioni dello script sono state controllate sulla documentazione ufficiale di Meshtastic e sui nomi dei campi del programma `meshtastic` versione 2.7.11. Gli script sono stati provati al computer con una radio simulata, non su una radio vera: fai la prova del passo 5 prima di usarli in servizio.

## File da scaricare

- [configura-mezzo.sh](/elettronica-emergenza/posizione-mezzi-meshtastic/configura-mezzo.sh), configura il nodo di un mezzo con il canale SQUADRA.
- [posizione.sh](/elettronica-emergenza/posizione-mezzi-meshtastic/posizione.sh), spegne o riaccende l'invio della posizione.
- [README.txt](/elettronica-emergenza/posizione-mezzi-meshtastic/README.txt), le istruzioni brevi.
- [Testo della licenza EUPL 1.2](/elettronica-emergenza/LICENZA-EUPL-1.2.txt).

Gli script sono per il terminale di Linux e macOS; su Windows esegui gli stessi comandi `meshtastic` uno per uno. Non contengono chiavi né indirizzi dei canali. Usano il programma `meshtastic` così com'è, con la sua licenza, senza copiarne il codice.

## Fonti

Verificate il 24 novembre 2026.

- Meshtastic, [impostazioni della posizione](https://meshtastic.org/docs/configuration/radio/position/): nomi, valori ammessi e valori predefiniti di GPS e invio della posizione.
- Meshtastic, [canali](https://meshtastic.org/docs/configuration/radio/channels/): precisione della posizione per canale (0 = nessuna posizione, tabella dei bit), uplink e downlink.
- Meshtastic, [ruoli dei dispositivi](https://meshtastic.org/docs/configuration/radio/device/) e [scegliere il ruolo giusto](https://meshtastic.org/blog/choosing-the-right-device-role/): ruolo TRACKER.
- Meshtastic, [impostazioni LoRa](https://meshtastic.org/docs/configuration/radio/lora/): regione EU_868, 869,4-869,65 MHz, 27 dBm, limite del 10% calcolato sull'ora, `override_duty_cycle`.
- Meshtastic, [MQTT](https://meshtastic.org/docs/configuration/module/mqtt/): server pubblico predefinito e rapporto per la mappa non cifrato.
- Meshtastic, [LilyGO T-Beam](https://meshtastic.org/docs/hardware/devices/lilygo/tbeam/): modelli con GPS e a 868 MHz; [dispositivi supportati](https://meshtastic.org/docs/hardware/devices/).
- Meshtastic, [programma per il computer](https://meshtastic.org/docs/software/python/cli/).
- Unione europea, [Regolamento (UE) 2016/679](https://eur-lex.europa.eu/legal-content/IT/TXT/HTML/?uri=CELEX:32016R0679) (GDPR): articolo 4, punto 1, dati relativi all'ubicazione; articolo 5, paragrafo 1, lettera c, minimizzazione dei dati; articolo 13, informazioni da fornire agli interessati.

Script con licenza EUPL 1.2, testi con licenza CC BY-NC-SA 4.0. Gli altri progetti sono nella pagina [Elettronica per l'emergenza](/elettronica-emergenza/).
