#!/usr/bin/env python3
"""Controlla che ogni articolo di content/comunicazioni/ dichiari il suo canale.

Dal 19/11/2026 l'archivio e la homepage dividono gli articoli in tre canali:
territorio (Genzano e Castelli Romani), italia (Dall'Italia e dalla Regione)
e approfondimenti. Il canale si sceglie leggendo l'articolo e si scrive nel
frontmatter (`canale:`), perché il solo badge sbagliava. Le versioni facili
(-facile.md) non stanno nelle liste e sono escluse.

Uso: python3 scripts/check-canale-articoli.py [FILE ...]
Senza argomenti controlla tutti gli articoli. Esce con 1 se ne trova uno
senza canale o con un valore non ammesso.
"""
import pathlib
import re
import sys

AMMESSI = {"territorio", "italia", "approfondimenti"}
RADICE = pathlib.Path(__file__).resolve().parent.parent / "content" / "comunicazioni"


def canale(testo: str):
    if not testo.startswith("---"):
        return None
    fine = testo.find("\n---", 3)
    fm = testo[3:fine] if fine > 0 else ""
    m = re.search(r'^canale:\s*["\']?([^"\'\s#]+)', fm, re.M)
    return m.group(1).strip().lower() if m else None


def main(argv):
    if argv:
        file = [pathlib.Path(a) for a in argv]
    else:
        file = sorted(RADICE.glob("*.md"))
    errori = []
    for f in file:
        if f.name == "_index.md" or f.name.endswith("-facile.md"):
            continue
        if f.parent.name != "comunicazioni" or not f.exists():
            continue
        v = canale(f.read_text(encoding="utf-8"))
        if v is None:
            errori.append(f"{f}: manca «canale:» (territorio, italia o approfondimenti)")
        elif v not in AMMESSI:
            errori.append(f"{f}: canale «{v}» non ammesso (territorio, italia o approfondimenti)")
    for e in errori:
        print(e)
    if errori:
        print(f"\n{len(errori)} articoli senza canale valido. Scegli leggendo l'articolo:\n"
              "  territorio      = Genzano e Castelli Romani (interventi, vita del Gruppo, atti del Comune, eventi in città)\n"
              "  italia          = notizie nazionali e regionali di protezione civile (decreti, stati di emergenza, Regione)\n"
              "  approfondimenti = storia, anniversari, scienza, prevenzione")
        return 1
    print("Canale presente e valido in tutti gli articoli controllati.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
