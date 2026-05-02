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
- Build statica di Hugo (nessun server-side rendering, nessuna API runtime)
- Deploy FTP su Aruba (percorsi degli asset devono essere corretti per entrambi i baseURL)
- GitHub Pages con subpath `/sito-pc-genzano/` (usa `{{ absURL }}` o `{{ relURL }}` nei template, mai percorsi assoluti hardcoded)
- Certificato HTTPS esistente su Aruba (non modificare la configurazione DNS senza coordinamento)

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

Quando l'utente scrive un articolo da app mobile / Claude Code cloud, la sandbox blocca i domini esterni e gli script `foto-da-*.sh` non possono girare in quel contesto.

**Soluzione**: l'articolo si pubblica con `image: ""` e include nel frontmatter **un solo** marker di servizio (uno tra i seguenti, in base alla fonte da cui prendere la foto):

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
