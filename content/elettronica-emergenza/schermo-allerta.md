---
title: "Schermo dell'allerta in sede con Raspberry Pi"
description: "Un Raspberry Pi collegato a uno schermo mostra in sede il livello di allerta meteo pubblicato dal sito, con titolo, descrizione e ora dell'ultimo controllo."
date: 2026-11-24
dataUltimaRevisione: "2026-11-24"
image: ""
tts: true
---

Uno schermo in sede, sempre acceso, mostra a tutto schermo lo stato dell'allerta meteo per Genzano di Roma: livello, titolo, descrizione e ora dell'ultimo controllo. Il colore dello sfondo segue il livello, e il livello è sempre scritto anche a parole. Il programma legge ogni 5 minuti lo stato pubblico dell'allerta che il sito ricava dai bollettini ufficiali, lo stesso che alimenta la barra dell'allerta della [homepage](/).

## Limiti e avvertenze

- Lo schermo **informa e basta**. Non sostituisce il bollettino del Centro Funzionale della Regione Lazio, IT-alert né il **112**. Per le decisioni fanno fede le [allerte meteo](/allerte-meteo/) ufficiali.
- Se la lettura non riesce, lo schermo lo scrive e **tiene l'ultimo dato letto bene**, con la sua ora: un errore di rete non cambia mai il livello mostrato.
- Se l'ultimo controllo del sito ha più di 6 ore, lo schermo diventa grigio e scrive «Stato dell'allerta da confermare», con il rimando al bollettino ufficiale. È la stessa regola della barra in homepage.
- **Mai collegamenti alla rete a 230 V** fatti da te: usa l'alimentatore ufficiale del tuo modello di Raspberry Pi.

## Componenti

| Quantità | Componente | Note |
|---|---|---|
| 1 | Raspberry Pi con uscita video e rete | per esempio Raspberry Pi 4 o 5 |
| 1 | Scheda microSD | per il sistema operativo |
| 1 | Alimentatore ufficiale del modello di Raspberry Pi | |
| 1 | Schermo o televisore con ingresso HDMI | |
| 1 | Cavo HDMI adatto al Raspberry Pi | |
| 1 | Custodia per Raspberry Pi | quella ufficiale va bene: lo schermo sta al chiuso |
| 1 | Tastiera USB | solo per la prima configurazione |

## Collegamenti

| Da | A |
|---|---|
| Uscita HDMI del Raspberry Pi | ingresso HDMI dello schermo |
| Rete | cavo di rete o Wi-Fi della sede |
| Alimentatore ufficiale | ingresso di alimentazione del Raspberry Pi, per ultimo |

## Preparazione

1. **Sistema.** Prepara la scheda microSD con il programma ufficiale [Raspberry Pi Imager](https://www.raspberrypi.com/software/) e Raspberry Pi OS con desktop. Nelle impostazioni di Imager scegli nome utente, password e rete Wi-Fi.
2. **Programma.** Copia `schermo_allerta.py` e `configurazione.ini` in una cartella, per esempio `schermo-allerta` nella tua cartella personale.
3. **Prova senza schermo.** Apri il terminale nella cartella ed esegui `python3 schermo_allerta.py --una-volta`: deve scrivere livello, titolo e ora del controllo.
4. **Prova in finestra.** Esegui `python3 schermo_allerta.py --finestra`. Se manca il modulo grafico tkinter, installalo con `sudo apt install python3-tk`.
5. **Tutto schermo.** Esegui `python3 schermo_allerta.py`. Per uscire premi Esc.
6. **Schermo sempre acceso.** Disattiva lo spegnimento automatico dello schermo, come spiega la [documentazione di Raspberry Pi OS sullo screen blanking](https://www.raspberrypi.com/documentation/computers/configuration.html#screen-blanking).
7. **Avvio all'accensione.** Per far partire il programma da solo serve l'avvio automatico dei programmi del desktop. Il metodo cambia con la versione di Raspberry Pi OS: se non lo conosci, chiedi a chi gestisce i computer della sede.

Il programma usa solo la libreria standard di Python 3. Non invia nulla e non raccoglie dati personali: legge soltanto l'indirizzo pubblico dello stato dell'allerta.

## Che cosa legge

Il programma legge [allerta-stato/index.json](/allerta-stato/index.json), lo stato dell'allerta in formato aperto pubblicato dal Gruppo con licenza CC BY 4.0. Prende livello (`verde`, `gialla`, `arancione`, `rossa`), titolo, descrizione, ora dell'ultimo controllo e, quando ci sono, la previsione per il giorno dopo e l'eventuale emergenza in corso. Il giorno dopo è scritto con la data, per esempio «Previsto per mercoledì 25 novembre». I dati aperti del sito sono elencati nella pagina [Open data](/open-data/).

In `configurazione.ini` puoi cambiare l'intervallo di lettura, non sotto i 5 minuti, e le ore oltre le quali lo stato diventa da confermare.

## File da scaricare

- [schermo_allerta.py](/elettronica-emergenza/schermo-allerta/schermo_allerta.py), il programma.
- [configurazione.ini](/elettronica-emergenza/schermo-allerta/configurazione.ini), le impostazioni. Non contiene password.
- [README.txt](/elettronica-emergenza/schermo-allerta/README.txt), le istruzioni brevi.
- [Testo della licenza EUPL 1.2](/elettronica-emergenza/LICENZA-EUPL-1.2.txt).

Prova del 24 novembre 2026: il programma ha letto lo stato pubblicato dal sito. Con file di prova della stessa forma ha mostrato un'allerta arancione con la previsione del giorno dopo e lo stato grigio dopo 6 ore. Un file danneggiato e un indirizzo inesistente non hanno cambiato il dato già letto.

## Fonti

Verificate il 24 novembre 2026.

- Raspberry Pi, [installare il sistema operativo con Raspberry Pi Imager](https://www.raspberrypi.com/documentation/computers/getting-started.html) e [spegnimento automatico dello schermo](https://www.raspberrypi.com/documentation/computers/configuration.html#screen-blanking).
- Python, [tkinter](https://docs.python.org/3/library/tkinter.html), la libreria grafica usata dal programma.

Codice con licenza EUPL 1.2, testi con licenza CC BY-NC-SA 4.0. Gli altri progetti sono nella pagina [Elettronica per l'emergenza](/elettronica-emergenza/).
