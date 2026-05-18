# MANUALE-SITO — Manuale operativo (split)

Manuale operativo completo del sito Protezione Civile Genzano di Roma.
Diviso per Parti (1 file = 1 Parte) per facilità di manutenzione e revisione.

## Indice delle Parti

| # | Argomento | File |
|---|---|---|
| Parte 00 | Come usare questo manuale | [`parte-00-come-usare-questo-manuale.md`](parte-00-come-usare-questo-manuale.md) |
| Parte 01 | Scrivere un articolo passo per passo | [`parte-01-scrivere-un-articolo-passo-per-passo.md`](parte-01-scrivere-un-articolo-passo-per-passo.md) |
| Parte 02 | Le regole AGID in dettaglio | [`parte-02-le-regole-agid-in-dettaglio.md`](parte-02-le-regole-agid-in-dettaglio.md) |
| Parte 03 | Immagini per gli articoli | [`parte-03-immagini-per-gli-articoli.md`](parte-03-immagini-per-gli-articoli.md) |
| Parte 04 | Scrivere una pagina (diverso da articolo) | [`parte-04-scrivere-una-pagina-diverso-da-articolo.md`](parte-04-scrivere-una-pagina-diverso-da-articolo.md) |
| Parte 05 | Checklist pre-pubblicazione | [`parte-05-checklist-pre-pubblicazione.md`](parte-05-checklist-pre-pubblicazione.md) |
| Parte 06 | Procedura di aggiornamento manuale | [`parte-06-procedura-di-aggiornamento-manuale.md`](parte-06-procedura-di-aggiornamento-manuale.md) |
| Parte 07 | Aggiornamento automatico settimanale | [`parte-07-aggiornamento-automatico-settimanale.md`](parte-07-aggiornamento-automatico-settimanale.md) |
| Parte 08 | Modificare e cancellare contenuti | [`parte-08-modificare-e-cancellare-contenuti.md`](parte-08-modificare-e-cancellare-contenuti.md) |
| Parte 09 | File dati `data/` e stati del sito | [`parte-09-file-dati-data-e-stati-del-sito.md`](parte-09-file-dati-data-e-stati-del-sito.md) |
| Parte 10 | GitHub Actions e automazioni | [`parte-10-github-actions-e-automazioni.md`](parte-10-github-actions-e-automazioni.md) |
| Parte 11 | Testi per i social (Instagram, Facebook, X, Telegram) | [`parte-11-testi-per-i-social-instagram-facebook-x-telegram.md`](parte-11-testi-per-i-social-instagram-facebook-x-telegram.md) |
| Parte 12 | Comunicati stampa (tempo ordinario e tempo emergenziale) | [`parte-12-comunicati-stampa-tempo-ordinario-e-tempo-emergenziale.md`](parte-12-comunicati-stampa-tempo-ordinario-e-tempo-emergenziale.md) |
| Parte 13 | Social Media Policy pubblica | [`parte-13-social-media-policy-pubblica.md`](parte-13-social-media-policy-pubblica.md) |
| Parte 14 | Configurazione ambiente di sviluppo (Claude Code) | [`parte-14-configurazione-ambiente-di-sviluppo-claude-code.md`](parte-14-configurazione-ambiente-di-sviluppo-claude-code.md) |
| Parte 15 | Homepage enhancements v1.0 (aprile 2026) | [`parte-15-homepage-enhancements-v1-0-aprile-2026.md`](parte-15-homepage-enhancements-v1-0-aprile-2026.md) |
| Parte 16 | Bozze social: gestione quota Gemini API | [`parte-16-bozze-social-gestione-quota-gemini-api.md`](parte-16-bozze-social-gestione-quota-gemini-api.md) |
| Parte 17 | Coach didattico nei giochi e TTS esteso (maggio 2026) | [`parte-17-coach-didattico-nei-giochi-e-tts-esteso-maggio-2026.md`](parte-17-coach-didattico-nei-giochi-e-tts-esteso-maggio-2026.md) |
| Parte 18 | Lettura accessibile per fasce deboli: TTS dappertutto, glossario inline, tempo lettura, sillabazione (maggio 2026) | [`parte-18-lettura-accessibile-maggio-2026.md`](parte-18-lettura-accessibile-maggio-2026.md) |
| Parte 19 | Agenti specializzati Claude Code (maggio 2026) — **15 agent custom `pc-*`** (al 18 maggio 2026): caporedattore AGID, accessibility auditor IAAP CPACC, content freshness, italiano L2 A2, internal linker SEO, SEO checker, avvocato verificatore norme, art director immagini fascia blu, issue triage, release engineer pre-push, comunicazione di crisi social, QA schede stampabili, site auditor, gate visivo foto multimodale, publisher NotebookLM. Complementari alle skill globali (Parte 31). | [`parte-19-agenti-specializzati.md`](parte-19-agenti-specializzati.md) |
| Parte 20 | Kit Calamità per categorie vulnerabili (maggio 2026) — 12 kit operativi A4 stampabili (bambini, anziani, RSA, disabilità, neonati, gravidanza, animali, caregiver, terapie salvavita, senza dimora, italiano L2, volontari PC) basati su standard internazionali NCTSN, IFRC, WHO, Sphere, FEANTSA, UNHCR, IOM, IFE, MISP, WSAVA, Eurocarers | [`parte-20-kit-calamita-categorie-vulnerabili.md`](parte-20-kit-calamita-categorie-vulnerabili.md) |
| Parte 21 | Aggiornamenti contenuti didattici e prevenzione (maggio 2026) — 3 nuove pagine prevenzione, regole scuole/kit/marchi commerciali, sessione di consolidamento del 6 maggio (24 commit, 343 file ripuliti, asset -2.85 MB, glossario 61→82 voci, COC sede Comando Polizia Locale, icone H2 su 15 pagine lunghe) | [`parte-21-aggiornamenti-contenuti-didattici-prevenzione.md`](parte-21-aggiornamenti-contenuti-didattici-prevenzione.md) |
| Parte 22 | Icone Bootstrap nei titoli H2 delle pagine lunghe (maggio 2026) — pattern editoriale per alleggerire visivamente la lettura. Vocabolario standardizzato concetto→icona, integrazione automatica col TOC, vincolo `{#slug}` per anchor puliti | [`parte-22-icone-h2-pagine-lunghe.md`](parte-22-icone-h2-pagine-lunghe.md) |
| Parte 23 | Trigger esterno cron-job.org per allerta meteo (10 maggio 2026) — architettura doppio trigger fail-safe: cron-job.org primario ogni 5 min via API GitHub `workflow_dispatch` (latenza ~15 sec end-to-end) + GitHub schedule `17 * * * *` paracadute orario. Setup PAT fine-grained, secret `CRONJOB_GH_PAT`, workflow auto-promemoria scadenza | [`parte-23-cronjob-org-trigger-esterno-allerta.md`](parte-23-cronjob-org-trigger-esterno-allerta.md) |
| Parte 24 | Output Braille-ready per gli articoli — BRF (12 maggio 2026, **FEATURE COMPLETA** Sere 1+2+3) — script `scripts/genera-braille.py` (liblouis + `it-it-comp6.utb`), integrazione `deploy.yml` con apt-install + step generazione pre-build, partial `scarica-braille.html` con bottone "Scarica versione braille" su ogni articolo (guardia `fileExists`). Test accettazione UICI/BIC giugno 2026 | [`parte-24-output-braille-articoli.md`](parte-24-output-braille-articoli.md) |
| Parte 25 | Versione "italiano semplice" (A2 CEFR) per gli articoli (12 maggio 2026) — Punto 16 roadmap. File affiancati `<slug>.md` + `<slug>-facile.md`, frontmatter `versione_facile` / `versione_facile_di`, partial `versione-facile-toggle.html` con banner giallo. Eccezione gate AGID. Articolo campione: ISO 22324 + facile | [`parte-25-italiano-l2-versione-facile.md`](parte-25-italiano-l2-versione-facile.md) |
| Parte 26 | Pagina Podcast + Scarica trascrizione PDF (12 maggio 2026) — Punto 15 roadmap. Pagina `/podcast/` con elenco articoli + durata audio (`ReadingTime × 1.33`), voce menu sotto Risorse (sync Hugo + site-chrome.js), bottone "Scarica trascrizione PDF" che chiama `window.print()`. Niente MP3, niente feed RSS, niente costi runtime | [`parte-26-podcast-pdf-trascrizione.md`](parte-26-podcast-pdf-trascrizione.md) |
| Parte 27 | Archivio `/comunicazioni/` — design senza paginazione (12 maggio 2026) — `comunicazioni/list.html` NON usa `.Paginator`, mostra tutti i ~104 articoli raggruppati per mese con filter-pills JS per categoria/anno. 4 ragioni del design choice (no scroll-to-load, filtri client-side, indice mese navigabile, SEO senza JS). Trigger rivalutazione: ~300 articoli visibili | [`parte-27-archivio-comunicazioni-design.md`](parte-27-archivio-comunicazioni-design.md) |
| Parte 28 | Markup Schema.org / JSON-LD per SEO + rich result Google (12 maggio 2026) — 9 tipi attivi generati da `structured-data.html` context-aware. Vincolo `Organization+NGO` (no `GovernmentOrganization`). HowTo su tutte le 8 pagine `/rischi-prevenzione/*`. Sintassi critica `\| jsonify \| safeJS` per evitare doppio escape JS dentro `<script>` | [`parte-28-schema-org-markup.md`](parte-28-schema-org-markup.md) |
| Parte 29 | Iniziative roadmap (maggio 2026) — riepilogo iniziative chiave: quiz preparazione, hub LIS, modalità lanterna, notifiche allerta browser, ricerca Pagefind, QR articoli, stato sistema, podcast, ecc. | [`parte-29-iniziative-roadmap.md`](parte-29-iniziative-roadmap.md) |
| Parte 30 | Materiali pronti NotebookLM (16 maggio 2026) — pipeline pubblicazione automatica per podcast/infografiche/presentazioni Google NotebookLM. Drop zone `~/Scrivania/notebooklm-output/<tema>/`, script `pubblica-notebooklm-output.py`, cross-link auto, hub `/risorse-pronte/` | [`parte-30-materiali-pronti-notebooklm.md`](parte-30-materiali-pronti-notebooklm.md) |
| Parte 31 | **Skill globali Claude Code: invocazione obbligata col tool `Skill`** (18 maggio 2026) — ~100 skill installate in `~/.claude/skills/` post cleanup conservativo (da 269). Politica per usarle attivamente invece di lasciarle dormienti: scan a inizio task ≥3 step, routing rapido (accessibility, SEO, Python, test, git, ricerca, audit, security, plan, error handling, browser). Co-uso con agent custom `pc-*` in sequenza. Eccezioni e divieti. **Da leggere insieme alla Parte 19.** | [`parte-31-skill-globali-invocazione.md`](parte-31-skill-globali-invocazione.md) |

---

## Storia

Il manuale era un singolo file `MANUALE-SITO.md` di ~5500 righe. A maggio 2026
è stato spezzato per file di Parte (1 file = 1 Parte) per facilitare:
- editing puntuale (modifica della Parte 14 senza scrollare 5500 righe)
- diff PR più leggibili
- caricamento più rapido in editor di testo

Il file `MANUALE-SITO.md` nella root del repo resta come indice/redirect.
