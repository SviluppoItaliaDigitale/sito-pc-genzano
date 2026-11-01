# Regola LIM: ogni materiale per le scuole funziona sulla lavagna interattiva

Vale per tutto ciò che il sito offre alle scuole, presente e futuro: giochi (`static/giochi/`), schede stampabili, kit per le scuole e kit calamità, storie, Abili a proteggere, quiz (`static/quizpc/`, `static/formazionepc/`, `/quiz-preparazione/`), moduli per le scuole (`static/scuole/`), libro che si esplora, esperimenti, laboratorio meteo, tabelle CAA, Crea la mia lezione, Modalità Aula, pagine `content/formazione/**`. Istruzione dell'utente dell'01/11/2026, dopo le segnalazioni delle scuole: *«Rendi tutto perfettamente compatibile. Ho avuto segnalazioni in merito che non va bene sulle lim i contenuti del nostro sito!!!»* e *«scrivi poi una regola che il lavoro che hai fatto adesso sia replicato in futuro coi prossimi giochi kit eccetera, ogni documentazione utile utilizzabile per le scuole»*.

## Il caso da cui nasce

Una LIM non è un computer qualunque: si usa col dito o con la penna, senza mouse né tastiera, è proiettata a 1024×768 o 1366×768, spesso con lo zoom alto, e il suo browser (Android integrato nella lavagna o PC di classe con Windows 7) può essere fermo a cinque o sette anni fa. La verifica dell'01/11/2026 ha trovato:

- **Bootstrap Italia 2.x non si avviava** sui browser precedenti a Chrome 80 (optional chaining, campi statici di classe): su 101 pagine su 165 menu a tendina, finestre, caroselli e accordion restavano fermi. Due giochi dell'infanzia (`?.`) non partivano, e Hugo riscriveva negli script delle pagine `catch(e){}` in `catch{}`, che Chrome 65 non legge;
- la «Linea del tempo» non si poteva giocare col dito (solo trascinamento HTML5 col mouse o tastiera); in «Posiziona i cartelli» un tocco selezionava e subito deselezionava il cartello;
- pulsanti da 30×22 px, link «Torna…» alti 19 px;
- i giochi dell'infanzia senza `custom.css`: la barra per il telefono compariva anche sulla LIM e copriva il gioco;
- etichette che uscivano dallo schermo a 1366 px;
- il libro 3D bloccato su «Sto aprendo il libro…» dove il 3D non può partire;
- nessun pulsante «Schermo intero» nei giochi;
- con Firefox, a 1024 px, il menu del sito sforava di 18 px su 110 pagine (Firefox disegna il carattere un po' più largo di Chromium), e il libro 3D senza WebGL lasciava il pannello vuoto e un errore.

Nessun controllo se n'era accorto, perché tutti provavano con un browser moderno, il mouse e uno schermo largo.

## Che cosa vale per ogni materiale nuovo o modificato

1. **Il JavaScript resta entro ECMAScript 2018 (Chrome 64).** Niente `?.`, `??`, `??=`, campi di classe, `catch {}` senza parametro, blocchi `static {}`, `.at()`, `replaceAll`, `structuredClone`, `Object.hasOwn`, `replaceChildren` negli script delle pagine per le scuole. Lo verifica `scripts/check-sintassi-js.cjs`, bloccante su ogni PR insieme agli script dentro le pagine costruite (`hugo.toml`: `[minify.tdewolff.js] version = 2017`). Uniche eccezioni dichiarate nello script: il libro 3D (WebGL 2), con la sua versione testuale; la Sala situazioni.
2. **Bootstrap Italia si usa nella versione trascritta.** Dopo ogni aggiornamento `bash scripts/js-compatibile-lim.sh` (lo fa da sé `update-bootstrap-italia.yml`); il file porta in testa il segno `compatibile-lim`. Mai ripristinare il bundle originale.
3. **Tutto si fa col solo tocco.** Ogni azione che si fa trascinando ha un'alternativa a tocco singolo: tocca l'oggetto e poi la destinazione, oppure pulsanti (frecce ▲▼). Il trascinamento col dito, se c'è, usa i *pointer events* con `touch-action: none`, non il trascinamento HTML5, che sulle lavagne spesso non parte. Il codice che realizza l'alternativa porta il segno `alternativa-al-trascinamento`, che `scripts/check-lim.py` cerca in ogni gioco con `dragstart`. Niente informazioni o comandi solo al passaggio del mouse, niente doppio clic, niente tasti obbligatori (le frecce da tastiera vanno affiancate da pulsanti a schermo), niente pressione lunga obbligatoria.
4. **Bersagli grandi.** Nei giochi e nei quiz ogni comando misura almeno 44×44 px; il minimo assoluto, bloccante, è 24 px (WCAG 2.2, 2.5.8). Per caselle e scelte conta l'etichetta, che deve essere grande e cliccabile. Link «Torna…» e barre degli strumenti alti almeno 44 px (`scheda-print.css`, `app-common.css`).
5. **Proiettore e zoom.** Nessuna pagina più larga dello schermo a 1024×768 e 1366×768, né con lo zoom al 150% (910×512); niente `white-space: nowrap` su testi lunghi, `minmax(0, 1fr)` nelle griglie con parole grandi. I pulsanti fissi del sito non devono coprire il gioco: le pagine statiche caricano sempre `/css/custom.css` (lo stile della barra in basso, che compare solo sotto i 992 px), dopo `bootstrap-icons` e prima di `app-common.css`.
6. **Schermo intero.** I giochi e i quiz con schermate (`#intro`, `#game`, `#end`, `[data-gioco]`…) ricevono da `site-chrome.js` i pulsanti «Schermo intero» e «Torna al menu» (`#gioco-comandi`). Un gioco nuovo usa quei marcatori, così li riceve da sé; i contenuti da proiettare in Hugo usano Modalità Aula.
7. **Se una funzione non può partire, lo si dice.** Un componente che richiede tecnologie recenti (WebGL, moduli ES) ha un'alternativa che funziona ovunque (versione testuale, schede da stampare), e se dopo il caricamento non è partito mostra un messaggio che porta a quell'alternativa, come lo shortcode `libro-3d`. Mai uno «Sto caricando…» senza fine.
8. **Ogni materiale lo dichiara: «Pronto per la LIM».** Istruzione dell'utente dell'01/11/2026: *«Metti anche una specifica in ogni pagina utilizzabile sul lim»*. Il riquadro rimanda alla pagina [`/lim/`](/lim/), che spiega che cosa è controllato e come si usano i materiali in classe, ed è scritta per farsi trovare dai motori di ricerca (domande frequenti strutturate, mappa del sito, `llms.txt`). Dove compare:
   - **pagine Hugo**: partial `lim-pronto.html`, sopra «Leggi questa pagina in altri modi», per i prefissi di `data/lim.yaml` (voce `hugo`, meno `esclusi`);
   - **giochi, quiz, Abili a proteggere, indici di schede e storie**: lo inserisce `site-chrome.js` (`aggiungiProntoLim`);
   - **schede e storie**, che non caricano JavaScript: link nella barra in alto, scritto da `scripts/segno-lim-statiche.py` e dai generatori di `scripts/schede-didattiche/` e `scripts/genera-schede-esperimenti.py`.
   Il riquadro dice solo ciò che i controlli verificano: una famiglia di pagine nuova entra in `data/lim.yaml` (e, se statica, in `site-chrome.js` o nello script) solo insieme ai controlli che la provano. Testo identico nei tre posti: si cambia insieme. **Mai scrivere «unici in Italia», «i primi», «qualsiasi LIM» senza condizioni o altri primati e garanzie che nessuno ha misurato** (regola `qualita.md`, punti 1 e 7): la pagina dice con quali browser e a quali risoluzioni la compatibilità è provata.
9. **Si prova come in classe, prima di consegnare.** Per ogni gioco o strumento nuovo o modificato: `python3 scripts/check-lim.py --pagine /percorso/` dopo la build, e una partita intera col solo tocco fino alla verifica finale (Playwright con `has_touch`, `tap`; per il trascinamento col dito `Input.dispatchTouchEvent` via CDP). Per i giochi con schermate che compaiono dopo un tocco, la prova automatica vede solo la prima schermata: le altre si controllano giocando.

## Controlli automatici

| Controllo | Dove | Cosa blocca |
|---|---|---|
| `scripts/check-sintassi-js.cjs --public public` | `validate-pr.yml` (ogni PR), `controllo-lim.yml` | sintassi oltre ES2018 in file e pagine; Bootstrap Italia non trascritto |
| `scripts/check-lim.py --da-git` | `validate-pr.yml` job `fogli-stampa` (pagine toccate; tutte se cambia un file condiviso) | errori JS, pagina più larga dello schermo, comandi dei giochi sotto 24 px, trascinamento senza alternativa |
| `scripts/segno-lim-statiche.py --check` | `validate-pr.yml`, `controllo-lim.yml` | scheda o storia senza «Pronto per la LIM» |
| `scripts/check-lim.py` (Chromium e Firefox) + `scripts/check-lim-browser-vecchio.cjs` (Chromium 69) | `controllo-lim.yml`, ogni lunedì | tutte le pagine per le scuole, compreso il riquadro «Pronto per la LIM» mancante; script fermi, Bootstrap Italia assente e menu fermi sul browser del 2018 |

Il giro settimanale apre la issue in-place «🧑‍🏫 Pagine per le scuole da correggere per le LIM» (label `automazione`), che si chiude da sola. Un problema nuovo trovato in classe diventa una voce di questi controlli (regola `qualita.md`, punto 5). Il gate dei materiali scolastici `pc-didattica-reviewer` e il collaudo `pc-collaudo-funzionale` applicano questa regola.
