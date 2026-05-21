#!/usr/bin/env python3
"""Notifica IndexNow (Bing, Yandex, ecc.) delle URL modificate.

IndexNow permette ai motori di ricerca di sapere in pochi minuti che una pagina
è nuova o aggiornata, invece di aspettare il prossimo crawl. Utile soprattutto
per le notizie in /comunicazioni/.

Uso:
    python3 scripts/indexnow-ping.py                # URL dedotte dall'ultimo commit
    python3 scripts/indexnow-ping.py https://...    # URL esplicite

La chiave IndexNow è pubblica per definizione: è servita dal sito stesso a
https://www.protezionecivilegenzano.it/<KEY>.txt (file static/<KEY>.txt).
"""
import json
import re
import subprocess
import sys
import urllib.request

HOST = "www.protezionecivilegenzano.it"
KEY = "e464a79232683b147857dc3d5f9b98f9"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"


def urls_from_last_commit() -> list:
    try:
        out = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            capture_output=True, text=True, timeout=15,
        ).stdout
    except Exception:
        return []
    urls = set()
    for line in out.splitlines():
        line = line.strip()
        # solo articoli /comunicazioni/, esclusi i -facile (build.list:never)
        m = re.match(r"^content/comunicazioni/(.+)\.md$", line)
        if m and not m.group(1).endswith("-facile"):
            urls.add(f"https://{HOST}/comunicazioni/{m.group(1)}/")
    if urls:
        # quando esce un articolo cambiano anche home e archivio
        urls.add(f"https://{HOST}/")
        urls.add(f"https://{HOST}/comunicazioni/")
    return sorted(urls)


def main() -> None:
    urls = sys.argv[1:] or urls_from_last_commit()
    if not urls:
        print("IndexNow: nessuna URL da inviare.")
        return
    payload = {"host": HOST, "key": KEY, "keyLocation": KEY_LOCATION, "urlList": urls}
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow: HTTP {r.status} — inviate {len(urls)} URL")
    except Exception as e:
        # Un ping di indicizzazione non deve mai far fallire la pipeline.
        print(f"IndexNow: errore non bloccante: {e}", file=sys.stderr)
        return
    for u in urls:
        print("  ", u)


if __name__ == "__main__":
    main()
