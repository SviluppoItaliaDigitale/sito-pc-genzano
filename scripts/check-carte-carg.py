#!/usr/bin/env python3
"""
Controllo settimanale delle carte geologiche CARG copiate sul sito.

Il sito conserva in static/manuali/carg/ una copia degli otto PDF ISPRA
(carte e note illustrative dei fogli 374 Roma, 375 Tivoli, 387 Albano
Laziale, 388 Velletri) linkati dall'articolo sulla Carta geologica d'Italia
e dall'Area Download. La fonte che fa fede è l'archivio aperto dell'ISPRA
(openaccessrepository.it, InvenioRDM): se l'ISPRA ripubblica un foglio
corretto, la nostra copia resta vecchia senza che nessuno se ne accorga.

Per ogni record interroga l'API dell'archivio e segnala:
  - una NUOVA VERSIONE del record (versions.is_latest = false);
  - un file cambiato sulla fonte (md5 dell'archivio diverso dal nostro);
  - un nome di file cambiato o più file nel record (da guardare a mano);
  - un record che non risponde (fonte giù o record spostato).

Non scarica nulla e non modifica nulla: la sostituzione della copia e
l'aggiornamento dell'articolo si fanno in sessione, dopo aver letto cosa è
cambiato. Exit code = numero di segnalazioni (0 = tutto allineato); in
caso di fonte irraggiungibile su tutti i record esce 0 ma lo scrive, perché
un archivio giù per un'ora non è una carta cambiata.

Uso:
  python3 scripts/check-carte-carg.py [--issue-body corpo.md]
Solo Python standard.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARTELLA = ROOT / "static" / "manuali" / "carg"
API = "https://www.openaccessrepository.it/api/records/"
UA = "PCGenzanoBot/1.0 (https://www.protezionecivilegenzano.it/)"

# record dell'archivio ISPRA → copia locale. I DOI sono 10.15161/oar.it/<id>.
FOGLI = [
    ("374 Roma — carta", "76970", "carg-foglio-374-roma-carta.pdf"),
    ("374 Roma — note illustrative", "76975", "carg-foglio-374-roma-note.pdf"),
    ("375 Tivoli — carta", "j4z30-75560", "carg-foglio-375-tivoli-carta.pdf"),
    ("375 Tivoli — note illustrative", "bjed8-3mg96", "carg-foglio-375-tivoli-note.pdf"),
    ("387 Albano Laziale — carta", "73sy6-ztb78", "carg-foglio-387-albano-laziale-carta.pdf"),
    ("387 Albano Laziale — note illustrative", "3qrfn-yk004", "carg-foglio-387-albano-laziale-note.pdf"),
    ("388 Velletri — carta", "va3pg-a7z40", "carg-foglio-388-velletri-carta.pdf"),
    ("388 Velletri — note illustrative", "vdxbr-xhj22", "carg-foglio-388-velletri-note.pdf"),
]


def leggi_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def md5_locale(p: Path) -> str:
    h = hashlib.md5()
    with p.open("rb") as f:
        for blocco in iter(lambda: f.read(1 << 20), b""):
            h.update(blocco)
    return h.hexdigest()


def controlla(etichetta: str, rid: str, nome_locale: str) -> tuple[list[str], bool]:
    """Restituisce (segnalazioni, fonte_raggiunta)."""
    segn: list[str] = []
    locale = CARTELLA / nome_locale
    if not locale.is_file():
        segn.append(f"**{etichetta}**: la copia locale `{nome_locale}` manca dal repository.")
    try:
        rec = leggi_json(API + rid)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as e:
        segn.append(f"**{etichetta}**: record `{rid}` non raggiungibile ({e}).")
        return segn, False
    ver = rec.get("versions") or {}
    if ver.get("is_latest") is False:
        nuovo = ""
        try:
            ultimo = leggi_json(API + rid + "/versions/latest")
            nuovo = ultimo.get("id", "")
        except Exception:
            pass
        segn.append(
            f"**{etichetta}**: l'ISPRA ha pubblicato una NUOVA VERSIONE del record `{rid}`"
            + (f" → `{nuovo}` (https://doi.org/10.15161/oar.it/{nuovo})" if nuovo else "")
            + ". Scaricare il file nuovo, sostituire la copia e aggiornare DOI e dimensioni nell'articolo e nell'Area Download."
        )
        return segn, True
    entries = (rec.get("files") or {}).get("entries") or {}
    pdf = [(n, e) for n, e in entries.items() if n.lower().endswith(".pdf")]
    if len(pdf) != 1:
        segn.append(f"**{etichetta}**: il record `{rid}` ha {len(pdf)} file PDF (attesi 1): "
                    + ", ".join(n for n, _ in pdf) + ". Da guardare a mano.")
        return segn, True
    nome, e = pdf[0]
    checksum = (e.get("checksum") or "").removeprefix("md5:")
    if locale.is_file() and checksum and checksum != md5_locale(locale):
        segn.append(
            f"**{etichetta}**: il file `{nome}` sull'archivio ISPRA è CAMBIATO "
            f"(md5 fonte `{checksum[:12]}…`, dimensione {e.get('size')} byte; "
            f"la nostra copia `{nome_locale}` è di {locale.stat().st_size} byte). "
            "Scaricare la versione nuova e sostituire la copia; aggiornare la dimensione dichiarata."
        )
    return segn, True


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--issue-body", help="scrive qui il corpo Markdown per la issue")
    a = ap.parse_args(argv)
    segnalazioni: list[str] = []
    raggiunti = 0
    for etichetta, rid, nome in FOGLI:
        s, ok = controlla(etichetta, rid, nome)
        raggiunti += ok
        segnalazioni.extend(s)
        print(("⚠️  " if s else "✅ ") + etichetta + ("" if not s else " — " + s[0].split(": ", 1)[1][:90]))
    fonte_giu = raggiunti == 0
    if fonte_giu:
        print("\n❗ L'archivio ISPRA non ha risposto per nessun record: controllo non eseguibile, nessuna segnalazione.")
    elif segnalazioni:
        print(f"\n{len(segnalazioni)} segnalazioni: le copie in static/manuali/carg/ vanno riviste.")
    else:
        print("\nTutte le copie coincidono con l'archivio ISPRA (nessuna nuova versione, stessi checksum).")
    if a.issue_body and segnalazioni and not fonte_giu:
        corpo = ["Confronto fra le copie in `static/manuali/carg/` e i record dell'archivio aperto dell'ISPRA "
                 "(`openaccessrepository.it`, API InvenioRDM: versione del record e checksum md5 del file).", ""]
        corpo += [f"- {s}" for s in segnalazioni]
        corpo += ["", "**Come si ripara:** scaricare il file dal link `?download=1` del record nuovo, verificare che sia un PDF "
                  "(`%PDF`) e che il md5 coincida con quello dell'archivio, sostituire la copia con lo stesso nome, "
                  "aggiornare DOI e dimensione nell'articolo `2026-10-01-carta-geologica-italia-carg-fogli-genzano.md` "
                  "e nella tabella di `content/area-download/_index.md`, rigenerare l'audit PDF "
                  "(`scripts/audit-pdf-accessibilita.py --write`). Se il record ha una nuova versione, aggiornare anche "
                  "l'id in `scripts/check-carte-carg.py`."]
        Path(a.issue_body).write_text("\n".join(corpo) + "\n", encoding="utf-8")
    return 0 if fonte_giu else len(segnalazioni)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
