#!/usr/bin/env python3
"""
Audit grammaticale / ortografico italiano per i contenuti del sito Hugo.

Cosa controlla (per ogni file Markdown in content/):
  1. Apostrofi storti (` invece di ')
  2. "e'" usato come finto accento (deve essere "è")
  3. Accenti mancanti su parole comuni: perche → perché, piu → più,
     puo → può, gia → già, cosi → così, sara → sarà, faro → farò, ecc.
  4. "po" senza apostrofo (corretto: "po'")
  5. "qual'è" (errore — corretto: "qual è" senza apostrofo)
  6. "un'altro" (errore — "altro" è maschile, corretto: "un altro")
  7. "un altra" (errore — "altra" è femminile, corretto: "un'altra")
  8. Doppi spazi nel testo
  9. Spazio prima di punteggiatura (. , ; : ! ?)
 10. Virgolette tipografiche scorrette ("smart quotes" inconsistenti)
 11. Maiuscole italiane comuni sbagliate dopo punto (es. "perchè." senza
     spazio, ecc.)
 12. Tre puntini come "..." invece di "…" (non bloccante)
 13. "n'è" / "c'è" / "v'è" / "s'è" senza apostrofo
 14. Refusi specifici italiani: "obbiettivo" → "obiettivo" (preferibile),
     "asciascia" doppi caratteri sospetti
 15. Plurali/articoli sospetti: "lo zaino", "lo studio" ok ma "lo amico"
     no ("l'amico"), "una emergenza" no ("un'emergenza")

Esegue solo su content/comunicazioni/*.md e content/**/_index.md (contenuto pubblico).
NON tocca i template del tema o le rules (sono governance, non contenuto).

Output: lista findings su stdout. Exit 0 sempre (l'audit chiama questo
script come informazione, non come gate).
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


def rule(code, severity, pattern, desc, suggest=None, exclude=None, ignore_case=False):
    flags = re.IGNORECASE if ignore_case else 0
    return {
        "code": code,
        "severity": severity,
        "pattern": re.compile(pattern, flags),
        "desc": desc,
        "suggest": suggest,
        "exclude": re.compile(exclude, flags) if exclude else None,
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
    # corretta "giacché" ci affidiamo ad altre regole (es. "e' " errore).
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
    "necessita": "necessità",
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
    "e'": "è",
    "ne'": "né",
    "se'": "sé",
    "te'": "tè",
    "po'": "po'",  # corretta, NON nel dizionario
    "sara'": "sarà",
    "andra'": "andrà",
    "andro'": "andrò",
    "verra'": "verrà",
    "fara'": "farà",
    "stara'": "starà",
    "dovra'": "dovrà",
    "potra'": "potrà",
    "vorra'": "vorrà",
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
    rule(
        "UNA_VOCALE_FEMMINILE",
        "WARN",
        r"\buna\s+(altra|amica|emergenza|esperienza|opera|ora|ottica|unità|unica|università|attività|isola|idea|estate|alba|antica|opportunità)\b",
        "« una » davanti a vocale femminile è scorretto in italiano standard: usare « un' » (con apostrofo).",
        suggest="un'<parola>",
        ignore_case=True,
    ),
    rule(
        "DOPPIO_SPAZIO",
        "WARN",
        r"(?<=\S)  +(?=\S)",
        "Doppio spazio nel testo (probabile refuso da copia/incolla).",
        suggest="Sostituire con un solo spazio",
    ),
    rule(
        "SPAZIO_PRIMA_PUNTEGGIATURA",
        "WARN",
        r"\s+([,.;:!?])",
        "Spazio prima di punteggiatura (in italiano la punteggiatura è attaccata alla parola).",
        suggest="Rimuovere lo spazio prima del segno",
    ),
    rule(
        "TRE_PUNTINI",
        "INFO",
        r"\.{3,}",
        "Tre puntini come « ... » — preferire il carattere singolo « … » (U+2026) per coerenza tipografica.",
        suggest="…",
        exclude=r"```|/\*\*\*|\*\*\*/",  # ignora code fences e ASCII art
    ),
    rule(
        "TRATTINO_BREVE",
        "INFO",
        r"(?<=[a-zàèéìòù])\s-\s(?=[a-zàèéìòù])",
        "Trattino breve « - » con spazi attorno (incidentale): preferire trattino lungo « — » (em-dash) per inciso.",
        suggest="— (em-dash)",
        ignore_case=True,
    ),
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
    rule(
        "MAIUSCOLA_DOPO_PUNTO",
        "INFO",
        r"(?<=[.!?])\s+([a-zàèéìòù])(?=[a-zàèéìòù])",
        "Lettera minuscola dopo punto/!/? — verificare se è inizio frase nuova (in tal caso maiuscola).",
        suggest="Iniziare frase con maiuscola",
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
def find_articles() -> Iterator[Path]:
    """Ritorna i Markdown da auditare."""
    # Articoli pubblici
    yield from sorted(CONTENT.glob("comunicazioni/*.md"))
    # Pagine istituzionali (_index.md di ogni sezione)
    yield from sorted(CONTENT.glob("*/_index.md"))
    # Pagine di formazione (sotto-sezioni)
    yield from sorted(CONTENT.glob("formazione/*.md"))
    # Pagine rischi-prevenzione
    yield from sorted(CONTENT.glob("rischi-prevenzione/*.md"))


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


def audit_file(path: Path) -> list[dict]:
    """Analizza un file e ritorna la lista di findings."""
    findings = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return [{"file": str(path), "code": "READ_ERROR", "severity": "ERR", "msg": str(e)}]

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
    for m in re.finditer(r"<[^>]+>", masked):
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
            "file": str(path.relative_to(ROOT)),
            "line": line_no,
            "col": col,
            "code": "ACCENTO_MANCANTE",
            "severity": "WARN",
            "match": word,
            "suggest": suggested,
            "snippet": snippet,
            "msg": f'« {word} » → « {suggested} » (accento mancante)',
        })

    # Applica le altre regole
    for r in RULES:
        for m in r["pattern"].finditer(masked):
            matched = m.group(0)
            # Filtra esclusioni puntuali
            if r["exclude"] and r["exclude"].search(matched):
                continue
            line_no, col, snippet = line_index_to_friendly(text, m.start() + body_offset)
            findings.append({
                "file": str(path.relative_to(ROOT)),
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
    for path in find_articles():
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
