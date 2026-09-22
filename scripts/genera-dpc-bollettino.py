#!/usr/bin/env python3
"""Risolve qual è il bollettino di criticità DPC più recente e lo scrive come
snapshot nostro: static/open-data/dpc-bollettino.json

PERCHÉ ESISTE
-------------
Nel repository del Dipartimento (pcm-dpc/DPC-Bollettini-Criticita-Idrogeologica
-Idraulica) i bollettini si chiamano col minuto REALE di pubblicazione —
`files/20260922_1421.json` — e non esiste nessun file con nome stabile da
chiamare: l'unico nome fisso è `files/all/latest_all.zip`, un archivio che il
browser non può aprire. Per sapere qual è l'ultimo bisogna quindi chiedere
l'elenco dei commit all'API di GitHub.

Farlo dal browser di ogni visitatore significa appoggiarsi a un limite di
**60 richieste l'ora per indirizzo IP**, condiviso fra tutti quelli che escono
dalla stessa rete: in sede, con più persone sullo stesso IP e la pagina che si
ricarica, la scheda si spegne e la cartina delle zone resta senza colori.
Qui la domanda si fa UNA volta ogni quarto d'ora, in CI, dove il token dà mille
richieste l'ora, e il risultato diventa un file nostro che il browser legge in
una richiesta sola, senza limiti e senza dipendere dall'API.

🔴 FAIL-SAFE. Se la fonte non risponde, lo snapshot resta quello di prima e lo
script esce 0: mai un deploy rotto per una fonte di terzi, mai un file svuotato.
🔴 E una risposta che si legge ma è vuota non è un dato: se l'elenco dei commit
arriva senza nessun nome di bollettino riconoscibile, lo schema è cambiato — si
lascia com'era e si dichiara l'anomalia, invece di scrivere uno snapshot nullo.

Licenza dei dati: CC BY 4.0 — Dipartimento della Protezione Civile.

Uso:  python3 scripts/genera-dpc-bollettino.py [--dry-run]
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
OUT = Path(__file__).resolve().parent.parent / "static" / "open-data" / "dpc-bollettino.json"
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/ Sala situazioni)"
STAMP = re.compile(r"(\d{8}_\d{4})")
COMMIT_DA_LEGGERE = 8      # il pipeline del DPC committa anche cose che non sono bollettini
TIMEOUT = 25


def prendi(url: str, json_atteso: bool = True):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok and url.startswith(API):
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        dati = r.read()
    return json.loads(dati) if json_atteso else dati


def esiste(url: str) -> bool:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status == 200
    except (urllib.error.URLError, OSError):
        return False


def trova_stamp() -> str | None:
    """Il timbro del bollettino più recente, dai nomi dei file toccati dai commit."""
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
            # serve la terna completa: senza le due carte la cartina resta vuota
            if (esiste(f"{RAW}{t}.json")
                    and esiste(f"{RAW}topojson/{t}_today.json")
                    and esiste(f"{RAW}topojson/{t}_tomorrow.json")):
                return t
    return None


def main() -> int:
    secco = "--dry-run" in sys.argv
    # --stamp serve per il primo innesco e per un ripristino a mano da una
    # postazione che non raggiunge l'API: il timbro si legge sul repository
    # ufficiale e si passa qui, senza inventarlo.
    manuale = None
    for i, a in enumerate(sys.argv):
        if a == "--stamp" and i + 1 < len(sys.argv):
            manuale = sys.argv[i + 1]
    if manuale and not STAMP.fullmatch(manuale):
        print(f"[dpc] timbro non valido: {manuale}")
        return 1

    if manuale:
        if not esiste(f"{RAW}{manuale}.json"):
            print(f"[dpc] il bollettino {manuale} non esiste sulla fonte")
            return 1
        timbro = manuale
    else:
        try:
            timbro = trova_stamp()
        except Exception as e:                                # rete, API, quota
            print(f"[dpc] fonte non raggiungibile ({e}): snapshot lasciato com'era")
            return 0

    if not timbro:
        # non è "nessun bollettino": è che non lo abbiamo riconosciuto
        print("[dpc] ATTENZIONE: nessun timbro riconosciuto negli ultimi "
              f"{COMMIT_DA_LEGGERE} commit — schema dei nomi forse cambiato. "
              "Snapshot lasciato com'era.")
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
            "licenza": "CC BY 4.0 — Dipartimento della Protezione Civile",
            "nota": "Timbro del bollettino più recente, risolto in CI perché il "
                    "repository del DPC non espone un nome di file stabile.",
        },
    }

    vecchio = {}
    if OUT.exists():
        try:
            vecchio = json.loads(OUT.read_text(encoding="utf-8"))
        except Exception:
            vecchio = {}
    if vecchio.get("stamp") == timbro:
        print(f"[dpc] {timbro} invariato")
        return 0

    if secco:
        print(f"[dpc] (prova) scriverei {timbro} — {nome}")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(nuovo, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[dpc] aggiornato: {timbro} — {nome}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
