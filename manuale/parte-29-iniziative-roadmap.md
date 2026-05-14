_[Indice manuale](README.md)_

# Parte 29 — Iniziative roadmap (maggio 2026)

A maggio 2026 è stato implementato in blocco un gruppo di **13 iniziative** dalla roadmap di evoluzione del sito (libreria dei prompt in `riferimenti-interni/PROMPT-ROADMAP-PC-GENZANO.md`).

Questa Parte è il **riepilogo operativo**: per ogni feature, cosa fa, dove vive, come si mantiene. L'architettura tecnica di dettaglio è nella tabella *"Architettura — riferimenti rapidi"* di `CLAUDE.md` e nelle rules `.claude/rules/04a-hugo-shortcode-partial.md` e `04b-hugo-template-css.md`.

---

## 29.1 Ricerca full-text Pagefind (#24)

Ricerca interna full-text con modal accessibile, scorciatoia **Ctrl+K**, copertura delle 7 traduzioni.

- **Pagine**: modal su tutto il sito (`partials/ricerca-modal.html`), pagina a tutta pagina `/cerca/`.
- **Indice**: `static/pagefind/` — **va rigenerato** quando pubblichi nuovi articoli, con `bash scripts/genera-indice-ricerca.sh`. Senza rigenerazione i nuovi articoli non compaiono nei risultati (restano comunque raggiungibili da menu e link). Vedi anche **Parte 1, Passo 1.13-ter**.

## 29.2 Glossario interattivo (#21)

La pagina `/glossario/` ha una barra di **filtri alfabetici** A-Z e un campo di **ricerca live**. Enhancement progressivo: senza JavaScript resta la pagina statica A-Z. JS in `static/js/glossario-pagina.js`. Le voci restano in `data/glossario.yaml` e `content/glossario/_index.md`.

## 29.3 Stato del sistema (#25)

Pagina pubblica `/stato-sistema/`: cruscotto di trasparenza tecnica — stato di allerta, modalità del sito, automazioni di manutenzione con **semaforo** verde/giallo/rosso, conformità. I dati dei workflow stanno in `data/stato-sistema.json`, aggiornato ogni giorno dal workflow `aggiorna-stato-sistema.yml`.

## 29.4 Podcast con feed RSS (#22)

`/podcast/` ospita ora il **podcast vero** con episodi audio MP3 e **feed RSS iTunes-compatible** (`/podcast/index.xml`), distribuibile su Spotify/Apple.

⚠️ **Spostamento importante**: la vecchia pagina `/podcast/` (articoli ascoltabili via TTS) è stata spostata su **`/articoli-da-ascoltare/`**. Nuovi episodi: `hugo new podcast/episodio-NN-titolo.md` (archetipo `archetypes/podcast.md`), MP3 caricato come asset di una GitHub Release. Prima della distribuzione: sostituire `static/images/podcast-cover.png` con una copertina curata e compilare `podcast_spotify`/`podcast_apple` nel frontmatter di `content/podcast/_index.md`.

## 29.5 Timeline storica del territorio (#8)

Pagina `/storia/`: linea del tempo dei Castelli Romani (natura vulcanica, terremoti storici, evoluzione della protezione civile). Le voci stanno in `data/eventi_storici.yaml` — **ogni voce DEVE avere una fonte istituzionale verificabile** (niente contenuti non verificati).

## 29.6 Assistente vocale (#5)

L'`/assistente/` ha un bottone microfono: l'utente fa una domanda **a voce** (Web Speech API `SpeechRecognition`), la trascrizione confluisce nella ricerca dell'assistente, un riepilogo è letto ad alta voce. Niente IA esterna, niente backend. Nota privacy esplicita in pagina.

## 29.7 Modalità Lanterna (#4)

Pagina `/lanterna/`: pagina **standalone ultra-leggera** (~7 KB, non usa il layout del sito) di sopravvivenza — torcia, bussola, schermo sempre acceso (Wake Lock), 112 sticky in alto. Pensata per poca batteria, rete debole, di notte. Linkata da `/emergenza/`.

## 29.8 Contenuti in LIS (#10)

Sistema per i video in **Lingua Italiana dei Segni**. La pagina `/lis/` elenca i video; una pagina mostra il badge "Disponibile in LIS" se ha `lis_video: "<id>"` nel frontmatter, con `<id>` definito in `data/lis.yaml`. I video (da produrre con interprete LIS qualificato) andranno su GitHub Releases. Ogni voce ha trascrizione testuale completa.

## 29.9 Notifiche allerta browser (#2)

Su `/allerte-meteo/` c'è un opt-in per ricevere **notifiche del browser** quando l'allerta sale ad arancione/rosso. Polling dell'endpoint pubblico `/allerta-stato/index.json` (generato da `content/allerta-stato/`). **Senza Service Worker** (la PWA è vietata): funziona solo a scheda aperta, dichiarato chiaramente nell'opt-in.

## 29.10 Quiz "Quanto sei preparato?" (#7)

Pagina `/quiz-preparazione/`: quiz **adattivo** (le domande si ramificano in base alla situazione dichiarata) che produce un profilo di preparazione + un piano d'azione personalizzato. Badge PNG scaricabile (canvas) e versione stampabile. Tutto in localStorage, nessun dato raccolto.

## 29.11 Hub "Arena PC Genzano" (#11)

L'hub `/giochi/` è ora un **launcher** con tutti i giochi a colpo d'occhio, badge di progresso per gioco, "continua dove avevi lasciato", filtri per fascia. Doppia skin **Arena** (gaming) / **Classica** (sobria, default se `prefers-reduced-motion`). Legge il catalogo da `progressione.js`. File: `static/giochi/assets/{css/arena.css,js/arena.js}`.

## 29.12 QR articoli (#6) e Open Data

- **QR articoli**: ogni articolo ha un bottone "Scarica QR" (in `page-tools`). I QR stanno in `static/qr/`, rigenerati da `scripts/genera-qr-articoli.py` (vedi **Parte 1, Passo 1.13-bis**).
- **Open Data**: la pagina `/open-data/` (dataset delle attività del Gruppo in CSV/JSON, CC BY 4.0) è stata reinserita nel dropdown Risorse.

## 29.13 Manutenzione collaterale

- **Agent `pc-site-auditor`**: audit di sito interattivo on-demand (vedi Parte 19).
- **Workflow `backup-documenti-aruba.yml`**: backup mensile dei documenti che vivono solo sul server Aruba.
- **Fix pipeline Telegram allerta**: `check-allerta.yml` ora triggera esplicitamente `notifica-telegram.yml` (i push del `GITHUB_TOKEN` non auto-triggerano i workflow).

---

## 29.14 Cosa ricordare

- Dopo aver pubblicato articoli, **rigenera l'indice di ricerca** (`scripts/genera-indice-ricerca.sh`) e i **QR** (`scripts/genera-qr-articoli.py`).
- Ogni nuova voce di menu va aggiunta **sia in `hugo.toml` sia in `static/app-shared/site-chrome.js`**.
- Il dropdown **Risorse** è cresciuto molto (13 voci): se in futuro diventa ingestibile, valutare una riorganizzazione (vedi rule `04b` § menu).
- Le pagine/feature con "infrastruttura pronta, contenuto da completare": podcast (episodi), LIS (video), timeline (altre voci), open-data (dataset reali).
