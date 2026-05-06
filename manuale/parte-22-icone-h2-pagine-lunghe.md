# Parte 22 — Icone Bootstrap nei titoli H2 delle pagine lunghe (maggio 2026)

Durante la sessione di consolidamento del 6 maggio 2026 è stato introdotto un pattern editoriale per **alleggerire visivamente** la lettura delle pagine più lunghe del sito. L'idea: aggiungere una piccola icona Bootstrap monocromatica blu istituzionale davanti ad ogni titolo H2 di sezione, per dare un riferimento visivo immediato senza sostituire il testo.

## 22.1 Quando applicare il pattern

Il pattern ha senso su pagine **lunghe e strutturate** dove il lettore arriva con un obiettivo specifico e il muro di testo rallenta l'orientamento:

- Pagine con `toc: true` (TOC visibile) — l'icona si propaga automaticamente all'indice.
- Almeno 5-6 H2 di contenuto (sotto questa soglia il TOC stesso non è giustificato).
- Pagine di servizio con sezioni tematiche distinte (FAQ, kit, percorsi didattici, rischi).

Non lo applichiamo a:
- Articoli `comunicazioni/` (struttura libera, badge categoria già visivo).
- Pagine brevi (≤4 H2): l'icona aggiunge rumore senza beneficio.
- Pagine con sezioni omogenee (es. lista voci glossario): la ridondanza visiva svalorizza l'icona.

## 22.2 Pattern visivo standard

Stile uniforme su tutto il sito:

```html
## <i class="bi bi-NOME-ICONA text-primary me-2" aria-hidden="true"></i>Titolo della sezione {#slug-pulito}
```

Tre elementi obbligatori:

1. **`<i class="bi bi-NOME text-primary me-2" aria-hidden="true">`** — icona Bootstrap monocromatica colore blu istituzionale (`text-primary` = `#003366`) con margine destro `me-2`.
2. **`aria-hidden="true"`** — l'icona è decorativa, gli screen reader la saltano. Il testo del titolo è già auto-esplicativo (WCAG 1.1.1).
3. **`{#slug-pulito}`** — id esplicito per l'anchor URL. Senza, Hugo genererebbe un id sporco che include il markup HTML dell'icona (`#i-classbi-bi-...`).

## 22.3 Mapping concetto → icona (vocabolario v1.0)

Il mapping è ricorrente e va mantenuto coerente. Quando aggiungi icone a una nuova pagina, riusa lo stesso vocabolario:

### Schema fisso pagine rischio (cosa fare PRIMA / DURANTE / DOPO)

| Concetto del titolo | Icona Bootstrap | Esempio |
|---|---|---|
| "Perché è rilevante" | `bi-info-circle-fill` | Pagine `/rischi-prevenzione/*` |
| "Segnali e situazioni tipiche" | `bi-eye-fill` | Idem |
| "Cosa fare PRIMA" | `bi-clipboard-check-fill` | Idem |
| "Cosa fare DURANTE" | `bi-exclamation-triangle-fill` | Idem |
| "Cosa fare DOPO" | `bi-arrow-counterclockwise` | Idem |
| "Fonti istituzionali" | `bi-bookmark-star-fill` | Pagine con riferimenti scientifici |
| "Per le scuole / docenti" | `bi-mortarboard-fill` | Approfondimenti scolastici |

### Concetti tematici ricorrenti

| Concetto del titolo | Icona Bootstrap |
|---|---|
| Domande / spiegazione (Perché serve / A cosa serve) | `bi-question-circle-fill` |
| Preparazione / pianificazione | `bi-clipboard-check-fill` |
| Compilazione attiva | `bi-pencil-square` |
| Famiglia / bambini | `bi-emoji-smile-fill` |
| Anziani / persone | `bi-person-arms-up` |
| Disabilità / accessibilità | `bi-universal-access` |
| Animali domestici | `bi-house-heart-fill` |
| Casa | `bi-house-fill` |
| Auto / veicoli | `bi-car-front-fill` |
| Checklist / liste | `bi-check2-square` |
| Aggiornamento / ricarico ciclico | `bi-arrow-clockwise` |
| Recupero post-evento | `bi-arrow-counterclockwise` |
| Consigli pratici / suggerimenti | `bi-lightbulb-fill` |
| Tempo / orari | `bi-clock-fill` |
| Numeri / chiamate | `bi-telephone-fill` |
| Geografia / territorio | `bi-geo-alt-fill` |
| Mappe / aree | `bi-pin-map-fill` |
| Documenti / download | `bi-download` |
| Regole | `bi-list-check` |
| Persone / community | `bi-people-fill` |
| Volontariato / coordinamento | `bi-person-badge-fill` |
| Lettura / studio | `bi-book-fill` |

### Casi narrativi specifici (pagine rischio)

| Concetto specifico | Icona | Pagina |
|---|---|---|
| Terremoti recenti (broadcast eventi) | `bi-broadcast` | `rischio-sismico` |
| Emissioni gas (CO₂) | `bi-droplet-half` | `rischio-vulcanico` |
| Fulmini in tempo reale | `bi-lightning-charge-fill` | `temporali-intensi` |
| Interruzione acqua | `bi-droplet-half` | `blackout` |
| Rete vicinato | `bi-house-heart-fill` | `persone-necessita-specifiche` |

## 22.4 Bug Hugo: id slug sporco senza `{#slug}`

Senza l'attribute syntax `{#id-pulito}` esplicito, Hugo Goldmark genera l'id dello slug del titolo includendo il markup HTML dell'icona. Risultato: id assurdo tipo `id="i-classbi-bi-question-circle-fill-text-primary-me-2-aria-hiddentrueiperché-serve-un-piano-familiare"`.

**Soluzione obbligatoria:** sempre `{#slug-pulito}` accanto al titolo. Hugo userà quello come id e ignorerà il markup interno per lo slug.

Prerequisito attivo nel progetto: `[markup.goldmark.parser.attribute]` con `block = true` in `hugo.toml`.

## 22.5 Bonus: integrazione automatica con TOC

Le pagine con `toc: true` nel frontmatter mostrano l'indice "In questa pagina" generato da Hugo a partire dagli H2/H3. **Il TOC riusa automaticamente il markup completo del titolo, icona inclusa.** Questo è un effetto collaterale positivo: senza ulteriore lavoro, anche l'indice diventa visivamente più ricco e coerente con il contenuto.

## 22.6 Pagine già coperte (sessione 2026-05-06)

15 pagine totali con icone H2 applicate:

- `/piano-familiare/` (test campione, commit `68c87f4`)
- 8 pagine `/rischi-prevenzione/*` con schema fisso (sismico, vulcanico, idrogeologico, incendio, temporali-intensi, vento-forte, ondate-di-calore, blackout)
- `/rischi-prevenzione/persone-necessita-specifiche/`
- `/rischi-prevenzione/kit-emergenza/`
- `/faq/`
- `/cosa-fare-adesso/`
- `/piano-emergenza/`
- `/formazione/percorsi-didattici/`

Estensione globale (commit `c5968ba`): 76 H2 totali con icona.

## 22.7 Estendere ad altre pagine

Quando crei una pagina lunga nuova (≥5-6 H2), considera se applicare il pattern:

1. Apri il file `_index.md` o `.md`.
2. Per ogni H2, aggiungi `<i class="bi bi-XXX text-primary me-2" aria-hidden="true"></i>` davanti al testo + `{#slug}` in coda.
3. Scegli l'icona dal vocabolario standard (sezione 22.3). Se non c'è la voce giusta, aggiungila qui prima di usarla, così il vocabolario resta coerente.
4. Build con `hugo --quiet` e verifica che gli id nel build (`grep '<h2 id="'`) siano puliti, non sporchi col markup dell'icona.

## 22.8 Cosa NON fare

- Icona davanti a OGNI H2/H3 (rumore visivo, perde significato).
- Icone "carine" senza pertinenza al contenuto.
- Emoji decorativi tutti diversi tra le pagine (incoerenza visiva).
- Sostituire un titolo testuale con un'icona (es. solo 🚨 invece di "Allerta").
- Icone informative che cambiano significato senza testo equivalente (WCAG fail).
- Pittogrammi ARASAAC sui titoli H2 standard: l'effetto visuale è "infantilizzante" su una pagina istituzionale. ARASAAC va riservato alle sezioni `/facile-da-leggere/` e ai kit didattici.
