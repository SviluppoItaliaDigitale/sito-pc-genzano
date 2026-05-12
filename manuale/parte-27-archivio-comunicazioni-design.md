# Parte 27 — Archivio `/comunicazioni/` — design senza paginazione

Aggiunta a maggio 2026 dopo un audit ricorrente che segnalava "bug paginazione" sull'archivio. Non è un bug: è una scelta di design deliberata. Questa parte documenta come funziona davvero la pagina, perché è stata progettata così, e quando rivedere la decisione.

## 27.1 Lo "pseudo-bug" segnalato

Auditor che esaminano la pagina `/comunicazioni/` per la prima volta a volte segnalano:

> *"L'indice mostra solo i primi 10 articoli + paginazione a 2 pagine"*

oppure:

> *"Vediamo 10-12 articoli, ma sul disco ce ne sono 100+: dove sono gli altri?"*

Entrambe le percezioni sono **errate**, ma comprensibili. Vediamo perché.

## 27.2 Come funziona davvero

Il template è `themes/flavour-pcgenzano/layouts/comunicazioni/list.html`. Logica essenziale:

```go-html-template
{{/* 1. Filtra le versioni "facile da leggere" (NON devono apparire qui) */}}
{{- $pages := where .Pages "Params.versione_facile_di" nil -}}

{{/* 2. Raggruppa per mese (formato "2006-01" = "AAAA-MM") */}}
{{- $grouped := $pages.GroupByDate "2006-01" -}}

{{/* 3. Itera TUTTI i mesi, e per ciascuno TUTTI gli articoli */}}
{{ range $grouped }}
  <section class="archivio-mese">
    <h2>{{ $monthName }} {{ $year }}</h2>
    {{ range .Pages }}
      <article class="card card-notizia" data-badge="..." data-anno="...">
        ...
      </article>
    {{ end }}
  </section>
{{ end }}
```

**Niente `.Paginator`. Niente `first 10`. Niente limite di N.**

Tutti i ~104 articoli pubblicati (data passata) finiscono nel DOM, ordinati dal mese più recente al più antico, ciascuno con `data-badge` e `data-anno` per i filtri JavaScript.

## 27.3 Perché è stata fatta questa scelta

Decisione presa nel refactoring di aprile 2026. Quattro ragioni:

1. **Niente latency di scroll-to-load**. La paginazione classica (pagina 1, 2, 3, ...) introduce un click + reload per accedere a articoli vecchi. Per un cittadino che cerca *"l'articolo di tre mesi fa sull'allerta arancione"*, è friction. Con scroll unico + filtri, in 2 secondi è già lì.

2. **Filtri client-side immediati**. Le filter-pills per **categoria** (Allerta, Avviso, Formazione, ...) e **anno** lavorano sul DOM completo. Niente round-trip al server, niente loading state. Click → istantaneo.

3. **Indice mese-per-mese navigabile**. La sidebar a destra (sezione "Vai al mese") mostra l'elenco mesi → click → ancora `#mese-2026-04` → scroll. Più ergonomico di "pagina 2 di 11".

4. **SEO + screen reader**. Tutti gli articoli sono raggiungibili **senza JavaScript** (con la sola lettura sequenziale dell'HTML). Per un crawler o uno screen reader, l'archivio è un unico documento strutturato — niente paginazione che spezza il flusso.

## 27.4 Numeri attuali (snapshot 12 maggio 2026)

| Metrica | Valore |
|---|---|
| File `.md` sul disco | 388 |
| Articoli con `date <= today` (visibili) | 104 |
| Articoli con `date > today` (calendarizzati futuri, esclusi da Hugo) | 283 |
| Gruppi mese renderizzati | 24 (gennaio 2024 → maggio 2026) |
| Dimensione HTML buildato | ~208 KB |
| Tempo di rendering Hugo | <100 ms |
| Tempo di caricamento browser su 4G | ~1.2 s |

## 27.5 Perché un auditor può vedere "10 articoli + 2 pagine"

Tre ragioni plausibili:

1. **Filtro JavaScript attivo**: l'auditor ha cliccato una filter-pill (es. badge "Allerta") che ha N=10 articoli totali nel database. JavaScript nasconde tutte le altre card via `display: none`, quindi a video vede solo 10. Non è paginazione: è filtraggio.

2. **Mese corrente parziale**: il primo gruppo mensile (es. maggio 2026 al 12) ha ~10-15 articoli pubblicati al momento dell'audit. L'auditor scorre il primo `<section class="archivio-mese">`, vede l'h2 successivo (Aprile 2026), e legge erroneamente la transizione come "fine pagina 1".

3. **JavaScript filtri non ancora caricato**: se la pagina viene auditata mentre i filtri JS si stanno ancora inizializzando, alcuni utenti vedono brevemente solo le prime card. Comportamento documentato in console come `data-loading="true"` mentre il DOM si stabilizza.

In **tutti i tre casi** la verifica corretta è:

```bash
curl -sL "https://www.protezionecivilegenzano.it/comunicazioni/" \
  | grep -oE '/comunicazioni/20[0-9]{2}-[0-9]{2}-[0-9]{2}-[a-z0-9-]+' \
  | sort -u | wc -l
```

Restituisce il numero **vero** di articoli renderizzati nell'HTML (al 12 maggio 2026: 104). Niente paginazione, niente nascondimento server-side.

## 27.6 Quando rivedere la scelta

L'approccio "scorrimento unico" ha un limite naturale: quando il sito supererà **circa 300 articoli visibili** la pagina diventerà:

- pesante (>500 KB HTML);
- lenta da renderizzare su mobile vecchio;
- difficile da scrollare con la tastiera per chi usa `Page Down`.

Al raggiungimento di questa soglia, valutare due alternative non mutuamente esclusive:

a. **Paginazione per anno**: una pagina HTML per ogni anno (`/comunicazioni/2024/`, `/comunicazioni/2025/`, `/comunicazioni/2026/`), homepage archivio con i soli 30 articoli più recenti + link "Vai all'archivio 2025", "Vai all'archivio 2024", ecc. Vantaggio: ogni pagina < 100 KB. Svantaggio: i filtri devono essere ripensati (non più cross-anno automatici).

b. **Lazy load via IntersectionObserver**: HTML iniziale con i primi 30 articoli + caricamento progressivo via JS quando l'utente scorre vicino alla fine. Vantaggio: l'esperienza utente resta singola pagina. Svantaggio: senza JS l'utente vede solo i primi 30.

**Trigger preferito per la rivalutazione**: superamento dei 300 articoli visibili (saremo verso aprile-maggio 2027 al ritmo attuale di pubblicazione, ~1 articolo/giorno secondo PIANO-EDITORIALE.md).

## 27.7 Domande frequenti dell'audit

**D: La paginazione di Hugo (`paginate = 10` di default) è disabilitata o non viene chiamata?**
R: Hugo ha il valore di default `pagerSize = 10`, ma il template `comunicazioni/list.html` **non chiama** `.Paginator`. Quindi quel default è irrilevante. Il fatto che `hugo.toml` non abbia un `paginate` esplicito è ininfluente.

**D: Cosa succede agli articoli `*-facile.md` (versione italiano semplice)?**
R: Esclusi dall'archivio via `where .Pages "Params.versione_facile_di" nil` (riga 5 del template). Devono essere raggiunti **solo** dal bottone giallo "Leggi in italiano semplice" sull'articolo madre. Vedi Parte 25 § 25.11.

**D: Articoli calendarizzati (date futura) compaiono?**
R: No, Hugo li esclude automaticamente al build. Entrano nell'archivio il giorno della loro `date` quando `pubblica-programmata.yml` (06:00 UTC giornaliero) ricostruisce il sito.

**D: La pagina ha un indice ad ancora `#mese-AAAA-MM`?**
R: Sì, ogni `<section class="archivio-mese" id="mese-AAAA-MM">` è raggiungibile via deep link. Per esempio `https://www.protezionecivilegenzano.it/comunicazioni/#mese-2024-12` porta direttamente a "Dicembre 2024".

## 27.8 Riferimenti

- Template: `themes/flavour-pcgenzano/layouts/comunicazioni/list.html` (~270 righe)
- Filtri JS: `static/js/archivio-filters.js` (~120 righe, gestisce filter-pills e mostra/nasconde card)
- Articolo madre della convenzione "no paginazione": [Parte 25 § 25.11](parte-25-italiano-l2-versione-facile.md) (`build.list: never` esclusione dalle liste)
- Trigger di rivalutazione: PIANO-EDITORIALE.md (cadenza target ~1 articolo/giorno)
