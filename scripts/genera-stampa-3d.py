#!/usr/bin/env python3
"""Crea i file STL e le anteprime degli oggetti con il nominativo dei volontari (data/stampa_3d.yaml).
Uso: python3 scripts/genera-stampa-3d.py [--tutti] [--check]; servono openscad, trimesh, manifold3d e Pillow (pip),
Playwright con Chromium per le anteprime in tre quarti dei ganci e i caratteri dei modelli (su Ubuntu:
apt-get install fonts-liberation fonts-liberation-sans-narrow). Se un carattere manca lo script si ferma: OpenSCAD
ne userebbe un altro senza dirlo, e le scritte uscirebbero più larghe o più strette di come sono state misurate.
La base di ogni oggetto si calcola una volta sola; per ogni nominativo OpenSCAD fa solo le scritte e
manifold3d le unisce alla base (stesso risultato di OpenSCAD, trenta volte più veloce).

I modelli di partenza (famiglie di oggetti) stanno in scripts/stampa-3d/. Ogni oggetto ha la sua
cartella static/stampa-3d/<id>/, dove sta anche la sua pagina: il modello <id>.scad già impostato per
quell'oggetto, il file <prefisso>-NNN.stl per ogni nominativo (STL binario, in millimetri, un solo
pezzo) e l'anteprima <prefisso>-NNN.webp disegnata dal file stesso, più retro.webp per il lato
posteriore. Salta gli STL già presenti, salvo --tutti; il modello .scad si riscrive sempre.
Un oggetto in due pezzi (per esempio scatola e coperchio) ha «secondo_pezzo» nel catalogo: il pezzo con
le scritte cambia con il nominativo, il secondo è uguale per tutti e si crea una volta sola, con gli stessi controlli.
Se i due pezzi si montano insieme (gruccia, vassoio), «insieme» nell'anteprima aggiunge il secondo pezzo alle
anteprime, nella posizione di montaggio: nei file da stampare ogni pezzo resta da solo.
Nei modelli con viti controlla che la testa delle viti non copra mai bandiera e scritte.
Controlla le regole pubblicate da Craftcloud per la stampa FDM (support.craftcloud3d.com, articoli
31 e 32, consultati il 23/11/2026): superficie chiusa, un pezzo per file, appoggio sul piano,
tratti delle lettere da 0,6 mm in su. Con --check controlla soltanto che i file ci siano tutti e che
i modelli pubblicati siano allineati a quelli di partenza.
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
SORGENTI = RADICE / "scripts/stampa-3d"
USCITA = RADICE / "static/stampa-3d"
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


def carattere_installato(nome):
    """fontconfig risponde sempre con un carattere: se la famiglia non è quella chiesta, il carattere manca
    e OpenSCAD scriverebbe con il sostituto (25/11/2026: senza Liberation Sans Narrow le righe piccole uscivano
    con un carattere più largo, e il controllo delle viti scattava su tre oggetti già pubblicati)."""
    try:
        r = subprocess.run(["fc-match", "-f", "%{family}", nome], capture_output=True, text=True)
    except FileNotFoundError:
        return False
    return r.returncode == 0 and nome.split(":")[0].strip().lower() in [f.strip().lower() for f in r.stdout.split(",")]


def controlla_caratteri(sorgente):
    """Ogni coppia carattere-dimensione del modello deve avere tratti da TRATTO_MIN in su."""
    s = sorgente.read_text(encoding="utf-8")
    font = re.search(r'^font = "([^"]+)"', s, re.M).group(1)
    font2 = re.search(r'^font2 = "([^"]+)"', s, re.M).group(1)
    mancanti = [f for f in (font, font2) if not carattere_installato(f)]
    if mancanti:
        return [f"{sorgente.name}: manca il carattere «{f}» (su Ubuntu: apt-get install fonts-liberation "
                "fonts-liberation-sans-narrow): le scritte uscirebbero con un altro carattere" for f in mancanti]
    errori = []
    misure = re.findall(r'\["(\w+)",\s*\[([^\]]+)\]\]', s)
    if not misure:
        return [f"{sorgente.name}: tabella MISURE non trovata"]
    coppie = set()
    for _tipo, valori in misure:
        m = [float(x) for x in valori.split(",")]
        coppie |= {(font, m[4]), (font2, m[6])}
    # dimensioni scritte a mano nelle chiamate (riga(testo, x, y, 4, font2) o text(..., size = 4, font = font2))
    nomi = {"font": font, "font2": font2}
    for size, f in re.findall(r'riga\([^;]*?,\s*([\d.]+),\s*(font2?)\b', s):
        coppie.add((nomi[f], float(size)))
    for size, f in re.findall(r'size\s*=\s*([\d.]+),\s*font\s*=\s*(font2?)\b', s):
        coppie.add((nomi[f], float(size)))
    for f, size in sorted(coppie):
        t = tratto_minimo(f, size)
        if t < TRATTO_MIN:
            errori.append(f"{sorgente.name}: {f} a {size} mm ha tratti di {t:.2f} mm (minimo {TRATTO_MIN})")
    return errori


def modello_oggetto(sorgente, ogg):
    """Testo del modello .scad pubblicato nella cartella dell'oggetto: il modello della famiglia con
    i parametri dell'oggetto già impostati e due righe in testa su come usarlo."""
    s = sorgente.read_text(encoding="utf-8")
    for k, v in ogg.get("parametri", {}).items():
        s, n = re.subn(rf'^{k} = "[^"]*";', f'{k} = "{v}";', s, count=1, flags=re.M)
        if not n:
            raise SystemExit(f"{sorgente.name}: manca il parametro {k} per {ogg['id']}")
    testa = (f"// {ogg['nome']} con il nominativo. Modello per OpenSCAD (https://openscad.org/), gratuito.\n"
             "// Scrivi il tuo nominativo in riga1, premi F6 per l'anteprima e F7 per salvare il file STL.\n"
             "// Lo stesso modello fa anche altri oggetti: si sceglie con il parametro «tipo».\n")
    return testa + s


def viti_coperte(sorgente, parametri, testo):
    """Nei modelli con viti, la parte «controllo_viti» contiene ciò che delle scritte finirebbe sotto
    la testa di una vite: deve essere vuota. Torna il messaggio d'errore o None."""
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "v.stl"
        cmd = ["openscad", "-q", "-o", str(out)]
        for k, v in {**parametri, "riga1": testo, "parte": "controllo_viti"}.items():
            cmd += ["-D", f'{k}="{v}"']
        subprocess.run(cmd + [str(sorgente)], capture_output=True)
        if out.exists() and out.stat().st_size > 0:
            return f"{parametri.get('tipo')} {testo}: la testa di una vite copre la bandiera o le scritte"
    return None


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


def disegna(m, z_base, z_rilievo, colori, destinazione, specchia=False, z_incavi=None, bandiera=None, incise=False):
    """Anteprima vista dall'alto: base colorata, rilievi del secondo colore con la loro ombra,
    oppure (z_incavi) il retro con gli incavi disegnati più scuri, perché non sono fori passanti;
    con incise=True gli incavi sono le scritte, colorate come i rilievi e con il tricolore."""
    from PIL import Image, ImageChops, ImageFilter
    bordo = 6
    (x0, y0, _), (x1, y1, _) = m.bounds
    scala = min(16, 3680 / (x1 - x0 + 2 * bordo))   # oltre 218 mm l'immagine non cresce più (gruccia: 400 mm)
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
        if incise:
            img.paste(colori["rilievo"], (0, 0), incavi)
            if bandiera:   # la bandiera è a specchio nel file: vista dal retro torna con il verde a sinistra
                from PIL import ImageDraw
                bx0, by0, bx1, by1 = bandiera
                for i, col in enumerate(TRICOLORE):
                    fascia = Image.new("L", (w, h), 0)
                    xa, xb = -bx1 + (bx1 - bx0) * i / 3, -bx1 + (bx1 - bx0) * (i + 1) / 3
                    ImageDraw.Draw(fascia).rectangle([(xa - ox) * scala, (oy - by1) * scala, (xb - ox) * scala, (oy - by0) * scala], fill=255)
                    img.paste(col, (0, 0), ImageChops.multiply(fascia, incavi))
            img.paste((20, 45, 90), (0, 0), ImageChops.subtract(incavi, ImageChops.offset(incavi, -3, -4)))
        else:
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
    if incise and bandiera:
        # Pezzo alto e stretto (cover): nel formato del catalogo, 1100 × 500, il retro intero a sinistra
        # e a destra l'ingrandimento delle scritte, dalla bandiera alle due righe sotto
        tela = Image.new("RGB", (1100, 500), "white")
        intero = img.resize((int(w * 470 / h), 470), Image.LANCZOS)
        tela.paste(intero, (20, 15))
        bx0, by0, bx1, by1 = bandiera
        scritte = img.crop((0, max(0, int((oy - (by1 + 3)) * scala)), w, min(h, int((oy - (by0 - 22)) * scala))))
        k = min((1100 - intero.width - 60) / scritte.width, 470 / scritte.height)
        scritte = scritte.resize((int(scritte.width * k), int(scritte.height * k)), Image.LANCZOS)
        tela.paste(scritte, (intero.width + 40 + (1100 - intero.width - 60 - scritte.width) // 2, (500 - scritte.height) // 2))
        tela.save(destinazione, "WEBP", quality=82, method=6)
        return
    img = img.resize((w * 3 // 4, h * 3 // 4), Image.LANCZOS)
    img.save(destinazione, "WEBP", quality=82, method=6)


def scad(sorgente, parametri, uscita):
    cmd = ["openscad", "-q", "-o", str(uscita)]
    for k, v in parametri.items():
        cmd += ["-D", f'{k}="{v}"']
    subprocess.run(cmd + [str(sorgente)], check=True)


def unisci(a, b, sottrai=False):
    """Unione booleana di due pezzi con manifold3d (con sottrai=True, differenza: scritte incise)."""
    import manifold3d as mf
    import numpy as np
    import trimesh
    def man(m):
        return mf.Manifold(mf.Mesh(vert_properties=np.asarray(m.vertices, dtype=np.float32),
                                   tri_verts=np.asarray(m.faces, dtype=np.uint32)))
    r = (man(a) - man(b) if sottrai else man(a) + man(b)).to_mesh()
    m = trimesh.Trimesh(vertices=r.vert_properties[:, :3], faces=r.tri_verts, process=True)
    # L'unione in precisione singola può lasciare schegge di volume nullo sugli spigoli
    # (nella targa da tavolo, al colmo): si tolgono, i pezzi veri restano tutti.
    pezzi = m.split(only_watertight=False)
    if len(pezzi) > 1:
        veri = [p for p in pezzi if abs(p.volume) > 1.0]
        if veri:
            m = trimesh.util.concatenate(veri)
    return m


def superficie_sospesa(m):
    """Area delle facce rivolte in basso (più di 45°) sotto le quali c'è vuoto per più di 3 mm:
    in stampa resterebbero nel vuoto e chiederebbero supporti. Non contano i primi 2 mm sul piano,
    i bordi delle lettere in rilievo e gli archi dei fori piccoli, che si stampano da soli."""
    import numpy as np
    n, c, a = m.face_normals, m.triangles_center, m.area_faces
    giu = np.where((n[:, 2] < -0.71) & (c[:, 2] > 2.0))[0]
    if not len(giu):
        return 0.0
    origini = c[giu] - [0, 0, 0.02]
    vuoto = origini[:, 2].copy()                 # senza ostacoli si arriva al piano
    dove, raggi, _ = m.ray.intersects_location(origini, np.tile([0, 0, -1.0], (len(giu), 1)), multiple_hits=True)
    for p, r in zip(dove, raggi):
        vuoto[r] = min(vuoto[r], origini[r, 2] - p[2])
    import trimesh
    sotto = giu[vuoto > 3.0]
    # gli archi dei fori tondi (viti, occhielli) e i bordi stretti (rilievi da 1 mm su una parete)
    # si stampano da soli: contano solo le zone sospese più grandi di 30 mm² e larghe più di 1,6 mm
    gruppi = trimesh.graph.connected_components(m.face_adjacency, nodes=sotto) if len(sotto) else []
    def largo(gr):
        v = m.vertices[m.faces[gr].ravel()]
        return min(np.ptp(v[:, 0]), np.ptp(v[:, 1])) > 1.6
    return float(sum(a[gr].sum() for gr in gruppi if a[gr].sum() > 30 and largo(gr)))


def compagno(cartella, insieme):
    """Secondo pezzo nella posizione di montaggio, per le anteprime. «ribalta» = spessore del pezzo quando il file
    è capovolto per la stampa (x diventa -x, z diventa ribalta - z): è una rotazione, il verso delle facce resta."""
    import trimesh
    c = trimesh.load(cartella / insieme["file"])
    if insieme.get("ribalta") is not None:
        v = c.vertices.copy()
        v[:, 0] = -v[:, 0]
        v[:, 2] = insieme["ribalta"] - v[:, 2]
        c.vertices = v
    return c


def genera(sorgente, parametri, testo, destinazione, colori=None, retro=None, base_stl=None):
    import trimesh
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d) / "pezzo.stl"
        if base_stl:
            scad(sorgente, {**parametri, "riga1": testo, "parte": "testo"}, tmp)
            m = unisci(trimesh.load(base_stl), trimesh.load(tmp), sottrai=bool(colori and colori.get("incise")))
        else:
            scad(sorgente, {**parametri, "riga1": testo}, tmp)
            m = trimesh.load(tmp)
    if colori and colori.get("fianco") is not None:
        # Stampa di fianco: il lato sinistro (x = fianco) va sul piano (z' = x - fianco, x' = -z), così
        # ganci, fessure e alette si stampano senza supporti. Le anteprime lo rimettono dritto.
        import numpy as np
        m.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2, [0, 1, 0]))
        m.apply_translation([0, 0, -m.bounds[0][2]])
    errori = []
    sospesa = superficie_sospesa(m)
    if sospesa > 60:   # nessun oggetto deve chiedere supporti (archi dei fori e bordi da 1 mm non contano)
        errori.append(f"{sospesa:.0f} mm² sospesi nel vuoto: servirebbero supporti")
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
        if colori.get("incise"):
            # scritte incise sul retro, che sta sul piano: si guarda dal retro (a specchio), con le incisioni colorate
            disegna(m, rilievo + 0.05, None, colori, destinazione.with_suffix(".webp"), specchia=True,
                    z_incavi=0.05, bandiera=colori.get("bandiera"), incise=True)
        elif not colori.get("vista_3d"):
            # «insieme»: nell'anteprima si vede l'oggetto montato; «sagoma_z»: quota a cui si legge il contorno
            # (pezzi con gli spigoli smussati: a metà spessore il contorno è quello vero)
            vista = trimesh.util.concatenate([m, compagno(destinazione.parent, colori["insieme"])]) if colori.get("insieme") else m
            disegna(vista, colori.get("sagoma_z", base - 0.1), base + 0.4, colori, destinazione.with_suffix(".webp"),
                    bandiera=colori.get("bandiera"))
        if retro:
            disegna(m, base - 0.1, None, colori, retro, specchia=True, z_incavi=0.05)
    return None


PAGINA_3D = """<!doctype html><html><body style="margin:0;background:#fff">
<script type="module">
import * as THREE from './vendor/three/three.module.min.js';
const q = new URLSearchParams(location.search), A = JSON.parse(q.get('a'));
const buf = await (await fetch(q.get('f'))).arrayBuffer(), dv = new DataView(buf), n = dv.getUint32(80, true);
let pos = new Float32Array(n * 9);
for (let i = 0; i < n; i++) for (let k = 0; k < 9; k++) pos[i * 9 + k] = dv.getFloat32(84 + i * 50 + 12 + k * 4, true);
const suo = pos.length;      // fin qui il pezzo con il nominativo; dopo, il secondo pezzo montato (insieme)
if (A.insieme) {
  const b2 = await (await fetch(q.get('f').replace(/[^/]+$/, A.insieme.file))).arrayBuffer(), d2 = new DataView(b2), n2 = d2.getUint32(80, true);
  const p2 = new Float32Array(n2 * 9);
  for (let i = 0; i < n2; i++) for (let k = 0; k < 9; k++) p2[i * 9 + k] = d2.getFloat32(84 + i * 50 + 12 + k * 4, true);
  if (typeof A.insieme.ribalta === 'number') for (let i = 0; i < p2.length; i += 3) { p2[i] = -p2[i]; p2[i + 2] = A.insieme.ribalta - p2[i + 2]; }
  const tutto = new Float32Array(suo + p2.length); tutto.set(pos); tutto.set(p2, suo); pos = tutto;
}
if (A.fianco) for (let i = 0; i < pos.length; i += 3) { const xs = pos[i]; pos[i] = pos[i + 2] + A.fianco; pos[i + 2] = -xs; }
if (A.assi) for (let i = 0; i < pos.length; i += 3) {   // oggetto girato per mostrare le scritte verso l'alto
  const p = [pos[i], pos[i + 1], pos[i + 2]];
  for (let k = 0; k < 3; k++) pos[i + k] = A.assi[k][0] * p[0] + A.assi[k][1] * p[1] + A.assi[k][2] * p[2];
}
let pc = pos;
if (A.inclina) {        // targa da tavolo: piastra con le scritte riportata in piano per colorarle
  const [g, calo, meta] = A.inclina, a = g * Math.PI / 180, ca = Math.cos(a), sa = Math.sin(a);
  pc = new Float32Array(pos.length);
  for (let i = 0; i < pos.length; i += 3) { const y = pos[i + 1], z = pos[i + 2] + calo; pc[i] = pos[i]; pc[i + 1] = y * ca + z * sa - meta; pc[i + 2] = -y * sa + z * ca; }
}
const aree = new Map();
for (let t = 0; t < pc.length; t += 9) {
  const z0 = pc[t + 2]; if (Math.abs(z0 - pc[t + 5]) > 1e-3 || Math.abs(z0 - pc[t + 8]) > 1e-3) continue;
  const nz = (pc[t + 3] - pc[t]) * (pc[t + 7] - pc[t + 1]) - (pc[t + 4] - pc[t + 1]) * (pc[t + 6] - pc[t]);
  if (nz > 0) aree.set(z0.toFixed(2), (aree.get(z0.toFixed(2)) || 0) + nz);
}
let zb = 0, best = 0; aree.forEach((v, k) => { if (v > best) { best = v; zb = parseFloat(k); } });
if (typeof A.quota_scritte === 'number') zb = A.quota_scritte;
const ril = A.rilievo_mm || 1, cb = new THREE.Color(A.base), cr = new THREE.Color(A.rilievo);
const tri = ['#009246', '#ffffff', '#ce2b37'].map(c => new THREE.Color(c)), col = new Float32Array(pos.length);
for (let t = 0; t < pos.length; t += 9) {
  const zm = Math.max(pc[t + 2], pc[t + 5], pc[t + 8]);
  let c = t < suo && zm > zb + 0.01 && zm <= zb + ril + 0.02 ? cr : cb;
  if (c === cr && A.bandiera) {
    const [x0, y0, x1, y1] = A.bandiera, cx = (pc[t] + pc[t + 3] + pc[t + 6]) / 3, cy = (pc[t + 1] + pc[t + 4] + pc[t + 7]) / 3;
    if (cx >= x0 - 0.1 && cx <= x1 + 0.1 && cy >= y0 - 0.1 && cy <= y1 + 0.1) c = tri[Math.max(0, Math.min(2, Math.floor((cx - x0) / (x1 - x0) * 3)))];   // il bordo sinistro può cadere poco prima di x0
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
// «camera» nell'anteprima: da dove si guarda e quale asse sta in alto (vassoio: di fronte e dall'alto)
const K = A.camera || {};
if (K.su) cam.up.set(K.su[0], K.su[1], K.su[2]);
cam.position.copy(new THREE.Vector3(...(K.da || [0.85, -0.2, 0.75])).normalize().multiplyScalar(d)); cam.lookAt(0, 0, 0);
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
        class Muto(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *a):
                pass
        srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Muto, directory=d))
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


def controlla_pezzo(m):
    """Le stesse regole dei file generati: niente supporti, chiuso, un pezzo, appoggiato sul piano."""
    errori = []
    sospesa = superficie_sospesa(m)
    if sospesa > 60:
        errori.append(f"{sospesa:.0f} mm² sospesi nel vuoto")
    if not m.is_watertight:
        errori.append("superficie non chiusa")
    if len(m.split(only_watertight=False)) != 1:
        errori.append("più di un pezzo")
    if abs(m.bounds[0][2]) > 1e-3:
        errori.append("non appoggia sul piano")
    return errori


def secondo_pezzo(sorgente, parametri, destinazione):
    """Pezzo uguale per tutti i nominativi (scatola, tappo): si crea, si controlla come gli altri e si salva."""
    import trimesh
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d) / "pezzo.stl"
        scad(sorgente, parametri, tmp)
        m = trimesh.load(tmp)
    errori = controlla_pezzo(m)
    if not errori:
        destinazione.parent.mkdir(parents=True, exist_ok=True)
        m.export(destinazione)
    return errori


def prova_nome(cartella):
    """Nome e cognome aggiunti nel browser (static/js/stampa3d-nome-core.js): li crea scripts/prova-stampa3d-nome.mjs
    per ALFA 100 con un nome lungo, poi qui si controlla ogni file come quelli generati."""
    import trimesh
    r = subprocess.run(["node", str(RADICE / "scripts/prova-stampa3d-nome.mjs"), str(cartella)])
    errori = [] if r.returncode == 0 else ["il codice del sito non ha creato tutti i file con il nome"]
    for f in sorted(cartella.glob("*.stl")):
        errori += [f"{f.stem}: {e}" for e in controlla_pezzo(trimesh.load(f))]
    if errori:
        print("ERRORI:\n- " + "\n- ".join(errori))
        return 1
    print(f"Nome e cognome: {len(list(cartella.glob('*.stl')))} oggetti a posto.")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tutti", action="store_true", help="rifà anche i file già presenti")
    ap.add_argument("--check", action="store_true", help="controlla solo che i file ci siano tutti")
    ap.add_argument("--prova-nome", metavar="CARTELLA",
                    help="crea con il codice del sito (node) i file con nome e cognome e li controlla")
    a = ap.parse_args()
    if a.prova_nome:
        sys.exit(prova_nome(Path(a.prova_nome)))
    dati = yaml.safe_load(DATI.read_text(encoding="utf-8"))
    nom = dati["nominativi"]
    numeri = range(nom["primo"], nom["ultimo"] + 1)
    errori, lavori, viti, secondi = [], [], [], []
    cartella_basi = tempfile.TemporaryDirectory()
    categorie = {c["id"] for c in dati.get("categorie", [])}
    for ogg in dati["oggetti"]:
        sorgente = SORGENTI / ogg["sorgente"]
        if not sorgente.exists():
            errori.append(f"manca il modello {sorgente.relative_to(RADICE)}")
            continue
        if ogg.get("categoria") not in categorie:
            errori.append(f"{ogg['id']}: categoria «{ogg.get('categoria')}» assente in «categorie»")
        modello = USCITA / ogg["id"] / f'{ogg["id"]}.scad'
        testo_modello = modello_oggetto(sorgente, ogg)
        if a.check:
            if not modello.exists() or modello.read_text(encoding="utf-8") != testo_modello:
                errori.append(f"{modello.relative_to(RADICE)} non è allineato al modello di partenza: rilancia lo script")
        else:
            modello.parent.mkdir(parents=True, exist_ok=True)
            modello.write_text(testo_modello, encoding="utf-8")
        if not a.check and "controllo_viti" in sorgente.read_text(encoding="utf-8"):
            viti += [(sorgente, ogg.get("parametri", {}), f'{nom["prefisso"]} {n}') for n in numeri]
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
        sp = ogg.get("secondo_pezzo")
        ins = (ogg.get("anteprima") or {}).get("insieme")
        if ins and (not sp or ins.get("file") != sp["file"]):
            errori.append(f"{ogg['id']}: «insieme» deve indicare il file di «secondo_pezzo»")
        if sp:
            dest2 = USCITA / ogg["id"] / sp["file"]
            if a.check:
                if not dest2.exists():
                    errori.append(f"manca {dest2.relative_to(RADICE)}")
            elif a.tutti or not dest2.exists():
                secondi.append((sorgente, {**ogg.get("parametri", {}), "parte": sp["parte"]}, dest2))
        if not a.check:
            errori += controlla_caratteri(sorgente)
    # prima i secondi pezzi: le anteprime degli oggetti montati («insieme») li leggono
    for sorgente, parametri, dest2 in secondi:
        errori += [f"{dest2.name}: {e}" for e in secondo_pezzo(sorgente, parametri, dest2)]
    if errori:
        print("ERRORI:\n- " + "\n- ".join(errori))
        sys.exit(1)
    with ProcessPoolExecutor() as ex:
        errori += [e for e in ex.map(viti_coperte, *zip(*viti)) if e] if viti else []
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
