#!/usr/bin/env python3
"""Controllo della sezione «Cucina in emergenza» (/cucina-emergenza/): dati e collegamenti ai PDF ufficiali.

Regola della sezione (Alessandro, 24/11/2026): solo collegamenti, verificati, a file PDF pubblicati sui siti
di enti governativi e istituzionali. Lo script la fa rispettare in due modi.

  python3 scripts/check-cucina-emergenza.py [--public public] [--eta GIORNI]
      Senza rete: forma dei dati, solo siti dell'elenco ENTI, solo PDF, nessun doppione. Con --public anche
      le pagine costruite: contengono proprio i collegamenti dei dati, nessun file Word o Excel e nessun PDF
      fuori dai dati. Bloccante sulle pull request (validate-pr.yml). Con --eta è un errore anche una data
      «verificato» più vecchia di GIORNI giorni: lo usa l'audit del sito (audit-sito.yml, sezione 51), perché
      un giro mensile saltato non lascia nessun run rosso.

  python3 scripts/check-cucina-emergenza.py --rete [--file] [--browser] [--rapporto FILE] [--aggiorna-data]
      Con richieste vere e poche per volta: il sito del Ministero dell'agricoltura risponde 502 se lo si
      interroga con molte richieste insieme (per questo il catalogo è fuori dal controllo generale dei link,
      lychee) e ha periodi in cui impiega 30-40 secondi a risposta (per questo i tempi massimi sono lunghi).
      - Documenti: ogni indirizzo risponde ed è un PDF. Per EUR-Lex, che alle richieste automatiche risponde
        202 senza contenuto, si controlla che il documento esista nell'archivio dell'Ufficio delle
        pubblicazioni dell'UE; per i testi consolidati, che non ne sia uscito uno più recente; per i
        regolamenti collegati nel testo della Gazzetta ufficiale, che nel frattempo non siano stati modificati.
      - Catalogo: ogni disciplinare è ancora fra gli allegati della sua pagina del Ministero; gli allegati
        nuovi e un elenco ufficiale cambiato si segnalano come novità.
      - --file: chiede anche l'inizio di ogni PDF del catalogo, tre alla volta.
      - --browser: ciò che una richiesta semplice non legge si riprova con Chromium (Playwright), se c'è.
        Se Playwright manca o Chromium non parte, il controllo prosegue senza e il rapporto lo dice.
      - Verifiche anti-bot: se un sito risponde con una pagina di verifica o rifiuta la richiesta (403, 429),
        il collegamento non è rotto e non è controllato. Non si aggira: si dichiara nel rapporto, e la data
        di verifica non si aggiorna. Il sito del Ministero della Salute lo fa a tratti (24/11/2026).
      - --aggiorna-data (con --file): se tutto è stato letto e nulla è rotto, scrive la data di oggi in
        «verificato» dei due file di dati. Ogni mese: .github/workflows/controllo-cucina-emergenza.yml.

Uscita: 0 tutto a posto; 1 collegamenti rotti o dati sbagliati; 2 una fonte non si è fatta leggere (regola
guasti: un controllo che non legge la sua fonte non chiude in verde); 3 solo novità da valutare o
collegamenti dietro una verifica anti-bot (regola guasti, punto 3: non sono guasti, ma si dichiarano).
Dati: data/cucina_emergenza.yaml, data/disciplinari.json.
"""
import argparse
import hashlib
import html
import json
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
FILE_DOCUMENTI = RADICE / "data" / "cucina_emergenza.yaml"
FILE_CATALOGO = RADICE / "data" / "disciplinari.json"

# Siti ammessi: enti governativi e istituzionali. Un sito nuovo si aggiunge qui solo se è di un ente pubblico
# (ministero, regione, azienda sanitaria, agenzia o istituto pubblico, Unione europea), mai di terzi.
ENTI = {
    "www.masaf.gov.it": "Ministero dell'agricoltura, della sovranità alimentare e delle foreste",
    "www.salute.gov.it": "Ministero della Salute",
    "eur-lex.europa.eu": "Unione europea, EUR-Lex",
    "regione.lazio.it": "Regione Lazio",
    "salute.regione.emilia-romagna.it": "Regione Emilia-Romagna",
    "www.izs.it": "Istituto Zooprofilattico Sperimentale dell'Abruzzo e del Molise",
    "www.crea.gov.it": "CREA, Consiglio per la ricerca in agricoltura e l'analisi dell'economia agraria",
    "www.arsial.it": "ARSIAL, agenzia della Regione Lazio",
}
MASAF = "www.masaf.gov.it"
EURLEX = "eur-lex.europa.eu"
SITO = "www.protezionecivilegenzano.it"
PAGINA_MASAF = "https://www.masaf.gov.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/{}"
PAGINA_MODIFICHE = "8079"  # «Disciplinari in modifica temporanea»
RE_ALLEGATO = re.compile(r"""<a\s+title='([^']*)'\s+href="([^"]*ServeAttachment[^"]*)"[^>]*>""")
# Archivio dell'Ufficio delle pubblicazioni dell'UE: dice se un numero CELEX esiste (303) o no (404).
ARCHIVIO_UE = "https://publications.europa.eu/resource/celex/{}"
SPARQL_UE = "https://publications.europa.eu/webapi/rdf/sparql"
AGENTE = "Mozilla/5.0 (compatible; PCGenzanoLinkChecker/1.0; +https://www.protezionecivilegenzano.it/)"
TIPI = {"DOP", "IGP", "STG"}
PAUSA = 0.7            # secondi fra due richieste allo stesso sito
TEMPO_MASSIMO = 90     # secondi per una risposta: nei periodi lenti il sito del Ministero ne impiega 30-40
CONTEMPORANEE = 3      # richieste insieme per i PDF del catalogo: di più, il sito del Ministero risponde 502
SOGLIA_FERMO = 5       # richieste di fila senza risposta utile dopo le quali un sito non si interroga più
MASSIMO_BROWSER = 80   # collegamenti che si riprovano con il browser in un giro
TEMPO_RICHIESTE = 35 * 60  # secondi in tutto per le richieste dirette: oltre, ciò che resta è «non controllato»
TEMPO_BROWSER = 12 * 60    # secondi in tutto per il ripiego con il browser
FUORI_TEMPO = "non controllato: il tempo del controllo è finito prima (sito troppo lento)"
BLOCCO = re.compile(r"captcha|verify you are|are you a robot|just a moment|checking your browser|access denied|"
                    r"attention required|unusual traffic|sei un robot|enable javascript and cookies|"
                    r"browser validation|validation is complete|security service (?:to protect|for protection)", re.I)
ANTIBOT = "il sito ha risposto con una pagina di verifica anti-bot"
RIFIUTO = "il sito ha rifiutato la richiesta automatica"
PROTETTO = (ANTIBOT, RIFIUTO)  # esiti che non dicono nulla sul collegamento: né rotto né controllato

errori = []       # dati sbagliati o collegamenti rotti (uscita 1)
non_letti = []    # (sito, testo): fonti che non si sono fatte leggere (uscita 2)
novita = []       # cose nuove sulle fonti, da valutare: non sono guasti (uscita 3)
protetti = []     # collegamenti dietro una verifica anti-bot: non controllati in questo giro (uscita 3)
da_rivedere = []  # (dove, url, nota): PDF che la richiesta semplice non ha letto, da riprovare con il browser
senza_browser = []  # perché il ripiego con il browser, se chiesto, non è stato possibile
metodi = Counter()


def oggi_in_italia():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Europe/Rome")).date()
    except Exception:  # macchina senza i dati dei fusi orari
        return datetime.now().date()


def controlla_eta(documenti, catalogo, giorni):
    """L'ultimo controllo completo dei collegamenti non è più vecchio di `giorni`: lo usa l'audit del sito, perché
    un giro mensile saltato, o fermo per una verifica anti-bot, non lascia nessun run rosso."""
    for nome, dati in (("cucina_emergenza.yaml", documenti), ("disciplinari.json", catalogo)):
        try:
            fatta = date.fromisoformat(str(dati.get("verificato", "")))
        except ValueError:
            continue  # il formato sbagliato lo segnala già controlla_dati
        eta = (oggi_in_italia() - fatta).days
        if eta > giorni:
            errori.append(f"{nome}: l'ultimo controllo completo dei collegamenti è del {fatta:%d/%m/%Y}, {eta} giorni fa "
                          f"(soglia {giorni}): rilanciare «Cucina in emergenza: controllo mensile dei collegamenti» e, "
                          f"se resta una verifica anti-bot, aprire quei collegamenti con un browser")


def carica():
    try:
        import yaml
    except ImportError:
        sys.exit("Serve PyYAML: pip install pyyaml")
    documenti = yaml.safe_load(FILE_DOCUMENTI.read_text(encoding="utf-8"))
    catalogo = json.loads(FILE_CATALOGO.read_text(encoding="utf-8"))
    return documenti, catalogo


def sito(url):
    return urllib.parse.urlsplit(url or "").netloc.lower()


def pagina_di(url):
    """Numero della pagina del Ministero che pubblica l'allegato: sta nell'indirizzo dell'allegato."""
    m = re.search(r"BLOB%3AID%3D(\d+)", url or "")
    return m.group(1) if m else None


def celex_di(url):
    m = re.search(r"[?&]uri=CELEX:([^&#]+)", url or "")
    return urllib.parse.unquote(m.group(1)) if m else None


def tutti_i_documenti(documenti):
    return [doc for gruppo in documenti.get("gruppi", []) for doc in gruppo.get("documenti", [])]


# ───────────────────────── controllo dei dati, senza rete ─────────────────────────

def controlla_url(dove, url, deve_essere_pdf=True):
    if not isinstance(url, str) or not url.startswith("https://"):
        errori.append(f"{dove}: indirizzo non https: {url!r}")
        return
    if sito(url) not in ENTI:
        errori.append(f"{dove}: il sito «{sito(url)}» non è fra gli enti ammessi (elenco ENTI dello script)")
    if re.search(r"[\s<>\"']", url):
        errori.append(f"{dove}: l'indirizzo contiene spazi o caratteri non ammessi")
    if "(" in url or ")" in url:
        errori.append(f"{dove}: parentesi nell'indirizzo: vanno scritte %28 e %29, come le pubblica la pagina")
    if not deve_essere_pdf:
        return
    if sito(url) == MASAF:
        if not re.search(r"/E/pdf(\?mode=download)?$", url):
            errori.append(f"{dove}: l'allegato del Ministero non è un PDF")
    elif sito(url) == EURLEX:
        if "/TXT/PDF/" not in url or not celex_di(url):
            errori.append(f"{dove}: l'indirizzo di EUR-Lex deve essere quello del PDF (…/TXT/PDF/?uri=CELEX:…)")
    elif not urllib.parse.urlsplit(url).path.lower().endswith(".pdf"):
        errori.append(f"{dove}: l'indirizzo non finisce con .pdf")


def controlla_dati(documenti, catalogo):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(documenti.get("verificato", ""))):
        errori.append("cucina_emergenza.yaml: «verificato» deve essere una data AAAA-MM-GG")
    for nome, dati in (("cucina_emergenza.yaml", documenti), ("disciplinari.json", catalogo)):
        try:
            if date.fromisoformat(str(dati.get("verificato", ""))) > oggi_in_italia():
                errori.append(f"{nome}: «verificato» è una data futura")
        except ValueError:
            pass  # il formato sbagliato è segnalato qui sopra e più sotto
    visti, indirizzi = set(), set()
    for gruppo in documenti.get("gruppi", []):
        for campo in ("id", "titolo", "documenti"):
            if not gruppo.get(campo):
                errori.append(f"cucina_emergenza.yaml: gruppo senza «{campo}»: {gruppo.get('id')}")
        for doc in gruppo.get("documenti", []):
            dove = f"documento «{doc.get('id')}»"
            for campo in ("id", "titolo", "ente", "url", "pagine", "kb", "testo"):
                if doc.get(campo) in (None, ""):
                    errori.append(f"{dove}: manca «{campo}»")
            if doc.get("id") in visti:
                errori.append(f"{dove}: identificativo ripetuto")
            visti.add(doc.get("id"))
            if doc.get("url") in indirizzi:
                errori.append(f"{dove}: indirizzo già usato da un altro documento")
            indirizzi.add(doc.get("url"))
            controlla_url(dove, doc.get("url"))
            for campo in ("pagine", "kb"):
                if not isinstance(doc.get(campo), int) or doc.get(campo, 0) <= 0:
                    errori.append(f"{dove}: «{campo}» deve essere un numero intero maggiore di zero")
            if doc.get("pagina"):
                controlla_url(dove + ", pagina dell'ente", doc["pagina"].get("url"), deve_essere_pdf=False)
                if not doc["pagina"].get("testo"):
                    errori.append(f"{dove}: la pagina dell'ente non ha il testo del collegamento")
            if bool(doc.get("scarica")) != (sito(doc.get("url")) == MASAF):
                errori.append(f"{dove}: «scarica: true» va messo solo, e sempre, sui file del Ministero dell'agricoltura")

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(catalogo.get("verificato", ""))):
        errori.append("disciplinari.json: «verificato» deve essere una data AAAA-MM-GG")
    elenco = catalogo.get("elenco_ufficiale") or {}
    controlla_url("elenco ufficiale del Ministero", elenco.get("url"), deve_essere_pdf=False)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(elenco.get("aggiornato", ""))) or sito(elenco.get("allegato")) != MASAF:
        errori.append("disciplinari.json: «elenco_ufficiale» chiede url, allegato e la data «aggiornato»")
    classi = {c["id"]: c for c in catalogo.get("classi", [])}
    in_gruppo = [c for g in catalogo.get("gruppi", []) for c in g.get("classi", [])]
    if sorted(in_gruppo) != sorted(classi):
        errori.append("disciplinari.json: ogni classe deve stare in un gruppo, una volta sola")
    for c in classi.values():
        controlla_url(f"classe «{c['id']}»", c.get("pagina"), deve_essere_pdf=False)
    nomi, usati = set(), set()
    for voce in catalogo.get("voci", []):
        dove = f"disciplinare «{voce.get('nome')}»"
        if (voce.get("nome"), voce.get("tipo")) in nomi:
            errori.append(f"{dove}: voce ripetuta")
        nomi.add((voce.get("nome"), voce.get("tipo")))
        if voce.get("tipo") not in TIPI:
            errori.append(f"{dove}: tipo «{voce.get('tipo')}» sconosciuto")
        if voce.get("classe") not in classi:
            errori.append(f"{dove}: classe «{voce.get('classe')}» sconosciuta")
            continue
        if not isinstance(voce.get("regioni"), list) or (voce.get("tipo") != "STG" and not voce.get("regioni")):
            errori.append(f"{dove}: manca la regione")
        formato = voce.get("formato")
        della_classe = classi[voce["classe"]]["pagina"].rsplit("/", 1)[1]
        if formato == "pdf":
            controlla_url(dove, voce.get("url"))
            if not all(isinstance(voce.get(k), int) and voce.get(k) > 0 for k in ("pagine", "kb")):
                errori.append(f"{dove}: mancano pagine o peso del PDF")
            if pagina_di(voce.get("url")) != della_classe:
                errori.append(f"{dove}: l'allegato non è della pagina del Ministero della sua classe")
        elif formato == "docx":
            if not re.search(r"/E/docx(\?mode=download)?$", voce.get("url") or "") or pagina_di(voce.get("url")) != della_classe:
                errori.append(f"{dove}: formato «docx» ma l'indirizzo non è un file Word della pagina della sua classe")
        elif formato == "":
            if voce.get("url"):
                errori.append(f"{dove}: senza formato ma con un indirizzo")
        else:
            errori.append(f"{dove}: formato «{formato}» sconosciuto (pdf, docx o vuoto)")
        if voce.get("url"):
            if voce["url"] in usati:
                errori.append(f"{dove}: indirizzo già usato da un'altra voce")
            usati.add(voce["url"])
        for extra in voce.get("extra", []):
            controlla_url(dove + ", " + str(extra.get("etichetta")), extra.get("url"))
            if not extra.get("etichetta") or not isinstance(extra.get("kb"), int):
                errori.append(f"{dove}: documento aggiuntivo senza etichetta o peso")
    for noto in catalogo.get("allegati_noti", []):
        if sito(noto.get("url")) != MASAF or not noto.get("motivo"):
            errori.append("disciplinari.json: «allegati_noti» chiede, per ogni voce, l'indirizzo dell'allegato e il motivo")


# ───────────────────────── pagine costruite ─────────────────────────

def collegamenti(percorso):
    testo = percorso.read_text(encoding="utf-8")
    trovati = set()
    for doppi, singoli, nudi in re.findall(r"""\shref=(?:"([^"]*)"|'([^']*)'|([^\s>]+))""", testo):
        trovati.add(html.unescape(doppi or singoli or nudi))
    return trovati


def controlla_pagine(cartella, documenti, catalogo):
    base = Path(cartella) / "cucina-emergenza"
    hub, cat = base / "index.html", base / "disciplinari" / "index.html"
    for p in (hub, cat):
        if not p.exists():
            errori.append(f"pagina non costruita: {p}")
            return
    nel_hub, nel_cat = collegamenti(hub), collegamenti(cat)
    nei_dati = set()
    for doc in tutti_i_documenti(documenti):
        nei_dati.add(doc["url"])
        if doc["url"] not in nel_hub | nel_cat:
            errori.append(f"documento «{doc['id']}»: il collegamento non compare nelle pagine costruite")
    for voce in catalogo["voci"]:
        if voce["formato"] == "pdf":
            nei_dati.add(voce["url"])
            if voce["url"] not in nel_cat:
                errori.append(f"disciplinare «{voce['nome']}»: il collegamento non compare nel catalogo costruito")
        for extra in voce.get("extra", []):
            nei_dati.add(extra["url"])
            if extra["url"] not in nel_cat:
                errori.append(f"disciplinare «{voce['nome']}»: manca il collegamento a «{extra['etichetta']}»")
    for url in sorted(nel_hub | nel_cat):
        if not url.startswith("http") or sito(url) == SITO:
            continue
        percorso = urllib.parse.urlsplit(url).path
        if re.search(r"\.(docx?|xlsx?|pptx?|odt|ods|zip|rar)$", percorso, re.I) or re.search(r"/E/(docx?|xlsx?|zip)$", percorso):
            errori.append(f"le pagine collegano un file che non è un PDF: {url}")
        elif (percorso.lower().endswith(".pdf") or "/TXT/PDF/" in url or percorso.endswith("/E/pdf")) and url not in nei_dati:
            errori.append(f"le pagine collegano un PDF che non è nei dati, e quindi nessuno lo ricontrolla: {url}")


# ───────────────────────── richieste vere ─────────────────────────

class NonSeguire(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *argomenti, **parole):
        return None


SENZA_RINVII = urllib.request.build_opener(NonSeguire)
ultimo = {}    # sito → istante dell'ultima richiesta
di_fila = {}   # sito → richieste di fila senza una risposta utile
motivo = {}    # sito → che cosa è successo all'ultima richiesta non utile
scadenza = float("inf")  # istante oltre il quale non si fanno più richieste dirette (lo fissa main)


def chiedi(url, intervallo=None, quanto=None, intestazioni=None, segui=True, tentativi=3):
    """Una richiesta GET educata: pausa fra due richieste allo stesso sito, nuovi tentativi con attese
    crescenti. Restituisce (stato, contenuto, errore); stato 0 se non è arrivata nessuna risposta utile."""
    host = sito(url)
    errore = ""
    for n in range(tentativi):
        if time.time() > scadenza:
            return 0, b"", errore or FUORI_TEMPO
        attesa = PAUSA - (time.time() - ultimo.get(host, 0))
        if attesa > 0:
            time.sleep(attesa)
        campi = {"User-Agent": AGENTE, "Accept": "application/pdf,text/html;q=0.9,*/*;q=0.8",
                 "Accept-Language": "it-IT,it;q=0.9"}
        if intervallo:
            campi["Range"] = intervallo
        campi.update(intestazioni or {})
        try:
            richiesta = urllib.request.Request(url, headers=campi)
            apri = urllib.request.urlopen if segui else SENZA_RINVII.open
            with apri(richiesta, timeout=TEMPO_MASSIMO) as risposta:
                corpo = risposta.read(quanto) if quanto else risposta.read()
                ultimo[host] = time.time()
                return risposta.status, corpo, ""
        except urllib.error.HTTPError as e:
            ultimo[host] = time.time()
            if e.code in (404, 410) or 300 <= e.code < 400:
                return e.code, b"", ""
            errore = f"HTTP {e.code}"
            if e.code in (403, 429):  # il sito rifiuta la richiesta automatica: non si insiste
                return 0, b"", errore
        except Exception as e:  # rete, tempo scaduto, connessione chiusa, certificato
            ultimo[host] = time.time()
            errore = f"{type(e).__name__}: {e}"
        if n < tentativi - 1:
            time.sleep(8 * (n + 1))
    return 0, b"", errore


def segna(host, utile, nota=""):
    di_fila[host] = 0 if utile else di_fila.get(host, 0) + 1
    if not utile:
        motivo[host] = nota


def sembra_verifica(corpo):
    """Vero se il contenuto è una pagina di verifica anti-bot: si guarda il testo, non script e stili."""
    testo = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", corpo.decode("utf-8", "replace"))
    return bool(BLOCCO.search(re.sub(r"<[^>]+>", " ", testo)))


def leggi_pdf(url):
    """('pdf', '') se all'indirizzo c'è un PDF, ('assente', …) con 404 o 410, ('protetto', …) se il sito risponde
    con una pagina di verifica anti-bot o rifiuta la richiesta (403, 429), altrimenti che cosa è successo."""
    stato, inizio, errore = chiedi(url, intervallo="bytes=0-7", quanto=8)
    if stato in (200, 206) and not inizio.startswith(b"%PDF"):
        # qualche sito, a una richiesta parziale, risponde con una pagina: si richiede il file intero
        stato, inizio, errore = chiedi(url, quanto=32768)
    if stato in (404, 410):
        return "assente", f"HTTP {stato}"
    if stato in (200, 206) and inizio.startswith(b"%PDF"):
        return "pdf", ""
    if stato in (200, 206):
        return ("protetto", ANTIBOT) if sembra_verifica(inizio) else ("altro", "risponde, ma non con un PDF")
    if errore in ("HTTP 403", "HTTP 429"):
        return "protetto", f"{RIFIUTO} ({errore})"
    return "muto", errore or f"HTTP {stato}"


def controlla_pdf(dove, url):
    host = sito(url)
    if di_fila.get(host, 0) >= SOGLIA_FERMO:
        perche = motivo.get(host, "")
        da_rivedere.append((dove, url, perche if perche.startswith(PROTETTO) else
                            "non controllato: il sito non rispondeva alle richieste precedenti"))
        return
    esito, nota = leggi_pdf(url)
    segna(host, esito in ("pdf", "assente"), nota)
    if esito == "pdf":
        metodi["richiesta diretta"] += 1
    elif esito == "assente":
        errori.append(f"{dove}: {nota}: {url}")
    else:
        da_rivedere.append((dove, url, nota))


def ultima_consolidata(celex):
    """Numero CELEX dell'ultima versione consolidata dell'atto, chiesto all'archivio dell'UE; None se non risponde."""
    base, prefisso = "3" + celex.split("-")[0][1:], celex.split("-")[0] + "-"
    domanda = ("PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> SELECT DISTINCT ?celex WHERE { "
               f'?base cdm:resource_legal_id_celex "{base}"^^<http://www.w3.org/2001/XMLSchema#string> . '
               "?cons cdm:act_consolidated_consolidates_resource_legal ?base ; cdm:resource_legal_id_celex ?celex . }")
    stato, corpo, _ = chiedi(SPARQL_UE + "?" + urllib.parse.urlencode({"query": domanda}),
                             intestazioni={"Accept": "application/sparql-results+json"})
    if stato != 200:
        return None
    try:
        valori = [r["celex"]["value"] for r in json.loads(corpo)["results"]["bindings"]]
    except (ValueError, KeyError, TypeError):
        return None
    versioni = sorted(v for v in valori if v.startswith(prefisso))
    return versioni[-1] if versioni else None


def modifiche(celex):
    """Atti che hanno modificato un atto di base (numeri CELEX, senza le rettifiche), chiesti all'archivio dell'UE;
    None se non risponde. Un atto modificato ha un testo consolidato: è quello che conviene collegare."""
    domanda = ("PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> SELECT DISTINCT ?celex WHERE { "
               f'?base cdm:resource_legal_id_celex "{celex}"^^<http://www.w3.org/2001/XMLSchema#string> . '
               "?mod cdm:resource_legal_amends_resource_legal ?base ; cdm:resource_legal_id_celex ?celex . }")
    stato, corpo, _ = chiedi(SPARQL_UE + "?" + urllib.parse.urlencode({"query": domanda}),
                             intestazioni={"Accept": "application/sparql-results+json"})
    if stato != 200:
        return None
    try:
        valori = [r["celex"]["value"] for r in json.loads(corpo)["results"]["bindings"]]
    except (ValueError, KeyError, TypeError):
        return None
    return sorted(v for v in valori if "R(" not in v)


def controlla_ue(dove, url):
    """EUR-Lex risponde 202 senza contenuto alle richieste automatiche, per un documento vero come per uno
    inesistente: l'esistenza si chiede all'archivio dell'Ufficio delle pubblicazioni dell'UE."""
    celex = celex_di(url)
    stato, _, errore = chiedi(ARCHIVIO_UE.format(urllib.parse.quote(celex, safe="")), quanto=8, segui=False,
                              intestazioni={"Accept": "*/*", "Accept-Language": "it"})
    if stato == 404:
        errori.append(f"{dove}: il documento CELEX {celex} non esiste nell'archivio dell'Unione europea: {url}")
        return
    if stato not in (200, 303):
        non_letti.append(("publications.europa.eu", f"{dove}: l'archivio dell'UE non ha risposto per CELEX {celex} ({errore or 'HTTP ' + str(stato)})"))
        return
    if re.fullmatch(r"0\d{4}[A-Z]{1,2}\d{4}-\d{8}", celex):
        ultima = ultima_consolidata(celex)
        if ultima is None:
            non_letti.append(("publications.europa.eu", f"{dove}: l'archivio dell'UE non ha detto qual è l'ultima versione consolidata di {celex}"))
        elif ultima > celex:
            novita.append(f"{dove}: è uscita una versione consolidata più recente ({ultima}; il sito collega {celex})")
    elif re.fullmatch(r"3\d{4}[RLD]\d{4}", celex):
        # atto collegato nel testo della Gazzetta ufficiale: se nel frattempo è stato modificato, lo si dice
        cambiato_da = modifiche(celex)
        if cambiato_da is None:
            non_letti.append(("publications.europa.eu", f"{dove}: l'archivio dell'UE non ha detto se {celex} è stato modificato"))
        elif cambiato_da:
            novita.append(f"{dove}: l'atto {celex} è stato modificato da {', '.join(cambiato_da)}: va collegato il testo "
                          f"consolidato più recente al posto di quello della Gazzetta ufficiale")
    stato, inizio, errore = chiedi(url, quanto=8)
    if stato in (404, 410):
        errori.append(f"{dove}: HTTP {stato}: {url}")
    elif stato == 200 and inizio.startswith(b"%PDF"):
        metodi["richiesta diretta"] += 1
    elif stato in (200, 202):
        da_rivedere.append((dove, url, "EUR-Lex"))
    else:
        non_letti.append((EURLEX, f"{dove}: {errore or 'HTTP ' + str(stato)}: {url}"))


def allegati_della_pagina(numero):
    """Allegati pubblicati da una pagina del Ministero: {indirizzo: titolo}; None se la pagina non si legge."""
    if di_fila.get(MASAF, 0) >= SOGLIA_FERMO:
        non_letti.append((MASAF, f"pagina {numero} del Ministero: non controllata, il sito non rispondeva"))
        return None
    stato, corpo, errore = chiedi(PAGINA_MASAF.format(numero))
    segna(MASAF, stato == 200)
    if stato != 200:
        non_letti.append((MASAF, f"pagina {numero} del Ministero: {errore or 'HTTP ' + str(stato)}"))
        return None
    testo = corpo.decode("latin-1")
    return {html.unescape(m.group(2)): html.unescape(m.group(1)).strip() for m in RE_ALLEGATO.finditer(testo)}


def controlla_ministero(documenti, catalogo):
    """Ogni file del Ministero che il sito collega è ancora fra gli allegati della sua pagina."""
    attesi = {}
    for voce in catalogo["voci"]:
        if voce["url"]:
            attesi.setdefault(pagina_di(voce["url"]), []).append((f"disciplinare «{voce['nome']}»", voce["url"]))
        for extra in voce.get("extra", []):
            attesi.setdefault(pagina_di(extra["url"]), []).append(
                (f"disciplinare «{voce['nome']}», {extra['etichetta']}", extra["url"]))
    for doc in tutti_i_documenti(documenti):
        if sito(doc["url"]) == MASAF:
            attesi.setdefault(pagina_di(doc["url"]), []).append((f"documento «{doc['id']}»", doc["url"]))
    elenco = catalogo["elenco_ufficiale"]
    attesi.setdefault(pagina_di(elenco["allegato"]), [])
    noti = {n["url"] for n in catalogo.get("allegati_noti", [])}
    del_catalogo = {c["pagina"].rsplit("/", 1)[1] for c in catalogo["classi"]} | {PAGINA_MODIFICHE}
    for numero in sorted(attesi, key=int):
        trovati = allegati_della_pagina(numero)
        if trovati is None:
            continue
        indirizzo = PAGINA_MASAF.format(numero)
        mancanti = [(dove, url) for dove, url in attesi[numero] if url not in trovati]
        if not trovati or (len(attesi[numero]) >= 4 and len(mancanti) * 2 > len(attesi[numero])):
            # una pagina senza allegati, o senza più della metà di quelli attesi, è stata letta male o è
            # stata riorganizzata: non si dichiarano rotti tutti i suoi collegamenti, si dichiara la fonte
            non_letti.append((MASAF, f"pagina {indirizzo}: mancano {len(mancanti)} allegati su {len(attesi[numero])} "
                                     f"(pagina letta male o riorganizzata)"))
            continue
        for dove, url in mancanti:
            errori.append(f"{dove}: il file non è più fra gli allegati di {indirizzo} (il Ministero può averlo sostituito)")
        if numero == pagina_di(elenco["allegato"]) and elenco["allegato"] not in trovati:
            novita.append(f"il Ministero ha cambiato l'elenco dei prodotti DOP e IGP ({indirizzo}): va confrontato "
                          f"con il catalogo, che segue quello aggiornato al {elenco['aggiornato']}")
        if numero in del_catalogo:
            usati = {url for _, url in attesi[numero]}
            for url, titolo in trovati.items():
                if url not in usati and url not in noti:
                    novita.append(f"allegato nuovo «{titolo}» in {indirizzo}: {url}")


def controlla_rete(documenti, catalogo, anche_file):
    for doc in tutti_i_documenti(documenti):
        dove = f"documento «{doc['id']}»"
        if sito(doc["url"]) == EURLEX:
            controlla_ue(dove, doc["url"])
        else:
            controlla_pdf(dove, doc["url"])
        if doc.get("pagina") and sito(doc["pagina"]["url"]) != MASAF:  # le pagine del Ministero si leggono dopo
            stato, inizio, errore = chiedi(doc["pagina"]["url"], quanto=32768)
            if stato in (404, 410):
                errori.append(f"{dove}, pagina dell'ente: HTTP {stato}: {doc['pagina']['url']}")
            elif stato == 200 and sembra_verifica(inizio):
                protetti.append(f"{dove}, pagina dell'ente: {ANTIBOT}: {doc['pagina']['url']}")
            elif errore in ("HTTP 403", "HTTP 429"):
                protetti.append(f"{dove}, pagina dell'ente: {RIFIUTO} ({errore}): {doc['pagina']['url']}")
            elif stato != 200:
                non_letti.append((sito(doc["pagina"]["url"]), f"{dove}, pagina dell'ente: {errore or 'HTTP ' + str(stato)}"))
    controlla_ministero(documenti, catalogo)
    if anche_file:
        controlla_file_del_catalogo(catalogo)


def controlla_file_del_catalogo(catalogo):
    """Chiede l'inizio di ogni PDF del catalogo, CONTEMPORANEE alla volta. Dopo SOGLIA_FERMO file di fila senza
    risposta utile si ferma: gli altri restano «non controllati» e il rapporto lo dice."""
    voci = []
    for voce in catalogo["voci"]:
        if voce["formato"] == "pdf":
            voci.append((f"disciplinare «{voce['nome']}»", voce["url"]))
        for extra in voce.get("extra", []):
            voci.append((f"disciplinare «{voce['nome']}», {extra['etichetta']}", extra["url"]))
    fermo = threading.Event()
    perche = []  # motivo dell'ultima lettura non riuscita: lo scrive solo il ciclo qui sotto

    def uno(voce):
        if time.time() > scadenza:
            return "saltato", FUORI_TEMPO
        if fermo.is_set():
            ultimo_motivo = perche[-1] if perche else ""
            return "saltato", (ultimo_motivo if ultimo_motivo.startswith(PROTETTO) else
                               "non controllato: il sito non rispondeva alle richieste precedenti")
        return leggi_pdf(voce[1])

    muti = 0
    with ThreadPoolExecutor(max_workers=CONTEMPORANEE) as squadra:
        for (dove, url), (esito, nota) in zip(voci, squadra.map(uno, voci)):
            if esito == "pdf":
                metodi["richiesta diretta"] += 1
                muti = 0
            elif esito == "assente":
                errori.append(f"{dove}: {nota}: {url}")
                muti = 0
            else:
                da_rivedere.append((dove, url, nota))
                if esito != "saltato":
                    muti += 1
                    perche.append(nota)
                if muti >= SOGLIA_FERMO:
                    fermo.set()


def riprova_con_browser(voci):
    """Riprova con Chromium i PDF che la richiesta semplice non ha letto. Restituisce {indirizzo: (esito, nota)}
    oppure None se il browser non è disponibile: Playwright non installato, oppure Chromium o le sue librerie
    che non partono (il motivo va in «senza_browser»). In quel caso il controllo prosegue con ciò che ha già
    letto e scrive il rapporto. Una verifica anti-bot non si aggira: si dichiara."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        senza_browser.append("Playwright non è installato")
        return None
    esiti, falliti = {}, Counter()
    fine = time.time() + TEMPO_BROWSER
    try:
        gestore = sync_playwright().start()
    except Exception as e:
        senza_browser.append(f"Playwright non parte ({type(e).__name__})")
        return None
    try:
        try:
            browser = gestore.chromium.launch()
            contesto = browser.new_context(locale="it-IT", viewport={"width": 1366, "height": 900})
        except Exception as e:
            motivo_breve = (str(e).strip().splitlines() or [""])[0][:120]
            senza_browser.append(f"Chromium non parte ({type(e).__name__}: {motivo_breve})")
            return None
        for _, url, _ in voci:
            if time.time() > fine:
                break
            if falliti[sito(url)] >= 3:  # il sito non risponde nemmeno al browser: inutile insistere
                continue
            try:
                risposta = contesto.request.get(url, timeout=30000)
                if risposta.status in (404, 410):
                    esiti[url] = ("assente", f"HTTP {risposta.status}")
                    continue
                if not (risposta.ok and risposta.body()[:4] == b"%PDF"):
                    # il sito vuole prima una visita vera: si apre l'indirizzo e si richiede il file
                    pagina = contesto.new_page()
                    nota = ""
                    try:
                        try:
                            pagina.goto(url, wait_until="domcontentloaded", timeout=30000)
                        except Exception as e:  # un PDF fa partire lo scaricamento e interrompe la navigazione
                            if "Download is starting" not in str(e):
                                nota = type(e).__name__
                        # una validazione automatica del browser chiede qualche secondo: le si lascia il tempo
                        for _ in range(4):
                            pagina.wait_for_timeout(5000)
                            risposta = contesto.request.get(url, timeout=30000)
                            letto = risposta.ok and risposta.body()[:4] == b"%PDF"
                            if letto or risposta.status in (404, 410) or time.time() > fine:
                                break
                        if not letto and risposta.status not in (404, 410):
                            try:
                                if BLOCCO.search(pagina.title()) or BLOCCO.search(pagina.inner_text("body")[:3000]):
                                    nota = ANTIBOT
                            except Exception:  # la pagina può essersi chiusa per uno scaricamento
                                pass
                    finally:
                        pagina.close()
                    if risposta.status in (404, 410):
                        esiti[url] = ("assente", f"HTTP {risposta.status}")
                        continue
                    if not (risposta.ok and risposta.body()[:4] == b"%PDF"):
                        if not nota and risposta.status in (403, 429):
                            nota = f"{RIFIUTO} (HTTP {risposta.status})"
                        if not nota and sembra_verifica(risposta.body()[:32768]):
                            nota = ANTIBOT
                        esiti[url] = ("no", nota or f"anche il browser non ottiene un PDF (HTTP {risposta.status})")
                        falliti[sito(url)] += 1
                        continue
                esiti[url] = ("pdf", "")
                falliti[sito(url)] = 0
            except Exception as e:
                esiti[url] = ("no", f"{type(e).__name__}: {str(e)[:120]}")
                falliti[sito(url)] += 1
            time.sleep(PAUSA)
        try:
            browser.close()
        except Exception:  # un browser caduto a metà non cancella gli esiti già raccolti
            pass
    finally:
        try:
            gestore.stop()
        except Exception:
            pass
    return esiti


def chiudi_da_rivedere(con_browser):
    """Decide la sorte dei PDF non letti con la richiesta semplice."""
    if not da_rivedere:
        return
    in_fila = [v for v in da_rivedere if v[2] != "EUR-Lex"] + [v for v in da_rivedere if v[2] == "EUR-Lex"]
    esiti = riprova_con_browser(in_fila[:MASSIMO_BROWSER]) if con_browser else None
    if con_browser and esiti is None:
        print(f"Avviso: --browser chiesto, ma il browser non è disponibile ({'; '.join(senza_browser)}): "
              "si prosegue senza.", file=sys.stderr)
    for dove, url, nota in da_rivedere:
        esito, nota_browser = (esiti or {}).get(url, ("", ""))
        if esito == "pdf":
            metodi["browser"] += 1
        elif esito == "assente":
            errori.append(f"{dove}: {nota_browser}: {url}")
        elif nota == "EUR-Lex":
            # il documento esiste nell'archivio dell'UE e l'indirizzo di EUR-Lex risponde: di più una
            # richiesta automatica non ottiene
            metodi["archivio dell'UE"] += 1
        elif nota.startswith(PROTETTO) or nota_browser.startswith(PROTETTO):
            # né rotto né controllato: il sito non lascia leggere il file ai programmi, e non lo si aggira
            protetti.append(f"{dove}: {nota_browser if nota_browser.startswith(PROTETTO) else nota}: {url}")
        else:
            non_letti.append((sito(url), f"{dove}: {nota_browser or nota}: {url}"))


# ───────────────────────── rapporto, data, uscita ─────────────────────────

def elenco_non_letti():
    """Righe del rapporto per le fonti non lette: se un sito ne ha molte, le prime tre e il conto delle altre."""
    per_sito = {}
    for host, testo in non_letti:
        per_sito.setdefault(host, []).append(testo)
    righe = []
    for host, testi in per_sito.items():
        if len(testi) > 8:
            righe += [f"- {t}" for t in testi[:3]] + [f"- … e altri {len(testi) - 3} collegamenti di {host}"]
        else:
            righe += [f"- {t}" for t in testi]
    return righe


def rapporto(documenti, catalogo, con_rete, anche_file):
    n_doc = len(tutti_i_documenti(documenti))
    n_pdf = sum(1 for v in catalogo["voci"] if v["formato"] == "pdf")
    fatto = "dati" + (", documenti e pagine del Ministero" if con_rete else "") + (", inizio di ogni PDF del catalogo" if anche_file else "")
    righe = ["## Cucina in emergenza: controllo dei collegamenti", "",
             f"Documenti: {n_doc}. Disciplinari in PDF: {n_pdf}. Data scritta nei dati: {catalogo['verificato']}.",
             f"Controllo fatto: {fatto}."]
    if metodi:
        righe.append("PDF letti: " + ", ".join(f"{n} con {m}" for m, n in sorted(metodi.items())) + ".")
    if senza_browser:
        righe.append("Ripiego con il browser non disponibile in questo giro: " + "; ".join(senza_browser) + ".")
    righe.append("")
    if errori:
        righe += ["### Collegamenti rotti o dati sbagliati", ""] + [f"- {e}" for e in errori] + [""]
    if non_letti:
        righe += ["### Fonti che non si sono fatte leggere", ""] + elenco_non_letti() + [""]
    if protetti:
        righe += ["### Collegamenti non controllati: il sito chiede una verifica anti-bot", "",
                  "Il sito ha risposto alle richieste automatiche con una pagina di verifica o con un rifiuto. Non è un",
                  "collegamento rotto e la verifica non è stata aggirata: questi collegamenti restano da controllare, e la",
                  "data di verifica scritta nei dati non cambia. Si può rilanciare il controllo un altro giorno (Actions →",
                  "«Cucina in emergenza: controllo mensile dei collegamenti» → Run workflow) o aprirli con un browser.", ""]
        righe += [f"- {p}" for p in protetti] + [""]
    if novita:
        righe += ["### Novità sulle fonti, da valutare", ""] + [f"- {n}" for n in novita] + [""]
    if errori or non_letti or novita:
        righe += ["Come si lavora: l'indirizzo nuovo si prende dalla pagina dell'ente e si verifica con una richiesta",
                  "vera, mai indovinato (regola sui guasti); poi si aggiornano `data/cucina_emergenza.yaml` o",
                  "`data/disciplinari.json`. Un allegato che non serve al catalogo si aggiunge a `allegati_noti` con il motivo.", ""]
    elif not protetti:
        righe += ["Nessun problema.", ""]
    firma = hashlib.sha256("\n".join(sorted(errori + [t for _, t in non_letti] + protetti + novita)).encode("utf-8")).hexdigest()[:16]
    righe.append(f"<!-- firma-guasti:{firma} -->")
    return "\n".join(righe) + "\n"


def aggiorna_data():
    """Scrive la data di oggi (ora italiana) in «verificato» dei due file di dati."""
    oggi = oggi_in_italia().isoformat()
    da_scrivere = []
    for percorso, modello, nuovo in ((FILE_DOCUMENTI, r'(?m)^verificato: "\d{4}-\d{2}-\d{2}"', f'verificato: "{oggi}"'),
                                    (FILE_CATALOGO, r'(?m)^  "verificato": "\d{4}-\d{2}-\d{2}"', f'  "verificato": "{oggi}"')):
        testo = percorso.read_text(encoding="utf-8")
        cambiato, quante = re.subn(modello, nuovo, testo, count=1)
        if quante != 1:
            sys.exit(f"{percorso.name}: riga «verificato» non trovata, data non aggiornata in nessuno dei due file")
        if cambiato != testo:
            da_scrivere.append((percorso, cambiato))
    for percorso, cambiato in da_scrivere:  # solo dopo aver preparato entrambi: mai due date diverse
        percorso.write_text(cambiato, encoding="utf-8")
    return oggi


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--public", metavar="CARTELLA", help="controlla anche le pagine costruite da Hugo")
    ap.add_argument("--eta", type=int, metavar="GIORNI",
                    help="errore se l'ultimo controllo completo dei collegamenti ha più di GIORNI giorni")
    ap.add_argument("--rete", action="store_true", help="richieste vere a documenti e pagine del Ministero")
    ap.add_argument("--file", action="store_true", help="con --rete: chiede anche l'inizio di ogni PDF del catalogo")
    ap.add_argument("--browser", action="store_true", help="con --rete: riprova con Chromium ciò che non si legge")
    ap.add_argument("--rapporto", metavar="FILE", help="scrive il rapporto in Markdown")
    ap.add_argument("--aggiorna-data", action="store_true", help="con --rete --file: a controllo pulito, data di oggi nei dati")
    args = ap.parse_args()
    if (args.file or args.browser or args.aggiorna_data) and not args.rete:
        ap.error("--file, --browser e --aggiorna-data valgono solo con --rete")
    if args.aggiorna_data and not args.file:
        ap.error("--aggiorna-data chiede --file: la data dice che ogni collegamento è stato controllato")
    documenti, catalogo = carica()
    controlla_dati(documenti, catalogo)
    if args.eta is not None:
        controlla_eta(documenti, catalogo, args.eta)
    if args.public:
        controlla_pagine(args.public, documenti, catalogo)
    if args.rete and not errori:
        global scadenza
        scadenza = time.time() + TEMPO_RICHIESTE
        controlla_rete(documenti, catalogo, args.file)
        chiudi_da_rivedere(args.browser)
        if args.aggiorna_data and not errori and not non_letti and not protetti:
            catalogo["verificato"] = aggiorna_data()
    testo = rapporto(documenti, catalogo, args.rete, args.rete and args.file)
    if args.rapporto:
        Path(args.rapporto).write_text(testo, encoding="utf-8")
    print(testo)
    return 1 if errori else 2 if non_letti else 3 if novita or protetti else 0


if __name__ == "__main__":
    sys.exit(main())
