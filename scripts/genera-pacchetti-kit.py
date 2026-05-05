#!/usr/bin/env python3
"""
Genera ZIP offline dei kit didattici scolastici.

Per ogni kit-scuola-*.md in content/formazione/, parsa i link
/formazione/schede-stampabili/<slug>/ ed estrae le schede HTML autostampabili
in un pacchetto ZIP che contiene:

  kit-scuola-<fascia>.zip
  ├── INDICE.html             — pagina indice cliccabile (apri in browser)
  ├── README.txt              — istruzioni d'uso e licenza
  ├── kit-scuola-<fascia>.md  — testo originale del kit
  ├── assets/
  │   └── scheda-print.css    — stili condivisi
  └── schede/
      ├── <slug-1>/index.html
      ├── <slug-2>/index.html
      └── ...

Output in static/formazione/pacchetti/.

Idempotente: ricrea sempre lo ZIP da zero, basato solo sui link presenti
nei kit e sulle schede effettivamente esistenti nel filesystem.
"""

import os
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

KITS = {
    "infanzia": "kit-scuola-infanzia.md",
    "primaria": "kit-scuola-primaria.md",
    "secondaria-primo-grado": "kit-scuola-secondaria-primo-grado.md",
    "secondaria-secondo-grado": "kit-scuola-secondaria-secondo-grado.md",
}

CONTENT_BASE = ROOT / "content" / "formazione"
SCHEDE_BASE = ROOT / "static" / "formazione" / "schede-stampabili"
OUTPUT_DIR = ROOT / "static" / "formazione" / "pacchetti"


def estrai_titolo_kit(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r'^title:\s*"([^"]+)"', text, re.MULTILINE)
    return m.group(1) if m else md_path.stem


def estrai_descrizione_kit(md_path: Path) -> str:
    text = md_path.read_text(encoding="utf-8")
    m = re.search(r'^description:\s*"([^"]+)"', text, re.MULTILINE)
    return m.group(1) if m else ""


def estrai_link_schede(md_path: Path) -> list[str]:
    """Ritorna lista di slug schede linkati dal kit, ordine di prima apparizione."""
    text = md_path.read_text(encoding="utf-8")
    seen = []
    for m in re.finditer(r'/formazione/schede-stampabili/([a-z0-9][a-z0-9-]*?)/?(?=[)"\s\]])', text):
        slug = m.group(1)
        if slug == "assets":
            continue
        if slug not in seen:
            seen.append(slug)
    return seen


def patch_html_paths(html: str) -> str:
    """Riscrive path assoluti dipendenti dal sito in path relativi offline."""
    # CSS condiviso: assoluto -> relativo dalla cartella schede/<slug>/
    html = html.replace(
        '/formazione/schede-stampabili/assets/scheda-print.css',
        '../../assets/scheda-print.css',
    )
    # Favicon assoluto: rimuovo (non serve offline, evita errori 404 nel browser)
    html = re.sub(
        r'<link[^>]+rel=["\']?(?:icon|shortcut icon)["\']?[^>]*>',
        '',
        html,
        flags=re.IGNORECASE,
    )
    # Link "Torna alle schede" (assoluto al sito): lo neutralizzo a riferimento all'indice del pacchetto
    html = html.replace(
        'href="/formazione/schede-stampabili/"',
        'href="../../INDICE.html"',
    )
    return html


def estrai_titolo_scheda(html: str) -> str:
    m = re.search(r'<title>([^<]+)</title>', html, re.IGNORECASE)
    if not m:
        return "Scheda"
    titolo = m.group(1).strip()
    # Rimuovo prefisso comune "Scheda stampabile: " se presente
    titolo = re.sub(r'^Scheda stampabile:\s*', '', titolo, flags=re.IGNORECASE)
    return titolo


def estrai_descrizione_scheda(html: str) -> str:
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', html, re.IGNORECASE)
    return m.group(1).strip() if m else ""


def genera_indice_html(kit_titolo: str, kit_desc: str, schede: list[tuple[str, str, str]]) -> str:
    """schede = lista di (slug, titolo, descrizione)."""
    items_html = []
    for slug, titolo, desc in schede:
        desc_html = f'<p class="indice-desc">{desc}</p>' if desc else ''
        items_html.append(
            f'''        <li class="indice-item">
          <a href="schede/{slug}/index.html" class="indice-link">
            <span class="indice-titolo">{titolo}</span>
            {desc_html}
            <span class="indice-path">schede/{slug}/</span>
          </a>
        </li>'''
        )
    items = "\n".join(items_html)
    return f'''<!DOCTYPE html>
<html lang="it" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Indice — {kit_titolo}</title>
<style>
  * {{ box-sizing: border-box; }}
  body {{
    max-width: 900px;
    margin: 0 auto;
    padding: 1.5rem 1rem 3rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #212529;
    line-height: 1.55;
    background: #fff;
  }}
  header.kit-header {{
    background: #003366;
    color: #fff;
    padding: 1.4rem 1.5rem;
    border-radius: 8px;
    margin-bottom: 1.5rem;
  }}
  header.kit-header h1 {{
    margin: 0 0 0.4rem;
    font-size: 1.7rem;
  }}
  header.kit-header p {{
    margin: 0;
    font-size: 1rem;
    opacity: 0.92;
  }}
  .istruzioni {{
    background: #fff8e1;
    border-left: 5px solid #b45309;
    padding: 0.9rem 1.1rem;
    margin: 1.2rem 0 1.6rem;
    border-radius: 4px;
  }}
  .istruzioni strong {{ color: #b45309; }}
  h2 {{
    color: #003366;
    border-bottom: 3px solid #003366;
    padding-bottom: 0.4rem;
    font-size: 1.3rem;
    margin-top: 2rem;
  }}
  ul.indice-list {{
    list-style: none;
    padding: 0;
    margin: 0;
  }}
  .indice-item {{ margin-bottom: 0.7rem; }}
  .indice-link {{
    display: block;
    padding: 0.85rem 1rem;
    border: 1.5px solid #adb5bd;
    border-radius: 6px;
    text-decoration: none;
    color: #1a1a1a;
    background: #fff;
    transition: background 0.15s, border-color 0.15s;
  }}
  .indice-link:hover, .indice-link:focus {{
    background: #f0f4f8;
    border-color: #003366;
    outline: none;
  }}
  .indice-link:focus {{
    outline: 3px solid #ffbe2e;
    outline-offset: 2px;
  }}
  .indice-titolo {{
    display: block;
    color: #003366;
    font-weight: 700;
    font-size: 1.05rem;
    margin-bottom: 0.2rem;
  }}
  .indice-desc {{
    margin: 0.2rem 0;
    font-size: 0.92rem;
    color: #495057;
  }}
  .indice-path {{
    display: block;
    margin-top: 0.3rem;
    font-size: 0.8rem;
    color: #6c757d;
    font-family: monospace;
  }}
  footer {{
    margin-top: 2.5rem;
    padding-top: 1rem;
    border-top: 1px solid #dee2e6;
    font-size: 0.85rem;
    color: #6c757d;
    text-align: center;
  }}
  footer a {{ color: #003366; }}
</style>
</head>
<body>

<header class="kit-header">
<h1>{kit_titolo}</h1>
<p>Pacchetto offline — {len(schede)} schede pronte da stampare</p>
</header>

<div class="istruzioni">
<strong>Come si usa:</strong> apri questo file <code>INDICE.html</code> con doppio click (si apre nel browser predefinito). Da qui clicca su una scheda per aprirla, poi premi <strong>Ctrl+P</strong> (Windows) o <strong>⌘P</strong> (Mac) per stamparla. Tutto funziona offline, senza connessione internet.
</div>

<p>{kit_desc}</p>

<h2>Schede in questo pacchetto</h2>
<ul class="indice-list">
{items}
</ul>

<footer>
<p>Gruppo Comunale Volontari di Protezione Civile — Genzano di Roma<br>
<a href="https://www.protezionecivilegenzano.it/">protezionecivilegenzano.it</a> · <a href="mailto:segreteria@protezionecivilegenzano.it">segreteria@protezionecivilegenzano.it</a></p>
<p>Pacchetto generato automaticamente — i materiali sono distribuiti gratuitamente per uso scolastico e didattico. Per le schede con pittogrammi ARASAAC: licenza CC BY-NC-SA 4.0.</p>
</footer>

</body>
</html>
'''


def genera_readme(kit_titolo: str, n_schede: int, slug: str) -> str:
    return f'''KIT DIDATTICO PROTEZIONE CIVILE
{kit_titolo}
Pacchetto offline · {n_schede} schede · {slug}

================================================================
COME SI USA
================================================================

1. Estrai questo ZIP in una cartella sul tuo computer.

2. Apri il file INDICE.html con doppio click (si apre nel browser).

3. Da lì hai accesso a tutte le schede. Per stampare una scheda:
   apri la scheda, premi Ctrl+P (Windows) o Cmd+P (Mac).

Le schede sono pensate per la stampa A4. Il CSS dedicato nasconde
la barra di navigazione e mostra solo il contenuto stampabile.


================================================================
MODIFICARE UNA SCHEDA
================================================================

Le schede sono file HTML semplici. Per personalizzarle (logo della
scuola, nome insegnante, modifica di un campo) aprile con un editor
di testo (Blocco Note su Windows, TextEdit su Mac, VS Code, ecc.)
e modifica il contenuto. Salva e ristampa.


================================================================
LICENZA
================================================================

I materiali del Gruppo Comunale Volontari di Protezione Civile di
Genzano di Roma sono distribuiti gratuitamente per uso scolastico
e didattico. Citazione del Gruppo gradita ma non obbligatoria.

Per le schede che includono pittogrammi ARASAAC: licenza
CC BY-NC-SA 4.0, attribuzione obbligatoria. Vedi:
https://www.protezionecivilegenzano.it/attribuzioni-pittogrammi/


================================================================
AGGIORNAMENTI
================================================================

Questo pacchetto è generato automaticamente: ogni volta che
aggiungiamo, modifichiamo o togliamo una scheda dal kit, una
nuova versione del pacchetto è disponibile su:

https://www.protezionecivilegenzano.it/formazione/schede-stampabili/

Per restare aggiornato, ri-scarica il pacchetto periodicamente.


================================================================
CONTATTI
================================================================

Gruppo Comunale Volontari di Protezione Civile
Via Sicilia 13-15, Genzano di Roma
segreteria@protezionecivilegenzano.it
https://www.protezionecivilegenzano.it/
'''


def costruisci_pacchetto(slug: str, md_filename: str) -> tuple[int, int, list[str]]:
    """Ritorna (n_schede_incluse, dimensione_kb, lista_schede_mancanti)."""
    md_path = CONTENT_BASE / md_filename
    if not md_path.exists():
        print(f"⚠ File non trovato: {md_path}", file=sys.stderr)
        return (0, 0, [])

    kit_titolo = estrai_titolo_kit(md_path)
    kit_desc = estrai_descrizione_kit(md_path)
    schede_slug = estrai_link_schede(md_path)
    print(f"\n=== {slug} ===")
    print(f"  Titolo: {kit_titolo}")
    print(f"  Schede linkate: {len(schede_slug)}")

    schede_dati: list[tuple[str, str, str]] = []
    schede_mancanti: list[str] = []

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        # asset condivisi
        (tmp / "assets").mkdir()
        css_src = SCHEDE_BASE / "assets" / "scheda-print.css"
        if css_src.exists():
            shutil.copy(css_src, tmp / "assets" / "scheda-print.css")
        else:
            print(f"  ⚠ CSS non trovato: {css_src}", file=sys.stderr)

        # schede
        (tmp / "schede").mkdir()
        for s_slug in schede_slug:
            src_dir = SCHEDE_BASE / s_slug
            src_html = src_dir / "index.html"
            if not src_html.exists():
                schede_mancanti.append(s_slug)
                continue
            dst_dir = tmp / "schede" / s_slug
            dst_dir.mkdir(parents=True, exist_ok=True)
            html = src_html.read_text(encoding="utf-8")
            html_patched = patch_html_paths(html)
            (dst_dir / "index.html").write_text(html_patched, encoding="utf-8")
            # copia eventuali asset locali (immagini, css, js, json) accanto alla scheda
            for asset in src_dir.iterdir():
                if asset.name == "index.html" or asset.is_dir():
                    continue
                shutil.copy(asset, dst_dir / asset.name)
            titolo = estrai_titolo_scheda(html_patched)
            descrizione = estrai_descrizione_scheda(html_patched)
            schede_dati.append((s_slug, titolo, descrizione))

        # indice
        indice = genera_indice_html(kit_titolo, kit_desc, schede_dati)
        (tmp / "INDICE.html").write_text(indice, encoding="utf-8")

        # readme
        readme = genera_readme(kit_titolo, len(schede_dati), slug)
        (tmp / "README.txt").write_text(readme, encoding="utf-8")

        # copia kit md (testo originale)
        shutil.copy(md_path, tmp / md_filename)

        # zip
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        zip_path = OUTPUT_DIR / f"kit-scuola-{slug}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for path in sorted(tmp.rglob("*")):
                if path.is_file():
                    arcname = path.relative_to(tmp)
                    zf.write(path, arcname)

        size_kb = zip_path.stat().st_size // 1024
        print(f"  → {zip_path.relative_to(ROOT)} ({size_kb} KB, {len(schede_dati)} schede)")
        if schede_mancanti:
            print(f"  ⚠ Linkate ma MANCANTI nel filesystem: {schede_mancanti}", file=sys.stderr)
        return (len(schede_dati), size_kb, schede_mancanti)


def main() -> int:
    print("Genera pacchetti ZIP dei kit scolastici")
    print("=" * 60)
    totale_schede = 0
    totale_kb = 0
    tutti_mancanti: list[tuple[str, str]] = []

    for slug, filename in KITS.items():
        n, kb, mancanti = costruisci_pacchetto(slug, filename)
        totale_schede += n
        totale_kb += kb
        for m in mancanti:
            tutti_mancanti.append((slug, m))

    print("\n" + "=" * 60)
    print(f"Totale: {totale_schede} schede in {len(KITS)} pacchetti, {totale_kb} KB complessivi")

    if tutti_mancanti:
        print(f"\n⚠ {len(tutti_mancanti)} link a schede non esistenti nel filesystem:")
        for kit_slug, scheda_slug in tutti_mancanti:
            print(f"  - {kit_slug}: {scheda_slug}")
        # exit non zero per segnalare in CI senza fallire la build
        return 0  # non blocchiamo: lo ZIP è stato comunque prodotto

    return 0


if __name__ == "__main__":
    sys.exit(main())
