_[Indice manuale](README.md)_

# Parte 9 — File dati `data/` e stati del sito

I file nella cartella `data/` pilotano comportamenti dinamici del sito **senza toccare i template**. Questa è la strada preferita per aggiornare card, banner, numeri di emergenza, canali social. Tutti i file sono letti da Hugo a build time: modifiche richiedono un nuovo build per comparire online (automatico al push).

### 9.1 — Panoramica dei file dati

| File | Formato | Scopo |
|---|---|---|
| `emergenza.json` | JSON | Attiva/disattiva modalità emergenza sulla home |
| `allerta.json` | JSON | Livello allerta meteo corrente (verde / giallo / arancione / rossa) |
| `risk_cards.yaml` | YAML | card della pagina Rischi e Prevenzione |
| `numeri_utili.yaml` | YAML | Numeri di emergenza mostrati in home, contatti, footer |
| `quick_links.yaml` | YAML | CTA del hero + "Cosa fare in caso di..." + servizi |
| `social_links.yaml` | YAML | Canali social + linktree |
| `codici_colore.yaml` | YAML | Descrizioni colori allertamento (pagina Allerte Meteo) |
| `glossario.yaml` | YAML | Voci del glossario inline (sigle PC sostituite da popover) |
| `aree_emergenza.yaml` | YAML | 16 punti del Piano Emergenza (10 AA + 2 AS + 4 AR) — coordinate verificate |
| `idranti.yaml` | YAML | Idranti antincendio sul territorio (template, da popolare con dati VVF) |
| `dae.yaml` | YAML | Defibrillatori semi-Automatici Esterni (template, registro IRC ai sensi L. 116/2021) |

Regola d'oro: **prima di creare un nuovo partial o template, verifica se la stessa cosa può essere fatta con un data file**. Questo mantiene il sito manutenibile da chi non conosce Hugo.

### 9.2 — `emergenza.json` (modalità emergenza home)

**Schema completo:**

```json
{
  "attiva": false,
  "tipo": "blu",
  "titolo": "",
  "descrizione": "",
  "link": "",
  "ultimo_aggiornamento": ""
}
```

**Campi:**
- `attiva` *(boolean, obbligatorio)*: `true` attiva la modalità emergenza; `false` la disattiva. Quando è `true` la homepage cambia layout: compare in alto il banner rosso e i numeri di emergenza, l'hero diventa compatto e le notizie scendono più in basso. Vedi `themes/flavour-pcgenzano/layouts/index.html`.
- `tipo` *(string)*: `blu` | `giallo` | `arancione` | `rosso`. Pilota il colore del banner. `rosso` = emergenza massima (terremoto, alluvione in corso, evacuazione). `blu` = informativa istituzionale.
- `titolo` *(string)*: breve, in maiuscoletto o frase istituzionale. Esempi accettabili: "EMERGENZA IN CORSO — RESTATE IN CASA", "EVENTO SISMICO — VERIFICHE IN CORSO".
- `descrizione` *(string)*: una o due frasi brevi. **Niente punto esclamativo**, niente allarmismo gratuito. Indica fonte e azione.
- `link` *(string, opzionale)*: URL a un articolo di dettaglio sul sito o a una pagina istituzionale. Se vuoto, il banner non mostra pulsante.
- `ultimo_aggiornamento` *(string)*: ISO date-time dell'ultimo aggiornamento del banner (compare in piccolo sul banner). Formato consigliato: `2026-04-21T14:30:00+02:00`.

#### Procedura — Attivare la modalità emergenza

1. **Verifica la fonte**: la decisione di attivare la modalità emergenza è del responsabile del Gruppo o del COC, non del redattore. Non attivare mai di propria iniziativa.
2. Apri `data/emergenza.json`.
3. Compila i campi:

   ```json
   {
     "attiva": true,
     "tipo": "arancione",
     "titolo": "ALLERTA METEO ARANCIONE SUI CASTELLI ROMANI",
     "descrizione": "Il Centro Funzionale Regionale prevede piogge intense fino alle 24:00 di mercoledi. Limitare gli spostamenti.",
     "link": "/comunicazioni/2026-04-21-allerta-arancione-castelli/",
     "ultimo_aggiornamento": "2026-04-21T09:15:00+02:00"
   }
   ```

4. Commit: `Attivazione modalità emergenza — allerta arancione`.
5. Push: il sito si aggiorna in 2–3 minuti.
6. **In parallelo**: pubblica l'articolo linkato (vedi Parte 1).

#### Procedura — Disattivare la modalità emergenza

1. Verifica con il responsabile che l'evento sia chiuso.
2. Apri `data/emergenza.json`.
3. Riporta `attiva` a `false`. Svuota gli altri campi (lascia `""` o `"blu"`), per non lasciare residui in repository:

   ```json
   {
     "attiva": false,
     "tipo": "blu",
     "titolo": "",
     "descrizione": "",
     "link": "",
     "ultimo_aggiornamento": ""
   }
   ```

4. Commit: `Chiusura modalità emergenza — allerta rientrata`.
5. Pubblica in parallelo un articolo di aggiornamento operativo ("allerta rientrata, nessuna criticità rilevata").

### 9.3 — `allerta.json` (banner allerta meteo)

**Schema:**

```json
{
  "livello": "verde",
  "titolo": "NESSUNA ALLERTA",
  "descrizione": "Non sono previsti fenomeni significativi sul nostro territorio.",
  "ultimo_aggiornamento": "2026-04-23T16:07:32+02:00",
  "ultimo_controllo": "2026-04-27T11:00:00+02:00"
}
```

**Campi:**
- `livello` *(string, obbligatorio)*: `verde` | `gialla` | `arancione` | `rossa`. Pilota colore della barra allerta in cima a ogni pagina.
- `titolo` *(string)*: es. "ALLERTA GIALLA SUI CASTELLI ROMANI".
- `descrizione` *(string)*: una frase sintetica.
- `ultimo_aggiornamento` *(string ISO 8601)*: timestamp dell'**ultimo cambio di livello**. Cambia solo quando il livello reale passa da uno stato all'altro (es. verde → gialla).
- `ultimo_controllo` *(string ISO 8601)*: timestamp dell'**ultima verifica del bollettino DPC**. Aggiornato dal workflow ogni 6 ore (anche se il livello è invariato), così la barra mostra al cittadino una data sempre fresca con il testo "Verificato: …". Sulla homepage il JS lato browser aggiorna ulteriormente questo testo all'ora locale ad ogni visita.

**Aggiornamento automatico**: il workflow `check-allerta.yml` (vedi Parte 10) interroga il feed ufficiale DPC **4 volte/h** (ai minuti 7, 22, 37, 52 — scaglionati fuori dai picchi GitHub Actions) e aggiorna `allerta.json` quando il livello cambia OPPURE quando sono passate ≥5h45min dall'ultimo controllo. Limita i commit a max 4/giorno + cambi di livello. Latenza media al cambio livello DPC: ~7-8 min. Nella maggior parte dei casi **non serve intervenire manualmente**.

> **Nota tecnica (10 maggio 2026)**: i cron `*/N` (in particolare `*/5`) **non sono affidabili** su GitHub Actions — verifica empirica del 10 maggio mostra 0 run in 42 minuti col `*/5`. Documentazione GH: *"To decrease the chance of delay, schedule your workflow to run at a different time of the hour."* Cron espliciti scaglionati hanno aderenza molto migliore.

**Aggiornamento manuale**: serve solo se l'automazione fallisce o se si vuole forzare un messaggio istituzionale specifico. Modifica il file, commit, push. **Nota**: al successivo ciclo orario il workflow sovrascriverà il tuo intervento con il valore letto dal feed DPC. Per evitarlo, disabilita temporaneamente il workflow (vedi 10.9).

**Fonte dati ufficiale**: CSV pubblicato dal Dipartimento Protezione Civile, mirror mantenuto da opendatasicilia: `https://raw.githubusercontent.com/opendatasicilia/DPC-bollettini-criticita-idrogeologica-idraulica/refs/heads/main/data/bollettini/bollettino-oggi-comuni-latest.csv`.

### 9.4 — `risk_cards.yaml` (Rischi e Prevenzione)

Contiene le card mostrate nella pagina hub "Rischi e Prevenzione" e nella homepage. Ogni card rimanda a una sottopagina di `content/rischi-prevenzione/`.

**Schema di ogni card:**

```yaml
- id: "rischio-sismico"
  titolo: "Rischio Sismico"
  icona: "bi-tsunami"
  colore: "warning"
  classe_icona: "si-orange"
  descrizione_breve: "Cosa fare prima, durante e dopo un terremoto."
  peso: 1
```

**Campi:**
- `id`: slug della pagina di dettaglio (`/rischi-prevenzione/<id>/`). Deve esistere in `content/rischi-prevenzione/<id>/_index.md` o `<id>.md`.
- `titolo`: titolo card, coerente con l'H1 della pagina di dettaglio.
- `icona`: nome icona Bootstrap Italia (prefisso `bi-`). Vedi [icons.getbootstrap.com](https://icons.getbootstrap.com/).
- `colore`: variante Bootstrap (`primary`, `warning`, `danger`, `info`, `success`, `dark`). Pilota il bordo/sfondo della card.
- `classe_icona`: classe custom per colorare l'icona (`si-orange`, `si-blue`, `si-teal`, `si-green`, `si-dark`). Definite in `custom.css`.
- `descrizione_breve`: una frase max 100 caratteri.
- `peso`: intero, determina l'ordine di visualizzazione (1 = prima, 9 = ultima).

**Modifiche tipiche:**
- Aggiungere una card nuova: aggiungi blocco YAML + crea la pagina di dettaglio in `content/rischi-prevenzione/<id>.md`. Ricorda di aggiornare l'archivio e il menu se serve.
- Togliere una card: rimuovi il blocco + considera di lasciare la pagina di dettaglio come archivio (vedi 8.4 scenario B) o rimuoverla.
- Riordinare: modifica solo i `peso`.

### 9.5 — `numeri_utili.yaml` (numeri di emergenza)

**Regola chiave**: nel Lazio il **solo numero da comunicare al cittadino è il 112** (NUE). 115, 118, 1515 non sono più il riferimento. Qualunque AI che proponga di aggiungerli come "numeri da chiamare" va corretta.

**Struttura:**

```yaml
emergenza:      # Numeri in evidenza massima
  - numero: "112"
    nome: "Numero Unico Emergenza (NUE)"
    descrizione: "..."
    icona: "bi-telephone-fill"
    principale: true

utili:          # Numeri utili secondari
  - numero: "1530"
    nome: "Guardia Costiera"
    ...

locale:         # Numeri del Gruppo (MAI per emergenze)
  - numero: "+39 06 9362600"
    nome: "Segreteria Gruppo PC Genzano"
    ...
    nota: "NON per emergenze"
```

**Campi:**
- `numero`: formato leggibile con spaziature (`112`, `803 555`, `+39 06 9362600`).
- `nome`: ufficiale del servizio.
- `descrizione`: a cosa serve, una frase.
- `icona`: classe Bootstrap Italia.
- `principale`: se `true`, la card è in evidenza grafica maggiore.
- `nota` (opzionale): testo di avviso (tipicamente "NON per emergenze" per i numeri del Gruppo).

### 9.6 — `quick_links.yaml` (CTA hero + servizi)

sezioni distinte:
- `principali`: pulsanti del hero homepage (tipicamente 3).
- `cosa_fare`: card "Cosa fare in caso di..." in homepage.
- `servizi`: card "Servizi per il cittadino".

Campi comuni: `titolo`, `url`, `icona` (Bootstrap Italia icon), `classe` o `classe_icona`, `descrizione`, opzionalmente `azione` (testo sul pulsante).

Regole:
- Ogni URL deve esistere come pagina nel sito (altrimenti il render-link hook mostra testo inerte solo in contenuti markdown, ma in questi partial i link sono generati direttamente: qui un URL inesistente produce un 404 vero).
- Mantieni numero card coerente con il layout (3 principali, 4 cosa_fare, 4 servizi è la configurazione testata).

### 9.7 — `social_links.yaml`

Lista `canali:` + singolo `linktree:`. Campi per canale: `nome`, `url`, `icona`, `classe_btn`, `aria_label`, `descrizione`.

Aggiungere un canale nuovo: aggiungi blocco + verifica che l'icona Bootstrap Italia esista (`bi-whatsapp`, `bi-youtube`, ecc.). Rimuovere un canale: togli il blocco; i partial che usano `range canali` si adattano.

### 9.8 — `codici_colore.yaml`

Pilota la pagina "Allerte Meteo" sezione "Significato dei colori". Ogni livello ha: `livello` (slug), `titolo`, `colore_bg`, `colore_testo`, `significato`, `cosa_fare`, `icona`. I colori sono coordinati con la palette ufficiale del sistema di allertamento nazionale.

**Non modificare** `colore_bg` e `colore_testo` senza ricontrollare il contrasto WCAG (≥ 4.5:1 testo normale).

### 9.9 — Validazione data files

Prima di commit, verifica:

- **JSON** (`emergenza.json`, `allerta.json`): formato valido. Errori di virgola o virgolette rompono il build. Usa un linter o `python3 -m json.tool < data/emergenza.json`.
- **YAML**: indentazione a 2 spazi, niente tab. Stringhe con caratteri speciali tra virgolette doppie. Usa `python3 -c "import yaml; yaml.safe_load(open('data/risk_cards.yaml'))"`.
- **Caratteri accentati**: sempre UTF-8, mai entità HTML (`è`, non `&egrave;`).

Un `data` rotto blocca `hugo --minify` e il deploy fallisce: il sito resta sulla versione precedente e il monitoring Actions mostra un fallimento rosso.

---

_[Indice manuale](README.md)_

[← Parte 08 — Modificare e cancellare contenuti](parte-08-modificare-e-cancellare-contenuti.md) · [↑ Indice](README.md) · [Parte 10 — GitHub Actions e automazioni →](parte-10-github-actions-e-automazioni.md)
