"""Disegno delle carte in stile professionale, con testata istituzionale e attribuzione."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
import matplotlib.ticker as mticker
import numpy as np
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap, ListedColormap
from matplotlib.patches import FancyBboxPatch

from .config import (
    BLU,
    CITTA_EUROPA,
    CITTA_ITALIA,
    CONFINE,
    CONFINE_IT,
    COSTA,
    DOMINI,
    FONDO_MARE,
    FONDO_TERRA,
    FONDO_TITOLO,
    MODELLI,
    data_italiana,
)
from .campi import Stato

# Effetto contrasto per testi e isolinee sopra i campi colorati.
_HALO = [pe.withStroke(linewidth=2.2, foreground="white")]
_HALO_SOTTILE = [pe.withStroke(linewidth=1.4, foreground="white")]


def cmap_da(colori, nome="custom"):
    return LinearSegmentedColormap.from_list(nome, colori)


# Tavolozze ispirate alle carte sinottiche classiche (stile Albany),
# con transizioni più morbide e un contrasto adatto alla stampa e al web.
CMAP_PIOGGIA = ListedColormap(
    [
        "#d6f5d6", "#a8e6a3", "#5fc85a", "#22a01c",
        "#f6f07a", "#ffc14d", "#ff8c1a", "#f0470f",
        "#d41212", "#a80c5a", "#7a0878", "#4b0560", "#2a0336",
    ]
)
LIV_PIOGGIA = [0.2, 0.5, 1, 2, 4, 6, 8, 12, 16, 24, 32, 48, 64]

CMAP_TEMP = cmap_da(
    [
        "#4b0082", "#2e2e9c", "#1e6ad4", "#3aa0ff", "#7ed0ff",
        "#c8f0c8", "#f8f8b0", "#ffd24d", "#ff8c1a", "#e32222",
        "#9b0a4a", "#5a0540",
    ],
    "temp",
)

CMAP_VORT = cmap_da(
    ["#1a237e", "#3949ab", "#90caf9", "#ffffff", "#ffe082", "#fb8c00", "#c62828", "#6a1b9a"],
    "vort",
)
CMAP_OMEGA = cmap_da(
    ["#4a148c", "#1565c0", "#81d4fa", "#ffffff", "#ffe082", "#ef6c00", "#b71c1c"],
    "omega",
)
CMAP_IVT = cmap_da(
    ["#f7fbff", "#c6dbef", "#6baed6", "#2171b5", "#08306b", "#4a148c", "#f06292"],
    "ivt",
)
CMAP_CAPE = cmap_da(
    ["#ffffff", "#fff8c0", "#ffd54f", "#ff8f00", "#e53935", "#6a1b9a"],
    "cape",
)
CMAP_PW = cmap_da(
    ["#ffffe5", "#d9f0a3", "#78c679", "#238443", "#004529", "#08306b"],
    "pw",
)
CMAP_THETAE = cmap_da(
    ["#313695", "#74add1", "#e0f3f8", "#fee090", "#f46d43", "#a50026", "#67001f"],
    "thetae",
)
CMAP_SPESSORE = cmap_da(
    ["#08306b", "#2171b5", "#6baed6", "#f7f7f7", "#fd8d3c", "#d94801", "#7f0000"],
    "spessore",
)
CMAP_JET = cmap_da(
    ["#ffffff", "#c6dbef", "#6baed6", "#2171b5", "#08306b", "#7a0177", "#fa9fb5"],
    "jet",
)
CMAP_PV = cmap_da(
    ["#ffffd9", "#edf8b1", "#7fcdbb", "#2c7fb8", "#253494", "#081d58", "#4a004a"],
    "pv",
)
CMAP_THETA_DT = cmap_da(
    ["#5e3c99", "#3f6db5", "#80cdc1", "#f7f7f7", "#fdb863", "#e66101", "#b2182b"],
    "thetadt",
)
CMAP_COUPLING = cmap_da(
    ["#67001f", "#d6604d", "#fddbc7", "#f7f7f7", "#d1e5f0", "#4393c3", "#053061"],
    "coupling",
)
CMAP_PRESS = cmap_da(
    ["#fff7fb", "#ece7f2", "#a6bddb", "#3690c0", "#02818a", "#016450", "#014636"],
    "pres",
)


def _proiezione(chiave: str):
    import cartopy.crs as ccrs

    cfg = DOMINI[chiave]["proj"]
    return ccrs.LambertConformal(
        central_longitude=cfg["central_longitude"],
        central_latitude=cfg["central_latitude"],
        standard_parallels=cfg["standard_parallels"],
    )


def _feature_italia():
    """Geometria dell'Italia, per evidenziare il confine nazionale."""
    import cartopy.io.shapereader as shpreader

    shp = shpreader.natural_earth(resolution="50m", category="cultural", name="admin_0_countries")
    for rec in shpreader.Reader(shp).records():
        nome = (rec.attributes.get("ADMIN") or rec.attributes.get("NAME") or "").lower()
        if nome in {"italy", "italia"}:
            return rec.geometry
    return None


_ITALIA_GEOM = None


def _italia():
    global _ITALIA_GEOM
    if _ITALIA_GEOM is None:
        try:
            _ITALIA_GEOM = _feature_italia()
        except Exception:
            _ITALIA_GEOM = False
    return _ITALIA_GEOM if _ITALIA_GEOM else None


def nuova_carta(stato: Stato, dominio: str, titolo: str, sottotitolo: str):
    """Crea figura, assi della mappa e riservati per testata, barra e piede."""
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature

    cfg = DOMINI[dominio]
    proj = _proiezione(dominio)
    pc = ccrs.PlateCarree()
    fig = plt.figure(figsize=cfg["figsize"], facecolor=FONDO_TITOLO, dpi=140)
    # [sinistra, basso, larghezza, altezza] in frazione della figura
    ax = fig.add_axes([0.03, 0.10, 0.80, 0.76], projection=proj)
    cax = fig.add_axes([0.845, 0.16, 0.018, 0.62])
    ax.set_extent(cfg["extent"], crs=pc)
    ax.set_facecolor(FONDO_MARE)
    ax.add_feature(cfeature.OCEAN.with_scale("50m"), facecolor=FONDO_MARE, zorder=0)
    ax.add_feature(cfeature.LAND.with_scale("50m"), facecolor=FONDO_TERRA, zorder=0)
    ax.add_feature(cfeature.LAKES.with_scale("50m"), facecolor="#c5d6e4", edgecolor="#7a8c99", linewidth=0.3, zorder=1)
    ax.add_feature(cfeature.COASTLINE.with_scale("50m"), edgecolor=COSTA, linewidth=0.7, zorder=4)
    ax.add_feature(cfeature.BORDERS.with_scale("50m"), edgecolor=CONFINE, linewidth=0.45, linestyle="-", zorder=4)
    geom = _italia()
    if geom is not None:
        import cartopy.feature as cfeat
        ax.add_geometries(
            [geom], crs=pc, facecolor="none", edgecolor=CONFINE_IT, linewidth=1.35, zorder=5,
        )
    gl = ax.gridlines(draw_labels=True, linewidth=0.3, color="#6a7680", alpha=0.45, linestyle="--")
    gl.top_labels = False
    gl.right_labels = False
    gl.xlabel_style = {"size": 7, "color": "#e8eef3"}
    gl.ylabel_style = {"size": 7, "color": "#e8eef3"}
    gl.xlocator = mticker.FixedLocator(range(-20, 45, 4 if dominio == "italia" else 8))
    gl.ylocator = mticker.FixedLocator(range(28, 75, 2 if dominio == "italia" else 5))
    # Le etichette delle gridline cadono sul fondo scuro della figura: le coloriamo chiare.
    return fig, ax, cax, proj, pc


def testata_e_piede(fig, ax, stato: Stato, dominio: str, titolo: str, sottotitolo: str, unita: str):
    meta = MODELLI[stato.modello]
    # Testata
    fig.patches.append(
        FancyBboxPatch(
            (0.0, 0.875), 1.0, 0.125,
            transform=fig.transFigure, facecolor=FONDO_TITOLO,
            edgecolor="none", zorder=-1, boxstyle="square,pad=0",
        )
    )
    fig.text(
        0.03, 0.965,
        "Protezione Civile di Genzano di Roma",
        color="#8fb4d4", fontsize=8.5, fontweight="normal", va="top",
        fontfamily="sans-serif",
    )
    fig.text(
        0.03, 0.932,
        titolo,
        color="white", fontsize=14.5, fontweight="bold", va="top",
        fontfamily="sans-serif",
    )
    fig.text(
        0.03, 0.895,
        sottotitolo,
        color="#d5e3ee", fontsize=8, va="top", fontfamily="sans-serif",
    )
    # Blocco orari a destra, in stile «init / valid / Fxxx»
    blocco = (
        f"{meta['nome']}  ·  {meta['risoluzione']}\n"
        f"Inizializzazione  {data_italiana(stato.corsa)}\n"
        f"Validità          {data_italiana(stato.valid)}   F{stato.step:03d}"
    )
    fig.text(
        0.97, 0.960, blocco,
        color="white", fontsize=8, va="top", ha="right",
        fontfamily="DejaVu Sans Mono", linespacing=1.45,
    )
    # Piede
    fig.patches.append(
        FancyBboxPatch(
            (0.0, 0.0), 1.0, 0.08,
            transform=fig.transFigure, facecolor=FONDO_TITOLO,
            edgecolor="none", zorder=-1, boxstyle="square,pad=0",
        )
    )
    fig.text(
        0.03, 0.048,
        f"Fonte: {meta['attribuzione']}. Elaborazione: Gruppo Comunale Volontari di "
        f"Protezione Civile di Genzano di Roma. {DOMINI[dominio]['nome']}.",
        color="#c5d4e0", fontsize=6.7, va="center",
    )
    fig.text(
        0.03, 0.022,
        "Carta modellistica di inquadramento. Non sostituisce i bollettini ufficiali "
        "del Centro Funzionale Regionale né lo stato di allerta. In emergenza chiama il 112.",
        color="#8fa3b3", fontsize=6.3, va="center",
    )
    if unita:
        fig.text(0.845, 0.795, unita, color="#e8eef3", fontsize=7.5, ha="left", va="bottom")


def citta(ax, dominio: str, pc):
    elenco = CITTA_ITALIA if dominio == "italia" else CITTA_EUROPA
    for nome, lo, la, evidenza in elenco:
        ax.plot(
            lo, la, marker="o" if nome != "Genzano" else "*",
            markersize=4.6 if evidenza else 3.4,
            color=BLU if nome != "Genzano" else "#c0392b",
            markeredgecolor="white", markeredgewidth=0.6,
            transform=pc, zorder=7,
        )
        ax.text(
            lo + 0.08, la + 0.08, nome,
            transform=pc, fontsize=6.4 if evidenza else 5.8,
            color="#1a1a1a", fontweight="bold" if evidenza else "normal",
            path_effects=_HALO_SOTTILE, zorder=7,
        )


def campo_ombreggiato(ax, pc, lon, lat, dati, livelli, cmap, extend="both", **kw):
    """Contourf su lon/lat 1D. Restituisce l'oggetto per la colorbar."""
    lon2, lat2 = np.meshgrid(lon, lat)
    norm = BoundaryNorm(livelli, cmap.N, extend=extend) if len(livelli) > 2 else None
    cf = ax.contourf(
        lon2, lat2, dati, levels=livelli, cmap=cmap, norm=norm,
        extend=extend, transform=pc, zorder=2, **kw,
    )
    return cf


def isolinee(ax, pc, lon, lat, dati, livelli, colore="#222", spessore=0.55, etichette=True,
             fmt="%d", grassetto=None, tratteggio=None):
    lon2, lat2 = np.meshgrid(lon, lat)
    stile = tratteggio or "-"
    cs = ax.contour(
        lon2, lat2, dati, levels=livelli, colors=colore, linewidths=spessore,
        linestyles=stile, transform=pc, zorder=3,
    )
    if grassetto:
        ax.contour(
            lon2, lat2, dati, levels=grassetto, colors=colore,
            linewidths=spessore * 2.0, linestyles=stile, transform=pc, zorder=3,
        )
    if etichette and len(getattr(cs, "allsegs", [])) >= 0:
        try:
            cl = ax.clabel(cs, fmt=fmt, fontsize=6.2, inline=True, inline_spacing=2)
            for t in cl:
                t.set_path_effects(_HALO_SOTTILE)
        except Exception:
            pass
    return cs


def barbette(ax, pc, lon, lat, u, v, passo=None, colore="#1a1a1a"):
    """Vento in nodi (convenzione delle carte sinottiche)."""
    if passo is None:
        # circa 18 barbette sul lato corto
        passo = max(1, int(min(len(lat), len(lon)) / 16))
    uu = u[::passo, ::passo] * 1.943844  # m/s → nodi
    vv = v[::passo, ::passo] * 1.943844
    lon2, lat2 = np.meshgrid(lon[::passo], lat[::passo])
    ax.barbs(
        lon2, lat2, uu, vv,
        length=5.2, linewidth=0.45, color=colore,
        sizes=dict(emptybarb=0.08, spacing=0.18, height=0.4),
        transform=pc, zorder=6,
    )


def colorbar(cax, cf, etichette=None):
    cax.set_facecolor(FONDO_TITOLO)
    cb = plt.colorbar(cf, cax=cax, orientation="vertical")
    cb.ax.tick_params(colors="#e8eef3", labelsize=7, length=2)
    cb.outline.set_edgecolor("#8fb4d4")
    if etichette is not None:
        cb.set_ticks(etichette)
    return cb


def salva(fig, dest: Path, dpi: int = 112) -> Path:
    """PNG a tavolozza (256 colori): circa un quarto del peso, nessuna perdita visibile sui campi a fasce."""
    import io

    from PIL import Image

    dest.parent.mkdir(parents=True, exist_ok=True)
    buf = io.BytesIO()
    fig.savefig(
        buf, format="png", dpi=dpi, facecolor=fig.get_facecolor(),
        edgecolor="none", bbox_inches="tight", pad_inches=0.08,
    )
    plt.close(fig)
    buf.seek(0)
    with Image.open(buf) as im:
        im = im.convert("RGB").quantize(colors=256, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
        im.save(dest, "PNG", optimize=True)
    return dest
