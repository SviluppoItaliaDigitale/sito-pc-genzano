"""Disegnatori dei singoli prodotti in stile Albany."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from .campi import Stato
from .config import PRODOTTI
from . import disegna as d


def _livelli_int(vmin, vmax, passo):
    start = int(np.floor(vmin / passo) * passo)
    stop = int(np.ceil(vmax / passo) * passo)
    return list(range(start, stop + passo, passo))


def _prepara(stato: Stato, dominio: str, chiave: str):
    meta = PRODOTTI[chiave]
    fig, ax, cax, proj, pc = d.nuova_carta(stato, dominio, meta["titolo"], meta["sottotitolo"])
    return fig, ax, cax, pc, meta


def mslp_precip(stato: Stato, dominio: str, dest: Path) -> Path:
    fig, ax, cax, pc, meta = _prepara(stato, dominio, "mslp_precip")
    lon, lat = stato.lon, stato.lat
    pr = np.clip(stato.campi["tp_6h"], 0, None)
    msl = stato.campi["mslp"]
    # Maschera i valori sotto soglia così il terreno resta visibile
    pr_m = np.ma.masked_less(pr, 0.2)
    cf = d.campo_ombreggiato(ax, pc, lon, lat, pr_m, d.LIV_PIOGGIA, d.CMAP_PIOGGIA, extend="max")
    # Isobare ogni 2 hPa, in evidenza ogni 4
    liv = _livelli_int(np.nanmin(msl), np.nanmax(msl), 2)
    ev = [v for v in liv if v % 4 == 0]
    d.isolinee(ax, pc, lon, lat, msl, liv, colore="#222222", spessore=0.5, fmt="%d", grassetto=ev)
    d.citta(ax, dominio, pc)
    d.colorbar(cax, cf, d.LIV_PIOGGIA)
    d.testata_e_piede(fig, ax, stato, dominio, meta["titolo"], meta["sottotitolo"], "mm / 6 ore")
    return d.salva(fig, dest)


def t850_vento10(stato: Stato, dominio: str, dest: Path) -> Path:
    fig, ax, cax, pc, meta = _prepara(stato, dominio, "t850_vento10")
    lon, lat = stato.lon, stato.lat
    t = stato.campi["t850"]
    liv = list(range(-30, 36, 2))
    cf = d.campo_ombreggiato(ax, pc, lon, lat, t, liv, d.CMAP_TEMP, extend="both")
    d.isolinee(ax, pc, lon, lat, t, liv, colore="#333", spessore=0.3, fmt="%d")
    # zero gradi in evidenza
    d.isolinee(ax, pc, lon, lat, t, [0], colore="#003366", spessore=1.4, fmt="%d", etichette=True)
    d.barbette(ax, pc, lon, lat, stato.campi["u10"], stato.campi["v10"])
    d.citta(ax, dominio, pc)
    d.colorbar(cax, cf, liv[::2])
    d.testata_e_piede(fig, ax, stato, dominio, meta["titolo"], meta["sottotitolo"], "°C  ·  vento in nodi")
    return d.salva(fig, dest)


def h500(stato: Stato, dominio: str, dest: Path) -> Path:
    fig, ax, cax, pc, meta = _prepara(stato, dominio, "h500")
    lon, lat = stato.lon, stato.lat
    z = stato.campi["z500"] / 10.0  # decametri
    t = stato.campi["t500"]
    # Ombreggiatura: si preferisce il moto verticale (ascesa), altrimenti la vorticità
    unita = ""
    if stato.ha("w500"):
        # omega in Pa/s: valori negativi = ascesa. Convertiamo in µbar/s (1 Pa/s = 10 µbar/s)
        w = stato.campi["w500"] * 10.0
        liv_w = [-20, -15, -10, -8, -6, -4, -2, -1, 1, 2, 4, 6, 8, 10, 15, 20]
        cf = d.campo_ombreggiato(ax, pc, lon, lat, w, liv_w, d.CMAP_OMEGA, extend="both")
        unita = "µbar/s (valori negativi: ascesa)"
    elif stato.ha("vo500"):
        vo = stato.campi["vo500"] * 1.0e5
        liv_v = [-20, -16, -12, -8, -4, -2, 2, 4, 8, 12, 16, 20]
        cf = d.campo_ombreggiato(ax, pc, lon, lat, vo, liv_v, d.CMAP_VORT, extend="both")
        unita = "vorticità relativa (10^-5 / s)"
    else:
        # fallback: ombreggia la temperatura
        liv_t = list(range(-50, 12, 2))
        cf = d.campo_ombreggiato(ax, pc, lon, lat, t, liv_t, d.CMAP_TEMP, extend="both")
        unita = "temperatura a 500 hPa, °C"
    liv_z = _livelli_int(np.nanmin(z), np.nanmax(z), 4)
    ev = [v for v in liv_z if v % 8 == 0]
    d.isolinee(ax, pc, lon, lat, z, liv_z, colore="#111", spessore=0.6, fmt="%d", grassetto=ev)
    liv_t = _livelli_int(np.nanmin(t), np.nanmax(t), 2)
    d.isolinee(ax, pc, lon, lat, t, liv_t, colore="#9b111e", spessore=0.45, fmt="%d", tratteggio="--")
    if stato.ha("u500", "v500"):
        d.barbette(ax, pc, lon, lat, stato.campi["u500"], stato.campi["v500"])
    d.citta(ax, dominio, pc)
    d.colorbar(cax, cf)
    d.testata_e_piede(fig, ax, stato, dominio, meta["titolo"], meta["sottotitolo"], unita)
    return d.salva(fig, dest)


def ivt_h700(stato: Stato, dominio: str, dest: Path) -> Path:
    fig, ax, cax, pc, meta = _prepara(stato, dominio, "ivt_h700")
    lon, lat = stato.lon, stato.lat
    ivt = stato.campi["ivt"]
    z = stato.campi["z700"] / 10.0
    liv = [100, 150, 200, 250, 300, 400, 500, 600, 800, 1000, 1250]
    cf = d.campo_ombreggiato(ax, pc, lon, lat, ivt, liv, d.CMAP_IVT, extend="max")
    liv_z = _livelli_int(np.nanmin(z), np.nanmax(z), 3)
    d.isolinee(ax, pc, lon, lat, z, liv_z, colore="#111", spessore=0.6, fmt="%d")
    if stato.ha("ivt_u", "ivt_v"):
        # vettori IVT (non barbette): una freccia ogni tanto
        passo = max(1, int(min(len(lat), len(lon)) / 14))
        lon2, lat2 = np.meshgrid(lon[::passo], lat[::passo])
        ax.quiver(
            lon2, lat2,
            stato.campi["ivt_u"][::passo, ::passo],
            stato.campi["ivt_v"][::passo, ::passo],
            transform=pc, scale=8000, width=0.0022, color="#1a1a1a", zorder=6,
        )
    d.citta(ax, dominio, pc)
    d.colorbar(cax, cf, liv)
    d.testata_e_piede(fig, ax, stato, dominio, meta["titolo"], meta["sottotitolo"], "kg / (m s)")
    return d.salva(fig, dest)


def h850_cape_shear(stato: Stato, dominio: str, dest: Path) -> Path:
    fig, ax, cax, pc, meta = _prepara(stato, dominio, "h850_cape_shear")
    lon, lat = stato.lon, stato.lat
    cape = np.clip(stato.campi["cape"], 0, None)
    z = stato.campi["z850"] / 10.0
    t = stato.campi["t850"]
    liv = [50, 100, 250, 500, 750, 1000, 1500, 2000, 2500, 3000, 4000]
    cf = d.campo_ombreggiato(ax, pc, lon, lat, cape, liv, d.CMAP_CAPE, extend="max")
    liv_z = _livelli_int(np.nanmin(z), np.nanmax(z), 3)
    d.isolinee(ax, pc, lon, lat, z, liv_z, colore="#111", spessore=0.55, fmt="%d")
    d.isolinee(ax, pc, lon, lat, t, _livelli_int(np.nanmin(t), np.nanmax(t), 2),
               colore="#9b111e", spessore=0.4, fmt="%d", tratteggio="--")
    # shear 1000-500 come barbette (differenza vettoriale)
    su = stato.campi["u500"] - stato.campi["u1000"]
    sv = stato.campi["v500"] - stato.campi["v1000"]
    d.barbette(ax, pc, lon, lat, su, sv, colore="#3e2723")
    d.citta(ax, dominio, pc)
    d.colorbar(cax, cf, liv)
    d.testata_e_piede(fig, ax, stato, dominio, meta["titolo"], meta["sottotitolo"], "CAPE J/kg  ·  shear in nodi")
    return d.salva(fig, dest)


def spessore_mslp_jet(stato: Stato, dominio: str, dest: Path) -> Path:
    fig, ax, cax, pc, meta = _prepara(stato, dominio, "spessore_mslp_jet")
    lon, lat = stato.lon, stato.lat
    sp = stato.campi["spessore_1000_500"] / 10.0  # dam
    msl = stato.campi["mslp"]
    jet = stato.campi["mod250"] * 1.943844  # nodi
    liv_sp = list(range(492, 589, 6))
    cf = d.campo_ombreggiato(ax, pc, lon, lat, sp, liv_sp, d.CMAP_SPESSORE, extend="both")
    d.isolinee(ax, pc, lon, lat, sp, [540], colore="#003366", spessore=1.6, fmt="%d")
    liv_p = _livelli_int(np.nanmin(msl), np.nanmax(msl), 4)
    d.isolinee(ax, pc, lon, lat, msl, liv_p, colore="#111", spessore=0.6, fmt="%d")
    # isotache del getto
    liv_j = [50, 70, 90, 110, 130, 150, 170]
    d.isolinee(ax, pc, lon, lat, jet, liv_j, colore="#4a148c", spessore=0.8, fmt="%d")
    d.citta(ax, dominio, pc)
    d.colorbar(cax, cf, liv_sp[::2])
    d.testata_e_piede(fig, ax, stato, dominio, meta["titolo"], meta["sottotitolo"], "spessore in dam  ·  getto in nodi")
    return d.salva(fig, dest)


def h700_pw(stato: Stato, dominio: str, dest: Path) -> Path:
    fig, ax, cax, pc, meta = _prepara(stato, dominio, "h700_pw")
    lon, lat = stato.lon, stato.lat
    pw = stato.campi["pwat"]
    z = stato.campi["z700"] / 10.0
    t = stato.campi["t700"]
    liv = list(range(8, 61, 4))
    cf = d.campo_ombreggiato(ax, pc, lon, lat, pw, liv, d.CMAP_PW, extend="both")
    liv_z = _livelli_int(np.nanmin(z), np.nanmax(z), 3)
    d.isolinee(ax, pc, lon, lat, z, liv_z, colore="#111", spessore=0.55, fmt="%d")
    d.isolinee(ax, pc, lon, lat, t, _livelli_int(np.nanmin(t), np.nanmax(t), 2),
               colore="#9b111e", spessore=0.4, fmt="%d", tratteggio="--")
    d.barbette(ax, pc, lon, lat, stato.campi["u700"], stato.campi["v700"])
    d.citta(ax, dominio, pc)
    d.colorbar(cax, cf, liv)
    d.testata_e_piede(fig, ax, stato, dominio, meta["titolo"], meta["sottotitolo"], "acqua precipitabile, mm  ·  vento in nodi")
    return d.salva(fig, dest)


def thetae850(stato: Stato, dominio: str, dest: Path) -> Path:
    fig, ax, cax, pc, meta = _prepara(stato, dominio, "thetae850")
    lon, lat = stato.lon, stato.lat
    th = stato.campi["thetae850"]
    liv = list(range(280, 361, 4))
    cf = d.campo_ombreggiato(ax, pc, lon, lat, th, liv, d.CMAP_THETAE, extend="both")
    d.isolinee(ax, pc, lon, lat, th, liv[::2], colore="#111", spessore=0.4, fmt="%d")
    if stato.ha("u850", "v850"):
        d.barbette(ax, pc, lon, lat, stato.campi["u850"], stato.campi["v850"])
    d.citta(ax, dominio, pc)
    d.colorbar(cax, cf, liv[::2])
    d.testata_e_piede(fig, ax, stato, dominio, meta["titolo"], meta["sottotitolo"], "K  ·  vento in nodi")
    return d.salva(fig, dest)


def pv_jet(stato: Stato, dominio: str, dest: Path) -> Path:
    fig, ax, cax, pc, meta = _prepara(stato, dominio, "pv_jet")
    lon, lat = stato.lon, stato.lat
    pv = stato.campi["pv_300_200"]
    jet = stato.campi["mod250"] * 1.943844
    liv = [0.2, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8]
    cf = d.campo_ombreggiato(ax, pc, lon, lat, pv, liv, d.CMAP_PV, extend="max")
    d.isolinee(ax, pc, lon, lat, jet, [50, 70, 90, 110, 130, 150], colore="#4a148c", spessore=0.85, fmt="%d")
    if stato.ha("u250", "v250"):
        d.barbette(ax, pc, lon, lat, stato.campi["u250"], stato.campi["v250"])
    d.citta(ax, dominio, pc)
    d.colorbar(cax, cf, liv)
    d.testata_e_piede(fig, ax, stato, dominio, meta["titolo"], meta["sottotitolo"], "PVU  ·  getto in nodi")
    return d.salva(fig, dest)


def dt_2pvu(stato: Stato, dominio: str, dest: Path) -> Path:
    fig, ax, cax, pc, meta = _prepara(stato, dominio, "dt_2pvu")
    lon, lat = stato.lon, stato.lat
    th = stato.campi["theta_dt"]
    liv = list(range(280, 381, 5))
    cf = d.campo_ombreggiato(ax, pc, lon, lat, th, liv, d.CMAP_THETA_DT, extend="both")
    d.isolinee(ax, pc, lon, lat, th, liv[::2], colore="#111", spessore=0.4, fmt="%d")
    if stato.ha("vo_925_850"):
        vo = stato.campi["vo_925_850"] * 1.0e5
        # solo vorticità ciclonica (positiva), come nelle carte di riferimento
        d.isolinee(ax, pc, lon, lat, vo, [6, 10, 14, 18, 22],
                   colore="#4a148c", spessore=0.75, fmt="%d")
    if stato.ha("u_dt", "v_dt"):
        d.barbette(ax, pc, lon, lat, stato.campi["u_dt"], stato.campi["v_dt"])
    d.citta(ax, dominio, pc)
    d.colorbar(cax, cf, liv[::2])
    d.testata_e_piede(fig, ax, stato, dominio, meta["titolo"], meta["sottotitolo"], "K sulla superficie a 2 PVU  ·  vento in nodi")
    return d.salva(fig, dest)


def isent_330(stato: Stato, dominio: str, dest: Path) -> Path:
    fig, ax, cax, pc, meta = _prepara(stato, dominio, "isent_330")
    lon, lat = stato.lon, stato.lat
    pv = stato.campi["pv_330"]
    liv = [0.2, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8]
    cf = d.campo_ombreggiato(ax, pc, lon, lat, pv, liv, d.CMAP_PV, extend="max")
    if stato.ha("p_330"):
        d.isolinee(ax, pc, lon, lat, stato.campi["p_330"],
                   list(range(200, 901, 50)), colore="#111", spessore=0.5, fmt="%d")
    if stato.ha("u_330", "v_330"):
        d.barbette(ax, pc, lon, lat, stato.campi["u_330"], stato.campi["v_330"])
    d.citta(ax, dominio, pc)
    d.colorbar(cax, cf, liv)
    d.testata_e_piede(fig, ax, stato, dominio, meta["titolo"], meta["sottotitolo"], "PVU  ·  pressione in hPa  ·  vento in nodi")
    return d.salva(fig, dest)


def isent_310_350(stato: Stato, dominio: str, dest: Path) -> Path:
    fig, ax, cax, pc, meta = _prepara(stato, dominio, "isent_310_350")
    lon, lat = stato.lon, stato.lat
    pv = stato.campi["pv_310"]
    liv = [0.2, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 8]
    cf = d.campo_ombreggiato(ax, pc, lon, lat, pv, liv, d.CMAP_PV, extend="max")
    if stato.ha("p_350"):
        d.isolinee(ax, pc, lon, lat, stato.campi["p_350"],
                   list(range(150, 701, 50)), colore="#111", spessore=0.55, fmt="%d")
    if stato.ha("u_310", "v_310"):
        d.barbette(ax, pc, lon, lat, stato.campi["u_310"], stato.campi["v_310"])
    d.citta(ax, dominio, pc)
    d.colorbar(cax, cf, liv)
    d.testata_e_piede(fig, ax, stato, dominio, meta["titolo"], meta["sottotitolo"], "PVU a 310 K  ·  pressione a 350 K, hPa")
    return d.salva(fig, dest)


def coupling_index(stato: Stato, dominio: str, dest: Path) -> Path:
    fig, ax, cax, pc, meta = _prepara(stato, dominio, "coupling_index")
    lon, lat = stato.lon, stato.lat
    ci = stato.campi["coupling"]
    liv = list(range(-10, 51, 4))
    cf = d.campo_ombreggiato(ax, pc, lon, lat, ci, liv, d.CMAP_COUPLING, extend="both")
    d.isolinee(ax, pc, lon, lat, ci, liv, colore="#111", spessore=0.35, fmt="%d")
    if stato.ha("mslp"):
        msl = stato.campi["mslp"]
        d.isolinee(ax, pc, lon, lat, msl, _livelli_int(np.nanmin(msl), np.nanmax(msl), 4),
                   colore="#222", spessore=0.55, fmt="%d")
    d.citta(ax, dominio, pc)
    d.colorbar(cax, cf, liv)
    d.testata_e_piede(fig, ax, stato, dominio, meta["titolo"], meta["sottotitolo"], "K (valori bassi: troposfera accoppiata)")
    return d.salva(fig, dest)


DISEGNATORI = {
    "mslp_precip": mslp_precip,
    "t850_vento10": t850_vento10,
    "h500": h500,
    "ivt_h700": ivt_h700,
    "h850_cape_shear": h850_cape_shear,
    "spessore_mslp_jet": spessore_mslp_jet,
    "h700_pw": h700_pw,
    "thetae850": thetae850,
    "pv_jet": pv_jet,
    "dt_2pvu": dt_2pvu,
    "isent_330": isent_330,
    "isent_310_350": isent_310_350,
    "coupling_index": coupling_index,
}


def requisiti_ok(stato: Stato, chiave: str) -> bool:
    richiesti = PRODOTTI[chiave].get("richiede") or ()
    return stato.ha(*richiesti)


def disegna_prodotto(chiave: str, stato: Stato, dominio: str, dest: Path) -> Path | None:
    if chiave not in DISEGNATORI:
        return None
    if not requisiti_ok(stato, chiave):
        return None
    try:
        return DISEGNATORI[chiave](stato, dominio, dest)
    except Exception as e:  # noqa: BLE001
        print(f"  ! prodotto {chiave} non disegnato (F{stato.step:03d}): {e}")
        return None
