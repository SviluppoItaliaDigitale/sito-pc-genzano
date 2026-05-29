# Parte 35 — Conoscere la Protezione Civile (`/conoscere/`)

*Aggiunta: 29 maggio 2026.*

## Cos'è

Un **livello dottrinale** del sito: la protezione civile spiegata **come materia**, non come servizio operativo. Risponde alla domanda «come funziona il sistema, e perché?», mentre le pagine operative (`/cosa-fare-adesso/`, `/rischi-prevenzione/`, `/allerte-meteo/`, `/cartografia/`, `/piano-emergenza/`) rispondono a «cosa faccio?».

È un livello **additivo**: nessuna pagina esistente è stata rimossa o spostata. Ogni pagina di `/conoscere/` rimanda alle pagine operative corrispondenti, così la teoria resta collegata alla pratica.

## Pagine della sezione

| URL | Contenuto |
|---|---|
| `/conoscere/` | Landing: a chi serve, indice delle pagine, backlog dei temi futuri. |
| `/conoscere/servizio-nazionale/` | Componenti (art. 4), strutture operative (art. 13), livelli Stato/Regioni/Comuni, ruolo del Sindaco (art. 12). |
| `/conoscere/le-quattro-fasi/` | Panoramica delle 4 attività (art. 2) + modello del rischio **R = P × V × E**. |
| `/conoscere/le-quattro-fasi/previsione/` | Fase 1 — sapere prima cosa può accadere. |
| `/conoscere/le-quattro-fasi/prevenzione/` | Fase 2 — ridurre vulnerabilità ed esposizione. |
| `/conoscere/le-quattro-fasi/soccorso/` | Fase 3 — gestione dell'emergenza; catena COC→COM→CCS→DiComaC. |
| `/conoscere/le-quattro-fasi/superamento/` | Fase 4 — stato di emergenza (art. 24, durata 12+12 mesi), AeDES, *build back better*. |
| `/conoscere/telecomunicazioni-emergenza/` | Reti radio, radioamatori, IT-alert. |
| `/conoscere/telecomunicazioni-emergenza/rete-zamberletti/` | La Rete Radio nazionale di emergenza, frequenze, eredità di Zamberletti. |
| `/conoscere/rischio-vulcanico-colli-albani/` | Il Vulcano Laziale: storia eruttiva, laghi di Albano/Nemi, emissioni di gas, monitoraggio INGV. Pagina "materia" affiancata alla pagina operativa `/rischi-prevenzione/rischio-vulcanico/`. |

## Standard editoriale

- **Ogni fatto normativo verificato su fonte primaria** (Normattiva, D.Lgs. 1/2018 artt. 2, 4, 7, 12, 13, 24, 25) o istituzionale (DPC, INGV, Ministero dell'Interno, UNDRR). Niente numeri di articolo "a memoria".
- **Disclaimer divulgativo** (`alert alert-info`) su ogni pagina: il Gruppo non parla a nome di DPC/Regione; in emergenza vale il 112.
- **Data di revisione** nel frontmatter (`dataUltimaRevisione`).
- File di lavoro non pubblicati (`_FONTI-DA-VERIFICARE.md`, `_PR-DESCRIPTION.md`) esclusi via `build: { render: never, list: never }`.

## Dove è agganciata (scopribilità)

Quando si aggiunge o modifica una pagina in `/conoscere/`, mantenere allineati **tutti** questi punti:

1. **Menu Hugo** — `hugo.toml`, dropdown `identifier = "conoscere"` (voce di primo livello, peso 2, dopo Home).
2. **Menu pagine statiche** — `static/app-shared/site-chrome.js`, blocco `navDropdown-conoscere` (sincronizzazione obbligatoria con `hugo.toml`, vedi rule 04b).
3. **Assistente virtuale** — `themes/flavour-pcgenzano/layouts/assistente/list.html`, ramo `info_conoscere` (card nel menu `mode_informa` + nodi `info_conoscere_*`).
4. **Mappa del sito** — `content/mappa-sito/_index.md`, sezione "Conoscere la Protezione Civile".
5. **README** e **questo manuale**.

## Come aggiungere una nuova pagina dottrinale

1. Crea `content/conoscere/<slug>.md` (o sottocartella `<tema>/_index.md`) con frontmatter `layout: "single"`, `toc: true`, `dataUltimaRevisione`.
2. Apri con un paragrafo divulgativo + disclaimer `alert alert-info`.
3. Scrivi il corpo citando **solo** fonti verificate, con link. Se un fatto non è verificabile in sessione, marcalo `<!-- FONTE-DA-VERIFICARE: ... -->` e NON pubblicarlo come certo.
4. Chiudi con "Approfondimenti sul nostro sito" (link operativi) + "Per approfondire — fonti istituzionali".
5. Aggancia la pagina ai 5 punti di scopribilità sopra.
6. `hugo --minify` pulito → commit.

## Storia

Nata in "Onda 1" (29 maggio 2026) come sezione richiesta dall'utente per dare al sito un livello di autorevolezza verso cittadini ed enti, organizzato sulle quattro fasi del Codice della protezione civile. Pagina Colli Albani completata nella stessa giornata su fonti INGV.
