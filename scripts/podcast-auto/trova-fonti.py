#!/usr/bin/env python3
"""trova-fonti.py — Elenca le pagine pubblicate del sito su un tema della coda.

Usa «fonti» (sempre incluse) e «parole» di coda.yaml: cerca negli articoli e
nelle pagine già online (data passata, niente versioni facili, traduzioni,
podcast o pagine legali) quelle che hanno le parole nel titolo (la descrizione
conta solo per l'ordine), e stampa gli indirizzi da dare a NotebookLM (al massimo --max); scrive
~/podcast-lavoro/<id>/fonti.txt e fonte.md (testo di tutte, per il controllo).
Uso: trova-fonti.py ID [--max 30]
"""
from __future__ import annotations

import argparse
from html import unescape
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

import yaml

RADICE = Path(__file__).resolve().parents[2]
SITO = "https://www.protezionecivilegenzano.it"
ESCLUSE = ("cruscotto", "monitor", "laboratorio-meteo", "stato-sistema", "podcast", "english", "francais", "deutsch", "espanol", "portugues",
           "romana", "esperanto", "privacy", "note-legali", "accessibilita",
           "social-media-policy", "mappa-sito", "cerca", "manuale")


def frontmatter(p: Path) -> dict:
    t = p.read_text(encoding="utf-8")
    m = re.match(r"\A---\n(.*?)\n---\n", t, re.S)
    try:
        return yaml.safe_load(m.group(1)) or {} if m else {}
    except yaml.YAMLError:
        return {}


def url(p: Path) -> str:
    if p.suffix == ".html":
        return f"{SITO}/{p.parent.relative_to(RADICE / 'static').as_posix()}/"
    rel = p.relative_to(RADICE / "content")
    parti = rel.parent.parts if rel.name == "_index.md" else rel.with_suffix("").parts
    return f"{SITO}/{'/'.join(parti)}/"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--max", type=int, default=35)
    a = ap.parse_args()
    coda = yaml.safe_load((Path(__file__).with_name("coda.yaml")).read_text(encoding="utf-8"))["puntate"]
    voce = next((v for v in coda if v["id"] == a.id), None)
    if not voce:
        print(f"ERRORE: {a.id} non è in coda", file=sys.stderr)
        return 1
    escludi = voce.get("escludi", [])
    parole = [re.compile(r"\b" + w, re.I) for w in voce.get("parole", [])]
    oggi = date.today()
    fisse = [RADICE / f for f in voce["fonti"]]
    trovate = []
    for p in sorted((RADICE / "content").rglob("*.md")):
        rel = p.relative_to(RADICE / "content").as_posix()
        if any(e in rel for e in escludi):
            continue
        if p in fisse or rel.split("/")[0] in ESCLUSE or p.stem.endswith("-facile"):
            continue
        fm = frontmatter(p)
        if fm.get("draft") or fm.get("archiviato") or (fm.get("build") or {}).get("render") == "never":
            continue
        d = fm.get("date")
        if d and (d.date() if hasattr(d, "date") else d) > oggi:
            continue
        titolo = str(fm.get("title", ""))
        descr = str(fm.get("description", ""))
        nel_titolo = sum(3 for r in parole if r.search(titolo))
        if not nel_titolo:
            continue  # la parola deve stare nel titolo: la sola descrizione porta pagine generiche
        punti = nel_titolo + sum(1 for r in parole if r.search(descr))
        if punti and rel.split("/")[0] != "comunicazioni":
            punti += 5  # pagine stabili prima degli articoli di cronaca
        if punti and re.search(r"cosa fare|come comportarsi|prevenzion|autoprotezion|consigli", titolo, re.I):
            punti += 2
        if punti:
            trovate.append((punti, str(d or ""), p))
    # Materiali per la popolazione e per le scuole pubblicati come pagine HTML
    # (schede stampabili, kit, storie, esperimenti, Abili a proteggere, moduli
    # per le scuole): stesso criterio, parola nel titolo della pagina.
    for p in sorted(RADICE.glob("static/*/**/index.html")):
        rel = p.relative_to(RADICE / "static").as_posix()
        if any(e in rel for e in escludi):
            continue
        if rel.split("/")[0] not in ("formazione", "abili-a-proteggere", "scuole") or "pacchett" in rel:
            continue
        html = p.read_text(encoding="utf-8", errors="ignore")
        if re.search(r'<meta[^>]+noindex', html, re.I):
            continue
        m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
        titolo = re.sub(r"\s+", " ", m.group(1)) if m else ""
        nel_titolo = sum(3 for r in parole if r.search(titolo))
        if nel_titolo:
            trovate.append((nel_titolo + 4, "", p))
    trovate.sort(key=lambda x: (-x[0], x[1]), reverse=False)
    scelte = fisse + [p for _, _, p in trovate[: max(0, a.max - len(fisse))]]
    ufficiali = voce.get("ufficiali", [])
    dest = Path.home() / "podcast-lavoro" / a.id
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "fonti.txt").write_text("\n".join([url(p) for p in scelte] + ufficiali) + "\n", encoding="utf-8")
    # Il testo per il controllo dei fatti è quello delle pagine PUBBLICATE, cioè
    # esattamente ciò che legge NotebookLM: i file .md perdono i riquadri inseriti
    # dai componenti del sito (per esempio i numeri utili). Errore del 15/11/2026:
    # l'803 555 della pagina sul rischio sismico risultava «assente dalle fonti».
    testo = []
    for u in [url(p) for p in scelte] + ufficiali:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        try:
            html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
        except OSError as e:
            print(f"ERRORE: fonte non raggiungibile {u}: {e}", file=sys.stderr)
            return 1
        html = re.sub(r"(?is)<script.*?</script>|<style.*?</style>", " ", html)
        corpo = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", html)).strip()
        testo.append(f"===== {u}\n" + unescape(corpo).replace("\xa0", " "))
    (dest / "fonte.md").write_text("\n\n".join(testo) + "\n", encoding="utf-8")
    for u in [url(p) for p in scelte] + ufficiali:
        print(u)
    print(f"# {len(scelte)} fonti ({len(trovate)} pagine pertinenti trovate)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
