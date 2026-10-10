#!/usr/bin/env python3
"""Immagini meteo generate in automatico: stanno in una release, non in git.

Le carte ECMWF e la carta sinottica si rigenerano più volte al giorno. Committate
in git, ogni versione restava per sempre nella storia del repository (circa
1,5-2 GB l'anno di immagini che nessuno avrebbe più guardato). Dal 10/10/2026
stanno come allegati della release `immagini-meteo`, che si sovrascrive a ogni
giro e non pesa sul repository; i metadati JSON restano in git.

Uso (serve `gh` autenticato con GH_TOKEN, oppure in locale `gh auth login`):
    python3 scripts/immagini-meteo-release.py scarica   # prima della build o dei generatori
    python3 scripts/immagini-meteo-release.py carica ecmwf|sinottica  # dopo il generatore, solo i suoi file

`scarica` è fail-safe: se la release non risponde ripiega sulle copie servite
dal sito pubblicato, e se manca anche quella lo dice ed esce 0 (le immagini
tornano al deploy successivo). `carica` crea la release se non esiste ancora.
"""
from __future__ import annotations

import subprocess
import sys
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
}


def gh(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], cwd=REPO_ROOT, capture_output=True, text=True)


def dal_sito(percorso: str, dest: Path) -> bool:
    req = urllib.request.Request(f"{SITO}/{percorso}", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            dati = r.read()
    except Exception as e:  # noqa: BLE001
        print(f"  [ko ] {percorso} anche dal sito: {e}")
        return False
    if len(dati) < 1000:
        print(f"  [ko ] {percorso} dal sito: risposta troppo piccola ({len(dati)} byte)")
        return False
    dest.write_bytes(dati)
    return True


def scarica() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        r = gh("release", "download", TAG, "--dir", tmp, "--clobber")
        if r.returncode != 0:
            print(f"Release {TAG} non disponibile ({r.stderr.strip()}): ripiego sul sito.")
        mancanti = []
        for nome, percorso in FILE.items():
            dest = REPO_ROOT / "static" / percorso
            dest.parent.mkdir(parents=True, exist_ok=True)
            sorgente = Path(tmp) / nome
            if sorgente.is_file() and sorgente.stat().st_size > 0:
                dest.write_bytes(sorgente.read_bytes())
                print(f"  [ok ] {percorso} (release)")
            elif dal_sito(percorso, dest):
                print(f"  [ok ] {percorso} (copia del sito)")
            else:
                mancanti.append(percorso)
    if mancanti:
        print("ATTENZIONE: immagini non recuperate, torneranno al prossimo deploy: "
              + ", ".join(mancanti))
    return 0


def carica(gruppo: str) -> int:
    if gh("release", "view", TAG).returncode != 0:
        r = gh("release", "create", TAG, "--title", "Immagini meteo (aggiornate in automatico)",
               "--notes", "Carte ECMWF e carta sinottica dell'ultima esecuzione. "
               "Si sovrascrivono a ogni giro: scripts/immagini-meteo-release.py.",
               "--latest=false")
        if r.returncode != 0:
            print(f"Creazione della release non riuscita: {r.stderr.strip()}")
            return 1
    with tempfile.TemporaryDirectory() as tmp:
        da_caricare = []
        for nome, percorso in FILE.items():
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
    return 0


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else ""
    if comando == "scarica":
        sys.exit(scarica())
    if comando == "carica" and len(sys.argv) > 2 and sys.argv[2] in ("ecmwf", "meteo-sinottica", "sinottica"):
        sys.exit(carica("meteo-sinottica" if sys.argv[2] == "sinottica" else sys.argv[2]))
    print(__doc__)
    sys.exit(2)
