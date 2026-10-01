# GitHub + Aruba — Deploy e Infrastruttura

## Ambienti di pubblicazione

Il sito viene pubblicato su due ambienti distinti ad ogni push su `main`:

| Ambiente | URL | Metodo |
|---|---|---|
| Aruba (produzione) | https://www.protezionecivilegenzano.it/ | FTP via GitHub Actions |
| GitHub Pages (preview) | https://sviluppoitaliadigitale.github.io/sito-pc-genzano/ | GitHub Pages API |

## Workflow CI/CD

Il file `.github/workflows/deploy.yml` gestisce il deploy automatico:
1. Esegue `hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"` per Aruba
2. Esegue `hugo --minify` per GitHub Pages
3. Carica su Aruba via FTP usando i secret GitHub: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`
4. Pubblica su GitHub Pages tramite l'azione ufficiale

## Cartelle escluse dal deploy FTP (contenuto lato server)

L'azione FTP usa `dangerous-clean-slate: false` e una lista di esclusioni per proteggere contenuto gestito manualmente sul server Aruba. Queste cartelle **non vengono né caricate né aggiornate né rimosse** dal deploy:

```yaml
exclude: |
  **/documenti/**
```

**Conseguenza operativa:** un file depositato via git in `static/documenti/` **non arriverà mai su Aruba**. Compare solo nella build locale e su GitHub Pages. La cartella `static/documenti/` resta gestita manualmente sul server Aruba perché contiene materiale ereditato dal sito precedente (pieghevoli, kit "Io Non Rischio", schede storiche) mai migrato nel repo.

**Storico delle esclusioni (rimosse aprile 2026):** fino al 24 aprile 2026 la lista escludeva anche `**/cartelli/**`, `**/giochi-bambini/**`, `**/formazionepc/**`, `**/quizpc/**`. Dopo l'incidente del cartello AR4 Salesiani (un audit del sito ha rilevato che l'immagine era mancante sul server, ma non c'era modo di accorgersene dal repo), queste esclusioni sono state rimosse per eliminare il drift tra repo e server. I file vivono ora nel repo come unica fonte di verità e deployano automaticamente.

**Cartelle canoniche per nuovi file statici depositati via git:**

| Contenuto | Cartella | URL pubblico |
|---|---|---|
| Manuali tecnici permanenti citati da più articoli | `static/manuali/` | `/manuali/nome.pdf` |
| Allegati specifici di un articolo | `static/allegati/AAAA/` | `/allegati/AAAA/nome.pdf` |
| Comunicati stampa firmati | `static/comunicati/AAAA/` | `/comunicati/AAAA/nome.pdf` |
| Segnaletica aree di emergenza | `static/cartelli/` | `/cartelli/nome.png` |
| Immagini di copertina / foto evento | `static/images/` | `/images/nome.webp` |
| Archivio storico immagini | `static/images/archivio-storico/` | `/images/archivio-storico/nome.ext` |
| Pittogrammi ISO 7010 (sicurezza standard) | `static/pittogrammi/iso7010/` | `/pittogrammi/iso7010/nome.svg` |
| Pittogrammi ARASAAC (comprensione cognitiva) | `static/pittogrammi/arasaac/` | `/pittogrammi/arasaac/nome.png` |

Se aggiungi nuove esclusioni al workflow, aggiorna anche questa tabella e la **Parte 1.10** e **Parte 10.2** di `MANUALE-SITO.md`.

**Cartella `riferimenti-interni/` (NON deployata):** la cartella di livello root `riferimenti-interni/` contiene documentazione di lavoro per maintainer/AI di supporto (norme tecniche copyrighted, draft di consultazione, materiale interno). **Non viene deployata** perché Hugo costruisce solo da `content/`, `static/`, `themes/`, `data/`, `assets/`, `layouts/`: una cartella di livello root estranea a queste resta fuori dal sito pubblico, sia su Aruba che su GitHub Pages. Niente esclusione FTP esplicita serve perché Hugo non genera alcun output da quella cartella. Specifiche complete in regola `04c-hugo-static-cartelle.md` e in `riferimenti-interni/README.md`.

## Regole operative

- Il branch `main` è il branch di produzione: ogni push avvia il deploy.
- I secret FTP non vanno mai committati nel repository.
- Monitora i deploy nella tab Actions del repository GitHub.
- In caso di build rotta, il deploy non avviene: il sito rimane all'ultima versione funzionante.

## Regole di compatibilità

Ogni modifica deve essere compatibile con:
- Build statica di Hugo (nessun server-side rendering, nessuna API runtime) — **una sola eccezione, dichiarata: `static/api/aerei.php`**, vedi sotto
- Deploy FTP su Aruba (percorsi degli asset devono essere corretti per entrambi i baseURL)
- GitHub Pages con subpath `/sito-pc-genzano/` (usa `{{ absURL }}` o `{{ relURL }}` nei template, mai percorsi assoluti hardcoded)
- Certificato HTTPS esistente su Aruba (non modificare la configurazione DNS senza coordinamento)

## L'unica eccezione al sito statico: i ponti in `static/api/` (22/09/2026)

🔴 Il sito è statico, e resta statico. I **soli file eseguiti dal server** stanno in `static/api/`, e stanno qui documentati perché una deroga non dichiarata è una trappola per chi verrà dopo. Al 22/09/2026 sono due, nati dallo stesso vincolo e scritti sullo stesso schema:

| file | fonte | perché non si legge dal browser | licenza del dato |
|---|---|---|---|
| `aerei.php` | adsb.lol | risponde senza intestazione CORS | ODbL 1.0 |
| `pronto-soccorso.php` | Regione Lazio — Salute Lazio | risponde **400** se la richiesta porta `Origin` | CC BY 4.0 |

🔴 **Un terzo ponte non si aggiunge per comodità.** La domanda da farsi è sempre la stessa, e in quest'ordine: la fonte espone il CORS? (allora si legge dal browser e il ponte non serve); il dato regge una fotografia committata ogni quarto d'ora? (allora si usa quella, come per GDACS, EMS e MeteoAlarm); solo se entrambe le risposte sono no, e il dato serve **in diretta**, si scrive un ponte — con l'indirizzo fisso nel file, mai preso da chi chiama.

**Perché esiste.** L'utente ha chiesto i mezzi aerei in tempo reale, *«serve per forza vedere in che posizione sono durante un'emergenza»*. Nessuna fonte ADS-B gratuita espone il CORS — verificato il 22/09/2026 con GET reali, non con HEAD (che sul CORS può mentire): adsb.fi e adsb.lol rispondono 200 con i dati ma senza intestazione, OpenSky limita il CORS al proprio dominio, airplanes.live risponde 403. Il browser quindi non può leggerle, e una fotografia committata non è «tempo reale»: il minimo dello scheduler di GitHub Actions è di cinque minuti, in pratica ritarda di ore, e a cadenza alta il repository crescerebbe di GB l'anno. Un intermediario è **l'unica strada tecnica**, e questa è quella che non aggiunge nulla fuori da ciò che il Gruppo già controlla: niente account nuovi, niente credenziali nuove, niente servizi di terzi che sappiano chi sta guardando.

**Le alternative e perché no.** Un *Cloudflare Worker* avrebbe tenuto il sito statico, ma sarebbe stato il primo componente fuori da GitHub e Aruba, con credenziali proprie e fuori dai controlli automatici del sito. Incorporare una mappa altrui non si può: tutte vietano l'iframe tranne ADS-B Exchange, che lo consente tecnicamente ma lo proibisce nelle condizioni d'uso (rule 04a).

**Cosa comporta, e non va dimenticato.**
- **Solo su Aruba.** Su GitHub Pages il PHP non gira e in locale nemmeno: là la Sala ricade sulla fotografia committata **e lo dichiara nella scheda** (i mezzi aerei), oppure spegne la scheda dicendo che in quell'ambiente il dato non c'è (il pronto soccorso, che una fotografia non ce l'ha: un carico di pronto soccorso di ieri non serve a nessuno). È la condizione normale di metà degli ambienti in cui la pagina si apre, non un caso limite.
- **La CSP non cambia**: la chiamata è di stessa origine e `connect-src 'self'` la copre già. È un vantaggio di questa strada rispetto al Worker, che avrebbe richiesto un host nuovo in `connect-src`.
- **Non è un proxy generico**: l'indirizzo di destinazione è scritto nel file, non arriva da chi chiama. Un proxy che accetta un URL dall'esterno diventa un ponte per raggiungere qualunque cosa a nome del nostro dominio. Chi tocca quel file non aggiunga mai un parametro che diventi parte dell'URL chiamato.
- **Se il PHP non venisse eseguito**, il server servirebbe il sorgente come testo: nessun segreto dentro (non ce ne sono, e non ce ne devono entrare), e la Sala scarta una risposta che non sia il JSON atteso.
- **Va trattata con riguardo la fonte**: una copia locale di dodici secondi fa da cuscinetto, così cento visitatori restano poche richieste al minuto. adsb.lol chiede di essere avvisata per usi di produzione: se il traffico cresce, si scrive loro.

**Licenza.** I dati sono di **adsb.lol sotto ODbL 1.0**, la stessa di OpenStreetMap, che consente esplicitamente la ridistribuzione con attribuzione — obbligatoria, e sta nella scheda. 🔴 Si è passati da adsb.fi proprio per questo: le loro condizioni dicono *«open data is for personal, non-commercial use only»*, e un sito istituzionale pubblico «personale» non è. Valeva anche per la fotografia, che è stata spostata sulla stessa fonte.

## Rollback

Per tornare a una versione precedente:
```bash
git revert HEAD          # Crea un commit di ripristino (preferibile)
git push origin main     # Avvia il redeploy
```
Evita `git reset --hard` su `main` se il commit è già stato pushato.

## Header HTTP — `.htaccess` su Aruba

Il file `themes/flavour-pcgenzano/static/.htaccess` configura gli header di sicurezza che Apache invia su Aruba. Aruba supporta `mod_headers` ma GitHub Pages no, quindi questo file è effettivo **solo in produzione**.

**Permissions-Policy (header sensibile):**

```apache
Header always set Permissions-Policy "geolocation=(self), microphone=(), camera=()"
```

- `geolocation=(self)` — il sito può usare la Geolocation API del browser. È necessario per il bottone "Centra sulla mia posizione" sulla mappa `/cartografia/`.
- `microphone=()` e `camera=()` — negati a tutte le origini (non servono).

**ATTENZIONE:** non sostituire `geolocation=(self)` con `geolocation=()`. La forma `()` (lista vuota di origini) **disabilita la Geolocation API anche per il sito stesso**, e il browser blocca silenziosamente `navigator.geolocation.getCurrentPosition()` mostrando un errore "Geolocation has been disabled in this document by permissions policy". Questo è successo una volta in produzione e ha rotto il bottone della mappa cartografia. Se aggiungi nuove API (es. `payment`, `usb`), aggiungile in coda al valore con `(self)` o `()` esplicito.

**Licenza e TDM negli header (15/08/2026):** `.htaccess` emette `Link: rel="license"` CC BY 4.0 su tutte le risorse (variante CC BY-NC-SA 4.0 per `/pittogrammi/arasaac/` via `SetEnvIf`) + `TDM-Reservation: 1`/`TDM-Policy` (riserva dei diritti di text and data mining, con le condizioni d'uso in `/note-legali/`), speculari a `static/.well-known/tdmrep.json`.

**Redirect, header ed errori (26/09/2026, audit F30):** le cartelle del vecchio sito (`/assets/`, `/cache/`, `/immagini_web/`, `/sito_pc/`, `/sitovecchio/`, `/piano_protezione_civile/`) usano `RedirectMatch` con **destinazione fissa**: la direttiva `Redirect` accoda il resto del percorso e produceva 404 (`/assets/images/logo.png` → `/images/logo.png`). Il dominio senza www va su `https://www` in un salto. `X-XSS-Protection` è rimosso (obsoleto), c'è `Cross-Origin-Opener-Policy: same-origin-allow-popups`; `Cross-Origin-Resource-Policy` **non** si imposta, perché impedirebbe ad altri siti di mostrare le nostre immagini e i dati aperti. 403 e 410 mostrano la stessa pagina di recupero del 404. Le modifiche a `.htaccess` si provano prima con un Apache locale (`apt-get install apache2`, `AllowOverride All`, moduli rewrite/headers/deflate/alias) sul sito compilato per Aruba. Dettagli in rule 04a § "Partial `speculation-rules` + OpenSearch + TDMRep".

**CSP promossa a enforcing (15/08/2026):** l'header è ora `Content-Security-Policy` attivo (era Report-Only dal 10/05) con `upgrade-insecure-requests` reintrodotta. **Stretta dello stesso giorno:** rimosso `cdn.jsdelivr.net` da `script-src`/`style-src`/`font-src` (tutto è vendorizzato self-hosted, verifica meccanica: zero riferimenti nel repo) — se in futuro si reintroduce un asset da CDN, va prima riaggiunto alla policy. 🔴 Quando si aggiunge una nuova fonte dati al cruscotto o un nuovo widget, aggiornare anche `connect-src`/`frame-src` della policy: dimenticarlo produce una scheda vuota solo su Aruba (GitHub Pages non invia header). Dopo ogni modifica alla CSP: smoke test post-deploy su `/cruscotto/`.

## Cache HTTP — DISATTIVATA, non reintrodurla (12/09/2026)

🔴 **Istruzione permanente dell'utente (12/09/2026)**: *"elimina ogni cache e non metterla più"*, dopo problemi ripetuti di aggiornamenti non visibili sul sito live. Il blocco "Cache" di `themes/flavour-pcgenzano/static/.htaccess` invia su **ogni risorsa** (HTML, CSS, JS, immagini, PDF, ZIP, JSON, XML, font):

```apache
ExpiresActive Off
Header always set Cache-Control "no-store, no-cache, must-revalidate, max-age=0"
Header always set Pragma "no-cache"
Header always set Expires "0"
FileETag None
```

- **Vietato** reintrodurre `ExpiresByType`, `max-age > 0`, `immutable`, `stale-while-revalidate`, service worker con precache, o altri meccanismi che conservino una copia nel browser o in un proxy. Vale anche per le pagine statiche in `static/**` (stesso `.htaccess`).
- **Storia**: dal 06/06/2026 la policy era "pagine e codice senza cache, immagini 1 anno, PDF 1 mese". Restavano stantii i file che cambiano **mantenendo lo stesso nome** (cover rigenerate, `manuale-protezione-civile.pdf`, deck, pacchetti ZIP, open data, feed) e tutto ciò che non aveva una regola esplicita (JSON, XML, font, ZIP → cache euristica del browser, spesso giorni).
- I parametri `?v=<hash>` sui CSS/JS del tema e `?v=<timestamp>` sulle cartine meteo restano come rete di sicurezza per gli ambienti che ignorano `.htaccess` (GitHub Pages serve con `max-age=600`): non sono cache, sono anti-cache. Non toglierli, non aggiungerne altri per compensare una cache che non c'è.
- **Costo accettato**: ogni visita riscarica gli asset (bundle Bootstrap Italia ~250 KB compresso, CSS ~40 KB compresso, immagini della pagina). Lighthouse segnalerà `uses-long-cache-ttl`: è atteso, non è una regressione da correggere.
- **Transizione**: i visitatori che avevano già in cache un'immagine o un PDF con la vecchia scadenza (1 anno / 1 mese) continuano a vederli finché il browser non li scarta o finché non fanno un aggiornamento forzato (Ctrl+F5 / svuota dati del sito). Da quel momento la nuova policy vale per sempre.

## Workflow GitHub Actions — qualità YAML

I file in `.github/workflows/*.yml` sono validati da GitHub al momento del push. Se la validazione fallisce il run viene marcato "completed failure" con 0 job eseguiti, ma **nessuna issue viene aperta** e il problema può passare inosservato per settimane.

**Pattern velenoso da evitare** (causa errore di parsing YAML strict):

```bash
DIFF=$(python3 -c "
import datetime
try:
  d = datetime.datetime.strptime('$REV', '%Y-%m-%d').date()
  print((datetime.date.today() - d).days)
except Exception:
  print(-1)
")
```

Le righe Python (`import…`, `try:`, `print…`) iniziano a colonna 1, e il parser YAML le legge come nuove chiavi top-level rompendo la struttura. **Sostituiscilo con aritmetica bash usando `date`**:

```bash
TS=$(date -u -d "$REV" +%s 2>/dev/null || echo "")
[ -n "$TS" ] && DIFF=$(( ($(date -u +%s) - TS) / 86400 )) || DIFF=-1
```

Per validare un workflow prima del push:
```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/<file>.yml'))"
```

Se python3 yaml lo accetta, GitHub Actions lo accetterà sicuramente.

## Workflow `scarica-foto-automatica.yml` — supporto editing da mobile

⚠️ **DEPRECATO al 3 maggio 2026** per il caso d'uso "foto da fonti ufficiali nel banner". Il marker `# TODO-foto-*` è ora **bandito** da CLAUDE.md punto 9 perché:
1. Il workflow popola/sovrascrive `image:` del frontmatter con la foto scaricata → viola la regola "BANNER COL TITOLO INTOCCABILE"
2. Il marker `# TODO-foto-*` nel corpo Markdown è renderizzato da Hugo come `<h1>` finché il workflow non lo rimuove → se `deploy.yml` finisce prima del workflow CI il sito va live col marker H1 visibile (incidente reale: articolo radiocomunicazioni del 3 maggio 2026, vedi commit `4e8c289` di rimozione urgente).

**Procedura corretta** per inserire foto da fonti ufficiali in articoli: vedi agent `pc-image-fixer` (`.claude/agents/pc-image-fixer.md`) sezione "4. Foto da fonti esterne" — flusso WebFetch + curl + `applica-fascia-foto.sh` + shortcode `{{< foto >}}` inline nel corpo. La cover tipografica del banner resta intatta.

Lo step 2 del workflow (`auto-cover-mancanti.py`) per la generazione delle cover tipografiche per articoli con `image: ""` resta **valido e attivo**.

Lo step 1 (download foto da marker) resta nel codice ma di fatto non viene più triggerato perché la regola vieta i marker. Conservato per: (a) eventuale uso futuro se il workflow venisse riscritto per popolare foto INLINE invece che banner; (b) compatibilità retroattiva con articoli vecchi che potrebbero ancora avere marker.

---

**Documentazione storica del marker** (per riferimento, non più operativa):

L'articolo si pubblicava con `image: ""` e includeva nel frontmatter **un solo** marker di servizio (uno tra i seguenti, in base alla fonte da cui prendere la foto):

```
# TODO-foto-wikipedia: bash scripts/foto-da-wikipedia.sh "Titolo Pagina Wikipedia" slug-articolo [lang]
# TODO-foto-nasa:      bash scripts/foto-da-nasa.sh      "search query"            slug-articolo
# TODO-foto-usgs:      bash scripts/foto-da-usgs.sh      shakemap <eventid>        slug-articolo
# TODO-foto-noaa:      bash scripts/foto-da-noaa.sh      "URL diretto NOAA"        "Descrizione" slug
# TODO-foto-pexels:    bash scripts/foto-da-pexels.sh    "search query"            slug-articolo
# TODO-foto-pixabay:   bash scripts/foto-da-pixabay.sh   "search query"            slug-articolo
# TODO-foto-unsplash:  bash scripts/foto-da-unsplash.sh  "search query"            slug-articolo
```

**Quando usare quale fonte:**

| Tipo di articolo | Fonte consigliata | Crediti | API key |
|---|---|---|---|
| Anniversario evento storico (terremoti famosi, alluvioni, eruzioni) | Wikipedia (it/en) | sì (CC) | no |
| Fenomeno globale visto dallo spazio (uragani, eruzioni, ondata calore) | NASA | no (PD) | no |
| ShakeMap di un terremoto specifico | USGS (serve eventid da `earthquake.usgs.gov/earthquakes/search/`) | no (PD) | no |
| Uragani, NHC tracks, foto storiche meteo | NOAA (URL diretto) | no (PD) | no |
| Personaggio storico, opera, libro, organizzazione | Wikipedia | sì (CC) | no |
| Foto stock generica (atmosfera, persone in azione) | Pexels o Unsplash | no (cortesia) | sì (gratuita) |
| Foto stock alta qualità (illustrazioni, oggetti, paesaggi) | Pixabay | no | sì (gratuita) |

**Le 3 fonti stock (Pexels, Pixabay, Unsplash)** richiedono API key gratuita configurata come **GitHub Secret** (`PEXELS_API_KEY`, `PIXABAY_API_KEY`, `UNSPLASH_ACCESS_KEY`). Se mancanti, il workflow apre issue automatica con messaggio chiaro e l'articolo va riprovato con un'altra fonte. Le 4 fonti istituzionali (Wikipedia/NASA/USGS/NOAA) funzionano sempre senza API key.

Al successivo push su `main`, il workflow `.github/workflows/scarica-foto-automatica.yml` (runner Ubuntu, rete libera):
1. Scansiona `content/comunicazioni/*.md` cercando i marker `TODO-foto-(wikipedia|nasa|usgs|noaa|pexels|pixabay|unsplash)`.
2. Per ogni articolo trovato: estrae il marker, verifica che lo script chiamato sia in **whitelist** (`foto-da-wikipedia.sh`, `foto-da-nasa.sh`, `foto-da-usgs.sh`, `foto-da-noaa.sh`, `foto-da-pexels.sh`, `foto-da-pixabay.sh`, `foto-da-unsplash.sh`) — qualunque altro nome viene rigettato per sicurezza.
3. Esegue il comando con `bash -c "$CMD"` dopo la verifica whitelist.
4. **Successo**: aggiorna il frontmatter con `scripts/aggiorna-frontmatter-foto.py` — popola `image:` + `image_credit:` + `image_source_url:`, rimuove la riga TODO.
5. **Fallimento** (titolo Wikipedia non esiste, query NASA vuota, ShakeMap inesistente, ecc.): chiama `scripts/rimuovi-marker-foto.py` per rimuovere il marker pendente. **Why**: senza questa rimozione, ad ogni run il workflow ri-trova lo stesso marker, ri-prova lo stesso download, ri-fallisce, ri-apre issue — loop infinito di issue duplicate (è successo dal 29 aprile al 2 maggio 2026, 13 issue accumulate prima del fix). Lo step successivo `auto-cover-mancanti.py` genera la cover tipografica come fallback definitivo.
6. Committa con messaggio `[skip-foto-wiki] Cover automatiche: N foto + M cover tipografiche` per evitare loop del trigger push.
7. Triggera esplicitamente `deploy.yml` via `gh workflow run deploy.yml` (i push fatti dal `GITHUB_TOKEN` non auto-triggerano i workflow `push`).
8. Se uno o più articoli sono falliti, apre **issue di follow-up** che spiega: il marker è già stato rimosso + la cover tipografica è già stata generata + come ri-aggiungere un marker se l'utente vuole davvero una foto vera (titolo diverso o fonte diversa).

**Permissions richiesti dal workflow**: `contents: write` (per il commit) + `actions: write` (per `gh workflow run`) + `issues: write` (per l'issue di fallback).

**Cross-platform via Pillow**: `applica-fascia-foto.py` è la logica reale di composizione (foto + fascia blu + logo + testo Liberation Sans). Usa Python+Pillow al posto di ImageMagick per evitare problemi cronici (delegate WebP, policy.xml, font discovery, sintassi v6 vs v7). `applica-fascia-foto.sh` è solo un wrapper di compatibilità che invoca lo script Python. Dipendenze runner: `python3-pil` + `fonts-liberation` (apt install). Compressione progressiva: qualità 85→30, poi riduzione larghezza 1000→700px finché `output ≤ 200 KB`.

**Idempotenza**: `aggiorna-frontmatter-foto.py` non sovrascrive `image:` se già popolato. Riesecuzione del workflow su articoli senza marker non fa nulla.

**Sicurezza**: il workflow esegue il comando trovato nel marker via `bash -c`. Per evitare iniezioni di script arbitrari:
1. Il marker deve corrispondere alla regex `^# TODO-foto-(wikipedia|nasa|usgs|noaa|pexels|pixabay|unsplash):` (solo i 7 marker noti).
2. Il primo binario chiamato deve essere uno script in whitelist (i 7 `foto-da-*.sh`).
3. Tutti i parametri sono passati come argomenti dello script, non come codice eseguibile.

**Aggiungere una nuova fonte** (es. Copernicus): (a) creare `scripts/foto-da-NUOVA.sh` con stesso pattern di output (stampa Origine/Autore/Licenza); (b) aggiungere `foto-da-NUOVA.sh` alla `ALLOWED_SCRIPTS` del workflow + nuovo `case` nello switch FONTE; (c) aggiungere `nuova` alla regex del marker; (d) aggiornare archetype + doc.

**Caso particolare: NOAA.** A differenza di Wikipedia/NASA (API JSON ricche) e USGS (API earthquake), NOAA non ha un'API unificata di ricerca immagini. Lo script `foto-da-noaa.sh` accetta direttamente l'**URL diretto dell'immagine** (l'utente lo trova manualmente su `photolib.noaa.gov`, `weather.gov`, `nhc.noaa.gov`, `nesdis.noaa.gov`) + una stringa descrittiva del contesto + slug. Whitelist di sicurezza: solo URL `*.noaa.gov` o `weather.gov` (NWS). Esempio marker: `# TODO-foto-noaa: bash scripts/foto-da-noaa.sh "https://www.nhc.noaa.gov/.../katrina.png" "Traccia uragano Katrina (NHC)" 2026-08-29-katrina`.

### Cover tipografiche automatiche (`auto-cover-mancanti.py`)

Lo stesso workflow `scarica-foto-automatica.yml` ha un **secondo step** che, dopo il download foto, genera **cover tipografiche istituzionali** (gradiente blu + titolo + badge + fascia con logo) per gli articoli rimasti senza copertina. Garantisce che nessun articolo venga pubblicato senza immagine.

Lo script `scripts/auto-cover-mancanti.py` agisce così:
1. Itera tutti gli articoli in `content/comunicazioni/*.md`
2. Seleziona quelli con `image: ""` (vuoto) **E** senza marker `# TODO-foto-*` (in attesa di download da fonti esterne)
3. Per ciascuno: lancia `python3 scripts/genera-cover.py <file>` → produce `static/images/<slug>.webp`
4. Aggiorna `image: ""` → `image: "/images/<slug>.webp"` e `image_alt: ""` → `image_alt: "Cover dell'articolo: <title>"` **solo se vuoti** (mai sovrascrive)

**Sicurezza editoriale**: lo script **non sovrascrive mai** una foto utente custom. Se l'articolo ha già `image: "/images/foto-evento-utente.webp"`, viene saltato.

**Dipendenze runner**: `fonts-liberation` (font Liberation Sans usato dallo script di generazione cover) — installato dal workflow nello step `apt install`.

**Esecuzione locale**: `python3 scripts/auto-cover-mancanti.py` (oppure `--dry-run` per vedere cosa farebbe senza modificare).

**Risultato editoriale**: il sito non avrà mai articoli pubblicati con copertina mancante. livelli di fallback in cascata:
1. **Foto vera** (utente / Wikipedia / NASA / USGS via marker)
2. **Cover tipografica istituzionale** (gradiente blu + titolo, generata automaticamente)
3. **Default SVG** (`images/notizia-default.svg`) — solo come fallback estremo se anche cover tipografica fallisce

## File stantii su Aruba — manifesto della build, verifica e riparazione (dal 01/10/2026)

⚠️ **Problema noto del deploy FTP** (`dangerous-clean-slate: false`): l'azione `SamKirkland/FTP-Deploy-Action` v4.4.0 (pinnata a commit SHA in `deploy.yml` dal 15/08/2026 — hardening supply-chain: le action di terze parti che maneggiano segreti sono puntate allo SHA immutabile, non al tag mutabile; per aggiornarle si cambia SHA + commento versione) carica **solo i file cambiati** rispetto a uno stato di sincronizzazione salvato su Aruba. Se quello stato è sbagliato, o un caricamento viene interrotto a metà (merge in rapida successione, build fallite, timeout), alcune pagine restano **vecchie sul server** senza che nessuno se ne accorga. Storia: 12-13/05/2026 (pagine con l'header di aprile dopo 4 deploy falliti), 01/07/2026 (su Aruba convivevano `chi-siamo` di aprile, `allerte-meteo` di maggio e la home di luglio, col semaforo di allerta vecchio).

### Perché il caricamento era lento, e che cosa è cambiato il 01/10/2026

Fino al 01/10/2026 **ogni pagina cambiava a ogni build** per due righe che non c'entravano col contenuto: l'ora della build nella barra «Sito aggiornato il … alle HH:MM» (`utility-bar.html`, `now` di Hugo) e la meta `<meta name="pc-build-sha">` con lo SHA del commit (`baseof.html`). Risultato: ~1.100 sostituzioni FTP a ogni deploy, 17 minuti a circa 0,8 s l'una, anche per un solo articolo (misurato il 01/10/2026: con l'articolo della farmacia i file davvero cambiati erano 73). Più lungo è il caricamento, più è probabile che venga interrotto — ed è così che nascono le pagine vecchie.

Da quel giorno le pagine **non portano più nulla che dipenda dalla build**:

- l'ora «Sito aggiornato il» la scrive il **browser** leggendola da `/build-info.js` (output format BUILDINFO, un file solo, già usato dalle pagine statiche tramite `site-chrome.js`); il blocco resta nascosto finché non è stata letta, così senza JavaScript non compare un'icona senza testo;
- la meta `pc-build-sha` non esiste più; SHA e orario della build stanno in `/build-info.js` e in `data/buildinfo.json`;
- i feed RSS hanno `lastBuildDate` = ultima modifica (git) fra le voci del feed, non l'ora della build; l'id di fallback del partial `external-widget` deriva dall'URL del widget e non da `now.UnixNano`.

Verifica fatta prima di pubblicare: due build a un minuto di distanza differiscono per **5 file** (`build-info.js`, i tre JSON con il campo `generato`, `stato-sistema/`) invece di 1.086. Chi aggiunge un template con `now` di Hugo in una pagina rimette quella pagina fra i file ricaricati a ogni deploy: `now` va usato solo dove l'informazione cambia davvero (banner stagionali, soglie di età), mai per «firmare» la pagina.

🔴 **Non reintrodurre l'ora di build o lo SHA nelle pagine** per «vedere se è aggiornata»: per quello esiste il manifesto qui sotto, che dice di più e non costa un ricaricamento.

### Il manifesto della build e la guardia anti-stale

- **`scripts/genera-manifest-build.py`** scrive `public/build-manifest.json`: l'impronta sha256 di ogni file della build (esclusi le sottocartelle di `pagefind/`, i cui nomi derivano già dal contenuto, e `documenti/`, gestita a mano su Aruba). Un file solo, ~750 KB, generato da `deploy.yml` prima del caricamento (anche per la copia su GitHub Pages).
- **`scripts/verifica-deploy-aruba.py`** confronta le pagine servite dal sito con il manifesto, con richieste senza cache: `build-info.js`, le pagine critiche (home, allerte, emergenza, numeri utili, archivio, CAP…), l'ultimo articolo, le pagine chieste con `--pagine`, un campione casuale (`--campione N --seme X`) e, con `--precedente`, **tutti i file che il deploy doveva cambiare**. Con `--ripara` ricarica via FTPS, dalla build locale, i soli file diversi e li ricontrolla (credenziali `FTP_SERVER`/`FTP_USERNAME`/`FTP_PASSWORD`, cartella `FTP_SERVER_DIR`; mai `documenti/`). Il vecchio `verifica-fingerprint-live.sh` resta come involucro di compatibilità.
- **In `deploy.yml`**, prima dell'FTP si genera il manifesto e si scarica quello **servito in quel momento** dal sito: la differenza fra i due è l'elenco esatto dei file da cambiare. Dopo l'FTP lo step «🔁 Verifica il sito live contro la build e ripara» controlla quei file (fino a 250, poi un campione) più le pagine critiche e 30 a caso, ricarica i diversi e ricontrolla. Non ferma il deploy (`continue-on-error`): scrive l'esito nel riepilogo del run.
- **`verifica-deploy-aruba.yml`**, dopo ogni deploy riuscito, rifà il controllo in modo indipendente (pagine critiche + ultimo articolo + 60 a caso, con ritentativi ampi) e apre/aggiorna 1 issue `automazione`+`urgente` che si chiude da sola al rientro. **`audit-sito.yml § 43`** ripete ogni 6 ore lo stesso confronto (40 pagine a caso) più i 3 marker semantici di contenuto (`navDropdown-per-il-cittadino` presente, niente `>Giochi</a>`, niente `tel:+39%20`).
- Provato in locale il 01/10/2026 con un server HTTP e un server FTPS di prova (pyftpdlib, TLS con riuso della sessione sul canale dati, lo stesso che Aruba richiede): tre pagine manomesse, trovate, ricaricate e ricontrollate byte per byte.

**Rimedio quando scatta l'issue:** rilanciare il deploy (Actions → «🚀 Build e Deploy» → Run workflow): lo step di riparazione ricarica i soli file diversi. Se nel log di quello step il collegamento FTPS è fallito, il problema è nelle credenziali o nella cartella remota, non nelle pagine. Da una sessione con le credenziali: `python3 scripts/verifica-deploy-aruba.py --manifesto public/build-manifest.json --public public --ripara`.

> 🔴 **VIETATO il bump del `state-name` (regola invertita il 03/07/2026 — su questo sito NON funziona).** Fino a giugno 2026 il rimedio documentato per il drift grave era cambiare il `state-name` nello step FTP di `deploy.yml` per forzare il re-upload integrale. **Non farlo mai più**: il sito conta ~25.000 file (di cui migliaia di micro-file dell'indice Pagefind da ~5 KB) e su FTP Aruba ogni file è una connessione dati completa (~0,3-0,8 s) — l'upload integrale supera i 90 minuti di timeout e **non completa mai**. Il 03/07/2026 un bump ha innescato un loop di upload integrali mai finiti → sync-state mai salvato → **sito congelato per l'intera giornata** (12 deploy falliti, articolo da calendario mai andato live). Mai `dangerous-clean-slate: true` (distruggerebbe `/documenti/` gestita a mano). La riparazione mirata del manifesto rende inutile anche il vecchio trucco del commento `<!-- cache-bust: … -->` nei `_index.md` (PR #187 del 12/05/2026, #215 del 13/05/2026): resta valido come ultima risorsa manuale, perché un file toccato alla fonte cambia impronta e viene ricaricato, ma di norma non serve più.

**Eccezione**: le pagine HTML statiche sotto `static/` (es. `/abili-a-proteggere/`, `/giochi/`, `/quizpc/`, `/formazionepc/`, kit-calamita stampabili) hanno l'header iniettato lato client da `static/app-shared/site-chrome.js`; sono nel manifesto come ogni altro file, ma i marker semantici dell'audit non si applicano a loro.

## Verifica prima del push

Prima di fare push su `main`, verifica sempre:
- `hugo server` non mostra errori in console
- Il build `hugo --minify` completa senza errori
- I percorsi di immagini, PDF e asset statici sono corretti
- Il frontmatter degli articoli usa il formato data `AAAA-MM-GG`
- Nessun articolo con `draft: false` ha contenuti incompleti
- Se hai modificato un file `.github/workflows/*.yml`, validalo con `python3 -c "import yaml; yaml.safe_load(open(...))"` prima del push
- Se hai modificato `.htaccess`, ricontrolla che `Permissions-Policy: geolocation=(self)` resti integro

## Divieti

- Non fare push su `main` con un build rotto.
- Non committare credenziali, token o secret nel repository.
- Non modificare il workflow CI/CD senza verificare la compatibilità con entrambi gli ambienti.
- Non introdurre asset con percorsi hardcoded che funzionino solo su un ambiente.
- Non eliminare o rinominare file già pubblicati senza gestire i redirect appropriati (Aruba non ha redirect automatici).
