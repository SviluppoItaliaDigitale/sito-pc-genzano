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

2. **`scripts/genera-immagini-social.py`** usa Pillow per generare immagini
   Instagram con template istituzionale (logo + brand + cover articolo + URL
   sito) salvate **nella stessa cartella** `social-bozze/<slug>/` accanto ai
   testi (`instagram-post.jpg` per singola foto, `instagram-post-N.jpg` per
   carosello, `instagram-story.jpg` per la story). Comodo da scaricare
   insieme via mobile.

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
- `social-bozze/2026-04-20-articolo/instagram-post.jpg` (o `-1.jpg`, `-2.jpg`, … se carosello)
- `social-bozze/2026-04-20-articolo/instagram-story.jpg`

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

Tutto il materiale di un articolo (testi + immagini Instagram) sta in **una sola
cartella**, comoda da scaricare via mobile da GitHub.

| Cartella | Contenuto | Deployata sul sito? |
|---|---|---|
| `social-bozze/<slug>/` | 4 .txt + README.md + `instagram-post*.jpg` + `instagram-story.jpg` | ❌ no (cartella fuori da Hugo, solo archivio di lavoro) |

> **Nota storica (2 maggio 2026)**:
> 1. Le immagini stavano in `static/images-social/` con URL pubblico Aruba.
>    Spostate in `social-bozze/<slug>/` perché l'URL pubblico non era usato
>    da nessuna parte del sito e tenere tutto insieme è più comodo da mobile.
> 2. Il formato output era **WebP** (più piccolo) ma **Instagram non lo
>    accetta** in upload (web e app mobile lo rifiutano). Cambiato a **JPEG
>    quality 90 progressive**, universalmente accettato da IG, Facebook, X,
>    Telegram, LinkedIn. Le immagini sono ~2-3x più pesanti ma il peso non
>    è critico (sono per copia/incolla manuale, non per il sito pubblico).
