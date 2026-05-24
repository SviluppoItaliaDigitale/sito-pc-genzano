#!/usr/bin/env python3
"""
OPZIONE B — Carta sinottica Italia / Mediterraneo centrale (stile "realtime maps").

Ispirata alle carte sinottiche di livello meteorologico (es. atmos.albany.edu):
genera una carta animata dell'evoluzione prevista nelle prossime ~72 ore con i
campi classici della sinottica, focalizzata sull'Italia:

  - Shading: temperatura a 850 hPa (campo termico / avvezioni)
  - Contorni neri: pressione al livello del mare (isobare ogni 4 hPa, etichettate)
  - Contorni viola tratteggiati: geopotenziale a 500 hPa (saccature e promontori)
  - Barbe del vento a 500 hPa (corrente a getto)
  - Coste e confini da Natural Earth (Cartopy)

Dati aperti Open-Meteo (modelli ECMWF, licenza CC-BY, nessuna chiave API).
Output auto-ospitato, nessun embed di terzi (privacy-first).

Output:
  - static/images/meteo-sinottica-italia.webp   animazione (clip condivisibile)
  - static/images/meteo-sinottica-italia.png    frame statico (anteprima/fallback)
  - data/meteo_sinottica.json                   metadati

Uso:
  python3 scripts/genera-meteo-sinottica.py                  # fetch live
  python3 scripts/genera-meteo-sinottica.py --from-file g.json   # test offline (griglia salvata)

Dipendenze: numpy, matplotlib, cartopy.
"""
import json, os, sys, ssl, math, io, urllib.request, urllib.parse, datetime

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm
from matplotlib.cm import ScalarMappable
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.patheffects as pe
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_WEBP = os.path.join(ROOT, "static", "images", "meteo-sinottica-italia.webp")
OUT_PNG = os.path.join(ROOT, "static", "images", "meteo-sinottica-italia.png")
OUT_JSON = os.path.join(ROOT, "data", "meteo_sinottica.json")

try:
    from zoneinfo import ZoneInfo
    TZ_ROMA = ZoneInfo("Europe/Rome")
except Exception:
    TZ_ROMA = None

# Dominio: Italia + Mediterraneo centrale + arco alpino
LON_MIN, LON_MAX = 5.0, 20.0
LAT_MIN, LAT_MAX = 35.0, 48.0
DLON = DLAT = 0.75          # passo griglia (sinottico)
N_FRAME = 12               # 12 fotogrammi
STEP_H = 6                 # ogni 6 ore -> 72 ore
GENZANO = (41.7085, 12.6916)

HOURLY_VARS = ("pressure_msl", "temperature_850hPa",
               "geopotential_height_500hPa", "wind_speed_500hPa", "wind_direction_500hPa",
               "precipitation", "snowfall")


# ----------------------------------------------------------------- fetch a griglia
def _get(url):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "pc-genzano-meteo/1.0"})
    with urllib.request.urlopen(req, timeout=60, context=ctx) as r:
        return json.loads(r.read().decode("utf-8"))


def build_grid_coords():
    lats = list(np.arange(LAT_MAX, LAT_MIN - 1e-6, -DLAT))   # alto -> basso
    lons = list(np.arange(LON_MIN, LON_MAX + 1e-6, DLON))    # sx -> dx
    pts = [(la, lo) for la in lats for lo in lons]            # row-major
    return lats, lons, pts


def fetch_grid():
    lats, lons, pts = build_grid_coords()
    results = []
    BATCH = 120
    for i in range(0, len(pts), BATCH):
        chunk = pts[i:i + BATCH]
        q = {
            "latitude": ",".join(f"{p[0]:.4f}" for p in chunk),
            "longitude": ",".join(f"{p[1]:.4f}" for p in chunk),
            "hourly": ",".join(HOURLY_VARS),
            "timezone": "UTC",
            "forecast_days": "4",
        }
        url = "https://api.open-meteo.com/v1/forecast?" + urllib.parse.urlencode(q)
        d = _get(url)
        if isinstance(d, dict):     # batch da 1 punto -> dict singolo
            d = [d]
        results.extend(d)
    return lats, lons, results


# ----------------------------------------------------------------- selezione frame
def scegli_indici(times, now_utc):
    parsed = [datetime.datetime.fromisoformat(t) for t in times]
    floor = now_utc.replace(minute=0, second=0, microsecond=0, tzinfo=None)
    idx = [i for i, t in enumerate(parsed) if t >= floor and t.hour % STEP_H == 0][:N_FRAME]
    if len(idx) < N_FRAME:
        start = max(0, len(parsed) - N_FRAME * STEP_H)
        idx = list(range(start, len(parsed), STEP_H))[:N_FRAME]
    return idx, parsed


def campo(results, var, nlat, nlon, hour_i):
    """Estrae il campo 2D (nlat x nlon) per la variabile e l'ora dati."""
    flat = [results[p]["hourly"][var][hour_i] for p in range(nlat * nlon)]
    arr = np.array([np.nan if v is None else v for v in flat], dtype=float)
    return arr.reshape(nlat, nlon)


# ----------------------------------------------------------------- colormap temperatura 850
def cmap_t850():
    stops = [(-30, "#3b2a78"), (-20, "#3550a0"), (-10, "#3f8fc4"), (-5, "#7cc6c9"),
             (0, "#b9e0b0"), (5, "#e7f0a0"), (10, "#f7e07a"), (15, "#f6b94e"),
             (20, "#ef8a3c"), (25, "#e25b34"), (30, "#c62f37"), (38, "#8c1d3a")]
    lo, hi = stops[0][0], stops[-1][0]
    pts = [((t - lo) / (hi - lo), c) for t, c in stops]
    return LinearSegmentedColormap.from_list("t850", pts), lo, hi


# scala precipitazioni (mm/h, stile radar) e neve (cm)
PRECIP_LEVELS = [0.2, 0.5, 1, 2, 4, 8, 16, 32, 64]
PRECIP_COLORS = ["#a6d8ff", "#4aa3ff", "#2ecc71", "#a8e05f", "#f7e359", "#f5a623", "#e8412b", "#b5179e"]
SNOW_LEVELS = [0.1, 0.5, 1, 2, 5, 10]
SNOW_COLORS = ["#e6f2ff", "#bcd6ff", "#c3b6e8", "#9a7fd6", "#6f4fc0"]


def find_centers(field, lon2d, lat2d, kind, n=2):
    """Minimi (B) o massimi (A) locali della pressione, per marcare le strutture."""
    ny, nx = field.shape
    mean = float(np.nanmean(field))
    out = []
    for iy in range(1, ny - 1):
        for ix in range(1, nx - 1):
            v = field[iy, ix]
            if np.isnan(v):
                continue
            win = field[iy - 1:iy + 2, ix - 1:ix + 2].copy()
            win[1, 1] = np.nan
            nb = win[~np.isnan(win)]
            if nb.size == 0:
                continue
            if kind == "B" and v < nb.min() and v < mean - 1.0:
                out.append((v, float(lon2d[iy, ix]), float(lat2d[iy, ix])))
            if kind == "A" and v > nb.max() and v > mean + 1.0:
                out.append((v, float(lon2d[iy, ix]), float(lat2d[iy, ix])))
    out.sort(key=lambda r: r[0], reverse=(kind == "A"))
    return out[:n]


def main():
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    now_roma = datetime.datetime.now(TZ_ROMA)

    if len(sys.argv) >= 3 and sys.argv[1] == "--from-file":
        blob = json.load(open(sys.argv[2]))
        lats, lons, results = blob["lats"], blob["lons"], blob["results"]
    else:
        lats, lons, results = fetch_grid()

    nlat, nlon = len(lats), len(lons)
    times = results[0]["hourly"]["time"]
    indici, parsed = scegli_indici(times, now_utc)

    lon2d, lat2d = np.meshgrid(np.array(lons), np.array(lats))
    cmap, tlo, thi = cmap_t850()
    t_levels = np.arange(-30, 40, 2)
    p_levels = np.arange(960, 1056, 4)
    g_levels = np.arange(4800, 6120, 60)

    GIORNI = ["lun", "mar", "mer", "gio", "ven", "sab", "dom"]
    proj = ccrs.PlateCarree()
    coast = cfeature.NaturalEarthFeature("physical", "coastline", "50m",
                                         edgecolor="#333333", facecolor="none", linewidth=0.7)
    borders = cfeature.NaturalEarthFeature("cultural", "admin_0_boundary_lines_land", "50m",
                                           edgecolor="#666666", facecolor="none", linewidth=0.5)

    frames = []
    preview_path = None
    pcmap = ListedColormap(PRECIP_COLORS); pnorm = BoundaryNorm(PRECIP_LEVELS, pcmap.N)
    scmap = ListedColormap(SNOW_COLORS); snorm = BoundaryNorm(SNOW_LEVELS, scmap.N)
    land = cfeature.NaturalEarthFeature("physical", "land", "50m", facecolor="#f3efe6")
    ocean = cfeature.NaturalEarthFeature("physical", "ocean", "50m", facecolor="#dfeaf2")

    for fi, hi in enumerate(indici):
        t850 = campo(results, "temperature_850hPa", nlat, nlon, hi)
        mslp = campo(results, "pressure_msl", nlat, nlon, hi)
        g500 = campo(results, "geopotential_height_500hPa", nlat, nlon, hi)
        ws = campo(results, "wind_speed_500hPa", nlat, nlon, hi)
        wd = campo(results, "wind_direction_500hPa", nlat, nlon, hi)
        precip = campo(results, "precipitation", nlat, nlon, hi)
        snow = campo(results, "snowfall", nlat, nlon, hi)
        # vento -> componenti (kt). dir = direzione DA cui spira.
        wr = np.radians(wd)
        u = -(ws / 1.852) * np.sin(wr)
        v = -(ws / 1.852) * np.cos(wr)

        fig = plt.figure(figsize=(8.6, 7.9), dpi=100)
        ax = plt.axes(projection=proj)
        ax.set_extent([LON_MIN, LON_MAX, LAT_MIN, LAT_MAX], crs=proj)

        # sfondo terra/mare tenue
        ax.add_feature(land, zorder=0)
        ax.add_feature(ocean, zorder=0)
        # campo termico 850 hPa (sfondo, attenuato)
        cf = ax.contourf(lon2d, lat2d, t850, levels=t_levels, cmap=cmap,
                         vmin=tlo, vmax=thi, extend="both", transform=proj, alpha=0.60, zorder=1)
        # precipitazioni (pioggia) a colori stile radar
        pr = np.where(precip >= PRECIP_LEVELS[0], precip, np.nan)
        if np.isfinite(pr).any():
            ax.contourf(lon2d, lat2d, pr, levels=PRECIP_LEVELS, cmap=pcmap, norm=pnorm,
                        extend="max", alpha=0.85, transform=proj, zorder=3)
        # neve (palette viola)
        sn = np.where(snow >= SNOW_LEVELS[0], snow, np.nan)
        if np.isfinite(sn).any():
            ax.contourf(lon2d, lat2d, sn, levels=SNOW_LEVELS, cmap=scmap, norm=snorm,
                        extend="max", alpha=0.92, transform=proj, zorder=4)
        # isoterma 0 °C a 850 hPa (limite indicativo pioggia/neve)
        try:
            ci = ax.contour(lon2d, lat2d, t850, levels=[0], colors="#0050b3",
                            linewidths=1.6, linestyles=(0, (5, 2)), transform=proj, zorder=5)
            ax.clabel(ci, inline=True, fontsize=6, fmt="0°C")
        except Exception:
            pass
        # geopotenziale 500 hPa (saccature/promontori)
        cg = ax.contour(lon2d, lat2d, g500, levels=g_levels, colors="#5b2a86",
                        linewidths=0.9, linestyles="dashed", transform=proj, zorder=5)
        ax.clabel(cg, inline=True, fontsize=6.5, fmt="%d")
        # isobare MSLP
        cp = ax.contour(lon2d, lat2d, mslp, levels=p_levels, colors="#111111",
                        linewidths=1.0, transform=proj, zorder=6)
        ax.clabel(cp, inline=True, fontsize=7, fmt="%d")
        # barbe vento 500 hPa, sottocampionate
        s = 2
        ax.barbs(lon2d[::s, ::s], lat2d[::s, ::s], u[::s, ::s], v[::s, ::s],
                 length=4.6, linewidth=0.45, color="#23408f", transform=proj, zorder=6)

        ax.add_feature(coast, zorder=7)
        ax.add_feature(borders, zorder=7)

        # minimi (B) e massimi (A) di pressione, con valore
        stroke = [pe.withStroke(linewidth=2.4, foreground="white")]
        for vv, lo_, la_ in find_centers(mslp, lon2d, lat2d, "B"):
            ax.text(lo_, la_, "B", color="#d9001b", fontsize=17, fontweight="bold",
                    ha="center", va="center", transform=proj, zorder=8, path_effects=stroke)
            ax.text(lo_, la_ - 0.5, f"{round(vv)}", color="#d9001b", fontsize=7,
                    ha="center", va="top", transform=proj, zorder=8, path_effects=stroke)
        for vv, lo_, la_ in find_centers(mslp, lon2d, lat2d, "A"):
            ax.text(lo_, la_, "A", color="#0050b3", fontsize=17, fontweight="bold",
                    ha="center", va="center", transform=proj, zorder=8, path_effects=stroke)
            ax.text(lo_, la_ - 0.5, f"{round(vv)}", color="#0050b3", fontsize=7,
                    ha="center", va="top", transform=proj, zorder=8, path_effects=stroke)

        # Genzano di Roma
        ax.plot(GENZANO[1], GENZANO[0], marker="*", markersize=13, color="#b8860b",
                markeredgecolor="#ffffff", markeredgewidth=0.9, transform=proj, zorder=9)
        ax.text(GENZANO[1] + 0.15, GENZANO[0] + 0.12, "Genzano di Roma", fontsize=6.8,
                fontweight="bold", color="#1a1a1a", transform=proj, zorder=9, path_effects=stroke)

        ft = parsed[hi]
        valid_roma = ft.replace(tzinfo=datetime.timezone.utc).astimezone(TZ_ROMA) if TZ_ROMA else ft
        ax.set_title(
            f"Carta sinottica Italia — precipitazioni e neve (colore), 850 hPa, isobare MSLP, 500 hPa, vento, minimi/massimi\n"
            f"valido {GIORNI[ft.weekday()]} {ft.day:02d}/{ft.month:02d} ore {ft.hour:02d} UTC "
            f"({valid_roma.hour:02d}:00 ora italiana)",
            fontsize=8.5, fontweight="bold")

        cb = fig.colorbar(cf, ax=ax, orientation="vertical", shrink=0.78, pad=0.01, ticks=range(-30, 40, 5))
        cb.set_label("Temperatura 850 hPa (°C)", fontsize=7.5)
        cb.ax.tick_params(labelsize=6.5)
        cb2 = fig.colorbar(ScalarMappable(norm=pnorm, cmap=pcmap), ax=ax, orientation="horizontal",
                           shrink=0.7, pad=0.07, aspect=45, ticks=PRECIP_LEVELS)
        cb2.set_label("Precipitazione (mm/h) · neve in viola", fontsize=7)
        cb2.ax.tick_params(labelsize=6)
        fig.text(0.5, 0.028, "Elaborazione grafica del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma",
                 ha="center", fontsize=7.2, fontweight="bold", color="#003366")
        fig.text(0.5, 0.011, "Dati: Open-Meteo (modelli ECMWF) · dato indicativo, per le allerte vale il Centro Funzionale Regionale del Lazio",
                 ha="center", fontsize=6, color="#555555")
        fig.subplots_adjust(left=0.02, right=0.98, top=0.89, bottom=0.12)

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        frames.append(Image.open(buf).convert("RGB"))
        if fi == 0:
            preview_path = OUT_PNG
            frames[0].save(OUT_PNG)

    os.makedirs(os.path.dirname(OUT_WEBP), exist_ok=True)
    frames[0].save(OUT_WEBP, save_all=True, append_images=frames[1:],
                   duration=750, loop=0, format="WEBP", quality=72, method=4)

    meta = {
        "aggiornato": now_roma.strftime("%Y-%m-%dT%H:%M"),
        "frame": len(frames),
        "passo_ore": STEP_H,
        "dominio": {"lon": [LON_MIN, LON_MAX], "lat": [LAT_MIN, LAT_MAX]},
        "griglia": {"nlat": nlat, "nlon": nlon, "passo_gradi": DLON},
        "campi": list(HOURLY_VARS),
        "fonte": "Open-Meteo (modelli ECMWF)",
    }
    json.dump(meta, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    sz = os.path.getsize(OUT_WEBP) / 1024
    print(f"OK  {OUT_WEBP} ({sz:.0f} KB, {len(frames)} frame, griglia {nlat}x{nlon})")
    print(f"OK  {OUT_PNG}")
    print(f"OK  {OUT_JSON}")


if __name__ == "__main__":
    main()
