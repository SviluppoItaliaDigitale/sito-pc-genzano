# Parte 40 — Comunicazione di emergenza accessibile e interoperabile (giugno 2026)

> Quattro novità introdotte il 28 giugno 2026 (PR #625) più la news-sitemap Google News del 29 giugno (PR #636). Obiettivo comune: raggiungere **chi ha bisogni comunicativi o linguistici specifici** in emergenza e rendere l'allerta del Gruppo **leggibile dalle macchine** (app, aggregatori, bot), restando privacy-first e senza dipendenze esterne.

Indice:

1. Feed CAP 1.2 — `/allerta-cap.xml`
2. Tabelle di comunicazione CAA — `/tabelle-comunicazione/`
3. Piano familiare offline
4. Facile da leggere multilingua
5. News-sitemap Google News — `/news-sitemap.xml`

---

## 40.1 Feed CAP 1.2 — `/allerta-cap.xml`

**Cos'è.** Il **Common Alerting Protocol (CAP) 1.2** è lo standard internazionale **OASIS** per la diffusione di allerte interoperabili (namespace `urn:oasis:names:tc:emergency:cap:1.2`). Un feed CAP è un documento XML che app di terzi, aggregatori e bot sanno leggere automaticamente. Il sito pubblica lo **stato di allerta meteo del Gruppo** in questo formato.

**Dove vive.**
- Template: `themes/flavour-pcgenzano/layouts/index.cap.xml`
- Output format: `hugo.toml` → `[outputs] home = [..., "CAP"]` e `[outputFormats.CAP]` (`mediaType application/xml`, `baseName allerta-cap`, `rel alternate`, `notAlternative true`)
- Dati sorgente: `data/allerta.json` (via `.Site.Data.allerta`)
- **URL pubblico:** `/allerta-cap.xml`

**Cosa produce.** Un singolo `<alert>` con uno o più blocchi `<info>`, uno per pericolo concorrente:

| Blocco `<info>` | Quando compare | Note |
|---|---|---|
| Allerta di oggi | **sempre** | `category Met`, livello `$a.livello` (default `verde`) |
| Pre-allerta di domani | solo se `$a.domani.livello` ∈ {gialla, arancione, rossa} e c'è `.titolo` | `urgency Future`, `certainty Possible` |
| Avviso meteo avverso | solo se c'è `$a.avviso_meteo.tipo` | usa `validita_inizio`/`validita_fine`/`fonte_data` scritti da `check-avvisi-meteo.py` |
| Rischio incendi AIB | solo se `$a.rischio_incendi.livello` attivo e `data >= oggi` | `category Fire`, `geocode ZonaAIB=9` (Castelli Romani) |

Mappature livello → CAP via dizionari nel template (`$sevMap` Minor/Moderate/Severe/Extreme, `$urgMap`, `$certMap`, `$respMap`). Area: Genzano di Roma, ISTAT `058043`, zona allerta Lazio `F`, cerchio `41.7068,12.6925 5.0` (raggio 5 km). `scope Public`, `status Actual`, `msgType Alert`. Rimanda al 112 e cita Centro Funzionale Lazio / DPC.

🔴 **Anti-spam (stabilità byte).** L'`identifier` è **composito** (`PCGenzano-Allerta-…`), derivato dai soli campi di **contenuto mutabili** (livello, `ultimo_aggiornamento`, sotto-blocchi domani/avviso/incendi) e sanitizzato con `replaceRE`. Così il documento resta **identico byte-per-byte tra i deploy** (la home si rigenera ogni ora con le cartine meteo) finché lo stato allerta non cambia davvero: i consumatori che deduplicano per `identifier` non vedono "nuove" allerte spurie, ma colgono ogni cambiamento reale. Stesso principio del `data-controllo-unix` del box "stato attuale".

**Robots/sitemap.** `rel = "alternate"` + `notAlternative = true` → il feed **non** è elencato come alternate nelle pagine e **non** è dichiarato in `robots.txt` (a differenza della news-sitemap). Non è bloccato: è raggiungibile direttamente all'URL.

**Per disattivarlo:** rimuovere `"CAP"` dall'array `home` in `hugo.toml`.

---

## 40.2 Tabelle di comunicazione CAA — `/tabelle-comunicazione/`

**Cos'è.** Pagina di **tabelle di Comunicazione Aumentativa Alternativa (CAA)**: griglie di **pittogrammi ARASAAC + parola** che una persona che in emergenza **non riesce a parlare** (afasia, disabilità cognitiva, non parlante italiano, bambino, anziano in stress) può **indicare** per farsi capire. È **supporto, mai sostituto** del testo (WCAG 1.4.5).

**Dove vive.**
- Pagina: `content/tabelle-comunicazione/_index.md` (`layout single`, `tts: true`, `toc: true`, `dataUltimaRevisione: "2026-06-28"`, `risorse_tema: "kit-emergenza"`)
- Shortcode: `themes/flavour-pcgenzano/layouts/shortcodes/caa-tabella.html` + `caa-voce.html`
- CSS: sezione **TABELLE DI COMUNICAZIONE CAA v1.0** in `custom.css`
- Menu: voce **"Tabelle di comunicazione (CAA)"** sotto "Accessibilità e Supporti" (`hugo.toml`, `parent = "accessibilita-supporti"`, `weight = 4`)

**Gli shortcode** (dettaglio in `.claude/rules/04a-hugo-shortcode-partial.md`):

```go-html-template
{{< caa-tabella titolo="Ho bisogno di" >}}
{{< caa-voce src="/pittogrammi/arasaac/acqua.png" parola="Acqua" >}}
{{< caa-voce src="/pittogrammi/arasaac/cibo.png"  parola="Cibo" >}}
{{< /caa-tabella >}}
```

- `caa-tabella`: `titolo` (→ `<h3>` + `aria-label`), `id` opzionale (solo se passato esplicitamente — le ancore stanno sugli H2).
- `caa-voce`: `src` e `parola` **obbligatori** (`errorf` blocca la build se manca uno dei due); `parola` è sia la label sia l'`alt`.

🔴 **Accessibilità: i pittogrammi CAA sono CONTENUTO, non decorazione.** Restano visibili anche con la preferenza "Nascondi immagini" del toolbar (`html.a11y-hide-images img.caa-cell-img { visibility: visible !important }`). Le board sono **stampabili A4** (`break-inside: avoid` → una tabella per pagina, 4 colonne in stampa). **Attribuzione ARASAAC obbligatoria** (autore Sergio Palao / Governo di Aragona, CC BY-NC-SA 4.0): le tabelle stampate ereditano la stessa licenza. La pagina rimanda al 112 e all'app *Where Are U*.

**Aggiungere una board:** nuova sezione H2 con ancora `{#slug}` nella pagina, poi un `caa-tabella` con i `caa-voce`. I pittogrammi vanno scaricati con `scripts/scarica-pittogrammi.sh` se mancano in `static/pittogrammi/arasaac/`.

---

## 40.3 Piano familiare offline

**Cos'è.** Sulla pagina `/piano-familiare/` (`content/piano-familiare/_index.md`), accanto a "Stampa / salva PDF" e "Modifica", c'è il pulsante **"Salva piano offline (HTML)"**. Genera e fa scaricare un file `.html` **autoconsistente** del piano compilato dall'utente.

**Come funziona.** La funzione JS `salvaPianoOffline()`:
1. assicura che il piano sia generato (chiama `generaPiano()` se serve) e ricava uno `slug` dal cognome;
2. costruisce una stringa HTML completa (`<!DOCTYPE html>`, `lang="it"`, viewport) con **CSS inline embedded**, riusando `#piano-contenuto.innerHTML` + intestazione, numeri di emergenza (112, 803 555), "Prima di uscire", checklist essenziale e un pulsante `window.print()`;
3. **solo testo, nessuna immagine o risorsa esterna** → il file si apre **senza connessione** (blackout, rete satura);
4. download via pattern **Blob**: `new Blob([doc], {type:'text/html;charset=utf-8'})` → `URL.createObjectURL` → `<a download="piano-emergenza-<slug>.html">` → click → `revokeObjectURL` (stesso pattern del file `.ics` del promemoria scorte);
5. tutti i valori utente sono escapati con `esc()` (textContent) — niente XSS.

**Privacy.** Coerente con il generatore PEF: i dati restano **sul dispositivo**, nulla è inviato al sito. ⚠️ "Offline" qui significa **file HTML scaricato**, non caching via Service Worker (il PEF non usa SW).

---

## 40.4 Facile da leggere multilingua

**Cos'è.** Alla pagina italiana `/facile-da-leggere/` (linguaggio chiaro + pittogrammi ARASAAC) si affiancano **quattro traduzioni**: inglese `/facile-da-leggere/en/`, esperanto `/eo/`, rumeno `/ro/`, arabo `/ar/`.

**Come sono agganciate.** **Non** tramite l'i18n di Hugo (`hugo.toml` ha solo `defaultContentLanguage = "it"`, nessun blocco `[languages.*]`). I file `en.md`/`eo.md`/`ro.md`/`ar.md` sono **pagine di contenuto normali** dentro la sezione `facile-da-leggere/`, quindi pubblicate ai rispettivi URL. Frontmatter delle traduzioni: `language: "<codice>"` (param custom), `tts: false` (il TTS del browser legge l'italiano, non le altre lingue), `layout single`, `sitemap.priority 0.6`, `dataUltimaRevisione "2026-06-28"`.

**Come ci arriva l'utente.** La pagina IT espone in testa una `<nav class="facile-lang" aria-label="Lingua / Language">` con un link per lingua, ciascuno con attributi `hreflang` e `lang` corretti e `aria-current="page"` sull'italiano (più un secondo richiamo testuale nell'alert introduttivo). La voce di menu "Facile da Leggere" punta alla sola pagina IT; le traduzioni si raggiungono dal selettore interno.

**Aggiungere una lingua:** creare `content/facile-da-leggere/<codice>.md` con lo stesso frontmatter (`language`, `tts:false`) e la stessa struttura a blocchi `.facile-blocco`, poi aggiungere il link nel selettore `<nav class="facile-lang">` della pagina IT.

---

## 40.5 News-sitemap Google News — `/news-sitemap.xml`

**Cos'è.** Una sitemap conforme allo schema **Google News** (`xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"`) con i **soli articoli recenti**, da inviare/scoprire in Search Console per l'indicizzazione rapida sulle properties Google News.

**Dove vive.**
- Template: `themes/flavour-pcgenzano/layouts/index.newssitemap.xml`
- Output format: `hugo.toml` → `[outputs] home = [..., "NEWSSITEMAP"]` e `[outputFormats.NEWSSITEMAP]` (`baseName news-sitemap`, `rel sitemap`)
- Dichiarazione: `static/robots.txt` (riga `Sitemap: …/news-sitemap.xml` accanto alla `sitemap.xml` standard)
- **URL pubblico:** `/news-sitemap.xml`

**Filtro 48h.** Il template include **solo** le pagine della sezione `comunicazioni` con `Date` negli ultimi **2 giorni** (`now.AddDate 0 0 -2`), come richiesto da Google News (niente articoli oltre le ~48h). Gli articoli `-facile` (A2) sono già esclusi via `build.list:never`. Per ogni articolo emette `<loc>`, `<news:publication>` (name "Protezione Civile Genzano di Roma", language `it`), `<news:publication_date>` ISO 8601 e `<news:title>`.

**È generata da Hugo**, non è un file statico: per disattivarla rimuovere `"NEWSSITEMAP"` dall'array `home` in `hugo.toml` (ed eventualmente la riga in `robots.txt`); per cambiare la finestra, modificare `now.AddDate 0 0 -2` nel template.

---

**Riferimenti incrociati:** shortcode CAA in `.claude/rules/04a-hugo-shortcode-partial.md`; output format CAP/news-sitemap in `04-hugo-architecture.md`; accessibilità CAA/multilingua/PEF offline in `03-accessibility.md`; banner homepage in `04b-hugo-template-css.md`.
