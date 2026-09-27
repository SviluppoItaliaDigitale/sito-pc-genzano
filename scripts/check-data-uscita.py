#!/usr/bin/env python3
"""Controlla che la data di uscita di un articolo sia coerente con la data che annuncia.

Nasce il 28/09/2026. Un articolo programmato per il 28 settembre titolava
«15 ottobre: si chiude la stagione di grave pericolosità AIB»: uscito diciassette
giorni prima del fatto, diceva al cittadino che i divieti antincendio finivano
adesso. Il testo era stato corretto una settimana prima (la data vera era il
15 ottobre, non il 30 settembre), ma la data di uscita era rimasta quella vecchia.

Regola: se il titolo, la descrizione o il primo paragrafo legano una data a un
verbo che racconta il fatto COME PRESENTE («si chiude», «termina», «scade»,
«inizia», «scatta», «entra in vigore», «oggi»…), quella data deve cadere entro
TOLLERANZA giorni dalla data di uscita. Le forme che guardano avanti («fino al»,
«entro il», «dal … al», «si chiuderà») non fanno scattare il controllo, e nemmeno
le date con un anno diverso da quello di uscita (anniversari, fatti storici).

Uso:
  python3 scripts/check-data-uscita.py                 # articoli programmati (data futura)
  python3 scripts/check-data-uscita.py --tutti         # tutto l'archivio
  python3 scripts/check-data-uscita.py --giorni 7      # solo quelli in uscita entro 7 giorni
  python3 scripts/check-data-uscita.py FILE [FILE...]  # file indicati (usato da validate-pr)
Solo stdlib. Exit code = numero di articoli segnalati (0 = nessuno).
Un falso positivo si esclude con `controllo_data_uscita: false` nel frontmatter,
scrivendo il motivo in un commento YAML sulla riga sopra.
"""
import datetime
import glob
import os
import re
import sys
from zoneinfo import ZoneInfo

DIR = "content/comunicazioni"
OGGI = datetime.datetime.now(ZoneInfo("Europe/Rome")).date()
TOLLERANZA = 2  # giorni fra la data annunciata e la data di uscita

MESI = {m: i + 1 for i, m in enumerate(
    "gennaio febbraio marzo aprile maggio giugno luglio agosto "
    "settembre ottobre novembre dicembre".split())}
RE_DATA = re.compile(
    r"\b(\d{1,2}|1°|primo)\s+(" + "|".join(MESI) + r")(?:\s+(\d{4}))?\b", re.I)

# Verbi che raccontano il fatto come se accadesse nel giorno di lettura.
PRESENTE = re.compile(
    r"\b(si\s+chiude|chiude|chiudono|si\s+conclude|termina|terminano|finisce|"
    r"finiscono|scade|scadono|cessa|cessano|si\s+apre|apre|aprono|inizia|"
    r"iniziano|comincia|cominciano|parte|partono|scatta|scattano|"
    r"entra\s+in\s+vigore|entrano\s+in\s+vigore|è\s+in\s+corso|oggi|stasera|"
    r"stanotte|domani)\b", re.I)
# Forme che guardano avanti: una data introdotta così è una scadenza futura legittima.
PROSPETTICO = re.compile(
    r"(\b(fino\s+al|fino\s+a|entro\s+il|entro|dal|dall'|al|all'|tra\s+il|fra\s+il|"
    r"e\s+il|intorno\s+al|verso\s+il)\s*|\d\s*[-–]\s*)$", re.I)

RE_FM = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.S)


def campo(fm, nome):
    m = re.search(rf"^{nome}:\s*(.*)$", fm, re.M)
    return m.group(1).strip().strip('"').strip("'") if m else ""


def primo_paragrafo(corpo):
    for blocco in re.split(r"\n\s*\n", corpo.strip()):
        b = blocco.strip()
        if b and not b.startswith(("#", "{{", "<", "!", ">", "|")):
            return b
    return ""


def data_da(match, uscita):
    g_raw, mese, anno = match.group(1), match.group(2).lower(), match.group(3)
    giorno = 1 if g_raw.lower() in ("1°", "primo") else int(g_raw)
    if anno and int(anno) != uscita.year:
        return None  # anniversario o fatto di un altro anno
    candidati = []
    for a in ([uscita.year] if anno else [uscita.year - 1, uscita.year, uscita.year + 1]):
        try:
            candidati.append(datetime.date(a, MESI[mese], giorno))
        except ValueError:
            pass
    return min(candidati, key=lambda d: abs((d - uscita).days)) if candidati else None


def problemi(testo, uscita, dove):
    """Date raccontate al presente ma lontane dalla data di uscita."""
    trovati = []
    testo = re.sub(r"[*_`]|\[([^\]]*)\]\([^)]*\)", lambda m: m.group(1) or "", testo)
    for frase in re.split(r"(?<=[.!?])\s+|\n", testo):
        if not PRESENTE.search(frase):
            continue
        for m in RE_DATA.finditer(frase):
            if PROSPETTICO.search(frase[:m.start()]):
                continue
            d = data_da(m, uscita)
            if d is None:
                continue
            scarto = (d - uscita).days
            if abs(scarto) > TOLLERANZA:
                verso = "dopo" if scarto > 0 else "prima"
                trovati.append(f"{dove}: «{m.group(0)}» cade {abs(scarto)} giorni {verso} "
                               f"l'uscita ({uscita:%d/%m/%Y}) ma è raccontato al presente: "
                               f"«{frase.strip()[:140]}»")
    return trovati


def controlla(percorso):
    testo = open(percorso, encoding="utf-8").read()
    m = RE_FM.match(testo)
    if not m:
        return []
    fm, corpo = m.groups()
    if re.search(r"^controllo_data_uscita:\s*false", fm, re.M):
        return []
    if re.search(r"^archiviato:\s*true", fm, re.M):
        return []
    d = re.match(r"(\d{4})-(\d{2})-(\d{2})", campo(fm, "date"))
    if not d:
        return []
    uscita = datetime.date(*map(int, d.groups()))
    return (problemi(campo(fm, "title"), uscita, "titolo")
            + problemi(campo(fm, "description"), uscita, "descrizione")
            + problemi(primo_paragrafo(corpo), uscita, "primo paragrafo"))


def uscita_di(percorso):
    m = re.search(r"^date:\s*\"?(\d{4})-(\d{2})-(\d{2})",
                  open(percorso, encoding="utf-8").read(), re.M)
    return datetime.date(*map(int, m.groups())) if m else None


def main():
    args = sys.argv[1:]
    giorni = None
    if "--giorni" in args:
        i = args.index("--giorni")
        giorni = int(args[i + 1])
        del args[i:i + 2]
    tutti = "--tutti" in args
    args = [a for a in args if a != "--tutti"]

    if args:
        files = [f for f in args if f.startswith(DIR) and f.endswith(".md") and os.path.exists(f)]
    else:
        files = sorted(glob.glob(f"{DIR}/*.md"))
        if not tutti:
            files = [f for f in files if (u := uscita_di(f)) and u >= OGGI
                     and (giorni is None or (u - OGGI).days <= giorni)]
    files = [f for f in files if not f.endswith("-facile.md") and not f.endswith("_index.md")]

    segnalati = 0
    for f in files:
        esiti = controlla(f)
        if esiti:
            segnalati += 1
            print(f"✗ {f}")
            for e in esiti:
                print(f"    {e}")
    if segnalati:
        print(f"\n{segnalati} articoli con la data di uscita incoerente con la data annunciata.")
        print("Sposta la data di uscita (date:) vicino al fatto, oppure riscrivi il titolo "
              "al futuro («si chiuderà il…», «fino al…»). Agente: pc-calendario-editoriale.")
    else:
        print(f"OK: {len(files)} articoli controllati, date di uscita coerenti.")
    return segnalati


if __name__ == "__main__":
    sys.exit(min(main(), 125))
