#!/usr/bin/env python3
"""Controlla i testi del «Libro che si esplora» (data/libro_3d*.yaml).

Verifica che la versione italiana, quella in italiano semplice e quella
inglese abbiano gli stessi capitoli nello stesso ordine, una sola risposta
giusta nella stessa posizione, la spiegazione per le risposte sbagliate,
la risposta breve entro 151 caratteri con la lettera giusta e le stesse
fonti; che ogni capitolo abbia la sua scena in static/js/libro-3d.js; con
--public, che ogni fonte porti a una pagina e a un'ancora della build.
Uso: python3 scripts/check-libro-3d.py [--public public]
"""
import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FILE = {
    "italiano": ROOT / "data/libro_3d.yaml",
    "italiano semplice": ROOT / "data/libro_3d_facile.yaml",
    "inglese": ROOT / "data/libro_3d_en.yaml",
}
JS = ROOT / "themes/flavour-pcgenzano/static/js/libro-3d.js"
CAMPI = ("chiave", "occhiello", "titolo", "intro", "domanda", "opzioni", "risposta", "breve", "fonti")
MAX_BREVE = 151  # spazio del riquadro della risposta breve sulla pagina 3D


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--public", help="cartella della build Hugo, per controllare fonti e ancore")
    args = ap.parse_args()
    errori = []
    dati = {}
    for nome, f in FILE.items():
        if not f.exists():
            errori.append(f"{f.relative_to(ROOT)}: file mancante")
            continue
        dati[nome] = yaml.safe_load(f.read_text(encoding="utf-8"))["capitoli"]

    base = dati.get("italiano") or []
    js = JS.read_text(encoding="utf-8")
    scene = set(re.findall(r"^\s+([a-z]+)\(\)\{", js[js.index("const BUILD"):], re.M))
    for c in base:
        if c.get("chiave") not in scene:
            errori.append(f"capitolo «{c.get('chiave')}»: nessuna scena con questo nome in libro-3d.js")

    for nome, caps in dati.items():
        if len(caps) != len(base):
            errori.append(f"{nome}: {len(caps)} capitoli invece di {len(base)}")
        for i, c in enumerate(caps):
            dove = f"{nome}, capitolo {i + 1}"
            for k in CAMPI:
                if not c.get(k):
                    errori.append(f"{dove}: manca «{k}»")
            if i >= len(base):
                continue
            b = base[i]
            if c.get("chiave") != b.get("chiave"):
                errori.append(f"{dove}: chiave «{c.get('chiave')}» invece di «{b.get('chiave')}»")
            giuste = [k for k, o in enumerate(c.get("opzioni") or []) if o.get("giusta")]
            giuste_b = [k for k, o in enumerate(b.get("opzioni") or []) if o.get("giusta")]
            if len(giuste) != 1:
                errori.append(f"{dove}: {len(giuste)} risposte giuste invece di una")
            elif giuste != giuste_b:
                errori.append(f"{dove}: la risposta giusta non è nella stessa posizione dell'italiano")
            if len(c.get("opzioni") or []) != len(b.get("opzioni") or []):
                errori.append(f"{dove}: numero di risposte diverso dall'italiano")
            for k, o in enumerate(c.get("opzioni") or []):
                if not o.get("giusta") and not o.get("perche"):
                    errori.append(f"{dove}: la risposta {'ABCD'[k]} è sbagliata ma non spiega perché")
            breve = c.get("breve") or ""
            if len(breve) > MAX_BREVE:
                errori.append(f"{dove}: risposta breve di {len(breve)} caratteri (massimo {MAX_BREVE})")
            if giuste and not breve.startswith("ABCD"[giuste[0]] + " "):
                errori.append(f"{dove}: la risposta breve non comincia con la lettera giusta ({'ABCD'[giuste[0]]})")
            if [f.get("url") for f in c.get("fonti") or []] != [f.get("url") for f in b.get("fonti") or []]:
                errori.append(f"{dove}: fonti diverse da quelle della versione italiana")

    if args.public:
        pub = Path(args.public)
        for i, c in enumerate(base):
            for f in c.get("fonti") or []:
                percorso, _, ancora = f["url"].partition("#")
                pagina = pub / percorso.strip("/") / "index.html"
                if not pagina.exists():
                    errori.append(f"capitolo {i + 1}: la fonte {f['url']} non esiste nella build")
                elif ancora and not re.search(rf'id=["\']?{re.escape(ancora)}["\'\s>]', pagina.read_text(encoding="utf-8")):
                    errori.append(f"capitolo {i + 1}: la pagina {percorso} non ha l'ancora #{ancora}")

    if errori:
        print("❌ Libro che si esplora:")
        for e in errori:
            print("  -", e)
        return 1
    print(f"✅ Libro che si esplora: {len(base)} capitoli coerenti in {len(dati)} versioni"
          + (", fonti e ancore presenti nella build." if args.public else "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
