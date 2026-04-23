---
title: "Capitolo 3 — Funzioni tecniche"
description: "Gli impianti e le strutture di emergenza: rete radio, elettrico, idrico e fognario, tende e tensostrutture, ristorazione, magazzini, servizi igienici e sicurezza."
---

Un campo di accoglienza è una **piccola città temporanea**: deve funzionare giorno e notte, in qualsiasi stagione, con risorse portate dall'esterno. Le **funzioni tecniche** sono le infrastrutture invisibili che lo rendono abitabile.

Questo capitolo riprende i contenuti tecnici dei moduli di colonna mobile (§2.4, Check-list 4) dal punto di vista **operativo**: come si monta, come si collauda, come si mantiene.

## 3.1 Rete TLC (telecomunicazioni)

Le comunicazioni in emergenza sono di **tre tipi**:

### Collegamenti istituzionali

Affiancano o integrano le reti di servizio (Vigili del Fuoco, Polizia, Carabinieri, ARES 118, CRI) per avere canali sempre aperti senza rischio di linee occupate. Le **maglie radio provinciali** collegano:

- **COC di Genzano** ↔ operatore sul territorio
- **COC ↔ COM** (Castelli Romani)
- **COM ↔ CCS ↔ Regione Lazio ↔ DPC**

### Collegamenti di organizzazione

Collegamenti interni del Gruppo Comunale: tra postazioni, squadre, sede operativa. Frequenza di riferimento: VHF civile assegnata al Lazio dal protocollo Ministero/DPC.

### Collegamenti punto-punto

Collegamenti "ad hoc" tra squadre di organizzazioni diverse o tra due postazioni con esigenze specifiche.

### Bande di frequenza

Lo spazio radio destinato alla protezione civile è **limitato**. Il DPC — d'intesa con il Ministero dello Sviluppo Economico — assegna bande dedicate. I volontari del Gruppo Comunale utilizzano apparati **programmati su canali autorizzati**: modifiche autonome sono vietate per legge (D.Lgs. 259/2003 — Codice delle comunicazioni elettroniche).

Bande tipiche:

| Banda | Frequenza | Uso |
|---|---|---|
| HF | 3–30 MHz | Collegamenti a lunga distanza (radioamatori ARI-RE, emergenze nazionali) |
| VHF | 144–174 MHz | Collegamenti locali e provinciali, ponte radio |
| UHF | 403–470 MHz | Collegamenti tattici in area ristretta, urbani |
| Satellitare | Thuraya, Iridium, Inmarsat | Copertura globale senza infrastruttura terrestre |

### Antenne e ponti radio

Il **ponte radio campale VHF con link UHF** (modulo di base della Colonna Mobile) garantisce copertura di 12–30 km². L'installazione prevede:

- **sito alto** (collina, traliccio, terrazza edificio agibile)
- **alimentazione 220/12V** con batterie di backup
- **messa a terra** conforme
- **test di copertura** prima dell'attivazione operativa

### Regole della comunicazione radio

1. **Ascolta prima di trasmettere** — nessuno parla sopra un'altra comunicazione
2. **Identificati sempre** — nominativo del Gruppo + sigla individuale
3. **Frasi brevi** — il messaggio entra in pochi secondi
4. **Parole chiare** — usa l'**alfabeto fonetico NATO** per lettere critiche (Alfa, Bravo, Charlie…)
5. **Conferma ricezione** — "Ricevuto" o "Negativo"
6. **Niente dati personali** — nomi, numeri, indirizzi di persone fragili non vanno in chiaro sulla radio
7. **Disciplina assoluta** — la radio non è un telefono: serve solo per la missione

### ICT e connettività

Ogni campo ha una **rete dati**:

- **router satellitare** (soluzione più affidabile, costo alto)
- **chiavetta 4G/5G** (se copertura disponibile)
- **rete WiFi di campo** (copre segreteria, comando, infopoint)
- **VPN** verso la SOUR Lazio o verso il DPC per flussi ufficiali

## 3.2 Strutture sanitarie

Le strutture sanitarie di un campo si articolano su **livelli**:

- **Posto Medico Avanzato (PMA) di 1° livello**: triage rapido, primo soccorso, evacuazione
- **PMA di 2° livello**: triage + pronto soccorso chirurgico + pronto soccorso medico + alloggio personale (dettagli dotazione in G.U. n. 139 suppl. 196 del 25/08/2003)

In un campo di accoglienza attivato dalla Colonna Mobile, il PMA di 2° livello può trattare **50 pazienti/giorno per 72 ore**.

Sul territorio di Genzano, in emergenze di rilievo locale (Tipo A), non si installa un PMA: i **feriti** sono presi in carico dall'**ARES 118** (sistema 112 NUE) e trasportati al più vicino ospedale attivo (Ospedale dei Castelli di Ariccia, Policlinico Tor Vergata, San Camillo Forlanini).

## 3.3 Impiantistica

### 3.3.1 Elettricità

Un campo vive di **generatori**: la rete elettrica pubblica — quando disponibile — è quasi sempre sovraccarica e rischia interruzioni.

#### Cavi

| Tipo | Sigla | Uso |
|---|---|---|
| Unipolare/multipolare, gomma + PVC | **FG70R 0,1/1 kV** | Posa fissa, anche interrata |
| Unipolare/multipolare, gomma + neoprene | **H07RN-F** | Posa mobile, resistente acqua e abrasione |
| Unipolare/multipolare, gomma + policloroprene | **FG1K 450/750 V** | Posa mobile |

La **sezione del conduttore** si calcola conoscendo portata, corrente di utilizzo e lunghezza (per limitare la caduta di tensione).

#### Prese

Le prese mobili devono essere di **tipo industriale**, conformi alla norma **CEI 23-12**, grado di protezione almeno **IP67**.

#### Quadri elettrici

- Norma di riferimento: **CEI 17-13/1**
- Grado di protezione minimo: **IP55**
- **Quadro generale** con prese Power Look per alimentare fino a **4 quadri di zona**
- Ogni quadro di zona alimenta i **quadri di distribuzione** delle tende

#### Messa a terra e protezioni

- **Interruttore differenziale** (salvavita) su ogni circuito
- **Dispersore** di terra infisso nel terreno, collegato al quadro generale
- **Verifica continuità** con strumento certificato
- **Protezione magnetotermica** dimensionata sul carico

### 3.3.2 Acqua

- **Fonte primaria**: allacciamento a rete pubblica — con richiesta formale e lettura contatore
- **Fonte alternativa**: cisterne della Colonna Mobile (1000 l) + **kit potabilizzazione**
- **Controlli**: prelievo campioni per analisi microbiologiche (**ASL Roma 6**) entro 24 ore dall'apertura del campo, poi con cadenza settimanale
- **Autoclavi** per pressurizzazione della rete interna
- **Cartellonistica**: "Acqua potabile" o "Non potabile" in **più lingue** (italiano, inglese, francese, arabo, ucraino — adattare al contesto)

### 3.3.3 Fognature

- Allaccio alla rete pubblica se presente e funzionante
- Altrimenti **vasca Imhoff** o **serbatoi a tenuta** con svuotamento programmato tramite autospurgo
- **Separazione** acque nere / grigie dove possibile
- Manutenzione e svuotamento tracciati in registro

### 3.3.4 Gas

- **Bombole GPL** per cucina e boiler (stoccaggio in area dedicata, ventilata, con estintori)
- **Nessuna bombola** all'interno di tende chiuse
- **Impianto certificato** da tecnico abilitato prima della messa in esercizio

## 3.4 Tende e tensostrutture

### Tipologie

- **Tenda PI 88** (ministeriale) — 6 posti, struttura metallica e telo esterno; tempo di montaggio ~30 min in 4 persone
- **Tenda pneumatica 4 archi** (7,5×5,5 m) — montaggio 10–15 min con compressore, adatta a comando, mensa, sanità
- **Tenda pneumatica 8 posti** — alloggio ospiti, pavimentazione grelle
- **Tensostruttura 12×18 m** — distribuzione pasti / refettorio, con termoconvettore e condizionamento

### Accessori indispensabili

- **Pavimentazione** modulare (grelle livellanti) — evita infiltrazioni e umidità
- **Termoriscaldatori** per inverno, **condizionatori** per estate
- **Illuminazione** interna (una plafoniera per tenda minimo)
- **Quadro tenda** con prese e interruttore
- **Zavorre** per ancoraggi (non si confida solo sui picchetti)

### Montaggio

- Almeno **2 operatori esperti + 2 di supporto** per tenda PI 88
- **Checklist di sicurezza** prima dell'occupazione: tenuta teli, ancoraggi, impianti elettrici e termici collaudati

## 3.5 Ristorazione

La **funzione ristorazione** è una delle più visibili per la popolazione ospitata. Vive di **igiene** e di **regolarità**.

- **Modulo produzione e distribuzione pasti**: fino a **350 pasti a turno in 12 ore** (vedi §2.4, Check-list 4)
- **HACCP** sempre applicato: temperature di cottura, catena del freddo, separazione crudo/cotto
- **Tracciabilità** delle derrate: lotto, scadenza, provenienza
- **Turni pasti** scaglionati per evitare assembramenti
- **Menu ruotato** su 7 giorni, con alternative per **intolleranze** e **religioni** (ove possibile)

## 3.6 Magazzini

Strutture di stoccaggio per:

- **Depositi alimentari** — cella frigo + freezer + scaffalature secco
- **Depositi stoviglie monouso**
- **Depositi prodotti per pulizia e disinfezione** — area separata, etichettatura chiara, schede di sicurezza (SDS) disponibili
- **Stoccaggio merci** — container o tende dedicate

**Registro di magazzino**: ogni entrata/uscita tracciata (data, ora, voce, quantità, firma). La tracciabilità è un requisito di legge quando l'attività è rendicontata a Stato/Regione.

## 3.7 Servizi igienici

### Prima emergenza

Nelle prime 24–48 ore, quando il modulo container non è ancora installato:

- **Latrine chimiche** mobili (una ogni 20 persone, rapporto 3:1 donne/uomini — standard UNHCR)
- **Punti di lavaggio mani** con sapone
- **Raccolta rifiuti** in sacchi dedicati

### Installazione definitiva

- **Moduli container** 3×2,5 m con WC + lavabo + doccia
- **Modulo disabili** obbligatorio (almeno 1)
- **Separazione** servizi soccorritori / ospiti
- **Pulizia giornaliera** programmata e verbalizzata
- **Disinfezione** con prodotti clorati

## 3.8 Sicurezza

### Piano di emergenza del campo

Ogni campo ha un **piano di emergenza interno**, affisso in bacheca e illustrato agli ospiti:

- **vie di fuga** segnalate (frecce verdi, luci di emergenza)
- **punti di raccolta** in caso di evacuazione
- **procedure** in caso di incendio, scossa sismica, fuga di gas
- **elenco responsabili** per area

### Segnaletica

- **Cartellonistica** in più lingue
- **Pittogrammi** standard ISO 7010 (sicurezza)
- **Illuminazione** di emergenza in ogni area

### Antincendio

- **Estintori** (polvere ABC o CO2) in ogni modulo
- **Idranti** UNI 45 se disponibili
- **Formazione** degli addetti antincendio (almeno 1 per turno)
- **Procedure di evacuazione** esercitate alla prima apertura del campo

### Guardiania e sorveglianza

Vedi [Capitolo 4 — Funzioni di servizio](/formazione/manuale-campo/funzioni-servizio/).

## Leggi anche

- [Struttura organizzativa](/formazione/manuale-campo/struttura-organizzativa/)
- [Scouting e valutazione iniziale](/formazione/manuale-campo/scouting/)
- [Funzioni di servizio](/formazione/manuale-campo/funzioni-servizio/)
- [Schede tecniche — raccolta rapida](/formazione/manuale-campo/schede-tecniche/)
