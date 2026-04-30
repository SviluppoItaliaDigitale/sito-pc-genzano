# Manuale operativo da MOBILE (Android, smartphone)

Guida pratica per gestire il sito **interamente da telefono**, senza
PC, usando solo:

1. **App Claude per Android** (claude.ai) — per scrivere articoli e
   farsi aiutare
2. **Browser mobile** (Chrome/Firefox/Edge su Android) — per accedere
   a GitHub web
3. (opzionale) **App Termux** — per chi sa usare il terminale Android

> Tutto quello che fai sul sito da PC con Claude Code, lo puoi fare
> dal telefono con questi 3 strumenti. Le automazioni del sito girano
> in background su GitHub Actions: tu scrivi, GitHub fa.

---

## Indice

0. [Prima di iniziare a lavorare da mobile (CHECK SESSIONE)](#0-prima-di-iniziare-a-lavorare-da-mobile-check-sessione)
1. [Setup iniziale (una sola volta)](#1-setup-iniziale-una-sola-volta)
2. [Pubblicare un articolo nuovo da mobile](#2-pubblicare-un-articolo-nuovo-da-mobile)
3. [Aggiungere foto a un articolo](#3-aggiungere-foto-a-un-articolo)
4. [Ottenere le bozze social per gli articoli](#4-ottenere-le-bozze-social-per-gli-articoli)
5. [Pubblicare sui social da mobile](#5-pubblicare-sui-social-da-mobile)
6. [Modificare un articolo già pubblicato](#6-modificare-un-articolo-già-pubblicato)
7. [Attivare/disattivare la modalità emergenza](#7-attivaredisattivare-la-modalità-emergenza)
8. [Aggiornare l'allerta meteo](#8-aggiornare-lallerta-meteo)
9. [Cose che il sito fa DA SOLO (non devi farle tu)](#9-cose-che-il-sito-fa-da-solo-non-devi-farle-tu)
10. [Risoluzione problemi mobile](#10-risoluzione-problemi-mobile)

---

## 0. Prima di iniziare a lavorare da mobile (CHECK SESSIONE)

**Quando le rules vengono modificate da PC, la sessione mobile aperta in precedenza non lo sa.** Il context iniziale (CLAUDE.md + 8 rules in `.claude/rules/`) viene caricato **una sola volta all'avvio sessione** e resta fissato. Una sessione vecchia continua a ragionare con le rules vecchie finché non viene chiusa e riaperta.

### Quando archiviare la sessione mobile in corso e aprirne una nuova

| Cosa è stato modificato di recente nel repo | Devo ricominciare? |
|---|---|
| `CLAUDE.md`, `.claude/rules/*.md`, archetype | **SÌ, sempre** |
| `MANUALE-SITO.md`, `MANUALE-MOBILE.md`, `PIANO-EDITORIALE.md` (sezioni operative o nuove regole) | **SÌ** |
| Articoli `content/`, dati `data/`, template/CSS, script | No, va bene |
| Workflow CI (`.github/workflows/`) | No (girano su GitHub Actions, non in chat) |

### Procedura

1. **Chiudo / archivio** la sessione mobile in corso.
2. **Apro una sessione nuova** sul repo.
3. **Primo messaggio** alla nuova sessione: il prompt-test seguente.

### Prompt-test di verifica (consigliato)

Incolla questo come primo messaggio nella nuova sessione:

> "Prima di lavorare, riassumi in 3 righe: (a) le rules che stai applicando in questa sessione (file in `.claude/rules/`), (b) la regola più recente sul tema 'foto inline / foto stock / foto utente', (c) qualsiasi nuovo divieto o checkpoint pre-batch che dovresti rispettare. Non fare azioni operative finché non confermo."

Se la risposta cita correttamente la regola **"Divieto: foto stock generiche ripetute per macro-tema"** in `02-content-design-pa.md` e parla di **checkpoint pre-batch** (regola 07), la sessione è aggiornata. Se invece risponde con regole vecchie, sta usando un context obsoleto: chiudila e riapri (o forza un `git pull` se l'app lo permette).

### Cosa fa l'agent in autonomia (regola 07-proattivita-coerenza.md)

Da maggio 2026 la rule `07` formalizza un **checkpoint pre-operazione batch**: prima di toccare ≥5 articoli o ≥5 file in una singola operazione, l'agent deve **fermarsi**, riassumere in 2-3 righe le rules pertinenti, e chiedere conferma. Questo è il safety-net introdotto dopo l'incidente del batch foto stock di aprile 2026 (74 articoli con la stessa foto della Croce Rossa). Una sessione mobile aggiornata rispetterà questo checkpoint da sola; una sessione vecchia no.

---

## 1. Setup iniziale (una sola volta)

### Sul telefono Android

1. **Installa l'app Claude** dal Play Store: <https://play.google.com/store/apps/details?id=com.anthropic.claude>
   - Login con il tuo account Anthropic (lo stesso di claude.ai)
2. **Salva i siti GitHub nei segnalibri** del browser:
   - <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano> (repo principale)
   - <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions> (workflow CI)
   - <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/tree/main/social-bozze> (bozze social pronte)

### Su GitHub (una sola volta)

I secret per le automazioni devono essere già configurati nel repo:

1. Vai su **Settings → Secrets and variables → Actions**
2. Verifica che ci siano:
   - `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD` (per il deploy Aruba)
   - `GEMINI_API_KEY` (per generazione bozze social)

Se mancano, aggiungili usando le tue credenziali Aruba e la chiave
Google AI Studio (gratis: <https://aistudio.google.com/apikey>).

---

## 2. Pubblicare un articolo nuovo da mobile

### Step A — Chiedi a Claude (app Android) di scriverlo

Apri Claude e scrivigli qualcosa tipo:

> «Sono il referente del Gruppo Comunale Volontari di Protezione Civile
> di Genzano di Roma. Devo scrivere un articolo per il sito sul tema
> [TEMA]. Il sito usa Hugo e ha un archetype con frontmatter specifico.
> Scrivimi titolo, descrizione (≤160 caratteri), badge appropriato
> (Allerta/Avviso/Comunicazione/Attività/Formazione/Evento/
> Volontariato/Radiocomunicazioni/Prevenzione/Esercitazione/
> Aggiornamento/Informazione/Emergenza), e il corpo dell'articolo.
> Tono: istituzionale AGID, sobrio, voce attiva, frasi brevi.»

Claude ti risponde con un articolo strutturato.

> **Nota importante**: l'app Claude per Android NON ha accesso al tuo
> repo GitHub. Per farsi guidare dalle rules del Gruppo, copia/incolla
> il contenuto di queste pagine quando serve:
> - <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/blob/main/.claude/rules/02-content-design-pa.md>
> - <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/blob/main/.claude/rules/06-protezione-civile-scientifica.md>

### Step B — Crea il file su GitHub mobile

1. Apri il browser mobile e vai su:
   <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/new/main/content/comunicazioni>

2. Nel campo «Name your file» scrivi il nome del file:
   ```
   AAAA-MM-GG-titolo-slug.md
   ```
   Esempio: `2026-05-15-esercitazione-aib-castelli.md`

3. Nel corpo, incolla quello che Claude ti ha generato. Deve avere
   questo formato (frontmatter YAML in cima fra `---`):

   ```yaml
   ---
   title: "Esercitazione AIB ai Castelli Romani"
   date: 2026-05-15
   description: "Mezzi e volontari del Gruppo nell'esercitazione antincendio della Regione Lazio."
   badge: "Esercitazione"
   priorita: "normale"
   autore: "Gruppo Comunale Volontari PC Genzano"
   image: ""
   image_alt: ""
   scadenza: ""
   area: "Castelli Romani"
   allegati: []
   draft: false
   ---

   Il 15 maggio 2026 il Gruppo Comunale Volontari di Protezione Civile
   ...
   (corpo dell'articolo qui)
   ```

4. Scorri in fondo alla pagina, clicca **«Commit changes»**.
5. Conferma con un messaggio (es. `Nuovo articolo: esercitazione AIB`).

### Step C — Cosa succede dopo (automatico)

Entro 5-10 minuti GitHub Actions fa partire 3 workflow paralleli che
puoi seguire da:
<https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions>

| Workflow | Cosa fa |
|---|---|
| 🚀 Deploy | Builda Hugo e pubblica su Aruba + GitHub Pages |
| 📷 Scarica foto | Se hai messo un marker `# TODO-foto-wikipedia: ...` (vedi sezione 3), scarica la foto da Wikipedia |
| 📱 Genera bozze social | Crea `social-bozze/<slug>/` con 4 file `.txt` per X/Facebook/Instagram/Telegram + immagini Instagram |

Quando tutti i pallini diventano verdi ✅, l'articolo è online.

---

## 3. Aggiungere foto a un articolo

### Caso A — Hai una foto sul telefono che vuoi usare

Le foto servono caricate sul repo come file `.webp` di 1200px con
fascia blu istituzionale. Da mobile **non** puoi farlo direttamente:
serve l'opzione B (Wikipedia/NASA/USGS automatico) oppure devi
prima caricarle su un PC con `bash scripts/applica-fascia-foto.sh`.

### Caso B — Vuoi una foto automatica da fonti libere (7 fonti supportate)

Nel frontmatter dell'articolo, aggiungi UNA riga di **marker**.
Sono supportate **7 fonti**, ognuna pensata per un tipo di articolo diverso.

#### 🗺️ Tabella decisionale: quale fonte per quale articolo

| Tipo di articolo | Fonte consigliata | Esempio marker |
|---|---|---|
| Anniversario evento storico (terremoti famosi, alluvioni, eruzioni) | **Wikipedia** | `# TODO-foto-wikipedia: bash scripts/foto-da-wikipedia.sh "Terremoto dell'Irpinia del 1980" slug` |
| Personaggio storico, opera, libro, organizzazione | **Wikipedia** | `# TODO-foto-wikipedia: bash scripts/foto-da-wikipedia.sh "Giuseppe Zamberletti" slug` |
| Fenomeno globale visto dallo spazio (uragani, eruzioni, ondata calore) | **NASA** | `# TODO-foto-nasa: bash scripts/foto-da-nasa.sh "Etna eruption" slug` |
| ShakeMap di un terremoto specifico | **USGS** | `# TODO-foto-usgs: bash scripts/foto-da-usgs.sh shakemap us6000abcd slug` |
| Uragani, traccia tropicale (NHC), foto storica meteo | **NOAA** | `# TODO-foto-noaa: bash scripts/foto-da-noaa.sh "URL diretto" "Descrizione" slug` |
| **Foto stock generica** (volontari, atmosfera, persone, attività) | **Pexels** o **Unsplash** | `# TODO-foto-pexels: bash scripts/foto-da-pexels.sh "rescue volunteer" slug` |
| **Foto stock alta qualità** (illustrazioni, oggetti, paesaggi) | **Pixabay** | `# TODO-foto-pixabay: bash scripts/foto-da-pixabay.sh "ambulance" slug` |

> ⚠️ **Mai usare i marker `pexels`/`pixabay`/`unsplash` per popolare batch di articoli con la stessa query categoriale.** Le API stock restituiscono sempre la stessa prima immagine: il risultato è decine di articoli con foto identica e caption duplicata. Esempio reale evitato (ad aprile 2026 un batch ha messo la stessa foto della Croce Rossa su 74 articoli, è stato ripulito interamente). Regola formale in `.claude/rules/02-content-design-pa.md` sezione "Divieto: foto stock generiche ripetute per macro-tema". Usare i marker stock **solo** per articoli singoli con query specifica al contenuto, e preferire sempre Wikipedia/NASA/USGS/NOAA quando la materia lo permette.

#### Esempio completo

```yaml
---
title: "Anniversario terremoto Irpinia"
date: 2026-11-23
image: ""
# TODO-foto-wikipedia: bash scripts/foto-da-wikipedia.sh "Terremoto dell'Irpinia del 1980" 2026-11-23-irpinia
---
```

#### Lista completa marker

```yaml
# TODO-foto-wikipedia: bash scripts/foto-da-wikipedia.sh "Titolo Wikipedia" slug [it|en]
# TODO-foto-nasa:      bash scripts/foto-da-nasa.sh      "search query"     slug
# TODO-foto-usgs:      bash scripts/foto-da-usgs.sh      shakemap <eventid> slug
# TODO-foto-noaa:      bash scripts/foto-da-noaa.sh      "URL noaa.gov"     "Contesto" slug
# TODO-foto-pexels:    bash scripts/foto-da-pexels.sh    "search query"     slug
# TODO-foto-pixabay:   bash scripts/foto-da-pixabay.sh   "search query"     slug
# TODO-foto-unsplash:  bash scripts/foto-da-unsplash.sh  "search query"     slug
```

#### Cosa succede al commit

Il workflow `scarica-foto-automatica.yml` (CI):
1. Scansiona gli articoli con marker
2. Scarica la foto dalla fonte scelta (rete libera del runner GitHub)
3. Applica la fascia blu istituzionale
4. Popola `image:` + `image_credit:` + `image_source_url:` nel frontmatter
5. Rimuove il marker
6. Committa e ri-triggera il deploy

> ⚠️ **Pexels/Pixabay/Unsplash richiedono API key** (gratuite). Devono essere configurate **una sola volta** come GitHub Secrets:
> - `PEXELS_API_KEY` (https://www.pexels.com/api/)
> - `PIXABAY_API_KEY` (https://pixabay.com/api/docs/)
> - `UNSPLASH_ACCESS_KEY` (https://unsplash.com/developers)
>
> Se mancano, l'articolo con quel marker fallirà con messaggio chiaro nella issue automatica. Le altre 4 fonti (Wikipedia/NASA/USGS/NOAA) non richiedono API key e funzionano sempre.

> Da PC puoi farlo localmente con uno dei sette script (richiede le API key in `~/.bashrc` per le 3 stock). Da mobile usi **SOLO il marker**: il workflow CI fa tutto.

---

## 4. Ottenere le bozze social per gli articoli

Dopo che il workflow `📱 Genera bozze social` è andato a buon fine, le
bozze sono nel repo. Le trovi qui (replica per ogni articolo):

<https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/tree/main/social-bozze>

Apri la cartella dell'articolo (es. `2026-05-15-esercitazione-aib-castelli`)
e troverai:

| File | Per | Apri da mobile |
|---|---|---|
| `x.txt` | X (Twitter) | clicca → testo subito visibile, copia |
| `facebook.txt` | Facebook | clicca → testo subito visibile, copia |
| `instagram.txt` | Instagram | clicca → testo + percorsi delle immagini in fondo |
| `telegram.txt` | Telegram | clicca → testo Markdown, copia |
| `README.md` | Promemoria | spiega come usare le bozze |

### Per Instagram: scarica le immagini da mobile

Nel file `instagram.txt` in fondo trovi i percorsi delle immagini.
Se è un **carosello multi-immagine** (lo script l'ha rilevato dal
fatto che hai foto inline nel body), troverai qualcosa tipo:

```
📷 CAROSELLO Instagram (3 immagini, caricale in questo ordine):
   1. /home/.../static/images-social/<slug>-instagram-post-1.webp
   2. /home/.../static/images-social/<slug>-instagram-post-2.webp
   3. /home/.../static/images-social/<slug>-instagram-post-3.webp
📷 Story 1080x1920: /home/.../static/images-social/<slug>-instagram-story.webp
```

Quei percorsi locali li ignori. Le immagini le trovi anche nel repo a:

```
https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/tree/main/static/images-social
```

oppure raggiungibili in URL diretto sul sito Aruba:

```
https://www.protezionecivilegenzano.it/images-social/<slug>-instagram-post-1.webp
https://www.protezionecivilegenzano.it/images-social/<slug>-instagram-post-2.webp
https://www.protezionecivilegenzano.it/images-social/<slug>-instagram-story.webp
```

**Per scaricarle da mobile:**
1. Apri l'URL diretto Aruba in un nuovo tab del browser
2. Tieni premuto sull'immagine → «Salva immagine»
3. La trovi in `Galleria → Download`

---

## 5. Pubblicare sui social da mobile

### X (Twitter)

1. Apri l'app X
2. Nuovo post
3. Incolla il testo da `x.txt`
4. (Facoltativo) Allega cover dell'articolo se vuoi (X mostra l'anteprima
   automatica dal link)
5. Pubblica

### Facebook

1. Apri l'app Facebook
2. Nuovo post sulla pagina del Gruppo
3. Incolla il testo da `facebook.txt`
4. Aspetta che Facebook generi l'anteprima automatica del link
   (richiede ~5 secondi, vedrai cover + titolo + descrizione)
5. Pubblica

### Instagram

#### Post normale (singola immagine)

1. Apri l'app Instagram
2. Nuovo post
3. Seleziona l'immagine `<slug>-instagram-post.webp` dalla galleria
   (l'hai scaricata al passo 4)
4. Caption: incolla il testo da `instagram.txt`
5. Pubblica

#### Carosello (più immagini)

1. Apri l'app Instagram
2. Nuovo post
3. Tocca l'icona del **carosello** (in alto a destra, due quadrati
   sovrapposti)
4. Seleziona le immagini **NEL GIUSTO ORDINE** (1, 2, 3, ...)
5. Caption: incolla il testo da `instagram.txt`
6. Pubblica

#### Story

1. Apri Instagram → Storie
2. Sulla galleria seleziona `<slug>-instagram-story.webp`
3. (Facoltativo) Aggiungi adesivi/sticker — la story ha già il
   template con titolo e link
4. Pubblica

### Telegram

1. Apri l'app Telegram
2. Vai sul canale del Gruppo
3. Incolla il testo da `telegram.txt`
4. Telegram interpreta automaticamente il Markdown
   (`**grassetto**`, `[link](url)` ecc.)
5. Invia

---

## 6. Modificare un articolo già pubblicato

1. Vai su:
   <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/tree/main/content/comunicazioni>

2. Apri il file `.md` dell'articolo

3. Tocca l'icona ✏️ **Edit** (matita) in alto a destra

4. Modifica il testo direttamente nel browser

5. Scrolla giù e premi **Commit changes**

6. Entro 5 minuti il sito è aggiornato.

> Se modifichi titolo/descrizione e c'erano già le bozze social vecchie,
> queste **non vengono ri-generate** automaticamente. Per forzare:
> vai su **Actions → 📱 Genera bozze social → Run workflow** e
> mettendo `force: true`.

---

## 7. Attivare/disattivare la modalità emergenza

Il sito ha una modalità emergenza che si attiva da un singolo file.
La home cambia layout, banner rosso in cima.

### Attivare:

1. Apri:
   <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/edit/main/data/emergenza.json>

2. Cambia in:
   ```json
   {
     "attiva": true,
     "tipo": "rosso",
     "titolo": "Emergenza alluvione in corso",
     "descrizione": "Evacuata l'area di via Italo Belardi. Rifugiarsi ai piani alti."
   }
   ```

3. Commit changes.

4. **Entro 5 minuti** la home mostra il banner emergenza in cima e
   riorganizza tutto il layout.

### Disattivare:

Stesso file, cambia `"attiva": false`. Commit. Sito torna normale in
5 minuti.

---

## 8. Aggiornare l'allerta meteo

L'allerta meteo si aggiorna in 2 modi:

### Modo A — Automatico (controllato da workflow)

Il workflow `check-allerta.yml` gira ogni ora e legge il bollettino
del Centro Funzionale Lazio. Se il livello cambia (verde → giallo →
arancione → rosso), aggiorna `data/allerta.json` e committa da solo.

Tu non devi fare nulla, succede in background.

### Modo B — Manuale (per casi speciali)

1. Apri:
   <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/edit/main/data/allerta.json>

2. Cambia il `livello` (es. `"giallo"` → `"arancione"`) e aggiorna
   `titolo` e `descrizione`.

3. Commit changes.

---

## 9. Cose che il sito fa DA SOLO (non devi farle tu)

| Cosa | Quando | Output |
|---|---|---|
| Build + deploy Aruba | Ogni push su `main` | Sito aggiornato in ~3 min |
| Build + deploy GitHub Pages (preview) | Ogni push su `main` | Preview a `sviluppoitaliadigitale.github.io/sito-pc-genzano/` |
| Verifica allerta meteo Lazio | Ogni ora | Aggiorna `data/allerta.json` se cambia |
| Pubblicazione articoli calendarizzati | Ogni notte 06:00 UTC | Articoli con `date` futura entrano automaticamente al passare del giorno |
| Audit completo del sito | Lunedì 09:00 UTC | Issue settimanale con eventuali problemi |
| Verifica link rotti | Lunedì 10:00 UTC | Issue se trova link 404 |
| Verifica fonti AGID | Lunedì 06:00 UTC | Issue se le fonti AGID cambiano (rumorose, ignorale se vuoi) |
| Smoke test post-deploy | Dopo ogni deploy | Verifica che il sito risponda 200 |
| Audit accessibilità Lighthouse | Dopo ogni deploy | Report accessibilità |
| Cover automatica articoli | Push articolo senza foto | Genera cover tipografica blu+titolo |
| Foto da Wikipedia/NASA/USGS | Push con marker `# TODO-foto-*` | Scarica + applica fascia blu |
| **Bozze social X/FB/IG/TG** | Push articolo | Crea `social-bozze/<slug>/` |
| **Immagini Instagram (post + carosello + story)** | Push articolo | Crea `static/images-social/` |

---

## 10. Risoluzione problemi mobile

### «Il workflow è rosso ❌»

Vai su <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions>,
clicca sul workflow rosso, leggi l'errore. Le cause più comuni:

- **Build Hugo rotta**: probabilmente un errore nel frontmatter
  (esempio: `date:` con timezone, virgolette mancanti). Apri il file,
  correggi, commit.
- **GEMINI_API_KEY non configurata**: vai su Settings → Secrets,
  configurala. La trovi gratuita su <https://aistudio.google.com/apikey>.
- **Errore 503 Gemini**: temporaneo, lancia di nuovo il workflow tra
  10-30 minuti (tasto «Re-run failed jobs»).

### «Non vedo le bozze social»

Verifica che:
1. Il workflow `📱 Genera bozze social` sia andato a buon fine (verde ✅).
2. Hai dato qualche minuto al refresh. La cartella `social-bozze/<slug>/`
   compare nel repo dopo che il workflow ha committato.

### «Le bozze sono fatte male»

Modifica le rules in <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/tree/main/.claude/rules>
(specialmente `02-content-design-pa.md`) e fai commit. Al prossimo
articolo le bozze seguiranno la nuova policy.

### «L'articolo non si vede sul sito ma il workflow è verde»

Controlla la `date:` nel frontmatter:
- Se è `>` di oggi → l'articolo è calendarizzato, comparirà al
  passare del giorno (alle 06:00 UTC del giorno X gira il workflow
  `pubblica-programmata.yml`).
- Se è `≤` di oggi e l'articolo non c'è → potrebbe essere `draft: true`
  per errore. Apri il file, cambia in `draft: false`, commit.
- Se hai pubblicato 2 articoli nella stessa giornata e uno appare
  in cima all'archivio invece del più recente → manca l'orario nel
  `date:`. Il formato deve essere `AAAA-MM-GGT00:01:00+02:00` per
  il primo, `T00:02:00+02:00` per il secondo, ecc. (orari minimi
  crescenti). Da PC: `python3 scripts/fix-ordering-articoli-stesso-giorno.py`
  fa tutto in un colpo. Da mobile: modifica i 2 articoli a mano via
  GitHub web editor. Specifiche in `MANUALE-SITO.md` § frontmatter
  `date`.

### «Voglio cancellare un articolo»

Vai sul file `.md`, apri, tocca il cestino 🗑️ in alto a destra,
commit. Al deploy successivo l'articolo sparisce dal sito.

> Se l'articolo è stato indicizzato da Google e vuoi rimuoverlo
> velocemente: aggiungi anche un redirect nel `.htaccess`
> (vedi <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/edit/main/themes/flavour-pcgenzano/static/.htaccess>).

---

## Quick reference (link da salvare nei segnalibri mobile)

| Cosa | Link |
|---|---|
| Repo principale | <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano> |
| Nuovo articolo | <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/new/main/content/comunicazioni> |
| Modifica allerta | <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/edit/main/data/allerta.json> |
| Modifica emergenza | <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/edit/main/data/emergenza.json> |
| Workflow CI | <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions> |
| Bozze social pronte | <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/tree/main/social-bozze> |
| Immagini social | <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/tree/main/static/images-social> |
| Issue aperte | <https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/issues> |
| Sito live | <https://www.protezionecivilegenzano.it/> |

---

## Una cosa importante

Da mobile **fai solo le cose semplici**: pubblica articoli, modifica
testi, attiva/disattiva emergenza, copia bozze sui social.

Tutte le **modifiche strutturali** (template, layout, nuove sezioni,
modifiche al CSS, fix workflow, gestione del repo) richiedono il PC
con Claude Code attivo. Quando ti serve, programma una sessione PC
con un Claude Code aperto e procedi da lì.
