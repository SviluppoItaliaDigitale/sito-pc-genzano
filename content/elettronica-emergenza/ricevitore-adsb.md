---
title: "Ricevitore di aerei ed elicotteri ADS-B con Raspberry Pi"
description: "Un Raspberry Pi con una chiavetta RTL-SDR riceve i segnali ADS-B a 1090 MHz e mostra su una mappa il traffico aereo vicino alla sede."
date: 2026-11-24
dataUltimaRevisione: "2026-11-24"
image: ""
tts: true
---

Molti aerei ed elicotteri trasmettono da soli la loro posizione, la quota, la velocità e il codice che li identifica. È il sistema ADS-B (Automatic Dependent Surveillance – Broadcast, cioè «sorveglianza dipendente automatica trasmessa a tutti»), che in Europa usa la frequenza di 1090 MHz. Con un Raspberry Pi e una chiavetta RTL-SDR, un piccolo ricevitore radio da collegare alla porta USB, puoi ricevere questi segnali e vedere il traffico su una mappa nel browser della sede.

Serve per esempio a vedere se nella zona vola l'elisoccorso, o quale traffico c'è vicino prima di far volare un drone. Il ricevitore **ascolta e basta**: non trasmette nulla.

## Limiti e avvertenze

- **Non tutti trasmettono l'ADS-B.** Il regolamento europeo lo rende obbligatorio solo per gli aerei ad ala fissa con massa massima al decollo oltre 5.700 kg o velocità di crociera oltre 250 nodi. Elicotteri, aerei leggeri e altri velivoli possono non comparire sulla mappa: se non vedi un elicottero, **non vuol dire che non c'è**.
- Prima di far volare un drone valgono le regole dell'Ente Nazionale per l'Aviazione Civile (ENAC) e le zone del portale [D-Flight](https://www.d-flight.it/new_portal/). Il ricevitore è un aiuto in più, non le sostituisce.
- La mappa mostra un'**anomalia da verificare**, mai un allarme. Per un'emergenza chiama il **112**.
- Non pubblicare sui social le posizioni dell'elisoccorso o di altri mezzi di soccorso durante un intervento.
- Usa la chiavetta **solo per i segnali ADS-B**. Non usarla per ascoltare comunicazioni riservate.
- **Mai collegamenti alla rete a 230 V** fatti da te: usa l'alimentatore ufficiale del Raspberry Pi. Un'antenna sul tetto va montata in sicurezza e collegata a terra da chi sa farlo.
- La mappa funziona nella rete della sede. Non aprirla su internet dal router.

## Che cosa dice la legge sulla ricezione

Il Codice delle comunicazioni elettroniche (decreto legislativo 1° agosto 2003, n. 259, nel testo in vigore) dice all'articolo 105, comma 2, lettera b), che sono di libero uso «gli apparati radioelettrici solo riceventi, anche da satellite, per i quali non sono previste assegnazione di frequenze e protezione». Un ricevitore che non trasmette, come questo, rientra in quella descrizione. Questo non permette di trasmettere né di ascoltare e diffondere comunicazioni riservate. Per un uso diverso da quello descritto qui, chiedi a chi conosce la normativa radio, per esempio a una sezione dei radioamatori.

## Componenti

| Quantità | Componente | Note |
|---|---|---|
| 1 | Raspberry Pi con Raspberry Pi OS | per esempio Raspberry Pi 4; usalo solo per il ricevitore |
| 1 | Scheda microSD | per il sistema operativo |
| 1 | Alimentatore ufficiale del Raspberry Pi | |
| 1 | Chiavetta RTL-SDR | per esempio RTL-SDR Blog V4, che chiede un driver aggiornato (vedi sotto) |
| 1 | Antenna per 1090 MHz | comprata, oppure uno stilo a quarto d'onda costruito come più sotto |
| 1 | Prolunga USB | per portare la chiavetta vicino all'antenna e accorciare il cavo d'antenna |
| 1 | Filtro con amplificatore per 1090 MHz | facoltativo, riduce i disturbi |
| 1 | Custodia per Raspberry Pi | quella ufficiale va bene, con il Raspberry Pi al chiuso |

## Collegamenti

| Da | A |
|---|---|
| Antenna | ingresso d'antenna della chiavetta, con un cavo il più corto possibile |
| Chiavetta RTL-SDR | porta USB del Raspberry Pi, anche con la prolunga |
| Filtro con amplificatore, se c'è | fra antenna e chiavetta, vicino all'antenna |
| Rete | cavo di rete o Wi-Fi della sede |
| Alimentatore ufficiale | ingresso di alimentazione del Raspberry Pi, per ultimo |

La chiavetta RTL-SDR Blog V4 può alimentare il filtro dal suo connettore d'antenna, fino a 180 mA a 4,5 V, se attivi questa funzione con il comando `rtl_biast -b 1` del suo driver. Il produttore avverte di non attivarla con un'antenna che chiude in corto il connettore: usala solo con un amplificatore o un'antenna attiva.

## L'antenna a quarto d'onda

Per 1090 MHz basta uno stilo verticale lungo un quarto della lunghezza d'onda, con quattro radiali della stessa lunghezza che fanno da piano di terra, montati su un connettore da pannello.

Il calcolo:

- velocità della luce: c = 299.792.458 m/s;
- lunghezza d'onda: c ÷ f = 299.792.458 ÷ 1.090.000.000 = 0,275 m, cioè circa 27,5 cm;
- quarto d'onda: 0,275 m ÷ 4 = 68,8 mm.

Lo stilo e i radiali sono fili nell'aria: il fattore di velocità serve solo per i tratti di cavo coassiale, quindi qui non si usa. Taglia lo stilo qualche millimetro più lungo, poi accorcialo un poco per volta e guarda nella mappa se ricevi più aerei. Metti l'antenna in alto, con la vista più libera possibile verso l'orizzonte.

## Montaggio

1. **Sistema.** Prepara la scheda microSD con il programma ufficiale [Raspberry Pi Imager](https://www.raspberrypi.com/software/) e Raspberry Pi OS. Nelle impostazioni di Imager scegli nome utente, password e rete.
2. **Driver della V4.** Se usi la chiavetta RTL-SDR Blog V4, installa prima il driver aggiornato con le istruzioni del produttore ([pagina della V4](https://www.rtl-sdr.com/V4/), metodo per i pacchetti Debian). L'autore di readsb avverte che senza questo driver la V4 non riceve.
3. **Programmi.** Collega la chiavetta e lancia `bash installa-ricevitore.sh`. Lo script scarica dalla fonte ufficiale lo script di installazione di readsb, che decodifica i segnali, e di tar1090, che li mostra su una mappa. Prima di eseguirlo ti mostra l'impronta e gli indirizzi internet che contiene, e chiede conferma. Con `--solo-scarica` lo salva senza installarlo, così puoi leggerlo prima.
4. **Posizione.** Lo script chiede latitudine e longitudine della sede, facoltative: servono alla mappa per calcolare le distanze. Puoi impostarle anche dopo con `sudo readsb-set-location LATITUDINE LONGITUDINE`.
5. **Riavvio.** Se è il primo programma per SDR sul Raspberry Pi, riavvia con `sudo reboot`.
6. **Controllo.** Da un computer della stessa rete apri `http://INDIRIZZO-DEL-RASPBERRY/tar1090`. Se la pagina non si apre, l'autore consiglia `sudo apt install -y lighttpd` e di rilanciare l'installazione. Il registro del programma si legge con `sudo journalctl --no-pager -u readsb`.

Lo script di installazione di readsb, nella versione letta il 24 novembre 2026, non configura l'invio dei dati a servizi esterni e non imposta aggiornamenti automatici. Toglie invece altri decodificatori già installati, perché la chiavetta la può usare un solo programma: per questo conviene un Raspberry Pi dedicato. Gli aggiornamenti si fanno a mano, rilanciando lo stesso script dopo averlo letto.

Esistono programmi per condividere i dati con siti come OpenSky Network o Flightradar24. Non installarli se non l'avete deciso insieme, con chi è responsabile della rete e dei dati della sede.

## I programmi usati

| Programma | Che cosa fa | Autore | Licenza |
|---|---|---|---|
| [readsb](https://github.com/wiedehopf/readsb) | riceve e decodifica i segnali ADS-B dalla chiavetta | wiedehopf (Matthias Wirth) | GPL, versione 3 o successive |
| [tar1090](https://github.com/wiedehopf/tar1090) | mostra gli aerei su una mappa nel browser | wiedehopf (Matthias Wirth) | GPL, versione 2 o successive |
| [adsb-scripts](https://github.com/wiedehopf/adsb-scripts) | script di installazione di readsb e tar1090 | wiedehopf | MIT |

Questi programmi non sono copiati nel nostro sito: lo script li scarica ogni volta dai loro repository.

## File da scaricare

- [installa-ricevitore.sh](/elettronica-emergenza/ricevitore-adsb/installa-ricevitore.sh), lo script che scarica e lancia l'installazione ufficiale.
- [README.txt](/elettronica-emergenza/ricevitore-adsb/README.txt), le istruzioni brevi.
- [Testo della licenza EUPL 1.2](/elettronica-emergenza/LICENZA-EUPL-1.2.txt).

Prova del 24 novembre 2026: lo script ha scaricato dalla fonte ufficiale lo script di installazione e ne ha mostrato impronta e indirizzi. Non è stato provato su un Raspberry Pi vero con una chiavetta collegata.

## Fonti

Verificate il 24 novembre 2026.

- Codice delle comunicazioni elettroniche, d.lgs. 259/2003, [articolo 105, «Libero uso»](https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2003-08-01;259~art105!vig=), testo in vigore su Normattiva.
- Regolamento di esecuzione (UE) n. 1207/2011, [definizione dell'ADS-B e aerei obbligati](https://eur-lex.europa.eu/legal-content/IT/TXT/HTML/?uri=CELEX:32011R1207).
- Agenzia dell'Unione europea per la sicurezza aerea (EASA), [CS-ACNS, ADS-B a 1090 MHz Extended Squitter](https://www.easa.europa.eu/en/document-library/easy-access-rules/online-publications/easy-access-rules-airborne-communications?page=31).
- NIST, [velocità della luce nel vuoto](https://physics.nist.gov/cgi-bin/cuu/Value?c), valore esatto.
- wiedehopf, [installazione automatica di readsb](https://github.com/wiedehopf/adsb-scripts/wiki/Automatic-installation-for-readsb), [readsb](https://github.com/wiedehopf/readsb) e [tar1090](https://github.com/wiedehopf/tar1090).
- RTL-SDR Blog, [chiavetta V4: driver e alimentazione dell'antenna](https://www.rtl-sdr.com/V4/).
- Raspberry Pi, [installare il sistema operativo](https://www.raspberrypi.com/documentation/computers/getting-started.html).
- D-Flight, [portale per i droni](https://www.d-flight.it/new_portal/).

Codice con licenza EUPL 1.2, testi con licenza CC BY-NC-SA 4.0. I programmi di terzi restano con le loro licenze. Gli altri progetti sono nella pagina [Elettronica per l'emergenza](/elettronica-emergenza/).
