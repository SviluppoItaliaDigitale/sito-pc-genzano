#!/usr/bin/env python3
"""
Parità delle schede stampabili fra i quattro formati di distribuzione.

Ogni scheda didattica ha una sola fonte di verità (index.html nella sua
cartella) e quattro uscite che devono dire la stessa cosa:

  1. pagina singola   static/formazione/schede-stampabili/<slug>/index.html
  2. "Stampa tutto"   static/formazione/schede-stampabili/pacchetti/<fascia>.html
  3. ZIP offline      static/formazione/pacchetti/kit-scuola-<fascia>.zip
  4. elenco del kit   content/formazione/kit-scuola-<fascia>.md

Controlli (audit esterno del 06/09/2026, rilievi F02, F03, F08, F09):

  - insiemi di slug identici fra kit, pacchetto HTML, ZIP e cartelle esistenti;
  - le avvertenze obbligatorie (nota per l'adulto, note per il docente,
    soluzioni capovolte) presenti nella scheda singola devono comparire anche
    nel pacchetto "Stampa tutto" e nello ZIP: se stanno fuori dal wrapper
    stampabile il generatore le perde in silenzio;
  - lo ZIP deve aprirsi offline: nessun href/src radicato su "/", foglio di
    stile e immagini risolvibili dentro l'archivio.

Uso:
  python3 scripts/check-parita-schede.py            # tutte le fasce
  python3 scripts/check-parita-schede.py --report /tmp/parita.md
Exit code = numero di errori (0 = parità completa).
"""

from __future__ import annotations

import argparse
import posixpath
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEDE = ROOT / "static" / "formazione" / "schede-stampabili"
PACCHETTI_HTML = SCHEDE / "pacchetti"
PACCHETTI_ZIP = ROOT / "static" / "formazione" / "pacchetti"
KIT_DIR = ROOT / "content" / "formazione"

# fascia del pacchetto HTML → (kit markdown, nome ZIP)
FASCE = {
    "infanzia": ("kit-scuola-infanzia.md", "kit-scuola-infanzia.zip"),
    "primaria": ("kit-scuola-primaria.md", "kit-scuola-primaria.zip"),
    "secondaria": ("kit-scuola-secondaria-primo-grado.md", "kit-scuola-secondaria-primo-grado.zip"),
    "secondaria2": ("kit-scuola-secondaria-secondo-grado.md", "kit-scuola-secondaria-secondo-grado.zip"),
}

# Blocchi che, se presenti nella scheda singola, devono sopravvivere in
# "Stampa tutto" e nello ZIP. Sono le avvertenze e le istruzioni che un
# docente deve poter leggere sul foglio, non solo online.
CLASSI_OBBLIGATORIE = (
    "nota-adulto-box",
    "nota-adulto",
    "istruzioni-prof",
    "istruzioni-docente",
    "scheda-docente",
    "soluzione-capovolta",
    "avvertenza",
)

RE_SLUG = re.compile(r"/formazione/schede-stampabili/([a-z0-9][a-z0-9-]*?)/?(?=[)\"\s\]])")
RE_TAG = re.compile(r"<[^>]+>")
RE_WS = re.compile(r"\s+")


def slugs_kit(md_path: Path) -> list[str]:
    testo = md_path.read_text(encoding="utf-8")
    visti: list[str] = []
    for m in RE_SLUG.finditer(testo):
        slug = m.group(1)
        if slug in ("assets", "pacchetti") or slug in visti:
            continue
        visti.append(slug)
    return visti


def testo_pulito(html: str) -> str:
    return RE_WS.sub(" ", RE_TAG.sub(" ", html)).strip()


def blocchi_obbligatori(html: str) -> list[tuple[str, str]]:
    """Ritorna (classe, impronta testuale) dei blocchi obbligatori trovati."""
    trovati: list[tuple[str, str]] = []
    for classe in CLASSI_OBBLIGATORIE:
        for m in re.finditer(r'<(\w+)[^>]*class="[^"]*\b' + re.escape(classe) + r'\b[^"]*"[^>]*>', html):
            tag = m.group(1)
            fine = html.find(f"</{tag}>", m.end())
            if fine < 0:
                continue
            testo = testo_pulito(html[m.end():fine])
            if len(testo) < 20:
                continue
            impronta = testo[:80]
            if (classe, impronta) not in trovati:
                trovati.append((classe, impronta))
    return trovati


def impronta_presente(impronta: str, corpus_testo: str) -> bool:
    return impronta in corpus_testo


def controlla_zip_offline(zf: zipfile.ZipFile, errori: list[str], fascia: str) -> None:
    nomi = set(zf.namelist())
    for nome in sorted(nomi):
        if not (nome.startswith("schede/") and nome.endswith("index.html")):
            continue
        html = zf.read(nome).decode("utf-8", errors="replace")
        base = posixpath.dirname(nome)
        for attr, valore in re.findall(r'\b(href|src)="([^"]+)"', html):
            if valore.startswith("/"):
                errori.append(f"[{fascia}] ZIP {nome}: {attr}=\"{valore}\" radicato su / (offline apre il disco, non il sito)")
                continue
            if valore.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:", "javascript:")):
                continue
            pulito = valore.split("#", 1)[0].split("?", 1)[0]
            if not pulito:
                continue
            risolto = posixpath.normpath(posixpath.join(base, pulito))
            if risolto not in nomi:
                errori.append(f"[{fascia}] ZIP {nome}: {attr}=\"{valore}\" non risolvibile dentro l'archivio ({risolto})")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", help="scrive un report Markdown nel percorso indicato")
    args = ap.parse_args()

    errori: list[str] = []
    righe_report: list[str] = ["# Parità schede stampabili", ""]

    for fascia, (kit_md, zip_nome) in FASCE.items():
        kit_path = KIT_DIR / kit_md
        pacchetto_path = PACCHETTI_HTML / f"{fascia}.html"
        zip_path = PACCHETTI_ZIP / zip_nome
        if not kit_path.exists():
            errori.append(f"[{fascia}] kit mancante: {kit_path.relative_to(ROOT)}")
            continue

        attesi = slugs_kit(kit_path)
        set_kit = set(attesi)

        # cartelle esistenti
        set_cartelle = {s for s in attesi if (SCHEDE / s / "index.html").exists()}
        for s in sorted(set_kit - set_cartelle):
            errori.append(f"[{fascia}] il kit linka la scheda '{s}' ma static/formazione/schede-stampabili/{s}/index.html non esiste")

        # pacchetto HTML
        testo_pacchetto = ""
        if pacchetto_path.exists():
            html_p = pacchetto_path.read_text(encoding="utf-8")
            set_pacchetto = set(re.findall(r'id="scheda-([a-z0-9-]+)"', html_p))
            testo_pacchetto = testo_pulito(html_p)
            for s in sorted(set_cartelle - set_pacchetto):
                errori.append(f"[{fascia}] 'Stampa tutto' ({pacchetto_path.name}) non contiene la scheda '{s}' presente nel kit")
            for s in sorted(set_pacchetto - set_kit):
                errori.append(f"[{fascia}] 'Stampa tutto' ({pacchetto_path.name}) contiene '{s}' che il kit non linka più")
        else:
            errori.append(f"[{fascia}] pacchetto HTML mancante: {pacchetto_path.relative_to(ROOT)}")

        # ZIP
        testo_zip_per_slug: dict[str, str] = {}
        if zip_path.exists():
            with zipfile.ZipFile(zip_path) as zf:
                nomi = zf.namelist()
                set_zip = {m.group(1) for n in nomi for m in [re.match(r"schede/([a-z0-9-]+)/index\.html$", n)] if m}
                for s in sorted(set_cartelle - set_zip):
                    errori.append(f"[{fascia}] ZIP {zip_nome} non contiene la scheda '{s}' presente nel kit")
                for s in sorted(set_zip - set_kit):
                    errori.append(f"[{fascia}] ZIP {zip_nome} contiene '{s}' che il kit non linka più")
                for s in set_zip:
                    testo_zip_per_slug[s] = testo_pulito(zf.read(f"schede/{s}/index.html").decode("utf-8", errors="replace"))
                controlla_zip_offline(zf, errori, fascia)
        else:
            errori.append(f"[{fascia}] ZIP mancante: {zip_path.relative_to(ROOT)}")

        # avvertenze obbligatorie
        n_blocchi = 0
        for s in sorted(set_cartelle):
            html_s = (SCHEDE / s / "index.html").read_text(encoding="utf-8")
            for classe, impronta in blocchi_obbligatori(html_s):
                n_blocchi += 1
                if testo_pacchetto and not impronta_presente(impronta, testo_pacchetto):
                    errori.append(f"[{fascia}] scheda '{s}': il blocco .{classe} («{impronta[:50]}…») manca in 'Stampa tutto' — probabilmente sta fuori dal wrapper stampabile")
                if s in testo_zip_per_slug and not impronta_presente(impronta, testo_zip_per_slug[s]):
                    errori.append(f"[{fascia}] scheda '{s}': il blocco .{classe} manca nello ZIP")

        righe_report.append(f"- **{fascia}**: {len(attesi)} schede nel kit, {n_blocchi} blocchi obbligatori verificati")

    if errori:
        righe_report += ["", "## Errori", ""] + [f"- ❌ {e}" for e in errori]
    else:
        righe_report += ["", "✅ Parità completa: kit, 'Stampa tutto', ZIP e cartelle coincidono; avvertenze presenti in ogni formato; ZIP apribili offline."]

    testo = "\n".join(righe_report)
    print(testo)
    if args.report:
        Path(args.report).write_text(testo + "\n", encoding="utf-8")
    return len(errori)


if __name__ == "__main__":
    sys.exit(main())
