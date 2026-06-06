#!/usr/bin/env python3
"""
scrape-catalogo-video.py — Scarica il catalogo completo (storico) di tutti
i video dai 4 canali YouTube monitorati e salva il risultato in
data/video_dpc_catalogo.yaml.

Usa yt-dlp per estrarre la lista video (extract_flat = no download, solo
metadata). I canali monitorati:
  - Io non rischio (DPC + ANPAS + INGV + RELUIS + CIMA)
  - DPCgov (Dipartimento Protezione Civile, PCM, canale ufficiale)
  - Abili a Proteggere (Cooperativa Sociale Europe Consulting)
  - Geopop (divulgazione scientifica di disastri naturali, geologia,
    vulcani, terremoti, eventi storici e antropici — fonte aggiunta a
    maggio 2026 su richiesta editoriale per arricchire la sezione
    "Approfondimenti video" sui contenuti del sito con ricostruzioni
    divulgative dei principali eventi PC trattati)

Il catalogo è poi usato da scripts/genera-video-correlati.py per il
cross-match con i contenuti del sito. La selezione resta editoriale:
i video Geopop fuori scope PC (archeologia, biologia, fisica generale)
emergeranno con score basso nel cross-match e non verranno proposti.

Uso: python3 scripts/scrape-catalogo-video.py [--limit N]
"""

import os
import sys
import yaml
import argparse
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("ERRORE: yt-dlp non installato. Installa con:", file=sys.stderr)
    print("  pip install --break-system-packages yt-dlp", file=sys.stderr)
    sys.exit(1)

CANALI = {
    # Tematici PC (no filtro lessicale: ogni loro video è pertinente)
    "io-non-rischio": {
        "nome": "Io non rischio",
        "url": "https://www.youtube.com/@io_non_rischio/videos",
        "tematico_pc": True,
    },
    "dpc-gov": {
        "nome": "Dipartimento della Protezione Civile (PCM)",
        "url": "https://www.youtube.com/@DPCgov/videos",
        "tematico_pc": True,
    },
    "abili-a-proteggere": {
        "nome": "Abili a Proteggere",
        "url": "https://www.youtube.com/@abiliaproteggere4520/videos",
        "tematico_pc": True,
    },
    "ingv-terremoti": {
        "nome": "INGV — Istituto Nazionale di Geofisica e Vulcanologia",
        "url": "https://www.youtube.com/@INGVterremoti/videos",
        "tematico_pc": True,
    },
    "ingv-vulcani": {
        "nome": "INGVvulcani — Osservatorio Vesuviano e Vulcani INGV",
        "url": "https://www.youtube.com/@INGVvulcani/videos",
        "tematico_pc": True,
    },
    "italiameteo": {
        "nome": "ItaliaMeteo — Agenzia Nazionale per la Meteorologia e Climatologia",
        "url": "https://www.youtube.com/@AgenziaItaliaMeteo/videos",
        "tematico_pc": True,
    },
    "cima-foundation": {
        "nome": "CIMA Research Foundation",
        "url": "https://www.youtube.com/@CIMAfondazione/videos",
        "tematico_pc": True,
    },
    "cnsas": {
        "nome": "CNSAS — Corpo Nazionale Soccorso Alpino e Speleologico",
        "url": "https://www.youtube.com/@CnsasCanaleUfficiale/videos",
        "tematico_pc": True,
    },
    "solarino-sismologo": {
        "nome": "Stefano Solarino — sismologo INGV (divulgazione sismica)",
        "url": "https://www.youtube.com/@solarinosismologo/videos",
        "tematico_pc": True,
    },
    # Canali istituzionali/di volontariato NON inseriti perché privi di
    # un canale YouTube ricco con handle verificato: ISPRA (handle 404),
    # Vigili del Fuoco (no videos tab), Croce Rossa Italiana (pochi
    # video), CNR (pochi video), ANPAS e Misericordie (handle non
    # verificato al 2026-06-06). Sono comunque linkati come fonti in
    # content/siti-utili/_index.md. Reinserire qui se si verifica un
    # handle con catalogo video pertinente.
    # Divulgativi qualificati (con filtro lessicale PC, come Geopop)
    "geopop": {
        "nome": "Geopop — divulgazione scientifica",
        "url": "https://www.youtube.com/@geopop/videos",
        "tematico_pc": False,
    },
    "natgeo-italia": {
        "nome": "National Geographic Italia",
        "url": "https://www.youtube.com/@natgeoit/videos",
        "tematico_pc": False,
    },
    "rai-cultura": {
        "nome": "Rai Cultura (documentari)",
        "url": "https://www.youtube.com/@raicultura/videos",
        "tematico_pc": False,
    },
    "cicap": {
        "nome": "CICAP — Comitato Italiano per il Controllo delle Affermazioni sulle Pseudoscienze",
        "url": "https://www.youtube.com/@CICAP_it/videos",
        "tematico_pc": False,
    },
    "link4universe": {
        "nome": "Link4Universe — Adrian Fartade",
        "url": "https://www.youtube.com/@link4universe/videos",
        "tematico_pc": False,
    },
    "wired-italia": {
        "nome": "Wired Italia",
        "url": "https://www.youtube.com/@WiredItalia/videos",
        "tematico_pc": False,
    },
    "rai-news": {
        "nome": "Rai News",
        "url": "https://www.youtube.com/@RaiNews/videos",
        "tematico_pc": False,
    },
    "cmcc": {
        "nome": "CMCC — Centro Euro-Mediterraneo sui Cambiamenti Climatici",
        "url": "https://www.youtube.com/@CMCCvideo/videos",
        "tematico_pc": False,
    },
    "dario-bressanini": {
        "nome": "Dario Bressanini — chimica e scienza dell'alimentazione",
        "url": "https://www.youtube.com/@dariobressanini/videos",
        "tematico_pc": False,
    },
    # SkyTG24 e TGCom24 erano stati aggiunti (2026-05-19), poi rimossi
    # lo stesso giorno: rumore eccessivo. Producevano 63% di tutti i link
    # del sistema con match generici tipo "Seveso esonda Milano" su
    # articolo del disastro chimico di Seveso, "Tragedia funivia" su
    # articolo Vajont, "Turchia incendio vigili del fuoco" su articolo
    # terremoto Amatrice. Sono canali news con migliaia di clip brevi
    # che condividono parole comuni ad alto score. Rai News (1489 video,
    # 2% dei link, qualità decente) resta — è più editoriale e meno
    # "cronaca-flash". Per re-includere SkyTG24/TGCom24 servirebbero
    # filtri lessicali molto più stringenti.
}


def scrape_channel(url: str, limit: int = 0) -> list[dict]:
    """Restituisce lista [{id, title, url}] con tutti i video del canale."""
    ydl_opts = {
        "extract_flat": True,
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
    }
    if limit:
        ydl_opts["playlistend"] = limit
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    out = []
    for e in info.get("entries", []):
        if not e or not e.get("id"):
            continue
        out.append({
            "id": e["id"],
            "title": (e.get("title") or "").strip(),
            "url": f"https://youtu.be/{e['id']}",
        })
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=0,
                   help="Max video per canale (default: tutti)")
    p.add_argument("--output", default="data/video_dpc_catalogo.yaml")
    args = p.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    out_path = repo_root / args.output

    catalogo = {"canali": {}, "video": {}}
    total = 0
    for ck, meta in CANALI.items():
        print(f"Scarico {meta['nome']}…", file=sys.stderr)
        try:
            videos = scrape_channel(meta["url"], limit=args.limit)
        except Exception as e:
            print(f"  ERRORE {ck}: {e}", file=sys.stderr)
            videos = []
        print(f"  {len(videos)} video", file=sys.stderr)
        catalogo["canali"][ck] = {
            "nome": meta["nome"],
            "url": meta["url"],
            "video_count": len(videos),
            "tematico_pc": meta.get("tematico_pc", False),
        }
        for v in videos:
            key = f"{ck}-{v['id']}"
            catalogo["video"][key] = {
                "id": v["id"],
                "titolo": v["title"],
                "url": v["url"],
                "canale": ck,
            }
        total += len(videos)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# Catalogo completo dei video divulgativi sui 4 canali YouTube\n")
        f.write(f"# monitorati. Generato da scripts/scrape-catalogo-video.py.\n")
        f.write(f"# Aggiornato periodicamente; usato da scripts/genera-video-correlati.py\n")
        f.write(f"# per il cross-match con i contenuti del sito.\n")
        f.write(f"#\n")
        f.write(f"# Totale: {total} video ({len(CANALI)} canali).\n\n")
        yaml.safe_dump(catalogo, f, allow_unicode=True, sort_keys=True, width=120)
    print(f"\n✓ Scritto {out_path} con {total} video totali", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
