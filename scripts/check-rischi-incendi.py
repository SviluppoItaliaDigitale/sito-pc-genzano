#!/usr/bin/env python3
"""
Aggiorna data/allerta.json con il blocco "rischio_incendi" leggendo il
"Bollettino di Pericolosità da Incendi Boschivi" della Regione Lazio
(campagna AIB, di norma giugno-ottobre).

Fonte: https://protezionecivile.regione.lazio.it/.../tbl_rischio_incendi/
       Bollettino AIB Lazio_DD_MM_YYYY.pdf

Struttura del PDF:
- Pagina "Previsioni per oggi DD-MM-YYYY": tabella con 14 Zone AIB
  (1..14) e 14 livelli (BASSO/MEDIO/MODERATO/ELEVATO)
- Pagina "Previsioni per domani DD-MM-YYYY": idem

Genzano di Roma è in ZONA AIB 9 (confermato dal PDF ufficiale
"Tabelle Comuni_Zone Allerta AIB" 2019).

Logica:
1. Scarica PDF di oggi (giorno corrente, Europe/Rome). Se 404, prova ieri.
2. Parsa entrambe le sezioni oggi+domani.
3. Estrae il livello della Zona 9.
4. Mostra fascia in homepage SOLO se livello-oggi >= MEDIO (perché
   BASSO è la baseline estiva e creerebbe rumore).
5. Mantiene anche il livello DOMANI come pre-allerta (idem soglia).

Mapping livelli AIB → palette PC del sito (allineata ai bollettini meteo):
- BASSO     → "verde"      (NON mostrare, baseline)
- MEDIO     → "gialla"     (mostrare)
- MODERATO  → "arancione"  (mostrare)
- ELEVATO   → "rossa"      (mostrare)

Anti-spam: aggiorna allerta.json solo se cambia livello-oggi o livello-domani
del rischio incendi. Fuori stagione (no PDF di oggi né di ieri), rimuove
il blocco rischio_incendi se esisteva (cessazione automatica).
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

ROME_TZ = ZoneInfo("Europe/Rome")
USER_AGENT = "PC-Genzano-Bot/1.0"
HTTP_TIMEOUT = 30

# Genzano di Roma è in Zona AIB 9 (Castelli Romani, area sud Roma)
ZONA_AIB_GENZANO = 9

# I PDF AIB hanno nome variabile, due pattern frequenti:
PDF_NAME_PATTERNS = [
    "Bollettino AIB Lazio_{date}.pdf",
    "BollettinoAIB_{date}.pdf",
]
PDF_BASE_URL = (
    "https://protezionecivile.regione.lazio.it/sites/default/files/binary/"
    "rl_protezione_civile/tbl_rischio_incendi/"
)

LIVELLI_AIB = {"BASSO": 0, "MEDIO": 1, "MODERATO": 2, "ELEVATO": 3}
LIVELLO_PC = {0: "verde", 1: "gialla", 2: "arancione", 3: "rossa"}
LIVELLO_TITOLO = {
    "verde": "Pericolosità BASSA",
    "gialla": "Pericolosità MEDIA",
    "arancione": "Pericolosità MODERATA",
    "rossa": "Pericolosità ELEVATA",
}


def http_get_bytes(url, timeout=HTTP_TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def pdftotext_layout(pdf_bytes):
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


def scarica_pdf_aib(now):
    """Tenta di scaricare il PDF AIB di oggi, poi di ieri. Ritorna (bytes, data) o (None, None)."""
    candidates = [now.date(), (now - timedelta(days=1)).date()]
    for d in candidates:
        date_str = d.strftime("%d_%m_%Y")
        for pat in PDF_NAME_PATTERNS:
            url = PDF_BASE_URL + urllib.parse.quote(pat.format(date=date_str))
            try:
                pdf_bytes = http_get_bytes(url)
                print(f"📄 PDF AIB {date_str} scaricato ({len(pdf_bytes)} bytes) da {pat}")
                return pdf_bytes, d
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    continue
                print(f"::warning::Errore HTTP {e.code} per {url}")
            except Exception as e:
                print(f"::warning::Errore scaricamento {url}: {e}")
    return None, None


def estrai_zona_livello(testo, zona_numero):
    """Cerca la riga con 14 livelli AIB consecutivi e ritorna quello della zona richiesta.

    Pattern del PDF: dopo "Zona AIB 1 2 ... 14" c'è "Livello\nPericolosità"
    poi una riga con 14 token in {BASSO, MEDIO, MODERATO, ELEVATO}.
    """
    livelli_validi = set(LIVELLI_AIB.keys())
    for riga in testo.split("\n"):
        tokens = riga.split()
        if len(tokens) == 14 and all(t in livelli_validi for t in tokens):
            return tokens[zona_numero - 1]  # 1-indexed
    # Fallback: pattern più tollerante (es. riga si è spezzata su più linee)
    parole = testo.split()
    sequenze = []
    for i in range(len(parole) - 13):
        seq = parole[i:i + 14]
        if all(t in livelli_validi for t in seq):
            sequenze.append(seq)
    if sequenze:
        # Prendi la PRIMA sequenza (è quella per "oggi"; la seconda sarebbe "domani")
        return sequenze[0][zona_numero - 1]
    return None


def estrai_zona_livello_oggi_e_domani(testo, zona_numero):
    """Estrae i livelli OGGI e DOMANI dalla Zona N. Il PDF ha 2 sezioni separate."""
    # Spezza il testo nelle due sezioni
    m_oggi = re.search(r"Previsioni\s+per\s+oggi\s+(\d{2})-(\d{2})-(\d{4})", testo)
    m_dom = re.search(r"Previsioni\s+per\s+domani\s+(\d{2})-(\d{2})-(\d{4})", testo)

    data_oggi = None
    data_domani = None
    if m_oggi:
        data_oggi = f"{m_oggi.group(3)}-{m_oggi.group(2)}-{m_oggi.group(1)}"
    if m_dom:
        data_domani = f"{m_dom.group(3)}-{m_dom.group(2)}-{m_dom.group(1)}"

    start_oggi = m_oggi.end() if m_oggi else 0
    start_dom = m_dom.start() if m_dom else len(testo)
    sez_oggi = testo[start_oggi:start_dom]
    sez_dom = testo[m_dom.end():] if m_dom else ""

    liv_oggi = estrai_zona_livello(sez_oggi, zona_numero)
    liv_domani = estrai_zona_livello(sez_dom, zona_numero) if sez_dom else None

    return liv_oggi, liv_domani, data_oggi, data_domani


def aib_to_pc(livello_aib):
    """Mappa BASSO/MEDIO/MODERATO/ELEVATO → palette PC verde/gialla/arancione/rossa."""
    if not livello_aib:
        return None
    n = LIVELLI_AIB.get(livello_aib.upper())
    if n is None:
        return None
    return LIVELLO_PC[n]


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
    print(f"[{now.isoformat(timespec='seconds')}] check-rischi-incendi (Zona AIB {ZONA_AIB_GENZANO})")

    pdf_bytes, pdf_date = scarica_pdf_aib(now)
    if not pdf_bytes:
        # Fuori stagione: niente PDF disponibile. Rimuovi blocco se esisteva.
        allerta = load_allerta()
        if "rischio_incendi" in allerta:
            print("⚠️  Nessun PDF AIB disponibile → cessazione automatica blocco rischio_incendi")
            del allerta["rischio_incendi"]
            save_allerta(allerta)
            gh_out = os.environ.get("GITHUB_OUTPUT", "")
            if gh_out:
                with open(gh_out, "a") as f:
                    f.write("changed=true\n")
        else:
            print("ℹ️  Fuori stagione AIB (nessun PDF e nessun blocco precedente)")
            gh_out = os.environ.get("GITHUB_OUTPUT", "")
            if gh_out:
                with open(gh_out, "a") as f:
                    f.write("changed=false\n")
        return 0

    testo = pdftotext_layout(pdf_bytes)
    if not testo:
        print("::warning::pdftotext output vuoto, skip")
        return 0

    liv_oggi_aib, liv_dom_aib, data_oggi, data_dom = estrai_zona_livello_oggi_e_domani(
        testo, ZONA_AIB_GENZANO
    )
    print(f"  OGGI ({data_oggi}): Zona {ZONA_AIB_GENZANO} = {liv_oggi_aib}")
    print(f"  DOMANI ({data_dom}): Zona {ZONA_AIB_GENZANO} = {liv_dom_aib}")

    livello_oggi = aib_to_pc(liv_oggi_aib)
    livello_dom = aib_to_pc(liv_dom_aib)

    if not livello_oggi:
        print(f"::warning::Zona {ZONA_AIB_GENZANO} non trovata nel PDF AIB del {pdf_date}")
        return 0

    # Costruisci blocco rischio_incendi
    # Mostra in homepage solo se livello-oggi >= gialla (MEDIO)
    # Tuttavia salviamo sempre il blocco con il livello, e il template decide
    # se mostrarlo. Così abbiamo anche il dato "BASSO" per audit/log.
    rischio_block = {
        "livello": livello_oggi,
        "livello_aib": liv_oggi_aib,
        "titolo": LIVELLO_TITOLO[livello_oggi],
        "zona_aib": ZONA_AIB_GENZANO,
        "data": data_oggi,
        "fonte": "Regione Lazio — Centro Funzionale (modello RISICOLazio + Fondazione CIMA)",
    }
    if livello_dom:
        # Solo se la data domani è strettamente futura rispetto a oggi italiano
        try:
            data_dom_dt = datetime.strptime(data_dom, "%Y-%m-%d").date() if data_dom else None
        except ValueError:
            data_dom_dt = None
        if data_dom_dt and data_dom_dt > now.date():
            rischio_block["domani"] = {
                "livello": livello_dom,
                "livello_aib": liv_dom_aib,
                "data": data_dom,
            }

    allerta = load_allerta()
    current = allerta.get("rischio_incendi", {})
    changed = (
        current.get("livello") != rischio_block["livello"]
        or current.get("livello_aib") != rischio_block["livello_aib"]
        or (current.get("domani") or {}).get("livello") != (rischio_block.get("domani") or {}).get("livello")
    )

    if changed:
        old = current.get("livello_aib") or "—"
        new = rischio_block["livello_aib"]
        print(f"⚠️  Aggiornamento rischio_incendi: {old} → {new}")
        allerta["rischio_incendi"] = rischio_block
        save_allerta(allerta)
    else:
        print(f"✅ Rischio incendi invariato ({rischio_block['livello_aib']}), skip")

    gh_out = os.environ.get("GITHUB_OUTPUT", "")
    if gh_out:
        with open(gh_out, "a") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")
            f.write(f"livello={rischio_block['livello']}\n")
            f.write(f"livello_aib={rischio_block['livello_aib']}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
