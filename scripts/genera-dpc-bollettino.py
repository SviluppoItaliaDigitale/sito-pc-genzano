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
Si leggono **entrambe** le fonti e si tiene il bollettino completo più recente.

1. **Fonte ufficiale.** L'albero git del repository elenca `files/*.json` e
   `files/topojson/*`. Il timbro è nel nome (`20261109_1402.json` insieme a
   `_today.json` e `_tomorrow.json`). Bastano tre richieste, fatte in CI: il
   browser della Sala non le fa, legge solo questo snapshot.
2. **Mirror opendatasicilia**, che per la barra di allerta
   (`scripts/check-allerta.py`) è dall'11/11/2026 solo la riserva. Il CSV a
   nome fisso `bollettino-oggi-zone-latest.csv` ha `data_pubblicazione`
   (`2026-09-22T14:21:59+01:00` → `20260922_1421`).

Dall'11/11/2026 questa ricerca la usa anche `scripts/check-allerta.py`, che
importa le funzioni di questo file per leggere le carte della zona di
Genzano dal repository ufficiale: chi cambia la scelta del timbro la cambia
per entrambi.

Si sceglie il timbro più alto fra quelli trovati, ma solo se sulla fonte
ufficiale esiste la terna (`<timbro>.json` + le due carte). Un timbro più
vecchio non sostituisce lo snapshot già scritto.

🔴 **Perché non basta il mirror.** Dall'8 al 10 novembre 2026 il CSV è rimasto
fermo a `20261108_1422` mentre il Dipartimento aveva già pubblicato
`20261109_1402`. Lo script accettava il mirror appena la terna dell'8 novembre
esisteva ancora, e non guardava la fonte ufficiale (issue #1796).

🔴 **Il contenuto resta del Dipartimento.** Il mirror e l'albero servono solo a
sapere QUALE bollettino è il più recente: le carte si scaricano dal repository
ufficiale (rule 06, gerarchia delle fonti). Lo script non accetta un timbro
che sulla fonte ufficiale non ha la terna completa.

Se l'albero ufficiale non si legge, si ripiega sull'elenco dei commit (l'API
di GitHub). Se una delle due fonti è ferma o non risponde, si usa l'altra. Se
non si riconosce nessun timbro, lo snapshot resta quello di prima e lo script
esce 0: mai un deploy rotto per una fonte di terzi, mai un file svuotato.
Una risposta che si legge ma è vuota non è un dato: CSV senza
`data_pubblicazione`, o albero senza terna, si dichiarano e non si scrive uno
snapshot nullo.

Licenza dei dati: CC BY 4.0 — Dipartimento della Protezione Civile.

Uso:  python3 scripts/genera-dpc-bollettino.py [--dry-run] [--stamp AAAAMMGG_HHMM]
"""
from __future__ import annotations

import csv
import gzip
import io
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
# mirror opendatasicilia, CSV a nome fisso: qui serve solo come indizio del timbro
MIRROR = ("https://raw.githubusercontent.com/opendatasicilia/"
          "DPC-bollettini-criticita-idrogeologica-idraulica/refs/heads/main/"
          "data/bollettini/bollettino-oggi-zone-latest.csv")
OUT = Path(__file__).resolve().parent.parent / "static" / "open-data" / "dpc-bollettino.json"
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/ Sala situazioni)"
STAMP = re.compile(r"(\d{8}_\d{4})")
# Quanti bollettini recenti dell'albero ufficiale si confrontano col mirror.
# Il più nuovo basta quasi sempre; i precedenti servono se la sua terna non
# risponde ancora su raw.githubusercontent.com.
FINESTRA_UFFICIALE = 8
COMMIT_DA_LEGGERE = 20     # solo per il ripiego: il pipeline del DPC committa anche altro
TIMEOUT = 30
NOTA = ("Il timbro è il bollettino completo più recente fra il repository "
        "ufficiale del Dipartimento e il mirror opendatasicilia. Le carte "
        "restano quelle ufficiali. Se una fonte è ferma o non risponde, si "
        "usa l'altra.")


def prendi(url: str, json_atteso: bool = True):
    # Compressione richiesta: gli alberi git ufficiali sono di qualche MB e,
    # dall'11/11/2026, li legge anche check-allerta.py ogni 5 minuti.
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "*/*", "Accept-Encoding": "gzip"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok and url.startswith(API):
        req.add_header("Authorization", f"Bearer {tok}")
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        dati = r.read()
        if (r.headers.get("Content-Encoding") or "").lower() == "gzip":
            dati = gzip.decompress(dati)
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


def timbro_da_csv(testo: str) -> str | None:
    """`data_pubblicazione` del CSV, nell'ora del bollettino (non in UTC).

    `2026-11-08T14:22:59+01:00` è il file `20261108_1422.json`: si tiene l'ora
    scritta, non la si converte.
    """
    try:
        righe = csv.reader(io.StringIO(testo))
        intestazione = [c.strip() for c in next(righe)]
    except StopIteration:
        return None
    if "data_pubblicazione" not in intestazione:
        return None
    i = intestazione.index("data_pubblicazione")
    try:
        campi = next(righe)
    except StopIteration:
        return None
    if i >= len(campi) or not campi[i].strip():
        return None
    try:
        d = datetime.fromisoformat(campi[i].strip())
    except ValueError:
        return None
    return d.strftime("%Y%m%d_%H%M")


def stamp_dal_mirror() -> str | None:
    """Il timbro ricavato da `data_pubblicazione` del CSV a nome fisso."""
    return timbro_da_csv(prendi(MIRROR, json_atteso=False))


def timbri_completi(nomi_json: list[str], nomi_topo: list[str]) -> list[str]:
    """Timbri che nell'albero hanno il JSON e le due carte, dal più recente."""
    topo = set(nomi_topo)
    trovati = []
    for nome in nomi_json:
        m = re.fullmatch(r"(\d{8}_\d{4})\.json", nome)
        if not m:
            continue
        t = m.group(1)
        if f"{t}_today.json" in topo and f"{t}_tomorrow.json" in topo:
            trovati.append(t)
    return sorted(set(trovati), reverse=True)


def timbri_da_alberi(albero_files: dict, albero_topo: dict) -> list[str]:
    """Legge i due alberi git già scaricati. Un albero troncato non è la lista
    vera: meglio fallire e passare al ripiego che scegliere un bollettino vecchio."""
    if albero_files.get("truncated") or albero_topo.get("truncated"):
        raise RuntimeError("albero ufficiale troncato")
    nomi_json = [t.get("path", "") for t in albero_files.get("tree") or []
                 if t.get("type") == "blob"]
    nomi_topo = [t.get("path", "") for t in albero_topo.get("tree") or []
                 if t.get("type") == "blob"]
    return timbri_completi(nomi_json, nomi_topo)


def _url_sottoalbero(albero: dict, nome: str) -> str:
    for t in albero.get("tree") or []:
        if t.get("path") == nome and t.get("type") == "tree" and t.get("url"):
            return t["url"]
    raise RuntimeError(f"manca l'albero {nome}")


def timbri_ufficiali() -> list[str]:
    """Timbri completi nel repository del Dipartimento, dal più recente."""
    root = prendi(f"{API}/git/trees/master")
    files = prendi(_url_sottoalbero(root, "files"))
    topo = prendi(_url_sottoalbero(files, "topojson"))
    return timbri_da_alberi(files, topo)


def timbri_nei_nomi(nomi: list[str]) -> list[str]:
    return sorted({m.group(1) for n in nomi if (m := STAMP.search(n or ""))}, reverse=True)


def timbri_dai_commit() -> list[str]:
    """Ripiego se l'albero non si legge: i timbri nominati dagli ultimi commit."""
    commit = prendi(f"{API}/commits?per_page={COMMIT_DA_LEGGERE}")
    if not isinstance(commit, list) or not commit:
        return []
    trovati: set[str] = set()
    for c in commit:
        sha = c.get("sha")
        if not sha:
            continue
        det = prendi(f"{API}/commits/{sha}")
        nomi = [f.get("filename", "") for f in (det.get("files") or [])]
        trovati.update(timbri_nei_nomi(nomi))
    return sorted(trovati, reverse=True)


def raggruppa(candidati: list[tuple[str, str]]) -> dict[str, list[str]]:
    by: dict[str, list[str]] = {}
    for stamp, fonte in candidati:
        if not STAMP.fullmatch(stamp or ""):
            continue
        fonti = by.setdefault(stamp, [])
        if fonte not in fonti:
            fonti.append(fonte)
    return by


def etichetta(fonti: list[str]) -> str:
    if len(fonti) == 1:
        return fonti[0]
    return " e ".join(fonti) + " (concordi)"


def scegli_timbro(candidati: list[tuple[str, str]], completo):
    """Il timbro più recente la cui terna esiste. Ritorna
    (timbro, fonte, raggruppati, incompleti). Senza un timbro usabile i primi
    due valori sono vuoti."""
    by = raggruppa(candidati)
    incompleti = []
    for stamp in sorted(by, reverse=True):
        if completo(stamp):
            return stamp, etichetta(by[stamp]), by, incompleti
        incompleti.append(stamp)
    return "", "", by, incompleti


def migliori_per_fonte(candidati: list[tuple[str, str]]) -> dict[str, str]:
    """Per ogni fonte, solo il timbro più recente che ha proposto."""
    migliori: dict[str, str] = {}
    for stamp, fonte in candidati:
        if not STAMP.fullmatch(stamp or ""):
            continue
        if fonte not in migliori or stamp > migliori[fonte]:
            migliori[fonte] = stamp
    return migliori


def messaggio_scelta(timbro: str, via: str, candidati: list[tuple[str, str]],
                     incompleti: list[str], problemi: list[str]) -> str:
    """Una riga: timbro scelto, fonte, e che cosa dicevano le altre."""
    migliori = migliori_per_fonte(candidati)
    per_timbro: dict[str, list[str]] = {}
    for fonte, stamp in migliori.items():
        per_timbro.setdefault(stamp, [])
        if fonte not in per_timbro[stamp]:
            per_timbro[stamp].append(fonte)
    pezzi = [f"scelto {timbro} ({via})"]
    piu_vecchi = [f"{s} dal {etichetta(per_timbro[s])}"
                  for s in sorted(per_timbro, reverse=True) if s != timbro]
    if piu_vecchi:
        pezzi.append("più vecchi: " + "; ".join(piu_vecchi))
    if incompleti:
        dett = []
        for s in incompleti:
            fonti = per_timbro.get(s) or []
            dett.append(f"{s} ({etichetta(fonti)})" if fonti else s)
        pezzi.append("senza terna completa: " + ", ".join(dett))
    if problemi:
        pezzi.append("fonti: " + "; ".join(problemi))
    return "[dpc] " + " — ".join(pezzi)


def decisione(timbro: str, vecchio: str, manuale: bool = False) -> str:
    """`scrivi`, `invariato` o `piu_vecchio`. Un ripristino a mano può tornare
    indietro; una lettura delle fonti no."""
    if not vecchio or timbro == vecchio:
        return "invariato" if vecchio and timbro == vecchio else "scrivi"
    if manuale or timbro > vecchio:
        return "scrivi"
    return "piu_vecchio"


def candidati_dalle_fonti() -> tuple[list[tuple[str, str]], list[str]]:
    """Legge fonte ufficiale e mirror. Ognuna può mancare senza fermare l'altra."""
    candidati: list[tuple[str, str]] = []
    problemi: list[str] = []
    ufficiali: list[str] = []
    try:
        ufficiali = timbri_ufficiali()
    except Exception as e:
        problemi.append(f"albero ufficiale non raggiungibile ({e})")
    if ufficiali:
        for t in ufficiali[:FINESTRA_UFFICIALE]:
            candidati.append((t, "fonte ufficiale"))
    else:
        if not problemi:
            problemi.append("albero ufficiale senza una terna completa")
        try:
            for t in timbri_dai_commit():
                candidati.append((t, "API dei commit"))
            if not any(f == "API dei commit" for _, f in candidati):
                problemi.append("API dei commit senza un bollettino riconoscibile")
        except Exception as e:
            problemi.append(f"API dei commit non raggiungibile ({e})")
    try:
        t = stamp_dal_mirror()
        if t:
            candidati.append((t, "mirror opendatasicilia"))
        else:
            problemi.append("mirror senza data_pubblicazione riconoscibile")
    except Exception as e:
        problemi.append(f"mirror non raggiungibile ({e})")
    return candidati, problemi


def leggi_snapshot(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        dati = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return dati if isinstance(dati, dict) else {}


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

    problemi: list[str] = []
    if manuale:
        if not terna_completa(manuale):
            print(f"[dpc] il bollettino {manuale} non è completo sulla fonte ufficiale")
            return 1
        timbro, via = manuale, "indicato a mano"
        candidati, incompleti = [(manuale, "indicato a mano")], []
    else:
        candidati, problemi = candidati_dalle_fonti()
        timbro, via, _, incompleti = scegli_timbro(candidati, terna_completa)

    if not timbro:
        for p in problemi:
            print(f"[dpc] {p}")
        print("[dpc] ATTENZIONE: nessun bollettino completo riconosciuto. "
              "Snapshot lasciato com'era.")
        return 0

    vecchio = leggi_snapshot(OUT)
    vecchio_stamp = vecchio.get("stamp") or ""
    if not STAMP.fullmatch(str(vecchio_stamp)):
        vecchio_stamp = ""
    esito = decisione(timbro, vecchio_stamp, manuale=bool(manuale))
    print(messaggio_scelta(timbro, via, candidati, incompleti,
                           [] if manuale else problemi))

    if esito == "invariato":
        print(f"[dpc] {timbro} invariato ({via})")
        return 0
    if esito == "piu_vecchio":
        print(f"[dpc] {timbro} più vecchio dello snapshot {vecchio_stamp}: "
              "lasciato com'era")
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
            "nota": NOTA,
        },
    }

    if secco:
        print(f"[dpc] (prova) scriverei {timbro} — {nome} [{via}]")
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(nuovo, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[dpc] aggiornato: {timbro} — {nome} [{via}]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
