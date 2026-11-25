#!/usr/bin/env python3
"""Documenti unici europei del catalogo dei disciplinari (/cucina-emergenza/disciplinari/).

Il documento unico è la sintesi ufficiale del disciplinare di un prodotto DOP o IGP (regolamento (UE)
2024/1143, articolo 50): nome, descrizione del prodotto, zona, legame con il territorio. Lo pubblica la
Gazzetta ufficiale dell'Unione europea. Fino al 2008-2009 al suo posto c'era la «scheda riepilogativa».

Per ogni prodotto DOP e IGP di data/disciplinari.json questo script:
  1. trova la voce del prodotto nel registro europeo eAmbrosia, per nome (l'elenco intero si legge con una
     richiesta sola), e ne prende il numero di fascicolo. Non ci si fida del numero scritto nell'elenco del
     Ministero: in quello del 15/10/2026 diciotto righe hanno il numero di un prodotto vicino;
  2. legge dalla scheda del registro le pubblicazioni in Gazzetta della registrazione e delle modifiche
     approvate (non le temporanee);
  3. dalla più recente, chiede all'archivio dell'Ufficio delle pubblicazioni dell'UE il PDF in italiano e ne
     legge il testo: vale la prima che contiene «DOCUMENTO UNICO» seguito, entro poche righe, dalla
     denominazione del prodotto fra virgolette (intera, parola per parola: «Bra» non è «fibra») o dal suo
     numero di fascicolo; se nessuna lo contiene, la prima con «SCHEDA RIEPILOGATIVA» riconosciuta allo
     stesso modo. Se una pubblicazione citata non si lascia interpretare, o ha il titolo e il nome ma non in
     quella forma, il prodotto resta com'era e lo script lo scrive fra le cose da guardare a mano;
  4. scrive nella voce `sintesi` (tipo, indirizzo del PDF su EUR-Lex, data della Gazzetta, pagine, peso),
     `registro_ue` (impronta delle pubblicazioni in Gazzetta che l'elenco del registro cita per il prodotto:
     quando ne esce una nuova l'impronta cambia, e il controllo mensile se ne accorge; non si usa la data
     più recente perché nell'elenco qualche pubblicazione è scritta senza data) e il `fascicolo` del registro;
  5. chiede all'archivio quali rettifiche correggono l'atto che contiene la sintesi (relazione «corregge»
     dell'archivio, non il numero CELEX: una rettifica può portare il numero di un altro avviso dello stesso
     giorno) e scrive in `sintesi.rettifiche` quelle che hanno il testo in italiano e citano l'atto; le altre
     (senza testo italiano, o che non lo citano) restano annotate in `sintesi.rettifiche_altre`, così il
     controllo mensile non le segnala ogni volta. Il registro non cita sempre le rettifiche: per questo si
     chiedono per tutti i prodotti a ogni esecuzione, con una richiesta ogni quaranta atti.

Uso:
  python3 scripts/aggiorna-documenti-unici.py           i prodotti per cui il registro cita pubblicazioni
                                                         diverse da quelle viste, e quelli mai letti
  python3 scripts/aggiorna-documenti-unici.py --tutti   rilegge ogni prodotto
  python3 scripts/aggiorna-documenti-unici.py --nome "Pecorino Romano"   un prodotto (ripetibile)
  python3 scripts/aggiorna-documenti-unici.py --prova   non scrive: dice che cosa cambierebbe
  python3 scripts/aggiorna-documenti-unici.py --riscrivi   senza rete: riscrive il file dei dati nel suo
                                                         formato (un elemento per riga), dopo una modifica a mano
  --cartella DIR   dove tenere ciò che si scarica, per non richiederlo due volte: i testi degli atti
                   restano, l'elenco e le schede del registro si riusano solo se hanno meno di 12 ore

Richieste una per volta, con una pausa e con l'identità dichiarata del controllo. Servono pdftotext e
pdfinfo (pacchetto poppler-utils). I PDF scaricati sono dati non fidati: si leggono solo con quei due
programmi e non restano sul disco. EUR-Lex non si interroga: alle richieste di un programma risponde 202
senza contenuto. L'indirizzo che si pubblica si costruisce dal numero CELEX, e il documento si verifica
nell'archivio dell'Ufficio delle pubblicazioni, che di EUR-Lex è la fonte.

Un errore di lettura non cambia i dati: il prodotto per cui una fonte non ha risposto resta com'era, e il
file si scrive solo alla fine, tutto insieme. E ciò che il sito già mostra non arretra da solo: se la ricerca
di oggi darebbe nessuna sintesi, o una più vecchia, al posto di quella pubblicata, oppure toglierebbe una
rettifica collegata, il prodotto resta com'era e lo script lo scrive fra le cose da guardare (l'archivio può
aver risposto a metà). Chi ha guardato e vuole accettare la risposta di oggi lancia lo script per quel
prodotto, con --nome. Dopo: python3 scripts/check-cucina-emergenza.py --public public (dopo la build) e, con
la rete, python3 scripts/check-cucina-emergenza.py --rete.
Uscita 0; 1 se una fonte non si è fatta leggere; 2 se gli argomenti sono sbagliati; 3 se resta qualcosa da
guardare a mano (una pubblicazione che lo script non sa interpretare o di cui l'archivio non ha ancora il
testo italiano, una sintesi o una rettifica che arretrerebbe, un prodotto che nel registro non ha più una
voce sola con quel nome).
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
FILE_CATALOGO = RADICE / "data" / "disciplinari.json"
AGENTE = "Mozilla/5.0 (compatible; PCGenzanoLinkChecker/1.0; +https://www.protezionecivilegenzano.it/)"
REGISTRO = "https://webgate.ec.europa.eu/eambrosia-api/api/v1/geographical-indications"
SCHEDA = "https://webgate.ec.europa.eu/eambrosia-api/api/geographical-indications/{}"
SPARQL = "https://publications.europa.eu/webapi/rdf/sparql"
EURLEX_PDF = "https://eur-lex.europa.eu/legal-content/IT/TXT/PDF/?uri=CELEX:{}"
PAUSA = 0.5           # secondi fra due richieste
TEMPO_MASSIMO = 120   # secondi per una risposta
TITOLI = ((r"DOCUMENTO\s+UNICO", "unico"), (r"SCHEDA\s+RIEPILOGATIVA", "scheda"))
FINESTRA = 500        # caratteri dopo il titolo in cui devono comparire la denominazione o il numero del prodotto
ORE_REGISTRO = 12     # ore oltre le quali l'elenco e le schede del registro tenuti in --cartella si richiedono
A_GRUPPI_DI = 40      # atti per ogni domanda all'archivio dell'UE (l'indirizzo della richiesta resta corto)
AVVISI_AL_GIORNO = 40     # numeri d'ordine che si provano per gli avvisi della serie C usciti in un giorno
MASSIMO_PDF = 60 * 1024 * 1024  # byte: oltre non è un atto della Gazzetta (il più pesante visto è di circa 17 MB)
ARCHIVIO_FILE = "https://publications.europa.eu/"  # i PDF si scaricano solo dall'archivio
GIORNI_RECENTI = 60   # un atto o una rettifica più giovani, senza testo italiano in archivio, si riprovano
# Denominazione fra virgolette e numero di riferimento stampati sotto il titolo della sintesi: «PDO-IT-0002-AM03»
# (dal 2012 circa) o «IT-PDO-0117-0002» (prima: il primo numero è il tipo di domanda, il secondo il fascicolo).
VIRGOLETTE = re.compile(r"[«“\"]\s*([^»”\"]{2,120}?)\s*[»”\"]")
RIFERIMENTO = re.compile(r"\b(PDO|PGI|DOP|IGP)[-/ ]IT[-/ ](\d{4,5})\b|\bIT[-/ ](PDO|PGI|DOP|IGP)[-/ ]\d{4}[-/ ](\d{4,5})\b")
SIGLE = {"DOP": "PDO", "IGP": "PGI"}
# Un numero CELEX entra fra virgolette in una domanda all'archivio: cifre, maiuscole, parentesi e, per gli atti
# della serie C fino al 1999 («C1998/405/05»), la barra. Nient'altro.
CELEX_VALIDO = re.compile(r"[0-9A-Z()/]+")
# Il sito collega solo atti con il numero CELEX nella forma corrente («52016XC1126(01)»): è quella che il
# controllo dei dati accetta e per cui l'indirizzo del PDF su EUR-Lex è stato verificato.
CELEX_COLLEGABILE = re.compile(r"[0-9A-Z()]+")
RETTIFICA = re.compile(r"R\(\d+\)$")   # il numero CELEX di una rettifica finisce con «R(01)»
AVVISO_SERIE_C = re.compile(r"5\d{4}XC[0-9()]+")
CDM = "PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> "
STRINGA = "^^<http://www.w3.org/2001/XMLSchema#string>"

non_letti = []        # fonti che non si sono fatte leggere


# ───────────────────────── testi, nomi, date ─────────────────────────

def compatto(testo):
    """Solo lettere e cifre, senza accenti: «Terra d’Otranto» e «TERRA D'OTRANTO» diventano uguali."""
    ascii_ = unicodedata.normalize("NFKD", testo or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "", ascii_)


def parti_del_nome(nome):
    """Forme con cui un prodotto può essere scritto: «A / B», «A o B» e «A, B» valgono anche da sole."""
    pezzi = [nome] + re.split(r"\s*/\s*|\s+o\s+|,\s*", nome)
    pezzi += [p.replace("S. ", "San ") for p in pezzi]
    return {compatto(p) for p in pezzi if len(compatto(p)) >= 3}


def parole(testo):
    """Minuscole, senza accenti, una parola dopo l'altra: «TERRA D’OTRANTO» e «Terra d'Otranto» → «terra d otranto»."""
    piano = (testo or "").replace("’", "'").replace("‘", "'").replace("ʼ", "'")
    ascii_ = unicodedata.normalize("NFKD", piano).encode("ascii", "ignore").decode().lower()
    return " ".join(re.sub(r"[^a-z0-9]+", " ", ascii_).split())


def denominazioni(nomi):
    """Le denominazioni intere con cui la Gazzetta può scrivere il prodotto: ogni nome e le sue alternative
    («A / B», «A o B»), parola per parola. A differenza di parti_del_nome, qui un pezzo di nome non basta:
    «Bra» non deve valere per «fibra» né «Toscano» per «Prosciutto Toscano»."""
    forme = set()
    for nome in nomi:
        for pezzo in [nome or ""] + re.split(r"\s*/\s*|\s+o\s+", nome or ""):
            for variante in (pezzo, pezzo.replace("S. ", "San ")):
                if parole(variante):
                    forme.add(parole(variante))
    return forme


def ha_il_fascicolo(testo, fascicolo):
    """Vero se fra i numeri di riferimento scritti nel testo c'è il fascicolo del prodotto. Non vale il
    contrario: un atto di modifica può portare il numero della domanda di modifica al posto del fascicolo."""
    m = re.fullmatch(r"(PDO|PGI)-IT-0*(\d+)", fascicolo or "")
    if not m:
        return False
    cercato = (m.group(1), int(m.group(2)))
    for trovato in RIFERIMENTO.finditer(testo):
        sigla, numero = (trovato.group(1), trovato.group(2)) if trovato.group(1) else (trovato.group(3), trovato.group(4))
        if (SIGLE.get(sigla, sigla), int(numero)) == cercato:
            return True
    return False


def fascicolo_normale(numero):
    """«PGI-IT-01038» e «PGI-IT-1038» sono lo stesso fascicolo."""
    m = re.fullmatch(r"(PDO|PGI|TSG)-IT-0*(\d+)", numero or "")
    return f"{m.group(1)}-IT-{int(m.group(2))}" if m else (numero or "")


def data_dal_testo(testo):
    """Data di una pubblicazione scritta dal registro come «Official Journal C 186, 10.06.2017»."""
    m = re.search(r"(\d{1,2})\.(\d{1,2})\.(\d{2,4})", testo or "")
    if not m:
        return ""
    anno = int(m.group(3))
    anno += 2000 if anno < 50 else 1900 if anno < 100 else 0
    return f"{anno:04d}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"


def data_del_registro(valore):
    """Le schede del registro scrivono le date come GG-MM-AAAA."""
    m = re.fullmatch(r"(\d{2})-(\d{2})-(\d{4})", (valore or "").strip())
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else ""


def ultima_pubblicazione(voce_del_registro):
    """Data più recente fra le pubblicazioni in Gazzetta che l'elenco del registro cita per un prodotto, fra
    quelle scritte con la data: serve ai messaggi, non a decidere se qualcosa è cambiato."""
    date = [data_dal_testo(p.get("text")) for p in voce_del_registro.get("publications") or []
            if "http" in (p.get("uri") or "")]
    return max([d for d in date if d] or [""])


def impronta_del_registro(voce_del_registro):
    """Impronta delle pubblicazioni in Gazzetta che l'elenco del registro cita per un prodotto (i loro
    indirizzi): cambia quando ne esce una nuova, rettifiche comprese. Vuota se il registro non ne cita."""
    indirizzi = sorted({(p.get("uri") or "").strip() for p in voce_del_registro.get("publications") or []
                        if "http" in (p.get("uri") or "")})
    return hashlib.sha256("\n".join(indirizzi).encode("utf-8")).hexdigest()[:12] if indirizzi else ""


# ───────────────────────── richieste ─────────────────────────

def chiedi(url, intestazioni=None, tentativi=3, massimo=None, solo_da=None):
    """(stato, contenuto). Stato 0 se non arriva una risposta utile, se pesa più di `massimo` byte o se, dopo
    un rinvio, arriva da un indirizzo che non comincia con `solo_da`."""
    ultimo = (0, b"")
    for n in range(tentativi):
        try:
            richiesta = urllib.request.Request(url, headers={"User-Agent": AGENTE, **(intestazioni or {})})
            with urllib.request.urlopen(richiesta, timeout=TEMPO_MASSIMO) as risposta:
                if solo_da and not risposta.geturl().startswith(solo_da):
                    return 0, b""
                corpo = risposta.read() if massimo is None else risposta.read(massimo + 1)
            time.sleep(PAUSA)
            if massimo is not None and len(corpo) > massimo:
                return 0, b""
            return risposta.status, corpo
        except urllib.error.HTTPError as e:
            ultimo = (e.code, b"")
            if e.code in (400, 403, 404, 406, 410, 429):
                break
        except Exception:  # rete, tempo scaduto, connessione chiusa
            ultimo = (0, b"")
        time.sleep(4 * (n + 1))
    return ultimo


def interroga(domanda):
    """Risposte dell'archivio dell'Ufficio delle pubblicazioni a una domanda SPARQL; None se non risponde."""
    stato, corpo = chiedi(SPARQL + "?" + urllib.parse.urlencode({"query": domanda, "format": "application/sparql-results+json"}),
                          {"Accept": "application/sparql-results+json"})
    if stato != 200:
        return None
    try:
        return json.loads(corpo)["results"]["bindings"]
    except (ValueError, KeyError, TypeError):
        return None


class Deposito:
    """Ciò che si è già scaricato: elenco del registro, schede dei prodotti, testi degli atti."""

    def __init__(self, cartella):
        self.base = Path(cartella)
        for nome in ("schede", "atti"):
            (self.base / nome).mkdir(parents=True, exist_ok=True)

    def leggi(self, *percorso, ore=None):
        """Con `ore`, un file più vecchio vale come assente: il registro cambia, gli atti della Gazzetta no."""
        p = self.base.joinpath(*percorso)
        try:
            if not p.exists() or (ore is not None and time.time() - p.stat().st_mtime > ore * 3600):
                return None
            return json.loads(p.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            return None  # un file rimasto a metà dopo un'interruzione vale come non scaricato

    def scrivi(self, dati, *percorso):
        p = self.base.joinpath(*percorso)
        provvisorio = p.with_name(p.name + ".tmp")
        provvisorio.write_text(json.dumps(dati, ensure_ascii=False), encoding="utf-8")
        os.replace(provvisorio, p)


def voci_italiane(dati):
    """Dall'elenco intero del registro, i prodotti agricoli e alimentari italiani."""
    return [v for v in dati if "IT" in (v.get("countries") or []) and v.get("productType") == "FOOD"]


def indice_per_nome(registro):
    """{nome senza spazi né accenti: [voci del registro]}, con ogni forma dei nomi protetti."""
    per_nome = {}
    for v in registro:
        for nome in v.get("protectedNames") or []:
            for parte in parti_del_nome(nome):
                per_nome.setdefault(parte, []).append(v)
    return per_nome


def elenco_del_registro(deposito, riusa):
    dati = deposito.leggi("elenco.json", ore=ORE_REGISTRO) if riusa else None
    if dati is None:
        stato, corpo = chiedi(REGISTRO, {"Accept": "application/json"})
        if stato != 200:
            return None
        try:
            dati = json.loads(corpo)
        except ValueError:
            return None
        deposito.scrivi(dati, "elenco.json")
    return voci_italiane(dati)


def scheda_del_registro(deposito, identificativo, riusa):
    if not re.fullmatch(r"[A-Za-z0-9_-]+", identificativo or ""):
        return None  # l'identificativo finisce in un nome di file e in un indirizzo: solo lettere e cifre
    dati = deposito.leggi("schede", f"{identificativo}.json", ore=ORE_REGISTRO) if riusa else None
    if dati is None:
        stato, corpo = chiedi(SCHEDA.format(identificativo), {"Accept": "application/json"})
        if stato != 200:
            return None
        try:
            dati = json.loads(corpo)
        except ValueError:
            return None
        deposito.scrivi(dati, "schede", f"{identificativo}.json")
    return dati


def celex_di(indirizzo):
    """(numero CELEX, risorsa dell'archivio da interrogare): uno dei due, o nessuno."""
    if not indirizzo or "corrigendum" in indirizzo:
        return None, None
    m = re.search(r"CELEX(?:%3A|:)([0-9A-Z%()]+)", indirizzo)
    if m:
        numero = urllib.parse.unquote(m.group(1))
        return (numero, None) if CELEX_VALIDO.fullmatch(numero) else (None, None)
    m = re.search(r"/eli/C/(\d{4})/(\d+)/oj", indirizzo)
    if m:
        return None, f"http://publications.europa.eu/resource/oj/C_{m.group(1)}{int(m.group(2)):05d}"
    m = re.search(r"/eli/(?:reg|reg_impl|reg_del)/(\d{4})/(\d+)/oj", indirizzo)
    if m:
        return f"3{m.group(1)}R{int(m.group(2)):04d}", None
    m = re.search(r"uri=OJ(?:%3A|:)(JO[CL]_\d{4}_\d+_R_\d+|[CL]_\d{9})(?:&|$)", indirizzo)
    if m:
        return None, f"http://publications.europa.eu/resource/oj/{m.group(1)}"
    m = re.search(r"uri=uriserv(?:%3A|:)(OJ\.[CL]_?\.\d{4}\.\d+\.\d+\.\d+\.\d+\.[A-Z]{3})", indirizzo)
    if m:
        return None, f"http://publications.europa.eu/resource/uriserv/{m.group(1)}"
    return None, None


def celex_della_risorsa(deposito, risorsa):
    """Numero CELEX di una risorsa dell'archivio; "" se l'archivio non lo conosce; None se non ha risposto."""
    chiave = "risorsa-" + hashlib.sha256(risorsa.encode()).hexdigest()[:24] + ".json"
    nota = deposito.leggi("atti", chiave)
    if nota:
        return nota["celex"]
    righe = interroga("PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> PREFIX owl: <http://www.w3.org/2002/07/owl#> "
                      "SELECT DISTINCT ?celex WHERE { "
                      f"{{ ?w owl:sameAs <{risorsa}> . ?w cdm:resource_legal_id_celex ?celex }} UNION "
                      f"{{ ?e owl:sameAs <{risorsa}> . ?e cdm:expression_belongs_to_work ?w . ?w cdm:resource_legal_id_celex ?celex }} }}")
    if righe is None:
        non_letti.append(f"l'archivio dell'UE non ha detto il numero CELEX di {risorsa}")
        return None
    try:
        numeri = sorted({r["celex"]["value"] for r in righe})
    except (KeyError, TypeError):
        non_letti.append(f"l'archivio dell'UE ha risposto in una forma inattesa per {risorsa}")
        return None
    numeri = [n for n in numeri if CELEX_VALIDO.fullmatch(n)]
    avvisi = [n for n in numeri if AVVISO_SERIE_C.fullmatch(n)]
    # un numero solo, oppure un solo avviso della serie C fra più numeri; altrimenti non si sceglie a caso
    numero = numeri[0] if len(numeri) == 1 else avvisi[0] if len(avvisi) == 1 else ""
    if not numero:
        return ""
    deposito.scrivi({"celex": numero}, "atti", chiave)
    return numero


def atto_in_italiano(deposito, celex):
    """Dati e testo del PDF italiano di un atto: {"pagine", "kb", "testo"} oppure {"manca": motivo}; None se
    l'archivio non si è fatto leggere."""
    if not CELEX_VALIDO.fullmatch(celex or ""):
        return {"manca": "numero CELEX non valido"}
    nome = re.sub(r"[^0-9A-Za-z]", "_", celex)
    noto = deposito.leggi("atti", f"{nome}.json")
    if noto is not None and "manca" in noto and not noto["manca"].startswith("PDF senza testo"):
        # un atto che l'archivio non aveva in italiano può arrivare dopo: quel «manca» vale 12 ore
        noto = deposito.leggi("atti", f"{nome}.json", ore=ORE_REGISTRO)
    if noto is not None and "manca" in noto:
        return noto
    if noto is not None:
        try:
            return dict(noto, testo=(deposito.base / "atti" / f"{nome}.txt").read_text(encoding="utf-8"))
        except OSError:
            pass  # nel deposito c'è la nota ma non il testo: l'atto si riscarica
    righe = interroga("PREFIX cdm: <http://publications.europa.eu/ontology/cdm#> SELECT DISTINCT ?tipo ?item WHERE { "
                      f'?work cdm:resource_legal_id_celex "{celex}"^^<http://www.w3.org/2001/XMLSchema#string> . '
                      "?expr cdm:expression_belongs_to_work ?work ; cdm:expression_uses_language "
                      "<http://publications.europa.eu/resource/authority/language/ITA> . "
                      "?manif cdm:manifestation_manifests_expression ?expr ; cdm:manifestation_type ?tipo . "
                      "OPTIONAL { ?item cdm:item_belongs_to_manifestation ?manif } }")
    if righe is None:
        non_letti.append(f"l'archivio dell'UE non ha risposto per l'atto {celex}")
        return None
    try:
        file_pdf = sorted(r["item"]["value"] for r in righe if r["tipo"]["value"].startswith("pdf") and "item" in r)
    except (KeyError, TypeError):
        non_letti.append(f"l'archivio dell'UE ha risposto in una forma inattesa per l'atto {celex}")
        return None
    if len(file_pdf) != 1:
        dati = {"manca": "l'archivio non ha l'atto in italiano" if not righe else f"{len(file_pdf)} file PDF in italiano"}
        deposito.scrivi(dati, "atti", f"{nome}.json")
        return dati
    indirizzo = file_pdf[0].replace("http://", "https://", 1)
    if not indirizzo.startswith(ARCHIVIO_FILE):
        non_letti.append(f"per l'atto {celex} l'archivio dell'UE indica un file fuori dal suo sito: non scaricato")
        return None
    stato, corpo = chiedi(indirizzo, {"Accept": "*/*"}, massimo=MASSIMO_PDF, solo_da=ARCHIVIO_FILE)
    if stato != 200 or not corpo.startswith(b"%PDF-"):
        non_letti.append(f"PDF dell'atto {celex} non scaricato dall'archivio dell'UE (HTTP {stato}, file troppo pesante "
                         f"o rinvio a un altro sito)")
        return None
    with tempfile.TemporaryDirectory() as temporanea:
        percorso = Path(temporanea) / "atto.pdf"
        percorso.write_bytes(corpo)
        try:
            dati_pdf = subprocess.run(["pdfinfo", str(percorso)], capture_output=True, timeout=120)
            letto = subprocess.run(["pdftotext", "-q", "-enc", "UTF-8", str(percorso), "-"], capture_output=True, timeout=300)
        except subprocess.TimeoutExpired:
            non_letti.append(f"il PDF dell'atto {celex} non si è lasciato leggere in tempo")
            return None
    if dati_pdf.returncode != 0 or letto.returncode != 0:
        non_letti.append(f"il PDF dell'atto {celex} non si è lasciato leggere (pdfinfo {dati_pdf.returncode}, pdftotext {letto.returncode})")
        return None
    info, testo = dati_pdf.stdout.decode("utf-8", "replace"), letto.stdout.decode("utf-8", "replace")
    pagine = re.search(r"^Pages:\s+(\d+)", info, re.M)
    if not pagine or len(testo.strip()) < 200:
        dati = {"manca": "PDF senza testo leggibile"}
        deposito.scrivi(dati, "atti", f"{nome}.json")
        return dati
    dati = {"pagine": int(pagine.group(1)), "kb": max(1, round(len(corpo) / 1024)), "sha256": hashlib.sha256(corpo).hexdigest()}
    (deposito.base / "atti" / f"{nome}.txt").write_text(testo, encoding="utf-8")
    deposito.scrivi(dati, "atti", f"{nome}.json")
    return dict(dati, testo=testo)


def che_sintesi_contiene(testo, forme, fascicolo=""):
    """(tipo, dubbio). tipo è «unico» o «scheda» se il testo ha quel titolo e, nei FINESTRA caratteri che
    seguono, la prima denominazione fra virgolette è una di `forme` (intera, parola per parola) oppure il
    numero di riferimento è il fascicolo del prodotto. dubbio è il tipo quando il titolo c'è e una
    denominazione compare lì vicino, ma non in quella forma: allora non si decide da soli."""
    piano = " ".join(testo.split())
    dubbio = ""
    for titolo, tipo in TITOLI:
        for trovato in re.finditer(titolo, piano):
            finestra = piano[trovato.end():trovato.end() + FINESTRA]
            citate = VIRGOLETTE.findall(finestra)
            if citate:
                prima = parole(citate[0])
                senza_sigla = re.sub(r" (dop|igp|pdo|pgi)$", "", prima)
                pezzi = [parole(pezzo) for pezzo in re.split(r"\s*/\s*", citate[0]) if parole(pezzo)]
                if prima in forme or senza_sigla in forme or (pezzi and all(pezzo in forme for pezzo in pezzi)):
                    return tipo, ""
            if ha_il_fascicolo(finestra, fascicolo):
                return tipo, ""
            vicino = f" {parole(finestra)} "
            if not dubbio and any(f" {forma} " in vicino for forma in forme if len(forma) >= 4):
                dubbio = tipo
    return "", dubbio


# ───────────────────────── domande a gruppi all'archivio dell'UE ─────────────────────────

def celex_dell_indirizzo(url):
    """Numero CELEX di un indirizzo di EUR-Lex (…?uri=CELEX:…)."""
    m = re.search(r"[?&]uri=CELEX:([^&#]+)", url or "")
    return urllib.parse.unquote(m.group(1)) if m else None


def a_gruppi(numeri):
    """I numeri CELEX in gruppi da A_GRUPPI_DI, senza doppioni; solo cifre, maiuscole e parentesi."""
    buoni = sorted({n for n in numeri if n and CELEX_COLLEGABILE.fullmatch(n)})
    return [buoni[i:i + A_GRUPPI_DI] for i in range(0, len(buoni), A_GRUPPI_DI)]


def domanda_esistenza(gruppo):
    """Domanda SPARQL: quali di questi numeri CELEX esistono nell'archivio."""
    valori = " ".join(f'"{c}"{STRINGA}' for c in gruppo)
    return CDM + f"SELECT DISTINCT ?celex WHERE {{ VALUES ?celex {{ {valori} }} ?w cdm:resource_legal_id_celex ?celex }}"


def domanda_rettifiche(gruppo):
    """Domanda SPARQL: quali atti l'archivio registra come rettifiche di questi, con la loro data."""
    valori = " ".join(f'"{c}"{STRINGA}' for c in gruppo)
    return (CDM + f"SELECT DISTINCT ?atto ?rettifica ?data WHERE {{ VALUES ?atto {{ {valori} }} "
            "?w cdm:resource_legal_id_celex ?atto . ?c cdm:resource_legal_corrects_resource_legal ?w ; "
            "cdm:resource_legal_id_celex ?rettifica . OPTIONAL { ?c cdm:work_date_document ?data } }")


def righe_delle_rettifiche(righe):
    """{atto: [(numero CELEX della rettifica, data AAAA-MM-GG o vuota)]} dalle risposte a domanda_rettifiche."""
    trovate = {}
    for r in righe:
        date = trovate.setdefault(r["atto"]["value"], {}).setdefault(r["rettifica"]["value"], set())
        data = (r.get("data") or {}).get("value", "")[:10]
        if data:
            date.add(data)  # l'archivio può dare più date per la stessa rettifica: vale la prima
    return {atto: sorted(((numero, min(date) if date else "") for numero, date in per_numero.items()),
                         key=lambda coppia: (coppia[1], coppia[0]))
            for atto, per_numero in trovate.items()}


def rettifiche_nell_archivio(atti):
    """Rettifiche che l'archivio lega a ciascun atto (relazione «corregge»); None se l'archivio non risponde."""
    righe = []
    for gruppo in a_gruppi(atti):
        risposta = interroga(domanda_rettifiche(gruppo))
        if risposta is None:
            return None
        righe += risposta
    try:
        return righe_delle_rettifiche(righe)
    except (KeyError, TypeError, AttributeError):
        return None  # risposta in una forma inattesa: vale come archivio che non ha risposto


def rettifica_cita_l_atto(testo_rettifica, celex, testo_atto, forme, data_atto=""):
    """Seconda verifica, oltre alla relazione dell'archivio: la rettifica nomina il prodotto (la denominazione
    intera), oppure il numero dell'atto («C/2025/3944», Gazzetta dal 1º ottobre 2023), oppure il fascicolo della
    Gazzetta in cui l'atto è uscito insieme al suo anno («C 440 del 26 novembre 2016»): il fascicolo si ricava
    dai numeri di pagina stampati nell'atto («C 440/7»), l'anno dalla data dell'atto, perché la numerazione
    dei fascicoli riparte ogni anno. Fascicolo e anno valgono per tutti gli avvisi usciti in quel fascicolo:
    questa verifica da sola non basterebbe, e infatti arriva dopo la relazione «corregge» dell'archivio."""
    piano = " ".join(testo_rettifica.split())
    if "ettifica" not in piano:
        return False
    disteso = f" {parole(piano)} "
    if any(f" {forma} " in disteso for forma in forme if len(forma) >= 4):
        return True
    nuovo = re.fullmatch(r"5(\d{4})XC0*(\d+)", celex)
    if nuovo and re.search(rf"C/{nuovo.group(1)}/{int(nuovo.group(2))}(?!\d)", piano):
        return True
    anno = (data_atto or "")[:4]
    if not re.fullmatch(r"\d{4}", anno):
        return False
    fascicoli = set(re.findall(r"\b([CL] \d{1,3})/\d+\b", testo_atto))
    return any(re.search(rf"\b{re.escape(f)} del\b[^()]{{0,40}}\b{anno}\b", piano) for f in fascicoli)


def aggiorna_rettifiche(deposito, voce, trovate, forme, sempre=False, anche_meno=False):
    """Scrive in voce["sintesi"] le rettifiche dell'atto: quelle con il testo in italiano che citano l'atto in
    «rettifiche», le altre in «rettifiche_altre». Una rettifica recente che non ha ancora il testo in italiano
    non si annota: resta una novità per il controllo mensile, finché il testo arriva. Ciò che il sito già
    mostra non arretra da solo: se nella risposta dell'archivio manca una rettifica che i dati conoscono, la
    voce resta com'era (l'archivio può aver risposto a metà); se di una rettifica collegata oggi manca il testo
    italiano, o non supera più la verifica, resta collegata e lo script lo dice. Con `anche_meno`, cioè quando
    chi lancia lo script ha chiesto proprio quel prodotto, vale la risposta di oggi. Restituisce gli avvisi
    per chi lancia lo script; None se una fonte non si è fatta leggere, e anche allora la voce resta com'era."""
    sintesi = voce["sintesi"]
    recente = (date.today() - timedelta(days=GIORNI_RECENTI)).isoformat()
    celex = celex_dell_indirizzo(sintesi["url"])
    mostrate_prima = {celex_dell_indirizzo(r["url"]): r for r in sintesi.get("rettifiche", [])}
    gia = set(mostrate_prima) | set(sintesi.get("rettifiche_altre", []))
    if not sempre and {numero for numero, _ in trovate} == gia:
        return []
    sparite = sorted(gia - {numero for numero, _ in trovate})
    if sparite and not anche_meno:
        return [f"«{voce['nome']}»: l'archivio dell'UE non restituisce più {', '.join(sparite)}, che i dati conoscono come "
                f"rettifiche dell'atto {celex}: le rettifiche restano com'erano. Se l'archivio ha davvero tolto il "
                f"legame: --nome \"{voce['nome']}\""]
    avvisi, mostrate, altre = [], [], []
    atto = atto_in_italiano(deposito, celex) if trovate else {}
    if atto is None:
        return None
    if "manca" in atto:
        # la sintesi è stata letta nel testo italiano di questo atto: se oggi l'archivio dice di non averlo,
        # è la risposta di oggi che non vale
        non_letti.append(f"l'archivio dell'UE non dà il testo italiano dell'atto {celex}, da cui viene la sintesi di "
                         f"«{voce['nome']}» ({atto['manca']})")
        return None
    for numero, data in trovate:
        nota = None if anche_meno else mostrate_prima.get(numero)  # una rettifica che il sito già mostra
        if not CELEX_COLLEGABILE.fullmatch(numero):
            avvisi.append(f"«{voce['nome']}»: la rettifica {numero} ha un numero CELEX che il sito non sa collegare: "
                          f"non annotata, da guardare a mano")
            continue
        rettifica = atto_in_italiano(deposito, numero)
        if rettifica is None:
            return None
        if "manca" in rettifica:
            if nota:
                mostrate.append(nota)
                avvisi.append(f"«{voce['nome']}»: l'archivio non dà il testo italiano della rettifica {numero}, che il "
                              f"sito collega ({rettifica['manca']}): resta com'era, da guardare a mano")
            elif not data or data >= recente:
                avvisi.append(f"«{voce['nome']}»: la rettifica {numero} non ha ancora il testo in italiano "
                              f"({rettifica['manca']}): non annotata, si riprova al prossimo giro")
            else:
                altre.append(numero)  # non c'è in italiano: corregge altre versioni linguistiche
        elif (not re.fullmatch(r"\d{4}-\d{2}-\d{2}", data)
              or not rettifica_cita_l_atto(rettifica["testo"], celex, atto["testo"], forme, sintesi.get("data", ""))):
            if nota:
                mostrate.append(nota)
                avvisi.append(f"«{voce['nome']}»: la rettifica {numero}, che il sito collega, oggi non supera la verifica "
                              f"(senza data, o non cita l'atto {celex}): resta com'era, da guardare a mano")
            else:
                altre.append(numero)
                avvisi.append(f"«{voce['nome']}»: la rettifica {numero} non è stata collegata (senza data, o non cita "
                              f"l'atto {celex}): da guardare a mano")
        else:
            mostrate.append({"url": EURLEX_PDF.format(numero.replace("(", "%28").replace(")", "%29")), "data": data,
                             "pagine": rettifica["pagine"], "kb": rettifica["kb"]})
    for chiave, valore in (("rettifiche", mostrate), ("rettifiche_altre", sorted(altre))):
        if valore:
            sintesi[chiave] = valore
        else:
            sintesi.pop(chiave, None)
    return avvisi


# ───────────────────────── il lavoro su un prodotto ─────────────────────────

def abbina(voce, per_nome):
    """Voce del registro con lo stesso nome del prodotto del catalogo: una sola, o None."""
    trovate = {}
    for parte in parti_del_nome(voce["nome"]):
        for v in per_nome.get(parte, []):
            trovate[v["giIdentifier"]] = v
    registrate = [v for v in trovate.values() if (v.get("status") or "").lower() == "registered"]
    scelte = registrate or list(trovate.values())
    return scelte[0] if len(scelte) == 1 else None


def pubblicazioni(scheda):
    """Pubblicazioni in Gazzetta della registrazione e delle modifiche approvate, dalla più recente."""
    registrazione = scheda.get("registration") or {}
    elenco = [(data_del_registro(p.get("date")), p.get("uri"), (p.get("text") or "").strip())
              for p in registrazione.get("officialPublication") or []]
    for modifica in scheda.get("amendment") or []:
        if modifica.get("type") == "TEMPORARY_AMENDMENT" or modifica.get("status") != "APPROVED":
            continue
        elenco += [(data_del_registro(p.get("date")), p.get("uri"), (p.get("text") or "").strip())
                   for p in modifica.get("officialPublication") or []]
    elenco = [p for p in elenco if p[1] and "orrigendum" not in p[2]]
    # una pubblicazione senza data va in testa: finché non si sa di quando è, non si può dire qual è l'ultima
    return sorted(elenco, key=lambda p: (p[0] or "9999-99-99", p[1], p[2]), reverse=True)


def cerca_sintesi(deposito, voce, del_registro, scheda, a_mano=False):
    """La sintesi più recente del prodotto: (dati, tutto_letto, da_guardare). Senza sintesi i dati sono None.
    tutto_letto è falso se una fonte non ha risposto; da_guardare elenca ciò che lo script non sa decidere
    da solo (pubblicazione senza data o non interpretabile, sintesi che nomina il prodotto in un'altra forma,
    atto appena uscito di cui l'archivio non ha ancora il testo italiano). In tutti e due i casi chi chiama
    lascia il prodotto com'era. Con `a_mano` (chi lancia lo script ha chiesto proprio quel prodotto) una
    pubblicazione senza data si salta, invece di fermare la ricerca."""
    forme = denominazioni([voce["nome"]] + list(del_registro.get("protectedNames") or []))
    fascicolo = del_registro.get("fileNumber") or voce.get("fascicolo") or ""
    recente = (date.today() - timedelta(days=GIORNI_RECENTI)).isoformat()
    riserva = None
    for data, indirizzo, testo_rif in pubblicazioni(scheda):
        if "corrigendum" in indirizzo:
            continue  # le rettifiche si trattano a parte, con la relazione «corregge» dell'archivio
        citata = f"{testo_rif or 'senza testo'}, {indirizzo}"
        if not data:
            if a_mano:
                continue
            return None, True, [f"«{voce['nome']}»: il registro cita una pubblicazione senza data ({citata}): non si "
                                f"può dire qual è la più recente (per saltarla: --nome \"{voce['nome']}\")"]
        celex, risorsa = celex_di(indirizzo)
        candidati, a_numeri = ([celex] if celex else []), False
        if risorsa:
            trovato = celex_della_risorsa(deposito, risorsa)
            if trovato is None:
                return None, False, []
            candidati = [trovato] if trovato else []
        elif not celex and data < "2023-10-01" and re.search(r"Official Journal C\b", testo_rif):
            # il registro cita solo il fascicolo della Gazzetta: fino al 30/9/2023 gli avvisi della serie C
            # hanno CELEX 5AAAAXCMMGG(NN), e si provano quelli di quel giorno, uno dopo l'altro
            aaaa, mm, gg = data.split("-")
            candidati, a_numeri = [f"5{aaaa}XC{mm}{gg}({n:02d})" for n in range(1, AVVISI_AL_GIORNO + 1)], True
        if not candidati:
            return None, True, [f"«{voce['nome']}»: pubblicazione che lo script non sa interpretare ({citata})"]
        if all(RETTIFICA.search(numero) for numero in candidati):
            continue  # una rettifica citata con il suo numero CELEX: come quelle con «corrigendum» nell'indirizzo
        vuoti = 0
        for numero in candidati:
            atto = atto_in_italiano(deposito, numero)
            if atto is None:
                return None, False, []
            if "manca" in atto:
                if not a_numeri and data >= recente:
                    # un atto appena uscito può arrivare in archivio qualche giorno dopo: saltarlo vorrebbe dire
                    # scegliere una sintesi più vecchia e segnare il prodotto come già letto
                    return None, True, [f"«{voce['nome']}»: l'atto {numero}, che il registro cita con la data {data}, non "
                                        f"ha ancora il testo in italiano nell'archivio ({atto['manca']}): si riprova al "
                                        f"prossimo giro"]
                vuoti += 1
                if a_numeri and vuoti >= 3:
                    break  # tre numeri di fila senza un atto in italiano: gli avvisi di quel giorno sono finiti
                continue
            vuoti = 0
            tipo, dubbio = che_sintesi_contiene(atto["testo"], forme, fascicolo)
            if not tipo:
                if dubbio and not a_numeri:
                    # l'atto è citato dal registro per questo prodotto e ha il titolo, ma la denominazione non è
                    # scritta come ci si aspetta: collegarlo o saltarlo sarebbero tutti e due una scelta al buio
                    return None, True, [f"«{voce['nome']}»: l'atto {numero} ha "
                                        f"{'un documento unico' if dubbio == 'unico' else 'una scheda riepilogativa'} "
                                        f"che nomina il prodotto, ma non come denominazione sotto il titolo"]
                continue
            if not CELEX_COLLEGABILE.fullmatch(numero):
                return None, True, [f"«{voce['nome']}»: l'atto {numero} contiene "
                                    f"{'un documento unico' if tipo == 'unico' else 'una scheda riepilogativa'}, ma ha un "
                                    f"numero CELEX di vecchio tipo: il collegamento al PDF va cercato a mano"]
            sintesi = {"tipo": tipo, "url": EURLEX_PDF.format(numero.replace("(", "%28").replace(")", "%29")),
                       "data": data, "pagine": atto["pagine"], "kb": atto["kb"]}
            if tipo == "unico":
                return sintesi, True, []
            riserva = riserva or sintesi
            break
    return riserva, True, []


# ───────────────────────── il file dei dati ─────────────────────────

def testo_del_catalogo(dati):
    """Il file com'è scritto nel repository: un elemento per riga negli elenchi, così i confronti si leggono."""
    righe = ["{"]
    chiavi = list(dati)
    for n, chiave in enumerate(chiavi):
        valore, virgola = dati[chiave], "," if n < len(chiavi) - 1 else ""
        if isinstance(valore, list):
            righe.append(f'  "{chiave}": [')
            righe += [f"    {json.dumps(v, ensure_ascii=False)}{',' if i < len(valore) - 1 else ''}" for i, v in enumerate(valore)]
            righe.append(f"  ]{virgola}")
        else:
            righe.append(f'  "{chiave}": {json.dumps(valore, ensure_ascii=False)}{virgola}')
    return "\n".join(righe + ["}"]) + "\n"


def scrivi_catalogo(testo):
    """Scrive il file dei dati tutto insieme: prima su un file accanto, poi al suo posto. Un'interruzione a
    metà lascia il file com'era."""
    provvisorio = FILE_CATALOGO.with_name(FILE_CATALOGO.name + ".tmp")
    try:
        provvisorio.write_text(testo, encoding="utf-8")
        os.replace(provvisorio, FILE_CATALOGO)
    finally:
        if provvisorio.exists():  # la scrittura si è interrotta: il file accanto non deve restare
            provvisorio.unlink()


def riordina(voce):
    """Campi sempre nello stesso ordine: prima quelli del Ministero, poi quelli europei."""
    ordine = ("nome", "tipo", "regioni", "classe", "url", "formato", "pagine", "kb", "peso_dichiarato", "extra",
              "fascicolo", "sintesi", "registro_ue")
    return {k: voce[k] for k in ordine if k in voce} | {k: v for k, v in voce.items() if k not in ordine}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--tutti", action="store_true", help="rilegge ogni prodotto, non solo quelli con una pubblicazione nuova")
    ap.add_argument("--nome", action="append", default=[], help="lavora solo su questo prodotto (ripetibile)")
    ap.add_argument("--prova", action="store_true", help="non scrive il file: dice che cosa cambierebbe")
    ap.add_argument("--cartella", help="cartella in cui tenere ciò che si scarica; senza, una temporanea")
    ap.add_argument("--formato", action="store_true", help="controlla solo che il file dei dati sia scritto nel formato di questo script")
    ap.add_argument("--riscrivi", action="store_true", help="senza rete: riscrive il file dei dati nel formato di questo script")
    args = ap.parse_args()

    originale = FILE_CATALOGO.read_text(encoding="utf-8")
    catalogo = json.loads(originale)
    if args.formato:
        uguale = testo_del_catalogo(catalogo) == originale
        print("formato del file: " + ("uguale a quello che scrive questo script" if uguale else "DIVERSO da quello che scrive questo script"))
        return 0 if uguale else 1
    if args.riscrivi:
        catalogo["voci"] = [riordina(v) for v in catalogo["voci"]]
        nuovo = testo_del_catalogo(catalogo)
        if nuovo != originale:
            scrivi_catalogo(nuovo)
        print("File dei dati riscritto nel suo formato." if nuovo != originale else "Il file dei dati era già nel suo formato.")
        return 0
    sconosciuti = sorted(set(args.nome) - {v["nome"] for v in catalogo["voci"]})
    if sconosciuti:
        ap.error("nel catalogo non c'è un prodotto con questo nome (va scritto come in data/disciplinari.json): "
                 + "; ".join(sconosciuti))
    garantite = sorted(v["nome"] for v in catalogo["voci"] if v["nome"] in args.nome and v["tipo"] == "STG")
    if garantite:
        ap.error("le STG non sono nel registro delle indicazioni geografiche e non hanno una sintesi europea: "
                 + "; ".join(garantite))
    for programma in ("pdftotext", "pdfinfo"):
        if not shutil.which(programma):
            sys.exit(f"Manca {programma}: sudo apt-get update && sudo apt-get install -y poppler-utils")

    temporanea = None if args.cartella else tempfile.TemporaryDirectory()
    deposito = Deposito(args.cartella or temporanea.name)
    registro = elenco_del_registro(deposito, riusa=bool(args.cartella))
    if registro is None:
        sys.exit("Il registro europeo eAmbrosia non si è fatto leggere: nessun dato cambiato.")
    per_nome = indice_per_nome(registro)

    cambiate, senza_voce, avvisi, letti = [], [], [], 0
    for voce in catalogo["voci"]:
        if voce["tipo"] == "STG" or (args.nome and voce["nome"] not in args.nome):
            continue  # le STG non sono nel registro delle indicazioni geografiche
        del_registro = abbina(voce, per_nome)
        if del_registro is None:
            senza_voce.append(voce["nome"])
            continue
        prima = json.dumps(voce, ensure_ascii=False, sort_keys=True)
        voce["fascicolo"] = del_registro["fileNumber"]
        impronta = impronta_del_registro(del_registro)
        if args.tutti or args.nome or voce.get("registro_ue") != impronta:
            scheda = scheda_del_registro(deposito, del_registro["giIdentifier"], riusa=bool(args.cartella))
            if scheda is None:
                non_letti.append(f"scheda del registro non letta per «{voce['nome']}»")
                sintesi, tutto_letto, da_guardare = None, False, []
            else:
                sintesi, tutto_letto, da_guardare = cerca_sintesi(deposito, voce, del_registro, scheda, a_mano=bool(args.nome))
                letti += 1
            vecchia = voce.get("sintesi") or {}
            if tutto_letto and not da_guardare:
                if sintesi and not impronta:
                    # senza indirizzi nell'elenco del registro non c'è impronta, e senza impronta il controllo
                    # mensile non può accorgersi di una pubblicazione nuova: una sintesi così non si scrive
                    da_guardare = [f"«{voce['nome']}»: la scheda del registro ha una sintesi, ma l'elenco del registro non "
                                   f"cita pubblicazioni con un indirizzo"]
                elif vecchia and not args.nome and (not sintesi or sintesi["data"] < vecchia.get("data", "")):
                    # ciò che il sito già mostra non arretra da solo: l'archivio può aver risposto a metà
                    da_guardare = [f"«{voce['nome']}»: la ricerca di oggi darebbe "
                                   + (f"una sintesi più vecchia ({sintesi['data']})" if sintesi else "nessuna sintesi")
                                   + f" al posto di quella del {vecchia.get('data')} (per accettarla: --nome \"{voce['nome']}\")"]
            if not tutto_letto:
                pass  # una fonte non si è fatta leggere: sintesi e impronta restano com'erano
            elif da_guardare:
                # sintesi e impronta restano com'erano: così il controllo mensile continua a segnalare il prodotto
                avvisi += [riga + ": il prodotto resta com'era, da guardare a mano" for riga in da_guardare]
            else:
                if sintesi:
                    if vecchia.get("url") == sintesi["url"]:  # stesso atto: le rettifiche già note restano
                        sintesi.update({k: vecchia[k] for k in ("rettifiche", "rettifiche_altre") if k in vecchia})
                    voce["sintesi"] = sintesi
                else:
                    voce.pop("sintesi", None)
                voce["registro_ue"] = impronta
        if json.dumps(voce, ensure_ascii=False, sort_keys=True) != prima:
            cambiate.append(voce["nome"])
        if letti and letti % 25 == 0:
            print(f"… {letti} prodotti riletti", file=sys.stderr, flush=True)

    # Rettifiche: si chiedono per ogni prodotto con una sintesi, perché il registro non le cita sempre.
    scelte = [v for v in catalogo["voci"] if v.get("sintesi") and (not args.nome or v["nome"] in args.nome)]
    note = rettifiche_nell_archivio([celex_dell_indirizzo(v["sintesi"]["url"]) for v in scelte])
    if note is None:
        non_letti.append("l'archivio dell'UE non ha detto quali atti hanno una rettifica: le rettifiche restano com'erano")
    for voce in scelte if note is not None else []:
        prima = json.dumps(voce, ensure_ascii=False, sort_keys=True)
        forme = denominazioni([voce["nome"]] + list((abbina(voce, per_nome) or {}).get("protectedNames") or []))
        esito = aggiorna_rettifiche(deposito, voce, note.get(celex_dell_indirizzo(voce["sintesi"]["url"]), []), forme,
                                    sempre=args.tutti or bool(args.nome), anche_meno=bool(args.nome))
        if esito is None:
            non_letti.append(f"rettifiche di «{voce['nome']}» non lette")
            continue
        avvisi += esito
        if json.dumps(voce, ensure_ascii=False, sort_keys=True) != prima and voce["nome"] not in cambiate:
            cambiate.append(voce["nome"])
    catalogo["voci"] = [riordina(v) for v in catalogo["voci"]]

    con = [v for v in catalogo["voci"] if v.get("sintesi")]
    print(f"Prodotti riletti: {letti}. Voci cambiate: {len(cambiate)}.")
    print(f"Con una sintesi europea: {len(con)} (documento unico {sum(1 for v in con if v['sintesi']['tipo'] == 'unico')}, "
          f"scheda riepilogativa {sum(1 for v in con if v['sintesi']['tipo'] == 'scheda')}). "
          f"Rettifiche collegate: {sum(len(v['sintesi'].get('rettifiche', [])) for v in con)}.")
    for riga in avvisi:
        print("Da guardare: " + riga)
    if cambiate:
        print("Cambiate: " + "; ".join(cambiate[:40]) + (" …" if len(cambiate) > 40 else ""))
    if senza_voce:
        print("Senza una voce con lo stesso nome nel registro europeo (da guardare a mano): " + "; ".join(senza_voce))
    if non_letti:
        print("Fonti che non si sono fatte leggere (le voci interessate restano com'erano):")
        for riga in non_letti[:30]:
            print("  - " + riga)
    nuovo = testo_del_catalogo(catalogo)
    if args.prova:
        print("Prova: il file non è stato scritto." if nuovo != originale else "Prova: nessun cambiamento.")
    elif nuovo != originale:
        scrivi_catalogo(nuovo)
        print(f"Scritto {FILE_CATALOGO.relative_to(RADICE)}.")
    else:
        print("Nessun cambiamento.")
    return 1 if non_letti else 3 if avvisi or senza_voce else 0


if __name__ == "__main__":
    sys.exit(main())
