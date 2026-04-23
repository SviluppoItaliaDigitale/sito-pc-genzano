---
title: "Capitolo 3 — Reti, maglie e canali"
description: "Network theory: scegliere il canale giusto in base al messaggio. Telefono fisso, cellulare, VHF/UHF, HF, satellite, digitali. Caratteristiche, limiti, scenari d'uso per la protezione civile."
---

Quando hai un messaggio da far passare, non tutti i canali vanno bene. Lo studio di questa scelta si chiama **network theory** — trovare il **percorso di comunicazione più efficiente** in base al contenuto, all'urgenza, alla precisione richiesta, al numero di destinatari, e alle risorse disponibili.

La Guida IARU dedica il capitolo 6 a questa materia. Per il volontario TLC italiano la conclusione pratica è semplice: **conosci i tuoi canali**, sappi cosa possono e cosa non possono fare, e scegli consapevolmente.

## Le cinque dimensioni di un messaggio

Prima di scegliere un canale, classifica il tuo messaggio secondo cinque dimensioni:

### 1. Destinatari — uno o più

- **Uno-a-uno**: messaggio per una singola stazione (es.: "Inviate un'ambulanza al civico 14")
- **Uno-a-molti**: messaggio per più destinatari (es.: "Chiudere tutte le strade comunali fino a nuovo ordine")
- **Broadcast ambientale**: informazione utile anche a chi ascolta di passaggio (es.: "Allerta cessata")

### 2. Precisione — alta o bassa

- **Bassa precisione**: *"Il disperso è stato trovato"* — anche se manca una parola, il senso arriva
- **Alta precisione**: *"Codice fiscale RSSMRA85T10H501Z"* — una lettera sbagliata rovina tutto

La precisione non è la stessa cosa dell'accuratezza: tutti i messaggi devono essere accurati, ma solo alcuni richiedono precisione a livello di carattere.

### 3. Complessità — semplice o articolata

- **Semplice**: *"Acqua finita, servono 100 bottiglie"*
- **Articolato**: istruzioni cliniche per stabilizzare un politraumatizzato, o una lunga lista di medicinali con dosi

I messaggi complessi **devono essere** in forma scritta o digitale, non ripetuti in fonia.

### 4. Tempistica — urgente o differibile

- **Urgentissima**: pericolo di vita
- **Urgente**: azione richiesta a breve
- **Differibile**: può essere trattato quando il canale è libero

### 5. Priorità / capacità di interrompere

Alcuni canali consentono di **interrompere** una conversazione in corso per un messaggio di priorità più alta (QSK). Altri no: se il canale è occupato, il messaggio aspetta.

## Le caratteristiche dei canali

Ora vediamo i canali disponibili in Italia al volontario di protezione civile, ciascuno con i suoi punti di forza e di debolezza.

### Telefono fisso

**Tipo**: uno-a-uno, bassa-media precisione, semplice, non interrompibile.

**Forza**:

- intuitivo, non serve formazione
- funziona con plenty di capacità residua in emergenze locali
- adatto a messaggi riservati (liste di nomi, informazioni sensibili)

**Debolezza**:

- dipende da **cavi e centraline** — un palo abbattuto o una centrale inondata = niente linea
- si **satura** in eventi estesi
- **uno-a-uno**: niente broadcast
- **dial + ring + pickup** = tempi lunghi

**Quando usarlo**: messaggi riservati, informazioni di alta precisione (liste, dosaggi) in scenari locali con rete integra.

### Cellulare / smartphone

**Tipo**: uno-a-uno (anche messaggi, dati, foto, geolocalizzazione), bassa-alta precisione, non interrompibile.

**Forza**:

- **portabilità totale**
- non serve operatore radio dedicato
- app di messaggistica gestiscono **gruppi** (uno-a-molti asincrono)
- **dati** ricchi (foto, posizione GPS, mappe)

**Debolezza**:

- dipende dalla **rete cellulare** — spesso prima infrastruttura a cadere
- in eventi estesi si **satura** fortemente (design pensato per 6-10 % di utenti in simultanea)
- SMS possono avere **ritardi elevati** anche con rete formalmente attiva
- non c'è **fallback** a simplex

**Quando usarlo**: nella **prima fase** di evento, per allertamento dei volontari e coordinamento interno. Con riserva nelle fasi successive.

### Fax

Obsoleto per la vita quotidiana ma ancora utile in contesti istituzionali (Comuni, Prefetture) per messaggi formalmente firmati.

**Forza**: produce documento stampato con firma leggibile — utile per ordinanze, verbali.

**Debolezza**: dipende da linea telefonica. Lento. Qualità scadente se la linea è rumorosa.

**Quando usarlo**: per **firme** e **documenti ufficiali** in scenari con rete integra.

### E-mail

**Tipo**: uno-a-molti, alta precisione, semplice-complessa, tempistiche medie, interrompibile.

**Forza**:

- **allegati** (PDF, foto, mappe)
- traccia scritta storicizzata
- **mailing list** per broadcast interno
- funziona anche su 2G a velocità bassa

**Debolezza**: dipende da Internet. In zone remote senza copertura, niente.

### VHF — 144 MHz (2 metri)

**Tipo**: uno-a-molti in simplex o via ripetitore, bassa-media precisione, interrompibile, portata locale-regionale.

**Forza**:

- **apparati economici** e robusti, dal palmare da pochi watt alla stazione base
- **ripetitori** permettono copertura di decine di km anche in territori collinari come i Castelli Romani
- **self-contained**: nessuna infrastruttura commerciale, funziona se c'è il radioamatore e la radio
- **broadcast** nativo: tutti in ascolto sulla stessa frequenza
- possibilità di **digitale** (D-STAR, C4FM, DMR) per dati

**Debolezza**:

- **portata** limitata alla linea di vista — ostruzioni montuose possono bloccare il segnale in simplex
- i **ripetitori** possono perdere alimentazione se manca rete elettrica prolungata e la batteria tampone si esaurisce
- la qualità audio su palmare 5 W in zona urbana può essere **marginale**

**Quando usarla**: scenario locale (paese, provincia, regione). Il **Lazio** ha ottima copertura VHF tramite ripetitori ARI-RE e radioamatori. A Genzano, il 2 m è la **prima scelta operativa** in simplex sui canali assegnati o tramite ripetitori ufficiali.

### UHF — 430 MHz (70 cm)

**Tipo**: stesse caratteristiche del VHF, ma con **propagazione** diversa.

**Forza**:

- **migliore penetrazione** in edifici (ottimo in COC, centri storici)
- **ripetitori UHF** spesso complementari al VHF
- disponibilità di **link** UHF↔VHF incrociati
- ottimo per **digitale** (DMR con reti tipo BrandMeister)

**Debolezza**:

- **attenuazione** maggiore da vegetazione e pareti
- portata **puramente locale**

**Quando usarla**: comunicazioni ravvicinate o in ambiente urbano. In esercitazioni di Gruppo è spesso la frequenza di **coordinamento interno** della squadra.

### HF — onde corte

**Tipo**: uno-a-molti su distanze da regionale a intercontinentale, precisione variabile, interrompibile.

**Forza**:

- raggiunge **centinaia o migliaia di km** sfruttando la ionosfera
- **NVIS** (Near Vertical Incidence Skywave) — antenne basse irradiano verso lo zenit e "ricadono" a qualche centinaio di km: ideale per **comunicazione regionale** in zone con orografia ostile (40 m di giorno, 80 m al crepuscolo, 60 m nuova banda)
- **nessuna dipendenza** da ripetitori

**Debolezza**:

- **propagazione variabile** con l'ora, il ciclo solare, l'attività geomagnetica
- antenne **più ingombranti**: dipoli, yagi, verticali con radiali
- **QRM** (disturbi artificiali) e **QRN** (atmosferici) rendono difficile il collegamento in certi momenti
- richiede operatori più formati

**Quando usarla**: emergenza estesa oltre la portata VHF/UHF — alluvione regionale, sisma, grande incendio interprovinciale. A Genzano: utile per link con Sala Operativa Regionale o con altre province del Lazio in caso di ridondanza.

### Radio PMR 446 (Personal Mobile Radio)

**Tipo**: simplex UHF a bassa potenza (max 500 mW), **libera da licenza**, 16 canali.

**Forza**:

- **chiunque** può usarla (non serve patente)
- **apparati economici**, pronti all'uso
- adatta a **squadre ristrette** su distanze brevi (qualche centinaio di metri, massimo 1-2 km in visibilità)
- **utile nei Centri di Accoglienza** o al COC per coordinamento interno di più funzioni nello stesso edificio

**Debolezza**:

- portata **limitata**
- **affollamento** dei 16 canali in aree densamente abitate
- **nessun ripetitore** ammesso
- **nessuna interoperabilità** ufficiale con sistemi di protezione civile

**Quando usarla**: **complementare** alle radio di Gruppo. Utile per volontari non licenziati in supporto a operatori licenziati.

### CB — 27 MHz

In Italia la banda cittadina 27 MHz è libera entro limiti di potenza (max 4 W in AM/FM, 12 W in SSB) — ancora utilizzata da alcuni gruppi, ma in crescente dismissione.

**Forza**: storica, ampia base di utenza residua (soprattutto trasporto merci), economica.

**Debolezza**: **qualità audio** e portata modeste, banda affollata, in declino.

**Quando usarla**: raramente. Non è oggi un canale di riferimento per protezione civile.

### Satellite — telefonia e dati

Offerta da operatori come **Inmarsat**, **Iridium**, **Thuraya**, **Globalstar**.

**Forza**:

- **copertura globale** (o regionale, a seconda del servizio)
- **indipendente** da infrastruttura terrestre

**Debolezza**:

- **costi** elevati di apparato e di minuto chiamata
- richiede **linea di vista al satellite** (a volte antenna orientabile)
- in caso di saturazione del sistema, può **non garantire** servizio
- nessuna competenza diffusa fra i volontari

**Quando usarlo**: **Prefettura, Regione, DPC, DI.COMA.C.** — raramente disponibile ai Gruppi Comunali se non in grandi esercitazioni o in attivazione di colonna mobile.

### Digitali radioamatoriali — D-STAR, DMR, C4FM, APRS

Modalità digitali utilizzate dai radioamatori per **fonia compressa**, **dati leggeri**, **posizione GPS**, **SMS-like**, **immagini**.

- **D-STAR** (ICOM) — rete amatoriale mondiale con "reflectors"
- **DMR** (MotoTRBO/BrandMeister) — rete digitale integrabile con apparati commerciali
- **C4FM / System Fusion** (Yaesu) — evoluzione DMR/D-STAR
- **APRS** (Automatic Packet Reporting System) — posizione e messaggi brevi sulla frequenza 144.800 MHz in Europa

**Forza**:

- **qualità audio** costante indipendentemente dalla distanza (finché sopra soglia)
- **dati** strutturati: posizione GPS, stato, messaggi
- **reti globali** via Internet (hybrid) utili in scenari misti

**Debolezza**:

- apparati più **costosi** e a volte non retro-compatibili
- **dipendenza Internet** per i reflector (non per simplex on-air)
- **frammentazione**: tre standard incompatibili

**Quando usarli**: dove possibile per **tracking** dei mezzi, o per consegnare **messaggi strutturati** (liste, coordinate).

### WinLink / Packet / FT8 — dati HF

Modalità di **dati via HF** che consentono di inviare email, posizione, liste, moduli anche in assenza totale di Internet.

- **WinLink** — gateway radioamatoriali che accettano email via HF e le consegnano in Internet quando possibile
- **Packet radio** — protocollo storico AX.25 per dati radio
- **FT8** — modo digitale debole-segnale estremamente robusto, utile per collegare stazioni remote con poca potenza

**Forza**: **precisione** assoluta (è dato digitale), resiliente, funzionante anche con cellulare e Internet completamente giù.

**Debolezza**: richiede **formazione specifica**, un computer, un'interfaccia.

**Quando usarli**: invio di **liste strutturate** (sfollati, feriti, inventari) in scenari estesi.

## Matrice di scelta — esempio pratico

| Scenario | Canale consigliato | Motivo |
|---|---|---|
| Attivazione volontari | SMS + e-mail + WhatsApp | Veloce, multi-canale, log scritto |
| Comunicazione interna COC | PMR 446 o UHF 70 cm | Ravvicinata, continua, broadcast |
| COC → squadre distaccate sul territorio comunale | VHF 2 m via ripetitore locale | Copertura comunale, ridondanza |
| COC Genzano → SOUR Lazio | Canali Regione Lazio assegnati + telefono | Filiera istituzionale |
| Segnalazione criticità al 112 | **Telefono al 112 (NUE)** | Unico canale ufficiale |
| Link interprovinciale | HF 40 m NVIS o 80 m | Lunga portata indipendente |
| Lista di 50 sfollati con dati anagrafici | E-mail + WinLink in ridondanza | Alta precisione, dato scritto |
| Emergenza vitale in onda | Pro-word "**Emergenza**" + interruzione | Priorità assoluta |

## Principi di network theory applicati

1. **Scegli il canale che richiede meno tempo totale** — dall'originazione del messaggio alla ricezione completa dal destinatario
2. **Usa canali broadcast per messaggi broadcast** — non mandare uno-a-uno 20 chiamate separate
3. **Usa canali uno-a-uno per messaggi riservati** — nomi di feriti, informazioni sensibili
4. **Riserva i canali con priorità interrompibile** per il traffico di emergenza
5. **Scrivi i messaggi complessi** — non ripeterli in fonia
6. **Ridondanza** — per messaggi critici, usa più canali (radio + telefono + email)
7. **Time-shifting** — se il ricevente è occupato, lascia il messaggio in un "drop point" (segreteria, log, email) da ritirare dopo

## Il modello italiano del sistema di comunicazione PC

Il sistema nazionale di protezione civile usa una **filiera di canali** organizzata per livelli:

```
DPC (Roma, DI.COMA.C.)
    ↓
Prefettura — Regione (SOUR Lazio)
    ↓
COM / Città Metropolitana
    ↓
COC Comunale (Genzano)
    ↓
Squadre sul territorio
```

Ogni livello dispone di:

- **telefonia fissa e mobile** (primaria in condizioni normali)
- **canali radio istituzionali** (Regione, Prefettura)
- **link radioamatoriali** come **ridondanza** attivati tramite gruppi convenzionati
- **posta elettronica** (ufficiali) e **sistemi di messaggistica istituzionale**

In caso di evento, si attiva una **pluralità** di canali in parallelo, ciascuno con il suo ruolo. Il volontario TLC deve conoscere la **filiera** e inserirsi al livello giusto — in genere il **COC** del proprio Comune.

## Leggi anche

- [Capitolo 2 — Tecniche operative di base](/formazione/radiocomunicazioni-emergenza/tecniche-operative/)
- [Capitolo 4 — Gestione dei messaggi e controllo di maglia](/formazione/radiocomunicazioni-emergenza/gestione-messaggi/)
- [Manuale da Campo — Capitolo 4 — Funzioni tecniche](/formazione/manuale-campo/funzioni-tecniche/)
