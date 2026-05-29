#!/usr/bin/env python3
"""Re-check di freschezza per gli articoli PROGRAMMATI in uscita imminente.

Complementare a `check-freshness.py` (che guarda gli articoli GIÀ PUBBLICATI e
vecchi). Questo script guarda l'altro estremo: gli articoli con `date` FUTURA
che stanno per andare live nei prossimi giorni. Il sito ha una coda editoriale
lunga (a maggio 2026: ~257 articoli programmati fino a febbraio 2027): un pezzo
scritto mesi fa va live "fresco" per data, ma il suo contenuto è congelato al
momento della stesura. Norme citate, numeri di telefono, link esterni e
date-evento possono essere cambiati nel frattempo.

Segnala gli articoli in uscita entro FINESTRA giorni che contengono almeno un
segnale che invecchia, così un redattore può riverificarli PRIMA della
pubblicazione (in sessione con l'agent `pc-content-freshness`, e per le norme
anche `pc-normative-verifier`). Non modifica nulla, non fa deploy.

Esclude le versioni `-facile.md` e gli articoli con `archiviato: true`.
Solo stdlib. Exit code = numero di articoli segnalati (0 = nessuno).
Uso:  python3 scripts/check-articoli-programmati.py [--giorni N]
"""
import os
import re
import sys
import glob
import datetime

DIR = "content/comunicazioni"
OGGI = datetime.date.today()
FINESTRA = 14   # giorni di lookahead (default; sovrascrivibile con --giorni)
CAP = 60        # max voci nel report

RE_DATE = re.compile(r'^date:\s*"?(\d{4}-\d{2}-\d{2})', re.M)
RE_TITLE = re.compile(r'^title:\s*"?(.*?)"?\s*$', re.M)
RE_ARCH = re.compile(r'^archiviato:\s*true', re.M)
# Stessi pattern di check-freshness.py, per coerenza di rilevazione:
RE_TEL = re.compile(r'(\+39[\s.]?\d{6,})|(\b0\d{1,3}[\s./]?\d[\d\s./]{5,}\d)')
RE_NORMA = re.compile(
    r'(D\.?\s?Lgs\.?|D\.?P\.?C\.?M\.?|DPCM|D\.?\s?M\.?\s?\d|L\.R\.|'
    r'Legge\s+(n\.?\s?)?\d|Direttiva\s|Ordinanza\s|Decreto\s+(legge|del|n))', re.I)
RE_EXT = re.compile(r'https?://(?!www\.protezionecivilegenzano\.it)')


def split_frontmatter(testo):
    if testo.startswith("---"):
        parti = testo.split("---", 2)
        if len(parti) >= 3:
            return parti[1], parti[2]
    return testo, testo


def segnali(frontmatter, corpo):
    """Ritorna (forti, contesto).

    Segnali FORTI (consequenziali su un articolo imminente, fanno scattare il
    flag): norme citate (rischio abrogazione/modifica) e numeri di telefono
    (rischio cambio recapito). Sono quelli che `pc-normative-verifier` e
    `pc-content-freshness` devono riverificare prima della pubblicazione.

    Segnale di CONTESTO (non fa scattare il flag da solo, perché quasi ogni
    articolo linka fuori e i link morti sono già coperti da
    `check-links-sito.yml` via lychee): link esterni.
    """
    testo = frontmatter + "\n" + corpo
    forti = []
    if RE_NORMA.search(testo):
        forti.append("norme citate")
    if RE_TEL.search(testo):
        forti.append("numeri di telefono")
    contesto = ["link esterni"] if RE_EXT.search(testo) else []
    return forti, contesto


def main():
    finestra = FINESTRA
    if "--giorni" in sys.argv:
        try:
            finestra = int(sys.argv[sys.argv.index("--giorni") + 1])
        except (ValueError, IndexError):
            pass
    limite = OGGI + datetime.timedelta(days=finestra)

    trovati = []
    for path in sorted(glob.glob(os.path.join(DIR, "*.md"))):
        if path.endswith("-facile.md"):
            continue
        try:
            with open(path, encoding="utf-8") as fh:
                testo = fh.read()
        except OSError:
            continue
        fm, corpo = split_frontmatter(testo)
        if RE_ARCH.search(fm):
            continue
        m = RE_DATE.search(fm)
        if not m:
            continue
        try:
            data = datetime.date.fromisoformat(m.group(1))
        except ValueError:
            continue
        # Solo articoli in uscita imminente: futuri ma entro la finestra.
        if not (OGGI < data <= limite):
            continue
        forti, contesto = segnali(fm, corpo)
        if not forti:
            continue
        tm = RE_TITLE.search(fm)
        titolo = tm.group(1).strip() if tm else os.path.basename(path)
        trovati.append((data, os.path.basename(path), titolo, forti + contesto))

    trovati.sort(key=lambda t: t[0])

    if not trovati:
        print(f"Nessun articolo programmato in uscita nei prossimi {finestra} "
              "giorni contiene segnali che invecchiano.")
        return 0

    print(f"## Articoli programmati in uscita nei prossimi {finestra} giorni "
          "da riverificare\n")
    print(f"Articoli con `date` futura entro il {limite.isoformat()} che "
          "contengono informazioni che possono essere cambiate dalla stesura. "
          "Riverificare **prima** della pubblicazione (agent "
          "`pc-content-freshness`; per le norme anche `pc-normative-verifier`).\n")
    for data, nome, titolo, s in trovati[:CAP]:
        print(f"- **{data.isoformat()}** — {titolo}  \n"
              f"  `{nome}` · segnali: {', '.join(s)}")
    if len(trovati) > CAP:
        print(f"\n…e altri {len(trovati) - CAP} articoli (troncato a {CAP}).")

    return len(trovati)


if __name__ == "__main__":
    sys.exit(main())
