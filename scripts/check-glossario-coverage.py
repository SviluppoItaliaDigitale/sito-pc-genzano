#!/usr/bin/env python3
"""
check-glossario-coverage.py — Audit della copertura del glossario inline.

Scansiona tutti gli articoli e le pagine del sito, estrae le sigle PC
ricorrenti (acronimi maiuscoli 3+ caratteri, con word boundary), confronta
con i termini già presenti in `data/glossario.yaml`, e produce:
  - Elenco sigle non coperte dal glossario (ordinate per frequenza)
  - Elenco sigle coperte ma usate poche volte (candidate alla rimozione)

Il risultato è usato dal workflow `audit-glossario-coverage.yml` per aprire
issue automatica con elenco delle sigle da aggiungere al glossario per
attivare il popover inline su quelle pagine.

Uso: python3 scripts/check-glossario-coverage.py
"""

import re
import sys
import yaml
from pathlib import Path
from collections import Counter

# Sigle da escludere (falsi positivi tipici)
SIGLE_BLACKLIST = {
    # acronimi tecnici irrilevanti / di sistema
    "HTML", "CSS", "JS", "URL", "URI", "API", "DOM", "RSS", "XML", "JSON",
    "PDF", "WEBP", "JPG", "PNG", "SVG", "MP3", "MP4", "GIF", "WAV",
    "HTTP", "HTTPS", "WWW", "FTP", "SMTP", "SSL", "TLS",
    "USB", "GPS", "WIFI", "WI", "FI", "BLE", "RGB", "CMYK", "RAM", "CPU",
    "IT", "OK", "TV", "DJ", "PR",  # 2 char ma sfuggono al filtro 3+
    "BY", "SA", "NC", "ND",  # licenze CC
    "AM", "PM",  # orari
    "DC", "AC",  # corrente
    # parole italiane comuni in maiuscolo (titoli, enfasi)
    "NON", "TUTTI", "FARE", "BENE", "MALE", "PRIMA", "DOPO", "DURANTE",
    "ATTENZIONE", "STOP", "AIUTO", "VIETATO", "OBBLIGO", "AVVISO",
    "EMERGENZA", "ALLERTA", "ALLARME",  # parole frequenti nei titoli sito
    # parole inglesi maiuscole comuni
    "AND", "FOR", "WITH", "FROM", "INTO", "OVER", "UNDER", "THE", "OUR", "YOUR",
    "ALL", "NEW", "NOW", "ONE", "TWO", "TOP", "GET", "SET", "USE",
    # date / numeri romani
    "MM", "DD", "YY", "YYYY", "I", "II", "III", "IV", "VI", "VII", "VIII", "IX",
    # ordinali italiani come "I°", "II°"
}

# Pattern: parola maiuscola 3+ caratteri (sigla PC tipica)
# Include puntini eventuali (es. "D.Lgs.", "L.R.", "FE.PI.VOL.")
SIGLA_REGEX = re.compile(r"\b(?:[A-Z]\.){2,}[A-Z]*\.?|\b[A-Z]{3,}\b")


def load_glossario(path: Path) -> set[str]:
    """Carica le sigle/termini noti dal glossario."""
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return set()
    # Il glossario è un file Markdown con sezioni H2/H3 per ciascun termine
    # Pattern: ## **SIGLA** o ## SIGLA o ### SIGLA
    sigle = set()
    for line in content.splitlines():
        m = re.match(r"^#{2,3}\s+\**([A-Z][A-Z0-9\.\-\s]{2,40})\**\s*(?:—|–|-|:)?", line)
        if m:
            term = m.group(1).strip().rstrip(".").strip()
            # Estrai eventuali sigle dentro
            for s in SIGLA_REGEX.findall(term):
                sigle.add(s.strip("."))
    return sigle


def scan_content(content_root: Path) -> Counter:
    """Scansiona tutti i .md e ritorna Counter delle sigle trovate."""
    counter = Counter()
    for md in content_root.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        # Strip frontmatter
        if text.startswith("---"):
            end = text.find("\n---", 4)
            if end > 0:
                text = text[end + 4:]
        # Strip code blocks
        text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
        # Strip shortcode
        text = re.sub(r"\{\{<[^>]*>\}\}", " ", text)
        # Strip URL
        text = re.sub(r"https?://\S+", " ", text)
        # Estrai sigle
        for m in SIGLA_REGEX.findall(text):
            s = m.strip(".")
            if len(s) < 3 or s in SIGLE_BLACKLIST:
                continue
            counter[s] += 1
    return counter


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    glossario_path = repo_root / "content" / "glossario" / "_index.md"
    content_root = repo_root / "content"

    print(f"Carico glossario da: {glossario_path}", file=sys.stderr)
    sigle_glossario = load_glossario(glossario_path)
    print(f"  Sigle nel glossario: {len(sigle_glossario)}", file=sys.stderr)

    print(f"Scansiono articoli e pagine in: {content_root}", file=sys.stderr)
    sigle_usate = scan_content(content_root)
    print(f"  Sigle uniche trovate: {len(sigle_usate)}", file=sys.stderr)

    # Differenza: usate nei contenuti ma NON nel glossario
    missing = {s: n for s, n in sigle_usate.items() if s not in sigle_glossario}
    missing_sorted = sorted(missing.items(), key=lambda x: -x[1])

    # Soglia: solo sigle usate ≥ 3 volte (per filtrare rumore)
    significative = [(s, n) for s, n in missing_sorted if n >= 3]

    if not significative:
        print("OK_NO_MISSING")
        print("Tutte le sigle ricorrenti del sito sono già nel glossario.")
        return 0

    print("MISSING_SIGLE_FOUND")
    print(f"Trovate {len(significative)} sigle ricorrenti NON ancora nel glossario:")
    print()
    print("| Sigla | Occorrenze | Suggerimento |")
    print("|---|---:|---|")
    for s, n in significative[:40]:
        suggested = suggest_meaning(s)
        print(f"| `{s}` | {n} | {suggested} |")

    if len(significative) > 40:
        print(f"\n…e altre {len(significative) - 40} sigle minori.")

    print()
    print("## Come aggiungere una sigla al glossario")
    print()
    print("1. Apri `content/glossario/_index.md`")
    print("2. Trova la sezione alfabetica appropriata")
    print("3. Aggiungi una nuova voce `### **SIGLA** — Espansione completa` + descrizione AGID 2-3 frasi")
    print("4. Aggiorna eventualmente `data/glossario.yaml` se il termine è da rendere popover inline")
    print()
    print("_Generato da scripts/check-glossario-coverage.py._")

    return 0


def suggest_meaning(sigla: str) -> str:
    """Heuristic suggestions for common PC acronyms."""
    known = {
        "COC": "Centro Operativo Comunale",
        "COI": "Centro Operativo Intercomunale",
        "CCS": "Centro Coordinamento Soccorsi",
        "COM": "Centro Operativo Misto",
        "DPC": "Dipartimento Protezione Civile",
        "DICOMAC": "Direzione Comando e Controllo",
        "SOUP": "Sala Operativa Unificata Permanente",
        "FEPIVOL": "Federazione Provinciale Volontari del Lazio",
        "ASL": "Azienda Sanitaria Locale",
        "AIB": "Antincendio Boschivo",
        "ANPAS": "Associazione Nazionale Pubbliche Assistenze",
        "INGV": "Istituto Nazionale di Geofisica e Vulcanologia",
        "ISPRA": "Istituto Superiore per la Protezione Ambientale",
        "CFR": "Centro Funzionale Regionale",
        "CFC": "Centro Funzionale Centrale",
        "NUE": "Numero Unico di Emergenza",
        "ARES": "Azienda Regionale Emergenza Sanitaria",
        "RUNTS": "Registro Unico Nazionale Terzo Settore",
        "ETS": "Ente del Terzo Settore",
        "OdV": "Organizzazione di Volontariato",
        "CRI": "Croce Rossa Italiana",
        "VVF": "Vigili del Fuoco",
        "DPCM": "Decreto del Presidente del Consiglio dei Ministri",
        "GU": "Gazzetta Ufficiale",
        "BURL": "Bollettino Ufficiale della Regione Lazio",
        "DGR": "Delibera della Giunta Regionale",
        "TAR": "Tribunale Amministrativo Regionale",
        "TUEL": "Testo Unico Enti Locali (D.Lgs. 267/2000)",
        "AGID": "Agenzia per l'Italia Digitale",
        "WCAG": "Web Content Accessibility Guidelines",
        "LIS": "Lingua Italiana dei Segni",
        "CEFR": "Common European Framework of Reference (livelli linguistici)",
        "AEDES": "Agibilità e Danno nell'Emergenza Sismica (scheda)",
        "FAST": "Fabbricati per Sopralluogo Tecnico",
        "DRPC": "Dipartimento Regionale Protezione Civile",
        "ENS": "Ente Nazionale Sordi",
        "RELUIS": "Rete dei Laboratori Universitari di Ingegneria Sismica",
        "CIMA": "Centro Internazionale in Monitoraggio Ambientale",
        "ARASAAC": "Centro Aragonese di Comunicazione Aumentativa e Alternativa",
        "MIM": "Ministero dell'Istruzione e del Merito",
        "ITALERT": "IT-alert, sistema italiano di allarme pubblico",
    }
    return known.get(sigla, "_espansione da definire_")


if __name__ == "__main__":
    sys.exit(main())
