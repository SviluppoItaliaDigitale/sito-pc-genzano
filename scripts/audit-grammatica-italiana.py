#!/usr/bin/env python3
"""
Audit grammaticale / ortografico italiano per i contenuti del sito Hugo.

Cosa controlla (tutti i .md di content/ + gli HTML statici di
static/formazione/ e static/giochi/ — schede stampabili e giochi):

  REGOLE ATTIVE (ognuna corrisponde a un `rule(...)` nella lista RULES):
   1. Accenti mancanti su parole non ambigue: perche -> perché, piu -> più,
      puo -> può, gia -> già, cosi -> così, lunedi -> lunedì, ecc.
   2. Apostrofi finti usati al posto dell'accento (e' -> è)
   3. Backtick in mezzo a una parola (apostrofo errato)
   4. "un po" senza apostrofo -> "un po'"
   5. "qual'è" -> "qual è"
   6. "un'altro" -> "un altro"
   7. "obbiettivo" -> "obiettivo"
   8. "famigli" errato
   9. "ecc..." ridondante
  10. Spazio mancante dopo la punteggiatura ("superficiale.Il")   [19/08/2026]
  11. Doppio spazio FRA DUE PAROLE (non negli allineamenti)        [19/08/2026]
  12. Spazio prima della punteggiatura                             [19/08/2026]
  13. Parola GRAMMATICALE ripetuta sulla stessa riga ("il il")     [19/08/2026]
      NB: il raddoppiamento di nomi e aggettivi è italiano legittimo
      ("piccola piccola", "Natrix natrix", "Giro giro tondo") e non si
      segnala; i refusi veri raddoppiano articoli e preposizioni.
  14. Elisione mancante ("una emergenza" -> "un'emergenza")        [19/08/2026]

  FUORI PERIMETRO (saltati apposta):
   - file `-facile.md` e /facile-da-leggere/: registro A2 CEFR, le forme non
     elise e le frasi ripetitive sono una scelta didattica;
   - pagine con `language:` diverso da it (spagnolo, inglese...): le regole
     dell'italiano vi produrrebbero solo falsi positivi.

  NON RILEVABILE QUI (serve una lettura, non una regex):
   - articoli mancanti ("L'Italia ha rete ben strutturata"), accordi di
     genere/numero, concordanze verbali a distanza, reggenze delle
     preposizioni. Se ne occupa l'agent `pc-revisore-linguistico`, gate
     obbligato richiamato da `pc-article-reviewer` prima del commit.

  STORIA: fino al 19/08/2026 questa docstring elencava 15 controlli ma solo 8
  erano implementati; lo script rispondeva "Nessun problema rilevato" su testi
  che contenevano errori reali, dando una falsa sicurezza. Le regole 10-14 sono
  state aggiunte allora, calibrate misurando i falsi positivi sul sito reale.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

# ----------------------------------------------------------------
# Pattern di controllo. Ogni regola è una tupla:
#   (codice, gravità, regex, descrizione, suggerimento, esempi-da-escludere-regex)
# Gravità: ERR (errore certo) | WARN (probabile errore) | INFO (suggerimento)

CTL_QUOTE = "’"  # apostrofo curvo right-single-quotation-mark


def rule(code, severity, pattern, desc, suggest=None, exclude=None, ignore_case=False,
         prose_only=False):
    flags = re.IGNORECASE if ignore_case else 0
    return {
        "code": code,
        "severity": severity,
        "pattern": re.compile(pattern, flags),
        "desc": desc,
        "suggest": suggest,
        "exclude": re.compile(exclude, flags) if exclude else None,
        # prose_only: la regola vale SOLO sulle righe di prosa pura.
        # WHY: il body viene mascherato sostituendo tag HTML/shortcode/URL
        # con spazi (per preservare gli offset). Le regole sensibili agli
        # spazi leggerebbero quegli spazi artificiali come errori.
        "prose_only": prose_only,
    }


# Parole con accento che vanno scritte con accento: chi le scrive senza è
# un refuso. Per evitare falsi positivi, controlliamo solo se la parola è
# una "word" intera (delimitata) e seguita da spazio/punteggiatura/EOL.
# Dizionario CONSERVATIVO: solo parole NON ambigue (cioè parole che senza
# accento NON hanno significato corretto in italiano, mai). Esclude verbi
# al passato remoto 3a singolare che sono omografi di sostantivi/verbi
# all'indicativo presente: arrivo, porto, passo, faro, ando, comincio, ecc.
# (es. "l'arrivo della merce" è giusto, "l'arrivò" è errore).
ACCENTI_OBBLIGATORI = {
    # Congiunzioni e avverbi tronchi (sempre con accento obbligatorio)
    "perche": "perché",
    "poiche": "poiché",
    "benche": "benché",
    "anziche": "anziché",
    "finche": "finché",
    "affinche": "affinché",
    # NOTA: "giacche" è ESCLUSO dal dizionario perché è il plurale legittimo
    # del sostantivo "giacca" (capo di abbigliamento). Per la congiunzione
    # corretta "giacché" ci affidiamo ad altre regole (es. "è " errore).
    "sicche": "sicché",
    "nonche": "nonché",
    "piu": "più",
    "puo": "può",
    "gia": "già",
    "cosi": "così",
    "pero": "però",
    "cio": "ciò",
    # Sostantivi tronchi italiani con accento finale obbligatorio
    # (queste parole NON esistono senza accento)
    "citta": "città",
    "liberta": "libertà",
    "qualita": "qualità",
    "quantita": "quantità",
    "universita": "università",
    "comunita": "comunità",
    "responsabilita": "responsabilità",
    "attivita": "attività",
    "specialita": "specialità",
    "autorita": "autorità",
    "dignita": "dignità",
    "civilta": "civiltà",
    "pieta": "pietà",
    "tribu": "tribù",
    "virtu": "virtù",
    "gioventu": "gioventù",
    "schiavitu": "schiavitù",
    "servitu": "servitù",
    # Giorni della settimana (lunedi senza accento è errore certo)
    "lunedi": "lunedì",
    "martedi": "martedì",
    "mercoledi": "mercoledì",
    "giovedi": "giovedì",
    "venerdi": "venerdì",
    # Apostrofi finti usati al posto dell'accento (errore certo)
    "è": "è",
    "né": "né",
    "sé": "sé",
    "tè": "tè",
    "po'": "po'",  # corretta, NON nel dizionario
    "sarà": "sarà",
    "andrà": "andrà",
    "andro'": "andrò",
    "verrà": "verrà",
    "farà": "farà",
    "starà": "starà",
    "dovrà": "dovrà",
    "potrà": "potrà",
    "vorrà": "vorrà",
}
# Filtra voci self-mapping
ACCENTI_OBBLIGATORI = {k: v for k, v in ACCENTI_OBBLIGATORI.items() if k != v}


def make_accenti_pattern() -> re.Pattern:
    """Costruisce un'unica regex con OR su tutte le parole sbagliate."""
    # Word boundary italiana: non preceduto né seguito da carattere parola.
    # Usiamo (?<![A-Za-zÀ-ÿ\d-]) e (?![A-Za-zÀ-ÿ\d-]) per Unicode.
    parole = sorted(ACCENTI_OBBLIGATORI.keys(), key=len, reverse=True)
    alternatives = "|".join(re.escape(p) for p in parole)
    pattern = rf"(?<![A-Za-zÀ-ÿ\d-])({alternatives})(?![A-Za-zÀ-ÿ\d-])"
    return re.compile(pattern, re.IGNORECASE)


ACCENTI_RE = make_accenti_pattern()

# Regex per altri controlli specifici
RULES = [
    rule(
        "QUOTE_BACKTICK",
        "WARN",
        r"\w`\w",
        "Backtick (`) usato in mezzo a una parola — probabile apostrofo errato.",
        suggest="Sostituire con apostrofo curvo (')",
        exclude=r"```",  # ignora code fences
    ),
    rule(
        "PO_SENZA_APOSTROFO",
        "ERR",
        r"\bun\s+po\b(?![''’])",
        "« un po » senza apostrofo — corretto: « un po' » (troncamento di « poco »).",
        suggest="un po'",
        ignore_case=True,
    ),
    rule(
        "QUAL_E_APOSTROFO",
        "ERR",
        r"\bqual['’]\s*è\b",
        "« qual'è » è errore: « qual » è già forma elisa di « quale », non vuole apostrofo.",
        suggest="qual è",
        ignore_case=True,
    ),
    rule(
        "UN_ALTRO_APOSTROFO",
        "ERR",
        r"\bun['’]\s*altro\b",
        "« un'altro » è errore: « altro » è maschile, vuole « un altro » senza apostrofo.",
        suggest="un altro",
        ignore_case=True,
    ),
    # NOTE: regole DISABILITATE per troppi falsi positivi:
    # - UNA_VOCALE_FEMMINILE (ammesso in molti contesti, calibrazione futura)
    # - DOPPIO_SPAZIO (HTML attributes, formattazione MD legittima)
    # - SPAZIO_PRIMA_PUNTEGGIATURA (falsi positivi su </tag> .)
    # - TRE_PUNTINI / TRATTINO_BREVE (scelte stilistiche, info inutile)
    # - MAIUSCOLA_DOPO_PUNTO (numerazioni, decimali, abbreviazioni)
    # Si potranno riabilitare quando i pattern saranno più restrittivi.

    rule(
        "OBBIETTIVO",
        "WARN",
        r"\bobbiettiv[oaie]\b",
        "« obbiettivo » è ammesso ma sconsigliato: la forma standard è « obiettivo ».",
        suggest="obiettivo",
        ignore_case=True,
    ),
    rule(
        "DAVA_DAREI",
        "INFO",
        r"\b(davva|sarra|verrra|farra|starra)\w*",
        "Probabile triplicazione di consonante (errore di battitura).",
        ignore_case=True,
    ),
    rule(
        "FAMIGLI_ERRATO",
        "WARN",
        r"\bfamigli\b(?!e|a)",
        "« famigli » senza desinenza è errore: deve essere « famiglia » (singolare) o « famiglie » (plurale).",
        ignore_case=True,
    ),
    rule(
        "ABBREVIAZIONE_ECC",
        "INFO",
        r"\becc\.\.\.+",
        "« ecc... » è ridondante: « ecc. » significa già « eccetera ».",
        suggest="ecc.",
        ignore_case=True,
    ),
    # ----------------------------------------------------------------
    # Regole meccaniche/tipografiche (aggiunte 19/08/2026).
    # WHY: la docstring di questo script prometteva questi controlli (punti
    # 8, 9, 11, 15) ma non erano mai stati implementati: lo script rispondeva
    # "Nessun problema rilevato" su testi che contenevano errori reali.
    # Incidente 19/08/2026: "L'Italia ha rete ben strutturata", "nella
    # immagine", "superficiale.Il bilancio" andati live e trovati a mano.
    rule(
        "SPAZIO_DOPO_PUNTEGGIATURA",
        "ERR",
        r"[a-zà-ù]{2}[.;:!?],?(?=[A-ZÀ-Ù][a-zà-ù])",
        "Manca lo spazio dopo la punteggiatura (parola incollata alla successiva).",
        suggest="Inserire uno spazio dopo il segno di punteggiatura",
        exclude=r"(https?://|www\.|@|\.(md|html?|it|com|org|gov|eu|net|php|py|sh|js|css|xml|json|pdf|webp|png|jpg|yml|yaml|txt|brf|zip))",
        prose_only=True,
    ),
    rule(
        "DOPPIO_SPAZIO",
        "WARN",
        r"(?<=[a-zà-ù,;:])  +(?=[A-Za-zà-ù])",  # solo fra parole, non negli allineamenti
        "Doppio spazio in mezzo al testo.",
        suggest="Lasciare un solo spazio",
        prose_only=True,
    ),
    rule(
        "SPAZIO_PRIMA_PUNTEGGIATURA",
        "ERR",
        r"\S\s+[,;:!?](?=\s|$)",
        "Spazio prima del segno di punteggiatura (in italiano non si mette).",
        suggest="Attaccare il segno alla parola precedente",
        prose_only=True,
    ),
    rule(
        "PAROLA_RIPETUTA",
        "WARN",
        # Solo parole grammaticali e solo sulla STESSA riga ([ \t], non \s):
        # il raddoppiamento di nomi e aggettivi è italiano legittimo
        # («piccola piccola», «Natrix natrix»), quello di articoli e
        # preposizioni è sempre un refuso.
        r"(?<!zero )(?<!uno )(?<!due )(?<!tre )(?<!sei )(?<!otto )(?<!nove )(?<!sette )(?<!quattro )(?<!cinque )"
        r"\b(il|lo|la|i|gli|le|un|uno|una|di|da|in|con|su|per|tra|fra|del|dello|della|dei|degli|delle"
        r"|dal|dalla|al|allo|alla|ai|agli|alle|nel|nello|nella|nei|negli|nelle|sul|sulla|sui|sugli|sulle"
        r"|che|non|si|ci|vi|ne|ha|ho|hai|hanno|essere|sono|era|erano)[ \t]+\1\b",
        "Parola ripetuta due volte di seguito.",
        suggest="Eliminare la ripetizione",
        ignore_case=True,
    ),
    rule(
        "ELISIONE_MANCANTE",
        "ERR",
        r"\b([Uu]na|[Nn]ella|[Dd]ella|[Dd]alla|[Aa]lla|[Ss]ulla)\s+([aeiouàèéìòù][a-zà-ù]{2,})",
        "Manca l'elisione davanti a vocale (es. « una emergenza » -> « un'emergenza »).",
        suggest="Elidere: un', nell', dell', dall', all', sull', quell', quest'",
        # i/u semiconsonantiche non si elidono (una iena, una uova);
        # davanti a sigle e nomi propri (della IARU, dalla ITU) nemmeno.
        # NON si elide davanti a: i/u semiconsonantiche (una iena, una uova);
        # preposizioni e avverbi (« una alla volta », « una ad una »);
        # « uno » cardinale (« una a una »).
        # BUG corretto 19/08/2026: il \b finale valeva per TUTTO il gruppo e
        # impediva il match su "ionosfera"/"iodoprofilassi" (dopo "io" c'è una
        # consonante), che venivano segnalate a torto. Le i/u semiconsonantiche
        # ora hanno un ramo proprio senza \b.
        exclude=r"\s+(i[aeou]|u[aeio])|\s+(alla|allo|alle|agli|ad|anche|ancora|inoltre|oppure|accanto|ogni|altra|altro|una|aveva|avevano|era|erano|ha|hanno|è)\b",
    ),
]


# ----------------------------------------------------------------
# Filtri di esclusione globali

# Linee da saltare completamente: code fences, frontmatter YAML, link URL,
# tag HTML, shortcode Hugo (interno).
def is_skippable_line(line: str, in_code_fence: bool) -> bool:
    if in_code_fence:
        return True
    stripped = line.strip()
    # Frontmatter delimitatori
    if stripped == "---":
        return True
    # Linee che sono SOLO un URL (link nudo)
    if re.match(r"^https?://\S+$", stripped):
        return True
    return False


# ----------------------------------------------------------------
def find_articles(only: list[str] | None = None) -> Iterator[Path]:
    """Ritorna i Markdown da auditare.

    Senza argomenti: TUTTI i .md sotto content/ (ricorsivo). Fino al
    19/08/2026 la funzione elencava solo 4 glob non ricorsivi e lasciava
    scoperti ~300 file annidati (es. content/formazione/manuale-campo/*.md):
    una PR che ne modificava uno passava il gate senza essere controllata.

    Con `only`: solo i file indicati (usato dal gate di PR per auditare
    esattamente i file modificati).
    """
    if only:
        for f in only:
            pth = Path(f)
            if not pth.is_absolute():
                pth = ROOT / f
            if pth.suffix in (".md", ".html", ".htm") and pth.exists():
                yield pth
        return
    yield from sorted(CONTENT.rglob("*.md"))
    # Schede stampabili e giochi: contenuto in HTML statico, fuori da content/.
    # WHY (19/08/2026): erano il punto cieco grammaticale — 372 file che
    # finiscono STAMPATI nelle scuole non passavano da nessun controllo di
    # accenti/apostrofi/elisioni (solo dallo spell-check di parola singola).
    # Lo stesso punto cieco da cui era passato «cuoperti» → «copriti».
    yield from sorted((ROOT / "static" / "formazione").rglob("*.html"))
    yield from sorted((ROOT / "static" / "giochi").rglob("*.html"))


def line_index_to_friendly(text: str, idx: int) -> tuple[int, int, str]:
    """Da offset assoluto in `text` ritorna (numero_riga_1based, col, snippet)."""
    line_start = text.rfind("\n", 0, idx) + 1
    line_end = text.find("\n", idx)
    if line_end == -1:
        line_end = len(text)
    line_no = text.count("\n", 0, idx) + 1
    col = idx - line_start + 1
    snippet = text[line_start:line_end].rstrip()
    if len(snippet) > 120:
        # Tronca attorno al match
        rel_idx = idx - line_start
        start = max(0, rel_idx - 40)
        end = min(len(snippet), rel_idx + 80)
        snippet = ("..." if start > 0 else "") + snippet[start:end] + ("..." if end < len(snippet) else "")
    return line_no, col, snippet


def _mask_preserve_lines(text: str, pattern: str, flags=0) -> str:
    """Sostituisce i match con spazi mantenendo i newline (offset stabili)."""
    def repl(m):
        return "".join(ch if ch == "\n" else " " for ch in m.group(0))
    return re.sub(pattern, repl, text, flags=flags)


_JS_LITERAL_RE = re.compile(
    r"'(?:[^'\\\n]|\\.)*'"      # '...'
    r"|\"(?:[^\"\\\n]|\\.)*\""  # "..."
    r"|`(?:[^`\\]|\\.)*`",       # `...` (anche multi-riga)
    re.S,
)


def _mask_js_keep_prose(code: str) -> str:
    """Maschera il codice JS ma CONSERVA i letterali che sono prosa italiana.

    WHY (review Codex su PR #876): nei giochi il testo per l'utente vive
    dentro stringhe JavaScript (domande, feedback: «può innescare una
    esplosione»). Mascherare l'intero <script> lasciava quel testo fuori
    da ogni controllo. Qui il codice diventa spazi, ma i letterali che
    "sembrano frasi" (due parole di fila, niente caratteri da codice)
    restano e passano per le regole. Gli apostrofi escapati \' diventano
    apostrofi veri (offset preservati: 2 char -> 2 char).
    """
    code = _mask_preserve_lines(code, r"/\*.*?\*/", re.S)   # commenti /* */
    code = _mask_preserve_lines(code, r"//[^\n]*")            # commenti //
    out = []
    pos = 0
    for m in _JS_LITERAL_RE.finditer(code):
        out.append("".join(ch if ch == "\n" else " " for ch in code[pos:m.start()]))
        lit = m.group(0)
        inner = lit[1:-1]
        norm = inner.replace("\\'", "' ").replace('\\"', '" ')
        e_prosa = (
            re.search(r"[A-Za-zà-ùÀ-Ù]{2,}\s+[A-Za-zà-ùÀ-Ù]{2,}", norm)
            and not re.search(r"[<>{}=;\\]|\$\{", norm)
        )
        if e_prosa:
            out.append(" " + norm + " ")
        else:
            out.append("".join(ch if ch == "\n" else " " for ch in lit))
        pos = m.end()
    out.append("".join(ch if ch == "\n" else " " for ch in code[pos:]))
    return "".join(out)


def _mask_html(text: str) -> str:
    """Maschera di un file HTML: resta solo il testo visibile, riga per riga.

    Ordine: blocchi <style> (via il CSS), <script> (via il codice ma NON i
    letterali di prosa — vedi _mask_js_keep_prose), commenti, tag (anche
    multi-riga), entità, URL. Tutto sostituito con spazi preservando i
    newline, così i numeri di riga dei findings sono giusti.
    """
    def _script_repl(m):
        apertura = "".join(ch if ch == "\n" else " " for ch in m.group(1))
        chiusura = "".join(ch if ch == "\n" else " " for ch in m.group(3))
        return apertura + _mask_js_keep_prose(m.group(2)) + chiusura
    t = re.sub(r"(<script[^>]*>)(.*?)(</script>)", _script_repl, text, flags=re.I | re.S)
    t = _mask_preserve_lines(t, r"<style[^>]*>.*?</style>", re.I | re.S)
    t = _mask_preserve_lines(t, r"<!--.*?-->", re.S)
    t = _mask_preserve_lines(t, r"<[^>]*>", re.S)      # tag, anche spezzati su piu' righe
    def _apos(m):  # scrive l'apostrofo al posto del 1° carattere dell'entita'
        return "'" + " " * (len(m.group(0)) - 1)
    t = re.sub(r"&(?:#x27|#39|apos|rsquo|#8217);", _apos, t)
    t = _mask_preserve_lines(t, r"&[a-zA-Z#0-9]+;")
    t = _mask_preserve_lines(t, r"https?://\S+")
    return t


def _rel(path: Path) -> str:
    """Path relativo alla root del repo; assoluto se il file sta fuori."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def _audit_html(path: Path, text: str) -> list[dict]:
    """Audita il testo visibile di un file HTML statico (schede, giochi).

    Differenze rispetto ai Markdown, motivate:
    - la mascheratura sostituisce tag/JS/CSS con SPAZI: le regole che scattano
      sulla PRESENZA di spazi (DOPPIO_SPAZIO, SPAZIO_PRIMA_PUNTEGGIATURA)
      qui darebbero solo falsi positivi da markup e sono saltate — tanto in
      HTML gli spazi multipli collassano comunque alla resa;
    - restano attive le regole sull'ASSENZA di spazio e su parole/accenti/
      apostrofi/elisioni, che la mascheratura non puo' falsare (inserisce
      spazi, non li toglie).
    """
    findings = []
    masked = _mask_html(text)

    for m in ACCENTI_RE.finditer(masked):
        word = m.group(1)
        suggested = ACCENTI_OBBLIGATORI.get(word.lower())
        if not suggested:
            continue
        if word[0].isupper():
            suggested = suggested[0].upper() + suggested[1:]
        line_no, col, snippet = line_index_to_friendly(text, m.start())
        findings.append({
            "file": _rel(path), "line": line_no, "col": col,
            "code": "ACCENTO_MANCANTE", "severity": "ERR",
            "match": word, "suggest": suggested, "snippet": snippet,
            "msg": f"« {word} » senza accento — corretto: « {suggested} ».",
        })

    SALTA_SU_HTML = {"DOPPIO_SPAZIO", "SPAZIO_PRIMA_PUNTEGGIATURA"}
    for r in RULES:
        if r["code"] in SALTA_SU_HTML:
            continue
        for m in r["pattern"].finditer(masked):
            matched = m.group(0)
            if r["exclude"] and r["exclude"].search(matched):
                continue
            # Alfabetieri: il tracciamento «I I I» ripete lettere singole apposta.
            if r["code"] == "PAROLA_RIPETUTA" and len(m.group(1)) == 1:
                continue
            line_no, col, snippet = line_index_to_friendly(text, m.start())
            findings.append({
                "file": _rel(path), "line": line_no, "col": col,
                "code": r["code"], "severity": r["severity"],
                "match": matched.strip(), "suggest": r.get("suggest"),
                "snippet": snippet, "msg": r["desc"],
            })
    return findings


def audit_file(path: Path) -> list[dict]:
    """Analizza un file e ritorna la lista di findings."""
    findings = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return [{"file": str(path), "code": "READ_ERROR", "severity": "ERR", "msg": str(e)}]

    # Fuori perimetro delle regole di italiano standard:
    #  - versioni facili A2 (`-facile.md`): frasi e forme NON elise sono una
    #    scelta didattica per l'italiano L2 (rule 02 § "Versione facile");
    #  - pagine tradotte (`language:` diverso da it): lo spagnolo non elide,
    #    l'inglese non ha accenti italiani -> ogni regola qui è un falso positivo.
    if path.name.endswith("-facile.md") or "facile-da-leggere" in str(path):
        return []
    m_lang = re.search(r"^language:\s*[\"']?([a-z]{2})", text, re.M)
    if m_lang and m_lang.group(1) != "it":
        return []
    # Pagine HTML con lang esplicito non italiano (es. traduzioni statiche).
    if path.suffix in (".html", ".htm"):
        m_html_lang = re.search(r"<html[^>]*\blang=[\"']?([a-z]{2})", text, re.I)
        if m_html_lang and m_html_lang.group(1) != "it":
            return []
        return _audit_html(path, text)

    # Salta il frontmatter YAML iniziale (delimitato da ---).
    body_start = 0
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            body_start = text.find("\n", end + 4) + 1
    body = text[body_start:]
    body_offset = body_start

    # Maschera code fences ``` ... ``` con spazi (mantiene posizioni)
    masked = body
    for m in re.finditer(r"```.*?```", body, re.DOTALL):
        s, e = m.start(), m.end()
        masked = masked[:s] + (" " * (e - s)) + masked[e:]
    # Maschera anche shortcode Hugo {{< ... >}} che possono avere parametri
    # in lingue diverse o codice
    for m in re.finditer(r"\{\{[<%].*?[%>]\}\}", masked, re.DOTALL):
        s, e = m.start(), m.end()
        masked = masked[:s] + (" " * (e - s)) + masked[e:]
    # Maschera URL nudi e link Markdown
    for m in re.finditer(r"https?://\S+", masked):
        s, e = m.start(), m.end()
        masked = masked[:s] + (" " * (e - s)) + masked[e:]
    # Maschera tag HTML (preserve sostanziale del testo)
    for m in re.finditer(r"<[^>\n]+>", masked):  # niente match multi-riga
        s, e = m.start(), m.end()
        masked = masked[:s] + (" " * (e - s)) + masked[e:]
    # Maschera attributi tipo alt="..." e caption="..." dentro shortcode
    # (sono già gestiti dalla maschera shortcode sopra, ma per sicurezza)

    # Applica regola accenti
    for m in ACCENTI_RE.finditer(masked):
        word = m.group(1)
        # Se la parola originale è in maiuscolo, anche il suggerimento lo è
        suggested = ACCENTI_OBBLIGATORI.get(word.lower())
        if not suggested:
            continue
        if word[0].isupper():
            suggested = suggested[0].upper() + suggested[1:]
        line_no, col, snippet = line_index_to_friendly(text, m.start() + body_offset)
        findings.append({
            "file": _rel(path),
            "line": line_no,
            "col": col,
            "code": "ACCENTO_MANCANTE",
            "severity": "ERR",
            "match": word,
            "suggest": suggested,
            "snippet": snippet,
            "msg": f'« {word} » → « {suggested} » (accento mancante)',
        })

    # Righe NON di prosa: contengono HTML, tabelle Markdown, codice inline o
    # shortcode. Le regole sensibili agli spazi (prose_only) le saltano, perché
    # la mascheratura sostituisce quei costrutti con spazi e produrrebbe falsi
    # positivi (incidente 19/08/2026: 40+ segnalazioni fasulle su <abbr>, <a>).
    righe_non_prosa = set()
    for i, riga in enumerate(text.split("\n"), start=1):
        # Riga di codice o markup: qui la mascheratura crea spazi artificiali.
        # NB: il punto e virgola da solo NON basta a squalificare una riga —
        # in italiano separa legittimamente gli elementi di un elenco.
        e_codice = bool(
            re.search(r"<[a-zA-Z/!]", riga)          # tag HTML
            or "`" in riga                            # code span
            or "{{" in riga                           # shortcode Hugo
            or "](" in riga or "http" in riga         # link markdown / URL
            or riga.lstrip().startswith("|")          # tabella
            or re.search(r"(^|\s)(var|let|const|function|return|if)\s", riga)
            or re.search(r"[=<>]=|=>|\)\s*[;{]|;\s*$|\w\.\w+\(", riga)
        )
        if e_codice:
            righe_non_prosa.add(i)

    # Applica le altre regole
    for r in RULES:
        for m in r["pattern"].finditer(masked):
            matched = m.group(0)
            # Filtra esclusioni puntuali
            if r["exclude"] and r["exclude"].search(matched):
                continue
            line_no, col, snippet = line_index_to_friendly(text, m.start() + body_offset)
            if r.get("prose_only") and line_no in righe_non_prosa:
                continue
            findings.append({
                "file": _rel(path),
                "line": line_no,
                "col": col,
                "code": r["code"],
                "severity": r["severity"],
                "match": matched.strip(),
                "suggest": r.get("suggest"),
                "snippet": snippet,
                "msg": r["desc"],
            })

    return findings


def main() -> int:
    all_findings: list[dict] = []
    files_count = 0
    for path in find_articles(sys.argv[1:]):
        files_count += 1
        all_findings.extend(audit_file(path))

    # Output ordinato per gravità (ERR > WARN > INFO) poi per file
    severity_order = {"ERR": 0, "WARN": 1, "INFO": 2}
    all_findings.sort(key=lambda f: (severity_order.get(f["severity"], 99), f["file"], f.get("line", 0)))

    n_err = sum(1 for f in all_findings if f["severity"] == "ERR")
    n_warn = sum(1 for f in all_findings if f["severity"] == "WARN")
    n_info = sum(1 for f in all_findings if f["severity"] == "INFO")

    print(f"# Audit grammaticale italiano — {files_count} file analizzati\n")
    print(f"**Totale findings**: {len(all_findings)} — {n_err} errori, {n_warn} warning, {n_info} info\n")

    if not all_findings:
        print("✅ Nessun problema rilevato.\n")
        return 0

    # Raggruppa per severità → file
    by_severity: dict[str, list[dict]] = {"ERR": [], "WARN": [], "INFO": []}
    for f in all_findings:
        by_severity[f["severity"]].append(f)

    for sev_label, sev_emoji in [("ERR", "❌"), ("WARN", "⚠️"), ("INFO", "ℹ️")]:
        items = by_severity[sev_label]
        if not items:
            continue
        print(f"\n## {sev_emoji} {sev_label} ({len(items)})\n")
        # Raggruppa per codice regola → file
        by_code: dict[str, list[dict]] = {}
        for it in items:
            by_code.setdefault(it["code"], []).append(it)
        for code, lst in sorted(by_code.items()):
            print(f"### {code} — {lst[0]['msg']}")
            if lst[0].get("suggest"):
                print(f"_Suggerimento_: « {lst[0]['suggest']} »")
            print()
            # Mostra max 20 occorrenze per regola (per leggibilità)
            shown = lst[:20]
            for it in shown:
                print(f"- `{it['file']}:{it.get('line', '?')}` — `{it.get('match', '')}` — {it.get('snippet', '')}")
            if len(lst) > 20:
                print(f"- _… altre {len(lst) - 20} occorrenze omesse._")
            print()

    return 0  # informativo, non bloccante


if __name__ == "__main__":
    sys.exit(main())
