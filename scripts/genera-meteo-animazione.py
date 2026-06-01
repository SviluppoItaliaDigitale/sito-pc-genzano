#!/usr/bin/env python3
"""
OPZIONE A — Animazione della cartina meteo del Lazio (choropleth animata).

Estende la cartina statica `genera-meteo-lazio.py` aggiungendo il MOVIMENTO:
mostra l'evoluzione della temperatura e del cielo previsti nelle prossime ~72 ore
(frame ogni 6 ore) come **SVG animato** auto-ospitato, senza JavaScript e senza
embed di terzi. Dati aperti Open-Meteo (modelli ECMWF, licenza CC-BY, nessuna chiave).

Tecnica: un solo set di geometrie province (peso minimo), con il `fill` animato via
SMIL `calcMode="discrete"` sui colori dei vari frame; le pillole (nome+icona+temp) e
la fascia oraria sono gruppi per-frame con opacità animata. SMIL discreto = scatti
netti tra un frame e l'altro, deterministico, riprodotto anche dentro <img>.

Output:
  - static/images/meteo-lazio-animata.svg   animazione 72h
  - data/meteo_animazione.json              metadati (n. frame, span, aggiornato)

Uso:
  python3 scripts/genera-meteo-animazione.py                 # fetch live
  python3 scripts/genera-meteo-animazione.py --from-file h.json   # test offline

Idempotente: riscrive sempre l'output.
"""
import json, math, os, sys, ssl, urllib.request, datetime, importlib.util

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# riuso delle funzioni della cartina statica (filename con trattino -> import per path)
_spec = importlib.util.spec_from_file_location(
    "genera_meteo_lazio", os.path.join(ROOT, "scripts", "genera-meteo-lazio.py"))
ml = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ml)

colore, wmo, icona_svg = ml.colore, ml.wmo, ml.icona_svg
CAPOLUOGHI, GENZANO = ml.CAPOLUOGHI, ml.GENZANO
TEMP_MIN, TEMP_MAX = ml.TEMP_MIN, ml.TEMP_MAX
GIORNI_BREVI, MESI_IT = ml.GIORNI_BREVI, ml.MESI_IT
GEO = ml.GEO

try:
    from zoneinfo import ZoneInfo
    TZ_ROMA = ZoneInfo("Europe/Rome")
except Exception:
    TZ_ROMA = None

OUT_SVG = os.path.join(ROOT, "static", "images", "meteo-lazio-animata.svg")
OUT_JSON = os.path.join(ROOT, "data", "meteo_animazione.json")

N_FRAME = 12          # 12 frame
STEP_H = 6            # ogni 6 ore -> copre 72 ore
DUR_S = 24            # durata del ciclo (2 s/frame)

# Punti campione: 5 capoluoghi + Genzano (ultimo)
PUNTI = [(c[0], c[1], c[2]) for c in CAPOLUOGHI] + [("Genzano", GENZANO[0], GENZANO[1])]
# posizione manuale delle pillole (lon,lat) — come la cartina statica
LBL = {"Viterbo": (12.10, 42.42), "Rieti": (12.86, 42.40), "Roma": (12.50, 41.99),
       "Latina": (13.00, 41.42), "Frosinone": (13.45, 41.66)}


# ----------------------------------------------------------- fetch Open-Meteo (orario)
def _get(url):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "pc-genzano-meteo/1.0"})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        return json.loads(r.read().decode("utf-8"))


def fetch_hourly():
    lats = ",".join(f"{p[1]}" for p in PUNTI)
    lons = ",".join(f"{p[2]}" for p in PUNTI)
    url = ("https://api.open-meteo.com/v1/forecast?latitude=" + lats + "&longitude=" + lons +
           "&hourly=temperature_2m,weather_code&timezone=Europe%2FRome&forecast_days=4")
    return _get(url)


# ----------------------------------------------------------- proiezione (come build_svg)
LON0, LAT0, LON1, LAT1 = 11.25, 40.55, 14.15, 42.98
Wmap = 580
_latmid = (LAT0 + LAT1) / 2
_sx = Wmap / ((LON1 - LON0) * math.cos(math.radians(_latmid)))
_sy = _sx
Hmap = (LAT1 - LAT0) * _sy


def px(lon, lat):
    return (lon - LON0) * math.cos(math.radians(_latmid)) * _sx, (LAT1 - lat) * _sy


def ring_path(ring):
    d = ""
    for i, (lon, lat) in enumerate(ring):
        x, y = px(lon, lat)
        d += ("M" if i == 0 else "L") + f"{x:.0f},{y:.0f}"
    return d + "Z"


# ----------------------------------------------------------- selezione frame
def scegli_frame(hourly, now):
    """Restituisce gli indici orari da usare come frame: prossime ore, a passo 6h.
    `hourly` e' la lista di oggetti Open-Meteo (uno per punto): i tempi sono comuni."""
    times = hourly[0]["hourly"]["time"]
    parsed = [datetime.datetime.fromisoformat(t) for t in times]
    floor = now.replace(minute=0, second=0, microsecond=0, tzinfo=None)
    idx = []
    for i, t in enumerate(parsed):
        if t >= floor and t.hour % STEP_H == 0:
            idx.append(i)
        if len(idx) >= N_FRAME:
            break
    # fallback: se ne troviamo pochi (fine serie), riempi all'indietro
    if len(idx) < N_FRAME:
        start = max(0, len(parsed) - N_FRAME * STEP_H)
        idx = list(range(start, len(parsed), STEP_H))[:N_FRAME]
    return idx, parsed


def serie_per_punto(hourly, p_index, indici):
    h = hourly[p_index]["hourly"]
    temps = h["temperature_2m"]
    codes = h["weather_code"]
    return [(temps[i], codes[i]) for i in indici]


# ----------------------------------------------------------- pillola provincia (per frame)
def pillola(nome, lx, ly, t, wc):
    col = colore(t)
    desc, ico = wmo(wc)
    pw, ph = 104, 46
    return (f'<g>'
            f'<rect x="{lx-pw/2:.1f}" y="{ly-ph/2:.1f}" width="{pw}" height="{ph}" rx="9" '
            f'fill="#ffffff" fill-opacity="0.93" stroke="{col}" stroke-width="1.6"/>'
            f'<text x="{lx:.1f}" y="{ly-9:.1f}" font-size="12.5" font-weight="700" '
            f'text-anchor="middle" fill="#003366">{nome}</text>'
            f'{icona_svg(ico, lx-26, ly+9, 8)}'
            f'<text x="{lx+12:.1f}" y="{ly+15:.1f}" font-size="20" font-weight="800" '
            f'text-anchor="middle" fill="#1a1a1a">{round(t)}&#176;</text>'
            f'</g>')


# ----------------------------------------------------------- build SVG animato
def build(hourly, now):
    geo = json.load(open(GEO))
    indici, parsed = scegli_frame(hourly, now)
    nfr = len(indici)

    # serie per provincia + Genzano
    serie = {}
    for pi, p in enumerate(PUNTI):
        serie[p[0]] = serie_per_punto(hourly, pi, indici)

    # contesto regioni confinanti (statico)
    contesto = "".join(
        f'<path d="{ring_path(r)}" fill="#f0f2f4" stroke="#e2e7eb" stroke-width="0.7"/>'
        for r in geo["contesto"])

    # geometria province: UNA volta sola, fill animato sui colori dei frame
    prov_svg = ""
    for pr in geo["province"]:
        nome = pr["nome"]
        cols = ";".join(colore(serie[nome][k][0]) for k in range(nfr))
        anim = (f'<animate attributeName="fill" dur="{DUR_S}s" repeatCount="indefinite" '
                f'calcMode="discrete" values="{cols}"/>')
        for ring in pr["rings"]:
            prov_svg += (f'<path d="{ring_path(ring)}" fill="{colore(serie[nome][0][0])}" '
                         f'fill-opacity="0.85" stroke="#ffffff" stroke-width="1.6">{anim}</path>')

    # marker Genzano (statico)
    gx, gy = px(GENZANO[1], GENZANO[0])
    marker = (f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="5.5" fill="#b8860b" '
              f'stroke="#ffffff" stroke-width="2"/>')

    # gruppi per-frame: pillole 5 province + fascia oraria, opacita' discreta
    frame_groups = ""
    for k in range(nfr):
        pills = ""
        for nome in ("Viterbo", "Rieti", "Roma", "Latina", "Frosinone"):
            lx, ly = px(LBL[nome][0], LBL[nome][1])
            t, wc = serie[nome][k]
            pills += pillola(nome, lx, ly, t, wc)
        # fascia oraria del frame (con dato Genzano)
        ft = parsed[indici[k]]
        gz_t, gz_wc = serie["Genzano"][k]
        gz_desc, _ = wmo(gz_wc)
        etich = f"{GIORNI_BREVI[ft.weekday()]} {ft.day} {MESI_IT[ft.month][:3]} · ore {ft.hour:02d}:00"
        banner = (f'<g transform="translate(8,{Hmap-40:.0f})">'
                  f'<rect x="0" y="0" width="360" height="32" rx="9" fill="#003366" '
                  f'stroke="#b8860b" stroke-width="1.4"/>'
                  f'<text x="12" y="21" font-size="13" font-weight="700" fill="#ffffff">{etich}</text>'
                  f'<text x="348" y="21" font-size="13" font-weight="800" text-anchor="end" '
                  f'fill="#ffd166">Genzano di Roma {round(gz_t)}&#176;</text>'
                  f'</g>')
        # valori opacita' discreti: 1 solo nella propria finestra
        vals = ";".join("1" if j == k else "0" for j in range(nfr))
        frame_groups += (f'<g opacity="{1 if k==0 else 0}">'
                         f'<animate attributeName="opacity" dur="{DUR_S}s" repeatCount="indefinite" '
                         f'calcMode="discrete" values="{vals}"/>{pills}{banner}</g>')

    # legenda statica (identica alla cartina)
    PAD = 18; HEAD = 64; FOOT = 88
    W = Wmap + 2 * PAD; H = Hmap + HEAD + FOOT + PAD
    barW = min(440, W - 2 * PAD - 30); barX = (W - barW) / 2; barY = H - 64; barH = 13
    nseg = int(TEMP_MAX - TEMP_MIN); segw = barW / nseg
    segs = "".join(f'<rect x="{barX+kk*segw:.2f}" y="{barY:.1f}" width="{segw+0.6:.2f}" '
                   f'height="{barH}" fill="{colore(TEMP_MIN+kk+0.5)}"/>' for kk in range(nseg))
    ticks = ""
    for tv in (-5, 0, 5, 10, 15, 20, 25, 30, 35, 40):
        tx = barX + (tv - TEMP_MIN) / (TEMP_MAX - TEMP_MIN) * barW
        ticks += (f'<line x1="{tx:.1f}" y1="{barY:.1f}" x2="{tx:.1f}" y2="{barY+barH+3:.1f}" '
                  f'stroke="#495057" stroke-width="0.9"/>'
                  f'<text x="{tx:.1f}" y="{barY+barH+15:.1f}" font-size="9.5" '
                  f'text-anchor="middle" fill="#495057">{tv}&#176;</text>')
    leg = (f'<text x="{barX:.1f}" y="{barY-5:.1f}" font-size="10" fill="#495057">'
           f'Temperatura (&#176;C)</text>{segs}'
           f'<rect x="{barX:.1f}" y="{barY:.1f}" width="{barW:.1f}" height="{barH}" rx="3" '
           f'fill="none" stroke="#adb5bd" stroke-width="0.8"/>{ticks}')

    titolo = (f'<text x="{PAD}" y="26" font-size="17" font-weight="800" fill="#003366">'
              f'Lazio — previsione animata 72 ore</text>'
              f'<text x="{PAD}" y="45" font-size="11" fill="#495057">'
              f'Temperatura e cielo previsti nelle province, fotogramma ogni 6 ore.</text>')
    fonte = (f'<text x="{W/2:.0f}" y="{H-21:.0f}" font-size="10.5" font-weight="700" text-anchor="middle" '
             f'fill="#003366">Elaborazione grafica del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma</text>'
             f'<text x="{W/2:.0f}" y="{H-8:.0f}" font-size="8.5" text-anchor="middle" '
             f'fill="#6c757d">Dati: Open-Meteo (modelli ECMWF) &#183; dato indicativo, '
             f'per le allerte vale il Centro Funzionale Regionale del Lazio</text>')

    aria = (f"Animazione della previsione meteo del Lazio per le prossime 72 ore: "
            f"temperatura e cielo previsti nelle province, con dettaglio per Genzano di Roma. "
            f"{nfr} fotogrammi a passo di 6 ore.")
    inner = (
        f'<rect x="0" y="0" width="{W:.0f}" height="{H:.0f}" fill="#ffffff"/>'
        f'<defs><clipPath id="mapclipA"><rect x="0" y="0" width="{Wmap:.0f}" height="{Hmap:.0f}"/></clipPath></defs>'
        f'{titolo}'
        f'<g transform="translate({PAD},{HEAD})" clip-path="url(#mapclipA)">'
        f'{contesto}{prov_svg}{marker}{frame_groups}</g>'
        f'{leg}{fonte}')
    # cornice di microtesto attorno a tutto (banda dedicata, non sovrapposta al contenuto)
    F = 13
    W2, H2 = W + 2 * F, H + 2 * F
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W2:.0f} {H2:.0f}" '
        f'font-family="Trebuchet MS,Verdana,Arial,sans-serif" role="img" aria-label="{aria}">'
        f'<rect x="0" y="0" width="{W2:.0f}" height="{H2:.0f}" fill="#ffffff"/>'
        f'<g transform="translate({F},{F})">{inner}</g>'
        f'{ml.microtext_frame(W2, H2, F, now.year)}'
        f'</svg>')
    meta = {
        "aggiornato": now.strftime("%Y-%m-%dT%H:%M"),
        "frame": nfr,
        "passo_ore": STEP_H,
        "durata_s": DUR_S,
        "fonte": "Open-Meteo (modelli ECMWF)",
        "span_da": parsed[indici[0]].strftime("%Y-%m-%dT%H:%M"),
        "span_a": parsed[indici[-1]].strftime("%Y-%m-%dT%H:%M"),
    }
    return svg, meta


def main():
    now = datetime.datetime.now(TZ_ROMA)
    if len(sys.argv) >= 3 and sys.argv[1] == "--from-file":
        hourly = json.load(open(sys.argv[2]))
    else:
        hourly = fetch_hourly()
    svg, meta = build(hourly, now)
    os.makedirs(os.path.dirname(OUT_SVG), exist_ok=True)
    open(OUT_SVG, "w", encoding="utf-8").write(svg)
    json.dump(meta, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"OK  {OUT_SVG} ({len(svg)} byte, {meta['frame']} frame)")
    print(f"OK  {OUT_JSON}")


if __name__ == "__main__":
    main()
