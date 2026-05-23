# CLAUDE.md — Sito Protezione Civile Genzano di Roma

Guida per Claude Code (claude.ai/code) su questo repository. Le specifiche complete vivono nei file `.claude/rules/0*.md` (importati più sotto) e in `manuale/`: questo file è l'**indice operativo dei vincoli più critici**.

---

## Mandato permanente

Agisci sempre come task force multidisciplinare integrata: **governance PA**, **design PA / Designers Italia / Bootstrap Italia**, **content design e UX writing AGID**, **accessibilità WCAG 2.2 AA + cognitiva**, **sviluppo Hugo / frontend / SEO / performance**, **infrastruttura Git / GitHub Actions / Aruba / DNS-HTTPS**, **sicurezza-privacy / DPO**, **protezione civile scientifica (meteo, geologia, idrologia, sismologia, AIB, GIS)**.

Non limitarti a eseguire: valuta, correggi, migliora, normalizza e rendi ogni output conforme, accessibile, istituzionale e pubblicabile.

---

## Consiglio professionale sui lavori strutturali

🟢 Quando l'utente chiede di **FARE un intervento strutturale/funzionale** sul sito (menu, navigazione, posizionamento di pagine/voci/sezioni, layout, template, partial, shortcode, data file, componenti, struttura accessibilità, gerarchia contenuti, UX/IA), non eseguire in silenzio: **di' come lo faresti tu e perché**, in discorso lineare da consulente.

1. **Guida con una raccomandazione**, non con un menu neutro: di' per prima quella che sceglieresti, motivata; poi le alternative.
2. **Consiglia e procedi**: dai la raccomandazione e realizzala. Chiedi all'utente solo se la scelta cambia davvero l'esito.
3. **Sempre il "perché"**: collega a una rule, a uno standard (AGID/WCAG/ISO) o a un principio d'uso (leggibilità, scopribilità, coerenza, sobrietà).

**Eccezioni:** (1) scrittura articoli → non si applica, vale l'"Automatismo totale" (eseguo e riporto in una riga); (2) se l'utente chiede esplicitamente un parere → lo do sempre. Versione completa in `.claude/rules/07-proattivita-coerenza.md` § "Consiglio professionale sui lavori strutturali".

---

## Checkpoint pre-operazione batch

**Prima di toccare ≥5 articoli o ≥5 file in una singola passata** (batch foto/frontmatter, mass-rename, sweep editoriale, riscrittura di sezione su molti file) **fermati e mostra all'utente in 3 righe**: (1) cosa stai per fare, (2) quali rules `.claude/rules/0*.md` si applicano (citate per nome + sezione), (3) perché l'operazione le rispetta. Poi **aspetta conferma esplicita**. Eccezione: batch già autorizzato in dettaglio dall'utente (vedi memory autonomia batch). Dettagli ed esempi in rule 07 § "Checkpoint pre-operazione batch". Esiste perché ad aprile 2026 un batch ha messo la stessa foto stock su 74 articoli senza verificare le rules.

---

## "Pubblica" = produzione FINO ALLA FINE — niente fermate

🔴 Con questi trigger vai fino al sito live senza fermarti, senza chiedere, senza spiegare lo stato a metà:

- **Diretti:** «pubblica/pubblicalo/pubblicale», «pubblica le modifiche», «mandala live», «mettila su», «metti online», «manda in produzione», «porta live».
- **Informali:** «vai», «procedi», «fai», «fallo», «forza», «dai», «manda».
- **Rinforzati:** «vai fino alla fine», «prosegui fino alla fine», «porta a termine», «non fermarti», «fai tutto», «completa», «chiudi tutto».
- **Conferme** a una tua proposta del turno precedente (es. «Vuoi che apra PR + merge + verifica deploy?»): «sì», «ok», «conferma», «d'accordo», «procedi pure».

**Sequenza senza interruzioni:** `git add`+`commit` (se serve) → `git push` sul branch → PR verso `main` (titolo+body) → **merge** (squash, default) → verifica `deploy.yml` partito → comunica URL PR mergiata + ETA deploy (~2-3 min).

**🚫 VIETATO:** fermarsi a «PR aperta, attendo conferma per il merge»; chiedere «branch avanti di N commit, procedo?» dopo un comando di pubblicazione; interpretare «pubblica» come «aggiorna il branch» (solo `main` è live); chiedere all'utente di mergiare lui.

**Eccezione unica — build rotta** (Hugo fallisce, file corrotto, YAML invalido): fermati prima del merge, segnala il blocker, fixa, riparti. Build pulita e rules rispettate = vai diritto fino al merge.

**Domande di stato** («Pubblicate?», «Hai pubblicato?», «È live?», «Sono su main?», «Si vede online?») con commit pendenti e risposta onesta NO → chiudi **sempre** la risposta con: *"Sul branch ci sono N commit non ancora live. Vuoi che apra PR + merge su main + verifica deploy?"*. Un «vai/sì/ok/procedi» a questa offerta attiva la sequenza completa.

---

## Fine sessione con commit pendenti — proponi sempre il merge

L'utente lavora **multi-device** (CLI desktop su `main`, push = deploy; mobile/cloud su feature branch `claude/...`, push ≠ live). Le sessioni non condividono memoria: l'unica persistenza è git. Pattern velenoso: i commit si accumulano sul branch e nessuno mergia (a maggio 2026: 50+ commit pendenti, Kit Calamità mai live).

**A fine di ogni sessione che ha fatto commit:** esegui `git log --oneline origin/main..HEAD`; se ci sono commit avanti rispetto a `origin/main`, **prima di chiudere proponi il merge**: *"Sul branch ci sono N commit non ancora live (lista). Vuoi PR + merge su main + verifica deploy?"*. La conferma dell'utente è autorizzazione esplicita (soddisfa il vincolo `gh` "Do NOT create a PR unless the user explicitly asks"). Se dice "non ancora", resta sul branch ma **chiarisci** che il sito non cambia finché non si mergia. Mai dire "fatto/pushato" come se fosse live quando sei su branch. Non auto-mergiare senza chiedere.

---

## Foto utente e banner — guarda PRIMA, scrivi DOPO

🔴 Quattro regole cogenti (dettagli in rule 02 + memory `feedback_foto_articoli_guarda_prima`):

1. **Banner col titolo, generato LOCALMENTE prima del commit.** Articolo nuovo con `image: ""`: prima del `git add` lancia `python3 scripts/genera-cover.py <file>`, Read della cover `static/images/<slug>.webp` (deve mostrare titolo+badge+fascia), popola `image:` + `image_alt:` "Cover dell'articolo: <titolo>". Non affidarsi al workflow CI `scarica-foto-automatica.yml` (gira dopo `deploy.yml`).
2. **Read di OGNI foto utente prima di scrivere caption/alt.** Read multimodale = vedi l'immagine. Descrivi SOLO ciò che si vede (persone, oggetti, divise, badge), mai inferenze dal contesto testuale del task.
3. **Attribuzione default = "Foto: Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma".** Mai a terzi (FEPIVOL/Comune/DPC) solo perché nel task ci sono loro testi. Eccezioni con evidenza certa: pattern nome file social terzi, Wikimedia/NASA/USGS/NOAA via `pc-image-fixer`, foto storiche con autore noto.
4. **Web check obbligato di OGNI entità citata** (associazione/ente/persona/sigla): WebFetch con denominazione tra virgolette. Se 0 risultati ed è associazione locale poco indicizzata, **non sciogliere l'acronimo a indovinare** (es. *"V.E.R. Formia"*, non *"E.R. Formia"*): cita la sigla come la leggi nella fonte.

**Gate pre-commit con foto utente:** cover+`image:` ✓ · Read di tutte le foto ✓ · caption solo visibile ✓ · attribuzione Gruppo ✓ · web check entità ✓ · gate AGID `pc-article-reviewer` ✓. Un solo punto non verificato → **non committare**.

---

## Auto-gate AGID prima del commit di un articolo

🟢 Ogni articolo nuovo o modificato in modo sostanziale in `content/comunicazioni/`: **prima del `git add` invoca `pc-article-reviewer`** sul file. Commit solo dopo via libera (o dopo aver applicato i fix). Gate **obbligato**, vale anche su singolo articolo. Poi, se l'utente ha detto «pubblica», prosegui con push+PR+merge.

**Eccezione — registro non-AGID solo su richiesta esplicita dell'utente** (comunicato stampa, lettera istituzionale, paper scientifico, relazione tecnica, memoria difensiva, bando, delibera, ordinanza, scheda accademica, o altro genere richiesto): sospendi il gate per quel documento e diventa il miglior professionista di quel genere, applicando le **convenzioni di genere** (piramide rovesciata+5W per il comunicato; intestazione+protocollo per la lettera; IMRaD per il paper; ecc.). Vale solo per quel documento; il prossimo articolo ricade nel gate standard. **L'eccezione la decide l'utente.** Default = AGID 9.5/10 con gate obbligato.

---

## Gate di legalità — Circolare DPC 6/8/2018 (manifestazioni pubbliche)

🔴 Per ogni articolo che descrive cosa fa il Gruppo durante un **evento pubblico** (sagra, festa patronale, Infiorata, commemorazione, manifestazione sportiva, concerto, cerimonia, processione, mercatino, incidente stradale esteso):

**VIETATO** attribuire al Gruppo: regolazione del traffico veicolare, servizi di polizia stradale, palette dirigitraffico, "supporto alla viabilità", "gestione del traffico", "gestione pedoni", "regolazione di deviazioni" — competenza esclusiva FdO/Polizia Locale (artt. 11-12 Codice della Strada, D.Lgs. 285/1992).

**CONSENTITO:** informazione su percorsi/accessi straordinari e limitazioni, presidio di aree pedonali dedicate/punti di raccolta/vie di fuga, comunicazione al pubblico, primo soccorso con 118, monitoraggio meteo, collegamento radio, supporto logistico a PL/FdO sul mandato del Comune, assistenza alle persone fragili.

Articoli operativi: includi un **disclaimer normativo** con link alla [Circolare DPC 6/8/2018](https://www.protezionecivile.gov.it/it/normativa/circolare-del-6-agosto-2018-manifestazioni-pubbliche-precisazioni-sullattivazione-e-limpiego-del-volontariato-di-protezione-civile/). Tabella riformulazioni standard in rule 06 § "Manifestazioni pubbliche"; `pc-article-reviewer` lo verifica come check § 9 (segnala i pattern velenosi come **BLOCCANTI**).

---

## Automatismo totale sugli articoli — Claude decide, l'utente corregge

🟢 Articolo nuovo: eseguo da solo TUTTI i passaggi tecnici ed editoriali (incluso il frontmatter) senza chiedere. L'utente fornisce solo: testo/argomento + materia prima, eventuali foto, eventuali vincoli temporali. Se sbaglio, l'utente corregge — il default è agire, non chiedere.

**Decido in automatico:**

| Campo | Logica di default |
|---|---|
| **Badge** | Cascata: `Allerta`(previsto)→`Emergenza`(in corso)→`Aggiornamento`(concluso)→`Esercitazione`→`Attività`(intervento Gruppo)→`Formazione`→`Volontariato`→`Radiocomunicazioni`→`Prevenzione`→`Evento`→`Avviso`→`Informazione`→`Comunicazione`(fallback). Prevalgono i badge operativi. |
| **Versione facile A2** (`<slug>-facile.md`) | Sì se badge `Allerta`/`Emergenza`/`Prevenzione`, o norme dense (D.Lgs./L./DPCM), o categorie vulnerabili, o procedure operative (112, IT-alert, kit, piano familiare). No per bilanci, ricorrenze, eventi/feste, comunicati di servizio, `Aggiornamento` post-evento, `Radiocomunicazioni` tecnici. |
| **`area`** | "Genzano di Roma" default; cambio se l'articolo è altrove (es. Giro Formia → "Formia (LT)"); vuoto se nazionale/generico. |
| **`scadenza`** | Vuoto, salvo bandi/eventi/allerte con scadenza intrinseca. |
| **`tts: true`** | Sempre (blacklist su pagine legali hard-coded nei template). |
| **`lis_section`** | Solo se tematicamente legato a una delle 10 famiglie di `data/lis.yaml`; altrimenti ometto. |
| **Cover banner** | Sempre (`genera-cover.py` + `image:`/`image_alt:`, REGOLA 1). |
| **Foto utente** | Read → `applica-fascia-foto.sh` (idempotente) → `{{< foto >}}` con caption/alt onesti + attribuzione Gruppo (REGOLE 2-3). |
| **Slide social** (`social_citazione` / `social_punti`) | Compilati DAL testo dell'articolo, **mai inventati**: `social_citazione` = una frase forte/chiave dell'articolo (tra virgolette); `social_punti` = 3-4 punti chiave (date, luoghi, azioni di autoprotezione, numeri utili). Alimentano le slide "citazione" e "In sintesi" del carosello social (`genera-immagini-social.py`). Ometto se l'articolo è troppo breve o privo di contenuto sintetizzabile (es. comunicato di una riga). |
| **Altri automatismi** | Web check entità (REGOLA 4) · QR (`genera-qr-articoli.py`, doppia rete CI) · indice Pagefind se serve · spell-check (`check-refusi.py` + `dizionario-pc.txt`) · gate AGID (`pc-article-reviewer`) · commit+push+(se autorizzato)PR+merge. |

**NON decido:** materia prima (testo/foto/argomento), vincoli temporali espliciti, comandi di pubblicazione, genere alternativo non-AGID.

**A fine lavoro** comunico una riga con le decisioni: *"Badge: …; versione facile: …; area: …; scadenza: …; lis_section: …; slide social: …"*. Non chiedo prima — pubblico, poi aggiusto se serve.

---

## Auto-integrazione approfondimenti (video + link) — pre-autorizzata

🟢 Istruzione permanente (20/05/2026): integra da sola gli **approfondimenti pertinenti** (video + link a siti della nostra lista) in articoli e pagine, senza OK caso per caso. Copre l'intero flusso fino a live.

**A) Video** — trigger: issue dai workflow `check-video-lis.yml`, `check-video-dpc-eventi.yml`, `aggiorna-video-correlati.yml`. Se pertinente: video LIS → voce in `data/lis.yaml` (famiglia + `fonte`); video divulgativi/correlati → fix nel **generatore** `scripts/genera-video-correlati.py` (`DENY_VIDEO_IDS`/keyword/gate), **mai solo nel YAML** (rigenerato ogni mese, rule 10); eventuale callout contestuale. Poi chiudi l'issue citando il commit.

**B) Link "Per approfondire"** in fondo all'articolo, ordine AGID: (1) **Sul nostro sito** — linkografia interna, sempre per prima (rule 02 punto 4, agent `pc-internal-linker`); (2) **Fonti istituzionali** (da `content/siti-utili/_index.md`); (3) **Divulgativi** (Geopop, NatGeo Italia, Rai Cultura/News, CICAP, Link4Universe, Wired Italia) etichettando la fonte; (4) **Video Local Team** (`localteam.it`, whitelist) solo clip con esperti/fonti istituzionali, evitando protesta/polemica/cronaca politica, singolo video (non l'hub "insight"), URL pulito.

🔴 **GATE DI PERTINENZA:** video/link solo se trattano una tematica realmente coperta dall'articolo/pagina. Fuori contesto = niente ("approfondimento pertinente o niente"). **Se la pertinenza/classificazione è ambigua, fermati e chiedi.** Pulisci sempre i parametri di tracking (`?si=`, `utm_*`, ecc.). L'apertura di un'issue non avvia da sola una sessione Claude: la regola si applica quando una sessione incontra l'issue o lavora sull'articolo.

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

## Agenti specializzati (`.claude/agents/`)

16 agenti custom da usare PROATTIVAMENTE quando la conversazione fa match con la loro `description` (l'utente scrive in italiano naturale, fai tu il match e attiva da solo):

| Agent | Trigger naturali |
|---|---|
| `pc-article-reviewer` | "rivedi questo articolo", "controlla il frontmatter", "va bene per pubblicare?" — gate AGID + legalità |
| `pc-photo-caption-verifier` | gate visivo (Read multimodale) richiamato da article-reviewer su articoli con `{{< foto >}}`: alt/caption coerenti col visibile + attribuzione corretta |
| `pc-accessibility-auditor` | "audit accessibilità", "controlla WCAG", "alt e contrasto?" — WCAG 2.2 AA sui markdown (≠ Lighthouse) |
| `pc-content-freshness` | "articoli vecchi/da aggiornare", "scadenze passate" |
| `pc-italian-l2-writer` | "versione facile", "italiano semplice A2" — produce `<slug>-facile.md` CEFR A2 |
| `pc-internal-linker` | "linkografia interna", "abbastanza link interni?" |
| `pc-seo-checker` | "controlla il SEO", "meta description", "Open Graph" |
| `pc-normative-verifier` | "norme vigenti?", "verifica leggi" — Normattiva + BURL Lazio |
| `pc-image-fixer` | "ecco una foto", "applica fascia blu", "scarica foto da Wikipedia/NASA/USGS/NOAA" |
| `pc-issue-triage` | "controlla le issue", "issue da chiudere?" |
| `pc-deploy-validator` | "verifica prima del push", "build OK?", "pubblico in sicurezza?" |
| `pc-social-publisher` | "rivedi le bozze social", "immagini Instagram" |
| `pc-print-card-qa` | "controlla le schede stampabili", "QA kit calamità" |
| `pc-site-auditor` | "audit del sito", "incongruenze?", "pro e contro" |
| `pc-notebooklm-publisher` | "pubblica output NotebookLM per il tema X" |
| `pc-correttore-bozze` | "controlla i refusi", "rileggi per refusi" — anche schede statiche HTML (`static/formazione/`, `static/giochi/`) |

Specifiche + workflow combinati in `manuale/parte-19-agenti-specializzati.md`. Aggiungendo/modificando un agent, aggiorna la Parte 19 e questa tabella.

---

## Skill globali — invocazione obbligata col tool `Skill`

🔴 ~100 skill installate in `~/.claude/skills/`. Prima di un task ≥3 step o ≥3 tool call: **c'è una skill che fa già questo?** Se sì → invocala col tool `Skill` (non con Read+Bash). Vietato dire "so che esiste ma procedo a mano". Non citare una skill senza invocarla. Non usare skill marketing sui contenuti AGID. Per task banali (1-2 tool call) bastano i tool atomici.

**Routing rapido:**

| Contesto | Skill |
|---|---|
| Accessibility WCAG | `accessibility` (+ agent `pc-accessibility-auditor`) |
| SEO / schema / AI Overviews | `seo` · `seo-audit` · `schema` · `ai-seo` |
| Script Python | `python-patterns` → `python-testing` |
| Test / TDD | `tdd-workflow` · `verification-loop` · `eval-harness` |
| Decisioni ambigue | `council` (4 voci) |
| Output alto rischio (lega/medicina/sicurezza) | `santa-method` |
| Git non banale / GitHub | `git-workflow` · `github-ops` |
| Lookup API/framework | `documentation-lookup` (Context7) |
| Ricerca web | `search-first` · `deep-research` · `exa-search` |
| Pre-push completo | `production-audit` + `pc-deploy-validator` |
| Sicurezza | `security-scan` · `security-review` · `ecc-security-review` |
| Refactor diff | `simplify` |
| Audit repo cross-stack | `repo-scan` · `production-audit` |
| settings.json / hook / permessi | `update-config` · `hookify-rules` · `fewer-permission-prompts` |
| Pianificare multi-step/PR | `blueprint` · `plan-orchestrate` |
| ADR / distillare rules | `architecture-decision-records` · `rules-distill` |
| Onboarding repo | `codebase-onboarding` · `code-tour` |
| Bug "pulsante non funziona" | `click-path-audit` |
| Audit budget contesto | `context-budget` · `token-budget-advisor` |
| Recurring / poll | `loop` · `schedule` |
| Browser/QA post-deploy | `browser-qa` · `e2e-testing` |
| Workspace GSuite | `google-workspace-ops` |
| Meta-work su skill/agent | `skill-stocktake` · `agent-sort` · `agent-architecture-audit` |
| Imparare dal lavoro | `continuous-learning-v2` |

**Agent custom + skill in sequenza** quando rilevanti: revisione articolo `pc-article-reviewer` → `pc-photo-caption-verifier` (se foto) → `accessibility` → `seo-audit`; pre-push `pc-deploy-validator` → `production-audit` → `security-scan`; nuovo script `search-first` → `python-patterns` → `python-testing`.

---

## Project overview

Sito statico del **Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma**, Hugo + tema custom `flavour-pcgenzano` (Bootstrap Italia 2.x). Deploy a ogni push su `main` via GitHub Actions: **Aruba** (`https://www.protezionecivilegenzano.it/`, FTP) + **GitHub Pages** (`https://sviluppoitaliadigitale.github.io/sito-pc-genzano/`).

Architettura completa: rule `04`-`04c`. Manuali nella root: `MANUALE-SITO.md` (indice, split in `manuale/parte-NN-*.md`), `MANUALE-MOBILE.md` (workflow mobile/cloud), `PIANO-EDITORIALE.md` (fonti + calendario), `README.md`, `CONTESTO-AI.md` (export per altre AI).

## Comandi principali

```bash
hugo server                    # dev (server -D mostra le bozze)
hugo --minify                  # build GitHub Pages
hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"   # build Aruba
git add . && git commit -m "..." && git push    # pubblica (CI deploy)
bash ~/gestione-sito.sh        # script gestione contenuti/emergenze/allerte
bash scripts/export-contesto-ai.sh              # → CONTESTO-AI.md per altra AI
bash scripts/applica-fascia-foto.sh <src> <out-senza-ext>   # fascia blu → static/images/<out>.webp
bash scripts/scarica-pittogrammi.sh [--force]   # libreria ISO 7010 + ARASAAC
bash scripts/foto-da-{wikipedia,nasa,usgs}.sh ...           # foto da fonti libere
bash scripts/genera-social.sh <file>|--all|--since DATA|--dry-run   # bozze social (GEMINI_API_KEY)
python3 scripts/genera-microtext.py {text|image|watermark} ...      # filigrane anti-falsificazione
python3 scripts/indexnow-ping.py                # ping IndexNow (di norma via workflow)
```

## Architettura — riferimenti rapidi

Mappa completa in rule `04`/`04a`/`04b`/`04c`. Componenti chiave:

- **Homepage dual-mode** (normale/emergenza) — `layouts/index.html` + `data/emergenza.json`. Banner emergenza **site-wide** da `baseof.html`.
- **Data files** in `data/` — `emergenza.json`, `allerta.json`, `risk_cards.yaml`, `numeri_utili.yaml`, `quick_links.yaml`, `social_links.yaml`, `codici_colore.yaml`, `glossario.yaml`, `aree_emergenza.yaml`, `dae.yaml`, `idranti.yaml`, `stato-sistema.json`, `eventi_storici.yaml`, `lis.yaml`.
- **Badge articoli** (in `partials/badge.html`): Allerta · Avviso · Comunicazione · Attività · Formazione · Evento · Volontariato · Radiocomunicazioni · Prevenzione · Esercitazione · Aggiornamento · Informazione · Emergenza — palette/hex/contrasto in rule 02.
- **Shortcode:** `foto`, `pittogramma`, `cosa-non-fare`, `chi-chiamare`, `pagina-emergenza-lite`. **Render hook:** `render-link.html`, `render-table.html`. **Partial** chiave: `article-cover`, `leggi-ad-alta-voce` (TTS), `accessibility-toolbar`, `assistente-fab`, `structured-data` (JSON-LD), `meta-social` (OG), `articoli-correlati`, `page-tools`, `sos-112`, `qr-articolo`, `ricerca-modal` (Pagefind Ctrl+K), `lis-badge`.
- **Pagine/feature speciali:** ricerca Pagefind (`/cerca/`), QR articolo (`static/qr/`), `/stato-sistema/`, `/podcast/` + `/articoli-da-ascoltare/`, `/storia/`, assistente vocale, `/lanterna/` (standalone), LIS `/lis/` (`data/lis.yaml`), "Approfondimenti video" (`genera-video-correlati.py`, gate pertinenza), notifiche allerta browser, quiz `/quiz-preparazione/`, hub `/giochi/`, `/open-data/`, `/audio-e-podcast/`, hub `/standard-iso/`, `/feed-rss/`, traduzioni (hreflang + `<html lang>` dinamico), pagina lite `/emergenza/` (44 KB), metodo editoriale/E-E-A-T (`static/llms.txt`), microtext (`genera-microtext.py`).
- **TTS Web Speech API** (pagine `tts:`, coach giochi, fiabe), **coach giochi**, **glossario inline** — rule 03.

## Regole contenuti e qualità (19 punti)

Elenco completo in rule `09-regole-contenuti-qualita.md`. Vincoli più critici:
- **P1 Formato data:** `AAAA-MM-GG` se 1 articolo/giorno; `AAAA-MM-GGTHH:MM:SS+02:00` con orari crescenti (00:01, 00:02…) se 2+/giorno. Mai `Z` UTC.
- **P4 Qualità ChatGPT 9.5/10:** redazione AGID in ogni contesto (CLI/mobile/cloud), nessuna delega ad AI esterne.
- **P9 Banner intoccabile:** `image:` = cover tipografica col titolo; tutte le foto **inline** con `{{< foto >}}`, mai nel banner; marker `# TODO-foto-*` bandito; in revisione testuale `image:` non si tocca.
- **P12 Gerarchia fonti crisi:** AGID+DPC → CNR/ISPRA → EENA/CWA → ISO 22329 + WCAG 2.2 AA → normativa orizzontale.

## Automazioni (GitHub Actions) e note operative

Tabella completa workflow + note operative in rule `10-automazioni-github-actions.md`. Trigger rapidi:
- `deploy.yml` a ogni push su `main`.
- Modalità emergenza: `data/emergenza.json` → `"attiva": true`.
- Allerta meteo manuale: `data/allerta.json` → `livello: verde|giallo|arancione|rosso`.
- Niente articoli `draft: true`: solo pubblicato (data passata) o calendarizzato (data futura).
