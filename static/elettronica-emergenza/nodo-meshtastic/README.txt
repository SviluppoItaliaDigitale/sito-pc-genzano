NODO MESHTASTIC PER LA SQUADRA
Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
Istruzioni complete: https://www.protezionecivilegenzano.it/elettronica-emergenza/nodo-meshtastic/

ATTENZIONE
- Meshtastic e' un aiuto in piu': non sostituisce le radio del Gruppo, i
  canali della sala operativa ne' il 112.
- I messaggi possono arrivare in ritardo o non arrivare: mai comunicazioni da
  cui dipende la sicurezza di qualcuno.
- Mai accendere la radio senza antenna: il chip radio si puo' danneggiare.
- Banda 869,4-869,65 MHz: al massimo 500 mW e.r.p. (27 dBm) e trasmissione per
  il 10% del tempo (raccomandazione CEPT ERC 70-03, banda h1.7). Non attivare
  mai override_duty_cycle.
- Nomi dei nodi: sigle di servizio, mai nome e cognome.

FILE
- configura-primo-nodo.sh   configura il primo nodo e crea il canale SQUADRA
- unisci-nodo.sh            configura gli altri nodi con il QR del primo
- custodia-nodo-meshtastic.scad             modello della custodia (OpenSCAD)
- custodia-nodo-meshtastic-scatola.stl      scatola (ASA o PETG)
- custodia-nodo-meshtastic-coperchio.stl    coperchio con foro SMA
- custodia-nodo-meshtastic-guarnizione.stl  guarnizione (TPU)
- LICENZA-EUPL-1.2.txt   si scarica dalla pagina del progetto

COME SI USA
1. Carica il firmware Meshtastic con il programma ufficiale:
   https://flasher.meshtastic.org/
2. Installa il programma per il computer:
     pip3 install --upgrade "meshtastic[cli]"
3. Antenna avvitata, radio collegata via USB. Primo nodo:
     bash configura-primo-nodo.sh "PC Genzano 01" PC01
4. Lo script mostra il QR dei canali: fallo inquadrare di persona agli altri
   volontari con l'app, oppure leggi l'indirizzo e usalo per gli altri nodi:
     bash unisci-nodo.sh "PC Genzano 02" PC02
   Lo script chiede l'indirizzo senza mostrarlo e non lo salva.
5. Prova un messaggio sul canale SQUADRA e una prova di portata dai punti
   dove operate.

Il QR e l'indirizzo contengono la chiave del canale: non fotografarli, non
mandarli in chat o per email. Se finiscono dove non devono, crea una chiave
nuova (configura-primo-nodo.sh) e ricondividila.

LICENZE
Script: EUPL 1.2. Testi e modello della custodia: CC BY-NC-SA 4.0.
Il programma meshtastic si usa cosi' com'e', con la sua licenza (GPL 3.0).
