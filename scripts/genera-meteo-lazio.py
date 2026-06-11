#!/usr/bin/env python3
"""
Genera la cartina meteo del Lazio (aree colorate per provincia) e il riquadro
meteo di Genzano di Roma, a partire dai dati aperti Open-Meteo (modelli ECMWF,
licenza CC-BY, nessuna chiave API).

Output:
  - static/images/meteo-lazio.svg     mappa choropleth (temperatura + cielo per provincia)
  - data/meteo_genzano.json           dati del riquadro Genzano (oggi + prossimi giorni)

Geometria: data/meteo-lazio-geo.json (province del Lazio + contesto regioni confinanti),
estratto una tantum dai confini ISTAT (openpolis/geojson-italy), così il generatore
orario non scarica i grandi file nazionali.

Uso:
  python3 scripts/genera-meteo-lazio.py            # fetch live (runner CI / locale con rete)
  python3 scripts/genera-meteo-lazio.py --from-file map.json card.json   # test offline

Idempotente: sovrascrive sempre i due output con i dati del giorno.
"""
import json, math, sys, os, time, urllib.request, urllib.error, datetime, ssl

try:
    from zoneinfo import ZoneInfo
    TZ_ROMA = ZoneInfo("Europe/Rome")
except Exception:  # tzdata assente: fallback orario di sistema
    TZ_ROMA = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEO = os.path.join(ROOT, "data", "meteo-lazio-geo.json")
OUT_SVG = os.path.join(ROOT, "static", "images", "meteo-lazio.svg")
OUT_JSON = os.path.join(ROOT, "data", "meteo_genzano.json")

# Capoluoghi di provincia del Lazio (per il colore/etichetta di ogni area)
CAPOLUOGHI = [
    ("Viterbo",   42.42, 12.10),
    ("Rieti",     42.40, 12.86),
    ("Roma",      41.90, 12.50),
    ("Latina",    41.47, 12.90),
    ("Frosinone", 41.64, 13.34),
]
GENZANO = (41.7085, 12.6916)

GIORNI_IT = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
GIORNI_BREVI = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
MESI_IT = ["", "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
           "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"]

# WMO weather code -> (descrizione italiana, chiave icona)
WMO = {
    0: ("Sereno", "sole"),
    1: ("Prevalentemente sereno", "sole-nuvola"),
    2: ("Parzialmente nuvoloso", "sole-nuvola"),
    3: ("Coperto", "nuvola"),
    45: ("Nebbia", "nebbia"), 48: ("Nebbia", "nebbia"),
    51: ("Pioggerella", "pioggia"), 53: ("Pioggerella", "pioggia"), 55: ("Pioggerella", "pioggia"),
    56: ("Pioggerella gelata", "pioggia"), 57: ("Pioggerella gelata", "pioggia"),
    61: ("Pioggia debole", "pioggia"), 63: ("Pioggia", "pioggia"), 65: ("Pioggia forte", "pioggia"),
    66: ("Pioggia gelata", "pioggia"), 67: ("Pioggia gelata", "pioggia"),
    71: ("Neve debole", "neve"), 73: ("Neve", "neve"), 75: ("Neve forte", "neve"), 77: ("Neve", "neve"),
    80: ("Rovesci", "pioggia"), 81: ("Rovesci", "pioggia"), 82: ("Rovesci forti", "pioggia"),
    85: ("Rovesci di neve", "neve"), 86: ("Rovesci di neve", "neve"),
    95: ("Temporale", "temporale"), 96: ("Temporale con grandine", "temporale"), 99: ("Temporale con grandine", "temporale"),
}

def wmo(code):
    return WMO.get(int(code), ("Coperto", "nuvola"))

# ---------------------------------------------------------------- icone vettoriali
# Ogni funzione restituisce un <g> SVG centrato in (cx,cy), scala s (raggio ~s).
def _sun(cx, cy, s, col="#f6a800"):
    rays = ""
    for k in range(8):
        a = math.radians(k * 45)
        x1 = cx + math.cos(a) * s * 1.05; y1 = cy + math.sin(a) * s * 1.05
        x2 = cx + math.cos(a) * s * 1.55; y2 = cy + math.sin(a) * s * 1.55
        rays += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{s*0.32:.1f}" stroke-linecap="round"/>'
    return f'{rays}<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{s:.1f}" fill="{col}"/>'

def _cloud(cx, cy, s, fill="#cfd8e0", stroke="#9aa7b4"):
    # nuvola = 3 cerchi + base
    w = s * 2.6
    return (
        f'<g>'
        f'<ellipse cx="{cx:.1f}" cy="{cy+s*0.35:.1f}" rx="{w*0.62:.1f}" ry="{s*0.78:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
        f'<circle cx="{cx-s*0.7:.1f}" cy="{cy:.1f}" r="{s*0.72:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
        f'<circle cx="{cx+s*0.55:.1f}" cy="{cy-s*0.15:.1f}" r="{s*0.62:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
        f'<circle cx="{cx:.1f}" cy="{cy-s*0.45:.1f}" r="{s*0.72:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
        f'</g>'
    )

def _drops(cx, cy, s, col="#3a78c2"):
    d = ""
    for dx in (-s*0.7, 0, s*0.7):
        x = cx + dx; y = cy + s*1.05
        d += f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x-s*0.18:.1f}" y2="{y+s*0.7:.1f}" stroke="{col}" stroke-width="{s*0.34:.1f}" stroke-linecap="round"/>'
    return d

def icona_svg(key, cx, cy, s):
    if key == "sole":
        return f'<g>{_sun(cx, cy, s)}</g>'
    if key == "sole-nuvola":
        return f'<g>{_sun(cx-s*0.7, cy-s*0.6, s*0.7)}{_cloud(cx+s*0.25, cy+s*0.15, s*0.95)}</g>'
    if key == "nuvola":
        return f'<g>{_cloud(cx, cy, s)}</g>'
    if key == "pioggia":
        return f'<g>{_cloud(cx, cy-s*0.2, s*0.95)}{_drops(cx, cy+s*0.3, s*0.8)}</g>'
    if key == "temporale":
        bolt = (f'<polygon points="{cx-s*0.1:.1f},{cy+s*0.9:.1f} {cx+s*0.5:.1f},{cy+s*0.9:.1f} '
                f'{cx+s*0.05:.1f},{cy+s*1.9:.1f} {cx+s*0.3:.1f},{cy+s*1.1:.1f} {cx-s*0.2:.1f},{cy+s*1.1:.1f}" '
                f'fill="#f6a800"/>')
        return f'<g>{_cloud(cx, cy-s*0.2, s*0.95)}{bolt}</g>'
    if key == "nebbia":
        lines = ""
        for i, dy in enumerate((-s*0.2, s*0.25, s*0.7)):
            lines += f'<line x1="{cx-s*1.2:.1f}" y1="{cy+dy:.1f}" x2="{cx+s*1.2:.1f}" y2="{cy+dy:.1f}" stroke="#9aa7b4" stroke-width="{s*0.3:.1f}" stroke-linecap="round"/>'
        return f'<g>{lines}</g>'
    return f'<g>{_cloud(cx, cy, s)}</g>'

# ---------------------------------------------------------------- colore temperatura
# Scala meteo continua, ampia (da sotto zero a oltre 40 °C): viola/blu = freddo,
# verde/giallo = mite, arancio/rosso = caldo. Copre tutte le stagioni.
TEMP_STOPS = [(-6,"#4d4f9e"),(-2,"#3b5fb5"),(2,"#3a8bc2"),(6,"#56b0c9"),(10,"#7fc9b8"),
              (14,"#a8db9c"),(18,"#d4e88a"),(22,"#f3ec79"),(26,"#fbd14e"),(30,"#f7a93b"),
              (34,"#ef7733"),(38,"#df4a35"),(42,"#b81f3a")]
TEMP_MIN, TEMP_MAX = TEMP_STOPS[0][0], TEMP_STOPS[-1][0]

def colore(t):
    t = max(TEMP_MIN, min(TEMP_MAX, t))
    for i in range(len(TEMP_STOPS)-1):
        t0,c0 = TEMP_STOPS[i]; t1,c1 = TEMP_STOPS[i+1]
        if t <= t1 or i == len(TEMP_STOPS)-2:
            f = max(0, min(1, (t-t0)/(t1-t0)))
            c0 = [int(c0[1:][j:j+2],16) for j in (0,2,4)]
            c1 = [int(c1[1:][j:j+2],16) for j in (0,2,4)]
            rgb = [round(c0[k]+(c1[k]-c0[k])*f) for k in range(3)]
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    return TEMP_STOPS[-1][1]

# ---------------------------------------------------------------- fetch Open-Meteo
def _get(url):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "pc-genzano-meteo/1.0"})
    # Retry sugli errori di rete transitori dei runner CI (DNS, timeout, 5xx):
    # 3 tentativi con attesa crescente. I 4xx non si ritentano (non transitori).
    for tentativo in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code < 500 or tentativo == 2:
                raise
        except (urllib.error.URLError, OSError):
            if tentativo == 2:
                raise
        attesa = 15 * (tentativo + 1)
        print(f"[retry] errore di rete, riprovo tra {attesa}s: {url[:90]}", file=sys.stderr)
        time.sleep(attesa)

def fetch_map():
    lats = ",".join(f"{c[1]}" for c in CAPOLUOGHI)
    lons = ",".join(f"{c[2]}" for c in CAPOLUOGHI)
    url = ("https://api.open-meteo.com/v1/forecast?latitude=" + lats + "&longitude=" + lons +
           "&daily=temperature_2m_max,temperature_2m_min,weather_code&timezone=Europe%2FRome&forecast_days=1")
    return _get(url)

def cardinale(deg):
    if deg is None:
        return ""
    dirs = ["N", "NE", "E", "SE", "S", "SO", "O", "NO"]
    return dirs[int((deg % 360) / 45 + 0.5) % 8]

def fetch_card():
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={GENZANO[0]}&longitude={GENZANO[1]}"
           "&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,wind_gusts_10m,"
           "weather_code,pressure_msl,cloud_cover,precipitation,wind_direction_10m"
           "&daily=temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max,"
           "precipitation_sum,wind_gusts_10m_max,uv_index_max,sunrise,sunset"
           "&timezone=Europe%2FRome&forecast_days=4")
    return _get(url)

# ---------------------------------------------------------------- cornice microtesto
def microtext_frame(W, H, band, year):
    """Cornice di microtesto lungo i 4 bordi: incide la provenienza (nome + sito)
    in caratteri minuscoli, leggibili solo allo zoom. Funzione anti-appropriazione:
    chi ripubblica la cartina si porta dietro l'attribuzione; ritagliare la cornice
    è evidente e distruttivo. Decorativa per gli screen reader (aria-hidden): la
    descrizione testuale della mappa è già nell'aria-label dell'<svg>."""
    base = ("PROTEZIONE CIVILE GENZANO DI ROMA · www.protezionecivilegenzano.it · "
            "elaborazione grafica del Gruppo Comunale Volontari di Protezione Civile · "
            "© %d · " % year)
    fs = 4.6
    col, op = "#003366", "0.55"
    cw = fs * 0.52  # larghezza media carattere stimata
    def rep(length):
        n = max(2, int(length / (len(base) * cw)) + 1)
        return base * n
    Wt, Ht = W - 2 * band, H - 2 * band
    top   = (f'<text x="{band:.1f}" y="{band*0.72:.1f}" textLength="{Wt:.1f}" lengthAdjust="spacing" '
             f'font-size="{fs}" fill="{col}" fill-opacity="{op}">{rep(Wt)}</text>')
    bot   = (f'<text x="{band:.1f}" y="{H-band*0.42:.1f}" textLength="{Wt:.1f}" lengthAdjust="spacing" '
             f'font-size="{fs}" fill="{col}" fill-opacity="{op}">{rep(Wt)}</text>')
    left  = (f'<text transform="translate({band*0.72:.1f},{H-band:.1f}) rotate(-90)" textLength="{Ht:.1f}" '
             f'lengthAdjust="spacing" font-size="{fs}" fill="{col}" fill-opacity="{op}">{rep(Ht)}</text>')
    right = (f'<text transform="translate({W-band*0.42:.1f},{band:.1f}) rotate(90)" textLength="{Ht:.1f}" '
             f'lengthAdjust="spacing" font-size="{fs}" fill="{col}" fill-opacity="{op}">{rep(Ht)}</text>')
    return (f'<g aria-hidden="true" font-family="Trebuchet MS,Verdana,Arial,sans-serif" '
            f'letter-spacing="0.2">{top}{bot}{left}{right}</g>')

# ---------------------------------------------------------------- proiezione mappa
def build_svg(map_data, card_data, oggi):
    geo = json.load(open(GEO))
    LON0,LAT0,LON1,LAT1 = 11.25,40.55,14.15,42.98
    Wmap = 580; latmid = (LAT0+LAT1)/2
    sx = Wmap/((LON1-LON0)*math.cos(math.radians(latmid))); sy = sx
    Hmap = (LAT1-LAT0)*sy
    def px(lon, lat):
        return (lon-LON0)*math.cos(math.radians(latmid))*sx, (LAT1-lat)*sy
    def ring_path(ring):
        d = ""
        for i,(lon,lat) in enumerate(ring):
            x,y = px(lon,lat); d += ("M" if i==0 else "L") + f"{x:.0f},{y:.0f}"
        return d + "Z"

    # contesto regioni confinanti, faint
    contesto = "".join(
        f'<path d="{ring_path(r)}" fill="#f0f2f4" stroke="#e2e7eb" stroke-width="0.7"/>'
        for r in geo["contesto"]
    )

    # dati per provincia (capoluogo): max, min, weather_code
    perprov = {}
    for i, c in enumerate(CAPOLUOGHI):
        d = map_data[i]["daily"]
        tmin = d.get("temperature_2m_min", [None])[0]
        perprov[c[0]] = (d["temperature_2m_max"][0], tmin, d["weather_code"][0])
    # posizione manuale dell'etichetta-pillola (lon,lat)
    LBL = {"Viterbo":(12.10,42.42),"Rieti":(12.86,42.40),"Roma":(12.50,41.99),
           "Latina":(13.00,41.42),"Frosinone":(13.45,41.66)}

    prov_svg = ""; labels = ""
    for pr in geo["province"]:
        nome = pr["nome"]; t, tmin, wc = perprov[nome]
        col = colore(t)
        for ring in pr["rings"]:
            prov_svg += f'<path d="{ring_path(ring)}" fill="{col}" fill-opacity="0.85" stroke="#ffffff" stroke-width="1.6"/>'
        lx, ly = px(LBL[nome][0], LBL[nome][1])
        desc, ico = wmo(wc)
        # pillola bianca: nome (sopra) + icona (sx) + max/min (dx). Larghezza invariata
        # (province vicine: evitare sovrapposizioni), solo un filo più alta per la minima.
        min_sp = f'<tspan font-size="12" font-weight="500" fill="#6c757d">/{round(tmin)}&#176;</tspan>' if tmin is not None else ''
        pw, ph = 104, 50
        labels += (f'<g>'
                   f'<rect x="{lx-pw/2:.1f}" y="{ly-ph/2:.1f}" width="{pw}" height="{ph}" rx="9" '
                   f'fill="#ffffff" fill-opacity="0.93" stroke="{col}" stroke-width="1.6"/>'
                   f'<text x="{lx:.1f}" y="{ly-11:.1f}" font-size="12.5" font-weight="700" text-anchor="middle" fill="#003366">{nome}</text>'
                   f'{icona_svg(ico, lx-30, ly+10, 8)}'
                   f'<text x="{lx+14:.1f}" y="{ly+16:.1f}" font-size="18" font-weight="800" text-anchor="middle" fill="#1a1a1a">{round(t)}&#176;{min_sp}</text>'
                   f'</g>')

    # punto Genzano + riquadro di dettaglio collegato.
    # Il riquadro rispecchia i dati CORRENTI ("adesso") del riquadro grande della
    # pagina (.meteo-gz): stessa temperatura, condizione e percepita, piu' max/min,
    # umidita' e vento. Cosi' i due riquadri non si contraddicono (prima la cartina
    # mostrava il codice meteo "del giorno", il riquadro grande quello "di adesso").
    gx, gy = px(GENZANO[1], GENZANO[0])
    gz_d = card_data["daily"]
    cur = card_data["current"]
    gz_max = round(gz_d["temperature_2m_max"][0]); gz_min = round(gz_d["temperature_2m_min"][0])
    gz_now = round(cur["temperature_2m"], 1)
    gz_perc = round(cur["apparent_temperature"], 1)
    gz_hum = round(cur["relative_humidity_2m"])
    gz_wind = round(cur["wind_speed_10m"])
    gz_gust = round(cur.get("wind_gusts_10m") or 0)
    gz_desc, gz_ico = wmo(cur["weather_code"])
    gz_uv = round(gz_d["uv_index_max"][0] or 0)
    gz_uv_l = uv_label(gz_d["uv_index_max"][0])
    gz_alba = (gz_d["sunrise"][0] or "")[11:16]
    gz_tram = (gz_d["sunset"][0] or "")[11:16]
    gz_press = round(cur.get("pressure_msl") or 0)
    gz_cloud = round(cur.get("cloud_cover") or 0)
    gz_rain = round(cur.get("precipitation") or 0, 1)
    gz_dir = cardinale(cur.get("wind_direction_10m"))
    gz_ora = oggi.strftime("%H:%M")
    # prossimi 3 giorni (mini-strip)
    days_svg = ""
    # marcatore sul punto
    marker = (f'<circle cx="{gx:.1f}" cy="{gy:.1f}" r="5.5" fill="#b8860b" stroke="#ffffff" stroke-width="2"/>')
    # riquadro completo nell'angolo basso-sinistra (mare, area libera), con linea al punto
    bx, by, bw, bh = 8, Hmap-256, 272, 238
    for j, i in enumerate((1, 2, 3)):
        try:
            wcd = gz_d["weather_code"][i]
            mx = round(gz_d["temperature_2m_max"][i]); mn = round(gz_d["temperature_2m_min"][i])
            dd = oggi + datetime.timedelta(days=i)
            _, ic = wmo(wcd)
            cxd = bx + bw * (0.2 + 0.3 * j)
            days_svg += (f'<text x="{cxd:.1f}" y="{by+196:.1f}" font-size="10.5" font-weight="700" text-anchor="middle" fill="#cfe0f0">{GIORNI_BREVI[dd.weekday()]}</text>'
                         f'{icona_svg(ic, cxd, by+212, 6.5)}'
                         f'<text x="{cxd:.1f}" y="{by+232:.1f}" font-size="10.5" text-anchor="middle" fill="#ffffff">{mx}&#176;<tspan fill="#9ec5e8">/{mn}&#176;</tspan></text>')
        except Exception:
            pass
    cardg = (
        f'<line x1="{bx+bw:.1f}" y1="{by+22:.1f}" x2="{gx:.1f}" y2="{gy:.1f}" stroke="#b8860b" stroke-width="1.4" stroke-dasharray="4 3"/>'
        f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="12" fill="#003366" stroke="#b8860b" stroke-width="2"/>'
        f'<text x="{bx+14}" y="{by+25:.1f}" font-size="13.5" font-weight="800" fill="#ffffff">&#9733; Genzano di Roma <tspan font-size="11" font-weight="400" fill="#cfe0f0">&#183; ore {gz_ora}</tspan></text>'
        f'{icona_svg(gz_ico, bx+36, by+62, 14)}'
        f'<text x="{bx+70}" y="{by+68:.1f}" font-size="26" font-weight="800" fill="#ffffff">{gz_now}&#176;</text>'
        f'<text x="{bx+14}" y="{by+90:.1f}" font-size="11.5" fill="#cfe0f0">{gz_desc} &#183; percepita {gz_perc}&#176;</text>'
        f'<text x="{bx+14}" y="{by+107:.1f}" font-size="11" fill="#9ec5e8">Massima {gz_max}&#176; &#183; minima {gz_min}&#176;</text>'
        f'<text x="{bx+14}" y="{by+124:.1f}" font-size="10" fill="#e7eef6">Umidit&#224; {gz_hum}% &#183; Vento {gz_wind} km/h da {gz_dir} (raff. {gz_gust})</text>'
        f'<text x="{bx+14}" y="{by+140:.1f}" font-size="10" fill="#e7eef6">Pressione {gz_press} hPa &#183; Nuvolosit&#224; {gz_cloud}% &#183; Pioggia {gz_rain} mm</text>'
        f'<text x="{bx+14}" y="{by+156:.1f}" font-size="10" fill="#e7eef6">UV {gz_uv} ({gz_uv_l}) &#183; Alba {gz_alba} &#183; Tramonto {gz_tram}</text>'
        f'<line x1="{bx+12}" y1="{by+166:.1f}" x2="{bx+bw-12}" y2="{by+166:.1f}" stroke="#1f4a78" stroke-width="1"/>'
        f'<text x="{bx+14}" y="{by+182:.1f}" font-size="9.5" fill="#9ec5e8">Prossimi giorni</text>'
        f'{days_svg}'
    )

    PAD=18; HEAD=64; FOOT=82
    W = Wmap+2*PAD; H = Hmap+HEAD+FOOT+PAD

    # legenda: barra campionata 1°C alla volta (rende identica in ogni renderer)
    barW = min(440, W-2*PAD-30); barX = (W-barW)/2; barY = H-64; barH = 13
    nseg = int(TEMP_MAX-TEMP_MIN)
    segw = barW/nseg
    segs = ""
    for k in range(nseg):
        tv = TEMP_MIN + k
        segs += f'<rect x="{barX+k*segw:.2f}" y="{barY:.1f}" width="{segw+0.6:.2f}" height="{barH}" fill="{colore(tv+0.5)}"/>'
    ticks = ""
    for tv in (-5,0,5,10,15,20,25,30,35,40):
        tx = barX + (tv-TEMP_MIN)/(TEMP_MAX-TEMP_MIN)*barW
        ticks += (f'<line x1="{tx:.1f}" y1="{barY:.1f}" x2="{tx:.1f}" y2="{barY+barH+3:.1f}" stroke="#495057" stroke-width="0.9"/>'
                  f'<text x="{tx:.1f}" y="{barY+barH+15:.1f}" font-size="9.5" text-anchor="middle" fill="#495057">{tv}&#176;</text>')
    leg = (f'<text x="{barX:.1f}" y="{barY-5:.1f}" font-size="10" fill="#495057">Temperatura massima (&#176;C)</text>'
           f'{segs}'
           f'<rect x="{barX:.1f}" y="{barY:.1f}" width="{barW:.1f}" height="{barH}" rx="3" fill="none" stroke="#adb5bd" stroke-width="0.8"/>'
           f'{ticks}')

    data_lunga = f"{GIORNI_IT[oggi.weekday()]} {oggi.day} {MESI_IT[oggi.month]} {oggi.year}"
    ora = oggi.strftime("%H:%M")
    # contenuto della cartina (coordinate invariate); verrà traslato dentro la cornice
    inner = (
        f'<defs><clipPath id="mapclip"><rect x="0" y="0" width="{Wmap:.0f}" height="{Hmap:.0f}"/></clipPath></defs>'
        f'<rect x="0" y="0" width="{W:.0f}" height="{H:.0f}" fill="#ffffff"/>'
        f'<g transform="translate({PAD},{HEAD})" clip-path="url(#mapclip)">{contesto}{prov_svg}{marker}{labels}{cardg}</g>'
        f'<rect x="0" y="0" width="{W:.0f}" height="{HEAD-2}" fill="#ffffff"/>'
        f'<text x="{W/2:.0f}" y="27" font-size="20" font-weight="700" text-anchor="middle" fill="#003366">Lazio &#8212; oggi: temperatura e cielo</text>'
        f'<text x="{W/2:.0f}" y="47" font-size="12" text-anchor="middle" fill="#495057">{data_lunga}, ore {ora} &#183; temperatura in &#176;C per provincia &#183; dettaglio Genzano di Roma</text>'
        f'<rect x="0" y="{HEAD+Hmap:.0f}" width="{W:.0f}" height="{FOOT+PAD}" fill="#ffffff"/>'
        f'<g>{leg}</g>'
        f'<text x="{W/2:.0f}" y="{H-22:.0f}" font-size="10.5" font-weight="700" text-anchor="middle" fill="#003366">Elaborazione grafica del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma</text>'
        f'<text x="{W/2:.0f}" y="{H-8:.0f}" font-size="8.5" text-anchor="middle" fill="#6c757d">Dati: Open-Meteo (modelli ECMWF) &#183; dato indicativo, per le allerte vale il Centro Funzionale Regionale del Lazio</text>'
    )
    # cornice di microtesto attorno a tutto (banda dedicata, non sovrapposta al contenuto)
    F = 13
    W2, H2 = W + 2 * F, H + 2 * F
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W2:.0f} {H2:.0f}" '
        f'font-family="Trebuchet MS,Verdana,Arial,sans-serif" role="img" '
        f'aria-label="Mappa del Lazio con temperatura massima e cielo previsti oggi per ogni provincia, e un riquadro di dettaglio per Genzano di Roma: alle {gz_ora}, {gz_now} gradi, {gz_desc}, percepita {gz_perc} gradi, massima {gz_max} gradi, minima {gz_min} gradi.">'
        f'<rect x="0" y="0" width="{W2:.0f}" height="{H2:.0f}" fill="#ffffff"/>'
        f'<g transform="translate({F},{F})">{inner}</g>'
        f'{microtext_frame(W2, H2, F, oggi.year)}'
        f'</svg>'
    )
    return svg

# ---------------------------------------------------------------- card Genzano
# Indice UV: bande standard WHO (Global Solar UV Index) -> etichetta italiana.
def uv_label(v):
    v = round(v or 0)
    if v <= 2:  return "basso"
    if v <= 5:  return "moderato"
    if v <= 7:  return "alto"
    if v <= 10: return "molto alto"
    return "estremo"

def _hhmm(iso):
    # "2026-05-23T05:39" -> "05:39"
    return iso.split("T")[1][:5] if iso and "T" in iso else (iso or "")

def build_card(card_data, now):
    cur = card_data["current"]
    d = card_data["daily"]
    desc_cur, ico_cur = wmo(cur["weather_code"])
    giorni = []
    for i in range(len(d["time"])):
        dt = datetime.date.fromisoformat(d["time"][i])
        desc, ico = wmo(d["weather_code"][i])
        label = "Oggi" if i == 0 else f"{GIORNI_BREVI[dt.weekday()]} {dt.day}"
        giorni.append({
            "label": label,
            "icona": icona_svg(ico, 16, 16, 9),
            "cielo": desc,
            "tmax": round(d["temperature_2m_max"][i]),
            "tmin": round(d["temperature_2m_min"][i]),
            "pioggia": d["precipitation_probability_max"][i],
            "pioggia_mm": round(d["precipitation_sum"][i] or 0, 1),
            "raffiche": round(d["wind_gusts_10m_max"][i] or 0),
            "uv": round(d["uv_index_max"][i] or 0),
            "uv_label": uv_label(d["uv_index_max"][i]),
        })
    data_lunga = f"{GIORNI_IT[now.weekday()]} {now.day} {MESI_IT[now.month]} {now.year}"
    return {
        "aggiornato": now.strftime("%Y-%m-%dT%H:%M"),
        "data_lunga": data_lunga,
        "aggiornato_label": f"{data_lunga}, ore {now.strftime('%H:%M')}",
        "alba": _hhmm(d["sunrise"][0]),
        "tramonto": _hhmm(d["sunset"][0]),
        "corrente": {
            "temp": round(cur["temperature_2m"], 1),
            "percepita": round(cur["apparent_temperature"], 1),
            "cielo": desc_cur,
            "icona": icona_svg(ico_cur, 28, 28, 16),
            "umidita": round(cur["relative_humidity_2m"]),
            "vento": round(cur["wind_speed_10m"]),
            "raffiche": round(cur["wind_gusts_10m"] or 0),
        },
        "giorni": giorni,
        "fonte": "Open-Meteo (modelli ECMWF)",
    }

def main():
    now = datetime.datetime.now(TZ_ROMA)  # ora italiana anche sul runner UTC
    if len(sys.argv) >= 4 and sys.argv[1] == "--from-file":
        map_data = json.load(open(sys.argv[2]))
        card_data = json.load(open(sys.argv[3]))
    else:
        map_data = fetch_map()
        card_data = fetch_card()

    svg = build_svg(map_data, card_data, now)
    os.makedirs(os.path.dirname(OUT_SVG), exist_ok=True)
    open(OUT_SVG, "w", encoding="utf-8").write(svg)

    card = build_card(card_data, now)
    json.dump(card, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(f"OK  {OUT_SVG} ({len(svg)} byte)")
    print(f"OK  {OUT_JSON}")

if __name__ == "__main__":
    main()
