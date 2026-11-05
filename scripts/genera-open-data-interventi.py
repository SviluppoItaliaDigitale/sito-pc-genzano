#!/usr/bin/env python3
"""Genera dataset OPEN DATA AGGREGATI dagli export del gestionale interventi.

Legge l'export .xlsx del gestionale (fogli: Interventi, Interventi membri,
Risposte Selettive) e produce SOLO statistiche aggregate e anonime in
static/open-data/. NON pubblica MAI dati personali o sensibili: nessun nome,
nessun richiedente, nessuna descrizione, nessun luogo/indirizzo specifico.

Il file .xlsx NON va committato (contiene nomi dei volontari): resta sul PC.
Questo script ne estrae solo i numeri.

Scrive anche data/open_data_interventi.json, i dati dei grafici interattivi
della pagina /open-data/: per giorno quanti interventi e quante ore, per mese
misure, tipologie, fasce orarie e automezzi (vedi la sezione GRAFICI sotto).

Uso:  python3 scripts/genera-open-data-interventi.py [percorso.xlsx]

Senza argomento prende automaticamente l'export PIÙ RECENTE in ~/Scrivania
(file `gcpc-genzano-di-roma_global_reports_*.xlsx`): il nome cambia a ogni
esportazione, quindi basta scaricare il nuovo file e rilanciare lo script.

L'export del gestionale è CUMULATIVO ("global report"): contiene sempre tutto
dall'adozione del sistema. Perciò NON serve scartare a mano i dati già usati:
ogni nuovo export ricontiene i vecchi + i nuovi, e questo script ricalcola e
SOVRASCRIVE i totali aggregati. I dati restano PROVVISORI (dal nuovo gestionale,
non da inizio anno). Se l'export NON è cumulativo (filtrato a un periodo),
NON usare questo script: sovrascriverebbe i totali con un sottoinsieme.
Usa invece scripts/aggiorna-open-data-delta.py, che aggiunge ai dataset
pubblicati le sole righe nuove dell'export parziale.
"""
import csv
import glob
import json
import re
import sys
import os
import datetime

try:
    import openpyxl
except ImportError:
    sys.exit("Serve openpyxl:  pip install --break-system-packages openpyxl")

GLOB = os.path.expanduser("~/Scrivania/gcpc-genzano-di-roma_global_reports_*.xlsx")
OUT = "static/open-data"

# Etichette con refuso nel menu del gestionale: si pubblica la forma corretta
# (il dato non cambia, cambia solo la grafia). Usata anche dal delta
# (aggiorna-open-data-delta.py). Da correggere anche alla fonte, nel
# vocabolario del gestionale, appena possibile.
TIPOLOGIE_NORMALIZZATE = {"Allagamaneto": "Allagamento"}


def trova_export():
    """Ritorna l'export più recente che corrisponde al pattern, o None."""
    cand = glob.glob(GLOB)
    return max(cand, key=os.path.getmtime) if cand else None

MESI = {"gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4, "maggio": 5,
        "giugno": 6, "luglio": 7, "agosto": 8, "settembre": 9, "ottobre": 10,
        "novembre": 11, "dicembre": 12}
MESI_NOME = {v: k for k, v in MESI.items()}

NOTA = ("Dati PROVVISORI: censiti solo dall'adozione del nuovo gestionale, "
        "non coprono l'intero anno (mancano i mesi precedenti). Aggregati e "
        "anonimi, senza dati personali.")

# un automezzo nel campo Veicoli: "M04 Evo [Pickup] (TARGA)". Più mezzi sono
# concatenati nella stessa cella. La targa serve SOLO a deduplicare e NON si
# pubblica mai (la policy privacy del sito esclude le targhe). Etichetta = sigla
# + nome + tipo, es. "M04 Evo (Pickup)".
RE_VEICOLO = re.compile(r'(.+?)\s*\[([^\]]+)\]\s*\(([A-Z0-9]+)\)')


def automezzi(cella):
    """Da una cella Veicoli ritorna lista di (etichetta_senza_targa, targa)."""
    out = []
    for nome, tipo, targa in RE_VEICOLO.findall(str(cella or "")):
        nome = nome.strip()
        if nome:
            out.append((f"{nome} ({tipo.strip()})", targa))
    return out


# Date sbagliate nel gestionale che il Gruppo non può correggere alla fonte.
# Valgono per ogni export, cumulativo o parziale (le applica anche
# aggiorna-open-data-delta.py). Numero intervento -> data vera, con il motivo.
CORREZIONI_DATE = {
    # Memorial Giordano Funari, piazza Frasconi: sabato 24 ottobre 2026
    # (confermato da Alessandro il 25 e il 28/10/2026); il rapporto è datato 25.
    "217/2026": "sabato 24 ottobre 2026",
}


def applica_correzioni(righe, idx):
    """Sostituisce Data Inizio e Data Fine dei rapporti in CORREZIONI_DATE."""
    i_num, campi = idx.get("Numero"), [idx[c] for c in ("Data Inizio", "Data Fine") if c in idx]
    out = []
    for r in righe:
        nuova = CORREZIONI_DATE.get(str(r[i_num]).strip()) if i_num is not None else None
        if nuova:
            r = list(r)
            for i in campi:
                if i < len(r):
                    r[i] = nuova
            r = tuple(r)
        out.append(r)
    return out


def parse_data_it(s):
    if not s:
        return None
    s = str(s).lower()
    m = re.search(r'(\d{1,2})\s+([a-zà]+)\s+(\d{4})', s)
    if not m:
        return None
    g, mese, a = int(m.group(1)), MESI.get(m.group(2)), int(m.group(3))
    if not mese:
        return None
    try:
        return datetime.date(a, mese, g)
    except ValueError:
        return None


def minuti(s):
    if s is None:
        return 0
    tot = 0
    for n, u in re.findall(r'(\d+)\s*(or[ae]|min\w*)', str(s).lower()):
        tot += int(n) * (60 if u.startswith("or") else 1)
    return tot


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def fnum(x):
    v = num(x)
    return v if v is not None else 0


def chiave_numero(n):
    """'130/2026' -> (2026, 130) per confronti; None se non parsabile."""
    m = re.match(r"\s*(\d+)\s*/\s*(\d{4})", str(n or ""))
    return (int(m.group(2)), int(m.group(1))) if m else None


def ultimo_numero(righe, col):
    """Numero di intervento più alto presente nelle righe (es. '130/2026')."""
    nums = [(chiave_numero(col(r, "Numero")), col(r, "Numero")) for r in righe]
    nums = [x for x in nums if x[0]]
    return max(nums)[1].strip() if nums else None


def write_kv(nome, indicatori, periodo):
    """Scrive un dataset chiave/valore in CSV + JSON."""
    csv_path = os.path.join(OUT, nome + ".csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as fp:
        w = csv.writer(fp)
        w.writerow(["indicatore", "valore"])
        for k, v in indicatori:
            w.writerow([k, v])
    json_path = os.path.join(OUT, nome + ".json")
    with open(json_path, "w", encoding="utf-8") as fp:
        json.dump({
            "dataset": nome,
            "fonte": "Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma",
            "licenza": "CC BY 4.0",
            "periodo": periodo,
            "nota": NOTA,
            "generato_il": datetime.date.today().isoformat(),
            "dati": {k: v for k, v in indicatori},
        }, fp, ensure_ascii=False, indent=2)
    print(f"  scritto {csv_path} + .json")


def write_rows(nome, header, rows, periodo):
    csv_path = os.path.join(OUT, nome + ".csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as fp:
        w = csv.writer(fp)
        w.writerow(header)
        w.writerows(rows)
    json_path = os.path.join(OUT, nome + ".json")
    with open(json_path, "w", encoding="utf-8") as fp:
        json.dump({
            "dataset": nome,
            "fonte": "Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma",
            "licenza": "CC BY 4.0",
            "periodo": periodo,
            "nota": NOTA,
            "generato_il": datetime.date.today().isoformat(),
            "dati": [dict(zip(header, r)) for r in rows],
        }, fp, ensure_ascii=False, indent=2)
    print(f"  scritto {csv_path} + .json")


# ---------- GRAFICI INTERATTIVI di /open-data/ (15/10/2026) ----------
# Lo shortcode grafico-interattivo della pagina degli open data legge
# data/open_data_interventi.json. Solo aggregati, al livello che la pagina
# dichiara: per GIORNO soltanto quanti interventi e quante ore; tipologie,
# fasce orarie di partenza e automezzi solo per MESE. Un giorno con un solo
# intervento, accanto alla sua tipologia, racconterebbe quel singolo evento, e
# alcune tipologie riguardano persone (es. "Ricerca persona"): per questo le
# tipologie non scendono sotto il mese. Nessun elenco dei singoli interventi.
# Lo scrivono questo script (export cumulativo) e aggiorna-open-data-delta.py
# (export parziale, per somma), con le stesse funzioni.
# Gli articoli che raccontano le giornate stanno in data/racconti_interventi.json,
# curato a mano (giorno -> pagine): il file dei grafici vi rimanda per nome,
# così aggiungere un racconto non richiede di rigenerare i dati.
DATI_GRAFICI = "data/open_data_interventi.json"
RACCONTI = "racconti_interventi"          # data/racconti_interventi.json
FASCE = ["Prima delle 12", "12–14", "14–16", "16–18", "18–20", "Dopo le 20"]


def fascia_oraria(ora):
    m = re.match(r"\s*(\d{1,2})[:.](\d{2})", str(ora or ""))
    if not m:
        return None
    t = int(m.group(1)) * 60 + int(m.group(2))
    for limite, nome in zip((12, 14, 16, 18, 20), FASCE):
        if t < limite * 60:
            return nome
    return FASCE[-1]


def tipologia(r, col):
    """Tipologia pubblicata: menu del gestionale, altrimenti il Motivo."""
    t = str(col(r, "Tipologia evento") or "").strip()
    if t in ("", "-", "None"):
        t = " ".join(str(col(r, "Motivo") or "").split())
    t = TIPOLOGIE_NORMALIZZATE.get(t, t)
    return t or "Non classificato"


def record_grafico(r, col):
    """Riassunto anonimo di un intervento, usato SOLO per sommare: non si scrive."""
    mezzi = []
    for etichetta, _targa in automezzi(col(r, "Veicoli")):
        if etichetta not in mezzi:
            mezzi.append(etichetta)
    persone = [n for n in str(col(r, "Utenti") or "").split("|") if n.strip()]
    return {"d": parse_data_it(col(r, "Data Inizio")), "fascia": fascia_oraria(col(r, "Ora Inizio")),
            "min": minuti(col(r, "Durata")), "persone": len(persone), "mezzi": mezzi,
            "tipo": tipologia(r, col)}


def grafici_vuoti():
    return {"giorni": {}, "mesi": {}, "per_mese": {"tipologie": {}, "orari": {}, "mezzi": {}}}


def grafici_da_file():
    """Aggregati del file già pubblicato, per sommarci un export parziale.
    Ore (al decimo) e ore di servizio (all'unità) sono arrotondate nel file:
    sommando il delta si eredita quell'incertezza, che si azzera al primo
    export cumulativo (come per i totali di statistiche-interventi)."""
    with open(DATI_GRAFICI, encoding="utf-8") as fp:
        g = json.load(fp)
    agg = grafici_vuoti()
    for x in g["giorni"]:
        if x["n"]:
            agg["giorni"][x["d"]] = {"n": x["n"], "ore": x["ore"]}
    s = g["serie"]
    misure = s["mesi"]["misure"]
    for i, k in enumerate(s["mesi"]["chiavi"]):
        agg["mesi"][k] = {"n": misure[0]["valori"][i], "ore": misure[1]["valori"][i], "serv": misure[2]["valori"][i]}
    for nome in ("tipologie", "orari", "mezzi"):
        for k, valori in s[nome]["per_mese"].items():
            agg["per_mese"][nome][k] = {e: v for e, v in zip(s[nome]["etichette"], valori) if v}
    return agg


def aggiungi_grafico(agg, rec):
    iso = rec["d"].isoformat()
    mese = iso[:7]
    g = agg["giorni"].setdefault(iso, {"n": 0, "ore": 0.0})
    g["n"] += 1
    g["ore"] += rec["min"] / 60
    m = agg["mesi"].setdefault(mese, {"n": 0, "ore": 0.0, "serv": 0.0})
    m["n"] += 1
    m["ore"] += rec["min"] / 60
    m["serv"] += rec["min"] * rec["persone"] / 60
    pm = agg["per_mese"]
    voci = {"tipologie": [rec["tipo"]], "orari": [rec["fascia"]] if rec["fascia"] else [], "mezzi": rec["mezzi"]}
    for nome, etichette in voci.items():
        cont = pm[nome].setdefault(mese, {})
        for e in etichette:
            cont[e] = cont.get(e, 0) + 1


def racconti_mancanti(giorni):
    """Giornate con interventi senza un racconto in data/racconti_interventi.json.
    Serve a chi aggiorna i dati: dopo gli articoli sulle giornate nuove si
    aggiunge lì la riga giorno -> pagina (il grafico la mostra al build)."""
    try:
        with open(os.path.join("data", RACCONTI + ".json"), encoding="utf-8") as fp:
            racc = json.load(fp)
    except (OSError, ValueError):
        racc = {}
    attivi = [x["d"] for x in giorni if x["n"]]
    senza = [d for d in attivi if d not in racc]
    print(f"  racconti: {len(attivi) - len(senza)} giornate su {len(attivi)} hanno un articolo "
          f"in data/{RACCONTI}.json")
    if senza:
        print("  giornate senza racconto (aggiungerlo se un articolo le racconta): " + ", ".join(senza))


def controlla_grafici(g, n_tot, tip, mez, ore=None):
    """Confronta i grafici costruiti con i totali dei dataset e restituisce i
    problemi trovati (lista vuota se tornano). Si chiama PRIMA di scrivere
    qualunque file: se qualcosa non torna, nessun dataset viene toccato."""
    s = g["serie"]
    problemi = []
    giorni = sum(x["n"] for x in g["giorni"])
    if giorni != n_tot:
        problemi.append(f"interventi nel calendario {giorni}, nel dataset {n_tot}")
    mesi = sum(s["mesi"]["misure"][0]["valori"])
    if mesi != n_tot:
        problemi.append(f"interventi nei mesi {mesi}, nel dataset {n_tot}")
    if dict(zip(s["tipologie"]["etichette"], s["tipologie"]["misure"][0]["valori"])) != dict(tip):
        problemi.append("tipologie diverse dal dataset")
    if dict(zip(s["mezzi"]["etichette"], s["mezzi"]["misure"][0]["valori"])) != dict(mez):
        problemi.append("automezzi diversi dal dataset")
    if ore is not None:
        ore_mesi = round(sum(s["mesi"]["misure"][1]["valori"]), 1)
        if abs(ore_mesi - ore) >= 0.5:
            problemi.append(f"ore nei mesi {ore_mesi}, nel dataset {ore}")
    return problemi


def senza_data(righe, col):
    """Numeri degli interventi con la data di inizio non leggibile."""
    return [str(col(r, "Numero")) for r in righe if not parse_data_it(col(r, "Data Inizio"))]


def scrivi_grafici(out):
    """Scrive il file dei grafici già costruito e controllato."""
    with open(DATI_GRAFICI, "w", encoding="utf-8") as fp:
        json.dump(out, fp, ensure_ascii=False, indent=1)
        fp.write("\n")
    print(f"  scritto {DATI_GRAFICI} (grafici di /open-data/, solo aggregati)")
    racconti_mancanti(out["giorni"])


def costruisci_grafici(agg, periodo):
    """Dati dei grafici in memoria (nessun file scritto)."""
    dal = datetime.date.fromisoformat(periodo["dal"])
    al = datetime.date.fromisoformat(periodo["al"])
    giorni, d = [], dal
    while d <= al:
        x = agg["giorni"].get(d.isoformat(), {"n": 0, "ore": 0.0})
        giorni.append({"d": d.isoformat(), "n": x["n"], "ore": round(x["ore"], 1)})
        d += datetime.timedelta(days=1)
    chiavi, m = [], datetime.date(dal.year, dal.month, 1)
    while m <= al:
        chiavi.append(m.strftime("%Y-%m"))
        m = datetime.date(m.year + (m.month == 12), m.month % 12 + 1, 1)
    etichette = []
    for k in chiavi:
        a, mm = map(int, k.split("-"))
        nome = MESI_NOME[mm].capitalize()
        fine_mese = (datetime.date(a + (mm == 12), mm % 12 + 1, 1) - datetime.timedelta(days=1)).day
        dal_qui = k == chiavi[0] and dal.day > 1
        al_qui = k == chiavi[-1] and al.day < fine_mese
        if dal_qui and al_qui:
            nome += f" (dal {dal.day} al {al.day})"
        elif dal_qui:
            nome += f" (dal {dal.day})"
        elif al_qui:
            nome += f" (fino al {al.day})"
        etichette.append(nome)
    vuoto = {"n": 0, "ore": 0.0, "serv": 0.0}

    def misura(nome, unita, unita1, valori):
        return {"nome": nome, "unita": unita, "unita1": unita1, "valori": valori}

    def serie_per_mese(nome, ordine=None):
        pm = agg["per_mese"][nome]
        tot = {}
        for k in chiavi:
            for e, n in pm.get(k, {}).items():
                tot[e] = tot.get(e, 0) + n
        voci = ordine or sorted(tot, key=lambda e: (-tot[e], e))
        return {"etichette": voci,
                "misure": [misura("Interventi", "interventi", "intervento", [tot.get(e, 0) for e in voci])],
                "per_mese": {k: [pm.get(k, {}).get(e, 0) for e in voci] for k in chiavi}}

    out = {
        "titolo": "Interventi del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma",
        "fonte": "Registro interventi del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma, dati aggregati e anonimi",
        "aggiornato": periodo["al"],
        "testi": {"tutto": "tutto il periodo", "rivivi": "Rivivi l'attività del Gruppo giorno per giorno"},
        "giorni": giorni,
        "serie": {
            "mesi": {"etichette": etichette, "chiavi": chiavi, "misure": [
                misura("Interventi", "interventi", "intervento", [agg["mesi"].get(k, vuoto)["n"] for k in chiavi]),
                misura("Ore di intervento", "ore", "ora", [round(agg["mesi"].get(k, vuoto)["ore"], 1) for k in chiavi]),
                misura("Ore di servizio dei volontari", "ore", "ora", [round(agg["mesi"].get(k, vuoto)["serv"]) for k in chiavi]),
            ]},
            "tipologie": serie_per_mese("tipologie"),
            "orari": serie_per_mese("orari", FASCE),
            "mezzi": serie_per_mese("mezzi"),
        },
        # rimando al file curato a mano: lo shortcode lo legge al build
        "racconti": RACCONTI,
    }
    return out


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else trova_export()
    if not src or not os.path.exists(src):
        sys.exit("Export non trovato. Passa il percorso del .xlsx come argomento, "
                 "oppure mettilo in ~/Scrivania col nome gcpc-...global_reports_*.xlsx")
    print(f"Export: {os.path.basename(src)}")
    os.makedirs(OUT, exist_ok=True)
    wb = openpyxl.load_workbook(src, read_only=True, data_only=True)

    # ---------- INTERVENTI ----------
    ws = wb["Interventi"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = rows[0]
    idx = {h: i for i, h in enumerate(hdr) if h}

    def col(r, name):
        i = idx.get(name)
        return r[i] if i is not None and i < len(r) else None

    data = [r for r in rows[1:] if col(r, "Numero") not in (None, "")]
    data = applica_correzioni(data, idx)
    n_tot = len(data)
    min_tot = sum(minuti(col(r, "Durata")) for r in data)
    ore = round(min_tot / 60, 1)
    # Un intervento con PIÙ mezzi ha più letture del contachilometri nella
    # stessa cella, separate da spazi (es. "227412  13161"). float() su quella
    # cella fallirebbe e scarterebbe i km dell'intervento: vanno estratti tutti
    # i numeri e accoppiati per posizione iniziali[i] -> finali[i].
    def km_letture(x):
        return [float(t) for t in re.findall(r"\d+(?:[.,]\d+)?",
                                             str(x or "").replace(",", "."))]

    km = 0
    for r in data:
        ini = km_letture(col(r, "Km iniziali"))
        fin = km_letture(col(r, "Km finali"))
        for a, b in zip(ini, fin):
            if b >= a:
                km += b - a
    date = [parse_data_it(col(r, "Data Inizio")) for r in data]
    date = [d for d in date if d]
    periodo = {"dal": min(date).isoformat() if date else None,
               "al": max(date).isoformat() if date else None,
               # ultimo numero di intervento incluso: serve a
               # aggiorna-open-data-delta.py per riconoscere le righe nuove
               # di un export parziale, anche se cadono nello stesso giorno.
               "ultimo_numero": ultimo_numero(data, col)}
    per_label = ""
    if date:
        d0, d1 = min(date), max(date)
        per_label = (f"dal {d0.day} {MESI_NOME[d0.month]} {d0.year} "
                     f"al {d1.day} {MESI_NOME[d1.month]} {d1.year}")

    # tipologie: si usa "Tipologia evento" (vocabolario controllato a menu) dove
    # compilato; dove è vuoto ("-") si ripiega sul "Motivo", che gli operatori
    # compilano sempre. NB: "Motivo" è un campo più libero del menu: va tenuto
    # generico e senza dati personali nel gestionale (qui sono tutte categorie
    # operative: "Taglio pianta", "Incendio sterpaglie", ...).
    from collections import Counter
    tip = Counter(tipologia(r, col) for r in data)

    # automezzi impiegati (dedup per targa entro la cella; targa MAI pubblicata)
    veic_interventi = Counter()   # etichetta -> n. interventi in cui è usato
    targhe_distinte = set()
    interventi_con_mezzo = 0
    for r in data:
        mezzi = automezzi(col(r, "Veicoli"))
        if not mezzi:
            continue
        interventi_con_mezzo += 1
        visti = set()
        for etichetta, targa in mezzi:
            targhe_distinte.add(targa)
            if etichetta not in visti:        # un mezzo conta 1 volta per intervento
                visti.add(etichetta)
                veic_interventi[etichetta] += 1

    # ---------- MEMBRI (solo aggregato, niente nomi) ----------
    ws2 = wb["Interventi membri"]
    d2 = [r for r in ws2.iter_rows(values_only=True)][1:]
    d2 = [r for r in d2 if r and r[0]]
    vol_elenco = len(d2)
    vol_attivi = sum(1 for r in d2 if fnum(r[1]) > 0)
    rap_tot = int(sum(fnum(r[1]) for r in d2))
    # "Volontari in organico" rimosso dall'output: il foglio "Interventi membri"
    # elenca i membri presenti nell'export del gestionale, non è la consistenza
    # ufficiale dell'organico. Si pubblicano solo gli aggregati legati agli
    # interventi effettivi.
    # ---------- GRAFICI di /open-data/ (solo aggregati) ----------
    # Si costruiscono e si controllano PRIMA di scrivere qualunque file: se una
    # data non si legge o i conti non tornano, i dataset pubblicati restano com'erano.
    illeggibili = senza_data(data, col)
    if illeggibili:
        sys.exit("Data di inizio non leggibile negli interventi " + ", ".join(illeggibili)
                 + ": correggi il registro e riesporta. Nessun file scritto.")
    agg = grafici_vuoti()
    for r in data:
        aggiungi_grafico(agg, record_grafico(r, col))
    g = costruisci_grafici(agg, periodo)
    problemi = controlla_grafici(g, n_tot, tip, veic_interventi, ore)
    if problemi:
        sys.exit("Grafici non coerenti con i dataset (" + "; ".join(problemi) + "). Nessun file scritto.")

    # ---------- scrittura: dataset di static/open-data/ e grafici ----------
    write_kv("statistiche-interventi", [
        ("Periodo (provvisorio)", per_label or "n.d."),
        ("Interventi registrati", n_tot),
        ("Interventi con automezzo", interventi_con_mezzo),
        ("Automezzi impiegati (distinti)", len(targhe_distinte)),
        ("Ore di intervento totali", ore),
        ("Chilometri percorsi totali", int(km)),
    ], periodo)

    write_rows("interventi-per-tipologia",
               ["tipologia", "numero_interventi"],
               sorted(([k, v] for k, v in tip.items()), key=lambda x: -x[1]),
               periodo)

    write_rows("automezzi-impiegati",
               ["automezzo", "interventi"],
               sorted(([k, v] for k, v in veic_interventi.items()), key=lambda x: -x[1]),
               periodo)

    write_kv("statistiche-volontari", [
        ("Volontari con almeno un intervento", vol_attivi),
        ("Presenze dei volontari agli interventi", rap_tot),
    ], periodo)

    scrivi_grafici(g)

    print("\nRiepilogo (anonimo):")
    print(f"  interventi: {n_tot}, ore {ore}, km {int(km)}, {per_label}")
    print(f"  volontari: {vol_elenco} in organico, {vol_attivi} attivi, {rap_tot} rapporti")
    print("\nNessun dato personale scritto. Il file .xlsx NON va committato.")


if __name__ == "__main__":
    main()
