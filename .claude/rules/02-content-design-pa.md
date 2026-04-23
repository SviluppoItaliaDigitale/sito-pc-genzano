# Content Design PA

## Principi di scrittura

Scrivi sempre in italiano corretto, chiaro, sobrio e leggibile.
Evita burocratese, slogan vuoti, frasi troppo lunghe e tecnicismi inutili.
Scrivi pensando a cittadini reali: famiglie, anziani, volontari, scuole, persone fragili, utenti da mobile.
Ogni testo deve aiutare l'utente a capire cosa sta leggendo, cosa deve fare e dove trovare altre informazioni.

## Regole di struttura

- Titoli chiari e informativi (descrivono il contenuto, non lo pubblicizzano).
- Sottotitoli utili all'orientamento.
- Liste solo quando servono davvero, non per frammentare testo continuo.
- Call to action chiare, istituzionali, mai pressanti.
- Evita ripetizioni inutili tra titolo, occhiello e primo paragrafo.
- Mantieni coerenza tra titoli pagina, menu, breadcrumb e corpo del testo.

## Regole lessicali

- Voce attiva preferita alla passiva.
- Frasi brevi: tendenzialmente sotto le 20 parole.
- Usa "tu" o "voi" quando ti rivolgi direttamente al cittadino, se il contesto lo permette.
- Evita nominalizzazioni inutili ("effettuare il pagamento" → "pagare").
- Usa parole comuni al posto di tecnicismi quando possibile.
- Numeri di telefono: scrivi sempre in formato leggibile (es. 06 1234 5678).
- Date: scrivi in formato esteso quando rivolto ai cittadini (es. "martedì 6 aprile 2026"), usa AAAA-MM-GG solo nel frontmatter Hugo.

## Regola immagini — fascia blu istituzionale

Ogni immagine di copertina degli articoli DEVE avere una fascia blu in basso con:
- Sfondo: `#003366` (--pc-primary), opacità 85-90%, altezza ~15-18% dell'immagine
- Logo: `logo-pc-genzano.png` a sinistra (~75px di altezza)
- Riga 1: "PROTEZIONE CIVILE" — bianco, bold, ~30px
- Riga 2: "Gruppo Comunale Volontari — Genzano di Roma" — bianco, regular, ~15px
- Formato: WebP, 1200px di larghezza, max 200 KB
- Nome file: `AAAA-MM-GG-descrizione-breve.webp` in `static/images/`
- Alt text: sempre significativo, mai "Immagine di..."

Riferimento visivo: `static/images/zamberletti-protezione-civile-genzano.webp`
Specifiche complete: `MANUALE-SITO.md`, Parte 3.

## Regola foto evento — quando l'utente fornisce foto reali

**Quando l'utente fornisce foto** di un intervento, esercitazione, attività o evento, vale la **regola rigida**:

1. **TUTTE** le foto fornite vanno **inserite nel corpo dell'articolo** (mai sostituite dalla sola copertina).
2. Ogni foto deve essere inserita con lo shortcode `{{< foto >}}` — mai con markdown `![...]()` diretto:
   ```go-html-template
   {{< foto src="/images/AAAA-MM-GG-descrizione-specifica.webp"
            alt="Descrizione significativa per screen reader"
            caption="Didascalia opzionale." >}}
   ```
3. Il **nome del file foto** deve essere **diverso dallo slug dell'articolo** (es. `2026-04-20-incendio-cecchina-casolare.webp`), così lo script `genera-cover.py` non sovrascrive la foto reale con una copertina tipografica.
4. Ogni foto deve comunque avere la **fascia blu istituzionale** (vedi regola sopra). Per trattare in modo uniforme le foto fornite dall'utente, usa lo script `scripts/applica-fascia-foto.sh`:
   ```bash
   bash scripts/applica-fascia-foto.sh <file-sorgente> <nome-output-senza-ext>
   ```
   Ridimensiona a 1200 px, sovrappone logo + testo istituzionale, esporta WebP qualità 85 (ricompresso a 75 se >200 KB) in `static/images/<nome>.webp`. Evita passaggi manuali in Canva/GIMP. Dettagli in `MANUALE-SITO.md` Parte 3.8, Metodo 4.
5. Lo shortcode produce `<figure>`/`<figcaption>` accessibili, immagine cliccabile per ingrandire (apre in nuova scheda), `aria-label` descrittivo, `loading="lazy"`. La tipografia `.article-body` v7.2 (`custom.css`) applica automaticamente cornice con ombra morbida e didascalia in corsivo blu — non serve CSS inline.

Questa regola nasce dopo un incidente in cui una foto fornita dall'utente era stata sostituita dalla sola copertina automatica — comportamento non accettabile.

## Regola critica — formato data nel frontmatter Hugo

Nel frontmatter degli articoli usa SEMPRE il formato `AAAA-MM-GG` (esempio: `2026-04-06`).
NON usare MAI il formato con timezone (esempio: `2026-04-06T03:32:00Z`): causa l'esclusione dell'articolo dalla build Hugo.

## Regole editoriali

- Nessun contenuto ambiguo o non verificato.
- Nessun testo "che sembra giusto": deve essere realmente pubblicabile.
- Correggi i testi proposti dall'utente in modo conservativo, senza tradirne il significato.
- Verifica sempre ortografia, grammatica, punteggiatura e accenti.
- Se il testo originale non rispetta queste regole, riscrivilo prima di proporre pubblicazione.

## Frontmatter obbligatorio per gli articoli (comunicazioni/)

Ogni articolo deve avere tutti i campi previsti dall'archetipo:
- `title`: titolo chiaro e informativo
- `date`: formato AAAA-MM-GG
- `description`: breve sommario (massimo 160 caratteri, utile anche per SEO)
- `badge`: Allerta | Avviso | Comunicazione | Attività | Formazione | Evento | Volontariato | Radiocomunicazioni | Prevenzione | Esercitazione | Aggiornamento | Informazione | Emergenza (categorie nuove ricevono colore automatico da palette in `themes/flavour-pcgenzano/layouts/partials/badge.html`)

**Palette ufficiale delle categorie** (contrasto WCAG AA ≥ 4.5:1 su bianco):

| Categoria | Hex | Note |
|---|---|---|
| Allerta | `#d9364f` | Rosso allerta — richiede attenzione immediata |
| Emergenza | `#7f1d1d` | Rosso scuro — evento in corso di gravità massima |
| Avviso | `#b45309` | Ambra scuro — segnalazione operativa non urgente |
| Evento | `#c026d3` | Magenta — iniziativa pubblica |
| Comunicazione | `#003366` | Blu istituzionale — informazione ordinaria |
| Radiocomunicazioni | `#0369a1` | Blu radio — attività HF/VHF/UHF |
| Informazione | `#0284c7` | Azzurro — notizia di servizio |
| Prevenzione | `#15803d` | Verde — contenuti di auto-protezione |
| Esercitazione | `#ea580c` | Arancione — addestramento operativo |
| Aggiornamento | `#4338ca` | Indaco — stato avanzamento |
| Formazione | `#7c3aed` | Viola — corsi e didattica |
| Volontariato | `#b45309` | Ambra scuro — reclutamento e attività volontari |
| Attività | `#0891b2` | Turchese — operatività ordinaria |

Queste tinte sono applicate in `custom.css` in due gruppi coordinati: le classi `.notizia-categoria.<categoria>` (badge nelle card) e i selettori `.filter-pill[data-filter="<categoria>"]` (pulsanti filtro nell'archivio). Qualsiasi modifica alla palette va replicata in **entrambi** i gruppi per mantenere la coerenza visiva.
- `priorita`: normale | urgente
- `autore`: "Gruppo Comunale Volontari PC Genzano" (default)
- `image`: percorso immagine o stringa vuota
- `scadenza`: data di scadenza o stringa vuota
- `area`: zona geografica o stringa vuota
- `allegati`: lista di PDF o array vuoto `[]`. Ogni voce è un oggetto con `titolo`, `url` e `dimensione` opzionale ma raccomandata (WCAG 3.3.5 Help):
  ```yaml
  allegati:
    - titolo: "Ordinanza sindacale"
      url: "/documenti/ordinanza.pdf"
      dimensione: "120 KB"
  ```
- `draft`: false (per articoli pubblicati)

## Frontmatter per le pagine legali / istituzionali

Le pagine `content/privacy/_index.md`, `content/note-legali/_index.md`, `content/accessibilita/_index.md` e `content/social-media-policy/_index.md` devono avere il campo:

- **`dataUltimaRevisione: "AAAA-MM-GG"`** — data dell'ultima revisione sostanziale della pagina.

Il template `themes/flavour-pcgenzano/layouts/_default/single.html` mostra questo valore come box evidente (`<div class="alert alert-light">`) in cima al contenuto con il testo "Pagina rivista il …". Il partial `page-tools.html` disattiva la `.Lastmod` automatica se il campo è presente, per evitare date duplicate o in conflitto.

**Regole operative:**
- Aggiorna `dataUltimaRevisione` ogni volta che modifichi contenuto sostanziale (non refusi o link morti).
- Non scrivere date di revisione nel corpo del testo (stringhe tipo "Marzo 2026", "Ultimo aggiornamento: …"): il riferimento è unico e nel frontmatter.
- Il workflow `coerenza-docs.yml` verifica settimanalmente che le 4 pagine legali abbiano il campo impostato.
