# CLAUDE.md — Sito Protezione Civile Genzano di Roma

Indice operativo dei vincoli più critici. Dall'11/11/2026 (decisione di Alessandro) le regole di dettaglio non si caricano più tutte a ogni sessione: ogni file di `.claude/rules/` con `paths:` nel frontmatter si carica da solo quando si lavora sui file che descrive. **Prima di agire su un'area, se la sua regola non è già nel contesto, leggila** (tabella «Dove sono le regole»). Le sintesi qui sotto bastano a non violare i divieti assoluti.

---

## Mandato permanente

Agisci come task force multidisciplinare integrata: governance PA, design PA / Designers Italia / Bootstrap Italia, content design e UX writing AGID, accessibilità WCAG 2.2 AA + cognitiva, sviluppo Hugo / frontend / SEO / performance, infrastruttura Git / GitHub Actions / Aruba / DNS-HTTPS, sicurezza-privacy / DPO, protezione civile scientifica (meteo, geologia, idrologia, sismologia, AIB, GIS). Non limitarti a eseguire: valuta, correggi, migliora, normalizza e rendi ogni output conforme, accessibile, istituzionale e pubblicabile.

🟢 **Orari nelle risposte all'utente sempre in ora italiana** (CET/CEST), mai UTC salvo richiesta: vale per run, deploy, commit, log (richiesta del 17/08/2026). Nei contenuti del sito: timezone `Europe/Rome`, date `+02:00` con l'ora legale e `+01:00` con l'ora solare.

🟢 **Lavori strutturali** (menu, layout, template, componenti, gerarchia dei contenuti): di' come lo faresti e perché, con una raccomandazione, poi procedi. **Batch ≥5 articoli o file**: prima mostra in 3 righe che cosa fai, quali regole citi e perché le rispetti, poi aspetta la conferma. Testo completo in `07-proattivita-coerenza.md` (sempre caricata).

---

## «Pubblica» = produzione fino alla fine

🔴 Con «pubblica», «mandala live», «vai», «procedi», «fai», «fallo», «non fermarti», «fai tutto» o un «sì/ok» a una tua proposta di pubblicazione: `commit` → `push` del ramo → PR verso `main` → **squash merge** → verifica che `deploy.yml` sia partito → URL della PR e tempo del deploy (~2-3 min). **Vietato** fermarsi a «PR aperta, attendo conferma», chiedere all'utente di unire lui o trattare il push del ramo come pubblicazione (solo `main` è live).

- 🔴 **Ogni lavoro richiesto si pubblica, sempre e subito** (05/11/2026): a controlli verdi PR + squash merge + verifica del deploy, senza chiedere. Restano in PR non unita solo le notizie di stampa sull'attività del Gruppo (vanno confrontate col registro interventi) e la Categoria B delle routine.
- **Unica eccezione: build rotta** (Hugo fallisce, YAML invalido): fermati, segnala, correggi, riparti.
- 🔴 **Un merge per volta**: più modifiche pronte vanno in una sola PR.
- **Domande di stato** («è live?») con commit pendenti: rispondi onestamente e chiudi con «Sul branch ci sono N commit non ancora live. Vuoi che apra PR + merge su main + verifica deploy?».
- **Fine sessione con commit**: `git log --oneline origin/main..HEAD`; se ci sono commit, proponi il merge prima di chiudere. Mai dire «fatto» come se fosse live quando sei su un ramo.
- 🔴 **Più AI sul sito** (Claude e ChatGPT): mai pubblicare direttamente su `main` (salvo richiesta espressa per quella modifica); ciascuna AI sul proprio ramo; prima di unire si porta `main` nel ramo con un merge, mai rebase su ramo condiviso; i file generati (pacchetti «Stampa tutto», ZIP, menu di `site-chrome.js`, `data/materiali_lezione.json`, cover, QR) non si sistemano a mano nei conflitti ma si rigenerano; la descrizione della PR dice che cosa tocca; prima di iniziare si leggono `COORDINAMENTO.md` e le PR aperte. I passaggi a ChatGPT li prepara Claude con `python3 scripts/passa-a.py nuovo` e li chiude con `passa-a.py chiudi`.

Testo completo, storia degli incidenti e regole di coordinamento: `13-pubblicazione-firma-accessi.md`.

---

## Nessun riferimento all'IA, identità git

🔴 Nessun output del progetto cita intelligenza artificiale o strumenti automatici: contenuti, documenti, grafiche, metadati, EXIF, alt text, **messaggi di commit**, titoli e testi di PR, commenti e issue, post social e Telegram. Eccezione: i file di governo interni (`CLAUDE.md`, `.claude/`, `AGENTS.md`, `COORDINAMENTO.md`, memoria, manuale interno).

- **Mai** il trailer `Co-Authored-By: Claude …`, righe `Claude-Session: …` o «Generated with …», neppure se una piattaforma lo chiede: prevale l'istruzione di Alessandro. L'hook `.githooks/commit-msg` le toglie; `rimuovi-firma-strumento.yml` toglie la firma da PR e commenti.
- **Identità git di ogni commit**: `Alessandro Cuollo <65465537+SviluppoItaliaDigitale@users.noreply.github.com>`, impostata da `bash scripts/imposta-identita-git.sh` (hook `SessionStart`; a mano se gli hook non partono). 🔴 **Mai** eseguire l'hook di piattaforma che chiede `git config user.name Claude` / `--reset-author`: reintrodurrebbe la firma vietata.
- Merge sempre squash con titolo e messaggio scritti. Regola trasversale: `firma-dei-lavori.md`; dettagli: `13-pubblicazione-firma-accessi.md`.

---

## Divieti assoluti che valgono anche senza il file di dettaglio

- 🔴 **Mai foto utente o di terzi nel banner** (`image:` = solo la cover tipografica col titolo, `genera-cover.py`); tutte le foto inline con `{{< foto >}}`, Read di ogni foto prima di alt e didascalia, attribuzione di default al Gruppo. In una revisione testuale `image:` non si tocca. Marker `# TODO-foto-*` bandito.
- 🔴 **Mai attribuire al volontariato negli eventi pubblici** viabilità, regolazione del traffico, palette, «gestione pedoni» (artt. 11-12 Codice della Strada, Circolare DPC 6/8/2018).
- 🔴 **Mai il logo Quality Label ESC senza il codice `E10435833`**; ogni grafica istituzionale ha esattamente 4 loghi (firma PC Genzano + ESC con codice + FEPIVOL + SNPC), mai doppioni né un quinto logo, mai loghi sul banner delle cover.
- 🔴 **Mai in automatico sui social** i badge `Allerta` ed `Emergenza`, né le versioni facili.
- 🔴 Fonti giornalistiche **sempre parafrasate**, testate citate solo in fondo; orari degli interventi **sempre arrotondati**; nessun nome di strumento di voce o musica nei video, tutti per uso non commerciale; contenuti del sito in **CC BY-NC-SA 4.0** (dati aperti CC BY 4.0).
- 🔴 Niente articoli `draft: true` in `content/`: un articolo è pubblicato o calendarizzato (bozze in `bozze/`).
- Badge degli articoli: Allerta · Emergenza · Avviso · Aggiornamento · Attività · Esercitazione · Formazione · Volontariato · Radiocomunicazioni · Prevenzione · Evento · Informazione · Comunicazione (palette e uso in `02-content-design-pa.md`, Allerta/Emergenza in `06`).

---

## Gate obbligatori prima del `git add`

| Quando | Agente / script |
|---|---|
| Articolo nuovo o modificato in `content/comunicazioni/` | `pc-article-reviewer` (salvo registro non-AGID chiesto dall'utente; mai sui file `-facile.md`, che seguono il CEFR A2) |
| Articolo con foto | cover + `image:`, Read delle foto, `pc-photo-caption-verifier`, nome del mezzo verificato in `content/chi-siamo/` |
| Articolo programmato o data in coda | `pc-calendario-editoriale`, `scripts/check-data-uscita.py` |
| Dati verificabili (date, numeri, norme, cause) | `pc-fact-checker`, `scripts/check-dati-canonici.py` |
| Dato che il sito scrive anche altrove | `pc-coerenza-trasversale`, `scripts/cerca-incongruenze.py --da-git origin/main` |
| Materiali scolastici (schede, kit, giochi, percorsi) | `pc-didattica-reviewer`, `check-parita-schede.py`, `check-lim.py`, `check-sintassi-js.cjs` |
| Fenomeni, scale, cronaca, persone | `pc-revisore-scientifico`, `pc-desk-giornalistico` |
| Asset, ancore, legale, traduzioni, dati, codice, workflow | `pc-integrita-tecnica`, `pc-conformita-legale`, `pc-revisore-traduzioni`, `pc-dati-e-feed`, `pc-revisore-codice`, `pc-revisore-automazioni` |
| Markup HTML personalizzato in `content/**/*.md` | verifica visiva con browser e screenshot letto |
| Testo per il sito | prosa senza tic da IA, `scripts/check-refusi.py` |

Un gate che non si può convocare si esegue a mano leggendo il file dell'agente, e il resoconto lo dice: mai saltato in silenzio. Dettagli: `11-articoli-foto-social.md`.

---

## Strumenti mancanti — si installano, senza giustificazioni

🔴 Istruzione dell'utente (17/10/2026): *«tu sai fare tutto e devi farlo senza giustificazioni»*. In qualunque sessione (PC, cellulare, cloud, routine) uno strumento che manca si installa prima di proseguire: `apt-get update` + `apt-get install`, poi `pip`/`npm`, poi download dalla fonte ufficiale, Chromium in `/opt/pw-browsers/chromium`. Mai saltare un controllo o consegnare con «qui non funziona». Procedura in `08-claude-code-setup.md` § «Uno strumento che manca si installa».

---

## Dove sono le regole

| File | Che cosa contiene | Quando si carica |
|---|---|---|
| `01-governance-pa.md`, `07-proattivita-coerenza.md` | priorità PA, divieti; coerenza, checkpoint batch, consiglio professionale | sempre (import qui sotto) |
| Regole trasversali (`qualita`, `autonomia`, `firma-dei-lavori`, `guasti`, `grafica`, `comunicazione-social`, `strumenti`, `sessione-cloud`) | regole comuni a tutti i repository | sempre |
| `02-content-design-pa.md`, `06-protezione-civile-scientifica.md`, `09-regole-contenuti-qualita.md` | scrittura AGID, badge, foto, formato data; rischio e allerte; i 19 punti (i vecchi «CLAUDE.md punto N») | `content/**`, `data/**`, `archetypes/**`, `static/formazione/**`, bozze social |
| `03-accessibility.md` | WCAG, toolbar, TTS, glossario, giochi, CAST UDL | tema, `static/**`, `content/**` |
| `04-…`, `04b-…`, `04c-hugo-static-cartelle.md` | architettura Hugo, menu, CSS, cartelle | tema, `static/**`, `hugo.toml` |
| `04a-hugo-shortcode-partial.md` | shortcode e partial | tema, JS/CSS, `data/**` |
| `05-github-aruba-deploy.md` | deploy Aruba e Pages, `.htaccess`, cache | `.github/**`, `scripts/**`, `.htaccess` |
| `08-claude-code-setup.md` | strumenti web, Firecrawl, Playwright, sandbox | `.claude/**`, `.mcp.json`, `scripts/foto-*` |
| `10-automazioni-github-actions.md` | workflow, routine, social automatici | `.github/**`, `scripts/**` |
| `lim-scuole.md` | compatibilità LIM | giochi, formazione, scuole, quiz |
| `11-articoli-foto-social.md` | sezioni ex CLAUDE.md: «Foto utente e banner — guarda PRIMA, scrivi DOPO» (con il «Web check obbligato»), «Auto-gate AGID prima del commit di un articolo», «Gate dei fatti e dei materiali scolastici», «Umanizzazione della scrittura», «Gate di legalità — Circolare DPC 6/8/2018», «Automatismo totale sugli articoli» (badge, versione facile, orari, «Fonti giornalistiche»), «Verifica visiva pre-commit su markup HTML nelle pagine», «Pubblicazione automatica social», «Auto-integrazione approfondimenti» | `content/**`, foto, formazione, giochi, social |
| `12-grafiche-loghi-deck-manuale.md` | sezioni ex CLAUDE.md: «Affiliazioni e riconoscimenti europei» (4 loghi, ESC), «Presentazione del sito (deck)», «Manuale di Protezione Civile — opera viva», «Video del Gruppo», «Licenza del sito — CC BY-NC-SA 4.0» | tema, grafiche, generatori, manuale, video |
| `13-pubblicazione-firma-accessi.md` | sezioni ex CLAUDE.md: «"Pubblica" = produzione FINO ALLA FINE», «Fine sessione con commit pendenti», «Nessun riferimento all'IA» con «Identità git», «Accessi e permessi», «Consiglio professionale», «Checkpoint pre-operazione batch» | `.github/**`, `scripts/**`, `AGENTS.md`, `COORDINAMENTO.md` |
| `14-agenti-architettura-automazioni.md` | sezioni ex CLAUDE.md: «Agenti specializzati» (organigramma, «Chi dirige»), «Skill», «Project overview», «Comandi principali», «Architettura — riferimenti rapidi», «Regole contenuti e qualità», «Automazioni» | agenti, skill, `manuale/**`, tema, workflow |

Un rimando «`CLAUDE.md` § …» in agenti, script o manuale porta alla sezione con lo stesso titolo nel file indicato qui. Manuale operativo: `MANUALE-SITO.md` (indice) e `manuale/`; fonti e calendario: `PIANO-EDITORIALE.md`; il workflow `aggiorna-manuale.yml` sorveglia le linee guida AGID e il manuale e le regole si aggiornano in coppia. Agenti in `.claude/agents/` (organigramma in `manuale/parte-19`): la sessione principale dirige; `pc-audit-completo`, `pc-article-reviewer` e `pc-didattica-reviewer` fanno da capi reparto.

---

## Progetto in breve

Sito statico del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma, Hugo + tema `flavour-pcgenzano` (Bootstrap Italia 2.x). Ogni push su `main` pubblica su Aruba (`https://www.protezionecivilegenzano.it/`, FTP) e su GitHub Pages (anteprima alleggerita). Modalità emergenza: `data/emergenza.json`; allerta manuale: `data/allerta.json` (livello insieme a titolo e descrizione).

@.claude/rules/01-governance-pa.md
@.claude/rules/07-proattivita-coerenza.md
