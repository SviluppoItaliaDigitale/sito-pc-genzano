#!/usr/bin/env python3
"""
genera-video-correlati.py — Cross-match algoritmico fra il catalogo completo
dei video DPC/AaP (data/video_dpc_catalogo.yaml) e tutti i contenuti del
sito. Salva il risultato in data/video_correlati.yaml.

Per ogni pagina/articolo:
  - calcola le keyword significative (frontmatter + corpo)
  - cerca i video del catalogo che condividono >= N keyword pesate (IDF)
  - mantiene i top K video (default: 4) ordinati per score

Esclude i video che sono già presenti in data/lis.yaml (sono mostrati
tramite il badge LIS contestuale: evitiamo duplicazione visiva).

Il file generato è letto dal partial Hugo `video-correlati.html` che
renderizza in fondo agli articoli una sezione "Approfondimenti video"
con link esterni privacy-first (niente embed).

Uso: python3 scripts/genera-video-correlati.py [--max-per-page N] [--min-score F]
"""

import re
import sys
import yaml
import argparse
from pathlib import Path
from collections import defaultdict

STOPWORDS_IT = set("""
a ad ai al alla alle allo anche b c che chi ci con d da dai dal dalla dalle dei del
della delle dello di dove e ed essere fa fra gli ha hai hanno ho i il in la le lo
ma mi nei nel nella nelle nello noi non o per più poi qua qual quale quali
quando quanta quante quanti quanto quel quella quelle quelli quello questa queste
questi questo se senza si siamo sia sono su sua sue sugli sui sul sull sulla sulle
sullo suo suoi sta stati stato te ti tra tu tua tue tuoi tutta tutte tutti tutto
un una uno vi via voi cui ma anche già più ancora come così solo ogni quando
2018 2019 2020 2021 2022 2023 2024 2025 2026 2027 ed del giornata convegno
edizione progetto presentazione conferenza diretta speciale incontra incontro racconta
salone internazionale libro torino punto attività attivita prima dopo durante intervento
incontri ascolta tappa stati generali confronto temi tema tavolo nazionale nazionali
italia italiana italiano dipartimento protezione civile pc dpc ente glossario
serie episodi video cosa fare sapere come dove quando perché perche
spiega capire significato termine termini parola parole pagina pagine sito
nuovo nuova nuovi nuove sicurezza articolo articoli volontari volontariato
gennaio febbraio marzo aprile maggio giugno luglio agosto settembre ottobre novembre
dicembre notte giorno giorni mese mesi anno anni mattina pomeriggio sera notte
ieri oggi domani lunedì martedì mercoledì giovedì venerdì sabato domenica
attivazione gestione presentazione interno esterno
home work much find very this that these those here there with into very like
what when where which whose whom whose were have having does have did doing done
just from over more most less least some many other another only also still both
each every same well way ways things kind kinds type types whose really
about across after again against among around because before behind below beside
between beyond during except inside outside through under above against
will would could should might must shall used find finding work works
ourselves yourself himself herself itself themselves ones really since
parole astratte/comuni/geografiche non-topiche: non devono MAI ancorare
da sole un video correlato. Aggiunte 20/05/2026 dopo l'audit dei falsi
positivi (es. "sciami d'api"->"sciami sismici", "Haiti 2010"->"curiosità
sul Lazio", "piano emergenza condominio"->"reattori nucleari"): l'IDF è
calcolato solo sul corpus del sito, quindi parole generiche ma rare
negli articoli PC prendevano peso pieno e diventavano ancore forti.
bisogno nostra nostro nostre nostri vostra vostro vostre vostri
proprio propria propri proprie stesso stessa stessi stesse paura
volta volte modo modi grande grandi piccolo piccola piccoli piccole
bene meglio peggio forse magari davvero soprattutto oppure invece
mentre quindi parte parti caso casi vero vera veri vere poco poca
pochi poche tanto tanta tanti tante molto molta molti molte ecco
contro storia storie settimana versione mondo morti morto feriti
ferito citta città persone persona paese paesi milioni miliardi
numero numeri record curiosita curiosità europa europea europeo
europei europee qualcuno qualcosa niente nulla nessuno troppo
""".split())

# Pagine del sito da escludere dal cross-match (non avrebbe senso linkare
# video correlati a pagine legali, tecniche, di servizio).
SKIP_PAGE_PATTERNS = [
    r"^/?privacy/?$",
    r"^/?note-legali/?$",
    r"^/?accessibilita/?$",
    r"^/?social-media-policy/?$",
    r"^/?mappa-sito/?$",
    r"^/?attribuzioni-pittogrammi/?$",
    r"^/?cerca/?$",
    r"^/?stato-sistema/?$",
    r"^/?feed-rss/?$",
    r"^/?siti-utili/?$",
    r"^/?trasparenza/?$",
    r"^/?open-data/?$",
    r"^/?podcast/?",   # ha già contenuti audio
    r"^/?articoli-da-ascoltare/?$",
    r"^/?audio-e-podcast/?$",
    r"^/?lis/?$",       # è la pagina hub LIS, ha già tutto
    r"^/?assistente/?$",
    r"^/?cruscotto/?$",      # pagina-strumento a dati live: niente "Approfondimenti video"
    r"^/?english/", r"^/?francais/", r"^/?deutsch/", r"^/?espanol/",
    r"^/?portugues/", r"^/?romana/", r"^/?esperanto/",  # traduzioni
    r"^/?formazione/?$",  # hub formazione (ne ha già molti link nei kit)
    r"^/?storia/?$",      # hub timeline storia del territorio (narrativo,
                          # nessun video locale; agganciava Stromboli a sproposito)
    # Articoli senza video pertinenti nei canali monitorati: il cross-match
    # produce solo falsi positivi (parole generiche o omonimie). Escludi per
    # non mostrare "Approfondimenti video" fuori tema (rule: niente sezione
    # video se non ci sono video davvero pertinenti).
    #  - sciami d'api: "sciami" agganciava video INGV su SCIAMI SISMICI,
    #    "bisogno"/"nostra" agganciavano video su nucleare/demografia (20/05/2026).
    r"^/?comunicazioni/2026-05-20-sciami-api-estate-recupero-genzano/?$",
    #  - balneazione laghi Nemi/Albano: l'articolo parla di sicurezza in
    #    acqua; i laghi sono di ORIGINE vulcanica, quindi l'ancora "vulcanico"
    #    pesca l'intero catalogo di video su eruzioni/gas (fuori tema). Nessun
    #    video di balneazione nei canali → niente sezione (20/05/2026).
    r"^/?comunicazioni/2026-08-12-balneazione-laghi-nemi-albano-sicurezza/?$",
]


# Mini-lemmatizzazione PC: forme plurali → singolari per matchare titoli
# di video DPC (che usano forme tecniche al singolare).
LEMMA_PC = {
    "alluvioni": "alluvione",
    "frane": "frana",
    "terremoti": "terremoto",
    "incendi": "incendio",
    "maremoti": "maremoto",
    "tsunamis": "tsunami",
    "scosse": "scossa",
    "evacuazioni": "evacuazione",
    "esercitazioni": "esercitazione",
    "bollettini": "bollettino",
    "emergenze": "emergenza",
    "criticita": "criticità",
    "allerte": "allerta",
    "boschive": "boschivo",
    "boschivi": "boschivo",
    "vulcani": "vulcano",
    "vulcanici": "vulcanico",
    "vulcaniche": "vulcanico",
    "sismiche": "sismico",
    "sismici": "sismico",
    "idrogeologici": "idrogeologico",
    "idrogeologiche": "idrogeologico",
    "operativi": "operativo",
    "operative": "operativo",
    "comunali": "comunale",
    "regionali": "regionale",
    "nazionali": "nazionale",
    "esondazioni": "esondazione",
    "smottamenti": "smottamento",
    "frequenze": "frequenza",
    "radiocomunicazioni": "radiocomunicazione",
    "telecomunicazioni": "telecomunicazione",
    "soccorsi": "soccorso",
    "interventi": "intervento",
    "centri": "centro",
    "sale": "sala",
    "piani": "piano",
    "rischi": "rischio",
    "fenomeni": "fenomeno",
}


# Whitelist lessicale PC-specifica per i canali divulgativi non-tematici
# (Geopop, Focus, NatGeo Italia, Rai Documentari, CICAP, Link4Universe,
# CNR). Questi canali pubblicano molti contenuti fuori scope PC; vengono
# ammessi al cross-match SOLO se il titolo contiene almeno una keyword di
# questa lista (case-insensitive, substring match).
#
# I canali tematici PC (DPCgov, Io non rischio, Abili a Proteggere, INGV,
# ISPRA, VVF, CRI, CMCC) sono marcati tematico_pc=True nel catalogo e
# entrano nel match senza filtro.
DIVULGATIVO_PC_KEYWORDS = [
    # Sismico
    "terremot", "sism", "magnitud", "mercalli", "faglia", "faglie", "epicentr",
    "tettonic", "earthquake", "richter", "subduzion", "subduction",
    # Vulcanico
    "vulcan", "eruzion", "magma", "lava", "cratere", "vesuvio", "etna", "stromboli",
    "campi flegrei", "marsili", "krakat", "pompei", "ercolan",
    "colli albani", "kilauea", "fuji", "mauna loa", "santorini", "tambora",
    "yellowstone", "phlegr", "ischia", "volcan", "eruption",
    "piroclast", "pyroclast", "lapilli", "tefra", "tephra", "bradisism", "bradyseism",
    # Tsunami / maremoto
    "tsunami", "maremoto", "onda anomala", "megaonda", "megatsunami",
    # Idrogeologico
    "frana", "frane", "alluvion", "idrogeologic", "valanga", "smottament",
    "dissest", "esondazion", "piena ", "allagament", "nubifrag",
    "flood", "landslide", "mudslide", "rockslide", "rockfall", "debris flow",
    "avalanche", "voragine", "sinkhole",
    # Incendi
    "incendi", "antincend", "divamp", "rogo ", "boschiv",
    "wildfire", "bushfire", "vegetation fire", "forest fire",
    # Meteorologia estrema
    "ondata di caldo", "heatwave", "heat wave", "caldo estremo",
    "temporal", "tempesta", "uragan", "ciclon", "tornad", "grandin",
    "hurricane", "typhoon", "cyclone", "tornado", "thunderstorm",
    "vento forte", "raffica", "raffiche", "bora", "scirocco", "libeccio", "tramontana",
    "strong wind", "nevicat", "gelat", "blizzard",
    # Blackout / infrastrutture
    "blackout", "interruzione di corrente", "crisi energetica",
    "power outage", "power cut", "grid failure",
    "diga ", "dighe", "vajont", "dam break", "dam failure", "dam collapse",
    "ponte crollato", "morandi", "bridge collapse", "viadotto",
    # Chimico / radiologico / nucleare
    "inquinament", "radioattiv", "radioactive", "nuclear", "nucleare", "atomic",
    "chernobyl", "fukushima", "seveso", "bhopal", "three mile island",
    "contaminaz", "diossina", "dioxin", "scoria", "hazmat", "fallout",
    "rifiuti tossici",
    # Disastri / emergenze
    "disastro", "disastr", "calamit", "catastrof", "emergenz", " crisi ",
    "disaster", "catastrophe", "emergency",
    # Eventi storici italiani
    "aquila", "amatrice", "norcia", "irpinia", "friuli", "belice",
    "stava", "versilia", "rigopiano", "polesine", "messina", "molise",
    "sarno", "salerno", "lazio", "abruzzo",
    # Eventi internazionali memorabili
    "haiti", "lisbon", "lisbona", "san francisco", "tohoku", "indonesia",
    "kobe", "spitak", "northridge", "valdivia",
    # Protezione civile
    "protezione civile", "civil protection", "soccors", "evacuaz", "salvataggi",
    "rescue", "first responder",
    # Clima
    "climatic", "cambiamento climatico", "climate change", "global warming",
    "riscaldamento global", "siccit", "drought", "carestia", "famine",
    "el nino", "la nina", "monsoni", "monsoon", "desertificaz",
    # Pandemie / sanità di massa
    "pandemi", "epidem", "spagnola", "peste nera", "black death", "plague",
    "ebola", "covid", "sars", "vaiolo", "smallpox", "colera", "cholera",
    "h1n1", "h5n1",
    # "Cosa succede se" (pattern Geopop molto usato, pertinente PC)
    "cosa succede se", "cosa succederebbe", "what happens if", "what would happen",
    "what if a", "what if the", "what if an",
    # Esplosioni
    "esplosion", "explosion", "blast",
    # Geofisica
    "placca", "rift", "polo magnetico", "magnetic pole", "campo magnetico",
    "magnetosfera", "ionosfera",
    # Astronomia (impatti)
    "asteroid", "meteorit", "comet ", "cometa", "impact crater", "tunguska",
    "chicxulub",
    # Cyber e infrastrutture digitali (di interesse PC)
    "cyberattacc", "cyberattack", "ransomware", "blackout informatic",
    "infrastruttura critica", "critical infrastructure",
    # Eventi storici Italia (recuperati: erano falsi negativi nel test iniziale)
    "vermicino", "alfredino", "rampi",
    "torri gemelle", "world trade center", "twin towers", "9/11", "11 settembre",
    "monte bianco", "mont blanc", "tunnel", "galleria",
    "moby prince", "salermo", "linate",
    "ustica",
    # Geologia applicata
    "geotermic", "geothermal", "stratovulcan", "calder",
    "scossa", "ipocentro",
    # Crollo di edifici/strutture
    "crollo ", "collapse", "crollat",
    # Incidenti industriali
    "fabbrica esplosa", "industrial accident", "chemical spill",

    # --- PC in senso ampio (estensione 2026-05-19): temi del sito che
    # non ricadono nelle categorie "rischio naturale puro" ma sono parte
    # integrante della Protezione Civile e della cittadinanza attiva. ---

    # Operatività e mezzi
    "primo soccorso", "first aid", "bls", "blsd", "dae", "defibrillator",
    "defibrillator", "massaggio cardiaco", "rcp", "cpr", "rianimaz",
    "antisoffocament", "heimlich", "manovre antisoffocamento",
    "drone", "uav", "telerilevament", "remote sensing", "satellite",
    "ricostruzione 3d", "3d reconstruction",
    # Numeri e canali di emergenza
    "numero unico", "single emergency number", "nue", "112", "118",
    "it-alert", "cell broadcast", "wireless emergency alert",
    "early warning", "sistema di allerta",
    # Esercitazioni e formazione
    "esercitazione ", "simulazione ", "drill ", "exercise ", "training ",
    "addestrament", "formazione di emergenza",
    # Volontariato e cittadinanza
    "volontariat", "volunteer", "volunteering",
    "cittadinanza attiv", "active citizenship",
    "terzo settore", "third sector", "ets ",
    "sussidiariet", "subsidiarit",
    # PC europea
    "ucpm", "ercc", "resceu", "rescue eu", "meccanismo unionale",
    "civil protection mechanism", "european civil protection",
    "copernicus ems", "copernicus emergency",
    # Psicologia emergenza
    "psicologia dell'emergenza", "psicologia emergenza",
    "trauma psicologic", "stress post-traum", "ptsd",
    "psychological first aid", "pfa ",
    "resilienz", "resilience", "comunità resilienti",
    # Inclusione e accessibilità
    "disabilit", "disability", "inclusion", "inclusivit",
    "accessibilit", "accessibility",
    "persone vulnerabil", "vulnerable people", "vulnerabilit",
    "didrr",
    # Patrimonio culturale in emergenza
    "patrimonio cultural", "cultural heritage in emergency",
    "tutela beni cultural", "caschi blu cultura",
    # Piano emergenza e kit
    "piano di emergenza", "emergency plan", "emergency planning",
    "kit di emergenza", "emergency kit", "go bag", "go-bag",
    "piano comunale", "centro operativo comunale", "coc ",
    "coi ", "centro operativo intercomunale",
    "evacuazione", "evacuation", "evacuat",
    # Cartografia e GIS
    "cartografia", "mappa del rischio", "risk map", "gis ",
    "carta tematic", "thematic map",
    # Ricostruzione, recovery
    "ricostruzione", "rebuilding", "post-disaster recovery", "ricostruir",
    # Norme e codici
    "codice della protezione civile", "civil protection code",
    "io non rischio", "campagna io non rischio",
    "sendai framework", "hyogo framework",
    "iso 22324", "iso 22329", "iso 22361", "iso 22395", "iso 31000",
    # Sicurezza nei luoghi di lavoro (collegato a PCTO)
    "sicurezza sul lavoro", "workplace safety", "occupational safety",
    "dlgs 81", "decreto 81", "d.lgs. 81",
    "dpi ", "dispositivi protezione individual",
    # Stradale (incidenti e gestione)
    "incidente stradale", "road accident", "traffic accident",
    "sicurezza stradale", "road safety",
    # Antisismica e costruzione
    "antisismic", "isolator", "base isolation", "miglioramento sismico",
    "adeguamento sismic", "vulnerabilità sismic",
    # Animali in emergenza
    "animali in emergenza", "pets in emergency", "pet evacuation",
    # Fake news e comunicazione di crisi
    "fake news", "disinformazion", "disinformation", "misinformation",
    "comunicazione di crisi", "crisis communication",
    "verifica delle fonti", "fact check",
    # Radiocomunicazioni
    "radioamator", "ham radio", "banda cb", "vhf", "uhf",
    "radio di emergenza",
    # Allerta meteo (specifico PC)
    "allerta meteo", "weather warning", "codice giallo", "codice arancion",
    "codice rosso", "centro funzionale",
    # Sicurezza ambientale e prevenzione
    "prevenzione", "prevention", "mitigazione del rischio",
    "risk mitigation", "early action",
]


# Gate tematico sull'ANCORA: un match pagina↔video è valido solo se almeno
# una parola-ancora (dal lato pagina) è realmente PC-tematica. È la difesa
# strutturale contro gli agganci su parole generiche che, essendo rare nel
# corpus del sito, prendevano peso IDF pieno e diventavano "ancore forti"
# pur non c'entrando nulla (es. "presenta", "fatta", "europa", "storia",
# "morti", "bisogno"). La whitelist delle stop-words da sola era whack-a-mole:
# ogni rigenero faceva emergere un nuovo strato di parole generiche.
# Gli stem topici a parola singola sono derivati da DIVULGATIVO_PC_KEYWORDS
# (terremot, alluvion, vulcan, frana, soccors, evacuaz, aquila, fukushima…)
# + un set curato di luoghi/sigle PC legittimi non presenti nel vocabolario.
TOPICAL_ANCHOR_STEMS = {
    kw.strip() for kw in DIVULGATIVO_PC_KEYWORDS
    if " " not in kw.strip() and len(kw.strip()) >= 4
    and re.fullmatch(r"[a-zàèéìòù]+", kw.strip())
} | {
    # luoghi/termini disastro legittimi assenti dal vocabolario divulgativo
    "emilia", "marche", "umbria", "liguria", "genova", "nemi", "albano",
    "castelli", "genzano", "montagna", "neve", "gelo", "fulmine",
    "mareggiata", "mareggiate", "grandinata",
}
# Sigle/termini brevi (< 4 char) PC-tematici, accettati come match esatto.
TOPICAL_ANCHOR_SHORT = {
    "coc", "coi", "dpc", "vvf", "dae", "rcp", "cpr", "bls", "blsd", "nue",
    "112", "118", "gis", "ets", "odv", "sar", "ptsd", "ucpm", "ercc", "dpi",
}

# Denylist di VIDEO specifici (per ID YouTube): controllo finale di ultimo
# miglio per i falsi positivi che hanno una parola topica ma un contesto
# NON di protezione civile (la parola è usata in senso non-PC). Nessun
# algoritmo a keyword li distingue, quindi si escludono a mano. Persiste ai
# rigeneri mensili (a differenza della rimozione manuale dal file YAML).
# Aggiungere qui l'ID quando si trova un video fuori tema nella mappa.
DENY_VIDEO_IDS = {
    # Audit 18/08/2026 — video CMCC in lingua inglese sfuggiti al filtro lingua
    # (titolo senza marcatori EN evidenti), comparsi sul dossier Covid:
    "0rv_smpJQvM",  # "Fostering green finance for a climate-resilient post-COVID-19 recovery" (EN)
    "6G0gfNm8IRk",  # "Impacts of COVID-19 and recovery packages on climate change mitigation" (EN)
    "A1QE73885gQ",  # "Una battaglia di palle di neve" (neve, ma è svago)
    "WtnfQiTiDm0",  # "Trump all'ONU: ho fatto finire 7 guerre" (climatico, politica)
    "DGA46S82EMw",  # "Una giornata con i Masai in Kenya" (siccità, reportage)
    "srrLwK0ybVE",  # "Forio d'Ischia: Man kills his ex-wife's mother" (ischia, cronaca, EN)
    # Audit 20/05/2026 — falsi positivi su parola topica ma contesto diverso:
    "HQ_Q_hYO0Os",  # "Il cerino in mano del piromane: incendio in Irpinia" (arson, su articoli TERREMOTO Irpinia)
    "MkOC31Yfhjs",  # "Cosa accadrebbe se la Terra colpita da tempesta solare" (tempesta SOLARE su Vaia, vento)
    "uvuPi3HQgLU",  # "Dirotta un aereo e sparisce nella tempesta" (dirottamento)
    "8MjAWLhRIWk",  # "L'aurora boreale durante la tempesta [geomagnetica]" (tempesta solare)
    "ngOlPmFgpXE",  # "Ischia, Capri, Procida: mare in tempesta" (mareggiata, su Vaia/Ischia-terremoto)
    "-Jcz-q5tih4",  # "Ponte sullo stretto di Messina: sarebbe un'assurdità" (politica, su Messina-terremoto)
    "bwPQHnbeYpo",  # "Ponte sullo Stretto di Messina: il progetto" (infrastruttura)
    "1CGJQMQiurQ",  # "Earthquake 4.6 in Naples" (titolo EN)
    "49g9E2959gc",  # "Myanmar M7.7 Earthquake - A Geological Look" (titolo EN)
    "ssk5ngl30us",  # "MappaMondi - Myanmar hit by war and earthquake" (titolo EN)
    "v088X7C49fk",  # "La neve di primavera: il drone in Alta Badia" (scenico, non emergenza)
    "RdomcSSu6PY",  # "Come lo sport elimina ogni disabilità" (sport, non emergenza)
    "it9NrBPZB0Y",  # "Le protesi supertech" (tech, non emergenza)
    "SPG1k8nnCeY",  # "La nuova Diga foranea di Genova" (frangiflutti, non alluvione/diga-disastro)
    # Audit Geopop 01/09/2026 — video divulgativi senza contenuto di PC:
    "84LU4UUU_2c",  # "La prima funicolare d'Italia fu costruita sul Vesuvio" (trasporti)
    "BzItiC5kzfk",  # "Monte Taranaki: il vulcano visto dallo spazio ha la forma di un cerchio" (curiosità)
    "DpALnPyfFm4",  # "Olympus Mons, mega vulcani su Marte" (planetologia)
    "W3C02y8A8LY",  # "Fusione nucleare, a che punto è la ricerca? ITER" (energia, non rischio radiologico)
    "xo0yPCPZcb8",  # CICAP "Fusione nucleare: facciamo chiarezza" (energia, non rischio radiologico)
    "-TOGq4pkZiM",  # "Navi rompighiaccio a propulsione nucleare" (trasporti)
    "l4RqFtMYvjo",  # "Cos'è la valigetta nucleare" (geopolitica)
    "_OYMeOYJJFs",  # "Terremoto in Italia - 9 scosse in 20 minuti nell'Adriatico" (cronaca datata)
    "WI0S15ShvsM",  # "Cosa fa un geologo?" (orientamento professionale)
    # Primo giro dei feed RSS settimanali (02/09/2026):
    "adkGcJt0P6s",  # "Uranio: la risorsa chiave per la fissione nucleare" (economia mineraria)
    "o9AKgqvEI4E",  # "Fusione nucleare USA, perché sono tutti così eccitati" (ricerca energetica)
    "nrnpCGMiEQU",  # Solarino "Il temporale provoca un black out, subito risolto" (aneddoto, agganciava 7 pagine su temporali/fulmini)
    "9olXT9ucTKk",  # Link4Universe "Lancio missione di SALVATAGGIO spaziale per il telescopio Swift" (spazio, non soccorso)
    "58YdCsnjopE",  # Link4Universe "Dragonfly - Drone nucleare nei cieli di Titano" (sonda spaziale, non rischio radiologico)
    "JHV2yok0r2I",  # Link4Universe "Dragonfly: andremo su Titano con un drone nucleare" (idem)
    "8EA8swJodJs",  # rai-news "La storia del nucleare in Iran" (geopolitica, non rischio radiologico)
}


# ---------------------------------------------------------------------------
# CURATELA EDITORIALE (audit Geopop 01/09/2026)
#
# Due liste che il cross-match algoritmico NON può dedurre da solo e che
# persistono ai rigeneri mensili (vale la regola "i fix vanno nel generatore,
# mai solo nel YAML"):
#
# - FORCE_MATCHES: abbinamenti pagina → video verificati a mano (video
#   pertinente al SOGGETTO della pagina, sfuggito all'IDF perché le parole
#   chiave non coincidono: es. "Terremoto a Milano rilevato da Google" per
#   l'articolo sugli smartphone-sismometri). Vengono messi in testa alla
#   lista della pagina con score 10 e `curato: true`; la pagina viene creata
#   anche se l'algoritmo non le aveva trovato nulla.
# - DENY_PAGE_VIDEO: falsi positivi di una SINGOLA pagina (il video è
#   pertinente altrove, quindi non va in DENY_VIDEO_IDS): es. il video sulla
#   tempesta Vaia sul dossier della tempesta SOLARE.
#
# Chiavi pagina = stesse di data/video_correlati.yaml (build_key):
# "comunicazioni/<slug>", "rischi-prevenzione/<slug>", "manuale/<slug>"…
# ---------------------------------------------------------------------------
FORCE_MATCHES = {
    # Sismico
    "comunicazioni/2027-02-06-turchia-siria-2023-terremoto-cooperazione-italiana": [
        "pjoN6F-nchA",  # Geopop — Perché il terremoto in Turchia e Siria è stato così devastante?
    ],
    "comunicazioni/2026-06-26-smartphone-sismometri-allerta-terremoto-venezuela": [
        "fJsKkMR4EIM",  # Geopop — Terremoto a Milano rilevato da Google: come funziona il sistema
    ],
    "comunicazioni/2026-10-06-sismicita-castelli-romani-zona-2b": [
        "gw33yaQUXb0",  # Geopop — Dalla mappa dei terremoti: in che zone si verificano gli eventi sismici
    ],
    # Vulcanico / Campi Flegrei
    "comunicazioni/2026-05-22-campi-flegrei-radici-sistema-magmatico": [
        "r4AgouD-gV8",  # Geopop — Anidride carbonica ai Campi Flegrei: cosa succede e possibili rischi
        "MvPO-DsgJtQ",  # Geopop — Terremoto ai Campi Flegrei sentito a Napoli: il meccanismo geologico
    ],
    "rischi-prevenzione/rischio-vulcanico": [
        "HjhnA7sC1OU",  # Geopop — Piano di evacuazione dei Campi Flegrei e Vesuvio: intervista a chi li progetta
    ],
    # Industriale
    "comunicazioni/2026-10-20-rischio-industriale-seveso": [
        "6WMacaxW-ck",  # Geopop — Esplosione al deposito Eni di Calenzano: le possibili cause
        "CZ-o14lvcJw",  # Geopop — Incendio in un'azienda a Cavenago: il monitoraggio dell'aria dei tecnici
    ],
    "comunicazioni/2026-06-29-viareggio-2009-memoria-rischio-industriale": [
        "tnVy7Bl35Wg",  # Geopop — L'incidente ferroviario di Viareggio: ricostruzione 3D e cause
    ],
    # Idrogeologico / glaciale
    "comunicazioni/2026-08-27-nepal-tibet-colata-detritica-bhote-koshi": [
        "SBzCu3Ej4cw",  # Geopop — Cosa è successo in Nepal: dal ghiacciaio all'alluvione (01/09/2026)
    ],
    # Idraulico / clima
    "comunicazioni/2026-09-15-rischio-idraulico-urbano-genzano": [
        "QiLt_8rwC-s",  # Geopop — Il tunnel sotterraneo di Tokyo (G-Cans) contro le inondazioni
    ],
    "comunicazioni/2026-09-15-alluvione-marche-2022-bombe-acqua-cambiamento-climatico": [
        "za7qd7dFF0k",  # Geopop — Ondata di caldo e alluvioni: perché i due fenomeni sono collegati
    ],
    # Siccità
    "rischi-prevenzione/siccita": [
        "PvY7kRxwOGI",  # Geopop — Dissalare l'acqua di mare contro la crisi idrica: pro e contro
    ],
    "comunicazioni/2026-07-18-siccita-gestione-risorsa-idrica": ["PvY7kRxwOGI"],
    "comunicazioni/2026-08-18-siccita-lazio-risorsa-idrica": ["PvY7kRxwOGI"],
    "manuale/720-rischio-idrico-siccita": ["PvY7kRxwOGI"],
}

DENY_PAGE_VIDEO = {
    # Tempesta SOLARE ≠ tempesta Vaia (vento)
    ("dossier/la-tempesta-solare", "cmEzpKqaTEU"),
    # Sciame di Santorini: pertinente solo per il Pollino (sequenza sismica)
    ("rischi-prevenzione/rischio-sismico", "v2VFX_ZIWr8"),
    ("comunicazioni/2026-06-15-sentinel-1c-radar-deformazione-suolo", "v2VFX_ZIWr8"),
    # Scossa M3.9 Campi Flegrei: pertinente solo sulle pagine flegree
    ("comunicazioni/2026-04-25-nepal-2015-gorkha-terremoto", "ROlhXYtdP_w"),
    ("comunicazioni/2026-05-22-studio-ingv-fluidi-sequenza-sismica-2016", "ROlhXYtdP_w"),
    ("comunicazioni/2026-06-26-smartphone-sismometri-allerta-terremoto-venezuela", "ROlhXYtdP_w"),
    ("comunicazioni/2026-10-30-norcia-2016-decimo-anniversario-sequenza-centro-italia", "ROlhXYtdP_w"),
    # Sciame in Adriatico 2022: pertinente solo per Marche 2016 (stessa area)
    ("comunicazioni/2026-05-06-friuli-1976-cinquant-anni-protezione-civile", "ssHdkhrAvz0"),
    ("comunicazioni/2026-06-26-smartphone-sismometri-allerta-terremoto-venezuela", "ssHdkhrAvz0"),
    ("comunicazioni/2026-12-28-messina-reggio-calabria-1908-soccorso-moderno", "ssHdkhrAvz0"),
    # Diga romana in Spagna: non c'entra con la tragedia del Vajont
    ("comunicazioni/2026-10-09-vajont-1963-tragedia-prevista", "ts9vqg-I7f4"),
    # Frana di Sarno sugli articoli satellitari (Sentinel, IRIDE): fuori soggetto
    ("comunicazioni/2026-06-15-sentinel-1c-radar-deformazione-suolo", "fpeEmFI5G8s"),
    ("comunicazioni/2026-07-03-iride-costellazione-osservazione-terra-operativa", "fpeEmFI5G8s"),
    # Articolo sull'INCENDIO del Parco del Vesuvio: i video sul rischio vulcanico sono fuori tema
    ("comunicazioni/2025-08-16-volontari-in-allerta", "xwXlvUH1sa0"),
    ("comunicazioni/2025-08-16-volontari-in-allerta", "KG8xHth3n_8"),
    ("comunicazioni/2025-08-16-volontari-in-allerta", "2tC0fE5ZgNo"),
    # Radon: il confronto Etna/Vesuvio non c'entra
    ("dossier/radon-il-nemico-invisibile", "KG8xHth3n_8"),
    # Direttiva Seveso (rischio industriale) ≠ fiume Seveso (esondazione a Milano)
    ("comunicazioni/2026-10-20-rischio-industriale-seveso", "Zh_2N7Wulus"),
    # Primo giro dei feed RSS settimanali (02/09/2026)
    ("comunicazioni/2026-07-12-etiopia-magma-satelliti-monitoraggio-vulcani", "r8OySuD_Fi8"),  # esperimento didattico "vulcano di Anita" su articolo satellitare
    ("dossier/genzano-castelli-i-nostri-rischi", "r8OySuD_Fi8"),
    ("comunicazioni/2026-06-15-sentinel-1c-radar-deformazione-suolo", "Mep1CHoxbIk"),  # "Come funzionano i vulcani?" su articolo radar satellitare
    ("dossier/il-lago-che-si-abbasso", "AfJMiAw2UnI"),  # parossismo Etna sul dossier dei laghi
    ("dossier/vulcano-sotto-casa", "o5oUgB5U1RM"),  # volo spettacolare sull'Etna (cronaca)
    ("comunicazioni/2026-01-31-neve-castelli-romani-organizzazione", "JEhyPLmVrEc"),  # sicurezza in montagna sull'organizzazione neve
    ("comunicazioni/2026-04-27-terremoto-cosa-fare-durante-dopo-la-scossa", "cRTmbi7MFSo"),  # danni Emilia 2012 su articolo di comportamento
    ("comunicazioni/2025-08-16-volontari-in-allerta", "HjhnA7sC1OU"),  # piano evacuazione Flegrei/Vesuvio su articolo dell'INCENDIO del Vesuvio
    ("comunicazioni/2026-06-15-sentinel-1c-radar-deformazione-suolo", "_AYUUv69F3U"),  # esercitazione vulcanica su articolo radar satellitare
    ("comunicazioni/2026-04-27-terremoto-cosa-fare-durante-dopo-la-scossa", "0--y1oKrz-4"),  # DPC "San Carlo, i danni dopo la scossa del 20…" danni Emilia 2012 su articolo di comportamento
    ("comunicazioni/2026-04-27-terremoto-cosa-fare-durante-dopo-la-scossa", "4-r2rPCOEPM"),  # DPC "Finale Emilia, i danni dopo la scossa de…" danni Emilia 2012 su articolo di comportamento
    ("comunicazioni/2026-04-27-terremoto-cosa-fare-durante-dopo-la-scossa", "KjQSuaVrjlY"),  # DPC "Mirandola, i danni dopo la scossa del 29…" danni Emilia 2012 su articolo di comportamento
    ("comunicazioni/2026-04-27-terremoto-cosa-fare-durante-dopo-la-scossa", "beYhBfj9LoE"),  # DPC "Sant'Agostino, i danni dopo la scossa de…" danni Emilia 2012 su articolo di comportamento
}


def apply_curation(results: dict, videos_by_id: dict, page_meta: dict,
                   max_per_page: int) -> tuple[int, int]:
    """Applica DENY_PAGE_VIDEO e FORCE_MATCHES ai risultati del cross-match.

    - results: {page_key: {"title","url","video":[...]}} (modificato in place)
    - videos_by_id: {youtube_id: voce del catalogo}
    - page_meta: {page_key: {"title","url"}} per creare pagine assenti
    Ritorna (n_rimossi, n_forzati).
    """
    removed = 0
    for key, vid in DENY_PAGE_VIDEO:
        r = results.get(key)
        if not r:
            continue
        before = len(r["video"])
        r["video"] = [v for v in r["video"] if v["id"] != vid]
        removed += before - len(r["video"])
        if not r["video"]:
            del results[key]
    forced = 0
    for key, ids in FORCE_MATCHES.items():
        meta = page_meta.get(key)
        if meta is None:
            print(f"  [curatela] pagina non trovata, salto: {key}", file=sys.stderr)
            continue
        r = results.setdefault(key, {"title": meta["title"], "url": meta["url"], "video": []})
        existing = {v["id"] for v in r["video"]}
        head = []
        for vid in ids:
            v = videos_by_id.get(vid)
            if v is None:
                print(f"  [curatela] video non in catalogo, salto: {vid}", file=sys.stderr)
                continue
            if vid in existing:
                continue
            head.append({
                "id": v["id"], "titolo": v["titolo"], "url": v["url"],
                "canale": v.get("canale", ""), "score": 10.0,
                "overlap": [], "anchored": [], "is_lis": False, "curato": True,
            })
            forced += 1
        r["video"] = (head + r["video"])[:max_per_page]
    return removed, forced


# Termini PC ma TROPPO astratti per ancorare da soli: agganciano qualsiasi
# cosa (es. "crisi" → 9/11 ↔ "crisi energetica"; "disastro" → canadair AIB ↔
# "disastro delle Ande"; "ricostruzione" → Friuli 1976 ↔ "esplosione Beirut").
# Valgono SOLO se nel match c'è anche un'ancora topica specifica.
TOPICAL_BROAD_STEMS = {
    "crisi", "disastro", "disastr", "disaster", "catastrof", "catastrophe",
    "ricostruzion", "ricostruzione", "ricostruir", "tragedia", "tragedi",
    "emergency", "evento", "eventi", "incidente", "incidenti",
    # "crollo" generico agganciava crollo di ghiacciai/archi naturali ad
    # articoli su terremoti (crollo edifici). Valido solo con co-aggancio
    # specifico (es. "morandi", "ponte morandi").
    "crollo", "crollat", "collapse",
}


def _anchor_is_broad(w: str) -> bool:
    for s in TOPICAL_BROAD_STEMS:
        if w == s or (len(s) >= 5 and w.startswith(s)):
            return True
    return False


def _anchor_is_topical(w: str) -> bool:
    """True se la parola-ancora è PC-tematica (rischio, soccorso, disastro,
    luogo di un evento, sigla operativa). Stem ≥5 char → prefix match
    (terremoto→terremot); stem 4 char e sigle brevi → solo match esatto
    (evita falsi positivi tipo 'lavandino' che inizia per 'lava')."""
    if w in TOPICAL_ANCHOR_SHORT:
        return True
    for s in TOPICAL_ANCHOR_STEMS:
        if w == s:
            return True
        if len(s) >= 5 and w.startswith(s):
            return True
    return False


def _anchor_is_topical_specific(w: str) -> bool:
    """Ancora topica E specifica (non un termine PC troppo astratto)."""
    return _anchor_is_topical(w) and not _anchor_is_broad(w)


def _is_italian_title(title: str) -> bool:
    """Heuristic per filtrare i titoli in inglese (Geopop e altri
    canali divulgativi pubblicano spesso versione bilingue: i video
    con titolo in inglese non hanno senso sul nostro sito italiano).

    Rigetta se:
    - inizia con tipiche parole inglesi (The, How, What, Why, Is, Are,
      Can, Does, etc.)
    - contiene pattern inglesi distintivi (' of the ', ' in the ',
      ' how to ', ' it's ', etc.)
    - >40% delle parole sono stopword inglesi pure"""
    if not title:
        return True
    t = title.lower().strip()
    en_prefixes = (
        "the ", "how ", "what ", "why ", "is ", "are ", "can ",
        "do ", "does ", "did ", "was ", "were ", "when ", "where ",
        "with ", "from ", "this ", "these ", "those ", "that ",
        "which ", "who ", "whose ", "every ", "any ", "no ",
        "meet ", "let ", "let's ", "it's ", "here ", "there ",
        "a guide ", "an introduction ",
    )
    if t.startswith(en_prefixes):
        return False
    en_patterns = (
        " the ", " is ", " are ", " was ", " were ", " of the ",
        " in the ", " on the ", " at the ", " to the ", " for the ",
        " from the ", " with the ", " by the ", " and the ",
        " how to ", " what's ", " it's ", " they're ", " we're ",
        " you're ", " doesn't ", " don't ", " won't ", " can't ",
        " could ", " would ", " should ", " might ", " must ",
        " between ", " against ", " through ", " among ",
        " because ", " however ", " although ", " whether ",
        " who's ", " whose ", " where's ", " there's ",
    )
    if any(p in (" " + t + " ") for p in en_patterns):
        return False
    return True


def _divulgativo_pc_relevant(title: str) -> bool:
    """True se il titolo di un canale divulgativo non-tematico contiene
    almeno una keyword PC-tematica (in senso ampio: rischi naturali,
    eventi storici, primo soccorso, volontariato, PC europea, psicologia
    emergenza, inclusione, comunicazione di crisi, ecc.).
    Match case-insensitive su substring (non word-boundary, perché molte
    voci sono prefissi tipo 'terremot' per coprire terremoto/terremoti)."""
    t = title.lower()
    return any(kw in t for kw in DIVULGATIVO_PC_KEYWORDS)


def tokenize(text: str) -> set[str]:
    """Estrae keywords da text. Include:
       - parole lunghe ≥4 caratteri (es. "terremoto", "alluvione")
       - sigle maiuscole 3+ caratteri (es. "COC", "DPC", "ASL", "INGV")
       - lemmatizzazione PC (plurale→singolare) per matchare titoli DPC
       Esclude stop-words italiane."""
    # 1) Sigle maiuscole (preservate dal testo originale)
    sigle = {s.lower() for s in re.findall(r"\b[A-Z]{3,}\b", text)}
    # 2) Parole lowercase ≥4 char + lemmatizzazione PC
    t = text.lower()
    t = re.sub(r"[^a-zàèéìòùù\s]", " ", t)
    parole = set()
    for w in t.split():
        if len(w) < 4 or w in STOPWORDS_IT:
            continue
        parole.add(LEMMA_PC.get(w, w))
    return parole | sigle


def extract_page_data(path: Path) -> dict:
    """Return {title, title_kw, desc_kw, body_kw} with separated keyword sets."""
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}
    m = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if not m:
        return {}
    fm_text, body = m.group(1), m.group(2)
    title = ""
    desc = ""
    for line in fm_text.splitlines():
        s = line.strip()
        if s.startswith("title:") and not title:
            title = s[6:].strip().strip('"\'')
        elif s.startswith("description:"):
            desc = s[12:].strip().strip('"\'')
    headings = " ".join(re.findall(r"^##+\s+(.+)$", body, re.MULTILINE))
    body_clean = re.sub(r"\{\{<[^>]*>\}\}", " ", body)[:3000]
    return {
        "title": title,
        "title_kw": tokenize(title),
        "desc_kw": tokenize(desc) - tokenize(title),         # solo nuove rispetto al title
        "body_kw": tokenize(headings + " " + body_clean) - tokenize(title) - tokenize(desc),
    }


def build_url(content_root: Path, md_path: Path) -> str:
    rel = md_path.relative_to(content_root)
    s = str(rel)
    # Drop _index.md → directory URL
    if s.endswith("_index.md"):
        s = s[:-len("_index.md")]
    elif s.endswith(".md"):
        s = s[:-3] + "/"
    # Normalize
    return "/" + s.strip("/") + ("" if s == "" else "/")


def build_key(content_root: Path, md_path: Path) -> str:
    """Stable key per il lookup Hugo: path relativo a content/, senza
    estensione .md né suffisso /_index. Esempio:
       content/rischi-prevenzione/rischio-sismico.md
       → 'rischi-prevenzione/rischio-sismico'
       content/rischi-prevenzione/kit-emergenza/_index.md
       → 'rischi-prevenzione/kit-emergenza'"""
    rel = md_path.relative_to(content_root)
    s = str(rel)
    if s.endswith("/_index.md"):
        s = s[:-len("/_index.md")]
    elif s == "_index.md":
        s = ""
    elif s.endswith(".md"):
        s = s[:-3]
    return s


def page_excluded(url: str) -> bool:
    for pat in SKIP_PAGE_PATTERNS:
        if re.match(pat, url):
            return True
    return False


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--max-per-page", type=int, default=5,
                   help="Max video correlati per pagina (default: 5)")
    p.add_argument("--min-score", type=float, default=2.0,
                   help="Punteggio minimo per accettare un match (default: 2.0)")
    p.add_argument("--output", default="data/video_correlati.yaml")
    args = p.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    content_root = repo_root / "content"

    # Carica catalogo video
    with open(repo_root / "data" / "video_dpc_catalogo.yaml") as f:
        catalogo = yaml.safe_load(f)
    videos = catalogo["video"]
    print(f"Catalogo: {len(videos)} video totali", file=sys.stderr)

    # Carica registry LIS per marcare i video LIS nel risultato (NON per
    # escluderli: un video LIS pertinente al contesto specifico di un
    # articolo è prezioso anche se il badge LIS è già presente sulla
    # pagina madre del rischio. Cf. caso articolo "Centro Operativo
    # Comunale COC" — il video LIS specifico sul COC va integrato).
    with open(repo_root / "data" / "lis.yaml") as f:
        lis_data = yaml.safe_load(f)
    lis_video_ids = set()
    for v in (lis_data.get("video") or {}).values():
        url = v.get("youtube_url", "")
        m = re.search(r"youtu\.be/([A-Za-z0-9_-]{11})", url)
        if m:
            lis_video_ids.add(m.group(1))
    print(f"Video LIS marcati: {len(lis_video_ids)} (inclusi nel cross-match)", file=sys.stderr)

    # Scansiona contenuti sito
    pages = []
    for md in content_root.rglob("*.md"):
        url = build_url(content_root, md)
        if page_excluded(url):
            continue
        pd = extract_page_data(md)
        if not pd or not pd.get("title"):
            continue
        all_kw = pd["title_kw"] | pd["desc_kw"] | pd["body_kw"]
        if len(all_kw) < 5:
            continue
        pages.append({
            "key": build_key(content_root, md),
            "url": url,
            "title": pd["title"],
            "title_kw": pd["title_kw"],
            "desc_kw": pd["desc_kw"],
            "body_kw": pd["body_kw"],
            "all_kw": all_kw,
        })
    print(f"Pagine sito analizzate: {len(pages)}", file=sys.stderr)

    # Costruisci IDF dei video (frequenza delle keyword nei titoli video).
    # Filtra a monte i video dei canali NON-TEMATICI: solo quelli con
    # titolo PC-pertinente (whitelist DIVULGATIVO_PC_KEYWORDS) entrano
    # nel cross-match. I canali tematici PC (DPCgov, INGV, ISPRA, VVF,
    # CRI, CMCC, Io non rischio, Abili a Proteggere) sono marcati
    # tematico_pc=True nel catalogo e passano senza filtro.
    canali_tematici = {ck for ck, cm in catalogo.get("canali", {}).items()
                       if cm.get("tematico_pc")}
    video_keywords = {}
    skipped_divulgativo = 0
    skipped_lingua = 0
    for key, v in videos.items():
        # Denylist video di ultimo miglio (falsi positivi a contesto non-PC)
        if v["id"] in DENY_VIDEO_IDS:
            continue
        # Vincolo lingua: il sito è in italiano, escludi i video con
        # titolo in inglese (Geopop ne ha ~14% bilingue, anche altri
        # canali divulgativi pubblicano in inglese per audience globale)
        if not _is_italian_title(v["titolo"]):
            skipped_lingua += 1
            continue
        ck = v.get("canale", "")
        if ck not in canali_tematici and not _divulgativo_pc_relevant(v["titolo"]):
            skipped_divulgativo += 1
            continue
        kw = tokenize(v["titolo"])
        if not kw:
            continue
        video_keywords[key] = {
            "v": v,
            "kw": kw,
            "is_lis": v["id"] in lis_video_ids,
        }
    print(f"Video candidati: {len(video_keywords)} "
          f"(divulgativi filtrati out per non-pertinenza PC: {skipped_divulgativo}, "
          f"video in inglese scartati: {skipped_lingua})",
          file=sys.stderr)

    # IDF su pagine sito: parole molto frequenti = peso 0.2
    df = defaultdict(int)
    for p in pages:
        for k in p["all_kw"]:
            df[k] += 1
    n_pages = len(pages)
    weights = {}
    th_generic = max(2, int(0.20 * n_pages))
    th_common = max(2, int(0.10 * n_pages))
    for k, c in df.items():
        if c > th_generic:
            weights[k] = 0.2
        elif c > th_common:
            weights[k] = 0.6
        else:
            weights[k] = 1.0

    # Cross-match con pesi posizionali: title × 3, desc × 2, body × 1.
    # Vincolo: almeno una keyword in overlap deve essere nel titolo o nella
    # description della pagina E avere peso IDF >= 0.7 (cioè non super-generica).
    results = {}
    for page in pages:
        candidates = []
        title_desc_kw = page["title_kw"] | page["desc_kw"]
        for vkey, vdata in video_keywords.items():
            overlap = page["all_kw"] & vdata["kw"]
            if not overlap:
                continue
            # Vincolo qualità: almeno una keyword "ancorata" al titolo/desc
            # della pagina. Accetto anche peso IDF moderato (>= 0.5) per
            # consentire match su frasi tecniche con parole comuni nel sito
            # (es. "Centro Operativo Comunale" dove tutte le parole sono
            # frequenti ma il match è genuino sulla terminologia tecnica).
            anchored = [k for k in overlap
                        if k in title_desc_kw and weights.get(k, 1.0) >= 0.5]
            if not anchored:
                continue
            # Gate tematico (difesa strutturale): almeno una parola-ancora
            # dev'essere PC-tematica (terremoto, alluvione, soccorso, dae,
            # evacuazione, nome di un disastro…). Senza questo, parole
            # generiche rare nel corpus del sito ("presenta", "fatta",
            # "europa", "storia", "morti", "bisogno") prendevano peso IDF
            # pieno e agganciavano video fuori tema. Vale per TUTTI i canali.
            # Principio editoriale: video pertinente o niente sezione video.
            # Il termine PC dev'essere tra le ancore di titolo/descrizione
            # (non incidentale nel corpo): garantisce che il SOGGETTO della
            # pagina, non un termine di passaggio, sia ciò che lega il video.
            # Es.: un libro sul risparmio alimentare che cita "incendio" nel
            # corpo NON deve agganciare un video sugli incendi boschivi.
            # Inoltre l'ancora topica dev'essere SPECIFICA: i termini PC
            # troppo astratti (crisi, disastro, ricostruzione, tragedia)
            # non bastano da soli, servono con un co-aggancio specifico.
            if not any(_anchor_is_topical_specific(k) for k in anchored):
                continue
            # Vincolo extra per canali divulgativi non-tematici: visto che
            # hanno titoli molto eterogenei (alcuni passano la whitelist PC
            # ma toccano temi ortogonali tipo "10 curiosità sulla Sicilia"),
            # serve un anchor più stringente. Almeno una keyword anchored
            # deve avere peso IDF >= 0.7 (parola tecnico-specifica, non
            # comune nel sito).
            if vdata["v"].get("canale", "") not in canali_tematici:
                strong_anchored = [k for k in anchored
                                   if weights.get(k, 1.0) >= 0.7]
                if not strong_anchored:
                    continue
            # Score posizionale: title × 3, desc × 2, body × 1
            score = 0.0
            for k in overlap:
                w = weights.get(k, 1.0)
                if k in page["title_kw"]:
                    score += w * 3.0
                elif k in page["desc_kw"]:
                    score += w * 2.0
                else:
                    score += w * 1.0
            # Bonus "match esatto titolo→titolo" per parole tecniche rare:
            # quando una keyword RARA nel sito (peso IDF >= 0.9) appare sia
            # nel titolo della pagina sia nel titolo del video, aggiungi +3
            # al score. Serve per favorire match perfetti (es. articolo
            # "Seveso 1976" vs video "The Seveso disaster") rispetto a
            # match generici che pescano parole comuni nel body dell'articolo.
            title_match = [k for k in (page["title_kw"] & vdata["kw"])
                           if weights.get(k, 1.0) >= 0.9]
            score += 3.0 * len(title_match)
            if score < args.min_score:
                continue
            candidates.append({
                "id": vdata["v"]["id"],
                "titolo": vdata["v"]["titolo"],
                "url": vdata["v"]["url"],
                "canale": vdata["v"]["canale"],
                "score": round(score, 2),
                "overlap": sorted(overlap),
                "anchored": sorted(anchored),
                "is_lis": vdata["is_lis"],
            })
        candidates.sort(key=lambda x: -x["score"])
        top = candidates[: args.max_per_page]
        if top:
            results[page["key"]] = {
                "title": page["title"],
                "url": page["url"],
                "video": top,
            }

    # Curatela editoriale (abbinamenti forzati + falsi positivi per pagina)
    videos_by_id = {v["id"]: v for v in videos.values()}
    page_meta = {p["key"]: {"title": p["title"], "url": p["url"]} for p in pages}
    n_removed, n_forced = apply_curation(results, videos_by_id, page_meta, args.max_per_page)
    print(f"Curatela: {n_removed} abbinamenti rimossi, {n_forced} forzati", file=sys.stderr)

    # Stats
    n_pages_with_video = len(results)
    n_video_unique = len({v["id"] for r in results.values() for v in r["video"]})
    total_links = sum(len(r["video"]) for r in results.values())
    print(f"\nRisultato:", file=sys.stderr)
    print(f"  Pagine con almeno 1 video correlato: {n_pages_with_video}", file=sys.stderr)
    print(f"  Video unici usati: {n_video_unique}", file=sys.stderr)
    print(f"  Link video totali: {total_links}", file=sys.stderr)

    # Lookup canale per metadata di attribuzione
    canali = catalogo["canali"]

    out_path = repo_root / args.output
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# Mappa pagina del sito → video correlati pertinenti.\n")
        f.write(f"# Generato da scripts/genera-video-correlati.py via cross-match\n")
        f.write(f"# algoritmico (IDF-weighted) sul catalogo data/video_dpc_catalogo.yaml.\n")
        f.write(f"#\n")
        f.write(f"# Usato dal partial Hugo `video-correlati.html` per renderizzare la\n")
        f.write(f"# sezione 'Approfondimenti video' in fondo agli articoli pertinenti.\n")
        f.write(f"#\n")
        f.write(f"# Pagine coperte: {n_pages_with_video} / Video unici usati: {n_video_unique} /\n")
        f.write(f"# Link totali: {total_links} (max {args.max_per_page} per pagina,\n")
        f.write(f"# soglia score >= {args.min_score}).\n\n")
        yaml.safe_dump({"canali": canali, "pagine": results},
                       f, allow_unicode=True, sort_keys=True, width=120)
    print(f"\n✓ Scritto {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
