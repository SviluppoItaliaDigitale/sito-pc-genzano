#!/usr/bin/env python3
"""
Cerca le incongruenze fra i testi del sito: lo stesso dato con valori diversi.

Il registro data/dati_canonici.yaml (check-dati-canonici.py) blocca le varianti
già note. Questo script serve a SCOPRIRE quelle che nessuno ha ancora
registrato: per ogni famiglia di dati che si ripetono (ore del caldo, litri
d'acqua a persona, giorni di autonomia del kit, compressioni al minuto, numeri
dei recapiti…) raccoglie tutti i valori scritti nei testi del sito, compresi
quelli dentro il codice, e segnala le famiglie che ne hanno più di uno.

Non decide quale valore è giusto: elenca i valori, quanti file usano
ciascuno e dove. Il giudizio spetta all'agente pc-coerenza-trasversale, che
allinea alla fonte canonica e poi aggiunge la voce al registro.

Nasce il 17/10/2026: l'orario del caldo compariva come 11-18 nella pagina
canonica e come 11-17 in 19 file (articoli, kit, giochi, libro pop-up,
messaggi Telegram), e nessun controllo lo vedeva perché il dato non era nel
registro. Lo ha trovato un audit esterno.

Modalità «pubblicazione» (dal 17/10/2026, su richiesta dell'utente: ogni
dato pubblicato va confrontato con quello già presente sul sito):
  python3 scripts/cerca-incongruenze.py --da-git origin/main
confronta soltanto i valori sulle righe AGGIUNTE rispetto a quel ramo
(commit e modifiche non ancora committate) con i valori della stessa
famiglia scritti nel resto del sito. Se un valore nuovo è diverso da uno già
presente, esce con errore: o si corregge il nuovo, o si allineano anche le
altre pagine. È bloccante in validate-pr.yml; i gate degli articoli e dei
materiali lo eseguono prima del commit.

Uso:
  python3 scripts/cerca-incongruenze.py                  # rapporto testuale
  python3 scripts/cerca-incongruenze.py --markdown F.md  # rapporto per la issue
  python3 scripts/cerca-incongruenze.py --famiglia ore-caldo
Exit code = numero di famiglie con più valori (0 = tutto coerente).
Solo Python standard.

Aggiungere una famiglia: una voce in FAMIGLIE con un'espressione regolare che
cattura il valore (gruppi), un contesto che deve stare nella stessa frase e,
se serve, i valori legittimamente diversi in "ammessi" con il motivo.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from fnmatch import fnmatch
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PERIMETRO = [
    ("content", "*.md"),
    ("data", "*.yaml"),
    ("static", "*.html"),
    ("static", "*.js"),
    ("themes/flavour-pcgenzano/layouts", "*.html"),
    ("themes/flavour-pcgenzano/static/js", "*.js"),
    ("scripts", "*.py"),
]
ESCLUSI = [
    "data/dati_canonici.yaml",
    "data/video_*.yaml",
    "data/audit-pdf.yaml",
    "static/vendor/*",
    "static/pagefind/*",
    "static/open-data/*",
    "static/open-kit/*",
    "static/formazione/schede-stampabili/pacchetti/*",
    "themes/flavour-pcgenzano/static/vendor/*",
    "scripts/cerca-incongruenze.py",
    "scripts/check-dati-canonici.py",
    # Articoli del 2025 e anniversari raccontano altri anni: i loro dati
    # possono essere legittimamente diversi.
    "content/comunicazioni/2025-*",
]

# Ogni famiglia: id, descrizione, regex (gruppi = valore), contesto nella
# stessa frase, funzione di normalizzazione, valori ammessi con motivo.
FAMIGLIE = [
    {
        "id": "ore-caldo",
        "dato": "Ore più calde da evitare",
        "regex": r"(?<![\d/-])\b(1[0-2])(?:[.:]00)?\s*(?:[-–]|alle|e\s+le)\s*(1[5-9])(?:[.:]00)?\b(?![\d/-]|\s*(?:min|km|cm|°|anni|gradi))",
        "contesto": r"[Cc]ald|[Ss]ole|calore|ombra|fresc|ore centrali",
        "norm": lambda g: f"{int(g[0])}-{int(g[1])}",
        "salvo_se": r"turn[io]|avvistament|fasce di",
    },
    {
        "id": "acqua-persona-giorno",
        "dato": "Litri d'acqua a persona al giorno nella scorta",
        "regex": r"\b(\d+(?:[,.]\d+)?)\s*(?:litri|l)\b[^.\n]{0,40}?\b(?:a|per)\s+(?:persona|testa)",
        "contesto": r"giorno|al dì|quotidian",
        "norm": lambda g: g[0].replace(".", ","),
        # Bere (1,5-2 litri) non è la scorta (circa 4 litri con l'igiene).
        "salvo_se": r"\bbev|\bbere\b|idrat|per\s+3\s+giorni|in tutto|totale",
        "ammessi": {"3,8": "riferimento Ready.gov citato come fonte del «circa 4 litri»"},
    },
    {
        "id": "autonomia-kit",
        "dato": "Ore o giorni di autonomia del kit di casa",
        "regex": r"\b(\d{2})\s*ore\b",
        "contesto": r"\bkit\b(?! [Ss]cuola)|scorta",
        "norm": lambda g: f"{g[0]} ore",
        "salvo_se": r"preavviso|validit|bollettin|allert|previsio|entro|dopo|\bh24|ogni|squadr|colonn|UdA|volontar",
    },
    {
        "id": "rcp-frequenza",
        "dato": "Compressioni toraciche al minuto",
        "regex": r"\b(\d{2,3})\s*[-–]\s*(\d{2,3})\s*(?:compressioni\s+)?(?:al|per)\s+minuto",
        "contesto": r"compressi|massaggio|RCP|rianimaz",
        "norm": lambda g: f"{g[0]}-{g[1]}",
    },
    {
        "id": "rcp-profondita",
        "dato": "Profondità delle compressioni nell'adulto",
        "regex": r"\b(\d)\s*[-–]\s*(\d)\s*cm\b",
        "contesto": r"compressi|massaggio|torace|sterno",
        "norm": lambda g: f"{g[0]}-{g[1]} cm",
        "salvo_se": r"bambin|lattant|neonat|infan",
    },
    {
        "id": "rcp-rapporto",
        "dato": "Rapporto compressioni : ventilazioni",
        "regex": r"\b(\d{1,2})\s*:\s*(\d)\b",
        "contesto": r"compressi|insuffla|ventila",
        "norm": lambda g: f"{g[0]}:{g[1]}",
        "salvo_se": r"bambin|lattant|neonat|due soccorritori",
        "ammessi": {"15:2": "rapporto pediatrico (IRC), diverso dall'adulto"},
    },
    {
        "id": "ustione-minuti",
        "dato": "Minuti di acqua corrente su un'ustione",
        "regex": r"\b(\d{1,2})(?:\s*[-–]\s*(\d{2}))?\s*min(?:uti)?\b",
        "contesto": r"[Uu]stion|[Ss]cottat",
        "norm": lambda g: g[0] + (f"-{g[1]}" if g[1] else ""),
        "salvo_se": r"chimic|attendi|aspetta|dura|occhi|cammino|primi \d+ minuti|<div|<a ",
    },
    {
        "id": "farmaci-giorni",
        "dato": "Giorni di farmaci abituali nella scorta",
        "regex": r"(?:[Ff]armac|[Mm]edicin|[Tt]erapi)\w*[^.\n<]{0,60}?\b(\d{1,2})(?:\s*[-–]\s*(\d{1,2}))?\s*giorni\b",
        "contesto": r".",
        "ammessi": {"7-14": "terapie salvavita (calcolatore della scorta)",
                    "7-10": "compatibile con «almeno 7 giorni»",
                    "14": "compatibile con «almeno 7 giorni»"},
        "norm": lambda g: g[0] + (f"-{g[1]}" if g[1] else ""),
        "salvo_se": r"scaden|ricett|dopo|entro|ricover|sintom|febbre|vaccin|ogni|cicl|chemio|dialisi",
    },
    {
        "id": "sala-operativa-lazio",
        "dato": "Numero della Sala Operativa della Protezione Civile del Lazio",
        "regex": r"\b(80\d)[\s.]?(\d{3})(?:[\s.]?(\d{3}))?\b",
        "contesto": r"Sala Operativa|SOUP|Protezione Civile (?:del )?Lazio|Regione",
        "norm": lambda g: "".join(x for x in g if x),
        "salvo_se": r"\b800[\s.]?\d",
    },
    {
        "id": "distanza-alberi-cavi",
        "dato": "Distanza da tenere da cavi elettrici caduti",
        "regex": r"\b(\d{1,2})\s*metri\b",
        "contesto": r"cav[oi] elettric|fili? elettric|linee? elettric",
        "norm": lambda g: f"{g[0]} m",
    },
]

FINE_FRASE = re.compile(r"(?<=[.!?;])\s|\n\s*\n|\n\s*[-*•|]|</li>|</p>|</t[dh]>|</?caption>|<tr>|\\n|',|\",")


def file_del_perimetro() -> list[Path]:
    out = []
    for cartella, schema in PERIMETRO:
        base = ROOT / cartella
        if base.is_dir():
            out.extend(base.rglob(schema))
    return sorted(set(out))


def frase_intorno(testo: str, inizio: int, fine: int) -> str:
    a = max(0, inizio - 300)
    b = min(len(testo), fine + 300)
    pezzo = testo[a:b]
    rel_i, rel_f = inizio - a, fine - a
    tagli = [m.end() for m in FINE_FRASE.finditer(pezzo, 0, rel_i)]
    s = tagli[-1] if tagli else 0
    m = FINE_FRASE.search(pezzo, rel_f)
    e = m.start() if m else len(pezzo)
    return pezzo[s:e]


def raccogli(famiglie):
    risultati = {f["id"]: defaultdict(list) for f in famiglie}
    compilati = [(f, re.compile(f["regex"], re.I), re.compile(f["contesto"]),
                  re.compile(f["salvo_se"], re.I) if f.get("salvo_se") else None)
                 for f in famiglie]
    for path in file_del_perimetro():
        rel = path.relative_to(ROOT).as_posix()
        if any(fnmatch(rel, e) for e in ESCLUSI):
            continue
        try:
            testo = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for fam, rx, ctx, salvo in compilati:
            for m in rx.finditer(testo):
                frase = frase_intorno(testo, m.start(), m.end())
                if not ctx.search(frase):
                    continue
                if salvo and salvo.search(frase):
                    continue
                valore = fam["norm"](m.groups())
                if valore in fam.get("ammessi", {}):
                    continue
                riga = testo.count("\n", 0, m.start()) + 1
                risultati[fam["id"]][valore].append(
                    (rel, riga, " ".join(frase.split())[:160]))
    return risultati


def righe_aggiunte(rif: str) -> dict[str, set[int]]:
    """File e numeri di riga aggiunti rispetto a rif (merge-base con HEAD)."""
    import subprocess
    try:
        base = subprocess.run(["git", "merge-base", rif, "HEAD"], cwd=ROOT,
                              capture_output=True, text=True, check=True).stdout.strip()
    except subprocess.CalledProcessError:
        base = rif
    diff = subprocess.run(["git", "diff", "-U0", "--no-color", base], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout
    # anche i file nuovi non ancora aggiunti all'indice
    nuovi = subprocess.run(["git", "ls-files", "--others", "--exclude-standard"],
                           cwd=ROOT, capture_output=True, text=True).stdout.split()
    out: dict[str, set[int]] = {}
    corrente = None
    for riga in diff.splitlines():
        if riga.startswith("+++ "):
            corrente = riga[6:] if riga.startswith("+++ b/") else None
        elif riga.startswith("@@") and corrente:
            m = re.search(r"\+(\d+)(?:,(\d+))?", riga)
            inizio, n = int(m.group(1)), int(m.group(2) or 1)
            out.setdefault(corrente, set()).update(range(inizio, inizio + n))
    for rel in nuovi:
        f = ROOT / rel
        if f.is_file():
            try:
                n = f.read_text(encoding="utf-8").count("\n") + 1
            except (UnicodeDecodeError, OSError):
                continue
            out[rel] = set(range(1, n + 1))
    return out


def controlla_pubblicazione(famiglie, risultati, aggiunte) -> int:
    problemi = 0
    for fam in famiglie:
        valori = risultati[fam["id"]]
        nuovi, gia = [], defaultdict(set)
        for valore, occ in valori.items():
            for rel, riga, frase in occ:
                if riga in aggiunte.get(rel, ()):
                    nuovi.append((valore, rel, riga, frase))
                else:
                    gia[valore].add(rel)
        for valore, rel, riga, frase in nuovi:
            altri = {v: f for v, f in gia.items() if v != valore}
            if not altri:
                continue
            problemi += 1
            elenco = "; ".join(f"«{v}» in {len(f)} file (es. {sorted(f)[0]})"
                               for v, f in sorted(altri.items(), key=lambda kv: -len(kv[1])))
            print(f"{rel}:{riga}: [{fam['id']}] nuovo valore «{valore}» per «{fam['dato']}», "
                  f"ma sul sito c'è già {elenco}.\n    {frase}")
    if problemi:
        print(f"\n{problemi} dato/i nuovi diversi da quelli già pubblicati. Verifica sulla fonte "
              "canonica: correggi il nuovo valore oppure allinea tutte le pagine "
              "(agente pc-coerenza-trasversale) e registra il dato in data/dati_canonici.yaml.")
    else:
        print("Dati nuovi coerenti con quelli già presenti sul sito.")
    return min(problemi, 255)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--famiglia", help="Solo questa famiglia")
    ap.add_argument("--markdown", help="Scrive il rapporto in Markdown in questo file")
    ap.add_argument("--da-git", metavar="RIF",
                    help="Confronta solo i dati sulle righe aggiunte rispetto a RIF con il resto del sito")
    args = ap.parse_args()

    famiglie = [f for f in FAMIGLIE if not args.famiglia or f["id"] == args.famiglia]
    risultati = raccogli(famiglie)
    if args.da_git:
        return controlla_pubblicazione(famiglie, risultati, righe_aggiunte(args.da_git))

    righe = []
    divergenti = 0
    for fam in famiglie:
        valori = risultati[fam["id"]]
        if len(valori) <= 1:
            continue
        divergenti += 1
        righe.append(f"### {fam['dato']} (`{fam['id']}`)\n")
        ordinati = sorted(valori.items(), key=lambda kv: -len({o[0] for o in kv[1]}))
        for valore, occ in ordinati:
            files = sorted({o[0] for o in occ})
            righe.append(f"- **{valore}**: {len(occ)} occorrenze in {len(files)} file")
            for rel, riga, frase in occ[:8]:
                righe.append(f"  - `{rel}:{riga}` — {frase}")
            if len(occ) > 8:
                righe.append(f"  - … e altre {len(occ) - 8}")
        righe.append("")

    if divergenti:
        testa = (f"{divergenti} famiglia/e di dati con valori diversi nel sito. "
                 "Il valore più frequente non è per forza quello giusto: si allinea "
                 "alla fonte canonica (agente pc-coerenza-trasversale) e si aggiunge "
                 "la voce a data/dati_canonici.yaml.\n")
    else:
        testa = f"Nessuna incongruenza nelle {len(famiglie)} famiglie controllate.\n"
    rapporto = testa + "\n" + "\n".join(righe)
    print(rapporto)
    if args.markdown:
        Path(args.markdown).write_text(rapporto, encoding="utf-8")
    return min(divergenti, 255)


if __name__ == "__main__":
    sys.exit(main())
