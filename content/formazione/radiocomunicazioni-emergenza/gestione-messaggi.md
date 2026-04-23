---
title: "Capitolo 4 — Gestione dei messaggi e controllo di maglia"
description: "Net Control Station, Net Manager, maglie dirette e libere, precedenze, formato del messaggio radioamatoriale (intestazione, testo, firma), collegamento con l'Incident Command System (ICS) e il Metodo Augustus."
---

Una volta padroneggiate le tecniche di base (Cap. 2) e conosciuti i canali (Cap. 3), il volontario TLC entra nel cuore del suo mestiere: **far funzionare una maglia** in cui molti operatori passano molti messaggi, tutti con tempi e priorità diverse, senza caos. La disciplina di maglia è ciò che distingue un gruppo pronto da un coro stonato.

Questo capitolo riprende i contenuti dei capitoli 7-13 della Guida IARU, centrati sul **Net Control Station** (NCS), il **Net Manager** (NM) e il **formato dei messaggi**.

## Maglia diretta vs maglia libera

### Maglia diretta ("directed net")

Una **maglia diretta** è controllata da un Net Control. **Nessuno trasmette senza l'autorizzazione del NCS**, salvo che per emergenze vitali. Le caratteristiche:

- **disciplinata**: ogni trasmissione ha il permesso
- **ordinata**: un messaggio alla volta, per priorità
- **controllata**: il NCS tiene il log, assegna le stazioni

Si usa nelle **emergenze serie** e negli **eventi con molto traffico**. È il modo standard in protezione civile italiana.

### Maglia libera ("open net" o "ragchew")

Le stazioni trasmettono **quando vogliono**, nel rispetto reciproco. Adatta a:

- **reti quotidiane** di routine
- **drill di prova** in momenti tranquilli
- **chiacchierate** di formazione continua

In emergenza vera, la maglia libera **non funziona**: si sovrappongono troppe stazioni.

### Transizione da libera a diretta

All'**innesco** di un'emergenza, una maglia libera diventa una maglia diretta. Chi apre la maglia (in genere il primo ad accorgersi, o un operatore pre-designato) dichiara:

*"Questa è la Maglia di Emergenza di Genzano, diretta, dal nominativo IØXYZ Net Control. Chiedo silenzio radio salvo traffico di emergenza o priorità. Stazioni con traffico di emergenza, chiamate ora."*

## Il Net Control Station (NCS)

Il **NCS** è l'operatore che controlla la maglia. Le sue responsabilità:

1. **Aprire** la maglia con uno script standard
2. **Ricevere check-in** delle stazioni che entrano
3. **Autorizzare** le trasmissioni in base alle precedenze
4. **Facilitare** il passaggio dei messaggi fra due stazioni
5. **Tenere il log** di maglia
6. **Chiudere** la maglia con uno script standard

### Dove opera il NCS

Può operare:

- dal **COC** (buono: sente il responsabile della funzione, ma ambiente rumoroso)
- da una **postazione esterna** tranquilla (buono: concentrazione, ma scollegato dal COC)
- dalla propria **casa** se fuori dall'area di impatto (buono: stazione attrezzata, ma distante)

Dipende dalla scala dell'evento e dalla disponibilità.

### Non è il capo di tutto

Il NCS controlla **una maglia**, non l'intera operazione TLC. Il controllo di alto livello appartiene al **Net Manager** (o al Responsabile della Funzione TLC nel COC). Non puoi fare il NCS e il comandante della risposta: ognuno dei due ruoli richiede 100 % di attenzione.

### Script di apertura e chiusura

Usare uno **script** garantisce che:

- la maglia suoni **coerente** ogni volta
- i listener capiscano **scopo e formato** della maglia
- chiunque possa assumere il ruolo di NCS senza inventarsi le parole

Esempio di apertura:

> *"Questa è [nominativo], Net Control Station per la Maglia di Emergenza del Gruppo Comunale di Protezione Civile di Genzano di Roma. Questa è una maglia diretta di emergenza. Chiedo di trasmettere solo se autorizzati, salvo traffico di emergenza.*
>
> *Stazioni con traffico di emergenza, chiamate ora.*
> *[si attende. Se emergenza → si gestisce.]*
>
> *Stazioni con traffico di priorità, chiamate ora.*
> *[si attende.]*
>
> *Altre stazioni con o senza traffico, chiamate ora."*

Esempio di chiusura:

> *"Grazie a tutte le stazioni che hanno partecipato. Questa è [nominativo], chiudo la Maglia di Emergenza di Genzano alle [ora] del [data]. Frequenza restituita all'uso normale."*

### NCS di backup

Per ogni NCS deve esserci un **backup** pronto a subentrare:

- guasto dell'apparato primario
- necessità di pausa
- passaggio di turno a metà evento

Il backup può operare in **hot standby** (in ascolto sulla stessa frequenza, pronto a intervenire) o in **cold standby** (pronto al richiamo).

## Il Net Manager (NM)

Il **Net Manager** coordina l'insieme delle maglie e la gestione dei turni. Le sue responsabilità:

- assegnare i **NCS titolari e backup** per ogni sessione
- reclutare **liaison stations** tra maglie diverse
- scegliere le **frequenze** operative
- curare la **formazione** dei NCS
- fare il **debriefing** post-evento

Nel Gruppo Comunale di Genzano, il ruolo di Net Manager coincide con il **responsabile della funzione TLC** del COC.

## Le precedenze del traffico

La Guida IARU riprende lo schema internazionale delle precedenze, spesso marcato all'inizio di ogni messaggio:

| Precedenza | Pro-word | Quando usarla |
|---|---|---|
| **Emergenza** (EMERGENCY) | Emergenza | Vita umana in pericolo immediato, richiesta di intervento salvavita |
| **Priorità** (PRIORITY) | Priorità | Richieste urgenti dalle autorità, segnalazioni che richiedono azione rapida |
| **Salute e Benessere** (WELFARE) | Welfare | Informazioni sui dispersi, ricongiungimento familiare |
| **Routine** (ROUTINE) | Routine | Messaggi ordinari non urgenti |

In Italia non c'è un allineamento formale uno-a-uno, ma l'uso dei tre livelli **Emergenza / Priorità / Routine** è consolidato.

### Come si chiama una stazione con traffico

Il formato corretto di chiamata da una stazione tattica al NCS:

- *"Net, Aid 3"* — chiamata generica (senza traffico urgente)
- *"Aid 3, emergenza"* — ho un messaggio emergency, sento di interrompere
- *"Aid 3, priorità per COC Genzano"* — ho un priority per una specifica stazione
- *"Aid 3, routine per Logistica"* — messaggio ordinario, aspetto il mio turno

Il NCS risponde riordinando per priorità: prima emergenze, poi priorità, poi routine.

## Formato del messaggio radioamatoriale

Un **messaggio formale** ha una struttura standard in quattro parti: **intestazione (preamble)**, **indirizzamento**, **testo**, **firma**. Questa struttura è una delle grandi tradizioni dell'handling traffic radioamatoriale (ARRL Radiogram, IARU format).

### 1. Preambolo (preamble)

Informazioni di controllo del messaggio:

- **numero** progressivo del messaggio
- **precedenza** (Emergenza, Priorità, Welfare, Routine)
- **nominativo stazione** originante
- **numero di parole** (*check*)
- **stazione di origine** (città/luogo)
- **data e ora** di originazione (UTC)

### 2. Indirizzamento (address)

A chi va consegnato:

- **Nome** e **qualifica** (es.: Sindaco, Prefetto, Mario Rossi, COC Genzano)
- **Indirizzo** fisico o logistico
- **Telefono** se disponibile

### 3. Testo (text)

Il contenuto vero e proprio. Regole:

- **chiaro**, breve, in linguaggio piano
- un argomento per messaggio
- **niente contrazioni**, codici o slang
- il **numero di parole** va contato per verifica ("check")

### 4. Firma (signature)

Chi **origina** il messaggio (cioè l'autore, non il trasmettitore):

- nome
- qualifica / ruolo
- eventuale contatto per risposta

### Esempio di messaggio formale

```
NUMERO 47 — PRIORITÀ — IØABC
CHECK 22
DA: IØABC — GENZANO DI ROMA — 20 APR 2026 — 10:45 UTC

A:
Sindaco Flavio Gabbarini
Comune di Genzano di Roma
Piazza Tommaso Frasconi 3
06 93 711 1 (centralino)

TESTO:
Richiesta autorizzazione sosta prolungata presso piazzale scuola
Belardi per allestimento punto informazioni volontari. Area libera
fino a ore 18.00. Fine messaggio.

FIRMA:
Ing. Laura Bianchi
Coordinatore Gruppo Comunale PC Genzano
345 123 4567
```

### Pro-words durante la trasmissione del messaggio

Mentre trasmetti un messaggio formale si usano pro-word specifici:

- **"Fine messaggio"** — termine del testo prima della firma
- **"Correggo"** — parola errata precedente, segue correzione
- **"Ripeto"** — la parola che segue è ripetuta per chiarezza (usare con parsimonia)
- **"Vi compito"** / **"Spelling"** — sto per compitare
- **"Passo"** — ho finito la mia trasmissione, aspetto conferma

## Il log di maglia

Il **log** è il registro di tutto ciò che passa sulla maglia. Deve contenere:

- ora di apertura e chiusura
- **check-in / check-out** delle stazioni
- **messaggi** passati (numero, precedenza, da, per, oggetto)
- **eventi rilevanti** (guasti, cambio NCS, emergenze)
- **note operative**

Il log si conserva perché:

- serve al **debriefing**
- può essere richiesto da **autorità** per ricostruire gli eventi
- è la **traccia storica** dell'operazione

Esistono formati cartacei (vedi [Capitolo 6 del Manuale da Campo — Registro di Stazione](/formazione/manuale-campo/moduli-radio/)) e digitali. In esercitazioni recenti nel Lazio si usano **tablet condivisi** con log in cloud quando la connettività lo consente.

## Integrazione con la struttura di comando

### Il Metodo Augustus (Italia)

In Italia, la **funzione TLC** è una delle **funzioni di supporto** del COC secondo il **Metodo Augustus** (DPC, 1997; aggiornato nei piani comunali moderni). La funzione è presidiata da:

- un **Responsabile di Funzione** nominato dal Sindaco
- uno o più **operatori**

Il Responsabile TLC:

- mantiene il contatto con la **Sala Operativa Regionale**
- attiva e coordina la **maglia radio** del Gruppo
- garantisce la **ridondanza** con i canali istituzionali
- segnala al Sindaco **anomalie** sui canali
- partecipa al **briefing** di aggiornamento al Sindaco

### ICS — Incident Command System (riferimento internazionale)

Il sistema americano ICS — e la sua versione semplificata per gli USA, **NIMS** — prevede cinque funzioni:

1. **Command** — decisione
2. **Operations** — esecuzione
3. **Planning** — analisi e scenari
4. **Logistics** — risorse materiali
5. **Finance/Administration** — contabilità

La funzione TLC è **trasversale**: serve tutte e cinque. In scenari di grande entità, l'ICS italianizzato è stato adottato in alcune esercitazioni della Colonna Mobile Nazionale.

Per il volontario a Genzano il punto fermo è: **sei parte della funzione TLC del COC**, e riferisci al Responsabile di funzione, che riferisce al **Sindaco** come autorità comunale di protezione civile (art. 12 D.Lgs. 1/2018).

## Handling traffic — procedura standard per un messaggio

Passaggio tipo di un messaggio dalla sorgente al destinatario in maglia:

**1. Origine del messaggio**
Qualcuno al punto A scrive un messaggio. Lo consegna all'operatore radio del punto A.

**2. Contatto con Net Control**
*"Net, Punto A con un messaggio priorità per COC."*

**3. Autorizzazione Net Control**
*"Punto A, passate al COC direttamente."*

oppure (se COC è occupato):

*"Punto A, attendete, COC occupato."*

**4. Chiamata al destinatario**
*"COC, Punto A con messaggio priorità numero 12."*

**5. Conferma del destinatario**
*"Punto A, COC pronto a ricevere."*

**6. Trasmissione del messaggio**

*"Messaggio numero 12 priorità da Punto A — check 22 — da IØABC — Genzano — 20 aprile 2026 — 10 e 45 UTC.*

*A: Sindaco, Comune di Genzano, piazza Tommaso Frasconi 3, zero sei nove tre sette uno uno.*

*Testo: Richiesta autorizzazione sosta prolungata presso piazzale scuola Belardi per allestimento punto informazioni volontari. Area libera fino a ore 18 — spelling diciotto. Fine messaggio.*

*Firma: ing. Laura Bianchi, coordinatore, tre quattro cinque uno due tre quattro cinque sei sette."*

**7. Verifica ricezione**
*"Punto A, COC ha ricevuto messaggio 12, attendo conferma check e passo alla consegna."*

**8. Consegna al destinatario finale**
L'operatore radio al COC trascrive il messaggio e lo consegna (cartaceo o digitale) al Sindaco o alla funzione competente.

**9. Ricevuta di ritorno**
Se il messaggio richiede ricevuta, si formula una "Reply/Ricevuta" seguendo lo stesso protocollo.

## Liaison fra maglie diverse

In scenari estesi possono essere attive **più maglie** (es.: una maglia comunale VHF + una provinciale HF + una logistica UHF). Ogni maglia ha uno o più **operatori di collegamento** (liaison) che ascoltano entrambe e trasferiscono i messaggi rilevanti.

Il Net Manager assegna le liaison: di solito operatori esperti con buoni apparati e buone antenne.

## Debriefing

Poco dopo il termine delle operazioni, il gruppo TLC conduce un **debriefing** con l'ente servito. Punti da valutare:

- **maglie** — hanno tenuto? dove hanno fallito?
- **copertura** — zone morte, rientri in ripetitori non funzionanti
- **disciplina di maglia** — sovrapposizioni, operatori "chiacchieroni"
- **handling traffic** — precedenze rispettate? errori di consegna?
- **personale** — turni troppo lunghi, stress, bisogno di ricambio
- **equipaggiamento** — cosa è mancato, cosa è rotto
- **relazione con l'ente servito** — conflitti, malintesi, buone pratiche

Il debriefing genera un **verbale** che contribuisce all'aggiornamento del Piano Comunale di Protezione Civile e dei protocolli del Gruppo.

## Leggi anche

- [Capitolo 3 — Reti, maglie e canali](/formazione/radiocomunicazioni-emergenza/reti-canali/)
- [Capitolo 5 — Attivazione, equipaggiamento e impianto di stazione](/formazione/radiocomunicazioni-emergenza/attivazione-equipaggiamento/)
- [Manuale da Campo — Capitolo 6 — Moduli e codici radio](/formazione/manuale-campo/moduli-radio/)
- [Manuale da Campo — Capitolo 1 — Struttura organizzativa](/formazione/manuale-campo/struttura-organizzativa/)
