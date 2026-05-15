#!/usr/bin/env python3
"""
scrape-catalogo-video.py — Scarica il catalogo completo (storico) di tutti
i video dai 3 canali YouTube monitorati e salva il risultato in
data/video_dpc_catalogo.yaml.

Usa yt-dlp per estrarre la lista video (extract_flat = no download, solo
metadata). I canali monitorati:
  - Io non rischio (DPC + ANPAS + INGV + RELUIS + CIMA)
  - DPCgov (Dipartimento Protezione Civile, PCM, canale ufficiale)
  - Abili a Proteggere (Cooperativa Sociale Europe Consulting)

Il catalogo è poi usato da scripts/genera-video-correlati.py per il
cross-match con i contenuti del sito.

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
    "io-non-rischio": {
        "nome": "Io non rischio",
        "url": "https://www.youtube.com/@io_non_rischio/videos",
    },
    "dpc-gov": {
        "nome": "Dipartimento della Protezione Civile (PCM)",
        "url": "https://www.youtube.com/@DPCgov/videos",
    },
    "abili-a-proteggere": {
        "nome": "Abili a Proteggere",
        "url": "https://www.youtube.com/@abiliaproteggere4520/videos",
    },
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
        f.write(f"# Catalogo completo dei video LIS + eventi sui 3 canali YouTube\n")
        f.write(f"# monitorati. Generato da scripts/scrape-catalogo-video.py.\n")
        f.write(f"# Aggiornato periodicamente; usato da scripts/genera-video-correlati.py\n")
        f.write(f"# per il cross-match con i contenuti del sito.\n")
        f.write(f"#\n")
        f.write(f"# Totale: {total} video (3 canali).\n\n")
        yaml.safe_dump(catalogo, f, allow_unicode=True, sort_keys=True, width=120)
    print(f"\n✓ Scritto {out_path} con {total} video totali", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
