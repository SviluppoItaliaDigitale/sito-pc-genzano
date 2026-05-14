# Sito Protezione Civile Genzano di Roma

Sito istituzionale del **Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma**.

- **Produzione**: https://www.protezionecivilegenzano.it/
- **Preview GitHub Pages**: https://sviluppoitaliadigitale.github.io/sito-pc-genzano/
- **Tecnologia**: [Hugo](https://gohugo.io/) (static site generator) + [Bootstrap Italia](https://italia.github.io/bootstrap-italia/) 2.x
- **Conformità**: AGID / Designers Italia, WCAG 2.2 AA
- **Deploy**: automatico a ogni push su `main` (GitHub Actions → Aruba via FTP + GitHub Pages)

---

## Guida ai file di documentazione (`.md`)

Questo repository contiene diversi file Markdown con ruoli diversi. Non vanno eliminati: ognuno ha una funzione operativa o di governance.

### File in root

| File | A cosa serve | Quando aprirlo |
|---|---|---|
| [`README.md`](README.md) | Panoramica del progetto, guida ai file, comandi principali. | Primo file da leggere. |
| [`MANUALE-SITO.md`](MANUALE-SITO.md) | **Indice del manuale operativo** (v3.0). Da maggio 2026 il manuale è split per Parti nella cartella [`manuale/`](manuale/) (1 file = 1 Parte). Questo file resta come indice/redirect. | Per orientarti fra le Parti. La singola Parte è poi in `manuale/parte-NN-*.md`. |
| [`manuale/`](manuale/) | **Manuale operativo split** (1 file per Parte): procedura articoli, regole AGID, immagini fascia blu, social, comunicati stampa, configurazione Claude Code, coach giochi + TTS, lettura accessibile. | Quando devi scrivere un articolo, gestire emergenza, configurare workflow ecc. Apri il file della Parte specifica. |
| [`MANUALE-MOBILE.md`](MANUALE-MOBILE.md) | **Workflow mobile-first** — guida per pubblicare articoli, modificare il sito, attivare emergenza, pubblicare sui social usando solo app Claude Android + GitHub web mobile. Niente PC. | Quando gestisci il sito dal telefono. |
| [`PIANO-EDITORIALE.md`](PIANO-EDITORIALE.md) | Fonti ufficiali da monitorare (DPC, INGV, ISPRA, Regione Lazio, ASL, Parco Castelli), calendario redazionale mensile e biblioteca di 250+ titoli evergreen. Obiettivo: tendere a un articolo al giorno (300-365/anno), minimo sostenibile 3-4 a settimana. | Quando devi proporre nuovi contenuti o cerchi ispirazione sulle fonti. |
| [`CLAUDE.md`](CLAUDE.md) | Istruzioni operative per Claude Code (o altra AI) — mandato, priorità, regole di qualità e sicurezza. Importa automaticamente le 11 regole in `.claude/rules/`. | Lettura automatica per ogni sessione AI. Va aggiornato solo se cambia la governance. |

### File in `.claude/rules/` (governance di dettaglio)

Questi 8 file sono importati automaticamente da `CLAUDE.md` e definiscono le regole operative per dominio. Non vanno eliminati.

| File | Dominio |
|---|---|
| [`01-governance-pa.md`](.claude/rules/01-governance-pa.md) | Riferimenti AGID, priorità, divieti assoluti. |
| [`02-content-design-pa.md`](.claude/rules/02-content-design-pa.md) | Scrittura PA, frontmatter articoli, fascia blu immagini, 13 categorie badge, regola foto utente (banner cover col titolo, foto nel corpo). |
| [`03-accessibility.md`](.claude/rules/03-accessibility.md) | Checklist WCAG 2.2 AA: HTML semantico, focus, alt text, contrasto, toolbar a11y, TTS, social media accessibility. |
| [`04-hugo-architecture.md`](.claude/rules/04-hugo-architecture.md) | Mappa generale: struttura del progetto, regole Hugo fondamentali, homepage dual-mode, articoli, comandi, divieti. Punta ai 3 file di dettaglio sotto. |
| [`04a-hugo-shortcode-partial.md`](.claude/rules/04a-hugo-shortcode-partial.md) | Shortcode (`foto`, `pittogramma`, `cosa-non-fare`, `chi-chiamare`, `pagina-emergenza-lite`), render hook tabelle/link, partial (article-cover, leggi-ad-alta-voce, articolo-navigazione, articoli-correlati, share buttons, modal SOS-112, striscia pittogrammi, FAQ accordion, **structured-data JSON-LD, meta-social Open Graph**), **assistente guidato `/assistente/`**. |
| [`04b-hugo-template-css.md`](.claude/rules/04b-hugo-template-css.md) | Menu di navigazione mega-menu, TOC, pagine legali con `dataUltimaRevisione`, regole stampa, tipografia `.article-body` v7.2, toolbar di accessibilità, sistema bozze social automatiche, pagina 404 istituzionale. |
| [`04c-hugo-static-cartelle.md`](.claude/rules/04c-hugo-static-cartelle.md) | Cartelle `static/` canoniche (manuali, allegati, comunicati, cartelli, immagini, pittogrammi), cartella `riferimenti-interni/` non deployata. |
| [`05-github-aruba-deploy.md`](.claude/rules/05-github-aruba-deploy.md) | Deploy CI/CD su Aruba e GitHub Pages, rollback, header HTTP, workflow scarica-foto-automatica, divieti. |
| [`06-protezione-civile-scientifica.md`](.claude/rules/06-protezione-civile-scientifica.md) | Codici colore allerte, rischi territoriali, numeri emergenza (NUE 112), comunicazione del rischio, gerarchia fonti. |
| [`07-proattivita-coerenza.md`](.claude/rules/07-proattivita-coerenza.md) | Verifica proattiva di pattern simili dopo ogni fix: completare il fix sul tutto, non solo dove richiesto. |
| [`08-claude-code-setup.md`](.claude/rules/08-claude-code-setup.md) | Setup ambiente Claude Code: sandbox `.claude/settings.local.json` per sblocco domini foto (7 fonti: Wikipedia, NASA, USGS, NOAA + Pexels, Pixabay, Unsplash). |

### Storie e Racconti per le scuole (`/formazione/storie-e-racconti/`)

**18 storie di qualità letteraria** per bambini 3-11 anni, distribuite per fascia d'età:

- **3-5 anni** (6 fiabe brevi, mascotte Tina la Tartaruga): autoprotezione di base con linguaggio semplice
- **6-8 anni** (6 racconti, protagonista Flavio o Flavia, attimo decisivo ispirato a campagna DPC *Attimo Decisivo*)
- **9-11 anni** (6 racconti più letterari su memoria, ricostruzione, volontariato tecnico, lessico PC)

Ogni storia ha:
- **Box "Cosa abbiamo imparato"** con 2-3 consigli pratici
- **"Per parlarne insieme"** (domande di comprensione)
- **"Per il/la docente — valore pedagogico"**: obiettivi di apprendimento, discipline coinvolte, competenze chiave europee, attività in classe, riferimenti curricolari (Indicazioni Nazionali 2012, L. 92/2019, D.Lgs. 1/2018, campagne DPC *Io non rischio* / *Attimo Decisivo*)
- **Bottone "🔊 Ascolta la storia"** che legge la fiaba ad alta voce in italiano via Web Speech API (browser-native, gratis, niente file MP3). Fondamentale per bambini che non leggono ancora bene, anziani che leggono con un nipote, persone con dislessia.

Le storie sono usabili come materiale didattico per l'educazione civica nelle scuole; il Gruppo apprezza la citazione nelle programmazioni.

### Coach didattico nei giochi (`/giochi/`)

Tutti i giochi della sezione **Giochi della Sicurezza** hanno un sistema di onboarding e teoria di rinforzo:

- **Bottone "💡 Consigli per giocare"** sotto il titolo: apre un dialog con la regola del gioco, "Come si gioca" e link alle pagine teoria del sito (rischi-prevenzione, numeri-utili, pittogrammi, ecc.).
- **Bottone "🔊 Ascolta i consigli"** dentro il dialog (Web Speech API).
- **Suggerimento contestuale su errore**: quando un bambino sbaglia, appare un riquadro con un suggerimento mirato e un link "Scopri perché →" alla teoria pertinente.

Pattern ispirato a campagna DPC "Io non rischio" e linee guida AGID per accessibilità cognitiva. Riduce l'abbandono dei bambini che giocano senza nozioni di base.

### Kit Calamità per categorie vulnerabili (`/formazione/kit-calamita/`)

Iniziativa autonoma del Gruppo (maggio 2026): **12 kit operativi A4 stampabili** per assistere persone particolarmente vulnerabili durante una calamità.

Hub centrale: `/formazione/kit-calamita/` — cruscotto cruscotto-style: il visitatore sceglie la propria situazione ("Sono...") e arriva in 1 click al kit giusto.

**12 kit pubblicati**:

| Kit | Standard adottati |
|---|---|
| 👧 Bambini 3-14 anni | NCTSN PFA Children + IFRC + WHO/UNHCR + Sphere 2018 |
| 👶 Neonati 0-3 anni | IFE Core Group v3.0 + WHO Code latte materno + Sphere |
| 👴 Anziani in casa | HelpAge International + WHO mhGAP + SIGG/AIP |
| 🤝 Caregiver familiari | L. 205/2017 + Carta Eurocarers 2014 + WHO Self-care 2022 |
| 🏥 Strutture sanitarie / RSA | Min. Salute + AGENAS + WHO Hospital Safety Index |
| ♿ Disabilità adulti | CRPD ONU art. 11 + L. 18/2009 + WHO Disability 2013 |
| 🩺 Terapie salvavita | WHO Health Cluster + Sphere § Essential health + ARERA 295/2018 |
| 🤰 Gravidanza e neomamme | MISP IAWG 2018 + WHO Pregnancy + UNFPA + Sphere |
| 🏚️ Senza fissa dimora | FEANTSA ETHOS + FIO.PSD + Min. Lavoro 2015 + Housing First |
| 🌐 Italiano L2 / stranieri | UNHCR CwC 2020 + IOM CCCM + Sphere § Communication |
| 🐕 Animali domestici | D.Lgs. 1/2018 art. 12 + L. 281/1991 + WSAVA |
| 🟢 Volontari PC (auto-cura) | IFRC Caring 2015 + NCTSN STS + WHO mhGAP + ProQOL-5 |

Ogni kit ha guida operatori + carte d'identità di emergenza compilabili + checklist evacuazione, tutto in formato A4 con font **eco-print URW Gothic L** (~30% inchiostro in meno di Arial). I giochi (cruciverba, sudoku) hanno la **soluzione capovolta** in fondo alla scheda (paradigma enigmistico).

Materiali **rilasciati gratuitamente**, liberi e riutilizzabili da altri Comuni/Gruppi PC. La citazione del nostro Gruppo è gradita ma non obbligatoria.

Specifiche complete in [`manuale/parte-20-kit-calamita-categorie-vulnerabili.md`](manuale/parte-20-kit-calamita-categorie-vulnerabili.md).

### Feed RSS pubblici (`/feed-rss/`)

Hugo genera **39 feed RSS** automaticamente, uno per sezione del sito (homepage, comunicazioni, allerte, rischi, formazione, glossario, standard ISO, ecc.). Tutti i feed sono live su Aruba (`https://www.protezionecivilegenzano.it/<sezione>/index.xml`) e auto-discoverable via `<link rel="alternate" type="application/rss+xml">` nell'`<head>` di ogni pagina.

A maggio 2026 è stata pubblicata una **pagina divulgativa** [`/feed-rss/`](content/feed-rss/_index.md) per cittadini e maintainer di altri Gruppi PC con: spiegazione di cosa sono i feed, 3 modi per iscriversi (aggregatori web, programmi desktop/mobile, browser), elenco dei 14 feed più utili, nota privacy (zero registrazione, zero cookie, zero dati personali). Voce **"Feed RSS"** nel **footer** del sito + nella **mappa-sito** + nell'**assistente virtuale** sotto "Servizi e documenti".

Standard tecnico: RSS 2.0 generato da Hugo, content-type `application/xml`. Nessuna configurazione manuale richiesta — Hugo li mantiene aggiornati a ogni build.

### Standard ISO per la Protezione Civile (`/standard-iso/`)

Hub permanente di consultazione (8 maggio 2026) con **30 schede brevi** sugli standard internazionali ISO rilevanti per la PC, organizzate per famiglia: **ISO/TC 292** emergency management (16 standard), **ISO 31000** risk management family (3), **ISO 14090** adattamento climatico (3), **ISO 7010** segnaletica (3), settori connessi (5: città resilienti, acqua, antincendio, sicurezza lavoro, GIS).

Ogni scheda spiega cosa è la norma, a chi serve, come si collega alla prassi italiana (D.Lgs. 1/2018, AGID, DPC, normativa di settore).

**Vincolo copyright**: gli ISO sono norme a pagamento, le schede contengono solo titolo, ambito e contestualizzazione italiana — mai testo della norma. Per il dettaglio si rinvia a [iso.org](https://www.iso.org/) e al [catalogo UNI](https://store.uni.com/).

Accompagnano l'hub **10 news divulgative** calendarizzate dal 12 maggio al 12 giugno 2026 sui 10 ISO più utili al cittadino: 22324 (codici colore allerta), 22322 (public warning + IT-alert), 22329 (social in emergenza), 22361 (gestione crisi), 22398 (esercitazioni), 22395 (persone vulnerabili), 31000 (gestione rischio), 22327 (allerta frane), 7010 (segnaletica), 14090 (adattamento clima).

### Aggiornamenti contenuti didattici e prevenzione (maggio 2026)

Sessione di consolidamento del 6 maggio 2026 con esiti strutturali sul sito.

**Nuove pagine di prevenzione**:

- [`content/rischi-prevenzione/scuole-genzano-rischi-locali.md`](content/rischi-prevenzione/scuole-genzano-rischi-locali.md) — pagina di raccordo tra scuola, famiglie, rischi locali e materiali didattici. Non contiene dati inventati su singoli istituti: rimanda ai piani interni e al Piano Comunale.
- [`content/rischi-prevenzione/rischi-in-parole-semplici.md`](content/rischi-prevenzione/rischi-in-parole-semplici.md) — versione semplificata dei rischi principali per bambini, BES, persone con disabilità cognitive e parlanti italiano L2.
- [`content/rischi-prevenzione/kit-emergenza-economico-progressivo.md`](content/rischi-prevenzione/kit-emergenza-economico-progressivo.md) — guida per costruire il kit poco alla volta, senza marchi, negozi o prodotti sponsorizzati.

**Schede didattiche aggiornate** (`static/formazione/kit-calamita-bambini/`): lavaggio completo delle mani (rinominato dal vecchio "5 passi"), unisci i puntini casco PC, mandala del sole.

**Regole editoriali consolidate**:

- Nei contenuti istituzionali non si indicano marchi commerciali, negozi o prodotti sponsorizzati.
- Le pagine rivolte alle scuole non inventano dati su istituti, indirizzi, referenti o procedure interne: rimandano sempre al piano del singolo istituto e alle fonti ufficiali.
- La mappa manuale del sito si aggiorna quando si pubblicano nuove pagine informative importanti. Il `sitemap.xml` tecnico resta generato da Hugo.

**Drift documentale corretto**: `14° COI` allineato in tutti i file, bandiera SPQR errata rimossa dall'articolo Reggio Emilia 1996, caption ShakeMap INGV corrette in 5 articoli storici, duplicato editoriale Amatrice 2016 risolto. Asset -2.85 MB ottimizzati.

Specifiche complete in [`manuale/parte-21-aggiornamenti-contenuti-didattici-prevenzione.md`](manuale/parte-21-aggiornamenti-contenuti-didattici-prevenzione.md).

### Iniziative roadmap (maggio 2026)

Blocco di 13 iniziative dalla roadmap di evoluzione del sito (libreria prompt in `riferimenti-interni/PROMPT-ROADMAP-PC-GENZANO.md`):

- **#24 Ricerca Pagefind** — ricerca full-text con modal `Ctrl+K`; indice `static/pagefind/` rigenerato da `scripts/genera-indice-ricerca.sh`.
- **#21 Glossario interattivo** — filtri alfabetici + ricerca live sulla pagina `/glossario/`.
- **#25 Stato del sistema** — pagina `/stato-sistema/`, cruscotto di trasparenza tecnica con semaforo, alimentato da `aggiorna-stato-sistema.yml`.
- **#22 Podcast** — `/podcast/` con episodi MP3 + feed RSS iTunes; la vecchia pagina TTS si è spostata su `/articoli-da-ascoltare/`.
- **#8 Storia del territorio** — timeline `/storia/` dei Castelli Romani, voci con fonte istituzionale (`data/eventi_storici.yaml`).
- **#5 Assistente vocale** — input vocale (`SpeechRecognition`) nell'`/assistente/`.
- **#4 Modalità Lanterna** — `/lanterna/`, pagina standalone ultra-leggera (torcia, bussola, Wake Lock, 112 sticky).
- **#10 Contenuti LIS** — `/lis/` + badge "Disponibile in LIS" su pagine con `lis_video:` nel frontmatter (`data/lis.yaml`).
- **#2 Notifiche allerta browser** — opt-in su `/allerte-meteo/`, polling dell'endpoint JSON `/allerta-stato/`, senza Service Worker.
- **#7 Quiz "Quanto sei preparato?"** — `/quiz-preparazione/`, quiz adattivo con badge PNG e stampa.
- **#11 Hub "Arena PC Genzano"** — `/giochi/` ridisegnato come launcher (skin Arena/Classica, badge progressi, "continua").
- **#6 QR articoli** + **Open Data** reinserita (`/open-data/`).
- Più: agent `pc-site-auditor`, workflow `backup-documenti-aruba.yml`, fix pipeline Telegram allerta.

Architettura di dettaglio nella tabella "Architettura — riferimenti rapidi" di [`CLAUDE.md`](CLAUDE.md) e nelle rules `.claude/rules/04a` / `04b`. Riepilogo operativo in [`manuale/parte-29-iniziative-roadmap.md`](manuale/parte-29-iniziative-roadmap.md).

### File in `archetypes/` (template Hugo)

| File | A cosa serve |
|---|---|
| [`archetypes/comunicazioni.md`](archetypes/comunicazioni.md) | Template frontmatter per nuovi articoli (`hugo new comunicazioni/AAAA-MM-GG-titolo.md`). |
| [`archetypes/default.md`](archetypes/default.md) | Template minimale per pagine generiche. |

### File in `content/` (contenuti pubblicati)

- `content/comunicazioni/*.md` — articoli e news. Uno per file, frontmatter + corpo Markdown.
- `content/<sezione>/_index.md` — pagine statiche (una per sezione del sito).

---

## Struttura del progetto

```
sito-pc-genzano/
├── README.md                   ← sei qui
├── MANUALE-SITO.md             ← indice del manuale (v3.0) — split in manuale/
├── manuale/                    ← file Parte (split da maggio 2026, 1 file = 1 Parte)
│   ├── README.md               ← indice navigabile
│   └── parte-NN-*.md           ← 1 file per Parte (redazione articoli, AGID,
│                                 immagini, social, comunicati, deploy, ecc.)
├── MANUALE-MOBILE.md           ← workflow mobile-first (app + GitHub web)
├── PIANO-EDITORIALE.md         ← fonti e calendario redazionale
├── CLAUDE.md                   ← istruzioni per AI (importa .claude/rules/)
├── hugo.toml                   ← configurazione Hugo
│
├── .claude/rules/              ← 11 regole di governance (01-08, 04 split a/b/c)
├── .github/workflows/          ← 17 workflow CI/CD e controlli periodici
├── .manuale/sources-hashes.json ← stato hash fonti AGID (gestito dal workflow)
│
├── archetypes/                 ← template per nuovi contenuti
│   ├── comunicazioni.md        ← frontmatter articoli completo
│   └── default.md              ← template minimale pagine
│
├── content/                    ← contenuti del sito (Markdown + frontmatter)
│   ├── comunicazioni/          ← articoli/news (uno per file)
│   └── <altre-sezioni>/        ← pagine statiche (chi-siamo, contatti, faq,
│                                  rischi-prevenzione, cosa-fare-adesso,
│                                  formazione, area-download, allerte-meteo,
│                                  diventa-volontario, accessibilita, ecc.)
│
├── data/                       ← file dati (JSON/YAML) per contenuti dinamici
│   ├── emergenza.json          ← modalità emergenza on/off
│   ├── allerta.json            ← livello allerta meteo
│   ├── risk_cards.yaml         ← 9 card rischi
│   ├── numeri_utili.yaml       ← numeri emergenza
│   ├── quick_links.yaml        ← CTA homepage
│   ├── social_links.yaml       ← link social
│   ├── codici_colore.yaml      ← descrizioni codici allerta
│   ├── glossario.yaml          ← voci glossario inline (sigle PC)
│   ├── aree_emergenza.yaml     ← 16 punti del Piano Emergenza (verified)
│   ├── idranti.yaml            ← idranti antincendio territorio (template)
│   └── dae.yaml                ← DAE territorio (template, registro IRC)
│
├── scripts/                    ← script Python/bash di automazione
│   ├── genera-cover.py             ← cover tipografica con titolo (gradiente blu)
│   ├── auto-cover-mancanti.py      ← genera cover per articoli con image:""
│   ├── applica-fascia-foto.{py,sh} ← applica fascia blu istituzionale a foto
│   ├── audit-grammatica-italiana.py ← audit testuale italiano (40 sez. workflow)
│   ├── fix-grammatica-italiana.py  ← fix automatici sicuri (apostrofi, accenti)
│   ├── genera-social.{py,sh}       ← bozze X/FB/IG/Telegram via Gemini API
│   ├── genera-immagini-social.py   ← immagini Instagram (post + carosello + story)
│   ├── foto-da-wikipedia.sh        ← download foto da Wikipedia + fascia blu
│   ├── foto-da-nasa.sh             ← idem da NASA Image Library
│   ├── foto-da-usgs.sh             ← idem da USGS (ShakeMap eventid)
│   ├── foto-da-noaa.sh             ← idem da NOAA (URL diretto)
│   ├── aggiorna-frontmatter-foto.py ← popola image:/credit:/source_url:
│   ├── scarica-pittogrammi.sh      ← libreria pittogrammi ISO 7010+ARASAAC
│   ├── smoke-test-live.sh          ← smoke test post-deploy (chiamato da CI)
│   ├── hash-fonte-agid.py          ← hashing testuale fonti AGID per drift detection
│   └── export-contesto-ai.sh       ← genera CONTESTO-AI.md per altre AI
│
├── static/                     ← asset statici (deployati al pubblico)
│   ├── images/                 ← copertine articoli + foto evento
│   ├── manuali/                ← PDF, manuali tecnici, loghi e locandine ufficiali
│   │   ├── loghi/              ← stemmi/loghi del Gruppo per personalizzazioni
│   │   └── locandine/          ← locandine ufficiali (es. Diventa Volontario)
│   ├── pittogrammi/            ← pittogrammi ISO 7010 + ARASAAC
│   ├── cartelli/               ← segnaletica aree di emergenza
│   ├── giochi/, quizpc/, formazionepc/, abili-a-proteggere/, giochi-bambini/
│   │                              ← micro-siti HTML autonomi educativi/didattici
│   ├── allegati/               ← PDF allegati specifici di articoli
│   ├── comunicati/             ← comunicati stampa firmati
│   ├── formazione/             ← schede stampabili, kit didattici
│   ├── .htaccess               ← redirect 301/410 + header sicurezza Aruba
│   └── robots.txt              ← regole indicizzazione (sincronizzato col tema)
│
├── social-bozze/               ← bozze testuali AI per i social (NON deployata)
│   └── <slug>/                 ← per ogni articolo: x.txt, facebook.txt,
│                                  instagram.txt, telegram.txt + README
│
├── riferimenti-interni/        ← documentazione di lavoro (NON deployata,
│                                  visibile solo nel repo: norme copyrighted,
│                                  draft consultazioni, materiale interno)
│
└── themes/flavour-pcgenzano/   ← tema custom (Bootstrap Italia 2.x)
    ├── layouts/                ← template Hugo
    │   ├── _default/           ← baseof, list, single, 404, _markup hooks
    │   ├── partials/           ← navbar, footer, banner, sos-112, share, ecc.
    │   ├── shortcodes/         ← {{< foto >}}, {{< pittogramma >}},
    │   │                          {{< cosa-non-fare >}}, {{< chi-chiamare >}},
    │   │                          {{< pagina-emergenza-lite >}}
    │   ├── comunicazioni/      ← list.html (archivio + filtri + accordion anni)
    │   ├── assistente/         ← albero decisionale autoprotezione
    │   └── pittogrammi/        ← catalogo pubblico libreria
    └── static/                 ← asset deployati col tema
        ├── css/custom.css      ← override CSS + @media print + tipografia v7.2
        ├── css/a11y-toolbar.css ← FAB strumenti accessibilità
        ├── js/                 ← share.js, a11y-toolbar.js, ecc.
        ├── .htaccess           ← regole Apache (replicato in static/ root)
        └── robots.txt          ← (sincronizzato con static/robots.txt)
```

---

## Comandi principali

### Dev server e build

```bash
hugo server              # solo contenuti pubblicati
hugo server -D           # anche bozze (draft: true)
hugo --minify            # build per GitHub Pages
hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"  # build Aruba
```

### Nuovo articolo

```bash
# Crea articolo dall'archetype
hugo new comunicazioni/AAAA-MM-GG-titolo-articolo.md

# Genera cover tipografica con titolo grande (per articoli con image:"")
python3 scripts/auto-cover-mancanti.py

# Pubblica
git add . && git commit -m "..." && git push
```

> 🤖 **Se redigi con Claude Code (CLI/mobile/cloud/agent):** il workflow ha un **gate AGID obbligato** prima del `git add` — Claude invoca automaticamente l'agent `pc-article-reviewer` sul file appena scritto e applica i fix di linguaggio AGID livello ChatGPT 9.5/10 (frasi <20 parole, voce attiva, sigle sciolte, fonti istituzionali, badge corretto). Eccezione: se chiedi esplicitamente un comunicato stampa, una lettera istituzionale, un paper scientifico o **qualsiasi altro documento in registro non-AGID**, il gate è sospeso e Claude applica le convenzioni di genere. Specifiche in `CLAUDE.md` § *"Auto-gate AGID prima del commit di un nuovo articolo"*.

### Foto

```bash
# Cover tipografica banner (gradiente blu + titolo) — generata automatica
# se l'articolo ha image:"". MAI sostituita da foto, la cover serve per
# Open Graph (anteprima social) e fallback emergenza. Vedi CLAUDE.md punto 9.
python3 scripts/auto-cover-mancanti.py

# Per inserire una foto INLINE nel corpo articolo (Wikipedia/NASA/foto utente):
# chiedi a Claude in italiano (es. "trovami una foto gratuita per X" oppure
# "ecco una foto, mettila nell'articolo Y") — l'agent pc-image-fixer fa
# WebFetch (per fonti web) + applica fascia blu + shortcode {{< foto >}}
# inline nel corpo. NON usare il marker # TODO-foto-* nel frontmatter
# (bandito dopo incidente del 3 maggio 2026: viene reso da Hugo come H1
# in produzione + sovrascrive il banner).

# Comandi shell singoli (per chi preferisce eseguire a mano):
bash scripts/applica-fascia-foto.sh /path/foto.jpg <nome-DIVERSO-da-slug>
# Output: static/images/<nome>.webp (1200px, fascia blu, max 200KB)
# Poi inserisci manualmente {{< foto src="/images/<nome>.webp" alt="..." caption="..." >}}
```

### Bozze social

```bash
# Genera bozze X/Facebook/Instagram/Telegram + immagini IG per UN articolo
bash scripts/genera-social.sh content/comunicazioni/<file>.md

# Tutti gli articoli pubblicati senza bozze
bash scripts/genera-social.sh --all

# Solo articoli da una data in poi
bash scripts/genera-social.sh --since 2026-04-01

# Solo anteprima senza salvare
bash scripts/genera-social.sh --dry-run <file>.md
# Richiede GEMINI_API_KEY in env (gratuita: aistudio.google.com/apikey).
```

### Versione Braille degli articoli (BRF)

```bash
# Prerequisito una sola volta (Ubuntu/Debian):
sudo apt-get install -y python3-louis liblouis-data python3-yaml

# Genera/aggiorna i .brf di tutti gli articoli (idempotente: skip se up-to-date)
python3 scripts/genera-braille.py

# Solo i primi N (utile per test)
python3 scripts/genera-braille.py --limit 10

# Forza rigenerazione completa
python3 scripts/genera-braille.py --force

# Solo un articolo specifico
python3 scripts/genera-braille.py --article 2026-05-12-iso-22324-codici-colore-allerta

# Output: static/braille/comunicazioni/<slug>.brf (ASCII puro, BRF/ICEB-compliant)
# Tabella: it-it-comp6.utb (braille italiano 6 punti standard, output ASCII).
# Per display braille e stampanti braille (Index, ViewPlus). UICI Roma + BIC Monza
# leggono nativamente questo formato. Specifiche: manuale/parte-24-output-braille-articoli.md
```

### Pagina Podcast + Scarica trascrizione PDF (P15)

Pagina automatica `/podcast/` con elenco di tutti gli articoli ascoltabili + durata stimata audio (`ReadingTime × 1.33`). Su ogni articolo c'è anche un bottone "Scarica trascrizione PDF" che chiama `window.print()` — il sito ha già un CSS `@media print` globale che produce stampa pulita senza chrome.

Niente da generare a mano: la pagina podcast si aggiorna automaticamente ad ogni build Hugo (gli articoli con TTS attivo + WordCount > 30 entrano nella lista). Specifiche complete: `manuale/parte-26-podcast-pdf-trascrizione.md`.

### Versione "italiano semplice" (A2 CEFR) — workflow on-demand (P16)

Per articoli ad alta priorità (bollettini allerta, procedure autoprotezione, ISO densi) si può affiancare una versione semplificata in italiano L2 livello A2 CEFR.

```bash
# Convenzione: file affiancati nella stessa cartella
content/comunicazioni/<slug>.md          # versione completa AGID
content/comunicazioni/<slug>-facile.md   # versione italiano semplice A2

# Frontmatter incrociato:
# Sull'articolo completo:  versione_facile: "<slug>-facile"
# Sull'articolo facile:    versione_facile_di: "<slug>"
```

Hugo genera due pagine distinte. Un banner giallo in cima a ciascuna permette di passare all'altra. Eccezione gate AGID: NON invocare `pc-article-reviewer` sui file `*-facile.md` (è registro CEFR A2 deliberato, non AGID). Articolo campione live: ISO 22324. Specifiche: `manuale/parte-25-italiano-l2-versione-facile.md`.

### Audit grammaticale italiano

```bash
# Rileva errori ortografici/grammaticali (apostrofi finti, accenti mancanti, refusi)
python3 scripts/audit-grammatica-italiana.py

# Applica fix automatici sicuri (e' → è, piu' → più, città', perché, ecc.)
python3 scripts/fix-grammatica-italiana.py            # dry-run (default)
python3 scripts/fix-grammatica-italiana.py --apply    # applica
```

### Gestione e contesto

```bash
# Script interattivo di gestione (menu per articoli, emergenza, allerta)
bash ~/gestione-sito.sh

# Export contesto completo per altra AI (ChatGPT, Gemini, Claude web)
bash scripts/export-contesto-ai.sh
# → Genera CONTESTO-AI.md nella root con TUTTA la documentazione del sito
#   in un unico file, pronto da copia-incollare in qualsiasi altra AI per
#   avere continuità di gestione senza perdere nulla.
```

---

## Continuità su altra AI o altra sessione

Per lavorare sul sito con un'AI diversa (ChatGPT, Gemini, Claude web) o in una
nuova sessione dove non si ha accesso automatico ai file del repo, esiste uno
**script di export** che raccoglie tutta la documentazione in un singolo file:

```bash
bash scripts/export-contesto-ai.sh
```

Produce `CONTESTO-AI.md` (~300 KB) contenente:
- README, CLAUDE.md, 11 regole di governance (`.claude/rules/01-08` con 04a/b/c)
- Manuale operativo completo (indice `MANUALE-SITO.md` + file `manuale/parte-NN.md`) + `MANUALE-MOBILE.md`
- Piano editoriale (fonti + calendario + biblioteca evergreen)
- Archetype articoli, configurazione Hugo, shortcode (`foto`, `pittogramma`, `cosa-non-fare`, `chi-chiamare`)
- Memorie utente (feedback durevoli salvati da Claude Code)

Basta copiare il contenuto di `CONTESTO-AI.md` e incollarlo come primo messaggio
nell'altra AI per avere continuità operativa senza perdere contesto.

Il file è `.gitignore`d perché si rigenera on-demand dallo stato corrente del repo.

---

## Automazioni attive (GitHub Actions)

Tutti i workflow di manutenzione girano **ogni lunedì** (primo giorno della settimana), scaglionati in orari diversi per ridurre il carico sul runner.

| Workflow | Frequenza | Scopo |
|---|---|---|
| `deploy.yml` | Ogni push su `main` | Build + deploy Aruba (FTP) + GitHub Pages |
| `check-allerta.yml` | **Doppio trigger fail-safe**: cron-job.org ogni 5 min (primario, ~15 sec latenza) + GitHub schedule `17 * * * *` (fail-safe orario) | **Pipeline a tre script** (refactor 13/05/2026): (a) `check-allerta.py` — criticità idrogeologica/idraulica (CSV opendatasicilia + fallback PDF Regione Lazio, MAX time-aware oggi+domani, fuso Europe/Rome dinamico); (b) `check-avvisi-meteo.py` — avvisi vento/neve/calore (PDF Regione Lazio); (c) `check-rischi-incendi.py` — rischio AIB Zona 9 = Genzano (PDF Regione Lazio, campagna giugno-ottobre). Commit unico combinato se almeno uno modifica `data/allerta.json`. |
| `pubblica-programmata.yml` | Giornaliero 06:00 UTC | Pubblica articoli programmati |
| `lighthouse-audit.yml` | Post-deploy | Audit performance/accessibilità/SEO |
| `smoke-test-post-deploy.yml` | Post-deploy | Smoke test live: status HTTP, marker JS, header sicurezza |
| `aggiorna-manuale.yml` | Lunedì 06:00 UTC | Hash fonti AGID/Designers Italia → issue se cambiano |
| `update-bootstrap-italia.yml` | Lunedì 06:00 UTC | Aggiornamenti Bootstrap Italia |
| `audit-sito.yml` | Lunedì 09:00 UTC | **Audit completo (40 sezioni)**: contenuti, codice/template, governance docs, audit aggiuntivo, link critici normativa, **audit grammaticale italiano** (apostrofi finti, accenti mancanti, errori italiani tipici via `audit-grammatica-italiana.py`). Fusi `coerenza-docs.yml` + `check-normativa-links.yml` il 26 aprile 2026, sezione 40 grammaticale aggiunta il 29 aprile 2026. |
| `check-links-sito.yml` | Lunedì 10:00 UTC | Crawl completo lychee: tutti i link (interni + esterni) |
| `genera-social-bozze.yml` | Push su `content/comunicazioni/**.md` o `.claude/rules/**.md` (o `workflow_dispatch`) | Genera bozze post X/Facebook/Instagram/Telegram via Gemini API + immagini Instagram (post 1080x1080 + carosello + story 1080x1920). Output **tutto insieme** in `social-bozze/<slug>/` (testi e immagini). Tier gratuito Gemini, costo zero. |
| `scarica-foto-automatica.yml` | Push su `content/comunicazioni/**` o sui suoi script foto | Step 2 attivo: cover tipografica auto col titolo per articoli con `image:""` (`auto-cover-mancanti.py` + protezione regenerate-missing). **Step 1 marker `# TODO-foto-*` deprecato** dal 3 maggio 2026 (CLAUDE.md punto 9: il marker veniva reso da Hugo come H1 in produzione + sovrascriveva il banner col foto, contro la regola "BANNER COL TITOLO INTOCCABILE"). Per inserire foto da fonti ufficiali nel corpo articolo, usare l'agent `pc-image-fixer` (procedura WebFetch + curl + applica-fascia + shortcode `{{< foto >}}` inline). |

Le issue generate automaticamente compaiono nella [tab Issues](https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/issues) con label `manutenzione`, `documentazione`, `link-rotti`, ecc.

---

## Regole permanenti chiave

Il progetto ha alcune regole non negoziabili da avere a portata di vista:

- **Banner articoli** = **sempre cover tipografica con titolo grande** (gradiente blu + badge categoria + titolo articolo + fascia istituzionale). Generata da `scripts/auto-cover-mancanti.py`. Mai vuota in produzione, mai una foto utente.
- **Foto fornite dall'utente** = sempre nel **corpo dell'articolo** come `{{< foto >}}` (mai nel campo `image:` del frontmatter). ≥4 foto → galleria nel corpo. Sui social diventano automaticamente carosello Instagram.
- **NUE 112** è l'unico numero di emergenza nel Lazio: 115/118/1515 non vanno mai citati come numeri da chiamare al cittadino.
- **14° COI** della Provincia di Roma (non 15°) è il riferimento del Gruppo.
- **Formato data nel frontmatter**: sempre `AAAA-MM-GG`. Mai con timezone (`AAAA-MM-DDTHH:MM:SSZ` causa esclusione dell'articolo dalla build).
- **Nessun articolo `draft: true`** — solo pubblicazione immediata (data passata) o programmata (data futura).
- **Lingua AGID**: frasi brevi (max ~20 parole), voce attiva, niente burocratese, linguaggio inclusivo.

Specifiche complete in [CLAUDE.md](CLAUDE.md) e nelle 11 regole `.claude/rules/`.

---

## Flusso di lavoro tipico per pubblicare un articolo

1. Apri [`manuale/parte-01-scrivere-un-articolo-passo-per-passo.md`](manuale/parte-01-scrivere-un-articolo-passo-per-passo.md) (procedura completa) o [`MANUALE-SITO.md`](MANUALE-SITO.md) (indice).
2. Identifica lo slug: `AAAA-MM-GG-titolo-breve`.
3. Esegui `hugo new comunicazioni/AAAA-MM-GG-titolo-breve.md`.
4. Compila il frontmatter (vedi Parte 1.5 del manuale): `image: ""` (cover tipografica generata dopo).
5. Scrivi il corpo seguendo le regole AGID (Parte 2 del manuale).
6. Foto evento: inseriscile **nel corpo** con `{{< foto >}}` (Parte 3.14) — nome file diverso dallo slug. Per articoli storici con eventi multipli (anniversari, memoria, sequenze sismiche): 1ª foto dopo 1° H2, 2ª dopo 2° H2, ecc. (Parte 14.9). Mai foto nel banner `image:`.
7. Genera la cover tipografica col titolo: `python3 scripts/auto-cover-mancanti.py` (popola automaticamente `image:` con la cover).
8. (Opzionale) Verifica audit grammaticale: `python3 scripts/audit-grammatica-italiana.py` → se restituisce findings, lancia `python3 scripts/fix-grammatica-italiana.py --apply`.
9. Verifica con `hugo server` in locale.
10. Esegui la checklist pre-pubblicazione (Parte 5).
11. `git add . && git commit -m "Nuovo articolo: titolo" && git push`.
12. Al push automaticamente: deploy + bozze social generate (Gemini API) + immagini Instagram. Risultato **tutto insieme** in `social-bozze/<slug>/` (4 .txt + `instagram-post*.jpg` + `instagram-story.jpg`) entro 5–10 minuti.
13. Controlla il deploy nella tab Actions.

---

## Pubblicare da mobile (senza PC)

Workflow completo in [`MANUALE-MOBILE.md`](MANUALE-MOBILE.md): app **Claude Android** + **GitHub web mobile**. Niente PC, niente git clone.

In sintesi:
- L'articolo si scrive direttamente su GitHub web (modifica un file in `content/comunicazioni/` o crearne uno nuovo).
- Banner: lasciare `image: ""` vuoto, la cover tipografica viene generata automaticamente al deploy.
- Per inserire una foto inline nel corpo: chiedi a Claude (app Android) di trovartene una gratuita pertinente — l'agent `pc-image-fixer` cerca su Wikipedia/NASA/USGS, scarica, applica fascia blu, e inserisce shortcode `{{< foto >}}` nel corpo. **Non usare** il marker `# TODO-foto-*` nel frontmatter (bandito dopo incidente 3 maggio 2026).
- Bozze social e immagini Instagram vengono generate automaticamente al push.

---

## Contatti

- Repository: [github.com/SviluppoItaliaDigitale/sito-pc-genzano](https://github.com/SviluppoItaliaDigitale/sito-pc-genzano)
- Sito pubblico: [protezionecivilegenzano.it](https://www.protezionecivilegenzano.it/)
- Email istituzionale: vedi pagina [Contatti](https://www.protezionecivilegenzano.it/contatti/)

---

## Licenza e diritti

Contenuti testuali: © Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.
Codice del tema: vedi `themes/flavour-pcgenzano/`.
Riferimenti normativi: AGID, Designers Italia, Dipartimento Protezione Civile.
