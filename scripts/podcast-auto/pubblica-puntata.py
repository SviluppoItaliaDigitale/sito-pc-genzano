#!/usr/bin/env python3
"""pubblica-puntata.py — Mette in calendario una puntata che ha superato il controllo.

Ricodifica l'audio (64 kbps mono, senza metadati né firma dell'encoder),
scrive content/podcast/<data>-<id>.md con la data del primo martedì
o venerdì libero (il sito la pubblica da solo quel giorno, anche a PC
spento, col rebuild di ogni mattina), con la trascrizione verificata come
corpo, segna la voce «programmata» in coda.yaml e riattiva il podcast.
Uso: pubblica-puntata.py ID AUDIO TRASCRIZIONE_VERIFICATA.md [--descrizione "…"]
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

RADICE = Path(__file__).resolve().parents[2]
CODA = Path(__file__).with_name("coda.yaml")
PODCAST = RADICE / "content" / "podcast"
EPISODI = RADICE / "static" / "podcast" / "episodi"


def durata(file: Path) -> str:
    sec = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(file)], text=True).strip())
    return f"{int(sec // 60)} min {int(round(sec % 60)):02d} s"


def prossimo_episodio() -> int:
    numeri = []
    for f in PODCAST.glob("*.md"):
        testo = f.read_text(encoding="utf-8")
        if "render: never" in testo or f.name == "_index.md":
            continue
        m = re.search(r"^episodio:\s*(\d+)", testo, re.M)
        if m:
            numeri.append(int(m.group(1)))
    return max(numeri, default=0) + 1


GIORNI_USCITA = (1, 4)  # martedì e venerdì


def date_programmate() -> list[date]:
    """Date delle puntate attive (pubblicate o in calendario)."""
    out = []
    for f in PODCAST.glob("*.md"):
        testo = f.read_text(encoding="utf-8")
        if f.name == "_index.md" or "render: never" in testo:
            continue
        m = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", testo, re.M)
        if m:
            out.append(date.fromisoformat(m.group(1)))
    return out


def prossima_uscita() -> date:
    """Primo martedì o venerdì libero dopo oggi e dopo l'ultima in calendario."""
    giorno = max([date.today()] + date_programmate()) + timedelta(days=1)
    while giorno.weekday() not in GIORNI_USCITA:
        giorno += timedelta(days=1)
    return giorno


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("audio")
    ap.add_argument("trascrizione")
    ap.add_argument("--descrizione", required=True)
    ap.add_argument("--oggi", action="store_true", help="esce oggi invece che al primo martedì o venerdì libero")
    a = ap.parse_args()

    dati = yaml.safe_load(CODA.read_text(encoding="utf-8"))
    voce = next((v for v in dati["puntate"] if v["id"] == a.id), None)
    if not voce:
        print(f"ERRORE: {a.id} non è in coda.yaml", file=sys.stderr)
        return 1
    oggi = (date.today() if a.oggi else prossima_uscita()).isoformat()
    slug = f"{oggi}-{a.id}"
    if (PODCAST / f"{slug}.md").exists():
        print(f"ERRORE: esiste già content/podcast/{slug}.md", file=sys.stderr)
        return 1
    EPISODI.mkdir(parents=True, exist_ok=True)
    audio_out = EPISODI / f"{slug}-podcast.m4a"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", a.audio, "-vn", "-ac", "1",
         "-c:a", "aac", "-b:a", "64k", "-map_metadata", "-1", "-fflags", "+bitexact",
         "-flags:a", "+bitexact", "-movflags", "+faststart", str(audio_out)],
        check=True)

    corpo = Path(a.trascrizione).read_text(encoding="utf-8").strip()
    fonti = "\n".join(
        f"- [{Path(f).stem.replace('-', ' ').replace('_index', '').strip() or Path(f).parent.name.replace('-', ' ')}]"
        f"(/{Path(f).relative_to('content').parent.as_posix() if Path(f).name == '_index.md' else Path(f).relative_to('content').with_suffix('').as_posix()}/)"
        for f in voce["fonti"])
    episodio = prossimo_episodio()
    titolo = voce["titolo"].replace('"', "'")
    descr = a.descrizione.replace('"', "'")
    testo = f"""---
title: "{titolo}"
date: {oggi}
description: "{descr}"
episodio: {episodio}
audio: "/podcast/episodi/{audio_out.name}"
durata: "{durata(audio_out)}"
tts: false
draft: false
---

{corpo}

## Per approfondire sul nostro sito

{fonti}

In emergenza chiama il 112. Il Gruppo Comunale non si attiva su chiamata diretta dei cittadini.
"""
    (PODCAST / f"{slug}.md").write_text(testo, encoding="utf-8")

    voce["stato"] = "programmata"
    voce["file"] = f"content/podcast/{slug}.md"
    voce["data"] = oggi
    CODA.write_text(
        CODA.read_text(encoding="utf-8").split("puntate:")[0]
        + yaml.safe_dump({"puntate": dati["puntate"]}, allow_unicode=True, sort_keys=False),
        encoding="utf-8")

    indice = PODCAST / "_index.md"
    t = indice.read_text(encoding="utf-8")
    if re.search(r"^sospeso:\s*true", t, re.M):
        t = re.sub(r"^sospeso:\s*true", "sospeso: false", t, flags=re.M)
        t = re.sub(r'^description: ".*"$',
                   'description: "Il podcast del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma: '
                   'puntate brevi sull\'autoprotezione, con la trascrizione in pagina."', t, count=1, flags=re.M)
        indice.write_text(t, encoding="utf-8")
    print(f"PROGRAMMATA content/podcast/{slug}.md episodio {episodio} in uscita il {oggi}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
