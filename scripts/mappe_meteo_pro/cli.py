"""Punto di ingresso: scarica, elabora, disegna, anima e (facoltativo) pubblica."""

from __future__ import annotations

import argparse
import sys
import traceback
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*Downloading.*")
from datetime import datetime, timezone
from pathlib import Path

from .animazioni import scrivi_gif, scrivi_miniatura, scrivi_video
from .campi import carica_stato, stato_per_dominio
from .config import (
    DOMINI,
    MODELLI,
    ORE_ANTEPRIMA,
    ORE_STANDARD,
    PRODOTTI,
    RAMO_DATI,
)
from .prodotti import disegna_prodotto, requisiti_ok
from .pubblica import costruisci_manifesto, leggi_manifesto, pubblica_ramo, pulisci_corse_vecchie
from .scarica import ScaricoErrore, scarica_step, trova_corsa


def _parse_lista(val: str, ammessi: list[str], tutti_alias: tuple[str, ...] = ("tutti", "all", "")) -> list[str]:
    if val.strip().lower() in tutti_alias or val.strip() == "":
        return list(ammessi)
    pezzi = [p.strip() for p in val.split(",") if p.strip()]
    sconosciuti = [p for p in pezzi if p not in ammessi]
    if sconosciuti:
        raise SystemExit(f"Valori non riconosciuti: {', '.join(sconosciuti)}. Ammessi: {', '.join(ammessi)}")
    return pezzi


def _parse_ore(val: str, anteprima: bool) -> list[int]:
    if val.strip().lower() in {"standard", ""}:
        return list(ORE_ANTEPRIMA if anteprima else ORE_STANDARD)
    if val.strip().lower() == "anteprima":
        return list(ORE_ANTEPRIMA)
    pezzi = []
    for p in val.split(","):
        p = p.strip()
        if not p:
            continue
        if "-" in p:
            a, b = p.split("-", 1)
            if "/" in b:
                b, passo = b.split("/", 1)
                pezzi.extend(range(int(a), int(b) + 1, int(passo)))
            else:
                pezzi.extend(range(int(a), int(b) + 1, 6))
        else:
            pezzi.append(int(p))
    return sorted(set(pezzi))


def _union_extent(domini: list[str]) -> tuple[float, float, float, float]:
    lons0, lons1, lats0, lats1 = [], [], [], []
    for d in domini:
        a, b, c, e = DOMINI[d].get("bbox") or DOMINI[d]["extent"]
        lons0.append(a); lons1.append(b); lats0.append(c); lats1.append(e)
    return (min(lons0), max(lons1), min(lats0), max(lats1))


def _disegna_gruppo(args):
    """Lavoro di un processo: tutti i prodotti di uno step su un dominio."""
    stato, dominio, prodotti, uscita, etichetta_corsa = args
    fatti = []
    for pid in prodotti:
        rel_dir = Path(stato.modello) / dominio / pid / etichetta_corsa
        dest = Path(uscita) / rel_dir / f"f{stato.step:03d}.png"
        out = disegna_prodotto(pid, stato, dominio, dest)
        if out is not None:
            fatti.append((pid, stato.step, str(rel_dir / f"f{stato.step:03d}.png").replace("\\", "/"), str(out)))
    return dominio, fatti


def elabora_modello(modello: str, ore: list[int], domini: list[str], prodotti: list[str],
                    cache: Path, uscita: Path, corsa_forzata: datetime | None = None,
                    processi: int = 0) -> dict:
    import os
    from concurrent.futures import ProcessPoolExecutor

    print(f"\n=== {MODELLI[modello]['nome']} ===", flush=True)
    corsa = corsa_forzata or trova_corsa(modello)
    print(f"Corsa {corsa:%Y%m%d %H} UTC", flush=True)
    extent = _union_extent(domini)
    etichetta_corsa = corsa.strftime("%Y%m%d%H")
    acc_prec = None
    # Per la pioggia in 6 ore su ECMWF e ICON serve l'accumulo dello step precedente.
    ore_lavoro = sorted(set(list(ore) + [h - 6 for h in ore if h >= 6 and modello != "gfs"]))

    lavori = []
    for step in ore_lavoro:
        print(f"  F{step:03d}: prelievo…", flush=True)
        try:
            grib = scarica_step(modello, corsa, step, cache)
            stato = carica_stato(modello, corsa, step, grib, acc_prec_prec=acc_prec, extent=extent)
            acc_prec = stato.campi.get("_tp_acc_pieno", stato.campi.get("tp_acc"))
            if step in ore:
                pronti = [k for k in prodotti if requisiti_ok(stato, k)]
                print(f"         {grib.stat().st_size // 1024} KB, {len(pronti)}/{len(prodotti)} prodotti calcolabili", flush=True)
                for dominio in domini:
                    lavori.append((stato_per_dominio(stato, DOMINI[dominio]), dominio, pronti, str(uscita), etichetta_corsa))
            del stato
        except ScaricoErrore as e:
            print(f"         prelievo non riuscito: {e}", flush=True)
        except Exception as e:  # noqa: BLE001
            print(f"         elaborazione non riuscita: {e}", flush=True)
            traceback.print_exc()

    n = processi or max(1, (os.cpu_count() or 2))
    print(f"  disegno di {len(lavori)} gruppi con {n} processi…", flush=True)
    raccolti: dict[str, dict[str, list]] = {d: {} for d in domini}
    if n == 1:
        risultati = map(_disegna_gruppo, lavori)
    else:
        import multiprocessing as mp
        ctx = mp.get_context("fork")
        pool = ProcessPoolExecutor(max_workers=n, mp_context=ctx)
        risultati = pool.map(_disegna_gruppo, lavori)
    for dominio, fatti in risultati:
        for pid, step, rel, assoluto in fatti:
            raccolti[dominio].setdefault(pid, []).append((step, rel, Path(assoluto)))
    if n != 1:
        pool.shutdown()

    info = {"corsa": corsa, "domini": {d: {} for d in domini}}
    for dominio in domini:
        for pid in prodotti:
            elenco = sorted(raccolti[dominio].get(pid, []))
            if not elenco:
                continue
            percorsi = [x[2] for x in elenco]
            cartella = uscita / modello / dominio / pid / etichetta_corsa
            gif = scrivi_gif(percorsi, cartella / "animazione.gif")
            mini = scrivi_miniatura(percorsi[min(len(percorsi) // 2, len(percorsi) - 1)], cartella / "miniatura.jpg")
            video = scrivi_video(percorsi, cartella / "animazione.mp4")
            voce = {"fotogrammi": [(x[0], x[1]) for x in elenco]}
            if gif:
                voce["gif"] = str((cartella / "animazione.gif").relative_to(uscita)).replace("\\", "/")
            if mini:
                voce["miniatura"] = str((cartella / "miniatura.jpg").relative_to(uscita)).replace("\\", "/")
            for k, pth in video.items():
                voce[k] = str(pth.relative_to(uscita)).replace("\\", "/")
            info["domini"][dominio][pid] = voce
        print(f"  {dominio}: {len(info['domini'][dominio])} prodotti animati", flush=True)
    return info


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Genera le mappe meteo professionali per l'Italia a partire da dati aperti "
            "(GFS, ECMWF IFS/AIFS, ICON-EU)."
        )
    )
    p.add_argument("--modelli", default="gfs,ecmwf,icon-eu",
                   help="Elenco separato da virgola, oppure 'tutti'.")
    p.add_argument("--domini", default="tutti",
                   help="italia, europa, oppure tutti (ogni modello usa solo i domini previsti in config).")
    p.add_argument("--prodotti", default="tutti")
    p.add_argument("--ore", default="standard",
                   help="standard, anteprima, oppure 0,12,24 oppure 0-120/6")
    p.add_argument("--corsa", default="auto",
                   help="YYYYMMDDHH (UTC) oppure auto")
    p.add_argument("--cache", default="/tmp/mappe-meteo-cache")
    p.add_argument("--uscita", default="mappe-meteo-dati")
    p.add_argument("--anteprima", action="store_true",
                   help="Usa il sottoinsieme di ore corto (0-72 ogni 12).")
    p.add_argument("--pubblica", action="store_true",
                   help="Invia le carte sul ramo orfano mappe-meteo-dati (force-push, un solo commit).")
    p.add_argument("--forza", action="store_true",
                   help="Rielabora anche le corse già pubblicate.")
    p.add_argument("--svuota-cache", action="store_true",
                   help="Cancella i GRIB di un modello appena finito (utile sui runner con poco disco).")
    p.add_argument("--processi", type=int, default=0,
                   help="Processi per il disegno (0 = tutti i core).")
    p.add_argument("--repo", default=".",
                   help="Percorso del repository del sito, per il push del ramo dati.")
    args = p.parse_args(argv)

    modelli = _parse_lista(args.modelli, list(MODELLI.keys()))
    domini = _parse_lista(args.domini, list(DOMINI.keys()))
    prodotti = _parse_lista(args.prodotti, list(PRODOTTI.keys()))
    ore = _parse_ore(args.ore, args.anteprima)
    cache = Path(args.cache)
    uscita = Path(args.uscita)
    uscita.mkdir(parents=True, exist_ok=True)
    cache.mkdir(parents=True, exist_ok=True)

    corsa_forzata = None
    if args.corsa.lower() != "auto":
        corsa_forzata = datetime.strptime(args.corsa, "%Y%m%d%H").replace(tzinfo=timezone.utc)

    precedente = leggi_manifesto(uscita)
    gia = (precedente.get("modelli") or {})
    risultati = {}
    for mid in modelli:
        domini_mod = [d for d in domini if d in MODELLI[mid].get("domini", tuple(DOMINI))]
        if not domini_mod:
            continue
        try:
            corsa = corsa_forzata or trova_corsa(mid)
        except ScaricoErrore as e:
            print(f"Modello {mid} saltato: {e}", flush=True)
            continue
        if not args.forza and gia.get(mid, {}).get("corsa") == corsa.strftime("%Y%m%d%H"):
            print(f"{MODELLI[mid]['nome']}: corsa {corsa:%Y%m%d%H} già pubblicata, nessun lavoro.", flush=True)
            continue
        try:
            info = elabora_modello(
                mid, ore, domini_mod, prodotti, cache, uscita, corsa, args.processi,
            )
            if any(info["domini"].values()):
                risultati[mid] = info
            else:
                print(f"Modello {mid}: nessuna carta prodotta, resta la corsa precedente.", flush=True)
        except Exception as e:  # noqa: BLE001
            print(f"Modello {mid} interrotto: {e}", flush=True)
            traceback.print_exc()
        if args.svuota_cache:
            import shutil
            for sotto in cache.glob(f"{'ecmwf-' if mid.startswith('ecmwf') else mid}*"):
                shutil.rmtree(sotto, ignore_errors=True)

    if not risultati:
        if precedente:
            print("Nessuna corsa nuova: il ramo dati resta com'è.")
            return 0
        print("Nessun modello è stato elaborato.", file=sys.stderr)
        return 1

    manifesto = costruisci_manifesto(uscita, risultati, precedente=precedente)
    tolte = pulisci_corse_vecchie(uscita, manifesto)
    print(f"\nManifesto scritto in {uscita / 'manifesto.json'} (corse vecchie rimosse: {tolte})")
    if args.pubblica:
        sha = pubblica_ramo(uscita, Path(args.repo).resolve(), RAMO_DATI)
        print(f"Pubblicato sul ramo {RAMO_DATI} ({sha}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
