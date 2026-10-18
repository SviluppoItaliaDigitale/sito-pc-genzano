#!/usr/bin/env python3
"""Manutenzione straordinaria autorizzata il 18/10/2026: solo output storici.

Salva tutti i rami e tag in una Release indipendente, verifica ogni parte
riscaricandola, simula la riscrittura e confronta i contenuti. L'applicazione
usa un unico push atomico con lease su ogni riferimento; nessun file del sito
o delle richieste aperte può cambiare. Le protezioni GitHub restano in vigore.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import urllib.request

REPO = "SviluppoItaliaDigitale/sito-pc-genzano"
URL = f"https://github.com/{REPO}.git"
PERCORSI = (
    "static/pagefind/", "static/images/ecmwf/",
    "static/images/meteo-sinottica-italia.webp",
    "static/images/meteo-sinottica-italia.png", "static/open-kit/",
)
FILTRO_SHA = "d7b75aca907380f608892cc289e616f195427b99"
FILTRO_HASH = "39d35fb2c35637a9d555353b6a8b53a223a227d3beb61a0ac7e1180bfa5572f1"


def run(args, cwd=None, data=None):
    r = subprocess.run(args, cwd=cwd, input=data, capture_output=True)
    if r.returncode:
        raise RuntimeError(f"{args[0]}: {r.stderr.decode(errors='replace')[-6000:]}")
    return r.stdout


def git(repo, *args, data=None):
    return run(["git", "-C", str(repo), *args], data=data)


def api(path):
    return json.loads(run(["gh", "api", f"repos/{REPO}/{path}"]))


def refs(repo, remote=False):
    data = (git(repo, "ls-remote", "--heads", "--tags", "--refs", "origin") if remote
            else git(repo, "for-each-ref", "--format=%(objectname) %(refname)", "refs/heads", "refs/tags"))
    return {line.split()[1]: line.split()[0] for line in data.decode().splitlines()}


def tree(repo, ref):
    return git(repo, "rev-parse", f"{ref}^{{tree}}").decode().strip()


def escluso(path):
    return any(path.startswith(p) if p.endswith("/") else path == p for p in PERCORSI)


def contenuti(repo, ref):
    dati = git(repo, "ls-tree", "-r", "-z", ref)
    return {p: meta for voce in dati.split(b"\0") if voce
            for meta, p in [voce.split(b"\t", 1)] if not escluso(p.decode())}


def aperte():
    prs = api("pulls?state=open&per_page=100")
    if len(prs) >= 100:
        raise RuntimeError("Troppe richieste aperte per questa manutenzione.")
    if any(p["head"]["repo"]["full_name"] != REPO or p["base"]["ref"] != "main" for p in prs):
        raise RuntimeError("Una richiesta aperta necessita di coordinamento separato.")
    return sorted((p["number"], p["head"]["ref"], p["head"]["sha"]) for p in prs)


def impronta(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for blocco in iter(lambda: f.read(1024 * 1024), b""):
            h.update(blocco)
    return h.hexdigest()


def pack_bytes(repo):
    return sum(p.stat().st_size for p in (repo / "objects" / "pack").glob("*.pack"))


def pubblica(tag, path):
    run(["gh", "release", "upload", tag, str(path), "--repo", REPO])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--applica", action="store_true")
    args = ap.parse_args()
    if os.environ.get("GITHUB_REPOSITORY") != REPO:
        raise RuntimeError("Eseguire solo nel repository autorizzato.")
    os.environ.update({"GIT_AUTHOR_NAME": "Alessandro Cuollo", "GIT_COMMITTER_NAME": "Alessandro Cuollo",
                       "GIT_AUTHOR_EMAIL": "65465537+SviluppoItaliaDigitale@users.noreply.github.com",
                       "GIT_COMMITTER_EMAIL": "65465537+SviluppoItaliaDigitale@users.noreply.github.com"})
    run(["gh", "auth", "setup-git"])
    with tempfile.TemporaryDirectory(prefix="manutenzione-git-") as tmp:
        root = Path(tmp)
        source, clean, archivio = root / "originale.git", root / "ripulito.git", root / "backup"
        archivio.mkdir()
        run(["git", "init", "--bare", str(source)])
        git(source, "remote", "add", "origin", URL)
        git(source, "fetch", "--quiet", "origin", "+refs/heads/*:refs/heads/*", "+refs/tags/*:refs/tags/*")
        git(source, "symbolic-ref", "HEAD", "refs/heads/main")
        originali = refs(source)
        if refs(source, remote=True) != originali:
            raise RuntimeError("I riferimenti sono cambiati durante l'acquisizione; nessuna modifica remota.")
        prs = aperte()
        for _, ramo, sha in prs:
            if originali.get("refs/heads/" + ramo) != sha:
                raise RuntimeError("Richiesta aperta cambiata durante l'acquisizione.")
        main_ref = originali["refs/heads/main"]
        main_tree = tree(source, "refs/heads/main")
        source_bytes = pack_bytes(source)
        print(f"Acquisiti {len(originali)} rami e tag; main {main_ref}; pack {source_bytes} byte.", flush=True)

        # La copia completa precede ogni riscrittura e conserva tutti i riferimenti.
        bundle = root / "repository.bundle"
        git(source, "bundle", "create", str(bundle), "--all")
        git(source, "bundle", "verify", str(bundle))
        parti = []
        with bundle.open("rb") as src:
            numero = 0
            while True:
                blocco = src.read(1024 * 1024)
                if not blocco:
                    break
                parte = archivio / f"repository.bundle.part-{numero:03d}"
                with parte.open("wb") as dest:
                    dest.write(blocco)
                    for _ in range(1023):
                        blocco = src.read(1024 * 1024)
                        if not blocco:
                            break
                        dest.write(blocco)
                parti.append(parte)
                numero += 1
        bundle.unlink()  # solo il file temporaneo duplicato; le parti restano integre
        (archivio / "riferimenti-originali.json").write_text(json.dumps(originali, indent=2))
        (archivio / "RIPRISTINO.txt").write_text(
            "Backup completo dei rami e tag prima della manutenzione del 18/10/2026.\n"
            "Verificare: sha256sum -c SHA256SUMS\n"
            "Ricostruire: cat repository.bundle.part-* > repository.bundle\n"
            "Verificare: git bundle verify repository.bundle\n"
            "Recuperare: git clone --mirror repository.bundle recupero.git\n"
            "I riferimenti originali sono in riferimenti-originali.json.\n"
            "Non pubblicare o sovrascrivere riferimenti senza verificare i lavori successivi.\n")
        sums = {p.name: impronta(p) for p in archivio.iterdir()}
        (archivio / "SHA256SUMS").write_text("".join(f"{h}  {n}\n" for n, h in sorted(sums.items())))

        # Il tag del backup punta a una radice vuota: non trattiene lo storico.
        tag = (f"backup-storico-20261018-{os.environ['GITHUB_RUN_ID']}"
               f"-{os.environ.get('GITHUB_RUN_ATTEMPT', '1')}")
        empty = git(source, "mktree", data=b"").decode().strip()
        orphan = git(source, "commit-tree", empty, data=b"Copia di sicurezza della cronologia prima della manutenzione\n").decode().strip()
        git(source, "push", "origin", f"{orphan}:refs/tags/{tag}")
        run(["gh", "release", "create", tag, "--repo", REPO, "--latest=false",
             "--title", "Backup completo prima della pulizia dello storico",
             "--notes-file", str(archivio / "RIPRISTINO.txt")])
        for path in sorted(archivio.iterdir()):
            pubblica(tag, path)
        verifiche = {**sums, "SHA256SUMS": impronta(archivio / "SHA256SUMS")}
        for nome, attesa in verifiche.items():
            with tempfile.TemporaryDirectory(dir=root) as verifica:
                run(["gh", "release", "download", tag, "--repo", REPO, "--pattern", nome, "--dir", verifica])
                if impronta(Path(verifica) / nome) != attesa:
                    raise RuntimeError(f"Backup remoto diverso: {nome}; applicazione annullata.")
            print(f"Backup remoto verificato: {nome}", flush=True)
        print(f"BACKUP_COMPLETO_VERIFICATO https://github.com/{REPO}/releases/tag/{tag}", flush=True)

        run(["git", "clone", "--mirror", "--quiet", str(source), str(clean)])
        filtro = root / "git-filter-repo"
        with urllib.request.urlopen(f"https://raw.githubusercontent.com/newren/git-filter-repo/{FILTRO_SHA}/git-filter-repo", timeout=30) as r:
            filtro.write_bytes(r.read())
        if impronta(filtro) != FILTRO_HASH:
            raise RuntimeError("Versione dello strumento non verificata.")
        cmd = ["python3", str(filtro), "--force", "--invert-paths", "--prune-empty", "never",
               "--prune-degenerate", "never", "--preserve-commit-hashes"]
        for path in PERCORSI:
            cmd.extend(["--path", path])
        run(cmd, cwd=clean)
        dopo = refs(clean)
        if set(dopo) != set(originali):
            raise RuntimeError("Elenco di rami o tag cambiato nella simulazione.")
        for ref in originali:
            if contenuti(source, ref) != contenuti(clean, ref):
                raise RuntimeError(f"Contenuti non tecnici diversi: {ref}.")
        if tree(clean, "refs/heads/main") != main_tree:
            raise RuntimeError("Il tree attuale del sito è cambiato: applicazione annullata.")
        for numero, ramo, _ in prs:
            ref = "refs/heads/" + ramo
            if tree(source, ref) != tree(clean, ref):
                raise RuntimeError(f"Contenuti della richiesta {numero} cambiati.")
            for separatore in ("..", "..."):
                confronto = "refs/heads/main" + separatore + ref
                if git(source, "diff", "--binary", confronto) != git(clean, "diff", "--binary", confronto):
                    raise RuntimeError(f"Differenze della richiesta {numero} cambiate.")
        git(clean, "fsck", "--connectivity-only", "--no-dangling")
        clean_bytes = pack_bytes(clean)
        report = {"prima_main": main_ref, "dopo_main": dopo["refs/heads/main"], "tree_main_identico": main_tree,
                  "rami_tag_verificati": len(originali), "richieste_verificate": [p[0] for p in prs],
                  "pack_prima_byte": source_bytes, "pack_dopo_byte": clean_bytes,
                  "riduzione_pack_byte": source_bytes - clean_bytes, "percorsi_storici": PERCORSI,
                  "backup": tag, "applicato": False}
        if clean_bytes >= source_bytes:
            raise RuntimeError("Nessuna riduzione misurata: applicazione annullata.")
        print("SIMULAZIONE_VERIFICATA " + json.dumps(report), flush=True)
        for nome in ("commit-map", "ref-map"):
            p = clean / "filter-repo" / nome
            if p.is_file():
                pubblica(tag, p)
        preliminare = root / "simulazione.json"
        preliminare.write_text(json.dumps(report, indent=2))
        pubblica(tag, preliminare)
        if not args.applica:
            return 0

        # Nessun lavoro intervenuto nel frattempo può essere sovrascritto.
        attesi_remoti = {**originali, f"refs/tags/{tag}": orphan}
        if refs(source, remote=True) != attesi_remoti or aperte() != prs:
            raise RuntimeError("Rami, tag o richieste cambiati durante il backup: nessuna riscrittura remota.")
        git(clean, "remote", "add", "origin", URL)
        # Gli oggetti originali servono soltanto alla negoziazione del push:
        # impediscono di ritrasmettere i blob già presenti su GitHub.
        (clean / "objects" / "info" / "alternates").write_text(str(source / "objects") + "\n")
        cambiati = [r for r in originali if originali[r] != dopo[r]]
        comando = ["git", "-C", str(clean), "push", "--atomic"]
        comando += [f"--force-with-lease={r}:{originali[r]}" for r in cambiati]
        comando += ["origin"] + [f"{dopo[r]}:{r}" for r in cambiati]
        print(f"Applicazione atomica di {len(cambiati)} riferimenti con contenuti verificati.", flush=True)
        run(comando)
        if refs(clean, remote=True) != {**dopo, f"refs/tags/{tag}": orphan}:
            raise RuntimeError("Controllare i riferimenti remoti dopo l'applicazione.")
        report["applicato"] = True
        esito = root / "esito.json"
        esito.write_text(json.dumps(report, indent=2))
        pubblica(tag, esito)
        print("PULIZIA_COMPLETATA " + json.dumps(report), flush=True)
        # Questo dispatch richiama la normale pubblicazione, con priorità bassa.
        run(["gh", "workflow", "run", "deploy.yml", "--repo", REPO, "--ref", "main", "-f", "priority=background"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
