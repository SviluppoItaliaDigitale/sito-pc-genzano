# Audit interno del sito — 3 ottobre 2026 — snapshot `f807cfa`

Esito: **23 rilievi** (P1: 6 · P2: 9 · P3: 8) · corretti in questo run (Categoria A, commit sul branch `claude/audit-interno-2026-10-03`): **16** · in PR separata (Categoria B): **0** · da validare esternamente o da decidere: **7** · rilievi aperti ereditati dagli audit precedenti: **9** (elencati in fondo con il loro numero originale)

Audit mensile **completo** (routine `trig_01RMQwDs5Ku2mRfkwkDZnKmx`). Snapshot di partenza `f807cfa` di `main` (3 ottobre 2026, ore 04 italiane); sito live verificato sulla build `be50f97` del 3 ottobre, ore 02:49. Il perimetro comprende tutti i controlli deterministici, la build locale con e senza i contenuti programmati, la revisione dei contenuti cambiati dopo l'audit esterno del 25/09 (5 articoli nuovi, 46 pagine e 80 file fra template, script e workflow) e dei 7 articoli in uscita entro il 17 ottobre, axe-core (WCAG 2.2 AA) su 24 pagine Hugo a 1280 e 375 px e su 413 schede stampabili e materiali dei kit, un'esercitazione locale della catena di allerta e la verifica del sito live contro il manifesto della build.

## Bloccanti in testa

**F01 — Per la terza volta in un mese, contenuti pubblicati dicevano che i divieti antincendio finivano il 30 settembre.** Gli audit del 21/09 e del 25/09 avevano corretto 7 articoli; ne restavano altri 11, più tre versioni facili e un gioco per la primaria, alcuni con il divieto di bruciare «fino al 30 settembre». Corretti tutti, e il dato ora sta nel registro canonico: una variante blocca la PR.
**F02 — L'anniversario dell'alluvione di Genova 1970, in uscita il 7 ottobre, aveva il bilancio delle vittime sbagliato** e un numero senza fonte («8.000 vittime indirette»). Corretto sul CNR-IRPI.
**F03 — L'articolo su Assisi 1997 collocava il crollo della volta, con quattro morti, «la mattina successiva» invece che la stessa mattina.** Corretto.
**F04 — L'anniversario del terremoto di Reggio Emilia 1996 (15 ottobre) aveva magnitudo, profondità e danni senza riscontro nel catalogo INGV.** Corretto su CPTI15.
**F05 — L'articolo sui diritti dei volontari lavoratori (12 ottobre) attribuiva il rimborso al «datore di lavoro autonomo» e semplificava male i limiti dell'art. 39 del Codice.** Corretto sul testo Normattiva.
**F06 — Una scheda per la secondaria presentava come «dati ISPRA» una serie inventata.** Ora è dichiarata come dato di esercizio, con il rimando alle fonti vere.

---

## Rilievi

### F01 · Fine del periodo di grave pericolosità AIB 2026 data al 30 settembre (o «1 giugno - 30 settembre») in 15 contenuti  P1
Tipo: difetto confermato — **corretto** (commit `aec3a4e1`)
Prova: `grep -rnE -i "giugno[^.]{0,40}30 settembre|fino al 30 settembre|al 30 settembre" content static/formazione static/giochi data` sul commit `f807cfa`. Fra gli altri: `content/comunicazioni/2026-09-09-quattro-incendi-falcognana-albano-genzano.md:20` («fino al 30 settembre accendere fuochi è vietato», in `social_punti`) e `:44`; `2026-09-07-lariano-incendio-bosco-quattro-ore.md:41` («fino al 30 settembre siamo nel periodo di massima pericolosità dichiarato dalla Regione Lazio»); `2026-04-23-prevenzione-incendi-pulizia-terreni-primavera-facile.md:36` («Dal 15 giugno al 30 settembre non puoi bruciare»); `2026-06-20-solstizio-estate-massima-attenzione-incendi.md:56` e facile `:32`, `2026-06-16-estate-boschi-castelli-escursionismo-sicuro.md:31` e facile `:37` («1 giugno - 30 settembre», nessuna fonte); `2026-06-16-ispra-incendi-2025-superficie-bruciata-prevenzione.md:65`; `2026-08-29-fine-estate-meteorologica-passaggio-autunno.md:31` («si chiude spesso a fine settembre», con un «DPGR Lazio» non citabile); `2026-09-27-sala-operativa-regionale-soup-803555.md:19,38` (la configurazione SOUP presentata come «periodo di massima pericolosità»); `static/giochi/primaria/cruciverba/js/puzzles.js:357`. Due articoli (`2026-06-30-bilancio-primo-mese-aib-2026.md:30`, `2026-07-04-turni-avvistamento-aib-come-funzionano.md:56`) davano la SOUP al 15 settembre.
Impatto: è la stessa famiglia dei rilievi F03 del 21/09 e F03 del 25/09, ed è rimasta aperta perché le correzioni cercavano frasi, non il dato. Chi legge oggi uno di quegli articoli pensa che dal 1° ottobre si possa bruciare sterpaglie senza autorizzazione, mentre l'ordinanza vale fino al 15 ottobre compreso.
Correzione: testo riallineato alla fonte primaria in tutti i file (gli articoli del 2025 restano, archiviati, perché raccontano la campagna di quell'anno; la versione facile del 2025 ora ha `archiviato: true` come la madre). Distinti i due dati: lo stato di grave pericolosità a Genzano (17 giugno - 15 ottobre 2026) e la configurazione SOUP della sala regionale (15 giugno - 30 settembre di ogni anno, secondo la pagina della Regione), con una frase che dice esplicitamente che la seconda non chiude i divieti. Nuova voce `aib-2026-grave-pericolosita` in `data/dati_canonici.yaml`, provata con un file di prova: intercetta «fino al 30 settembre» e «1 giugno - 30 settembre» accanto a incendi/fuochi/abbruciamenti, e lascia passare le frasi sulla SOUP.
Verifica di chiusura: `python3 scripts/check-dati-canonici.py` → «OK: 14 dati canonici, 1955 file controllati»; la grep sopra, esclusi gli articoli 2025 e le frasi sulla SOUP, non restituisce più nulla.
Fonti: Comune di Genzano, Ordinanza sindacale n. 14 del 17/06/2026, `static/area-download/normativa/Ordinanza_Sindacale_AIB_2026.pdf` (pagina 3: «con decorrenza dal 17 giugno 2026 al 15 ottobre 2026 è dichiarato lo stato di grave pericolosità»; richiama la DGR Lazio 228/2023, periodi di allerta «da metà giugno a metà ottobre»); Regione Lazio, pagina «Sala Operativa Regionale» (SOUP dal 15 giugno al 30 settembre di ogni anno).

### F02 · Genova, 7 ottobre 1970 (articolo in uscita il 7/10): bilancio e piogge sbagliati, un dato senza fonte  P1
Tipo: difetto confermato — **corretto** (commit `10ff23e9`)
Prova: `content/comunicazioni/2026-10-07-genova-1970-alluvione-storica-piu-grave.md:18` — «44 morti in città, 22 dispersi, 2.000 senzatetto, 8.000 vittime indirette di danni secondo i registri comunali dell'epoca»; `:16` — «oltre 900 millimetri di pioggia in 24 ore in alcune stazioni del bacino del Bisagno»; description «il rio Bisagno esondò, uccidendo 44 persone».
Impatto: errore fattuale sulle vittime di una tragedia, la categoria che ha originato il gate dei fatti. «22 dispersi» e «8.000 vittime indirette» non trovano riscontro in nessuna fonte; i 948 mm furono misurati a Bolzaneto, in Val Polcevera; le vittime furono causate anche dal Leira a Voltri (13), non dal solo Bisagno.
Correzione: bilancio del CNR-IRPI (35 morti, 8 dispersi, oltre 2.000 sfollati; 13 vittime a Voltri), pioggia attribuita alla stazione di Bolzaneto con l'indicazione che il dato è di una stazione amatoriale, torrenti elencati come nella fonte, superlativo attenuato («una delle alluvioni più gravi del Novecento ligure»), «versanti deforestati» tolto perché non documentato; aggiunta la scheda Polaris fra le fonti. Didascalie riallineate.
Verifica di chiusura: `grep -n "44\|22 dispersi\|8.000" content/comunicazioni/2026-10-07-genova-1970-*.md` → nessun risultato.
Fonti: CNR-IRPI, Polaris, «Genova e i suoi torrenti: una lunga storia di alluvioni, danni e vittime»; Wikipedia, «Alluvione di Genova del 7 ottobre 1970» (testo e infobox con fonti).
Nota: la fonte CNR scrive «44 vittime, di cui 35 morti e 8 dispersi», che sommati fanno 43 (come Wikipedia). Nell'articolo si usano i due addendi, non il totale.

### F03 · Assisi 1997: il crollo della volta, con quattro morti, collocato «la mattina successiva»  P1
Tipo: difetto confermato — **corretto** (commit `10ff23e9`)
Prova: `content/comunicazioni/2026-09-26-marche-umbria-1997-basilica-assisi.md:16` — «Alle 2:33 della notte del 26 settembre 1997 [...] Alle 11:40 della mattina successiva [...] crollare la volta della Basilica, schiacciando quattro persone». Lo stesso paragrafo attribuiva le riprese a «una troupe RAI».
Impatto: data sbagliata della morte di quattro persone in un articolo già pubblicato (26/09). Le riprese furono di Umbria TV.
Correzione: «Alle 11:40 della stessa mattina»; «riprese da un operatore di un'emittente umbra che si trovava nella basilica».
Verifica di chiusura: `grep -n "mattina successiva\|RAI" content/comunicazioni/2026-09-26-marche-umbria-1997-basilica-assisi.md` → nessun risultato.
Fonti: Wikipedia, «Terremoto di Umbria e Marche del 1997» (ora 11:40:24 del 26/09; vittime nella basilica; riprese di Umbria Tv).

### F04 · Reggio Emilia, 15 ottobre 1996 (in uscita il 15/10): magnitudo, profondità e danni senza riscontro  P1
Tipo: difetto confermato — **corretto** (commit `10ff23e9`)
Prova: `content/comunicazioni/2026-10-15-reggio-emilia-1996-terremoto-correggio-rischio-padano.md:4,16` — «magnitudo 4.9», «Profondità ipocentrale 27 chilometri», «circa 100 edifici dichiarati inagibili»; `:24` terremoti storici «1547, 1671, 1796, 1810 nella stessa zona»; `:28` «magnitudo 6.1 [...] esattamente nella stessa zona del 1996», mentre la didascalia della stessa pagina dice M 5.8; `:72` link a una voce Wikipedia che non esiste (404).
Impatto: dati scientifici sbagliati o non verificabili in un articolo che esiste proprio per correggere la percezione del rischio sismico padano.
Correzione: magnitudo momento 5,4 e intensità epicentrale VII MCS dal catalogo CPTI15 v4.0 (135 osservazioni macrosismiche); tolti profondità e inagibilità; terremoti storici ridotti a quelli presenti nel catalogo per l'area (1547, 1671, 1810); per il 2012 indicati i due valori, ciascuno con la sua fonte, e la distanza reale (Finale Emilia, circa 40 km a est); link Wikipedia sostituito con il catalogo INGV.
Verifica di chiusura: `curl "https://emidius.mi.ingv.it/services/macroseismic/query?starttime=1996-10-15&endtime=1996-10-16&format=text"` → evento 09:55:59 UTC, Mw 5.38, «Pianura emiliana»; `grep -n "4.9\|27 chilometri\|1796" <file>` → nessun risultato.
Fonti: INGV, CPTI15/DBMI15 v4.0 (servizio macrosismico ASMI); INGV FDSN, bollettino (evento 772691 del 20/05/2012, Mw 5.8).

### F05 · Volontari lavoratori (in uscita il 12/10): rimborsi e limiti esposti in modo non conforme all'art. 39 del Codice  P1
Tipo: difetto confermato — **corretto** (commit `10ff23e9`)
Prova: `content/comunicazioni/2026-10-12-volontariato-diritto-lavoratore-assenza.md:42-49` — «30/90 giorni per emergenze dichiarate», «prorogabili in casi eccezionali», rimborso solo al «datore di lavoro privato», «Il datore di lavoro autonomo [...] ha diritto a un rimborso forfettario»; `:52` copertura assicurativa «stipulata dal Gruppo, con oneri a carico della Regione o del Dipartimento»; fonte linkata = homepage del Dipartimento.
Impatto: informazione legale sbagliata rivolta a volontari e datori di lavoro: il rimborso spetta al datore pubblico o privato (anche come credito d'imposta), mentre al lavoratore autonomo spetta il mancato guadagno calcolato sul reddito, con un tetto giornaliero; l'innalzamento a 60/180 giorni ha condizioni precise.
Correzione: testo riscritto comma per comma (commi 1-5), con la condizione dell'attivazione formale e dell'iscrizione all'Elenco nazionale; fonte sostituita con l'articolo su Normattiva. Il tetto giornaliero non è riportato in cifra perché viene aggiornato ogni tre anni.
Verifica di chiusura: lettura del testo vigente `https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2018-01-02;1~art39` contro le righe 30-52 dell'articolo.
Fonti: D.Lgs. 2 gennaio 2018, n. 1, art. 39 (testo vigente, Normattiva).

### F06 · Scheda «Cambiamento climatico» (secondaria 2° grado): serie inventata attribuita all'ISPRA  P1
Tipo: difetto confermato — **corretto** in parte (commit `916531db`); il resto della scheda **da validare** (vedi F18)
Prova: `static/formazione/schede-stampabili/climate-change-secondaria2/index.html:138-139` — «numero di alluvioni significative documentate dall'ISPRA (Y, valori indicativi: 2010=8, 2013=14, ... 2023=37)»; `:130` Marmolada «+10 °C sulla cima rispetto alla media».
Impatto: è la classe di rilievi dell'audit esterno del 6/09 (esercizi che presentano ipotesi come dati ufficiali). Uno studente avrebbe citato come ISPRA una serie che l'ISPRA non pubblica. Per la Marmolada la fonte riporta 10 °C misurati in vetta, record della cima, non uno scarto di 10 °C dalla media.
Correzione: la serie è dichiarata «dati di esercizio, inventati per allenarsi a leggere una tendenza, non dati ufficiali», con il rimando al rapporto ISPRA «Dissesto idrogeologico in Italia» e al portale IdroGEO; Marmolada corretta. Pacchetti «Stampa tutto» e ZIP rigenerati.
Verifica di chiusura: `grep -rn "valori indicativi\|+10 °C sulla cima" static/formazione` (esclusi i pacchetti) → nessun risultato; `check-parita-schede.py` → parità completa; screenshot in stampa letto.
Fonti: Wikipedia, «Valanga della Marmolada» (temperatura record di 10 °C sulla cima il giorno prima, con fonte).

### F07 · Ustioni: tempo di raffreddamento di 10-15 o 15-20 minuti in 9 testi, contro i 20 della pagina canonica  P2
Tipo: difetto confermato — **corretto** (commit `10ff23e9`)
Prova: `content/formazione/primo-soccorso/emorragie-ustioni-traumi.md:58` e tutte le schede (`casa-una-scottatura-primaria`, `casa-sicura-guida-adulti`, …) indicano «almeno 20 minuti»; i testi difformi erano `2026-06-29-primo-soccorso-estivo-caldo-traumi.md:97` e facile `:108`, `2026-10-14-primo-soccorso-base-famiglie.md:41` e facile `:56`, `2026-11-24-sicurezza-cucina-festivita.md:124` e facile `:86`, `2026-12-30-capodanno-petardi-sicurezza.md:185` e facile `:89`.
Impatto: istruzione di primo soccorso diversa a seconda della pagina letta.
Correzione: «almeno 20 minuti» ovunque; nuova voce `ustione-raffreddamento` nel registro canonico (le ustioni chimiche e il lavaggio degli occhi restano fuori dalla regola). Limite noto: il controllo ragiona per frase, quindi una frase che dice «Metti acqua fresca per 15 minuti» sotto il titolo «Ustioni» non viene vista; per questo è stata fatta anche la grep `acqua[^.]{0,40}per (1|5|10|15)(-1[05]|-20)? ?min` su tutto il perimetro.
Verifica di chiusura: `python3 scripts/check-dati-canonici.py` → OK; la grep sopra restituisce solo l'ustione chimica dell'articolo di Santa Lucia.
Fonti: pagina canonica del sito (Linee guida IRC); Ospedale Pediatrico Bambino Gesù, «Bambini e incidenti: cosa fare nei primi 5 minuti».

### F08 · Iscrizione del Gruppo al RUNTS datata «fine 2023» nel dossier e nell'articolo sulla storia  P2
Tipo: difetto confermato — **corretto** (commit `10ff23e9`)
Prova: `content/dossier/il-nostro-gruppo.md:33` («Alla fine del 2023 [...] viene iscritto al RUNTS»); `content/comunicazioni/2026-04-05-storia-gruppo-comunale-volontari-genzano-quarant-anni.md:128` («Con l'entrata in vigore del Codice del Terzo Settore e l'iscrizione al RUNTS» nel paragrafo sul 2023). Note legali, trasparenza e Chi siamo dicono: determina n. G14230 del 28/10/2024.
Impatto: dato istituzionale incoerente fra pagine; l'articolo attribuiva inoltre al 2023 l'«entrata in vigore» di un decreto del 2017.
Correzione: dossier e articolo riportano il 28 ottobre 2024 e la determina; nel 2023 restano il nuovo Statuto, il Regolamento, Direttivo e Assemblea.
Verifica di chiusura: `grep -rn "RUNTS" content | grep 2023` → nessuna frase che dati l'iscrizione al 2023.
Fonti: `content/note-legali/_index.md:12`, `content/trasparenza/_index.md:12,22`.

### F09 · Psicologia dell'emergenza (in uscita il 10/10): riferimento normativo non verificabile  P2
Tipo: difetto confermato — **corretto** (commit `10ff23e9`)
Prova: `content/comunicazioni/2026-10-10-psicologi-emergenza-trauma.md:29` — «il Codice della Protezione Civile [...] riconosce il supporto psicologico tra le attività di soccorso, e le Linee Guida del CNOP sull'intervento psicosociale nelle emergenze»; glossario «CNOP — Riferimento normativo italiano».
Impatto: il Codice non nomina il supporto psicologico, le «Linee guida CNOP» citate non sono state trovate, e manca il documento che il Dipartimento indica come riferimento.
Correzione: citati i Criteri di massima sugli interventi psicosociali nelle catastrofi (2006), con link alla pagina del Dipartimento; il Codice resta come cornice delle attività di soccorso e assistenza; il CNOP descritto come ente di rappresentanza della professione.
Verifica di chiusura: lettura di `https://rischi.protezionecivile.gov.it/it/sanitario/attivita/` («Nel 2006 il Dipartimento [...] Criteri di massima sugli interventi psicosociali nelle catastrofi»).
Fonti: Dipartimento della Protezione Civile, «Rischio sanitario — Le attività».

### F10 · Schede stampabili e kit: contrasto e ARIA (axe-core, WCAG 2.2 AA)  P2
Tipo: difetto confermato — **corretto** per 23 pagine (commit `916531db`); residui in P3 (F20)
Prova: axe-core 4.10 su 413 pagine (`static/formazione/schede-stampabili/*`, `static/formazione/kit-calamita-*`) a 1280 px: 36 pagine con violazioni. Cause sistemiche nelle variabili condivise di `static/formazione/schede-stampabili/assets/scheda-print.css`: `--scheda-verde` #198754 sul verde dei box per il docente 3,49:1, `--scheda-rosso` #dc3545 sul rosa degli avvisi di sicurezza 4,23:1 (fra cui l'avviso sulla candela di `triangolo-fuoco-primaria`), `--scheda-grigio` #6c757d sui fondi chiari 4,36-4,42:1; bianco su giallo e arancione nelle etichette del triage SALT (`kit-calamita-strutture-sanitarie/08-triage-geriatrico-salt.html`, 2,93 e 3,55:1); `aria-label` su `div` senza ruolo in 7 aree di disegno; `role="grid"` senza righe né celle nella griglia di `cruciverba-primaria`.
Impatto: testo sotto soglia nei box rivolti all'adulto e negli avvisi di sicurezza; etichette lette in modo incoerente dagli screen reader.
Correzione: variabili scurite (#146c43, #b02a37, #5a6169: tutte oltre 4,5:1 sui fondi usati), come chiede la rule 03 (si alza la variabile, non il caso singolo); testo nero sulle etichette gialla e arancione; `role="img"` sulle aree di disegno e sulla griglia (come già nel cruciverba della secondaria); tre aree grafico e il magenta della scheda sui social corretti. Pacchetti rigenerati.
Verifica di chiusura: axe rieseguito sulle 36 pagine dopo la correzione → restano 20 pagine, tutte nel tipo descritto in F20; screenshot dell'avviso di sicurezza letto.
Fonti: WCAG 2.2, criteri 1.4.3 e 4.1.2; rule 03 § «Contrasto testo su sfondo colorato».

### F11 · Allerta impostata a mano: con il solo `livello` cambiato, barra e feed CAP dicono «NESSUNA ALLERTA» con colore e severità di un'allerta  P2
Tipo: difetto confermato nella procedura documentata — **corretto in rule 10** (commit `763b67f9`); **CLAUDE.md da allineare** (vedi «Da decidere»)
Prova: esercitazione locale: in `data/allerta.json` solo `livello: "arancione"`, build in `/tmp/pubE` → barra in homepage `class="allerta-bar allerta-bar-arancione"` con `<strong id=allerta-titolo>NESSUNA ALLERTA</strong>`; `allerta-cap.xml` con `<severity>Severe</severity>` e `<headline>NESSUNA ALLERTA</headline>`; `allerta-stato/index.json` con `livello: arancione` e `titolo: NESSUNA ALLERTA`. Il file è stato ripristinato subito dopo (`git status data/` pulito). La procedura manuale di `CLAUDE.md:477` e della rule 10 diceva di cambiare solo il `livello`.
Impatto: in un'allerta impostata a mano (caso raro, ma è proprio il caso in cui gli automatismi non bastano) il sito e il feed per gli aggregatori darebbero due messaggi contraddittori nello stesso riquadro.
Correzione: rule 10 § «Key operational notes» ora chiede di cambiare `livello`, `titolo` e `descrizione` nella stessa modifica e spiega perché. Raccomandazione aggiuntiva (non applicata, è una scelta di template): ricavare titolo e `<event>` del CAP dal livello quando il titolo è quello della condizione verde.
Verifica di chiusura: la stessa esercitazione con i tre campi coerenti produce barra, pagina lite e CAP concordi.
Fonti: `themes/flavour-pcgenzano/layouts/index.cap.xml`, `layouts/index.html` (barra), esercitazione del 3/10.

### F12 · Pacchetti ZIP dei kit scolastici non riproducibili  P3
Tipo: difetto confermato — **corretto** (commit `9b310b82`)
Prova: `python3 scripts/genera-pacchetti-kit.py` sul commit `f807cfa` → i 4 ZIP risultano modificati in git pur con contenuto identico (CRC uguali, date delle voci 2026-10-01 01:57 → 2026-10-03 04:11).
Impatto: ogni esecuzione del workflow produceva un commit e 19 MB da ricaricare su Aruba senza che nulla fosse cambiato; il controllo dell'audit «pacchetti stantii» dava un falso allarme.
Correzione: data fissa nelle voci (`ZIP_DATA_FISSA`); documentato in rule 10.
Verifica di chiusura: due esecuzioni consecutive danno ZIP con md5 identici; `check-parita-schede.py` → parità completa.

### F13 · La verifica del sito live si arrendeva al primo errore di rete sul manifesto  P3
Tipo: difetto confermato — **corretto** (commit `9b310b82`)
Prova: `python3 scripts/verifica-deploy-aruba.py --campione 40` → «❌ /build-manifest.json non leggibile dal sito», mentre `curl` sullo stesso URL subito dopo risponde 200 (848.620 byte).
Impatto: un solo inciampo di rete trasformava il controllo in un falso «sito non leggibile» senza aver guardato alcuna pagina.
Correzione: tre tentativi su `build-manifest.json` e `build-info.js` quando non arriva risposta.
Verifica di chiusura: stesso comando → «66/66 file coincidono con il manifesto della build».

### F14 · Controllo refusi: falsi positivi dalle immagini in base64  P3
Tipo: difetto confermato — **corretto** (commit `9b310b82`)
Prova: `check-refusi.py` sweep completo → 1.281 parole sospette in 20 file, di cui oltre 1.200 da un PNG in base64 dentro un `<textarea>` di `kit-calamita-bambini/12-unisci-puntini-casco.html`.
Correzione: le righe in base64 sono ignorate; aggiunte 8 parole italiane al dizionario (pneumologo, elevabili, distrattori, …). Gli altri «sospetti» sono onomatopee delle fiabe, abbreviazioni e titoli inglesi di articoli scientifici: nessun refuso reale.
Verifica di chiusura: lo stesso file → 0 parole sospette.

### F15 · Messaggio del watchdog sulla crescita del repository: suggerisce un'azione già fatta  P3
Tipo: difetto confermato — **corretto** (commit `9b310b82`)
Prova: issue #1186 e `.github/workflows/aggiorna-stato-sistema.yml:233` — «valutare di smettere di committare static/pagefind/», mentre `static/pagefind/` è in `.gitignore` dal 15/07/2026 e non ha file versionati.
Correzione: il messaggio indica le cause reali della crescita (storia dei commit di podcast, presentazioni, snapshot e cartine).

### F16 · Filtro arancione della Cartografia: bianco su arancione  P3
Tipo: difetto confermato — **corretto** (commit `fea10bc9`)
Prova: axe su `/cartografia/` → `button[data-tipo="AS"]` #ffffff su #ea580c, 3,55:1 (`themes/flavour-pcgenzano/layouts/shortcodes/mappa-aree.html:23`).
Correzione: testo nero (5,9:1), come prescrive la rule 03 per l'arancione; screenshot letto.
Verifica di chiusura: axe su `/cartografia/` → nessuna violazione di contrasto. Restano i marcatori della mappa sotto i 24 px (eccezione «essenziale» di WCAG 2.5.8: la posizione è l'informazione).

### F17 · Emorragie: «sollevare l'arto» nella pagina canonica e in un articolo programmato  P2
Tipo: **da validare** (direzione sanitaria o istruttore IRC)
Prova: `content/formazione/primo-soccorso/emorragie-ustioni-traumi.md:28` («solleva la parte ferita, se non si sospetta una frattura»); `content/comunicazioni/2026-10-14-primo-soccorso-base-famiglie.md` § «Emorragie gravi» («sollevare l'arto se possibile»).
Impatto: le linee guida europee di primo soccorso del 2021 non raccomandano più l'elevazione dell'arto per controllare un'emorragia (la pressione diretta resta il gesto principale). Il sito è coerente con se stesso, quindi non c'è contraddizione interna: è una possibile obsolescenza, e un testo sanitario non si cambia senza una firma.
Correzione: issue da aprire con la verifica sul capitolo di primo soccorso delle Linee guida IRC 2025; se confermato, si toglie la riga nei due file (e si aggiunge al registro canonico).
Verifica di chiusura: parere scritto del responsabile sanitario o del capitolo IRC citato nella pagina.

### F18 · Dati delle schede di economia e clima da riverificare voce per voce  P2
Tipo: **da validare** (referente didattico, con le fonti)
Prova: `static/formazione/schede-stampabili/economia-rischio-secondaria2/index.html` tabella «Casi studio — costi reali»: Friuli 1976 «4,5» miliardi di euro (le stime correnti, attualizzate, sono di un altro ordine di grandezza), con fonte collettiva «DPC, CNI, MEF, Regioni» non riferita a riga; `climate-change-secondaria2/index.html`: «+19% di eventi estremi negli ultimi 30 anni (fonte: Legambiente, ISPRA)», «Sardegna 2013: 440 mm in 12h», «Emilia-Romagna 2023: 500 mm in 36h».
Impatto: numeri in schede che gli studenti copiano come dato; fonte non riconducibile al singolo valore.
Correzione: per ogni riga una fonte puntuale, oppure la dicitura di stima o di dato di esercizio come in F06. Non applicata perché i valori corretti vanno presi dai documenti, non stimati.
Verifica di chiusura: ogni cella numerica ha una fonte nominata nella scheda.

### F19 · Social media policy: «commenti disattivati» anche su Facebook?  P3
Tipo: **da validare** (redazione)
Prova: `content/social-media-policy/_index.md:35` — «Sui soli post programmati i commenti sono disattivati»; rule 10 § «Pubblicazione automatica social»: su Instagram i commenti si disattivano via API, «su Facebook si imposta dalla Pagina, non via API».
Correzione: verificare l'impostazione della Pagina Facebook; se i commenti restano aperti, la frase va limitata a Instagram.

### F20 · Schede di pregrafismo e pop-up: modelli da ricalcare e placeholder sotto il contrasto minimo  P3
Tipo: raccomandazione motivata (backlog)
Prova: axe dopo F10 → 20 pagine residue, quasi tutte con testo-guida chiaro da ricalcare (`.alf-traccia`, `.parola-modello`, `.puntini`, `.traccia`, spesso `aria-hidden`), segnaposto («[ Spazio per la foto ]») e alcune etichette dei libri pop-up (`libro-popup-protezione-civile`, `flavia-libro-popup`).
Impatto: per i modelli da ricalcare il tono chiaro è parte della funzione (il bambino ci scrive sopra), e axe non lo può sapere; restano da correggere le etichette dei libri pop-up e i segnaposto.
Correzione proposta: lasciare i modelli da ricalcare, scurire etichette e segnaposto dei due libri e di `diventa-giornalista-primaria`; in `gioco-oca-protezione-civile` portare i link dell'indice a 24 px.

### F21 · Numeri utili: manca il 1530 della Guardia Costiera  P3
Tipo: raccomandazione motivata
Prova: rule 06 § «Numeri di emergenza da citare sempre correttamente» elenca il 1530 (emergenze in mare e sui laghi); `grep -c 1530 content/numeri-utili/_index.md data/numeri_utili.yaml` → 0 e 0. Il numero compare solo in maremoto, dossier del Tevere e appendici del manuale.
Correzione proposta: aggiungerlo a `data/numeri_utili.yaml` e alla pagina, con la nota sui laghi di Albano e Nemi, e poi nelle 7 traduzioni (lavoro su più di 5 file: va concordato).

### F22 · Articolo del 26/09 sugli alberi di via Lenin uscito sul sito il 1° ottobre e mai sui social  P3
Tipo: **da validare** (redazione)
Prova: issue #1186 («online dal 01/10/2026 00:03, assente dalla coda»): l'articolo è retrodatato e il repository dei social scarta le voci con data più vecchia di tre giorni.
Correzione: pubblicazione manuale su Instagram e Facebook, se ancora utile.

### F23 · Dossier «Il nostro Gruppo»: description di 169 caratteri  P3
Tipo: difetto confermato (non corretto: il testo è editoriale)
Prova: `content/dossier/il-nostro-gruppo.md` frontmatter `description` = 169 caratteri (limite del progetto 160).
Correzione proposta: accorciare la description senza cambiare titolo né contenuto.

## Rilievi aperti ereditati dagli audit precedenti (stesso numero)

| Rilievo | Stato al 3/10 | Responsabile |
|---|---|---|
| A25-F04 Deposito della dichiarazione di accessibilità su form.agid.gov.it (scadenza 23/09 passata) | **aperto**: `hugo.toml` `dichiarazioneAccessibilita = ""`, `_attesa_ente = true`; la pagina dichiara che il deposito è in capo al Comune | Comune di Genzano (referente accessibilità) |
| A25-F05 Numero della delibera del 1991 di istituzione del Gruppo | **aperto**: la Trasparenza dice «1991, con delibera del Consiglio Comunale» senza numero | Segreteria del Gruppo / Comune |
| A25-F01 Rotazione della password FTP dopo il passaggio a FTPS | FTPS **attivo** (`deploy.yml:207 protocol: ftps`); rotazione non verificabile da qui | Titolare dell'account Aruba |
| A25-F16 Privacy: recapito dell'RPD solo per rimando al sito del Comune | **aperto** | RPD del Comune |
| A25-F08 CSP con `'unsafe-eval'` e `img-src https:` | **aperto** (richiede prova in Report-Only) | decisione tecnica dell'utente |
| A25-F18 Archivio `/comunicazioni/` in una sola pagina | **aperto**: 687 KB, 415 immagini | decisione di struttura dell'utente |
| A25-F06 Cache HTTP disattivata | **accettato consapevolmente** (istruzione permanente, rule 05) | — |
| A25-F22 SEO on-page (titoli e description fuori misura) | **aperto**, vedi anche F23 | redazione |
| A25-F11 Accessibilità residua (marcatori Leaflet, h1 multipli in alcune schede) | **parziale**: axe pulito su 22 delle 24 pagine Hugo controllate; marcatori in eccezione 2.5.8 | — |

Chiusi e riverificati in questo run: A25-F01 (FTPS attivo), A25-F07 (file di stato FTP negati in `.htaccess`), A25-F09 (aggiornamento Bootstrap Italia via PR con verifica sha512), A25-F14 (social policy riallineata, un post per articolo), A25-F15 (cruciverba reale 13x13), A25-F20 (`safeStorage` in quizpc).

## Da validare esternamente (issue da aprire, label `audit` + `revisione`)

1. **F17** — elevazione dell'arto nelle emorragie. Responsabile: direzione sanitaria di riferimento o istruttore IRC del Gruppo. Chiusura: parere scritto o capitolo IRC 2025 citato; poi correzione dei due file.
2. **F18** — dati numerici delle schede di economia e clima. Responsabile: referente didattico. Chiusura: fonte puntuale per ogni cella o dicitura di dato di esercizio.
3. **F19** — commenti sui post Facebook programmati. Responsabile: redazione social. Chiusura: impostazione della Pagina verificata e frase della policy allineata.
4. **F22** — pubblicazione manuale dell'articolo del 26/09. Responsabile: redazione social.
5. **A25-F04** — deposito AgID. Responsabile: Comune di Genzano. Chiusura: URL della dichiarazione nel campo `dichiarazioneAccessibilita`.
6. **A25-F05** — numero della delibera del 1991. Responsabile: segreteria del Gruppo.
7. **A25-F16** — recapito diretto dell'RPD. Responsabile: RPD del Comune.

Da decidere da parte dell'utente: allineare la riga 477 di `CLAUDE.md` alla nuova nota della rule 10 (F11); la variante di template per il CAP (F11); F20, F21 e F23.

## Controlli superati

- Build Hugo 0.154.5 pulita (1.093 pagine), anche con `-F` sui contenuti programmati; due build a un minuto di distanza differiscono per i 5 file attesi (rule 05).
- `check-integrita-asset.py`: 4.887 file, nessuno vuoto o corrotto (62 PDF letti; 49 senza tag e 24 senza testo estraibile, informativo).
- `check-ancore.py`: 4.798 ancore su 1.581 pagine, tutte valide (anche sulla build con i programmati).
- `check-parita-schede.py`: parità completa nelle quattro fasce, prima e dopo le correzioni.
- `check-dati-schede.py`: 20 confronti, tutti coincidenti con i dataset.
- `check-jsonld.py`: tutti i blocchi del campione validi, paternità presente.
- `check-dati-canonici.py`: 14 dati (2 nuovi), nessuna variante.
- `check-data-uscita.py --giorni 30`: 36 articoli coerenti.
- `audit-grammatica-italiana.py`: 1.541 file, nessun rilievo.
- `genera-chrome-menu.py --check`: menu allineato.
- `check-fascicolo-esperimenti.py` (Playwright): 33 schede, un foglio per esperimento, nessuna scritta tagliata.
- `check-fonti-cruscotto.py`: 25 fonti su 26 raggiungibili; Open-Meteo forecast in timeout al primo tentativo, 200 al secondo (passeggero).
- `verifica-deploy-aruba.py --campione 40`: 66/66 file live coincidono con il manifesto della build `be50f97`.
- `smoke-test-live.sh`: 69 controlli superati al primo giro; i 29 negativi (26 risposte «000» e 3 marker che dipendevano da quelle risposte) erano interruzioni del proxy di questa sessione (`ws_closed_mid_exchange`): ripetuti, tutti gli URL rispondono 200 e i marker sono presenti (verificati anche sulla build locale). La sezione degli header non è arrivata in fondo per il limite di tempo del comando ed è stata ripetuta a mano: HSTS, CSP, `nosniff`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy` con `geolocation=(self)`, COOP, TDM e `Cache-Control: no-store` presenti.
- Workflow: 53 file YAML validi, `timeout-minutes` su ogni job, tutte le action di terzi pinnate a SHA, tutti i workflow documentati nella rule 10; 35 agenti documentati in `CLAUDE.md` e nella parte 19 del manuale.
- Dati e feed: tutti i JSON di `static/open-data/` e della build validi; CAP, sitemap, news-sitemap e 134 feed RSS ben formati; 1.173 URL della sitemap tutti presenti nella build, nessuno `noindex`; numeri utili coerenti fra YAML, JSON e CSV.
- Traduzioni: le 7 lingue hanno `language:`, `tts: false`, 112 e 803 555 nelle tre pagine tradotte e i 4 litri d'acqua del piano familiare.
- Sicurezza: nessun segreto nel repository (le corrispondenze sono miniature JPEG dentro i PDF); `Permissions-Policy` con `geolocation=(self)` integra; gli host chiamati dalla Sala situazioni sono coperti dalla CSP o sono link e tessere.
- Usabilità: nessuna pagina orfana reale (le apparenti erano alias di redirect o link con il prefisso di GitHub Pages).
- Conformità: pagine legali con `dataUltimaRevisione` entro 12 mesi; link al Difensore civico per il digitale 200; nessun articolo con `scadenza` passata non archiviato.
- Esercitazione della catena di allerta in locale: con l'emergenza attiva il banner compare in homepage, numeri utili, archivio, formazione ed `/emergenza/`; `allerta-stato/index.json` e CAP si aggiornano (vedi F11 per l'incoerenza trovata). `data/allerta.json` e `data/emergenza.json` ripristinati, `git status` pulito.
- Fatti verificati e confermati: numero verde del Centro Funzionale 800 276 570 e sede di via Laurentina (Regione Lazio); SOUP 15 giugno - 30 settembre (Regione Lazio); Sendai Framework (18 marzo 2015, sette obiettivi, quattro priorità; giornata istituita nel 1989); livelli di allerta dei vulcani (Campi Flegrei al giallo dal 2012).

## Perimetro, metodo e limiti

- **Perimetro completo**: tutte le aree della tabella degli specialisti, applicandone i criteri dall'orchestratore. Approfondimento manuale sui contenuti cambiati dopo il 25/09 e sui 7 articoli in uscita entro il 17/10 (`check-articoli-programmati.py`); gli altri contenuti sono coperti dai controlli automatici e dalle grep di famiglia (AIB, ustioni, RUNTS).
- **Rete**: la sessione esce attraverso un proxy che ha interrotto diverse connessioni verso il sito; ogni esito negativo di rete è stato ripetuto prima di essere valutato. Wikipedia, CNR-IRPI, INGV, Normattiva, Regione Lazio e il Dipartimento erano raggiungibili.
- **Non verificato qui**: rotazione della password FTP, deposito AgID, impostazioni delle pagine social, contenuto dei capitoli IRC 2025 (F17).
- **Non eseguito**: `pa11y-ci` (lo stesso motore, axe-core, è stato usato direttamente); Lighthouse.
- **Gate editoriali**: sugli articoli corretti si sono applicati i criteri del gate AGID e del desk giornalistico (fonte primaria, nessun dato senza fonte, campo `image:` invariato — verificato con `git diff | grep '^[+-]image'` vuoto — refusi a zero sui file toccati). Nessun articolo nuovo, nessun testo sanitario nuovo: il solo intervento sanitario (F07) allinea testi esistenti alla pagina canonica.
- **Commit** sul branch `claude/audit-interno-2026-10-03`, identità `Alessandro Cuollo`: `aec3a4e1`, `10ff23e9`, `916531db`, `9b310b82`, `763b67f9`, `fea10bc9`, più il commit di questo rapporto. Push, PR e merge a cura dell'orchestratore, un merge per volta.

## Prossimo audit

- Routine mensile del **3 novembre 2026**, ore 06 italiane.
- Da controllare per primi: chiusura delle 7 validazioni esterne; nessuna variante AIB dopo il 15 ottobre (alla fine del periodo la voce del registro va riletta e, se serve, chiusa); i tre articoli di freschezza segnalati (`2024-11-26-manuale-caritas-banco-alimentare-presentazione`, `2025-02-05-libro-risparmio-fondazione-barilla-presentazione`, `2025-03-10-cucina-emergenza-haccp-ruoli-volontari`); gli anniversari in uscita in novembre (Firenze 1966, Polesine 1951, Irpinia 1980, Genova 2011), con il controllo delle vittime sulle fonti primarie prima dell'uscita.
- Lezione di metodo: tre audit hanno corretto il «30 settembre» frase per frase e il difetto è tornato ogni volta. Quando un dato sbagliato compare in più di un file, la correzione si chiude solo con la voce nel registro `data/dati_canonici.yaml`.
