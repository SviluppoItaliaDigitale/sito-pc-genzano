# Manuale Operativo — Sito Protezione Civile Genzano di Roma

**Versione:** 3.3
**Ultimo aggiornamento manuale:** 2026-05-10
**Roadmap 8-item ROI:** completata 2026-05-10 (Lighthouse 95/100/100/100, Telegram allerta, cron 7,22,37,52, schede offline 299, dichiarazione AGID conforme, scheletri Trasparenza+Open Data+Mappa territorio).
**Ultimo check linee guida AGID:** 2026-04-20
**Manuale operativo di design PA:** versione 2025.1
**Bootstrap Italia:** versione 2.17.3
**WCAG di riferimento:** 2.2 livello AA
**Hugo di riferimento:** 0.143.x extended

> **🗂️ Manuale spezzato in 19 file (maggio 2026)** — A maggio 2026 il manuale è stato
> diviso in file separati nella cartella [`manuale/`](manuale/) (1 file per Parte) per
> facilitare manutenzione, revisioni puntuali e diff PR più leggibili. Questo file resta
> come **indice/redirect** per i riferimenti esterni che citano "MANUALE-SITO.md Parte N".

---

## 📚 Indice delle Parti

| # | Argomento | File |
|---|---|---|
| Parte 0 | Come usare questo manuale | [`manuale/parte-00-come-usare-questo-manuale.md`](manuale/parte-00-come-usare-questo-manuale.md) |
| Parte 1 | Scrivere un articolo passo per passo | [`manuale/parte-01-scrivere-un-articolo-passo-per-passo.md`](manuale/parte-01-scrivere-un-articolo-passo-per-passo.md) |
| Parte 2 | Le regole AGID in dettaglio | [`manuale/parte-02-le-regole-agid-in-dettaglio.md`](manuale/parte-02-le-regole-agid-in-dettaglio.md) |
| Parte 3 | Immagini per gli articoli (fascia blu, shortcode `foto`, pittogrammi, fonti libere) | [`manuale/parte-03-immagini-per-gli-articoli.md`](manuale/parte-03-immagini-per-gli-articoli.md) |
| Parte 4 | Scrivere una pagina (diverso da articolo) | [`manuale/parte-04-scrivere-una-pagina-diverso-da-articolo.md`](manuale/parte-04-scrivere-una-pagina-diverso-da-articolo.md) |
| Parte 5 | Checklist pre-pubblicazione | [`manuale/parte-05-checklist-pre-pubblicazione.md`](manuale/parte-05-checklist-pre-pubblicazione.md) |
| Parte 6 | Procedura di aggiornamento manuale | [`manuale/parte-06-procedura-di-aggiornamento-manuale.md`](manuale/parte-06-procedura-di-aggiornamento-manuale.md) |
| Parte 7 | Aggiornamento automatico settimanale | [`manuale/parte-07-aggiornamento-automatico-settimanale.md`](manuale/parte-07-aggiornamento-automatico-settimanale.md) |
| Parte 8 | Modificare e cancellare contenuti | [`manuale/parte-08-modificare-e-cancellare-contenuti.md`](manuale/parte-08-modificare-e-cancellare-contenuti.md) |
| Parte 9 | File dati `data/` e stati del sito (`emergenza.json`, `allerta.json`, ecc.) | [`manuale/parte-09-file-dati-data-e-stati-del-sito.md`](manuale/parte-09-file-dati-data-e-stati-del-sito.md) |
| Parte 10 | GitHub Actions e automazioni | [`manuale/parte-10-github-actions-e-automazioni.md`](manuale/parte-10-github-actions-e-automazioni.md) |
| Parte 11 | Testi per i social (Instagram, Facebook, X, Telegram) | [`manuale/parte-11-testi-per-i-social-instagram-facebook-x-telegram.md`](manuale/parte-11-testi-per-i-social-instagram-facebook-x-telegram.md) |
| Parte 12 | Comunicati stampa (tempo ordinario e tempo emergenziale) | [`manuale/parte-12-comunicati-stampa-tempo-ordinario-e-tempo-emergenziale.md`](manuale/parte-12-comunicati-stampa-tempo-ordinario-e-tempo-emergenziale.md) |
| Parte 13 | Social Media Policy pubblica (gerarchia fonti AGID/DPC/CNR/EENA/ISO) | [`manuale/parte-13-social-media-policy-pubblica.md`](manuale/parte-13-social-media-policy-pubblica.md) |
| Parte 14 | Configurazione ambiente di sviluppo (Claude Code, sandbox, foto API) | [`manuale/parte-14-configurazione-ambiente-di-sviluppo-claude-code.md`](manuale/parte-14-configurazione-ambiente-di-sviluppo-claude-code.md) |
| Parte 15 | Homepage enhancements v1.0 (aprile 2026) | [`manuale/parte-15-homepage-enhancements-v1-0-aprile-2026.md`](manuale/parte-15-homepage-enhancements-v1-0-aprile-2026.md) |
| Parte 16 | Bozze social: gestione quota Gemini API | [`manuale/parte-16-bozze-social-gestione-quota-gemini-api.md`](manuale/parte-16-bozze-social-gestione-quota-gemini-api.md) |
| Parte 17 | Coach didattico nei giochi e TTS esteso (maggio 2026) | [`manuale/parte-17-coach-didattico-nei-giochi-e-tts-esteso-maggio-2026.md`](manuale/parte-17-coach-didattico-nei-giochi-e-tts-esteso-maggio-2026.md) |
| Parte 18 | Lettura accessibile per fasce deboli: TTS dappertutto, glossario inline, tempo lettura, sillabazione (maggio 2026) | [`manuale/parte-18-lettura-accessibile-maggio-2026.md`](manuale/parte-18-lettura-accessibile-maggio-2026.md) |
| Parte 19 | Agenti specializzati Claude Code (maggio 2026) — 7 profili professionali virtuali per redazione, immagini, issue, deploy, social, QA schede stampabili, audit di sistema | [`manuale/parte-19-agenti-specializzati.md`](manuale/parte-19-agenti-specializzati.md) |
| Parte 20 | Kit Calamità per categorie vulnerabili (maggio 2026) — 12 kit operativi A4 stampabili (bambini, anziani, RSA, disabilità, neonati, gravidanza, animali, caregiver, terapie salvavita, senza dimora, italiano L2, volontari PC) basati su standard internazionali NCTSN, IFRC, WHO, Sphere, FEANTSA, UNHCR, IOM, IFE, MISP, WSAVA, Eurocarers | [`manuale/parte-20-kit-calamita-categorie-vulnerabili.md`](manuale/parte-20-kit-calamita-categorie-vulnerabili.md) |
| Parte 21 | Aggiornamenti contenuti didattici e prevenzione (maggio 2026) — 3 nuove pagine prevenzione, regole scuole/kit/marchi commerciali, sessione consolidamento del 6 maggio (24 commit, 343 file ripuliti, asset -2.85 MB, glossario 61→82 voci, COC sede Comando Polizia Locale, icone H2 su 15 pagine lunghe) | [`manuale/parte-21-aggiornamenti-contenuti-didattici-prevenzione.md`](manuale/parte-21-aggiornamenti-contenuti-didattici-prevenzione.md) |
| Parte 22 | Icone Bootstrap nei titoli H2 delle pagine lunghe (maggio 2026) — pattern editoriale per alleggerire visivamente la lettura. Vocabolario standardizzato concetto→icona, integrazione automatica col TOC, vincolo `{#slug}` per anchor puliti | [`manuale/parte-22-icone-h2-pagine-lunghe.md`](manuale/parte-22-icone-h2-pagine-lunghe.md) |
| Parte 23 | Trigger esterno cron-job.org per allerta meteo (10 maggio 2026) — architettura doppio trigger fail-safe: cron-job.org primario ogni 5 min via API GitHub `workflow_dispatch` (latenza ~15 sec end-to-end) + GitHub schedule `17 * * * *` paracadute orario. Setup PAT fine-grained, secret `CRONJOB_GH_PAT`, workflow auto-promemoria scadenza | [`manuale/parte-23-cronjob-org-trigger-esterno-allerta.md`](manuale/parte-23-cronjob-org-trigger-esterno-allerta.md) |
| Parte 24 | Output Braille-ready per gli articoli — BRF (12 maggio 2026, **FEATURE COMPLETA** Sere 1+2+3) — Sera 1: script Python `scripts/genera-braille.py` (liblouis + `it-it-comp6.utb`, idempotente, CLI ricca, preprocessing Markdown + shortcode). Sera 2: integrazione `deploy.yml` con apt-install + step generazione pre-build (output in `public/braille/comunicazioni/`). Sera 3: partial `scarica-braille.html` + bottone "Scarica versione braille" su ogni articolo (visibile solo se il `.brf` esiste, guardia `fileExists`). Test accettazione UICI/BIC pianificato giugno 2026 | [`manuale/parte-24-output-braille-articoli.md`](manuale/parte-24-output-braille-articoli.md) |
| Parte 25 | Versione "italiano semplice" (A2 CEFR) per gli articoli (12 maggio 2026) — Punto 16 roadmap. Coppia di file affiancati `<slug>.md` (versione completa) + `<slug>-facile.md` (versione italiano L2 A2), frontmatter incrociato `versione_facile` / `versione_facile_di`. Partial `versione-facile-toggle.html` con banner giallo sopra l'articolo che linka tra le due. Eccezione gate AGID documentata. Articolo campione live: ISO 22324 + versione facile. Per parlanti italiano L2, persone con disabilità cognitive, anziani, chi legge in fretta | [`manuale/parte-25-italiano-l2-versione-facile.md`](manuale/parte-25-italiano-l2-versione-facile.md) |
| Parte 26 | "Articoli da ascoltare" (TTS) + Scarica trascrizione PDF (12 maggio 2026) — Punto 15 roadmap. ⚠️ La pagina degli articoli ascoltabili via TTS, in origine `/podcast/`, è stata **spostata su `/articoli-da-ascoltare/`** (maggio 2026, idea #22): `/podcast/` ora ospita il podcast vero con episodi MP3 (vedi Parte 29). Elenco articoli ascoltabili + durata stimata audio (`ReadingTime × 1.33`). Bottone "Scarica trascrizione PDF" sopra ogni articolo (chiama `window.print()`). Niente MP3, niente feed RSS, niente costi runtime | [`manuale/parte-26-podcast-pdf-trascrizione.md`](manuale/parte-26-podcast-pdf-trascrizione.md) |
| Parte 27 | Archivio `/comunicazioni/` — design senza paginazione (12 maggio 2026) — documenta lo "pseudo-bug" ricorrente in audit: il template `comunicazioni/list.html` NON usa `.Paginator`, mostra tutti i ~104 articoli pubblicati raggruppati per mese con filter-pills JS per categoria/anno. 4 ragioni del design choice (no friction scroll-to-load, filtri client-side immediati, indice mese navigabile, SEO senza JS). Trigger di rivalutazione: ~300 articoli visibili (~aprile-maggio 2027) | [`manuale/parte-27-archivio-comunicazioni-design.md`](manuale/parte-27-archivio-comunicazioni-design.md) |
| Parte 28 | Markup Schema.org / JSON-LD per SEO + rich result Google (12 maggio 2026) — 9 tipi attivi (Organization+NGO, ContactPoint, WebSite+SearchAction, Article, Event, FAQPage, HowTo, BreadcrumbList, WebPage) generati da un solo partial `structured-data.html` context-aware. Vincolo `Organization+NGO` (NON `GovernmentOrganization`/`EmergencyService`) confermato. HowTo su tutte le 8 pagine `/rischi-prevenzione/*` con frontmatter `howto_prima/durante/dopo`. Sintassi critica `\| jsonify \| safeJS` documentata | [`manuale/parte-28-schema-org-markup.md`](manuale/parte-28-schema-org-markup.md) |
| Parte 29 | Iniziative roadmap (maggio 2026) — riepilogo operativo delle 13 iniziative roadmap implementate in blocco: ricerca Pagefind (#24), glossario interattivo (#21), stato del sistema (#25), podcast con RSS + spostamento pagina TTS (#22), timeline storica (#8), assistente vocale (#5), modalità Lanterna (#4), contenuti LIS (#10), notifiche allerta browser (#2), quiz preparazione (#7), hub Arena giochi (#11), QR articoli (#6), Open Data reinserita. Per ogni feature: cosa fa, dove vive, come si rigenera. Architettura di dettaglio nella tabella di `CLAUDE.md` e nelle rules `04a`/`04b` | [`manuale/parte-29-iniziative-roadmap.md`](manuale/parte-29-iniziative-roadmap.md) |
| Parte 30 | Materiali pronti NotebookLM (`/risorse-pronte/`) — workflow completo dalla preparazione del pacchetto sul Desktop alla pubblicazione live sul sito. 8 passi operativi, agent dedicato `pc-notebooklm-publisher`, workflow CI `aggiorna-indice-ricerca.yml`, troubleshooting, licenza CC BY-NC-SA 4.0 | [`manuale/parte-30-materiali-pronti-notebooklm.md`](manuale/parte-30-materiali-pronti-notebooklm.md) |

> 👉 **[Vai all'indice completo del manuale (`manuale/README.md`)](manuale/README.md)**

---

## 🔍 Cerca per argomento

Se non sai in quale Parte cercare:

| Vuoi… | Vai a |
|---|---|
| Scrivere un nuovo articolo | [Parte 1](manuale/parte-01-scrivere-un-articolo-passo-per-passo.md) → [Parte 2](manuale/parte-02-le-regole-agid-in-dettaglio.md) → [Parte 3](manuale/parte-03-immagini-per-gli-articoli.md) → [Parte 5](manuale/parte-05-checklist-pre-pubblicazione.md) |
| 🤖 Auto-gate AGID Claude Code (obbligato pre-commit) | [Parte 5](manuale/parte-05-checklist-pre-pubblicazione.md) → [Parte 19](manuale/parte-19-agenti-specializzati.md) § 19.1 + `CLAUDE.md` § *"Auto-gate AGID prima del commit"* |
| Comunicato stampa o altro documento NON-AGID con Claude | [Parte 12](manuale/parte-12-comunicati-stampa-tempo-ordinario-e-tempo-emergenziale.md) — eccezione registro su richiesta esplicita |
| Mettere la fascia blu su una foto | [Parte 3](manuale/parte-03-immagini-per-gli-articoli.md) § 3.8 Metodo 4 |
| Pittogrammi ISO 7010 / ARASAAC | [Parte 3](manuale/parte-03-immagini-per-gli-articoli.md) § 3.16 |
| Scaricare foto da Wikipedia/NASA/USGS/NOAA/Pexels/Pixabay/Unsplash | [Parte 3](manuale/parte-03-immagini-per-gli-articoli.md) + [Parte 14](manuale/parte-14-configurazione-ambiente-di-sviluppo-claude-code.md) |
| Modificare il livello allerta meteo | [Parte 9](manuale/parte-09-file-dati-data-e-stati-del-sito.md) § 9.3 |
| Attivare modalità emergenza | [Parte 9](manuale/parte-09-file-dati-data-e-stati-del-sito.md) § 9.1 |
| Capire un workflow GitHub Actions | [Parte 10](manuale/parte-10-github-actions-e-automazioni.md) |
| Pubblicare su Instagram/Facebook/X/Telegram | [Parte 11](manuale/parte-11-testi-per-i-social-instagram-facebook-x-telegram.md) |
| Comunicato stampa in emergenza | [Parte 12](manuale/parte-12-comunicati-stampa-tempo-ordinario-e-tempo-emergenziale.md) |
| Gerarchia fonti DPC/CNR/EENA per crisi sui social | [Parte 13](manuale/parte-13-social-media-policy-pubblica.md) § 13.7 + 13.9 |
| Configurare Claude Code (sandbox, API keys) | [Parte 14](manuale/parte-14-configurazione-ambiente-di-sviluppo-claude-code.md) |
| Avviare Claude Code o il menu di gestione (alias + icone desktop) | [Parte 14](manuale/parte-14-configurazione-ambiente-di-sviluppo-claude-code.md) § 14.10 |
| Coach dei giochi + TTS audio + fiabe | [Parte 17](manuale/parte-17-coach-didattico-nei-giochi-e-tts-esteso-maggio-2026.md) |
| TTS dappertutto + glossario inline + tempo lettura + sillabazione | [Parte 18](manuale/parte-18-lettura-accessibile-maggio-2026.md) |
| Aggiungere voce al glossario inline (popover sui termini PC) | [Parte 18](manuale/parte-18-lettura-accessibile-maggio-2026.md) § 18.9 |
| Vincoli copyright sulle definizioni del glossario (Treccani NO) | [Parte 18](manuale/parte-18-lettura-accessibile-maggio-2026.md) § 18.10 |

---

## 📜 Changelog

> **3.1 (2026-05-02) — Lettura accessibile per fasce deboli**
> Cinque strumenti integrati per anziani, dislessici, italiano L2, bambini in
> lettura lenta, persone in stress da emergenza:
> - TTS "Leggi ad alta voce" **default ON su tutto il sito** (logica invertita
>   da opt-in a opt-out — blacklist legali/tecniche)
> - Selettore velocità (Lento 0.75x / Normale 0.95x / Veloce 1.15x), persistito
>   in localStorage
> - ~~Toggle "Segui parole" che evidenzia la parola in lettura~~ — **rimosso il
>   2 maggio 2026**: dipende da `SpeechSynthesisUtterance.onboundary 'word'`
>   che Chrome/Edge non emettono con voci cloud Google (default), feature
>   invisibile per la maggioranza degli utenti italiani
> - Tempo di lettura stimato sopra ogni articolo (`Lettura: ~N minuti`)
> - Sillabazione automatica `hyphens: auto` con regole italiane
> - Glossario inline con popover sui termini PC alla prima occorrenza (61 voci
>   in `data/glossario.yaml`, definizioni nostre AGID — vincolo copyright:
>   nessuna copia da Treccani)
> Specifiche complete in nuova **Parte 18**.

> **3.0 (2026-05-01) — Manuale spezzato per Parti**
> - Il manuale era diventato un singolo file di ~5500 righe / 290 KB (troppo grande
>   per editing comodo). È stato spezzato per Parte in `manuale/parte-{NN}-{slug}.md`
>   (1 file = 1 Parte).
> - `manuale/README.md` è il nuovo indice navigabile della documentazione.
> - Questo file `MANUALE-SITO.md` resta come indice/redirect per i riferimenti
>   esterni che citano "MANUALE-SITO.md Parte N".
> - Specifiche complete dello split + nuova **Parte 17** (Coach giochi + TTS) in
>   [`manuale/parte-17-coach-didattico-nei-giochi-e-tts-esteso-maggio-2026.md`](manuale/parte-17-coach-didattico-nei-giochi-e-tts-esteso-maggio-2026.md).

> **2.9 (2026-04-28) — Anteprime social link**
> Estratti i meta tag Open Graph + Twitter Card in partial dedicato `meta-social.html`,
> completati con tutti i campi raccomandati 2026 (og:image:secure_url, og:image:type,
> width/height, alt; article:published_time, modified_time, author, section, tag;
> twitter:image:alt). Refresh cache via Facebook Sharing Debugger e Twitter Card Validator.

> **2.8 (2026-04-27) — Share buttons privacy-first**
> Aggiunti bottoni share (WhatsApp/Telegram/Facebook/X/LinkedIn/Email/Copia/Condividi
> nativo) in `partials/page-tools.html`. Solo link "share intent" + Clipboard API + Web
> Share API native: niente JavaScript SDK, niente tracker, conforme AGID + GDPR.

> **2.7 (2026-04-27) — Configurazione Claude Code (Parte 14)**
> Documentato `.claude/settings.local.json` per sandbox + 9 fonti foto libere. Nuova
> regola `.claude/rules/08-claude-code-setup.md`.

> **2.6 (2026-04-27) — Cartella `riferimenti-interni/`**
> Cartella per documentazione di lavoro NON deployata (norme copyrighted, draft,
> materiale interno). Indice in `riferimenti-interni/README.md`.

> **2.5 (2026-04-27) — Allerta + comunicazione di crisi**
> Campo `ultimo_controllo` separato in `allerta.json` (max 4 commit/giorno). Nuova
> Parte 13.7 "Comunicazione di crisi sui social" allineata a ISO 22329:2021 + CWA
> CEN/CENELEC. Gerarchia fonti normative riorganizzata in livelli (Parte 13.9).

> **2.4 (2026-04-24) — Kit scuola** (Parte 4.8) — struttura didattica completa.
> **2.3 (2026-04-22) — Holding statement** + Parte 13 Social Media Policy pubblica.
> **2.2 (2026-04-21) — Parte 11 social** + **Parte 12 comunicati stampa**.
> **2.1 (2026-04-21) — Parte 8 contenuti** + **Parte 9 data files** + **Parte 10 workflow**.

Per il changelog completo storico (2.0 e precedenti) vedi i singoli file in [`manuale/`](manuale/).

---

## ❓ Domande non coperte

Per domande non coperte qui, apri un'Issue sul repository o contatta il Chief Digital
Officer del Gruppo.

Per altre AI o sessioni nuove: [`CONTESTO-AI.md`](CONTESTO-AI.md) (auto-generato da
`scripts/export-contesto-ai.sh`) contiene tutto in un unico file pronto da incollare.
