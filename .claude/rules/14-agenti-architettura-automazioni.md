---
paths:
  - ".claude/agents/**"
  - ".claude/skills/**"
  - "manuale/**"
  - "MANUALE-SITO.md"
  - "themes/**"
  - "layouts/**"
  - "assets/**"
  - "hugo.toml"
  - "data/**"
  - ".github/**"
  - "scripts/**"
---

# Agenti, skill, architettura, comandi e automazioni

Sezioni spostate da `CLAUDE.md` l'11/11/2026, con il testo integrale: organigramma degli agenti, uso delle skill, panoramica del progetto, comandi, architettura, i 19 punti e le automazioni. Si caricano quando si lavora su agenti, skill, manuale operativo, tema, dati, workflow e script.

## Agenti specializzati (`.claude/agents/`)

52 agenti custom da usare PROATTIVAMENTE quando la conversazione fa match con la loro `description` (l'utente scrive in italiano naturale, fai tu il match e attiva da solo). I 17 aggiunti il 06/09/2026 (dopo l'audit esterno) formano il **sistema di affidabilità interno** descritto in § "Gate dei fatti e dei materiali scolastici"; i 3 aggiunti il 07/10/2026 (`pc-visitatore-reale`, `pc-collaudo-funzionale`, `pc-prestazioni`) guardano il sito **da fuori**, sul sito pubblicato e con un browser vero, dopo che un audit esterno ha trovato `/volontariato/` in 404 con tutti i controlli interni verdi; i 12 aggiunti lo stesso giorno completano l'organigramma «azienda» chiesto dall'utente (*«tutti gli specialisti del settore protezione civile, più agenzia di marketing e giornalistica»*). I 2 aggiunti il 17/10/2026 (`pc-testi-nel-codice`, `pc-auditor-indipendente`) coprono le sviste trovate da un altro audit esterno: i testi che vivono dentro il codice (assistente, giochi, lezioni, Telegram, generatori) e il metodo dell'auditor esterno, con la regola che **ogni rilievo diventa un controllo**.

🔴 **Chi dirige**: la **sessione principale** è la direzione: convoca gli specialisti in sequenza (i gate degli articoli, l'audit completo, i materiali scolastici sono copioni che lei esegue) o in parallelo quando il lavoro si divide in parti indipendenti (fino a venti agenti alla volta). Dal 16/10/2026, su richiesta dell'utente, tre agenti fanno da capi reparto e hanno `Agent` fra i `tools`: `pc-audit-completo`, `pc-article-reviewer` e `pc-didattica-reviewer`. Quando lo strumento c'è, convocano da soli gli specialisti dei loro copioni; quando manca, ne eseguono a mano i controlli essenziali. Gli altri agenti non delegano. Lo strumento c'è solo se la sessione ammette più livelli di agenti (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`): da terminale sul PC il valore predefinito è 3, le sessioni cloud dell'app partono da 1. In cloud la sessione principale può alzarlo per sé scrivendo `{"env":{"CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH":"3"}}` in `~/.claude/settings.json` della macchina della sessione: vale dopo qualche secondo, senza riavvio, e solo per quella sessione (verificato il 16/10/2026: prima un sottoagente non aveva `Agent`, dopo sì). 🔴 Mai sul PC, dove quel file contiene le impostazioni personali dell'utente, e mai nelle routine: il livello si alza solo per un lavoro grande e divisibile in una sessione con l'utente, perché in quella prova ogni agente è partito con circa 390 mila token di contesto e una catena moltiplica il consumo. Il `.claude/settings.json` del repository non serve allo scopo: le chat dell'app partono dalla cartella sopra il repository e non lo leggono. Le squadre di agenti sperimentali (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`), provate lo stesso giorno, non servono: attivate a sessione in corso, l'agente con nome è partito come un sottoagente qualsiasi. Un gate che non può essere convocato si esegue a mano leggendo il file dell'agente, e il rapporto lo dichiara; mai saltato in silenzio.

**Organigramma per reparti** (dettaglio in `manuale/parte-19` § 19.0):

| Reparto | Agenti |
|---|---|
| Direzione e qualità | `pc-audit-completo`, `pc-auditor-indipendente`, `pc-documentazione`, `pc-site-auditor` (fotografia rapida del repo) |
| Protezione civile tecnico-scientifica | `pc-revisore-scientifico`, `pc-normative-verifier`, `pc-pianificatore-emergenza`, `pc-cartografo-gis`, `pc-medico-emergenza`, `pc-psicologo-emergenza`, `pc-radiocomunicazioni` |
| Sala operativa | `pc-comunicazione-crisi`, `pc-esercitazione-emergenza` |
| Volontariato e inclusione | `pc-volontariato-terzo-settore`, `pc-inclusione-fragilita` |
| Redazione giornalistica | `pc-article-reviewer`, `pc-desk-giornalistico`, `pc-fact-checker`, `pc-revisore-linguistico`, `pc-correttore-bozze`, `pc-calendario-editoriale`, `pc-internal-linker`, `pc-content-freshness`, `pc-coerenza-trasversale`, `pc-italian-l2-writer`, `pc-revisore-traduzioni`, `pc-ufficio-stampa` |
| Agenzia di comunicazione | `pc-strategia-comunicazione`, `pc-art-director`, `pc-social-publisher`, `pc-produzione-multimediale`, `pc-seo-checker`, `pc-materiali-publisher` |
| Fotografia | `pc-image-fixer`, `pc-photo-caption-verifier` |
| Scuola | `pc-didattica-reviewer`, `pc-print-card-qa` |
| Esperienza utente e collaudo | `pc-accessibility-auditor`, `pc-usabilita`, `pc-verifica-visiva`, `pc-visitatore-reale`, `pc-collaudo-funzionale` |
| Tecnologia | `pc-revisore-codice`, `pc-testi-nel-codice`, `pc-revisore-automazioni`, `pc-sicurezza`, `pc-integrita-tecnica`, `pc-dati-e-feed`, `pc-deploy-validator`, `pc-prestazioni`, `pc-issue-triage` |
| Legale | `pc-conformita-legale` |


Le descrizioni complete degli agenti, con i trigger, sono nel frontmatter dei file in `.claude/agents/` e arrivano a ogni sessione insieme all'elenco degli agenti.

Specifiche + workflow combinati in `manuale/parte-19-agenti-specializzati.md`. Aggiungendo/modificando un agent, aggiorna la Parte 19 e questa tabella.

---

## Skill — invocazione col tool `Skill`

🔴 Prima di un task ≥3 step: se fra le skill disponibili nella sessione ce n'è una che fa già questo, invocala col tool `Skill` (non con Read+Bash). Non citare una skill senza invocarla; non usare skill di marketing sui contenuti AGID.

**Agent custom + skill in sequenza** quando rilevanti: revisione articolo `pc-article-reviewer` → `pc-calendario-editoriale` (se programmato) → `pc-fact-checker` (se dati) → `pc-desk-giornalistico` (se cronaca) → `pc-revisore-scientifico` (se fenomeni) → `pc-photo-caption-verifier` (se foto) → `accessibility` → `seo-audit`; materiali scolastici `pc-didattica-reviewer` → `pc-fact-checker` → `pc-verifica-visiva`; pre-push `pc-revisore-codice` → `pc-deploy-validator` → `production-audit` → `security-scan`; nuovo script `search-first` → `python-patterns` → `python-testing` → `pc-revisore-automazioni` (se in CI); modifica strutturale → `pc-usabilita` → `pc-documentazione`; allerta o emergenza → `pc-comunicazione-crisi` → `pc-fact-checker` → `pc-psicologo-emergenza` (se tocca persone); contenuto sanitario → `pc-medico-emergenza` → `pc-fact-checker`; grafica istituzionale → `pc-art-director` → `pc-verifica-visiva`; modifica a uno strumento interattivo o a CSS/JS comuni → `pc-revisore-codice` → `pc-collaudo-funzionale` → `pc-prestazioni`; menu, home o ricerca → `pc-usabilita` → `pc-visitatore-reale`.

---

## Project overview

Sito statico del **Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma**, Hugo + tema custom `flavour-pcgenzano` (Bootstrap Italia 2.x). Deploy a ogni push su `main` via GitHub Actions: **Aruba** (`https://www.protezionecivilegenzano.it/`, FTP) + **GitHub Pages** (`https://sviluppoitaliadigitale.github.io/sito-pc-genzano/`). Dal 06/11/2026 la copia su GitHub Pages è alleggerita, e dal 10/11/2026 il taglio è più stretto perché la pubblicazione si interrompe a 10 minuti e non si può allungare: senza video, audio, presentazioni, archivi ZIP, PDF oltre 2 MB e raster non ottimizzati oltre 2 MB, che si aprono da Aruba (`scripts/alleggerisci-copia-pages.py`, rule 05 § «Conservare immagini e allegati»). Aruba resta completo e non si tocca.

Architettura completa: rule `04`-`04c`. Manuali nella root: `MANUALE-SITO.md` (indice, split in `manuale/parte-NN-*.md`), `MANUALE-MOBILE.md` (workflow mobile/cloud), `PIANO-EDITORIALE.md` (fonti + calendario), `README.md`, `CONTESTO-PROGETTO.md` (export per altre AI).

---

## Comandi principali

```bash
hugo server                    # dev (server -D mostra le bozze)
hugo --minify                  # build GitHub Pages
hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"   # build Aruba
git add . && git commit -m "..." && git push    # pubblica (CI deploy)
bash ~/gestione-sito.sh        # script gestione contenuti/emergenze/allerte
bash scripts/export-contesto-progetto.sh              # → CONTESTO-PROGETTO.md per altra AI
bash scripts/applica-fascia-foto.sh <src> <out-senza-ext>   # fascia blu → static/images/<out>.webp
bash scripts/scarica-pittogrammi.sh [--force]   # libreria ISO 7010 + ARASAAC
bash scripts/foto-da-{wikipedia,nasa,usgs}.sh ...           # foto da fonti libere
bash scripts/genera-social.sh <file>|--all|--since DATA|--dry-run   # bozze social (GEMINI_API_KEY)
python3 scripts/genera-microtext.py {text|image|watermark} ...      # filigrane anti-falsificazione
python3 scripts/indexnow-ping.py                # ping IndexNow (di norma via workflow)
```

---

## Architettura — riferimenti rapidi

Mappa completa in rule `04`/`04a`/`04b`/`04c`. Componenti chiave:

- **Homepage dual-mode** (normale/emergenza) — `layouts/index.html` + `data/emergenza.json`. Banner emergenza **site-wide** da `baseof.html`.
- **Data files** in `data/` — `emergenza.json`, `allerta.json`, `risk_cards.yaml`, `numeri_utili.yaml`, `quick_links.yaml`, `social_links.yaml`, `codici_colore.yaml`, `glossario.yaml`, `aree_emergenza.yaml`, `dae.yaml`, `idranti.yaml`, `stato-sistema.json`, `eventi_storici.yaml`, `lis.yaml`, `ecmwf_charts.json` (carte Meteo Europa), `meteo_genzano.json` (riquadro cartina Lazio). Open data del Laboratorio meteo in `static/open-data/clima-*.json`.
- **Badge articoli** (in `partials/badge.html`): Allerta · Avviso · Comunicazione · Attività · Formazione · Evento · Volontariato · Radiocomunicazioni · Prevenzione · Esercitazione · Aggiornamento · Informazione · Emergenza — palette/hex/contrasto in rule 02.
- **Shortcode:** `foto`, `pittogramma`, `cosa-non-fare`, `chi-chiamare`, `link-card`, `pagina-emergenza-lite`, `dashboard-*` (cruscotto), `scheda-terremoto` (scheda dettaglio evento sismico INGV su `/cruscotto/terremoto/#<id>`), i **dossier interattivi** (`dossier-hero`/`dossier-scena`/`dossier-dati`/`dossier-dato`/`dossier-confronto`/`dossier-hotspot`/`dossier-punto`/`dossier-chiusura`/`dossier-fonti`, sezione `/dossier/` scrollytelling full-bleed), e i **componenti Bootstrap Italia** `callout` (nativo BI), `passi` (stepper), `timeline`, `galleria` (carosello ≥4 foto), e gli shortcode **CAA** `caa-tabella`/`caa-voce` (tabelle di Comunicazione Aumentativa Alternativa: pittogrammi ARASAAC + parola, pagina `/tabelle-comunicazione/`). **Render hook:** `render-link.html`, `render-table.html`. **Partial** chiave: `article-cover`, `leggi-ad-alta-voce` (TTS), `indice-pagina` (indice + scrollspy site-wide), `accessibility-toolbar`, `assistente-fab`, `structured-data` (JSON-LD), `meta-social` (OG), `articoli-correlati`, `page-tools`, `sos-112`, `qr-articolo`, `ricerca-modal` (Pagefind Ctrl+K), `lis-badge`.
- **Pagine/feature speciali:** ricerca Pagefind (`/cerca/`), QR articolo (`static/qr/`), `/stato-sistema/`, `/podcast/` (puntate sospese dal 05/11/2026: tornano solo rifatte, con trascrizione verificata — `pc-materiali-publisher` § «Niente si pubblica senza verifica») + `/articoli-da-ascoltare/`, `/storia/`, assistente vocale, `/lanterna/` (standalone), LIS `/lis/` (`data/lis.yaml`), "Approfondimenti video" (`genera-video-correlati.py`, gate pertinenza), notifiche allerta browser, quiz `/quiz-preparazione/`, hub `/giochi/`, `/open-data/`, `/audio-e-podcast/`, hub `/standard-iso/`, `/feed-rss/`, traduzioni (hub + 3 pagine × 7 lingue, `tts: false`, hreflang + `<html lang>` dinamico), pagina lite `/emergenza/` (44 KB), metodo editoriale/E-E-A-T (`static/llms.txt`), microtext (`genera-microtext.py`), **cruscotto** `/cruscotto/` (schede dati live INGV/meteo/radar/satellite/aria/mare/ECMWF), **scheda terremoto** `/cruscotto/terremoto/#<id>` (dettaglio di un singolo evento sismico da INGV FDSN, tab sul modello di terremoti.ingv.it, linkata da ogni riga del cruscotto sismico), **Laboratorio meteo** `/laboratorio-meteo/` (costruttore di grafici climatici ERA5/Open-Meteo live + esempi pre-cotti, `static/js/laboratorio-meteo.js`), **Dossier interattivi** `/dossier/` (racconti visivi scrollytelling full-bleed a tema scuro, motore riusabile = sezione + layout + 9 shortcode `dossier-*` + `dossier.css`/`dossier.js`; ogni nuovo dossier = un file in `content/dossier/`; box homepage col più recente; immagini solo con licenza chiara; vedi `manuale/parte-39-dossier-interattivi.md`), **Tabelle di comunicazione CAA** `/tabelle-comunicazione/` (board ARASAAC stampabili per chi in emergenza non riesce a parlare — shortcode `caa-tabella`/`caa-voce`, voce di menu sotto "Accessibilità e Supporti"), **Piano familiare offline** (`/piano-familiare/` — pulsante "Salva piano offline (HTML)": file `.html` autoconsistente solo-testo generato via Blob, apribile senza rete in blackout), **Facile da leggere multilingua** (`/facile-da-leggere/` IT + traduzioni `en`/`eo`/`ro`/`ar` come pagine di sezione, selettore lingua interno + tag `hreflang` SEO reciproci via frontmatter `hreflang:`/`hreflang_xdefault`), e i **banner homepage** `banner-caldo.html` (striscia stagionale "Consigli sul caldo", visibile solo giugno–settembre, mese deciso a build-time) + `banner-volontariato.html` (campagna Regione Lazio "Non c'è PC senza di te", solo modalità ordinaria; vedi memory [[project_campagna_lazio_non_ce_pc_senza_di_te]]).
- **Output format custom** (`hugo.toml [outputs] home`): oltre a HTML/RSS/JSON, la home genera **`/allerta-cap.xml`** (feed **CAP 1.2** Common Alerting Protocol OASIS, machine-readable, da `data/allerta.json` — un `<info>` per pericolo: oggi/domani/avviso meteo/incendi AIB Zona 9; `identifier` composito byte-stabile anti-spam) e **`/news-sitemap.xml`** (sitemap Google News, solo articoli `comunicazioni` delle ultime 48h, dichiarata in `static/robots.txt`).
- **TTS Web Speech API** (pagine `tts:`, coach giochi, fiabe), **coach giochi**, **glossario inline** — rule 03.

---

## Regole contenuti e qualità (19 punti)

Elenco completo in rule `09-regole-contenuti-qualita.md`. Vincoli più critici:
- **P1 Formato data:** `AAAA-MM-GG` se 1 articolo/giorno; `AAAA-MM-GGTHH:MM:SS+02:00` con orari crescenti (00:01, 00:02…) se 2+/giorno. Mai `Z` UTC.
- **P4 Qualità ChatGPT 9.5/10:** redazione AGID in ogni contesto (CLI/mobile/cloud), nessuna delega ad AI esterne.
- **P9 Banner intoccabile:** `image:` = cover tipografica col titolo; tutte le foto **inline** con `{{< foto >}}`, mai nel banner; marker `# TODO-foto-*` bandito; in revisione testuale `image:` non si tocca.
- **P12 Gerarchia fonti crisi:** AGID+DPC → CNR/ISPRA → EENA/CWA → ISO 22329 + WCAG 2.2 AA → normativa orizzontale.

---

## Automazioni (GitHub Actions) e note operative

Tabella completa workflow + note operative in rule `10-automazioni-github-actions.md`. Trigger rapidi:
- `deploy.yml` a ogni push su `main`. **Priorità deploy (3 livelli, 31/05/2026):** allerta/`pubblica-programmata` immediati (`-f priority=urgent`), articoli (push merge) immediati e prioritari, aggiornamenti di sfondo (meteo/ECMWF/clima/video/stato/QR/pacchetti/indice) **coalescati** da `deploy-coalescer.yml` (`workflow_run` al completamento dei workflow meteo + cron ~30 min come fallback, dall'11/06/2026). Dettagli in rule 10 § "Modello di priorità del deploy".
- `aggiorna-manuale.yml` (lunedì 06:04 UTC): monitora le fonti AGID/Designers Italia/DPC e apre issue quando cambiano — manuale e `.claude/rules/` vanno aggiornati in coppia (rule 02 § "Sincronizzazione automatica con gli aggiornamenti AGID").
- `normativa-watcher.yml` (ogni giorno 07:30 italiane) legge **albo pretorio di Genzano, Gazzetta Ufficiale, Normattiva, BURL Lazio, notizie del Consiglio regionale e, dal 13/10/2026, le immagini satellitari del giorno di EU Space (Copernicus)**, e dal 05/11/2026 anche **avvisi, comunicati e notizie del sito del Comune di Genzano**, **notizie di Regione Lazio, Città metropolitana di Roma e Prefettura di Roma**, le **sentenze e ordinanze della Corte costituzionale** (Gazzetta Ufficiale, 1ª Serie speciale), e nella rassegna stampa i **feed delle testate locali** (Castelli Notizie, Il Mamilio, Il Caffè, Controluce, Terzo Binario, RomaToday, **Il Messaggero Roma**, Il Giornale dei Castelli Romani) e di **ANSA Lazio**, le riviste giuridiche **Giurisprudenza Penale** e **Diritto.it** e ricerche mirate sulle **sentenze di Cassazione, tribunali, TAR, Consiglio di Stato e Corte dei conti** in materia di protezione civile (mai gli albi dei Comuni vicini) e apre la issue del giorno; la **Routine «Rassegna normativa e albo pretorio»** (dal 05/10/2026 tre giri, 07:52, 12:52 e 19:52 italiane, con tutte le fonti compresa la rassegna stampa) lavora ogni issue aperta e **pubblica fino a live** un articolo per ogni atto che riguarda la protezione civile direttamente o indirettamente — attivazioni COC comprese (istruzione permanente dell'utente 18/09/2026; rule 10 § omonimo). 🔴 Eccezione dall'08/10/2026: le notizie di stampa che raccontano interventi o attività del Gruppo restano in **PR non unita** finché l'utente non le confronta con il registro interventi.
- Modalità emergenza: `data/emergenza.json` → `"attiva": true`.
- Allerta meteo manuale: `data/allerta.json` → `livello: verde|giallo|arancione|rosso`, **insieme a `titolo` e `descrizione`** nella stessa modifica (cambiare solo `livello` produce una barra colorata e un CAP con severità coerenti ma titolo "NESSUNA ALLERTA" — verificato con un'esercitazione locale il 03/10/2026, dettagli in rule 10 § "Key operational notes").
- Niente articoli `draft: true`: solo pubblicato (data passata) o calendarizzato (data futura).
