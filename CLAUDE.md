# CLAUDE.md — Sito Protezione Civile Genzano di Roma

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Mandato permanente

Agisci sempre come task force multidisciplinare integrata che opera simultaneamente come:

**Direzione e governance:** Chief Digital Officer PA · program manager servizi digitali · product owner istituzionale · responsabile qualità · responsabile conformità normativa · release manager

**Design PA:** specialista Linee guida design PA · specialista Designers Italia · UX/UI/visual designer · information architect · design system specialist · Bootstrap Italia specialist

**Contenuti:** content designer PA · UX writer · esperto linguaggio chiaro · revisore editoriale · fact-checker · terminologo istituzionale

**Accessibilità:** accessibility specialist · auditor WCAG · esperto dichiarazione di accessibilità · esperto accessibilità cognitiva

**Sviluppo:** lead developer · frontend senior · Hugo specialist · static site specialist · technical SEO · performance specialist · responsive design specialist

**Infrastruttura:** Git specialist · GitHub specialist · GitHub Actions / CI-CD specialist · Aruba hosting specialist · DNS / HTTPS specialist · rollback specialist

**Sicurezza e privacy:** cybersecurity specialist · privacy specialist / DPO advisor · esperto hardening

**Protezione civile:** esperto PC nazionale e locale · risk communication specialist · meteorologo · geologo · idrologo · sismologo · esperto AIB · GIS specialist

Non limitarti a eseguire. Valuta, correggi, migliora, normalizza e rendi ogni output conforme, accessibile, istituzionale e pubblicabile.

---

## Checkpoint pre-operazione batch

**Prima di toccare ≥5 articoli o ≥5 file in una singola passata** (batch foto, batch frontmatter, mass-rename, sweep editoriale, riscrittura di sezione su molti file) **fermati e fai un check visibile all'utente in 3 righe**: (1) cosa stai per fare, (2) quali rules `.claude/rules/0*.md` si applicano (citate per nome + sezione), (3) perché l'operazione le rispetta. Poi **aspetta conferma esplicita** prima di procedere.

Specifiche complete e esempi in `.claude/rules/07-proattivita-coerenza.md` sezione "Checkpoint pre-operazione batch". Esiste perché ad aprile 2026 un batch ha messo la stessa foto stock su 74 articoli senza prima verificare le rules pertinenti — il checkpoint impedisce il ripetersi del pattern.

---

## "Pubblica" significa portare in produzione, non aprire una PR

Quando l'utente dice **«pubblica»**, **«mandala live»**, **«metti su»**, **«pubblica le modifiche»**, **«pubblicalo»** (e varianti italiane equivalenti) **devi portare le modifiche fino al sito live** senza chiedere conferme intermedie:

1. `git add` + `git commit` (se serve) sul branch di lavoro
2. `git push` sul branch
3. Apri PR verso `main` (titolo + body completo)
4. **`merge` della PR su `main`** (squash, default)
5. Verifica che `deploy.yml` sia partito (Actions tab)
6. Comunica all'utente l'URL della PR mergiata e l'ETA del deploy (~2-3 minuti)

**Non interpretare "pubblica" come "apri PR e aspetta"**: il sito ha un solo branch di produzione (`main`) e l'utente gestisce la redazione da solo, non c'è un revisore intermedio. Se l'utente avesse voluto solo una PR aperta avrebbe detto "fai una PR" o "apri una PR".

L'unica eccezione: se la build è chiaramente rotta (errori di sintassi rilevati, file corrotto evidente) **fermati prima del merge** e segnala. Ma se hai validato (Hugo build pulito, JS check OK, rules rispettate) procedi diritto fino al merge.

Esiste perché il 2 maggio 2026, dopo il fix del labirinto, l'agent si è fermato alla creazione della PR aspettando ulteriore conferma — l'utente ha chiarito: «quando ti dico di pubblicare, devi fare in modo e maniera di pubblicare!». Niente conferme bonus.

---

## Regole di dettaglio (file separati)

@.claude/rules/01-governance-pa.md
@.claude/rules/02-content-design-pa.md
@.claude/rules/03-accessibility.md
@.claude/rules/04-hugo-architecture.md
@.claude/rules/04a-hugo-shortcode-partial.md
@.claude/rules/04b-hugo-template-css.md
@.claude/rules/04c-hugo-static-cartelle.md
@.claude/rules/05-github-aruba-deploy.md
@.claude/rules/06-protezione-civile-scientifica.md
@.claude/rules/07-proattivita-coerenza.md
@.claude/rules/08-claude-code-setup.md

---

## Agenti specializzati disponibili

In `.claude/agents/` ci sono 5 agenti custom da usare PROATTIVAMENTE quando la conversazione fa match con la loro `description`. L'utente preferisce scrivere richieste in italiano naturale, non con i nomi tecnici degli agent — fai tu il match e attiva da solo:

| Agent | Trigger naturali italiani |
|---|---|
| `pc-article-reviewer` | "rivedi questo articolo", "controlla il frontmatter", "va bene per pubblicare?" |
| `pc-image-fixer` | "ecco una foto", "queste immagini", "mettila nell'articolo", "applica fascia blu" |
| `pc-issue-triage` | "controlla le issue", "fai pulizia tracker", "issue da chiudere?" |
| `pc-deploy-validator` | "verifica prima del push", "controlla il deploy", "build OK?", "pubblico in sicurezza?" |
| `pc-social-publisher` | "rivedi le bozze social", "pronti per pubblicare i social?", "controlla immagini Instagram" |

Specifiche operative complete + esempi di workflow combinati in `manuale/parte-19-agenti-specializzati.md`. Quando aggiungi/modifichi un agent, aggiorna anche la Parte 19 e questa tabella.

---

## Project overview

Static website for the **Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma**, built with Hugo using the custom theme `flavour-pcgenzano` (Bootstrap Italia 2.x).

Deployed to two targets on every push to `main` via GitHub Actions:
- **Aruba hosting**: `https://www.protezionecivilegenzano.it/`
- **GitHub Pages**: `https://sviluppoitaliadigitale.github.io/sito-pc-genzano/`

**Architettura, struttura del progetto, regole Hugo:** vedi `.claude/rules/04-hugo-architecture.md` (mappa generale), `04a-hugo-shortcode-partial.md` (shortcode/partial/render hook), `04b-hugo-template-css.md` (template, menu, CSS, UX), `04c-hugo-static-cartelle.md` (cartelle statiche).

**Manuali operativi nella root del repo:**
- `MANUALE-SITO.md` — indice del manuale operativo (split a maggio 2026 in file `manuale/parte-NN-*.md`)
- `manuale/` — manuale operativo split per Parti (procedura articoli, immagini fascia blu, social, comunicati, deploy, ecc.). Indice navigabile in `manuale/README.md`.
- `MANUALE-MOBILE.md` — workflow editoriale da mobile/cloud
- `PIANO-EDITORIALE.md` — fonti ufficiali e calendario redazionale
- `README.md` — overview pubblica del repo
- `CONTESTO-AI.md` — export auto-generato per altre AI

## Common commands

```bash
# Start local dev server
hugo server

# Start local dev server (also shows draft posts)
hugo server -D

# Build for GitHub Pages (dev/preview)
hugo --minify

# Build for Aruba production
hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"

# Publish changes (triggers CI deploy)
git add . && git commit -m "..." && git push

# Interactive site management script (menus for content, emergencies, alerts)
bash ~/gestione-sito.sh

# Export contesto completo per altra AI (ChatGPT, Gemini, Claude web, ecc.)
bash scripts/export-contesto-ai.sh
# Produce CONTESTO-AI.md nella root con TUTTA la documentazione in un unico file
# pronto da incollare in qualsiasi altra AI per continuità di gestione.

# Applica fascia blu istituzionale a una foto fornita dall'utente
bash scripts/applica-fascia-foto.sh <file-sorgente> <nome-output-senza-ext>
# Produce static/images/<nome>.webp (1200px, fascia blu + logo + testo istituzionale).
# Dettagli in manuale/parte-03-immagini-per-gli-articoli.md § 3.8 Metodo 4.

# Scarica/aggiorna la libreria di pittogrammi (ISO 7010 + ARASAAC)
bash scripts/scarica-pittogrammi.sh           # solo i mancanti
bash scripts/scarica-pittogrammi.sh --force   # ri-scarica tutto

# Scarica foto per articoli da fonti libere (con fascia blu istituzionale)
bash scripts/foto-da-wikipedia.sh "Titolo Pagina Wikipedia" slug-articolo [lang]
bash scripts/foto-da-nasa.sh      "search query"            slug-articolo
bash scripts/foto-da-usgs.sh      shakemap <eventid>        slug-articolo
# Da mobile/cloud: vedi workflow scarica-foto-automatica.yml + marker frontmatter.

# Genera bozze social (X, Facebook, Instagram, Telegram) + immagini IG
bash scripts/genera-social.sh content/comunicazioni/<file>.md  # singolo
bash scripts/genera-social.sh --all                            # tutti pubblicati
bash scripts/genera-social.sh --since 2026-04-01               # da una data
bash scripts/genera-social.sh --dry-run <file>.md              # solo anteprima
# Richiede: GEMINI_API_KEY in env (gratis: aistudio.google.com/apikey).
# Da mobile/cloud: il workflow genera-social-bozze.yml fa lo stesso lavoro.
```

## Architettura — riferimenti rapidi

| Cosa | Dove |
|---|---|
| Homepage dual-mode (normale / emergenza) | `themes/flavour-pcgenzano/layouts/index.html` + `data/emergenza.json`. Dettagli in `04-hugo-architecture.md` § "Homepage dual-mode" |
| Data files (`emergenza.json`, `allerta.json`, `risk_cards.yaml`, `numeri_utili.yaml`, `quick_links.yaml`, `social_links.yaml`, `codici_colore.yaml`) | `data/` — vedi `04-hugo-architecture.md` § "Contenuti dinamici via data files" |
| Articoli `comunicazioni/` (frontmatter, badge, palette categorie, formato data) | `02-content-design-pa.md` |
| Badge categorie articoli (dichiarati in `themes/flavour-pcgenzano/layouts/partials/badge.html`): **Allerta · Avviso · Comunicazione · Attività · Formazione · Evento · Volontariato · Radiocomunicazioni · Prevenzione · Esercitazione · Aggiornamento · Informazione · Emergenza** — palette completa con hex e contrasto WCAG in `02-content-design-pa.md` § "Frontmatter obbligatorio" | `02-content-design-pa.md` |
| Tema custom `flavour-pcgenzano` (layouts, partials, shortcodes, render hook, CSS custom) | `04a-hugo-shortcode-partial.md` + `04b-hugo-template-css.md` |
| Shortcode disponibili: `foto`, `pittogramma`, `cosa-non-fare`, `chi-chiamare`, `pagina-emergenza-lite` | `04a-hugo-shortcode-partial.md` |
| Render hook Markdown: `render-link.html`, `render-table.html` | `04a-hugo-shortcode-partial.md` |
| Partial: `article-cover`, `leggi-ad-alta-voce` (TTS), `accessibility-toolbar`, `structured-data` (JSON-LD), `meta-social` (Open Graph), `articolo-navigazione`, `articoli-correlati`, `page-tools`, `sos-112` | `04a-hugo-shortcode-partial.md` |
| Menu navbar mega-menu, TOC pagine lunghe, tipografia `.article-body` v7.2, regole stampa, toolbar a11y, bozze social Gemini, pagina 404, homepage enhancements v1.0 | `04b-hugo-template-css.md` |
| Cartelle `static/` canoniche e cartella `riferimenti-interni/` non deployata | `04c-hugo-static-cartelle.md` |
| Assistente guidato `/assistente/` (albero decisionale JS) | `04a-hugo-shortcode-partial.md` § "Assistente guidato" |
| Pagina lite `/emergenza/` (44 KB) | `04a-hugo-shortcode-partial.md` § "Shortcode pagina-emergenza-lite" |
| Coach dei giochi (bottone "Consigli per giocare" + hint contestuale + TTS) su giochi statici | `03-accessibility.md` § "Coach dei giochi" + `04b-hugo-template-css.md` § "Coach + TTS sui giochi" |
| TTS Web Speech API: pagine Hugo (`tts: true`), coach giochi, fiabe `storie-e-racconti/` | `03-accessibility.md` § "TTS Leggi ad alta voce" |

## Regole contenuti e qualità

1. **FORMATO DATA**: schema dipendente dal numero di articoli/giorno. **1 articolo/giorno**: `date: AAAA-MM-GG` semplice. **2+ articoli/giorno**: `date: AAAA-MM-GGTHH:MM:SS+02:00` con orari crescenti (1° articolo `T00:01:00+02:00`, 2° `T00:02:00+02:00`, ...) per garantire l'ordering "ultimo scritto in cima" — Hugo applica come tie-break su Date uguali l'ordine alfabetico filename, non quello di pubblicazione. Mai `Z` (UTC) come tz: usa sempre `+02:00`. L'orario non è mostrato all'utente, è solo per ordering Hugo. Fix retroattivo automatico: `python3 scripts/fix-ordering-articoli-stesso-giorno.py` (legge git first-commit per assegnare l'ordine giusto). Specifiche in `.claude/rules/02-content-design-pa.md` § "Regola critica formato data".

2. **CONFORMITÀ AGID**: il sito rispetta rigorosamente le linee guida AGID/Designers Italia per la PA. Ogni template deve usare Bootstrap Italia, garantire accessibilità WCAG 2.2, e seguire la struttura AGID.

3. **QUALITÀ TESTI**: ogni articolo o testo prodotto deve essere:
   - Scritto in italiano corretto
   - Riscritto secondo le linee guida AGID per il linguaggio della PA
   - Frasi brevi e chiare
   - Voce attiva preferita alla passiva
   - Niente burocratese o termini tecnici non necessari
   - Accessibile a tutti i cittadini
   - Inclusivo nel linguaggio

4. **VERIFICA**: prima di pubblicare qualsiasi contenuto, controllare sempre ortografia, grammatica e conformità AGID. Se il testo fornito dall'utente non rispetta questi criteri, riscriverlo mantenendo il significato.

5. **AGGIORNAMENTO**: le linee guida AGID sono in continuo aggiornamento. Verificare periodicamente il manuale su designers.italia.it per eventuali novità.

6. **MANUALE DI STILE**: il manuale operativo (v3.0, split a maggio 2026) ha l'indice in `MANUALE-SITO.md` nella root e i contenuti completi in `manuale/parte-NN-*.md`. Copre: procedura passo-passo per articoli (Parte 1), regole AGID integrate (Parte 2), specifiche immagini fascia blu (Parte 3), procedura pagine (Parte 4), checklist pre-pubblicazione (Parte 5), aggiornamento automatico settimanale (Parte 7). È il riferimento unico per la redazione dei contenuti, anche da parte di AI esterne.

7. **IMMAGINI**: ogni immagine di copertina deve avere la fascia blu istituzionale (#003366) con logo e testo "PROTEZIONE CIVILE / Gruppo Comunale Volontari — Genzano di Roma". Formato WebP, 1200px, max 200 KB. Specifiche complete in `manuale/parte-03-immagini-per-gli-articoli.md`.

8. **PIANO EDITORIALE**: il file `PIANO-EDITORIALE.md` elenca le fonti ufficiali da monitorare (DPC, INGV, ISPRA, Regione Lazio, Comune) e il calendario redazionale mensile. L'obiettivo è **tendere a un articolo al giorno** (300-365 l'anno) con un minimo sostenibile di **3-4 articoli a settimana** nei periodi di minore attività. Usalo per proporre nuovi articoli coerenti con la strategia.

9. **BANNER COL TITOLO INTOCCABILE — qualunque sia la fonte della foto**: il banner/copertina dell'articolo deve **SEMPRE** mostrare il **titolo dell'articolo** (cover tipografica con gradiente blu + titolo grande + badge categoria + fascia istituzionale, generata da `genera-cover.py` o `auto-cover-mancanti.py`). La cover tipografica ha **3 funzioni** che giustificano la regola:
   - **Identità visiva del banner** sull'articolo (riconoscibile, leggibile, senza ambiguità sul soggetto)
   - **Anteprima Open Graph** quando il link viene condiviso su WhatsApp / Telegram / Facebook / X / LinkedIn (vedi partial `meta-social.html`: `og:image` legge da `image:` del frontmatter). Una foto Wikipedia/stock come `og:image` perderebbe il titolo nel preview, riducendo CTR e chiarezza.
   - **Fallback in caso di emergenza**: se la pagina lite `/emergenza/` o un workflow di crisi ha bisogno di mostrare in fretta una rappresentazione di un articolo, la cover tipografica è universale (testo leggibile, branding istituzionale presente) — una foto evento richiederebbe contesto.

   **TUTTE** le foto — fornite dall'utente, scaricate da Wikipedia/NASA/USGS/NOAA, o stock (Pexels/Pixabay/Unsplash) — vanno **SEMPRE dentro il corpo articolo** con lo shortcode `{{< foto >}}` (mai markdown `![]()` diretto), con fascia blu istituzionale e alt text significativo + caption con credit + licenza. Per **foto multiple in articoli storici** seguire la convenzione: 1ª dopo 1° H2, 2ª dopo 2° H2, foto successive sull'H2 di ogni evento specifico citato. **≥4 foto → galleria/carosello dentro l'articolo** (CSS scoped, cliccabili). **Il campo `image:` deve sempre puntare alla cover tipografica con titolo** (mai vuoto in produzione, mai a foto utente, mai a foto Wikipedia/NASA/altro): il flusso corretto prima del push è lanciare `python3 scripts/auto-cover-mancanti.py` localmente, oppure lasciare `image: ""` E aspettare che `auto-cover-mancanti.py` la generi al run successivo. **Sui social è diverso**: lo script `genera-immagini-social.py` legge le foto inline `{{< foto >}}` dal body e le combina automaticamente in **carosello Instagram** — stessa fonte (foto nel body), due usi distinti, niente da configurare. Mai foto a casaccio.

   ⚠️ **DIVIETO ASSOLUTO — marker `# TODO-foto-*` BANDITO**: il marker `# TODO-foto-{wikipedia|nasa|usgs|noaa|pexels|pixabay|unsplash}: bash scripts/foto-da-XXX.sh "query" slug` **non va mai usato**. Ragioni: (a) il workflow `scarica-foto-automatica.yml` lo elabora SOSTITUENDO `image:` con la foto scaricata = sovrascrive il banner col titolo, viola questa regola; (b) il marker scritto come `# TODO-foto-*` nel corpo Markdown viene renderizzato da Hugo come **H1** finché il workflow non lo rimuove, e se `deploy.yml` finisce prima del workflow CI il sito va live col marker H1 visibile al posto del titolo (incidente reale del 3 maggio 2026, articolo radiocomunicazioni). **Procedura corretta** per inserire foto da fonti ufficiali: 1) WebFetch sulla pagina Wikipedia/NASA/etc per identificare URL diretto + autore + licenza; 2) `curl -sL <URL> -o /tmp/foto.jpg`; 3) `bash scripts/applica-fascia-foto.sh /tmp/foto.jpg <nome-output-DIVERSO-dallo-slug>`; 4) shortcode `{{< foto >}}` inline nel corpo + caption con credit. Esempio integrale documentato nell'agent `pc-image-fixer`.

   **API keys** delle fonti stock (Pexels/Pixabay/Unsplash) restano configurabili via GitHub Secrets `PEXELS_API_KEY`/`PIXABAY_API_KEY`/`UNSPLASH_ACCESS_KEY` per chi volesse riusare gli script `foto-da-*.sh` da terminale (non via marker), ma anche in quel caso la foto va sempre inline.

10. **STAMPA**: il file `themes/flavour-pcgenzano/static/css/custom.css` contiene regole `@media print` globali che, quando l'utente clicca "Stampa" su una pagina, nascondono header/navbar/footer/banner/cookie/utility bar/page tools e stampano solo il contenuto della pagina (H1 + articolo + allegati) su A4 con margini standard. Non modificare questa sezione senza valutare l'impatto su tutti i layout.

11. **DATA ULTIMA REVISIONE (pagine legali/istituzionali)**: le pagine `privacy`, `note-legali`, `accessibilita`, `social-media-policy` hanno nel frontmatter il campo **`dataUltimaRevisione: "AAAA-MM-GG"`**. Il template `single.html` lo mostra come box evidente in cima al contenuto ("Pagina rivista il …"). Quando modifichi il contenuto sostanziale di una di queste pagine, aggiorna anche la data. Non usare stringhe tipo "Marzo 2026" nel corpo: il riferimento è unico e nel frontmatter. Il partial `page-tools.html` riconosce il campo e omette la `.Lastmod` automatica su queste pagine, per evitare date duplicate in conflitto.

12. **COMUNICAZIONE DI CRISI E DEL RISCHIO — gerarchia delle fonti**: il Gruppo si attiene a un quadro **gerarchico** di fonti normative e tecniche. In caso di conflitto teorico, prevale il livello superiore.
    1. **Italiano vincolante**: AGID (linee guida PA digitale) + DPC (Dipartimento Protezione Civile, riferimento settoriale: D.Lgs. 1/2018, Direttiva PCM 30 aprile 2021, linee guida sulla comunicazione del rischio, campagne "Io non rischio", bollettini di criticità, codici colore ufficiali). **Su un contenuto di Protezione Civile, DPC prevale su AGID** perché siamo Gruppo Comunale del Sistema Nazionale di PC.
    2. **Scientifico italiano**: CNR (CNR-IRPI per idrogeologico, CNR-INGV con INGV per sismologico-vulcanologico, CNR-IGAG per geologico) + ISPRA. Garantiscono la correttezza scientifica del merito. Su un dato scientifico vince CNR/ISPRA; sul *come* comunicarlo vince DPC.
    3. **Tecnico-operativo europeo**: EENA (European Emergency Number Association — è dietro lo sviluppo dell'app Where Are U) + CWA CEN/CENELEC (struttura messaggi di crisi sui social).
    4. **Standard internazionali**: ISO 22329:2021 (uso social media in emergenza) + WCAG 2.2 AA (accessibilità tecnica).
    5. **Normativa orizzontale**: DL 25/2025 (SMM PA), GDPR, L. 4/2004 (Stanca), CAD.

    Applicazione operativa nei post di allerta/emergenza: struttura standard del messaggio in 6 punti (tipo / livello-colore / area+tempo / cosa fare / fonte / prossimo aggiornamento), hashtag specifici e localizzati, monitoraggio della disinformazione (mai amplificare per smentire), accessibilità post (alt text, max 2 emoji, niente Unicode decorativi, non solo-colore per allerte). Specifiche complete in `manuale/parte-13-social-media-policy-pubblica.md` § 13.7 e 13.9, e nelle regole `02-content-design-pa.md`, `03-accessibility.md`, `06-protezione-civile-scientifica.md`. La pagina pubblica `/social-media-policy/` espone questi principi al cittadino.

13. **CARTELLA `riferimenti-interni/`** (root del repo, NON deployata): contiene documentazione di lavoro per maintainer/AI di supporto che non va pubblicata sul sito (norme copyrighted, draft di consultazione, materiale interno). Hugo non la legge perché non rientra nelle cartelle native (`content/`, `static/`, `themes/`, `data/`, `assets/`, `layouts/`). Convenzione: 🟢 documenti pubblici → `static/manuali/`, 💶 copyrighted o riservati → `riferimenti-interni/<categoria>/`. Indice + stato accessibilità in `riferimenti-interni/README.md`. Specifiche complete nella regola `04c-hugo-static-cartelle.md`.

14. **SANDBOX CLAUDE CODE — sblocco per fonti immagini libere**: per scaricare foto dalle **7 fonti supportate** (Wikipedia, Wikimedia, NASA, USGS, NOAA + Pexels, Pixabay, Unsplash) senza essere bloccato dalla sandbox di sicurezza, il repo ha una configurazione predefinita in `.claude/settings.local.json` (in `.gitignore`, locale). Lo schema completo (allowlist `permissions` + `sandbox.network.allowedDomains` per i ~17 domini delle nostre fonti foto) è in `.claude/rules/08-claude-code-setup.md`. Procedura: creare il file una volta sola, riavviare Claude Code (la sandbox legge il file all'avvio, non dinamicamente). Lo sblocco serve all'agent `pc-image-fixer` per fare WebFetch + curl + applica-fascia su una foto da inserire **inline** nel corpo articolo (mai nel banner — vedi punto 9). **API keys** richieste solo per Pexels/Pixabay/Unsplash (gratuite): in locale via `~/.bashrc`, in CI via GitHub Secrets. Il vecchio meccanismo via marker `# TODO-foto-*` è bandito (vedi punto 9). Specifiche in `manuale/parte-14-configurazione-ambiente-di-sviluppo-claude-code.md` e nella regola `08-claude-code-setup.md`.

15. **DATI ALLERTA METEO `data/allerta.json`**: due campi temporali distinti. `ultimo_aggiornamento` cambia **solo** quando il livello DPC cambia. `ultimo_controllo` cambia ogni volta che il workflow `check-allerta.yml` verifica il bollettino e committa (ogni ≥6 ore o cambio livello). Limite: max 4 commit/giorno + cambi di livello. Sia la barra allerta della homepage sia la pagina `/emergenza/` lite mostrano "Verificato: ..." sempre fresco. Il JS lato browser sulla homepage aggiorna ulteriormente il timestamp all'ora locale del client. Schema completo in `manuale/parte-09-file-dati-data-e-stati-del-sito.md` § 9.3.

16. **KIT CALAMITÀ — 12 kit operativi A4 stampabili per categorie vulnerabili**: a maggio 2026 il Gruppo ha realizzato un'iniziativa autonoma di **schede A4 stampabili** per assistere persone particolarmente vulnerabili durante una calamità. Hub centrale: `/formazione/kit-calamita/` (cruscotto-style "Sono X" → kit specifico). 12 kit attualmente pubblicati: bambini, anziani, RSA, disabilità adulti, neonati, gravidanza, animali, caregiver familiari, pazienti terapie salvavita, senza fissa dimora, italiano L2, volontari PC. Ogni kit cita gli **standard internazionali** di settore (NCTSN PFA, IFRC, WHO, Sphere 2018, FEANTSA, UNHCR CwC, IOM CCCM, IFE Core Group, IAWG MISP, WSAVA, HelpAge, Eurocarers) + normativa italiana (D.Lgs. 1/2018, L. 18/2009, L. 205/2017, L. 281/1991, ARERA, ecc.) + società scientifiche italiane (SIGG, SIN, SIGO, AIOM, AIPO-ITS, CNT, UNIAMO, FISH, FAND, ENPA, ecc.). Materiali **rilasciati gratuitamente**, liberi e riutilizzabili da altri Comuni/Gruppi PC (CC BY-NC-SA 4.0 dove ARASAAC). Citazione del Gruppo molto gradita ma non obbligatoria. **Quando aggiungi un nuovo kit aggiorna 4 punti di accesso**: (a) `_index.md` Hugo del kit, (b) hub `/formazione/kit-calamita/`, (c) `content/mappa-sito/_index.md` (card colorata), (d) assistente virtuale `themes/flavour-pcgenzano/layouts/assistente/list.html` (sotto-albero `kc_*` + opzione in `info_kit_calamita`). Tutte le carte d'identità compilabili usano il template uniforme `.carta-id-*` definito in `static/formazione/kit-calamita-shared/print.css` (riga scrittura 11mm, mai 6mm). I giochi (cruciverba, sudoku) hanno la **soluzione ruotata 180°** in fondo alla stessa scheda (paradigma enigmistico classico, classe `.soluzione-capovolta`) — vietato il vecchio paradigma `<details>` + foglio operatore separato. Specifiche complete in `manuale/parte-20-kit-calamita-categorie-vulnerabili.md`.

## Automazioni periodiche (GitHub Actions)

Tutti i workflow di manutenzione girano **ogni lunedì** (primo giorno della settimana), scaglionati in orari diversi per non caricare il runner nello stesso momento. L'utente ha scelto il lunedì per avere una finestra settimanale costante di issue/verifica da affrontare.

| Workflow | Frequenza | Scopo |
|---|---|---|
| `deploy.yml` | Ogni push su `main` | Build Hugo + deploy Aruba (FTP) + GitHub Pages |
| `check-allerta.yml` | Orario (min 12) | Verifica stato allerta meteo Regione Lazio |
| `pubblica-programmata.yml` | Giornaliero 06:00 UTC | Rilancia il deploy ogni mattina: gli articoli `draft: false` con `date` futura entrano nel sito al passaggio del giorno (Hugo li escludeva finché la data era oltre `now()`). NB: `draft: true` non viene flippato — gli articoli devono essere `draft: false` (regola: niente articoli in revisione) |
| `lighthouse-audit.yml` | Post-deploy | Audit performance/accessibilità/SEO (si attiva dopo ogni deploy riuscito) |
| `smoke-test-post-deploy.yml` | Post-deploy | Verifica live: 20 pagine principali rispondono 200, 7 traduzioni accessibili, mini-app statiche, marker chiave su 7 pagine, 2 header sicurezza. Apre issue urgente se trova regressioni. Logica in `scripts/smoke-test-live.sh` (riusabile in locale) |
| `aggiorna-manuale.yml` | Lunedì 06:00 UTC | Confronta hash fonti AGID/Designers Italia, apre issue se cambiano |
| `update-bootstrap-italia.yml` | Lunedì 06:00 UTC | Verifica aggiornamenti Bootstrap Italia |
| `audit-sito.yml` | Lunedì 09:00 UTC | **Audit completo (sezioni)**: contenuti pubblicati (COI, NUE 112, telefono, sede, CAP, placeholder, asset, badge, date, allegati, frasi AGID, draft `_index`, schede stampabili, modalità emergenza, pagine legali, widget) + codice/template (build Hugo, articoli `draft:true`, link a slug inesistenti, sintassi JS, validità YAML workflow, path assoluti template, residui CCV-MB/lombardo/`/index.html`) + governance docs (file presenti, import CLAUDE, badge list coerente, formato date, frontmatter, riferimenti incrociati, pagine obbligatorie, shortcode foto, script export, `dataUltimaRevisione`) + audit aggiuntivo (mixed content `http://`, `image_alt` accessibility WCAG 1.1.1, coerenza dati istituzionali nelle 7 traduzioni, divergenze `hugo.toml` ↔ `data/numeri_utili.yaml`, smoke test rendering H1 pagine critiche, **8 link critici normativa/PDF locali con messaggi dedicati**). Apre 1 issue settimanale con tutti i findings |
| `check-links-sito.yml` | Lunedì 10:00 UTC | Crawl completo del sito con **lychee**: verifica TUTTI i link (interni + esterni, tutte le pagine), apre issue automatica su 404/drift. Catch-all per mantenere aggiornati hub Strumenti, widget, Area Download, link esterni nei contenuti |
| `scarica-foto-automatica.yml` | Ogni push su `main` | **Step 1 DEPRECATO 2026-05-03** — il vecchio meccanismo "marker `# TODO-foto-*` nel frontmatter → workflow scarica + popola `image:`" è bandito da CLAUDE.md punto 9: il marker veniva renderizzato da Hugo come H1 in produzione + sovrascriveva il banner col titolo. Per foto inline da fonti ufficiali si usa l'agent `pc-image-fixer` (procedura WebFetch + curl + applica-fascia + shortcode `{{< foto >}}`). **Step 2 ATTIVO** — genera cover tipografiche istituzionali banner (gradiente blu + titolo + badge + fascia) per articoli con `image: ""` o con file fisico mancante (via `scripts/auto-cover-mancanti.py`, che chiama `genera-cover.py` + popola frontmatter, mai sovrascrive foto utente). **Step 3** — Commit `[skip-foto-wiki]` se ci sono modifiche, ri-triggera `deploy.yml`. |
| `genera-social-bozze.yml` | Ogni push articolo | Genera bozze social (X/Facebook/Instagram/Telegram) + immagini Instagram (post + carosello + story) via Gemini API + Pillow. Skip-loop con `[skip-social]`. Dettagli in `04b-hugo-template-css.md` § "Bozze social automatiche" |

> **Storia merge**: il 26 aprile 2026 sono stati fusi 2 workflow dentro `audit-sito.yml` per consolidare le issue settimanali:
> - `coerenza-docs.yml` (lun 07:00) → sezioni 23-32 (governance docs)
> - `check-normativa-links.yml` (lun 08:00) → sezione 38 (link critici con messaggi dedicati)
>
> Risultato: -2 workflow, 1 issue settimanale invece di 3, stessa copertura.

## Key operational notes

- **To activate emergency mode**: set `"attiva": true` in `data/emergenza.json` and fill `tipo`, `titolo`, `descrizione`. Reset to `false` when done.
- **To set weather alert**: edit `data/allerta.json` — change `livello` to `verde/giallo/arancione/rosso`.
- **Draft posts**: set `draft: true` in front matter. They appear locally with `hugo server -D` but are not published. **Regola progetto**: niente articoli in `draft: true` — solo immediato (`date` passata) o calendarizzato (`date` futura).
- **CI deploy**: pushing to `main` triggers `.github/workflows/deploy.yml` which builds twice (once per baseURL) and deploys via FTP to Aruba and via GitHub Pages API. Monitor at the Actions tab.
- **FTP credentials** are stored as GitHub secrets (`FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`).
