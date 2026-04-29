# Generazione bozze social automatica

Sistema per generare bozze di post social (X, Facebook, Instagram, Telegram) +
immagini Instagram (post 1080×1080, story 1080×1920) a partire dagli articoli
del sito istituzionale.

## Cosa fa

Per ogni articolo in `content/comunicazioni/*.md`:

1. **`scripts/genera-social.py`** chiama Google Gemini API e produce 4 file di
   testo in `social-bozze/<slug>/` (uno per ogni piattaforma) seguendo le
   regole istituzionali AGID + DPC + social-media-policy del Gruppo
   (caricate automaticamente da `.claude/rules/`).

2. **`scripts/genera-immagini-social.py`** usa Pillow per generare 2 immagini
   Instagram con template istituzionale (logo + brand + cover articolo + URL
   sito) salvate in `static/images-social/<slug>-instagram-{post,story}.webp`.

## Setup iniziale (una sola volta)

### 1. Chiave Gemini API (gratuita)

Vai su <https://aistudio.google.com/apikey> e crea una API key.
Tier gratuito: 1.500 richieste/giorno (largamente sufficiente).

### 2. In locale

Aggiungi a `~/.bashrc`:

```bash
export GEMINI_API_KEY="incolla-qui-la-chiave"
```

Poi:

```bash
source ~/.bashrc
echo $GEMINI_API_KEY  # deve mostrare la chiave
```

### 3. Su GitHub (per workflow automatico)

`Settings → Secrets and variables → Actions → New repository secret`

- Name: `GEMINI_API_KEY`
- Value: la chiave

### 4. Dipendenze locali

```bash
sudo apt install -y fonts-liberation python3-pil
```

## Uso quotidiano

### Singolo articolo

```bash
bash scripts/genera-social.sh content/comunicazioni/2026-04-20-articolo.md
```

Output:

- `social-bozze/2026-04-20-articolo/x.txt`
- `social-bozze/2026-04-20-articolo/facebook.txt`
- `social-bozze/2026-04-20-articolo/instagram.txt`
- `social-bozze/2026-04-20-articolo/telegram.txt`
- `social-bozze/2026-04-20-articolo/README.md`
- `static/images-social/2026-04-20-articolo-instagram-post.webp`
- `static/images-social/2026-04-20-articolo-instagram-story.webp`

### Tutti gli articoli pubblicati (batch retroattivo)

```bash
bash scripts/genera-social.sh --all
```

Salta automaticamente gli articoli che hanno già le bozze (usa `--force` per
sovrascrivere).

### Solo dopo una data

```bash
bash scripts/genera-social.sh --since 2026-04-01
```

### Anteprima (dry-run, niente file scritti)

```bash
bash scripts/genera-social.sh --dry-run content/comunicazioni/<file>.md
```

## Workflow automatico (GitHub Action)

Al **push su `main`** che modifica un articolo `content/comunicazioni/*.md`,
il workflow `genera-social-bozze.yml`:

1. Identifica gli articoli toccati nel commit
2. Genera le bozze per ognuno
3. Genera le immagini Instagram
4. Committa il tutto con messaggio `[skip-social] Bozze social: ...`

Il marker `[skip-social]` impedisce ricorsioni infinite.

Si può anche lanciare manualmente da `Actions → 📱 Genera bozze social automatiche → Run workflow`.

## Costi

Tier gratuito Gemini: **1.500 richieste/giorno**. Per il tuo volume tipico
(1-2 articoli/giorno) sei a 0,1% del limite. **Costo annuale stimato: 0 €**.

Se per qualche motivo superassi il limite, Google blocca semplicemente le
chiamate fino al giorno dopo (non ti spilla soldi).

## Cosa NON fa

- **Non pubblica** automaticamente sui social. Le bozze sono per copia/incolla
  manuale (scelta voluta: tu hai sempre il controllo finale).
- **Non aggiunge informazioni** che non sono nell'articolo (mai inventa
  numeri, date, fonti).
- **Non sostituisce la rilettura umana**: la AI può commettere errori. Sempre
  rileggere prima di pubblicare.

## Personalizzare lo stile

Le rules istituzionali sono in `.claude/rules/`. Modificale per cambiare:

- Tono dei testi → `02-content-design-pa.md`
- Hashtag stabili → `02-content-design-pa.md`
- Regole di accessibilità social → `03-accessibility.md`
- Distinzione badge Allerta/Emergenza → `06-protezione-civile-scientifica.md`

Allo script non serve modifica: legge automaticamente i file aggiornati al
prossimo run.

## Output

| Cartella | Contenuto | Deployata sul sito? |
|---|---|---|
| `social-bozze/<slug>/` | 4 .txt + README.md | ❌ no (cartella fuori da Hugo) |
| `static/images-social/<slug>-instagram-*.webp` | 2 immagini | ✅ sì (path pubblico `/images-social/...`) |
