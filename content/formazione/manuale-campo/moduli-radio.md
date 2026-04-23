---
title: "Capitolo 6 — Moduli e codici radio (allegati operativi)"
description: "Modulo messaggio, registro di stazione, alfabeto fonetico NATO e codice Q personalizzati per il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma."
---

Questo capitolo raccoglie i **moduli e le tabelle di riferimento** per la squadra radiocomunicazioni del **Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma**. Sono adattati dagli allegati del manuale *"Comunicazioni Radio in emergenza"* del Sistema di Protezione Civile, con i riferimenti di Genzano (COC, Ufficio Comunale PC, canali Regione Lazio).

Per la parte teorica sulla rete TLC, le bande di frequenza (HF/VHF/UHF), il ponte radio e la catena di comando vedi [Capitolo 3 — Funzioni tecniche](/formazione/manuale-campo/funzioni-tecniche/).

## Allegato 1 — Modulo messaggio

Il modulo messaggio è lo **strumento standard** con cui ogni richiesta o comunicazione viene tracciata in postazione radio. Va compilato **in duplice copia**: una resta in stazione, l'altra accompagna la consegna al destinatario.

### Campi del modulo

| N° | Campo | Chi lo compila |
|---|---|---|
| 1 | Qualifica di precedenza (Ordinario / Urgente) | Mittente |
| 2 | Classifica di segretezza (Non classificato / Riservato / Segreto) | Mittente |
| 4 | Data generazione messaggio | Mittente |
| 5 | Ora generazione messaggio | Mittente |
| 6 | Da (mittente — persona, funzione o ente) | Mittente |
| 7 | A (destinatario/i) | Mittente |
| 8 | Per conoscenza (eventuali) | Mittente |
| 10 | Testo del messaggio | Mittente |
| 11 | Firmato (nome e funzione) | Mittente |
| 12 | Visto ed autorizza MESSAGGIO | Responsabile / Capo Campo |
| 21 | Qualifica di trasmissione (PA / P / U / O) | Chi autorizza |
| 22 | Spazio riservato al COC o alla stazione radio | Operatore |
| 23 | Ora ricezione / Ora trasmissione / Sistema (fonia / fax / ecc.) | Operatore |
| 24 | Firma ENTE a cui si consegna | Destinatario |
| 25 | MHz (frequenza o canale) | Operatore |
| 26 | Operatore (nome e cognome) | Operatore |
| 27 | Note | Operatore |
| 28 | N° progressivo (pari al Registro di stazione) | Operatore |

### Indicatori di qualità del segnale

Durante ricezione e trasmissione l'operatore annota:

- **QRM** — disturbi elettromagnetici generici
- **QRN** — disturbi da interferenze (atmosferiche o industriali)
- **Santiago (S)** — forza del segnale in scala 1–9
- **Radio (R)** — comprensibilità della modulazione in scala 1–5

## Allegato 2 — Note per la compilazione del modulo messaggio

### Qualifica di precedenza (campo 1)

Stabilita da chi genera il messaggio. Definisce i **tempi massimi di trattazione**:

| Qualifica | Tempo massimo di trattazione |
|---|---|
| **Urgente** | Non definito. Solo il tempo tecnico di recapito, dando precedenza ai messaggi PA e P |
| **Ordinario** | Entro 30 minuti, dopo aver assolto le precedenze superiori. Se ricevuto dopo le 18 e destinato a enti non allertati, consegna al giorno lavorativo successivo |

### Qualifica di trasmissione (campo 21)

Definisce la **priorità di instradamento** attribuita dalla stazione radio:

| Sigla | Criterio |
|---|---|
| **PA** | Messaggio che richiede soccorso e interventi a **salvaguardia della vita umana** o di animali |
| **P** | Messaggio che richiede soccorso e interventi a **salvaguardia di beni materiali**, mobili o immobili |
| **U** | Già definito dal compilatore come Urgente nella qualifica di precedenza |
| **O** | Già definito dal compilatore come Ordinario nella qualifica di precedenza |

**Regola**: i messaggi **PA interrompono** qualunque trasmissione di qualifica inferiore. La qualifica PA si usa **solo** per richieste di soccorso a persone in pericolo di vita: un uso improprio impegna inutilmente risorse e può ritardare emergenze reali.

### Altri campi

- **Campo 2 — Classifica di segretezza**: stabilita dal mittente (normalmente "Non classificato" in emergenza ordinaria).
- **Campo 6 — Da**: indicare sempre mittente e funzione (es. "Capo Campo Genzano — Sig. Rossi").
- **Campo 7 — A**: destinatario/i (es. "Sindaco Genzano", "Sala Operativa Regione Lazio", "Prefettura Roma").
- **Campo 22 — Esempio compilazione**: `COC Genzano — n° 25 — Località Campo Sportivo Via Pedemonte`.
- **Campo 25 — MHz**: annotare frequenza o canale usato (es. canale 13 oppure 430.125 MHz).
- **Campo 26 — Operatore**: nome e cognome dell'operatore radio in servizio.
- **Campo 27 — Note**: osservazioni dell'operatore (condizioni di propagazione, ripetizioni, ecc.).
- **Campo 28 — N° progressivo**: stesso numero con cui il messaggio è registrato nel Registro di stazione.

## Allegato 3 — Registro di stazione

Il registro di stazione è il **giornale di bordo** della postazione radio. Ogni messaggio in arrivo o in partenza va annotato con numero progressivo. Permette di **ricostruire a posteriori** l'intera attività radio del campo.

### Campi del registro

| N° | Campo |
|---|---|
| 1 | Operatore (Cognome e Nome) |
| 2 | N° identificativo del volontario nel Gruppo (se previsto) |
| 3 | Località Centro Trasmissioni (COC Genzano o altra sede) |
| 4 | Località Radio Mobile (se si opera da veicolo) |
| 5 | N° progressivo del messaggio |
| 6 | Da (mittente) |
| 7 | A (destinatario) |
| 8 | Testo sintetico del messaggio |
| 9 | Firmato (nome e funzione di chi ha generato il testo) |

Ogni voce è marcata **Ricevuto** oppure **Trasmesso**, con data e ora.

## Allegato 4 — Note per la compilazione del registro di stazione

1. **Operatore**: cognome e nome dell'operatore radio.
2. **N° identificativo**: codice del volontario nel Gruppo di Genzano (se assegnato in sede di iscrizione).
3. **Centro trasmissioni**: usare questo campo quando si opera in postazione fissa (es. COC di Genzano).
4. **Radio mobile**: usare questo campo quando si opera da veicolo (es. squadra in ricognizione).
5. **N° progressivo**: corrisponde al pari numero del modulo messaggio.
6. **Da**: nome o ente che ha generato il messaggio.
7. **A**: nome o ente destinatario.
8. **Testo**: riportare **sinteticamente** il contenuto del messaggio di pari numero. Per il testo integrale si rimanda al modulo messaggio.
9. **Firmato**: nome e funzione di chi ha generato il testo.

## Allegato 5 — Alfabeto fonetico NATO (spelling)

L'alfabeto fonetico **NATO** è lo standard internazionale per la trasmissione di lettere critiche in fonia (nomi propri, sigle, coordinate). Il Gruppo Comunale di Genzano lo adotta in tutte le comunicazioni radio di servizio.

| Lettera | NATO | Pronuncia | Equivalente italiano |
|---|---|---|---|
| A | **ALFA** | al-fa | Ancona |
| B | **BRAVO** | bra-vo | Bologna |
| C | **CHARLIE** | cià-li / ciar-li | Como |
| D | **DELTA** | del-ta | Domodossola |
| E | **ECHO** | ec-o | Empoli |
| F | **FOXTROT** | fox-strot | Firenze |
| G | **GOLF** | golf | Genova |
| H | **HOTEL** | ho-tel | Hotel |
| I | **INDIA** | in-dia | Imola |
| J | **JULIET** | giù-li-et | Jesolo |
| K | **KILO** | ki-lo | Kursaal |
| L | **LIMA** | li-ma | Livorno |
| M | **MIKE** | ma-ik | Milano |
| N | **NOVEMBER** | no-vem-ber | Napoli |
| O | **OSCAR** | os-car | Otranto |
| P | **PAPA** | pa-pa | Palermo |
| Q | **QUEBEC** | ke-bek | Quarto |
| R | **ROMEO** | ro-mi-o | Roma |
| S | **SIERRA** | si-er-ra | Savona |
| T | **TANGO** | tan-go | Torino |
| U | **UNIFORM** | iu-ni-form | Udine |
| V | **VICTOR** | vic-tar | Venezia |
| W | **WHISKY** | uiss-chi | Washington |
| X | **X-RAY** | ecs-rei | Xantia |
| Y | **YANKEE** | ian-chi | York |
| Z | **ZULU** | zu-lu | Zara |

### Regole operative

- Per trasmettere **cifre** o **segni** (virgola, barra, punto interrogativo, ecc.), premettere o far seguire le parole **"in cifra"** o **"in segno"**.
- Le sillabe accentate sono in grassetto nella tabella.
- Esempio pratico per Genzano:
  - `GENZANO = Golf-Echo-November-Zulu-Alfa-November-Oscar`
  - `VIA PEDEMONTE 25 = Victor-India-Alfa … Papa-Echo-Delta-Echo-Mike-Oscar-November-Tango-Echo … 25 in cifra`

## Allegato 6 — Codice Q

Il **codice Q** è composto da circa 200 codici. Nelle comunicazioni radio di emergenza ne viene usata una ventina, con definizione **univoca in fonia**. Ogni codice, pronunciato come domanda o come affermazione, sostituisce una frase intera e riduce il tempo di trasmissione.

| Codice | Significato |
|---|---|
| **QRA** | Nominativo della stazione |
| **QRB** | Distanza tra le due stazioni |
| **QRG** | La vostra frequenza esatta è: … |
| **QRK** | Comprensibilità della modulazione |
| **QRM** | Sono disturbato (interferenze elettromagnetiche) |
| **QRN** | Sono disturbato da interferenze (atmosferiche) |
| **QRT** | Sospensione della trasmissione |
| **QRX** | Richiamerò alle ore: … |
| **QRZ** | Siete chiamati da: … |
| **QSA** | Forza del segnale |
| **QSL** | Accuso ricevuta della trasmissione |
| **QSO** | Comunicazione diretta |
| **QSP** | Ritrasmissione del messaggio |
| **QSY** | Passaggio ad altra frequenza |
| **QSX** | In ascolto radio |
| **QTC** | Messaggio destinato a: … |
| **QTH** | Posizione o località |
| **QTR** | Ora esatta |
| **QUA** | Trasmissione notizie |

### Esempi pratici a Genzano

- `QRZ?` → "Chi mi chiama?" Risposta: `QRZ Genzano Uno` ("vi chiama la stazione Genzano Uno").
- `QTH?` → "Qual è la vostra posizione?" Risposta: `QTH Piazza IV Novembre`.
- `QRM 5` → "Sono disturbato al livello 5" (massimo disturbo).
- `QSY 430.125` → "Passiamo sulla frequenza 430.125 MHz".
- `QRT` → "Sospendiamo la trasmissione".

## Contatti e canali operativi a Genzano

| Struttura | Riferimento |
|---|---|
| **Centro Operativo Comunale (COC)** | Presso Ufficio Protezione Civile del Comune di Genzano |
| **Canali radio Gruppo Comunale** | Da verificare con il Responsabile radiocomunicazioni prima dell'attivazione |
| **Canali Regione Lazio** | Coordinati dall'Agenzia Regionale di Protezione Civile — vedi portale [regione.lazio.it](https://www.regione.lazio.it/cittadini/protezione-civile) |
| **Sala Operativa Regionale Lazio (SOUR)** | Raggiungibile via ponte radio regionale e in fonia |
| **NUE 112** | Unico numero di emergenza per il cittadino — **non** passa dalla radio di gruppo |

**Avvertenza**: frequenze e canali autorizzati vanno verificati con il **Responsabile del Gruppo** e con l'**Agenzia Regionale di Protezione Civile del Lazio** prima di ogni attivazione. Non trasmettere su canali non autorizzati.

## Formato stampa

Questa pagina è progettata per essere **stampata in bianco e nero** su A4 fronte-retro come riferimento rapido da tenere in postazione radio. Abbinare alla [Scheda 10 — Comunicazione radio](/formazione/manuale-campo/schede-tecniche/#scheda-10--comunicazione-radio-promemoria) del Capitolo 5.

## Fonti

- *Comunicazioni Radio in emergenza* — allegati 1–6 del manuale operativo (2001), pubblicato sul portale Sistema di Protezione Civile ([link al PDF originale](https://www.sistemaprotezionecivile.it/allegati/480_Comunicazioni_Radio_in_emergenza.pdf))
- **Codice Q** — Union Internationale des Télécommunications (UIT)
- **Alfabeto fonetico NATO** — ICAO / NATO 1956, standard internazionale

## Leggi anche

- [Capitolo 3 — Funzioni tecniche (rete TLC)](/formazione/manuale-campo/funzioni-tecniche/)
- [Capitolo 5 — Schede tecniche (promemoria radio)](/formazione/manuale-campo/schede-tecniche/#scheda-10--comunicazione-radio-promemoria)
- [Radiocomunicazioni — area tematica](/comunicazioni/?filter=Radiocomunicazioni)
