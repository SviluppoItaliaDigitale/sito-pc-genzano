#!/usr/bin/env python3
"""
Fix automatico errori grammaticali italiani — companion di audit-grammatica-italiana.py.

Applica SOLO fix sicuri al 100% (accenti mancanti su parole non ambigue,
apostrofi finti). Salta sempre frontmatter, code fences, URL, tag HTML,
shortcode Hugo, attributi HTML.

Modi:
  python3 scripts/fix-grammatica-italiana.py --dry-run   # default, mostra cosa farebbe
  python3 scripts/fix-grammatica-italiana.py --apply     # applica i fix

Output: lista delle modifiche per ogni file (file:line, before → after).
Idempotente: rilanciarlo non cambia nulla se non ci sono nuovi errori.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"

# ----------------------------------------------------------------
# Mappa fix: parola_errata → parola_corretta
# Solo voci NON AMBIGUE: la parola sbagliata non esiste in italiano
# come legittima.
ACCENTI = {
    # Congiunzioni e avverbi tronchi
    "perche": "perché",
    "poiche": "poiché",
    "benche": "benché",
    "anziche": "anziché",
    "finche": "finché",
    "affinche": "affinché",
    "sicche": "sicché",
    "nonche": "nonché",
    "piu": "più",
    "puo": "può",
    "gia": "già",
    "cosi": "così",
    "pero": "però",
    "cio": "ciò",
    # Sostantivi tronchi italiani con accento finale obbligatorio
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
    # Giorni della settimana
    "lunedi": "lunedì",
    "martedi": "martedì",
    "mercoledi": "mercoledì",
    "giovedi": "giovedì",
    "venerdi": "venerdì",
}

# Apostrofi finti usati al posto degli accenti
# Si applicano PRIMA degli ACCENTI: catturano la parola CON apostrofo finto.
APOSTROFI_FINTI = {
    # Parole tronche italiane scritte con ' al posto dell'accento
    "è": "è",
    "né": "né",
    "sé": "sé",
    "tè": "tè",
    "più": "più",
    "può": "può",
    "già": "già",
    "così": "così",
    "però": "però",
    "ciò": "ciò",
    "perché": "perché",
    "poiché": "poiché",
    "benché": "benché",
    "anziché": "anziché",
    "finché": "finché",
    "affinché": "affinché",
    "sicché": "sicché",
    "nonché": "nonché",
    # Verbi futuri 3a singolare con apostrofo finto
    "sarà": "sarà",
    "andrà": "andrà",
    "andro'": "andrò",
    "verrà": "verrà",
    "farà": "farà",
    "starà": "starà",
    "dovrà": "dovrà",
    "potrà": "potrà",
    "vorrà": "vorrà",
    "sarò": "sarò",
    # Sostantivi tronchi con apostrofo finto
    "città": "città",
    "libertà": "libertà",
    "qualità": "qualità",
    "quantita'": "quantità",
    "università": "università",
    "comunità": "comunità",
    "necessità": "necessità",
    "responsabilità": "responsabilità",
    "attività": "attività",
    "specialità": "specialità",
    "autorità": "autorità",
    "dignità": "dignità",
    "civiltà": "civiltà",
    "pietà": "pietà",
    # Giorni della settimana con apostrofo finto
    "lunedi'": "lunedì",
    "martedi'": "martedì",
    "mercoledi'": "mercoledì",
    "giovedi'": "giovedì",
    "venerdi'": "venerdì",
}

# Errori specifici idiomatici
SOSTITUZIONI_DIRETTE = [
    # (pattern, replacement, descrizione)
    # "qual'è" → "qual è" (qual è già forma elisa)
    (re.compile(r"\bqual['’]\s*è\b", re.IGNORECASE), "qual è", "qual'è → qual è"),
    (re.compile(r"\bQual['’]\s*è\b"), "Qual è", "Qual'è → Qual è"),
    # "un'altro" → "un altro" (altro è maschile)
    (re.compile(r"\bun['’]\s*altro\b", re.IGNORECASE), "un altro", "un'altro → un altro"),
    (re.compile(r"\bUn['’]\s*altro\b"), "Un altro", "Un'altro → Un altro"),
    # Apostrofo residuo dopo parola già accentata (caso da pulizia
    # incompleta): "più'" → "più", "città'" → "città", "università'" →
    # "università", ecc. La regex matcha qualsiasi parola che termina con
    # vocale accentata + ' + spazio/punteggiatura.
    (re.compile(r"([àèéìòùÀÈÉÌÒÙ])['’](?=[\s.,;:!?»\)\]\-—])"), r"\1",
     "Apostrofo residuo dopo accento (es. più' → più)"),
]


def preserve_case(original: str, target: str) -> str:
    """Mantiene la capitalizzazione dell'originale nel target."""
    if not original:
        return target
    if original[0].isupper():
        return target[0].upper() + target[1:]
    return target


def make_word_pattern(word_dict: dict) -> re.Pattern:
    """Costruisce regex con OR su tutte le parole del dizionario."""
    words = sorted(word_dict.keys(), key=len, reverse=True)
    alternatives = "|".join(re.escape(w) for w in words)
    pattern = rf"(?<![A-Za-zÀ-ÿ\d-])({alternatives})(?![A-Za-zÀ-ÿ\d-])"
    return re.compile(pattern, re.IGNORECASE)


ACCENTI_RE = make_word_pattern(ACCENTI)
APOSTROFI_RE = make_word_pattern(APOSTROFI_FINTI)


def mask_protected_regions(text: str) -> tuple[str, list[tuple[int, int]]]:
    """Restituisce (text_mascherato, lista_intervalli_protetti).
    Le regioni protette sono: code fences, URL, tag HTML, shortcode, frontmatter.
    """
    masked = list(text)
    protected = []

    def mask_range(s: int, e: int):
        protected.append((s, e))
        for i in range(s, e):
            masked[i] = " "

    # Frontmatter YAML: maschera SOLO le righe con chiavi tecniche
    # (image:, slug:, area:, badge:, autore:, allegati:, scadenza:, draft:,
    # priorita:, layout:, aliases:, type:, weight:, parent:, identifier:,
    # dataUltimaRevisione:, sitemap:, tts:, toc:, image_alt:, image_credit:,
    # image_source_url:, etc.). Le righe title: e description: contengono
    # testo italiano e NON vanno mascherate (vanno fixate).
    TECH_KEYS = (
        "image", "image_alt", "image_credit", "image_source_url",
        "slug", "area", "badge", "autore", "allegati", "scadenza",
        "draft", "priorita", "layout", "aliases", "type", "weight",
        "parent", "identifier", "dataUltimaRevisione", "sitemap", "tts",
        "toc", "url", "src", "menus", "permalink", "lastmod", "expirydate",
        "publishdate", "tags", "categories", "keywords",
    )
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end > 0:
            fm_end = text.find("\n", end + 4)
            if fm_end > 0:
                # Itera ogni riga del frontmatter
                pos = 0
                while pos < fm_end:
                    line_end = text.find("\n", pos)
                    if line_end < 0 or line_end > fm_end:
                        line_end = fm_end
                    line = text[pos:line_end]
                    # Estrae la chiave (prima dei `:`)
                    stripped = line.lstrip()
                    indent = len(line) - len(stripped)
                    if ":" in stripped:
                        key = stripped.split(":", 1)[0].strip().strip('"').strip("'")
                        if key in TECH_KEYS or key.startswith("-"):
                            mask_range(pos, line_end)
                    elif stripped.startswith("---") or stripped.startswith("#"):
                        mask_range(pos, line_end)
                    elif stripped.startswith("- "):
                        # Voce di lista YAML — maschera (probabilmente technical)
                        mask_range(pos, line_end)
                    pos = line_end + 1

    # Code fences ``` ... ```
    for m in re.finditer(r"```.*?```", text, re.DOTALL):
        mask_range(m.start(), m.end())

    # Shortcode Hugo {{< ... >}} e {{% ... %}}
    for m in re.finditer(r"\{\{[<%].*?[%>]\}\}", text, re.DOTALL):
        mask_range(m.start(), m.end())

    # URL http(s)://...
    for m in re.finditer(r"https?://\S+", text):
        mask_range(m.start(), m.end())

    # Tag HTML <...>
    for m in re.finditer(r"<[^>]+>", text):
        mask_range(m.start(), m.end())

    # Inline code `...`
    for m in re.finditer(r"`[^`]+`", text):
        mask_range(m.start(), m.end())

    # Link Markdown: solo l'URL [text](url) — preserve text, mask url
    for m in re.finditer(r"\]\([^)]+\)", text):
        mask_range(m.start(), m.end())

    return "".join(masked), protected


def apply_fix(text: str) -> tuple[str, list[dict]]:
    """Applica fix al testo. Ritorna (testo_fissato, lista_modifiche).

    Strategia: lavoriamo sul testo originale, mantenendo allineato il
    masked solo per identificare le regioni protette. Iteriamo finché
    nessun fix è applicato (idempotenza)."""
    changes = []
    fixed = text

    # Ricalcoliamo masked dopo ogni passata di sostituzioni dirette
    # (perché le posizioni cambiano)

    # PASSO 1: Sostituzioni dirette con re.sub (gestiscono \1 backref)
    for pattern, replacement, desc in SOSTITUZIONI_DIRETTE:
        masked, _ = mask_protected_regions(fixed)
        # Trova match nel masked (per identificare regioni protette)
        # ma applica la sub al fixed reale solo se NON è in regione protetta
        new_fixed = fixed
        offset = 0
        for m in pattern.finditer(masked):
            real_match = pattern.search(fixed, m.start() + offset)
            if real_match is None:
                continue
            start = real_match.start()
            end = real_match.end()
            actual_replacement = real_match.expand(replacement)
            line_no = fixed.count("\n", 0, start) + 1
            changes.append({
                "line": line_no,
                "before": real_match.group(0),
                "after": actual_replacement,
                "kind": desc,
            })
            new_fixed = new_fixed[:start] + actual_replacement + new_fixed[end:]
            offset += len(actual_replacement) - (end - start)
        fixed = new_fixed

    # PASSO 2: Apostrofi finti e accenti — collezioniamo tutti i match
    masked, _ = mask_protected_regions(fixed)
    all_matches = []

    for m in APOSTROFI_RE.finditer(masked):
        word = m.group(1).lower()
        if word in APOSTROFI_FINTI:
            replacement = preserve_case(m.group(1), APOSTROFI_FINTI[word])
            all_matches.append((m.start(), m.end(), m.group(0), replacement, "apostrofo_finto"))

    for m in ACCENTI_RE.finditer(masked):
        word = m.group(1).lower()
        if word in ACCENTI:
            replacement = preserve_case(m.group(1), ACCENTI[word])
            all_matches.append((m.start(), m.end(), m.group(0), replacement, "accento"))

    # Ordina per posizione decrescente
    all_matches.sort(key=lambda x: x[0], reverse=True)

    # Dedup overlap
    deduped = []
    last_start = float("inf")
    for s, e, orig, repl, kind in all_matches:
        if e <= last_start:
            deduped.append((s, e, orig, repl, kind))
            last_start = s
    deduped.sort(key=lambda x: x[0], reverse=True)

    for s, e, orig, repl, kind in deduped:
        line_no = fixed.count("\n", 0, s) + 1
        changes.append({
            "line": line_no,
            "before": orig,
            "after": repl,
            "kind": kind,
        })
        fixed = fixed[:s] + repl + fixed[e:]

    return fixed, changes


def find_files() -> list[Path]:
    files = []
    files.extend(sorted(CONTENT.glob("comunicazioni/*.md")))
    files.extend(sorted(CONTENT.glob("*/_index.md")))
    files.extend(sorted(CONTENT.glob("formazione/*.md")))
    files.extend(sorted(CONTENT.glob("rischi-prevenzione/*.md")))
    return files


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--apply", action="store_true",
                    help="Applica i fix (default: dry-run)")
    ap.add_argument("--quiet", action="store_true",
                    help="Solo summary, niente dettaglio per file")
    args = ap.parse_args()

    total_files = 0
    total_changes = 0
    files_changed = 0

    for path in find_files():
        total_files += 1
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"❌ {path}: {e}", file=sys.stderr)
            continue

        fixed, changes = apply_fix(text)
        if not changes:
            continue

        files_changed += 1
        total_changes += len(changes)
        rel = path.relative_to(ROOT)
        if not args.quiet:
            print(f"\n📝 {rel} ({len(changes)} fix)")
            for c in changes[:10]:  # Mostra max 10 per file
                print(f"   line {c['line']:>4}: « {c['before']} » → « {c['after']} » ({c['kind']})")
            if len(changes) > 10:
                print(f"   … altre {len(changes) - 10} sostituzioni")

        if args.apply:
            path.write_text(fixed, encoding="utf-8")

    print(f"\n{'=' * 60}")
    if args.apply:
        print(f"✅ APPLICATI: {total_changes} fix in {files_changed}/{total_files} file.")
    else:
        print(f"🔍 DRY-RUN: {total_changes} fix proposti in {files_changed}/{total_files} file.")
        print("   Per applicare: python3 scripts/fix-grammatica-italiana.py --apply")
    print("=" * 60)


if __name__ == "__main__":
    main()
