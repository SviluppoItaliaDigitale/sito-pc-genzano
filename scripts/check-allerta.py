#!/usr/bin/env python3
"""
Aggiorna data/allerta.json con i dati di criticità idrogeologica/idraulica
per Genzano di Roma (Zona F — Bacini Costieri Sud) leggendo:

1. Fonte PRIMARIA: CSV opendatasicilia (mirror DPC nazionale)
   - bollettino-oggi-comuni-latest.csv
   - bollettino-domani-comuni-latest.csv

2. Fonte di FALLBACK: PDF firmato Regione Lazio
   /sites/.../tbl_bollettini_criticita/bollettino_DD_MM_AAAA.pdf
   Attivato SOLO se opendatasicilia non risponde su entrambi i file CSV
   (entrambi != raggiungibili, non solo uno). Il fallback parsa il PDF
   con pdftotext -layout ed estrae le tabelle "Valutazioni per OGGI" e
   "Valutazioni per DOMANI" per la Zona F.

Logica: filtra per data_validita_inizio ≤ now ≤ data_validita_fine (tz
Europe/Rome), prende il MAX livello tra i bollettini validi, espone anche
un blocco "domani" separato come pre-allerta (solo se data_validita_inizio
strettamente futura rispetto a today).

Output GH:
- changed=true|false
- old_level / new_level
- descrizione / motivo
- level_changed=true|false
- source=opendatasicilia|pdf-regione-lazio|misto
"""

import csv
import io
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
ALLERTA_PATH = ROOT / "data" / "allerta.json"

CSV_URLS = {
    "oggi": (
        "https://raw.githubusercontent.com/opendatasicilia/"
        "DPC-bollettini-criticita-idrogeologica-idraulica/"
        "refs/heads/main/data/bollettini/bollettino-oggi-comuni-latest.csv"
    ),
    "domani": (
        "https://raw.githubusercontent.com/opendatasicilia/"
        "DPC-bollettini-criticita-idrogeologica-idraulica/"
        "refs/heads/main/data/bollettini/bollettino-domani-comuni-latest.csv"
    ),
}
PDF_REGIONE_BASE = (
    "https://protezionecivile.regione.lazio.it/sites/default/files/binary/"
    "rl_protezione_civile/tbl_bollettini_criticita/bollettino_"
)

COMUNE = "Genzano di Roma"
ZONA_GENZANO = "F"  # Bacini Costieri Sud
USER_AGENT = "PC-Genzano-Bot/1.0"
HTTP_TIMEOUT = 30

ROME_TZ = ZoneInfo("Europe/Rome")

LEVEL_NAME = {0: "verde", 1: "gialla", 2: "arancione", 3: "rossa"}
LEVEL_FROM_PDF = {"VERDE": 0, "GIALLO": 1, "GIALLA": 1, "ARANCIONE": 2, "ROSSO": 3, "ROSSA": 3}

RISK_FIELDS = {
    "avviso_idrogeologico": "rischio idrogeologico",
    "avviso_temporali": "temporali",
    "avviso_idraulico": "rischio idraulico",
}

TITLES = {
    "verde": "NESSUNA ALLERTA",
    "gialla": "ALLERTA GIALLA",
    "arancione": "ALLERTA ARANCIONE",
    "rossa": "ALLERTA ROSSA",
}

BASE_DESCS = {
    "verde": "Non sono previsti fenomeni significativi sul nostro territorio.",
    "gialla": "Prestare attenzione.",
    "arancione": "Limitare gli spostamenti.",
    "rossa": "Seguire le indicazioni delle autorità.",
}

MESI_IT = [
    "", "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno",
    "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre",
]
# Genzano è in Zona di Allerta Lazi-F = "Bacini Costieri Sud" (Centro Funzionale
# Regionale Lazio, DGR 865 del 26/11/2019). Hardcoded perché vale sempre per
# questo sito (un solo Comune monitorato).
ZONA_NAME_BREVE = "Zona F"
ZONA_NAME_LUNGO = "Zona F — Bacini Costieri Sud (Genzano)"


def costruisci_descrizione_ricca(row, livello, rischi_attivi):
    """Combina i dati grezzi del CSV in una descrizione AGID dettagliata.

    Forma desiderata (esempio gialla per temporali):
      "Ordinaria per rischio temporali, Zona F — Bacini Costieri Sud (Genzano).
      Bollettino DPC/Regione Lazio del 12 maggio 2026,
      validità 13 maggio 00:00–23:59."

    Per livello verde: descrizione standard generica (BASE_DESCS).
    Per livelli ≥ gialla: combina avviso_criticita CSV + zona + finestra
    di validità formattata in italiano.
    """
    if livello == "verde" or not row:
        return BASE_DESCS[livello]

    # Frase fenomeno dal CSV: "Ordinaria per rischio temporali / ALLERTA GIALLA"
    # → tieni solo la parte PRIMA dello slash
    crit_raw = row.get("avviso_criticita", "") or ""
    if "/" in crit_raw:
        fenomeno = crit_raw.split("/")[0].strip()
    else:
        fenomeno = crit_raw.strip()
    if not fenomeno:
        # Fallback: usa BASE_DESCS
        fenomeno = BASE_DESCS[livello]

    parts = [f"{fenomeno}, {ZONA_NAME_LUNGO}."]

    # Date emissione + finestra validità
    pub = parse_iso(row.get("data_pubblicazione", ""))
    val_inizio = parse_iso(row.get("data_validita_inizio", ""))
    val_fine = parse_iso(row.get("data_validita_fine", ""))
    if pub and val_inizio and val_fine:
        bol_data = f"{pub.day} {MESI_IT[pub.month]} {pub.year}"
        val_giorno = f"{val_inizio.day} {MESI_IT[val_inizio.month]}"
        val_h = f"{val_inizio.strftime('%H:%M')}–{val_fine.strftime('%H:%M')}"
        parts.append(f"Bollettino DPC/Regione Lazio del {bol_data}, validità {val_giorno} {val_h}.")

    return " ".join(parts)


def costruisci_titolo_ricco(livello, rischi_attivi):
    """Titolo banner: 'ALLERTA <LIV>' + ' — <lista rischi>' se ce ne sono.

    Esempi:
    - verde: "NESSUNA ALLERTA"
    - gialla con temporali: "ALLERTA GIALLA — temporali"
    - arancione con temporali + idrogeologico: "ALLERTA ARANCIONE — temporali, rischio idrogeologico"
    """
    base = TITLES[livello]
    if livello == "verde" or not rischi_attivi:
        return base
    return f"{base} — {', '.join(rischi_attivi)}"


def http_get_text(url, timeout=HTTP_TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8")


def http_get_bytes(url, timeout=HTTP_TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_csv(url, label):
    """Scarica un CSV opendatasicilia. Ritorna riga Comune o None se fallisce."""
    try:
        data = http_get_text(url)
    except Exception as e:
        print(f"::warning::CSV {label} non disponibile: {e}")
        return None
    reader = csv.DictReader(io.StringIO(data))
    for row in reader:
        if row.get("comune_nome", "").strip() == COMUNE:
            return row
    print(f"::warning::{COMUNE} non trovato nel CSV {label}")
    return None


def pdftotext_layout(pdf_bytes):
    """Estrae testo PDF preservando layout."""
    try:
        res = subprocess.run(
            ["pdftotext", "-layout", "-", "-"],
            input=pdf_bytes,
            capture_output=True,
            timeout=30,
        )
        if res.returncode != 0:
            return ""
        return res.stdout.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"::warning::pdftotext error: {e}")
        return ""


def parse_pdf_regione(testo, zona=ZONA_GENZANO):
    """Estrae da PDF Regione Lazio le righe Zona X per OGGI e DOMANI.

    Output: {"oggi": (idrogeo_level, temporali_level, idraulico_level) | None,
             "domani": (idrogeo_level, temporali_level, idraulico_level) | None,
             "data_oggi": "YYYY-MM-DD", "data_domani": "YYYY-MM-DD"}
    """
    out = {"oggi": None, "domani": None, "data_oggi": None, "data_domani": None}

    # Spezza il testo nelle due sezioni
    m_oggi = re.search(r"Valutazioni\s+per\s+OGGI,\s*(\d{2})/(\d{2})/(\d{4})", testo)
    m_dom = re.search(r"Valutazioni\s+per\s+DOMANI,\s*(\d{2})/(\d{2})/(\d{4})", testo)
    if m_oggi:
        out["data_oggi"] = f"{m_oggi.group(3)}-{m_oggi.group(2)}-{m_oggi.group(1)}"
    if m_dom:
        out["data_domani"] = f"{m_dom.group(3)}-{m_dom.group(2)}-{m_dom.group(1)}"

    if not m_oggi:
        print("::warning::PDF: 'Valutazioni per OGGI' non trovate")
        return out

    inizio_oggi = m_oggi.end()
    inizio_dom = m_dom.start() if m_dom else len(testo)
    sez_oggi = testo[inizio_oggi:inizio_dom]
    sez_dom = testo[m_dom.end():] if m_dom else ""

    # Pattern riga zona: "F     VERDE    GIALLO   VERDE" (con spazi variabili)
    livelli_pat = r"(VERDE|GIALLO|GIALLA|ARANCIONE|ROSSO|ROSSA)"
    row_pat = re.compile(rf"^\s*{zona}\s+{livelli_pat}\s+{livelli_pat}\s+{livelli_pat}\s*$", re.MULTILINE)

    m1 = row_pat.search(sez_oggi)
    if m1:
        out["oggi"] = (LEVEL_FROM_PDF[m1.group(1)], LEVEL_FROM_PDF[m1.group(2)], LEVEL_FROM_PDF[m1.group(3)])
        print(f"PDF Zona {zona} OGGI: idrogeo={m1.group(1)}, temp={m1.group(2)}, idraul={m1.group(3)}")
    else:
        print(f"::warning::PDF: zona {zona} non trovata in 'Valutazioni per OGGI'")

    m2 = row_pat.search(sez_dom)
    if m2:
        out["domani"] = (LEVEL_FROM_PDF[m2.group(1)], LEVEL_FROM_PDF[m2.group(2)], LEVEL_FROM_PDF[m2.group(3)])
        print(f"PDF Zona {zona} DOMANI: idrogeo={m2.group(1)}, temp={m2.group(2)}, idraul={m2.group(3)}")

    return out


def fallback_pdf_regione_lazio(now):
    """Fallback: scarica e parsa il PDF Regione Lazio del giorno corrente
    (o del precedente se quello di oggi non è ancora online).
    Ritorna un dict label → row in formato CSV-compatibile, in modo che
    la logica downstream funzioni invariata."""
    candidates_dates = [now.date(), (now - timedelta(days=1)).date()]
    pdf_text = None
    pdf_date = None
    for d in candidates_dates:
        url = PDF_REGIONE_BASE + d.strftime("%d_%m_%Y") + ".pdf"
        try:
            pdf_bytes = http_get_bytes(url)
            pdf_text = pdftotext_layout(pdf_bytes)
            if pdf_text:
                pdf_date = d
                print(f"📄 Fallback: PDF Regione Lazio del {d.isoformat()} scaricato ({len(pdf_bytes)} bytes)")
                break
        except Exception as e:
            print(f"  ⏭️  PDF del {d.isoformat()} non disponibile: {e}")

    if not pdf_text:
        return {}

    parsed = parse_pdf_regione(pdf_text, zona=ZONA_GENZANO)
    if not parsed["oggi"] and not parsed["domani"]:
        return {}

    bollettini_finti = {}

    def make_row(levels_tuple, data_str):
        idrogeo_n, temp_n, idraul_n = levels_tuple
        max_n = max(idrogeo_n, temp_n, idraul_n)
        # Costruisci stringhe coerenti con quelle del CSV: "Ordinaria per … / ALLERTA GIALLA"
        def lev_to_str(n, is_temp=False):
            if n == 0:
                return "Assenza di fenomeni significativi prevedibili / NESSUNA ALLERTA"
            if n == 1:
                return ("Ordinaria per rischio temporali / ALLERTA GIALLA" if is_temp
                        else "Ordinaria / ALLERTA GIALLA")
            if n == 2:
                return "Moderata / ALLERTA ARANCIONE"
            if n == 3:
                return "Elevata / ALLERTA ROSSA"
            return ""
        inizio = data_str + "T00:00:00+02:00"
        fine = data_str + "T23:59:59+02:00"
        return {
            "comune_nome": COMUNE,
            "data_validita_inizio": inizio,
            "data_validita_fine": fine,
            "avviso_idrogeologico": lev_to_str(idrogeo_n),
            "avviso_temporali": lev_to_str(temp_n, is_temp=True),
            "avviso_idraulico": lev_to_str(idraul_n),
            "avviso_criticita": lev_to_str(max_n),
        }

    if parsed["oggi"] and parsed["data_oggi"]:
        bollettini_finti["oggi"] = make_row(parsed["oggi"], parsed["data_oggi"])
    if parsed["domani"] and parsed["data_domani"]:
        bollettini_finti["domani"] = make_row(parsed["domani"], parsed["data_domani"])

    return bollettini_finti


def extract_level(value):
    v = (value or "").lower()
    if "allerta rossa" in v:
        return 3
    if "allerta arancione" in v:
        return 2
    if "allerta gialla" in v:
        return 1
    return 0


def parse_iso(s):
    try:
        return datetime.fromisoformat(s)
    except Exception:
        return None


def gh_output(**kwargs):
    gh_out = os.environ.get("GITHUB_OUTPUT", "")
    if not gh_out:
        return
    with open(gh_out, "a") as f:
        for k, v in kwargs.items():
            f.write(f"{k}={v}\n")


def main():
    now = datetime.now(ROME_TZ)

    # ── 1. Tenta fonte primaria opendatasicilia ──
    bollettini = {}
    for label, url in CSV_URLS.items():
        row = fetch_csv(url, label)
        if row:
            bollettini[label] = row

    # ── 1-bis. Fallback PDF Regione Lazio se ENTRAMBI i CSV mancano ──
    source = "opendatasicilia"
    if not bollettini:
        print("⚠️  Entrambi i CSV opendatasicilia irraggiungibili: attivo fallback PDF Regione Lazio")
        bollettini = fallback_pdf_regione_lazio(now)
        if bollettini:
            source = "pdf-regione-lazio"
        else:
            print("::warning::Anche il fallback PDF ha fallito. Non aggiorno allerta.json")
            gh_output(changed="false", source="none")
            sys.exit(0)
    elif len(bollettini) < 2:
        # Solo uno dei due CSV è arrivato. Tentiamo di completare via PDF
        # ma SOLO se possiamo (e ricomponendo: NON sovrascrivere il CSV
        # che c'è già). Strategia conservativa: NON attiviamo fallback per
        # "solo uno", perché un fetch a vuoto su un singolo CSV è rumore
        # comune (es. CDN GitHub temporaneamente). La logica MAX time-aware
        # downstream gestisce gracefully il caso "solo oggi" o "solo domani".
        print(f"ℹ️  Solo CSV {list(bollettini.keys())} disponibile, non attivo fallback (rumore CDN)")

    print(f"Fonte attiva: {source}, bollettini ricevuti: {list(bollettini.keys())}")

    # ── 2. Filtra bollettini VALIDI ADESSO ──
    attivi = {}
    for label, row in bollettini.items():
        inizio = parse_iso(row.get("data_validita_inizio", ""))
        fine = parse_iso(row.get("data_validita_fine", ""))
        if inizio and fine and inizio <= now <= fine:
            attivi[label] = row
            print(f"✅ Bollettino {label} ATTIVO (validità {inizio} → {fine})")
        else:
            print(f"⏭️  Bollettino {label} fuori validità (inizio={inizio}, fine={fine})")

    if not attivi:
        fallback_key = "domani" if "domani" in bollettini else ("oggi" if "oggi" in bollettini else None)
        if fallback_key:
            attivi = {fallback_key: bollettini[fallback_key]}
            print(f"::warning::Nessun bollettino in finestra di validità, uso {fallback_key} come fallback")

    if not attivi:
        gh_output(changed="false", source=source)
        sys.exit(0)

    # ── 3. MAX livello combinando i bollettini attivi ──
    max_level = 0
    active_risks_set = set()
    active_risks_order = []
    bollettino_attivo_label = None

    for label, row in attivi.items():
        crit_level = extract_level(row.get("avviso_criticita", ""))
        if crit_level > max_level:
            max_level = crit_level
            bollettino_attivo_label = label
        for field, risk_label in RISK_FIELDS.items():
            level = extract_level(row.get(field, ""))
            if level > 0 and risk_label not in active_risks_set:
                active_risks_set.add(risk_label)
                active_risks_order.append(risk_label)
            if level > max_level:
                max_level = level
                bollettino_attivo_label = label

    if bollettino_attivo_label is None:
        bollettino_attivo_label = next(iter(attivi))

    active_risks = active_risks_order
    livello = LEVEL_NAME[max_level]
    print(f"📊 MAX level={livello}, dal bollettino '{bollettino_attivo_label}'")

    # ── 3-bis. Blocco "domani" SEPARATO se data_validita_inizio > today ──
    domani_block = None
    if "domani" in bollettini:
        row_d = bollettini["domani"]
        inizio_d = parse_iso(row_d.get("data_validita_inizio", ""))
        today_in_rome = now.date()
        if inizio_d and inizio_d.date() > today_in_rome:
            max_dom = 0
            risks_dom_order = []
            risks_dom_set = set()
            crit_d = extract_level(row_d.get("avviso_criticita", ""))
            if crit_d > max_dom:
                max_dom = crit_d
            for field, risk_label in RISK_FIELDS.items():
                lev_d = extract_level(row_d.get(field, ""))
                if lev_d > 0 and risk_label not in risks_dom_set:
                    risks_dom_set.add(risk_label)
                    risks_dom_order.append(risk_label)
                if lev_d > max_dom:
                    max_dom = lev_d
            liv_dom = LEVEL_NAME[max_dom]
            titolo_dom = {
                "verde": "Previsto verde",
                "gialla": "Previsto giallo",
                "arancione": "Previsto arancione",
                "rossa": "Previsto rosso",
            }[liv_dom]
            domani_block = {
                "livello": liv_dom,
                "titolo": titolo_dom,
                "rischi": risks_dom_order,
                "data": inizio_d.date().isoformat(),
            }
            print(f"📅 Bollettino DOMANI ({inizio_d.date()}): {liv_dom}, rischi={risks_dom_order}")

    # ── 4. Costruisci titolo e descrizione ricca ──
    # Il titolo include la lista rischi attivi (es. "ALLERTA GIALLA — temporali").
    # La descrizione integra: frase fenomeno DPC + zona Lazi-F + data emissione
    # bollettino + finestra validità (es. "Ordinaria per rischio temporali,
    # Zona F — Bacini Costieri Sud (Genzano). Bollettino DPC/Regione Lazio del
    # 12 maggio 2026, validità 13 maggio 00:00–23:59.").
    # Il dato grezzo del CSV opendatasicilia ha già tutti i campi necessari.
    titolo = costruisci_titolo_ricco(livello, active_risks)
    # Per la descrizione passo la riga "vincente" dell'attivo (quella che ha
    # determinato il MAX); per livello verde la riga può essere None.
    row_per_descr = attivi.get(bollettino_attivo_label) if bollettino_attivo_label else None
    descrizione = costruisci_descrizione_ricca(row_per_descr, livello, active_risks)

    timestamp_now = now.isoformat(timespec="seconds")

    # ── 5. Diff vs stato corrente ──
    try:
        with open(ALLERTA_PATH, "r", encoding="utf-8") as f:
            current = json.load(f)
    except Exception:
        current = {}

    old_level = current.get("livello", "sconosciuto")
    level_changed = current.get("livello") != livello
    old_domani_level = ((current.get("domani") or {}).get("livello") or "verde")
    new_domani_level = (domani_block.get("livello") if domani_block else "verde")
    domani_level_changed = old_domani_level != new_domani_level

    stale_check = True
    last_check_str = current.get("ultimo_controllo") or current.get("ultimo_aggiornamento")
    if last_check_str:
        try:
            last_check = datetime.fromisoformat(last_check_str)
            if (now - last_check) < timedelta(hours=5, minutes=45):
                stale_check = False
        except Exception:
            pass

    if not level_changed and not domani_level_changed and not stale_check:
        print(f"✅ Livello invariato (oggi={livello}, domani={new_domani_level}) e ultimo controllo recente: skip commit")
        gh_output(changed="false", source=source)
        sys.exit(0)

    # ── 6. Aggiorna allerta.json ──
    if level_changed:
        ultimo_aggiornamento = timestamp_now
        motivo = f"livello {old_level} → {livello}"
    elif domani_level_changed:
        ultimo_aggiornamento = current.get("ultimo_aggiornamento", timestamp_now)
        motivo = f"pre-allerta domani {old_domani_level} → {new_domani_level} (oggi invariato: {livello})"
    else:
        ultimo_aggiornamento = current.get("ultimo_aggiornamento", timestamp_now)
        motivo = f"controllo periodico (livello invariato: {livello})"

    new_data = {
        "livello": livello,
        "titolo": titolo,
        "descrizione": descrizione,
        "ultimo_aggiornamento": ultimo_aggiornamento,
        "ultimo_controllo": timestamp_now,
    }
    if domani_block:
        new_data["domani"] = domani_block

    # Preserva avviso_meteo se esiste già (script avvisi-meteo lo gestisce separatamente)
    if current.get("avviso_meteo"):
        new_data["avviso_meteo"] = current["avviso_meteo"]

    with open(ALLERTA_PATH, "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"⚠️  Aggiornamento: {motivo} (source={source})")
    gh_output(
        changed="true",
        old_level=old_level,
        new_level=livello,
        descrizione=descrizione,
        motivo=motivo,
        level_changed=("true" if level_changed else "false"),
        source=source,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
