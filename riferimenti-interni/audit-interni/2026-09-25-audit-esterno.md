# Audit esterno del sito — 25 settembre 2026 — snapshot `8fbf542` (live verificato dalle 18:05 alle 20:30)

Esito: **33 rilievi** (P1: 5 · P2: 17 · P3: 11) · **corretti nella patch `0001` (47 file): 23** · in patch separata `0002` (da mergiare osservando il deploy): 1 (F01) · rimandati a una decisione dell'utente: 5 (F06, F08, F09, F15, F19) · da validare esternamente: 4 (F04 deposito AgID, F16, F05 numero delibera 1991, F01 rotazione password)

## Stato delle correzioni (patch `0001-audit-esterno-2026-09-25-correzioni.patch`, commit su branch `claude/audit-esterno-2026-09-25`)

| Rilievo | Stato | Dove |
|---|---|---|
| F01 FTP in chiaro | **patch separata `0002`** (`protocol: ftps`; da mergiare quando si può osservare il deploy; poi ruotare la password) | `deploy.yml` |
| F02 quiz sismico | **corretto** (domanda 1 e domanda "vano della porta" allineate a Io non rischio; stesso vincolo in 2026-04-27 e -facile, Acchiappa-pericolo) | 5 file |
| F03 data AIB | **corretto** in tutti i 6 articoli (15 ottobre 2026) | 6 file |
| F04 accessibilità | **corretto** link Difensore civico (URL attuale AgID), riferimento normativo, frequenza test; **resta il deposito su form.agid.gov.it** (Comune) | `content/accessibilita/_index.md` |
| F05 1981/1991 | **corretto** Trasparenza, JSON-LD, home, Chi siamo, articolo Belice; **resta da recuperare il numero della delibera 1991** | 5 file |
| F06 cache | **non applicato** (istruzione permanente rule 05): proposta `no-cache`+ETag da decidere | — |
| F07 file di stato FTP | **corretto** (`Require all denied` + fallback 2.2; anche .gitkeep, CNAME, PROVENANCE-*.md); cancellare via FTP il file di giugno | `.htaccess` |
| F08 CSP | **non applicato** (richiede test Report-Only) | — |
| F09 update Bootstrap Italia | **non applicato** (modifica al workflow: checksum + PR) | — |
| F10 hreflang | **corretto** (le 7 home in lingua emettono 9 tag) | `hreflang-tags.html` |
| F11 accessibilità | **corretto**: 112 in 7 lingue, mappa del sito, 11 checkbox, h1 /emergenza/. Restano: marker Leaflet, h1 multipli in 4 schede, campo ricerca Pagefind | 11 file |
| F12 lingua delle parti | **corretto** (`lang="it"` su header, footer, barra rapida, pulsanti flottanti, banner cookie nelle pagine non italiane) | `baseof.html` |
| F13 link esterni | **corretto** solo il link AgID; gli altri 57 nel CSV allegato | — |
| F14 riferimenti a strumenti | **corretto** area-download e accessibilità; **da decidere**: social media policy (contraddizione 1 post/articolo vs 2 al giorno), metadati m4a | 2 file |
| F15 cruciverba | **non applicato** (contenuto nuovo: serve un cruciverba reale o il ritiro della scheda) | — |
| F16 privacy/trasparenza | **da validare** con RPD e referente | — |
| F17 candele / 1515 | **corretto** (facile da leggere it/en/ro/eo, neve e ghiaccio, assistente, quiz AIB, llms.txt, CSV) | 10 file |
| F18 archivio comunicazioni | **non applicato** (paginazione: scelta di struttura) | — |
| F19 pipeline | **non applicato** (decisione infrastrutturale) | — |
| F20 localStorage | **corretto** banner cookie; **resta** quizpc (16 accessi) | `cookie-banner.html` |
| F21 escape Monitor | **corretto** (`esc()` con apice; `q.place` escapato) | `static/monitor/index.html` |
| F22 SEO on-page | **non applicato** (titoli/description: lavoro editoriale) | — |
| F25 striscia caldo | **corretto** (fino al 15 settembre) | `banner-caldo.html` |
| F27 /emergenza/ | **parziale**: h1 aggiunto; il micro-fetch resta da decidere | — |
| F29 dichiarazione | **corretto** riferimento normativo e frequenza test; obiettivi e "pagina tradotta" da riscrivere | — |
| F30 .htaccess | **corretto** `AddDefaultCharset UTF-8` e robots.txt; il resto da decidere | — |
| F32 stato non verificato | **corretto** (barra grigia "STATO ALLERTA NON VERIFICATO" dopo 6 h senza bollettini leggibili) | `home-allerta.js`, `custom.css` |
| F33 refusi | **corretto** | `schede-stampabili/index.html` |

Verifiche eseguite sulla patch: build Hugo 0.154.5 pulita; `check-ancore.py` (4.792 ancore ok); `check-jsonld.py` ok; `genera-chrome-menu.py --check` allineato; `check-dati-schede.py` ok; `check-parita-schede.py` ok; parsing JS dei banchi domande e di `home-allerta.js`; output verificato pagina per pagina (hreflang 9/9 sulle home in lingua, `foundingDate` 1991, h1 su /emergenza/, `lang="it"` solo sulle pagine non italiane, striscia caldo assente il 25/09). Commit con identità `Alessandro Cuollo`, hook `.githooks` attivi, nessun trailer.

Perimetro: **completo**. Sito live (tutti i 1.168 URL della sitemap), repository `SviluppoItaliaDigitale/sito-pc-genzano` al commit `8fbf542` (25/09/2026, 18:02 ora italiana), pipeline di deploy, header HTTP, prestazioni, accessibilità, SEO, conformità legale, contenuti critici per l'emergenza, materiali didattici, open data, traduzioni.

## Bloccanti in testa

**F01 — Il deploy su Aruba viaggia in FTP non cifrato.** Lo step FTP di `deploy.yml` non dichiara `protocol:` e l'action usa `ftp` in chiaro: credenziali e contenuti passano non cifrati a ogni deploy (decine al giorno).
**F02 — Il quiz per volontari sul rischio sismico si contraddice sul vano della porta** e una risposta data per "corretta" contraddice le indicazioni ufficiali di "Io non rischio".
**F03 — Sei articoli pubblicati dicono che il periodo di massima pericolosità AIB 2026 finisce il 30 settembre**; il resto del sito (e la verifica sulla fonte primaria, PR #1081) dice 15 ottobre. Chi legge quegli articoli oggi crede che i divieti cessino fra 5 giorni.
**F04 — Dichiarazione di accessibilità: deposito AgID assente a scadenza passata (23/09) e il link al Difensore civico digitale, elemento obbligatorio della dichiarazione, risponde 404.**
**F05 — La pagina Trasparenza dichiara "Anno di costituzione 1981" con soggetto costituente il Consiglio Comunale**: la delibera del Consiglio Comunale è del 1991, come dice la stessa pagina Chi siamo. Il dato macchina `foundingDate: 1981` è su tutte le pagine.

---

## Rilievi

### F01 · Deploy FTP senza cifratura (credenziali di produzione in chiaro)  P1
Tipo: difetto confermato
Prova: `.github/workflows/deploy.yml:177-206` — step `SamKirkland/FTP-Deploy-Action@110f918… # v4.4.0` con `server`, `username`, `password`, `local-dir`, `server-dir`, `dangerous-clean-slate: false`, `state-name`, `exclude`; **nessuna chiave `protocol:`**. Il valore predefinito dell'action è `ftp` (testo in chiaro), non `ftps`.
Impatto: utente e password dello spazio Aruba, più l'intero contenuto del sito, transitano non cifrati dal runner GitHub ad Aruba a ogni deploy. Il rischio pratico è limitato al percorso di rete fra i due fornitori, ma è la superficie più grave del progetto: chi intercetta un deploy ottiene l'accesso in scrittura al sito ufficiale di protezione civile.
Correzione: verificare che il server Aruba accetti `AUTH TLS` (FTPS esplicito, porta 21); aggiungere `protocol: ftps` (fallback `ftps-legacy`); dopo il primo deploy riuscito **ruotare la password FTP** e aggiornare il secret. Un deploy manuale (`workflow_dispatch`) basta come prova.
Verifica di chiusura: log del deploy con handshake TLS; `grep -n "protocol:" .github/workflows/deploy.yml` restituisce `protocol: ftps`.
Fonti: README dell'action (parametro `protocol`, default `ftp`); `deploy.yml`.

### F02 · Quiz volontari, rischio sismico: due domande in contraddizione, una contro le indicazioni ufficiali  P1
Tipo: difetto confermato
Prova: `static/quizpc/js/banco_domande/2_rischio_sismico.js:2` — risposta corretta: *"Ripararsi sotto un tavolo, una trave o nel vano di una porta"*. Stesso file, riga 59 — risposta corretta: il vano della porta *"era considerato valido per le vecchie case in muratura, oggi è sconsigliato"*. La guida ufficiale "Io non rischio – Terremoto – Cosa fare" (iononrischio.gov.it, verificata il 25/09) dice ancora: *"Mettiti nel vano di una porta inserita in un muro portante (quello più spesso) […] oppure riparati sotto un letto o un tavolo resistente"*. Lo stesso vano della porta è indicato come corretto in `content/comunicazioni/2026-04-27-terremoto…:28`, `content/dossier/quando-la-terra-trema.md:91`, `schede-1-minuto:102`, `kit-scuola-primaria.md:153`, `kit-scuola-secondaria-primo-grado.md:241`, `giochi/primaria/caccia-al-rischio/js/script.js:93`, `giochi/infanzia/acchiappa-pericolo/index.html:195`. La pagina canonica `content/rischi-prevenzione/rischio-sismico.md:12,97` non lo cita (tavolo, scrivania, muro portante).
Impatto: un volontario che si addestra col quiz riceve due risposte "giuste" opposte sulla stessa istruzione di autoprotezione; una delle due è contraria alla fonte istituzionale che il sito stesso adotta come riferimento. È esattamente il caso "istruzione che può produrre un comportamento non sicuro" del vostro schema P1.
Correzione: allineare la domanda della riga 59 a "Io non rischio" (il vano della porta è valido **solo** se inserito in un muro portante; preferire tavolo/trave); aggiungere il vincolo "in un muro portante" ovunque il vano della porta compare; valutare se la pagina canonica debba citarlo con la stessa condizione, così che pagina, quiz, dossier, schede e giochi dicano la stessa cosa.
Verifica di chiusura: `grep -rn "vano" static/quizpc content static/giochi static/formazione` restituisce solo formulazioni con "muro portante"; nessuna domanda del banco marca come corretto "sconsigliato".
Fonti: iononrischio.gov.it/it/preparati/terremoto/cosa-fare/; file citati.

### F03 · Fine del periodo di massima pericolosità AIB 2026: 30 settembre in 6 articoli, 15 ottobre nel resto del sito  P1
Tipo: difetto confermato (residuo del rilievo F03 dell'audit interno del 21/09, corretto allora su un solo articolo)
Prova: dicono **30 settembre**: `content/comunicazioni/2026-08-03-rischio-incendi-agosto-picco.md:18,35`, la sua versione `-facile.md:38`, `2026-08-28-incendi-ardea-tor-de-cenci-pontina.md:65`, `2026-08-28-tuscolo-quarta-uscita-drone-abbruciamento.md:30` (*"dal 15 giugno al 30 settembre. In queste settimane bruciare residui vegetali è vietato"*), `2026-08-30-incendio-campoleone-ulivi-abitazioni.md:69` (*"che si chiude il 30 settembre"*), `2026-09-01-bilancio-agosto-2026-numeri.md:52`. Dicono **15 ottobre**: `2026-06-08-campagna-antincendio-boschivo-2026.md`, `2026-06-18-ordinanza-sindacale-incendi-boschivi-2026.md`, `2026-09-28-chiusura-stagione-aib-lazio.md` (programmato) e altri 7. La PR #1081 del repo documenta la fonte primaria (GU Serie generale n. 133 dell'11/06/2026 e DGR Lazio 228/2023 prorogata): 15 giugno – 15 ottobre.
Impatto: la data decide la vigenza dei divieti di abbruciamento e delle sanzioni. Oggi, 25 settembre, sei pagine del sito ufficiale dicono al cittadino che i divieti finiscono fra cinque giorni; il rilievo interno del 21/09 aveva corretto la data ma non l'aveva propagata ("una correzione fattuale si applica in tutti i file che ripetono il dato" è una vostra regola cogente).
Correzione: sostituire "30 settembre" con "15 ottobre" nei 6 file, citando l'atto; in `content/rischi-prevenzione/rischio-incendio.md:34,55` ("da giugno a settembre") aggiungere il riferimento al periodo dichiarato annualmente dalla Regione, così la pagina canonica non invecchia.
Verifica di chiusura: `grep -rln "30 settembre" content/comunicazioni/2026-0[6-9]*aib* content/comunicazioni/2026-08-*incend* content/comunicazioni/2026-09-01*` → 0 file.
Fonti: PR #1081; file citati.

### F04 · Dichiarazione di accessibilità: deposito AgID mancante a scadenza passata, link obbligatorio rotto  P1
Tipo: difetto confermato + da validare (Comune)
Prova: `hugo.toml:55` `dichiarazioneAccessibilita = ""`, `:61` `dichiarazioneAccessibilita_attesa_ente = true`; `content/accessibilita/_index.md:68` rimanda il deposito al Comune "non appena disponibile"; `scadenze-conformita.yml:69` fissa la scadenza annuale al 23 settembre (passata da 2 giorni; issue #995 aperta). Nella stessa pagina il collegamento al Difensore civico per il digitale (`content/accessibilita/_index.md:380` → `agid.gov.it/it/design-servizi/accessibilita/difensore-civico-digitale`) risponde **404** (verificato con user agent browser; anche `agid.gov.it/it/design-servizi/accessibilita` è ora un 301 verso `/it/ambiti-intervento/accessibilita-usabilita`). Nessun template legge il parametro: il footer punta sempre a `/accessibilita/` (`footer.html:95`).
Impatto: il Gruppo è un'articolazione del Comune (art. 35 D.Lgs. 1/2018) e il sito si presenta come "sito ufficiale": l'obbligo di dichiarazione via form.agid.gov.it (L. 4/2004, Linee guida AgID) ricade sul Comune. La pagina è sostanzialmente completa, ma il meccanismo di enforcement obbligatorio (Difensore civico) è un link morto e la scadenza è passata.
Correzione: (a) sollecitare formalmente il Comune con testo pronto (URL, stato "parzialmente conforme", contenuti non accessibili già elencati); (b) correggere subito il link al Difensore civico digitale con l'URL attuale di AgID; (c) collegare davvero `dichiarazioneAccessibilita` al footer, o togliere il parametro e il commento che descrive un comportamento inesistente (`hugo.toml:50-54`).
Verifica di chiusura: link AgID 200; `dichiarazioneAccessibilita` valorizzato o parametro rimosso; issue #995 chiusa con l'URL del deposito.
Fonti: file citati; issue #995.

### F05 · Trasparenza: "Anno di costituzione 1981" attribuito al Consiglio Comunale; `foundingDate` 1981 su tutte le pagine  P1
Tipo: difetto confermato (dato istituzionale) + raccomandazione editoriale
Prova: `content/trasparenza/_index.md:18` `| Anno di costituzione | 1981 |` con soggetto costituente Consiglio Comunale. `content/chi-siamo/_index.md:80-82,167-168`: il Comitato nasce il 23/07/1981, *"Nel 1991 viene istituito il Gruppo Comunale di Protezione Civile con delibera del Consiglio Comunale"*. `themes/flavour-pcgenzano/layouts/partials/structured-data.html:49` `"foundingDate": "1981"` (JSON-LD `Organization`/`NGO`, in ogni pagina). Home: `themes/flavour-pcgenzano/layouts/index.html:59,98` *"Gruppo Comunale Volontari — al servizio della comunità dal 1981"*, `:110` "45 anni di attività". `content/comunicazioni/2027-01-14-belice-1968-…:57` (programmato): *"Il nostro Gruppo Comunale è nato nel 1981"*. Il numero della delibera del 1991 non compare in nessuna pagina; `area-download:58` e `assistente/list.html:935` chiamano "Costituzione del Gruppo" la Delibera C.C. n. 31 del 31/07/2023.
Impatto: la pagina di trasparenza di un ETS iscritto al RUNTS riporta un atto istitutivo con anno sbagliato; il dato macchina propaga l'errore ai motori di ricerca; la frase in home attribuisce al "Gruppo Comunale" dieci anni in cui non esisteva. La storia del 1981 è legittima, ma va detta come storia del volontariato locale, non come costituzione dell'ente.
Correzione: Trasparenza: "Istituzione del Gruppo Comunale: 1991, delibera C.C. n. … (sindaco Cesaroni); origini del volontariato locale: 1981 (Comitato); nuovo regolamento: Delibera C.C. n. 31/2023". JSON-LD: `foundingDate: 1991`. Home: "I volontari di Genzano al servizio della comunità dal 1981; Gruppo Comunale dal 1991". Articolo Belice: correggere. Recuperare e citare il numero della delibera del 1991.
Verifica di chiusura: `grep -rn "1981" content/trasparenza themes/*/layouts/partials/structured-data.html` → 0; la home distingue le due date.
Fonti: file citati.

### F06 · Cache HTTP disattivata per ogni file (HTML, CSS, JS, font, JSON): ogni visita riscarica tutto  P2
Tipo: difetto confermato
Prova: `themes/flavour-pcgenzano/static/.htaccess:215-220` — `Header set Cache-Control "no-store, no-cache, must-revalidate, max-age=0"` senza `<FilesMatch>`, più `Header unset ETag` e `FileETag None`. Live: le 1.167 pagine HTML e `bootstrap-italia.bundle.min.js` (298 KB gzip), `bootstrap-italia.min.css` (92 KB), `custom.css` (59 KB), `bootstrap-icons.min.css` (86 KB), `index.json` (1,7 MB gzip, caricato da /assistente/) rispondono tutti `cache-control: no-store…`. Lighthouse 12 (mobile, rete simulata): home **performance 53** — LCP 5,9 s, FCP 4,3 s, TBT 350 ms, Speed Index 12,1 s, 961 KiB, 31 richieste; `/giochi/` 35 (LCP 6,4 s, CLS 0,30); `/chi-siamo/` 62 (LCP 7,1 s, 1.037 KiB); `/english/` 66; `/cosa-fare-adesso/` 68; `/allerte-meteo/` 74; `/numeri-utili/` 83; `/emergenza/` 100. Diagnostica: "Page prevented back/forward cache restoration: main resource has cache-control:no-store".
Impatto: su rete mobile in emergenza — il caso d'uso che il sito dichiara di servire — ogni pagina ricarica ~600 KB di asset comuni identici alla pagina precedente; il tasto "indietro" rifà la richiesta; niente risposte 304. L'obiettivo "sempre aggiornato" non richiede `no-store`.
Correzione: **non applicata** — `.claude/rules/05 § "Cache HTTP — DISATTIVATA, non reintrodurla (12/09/2026)"` registra un'istruzione permanente dell'utente ("elimina ogni cache e non metterla più") dopo aggiornamenti non visibili sul live. Resta una scelta sua. L'unica variante compatibile con quell'obiettivo (ogni richiesta arriva al server e riceve sempre la versione corrente) è `Cache-Control: no-cache` + ETag/Last-Modified al posto di `no-store`: il browser rivalida **ogni** richiesta e riceve un 304 solo se il file è identico byte per byte, ma può riusare la copia locale e il tasto "indietro" torna a funzionare. Da decidere; se resta `no-store`, il rilievo si chiude come "accettato consapevolmente".
Verifica di chiusura (se si adotta `no-cache`): `curl -sI …/css/custom.css | grep -i cache-control` → `no-cache`; seconda richiesta con `If-None-Match` → 304; bfcache abilitata.
Nota di metodo: Lighthouse eseguito da un ambiente con proxy — i valori assoluti sono indicativi; da confermare con PageSpeed Insights (l'API era in quota-exceeded durante l'audit). Le segnalazioni "uses-http2" ed "errors-in-console" sono state scartate come artefatti del proxy (il server risponde in HTTP/2, `bootstrap-icons.min.css` è servito come `text/css`).

### F07 · I file di stato dell'action FTP sono pubblici: inventario completo del server con hash  P2
Tipo: difetto confermato
Prova: `https://www.protezionecivilegenzano.it/.ftp-deploy-sync-state-2026-06-09.json` → **200**, 488 KB gzip (≈2,1 MB); `/.ftp-deploy-sync-state.json` → **200**, 906 KB gzip (≈4,0 MB, residuo di giugno). Elencano ogni file dello spazio web (≈8.350 voci) con hash e dimensione, incluso ciò che non è linkato.
Impatto: information disclosure: mappa completa del server per chi cerca file dimenticati, cartelle di lavoro o versioni precedenti; conferma il meccanismo di deploy usato.
Correzione: in `.htaccess` `<FilesMatch "^\.ftp-deploy-sync-state.*\.json$"> Require all denied </FilesMatch>` (l'action li legge via FTP, non via HTTP); cancellare via FTP il file di giugno non più usato. Estendere il blocco a `.gitkeep`, `CNAME` (`/CNAME` risponde 200), `PROVENANCE-dossier.md` e ai 65 `.map` pubblicati.
Verifica di chiusura: i due URL rispondono 403/404.

### F08 · Content-Security-Policy debole: `'unsafe-inline' 'unsafe-eval'`, `img-src https:`, host inutili, nessun report  P2
Tipo: raccomandazione motivata (già segnalato in parte come F12 il 21/09)
Prova: header live `script-src 'self' 'unsafe-inline' 'unsafe-eval'`, `img-src 'self' data: blob: https:`; `connect-src` include `https://*.arpalazio.gov.it` (0 riferimenti nel codice: l'host reale è `qa.arpalazio.net`) e `https://gc.zgo.at` (solo in un commento); manca `report-to`/`report-uri`. Nel codice: 45 `<script>` inline nei template, 419 handler `on*=` nelle micro-app statiche; nessun vendor usa `eval` (il commento in `.htaccess:157-159` che lo giustifica per Leaflet non trova riscontro).
Impatto: con `'unsafe-inline'` la CSP non blocca un'iniezione (vedi F21); `'unsafe-eval'` è rimovibile subito.
Correzione: togliere `'unsafe-eval'` (prova in `Content-Security-Policy-Report-Only`); pianificare nonce per gli script inline dei template Hugo e una CSP per cartella per le micro-app; restringere `img-src` ai domini davvero usati; rimuovere i due host morti; aggiungere un endpoint di report.
Verifica di chiusura: header senza `'unsafe-eval'`, zero violazioni nel report dopo 7 giorni.

### F09 · Aggiornamento automatico di Bootstrap Italia senza checksum, con push diretto su `main`  P2
Tipo: difetto confermato (supply chain)
Prova: `.github/workflows/update-bootstrap-italia.yml:190` scarica lo zip della release senza verifica di checksum/firma; `:199-203` `rm -rf` + `unzip`; `:256` `git add -A`; push diretto su `main` senza passare da `validate-pr.yml`; il coalescer pubblica entro ~30 minuti. Altri 81 usi di `actions/*` sono agganciati al tag e non allo SHA (le action di terzi invece sono pinnate: 13 usi).
Impatto: un asset compromesso o corrotto a monte finisce in produzione in automatico, senza revisione né controlli.
Correzione: verificare l'hash della release (o confrontare con npm `bootstrap-italia`), aprire una PR invece del push diretto, far passare i controlli di `validate-pr.yml`; pinnare anche `actions/*` allo SHA (Dependabot li aggiorna).
Verifica di chiusura: il workflow apre PR; `grep -c "actions/.*@[0-9a-f]\{40\}"` copre tutti gli usi.

### F10 · hreflang non reciproco: le 7 home di lingua non dichiarano nessuna alternativa  P2
Tipo: difetto confermato
Prova: live, `/` dichiara 9 tag (`de, en, eo, es, fr, it, pt, ro, x-default`); `/english/`, `/francais/`, `/deutsch/`, `/espanol/`, `/portugues/`, `/romana/`, `/esperanto/` → **0 tag** `hreflang`. Causa: `themes/flavour-pcgenzano/layouts/partials/hreflang-tags.html:32,49` — gli slug delle sezioni di lingua non sono in `$sezioniTradotte` (funziona invece per `cosa-fare-adesso`, `numeri-utili`, `piano-familiare`, `about-this-practice`: 36 pagine con tag corretti).
Impatto: Google ignora i cluster senza link di ritorno: le home in lingua non vengono associate alla home italiana e viceversa.
Correzione: aggiungere le 7 home al partial (o generare i tag dal front matter `language:`), poi verificare con Search Console → "Targeting internazionale".
Verifica di chiusura: `curl -s …/english/ | grep -c hreflang` ≥ 9.

### F11 · Accessibilità WCAG 2.2 AA: rilievi confermati su pagine chiave (axe-core, mobile e desktop)  P2
Tipo: difetto confermato (il sito dichiara WCAG 2.2 AA)
Prova (27 pagine, viewport 390×844 e 1366×900; ogni rilievo riscontrato anche nel codice sorgente):
- **1.4.3 contrasto**: `/english/` e le altre 6 home in lingua — `a.en-tel` "📞 Call 112" reso `#003366` su `#dc3545` (2,78:1): la regola `.article-body a:not(.btn) { color:#003366 }` (`custom.css:1999`) batte `.en-tel { color:#fff }` definita nello `<style>` della pagina. È la chiamata d'emergenza della pagina per stranieri. `/mappa-sito/` 13 elementi `#0891b2` su bianco (3,68:1, `content/mappa-sito/_index.md:106-107,670`; altrove il sito usa già `#0e7490`, `custom.css:876`). Pagina 404: `.display-1` con `opacity:.25` (1,45:1, decorativo).
- **4.1.2 / 1.3.1 label**: `/formazione/radiocomunicazioni-emergenza/sicurezza-sopravvivenza/` — 11 `<input type="checkbox" disabled>` senza label, generati dalle task list Markdown `- [ ]` del file sorgente (impatto "critical").
- **4.1.2 nome accessibile**: `/allerte-meteo/` marker Leaflet `role="button"` senza nome (`.radar-dpc-stella`).
- **Struttura**: `/emergenza/` senza `<h1>` (solo due `<h2>`; `layouts/emergenza/single.html:37`); `/formazione/schede-stampabili/esperimenti-protezione-civile/` ha 33 `<h1>`; `tabella-caa-emergenza-primaria/` 2; `pronto-soccorso-infanzia/` e `sicurezza-in-casa-infanzia/` 0.
- `/cerca/`: campo di ricerca etichettato solo da `title` (interfaccia Pagefind).
Scartati dopo verifica: i contrasti di `.btn-outline-light` in home e in `/giochi/` (sfondo a gradiente scuro non rilevabile dallo strumento) e le segnalazioni di **2.5.8 target size** (indice di pagina, `#assistente-fab`, bottom-nav): nelle esecuzioni in cui comparivano il foglio `custom.css` non era stato caricato per un guasto del proxy dell'ambiente di test (elemento reso 149×17 px anziché 50×50 px fissi come definito in `custom.css:4384-4395`); da riverificare con `pa11y-ci` in un ambiente stabile prima di considerarle.
Impatto: violazioni formali del livello dichiarato, due su percorsi d'emergenza (pulsante 112 delle pagine in lingua, pagina emergenza senza h1).
Correzione: `color:#fff` con specificità sufficiente su `a.en-tel` (7 pagine); palette mappa del sito su `#0e7490`; sostituire le task list con elenchi (o `<label>`); `aria-label` sui marker Leaflet; `<h1>` (anche visivamente nascosto) in `/emergenza/`; una sola h1 nelle schede; `aria-label` sul campo di ricerca.
Verifica di chiusura: axe 0 violazioni sulle 27 pagine da ambiente stabile; `pa11y-ci` esteso a queste URL.

### F12 · Lingua delle parti: l'intero chrome del sito resta in italiano dentro le pagine `lang="en|fr|de|es|pt|ro|eo"`  P2
Tipo: difetto confermato (WCAG 3.1.2)
Prova: `i18n/` contiene solo `it.toml` (2 righe); su `/english/` (screenshot mobile) header "Enti istituzionali / Accedi", bottom-nav "Emergenza / Allerte / Numeri / Cerca", banner cookie, finestra SOS e footer sono in italiano senza `lang="it"`; 33 pagine in 7 lingue hanno `<html lang>` corretto (verificato).
Impatto: lo screen reader legge il menu italiano con la pronuncia inglese/francese; per un residente straniero in emergenza la navigazione resta in italiano.
Correzione: `lang="it"` sui blocchi di chrome nelle pagine in lingua (fix immediato) e, in seguito, stringhe i18n per header/bottom-nav/footer nelle 7 lingue.
Verifica di chiusura: axe `valid-lang`/`html-lang-valid` ok; ispezione manuale delle 7 home.

### F13 · Link esterni rotti: 58 su 1.058 verificati (5,5 %), 26 dei 90 verso protezionecivile.gov.it, compreso il link AgID nella dichiarazione  P2
Tipo: difetto confermato
Prova: verifica del 25/09 con user agent browser (esclusi LinkedIn/YouTube/X che bloccano i bot): 404 su `www.protezionecivile.gov.it` (26: `/it/rischi/rischio-sismico`, `/it/rischi/rischio-meteo-idro`, `/it/approfondimento/sistema-di-allertamento-nazionale-e-regionale/`, `/it/normativa/dlgs-n-1-del-2-gennaio-2018/`, `/it/dipartimento/`, `/it/volontariato`…: il DPC ha ristrutturato il sito, molte URL "vecchie" ora finiscono in `/404/`), `it.wikipedia.org` (6, es. `Terremoto_del_Centro_Italia_del_2016_e_2017`, `Terremoto_di_Ischia_del_2017`, `Alluvione_della_Versilia_del_1996`), `commons.wikimedia.org` (4), `isprambiente.gov.it` (3), `regione.lazio.it` (2), `salute.gov.it` (1: pagina 116117), `agid.gov.it` (1, vedi F04). Pagine coinvolte: almeno 65. Il workflow `check-links-sito.yml` (lychee, settimanale) accetta 403 e 429 ma non dovrebbe lasciar passare i 404: verificare che le issue aperte non vengano chiuse da `stale-issues.yml` prima di essere lavorate.
Impatto: le "fonti" citate a piè d'articolo sono la garanzia di credibilità del sito; un quarto dei rimandi al DPC è morto, compresi quelli in pagine didattiche e nei dossier.
Correzione: sostituire con le URL attuali (per Wikipedia usare i titoli corretti; per il DPC le pagine sotto `rischi.protezionecivile.gov.it`); far fallire il job lychee sui 404 e assegnare le issue a una persona.
Verifica di chiusura: nuovo run lychee con 0 errori 404 sui domini istituzionali.
Elenco completo: allegato `link-esterni-rotti.csv`.

### F14 · Riferimenti a strumenti automatici in contenuti pubblicati (regola permanente del progetto)  P2
Tipo: difetto confermato (rispetto a una regola interna) + una scelta da prendere
Prova: `content/area-download/_index.md:188` *"URL diretto (pronto per AI esterne / Canva / stampa)"* (visibile live). `content/podcast/*.md` (18 pagine) e `themes/…/articoli-da-ascoltare/list.html:89`: *"letta da una voce sintetica"*; i 18 `static/podcast/episodi/*.m4a` portano `handler_name = ISO Media file produced by Google Inc.` e (13 su 18) `encoder = Google`. `content/social-media-policy/_index.md:35,213`: *"pubblicano anche in automatico"* (e le due righe si contraddicono: "un post per articolo distanziati di mezz'ora" vs "due post al giorno"). `content/accessibilita/_index.md:294` *"niente intelligenza artificiale"*. Nessuna firma di generatori in 2.641 immagini (verificate C2PA/XMP) né nei video.
Impatto: per la regola del 28/08 questi testi non dovrebbero esistere; la riga di area-download è la più esplicita. Per i podcast la dichiarazione "voce sintetica" è però anche un obbligo di trasparenza (AI Act, art. 50: i contenuti audio generati devono essere riconoscibili come tali) e va mantenuta in una forma neutra.
Correzione: riscrivere area-download ("pronto per grafiche, Canva, stampa"); social media policy: "pubblicazione programmata" e allineare le due frasi; accessibilità: togliere la negazione; podcast: mantenere "voce sintetica" (o "lettura automatica") come dichiarazione di trasparenza e azzerare i metadati dei file (`ffmpeg -i in.m4a -c copy -map_metadata -1 out.m4a`).
Verifica di chiusura: `grep -rn "AI esterne\|in automatico\|intelligenza artificiale" content/area-download content/social-media-policy content/accessibilita` → 0; `ffprobe` senza tag `encoder`/`handler_name` Google.

### F15 · Cruciverba per la secondaria: griglia "indicativa" con nota di lavorazione pubblicata  P2
Tipo: difetto confermato (materiale scolastico non usabile)
Prova: `static/formazione/schede-stampabili/cruciverba-secondaria/index.html:101` *"Schema indicativo. Le definizioni servono come glossario tecnico, indipendentemente dalla struttura della griglia."*; `:135` *"Nota: lo schema visivo è indicativo. Per uso reale, sostituire con cruciverba puntuale generato con stampino o software (es. Crossword Compiler)…"* — entrambe visibili nella pagina live e in stampa.
Impatto: un docente stampa una scheda il cui schema non corrisponde alle definizioni; il gate `pc-didattica-reviewer` (parità dei formati) l'ha lasciata passare.
Correzione: generare un cruciverba reale (griglia + numerazione coerenti) o ritirare la scheda dal catalogo e dai pacchetti ZIP fino a sostituzione; rimuovere le note di lavorazione.
Verifica di chiusura: `check-parita-schede.py` verde e assenza della parola "indicativo" nel file.

### F16 · Privacy e trasparenza ETS: RPD senza recapito, fornitori senza base giuridica, PEC vuota, contributi pubblici assenti  P2
Tipo: da validare (RPD del Comune / referente del Gruppo)
Prova: `content/privacy/_index.md:18-25`: titolare = Gruppo (C.F. 92011880588), RPD "quello designato dal Comune" senza recapito (art. 13.1.b GDPR richiede i dati di contatto del RPD); `:85-93` GoatCounter *"non raccoglie dati personali"* (tratta IP e user agent) senza responsabile ex art. 28, conservazione, base giuridica; `hugo.toml:37` `goatcounter = "apicuollo"` (account personale, non dell'ente); hosting Aruba assente dall'informativa (log del server); canale Telegram e pagine social senza informativa (solo in social-media-policy:21,37); `:78` `cookie_consent` descritto come "cookie, 12 mesi" ma è una voce `localStorage` senza scadenza (`cookie-banner.html:23-27`) e altre 4 chiavi non sono in tabella; manca il diritto alla portabilità (art. 20). Con soli strumenti tecnici il banner non è richiesto (Garante, linee guida 10/06/2021) e la sua aria-label "accetta i cookie" suggerisce un consenso che non esiste. `hugo.toml:38` `pec = ""` e nessuna PEC nei contenuti (domicilio digitale richiesto al RUNTS). Nessuna sezione sui contributi pubblici ricevuti (L. 124/2017, art. 1 c. 125-bis: pubblicazione entro il 30 giugno, o dichiarazione negativa). `content/trasparenza/_index.md:10` "costituita ai sensi della L.R. 2/2014" (anacronismo per un gruppo del 1991); `:50` promette dataset (esercitazioni, formazione, ore di servizio) che non esistono; il Regolamento non è collegato.
Impatto: adempimenti GDPR/CTS formali ma verificabili da chiunque (Garante, RUNTS, cittadino).
Correzione: recapito RPD del Comune in chiaro; sezioni su GoatCounter (responsabile, IP anonimizzato, retention), hosting, Telegram/social (contitolarità pagine social, C-210/16); tabella storage corretta; banner trasformato in nota informativa non modale o rimosso; PEC del Gruppo; sezione "Contributi pubblici" (anche negativa); trasparenza riallineata.
Verifica di chiusura: check-list dell'RPD firmata; `pec` valorizzato; sezione contributi presente.

### F17 · Contraddizioni residue di autoprotezione: candele nel blackout (versione facile e articolo neve) e numero 1515  P2
Tipo: difetto confermato (residuo di F01 del 21/09 + nuovo)
Prova: canonico `content/rischi-prevenzione/rischi-in-parole-semplici.md:115` e `dossier/quando-salta-la-corrente.md:80` *"usa una torcia, non una candela"*; in contrasto `content/facile-da-leggere/_index.md:247` *"non accendere candele da solo"* (ripetuto nelle versioni en/ro/eo:165) e `content/comunicazioni/2026-12-02-neve-e-ghiaccio…:154` (programmato) *"candele con estrema cautela"*. Numero 1515: `static/quizpc/js/banco_domande/4_incendi_boschivi.js:81` dà per corretto *"chiamare il 112 o 1515"*; `themes/…/assistente/list.html:1305` *"Non chiamare il 115, il 118 o il 1515: nel Lazio non sono più il riferimento per il cittadino"*; `static/llms.txt` attribuisce a numeri-utili un "1530 Guardia Costiera" che la pagina non riporta; `open-data/numeri-utili-emergenza.csv` descrive l'803 555 diversamente da `data/numeri_utili.yaml`.
Impatto: la versione "facile da leggere" è pensata per chi ha più bisogno di istruzioni univoche; sul 1515 il volontario e il cittadino ricevono indicazioni opposte (il 1515 è tuttora attivo a livello nazionale come numero dei Carabinieri forestali; nel Lazio il 112 NUE raccoglie anche le chiamate ai numeri storici: dire "non chiamare il 115/118" è fuorviante, basta dire "chiama il 112").
Correzione: facile-da-leggere in tutte le lingue: "Non usare candele. Usa una torcia."; articolo neve: allineare al divieto; assistente: "Chiama il 112: nel Lazio raccoglie anche le chiamate a 115, 118 e 1515"; quiz: coerente; llms.txt e CSV riallineati.
Verifica di chiusura: `grep -rn "candel" content/facile-da-leggere content/comunicazioni/2026-12-02*` solo con divieto; `grep -rn "1515"` con un'unica formulazione.

### F18 · Archivio `/comunicazioni/`: una sola pagina da 641 KB con 403 immagini e 463 link  P2
Tipo: difetto confermato
Prova: crawl live: `/comunicazioni/` 641.187 byte di HTML, 403 `<img>`, 463 link, 17.503 parole (mediana del sito: 113 KB). Lighthouse non ha completato l'analisi nell'ambiente di test.
Impatto: su mobile l'archivio è la pagina più pesante del sito; il filtro per categoria/anno lavora lato client su tutto il DOM.
Correzione: paginazione Hugo (es. 24 per pagina) con filtri server-side per anno/categoria, oppure caricamento incrementale da `index.json`.
Verifica di chiusura: HTML < 150 KB, Lighthouse mobile completato con performance ≥ 70.

### F19 · Pipeline: deploy urgenti che annullano upload in corso, 1.000 HTML riscritti a ogni build, >1.000 run/giorno  P2
Tipo: raccomandazione motivata (già toccato da F11 del 21/09)
Prova: `scripts/check-allerta.py:481-505` committa anche senza cambio di livello ogni ≥5h45'; `check-allerta.yml:121` lancia un deploy `urgent` a ogni commit e `deploy.yml:29` (concurrency) annulla l'upload in corso (≈4 volte al giorno); la meta `pc-build-sha/time` (`baseof.html:19-22`) cambia ogni pagina a ogni build → ~1.000 HTML ricaricati via FTP (≈5 minuti a deploy; lo stato FTP conta 1.565 `.html`); circa 238 run programmati/giorno più ~288 da cron-job.org e ~400 del watchdog `notifica-ci-fallita`; 9 cron al minuto 0 (lo slot più ritardato da GitHub, incluso `pubblica-programmata`); l'issue automatica di "drift" (`verifica-deploy-aruba.yml:17,81`) consiglia di cambiare `state-name`, esattamente ciò che `deploy.yml:188-201` vieta.
Impatto: più upload lunghi = più finestre in cui il sito è servito a pezzi (l'incidente del 31/08); ritardi degli articoli programmati; costo di runner.
Correzione: deploy urgente solo su cambio reale di livello; impronta di build derivata dallo SHA dei sorgenti (senza orario); ridurre i cron (`aggiorna-dati-sala` ogni 15' produce dati già serviti via raw.githubusercontent); spostare i cron dal minuto 0; correggere il testo dell'issue di drift; retry sul push di `aggiorna-dati-sala.yml:75-76`.
Verifica di chiusura: `git log --since=1.day --format=%s | grep -c "deploy urgente"` ≈ numero di cambi di allerta; stato FTP con < 200 file cambiati per deploy ordinario.

### F20 · `localStorage` senza `try/catch` in 18 accessi su 54 — incluso il banner cookie di ogni pagina  P2
Tipo: difetto confermato (vincolo permanente del progetto)
Prova: `themes/flavour-pcgenzano/layouts/partials/cookie-banner.html:23,27` (incluso da `baseof.html:114` in ogni pagina); `static/quizpc/js/script.js:20-31,188,203`, `js/results.js:2-4`, `js/training.js:2`, `start_quiz.html:86-87,143-145`, `start_training.html:103`. Il quiz salva nome e matricola del volontario in `localStorage` senza mai cancellarli.
Impatto: con storage bloccato (navigazione privata restrittiva, policy aziendali) il banner può lanciare un'eccezione che ferma gli script successivi; il quiz non parte.
Correzione: wrapper unico `safeStorage` (get/set/remove in try/catch) e pulizia dei dati del quiz a fine sessione.
Verifica di chiusura: `grep -rn "localStorage\." themes static/quizpc | grep -v try` → 0 (o analisi AST pulita).

### F21 · Dati esterni inseriti come HTML senza escape nel Monitor (INGV/USGS `bindPopup`)  P2
Tipo: difetto confermato (residuo del pattern corretto nel cruscotto il 21/09, F08)
Prova: `static/monitor/index.html:1342` passa `q.place` (INGV `:1322`, USGS `:1819`) a `bindPopup()` senza `esc()`; `esc()` stesso (`:1981`) non converte l'apice `'`. In totale 277 scritture `innerHTML` non letterali in 85 file.
Impatto: con `'unsafe-inline'` in CSP (F08) un campo malformato da una fonte esterna eseguirebbe script nella pagina. Rischio basso (fonti istituzionali HTTPS) ma il principio "nessuna terza parte scrive HTML per noi" è vostro.
Correzione: `esc()` completo (`&<>"'`) e applicato ai due punti; passare in rassegna le 277 scritture con un linter (`no-unsanitized`).
Verifica di chiusura: grep dei `bindPopup(`/`innerHTML =` con variabili esterne senza `esc(` → 0.

### F22 · SEO on-page: titoli e description fuori misura, pagine senza description, sitemap con URL 403 e canonical divergenti  P3
Prova: 663 titoli su 1.167 > 70 caratteri (mediana 78, max 182: il suffisso "— Protezione Civile Genzano di Roma" pesa 36 caratteri); 284 description > 160 caratteri (max 454); 20 pagine senza description (`/formazionepc/*.html`, `/quizpc/*.html`, 2 schede); 5 titoli duplicati (2 podcast doppi, "Scheda stampabile: A chi chiedere aiuto — Secondaria II" ×3, "Schede stampabili" ×3); sitemap: `/formazione/schede-stampabili/pacchetti/` risponde **403** (cartella senza index), `pronto-soccorso-infanzia/` e `sicurezza-in-casa-infanzia/` hanno canonical verso la pagina madre, `/quizpc/index.html` e `/formazionepc/index.html` redirigono; `/lanterna/` senza canonical; 2 podcast e 2 pagine formazione con description duplicata.
Correzione: suffisso più corto sulle pagine lunghe; description ≤ 160; escludere dalla sitemap le URL non canoniche; index in `pacchetti/` o rimozione.

### F23 · Immagini senza `width`/`height` e layout shift  P3
Prova: 2.120 `<img>` su 7.636 senza dimensioni esplicite; CLS 0,30 su `/giochi/` (soglia 0,10), 0,08 su articoli. 42 PNG/JPEG > 500 KB senza WebP (infografiche da 4-5 MB); `meteo-sinottica-italia.webp` (432 KB) più pesante del PNG (192 KB).

### F24 · Peso del codice per pagina  P3
Prova: mediana 54 KB di script inline per pagina (max 68 KB); `custom.css` 61 KB non minificato (27 KB risparmiabili); 250 KB di `bootstrap-italia.bundle.min.js` inutilizzato in home; 1,5 MB di vendor non referenziato da nessuna pagina (`plugins/`, ESM, `bootstrap-italia.min.js`); 65 `.map` pubblicati; font senza `font-display` (500 ms).
Correzione: spostare lo script inline comune in un file cacheable (dipende da F06); minificare i CSS propri; rimuovere il vendor inutilizzato.

### F25 · Striscia "Caldo estivo" mostrata fino al 30 settembre  P3
Prova: `themes/flavour-pcgenzano/layouts/partials/banner-caldo.html:9-10` — gate sul mese (`ge 6`/`le 9`): il 25/09 la home mostra "Caldo estivo: proteggi te stesso…" mentre lo stesso giorno il sito pubblica "La prima pioggia intensa d'autunno" e "Io non rischio autunno". Il sistema di previsione delle ondate di calore del Ministero della Salute chiude a metà settembre.
Correzione: gate sul 15 settembre (o sul bollettino attivo).

### F26 · Home mobile lunga 17.124 px e tre pulsanti flottanti sovrapposti al contenuto  P3
Prova: screenshot mobile 390×844: home ≈ 20 schermate; `SOS 112`, assistente e accessibilità coprono il testo della card "Sono in emergenza ora" e il corpo di `/english/`; bottom-nav più banner cookie occupano ~30 % dello schermo al primo accesso.
Correzione: ridurre la home (le sezioni sotto "Da dove iniziare?" sono raggiungibili dal menu), un solo FAB, banner cookie non modale.

### F27 · `/emergenza/` è statica: lo stato allerta mostrato è quello dell'ultima build  P3
Prova: alle 20:15 la pagina riportava "Verificato: 25 settembre 2026, 16:11" mentre la home (fetch live) diceva 20:13. Nessuno script (2 richieste, 7 KB: scelta coerente per reti deboli).
Correzione: micro-fetch inline di `/allerta-stato/index.json` con fallback al valore statico, o nota "aggiornato all'ultima pubblicazione".

### F28 · Dati istituzionali minori incoerenti  P3
Prova: mezzi: 8 (`chi-siamo:121-130`, open data) vs "10+" (home `index.html:111`) vs "11" (`dossier/il-nostro-gruppo.md:27`); "40 volontari" come dato reale in `problemi-matematici-pc-primaria/index.html:147` (open data: 32 con almeno un intervento); `static/quizpc/results.html:25` "Iscrizione RUNTS n. G14230" (G14230 è la determina, non il numero di iscrizione); open data: 4 dataset principali senza licenza/fonte/data nel file; `open-data/_index.md:19` "attesa + ammassamento" ma il dataset include 4 aree di ricovero.

### F29 · Dichiarazione di accessibilità: dettagli da correggere  P3
Prova: `content/accessibilita/_index.md:49` cita "art. 3, comma 6, Direttiva 2016/2102" per i contenuti di terzi (il riferimento è art. 1, par. 4, lett. e); `:70` "test settimanale + post-deploy" mentre `audit-sito.yml` gira ogni 6 ore e `lighthouse-audit.yml` due volte al giorno; `:104-114` piena conformità al 10/05/2027 ma audit di terzi al 31/12/2027; obiettivo 2 cita video YouTube/Vimeo incorporati inesistenti; `:249` dice che la pagina è tradotta nelle 7 lingue (non lo è); `_default/single.html:37` usa `role="alert"` per un avviso statico; `lighthouserc.json:17-20` tutte le asserzioni sono `warn` (il job non fallisce mai, ma il riepilogo scrive "errore").

### F30 · `.htaccess`: charset, redirect, header  P3
Prova: `Content-Type: text/html` senza `charset` (i parser che seguono la RFC leggono ISO-8859-1: aggiungere `AddDefaultCharset UTF-8`); `http://protezionecivilegenzano.it/` fa 2 salti (→ `http://www` → `https://www`); `Redirect 301 /assets/` accoda il percorso (`/assets/images/logo.png` → `/images/logo.png` → 404); `X-XSS-Protection` deprecato; COOP/CORP assenti; `ErrorDocument` per 403/410 assenti; `TDM-Reservation: 1` + `TDM-Policy` significa "diritti riservati, TDM consentito solo alle condizioni della policy" (TDMRep): è coerente con CC BY (attribuzione obbligatoria) ma non con il commento di `.htaccess:140-144` che lo descrive come "non divieto"; se l'intento è non riservare nulla, il valore è `0` — decidere e allineare commento e `/.well-known/tdmrep.json`; `robots.txt:17-19` blocca cartelle che hanno già un 301 (Google non vede il redirect); gzip non copre `text/plain` e `application/ld+json`.

### F31 · Repository e dipendenze  P3
Prova: 9.582 file, 1,68 GiB (pack 1,35 GiB anche con un solo commit; 8 job clonano l'intera storia); 54 file > 5 MB (1.093 MB: 18 m4a, 17 PDF, 16 pptx…); 2 podcast da 53,5 MB oltre la soglia GitHub; duplicati byte-identici per 169 MB (2 podcast doppi da 95 MB, un'immagine ripetuta 209 volte in `social-bozze/`); i bot aggiungono 10-25 MB/giorno; nessun `requirements.txt`/`package.json` (15 `pip install` e `npm install` senza versione; solo `pagefind@1.5.2` pinnato); `.devcontainer/setup.sh:64,105` scarica un `.deb` senza checksum ed esegue `curl … | bash`; `theme.toml` dichiara `min_version 0.100.0` con Hugo 0.154.5 in uso; 8 script Python usano `datetime.now()` senza fuso (`notifica-telegram-articolo.py:103-113`: fra le 00:00 e le 02:00 un articolo del giorno risulta futuro); 145 articoli programmati fino al 24/02/2027 (41 nei prossimi 30 giorni, 14 segnalati da `check-articoli-programmati.py` come da riverificare); 3 articoli con norme/link più vecchi di 18 mesi (`check-freshness.py`); 5 pagine chiave senza data di revisione (`sicurezza-scuolabus`, `dopo-emergenza`, `rischi-in-parole-semplici`, `scuole-genzano-rischi-locali`, `emergenza/_index.md`).
Correzione: media su Release/Aruba o LFS, checkout `filter: blob:none` per i bot, manifest con versioni, `zoneinfo("Europe/Rome")` negli script.

### F32 · Stato allerta non recente: dopo 6 ore cambia solo la riga "Verificato", non il colore né il titolo  P2
Tipo: raccomandazione motivata (rilievo ripreso dal rapporto esterno del 25/09 e verificato nel codice)
Prova: `themes/flavour-pcgenzano/static/js/home-allerta.js:100-131` — `segnalaDatoNonRecente()` aggiunge "— dato non recente, consulta il bollettino…" alla riga `#allerta-controllo` solo dopo 6 ore; `segnalaBollettinoNonVerificabile()` scrive "bollettino non verificabile in questo momento"; in entrambi i casi barra verde e titolo "NESSUNA ALLERTA" restano invariati. Le pagine statiche (`/emergenza/`, `data/allerta.json`) portano `ultimo_controllo` della build (25/09 16:11) mentre la home, con fetch lato client, mostrava "Verificato: 20:13" nello stesso istante (vedi F27). Il rapporto esterno aveva osservato un'istantanea con verifica del 23/09 23:36: prova debole (copia di cache), ma il meccanismo che descrive è reale.
Impatto: se la fonte resta irraggiungibile per ore, il messaggio più forte della pagina (colore + titolo) continua a rassicurare; la nota di cautela è in corpo piccolo. Rule 06 del progetto: "mai spacciare per attuale un dato che non lo è".
Correzione: superata la soglia (6 h, o la fine di validità del bollettino), passare barra e titolo a uno stato neutro grigio "Stato allerta non verificato — consulta il Centro Funzionale" con il link al bollettino prima di ogni altra indicazione; stessa regola in `/emergenza/` (statica: nota "aggiornato all'ultima pubblicazione") e nel cruscotto.
Verifica di chiusura: simulare fonte irraggiungibile (blocco di `raw.githubusercontent.com`) e `data-controllo` di 7 ore prima: la barra deve risultare grigia con titolo neutro.

### F33 · Refusi nella pagina indice delle schede stampabili  P3
Prova (rilievo del rapporto esterno, confermato): `static/formazione/schede-stampabili/index.html:344` "sui indicatori chiave"; `:335` e `:354` "indicatori" con iniziale minuscola dopo il punto. La pagina è statica, fuori dal perimetro di `check-refusi.py`.
Correzione: "sugli indicatori"; maiuscole; includere le pagine statiche di `static/formazione/` nello sweep dei refusi.

---

## Controlli superati

- **Disponibilità e struttura**: 1.167 URL su 1.168 rispondono 200 (unico non-200: F22); 0 errori di fetch; tempo mediano di risposta 0,19 s (p95 0,33 s); 0 link interni rotti su 3.738 distinti (2.604 fuori sitemap verificati uno a uno: QR, Braille, PDF, immagini, micro-app).
- **HTML**: un solo `<h1>` su 1.162 pagine; `<main>` e skip link su tutte le pagine Hugo; `lang` corretto (it 1.130, en 7, fr/de/ro/eo 5, es/pt 4, ar 1); JSON-LD valido su tutte le pagine (BreadcrumbList 788, Article 562, WebPage 227, HowTo 12, Event 7, FAQPage 3, Organization/NGO/WebSite); canonical corretto su 1.161; Open Graph e Twitter card su tutte le 789 pagine Hugo; nessun `<iframe>` di terzi (i widget si caricano al clic).
- **Immagini**: 7.636 `<img>`, **0 senza attributo `alt`**; 6.201 con `loading="lazy"`; 2.641 immagini del repo senza firme di generatori (C2PA/XMP), metadati puliti.
- **Sicurezza**: HTTPS con HSTS (1 anno, includeSubDomains); non-www → www; HTTP → HTTPS; `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy` presenti; listing cartelle negato (403); vecchie URL Joomla in 301/410; nessun segreto, chiave o dato personale nel working tree; 13 secret usati solo via `secrets.*`; nessun `pull_request_target`, nessun `curl|bash` in CI; `permissions:` e `timeout-minutes` su 49/49 workflow; action di terzi pinnate a SHA con Dependabot; `security.txt` valido; feed CAP 1.2 ben formato; mirror GitHub Pages con `noindex` e canonical verso la produzione.
- **Vincoli permanenti del progetto**: nessuna traccia di PWA/Service Worker/manifest; `dangerous-clean-slate: false`; solo JavaScript vanilla, nessun CDN, nessun framework; una sola copia di Leaflet per pagina; 0 apostrofi curvi nel front matter; 0 `draft: true`; 0 errori YAML; Bootstrap Italia 2.18.3, Leaflet 1.9.4, Pagefind 1.5.2 aggiornati; Hugo 0.154.5 pinnato in modo coerente in 8 workflow.
- **Accessibilità**: Lighthouse accessibilità 100 su 6 delle 8 pagine misurate (91 `/allerte-meteo/`, 97 `/english/`); axe 0 violazioni su 14 delle 27 pagine analizzate (`/cosa-fare-adesso/`, `/numeri-utili/`, `/comunicazioni/`, `/cruscotto/`, `/aree-attesa/`, `/piano-familiare/`, `/formazione/schede-stampabili/`, `/quizpc/`, `/faq/`, `/scuole/`, `/area-download/`, `/assistente/`, `/rischi-prevenzione/rischio-sismico/`, `/podcast/`); attribuzione ARASAAC su 18/18 pagine; la pagina `/emergenza/` pesa 7 KB in 2 richieste (Lighthouse 100/100/100).
- **Contenuti critici**: numeri 112, 803 555 e 06 9362600 identici in italiano e nelle 7 lingue; 16 aree di emergenza identiche fra YAML, JSON e CSV; `data/emergenza.json` in stato non attivo; nessuna contraddizione su ascensore, sottopassi, "esci subito", fuga di gas, "triangolo della vita" (correttamente smentito in `giochi/primaria/quiz/js/script.js:852-859`); C.O.I. 14°, Zona F, zona AIB 9, RUNTS G14230, E10435833, sede, telefono, nomi di coordinatore/sindaco/assessore coerenti ovunque.
- **Editoriale** (ultimi 10 articoli): description ≤ 160 caratteri 10/10; espressioni gonfiate pressoché assenti (2 in totale); link interni presenti; le correzioni F02, F04, F05, F06 dell'audit interno del 21/09 risultano applicate.
- **Open data**: 29 file (15 JSON, 11 CSV, 3 di supporto) tutti validi; dataset statistici con fonte, licenza, periodo e `generato_il`.
- **Traduzioni**: 33 pagine in 7 lingue con `language:` e `<html lang>` corretti; 0 frammenti italiani non tradotti nel corpo.

## Da validare esternamente (responsabile umano)

1. **Deposito della dichiarazione di accessibilità su form.agid.gov.it** — Comune di Genzano di Roma (F04, issue #995).
2. **Informativa privacy**: recapito RPD, ruolo di GoatCounter/Aruba/ActivePager, contitolarità social, base giuridica ActivePager (art. 6.1.b vs 6.1.e) — RPD del Comune (F16).
3. **Trasparenza ETS**: contributi pubblici (L. 124/2017), PEC, soglie art. 14 CTS, numero della delibera del 1991 — referente del Gruppo (F05, F16).
4. **Attivazione FTPS su Aruba e rotazione della password** — chi ha accesso al pannello Aruba (F01).

## Perimetro, metodo e limiti

- **Live**: crawl di tutti i 1.168 URL della sitemap (status, header, title/description/canonical/robots/hreflang/OG, heading, immagini e alt, JSON-LD, script/CSS, link); verifica di 3.738 link interni distinti e di 1.058 link esterni (esclusi LinkedIn, YouTube e X, che rispondono 404/999 ai client automatici); sonde HTTP su 40 percorsi sensibili; Lighthouse 12 mobile (rete simulata) su 10 pagine; axe-core 4 (WCAG 2.0/2.1/2.2 A-AA) su 27 pagine in viewport mobile e desktop, con verifica visiva via screenshot dei contrasti segnalati; screenshot mobile con emulazione dispositivo.
- **Repository**: clone superficiale del commit `8fbf542`; lettura di `hugo.toml`, `.htaccess`, template, partial, JS, 49 workflow, 110 script, front matter di 1.079 file; esecuzione in sola lettura di `check-freshness.py` e `check-articoli-programmati.py`; scansione metadati di 2.641 immagini, 18 audio, 4 video; grep sistematici per fatti istituzionali, contraddizioni di autoprotezione, riferimenti a strumenti automatici.
- **Limiti**: la storia git non è stata analizzata (clone shallow: uno scanner di segreti sull'intera storia resta consigliato); le metriche Lighthouse provengono da un ambiente con proxy e vanno confermate su PageSpeed Insights (F06); nessuna modifica è stata applicata: tutti i rilievi restano aperti per la lavorazione interna (Categoria A/B secondo rule 10).
- **Confronto con l'audit interno del 21/09**: 12 dei 15 rilievi risultano chiusi; restano aperti F11 (cron) e F12 (host CSP) come raccomandazioni e F09 (deposito AgID). Due correzioni (candele F01, AIB F03) sono state applicate a un solo file e non propagate: questo audit le riapre come F17 e F03.

## Prossimo audit

Dopo la chiusura dei 5 P1 e di F06/F07/F10/F13 (interventi da poche ore ciascuno), un audit mirato su: cache e prestazioni (PageSpeed reale), hreflang in Search Console, link esterni (nuovo run lychee), quiz e materiali con istruzioni di autoprotezione (parità completa pagina ↔ quiz ↔ schede ↔ giochi ↔ traduzioni).
