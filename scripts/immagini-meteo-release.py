#!/usr/bin/env python3
"""Immagini meteo generate in automatico: stanno in una release, non in git.

Le carte ECMWF e la carta sinottica si rigenerano più volte al giorno. Committate
in git, ogni versione restava per sempre nella storia del repository (circa
1,5-2 GB l'anno di immagini che nessuno avrebbe più guardato). Dal 10/10/2026
stanno come allegati della release `immagini-meteo`, che si sovrascrive a ogni
giro e non pesa sul repository; i metadati JSON restano in git.

Uso (serve `gh` autenticato con GH_TOKEN, oppure in locale `gh auth login`):
    python3 scripts/immagini-meteo-release.py scarica [--rigoroso]  # prima dei generatori; --rigoroso nel deploy
    python3 scripts/immagini-meteo-release.py carica ecmwf|sinottica|sentinel1|sentinel2  # dopo il generatore, solo i suoi file

`scarica` ripiega sulle copie servite dal sito pubblicato se la release non
risponde. Le scene Sentinel-2 (`sentinel2-genzano-AAAAMMGG.webp`) hanno nomi
che cambiano: l'elenco atteso si legge da static/open-data/copernicus-sentinel2.json
e `carica sentinel2` toglie dalla release le scene che il JSON non elenca più. Se manca anche quella esce 0 nei workflow dei generatori; con
`--rigoroso` (nel deploy) esce 1, perché un caricamento FTP senza quelle
immagini le cancellerebbe da Aruba. `carica` crea la release se non esiste ancora.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import urllib.error
import tempfile
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TAG = "immagini-meteo"
SITO = "https://www.protezionecivilegenzano.it"
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/)"

# nome dell'allegato nella release -> percorso nel sito (sotto static/)
FILE = {
    "ecmwf-medium-mslp-wind850.webp": "images/ecmwf/medium-mslp-wind850.webp",
    "ecmwf-medium-2mt-wind30.webp": "images/ecmwf/medium-2mt-wind30.webp",
    "ecmwf-medium-precipitation-type.webp": "images/ecmwf/medium-precipitation-type.webp",
    "ecmwf-medium-cape-cin.webp": "images/ecmwf/medium-cape-cin.webp",
    "meteo-sinottica-italia.webp": "images/meteo-sinottica-italia.webp",
    "meteo-sinottica-italia.png": "images/meteo-sinottica-italia.png",
    # radar Sentinel-1 su Genzano (scripts/genera-copernicus-sentinel1.py, dal 10/10/2026)
    "sentinel1-genzano.webp": "images/sentinel/sentinel1-genzano.webp",
    "sentinel1-genzano-prima.webp": "images/sentinel/sentinel1-genzano-prima.webp",
}
S2_JSON = REPO_ROOT / "static" / "open-data" / "copernicus-sentinel2.json"
S2_NOME = re.compile(r"sentinel2-genzano-\d{8}\.webp")


def file_attesi() -> dict[str, str]:
    """FILE più le scene Sentinel-2 elencate dal JSON (nomi variabili, dal 10/10/2026)."""
    attesi = dict(FILE)
    if S2_JSON.is_file():
        try:
            for s in json.loads(S2_JSON.read_text(encoding="utf-8")).get("scene", []):
                nome = Path(str(s.get("immagine", ""))).name
                if S2_NOME.fullmatch(nome):
                    attesi[nome] = "images/sentinel/" + nome
        except ValueError:
            pass
    return attesi


def repo_slug() -> str:
    r = subprocess.run(["git", "remote", "get-url", "origin"], cwd=REPO_ROOT, capture_output=True, text=True)
    m = re.search(r"github\.com[:/]([^/]+/[^/\s]+?)(?:\.git)?$", r.stdout.strip())
    return m.group(1) if m else ""


def asset_release() -> dict[str, int]:
    """nome -> id degli allegati della release (API REST: funziona anche dove GraphQL è filtrato)."""
    r = gh("api", f"repos/{repo_slug()}/releases/tags/{TAG}")
    if r.returncode != 0:
        return {}
    try:
        return {a["name"]: a["id"] for a in json.loads(r.stdout).get("assets", [])}
    except ValueError:
        return {}


def gh(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], cwd=REPO_ROOT, capture_output=True, text=True)


def dal_sito(percorso: str, dest: Path) -> bool | None:
    """True = copiato; False = errore; None = il sito non ha mai avuto quel file (404)."""
    req = urllib.request.Request(f"{SITO}/{percorso}", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            dati = r.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"  [ -- ] {percorso}: non ancora pubblicato (404), nessuna copia da proteggere")
            return None
        print(f"  [ko ] {percorso} anche dal sito: {e}")
        return False
    except Exception as e:  # noqa: BLE001
        print(f"  [ko ] {percorso} anche dal sito: {e}")
        return False
    if len(dati) < 1000:
        print(f"  [ko ] {percorso} dal sito: risposta troppo piccola ({len(dati)} byte)")
        return False
    dest.write_bytes(dati)
    return True


def scarica(rigoroso: bool = False) -> int:
    with tempfile.TemporaryDirectory() as tmp:
        r = gh("release", "download", TAG, "--dir", tmp, "--clobber")
        if r.returncode != 0:
            print(f"Release {TAG} non disponibile ({r.stderr.strip()}): ripiego sul sito.")
        mancanti = []
        for nome, percorso in file_attesi().items():
            dest = REPO_ROOT / "static" / percorso
            dest.parent.mkdir(parents=True, exist_ok=True)
            sorgente = Path(tmp) / nome
            if sorgente.is_file() and sorgente.stat().st_size > 0:
                dest.write_bytes(sorgente.read_bytes())
                print(f"  [ok ] {percorso} (release)")
            else:
                esito = dal_sito(percorso, dest)
                if esito:
                    print(f"  [ok ] {percorso} (copia del sito)")
                elif esito is False:
                    mancanti.append(percorso)
                # None: file nuovo, mai pubblicato — il caricamento FTP non cancella nulla
    if mancanti:
        if rigoroso:
            # Nel deploy: senza queste immagini il caricamento FTP cancellerebbe
            # da Aruba le ultime copie buone. Meglio fermare il deploy e lasciare
            # il sito com'è (succede solo se release e sito sono giù insieme).
            print("ERRORE: immagini meteo non recuperate né dalla release né dal sito: "
                  + ", ".join(mancanti) + ". Deploy fermato per non cancellarle da Aruba.")
            return 1
        print("ATTENZIONE: immagini non recuperate: " + ", ".join(mancanti))
    return 0


def carica(gruppo: str) -> int:
    # l'esistenza si chiede all'API REST: `gh release view` passa da GraphQL, che
    # in alcune sessioni e' filtrato, e un "non esiste" sbagliato farebbe tentare
    # una creazione (rifiutata) al posto del caricamento
    if gh("api", f"repos/{repo_slug()}/releases/tags/{TAG}").returncode != 0:
        r = gh("release", "create", TAG, "--title", "Immagini meteo (aggiornate in automatico)",
               "--notes", "Carte ECMWF e carta sinottica dell'ultima esecuzione. "
               "Si sovrascrivono a ogni giro: scripts/immagini-meteo-release.py.",
               "--latest=false")
        if r.returncode != 0:
            print(f"Creazione della release non riuscita: {r.stderr.strip()}")
            return 1
    with tempfile.TemporaryDirectory() as tmp:
        da_caricare = []
        for nome, percorso in file_attesi().items():
            if not nome.startswith(gruppo):
                continue  # ogni workflow carica solo i propri file
            src = REPO_ROOT / "static" / percorso
            if src.is_file() and src.stat().st_size > 0:
                copia = Path(tmp) / nome
                copia.write_bytes(src.read_bytes())
                da_caricare.append(str(copia))
        if not da_caricare:
            print("Nessuna immagine da caricare.")
            return 1
        r = gh("release", "upload", TAG, *da_caricare, "--clobber")
        if r.returncode != 0:
            print(f"Caricamento non riuscito: {r.stderr.strip()}")
            return 1
    print(f"Caricate {len(da_caricare)} immagini nella release {TAG}.")
    if gruppo == "sentinel2":
        # le scene uscite dall'archivio (le piu' vecchie di MAX_SCENE) si tolgono
        # dalla release, altrimenti si accumulano per sempre
        tenute = set(file_attesi())
        for nome, aid in asset_release().items():
            if S2_NOME.fullmatch(nome) and nome not in tenute:
                r = gh("api", "-X", "DELETE", f"repos/{repo_slug()}/releases/assets/{aid}")
                print(f"  {'[ok ]' if r.returncode == 0 else '[ko ]'} tolta dalla release: {nome}")
    return 0


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else ""
    if comando == "scarica":
        sys.exit(scarica(rigoroso="--rigoroso" in sys.argv))
    if comando == "carica" and len(sys.argv) > 2 and sys.argv[2] in ("ecmwf", "meteo-sinottica", "sinottica", "sentinel1", "sentinel2"):
        sys.exit(carica("meteo-sinottica" if sys.argv[2] == "sinottica" else sys.argv[2]))
    print(__doc__)
    sys.exit(2)
