#!/usr/bin/env python3
"""
Catalogo dei materiali per «Crea la mia lezione» (data/materiali_lezione.json).

Raccoglie i materiali GIÀ pubblicati sul sito e ne ricava, dalle loro stesse
pagine, ciò che serve per comporre una lezione: fascia d'età, durata (solo
quando il materiale la dichiara), tema, tipo. Non scrive contenuti nuovi.

Fonti:
  - schede stampabili: le card di static/formazione/schede-stampabili/index.html
    (titolo, fascia, minuti, descrizione, indirizzo);
  - storie: le card di static/formazione/storie-e-racconti/index.html
    (fascia dal titolo della sezione, minuti di lettura, temi);
  - giochi: static/giochi/{infanzia,primaria,ragazzi}/*/index.html
    (titolo e descrizione della pagina, fascia dalla cartella);
  - esperimenti: content/formazione/esperimenti.md (titoli ### con le
    fasce indicate dai pallini colorati della legenda).
Il tema si assegna per parole chiave (TEMI): una voce può averne più d'uno,
oppure nessuno, e allora non entra nelle lezioni. Un tema si aggiunge solo
quando ha materiali per più fasce: con uno solo la lezione resterebbe vuota
(il primo soccorso ne aveva uno, per la secondaria, ed è stato tolto).

Uso:
  python3 scripts/genera-materiali-lezione.py          # scrive il catalogo
  python3 scripts/genera-materiali-lezione.py --check  # esce 1 se non è aggiornato
Solo libreria standard.
"""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "materiali_lezione.json"

# tema: (etichetta, parole chiave, pagina d'introduzione sul sito)
TEMI = {
    "terremoto": ("Terremoto", ["terremot", "sism", "scoss", "amatrice", "irpinia", "friuli", "aquila",
                                "messina", "placch", "magnitud", "gelatina", "rigopiano", "san giuliano"],
                  "/rischi-prevenzione/rischio-sismico/"),
    "vulcani": ("Vulcani", ["vulcan", "eruzion", "flegre", "vesuv", "colli albani"],
                "/rischi-prevenzione/rischio-vulcanico/"),
    "acqua": ("Alluvioni, frane e maremoti", ["alluvion", "idrogeolog", "frana", "frane", "sarno", "vajont",
                                             "fium", "allagam", "piogg", "fango", "tombin", "maremot", "stava",
                                             "esondaz"],
              "/rischi-prevenzione/rischio-idrogeologico/"),
    "incendi": ("Incendi", ["incend", "fuoco", "fiamm", "fumo", "aib", "estintor", "bosco"],
                "/rischi-prevenzione/rischio-incendio/"),
    "meteo": ("Allerte meteo, temporali e vento", ["allert", "temporal", "vento", "fulmin", "bollettin",
                                                  "meteo", "neve", "grandin", "codice colore", "codici colore",
                                                  "nuvol", "tromba d"],
              "/allerte-meteo/"),
    "caldo": ("Caldo, clima e siccità", ["caldo", "clima", "siccit", "ondat", "calore"],
              "/rischi-prevenzione/ondate-di-calore/"),
    "112": ("Chiamare il 112", ["112", "chiamat", "chiamo", "numero unico", "numeri di emergenza",
                                "numeri utili", "telefonat"],
            "/numeri-utili/"),
    "casa": ("Casa sicura, kit e piano familiare", ["casa sicura", "kit", "zaino", "piano familiare",
                                                    "gas", "pentola", "blackout", "evacuaz", "uscita",
                                                    "labirint", "piano di famiglia", "domestic"],
             "/piano-familiare/"),
    "natura": ("Natura e oggetti da non toccare", ["natura che non si tocca", "cane", "animal", "oggetti sconosciuti",
                                                   "oggett", "fungh", "confezion", "siringh"],
               ""),
    "volontariato": ("Protezione civile e volontariato", ["volontar", "sistema di protezione civile", "costituzion",
                                                         "zamberletti", "coc ", "servizio nazionale",
                                                         "cittadinanza"],
                     "/conoscere/"),
    "informazione": ("Informazione, notizie e fake news", ["fake", "bufal", "notizi", "giornalis", "comunicaz",
                                                          "radio", "social"],
                     ""),
}
FASCE = ("infanzia", "primaria-bassa", "primaria-alta", "secondaria1", "secondaria2")


def testo(s: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def temi_di(*parti: str) -> list[str]:
    t = " " + " ".join(parti).lower() + " "
    return [k for k, (_, chiavi, _) in TEMI.items() if any(c in t for c in chiavi)]


def minuti_di(s: str) -> int | None:
    m = re.search(r"(\d{1,3})\s*min", s)
    return int(m.group(1)) if m else None


def fasce_scheda(f: str) -> list[str]:
    f = f.lower()
    if f.startswith("famigli"):
        return []
    if "tutte le età" in f or "età diverse" in f:
        return list(FASCE)
    out: list[str] = []
    if "infanzia" in f:
        out.append("infanzia")
    if "prim" in f:
        bassa = re.search(r"1ª|2ª|6.8 anni|5-7 anni|1ª-2ª|2ª-3ª|/ 1ª", f)
        alta = re.search(r"3ª|4ª|5ª|8.11|9.11|7.11|8-11", f)
        if bassa:
            out.append("primaria-bassa")
        if alta:
            out.append("primaria-alta")
        if not bassa and not alta:
            out += ["primaria-bassa", "primaria-alta"]
    if "secondaria i-ii" in f:
        out += ["secondaria1", "secondaria2"]
    elif "secondaria ii" in f or "quinto anno" in f:
        out.append("secondaria2")
    elif "secondaria i" in f:
        out.append("secondaria1")
    if f.startswith("infanzia / prim") or f.startswith("infanzia 5-6 / 1ª"):
        out = ["infanzia", "primaria-bassa"]
    return sorted(set(out), key=FASCE.index)


def schede() -> list[dict]:
    t = (ROOT / "static/formazione/schede-stampabili/index.html").read_text(encoding="utf-8")
    out = []
    for c in re.finditer(r'<div class="scheda-card">(.*?)</a>', t, re.S):
        b = c.group(1)
        href = re.search(r'href="([^"]+)"', b)
        titolo = re.search(r"<h3[^>]*>(.*?)</h3>", b, re.S)
        fascia = re.search(r'scheda-fascia">(.*?)</span>', b, re.S)
        if not (href and titolo and fascia) or href.group(1).startswith(("pacchetti", "http", "/")):
            continue
        meta = re.search(r'scheda-meta">(.*?)</div>', b, re.S)
        desc = re.search(r'scheda-desc">(.*?)</p>', b, re.S)
        tit, fas = testo(titolo.group(1)), testo(fascia.group(1))
        d = testo(desc.group(1)) if desc else ""
        slug = href.group(1).strip("/")
        fasce = fasce_scheda(fas)
        if not fasce:
            continue
        tipo = "valutazione" if "rubrica" in slug or "valutaz" in tit.lower() else (
            "colorare" if "colorar" in slug or "colorare" in fas.lower() else "scheda")
        out.append({
            "tipo": tipo, "titolo": tit, "url": f"/formazione/schede-stampabili/{slug}/",
            "fasce": fasce, "minuti": minuti_di(testo(meta.group(1))) if meta else None,
            "temi": temi_di(tit, d, slug.replace("-", " ")), "desc": d,
            "facilitata": "facilitat" in (tit + fas + slug).lower(),
        })
    return out


def storie() -> list[dict]:
    t = (ROOT / "static/formazione/storie-e-racconti/index.html").read_text(encoding="utf-8")
    out, fasce = [], []
    for pezzo in re.split(r"(<h2[^>]*>.*?</h2>)", t, flags=re.S):
        h = re.match(r"<h2[^>]*>(.*?)</h2>", pezzo, re.S)
        if h:
            n = testo(h.group(1)).lower()
            fasce = (["infanzia"] if "3-5" in n else ["primaria-bassa"] if "6-8" in n
                     else ["primaria-alta"] if "9-11" in n else ["secondaria1"] if "11-14" in n else [])
            continue
        for c in re.finditer(r'<a href="([^"]+)" class="storia-card">(.*?)</a>', pezzo, re.S):
            if not fasce:
                continue
            href, b = c.group(1), c.group(2)
            url = href if href.startswith("/") else f"/formazione/storie-e-racconti/{href}"
            tit = testo(re.search(r"<h3>(.*?)</h3>", b, re.S).group(1))
            sotto = re.search(r'sottotitolo">(.*?)</div>', b, re.S)
            meta = re.search(r'class="meta">(.*?)</div>', b, re.S)
            m = testo(meta.group(1)) if meta else ""
            out.append({
                "tipo": "storia", "titolo": tit, "url": url, "fasce": list(fasce),
                "minuti": minuti_di(m), "temi": temi_di(tit, testo(sotto.group(1)) if sotto else "", m),
                "desc": testo(sotto.group(1)) if sotto else "", "facilitata": False,
            })
    return out


def giochi() -> list[dict]:
    mappa = {"infanzia": ["infanzia"], "primaria": ["primaria-bassa", "primaria-alta"],
             "ragazzi": ["secondaria1", "secondaria2"]}
    out = []
    for cartella, fasce in mappa.items():
        for f in sorted((ROOT / "static/giochi" / cartella).glob("*/index.html")):
            t = f.read_text(encoding="utf-8")
            tit = re.search(r"<title>(.*?)</title>", t, re.S)
            desc = re.search(r'<meta name="description" content="([^"]*)"', t)
            if not tit:
                continue
            nome = testo(tit.group(1)).split(" — ")[0].strip()
            d = html.unescape(desc.group(1)) if desc else ""
            out.append({
                "tipo": "gioco", "titolo": nome, "url": f"/giochi/{cartella}/{f.parent.name}/",
                "fasce": fasce, "minuti": None, "temi": temi_di(nome, d, f.parent.name.replace("-", " ")),
                "desc": d, "facilitata": False,
            })
    return out


def esperimenti() -> list[dict]:
    t = (ROOT / "content/formazione/esperimenti.md").read_text(encoding="utf-8")
    out, sezione = [], ""
    for riga in t.splitlines():
        if riga.startswith("## "):
            sezione = riga[3:]
        m = re.match(r"### \d+\.\s+(.*?)\s*((?:🟢|🔵|🟠)+)\s*$", riga)
        if not m:
            continue
        fasce = []
        if "🟢" in m.group(2):
            fasce.append("infanzia")
        if "🔵" in m.group(2):
            fasce += ["primaria-bassa", "primaria-alta"]
        if "🟠" in m.group(2):
            fasce += ["secondaria1", "secondaria2"]
        out.append({
            "tipo": "esperimento", "titolo": m.group(1).strip(), "url": "/formazione/esperimenti/",
            "fasce": fasce, "minuti": None, "temi": temi_di(m.group(1), sezione), "desc": sezione,
            "facilitata": False,
        })
    return out


def main() -> int:
    voci = schede() + storie() + giochi() + esperimenti()
    for k, (_, _, intro) in TEMI.items():
        if intro:
            p = ROOT / "content" / intro.strip("/")
            if not (p.with_suffix(".md").exists() or (p / "_index.md").exists() or (p / "index.md").exists()):
                print(f"Pagina d'introduzione inesistente per il tema {k}: {intro}", file=sys.stderr)
                return 2
    dati = {
        "temi": {k: {"etichetta": v[0], "intro": v[2]} for k, v in TEMI.items()},
        "materiali": voci,
    }
    nuovo = json.dumps(dati, ensure_ascii=False, indent=1) + "\n"
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != nuovo:
            print("data/materiali_lezione.json non è aggiornato: esegui "
                  "python3 scripts/genera-materiali-lezione.py e committa il file.")
            return 1
        print("Catalogo dei materiali per le lezioni aggiornato.")
        return 0
    OUT.write_text(nuovo, encoding="utf-8")
    per_tipo: dict[str, int] = {}
    for v in voci:
        per_tipo[v["tipo"]] = per_tipo.get(v["tipo"], 0) + 1
    print(f"{OUT.relative_to(ROOT)}: {len(voci)} materiali {per_tipo}; "
          f"senza tema {sum(1 for v in voci if not v['temi'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
