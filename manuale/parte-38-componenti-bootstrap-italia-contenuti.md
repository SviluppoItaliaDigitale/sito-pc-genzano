# Parte 38 — Componenti Bootstrap Italia per i contenuti (callout, passi, timeline, galleria) + indice di pagina

Da fine maggio 2026 il redattore ha a disposizione quattro **shortcode di contenuto** in più, presi dal design system **Bootstrap Italia** (quindi già AGID e accessibili), per rendere più leggibili e navigabili le pagine. In più, tutte le pagine lunghe hanno un **indice di pagina con scrollspy** automatico. Questa parte spiega quando e come usarli.

Principio guida (rule 01): si usa un componente **dove aiuta davvero la lettura**, non per decorare. Inserire componenti dove non servono è "complessità inutile" ed è vietato.

## 38.1 Callout — box nota colorato

Riquadro per evidenziare una nota, un avviso o un richiamo. **È il componente nativo di Bootstrap Italia** (non scrivere CSS `.callout` custom: collide col bundle BI).

```go-html-template
{{</* callout tipo="info" titolo="Come usare questo piano" */>}}
Compila il piano insieme alla famiglia e rileggilo una volta l'anno.
{{</* /callout */>}}
```

- `tipo`: `info` (blu/nota), `avviso` (ambra), `pericolo` (rosso), `ok` (verde). Default `info`.
- `titolo`: opzionale (mostra l'icona del tipo + il titolo).
- Il corpo accetta Markdown.
- **Quando**: una nota che deve staccarsi dal testo (un chiarimento, un "attenzione", una conferma). Non per ogni paragrafo: perde forza.

## 38.2 Passi (stepper) — lista numerata a tappe

Trasforma una **lista ordinata Markdown** in passi con pallini numerati. Resta un `<ol>` reale (lo screen reader annuncia ordine e numero).

```go-html-template
{{</* passi titolo="Il corso di accesso, passo dopo passo" */>}}
1. Primo passo…
2. Secondo passo…
{{</* /passi */>}}
```

- `titolo`: opzionale.
- **Quando**: una sequenza o procedura (iscrizione, schema di funzionamento, "cosa succede quando…"). Per elenchi non sequenziali resta meglio la lista normale.

## 38.3 Timeline — linea del tempo

Trasforma una **lista Markdown** in una cronologia verticale con marcatori. Una voce per evento, di norma `**data/ora** — descrizione`.

```go-html-template
{{</* timeline */>}}
- **9:00** — arrivo in sede, riunione informativa
- **9:15** — verifica mezzi e attrezzature
{{</* /timeline */>}}
```

- **Quando**: una successione temporale (giornata-tipo, fasi di un evento, cronologia storica). La data/ora in `**grassetto**` a inizio voce diventa il riferimento del nodo.

## 38.4 Galleria — carosello per ≥4 foto

Per gli articoli con **almeno 4 foto**: invece di quattro `{{< foto >}}` in colonna, un carosello accessibile.

```go-html-template
{{</* galleria titolo="Le foto dell'esercitazione" */>}}
{{</* foto src="/images/2026-…-a.webp" alt="…" caption="…" */>}}
{{</* foto src="/images/2026-…-b.webp" alt="…" */>}}
… (≥4 foto) …
{{</* /galleria */>}}
```

- **Solo avanzamento manuale** (mai autoplay — WCAG 2.2.2): scorri o usa i pulsanti ‹ ›, disabilitati ai bordi.
- Le foto restano i normali `{{< foto >}}` (alt/caption/fascia blu come sempre). In stampa il carosello si apre e mostra tutte le foto in colonna.
- **Quando**: 4 o più foto della stessa attività. Con 1-3 foto si usa la convenzione standard (Parte 3): 1ª dopo il 1° H2, 2ª dopo il 2° H2, ecc.

## 38.5 Indice di pagina con scrollspy (automatico)

Tutte le pagine con **almeno 3 intestazioni** mostrano l'indice "In questa pagina": su desktop una colonna **sticky** a sinistra che evidenzia la sezione corrente mentre si scorre; su mobile un accordion collassabile in cima.

- È **automatico**: nessun frontmatter da attivare (il vecchio `toc: true` in `<details>` è stato rimosso).
- **Opt-out** su una pagina: `indice: false` (oppure `toc: false`) nel frontmatter.
- **Escluse** le pagine-strumento (cruscotto, laboratorio-meteo, cerca, emergenza, lanterna, mappa-sito, attribuzioni-pittogrammi).
- Per farlo funzionare bene, **scrivi H2 chiari e brevi**: diventano le voci dell'indice. Hugo genera gli id dagli H2; non servono id manuali.

## 38.6 Utility di supporto

- **`.pc-spinner`** — piccolo indicatore di caricamento (usato negli stati di attesa del Laboratorio meteo). Rispetta `prefers-reduced-motion` e la "pausa animazioni" del toolbar.
- **`.table-sticky`** — su un `<div class="table-responsive table-sticky">` rende l'intestazione della tabella **sticky** quando il tabellone è lungo (`max-height: 70vh`). Da usare solo su tabelle davvero lunghe.

## 38.7 Regole trasversali

- **Verifica visiva** prima del commit quando introduci uno di questi blocchi in una pagina (CLAUDE.md § "Verifica visiva pre-commit"): sono markup/CSS strutturali, vanno guardati con Playwright.
- **Niente CSS custom** che duplichi nomi del design system (vedi il caso `.callout`): se Bootstrap Italia ha già il componente, si usa quello.
- **Sobrietà**: questi componenti aiutano la lettura. Non vanno sparsi ovunque; si applicano dove c'è una nota, una sequenza, una cronologia o una galleria reale.
