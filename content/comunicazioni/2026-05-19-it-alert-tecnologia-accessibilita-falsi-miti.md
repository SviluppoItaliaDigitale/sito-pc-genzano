---
title: "IT-alert: storia, tecnologia, accessibilità e cinque falsi miti smontati"
date: 2026-05-19T00:03:00+02:00
description: "Da dove viene IT-alert, perché Cell Broadcast non è un SMS, come funziona per chi non sente o non vede, e i cinque falsi miti più diffusi."
badge: "Informazione"
priorita: "normale"
autore: "Gruppo Comunale Volontari PC Genzano"
image: "/images/2026-05-19-it-alert-tecnologia-accessibilita-falsi-miti.webp"
image_alt: "Cover dell'articolo: IT-alert: storia, tecnologia, accessibilità e cinque falsi miti smontati"
scadenza: ""
area: "Italia"
allegati: []
draft: false
tts: true
lis_section: "gestione-emergenza"
---

Sappiamo cos'è **IT-alert** e cosa fare quando arriva. Questo articolo fa un passo in più. Racconta da dove nasce il sistema, perché la sua tecnologia non è un SMS, come funziona per chi non sente o non vede, e smonta cinque falsi miti diffusi.

Non sostituisce la **guida base**: la integra con il backstage tecnico.

## Da dove nasce IT-alert

Il sistema viene da un obbligo europeo. La **direttiva UE 2018/1972** (Codice europeo delle comunicazioni elettroniche), all'articolo 110, chiede a ogni Stato membro di dotarsi di un sistema di **allerta pubblica via cellulare** entro il 21 giugno 2022.

L'Italia ha attuato l'obbligo con il **DPCM 19 giugno 2022** e con il **Decreto del Capo del DPC del 7 febbraio 2023** (DPC = Dipartimento della Protezione Civile). IT-alert è il nome del sistema nazionale.

La fase di test è durata circa due anni:

- **Estate 2023**: test regionali a rotazione (Toscana, Sardegna, Sicilia, Calabria, Emilia-Romagna, Friuli Venezia Giulia, e altre).
- **14 settembre 2023**: primo test simultaneo a livello nazionale.
- **13 febbraio 2024**: il sistema entra in operatività piena.

## Casi reali di attivazione

I test sono prove. Le **attivazioni reali** sono quando il sistema viene usato per una vera emergenza.

**21 settembre 2023, diga di Camastra (Basilicata).** Prima attivazione operativa di IT-alert. Il sistema avvisa i Comuni a valle del possibile sovrappieno della diga, in coordinamento con la Regione Basilicata. Funziona.

**9 ottobre 2023, Stromboli.** Un parossismo eruttivo del vulcano fa scattare IT-alert per residenti e turisti dell'isola, con indicazione delle zone sicure.

**2024, Etna.** Più attivazioni durante fontane di lava, con segnalazione di chiusura dello spazio aereo e ricaduta di cenere su alcuni Comuni.

**2024, esercitazione Campi Flegrei.** Test di evacuazione della zona gialla in scenario simulato: IT-alert affianca le sirene comunali per verificare i tempi di reazione della popolazione.

Il DPC pubblica le attivazioni più recenti sul sito ufficiale del sistema.

## Cell Broadcast — come funziona davvero

IT-alert non è un SMS. La tecnologia sotto si chiama **Cell Broadcast** ed è uno standard 3GPP per le reti mobili. Conoscerla aiuta a capire perché alcune cose sono possibili e altre no.

**È un broadcast**, non un invio uno-a-uno. L'antenna cellulare trasmette il messaggio come una radio: tutti i telefoni agganciati alla cella lo ricevono insieme. Non c'è una lista di destinatari, non c'è un numero da chiamare, non c'è un mittente.

**Non passa dalla rete dati**. Basta avere campo voce 2G, 3G, 4G o 5G. Il messaggio arriva anche con il piano dati esaurito o con i dati disattivati.

**Non drena la batteria**. Il telefono è già in ascolto sulle frequenze cellulari per ricevere chiamate. Il canale Cell Broadcast viaggia sulle stesse onde: nessun servizio in background nuovo, nessun consumo aggiuntivo.

**Non serve un'app**. I sistemi operativi mobili (iOS e Android) gestiscono nativamente i canali di emergenza. Apple e Google hanno implementato da molti anni le **API per le allerte di emergenza wireless** (Wireless Emergency Alerts). IT-alert usa questa infrastruttura già presente nel telefono.

**Il sistema non sa chi sei**. Il telefono riceve il messaggio, ma non risponde, non si registra, non comunica la sua posizione a IT-alert. Il DPC non vede un elenco di chi ha ricevuto la notifica.

## Per chi non sente o non vede

IT-alert ha caratteristiche di accessibilità native, ma anche limiti che è onesto dichiarare.

**Persone sorde o ipoacusiche.** Il telefono vibra in modo insistente e il messaggio appare a schermo intero. Su iPhone l'opzione "Avvisi LED del flash" lampeggia il flash della fotocamera. Su molti Android (Pixel, Samsung) c'è la funzione equivalente "Notifica con flash". Apple Watch e smartwatch Android vibrano al polso. **Limite**: chi è completamente sordo e dorme con il telefono lontano non percepisce nulla. Qui restano centrali il **piano famiglia** e il vicinato preparato.

**Persone cieche o ipovedenti.** I lettori di schermo (**VoiceOver** su iOS, **TalkBack** su Android) sono progettati per leggere automaticamente le notifiche di sistema. IT-alert appare come una notifica prioritaria e viene letta ad alta voce. **Limite**: la lettura automatica dipende dalle impostazioni del lettore e dallo stato del telefono (sblocco, blocco). Verificare la configurazione prima è importante.

**Italiano L2 e stranieri.** Il messaggio è scritto in **italiano e in inglese** (la versione inglese segue quella italiana nel corpo del testo). Chi parla solo arabo, urdu, rumeno, cinese o altre lingue non capisce. Il limite è strutturale: il DPC sta valutando l'estensione ad altre lingue. Nel frattempo il Gruppo Volontari e i Comuni completano IT-alert con cartelli multilingua nei **punti di raccolta** e con i mediatori culturali.

**Anziani con feature phone.** I telefoni a tastiera recenti (Doro, Nokia 110/150 di nuova generazione, alcuni Brondi) supportano il Cell Broadcast e ricevono IT-alert. I telefoni molto vecchi (pre-2010) o i "kid phone" semplificati di solito no. Un controllo nel libretto di istruzioni o un test con un familiare durante un test ufficiale chiarisce la situazione.

## Cinque falsi miti

**"IT-alert ti spia o ti traccia."** Falso. Il Cell Broadcast è unidirezionale: dall'antenna al telefono. Il telefono non risponde, non si registra, non manda la sua posizione. Il DPC non sa chi ha ricevuto il messaggio, sa solo a quali celle ha trasmesso.

**"IT-alert scarica la batteria."** Falso. Il canale Cell Broadcast non aggiunge consumo: viaggia sulle stesse frequenze che il telefono ascolta già per ricevere chiamate. Nessun servizio in background nuovo è in esecuzione.

**"È obbligatorio avere uno smartphone."** Falso. La legge non obbliga nessuno a possedere un cellulare. IT-alert è un canale aggiuntivo, non l'unico. Le allerte continuano a essere diffuse anche tramite radio, televisione, sito del Comune, altoparlanti delle squadre di volontariato.

**"Le aziende lo useranno per pubblicità."** Falso. Solo il DPC può autorizzare un messaggio IT-alert sul canale ufficiale. Le aziende non hanno accesso al sistema. Chi propone "iscrizioni IT-alert" o "abbonamenti premium" è una truffa: il sistema è gratuito, non richiede registrazioni, non ha versioni a pagamento.

**"All'estero ricevi IT-alert italiano, oppure pubblicità travestita."** Falso in entrambi i casi. Fuori dalle antenne italiane non ricevi IT-alert nazionale. Puoi però ricevere il **sistema di allerta del Paese ospitante** (EU-Alert francese, Cell Broadcast tedesco, sistema spagnolo ES-Alert, e così via) se sono attivi. Non sono pubblicità: sono allerte ufficiali del Paese in cui ti trovi. Sui telefoni le impostazioni si trovano in "Notifiche di emergenza" o "Avvisi pubblici di emergenza".

## Cosa portare a casa

IT-alert è un canale aggiuntivo che funziona con tecnologia matura, presente nei telefoni da anni, gestita dai sistemi operativi e usata in tutta Europa. Ha limiti reali — soprattutto per chi parla altre lingue o ha disabilità sensoriali profonde — e ci sono attivazioni concrete che dimostrano quando il sistema serve davvero.

Quando il telefono suonerà l'allarme inconfondibile, sai che dietro c'è una decisione del DPC, una verifica tecnica, e una rete di soccorso che si sta già muovendo. Leggi, capisci, agisci.

## Per approfondire

Sul nostro sito:

- [Come dovrebbe funzionare un sistema di allerta pubblica: ISO 22322 e IT-alert](/comunicazioni/2026-05-15-iso-22322-public-warning-it-alert/)
- [App Where Are U — localizzazione automatica al 112](/comunicazioni/2026-04-27-app-where-are-u-112-localizzazione-emergenza/)
- [Piano di emergenza familiare](/piano-familiare/)
- [Glossario: IT-alert, DPC, Cell Broadcast](/glossario/)

Fonti istituzionali:

- [IT-alert — Sito ufficiale del Dipartimento della Protezione Civile](https://www.it-alert.it/it/)
- [Direttiva UE 2018/1972 (Codice europeo comunicazioni elettroniche), articolo 110](https://eur-lex.europa.eu/legal-content/IT/TXT/?uri=CELEX%3A32018L1972)
- [DPCM 19 giugno 2022 — Istituzione di IT-alert](https://www.protezionecivile.gov.it/it/normativa/)
