#!/usr/bin/env python3
"""
fix-ordering-articoli-stesso-giorno.py

Modifica il campo `date:` degli articoli in content/comunicazioni/ che
condividono la stessa data con altri articoli, aggiungendo orari crescenti
basati sull'ordine reale di prima pubblicazione (git first commit timestamp).

Risolve il bug di ordering instabile dell'archivio /comunicazioni/: con due
articoli a `date: 2026-04-30` Hugo li ordina alfabeticamente per filename,
non per ordine di pubblicazione. Aggiungendo orario crescente nello stesso
giorno (00:01, 00:02, ... a seconda del numero), Hugo ordina Date desc
correttamente e l'ultimo scritto finisce in cima.

Articoli singoli giornalieri restano `date: AAAA-MM-GG` (no modifica).
"""
import re
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "comunicazioni"

# Match `date: AAAA-MM-GG` con o senza virgolette, senza orario
DATE_RE = re.compile(
    r'^(date:\s*)["\']?(\d{4}-\d{2}-\d{2})["\']?\s*$',
    re.MULTILINE,
)


def get_first_commit_unix(file_path: Path) -> int:
    """Unix timestamp del primo commit che ha aggiunto il file. 0 se untracked."""
    try:
        result = subprocess.run(
            [
                "git", "log", "--diff-filter=A", "--follow",
                "--format=%at", "--", str(file_path),
            ],
            capture_output=True, text=True, cwd=ROOT, check=True,
        )
        lines = [ln for ln in result.stdout.strip().split("\n") if ln]
        return int(lines[-1]) if lines else 0
    except (subprocess.CalledProcessError, ValueError):
        return 0


def slot_orari(n: int) -> list[str]:
    """
    N orari crescenti distribuiti tra 00:01 e 00:0N, formato HH:MM:SS.

    Strategia "orari minimi": tutti gli orari sono molto presto al mattino
    in modo che nessun articolo del giorno corrente risulti "futuro" per
    Hugo (cosa che lo escluderebbe dal build fino al rebuild successivo
    del workflow pubblica-programmata.yml, che gira alle 06:00 UTC).

    L'orario non è mostrato all'utente: il template `comunicazioni/list.html`
    formatta solo la data lunga ("30 aprile 2026") senza HH:MM. L'orario
    serve ESCLUSIVAMENTE come tie-break per l'ordering Hugo Date desc.
    """
    return [f"00:{i:02d}:00" for i in range(1, n + 1)]


def process():
    md_files = sorted(CONTENT.glob("*.md"))
    by_date: dict[str, list[Path]] = defaultdict(list)
    for md in md_files:
        text = md.read_text(encoding="utf-8")
        m = DATE_RE.search(text)
        if m:
            by_date[m.group(2)].append(md)

    # solo le date con 2+ articoli
    multi_day = {d: files for d, files in by_date.items() if len(files) >= 2}

    total_articles = sum(len(f) for f in multi_day.values())
    print(f"Giornate con 2+ articoli: {len(multi_day)}")
    print(f"Articoli da modificare:   {total_articles}")
    print()

    files_changed = 0
    for date_str, files in sorted(multi_day.items()):
        # ordina per first git commit timestamp asc; tie-break: filename asc
        files_with_ts = [(f, get_first_commit_unix(f)) for f in files]
        files_with_ts.sort(
            key=lambda x: (x[1] if x[1] > 0 else 9_999_999_999, x[0].name)
        )
        sorted_files = [f for f, _ in files_with_ts]

        n = len(sorted_files)
        orari = slot_orari(n)

        print(f"{date_str} ({n} articoli, ordinati per git first-commit asc):")
        for f, orario in zip(sorted_files, orari):
            text = f.read_text(encoding="utf-8")
            new_value = f"{date_str}T{orario}+02:00"
            new_text = DATE_RE.sub(rf'\g<1>{new_value}', text, count=1)
            if new_text != text:
                f.write_text(new_text, encoding="utf-8")
                files_changed += 1
                print(f"  → date: {new_value}   ({f.name})")

    print()
    print(f"File modificati totali: {files_changed}")


if __name__ == "__main__":
    process()
