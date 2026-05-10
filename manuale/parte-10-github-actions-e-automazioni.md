_[Indice manuale](README.md)_

# Parte 10 — GitHub Actions e automazioni

Il repository ha **9 workflow** attivi che automatizzano deploy, controlli, aggiornamenti e audit. Ogni workflow vive in `.github/workflows/*.yml`. Tutti supportano l'esecuzione manuale tramite `workflow_dispatch` dalla tab Actions del repository.

### 10.1 — Panoramica

| Workflow | File | Trigger | Scopo |
|---|---|---|---|
| Build e Deploy | `deploy.yml` | push su `main`, manuale | Build Hugo, deploy Aruba (FTP), deploy GitHub Pages |
| Aggiornamento Allerta Meteo | `check-allerta.yml` | **Doppio trigger fail-safe**: cron-job.org ogni 5 min (primario, ~15 sec latenza) + GitHub schedule `17 * * * *` (fail-safe orario) | Legge feed DPC, aggiorna `data/allerta.json`. Anti-spam interno (stale_check 5h45min) impedisce commit duplicati. |
| Pubblicazione programmata | `pubblica-programmata.yml` | giornaliero (06:00 UTC), manuale | Riavvia il deploy per pubblicare articoli a data futura |
| Audit Accessibilità | `lighthouse-audit.yml` | dopo ogni deploy, manuale | Lighthouse su home e 5 pagine chiave |
| Smoke test post-deploy | `smoke-test-post-deploy.yml` | dopo ogni deploy, manuale | Verifica live di 20 pagine + 7 lingue + mini-app + 11 marker JS + 2 header sicurezza. Logica in `scripts/smoke-test-live.sh` |
| Aggiorna Bootstrap Italia | `update-bootstrap-italia.yml` | lunedì 06:00 UTC, manuale | Verifica nuove release Bootstrap Italia, apre PR |
| Aggiornamento MANUALE | `aggiorna-manuale.yml` | lunedì 06:00 UTC, manuale | Confronta hash fonti AGID/DI, apre Issue se cambiate |
| **Audit completo sito** | `audit-sito.yml` | lunedì 09:00 UTC, manuale | **Sezioni**: contenuti (1-15) + codice/template (16-22) + governance docs (23-32) + audit aggiuntivo (33-37) + link critici normativa (38). Fuso da `coerenza-docs.yml` + `check-normativa-links.yml` il 26 aprile 2026 |
| Verifica link sito completo | `check-links-sito.yml` | lunedì 10:00 UTC, manuale | Crawl completo con **lychee**: tutti i link interni + esterni del sito, apre issue automatica su 404/drift |

### 10.2 — `deploy.yml` — Build e Deploy

**Trigger**: push su `main`, esecuzione manuale.

**Cosa fa:**
1. Checkout del repository (fetch-depth 0 per ottenere la storia completa).
2. Setup Hugo extended.
3. Build principale con `hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"` (per Aruba).
4. Build secondario con `hugo --minify --baseURL "https://sviluppoitaliadigitale.github.io/sito-pc-genzano/"` (per GitHub Pages).
5. Deploy FTP su Aruba usando i secret `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`.
6. Deploy su GitHub Pages tramite `actions/deploy-pages`.

**Durata tipica**: 2–4 minuti.

**Fallimenti comuni:**
- build Hugo rotto (frontmatter malformato, shortcode non definito, YAML data invalido): il commit va revertito o corretto subito;
- FTP timeout: retry automatico, altrimenti richiede intervento;
- secret scaduto: aggiornare nei Settings del repo.

**Come usarlo manualmente**: Actions → "🚀 Build e Deploy" → Run workflow. Utile per ripubblicare dopo aver corretto un secret o dopo un rollback DNS.

#### Cartelle protette (escluse dal deploy FTP)

Il workflow usa `SamKirkland/FTP-Deploy-Action` con `dangerous-clean-slate: false` e una lista di **esclusioni esplicite**: i file presenti in queste cartelle sul server Aruba **non vengono toccati** dal deploy (né aggiunti, né aggiornati, né rimossi). Sono aree gestite **direttamente sul server** — tipicamente con contenuto storico, caricamenti manuali via FTP o materiali legacy.

```yaml
exclude: |
  **/documenti/**
```

**Storico delle esclusioni (rimosse 24 aprile 2026):** fino al 24 aprile 2026 la lista escludeva anche `**/cartelli/**`, `**/giochi-bambini/**`, `**/formazionepc/**`, `**/quizpc/**`. Dopo l'incidente del cartello AR4 Salesiani — un audit lato utente ha rilevato che il file `ar4.png` era mancante sul server Aruba, ma non c'era modo di accorgersene dal repo perché la cartella era esclusa — queste esclusioni sono state rimosse per eliminare il drift tra repo e server. I cartelli sono stati recuperati dal backup settimanale e ora vivono nel repo come unica fonte di verità.

**Conseguenze operative:**

- Un file messo in `static/documenti/` **non viene caricato su Aruba**: rimane solo nel repository e nella build locale/GitHub Pages. La cartella resta gestita manualmente sul server perché contiene materiale ereditato dal sito precedente (pieghevoli, kit "Io Non Rischio", schede storiche) mai migrato nel repo.
- Per **nuovi PDF o allegati** da depositare via git, usa le cartelle consentite: `static/allegati/AAAA/`, `static/manuali/`, `static/comunicati/AAAA/`.
- Per **nuovi cartelli segnaletici** (aree di attesa, aree di ricovero, aree di ammassamento), usa `static/cartelli/`: ora deployano automaticamente.
- Se vuoi aggiornare un file in `static/documenti/`, devi caricarlo **manualmente via FTP** su Aruba, oppure migrare il contenuto in una cartella del repo e aggiornare i riferimenti.
- Vale lo stesso principio per eventuali cartelle aggiunte alla lista in futuro. Quando modifichi `deploy.yml`, aggiorna **anche questa tabella e la Parte 1.10** del manuale.

### 10.3 — `check-allerta.yml` — Aggiornamento allerta meteo

**Trigger**: architettura doppio trigger fail-safe (10 maggio 2026):

1. **Primario — cron-job.org ogni 5 minuti** (free tier, SLA 99.9%): chiama l'API GitHub `workflow_dispatch` con un Personal Access Token fine-grained. Latenza end-to-end ~15 sec al cambio livello DPC.
2. **Fail-safe — GitHub schedule `17 * * * *`** (1 run/h al minuto 17, fuori dai picchi): paracadute se cron-job.org va giù. Garantisce ricontrollo entro 60 min nel peggior caso.

Esecuzione manuale via Actions tab GitHub sempre disponibile.

> **Storia tecnica (10 maggio 2026)**: cron GitHub `*/5` testato in produzione il 10 maggio 2026 ha dato 0 run scheduled in 42 minuti. La documentazione GitHub conferma: *"Schedule events can be delayed during periods of high loads. To decrease the chance of delay, schedule your workflow to run at a different time of the hour."* Cron espliciti scaglionati (`7,22,37,52`) provati ma con aderenza ancora variabile. Soluzione definitiva: trigger esterno cron-job.org puntuale + GitHub schedule `17 * * * *` come fail-safe minimale (1 run/h invece di 96/h, per non sovraccaricare il runner).

**Cosa fa:**
1. Scarica il CSV ufficiale del Dipartimento Protezione Civile dal mirror opendatasicilia.
2. Cerca la riga di "Genzano di Roma".
3. Estrae il livello massimo tra `avviso_criticita`, `avviso_idrogeologico`, `avviso_temporali`, `avviso_idraulico`.
4. Se diverso dal livello corrente in `data/allerta.json`, aggiorna il file.
5. Commit automatico dal bot `github-actions[bot]` con messaggio `chore: aggiornamento allerta <livello>`.
6. Il commit su `main` ritriggera `deploy.yml`.

**Permessi**: `contents: write`.

**Quando NON intervenire manualmente**: mai, se non per test. L'automazione è affidabile e le modifiche umane vengono sovrascritte al ciclo successivo.

**Disattivazione temporanea**: commenta la sezione `schedule:` e lascia solo `workflow_dispatch:`. Esempio in caso di manutenzione straordinaria del feed DPC.

### 10.4 — `pubblica-programmata.yml` — Pubblicazione programmata

**Trigger**: cron giornaliero (`0 6 * * *` = 06:00 UTC = 08:00 CEST / 07:00 CET), esecuzione manuale.

**Cosa fa:**
1. Chiama via `workflow_dispatch` il workflow `deploy.yml`.

**Perché esiste**: Hugo esclude dal build gli articoli con `date` futura (comportamento default `buildFuture: false`). Al passaggio di mezzanotte, gli articoli del giorno diventano "pubblicabili" ma il sito resta fermo all'ultimo deploy finché non si fa un nuovo build. Questo workflow garantisce un build quotidiano alle 08:00 del mattino italiano: gli articoli con data = oggi entrano nel sito.

**Nota operativa**: se vuoi pubblicare un articolo **a un'ora specifica** diversa dalle 08:00, lancia manualmente `deploy.yml` dall'interfaccia Actions.

### 10.5 — `lighthouse-audit.yml` — Audit Accessibilità e Performance

**Trigger**: `workflow_run` dopo il successo di `deploy.yml`, esecuzione manuale.

**Cosa fa:**
1. Attende che GitHub Pages propaghi (pochi secondi).
2. Esegue Lighthouse CI su un set di URL chiave (home, rischi, allerte, contatti, un articolo recente).
3. Produce un report scaricabile come artifact.
4. Se i punteggi scendono sotto soglia (tipicamente 90 performance, 95 accessibilità, 100 best-practices), apre una Issue.

**Quando guardarlo**: quando un deploy produce una Issue di regressione. Le cause più frequenti sono immagini non ottimizzate, nuovi script bloccanti, contrasti troppo bassi.

### 10.6 — `update-bootstrap-italia.yml` — Aggiornamento Bootstrap Italia

**Trigger**: cron settimanale (lunedì 06:00 UTC), manuale.

**Cosa fa:**
1. Interroga la release più recente del repository `italia/bootstrap-italia`.
2. Confronta con la versione usata nel sito (nel template base `layouts/_default/baseof.html` o nel config).
3. Se c'è una nuova release, apre una PR con l'aggiornamento del riferimento CDN/asset e un commento con il changelog ufficiale.

**Permessi**: `contents: write`.

**Cosa fare quando apre una PR:**
1. Leggi il changelog della release (linkato nella PR).
2. Esegui `hugo server` in locale dopo il merge di prova per verificare che non ci siano breaking changes.
3. Testa manualmente: navbar, hero, card, form, alert, footer.
4. Lancia `lighthouse-audit.yml` manuale per confermare che accessibilità/performance non regrediscono.
5. Approva e fai merge.

**Quando rifiutare una PR**: major version bump (es. da 2.x a 3.x) richiede review completa del tema — non approvare automaticamente.

### 10.7 — `aggiorna-manuale.yml` — Verifica fonti AGID/Designers Italia

**Trigger**: cron settimanale (lunedì 06:00 UTC), manuale.

**Cosa fa:**
1. Scarica (con `curl`) le pagine ufficiali AGID / Designers Italia / Writing Toolkit / WCAG indicate nella configurazione del workflow.
2. Calcola hash SHA-256 del contenuto.
3. Confronta con gli hash salvati nel repository (commit precedente).
4. Se uno o più hash sono cambiati, apre una Issue con:
   - elenco delle pagine cambiate;
   - checklist di revisione ("confronta la sezione X del manuale con la nuova versione della pagina Y");
   - link alla pagina ufficiale aggiornata.

**Permessi**: `contents: write`, `issues: write`.

**Cosa fare quando apre una Issue:**
1. Apri la pagina ufficiale aggiornata.
2. Confronta con la Parte rilevante di `MANUALE-SITO.md` e con i file in `.claude/rules/`.
3. Aggiorna testo del manuale e/o delle regole se necessario.
4. Aggiorna il campo "Ultimo check linee guida AGID" in testa al manuale.
5. Commit + push, chiudi la Issue con un commento che cita il commit.

### 10.8 — `audit-sito.yml` — Audit completo settimanale (sezioni)

**Trigger**: cron settimanale (lunedì 09:00 UTC), manuale.

**Storia**: nato ad aprile 2026 con 15 controlli sui contenuti, esteso il 26 aprile 2026 a 32 controlli inglobando `coerenza-docs.yml` (lun 07:00). Lo stesso giorno esteso a 37 con il blocco "audit aggiuntivo" (mixed content, accessibility alt, coerenza traduzioni, hugo.toml ↔ data files, smoke test rendering) e a 38 inglobando anche `check-normativa-links.yml` (lun 08:00) come sezione 38 dedicata ai link critici con messaggi specifici. **Risultato: -2 workflow, 1 issue settimanale invece di 3, stessa copertura.**

**Cosa fa:** scansiona il sito completo per rilevare automaticamente la stessa classe di errori che emerse dagli audit manuali di aprile 2026 — COI 14°→15°, cartello AR4 mancante, citazioni di 115/118 come numero da chiamare, duplicate target paths sulle 7 lingue, articoli `draft:true` dimenticati con data passata, link interni a slug typo, residui di refactoring (CCV-MB, manuale lombardo), `/index.html` reintrodotti dopo il fix Chrome cache. Apre **una sola issue settimanale** se trova deviazioni.

**32 controlli effettuati** — divisi in 3 macro-aree:

#### Contenuti pubblicati (sezioni 1-15)
1. **COI** — riferimenti al 15° Centro Operativo Intercomunale (errore se grado diverso).
2. **NUE 112** — nessuna istruzione a chiamare 115/118/1515 (esclude usi legittimi tipo "ARES 118" come nome organizzazione, "Non chiamare il 115" didattico).
3. **Telefono istituzionale coerente** — cifre da `hugo.toml` confrontate con tutto il sito; `href="tel:"` senza spazi (RFC 3966 E.164).
4. **Sede e CAP** — warning su CAP ≠ `00045` accanto a "Genzano".
5. **Placeholder** — `TODO`, `TBD`, `FIXME`, `XXX`, `lorem ipsum`, `DA COMPLETARE`, template Go non espansi.
6. **File statici** — `src`, `href`, `url:` puntano a file esistenti in `static/`.
7. **Badge** — usati negli articoli devono essere in `badge.html` (case-insensitive).
8. **Anno articoli** — fuori `2020..anno_corrente+1` = typo.
9. **Allegati senza dimensione** (WCAG 3.3.5).
10. **Frasi AGID** — euristica: ≥3 frasi >40 parole = warning.
11. **Pagine `_index.md` con `draft:true`** (sparirebbero dal sito).
12. **Schede stampabili linkate** ma file HTML mancante.
13. **Modalità emergenza** attiva da troppo tempo (>14 giorni senza aggiornamento = probabile dimenticanza).
14. **Pagine legali con `dataUltimaRevisione` >18 mesi** (rivedere il contenuto).
15. **ID widget duplicati** nella stessa pagina (rompono il bottone "Carica").

#### Codice e template (sezioni 16-22)
16. **Hugo build pulito** — `hugo --minify --printPathWarnings` non emette warning di rilievo (es. duplicate target paths sulle 7 lingue come è successo ad aprile 2026).
17. **Articoli `draft:true`** — regola del progetto: nessun articolo in revisione, solo immediato o calendarizzato (`draft:false` + data futura).
18. **Link interni a slug inesistenti** — rileva typo o slug rinominati post-creazione (es. `chiamare-112-correttamente` vs `segnalare-emergenze-112-come-fare`).
19. **Sintassi JavaScript** — `node --check` su tutti i `.js` standalone in `static/` (giochi, quiz, scenari, mappa, abili-a-proteggere).
20. **Validità YAML workflow** — `python3 yaml.safe_load` su ogni `.github/workflows/*.yml` per intercettare il pattern velenoso heredoc-Python (vedi `.claude/rules/05-github-aruba-deploy.md` § "qualità YAML").
21. **Path assoluti nei template** — `href="/..."` hardcoded che funziona su Aruba ma è rotto su GitHub Pages (subpath). Tutti i path interni devono usare `relURL` / `absURL`.
22. **Residui di refactoring** — `/index.html`, `intercomunale lombarda`, `Imbersago`, `CCV-MB`, `Monza-Brianza`. Implementa la regola `.claude/rules/07-proattivita-coerenza.md`: dopo un fix di pattern, sweep continuo per evitare reintroduzioni.

#### Governance docs (sezioni 23-32)
23. **File di governance** esistenti (`CLAUDE.md`, `MANUALE-SITO.md`, `PIANO-EDITORIALE.md`, archetypes, 7 rule files).
24. **Import `@.claude/rules/*.md`** in `CLAUDE.md` puntano a file esistenti.
25. **Badge list coerente** fra `badge.html`, `CLAUDE.md`, `rule 02`, `archetypes/comunicazioni.md` (la fonte di verità è `badge.html`, le altre devono allinearsi).
26. **Formato data articoli** — solo `AAAA-MM-GG`, mai `AAAA-MM-DDTHH:MM:SSZ` (Hugo escluderebbe l'articolo dal build).
27. **Frontmatter completo** — campi obbligatori `title date description badge priorita autore draft` presenti in ogni articolo.
28. **Riferimenti incrociati** in `CLAUDE.md` verso `MANUALE-SITO.md`, `PIANO-EDITORIALE.md`, workflow `aggiorna-manuale.yml`.
29. **Pagine `_index.md` istituzionali** (19 pagine obbligatorie: privacy, note-legali, accessibilità, social-media-policy, contatti, ecc.).
30. **Shortcode `foto`** presente in `themes/.../shortcodes/` e documentato in `MANUALE-SITO.md` e `rule 02`.
31. **Script `scripts/export-contesto-ai.sh`** presente ed eseguibile (`chmod +x`).
32. **`dataUltimaRevisione`** sulle 4 pagine legali in formato `AAAA-MM-GG` tra virgolette.

#### Audit aggiuntivo (sezioni 33-37)
33. **Mixed content** — link `http://` esterni nelle pagine HTTPS (warning per browser moderni). Eccezioni note: `parcocastelliromani.it`, `idrografico.roma.it`, `zonesismiche.mi.ingv.it` (siti senza HTTPS lato fornitore).
34. **`image_alt` accessibility** (WCAG 1.1.1) — articoli con `image:` ma `image_alt` vuoto o mancante. Screen reader leggerebbero il filename.
35. **Coerenza dati istituzionali nelle 7 traduzioni** — pagine `content/{english,deutsch,espanol,francais,portugues,romana,esperanto}/numeri-utili/_index.md` devono contenere sede ("Sicilia"), CAP "00045", numero "112". Se uno manca = traduzione non aggiornata.
36. **Coerenza `hugo.toml` ↔ `data/numeri_utili.yaml`** — il telefono di sede in `hugo.toml` deve essere presente nel record "locale" del yaml (alimenta la card Numeri Utili).
37. **Smoke test rendering** — verifica che le 12 pagine critiche generate (`public/index.html`, `cosa-fare-adesso`, `numeri-utili`, `contatti`, `cartografia`, `assistente`, `comunicazioni`, `formazione`, `rischi-prevenzione`, `diventa-volontario`, `area-download`, `faq`) abbiano un `<h1>` (cattura rendering rotto / frontmatter sbagliato che Hugo non sempre segnala).
38. **Link critici (normativa, PDF locali, Normattiva)** — sentinella veloce con messaggi specifici sugli 8 link che, se cadono, vanno individuati subito perché compaiono in più pagine: 2 portali ufficiali (Lazio Agenzia PC, DPC normativa nazionale), 4 PDF locali sul server Aruba (Piano Emergenza Comunale, Ordinanza AIB 2025, Piano AIB Lazio, Piano Triennale Lazio) gestiti manualmente in `/documenti/`, 2 link Normattiva (D.Lgs. 1/2018 Codice PC, L. 353/2000 incendi boschivi). Lychee farà comunque il crawl completo lun 10:00 ma con output generico; questa sezione apre l'issue settimanale dell'audit con il nome del documento rotto. Sostituisce il workflow `check-normativa-links.yml` precedente (lun 08:00).

**Formato Issue:** report markdown con sezioni numerate. `❌` = errore (da correggere prima del prossimo deploy), `⚠️` = warning (valutare se falso positivo). Label issue: `audit`, `qualità-testi`, `manutenzione`.

**Quando intervenire:** ogni volta che apre una Issue. Il workflow è tarato per essere conservativo (pochi falsi positivi). Se un warning ricorrente è un falso positivo legittimo (es. una citazione lunga, un articolo intenzionalmente con anno fuori range), aggiungi un'eccezione mirata al workflow così la segnalazione non si ripete.

**Perché esiste:** gli audit manuali di aprile 2026 hanno trovato errori che convivevano da tempo nel sito senza che nessuno se ne accorgesse (COI 14° nel footer, AR4 404, `href="tel:+39 06 9362600"` con spazi che alcuni browser mobile non onoravano, duplicate target paths sulle 7 lingue, link interni a slug typo che il render-link hook nascondeva graceful, `draft:true` con data passata mai pubblicato). Questo workflow evita che errori analoghi si sedimentino di nuovo.

### 10.9 — `check-links-sito.yml` — Verifica link sito completo

**Trigger:** lunedì ore 10:00 UTC, esecuzione manuale.

**Cosa fa:**
1. Build Hugo del sito con baseURL di produzione.
2. Esegue **lychee** (`lycheeverse/lychee-action@v2`, industry standard per link checking) su tutti i file `public/**/*.html` generati dal build.
3. Verifica ogni link presente nelle pagine: interni (anchor, path), esterni (widget, card hub, fonti), asset (PDF, immagini).
4. Con cache di 1 giorno (`--max-cache-age 1d`) per evitare di martellare i fornitori esterni settimana dopo settimana se un link è già stato verificato di recente.
5. Se trova link rotti, apre **automaticamente** una issue GitHub con label `manutenzione`, `link-rotti`, `automatico` e report markdown dettagliato (link rotto, codice HTTP, pagina che lo contiene).

**Accepted HTTP codes:** 200, 201, 204, 206, 301, 302, 307, 308, 403, 429. I codici 403 e 429 sono considerati OK perché alcuni siti PA bloccano bot di default ma il link funziona per utenti umani, e 429 è rate-limiting non rottura vera.

**Timeout:** 20s per URL, 3 retry con 5s di attesa (gestisce i siti PA italiani che sono spesso lenti).

**User-Agent personalizzato:** `Mozilla/5.0 (compatible; PCGenzanoLinkChecker/1.0; +https://www.protezionecivilegenzano.it/)` — identifica chiaramente il checker ai fornitori.

**Esclusioni:**
- `^tel:` — link telefonici
- `^mailto:` — email
- `^#` — anchor interni
- `github.io/sito-pc-genzano` — evita self-check verso la preview
- `localhost`, `127.0.0.1` — dev local

**Quando intervenire:** ogni volta che apre una Issue. La Issue contiene l'elenco esatto dei link rotti con codice HTTP e pagina sorgente. Correggi il link (spesso è un path rinominato dal fornitore) e commit.

**Perché esiste:** catturare drift dei link esterni. Esempio reale: aprile 2026, la hub `/strumenti/` è stata pubblicata con il link ANAS `/it/le-strade/viabilita-italia` che in poche ore è tornato 404 (URL obsoleta). L'utente ha trovato il problema a mano; questo workflow lo avrebbe catturato al primo run settimanale.

**Distinzione con `audit-sito.yml` sezione 38:** quest'ultima verifica gli **8 link critici** (Normattiva, DPC, Lazio normativi, PDF locali) con pre-pattern e messaggi dedicati alle 09:00 — sentinella veloce. Il check completo con lychee alle 10:00 è il **catch-all**: tutto il resto del sito (hub strumenti, widget, card, contenuti degli articoli, link PDF nei documenti). Girano 1 ora di distanza per non sovraccaricare il runner.

### 10.10 — Disabilitare temporaneamente un workflow

Due modi:

**Modo A — Interfaccia GitHub** (reversibile, nessun commit):
1. Vai su Actions.
2. Seleziona il workflow nella sidebar.
3. Menu "···" in alto a destra → "Disable workflow".
4. Per riabilitare: stesso menu, "Enable workflow".

**Modo B — Commento in YAML** (tracciato in git):
1. Apri il file `.github/workflows/<nome>.yml`.
2. Commenta la sezione `schedule:` con `#`.
3. Commit con messaggio chiaro ("Sospensione temporanea workflow X — motivo: ...").
4. Per riabilitare: rimuovi i commenti, commit, push.

Preferisci sempre Modo B per tracciabilità, salvo esigenze di emergenza.

### 10.11 — Leggere i log di un workflow

1. Actions → workflow interessato → seleziona run specifica.
2. Espandi il job e lo step che ha fallito.
3. Leggi dalla prima riga rossa o gialla.

**Errori tipici e come leggerli:**
- `Error: YAMLParseError` → data file rotto, vedi 9.9.
- `hugo: error: failed to render...` → template o frontmatter rotto; riga indicata in output.
- `ftp: 550 ...` → permessi o path errato su Aruba; controlla secret.
- `Hash mismatch` → stai aggiornando un file con conflitto; riesegui dopo pull.

### 10.12 — Aggiungere un nuovo workflow

Regole:
- Nome file descrittivo in kebab-case: `nome-azione.yml`.
- `name:` con emoji opzionale ma coerente con gli altri.
- Sempre supportare `workflow_dispatch` per test manuale.
- Dichiarare esplicitamente i `permissions:` minimi necessari.
- Usare action ufficiali o mantenute (`actions/checkout@v4`, `actions/setup-node@v4`, ecc.), pinnate a major version.
- Niente secret hardcoded. Usare `${{ secrets.NAME }}` con secret creati nei Settings del repository.
- Documentare il nuovo workflow in questa Parte 10 e in `CLAUDE.md` (sezione Automazioni).

---

_[Indice manuale](README.md)_

[← Parte 09 — File dati `data/` e stati del sito](parte-09-file-dati-data-e-stati-del-sito.md) · [↑ Indice](README.md) · [Parte 11 — Testi per i social (Instagram, Facebook, X, Telegram) →](parte-11-testi-per-i-social-instagram-facebook-x-telegram.md)
