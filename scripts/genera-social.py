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
  python3 scripts/genera-social.py --riserva path/...     # se Gemini non risponde, testi di riserva

Testi di riserva (22/09/2026): se Gemini non risponde (quota, rete, chiave
assente) e lo script è lanciato con --riserva, i quattro testi si compongono
dal frontmatter dell'articolo (titolo, descrizione, social_punti), che ha già
passato il gate editoriale: niente viene inventato. Senza testi il repository
social non può pubblicare, e l'articolo resterebbe fuori dai social per
sempre. Il workflow passa --riserva solo quando l'articolo è pronto da almeno
un'ora, così Gemini ha prima qualche giro per rispondere.

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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import social_comune  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
CONTENT_COMUNICAZIONI = ROOT / "content" / "comunicazioni"
RULES_DIR = ROOT / ".claude" / "rules"
SOCIAL_BOZZE = ROOT / "social-bozze"


def slug_to_path(slug: str) -> Path:
    """Da slug 'AAAA-MM-GG-titolo' ricava la struttura nidificata
    AAAA/MM/AAAA-MM-GG-titolo per navigabilità in social-bozze/.

    Storia: il 16/05/2026 la cartella social-bozze/ aveva 103 cartelle
    piatte impossibili da navigare da mobile. Migrazione a struttura
    anno/mese per allineare alla logica della pagina /comunicazioni/.
    """
    parts = slug.split('-', 3)
    if (len(parts) >= 4
            and len(parts[0]) == 4 and parts[0].isdigit()
            and len(parts[1]) == 2 and parts[1].isdigit()
            and len(parts[2]) == 2 and parts[2].isdigit()):
        return Path(parts[0]) / parts[1] / slug
    return Path(slug)

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
    """Frontmatter dell'articolo: stesso parser di tutta la catena social
    (scripts/social_comune.py), che legge anche le liste come social_punti."""
    return social_comune.parse_frontmatter(testo)


def estrai_articolo(path: Path) -> dict | None:
    """Legge un articolo Hugo, estrae i campi utili. Salta drafts e date future."""
    try:
        testo = path.read_text(encoding="utf-8")
    except OSError as e:
        stampa_err(f"Impossibile leggere {path}: {e}")
        return None

    fm, body = parse_frontmatter(testo)

    # Le versioni "facile" (A2) sono nascoste da liste e feed: niente social
    # dedicato, come per le immagini (genera-immagini-social.py).
    if social_comune.is_facile(path, fm):
        return None

    # Online come lo decide Hugo: data e ora italiane (hugo.toml timeZone).
    # Fino al 22/09/2026 qui c'era date.today() del runner, cioè UTC: fra
    # mezzanotte e le due un articolo di oggi risultava "futuro".
    if not social_comune.is_online(fm):
        return None  # bozza, senza data, o calendarizzato non ancora online

    m_data = re.match(r"(\d{4}-\d{2}-\d{2})", social_comune.testo_campo(fm, "date"))
    if not m_data:
        return None

    slug = path.stem
    url = f"{SITO_BASE}/comunicazioni/{slug}/"

    # Estratto del corpo: prime ~600 caratteri di testo "vero" (no shortcode)
    corpo_pulito = re.sub(r"\{\{[<%].+?[%>]\}\}", "", body, flags=re.DOTALL)
    corpo_pulito = re.sub(r"<[^>]+>", "", corpo_pulito)
    corpo_pulito = re.sub(r"\s+", " ", corpo_pulito).strip()
    estratto = corpo_pulito[:600]

    punti = fm.get("social_punti") or []
    return {
        "path": str(path),
        "slug": slug,
        "title": social_comune.testo_campo(fm, "title"),
        "description": social_comune.testo_campo(fm, "description"),
        "badge": social_comune.testo_campo(fm, "badge"),
        "area": social_comune.testo_campo(fm, "area"),
        "date": m_data.group(1),
        "url": url,
        "estratto": estratto,
        "punti": [str(x).strip() for x in punti if str(x).strip()] if isinstance(punti, list) else [],
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
    out_dir = SOCIAL_BOZZE / slug_to_path(slug)
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
        # I .txt contengono SOLO il testo da pubblicare: si copiano e si
        # incollano così come sono. Le istruzioni su quale immagine va nel feed
        # e quale nella storia stanno nel README.md della cartella, scritto da
        # genera-immagini-social.py. Fino ad agosto 2026 l'elenco dei file
        # immagine veniva accodato a instagram.txt: finiva nel testo copiato e
        # rischiava di essere pubblicato insieme al post.
        (out_dir / f"{piattaforma}.txt").write_text(contenuto, encoding="utf-8")

    # Il README.md della cartella lo scrive scripts/genera-immagini-social.py
    # (unico proprietario: conosce le immagini create e gira anche nel batch).
    return out_dir


def trova_articoli_pubblicati(since: datetime.date | None = None) -> list[Path]:
    """Articoli online adesso (ora italiana), escluse bozze e versioni facili."""
    risultati = []
    for p, _fm, online in sorted(social_comune.articoli(), key=lambda x: x[0].name):
        if since and online.date() < since:
            continue
        risultati.append(p)
    return risultati


# Hashtag per badge: la stessa tabella del prompt (costruisci_system_prompt),
# che resta l'unica fonte degli hashtag ammessi.
HASHTAG_IG = {
    "Allerta": "#PCGenzano #Genzano #AllertaLazio #ProtezioneCivile #CastelliRomani",
    "Emergenza": "#PCGenzano #Genzano #NUE112 #AllertaLazio #ProtezioneCivile",
    "Volontariato": "#PCGenzano #Genzano #ProtezioneCivile #Volontariato #CastelliRomani",
    "Formazione": "#PCGenzano #Genzano #ProtezioneCivile #Volontariato #CastelliRomani",
    "Evento": "#PCGenzano #Genzano #ProtezioneCivile #Volontariato #CastelliRomani",
}
HASHTAG_IG_DEFAULT = "#PCGenzano #Genzano #ProtezioneCivile #GenzanoDiRoma #CastelliRomani"


def _pulisci(s: str) -> str:
    """Toglie il Markdown dai testi del frontmatter: sui social non si vede."""
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return re.sub(r"\s+", " ", s).strip()


def testi_di_riserva(art: dict) -> dict:
    """I quattro testi composti dal frontmatter, quando Gemini non risponde.

    Solo ciò che l'articolo dice già (titolo, descrizione, social_punti), che
    ha passato il gate editoriale: niente viene inventato. La forma segue le
    regole del prompt: tag del badge fra parentesi quadre, niente emoji,
    hashtag solo dalla lista approvata. L'invito a leggere sul sito, le
    menzioni degli enti e il luogo li aggiunge il repository social al
    momento della pubblicazione (social_coda_lib.componi_testo).
    """
    titolo = _pulisci(art["title"])
    descr = _pulisci(art["description"]) or _pulisci(art["estratto"])[:300].rsplit(". ", 1)[0]
    if descr and not descr.endswith((".", "!", "?")):
        descr += "."
    punti = [_pulisci(x) for x in art.get("punti", []) if _pulisci(x)]
    tag = f"[{art['badge'].upper()}] " if art["badge"] else ""
    ig_tag = HASHTAG_IG.get(art["badge"], HASHTAG_IG_DEFAULT)
    corti = " ".join(ig_tag.split()[:3])
    url = art["url"]

    blocco = [f"{tag}{titolo}", "", descr]
    if punti:
        blocco += ["", "In sintesi:"] + [f"• {x}" for x in punti]
    instagram = "\n".join(blocco + ["", "Link in bio.", "", "", "", ig_tag])
    facebook = "\n".join(blocco + ["", f"Approfondisci sul nostro sito: {url}", "", ig_tag])
    telegram = "\n".join(
        [f"{tag}**{titolo}**", "", descr]
        + ([""] + [f"— {x}" for x in punti] if punti else [])
        + ["", f"**[Leggi sul sito]({url})**", corti]
    )
    # X conta ogni indirizzo come 23 caratteri: il titolo sta sempre nei 280.
    spazio = 280 - 23 - len(corti) - 2
    x = f"{titolo if len(titolo) <= spazio else titolo[:spazio - 1].rstrip() + '…'} {url} {corti}"
    return {"x": x, "facebook": facebook, "instagram": instagram, "telegram": telegram}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("articolo", nargs="?", help="Path .md singolo articolo")
    parser.add_argument("--all", action="store_true", help="Tutti gli articoli pubblicati")
    parser.add_argument("--since", help="Solo articoli con data >= YYYY-MM-DD")
    parser.add_argument("--dry-run", action="store_true", help="Mostra senza scrivere")
    parser.add_argument("--force", action="store_true", help="Sovrascrivi bozze esistenti")
    parser.add_argument("--riserva", action="store_true",
                        help="Se Gemini non risponde, scrivi i testi di riserva dal frontmatter")
    args = parser.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key and not args.riserva:
        stampa_err("GEMINI_API_KEY non impostata. "
                   "Aggiungi 'export GEMINI_API_KEY=...' a ~/.bashrc e ricarica.")
        return 2
    if not api_key:
        stampa_info("GEMINI_API_KEY non impostata: userò i testi di riserva.")

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

        out_dir = SOCIAL_BOZZE / slug_to_path(art["slug"])
        # Si salta solo se i TESTI ci sono già, non se esiste la cartella: le
        # immagini (genera-immagini-social.py) possono essere state generate
        # prima, e in quel caso i testi vanno comunque prodotti.
        testi_presenti = all(
            (out_dir / f"{piattaforma}.txt").exists()
            for piattaforma in ("x", "facebook", "instagram", "telegram")
        )
        if testi_presenti and not args.force and not args.dry_run:
            stampa_info(f"  - GIÀ PRESENTE (usa --force per ri-generare): {art['slug']}")
            saltati += 1
            continue

        stampa_info(f"  → Genero: {art['slug']}")
        bozze = (chiama_gemini(api_key, system_prompt, costruisci_user_prompt(art))
                 if api_key else None)
        if not bozze and args.riserva:
            bozze = testi_di_riserva(art)
            avviso = f"Gemini non disponibile: testi di riserva per {art['slug']}"
            stampa_info(f"    {avviso}")
            if os.environ.get("GITHUB_ACTIONS"):
                print(f"::warning::{avviso}")
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
