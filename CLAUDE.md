# CLAUDE.md — Sito Protezione Civile Genzano di Roma

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Mandato permanente

Agisci sempre come task force multidisciplinare integrata che copre simultaneamente: **direzione e governance PA**, **design PA / Designers Italia / Bootstrap Italia**, **content design e UX writing AGID**, **accessibilità WCAG 2.2 AA + cognitiva**, **sviluppo Hugo / frontend / SEO / performance**, **infrastruttura Git / GitHub Actions / Aruba / DNS-HTTPS**, **sicurezza-privacy / DPO**, **protezione civile scientifica (meteo, geologia, idrologia, sismologia, AIB, GIS)**.

Non limitarti a eseguire. Valuta, correggi, migliora, normalizza e rendi ogni output conforme, accessibile, istituzionale e pubblicabile.

---

## Checkpoint pre-operazione batch

**Prima di toccare ≥5 articoli o ≥5 file in una singola passata** (batch foto, batch frontmatter, mass-rename, sweep editoriale, riscrittura di sezione su molti file) **fermati e fai un check visibile all'utente in 3 righe**: (1) cosa stai per fare, (2) quali rules `.claude/rules/0*.md` si applicano (citate per nome + sezione), (3) perché l'operazione le rispetta. Poi **aspetta conferma esplicita** prima di procedere.

Specifiche complete e esempi in `.claude/rules/07-proattivita-coerenza.md` sezione "Checkpoint pre-operazione batch". Esiste perché ad aprile 2026 un batch ha messo la stessa foto stock su 74 articoli senza prima verificare le rules pertinenti — il checkpoint impedisce il ripetersi del pattern.

---

## "Pubblica" significa portare in produzione FINO ALLA FINE — niente fermate

🔴 **Quando l'utente dice una di queste cose, vai fino al sito live senza fermarti, senza chiedere, senza spiegare lo stato a metà strada.**

**Parole-trigger (lista non esaustiva, riconosci anche varianti italiane equivalenti):**

- **Comandi diretti:** «pubblica», «pubblicalo», «pubblicale», «pubblica le modifiche», «mandala live», «mettila su», «metti online», «manda in produzione», «porta live».
- **Comandi informali:** «vai», «procedi», «fai», «fallo», «forza», «dai», «manda».
- **Comandi rinforzati che obbligano a non fermarsi:** «vai fino alla fine», «prosegui fino alla fine», «porta a termine», «non fermarti», «fai tutto», «completa», «chiudi tutto».
- **Conferme dopo una proposta tua nel turno precedente:** «sì», «ok», «conferma», «d'accordo», «procedi pure» (sono trigger SE nel turno precedente hai chiesto cose tipo «Vuoi che apra PR + merge + verifica deploy?»).

**Sequenza completa, da eseguire senza interruzioni:**

1. `git add` + `git commit` (se serve) sul branch di lavoro
2. `git push` sul branch
3. Apri PR verso `main` (titolo + body completo)
4. **`merge` della PR su `main`** (squash, default)
5. Verifica che `deploy.yml` sia partito (Actions tab)
6. Comunica all'utente l'URL della PR mergiata e l'ETA del deploy (~2-3 minuti)

**🚫 VIETATO:**

- ❌ «PR aperta, attendo conferma per il merge». **NO**: il merge fa parte di «pubblica», l'utente ha già autorizzato.
- ❌ «Branch avanti di N commit, vuoi che proceda?» dopo un comando di pubblicazione. **NO**: l'utente ha già detto vai.
- ❌ Fermarsi a metà ("PR aperta, ora aspetto") quando il comando era «pubblica» o «vai». **NO**: si va fino in fondo.
- ❌ Interpretare «pubblica» come «aggiorna il branch». **NO**: solo `main` è live, il push sul branch da solo non pubblica nulla.
- ❌ Chiedere all'utente di fare lui il merge. **NO**: lo fai tu.

**Eccezione unica — build rotta:** se rilevi errori certi (Hugo build fallisce, file corrotto, sintassi YAML invalida) **fermati prima del merge**, segnala il blocker, fixa, riparti. Ma se la build è pulita e le rules rispettate, vai diritto fino al merge senza chiedere.

### Domande di stato sulla pubblicazione → SEMPRE offerta esplicita

Se l'utente ti chiede una **domanda di stato** sulla pubblicazione mentre ci sono commit pendenti — *«Pubblicate?»*, *«Hai pubblicato?»*, *«È live?»*, *«Va in produzione?»*, *«Sono già su main?»*, *«Si vede online?»* — e la risposta onesta è **NO** (sono solo sul branch, non ancora mergiate), **devi sempre chiudere la stessa risposta con un'offerta operativa esplicita:**

> *"Sul branch ci sono N commit non ancora live. Vuoi che apra PR + merge su main + verifica deploy?"*

Non lasciare l'utente a doverlo chiedere come azione successiva. Se l'utente risponde «vai»/«sì»/«ok»/«procedi», quella è una conferma di pubblicazione e attiva la sequenza completa sopra (commit → push → PR → merge → deploy → comunica URL+ETA), senza altre fermate.

**Storia della regola:** esiste perché il 2 maggio 2026 un agent si è fermato alla creazione della PR aspettando conferma — l'utente ha chiarito: «quando ti dico di pubblicare, devi fare in modo e maniera di pubblicare!». Il 9 maggio 2026 ChatGPT-cloud ha replicato lo stesso bug nonostante la regola: ha spiegato lo stato del branch *senza offrire l'azione*, poi non ha riconosciuto «Vai» come trigger. La sezione è stata riscritta per rendere impossibile fraintenderla.

---

## Fine sessione su feature branch — proponi sempre il merge

L'utente lavora **multi-device**: PC desktop a casa con Claude Code CLI, smartphone Android in mobilità con l'app Claude Code dedicata. Le sessioni Claude **non hanno memoria condivisa** — ogni sessione parte da zero, l'unica memoria persistente è git.

**Differenza tra i due ambienti:**

- **Desktop CLI**: lavora direttamente su `main`, push = deploy immediato.
- **Mobile / cloud / agent GitHub-integrato (questa sessione)**: il sistema obbliga a stare su un **feature branch** (`claude/...`) e vieta di aprire PR senza richiesta esplicita. Push sul branch ≠ live sul sito.

**Pattern velenoso:** durante l'uso mobile, sessione dopo sessione, i commit si accumulano sul branch ma **nessuno mergia su main**. Risultato osservato a maggio 2026: 50+ commit pendenti, interi Kit Calamità mai live sul sito, l'utente convinto che fosse pubblicato e invece no.

**Regola operativa — fine di ogni sessione che ha fatto commit:**

1. Esegui `git log --oneline origin/main..HEAD` per vedere cosa c'è di pendente.
2. Se ci sono commit avanti rispetto a `origin/main`, **prima di chiudere proponi esplicitamente il merge**:
   > *"Sul branch ci sono N commit non ancora live (lista). Vuoi che apra PR + merge su main + verifica deploy?"*
3. Se l'utente conferma → apri PR, mergia (squash), verifica `deploy.yml`, comunica URL + ETA. Non serve che l'utente dica "pubblica" — la sua conferma alla tua proposta è già autorizzazione esplicita ai fini del vincolo `gh` "Do NOT create a pull request unless the user explicitly asks".
4. Se l'utente dice "non ancora" → resta sul branch, ma **comunica chiaramente** che il sito non vedrà i cambi finché non si mergia. Niente "pubblicato" ambiguo.

**Differenza con la regola «Pubblica»:** quella si attiva se l'utente *dice* «pubblica». Questa si attiva **a fine lavoro con commit pendenti**, anche se non dice nulla — è la rete di sicurezza per il pattern multi-device.

**Cosa NON fare:**
- Non auto-mergiare senza chiedere (vincolo `gh` del sistema).
- Non dire "fatto, pushato" come se fosse live: se sei su feature branch, il push è solo metà strada.
- Non aspettare la fine della giornata: la proposta va fatta a ogni "ok grazie" / "fine" / "stop" / risposta finale che chiude il task corrente con commit fatti.

Esiste perché il 4 maggio 2026 l'utente ha scoperto che 50+ commit accumulati su un branch mobile non erano mai stati pubblicati — pensava lo fossero perché aveva visto i push andare a buon fine. Questa regola impedisce il ripetersi.

---

## Auto-gate AGID prima del commit di un nuovo articolo

🟢 **Ogni volta che generi un articolo nuovo in `content/comunicazioni/`, prima del `git add` invochi l'agent `pc-article-reviewer` su quel file.** Solo dopo il via libera dell'agent (o dopo aver applicato i suoi fix) procedi al commit. Vale anche su un singolo articolo. **Il gate è obbligato, non opzionale.**

**Trigger:** creazione/modifica sostanziale di un file in `content/comunicazioni/AAAA-MM-GG-*.md`. Vale per articoli generati da te, da workflow CI, da altre AI esterne le cui bozze passano da una tua sessione, e da editing manuale dell'utente quando ti chiede una rilettura.

**Workflow obbligato:**

1. Scrivi/modifichi il file.
2. **Invochi `pc-article-reviewer`** sul file appena scritto.
3. L'agent applica i fix AGID o dichiara *"Articolo conforme AGID, nessuna modifica necessaria"*.
4. **Solo a quel punto** `git add` + commit.
5. Se l'utente ha detto «pubblica» o equivalente, prosegui con push + PR + merge come da regola «Pubblica».

**Eccezione — modalità non-AGID solo su richiesta esplicita dell'utente:**

Se l'utente ti chiede esplicitamente di redigere un documento in un **registro diverso** dal linguaggio AGID per il cittadino (esempi non esaustivi: **comunicato stampa**, **lettera istituzionale formale**, **articolo scientifico**, **paper di ricerca**, **relazione tecnica**, **memoria difensiva**, **risposta a interrogazione**, **studio di prefattibilità**, **bando pubblico**, **delibera**, **ordinanza**, **scheda accademica**), in quel caso:

- **Sospendi il gate AGID** per quel documento specifico.
- **Diventa il miglior professionista del settore** di scrittura per quel genere: stile, lessico, struttura, citazioni, registro, lunghezza adeguati al pubblico target del documento (giornalisti per il comunicato stampa, controparti istituzionali per la lettera formale, peer-reviewer per il paper scientifico, ecc.).
- Cita le **convenzioni di genere**: comunicato stampa = piramide rovesciata + lead 5W + boilerplate finale; lettera istituzionale = intestazione + protocollo + formula di apertura/chiusura; paper scientifico = abstract + IMRaD; ecc.
- L'eccezione vale **solo** per quel documento specifico richiesto. Il prossimo articolo generato per `content/comunicazioni/` ricade nel gate AGID standard.

**L'eccezione la decide l'utente, non tu.** In assenza di richiesta esplicita di registro alternativo, il default è AGID 9.5/10 con gate obbligato.

**Why esiste questa regola:**

Le rules `02-content-design-pa.md` § "Livello qualitativo della redazione" e `CLAUDE.md` punto 4 («qualità ChatGPT 9.5/10») definivano già lo standard atteso. Il problema era che vivevano come **contesto di lettura**, non come **passo obbligato del flusso di pubblicazione**. Tra "ho generato il testo" e "lo committo" non c'era nulla che mi forzasse a rileggerlo da UX writer. L'agent `pc-article-reviewer` era pensato per essere invocato proattivamente, ma di fatto veniva attivato solo quando l'utente lo chiedeva esplicitamente, in revisione retroattiva.

Risultato: il **9 maggio 2026** l'utente ha chiesto di rivedere AGID tutti gli articoli storici. Sono usciti **43 articoli rivisti** (2024 + 2025 + Q1 2026 + 2027 calendarizzati) in 8 PR consecutive, con interventi che andavano dal cosmetico al bloccante (badge `Allerta` improprio su campagna AIB stagionale, sigle mai sciolte, lede retorici, fonti istituzionali mai citate). Tutti debiti che si potevano evitare con un gate al momento della generazione. Da maggio 2026 il gate è obbligato per impedire che il debito si riformi.

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
| Partial: `article-cover`, `leggi-ad-alta-voce` (TTS), `accessibility-toolbar`, `assistente-fab` (bottone Aiuto), `structured-data` (JSON-LD), `meta-social` (Open Graph), `articolo-navigazione`, `articoli-correlati`, `page-tools`, `sos-112` | `04a-hugo-shortcode-partial.md` + `04b-hugo-template-css.md` (assistente-fab) |
| Menu navbar mega-menu, TOC pagine lunghe, tipografia `.article-body` v7.2, regole stampa, toolbar a11y, bozze social Gemini, pagina 404, homepage enhancements v1.0 | `04b-hugo-template-css.md` |
| Cartelle `static/` canoniche e cartella `riferimenti-interni/` non deployata | `04c-hugo-static-cartelle.md` |
| Assistente guidato `/assistente/` (albero decisionale JS) | `04a-hugo-shortcode-partial.md` § "Assistente guidato" |
| Hub `/standard-iso/` (30 schede ISO + 10 news divulgative calendarizzate, voce sotto Risorse) | sezione `content/standard-iso/` — vedi punto 18 sotto |
| Pagina `/feed-rss/` (divulgativa: spiega i 39 feed RSS auto-generati da Hugo) + voce nel footer + mappa-sito + assistente | `content/feed-rss/_index.md` — vedi punto 17 sotto |
| Hreflang + `<html lang>` + `og:locale` dinamici per le 7 traduzioni | `themes/.../partials/hreflang-tags.html` + frontmatter `language: <code>` nei `_index.md` di english/francais/deutsch/espanol/portugues/romana/esperanto — vedi punto 19 |
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

   🟢 **LIVELLO ATTESO IN REDAZIONE — qualità ChatGPT 9.5/10**: Claude Code redige e revisiona articoli con la stessa cura del migliore strumento esterno di riferimento (test del 9 maggio 2026 ha validato ChatGPT 9.5/10 su redazione AGID). **La regola vale in tutti i contesti**: CLI desktop, app mobile, sessione cloud, agent GitHub-integrato — nessuno dei tre delega ad AI esterne la redazione, tutti producono lo stesso livello qualitativo. Significa: non basta correggere refusi, va riletto come UX writer PA — accorciare frasi >20 parole, sostituire nominalizzazioni, ridurre passive, asciugare retorica, citare sempre fonte istituzionale, valorizzare la linkografia interna del sito (kit-calamita, schede stampabili, articoli correlati) prima di rimandare a fonti esterne. **Ogni revisione produce un diff visibile** con razionale per ogni modifica, e **rispetta sempre l'ANTI-PATTERN del campo `image:`** (mai toccato durante revisione testuale). Specifiche operative in `.claude/rules/02-content-design-pa.md` § "Livello qualitativo della redazione".

5. **AGGIORNAMENTO AGID — automazione + regola di coerenza**: le linee guida AGID sono in continuo aggiornamento. Il workflow `.github/workflows/aggiorna-manuale.yml` (lunedì 06:00 UTC) monitora 10 fonti ufficiali (Linee guida design PA, Designers Italia, Writing Toolkit, Content Toolkit, UI Kit, Bootstrap Italia, Accessibilità AGID, Dichiarazione, DPC) via hash SHA-256 con BeautifulSoup, e apre automaticamente issue con checklist tripartita quando una fonte cambia. **Regola di coerenza obbligatoria**: il manuale operativo (cartella `manuale/`) e le rules `.claude/` (lette da Claude Code in ogni sessione — CLI, mobile, cloud) devono dire **la stessa cosa** sulla stessa regola AGID. Aggiornarne uno senza l'altro = due fonti di verità divergenti + Claude applica regole obsolete in tutte le sessioni successive. Specifiche operative complete in `.claude/rules/02-content-design-pa.md` § "Sincronizzazione automatica con gli aggiornamenti AGID".

6. **MANUALE DI STILE**: il manuale operativo (v3.0, split a maggio 2026) ha l'indice in `MANUALE-SITO.md` nella root e i contenuti completi in `manuale/parte-NN-*.md`. Copre: procedura passo-passo per articoli (Parte 1), regole AGID integrate (Parte 2), specifiche immagini fascia blu (Parte 3), procedura pagine (Parte 4), checklist pre-pubblicazione (Parte 5), aggiornamento automatico settimanale (Parte 7). È il riferimento unico per la redazione dei contenuti, anche da parte di AI esterne.

7. **IMMAGINI**: ogni immagine di copertina deve avere la fascia blu istituzionale (#003366) con logo e testo "PROTEZIONE CIVILE / Gruppo Comunale Volontari — Genzano di Roma". Formato WebP, 1200px, max 200 KB. Specifiche complete in `manuale/parte-03-immagini-per-gli-articoli.md`.

8. **PIANO EDITORIALE**: il file `PIANO-EDITORIALE.md` elenca le fonti ufficiali da monitorare (DPC, INGV, ISPRA, Regione Lazio, Comune) e il calendario redazionale mensile. L'obiettivo è **tendere a un articolo al giorno** (300-365 l'anno) con un minimo sostenibile di **3-4 articoli a settimana** nei periodi di minore attività. Usalo per proporre nuovi articoli coerenti con la strategia.

9. **BANNER COL TITOLO INTOCCABILE — qualunque sia la fonte della foto**: il banner/copertina dell'articolo deve **SEMPRE** mostrare il **titolo dell'articolo** (cover tipografica con gradiente blu + titolo + badge + fascia, generata da `genera-cover.py` o `auto-cover-mancanti.py`). Funzioni: identità visiva, anteprima Open Graph corretta sui social, fallback universale in emergenza.

   **TUTTE** le foto (utente, Wikipedia/NASA/USGS/NOAA, stock Pexels/Pixabay/Unsplash) vanno **SEMPRE inline nel corpo** con lo shortcode `{{< foto >}}` (mai markdown `![]()` diretto), con fascia blu + alt text + caption credit/licenza. Convenzione foto multiple in articoli storici: 1ª dopo 1° H2, 2ª dopo 2° H2, ecc. **≥4 foto → galleria/carosello inline**. Il campo `image:` punta **sempre** alla cover tipografica (mai a foto utente/Wikipedia/altro): pre-push lanciare `python3 scripts/auto-cover-mancanti.py` o lasciare `image: ""` per generazione CI. Lo script `genera-immagini-social.py` legge le `{{< foto >}}` dal body e le usa in carosello Instagram automatico.

   ⚠️ **DIVIETO ASSOLUTO — marker `# TODO-foto-*` BANDITO**: sovrascriveva `image:` (viola questa regola) e veniva renderizzato come H1 finché il workflow CI non lo rimuoveva (incidente 3 maggio 2026). **Procedura corretta** per foto da fonti ufficiali: WebFetch per URL+autore+licenza → `curl -sL <URL> -o /tmp/foto.jpg` → `bash scripts/applica-fascia-foto.sh /tmp/foto.jpg <nome-DIVERSO-dallo-slug>` → shortcode `{{< foto >}}` inline + caption credit. Vedi agent `pc-image-fixer`.

   🔴 **ANTI-PATTERN — `image:` non si tocca durante una revisione**. Su task *"rivedi/riscrivi/correggi/miglioralo"*, **non modificare `image:`** salvo: (a) richiesta esplicita; (b) file inesistente → svuotalo a `""`. Foto pertinenti trovate durante la revisione vanno inline, mai nel banner. **Check pre-commit:** `git diff <file.md> | grep -E '^[+-]image' | head -5` — se trovi diff su `image:` non richiesto, ripristina. Storico: incidente del 9 maggio 2026 (ChatGPT-cloud articolo Giornata Europa) e dettagli in `02-content-design-pa.md`.

   API keys stock (Pexels/Pixabay/Unsplash) configurabili via GitHub Secrets, ma la foto va comunque inline.

10. **STAMPA**: il file `themes/flavour-pcgenzano/static/css/custom.css` contiene regole `@media print` globali che, quando l'utente clicca "Stampa" su una pagina, nascondono header/navbar/footer/banner/cookie/utility bar/page tools e stampano solo il contenuto della pagina (H1 + articolo + allegati) su A4 con margini standard. Non modificare questa sezione senza valutare l'impatto su tutti i layout.

11. **DATA ULTIMA REVISIONE (pagine legali/istituzionali)**: le pagine `privacy`, `note-legali`, `accessibilita`, `social-media-policy` hanno nel frontmatter il campo **`dataUltimaRevisione: "AAAA-MM-GG"`**. Il template `single.html` lo mostra come box evidente in cima al contenuto ("Pagina rivista il …"). Quando modifichi il contenuto sostanziale di una di queste pagine, aggiorna anche la data. Non usare stringhe tipo "Marzo 2026" nel corpo: il riferimento è unico e nel frontmatter. Il partial `page-tools.html` riconosce il campo e omette la `.Lastmod` automatica su queste pagine, per evitare date duplicate in conflitto.

12. **COMUNICAZIONE DI CRISI — gerarchia delle fonti** (in caso di conflitto, prevale il livello superiore): (1) **Italiano vincolante**: AGID + DPC (D.Lgs. 1/2018, Direttiva PCM 30 aprile 2021, "Io non rischio", codici colore) — su contenuti PC, DPC prevale su AGID; (2) **Scientifico italiano**: CNR (IRPI/INGV/IGAG) + ISPRA; (3) **Tecnico-operativo europeo**: EENA + CWA CEN/CENELEC; (4) **Standard internazionali**: ISO 22329:2021 + WCAG 2.2 AA; (5) **Normativa orizzontale**: DL 25/2025, GDPR, L. 4/2004, CAD.

    Post allerta/emergenza: struttura 6 punti (tipo / livello-colore / area+tempo / cosa fare / fonte / prossimo aggiornamento), hashtag localizzati, mai amplificare disinformazione per smentire, alt text + max 2 emoji + non solo-colore. Dettagli in `manuale/parte-13-social-media-policy-pubblica.md` § 13.7-13.9 e nelle rules `02`, `03`, `06`.

13. **CARTELLA `riferimenti-interni/`** (root del repo, NON deployata): contiene documentazione di lavoro per maintainer/AI di supporto che non va pubblicata sul sito (norme copyrighted, draft di consultazione, materiale interno). Hugo non la legge perché non rientra nelle cartelle native (`content/`, `static/`, `themes/`, `data/`, `assets/`, `layouts/`). Convenzione: 🟢 documenti pubblici → `static/manuali/`, 💶 copyrighted o riservati → `riferimenti-interni/<categoria>/`. Indice + stato accessibilità in `riferimenti-interni/README.md`. Specifiche complete nella regola `04c-hugo-static-cartelle.md`.

14. **SANDBOX CLAUDE CODE — sblocco fonti foto**: per le 7 fonti supportate (Wikipedia/Wikimedia, NASA, USGS, NOAA, Pexels, Pixabay, Unsplash) il repo ha `.claude/settings.local.json` (in `.gitignore`) con allowlist `permissions` + `sandbox.network.allowedDomains`. Riavviare Claude Code dopo creazione (sandbox letta solo all'avvio). Serve all'agent `pc-image-fixer` per WebFetch+curl+applica-fascia su foto **inline** (mai banner — punto 9). API keys solo per stock (gratuite): locale `~/.bashrc`, CI GitHub Secrets. Schema completo in `.claude/rules/08-claude-code-setup.md`.

15. **DATI ALLERTA METEO `data/allerta.json`**: due campi temporali distinti. `ultimo_aggiornamento` cambia **solo** quando il livello DPC cambia. `ultimo_controllo` cambia ogni volta che il workflow `check-allerta.yml` verifica il bollettino e committa (ogni ≥6 ore o cambio livello). Limite: max 4 commit/giorno + cambi di livello. Sia la barra allerta della homepage sia la pagina `/emergenza/` lite mostrano "Verificato: ..." sempre fresco. Il JS lato browser sulla homepage aggiorna ulteriormente il timestamp all'ora locale del client. Schema completo in `manuale/parte-09-file-dati-data-e-stati-del-sito.md` § 9.3.

16. **KIT CALAMITÀ — kit A4 stampabili per categorie vulnerabili**: hub `/formazione/kit-calamita/`, voce menu **"Kit pronti per situazioni vulnerabili"** sotto **"Per il Cittadino"** (NON "Per le scuole": target cittadino vulnerabile). Categorie: bambini, anziani, RSA, disabilità, neonati, gravidanza, animali, caregiver, pazienti terapie salvavita, senza fissa dimora, italiano L2, volontari PC. Ogni kit cita standard internazionali (NCTSN PFA, IFRC, WHO, Sphere 2018, ecc.) + normativa italiana + società scientifiche. Materiali liberi e riutilizzabili (CC BY-NC-SA 4.0 dove ARASAAC). **Aggiungere nuovo kit aggiorna 4 punti**: (a) `_index.md` del kit, (b) hub `/formazione/kit-calamita/`, (c) `content/mappa-sito/_index.md`, (d) assistente `themes/flavour-pcgenzano/layouts/assistente/list.html` (sotto-albero `kc_*`). Carte d'identità: template `.carta-id-*` in `static/formazione/kit-calamita-shared/print.css` (riga 11mm). Giochi: soluzione ruotata 180° (`.soluzione-capovolta`), vietato `<details>` + foglio operatore separato. Specifiche in `manuale/parte-20-kit-calamita-categorie-vulnerabili.md`.

17. **FEED RSS PUBBLICI**: Hugo genera 39 feed RSS 2.0 auto-discoverable (uno per sezione). Pagina divulgativa `/feed-rss/` per il cittadino, voce nel footer Hugo + `site-chrome.js`, card mappa-sito, nodo `info_servizi_rss` nell'assistente. Privacy-first (zero registrazione/cookie). Auto-generati da Hugo al build, niente da configurare.

18. **STANDARD ISO — hub `/standard-iso/`**: 30 schede ISO rilevanti per PC organizzate per famiglia (ISO/TC 292 emergency management, ISO 31000 risk, ISO 14090 clima, ISO 7010 segnaletica, ecc.). Voce menu sotto **Risorse**, presente in assistente + mappa-sito. ⚠️ **VINCOLO COPYRIGHT**: norme a pagamento — solo titolo/ambito/contestualizzazione italiana, mai testo della norma, link a iso.org/store.uni.com per dettagli. 10 news divulgative calendarizzate 12 maggio-12 giugno 2026. **Aggiungere nuovo standard aggiorna 4 punti**: (a) `content/standard-iso/iso-XXXX.md`, (b) tabella in `_index.md`, (c) eventuale card mappa-sito, (d) eventuale link assistente.

19. **TRADUZIONI — `<html lang>` dinamico + hreflang + og:locale**: 7 traduzioni (`/english/`, `/francais/`, `/deutsch/`, `/espanol/`, `/portugues/`, `/romana/`, `/esperanto/`) × 4 sotto-pagine = 28 pagine tradotte. Ogni `_index.md` ha `language: "<codice>"` (en/fr/de/es/pt/ro/eo) letto da `baseof.html` per `<html lang>` e da `meta-social.html` per `og:locale`. Partial `hreflang-tags.html` aggiunge `<link rel="alternate" hreflang>` per IT + 7 lingue + x-default sulle sezioni in whitelist (`$sezioniTradotte` hardcoded). Aggiungere nuova pagina tradotta: crea `_index.md` con `language` + aggiungi slug a `$sezioniTradotte`. Storia bug: fino all'8 maggio 2026 era hardcoded `lang="it"` → violazione WCAG 3.1.1 + Google duplicati.

## Automazioni periodiche (GitHub Actions)

Tutti i workflow di manutenzione girano **ogni lunedì** (primo giorno della settimana), scaglionati in orari diversi per non caricare il runner nello stesso momento. L'utente ha scelto il lunedì per avere una finestra settimanale costante di issue/verifica da affrontare.

| Workflow | Frequenza | Scopo |
|---|---|---|
| `deploy.yml` | Ogni push su `main` | Build Hugo + deploy Aruba (FTP) + GitHub Pages |
| `check-allerta.yml` | Ogni 5 minuti (`*/5 * * * *`) | Verifica stato allerta meteo Regione Lazio. Polling 5-min per latenza ≤7 min al cambio livello DPC; il commit di `data/allerta.json` resta vincolato a cambio livello effettivo o ultimo_controllo ≥5h45min (max ~4 commit/giorno + cambi reali). |
| `pubblica-programmata.yml` | Giornaliero 06:00 UTC | Rilancia il deploy ogni mattina: gli articoli `draft: false` con `date` futura entrano nel sito al passaggio del giorno (Hugo li escludeva finché la data era oltre `now()`). NB: `draft: true` non viene flippato — gli articoli devono essere `draft: false` (regola: niente articoli in revisione) |
| `lighthouse-audit.yml` | Post-deploy | Audit performance/accessibilità/SEO (si attiva dopo ogni deploy riuscito) |
| `smoke-test-post-deploy.yml` | Post-deploy | Verifica live: 20 pagine principali rispondono 200, 7 traduzioni accessibili, mini-app statiche, marker chiave su 7 pagine, 2 header sicurezza. Apre issue urgente se trova regressioni. Logica in `scripts/smoke-test-live.sh` (riusabile in locale) |
| `aggiorna-manuale.yml` | Lunedì 06:00 UTC | Confronta hash fonti AGID/Designers Italia/DPC (10 URL), apre issue con checklist tripartita se cambiano: (A) manuale operativo, (B) rules `.claude/` + CLAUDE.md + agent, (C) verifica finale. Regola di coerenza obbligatoria: manuale e rules dicono la stessa cosa |
| `update-bootstrap-italia.yml` | Lunedì 06:00 UTC | Verifica aggiornamenti Bootstrap Italia |
| `audit-sito.yml` | Lunedì 09:00 UTC | **Audit completo (sezioni)**: contenuti pubblicati (COI, NUE 112, telefono, sede, CAP, placeholder, asset, badge, date, allegati, frasi AGID, draft `_index`, schede stampabili, modalità emergenza, pagine legali, widget) + codice/template (build Hugo, articoli `draft:true`, link a slug inesistenti, sintassi JS, validità YAML workflow, path assoluti template, residui CCV-MB/lombardo/`/index.html`) + governance docs (file presenti, import CLAUDE, badge list coerente, formato date, frontmatter, riferimenti incrociati, pagine obbligatorie, shortcode foto, script export, `dataUltimaRevisione`) + audit aggiuntivo (mixed content `http://`, `image_alt` accessibility WCAG 1.1.1, coerenza dati istituzionali nelle 7 traduzioni, divergenze `hugo.toml` ↔ `data/numeri_utili.yaml`, smoke test rendering H1 pagine critiche, **8 link critici normativa/PDF locali con messaggi dedicati**). Apre 1 issue settimanale con tutti i findings |
| `check-links-sito.yml` | Lunedì 10:00 UTC | Crawl completo del sito con **lychee**: verifica TUTTI i link (interni + esterni, tutte le pagine), apre issue automatica su 404/drift. Catch-all per mantenere aggiornati hub Strumenti, widget, Area Download, link esterni nei contenuti |
| `stale-issues.yml` | Giornaliero 04:00 UTC | **Pulizia issue automatiche**: chiude le issue create dai workflow (`automazione`, `normativa-watcher`, `smoke-test`, `scarica-foto`) dopo 14 gg di inattività (marcatura "stale") + 7 gg ulteriori di silenzio (chiusura). Riapre se qualcuno commenta. **NON tocca** issue umane (label `tracking`, `audit-followup`, `enhancement`, `bug`, `pinned`, `urgente-permanente`). Logica `actions/stale@v9` |
| `normativa-watcher.yml` | Lunedì 06:00 UTC | **Sweep RSS settimanale** delle novità normative PC. Aggrega 37 query Google News (12 tematiche + 25 con filtro `site:dominio.it` per i 25+ siti istituzionali in whitelist: Normattiva, GU, Regione Lazio, DPC, VVF, ISPRA, CNR-IRPI, CMCC, ARPA, ISS, Camera, Governo, Corte Costituzionale, ecc.) + feed RSS TGR Lazio. Filtra per parole chiave PC, deduplica per URL, apre 1 issue/settimana con digest se trova hit (silenzioso se zero). Logica in `scripts/normativa-watcher.py` (riusabile in locale: `python3 scripts/normativa-watcher.py --days 7`). Output JSON archiviato come artifact GitHub Actions per 14 giorni |
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
