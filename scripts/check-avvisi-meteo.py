#!/usr/bin/env python3
"""
Aggiorna data/allerta.json con il blocco "avviso_meteo" leggendo la pagina
"Allertamenti" della Regione Lazio, filtrando i PDF degli avvisi di
condizioni meteorologiche avverse (vento, neve, ondate di calore, ghiaccio,
gelate, mareggiate) — distinti dai normali allertamenti di criticità
idrogeologica e idraulica già coperti da check-allerta.py (bollettino di criticità del Dipartimento e della Regione).

Logica:
1. Scarica la pagina HTML degli "allertamenti".
2. Estrae i link PDF e la loro data dal nome file (regex su date IT).
3. Filtra solo i PDF emessi negli ultimi 5 giorni (gli avvisi sono validi
   24-36 ore, do margine per coprire emissioni serali).
4. Per ognuno, scarica e parsa con pdftotext:
   - Identifica "PER I SEGUENTI RISCHI: <RISCHIO>"
   - Se <RISCHIO> contiene "IDROGEOLOGIC" → ignora (già coperto)
   - Altrimenti estrae: livello, descrizione fenomeno, validità
5. Se trova un avviso valido ADESSO (validità ≥ now), lo scrive
   in data/allerta.json come campo "avviso_meteo".
6. Se nessun avviso valido adesso, rimuove il campo "avviso_meteo"
   esistente (cessazione automatica).

Dipendenze runtime:
- poppler-utils (per pdftotext) — preinstallato su ubuntu-latest
- python3 (stdlib only)

Guasti delle fonti (17/10/2026): una pagina o un PDF che non si leggono NON
fanno cessare l'avviso in vigore. La cessazione avviene solo se tutti gli
allertamenti recenti sono stati letti e nessuno è in corso, oppure quando la
validità dichiarata dall'avviso salvato è scaduta. Ogni lettura fallita si
annota in $FONTI_KO_FILE («fonte<TAB>motivo») e in GITHUB_OUTPUT fonti_ko=true:
il workflow apre la issue `fonte-rotta` se il guasto persiste. Uscita sempre 0.

Validità (dall'11/11/2026): inizio e fine si ricavano dalle frasi del PDF
«dal mattino di domani, giovedì 12.11.2026, e per le successive 24-36 ore»
(parte del giorno + data + durata, sempre l'intervallo più largo), e si
salvano anche le parole del bollettino («validita_dal», «validita_durata»)
che la home e Telegram mostrano. Prove: scripts/test-check-avvisi-meteo.py.

Anti-spam: lo script aggiorna allerta.json quando cambia qualcosa dell'avviso
(tipo, livello, validità, testo, PDF), mai per i soli refresh periodici: a
ogni giro, con lo stesso PDF, il risultato è identico. La notifica Telegram
del blocco avviso_meteo è gestita da scripts/notifica-telegram.py e parte solo
alla comparsa, al cambio o al rientro di tipo o livello (Priorità 3).
"""

import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
ALLERTA_PATH = ROOT / "data" / "allerta.json"

# Dall'autunno 2026 gli allertamenti stanno sul portale www.regione.lazio.it
# (pagina «Allertamenti del sistema regionale di Protezione Civile», PDF nella
# cartella allertamentiregionali-allegati/<anno>/). Il vecchio indirizzo su
# protezionecivile.regione.lazio.it rimanda alla home della protezione civile
# regionale, dove non c'è nessun PDF: il 14/10/2026 lo script trovava «0 PDF
# candidati» a ogni giro e non avrebbe mai visto un avviso. Si legge prima la
# pagina nuova; quella vecchia resta come ripiego.
BASE_URL = "https://www.regione.lazio.it"
INDEX_URLS = [
    "https://www.regione.lazio.it/protezione-civile/centro-funzionale-regionale/bollettini-allertamenti",
    "https://protezionecivile.regione.lazio.it/gestione-emergenze/centro-funzionale/bollettini/allertamenti",
]
# Link ai PDF: cartella nuova e cartella vecchia, relativi o assoluti.
PDF_HREF = re.compile(
    r'href="((?:https://[a-z.]+)?/sites/default/files/'
    r'(?:allertamentiregionali-allegati/\d{4}|binary/rl_protezione_civile/tbl_avvisi_meteo_avverso)'
    r'/[^"]*\.pdf)"',
    re.IGNORECASE,
)

ROME_TZ = ZoneInfo("Europe/Rome")
USER_AGENT = "PC-Genzano-Bot/1.0"
HTTP_TIMEOUT = 30

# Finestra retroattiva: scaricamo solo PDF emessi negli ultimi N giorni.
# Gli avvisi DPC sono validi 24-36 ore, 5 giorni di margine basta e avanza.
LOOKBACK_DAYS = 5

# Mapping: parola chiave nel campo "PER I SEGUENTI RISCHI:" → tipo umano.
# IDROGEOLOG e IDRAULICA sono ignorati: già coperti da check-allerta.py (bollettini di criticità).
RISK_TYPES = {
    "VENTO": "vento",
    "NEVE": "neve",
    "GHIACCIO": "ghiaccio e gelate",
    "GELATE": "ghiaccio e gelate",
    "ONDATA DI CALORE": "ondate di calore",
    "ONDATE DI CALORE": "ondate di calore",
    "CALORE": "ondate di calore",
    "MAREGGIATE": "mareggiate",
    "TEMPORALI": "temporali",  # avviso meteo separato dal bollettino criticità
}

# Tipi che SONO già coperti dal CSV (= ignora):
SKIP_RISKS = ["IDROGEOLOG", "IDRAULIC", "CRITICIT"]

LEVEL_NAMES = {0: "verde", 1: "gialla", 2: "arancione", 3: "rossa"}


def http_get(url, timeout=HTTP_TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def http_get_text(url):
    data = http_get(url)
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("latin-1", errors="replace")


def estrai_data_da_nome(filename):
    """Cerca date nel nome file: GG_MM_AAAA, GG-MM-AAAA, GG MM AAAA."""
    m = re.search(r"(\d{2})[_\-\s.](\d{2})[_\-\s.](\d{4})", filename)
    if not m:
        return None
    try:
        return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)), tzinfo=ROME_TZ)
    except ValueError:
        return None


def parse_pdf(pdf_bytes):
    """Restituisce testo del PDF via pdftotext stdin/stdout."""
    res = subprocess.run(
        ["pdftotext", "-layout", "-", "-"],
        input=pdf_bytes,
        capture_output=True,
        timeout=30,
    )
    if res.returncode != 0:
        return ""
    return res.stdout.decode("utf-8", errors="replace")


def estrai_rischio(testo):
    """Estrae il valore di 'PER I SEGUENTI RISCHI: <X>' dal testo PDF."""
    m = re.search(r"PER\s+I\s+SEGUENTI\s+RISCHI\s*:\s*(.+?)\s*\.", testo, re.IGNORECASE)
    if m:
        return m.group(1).strip().upper()
    return None


def classifica_rischio(rischio_raw):
    """Mappa il rischio raw del PDF al tipo umano. None se è SOLO idrogeologico.

    Caso composito: 'VENTO, NEVE, CRITICITÀ IDROGEOLOGICA ED IDRAULICA' →
    estraggo "vento, neve" e ignoro la parte idrogeologica che è già
    coperta da check-allerta.py (bollettini di criticità).
    """
    if not rischio_raw:
        return None
    tipi_trovati = []
    seen = set()
    for kw, tipo_umano in RISK_TYPES.items():
        if kw in rischio_raw and tipo_umano not in seen:
            seen.add(tipo_umano)
            tipi_trovati.append(tipo_umano)
    if tipi_trovati:
        return ", ".join(tipi_trovati)
    # Nessuna keyword meteo riconosciuta: è solo idrogeologico (già coperto)?
    for skip in SKIP_RISKS:
        if skip in rischio_raw:
            return None
    # Rischio sconosciuto, non skippabile: ritorno la stringa raw normalizzata
    return rischio_raw.title()


def estrai_livello(testo):
    """Estrae il livello max menzionato nel PDF (ROSSA > ARANCIONE > GIALLA)."""
    t = testo.upper()
    if "ALLERTA ROSSA" in t:
        return 3
    if "ALLERTA ARANCIONE" in t:
        return 2
    if "ALLERTA GIALLA" in t:
        return 1
    return 0


# Parti del giorno con cui l'allertamento indica da quando si attendono i fenomeni
# («dal mattino di domani», «dalla tarda mattinata di domani», «dalle prime ore di
# domani»). Per ognuna: l'ora più presto in cui può cominciare e l'ora più tardi,
# contate dalla mezzanotte del giorno indicato (24 = mezzanotte del giorno dopo,
# 30 = le 6 del giorno dopo). Le ore sono volutamente larghe: decidono solo da
# quando il sito mostra l'avviso «in vigore» e quando lo toglie, e un avviso deve
# comparire prima e scadere dopo, mai il contrario. Le parole mostrate al cittadino
# restano quelle del bollettino («dal mattino», «per 24-36 ore»). L'ordine conta:
# le forme lunghe prima delle brevi («tarda mattinata» prima di «mattinata»).
PARTI_DEL_GIORNO = (
    (r"prime\s+ore", 0, 6),
    (r"primo\s+mattino", 5, 9),
    (r"prima\s+mattinata", 6, 10),
    (r"tarda\s+mattinata", 10, 13),
    (r"mattin(?:o|ata)", 6, 12),
    (r"primo\s+pomeriggio", 12, 15),
    (r"tardo\s+pomeriggio", 16, 19),
    (r"pomeriggio", 12, 18),
    (r"tarda\s+ser(?:a|ata)", 21, 24),
    (r"ser(?:a|ata)", 18, 24),
    (r"mezzanotte", 0, 0),
    (r"nott(?:e|ata)", 0, 30),
    (r"ore\s+(?P<ora>\d{1,2})(?:[:.](?P<minuti>\d{2}))?", None, None),  # «dalle ore 12 di domani», «dalle ore 18.30»
)
RE_INIZIO = re.compile(
    r"\b(?P<dal>(?:a\s+partire\s+)?dal(?:l[ae]|l['’])?)\s*(?P<parte>"
    + "|".join(f"(?P<p{i}>{rx})" for i, (rx, _, _) in enumerate(PARTI_DEL_GIORNO))
    + r")\b",
    re.IGNORECASE,
)
# Dopo la parte del giorno: «di domani», «di oggi», «del giorno», poi la data.
RE_QUANDO = re.compile(r"\s*(?:di|del)\s+(?:giorno\s+)?(?P<quando>oggi|domani|dopodomani)?", re.IGNORECASE)
RE_DATA = re.compile(r"(\d{1,2})[./](\d{1,2})[./](\d{4})")
RE_DURATA = re.compile(r"(?:successiv[ei]|prossim[ei])\s+(\d{1,2})(?:\s*[-–÷]\s*(\d{1,2}))?\s*ore", re.IGNORECASE)
# Data di emissione scritta nell'allertamento: protocollo regionale, poi data
# dell'avviso del Dipartimento. Serve solo se una frase dice «domani» senza la
# data: dall'autunno 2026 il nome del file porta il giorno di validità (il PDF
# emesso l'11/11/2026 si chiama «Allertamento12-11-2026.pdf»), non l'emissione.
RE_EMISSIONE = (
    re.compile(r"REGISTRO\s+UFFICIALE\.U\.\d+\.(\d{1,2})-(\d{1,2})-(\d{4})", re.IGNORECASE),
    re.compile(r"avverse\s+n\.?\s*\d+\s+del\s+(\d{1,2})[./](\d{1,2})[./](\d{4})", re.IGNORECASE),
)
# Parole che dicono di quale fenomeno parla una frase, per tipo di avviso. Si
# guarda solo il primo periodo dopo «si prevedono»: nel PDF dell'11/11/2026 la
# frase sulle piogge cita anche le «forti raffiche di vento» dei temporali, ma
# l'avviso per il vento è la frase che comincia con «Venti da forti a burrasca».
PAROLE_TIPO = {
    "vento": r"\bvent[oi]\b",
    "neve": r"\bnev(?:e|i|icat)",
    "ghiaccio e gelate": r"\b(?:gelat|ghiacc)",
    "ondate di calore": r"\b(?:calor|temperatur)",
    "mareggiate": r"\bmareggiat",
    "temporali": r"\btemporal",
}


def _data_emissione_testo(t):
    """Data di emissione scritta nel PDF (protocollo o avviso DPC), o None."""
    for rx in RE_EMISSIONE:
        m = rx.search(t)
        if m:
            try:
                return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)), tzinfo=ROME_TZ)
            except ValueError:
                continue
    return None


def _primo_periodo_previsto(segmento):
    """Primo periodo dopo «si prevedono (sul Lazio):», cioè il fenomeno della frase."""
    m = re.search(r"si\s+prevedono(?:\s+sul\s+Lazio)?\s*:?\s*(.+?)(?:\.\s|\.$|$)", segmento, re.IGNORECASE)
    return m.group(1).strip() if m else ""


def frasi_validita(testo, data_emissione):
    """Frasi dell'allertamento che dicono da quando e per quanto valgono i fenomeni.

    Per ogni frase «dal mattino di domani, giovedì 12.11.2026, e per le successive
    24-36 ore, si prevedono …» restituisce un dizionario con inizio più presto,
    fine più tardi, le parole del bollettino («dal mattino», «24-36 ore») e il
    fenomeno previsto. Una frase senza giorno (né data né oggi/domani) si scarta,
    e così una frase con «domani» senza data se il PDF non scrive la data di
    emissione: contarlo dal nome del file sbaglierebbe di un giorno.
    """
    t = re.sub(r"\s+", " ", testo)
    base_testo = _data_emissione_testo(t)
    trovate = list(RE_INIZIO.finditer(t))
    frasi = []
    for i, m in enumerate(trovate):
        dopo = t[m.end():m.end() + 70]
        mq = RE_QUANDO.match(dopo)
        md = RE_DATA.search(dopo[:50])
        if not mq and not md:
            continue
        quando = (mq.group("quando") or "").lower() if mq else ""
        if md:
            try:
                giorno = datetime(int(md.group(3)), int(md.group(2)), int(md.group(1)), tzinfo=ROME_TZ)
            except ValueError:
                continue
        elif quando and base_testo:
            giorno = base_testo + timedelta(days={"oggi": 0, "domani": 1, "dopodomani": 2}[quando])
        else:
            continue
        idx = next(k for k in range(len(PARTI_DEL_GIORNO)) if m.group(f"p{k}"))
        _, ora_da, ora_a = PARTI_DEL_GIORNO[idx]
        if ora_da is None:  # «dalle ore 12», «dalle ore 18.30»
            ora_da = int(m.group("ora"))
            if ora_da > 24:
                continue
            # Con i minuti la fine si arrotonda all'ora dopo: sempre larga.
            ora_a = ora_da + (1 if int(m.group("minuti") or 0) else 0)
        fine_frase = trovate[i + 1].start() if i + 1 < len(trovate) else len(t)
        segmento = t[m.end():min(fine_frase, m.end() + 600)]
        mdur = RE_DURATA.search(segmento[:160])
        if mdur:
            ore = int(mdur.group(2) or mdur.group(1))
            durata = f"{mdur.group(1)}-{mdur.group(2)} ore" if mdur.group(2) else f"{mdur.group(1)} ore"
        else:
            ore, durata = 36, None
        giorno = giorno.replace(hour=0, minute=0, second=0, microsecond=0)
        frasi.append({
            "inizio": giorno + timedelta(hours=ora_da),
            "fine": giorno + timedelta(hours=ora_a + ore),
            "dal": re.sub(r"\s+", " ", f"{m.group('dal')} {m.group('parte')}".lower()).replace("' ", "'").replace("’ ", "’"),
            "durata": durata,
            "previsto": _primo_periodo_previsto(segmento),
        })
    return frasi


def estrai_validita_e_descrizione(testo, data_emissione, tipo=None):
    """Validità e descrizione dell'avviso dal testo del PDF.

    Restituisce (inizio, fine, descrizione, dal, durata). Inizio e fine sono il
    più presto e il più tardi fra le frasi che parlano del fenomeno dell'avviso
    (``tipo``, es. «vento»); se nessuna frase lo nomina valgono tutte, e se il PDF
    non ha frasi di validità si torna alla regola di prima: dal giorno del file
    per 36 ore. ``dal`` e ``durata`` sono le parole del bollettino della frase
    che comincia per prima («dal mattino», «24-36 ore»), o None.

    Fino all'11/11/2026 si riconosceva solo «dalle prime ore di domani»: per
    «dal mattino di domani, giovedì 12.11.2026, e per le successive 24-36 ore»
    l'avviso del vento risultava valido dal giorno del file per 36 ore, cioè
    fino a venerdì alle 12 invece che fino a sera.
    """
    frasi = frasi_validita(testo, data_emissione)
    scelte = frasi
    parole = [PAROLE_TIPO[p.strip()] for p in (tipo or "").split(",") if p.strip() in PAROLE_TIPO]
    if parole:
        dello_stesso_tipo = [f for f in frasi if any(re.search(rx, f["previsto"], re.IGNORECASE) for rx in parole)]
        if dello_stesso_tipo:
            scelte = dello_stesso_tipo

    descrizione = None
    if scelte:
        prima = min(scelte, key=lambda f: f["inizio"])
        inizio = prima["inizio"]
        fine = max(f["fine"] for f in scelte)
        dal, durata = prima["dal"], prima["durata"]
        descrizione = prima["previsto"] or None
    else:
        inizio = data_emissione
        fine = data_emissione + timedelta(hours=36)
        dal = durata = None

    if not descrizione:
        # Frase tipica "si prevedono sul Lazio:\n<descr>."
        m2 = re.search(r"si\s+prevedono\s+sul\s+Lazio\s*:?\s*\n?\s*([^\n]+?)\.", testo, re.IGNORECASE | re.DOTALL)
        if m2:
            descrizione = m2.group(1).strip()
    if descrizione:
        descrizione = re.sub(r"\s+", " ", descrizione.replace("\n", " "))
        if len(descrizione) > 250:
            descrizione = descrizione[:247] + "..."

    return inizio, fine, descrizione, dal, durata


FONTE = "Allertamenti meteo Regione Lazio"


def segnala_fonte_ko(motivo, fonte=FONTE):
    """Annota una fonte non letta: log del run + file letto dal workflow."""
    print(f"::warning::Fonte non letta — {fonte}: {motivo}")
    percorso = os.environ.get("FONTI_KO_FILE")
    if percorso:
        with open(percorso, "a", encoding="utf-8") as f:
            f.write(f"{fonte}\t{motivo}\n")
    gh_out = os.environ.get("GITHUB_OUTPUT", "")
    if gh_out:
        with open(gh_out, "a") as f:
            f.write("fonti_ko=true\n")


def avviso_scaduto(avviso, now):
    """True se l'avviso salvato ha una validità dichiarata già passata."""
    if not avviso or not avviso.get("validita_fine"):
        return False
    try:
        return now > datetime.fromisoformat(avviso["validita_fine"])
    except ValueError:
        return False


def load_allerta():
    try:
        with open(ALLERTA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_allerta(data):
    with open(ALLERTA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    now = datetime.now(ROME_TZ)

    pdf_paths = []
    errori_indice = []
    for index_url in INDEX_URLS:
        print(f"[{now.isoformat(timespec='seconds')}] check-avvisi-meteo: scarico {index_url}")
        try:
            html = http_get_text(index_url)
        except Exception as e:
            print(f"::warning::Impossibile scaricare la pagina allertamenti: {e}")
            errori_indice.append(f"{index_url}: {e}")
            continue
        pdf_paths = list(dict.fromkeys(PDF_HREF.findall(html)))  # dedup mantenendo ordine
        print(f"Trovati {len(pdf_paths)} PDF candidati nella pagina")
        if pdf_paths:
            break

    if not pdf_paths:
        # La pagina elenca sempre gli allertamenti passati: zero link non vuol dire
        # «nessun avviso», vuol dire che la pagina è cambiata o non risponde. Lo stato
        # resta com'era, salvo un avviso già scaduto, che si toglie comunque.
        segnala_fonte_ko(
            "nessun PDF di allertamento nella pagina (pagina cambiata o non raggiungibile"
            + (f": {'; '.join(errori_indice)}" if errori_indice else "") + "). Avviso lasciato com'era."
        )
        allerta = load_allerta()
        corrente = allerta.get("avviso_meteo")
        scaduto = avviso_scaduto(corrente, now)
        if scaduto:
            print(f"⚠️  Avviso meteo scaduto ({corrente.get('validita_fine')}): lo tolgo")
            del allerta["avviso_meteo"]
            save_allerta(allerta)
        gh_out = os.environ.get("GITHUB_OUTPUT", "")
        if gh_out:
            with open(gh_out, "a") as f:
                f.write(f"changed={'true' if scaduto else 'false'}\n")
        return 0

    # Filtra per data dal nome (lookback)
    candidates = []
    cutoff = now - timedelta(days=LOOKBACK_DAYS)
    # Allertamenti recenti che non si sono potuti leggere: se ce n'è anche uno
    # solo, «nessun avviso in corso» non è una conclusione affidabile.
    non_letti = []
    for path in pdf_paths:
        filename = urllib.parse.unquote(path.rsplit("/", 1)[-1])
        data_pdf = estrai_data_da_nome(filename)
        if data_pdf is None:
            # Senza data nel nome il PDF non si può collocare nel tempo: è un
            # cambio di nomenclatura da riparare, non un PDF da ignorare.
            non_letti.append((None, f"{filename}: data non riconosciuta nel nome"))
            continue
        if data_pdf < cutoff:
            continue
        candidates.append((data_pdf, path, filename))

    candidates.sort(key=lambda x: x[0], reverse=True)  # più recente prima
    print(f"Candidati ultimi {LOOKBACK_DAYS} giorni: {len(candidates)}")

    avviso_attivo = None
    validita_stimata = False
    for data_pdf, path, filename in candidates:
        # Il link può essere relativo o assoluto e contenere spazi
        # («REGISTRO UFFICIALE(U)», «vento 30 03 2026»): si codificano solo quelli.
        full_url = path if path.lower().startswith("http") else BASE_URL + path
        try:
            req = urllib.request.Request(full_url.replace(" ", "%20"), headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                pdf_bytes = r.read()
        except Exception as e:
            print(f"  ⏭️  {filename}: impossibile scaricare ({e})")
            non_letti.append((data_pdf, f"{filename}: non scaricabile ({e})"))
            continue
        if not pdf_bytes.startswith(b"%PDF"):
            print(f"  ⏭️  {filename}: la risposta non è un PDF ({len(pdf_bytes)} bytes)")
            non_letti.append((data_pdf, f"{filename}: la risposta non è un PDF"))
            continue

        try:
            testo = parse_pdf(pdf_bytes)
        except (OSError, subprocess.SubprocessError) as e:
            testo = ""
            print(f"  ⏭️  {filename}: pdftotext non eseguibile ({e})")
        if not testo:
            print(f"  ⏭️  {filename}: pdftotext output vuoto")
            non_letti.append((data_pdf, f"{filename}: testo non estraibile (pdftotext)"))
            continue

        rischio_raw = estrai_rischio(testo)
        if rischio_raw is None:
            # Tutti gli allertamenti regionali riportano «PER I SEGUENTI
            # RISCHI:» (verificato il 17/10/2026): se manca, il modello è cambiato.
            print(f"  ⏭️  {filename}: «PER I SEGUENTI RISCHI» non trovato")
            non_letti.append((data_pdf, f"{filename}: «PER I SEGUENTI RISCHI» non trovato, formato cambiato?"))
            continue
        tipo = classifica_rischio(rischio_raw)
        if not tipo:
            print(f"  ⏭️  {filename}: rischio='{rischio_raw}' (skip, idrogeologico già coperto)")
            continue

        livello = estrai_livello(testo)
        if livello == 0:
            print(f"  ⏭️  {filename}: tipo={tipo} ma nessun livello allerta esplicito")
            continue

        inizio, fine, descrizione, dal, durata = estrai_validita_e_descrizione(testo, data_pdf, tipo)
        stimata = not dal
        motivo_stima = (f"{filename}: validità dell'avviso non trovata nel testo (formato cambiato?), "
                        "stimata dal giorno del file per 36 ore")
        if now > fine:
            if stimata:
                # Scaduto secondo la stima, non secondo il bollettino: non basta
                # per togliere l'avviso salvato (lettura incompleta, segnalata
                # più sotto con le altre).
                non_letti.append((data_pdf, motivo_stima))
            print(f"  ⏭️  {filename}: tipo={tipo}, livello={LEVEL_NAMES[livello]}, ma scaduto ({fine.isoformat()})")
            continue
        if stimata:
            # Nessuna frase «dal mattino di domani, …, e per le successive N ore»:
            # vale la regola di prima (giorno del file per 36 ore), ma è un modello
            # che lo script non conosce e va guardato. Una stima non accorcia la
            # validità dichiarata dell'avviso in vigore (più sotto).
            segnala_fonte_ko(motivo_stima)

        # Trovato un avviso valido. Prendiamo il PIÙ RECENTE che soddisfa.
        avviso_attivo = {
            "tipo": tipo,
            "livello": LEVEL_NAMES[livello],
            "validita_inizio": inizio.isoformat(timespec="seconds"),
            "validita_fine": fine.isoformat(timespec="seconds"),
            "url": full_url.replace(" ", "%20"),
            "fonte_data": data_pdf.date().isoformat(),
        }
        # Le parole del bollettino sulla validità («dal mattino», «24-36 ore»):
        # la home e il messaggio Telegram le mostrano così come sono scritte.
        if dal:
            avviso_attivo["validita_dal"] = dal
        if durata:
            avviso_attivo["validita_durata"] = durata
        if descrizione:
            avviso_attivo["descrizione"] = descrizione
        print(f"  ✅ {filename}: tipo={tipo}, livello={LEVEL_NAMES[livello]}, valido fino a {fine.isoformat(timespec='seconds')}")
        validita_stimata = stimata
        break

    # Aggiorna allerta.json se serve
    allerta = load_allerta()
    avviso_corrente = allerta.get("avviso_meteo")

    # Letture fallite più recenti dell'avviso scelto (o qualsiasi, se non se ne
    # è scelto nessuno): il risultato non è affidabile per togliere o cambiare
    # l'avviso salvato.
    data_scelta = datetime.fromisoformat(avviso_attivo["fonte_data"]).replace(tzinfo=ROME_TZ) if avviso_attivo else None
    dubbi = [m for d, m in non_letti if d is None or data_scelta is None or d >= data_scelta]
    if non_letti:
        segnala_fonte_ko("; ".join(m for _, m in non_letti))

    changed = False
    if dubbi and avviso_corrente and not avviso_scaduto(avviso_corrente, now):
        print("⚠️  Lettura incompleta: l'avviso meteo in vigore resta com'era finché la fonte non si legge di nuovo")
    elif dubbi and not avviso_attivo:
        if avviso_corrente:
            print(f"⚠️  Avviso meteo scaduto ({avviso_corrente.get('validita_fine')}): lo tolgo")
            del allerta["avviso_meteo"]
            changed = True
        else:
            print("ℹ️  Lettura incompleta e nessun avviso salvato: nulla da cambiare")
    elif (avviso_attivo and validita_stimata and avviso_corrente
          and not avviso_scaduto(avviso_corrente, now)
          and avviso_corrente.get("tipo") == avviso_attivo["tipo"]
          and avviso_corrente.get("livello") == avviso_attivo["livello"]):
        # Stesso tipo e livello, ma la validità del bollettino nuovo è solo una
        # stima: resta quella dichiarata dall'avviso in vigore, fino alla sua
        # scadenza (revisione dell'11/11/2026: le 36 ore presunte anticipavano
        # dal 14 alle 0 al 13 alle 12 la fine di un avviso ancora valido). Un tipo
        # o un livello diversi sono informazione nuova e si salvano (ramo sotto).
        print("⚠️  Validità del bollettino nuovo non letta: l'avviso in vigore resta com'era "
              f"fino a {avviso_corrente.get('validita_fine')}")
    elif avviso_attivo:
        # Si salva ogni cambio dell'avviso, anche con lo stesso tipo e livello:
        # un bollettino nuovo che sposta o allunga la validità, o cambia il testo,
        # deve arrivare sul sito. Fino all'11/11/2026 si salvava solo al cambio
        # di tipo o livello, e una validità corretta non arrivava mai. Il
        # messaggio Telegram resta legato al solo cambio di tipo o livello
        # (notifica-telegram.py), quindi qui non nasce nessun messaggio in più.
        if avviso_corrente != avviso_attivo:
            if not avviso_corrente or avviso_corrente.get("tipo") != avviso_attivo["tipo"] or avviso_corrente.get("livello") != avviso_attivo["livello"]:
                print(f"⚠️  Aggiornamento avviso_meteo: {avviso_corrente.get('tipo') if avviso_corrente else 'nessuno'} → {avviso_attivo['tipo']} ({avviso_attivo['livello']})")
            else:
                print(f"ℹ️  Avviso meteo {avviso_attivo['tipo']} ({avviso_attivo['livello']}): aggiornati validità o testo "
                      f"({avviso_attivo['validita_inizio']} → {avviso_attivo['validita_fine']})")
            changed = True
        allerta["avviso_meteo"] = avviso_attivo
    elif avviso_corrente:
        print(f"⚠️  Avviso meteo cessato: era {avviso_corrente.get('tipo')} ({avviso_corrente.get('livello')})")
        del allerta["avviso_meteo"]
        changed = True
    else:
        print("ℹ️  Nessun avviso meteo attivo (né prima né adesso)")

    if changed:
        save_allerta(allerta)
        print("✓ data/allerta.json aggiornato")

    gh_out = os.environ.get("GITHUB_OUTPUT", "")
    if gh_out:
        with open(gh_out, "a") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")
            if avviso_attivo:
                f.write(f"tipo={avviso_attivo['tipo']}\n")
                f.write(f"livello={avviso_attivo['livello']}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
