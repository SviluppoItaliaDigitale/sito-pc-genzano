#!/usr/bin/env python3
"""Controllo SVG didattici CAST-UDL e riferimenti alle illustrazioni Hugo.

Le immagini non sono sostitutive del testo: verifica che abbiano una didascalia
e una descrizione alternativa, senza script o risorse esterne negli SVG.
"""
import pathlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "static/formazione/illustrazioni-udl"
SHORTCODE = re.compile(r"\{\{<\s*illustrazione-udl\s+([^>]*?)>\}\}", re.S)
ATTR = re.compile(r'\b(src|alt|caption)\s*=\s*"([^"]*)"')
SVG = "{http://www.w3.org/2000/svg}"
errors = []
references = {}
files = sorted(ASSETS.glob("*.svg"))
for file in files:
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        if root.tag != SVG + "svg":
            errors.append(f"{file}: elemento radice svg errato")
        if not root.attrib.get("viewBox"):
            errors.append(f"{file}: viewBox mancante")
        for tag in ("title", "desc"):
            el = root.find(SVG + tag)
            if el is None or not "".join(el.itertext()).strip():
                errors.append(f"{file}: {tag} mancante o vuoto")
        for el in root.iter():
            local = el.tag.split("}")[-1]
            if local in ("script", "foreignObject"):
                errors.append(f"{file}: elemento non permesso {local}")
            for key, val in el.attrib.items():
                name = key.split("}")[-1]
                if name.lower().startswith("on") or ("href" in name.lower() and (
                    val.startswith("http:") or val.startswith("https:") or val.startswith("//")
                )):
                    errors.append(f"{file}: attributo o risorsa esterna non permessi")
    except ET.ParseError as exc:
        errors.append(f"{file}: XML non valido: {exc}")

for page in (ROOT / "content").rglob("*.md"):
    content = page.read_text(encoding="utf-8")
    for match in SHORTCODE.finditer(content):
        attrs = dict(ATTR.findall(match.group(1)))
        for field in ("src", "alt", "caption"):
            if not attrs.get(field, "").strip():
                errors.append(f"{page}: {field} mancante per illustrazione-udl")
        source = attrs.get("src", "")
        if not source.startswith("/formazione/illustrazioni-udl/"):
            errors.append(f"{page}: percorso fuori dalla directory consentita: {source}")
            continue
        image = ROOT / "static" / source.lstrip("/")
        if not image.is_file():
            errors.append(f"{page}: SVG non trovato: {source}")
        references[source] = references.get(source, 0) + 1

if not files:
    errors.append("Nessuna illustrazione SVG trovata")
if errors:
    for msg in errors:
        print("ERRORE:", msg)
    sys.exit(1)
print(f"OK: {len(files)} SVG, {sum(references.values())} inserimenti in {len(references)} immagini referenziate.")
