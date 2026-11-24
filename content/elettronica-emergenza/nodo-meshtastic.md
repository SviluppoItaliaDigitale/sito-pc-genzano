---
title: "Nodo Meshtastic per la squadra"
description: "Radio LoRa con Meshtastic per scambiare messaggi brevi fra volontari anche dove il telefono non prende, su un canale privato e nei limiti della banda a 868 MHz."
date: 2026-11-24
dataUltimaRevisione: "2026-11-24"
image: ""
tts: true
---

Meshtastic è un programma libero che trasforma piccole schede radio LoRa (Long Range, radio a lungo raggio e basso consumo) in una rete di messaggi brevi. Ogni radio ripete i messaggi delle altre, quindi la rete arriva più lontano quante più radio ci sono. Con l'app Meshtastic il telefono si abbina alla radio e serve per scrivere e leggere: i messaggi viaggiano via radio, senza rete cellulare né internet. Qui trovi come preparare le radio della squadra con un canale privato.

## Limiti e avvertenze

- Meshtastic è un aiuto in più. **Non sostituisce le radio del Gruppo**, i canali della sala operativa né il **112**.
- I messaggi possono arrivare in ritardo o non arrivare. Non usarlo per comunicazioni da cui dipende la sicurezza di qualcuno.
- **Non accendere mai la radio senza l'antenna avvitata**: il chip radio si può danneggiare.
- Nei messaggi non scrivere dati sanitari né nomi delle persone assistite. Ai nodi dai nomi di servizio, come «PC Genzano 01», mai nome e cognome: li vede tutta la rete.
- Le frequenze radio assegnate al Gruppo non si usano con queste schede e non si pubblicano.

## Le regole della banda a 868 MHz

In Europa Meshtastic usa la regione **EU_868**, cioè la banda da 869,4 a 869,65 MHz. È una banda per dispositivi a corto raggio che si usa senza licenza, con due limiti:

- potenza irradiata al massimo **500 mW e.r.p.**, cioè 27 dBm;
- trasmissione al massimo per il **10% del tempo**, cioè 6 minuti in un'ora.

Li fissa la raccomandazione [ERC 70-03](https://docdb.cept.org/document/845) della CEPT (Conferenza europea delle amministrazioni delle poste e delle telecomunicazioni), allegato 1, banda h1.7. Nella tabella di attuazione nazionale della stessa raccomandazione l'Italia risulta fra i Paesi che la applicano.

Meshtastic rispetta da solo il limite del 10%: quando lo raggiunge, la radio smette di trasmettere e riprende appena può. **Non attivare mai l'opzione `override_duty_cycle`**, che toglie questo limite. Per la potenza conta anche l'antenna: la potenza irradiata è la potenza della radio, più il guadagno dell'antenna in dBi, meno 2,15 dB e meno le perdite del cavo. Una scheda Heltec WiFi LoRa 32 V3 trasmette al massimo a 21 ± 1 dBm: con antenne fino a circa 7 dBi resti entro i 27 dBm. Con antenne più grandi abbassa la potenza della radio.

## Componenti

| Quantità per nodo | Componente | Note |
|---|---|---|
| 1 | Scheda LoRa compatibile con Meshtastic, versione a 868 MHz | per esempio Heltec WiFi LoRa 32 V3, una LilyGO T-Beam o una scheda RAK WisBlock |
| 1 | Antenna per 868 MHz | quella fornita va bene per cominciare |
| 1 | Batteria al litio da 3,7 V con il connettore della scheda | oppure alimentazione USB |
| 1 | Cavo adattatore con connettore SMA da pannello | se l'antenna della tua scheda non ha già un connettore SMA |
| 1 | Pressacavo PG7 | per il cavo USB di ricarica |
| 4 | Viti M3 in acciaio inox | per il coperchio |
| 1 | Custodia stampata in 3D | file più sotto |

Prima di comprare una scheda controlla che sia nell'elenco dei [dispositivi supportati da Meshtastic](https://meshtastic.org/docs/hardware/devices/) e che sia la versione a 868 MHz.

## Collegamenti

La scheda non ha collegamenti da saldare: radio, processore e connettore della batteria sono già sulla scheda.

| Da | A |
|---|---|
| Antenna o cavo adattatore SMA | connettore d'antenna della scheda, **prima** di accenderla |
| Batteria al litio da 3,7 V | connettore della batteria della scheda, rispettando il rosso (+) e il nero (−) |
| Cavo USB | computer, per configurare; alimentatore USB certificato, per ricaricare |

## Preparazione

1. **Firmware.** Carica Meshtastic con il programma ufficiale [Meshtastic Web Flasher](https://flasher.meshtastic.org/), da Chrome o da Edge.
2. **Programma per il computer.** Installa il programma ufficiale: `pip3 install --upgrade "meshtastic[cli]"`.
3. **Primo nodo.** Con l'antenna avvitata e la radio collegata via USB, esegui `bash configura-primo-nodo.sh "PC Genzano 01" PC01`. Lo script imposta la regione EU_868, il preset LONG_FAST della rete locale, 3 salti e il limite del tempo in aria. Poi dà al nodo il ruolo CLIENT e spegne MQTT, che manderebbe i messaggi su internet. Toglie la posizione dal canale pubblico e crea il canale **SQUADRA** con una chiave casuale a 256 bit.
4. **Condivisione del canale.** Alla fine lo script mostra il codice QR dei canali. Fallo inquadrare **di persona** con l'app Meshtastic dagli altri volontari. Non fotografarlo e non mandarlo in chat o per email: contiene la chiave del canale.
5. **Altri nodi.** Per configurarli dal computer, esegui `bash unisci-nodo.sh "PC Genzano 02" PC02` e incolla l'indirizzo dei canali quando lo chiede. Lo script non lo mostra e non lo salva. Per molte radio nello stesso posto, come a una manifestazione, usa il ruolo `CLIENT_MUTE`: non ripetono i messaggi e il canale non si intasa. Per la stazione fissa in sede usa `CLIENT_BASE`.
6. **Prova di portata.** Prova i messaggi dai punti in cui operate e annota dove non arrivano.

Se l'indirizzo o il QR finiscono dove non devono, o se perdi una radio, crea una chiave nuova con `configura-primo-nodo.sh` e condividila di nuovo con tutti.

## Custodia

La custodia ha il foro per un connettore SMA da pannello sul coperchio e un pressacavo per il cavo USB. Monta la scatola con il pressacavo verso il basso. La custodia esterna misura circa 124 × 51 × 32 mm, alette comprese. Scatola e coperchio vanno in ASA, o in PETG se il nodo sta al riparo; la guarnizione in TPU. Nessuna parte chiede supporti.

Le batterie al litio soffrono il caldo. Stampa la custodia in un colore chiaro e, se puoi, mettila all'ombra.

## File da scaricare

- [configura-primo-nodo.sh](/elettronica-emergenza/nodo-meshtastic/configura-primo-nodo.sh), configura il primo nodo e crea il canale SQUADRA.
- [unisci-nodo.sh](/elettronica-emergenza/nodo-meshtastic/unisci-nodo.sh), configura gli altri nodi.
- [README.txt](/elettronica-emergenza/nodo-meshtastic/README.txt), le istruzioni brevi.
- [Scatola](/elettronica-emergenza/nodo-meshtastic/custodia-nodo-meshtastic-scatola.stl), [coperchio](/elettronica-emergenza/nodo-meshtastic/custodia-nodo-meshtastic-coperchio.stl) e [guarnizione](/elettronica-emergenza/nodo-meshtastic/custodia-nodo-meshtastic-guarnizione.stl) della custodia (STL).
- [Modello della custodia](/elettronica-emergenza/nodo-meshtastic/custodia-nodo-meshtastic.scad) per OpenSCAD, da modificare.
- [Testo della licenza EUPL 1.2](/elettronica-emergenza/LICENZA-EUPL-1.2.txt).

Gli script sono per il terminale di Linux e macOS; su Windows esegui gli stessi comandi `meshtastic` uno per uno. Usano il programma `meshtastic` così com'è, con la sua licenza, senza copiarne il codice.

## Fonti

Verificate il 24 novembre 2026.

- CEPT, [raccomandazione ERC 70-03](https://docdb.cept.org/document/845), edizione di ottobre 2026: allegato 1, banda h1.7, 869,4-869,65 MHz, 500 mW e.r.p., trasmissione al massimo per il 10% del tempo; tabella di attuazione nazionale.
- CEPT, [decisione ERC/DEC/(01)04](https://docdb.cept.org/download/2369) sulle bande da 868 a 870 MHz.
- Meshtastic, [impostazioni LoRa](https://meshtastic.org/docs/configuration/radio/lora/): regione EU_868, limite del 10% calcolato sull'ora, preset predefinito LONG_FAST, 3 salti.
- Meshtastic, [canali](https://meshtastic.org/docs/configuration/radio/channels/) e [ruoli dei dispositivi](https://meshtastic.org/docs/configuration/radio/device/).
- Meshtastic, [programma per il computer](https://meshtastic.org/docs/software/python/cli/) e [MQTT](https://meshtastic.org/docs/configuration/module/mqtt/).
- Meshtastic, [primi passi](https://meshtastic.org/docs/getting-started/): mai accendere la radio senza antenna; [dispositivi supportati](https://meshtastic.org/docs/hardware/devices/).
- Heltec Automation, [WiFi LoRa 32 V3](https://wiki.heltec.org/docs/devices/open-source-hardware/esp32-series/lora-32/wifi-lora-32-v3/): misure della scheda e potenza massima.

Script con licenza EUPL 1.2, testi e modello della custodia con licenza CC BY-NC-SA 4.0. Gli altri progetti sono nella pagina [Elettronica per l'emergenza](/elettronica-emergenza/).
