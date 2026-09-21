# Audit interno del sito — 21 settembre 2026 — snapshot ca6b197

Esito: 15 rilievi (P1: 4 · P2: 5 · P3: 6) · corretti fino a live in questo run: 12 · da validare esternamente: 3 · workflow/documentazione allineati: 6

Audit mensile completo (routine `trig_01RMQwDs5Ku2mRfkwkDZnKmx`). Perimetro coperto: build e script deterministici, più 9 agenti specialisti in parallelo (fatti, conformità legale, automazioni, coerenza trasversale, sicurezza, documentazione, dati aperti, cronaca/deontologia, traduzioni/accessibilità) e un gate AGID finale sugli articoli corretti. A differenza dell'audit del 15/09 (solo diagnostico), questo run **corregge fino a live** quanto rientra in manutenzione ordinaria (Categoria A), lasciando come "da validare" solo ciò che richiede una decisione o un accesso non automatizzabile.

## Bloccanti in testa

**F01 — Il pacchetto blackout consigliava le candele, contro il divieto esplicito della pagina rischio canonica.** Vedi sotto. Corretto.
**F02 — Una frase non verificabile su un volontario deceduto era stata aggiunta all'articolo sull'alluvione Marche 2022.** Vedi sotto. Rimossa.
**F03 — L'articolo sulla chiusura della campagna AIB dava per corretta la data sbagliata (30 settembre invece di 15 ottobre).** Vedi sotto. Corretto.
**F04 — Il bilancio dell'alluvione di Livorno 2017 era sbagliato (9 vittime invece di 8) e citava un torrente inesistente.** Vedi sotto. Corretto.

## Rilievi

### F01 · Contraddizione: il kit/articoli blackout ammettevano le candele, la pagina rischio le vieta  P1
Tipo: difetto confermato — **corretto fino a live**
Prova: `content/rischi-prevenzione/blackout.md` vieta esplicitamente le candele ("Usa torce elettriche, non candele — rischio incendio"). Tre file le presentavano invece come opzione accettabile: `content/comunicazioni/2026-05-06-blackout-interruzione-corrente-cosa-fare.md` ("Candele solo con contenitori stabili e lontano da tende o carta"), `content/comunicazioni/2026-08-07-blackout-estivi-come-affrontarli.md` e la sua versione facile ("una candela solo come ultima risorsa").
Impatto: un cittadino che legge un solo articolo del sito riceve un'indicazione di autoprotezione opposta a quella della pagina rischio ufficiale — proprio il tipo di contraddizione su un rischio reale (incendio da fiamma libera) che il gate di coerenza trasversale esiste per intercettare.
Correzione: le tre occorrenze riformulate in linea col divieto assoluto ("Mai candele: usa solo torce elettriche/a pile o lampade a LED"), stile e registro preservati (AGID nei due standard, CEFR A2 nella facile). Verificata anche l'assenza di residui di contraddizione nella sezione "Cosa NON fare" dell'articolo del 6 maggio (gate finale).
Verifica di chiusura: `grep -rn "candela" content/comunicazioni/2026-05-06-blackout* content/comunicazioni/2026-08-07-blackout*` non deve più restituire indicazioni difformi dal divieto.
Fonti: `content/rischi-prevenzione/blackout.md`; i tre file citati.

### F02 · Dettaglio non verificabile ("un volontario deceduto") aggiunto a un articolo su una tragedia reale  P1
Tipo: difetto confermato — **corretto fino a live**
Prova: `content/comunicazioni/2026-09-15-alluvione-marche-2022-bombe-acqua-cambiamento-climatico.md` conteneva la frase "Tra le vittime si contò anche un volontario intervenuto per soccorrere chi era rimasto intrappolato nelle case allagate". Verificata la fonte primaria già citata nello stesso articolo (CNR-IRPI Polaris, ricostruzione dettagliata delle 13 vittime dell'alluvione): nessuna delle vittime è un volontario deceduto in soccorso.
Impatto: violazione diretta del principio NO INVENZIONI su un evento con morti reali — il caso più delicato in assoluto per la deontologia giornalistica del sito (stesso principio del precedente Rigopiano che ha originato il gate `pc-desk-giornalistico`).
Correzione: frase rimossa. Nello stesso giro corretti anche due dati imprecisi rispetto a fonte (Wikipedia, infobox sourced): sfollati "centinaia" → **circa 150**; danni "decine di milioni di euro" → **~2 miliardi di euro** (sottostima di due ordini di grandezza).
Verifica di chiusura: `grep -n "volontario" content/comunicazioni/2026-09-15-alluvione-marche-2022*.md` non deve restituire riferimenti a vittime tra i volontari.
Fonti: CNR-IRPI Polaris ("15 settembre 2022: le vittime dell'alluvione nelle Marche"); Wikipedia (infobox sourced).

### F03 · Data di chiusura della campagna AIB Lazio invertita rispetto alla fonte regionale  P1
Tipo: difetto confermato — **corretto fino a live**
Prova: `content/comunicazioni/2026-09-28-chiusura-stagione-aib-lazio.md` (programmato, in uscita fra 7 giorni) affermava che il 30 settembre termina il periodo di grave pericolosità AIB nel Lazio, e che l'ordinanza comunale n. 14 di Genzano lo "estenderebbe" al 15 ottobre. Verificato su fonte Regione Lazio (comunicato "Campagna Antincendio Boschivo 2026": periodo 15 giugno–15 ottobre) e per riscontro incrociato su 4 ordinanze sindacali di altri Comuni del Lazio, tutte con lo stesso periodo regionale 15/6–15/10.
Impatto: l'articolo avrebbe pubblicato un termine legale regionale falso — un cittadino o un altro Comune che si fidasse dell'articolo penserebbe che lo stato di grave pericolosità cessi 15 giorni prima del reale, con possibili conseguenze su comportamenti di prevenzione in un periodo che resta ad alto rischio.
Correzione: titolo, description, corpo (sezioni "Dichiarazione dello stato" e "Presidio sul territorio") riallineati: il termine regionale **è** il 15 ottobre, l'ordinanza comunale lo recepisce, non lo estende. Verificato con gate finale: zero residui del "30 settembre" nel file.
Verifica di chiusura: `grep -n "30 settembre" content/comunicazioni/2026-09-28-chiusura-stagione-aib-lazio.md` deve dare 0 risultati.
Fonti: Regione Lazio (comunicato Campagna AIB 2026); Consiglio Regionale Lazio (proroga Piano AIB, seduta 21/07/2026); 4 ordinanze comunali di riscontro.
Nota: l'articolo resta programmato con `date: 2026-09-28`, 17 giorni prima della scadenza reale — più in anticipo del solito per questo tipo di contenuto. Segnalato per un'eventuale revisione editoriale della data di pubblicazione (non modificata in questo audit: è una decisione di scheduling, non un fatto da correggere).

### F04 · Bilancio e torrenti sbagliati nell'articolo sull'alluvione di Livorno 2017  P1
Tipo: difetto confermato — **corretto fino a live**
Prova: `content/comunicazioni/2026-09-20-alluvione-livorno-2017-memoria.md` riportava **9 vittime** e citava tre torrenti (Rio Maggiore, Rio Ardenza, "Rio Ugione" nel corpo; "Rio Banditella" nella didascalia — incoerenti fra loro). Verificato su fonte primaria (Wikipedia, dati sourced, confermati via scraping diretto): le vittime dell'alluvione del 9-10 settembre 2017 sono **8**, i corsi d'acqua esondati sono **due**, Rio Maggiore e Rio Ardenza. "Rio Ugione" non è un corso d'acqua del bacino livornese.
Impatto: un articolo di memoria su un evento con vittime reali riportava un bilancio sbagliato e un dettaglio geografico inventato — stesso principio di F02.
Correzione: bilancio e nomi dei torrenti allineati alla fonte in tutti i punti del file (corpo, didascalia foto, `description` del frontmatter). Verificato con gate finale: nessuna incoerenza residua da lavorazione parallela di più agenti sullo stesso file.
Verifica di chiusura: `grep -n "Rio Ugione\|Rio Banditella\|9 vittime" content/comunicazioni/2026-09-20-alluvione-livorno-2017-memoria.md` deve dare 0 risultati.
Fonti: Wikipedia ("Alluvione di Livorno del 2017", infobox sourced).

### F05 · Cassetta di primo soccorso attribuita alla norma sbagliata  P2
Tipo: difetto confermato — **corretto fino a live**
Prova: `content/comunicazioni/2025-03-10-cucina-emergenza-haccp-ruoli-volontari.md` attribuiva il contenuto minimo della cassetta di primo soccorso "tipo B" direttamente al D.Lgs. 81/2008. Il contenuto minimo è fissato dal **D.M. 388/2003, Allegato 1**, emanato in attuazione dell'art. 45 del D.Lgs. 81/2008.
Correzione: corpo e sezione "Riferimenti" aggiornati con la citazione corretta (D.M. 388/2003, in attuazione dell'art. 45 D.Lgs. 81/2008).
Verifica di chiusura: il file cita esplicitamente D.M. 388/2003 accanto al D.Lgs. 81/2008.
Fonti: Normattiva (D.Lgs. 193/2007, D.Lgs. 81/2008 — testi vigenti verificati).

### F06 · Data della petizione alla CEI sbagliata nell'articolo su San Pio patrono dei volontari  P2
Tipo: difetto confermato — **corretto fino a live**
Prova: `content/comunicazioni/2026-09-23-san-pio-patrono-volontari-festa.md` (programmato) datava la petizione delle associazioni di volontariato "settembre 2002". Verificato su documento ufficiale CEI (chiesacattolica.it, testo del decreto del 21 febbraio 2004): la petizione fu presentata il **24 settembre 2000**.
Correzione: data corretta, resta coerente con il decreto del 21/02/2004 citato subito dopo.
Fonti: Chiesa Cattolica Italiana (CEI), documento ufficiale del decreto; riscontro indipendente su fonte diocesana.

### F07 · Gap di accessibilità: 8 poster di emergenza multilingua senza alcun equivalente testuale  P2
Tipo: difetto confermato — **corretto fino a live**
Prova: `check-integrita-asset.py --pdf-report` ha rilevato che tutti gli 8 PDF di `static/poster-emergenza-multilingua/` (it/en/fr/de/es/pt/ro/eo) hanno zero testo estraibile e nessun tag PDF/UA — sono immagini pure, illeggibili da screen reader. Non esisteva alcuna pagina HTML equivalente, nonostante la regola lo preveda (rule 03).
Correzione: creata `content/poster-emergenza/_index.md`, con il testo di tutti e 8 i poster (fonte: `scripts/poster_emergenza_i18n.json`, lo stesso dataset usato dal generatore grafico — zero rischio di trascrizione imprecisa), blocchi `lang="xx"` per le 7 lingue non italiane (WCAG 3.1.2). Aggiunta voce nel menu "Accessibilità e Supporti" (`hugo.toml`, `site-chrome.js` rigenerato), in `content/mappa-sito/_index.md` e linkata da `content/area-download/_index.md` (nuova colonna "Testo accessibile" nella tabella dei poster).
Verifica di chiusura: `/poster-emergenza/` risponde 200 con le 8 sezioni; menu e mappa del sito la raggiungono; build Hugo pulita.
Residuo P2 non risolvibile in automatico: i PDF restano immagini pure (richiederebbe riscrivere `genera-poster-emergenza.py` con una libreria PDF/UA-capable) — la pagina HTML è l'equivalente testuale richiesto dalla regola, il PDF stampabile resta un secondo canale.
Fonti: `.claude/rules/03-accessibility.md`; `scripts/poster_emergenza_i18n.json`.

### F08 · Superficie XSS: dati esterni (INGV, ItaliaMeteo) inseriti in innerHTML senza escape su 3 shortcode del cruscotto  P2
Tipo: difetto confermato — **corretto fino a live**
Prova: `dashboard-terremoti.html`, `scheda-terremoto.html` e `dashboard-italiameteo-osservazioni.html` inserivano campi provenienti da API esterne (nome località INGV, agencyID/tipo magnitudo QuakeML, nome stazione ItaliaMeteo) direttamente in `innerHTML`/`bindPopup()` senza escape, in 7 punti totali.
Impatto: rischio basso in pratica (fonti HTTPS istituzionali verificate) ma violazione del principio "nessuna terza parte scrive HTML per noi"; `dashboard-ems.html` e la Sala situazioni avevano già il pattern corretto, preso a modello.
Correzione: aggiunta funzione `escapeHtml()` locale (stesso pattern già in uso altrove) e applicata ai 7 punti di inserimento. Build Hugo verificata pulita dopo la modifica.
Verifica di chiusura: i 3 file usano `escapeHtml()` su ogni campo esterno inserito in markup.
Fonti: `.claude/rules/05-github-aruba-deploy.md` (CSP/hardening); diff dei 3 shortcode.

### F09 · Dichiarazione di accessibilità e pagina di audit PDF ferme al 14/15 settembre, a 2 giorni dalla scadenza del 23  P2
Tipo: difetto confermato — **corretto fino a live** (per la parte automatizzabile)
Prova: `content/accessibilita/_index.md` e `content/accessibilita/audit-pdf.md` dichiaravano "51 PDF, stato al 14 settembre", ma il sito ne conta oggi 54 (3 nuove ordinanze comunali). La scadenza AgID del riesame annuale (23 settembre) cade fra 2 giorni.
Correzione: rieseguito `scripts/audit-pdf-accessibilita.py --write` (dataset aggiornato: 54 PDF, 35 nostri/19 di terzi), aggiornati testo e `dataUltimaRevisione` delle due pagine al 21 settembre. Corretta anche una frase autocontraddittoria in `content/privacy/_index.md` ("non raccoglie dati personali oltre a quelli tecnici" vs. il trasferimento credenziali ad ActivePager descritto poco sotto) e aggiornata `content/social-media-policy/_index.md` per riflettere la pubblicazione social automatica attiva dal 20/09 (assente dal testo, fermo al 6/05).
Residuo da validare esternamente: **`dichiarazioneAccessibilita` in `hugo.toml` resta vuoto** — il deposito su `form.agid.gov.it` richiede login istituzionale del referente del Gruppo, non automatizzabile. Tracciato dall'issue GitHub #995 (aperta, aggiornata). Anche la base giuridica del trasferimento dati ad ActivePager (art. 6.1.b vs 6.1.e GDPR) resta un'interpretazione da confermare col RPD del Comune, non un errore manifesto.
Fonti: `data/audit-pdf.yaml`; issue #995; `.claude/rules/03-accessibility.md`.

### F10 · Sintesi grafica del dossier clima sovrastimava la frequenza dei giorni roventi rispetto al proprio dataset  P2
Tipo: difetto confermato — **corretto fino a live**
Prova: `content/dossier/il-clima-che-cambia-i-rischi.md`, sezione "roventi": l'alt-text diceva "barre comparse quasi ogni anno dal 2017". Il dataset citato come fonte (`clima-giorni-molto-caldi-genzano.json`) mostra 4 anni su 9 (2018, 2019, 2021, 2025) con **zero** giorni ≥35°C anche dopo il 2017.
Correzione: riformulato in "comparse a intermittenza dal 2017, in circa metà degli anni successivi" — fedele al dato citato. Le altre due affermazioni numeriche della stessa sezione (media luglio, range di pioggia annua) erano già corrette.
Fonti: `static/open-data/clima-giorni-molto-caldi-genzano.json`.

### F11 · Due snapshot della Sala situazioni (EMS, GDACS) fermi da ore/giorni per throttling dello scheduler GitHub, non per un guasto  P2
Tipo: diagnosticato, non ancora corretto (richiede una decisione infrastrutturale)
Prova: verificato con fetch diretto che le API Copernicus EMS e GDACS rispondono regolarmente; i log dei run di `aggiorna-dati-sala.yml` mostrano job sempre `success`, script corretti (nessun errore, nessun 403/timeout). La causa reale: il cron ogni 15 minuti (96 trigger/giorno attesi, il più denso di tutto il repo) viene onorato da GitHub Actions solo ogni 2-5 ore in pratica — comportamento "best effort" documentato di GitHub per gli eventi `schedule` sotto carico.
Impatto: gli snapshot restano più stantii di quanto la documentazione (rule 10) lasci intendere ("~15-20 minuti"); il dato EMS specifico risulta comunque davvero invariato dal 18/09 (nessuna nuova attivazione), quindi nessun danno concreto oggi.
Raccomandazione (non applicata in questo audit — cambierebbe un meccanismo infrastrutturale, non manutenzione ordinaria): allineare la cadenza attesa nella documentazione alla realtà di GitHub Actions, oppure spostare il trigger su un servizio esterno affidabile come già fa `check-allerta.yml` con cron-job.org.
Fonti: log dei run di `aggiorna-dati-sala.yml`; fetch diretto delle due API.

### F12 · Host CSP morto (`*.arpalazio.gov.it`), mai usato — l'host reale è un altro dominio  P3
Tipo: raccomandazione
Prova: `themes/flavour-pcgenzano/static/.htaccess` include `https://*.arpalazio.gov.it` in `connect-src`, ma il fetch reale per l'aria regionale usa `qa.arpalazio.net` (dominio diverso, via `img.src`, già coperto dal wildcard `img-src https:`).
Correzione proposta (non applicata: rimuovere un host da una policy attiva non è "a basso rischio" senza controprova aggiuntiva): eliminare la voce morta alla prossima revisione della CSP.
Fonti: diff CSP; grep dei fetch del cruscotto.

### F13 · Documentazione degli agenti disallineata dal numero reale di file (34 agenti, non tutti censiti in 3 punti)  P3
Tipo: difetto confermato — **corretto fino a live**
Prova: `manuale/parte-19-agenti-specializzati.md` §19.1 aveva un buco di numerazione (16→17 mancanti: `pc-revisore-linguistico`, `pc-materiali-publisher` non narrati) e §19.4 elencava solo 24/34 agenti in tabella; `AGENTS.md` §7 mancava `pc-correttore-bozze` e citava ancora "17 agenti (19/08)"; `manuale/README.md` citava "16 agent custom" con elenco incompleto.
Correzione: le 4 fonti riallineate a 34/34 agenti coerenti, `CONTESTO-PROGETTO.md` rigenerato.
Fonti: confronto diretto `.claude/agents/*.md` vs le 4 fonti documentali.

### F14 · `check-refusi.py` e `audit-grammatica-italiana.py` producono falsi positivi su contenuti multilingua e blob base64  P3
Tipo: raccomandazione (tooling, non un difetto del sito pubblicato)
Prova: lo sweep completo di `check-refusi.py` segnala ~1250 "parole sospette" da un'unica stringa base64 embedded in `static/formazione/kit-calamita-bambini/12-unisci-puntini-casco.html` (già noto, F05 dell'audit del 15/09, non ancora corretto nello script); la nuova pagina `/poster-emergenza/` (creata in questo audit) genera ulteriori falsi positivi attesi (parole in 7 lingue diverse dall'italiano) sia in `check-refusi.py` sia in `audit-grammatica-italiana.py` (che ha segnalato "una emergencia" come elisione italiana mancante, quando è spagnolo corretto dentro un blocco `lang="es"`).
Impatto: nessuno sul sito pubblico; rischio che un refuso vero si perda nel rumore di un report che continuerà a crescere ogni volta che si aggiunge contenuto multilingua.
Raccomandazione: escludere dal tokenizzatore i blocchi `<div lang="...">` con lingua diversa da `it`/assente, e le stringhe alfanumeriche lunghe senza spazi (pattern base64).
Fonti: output degli script; `content/poster-emergenza/_index.md`.

### F15 · Issue GitHub #1069 (watchdog smoke-test) rimasta aperta dopo il rientro del problema  P3
Tipo: difetto confermato — **chiuso in questo run** (non è una modifica al sito, solo igiene del tracker)
Prova: lo smoke-test del 20/09 era fallito per un drift temporaneo di propagazione FTP su Aruba (status `000`/timeout, non 404); il run successivo (16 minuti dopo) era tornato verde, confermato anche dalla guardia anti-stale. La issue gemella #1068 (aperta dallo stesso smoke-test) si era auto-chiusa; la #1069, aperta dal watchdog `notifica-ci-fallita.yml`, non ha logica di auto-chiusura ed era rimasta aperta senza commenti.
Correzione: commentata con la diagnosi e chiusa.
Fonti: log dei run GitHub Actions citati nel commento di chiusura.

## Confermati senza modifiche (controlli superati)

- Build Hugo, integrità di tutti i 4.790 file statici, ancore interne (4.764 verificate), parità pacchetti "Stampa tutto" ↔ kit ↔ ZIP (290 schede, 4 fasce), coerenza tabelle-dataset, blocchi JSON-LD (paternità presente ovunque nel campione), sincronia menu `hugo.toml` ↔ `site-chrome.js`.
- 48 workflow GitHub Actions: YAML validi, timeout su ogni job, action di terzi pinnate a SHA, permessi minimi, anti-loop dei commit automatici, modello di priorità del deploy rispettato, nomi del watchdog allineati.
- Nessun segreto né dato personale nel repository; header di sicurezza (HSTS, Permissions-Policy con `geolocation=(self)` intatto, X-Content-Type-Options) tutti presenti e corretti.
- Numeri di emergenza, dati istituzionali (COI, Quality Label ESC + E10435833, FEPIVOL, SNPC), nomi tecnici dei mezzi: coerenti ovunque compaiono, incluse le 7 traduzioni.
- Articoli di cronaca della settimana 12-21/09 (interventi alberi/rami, giornata aggiornamento volontari, esercitazione nazionale, convenzioni PC): nessuna criticità deontologica. **Verifica esplicita sulla "Festa del Pane"**: nessuna attribuzione impropria di viabilità al Gruppo, disclaimer normativo (Circolare DPC 6/8/2018) presente in entrambi gli articoli.
- Traduzioni `/cosa-fare-adesso/` nelle 7 lingue: numeri e azioni di autoprotezione identici all'italiano canonico.
- 18 dataset in `static/open-data/` + 25 file in `data/`: JSON/YAML validi, coerenza CSV↔JSON, nessun dato personale. Segnalati come miglioria futura (non bloccante): 4 dataset senza blocco metadati embedded nel file stesso (licenza/fonte solo nella pagina HTML).
- Rilievi F02 (refuso "pop-updella" nei pacchetti primaria) e F03 (ordine sezioni pagina rischio vulcanico) dell'audit del 15/09: **risolti** nel frattempo, verificato in questo giro. F07 dell'audit del 15/09 (sigle MTG/ASI/APS mancanti dal glossario): **risolto**.

## Da validare esternamente (responsabile umano)

1. **Dichiarazione di accessibilità su `form.agid.gov.it`** — referente del Gruppo, entro il 23 settembre 2026 (issue #995, aperta).
2. **Base giuridica del trasferimento dati ad ActivePager** (art. 6.1.b vs 6.1.e GDPR) — RPD del Comune.
3. **Mappatura completa PDF→HTML equivalente** per le 9 presentazioni tematiche rimanenti nella pagina `/accessibilita/audit-pdf/` (rilievo F04 dell'audit del 15/09, ancora aperto): richiede verifica puntuale pagina per pagina, riservata a una sessione editoriale dedicata.

## Non applicate per scelta esplicita (fuori mandato di manutenzione ordinaria)

- F11 (cadenza reale del cron Sala situazioni) e F12 (host CSP morto): entrambe raccomandazioni tecniche che richiedono una decisione infrastrutturale, non un fix "a basso rischio" da applicare in automatico durante un audit di manutenzione.

## Metodo

Fase 1 (deterministica): build, `check-integrita-asset.py`, `check-ancore.py`, `check-parita-schede.py`, `check-dati-schede.py`, `check-jsonld.py`, `check-refusi.py`, `audit-grammatica-italiana.py`, `check-freshness.py`, `check-articoli-programmati.py`, `check-fonti-cruscotto.py`, `genera-chrome-menu.py --check`, rigenerazione pacchetti "Stampa tutto" (diff vuoto), `verifica-fingerprint-live.sh`, `smoke-test-live.sh` — tutti eseguiti su Hugo 0.154.5 extended.

Fase 2: agenti specialisti in parallelo su perimetri delimitati (non l'intero sito, per contenere i tempi in un run mensile di manutenzione): `pc-fact-checker` (6 articoli segnalati da freschezza/programmazione), `pc-conformita-legale` (4 pagine legali + audit PDF), `pc-revisore-automazioni` (48 workflow), `pc-coerenza-trasversale` (numeri, autoprotezione, dati istituzionali, mezzi, eventi storici), `pc-sicurezza` (segreti, CSP, superficie JS), `pc-documentazione` (agenti, workflow, manuale), `pc-dati-e-feed` (open data e snapshot), `pc-desk-giornalistico` (11 articoli della settimana 12-21/09), `pc-revisore-traduzioni` (poster multilingua + spot-check traduzioni).

Fase 3: gate AGID finale (`pc-article-reviewer`) sui 9 articoli corretti dagli specialisti, con lettura integrale (non solo diff) e verifica di coerenza interna — ha trovato e corretto un'ultima incoerenza residua (F01, contraddizione candele non ancora sanata nella sezione "Cosa NON fare" di un articolo).

Fase 4: build finale pulita, ri-esecuzione dei controlli deterministici principali (ancore, JSON-LD, menu), commit unico, PR, merge, verifica deploy.
