_[Indice manuale](README.md)_

# Parte 8 — Modificare e cancellare contenuti

Questa parte documenta **come intervenire su contenuti già pubblicati**: correzioni, aggiornamenti, rimozioni, gestione URL storici. Ogni operazione ha effetti su SEO, link interni e cache: seguire le procedure previene pagine 404 e perdita di traffico.

### 8.1 — Modificare un articolo esistente

**Quando farlo:**
- correzione di errori di battitura, grammatica o fattuali;
- aggiornamento con nuovi sviluppi (allerta rientrata, esercitazione conclusa, ecc.);
- completamento di informazioni mancanti;
- aggiornamento allegati.

**Procedura:**

1. Individua l'articolo in `content/comunicazioni/AAAA-MM-GG-slug.md`.
2. Apri il file con un editor che preservi gli accenti UTF-8 e i line-ending Unix.
3. Modifica il contenuto. **Non modificare** `date` e `slug` a meno che non sia proprio necessario (vedi 8.3).
4. Se aggiungi contenuti sostanziali, aggiorna `description` in frontmatter (massimo 160 caratteri).
5. Se cambi la sostanza dell'articolo, aggiungi in coda al corpo un **blocco "Aggiornamento"** con data:

   ```markdown
   ---

   **Aggiornamento del 21 aprile 2026**

   Il testo precedente è stato corretto dopo una nuova comunicazione del Centro Funzionale Regionale.
   ```

6. Verifica in locale con `hugo server -D`.
7. Commit con messaggio chiaro: `Aggiornamento articolo <titolo breve>`.

**Cosa NON fare:**
- Non cambiare il titolo in modo drastico senza coordinarlo con chi ha linkato l'articolo altrove.
- Non eliminare campi frontmatter obbligatori (vedi Parte 1).
- Non aggiungere `draft: true` a un articolo già pubblicato: il cittadino vedrebbe il link rotto. Per ritirare un articolo, vedi 8.4.

### 8.2 — Modificare una pagina statica

Le pagine statiche (`content/<sezione>/_index.md` o sottopagine) si modificano come gli articoli, ma con alcune accortezze in più:

- **Navbar e menu**: se modifichi il titolo (`title`) di una sezione principale, controlla anche la voce di menu in `hugo.toml` (`[[menu.main]]`). I due devono combaciare.
- **Breadcrumb**: Hugo costruisce il breadcrumb dalla gerarchia dei file, non dal `title`. Se rinomini una cartella, aggiorni il breadcrumb di tutte le pagine figlie.
- **URL**: cambiare la cartella di una pagina statica ne cambia l'URL. Prima di farlo, leggi 8.5 sulla gestione degli alias.

### 8.3 — Rinominare un articolo o cambiarne la data

Lo slug di un articolo (la parte finale della URL) deriva dal nome del file, tolta l'estensione `.md`. Esempio: `2026-03-10-esercitazione-castelli.md` → `/comunicazioni/2026-03-10-esercitazione-castelli/`.

**Cambiare lo slug** è un'operazione **critica**: tutti i link esterni all'articolo (social, email, altri siti, motori di ricerca) puntano al vecchio URL. Dopo la rinomina, il vecchio URL restituisce 404.

**Procedura sicura per rinominare:**

1. Rinomina il file: `git mv content/comunicazioni/vecchio-nome.md content/comunicazioni/nuovo-nome.md`.
2. Apri il file rinominato e **aggiungi un alias** nel frontmatter verso il vecchio URL:

   ```yaml
   aliases:
     - /comunicazioni/2026-03-10-esercitazione-castelli/
   ```

3. Hugo genererà una pagina al vecchio URL che redireziona automaticamente al nuovo (redirect HTML con `<meta http-equiv="refresh">`).
4. Verifica in locale che sia il vecchio sia il nuovo URL funzionino.
5. Commit con messaggio: `Rinomina articolo <titolo>, alias di redirect mantenuto`.

**Cambiare la data** cambia lo slug solo se la data è parte del nome del file (ed è sempre il caso per gli articoli di questo sito). Stesse regole: `git mv` + `aliases`.

### 8.4 — Ritirare o cancellare un articolo

Tre scenari distinti, tre procedure diverse.

#### Scenario A — Articolo pubblicato per errore, da togliere subito

Se l'articolo contiene dati non verificati, un errore grave o è stato pubblicato su richiesta e poi revocato:

1. Apri il file in `content/comunicazioni/`.
2. Imposta `draft: true` nel frontmatter **oppure** imposta `expiryDate` a una data passata:

   ```yaml
   expiryDate: 2026-04-21
   ```

3. Commit: `Ritiro articolo <titolo> — motivo: ...`.
4. Al prossimo deploy l'articolo sparisce dal sito. L'URL inizia a restituire 404.

**Nota**: se l'URL era già stato condiviso, restituire 404 è il comportamento corretto (indica "non disponibile"). Non mettere al suo posto un articolo diverso.

#### Scenario B — Articolo obsoleto ma con valore storico

Quando un articolo è vecchio ma qualcuno potrebbe ancora arrivarci via link o motore di ricerca:

1. Lascialo pubblicato.
2. Aggiungi in cima al corpo un avviso:

   ```markdown
   > **Articolo di archivio del <data>.** Le informazioni operative contenute possono essere superate.
   > Per dati aggiornati consulta [Allerte Meteo](/allerte-meteo/) o [Rischi e Prevenzione](/rischi-prevenzione/).
   ```

3. Mantieni intatto il contenuto storico originale, con date e riferimenti dell'epoca.

#### Scenario C — Articolo da rimuovere completamente dal repository

Solo se non ha mai avuto valore o se contiene dati sensibili da eliminare per motivi di privacy/GDPR:

1. `git rm content/comunicazioni/AAAA-MM-GG-slug.md`.
2. Rimuovi anche l'immagine di copertina se non più usata: `git rm static/images/AAAA-MM-GG-slug.webp`.
3. Commit: `Rimozione articolo <titolo> — motivo: richiesta di cancellazione dati`.
4. **Sul sito pubblicato** l'URL restituirà 404 fino al prossimo deploy, poi il file sparirà del tutto.
5. Se c'è un rischio di richieste di cache (es. Google), considera un redirect 301 a un URL simile tramite `aliases:` su un articolo esistente coerente.

**Nota git**: il contenuto rimosso resta nella cronologia git del repository. Per dati che devono sparire anche dalla storia (solo in caso di reale necessità legale) serve `git filter-repo` o una procedura coordinata con GitHub Support: **non** è operazione da fare in autonomia.

### 8.5 — Gestione alias e redirect

Hugo gestisce i redirect lato client tramite il campo `aliases:` nel frontmatter. Quando imposti:

```yaml
aliases:
  - /vecchio-url/
  - /altro-vecchio-url/
```

Hugo genera, per ciascun alias, una pagina HTML minimale con:

```html
<meta http-equiv="refresh" content="0; url=/nuovo-url/">
```

Questo funziona su qualsiasi hosting statico (incluso Aruba) senza bisogno di configurare nulla lato server.

**Quando usare aliases:**
- rinomina di articolo o pagina (vedi 8.3);
- fusione di due pagine in una sola;
- cambio della struttura di una sezione (es. `/volontariato/` → `/diventa-volontario/`).

**Quando NON è il caso:**
- articoli eliminati per dati errati: non vuoi redirezionare a nulla, vuoi un 404 onesto;
- URL di test mai indicizzati.

### 8.6 — Link verso articoli futuri o non ancora pubblicati (render-link hook)

Il tema `flavour-pcgenzano` implementa un **render-link hook** personalizzato in `layouts/_default/_markup/render-link.html` (e copia speculare nel tema) che risolve un problema specifico: link Markdown interni verso pagine non ancora buildate (tipicamente articoli con `date` futura) venivano renderizzati come anchor HTML, restituendo 404 al cittadino.

**Comportamento attuale dell'hook:**

| Tipo di link | Resa HTML |
|---|---|
| Link interno `/...` verso **file statico** (estensione `.pdf`, `.webp`, `.jpg`, `.png`, `.doc`, `.docx`, `.xls`, `.xlsx`, `.ppt`, `.pptx`, `.zip`, `.mp3`, `.mp4`, `.csv`, `.txt`, `.rtf`, `.svg`, `.gif`, `.jpeg`) | `<a href="/...">testo</a>` — anchor diretto, nessun lookup di pagina |
| Link interno `/...` verso pagina esistente | `<a href="/...">testo</a>` — anchor normale |
| Link interno `/...` verso pagina non trovata (né file statico) | `<span class="text-muted" title="Contenuto non ancora disponibile">testo</span>` — testo inerte |
| Link esterno `http://` o `https://` | `<a href="..." target="_blank" rel="noopener noreferrer">testo</a>` |
| Link `tel:` o `mailto:` | `<a href="..." safeURL>testo</a>` |
| Altri formati (ancore `#...`, relativi, ecc.) | anchor grezzo, nessun controllo |

**Conseguenze per chi scrive:**

- Puoi tranquillamente inserire link markdown verso articoli correlati **anche se non ancora pubblicati**: il giorno in cui l'articolo viene pubblicato, il link diventa attivo automaticamente al deploy successivo.
- I link verso **file statici** in `static/` (es. `/manuali/nome.pdf`, `/images/foto.webp`) sono sempre resi come anchor diretti: il controllo avviene per estensione, non via `site.GetPage`. Quindi un PDF in `static/manuali/` è cliccabile anche se non c'è una pagina Hugo con quell'URL.
- Se un lettore vede testo in grigio muto ("Contenuto non ancora disponibile") significa che l'articolo linkato non esiste (tipo, refuso nello slug, o articolo rimosso). Verifica con `hugo server -D`.
- I link esterni si aprono sempre in nuova scheda con `rel="noopener noreferrer"` per sicurezza.
- Frammenti (`#sezione`) e query string vengono ignorati nella lookup: l'hook controlla solo il path.

**Se devi estendere la lista di estensioni statiche**: modifica la variabile `$staticExts` (slice di stringhe) in entrambi i file `render-link.html` — quello in `layouts/` e quello in `themes/flavour-pcgenzano/layouts/`.

**Quando va aggiornato l'hook**: solo se cambia la struttura degli URL interni o si vuole modificare la modalità di fallback (es. tooltip, icona, classe CSS). Qualsiasi modifica va applicata **in entrambi i file** (`layouts/_default/_markup/render-link.html` e `themes/flavour-pcgenzano/layouts/_default/_markup/render-link.html`) per coerenza.

### 8.7 — Sostituzione immagini di copertina

Le immagini di copertina (in `static/images/AAAA-MM-GG-slug.webp`) possono essere sostituite in due modi.

**Modo A — Stessa versione, file aggiornato** (es. ritocco grafico della fascia blu):

1. Sovrascrivi il file esistente con la nuova versione (stesso nome).
2. `git add static/images/<nomefile>.webp`.
3. Commit: `Aggiornamento grafica copertina <titolo>`.

Non serve cambiare nulla nell'articolo: il path in frontmatter è invariato.

**Modo B — Immagine completamente diversa**:

1. Crea la nuova immagine seguendo le specifiche di Parte 3 (WebP, 1200px, fascia blu).
2. Nominala con lo stesso slug dell'articolo (`AAAA-MM-GG-slug.webp`).
3. `git rm` della vecchia, `git add` della nuova (se lo slug cambia).
4. Aggiorna `image:` nel frontmatter dell'articolo.
5. Verifica che `alt:` sia ancora coerente con la nuova immagine; se non lo è, riscrivilo.

**Cosa NON fare:**
- mai cambiare una foto di copertina che ritrae persone senza verificare il consenso al trattamento dell'immagine (GDPR);
- mai usare immagini da banche dati non libere senza licenza commerciale verificata;
- mai usare immagini generate da AI senza averlo esplicitato in didascalia o in nota editoriale (per trasparenza istituzionale).

---

_[Indice manuale](README.md)_

[← Parte 07 — Aggiornamento automatico settimanale](parte-07-aggiornamento-automatico-settimanale.md) · [↑ Indice](README.md) · [Parte 09 — File dati `data/` e stati del sito →](parte-09-file-dati-data-e-stati-del-sito.md)
