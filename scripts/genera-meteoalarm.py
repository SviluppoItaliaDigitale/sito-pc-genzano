#!/usr/bin/env python3
"""Snapshot degli avvisi MeteoAlarm per l'Italia (quadro nazionale).

MeteoAlarm è il portale di EUMETNET che raccoglie gli avvisi emessi dai servizi
meteorologici nazionali europei. Il feed italiano riporta gli avvisi per regione
in formato CAP dentro un Atom.

Perché uno snapshot: il feed risponde 200 ma non espone le intestazioni CORS
(verificato 22/09/2026), quindi non è leggibile dal browser.

🔴 RAPPORTO CON IL BOLLETTINO DPC — questo NON è il bollettino di criticità della
Protezione Civile e non lo sostituisce mai. Per Genzano di Roma la fonte che fa
fede resta il bollettino DPC per la Zona F, che la Sala situazioni già mostra in
cima. MeteoAlarm serve a una cosa sola: vedere il quadro delle altre regioni, utile
quando si valuta una partenza in colonna mobile o si legge una notizia nazionale.
La scheda lo dice esplicitamente.

Fail-safe: qualunque errore lascia lo snapshot invariato ed esce 0.
"""
from __future__ import annotations

import json
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

FEED = "https://feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-italy"
UA = "PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/)"
USCITA = pathlib.Path(__file__).resolve().parent.parent / "static" / "open-data" / "meteoalarm-italia.json"
NS = {"a": "http://www.w3.org/2005/Atom", "cap": "urn:oasis:names:tc:emergency:cap:1.2"}

# Tipi di fenomeno usati da MeteoAlarm (vocabolario EUMETNET) resi in italiano.
# Un tipo non previsto resta nella forma originale: meglio l'inglese che una
# traduzione inventata.
FENOMENI = {
    "thunderstorm": "Temporali",
    "rain": "Pioggia",
    "rain-flood": "Pioggia e piene",
    "rainflood": "Pioggia e piene",
    "flood": "Alluvione",
    "wind": "Vento",
    "snow-ice": "Neve e ghiaccio",
    "snow/ice": "Neve e ghiaccio",
    "snow": "Neve",
    "forest fire": "Incendi boschivi",
    "forestfire": "Incendi boschivi",
    "coastal event": "Mareggiate",
    "coastalevent": "Mareggiate",
    "high temperature": "Caldo",
    "extreme high temperature": "Caldo estremo",
    "low temperature": "Freddo",
    "extreme low temperature": "Freddo estremo",
    "avalanches": "Valanghe",
    "avalanche": "Valanghe",
    "fog": "Nebbia",
}
LIVELLI = {"yellow": "gialla", "orange": "arancione", "red": "rossa", "green": "verde"}


def ora() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def txt(el, tag: str) -> str:
    for pre in ("cap:", "a:", ""):
        n = el.find(pre + tag, NS) if pre else el.find(tag)
        if n is not None and n.text:
            return n.text.strip()
    return ""


def scarica(tentativi: int = 3) -> bytes:
    ultimo = None
    for n in range(tentativi):
        try:
            req = urllib.request.Request(FEED, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read()
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            ultimo = e
            if n < tentativi - 1:
                time.sleep(4 * (n + 1))
    raise RuntimeError(f"feed non raggiungibile: {ultimo}")


def traduci(evento: str) -> tuple[str, str]:
    """Dal titolo CAP ricava (livello in italiano, fenomeno in italiano)."""
    b = evento.lower()
    livello = next((LIVELLI[k] for k in LIVELLI if b.startswith(k)), "")
    # toglie il colore iniziale e la parola "warning" finale
    resto = re.sub(r"^\s*(yellow|orange|red|green)\s+", "", b)
    resto = re.sub(r"\s*warning\s*$", "", resto).strip()
    return livello, FENOMENI.get(resto, evento.strip())


def main() -> int:
    try:
        grezzo = scarica()
        radice = ET.fromstring(grezzo)
    except (RuntimeError, ET.ParseError) as e:
        print(f"[fail-safe] {e}: snapshot lasciato invariato.", file=sys.stderr)
        return 0

    avvisi = []
    adesso = datetime.now(timezone.utc)
    scaduti = 0
    for e in radice.findall("a:entry", NS):
        evento = txt(e, "event")
        if not evento:
            continue
        livello, fenomeno = traduci(evento)
        if livello == "verde":
            continue  # "nessun avviso" non è un avviso da mostrare
        # 🔴 Un avviso scaduto non è un avviso: il feed continua a esporlo per un
        #    po' dopo la fine della validità, e mostrarlo lo farebbe leggere come
        #    corrente. Stessa regola della barra allerta in homepage.
        fine = txt(e, "expires")
        if fine:
            try:
                if datetime.fromisoformat(fine.replace("Z", "+00:00")) < adesso:
                    scaduti += 1
                    continue
            except ValueError:
                pass  # data illeggibile: si tiene, meglio un avviso in più che uno perso
        avvisi.append({
            "regione": txt(e, "areaDesc") or "—",
            "fenomeno": fenomeno,
            "livello": livello or "non dichiarato",
            "evento_originale": evento,
            "severita": txt(e, "severity"),
            "certezza": txt(e, "certainty"),
            "inizio": txt(e, "onset") or txt(e, "effective"),
            "fine": fine,
            "emesso": txt(e, "sent"),
            "identificativo": txt(e, "identifier"),
        })

    ordine = {"rossa": 0, "arancione": 1, "gialla": 2}
    avvisi.sort(key=lambda a: (ordine.get(a["livello"], 9), a["regione"]))

    dati = {
        "_snapshot": {
            "generato": ora(),
            "fonte": "MeteoAlarm — EUMETNET, feed ufficiale per l'Italia",
            "fonte_url": "https://meteoalarm.org/",
            "avvisi": len(avvisi),
            "scaduti_scartati": scaduti,
            "avvertenza": (
                "Quadro nazionale, non sostituisce il bollettino di criticità del "
                "Dipartimento della Protezione Civile: per Genzano di Roma fa fede "
                "la Zona F del bollettino DPC."
            ),
        },
        "avvisi": avvisi,
    }

    USCITA.parent.mkdir(parents=True, exist_ok=True)
    if USCITA.exists():
        try:
            if json.loads(USCITA.read_text(encoding="utf-8")).get("avvisi") == avvisi:
                print(f"Nessuna variazione ({len(avvisi)} avvisi): file invariato.")
                return 0
        except ValueError:
            pass
    USCITA.write_text(json.dumps(dati, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Scritto {USCITA.name}: {len(avvisi)} avvisi regionali in corso "
          f"({scaduti} scaduti scartati).")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"[fail-safe] errore non previsto, snapshot invariato: {e}", file=sys.stderr)
        sys.exit(0)
