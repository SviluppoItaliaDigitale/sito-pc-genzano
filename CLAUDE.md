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

1. **Banner col titolo, generato LOCALMENTE prima del commit.** Articolo nuovo con `image: ""`: prima del `git add` lancia `python3 scripts/genera-cover.py <file>`, Read della cover `static/images/<slug>.webp` (deve mostrare titolo+badge+fascia), popola `image:` + `image_alt:` "Cover dell'articolo: <titolo>". Non affidarsi al workflow CI `scarica-foto-automatica.yml` (gira dopo `deploy.yml`). **Rete di sicurezza deterministica (dal 04/06/2026):** `deploy.yml` esegue `scripts/auto-cover-mancanti.py` come step **pre-build** (accanto a QR/Braille), quindi un articolo con `image: ""` non può più andare live col banner SVG di default — ma resta tua responsabilità generare e Read la cover prima del commit (il pre-build è fail-safe, non una scusa per saltare lo step).
2. **Read di OGNI foto utente prima di scrivere caption/alt.** Read multimodale = vedi l'immagine. Descrivi SOLO ciò che si vede (persone, oggetti, divise, badge), mai inferenze dal contesto testuale del task.
3. **Attribuzione default = "Foto: Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma".** Mai a terzi (FEPIVOL/Comune/DPC) solo perché nel task ci sono loro testi. Eccezioni con evidenza certa: pattern nome file social terzi, Wikimedia/NASA/USGS/NOAA via `pc-image-fixer`, foto storiche con autore noto.
4. **Web check obbligato di OGNI entità citata** (associazione/ente/persona/sigla): WebFetch con denominazione tra virgolette. Se 0 risultati ed è associazione locale poco indicizzata, **non sciogliere l'acronimo a indovinare** (es. *"V.E.R. Formia"*, non *"E.R. Formia"*): cita la sigla come la leggi nella fonte.

**Gate pre-commit con foto utente:** cover+`image:` ✓ · Read di tutte le foto ✓ · caption solo visibile ✓ · attribuzione Gruppo ✓ · web check entità ✓ · **nome mezzo/attrezzatura verificato in `content/chi-siamo/_index.md` § "I nostri mezzi"** (la livrea sul fianco non è il modello del veicolo — dettagli in rule 02 § "Nomi dei nostri mezzi") ✓ · gate AGID `pc-article-reviewer` ✓. Un solo punto non verificato → **non committare**.

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

## Verifica visiva pre-commit su markup HTML nelle pagine

🔴 **Quando modifichi/aggiungi markup HTML custom dentro `content/**/*.md`** (card Bootstrap, blocchi `<div>` con `d-flex`/grid, layout custom, immagini in box affiancati), **`hugo --quiet --minify` NON BASTA**: la build può essere pulita mentre il rendering visivo è rotto. Incidente del 27/05/2026: card affiliazioni con `<div class="d-flex"><img></div>` viste come immagini giganti che schiacciavano il testo affiancato a 5ch di larghezza, con parole a capo lettera per lettera ("schifo" segnalato dall'utente sul live).

**Procedura obbligatoria pre-commit** (5 passi):

1. `hugo server --port 1314 --bind 127.0.0.1 --logLevel error > /tmp/hugo-server.log 2>&1 &` in background
2. `mcp__playwright__browser_navigate` su `http://127.0.0.1:1314/sito-pc-genzano/<percorso-pagina>/` (nota: dev server usa subpath GitHub Pages)
3. `mcp__playwright__browser_take_screenshot` con `element` + `target=".<selettore>"` zoomato sul nuovo blocco
4. **Read del PNG** per verifica multimodale del rendering (vedi davvero come appare)
5. **Solo se il rendering è corretto** → `kill %1` + commit + push. Se sbagliato → fix CSS/markup + ripetere

**Eccezioni** (la verifica visiva non serve):

- Modifiche puramente Markdown standard (paragrafi, liste, link, blockquote, code, tabelle MD pipe).
- Modifiche a frontmatter, data files YAML/JSON, CSS già scoped a classe esistente che NON crea nuova struttura.
- Fix testuale che non cambia struttura DOM (refusi, datazione, link).
- Modifiche a template Hugo / partial che NON introducono nuovi pattern di layout (es. cambio testo, aggiunta classe utility a element esistente).

**Per markup HTML custom (card, grid, flex con img, sezioni inline) la verifica visiva è SEMPRE obbligatoria.** Anche se "sembra ovvio". Meglio 30 secondi di Playwright che 1 ora di figura barbina sul live.

---

## Affiliazioni e riconoscimenti europei — Quality Label ESC + codice obbligatorio

🔴 Il Gruppo è organizzazione accreditata dal **Corpo europeo di solidarietà** (European Solidarity Corps, ESC) della Commissione europea. **Vincolo cogente** ai sensi del **Regolamento (UE) 2021/888**: il logo Quality Label **deve essere mostrato sempre accompagnato dal codice di accreditamento dell'organizzazione**. Mai logo nudo.

- **Codice del Gruppo:** `E10435833` (sempre accanto al logo, in tutte le grafiche e i materiali di comunicazione).
- **Logo ufficiale UE:** `static/images/quality-label-esc.png` (PNG 400×400). Versione hi-res per stampa/deck in `static/images/logo-esc-quality-label-it.png` (4016×4016). Pacchetto ufficiale UE in `static/manuali/loghi-esc-italiano-pacchetto-ufficiale.zip` (PDF vettoriale + PNG).
- **Loghi affiliazione del Gruppo** = **2**, non 3: Quality Label ESC (+codice) e **SNPC Volontariato** (`static/images/logo-snpc-volontariato.png`). Il logo PC Genzano è la firma istituzionale del Gruppo (banner, header, schede): **non si conta tra le affiliazioni** per evitare duplicazione.

**Dove sono già esposti (non duplicare):**

| Superficie | Implementazione |
|---|---|
| Footer site-wide Hugo | `themes/flavour-pcgenzano/layouts/partials/footer.html` (blocco `.esc-quality-label`) |
| Footer pagine statiche | `static/app-shared/site-chrome.js` (stesso blocco iniettato JS) |
| Pagina `/chi-siamo/` | Sezione "Affiliazioni e riconoscimenti europei" con descrizione + codice + Reg. UE 2021/888 |
| Carosello social Instagram | Slide finale "Affiliazioni" via `crea_slide_affiliazioni()` in `scripts/genera-immagini-social.py` (E10435833 in colore accento) |
| Schede stampabili A4 | Banda piè pagina in stampa via `.scheda::after` in `static/formazione/kit-calamita-shared/print.css` (immagine `static/images/footer-print-affiliazioni.png`) |
| Deck di presentazione | Slide "Affiliazioni e riconoscimenti europei" in `scripts/genera-presentazione.py` |

**Cosa NON serve fare:**

- **Mai aggiungere i 2 loghi al banner cover degli articoli** (fascia blu col titolo). Il vincolo UE è già soddisfatto dal footer site-wide; aggiungerli al banner sovraffolla il titolo e rompe l'identità visiva.
- **Mai batch retroattivo** sulle ~577 immagini esistenti per aggiungere i loghi. La ricompressione WebP degrada la qualità senza valore aggiunto (i loghi sono già nel footer di ogni pagina che le mostra).
- **Mai modificare i pittogrammi ISO 7010 / ARASAAC** per aggiungere loghi: violerebbe le licenze d'uso terze.

**Cosa fare in nuove grafiche/slide future:** se la grafica include un blocco "affiliazioni / riconoscimenti", usare **sempre** i 3 loghi affiliazione insieme + codice `E10435833` ben leggibile accanto al Quality Label. Mai logo ESC senza codice. Mai aggiungere PC Genzano tra gli "affiliati" (è la firma).

**🔴 Composizione standard di ogni nuova grafica istituzionale = ESATTAMENTE 4 LOGHI, MAI DOPPIONI:**

1. **Firma PC Genzano** (logo del Gruppo) — nell'**header/banner/intestazione** della grafica (cover articoli, header schede A4, barra brand top slide social, prima pagina deck). Identità visiva del Gruppo.
2. **Quality Label ESC + codice E10435833** — nel **footer/blocco affiliazioni** della grafica. Mai logo nudo (vincolo cogente Reg. UE 2021/888).
3. **Coordinamento FEPIVOL** — nel **footer/blocco affiliazioni** insieme agli altri 2.
4. **SNPC Volontariato** — nel **footer/blocco affiliazioni** insieme agli altri 2.

**Regole di composizione, vietato deviare:**

- La firma (1) è sempre **separata** dalle affiliazioni (2-4): mai mescolare PC Genzano tra le card affiliazione (sarebbe doppione).
- **Mai inserire lo stesso logo due volte** nella stessa grafica.
- **Mai inserire un 5° logo** (PC Lazio, Comune, Croce Rossa, ANPAS, VVF, INGV, ecc.): quei loghi sono di enti coordinatori/operatori del Sistema PC e vanno citati nei contenuti testuali o nel footer site-wide del sito, MAI nella grafica istituzionale del Gruppo.

**Vale anche per grafiche realizzate con AI esterne** (ChatGPT, Gemini, Midjourney, Canva, Adobe Express, DALL-E, ecc.): includere sempre nel prompt la regola "esattamente 4 loghi, mai doppioni, mai 5° logo, ESC sempre con codice E10435833" + fornire i 4 file dal repo. Specifiche complete + pattern brief da incollare alle AI esterne in `.claude/rules/02-content-design-pa.md § "Composizione standard"` (auto-incluso in `CONTESTO-AI.md` rigenerato).

Le grafiche già aggiornate seguono questo schema: cover articoli, slide social, schede A4, deck, /chi-siamo/ § Affiliazioni. Footer site-wide del sito: blocco chrome del portale (non grafica isolata), ha 4 loghi con PC Lazio come ente territoriale al posto della firma PC Genzano (che è già nel banner top del sito, mai duplicato nel footer).

---

## Presentazione del sito (deck) — rigenerare a ogni cambiamento di struttura o dati

🟢 Esiste un **deck istituzionale di presentazione del portale**: `static/manuali/presentazione-struttura-sito.pdf` (+ `.pptx` editabile), generato da `scripts/genera-presentazione.py`, linkato dall'**Area Download** (`content/area-download/_index.md` § "Presentazione del sito").

🔴 **Regola precisa:** ogni volta che una **sezione/area del sito viene aggiunta, modificata o eliminata**, o quando cambiano **dati, contatti, fonti o standard** mostrati nel deck (es. menu, schede del cruscotto, recapiti, affiliazioni come FEPIVOL), **rigenera il deck e ripubblicalo nello stesso commit** della modifica. Il deck non deve mai restare disallineato dal sito.

**Come:** `python scripts/genera-presentazione.py` (serve un venv con `python-pptx pillow fonttools brotli` + **LibreOffice** per l'export PDF). Lo script ricava font-icone (Bootstrap Icons self-hostate), logo e contatti **dal repo**, produce PPTX+PDF in `static/manuali/`. Se aggiungi una sezione al sito, aggiungi la slide corrispondente nel generatore. Vincoli del deck: **nessun riferimento a strumenti automatici/IA**, logo + contatti reali, rischi mostrati come **copertura** (non dettaglio del singolo rischio), slide di autorevolezza con fonti/standard, agenda a pulsanti + navigazione (frecce + "torna all'agenda").

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
- **Data files** in `data/` — `emergenza.json`, `allerta.json`, `risk_cards.yaml`, `numeri_utili.yaml`, `quick_links.yaml`, `social_links.yaml`, `codici_colore.yaml`, `glossario.yaml`, `aree_emergenza.yaml`, `dae.yaml`, `idranti.yaml`, `stato-sistema.json`, `eventi_storici.yaml`, `lis.yaml`, `ecmwf_charts.json` (carte Meteo Europa), `meteo_genzano.json` (riquadro cartina Lazio). Open data del Laboratorio meteo in `static/open-data/clima-*.json`.
- **Badge articoli** (in `partials/badge.html`): Allerta · Avviso · Comunicazione · Attività · Formazione · Evento · Volontariato · Radiocomunicazioni · Prevenzione · Esercitazione · Aggiornamento · Informazione · Emergenza — palette/hex/contrasto in rule 02.
- **Shortcode:** `foto`, `pittogramma`, `cosa-non-fare`, `chi-chiamare`, `link-card`, `pagina-emergenza-lite`, `dashboard-*` (cruscotto), `scheda-terremoto` (scheda dettaglio evento sismico INGV su `/cruscotto/terremoto/#<id>`), e i **componenti Bootstrap Italia** `callout` (nativo BI), `passi` (stepper), `timeline`, `galleria` (carosello ≥4 foto). **Render hook:** `render-link.html`, `render-table.html`. **Partial** chiave: `article-cover`, `leggi-ad-alta-voce` (TTS), `indice-pagina` (indice + scrollspy site-wide), `accessibility-toolbar`, `assistente-fab`, `structured-data` (JSON-LD), `meta-social` (OG), `articoli-correlati`, `page-tools`, `sos-112`, `qr-articolo`, `ricerca-modal` (Pagefind Ctrl+K), `lis-badge`.
- **Pagine/feature speciali:** ricerca Pagefind (`/cerca/`), QR articolo (`static/qr/`), `/stato-sistema/`, `/podcast/` + `/articoli-da-ascoltare/`, `/storia/`, assistente vocale, `/lanterna/` (standalone), LIS `/lis/` (`data/lis.yaml`), "Approfondimenti video" (`genera-video-correlati.py`, gate pertinenza), notifiche allerta browser, quiz `/quiz-preparazione/`, hub `/giochi/`, `/open-data/`, `/audio-e-podcast/`, hub `/standard-iso/`, `/feed-rss/`, traduzioni (hreflang + `<html lang>` dinamico), pagina lite `/emergenza/` (44 KB), metodo editoriale/E-E-A-T (`static/llms.txt`), microtext (`genera-microtext.py`), **cruscotto** `/cruscotto/` (schede dati live INGV/meteo/radar/satellite/aria/mare/ECMWF), **scheda terremoto** `/cruscotto/terremoto/#<id>` (dettaglio di un singolo evento sismico da INGV FDSN, tab sul modello di terremoti.ingv.it, linkata da ogni riga del cruscotto sismico), **Laboratorio meteo** `/laboratorio-meteo/` (costruttore di grafici climatici ERA5/Open-Meteo live + esempi pre-cotti, `static/js/laboratorio-meteo.js`).
- **TTS Web Speech API** (pagine `tts:`, coach giochi, fiabe), **coach giochi**, **glossario inline** — rule 03.

## Regole contenuti e qualità (19 punti)

Elenco completo in rule `09-regole-contenuti-qualita.md`. Vincoli più critici:
- **P1 Formato data:** `AAAA-MM-GG` se 1 articolo/giorno; `AAAA-MM-GGTHH:MM:SS+02:00` con orari crescenti (00:01, 00:02…) se 2+/giorno. Mai `Z` UTC.
- **P4 Qualità ChatGPT 9.5/10:** redazione AGID in ogni contesto (CLI/mobile/cloud), nessuna delega ad AI esterne.
- **P9 Banner intoccabile:** `image:` = cover tipografica col titolo; tutte le foto **inline** con `{{< foto >}}`, mai nel banner; marker `# TODO-foto-*` bandito; in revisione testuale `image:` non si tocca.
- **P12 Gerarchia fonti crisi:** AGID+DPC → CNR/ISPRA → EENA/CWA → ISO 22329 + WCAG 2.2 AA → normativa orizzontale.

## Automazioni (GitHub Actions) e note operative

Tabella completa workflow + note operative in rule `10-automazioni-github-actions.md`. Trigger rapidi:
- `deploy.yml` a ogni push su `main`. **Priorità deploy (3 livelli, 31/05/2026):** allerta/`pubblica-programmata` immediati (`-f priority=urgent`), articoli (push merge) immediati e prioritari, aggiornamenti di sfondo (meteo/ECMWF/clima/video/stato/QR/pacchetti/indice) **coalescati** da `deploy-coalescer.yml` (1 deploy ogni ~30 min). Dettagli in rule 10 § "Modello di priorità del deploy".
- `aggiorna-manuale.yml` (lunedì 06:00 UTC): monitora le fonti AGID/Designers Italia/DPC e apre issue quando cambiano — manuale e `.claude/rules/` vanno aggiornati in coppia (rule 02 § "Sincronizzazione automatica con gli aggiornamenti AGID").
- Modalità emergenza: `data/emergenza.json` → `"attiva": true`.
- Allerta meteo manuale: `data/allerta.json` → `livello: verde|giallo|arancione|rosso`.
- Niente articoli `draft: true`: solo pubblicato (data passata) o calendarizzato (data futura).
