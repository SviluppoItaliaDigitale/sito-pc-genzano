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
giornaliero non scarica i grandi file nazionali.

Uso:
  python3 scripts/genera-meteo-lazio.py            # fetch live (runner CI / locale con rete)
  python3 scripts/genera-meteo-lazio.py --from-file map.json card.json   # test offline

Idempotente: sovrascrive sempre i due output con i dati del giorno.
"""
import json, math, sys, os, urllib.request, datetime, ssl

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
def colore(t):
    stops = [(12,"#2c7fb8"),(18,"#41b6c4"),(22,"#a1dab4"),(26,"#fec44f"),(30,"#fe9929"),(34,"#d7301f")]
    for i in range(len(stops)-1):
        t0,c0 = stops[i]; t1,c1 = stops[i+1]
        if t <= t1 or i == len(stops)-2:
            f = max(0, min(1, (t-t0)/(t1-t0)))
            c0 = [int(c0[1:][j:j+2],16) for j in (0,2,4)]
            c1 = [int(c1[1:][j:j+2],16) for j in (0,2,4)]
            rgb = [round(c0[k]+(c1[k]-c0[k])*f) for k in range(3)]
            return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    return "#d7301f"

# ---------------------------------------------------------------- fetch Open-Meteo
def _get(url):
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": "pc-genzano-meteo/1.0"})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as r:
        return json.loads(r.read().decode("utf-8"))

def fetch_map():
    lats = ",".join(f"{c[1]}" for c in CAPOLUOGHI)
    lons = ",".join(f"{c[2]}" for c in CAPOLUOGHI)
    url = ("https://api.open-meteo.com/v1/forecast?latitude=" + lats + "&longitude=" + lons +
           "&daily=temperature_2m_max,weather_code&timezone=Europe%2FRome&forecast_days=1")
    return _get(url)

def fetch_card():
    url = (f"https://api.open-meteo.com/v1/forecast?latitude={GENZANO[0]}&longitude={GENZANO[1]}"
           "&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code"
           "&daily=temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max"
           "&timezone=Europe%2FRome&forecast_days=4")
    return _get(url)

# ---------------------------------------------------------------- proiezione mappa
def build_svg(map_data, oggi):
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

    # dati per provincia (capoluogo): temp + weather_code
    perprov = {}
    units = map_data[0].get("daily_units", {})
    for i, c in enumerate(CAPOLUOGHI):
        d = map_data[i]["daily"]
        perprov[c[0]] = (d["temperature_2m_max"][0], d["weather_code"][0])
    # etichetta: posizione manuale per leggibilità
    LBL = {"Viterbo":(12.10,42.42),"Rieti":(12.86,42.40),"Roma":(12.55,41.95),
           "Latina":(12.95,41.45),"Frosinone":(13.45,41.66)}

    prov_svg = ""; labels = ""
    for pr in geo["province"]:
        nome = pr["nome"]; t, wc = perprov[nome]
        col = colore(t)
        for ring in pr["rings"]:
            prov_svg += f'<path d="{ring_path(ring)}" fill="{col}" fill-opacity="0.82" stroke="#ffffff" stroke-width="1.6"/>'
        lx, ly = px(LBL[nome][0], LBL[nome][1])
        desc, ico = wmo(wc)
        labels += f'<text x="{lx:.1f}" y="{ly-22:.1f}" font-size="13" font-weight="700" text-anchor="middle" fill="#003366">{nome}</text>'
        labels += f'<text x="{lx:.1f}" y="{ly+2:.1f}" font-size="23" font-weight="800" text-anchor="middle" fill="#1a1a1a">{round(t)}°</text>'
        labels += icona_svg(ico, lx, ly+26, 9)

    # stella Genzano
    gx, gy = px(GENZANO[1], GENZANO[0])
    star = (f'<path transform="translate({gx:.1f},{gy:.1f})" d="M0,-8 L2.4,-2.5 8,-2.5 3.4,1.3 5,7 0,3.4 -5,7 -3.4,1.3 -8,-2.5 -2.4,-2.5 Z" '
            f'fill="#b8860b" stroke="#7a5c08" stroke-width="0.6"/>'
            f'<text x="{gx+42:.1f}" y="{gy+3.5:.1f}" font-size="11.5" font-weight="700" text-anchor="middle" fill="#003366">Genzano</text>')

    PAD=18; HEAD=64; FOOT=46
    W = Wmap+2*PAD; H = Hmap+HEAD+FOOT+PAD
    # legenda
    legitems = [("16°","#41b6c4"),("20°","#a1dab4"),("24°","#cfe08a"),("28°","#fec44f"),("32°","#fe9929"),("34°+","#d7301f")]
    leg=""; lx0=PAD; ly=H-26
    for i,(lab,c) in enumerate(legitems):
        lx = lx0+i*72
        leg += f'<rect x="{lx}" y="{ly-9}" width="16" height="16" rx="3" fill="{c}" stroke="#adb5bd" stroke-width="0.6"/>'
        leg += f'<text x="{lx+22}" y="{ly+3}" font-size="11" fill="#495057">{lab}</text>'

    data_lunga = f"{GIORNI_IT[oggi.weekday()]} {oggi.day} {MESI_IT[oggi.month]} {oggi.year}"
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
        f'font-family="Trebuchet MS,Verdana,Arial,sans-serif" role="img" '
        f'aria-label="Mappa del Lazio con temperatura massima e cielo previsti oggi per ogni provincia. Genzano di Roma evidenziata con una stella.">'
        f'<rect x="0" y="0" width="{W:.0f}" height="{H:.0f}" fill="#ffffff"/>'
        f'<defs><clipPath id="mapclip"><rect x="0" y="0" width="{Wmap:.0f}" height="{Hmap:.0f}"/></clipPath></defs>'
        f'<g transform="translate({PAD},{HEAD})" clip-path="url(#mapclip)">{contesto}{prov_svg}{labels}{star}</g>'
        f'<rect x="0" y="0" width="{W:.0f}" height="{HEAD-2}" fill="#ffffff"/>'
        f'<text x="{W/2:.0f}" y="27" font-size="20" font-weight="700" text-anchor="middle" fill="#003366">Lazio &#8212; oggi: temperatura e cielo</text>'
        f'<text x="{W/2:.0f}" y="47" font-size="12" text-anchor="middle" fill="#495057">{data_lunga} &#183; massime in &#176;C per provincia &#183; &#9733; Genzano di Roma</text>'
        f'<rect x="0" y="{HEAD+Hmap:.0f}" width="{W:.0f}" height="{FOOT+PAD}" fill="#ffffff"/>'
        f'<g>{leg}</g>'
        f'<text x="{W-PAD}" y="{H-10:.0f}" font-size="9" text-anchor="end" fill="#6c757d">Dati: Open-Meteo (modelli ECMWF) &#183; elaborazione Protezione Civile Genzano &#183; dato indicativo, per le allerte vale il Centro Funzionale Lazio</text>'
        f'</svg>'
    )
    return svg

# ---------------------------------------------------------------- card Genzano
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
        })
    data_lunga = f"{GIORNI_IT[now.weekday()]} {now.day} {MESI_IT[now.month]} {now.year}"
    return {
        "aggiornato": now.strftime("%Y-%m-%dT%H:%M"),
        "data_lunga": data_lunga,
        "corrente": {
            "temp": round(cur["temperature_2m"], 1),
            "percepita": round(cur["apparent_temperature"], 1),
            "cielo": desc_cur,
            "icona": icona_svg(ico_cur, 28, 28, 16),
            "umidita": round(cur["relative_humidity_2m"]),
            "vento": round(cur["wind_speed_10m"]),
        },
        "giorni": giorni,
        "fonte": "Open-Meteo (modelli ECMWF)",
    }

def main():
    now = datetime.datetime.now()
    if len(sys.argv) >= 4 and sys.argv[1] == "--from-file":
        map_data = json.load(open(sys.argv[2]))
        card_data = json.load(open(sys.argv[3]))
    else:
        map_data = fetch_map()
        card_data = fetch_card()

    svg = build_svg(map_data, now.date())
    os.makedirs(os.path.dirname(OUT_SVG), exist_ok=True)
    open(OUT_SVG, "w", encoding="utf-8").write(svg)

    card = build_card(card_data, now)
    json.dump(card, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print(f"OK  {OUT_SVG} ({len(svg)} byte)")
    print(f"OK  {OUT_JSON}")

if __name__ == "__main__":
    main()
