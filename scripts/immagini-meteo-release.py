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
    python3 scripts/immagini-meteo-release.py carica-permanenti  # copia aggiuntiva immutabile e verifica
    python3 scripts/immagini-meteo-release.py scarica-permanenti  # ripristino integrale degli allegati

`scarica` ripiega sulle copie servite dal sito pubblicato se la release non
risponde. Le scene Sentinel-2 (`sentinel2-genzano-AAAAMMGG.webp`) hanno nomi
che cambiano: l'elenco atteso si legge da static/open-data/copernicus-sentinel2.json
e `carica sentinel2` toglie dalla release le scene che il JSON non elenca più. Se manca anche quella esce 0 nei workflow dei generatori; con
`--rigoroso` (nel deploy) esce 1, perché un caricamento FTP senza quelle
immagini le cancellerebbe da Aruba. `carica` crea la release se non esiste ancora.

Gli allegati permanenti stanno in una release separata, senza scadenza. Ogni
ripristino verifica dimensione e SHA-256 e conserva gli indirizzi originali.
Un allegato mancante blocca sempre il comando, anche senza --rigoroso.
Le copie permanenti non vengono mai sovrascritte o eliminate automaticamente.
"""
from __future__ import annotations

import json
import hashlib
import os
import re
import subprocess
import sys
import time
import urllib.error
import tempfile
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TAG = "immagini-meteo"
SITO = "https://www.protezionecivilegenzano.it"
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/)"

# Allegati permanenti: copie immutabili, separate dalle carte meteo aggiornabili.
# Il ripristino precede la build e controlla tutti i byte. Non si eliminano
# allegati dalla release né dal sito. Per aggiungerne uno verificare prima
# originale, copia pubblica e impronta; poi eseguire carica-permanenti.
TAG_PERMANENTI = "allegati-permanenti"
PERMANENTI = {
    "e9a894dc914d0c11-campagna-lazio-intervista-volontario-aib-pomezia.mp4": {
        "percorso": "video/campagna-lazio-intervista-volontario-aib-pomezia.mp4",
        "byte": 19389458,
        "sha256": "e9a894dc914d0c118a12b183ca65ade9f37f5549f5baeb6584dc6a5e0795a084",
    },
}


def verifica_permanente(path: Path, info: dict) -> bool:
    if not path.is_file() or path.stat().st_size != info["byte"]:
        return False
    h = hashlib.sha256()
    with path.open("rb") as f:
        for blocco in iter(lambda: f.read(1024 * 1024), b""):
            h.update(blocco)
    return h.hexdigest() == info["sha256"]


def copia_permanente(url: str, dest: Path, info: dict) -> bool:
    """Download limitato e atomico: la destinazione cambia solo dopo la verifica."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(dir=dest.parent) as tmp:
            copia = Path(tmp) / "allegato"
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            totale = 0
            with urllib.request.urlopen(req, timeout=45) as risposta, copia.open("wb") as f:
                for blocco in iter(lambda: risposta.read(1024 * 1024), b""):
                    totale += len(blocco)
                    if totale > info["byte"]:
                        raise ValueError("risposta più grande dell'originale verificato")
                    f.write(blocco)
            if not verifica_permanente(copia, info):
                raise ValueError("dimensione o SHA-256 diverso dall'originale verificato")
            os.replace(copia, dest)
        return True
    except (OSError, ValueError) as e:
        print(f"  [ko ] {info['percorso']}: {e}")
        return False


def url_permanente(nome: str) -> str:
    return f"https://github.com/{repo_slug()}/releases/download/{TAG_PERMANENTI}/{nome}"


def scarica_permanenti() -> int:
    """Ogni allegato deve essere completo; un guasto blocca la pubblicazione."""
    mancanti = []
    for nome, info in PERMANENTI.items():
        dest = REPO_ROOT / "static" / info["percorso"]
        if verifica_permanente(dest, info):
            print(f"  [ok ] {info['percorso']} (originale verificato)")
            continue
        if dest.exists():
            print(f"  [ko ] {info['percorso']}: file locale diverso dall'inventario; non sovrascritto")
            mancanti.append(info["percorso"])
            continue
        for url in (url_permanente(nome), f"{SITO}/{info['percorso']}"):
            if copia_permanente(url, dest, info):
                print(f"  [ok ] {info['percorso']} (copia verificata)")
                break
        else:
            mancanti.append(info["percorso"])
    if mancanti:
        print("ERRORE: allegati permanenti non recuperati integralmente: "
              + ", ".join(mancanti) + ". Pubblicazione fermata per conservarli sul sito.")
        return 1
    return 0


def carica_permanenti() -> int:
    """Crea copie aggiuntive e le riscarica: nessuna sostituzione o cancellazione."""
    if scarica_permanenti():
        return 1
    repo = repo_slug()
    if not repo:
        print("ERRORE: repository di origine non riconosciuto.")
        return 1
    endpoint = f"repos/{repo}/releases/tags/{TAG_PERMANENTI}"
    r = gh("api", endpoint)
    if r.returncode:
        if "404" not in r.stderr:
            print(f"ERRORE: lettura della release non riuscita: {r.stderr.strip()}")
            return 1
        r = gh("release", "create", TAG_PERMANENTI, "--repo", repo,
               "--target", os.environ.get("GITHUB_SHA", "main"),
               "--title", "Allegati permanenti del sito",
               "--notes", "Copie integrali degli allegati, conservate senza scadenza. "
               "Il sito mantiene gli stessi indirizzi e verifica dimensione e SHA-256 prima della pubblicazione. "
               "Nessun allegato va cancellato senza ordine esplicito di Alessandro Cuollo.",
               "--latest=false")
        if r.returncode:
            print(f"ERRORE: creazione della release non riuscita: {r.stderr.strip()}")
            return 1
    r = gh("api", endpoint)
    try:
        if r.returncode:
            raise ValueError(r.stderr.strip())
        assets = {a["name"]: a for a in json.loads(r.stdout)["assets"]}
    except (ValueError, KeyError, TypeError) as e:
        print(f"ERRORE: elenco allegati non verificabile: {e}")
        return 1
    for nome, info in PERMANENTI.items():
        if nome not in assets:
            with tempfile.TemporaryDirectory() as tmp:
                copia = Path(tmp) / nome
                copia.write_bytes((REPO_ROOT / "static" / info["percorso"]).read_bytes())
                r = gh("release", "upload", TAG_PERMANENTI, str(copia), "--repo", repo)
                if r.returncode:
                    print(f"ERRORE: copia di sicurezza non caricata: {r.stderr.strip()}")
                    return 1
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / nome
            for tentativo in range(3):
                if copia_permanente(url_permanente(nome), dest, info):
                    print(f"  [ok ] backup nella release verificato byte per byte: {info['percorso']}")
                    break
                if tentativo < 2:
                    time.sleep(3)
            else:
                print("ERRORE: copia di sicurezza non verificata; conservare l'originale in git.")
                return 1
    return 0

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
    # mappa dei cambiamenti radar (stessa orbita) e dei cambiamenti Sentinel-2, dall'11/10/2026
    "sentinel1-genzano-cambi.webp": "images/sentinel/sentinel1-genzano-cambi.webp",
    "sentinel2-genzano-cambi.webp": "images/sentinel/sentinel2-genzano-cambi.webp",
}
S2_JSON = REPO_ROOT / "static" / "open-data" / "copernicus-sentinel2.json"
S1_JSON = REPO_ROOT / "static" / "open-data" / "copernicus-sentinel1.json"
# nomi variabili: scene Sentinel-2 (colori naturali e indici) e misure radar
# Sentinel-1 in decibel (una per passaggio, per il confronto a parita' di orbita)
S2_NOME = re.compile(r"sentinel2-genzano-\d{8}(-ndvi|-ndwi|-nbr)?\.webp")
S1_NOME = re.compile(r"sentinel1-genzano-db-\d{8}T\d{4}\.png")
VARIABILI = {"sentinel2": S2_NOME, "sentinel1": S1_NOME}


def _json(p: Path) -> dict:
    try:
        return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
    except ValueError:
        return {}


def file_attesi() -> dict[str, str]:
    """FILE più i nomi variabili elencati dai JSON (scene Sentinel-2, misure radar)."""
    attesi = dict(FILE)
    for s in _json(S2_JSON).get("scene", []):
        for percorso in [s.get("immagine", "")] + list((s.get("indici") or {}).get("immagini", {}).values()):
            nome = Path(str(percorso)).name
            if S2_NOME.fullmatch(nome):
                attesi[nome] = "images/sentinel/" + nome
    for r in _json(S1_JSON).get("storico", []):
        nome = Path(str(r.get("db", ""))).name
        if S1_NOME.fullmatch(nome):
            attesi[nome] = "images/sentinel/" + nome
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
    # una mappa dei cambiamenti quasi tutta trasparente pesa poche centinaia di byte
    if len(dati) < (120 if percorso.endswith("-cambi.webp") else 1000):
        print(f"  [ko ] {percorso} dal sito: risposta troppo piccola ({len(dati)} byte)")
        return False
    dest.write_bytes(dati)
    return True


def scarica(rigoroso: bool = False) -> int:
    # Anche il controllo dei link usa questo comando: il file deve esserci
    # sia nella produzione sia nelle build che ne verificano i collegamenti.
    if scarica_permanenti():
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        r = gh("release", "download", TAG, "--dir", tmp, "--clobber")
        if r.returncode != 0:
            print(f"Release {TAG} non disponibile ({r.stderr.strip()}): ripiego sul sito.")
        mancanti = []
        for nome, percorso in file_attesi().items():
            if rigoroso and S1_NOME.fullmatch(nome):
                continue  # le misure radar in decibel servono solo al generatore, non al sito
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
    if gruppo in VARIABILI:
        # i file usciti dall'archivio (scene piu' vecchie di MAX_SCENE, misure radar
        # oltre la finestra) si tolgono dalla release, altrimenti si accumulano per sempre
        tenute = set(file_attesi())
        for nome, aid in asset_release().items():
            if VARIABILI[gruppo].fullmatch(nome) and nome not in tenute:
                r = gh("api", "-X", "DELETE", f"repos/{repo_slug()}/releases/assets/{aid}")
                print(f"  {'[ok ]' if r.returncode == 0 else '[ko ]'} tolta dalla release: {nome}")
    return 0


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else ""
    if comando == "carica-permanenti":
        sys.exit(carica_permanenti())
    if comando == "scarica-permanenti":
        sys.exit(scarica_permanenti())
    if comando == "scarica":
        sys.exit(scarica(rigoroso="--rigoroso" in sys.argv))
    if comando == "carica" and len(sys.argv) > 2 and sys.argv[2] in ("ecmwf", "meteo-sinottica", "sinottica", "sentinel1", "sentinel2"):
        sys.exit(carica("meteo-sinottica" if sys.argv[2] == "sinottica" else sys.argv[2]))
    print(__doc__)
    sys.exit(2)
