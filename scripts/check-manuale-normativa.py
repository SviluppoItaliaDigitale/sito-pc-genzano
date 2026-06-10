#!/usr/bin/env python3
# ============================================================================
# Controllo delle norme citate nel Manuale di Protezione Civile (opera viva).
# Estrae da content/manuale/**.md le citazioni normative e tecniche, raggruppate
# per capitolo, e produce un report Markdown: una CHECKLIST di verifica vigenza.
# NON modifica nulla e NON giudica la vigenza (lo fa l'agent pc-normative-verifier
# in sessione, su Normattiva/BURL) — flag, non riscrittura automatica (NO INVENZIONI).
#
# Uso:  python3 scripts/check-manuale-normativa.py   (stampa il report su stdout)
# Il workflow controllo-manuale-normativa.yml ne usa l'output per un'issue mensile.
# ============================================================================
import os, re, glob

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(REPO, "content", "manuale")

# pattern delle citazioni (norme italiane + standard tecnici)
PATTERNS = [
    r"decreto legislativo[^,.;]*?n\.?\s*\d+[^,.;]*?\d{4}",
    r"d\.?\s?lgs\.?\s*\d+/\d{4}",
    r"legge(?:\s+costituzionale)?[^,.;]*?n\.?\s*\d+[^,.;]*?\d{4}",
    r"\bl\.?\s*\d+/\d{4}",
    r"\bl\.?\s?r\.?\s*\d+/\d{4}",
    r"d\.?\s?p\.?\s?c\.?\s?m\.?[^,.;]*?\d{4}",
    r"d\.?\s?p\.?\s?r\.?\s*\d+/\d{4}",
    r"d\.?\s?m\.?[^,.;]*?\d{4}",
    r"direttiv[ao][^,.;]*?\d{4}",
    r"decisione[^,.;]*?UE[^,.;]*?\d{4}",
    r"circolare[^,.;]*?\d{4}",
    r"UNI\s*\d{4,5}(?::\d{4})?",
    r"ISO\s*\d{3,5}(?::\d{4})?",
    r"urn:nir:[^\s\")]+",
]
RX = re.compile("|".join("(%s)" % p for p in PATTERNS), re.IGNORECASE)


def norm(s):
    return re.sub(r"\s+", " ", s.strip().rstrip(".,;)»").lstrip("(«")).strip()


def main():
    files = sorted(f for f in glob.glob(os.path.join(MAN, "*.md"))
                   if os.path.basename(f) not in ("_index.md", "versione-stampabile.md"))
    blocks, total = [], 0
    for f in files:
        txt = open(f, encoding="utf-8").read()
        title = re.search(r'^title:\s*"?(.*?)"?\s*$', txt, re.M)
        title = title.group(1) if title else os.path.basename(f)
        cites = {norm(m.group(0)) for m in RX.finditer(txt)}
        cites = sorted(c for c in cites if len(c) > 3)
        if cites:
            total += len(cites)
            blocks.append((title, os.path.basename(f), cites))

    lines = [
        "## Checklist — vigenza delle norme citate nel Manuale di Protezione Civile",
        "",
        f"Capitoli con citazioni: **{len(blocks)}** · riferimenti totali: **{total}**.",
        "",
        "Verificare con l'agent `pc-normative-verifier` (Normattiva / BURL Lazio) che ogni "
        "norma sia **vigente** e non abrogata/sostituita. Se una norma è cambiata, "
        "aggiornare il capitolo (e rigenerare il PDF). **Flag, non riscrittura automatica — "
        "NO INVENZIONI.** Per gli standard ISO/UNI, controllare l'edizione vigente su iso.org/uni.com.",
        "",
    ]
    for title, fname, cites in blocks:
        lines.append(f"### {title}")
        lines.append(f"`content/manuale/{fname}`")
        lines.append("")
        for c in cites:
            lines.append(f"- [ ] {c}")
        lines.append("")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
