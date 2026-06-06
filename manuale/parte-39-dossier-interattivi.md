# Parte 39 — Dossier interattivi (`/dossier/`)

I **dossier interattivi** sono racconti visivi *scrollytelling*: storie che si leggono scorrendo, con immagini a tutto schermo, dati che si animano, slider di confronto e mappe da esplorare con un tocco. Servono a spiegare in modo chiaro temi di protezione civile (rischi, prevenzione, territorio) a cittadini e scuole, con una qualità grafica da rivista digitale ma **interamente web-native, accessibile e auto-ospitata** (niente Adobe, niente flipbook di terzi, niente cookie).

Il sistema è un **"motore" riusabile**: l'impianto (sezione + layout + shortcode + CSS + JS) è scritto una volta sola; **ogni nuovo dossier è un singolo file** in `content/dossier/`.

## 39.1 Architettura

| Pezzo | File |
|---|---|
| Sezione contenuti | `content/dossier/_index.md` (landing) + `content/dossier/<slug>.md` (un dossier) |
| Layout pagina dossier | `themes/flavour-pcgenzano/layouts/dossier/single.html` |
| Layout landing (griglia card) | `themes/flavour-pcgenzano/layouts/dossier/list.html` |
| Sistema grafico immersivo | `static/css/dossier.css` (tema scuro full-bleed) |
| Interattività | `static/js/dossier.js` (vanilla, nessuna dipendenza) |
| Card homepage (dossier più recente) | `themes/flavour-pcgenzano/layouts/partials/dossier-home.html` + `static/css/dossier-home.css` |
| Stile griglia landing | `static/css/dossier-list.css` |
| Shortcode (9) | `themes/flavour-pcgenzano/layouts/shortcodes/dossier-*.html` |

Il layout `single.html` definisce `{{ define "main" }}`, carica `dossier.css`, rende la barra di avanzamento, la navigazione a pallini (dai `sezioni` del frontmatter), il `{{ .Content }}` (gli shortcode) e una sezione di condivisione (WhatsApp/Telegram/Facebook/X/email/copia/condivisione nativa), infine carica `dossier.js`.

Il CSS usa `main:has(> .dossier){padding:0}` per uscire dal padding del `<main>` del tema e andare **full-bleed**.

## 39.2 Gli shortcode

- **`dossier-hero`** — apertura a tutto schermo: immagine di sfondo, occhiello, titolo grande, sottotitolo, credito. Parametri: `id`, `image`, `alt`, `eyebrow`, `title` (accetta `<br>`), `sub`, `credito`.
- **`dossier-scena`** — sezione scrollytelling: sfondo immagine + pannello di testo in vetro. `align="left|right|top"` posiziona il pannello (con `top` l'immagine resta grande e centrata, utile quando il soggetto è al centro). Parametri: `id`, `image`, `alt`, `align`, `kicker`, `title`, `credito`; il corpo è Markdown.
- **`dossier-dati`** + **`dossier-dato`** — fascia di numeri che si animano (count-up) quando entrano nello schermo. `dossier-dato` accetta `to` (valore finale), `unita`, `label` (Markdown), oppure `da="ANNO"` per calcolare **dinamicamente** gli anni trascorsi (`{{ sub now.Year ... }}`) ed evitare dati che invecchiano.
- **`dossier-confronto`** — slider prima/dopo (due immagini sovrapposte, cursore trascinabile, accessibile da tastiera). Parametri: `titolo`, `testo`, `base`/`baseAlt`/`baseLab`, `top`/`topAlt`/`topLab`, `ratio`, `cap`.
- **`dossier-hotspot`** + **`dossier-punto`** — immagine grande con punti cliccabili (popover accessibili). `dossier-punto` accetta `x`/`y` (percentuali sull'immagine) e `titolo`; il corpo è Markdown. I popover si **capovolgono** automaticamente (alto/basso/sinistra/destra) per non uscire dallo schermo.
- **`dossier-chiusura`** — sezione finale con titolo, testo e fino a 2 CTA (`cta1`/`cta1url`, `cta2`/`cta2url`).
- **`dossier-fonti`** — crediti e fonti in fondo (Markdown).

Tutti gli shortcode che accettano un'immagine usano `strings.TrimPrefix "/" | relURL` per restare compatibili con il subpath di GitHub Pages.

## 39.3 Animazioni e accessibilità

Le animazioni sono numerose e curate (Ken Burns sull'eroe, parallasse degli sfondi, ingresso direzionale dei pannelli, comparsa "a cascata" dei punti hotspot, cielo stellato e nebulosa che derivano dietro le sezioni scure, stelle cadenti, anelli orbitanti nella chiusura, riflesso sui numeri, micro-interazioni su pulsanti e pallini). **Tutte** sono spente da:

- `@media (prefers-reduced-motion: reduce)` (preferenza di sistema);
- `html.a11y-pause-anim` (toggle "Pausa animazioni" del toolbar di accessibilità del sito).

Il dossier resta **interamente leggibile e navigabile** senza animazioni: i contenuti compaiono comunque, i popover funzionano da tastiera (Invio/Spazio per aprire, Esc per chiudere), lo slider di confronto è un `input[type=range]` nativo.

## 39.4 Creare un nuovo dossier

1. `content/dossier/<slug>.md` con frontmatter: `type: "dossier"`, `title`, `description`, `image` (cover per social/landing), `tts: false`, `indice: false`, e la lista `sezioni: [{ id, label }, ...]` (un punto per ogni `id` di sezione, per la navigazione a pallini).
2. Comporre il corpo con gli shortcode `dossier-*`, dando a ogni sezione lo stesso `id` dichiarato in `sezioni`.
3. Immagini in `static/images/dossier/` (WebP). **Solo immagini con licenza chiara** (NASA pubblico dominio, Copernicus/ESA CC BY, autori con CC) e **credito onesto** in `credito`/`cap`/`fonti`. Mai attribuire al satellite sbagliato o spacciare un'immagine per un'altra.
4. La voce compare da sola nella landing `/dossier/`; il dossier più recente compare nel box della homepage.

## 39.5 Menu e homepage

- Menu: voce **"Dossier interattivi" → `/dossier/`** nel dropdown **Risorse**, subito dopo "Conoscere la Protezione Civile". Va tenuta sincronizzata in `hugo.toml` **e** in `static/app-shared/site-chrome.js` (menu hard-coded delle pagine statiche).
- Homepage: `partials/dossier-home.html` (inserito in `layouts/index.html`, modalità normale, fra `cruscotto-home` e `services`) mostra il dossier più recente con la sua copertina; si auto-nasconde se non ci sono dossier e mostra "Vedi tutti i dossier" solo se ce n'è più di uno.

## 39.6 Pilota

**"La Terra vista dallo spazio"** (`content/dossier/terra-dallo-spazio.md`): come i satelliti osservano la Terra e aiutano la protezione civile — Copernicus/Sentinel, incendi (EFFIS), alluvioni (Copernicus EMS), qualità dell'aria (CAMS), i Castelli Romani e i loro crateri dall'orbita, la costellazione italiana **IRIDE**, la visione notturna. Immagini NASA (PD) + Copernicus/ESA (CC BY) + Pierre Markuse (CC BY 2.0). La mappa "Esplora i crateri dei Castelli" usa un'immagine Sentinel-2 reale dei Colli Albani (ESA, CC BY).
