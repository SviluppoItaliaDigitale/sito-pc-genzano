# Audit interno del sito — 15 settembre 2026 — snapshot f5efbef44

Esito: 10 rilievi (P1: 1 · P2: 3 · P3: 6) · chiusi in questo run: 0 · in PR: 0 · da validare: 1

Questo giro è stato **solo diagnostico** su istruzione esplicita dell'utente: nessun commit, nessuna PR, nessuna issue aperta. Le correzioni restano da autorizzare.

## Bloccante in testa (compliance, non dato pubblicato sbagliato)

**F01 — Dichiarazione di accessibilità non depositata: scadenza il 23 settembre 2026 (8 giorni)**, vedi sotto. Non è un errore di contenuto pubblicato, ma un adempimento legale con termine imminente: lo metto in testa perché un mese senza intervento supera la scadenza di legge (L. 4/2004).

## Rilievi

### F01 · Dichiarazione di accessibilità non depositata su form.agid.gov.it — scadenza 23/09/2026  P1
Tipo: da validare (adempimento non eseguibile da Claude Code — richiede accesso a form.agid.gov.it con credenziali istituzionali)
Prova: `hugo.toml:55` → `dichiarazioneAccessibilita = ""` (vuoto). `content/accessibilita/_index.md:68` dichiara esplicitamente: *"il collegamento sarà aggiunto qui e nel piè di pagina appena disponibile"*. Confermato anche dall'issue GitHub aperta **#995** ("Scadenze di conformità: accessibilità e pagine legali"), aggiornata il 2026-09-14, che segnala lo stesso vuoto e il conto alla rovescia.
Impatto: la Legge 9 gennaio 2004 n. 4 impone il riesame annuale della dichiarazione di accessibilità **entro il 23 settembre**. Il sito non risulta avere un link alla dichiarazione depositata; se il deposito non avviene entro la scadenza, il Gruppo è inadempiente su un obbligo di legge verificabile da AgID.
Correzione: il referente del Gruppo deve accedere a `form.agid.gov.it`, compilare/rinnovare la dichiarazione (i contenuti sostanziali della pagina `/accessibilita/` sono già pronti e aggiornati al 2026-09-14), ottenere il link permanente e incollarlo in `hugo.toml` (`dichiarazioneAccessibilita`) e in `content/accessibilita/_index.md:68`. Nessuna parte di questo passo è automatizzabile: il form richiede login istituzionale.
Verifica di chiusura: `grep dichiarazioneAccessibilita hugo.toml` non deve più dare stringa vuota; la issue #995 si chiude da sola al prossimo run di `scadenze-conformita.yml` quando il campo è valorizzato.
Fonti: L. 4/2004 art. 3; `.github/workflows/scadenze-conformita.yml`; issue #995.

### F02 · Refuso riproducibile "pop-updella" nel pacchetto stampabile primaria (bug del generatore)  P2
Tipo: difetto confermato
Prova: `scripts/genera-pacchetti-schede.py:101` e `:105` — `titolo = re.sub(r"<[^>]+>", "", m_h1.group(1)).strip()` rimuove i tag HTML (incluso `<br>`) senza sostituirli con uno spazio. La scheda sorgente `static/formazione/schede-stampabili/libro-popup-protezione-civile/index.html:173` ha `<h1 class="lib-cop-titolo">Il libro pop-up<br>della protezione civile</h1>`: lo strip produce "Il libro pop-updella protezione civile". Verificato **live**: `curl https://www.protezionecivilegenzano.it/formazione/schede-stampabili/pacchetti/primaria.html | grep pop-up` restituisce 2 occorrenze di "pop-updella" (voce indice a riga 2813 del sorgente e `aria-label` della sezione a riga 3522). Riprodotto anche rigenerando il pacchetto in locale (`python3 scripts/genera-pacchetti-schede.py`): il refuso si ripresenta identico, quindi non è un fatto isolato ma sistemico ogni volta che il pacchetto viene rigenerato.
Impatto: il pacchetto "Stampa tutto — Primaria" (119 pagine A4, scaricato da insegnanti) mostra un refuso visibile sia nell'indice sia nell'etichetta accessibile della sezione (l'`aria-label` letto dagli screen reader dice "pop-updella", non "pop-up della"). Danno di immagine minore ma concreto su un materiale scolastico pubblico.
Correzione: in `genera-pacchetti-schede.py`, prima dello strip generico dei tag, sostituire `<br\s*/?>` con uno spazio (`re.sub(r"<br\s*/?>", " ", ...)`), poi applicare lo strip esistente; normalizzare gli spazi multipli risultanti con `re.sub(r"\s+", " ", titolo)`.
Verifica di chiusura: rigenerare i pacchetti e controllare `grep -o "pop-up.\{0,10\}" static/formazione/schede-stampabili/pacchetti/primaria.html` → deve restituire "pop-up della", non "pop-updella"; il check-refusi.py sul file non deve più segnalare "updella".
Fonti: `scripts/genera-pacchetti-schede.py`; pagina live citata sopra.

### F03 · `/rischi-prevenzione/rischio-vulcanico/` non rispetta l'ordine fisso delle pagine rischio (chi-chiamare non è l'ultima sezione)  P2
Tipo: difetto confermato
Prova: `content/rischi-prevenzione/rischio-vulcanico.md` — lo shortcode `{{< chi-chiamare >}}` è a riga 108 di 132 righe totali, seguito da due `## ` H2 aggiuntivi: "Fonti istituzionali e scientifiche" (riga 110) e "Approfondimenti per le scuole" (riga 125). Confrontato con le altre 7 pagine rischio (sismico, idrogeologico, incendio, vento-forte, temporali-intensi, blackout, ondate-di-calore): in tutte e 7 `{{< chi-chiamare >}}` è l'ultima riga del file (0 H2 dopo). Confermato **live**: `curl .../rischi-prevenzione/rischio-vulcanico/ | grep -oE "id=chi-chiamare|id=fonti|id=scuole"` restituisce l'ordine `chi-chiamare, fonti, scuole` — cioè il box dei numeri di emergenza compare a metà pagina, prima delle fonti e dei materiali didattici.
Impatto: rule 06 § "Struttura uniforme delle pagine rischio" e CLAUDE.md la definiscono esplicitamente "fissa e non negoziabile" per motivi di accessibilità (WCAG 3.2.3/3.2.4 — Consistent Navigation): il cittadino in stress e l'utente di screen reader che hanno imparato a trovare "Chi chiamare" sempre in fondo alle altre 7 pagine, sulla pagina vulcanico lo trovano a metà, con altri contenuti dopo.
Correzione: spostare `{{< chi-chiamare >}}` alla fine del file, dopo le sezioni "Fonti istituzionali e scientifiche" e "Approfondimenti per le scuole" (semplice riordino di blocco, nessuna perdita di contenuto).
Verifica di chiusura: `grep -n "chi-chiamare\|^## " content/rischi-prevenzione/rischio-vulcanico.md | tail -1` deve mostrare `chi-chiamare` come ultima riga del file; ripetere il confronto con le altre 7 pagine (0 H2 dopo).
Fonti: `.claude/rules/06-protezione-civile-scientifica.md` § "Struttura uniforme delle pagine `/rischi-prevenzione/*`"; CLAUDE.md.

### F04 · Pagina di trasparenza sui PDF (`/accessibilita/audit-pdf/`) non elenca gli equivalenti HTML per 9 presentazioni più recenti e per i poster multilingua  P2
Tipo: raccomandazione (la tabella completa via shortcode è corretta e aggiornata; manca solo il testo curato di supporto)
Prova: `data/audit-pdf.yaml` (ultimo_audit: 2026-09-14) elenca **18 PDF di produzione propria** in stato `NON_ACCESSIBILE`: 1 carta naturalistica, 8 poster multilingua (`static/poster-emergenza-multilingua/poster-emergenza-{it,en,fr,de,es,pt,ro,eo}.pdf`) e **9 presentazioni tematiche** (`2026-05-29-{animali-emergenza,it-alert,nue-112,piano-familiare,temporali-intensi}-presentazione-pdf.pdf`, `2026-05-30-{aree-emergenza,blackout,dopo-emergenza,vento-forte}-presentazione-pdf.pdf`). Il testo curato in `content/accessibilita/audit-pdf.md` § "Caso specifico — le 5 presentazioni tematiche" elenca **solo 5** presentazioni (sismico, idrogeologico, incendio, allerta meteo, kit emergenza — quelle di marzo-maggio) con il rimando alla pagina HTML equivalente; le altre 9 presentazioni e gli 8 poster non hanno alcun rimando testuale nella pagina di trasparenza, pur avendo quasi tutte un equivalente HTML già pubblicato sul sito (es. `/piano-familiare/`, `/rischi-prevenzione/blackout/`, `/rischi-prevenzione/vento-forte/`, `/rischi-prevenzione/temporali-intensi/`).
Impatto: la tabella completa (`{{< audit-pdf-table >}}`) mostra comunque il verdetto 🔴 per tutti e 18, quindi la trasparenza minima è rispettata; ma la sezione discorsiva, che è quella letta da un utente/screen reader in cerca di un'alternativa concreta, è disallineata dall'inventario reale e potrebbe far pensare che solo 5 documenti abbiano un problema, quando sono 18.
Correzione: estendere la tabella "Presentazione PDF → Pagina HTML equivalente" con le 9 voci mancanti (linkando le pagine rischio/piano familiare/numeri utili già esistenti); per gli 8 poster multilingua, aggiungere una riga che rimanda a `/emergenza/` (o alla traduzione corrispondente) come equivalente testuale; per la carta naturalistica, valutare se serve un equivalente o se la natura cartografica del documento la rende un'eccezione dichiarata.
Verifica di chiusura: il numero di righe della tabella "Caso specifico" deve coincidere con il numero di voci `NON_ACCESSIBILE` + `origine: GRUPPO` in `data/audit-pdf.yaml` (attualmente 18).
Fonti: `data/audit-pdf.yaml`; `content/accessibilita/audit-pdf.md`; `content/area-download/_index.md` (tabella poster).

### F05 · `check-refusi.py` non filtra i blob base64 embedded in JS: una sola scheda genera il 97% del rumore del report  P3
Tipo: raccomandazione (tooling)
Prova: sweep completo `python3 scripts/check-refusi.py` → 1284 "parole sospette" totali; 1252 di queste (97,5%) provengono da un'unica riga di `static/formazione/kit-calamita-bambini/12-unisci-puntini-casco.html:141` e righe seguenti, dove una stringa base64 lunga (decodificata via JS in `data:image/png;base64,...` per popolare l'immagine del puzzle "unisci i puntini") viene tokenizzata come se fosse prosa italiana.
Impatto: nessun impatto sul sito pubblico (l'immagine si genera correttamente via JS, con `alt` e fallback `<noscript>` presenti — verificato). L'impatto è sulla qualità dello strumento di audit: un report settimanale (`controllo-refusi.yml`) che tocchi questo file per un motivo qualsiasi diventerebbe illeggibile (1250+ righe di rumore) e potrebbe far perdere refusi veri nello stesso batch.
Correzione: in `check-refusi.py`, escludere dal tokenizzatore i pattern di stringhe alfanumeriche molto lunghe senza spazi (es. `[A-Za-z0-9+/=]{40,}`) o, più semplicemente, i contenuti dentro dichiarazioni `const/var/let` con stringhe letterali oltre una soglia di lunghezza.
Verifica di chiusura: ri-eseguire lo sweep completo dopo il fix; il totale delle "parole sospette" deve scendere da 1284 a circa 30 (i restanti falsi positivi elencati in F-nota sotto restano, ma sono gestibili).
Fonti: `scripts/check-refusi.py`; file citato.

### F06 · `genera-pacchetti-kit.py` produce ZIP non riproducibili byte-per-byte a parità di contenuto  P3
Tipo: raccomandazione (tooling)
Prova: eseguito `python3 scripts/genera-pacchetti-kit.py` due volte di seguito senza modifiche al contenuto sorgente: `git diff --stat` segnala i 4 file `static/formazione/pacchetti/kit-scuola-*.zip` come modificati, con dimensione identica in byte ma contenuto binario diverso (tipico sintomo di timestamp interni allo ZIP non fissati). Modifiche scartate con `git checkout` per non lasciare il working tree sporco.
Impatto: se il workflow `genera-pacchetti-kit.yml` si attiva (push su file kit/schede), può produrre un commit di "aggiornamento" degli ZIP anche quando il contenuto delle schede non è cambiato per nulla — rumore nella cronologia git, non un danno per l'utente finale.
Correzione: fissare `date_time` nello `zipfile.ZipInfo` di ogni voce (es. tupla costante) invece di lasciare il default corrente, oppure ordinare le voci e azzerare i metadati variabili prima di scrivere l'archivio.
Verifica di chiusura: due esecuzioni consecutive dello script senza modifiche al sorgente devono produrre ZIP byte-identici (`sha256sum` uguale).
Fonti: `scripts/genera-pacchetti-kit.py`.

### F07 · 9 sigle ricorrenti non coperte dal glossario, 3 delle quali pertinenti (MTG, ASI, APS)  P3
Tipo: raccomandazione
Prova: `python3 scripts/check-glossario-coverage.py` → 9 sigle: U.S (41), IGO (20), MTG (16), ASI (14), XII (14), XIV (13), USA (12), FAQ (11), APS (10). Delle 9, la maggioranza sono falsi positivi (numeri romani XII/XIV, sigle generiche U.S./USA/FAQ), ma **MTG** (Meteosat Third Generation, citato negli articoli sui satelliti), **ASI** (Agenzia Spaziale Italiana) e **APS** (Associazione di Promozione Sociale, rilevante per il Terzo Settore) sono acronimi tecnici PC-pertinenti che meriterebbero una voce.
Impatto: minimo — il popover inline del glossario semplicemente non scatta su queste 3 sigle nei relativi articoli.
Correzione: aggiungere 3 voci a `content/glossario/_index.md` (MTG, ASI, APS) con definizione AGID di 1-2 frasi.
Verifica di chiusura: `check-glossario-coverage.py` non deve più elencare MTG/ASI/APS tra le mancanti.
Fonti: `scripts/check-glossario-coverage.py`.

### F08 · 3 articoli oltre i 18-22 mesi con norme/link da riverificare  P3
Tipo: raccomandazione
Prova: `python3 scripts/check-freshness.py` → `2024-11-26-manuale-caritas-banco-alimentare-presentazione` (~22 mesi, norma+link), `2025-02-05-libro-risparmio-fondazione-barilla-presentazione` (~19 mesi, norma), `2025-03-10-cucina-emergenza-haccp-ruoli-volontari` (~18 mesi, norma).
Impatto: basso — argomenti di divulgazione alimentare/Terzo Settore, non rischio/sicurezza in senso stretto, ma le norme citate (probabile riferimento HACCP, D.Lgs. 155/1997 o Reg. CE 852/2004) vanno riverificate come vigenti.
Correzione: invocare `pc-content-freshness` + `pc-normative-verifier` sui 3 articoli.
Verifica di chiusura: articoli aggiornati o marcati `archiviato: true` se superati; il check non li elenca più.
Fonti: `scripts/check-freshness.py`.

### F09 · 5 articoli programmati (19-28 settembre 2026) da riverificare prima della pubblicazione  P3
Tipo: raccomandazione
Prova: `python3 scripts/check-articoli-programmati.py` → 5 articoli con norme/link citati, in uscita tra 4 e 13 giorni da oggi (19, 21, 23, 26, 28 settembre). Ho letto integralmente `2026-09-23-san-pio-patrono-volontari-festa.md`: il fatto storico (San Pio da Pietrelcina patrono dei Volontari di PC dal 21/02/2004, petizione di ~160 associazioni) risulta corretto e verificabile, nessuna correzione necessaria su questo articolo.
Impatto: nessuno ora; il rischio è che una norma citata negli altri 4 articoli (giornata volontari, equinozio, BLS-D/defibrillatore, chiusura campagna AIB) cambi tra la stesura e la data di pubblicazione.
Correzione: promemoria operativo, nessuna azione ora — la sessione che li pubblica deve ririverificare norme e link.
Verifica di chiusura: nessuna, è un controllo ricorrente.
Fonti: `scripts/check-articoli-programmati.py`.

### F10 · 3 articoli futuri con badge Prevenzione ancora privi di versione facile (A2)  P3
Tipo: raccomandazione
Prova: `python3 scripts/check-versione-facile-coverage.py` → `2026-10-17-neve-e-gelo-casa-e-auto-pronte-prima-dell-inverno`, `2026-12-15-nebbia-guidare-in-sicurezza`, `2026-12-29-vacanze-in-montagna-valanghe-sicurezza`.
Impatto: nessuno ora (articoli non ancora pubblicati, uscita tra 1 e 3,5 mesi).
Correzione: creare le versioni `-facile.md` prima della pubblicazione o quando si lavora sull'articolo.
Verifica di chiusura: il check non li elenca più.
Fonti: `scripts/check-versione-facile-coverage.py`.

## Controlli superati

- **Build Hugo pulita**: scaricato e usato Hugo 0.154.5+extended (stessa versione della CI, `peaceiris/actions-hugo` in `deploy.yml`), `hugo --quiet --minify -d /tmp/public` → **0 errori, 0 warning**, 5919 file generati.
- **`check-integrita-asset.py`**: 4767 file controllati, 0 file vuoti o corrotti. 51 PDF letti (20 senza testo estraibile, 42 senza tag) — tutti già censiti e disclosi in `data/audit-pdf.yaml`/`/accessibilita/audit-pdf/` (vedi F04 per il rilievo sulla sezione discorsiva).
- **`check-ancore.py`** (su `/tmp/public`): 1532 pagine indicizzate, 4719 ancore verificate, tutte puntano a un id esistente; nessun `mailto:` codificato due volte.
- **`check-parita-schede.py`**: parità completa su 4 fasce (infanzia 77, primaria 84, secondaria 65, secondaria2 62 schede) tra kit, "Stampa tutto", ZIP e cartelle; avvertenze per l'adulto presenti in ogni formato; ZIP apribili offline.
- **`check-dati-schede.py`**: 20 confronti tabella-scheda ↔ dataset aperto, tutti coincidenti.
- **`check-jsonld.py`** (su `/tmp/public`): campione di ~90 pagine (tutte le comunicazioni recenti + un capitolo del manuale), tutti i blocchi JSON-LD validi con paternità presente.
- **`audit-grammatica-italiana.py`**: 1514 file analizzati, 0 errori/warning/info.
- **`check-fonti-cruscotto.py`**: tutte le 19 fonti dati esterne del cruscotto rispondono HTTP 200 (INGV, Open-Meteo, DPC radar, EUMETSAT, NASA GIBS, EFFIS, ARPA Lazio, Copernicus CAMS/EMS, GDACS, 2 ricevitori SDR, ItaliaMeteo).
- **`genera-chrome-menu.py --check`**: `site-chrome.js` allineato a `hugo.toml` (fonte unica del menu).
- **Rigenerazione pacchetti schede**: `genera-pacchetti-schede.py` rieseguito, `git diff --quiet` sulla cartella pacchetti → nessuna deriva (a parte il bug F02, stabile e riproducibile, non un nuovo difetto introdotto da questo run).
- **Catena dell'allerta, verificata LIVE (non solo in locale)**: `data/allerta.json` su `main` (via API GitHub) mostra 5 commit "controllo periodico" regolari distanziati di ~5h45 (01:31, 07:16, 13:02, 18:51, 00:41 UTC del 14-15/09), confermando che il meccanismo anti-staleness descritto in rule 09 §15 funziona; il fingerprint live (`verifica-fingerprint-live.sh`) mostra tutte le 15 pagine campione sulla stessa build (`sha=0d0c599`, `time=2026-09-15T01:28:59Z`); la homepage live mostra "Verificato: 15 settembre 2026, 02:41", coerente con l'ultimo commit su `main`. **Nota di metodo**: la mia prima lettura del file locale `data/allerta.json` sul branch di lavoro (fermo al 14/09 pomeriggio, perché i commit automatici avvengono su `main` e non su questo branch) mi aveva fatto temere un drift; il confronto con `raw.githubusercontent.com/.../main/...` e con la pagina live ha smentito il sospetto. Nessun problema reale.
- **`smoke-test-live.sh`**: PASSATO — 70 pagine principali + 5 articoli recenti + 7 traduzioni + 6 mini-app statiche + 12 marker JS/HTML chiave (assistente 8 percorsi, Leaflet, numeri utili senza 115/118/1515, endpoint allerta-stato, ecc.) + 2 header di sicurezza, tutti a 200/verdi.
- **Header di sicurezza live**: CSP enforcing coerente con `connect-src`/`frame-src` documentati, `Permissions-Policy: geolocation=(self)` corretto (non `()`), `X-Content-Type-Options`, `Strict-Transport-Security`, `Cache-Control: no-store` (coerente con l'istruzione "niente cache" del 12/09/2026).
- **Crawl link completo (issue GitHub #1035, `check-links-sito.yml`, ieri)**: 14.763 link controllati, **0 errori**, solo 5 timeout su siti terzi (AREU Lombardia, ASL Roma 6, Stradeanas) e redirect attesi (share button).
- **48 workflow YAML** in `.github/workflows/`: tutti sintatticamente validi (`yaml.safe_load`).
- **34 agenti dichiarati in CLAUDE.md**: tutti presenti in `.claude/agents/` (nessun agente fantasma, nessun agente orfano).
- **Correzioni della verifica interna del 6/09/2026 ancora in vigore**: nessuna occorrenza residua di "3 litri"/"2 litri" per il kit 72 ore fuori dai contesti legittimi (idratazione, escursioni, Sphere/IARU); spot-check su `content/english/piano-familiare/_index.md` conferma "4 L per person per day, for 3 days" e hreflang reciproci su `/facile-da-leggere/` presenti e corretti.
- **8 pagine rischio**: tutte hanno sia `cosa-non-fare` sia `chi-chiamare`; 7 su 8 rispettano l'ordine fisso (l'eccezione è F03).
- **Manuale**: nessuna citazione della norma UNI 11656 superata (2016); tutte le occorrenze citano correttamente l'edizione vigente 2023.
- **Open data interventi**: `periodo.al = 2026-09-11`, 4 giorni di scarto da oggi, ben sotto la soglia di 21 giorni del promemoria automatico.
- **Nessuna PR aperta**, nessuna issue con label `audit` in attesa; le issue automatiche aperte (7 totali) sono tutte già note e coerenti con questo rapporto (in particolare #995 conferma F01, #1035 conferma il crawl link pulito).

## Perimetro, metodo e limiti

**Perimetro**: completo per la parte deterministica (Fase 1 del mandato, incluse due verifiche non elencate esplicitamente ma coerenti — `check-glossario-coverage.py` e `check-versione-facile-coverage.py`); **parziale** per la parte di merito (Fase 2), per un limite di ambiente dichiarato onestamente qui sotto.

**Limite dichiarato — nessun tool per invocare sotto-agenti**: l'ambiente in cui ho eseguito questo audit espone solo `Read/Edit/Write/Grep/Glob/Bash/WebFetch` più il canale di consegna finale — **non ho a disposizione un tool `Agent`/`Task`** per invocare i 16 specialisti (`pc-fact-checker`, `pc-didattica-reviewer`, `pc-conformita-legale`, `pc-integrita-tecnica`, `pc-coerenza-trasversale`, `pc-accessibility-auditor`, `pc-revisore-scientifico`, `pc-desk-giornalistico`, `pc-revisore-codice`, `pc-revisore-automazioni`, `pc-sicurezza`, `pc-revisore-traduzioni`, `pc-dati-e-feed`, `pc-esercitazione-emergenza`, `pc-verifica-visiva`, `pc-usabilita`, `pc-documentazione`) previsti dal mandato. Ho compensato eseguendo io stesso, con `grep`/`curl`/lettura diretta dei file, un sottoinsieme mirato dei controlli di merito che quegli specialisti avrebbero coperto: struttura delle pagine rischio (F03), coerenza dei fatti su acqua/hreflang/112 (verifica di tenuta delle correzioni del 6/9), un fatto storico su un articolo programmato (San Pio), sicurezza HTTP live, validità YAML dei workflow, esistenza degli agenti dichiarati, freschezza open data, stato delle issue/PR GitHub.
**Limite dichiarato — nessun tool di verifica visiva**: non ho **Playwright** né altro strumento di screenshot/rendering browser in questo ambiente. Non ho potuto eseguire `pc-verifica-visiva` (layout mobile, stampa A4 reale, contrasto renderizzato) né una vera Lighthouse/pa11y run locale. Mi sono affidato a `smoke-test-live.sh` (solo HTTP/marker testuali) e alla lettura dei sorgenti CSS/HTML. **Questo è il limite più significativo del giro**: eventuali difetti puramente visivi (schiacciamenti, sovrapposizioni, contrasto reale su sfondi custom) non sarebbero stati rilevati.
**Limite dichiarato — versione Hugo**: l'ambiente non aveva Hugo preinstallato; ho scaricato il binario 0.154.5+extended da GitHub Releases (stessa versione pinnata in `deploy.yml`), quindi il build è rappresentativo del build di produzione.
**Confusione poi corretta**: in una fase intermedia ho scambiato lo stato locale di `data/allerta.json` (fermo sul branch di lavoro) per lo stato live, temendo un drift P1 inesistente; l'ho verificato e smentito con `raw.githubusercontent.com` + curl del sito live prima di scriverlo nel rapporto (vedi nota in "Controlli superati").
**Nessuna modifica al repository**: nessun commit, nessuna PR, nessuna issue aperta in questo giro, per istruzione esplicita. Le uniche operazioni scrittura sono state rigenerazioni locali di script idempotenti (pacchetti schede/kit) per verificarne la stabilità, scartate con `git checkout`/`git stash drop` prima di concludere: `git status` a fine sessione è pulito.

## Prossimo audit

Perimetro **completo** raccomandato per il 3 ottobre 2026 (routine mensile `trig_01RMQwDs5Ku2mRfkwkDZnKmx`), condizionato alla disponibilità in quella sessione degli strumenti Agent/Task e Playwright per coprire i due limiti dichiarati sopra. Prima di allora, priorità: chiudere F01 (scadenza 23/09) e valutare F02/F03 (piccole correzioni, a basso rischio, applicabili anche fuori dalla routine mensile).
