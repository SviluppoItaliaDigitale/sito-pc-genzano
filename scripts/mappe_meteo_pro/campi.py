"""Lettura dei GRIB e calcolo dei campi derivati (PV, IVT, theta-e, tropopausa, ecc.)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import xarray as xr

from .config import LIVELLI_HPA

# Costanti
G = 9.80665  # m s-2, gravità standard
PVU = 1.0e-6  # 1 PVU = 10^-6 K m^2 kg^-1 s^-1


@dataclass
class Stato:
    """Campi di uno step, già ritagliati e in unità comode per il disegno."""

    modello: str
    corsa: datetime
    step: int
    valid: datetime
    lon: np.ndarray  # (nx,)
    lat: np.ndarray  # (ny,)
    campi: dict[str, np.ndarray] = field(default_factory=dict)
    avvisi: list[str] = field(default_factory=list)

    def ha(self, *nomi: str) -> bool:
        return all(n in self.campi and self.campi[n] is not None for n in nomi)

    def get(self, nome: str) -> np.ndarray | None:
        return self.campi.get(nome)


# ---------------------------------------------------------------------------
# Apertura GRIB
# ---------------------------------------------------------------------------

def _apri_grib(path: Path) -> list[xr.Dataset]:
    """Apre un GRIB misto dividendolo in dataset omogenei (cfgrib)."""
    import cfgrib

    try:
        elenco = cfgrib.open_datasets(str(path), backend_kwargs={"indexpath": ""})
    except Exception as e:  # noqa: BLE001
        # Un tentativo più semplice, un solo gruppo.
        try:
            elenco = [xr.open_dataset(str(path), engine="cfgrib", backend_kwargs={"indexpath": ""})]
        except Exception as e2:  # noqa: BLE001
            raise RuntimeError(f"Impossibile leggere {path}: {e} / {e2}") from e2
    return elenco


def _arr(da: xr.DataArray) -> np.ndarray:
    v = np.asarray(da.values, dtype=np.float64)
    return np.ma.filled(v, np.nan) if np.ma.isMaskedArray(v) else v


def _lon_lat(ds: xr.Dataset) -> tuple[np.ndarray, np.ndarray] | tuple[None, None]:
    lon_n = next((n for n in ("longitude", "lon") if n in ds.coords or n in ds.variables), None)
    lat_n = next((n for n in ("latitude", "lat") if n in ds.coords or n in ds.variables), None)
    if not lon_n or not lat_n:
        return None, None
    lon = np.asarray(ds[lon_n].values, dtype=np.float64)
    lat = np.asarray(ds[lat_n].values, dtype=np.float64)
    # Porta le longitudini in [-180, 180] per il ritaglio europeo.
    lon = ((lon + 180.0) % 360.0) - 180.0
    return lon, lat


def _isobarici(ds: xr.Dataset) -> xr.DataArray | None:
    for n in ("isobaricInhPa", "isobaricInPa", "level", "isobaric"):
        if n in ds.coords or n in ds.dims or n in ds.variables:
            return ds[n]
    return None


def _livelli_hpa(coord: xr.DataArray) -> np.ndarray:
    v = np.asarray(coord.values, dtype=np.float64)
    # se sono Pascal (valori grandi), converte
    if np.nanmax(v) > 2000:
        v = v / 100.0
    return v


def _var_per_nome(ds: xr.Dataset, candidati: tuple[str, ...]) -> xr.DataArray | None:
    for n in candidati:
        if n in ds.data_vars:
            return ds[n]
    # a volte il shortName è un attributo
    for nome, da in ds.data_vars.items():
        sn = str(da.attrs.get("GRIB_shortName", "")).lower()
        if sn in candidati or nome.lower() in candidati:
            return da
    return None


def _mesh(lon: np.ndarray, lat: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    if lon.ndim == 1 and lat.ndim == 1:
        return np.meshgrid(lon, lat)
    return lon, lat


def _ordina_lat(lat: np.ndarray, *arrays: np.ndarray) -> tuple:
    """Garantisce latitudine crescente (sud → nord), comodo per pcolormesh e MetPy."""
    if lat.ndim != 1:
        return (lat,) + arrays
    if lat[0] < lat[-1]:
        return (lat,) + arrays
    idx = slice(None, None, -1)
    return (lat[idx],) + tuple(a[idx, ...] if a is not None and a.ndim >= 1 else a for a in arrays)



def _gfs_prec_6h(path: Path, step: int) -> np.ndarray | None:
    """GFS pubblica a ogni step multiplo di 6 sia l'accumulo 0-N sia quello (N-6)-N: si prende il secondo."""
    if step < 6:
        return None
    try:
        ds = xr.open_dataset(
            str(path), engine="cfgrib",
            backend_kwargs={"indexpath": "", "filter_by_keys": {"shortName": "tp", "stepRange": f"{step - 6}-{step}"}},
        )
    except Exception:
        return None
    for da in ds.data_vars.values():
        v = _arr(da)
        while v.ndim > 2:
            v = v[0]
        return v
    return None


def _unita_tp(sfc: dict) -> str:
    for da in sfc.values():
        if str(da.attrs.get("GRIB_shortName", "")).lower() == "tp" or da.name == "tp":
            return str(da.attrs.get("GRIB_units", da.attrs.get("units", ""))).strip()
    return ""


def _gfs_campo(path: Path, chiavi: dict) -> np.ndarray | None:
    """Un solo messaggio GFS scelto per chiavi GRIB (es. nuvolosità istantanea, accumulo 0-N)."""
    try:
        ds = xr.open_dataset(
            str(path), engine="cfgrib",
            backend_kwargs={"indexpath": "", "filter_by_keys": chiavi},
        )
    except Exception:
        return None
    for da in ds.data_vars.values():
        v = _arr(da)
        while v.ndim > 2:
            v = v[0]
        return v
    return None


def _carte_per_tutti(modello: str, step: int, path: Path, prendi_sfc, campi: dict) -> None:
    """Campi delle carte «per tutti»: temperatura a 2 m, raffica, pioggia totale, neve, nubi.

    Unità d'uscita: °C, km/h, mm, cm, %. I nomi GRIB e le unità sono quelli
    letti nei file dei cinque modelli il 13/11/2026.
    """
    t2 = prendi_sfc("t2m", "2t", "t_2m")
    if t2 is not None:
        campi["t2m"] = t2 - 273.15 if np.nanmean(t2) > 150 else t2

    # Raffica: GFS istantanea all'ora di validità; ECMWF IFS (10fg) e ICON
    # (VMAX_10M) massimo dell'ora precedente; ECMWF IFS oltre +90 (10fg3)
    # massimo delle tre ore precedenti. Allo step 0 ECMWF e ICON non
    # hanno un periodo su cui calcolarla: niente carta.
    if modello == "gfs":
        raffica = _gfs_campo(path, {"shortName": "gust", "typeOfLevel": "surface"})
    elif step > 0:
        raffica = prendi_sfc("fg10", "10fg", "fg310", "10fg3", "i10fg", "max_i10fg", "vmax_10m")
    else:
        raffica = None
    if raffica is not None:
        campi["raffica"] = np.clip(raffica, 0, None) * 3.6  # m/s → km/h

    # Pioggia totale dall'inizializzazione.
    if step == 0 and "mslp" in campi:
        campi["tp_tot"] = np.zeros_like(campi["mslp"])
    elif modello == "gfs":
        tot = _gfs_campo(path, {"shortName": "tp", "stepRange": f"0-{step}"})
        if tot is not None:
            campi["tp_tot"] = np.clip(tot, 0, None)
    elif "tp_acc" in campi:
        campi["tp_tot"] = np.clip(campi["tp_acc"], 0, None)

    # Neve al suolo in cm. ECMWF dà l'equivalente in acqua (m) e la densità
    # del manto (kg/m3): altezza = sd * 1000 / densità.
    if modello == "ecmwf":
        sd = prendi_sfc("sd")
        rsn = prendi_sfc("rsn")
        if sd is not None and rsn is not None:
            with np.errstate(divide="ignore", invalid="ignore"):
                h = np.where(rsn > 50, sd * 1000.0 / rsn, 0.0)
            campi["neve_cm"] = np.clip(h, 0, None) * 100.0
    elif modello != "ecmwf-aifs":
        h = _gfs_campo(path, {"shortName": "sde", "typeOfLevel": "surface"}) if modello == "gfs" else prendi_sfc("sde", "h_snow")
        if h is not None:
            campi["neve_cm"] = np.clip(h, 0, None) * 100.0

    # Nuvolosità totale in %. ECMWF IFS la dà fra 0 e 1; GFS ha anche la media
    # sulle 6 ore precedenti: si prende il valore istantaneo.
    if modello == "gfs":
        nubi = _gfs_campo(path, {"shortName": "tcc", "typeOfLevel": "atmosphere", "stepType": "instant"})
    else:
        nubi = prendi_sfc("tcc", "clct")
    if nubi is not None:
        if np.nanmax(nubi) <= 1.0001:
            nubi = nubi * 100.0
        campi["nubi"] = np.clip(nubi, 0, 100)


# ---------------------------------------------------------------------------
# Lettura e normalizzazione
# ---------------------------------------------------------------------------

def carica_stato(modello: str, corsa: datetime, step: int, path: Path,
                 acc_prec_prec: np.ndarray | None = None,
                 extent: tuple[float, float, float, float] | None = None) -> Stato:
    """Legge un GRIB e restituisce uno Stato con campi 2D già normalizzati.

    `acc_prec_prec` è l'accumulo di precipitazione dello step precedente
    (stessa griglia), utile per calcolare la pioggia in 6 ore su ECMWF e ICON.
    """
    dataset = _apri_grib(path)
    lon = lat = None
    sfc: dict[str, xr.DataArray] = {}
    pl: dict[str, xr.DataArray] = {}  # nome -> DataArray con dim livello
    livelli_ref = None

    for ds in dataset:
        lo, la = _lon_lat(ds)
        if lo is not None:
            lon, lat = lo, la
        coord_p = _isobarici(ds)
        if coord_p is not None and coord_p.size > 1:
            # campi su livelli di pressione
            for nome, da in ds.data_vars.items():
                pl[nome] = da
            livelli_ref = coord_p
        else:
            for nome, da in ds.data_vars.items():
                sfc[nome] = da

    if lon is None or lat is None:
        raise RuntimeError(f"Griglia assente nel file {path}")

    # Se lon/lat sono 1D, bene; se 2D (raro qui) si tiene la riga/colonna.
    if lon.ndim == 2:
        lon = lon[0, :]
    if lat.ndim == 2:
        lat = lat[:, 0]

    campi: dict[str, np.ndarray] = {}
    avvisi: list[str] = []

    def prendi_sfc(*nomi: str) -> np.ndarray | None:
        for n in nomi:
            if n in sfc:
                v = _arr(sfc[n])
                # togli dimensioni extra (time, step, surface)
                while v.ndim > 2:
                    v = v[0]
                return v
        # shortName
        for da in sfc.values():
            sn = str(da.attrs.get("GRIB_shortName", "")).lower()
            if sn in nomi or da.name in nomi:
                v = _arr(da)
                while v.ndim > 2:
                    v = v[0]
                return v
        return None

    def prendi_pl(nomi: tuple[str, ...], livello: int) -> np.ndarray | None:
        da = None
        for n in nomi:
            if n in pl:
                da = pl[n]
                break
        if da is None:
            for cand, x in pl.items():
                sn = str(x.attrs.get("GRIB_shortName", "")).lower()
                if sn in nomi or cand in nomi:
                    da = x
                    break
        if da is None or livelli_ref is None:
            return None
        lev = _livelli_hpa(livelli_ref)
        # quale dimensione è il livello?
        v = da.values
        # allinea: dim 0 o una dim chiamata come il coord
        dim_liv = None
        for d in da.dims:
            if d in ("isobaricInhPa", "isobaricInPa", "level", "isobaric"):
                dim_liv = d
                break
        if dim_liv is None:
            # prova a indovinare: la dim che ha la stessa lunghezza dei livelli
            for d in da.dims:
                if da.sizes[d] == lev.size:
                    dim_liv = d
                    break
        if dim_liv is None:
            return None
        # nearest level
        k = int(np.argmin(np.abs(lev - livello)))
        if abs(lev[k] - livello) > 10:
            return None
        sel = da.isel({dim_liv: k})
        arr = _arr(sel)
        while arr.ndim > 2:
            arr = arr[0]
        return arr

    # --- superficie ---
    msl = prendi_sfc("prmsl", "msl", "pmsl", "mslma", "pres")
    if msl is not None:
        campi["mslp"] = msl / 100.0 if np.nanmean(msl) > 2000 else msl  # Pa → hPa

    u10 = prendi_sfc("u10", "10u", "u_10m", "u10m")
    v10 = prendi_sfc("v10", "10v", "v_10m", "v10m")
    if u10 is not None:
        campi["u10"] = u10
    if v10 is not None:
        campi["v10"] = v10

    cape = prendi_sfc("cape", "mucape", "cape_ml", "cape_con")
    if cape is not None:
        campi["cape"] = np.clip(cape, 0, None)

    pwat = prendi_sfc("pwat", "tcwv", "tqv", "tcw", "precipitable_water")
    if pwat is not None:
        # kg/m2 = mm; a volte è in m
        campi["pwat"] = pwat * 1000.0 if np.nanmax(pwat) < 1.5 else pwat

    tp = prendi_sfc("apcp", "tp", "tot_prec", "prate")
    tp_6h_diretto = _gfs_prec_6h(path, step) if modello == "gfs" else None
    if tp is not None:
        # ECMWF IFS dà tp in metri; AIFS, ICON e GFS in kg/m2 (= mm). Si
        # decide dall'unità scritta nel GRIB: a occhio (massimo sotto 1,5)
        # una corsa AIFS quasi asciutta sarebbe stata moltiplicata per mille.
        if modello == "ecmwf" and _unita_tp(sfc) in ("m", ""):
            tp_mm = tp * 1000.0
        else:
            tp_mm = tp
        campi["tp_acc"] = tp_mm
        if tp_6h_diretto is not None and tp_6h_diretto.shape == tp_mm.shape:
            campi["tp_6h"] = np.clip(tp_6h_diretto, 0, None)
        elif acc_prec_prec is not None and acc_prec_prec.shape == tp_mm.shape:
            campi["tp_6h"] = np.clip(tp_mm - acc_prec_prec, 0, None)
        elif step == 0:
            campi["tp_6h"] = np.zeros_like(tp_mm)
        else:
            # GFS: spesso APCP è già l'accumulo sul periodo del messaggio.
            # Se non abbiamo lo step precedente, usiamo il valore com'è
            # (può essere 1, 3 o 6 ore: lo dichiaramo nell'avviso).
            campi["tp_6h"] = np.clip(tp_mm, 0, None)
            if modello == "gfs":
                avvisi.append(
                    "Precipitazione letta dal messaggio GFS di questo step "
                    "(intervallo del GRIB, di solito 1-6 ore) perché manca l'accumulo precedente."
                )

    if "tp_6h" not in campi and step == 0 and "mslp" in campi:
        campi["tp_6h"] = np.zeros_like(campi["mslp"])

    _carte_per_tutti(modello, step, path, prendi_sfc, campi)

    # --- livelli isobarici, nomi corti t850, z500, ... ---
    alias_t = ("t", "tmp", "temperature")
    alias_z = ("gh", "z", "hgt", "fi", "geopotential")
    alias_u = ("u", "ugrd", "u-component_of_wind")
    alias_v = ("v", "vgrd", "v-component_of_wind")
    alias_w = ("w", "vvel", "omega", "wz")
    alias_q = ("q", "spfh", "qv", "specific_humidity")
    alias_r = ("r", "rh", "relhum", "relative_humidity")
    alias_vo = ("vo", "absv", "relv", "vorticity")

    cubi: dict[str, dict[int, np.ndarray]] = {k: {} for k in ("t", "z", "u", "v", "w", "q", "r", "vo")}

    for lv in LIVELLI_HPA:
        t = prendi_pl(alias_t, lv)
        z = prendi_pl(alias_z, lv)
        u = prendi_pl(alias_u, lv)
        v = prendi_pl(alias_v, lv)
        w = prendi_pl(alias_w, lv)
        q = prendi_pl(alias_q, lv)
        r = prendi_pl(alias_r, lv)
        vo = prendi_pl(alias_vo, lv)
        if t is not None:
            cubi["t"][lv] = t  # Kelvin (GFS/ECMWF/ICON)
            campi[f"t{lv}"] = t - 273.15 if np.nanmean(t) > 150 else t
        if z is not None:
            # geopotenziale (m2/s2) oppure altezza in metri
            z_m = z / G if np.nanmean(np.abs(z)) > 20000 else z
            cubi["z"][lv] = z_m
            campi[f"z{lv}"] = z_m
        if u is not None:
            cubi["u"][lv] = u
            campi[f"u{lv}"] = u
        if v is not None:
            cubi["v"][lv] = v
            campi[f"v{lv}"] = v
        if w is not None:
            cubi["w"][lv] = w
            campi[f"w{lv}"] = w
        if q is not None:
            cubi["q"][lv] = q
            campi[f"q{lv}"] = q
        if r is not None:
            # 0-1 oppure 0-100
            cubi["r"][lv] = r / 100.0 if np.nanmax(r) > 2 else r
            campi[f"r{lv}"] = cubi["r"][lv]
        if vo is not None:
            cubi["vo"][lv] = vo
            campi[f"vo{lv}"] = vo

    if 250 in cubi["u"] and 250 in cubi["v"]:
        campi["mod250"] = np.hypot(cubi["u"][250], cubi["v"][250])
    if 1000 in cubi["z"] and 500 in cubi["z"]:
        campi["spessore_1000_500"] = cubi["z"][500] - cubi["z"][1000]  # metri

    # Ordina le latitudini crescenti e allinea tutti i 2D.
    arrays_2d = {k: v for k, v in campi.items() if isinstance(v, np.ndarray) and v.ndim == 2}
    if arrays_2d:
        primo = next(iter(arrays_2d.values()))
        # alcuni campi potrebbero non avere ancora la stessa forma: si filtrano
        chiavi = [k for k, v in arrays_2d.items() if v.shape == primo.shape]
        extra = [campi[k] for k in chiavi]
        lat, *extra = _ordina_lat(lat, *extra)
        for k, v in zip(chiavi, extra):
            campi[k] = v
        # ri-allinea i cubi
        if lat[0] > lat[-1] if False else False:
            pass
        # se abbiamo invertito, i cubi originali (non copiati in campi come cubo)
        # vanno riallineati prima dei derivati: ricalcoliamo dai campi già girati.

    # Ricostruisci cubi dopo l'eventuale flip, dai campi già presenti.
    cubi2: dict[str, dict[int, np.ndarray]] = {k: {} for k in cubi}
    for pref, chiave in (("t", "t"), ("z", "z"), ("u", "u"), ("v", "v"), ("w", "w"), ("q", "q"), ("r", "r"), ("vo", "vo")):
        for lv in LIVELLI_HPA:
            n = f"{pref}{lv}"
            if n in campi:
                cubi2[chiave][lv] = campi[n] if pref != "t" else (
                    campi[n] + 273.15 if np.nanmean(campi[n]) < 150 else campi[n]
                )
            # t è in Celsius nei campi; per i calcoli serve Kelvin
        # fix t: sopra ho messo Kelvin se la media era già K. Rileggo in modo pulito.
    # Ricostruzione pulita di t in Kelvin:
    cubi2["t"] = {}
    for lv in LIVELLI_HPA:
        n = f"t{lv}"
        if n in campi:
            val = campi[n]
            cubi2["t"][lv] = val + 273.15 if np.nanmean(val) < 150 else val

    tp_acc_pieno = campi.get("tp_acc")

    # Ritaglio geografico PRIMA dei calcoli 3D (ICON-EU sull'Europa intera sarebbe troppo pesante).
    if extent is not None:
        lon, lat, campi = ritaglia(lon, lat, campi, extent, pad=1.5)
        cubi2 = {k: {} for k in cubi2}
        cubi2["t"] = {}
        for pref, chiave in (("t", "t"), ("z", "z"), ("u", "u"), ("v", "v"), ("w", "w"), ("q", "q"), ("r", "r"), ("vo", "vo")):
            for lv in LIVELLI_HPA:
                n = f"{pref}{lv}"
                if n in campi:
                    if pref == "t":
                        val = campi[n]
                        cubi2["t"][lv] = val + 273.15 if np.nanmean(val) < 150 else val
                    else:
                        cubi2[chiave][lv] = campi[n]

    # Derivati che non dipendono da MetPy in modo pesante
    _deriva_umidita(campi, cubi2)
    _deriva_ivt(campi, cubi2, avvisi)
    _deriva_thetae(campi, cubi2, avvisi)
    _deriva_vorticita(campi, cubi2, lat, lon, avvisi)
    _deriva_pv_e_tropopausa(campi, cubi2, lat, lon, avvisi)

    valid = corsa + __import__("datetime").timedelta(hours=int(step))
    if corsa.tzinfo is None:
        corsa = corsa.replace(tzinfo=timezone.utc)
    if valid.tzinfo is None:
        valid = valid.replace(tzinfo=timezone.utc)

    if tp_acc_pieno is not None:
        campi["_tp_acc_pieno"] = tp_acc_pieno

    return Stato(
        modello=modello,
        corsa=corsa,
        step=step,
        valid=valid,
        lon=lon,
        lat=lat,
        campi=campi,
        avvisi=avvisi,
    )


def _deriva_umidita(campi: dict, cubi: dict, ) -> None:
    """Se manca q ma c'è RH e T, stima la umidità specifica."""
    try:
        import metpy.calc as mpcalc
        from metpy.units import units
    except Exception:
        return
    for lv in LIVELLI_HPA:
        if lv in cubi["q"]:
            continue
        if lv not in cubi["t"] or lv not in cubi.get("r", {}):
            continue
        try:
            t = cubi["t"][lv] * units.kelvin
            p = lv * units.hPa
            rh = cubi["r"][lv] * units.dimensionless
            # vapor pressure then mixing ratio
            q = mpcalc.specific_humidity_from_dewpoint(
                p, mpcalc.dewpoint_from_relative_humidity(t, rh)
            )
            cubi["q"][lv] = np.asarray(q.astype("float64").magnitude)
            campi[f"q{lv}"] = cubi["q"][lv]
        except Exception:
            continue


def _deriva_ivt(campi: dict, cubi: dict, avvisi: list[str]) -> None:
    """Trasporto integrato di vapore (kg m-1 s-1) da 1000 a 300 hPa."""
    livelli = sorted([lv for lv in cubi["u"] if lv in cubi["v"] and lv in cubi["q"] and lv >= 300], reverse=True)
    if len(livelli) < 4:
        avvisi.append("IVT non calcolato: troppi pochi livelli con umidità specifica.")
        return
    # integrazione trapezoidale in pressione (Pa): IVT = 1/g ∫ q V dp
    u_int = None
    v_int = None
    for i in range(len(livelli) - 1):
        p1, p2 = livelli[i], livelli[i + 1]  # hPa, p1 > p2 (dal basso verso l'alto)
        dp = (p1 - p2) * 100.0  # Pa
        q1, q2 = cubi["q"][p1], cubi["q"][p2]
        u1, u2 = cubi["u"][p1], cubi["u"][p2]
        v1, v2 = cubi["v"][p1], cubi["v"][p2]
        qbar = 0.5 * (q1 + q2)
        ubar = 0.5 * (u1 + u2)
        vbar = 0.5 * (v1 + v2)
        pezzo_u = qbar * ubar * dp / G
        pezzo_v = qbar * vbar * dp / G
        u_int = pezzo_u if u_int is None else u_int + pezzo_u
        v_int = pezzo_v if v_int is None else v_int + pezzo_v
    campi["ivt_u"] = u_int
    campi["ivt_v"] = v_int
    campi["ivt"] = np.hypot(u_int, v_int)


def _deriva_thetae(campi: dict, cubi: dict, avvisi: list[str]) -> None:
    try:
        import metpy.calc as mpcalc
        from metpy.units import units
    except Exception as e:
        avvisi.append(f"Theta-e non calcolata: {e}")
        return
    if 850 not in cubi["t"]:
        return
    t = cubi["t"][850] * units.kelvin
    p = 850 * units.hPa
    try:
        if 850 in cubi["q"]:
            dew = mpcalc.dewpoint_from_specific_humidity(p, t, cubi["q"][850] * units.dimensionless)
        elif 850 in cubi.get("r", {}):
            dew = mpcalc.dewpoint_from_relative_humidity(t, cubi["r"][850] * units.dimensionless)
        else:
            avvisi.append("Theta-e non calcolata: manca umidità a 850 hPa.")
            return
        th = mpcalc.equivalent_potential_temperature(p, t, dew)
        campi["thetae850"] = np.asarray(th.to("K").magnitude)
    except Exception as e:
        avvisi.append(f"Theta-e non calcolata: {e}")


def _dx_dy(lat: np.ndarray, lon: np.ndarray):
    import metpy.calc as mpcalc
    from metpy.units import units

    lon2, lat2 = np.meshgrid(lon, lat)
    dx, dy = mpcalc.lat_lon_grid_deltas(lon2 * units.degree, lat2 * units.degree)
    return dx, dy, lat2


def _deriva_vorticita(campi: dict, cubi: dict, lat: np.ndarray, lon: np.ndarray, avvisi: list[str]) -> None:
    """Vorticità relativa a 500 e media 925-850, se non già presente o come verifica."""
    try:
        import metpy.calc as mpcalc
        from metpy.units import units
        dx, dy, _ = _dx_dy(lat, lon)
    except Exception as e:
        avvisi.append(f"Vorticità non ricalcolata: {e}")
        dx = dy = None

    def vo_da(u, v):
        if dx is None:
            return None
        vo = mpcalc.vorticity(u * units("m/s"), v * units("m/s"), dx=dx, dy=dy)
        return np.asarray(vo.magnitude)

    for lv in (500, 700, 850, 925):
        chiave = f"vo{lv}"
        if chiave not in campi and lv in cubi["u"] and lv in cubi["v"]:
            try:
                campi[chiave] = vo_da(cubi["u"][lv], cubi["v"][lv])
            except Exception:
                pass
        # GFS ABSV è vorticità assoluta: togli f per avere quella relativa
        if chiave in campi and campi[chiave] is not None:
            media = np.nanmean(np.abs(campi[chiave]))
            # se è assoluta, i valori sono ~ 10^-4 (f + zeta). Relativa è ~ 10^-5.
            # In GFS ABSV è assoluta. Se la media è > 5e-5 e siamo a 45N, ricalcoliamo
            # oppure sottraiamo 2*omega*sin(lat).
            if media > 5.0e-5 and dx is not None:
                # probabilmente assoluta
                lat2 = np.deg2rad(lat)[:, None]
                f = 2 * 7.292115e-5 * np.sin(lat2)
                campi[chiave] = campi[chiave] - f

    # media 925-850
    if "vo925" in campi and "vo850" in campi and campi["vo925"] is not None and campi["vo850"] is not None:
        campi["vo_925_850"] = 0.5 * (campi["vo925"] + campi["vo850"])
    elif "vo850" in campi:
        campi["vo_925_850"] = campi["vo850"]


def _stack(cubi: dict, nome: str, livelli: list[int]) -> np.ndarray | None:
    if any(lv not in cubi[nome] for lv in livelli):
        return None
    return np.stack([cubi[nome][lv] for lv in livelli], axis=0)  # (lev, y, x)


def _deriva_pv_e_tropopausa(campi: dict, cubi: dict, lat: np.ndarray, lon: np.ndarray, avvisi: list[str]) -> None:
    """PV 3D, media 300-200, superfici isentropiche e tropopausa 2 PVU."""
    try:
        import metpy.calc as mpcalc
        from metpy.units import units
    except Exception as e:
        avvisi.append(f"PV non calcolata: {e}")
        return

    livelli = [lv for lv in LIVELLI_HPA if lv in cubi["t"] and lv in cubi["u"] and lv in cubi["v"] and lv in cubi["z"]]
    # dal suolo verso l'alto o viceversa: MetPy vuole pressione decrescente (verso l'alto)
    livelli = sorted(livelli, reverse=True)  # 1000 ... 100
    if len(livelli) < 6:
        avvisi.append("PV non calcolata: livelli verticali insufficienti.")
        return

    try:
        dx, dy, lat2 = _dx_dy(lat, lon)
        t = _stack(cubi, "t", livelli) * units.kelvin
        u = _stack(cubi, "u", livelli) * units("m/s")
        v = _stack(cubi, "v", livelli) * units("m/s")
        p = np.array(livelli, dtype=np.float64)[:, None, None] * units.hPa
        theta = mpcalc.potential_temperature(p, t)
        pv = mpcalc.potential_vorticity_baroclinic(
            theta, p, u, v, dx=dx[None, :, :], dy=dy[None, :, :],
            latitude=(lat2 * units.degree)[None, :, :], x_dim=-1, y_dim=-2, vertical_dim=-3,
        )
        pv_si = pv.to("K * m**2 / (kg * s)")
        pv_pvu = np.asarray(pv_si.magnitude, dtype=np.float64) / PVU
    except Exception as e:
        avvisi.append(f"PV non calcolata: {e}")
        return

    theta_v = np.asarray(theta.magnitude) if hasattr(theta, "magnitude") else np.asarray(theta)
    u_v = _stack(cubi, "u", livelli)
    v_v = _stack(cubi, "v", livelli)
    p_v = np.array(livelli, dtype=np.float64)

    # Media PV 300-200
    idx_m = [i for i, lv in enumerate(livelli) if 200 <= lv <= 300]
    if idx_m:
        campi["pv_300_200"] = np.nanmean(pv_pvu[idx_m, ...], axis=0)

    # Superfici isentropiche 310, 330, 350 K
    for th0 in (310.0, 330.0, 350.0):
        pv_s, p_s, u_s, v_s = _interp_isentropica(theta_v, pv_pvu, p_v, u_v, v_v, th0)
        if pv_s is None:
            continue
        tag = str(int(th0))
        campi[f"pv_{tag}"] = pv_s
        campi[f"p_{tag}"] = p_s
        campi[f"u_{tag}"] = u_s
        campi[f"v_{tag}"] = v_s

    # Tropopausa dinamica 2 PVU (emisfero nord: +2 PVU, dal tetto verso il basso)
    theta_dt, p_dt, u_dt, v_dt = _superficie_2pvu(theta_v, pv_pvu, p_v, u_v, v_v)
    if theta_dt is not None:
        campi["theta_dt"] = theta_dt
        campi["p_dt"] = p_dt
        campi["u_dt"] = u_dt
        campi["v_dt"] = v_dt
        if "thetae850" in campi:
            campi["coupling"] = theta_dt - campi["thetae850"]



def ritaglia(lon, lat, campi, extent, pad=1.0):
    """Ritaglia lon/lat 1D e tutti i campi 2D a un riquadro (lon0, lon1, lat0, lat1)."""
    lon0, lon1, lat0, lat1 = extent
    lon0, lon1, lat0, lat1 = lon0 - pad, lon1 + pad, lat0 - pad, lat1 + pad
    ix = np.where((lon >= lon0) & (lon <= lon1))[0]
    iy = np.where((lat >= lat0) & (lat <= lat1))[0]
    if ix.size < 4 or iy.size < 4:
        return lon, lat, campi
    slx, sly = slice(ix[0], ix[-1] + 1), slice(iy[0], iy[-1] + 1)
    lon_n, lat_n = lon[slx], lat[sly]
    nuovi = {}
    for k, v in campi.items():
        if isinstance(v, np.ndarray) and v.ndim == 2 and v.shape == (lat.size, lon.size):
            nuovi[k] = v[sly, slx]
        else:
            nuovi[k] = v
    return lon_n, lat_n, nuovi


def _interp_a_valore(coord, valore, *fields, dal_tetto=False):
    """Interpola campi (lev, y, x) sulla superficie dove coord == valore, in modo vettoriale."""
    c0, c1 = coord[:-1], coord[1:]
    den = c1 - c0
    with np.errstate(divide="ignore", invalid="ignore"):
        w = (valore - c0) / den
    dentro = (w >= -1e-6) & (w <= 1.0 + 1e-6) & np.isfinite(w)
    nlevm = dentro.shape[0]
    ord_idx = np.arange(nlevm, dtype=np.int32)[:, None, None]
    if dal_tetto:
        k = np.where(dentro, ord_idx, -1).max(axis=0)
    else:
        k = np.where(dentro, ord_idx, nlevm + 5).min(axis=0)
        k = np.where(k > nlevm, -1, k)
    valid = k >= 0
    yy, xx = np.indices(k.shape)
    kk = np.clip(k, 0, nlevm - 1)
    ww = w[kk, yy, xx]
    out = []
    for field in fields:
        f0 = field[kk, yy, xx]
        f1 = field[kk + 1, yy, xx]
        val = f0 + ww * (f1 - f0)
        val = np.where(valid, val, np.nan)
        out.append(val)
    return out



def _interp_isentropica(theta, pv, p, u, v, th0: float):
    p3 = np.broadcast_to(p.reshape((-1, 1, 1)), theta.shape).copy()
    res = _interp_a_valore(theta, th0, pv, p3, u, v, dal_tetto=False)
    pv_s, p_s, u_s, v_s = res
    if np.isfinite(pv_s).mean() < 0.3:
        return None, None, None, None
    return pv_s, p_s, u_s, v_s


def _superficie_2pvu(theta, pv, p, u, v, soglia: float = 2.0):
    """Prima intersezione di PV = 2 PVU scendendo dalla sommità (tropopausa, emisfero nord)."""
    p3 = np.broadcast_to(p.reshape((-1, 1, 1)), theta.shape).copy()
    theta_s, p_s, u_s, v_s = _interp_a_valore(pv, soglia, theta, p3, u, v, dal_tetto=True)
    if np.isfinite(theta_s).mean() < 0.3:
        return None, None, None, None
    return theta_s, p_s, u_s, v_s


# Campi da conservare dopo il ritaglio per dominio (il resto occupa solo memoria).
CAMPI_DISEGNO = {
    "mslp", "tp_6h", "t850", "t700", "t500", "u10", "v10",
    "z1000", "z850", "z700", "z500",
    "u1000", "v1000", "u850", "v850", "u700", "v700", "u500", "v500", "u250", "v250",
    "w500", "vo500", "vo_925_850", "mod250", "spessore_1000_500",
    "ivt", "ivt_u", "ivt_v", "cape", "pwat", "thetae850",
    "pv_300_200", "theta_dt", "p_dt", "u_dt", "v_dt", "coupling",
    "pv_330", "p_330", "u_330", "v_330", "pv_310", "u_310", "v_310", "p_350",
    "t2m", "raffica", "tp_tot", "neve_cm", "nubi",
}

# Campi rumorosi (derivate spaziali): si leviga con una gaussiana di circa 0,35°.
CAMPI_LEVIGATI = {
    "w500": 0.35, "vo500": 0.4, "vo_925_850": 0.5,
    "pv_300_200": 0.35, "pv_330": 0.35, "pv_310": 0.35,
    "theta_dt": 0.35, "p_dt": 0.35, "coupling": 0.4,
    "p_330": 0.3, "p_350": 0.3, "ivt": 0.25, "cape": 0.2,
}


def _leviga(arr: np.ndarray, sigma_punti: float) -> np.ndarray:
    from scipy.ndimage import gaussian_filter

    if sigma_punti < 0.6:
        return arr
    mask = ~np.isfinite(arr)
    if mask.all():
        return arr
    pieno = np.where(mask, np.nanmean(arr), arr)
    out = gaussian_filter(pieno, sigma=sigma_punti, mode="nearest")
    out[mask] = np.nan
    return out


def stato_per_dominio(stato: "Stato", dominio_cfg: dict) -> "Stato":
    """Ritaglia al riquadro visibile del dominio, dirada le griglie fitte e leviga i campi rumorosi."""
    bbox = dominio_cfg.get("bbox") or dominio_cfg["extent"]
    campi = {k: v for k, v in stato.campi.items() if k in CAMPI_DISEGNO}
    lon, lat, campi = ritaglia(stato.lon, stato.lat, campi, bbox, pad=1.0)
    max_punti = int(dominio_cfg.get("max_punti", 420))
    passo = max(1, int(np.ceil(max(lon.size, lat.size) / max_punti)))
    if passo > 1:
        lon, lat = lon[::passo], lat[::passo]
        campi = {k: (v[::passo, ::passo] if isinstance(v, np.ndarray) and v.ndim == 2 else v) for k, v in campi.items()}
    ris = float(np.nanmedian(np.abs(np.diff(lat)))) if lat.size > 1 else 0.25
    for k, sigma_gradi in CAMPI_LEVIGATI.items():
        if k in campi and isinstance(campi[k], np.ndarray):
            campi[k] = _leviga(campi[k], sigma_gradi / max(ris, 1e-3))
    return Stato(
        modello=stato.modello, corsa=stato.corsa, step=stato.step, valid=stato.valid,
        lon=lon, lat=lat, campi=campi, avvisi=list(stato.avvisi),
    )
