#!/usr/bin/env python3
"""
Aggiorna data/allerta.json con il blocco "avviso_meteo" leggendo la pagina
"Allertamenti" della Regione Lazio, filtrando i PDF degli avvisi di
condizioni meteorologiche avverse (vento, neve, ondate di calore, ghiaccio,
gelate, mareggiate) — distinti dai normali allertamenti di criticità
idrogeologica e idraulica già coperti dal check-allerta sul CSV opendatasicilia.

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

Anti-spam: lo script aggiorna allerta.json solo se cambia il "tipo" o il
"livello" dell'avviso_meteo (non per refresh periodici). Il workflow
notifica-telegram.yml deve essere esteso separatamente per gestire questo
nuovo campo (TODO follow-up).
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

BASE_URL = "https://protezionecivile.regione.lazio.it"
INDEX_URL = f"{BASE_URL}/gestione-emergenze/centro-funzionale/bollettini/allertamenti"

ROME_TZ = ZoneInfo("Europe/Rome")
USER_AGENT = "PC-Genzano-Bot/1.0"
HTTP_TIMEOUT = 30

# Finestra retroattiva: scaricamo solo PDF emessi negli ultimi N giorni.
# Gli avvisi DPC sono validi 24-36 ore, 5 giorni di margine basta e avanza.
LOOKBACK_DAYS = 5

# Mapping: parola chiave nel campo "PER I SEGUENTI RISCHI:" → tipo umano.
# IDROGEOLOG e IDRAULICA sono ignorati: già coperti dal CSV opendatasicilia.
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
    coperta dal CSV opendatasicilia.
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


def estrai_validita_e_descrizione(testo, data_emissione):
    """Estrae validità + descrizione fenomeno dal PDF.

    Pattern frequenti:
    - 'dalle prime ore di domani, martedì 31.03.2026, e per le successive 24-36 ore'
    - 'a partire dalla mezzanotte di domani'
    - 'dalle prossime ore'

    Se non trova validità esplicita, assume:
    - inizio: data emissione (o domani 00:00 se 'dalle prime ore di domani')
    - fine: inizio + 36 ore
    """
    inizio = data_emissione
    fine = data_emissione + timedelta(hours=36)

    # Cerca "dalle prime ore di domani, ..., DD.MM.YYYY"
    m = re.search(r"dalle\s+prime\s+ore\s+di\s+domani.*?(\d{1,2})[./](\d{1,2})[./](\d{4})", testo, re.IGNORECASE)
    if m:
        try:
            inizio = datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)), 0, 0, tzinfo=ROME_TZ)
            fine = inizio + timedelta(hours=36)
        except ValueError:
            pass

    # Estrazione descrizione fenomeno: frase tipica "si prevedono sul Lazio:\n<descr>."
    descrizione = None
    m2 = re.search(r"si\s+prevedono\s+sul\s+Lazio\s*:?\s*\n?\s*([^\n]+?)\.", testo, re.IGNORECASE | re.DOTALL)
    if m2:
        descrizione = m2.group(1).strip().replace("\n", " ")
        descrizione = re.sub(r"\s+", " ", descrizione)
        if len(descrizione) > 250:
            descrizione = descrizione[:247] + "..."

    return inizio, fine, descrizione


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
    print(f"[{now.isoformat(timespec='seconds')}] check-avvisi-meteo: scarico {INDEX_URL}")

    try:
        html = http_get_text(INDEX_URL)
    except Exception as e:
        print(f"::warning::Impossibile scaricare la pagina allertamenti: {e}")
        return 0

    # Estrai tutti i link PDF della cartella tbl_avvisi_meteo_avverso
    pdf_paths = re.findall(
        r'href="(/sites/default/files/binary/rl_protezione_civile/tbl_avvisi_meteo_avverso/[^"]*\.pdf)"',
        html,
    )
    pdf_paths = list(dict.fromkeys(pdf_paths))  # dedup mantenendo ordine
    print(f"Trovati {len(pdf_paths)} PDF candidati nella pagina")

    # Filtra per data dal nome (lookback)
    candidates = []
    cutoff = now - timedelta(days=LOOKBACK_DAYS)
    for path in pdf_paths:
        filename = urllib.parse.unquote(path.rsplit("/", 1)[-1])
        data_pdf = estrai_data_da_nome(filename)
        if data_pdf is None:
            continue
        if data_pdf < cutoff:
            continue
        candidates.append((data_pdf, path, filename))

    candidates.sort(key=lambda x: x[0], reverse=True)  # più recente prima
    print(f"Candidati ultimi {LOOKBACK_DAYS} giorni: {len(candidates)}")

    avviso_attivo = None
    for data_pdf, path, filename in candidates:
        full_url = BASE_URL + urllib.parse.quote(path)
        # Quote rimette anche % di caratteri speciali, ma il path che abbiamo
        # è già URL-style. Decodifico prima e ri-quoto correttamente.
        full_url = BASE_URL + path  # spazi tipo "vento 30 03 2026" → urllib li gestisce con il quote sotto
        try:
            req = urllib.request.Request(full_url.replace(" ", "%20"), headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                pdf_bytes = r.read()
        except Exception as e:
            print(f"  ⏭️  {filename}: impossibile scaricare ({e})")
            continue

        testo = parse_pdf(pdf_bytes)
        if not testo:
            print(f"  ⏭️  {filename}: pdftotext output vuoto")
            continue

        rischio_raw = estrai_rischio(testo)
        tipo = classifica_rischio(rischio_raw)
        if not tipo:
            print(f"  ⏭️  {filename}: rischio='{rischio_raw}' (skip, idrogeologico già coperto)")
            continue

        livello = estrai_livello(testo)
        if livello == 0:
            print(f"  ⏭️  {filename}: tipo={tipo} ma nessun livello allerta esplicito")
            continue

        inizio, fine, descrizione = estrai_validita_e_descrizione(testo, data_pdf)
        if now > fine:
            print(f"  ⏭️  {filename}: tipo={tipo}, livello={LEVEL_NAMES[livello]}, ma scaduto ({fine.isoformat()})")
            continue

        # Trovato un avviso valido. Prendiamo il PIÙ RECENTE che soddisfa.
        avviso_attivo = {
            "tipo": tipo,
            "livello": LEVEL_NAMES[livello],
            "validita_inizio": inizio.isoformat(timespec="seconds"),
            "validita_fine": fine.isoformat(timespec="seconds"),
            "url": full_url.replace(" ", "%20"),
            "fonte_data": data_pdf.date().isoformat(),
        }
        if descrizione:
            avviso_attivo["descrizione"] = descrizione
        print(f"  ✅ {filename}: tipo={tipo}, livello={LEVEL_NAMES[livello]}, valido fino a {fine.isoformat(timespec='seconds')}")
        break

    # Aggiorna allerta.json se serve
    allerta = load_allerta()
    avviso_corrente = allerta.get("avviso_meteo")

    changed = False
    if avviso_attivo:
        if not avviso_corrente or avviso_corrente.get("tipo") != avviso_attivo["tipo"] or avviso_corrente.get("livello") != avviso_attivo["livello"]:
            print(f"⚠️  Aggiornamento avviso_meteo: {avviso_corrente.get('tipo') if avviso_corrente else 'nessuno'} → {avviso_attivo['tipo']} ({avviso_attivo['livello']})")
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
