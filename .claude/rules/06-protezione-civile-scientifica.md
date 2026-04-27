# Protezione Civile — Validazione Scientifica e Comunicazione del Rischio

## Principio guida

Ogni contenuto relativo a rischio, allerta, emergenza, prevenzione, meteo, territorio o volontariato deve essere:
- Tecnicamente corretto e verificabile
- Coerente con le fonti ufficiali nazionali e regionali
- Prudente e non allarmistico
- Comprensibile da un cittadino non tecnico
- Utile all'autoprotezione della popolazione
- Adattato al contesto territoriale di Genzano di Roma quando rilevante

## Distinzioni obbligatorie

Distingui sempre chiaramente tra:

| Tipo | Caratteristiche |
|---|---|
| **Informazione ordinaria** | Aggiornamenti istituzionali, attività del gruppo, comunicazioni organizzative |
| **Prevenzione** | Comportamenti e buone pratiche fuori dall'emergenza |
| **Allertamento** | Comunicazioni di allerta meteo o rischio in corso, con livello e area precisi |
| **Comunicazione di emergenza** | Istruzioni operative durante un evento in atto |
| **Aggiornamento operativo** | Stato degli interventi, esito di attivazioni |
| **Volontariato** | Promozione, iscrizioni, formazione, attività del gruppo |
| **Formazione** | Corsi, esercitazioni, aggiornamenti tecnici |

Non mescolare questi tipi all'interno dello stesso comunicato senza chiarezza esplicita.

## Quando usare il badge "Allerta" e quando "Emergenza"

I badge `Allerta` ed `Emergenza` hanno colori distinti (rosso `#d9364f` vs rosso scuro `#7f1d1d`) perché comunicano due fasi diverse del ciclo del rischio. Non sono sinonimi e non vanno alternati per varietà editoriale.

**Badge `Allerta` — fase di PREVISIONE**
- Usa questo badge quando l'evento è **previsto** ma non ancora in corso.
- Il contenuto tipico è un bollettino di allerta meteo regionale, un avviso di criticità idrogeologica, un'allerta incendio boschivo su base previsionale.
- Deve riportare: livello (`verde`, `giallo`, `arancione`, `rosso`), tipo di rischio, area geografica, finestra temporale di validità, fonte ufficiale (Centro Funzionale Regionale Lazio, DPC, Protezione Civile Lazio).
- Il tono è prudenziale e informativo: "è previsto", "sono attesi", "si raccomanda di".
- Viene emesso prima che accada qualcosa, in modo da consentire l'autoprotezione.

**Badge `Emergenza` — fase di EVENTO IN CORSO**
- Usa questo badge solo quando un evento **è in atto** e impone azioni operative immediate alla popolazione.
- Il contenuto tipico è una comunicazione durante l'attivazione del Centro Operativo Comunale (COC), un'evacuazione in corso, un intervento attivo su un territorio, un'emergenza sanitaria locale in evoluzione.
- Deve riportare: cosa sta accadendo adesso, dove, chi sta intervenendo, cosa deve fare il cittadino in quel preciso momento, canale di aggiornamento continuo.
- Il tono è operativo e direttivo: "è in corso", "allontanarsi da", "raggiungere l'area di raccolta".
- Il badge `Emergenza` non si usa per raccontare eventi conclusi: in quel caso il badge corretto è `Aggiornamento` (esito operativo) o `Comunicazione` (resoconto istituzionale).

**Criterio sintetico:**

| Fase | Badge | Tono verbale |
|---|---|---|
| Prima dell'evento (previsione) | `Allerta` | "è previsto / atteso" |
| Durante l'evento (azione) | `Emergenza` | "è in corso / in atto" |
| Dopo l'evento (resoconto) | `Aggiornamento` o `Comunicazione` | "è stato / si è concluso" |

**Regola operativa:** se hai dubbi tra `Allerta` e `Emergenza`, chiediti se l'evento è già iniziato per il cittadino. Se no, è `Allerta`. Se sì e richiede un comportamento immediato, è `Emergenza`.

Il badge `Emergenza` è intenzionalmente raro. Un abuso ne riduce l'impatto comunicativo proprio quando serve davvero.

## Codici colore allerta meteo (Regione Lazio)

| Colore | Significato |
|---|---|
| Verde | Nessuna allerta, situazione ordinaria |
| Giallo | Allerta ordinaria — fenomeni previsti di intensità moderata |
| Arancione | Allerta elevata — fenomeni intensi con possibili effetti rilevanti |
| Rosso | Allerta massima — fenomeni molto intensi con rischio elevato per la popolazione |

Il codice colore va sempre associato al tipo di rischio (idrogeologico, temporali, vento, neve, ecc.) e all'area geografica interessata.
Non usare "massima allerta" o "allerta rossa" in modo improprio per fenomeni ordinari.

## Struttura uniforme delle pagine `/rischi-prevenzione/*`

Le 7 pagine operative dei rischi (sismico, idrogeologico, incendio, vento, temporali, blackout, ondate calore) hanno una **struttura fissa**, in quest'ordine:

1. **Perché è rilevante sul nostro territorio** (contesto Genzano/Castelli Romani: dati territoriali, eventi storici, fattori di rischio specifici).
2. **Segnali e situazioni tipiche** (opzionale, dove serve preavviso percepibile dal cittadino).
3. **Cosa fare PRIMA** — preparazione: bullet, voce attiva, frasi brevi.
4. **Cosa fare DURANTE** — azione immediata: bullet con verbi all'imperativo.
5. **Cosa fare DOPO** — recupero e segnalazione danni: bullet, riferimento al 112 per pericoli concreti.
6. **`{{< cosa-non-fare >}}`** — box rosso con i 4-6 errori comportamentali tipici di quel rischio.
7. **`{{< chi-chiamare >}}`** — chiusura standard con la tabella accessibile dei numeri (112 / 112 / 803 555) + nota istituzionale che chiarisce che il **Gruppo Comunale non è attivabile direttamente dai cittadini**.

**Regole operative:**
- L'ordine è **fisso e non negoziabile**: il cittadino in stress (e lo screen reader user) deve trovare le stesse sezioni nello stesso posto in ogni pagina rischio. Coerenza WCAG 3.2.3 / 3.2.4.
- Lo shortcode `{{< chi-chiamare >}}` chiude **sempre** la pagina: se aggiungi nuove sezioni, vanno **prima** del chi-chiamare, mai dopo.
- Il numero 112 nel testo è un'occorrenza editoriale; nella tabella `chi-chiamare` è un `<a href="tel:112">` cliccabile (mobile). Non duplicare la stessa logica con altri "Chi chiamare" hand-rolled: usare sempre lo shortcode per garantire coerenza.
- Se in futuro si aggiunge un nuovo rischio operativo (es. ondate di freddo, neve, eruzioni), creare la nuova pagina `content/rischi-prevenzione/<nuovo>.md` rispettando lo stesso schema.

Le **2 pagine di supporto** (`kit-emergenza.md`, `persone-necessita-specifiche.md`) sono pagine di servizio, non di rischio: non rientrano nello schema sopra. Hanno strutture proprie (bullet di componenti, raccomandazioni per categorie). Nessun `chi-chiamare` né `cosa-non-fare` obbligatorio.

## Rischi specifici del territorio

### Rischio idrogeologico
Genzano di Roma è nel territorio dei Castelli Romani, con versanti collinari soggetti a fenomeni di erosione e frane localizzate. In caso di allerta idrogeologica, indicare sempre l'area interessata e i comportamenti di autoprotezione raccomandati dal Piano di Protezione Civile comunale.

### Rischio incendi boschivi (AIB)
Il periodo di massima pericolosità è giugno–settembre. Nel Lazio il numero da chiamare è **il 112** (NUE): la Centrale Unica smista l'intervento a vigili del fuoco e squadre AIB. Non chiamare direttamente il gruppo di volontari per segnalare incendi attivi.

### Rischio sismico
Il Lazio è una regione a sismicità media. In caso di scossa, rimanda sempre alle linee guida ufficiali del Dipartimento di Protezione Civile per i comportamenti di autoprotezione.

### Rischio meteo generico
Per allerte meteo usa solo i dati ufficiali di ARPAM Lazio o del Centro Funzionale Regionale del Lazio. Non diffondere previsioni non ufficiali come comunicazioni istituzionali.

## Numeri di emergenza da citare sempre correttamente

Nel Lazio, dal 2017, **l'unico numero di emergenza per il cittadino è il 112** (NUE — Numero Unico Europeo). Tutte le chiamate arrivano alla Centrale Unica del NUE, che smista l'intervento all'ente competente (vigili del fuoco, emergenza sanitaria, forze dell'ordine, squadre AIB). Le vecchie linee 115, 118 e 1515 non sono più il riferimento da comunicare al cittadino.

| Numero | Servizio |
|---|---|
| 112 | Numero Unico Emergenze (NUE) — qualsiasi emergenza |
| 803 555 | Sala Operativa Protezione Civile Lazio — segnalazioni non urgenti |
| 1530 | Guardia Costiera — emergenze in mare e sui laghi |

Non citare numeri di emergenza non verificati. Non presentare più 115/118/1515 come numeri da chiamare: il cittadino deve memorizzare un solo numero, il 112. I numeri del gruppo di volontari non sostituiscono il 112.

**Nota**: "NUE 112" e "ARES 118" possono essere citati come **nomi di organizzazioni** quando il contesto lo richiede (es. riferimenti istituzionali), ma mai come numero da chiamare in emergenza.

## Regole di comunicazione del rischio

- Non generare allarme ingiustificato: usa un tono calmo, informativo e rassicurante.
- Non minimizzare: se un rischio è reale e documentato, comunicalo con chiarezza.
- Indica sempre la fonte dell'allerta (es. "secondo il bollettino del Centro Funzionale Regionale Lazio").
- Distingui tra "è previsto" e "è in corso".
- Per i comportamenti di autoprotezione, cita sempre fonti ufficiali (DPC, Regione, Comune).
- Non pubblicare contenuti meteo o di rischio basati su fonti non istituzionali.

## Gerarchia delle fonti per la comunicazione del rischio e dell'emergenza

Il Gruppo si attiene a un quadro di fonti **gerarchico**: in caso di conflitto teorico, prevale la fonte di livello superiore. Specifiche complete in `MANUALE-SITO.md` Parte 13.9.

### Livello 1 — italiano vincolante (AGID + DPC)

- **AGID — Linee guida per la comunicazione digitale della PA**: stile, accessibilità, linguaggio chiaro, design system. Riferimento orizzontale per ogni contenuto digitale della PA.
- **DPC — Dipartimento della Protezione Civile**, riferimento settoriale italiano per la comunicazione del rischio:
  - **D.Lgs. 1/2018** (Codice della Protezione Civile);
  - **Direttiva PCM 30 aprile 2021** sul Servizio nazionale di Protezione Civile;
  - **Linee guida DPC sulla comunicazione del rischio e dell'emergenza**;
  - **Campagne nazionali "Io non rischio"** — manuali operativi per rischio sismico, vulcanico, maremoto, alluvione, incendio boschivo;
  - **Bollettini di criticità nazionale** e **codici colore ufficiali** (verde, giallo, arancione, rosso).

In caso di conflitto tra AGID e DPC su un contenuto di Protezione Civile, **vince DPC**: siamo un Gruppo Comunale del Sistema Nazionale di PC ai sensi del D.Lgs. 1/2018.

### Livello 2 — scientifico italiano (CNR, ISPRA)

- **CNR — Consiglio Nazionale delle Ricerche**, autorità scientifica per i rischi naturali:
  - **CNR-IRPI** (Istituto di Ricerca per la Protezione Idrogeologica) — frane, alluvioni, dissesti.
  - **CNR-INGV** (con l'Istituto Nazionale di Geofisica e Vulcanologia) — sismologia, vulcanologia.
  - **CNR-IGAG** (Geologia Ambientale e Geoingegneria) — territori e infrastrutture.
- **ISPRA** — dati territoriali nazionali (idrogeologico, costiero, sismico).

CNR/ISPRA garantiscono la **correttezza scientifica** dei contenuti; DPC garantisce la **correttezza operativa** della comunicazione. Su un dato scientifico vince CNR/ISPRA; sul *come* comunicarlo al cittadino vince DPC.

### Livello 3 — tecnico-operativo europeo (EENA, CWA)

- **EENA — European Emergency Number Association**: riferimento europeo per il **Numero Unico 112** e per l'**app Where Are U**, sviluppata con il loro coinvolgimento. Pubblicazioni rilevanti: *Social Media in Emergency Services*, linee guida sull'accessibilità del 112 per persone con disabilità.
- **CWA CEN/CENELEC draft** *Guidelines for effective social media messages in crisis and emergency situations*: struttura messaggi di allerta, hashtag, accessibilità dei post.

### Livello 4 — standard internazionali (ISO, WCAG)

- **ISO 22329:2021** *Security and resilience — Emergency management — Guidelines for the use of social media in emergencies*: monitoraggio, disseminazione, interazione, gestione della disinformazione.
- **WCAG 2.2 AA** (W3C): accessibilità tecnica.

### Cosa NON adottiamo (con motivazione esplicita)

- **CWA: "evitare il colore verde"** — in Italia il codice colore verde = nessuna criticità è ufficiale e standardizzato dal Centro Funzionale Regionale. Cambiarlo creerebbe confusione, quindi **resta verde** (prevale livello 1, DPC).
- **ISO 22329: "Social Media Manager dedicato 24/7"** — non sostenibile per un Gruppo di volontari. Manteniamo gli orari di presìdio dichiarati onestamente nella Social Media Policy (compatibile con AGID).

## Esperti da attivare in base al tema

Quando produci contenuti su questi temi, ragiona come se stessi consultando:
- **Allerte meteo**: meteorologo + Centro Funzionale Regionale Lazio
- **Frane e dissesto**: geologo + PAI (Piano di Assetto Idrogeologico)
- **Alluvioni e allagamenti**: idrologo / ingegnere idraulico
- **Terremoti**: sismologo + DPC (mappe di pericolosità sismica)
- **Incendi boschivi**: esperto AIB + Regione Lazio
- **Mappe e territorio**: GIS specialist + dati comunali
- **Emergenze sanitarie**: autorità sanitarie competenti (ASL Roma 6)
