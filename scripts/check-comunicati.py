#!/usr/bin/env python3
"""Controlla i comunicati stampa in content/sala-stampa/comunicati/ (bloccante in validate-pr.yml).
Front matter completo, PDF presente e allineato al testo, articolo collegato esistente, citazioni approvate, nessun nome di strumenti.

Uso:
  python3 scripts/check-comunicati.py            # tutti i comunicati
  python3 scripts/check-comunicati.py FILE.md    # solo quelli indicati
  python3 scripts/check-comunicati.py --candidati [--giorni 2]
      # articoli online negli ultimi N giorni che la routine «Comunicati stampa
      # automatici» deve valutare, con il motivo di ogni esclusione
      # (agente pc-ufficio-stampa, punto 8)

Controlli, per ogni comunicato (file .md diverso da _index.md):
  1. front matter: title (al massimo 110 caratteri, perché i siti di notizie
     tagliano i titoli lunghi), sottotitolo, description, date AAAA-MM-GG,
     pdf (percorso dentro static/, cartella /comunicati/AAAA/);
  2. il PDF esiste e contiene ogni paragrafo del testo del comunicato
     (confronto senza spazi: un PDF non rigenerato dopo una correzione del
     testo blocca la PR; si rigenera con scripts/genera-comunicati-pdf.py);
  3. `articolo:` (se c'è) porta a un articolo esistente in content/comunicazioni/;
  4. citazioni: se il testo contiene una citazione fra « » di almeno otto
     parole, il front matter deve avere `citazioni_approvate: true`. Lo si
     scrive solo quando le parole vengono da un testo approvato da chi parla
     (comunicato già diffuso, articolo pubblicato, testo confermato): mai per
     citazioni scritte da chi prepara il comunicato;
  5. nessun nome di strumenti di intelligenza artificiale nel testo, nel front
     matter e nei metadati del PDF (CLAUDE.md, «Nessun riferimento all'IA»).

Esce con 1 se un controllo non passa. Dipendenze: PyYAML e pypdf (oppure PyMuPDF).
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

import yaml

RADICE = Path(__file__).resolve().parent.parent
CARTELLA = RADICE / "content" / "sala-stampa" / "comunicati"
STRUMENTI = re.compile(
    r"\b(claude|chatgpt|codex|gemini|openai|anthropic|copilot|intelligenza artificiale|"
    r"artificial intelligence|elevenlabs|midjourney)\b", re.I)
CITAZIONE = re.compile(r"«([^»]+)»")


def leggi(percorso: Path) -> tuple[dict, str]:
    testo = percorso.read_text(encoding="utf-8")
    if not testo.startswith("---"):
        raise ValueError("manca il front matter")
    _, fm, corpo = testo.split("---", 2)
    return yaml.safe_load(fm) or {}, corpo


def paragrafi(corpo: str) -> list[str]:
    """Paragrafi del comunicato come compaiono a stampa (senza shortcode e attributi)."""
    out = []
    for p in corpo.split("\n\n"):
        p = p.strip()
        if not p or p.startswith("{{<"):
            continue
        p = re.sub(r"\n\{\.[^}]+\}\s*$", "", p)          # {.cs-evidenza}
        p = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", p)    # link: resta il testo
        p = p.replace("**", "").replace("__", "")
        p = re.sub(r"(?<!\w)[*_]([^*_]+)[*_](?!\w)", r"\1", p)
        out.append(p.strip())
    return out


def compatto(testo: str) -> str:
    """Testo senza spazi e con apostrofi e virgolette uniformi, per il confronto con il PDF."""
    t = unicodedata.normalize("NFKC", testo)
    t = t.replace("­", "").replace("’", "'").replace("‘", "'")
    t = t.replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", "", t)


def testo_pdf(file: Path) -> tuple[str, dict]:
    try:
        from pypdf import PdfReader
        r = PdfReader(str(file))
        testo = "\n".join((pg.extract_text() or "") for pg in r.pages)
        meta = {k.lstrip("/"): str(v) for k, v in (r.metadata or {}).items()}
        return testo, meta
    except ImportError:
        import fitz  # PyMuPDF
        doc = fitz.open(str(file))
        return "\n".join(pg.get_text() for pg in doc), {k: str(v) for k, v in (doc.metadata or {}).items()}


def controlla(percorso: Path) -> list[str]:
    errori: list[str] = []
    try:
        fm, corpo = leggi(percorso)
    except (ValueError, yaml.YAMLError) as e:
        return [f"front matter illeggibile: {e}"]

    titolo = str(fm.get("title") or "")
    for campo in ("title", "sottotitolo", "description", "date", "pdf"):
        if not fm.get(campo):
            errori.append(f"manca `{campo}` nel front matter")
    if len(titolo) > 110:
        errori.append(f"titolo di {len(titolo)} caratteri: al massimo 110")
    data = str(fm.get("date") or "")
    if data and not re.fullmatch(r"\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}\+0[12]:00)?", data):
        errori.append(f"data `{data}` non nel formato AAAA-MM-GG")

    pdf = str(fm.get("pdf") or "")
    if pdf:
        if not re.fullmatch(r"/comunicati/\d{4}/[a-z0-9-]+\.pdf", pdf):
            errori.append(f"`pdf: {pdf}`: va in /comunicati/AAAA/<slug>.pdf")
        file = RADICE / "static" / pdf.lstrip("/")
        if not file.is_file():
            errori.append(f"PDF mancante: static{pdf} (genera con scripts/genera-comunicati-pdf.py)")
        else:
            testo, meta = testo_pdf(file)
            nel_pdf = compatto(testo)
            for p in paragrafi(corpo):
                if compatto(p) not in nel_pdf:
                    errori.append("il PDF non contiene questo paragrafo (rigeneralo con "
                                  f"scripts/genera-comunicati-pdf.py): «{p[:90]}…»")
            if compatto(titolo) not in nel_pdf:
                errori.append("il PDF non contiene il titolo del comunicato")
            for chiave, valore in meta.items():
                if STRUMENTI.search(valore):
                    errori.append(f"metadato del PDF con il nome di uno strumento: {chiave} = {valore}")

    articolo = str(fm.get("articolo") or "")
    if articolo:
        slug = articolo.strip("/").split("/")[-1]
        if not articolo.startswith("/comunicazioni/") or not (RADICE / "content" / "comunicazioni" / f"{slug}.md").is_file():
            errori.append(f"`articolo: {articolo}` non porta a un articolo di content/comunicazioni/")

    lunghe = [c for c in CITAZIONE.findall(corpo) if len(c.split()) >= 8]
    if lunghe and fm.get("citazioni_approvate") is not True:
        errori.append("citazioni fra « » senza `citazioni_approvate: true`: si pubblicano solo parole "
                      f"approvate da chi parla (prima: «{lunghe[0][:70]}…»)")

    tutto = percorso.read_text(encoding="utf-8")
    m = STRUMENTI.search(tutto)
    if m:
        errori.append(f"nome di uno strumento nel comunicato: «{m.group(0)}»")
    return errori


def candidati(giorni: float) -> int:
    """Elenca gli articoli online negli ultimi `giorni` giorni da valutare per un comunicato.

    Esclude in modo deterministico ciò che il punto 8 dell'agente pc-ufficio-stampa
    esclude sempre: versioni facili e bozze (le scarta social_comune.articoli),
    articoli archiviati, badge Allerta ed Emergenza (si comunicano a mano, d'intesa
    con il Comune), articoli che hanno già un comunicato (campo `articolo:`).
    Il giudizio sul resto (notizia per le testate o no) resta a chi legge l'articolo.
    """
    sys.path.insert(0, str(RADICE / "scripts"))
    import social_comune as sc  # stesse regole di «articolo online» dei social

    gia: dict[str, str] = {}
    for p in CARTELLA.glob("*.md"):
        if p.name == "_index.md":
            continue
        try:
            fm, _ = leggi(p)
        except (ValueError, yaml.YAMLError):
            continue
        slug = str(fm.get("articolo") or "").strip("/").split("/")[-1]
        if slug:
            gia[slug] = p.stem

    magazine = {"Informazione", "Prevenzione", "Formazione"}  # canale-articolo.html
    righe = sc.articoli(finestra_ore=giorni * 24)
    print(f"Articoli online nelle ultime {giorni:g}×24 ore: {len(righe)}\n")
    da_valutare = 0
    for p, fm, d in righe:
        badge = sc.testo_campo(fm, "badge") or "?"
        canale = sc.testo_campo(fm, "canale") or ("approfondimenti" if badge in magazine else "gruppo")
        titolo = sc.testo_campo(fm, "title")
        if sc.testo_campo(fm, "archiviato").lower() == "true":
            motivo = "archiviato"
        elif badge in ("Allerta", "Emergenza"):
            motivo = f"badge {badge}: si comunica a mano, d'intesa con il Comune"
        elif p.stem in gia:
            motivo = f"ha già il comunicato {gia[p.stem]}"
        else:
            motivo = ""
        if motivo:
            print(f"– escluso  {sc.fmt(d)}  [{badge}]  {titolo}\n           {p.relative_to(RADICE)} ({motivo})")
        else:
            da_valutare += 1
            print(f"✓ valutare {sc.fmt(d)}  [{badge}, canale {canale}]  {titolo}\n           {p.relative_to(RADICE)}")
    print(f"\nDa valutare: {da_valutare}. Merita un comunicato solo una notizia per le testate "
          "(punto 8 di .claude/agents/pc-ufficio-stampa.md); al massimo uno per giro.")
    return 0


def main(argv: list[str]) -> int:
    if argv and argv[0] == "--candidati":
        giorni = 2.0
        if "--giorni" in argv:
            try:
                giorni = float(argv[argv.index("--giorni") + 1])
            except (IndexError, ValueError):
                print("--giorni vuole un numero, per esempio --giorni 2")
                return 2
        return candidati(giorni)
    if argv:
        file = [Path(a) for a in argv]
    else:
        file = sorted(p for p in CARTELLA.glob("*.md") if p.name != "_index.md")
    file = [f if f.is_absolute() else (Path.cwd() / f) for f in file]
    file = [f for f in file if f.name != "_index.md" and f.suffix == ".md"]
    if not file:
        print("Nessun comunicato da controllare.")
        return 0
    totale = 0
    for f in file:
        errori = controlla(f)
        nome = f.relative_to(RADICE) if f.is_relative_to(RADICE) else f
        if errori:
            totale += len(errori)
            print(f"✗ {nome}")
            for e in errori:
                print(f"   - {e}")
        else:
            print(f"✓ {nome}")
    if totale:
        print(f"\n{totale} problemi nei comunicati stampa.")
        return 1
    print(f"\nComunicati stampa a posto: {len(file)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
