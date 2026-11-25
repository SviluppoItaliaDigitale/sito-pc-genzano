#!/usr/bin/env python3
"""Controllo della sezione «Cucina in emergenza» (/cucina-emergenza/): dati e collegamenti ai PDF ufficiali.

Regola della sezione (Alessandro, 24/11/2026): solo collegamenti, verificati, a file PDF pubblicati sui siti
di enti governativi e istituzionali. Lo script la fa rispettare in due modi.

  python3 scripts/check-cucina-emergenza.py [--public public] [--eta GIORNI]
      Senza rete: forma dei dati, solo siti dell'elenco ENTI, solo PDF, nessun doppione. Con --public anche
      le pagine costruite: contengono proprio i collegamenti dei dati, nessun file Word o Excel e nessun PDF
      fuori dai dati. Bloccante sulle pull request (validate-pr.yml). Controlla anche la data di verifica:
      «verificato» è uguale nei due file di dati e non è più recente delle letture annotate in
      .manuale/cucina-emergenza-letture.json, che devono essere ben formate (la data la scrive lo script, non
      si porta avanti a mano). Con --eta è un errore anche una data «verificato» più vecchia di GIORNI
      giorni, e il messaggio nomina i collegamenti che la tengono ferma: lo usa l'audit del sito
      (audit-sito.yml, sezione 51), perché un giro mensile saltato non lascia nessun run rosso.

  python3 scripts/check-cucina-emergenza.py --unisci-letture FILE
      Senza rete: somma alle letture annotate quelle di FILE (per ogni collegamento vale il giorno più
      recente) e riporta la data di verifica. Lo usa il workflow per salvare le letture di un giro sopra
      l'ultimo main, senza conflitti con una pull request che nel frattempo ne ha annotate altre.

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
      - Disciplinari nuovi, tolti o aggiornati (Alessandro, 25/11/2026: si controlla sempre). Nuovi: un prodotto
        italiano registrato nel registro europeo che il catalogo non ha, un allegato nuovo nelle pagine del
        Ministero, l'elenco ufficiale cambiato. Tolti: un file sparito dagli allegati o che risponde 404, un
        prodotto che nel registro europeo non c'è più o non è più fra i registrati. Aggiornati: un file che
        allo stesso indirizzo pesa diversamente dal «byte» dei dati (con --file), pubblicazioni nuove nel
        registro europeo, una rettifica nuova. Il rapporto lo dice in ogni giro, anche quando non c'è nulla.
      - Sintesi europee (documento unico o scheda riepilogativa, e le loro rettifiche): il registro europeo
        eAmbrosia, letto con una richiesta, dice se per un prodotto sono uscite pubblicazioni nuove o se il
        numero di fascicolo è cambiato (novità: si rilancia scripts/aggiorna-documenti-unici.py); l'archivio
        dell'Ufficio delle pubblicazioni dell'UE, interrogato quaranta atti alla volta, dice se ogni atto
        collegato esiste ancora e se ha una rettifica che i dati non conoscono.
      - --file: chiede anche l'inizio di ogni PDF del catalogo, tre alla volta.
      - --browser: ciò che una richiesta semplice non legge si riprova con Chromium (Playwright), se c'è.
        Se Playwright manca o Chromium non parte, il controllo prosegue senza e il rapporto lo dice.
      - Verifiche anti-bot: se un sito risponde con una pagina di verifica o rifiuta la richiesta (403, 429),
        il collegamento non è rotto e non è controllato. Non si aggira: si dichiara nel rapporto, e la data
        di verifica non si aggiorna. Il sito del Ministero della Salute lo fa a tratti (24/11/2026).
      - Siti che non rispondono: un collegamento che dà tempo scaduto o un errore del server (5xx), o a cui
        il sito chiude o rifiuta la connessione, dalla macchina del controllo non è rotto e non è controllato
        (regola guasti, punto 3: non rende rosso il controllo, resta nel rapporto e si riapre con una
        richiesta vera da un'altra rete). Il 25/11/2026 il sito dell'IZS rispondeva in due secondi da una
        rete, e ai server di GitHub prima non rispondeva e poi chiudeva la connessione.
      - --aggiorna-data: se le fonti del controllo sono state lette e nulla è rotto, annota in
        .manuale/cucina-emergenza-letture.json il giorno in cui ogni collegamento è stato letto l'ultima
        volta (oggi per quelli letti in questo giro, anche senza --file) e porta «verificato» dei due file
        di dati al più vecchio di quei giorni: è la data da cui ogni collegamento è stato riletto almeno una
        volta. Così le letture fatte da reti diverse si sommano: ciò che i server di GitHub non raggiungono
        si rilegge da un'altra rete, e la data avanza lo stesso. Non torna mai indietro. Le letture
        portano il giorno in cui il giro è cominciato.
        Ogni mese: .github/workflows/controllo-cucina-emergenza.yml.

Uscita: 0 tutto a posto; 1 collegamenti rotti o dati sbagliati (con i dati sbagliati i siti non si interrogano,
e il rapporto lo dice); 2 una fonte non si è fatta leggere (pagine del Ministero, registro europeo, archivio
dell'UE, un indirizzo che risponde con altro al posto del PDF, oppure troppi collegamenti rimasti senza
controllo: più di 5 e più di un quinto di quelli da aprire. Regola guasti: un controllo che non legge la sua
fonte non chiude in verde); 3 solo novità da valutare, oppure pochi collegamenti non controllati perché il
sito chiede una verifica anti-bot o non ha risposto (regola guasti, punto 3: non sono guasti, ma si
dichiarano, e la data di verifica non va oltre il giorno della loro ultima lettura riuscita: se resta ferma
più di 45 giorni lo dice l'audit del sito con --eta).
Dati: data/cucina_emergenza.yaml, data/disciplinari.json. Le sintesi europee le scrive nei dati
scripts/aggiorna-documenti-unici.py, da cui questo script prende le funzioni sul registro e sull'archivio.
"""
import argparse
import hashlib
import html
import json
import os
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
from email.utils import parsedate_to_datetime
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
FILE_DOCUMENTI = RADICE / "data" / "cucina_emergenza.yaml"
FILE_CATALOGO = RADICE / "data" / "disciplinari.json"
# Giorno dell'ultima lettura riuscita di ogni collegamento, da qualunque rete: lo scrive --aggiorna-data.
FILE_LETTURE = RADICE / ".manuale" / "cucina-emergenza-letture.json"

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
ARCHIVIO = "publications.europa.eu"
SCRIPT_SINTESI = Path(__file__).resolve().parent / "aggiorna-documenti-unici.py"
AGENTE = "Mozilla/5.0 (compatible; PCGenzanoLinkChecker/1.0; +https://www.protezionecivilegenzano.it/)"
TIPI = {"DOP", "IGP", "STG"}
PAUSA = 0.7            # secondi fra due richieste allo stesso sito
TEMPO_MASSIMO = 90     # secondi per una risposta: nei periodi lenti il sito del Ministero ne impiega 30-40
CONTEMPORANEE = 3      # richieste insieme per i PDF del catalogo: di più, il sito del Ministero risponde 502
SOGLIA_FERMO = 5       # richieste di fila senza risposta utile dopo le quali un sito non si interroga più
QUOTA_FERMA = 0.2      # parte dei collegamenti da aprire: se ne restano di più senza controllo, il giro non vale
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
ALTRO = "risponde, ma non con un PDF"
SALTATO = "non controllato: il sito non rispondeva alle richieste precedenti"
# Il sito non ha risposto: tempo scaduto, errore del server, connessione chiusa o rifiutata dal sito prima
# della risposta (lo fa chi filtra gli indirizzi dei centri di calcolo), sito non raggiungibile dalla macchina
# del controllo, o collegamento saltato per uno di questi motivi. Non ci sono il nome che non si risolve e il
# certificato che non vale: quelli il cittadino li incontra da ogni rete, e restano fra le fonti non lette.
# Un sito spento per tutti finisce qui anche lui: lo ferma la data, che resta al giorno della sua ultima
# lettura finché, oltre i 45 giorni, l'audit del sito non lo nomina (--eta).
SILENZIO = re.compile(r"timed out|TimeoutError|\bHTTP 5\d\d\b|^non controllato:|"
                      r"(?i:socket hang up|ECONNRESET|ECONNREFUSED|ECONNABORTED|ETIMEDOUT|EHOSTUNREACH|ENETUNREACH|EPIPE\b|"
                      r"ERR_CONNECTION_(?:RESET|REFUSED|CLOSED|ABORTED|TIMED_OUT)|ERR_EMPTY_RESPONSE|ERR_TIMED_OUT|"
                      r"ERR_ADDRESS_UNREACHABLE|connection (?:reset|refused|aborted)|RemoteDisconnected|"
                      r"remote end closed connection|IncompleteRead|UNEXPECTED_EOF|EOF occurred in violation of protocol|"
                      r"broken pipe|network is unreachable|no route to host|"
                      r"socket disconnected before secure TLS connection)")

errori = []       # dati sbagliati o collegamenti rotti (uscita 1)
non_letti = []    # (sito, testo): fonti che non si sono fatte leggere (uscita 2)
novita = []       # cose nuove sulle fonti, da valutare: non sono guasti (uscita 3)
protetti = []     # collegamenti dietro una verifica anti-bot: non controllati in questo giro (uscita 3)
muti = []         # collegamenti a cui il sito non ha risposto: non controllati in questo giro (uscita 3)
da_rivedere = []  # (dove, url, nota): PDF che la richiesta semplice non ha letto, da riprovare con il browser
senza_browser = []  # perché il ripiego con il browser, se chiesto, non è stato possibile
letti = set()     # indirizzi letti davvero in questo giro: --aggiorna-data ne annota il giorno
pesi = {}         # indirizzo → (peso in byte, data del file) che il sito ha dichiarato rispondendo in questo giro
# Disciplinari nuovi, tolti o aggiornati trovati dal giro (Alessandro, 25/11/2026: «controlla sempre»): le stesse
# righe stanno anche in «novita» o, per un file sparito, in «errori», che decidono l'uscita.
disciplinari = {"nuovi": [], "tolti": [], "aggiornati": []}
confronti = {}    # che cosa il giro ha confrontato per dirlo: registro europeo, pagine del Ministero, peso dei file
note_letture = []  # che cosa --aggiorna-data ha annotato e dove si ferma la data: va nel rapporto
metodi = Counter()


def oggi_in_italia():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("Europe/Rome")).date()
    except Exception:  # macchina senza i dati dei fusi orari
        return datetime.now().date()


def controlla_eta(documenti, catalogo, giorni):
    """La data di verifica non è più vecchia di `giorni`: lo usa l'audit del sito, perché un giro mensile
    saltato, o un collegamento che la macchina del controllo non riesce a leggere, non lascia nessun run rosso."""
    fermi = ""
    try:
        attuali = list(dict.fromkeys(collegamenti_da_leggere(documenti, catalogo)))
        letture = letture_scritte()
        valide = {url: letture[url] for url in attuali if giorno_di_lettura(letture.get(url))}
        mai = [url for url in attuali if url not in valide]
        vecchio = min(valide.values(), default="")
        quali = mai or [url for url, quando in valide.items() if quando == vecchio]
        if letture and quali:
            fermi = (" Collegamenti " + ("senza una lettura annotata" if mai else f"letti l'ultima volta il {giorno(vecchio)}")
                     + ": " + ", ".join(quali[:3]) + (f" e altri {len(quali) - 3}" if len(quali) > 3 else "") + ".")
    except (KeyError, TypeError, AttributeError):  # dati malformati: lo dice già controlla_dati
        pass
    for nome, dati in (("cucina_emergenza.yaml", documenti), ("disciplinari.json", catalogo)):
        try:
            fatta = date.fromisoformat(str(dati.get("verificato", "")))
        except ValueError:
            continue  # il formato sbagliato lo segnala già controlla_dati
        eta = (oggi_in_italia() - fatta).days
        if eta > giorni:
            errori.append(f"{nome}: la data di verifica dei collegamenti è ferma al {fatta:%d/%m/%Y}, {eta} giorni fa "
                          f"(soglia {giorni}): da allora almeno un collegamento non è stato riletto. Rilanciare «Cucina in "
                          f"emergenza: controllo mensile dei collegamenti»; ciò che la macchina del controllo non legge si "
                          f"rilegge da un'altra rete con `python3 scripts/{Path(__file__).name} --rete --browser "
                          f"--aggiorna-data`, che annota le letture in {FILE_LETTURE.relative_to(RADICE)}.{fermi}")


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


def collegamenti_europei(voce):
    """Indirizzi di EUR-Lex che il catalogo mostra per un prodotto: la sintesi e le sue rettifiche."""
    sintesi = voce.get("sintesi")
    if not isinstance(sintesi, dict):
        return []
    return [x["url"] for x in [sintesi] + list(sintesi.get("rettifiche") or []) if isinstance(x, dict) and x.get("url")]


def giorno(iso):
    """«2025-10-20» → «20/10/2025»; vuoto se non è una data."""
    try:
        return date.fromisoformat(str(iso)).strftime("%d/%m/%Y")
    except ValueError:
        return ""


_sintesi = []  # il modulo scripts/aggiorna-documenti-unici.py, caricato una volta sola


def documenti_unici():
    """Funzioni e indirizzi comuni con scripts/aggiorna-documenti-unici.py: nomi dei prodotti, registro europeo,
    domande all'archivio dell'UE. Lo script si carica solo per i controlli con la rete."""
    if not _sintesi:
        import importlib.util
        spec = importlib.util.spec_from_file_location("aggiorna_documenti_unici", SCRIPT_SINTESI)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        _sintesi.append(modulo)
    return _sintesi[0]


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


def controlla_peso(dove, dati):
    """Il peso in byte del file, come lo dichiara il sito del Ministero: serve al controllo con la rete per
    riconoscere un file aggiornato senza cambiare indirizzo, e deve tornare con i KB che la pagina mostra."""
    byte, kb = dati.get("byte"), dati.get("kb")
    if not isinstance(byte, int) or byte <= 0:
        errori.append(f"{dove}: manca «byte», il peso esatto del file (l'intestazione Content-Length con cui il sito "
                      f"del Ministero lo serve): senza, un file aggiornato allo stesso indirizzo non si riconosce")
    elif isinstance(kb, int) and kb != max(1, round(byte / 1024)):
        errori.append(f"{dove}: «kb» ({kb}) non torna con «byte» ({byte}, cioè {max(1, round(byte / 1024))} KB): quando il "
                      f"file cambia si riscrivono tutti e due, con le pagine")


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
            controlla_peso(dove, voce)
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
            controlla_peso(dove + ", " + str(extra.get("etichetta")), extra)
        controlla_sintesi(dove, voce, usati)
    for noto in catalogo.get("allegati_noti", []):
        if sito(noto.get("url")) != MASAF or not noto.get("motivo"):
            errori.append("disciplinari.json: «allegati_noti» chiede, per ogni voce, l'indirizzo dell'allegato e il motivo")


def controlla_sintesi(dove, voce, usati):
    """Dati europei di un prodotto: fascicolo e impronta del registro, sintesi (documento unico o scheda
    riepilogativa) e sue rettifiche. Li scrive scripts/aggiorna-documenti-unici.py."""
    sintesi, impronta = voce.get("sintesi"), voce.get("registro_ue")
    if voce.get("tipo") == "STG":
        if sintesi is not None or impronta is not None:
            errori.append(f"{dove}: una STG non ha sintesi europea né «registro_ue»: non è nel registro delle indicazioni geografiche")
        return
    if impronta is not None and not re.fullmatch(r"([0-9a-f]{12})?", str(impronta)):
        errori.append(f"{dove}: «registro_ue» è l'impronta scritta da scripts/aggiorna-documenti-unici.py (12 cifre esadecimali, o vuota)")
    if (impronta is not None or sintesi is not None) and not re.fullmatch(r"(PDO|PGI)-IT-\d+", str(voce.get("fascicolo", ""))):
        errori.append(f"{dove}: «fascicolo» deve essere il numero del registro europeo (PDO-IT-… o PGI-IT-…)")
    if sintesi is None:
        return
    if not isinstance(sintesi, dict) or sintesi.get("tipo") not in ("unico", "scheda"):
        errori.append(f"{dove}: «sintesi» chiede il tipo «unico» (documento unico) o «scheda» (scheda riepilogativa)")
        return
    if impronta in (None, ""):
        errori.append(f"{dove}: ha una sintesi europea ma non l'impronta «registro_ue»: va riletto con scripts/aggiorna-documenti-unici.py")
    rettifiche = sintesi.get("rettifiche", [])
    if not isinstance(rettifiche, list) or not all(isinstance(r, dict) for r in rettifiche):
        errori.append(f"{dove}: «rettifiche» è un elenco di documenti (url, data, pagine, kb)")
        rettifiche = []
    for che, documento in [("sintesi europea", sintesi)] + [("rettifica della sintesi europea", r) for r in rettifiche]:
        qui = f"{dove}, {che}"
        url = documento.get("url")
        controlla_url(qui, url)
        if sito(url) != EURLEX or not re.fullmatch(r"[0-9A-Z()]+", celex_di(url) or ""):
            errori.append(f"{qui}: si collega solo il PDF su EUR-Lex, con il suo numero CELEX")
        if url in usati:
            errori.append(f"{qui}: indirizzo già usato da un'altra voce")
        usati.add(url)
        if not all(isinstance(documento.get(k), int) and documento.get(k) > 0 for k in ("pagine", "kb")):
            errori.append(f"{qui}: mancano pagine o peso del PDF")
        try:
            uscita = date.fromisoformat(str(documento.get("data", "")))
        except ValueError:
            errori.append(f"{qui}: «data» deve essere la data della Gazzetta ufficiale, AAAA-MM-GG")
            continue
        if uscita > oggi_in_italia():
            errori.append(f"{qui}: «data» è una data futura")
        if documento is not sintesi and str(documento["data"]) < str(sintesi.get("data", "")):
            errori.append(f"{qui}: è più vecchia dell'atto che corregge")
    altre = sintesi.get("rettifiche_altre", [])
    if not isinstance(altre, list) or not all(isinstance(a, str) and re.fullmatch(r"[0-9A-Z()]+", a) for a in altre):
        errori.append(f"{dove}: «rettifiche_altre» è un elenco di numeri CELEX")


# ───────────────────────── pagine costruite ─────────────────────────

def giorno_di_lettura(quando):
    """Vero se `quando` è un giorno AAAA-MM-GG, non nel futuro: così si scrivono le letture annotate."""
    return (isinstance(quando, str) and bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", quando)) and bool(giorno(quando))
            and quando <= oggi_in_italia().isoformat())


def controlla_letture(documenti, catalogo):
    """Le due date «verificato» coincidono; il file delle letture, se c'è, è una mappa indirizzo → giorno, e la
    data dei dati non è più recente dell'ultima lettura annotata di nessun collegamento: la data la scrive lo
    script, e chi la porta avanti a mano dichiara un controllo che non c'è stato. Restituisce i collegamenti
    dei dati che non hanno ancora una lettura annotata (non è un errore: la data resta ferma finché non si
    leggono)."""
    nome = FILE_LETTURE.relative_to(RADICE)
    if str(documenti.get("verificato", "")) != str(catalogo.get("verificato", "")):
        errori.append(f"«verificato» è diverso nei due file di dati ({documenti.get('verificato')} in cucina_emergenza.yaml, "
                      f"{catalogo.get('verificato')} in disciplinari.json): le due date le scrive insieme lo script")
    try:
        letture = json.loads(FILE_LETTURE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except (OSError, ValueError) as e:
        errori.append(f"{nome}: il file delle letture non si legge ({type(e).__name__})")
        return []
    if not isinstance(letture, dict):
        errori.append(f"{nome}: il file delle letture deve essere una mappa indirizzo → giorno")
        return []
    sbagliati = sorted(url for url, quando in letture.items() if not giorno_di_lettura(quando))
    if sbagliati:
        errori.append(f"{nome}: {len(sbagliati)} letture con il giorno scritto male o nel futuro (la prima: {sbagliati[0]})")
    attuali = set(collegamenti_da_leggere(documenti, catalogo))
    scritta = max(str(documenti.get("verificato", "")), str(catalogo.get("verificato", "")))
    indietro = sorted(url for url, quando in letture.items() if url in attuali and giorno_di_lettura(quando) and quando < scritta)
    if indietro:
        errori.append(f"«verificato» ({scritta}) è più recente dell'ultima lettura annotata di {len(indietro)} collegamenti "
                      f"(il primo: {indietro[0]}, letto il {letture[indietro[0]]}): la data la scrive lo script da {nome}, "
                      f"con --rete --aggiorna-data, e non si porta avanti a mano")
    return [url for url in dict.fromkeys(collegamenti_da_leggere(documenti, catalogo)) if not giorno_di_lettura(letture.get(url))]


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
        for url in collegamenti_europei(voce):
            nei_dati.add(url)
            if url not in nel_cat:
                errori.append(f"disciplinare «{voce['nome']}»: la sintesi europea, o una sua rettifica, non compare "
                              f"nel catalogo costruito: {url}")
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


def chiedi(url, intervallo=None, quanto=None, intestazioni=None, segui=True, tentativi=3, ricevute=None):
    """Una richiesta GET educata: pausa fra due richieste allo stesso sito, nuovi tentativi con attese
    crescenti. Restituisce (stato, contenuto, errore); stato 0 se non è arrivata nessuna risposta utile.
    Se `ricevute` è un dizionario, vi finiscono le intestazioni della risposta, con i nomi in minuscolo."""
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
                if ricevute is not None:
                    ricevute.clear()
                    ricevute.update({nome.lower(): valore for nome, valore in risposta.headers.items()})
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
            errore = " ".join(f"{type(e).__name__}: {e}".split())  # su una riga: finisce nel rapporto
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


def peso_del_file(stato, campi):
    """Peso in byte del file intero secondo le intestazioni della risposta: il totale di Content-Range in una
    risposta parziale (206), Content-Length in una intera (200). None se il sito non lo dice."""
    if campi.get("content-encoding"):
        return None  # sarebbe il peso della versione compressa, non del file
    if stato == 206:
        m = re.fullmatch(r"bytes\s+[0-9]+-[0-9]+/([0-9]+)", (campi.get("content-range") or "").strip())
        return int(m.group(1)) if m else None
    m = re.fullmatch(r"[0-9]+", (campi.get("content-length") or "").strip())
    return int(m.group(0)) if stato == 200 and m else None


def data_del_file(campi):
    """Giorno «Last-Modified» dichiarato dal sito, AAAA-MM-GG; vuoto se manca o non si legge."""
    try:
        return parsedate_to_datetime(campi.get("last-modified") or "").date().isoformat()
    except (TypeError, ValueError):
        return ""


def leggi_pdf(url):
    """('pdf', '') se all'indirizzo c'è un PDF, ('assente', …) con 404 o 410, ('protetto', …) se il sito risponde
    con una pagina di verifica anti-bot o rifiuta la richiesta (403, 429), altrimenti che cosa è successo.
    Di un PDF letto annota in `pesi` il peso e la data che il sito dichiara: servono a riconoscere un file
    aggiornato senza cambiare indirizzo."""
    campi = {}
    stato, inizio, errore = chiedi(url, intervallo="bytes=0-7", quanto=8, ricevute=campi)
    if stato in (200, 206) and not inizio.startswith(b"%PDF"):
        # qualche sito, a una richiesta parziale, risponde con una pagina: si richiede il file intero
        stato, inizio, errore = chiedi(url, quanto=32768, ricevute=campi)
    if stato in (404, 410):
        return "assente", f"HTTP {stato}"
    if stato in (200, 206) and inizio.startswith(b"%PDF"):
        peso = peso_del_file(stato, campi)
        if peso:
            pesi[url] = (peso, data_del_file(campi))
        return "pdf", ""
    if stato in (200, 206):
        return ("protetto", ANTIBOT) if sembra_verifica(inizio) else ("altro", ALTRO)
    if errore in ("HTTP 403", "HTTP 429"):
        return "protetto", f"{RIFIUTO} ({errore})"
    return "muto", errore or f"HTTP {stato}"


def controlla_pdf(dove, url):
    host = sito(url)
    if di_fila.get(host, 0) >= SOGLIA_FERMO:
        perche = motivo.get(host, "")
        da_rivedere.append((dove, url, perche if perche.startswith(PROTETTO) else SALTATO))
        return
    esito, nota = leggi_pdf(url)
    segna(host, esito in ("pdf", "assente"), nota)
    if esito == "pdf":
        metodi["richiesta diretta"] += 1
        letti.add(url)
    elif esito == "assente":
        errori.append(f"{dove}: {nota}: {url}")
    else:
        da_rivedere.append((dove, url, nota))


def chiedi_all_archivio(domanda):
    """Righe della risposta dell'archivio dell'UE a una domanda SPARQL; None se l'archivio non risponde."""
    stato, corpo, _ = chiedi(SPARQL_UE + "?" + urllib.parse.urlencode({"query": domanda}),
                             intestazioni={"Accept": "application/sparql-results+json"})
    if stato != 200:
        return None
    try:
        righe = json.loads(corpo)["results"]["bindings"]
    except (ValueError, KeyError, TypeError):
        return None
    return righe if isinstance(righe, list) else None


def ultima_consolidata(celex):
    """Numero CELEX dell'ultima versione consolidata dell'atto, chiesto all'archivio dell'UE; None se non risponde."""
    base, prefisso = "3" + celex.split("-")[0][1:], celex.split("-")[0] + "-"
    righe = chiedi_all_archivio(
        "PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> SELECT DISTINCT ?celex WHERE { "
        f'?base cdm:resource_legal_id_celex "{base}"^^<http://www.w3.org/2001/XMLSchema#string> . '
        "?cons cdm:act_consolidated_consolidates_resource_legal ?base ; cdm:resource_legal_id_celex ?celex . }")
    try:
        valori = [r["celex"]["value"] for r in righe]
    except (KeyError, TypeError):  # anche righe None: l'archivio non ha risposto
        return None
    versioni = sorted(v for v in valori if v.startswith(prefisso))
    return versioni[-1] if versioni else None


def modifiche(celex):
    """Atti che hanno modificato un atto di base (numeri CELEX, senza le rettifiche), chiesti all'archivio dell'UE;
    None se non risponde. Un atto modificato ha un testo consolidato: è quello che conviene collegare."""
    righe = chiedi_all_archivio(
        "PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> SELECT DISTINCT ?celex WHERE { "
        f'?base cdm:resource_legal_id_celex "{celex}"^^<http://www.w3.org/2001/XMLSchema#string> . '
        "?mod cdm:resource_legal_amends_resource_legal ?base ; cdm:resource_legal_id_celex ?celex . }")
    try:
        valori = [r["celex"]["value"] for r in righe]
    except (KeyError, TypeError):  # anche righe None: l'archivio non ha risposto
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
        non_letti.append((ARCHIVIO, f"{dove}: l'archivio dell'UE non ha risposto per CELEX {celex} ({errore or 'HTTP ' + str(stato)})"))
        return
    if re.fullmatch(r"0\d{4}[A-Z]{1,2}\d{4}-\d{8}", celex):
        ultima = ultima_consolidata(celex)
        if ultima is None:
            non_letti.append((ARCHIVIO, f"{dove}: l'archivio dell'UE non ha detto qual è l'ultima versione consolidata di {celex}"))
        elif ultima > celex:
            novita.append(f"{dove}: è uscita una versione consolidata più recente ({ultima}; il sito collega {celex})")
    elif re.fullmatch(r"3\d{4}[RLD]\d{4}", celex):
        # atto collegato nel testo della Gazzetta ufficiale: se nel frattempo è stato modificato, lo si dice
        cambiato_da = modifiche(celex)
        if cambiato_da is None:
            non_letti.append((ARCHIVIO, f"{dove}: l'archivio dell'UE non ha detto se {celex} è stato modificato"))
        elif cambiato_da:
            novita.append(f"{dove}: l'atto {celex} è stato modificato da {', '.join(cambiato_da)}: va collegato il testo "
                          f"consolidato più recente al posto di quello della Gazzetta ufficiale")
    stato, inizio, errore = chiedi(url, quanto=8)
    if stato in (404, 410):
        errori.append(f"{dove}: HTTP {stato}: {url}")
    elif stato == 200 and inizio.startswith(b"%PDF"):
        metodi["richiesta diretta"] += 1
        letti.add(url)
    elif stato in (200, 202):
        da_rivedere.append((dove, url, "EUR-Lex"))
    elif errore in ("HTTP 403", "HTTP 429"):
        protetti.append(f"{dove}: {RIFIUTO} ({errore}): {url}")
    elif SILENZIO.search(errore or f"HTTP {stato}"):
        # il documento esiste nell'archivio (controllato qui sopra): è l'indirizzo di EUR-Lex che da questa
        # macchina non ha risposto. Come per gli altri siti: né rotto né controllato (regola guasti, punto 3)
        muti.append(f"{dove}: {errore or 'HTTP ' + str(stato)}: {url}")
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
    confronti["pagine"] = [0, len(attesi)]  # pagine del Ministero lette, pagine da leggere
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
        confronti["pagine"][0] += 1
        for dove, url in mancanti:
            errori.append(f"{dove}: il file non è più fra gli allegati di {indirizzo} (il Ministero può averlo sostituito)")
            if dove.startswith("disciplinare"):
                disciplinari["tolti"].append(errori[-1])
        if numero == pagina_di(elenco["allegato"]) and elenco["allegato"] not in trovati:
            novita.append(f"il Ministero ha cambiato l'elenco dei prodotti DOP e IGP ({indirizzo}): va confrontato "
                          f"con il catalogo, che segue quello aggiornato al {elenco['aggiornato']}")
            disciplinari["nuovi"].append(novita[-1])
        if numero in del_catalogo:
            usati = {url for _, url in attesi[numero]}
            for url, titolo in trovati.items():
                if url not in usati and url not in noti:
                    novita.append(f"allegato nuovo «{titolo}» in {indirizzo}: {url}")
                    # nella pagina delle modifiche temporanee è un cambiamento a un disciplinare che c'è già
                    disciplinari["aggiornati" if numero == PAGINA_MODIFICHE else "nuovi"].append(novita[-1])


def registrato(voce_del_registro):
    """Vero se il registro europeo dà il prodotto per registrato e non tolto. Un prodotto cancellato resta
    nell'elenco con lo stato «registered» e il segno «removedFlag»: il 24/11/2026 erano così 21 voci (16 vini
    e 5 alimenti, nessun alimento italiano); lo stesso segno hanno le domande ritirate."""
    return (voce_del_registro.get("status") or "").lower() == "registered" and not voce_del_registro.get("removedFlag")


def controlla_registro_europeo(ue, voci):
    """Il registro eAmbrosia, letto con una richiesta sola, dice se per un prodotto sono uscite pubblicazioni che i
    dati non hanno visto, se il numero di fascicolo è cambiato, se il prodotto non c'è più con quel nome o non è
    più fra quelli registrati, e se l'Italia ha un prodotto registrato che il catalogo non ha. Sono novità da
    valutare, non guasti: l'atto collegato resta quello che era."""
    host = sito(ue.REGISTRO)
    stato, corpo, errore = chiedi(ue.REGISTRO, intestazioni={"Accept": "application/json", "Accept-Language": "en"})
    registro = None
    if stato == 200:
        try:
            registro = ue.voci_italiane(json.loads(corpo))
        except (ValueError, TypeError, AttributeError):
            registro = None
    if not registro:
        perche = errore or (f"HTTP {stato}" if stato != 200 else "risposta non leggibile, o senza prodotti italiani")
        non_letti.append((host, f"registro europeo eAmbrosia: {perche}: non si sa se per i prodotti del catalogo sono "
                                f"uscite pubblicazioni nuove"))
        return
    per_nome = ue.indice_per_nome(registro)
    assenti, trovate, tolti, cambiati = [], [], [], []
    del_catalogo = set()  # voci del registro che portano il nome di un prodotto del catalogo
    for voce in voci:
        dove = f"disciplinare «{voce['nome']}»"
        for parte in ue.parti_del_nome(voce["nome"]):
            del_catalogo.update(v.get("giIdentifier") for v in per_nome.get(parte, []))
        del_registro = ue.abbina(voce, per_nome)
        if del_registro is None:
            assenti.append(f"{dove}: nel registro europeo non c'è più un solo prodotto con questo nome (rinominato, "
                           f"cancellato o doppio): va guardato a mano")
            continue
        if not registrato(del_registro):
            come = "è segnato come tolto" if del_registro.get("removedFlag") else f"ha lo stato «{del_registro.get('status')}»"
            tolti.append(f"{dove}: nel registro europeo non è più fra i prodotti registrati ({come}): va guardato a mano, "
                         f"e se la registrazione è stata cancellata la voce si toglie dal catalogo")
        if "registro_ue" not in voce:
            trovate.append(f"{dove}: mai cercato nel registro europeo: `python3 scripts/aggiorna-documenti-unici.py`")
            continue
        if ue.fascicolo_normale(del_registro.get("fileNumber")) != ue.fascicolo_normale(voce.get("fascicolo")):
            trovate.append(f"{dove}: per il registro europeo il fascicolo è {del_registro.get('fileNumber')}, nei dati "
                           f"{voce.get('fascicolo')}")
        if ue.impronta_del_registro(del_registro) != voce["registro_ue"]:
            ultima = giorno(ue.ultima_pubblicazione(del_registro))
            cambiati.append(f"{dove}: il registro europeo cita pubblicazioni diverse da quelle viste"
                            + (f" (la più recente con la data è del {ultima})" if ultima else "")
                            + ": la sintesi europea può essere cambiata")
    if len(assenti) * 2 > len(voci):
        # più della metà dei prodotti introvabile: è l'elenco che è stato letto male o ha cambiato forma
        non_letti.append((host, f"registro europeo eAmbrosia: {len(assenti)} prodotti su {len(voci)} non si trovano "
                                f"(elenco letto male o cambiato)"))
        return
    # prodotti registrati per l'Italia che non portano il nome di nessuna voce del catalogo: disciplinari nuovi
    nuovi = []
    for v in registro:
        if not registrato(v) or v.get("giIdentifier") in del_catalogo:
            continue
        nome = " / ".join(n.strip() for n in v.get("protectedNames") or [] if (n or "").strip()) or "senza nome"
        sigla = {"PDO": "DOP", "PGI": "IGP"}.get(v.get("giType"), v.get("giType") or "tipo non indicato")
        dal = giorno(v.get("euProtectionDate"))
        nuovi.append(f"prodotto nuovo nel registro europeo: «{nome}» ({sigla}, fascicolo {v.get('fileNumber')}"
                     + (f", protezione europea dal {dal}" if dal else "") + "): non è nel catalogo, va aggiunto con il "
                     "disciplinare che il Ministero pubblica nella pagina della sua classe")
    confronti["registro"] = sum(1 for v in registro if registrato(v))
    novita.extend(assenti + tolti + trovate + cambiati + nuovi)
    disciplinari["tolti"] += assenti + tolti
    disciplinari["aggiornati"] += cambiati
    disciplinari["nuovi"] += nuovi


def controlla_archivio_delle_sintesi(ue, voci):
    """L'archivio dell'Ufficio delle pubblicazioni dell'UE dice, quaranta atti alla volta, se ogni atto collegato
    come sintesi o come rettifica esiste ancora e se ha una rettifica che i dati non conoscono. EUR-Lex non si
    interroga: alle richieste di un programma risponde 202 senza contenuto, per 288 atti come per uno."""
    attesi, note = {}, {}
    non_letti_prima = len(non_letti)
    for voce in voci:
        sintesi = voce.get("sintesi")
        if not sintesi:
            continue
        atto = celex_di(sintesi["url"])
        attesi[atto] = (f"disciplinare «{voce['nome']}», sintesi europea", sintesi["url"])
        conosciute = set(sintesi.get("rettifiche_altre", []))
        for rettifica in sintesi.get("rettifiche", []):
            numero = celex_di(rettifica["url"])
            attesi[numero] = (f"disciplinare «{voce['nome']}», rettifica della sintesi europea", rettifica["url"])
            conosciute.add(numero)
        note[atto] = (voce["nome"], conosciute)
    for gruppo in ue.a_gruppi(attesi):
        righe = chiedi_all_archivio(ue.domanda_esistenza(gruppo))
        try:
            presenti = {r["celex"]["value"] for r in righe}
        except (KeyError, TypeError):  # anche righe None: l'archivio non ha risposto
            non_letti.append((ARCHIVIO, f"l'archivio dell'UE non ha detto se esistono ancora {len(gruppo)} atti delle "
                                        f"sintesi europee (da {gruppo[0]} a {gruppo[-1]})"))
            continue
        for numero in gruppo:
            dove, url = attesi[numero]
            if numero in presenti:
                metodi["archivio dell'UE"] += 1
                continue
            # la risposta a gruppi può arrivare incompleta: prima di dichiarare rotto un collegamento si chiede
            # l'atto da solo, all'indirizzo che risponde 303 se esiste e 404 se no
            stato, _, errore = chiedi(ARCHIVIO_UE.format(urllib.parse.quote(numero, safe="")), quanto=8, segui=False,
                                      intestazioni={"Accept": "*/*", "Accept-Language": "it"})
            if stato == 404:
                errori.append(f"{dove}: il documento CELEX {numero} non esiste nell'archivio dell'Unione europea: {url}")
            elif stato in (200, 303):
                metodi["archivio dell'UE"] += 1
            else:
                non_letti.append((ARCHIVIO, f"{dove}: l'archivio dell'UE non ha risposto per CELEX {numero} "
                                            f"({errore or 'HTTP ' + str(stato)})"))
    for gruppo in ue.a_gruppi(note):
        righe = chiedi_all_archivio(ue.domanda_rettifiche(gruppo))
        try:
            legate = ue.righe_delle_rettifiche(righe)
        except (KeyError, TypeError):  # anche righe None: l'archivio non ha risposto
            non_letti.append((ARCHIVIO, f"l'archivio dell'UE non ha detto se {len(gruppo)} atti delle sintesi europee "
                                        f"hanno rettifiche nuove (da {gruppo[0]} a {gruppo[-1]})"))
            continue
        for atto, coppie in sorted(legate.items()):
            nome, conosciute = note.get(atto, ("", set()))
            for numero, quando in coppie:
                if nome and numero not in conosciute:
                    novita.append(f"disciplinare «{nome}»: l'archivio dell'UE ha una rettifica della sintesi europea che i "
                                  f"dati non conoscono ({numero}" + (f", del {giorno(quando)}" if giorno(quando) else "") + ")")
                    disciplinari["aggiornati"].append(novita[-1])
        # la controprova: le rettifiche che i dati conoscono devono tornare nella risposta. Se mancano, la
        # risposta è incompleta o la domanda non funziona più, e «nessuna rettifica nuova» non vorrebbe dire nulla
        perse = sorted((note[atto][0], numero, atto) for atto in gruppo for numero in note[atto][1]
                       if numero not in {n for n, _ in legate.get(atto, [])})
        if perse:
            nome, numero, atto = perse[0]
            non_letti.append((ARCHIVIO, f"l'archivio dell'UE non ha restituito {len(perse)} rettifiche che i dati conoscono "
                                        f"(la prima: {numero}, dell'atto {atto}, «{nome}»): risposta incompleta, non si sa "
                                        f"se ci sono rettifiche nuove. Se si ripete, e l'archivio ha davvero tolto il "
                                        f"legame, la rettifica si toglie dai dati solo così: "
                                        f"`python3 scripts/aggiorna-documenti-unici.py --nome \"{nome}\"`"))
    confronti["archivio"] = len(non_letti) == non_letti_prima  # letto tutto: «nessuna rettifica nuova» vale


def controlla_europa(catalogo):
    """Sintesi europee del catalogo: registro eAmbrosia e archivio dell'Ufficio delle pubblicazioni dell'UE."""
    voci = [v for v in catalogo["voci"] if v.get("tipo") != "STG"]
    if not any("registro_ue" in v or v.get("sintesi") for v in voci):
        return
    try:
        ue = documenti_unici()
    except Exception as e:  # file mancante o non caricabile: è un errore del repository, non di una fonte
        errori.append(f"scripts/{SCRIPT_SINTESI.name} non si carica ({type(e).__name__}: {e}): le sintesi europee "
                      f"non sono state controllate")
        return
    controlla_registro_europeo(ue, voci)
    controlla_archivio_delle_sintesi(ue, voci)


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
                nota = errore or "HTTP " + str(stato)
                if SILENZIO.search(nota):
                    muti.append(f"{dove}, pagina dell'ente: {nota}: {doc['pagina']['url']}")
                else:
                    non_letti.append((sito(doc["pagina"]["url"]), f"{dove}, pagina dell'ente: {nota}"))
            else:
                letti.add(doc["pagina"]["url"])
    controlla_ministero(documenti, catalogo)
    controlla_europa(catalogo)  # prima dei file del Ministero, che nei periodi lenti consumano il tempo del giro
    if anche_file:
        controlla_file_del_catalogo(catalogo)


def file_del_catalogo(catalogo):
    """I PDF del Ministero che il catalogo collega: (dove, indirizzo, peso in byte scritto nei dati)."""
    voci = []
    for voce in catalogo["voci"]:
        if voce["formato"] == "pdf":
            voci.append((f"disciplinare «{voce['nome']}»", voce["url"], voce.get("byte")))
        for extra in voce.get("extra", []):
            voci.append((f"disciplinare «{voce['nome']}», {extra['etichetta']}", extra["url"], extra.get("byte")))
    return voci


def controlla_file_del_catalogo(catalogo):
    """Chiede l'inizio di ogni PDF del catalogo, CONTEMPORANEE alla volta. Dopo SOGLIA_FERMO file di fila senza
    risposta utile si ferma: gli altri restano «non controllati» e il rapporto lo dice."""
    voci = [(dove, url) for dove, url, _ in file_del_catalogo(catalogo)]
    fermo = threading.Event()
    perche = []  # motivo dell'ultima lettura non riuscita: lo scrive solo il ciclo qui sotto

    def uno(voce):
        if time.time() > scadenza:
            return "saltato", FUORI_TEMPO
        if fermo.is_set():
            ultimo_motivo = perche[-1] if perche else ""
            return "saltato", ultimo_motivo if ultimo_motivo.startswith(PROTETTO) else SALTATO
        return leggi_pdf(voce[1])

    senza_risposta = 0  # file di fila senza risposta utile (non la lista «muti» del rapporto)
    with ThreadPoolExecutor(max_workers=CONTEMPORANEE) as squadra:
        for (dove, url), (esito, nota) in zip(voci, squadra.map(uno, voci)):
            if esito == "pdf":
                metodi["richiesta diretta"] += 1
                letti.add(url)
                senza_risposta = 0
            elif esito == "assente":
                errori.append(f"{dove}: {nota}: {url}")
                disciplinari["tolti"].append(errori[-1])
                senza_risposta = 0
            else:
                da_rivedere.append((dove, url, nota))
                if esito != "saltato":
                    senza_risposta += 1
                    perche.append(nota)
                if senza_risposta >= SOGLIA_FERMO:
                    fermo.set()


def confronta_pesi(catalogo):
    """Un file aggiornato senza cambiare indirizzo: il sito ne dichiara un peso diverso dal «byte» dei dati. Si
    chiama dopo il ripiego con il browser, così vale anche per i file che ha letto lui. Un file sostituito con
    uno dello stesso peso, al byte, non si vede da qui: di una modifica vera al disciplinare parla anche il
    registro europeo, che cita una pubblicazione in più."""
    voci = file_del_catalogo(catalogo)
    confronti["file"] = [0, len(voci)]  # file di cui si è confrontato il peso, file del catalogo
    for dove, url, atteso in voci:
        peso, del_giorno = pesi.get(url, (None, ""))
        if not peso or not isinstance(atteso, int):
            continue
        confronti["file"][0] += 1
        if peso != atteso:
            novita.append(f"{dove}: il file allo stesso indirizzo è cambiato: nei dati pesa {atteso} byte, ora {peso}"
                          + (f" (il sito del Ministero lo data al {giorno(del_giorno)})" if giorno(del_giorno) else "")
                          + f". Va riaperto e riletto, e nei dati si riscrivono pagine, kb e byte: {url}")
            disciplinari["aggiornati"].append(novita[-1])


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
                        except Exception:
                            # un PDF fa partire lo scaricamento e interrompe la navigazione; di ogni altra
                            # interruzione dice di più la richiesta che segue: la risposta del sito, o
                            # l'errore di rete, che finisce nell'«except» in fondo
                            pass
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
                pesi[url] = (len(risposta.body()), "")  # il browser riceve il file intero
                falliti[sito(url)] = 0
            except Exception as e:
                # di un errore di Playwright serve la prima riga: le altre sono il registro delle chiamate
                esiti[url] = ("no", f"{type(e).__name__}: {(str(e).strip().splitlines() or [''])[0][:120]}")
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
        note = [n for n in (nota_browser, nota) if n]  # prima ciò che ha visto il browser, poi la richiesta semplice
        if esito == "pdf":
            metodi["browser"] += 1
            letti.add(url)
        elif esito == "assente":
            errori.append(f"{dove}: {nota_browser}: {url}")
            if dove.startswith("disciplinare"):  # un file del catalogo che non c'è più
                disciplinari["tolti"].append(errori[-1])
        elif nota == "EUR-Lex":
            # il documento esiste nell'archivio dell'UE e l'indirizzo di EUR-Lex risponde: di più una
            # richiesta automatica non ottiene
            metodi["archivio dell'UE"] += 1
            letti.add(url)
        elif any(n.startswith(PROTETTO) for n in note):
            # né rotto né controllato: il sito non lascia leggere il file ai programmi, e non lo si aggira
            protetti.append(f"{dove}: {next(n for n in note if n.startswith(PROTETTO))}: {url}")
        elif note and all(SILENZIO.search(n) for n in note):
            # né rotto né controllato: da questa macchina il sito non ha risposto, né alla richiesta semplice
            # né al browser (regola guasti, punto 3)
            muti.append(f"{dove}: {note[0]}: {url}")
        else:
            # almeno una delle due richieste ha avuto una risposta, e non era il PDF: conta quella, non il
            # silenzio dell'altra
            non_letti.append((sito(url), f"{dove}: {next((n for n in note if not SILENZIO.search(n)), '')}: {url}"))


def collegamenti_da_leggere(documenti, catalogo, anche_file=True):
    """Gli indirizzi che il giro apre con una richiesta sua: documenti, pagine degli enti e, con --file, i PDF
    del catalogo. Le sintesi europee non ci sono: di quelle si chiede all'archivio dell'UE, tutte insieme."""
    indirizzi = []
    for doc in tutti_i_documenti(documenti):
        indirizzi.append(doc["url"])
        if doc.get("pagina") and sito(doc["pagina"]["url"]) != MASAF:
            indirizzi.append(doc["pagina"]["url"])
    if anche_file:
        for voce in catalogo["voci"]:
            if voce["formato"] == "pdf":
                indirizzi.append(voce["url"])
            indirizzi += [extra["url"] for extra in voce.get("extra", [])]
    return indirizzi


def collegamenti_da_aprire(documenti, catalogo, anche_file):
    """Quanti collegamenti il giro apre con una richiesta sua."""
    return len(collegamenti_da_leggere(documenti, catalogo, anche_file))


def segnala_controllo_mancato(da_aprire):
    """Qualche collegamento dietro una verifica anti-bot o senza risposta è un collegamento da riaprire, e il
    giro resta verde (regola guasti, punto 3). Quando sono più di SOGLIA_FERMO e più di QUOTA_FERMA di quelli
    da aprire, è il controllo che non c'è stato (rete della macchina, un sito fermo, una fonte intera che
    rifiuta i programmi): vale la regola guasti, punto 1, e il giro non chiude in verde."""
    fermi = protetti + muti
    if len(fermi) <= SOGLIA_FERMO or len(fermi) <= QUOTA_FERMA * da_aprire:
        return
    per_sito = Counter(sito(voce.rsplit(": ", 1)[-1]) for voce in fermi).most_common()
    non_letti.append((per_sito[0][0], f"{len(fermi)} collegamenti su {da_aprire} non controllati ("
                                      + ", ".join(f"{quanti} di {host}" for host, quanti in per_sito)
                                      + "): sono troppi perché il giro valga come controllo dei collegamenti. "
                                        "L'elenco è nelle due sezioni dei collegamenti non controllati"))


# ───────────────────────── rapporto, data, uscita ─────────────────────────

def elenco_per_sito(voci):
    """Righe del rapporto per un elenco di (sito, testo): se un sito ne ha molte, le prime tre e il conto delle altre."""
    per_sito = {}
    for host, testo in voci:
        per_sito.setdefault(host, []).append(testo)
    righe = []
    for host, testi in per_sito.items():
        if len(testi) > 8:
            righe += [f"- {t}" for t in testi[:3]] + [f"- … e altri {len(testi) - 3} collegamenti di {host}"]
        else:
            righe += [f"- {t}" for t in testi]
    return righe


def righe_dei_disciplinari(anche_file):
    """Che cosa il giro ha trovato di nuovo, tolto o aggiornato fra i disciplinari, e con quali confronti: la
    prima riga c'è in ogni rapporto fatto con la rete, anche quando non è cambiato nulla (Alessandro,
    25/11/2026: «controlla sempre se ci sono nuovi disciplinari, se vengono tolti o aggiornati»). «Nessuno» si
    scrive solo se i confronti di quella voce sono stati fatti per intero: altrimenti la riga dice che cosa manca."""
    def prodotti(voci):
        """Quanti disciplinari o allegati diversi: dello stesso disciplinare possono parlare più righe (file
        sparito dagli allegati, 404, registro)."""
        diversi = set()
        for voce in voci:
            nome = re.match(r"disciplinare «[^»]+»", voce)
            diversi.add(nome.group(0) if nome else voce)
        return len(diversi)

    def esito(chiave, mancano):
        voci = disciplinari[chiave]
        if mancano:
            return (f"{prodotti(voci)}, con il confronto incompleto" if voci else "confronto incompleto") + f" ({', '.join(mancano)})"
        return str(prodotti(voci)) if voci else "nessuno"

    lette, tutte = confronti.get("pagine", [0, 0])
    senza_registro = [] if "registro" in confronti else ["registro europeo non letto"]
    senza_pagine = ([] if "pagine" in confronti and lette == tutte else
                    [f"{tutte - lette} pagine del Ministero su {tutte} non lette" if "pagine" in confronti
                     else "pagine del Ministero non lette"])
    senza_archivio = [] if confronti.get("archivio") else ["archivio dell'UE non letto per intero"]
    pesati, file = confronti.get("file", [0, 0])
    if not anche_file:
        senza_peso = ["peso dei file non confrontato: giro senza --file"]
    else:
        senza_peso = [] if "file" in confronti and pesati == file else [f"peso confrontato per {pesati} file su {file}"]
    riga = (f"Disciplinari nuovi: {esito('nuovi', senza_registro + senza_pagine)}. "
            f"Tolti: {esito('tolti', senza_registro + senza_pagine)}. "
            f"Aggiornati: {esito('aggiornati', senza_registro + senza_archivio + senza_peso)}.")
    fatti = ([f"{confronti['registro']} prodotti italiani registrati nel registro europeo"] if "registro" in confronti else [])
    if "pagine" in confronti:
        fatti.append(f"allegati di {lette} pagine del Ministero su {tutte}")
    if anche_file and "file" in confronti:
        fatti.append(f"peso di {pesati} file del Ministero su {file}")
    righe = [riga + (f" Confrontati: {'; '.join(fatti)}." if fatti else ""), ""]
    if not any(disciplinari.values()):
        return righe
    righe += ["### Disciplinari nuovi, tolti o aggiornati", ""]
    for titolo, chiave in (
            ("Nuovi (prodotti registrati che il catalogo non ha, allegati comparsi nelle pagine del Ministero)", "nuovi"),
            ("Tolti (file spariti, prodotti che nel registro europeo non si trovano più o non sono più registrati)", "tolti"),
            ("Aggiornati (file cambiati allo stesso indirizzo, modifiche temporanee, pubblicazioni o rettifiche nuove)", "aggiornati")):
        if disciplinari[chiave]:
            righe += [f"{titolo}:", ""] + [f"- {voce}" for voce in disciplinari[chiave]] + [""]
    righe += ["Come si lavorano: un prodotto nuovo si aggiunge a `data/disciplinari.json` con il PDF che il Ministero",
              "pubblica nella pagina della sua classe (nome, tipo, regioni, classe, url, formato, pagine, kb, byte), poi",
              "`python3 scripts/aggiorna-documenti-unici.py --nome \"Prodotto\"` cerca la sua sintesi europea; se il",
              "Ministero non ha ancora pubblicato il disciplinare, la voce entra senza file (`formato` vuoto) e rimanda",
              "alla pagina della classe. Di un file aggiornato si riapre il PDF e nei dati si riscrivono pagine, kb e byte.",
              "Un file sostituito compare due volte: fra i tolti il vecchio indirizzo, fra i nuovi l'allegato comparso;",
              "nei dati cambia l'indirizzo, preso dalla pagina del Ministero. Una voce si toglie dal catalogo solo se la",
              "registrazione è stata cancellata o se il Ministero non pubblica più il disciplinare. Ogni indirizzo si",
              "verifica con una richiesta vera, mai indovinato.", ""]
    return righe


def rapporto(documenti, catalogo, con_rete, anche_file, rete_saltata=False):
    n_doc = len(tutti_i_documenti(documenti))
    n_pdf = sum(1 for v in catalogo["voci"] if v["formato"] == "pdf")
    n_ue = sum(len(collegamenti_europei(v)) for v in catalogo["voci"])
    fatto = ("dati" + (", documenti, pagine del Ministero, registro europeo e archivio dell'UE" if con_rete else "")
             + (", inizio di ogni PDF del catalogo" if anche_file else ""))
    righe = ["## Cucina in emergenza: controllo dei collegamenti", "",
             f"Documenti: {n_doc}. Disciplinari in PDF: {n_pdf}. Sintesi europee e rettifiche: {n_ue}. "
             f"Data scritta nei dati: {catalogo['verificato']}.",
             f"Controllo fatto: {fatto}."]
    if rete_saltata:
        righe.append("Le richieste ai siti non sono state fatte: i dati hanno gli errori elencati qui sotto, e vanno "
                     "corretti prima. Nessun collegamento è stato riaperto in questo giro.")
    if metodi:
        righe.append("PDF letti: " + ", ".join(f"{n} con {m}" for m, n in sorted(metodi.items())) + ".")
    if senza_browser:
        righe.append("Ripiego con il browser non disponibile in questo giro: " + "; ".join(senza_browser) + ".")
    righe += note_letture
    righe.append("")
    if con_rete:
        righe += righe_dei_disciplinari(anche_file)
    if errori:
        righe += ["### Collegamenti rotti o dati sbagliati", ""] + [f"- {e}" for e in errori] + [""]
    if non_letti:
        righe += ["### Fonti che non si sono fatte leggere", ""] + elenco_per_sito(non_letti) + [""]
    if protetti:
        righe += ["### Collegamenti non controllati: il sito chiede una verifica anti-bot", "",
                  "Il sito ha risposto alle richieste automatiche con una pagina di verifica o con un rifiuto. Non è un",
                  "collegamento rotto e la verifica non è stata aggirata: questi collegamenti restano da controllare, e la",
                  "data di verifica scritta nei dati non va oltre il giorno della loro ultima lettura riuscita.", ""]
        righe += [f"- {p}" for p in protetti] + [""]
    if muti:
        righe += ["### Collegamenti non controllati: il sito non ha risposto", "",
                  "Dalla macchina del controllo il sito ha dato tempo scaduto o un errore del server, oppure ha chiuso o",
                  "rifiutato la connessione. Non è detto che il collegamento sia rotto: va riaperto con una richiesta vera",
                  "da un'altra rete, e se non risponde per più settimane si tratta come rotto (regola sui guasti, punto 3).",
                  "La data di verifica scritta nei dati non va oltre il giorno della sua ultima lettura riuscita.", ""]
        righe += elenco_per_sito([(sito(m.rsplit(": ", 1)[-1]), m) for m in muti]) + [""]
    if protetti or muti:
        righe += ["Come si completa il controllo: lo si rilancia un altro giorno (Actions → «Cucina in emergenza: controllo",
                  "mensile dei collegamenti» → Run workflow), oppure si rileggono questi collegamenti da un'altra rete con",
                  f"`python3 scripts/{Path(__file__).name} --rete --browser --aggiorna-data` (con `--file` anche i PDF del",
                  f"catalogo). Lo script annota in `{FILE_LETTURE.relative_to(RADICE)}` il giorno di ogni lettura riuscita: le",
                  "letture fatte da reti diverse si sommano, e la data che il sito mostra è quella del collegamento letto da",
                  "più tempo. Poi una pull request con quel file e, se la data è cambiata, con i due file di dati. Se nel",
                  "rapporto non resta altro da lavorare, la issue si chiude a mano: il giro del mese dopo ne apre una nuova",
                  "solo se serve.", ""]
    gia_dette = {voce for voci in disciplinari.values() for voce in voci}  # stanno nella sezione dei disciplinari
    altre = [n for n in novita if n not in gia_dette]
    if altre:
        righe += ["### Novità sulle fonti, da valutare", ""] + [f"- {n}" for n in altre] + [""]
    if errori or non_letti or novita:
        righe += ["Come si lavora: l'indirizzo nuovo si prende dalla pagina dell'ente e si verifica con una richiesta",
                  "vera, mai indovinato (regola sui guasti); poi si aggiornano `data/cucina_emergenza.yaml` o",
                  "`data/disciplinari.json`. Un allegato che non serve al catalogo si aggiunge a `allegati_noti` con il motivo.",
                  "Per le sintesi europee (pubblicazioni nuove nel registro, rettifiche nuove, fascicolo cambiato):",
                  "`python3 scripts/aggiorna-documenti-unici.py`, che rilegge i soli prodotti cambiati e riscrive i dati;",
                  "poi la build e questo controllo con `--public public`. Lo script non fa arretrare da solo ciò che il",
                  "sito già mostra (una sintesi più vecchia, una rettifica in meno): lo elenca sotto «Da guardare», e chi",
                  "ha guardato lo accetta lanciandolo per quel prodotto, con `--nome \"Prodotto\"`.", ""]
    elif not protetti and not muti:
        righe += ["Nessun problema.", ""]
    firma = hashlib.sha256("\n".join(sorted(errori + [t for _, t in non_letti] + protetti + muti + novita)).encode("utf-8")).hexdigest()[:16]
    righe.append(f"<!-- firma-guasti:{firma} -->")
    return "\n".join(righe) + "\n"


def letture_scritte():
    """Le letture già annotate, {indirizzo: giorno}. Vuoto se il file non c'è o non si legge."""
    try:
        letture = json.loads(FILE_LETTURE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as e:
        print(f"Avviso: {FILE_LETTURE.name} non si legge ({type(e).__name__}): le letture ripartono da questo giro.",
              file=sys.stderr)
        return {}
    return letture if isinstance(letture, dict) else {}


def annota_letture(documenti, catalogo, oggi, altre=None):
    """Scrive in FILE_LETTURE il giorno dell'ultima lettura riuscita di ogni collegamento, da qualunque rete: il
    più recente fra `oggi` (per i collegamenti letti in questo giro), il giorno già scritto e quello di `altre`
    (le letture di un altro giro, da sommare). I collegamenti usciti dai dati si tolgono. Restituisce
    (giorno, quali): il giorno più vecchio fra tutti, cioè la data da cui ogni collegamento è stato riletto
    almeno una volta, con i collegamenti fermi a quel giorno; (None, quali) se qualcuno non è mai stato letto.
    Un giorno scritto male o nel futuro vale come lettura mai fatta."""
    prima, altre = letture_scritte(), altre or {}
    letture, mai = {}, []
    for url in dict.fromkeys(collegamenti_da_leggere(documenti, catalogo)):
        giorni = [g for g in (oggi if url in letti else None, prima.get(url), altre.get(url)) if giorno_di_lettura(g)]
        if giorni:
            letture[url] = max(giorni)
        else:
            mai.append(url)
    testo = json.dumps(letture, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
    try:
        uguale = FILE_LETTURE.read_text(encoding="utf-8") == testo
    except (OSError, ValueError):
        uguale = False
    if not uguale:
        FILE_LETTURE.parent.mkdir(parents=True, exist_ok=True)
        provvisorio = FILE_LETTURE.with_name(FILE_LETTURE.name + ".tmp")
        try:
            provvisorio.write_text(testo, encoding="utf-8")
            os.replace(provvisorio, FILE_LETTURE)  # o tutto il file o niente: mai un elenco a metà
        finally:
            provvisorio.unlink(missing_ok=True)
    if mai:
        return None, mai
    fermo = min(letture.values(), default=None)
    return fermo, [url for url, quando in letture.items() if quando == fermo]


def aggiorna_verifica(documenti, catalogo, oggi=None, altre=None):
    """Annota le letture del giro (o somma quelle di `altre`) e porta la data di verifica dei due file di dati
    al giorno da cui ogni collegamento è stato riletto. Mai indietro, e mai avanti se un collegamento non è mai
    stato letto. `oggi` è il giorno in cui il giro è cominciato: un giro a cavallo della mezzanotte non
    annota letture con il giorno dopo."""
    oggi = oggi or oggi_in_italia().isoformat()
    fermo, quali = annota_letture(documenti, catalogo, oggi, altre)
    dove = f"`{FILE_LETTURE.relative_to(RADICE)}`"
    note_letture.append(f"Letture annotate in {dove}: {len(letti)} collegamenti letti in questo giro." if altre is None else
                        f"Letture sommate a quelle di {dove}: per ogni collegamento vale il giorno più recente.")
    primi = ", ".join(quali[:3]) + (f" e altri {len(quali) - 3}" if len(quali) > 3 else "")
    if fermo is None:
        note_letture.append(f"La data di verifica non cambia: {len(quali)} collegamenti non risultano mai letti ({primi}).")
        return
    scritte = str(documenti.get("verificato", "")), str(catalogo.get("verificato", ""))
    if fermo > min(scritte):
        aggiorna_data(fermo)
        documenti["verificato"], catalogo["verificato"] = max(scritte[0], fermo), max(scritte[1], fermo)
    if fermo < oggi:
        note_letture.append(f"Ogni collegamento è stato riletto dal {giorno(fermo)} in poi: la data di verifica non può "
                            f"andare oltre. Letti l'ultima volta quel giorno: {primi}.")
    elif altre is None and set(collegamenti_da_leggere(documenti, catalogo)) <= letti:
        note_letture.append("Ogni collegamento è stato letto in questo giro.")
    else:
        note_letture.append("Ogni collegamento ha una lettura di oggi, di questo giro o di un altro: ciò che qui sotto è "
                            "«non controllato» è stato letto oggi da un'altra rete.")


def unisci_letture(documenti, catalogo, percorso):
    """--unisci-letture: somma alle letture annotate quelle di un altro file, senza rete. Lo usa il workflow per
    salvare le letture di un giro sopra l'ultimo main: se nel frattempo una pull request ha annotato altre
    letture, per ogni collegamento resta il giorno più recente, e nessuna delle due si perde."""
    try:
        altre = json.loads(Path(percorso).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        errori.append(f"--unisci-letture: {percorso} non si legge ({type(e).__name__})")
        return
    if not isinstance(altre, dict):
        errori.append(f"--unisci-letture: {percorso} deve essere una mappa indirizzo → giorno")
        return
    aggiorna_verifica(documenti, catalogo, altre=altre)


def aggiorna_data(quando):
    """Porta al giorno `quando` (AAAA-MM-GG) la data «verificato» dei due file di dati, dove è più vecchia: una
    data non torna mai indietro."""
    da_scrivere = []
    for percorso, modello in ((FILE_DOCUMENTI, r'(?m)^verificato: "(\d{4}-\d{2}-\d{2})"'),
                              (FILE_CATALOGO, r'(?m)^  "verificato": "(\d{4}-\d{2}-\d{2})"')):
        testo = percorso.read_text(encoding="utf-8")
        trovata = re.search(modello, testo)
        if not trovata:
            sys.exit(f"{percorso.name}: riga «verificato» non trovata, data non aggiornata in nessuno dei due file")
        if trovata.group(1) < quando:
            da_scrivere.append((percorso, testo[:trovata.start(1)] + quando + testo[trovata.end(1):]))
    for percorso, cambiato in da_scrivere:  # solo dopo aver preparato entrambi: mai una data scritta e l'altra no
        percorso.write_text(cambiato, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--public", metavar="CARTELLA", help="controlla anche le pagine costruite da Hugo")
    ap.add_argument("--eta", type=int, metavar="GIORNI",
                    help="errore se la data di verifica dei collegamenti ha più di GIORNI giorni")
    ap.add_argument("--rete", action="store_true", help="richieste vere a documenti e pagine del Ministero")
    ap.add_argument("--file", action="store_true", help="con --rete: chiede anche l'inizio di ogni PDF del catalogo")
    ap.add_argument("--browser", action="store_true", help="con --rete: riprova con Chromium ciò che non si legge")
    ap.add_argument("--rapporto", metavar="FILE", help="scrive il rapporto in Markdown")
    ap.add_argument("--aggiorna-data", action="store_true",
                    help="con --rete: annota il giorno di ogni lettura riuscita e porta la data di verifica dei dati "
                         "al giorno da cui ogni collegamento è stato riletto")
    ap.add_argument("--unisci-letture", metavar="FILE",
                    help="senza rete: somma alle letture annotate quelle di FILE (per ogni collegamento vale il giorno "
                         "più recente) e riporta la data di verifica; lo usa il workflow per salvare un giro sull'ultimo main")
    args = ap.parse_args()
    if (args.file or args.browser or args.aggiorna_data) and not args.rete:
        ap.error("--file, --browser e --aggiorna-data valgono solo con --rete")
    if args.unisci_letture and args.rete:
        ap.error("--unisci-letture lavora senza rete: non va insieme a --rete")
    documenti, catalogo = carica()
    controlla_dati(documenti, catalogo)
    # con i dati malformati l'elenco dei collegamenti non si sa costruire
    senza_lettura = controlla_letture(documenti, catalogo) if not errori else []
    if args.eta is not None:
        controlla_eta(documenti, catalogo, args.eta)
    if args.public:
        controlla_pagine(args.public, documenti, catalogo)
    if args.unisci_letture and not errori:
        unisci_letture(documenti, catalogo, args.unisci_letture)
    elif senza_lettura and not args.rete:
        primi = ", ".join(senza_lettura[:3]) + (f" e altri {len(senza_lettura) - 3}" if len(senza_lettura) > 3 else "")
        note_letture.append(f"Avviso: {len(senza_lettura)} collegamenti dei dati non hanno una lettura annotata ({primi}): "
                            f"la data di verifica non avanza finché non si leggono con `--rete --aggiorna-data` "
                            f"(con `--file` per i PDF del catalogo).")
    rete_fatta = args.rete and not errori  # con i dati sbagliati non si interrogano i siti: prima si correggono
    if rete_fatta:
        global scadenza
        scadenza = time.time() + TEMPO_RICHIESTE
        inizio = oggi_in_italia().isoformat()  # le letture portano il giorno in cui il giro è cominciato
        controlla_rete(documenti, catalogo, args.file)
        chiudi_da_rivedere(args.browser)
        if args.file:
            confronta_pesi(catalogo)
        segnala_controllo_mancato(collegamenti_da_aprire(documenti, catalogo, args.file))
        if args.aggiorna_data and not errori and not non_letti:
            # un collegamento rotto o una fonte non letta: nessuna lettura si annota, la data resta com'è
            aggiorna_verifica(documenti, catalogo, inizio)
    testo = rapporto(documenti, catalogo, rete_fatta, rete_fatta and args.file, rete_saltata=args.rete and not rete_fatta)
    if args.rapporto:
        Path(args.rapporto).write_text(testo, encoding="utf-8")
    print(testo)
    return 1 if errori else 2 if non_letti else 3 if novita or protetti or muti else 0


if __name__ == "__main__":
    sys.exit(main())
