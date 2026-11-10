"""Manifesto JSON e pubblicazione sul ramo orfano `mappe-meteo-dati` (un solo commit, storia azzerata)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from .config import BASE_DATI_RAW, MANIFESTO_NOME, MODELLI, PRODOTTI, PRODOTTI_SALTATI, RAMO_DATI, data_italiana


def leggi_manifesto(uscita: Path) -> dict:
    p = uscita / MANIFESTO_NOME
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except ValueError:
        return {}


def _blocco_modello(mid: str, info: dict) -> dict:
    blocco = {
        "id": mid,
        "nome": MODELLI[mid]["nome"],
        "nome_lungo": MODELLI[mid]["nome_lungo"],
        "ente": MODELLI[mid]["ente"],
        "risoluzione": MODELLI[mid]["risoluzione"],
        "licenza": MODELLI[mid]["licenza"],
        "attribuzione": MODELLI[mid]["attribuzione"],
        "url_licenza": MODELLI[mid]["url_licenza"],
        "corsa": info["corsa"].strftime("%Y%m%d%H"),
        "init_iso": info["corsa"].strftime("%Y-%m-%dT%H:%M:%SZ"),
        "init_testo": data_italiana(info["corsa"]),
        "domini": {},
    }
    for dominio, prodotti in info.get("domini", {}).items():
        if not prodotti:
            continue
        blocco["domini"][dominio] = {"prodotti": {}}
        for pid, dati in prodotti.items():
            voce = {
                "id": pid,
                "titolo": PRODOTTI[pid]["titolo"],
                "sottotitolo": PRODOTTI[pid]["sottotitolo"],
                "ordine": PRODOTTI[pid]["ordine"],
                "fotogrammi": [{"ora": ora, "png": rel} for ora, rel in dati.get("fotogrammi", [])],
            }
            for k in ("gif", "mp4", "miniatura"):
                if dati.get(k):
                    voce[k] = dati[k]
            blocco["domini"][dominio]["prodotti"][pid] = voce
    return blocco


def costruisci_manifesto(uscita: Path, modelli_info: dict, generato: datetime | None = None,
                         precedente: dict | None = None) -> dict:
    """Scrive il manifesto: i modelli rielaborati aggiornano il loro blocco, gli altri restano.

    Se la corsa è la stessa, i prodotti appena generati si uniscono a quelli
    già presenti, così un giro parziale (`--prodotti`) non cancella le altre carte.
    """
    quando = generato or datetime.now(timezone.utc)
    modelli = dict((precedente or {}).get("modelli") or {})
    for mid, info in modelli_info.items():
        nuovo = _blocco_modello(mid, info)
        vecchio = modelli.get(mid)
        if vecchio and vecchio.get("corsa") == nuovo.get("corsa"):
            for dominio, dd in (vecchio.get("domini") or {}).items():
                dest = nuovo["domini"].setdefault(dominio, {"prodotti": {}})
                fusi = dict(dd.get("prodotti") or {})
                fusi.update(dest.get("prodotti") or {})
                dest["prodotti"] = fusi
        modelli[mid] = nuovo
    # Un modello tolto dalla configurazione esce anche dal manifesto.
    modelli = {k: v for k, v in modelli.items() if k in MODELLI}
    manifesto = {
        "versione": 1,
        "generato": quando.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generato_testo": data_italiana(quando),
        "base_url": BASE_DATI_RAW,
        "prodotti_saltati": PRODOTTI_SALTATI,
        "modelli": modelli,
    }
    dest = uscita / MANIFESTO_NOME
    dest.write_text(json.dumps(manifesto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifesto


def pulisci_corse_vecchie(uscita: Path, manifesto: dict) -> int:
    """Toglie dalla cartella le corse che il manifesto non cita più (resta solo l'ultima per modello)."""
    tenute = set()
    for mid, m in (manifesto.get("modelli") or {}).items():
        for dominio, dd in (m.get("domini") or {}).items():
            for pid in (dd.get("prodotti") or {}):
                tenute.add((mid, dominio, pid, m.get("corsa")))
    tolte = 0
    for mid_dir in [p for p in uscita.iterdir() if p.is_dir() and not p.name.startswith(".")]:
        for dom_dir in [p for p in mid_dir.iterdir() if p.is_dir()]:
            for pid_dir in [p for p in dom_dir.iterdir() if p.is_dir()]:
                for corsa_dir in [p for p in pid_dir.iterdir() if p.is_dir()]:
                    if (mid_dir.name, dom_dir.name, pid_dir.name, corsa_dir.name) not in tenute:
                        shutil.rmtree(corsa_dir)
                        tolte += 1
                if not any(pid_dir.iterdir()):
                    pid_dir.rmdir()
            if not any(dom_dir.iterdir()):
                dom_dir.rmdir()
        if not any(mid_dir.iterdir()):
            mid_dir.rmdir()
    return tolte


def _git(args: list[str], cwd: Path, env: dict | None = None) -> subprocess.CompletedProcess:
    e = os.environ.copy()
    if env:
        e.update(env)
    return subprocess.run(["git", *args], cwd=str(cwd), env=e, text=True, capture_output=True)


def url_remoto(repo: Path) -> str:
    """URL del repository. In GitHub Actions si usa il GITHUB_TOKEN del giro (mai salvato su disco)."""
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    slug = os.environ.get("GITHUB_REPOSITORY")
    if os.environ.get("GITHUB_ACTIONS") and token and slug:
        return f"https://x-access-token:{token}@github.com/{slug}.git"
    r = _git(["remote", "get-url", "origin"], repo)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "Remote origin assente")
    return r.stdout.strip()


def pubblica_ramo(uscita: Path, repo: Path, ramo: str = RAMO_DATI) -> str:
    """Pubblica `uscita` sul ramo orfano con un solo commit (storia azzerata, force-push).

    Se il ramo esiste già, lo si scarica prima (profondità 1): così git sa quali
    file il server ha già e invia solo le immagini nuove. Non tocca `main` e
    non avvia il deploy del sito.
    """
    uscita = uscita.resolve()
    if not (uscita / MANIFESTO_NOME).is_file():
        raise RuntimeError("Manca il manifesto, non pubblico un ramo vuoto.")
    remoto = url_remoto(repo)
    env = {
        "GIT_AUTHOR_NAME": "github-actions[bot]",
        "GIT_AUTHOR_EMAIL": "github-actions[bot]@users.noreply.github.com",
        "GIT_COMMITTER_NAME": "github-actions[bot]",
        "GIT_COMMITTER_EMAIL": "github-actions[bot]@users.noreply.github.com",
    }
    if not os.environ.get("GITHUB_ACTIONS"):
        nome = _git(["config", "user.name"], repo).stdout.strip()
        mail = _git(["config", "user.email"], repo).stdout.strip()
        if nome:
            env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = nome
        if mail:
            env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = mail

    readme = (
        "Mappe meteo professionali generate in automatico per il sito "
        "della Protezione Civile di Genzano di Roma.\n\n"
        "Questo ramo è orfano e viene sovrascritto a ogni aggiornamento: non contiene "
        "il sito e non va modificato a mano. Le carte arrivano da dati aperti "
        "(NOAA GFS, ECMWF Open Data CC BY 4.0, DWD ICON-EU dl-de/by-2-0).\n"
    )
    (uscita / "README.md").write_text(readme, encoding="utf-8")

    with tempfile.TemporaryDirectory(prefix="mappe-meteo-ramo-") as tmp:
        tmp_p = Path(tmp)
        _git(["init", "-q"], tmp_p)
        _git(["remote", "add", "origin", remoto], tmp_p)
        # Commit attuale del ramo, se esiste: serve solo a non reinviare i file già presenti.
        prec = _git(["fetch", "-q", "--depth", "1", "origin", ramo], tmp_p)
        _git(["checkout", "-q", "--orphan", "pubblica"], tmp_p)
        # copia senza un eventuale .git di `uscita` (non deve sovrascrivere quello temporaneo)
        shutil.copytree(uscita, tmp_p, dirs_exist_ok=True, ignore=shutil.ignore_patterns(".git"))
        _git(["add", "-A", "--", "."], tmp_p)
        r = _git(["commit", "-q", "-m", "Aggiorna le mappe meteo professionali"], tmp_p, env=env)
        if r.returncode != 0:
            raise RuntimeError(r.stderr or r.stdout or "Commit sul ramo dati non riuscito")
        sha = _git(["rev-parse", "HEAD"], tmp_p).stdout.strip()
        r = _git(["push", "-q", "--force", "origin", f"HEAD:refs/heads/{ramo}"], tmp_p)
        if r.returncode != 0:
            errore = (r.stderr or r.stdout or "Push del ramo dati non riuscito")
            token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
            raise RuntimeError(errore.replace(token, "***") if token else errore)
        stato = "aggiornato" if prec.returncode == 0 else "creato"
        print(f"Ramo {ramo} {stato} ({sha[:12]}).")
        return sha
