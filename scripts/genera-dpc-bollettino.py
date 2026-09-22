#!/usr/bin/env python3
"""Risolve qual è il bollettino di criticità DPC più recente e lo scrive come
snapshot nostro: static/open-data/dpc-bollettino.json

PERCHÉ ESISTE
-------------
Nel repository del Dipartimento (pcm-dpc/DPC-Bollettini-Criticita-Idrogeologica
-Idraulica) i bollettini si chiamano col minuto REALE di pubblicazione —
`files/20260922_1421.json` — e non esiste nessun file con nome stabile da
chiamare: l'unico è `files/all/latest_all.zip`, un archivio che il browser non
può aprire. Senza sapere il «timbro» non si trovano nemmeno le due carte che
colorano le zone sulla cartina della Sala situazioni.

DA DOVE SI PRENDE IL TIMBRO
---------------------------
🔴 Dal **mirror opendatasicilia**, la stessa fonte che il sito usa già per la
barra di allerta (`scripts/check-allerta.py`). Quel repository ripubblica i
bollettini del DPC in CSV con **nomi di file fissi** (`bollettino-oggi-zone-
latest.csv`) e, dentro, il campo `data_pubblicazione`: `2026-09-22T14:21:59`
corrisponde esattamente al file ufficiale `20260922_1421.json`. Verificato su
sei giorni consecutivi (17→22 settembre 2026): sei timbri su sei coincidono e
sei file ufficiali esistono.

È la strada più solida perché non dipende da nessuna quota: leggere l'elenco
dei commit dall'**API di GitHub** costa **60 richieste l'ora per indirizzo IP**
senza credenziali, e fatto dal browser di ogni visitatore significa che in sede,
con più postazioni sullo stesso IP, la cartina resta senza colori. L'API resta
qui solo come ripiego, se il mirror non risponde.

🔴 **Il contenuto resta del Dipartimento.** Il mirror serve solo a sapere QUALE
bollettino è quello corrente: le due carte delle zone si scaricano dal
repository ufficiale, che è la fonte primaria (rule 06, gerarchia delle fonti).
Lo script non accetta un timbro che sulla fonte ufficiale non esiste.

🔴 FAIL-SAFE. Se le fonti non rispondono, lo snapshot resta quello di prima e lo
script esce 0: mai un deploy rotto per una fonte di terzi, mai un file svuotato.
🔴 E una risposta che si legge ma è vuota non è un dato: se il CSV arriva senza
`data_pubblicazione` leggibile, lo schema è cambiato — si lascia il file com'era
e si dichiara l'anomalia, invece di scrivere uno snapshot nullo.

Licenza dei dati: CC BY 4.0 — Dipartimento della Protezione Civile.

Uso:  python3 scripts/genera-dpc-bollettino.py [--dry-run] [--stamp AAAAMMGG_HHMM]
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = "pcm-dpc/DPC-Bollettini-Criticita-Idrogeologica-Idraulica"
API = f"https://api.github.com/repos/{REPO}"
RAW = f"https://raw.githubusercontent.com/{REPO}/master/files/"
# stessa fonte della barra di allerta del sito (check-allerta.py): nome fisso
MIRROR = ("https://raw.githubusercontent.com/opendatasicilia/"
          "DPC-bollettini-criticita-idrogeologica-idraulica/refs/heads/main/"
          "data/bollettini/bollettino-oggi-zone-latest.csv")
OUT = Path(__file__).resolve().parent.parent / "static" / "open-data" / "dpc-bollettino.json"
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/ Sala situazioni)"
STAMP = re.compile(r"(\d{8}_\d{4})")
COMMIT_DA_LEGGERE = 8      # solo per il ripiego: il pipeline del DPC committa anche altro
TIMEOUT = 30


def prendi(url: str, json_atteso: bool = True):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok and url.startswith(API):
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        dati = r.read()
    return json.loads(dati) if json_atteso else dati.decode("utf-8", "replace")


def esiste(url: str) -> bool:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status == 200
    except (urllib.error.URLError, OSError):
        return False


def terna_completa(t: str) -> bool:
    """Senza le due carte la cartina delle zone resterebbe vuota."""
    return (esiste(f"{RAW}{t}.json")
            and esiste(f"{RAW}topojson/{t}_today.json")
            and esiste(f"{RAW}topojson/{t}_tomorrow.json"))


def stamp_dal_mirror() -> str | None:
    """Il timbro ricavato da `data_pubblicazione` del CSV a nome fisso."""
    testo = prendi(MIRROR, json_atteso=False)
    righe = testo.splitlines()
    if len(righe) < 2:
        return None
    intestazione = [c.strip() for c in righe[0].split(",")]
    if "data_pubblicazione" not in intestazione:
        return None                                   # schema cambiato
    i = intestazione.index("data_pubblicazione")
    campi = righe[1].split(",")
    if i >= len(campi):
        return None
    try:
        d = datetime.fromisoformat(campi[i].strip())
    except ValueError:
        return None
    return d.strftime("%Y%m%d_%H%M")


def stamp_dall_api() -> str | None:
    """Ripiego: i nomi dei file toccati dagli ultimi commit del DPC."""
    commit = prendi(f"{API}/commits?per_page={COMMIT_DA_LEGGERE}")
    if not isinstance(commit, list) or not commit:
        return None
    for c in commit:
        sha = c.get("sha")
        if not sha:
            continue
        det = prendi(f"{API}/commits/{sha}")
        timbri = sorted({m.group(1) for f in (det.get("files") or [])
                         if (m := STAMP.search(f.get("filename", "")))}, reverse=True)
        for t in timbri:
            if terna_completa(t):
                return t
    return None


def main() -> int:
    secco = "--dry-run" in sys.argv
    # --stamp serve per un ripristino a mano da una postazione che non raggiunge
    # le fonti: il timbro si legge sul repository ufficiale e si passa qui,
    # senza inventarlo.
    manuale = None
    for i, a in enumerate(sys.argv):
        if a == "--stamp" and i + 1 < len(sys.argv):
            manuale = sys.argv[i + 1]
    if manuale and not STAMP.fullmatch(manuale):
        print(f"[dpc] timbro non valido: {manuale}")
        return 1

    timbro, via = None, ""
    if manuale:
        if not terna_completa(manuale):
            print(f"[dpc] il bollettino {manuale} non è completo sulla fonte ufficiale")
            return 1
        timbro, via = manuale, "indicato a mano"
    else:
        try:
            t = stamp_dal_mirror()
            if t and terna_completa(t):
                timbro, via = t, "mirror opendatasicilia"
            elif t:
                print(f"[dpc] il mirror indica {t}, ma sulla fonte ufficiale non c'è "
                      "la terna completa: provo l'API")
        except Exception as e:
            print(f"[dpc] mirror non raggiungibile ({e}): provo l'API")

        if not timbro:
            try:
                t = stamp_dall_api()
                if t:
                    timbro, via = t, "API di GitHub (ripiego)"
            except Exception as e:
                print(f"[dpc] anche l'API non risponde ({e}): snapshot lasciato com'era")
                return 0

    if not timbro:
        # non è "nessun bollettino": è che non lo abbiamo riconosciuto
        print("[dpc] ATTENZIONE: nessun timbro riconosciuto — schema dei nomi o "
              "del CSV forse cambiato. Snapshot lasciato com'era.")
        return 0

    try:
        boll = prendi(f"{RAW}{timbro}.json")
        nome = boll.get("name") or ""
    except Exception as e:
        print(f"[dpc] bollettino {timbro} non leggibile ({e}): snapshot lasciato com'era")
        return 0

    nuovo = {
        "stamp": timbro,
        "name": nome,
        "_snapshot": {
            "letto": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fonte": f"https://github.com/{REPO}",
            "timbro_da": via,
            "licenza": "CC BY 4.0 — Dipartimento della Protezione Civile",
            "nota": "Il repository del DPC non espone un nome di file stabile: il "
                    "timbro del bollettino corrente si ricava dal mirror "
                    "opendatasicilia (stessa fonte della barra di allerta del sito) "
                    "e si verifica sulla fonte ufficiale, da cui restano le carte.",
        },
    }

    vecchio = {}
    if OUT.exists():
        try:
            vecchio = json.loads(OUT.read_text(encoding="utf-8"))
        except Exception:
            vecchio = {}
    if vecchio.get("stamp") == timbro:
        print(f"[dpc] {timbro} invariato ({via})")
        return 0

    if secco:
        print(f"[dpc] (prova) scriverei {timbro} — {nome} [{via}]")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(nuovo, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[dpc] aggiornato: {timbro} — {nome} [{via}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
