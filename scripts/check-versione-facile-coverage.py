#!/usr/bin/env python3
"""
check-versione-facile-coverage.py — Audit della copertura "versione facile" (A2).

Scansiona gli articoli in content/comunicazioni/ e individua quelli che, per i
criteri editoriali del progetto (CLAUDE.md § "Automatismo totale sugli articoli"
e manuale/parte-25 § 25.7), DOVREBBERO avere una versione in italiano semplice
(CEFR A2) `<slug>-facile.md` ma ne sono sprovvisti.

Criteri di qualificazione (un articolo "merita" la facile se):
  - badge in {Allerta, Emergenza, Prevenzione}  → sempre (alta priorità);
  - badge in {Formazione, Informazione} E il contenuto cita norme dense
    (ISO, D.Lgs., DPCM, L. NNN, Direttiva…) OPPURE riguarda categorie
    vulnerabili OPPURE descrive procedure operative (112, IT-alert, kit
    emergenza, piano familiare, evacuazione, primo soccorso…).
Esclusi per design: bilanci, ricorrenze/giornate (badge Informazione senza
segnali operativi), eventi/feste, comunicati di servizio, Aggiornamento,
Radiocomunicazioni, Volontariato, Attività, Esercitazione, Avviso, Evento.

Output (consumato da audit-versione-facile-coverage.yml):
  - prima riga "OK_NO_MISSING" se nessun candidato scoperto;
  - altrimenti "MISSING_FACILE_FOUND" + corpo Markdown dell'issue.

Uso: python3 scripts/check-versione-facile-coverage.py
"""

import re
import sys
from pathlib import Path

BADGE_SEMPRE = {"Allerta", "Emergenza", "Prevenzione"}
BADGE_CONDIZIONALE = {"Formazione", "Informazione"}
# Tutti gli altri badge → esclusi per design.

NORM_REGEX = re.compile(
    r"\bISO\s+\d|\bIEC\b|D\.?\s?Lgs\.?|DPCM|\bDPR\b|\bD\.M\.|\bL\.R\.|"
    r"\bL\.\s*\d|Direttiva\b|Regolamento\b|Codice della Protezione Civile|"
    r"\bDGR\b|\bWCAG\b",
)
VULNERABLE_KW = (
    "anzian", "disabil", "vulnerabil", "fragil", "bambin", "neonat",
    "gravidanz", "caregiver", "italiano l2", "stranier", "non vedent",
    "non udent", "sord", "ciec", " rsa", "senza fissa dimora", "minori",
)
OPERATIONAL_KW = (
    "112", "it-alert", "kit di emergenza", "kit emergenza", "kit di",
    "piano familiare", "piano di emergenza", "evacuazion", "autoprotezione",
    "primo soccorso", "defibrillator", "antisoffocamento", "colpo di calore",
    "cosa fare", "cosa non fare", "numero unico", "punto di raccolta",
)
# Per il badge Informazione: segnali di "ricorrenza/giornata" che da soli
# NON qualificano (servono segnali operativi per promuovere).
RICORRENZA_KW = (
    "giornata", "anniversario", "ricorrenza", " festa", "auguri",
    "natal", "tradizione", "vacanze",
)


def parse_frontmatter(text: str) -> dict:
    """Estrae i campi chiave dal frontmatter senza dipendenze YAML pesanti."""
    fm = {}
    if not text.startswith("---"):
        return fm
    end = text.find("\n---", 4)
    if end < 0:
        return fm
    block = text[4:end]
    for line in block.splitlines():
        m = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            fm[key] = val.strip('"').strip("'")
    return fm


def qualifies(badge: str, title_lower: str) -> tuple[bool, str]:
    """Ritorna (qualifica, motivo).

    Per alta precisione i segnali condizionali si cercano SOLO nel titolo:
    il titolo dichiara il soggetto dell'articolo, mentre il corpo cita quasi
    sempre 112/anziani/cosa-fare di passaggio (rumore). La decisione resta
    editoriale: meglio pochi candidati certi che 140 falsi positivi.
    """
    if badge in BADGE_SEMPRE:
        return True, f"badge {badge} (alta priorità)"
    if badge in BADGE_CONDIZIONALE:
        # Le ricorrenze/giornate (badge Informazione) non qualificano da sole.
        is_ricorrenza = any(k in title_lower for k in RICORRENZA_KW)
        if NORM_REGEX.search(title_lower) or re.search(r"\biso\s*\d", title_lower):
            return True, "standard/norma nel titolo (ISO, D.Lgs., DPCM…)"
        if not is_ricorrenza and any(k in title_lower for k in VULNERABLE_KW):
            return True, "categorie vulnerabili nel titolo"
        if not is_ricorrenza and any(k in title_lower for k in OPERATIONAL_KW):
            return True, "procedura operativa nel titolo (112, kit, soccorso…)"
    return False, ""


def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    comuni = repo / "content" / "comunicazioni"

    candidati = []  # (slug, title, motivo, date)
    for md in sorted(comuni.glob("*.md")):
        slug = md.stem
        if slug.endswith("-facile"):
            continue
        text = md.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        # Se ha già una versione facile dichiarata o il file affiancato esiste → ok
        if fm.get("versione_facile"):
            continue
        if (comuni / f"{slug}-facile.md").exists():
            continue
        badge = fm.get("badge", "")
        ok, motivo = qualifies(badge, fm.get("title", "").lower())
        if ok:
            candidati.append((slug, fm.get("title", slug), motivo, fm.get("date", "")))

    if not candidati:
        print("OK_NO_MISSING")
        print("Tutti gli articoli che qualificano hanno già la versione facile.")
        return 0

    candidati.sort(key=lambda x: x[3])  # per data crescente
    print("MISSING_FACILE_FOUND")
    print("# Versione facile (A2): articoli candidati ancora scoperti")
    print()
    print(
        f"Trovati **{len(candidati)} articoli** che — per i criteri di "
        "`CLAUDE.md § \"Automatismo totale\"` e `manuale/parte-25 § 25.7` — "
        "dovrebbero avere una versione in italiano semplice (CEFR A2) "
        "`<slug>-facile.md` ma ne sono ancora privi."
    )
    print()
    print("| Articolo | Perché qualifica |")
    print("|---|---|")
    for slug, title, motivo, _ in candidati[:60]:
        t = title if len(title) <= 60 else title[:57] + "…"
        print(f"| `{slug}` — {t} | {motivo} |")
    if len(candidati) > 60:
        print(f"\n…e altri {len(candidati) - 60} articoli.")

    print()
    print("## Come generare una versione facile")
    print()
    print("1. Leggi l'articolo standard in `content/comunicazioni/<slug>.md`.")
    print("2. Crea `content/comunicazioni/<slug>-facile.md` in registro **CEFR A2** "
          "(frasi ≤ 12 parole, lessico comune, sigle spiegate, presente indicativo, "
          "niente subordinate) con frontmatter `versione_facile_di: <slug>` + "
          "`build: { list: never, render: always, publishResources: true }`.")
    print("3. Aggiungi `versione_facile: <slug>-facile` al frontmatter dello standard.")
    print("4. Genera la cover: `python3 scripts/genera-cover.py content/comunicazioni/<slug>-facile.md`.")
    print("5. **Non** invocare `pc-article-reviewer` sulla facile (eccezione gate AGID, "
          "registro A2).")
    print()
    print("Falsi positivi possibili (ricorrenze/comunicati con parole-chiave operative): "
          "valuta caso per caso, la decisione resta editoriale.")
    print()
    print("_Generato da `scripts/check-versione-facile-coverage.py`._")
    return 0


if __name__ == "__main__":
    sys.exit(main())
