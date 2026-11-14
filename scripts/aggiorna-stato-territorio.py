#!/usr/bin/env python3
"""Tiene aggiornata da sola la pagina /stato-del-territorio/, ogni giorno.

Due lavori, entrambi fail-safe (una fonte che non risponde non cambia nulla):
1. Riverifica le righe statiche di data/stato_territorio.yaml: per ogni riga legge le
   fonti elencate in `verifica:` (pagina web o file del repository) e controlla che
   contengano ancora il testo indicato. Se tutte lo contengono, `verificato` prende la
   data di oggi (ora italiana). Altrimenti la data resta com'era e la fonte finisce
   nel rapporto dei guasti.
2. Sismicità: chiede all'INGV (FDSN) i terremoti degli ultimi 7 giorni entro 30 km da
   Genzano e scrive data/sismicita_genzano.json, che lo shortcode matrice-territorio
   mostra nella riga «Sismico» (dinamico: "sismico").

Nato il 14/11/2026 su richiesta dell'utente («Fai in modo che sia sempre aggiornato»),
dopo che quattro righe erano rimaste con la verifica scaduta.

Uso:  python3 scripts/aggiorna-stato-territorio.py [--guasti FILE.md] [--prova]
  --prova   legge le fonti e stampa l'esito senza scrivere nulla.
Exit code: 0 sempre se il lavoro è arrivato in fondo (i guasti vanno in --guasti),
           2 se il file dei dati non si legge.
"""
import argparse
import datetime as dt
import gzip
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from html import unescape
from zoneinfo import ZoneInfo

import yaml

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATI = os.path.join(RADICE, "data", "stato_territorio.yaml")
SISMICITA = os.path.join(RADICE, "data", "sismicita_genzano.json")
ROMA = ZoneInfo("Europe/Rome")
UA = "Mozilla/5.0 (compatible; PCGenzanoVerifica/1.0; +https://www.protezionecivilegenzano.it/)"
GENZANO = (41.7064, 12.6894)  # municipio, WGS84
RAGGIO_KM, GIORNI = 30, 7


def leggi_url(url, tentativi=3):
    errore = None
    for n in range(tentativi):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
            with urllib.request.urlopen(req, timeout=40) as r:
                dati = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    dati = gzip.decompress(dati)
                return r.status, dati.decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code == 204:
                return 204, ""
            errore = f"HTTP {e.code}"
            if e.code in (404, 410):
                break
        except Exception as e:  # rete, timeout, TLS
            errore = type(e).__name__ + ": " + str(e)[:120]
        time.sleep(5 * (n + 1))
    raise RuntimeError(errore or "nessuna risposta")


def testo_visibile(html):
    html = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html)
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html)))


def verifica_riga(riga, cache):
    """Restituisce l'elenco dei problemi (vuoto = riga confermata)."""
    problemi = []
    for v in riga.get("verifica") or []:
        atteso = v["testo"]
        if "url" in v:
            url = v["url"]
            if url not in cache:
                try:
                    stato, corpo = leggi_url(url)
                    cache[url] = ("ok", testo_visibile(corpo))
                except RuntimeError as e:
                    cache[url] = ("errore", str(e))
            esito, contenuto = cache[url]
            if esito == "errore":
                problemi.append(f"{url} non risponde ({contenuto})")
            elif atteso not in contenuto:
                problemi.append(f"{url} non contiene più «{atteso}»")
        elif "file" in v:
            percorso = os.path.join(RADICE, v["file"])
            try:
                contenuto = open(percorso, encoding="utf-8").read()
            except OSError:
                problemi.append(f"{v['file']} non esiste")
                continue
            if atteso not in contenuto:
                problemi.append(f"{v['file']} non contiene più «{atteso}»")
    return problemi


def sismicita(oggi):
    inizio = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=GIORNI)).strftime("%Y-%m-%dT%H:%M:%S")
    url = ("https://webservices.ingv.it/fdsnws/event/1/query?"
           f"starttime={inizio}&lat={GENZANO[0]}&lon={GENZANO[1]}"
           f"&maxradiuskm={RAGGIO_KM}&format=text&orderby=time")
    stato, corpo = leggi_url(url)
    eventi = []
    for riga in corpo.splitlines():
        if not riga or riga.startswith("#"):
            continue
        c = riga.split("|")
        if len(c) < 13:
            raise RuntimeError("schema INGV cambiato: " + riga[:80])
        try:
            eventi.append({"tempo": c[1], "magnitudo": float(c[10]), "luogo": c[12]})
        except ValueError:
            continue
    piu_forte = max(eventi, key=lambda e: e["magnitudo"]) if eventi else None
    if piu_forte:
        t = dt.datetime.fromisoformat(piu_forte["tempo"].split(".")[0]).replace(tzinfo=dt.timezone.utc)
        piu_forte = {"magnitudo": piu_forte["magnitudo"], "luogo": piu_forte["luogo"],
                     "data": t.astimezone(ROMA).date().isoformat()}
    return {
        "aggiornato": oggi.isoformat(),
        "giorni": GIORNI,
        "raggio_km": RAGGIO_KM,
        "numero": len(eventi),
        "piu_forte": piu_forte,
        "fonte": "INGV, servizio FDSN webservices.ingv.it",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--guasti", help="file Markdown dove scrivere le fonti in errore")
    ap.add_argument("--prova", action="store_true")
    a = ap.parse_args()
    oggi = dt.datetime.now(ROMA).date()
    try:
        testo = open(DATI, encoding="utf-8").read()
        righe = yaml.safe_load(testo)["righe"]
    except Exception as e:
        print(f"ERRORE: {DATI} non si legge ({e})")
        return 2

    guasti, cache, confermate = [], {}, 0
    for r in righe:
        if not r.get("verifica"):
            continue
        problemi = verifica_riga(r, cache)
        if problemi:
            guasti += [f"- **{r['rischio']}** (`{r['id']}`): {p}" for p in problemi]
            print(f"DA RIVEDERE {r['id']}: " + "; ".join(problemi))
            continue
        confermate += 1
        print(f"confermata  {r['id']}")
        blocco = re.compile(r'(  - id: "%s"\n(?:    .*\n)*?    verificato: )"[\d-]+"' % re.escape(r["id"]))
        testo, n = blocco.subn(lambda m: m.group(1) + f'"{oggi.isoformat()}"', testo, count=1)
        if n != 1:
            guasti.append(f"- `{r['id']}`: campo `verificato` non trovato nel file")
    if confermate:
        testo = re.sub(r'^aggiornamento: "[\d-]+"', f'aggiornamento: "{oggi.isoformat()}"', testo, count=1, flags=re.M)

    try:
        sism = sismicita(oggi)
        print(f"sismicità   {sism['numero']} eventi in {GIORNI} giorni entro {RAGGIO_KM} km")
    except RuntimeError as e:
        sism = None
        guasti.append(f"- **Sismicità INGV**: il servizio FDSN non risponde ({e}); resta il dato precedente")
        print(f"ERRORE sismicità: {e}")

    if not a.prova:
        yaml.safe_load(testo)  # mai scrivere un YAML rotto
        open(DATI, "w", encoding="utf-8").write(testo)
        if sism:
            with open(SISMICITA, "w", encoding="utf-8") as f:
                json.dump(sism, f, ensure_ascii=False, indent=2)
                f.write("\n")
    if a.guasti:
        with open(a.guasti, "w", encoding="utf-8") as f:
            f.write("\n".join(guasti) + ("\n" if guasti else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
