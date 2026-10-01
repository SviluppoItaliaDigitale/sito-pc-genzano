#!/usr/bin/env python3
"""Controllo settimanale delle copie dei nostri articoli.

Perché esiste (01/10/2026): i testi del sito sono redazione originale del
Gruppo, rilasciati in CC BY 4.0 (attribuzione obbligatoria). Capita che un
articolo venga ripreso parola per parola, con o senza fonte. Accorgersene a
mano vuol dire cercare frase per frase su più motori ogni settimana: questo
script fa la parte automatizzabile e prepara il resto.

Tre parti, che finiscono nella stessa issue:

  1) FEED DELLE TESTATE. Legge i feed RSS pubblici delle testate locali
     (TESTATE: Castelli Romani, Roma, litorale e Pontino), prende le notizie
     degli ultimi GIORNI_FEED giorni (sui feed WordPress anche le pagine
     successive, `?paged=2`..., fino a PAGINE_FEED_WP pagine e
     TEMPO_FEED_TESTATA_S secondi per testata: per le testate più attive la
     finestra coperta può essere più corta, e l'issue dice da quando parte),
     scarica le pagine e le confronta con i nostri
     articoli usciti negli ultimi GIORNI_NOSTRI giorni. Il confronto è per
     frammenti di 8 parole consecutive, normalizzate (minuscole, senza
     punteggiatura): una notizia è segnalata quando condivide almeno
     SOGLIA_FRAMMENTI frammenti con un nostro articolo. Si dice anche se nella
     pagina compare un link o una citazione a protezionecivilegenzano.it: in
     quel caso la ripresa è «con fonte».
     Il testo del feed (content:encoded, quando c'è) si confronta sempre, anche
     per le notizie oltre il tetto delle pagine scaricate. Le pagine da
     scaricare per prime sono quelle i cui titoli e sommari hanno più parole in
     comune con i nostri articoli recenti, alternando le testate. Limiti:
     MAX_PAGINE in tutto, MAX_PER_TESTATA per testata, almeno PAUSA_DOMINIO_S
     secondi fra due richieste allo stesso dominio, TEMPO_PAGINE_S di tempo.

  2) GOOGLE NEWS. Per ogni nostro articolo degli ultimi GIORNI_ASSISTITA
     giorni sceglie due frasi caratteristiche del corpo (12-25 parole, non
     titoli, elenchi, citazioni o frasi con link; preferite quelle con numeri,
     nomi di luogo e dettagli) e le cerca come frase esatta nel feed RSS
     pubblico di Google News (news.google.com/rss/search, lo stesso canale di
     normativa-watcher.py). Copre le testate indicizzate da Google News anche
     oltre la finestra dei feed. I risultati del nostro dominio si scartano.
     Al massimo MAX_QUERY_GNEWS ricerche per giro, PAUSA_GNEWS_S secondi l'una
     dall'altra; un 429 o 503 chiude la serie. Solo il feed RSS di Google News:
     le pagine dei risultati di Google Search non si interrogano, le loro
     condizioni d'uso lo vietano.

  3) RICERCA ASSISTITA. Le stesse frasi, con i link di ricerca esatta su
     Google, Bing e DuckDuckGo (escluso il nostro dominio), da aprire a mano:
     coprono il web oltre le testate giornalistiche.

Filtro dei frammenti comuni (per non segnalare ciò che chiunque scrive):
  - si scarta un frammento che contiene un numero di emergenza o di servizio
    (112, 803 555, 1530, 115, 118...): «chiama il 112» non è una copia;
  - si scarta un frammento con meno di 3 parole «di contenuto», cioè fuori
    dall'elenco PAROLE_COMUNI: articoli, preposizioni, ausiliari, i nomi di
    enti ripetuti ovunque (protezione civile, regione Lazio, Polizia Locale,
    Dipartimento...) e i nomi dei comuni dei Castelli, che negli elenchi
    («Genzano, Lanuvio, Nemi, Rocca di Papa...») tutti scrivono uguali;
  - si scarta un frammento che compare in 3 o più dei nostri articoli: è una
    nostra formula ricorrente (avvertenze, disclaimer normativi, chiusure);
  - dei nostri articoli si confronta il corpo fino a «Per approfondire», più
    le didascalie delle foto; frontmatter, shortcode e link restano fuori.

Lo user agent dice chi siamo ma comincia con «Mozilla/5.0 (compatible; ...)»:
nella verifica del 01/10/2026 alcune testate (Aprilianews, Velletri Life)
rifiutavano con 403 un user agent senza quel prefisso.

    python3 scripts/controllo-copie.py [--dry-run] [--issue-body FILE.md] [--senza-gnews]

Con --dry-run legge feed, pagine e Google News e stampa l'esito, senza
scrivere file salvo --issue-body. Esce sempre con 0: una testata, una pagina
o una ricerca che non risponde si salta e si annota.

Solo libreria standard.
"""

from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import html
import http.client
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import social_comune as S  # noqa: E402

UA = "Mozilla/5.0 (compatible; PCGenzanoControlloCopie/1.0; +https://www.protezionecivilegenzano.it/)"
DOMINIO = "protezionecivilegenzano.it"

# ──────────────────────────────────────────────────────────────
# Testate locali con un feed RSS funzionante
# ──────────────────────────────────────────────────────────────
# Ogni voce: nome, indirizzo del feed, zona, e `wp=True` se il feed è di
# WordPress (accetta `?paged=2`, `?paged=3`... per andare indietro nel tempo:
# i feed WordPress mostrano di solito solo le ultime 10 notizie, che per una
# testata attiva sono poche ore).
#
# Per aggiungere una testata: verificare che il feed risponda con notizie
# recenti (curl -sSL -A "<UA sopra>" <feed> | grep -m3 pubDate), poi una riga
# qui. Elenco verificato il 01/10/2026.
#
# Provate e lasciate fuori il 01/10/2026, da riprovare ogni tanto:
#   - Il Giornale dei Castelli Romani (giornaleinfocastelliromani.it):
#     /feed/ e ?feed=rss2 rimandano alla home page, il feed è disattivato;
#   - Cronache Cittadine (cronachecittadine.it): la home dichiara /feed/, che
#     risponde 403;
#   - Velletri Life (velletrilife.it): 403, poi connessione interrotta;
#   - La Spunta (laspunta.it), Il Metropolitano (ilmetropolitano.it), Abitare
#     a Roma (abitarearoma.it): dichiarano /feed/ ma la connessione si
#     interrompe;
#   - Il Corriere della Città: il feed risponde ma è fermo a luglio 2026;
#   - Pomezianews: feed fermo al 2025;
#   - Latina Oggi: /rss è una pagina HTML, non un feed;
#   - Cinque Quotidiano, Latina Quotidiano: pagina di verifica anti-bot.
# Castelli News, Il Tuscolo, Il Giornale dei Castelli e altri nomi cercati non
# hanno risposto affatto (dominio inesistente o certificato non valido).
TESTATE = (
    # Castelli Romani
    {"nome": "Castelli Notizie", "feed": "https://www.castellinotizie.it/feed/", "zona": "Castelli Romani", "wp": True},
    # Dal 01/10/2026 il feed risponde (verificato da fuori), ma da alcune reti
    # la connessione viene interrotta: in quel caso lo script lo annota.
    {"nome": "Il Mamilio", "feed": "https://www.ilmamilio.it/wp/feed/", "zona": "Castelli Romani", "wp": True},
    {"nome": "Il Caffè", "feed": "https://www.ilcaffe.tv/feed/", "zona": "Castelli Romani e litorale", "wp": True},
    {"nome": "Controluce", "feed": "https://www.controluce.it/feed/", "zona": "Castelli Romani e Monti Prenestini", "wp": True},
    {"nome": "Terzo Binario", "feed": "https://www.terzobinario.it/feed/", "zona": "Roma sud-est e Castelli", "wp": True},
    # Roma
    {"nome": "RomaToday", "feed": "https://www.romatoday.it/rss", "zona": "Roma", "wp": False},
    {"nome": "RomaDailyNews", "feed": "https://www.romadailynews.it/feed/", "zona": "Roma", "wp": True},
    {"nome": "RomaIT", "feed": "https://www.romait.it/feed", "zona": "Roma", "wp": True},
    {"nome": "Il Quotidiano del Lazio", "feed": "https://www.ilquotidianodellazio.it/feed/", "zona": "Lazio", "wp": True},
    # Litorale e Pontino
    {"nome": "Il Faro on line", "feed": "https://www.ilfaroonline.it/feed/", "zona": "Ostia e Fiumicino", "wp": True},
    {"nome": "Il Granchio", "feed": "https://www.ilgranchio.it/feed/", "zona": "Anzio e Nettuno", "wp": True},
    {"nome": "InLiberaUscita", "feed": "https://www.inliberauscita.it/feed/", "zona": "Anzio e Nettuno", "wp": True},
    {"nome": "Aprilianews", "feed": "https://www.aprilianews.it/feed/", "zona": "Aprilia", "wp": True},
    {"nome": "LatinaToday", "feed": "https://www.latinatoday.it/rss", "zona": "Latina", "wp": False},
    {"nome": "Latina Corriere", "feed": "https://www.latinacorriere.it/feed/", "zona": "Latina", "wp": True},
    {"nome": "H24 Notizie", "feed": "https://www.h24notizie.com/feed/", "zona": "Provincia di Latina", "wp": True},
)

GIORNI_FEED = 14
GIORNI_NOSTRI = 30
GIORNI_ASSISTITA = 14
GIORNI_FORMULE = 180      # finestra in cui si cercano le nostre formule ricorrenti
PAGINE_FEED_WP = 30       # pagine di feed WordPress per testata (10 notizie l'una):
                          # una testata attiva ne pubblica una trentina al giorno
TEMPO_FEED_TESTATA_S = 45 # tempo massimo per sfogliare il feed di una testata
MAX_PAGINE = 240          # pagine di notizie scaricate in tutto
MAX_PER_TESTATA = 20      # ... e per singola testata
PAUSA_DOMINIO_S = 1.5     # fra due richieste allo stesso dominio
TEMPO_PAGINE_S = 15 * 60  # oltre questo tempo si smette di scaricare pagine
TIMEOUT_S = 25
MAX_QUERY_GNEWS = 60
PAUSA_GNEWS_S = 3
TEMPO_GNEWS_S = 8 * 60    # tetto di tempo delle ricerche: il job ha 40 minuti
GOOGLE_NEWS = "https://news.google.com/rss/search?q={q}&hl=it&gl=IT&ceid=IT:it"
N = 8                     # parole per frammento
SOGLIA_FRAMMENTI = 3
SOGLIA_FORMULA = 3        # un frammento in 3+ nostri articoli è una formula
MAX_CORPO = 60_000        # caratteri; GitHub accetta al massimo 65.536

NUMERI_SERVIZIO = frozenset({"112", "113", "115", "118", "1515", "1530", "803", "555"})

PAROLE_COMUNI = frozenset("""
il lo la i gli le l un uno una di a da in con su per tra fra del dello della
dei degli delle al allo alla ai agli alle dal dallo dalla dai dagli dalle nel
nello nella nei negli nelle col coi sul sullo sulla sui sugli sulle e ed o od
ma anche come che chi cui non se si ci vi ne è e ha hanno ho sono era erano
essere stato stata stati state sia siano fa fare può possono deve devono più
meno molto poco già ancora quando dove questo questa questi queste
quello quella quelli quelle suo sua suoi sue loro nostro nostra nostri nostre
tutto tutti tutta tutte ogni altro altra altri altre stesso stessa so sa
protezione civile gruppo comunale volontari volontario volontaria volontarie
roma regione lazio comune comuni città sindaco polizia locale
carabinieri vigili fuoco dipartimento nazionale regionale provinciale
metropolitana castelli romani centro funzionale sala operativa servizio
numero unico emergenza emergenze europeo chiama chiamare chiamate
genzano ariccia albano laziale castel gandolfo nemi lanuvio velletri lariano
marino frascati grottaferrata rocca papa priora monte compatri porzio catone
colonna ciampino artena montecompatri cecchina pavona landi
""".split())

MOTORI = (
    ("Google", "https://www.google.com/search?q="),
    ("Bing", "https://www.bing.com/search?q="),
    ("DuckDuckGo", "https://duckduckgo.com/?q="),
)


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


# ──────────────────────────────────────────────────────────────
# Testo
# ──────────────────────────────────────────────────────────────

def parole(testo: str) -> list[str]:
    """Minuscole, apostrofi e punteggiatura come spazi, accenti conservati
    (gli stessi per noi e per le testate, quindi il confronto regge)."""
    t = unicodedata.normalize("NFC", html.unescape(testo)).lower()
    t = t.replace("’", " ").replace("'", " ")
    return re.findall(r"[0-9a-zàèéìíòóùú]+", t)


def frammenti(tok: list[str]) -> dict[str, int]:
    """Frammento → posizione della sua prima parola."""
    out: dict[str, int] = {}
    for i in range(len(tok) - N + 1):
        out.setdefault(" ".join(tok[i:i + N]), i)
    return out


def frammento_utile(fr: str) -> bool:
    tok = fr.split()
    if any(t in NUMERI_SERVIZIO for t in tok):
        return False
    return sum(1 for t in tok if t not in PAROLE_COMUNI) >= 3


def corpo_articolo(path: Path) -> str:
    """Corpo in testo semplice, fino a «Per approfondire», con le didascalie."""
    try:
        _, body = S.parse_frontmatter(path.read_text(encoding="utf-8"))
    except OSError:
        return ""
    m = re.search(r"^#{2,3}\s+Per approfondire", body, flags=re.M | re.I)
    if m:
        body = body[:m.start()]
    didascalie = re.findall(r'caption="([^"]*)"', body)
    body = re.sub(r"\{\{[<%].*?[>%]\}\}", " ", body, flags=re.S)
    body = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", body)
    body = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", body)
    body = re.sub(r"<[^>]+>", " ", body)
    body = re.sub(r"[*_`]+", "", body)
    return body + "\n\n" + "\n\n".join(didascalie)


class _Testo(HTMLParser):
    """Testo visibile di una pagina, senza script e stili."""

    SALTA = {"script", "style", "noscript", "template", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parti: list[str] = []
        self._salta = 0

    def handle_starttag(self, tag, attrs):
        if tag in self.SALTA:
            self._salta += 1

    def handle_endtag(self, tag):
        if tag in self.SALTA and self._salta:
            self._salta -= 1

    def handle_data(self, data):
        if not self._salta:
            self.parti.append(data)


def testo_html(sorgente: str) -> str:
    p = _Testo()
    try:
        p.feed(sorgente)
    except Exception:  # noqa: BLE001 — HTML malformato: si tiene quello che c'è
        pass
    return " ".join(p.parti)


RE_CORNICE = re.compile(r"<(header|nav|footer|aside)\b.*?</\1\s*>", flags=re.S | re.I)


def regione_articolo(sorgente: str) -> str:
    """Il contenuto della notizia, senza menu, barre laterali e piè di pagina:
    un link al nostro sito lì non dice nulla su questa notizia. Si prende il
    blocco <article> più lungo, anche se breve (una notizia di poche righe resta
    una notizia); senza <article> si toglie la cornice dalla pagina intera."""
    blocchi = re.findall(r"<article\b.*?</article>", sorgente, flags=re.S | re.I)
    if blocchi:
        return max(blocchi, key=len)
    return RE_CORNICE.sub(" ", sorgente)


# ──────────────────────────────────────────────────────────────
# Rete
# ──────────────────────────────────────────────────────────────

class TroppeRichieste(Exception):
    """Il servizio ha risposto 429 o 503: la serie di richieste finisce qui."""


_ultima_richiesta: dict[str, float] = {}


def scarica(url: str) -> str:
    """GET con pausa minima per dominio. Solleva TroppeRichieste su 429/503."""
    host = urllib.parse.urlsplit(url).hostname or ""
    dominio = ".".join(host.split(".")[-2:])
    attesa = _ultima_richiesta.get(dominio, 0) + PAUSA_DOMINIO_S - time.monotonic()
    if attesa > 0:
        time.sleep(attesa)
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/rss+xml,application/xml;q=0.9,*/*;q=0.5",
        "Accept-Language": "it-IT,it;q=0.9",
    })
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
            dati = r.read(5_000_000)
            cs = r.headers.get_content_charset() or "utf-8"
    except urllib.error.HTTPError as e:
        if e.code in (429, 503):
            raise TroppeRichieste(f"HTTP {e.code}") from e
        raise
    except http.client.HTTPException as e:
        # IncompleteRead e simili non sono OSError: senza questa conversione
        # una risposta troncata interromperebbe l'intera parte dei feed.
        raise OSError(f"{type(e).__name__}") from e
    finally:
        _ultima_richiesta[dominio] = time.monotonic()
    try:
        return dati.decode(cs, "replace")
    except LookupError:  # charset dichiarato inesistente
        return dati.decode("utf-8", "replace")


def _data_feed(s: str) -> dt.datetime | None:
    s = (s or "").strip()
    if not s:
        return None
    try:
        d = email.utils.parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            d = dt.datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=dt.timezone.utc)
    return d


def voci_feed(xml: str) -> list[dict]:
    """Voci di un feed RSS 2.0 o Atom: titolo, link, data, testo, fonte."""
    try:
        radice = ET.fromstring(xml.encode("utf-8"))
    except ET.ParseError:
        return []
    out = []
    atom = "{http://www.w3.org/2005/Atom}"
    for it in radice.iter("item"):
        fonte = it.find("source")
        out.append({
            "titolo": (it.findtext("title") or "").strip(),
            "link": (it.findtext("link") or "").strip(),
            "data": _data_feed(it.findtext("pubDate") or it.findtext("{http://purl.org/dc/elements/1.1/}date") or ""),
            "sommario": it.findtext("description") or "",
            "contenuto": it.findtext("{http://purl.org/rss/1.0/modules/content/}encoded") or "",
            "fonte": (fonte.text or "").strip() if fonte is not None else "",
            "fonte_url": (fonte.get("url") or "") if fonte is not None else "",
        })
    for it in radice.iter(f"{atom}entry"):
        link = it.find(f"{atom}link")
        out.append({
            "titolo": (it.findtext(f"{atom}title") or "").strip(),
            "link": (link.get("href") if link is not None else "") or "",
            "data": _data_feed(it.findtext(f"{atom}published") or it.findtext(f"{atom}updated") or ""),
            "sommario": it.findtext(f"{atom}summary") or "",
            "contenuto": it.findtext(f"{atom}content") or "",
            "fonte": "", "fonte_url": "",
        })
    return out


def notizie_testata(t: dict, limite: dt.datetime) -> tuple[list[dict], int]:
    """Notizie della testata dopo `limite`, sfogliando il feed WordPress
    finché le notizie restano nella finestra. Torna anche le pagine lette."""
    pagine = PAGINE_FEED_WP if t["wp"] else 1
    voci: list[dict] = []
    visti: set[str] = set()
    lette = 0
    scadenza = time.monotonic() + TEMPO_FEED_TESTATA_S
    for n in range(1, pagine + 1):
        if n > 1 and time.monotonic() > scadenza:
            break
        url = t["feed"] if n == 1 else t["feed"] + ("&" if "?" in t["feed"] else "?") + f"paged={n}"
        try:
            nuove = voci_feed(scarica(url))
            if n == 1 and not nuove:
                raise ValueError("feed vuoto o non leggibile")
        except (urllib.error.URLError, OSError, ValueError, TroppeRichieste):
            if n == 1:
                raise
            break
        lette += 1
        nuove = [v for v in nuove if v["link"] and v["link"] not in visti]
        if not nuove:
            break
        visti.update(v["link"] for v in nuove)
        voci += nuove
        # Feed in ordine cronologico inverso: una notizia fuori finestra vuol
        # dire che le pagine successive sono tutte più vecchie.
        if any(v["data"] and v["data"] < limite for v in nuove):
            break
    return [v for v in voci if v["data"] is None or v["data"] >= limite], lette


# ──────────────────────────────────────────────────────────────
# I nostri articoli
# ──────────────────────────────────────────────────────────────

def nostri_articoli(ora: dt.datetime) -> tuple[list[dict], set[str]]:
    """Articoli degli ultimi GIORNI_NOSTRI giorni con i loro frammenti utili,
    e l'insieme delle nostre formule ricorrenti."""
    conteggio: Counter = Counter()
    per_articolo = []
    limite = ora - dt.timedelta(days=GIORNI_NOSTRI)
    for path, fm, online in S.articoli(finestra_ore=GIORNI_FORMULE * 24, ora=ora):
        testo = corpo_articolo(path)
        fr = set(frammenti(parole(testo)))
        conteggio.update(fr)
        if online >= limite:
            per_articolo.append({
                "slug": path.stem, "titolo": S.testo_campo(fm, "title") or path.stem,
                "online": online, "testo": testo, "frammenti": fr,
            })
    formule = {f for f, n in conteggio.items() if n >= SOGLIA_FORMULA}
    for a in per_articolo:
        a["frammenti"] = {f for f in a["frammenti"] if f not in formule and frammento_utile(f)}
    return per_articolo, formule


# ──────────────────────────────────────────────────────────────
# Parte 1: feed delle testate
# ──────────────────────────────────────────────────────────────

def _spezzoni(tok: list[str], posizioni: list[int]) -> list[str]:
    """Frammenti contigui o sovrapposti uniti in spezzoni di testo leggibili."""
    spezzoni: list[list[int]] = []
    for p in sorted(set(posizioni)):
        if spezzoni and p <= spezzoni[-1][1]:
            spezzoni[-1][1] = max(spezzoni[-1][1], p + N)
        else:
            spezzoni.append([p, p + N])
    spezzoni.sort(key=lambda s: s[1] - s[0], reverse=True)
    return [" ".join(tok[a:b]) for a, b in spezzoni]


def confronta(testo: str, indice: dict[str, set[str]]) -> dict[str, tuple[int, list[str]]]:
    """Slug dei nostri articoli → (frammenti condivisi, spezzoni di testo),
    solo sopra soglia."""
    tok = parole(testo)
    per_slug: dict[str, list[int]] = defaultdict(list)
    for fr, pos in frammenti(tok).items():
        for slug in indice.get(fr, ()):
            per_slug[slug].append(pos)
    return {slug: (len(pos), _spezzoni(tok, pos))
            for slug, pos in per_slug.items() if len(pos) >= SOGLIA_FRAMMENTI}


def uscita_prima(data_notizia: dt.datetime | None, nostro: dt.datetime | None) -> bool:
    """Vero solo se la notizia esterna è di un giorno precedente al nostro.
    La data dei nostri articoli è il giorno (mezzanotte, o 00:01, 00:02…),
    mentre la pagina va online al primo deploy utile: dentro lo stesso giorno
    l'ordine non si conosce, e non si dichiara una precedenza che non si sa."""
    if not data_notizia or not nostro:
        return False
    return data_notizia.astimezone(S.TZ).date() < nostro.astimezone(S.TZ).date()


def parte_feed(nostri: list[dict], ora: dt.datetime) -> dict:
    indice: dict[str, set[str]] = defaultdict(set)
    parole_nostre: set[str] = {"genzano"}
    for a in nostri:
        for fr in a["frammenti"]:
            indice[fr].add(a["slug"])
        parole_nostre.update(t for t in parole(a["titolo"]) if len(t) >= 5 and t not in PAROLE_COMUNI)

    esito = {"testate": [], "senza_risposta": [], "trovate": [], "pagine": 0, "pagine_ko": [],
             "notizie": 0, "solo_feed": 0}
    limite = ora - dt.timedelta(days=GIORNI_FEED)
    per_testata: dict[str, list[dict]] = {}
    for t in TESTATE:
        try:
            recenti, lette = notizie_testata(t, limite)
        except (urllib.error.URLError, OSError, ValueError, TroppeRichieste) as e:
            esito["senza_risposta"].append(f"{t['nome']} ({t['feed']}): {type(e).__name__}: {str(e)[:90]}")
            log(f"{t['nome']}: feed non raggiungibile ({e})")
            continue
        date = [v["data"] for v in recenti if v["data"]]
        dal = S.fmt(min(date)) if date else "?"
        esito["testate"].append(f"{t['nome']} ({t['zona']}): {len(recenti)} notizie dal {dal}, "
                                f"{lette} pagine di feed")
        log(f"{t['nome']}: {len(recenti)} notizie dal {dal} ({lette} pagine di feed)")
        for v in recenti:
            v["testata"] = t["nome"]
            # Il testo del feed si confronta subito, senza scaricare nulla.
            v["dal_feed"] = confronta(testo_html(v["contenuto"] or v["sommario"]), indice)
            v["fonte_feed"] = DOMINIO in (v["contenuto"] + v["sommario"]).lower()
            v["punteggio"] = (100 if v["dal_feed"] else 0) + len(
                parole_nostre & set(parole(v["titolo"] + " " + testo_html(v["sommario"]))))
        recenti.sort(key=lambda v: v["punteggio"], reverse=True)
        per_testata[t["nome"]] = recenti
        esito["notizie"] += len(recenti)

    # Coda di download: le più promettenti prima, alternando le testate.
    ordine: list[tuple[dict, bool]] = []
    code = {n: list(v) for n, v in per_testata.items()}
    quante: Counter = Counter()
    while any(code.values()):
        for nome in list(code):
            if code[nome]:
                v = code[nome].pop(0)
                da_scaricare = quante[nome] < MAX_PER_TESTATA and sum(quante.values()) < MAX_PAGINE
                if da_scaricare:
                    quante[nome] += 1
                ordine.append((v, da_scaricare))

    titoli = {a["slug"]: a["titolo"] for a in nostri}
    usciti = {a["slug"]: a["online"] for a in nostri}
    inizio = time.monotonic()
    for v, da_scaricare in ordine:
        risultati, con_fonte, da = v["dal_feed"], v["fonte_feed"], "sul testo del feed"
        if da_scaricare and time.monotonic() - inizio < TEMPO_PAGINE_S:
            try:
                sorgente = scarica(v["link"])
                esito["pagine"] += 1
                regione = regione_articolo(sorgente)
                dalla_pagina = confronta(testo_html(regione), indice)
                if dalla_pagina:
                    risultati, con_fonte, da = dalla_pagina, DOMINIO in regione.lower(), "sulla pagina"
            except (urllib.error.URLError, OSError, ValueError, TroppeRichieste) as e:
                esito["pagine_ko"].append(f"{v['testata']}: {v['link']} ({type(e).__name__})")
        else:
            esito["solo_feed"] += 1
        for slug, (n, spezzoni) in risultati.items():
            esito["trovate"].append({
                "testata": v["testata"], "titolo": v["titolo"], "link": v["link"],
                "data": v["data"], "slug": slug, "nostro_titolo": titoli.get(slug, slug),
                "frammenti": n, "spezzoni": spezzoni[:3], "con_fonte": con_fonte, "da": da,
                # Una notizia uscita prima del nostro articolo non lo ha
                # ripreso: il testo in comune viene da una fonte comune
                # (programma di un evento, comunicato di un ente).
                "precedente": uscita_prima(v["data"], usciti.get(slug)),
            })
    log(f"Pagine scaricate: {esito['pagine']}; notizie confrontate sul solo feed: {esito['solo_feed']}")
    return esito


# ──────────────────────────────────────────────────────────────
# Frasi caratteristiche (parti 2 e 3)
# ──────────────────────────────────────────────────────────────

def frasi_corpo(testo: str) -> list[str]:
    """Frasi dei paragrafi di prosa: niente titoli, elenchi, citazioni,
    tabelle, righe con link."""
    frasi = []
    for paragrafo in re.split(r"\n\s*\n", testo):
        righe = [r.strip() for r in paragrafo.strip().splitlines() if r.strip()]
        if not righe or any(re.match(r"^(#|[-*+] |\d+\. |>|\|)", r) for r in righe):
            continue
        prosa = " ".join(righe)
        if "http" in prosa or "](" in prosa:
            continue
        for f in re.split(r"(?<=[.!?])\s+(?=[A-ZÀÈÉÌÒÙ«\"])", prosa):
            f = f.strip()
            if 12 <= len(f.split()) <= 25:
                frasi.append(f)
    return frasi


def _punteggio_frase(f: str) -> int:
    parti = f.split()
    cifre = sum(1 for p in parti if re.search(r"\d", p))
    nomi = sum(1 for p in parti[1:] if p[:1].isupper())
    rare = sum(1 for t in parole(f) if len(t) >= 8 and t not in PAROLE_COMUNI)
    generico = any(t in NUMERI_SERVIZIO for t in parole(f))
    return 3 * cifre + 2 * nomi + rare - (10 if generico else 0)


def frasi_caratteristiche(nostri: list[dict], formule: set[str], ora: dt.datetime) -> list[dict]:
    limite = ora - dt.timedelta(days=GIORNI_ASSISTITA)
    out = []
    for a in nostri:
        if a["online"] < limite:
            continue
        candidate = []
        for f in frasi_corpo(a["testo"]):
            # Una frase che contiene una nostra formula ricorrente non
            # distingue questo articolo dagli altri.
            if any(fr in formule for fr in frammenti(parole(f))):
                continue
            if f not in candidate:
                candidate.append(f)
        candidate.sort(key=_punteggio_frase, reverse=True)
        out.append({"slug": a["slug"], "titolo": a["titolo"], "online": a["online"],
                    "frasi": candidate[:2]})
    out.sort(key=lambda a: a["online"], reverse=True)
    return out


def link_ricerca(frase: str) -> list[tuple[str, str]]:
    q = urllib.parse.quote_plus(f'"{frase}" -site:{DOMINIO}')
    return [(nome, base + q) for nome, base in MOTORI]


# ──────────────────────────────────────────────────────────────
# Parte 2: Google News
# ──────────────────────────────────────────────────────────────

def parte_gnews(articoli: list[dict]) -> dict:
    esito = {"query": 0, "trovate": [], "errori": [], "interrotta": "", "saltate": 0}
    visti: set[tuple[str, str]] = set()
    scadenza = time.monotonic() + TEMPO_GNEWS_S
    for a in articoli:
        for f in a["frasi"]:
            if not esito["interrotta"] and time.monotonic() > scadenza:
                esito["interrotta"] = "tempo massimo delle ricerche raggiunto: le altre al prossimo giro"
                log(esito["interrotta"])
            if esito["interrotta"] or esito["query"] >= MAX_QUERY_GNEWS:
                esito["saltate"] += 1
                continue
            if esito["query"]:
                time.sleep(PAUSA_GNEWS_S)
            url = GOOGLE_NEWS.format(q=urllib.parse.quote(f'"{f}"'))
            esito["query"] += 1
            try:
                voci = voci_feed(scarica(url))
            except TroppeRichieste as e:
                esito["interrotta"] = f"Google News ha risposto {e}: ricerche sospese fino al prossimo giro"
                log(esito["interrotta"])
                continue
            except (urllib.error.URLError, OSError, ValueError) as e:
                esito["errori"].append(f"{type(e).__name__}")
                continue
            for v in voci:
                if DOMINIO in (v["fonte_url"] + v["link"]).lower():
                    continue
                chiave = (a["slug"], v["link"])
                if chiave in visti:
                    continue
                visti.add(chiave)
                titolo = v["titolo"]
                if v["fonte"] and titolo.endswith(" - " + v["fonte"]):
                    titolo = titolo[: -len(v["fonte"]) - 3]
                esito["trovate"].append({
                    "slug": a["slug"], "nostro_titolo": a["titolo"], "frase": f,
                    "testata": v["fonte"] or urllib.parse.urlsplit(v["fonte_url"]).hostname or "?",
                    "sito": v["fonte_url"], "titolo": titolo, "link": v["link"], "data": v["data"],
                })
    log(f"Google News: {esito['query']} ricerche, {len(esito['trovate'])} risultati")
    return esito


# ──────────────────────────────────────────────────────────────
# Issue
# ──────────────────────────────────────────────────────────────

def corpo_issue(feed: dict, gnews: dict | None, frasi: list[dict], ora: dt.datetime) -> str:
    r = [
        f"_Aggiornata il {S.fmt(ora)} (ora italiana) da `controllo-copie.yml`, ogni lunedì._",
        "",
        "## 1. Riprese trovate nei feed delle testate locali",
        "",
    ]
    if feed["trovate"]:
        r.append(f"Una notizia è segnalata quando condivide almeno {SOGLIA_FRAMMENTI} frammenti "
                 f"di {N} parole con un nostro articolo degli ultimi {GIORNI_NOSTRI} giorni.")
        r.append("")
        for t in sorted(feed["trovate"], key=lambda t: (t["precedente"], -t["frammenti"])):
            fonte = "**con fonte** (link o citazione a protezionecivilegenzano.it)" if t["con_fonte"] \
                else "**senza fonte**"
            if t["precedente"]:
                fonte += "; **uscita prima del nostro articolo**: testo comune a una fonte terza, non una ripresa"
            data = S.fmt(t["data"]) if t["data"] else "data non indicata"
            r.append(f"- **{t['testata']}** — [{t['titolo'] or t['link']}]({t['link']}) ({data})")
            r.append(f"  - nostro articolo: [{t['nostro_titolo']}]({S.url_articolo(t['slug'])})")
            r.append(f"  - {t['frammenti']} frammenti in comune {t['da']}, {fonte}")
            for s in t["spezzoni"]:
                r.append(f"  - «{s}»")
    else:
        r.append("Nessuna copia trovata nei feed delle testate locali.")
    r += ["", "<details><summary>Testate lette e pagine controllate</summary>", ""]
    r += [f"- {t}" for t in feed["testate"]] or ["- nessuna"]
    r.append(f"- Pagine scaricate: {feed['pagine']} (al massimo {MAX_PAGINE}, {MAX_PER_TESTATA} per testata); "
             f"notizie confrontate sul solo testo del feed: {feed['solo_feed']}.")
    if feed["senza_risposta"]:
        r += ["", "Feed che non hanno risposto:"] + [f"- {t}" for t in feed["senza_risposta"]]
    if feed["pagine_ko"]:
        r += ["", f"Pagine non raggiungibili ({len(feed['pagine_ko'])}):"] + \
             [f"- {t}" for t in feed["pagine_ko"][:20]]
    r += ["", "</details>", "", "## 2. Frasi nostre trovate su Google News", ""]
    if gnews is None:
        r.append("_Ricerca su Google News non eseguita in questo giro._")
    else:
        if gnews["trovate"]:
            r.append("Risultati della ricerca della frase esatta nel feed di Google News "
                     "(il nostro sito è escluso). Il link apre la notizia attraverso Google News.")
            r.append("")
            for t in gnews["trovate"]:
                data = S.fmt(t["data"]) if t["data"] else "data non indicata"
                r.append(f"- **{t['testata']}** — [{t['titolo']}]({t['link']}) ({data})")
                r.append(f"  - nostro articolo: [{t['nostro_titolo']}]({S.url_articolo(t['slug'])})")
                r.append(f"  - frase cercata: «{t['frase']}»")
        else:
            r.append("Nessuna delle frasi cercate compare su Google News fuori dal nostro sito.")
        r.append("")
        nota = f"_{gnews['query']} ricerche"
        if gnews["saltate"]:
            nota += f", {gnews['saltate']} rimandate al prossimo giro"
        if gnews["errori"]:
            nota += f", {len(gnews['errori'])} senza risposta"
        r.append(nota + "._")
        if gnews["interrotta"]:
            r.append(f"_{gnews['interrotta']}._")
    r += ["",
          "## 3. Ricerca assistita sul web",
          "",
          f"Le stesse frasi degli articoli degli ultimi {GIORNI_ASSISTITA} giorni, con la ricerca "
          "esatta già pronta sui motori (il nostro sito è escluso). Vanno aperte a mano: "
          "un risultato è una pagina che riporta la frase identica.",
          ""]
    if not frasi:
        r.append("Nessun articolo uscito nel periodo.")
    for a in frasi:
        r.append(f"### [{a['titolo']}]({S.url_articolo(a['slug'])})")
        r.append("")
        if not a["frasi"]:
            r.append("_Nessuna frase adatta (articolo fatto di elenchi o tabelle)._")
        for f in a["frasi"]:
            link = " · ".join(f"[{n}]({u})" for n, u in link_ricerca(f))
            r.append(f"- «{f}» — {link}")
        r.append("")
    r += ["---",
          "_Frammenti esclusi dal confronto: quelli con numeri di emergenza o di servizio, "
          "quelli fatti quasi solo di parole comuni, nomi di enti o di comuni dei Castelli, e le "
          f"nostre formule che ricorrono in {SOGLIA_FORMULA} o più articoli. Titoli di eventi o "
          "frasi di un comunicato possono coincidere perché vengono dalla stessa fonte: prima di "
          "parlare di copia si confrontano le date. Una ripresa con "
          "fonte rispetta la licenza CC BY 4.0 del sito; una senza fonte va valutata caso per caso._"]
    return "\n".join(r) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Controllo settimanale delle copie degli articoli.")
    ap.add_argument("--dry-run", action="store_true", help="stampa l'esito senza scrivere nulla (salvo --issue-body)")
    ap.add_argument("--issue-body", type=Path, help="file Markdown in cui scrivere il corpo dell'issue")
    ap.add_argument("--senza-gnews", action="store_true", help="salta la ricerca su Google News")
    args = ap.parse_args()

    ora = S.adesso()
    nostri, formule = nostri_articoli(ora)
    log(f"Nostri articoli degli ultimi {GIORNI_NOSTRI} giorni: {len(nostri)}; "
        f"formule ricorrenti escluse: {len(formule)}")
    frasi = frasi_caratteristiche(nostri, formule, ora)
    try:
        feed = parte_feed(nostri, ora)
    except Exception as e:  # noqa: BLE001 — le altre parti escono comunque
        log(f"Controllo dei feed interrotto: {type(e).__name__}: {e}")
        feed = {"testate": [], "senza_risposta": [f"interruzione: {type(e).__name__}"],
                "trovate": [], "pagine": 0, "pagine_ko": [], "notizie": 0, "solo_feed": 0}
    gnews = None
    if not args.senza_gnews:
        try:
            gnews = parte_gnews(frasi)
        except Exception as e:  # noqa: BLE001
            log(f"Ricerca su Google News interrotta: {type(e).__name__}: {e}")
            gnews = {"query": 0, "trovate": [], "errori": [type(e).__name__],
                     "interrotta": "ricerca interrotta da un errore", "saltate": 0}
    corpo = corpo_issue(feed, gnews, frasi, ora)
    # GitHub rifiuta il corpo di un'issue oltre 65.536 caratteri: si accorcia
    # la coda (la ricerca assistita), che è l'ultima sezione.
    if len(corpo) > MAX_CORPO:
        corpo = corpo[:MAX_CORPO].rsplit("\n### ", 1)[0] + \
            "\n\n_Elenco accorciato: l'issue ha un limite di lunghezza._\n"
    if args.issue_body:
        args.issue_body.write_text(corpo, encoding="utf-8")
        log(f"Corpo dell'issue scritto in {args.issue_body}")
    if args.dry_run or not args.issue_body:
        print(corpo)
    log(f"Riprese dai feed: {len(feed['trovate'])}; "
        f"da Google News: {len(gnews['trovate']) if gnews else 'non eseguita'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
