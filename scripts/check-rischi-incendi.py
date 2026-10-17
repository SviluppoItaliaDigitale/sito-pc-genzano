#!/usr/bin/env python3
"""
Aggiorna data/allerta.json con il blocco "rischio_incendi" leggendo il
"Bollettino di Pericolosità da Incendi Boschivi" della Regione Lazio
(campagna AIB, di norma giugno-ottobre).

Fonte: https://www.regione.lazio.it/sites/default/files/rischio-incendi/<anno>/
       Bollettino AIB Lazio_DD_MM_YYYY.pdf (elenco nella pagina
       https://www.regione.lazio.it/protezione-civile/centro-funzionale-regionale/bollettini-rischi-incendi)

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
del rischio incendi.

Fuori stagione e guasti (17/10/2026). I PDF si cercano nella pagina elenco dei
bollettini, non solo a nome indovinato: il 15/10/2026 il bollettino è uscito
come «Bollettino AIB Lazio_15_10_2026_0.pdf» e un nome cambiato dava 404, che
lo script prendeva per «fuori stagione» togliendo il blocco. Ora:
- pagina letta, con bollettini elencati ma nessuno di oggi o di ieri →
  fuori stagione (fonte letta, nulla in corso): il blocco si toglie;
- pagina non letta o senza nessun bollettino, PDF non scaricabile, testo non
  estraibile, Zona 9 non trovata → fonte NON letta: il blocco resta com'era
  (salvo che la sua data sia già passata: lo si toglie perché scaduto) e il
  guasto si annota in $FONTI_KO_FILE e in GITHUB_OUTPUT fonti_ko=true, per la
  issue `fonte-rotta` del workflow. Uscita sempre 0.
"""

import json
import os
import re
import subprocess
import sys
import urllib.error
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
# Dall'autunno 2026 i bollettini stanno sul portale www.regione.lazio.it, nella
# cartella rischio-incendi/<anno>/ (pagina «Bollettini di Pericolosità incendi
# boschivi»). Il vecchio indirizzo su protezionecivile.regione.lazio.it risponde
# con la home della protezione civile regionale (200, HTML) e lo script la
# scambiava per il PDF: il 14/10/2026 il blocco rischio_incendi non si aggiornava
# più, senza errori. Si prova prima l'indirizzo nuovo, poi quello vecchio, e si
# accetta solo una risposta che comincia con %PDF.
PAGINA_ELENCO = "https://www.regione.lazio.it/protezione-civile/centro-funzionale-regionale/bollettini-rischi-incendi"
# Link ai bollettini nella pagina elenco: la data è nel nome, con eventuale
# suffisso «_0», «_1» che il portale aggiunge ai file ricaricati.
PDF_ELENCO_HREF = re.compile(
    r'href="((?:https://[a-z.]+)?/sites/default/files/rischio-incendi/\d{4}/[^"]*?'
    r'(\d{2})_(\d{2})_(\d{4})[^"/]*\.pdf)"',
    re.IGNORECASE,
)
FONTE = "Bollettino incendi boschivi Regione Lazio (AIB)"

PDF_BASE_URLS = [
    "https://www.regione.lazio.it/sites/default/files/rischio-incendi/{anno}/",
    "https://protezionecivile.regione.lazio.it/sites/default/files/binary/"
    "rl_protezione_civile/tbl_rischio_incendi/",
]

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


def segnala_fonte_ko(motivo):
    """Annota una fonte non letta: log del run + file letto dal workflow."""
    print(f"::warning::Fonte non letta — {FONTE}: {motivo}")
    percorso = os.environ.get("FONTI_KO_FILE")
    if percorso:
        with open(percorso, "a", encoding="utf-8") as f:
            f.write(f"{FONTE}\t{motivo}\n")
    scrivi_output(fonti_ko="true")


def scrivi_output(**kwargs):
    gh_out = os.environ.get("GITHUB_OUTPUT", "")
    if gh_out:
        with open(gh_out, "a") as f:
            for k, v in kwargs.items():
                f.write(f"{k}={v}\n")


def leggi_elenco():
    """Legge la pagina elenco dei bollettini.

    Ritorna (dict data → [url], errore). dict vuoto con errore None = pagina
    letta ma senza nessun bollettino riconoscibile (schema cambiato).
    """
    try:
        html = http_get_bytes(PAGINA_ELENCO).decode("utf-8", errors="replace")
    except Exception as e:
        return None, f"pagina elenco non raggiungibile ({e})"
    per_data = {}
    for href, gg, mm, aaaa in PDF_ELENCO_HREF.findall(html):
        try:
            d = datetime(int(aaaa), int(mm), int(gg)).date()
        except ValueError:
            continue
        url = href if href.lower().startswith("http") else "https://www.regione.lazio.it" + href
        per_data.setdefault(d, []).append(url.replace(" ", "%20"))
    return per_data, None


def scarica_url(url):
    """Scarica un PDF. Ritorna (bytes, None) oppure (None, motivo)."""
    try:
        pdf_bytes = http_get_bytes(url)
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except Exception as e:
        return None, str(e)
    if not pdf_bytes.startswith(b"%PDF"):
        return None, f"la risposta non è un PDF ({len(pdf_bytes)} bytes)"
    return pdf_bytes, None


def scarica_pdf_aib(now):
    """Cerca il bollettino di oggi, poi di ieri.

    Ritorna (bytes, data, esito) dove esito è:
    - "ok"            → bollettino trovato e scaricato;
    - "fuori-stagione"→ elenco letto, bollettini presenti ma nessuno di oggi/ieri;
    - "guasto: …"     → fonte non letta (elenco o PDF non leggibili).
    """
    candidates = [now.date(), (now - timedelta(days=1)).date()]
    elenco, errore_elenco = leggi_elenco()
    errori = []
    if elenco:
        for d in candidates:
            for url in elenco.get(d, []):
                pdf_bytes, motivo = scarica_url(url)
                if pdf_bytes:
                    print(f"📄 PDF AIB {d.isoformat()} scaricato ({len(pdf_bytes)} bytes) da {url}")
                    return pdf_bytes, d, "ok"
                errori.append(f"{url}: {motivo}")
        if errori:
            return None, None, "guasto: bollettino elencato ma non scaricabile — " + "; ".join(errori)
        ultimo = max(elenco)
        print(f"ℹ️  Elenco letto: ultimo bollettino del {ultimo.isoformat()}, nessuno di oggi o di ieri")
        return None, None, "fuori-stagione"

    # Elenco non letto (o senza bollettini): si prova coi nomi noti, così un
    # guasto della sola pagina non ferma l'aggiornamento.
    for d in candidates:
        date_str = d.strftime("%d_%m_%Y")
        for base in PDF_BASE_URLS:
            base = base.format(anno=d.year)
            for pat in PDF_NAME_PATTERNS:
                url = base + urllib.parse.quote(pat.format(date=date_str))
                pdf_bytes, motivo = scarica_url(url)
                if pdf_bytes:
                    print(f"📄 PDF AIB {date_str} scaricato ({len(pdf_bytes)} bytes) da {url}")
                    if errore_elenco is None:
                        # Pagina letta ma senza link riconoscibili: lo schema è
                        # cambiato anche se il PDF si trova ancora.
                        segnala_fonte_ko("la pagina elenco non contiene link riconoscibili ai bollettini")
                    else:
                        segnala_fonte_ko(errore_elenco)
                    return pdf_bytes, d, "ok"
                print(f"  ⏭️  {url}: {motivo}")
    # Un 404 sui nomi indovinati non dice «fuori stagione»: senza l'elenco
    # non si sa se il bollettino manca o ha solo cambiato nome.
    return None, None, "guasto: " + (errore_elenco or "la pagina elenco non contiene link riconoscibili ai bollettini") + \
        "; nessun PDF di oggi o di ieri ai nomi noti"


def blocco_scaduto(blocco, now):
    """True se il blocco salvato non copre più né oggi né un giorno futuro."""
    oggi = now.strftime("%Y-%m-%d")
    date = [blocco.get("data") or ""] + [((blocco.get("domani") or {}).get("data")) or ""]
    return all(d < oggi for d in date)


def conserva_per_guasto(motivo, now):
    """Fonte non letta: il blocco in vigore resta, salvo che sia già scaduto."""
    segnala_fonte_ko(motivo)
    allerta = load_allerta()
    blocco = allerta.get("rischio_incendi")
    changed = bool(blocco) and blocco_scaduto(blocco, now)
    if changed:
        print(f"⚠️  Blocco rischio_incendi scaduto (data {blocco.get('data')}): lo tolgo")
        del allerta["rischio_incendi"]
        save_allerta(allerta)
    elif blocco:
        print("⚠️  Lettura non riuscita: il blocco rischio_incendi resta com'era")
    scrivi_output(changed="true" if changed else "false")
    return 0


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

    pdf_bytes, pdf_date, esito = scarica_pdf_aib(now)
    if esito.startswith("guasto"):
        return conserva_per_guasto(esito.split(": ", 1)[1], now)
    if not pdf_bytes:
        # Fuori stagione: elenco letto, nessun bollettino di oggi né di ieri.
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
        return conserva_per_guasto(f"testo del PDF del {pdf_date} non estraibile (pdftotext)", now)

    liv_oggi_aib, liv_dom_aib, data_oggi, data_dom = estrai_zona_livello_oggi_e_domani(
        testo, ZONA_AIB_GENZANO
    )
    # Fallback data di validità: se la regex interna al PDF non aggancia l'header
    # "Previsioni per oggi DD-MM-YYYY", usa la data del PDF scaricato (è nel nome
    # del file ed è il giorno di validità del bollettino "oggi"). Evita data=null.
    if not data_oggi and pdf_date:
        data_oggi = pdf_date.strftime("%Y-%m-%d")
    if not data_dom and pdf_date:
        data_dom = (pdf_date + timedelta(days=1)).strftime("%Y-%m-%d")
    print(f"  OGGI ({data_oggi}): Zona {ZONA_AIB_GENZANO} = {liv_oggi_aib}")
    print(f"  DOMANI ({data_dom}): Zona {ZONA_AIB_GENZANO} = {liv_dom_aib}")

    # Scadenza per data: la sezione "oggi" del PDF può riferirsi a IERI quando il
    # bollettino di oggi non è ancora pubblicato (di norma la mattina). In quel
    # caso il PDF di ieri contiene già la previsione "domani" = oggi reale:
    # la promuoviamo a giorno corrente, così la barra non resta mai datata indietro.
    today_str = now.strftime("%Y-%m-%d")
    if data_oggi and data_oggi < today_str:
        if data_dom == today_str and liv_dom_aib:
            print(f"  ↪ Bollettino 'oggi' = {data_oggi} è passato: promuovo 'domani' ({data_dom}) a giorno corrente")
            liv_oggi_aib, data_oggi = liv_dom_aib, data_dom
            liv_dom_aib, data_dom = None, None
        else:
            # Bollettino troppo vecchio per coprire oggi → cessazione automatica.
            allerta = load_allerta()
            changed = "rischio_incendi" in allerta
            if changed:
                print(f"⚠️  Bollettino scaduto (oggi={today_str}, PDF copre {data_oggi}) → rimuovo blocco rischio_incendi")
                del allerta["rischio_incendi"]
                save_allerta(allerta)
            else:
                print(f"ℹ️  Bollettino scaduto (oggi={today_str}, PDF copre {data_oggi}) e nessun blocco da rimuovere")
            gh_out = os.environ.get("GITHUB_OUTPUT", "")
            if gh_out:
                with open(gh_out, "a") as f:
                    f.write(f"changed={'true' if changed else 'false'}\n")
            return 0

    livello_oggi = aib_to_pc(liv_oggi_aib)
    livello_dom = aib_to_pc(liv_dom_aib)

    if not livello_oggi:
        return conserva_per_guasto(
            f"Zona {ZONA_AIB_GENZANO} non trovata nel PDF del {pdf_date}: formato cambiato?", now)

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
        or current.get("data") != rischio_block["data"]
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
