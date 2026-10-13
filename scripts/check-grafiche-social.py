#!/usr/bin/env python3
"""Controlla che i testi delle grafiche di un articolo escano INTERI.

Con lo stesso codice che disegna le immagini (scripts/genera-immagini-social.py)
impagina, senza scrivere nulla: il titolo della prima slide, social_citazione,
social_punti (anche su più slide), titolo e description della storia e il
limite di 10 slide di Instagram; poi il titolo della cover del sito
(scripts/genera-cover.py). Verifica anche che il font sappia disegnare ogni
carattere: quelli che mancano (→ ≥ ≤ ≈, le emoji) uscirebbero come spazi vuoti.

Nato il 13/10/2026: il post sul soccorso alpino è uscito su Instagram e Facebook
con tre punti su quattro tagliati a metà frase, e guardando le immagini dei
post già usciti se ne sono trovati altri otto con lo stesso difetto dal
20/09/2026. Il generatore ora non taglia più, e se il testo non entra si ferma
e toglie anche le immagini vecchie dell'articolo: questo script
fa vedere il problema sulla pull request, prima che l'articolo vada online
senza il suo post.

Uso:
  python3 scripts/check-grafiche-social.py content/comunicazioni/<file>.md ...
  python3 scripts/check-grafiche-social.py --tutti          # tutti gli articoli
  python3 scripts/check-grafiche-social.py --da-git BASE    # toccati rispetto a BASE
Uscita: numero di articoli con errori (0 = tutti i testi escono interi).
"""

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENUTI = ROOT / "content" / "comunicazioni"


def _carica(nome: str, file: str):
    spec = importlib.util.spec_from_file_location(nome, ROOT / "scripts" / file)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


G = _carica("genera_immagini_social", "genera-immagini-social.py")
COVER = _carica("genera_cover", "genera-cover.py")
COVER_LARGHEZZA = COVER.W - 2 * 80      # margini laterali della cover
COVER_ALTEZZA = 372                     # spazio del titolo (fit_title, BOX_H)


def _testo(valore) -> str:
    return valore if isinstance(valore, str) else ""


def controlla_cover(titolo: str) -> list[str]:
    """Il titolo della cover del sito: intero, dentro i margini, disegnabile."""
    errori = []
    corpo, interlinea, righe = COVER.fit_title(titolo)
    if " ".join(righe).split() != titolo.split():
        errori.append("cover del sito: il titolo impaginato non coincide con l'originale")
    ft = COVER.font(True, corpo)
    for riga in righe:
        larghezza = ft.getlength(riga)
        if larghezza > COVER_LARGHEZZA:
            errori.append(f"cover del sito: la riga «{riga}» è larga {larghezza:.0f} px "
                          f"(massimo {COVER_LARGHEZZA})")
    if len(righe) * (corpo + interlinea) > COVER_ALTEZZA:
        errori.append(f"cover del sito: il titolo occupa {len(righe)} righe e supera lo spazio")
    if hasattr(ft, "getmask"):
        mancanti = G.caratteri_mancanti(titolo, ft)
        if mancanti:
            errori.append("cover del sito: caratteri che il font non disegna: "
                          + " ".join(f"«{c}»" for c in mancanti))
    return errori


def controlla(path: Path) -> tuple[list[str], list[str]]:
    """(errori, note) per un articolo."""
    testo = path.read_text(encoding="utf-8")
    fm, corpo = G.parse_frontmatter(testo)
    if fm.get("versione_facile_di") or path.name.endswith("-facile.md"):
        return [], ["versione facile: niente grafiche social"]
    titolo = _testo(fm.get("title"))
    badge = _testo(fm.get("badge"))
    descrizione = _testo(fm.get("description"))
    citazione = _testo(fm.get("social_citazione")).strip()
    punti = fm.get("social_punti") or []
    if not isinstance(punti, list):
        punti = []
    foto = G.estrai_foto_inline(corpo)
    art = {"title": titolo, "badge": badge, "description": descrizione,
           "citazione": citazione, "punti": [str(p).strip() for p in punti if str(p).strip()],
           "carousel": [None] + foto}

    errori, note = [], []
    prove = [
        ("prima slide", lambda: G.piano_titolo(titolo, badge)),
        ("storia", lambda: G.piano_storia_completo(titolo, descrizione, badge, bool(foto))),
    ]
    if citazione:
        prove.append(("citazione", lambda: G.piano_citazione(citazione)))
    prove.append(("carosello", lambda: G.piano_carosello(art)))
    esiti = {}
    for nome, prova in prove:
        try:
            esiti[nome] = prova()
        except G.TestoIncompleto as e:
            errori.append(str(e))
    errori.extend(controlla_cover(titolo))

    # Note: che cosa cambia rispetto ai corpi pieni (utile a chi scrive).
    piano = esiti.get("carosello") or []
    sintesi = [d for k, d in piano if k == "punti"]
    if sintesi:
        corpo_punti = sintesi[0][1]
        if len(sintesi) > 1:
            note.append(f"sintesi su {len(sintesi)} slide (corpo {corpo_punti} px)")
        elif corpo_punti < G.PUNTI_CORPO[0]:
            note.append(f"sintesi ridotta a corpo {corpo_punti} px per entrare in una slide")
    storia = esiti.get("storia")
    if storia:
        if foto and not storia["con_foto"]:
            note.append("storia senza la foto in evidenza, per far entrare il testo")
        if storia["descrizione_tolta"]:
            note.append("storia senza descrizione: troppo lunga anche senza foto")
    return errori, note


def file_da_git(base: str) -> list[Path]:
    uscita = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=AM", f"{base}...HEAD", "--",
         "content/comunicazioni/"],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return [ROOT / r for r in uscita.split() if r.endswith(".md")
            and not r.endswith("/_index.md")]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", nargs="*", type=Path)
    ap.add_argument("--tutti", action="store_true", help="tutti gli articoli")
    ap.add_argument("--da-git", metavar="BASE", help="articoli toccati rispetto a BASE")
    ap.add_argument("--note", action="store_true", help="mostra anche le note")
    args = ap.parse_args()

    if args.tutti:
        articoli = sorted(p for p in CONTENUTI.glob("*.md") if p.name != "_index.md")
    elif args.da_git:
        articoli = file_da_git(args.da_git)
    else:
        articoli = [p if p.is_absolute() else Path.cwd() / p for p in args.file]
    if not articoli:
        print("Nessun articolo da controllare.")
        return 0

    con_errori = 0
    for path in articoli:
        if not path.exists():
            continue
        errori, note = controlla(path)
        nome = path.name
        if errori:
            con_errori += 1
            print(f"✗ {nome}")
            for e in errori:
                print(f"    - {e}")
                print(f"::error file=content/comunicazioni/{nome}::{e}")
        elif args.note and note:
            print(f"✓ {nome} — " + "; ".join(note))
    print(f"\n{len(articoli)} articoli controllati, {con_errori} con testi che non "
          f"uscirebbero interi nelle grafiche.")
    return con_errori


if __name__ == "__main__":
    sys.exit(min(main(), 125))
