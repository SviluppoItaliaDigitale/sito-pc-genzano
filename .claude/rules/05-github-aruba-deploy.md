# GitHub + Aruba — Deploy e Infrastruttura

## Ambienti di pubblicazione

Il sito viene pubblicato su due ambienti distinti ad ogni push su `main`:

| Ambiente | URL | Metodo |
|---|---|---|
| Aruba (produzione) | https://www.protezionecivilegenzano.it/ | FTP via GitHub Actions |
| GitHub Pages (preview) | https://sviluppoitaliadigitale.github.io/sito-pc-genzano/ | GitHub Pages API |

## Workflow CI/CD

Il file `.github/workflows/deploy.yml` gestisce il deploy automatico:
1. Esegue `hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"` per Aruba
2. Esegue `hugo --minify` per GitHub Pages
3. Carica su Aruba via FTP usando i secret GitHub: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`
4. Pubblica su GitHub Pages tramite l'azione ufficiale

## Cartelle escluse dal deploy FTP (contenuto lato server)

L'azione FTP usa `dangerous-clean-slate: false` e una lista di esclusioni per proteggere contenuto gestito manualmente sul server Aruba. Queste cartelle **non vengono né caricate né aggiornate né rimosse** dal deploy:

```yaml
exclude: |
  **/documenti/**
```

**Conseguenza operativa:** un file depositato via git in `static/documenti/` **non arriverà mai su Aruba**. Compare solo nella build locale e su GitHub Pages. La cartella `static/documenti/` resta gestita manualmente sul server Aruba perché contiene materiale ereditato dal sito precedente (pieghevoli, kit "Io Non Rischio", schede storiche) mai migrato nel repo.

**Storico delle esclusioni (rimosse aprile 2026):** fino al 24 aprile 2026 la lista escludeva anche `**/cartelli/**`, `**/giochi-bambini/**`, `**/formazionepc/**`, `**/quizpc/**`. Dopo l'incidente del cartello AR4 Salesiani (un audit del sito ha rilevato che l'immagine era mancante sul server, ma non c'era modo di accorgersene dal repo), queste esclusioni sono state rimosse per eliminare il drift tra repo e server. I file vivono ora nel repo come unica fonte di verità e deployano automaticamente.

**Cartelle canoniche per nuovi file statici depositati via git:**

| Contenuto | Cartella | URL pubblico |
|---|---|---|
| Manuali tecnici permanenti citati da più articoli | `static/manuali/` | `/manuali/nome.pdf` |
| Allegati specifici di un articolo | `static/allegati/AAAA/` | `/allegati/AAAA/nome.pdf` |
| Comunicati stampa firmati | `static/comunicati/AAAA/` | `/comunicati/AAAA/nome.pdf` |
| Segnaletica aree di emergenza | `static/cartelli/` | `/cartelli/nome.png` |
| Immagini di copertina / foto evento | `static/images/` | `/images/nome.webp` |
| Archivio storico immagini | `static/images/archivio-storico/` | `/images/archivio-storico/nome.ext` |
| Pittogrammi ISO 7010 (sicurezza standard) | `static/pittogrammi/iso7010/` | `/pittogrammi/iso7010/nome.svg` |
| Pittogrammi ARASAAC (comprensione cognitiva) | `static/pittogrammi/arasaac/` | `/pittogrammi/arasaac/nome.png` |

Se aggiungi nuove esclusioni al workflow, aggiorna anche questa tabella e la **Parte 1.10** e **Parte 10.2** di `MANUALE-SITO.md`.

## Regole operative

- Il branch `main` è il branch di produzione: ogni push avvia il deploy.
- I secret FTP non vanno mai committati nel repository.
- Monitora i deploy nella tab Actions del repository GitHub.
- In caso di build rotta, il deploy non avviene: il sito rimane all'ultima versione funzionante.

## Regole di compatibilità

Ogni modifica deve essere compatibile con:
- Build statica di Hugo (nessun server-side rendering, nessuna API runtime)
- Deploy FTP su Aruba (percorsi degli asset devono essere corretti per entrambi i baseURL)
- GitHub Pages con subpath `/sito-pc-genzano/` (usa `{{ absURL }}` o `{{ relURL }}` nei template, mai percorsi assoluti hardcoded)
- Certificato HTTPS esistente su Aruba (non modificare la configurazione DNS senza coordinamento)

## Rollback

Per tornare a una versione precedente:
```bash
git revert HEAD          # Crea un commit di ripristino (preferibile)
git push origin main     # Avvia il redeploy
```
Evita `git reset --hard` su `main` se il commit è già stato pushato.

## Header HTTP — `.htaccess` su Aruba

Il file `themes/flavour-pcgenzano/static/.htaccess` configura gli header di sicurezza che Apache invia su Aruba. Aruba supporta `mod_headers` ma GitHub Pages no, quindi questo file è effettivo **solo in produzione**.

**Permissions-Policy (header sensibile):**

```apache
Header always set Permissions-Policy "geolocation=(self), microphone=(), camera=()"
```

- `geolocation=(self)` — il sito può usare la Geolocation API del browser. È necessario per il bottone "Centra sulla mia posizione" sulla mappa `/cartografia/`.
- `microphone=()` e `camera=()` — negati a tutte le origini (non servono).

**ATTENZIONE:** non sostituire `geolocation=(self)` con `geolocation=()`. La forma `()` (lista vuota di origini) **disabilita la Geolocation API anche per il sito stesso**, e il browser blocca silenziosamente `navigator.geolocation.getCurrentPosition()` mostrando un errore "Geolocation has been disabled in this document by permissions policy". Questo è successo una volta in produzione e ha rotto il bottone della mappa cartografia. Se aggiungi nuove API (es. `payment`, `usb`), aggiungile in coda al valore con `(self)` o `()` esplicito.

## Workflow GitHub Actions — qualità YAML

I file in `.github/workflows/*.yml` sono validati da GitHub al momento del push. Se la validazione fallisce il run viene marcato "completed failure" con 0 job eseguiti, ma **nessuna issue viene aperta** e il problema può passare inosservato per settimane.

**Pattern velenoso da evitare** (causa errore di parsing YAML strict):

```bash
DIFF=$(python3 -c "
import datetime
try:
  d = datetime.datetime.strptime('$REV', '%Y-%m-%d').date()
  print((datetime.date.today() - d).days)
except Exception:
  print(-1)
")
```

Le righe Python (`import…`, `try:`, `print…`) iniziano a colonna 1, e il parser YAML le legge come nuove chiavi top-level rompendo la struttura. **Sostituiscilo con aritmetica bash usando `date`**:

```bash
TS=$(date -u -d "$REV" +%s 2>/dev/null || echo "")
[ -n "$TS" ] && DIFF=$(( ($(date -u +%s) - TS) / 86400 )) || DIFF=-1
```

Per validare un workflow prima del push:
```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/<file>.yml'))"
```

Se python3 yaml lo accetta, GitHub Actions lo accetterà sicuramente.

## Verifica prima del push

Prima di fare push su `main`, verifica sempre:
- `hugo server` non mostra errori in console
- Il build `hugo --minify` completa senza errori
- I percorsi di immagini, PDF e asset statici sono corretti
- Il frontmatter degli articoli usa il formato data `AAAA-MM-GG`
- Nessun articolo con `draft: false` ha contenuti incompleti
- Se hai modificato un file `.github/workflows/*.yml`, validalo con `python3 -c "import yaml; yaml.safe_load(open(...))"` prima del push
- Se hai modificato `.htaccess`, ricontrolla che `Permissions-Policy: geolocation=(self)` resti integro

## Divieti

- Non fare push su `main` con un build rotto.
- Non committare credenziali, token o secret nel repository.
- Non modificare il workflow CI/CD senza verificare la compatibilità con entrambi gli ambienti.
- Non introdurre asset con percorsi hardcoded che funzionino solo su un ambiente.
- Non eliminare o rinominare file già pubblicati senza gestire i redirect appropriati (Aruba non ha redirect automatici).
