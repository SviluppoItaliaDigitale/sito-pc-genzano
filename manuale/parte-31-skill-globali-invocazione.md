_[Indice manuale](README.md)_

# Parte 31 — Skill globali Claude Code: invocazione obbligata col tool `Skill` (maggio 2026)

A maggio 2026 Claude Code ha installate ~100 **skill globali** in `~/.claude/skills/`, residue del cleanup conservativo del 18 maggio (da 269 a 102, vedi `feedback_skill_cleanup_conservativo.md` nella memoria). Sono **pattern operativi pre-ottimizzati** — accessibilità WCAG, SEO, audit del repo, ricerca, plan multi-step, sicurezza, parsing testo, ecc. — caricati in contesto a ogni sessione.

**Il problema che questa Parte risolve**: averle installate non basta. Vanno **invocate col tool `Skill`** quando il task lo richiede, altrimenti restano peso morto in contesto. L'utente ha richiesto esplicitamente il 18 maggio 2026: *"fai in modo che queste skills vengano da te automaticamente richiamate ok? non le lasciare nel dimenticatoio... usale quando servono!!"*

Questa Parte codifica la politica per **te (utente)** e per **Claude Code** in tutte le sessioni.

---

## 31.1 La regola in 3 righe

1. Quando il task ha **complessità ≥3 step o ≥3 tool call**, Claude scansiona la lista skill nel system reminder PRIMA di scrivere codice.
2. Se trova una skill che già fa quel lavoro → la invoca col tool `Skill` (non con Read+Edit+Bash a mano).
3. Se non trova match → procede con tool atomici.

La regola estesa con vincoli e divieti vive in `CLAUDE.md` § *"Skill globali — invocazione obbligata col tool `Skill`"*. Questa Parte è la versione operativa dettagliata per consultazione.

---

## 31.2 Differenza tra agent custom `pc-*` e skill globali

Servono a cose diverse e **convivono**.

| Aspetto | Agent custom `pc-*` (in `.claude/agents/`) | Skill globali (in `~/.claude/skills/`) |
|---|---|---|
| Cosa sono | 15 profili professionali virtuali con expertise specifica del sito Genzano | ~100 pattern tecnici trasversali (accessibilità, SEO, audit, ricerca, ecc.) |
| Dominio | Editoriale + tecnico **del sito istituzionale PA** | Tecnico **generale**, applicabili in vari progetti |
| Esempi | `pc-article-reviewer` (gate AGID), `pc-image-fixer` (fascia blu), `pc-photo-caption-verifier` (Read multimodale foto) | `accessibility` (WCAG ARIA), `seo-audit`, `python-patterns`, `tdd-workflow`, `council` |
| Storia | Creati 6-16 maggio 2026 per gli incidenti specifici del nostro flusso editoriale | Provengono dal repo upstream di Affaan Mustafa (ECC), curate al 18 maggio 2026 |
| Come si attivano | Auto-match sulle frasi italiane naturali (vedi Parte 19) | Auto-match sui pattern del task; Claude le invoca col tool `Skill` |

**Co-uso tipico**: prima l'agent custom (taglio repo-specifico), poi 1-2 skill globali (cross-cutting). Esempio per la revisione di un articolo:

```
1. pc-article-reviewer (custom): frontmatter + AGID + check immagine banner
2. pc-photo-caption-verifier (custom): Read multimodale di ogni foto
3. accessibility (skill): WCAG 2.2 AA cross-cutting (alt, headings, link)
4. seo-audit (skill): meta description, OG image, canonical, sitemap entry
```

---

## 31.3 Routing rapido — task frequenti sul repo → skill primaria

Tabella curata dei pattern più ricorrenti su `sito-pc-genzano`. Versione corta in `CLAUDE.md`; questa è la versione lunga con esempi.

### Accessibilità

- **`accessibility`** — quando lavori su contenuto markdown / pagina HTML / componente UI e devi garantire WCAG 2.2 AA. Lavora a fianco del custom `pc-accessibility-auditor`: la skill è il pattern generale (genera ARIA per Web/Native, traits iOS/Android), l'agent è il check editoriale del sito.

### SEO e visibilità

- **`seo`** — audit + plan + implementazione SEO trasversale.
- **`seo-audit`** — audit tecnico SEO mirato (meta tag, core web vitals, crawl, indicizzazione, page speed).
- **`schema`** — markup strutturato JSON-LD (rich snippet, FAQPage, HowTo, Article).
- **`ai-seo`** — ottimizzazione per AI Overviews / GEO / LLMO (essere citati da ChatGPT, Perplexity, Gemini).

In tandem col custom `pc-seo-checker` per i check specifici del nostro sito (Open Graph 1200×630, `og:type=article`, `Organization+NGO`).

### Python — gli script del repo

- **`python-patterns`** — Pythonic idioms, PEP 8, type hints. Da invocare prima di scrivere uno script nuovo in `scripts/`.
- **`python-testing`** — pytest, TDD, fixtures, mocking, coverage. Dopo aver scritto lo script.

Esempio applicato: quando ho scritto `scripts/genera-pacchetti-schede.py` (17 maggio 2026) avrei dovuto invocare `python-patterns` per gli idioms (`pathlib.Path`, `dataclasses`, `f-string`, ecc.) e `python-testing` per i test associati. Oggi quello script ha `pathlib` + type hints ma niente test: prossima iterazione li aggiunge.

### Test e verifica

- **`tdd-workflow`** — quando aggiungi una feature o fixi un bug e vuoi che la verifica preceda l'implementazione (red → green → refactor).
- **`verification-loop`** — quando un task multi-step richiede verifica progressiva (ogni step ha un check).
- **`eval-harness`** — framework di valutazione formale (eval-driven development) per task agentici.

### Decisioni ambigue

- **`council`** — 4 voci adversariali quando esistono più approcci validi e serve disagreement strutturato prima di scegliere.
- **`santa-method`** — 2 review agent indipendenti, loop di convergenza obbligato, per output ad alto rischio (legale, medico, comunicazione di crisi). Più pesante di `council`, più stringente.

### Git e GitHub

- **`git-workflow`** — operazioni git non banali (rebase interattivo, conflict resolution, conventional commits, recovery da reset).
- **`github-ops`** — issue triage, PR management, gh CLI, release. In tandem con `pc-issue-triage` (custom).

### Ricerca

- **`search-first`** — workflow research-before-coding. Da invocare PRIMA di scrivere codice nuovo: "esiste già una libreria/pattern/skill che fa questo?".
- **`deep-research`** — multi-source con firecrawl + exa MCP, output con citazioni.
- **`iterative-retrieval`** — quando l'agent si perde nel context, retrieval progressivo.
- **`exa-search`** — neural search via Exa per web/code/company research.
- **`documentation-lookup`** — Context7 MCP per docs aggiornate di framework. Da preferire a indovinare l'API.

### Audit e validazione

- **`production-audit`** — readiness audit pre-launch, post-merge, "che cosa si rompe in prod?".
- **`repo-scan`** — audit cross-stack del codice, classificazione file, librerie third-party.
- **`security-scan`** — scan vulnerabilità config `.claude/`, MCP, hook.
- **`ecc-security-review`** — checklist sicurezza per auth, input utente, secret, endpoint API.
- **`security-review`** (built-in) — security review delle modifiche pendenti sul branch corrente.

In tandem con `pc-deploy-validator` (custom: 26 check specifici del sito) e `pc-site-auditor` (custom: audit whole-site read-only).

### Pianificazione multi-step

- **`blueprint`** — turn una richiesta in un piano step-by-step per task multi-PR / multi-sessione, con review adversarial, dependency graph, anti-pattern catalog.
- **`plan-orchestrate`** — legge un piano e produce orchestrate prompts per agent chains.

### Documentazione di decisioni

- **`architecture-decision-records`** — quando prendi una decisione architetturale durante una sessione, salvala come ADR strutturato (context + alternatives + rationale).
- **`rules-distill`** — estrai principi ricorrenti da skill/sessioni e distillali in nuove rules (output: append/revise/create in `.claude/rules/`).

### Onboarding

- **`codebase-onboarding`** — analizza un repo sconosciuto, genera guida con architecture map, entry points, conventions, starter CLAUDE.md.
- **`code-tour`** — crea file `.tour` (CodeTour) con walkthrough step-by-step ancorati a file:linea reali.

### Bug di UI / refactor

- **`click-path-audit`** — traccia ogni button/touchpoint attraverso la sequenza di state change per trovare bug dove le funzioni individualmente funzionano ma cancellano l'effetto l'una dell'altra. Da usare dopo refactor di shared state stores.

### Gestione errori / parsing

- **`error-handling`** — pattern per TypeScript/Python/Go: typed errors, error boundaries, retries, circuit breakers, messaggi user-facing.
- **`regex-vs-llm-structured-text`** — decision framework regex vs LLM per parsing strutturato; start with regex, add LLM only for low-confidence edge cases.

### Contesto e costi

- **`context-budget`** — audit consumo context window (agent, skill, MCP, rules) e raccomandazioni di token-savings.
- **`token-budget-advisor`** — quando l'utente chiede esplicitamente versione corta/lunga (offre scelta informata).
- **`cost-tracking`** — report spending/usage da DB locale.
- **`cost-aware-llm-pipeline`** — model routing by task complexity, prompt caching.

### Skill/Agent meta-work

- **`skill-stocktake`** — audit qualità skill/commands (Quick Scan o Full).
- **`skill-scout`** — ricerca skill esistenti (locali/marketplace/GitHub) prima di crearne una nuova.
- **`skill-comply`** — verifica se skill/rules/agent vengono **effettivamente** rispettati (auto-genera scenari + classifica behavior + compliance rate).
- **`agent-sort`** — sort skill/commands/rules/hooks in DAILY vs LIBRARY buckets per uno specifico repo.
- **`agent-architecture-audit`** — diagnostic 12-layer agent stack: wrapper regression, memory pollution, tool discipline failure.

### Hook / config / built-in

- **`update-config`** (built-in) — modifiche `settings.json`, hook, permessi.
- **`hookify-rules`** — pattern per creare hookify rules.
- **`fewer-permission-prompts`** — scan transcript + add allowlist per ridurre i prompt di permessi.
- **`simplify`** (built-in) — review code changed, fix issues trovati.
- **`init`** (built-in) — crea CLAUDE.md per nuovo repo.
- **`review`** (built-in) — review PR.

### Loop / scheduling

- **`loop`** — task ricorrente o polling (es. *"check deploy ogni 5 minuti"*).
- **`schedule`** — cron remoti / scheduled agents.

### Browser testing

- **`browser-qa`** — automated visual testing UI con browser automation post-deploy.
- **`e2e-testing`** — Playwright E2E, Page Object Model, CI/CD, artefacts, flaky test.

### Workspace esterno

- **`google-workspace-ops`** — Drive, Docs, Sheets, Slides come workflow surface unico.

### Continuous learning

- **`continuous-learning-v2`** — instinct-based learning system, project-scoped via hook, evolve instincts in skill/command/agent. Da invocare dopo task non-banali per estrarre lezioni riusabili.

---

## 31.4 Cosa NON fare

- ❌ **Re-implementare a mano** in Bash/Read/Edit ciò che una skill copre già con procedura migliore. Esempio velenoso: scrivere 30 righe di `grep` + `awk` per estrarre meta description quando esiste `seo-audit`.
- ❌ **Citare il nome della skill all'utente** ("la skill X farebbe questo") **senza invocarla**: o la usi o non la menzioni.
- ❌ **Invocare skill marketing** (cold-email, page-cro, churn-prevention, ecc. se mai re-introdotte) sui contenuti AGID del sito istituzionale — sono globali ma fuori scope PA. Vedi memoria `feedback_skill_cleanup_conservativo`.
- ❌ **Forzare invocazione skill per task banali** (1-2 tool call, fix mirato, refuso, rename file): per quelli i tool atomici bastano. La soglia è ~3 step o ~3 tool call.

---

## 31.5 Eccezione — registro non-AGID

Quando l'utente chiede esplicitamente un documento in registro diverso dal linguaggio AGID per il cittadino (comunicato stampa, lettera istituzionale formale, paper scientifico, relazione tecnica, ordinanza, bando, ecc.), come da CLAUDE.md § *"Auto-gate AGID prima del commit"*:

- Sospendi le skill di contenuto AGID (`accessibility`, `content-strategy`, `article-writing` brand-voice) come **default**.
- Mantieni le skill tecniche (Python, git, audit, deploy) per il supporto.
- Diventa il miglior professionista del genere richiesto e applica le convenzioni del settore.

---

## 31.6 Storia e versioning

- **18 maggio 2026** — cleanup conservativo: 269 → 102 skill. EXCLUDE list (135 ECC) + KEEP list (6 MKT: `ai-seo schema seo-audit site-architecture content-strategy social`) nei 2 sync script in `~/.claude/skill-sources/`. Backup in `~/.claude/backups/skill-cleanup-20260518-092623/`.
- **18 maggio 2026** — audit chirurgico dei 15 agent `pc-*`: 3 fix applicati (pc-image-fixer +WebFetch, pc-article-reviewer forma vs taglio, pc-deploy-validator item #26 spostato).
- **18 maggio 2026** — codificata la politica di invocazione skill in `CLAUDE.md` + memoria persistente `feedback_skill_proactive_invocation.md` + questa Parte 31.

**Per re-aggiungere una skill rimossa**: rimuovi il nome dalla EXCLUDE list (`sync-everything-claude-code.sh`) o aggiungilo alla KEEP list (`sync-marketingskills.sh`), poi lancia il sync script. Il symlink viene ricreato e la skill torna disponibile alla prossima sessione.

**Per estendere il routing** di questa Parte quando un nuovo task pattern diventa frequente: aggiungi la riga in 31.3 + aggiorna la tabella in `CLAUDE.md` § *"Skill globali"* (entrambi i posti devono restare sincronizzati).

---

## 31.7 Riferimenti

- `CLAUDE.md` § *"Skill globali — invocazione obbligata col tool `Skill`"* — versione corta della politica, sempre in contesto a ogni sessione.
- `~/.claude/projects/-home-iu0qvw-sito-pc-genzano/memory/feedback_skill_proactive_invocation.md` — memoria persistente.
- `~/.claude/projects/-home-iu0qvw-sito-pc-genzano/memory/feedback_skill_cleanup_conservativo.md` — storia del cleanup e regole sul re-aggiungere skill.
- `~/.claude/skill-sources/sync-everything-claude-code.sh` — script con EXCLUDE list (ECC, 135 voci).
- `~/.claude/skill-sources/sync-marketingskills.sh` — script con KEEP list (MKT, 6 voci).
- Parte 19 — agent custom `pc-*` (compagni delle skill globali, dominio editoriale repo-specifico).
