#!/usr/bin/env python3
"""Genera bozze di post social (X, Facebook, Instagram, Telegram) per gli
articoli del sito a partire dal frontmatter Markdown.

Funzionamento:
  - Legge le rules istituzionali da .claude/rules/*.md (AGID, accessibility,
    protezione civile, social-media-policy del Gruppo).
  - Le inietta nel system prompt di Gemini API.
  - Per ogni articolo, passa il frontmatter + estratto del corpo come user
    message e chiede 4 testi calibrati per piattaforma.
  - Salva le bozze in social-bozze/<slug>/ come 4 file .txt.

Modalità:
  python3 scripts/genera-social.py path/articolo.md       # singolo articolo
  python3 scripts/genera-social.py --all                  # tutti i pubblicati
  python3 scripts/genera-social.py --since 2026-04-01     # da una data in poi
  python3 scripts/genera-social.py --dry-run path/...     # mostra senza scrivere
  python3 scripts/genera-social.py --force path/...       # sovrascrive bozze esistenti

Variabili d'ambiente richieste:
  GEMINI_API_KEY    chiave Google AI Studio (gratuita)

Modello: gemini-2.5-flash (tier gratuito, ~1500 req/giorno)
Endpoint: https://generativelanguage.googleapis.com/v1beta/models/...

Costo: zero entro tier gratuito. Articolo singolo: 1 chiamata API.
"""

import argparse
import datetime
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_COMUNICAZIONI = ROOT / "content" / "comunicazioni"
RULES_DIR = ROOT / ".claude" / "rules"
SOCIAL_BOZZE = ROOT / "social-bozze"

# Le rules che lo script inietta nel system prompt. Ordinate per rilevanza
# per la generazione dei post social (no manuale Hugo, no setup tecnico).
RULES_FILES = [
    "02-content-design-pa.md",   # linguaggio AGID, hashtag, struttura crisi
    "03-accessibility.md",       # alt text, max 2 emoji, no Unicode decorativi
    "06-protezione-civile-scientifica.md",  # codici colore, badge, gerarchia fonti
]

GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_ENDPOINT = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)

SITO_BASE = "https://www.protezionecivilegenzano.it"

# Schema strutturato per la risposta JSON di Gemini.
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "x": {
            "type": "string",
            "description": "Testo per X (Twitter), max 280 caratteri INCLUSO l'URL.",
        },
        "facebook": {
            "type": "string",
            "description": "Testo per Facebook, 200-400 caratteri ideali, con URL articolo.",
        },
        "instagram": {
            "type": "string",
            "description": "Caption Instagram con ESATTAMENTE 5 hashtag in fondo, separati dal testo da 3 righe vuote.",
        },
        "telegram": {
            "type": "string",
            "description": "Testo Telegram con Markdown (**bold**, [link](url) ecc.).",
        },
    },
    "required": ["x", "facebook", "instagram", "telegram"],
}


def stampa_err(msg: str) -> None:
    print(f"ERRORE: {msg}", file=sys.stderr)


def stampa_info(msg: str) -> None:
    print(msg, file=sys.stderr)


def carica_rules() -> str:
    """Concatena le rules istituzionali dal repo per il system prompt."""
    blocchi = []
    for nome in RULES_FILES:
        p = RULES_DIR / nome
        if not p.exists():
            stampa_err(f"Rule mancante: {p}")
            continue
        blocchi.append(f"# === {nome} ===\n\n{p.read_text(encoding='utf-8')}\n")
    if not blocchi:
        raise SystemExit("Nessuna rule trovata in .claude/rules/. Stop.")
    return "\n\n".join(blocchi)


def parse_frontmatter(testo: str) -> tuple[dict, str]:
    """Frontmatter YAML semplice (senza dipendenze): coppie chiave: valore.
    Ritorna (dict_frontmatter, corpo_articolo).
    """
    if not testo.startswith("---\n"):
        return {}, testo
    fine = testo.find("\n---", 4)
    if fine < 0:
        return {}, testo
    raw_fm = testo[4:fine].strip()
    body = testo[fine + 4:].lstrip("\n")

    fm = {}
    chiave_corrente = None
    for riga in raw_fm.split("\n"):
        if not riga.strip() or riga.lstrip().startswith("#"):
            continue
        m = re.match(r"^([a-zA-Z_][a-zA-Z0-9_]*):\s*(.*)$", riga)
        if m:
            chiave_corrente = m.group(1)
            valore = m.group(2).strip()
            if valore.startswith('"') and valore.endswith('"'):
                valore = valore[1:-1]
            elif valore == "":
                valore = ""
            fm[chiave_corrente] = valore
    return fm, body


def estrai_articolo(path: Path) -> dict | None:
    """Legge un articolo Hugo, estrae i campi utili. Salta drafts e date future."""
    try:
        testo = path.read_text(encoding="utf-8")
    except OSError as e:
        stampa_err(f"Impossibile leggere {path}: {e}")
        return None

    fm, body = parse_frontmatter(testo)

    if fm.get("draft", "").lower() in ("true", "yes", "1"):
        return None

    data_str = fm.get("date", "")
    m_data = re.match(r"(\d{4}-\d{2}-\d{2})", data_str)
    if not m_data:
        return None
    data_articolo = datetime.date.fromisoformat(m_data.group(1))
    if data_articolo > datetime.date.today():
        return None  # articolo futuro calendarizzato, non ancora pubblicato

    slug = path.stem
    url = f"{SITO_BASE}/comunicazioni/{slug}/"

    # Estratto del corpo: prime ~600 caratteri di testo "vero" (no shortcode)
    corpo_pulito = re.sub(r"\{\{[<%].+?[%>]\}\}", "", body, flags=re.DOTALL)
    corpo_pulito = re.sub(r"<[^>]+>", "", corpo_pulito)
    corpo_pulito = re.sub(r"\s+", " ", corpo_pulito).strip()
    estratto = corpo_pulito[:600]

    return {
        "path": str(path),
        "slug": slug,
        "title": fm.get("title", ""),
        "description": fm.get("description", ""),
        "badge": fm.get("badge", ""),
        "area": fm.get("area", ""),
        "date": m_data.group(1),
        "url": url,
        "estratto": estratto,
    }


def costruisci_system_prompt(rules: str) -> str:
    """System prompt completo per Gemini. Include rules + istruzioni operative."""
    return f"""Sei l'assistente social del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.
Il tuo unico compito è generare BOZZE di post social per 4 piattaforme partendo da un articolo del sito istituzionale.

Devi seguire RIGOROSAMENTE le regole istituzionali del Gruppo (estratte dalle rules del repo):

{rules}

# REGOLE OPERATIVE PER QUESTO TASK

Genera SEMPRE 4 testi distinti e calibrati per piattaforma:

## X (Twitter)
- LIMITE RIGIDO: 280 caratteri totali, INCLUSO l'URL.
- L'URL dell'articolo è lungo ~135 caratteri da solo.
- Quindi il TUO testo (frase + hashtag) deve stare in MAX 140 CARATTERI.
- Struttura: una sola frase incisiva (max 100 char) + URL + 2-3 hashtag.
- Niente emoji decorative.
- VIETATO: "leggi di più", "scopri", "non perdere", "imperdibile" — è linguaggio commerciale.
- Conta i caratteri PRIMA di rispondere. Se superi 280, riscrivi più corto.

## Facebook
- 200-400 caratteri ideali (ma non un limite duro).
- Apertura con tag istituzionale tra parentesi quadre, es. [AGGIORNAMENTO], [ALLERTA], [INFORMAZIONE].
- Testo informativo, voce attiva, frasi brevi.
- Link all'articolo nel corpo.
- 3-5 hashtag stabili in fondo.

## Instagram
- Caption ≤ 2200 caratteri.
- Apertura con tag istituzionale tra parentesi quadre.
- Testo informativo come Facebook.
- L'ULTIMA RIGA del testo (prima delle 3 righe vuote e degli hashtag)
  DEVE essere ESATTAMENTE questa frase, niente di più, niente di meno:

      Link in bio.

  È una frase chiusa di 12 caratteri con punto finale. NON aggiungere
  "per tutti i dettagli", "per saperne di più", "per maggiori
  informazioni", "per scoprire", "per leggere", o qualsiasi altra
  estensione. Solo "Link in bio." e basta.

- Dopo "Link in bio." metti 3 righe vuote.
- ESATTAMENTE 5 hashtag in fondo, su una sola riga separati da spazi.
- Selezione hashtag in base al BADGE dell'articolo (logica obbligatoria):
  * Allerta: #PCGenzano #Genzano #AllertaLazio #ProtezioneCivile #CastelliRomani
  * Emergenza: #PCGenzano #Genzano #NUE112 #AllertaLazio #ProtezioneCivile
  * Volontariato / Formazione / Evento: #PCGenzano #Genzano #ProtezioneCivile #Volontariato #CastelliRomani
  * Comunicazione / Aggiornamento / Informazione / Prevenzione: #PCGenzano #Genzano #ProtezioneCivile #GenzanoDiRoma #CastelliRomani

## Telegram
- Markdown supportato: **grassetto**, *italic*, [testo](url).
- Apertura con tag istituzionale tra parentesi quadre.
- Testo strutturato (bullet con · oppure "—").
- Link all'articolo IN GRASSETTO con etichetta "Leggi sul sito".
- 2-4 hashtag in fondo.

# DIVIETI ASSOLUTI (mai violarli, in nessun caso)

- Mai inventare informazioni che non sono nell'articolo (numeri, date, citazioni, fonti, esiti).
- Mai INVENTARE HASHTAG. Usa SOLO quelli della lista approvata sotto.
  Vietatissimi hashtag come #AlbanoLaziale, #Cecchina, #Vesuvio, #IncendioCecchina,
  o qualunque altro hashtag NON esplicitamente approvato.
- Mai usare caratteri Unicode decorativi (𝐁𝐎𝐋𝐃, ✰, 🅒, ecc.).
- Mai più di 2 emoji per post.
- Mai testo in MAIUSCOLO continuo (gli screen reader leggono come URLA).
- Mai "click qui", "scopri di più", "leggi di più", "non perdere", "imperdibile",
  "tutti i dettagli", "per maggiori informazioni" — linguaggio commerciale vietato.
- Mai amplificare disinformazione anche per smentirla.
- Per allerte/emergenze: mai esprimere panico né minimizzare, mai presentare il
  Gruppo come servizio attivabile direttamente dal cittadino (la chiamata va al 112).

# LISTA HASHTAG APPROVATI (è l'UNICA fonte ammessa, non inventarne altri)

Hashtag stabili (sempre disponibili):
- #PCGenzano (sempre presente)
- #Genzano (sempre presente)
- #ProtezioneCivile
- #AllertaLazio (solo per allerte/meteo)
- #NUE112 (solo per emergenze/sicurezza)
- #CastelliRomani
- #GenzanoDiRoma
- #Volontariato (solo per badge Volontariato)
- #Formazione (solo per badge Formazione)
- #Attività (solo per badge Attività)
- #Aggiornamento (solo per badge Aggiornamento)
- #Evento (solo per badge Evento)

NESSUN ALTRO HASHTAG è ammesso. Se la AI sente il bisogno di "specificare meglio"
con #LuogoSpecifico o #TemaSpecifico, deve trattenersi.

# DISTINZIONE CRITICA

Quando il badge è "Allerta" (evento PREVISTO) usa il futuro: «è previsto», «sono attesi».
Quando il badge è "Emergenza" (evento IN CORSO) usa il presente: «è in corso», «in atto».
Quando il badge è "Aggiornamento" (evento CONCLUSO) usa il passato: «è stato», «si è concluso».

# OUTPUT

Ritorna SOLO un JSON valido conforme allo schema con 4 chiavi: x, facebook, instagram, telegram.
Niente preamboli, niente conclusioni, niente Markdown wrapper. Solo JSON puro.
"""


def costruisci_user_prompt(art: dict) -> str:
    """User message: i dati dell'articolo per cui generare le bozze."""
    return f"""Genera le bozze social per questo articolo del sito istituzionale.

# DATI ARTICOLO

- Titolo: {art['title']}
- Data: {art['date']}
- Badge: {art['badge']}
- Area: {art['area'] or 'Non specificata'}
- URL canonico: {art['url']}

# DESCRIZIONE BREVE (frontmatter)

{art['description']}

# ESTRATTO DEL CORPO

{art['estratto']}

# OUTPUT ATTESO

JSON con 4 chiavi (x, facebook, instagram, telegram). Nessun preambolo, solo il JSON.
"""


def chiama_gemini(api_key: str, system_prompt: str, user_prompt: str,
                  retries: int = 2) -> dict | None:
    """Chiama Gemini API con retry. Ritorna il dict parsato dalla risposta JSON."""
    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": RESPONSE_SCHEMA,
            "temperature": 0.7,
            # 8192 = limite Gemini 2.5 Flash. I 4 testi insieme stanno
            # sotto i ~3500 token in pratica, ma teniamo margine perché
            # l'instagram caption può arrivare a 2200 caratteri da sola.
            "maxOutputTokens": 8192,
        },
    }
    body = json.dumps(payload).encode("utf-8")
    url = f"{GEMINI_ENDPOINT}?key={api_key}"
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/json"}, method="POST"
    )

    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            err = e.read().decode("utf-8", errors="replace")
            if attempt < retries and e.code in (429, 500, 502, 503):
                stampa_err(f"HTTP {e.code} (tentativo {attempt+1}/{retries+1}), riprovo in 3s")
                time.sleep(3)
                continue
            stampa_err(f"Gemini HTTP {e.code}: {err[:300]}")
            return None
        except Exception as e:
            stampa_err(f"Errore di rete: {e}")
            return None

        try:
            risposta = json.loads(raw)
        except json.JSONDecodeError as e:
            stampa_err(f"Risposta non JSON: {e}")
            return None

        try:
            cand = risposta["candidates"][0]
            finish = cand.get("finishReason", "")
            testo = cand["content"]["parts"][0]["text"]
            if finish == "MAX_TOKENS":
                stampa_err("Risposta troncata da limite token (MAX_TOKENS). "
                           "Aumenta maxOutputTokens nel generationConfig.")
                return None
            return json.loads(testo)
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            stampa_err(f"Struttura risposta inattesa: {e}")
            stampa_err(f"Raw: {raw[:800]}")
            return None
    return None


def salva_bozze(slug: str, bozze: dict, art: dict, dry_run: bool = False) -> Path:
    """Scrive 4 file .txt + un README.md in social-bozze/<slug>/."""
    out_dir = SOCIAL_BOZZE / slug
    if dry_run:
        stampa_info(f"\n=== DRY-RUN: {out_dir} ===")
        for piattaforma in ("x", "facebook", "instagram", "telegram"):
            stampa_info(f"\n--- {piattaforma}.txt ---")
            stampa_info(bozze.get(piattaforma, "(vuoto)"))
        return out_dir

    out_dir.mkdir(parents=True, exist_ok=True)

    for piattaforma in ("x", "facebook", "instagram", "telegram"):
        contenuto = bozze.get(piattaforma, "")
        if not contenuto:
            continue
        # Aggiungi riferimento immagini Instagram se generate
        suffix = ""
        if piattaforma == "instagram":
            social_dir = ROOT / "static" / "images-social"
            # Caso 1: singola immagine <slug>-instagram-post.webp
            img_post_singola = social_dir / f"{slug}-instagram-post.webp"
            # Caso 2: carosello <slug>-instagram-post-1.webp, -2.webp, ...
            carousel = sorted(social_dir.glob(f"{slug}-instagram-post-*.webp"))
            img_story = social_dir / f"{slug}-instagram-story.webp"

            righe_img = []
            if img_post_singola.exists():
                righe_img.append(f"📷 Post 1080x1080: {img_post_singola}")
            elif carousel:
                righe_img.append(f"📷 CAROSELLO Instagram ({len(carousel)} immagini, "
                                 f"caricale in questo ordine):")
                for i, c in enumerate(carousel, 1):
                    righe_img.append(f"   {i}. {c}")
            if img_story.exists():
                righe_img.append(f"📷 Story 1080x1920: {img_story}")
            if righe_img:
                suffix = "\n\n---\n" + "\n".join(righe_img) + "\n"
        (out_dir / f"{piattaforma}.txt").write_text(
            contenuto + suffix, encoding="utf-8"
        )

    readme = f"""# Bozze social per «{art['title']}»

Generate automaticamente da `scripts/genera-social.py` (motore: Gemini API).

- **Articolo**: {art['url']}
- **Data**: {art['date']}
- **Badge**: {art['badge']}

## Come usarle

Apri il file della piattaforma desiderata, copia il testo, incollalo nel
post composer del social. Per Instagram ricorda di caricare anche
l'immagine generata (post 1080x1080 e story 1080x1920) in
`static/images-social/`.

## File

| Piattaforma | File | Note |
|---|---|---|
| X (Twitter) | `x.txt` | Max 280 caratteri |
| Facebook | `facebook.txt` | Anteprima OG da URL |
| Instagram | `instagram.txt` | + immagine in `static/images-social/` |
| Telegram | `telegram.txt` | Usa Markdown |

> **Nota**: queste sono BOZZE. Rileggi sempre prima di pubblicare.
> La AI può commettere errori.
"""
    (out_dir / "README.md").write_text(readme, encoding="utf-8")
    return out_dir


def trova_articoli_pubblicati(since: datetime.date | None = None) -> list[Path]:
    """Trova tutti gli articoli pubblicati (data <= oggi, non draft)."""
    risultati = []
    oggi = datetime.date.today()
    for p in sorted(CONTENT_COMUNICAZIONI.glob("*.md")):
        if p.name == "_index.md":
            continue
        try:
            testo = p.read_text(encoding="utf-8")
        except OSError:
            continue
        fm, _ = parse_frontmatter(testo)
        if fm.get("draft", "").lower() in ("true", "yes", "1"):
            continue
        m = re.match(r"(\d{4}-\d{2}-\d{2})", fm.get("date", ""))
        if not m:
            continue
        data = datetime.date.fromisoformat(m.group(1))
        if data > oggi:
            continue
        if since and data < since:
            continue
        risultati.append(p)
    return risultati


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("articolo", nargs="?", help="Path .md singolo articolo")
    parser.add_argument("--all", action="store_true", help="Tutti gli articoli pubblicati")
    parser.add_argument("--since", help="Solo articoli con data >= YYYY-MM-DD")
    parser.add_argument("--dry-run", action="store_true", help="Mostra senza scrivere")
    parser.add_argument("--force", action="store_true", help="Sovrascrivi bozze esistenti")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        stampa_err("GEMINI_API_KEY non impostata. "
                   "Aggiungi 'export GEMINI_API_KEY=...' a ~/.bashrc e ricarica.")
        return 2

    rules = carica_rules()
    system_prompt = costruisci_system_prompt(rules)

    if args.articolo:
        articoli = [Path(args.articolo)]
    else:
        since = None
        if args.since:
            since = datetime.date.fromisoformat(args.since)
        articoli = trova_articoli_pubblicati(since)
        if not args.all and not since:
            stampa_err("Specificare un articolo, --all, o --since YYYY-MM-DD.")
            return 2

    if not articoli:
        stampa_info("Nessun articolo da processare.")
        return 0

    stampa_info(f"Da processare: {len(articoli)} articolo/i")

    ok = 0
    saltati = 0
    errori = 0
    for path in articoli:
        art = estrai_articolo(path)
        if not art:
            stampa_info(f"  - SKIP (non pubblicato o errore): {path.name}")
            saltati += 1
            continue

        out_dir = SOCIAL_BOZZE / art["slug"]
        if out_dir.exists() and not args.force and not args.dry_run:
            stampa_info(f"  - GIÀ PRESENTE (usa --force per ri-generare): {art['slug']}")
            saltati += 1
            continue

        stampa_info(f"  → Genero: {art['slug']}")
        bozze = chiama_gemini(api_key, system_prompt, costruisci_user_prompt(art))
        if not bozze:
            errori += 1
            continue

        salva_bozze(art["slug"], bozze, art, dry_run=args.dry_run)
        ok += 1
        # Pacing tier gratuito Gemini (15 req/min): 4 secondi tra una chiamata
        # e l'altra ci tiene larghi sotto il limite.
        if len(articoli) > 1:
            time.sleep(4)

    stampa_info(f"\nFatto. OK={ok}, saltati={saltati}, errori={errori}")
    return 0 if errori == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
