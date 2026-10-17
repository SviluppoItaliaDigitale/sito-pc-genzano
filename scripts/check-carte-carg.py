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
  - un nome di file cambiato o più file nel record (da guardare a mano).
Un record che non risponde (fonte giù o record spostato) non è una novità
ma una fonte rotta: va nel file di --fonti-ko, non fra le segnalazioni.

Cerca inoltre nell'archivio (comunità ISPRA) le NUOVE CARTE DELLA NOSTRA
ZONA: ogni record che cita i fogli 374, 375, 387 o 388 o un luogo dei
Castelli Romani nel titolo e che non è fra quelli già noti (le otto copie e
quelli già valutati in NOTI_NON_COPIATI) viene segnalato come da valutare —
un'edizione a stampa nuova, una carta geotematica (gravimetrica, geologia di
sottosuolo, idrogeologica) o un foglio rifatto. Richiesta dell'utente del
01/10/2026: «fai in modo che tu possa vedere se ci sono nuove cartine della
nostra zona».

Non scarica nulla e non modifica nulla: la sostituzione della copia e
l'aggiornamento dell'articolo si fanno in sessione, dopo aver letto cosa è
cambiato. Exit code: 0 = tutto letto e tutto allineato; 1 = almeno una
segnalazione e/o una fonte non letta. Le segnalazioni vanno in
--issue-body, i record o la ricerca che non hanno risposto in --fonti-ko
(una riga ciascuno, più la riga «FONTI_IN_ERRORE: …» su stdout). Dal
17/10/2026 una fonte che non risponde non resta un avviso nel log: il
workflow apre la issue `fonte-rotta` e chiude il run in rosso (istruzione
dell'utente: «gli errori 404 e simili non devono mai essere ignorati»).
Fino ad allora l'exit 2 «esito indeterminato» lasciava il run verde per
sempre, e si confondeva con «2 segnalazioni».

Uso:
  python3 scripts/check-carte-carg.py [--issue-body corpo.md] [--fonti-ko fonti.md]
Solo Python standard.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CARTELLA = ROOT / "static" / "manuali" / "carg"
API = "https://www.openaccessrepository.it/api/records/"
# Ricerche limitate alla comunità ISPRA dell'archivio: l'archivio è
# multi-ente (INFN compreso) e «Frascati» da solo dà mille risultati di fisica.
API_ISPRA = "https://www.openaccessrepository.it/api/communities/ispra-oa/records"
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

# Record della nostra zona già visti e valutati, NON copiati sul sito: si
# elencano qui con il motivo, così non vengono risegnalati ogni lunedì.
# Un record nuovo che compare nelle ricerche e non sta né in FOGLI né qui
# finisce nella issue come «da valutare».
NOTI_NON_COPIATI = {
    "g905h-bqs87": "Carta Gravimetrica d'Italia 1:50.000, F. 374 Roma (2008): carta geofisica, non geologica — fuori perimetro",
    "h225t-n9d04": "Note illustrative della Carta Gravimetrica F. 374 Roma (2008): idem",
}

# Ricerche per scoprire carte nuove della nostra zona (sintassi InvenioRDM).
RICERCHE_ZONA = [
    '"F. 374" OR "F. 375" OR "F. 387" OR "F. 388"',
    '"Foglio 374" OR "Foglio 375" OR "Foglio 387" OR "Foglio 388"',
    'metadata.title:(Velletri OR Albano OR Nemi OR Genzano OR Ariccia OR Lanuvio OR Albani '
    'OR "Castelli Romani" OR "Vulcano Laziale" OR Tivoli OR Frascati OR Grottaferrata OR "Rocca di Papa")',
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
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, OSError) as e:
        # Fonte rotta, non novità: la riporta main() fra le fonti in errore.
        controlla.ultimo_errore = f"record `{rid}` ({API + rid}): {e}"
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


def cerca_nuove() -> tuple[list[str], bool, list[str]]:
    """Record della zona non ancora noti. Restituisce (segnalazioni, tutte_le_ricerche_ok, errori)."""
    noti = {rid for _, rid, _ in FOGLI} | set(NOTI_NON_COPIATI)
    trovati: dict[str, dict] = {}
    errori: list[str] = []
    for q in RICERCHE_ZONA:
        url = API_ISPRA + "?size=100&sort=newest&q=" + urllib.parse.quote(q, safe="")
        try:
            d = leggi_json(url)
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, OSError) as e:
            errori.append(f"ricerca delle carte nuove `{q}`: {e}")
            continue
        for r in d.get("hits", {}).get("hits", []):
            trovati.setdefault(r["id"], r)
    segn = []
    for rid, r in sorted(trovati.items(), key=lambda kv: kv[1].get("updated", ""), reverse=True):
        if rid in noti:
            continue
        m = r.get("metadata", {})
        segn.append(
            f"**Nuova carta della nostra zona da valutare**: «{m.get('title', '?')}» "
            f"(pubblicata {m.get('publication_date', '?')}, record `{rid}`, https://doi.org/10.15161/oar.it/{rid}). "
            "Se riguarda i Castelli Romani: scaricare, copiare in `static/manuali/carg/`, citarla nell'articolo e nell'Area "
            "Download e aggiungerla a `FOGLI`; altrimenti annotarla in `NOTI_NON_COPIATI` con il motivo."
        )
    return segn, not errori, errori


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--issue-body", help="scrive qui il corpo Markdown per la issue delle novità")
    ap.add_argument("--fonti-ko", help="scrive qui l'elenco delle fonti che non hanno risposto (solo se ce ne sono)")
    a = ap.parse_args(argv)
    segnalazioni: list[str] = []
    fonti_ko: list[str] = []
    for etichetta, rid, nome in FOGLI:
        controlla.ultimo_errore = ""
        s, ok = controlla(etichetta, rid, nome)
        segnalazioni.extend(s)
        if not ok:
            fonti_ko.append(f"{etichetta}: {controlla.ultimo_errore}")
            print(f"❗ {etichetta} — record non raggiungibile ({controlla.ultimo_errore[:90]})")
        else:
            print(("⚠️  " if s else "✅ ") + etichetta + ("" if not s else " — " + s[0].split(": ", 1)[1][:90]))
    nuove, ricerca_ok, errori_ricerca = cerca_nuove()
    segnalazioni.extend(nuove)
    fonti_ko.extend(errori_ricerca)
    if ricerca_ok:
        print(("⚠️  " if nuove else "✅ ") + f"ricerca di carte nuove della zona: {len(nuove)} da valutare")
    else:
        print(f"❗ ricerca di carte nuove della zona: {len(errori_ricerca)} ricerche su {len(RICERCHE_ZONA)} senza risposta")
    if segnalazioni:
        print(f"\n{len(segnalazioni)} segnalazioni: le copie in static/manuali/carg/ vanno riviste.")
    elif not fonti_ko:
        print("\nTutte le copie coincidono con l'archivio ISPRA (nessuna nuova versione, stessi checksum).")
    if fonti_ko:
        print(f"\n❗ {len(fonti_ko)} fonti non hanno risposto: il controllo è incompleto, da riparare.")
        print("FONTI_IN_ERRORE: " + "; ".join(fonti_ko))
        if a.fonti_ko:
            Path(a.fonti_ko).write_text("".join(f"- {f}\n" for f in fonti_ko), encoding="utf-8")
    if a.issue_body and segnalazioni:
        corpo = ["Confronto fra le copie in `static/manuali/carg/` e i record dell'archivio aperto dell'ISPRA "
                 "(`openaccessrepository.it`, API InvenioRDM: versione del record e checksum md5 del file), più la "
                 "ricerca di record nuovi che citano i fogli 374/375/387/388 o un luogo dei Castelli Romani nel titolo.", ""]
        corpo += [f"- {s}" for s in segnalazioni]
        corpo += ["", "**Come si ripara:** scaricare il file dal link `?download=1` del record nuovo, verificare che sia un PDF "
                  "(`%PDF`) e che il md5 coincida con quello dell'archivio, sostituire la copia con lo stesso nome, "
                  "aggiornare DOI e dimensione nell'articolo `2026-10-01-carta-geologica-italia-carg-fogli-genzano.md` "
                  "e nella tabella di `content/area-download/_index.md`, rigenerare l'audit PDF "
                  "(`scripts/audit-pdf-accessibilita.py --write`). Se il record ha una nuova versione, aggiornare anche "
                  "l'id in `scripts/check-carte-carg.py`."]
        Path(a.issue_body).write_text("\n".join(corpo) + "\n", encoding="utf-8")
    return 1 if (segnalazioni or fonti_ko) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
