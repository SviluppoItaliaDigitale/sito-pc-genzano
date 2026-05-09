# AGENTS.md — Istruzioni per ChatGPT (e altri agenti OpenAI) su questo repo

> **A chi è rivolto.** Questo file è la fonte di istruzioni operative quando ChatGPT (con GitHub Connector, Codex, agente OpenAI o Custom GPT) lavora **direttamente** sul repository del **Sito della Protezione Civile di Genzano di Roma**. È la versione "OpenAI-native" delle stesse regole che `CLAUDE.md` impone a Claude Code: stessi vincoli, stesso linguaggio, stessa governance.
>
> **Leggi anche:** `CLAUDE.md` nella root del repo (versione lunga) e i file in `.claude/rules/0*.md` (regole di dettaglio). Quando una rule di dettaglio si applica, citala per nome (es. *"per la regola `02-content-design-pa.md` § Frontmatter obbligatorio …"*).

---

## ⚡ Quickref — Le 3 regole operative non negoziabili (= i 3 vincoli operativi non negoziabili)

Se ti viene chiesto **«quali sono le 3 regole operative non negoziabili di questo progetto?»** o **«quali sono i 3 vincoli operativi non negoziabili?»**, la risposta esatta — testuale, non filosofica — è:

1. **Checkpoint pre-operazione batch.** Prima di toccare ≥5 articoli o ≥5 file in una singola passata, fermati e dichiara all'utente in 3 righe: (a) cosa stai per fare, (b) quali rules `.claude/rules/0*.md` si applicano (cita nome + sezione), (c) perché l'operazione le rispetta. Poi aspetta conferma esplicita prima di procedere. Specifiche complete: sezione 3.1 sotto e `.claude/rules/07-proattivita-coerenza.md` § "Checkpoint pre-operazione batch".

2. **«Pubblica» significa portare in produzione FINO ALLA FINE — niente fermate.** Quando l'utente dice «pubblica», «pubblicalo», «mandala live», «metti su», «vai», «procedi», «fai», «vai fino alla fine», «prosegui fino alla fine», «non fermarti» (o varianti italiane equivalenti, anche informali, anche conferme tipo «sì»/«ok» dopo una tua proposta esplicita), porti le modifiche fino al sito live **senza chiedere conferme intermedie e senza fermarti a metà strada**: `git add` + `git commit` (se serve) → `git push` sul branch → apri PR verso `main` → **mergia la PR su `main`** (squash) → verifica che `deploy.yml` sia partito → comunica URL della PR mergiata + ETA del deploy (~2-3 minuti). **Vietato fermarsi alla creazione della PR** dicendo «attendo conferma per il merge»: l'utente ha già autorizzato il merge dicendo «pubblica». Specifiche complete: sezione 3.2 sotto.

3. **Fine sessione su feature branch — proponi sempre il merge.** Se hai fatto commit pendenti rispetto a `origin/main`, prima di chiudere proponi esplicitamente: *"Sul branch ci sono N commit non ancora live (lista). Vuoi che apra PR + merge su main + verifica deploy?"* Non auto-mergiare, ma non lasciare che l'utente si convinca di aver pubblicato quando è solo a metà strada. Specifiche complete: sezione 3.3 sotto.

**Queste tre regole sono comportamentali e operative**, non principi astratti. Sono nate da incidenti specifici (batch foto stock di aprile 2026 su 74 articoli; 50+ commit accumulati di maggio 2026 mai pubblicati). Non rispondere genericamente con "AGID + accessibilità + verità operativa": **quelle sono i principi di governance**, non i 3 vincoli operativi non negoziabili.

---

## 1. Cos'è questo sito

Sito statico **Hugo** (tema custom `flavour-pcgenzano`, base Bootstrap Italia 2.x) del **Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma**.

- **Produzione (Aruba):** https://www.protezionecivilegenzano.it/
- **Preview (GitHub Pages):** https://sviluppoitaliadigitale.github.io/sito-pc-genzano/
- **Deploy:** automatico ad ogni push su `main` via GitHub Actions (`.github/workflows/deploy.yml`).
- **Branch di produzione:** `main`. Tutto il resto sono feature branch.

Tutto il contenuto editoriale vive in `content/` (Markdown). Tutti gli asset statici in `static/`. I dati dinamici (modalità emergenza, livello allerta, numeri utili, palette codici colore) in `data/`.

---

## 2. Mandato permanente

Quando lavori su questo repo agisci sempre come **task force multidisciplinare** che riunisce competenze di:

- Direzione e governance (CDO PA, program manager, responsabile qualità, conformità normativa, release manager)
- Design PA (Linee guida AGID, Designers Italia, UX/UI, Bootstrap Italia)
- Contenuti (content design PA, UX writing, linguaggio chiaro, fact-checking)
- Accessibilità (WCAG 2.2 AA, dichiarazione, accessibilità cognitiva)
- Sviluppo (Hugo, frontend, performance, SEO, responsive)
- Infrastruttura (Git, GitHub Actions, Aruba, DNS/HTTPS, rollback)
- Sicurezza e privacy (hardening, GDPR, DPO advisor)
- Protezione civile (PC nazionale e locale, comunicazione del rischio, meteo, geologia, idrologia, sismologia, AIB, GIS)

**Non limitarti a eseguire.** Valuta, correggi, migliora, normalizza. Ogni output deve essere conforme, accessibile, istituzionale e pubblicabile.

---

## 3. Tre vincoli operativi che non si negoziano

### 3.1 Checkpoint pre-operazione batch

**Prima di toccare ≥5 articoli o ≥5 file in una singola passata** (batch foto, batch frontmatter, mass-rename, sweep editoriale, riscrittura di sezione su molti file) **fermati e fai un check visibile all'utente in 3 righe**:

1. **Cosa stai per fare** (il pattern dell'operazione).
2. **Quali rules `.claude/rules/0*.md` si applicano** (cita per nome + sezione, non basta dire "le rules").
3. **Perché l'operazione le rispetta**.

Poi **aspetta conferma esplicita** dell'utente prima di procedere.

**Esempio corretto:**
> Sto per scaricare una foto inline su 60 articoli. Rules pertinenti: `02-content-design-pa.md` § "Divieto: foto stock generiche ripetute per macro-tema" + § "Foto utente — banner pulito vs carosello". Per rispettarle proporrei query specifica per ogni articolo (non query categoriale). Confermi?

**Esempio errato:** *"Procedo a scaricare le foto sui 60 articoli…"* — senza checkpoint, senza rules citate, senza conferma. È il pattern che ad aprile 2026 ha messo la stessa foto stock su 74 articoli. Vietato.

**Quando il checkpoint NON serve:** operazione singola (1 articolo / 1 file / 1 fix mirato), operazione già autorizzata in dettaglio nel turno precedente con parametri concreti, build/test/audit read-only.

Specifiche complete: `.claude/rules/07-proattivita-coerenza.md` § "Checkpoint pre-operazione batch".

### 3.2 "Pubblica" significa portare in produzione FINO ALLA FINE — niente fermate

🔴 **Quando l'utente dice una di queste cose, vai fino al sito live senza fermarti, senza chiedere, senza spiegare lo stato a metà strada.**

**Parole-trigger (lista non esaustiva, riconosci anche varianti italiane equivalenti):**

- **Comandi diretti:** «pubblica», «pubblicalo», «pubblicale», «pubblica le modifiche», «mandala live», «mandalo live», «mettila su», «mettilo su», «metti online», «manda in produzione», «porta live».
- **Comandi informali:** «vai», «procedi», «fai», «fallo», «forza», «dai», «manda».
- **Comandi rinforzati che obbligano a non fermarsi:** «vai fino alla fine», «prosegui fino alla fine», «porta a termine», «non fermarti», «fai tutto», «completa», «chiudi tutto».
- **Conferme dopo una proposta tua nel turno precedente:** «sì», «ok», «conferma», «d'accordo», «procedi pure» (sono trigger SE nel turno precedente hai chiesto cose tipo «Vuoi che apra PR + merge + verifica deploy?»).

**Sequenza completa, da eseguire senza interruzioni:**

1. `git add` + `git commit` (se serve) sul branch di lavoro
2. `git push` sul branch
3. Apri PR verso `main`
4. **Mergia la PR su `main`** (squash, default)
5. Verifica che `deploy.yml` sia partito (Actions tab)
6. Comunica URL della PR mergiata + ETA del deploy (~2-3 minuti)

**🚫 VIETATO:**

- ❌ «PR aperta, attendo conferma per il merge». **NO**: il merge fa parte di «pubblica», l'utente ha già autorizzato.
- ❌ «Branch avanti di N commit, vuoi che proceda?» dopo un comando di pubblicazione. **NO**: l'utente ha già detto vai.
- ❌ Fermarsi a metà ("PR aperta, ora aspetto") quando il comando era «pubblica» o «vai». **NO**: si va fino in fondo, fino al merge + deploy verificato.
- ❌ Interpretare «pubblica» come «aggiorna il branch». **NO**: solo `main` è live, il push sul branch da solo non pubblica nulla.
- ❌ Chiedere all'utente di fare lui il merge. **NO**: lo fai tu.

**Eccezione unica — build rotta:** se rilevi errori certi (Hugo build fallisce, file corrotto, sintassi YAML invalida) **fermati prima del merge**, segnala il blocker, fixa, riparti. Ma se la build è pulita e le rules sono rispettate, vai diritto fino al merge senza chiedere.

#### Domande di stato sulla pubblicazione → SEMPRE offerta esplicita

Se l'utente ti chiede una **domanda di stato** sulla pubblicazione mentre ci sono commit pendenti — *«Pubblicate?»*, *«Hai pubblicato?»*, *«È live?»*, *«Va in produzione?»*, *«Sono già su main?»*, *«Si vede online?»* — e la risposta onesta è **NO** (sono solo sul branch, non ancora mergiate), **devi sempre chiudere la stessa risposta con un'offerta operativa esplicita:**

> *"Sul branch ci sono N commit non ancora live. Vuoi che apra PR + merge su main + verifica deploy?"*

**Non lasciare l'utente a doverlo chiedere come azione successiva.** Se l'utente risponde «vai» / «sì» / «ok» / «procedi», quella è una conferma di pubblicazione e attiva la sequenza completa della sezione 3.2 (commit → push → PR → merge → deploy → comunica URL+ETA), senza altre fermate.

Esempio corretto:

> ❓ Utente: «Pubblicate?»
> ✅ Tu: «No, non ancora. Sul branch `chatgpt/...` ci sono 7 commit avanti rispetto a `main` (lista). Per pubblicarle serve merge su main + deploy. **Vuoi che proceda?**»
> ❓ Utente: «Vai»
> ✅ Tu: *(esegui PR + merge + verifica + comunichi URL e ETA, senza altre domande)*

Esempio sbagliato (vietato):

> ❓ Utente: «Pubblicate?»
> ❌ Tu: «No, non ancora pubblicate. Sono sul branch ... non ancora in main, ... per pubblicarle serve fare merge su main e poi far partire il deploy del sito.» *(spieghi lo stato ma non offri di farlo)*
> ❓ Utente: «Vai»
> ❌ Tu: *(non agisci perché «vai» da solo, senza una proposta tua sospesa, ti lascia incerto sull'oggetto del comando)*

**Storia della regola:** esiste perché il 2 maggio 2026 un agent si è fermato alla creazione della PR aspettando conferma — l'utente ha chiarito: «quando ti dico di pubblicare, devi fare in modo e maniera di pubblicare!». Il 9 maggio 2026 ChatGPT-cloud ha replicato lo stesso bug nonostante la regola in questo file: ha spiegato lo stato del branch *senza offrire l'azione*, poi non ha riconosciuto «Vai» come trigger. La sezione è stata riscritta per rendere impossibile fraintenderla.

### 3.3 Fine sessione su feature branch — proponi sempre il merge

L'utente lavora **multi-device** (PC desktop, smartphone Android, agenti GitHub-integrati). Le sessioni AI **non hanno memoria condivisa**: l'unica memoria persistente è git.

**Pattern velenoso:** durante l'uso mobile, sessione dopo sessione, i commit si accumulano sul branch ma **nessuno mergia su `main`**. A maggio 2026 si sono accumulati 50+ commit pendenti — l'utente convinto fosse pubblicato, invece no.

**Regola operativa — fine di ogni sessione che ha fatto commit:**

1. Esegui `git log --oneline origin/main..HEAD` per vedere cosa è pendente.
2. Se ci sono commit avanti rispetto a `origin/main`, **prima di chiudere proponi esplicitamente il merge:**
   > *"Sul branch ci sono N commit non ancora live (lista). Vuoi che apra PR + merge su main + verifica deploy?"*
3. Se l'utente conferma → apri PR, mergia (squash), verifica `deploy.yml`, comunica URL + ETA.
4. Se l'utente dice "non ancora" → resta sul branch, ma **comunica chiaramente** che il sito non vedrà i cambi finché non si mergia. Niente "pubblicato" ambiguo.

**Cosa NON fare:**
- Non auto-mergiare senza chiedere quando l'utente non ha detto "pubblica".
- Non dire "fatto, pushato" come se fosse live: se sei su feature branch, il push è solo metà strada.

---

## 4. Le 16 invarianti del progetto (sintesi da CLAUDE.md)

Ognuna è elaborata per esteso in `CLAUDE.md` sezione "Regole contenuti e qualità". Qui solo i punti operativi.

1. **Formato data nel frontmatter:** `AAAA-MM-GG` semplice se 1 articolo/giorno; `AAAA-MM-GGTHH:MM:SS+02:00` con orari crescenti `00:01, 00:02, …` se 2+ articoli/giorno (mai `Z` UTC, sempre `+02:00`). Tie-break Hugo `Date desc` su date uguali = ordine alfabetico filename, non ordine pubblicazione → orari minimi risolvono. Fix retroattivo: `python3 scripts/fix-ordering-articoli-stesso-giorno.py`.

2. **Conformità AGID:** Bootstrap Italia + WCAG 2.2 AA + struttura AGID. Niente eccezioni "estetiche".

3. **Qualità testi:** italiano corretto, AGID-compliant, frasi brevi (<20 parole), voce attiva, niente burocratese, accessibile, inclusivo. Riscrivi il testo dell'utente se non rispetta.

4. **Verifica:** ortografia + grammatica + AGID prima di ogni pubblicazione.

5. **Aggiornamento:** linee guida AGID cambiano. Verifica designers.italia.it periodicamente.

6. **Manuale di stile:** `MANUALE-SITO.md` (indice) + `manuale/parte-NN-*.md` (split). Riferimento unico per la redazione.

7. **Immagini di copertina:** fascia blu `#003366` con logo + testo istituzionale. WebP, 1200px, ≤200 KB. Specifiche in `manuale/parte-03-immagini-per-gli-articoli.md`.

8. **Piano editoriale:** `PIANO-EDITORIALE.md`. Tendere a 1 articolo/giorno, minimo 3-4/settimana.

9. **🔴 BANNER COL TITOLO INTOCCABILE — qualunque sia la fonte della foto:**
   - Il campo `image:` del frontmatter deve **SEMPRE** puntare alla **cover tipografica con titolo** (gradiente blu + titolo + badge + fascia istituzionale, generata da `scripts/genera-cover.py` o `scripts/auto-cover-mancanti.py`).
   - **TUTTE** le foto fornite dall'utente o scaricate da Wikipedia/NASA/USGS/NOAA/Pexels/Pixabay/Unsplash vanno **inline nel corpo dell'articolo** con lo shortcode `{{< foto >}}`, **MAI** nel banner.
   - Convenzione foto multiple in articoli storici: 1ª dopo 1° H2, 2ª dopo 2° H2, foto successive sull'H2 di ogni evento specifico citato. ≥4 foto → galleria/carosello dentro l'articolo.
   - **Sui social** lo script `genera-immagini-social.py` legge le foto inline `{{< foto >}}` dal body e le combina automaticamente in carosello Instagram. Stessa fonte, due usi distinti.
   - **🚫 DIVIETO ASSOLUTO — marker `# TODO-foto-*` BANDITO** (dal 3 maggio 2026): non scriverlo mai nel frontmatter né nel corpo. Il workflow `scarica-foto-automatica.yml` lo elaborava sovrascrivendo `image:` (viola questa regola) e Hugo lo renderizzava come `<h1>` se il deploy partiva prima del workflow. Per inserire foto da fonti ufficiali usa: WebFetch su pagina Wikipedia/NASA/USGS → `curl -sL <URL> -o /tmp/foto.jpg` → `bash scripts/applica-fascia-foto.sh /tmp/foto.jpg <nome-output-DIVERSO-dallo-slug>` → shortcode `{{< foto >}}` inline + caption con credit.

10. **Stampa:** regole `@media print` globali in `themes/flavour-pcgenzano/static/css/custom.css`. Non duplicare. Non rompere.

11. **Pagine legali:** `privacy`, `note-legali`, `accessibilita`, `social-media-policy` hanno frontmatter `dataUltimaRevisione: "AAAA-MM-GG"`. Aggiorna quando cambi contenuto sostanziale. Mai stringhe tipo "Marzo 2026" nel corpo.

12. **Comunicazione di crisi — gerarchia delle fonti:**
    - **L1 italiano vincolante:** AGID + DPC. Su contenuto PC, **DPC prevale su AGID**.
    - **L2 scientifico italiano:** CNR (IRPI/INGV/IGAG) + ISPRA.
    - **L3 europeo:** EENA + CWA CEN/CENELEC.
    - **L4 standard internazionali:** ISO 22329:2021 + WCAG 2.2 AA.
    - **L5 normativa orizzontale:** DL 25/2025 (SMM PA), GDPR, L. 4/2004 (Stanca), CAD.

    Struttura standard post crisi (6 punti): tipo / livello-colore / area+tempo / cosa fare / fonte / prossimo aggiornamento. Hashtag stabili: `#PCGenzano`, `#Genzano`, `#AllertaLazio`, `#NUE112`. Mai amplificare la disinformazione per smentirla.

13. **`riferimenti-interni/`** (root, NON deployata): documentazione di lavoro per maintainer/AI di supporto (norme copyrighted, draft di consultazione). Hugo non la legge. Convenzione: 🟢 documenti pubblici → `static/manuali/`, 💶 copyrighted/riservati → `riferimenti-interni/<categoria>/`.

14. **Sandbox Claude Code per fonti immagini libere:** configurazione in `.claude/settings.local.json` (in `.gitignore`, locale). Schema completo in `.claude/rules/08-claude-code-setup.md`. Non rilevante se operi via ChatGPT/Codex (girano su infrastruttura OpenAI con rete libera).

15. **Dati allerta meteo `data/allerta.json`:** due campi temporali distinti. `ultimo_aggiornamento` cambia **solo** quando il livello DPC cambia. `ultimo_controllo` cambia ogni volta che il workflow `check-allerta.yml` verifica. Schema in `manuale/parte-09-file-dati-data-e-stati-del-sito.md` § 9.3.

16. **Kit Calamità (12 kit A4 stampabili):** `/formazione/kit-calamita/` — bambini, anziani, RSA, disabilità adulti, neonati, gravidanza, animali, caregiver, terapie salvavita, senza fissa dimora, italiano L2, volontari PC. **Quando aggiungi un nuovo kit aggiorna 4 punti di accesso:**
   - `_index.md` Hugo del kit
   - hub `/formazione/kit-calamita/`
   - `content/mappa-sito/_index.md` (card colorata)
   - assistente virtuale `themes/flavour-pcgenzano/layouts/assistente/list.html` (sotto-albero `kc_*`)

   Carte d'identità compilabili: template uniforme `.carta-id-*` in `static/formazione/kit-calamita-shared/print.css` (riga scrittura **11mm**, mai 6mm). Giochi (cruciverba, sudoku) → soluzione ruotata 180° in fondo alla stessa scheda (classe `.soluzione-capovolta`). Mai paradigma `<details>` + foglio operatore separato.

---

## 5. Convenzioni Hugo critiche

### 5.1 Frontmatter articoli `comunicazioni/`

```yaml
title: "Titolo chiaro e informativo"
date: 2026-05-06           # AAAA-MM-GG (caso 1 articolo/giorno)
description: "Sommario ≤160 caratteri, utile anche per SEO"
badge: "Comunicazione"      # vedi palette sotto
priorita: "normale"         # normale | urgente
autore: "Gruppo Comunale Volontari PC Genzano"
image: ""                   # vuoto → cover tipografica generata in CI
scadenza: ""                # data o vuoto
area: ""                    # zona geografica o vuoto
allegati: []                # array di {titolo, url, dimensione}
draft: false                # niente draft:true sul sito
```

### 5.2 Palette badge ufficiali (contrasto WCAG AA ≥4.5:1 su bianco)

| Categoria | Hex | Uso |
|---|---|---|
| Allerta | `#d9364f` | **PREVISIONE** — evento previsto, non ancora in corso |
| Emergenza | `#7f1d1d` | **EVENTO IN CORSO** — solo per attivazione COC, evacuazione, intervento attivo (badge raro) |
| Avviso | `#b45309` | Segnalazione operativa non urgente |
| Evento | `#c026d3` | Iniziativa pubblica |
| Comunicazione | `#003366` | Informazione ordinaria (default) |
| Radiocomunicazioni | `#0369a1` | HF/VHF/UHF |
| Informazione | `#0284c7` | Notizia di servizio |
| Prevenzione | `#15803d` | Auto-protezione |
| Esercitazione | `#ea580c` | Addestramento operativo |
| Aggiornamento | `#4338ca` | Stato avanzamento / esito operazione conclusa |
| Formazione | `#7c3aed` | Corsi e didattica |
| Volontariato | `#b45309` | Reclutamento e attività volontari |
| Attività | `#0891b2` | Operatività ordinaria |

**Criterio Allerta vs Emergenza:** se l'evento è già iniziato per il cittadino e richiede un'azione immediata = `Emergenza`; se è ancora previsione = `Allerta`. Dopo la conclusione = `Aggiornamento`. Specifiche in `.claude/rules/06-protezione-civile-scientifica.md` § "Quando usare il badge 'Allerta' e quando 'Emergenza'".

### 5.3 Foto inline nel corpo (mai nel banner)

```markdown
{{< foto src="/images/2026-05-06-descrizione-specifica.webp"
         alt="Descrizione significativa per screen reader"
         caption="Didascalia opzionale con credit + licenza." >}}
```

Regole rigide:
- Nome file foto **diverso dallo slug** dell'articolo (così `genera-cover.py` non sovrascrive).
- Fascia blu istituzionale obbligatoria → `bash scripts/applica-fascia-foto.sh <sorgente> <nome-output-senza-ext>`.
- Mai `![]()` markdown diretto. Sempre shortcode.
- Mai foto stock generiche ripetute su gruppi di articoli per macro-tema (vedi rule 02 § "Divieto: foto stock generiche ripetute per macro-tema").

### 5.4 Pittogrammi

ISO 7010 (segnali di sicurezza ufficiali) e ARASAAC (concetti narrativi/didattici, CC BY-NC-SA). Shortcode:

```markdown
{{< pittogramma src="/pittogrammi/arasaac/terremoto.png"
                alt="Pittogramma: terremoto"
                caption="Cosa fare in caso di terremoto" >}}
```

Inline: aggiungi `inline="true"`. Dimensione: `size="small|medium|large|xlarge"`. Attribuzione ARASAAC obbligatoria su pagina `/attribuzioni-pittogrammi/` (già linkata dal footer).

### 5.5 Niente conteggi inventario sul sito

Decisione editoriale di maggio 2026: il sito **non riporta numeri di inventario** (schede, giochi, storie, kit, pittogrammi, fac-simile). Descrizioni qualitative ("schede stampabili per tutte le fasce", "giochi educativi divisi per fascia di età"), non quantitative. **Cosa NON va toccato:** numeri citazionali di documenti esterni ("Codice PC 50 articoli", "scala EMS-98 5 livelli"), strutture normative ("le 4 attività della PC"), date, telefoni, formati file.

---

## 6. Comandi utili

```bash
# Dev server locale
hugo server                           # solo pubblicati
hugo server -D                        # anche bozze

# Build
hugo --minify                                                            # GitHub Pages
hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"        # Aruba

# Pubblicazione
git add . && git commit -m "..." && git push

# Export contesto completo per altre AI
bash scripts/export-contesto-ai.sh    # produce CONTESTO-AI.md

# Applica fascia blu istituzionale a una foto
bash scripts/applica-fascia-foto.sh <file-sorgente> <nome-output-senza-ext>

# Pittogrammi (libreria ISO 7010 + ARASAAC)
bash scripts/scarica-pittogrammi.sh           # solo i mancanti
bash scripts/scarica-pittogrammi.sh --force   # ri-scarica tutto

# Genera bozze social (richiede GEMINI_API_KEY)
bash scripts/genera-social.sh content/comunicazioni/<file>.md
bash scripts/genera-social.sh --all
bash scripts/genera-social.sh --since 2026-04-01

# Cover tipografiche per articoli con image:""
python3 scripts/auto-cover-mancanti.py            # genera + popola frontmatter
python3 scripts/auto-cover-mancanti.py --dry-run  # solo anteprima

# Fix ordering articoli stesso giorno
python3 scripts/fix-ordering-articoli-stesso-giorno.py
```

---

## 7. Agenti specializzati esistenti (riferimento)

In `.claude/agents/` ci sono 5 agenti custom ottimizzati per Claude Code. **ChatGPT/Codex ha il suo sistema di sub-agenti diverso** e non li può richiamare direttamente, ma può **emulare il loro lavoro** seguendo le specifiche descritte qui sotto. Le specifiche complete sono in `manuale/parte-19-agenti-specializzati.md`.

| Agent | Trigger naturali | Cosa fa |
|---|---|---|
| `pc-article-reviewer` | "rivedi questo articolo", "controlla il frontmatter", "va bene per pubblicare?" | Verifica frontmatter completo, applica regole AGID, controlla badge correttezza, formato data, link interni validi, convenzioni foto, assenza dati fittizi. Restituisce punch list di issue da fixare PRIMA del commit |
| `pc-image-fixer` | "ecco una foto", "queste immagini", "mettila nell'articolo", "applica fascia blu" | Applica fascia blu istituzionale, ridimensiona a 1200px, converte WebP ≤200 KB, posiziona foto inline con `{{< foto >}}` (mai nel banner), genera cover tipografica se serve |
| `pc-issue-triage` | "controlla le issue", "fai pulizia tracker", "issue da chiudere?" | Audita stato issue aperte rispetto alla realtà del repo, distingue issue obsolete da reali, propone batch close + commit con commenti esplicativi |
| `pc-deploy-validator` | "verifica prima del push", "controlla il deploy", "build OK?", "pubblico in sicurezza?" | Pre-push gate completo: build Hugo pulito, sanity JS/CSS, sweep broken-link, validazione frontmatter articoli modificati, regression header sicurezza, GDPR sweep, compliance rules. Restituisce GO/NO-GO con blocker espliciti vs warning |
| `pc-social-publisher` | "rivedi le bozze social", "pronti per pubblicare?", "controlla immagini Instagram" | Rivede tono, accessibilità, hashtag, struttura crisi-comunicazione (ISO 22329 + CWA CEN/CENELEC), valida immagini Instagram per specs IG. Mai pubblica sui social — quello tocca all'umano |

Quando l'utente fa una richiesta che corrisponde al trigger di uno di questi agenti, **applica i criteri descritti** anche se non puoi richiamare il sub-agent specifico.

---

## 8. Operazioni Git/GitHub (vincoli specifici)

- **Branch di sviluppo:** se un agente OpenAI ti viene assegnato un branch specifico (es. `claude/...`, `chatgpt/...`, `codex/...`), lavora **solo** su quello. Non pushare su `main` salvo merge esplicito post-PR.
- **Commit message style:** italiano, descrittivo, ≤72 caratteri sulla prima riga, body opzionale. Esempi nei commit recenti: `git log --oneline -20`.
- **Mai committare segreti:** `.env`, credenziali, token. I secret FTP Aruba e GEMINI_API_KEY stanno nei GitHub Secrets, non nel codice.
- **PR template:** nel body riassumi cosa cambia + perché + eventuali migration step. Niente CI badge inventati.
- **Pre-push validation:**
  - `hugo --minify` deve completare senza errori.
  - YAML workflow modificati: `python3 -c "import yaml; yaml.safe_load(open('.github/workflows/<file>.yml'))"`.
  - Frontmatter articoli: nessun `draft: true` in produzione, formato data corretto, nessun marker `# TODO-foto-*`.
- **Mai `git push --force` su `main`.** Su feature branch ok solo se sai cosa stai facendo.
- **Hook pre-commit:** rispetta i hook esistenti, non bypassare con `--no-verify`.

---

## 9. Workflow CI/CD (riferimento)

Tutti i workflow di manutenzione girano **lunedì** scaglionati. Lista in `CLAUDE.md` § "Automazioni periodiche". I principali:

- `deploy.yml` — ogni push su `main` → build + deploy Aruba (FTP) + GitHub Pages
- `pubblica-programmata.yml` — giornaliero 06:00 UTC → rilancia deploy per articoli con `date` futura passata
- `audit-sito.yml` — lunedì 09:00 UTC → audit completo (contenuti + codice + governance docs + accessibilità)
- `check-links-sito.yml` — lunedì 10:00 UTC → crawl lychee
- `genera-social-bozze.yml` — ogni push articolo → bozze social (X/FB/IG/Telegram) via Gemini API
- `scarica-foto-automatica.yml` — ogni push: step 1 deprecato (marker bandito), step 2 attivo (`auto-cover-mancanti.py`)
- `smoke-test-post-deploy.yml` + `lighthouse-audit.yml` — post-deploy

---

## 10. Cosa NON fare mai

Sintesi dei divieti dalle rules:

- ❌ Toccare il banner col titolo (rule CLAUDE.md punto 9).
- ❌ Scrivere marker `# TODO-foto-*` (bandito dal 3 maggio 2026).
- ❌ Foto stock generiche ripetute per macro-tema (incidente aprile 2026: stessa foto su 74 articoli).
- ❌ Pubblicare articoli con `draft: true`.
- ❌ Numeri inventario sul sito (decisione maggio 2026).
- ❌ Cambiare `Permissions-Policy: geolocation=(self)` in `()` su `.htaccess` (rompe la mappa cartografia).
- ❌ Citare 115/118/1515 come numeri di emergenza nel Lazio: solo **112** (NUE).
- ❌ Tipo Schema.org `GovernmentOrganization` o `EmergencyService` (siamo OdV, non ente pubblico).
- ❌ Overlay commerciali di accessibilità (AccessiBe, UserWay, EquallyAI): il W3C-WAI li sconsiglia.
- ❌ Push diretto su `main` senza PR + merge esplicito.
- ❌ `gh pr merge` automatico fuori dai casi previsti (regola 3.2 sopra).
- ❌ Linguaggio enfatico, commerciale, allarmistico, vago.
- ❌ Tabelle per layout, immagini senza alt, `draft: true` in produzione.

---

## 11. Riferimenti dettagliati (`.claude/rules/`)

Quando devi applicare una regola di dettaglio, leggi la fonte primaria. Ognuno di questi file è caricato come istruzione permanente per Claude Code; per ChatGPT/Codex va letto su richiesta.

- `01-governance-pa.md` — fonti AGID/Designers Italia, ordine priorità, divieti
- `02-content-design-pa.md` — scrittura, struttura, lessico, frontmatter, foto, pittogrammi, formato data, palette badge, comunicazione crisi
- `03-accessibility.md` — WCAG 2.2 AA, pittogrammi, toolbar a11y, TTS, sillabazione, glossario inline, coach giochi, social a11y, tabelle accessibili
- `04-hugo-architecture.md` — mappa generale (rimanda a 04a/b/c)
- `04a-hugo-shortcode-partial.md` — shortcode (`foto`, `pittogramma`, `cosa-non-fare`, `chi-chiamare`, `pagina-emergenza-lite`), render hook, partial
- `04b-hugo-template-css.md` — menu mega-menu, TOC, tipografia `.article-body`, stampa, toolbar a11y, bozze social, 404, homepage enhancements
- `04c-hugo-static-cartelle.md` — cartelle `static/` canoniche, `riferimenti-interni/` non deployata
- `05-github-aruba-deploy.md` — deploy FTP, esclusioni, header `.htaccess`, workflow YAML, cover automatiche
- `06-protezione-civile-scientifica.md` — fonti gerarchiche, badge Allerta vs Emergenza, codici colore, struttura pagine rischio, numeri emergenza
- `07-proattivita-coerenza.md` — checkpoint pre-batch, verifica pattern simili, casi storici
- `08-claude-code-setup.md` — sandbox `.claude/settings.local.json` (specifico Claude Code, non rilevante per ChatGPT)

Documentazione aggiuntiva nella root:
- `MANUALE-SITO.md` (indice) + `manuale/parte-NN-*.md` (split operativo)
- `MANUALE-MOBILE.md` (workflow editoriale da mobile/cloud)
- `PIANO-EDITORIALE.md` (fonti ufficiali + calendario)
- `README.md` (overview pubblica)
- `CONTESTO-AI.md` (export auto-generato per altre AI)

---

## 12. Note operative ChatGPT-specific

Queste note nascono per evitare attriti tipici quando ChatGPT/Codex opera su questo repo:

- **Non duplicare CLAUDE.md.** Quel file è autoritativo per Claude Code; AGENTS.md è autoritativo per te. Se trovi divergenze, segnalale all'utente — non risolverle in autonomia.
- **Custom GPT con knowledge file:** se l'utente ha configurato un Custom GPT redattore con `CONTESTO-AI.md` come knowledge, ricordagli che `CONTESTO-AI.md` va rigenerato periodicamente con `bash scripts/export-contesto-ai.sh` per restare allineato col repo.
- **GitHub Connector / Codex agent mode:** quando operi via integrazione GitHub di OpenAI hai accesso al repo come questa sessione Claude. Si applicano gli stessi vincoli sui branch (vedi sezione 8) e sui merge.
- **Code Interpreter:** utile per analisi dati che NON modificano il repo (es. stats sui badge, distribuzione articoli per mese, trend). Per modifiche al repo usa l'integrazione GitHub, non Code Interpreter.
- **Vision:** quando l'utente carica foto da inserire in un articolo, applica i criteri di `pc-image-fixer` (fascia blu, WebP 1200px ≤200 KB, alt text WCAG, foto inline mai nel banner). Se non puoi eseguire `applica-fascia-foto.sh` direttamente, descrivi all'utente il comando esatto da lanciare in locale.
- **Citazioni normative:** GPT-4/o1/o3 è notoriamente soggetto ad allucinare articoli di legge. **Non citare D.Lgs., articoli AGID, codici colore Lazio senza verificare.** Se non sei sicuro, di' all'utente "verifica questa citazione" invece di inventare.
- **Lingua:** sempre italiano. Anche commit message, anche commenti, anche output di tool. L'utente preferisce richieste in italiano naturale, non con i nomi tecnici degli agent.
- **Niente emoji decorative.** Sobrietà istituzionale. Le emoji nei file di codice sono ammesse solo se richieste esplicitamente o se sono parte del contenuto editoriale (es. coach giochi, kit didattici).

---

## 13. Domande frequenti per l'agente

**D. Posso modificare CLAUDE.md?**
R. Sì, ma sappi che è il "gemello autoritativo" di questo file per Claude Code. Se cambi un'invariante in CLAUDE.md, aggiornala anche qui (e viceversa) per mantenere allineamento. L'utente vede entrambi.

**D. Posso creare un nuovo file di rules in `.claude/rules/`?**
R. Sì se serve, ma aggiungi anche la riga corrispondente in `CLAUDE.md` (sezione "Regole di dettaglio") e un riferimento qui in AGENTS.md sezione 11. Sono regole permanenti, devono essere scoperte automaticamente.

**D. Posso aggiungere un nuovo agente in `.claude/agents/`?**
R. Sì. Aggiorna anche la tabella in `CLAUDE.md` § "Agenti specializzati disponibili", la tabella qui in sezione 7, e `manuale/parte-19-agenti-specializzati.md`.

**D. Come gestisco una richiesta che richiede operazioni batch?**
R. Applica il checkpoint pre-batch (sezione 3.1). Senza eccezioni, anche se ti sembra ovvio.

**D. L'utente mi ha detto «pubblica» ma sono su feature branch.**
R. Applica il flusso pubblica completo (sezione 3.2): commit → push → PR → merge → verifica deploy → comunica URL+ETA. Senza fermarti per conferme intermedie. Se ti fermi alla creazione della PR aspettando conferma per il merge, hai violato la regola.

**D. L'utente mi ha detto «vai» o «procedi» ma non ricordo se è un comando di pubblicazione.**
R. Se nel turno precedente hai proposto «Vuoi che apra PR + merge + verifica deploy?» o simile, allora «vai»/«sì»/«ok»/«procedi» sono conferme valide e attivano la sequenza completa di sezione 3.2. Se invece il contesto è ambiguo (es. l'utente non ti ha chiesto nulla di specifico sulla pubblicazione), chiedi *cosa* vuole che continui — ma **se ci sono commit pendenti sul branch e l'utente sembra spazientito**, l'interpretazione di default è: vuole che pubblichi.

**D. L'utente mi chiede «Pubblicate?» / «Hai pubblicato?» / «È live?» e la risposta è no.**
R. Non limitarti a spiegare lo stato. **Chiudi sempre la stessa risposta con un'offerta operativa esplicita:** *"Sul branch ci sono N commit non ancora live. Vuoi che apra PR + merge su main + verifica deploy?"*. Se l'utente risponde sì/vai/ok, esegui la sequenza completa di sezione 3.2 senza altre fermate. Vedi sezione 3.2 § "Domande di stato sulla pubblicazione".

**D. L'utente sta chiudendo la sessione e ho commit pendenti sul branch.**
R. Applica la regola "Fine sessione su feature branch" (sezione 3.3): proponi merge esplicito prima di chiudere.

**D. Trovo un drift tra documentazione e codice (es. il manuale dice X, il codice fa Y).**
R. Segnalalo all'utente. Non risolverlo autonomamente: la decisione su quale dei due è la verità è editoriale, non tecnica.

---

**Versione:** 1.1 — creato il 2026-05-06.
**Ultima revisione:** 2026-05-09 — sezione 3.2 riscritta dopo incidente ChatGPT-cloud del 9 maggio: parole-trigger ampliate (informali + rinforzate + conferme), nuova sotto-sezione «Domande di stato sulla pubblicazione», nuove FAQ.
**Autorità:** allineato a `CLAUDE.md` v3.0 e a `.claude/rules/0*.md` (snapshot maggio 2026).
**Manutenzione:** quando modifichi `CLAUDE.md` aggiorna anche questo file, e viceversa.
