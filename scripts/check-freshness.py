#!/usr/bin/env python3
"""Rilevatore di freschezza dei contenuti (content/comunicazioni/).

Segnala gli articoli "anziani" che contengono informazioni che invecchiano e
vanno riverificate: numeri di telefono, citazioni di norme, link esterni. Non
modifica nulla: stampa un report Markdown. La riparazione si fa in sessione con
l'agent `pc-content-freshness`.

Criteri (conservativi, alta precisione — meglio pochi falsi positivi):
  - età > 18 mesi  E  contiene telefono O norma O link esterno;
  - età > 30 mesi  in ogni caso (molto vecchio, da rileggere).
Esclude le versioni `-facile.md` e gli articoli con `archiviato: true`.

Solo stdlib. Exit code = numero di articoli segnalati (0 = nessuno).
Uso:  python3 scripts/check-freshness.py
"""
import os
import re
import sys
import glob
import datetime

DIR = "content/comunicazioni"
OGGI = datetime.date.today()
SOGLIA_CON_SEGNALI = 548   # ~18 mesi
SOGLIA_ASSOLUTA = 913      # ~30 mesi
CAP = 60                   # max voci nel report

RE_DATE = re.compile(r'^date:\s*"?(\d{4}-\d{2}-\d{2})', re.M)
RE_TITLE = re.compile(r'^title:\s*"?(.*?)"?\s*$', re.M)
RE_ARCH = re.compile(r'^archiviato:\s*true', re.M)
# telefono reale (fisso 0.. o mobile 3.. con molte cifre, o +39) — NON i numeri brevi di emergenza
RE_TEL = re.compile(r'(\+39[\s.]?\d{6,})|(\b0\d{1,3}[\s./]?\d[\d\s./]{5,}\d)')
# citazioni normative forti (una norma specifica che può cambiare/essere abrogata)
RE_NORMA = re.compile(r'(D\.?\s?Lgs\.?|D\.?P\.?C\.?M\.?|DPCM|D\.?\s?M\.?\s?\d|L\.R\.|Legge\s+(n\.?\s?)?\d|Direttiva\s|Ordinanza\s|Decreto\s+(legge|del|n))', re.I)
RE_EXT = re.compile(r'https?://(?!www\.protezionecivilegenzano\.it)')


def split_frontmatter(testo):
    if testo.startswith("---"):
        parti = testo.split("---", 2)
        if len(parti) >= 3:
            return parti[1], parti[2]
    return testo, testo


def mesi(giorni):
    return round(giorni / 30.4)


def main():
    voci = []
    for path in sorted(glob.glob(os.path.join(DIR, "*.md"))):
        if path.endswith("-facile.md"):
            continue
        try:
            testo = open(path, encoding="utf-8").read()
        except Exception:
            continue
        fm, corpo = split_frontmatter(testo)
        if RE_ARCH.search(fm):
            continue
        m = RE_DATE.search(fm)
        if not m:
            continue
        try:
            d = datetime.date.fromisoformat(m.group(1))
        except ValueError:
            continue
        eta = (OGGI - d).days
        if eta < SOGLIA_CON_SEGNALI:
            continue
        segnali = []
        if RE_TEL.search(corpo):
            segnali.append("telefono")
        if RE_NORMA.search(corpo):
            segnali.append("norma citata")
        if RE_EXT.search(corpo):
            segnali.append("link esterno")
        if eta >= SOGLIA_ASSOLUTA or segnali:
            tit = RE_TITLE.search(fm)
            voci.append({
                "slug": os.path.basename(path)[:-3],
                "data": m.group(1),
                "mesi": mesi(eta),
                "titolo": tit.group(1) if tit else "",
                "segnali": segnali or ["molto vecchio"],
            })

    voci.sort(key=lambda v: v["data"])  # più vecchi prima
    n = len(voci)

    print(f"# Freschezza dei contenuti — {OGGI.isoformat()}\n")
    if n == 0:
        print("Nessun articolo da riverificare per anzianità. ✅\n")
        print("_Controllo automatico `scripts/check-freshness.py`: segnala articoli con "
              "più di 18 mesi che citano telefoni, norme o link esterni (informazioni che "
              "invecchiano). Oggi nessuno supera le soglie._")
        return 0

    print(f"Trovati **{n} articoli** da riverificare (più di 18 mesi e con informazioni "
          f"che invecchiano, oppure più di 30 mesi).\n")
    print("| Articolo | Pubblicato | Età | Da ricontrollare |")
    print("|---|---|---|---|")
    for v in voci[:CAP]:
        print(f"| **`{v['slug']}`**<br>{v['titolo']} | {v['data']} | ~{v['mesi']} mesi | {', '.join(v['segnali'])} |")
    if n > CAP:
        print(f"\n…e altri {n - CAP} (mostrati i {CAP} più vecchi).")
    print("\n## Come procedere\n")
    print("Per ciascun articolo verifica che **telefoni, norme citate e link** siano ancora "
          "validi; aggiorna o archivia. Per un audit guidato invoca l'agent "
          "`pc-content-freshness` sulla lista qui sopra (norme → anche `pc-normative-verifier`).\n")
    print("_Issue generata da `controllo-freschezza.yml`. Si aggiorna ogni lunedì 11:07 UTC. "
          "Segnalazione ad alta precisione: la decisione finale è editoriale._")
    return n


if __name__ == "__main__":
    sys.exit(min(main(), 250))
