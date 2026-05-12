#!/usr/bin/env python3
"""
genera-braille.py — Sera 1 del Punto 19 della roadmap.

Genera file BRF (Braille Ready Format) ASCII per ogni articolo in
content/comunicazioni/, salvandoli in static/braille/comunicazioni/<slug>.brf.

Dipendenze sistema:
  sudo apt-get install -y liblouis-data python3-louis python3-yaml

Verifica:
  python3 -c "import louis; print(louis.version())"  → 3.x

Tabella di traduzione: it-it-comp6.utb (braille italiano a 6 punti standard,
output ASCII puro). NOTA: la tabella `it-it-g1.utb` proposta nell'assessment
NON è disponibile in liblouis upstream — quella canonica italiana è comp6,
che corrisponde di fatto a "Grade 1 italiano uncontracted" lettera-per-lettera.

Uso:
  python3 scripts/genera-braille.py                 # processa tutti
  python3 scripts/genera-braille.py --limit 10      # solo i primi 10
  python3 scripts/genera-braille.py --force         # ignora idempotenza
  python3 scripts/genera-braille.py --article SLUG  # solo quel articolo
  python3 scripts/genera-braille.py --verbose       # DEBUG logging
"""

import argparse
import logging
import re
import sys
from pathlib import Path

try:
    import louis
except ImportError:
    sys.exit("ERRORE: python3-louis non installato. Esegui:\n"
             "  sudo apt-get install -y python3-louis liblouis-data")

try:
    import yaml
except ImportError:
    sys.exit("ERRORE: pyyaml non installato. Esegui:\n"
             "  sudo apt-get install -y python3-yaml")


# ============================================================
# CONFIGURAZIONE
# ============================================================
SOURCE_DIR = Path("content/comunicazioni")
OUTPUT_DIR = Path("static/braille/comunicazioni")
TABLE = "it-it-comp6.utb"   # braille italiano 6 punti, ASCII output
LINE_WIDTH = 40             # standard ICEB per stampanti braille comuni
PAGE_LENGTH = 25            # 25 righe per pagina A4 braille
FORM_FEED = "\x0c"          # delimitatore pagine BRF
ENCODING = "ascii"          # BRF è ASCII puro


# ============================================================
# LOGGING
# ============================================================
logging.basicConfig(
    format="%(levelname)s %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("genera-braille")


# ============================================================
# 1. FRONTMATTER PARSING
# ============================================================
def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Separa frontmatter YAML dal body Markdown.

    Restituisce (dict_frontmatter, body_string).
    Tollera frontmatter assente: in tal caso ({}, text).
    """
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as e:
        log.warning(f"YAML malformato: {e}")
        fm = {}
    body = parts[2].lstrip("\n")
    return fm, body


# ============================================================
# 2. SHORTCODE PARSING
# ============================================================
# Regex per shortcode con attributi quotati: {{< nome attr1="val" attr2="val" >}}
# - cattura nome + tutto il blob attributi
# Funziona sia per shortcode self-closing che per la apertura di shortcode-pair.
SHORTCODE_OPEN = re.compile(
    r"""\{\{<\s*
        (?P<name>/?[a-z][a-z0-9_-]*)
        (?P<attrs>(?:\s+[a-zA-Z][a-zA-Z0-9_-]*=(?:"[^"]*"|'[^']*'))*)
        \s*>\}\}""",
    re.VERBOSE | re.DOTALL,
)
# Regex per shortcode con contenuto inner: {{< nome >}}body{{< /nome >}}
SHORTCODE_PAIR = re.compile(
    r"""\{\{<\s*(?P<name>[a-z][a-z0-9_-]*)
        (?P<attrs>(?:\s+[a-zA-Z][a-zA-Z0-9_-]*=(?:"[^"]*"|'[^']*'))*)
        \s*>\}\}
        (?P<body>.*?)
        \{\{<\s*/(?P=name)\s*>\}\}""",
    re.VERBOSE | re.DOTALL,
)
ATTR_RE = re.compile(r"""([a-zA-Z][a-zA-Z0-9_-]*)=("([^"]*)"|'([^']*)')""")


def parse_attrs(attrs_blob: str) -> dict:
    """Estrae attributi `key="val"` da una stringa tipo ' alt="X" caption="Y"'."""
    d = {}
    for m in ATTR_RE.finditer(attrs_blob or ""):
        key = m.group(1)
        val = m.group(3) if m.group(3) is not None else m.group(4) or ""
        d[key] = val
    return d


# Set di shortcode "consumabili" come pair (con contenuto inner)
PAIR_SHORTCODES = {"cosa-non-fare"}

# Registro shortcode incontrati ma non gestiti (per warning summary)
unknown_shortcodes_seen: dict[str, int] = {}


def render_shortcode(name: str, attrs: dict, inner: str = "") -> str:
    """Risolve uno shortcode in testo piano braille-friendly."""
    if name == "foto":
        alt = attrs.get("alt", "").strip()
        caption = attrs.get("caption", "").strip()
        if alt and caption:
            return f"[Foto: {alt}. Didascalia: {caption}.]"
        if alt:
            return f"[Foto: {alt}.]"
        return "[Foto.]"
    if name == "pittogramma":
        alt = attrs.get("alt", "").strip()
        caption = attrs.get("caption", "").strip()
        if alt:
            return f"[Pittogramma: {alt}.]"
        return "[Pittogramma.]"
    if name == "cosa-non-fare":
        titolo = attrs.get("titolo", "Cosa NON fare").strip()
        # inner è Markdown — viene riprocessato dal pipeline più sotto.
        return f"\n[{titolo.upper()}]\n\n{inner}\n"
    if name == "chi-chiamare":
        return ("\nChi chiamare in caso di pericolo: 112 (Numero Unico "
                "Europeo per l'Emergenza), 115 (Vigili del Fuoco), 1515 "
                "(Carabinieri Forestali).\n")
    # Sconosciuto: log e rimozione
    unknown_shortcodes_seen[name] = unknown_shortcodes_seen.get(name, 0) + 1
    log.warning(f"Shortcode non gestito: {{{{< {name} ... >}}}} — rimosso")
    return ""


def resolve_shortcodes(text: str) -> str:
    """Risolve tutti gli shortcode (pair prima, single dopo) in testo piano."""
    # 1. Shortcode con coppia di tag (cosa-non-fare, ecc.)
    def _pair_sub(m):
        name = m.group("name")
        if name in PAIR_SHORTCODES:
            attrs = parse_attrs(m.group("attrs"))
            return render_shortcode(name, attrs, inner=m.group("body"))
        # se è una pair sconosciuta, tieni il contenuto inner (più sicuro)
        unknown_shortcodes_seen[name] = unknown_shortcodes_seen.get(name, 0) + 1
        log.warning(f"Shortcode pair non gestito: {{{{< {name} ... >}}}} — inner preservato")
        return m.group("body")

    text = SHORTCODE_PAIR.sub(_pair_sub, text)

    # 2. Shortcode self-closing (foto, pittogramma, chi-chiamare, ...)
    def _single_sub(m):
        name = m.group("name")
        if name.startswith("/"):
            # tag di chiusura orfano — ignora
            return ""
        attrs = parse_attrs(m.group("attrs"))
        return render_shortcode(name, attrs)

    text = SHORTCODE_OPEN.sub(_single_sub, text)
    return text


# ============================================================
# 3. MARKDOWN → PLAIN TEXT
# ============================================================
RE_H1 = re.compile(r"^# (.+)$", re.MULTILINE)
RE_H2 = re.compile(r"^## (.+)$", re.MULTILINE)
RE_H3PLUS = re.compile(r"^#{3,6} (.+)$", re.MULTILINE)
RE_BOLD = re.compile(r"\*\*([^*]+)\*\*")
RE_ITALIC = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")
RE_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
RE_LIST_DASH = re.compile(r"^(\s*)-\s+(.+)$", re.MULTILINE)
RE_INLINE_CODE = re.compile(r"`([^`]+)`")
RE_CODE_BLOCK = re.compile(r"```[a-z]*\n(.*?)\n```", re.DOTALL)
RE_HR = re.compile(r"^---+\s*$", re.MULTILINE)
RE_MULTI_NEWLINE = re.compile(r"\n{3,}")


def markdown_to_plain(text: str) -> str:
    """Trasforma Markdown in testo piano braille-friendly."""
    # Code blocks (prefisso "CODICE:")
    text = RE_CODE_BLOCK.sub(lambda m: f"CODICE:\n{m.group(1)}", text)

    # Heading: # H1 e ## H2 → MAIUSCOLO + linee vuote
    text = RE_H1.sub(lambda m: f"\n\n{m.group(1).upper()}\n", text)
    text = RE_H2.sub(lambda m: f"\n\n{m.group(1).upper()}\n", text)
    # H3+ → Title Case (iniziali maiuscole su parole significative)
    text = RE_H3PLUS.sub(lambda m: f"\n\n{m.group(1).title()}\n", text)

    # Liste con dash → asterisco (l'asterisco verrà tradotto da liblouis)
    text = RE_LIST_DASH.sub(lambda m: f"{m.group(1)}* {m.group(2)}", text)

    # Link: assoluti → "testo (URL)", relativi → solo "testo"
    def _link_sub(m):
        testo, url = m.group(1), m.group(2)
        if url.startswith(("http://", "https://")):
            return f"{testo} ({url})"
        # mailto:, tel:, relativi → solo testo
        return testo

    text = RE_LINK.sub(_link_sub, text)

    # Bold / italic → solo testo (Grade 1 italiano non ha standard di enfasi)
    text = RE_BOLD.sub(r"\1", text)
    text = RE_ITALIC.sub(r"\1", text)

    # Inline code: preserva il contenuto, rimuovi i backtick
    text = RE_INLINE_CODE.sub(r"\1", text)

    # Horizontal rule "---" come separatore → linea di asterischi
    text = RE_HR.sub("* * *", text)

    # Normalizza linee vuote multiple a max due
    text = RE_MULTI_NEWLINE.sub("\n\n", text)

    return text.strip()


# ============================================================
# 4. TRADUZIONE BRAILLE
# ============================================================
def to_braille(plain_text: str) -> str:
    """Traduce testo italiano in braille ASCII (tabella comp6)."""
    return louis.translateString(
        [TABLE],
        plain_text,
        typeform=None,
        mode=0,
    )


# ============================================================
# 5. PAGINAZIONE BRF
# ============================================================
def word_wrap(text: str, width: int) -> list[str]:
    """Word-wrap rispettando spazi. Non spezza parole; se una singola
    parola eccede `width`, viene comunque messa su una riga propria."""
    output_lines: list[str] = []
    for paragraph in text.split("\n"):
        if not paragraph:
            output_lines.append("")
            continue
        words = paragraph.split(" ")
        line = ""
        for w in words:
            if not line:
                line = w
            elif len(line) + 1 + len(w) <= width:
                line += " " + w
            else:
                output_lines.append(line)
                line = w
        if line:
            output_lines.append(line)
    return output_lines


def paginate(braille_text: str, title: str = "") -> str:
    """Spezza il testo in pagine, ognuna con intestazione (titolo + numero
    pagina) e form-feed. Restituisce stringa ASCII BRF-ready.

    Intestazione: prima riga = titolo troncato (sinistra) + "#N" destra-allineato.
    Pagina 1 ha titolo completo (centrato), pagine successive titolo troncato.
    """
    body_lines = word_wrap(braille_text, LINE_WIDTH)
    # Su ogni pagina: 1 riga intestazione + 1 riga vuota + (PAGE_LENGTH-2) righe corpo
    content_lines_per_page = PAGE_LENGTH - 2
    pages: list[list[str]] = []
    for i in range(0, len(body_lines), content_lines_per_page):
        pages.append(body_lines[i:i + content_lines_per_page])

    if not pages:
        pages = [[]]

    # Costruzione output
    title_braille = to_braille(title).strip() if title else ""
    out_pages: list[str] = []
    for n, page_lines in enumerate(pages, start=1):
        page_num = f"#{n}"
        # Titolo troncato per stare in width - len(page_num) - 1 (spazio)
        max_title_len = LINE_WIDTH - len(page_num) - 1
        truncated_title = title_braille[:max_title_len] if title_braille else ""
        header = (
            truncated_title.ljust(LINE_WIDTH - len(page_num))
            + page_num
        )
        page_str = header + "\n" + "".ljust(LINE_WIDTH) + "\n"
        # Padding pagine corte con linee vuote per arrivare a PAGE_LENGTH
        body = "\n".join(page_lines)
        page_str += body
        # Aggiungi linee vuote per arrivare a PAGE_LENGTH (esclusa header)
        actual_lines = len(page_lines)
        while actual_lines < content_lines_per_page:
            page_str += "\n"
            actual_lines += 1
        out_pages.append(page_str)
    return FORM_FEED.join(out_pages)


# ============================================================
# 6. PIPELINE COMPLETA SU UN ARTICOLO
# ============================================================
def process_article(md_file: Path, output_dir: Path, force: bool = False) -> str:
    """Restituisce stato: 'generated' | 'skip-uptodate' | 'skip-draft' | 'error'."""
    slug = md_file.stem
    brf_file = output_dir / f"{slug}.brf"

    try:
        text = md_file.read_text(encoding="utf-8")
    except Exception as e:
        log.error(f"{slug}: lettura fallita: {e}")
        return "error"

    fm, body = parse_frontmatter(text)
    if fm.get("draft", False):
        log.info(f"SKIP-DRAFT {slug}")
        return "skip-draft"

    # Idempotenza: skip se .brf più nuovo del .md
    if not force and brf_file.exists():
        if brf_file.stat().st_mtime >= md_file.stat().st_mtime:
            log.debug(f"SKIP-UPTODATE {slug}")
            return "skip-uptodate"

    title = fm.get("title", slug)
    try:
        body = resolve_shortcodes(body)
        plain = markdown_to_plain(body)
        # Trattare anche il titolo come parte del documento (intestazione)
        full_plain = title.upper() + "\n\n" + plain
        braille = to_braille(full_plain)
        paginated = paginate(braille, title=title)

        # Verifica purezza ASCII (i .brf devono essere ASCII puro)
        try:
            paginated.encode(ENCODING)
        except UnicodeEncodeError as e:
            # Se la traduzione braille ha lasciato caratteri non-ASCII,
            # significa che la tabella non li ha mappati. Loghiamo.
            log.warning(f"{slug}: caratteri non-ASCII residui ({e.reason})")
            # Fallback: strippa con replace
            paginated = paginated.encode(ENCODING, errors="replace").decode(ENCODING)

        output_dir.mkdir(parents=True, exist_ok=True)
        brf_file.write_text(paginated, encoding=ENCODING)
        log.info(f"OK {slug} ({brf_file.stat().st_size} bytes)")
        return "generated"
    except Exception as e:
        log.error(f"{slug}: generazione fallita: {e}")
        return "error"


# ============================================================
# 7. CLI
# ============================================================
def main():
    parser = argparse.ArgumentParser(
        description="Genera versioni Braille (BRF) degli articoli del sito."
    )
    parser.add_argument("--force", action="store_true",
                        help="Ignora l'idempotenza, rigenera tutto.")
    parser.add_argument("--limit", type=int, default=None,
                        help="Processa solo i primi N articoli (test).")
    parser.add_argument("--article", type=str, default=None,
                        help="Processa solo l'articolo con quello slug.")
    parser.add_argument("--verbose", action="store_true",
                        help="Logging DEBUG.")
    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)

    if not SOURCE_DIR.exists():
        sys.exit(f"ERRORE: cartella sorgente non trovata: {SOURCE_DIR}")

    log.info(f"liblouis {louis.version()} | tabella {TABLE} | "
             f"line-width {LINE_WIDTH} | page-length {PAGE_LENGTH}")

    if args.article:
        candidates = list(SOURCE_DIR.glob(f"{args.article}*.md"))
        if not candidates:
            sys.exit(f"ERRORE: nessun articolo matcha lo slug '{args.article}'")
        md_files = candidates[:1]
    else:
        md_files = sorted(SOURCE_DIR.glob("*.md"))

    if args.limit:
        md_files = md_files[:args.limit]

    counts = {"generated": 0, "skip-uptodate": 0, "skip-draft": 0, "error": 0}
    for md in md_files:
        status = process_article(md, OUTPUT_DIR, force=args.force)
        counts[status] = counts.get(status, 0) + 1

    # Riepilogo finale
    print()
    print("=" * 60)
    print("RIEPILOGO")
    print("=" * 60)
    print(f"  Articoli processati:    {sum(counts.values())}")
    print(f"  Generati:               {counts['generated']}")
    print(f"  Skip (up-to-date):      {counts['skip-uptodate']}")
    print(f"  Skip (draft):           {counts['skip-draft']}")
    print(f"  Errori:                 {counts['error']}")
    if unknown_shortcodes_seen:
        print(f"  Shortcode non gestiti:")
        for name, c in sorted(unknown_shortcodes_seen.items(),
                              key=lambda kv: -kv[1]):
            print(f"    {{{{< {name} >}}}}  ({c} occorrenze)")
    return 0 if counts["error"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
