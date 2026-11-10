"""Prelievo dei GRIB da fonti aperte: GFS (NOMADS, con riserva AWS), ECMWF Open Data, ICON-EU (DWD)."""

from __future__ import annotations

import bz2
import io
import json
import re
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable

from .config import LIVELLI_HPA, MODELLI, SCARICO_EXTENT, USER_AGENT

# Timeout e tentativi: NOMADS a volte è lento, DWD e ECMWF di solito no.
TIMEOUT = 120
TENTATIVI = 4
PAUSA = 4


class ScaricoErrore(RuntimeError):
    """Prelievo fallito dopo i tentativi previsti."""


def _req(url: str, headers: dict | None = None, range_bytes: tuple[int, int] | None = None):
    h = {"User-Agent": USER_AGENT}
    if headers:
        h.update(headers)
    if range_bytes:
        h["Range"] = f"bytes={range_bytes[0]}-{range_bytes[1]}"
    return urllib.request.Request(url, headers=h)


def scarica_bytes(url: str, range_bytes: tuple[int, int] | None = None) -> bytes:
    ultimo = None
    for i in range(TENTATIVI):
        try:
            with urllib.request.urlopen(_req(url, range_bytes=range_bytes), timeout=TIMEOUT) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            ultimo = e
            time.sleep(PAUSA * (i + 1))
    raise ScaricoErrore(f"Prelievo non riuscito: {url} ({ultimo})")


def testa_url(url: str) -> bool:
    try:
        with urllib.request.urlopen(_req(url), timeout=30) as r:
            r.read(16)
            return True
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


def _scrivi_atomico(path: Path, dati: bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(dati)
    tmp.replace(path)
    return path


def file_pronto(path: Path, minimo: int = 100) -> bool:
    return path.is_file() and path.stat().st_size >= minimo


# ---------------------------------------------------------------------------
# GFS (NOAA)
# ---------------------------------------------------------------------------

GFS_NOMADS = "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl"
GFS_NOMADS_IDX = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod"
GFS_AWS = "https://noaa-gfs-bdp-pds.s3.amazonaws.com"

# Livelli e variabili per il filtro NOMADS (griglia già ritagliata sul dominio).
_GFS_LIVELLI_MB = tuple(f"{lv}_mb" for lv in LIVELLI_HPA)
_GFS_FILTRO = {
    "PRMSL": ("mean_sea_level",),
    "TMP": ("2_m_above_ground",) + _GFS_LIVELLI_MB,
    "UGRD": ("10_m_above_ground",) + _GFS_LIVELLI_MB,
    "VGRD": ("10_m_above_ground",) + _GFS_LIVELLI_MB,
    "HGT": _GFS_LIVELLI_MB,
    "VVEL": _GFS_LIVELLI_MB,
    "SPFH": _GFS_LIVELLI_MB,
    "RH": _GFS_LIVELLI_MB,
    "ABSV": _GFS_LIVELLI_MB,
    "CAPE": ("surface",),
    "PWAT": ("entire_atmosphere_(considered_as_a_single_layer)",),
    "APCP": ("surface",),
}

# Chiavi da cercare nell'idx AWS (sottostringhe sul 4° e 5° campo).
_GFS_IDX_CERCA = (
    ("PRMSL", "mean sea level"),
    ("TMP", "2 m above ground"),
    ("UGRD", "10 m above ground"),
    ("VGRD", "10 m above ground"),
    ("CAPE", "surface"),
    ("PWAT", "entire atmosphere"),
    ("APCP", "surface"),
) + tuple(
    (nome, f"{lv} mb")
    for nome in ("TMP", "UGRD", "VGRD", "HGT", "VVEL", "SPFH", "RH", "ABSV")
    for lv in LIVELLI_HPA
)


def ultime_corse_possibili(corse_utc: Iterable[int], ritardo_ore: float, quante: int = 8):
    """Genera le corse più recenti, dalla più nuova, tenendo conto del ritardo di pubblicazione."""
    adesso = datetime.now(timezone.utc) - timedelta(hours=ritardo_ore)
    trovate = []
    giorno = adesso.replace(minute=0, second=0, microsecond=0)
    # allinea all'ora di corsa più vicina verso il passato
    while len(trovate) < quante:
        if giorno.hour in set(corse_utc):
            trovate.append(giorno)
        giorno -= timedelta(hours=1)
    return trovate


def trova_corsa_gfs(cache: Path) -> datetime:
    for corsa in ultime_corse_possibili(MODELLI["gfs"]["corse_utc"], 4.0):
        d, h = corsa.strftime("%Y%m%d"), f"{corsa.hour:02d}"
        # l'indice dell'ultimo step (+120) garantisce che la corsa sia completa fin lì
        idx = f"{GFS_NOMADS_IDX}/gfs.{d}/{h}/atmos/gfs.t{h}z.pgrb2.0p25.f120.idx"
        aws = f"{GFS_AWS}/gfs.{d}/{h}/atmos/gfs.t{h}z.pgrb2.0p25.f120.idx"
        if testa_url(idx) or testa_url(aws):
            return corsa
    raise ScaricoErrore("Nessuna corsa GFS recente risulta disponibile.")


def _url_filtro_gfs(corsa: datetime, step: int) -> str:
    d, h, fxx = corsa.strftime("%Y%m%d"), f"{corsa.hour:02d}", f"{step:03d}"
    file = f"gfs.t{h}z.pgrb2.0p25.f{fxx}"
    pezzi = [
        f"{GFS_NOMADS}?dir=%2Fgfs.{d}%2F{h}%2Fatmos",
        f"file={file}",
    ]
    for var, livelli in _GFS_FILTRO.items():
        pezzi.append(f"var_{var}=on")
        for lv in livelli:
            pezzi.append(f"lev_{lv}=on")
    lon0, lon1, lat0, lat1 = SCARICO_EXTENT
    pezzi += [
        "subregion=",
        f"leftlon={lon0}",
        f"rightlon={lon1}",
        f"toplat={lat1}",
        f"bottomlat={lat0}",
    ]
    return "&".join(pezzi)


def _gfs_idx_s3(corsa: datetime, step: int) -> tuple[str, str]:
    d, h, fxx = corsa.strftime("%Y%m%d"), f"{corsa.hour:02d}", f"{step:03d}"
    base = f"{GFS_AWS}/gfs.{d}/{h}/atmos/gfs.t{h}z.pgrb2.0p25.f{fxx}"
    return base, base + ".idx"


def _seleziona_intervalli_idx(idx_txt: str) -> list[tuple[int, int]]:
    """Intervalli byte da scaricare, in base all'indice wgrib2 del GFS."""
    righe = [ln for ln in idx_txt.splitlines() if ln.strip()]
    partenze = []
    for ln in righe:
        campi = ln.split(":")
        try:
            start = int(campi[1])
        except (IndexError, ValueError):
            continue
        nome = campi[3] if len(campi) > 3 else ""
        livello = campi[4] if len(campi) > 4 else ""
        tiene = any(nome == n and (s in livello) for n, s in _GFS_IDX_CERCA)
        partenze.append((start, tiene, ln))
    intervalli = []
    for i, (start, tiene, _) in enumerate(partenze):
        if not tiene:
            continue
        if i + 1 < len(partenze):
            fine = partenze[i + 1][0] - 1
        else:
            # ultimo messaggio: scarichiamo un blocco largo, il server chiude al EOF
            fine = start + 8_000_000
        intervalli.append((start, fine))
    return intervalli


def scarica_gfs_step(corsa: datetime, step: int, cache: Path) -> Path:
    dest = cache / "gfs" / corsa.strftime("%Y%m%d%H") / f"f{step:03d}.grib2"
    if file_pronto(dest, 10_000):
        return dest
    # 1) filtro NOMADS (griglia già ritagliata, pochi megabyte)
    try:
        dati = scarica_bytes(_url_filtro_gfs(corsa, step))
        if len(dati) > 10_000 and (dati[:4] == b"GRIB" or b"GRIB" in dati[:20]):
            return _scrivi_atomico(dest, dati)
        # NOMADS a volte risponde HTML di errore
        if len(dati) < 10_000 or dati.lstrip().startswith(b"<"):
            raise ScaricoErrore("Risposta NOMADS non valida")
        return _scrivi_atomico(dest, dati)
    except ScaricoErrore:
        pass
    # 2) riserva: AWS, solo i messaggi che servono (file globale, più pesante)
    base, idx_url = _gfs_idx_s3(corsa, step)
    idx_txt = scarica_bytes(idx_url).decode("utf-8", "replace")
    intervalli = _seleziona_intervalli_idx(idx_txt)
    if not intervalli:
        raise ScaricoErrore(f"Indice AWS GFS senza campi utili: {idx_url}")
    pezzi = []
    for a, b in intervalli:
        pezzi.append(scarica_bytes(base, range_bytes=(a, b)))
    dati = b"".join(pezzi)
    if len(dati) < 10_000:
        raise ScaricoErrore("Prelievo AWS GFS troppo piccolo")
    return _scrivi_atomico(dest, dati)


# ---------------------------------------------------------------------------
# ECMWF Open Data (IFS e AIFS)
# ---------------------------------------------------------------------------

def trova_corsa_ecmwf(modello: str = "ecmwf") -> datetime:
    """Cerca la corsa più recente con un indice pubblico (0,25°)."""
    # IFS e AIFS: 00/06/12/18. L'IFS 00/12 esce più tardi; 06/18 è più corto ma esiste.
    if modello == "ecmwf-aifs":
        modello_path, ritardo = "aifs-single", 5.0
    else:
        modello_path, ritardo = "ifs", 6.5
    radici = (
        "https://data.ecmwf.int/forecasts",
        "https://ecmwf-forecasts.s3.eu-central-1.amazonaws.com",
    )
    for corsa in ultime_corse_possibili(MODELLI[modello]["corse_utc"], ritardo):
        d, h = corsa.strftime("%Y%m%d"), f"{corsa.hour:02d}"
        # indice dello step +120: la corsa è completa almeno fin lì
        for radice in radici:
            url = (
                f"{radice}/{d}/{h}z/{modello_path}/0p25/oper/"
                f"{d}{h}0000-120h-oper-fc.index"
            )
            if testa_url(url):
                return corsa
    raise ScaricoErrore(f"Nessuna corsa ECMWF ({modello}) recente risulta disponibile.")


_ECMWF_SFC = ["msl", "2t", "10u", "10v", "tp", "tcwv", "mucape"]
_ECMWF_PL = ["gh", "t", "u", "v", "w", "q", "r", "vo"]
_ECMWF_AIFS_SFC = ["msl", "2t", "10u", "10v", "tp", "tcw"]
_ECMWF_AIFS_PL = ["gh", "t", "u", "v", "w", "q"]


def _ecmwf_retrieve(client, kw: dict, dest: Path) -> None:
    ultimo = None
    for i in range(TENTATIVI):
        try:
            try:
                client.retrieve(**kw, target=str(dest))
            except TypeError:
                kw = {k: v for k, v in kw.items() if k != "resol"}
                client.retrieve(**kw, target=str(dest))
            if file_pronto(dest, 5_000):
                return
            raise ScaricoErrore("File ECMWF troppo piccolo")
        except Exception as e:  # noqa: BLE001 — si ritenta, poi si alza in modo pulito
            ultimo = e
            time.sleep(PAUSA * (i + 1))
    raise ScaricoErrore(f"Prelievo ECMWF non riuscito: {ultimo}")


def scarica_ecmwf_step(corsa: datetime, step: int, cache: Path, modello: str = "ecmwf") -> Path:
    """Due richieste (superficie e livelli di pressione) concatenate in un solo GRIB.

    Con `levelist` il client scarta i campi al suolo, quindi vanno chiesti a parte.
    """
    aifs = modello == "ecmwf-aifs"
    etichetta = "aifs" if aifs else "ifs"
    cartella = cache / f"ecmwf-{etichetta}" / corsa.strftime("%Y%m%d%H")
    dest = cartella / f"f{step:03d}.grib2"
    if file_pronto(dest, 10_000):
        return dest
    from ecmwf.opendata import Client

    cartella.mkdir(parents=True, exist_ok=True)
    client = Client(source="ecmwf", model="aifs-single" if aifs else "ifs")
    base = {
        "date": int(corsa.strftime("%Y%m%d")),
        "time": corsa.hour,
        "step": step,
        "type": "fc",
        "stream": "oper",
        "model": "aifs-single" if aifs else "ifs",
    }
    if not aifs:
        base["resol"] = "0p25"
    sfc = cartella / f"f{step:03d}.sfc.grib2"
    pl = cartella / f"f{step:03d}.pl.grib2"
    if not file_pronto(sfc, 5_000):
        _ecmwf_retrieve(client, dict(base, param=_ECMWF_AIFS_SFC if aifs else _ECMWF_SFC), sfc)
    if not file_pronto(pl, 5_000):
        _ecmwf_retrieve(client, dict(base, param=_ECMWF_AIFS_PL if aifs else _ECMWF_PL,
                                     levelist=list(LIVELLI_HPA)), pl)
    dati = sfc.read_bytes() + pl.read_bytes()
    _scrivi_atomico(dest, dati)
    for f in (sfc, pl):
        try:
            f.unlink()
        except OSError:
            pass
    return dest


# ---------------------------------------------------------------------------
# ICON-EU (DWD)
# ---------------------------------------------------------------------------

DWD = "https://opendata.dwd.de/weather/nwp/icon-eu/grib"

# Parametri di pressione e al suolo. I nomi cartella sono minuscoli, il file è maiuscolo.
ICON_PL = {
    "t": "T",
    "u": "U",
    "v": "V",
    "fi": "FI",
    "qv": "QV",
    "relhum": "RELHUM",
    "omega": "OMEGA",
}
ICON_SFC = {
    "pmsl": "PMSL",
    "tot_prec": "TOT_PREC",
    "cape_ml": "CAPE_ML",
    "tqv": "TQV",
    "u_10m": "U_10M",
    "v_10m": "V_10M",
}
# Livelli ICON-EU tipicamente pubblicati (alcuni possono mancare: si ignora il 404).
ICON_LIVELLI = (1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100)


def _icon_url(corsa: datetime, step: int, cartella: str, nome: str, livello: int | None) -> str:
    dth = corsa.strftime("%Y%m%d%H")
    hh = f"{corsa.hour:02d}"
    if livello is None:
        fn = f"icon-eu_europe_regular-lat-lon_single-level_{dth}_{step:03d}_{nome}.grib2.bz2"
    else:
        fn = (
            f"icon-eu_europe_regular-lat-lon_pressure-level_{dth}_"
            f"{step:03d}_{livello}_{nome}.grib2.bz2"
        )
    return f"{DWD}/{hh}/{cartella}/{fn}"


def trova_corsa_icon_eu() -> datetime:
    for corsa in ultime_corse_possibili(MODELLI["icon-eu"]["corse_utc"], 3.5):
        # l'ultimo step dell'orizzonte garantisce che la corsa sia completa
        url = _icon_url(corsa, 120, "pmsl", "PMSL", None)
        if testa_url(url):
            return corsa
    raise ScaricoErrore("Nessuna corsa ICON-EU recente risulta disponibile.")


def _scarica_icon_uno(url: str, dest_grib: Path) -> Path | None:
    if file_pronto(dest_grib, 200):
        return dest_grib
    try:
        grezzo = scarica_bytes(url)
    except ScaricoErrore:
        return None
    # I file DWD sono bz2; se arrivasse già scompattato, lo teniamo com'è.
    if grezzo[:3] == b"BZh":
        try:
            grezzo = bz2.decompress(grezzo)
        except OSError:
            return None
    if b"GRIB" not in grezzo[:20] and grezzo[:4] != b"GRIB":
        return None
    return _scrivi_atomico(dest_grib, grezzo)


def scarica_icon_eu_step(corsa: datetime, step: int, cache: Path) -> Path:
    """Scarica i campi di uno step e li concatena in un unico GRIB."""
    dest = cache / "icon-eu" / corsa.strftime("%Y%m%d%H") / f"f{step:03d}.grib2"
    if file_pronto(dest, 50_000):
        return dest
    pezzi_dir = dest.parent / f"f{step:03d}.d"
    pezzi_dir.mkdir(parents=True, exist_ok=True)
    lavori = []
    for cartella, nome in ICON_SFC.items():
        url = _icon_url(corsa, step, cartella, nome, None)
        lavori.append((url, pezzi_dir / f"sfc_{nome}.grib2"))
    for cartella, nome in ICON_PL.items():
        for lv in ICON_LIVELLI:
            url = _icon_url(corsa, step, cartella, nome, lv)
            lavori.append((url, pezzi_dir / f"pl_{nome}_{lv}.grib2"))

    ok = 0
    with ThreadPoolExecutor(max_workers=16) as pool:
        fut = {pool.submit(_scarica_icon_uno, u, p): p for u, p in lavori}
        for f in as_completed(fut):
            if f.result() is not None:
                ok += 1
    if ok < 8:
        raise ScaricoErrore(
            f"ICON-EU: solo {ok} campi su {len(lavori)} per la corsa "
            f"{corsa:%Y%m%d%H} step {step}."
        )
    # Concatena i GRIB (ogni file è un messaggio autonomo).
    buf = io.BytesIO()
    for _u, p in lavori:
        if file_pronto(p, 200):
            buf.write(p.read_bytes())
    dati = buf.getvalue()
    if len(dati) < 50_000:
        raise ScaricoErrore("ICON-EU: GRIB concatenato troppo piccolo")
    return _scrivi_atomico(dest, dati)


# ---------------------------------------------------------------------------
# Interfaccia unica
# ---------------------------------------------------------------------------

def trova_corsa(modello: str) -> datetime:
    if modello == "gfs":
        return trova_corsa_gfs(Path("."))
    if modello in ("ecmwf", "ecmwf-aifs"):
        return trova_corsa_ecmwf(modello)
    if modello == "icon-eu":
        return trova_corsa_icon_eu()
    raise ScaricoErrore(f"Modello sconosciuto: {modello}")


def scarica_step(modello: str, corsa: datetime, step: int, cache: Path) -> Path:
    if modello == "gfs":
        return scarica_gfs_step(corsa, step, cache)
    if modello in ("ecmwf", "ecmwf-aifs"):
        return scarica_ecmwf_step(corsa, step, cache, modello)
    if modello == "icon-eu":
        return scarica_icon_eu_step(corsa, step, cache)
    raise ScaricoErrore(f"Modello sconosciuto: {modello}")


def registra_meta(cache: Path, modello: str, corsa: datetime, step: int, path: Path) -> None:
    meta = cache / "meta.jsonl"
    rec = {
        "modello": modello,
        "corsa": corsa.strftime("%Y%m%d%H"),
        "step": step,
        "file": str(path),
        "byte": path.stat().st_size if path.exists() else 0,
    }
    with meta.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")
