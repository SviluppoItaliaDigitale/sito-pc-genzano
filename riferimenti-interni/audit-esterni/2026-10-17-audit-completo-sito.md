# Audit completo del sito della Protezione Civile di Genzano di Roma

Data delle verifiche: 17 ottobre 2026. Sito: https://www.protezionecivilegenzano.it/

## 1. Giudizio complessivo

Il sito è un portale informativo e didattico evoluto, con una buona identità istituzionale, molti servizi concreti e una struttura tecnica già sottoposta a controlli frequenti. I punti migliori sono l'orientamento ai bisogni del cittadino, il patrimonio per le scuole, le alternative di lettura e l'uso di fonti riconoscibili.

La priorità è consolidare quello che esiste: prestazioni mobili, accessibilità effettiva delle funzioni interattive, coerenza delle indicazioni ripetute e attendibilità dei giudizi automatici sui documenti. L'ampiezza dell'offerta richiede un controllo trasversale delle versioni, oltre alla verifica delle singole pagine.

Non attribuisco una certificazione di accessibilità, sicurezza o conformità normativa. Il rapporto distingue problemi riprodotti, limiti dei controlli e miglioramenti proposti. Non sono state apportate correzioni al sito.

## 2. Perimetro e metodo

- Scansione HTTP di tutti i 1.241 indirizzi della sitemap corrente: 1.240 pagine HTML e un endpoint JSON. Tutti hanno risposto 200, senza reindirizzamenti.
- Controllo dell'HTML iniziale di tutte le 1.240 pagine: titolo principale, lingua, descrizione, canonical, presenza dell'attributo alt e sintassi dei dati strutturati.
- Analisi di 1.742 blocchi JSON-LD: nessun errore di sintassi. Non equivale a validazione semantica completa Schema.org o dei risultati avanzati di Google.
- Controllo delle ancore interne verso le pagine scansionate: nessun riferimento mancante rilevato. Le destinazioni create soltanto dopo interazioni JavaScript restano fuori da questo controllo statico.
- Ulteriori 34 destinazioni interne individuate fuori dalla sitemap e non risolte dall'inventario dei file statici: tutte raggiungibili con risposta 200. Controllati anche i quattro PDF nuovi assenti dall'audit documentale pubblico.
- Prove nel browser: home, ricerca, assistente, schede Terremoti e Allerta del cruscotto, composizione di una lezione e libro pop-up.
- Analisi tecnica di quattro PDF scaricati dal sito: poster italiano di emergenza, modulo di ammissione, manuale e presentazione della struttura del sito. Esame visivo del poster e di una pagina della presentazione.
- Lettura mirata del repository, delle configurazioni di controllo, degli header HTTP e dei log di esecuzioni automatiche del 17 ottobre.
- Verifica delle indicazioni sul caldo con il Ministero della Salute, della formulazione sulle fughe di gas con i Vigili del Fuoco e della procedura di dichiarazione con AgID.

Il repository inizialmente rilevato era al commit a236864facae71f04081bf6227b314964725c7da. Durante l'audit le automazioni hanno continuato a lavorare; una successiva lettura di main ha restituito 2087c99c6006bc11bbc5f60587fdc0c5ae1e4718. Il sito riportava una build del 17 ottobre alle 18:30, ora italiana. Le verifiche descrivono gli stati osservati durante la sessione.

## 3. Quadro per area

| Area | Valutazione | Motivo principale |
| --- | --- | --- |
| Disponibilità e collegamenti | Buona | Tutta la sitemap raggiungibile; pagina inesistente con vero HTTP 404 |
| Contenuti e utilità locale | Buona | Rischi, aree di attesa, contatti, piani e attività del territorio |
| Navigazione e ricerca | Buona, da snellire | Ricerca efficace; molte porte d'accesso e pagine molto estese |
| Didattica | Ricca, da consolidare | Materiali per fasce, esperimenti, percorsi; incoerenze nelle durate e nelle copie |
| Accessibilità HTML | Buona base, verifica incompleta | Markup curato; problema semantico riprodotto nell'assistente |
| Documenti PDF | Da migliorare con priorità | Poster raster, manuale senza struttura e classificazioni troppo ottimistiche |
| Prestazioni mobili | Da migliorare | Ultimo Lighthouse disponibile: home 76/100, sotto il target di 85 |
| SEO tecnico | Buona base | Canonical e descrizioni presenti; JSON-LD valido sintatticamente |
| Sicurezza HTTP | Buona base | HTTPS, HSTS e altri header; CSP ulteriormente restringibile |
| Privacy | Informativa articolata | Distinte richieste automatiche e widget su clic; trattamenti effettivi da verificare con il titolare |
| Affidabilità delle allerte | Impostazione prudente, da uniformare | Fonti e orari presenti; aggiornamento e gestione dei dati non recenti diverse tra le viste |
| Manutenzione e controlli | Evoluta, da ampliare | Controlli frequenti; campione limitato e alcuni esiti non bloccanti |

Le valutazioni sono giudizi editoriali motivati, non punteggi di uno standard o una classifica comparativa.

## 4. Punti di forza verificati

1. Le informazioni urgenti sono raggiungibili da più punti. Il 112 è separato dai recapiti per informazioni e il ruolo del Gruppo nella catena di attivazione è spiegato.
2. La pagina /emergenza/ pesa circa 9,8 kB di HTML non compresso e non richiede asset esterni di impaginazione. È una scelta utile per rete debole.
3. Nella ricerca, la frase aree di attesa restituisce come primo risultato la pagina locale pertinente. Sono disponibili anche i collegamenti alle sue sezioni.
4. Il cruscotto ha caricato i terremoti con data di aggiornamento, tabella testuale e fonte INGV. La scheda Allerta avverte quando il controllo pubblicato non è recente.
5. I materiali per le scuole comprendono fasce d'età, durata, istruzioni e collegamenti ai percorsi. Gli esperimenti esaminati descrivono anche i limiti del modello e la presenza dell'adulto.
6. L'offerta di lettura facile, voce, LIS, comunicazione aumentativa e sintesi tradotte aumenta le possibilità di accesso. La sola presenza di questi supporti non dimostra la conformità complessiva.
7. Tutte le pagine HTML scansionate hanno un H1, lingua dichiarata, descrizione e un canonical. Non sono state trovate immagini prive dell'attributo alt nell'HTML iniziale; non è stata verificata a vista la correttezza di ogni descrizione.
8. HTTP e dominio senza www conducono alla versione HTTPS con www. Una pagina volutamente inesistente restituisce 404. Sono attivi HSTS, nosniff, protezione da incorporamento e una Content Security Policy applicata dal server.

## 5. Rilievi da verificare e correggere

Priorità: P1 = errore con possibile conseguenza immediata grave; P2 = correzione necessaria; P3 = miglioramento o robustezza da aumentare. Non è stata accertata una criticità P1 nel perimetro esaminato. L'assenza di rilievi P1 non certifica l'assenza di vulnerabilità o errori negli ambiti non testati.

### R1 - Prestazioni della home sotto l'obiettivo dichiarato
- **Dove:** https://www.protezionecivilegenzano.it/ ; lighthouserc.json.
- **Che cosa non va:** il campione mobile dell'ultima esecuzione Lighthouse disponibile durante l'audit registra 76/100 per la home, rispetto alla soglia configurata di 85. I tre valori sono 73, 76 e 81. Il dato storico 95/100 nella dichiarazione non descrive questa misura recente.
- **Prova:** run 39026343083 del 17/10/2026, avviato alle 10:49 UTC; log del job 117377964568. La misura precede la build osservata alle 18:30: non è una nuova misurazione sulla build finale della sessione. Non sono disponibili qui dati reali sufficienti per giudicare i Core Web Vitals degli utenti.
- **Intervento suggerito:** misurare la build corrente, ridurre il codice comune e rinviare i componenti non necessari. Il bundle Bootstrap trasferisce circa 298 kB compressi nella richiesta esaminata; CSS Bootstrap circa 92 kB e CSS personalizzato circa 67 kB. Individuare il peso realmente inutilizzato prima di rimuovere codice.
- **Priorità:** P2.
- **Esito:** aperto: il peso della home va ridotto con una modifica dedicata.

### R2 - Un controllo Lighthouse verde non garantisce le soglie
- **Dove:** lighthouserc.json; .github/workflows/lighthouse-audit.yml; https://www.protezionecivilegenzano.it/stato-sistema/ .
- **Che cosa non va:** tutte e quattro le categorie sono configurate come warn. Il job può concludersi con successo anche sotto le soglie; il run di R1 ne è un esempio concreto. Le descrizioni che assimilano esito positivo e qualità raggiunta vanno rese più precise.
- **Prova:** configurazione letta e log dello stesso run: avviso per performance 0,76; conclusione del job success. Il riepilogo del workflow parla anche di errori per categorie che nel file sono solo avvisi.
- **Intervento suggerito:** separare esito di esecuzione, punteggi e rispetto delle soglie. Decidere quali regressioni devono bloccare e quali devono aprire una segnalazione.
- **Priorità:** P2.
- **Esito:** corretto nella PR #1460: il workflow Lighthouse apre una segnalazione quando un punteggio scende sotto soglia.

### R3 - Il campione accessibilità non copre i percorsi più complessi
- **Dove:** scripts/axe-gate.js; .github/workflows/pa11y-ci.yml.
- **Che cosa non va:** il gate visita 11 pagine ed esclude mappe Leaflet, iframe e dialog. Non esercita i passaggi dell'assistente, le lezioni generate, i filtri dei cataloghi o i giochi. Gli incomplete richiedono una valutazione, non sono automaticamente falsi positivi.
- **Prova:** elenco PATHS ed EXCLUDE nello script. Il run 39033056546, riferito alla PR #1439, riporta zero violazioni automatiche e 232 incomplete. È un controllo di una proposta di modifica, non una certificazione dell'intero sito pubblico.
- **Intervento suggerito:** aggiungere scenari che aprano i dialog, compongano una lezione e usino almeno un gioco per famiglia. Tenere un registro della revisione manuale degli incomplete. Affiancare prove con TalkBack, NVDA o VoiceOver.
- **Priorità:** P2.
- **Esito:** in parte: la PR #1460 aggiunge il controllo bloccante dei ruoli ARIA sui pulsanti; il campione axe resta da estendere ai percorsi interattivi.

### R4 - I due comandi iniziali dell'assistente perdono il ruolo di pulsante
- **Dove:** https://www.protezionecivilegenzano.it/assistente/ ; themes/flavour-pcgenzano/layouts/assistente/list.html, funzione di rendering delle card.
- **Che cosa non va:** i due elementi button iniziali sono sovrascritti con role=listitem. Nell'albero di accessibilità osservato compaiono come contenitori della lista, mentre le scelte del passo successivo sono riconosciute come pulsanti.
- **Prova:** DOM dei comandi Sono in difficoltà ORA e Voglio informarmi; entrambi hanno button e role=listitem. Il comportamento è stato riprodotto nella pagina pubblica.
- **Intervento suggerito:** conservare la semantica nativa del pulsante e, se serve una lista, collocare ciascun pulsante dentro un elemento li. Verificare annuncio, tastiera, focus e nome accessibile.
- **Priorità:** P2.
- **Esito:** corretto nella PR #1460.

### R5 - La lezione composta non rispetta sempre la durata dei materiali
- **Dove:** https://www.protezionecivilegenzano.it/formazione/crea-la-mia-lezione/?classe=primaria-alta&minuti=45&tema=terremoto ; themes/flavour-pcgenzano/static/js/crea-lezione.js.
- **Che cosa non va:** nel test il racconto Il giorno della prova è collocato nella fascia 5-15 minuti, quindi 10 minuti, ma la stessa card dichiara una durata di 15 minuti. La scaletta continua a presentarsi come lezione di 45 minuti. Non compare un adattamento che spieghi quale parte usare.
- **Prova:** composizione eseguita nel browser con primaria III-V, 45 minuti, terremoto. Il codice filtra la durata soltanto per l'attività principale; il racconto non riceve quel filtro. L'esito può variare con il catalogo o con nuove combinazioni, ma la lacuna è presente nell'algoritmo.
- **Intervento suggerito:** rispettare le durate per ogni fase oppure dichiarare un estratto e la sua durata. Per il pop-up indicare anche quale tavola usare, poiché il materiale completo ne contiene 13.
- **Priorità:** P2.
- **Esito:** corretto nella PR #1460: ogni fase usa materiali che stanno nel suo tempo, oppure dichiara di usarne solo una parte.

### R6 - Orario del caldo incoerente nel libro pop-up
- **Dove:** https://www.protezionecivilegenzano.it/formazione/schede-stampabili/libro-popup-protezione-civile/#tav8 ; https://www.protezionecivilegenzano.it/rischi-prevenzione/ondate-di-calore/ .
- **Che cosa non va:** la tavola del libro indica 11-17; la pagina tematica indica 11-18. Il Ministero della Salute indica 11-18 nei consigli per le ondate di calore.
- **Prova:** confronto dei due testi pubblici e della pagina Dieci consigli utili del Ministero, verificata il 17 ottobre.
- **Intervento suggerito:** uniformare il riferimento e controllare le altre copie stampabili e i pacchetti. Questo rilievo riguarda la coerenza del consiglio durante le ondate di calore; non implica una soglia universale di sicurezza per ogni luogo e giornata.
- **Priorità:** P2.
- **Esito:** corretto nella PR #1460 in tutte le copie (articoli, pagine, giochi, libro pop-up, script e messaggi Telegram), con il dato nel registro dei dati canonici.

### R7 - Nel percorso gas il divieto sui telefoni è formulato in modo parziale
- **Dove:** https://www.protezionecivilegenzano.it/assistente/#gas ; themes/flavour-pcgenzano/layouts/assistente/list.html, nodo gas.
- **Che cosa non va:** il testo menziona il telefono fisso; non esplicita il cellulare. Il richiamo a chiamare una volta fuori è presente e corretto, ma il divieto specifico può far pensare che il cellulare costituisca un'eccezione.
- **Prova:** percorso riprodotto nel browser e confronto con il vademecum dei Vigili del Fuoco, che comprende telefoni fissi e cellulari tra gli apparecchi da non utilizzare nel locale interessato.
- **Intervento suggerito:** formulare un unico divieto comprensibile e mantenere la chiamata al 112 da un luogo sicuro. Non cambiare automaticamente i numeri locali prendendoli da vecchi opuscoli nazionali.
- **Priorità:** P2, chiarimento di autoprotezione.
- **Esito:** corretto nella PR #1460 nell'assistente e nella pagina delle idee sbagliate.

### R8 - Poster e manuale hanno barriere documentali confermate
- **Dove:** /poster-emergenza-multilingua/poster-emergenza-it.pdf ; /manuali/manuale-protezione-civile.pdf .
- **Che cosa non va:** nel poster italiano non è estraibile alcun testo e mancano albero di struttura e lingua. Il manuale ha testo estraibile e lingua italiana, ma non ha l'albero di struttura. Il sito dichiara già questi limiti: resta un lavoro da completare.
- **Prova:** lettura strutturale dei PDF scaricati: poster una pagina e zero caratteri estratti; manuale 127 pagine e 222.827 caratteri estratti, senza StructTreeRoot. Le alternative HTML sono una mitigazione utile, non rendono accessibile il PDF stesso.
- **Intervento suggerito:** iniziare dai materiali urgenti e più usati, con testo reale, struttura, ordine di lettura e alternative per le figure. Verificare il risultato con strumenti documentali e lettore di schermo.
- **Priorità:** P2.
- **Esito:** aperto: le barriere sono dichiarate nell'audit PDF; i documenti vanno rifatti.

### R9 - La classificazione verde dei PDF non dimostra accessibilità
- **Dove:** https://www.protezionecivilegenzano.it/accessibilita/audit-pdf/ ; scripts/audit-pdf-accessibilita.py, funzione verdict; /manuali/presentazione-struttura-sito.pdf .
- **Che cosa non va:** il verdetto ACCESSIBILE dipende da testo estraibile e presenza di tag, senza richiedere lingua corretta, titolo o verifica semantica. La presentazione indicata come accessibile ha lingua en-US pur essendo in italiano e non ha titolo nei metadati letti. Anche il modulo verde non ha titolo nei metadati letti.
- **Prova:** esame dello script e dei due file pubblici. La presentazione scaricata ha 71 pagine; l'inventario ne riporta ancora 68. La presenza di tag non prova la conformità PDF/UA e non garantisce che le immagini abbiano descrizioni utili.
- **Intervento suggerito:** usare etichette descrittive dei controlli passati e riservare il giudizio completo a una verifica ulteriore. Correggere lingua, titolo e inventario, quindi controllare struttura e lettura effettiva.
- **Priorità:** P2.
- **Esito:** corretto nella PR #1460: «accessibile» solo con testo, tag, titolo e lingua coerente; gli altri PDF ricercabili sono «parziale».

### R10 - Quattro PDF pubblicati mancano nell'inventario documentale
- **Dove:** data/audit-pdf.yaml; https://www.protezionecivilegenzano.it/accessibilita/audit-pdf/ .
- **Che cosa non va:** l'audit pubblico e la dichiarazione corrente si riferiscono a 62 PDF; il ramo principale contiene 66 PDF pubblicabili in static/. Quattro aggiunte sono già raggiungibili e non sono nel riepilogo.
- **Prova:** confronto dei percorsi dell'inventario con l'albero del repository e risposte HTTP 200 per: avviso volontari civici del 5 ottobre; determinazione 80; modulo di domanda relativo; determinazione G13519 sulla convenzione con i coordinamenti. I due PDF in riferimenti-interni/ sono esclusi dal conteggio 66.
- **Intervento suggerito:** rigenerare l'inventario dopo aggiunte e sostituzioni, aggiornarne le date e derivare da una fonte unica i riepiloghi pubblici. Controllare anche i PDF presenti su Aruba ma gestiti fuori dal repository.
- **Priorità:** P2.
- **Esito:** corretto nella PR #1460: l'inventario conta tutti i 66 PDF e un controllo bloccante confronta impronte e totale.

### R11 - Manca il collegamento alla dichiarazione formale AgID
- **Dove:** https://www.protezionecivilegenzano.it/accessibilita/ e footer.
- **Che cosa non va:** il sito dichiara che il deposito formale presso AgID non è ancora completato e rinvia al Comune quale ente titolare. Il solo link alla pagina iniziale di form.agid.gov.it non identifica una dichiarazione depositata.
- **Prova:** testo corrente della pagina. AgID indica la compilazione nell'applicazione ufficiale e la pubblicazione del link generato; il richiamo annuale 2026 indica il 23 settembre.
- **Intervento suggerito:** verificare lo stato con il Responsabile per la transizione digitale del Comune e pubblicare il collegamento specifico quando disponibile. Questo audit non ha accesso all'area del Comune e non accerta se un deposito esista altrove.
- **Priorità:** P2, coordinamento amministrativo prioritario.
- **Esito:** aperto: serve l'indirizzo della dichiarazione pubblicata su form.agid.gov.it.

### R12 - La gestione dell'invecchiamento dell'allerta non è uniforme
- **Dove:** /emergenza/ ; /allerta-stato/index.json ; /cruscotto/#panel-allerta ; themes/flavour-pcgenzano/layouts/shortcodes/pagina-emergenza-lite.html .
- **Che cosa non va:** la home verifica anche fonti live, il cruscotto segnala il dato pubblicato poco recente e la pagina leggera conserva l'ultimo stato se l'aggiornamento fallisce. Nello script della versione leggera non c'è una soglia di età che trasformi lo stato in non verificato; accetta solo un timestamp più nuovo del precedente.
- **Prova:** nello stato osservato, la home aveva una verifica live delle 18:36 mentre endpoint pubblicato e pagina leggera indicavano 12:51. Il cruscotto mostrava un avvertimento. Il livello era verde in tutte le viste: non è stato accertato un colore errato. La lacuna sulla scadenza è desunta dal codice, non da un guasto provocato in produzione.
- **Intervento suggerito:** condividere criteri di freschezza, validità temporale e messaggio non verificato; simulare fonte assente, timeout, dato oltre soglia e cambio di giorno in un ambiente di prova. Non confondere l'assenza di una verifica recente con l'assenza di pericolo.
- **Priorità:** P3, robustezza di una funzione critica.
- **Esito:** corretto nella PR #1460 per la pagina /emergenza/, che oltre le 6 ore dichiara l'allerta non verificata.

## 6. Miglioramenti consigliati

### C1 - Alleggerire senza cambiare automaticamente la politica di cache

Il server invia no-store anche per CSS, JavaScript e documenti. È una scelta esplicita del Gruppo del 12 settembre per rendere visibili le sostituzioni dei file. Non è una svista da correggere senza decisione editoriale. Il costo è il nuovo trasferimento di risorse a ogni visita. Prima ridurre bundle e caricamenti superflui; un'eventuale cache di asset con nomi versionati richiede una scelta consapevole e una verifica degli aggiornamenti.

### C2 - Restringere progressivamente la CSP

La protezione è attiva e include object-src none, base-uri self e frame-ancestors self. Restano unsafe-inline e unsafe-eval per gli script. Sono margini di rafforzamento, non prova di un attacco o di una vulnerabilità sfruttabile. Mappare le dipendenze prima di introdurre hash o nonce, verificando che cruscotto, mappe e stampa continuino a funzionare.

### C3 - Rendere più brevi gli ingressi ai contenuti estesi

L'archivio comunicazioni contiene circa 733 kB di HTML non compresso; la pagina degli esperimenti stima 34 minuti di lettura e quella dei percorsi 38. Sono risorse valide, ma l'accesso deve restare rapido. Usare i filtri e i percorsi già esistenti per offrire subito una scelta per età, tempo e obiettivo; valutare paginazione o dettaglio progressivo dove il contenuto iniziale è eccessivo. Non serve aggiungere un altro catalogo parallelo.

### C4 - Verificare le figure per comprensione, oltre che per assenza di errori

La tavola sul terremoto del libro pop-up è leggibile a schermo nel campione osservato, ma richiede di distinguere istruzioni per adulti, spiegazione e pezzo da costruire. Va provata con bambini e docenti reali. Il controllo automatico dell'alt e la corretta resa di un SVG non dimostrano che il gesto sia capito. Provare stampa A4 in bianco e nero, taglio, piega e lettura senza aiuto su un campione di ogni famiglia grafica.

### C5 - Completare il collaudo privacy e l'identità istituzionale

L'informativa distingue le fonti caricate automaticamente dai widget su clic e descrive memoria locale e statistiche. È una base positiva. Rimangono da verificare con il titolare ruoli, tempi reali dei log, condizioni del servizio statistico e richieste effettive delle singole pagine. Nessuna conclusione di piena conformità GDPR deriva dalla sola lettura dell'informativa. Rivedere inoltre i testi e i dati strutturati affinché descrivano in modo coerente l'articolazione comunale e l'iscrizione ETS.

## 7. Piano operativo a costo contenuto

| Ordine | Interventi | Criterio di chiusura |
| --- | --- | --- |
| 1 | R4, R5, R6, R7: comandi, tempi e indicazioni | Prove ripetibili nel browser e controllo delle copie derivate |
| 2 | R9, R10: giudizi PDF e inventario | 66 file censiti, metadati correnti, nessun bollino basato solo sui tag |
| 3 | R8: poster e documenti prioritari | Testo e struttura verificati, alternativa HTML sempre raggiungibile |
| 4 | R1, R2: prestazioni e lettura degli esiti | Nuova misura sulla build corrente; soglie ed esiti distinti |
| 5 | R3, R12: copertura e indisponibilità | Percorsi interattivi e scenari di fonte assente collaudati |
| In parallelo | R11: deposito e collegamento AgID | Stato chiarito con il Comune e link specifico pubblicato |
| Successivamente | C1-C5: alleggerimento, hardening, usabilità | Verifiche su dispositivi e utenti reali, senza duplicare servizi |

Gli interventi di codice e contenuto possono usare gli strumenti già presenti. Il completamento della procedura amministrativa e i test con persone reali richiedono la collaborazione dei referenti competenti; non sono risolvibili con una sola modifica tecnica.

## 8. Limiti da mantenere espliciti

- La scansione completa è tecnica. Non è stata effettuata una revisione umana integrale del testo e della resa grafica di ogni pagina, figura e stampa.
- Non è stato eseguito in questa sessione un nuovo Lighthouse completo né un nuovo axe completo: sono stati letti log esistenti e svolte prove dirette mirate. Le date e le revisioni sono indicate nei rilievi.
- Non sono stati completati test su smartphone fisici, zoom al 400%, tutti i browser o lettori di schermo reali. La misura mobile citata è di laboratorio.
- Non sono stati verificati esaustivamente tutti i link esterni, i download derivati, i contenuti audio/video, tutti i giochi o tutti i 66 PDF. Le prove su quattro PDF non vengono estese automaticamente agli altri.
- Non sono stati ispezionati account Aruba, contratti, backup ripristinabili, pannelli privati, statistiche Search Console, dati CrUX o impostazioni dei fornitori. Nessun penetration test o prova di carico è stato effettuato.
- La presenza dell'alt, di un canonical o di tag PDF non prova da sola qualità, indicizzazione, leggibilità o conformità. Un'alternativa HTML deve essere anche pertinente e completa, non soltanto esistente.
- Le bozze delle PR #1439 e #1440 sono lavori separati: non sono state considerate funzionalità già pubblicate né difetti del sito corrente.

## 9. Riferimenti e riproduzione

Le prove HTTP e le letture dei file hanno usato gli indirizzi pubblici al momento dell'audit. Le copie indicizzate dai motori possono essere più vecchie della pagina scaricata direttamente.

- Sitemap: https://www.protezionecivilegenzano.it/sitemap.xml
- Dichiarazione locale: https://www.protezionecivilegenzano.it/accessibilita/
- Audit PDF: https://www.protezionecivilegenzano.it/accessibilita/audit-pdf/
- Stato del sito: https://www.protezionecivilegenzano.it/stato-sistema/
- Privacy: https://www.protezionecivilegenzano.it/privacy/
- Metodo editoriale: https://www.protezionecivilegenzano.it/metodo-editoriale/
- Ricerca e aree di attesa: https://www.protezionecivilegenzano.it/cerca/ ; https://www.protezionecivilegenzano.it/aree-attesa/
- Scuole: https://www.protezionecivilegenzano.it/scuole/
- Esperimenti: https://www.protezionecivilegenzano.it/formazione/esperimenti/
- Percorsi: https://www.protezionecivilegenzano.it/formazione/percorsi-didattici/
- Lighthouse, run letto: https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions/runs/39026343083
- Axe, run letto sulla PR: https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions/runs/39033056546
- AgID, procedura: https://www.agid.gov.it/it/design-servizi/accessibilita/dichiarazione-accessibilita
- AgID, richiamo 2026: https://www.agid.gov.it/it/notizie/dichiarazione-di-accessibilita-pubblicazione-o-aggiornamento-entro-il-23-settembre
- Ministero della Salute, caldo: https://www.salute.gov.it/new/it/tema/ondate-di-calore/dieci-consigli-utili/
- Vigili del Fuoco, vademecum, sezione fuga di gas: https://www.vigilfuoco.it/sites/default/files/2024-07/ita_vademecum.pdf
- W3C, focus non coperto: https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum

## 10. Consegna e coordinamento

Questo documento registra i rilievi secondo il formato di riferimenti-interni/audit-esterni/README.md. Le correzioni richiedono una successiva verifica e una propria proposta di modifica. Il campo Esito resta a disposizione di chi le esegue.

COORDINAMENTO.md non viene modificato in questa consegna: è già coinvolto nelle PR aperte #1439 e #1440. La descrizione della proposta di audit segnala il rapporto e il motivo della mancata modifica alla bacheca, evitando sovrapposizioni. Nessun file del sito pubblico è stato corretto o pubblicato da questo audit.
