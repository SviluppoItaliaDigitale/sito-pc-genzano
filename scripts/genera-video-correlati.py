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
    r"^/?english/", r"^/?francais/", r"^/?deutsch/", r"^/?espanol/",
    r"^/?portugues/", r"^/?romana/", r"^/?esperanto/",  # traduzioni
    r"^/?formazione/?$",  # hub formazione (ne ha già molti link nei kit)
    # Articoli senza video pertinenti nei canali monitorati: il cross-match
    # produce solo falsi positivi (parole generiche o omonimie). Escludi per
    # non mostrare "Approfondimenti video" fuori tema (rule: niente sezione
    # video se non ci sono video davvero pertinenti).
    #  - sciami d'api: "sciami" agganciava video INGV su SCIAMI SISMICI,
    #    "bisogno"/"nostra" agganciavano video su nucleare/demografia (20/05/2026).
    r"^/?comunicazioni/2026-05-20-sciami-api-estate-recupero-genzano/?$",
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
