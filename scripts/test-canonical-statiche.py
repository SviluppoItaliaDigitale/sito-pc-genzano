#!/usr/bin/env python3
"""Prova come aggiungi-canonical-statiche.py riconosce il link canonical.

Il controllo della mappa per i motori leggeva l'indirizzo solo con rel prima di
href e saltava in silenzio le pagine scritte nell'altro ordine (revisione della
PR #1529, 22/10/2026). Qui i due ordini, le virgolette semplici, i valori senza
virgolette, rel con più valori, un link che non è canonical, poi il controllo
della mappa su un file di prova scritto con href prima di rel.

    python3 scripts/test-canonical-statiche.py
"""

import importlib.util
import sys
import tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "canonical_statiche", Path(__file__).with_name("aggiungi-canonical-statiche.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

URL = "https://www.protezionecivilegenzano.it/giochi/prova/"
CASI = [
    (f'<link rel="canonical" href="{URL}">', URL),
    (f'<link href="{URL}" rel="canonical">', URL),
    (f"<link href='{URL}' rel='canonical' />", URL),
    (f"<LINK HREF={URL} REL=canonical>", URL),
    (f'<link rel="alternate canonical" href="{URL}">', URL),
    (f'<link rel="stylesheet" href="/css/x.css">\n<link href="{URL}"\n      rel="canonical">', URL),
    ('<link rel="stylesheet" href="/css/x.css">', None),
    ('<link rel="canonical">', ""),  # c'è, ma senza indirizzo
]

errori = 0
for html, atteso in CASI:
    link = mod.link_canonical(f"<html><head><title>Prova</title>{html}</head><body></body></html>")
    ottenuto = None if link is None else link.get("href", "")
    if ottenuto != atteso:
        errori += 1
        print(f"❌ {html!r}: atteso {atteso!r}, letto {ottenuto!r}")

# Il controllo della mappa deve segnalare una pagina con href prima di rel che
# nella mappa non c'è, e tacere quando c'è.
with tempfile.TemporaryDirectory() as cartella:
    radice = Path(cartella)
    pagina = radice / "static" / "giochi" / "prova" / "index.html"
    pagina.parent.mkdir(parents=True)
    pagina.write_text(f'<!doctype html><html lang="it"><head><title>Prova</title>\n'
                      f'<link href="{URL}" rel="canonical">\n</head><body></body></html>',
                      encoding="utf-8")
    mod.ROOT = radice
    mod.pagine = lambda: [pagina]
    for nella_mappa, attesi in ((False, 1), (True, 0)):
        mappa = radice / "sitemap.xml"
        loc = f"<url><loc>{URL}</loc></url>" if nella_mappa else ""
        mappa.write_text(f'<?xml version="1.0"?><urlset>{loc}</urlset>', encoding="utf-8")
        assenti = mod.assenti_dalla_mappa(mappa)
        if len(assenti) != attesi:
            errori += 1
            stato = "nella mappa" if nella_mappa else "assente dalla mappa"
            print(f"❌ pagina {stato}: attese {attesi} segnalazioni, ottenute {len(assenti)} {assenti}")

if errori:
    print(f"\n{errori} prove non superate.")
    sys.exit(1)
print(f"✅ Canonical riconosciuto in tutte le prove ({len(CASI)} casi) e controllo della mappa corretto.")
