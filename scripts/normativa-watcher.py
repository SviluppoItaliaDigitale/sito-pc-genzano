#!/usr/bin/env python3
"""
normativa-watcher.py — rassegna delle novità normative e degli atti di
interesse per la Protezione Civile (v2, 18/09/2026).

Due famiglie di fonti:

FONTI PRIMARIE (lette direttamente, ogni giorno) — "--fonti primarie"
- Albo pretorio del Comune di Genzano di Roma (portale jcitygov
  genzanodiroma.trasparenza-valutazione-merito.it): ordinanze, delibere,
  determinazioni, avvisi in pubblicazione.
- Gazzetta Ufficiale, Serie Generale (gazzettaufficiale.it): sommario di
  ogni numero uscito nella finestra.
- Normattiva (normattiva.it): elenco degli atti normativi dell'anno per
  data di emanazione (versione multivigente).
- BURL — Bollettino Ufficiale della Regione Lazio (sicer.regione.lazio.it):
  ricerca per parola nell'oggetto nella finestra di edizione.

FONTI SECONDARIE (rassegna stampa, di norma settimanale) — "--fonti news"
- Google News RSS con query tematiche e site:
- Feed RSS istituzionali (TGR Lazio)
- DPC home + Area stampa via Firecrawl (solo se FIRECRAWL_API_KEY)

Ogni voce è classificata per RILEVANZA con un punteggio a parole chiave:
- "diretta"   → riguarda la protezione civile, il volontariato di PC, le
                emergenze, o il Comune di Genzano su temi di sicurezza;
- "indiretta" → temi contigui (terzo settore, eventi pubblici locali,
                meteo, ambiente, sanità d'emergenza, radiocomunicazioni);
- le voci senza alcuna corrispondenza vengono scartate per le fonti
  primarie (rumore) e per le news.

Uso:
    python3 scripts/normativa-watcher.py [--days 2] [--fonti primarie|news|tutte]
        [--out novita.json] [--issue-body corpo.md] [--dedup-issues]
        [--escludi-url file.txt]

--dedup-issues  → con `gh` disponibile, scarta gli URL già comparsi nelle
                  issue con label `normativa-watcher` (stateless: nessun
                  file di stato da committare).
--escludi-url   → file con un URL per riga da scartare (per le sessioni
                  senza `gh`).

Dipendenze: solo stdlib per le fonti primarie; `feedparser` per le news.
Ogni fonte è fail-safe: se cade, viene registrata in `errori` e le altre
proseguono. Esce 0 (anche con zero hit), 1 solo su errore d'uso.
"""
import argparse
import html as htmllib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

ROMA = ZoneInfo("Europe/Rome")


def oggi_roma() -> date:
    """Data di oggi in ora italiana (il runner è in UTC; audit 25/09/2026, F31)."""
    return datetime.now(ROMA).date()
from urllib.parse import quote_plus

UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/)"
TIMEOUT = 40

# ---------------------------------------------------------------------------
# Classificazione di rilevanza
# ---------------------------------------------------------------------------

# Sintassi delle parole chiave: confronto a parole intere (non scattano dentro
# altre parole: "rsa" non trova "bersaglieri"); un asterisco finale ammette
# qualunque desinenza ("calamit*" → calamità/calamitoso).

# Parole/frasi che rendono un atto DIRETTAMENTE interessante per il Gruppo.
KW_DIRETTE = [
    'protezione civile', 'protezionecivile', 'centro operativo comunale', 'c.o.c.', 'coc',
    'dipartimento della protezione civile', 'capo dipartimento', 'ordinanza del capo',
    'volontariato di protezione civile', 'organizzazioni di volontariato', 'colonna mobile',
    'stato di emergenza', 'stato di mobilitazione', 'calamit*', 'emergenz*',
    'allert*', 'centro funzionale', 'bollettino di criticit*',
    'incendi boschivi', 'incendio boschivo', 'antincendio boschivo', 'aib', 'campagna aib',
    'rischio idrogeologico', 'dissesto idrogeologico', 'rischio idraulico', 'rischio sismico',
    'alluvion*', 'esondazion*', 'frana', 'frane', 'franoso', 'franosa', 'franament*', 'sisma', 'sismic*', 'terremot*', 'maremot*', 'vulcan*',
    'piano di emergenza', 'piano comunale di emergenza', 'pianificazione di emergenza',
    'evacuazion*', 'aree di attesa', 'aree di ammassamento', 'aree di accoglienza',
    'it-alert', 'numero unico', 'nue 112', 'n.u.e.',
    'esercitazion*', 'vigili del fuoco', 'soccorso pubblico',
    'genzano di roma', 'genzano', 'castelli romani',
    'd.lgs. 1/2018', 'decreto legislativo 2 gennaio 2018', 'codice della protezione civile',
    'l.r. 2/2014', 'legge regionale 26 febbraio 2014',
    'ordinanza contingibile', 'ordinanza sindacale',
    'idrant*', 'autobott*', 'radiocomunicazion*', 'radioamator*',
    'servizio nazionale della protezione civile',
]

# Parole/frasi che rendono un atto INDIRETTAMENTE interessante.
KW_INDIRETTE = [
    'terzo settore', 'runts', 'odv', 'ets', 'volontari*', 'servizio civile',
    'sicurezza urbana', 'pubblica sicurezza', 'ordine pubblico', 'manifestazion*', 'evento pubblico',
    'sagr*', 'festa del pane', 'festa patronale', 'infiorat*', 'procession*', 'fiera', 'fiere', 'mercatin*',
    'concerto', 'concerti', 'spettacolo pirotecnico', 'fuochi', 'corteo', 'cortei', 'carneval*',
    'meteo*', 'maltempo', 'neve', 'gelo', 'ghiaccio', 'vento forte', 'ondata di calore', 'caldo',
    'siccit*', 'crisi idrica', 'idric*', 'diga', 'dighe', 'invaso', 'invasi', 'bacino', 'bacini',
    'ambient*', 'incendi*', 'rogh*', 'rifiuti', 'amianto',
    'sanit*', '118', 'ares', 'ambulanz*', 'defibrillator*', 'dae', 'primo soccorso', 'pandemi*', 'epidemi*',
    'scuol*', 'scolastic*', 'sicurezza stradale', 'viabilit*', 'chiusur*', 'strad*', 'transito',
    'blackout', 'energia elettrica', 'interruzion*', 'gas',
    'difesa civile', 'prefettur*', 'prefett*', 'sindac*', 'polizia locale',
    'lago di nemi', 'lago albano', 'nemi', 'ariccia', 'albano', 'lanuvio', 'velletri', 'marino',
    'parco dei castelli', 'bosch*', 'forestal*',
    'accessibilit*', 'disabilit*', 'fragil*', 'anzian*', 'rsa',
    'sicurezza sul lavoro', 'd.lgs. 81', 'antincendio',
    'cambiamenti climatici', 'clima', 'adattamento',
    'radio', 'frequenz*', 'telecomunicazion*',
    'ordinanz*', 'giornata', 'commemorazion*',
]

# Nelle fonti nazionali/regionali (GU, Normattiva, BURL) i termini troppo
# generici producono rumore: valgono solo per l'albo pretorio, dove
# l'ambito è già il territorio di Genzano.
KW_INDIRETTE_SOLO_ALBO = {
    'chiusur*', 'strad*', 'transito', 'viabilit*', 'radio', 'gas', 'clima', 'scuol*', 'scolastic*',
    'giornata', 'commemorazion*', 'sindac*', 'polizia locale', 'concerto', 'concerti', 'fiera', 'fiere', 'mercatin*',
    'corteo', 'cortei', 'carneval*', 'interruzion*', 'energia elettrica', 'rifiuti', 'bosch*', 'accessibilit*',
    'disabilit*', 'fragil*', 'anzian*', 'rsa', 'ambient*', 'sanit*', '118', 'ares', 'ambulanz*',
    'caldo', 'incendi*', 'rogh*', 'idric*', 'ordinanz*', 'diga', 'dighe', 'invaso', 'invasi', 'bacino', 'bacini', 'ets', 'odv',
    'prefett*', 'prefettur*', 'sagr*', 'procession*', 'fuochi', 'neve', 'gelo', 'ghiaccio',
}

# Rumore ricorrente: atti che citano parole-chiave in senso estraneo alla PC.
KW_RUMORE = [
    'liquidazione coatta', 'concorso pubblico', 'diario delle prove', 'graduatori*',
    "autorizzazione all'immissione in commercio", 'medicinal*', 'farmac*',
    'tasso di interesse', 'buoni del tesoro', 'cambi di riferimento', 'titoli di stato',
    'nomina del commissario liquidatore', 'scioglimento del consiglio comunale',
    'ruolo tari', 'imu', 'tributi', 'canone', 'affidamento diretto', 'impegno di spesa',
    'liquidazione fattura', 'liquidazione delle competenze', 'contributo economico',
    'mensa', 'refezione', 'asilo nido', 'cimiter*', 'lampade votive', 'loculi',
    'concessione edilizia', 'permesso di costruire', 'condono', 'sanatoria edilizia',
    'toponomastica', 'numerazione civica', 'patrocinio',
]

_RE_CACHE = {}


def _pattern(kw):
    if kw not in _RE_CACHE:
        prefisso = kw.endswith('*')
        base = re.escape(kw.rstrip('*'))
        _RE_CACHE[kw] = re.compile(r'(?<![\w])' + base + (r'' if prefisso else r'(?![\w])'), re.I)
    return _RE_CACHE[kw]


def normalizza(s):
    s = htmllib.unescape(s or '')
    return re.sub(r'\s+', ' ', s).strip().lower()


def _trova(lista, testo, escludi=frozenset()):
    return [k for k in lista if k not in escludi and _pattern(k).search(testo)]


def classifica(testo, fonte_albo=False):
    """Ritorna (rilevanza, motivi) con rilevanza in {'diretta','indiretta',None}.

    Fonti nazionali/regionali: "Genzano"/"Castelli Romani" da soli valgono come
    rilevanza indiretta (serve anche un tema PC per la diretta). Albo pretorio:
    il territorio è implicito e non conta; conta il tema (PC, sicurezza,
    eventi pubblici) e ogni ordinanza è almeno indiretta.
    """
    t = normalizza(testo)
    territorio = {'genzano di roma', 'genzano', 'castelli romani'}
    dirette = _trova(KW_DIRETTE, t, escludi=territorio if fonte_albo else frozenset())
    indirette = _trova(KW_INDIRETTE, t, escludi=frozenset() if fonte_albo else KW_INDIRETTE_SOLO_ALBO)
    rumore = _trova(KW_RUMORE, t)
    solo_territorio = bool(dirette) and set(dirette) <= territorio
    if dirette and not solo_territorio:
        if rumore and len(dirette) == 1 and not fonte_albo:
            return 'indiretta', sorted(set(dirette + rumore))
        return 'diretta', sorted(set(dirette))
    if solo_territorio:
        return 'indiretta', sorted(set(dirette + indirette))
    if indirette and (fonte_albo or not rumore):
        return 'indiretta', sorted(set(indirette))
    return None, []


# ---------------------------------------------------------------------------
# Utilità HTTP (stdlib)
# ---------------------------------------------------------------------------

class Cliente:
    """Piccolo client HTTP con cookie jar (serve a SICER e al portale jcitygov)."""

    def __init__(self):
        import http.cookiejar
        self.jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))

    def get(self, url, referer=None):
        req = urllib.request.Request(url, headers={'User-Agent': UA, **({'Referer': referer} if referer else {})})
        with self.opener.open(req, timeout=TIMEOUT) as r:
            return decodifica(r.read(), r.headers.get_content_charset())

    def post(self, url, data, referer=None):
        body = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(url, data=body, method='POST', headers={
            'User-Agent': UA, 'Content-Type': 'application/x-www-form-urlencoded',
            **({'Referer': referer} if referer else {})})
        with self.opener.open(req, timeout=TIMEOUT) as r:
            return decodifica(r.read(), r.headers.get_content_charset())


def decodifica(raw, charset=None):
    for enc in ([charset] if charset else []) + ['utf-8', 'latin-1']:
        try:
            return raw.decode(enc)
        except (UnicodeDecodeError, LookupError, TypeError):
            continue
    return raw.decode('utf-8', errors='replace')


def solo_testo(frammento):
    t = re.sub(r'<(script|style).*?</\1>', '', frammento, flags=re.S)
    t = re.sub(r'<br\s*/?>', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', htmllib.unescape(t)).strip()


def campi_nascosti(pagina):
    return {m.group(1): m.group(2) for m in re.finditer(
        r'<input[^>]*name="([^"]+)"[^>]*value="([^"]*)"', pagina, flags=re.I)}


def parse_data_it(s):
    m = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', s or '')
    if not m:
        return None
    try:
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    except ValueError:
        return None


def parse_data_iso(s):
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', s or '')
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def voce(fonte, fonte_tipo, titolo, link, data_pub, tipo_atto='', numero='', ente='', sommario='', fonte_albo=False):
    rilevanza, motivi = classifica(f'{tipo_atto} {titolo} {"" if fonte_albo else ente} {sommario}', fonte_albo=fonte_albo)
    return {
        'fonte': fonte,
        'fonte_tipo': fonte_tipo,      # primaria | news
        'titolo': titolo,
        'link': link,
        'published': data_pub.isoformat() if isinstance(data_pub, date) else data_pub,
        'tipo_atto': tipo_atto,
        'numero': numero,
        'ente': ente,
        'sommario': (sommario or '')[:300],
        'rilevanza': rilevanza,
        'motivi': motivi,
    }


# ---------------------------------------------------------------------------
# FONTE PRIMARIA 1 — Albo pretorio del Comune di Genzano di Roma
# ---------------------------------------------------------------------------

ALBO_BASE = 'https://genzanodiroma.trasparenza-valutazione-merito.it'
ALBO_LISTA = ALBO_BASE + '/web/trasparenza/papca-ap/-/papca/igrid/5986'      # atti in pubblicazione
ALBO_PAGINAZIONE = (ALBO_BASE + '/web/trasparenza/papca-ap?p_p_id=jcitygovalbopubblicazioni_WAR_jcitygovalbiportlet'
                    '&p_p_lifecycle=1&p_p_state=pop_up&p_p_mode=view'
                    '&_jcitygovalbopubblicazioni_WAR_jcitygovalbiportlet_action=eseguiPaginazione')


def fetch_albo_genzano(cutoff, errori):
    out = []
    cli = Cliente()
    try:
        pagina = cli.get(ALBO_LISTA)
        # Chiediamo 50 righe per pagina: con 2 giorni di finestra basta e avanza.
        try:
            pagina2 = cli.post(ALBO_PAGINAZIONE, {'hidden_page_size': '50', 'hidden_page_to': '1'}, referer=ALBO_LISTA)
            if 'master-detail-list-line' in pagina2:
                pagina = pagina2
        except Exception as e:  # noqa: BLE001
            print(f'  [warn] albo: paginazione a 50 non riuscita, uso 20 righe ({e})', file=sys.stderr)
        righe = re.findall(r'<tr class="master-detail-list-line[^"]*"[^>]*data-id="(\d+)">(.*?)</tr>', pagina, flags=re.S)
        if not righe:
            raise RuntimeError('nessuna riga trovata: struttura della pagina cambiata?')
        for id_atto, riga in righe:
            celle = re.findall(r'<td[^>]*class="([^"]+)"[^>]*>(.*?)</td>', riga, flags=re.S)
            c = {k.split()[0]: solo_testo(v) for k, v in celle}
            registro = c.get('annonumeroregistrazione', '')
            numero = c.get('annonumero', '')
            tipo = c.get('categoria', '').replace(' / ', ' / ')
            oggetto = c.get('oggetto', '')
            periodo = c.get('periodo-pubblicazione', '')
            inizio = parse_data_it(periodo)
            if inizio and inizio < cutoff:
                continue
            link = f'{ALBO_BASE}/web/trasparenza/papca-ap/-/papca/display/{id_atto}'
            v = voce('Albo pretorio — Comune di Genzano di Roma', 'primaria', oggetto, link, inizio,
                     tipo_atto=tipo, numero=f'{numero} (reg. {registro})', ente='Comune di Genzano di Roma',
                     fonte_albo=True)
            if v['rilevanza']:
                out.append(v)
    except Exception as e:  # noqa: BLE001
        errori.append(f'Albo pretorio Genzano: {e}')
        print(f'  [error] albo pretorio: {e}', file=sys.stderr)
    return out


# ---------------------------------------------------------------------------
# FONTE PRIMARIA 2 — Gazzetta Ufficiale, Serie Generale
# ---------------------------------------------------------------------------

GU_BASE = 'https://www.gazzettaufficiale.it'
GU_30GIORNI = GU_BASE + '/30giorni/serie_generale'


def fetch_gazzetta_ufficiale(cutoff, errori):
    out = []
    cli = Cliente()
    try:
        elenco = cli.get(GU_30GIORNI)
        numeri = sorted(set(re.findall(r'dataPubblicazioneGazzetta=(\d{4})(\d{2})(\d{2})&numeroGazzetta=(\d+)', elenco)))
        if not numeri:
            raise RuntimeError('elenco ultimi 30 giorni vuoto: struttura cambiata?')
        for aaaa, mm, gg, n in numeri:
            d = date(int(aaaa), int(mm), int(gg))
            if d < cutoff:
                continue
            url = f'{GU_BASE}/gazzetta/serie_generale/caricaDettaglio?dataPubblicazioneGazzetta={aaaa}-{mm}-{gg}&numeroGazzetta={n}'
            try:
                sommario = cli.get(url)
            except Exception as e:  # noqa: BLE001
                errori.append(f'GU n. {n} del {gg}/{mm}/{aaaa}: {e}')
                continue
            out.extend(_parse_sommario_gu(sommario, d, n))
    except Exception as e:  # noqa: BLE001
        errori.append(f'Gazzetta Ufficiale: {e}')
        print(f'  [error] gazzetta ufficiale: {e}', file=sys.stderr)
    return out


def _parse_sommario_gu(pagina, d, numero_gu):
    """Scorre il sommario in ordine: rubrica/emettitore aggiornano il contesto,
    ogni coppia di link (estremi + oggetto) è un atto."""
    out = []
    rubrica = ente = ''
    visti = set()
    token = re.compile(
        r'<span class="rubrica">(.*?)</span>|<span class="emettitore">(.*?)</span>|'
        r'<a href="(/atto/serie_generale/caricaDettaglioAtto/originario\?[^"]+)">\s*<span class="data">(.*?)</span>\s*</a>\s*'
        r'<a href="[^"]+">(.*?)<span class="riferimento">', flags=re.S)
    for m in token.finditer(pagina):
        if m.group(1) is not None:
            rubrica = solo_testo(m.group(1))
            ente = ''
        elif m.group(2) is not None:
            ente = solo_testo(m.group(2))
        else:
            href, estremi, oggetto = m.group(3), solo_testo(m.group(4)), solo_testo(m.group(5))
            codice = re.search(r'codiceRedazionale=([^&]+)', href)
            chiave = codice.group(1) if codice else href
            if chiave in visti:
                continue
            visti.add(chiave)
            link = GU_BASE + htmllib.unescape(href)
            titolo = f'{estremi} — {oggetto}' if estremi else oggetto
            v = voce(f'Gazzetta Ufficiale — Serie Generale n. {numero_gu}', 'primaria', titolo, link, d,
                     tipo_atto=estremi.split(' ')[0] if estremi else '', numero=estremi,
                     ente=f'{rubrica} · {ente}'.strip(' ·'))
            if v['rilevanza']:
                out.append(v)
    return out


# ---------------------------------------------------------------------------
# FONTE PRIMARIA 3 — Normattiva (elenco atti per data di emanazione)
# ---------------------------------------------------------------------------

NORMATTIVA_BASE = 'https://www.normattiva.it'


def fetch_normattiva(cutoff, errori):
    out = []
    cli = Cliente()
    try:
        anno = oggi_roma().year
        pagina = cli.get(f'{NORMATTIVA_BASE}/ricerca/elencoPerData/anno/{anno}')
        blocchi = re.findall(r'<div id="collapseDiv_\d+" class="collapse-div boxAtto[^"]*"[^>]*>(.*?)(?=<div id="collapseDiv_|<!-- fine lista|</section>)', pagina, flags=re.S)
        if not blocchi:
            raise RuntimeError('nessun atto nella pagina: struttura cambiata?')
        for b in blocchi:
            href = re.search(r'href="(/atto/caricaDettaglioAtto\?[^"]+)"', b)
            testo = solo_testo(b)
            m_gu = re.search(r'\(GU n\.\s*(\d+) del (\d{2}-\d{2}-\d{4})\)', testo)
            d = parse_data_it(m_gu.group(2).replace('-', '/')) if m_gu else None
            if d and d < cutoff:
                continue
            if not d:
                # senza data di GU non possiamo finestrare: saltiamo (atti in attesa)
                continue
            titolo = re.sub(r'\s*\(GU n\..*$', '', testo).strip()
            link = NORMATTIVA_BASE + htmllib.unescape(href.group(1)).strip() if href else f'{NORMATTIVA_BASE}/ricerca/elencoPerData/anno/{anno}'
            link = re.sub(r'\s+', '', link)
            estremi = re.match(r'([A-ZÀ-Ü\-\. ]+ \d{1,2} [A-Za-z]+ \d{4}, n\. \d+)', titolo)
            v = voce('Normattiva — atti per data di emanazione', 'primaria', titolo, link, d,
                     tipo_atto=titolo.split(' ')[0], numero=estremi.group(1) if estremi else '',
                     ente=f'GU n. {m_gu.group(1)}' if m_gu else '')
            if v['rilevanza']:
                out.append(v)
    except Exception as e:  # noqa: BLE001
        errori.append(f'Normattiva: {e}')
        print(f'  [error] normattiva: {e}', file=sys.stderr)
    return out


# ---------------------------------------------------------------------------
# FONTE PRIMARIA 4 — BURL, Bollettino Ufficiale della Regione Lazio (SICER)
# ---------------------------------------------------------------------------

BURL_FRONTEND = 'https://sicer.regione.lazio.it/PublicBur/burlazio/FrontEnd'
BURL_RICERCA = BURL_FRONTEND + '/RicercaAtto'
BURL_PAROLE = [
    'protezione civile', 'emergenza', 'calamit', 'allerta', 'incendi', 'volontariato',
    'idrogeologic', 'sismic', 'Genzano', 'Castelli Romani', 'esercitazione', 'meteo',
]


def fetch_burl(cutoff, errori):
    out = []
    cli = Cliente()
    visti = set()
    try:
        form = cli.get(BURL_RICERCA)
        nascosti = campi_nascosti(form)
        if 'BL_ID' not in nascosti:
            raise RuntimeError('form di ricerca senza campi nascosti: struttura cambiata?')
        da = cutoff.strftime('%d/%m/%Y')
        a = oggi_roma().strftime('%d/%m/%Y')
        for parola in BURL_PAROLE:
            dati = dict(nascosti)
            dati.update({'BL_ACTION': 'CERCA', 'BL_PAR_OGGETTO_ATTO_0': parola,
                         'BL_PAR_DATA_DA_EDIZ_0': da, 'BL_PAR_DATA_A_EDIZ_0': a,
                         'BL_PAR_NUMERO_ATTO_0': '', 'BL_PAR_DATA_ATTO_0': '', 'BL_PAR_NUMERO_EDIZ_0': ''})
            try:
                ris = cli.post(BURL_FRONTEND, dati, referer=BURL_RICERCA)
            except Exception as e:  # noqa: BLE001
                errori.append(f'BURL ricerca "{parola}": {e}')
                continue
            for riga in re.findall(r'<tr[^>]*>(.*?)</tr>', ris, flags=re.S):
                celle = [solo_testo(c) for c in re.findall(r'<td[^>]*>(.*?)</td>', riga, flags=re.S)]
                if len(celle) < 9:
                    continue
                oggetto, num_atto, _num0, data_atto, _amg, tipo, num_ed, tipo_ed, data_ed = celle[:9]
                pdf = re.search(r"onGenericStreamRead\('([^']+)'\)", riga)
                chiave = pdf.group(1) if pdf else f'{num_atto}|{data_atto}'
                if chiave in visti:
                    continue
                visti.add(chiave)
                d = parse_data_it(data_ed)
                if d and d < cutoff:
                    continue
                link = f'{BURL_RICERCA}#atto={urllib.parse.quote(num_atto)}&ediz={num_ed}&data={d.isoformat() if d else ""}'
                if pdf:
                    link = f'https://www.regione.lazio.it/bur?vw=ultimibur#{pdf.group(1)}'
                v = voce(f'BURL Lazio n. {num_ed} ({tipo_ed}) del {data_ed}', 'primaria', oggetto, link, d,
                         tipo_atto=tipo, numero=f'{num_atto} del {data_atto}', ente='Regione Lazio',
                         sommario=f'file {pdf.group(1)} — ricerca atto puntuale su sicer.regione.lazio.it' if pdf else '')
                if v['rilevanza']:
                    out.append(v)
    except Exception as e:  # noqa: BLE001
        errori.append(f'BURL Lazio: {e}')
        print(f'  [error] burl: {e}', file=sys.stderr)
    return out


# ---------------------------------------------------------------------------
# FONTI SECONDARIE — Google News, RSS istituzionali, DPC via Firecrawl
# ---------------------------------------------------------------------------

GOOGLE_NEWS_BASE = "https://news.google.com/rss/search?q={q}&hl=it&gl=IT&ceid=IT:it"

FIRECRAWL_API_URL = "https://api.firecrawl.dev/v1/scrape"
FIRECRAWL_SOURCES = [
    {"nome": "DPC — Home (notizie in evidenza)", "url": "https://www.protezionecivile.gov.it/it/"},
    {"nome": "DPC — Area stampa", "url": "https://www.protezionecivile.gov.it/it/media-e-comunicazione/area-stampa/"},
]

QUERIES_GOOGLE_NEWS = [
    'protezione civile Lazio',
    'allerta meteo Lazio',
    'DPC ordinanza dipartimento protezione civile',
    'BURL Lazio protezione civile',
    'Regione Lazio decreto protezione civile',
    'Genzano di Roma protezione civile',
    'Castelli Romani allerta',
    'incendio boschivo Lazio',
    'rischio idrogeologico Castelli Romani',
    'IT-alert protezione civile',
    'volontariato protezione civile Lazio',
    'esercitazione protezione civile Lazio',
    'site:normattiva.it protezione civile',
    'site:gazzettaufficiale.it protezione civile',
    'site:regione.lazio.it protezione civile',
    'site:consiglio.regione.lazio.it protezione civile',
    'site:protezionecivile.gov.it',
    'site:vigilfuoco.it Lazio OR Castelli OR Genzano',
    'site:arpalazio.it',
    'site:arsial.it incendio OR allerta',
    'site:irpi.cnr.it',
    'site:cmcc.it adattamento OR clima OR Italia',
    'site:isprambiente.gov.it rischio OR allerta',
    'site:iss.it ondata OR emergenza OR pandemia',
    'site:camera.it protezione civile',
    'site:corteconti.it protezione civile',
    'site:cortecostituzionale.it protezione civile',
    'site:governo.it protezione civile OR consiglio dei ministri PC',
    'site:mit.gov.it sicurezza OR rischio',
    'site:cultura.gov.it patrimonio emergenza',
    'site:interno.gov.it prefettura OR emergenza',
    'site:istat.it popolazione vulnerabile OR rischio',
    'site:carabinieri.it forestali OR incendio',
    'site:anpas.org',
    'site:cri.it Lazio OR Castelli',
    'site:salute.gov.it caldo OR ondata OR emergenza',
    'site:opencoesione.gov.it protezione civile',
]

FEEDS_ISTITUZIONALI = [
    {"nome": "TGR Lazio (RAI)", "url": "https://www.rainews.it/tgr/lazio/archivio.rss"},
]


def parse_feed(url, fonte, days):
    try:
        import feedparser
    except ImportError:
        print("  [warn] feedparser non installato: fonti news saltate (pip install feedparser)", file=sys.stderr)
        return []
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    out = []
    try:
        feed = feedparser.parse(url, agent=UA)
        if feed.bozo and not feed.entries:
            print(f"  [warn] feed non parsabile: {fonte} ({url})", file=sys.stderr)
            return out
        for entry in feed.entries[:50]:
            titolo = entry.get('title', '').strip()
            link = entry.get('link', '').strip()
            sommario = re.sub(r'<[^>]+>', ' ', entry.get('summary', '')).strip()
            pp = entry.get('published_parsed') or entry.get('updated_parsed')
            if pp:
                published = datetime(*pp[:6], tzinfo=timezone.utc)
                if published < cutoff:
                    continue
                published_iso = published.isoformat()
            else:
                published_iso = None
            v = voce(fonte, 'news', titolo, link, published_iso, sommario=sommario)
            if v['rilevanza']:
                out.append(v)
    except Exception as e:  # noqa: BLE001
        print(f"  [error] {fonte}: {e}", file=sys.stderr)
    return out


def fetch_firecrawl(url, fonte):
    api_key = os.environ.get('FIRECRAWL_API_KEY')
    if not api_key:
        return []
    out = []
    try:
        req = urllib.request.Request(
            FIRECRAWL_API_URL,
            data=json.dumps({"url": url, "formats": ["markdown"], "onlyMainContent": True, "timeout": 30000}).encode('utf-8'),
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method='POST')
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        if not data.get('success'):
            print(f"  [warn] firecrawl no-success: {fonte}", file=sys.stderr)
            return out
        md = (data.get('data') or {}).get('markdown') or ''
        seen = set()
        for m in re.finditer(r'\[([^\]]+)\]\((https?://[^\)]+)\)', md):
            titolo, link = m.group(1).strip(), m.group(2).strip().split('#')[0]
            if len(titolo) < 15 or not re.search(r'protezionecivile\.gov\.it/it/(notizia|comunicato-stampa)/', link) or link in seen:
                continue
            seen.add(link)
            v = voce(fonte, 'news', titolo, link, None)
            if v['rilevanza']:
                out.append(v)
    except Exception as e:  # noqa: BLE001
        print(f"  [error] firecrawl {fonte}: {e}", file=sys.stderr)
    return out


# ---------------------------------------------------------------------------
# Dedup contro le issue già aperte (stateless) e file di esclusione
# ---------------------------------------------------------------------------

def url_gia_segnalati_da_issue():
    """URL già comparsi nelle issue `normativa-watcher` (aperte o chiuse, ultime 100).
    Richiede `gh` autenticato; altrimenti insieme vuoto."""
    if not shutil.which('gh'):
        print('  [warn] gh non disponibile: dedup contro le issue saltato', file=sys.stderr)
        return set()
    try:
        r = subprocess.run(['gh', 'issue', 'list', '--label', 'normativa-watcher', '--state', 'all',
                            '--limit', '100', '--json', 'body'], capture_output=True, text=True, timeout=60)
        if r.returncode != 0:
            print(f'  [warn] gh issue list fallito: {r.stderr.strip()[:200]}', file=sys.stderr)
            return set()
        urls = set()
        for it in json.loads(r.stdout or '[]'):
            urls.update(re.findall(r'\((https?://[^\s\)]+)\)', it.get('body') or ''))
        return urls
    except Exception as e:  # noqa: BLE001
        print(f'  [warn] dedup issue: {e}', file=sys.stderr)
        return set()


# ---------------------------------------------------------------------------
# Corpo della issue (Markdown)
# ---------------------------------------------------------------------------

ETICHETTA_RILEVANZA = {'diretta': '🔴 diretta', 'indiretta': '🟡 indiretta'}


def corpo_issue(output):
    hits = output['novita']
    primarie = [h for h in hits if h['fonte_tipo'] == 'primaria']
    news = [h for h in hits if h['fonte_tipo'] == 'news']
    oggi = datetime.now(ROMA).strftime('%d/%m/%Y')
    righe = []
    if primarie:
        righe.append(f"# Rassegna normativa e albo pretorio — {oggi}\n")
    else:
        righe.append(f"# Novità normative e cronaca PC — settimana al {oggi}\n")
    righe.append(f"Finestra: ultimi **{output['finestra_giorni']} giorni**. Fonti lette: {', '.join(output['fonti_lette'])}. "
                 f"Trovati **{len(primarie)} atti** dalle fonti primarie e **{len(news)} notizie** dalla rassegna stampa"
                 f"{' (' + str(output['scartati_gia_segnalati']) + ' già segnalati in issue precedenti, scartati)' if output.get('scartati_gia_segnalati') else ''}.\n")
    if output.get('errori'):
        righe.append("> ⚠️ Fonti non raggiunte in questo giro (da ricontrollare a mano): " + '; '.join(output['errori']) + "\n")

    def blocco(items, titolo):
        if not items:
            return
        righe.append(f"\n## {titolo} ({len(items)})\n")
        for r in ('diretta', 'indiretta'):
            sub = [i for i in items if i['rilevanza'] == r]
            if not sub:
                continue
            righe.append(f"\n### Rilevanza {ETICHETTA_RILEVANZA[r]} ({len(sub)})\n")
            for it in sub:
                data = (it.get('published') or '')[:10]
                t = it['titolo'].replace('|', '\\|').replace('\n', ' ')
                estremi = ' · '.join(x for x in [it.get('tipo_atto'), it.get('numero'), it.get('ente')] if x)
                righe.append(f"- **{data}** — {it['fonte']}{' · ' + estremi if estremi else ''}\n  [{t}]({it['link']})\n  <sub>parole chiave: {', '.join(it['motivi'])}</sub>")

    blocco(primarie, "Atti dalle fonti primarie (albo pretorio · Gazzetta Ufficiale · Normattiva · BURL)")
    if news:
        righe.append(f"\n## Rassegna stampa e feed ({len(news)})\n")
        righe.append("Le voci sotto vengono da Google News e feed: **verificare sempre la fonte originale** (possono essere riprese non istituzionali).\n")
        from collections import defaultdict
        per_fonte = defaultdict(list)
        for n in news:
            per_fonte[n['fonte']].append(n)
        for fonte, items in sorted(per_fonte.items()):
            righe.append(f"\n<details><summary><b>{fonte}</b> ({len(items)})</summary>\n")
            for it in items[:15]:
                data = (it.get('published') or '')[:10]
                t = it['titolo'].replace('|', '\\|')
                righe.append(f"- **{data}** — [{t}]({it['link']})")
            if len(items) > 15:
                righe.append(f"- *… e altri {len(items) - 15} risultati*")
            righe.append("\n</details>")

    righe.append("\n---\n")
    righe.append("📌 **Cosa fare (regola del 18/09/2026 — istruzione dell'utente):** per ogni atto con rilevanza **diretta** o **indiretta** "
                 "che riguarda il Gruppo, la protezione civile a Genzano e nei Castelli Romani, il volontariato di PC o la sicurezza dei cittadini, "
                 "**si scrive un articolo**. Sequenza: aprire la fonte primaria e leggere l'atto integrale (mai dal solo titolo); "
                 "verificare estremi e vigenza (`pc-normative-verifier`, `pc-fact-checker`); redigere l'articolo con tutti i gate "
                 "(`pc-article-reviewer`, cover, versione facile se norma densa); aggiornare le pagine che citano la norma (`/normativa/`, manuale — opera viva); "
                 "se l'evento ha già un articolo, integrare quello invece di duplicare; "
                 "**pubblicazione fino a live** (PR + merge + verifica deploy, come da Routine quotidiana «Rassegna normativa e albo pretorio», rule 10) e commento qui con il link all'articolo. "
                 "Atti che non riguardano il Gruppo (rumore delle parole chiave): dichiararlo in un commento e chiudere.")
    righe.append("\n_Issue generata da `.github/workflows/normativa-watcher.yml` (`scripts/normativa-watcher.py`)._")
    return '\n'.join(righe) + '\n'


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--days', type=int, default=2, help='Finestra temporale in giorni (default 2)')
    ap.add_argument('--fonti', choices=['primarie', 'news', 'tutte'], default='tutte',
                    help='primarie = albo/GU/Normattiva/BURL; news = Google News/RSS/Firecrawl; tutte (default)')
    ap.add_argument('--out', default='-', help='File output JSON (default stdout)')
    ap.add_argument('--issue-body', default=None, help='Scrive il corpo Markdown della issue in questo file')
    ap.add_argument('--dedup-issues', action='store_true', help='Scarta gli URL già comparsi nelle issue normativa-watcher (richiede gh)')
    ap.add_argument('--escludi-url', default=None, help='File con URL da scartare, uno per riga')
    ap.add_argument('--solo-rilevanti', action='store_true', default=True, help=argparse.SUPPRESS)
    args = ap.parse_args()

    cutoff = oggi_roma() - timedelta(days=args.days)
    errori = []
    hits = []
    fonti_lette = []
    seen_links = set()

    def aggiungi(results, nome):
        n = 0
        for r in results:
            if r['link'] in seen_links:
                continue
            seen_links.add(r['link'])
            hits.append(r)
            n += 1
        print(f"  [{n:3d}] {nome}", file=sys.stderr)

    print(f"[info] Rassegna ultimi {args.days} giorni (dal {cutoff.isoformat()}) — fonti: {args.fonti}", file=sys.stderr)

    if args.fonti in ('primarie', 'tutte'):
        for nome, fn in [('Albo pretorio Genzano di Roma', fetch_albo_genzano),
                         ('Gazzetta Ufficiale (Serie Generale)', fetch_gazzetta_ufficiale),
                         ('Normattiva', fetch_normattiva),
                         ('BURL Lazio', fetch_burl)]:
            fonti_lette.append(nome)
            aggiungi(fn(cutoff, errori), nome)

    if args.fonti in ('news', 'tutte'):
        fonti_lette.append(f'Google News ({len(QUERIES_GOOGLE_NEWS)} query)')
        for query in QUERIES_GOOGLE_NEWS:
            url = GOOGLE_NEWS_BASE.format(q=quote_plus(query))
            aggiungi(parse_feed(url, f"Google News: {query}", args.days), query)
        for f in FEEDS_ISTITUZIONALI:
            fonti_lette.append(f['nome'])
            aggiungi(parse_feed(f['url'], f['nome'], args.days), f['nome'])
        if os.environ.get('FIRECRAWL_API_KEY'):
            fonti_lette.append('DPC via Firecrawl')
            for f in FIRECRAWL_SOURCES:
                aggiungi(fetch_firecrawl(f['url'], f['nome']), f"{f['nome']} (Firecrawl)")
        else:
            print(f"  [skip] {len(FIRECRAWL_SOURCES)} fonti Firecrawl (FIRECRAWL_API_KEY non settata)", file=sys.stderr)

    # Dedup contro issue precedenti / file di esclusione
    esclusi = set()
    if args.dedup_issues:
        esclusi |= url_gia_segnalati_da_issue()
    if args.escludi_url and os.path.exists(args.escludi_url):
        with open(args.escludi_url, encoding='utf-8') as fh:
            esclusi |= {l.strip() for l in fh if l.strip()}
    prima = len(hits)
    if esclusi:
        hits = [h for h in hits if h['link'] not in esclusi]
    scartati = prima - len(hits)

    ordine = {'diretta': 0, 'indiretta': 1}
    hits.sort(key=lambda x: (0 if x['fonte_tipo'] == 'primaria' else 1, ordine.get(x['rilevanza'], 2), x.get('published') or ''), reverse=False)
    hits.sort(key=lambda x: x.get('published') or '', reverse=True)
    hits.sort(key=lambda x: (0 if x['fonte_tipo'] == 'primaria' else 1, ordine.get(x['rilevanza'], 2)))

    primarie = [h for h in hits if h['fonte_tipo'] == 'primaria']
    output = {
        "generato_il": datetime.now(timezone.utc).isoformat(),
        "finestra_giorni": args.days,
        "fonti": args.fonti,
        "fonti_lette": fonti_lette,
        "errori": errori,
        "scartati_gia_segnalati": scartati,
        "totale": len(hits),
        "totale_primarie": len(primarie),
        "totale_dirette": len([h for h in hits if h['rilevanza'] == 'diretta']),
        "novita": hits,
    }
    print(f"[info] Totale: {len(hits)} voci ({len(primarie)} da fonti primarie, {output['totale_dirette']} a rilevanza diretta); "
          f"{scartati} già segnalate; {len(errori)} fonti in errore", file=sys.stderr)

    if args.out == '-':
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        with open(args.out, 'w', encoding='utf-8') as fh:
            json.dump(output, fh, ensure_ascii=False, indent=2)
        print(f"[info] Output scritto in {args.out}", file=sys.stderr)
    if args.issue_body:
        with open(args.issue_body, 'w', encoding='utf-8') as fh:
            fh.write(corpo_issue(output))
        print(f"[info] Corpo issue scritto in {args.issue_body}", file=sys.stderr)


if __name__ == '__main__':
    main()
