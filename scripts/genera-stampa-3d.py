#!/usr/bin/env python3
"""Crea i file STL e le anteprime degli oggetti con il nominativo dei volontari (data/stampa_3d.yaml).
Uso: python3 scripts/genera-stampa-3d.py [--tutti] [--check]; servono openscad, trimesh, manifold3d e Pillow (pip),
e Playwright con Chromium per le anteprime in tre quarti dei ganci.
La base di ogni oggetto si calcola una volta sola; per ogni nominativo OpenSCAD fa solo le scritte e
manifold3d le unisce alla base (stesso risultato di OpenSCAD, trenta volte più veloce).

Per ogni oggetto e ogni nominativo scrive in static/stampa-3d/nominativi/<id>/ il file <prefisso>-NNN.stl
(STL binario, in millimetri, un solo pezzo per file) e l'anteprima <prefisso>-NNN.webp disegnata dal
file stesso, più retro.webp per il lato posteriore. Salta i file già presenti, salvo --tutti.
Controlla le regole pubblicate da Craftcloud per la stampa FDM (support.craftcloud3d.com, articoli
31 e 32, consultati il 23/11/2026): superficie chiusa, un pezzo per file, appoggio sul piano,
tratti delle lettere da 0,6 mm in su. Con --check controlla soltanto che i file ci siano tutti.
"""
import argparse
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import yaml

RADICE = Path(__file__).resolve().parent.parent
DATI = RADICE / "data/stampa_3d.yaml"
SORGENTI = RADICE / "static/stampa-3d/sorgenti"
USCITA = RADICE / "static/stampa-3d/nominativi"
TRATTO_MIN = 0.6


def nome_file(prefisso, n):
    return f"{prefisso.lower()}-{n:03d}.stl"


def tratto_minimo(font, size):
    """Tratto più sottile fra l'asta della «I» e le barre della «E» nel carattere indicato."""
    misure = []
    with tempfile.TemporaryDirectory() as d:
        for lettera, asse in (("I", "10"), ("E", "20")):
            scad, dxf = Path(d) / "l.scad", Path(d) / "l.dxf"
            scad.write_text(f'text("{lettera}", size={size}, font="{font}");')
            subprocess.run(["openscad", "-q", "-o", str(dxf), str(scad)], check=True)
            v = sorted({round(float(x), 3) for x in re.findall(rf"\n {asse}\n([-\d.]+)", dxf.read_text())})
            misure += [v[-1] - v[0]] if lettera == "I" else [v[i + 1] - v[i] for i in range(0, len(v) - 1, 2)]
    return min(misure)


def controlla_caratteri(sorgente):
    """Ogni coppia carattere-dimensione del modello deve avere tratti da TRATTO_MIN in su."""
    s = sorgente.read_text(encoding="utf-8")
    font = re.search(r'^font = "([^"]+)"', s, re.M).group(1)
    font2 = re.search(r'^font2 = "([^"]+)"', s, re.M).group(1)
    errori = []
    misure = re.findall(r'\["(\w+)",\s*\[([^\]]+)\]\]', s)
    if not misure:
        return [f"{sorgente.name}: tabella MISURE non trovata"]
    coppie = set()
    for _tipo, valori in misure:
        m = [float(x) for x in valori.split(",")]
        coppie |= {(font, m[4]), (font2, m[6])}
    for f, size in sorted(coppie):
        t = tratto_minimo(f, size)
        if t < TRATTO_MIN:
            errori.append(f"{sorgente.name}: {f} a {size} mm ha tratti di {t:.2f} mm (minimo {TRATTO_MIN})")
    return errori


def maschera(m, z, scala, w, h, ox, oy, specchia=False):
    """Sezione del pezzo all'altezza z come immagine in bianco e nero (fori compresi)."""
    from PIL import Image, ImageChops, ImageDraw
    sez = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    tot = Image.new("1", (w, h), 0)
    for anello in (sez.discrete if sez is not None else []):
        x = -anello[:, 0] if specchia else anello[:, 0]
        pts = [((xx - ox) * scala, (oy - yy) * scala) for xx, yy in zip(x, anello[:, 1])]
        un = Image.new("1", (w, h), 0)
        ImageDraw.Draw(un).polygon(pts, fill=1)
        tot = ImageChops.logical_xor(tot, un)
    return tot


TRICOLORE = [(0, 146, 70), (255, 255, 255), (206, 43, 55)]


def disegna(m, z_base, z_rilievo, colori, destinazione, specchia=False, z_incavi=None, bandiera=None):
    """Anteprima vista dall'alto: base colorata, rilievi del secondo colore con la loro ombra,
    oppure (z_incavi) il retro con gli incavi disegnati più scuri, perché non sono fori passanti."""
    from PIL import Image, ImageChops, ImageFilter
    scala, bordo = 16, 6
    (x0, y0, _), (x1, y1, _) = m.bounds
    w, h = int((x1 - x0 + 2 * bordo) * scala), int((y1 - y0 + 2 * bordo) * scala)
    ox, oy = (-x1 if specchia else x0) - bordo, y1 + bordo
    base = maschera(m, z_base, scala, w, h, ox, oy, specchia).convert("L")
    img = Image.new("RGB", (w, h), "white")
    ombra = base.filter(ImageFilter.GaussianBlur(18)).point(lambda v: v * 0.35)
    img.paste((40, 40, 40), (10, 16), ombra)
    img.paste(colori["base"], (0, 0), base)
    if z_incavi is not None:
        fondo = maschera(m, z_incavi, scala, w, h, ox, oy, specchia).convert("L")
        incavi = ImageChops.subtract(base, fondo)
        img.paste((12, 40, 85), (0, 0), incavi)
        img.paste((70, 120, 190), (0, 0), ImageChops.subtract(incavi, ImageChops.offset(incavi, 4, 5)))
    if z_rilievo is not None:
        ril = maschera(m, z_rilievo, scala, w, h, ox, oy, specchia).convert("L")
        img.paste((10, 25, 50), (5, 7), ril.filter(ImageFilter.GaussianBlur(3)).point(lambda v: v * 0.6))
        img.paste(colori["rilievo"], (0, 0), ril)
        if bandiera and not specchia:
            from PIL import ImageDraw
            x0, y0, x1, y1 = bandiera
            for i, col in enumerate(TRICOLORE):
                fascia = Image.new("L", (w, h), 0)
                xa, xb = x0 + (x1 - x0) * i / 3, x0 + (x1 - x0) * (i + 1) / 3
                ImageDraw.Draw(fascia).rectangle([(xa - ox) * scala, (oy - y1) * scala, (xb - ox) * scala, (oy - y0) * scala], fill=255)
                img.paste(col, (0, 0), ImageChops.multiply(fascia, ril))
    img = img.resize((w * 3 // 4, h * 3 // 4), Image.LANCZOS)
    img.save(destinazione, "WEBP", quality=82, method=6)


def scad(sorgente, parametri, uscita):
    cmd = ["openscad", "-q", "-o", str(uscita)]
    for k, v in parametri.items():
        cmd += ["-D", f'{k}="{v}"']
    subprocess.run(cmd + [str(sorgente)], check=True)


def unisci(a, b):
    """Unione booleana di due pezzi con manifold3d."""
    import manifold3d as mf
    import numpy as np
    import trimesh
    def man(m):
        return mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices, dtype=np.float32),
                                   tri_verts=np.asarray(m.faces, dtype=np.uint32)))
    r = (man(a) + man(b)).to_mesh()
    return trimesh.Trimesh(vertices=r.vert_properties[:, :3], faces=r.tri_verts, process=True)


def genera(sorgente, parametri, testo, destinazione, colori=None, retro=None, base_stl=None):
    import trimesh
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d) / "pezzo.stl"
        if base_stl:
            scad(sorgente, {**parametri, "riga1": testo, "parte": "testo"}, tmp)
            m = unisci(trimesh.load(base_stl), trimesh.load(tmp))
        else:
            scad(sorgente, {**parametri, "riga1": testo}, tmp)
            m = trimesh.load(tmp)
    errori = []
    if not m.is_watertight:
        errori.append("superficie non chiusa")
    if len(m.split(only_watertight=False)) != 1:
        errori.append("più di un pezzo nel file")
    if abs(m.bounds[0][2]) > 1e-6:
        errori.append("non appoggia sul piano")
    if errori:
        return f"{destinazione.name}: " + ", ".join(errori)
    destinazione.parent.mkdir(parents=True, exist_ok=True)
    m.export(destinazione)  # STL binario
    if colori:
        alto = m.bounds[1][2]
        rilievo = float(re.search(r"^rilievo = ([\d.]+);", sorgente.read_text(encoding="utf-8"), re.M).group(1))
        base = alto - rilievo
        if not colori.get("vista_3d"):
            disegna(m, base - 0.1, base + 0.4, colori, destinazione.with_suffix(".webp"), bandiera=colori.get("bandiera"))
        if retro:
            disegna(m, base - 0.1, None, colori, retro, specchia=True, z_incavi=0.05)
    return None


PAGINA_3D = """<!doctype html><html><body style="margin:0;background:#fff">
<script type="module">
import * as THREE from './vendor/three/three.module.min.js';
const q = new URLSearchParams(location.search), A = JSON.parse(q.get('a'));
const buf = await (await fetch(q.get('f'))).arrayBuffer(), dv = new DataView(buf), n = dv.getUint32(80, true);
const pos = new Float32Array(n * 9);
for (let i = 0; i < n; i++) for (let k = 0; k < 9; k++) pos[i * 9 + k] = dv.getFloat32(84 + i * 50 + 12 + k * 4, true);
const aree = new Map();
for (let t = 0; t < pos.length; t += 9) {
  const z0 = pos[t + 2]; if (Math.abs(z0 - pos[t + 5]) > 1e-3 || Math.abs(z0 - pos[t + 8]) > 1e-3) continue;
  const nz = (pos[t + 3] - pos[t]) * (pos[t + 7] - pos[t + 1]) - (pos[t + 4] - pos[t + 1]) * (pos[t + 6] - pos[t]);
  if (nz > 0) aree.set(z0.toFixed(2), (aree.get(z0.toFixed(2)) || 0) + nz);
}
let zb = 0, best = 0; aree.forEach((v, k) => { if (v > best) { best = v; zb = parseFloat(k); } });
const ril = A.rilievo_mm || 1, cb = new THREE.Color(A.base), cr = new THREE.Color(A.rilievo);
const tri = ['#009246', '#ffffff', '#ce2b37'].map(c => new THREE.Color(c)), col = new Float32Array(pos.length);
for (let t = 0; t < pos.length; t += 9) {
  const zm = Math.max(pos[t + 2], pos[t + 5], pos[t + 8]);
  let c = zm > zb + 0.01 && zm <= zb + ril + 0.02 ? cr : cb;
  if (c === cr && A.bandiera) {
    const [x0, y0, x1, y1] = A.bandiera, cx = (pos[t] + pos[t + 3] + pos[t + 6]) / 3, cy = (pos[t + 1] + pos[t + 4] + pos[t + 7]) / 3;
    if (cx >= x0 - 0.1 && cx <= x1 + 0.1 && cy >= y0 - 0.1 && cy <= y1 + 0.1) c = tri[Math.min(2, Math.floor((cx - x0) / (x1 - x0) * 3))];
  }
  for (let k = 0; k < 9; k += 3) { col[t + k] = c.r; col[t + k + 1] = c.g; col[t + k + 2] = c.b; }
}
const g = new THREE.BufferGeometry();
g.setAttribute('position', new THREE.BufferAttribute(pos, 3)); g.setAttribute('color', new THREE.BufferAttribute(col, 3));
g.computeBoundingBox(); const c = new THREE.Vector3(); g.boundingBox.getCenter(c); g.translate(-c.x, -c.y, -c.z); g.computeVertexNormals();
const r = new THREE.WebGLRenderer({ antialias: true, preserveDrawingBuffer: true }); r.setSize(1100, 640); r.setClearColor(0xffffff);
document.body.appendChild(r.domElement);
const sc = new THREE.Scene(); sc.add(new THREE.HemisphereLight(0xffffff, 0x8899aa, 1.6));
const l = new THREE.DirectionalLight(0xffffff, 1.6); l.position.set(-40, 60, 120); sc.add(l);
sc.add(new THREE.Mesh(g, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.6 })));
const s = new THREE.Vector3(); g.boundingBox.getSize(s);
const cam = new THREE.PerspectiveCamera(30, 1100 / 640, 1, 5000);
const d = Math.max(s.x, s.y * 1.72, s.z) * 0.5 / Math.tan(THREE.MathUtils.degToRad(15)) * 1.1;
cam.position.copy(new THREE.Vector3(0.85, -0.2, 0.75).normalize().multiplyScalar(d)); cam.lookAt(0, 0, 0);
r.render(sc, cam); window.pronto = true;
</script></body></html>"""


def anteprime_3d(voci):
    """Anteprime dei pezzi con parti in profondità (ganci): vista di tre quarti disegnata con three.js in Chromium."""
    import functools
    import http.server
    import io
    import threading
    from PIL import Image, ImageChops
    from playwright.sync_api import sync_playwright
    with tempfile.TemporaryDirectory() as d:
        Path(d, "vista.html").write_text(PAGINA_3D, encoding="utf-8")
        Path(d, "vendor").symlink_to(RADICE / "themes/flavour-pcgenzano/static/vendor")
        Path(d, "stampa-3d").symlink_to(RADICE / "static/stampa-3d")
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(
            http.server.SimpleHTTPRequestHandler, directory=d))
        srv.RequestHandlerClass.log_message = lambda *a: None
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{srv.server_address[1]}"
        import json
        import urllib.parse
        with sync_playwright() as pw:
            br = pw.chromium.launch(args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader"])
            pg = br.new_page(viewport={"width": 1100, "height": 640})
            for stl, colori in voci:
                rel = stl.resolve().relative_to(RADICE / "static").as_posix()
                q = urllib.parse.urlencode({"f": "/" + rel, "a": json.dumps(colori)})
                pg.goto(f"{base}/vista.html?{q}")
                pg.wait_for_function("window.pronto === true", timeout=60000)
                png = pg.locator("canvas").screenshot()
                im = Image.open(io.BytesIO(png)).convert("RGB")
                bb = ImageChops.difference(im, Image.new("RGB", im.size, "white")).getbbox()
                if bb:                                  # ritaglio sul pezzo, poi stesso formato delle altre anteprime
                    im = im.crop(bb)
                    w, h = im.size
                    sc = min(1000 / w, 420 / h)
                    im = im.resize((int(w * sc), int(h * sc)), Image.LANCZOS)
                    tela = Image.new("RGB", (1100, 500), "white")
                    tela.paste(im, ((1100 - im.width) // 2, (500 - im.height) // 2))
                    im = tela
                im.save(stl.with_suffix(".webp"), "WEBP", quality=82, method=6)
            br.close()
        srv.shutdown()


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tutti", action="store_true", help="rifà anche i file già presenti")
    ap.add_argument("--check", action="store_true", help="controlla solo che i file ci siano tutti")
    a = ap.parse_args()
    dati = yaml.safe_load(DATI.read_text(encoding="utf-8"))
    nom = dati["nominativi"]
    numeri = range(nom["primo"], nom["ultimo"] + 1)
    errori, lavori = [], []
    cartella_basi = tempfile.TemporaryDirectory()
    for ogg in dati["oggetti"]:
        sorgente = SORGENTI / ogg["sorgente"]
        if not sorgente.exists():
            errori.append(f"manca il modello {sorgente.relative_to(RADICE)}")
            continue
        for n in numeri:
            dest = USCITA / ogg["id"] / nome_file(nom["prefisso"], n)
            if a.check:
                if not dest.exists():
                    errori.append(f"manca {dest.relative_to(RADICE)}")
                if not dest.with_suffix(".webp").exists():
                    errori.append(f"manca l'anteprima {dest.with_suffix('.webp').relative_to(RADICE)}")
            elif a.tutti or not dest.exists() or not dest.with_suffix(".webp").exists():
                retro = dest.parent / "retro.webp" if n == nom["primo"] and ogg.get("retro") else None
                base_stl = Path(cartella_basi.name) / f'{ogg["id"]}-base.stl'
                if not base_stl.exists():
                    scad(sorgente, {**ogg.get("parametri", {}), "parte": "base"}, base_stl)
                lavori.append((sorgente, ogg.get("parametri", {}), f'{nom["prefisso"]} {n}', dest,
                               ogg.get("anteprima"), retro, base_stl))
        if not a.check:
            errori += controlla_caratteri(sorgente)
    with ProcessPoolExecutor() as ex:
        errori += [e for e in ex.map(genera, *zip(*lavori)) if e] if lavori else []
    voci_3d = [(l[3], l[4]) for l in lavori if l[4] and l[4].get("vista_3d") and l[3].exists()]
    if voci_3d and not errori:
        anteprime_3d(voci_3d)
    if errori:
        print("ERRORI:\n- " + "\n- ".join(errori))
        sys.exit(1)
    print(f"Stampa 3D: tutto a posto ({len(lavori)} file creati).")


if __name__ == "__main__":
    main()
