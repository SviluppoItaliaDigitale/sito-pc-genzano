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
@.claude/rules/09-regole-contenuti-qualita.md
@.claude/rules/10-automazioni-github-actions.md

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

## Regole contenuti e qualità (19 punti)

L'elenco numerato completo (formato data, AGID, qualità testi, banner intoccabile, anti-pattern `image:`, stampa, dataUltimaRevisione, gerarchia fonti crisi, sandbox foto, allerta meteo, kit calamità, feed RSS, standard ISO, traduzioni) è in `.claude/rules/09-regole-contenuti-qualita.md`. Sintesi dei vincoli più critici da tenere a mente:

- **Punto 1 — Formato data**: `AAAA-MM-GG` se 1 articolo/giorno; `AAAA-MM-GGTHH:MM:SS+02:00` con orari crescenti `00:01, 00:02, ...` se 2+ articoli/giorno. Mai `Z` UTC.
- **Punto 4 — Qualità ChatGPT 9.5/10**: redazione AGID in tutti i contesti (CLI/mobile/cloud), nessuna delega ad AI esterne.
- **Punto 9 — Banner intoccabile**: il campo `image:` è la cover tipografica col titolo. Tutte le foto (utente/Wikipedia/NASA/stock) vanno **inline** nel corpo con `{{< foto >}}`, mai nel banner. Marker `# TODO-foto-*` bandito. Anti-pattern: durante una revisione testuale, `image:` non si tocca.
- **Punto 12 — Gerarchia fonti crisi**: AGID+DPC vincolanti italiani → CNR/ISPRA scientifici → EENA/CWA tecnici UE → ISO 22329 + WCAG 2.2 AA → normativa orizzontale.

Tutti gli altri punti (2-3, 5-8, 10-11, 13-19) restano nel file split.

## Automazioni periodiche (GitHub Actions) e Key operational notes

La tabella completa dei workflow di manutenzione (deploy, check-allerta doppio trigger, audit-sito, check-links, normativa-watcher, scarica-foto-automatica, genera-social-bozze, ecc.) + le note operative chiave (modalità emergenza, allerta meteo, draft, deploy CI, credenziali FTP) sono in `.claude/rules/10-automazioni-github-actions.md`.

Trigger rapidi da ricordare:
- `deploy.yml` parte a ogni push su `main`.
- Modalità emergenza: `data/emergenza.json` → `"attiva": true`.
- Allerta meteo manuale: `data/allerta.json` → `livello: verde|giallo|arancione|rosso`.
- Regola progetto: niente articoli `draft: true`. Solo pubblicato (data passata) o calendarizzato (data futura).
