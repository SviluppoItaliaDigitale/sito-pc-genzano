"""Costanti, domini, modelli, prodotti e tavolozze delle mappe professionali."""

from __future__ import annotations

from typing import Any

# User-Agent onesto: il sito lo usa già in altri prelievi di dati aperti.
USER_AGENT = (
    "PCGenzanoMeteo/1.0 (+https://www.protezionecivilegenzano.it/; "
    "mappe di previsione a partire da dati aperti)"
)

RAMO_DATI = "mappe-meteo-dati"
MANIFESTO_NOME = "manifesto.json"
# Indirizzo da cui la pagina legge le mappe (CSP: raw.githubusercontent.com è già consentito).
BASE_DATI_RAW = (
    "https://raw.githubusercontent.com/SviluppoItaliaDigitale/"
    "sito-pc-genzano/" + RAMO_DATI
)

# Livelli isobarici (hPa) usati per derivare PV, IVT e superfici isentropiche.
# Sono quelli disponibili sia in ECMWF Open Data sia in ICON-EU e GFS.
LIVELLI_HPA = (1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100)

# Ore di previsione predefinite: ogni 6 ore fino a +72, poi ogni 12 fino a +120 (17 fotogrammi).
ORE_STANDARD = tuple(range(0, 73, 6)) + (84, 96, 108, 120)
# Anteprima locale più corta, per avere GIF reali in tempi ragionevoli.
ORE_ANTEPRIMA = (0, 12, 24, 36, 48, 60, 72)

GIORNI_IT = (
    "lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica",
)
MESI_IT = (
    "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
    "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre",
)

# Colori istituzionali del sito
# (themes/flavour-pcgenzano/static/css/custom.css: --pc-primary e correlati).
BLU = "#003366"
BLU_SCURO = "#00244d"
BLU_MEDIO = "#004080"
BLU_CHIARO = "#0066cc"
ARANCIO = "#FF6600"
FONDO_FIGURA = "#ffffff"
FONDO_CARTA = "#fafbfc"
TESTO = "#1a1a1a"
TESTO_SECONDARIO = "#42515c"
FONDO_TITOLO = FONDO_FIGURA  # testata, piede e figura: tema chiaro del sito
FONDO_MARE = "#c3d3df"
FONDO_TERRA = "#efe6d6"
COSTA = "#1c2833"
CONFINE = "#003366"
CONFINE_IT = "#003366"

# Proiezioni e riquadri. Il riquadro di scarico è l'unione, così un solo
# prelievo alimenta entrambi i domini.
DOMINI: dict[str, dict[str, Any]] = {
    "italia": {
        "nome": "Italia e Mediterraneo centrale",
        "extent": (4.0, 21.2, 34.8, 48.1),  # lon0, lon1, lat0, lat1
        "proj": {
            "name": "lcc",
            "central_longitude": 12.5,
            "central_latitude": 42.0,
            "standard_parallels": (36.0, 46.0),
        },
        "bbox": (2.1, 23.1, 34.8, 48.4),
        "figsize": (13.4, 10.4),
        "max_punti": 420,
    },
    "europa": {
        "nome": "Europa",
        "extent": (-8.0, 32.0, 35.0, 62.0),
        # riquadro geografico effettivamente visibile nella proiezione (calcolato)
        "bbox": (-21.2, 45.2, 33.1, 63.2),
        "proj": {
            "name": "lcc",
            "central_longitude": 12.0,
            "central_latitude": 48.0,
            "standard_parallels": (38.0, 58.0),
        },
        "figsize": (13.4, 10.6),
        "max_punti": 360,
    },
}

# Riquadro geografico unico per i prelievi GFS (filtro NOMADS).
SCARICO_EXTENT = (-24.0, 47.0, 31.0, 65.0)  # copre i riquadri visibili di entrambi i domini

CITTA_ITALIA = (
    ("Roma", 12.50, 41.90, True),
    ("Milano", 9.19, 45.46, True),
    ("Napoli", 14.27, 40.85, True),
    ("Torino", 7.69, 45.07, False),
    ("Palermo", 13.36, 38.12, True),
    ("Genova", 8.93, 44.41, False),
    ("Bologna", 11.34, 44.49, False),
    ("Firenze", 11.26, 43.77, False),
    ("Bari", 16.87, 41.12, False),
    ("Venezia", 12.33, 45.44, False),
    ("Cagliari", 9.13, 39.22, True),
    ("Catania", 15.09, 37.50, False),
    ("Trieste", 13.77, 45.65, False),
    ("Genzano", 12.69, 41.70, True),
)

CITTA_EUROPA = (
    ("Roma", 12.50, 41.90, True),
    ("Parigi", 2.35, 48.86, False),
    ("Berlino", 13.41, 52.52, False),
    ("Londra", -0.13, 51.51, False),
    ("Madrid", -3.70, 40.42, False),
    ("Atene", 23.73, 37.98, False),
    ("Vienna", 16.37, 48.21, False),
    ("Varsavia", 21.01, 52.23, False),
    ("Lisbona", -9.14, 38.72, False),
    ("Oslo", 10.75, 59.91, False),
    ("Istanbul", 28.98, 41.01, False),
    ("Algeri", 3.06, 36.75, False),
)

MODELLI: dict[str, dict[str, Any]] = {
    "gfs": {
        "nome": "GFS",
        "nome_lungo": "Global Forecast System",
        "ente": "NOAA/NCEP",
        "risoluzione": "0,25° (circa 25 km)",
        "licenza": "Dati pubblici del Governo degli Stati Uniti (dominio pubblico)",
        "attribuzione": "NOAA/NCEP GFS",
        "url_licenza": "https://www.weather.gov/disclaimer",
        "corse_utc": (0, 6, 12, 18),
        "domini": ("italia", "europa"),
        "ritardo_ore": 4.5,
        "passo_ore": 6,
        "orizzonte_ore": 120,
    },
    "ecmwf": {
        "nome": "ECMWF IFS",
        "nome_lungo": "Integrated Forecasting System",
        "ente": "ECMWF",
        "risoluzione": "0,25° (Open Data; disponibile anche 0,1°)",
        "licenza": "CC BY 4.0",
        "attribuzione": "ECMWF IFS Open Data (CC BY 4.0)",
        "url_licenza": "https://www.ecmwf.int/en/forecasts/datasets/open-data",
        "corse_utc": (0, 12),
        "domini": ("italia", "europa"),
        "ritardo_ore": 6.5,
        "passo_ore": 6,
        "orizzonte_ore": 120,
    },
    "ecmwf-aifs": {
        "nome": "ECMWF AIFS",
        "nome_lungo": "Artificial Intelligence Forecasting System",
        "ente": "ECMWF",
        "risoluzione": "0,25°",
        "licenza": "CC BY 4.0",
        "attribuzione": "ECMWF AIFS Open Data (CC BY 4.0)",
        "url_licenza": "https://www.ecmwf.int/en/forecasts/datasets/open-data",
        "corse_utc": (0, 12),
        "domini": ("italia",),
        "ritardo_ore": 5.0,
        "passo_ore": 6,
        "orizzonte_ore": 120,
    },
    "icon-eu": {
        "nome": "ICON-EU",
        "nome_lungo": "ICON sul dominio europeo",
        "ente": "Deutscher Wetterdienst (DWD)",
        "risoluzione": "0,0625° (circa 6,5 km)",
        "licenza": "Data licence Germany – attribution – Version 2.0 (dl-de/by-2-0)",
        "attribuzione": "DWD ICON-EU (dl-de/by-2-0)",
        "url_licenza": "https://www.govdata.de/dl-de/by-2-0",
        "corse_utc": (0, 12),
        "domini": ("italia",),
        "ritardo_ore": 4.0,
        "passo_ore": 6,
        "orizzonte_ore": 120,
    },
}

# Prodotti in stile Albany (Alicia Bentley). "richiede" elenca i campi
# normalizzati indispensabili; "richiede_3d" i campi con dimensione verticale.
PRODOTTI: dict[str, dict[str, Any]] = {
    "mslp_precip": {
        "titolo": "Pressione al suolo e pioggia in 6 ore",
        "sottotitolo": "Pressione al livello del mare (isobare) e precipitazione accumulata in 6 ore",
        "ordine": 10,
        "richiede": ("mslp", "tp_6h"),
    },
    "t850_vento10": {
        "titolo": "Temperatura a 850 hPa e vento a 10 metri",
        "sottotitolo": "Temperatura a circa 1.500 m e vento vicino al suolo (barbetti in nodi)",
        "ordine": 20,
        "richiede": ("t850", "u10", "v10"),
    },
    "h500": {
        "titolo": "Geopotenziale, temperatura, moto verticale e vorticità a 500 hPa",
        "sottotitolo": "Altezza di geopotenziale, temperatura, ascesa e vorticità relativa, con il vento in quota",
        "ordine": 30,
        "richiede": ("z500", "t500", "u500", "v500"),
        "opzionali": ("w500", "vo500"),
    },
    "ivt_h700": {
        "titolo": "Trasporto integrato di vapore (IVT) e geopotenziale a 700 hPa",
        "sottotitolo": "Flusso di umidità nella colonna e altezza di geopotenziale a circa 3.000 m",
        "ordine": 40,
        "richiede": ("ivt", "z700"),
    },
    "h850_cape_shear": {
        "titolo": "Geopotenziale e temperatura a 850 hPa, CAPE e shear 1000-500 hPa",
        "sottotitolo": "Instabilità convettiva (CAPE), vento a 850 hPa e shear nello strato 1000-500 hPa",
        "ordine": 50,
        "richiede": ("z850", "t850", "cape", "u1000", "v1000", "u500", "v500"),
    },
    "spessore_mslp_jet": {
        "titolo": "Pressione al suolo, spessore 1000-500 hPa e corrente a getto a 250 hPa",
        "sottotitolo": "Spessore dello strato 1000-500 hPa, isobare al suolo e intensità del getto",
        "ordine": 60,
        "richiede": ("mslp", "z1000", "z500", "mod250"),
    },
    "h700_pw": {
        "titolo": "Geopotenziale, temperatura e vento a 700 hPa e acqua precipitabile",
        "sottotitolo": "Acqua precipitabile nella colonna, con il flusso a circa 3.000 m",
        "ordine": 70,
        "richiede": ("z700", "t700", "u700", "v700", "pwat"),
    },
    "thetae850": {
        "titolo": "Temperatura potenziale equivalente a 850 hPa",
        "sottotitolo": "Theta-e a 850 hPa (massa d'aria e potenziale instabilità)",
        "ordine": 80,
        "richiede": ("thetae850", "u850", "v850"),
    },
    "pv_jet": {
        "titolo": "Vorticità potenziale 300-200 hPa e getto a 250 hPa",
        "sottotitolo": "PV nella media-alta troposfera e intensità del vento a 250 hPa",
        "ordine": 90,
        "richiede": ("pv_300_200", "mod250", "u250", "v250"),
    },
    "dt_2pvu": {
        "titolo": "Tropopausa dinamica (2 PVU): theta, vento e vorticità 925-850 hPa",
        "sottotitolo": "Temperatura potenziale sulla superficie a 2 PVU, vento e vorticità nei bassi strati",
        "ordine": 100,
        "richiede": ("theta_dt", "u_dt", "v_dt", "vo_925_850"),
    },
    "isent_330": {
        "titolo": "Superficie isentropica 330 K: PV, pressione e vento",
        "sottotitolo": "Vorticità potenziale, pressione e vento sulla superficie a 330 K",
        "ordine": 110,
        "richiede": ("pv_330", "p_330", "u_330", "v_330"),
    },
    "isent_310_350": {
        "titolo": "Superfici isentropiche 310 K e 350 K: PV e pressione",
        "sottotitolo": "PV a 310 K (ombreggiatura) e pressione a 350 K (isolinee), con il vento a 310 K",
        "ordine": 120,
        "richiede": ("pv_310", "p_350", "u_310", "v_310"),
    },
    "coupling_index": {
        "titolo": "Indice di accoppiamento (tropopausa e theta-e a 850 hPa)",
        "sottotitolo": "Differenza fra la temperatura potenziale sulla tropopausa dinamica e la theta-e a 850 hPa",
        "ordine": 130,
        "richiede": ("coupling", "mslp"),
    },
}

# Prodotti chiesti dallo stile Albany ma non realizzabili senza una climatologia
# (anomalie standardizzate) o senza dati grezzi aperti di un modello.
PRODOTTI_SALTATI = {
    "anomalie_standardizzate": (
        "Le anomalie standardizzate richiedono una climatologia di riferimento "
        "(per esempio 30 anni di rianalisi) che non è inclusa in questo "
        "prelievo di dati aperti. Senza quel dataset il campo non è calcolabile "
        "in modo rigoroso. Si potrà aggiungere in un secondo tempo se si decide "
        "di ospitare una climatologia nel ramo dei dati."
    ),
}


def data_italiana(dt) -> str:
    """Formatta una data/ora UTC in italiano, es. «martedì 10 novembre 2026 12:00 UTC»."""
    return (
        f"{GIORNI_IT[dt.weekday()]} {dt.day} {MESI_IT[dt.month - 1]} "
        f"{dt.year} {dt:%H:%M} UTC"
    )
