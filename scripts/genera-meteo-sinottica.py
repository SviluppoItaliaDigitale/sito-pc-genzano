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
from matplotlib.colors import LinearSegmentedColormap
import cartopy.crs as ccrs
import cartopy.feature as cfeature
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
               "geopotential_height_500hPa", "wind_speed_500hPa", "wind_direction_500hPa")


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
    for fi, hi in enumerate(indici):
        t850 = campo(results, "temperature_850hPa", nlat, nlon, hi)
        mslp = campo(results, "pressure_msl", nlat, nlon, hi)
        g500 = campo(results, "geopotential_height_500hPa", nlat, nlon, hi)
        ws = campo(results, "wind_speed_500hPa", nlat, nlon, hi)
        wd = campo(results, "wind_direction_500hPa", nlat, nlon, hi)
        # vento -> componenti (kt). dir = direzione DA cui spira.
        wr = np.radians(wd)
        u = -(ws / 1.852) * np.sin(wr)
        v = -(ws / 1.852) * np.cos(wr)

        fig = plt.figure(figsize=(8.2, 7.2), dpi=100)
        ax = plt.axes(projection=proj)
        ax.set_extent([LON_MIN, LON_MAX, LAT_MIN, LAT_MAX], crs=proj)

        cf = ax.contourf(lon2d, lat2d, t850, levels=t_levels, cmap=cmap,
                         vmin=tlo, vmax=thi, extend="both", transform=proj, alpha=0.92)
        # geopotenziale 500 hPa (saccature/promontori)
        cg = ax.contour(lon2d, lat2d, g500, levels=g_levels, colors="#5b2a86",
                        linewidths=0.9, linestyles="dashed", transform=proj)
        ax.clabel(cg, inline=True, fontsize=6.5, fmt="%d")
        # isobare MSLP
        cp = ax.contour(lon2d, lat2d, mslp, levels=p_levels, colors="#111111",
                        linewidths=1.0, transform=proj)
        ax.clabel(cp, inline=True, fontsize=7, fmt="%d")
        # barbe vento 500 hPa, sottocampionate
        s = 2
        ax.barbs(lon2d[::s, ::s], lat2d[::s, ::s], u[::s, ::s], v[::s, ::s],
                 length=4.6, linewidth=0.45, color="#23408f", transform=proj)

        ax.add_feature(coast)
        ax.add_feature(borders)
        ax.plot(GENZANO[1], GENZANO[0], marker="*", markersize=11, color="#b8860b",
                markeredgecolor="#ffffff", markeredgewidth=0.8, transform=proj, zorder=6)

        ft = parsed[hi]
        valid_roma = ft.replace(tzinfo=datetime.timezone.utc).astimezone(TZ_ROMA) if TZ_ROMA else ft
        ax.set_title(
            f"Carta sinottica Italia — 850 hPa (colore), MSLP (nero), 500 hPa (viola), vento 500 hPa\n"
            f"valido {GIORNI[ft.weekday()]} {ft.day:02d}/{ft.month:02d} ore {ft.hour:02d} UTC "
            f"({valid_roma.hour:02d}:00 ora italiana)",
            fontsize=9, fontweight="bold")

        cb = fig.colorbar(cf, ax=ax, orientation="vertical", shrink=0.8, pad=0.02, ticks=range(-30, 40, 5))
        cb.set_label("Temperatura a 850 hPa (°C)", fontsize=8)
        cb.ax.tick_params(labelsize=7)
        fig.text(0.5, 0.030, "Elaborazione grafica del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma",
                 ha="center", fontsize=7.2, fontweight="bold", color="#003366")
        fig.text(0.5, 0.012, "Dati: Open-Meteo (modelli ECMWF) · dato indicativo, per le allerte vale il Centro Funzionale Regionale del Lazio",
                 ha="center", fontsize=6, color="#555555")
        fig.subplots_adjust(left=0.02, right=0.98, top=0.9, bottom=0.06)

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
