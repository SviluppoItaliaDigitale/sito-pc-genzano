#!/usr/bin/env python3
"""
check-refusi.py — Controllo refusi (spell-check italiano) per il sito PC Genzano.

Trova parole non riconosciute dal dizionario italiano (hunspell it_IT) negli
articoli Markdown e nelle schede statiche HTML. Pensato per pescare refusi tipo
"cuoperti" (→ copriti) che sfuggono alla rilettura umana.

Motore: spylls (hunspell puro-Python) + dizionario /usr/share/hunspell/it_IT
        + allowlist scripts/dizionario-pc.txt (nomi propri, sigle, termini tecnici).
        Le sigle TUTTE MAIUSCOLE (DPC, NUE, ISO, INGV...) sono saltate d'ufficio.

Uso:
  python3 scripts/check-refusi.py                      # sweep completo del sito
  python3 scripts/check-refusi.py FILE [FILE ...]      # solo questi file (pre-commit)
  python3 scripts/check-refusi.py --md-only            # solo articoli/pagine .md
Exit code: 1 se trova parole sospette, 0 se pulito, 2 se manca il dizionario.

Dipendenze: pip install spylls  +  dizionario hunspell it_IT
            (Ubuntu/CI: apt-get install hunspell-it).
"""
import sys, re, os, glob, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOW_FILE = os.path.join(ROOT, "scripts", "dizionario-pc.txt")
DICT_CANDIDATES = [
    "/usr/share/hunspell/it_IT",
    "/usr/share/myspell/dicts/it_IT",
    "/usr/share/myspell/it_IT",
]

def load_dictionary():
    try:
        from spylls.hunspell import Dictionary
    except ImportError:
        sys.stderr.write("ERRORE: manca 'spylls'. Installa con: pip install spylls\n")
        sys.exit(2)
    for base in DICT_CANDIDATES:
        if os.path.exists(base + ".dic") and os.path.exists(base + ".aff"):
            return Dictionary.from_files(base)
    sys.stderr.write("ERRORE: dizionario hunspell it_IT non trovato.\n"
                     "        Ubuntu/CI: apt-get install hunspell-it\n")
    sys.exit(2)

def load_allowlist():
    words = set()
    if os.path.exists(ALLOW_FILE):
        with open(ALLOW_FILE, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line and not line.startswith("#"):
                    words.add(line.lower())
    return words

# Forme elise/troncate italiane: la parte prima dell'apostrofo è una parola
# grammaticale elisa (dell', sull', quell'...) → non è un refuso, va saltata.
ELISIONI = {
    "l", "un", "d", "c", "po", "mo", "gl", "agl", "dagl", "negl", "begl",
    "dell", "sull", "all", "nell", "dall", "quell", "bell", "sant", "anch",
    "buon", "grand", "mezz", "senz", "tutt", "quest", "cent", "vent", "sett",
    "fin", "fra", "sovra", "intern", "dov", "com", "cos", "nient",
    "trent", "cinquant", "quarant", "sessant", "settant", "ottant", "novant",
}

def strip_markdown(t):
    t = re.sub(r"(?s)^---\n.*?\n---\n", "", t)        # frontmatter YAML
    t = re.sub(r"\S+@\S+", " ", t)                      # email
    t = re.sub(r"\b[\w.-]+\.(?:it|com|org|net|gov|eu|edu|info)\b", " ", t)  # domini nudi
    t = re.sub(r"(?s)```.*?```", " ", t)               # blocchi codice
    t = re.sub(r"`[^`]*`", " ", t)                      # codice inline
    t = re.sub(r"(?s)\{\{[<%].*?[%>]\}\}", " ", t)      # shortcode Hugo
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)         # immagini
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)      # link → solo testo
    t = re.sub(r"<[^>]+>", " ", t)                      # tag HTML inline
    t = re.sub(r"https?://\S+", " ", t)                 # URL
    return t

def strip_html(t):
    t = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"\S+@\S+", " ", t)                      # email
    t = re.sub(r"\b[\w.-]+\.(?:it|com|org|net|gov|eu|edu|info)\b", " ", t)  # domini nudi
    return t

WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:['’][A-Za-zÀ-ÖØ-öø-ÿ]+)*")

def iter_words(text):
    for m in WORD_RE.finditer(text):
        for part in re.split(r"['’]", m.group(0)):
            if len(part) >= 3:
                yield part

def default_files(md_only=False):
    files = glob.glob(os.path.join(ROOT, "content", "**", "*.md"), recursive=True)
    if not md_only:
        files += glob.glob(os.path.join(ROOT, "static", "formazione", "**", "*.html"), recursive=True)
        files += glob.glob(os.path.join(ROOT, "static", "giochi", "**", "*.html"), recursive=True)
    return sorted(set(files))

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    md_only = "--md-only" in sys.argv
    d = load_dictionary()
    allow = load_allowlist()
    files = args if args else default_files(md_only)

    total = 0
    flagged_files = 0
    for f in files:
        if not os.path.isfile(f):
            continue
        raw = open(f, encoding="utf-8", errors="ignore").read()
        text = strip_html(raw) if f.endswith((".html", ".htm")) else strip_markdown(raw)
        suspects = {}
        for w in iter_words(text):
            lw = w.lower()
            if lw in allow or lw in ELISIONI:
                continue
            if w[0].isupper():    # maiuscola: nome proprio / inizio frase / parola straniera → salta (riduce i falsi positivi; i refusi più comuni sono in minuscolo)
                continue
            if any(c.isdigit() for c in w):
                continue
            if d.lookup(w) or d.lookup(lw):
                continue
            suspects[w] = suspects.get(w, 0) + 1
        if suspects:
            flagged_files += 1
            print(f"\n{os.path.relpath(f, ROOT)}")
            for w, c in sorted(suspects.items(), key=lambda x: x[0].lower()):
                print(f"  - {w}" + (f" (x{c})" if c > 1 else ""))
                total += 1

    print(f"\n=== {total} parole sospette in {flagged_files}/{len(files)} file ===")
    print("Falsi positivi (nomi propri, sigle, termini tecnici) → aggiungili a scripts/dizionario-pc.txt")
    sys.exit(1 if total else 0)

if __name__ == "__main__":
    main()
