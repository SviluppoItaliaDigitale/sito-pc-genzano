SCHERMO DELL'ALLERTA IN SEDE CON RASPBERRY PI
Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
Istruzioni complete: https://www.protezionecivilegenzano.it/elettronica-emergenza/schermo-allerta/

ATTENZIONE
- Lo schermo informa e basta: non sostituisce il bollettino del Centro
  Funzionale della Regione Lazio, IT-alert ne' il 112.
- Se non riesce a leggere il dato lo scrive e tiene l'ultimo dato letto bene,
  con la sua ora. Se l'ultimo controllo del sito ha piu' di 6 ore, lo schermo
  diventa grigio: "Stato dell'allerta da confermare".
- Alimentatore ufficiale del tuo modello di Raspberry Pi. Mai collegamenti
  alla rete a 230 V fatti a mano.

FILE
- schermo_allerta.py    programma (Python 3, solo libreria standard)
- configurazione.ini    indirizzo, intervallo di lettura, ore di validita'
- LICENZA-EUPL-1.2.txt  si scarica dalla pagina del progetto

COME SI USA
1. Prepara la scheda con Raspberry Pi Imager e Raspberry Pi OS con desktop.
2. Copia i due file in una cartella, per esempio /home/pi/schermo-allerta
   (usa il tuo nome utente al posto di pi).
3. Se manca tkinter:  sudo apt install python3-tk
4. Prova senza schermo:
     python3 schermo_allerta.py --una-volta
   Prova in finestra:
     python3 schermo_allerta.py --finestra
   A tutto schermo (Esc per uscire):
     python3 schermo_allerta.py
5. Disattiva lo spegnimento automatico dello schermo (screen blanking)
   nella configurazione di Raspberry Pi OS.
6. Per farlo partire all'accensione serve l'avvio automatico dei programmi
   del desktop: il metodo cambia con la versione di Raspberry Pi OS.

DATI
Il programma legge https://www.protezionecivilegenzano.it/allerta-stato/index.json,
lo stato dell'allerta pubblicato dal Gruppo con licenza CC BY 4.0 (dati aperti).
Non invia nulla e non raccoglie dati personali.

LICENZE
Codice: EUPL 1.2. Testi: CC BY-NC-SA 4.0.
