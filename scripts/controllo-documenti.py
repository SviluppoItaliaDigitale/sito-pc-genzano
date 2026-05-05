#!/usr/bin/env python3
"""
Controllo settimanale dei documenti scaricabili del sito.

Verifica:

1. INVENTARIO + INTEGRITÀ — tutti i PDF/ZIP/HTML stampabili sono presenti
   nel filesystem, non vuoti, non corrotti (PDF: header %PDF; ZIP:
   apribile da zipfile; HTML: contiene <html).

2. DRIFT ZIP PACCHETTI — ri-esegue la logica di genera-pacchetti-kit.py
   in una temp dir e confronta con i pacchetti committati. Se diversi
   significa che il workflow di generazione è saltato o c'è anomalia.

3. LINK ROTTI VERSO DOCUMENTI — cerca tutti i riferimenti
   /manuali/...pdf, /allegati/...pdf, /comunicati/...pdf,
   /pacchetti/...zip, /formazione/schede-stampabili/<slug>/ nel
   contenuto del sito (content/, themes/, static/) e verifica che
   ogni link punti a un file esistente.

4. DOCUMENTI ORFANI — documenti presenti nel filesystem ma non
   linkati da nessuna pagina del sito (potrebbero essere obsoleti).

Output:
- File `controllo-documenti-report.md` nella root con tutto il report.
- Exit code 0 se tutto OK, 1 se ci sono problemi bloccanti
  (corrotti / drift / link rotti). Documenti orfani sono solo warning.
"""

import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT_PATH = ROOT / "controllo-documenti-report.md"

# Cartelle dei documenti scaricabili
DIRS_PDF = [
    ROOT / "static" / "manuali",
    ROOT / "static" / "allegati",
    ROOT / "static" / "comunicati",
]
DIR_PACCHETTI = ROOT / "static" / "formazione" / "pacchetti"
DIR_SCHEDE = ROOT / "static" / "formazione" / "schede-stampabili"

# Cartelle dove cercare i link
DIRS_CONTENUTO = [
    ROOT / "content",
    ROOT / "themes",
    ROOT / "static",
    ROOT / "data",
    ROOT / "layouts",
]


def trova_pdf() -> list[Path]:
    pdf = []
    for d in DIRS_PDF:
        if d.is_dir():
            pdf.extend(sorted(d.rglob("*.pdf")))
    return pdf


def trova_zip_pacchetti() -> list[Path]:
    if not DIR_PACCHETTI.is_dir():
        return []
    return sorted(DIR_PACCHETTI.glob("*.zip"))


def trova_schede() -> list[Path]:
    if not DIR_SCHEDE.is_dir():
        return []
    schede = []
    for d in sorted(DIR_SCHEDE.iterdir()):
        if d.is_dir() and d.name != "assets":
            idx = d / "index.html"
            if idx.exists():
                schede.append(idx)
    return schede


def verifica_pdf(p: Path) -> str | None:
    """Ritorna messaggio di errore se PDF corrotto, None se OK."""
    if p.stat().st_size == 0:
        return "file vuoto (0 byte)"
    try:
        with open(p, "rb") as f:
            head = f.read(5)
        if not head.startswith(b"%PDF"):
            return f"header non %PDF (trovato: {head!r})"
    except OSError as e:
        return f"errore lettura: {e}"
    return None


def verifica_zip(p: Path) -> str | None:
    if p.stat().st_size == 0:
        return "file vuoto (0 byte)"
    try:
        with zipfile.ZipFile(p) as zf:
            bad = zf.testzip()
            if bad is not None:
                return f"file zip corrotto (membro problematico: {bad})"
            if len(zf.namelist()) == 0:
                return "zip vuoto (nessun file dentro)"
    except zipfile.BadZipFile as e:
        return f"non è uno zip valido: {e}"
    except OSError as e:
        return f"errore lettura: {e}"
    return None


def verifica_html(p: Path) -> str | None:
    if p.stat().st_size == 0:
        return "file vuoto (0 byte)"
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return f"errore lettura: {e}"
    if "<html" not in text.lower():
        return "manca tag <html> (file probabilmente non HTML)"
    if len(text) < 200:
        return f"contenuto troppo breve ({len(text)} byte): probabilmente segnaposto"
    return None


def hash_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def estrai_zip_in(p: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(p) as zf:
        zf.extractall(target)


def verifica_drift_pacchetti() -> list[str]:
    """Ri-genera i pacchetti, estrae entrambe le versioni in tmp dir e
    confronta i contenuti file-per-file. Più affidabile del confronto
    di hash dello ZIP che dipende da timestamp/compressione."""
    drift_msgs: list[str] = []
    script = ROOT / "scripts" / "genera-pacchetti-kit.py"
    if not script.exists():
        return ["script genera-pacchetti-kit.py non trovato — impossibile verificare drift"]

    zip_attuali = trova_zip_pacchetti()
    if not zip_attuali:
        return []

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # Estrai gli ZIP committati in 'before/<nome>/'
        before = tmp / "before"
        for z in zip_attuali:
            estrai_zip_in(z, before / z.stem)

        # Backup degli ZIP per ripristino post-test
        backup = tmp / "backup"
        backup.mkdir()
        for z in zip_attuali:
            shutil.copy(z, backup / z.name)

        # Rigenera i pacchetti (sovrascrive in DIR_PACCHETTI)
        try:
            subprocess.run(
                [sys.executable, str(script)],
                check=True,
                capture_output=True,
                cwd=ROOT,
            )
        except subprocess.CalledProcessError as e:
            for f in backup.iterdir():
                shutil.copy(f, DIR_PACCHETTI / f.name)
            return [f"esecuzione genera-pacchetti-kit.py fallita: {e.stderr.decode()[:200]}"]

        zip_rigenerati = trova_zip_pacchetti()

        # Estrai gli ZIP rigenerati in 'after/<nome>/'
        after = tmp / "after"
        for z in zip_rigenerati:
            estrai_zip_in(z, after / z.stem)

        # Ripristina i backup PRIMA di analizzare (così il filesystem
        # resta intatto anche se l'analisi fallisce)
        for f in backup.iterdir():
            shutil.copy(f, DIR_PACCHETTI / f.name)

        # Confronto: nomi mancanti / nuovi
        attesi = {p.name for p in before.iterdir() if p.is_dir()}
        trovati = {p.name for p in after.iterdir() if p.is_dir()}
        for nome in attesi - trovati:
            drift_msgs.append(f"`{nome}.zip` esiste in repo ma NON viene più generato (kit rinominato/cancellato?)")
        for nome in trovati - attesi:
            drift_msgs.append(f"`{nome}.zip` ora viene generato ma NON era in repo (kit nuovo?)")

        # Per i pacchetti comuni: confronta file-per-file
        for nome in sorted(attesi & trovati):
            d_before = before / nome
            d_after = after / nome
            files_before = {p.relative_to(d_before): p for p in d_before.rglob("*") if p.is_file()}
            files_after = {p.relative_to(d_after): p for p in d_after.rglob("*") if p.is_file()}

            extra = sorted(set(files_after) - set(files_before))
            mancanti = sorted(set(files_before) - set(files_after))
            cambiati = []
            for rel in sorted(set(files_before) & set(files_after)):
                if files_before[rel].read_bytes() != files_after[rel].read_bytes():
                    cambiati.append(rel)

            if extra or mancanti or cambiati:
                parti = []
                if mancanti:
                    parti.append(f"{len(mancanti)} file rimossi")
                if extra:
                    parti.append(f"{len(extra)} file aggiunti")
                if cambiati:
                    parti.append(f"{len(cambiati)} file modificati")
                drift_msgs.append(f"`{nome}.zip` — drift: {', '.join(parti)}")

    return drift_msgs


def trova_link_documenti(text: str) -> set[str]:
    """Estrae i path di link verso documenti interni del sito.

    Esclude i match che fanno parte di un URL esterno (riconosciuto dal
    fatto che il carattere immediatamente precedente è alfanumerico o
    `.`/`-`, segno che siamo dentro un dominio tipo `sito.it/path`).
    """
    patterns = [
        r"/manuali/[A-Za-z0-9_./-]+?\.pdf",
        r"/allegati/[A-Za-z0-9_./-]+?\.pdf",
        r"/comunicati/[A-Za-z0-9_./-]+?\.pdf",
        r"/formazione/pacchetti/[A-Za-z0-9_./-]+?\.zip",
        r"/formazione/schede-stampabili/[a-z][a-z0-9-]*/?",
    ]
    found = set()
    for pat in patterns:
        for m in re.finditer(pat, text):
            prev_char = text[m.start() - 1] if m.start() > 0 else ""
            # URL esterno (es. https://dominio.it/manuali/...): il carattere
            # immediatamente prima è parte del dominio (lettera, cifra, . o -)
            if prev_char.isalnum() or prev_char in ".-":
                continue
            link = m.group(0).rstrip("/")
            # Esclusione: la cartella assets/ delle schede non è una scheda
            if link.endswith("/schede-stampabili/assets"):
                continue
            found.add(link)
    return found


def scansiona_link_in_repo() -> set[str]:
    """Ritorna insieme dei link verso documenti trovati in tutti i contenuti."""
    estensioni = {".md", ".html", ".yaml", ".yml", ".json", ".js", ".toml"}
    tutti = set()
    for d in DIRS_CONTENUTO:
        if not d.is_dir():
            continue
        for f in d.rglob("*"):
            if not f.is_file():
                continue
            if f.suffix.lower() not in estensioni:
                continue
            # salta cartella public/, node_modules, ecc.
            try:
                rel = f.relative_to(ROOT)
            except ValueError:
                continue
            if "public/" in str(rel) or "node_modules/" in str(rel):
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            tutti |= trova_link_documenti(text)
    return tutti


def url_pubblico_di(p: Path) -> str | None:
    """Mappa un file su filesystem al suo URL pubblico (sito)."""
    try:
        rel = p.relative_to(ROOT / "static")
    except ValueError:
        return None
    s = str(rel).replace("\\", "/")
    # /formazione/schede-stampabili/<slug>/index.html → /formazione/schede-stampabili/<slug>
    if s.startswith("formazione/schede-stampabili/") and s.endswith("/index.html"):
        return "/" + s[: -len("/index.html")]
    return "/" + s


def main() -> int:
    print("Controllo settimanale documenti scaricabili")
    print("=" * 60)

    pdf = trova_pdf()
    zip_pacchetti = trova_zip_pacchetti()
    schede = trova_schede()

    inventario = {
        "PDF": pdf,
        "ZIP pacchetti": zip_pacchetti,
        "Schede HTML": schede,
    }

    problemi_corrotti: list[tuple[str, Path, str]] = []
    drift: list[str] = []
    link_rotti: list[str] = []
    orfani: list[Path] = []

    # 1. Integrità
    for nome, lista in inventario.items():
        for p in lista:
            if not p.exists():
                problemi_corrotti.append((nome, p, "file non esiste"))
                continue
            if nome == "PDF":
                err = verifica_pdf(p)
            elif nome == "ZIP pacchetti":
                err = verifica_zip(p)
            else:
                err = verifica_html(p)
            if err:
                problemi_corrotti.append((nome, p, err))

    # 2. Drift dei pacchetti
    drift = verifica_drift_pacchetti()

    # 3. Link rotti
    link_in_contenuti = scansiona_link_in_repo()
    file_esistenti_url = set()
    for lista in inventario.values():
        for p in lista:
            url = url_pubblico_di(p)
            if url:
                file_esistenti_url.add(url)

    for link in sorted(link_in_contenuti):
        if link not in file_esistenti_url:
            link_rotti.append(link)

    # 4. Orfani
    for nome, lista in inventario.items():
        for p in lista:
            url = url_pubblico_di(p)
            if url and url not in link_in_contenuti:
                orfani.append(p)

    # Genera report
    righe = ["# Controllo settimanale documenti scaricabili", ""]
    righe.append(f"**Inventario:** {len(pdf)} PDF · {len(zip_pacchetti)} ZIP · {len(schede)} schede HTML")
    righe.append("")

    bloccanti = len(problemi_corrotti) + len(drift) + len(link_rotti)

    if bloccanti == 0 and not orfani:
        righe.append("## ✅ Tutto a posto")
        righe.append("")
        righe.append("Nessun documento corrotto, nessun drift dei pacchetti ZIP, nessun link rotto, nessun documento orfano.")
    else:
        if bloccanti > 0:
            righe.append(f"## ⚠️ {bloccanti} problemi bloccanti")
        if orfani:
            righe.append(f"## ℹ️ {len(orfani)} documenti orfani (warning)")
        righe.append("")

    if problemi_corrotti:
        righe.append(f"### File corrotti o non leggibili ({len(problemi_corrotti)})")
        righe.append("")
        for tipo, p, err in problemi_corrotti:
            rel = p.relative_to(ROOT)
            righe.append(f"- **{tipo}** `{rel}` — {err}")
        righe.append("")

    if drift:
        righe.append(f"### Drift dei pacchetti ZIP ({len(drift)})")
        righe.append("")
        righe.append("Il contenuto attuale dei pacchetti non corrisponde a quello che lo script genera ora. Probabilmente il workflow `genera-pacchetti-kit.yml` è stato saltato dopo una modifica alle schede.")
        righe.append("")
        righe.append("**Soluzione:** lanciare manualmente `gh workflow run genera-pacchetti-kit.yml` oppure eseguire `python3 scripts/genera-pacchetti-kit.py` in locale e committare gli ZIP aggiornati.")
        righe.append("")
        for d in drift:
            righe.append(f"- {d}")
        righe.append("")

    if link_rotti:
        righe.append(f"### Link verso documenti inesistenti ({len(link_rotti)})")
        righe.append("")
        righe.append("Le pagine del sito linkano questi documenti, ma il file non esiste sul filesystem. Sono link che produrranno **404 in produzione**.")
        righe.append("")
        for link in link_rotti:
            righe.append(f"- `{link}`")
        righe.append("")

    if orfani:
        righe.append(f"### Documenti orfani — non linkati da nessuna pagina ({len(orfani)})")
        righe.append("")
        righe.append("Questi file esistono nel repo ma nessuna pagina del sito li linka. Possono essere intenzionali (asset usati solo via JS, redirect) oppure obsoleti da rimuovere.")
        righe.append("")
        for p in orfani:
            rel = p.relative_to(ROOT)
            righe.append(f"- `{rel}`")
        righe.append("")

    righe.append("---")
    righe.append("_Generato da `scripts/controllo-documenti.py` — verifica settimanale lunedì._")

    REPORT_PATH.write_text("\n".join(righe), encoding="utf-8")
    print(f"\nReport scritto in: {REPORT_PATH.relative_to(ROOT)}")
    print(f"Bloccanti: {bloccanti} · Orfani (warning): {len(orfani)}")

    return 1 if bloccanti > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
