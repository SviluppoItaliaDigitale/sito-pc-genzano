# Audit completo del sito — revisore A

## 1. Giudizio complessivo

Il sito è solido dove conta di più. I 1.492 indirizzi della mappa del sito rispondono tutti, l'HTML è pulito in modo uniforme e la pagina di emergenza è leggera, chiara e dice da dove viene il dato e quando è stato controllato. I controlli di coerenza del repository passano: i testi non si contraddicono sui dati che il progetto sorveglia.

I punti deboli stanno ai margini, dove i controlli automatici non guardano. Tre deploy su quattro partono senza le verifiche successive. La home scarica circa 190 KB e legge 5,9 MB di testo per sapere il colore dell'allerta. Alcuni comandi e alcune tabelle non rispettano WCAG 2.2 sul telefono, in pagine che il controllo delle pull request non apre. La ricerca non porta alle istruzioni per una fuga di gas, e la pagina di emergenza scrive «disabili» invece di «persone con disabilità».

Non ho trovato errori che mettano in pericolo il cittadino. Diversi rilievi vanno però corretti presto, perché toccano l'emergenza o la catena dei controlli.

## 2. Perimetro e metodo

- **Quando:** sabato 7 novembre 2026, fra le 5:50 e le 6:50 circa, ora italiana. Repository al commit `04eb54c` di `main`.
- **Sito pubblicato** (`https://www.protezionecivilegenzano.it/`):
  - scansione di tutti i 1.492 indirizzi di `sitemap.xml` (1.491 pagine HTML e un file JSON), con due richieste alla volta: codice HTTP, rinvii, peso, tempo di risposta, titolo, numero di h1, attributo `lang`, descrizione, canonical, immagini senza `alt`, lettura di ogni blocco JSON-LD;
  - 28 pagine aperte con Chromium senza interfaccia a 375×812 e a 1280×800 (56 viste), con axe-core 4.14 sulle regole WCAG 2.0, 2.1 e 2.2 di livello A e AA: `/`, `/accessibilita/`, `/allerte-meteo/`, `/aree-attesa/`, `/assistente/`, `/cerca/`, `/chi-siamo/`, `/comunicazioni/`, `/contatti/`, `/cosa-fare-adesso/`, `/cruscotto/`, `/diventa-volontario/`, `/emergenza/`, `/english/`, `/facile-da-leggere/`, `/formazione/`, `/giochi/`, `/lim/`, `/mappa-sito/`, `/monitor/`, `/numeri-utili/`, `/open-data/`, `/piano-emergenza/`, `/piano-familiare/`, `/privacy/`, `/rischi-prevenzione/`, `/rischi-prevenzione/rischio-sismico/`, `/sala-stampa/`;
  - Lighthouse 13.6, profilo mobile simulato, su 5 pagine: `/`, `/emergenza/`, `/cruscotto/`, `/rischi-prevenzione/rischio-sismico/` e l'articolo più recente, `/comunicazioni/2026-11-07-piemonte-1994-alluvione-tanaro/`;
  - richieste di rete della home e del cruscotto a 375 px, registrate per 12 secondi dopo il caricamento; spostamenti del layout registrati con `PerformanceObserver` a 412×823;
  - ricerca interna `/cerca/?q=…` con 16 parole comuni: per tutte i primi cinque risultati, per 10 anche il riquadro «Pagine di servizio»;
  - intestazioni HTTP della home (`curl -sSI`), `/.well-known/security.txt`, feed CAP `/allerta-cap.xml`, archivio `/comunicazioni/` scaricato e analizzato.
- **Repository:** template, CSS e JavaScript del tema, `data/ricerca.json`, `scripts/axe-gate.js`, workflow in `.github/workflows/`, rapporti in `riferimenti-interni/audit-esterni/` e `riferimenti-interni/audit-interni/`. Script eseguiti, con il codice d'uscita: `cerca-incongruenze.py` 0, `check-dati-canonici.py` 0, `check-data-uscita.py --giorni 10` 0, `check-ruoli-aria.py` 0, `check-refusi.py` sui 15 articoli dal 1° al 7 novembre 0 (nessuna parola sospetta), `check-freshness.py` 3, `check-articoli-programmati.py` 3.
- **Automazioni:** gli ultimi 60 run di «🚀 Build e Deploy» (creati dal 5 novembre alle 21:52 al 7 novembre alle 6:00), i log dei passi falliti, i run degli altri workflow nello stesso periodo, le issue aperte.
- **Non verificato:** velocità misurata sugli utenti reali (il sito non raccoglie questi dati); prove con lettori di schermo e con una LIM vera; stato del rinnovo del dominio sul pannello del registrar (conosco solo la data del registro, riportata dall'issue #1666); la causa precisa dell'a capo descritto in R9.

## 3. Pro: punti di forza

1. **Ogni pagina risponde.** I 1.492 indirizzi della mappa del sito rispondono tutti con codice 200, senza rinvii e senza errori. Tempo di risposta: mediana 0,74 s, il 95% delle pagine entro 0,86 s, massimo 1,4 s.
2. **HTML uniforme e corretto.** Sulle 1.491 pagine HTML: un solo h1 in ognuna, nessun titolo ripetuto, canonical sempre presente, 0 immagini senza `alt` su 9.821, 1.894 blocchi JSON-LD tutti leggibili. Le traduzioni dichiarano la loro lingua: `lang="en"` su 8 pagine, `fr`, `de`, `ro` ed `eo` su 5, `es` e `pt` su 4, `ar` su 1.
3. **Pagina di emergenza esemplare.** `/emergenza/`: Lighthouse 100 in tutte e quattro le categorie, 25 KB e 4 richieste, contenuto principale visibile in 1,0 s su rete mobile simulata. La pagina dice quando il dato è stato controllato e da dove viene: «Verificato: 7 novembre 2026, 02:26 (dato dell'ultima pubblicazione del sito) · Fonte: Centro Funzionale Lazio». Dalla home le quattro pagine di emergenza vengono caricate in anticipo (`/cosa-fare-adesso/`, `/numeri-utili/`, `/emergenza/`, `/allerte-meteo/`, 129 KB nelle richieste registrate).
4. **Accessibilità buona nelle pagine principali.** axe-core non trova violazioni su 24 delle 28 pagine provate, a entrambe le larghezze. Lighthouse dà 100 in accessibilità, buone pratiche e SEO su tutte e 5 le pagine misurate.
5. **Intestazioni di sicurezza complete.** Sulla home: `strict-transport-security: max-age=31536000; includeSubDomains`, `content-security-policy` attiva (non solo in prova), `x-content-type-options: nosniff`, `x-frame-options: SAMEORIGIN`, `referrer-policy: strict-origin-when-cross-origin`, `permissions-policy: geolocation=(self), microphone=(), camera=()`, `cross-origin-opener-policy: same-origin-allow-popups`. `/.well-known/security.txt` segue la RFC 9116, con scadenza `2027-07-01T00:00:00.000Z`.
6. **Dati di allerta riusabili da altre applicazioni.** Il feed CAP `/allerta-cap.xml` identifica il Comune con il codice ISTAT `058043` e la zona di allerta «F - Bacini Costieri Sud», senza bisogno di interpretare il testo.
7. **Privacy rispettosa e dichiarata.** La pagina `/privacy/` scrive: «Questo sito usa solo cookie tecnici necessari al funzionamento. Non usa cookie di profilazione o cookie pubblicitari», e dichiara il servizio con cui conta le visite in forma anonima. Fra le richieste della home l'unica chiamata di statistica è quella al servizio dichiarato.
8. **I testi non si contraddicono sui dati sorvegliati.** `cerca-incongruenze.py`: «Nessuna incongruenza nelle 10 famiglie controllate». `check-dati-canonici.py`: «59 dati canonici, 2313 file controllati, nessuna variante sbagliata». `check-data-uscita.py`: 11 articoli in uscita, date coerenti. Nessun refuso nei 15 articoli della settimana.
9. **Ricerca con scorciatoie per le parole dell'emergenza.** Cercando «terremoto», «volontario» o «allerta meteo», il riquadro «Pagine di servizio» porta subito a `/rischi-prevenzione/rischio-sismico/`, `/diventa-volontario/` e `/allerte-meteo/`, anche quando la ricerca mette prima degli articoli. Cercando «dae» il primo risultato è `/formazione/primo-soccorso/defibrillatore-dae/`.
10. **Caricamento su Aruba affidabile.** Nei 60 deploy esaminati il caricamento sul sito di produzione è riuscito sempre: gli 8 run rossi sono falliti solo nel passo della copia di anteprima su GitHub Pages (R7).

## 4. Contro: punti deboli

### R1 — Tre deploy su quattro partono senza i controlli successivi
- **Dove:** `.github/workflows/notifica-ci-fallita.yml` (righe 9-16), `.github/workflows/smoke-test-post-deploy.yml` e `.github/workflows/verifica-deploy-aruba.yml`: tutti e tre partono con `workflow_run` al termine di «🚀 Build e Deploy».
- **Che cosa non va:** i deploy avviati da altri workflow (aggiornamento dell'allerta, pubblicazione del mattino, deploy raggruppati di sfondo) partono con `workflow_dispatch` e il token di GitHub Actions. Per questi run GitHub non crea l'evento `workflow_run`, come scrive anche la regola 10 del repository («`workflow_run` non scatta per i run lanciati col `GITHUB_TOKEN`»). Dopo questi deploy non partono la prova del sito pubblicato, la verifica indipendente contro la build e l'avviso in caso di errore. La verifica con riparazione dentro `deploy.yml` invece gira sempre.
- **Prova:** dal 5 novembre alle 21:50 al 7 novembre alle 6:05: 60 run di deploy, 15 da `push` e 45 da `workflow_dispatch`. Nello stesso periodo `smoke-test-post-deploy.yml` e `verifica-deploy-aruba.yml` hanno 15 run ciascuno, tutti `workflow_run`. Gli 8 deploy falliti sono tutti `workflow_dispatch` e nessuno ha aperto un'issue: l'ultima «🚨 Workflow fallito: 🚀 Build e Deploy» (#1724) è chiusa dal 6 novembre alle 3:36, e da allora i fallimenti sono stati 6. Dopo quello delle 5:28 del 7 novembre il watchdog non ha nessun run fra le 5:26 e le 5:32.
- **Priorità:** P2
- **Esito:** (da compilare da chi verifica)

### R2 — La home scarica circa 190 KB e legge 5,9 MB di testo per sapere il colore dell'allerta
- **Dove:** `/`; `themes/flavour-pcgenzano/static/js/home-allerta.js`, righe 162-164 (indirizzi) e 70 (ricerca della riga).
- **Che cosa non va:** a ogni visita la home scarica i due bollettini per Comune, `bollettino-oggi-comuni-latest.csv` e `bollettino-domani-comuni-latest.csv`, e li scorre fino alla riga che contiene «genzano di roma». Sono 2,98 MB e 2,95 MB di testo, 94 KB ciascuno compressi. Lo stesso archivio ha il bollettino per zone: 63,8 KB di testo, 1,2 KB compressi. Genzano è nella zona Lazi-F, già scritta in `scripts/check-allerta.py` (righe 129-130).
- **Prova:** richieste della home a 375 px: due `Fetch` da 94 KB verso `raw.githubusercontent.com` a 1,6 s dall'inizio, su 1.136 KB e 35 richieste in tutto. Misura dei file con `curl`: 2.976.961 e 2.949.619 byte di testo, 95.942 e 95.905 compressi; il file per zone 63.754 byte di testo, 1.177 compressi.
- **Priorità:** P2: è la pagina che si apre in emergenza, spesso dal telefono e con la rete carica.
- **Esito:** (da compilare da chi verifica)

### R3 — Assistente: il nome dei due pulsanti iniziali non contiene tutto il testo visibile
- **Dove:** `/assistente/`; `themes/flavour-pcgenzano/layouts/assistente/list.html`, riga 1639.
- **Che cosa non va:** ogni scheda di scelta è un `<button>` con titolo e descrizione visibili, ma con `aria-label="' + escapeHTML(opt.text) + '"`, cioè il solo titolo. Il nome accessibile sostituisce il contenuto: chi usa un lettore di schermo sente il titolo e non la descrizione. È il caso che WCAG 2.5.3 «Etichetta nel nome» chiede di evitare.
- **Prova:** axe-core, regola `label-content-name-mismatch`, 2 nodi a 375 e a 1280 px: `.card-emergency` («Sono in difficoltà ORA») e `button[data-next="mode_informa"]` («Voglio informarmi»).
- **Priorità:** P2: è il primo comando dell'assistente, quello di chi ha un'emergenza in corso.
- **Esito:** (da compilare da chi verifica)

### R4 — Sul telefono alcune tabelle larghe non si scorrono da tastiera
- **Dove:** `/rischi-prevenzione/rischio-sismico/` e `/privacy/` a 375 px; `themes/flavour-pcgenzano/layouts/_default/_markup/render-table.html` (contenitore `<div class="table-responsive">`).
- **Che cosa non va:** su schermo stretto la tabella scorre in orizzontale dentro il suo contenitore, ma il contenitore non riceve il fuoco e la tabella non contiene link. Chi usa la tastiera, o un ausilio che la simula, non può scorrerla e non legge le colonne nascoste (WCAG 2.1.1).
- **Prova:** axe-core, regola `scrollable-region-focusable`, a 375 px: `.table-responsive:nth-child(23)` su rischio sismico, `.table-responsive:nth-child(24)` su privacy. A 1280 px nessuna violazione.
- **Priorità:** P2
- **Esito:** (da compilare da chi verifica)

### R5 — Il controllo di accessibilità delle pull request non guarda il telefono né le pagine di R3, R4 e R13
- **Dove:** `scripts/axe-gate.js`, righe 20-28 (`PATHS`) e avvio del browser.
- **Che cosa non va:** il controllo bloccante apre 13 pagine a una sola larghezza, quella predefinita del browser automatico (800×600): nello script non c'è nessuna impostazione della finestra. Non apre `/assistente/`, `/privacy/`, `/rischi-prevenzione/rischio-sismico/` né la Sala situazioni `/monitor/`. I difetti di R3, R4 e R13 non possono quindi fermare una pull request.
- **Prova:** lettura dello script (elenco `PATHS`; nessuna chiamata che imposti la larghezza); i difetti compaiono nella prova del § 2.
- **Priorità:** P2
- **Esito:** (da compilare da chi verifica)

### R6 — «disabili» invece di «persone con disabilità», anche nella pagina di emergenza
- **Dove:** `/emergenza/` (`themes/flavour-pcgenzano/layouts/shortcodes/pagina-emergenza-lite.html`, riga 135) e `/aree-attesa/` (`content/aree-attesa/_index.md`, riga 47): «Aiuta chi è in difficoltà se puoi farlo in sicurezza (anziani, bambini, disabili)». In tutto 29 file sorgente, fra cui articoli, il manuale di campo («Servizi igienici per disabili», «Modulo disabili»), schede per la secondaria, il gioco «Codice arancione», il coach dei giochi e il quiz.
- **Che cosa non va:** la regola del repository `comunicazione-social.md` chiede «persona con disabilità», vieta «il disabile» e «i disabili» e chiede «accessibile» invece di «per disabili». Il d.lgs. 62/2024, art. 4, sostituisce «disabile» con «persona con disabilità» nella normativa. Il sito si contraddice: la scheda «Emergenza inclusiva» per la secondaria insegna «"persona con disabilità", non "disabile"», mentre il pacchetto «Stampa tutto» della secondaria che la contiene ha anche «Assistenza disabili» e «Affiancamento ad anziani, disabili, bambini soli».
- **Prova:** ricerca della parola intera «disabile» o «disabili» nei sorgenti, esclusi i titoli dei video di terzi in `data/`, i nomi propri (Federazione Associazioni Nazionali Disabili), i nomi di variabili, le frasi che spiegano la regola e una frase fra virgolette che riprende il linguaggio delle norme antincendio; testo della pagina `/emergenza/` pubblicata.
- **Priorità:** P2
- **Esito:** (da compilare da chi verifica)

### R7 — La copia di anteprima su GitHub Pages fallisce ancora in un deploy su sette
- **Dove:** `.github/workflows/deploy.yml`, riga 364 (`alleggerisci-copia-pages.py public --tetto-mb 800`) e job `deploy-pages` (righe 376-386).
- **Che cosa non va:** dopo l'alleggerimento del 6 novembre (PR #1731; l'issue #1724 è stata chiusa subito dopo) la copia scende da 1.953 a 783 MB, ma la pubblicazione su GitHub Pages supera ancora i 10 minuti in 6 deploy su 43. Il limite di 10 minuti è di GitHub, quindi allungare l'attesa dell'azione non servirebbe. Il sito di produzione non ne risente, ma i run diventano rossi e, per R1, nessuno lo segnala.
- **Prova:** gli 8 run falliti su 60 hanno fallito tutti nel passo «🌐 Deploy GitHub Pages». Log dell'ultimo (run 42337424578): stato `syncing_files` per dieci minuti, poi «Timeout reached, aborting!». Log del deploy delle 6:00: «Copia per GitHub Pages: 1953 MB prima, 783 MB dopo (tetto 800 MB, limite di GitHub 1 GB)». La pagina «GitHub Pages limits» della documentazione di GitHub fissa a 10 minuti la durata massima di una pubblicazione.
- **Priorità:** P3
- **Esito:** (da compilare da chi verifica)

### R8 — Ricerca: «fuga di gas», «defibrillatore» e «scuola» non portano alla pagina che serve
- **Dove:** `/cerca/`; `data/ricerca.json`, elenco `scorciatoie`.
- **Che cosa non va:** per queste ricerche il riquadro «Pagine di servizio» non compare e i primi cinque risultati non contengono la pagina utile:
  - «fuga di gas»: primo risultato la scheda per bambini `/formazione/schede-stampabili/labirinto-evacuazione-primaria/`, poi un articolo sul piano di evacuazione; «gas» porta alla lezione sulla combustione. Le istruzioni su che cosa fare con l'odore di gas stanno nell'assistente (scelta «Sento odore di gas»), che la ricerca non propone;
  - «defibrillatore»: due articoli di marzo e settembre 2026; la pagina `/formazione/primo-soccorso/defibrillatore-dae/` esce solo cercando «dae»;
  - «scuola»: primo risultato `/scuole/pcto/convenzione-attuativa/`, poi la sicurezza sullo scuolabus; `/formazione/` non compare.
- **Prova:** prove su `/cerca/?q=…` del § 2, con il riquadro e i primi cinque risultati.
- **Priorità:** P2 per «fuga di gas», che è una situazione di pericolo; le altre due sono miglioramenti.
- **Esito:** (da compilare da chi verifica)

### R9 — All'apertura la pagina scende di 21 px: «Enti istituzionali» va a capo
- **Dove:** barra superiore dell'intestazione, link `a.it-opener` «Enti istituzionali» dentro `.it-header-slim-wrapper`, sul telefono. Non è la barra di navigazione.
- **Che cosa non va:** a 412 px, circa 1,3 s dopo l'inizio del caricamento, «Enti istituzionali» passa da una a due righe. La barra superiore cresce da 50 a 71 px e tutto il resto scende di 21 px: chi sta per toccare un comando può toccare quello sbagliato. Lo spostamento c'è o no a seconda che l'a capo avvenga prima o dopo il primo disegno della pagina.
- **Prova:** Lighthouse mobile: CLS 0,118 su `/cruscotto/` e sull'articolo più recente, 0 su home ed emergenza. Registrazione a 412×823 su `/cruscotto/`: spostamento di 0,117 a 1.297 ms, `.it-header-center-wrapper` da y=49 a y=70; il link passa da 37 a 58 px di altezza.
- **Priorità:** P3
- **Esito:** (da compilare da chi verifica)

### R10 — Cruscotto: lo stesso file dei confini scaricato due volte
- **Dove:** `/cruscotto/`; shortcode `dashboard-satellite.html` (riga 148), `dashboard-italiameteo-satellite.html` (riga 61) e `dashboard-cams.html` (riga 119).
- **Che cosa non va:** tre schede chiedono ciascuna `open-data/world-countries.geo.json` (257 KB di testo, 104 KB compressi). Con la cache disattivata per scelta ogni richiesta è uno scaricamento vero: all'apertura del cruscotto il file arriva due volte.
- **Prova:** richieste del cruscotto a 375 px: due `Fetch` da 103 KB dello stesso file a 1,45 e 1,47 s, su 1.298 KB e 37 richieste in tutto.
- **Priorità:** P3
- **Esito:** (da compilare da chi verifica)

### R11 — Logo dell'intestazione: 480 px e 54 KB per un'immagine mostrata a 82 px
- **Dove:** tutte le pagine; `themes/flavour-pcgenzano/layouts/partials/navbar.html`, righe 9-10.
- **Che cosa non va:** `images/logo-pc-genzano.webp` misura 480×480 px e pesa 53.674 byte, ma è mostrato a 82×82 (`width="82" height="82"`). Anche per gli schermi ad alta densità bastano 164 px. Con la cache disattivata il logo si scarica a ogni pagina visitata.
- **Prova:** file scaricato dal sito pubblicato (480×480 px, 53.674 byte); markup del partial.
- **Priorità:** P3
- **Esito:** (da compilare da chi verifica)

### R12 — Archivio delle comunicazioni: 857 KB di HTML in una sola pagina
- **Dove:** `/comunicazioni/`.
- **Che cosa non va:** l'archivio mette in una pagina sola 534 schede di articoli: 856.790 byte di HTML (96 KB compressi) e 11.241 elementi, più di due volte e mezza la seconda pagina più pesante del sito. Sul telefono è la pagina più pesante da costruire, e cresce con ogni articolo.
- **Prova:** scansione della sitemap (pagina più pesante: `/comunicazioni/` 856.790 byte, poi `/monitor/` 327.084); pagina scaricata e contata con un analizzatore HTML.
- **Priorità:** P3
- **Esito:** (da compilare da chi verifica)

### R13 — Sala situazioni: il pulsante «COPIA LINK» ha un nome diverso dal testo
- **Dove:** `/monitor/`; `static/monitor/index.html`, riga 776.
- **Che cosa non va:** `<button data-sh="copy" aria-label="Copia il link di questa schermata">COPIA LINK</button>`: il nome accessibile non contiene il testo visibile «COPIA LINK» (WCAG 2.5.3). Chi comanda con la voce e pronuncia «copia link» può non trovare il pulsante.
- **Prova:** axe-core, regola `label-content-name-mismatch`, a 1280 px.
- **Priorità:** P3
- **Esito:** (da compilare da chi verifica)

### R14 — Lo stesso coordinamento scritto in due modi
- **Dove:** `content/chi-siamo/_index.md`, righe 61-62 («Coordinamento FE.PI.VOL.») e riga 132 («Coordinamento FE.P.I.VOL.»); la seconda forma anche in quattro articoli di agosto e novembre 2026.
- **Che cosa non va:** nei sorgenti «FE.PI.VOL.» compare 99 volte e «FE.P.I.VOL.» 10 volte, anche nella stessa pagina. Le regole del progetto, per le affiliazioni, usano «Coordinamento FE.PI.VOL.». Il registro dei dati canonici non contiene questa voce, quindi nessun controllo lo vede.
- **Prova:** conteggio delle due forme in `content/`, `static/`, `themes/` e `data/`.
- **Priorità:** P3
- **Esito:** (da compilare da chi verifica)

### R15 — 139 schede dei kit calamità senza descrizione per i motori di ricerca
- **Dove:** pagine statiche in `static/formazione/kit-calamita-*/` (79 del kit per i bambini, 20 delle strutture sanitarie, 11 degli anziani e altre).
- **Che cosa non va:** non hanno `<meta name="description">`. Nei risultati dei motori di ricerca compare un estratto scelto dal motore, che per una scheda da stampare è spesso poco chiaro.
- **Prova:** scansione della sitemap: 139 pagine HTML senza descrizione, tutte schede dei kit calamità.
- **Priorità:** P3
- **Esito:** (da compilare da chi verifica)

### R16 — La pagina «Pronto per la LIM» promette più di quanto il processo garantisce
- **Dove:** `/lim/`; `content/lim/_index.md`, riga 21.
- **Che cosa non va:** la pagina scrive: «Se un controllo non va a buon fine, il problema viene segnalato e corretto prima della pubblicazione successiva». Il controllo completo è settimanale, apre un'issue e non ferma i deploy, che continuano. Il blocco prima della pubblicazione vale solo per le pagine toccate da una pull request.
- **Prova:** `.github/workflows/controllo-lim.yml`, riga 26 (`cron: "17 8 * * 1"`, lunedì alle 9:17 ora italiana d'inverno) e righe 91-119 (issue e uscita 1, senza legame con il deploy); regola `lim-scuole.md`, tabella dei controlli.
- **Priorità:** P3
- **Esito:** (da compilare da chi verifica)

### R17 — Nella ricerca le versioni in italiano semplice escono prima di quelle complete
- **Dove:** `/cerca/`.
- **Che cosa non va:** cercando «freddo», i primi quattro risultati sono parti della versione facile dell'articolo sulle ondate di freddo; la versione completa è al quinto posto. Cercando «terremoto», i primi quattro sono parti di `/comunicazioni/2026-10-29-terremoto-dalla-a-alla-z-video-3d-facile/`. Le versioni facili sono brevi, e la ricerca premia le pagine brevi con la parola nel titolo.
- **Prova:** prove su `/cerca/` del § 2.
- **Priorità:** P3
- **Esito:** (da compilare da chi verifica)

### R18 — Due scadenze che dipendono da altri restano aperte
- **Dove:** issue #1666 e #1203.
- **Che cosa non va:** la registrazione del dominio `protezionecivilegenzano.it` scade il 30 dicembre 2026, fra 53 giorni, e nel repository non risulta confermato il rinnovo automatico. La dichiarazione di accessibilità non è ancora depositata su form.agid.gov.it: l'adempimento spetta al Comune e la scadenza del 23 settembre è passata, come spiega la stessa pagina `/accessibilita/`.
- **Prova:** issue #1666 del 6 novembre: «scade fra 54 giorni (2026-12-30, dato del registro .it)»; issue #1203 ancora aperta; pagina `/accessibilita/`: «il deposito tramite la procedura ufficiale (form.agid.gov.it) è in capo al Comune di Genzano di Roma».
- **Priorità:** P2: se il dominio scade si spengono il sito, il feed di allerta e i QR già stampati.
- **Esito:** (da compilare da chi verifica)

### R19 — Sei articoli da riverificare prima che invecchino o escano
- **Dove:** `content/comunicazioni/`: `2024-11-26-manuale-caritas-banco-alimentare-presentazione`, `2025-02-05-libro-risparmio-fondazione-barilla-presentazione`, `2025-03-10-cucina-emergenza-haccp-ruoli-volontari` (pubblicati) e gli articoli in uscita il 14, il 19 e il 21 novembre (impianto elettrico, animali domestici, alberi).
- **Che cosa non va:** i primi tre hanno più di 18 mesi e citano norme, telefoni o link che invecchiano; gli altri tre citano norme e vanno ricontrollati prima della data di uscita. La segnalazione è già nell'issue #1679.
- **Prova:** `check-freshness.py` (uscita 3) e `check-articoli-programmati.py` (uscita 3), eseguiti sul commit `04eb54c`.
- **Priorità:** P3
- **Esito:** (da compilare da chi verifica)

## 5. Consigli per migliorarlo

1. **Avviare i controlli dopo ogni deploy da `deploy.yml`, non con `workflow_run`.** In fondo al deploy, un passo che lancia con `gh workflow run` la prova del sito pubblicato e la verifica indipendente, come già si fa per le bozze social; e un passo con `if: failure()` che apre o aggiorna l'issue «🚨 Workflow fallito». Il watchdog attuale resta per i run da `push`.
   - **Perché:** oggi l'allerta e la pubblicazione del mattino, i deploy più delicati, sono proprio quelli senza controlli; un errore di quei deploy non arriva a nessuno.
   - **Impegno:** piccolo.
   - **Rilievi:** R1, e rende visibile R7.
2. **Leggere il bollettino per zone nella home.** `home-allerta.js` può chiedere `bollettino-oggi-zone-latest.csv` e `bollettino-domani-zone-latest.csv` e cercare la zona `Lazi-F`, con la stessa logica di validità di oggi.
   - **Perché:** da circa 192 KB a circa 2,4 KB per ogni visita della home, e niente più 5,9 MB di testo da scorrere sul telefono.
   - **Impegno:** piccolo.
   - **Rilievi:** R2.
3. **Correggere i nomi accessibili dei pulsanti.** Nell'assistente togliere `aria-label` dalle schede, così il nome è il testo intero, oppure collegare la descrizione con `aria-describedby`; nella Sala situazioni scrivere un nome che cominci con «Copia link».
   - **Perché:** WCAG 2.5.3; il primo pulsante dell'assistente è quello dell'emergenza in corso.
   - **Impegno:** piccolo.
   - **Rilievi:** R3, R13.
4. **Far scorrere le tabelle larghe anche da tastiera.** Nel render hook dare al contenitore `tabindex="0"`, `role="region"` e un `aria-label` (la didascalia, se c'è, oppure «Tabella, scorri in orizzontale»); lo stesso nelle tabelle HTML scritte a mano.
   - **Perché:** WCAG 2.1.1; sul telefono, chi non usa il dito oggi non raggiunge le colonne nascoste.
   - **Impegno:** piccolo.
   - **Rilievi:** R4.
5. **Allargare il controllo di accessibilità delle pull request.** In `axe-gate.js` provare ogni pagina a 375 e a 1280 px e aggiungere `/assistente/`, `/privacy/`, `/rischi-prevenzione/rischio-sismico/` e `/monitor/`.
   - **Perché:** ogni rilievo deve diventare un controllo; questi quattro difetti sono passati perché nessun controllo guardava lì.
   - **Impegno:** piccolo.
   - **Rilievi:** R5, e impedisce il ritorno di R3, R4 e R13.
6. **Sostituire «disabili» nei 29 file e sorvegliarlo.** «persone con disabilità», e «accessibile» al posto di «per disabili» («servizi igienici accessibili»); la variante va nel registro `data/dati_canonici.yaml` o in un controllo lessicale bloccante, lasciando fuori titoli di terzi e nomi propri.
   - **Perché:** regola del progetto e d.lgs. 62/2024; la pagina di emergenza è la più letta nei momenti difficili, e il sito non deve insegnare una regola che poi non segue.
   - **Impegno:** medio.
   - **Rilievi:** R6.
7. **Completare le scorciatoie della ricerca.** In `data/ricerca.json`: «gas», «odore di gas» verso le istruzioni sulla fuga di gas (oggi nell'assistente: serve che il partial accetti un indirizzo con ancora, oppure una pagina dedicata); «defibrillat» verso `/formazione/primo-soccorso/defibrillatore-dae/`; «scuol», «docent», «insegnant» verso `/formazione/`. Dare alle versioni facili un peso di ricerca più basso di quelle complete.
   - **Perché:** chi cerca «fuga di gas» deve trovare subito che cosa fare; la versione facile resta trovabile, ma non davanti a tutto.
   - **Impegno:** piccolo.
   - **Rilievi:** R8, R17.
8. **Copia su GitHub Pages: un secondo tentativo e un tetto più basso.** Se la pubblicazione va oltre il limite, un secondo passo di pubblicazione con `if: failure()`; e un tetto più basso per la sola copia di anteprima (per esempio 500 MB), dove si tolgono altri PDF e ZIP pesanti che si aprono da Aruba. Le immagini restano, come prevede la regola.
   - **Perché:** il limite di 10 minuti è fisso; con meno da caricare e un secondo tentativo i run rossi si riducono, e quelli che restano li segnala il consiglio 1.
   - **Impegno:** piccolo.
   - **Rilievi:** R7.
9. **Fermare l'a capo di «Enti istituzionali» sul telefono.** Riservare in `custom.css` l'altezza della barra superiore sotto i 576 px, oppure impedire l'a capo del solo link, senza toccare il CSS della barra di navigazione; poi provare da 320 a 1920 px, come per la modifica del 24 ottobre.
   - **Perché:** uno spostamento di 21 px mentre si sta per toccare un comando è un errore di tocco possibile, e porta il CLS oltre 0,1.
   - **Impegno:** piccolo.
   - **Rilievi:** R9.
10. **Un solo scaricamento dei confini nel cruscotto.** Le tre schede possono condividere la stessa richiesta, salvata in una variabile della pagina (per esempio `window.pcConfini`), come già si fa per Leaflet con la guardia `.Page.Store`.
    - **Perché:** 103 KB in meno a ogni apertura del cruscotto; resta compatibile con la cache disattivata, perché è la stessa pagina.
    - **Impegno:** piccolo.
    - **Rilievi:** R10.
11. **Un logo della misura giusta.** Una versione WebP a 164×164 px per l'intestazione, con `srcset` per 1x e 2x; il file a 480 px resta per gli altri usi.
    - **Perché:** circa 40 KB in meno per ogni pagina visitata, con la cache disattivata: una prova di conversione a 164 px dà 12,5 KB.
    - **Impegno:** piccolo.
    - **Rilievi:** R11.
12. **Dividere l'archivio delle comunicazioni.** Le pagine dell'archivio di Hugo (per esempio 50 schede per pagina) o una pagina per anno, con i filtri che restano utilizzabili.
    - **Perché:** l'archivio cresce di un articolo al giorno; oggi pesa più di due volte e mezza la seconda pagina più pesante del sito.
    - **Impegno:** medio.
    - **Rilievi:** R12.
13. **Una sola grafia per il coordinamento.** Allineare le 10 occorrenze a «FE.PI.VOL.» e aggiungere la variante al registro dei dati canonici, così il controllo bloccante la ferma.
    - **Perché:** lo stesso ente scritto in due modi nella stessa pagina sembra una svista.
    - **Impegno:** piccolo.
    - **Rilievi:** R14.
14. **Descrizioni per le schede dei kit.** Lo script che già aggiunge il canonical alle pagine statiche può scrivere anche la descrizione, ricavandola dal titolo e dal sottotitolo di ogni scheda.
    - **Perché:** nei motori di ricerca la scheda si presenta con una frase chiara invece di un estratto casuale.
    - **Impegno:** medio.
    - **Rilievi:** R15.
15. **Riscrivere la frase della pagina /lim/.** Per esempio: «Se un controllo non va a buon fine, il problema viene segnalato e corretto; le pagine che modifichiamo non vengono pubblicate finché il controllo non passa».
    - **Perché:** il sito non deve promettere un controllo che non fa.
    - **Impegno:** piccolo.
    - **Rilievi:** R16.
16. **Chiudere le scadenze esterne.** Confermare sul pannello del registrar che il rinnovo automatico del dominio è attivo; sollecitare il Comune per il deposito su form.agid.gov.it.
    - **Perché:** un dominio scaduto spegne il sito e il feed di allerta; la dichiarazione è un obbligo di legge.
    - **Impegno:** piccolo, ma serve chi ha l'accesso.
    - **Rilievi:** R18.
17. **Riverificare i sei articoli segnalati.** Norme, telefoni e link sulle fonti, prima del 14 novembre per quelli in uscita.
    - **Perché:** un articolo vero quando è stato scritto e falso oggi è un errore.
    - **Impegno:** piccolo.
    - **Rilievi:** R19.

## 6. Domande e dubbi

- **Perché «Enti istituzionali» va a capo (R9)?** La larghezza del link passa da 118 a 116 px nello stesso istante: può essere un carattere o un'icona che arriva dopo il primo disegno. Si chiarisce ripetendo la misura bloccando un file alla volta.
- **Velocità della home.** Nella mia misura Lighthouse dà 97 alla home, mentre l'issue #1744 riporta punteggi sotto soglia nelle misure automatiche: le misure simulate variano da un giro all'altro, e servono più misure prima di trarre conclusioni.
- **Prove con i lettori di schermo.** La dichiarazione di accessibilità cita sessioni di autovalutazione di maggio 2026; da allora il sito è cambiato molto, e io non ho potuto ripeterle.
- **Grafia del coordinamento (R14).** Non ho trovato su una fonte primaria quale forma usi il coordinamento stesso; propongo quella delle regole del progetto.
- **Rinnovo del dominio (R18).** Se il rinnovo automatico sia attivo lo sa solo chi ha accesso al pannello.
- **Pagine caricate in anticipo dalla home.** Con la cache disattivata costano 129 KB a ogni visita della home anche a chi non le apre. È un costo che si accetta per l'emergenza: lo segnalo come scelta da tenere presente, non come rilievo.
- **Pubblicazione su GitHub Pages (R7).** Non so se il tempo di pubblicazione dipenda più dai byte o dal numero dei file: un tetto più basso riduce i byte, non il numero dei file.
