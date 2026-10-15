#!/usr/bin/env python3
"""Manuali ufficiali per scrivere i testi della pubblica amministrazione (AgID e Designers Italia).

Tiene aggiornati dentro la skill i testi dei manuali e controlla una pagina con le regole che i manuali scrivono in modo esplicito.
Comandi:
  versioni     di quando sono i manuali che la skill sta usando
  controlla    confronta con i manuali su GitHub: codice 0 aggiornati, 1 cambiati, 2 non raggiungibili
  aggiorna     scarica i manuali e riscrive la copia in uso (o --uscita), dice cosa è cambiato; --pacchetto crea il file .skill
  testo FILE   controlla pagine Markdown (anche con front matter Hugo) e cita per ogni segnalazione la sezione del manuale
Serve git per scaricare; «aggiorna» usa anche PyYAML per le pagine dei Fondamenti. --autotest prova tutto senza rete.
Lo stesso file è nel repository del sito della PC Genzano come scripts/manuali-agid.py: il workflow aggiorna-manuale.yml lo usa
ogni lunedì con «aggiorna --uscita .manuale/manuali-agid --resoconto» e mette le righe cambiate nell'issue di revisione.
La copia in uso è references/manuali nella skill e .manuale/manuali-agid nel repository del sito.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

try:  # ora italiana anche dove l'orologio è in UTC (il workflow del sito gira su GitHub)
    from zoneinfo import ZoneInfo
    FUSO = ZoneInfo("Europe/Rome")
except Exception:  # senza la banca dati dei fusi orari vale l'ora del computer
    FUSO = None

CARTELLA_SKILL = Path(__file__).resolve().parent.parent
# Nella skill i manuali stanno in references/manuali; nel repository del sito (niente SKILL.md accanto a scripts/) stanno nella
# copia che il controllo del lunedì tiene in .manuale/manuali-agid. Il file .skill si crea solo dentro la skill.
DENTRO_LA_SKILL = (CARTELLA_SKILL / "SKILL.md").is_file()
MANUALI = CARTELLA_SKILL / ("references/manuali" if DENTRO_LA_SKILL else ".manuale/manuali-agid")
CACHE = Path(os.environ.get("MANUALI_AGID_CACHE") or Path.home() / ".cache" / "manuali-agid")
BASE_DI = "https://designers.italia.it"
MOD_URL = "https://docs.italia.it/italia/designers-italia/manuale-operativo-design-docs/it/versione-corrente/doc/progettazione-dei-contenuti/"
VERSIONAMENTO = "src/data/content/design-system/fondamenti/versionamento.yaml"
FINE_INTESTAZIONE = "<!-- fine intestazione -->"
COMANDO = f"python3 scripts/{Path(__file__).name}"  # scripts/manuali.py nella skill, scripts/manuali-agid.py nel sito

FONTI = {
    "lg-design": {"nome": "AgID, Linee guida di design per i siti internet e i servizi digitali della PA", "editore": "AgID",
                  "repo": "https://github.com/italia/lg-design-servizi-web", "ramo": "versione-corrente", "licenza": "CC0 1.0", "sparse": False},
    "designers": {"nome": "Designers Italia, design system .italia (sito designers.italia.it)", "editore": "Designers Italia",
                  "repo": "https://github.com/italia/designers.italia.it", "ramo": "main", "licenza": "CC BY 4.0", "sparse": True},
    "parole-pa": {"nome": "Designers Italia, Guida alle parole della Pubblica Amministrazione", "editore": "Designers Italia",
                  "repo": "https://github.com/italia/writing-toolkit", "ramo": "master", "licenza": "CC BY 4.0", "sparse": False},
    "mod": {"nome": "Designers Italia, Manuale operativo di design", "editore": "Designers Italia",
            "repo": "https://github.com/italia/manuale-operativo-design-docs", "ramo": "versione-corrente", "licenza": "CC BY 4.0", "sparse": False},
}
LICENZE = {"CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/deed.it", "CC0 1.0": "https://creativecommons.org/publicdomain/zero/1.0/deed.it"}
FONDAMENTI = {"contenuti": "Contenuti", "linguaggio": "Linguaggio", "microtesti": "Microtesti", "tono-di-voce": "Tono di voce"}
MOD_PAGINE = {"scrittura-e-linguaggio": "Scrittura e linguaggio", "architettura-dell-informazione": "Architettura dell'informazione",
              "documenti": "Documenti", "immagini-e-video": "Immagini e video",
              "ottimizzazione-per-i-motori-di-ricerca-seo": "Ottimizzazione per i motori di ricerca (SEO)",
              "proprieta-intellettuale-e-privacy": "Proprietà intellettuale e privacy", "gestire-i-contenuti": "Gestire i contenuti"}


def _documenti(fonti_file: dict | None = None) -> list[dict]:
    documenti = [{"id": "linee-guida-design", "fonte": "lg-design", "file": ["note-lettura.rst", "requisiti.rst"], "tipo": "rst",
                  "uscita": "linee-guida-design.rst", "url": f"{BASE_DI}/normativa/linee-guida-di-design/",
                  "titolo": "Linee guida di design per i siti internet e i servizi digitali della PA: note di lettura e requisiti"}]
    for nome, titolo in FONDAMENTI.items():
        documenti.append({"id": f"fondamenti-{nome}", "fonte": "designers", "file": [f"src/data/content/design-system/fondamenti/{nome}.yaml"],
                          "tipo": "pagina", "uscita": f"fondamenti-{nome}.md", "url": f"{BASE_DI}/design-system/fondamenti/{nome}/",
                          "titolo": f"Fondamenti del design system .italia: {titolo}"})
    documenti.append({"id": "guida-parole-pa", "fonte": "parole-pa", "file": ["index.rst", "le-parole-della-pubblica-amministrazione/*.rst"],
                      "tipo": "rst", "uscita": "guida-parole-pa.rst", "titolo": "Guida alle parole della Pubblica Amministrazione",
                      "url": "https://docs.italia.it/italia/designers-italia/writing-toolkit/it/bozza/le-parole-della-pubblica-amministrazione.html"})
    for nome, titolo in MOD_PAGINE.items():
        documenti.append({"id": f"mod-{nome}", "fonte": "mod", "file": [f"doc/progettazione-dei-contenuti/{nome}.rst"], "tipo": "rst",
                          "uscita": f"mod-{nome}.rst", "url": f"{MOD_URL}{nome}.html", "titolo": f"Manuale operativo di design: {titolo}"})
    return documenti


DOCUMENTI = _documenti()
PER_ID = {d["id"]: d for d in DOCUMENTI}


class ErroreRete(Exception):
    pass


# ————————————————————————————————————————— scaricare con git —————————————————————————————————————————

def git(argomenti: list, attesa: int = 300) -> str:
    try:
        esito = subprocess.run(["git", *map(str, argomenti)], capture_output=True, text=True, timeout=attesa,
                               env={**os.environ, "GIT_TERMINAL_PROMPT": "0", "LC_ALL": "C"})
    except FileNotFoundError:
        raise ErroreRete("git non è installato su questo computer") from None
    except subprocess.TimeoutExpired:
        raise ErroreRete(f"git {argomenti[0]}: tempo scaduto") from None
    if esito.returncode != 0:
        raise ErroreRete(f"git {argomenti[0] if argomenti[0] != '-C' else argomenti[2]}: {(esito.stderr or esito.stdout).strip()[-300:]}")
    return esito.stdout


def file_della_fonte(fid: str, documenti: list[dict]) -> list[str]:
    elenco = [f for d in documenti if d["fonte"] == fid for f in d["file"]]
    if fid == "designers":
        elenco.append(VERSIONAMENTO)
    return elenco


def commit_remoto(fonte: dict) -> str:
    uscita = git(["ls-remote", fonte["repo"], f"refs/heads/{fonte['ramo']}"], attesa=90)
    if not uscita.strip():
        raise ErroreRete(f"ramo {fonte['ramo']} non trovato in {fonte['repo']}")
    return uscita.split()[0]


def copia_aggiornata(fid: str, fonte: dict, cache: Path, documenti: list[dict]) -> tuple[Path, str, str]:
    """Clona (o aggiorna) la fonte in cache, solo l'ultima versione e, per designers.italia.it, solo i file che servono."""
    destinazione = cache / fid
    if (destinazione / ".git").is_dir():
        git(["-C", destinazione, "remote", "set-url", "origin", fonte["repo"]])
        git(["-C", destinazione, "fetch", "--quiet", "--depth", "1", "origin", fonte["ramo"]])
        git(["-C", destinazione, "reset", "--quiet", "--hard", "FETCH_HEAD"])
    else:
        if destinazione.exists():
            shutil.rmtree(destinazione)
        destinazione.parent.mkdir(parents=True, exist_ok=True)
        comando = ["clone", "--quiet", "--depth", "1", "--branch", fonte["ramo"]]
        if fonte.get("sparse"):
            comando += ["--filter=blob:none", "--sparse"]
        git(comando + [fonte["repo"], destinazione])
    if fonte.get("sparse"):
        git(["-C", destinazione, "sparse-checkout", "set", "--no-cone", *["/" + f for f in file_della_fonte(fid, documenti)]])
    commit = git(["-C", destinazione, "rev-parse", "HEAD"]).strip()
    data = git(["-C", destinazione, "log", "-1", "--format=%cI"]).strip()
    return destinazione, commit, data


def leggi_sorgenti(documento: dict, cartella: Path) -> list[tuple[str, bytes]]:
    trovati = []
    for schema in documento["file"]:
        if any(c in schema for c in "*?["):
            percorsi = sorted(cartella.glob(schema))
            if not percorsi:
                raise FileNotFoundError(f"{documento['id']}: nessun file per {schema}")
            trovati += [(p.relative_to(cartella).as_posix(), p.read_bytes()) for p in percorsi]
        else:
            percorso = cartella / schema
            if not percorso.is_file():
                raise FileNotFoundError(f"{documento['id']}: manca {schema} (il manuale è stato spostato o rinominato?)")
            trovati.append((schema, percorso.read_bytes()))
    return trovati


def impronta(sorgenti: list[tuple[str, bytes]]) -> str:
    calcolo = hashlib.sha256()
    for nome, dati in sorgenti:
        calcolo.update(nome.encode("utf-8") + b"\0" + dati.replace(b"\r\n", b"\n") + b"\0")
    return calcolo.hexdigest()


# ————————————————————————————————————————— conversione dei testi —————————————————————————————————————————

def data_italiana(iso: str) -> str:
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%d/%m/%Y")
    except ValueError:
        return iso[:10]


def assoluto(url: str) -> str:
    url = (url or "").strip()
    if url.startswith("/"):
        return BASE_DI + url
    if re.match(r"(design-system|risorse-per-progettare|modelli|normativa|community)/", url):
        return f"{BASE_DI}/{url}"
    return url


def pulisci(testo) -> str:
    t = str(testo).replace("\r\n", "\n")
    t = re.sub(r"!\[([^\]]*)\]\([^)]*\)", lambda m: f"(Immagine: {m.group(1).strip()})", t)
    t = re.sub(r"\]\(([^)\s]+)", lambda m: "](" + assoluto(m.group(1)), t)
    return t.strip()


def _cella(colonna) -> str:
    if not isinstance(colonna, dict):
        return ""
    if colonna.get("text") is not None:
        testo = str(colonna["text"])
    elif isinstance(colonna.get("tag"), dict):
        testo = str(colonna["tag"].get("label", ""))
    elif isinstance(colonna.get("simpleCta"), dict):
        cta = colonna["simpleCta"]
        testo = f"[{cta.get('label', '')}]({assoluto(cta.get('url', ''))})"
    else:
        testo = ""
    return re.sub(r"\s+", " ", pulisci(testo)).replace("|", "\\|").strip()


def _tabella(componente: dict) -> list[str]:
    testa = [_cella(c) for c in componente.get("head") or []]
    righe = [[_cella(c) for c in (r or {}).get("cols") or []] for r in componente.get("rows") or []]
    colonne = max([len(testa)] + [len(r) for r in righe] + [1])
    testa += [""] * (colonne - len(testa))
    uscita = ["| " + " | ".join(testa) + " |", "|" + "---|" * colonne]
    for riga in righe:
        riga += [""] * (colonne - len(riga))
        uscita.append("| " + " | ".join(riga) + " |")
    return uscita + [""]


def _componente(componente) -> list[str]:
    if not isinstance(componente, dict):
        return []
    uscita = []
    if componente.get("title"):
        livello = componente.get("headingLevel")
        livello = livello if isinstance(livello, int) and 2 <= livello <= 4 else 3
        uscita += [f"{'#' * livello} {str(componente['title']).strip()}", ""]
    if componente.get("name") == "Table":
        uscita += _tabella(componente)
    else:
        if componente.get("text"):
            uscita += [pulisci(componente["text"]), ""]
        if componente.get("img") and componente.get("alt"):
            uscita += [f"(Immagine: {componente['alt']})", ""]
    for cta in componente.get("ctas") or []:
        if isinstance(cta, dict) and cta.get("label"):
            uscita += [f"→ [{str(cta['label']).strip()}]({assoluto(cta.get('url', ''))})", ""]
    return uscita


def intestazione(documento: dict, fonte: dict, commit: str, data: str) -> str:
    file = ", ".join(documento["file"])
    return (f"> Testo ufficiale di {fonte['editore']}, «{documento['titolo']}» ({documento['url']}), licenza {fonte['licenza']} "
            f"({LICENZE[fonte['licenza']]}). Convertito in Markdown senza cambiare il testo dal file {file} del repository "
            f"{fonte['repo']} (commit {commit[:7]} del {data_italiana(data)}). Non modificarlo a mano: si aggiorna con "
            f"`{COMANDO} aggiorna`.")


def pagina_in_markdown(dati: bytes, documento: dict, fonte: dict, commit: str, data: str) -> str:
    try:
        import yaml
    except ImportError:
        raise SystemExit("Per aggiornare i Fondamenti serve PyYAML: pip install pyyaml") from None
    pagina = yaml.safe_load(dati.decode("utf-8")) or {}
    componenti = pagina.get("components") or {}
    eroe = componenti.get("hero") or {}
    titolo = eroe.get("title") or (pagina.get("seo") or {}).get("name") or documento["titolo"]
    righe = [f"# {titolo}", "", intestazione(documento, fonte, commit, data), FINE_INTESTAZIONE, ""]
    if eroe.get("subtitle"):
        righe += [pulisci(eroe["subtitle"]), ""]
    for sezione in componenti.get("sectionsEditorial") or []:
        if not isinstance(sezione, dict):
            continue
        if sezione.get("title"):
            righe += [f"## {str(sezione['title']).strip()}", ""]
        if sezione.get("text"):
            righe += [pulisci(sezione["text"]), ""]
        for componente in sezione.get("components") or []:
            righe += _componente(componente)
    testo = "\n".join(righe)
    return re.sub(r"\n{3,}", "\n\n", testo).strip() + "\n"


def testo_rst(sorgenti: list[tuple[str, bytes]]) -> str:
    parti = [f".. file: {nome}\n\n" + dati.decode("utf-8").replace("\r\n", "\n").rstrip() + "\n" for nome, dati in sorgenti]
    return "\n".join(parti)


def corpo_senza_intestazione(testo: str) -> str:
    return testo.split(FINE_INTESTAZIONE, 1)[1] if FINE_INTESTAZIONE in testo else testo


def versione_design_system(cartella: Path) -> str | None:
    percorso = cartella / VERSIONAMENTO
    if not percorso.is_file():
        return None
    testo = percorso.read_text(encoding="utf-8")
    m = re.search(r"Documentazione \(questo sito\).*?label:\s*\"?([\d.]+[\w.-]*)\"?", testo, re.S)
    return m.group(1) if m else None


def novita_design_system(cartella: Path, da_versione: str | None) -> list[str]:
    """Voci del changelog della documentazione più recenti della versione indicata (titolo e data)."""
    percorso = cartella / VERSIONAMENTO
    if not percorso.is_file() or not da_versione:
        return []
    voci = []
    for m in re.finditer(r"###\s+v([\d.]+)\s*\n\s*([^\n]+)", percorso.read_text(encoding="utf-8")):
        if _versione(m.group(1)) > _versione(da_versione):
            voci.append(f"v{m.group(1)} ({m.group(2).strip()})")
    return voci


def _versione(testo: str) -> tuple:
    return tuple(int(x) for x in re.findall(r"\d+", testo)[:3])


# ————————————————————————————————————————— glossario della Guida alle parole —————————————————————————————————————————

def _voce_pulita(riga: str) -> str:
    return re.sub(r"`([^<`]+?)\s*<[^>]+>`_+", r"\1", riga).strip()


def forme_della_voce(riga: str) -> list[str]:
    testo = _voce_pulita(riga).rstrip("?").strip()
    forme = []
    for parte in re.split(r"\s+/\s+|,\s*|\s+oppure\s+|\s+o\s+", testo):
        parte = parte.strip()
        if not parte:
            continue
        m = re.fullmatch(r"(.+?)\s*\((.+?)\)", parte)
        if not m:
            forme.append(parte)
            continue
        base, dentro = m.group(1).strip(), m.group(2).strip()
        forme.append(base)
        if (" " not in base and " " not in dentro) or re.fullmatch(r"[A-Z][A-Za-z]{1,5}", dentro):
            forme.append(dentro)
        else:
            forme.append(f"{base} {dentro}")
    visti, uniche = set(), []
    for forma in forme:
        if forma.lower() not in visti:
            visti.add(forma.lower())
            uniche.append(forma)
    return uniche


def leggi_glossario(testo: str) -> list[dict]:
    voci, corrente, modo, dentro = [], None, None, False
    righe = testo.splitlines()
    for indice, riga in enumerate(righe):
        m = re.match(r"\.\. file: (.+)$", riga)
        if m:
            nome = m.group(1).strip()
            dentro = "/" in nome and not nome.endswith("index.rst")
            corrente = None
            continue
        if not dentro or not riga.strip():
            continue
        pulita = riga.strip()
        rientro = len(riga) - len(riga.lstrip())
        seguente = next((r for r in righe[indice + 1:] if r.strip()), "")
        voce_rientrata = (0 < rientro < 4 and not pulita.startswith("..") and pulita != "|"
                          and len(seguente) - len(seguente.lstrip()) > rientro + 2)  # voce scritta con un rientro di troppo nel sorgente
        if not riga.startswith((" ", "\t")) or voce_rientrata:
            if re.fullmatch(r"[=\-~^\"'#*+]{2,}|[=]", pulita) or re.fullmatch(r"[A-Z]", pulita):
                continue
            corrente = {"voce": _voce_pulita(pulita), "forme": forme_della_voce(pulita), "nota": "", "va_bene": [], "non_va_bene": []}
            voci.append(corrente)
            modo = None
            continue
        if corrente is None:
            continue
        if pulita == "|":
            modo = None
            continue
        m = re.match(r"\.\.\s+admonition::\s*(\S+)", pulita)
        if m:
            modo = {"use": "va_bene", "use-not": "non_va_bene"}.get(m.group(1))
            continue
        if modo and rientro >= 8:
            corrente[modo].append(pulita.strip("*").strip())
            continue
        modo = None
        corrente["nota"] = (corrente["nota"] + " " + pulita).strip()
    return voci


# ————————————————————————————————————————— regole controllate dallo script —————————————————————————————————————————
# Ogni regola vale solo se le frasi di «conferma» si trovano ancora nel manuale: dopo un aggiornamento le regole
# che il manuale non dice più restano spente finché qualcuno non le rivede.

REGOLE = [
    # id, documento, sezione, conferme, regex del valore, gravità
    ("CONT-TITOLO", "fondamenti-contenuti", "Organizza le informazioni su pagina › Titoli",
     [r"i titoli devono essere chiari e descrittivi"], r"in massimo (\d+) caratteri", "correggere"),
    ("CONT-SOMMARIO-PRESENTE", "fondamenti-contenuti", "Sommari", [r"essere presente in tutte le pagine"], None, "valutare"),
    ("CONT-SOMMARIO-LUNGHEZZA", "fondamenti-contenuti", "Sommari", [r"il sommario dovrebbe"], r"non superare i (\d+) caratteri", "correggere"),
    ("CONT-SOMMARIO-PUNTO", "fondamenti-contenuti", "Sommari", [r"finire con il punto"], None, "correggere"),
    ("CONT-SOMMARIO-TITOLO", "fondamenti-contenuti", "Sommari", [r"non ripetere il contenuto del titolo"], None, "valutare"),
    ("CONT-PARAGRAFI", "fondamenti-contenuti", "Corpo di pagina", [r"i paragrafi non dovrebbero avere"], r"non dovrebbero avere più di (\d+) frasi", "valutare"),
    ("CONT-H1", "fondamenti-contenuti", "Intestazioni", [r"ogni titolo di pagina è un h1, quindi parti con gli h2"], None, "correggere"),
    ("CONT-LIVELLI", "fondamenti-contenuti", "Intestazioni", [r"in maniera ordinata"], r"livelli di intestazione \(da h2 a h(\d)\)", "correggere"),
    ("CONT-GRASSETTO-TITOLO", "fondamenti-contenuti", "Intestazioni", [r"non usare il grassetto come sostitutivo"], None, "valutare"),
    ("CONT-SOTTOELENCHI", "fondamenti-contenuti", "Elenchi puntati e numerati", [r"evita sottoelenchi puntati"], None, "valutare"),
    ("CONT-NUMERATI-PUNTO", "fondamenti-contenuti", "Elenchi puntati e numerati",
     [r"usa un elenco numerato quando devi guidare", r"mettere il punto fermo alla fine di ogni frase"], None, "valutare"),
    ("CONT-ELENCO-FRASE", "fondamenti-contenuti", "Elenchi puntati e numerati",
     [r"l'iniziale del punto elenco è minuscola e la frase si chiude col punto e virgola"], None, "valutare"),
    ("CONT-LINK", "fondamenti-contenuti", "Link", [r"assicurati che sia chiara la destinazione di ogni link"], None, "correggere"),
    ("CONT-ALT", "fondamenti-contenuti", "Immagini e video", [r"includere alt-text per le immagini"], None, "correggere"),
    ("LING-SIGLE", "fondamenti-linguaggio", "Acronimi e sigle", [r"nome completo per esteso seguito dall'acronimo tra parentesi"], None, "valutare"),
    ("LING-NORME", "fondamenti-linguaggio", "Riferimenti normativi", [r"aggiungi sempre il link alla norma di riferimento"], None, "valutare"),
    ("LING-ATTIVI", "fondamenti-linguaggio", "Linguaggio semplice e naturale", [r"forme verbali attive", r"evitando nominalizzazioni"], None, "valutare"),
    ("LING-GRASSETTO", "fondamenti-linguaggio", "Grassetto", [r"evidenziare parole chiave e non frasi intere"], None, "valutare"),
    ("LING-SOTTOLINEATO", "fondamenti-linguaggio", "Testo sottolineato", [r"non usare testo sottolineato"], None, "correggere"),
    ("LING-GIUSTIFICATO", "fondamenti-linguaggio", "Allineamento", [r"allinea sempre il testo a sinistra"], None, "correggere"),
    ("LING-MAIUSCOLO", "fondamenti-linguaggio", "Uso delle maiuscole", [r"usa il maiuscolo soltanto per la prima lettera della frase"], None, "valutare"),
    ("LING-MIGLIAIA", "fondamenti-linguaggio", "Numeri", [r"usa il punto per separare le migliaia a partire dai 10 mila in su"], None, "valutare"),
    ("LING-DECIMALI", "fondamenti-linguaggio", "Numeri", [r"usa la virgola per separare i decimali"], None, "correggere"),
    ("LING-DATE", "fondamenti-linguaggio", "Date",
     [r"scrivi i giorni del mese e l'anno in cifre, mentre scrivi il mese", r"in lettere \(con l'iniziale minuscola\)"], None, "correggere"),
    ("LING-ORARI", "fondamenti-linguaggio", "Orari", [r"separa ore e minuti con i due punti"], None, "correggere"),
    ("LING-TELEFONO", "fondamenti-linguaggio", "Numeri di telefono",
     [r"usa sempre anche il prefisso internazionale", r"numeri di telefono come link attivi"], None, "valutare"),
    ("LING-EMAIL", "fondamenti-linguaggio", "Email", [r"la parola \"email\" si scrive senza trattini o spazi, in minuscolo"], None, "correggere"),
    ("LING-EMAIL-LINK", "fondamenti-linguaggio", "Email", [r"link attivi usando l'attributo mailto:"], None, "valutare"),
    ("LING-UNITA", "fondamenti-linguaggio", "Unità di misura", [r"seguito dal simbolo dell'unità di misura", r"separato da uno spazio"], None, "correggere"),
    ("INCL-VEDI", "fondamenti-linguaggio", "Inclusività", [r"non usare: verbi abilisti", r"vedi / leggi"], None, "valutare"),
    ("INCL-MASCHILE", "fondamenti-linguaggio", "Inclusività", [r"maschile sovresteso", r"benvenuto, rimani aggiornato"], None, "valutare"),
    ("INCL-DISABILI", "fondamenti-linguaggio", "Inclusività", [r"persone con disabilità \| disabili"], None, "valutare"),
    ("INCL-CLANDESTINI", "fondamenti-linguaggio", "Inclusività", [r"clandestini"], None, "valutare"),
    ("TONO-TU", "fondamenti-tono-di-voce", "Rivolgiti a chi legge con il \"tu\"",
     [r"parla all'interlocutore in modo diretto usando il \"tu\"", r"quanto la forma impersonale"], None, "valutare"),
    ("MICRO-CTA", "fondamenti-microtesti", "Usa azioni specifiche", [r"inizia le call-to-action con un verbo"], None, "valutare"),
    ("MICRO-CONFERMA", "fondamenti-microtesti", "Chiedi conferma prima di azioni importanti",
     [r"evitando generici \"attenzione!\" o \"sei sicuro di voler"], None, "valutare"),
    ("PAROLE-EURO", "guida-parole-pa", "Euro, euri, EUR, €", [r"nei contenuti testuali, usa la forma estesa", r"nelle tabelle, usa il simbolo"], None, "valutare"),
    ("PAROLE-GLOSSARIO", "guida-parole-pa", "Glossario", [r"glossario"], None, "valutare"),
    ("LG-AGGIORNAMENTO", "linee-guida-design", "Semplicità di consultazione ed esperienza d'uso",
     [r"si dovrebbe pubblicare, su ogni pagina del sito internet, la data dell'ultimo aggiornamento"], None, "nota"),
    ("LEGGIBILITA", "fondamenti-linguaggio", "Ricerca e testa il linguaggio del tuo servizio", [r"indice gulpease"], None, "nota"),
]
TITOLI_DOC = {d["id"]: d["titolo"].split(": ", 1)[-1] for d in DOCUMENTI}
TITOLI_DOC["guida-parole-pa"] = "Guida alle parole della PA"
TITOLI_DOC["linee-guida-design"] = "Linee guida di design AgID"


def normalizza(testo: str) -> str:
    t = testo.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace(" ", " ")
    t = t.replace("**", "").replace("`", "")
    t = re.sub(r"(?<![\w*])\*(?!\s)([^*\n]+?)\*(?!\w)", r"\1", t)
    return re.sub(r"\s+", " ", t).lower()


def conferma_regole(cartella: Path) -> dict:
    testi = {}
    risultato = {}
    for rid, doc, sezione, conferme, valore_re, gravita in REGOLE:
        if doc not in testi:
            percorso = cartella / PER_ID[doc]["uscita"]
            testi[doc] = normalizza(percorso.read_text(encoding="utf-8")) if percorso.is_file() else ""
        testo = testi[doc]
        confermata = bool(testo) and all(re.search(c, testo) for c in conferme)
        valore = None
        if confermata and valore_re:
            m = re.search(valore_re, testo)
            if m:
                valore = int(m.group(1))
            else:
                confermata = False
        risultato[rid] = {"confermata": confermata, "valore": valore, "documento": doc, "sezione": sezione, "gravita": gravita}
    return risultato


# ————————————————————————————————————————— lettura di una pagina Markdown —————————————————————————————————————————

RE_ELENCO = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
RE_TITOLO = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
RE_LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]*)(?:\s+\"[^\"]*\")?\)")
RE_IMMAGINE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)")
RE_IMMAGINE_INTERA = re.compile(r"!\[[^\]]*\]\([^)]*\)")
RE_FIGURA = re.compile(r"\{\{[<%]\s*figure\b(.*?)[>%]\}\}")
RE_IMG_HTML = re.compile(r"<img\b[^>]*>", re.I)
RE_TELEFONO = re.compile(r"(?<![\w+/.])(\+39[\s.]?)?((?:0\d{1,3}|3\d{2})[\s./-]?\d{2,4}[\s./-]?\d{2,4}(?:[\s./-]?\d{1,4})?)(?![\w/])")
MESI = "gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre"
GIORNI = "lunedì|martedì|mercoledì|giovedì|venerdì|sabato|domenica"
PAROLE_FUNZIONE = {"Di", "Da", "Del", "Della", "Dello", "Dei", "Degli", "Delle", "Con", "Per", "In", "Il", "Lo", "La", "Le", "Gli", "I", "Un",
                   "Una", "Al", "Alla", "Ai", "Alle", "Nel", "Nella", "Nei", "Nelle", "Sul", "Sulla", "Sui", "E", "O", "Tra", "Fra", "A"}
LINK_VAGHI = {"qui", "clicca qui", "clicca", "link", "questo link", "a questo link", "leggi qui", "qui sotto", "click", "clicca sul link", "vai",
              "scopri di più qui", "premi qui"}


def _valore_fm(valore: str) -> str:
    valore = valore.strip()
    if len(valore) >= 2 and valore[0] == valore[-1] == "'":
        return valore[1:-1].replace("''", "'")
    if len(valore) >= 2 and valore[0] == valore[-1] == '"':
        return valore[1:-1].replace('\\"', '"')
    return valore


def leggi_pagina(testo: str) -> dict:
    righe = testo.replace("\r\n", "\n").split("\n")
    front, righe_front, inizio = {}, {}, 0
    if righe and righe[0].strip() in ("---", "+++"):
        delimitatore = righe[0].strip()
        for i in range(1, len(righe)):
            if righe[i].strip() == delimitatore:
                inizio = i + 1
                break
            m = re.match(r"^([A-Za-z_][\w-]*)\s*[:=]\s*(.*)$", righe[i])
            if m and not righe[i].startswith((" ", "\t")):
                front[m.group(1).lower()] = _valore_fm(m.group(2))
                righe_front[m.group(1).lower()] = i + 1
    corpo, in_codice, in_commento = [], False, False
    for n in range(inizio, len(righe)):
        riga = righe[n]
        if re.match(r"^\s*(```|~~~)", riga):
            in_codice = not in_codice
            corpo.append((n + 1, ""))
            continue
        if in_codice:
            corpo.append((n + 1, ""))
            continue
        if in_commento:
            if "-->" in riga:
                in_commento = False
                riga = riga.split("-->", 1)[1]
            else:
                corpo.append((n + 1, ""))
                continue
        riga = re.sub(r"<!--.*?-->", "", riga)
        if "<!--" in riga:
            riga, in_commento = riga.split("<!--", 1)[0], True
        corpo.append((n + 1, riga))
    return {"front": front, "righe_front": righe_front, "corpo": corpo}


def visibile(riga: str) -> str:
    """Il testo che legge una persona: senza indirizzi dei link, codice, tag, shortcode e segni di formattazione."""
    t = RE_IMMAGINE_INTERA.sub(" ", riga)
    t = re.sub(r"\{\{[<%].*?[>%]\}\}", " ", t)
    t = RE_LINK.sub(lambda m: m.group(1), t)
    t = re.sub(r"`[^`]*`", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"^\s*(#{1,6}\s+|[-*+]\s+|\d+[.)]\s+|>\s*|\|)", "", t)
    return t.replace("**", "").replace("__", "")


def inizio_frase(testo: str, posizione: int) -> bool:
    prima = re.sub(r"^\s*(?:#{1,6}\s+|[-*+]\s+|\d+[.)]\s+|>\s*)*", "", testo[:posizione])
    prima = prima.rstrip(" \t*_«\"“'(")
    return prima == "" or prima.endswith((".", "!", "?", ":", "…", "|"))


def blocchi(corpo: list[tuple[int, str]]) -> dict:
    """Divide il corpo in titoli, elenchi, paragrafi e tabelle."""
    titoli, voci, paragrafi, tabelle = [], [], [], []
    paragrafo, ultima_non_vuota = [], ""
    for numero, riga in corpo:
        if not riga.strip():
            if paragrafo:
                paragrafi.append(paragrafo)
                paragrafo = []
            continue
        m_titolo = RE_TITOLO.match(riga)
        m_voce = RE_ELENCO.match(riga)
        if m_titolo:
            if paragrafo:
                paragrafi.append(paragrafo)
                paragrafo = []
            titoli.append((numero, len(m_titolo.group(1)), m_titolo.group(2)))
        elif m_voce:
            if paragrafo:
                paragrafi.append(paragrafo)
                paragrafo = []
            voci.append({"riga": numero, "rientro": len(m_voce.group(1).replace("\t", "    ")), "numerata": m_voce.group(2)[0].isdigit(),
                         "testo": m_voce.group(3), "introduzione": ultima_non_vuota})
        elif riga.lstrip().startswith("|"):
            tabelle.append(numero)
        elif voci and voci[-1]["riga"] == numero - 1 and riga.startswith((" ", "\t")):
            voci[-1]["testo"] += " " + riga.strip()
        elif not re.match(r"^\s*(\{\{[<%].*[>%]\}\}\s*)+$", riga) and not re.match(r"^\s*</?\w+[^>]*>\s*$", riga) and not riga.lstrip().startswith(">"):
            paragrafo.append((numero, riga))
        ultima_non_vuota = riga
    if paragrafo:
        paragrafi.append(paragrafo)
    return {"titoli": titoli, "voci": voci, "paragrafi": paragrafi, "tabelle": set(tabelle)}


def conta_frasi(testo: str) -> int:
    testo = re.sub(r"\b(art|artt|n|nn|ecc|etc|lett|pag|pagg|sig|dott|prof|ing|avv|geom|c\.a|d\.lgs|d\.l|p\.es)\.", lambda m: m.group(0)[:-1], testo, flags=re.I)
    pezzi = [p for p in re.split(r"(?<=[.!?…])\s+(?=[A-ZÀ-Ý«\"“(0-9])", testo.strip()) if re.search(r"\w", p)]
    return len(pezzi)


def gulpease(testo: str) -> dict | None:
    parole = re.findall(r"[A-Za-zÀ-ÿ']+", testo)
    if len(parole) < 20:
        return None
    lettere = sum(1 for c in testo if c.isalpha())
    frasi = max(1, len([p for p in re.split(r"[.!?…]+", testo) if re.search(r"\w", p)]))
    valore = 89 + (300 * frasi - 10 * lettere) / len(parole)
    return {"valore": round(max(0.0, min(100.0, valore)), 1), "parole": len(parole), "frasi": frasi}


def romano(parola: str) -> bool:
    return bool(re.fullmatch(r"M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})", parola))


# ————————————————————————————————————————— controllo di un testo —————————————————————————————————————————

def controlla_testo(testo: str, regole: dict, glossario: list[dict]) -> dict:
    pagina = leggi_pagina(testo)
    front, corpo = pagina["front"], pagina["corpo"]
    parti = blocchi(corpo)
    segnalazioni = []

    def attiva(rid):
        return regole.get(rid, {}).get("confermata", False)

    def segnala(rid, riga, messaggio, gravita=None):
        info = regole.get(rid, {})
        segnalazioni.append({"riga": riga, "regola": rid, "gravita": gravita or info.get("gravita", "valutare"), "messaggio": messaggio,
                             "fonte": f"{TITOLI_DOC.get(info.get('documento', ''), '')} › {info.get('sezione', '')}"})

    titolo = front.get("title", "")
    sommario = front.get("description") or front.get("summary") or front.get("sommario") or ""
    chiave_sommario = next((k for k in ("description", "summary", "sommario") if front.get(k)), "description")
    riga_titolo = pagina["righe_front"].get("title", 1)
    riga_sommario = pagina["righe_front"].get(chiave_sommario, 1)
    prosa = []  # (riga, testo visibile, è tabella)
    if titolo:
        prosa.append((riga_titolo, titolo, False))
    if sommario:
        prosa.append((riga_sommario, sommario, False))
    for numero, riga in corpo:
        if riga.strip():
            prosa.append((numero, visibile(riga), numero in parti["tabelle"]))

    # Contenuti: titolo e sommario
    if front:
        if titolo and attiva("CONT-TITOLO") and len(titolo) > regole["CONT-TITOLO"]["valore"]:
            segnala("CONT-TITOLO", riga_titolo, f"titolo di {len(titolo)} caratteri: il massimo è {regole['CONT-TITOLO']['valore']}")
        if not sommario and attiva("CONT-SOMMARIO-PRESENTE"):
            segnala("CONT-SOMMARIO-PRESENTE", 1, "manca il sommario (campo description nel front matter): deve esserci in tutte le pagine")
        if sommario:
            if attiva("CONT-SOMMARIO-LUNGHEZZA") and len(sommario) > regole["CONT-SOMMARIO-LUNGHEZZA"]["valore"]:
                segnala("CONT-SOMMARIO-LUNGHEZZA", riga_sommario,
                        f"sommario di {len(sommario)} caratteri: il massimo è {regole['CONT-SOMMARIO-LUNGHEZZA']['valore']}")
            if attiva("CONT-SOMMARIO-PUNTO") and not sommario.rstrip().endswith("."):
                segnala("CONT-SOMMARIO-PUNTO", riga_sommario, "il sommario deve finire con il punto")
            if titolo and attiva("CONT-SOMMARIO-TITOLO"):
                a, b = titolo.lower().strip(" ."), sommario.lower().strip(" .")
                if a in b or b in a:
                    segnala("CONT-SOMMARIO-TITOLO", riga_sommario, "il sommario ripete il titolo: aggiungi informazioni nuove")
        if attiva("LG-AGGIORNAMENTO") and not any(k in front for k in ("lastmod", "ultimo_aggiornamento", "modified")):
            segnala("LG-AGGIORNAMENTO", 1, "nessuna data di ultimo aggiornamento (in Hugo il campo lastmod, se il tema la mostra): "
                                            "le Linee guida dicono che SI DOVREBBE pubblicarla su ogni pagina")

    # Contenuti: intestazioni
    precedente = 1
    for numero, livello, testo_titolo in parti["titoli"]:
        if livello == 1 and attiva("CONT-H1"):
            segnala("CONT-H1", numero, "intestazione H1 nel corpo: il titolo della pagina è già l'H1, parti dagli H2 (##)")
        elif attiva("CONT-LIVELLI"):
            massimo = regole["CONT-LIVELLI"]["valore"]
            if livello > massimo:
                segnala("CONT-LIVELLI", numero, f"intestazione H{livello}: usa i livelli da H2 a H{massimo}")
            elif livello > precedente + 1 and livello > 2:
                segnala("CONT-LIVELLI", numero, f"salto da H{precedente} a H{livello}: usa i livelli in ordine")
        precedente = max(livello, 2) if livello >= 2 else 2
    if attiva("CONT-GRASSETTO-TITOLO"):
        for numero, riga in corpo:
            if re.fullmatch(r"\s*(\*\*|__)[^*_]{2,80}(\*\*|__)\s*:?\s*", riga):
                segnala("CONT-GRASSETTO-TITOLO", numero, "riga tutta in grassetto usata come titoletto: usa un'intestazione (## o ###)")

    # Contenuti: paragrafi
    if attiva("CONT-PARAGRAFI"):
        massimo = regole["CONT-PARAGRAFI"]["valore"]
        for paragrafo in parti["paragrafi"]:
            n = conta_frasi(" ".join(visibile(r) for _, r in paragrafo))
            if n > massimo:
                segnala("CONT-PARAGRAFI", paragrafo[0][0], f"paragrafo di {n} frasi: al massimo {massimo}, dividilo o usa un elenco")

    # Contenuti: elenchi
    voci = parti["voci"]
    if attiva("CONT-SOTTOELENCHI"):
        for i, voce in enumerate(voci):
            if voce["rientro"] >= 2 and i > 0 and voci[i - 1]["riga"] < voce["riga"] and not voce["numerata"]:
                segnala("CONT-SOTTOELENCHI", voce["riga"], "sottoelenco: evita gli elenchi dentro gli elenchi, crea piuttosto un nuovo elenco")
                break
    gruppi, gruppo = [], []
    for voce in voci:
        if gruppo and (voce["riga"] - gruppo[-1]["riga"] > 2 or voce["numerata"] != gruppo[-1]["numerata"] or voce["rientro"] != gruppo[-1]["rientro"]):
            gruppi.append(gruppo)
            gruppo = []
        gruppo.append(voce)
    if gruppo:
        gruppi.append(gruppo)
    for gruppo in gruppi:
        testi = [visibile("- " + v["testo"]).strip() for v in gruppo]
        if gruppo[0]["numerata"] and attiva("CONT-NUMERATI-PUNTO"):
            senza = [v["riga"] for v, t in zip(gruppo, testi) if t and not re.search(r"[.!?][\"”»)]?$", t)]
            if senza:
                segnala("CONT-NUMERATI-PUNTO", senza[0], f"elenco numerato: metti il punto fermo alla fine di ogni passo (righe {', '.join(map(str, senza))})")
        if not gruppo[0]["numerata"] and attiva("CONT-ELENCO-FRASE") and visibile(gruppo[0]["introduzione"]).rstrip().endswith(":"):
            problemi = []
            for indice, (voce, t) in enumerate(zip(gruppo, testi)):
                ultimo = indice == len(gruppo) - 1
                if t[:1].isupper() and not re.match(r"[A-Z]{2,}", t):
                    problemi.append(f"riga {voce['riga']} iniziale maiuscola")
                if not ultimo and not t.endswith(";"):
                    problemi.append(f"riga {voce['riga']} senza punto e virgola")
                if ultimo and not t.endswith("."):
                    problemi.append(f"riga {voce['riga']} senza punto finale")
            if problemi:
                segnala("CONT-ELENCO-FRASE", gruppo[0]["riga"], "elenco che continua la frase introduttiva (finisce con i due punti): "
                        "voci con l'iniziale minuscola, punto e virgola, punto all'ultima; " + "; ".join(problemi[:4]))

    # Contenuti: link e immagini
    for numero, riga in corpo:
        for m in RE_LINK.finditer(riga):
            testo_link = re.sub(r"[*_`]", "", m.group(1)).strip()
            semplice = testo_link.lower().strip(" .:!»«\"")
            if attiva("CONT-LINK") and semplice in LINK_VAGHI:
                segnala("CONT-LINK", numero, f"link «{testo_link}»: il testo deve dire dove porta (per esempio «Scarica il modulo di iscrizione»)")
            elif attiva("CONT-LINK") and re.match(r"https?://|www\.", testo_link):
                segnala("CONT-LINK", numero, "il testo del link è un indirizzo: scrivi dove porta", "valutare")
            if attiva("MICRO-CTA") and semplice in ("ok", "si", "sì", "conferma?"):
                segnala("MICRO-CTA", numero, f"«{testo_link}»: le call-to-action iniziano con un verbo che dice l'azione (Invia, Iscriviti)")
            if attiva("INCL-VEDI") and re.match(r"(vedi|leggi)\b", semplice):
                segnala("INCL-VEDI", numero, f"«{testo_link}»: verbo abilista, usa «Scopri», «Vai a», «Approfondisci»")
        if attiva("CONT-ALT"):
            for m in RE_IMMAGINE.finditer(riga):
                if not m.group(1).strip():
                    segnala("CONT-ALT", numero, "immagine senza testo alternativo: scrivi cosa mostra tra le parentesi quadre")
            for m in RE_FIGURA.finditer(riga):
                alt = re.search(r"\balt\s*=\s*(\"([^\"]*)\"|'([^']*)')", m.group(1))
                if not alt or not (alt.group(2) or alt.group(3) or "").strip():
                    segnala("CONT-ALT", numero, "shortcode figure senza alt: aggiungi alt=\"…\" con cosa mostra l'immagine")
            for m in RE_IMG_HTML.finditer(riga):
                alt = re.search(r"\balt\s*=\s*(\"([^\"]*)\"|'([^']*)')", m.group(0))
                if not alt or not (alt.group(2) or alt.group(3) or "").strip():
                    segnala("CONT-ALT", numero, "immagine HTML senza alt")
        if attiva("LING-SOTTOLINEATO") and re.search(r"<u>|text-decoration\s*:\s*underline", riga, re.I):
            segnala("LING-SOTTOLINEATO", numero, "testo sottolineato: si sottolineano solo i link")
        if attiva("LING-GIUSTIFICATO") and re.search(r"text-align\s*:\s*justify|text-justify", riga, re.I):
            segnala("LING-GIUSTIFICATO", numero, "testo giustificato: allinea sempre a sinistra")
        if attiva("LING-GRASSETTO"):
            for m in re.finditer(r"\*\*([^*]+)\*\*|__([^_]+)__", riga):
                parole = len(re.findall(r"\w+", m.group(1) or m.group(2)))
                if parole > 6 and not re.fullmatch(r"\s*(\*\*|__).+(\*\*|__)\s*:?\s*", riga):
                    segnala("LING-GRASSETTO", numero, f"grassetto su {parole} parole: usalo solo per parole chiave, non per frasi intere")
        if attiva("LING-TELEFONO"):
            collegati = {re.sub(r"\D", "", m.group(2)) for m in RE_LINK.finditer(riga) if m.group(2).lower().startswith("tel:")}
            for m in RE_TELEFONO.finditer(visibile(riga)):
                cifre = re.sub(r"\D", "", m.group(2))
                if not 8 <= len(cifre) <= 11:
                    continue
                problemi = []
                if not m.group(1):
                    problemi.append("senza prefisso +39")
                if not any(c.endswith(cifre) for c in collegati):
                    problemi.append("non collegato come link telefonico")
                if problemi:
                    segnala("LING-TELEFONO", numero, f"numero «{m.group(0).strip()}» {' e '.join(problemi)}; per esempio "
                                                     "[+39 06 123 456 78](tel:+390612345678)")
        if attiva("LING-EMAIL-LINK"):
            dentro_link = {m.group(2)[7:].lower() for m in RE_LINK.finditer(riga) if m.group(2).lower().startswith("mailto:")}
            dentro_link |= {m.group(1).lower() for m in re.finditer(r"<(?:mailto:)?([\w.+-]+@[\w-]+(?:\.[\w-]+)+)>", riga)}
            for m in re.finditer(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", re.sub(r"\]\(mailto:[^)]*\)", "]", riga)):
                if m.group(0).lower() not in dentro_link:
                    segnala("LING-EMAIL-LINK", numero, f"indirizzo {m.group(0)} non collegato: [{m.group(0)}](mailto:{m.group(0)})")

    # Testo visibile: date, orari, numeri, parole
    sigle_viste = set()
    for numero, testo_riga, in_tabella in prosa:
        telefoni = [m.span() for m in RE_TELEFONO.finditer(testo_riga) if 8 <= len(re.sub(r"\D", "", m.group(2))) <= 11]
        if attiva("LING-DATE"):
            for m in re.finditer(r"(?<![\d/.-])(0?[1-9]|[12]\d|3[01])([/.-])(0?[1-9]|1[0-2])\2(\d{4}|\d{2})(?![\d/.-])", testo_riga):
                segnala("LING-DATE", numero, f"data «{m.group(0)}» in cifre: il mese va in lettere (per esempio 25 gennaio 2018)")
            for m in re.finditer(rf"\b({MESI}|{GIORNI})\b", testo_riga, re.I):
                if m.group(0)[0].isupper() and not inizio_frase(testo_riga, m.start()):
                    segnala("LING-DATE", numero, f"«{m.group(0)}»: mesi e giorni della settimana con l'iniziale minuscola")
        if attiva("LING-ORARI"):
            for m in re.finditer(r"\b(?:ore|alle|dalle|entro le|fino alle|verso le|dopo le|prima delle|tra le|e le|h\.?)\s+(?:([01]?\d|2[0-3])[.,]([0-5]\d))\b",
                                 testo_riga, re.I):
                segnala("LING-ORARI", numero, f"orario «{m.group(1)}.{m.group(2)}»: ore e minuti con i due punti ({m.group(1)}:{m.group(2)})")
            for m in re.finditer(r"(?<![\d.,])([01]?\d|2[0-3])[.]([0-5]\d)\s?[-–]\s?([01]?\d|2[0-3])[.:]([0-5]\d)(?![\d.])", testo_riga):
                segnala("LING-ORARI", numero, f"orario «{m.group(0)}»: ore e minuti con i due punti, senza spazi ({m.group(1)}:{m.group(2)})")
        if attiva("LING-DECIMALI"):
            for m in re.finditer(r"(?<![\d.,])(\d+)\.(\d{1,2})\s?(km/h|km|kg|cm|mm|m|g|l|ml|ha|°C|%|euro|€|hPa|kW|MHz)(?![\w/])", testo_riga):
                segnala("LING-DECIMALI", numero, f"«{m.group(0)}»: decimali con la virgola ({m.group(1)},{m.group(2)})")
        if attiva("LING-MIGLIAIA"):
            for m in re.finditer(r"(?<![\d.,/+])([1-9])\.(\d{3})(?![\d.,/])", testo_riga):
                if not re.match(r"\s?(ore|h\b)", testo_riga[m.end():]):
                    segnala("LING-MIGLIAIA", numero, f"«{m.group(0)}»: sotto i 10 mila senza punto ({m.group(1)}{m.group(2)})")
            for m in re.finditer(r"(?<![\d.,/+])([1-9]\d{4,7})(?![\d.,/])", testo_riga):
                prima = testo_riga[max(0, m.start() - 12):m.start()].lower()
                if any(a <= m.start() < b for a, b in telefoni):
                    continue
                if not re.search(r"(cap|n\.|nr\.?|prot\.?|codice|cod\.|protocollo|tel\.?)\s*$", prima):
                    cifre = m.group(1)
                    gruppi = f"{int(cifre):,}".replace(",", ".")
                    segnala("LING-MIGLIAIA", numero, f"«{cifre}»: da 10 mila in su usa il punto per le migliaia ({gruppi})")
        if attiva("LING-UNITA"):
            for m in re.finditer(r"(?<![\w.,])(\d+(?:[.,]\d+)?)(km/h|km|kg|cm|mm|m|g|ml|kW|MHz|GHz|hPa)(?![\w/])", testo_riga):
                segnala("LING-UNITA", numero, f"«{m.group(0)}»: tra numero e unità di misura uno spazio ({m.group(1)} {m.group(2)})")
            for m in re.finditer(r"(?<![\d.,])(\d+(?:[.,]\d+)?)(°\s?C|\s°\s+C)\b", testo_riga):
                segnala("LING-UNITA", numero, f"«{m.group(0)}»: scrivi «{m.group(1)} °C»")
        if attiva("LING-EMAIL"):
            for m in re.finditer(r"\b[Ee][-\s][Mm]ail\b", testo_riga):
                segnala("LING-EMAIL", numero, f"«{m.group(0)}»: si scrive «email», senza trattino e in minuscolo")
            for m in re.finditer(r"\bE(?:mail|MAIL)\b", testo_riga):
                if not inizio_frase(testo_riga, m.start()):
                    segnala("LING-EMAIL", numero, f"«{m.group(0)}»: «email» in minuscolo")
        if attiva("PAROLE-EURO"):
            if not in_tabella and re.search(r"\d\s?€|€\s?\d|\bEUR\b", testo_riga):
                segnala("PAROLE-EURO", numero, "nel testo usa la forma estesa (per esempio «250 euro»): il simbolo € solo nelle tabelle")
            if in_tabella and re.search(r"€\s?\d|\d€", testo_riga):
                segnala("PAROLE-EURO", numero, "nelle tabelle il simbolo va dopo la cifra, separato da uno spazio (250 €)")
        if attiva("LING-NORME") and re.search(r"\b(d\.\s?lgs\.?|d\.\s?l\.|decreto legislativo|decreto[- ]legge|legge (n\.\s*)?\d|l\.\s*\d+/\d{2,4}|"
                                               r"d\.?p\.?r\.?\s|regolamento \(ue\)|art\.\s*\d+|articolo \d+)", testo_riga, re.I):
            riga_originale = next((r for n, r in corpo if n == numero), "")
            if "](http" not in riga_originale:
                segnala("LING-NORME", numero, "riferimento a una norma senza link: spiega cosa dice e collega il testo (per esempio su Normattiva)")
        if attiva("LING-ATTIVI"):
            for m in re.finditer(r"\bsi (?:è|sono) (?:provveduto|proceduto|deciso di procedere)\b|\bsi provvederà\b|\b(?:è|sono) stat[oaie] effettuat[oaie]\b",
                                 testo_riga, re.I):
                segnala("LING-ATTIVI", numero, f"«{m.group(0)}»: usa un verbo attivo con il soggetto vero")
        if attiva("TONO-TU"):
            for m in re.finditer(r"\bsi (?:prega|pregano|invita|invitano|informa|informano|comunica|ricorda|avvisa|rende noto|raccomanda)\b", testo_riga, re.I):
                segnala("TONO-TU", numero, f"«{m.group(0)}»: forma impersonale, rivolgiti a chi legge con il «tu» (per esempio «Ti ricordiamo che…»)")
            for m in re.finditer(r"\b(?:La|Le|Vi|vi) (?:invitiamo|preghiamo|ricordiamo|informiamo|chiediamo|comunichiamo|ringraziamo|aspettiamo)\b", testo_riga):
                segnala("TONO-TU", numero, f"«{m.group(0)}»: il manuale chiede di dare del «tu» a chi legge")
        if attiva("INCL-MASCHILE"):
            for m in re.finditer(r"\bbenvenut[oi]\b|\b(?:rimani|resta|restate|rimanete) aggiornat[oi]\b", testo_riga, re.I):
                proposta = "Ti diamo il benvenuto" if "benvenut" in m.group(0).lower() else "Ricevi aggiornamenti"
                segnala("INCL-MASCHILE", numero, f"«{m.group(0)}»: maschile sovraesteso, usa «{proposta}»")
        if attiva("INCL-DISABILI"):
            for m in re.finditer(r"\bdisabili\b", testo_riga, re.I):
                segnala("INCL-DISABILI", numero, "«disabili»: scrivi «persone con disabilità»")
        if attiva("INCL-CLANDESTINI"):
            for m in re.finditer(r"\bclandestin[io]\b", testo_riga, re.I):
                segnala("INCL-CLANDESTINI", numero, f"«{m.group(0)}»: denominazione scorretta, scrivi «persone»")
        if attiva("MICRO-CONFERMA"):
            for m in re.finditer(r"\bAttenzione!|\bSei sicur[oa] di\b", testo_riga, re.I):
                segnala("MICRO-CONFERMA", numero, f"«{m.group(0)}»: nelle conferme scrivi «Vuoi + verbo?» (per esempio «Vuoi annullare la pratica?»)")
        if attiva("LING-MAIUSCOLO"):
            for m in re.finditer(r"\b[A-ZÀ-Ý]{2,}(?:['’][A-ZÀ-Ý]+)?(?:[ \t]+[A-ZÀ-Ý]{2,}(?:['’][A-ZÀ-Ý]+)?)+\b|\b[A-ZÀ-Ý]{7,}\b", testo_riga):
                if max(len(p) for p in re.findall(r"[A-ZÀ-Ý]+", m.group(0))) >= 4:
                    segnala("LING-MAIUSCOLO", numero, f"«{m.group(0)}» in maiuscolo: è difficile da leggere, usa la maiuscola solo all'inizio della frase")
            parole = re.findall(r"[A-Za-zÀ-ÿ]+", testo_riga)
            if len(parole) >= 4 and any(p in PAROLE_FUNZIONE for p in parole[1:]) and (numero == riga_titolo and testo_riga == titolo
                                                                                        or any(t[0] == numero for t in parti["titoli"])):
                segnala("LING-MAIUSCOLO", numero, "titolo con le iniziali maiuscole: maiuscola solo alla prima parola (e ai nomi propri)")
        if attiva("LING-SIGLE"):
            for m in re.finditer(r"(?<![\w.])([A-Z]{2,6})(?![\w.])", testo_riga):
                sigla = m.group(1)
                if sigla in sigle_viste or romano(sigla) or sigla == "OK" or any(sigla.lower() == f.lower() for v in glossario for f in v["forme"]):
                    continue
                if re.search(r"[A-ZÀ-Ý]{2,}['’]?\s*$", testo_riga[:m.start()]) or re.match(r"\s*[A-ZÀ-Ý]{2,}", testo_riga[m.end():]):
                    continue  # parola di una frase tutta in maiuscolo: la segnala LING-MAIUSCOLO
                sigle_viste.add(sigla)
                dintorno = testo_riga[max(0, m.start() - 1):m.end() + 1]
                if not (dintorno.startswith("(") and dintorno.endswith(")")):
                    segnala("LING-SIGLE", numero, f"sigla «{sigla}» senza il nome per esteso alla prima volta: scrivi «nome per esteso ({sigla})»")
    if attiva("PAROLE-GLOSSARIO"):
        segnalazioni += controlla_glossario(prosa, glossario, regole["PAROLE-GLOSSARIO"])

    risultato = {"segnalazioni": sorted(segnalazioni, key=lambda s: ({"correggere": 0, "valutare": 1, "nota": 2}[s["gravita"]], s["riga"]))}
    if attiva("LEGGIBILITA"):
        prosa_lunga = " ".join(visibile(r) for p in parti["paragrafi"] for _, r in p) + " " + " ".join(visibile("- " + v["testo"]) for v in voci)
        risultato["gulpease"] = gulpease(prosa_lunga)
    return risultato


CASO_NOTA = re.compile(r"maiuscol|minuscol|iniziale|iniziali|\bsi scrive\b", re.I)
SUGG_NOTA = re.compile(r"preferisci|usa invece|limita|non abusare|non usare|evita|meglio|più semplic|scrivil|parla semplicemente|preferibile|"
                       r"termini italiani|termini? in italiano|equivalente italiano|forma italiana|l[’']italiano\s+[“\"]|dovrebbe essere sostituit|"
                       r"dicitura completa", re.I)
ESTESO_NOTA = re.compile(r"\bscrivil\w*\s+per esteso|solo dopo aver|dicitura completa|uso esteso|dicitura per esteso", re.I)


def tipo_nota(nota: str) -> tuple[bool, bool, bool]:
    """Che cosa chiede la nota della Guida: grafia (maiuscole e minuscole), un consiglio sulla parola, il nome per esteso."""
    frasi = re.split(r"(?<=[.!?])\s+", nota)
    caso = any(CASO_NOTA.search(f) for f in frasi)
    consiglio = any(SUGG_NOTA.search(f) and not CASO_NOTA.search(f) for f in frasi)
    esteso = any(ESTESO_NOTA.search(f) for f in frasi)
    return caso, consiglio or esteso, esteso


def _grafia_sbagliata(scritto: str, forma: str, testo: str, inizio: int, fine: int, nota: str) -> bool:
    if scritto == forma:
        return False
    a_inizio = inizio_frase(testo, inizio)
    if " " in forma:
        return not (a_inizio and scritto[1:] == forma[1:])
    if forma.islower():
        if "nome completo" in nota and re.match(r"\s+[A-ZÀ-Ý][a-zà-ÿ']+\s+[A-ZÀ-Ý][a-zà-ÿ']+", testo[fine:]):
            return False  # per esempio «il Sindaco Giuseppe Rossi»: eccezione scritta nella Guida
        return any(c.isupper() for c in scritto) and not (a_inizio and scritto[1:].islower())
    if forma[:1].isupper() and forma[1:].islower():
        if re.search(r"sempre[^.]*maiuscol", nota):  # «Repubblica», «Parlamento»: maiuscola sempre
            return scritto[:1].islower() or (scritto.isupper() and len(scritto) > 1)
        return scritto.isupper() and len(scritto) > 1  # «Stato», «Comune»: in minuscolo possono essere altre parole
    return scritto.lower() == forma.lower()


def controlla_glossario(prosa: list, glossario: list[dict], info: dict) -> list[dict]:
    trovate = {}
    for voce in glossario:
        caso, consiglio, esteso = tipo_nota(voce["nota"])
        if not (caso or consiglio) or not voce["forme"] or "€" in voce["forme"]:
            continue  # la voce sull'euro la controlla la regola PAROLE-EURO
        citate = {c.lower() for c in re.findall(r"[“\"]([^”\"]+)[”\"]", voce["nota"])}
        occorrenze = []
        for forma in voce["forme"]:
            schema = re.compile(r"(?<![\w-])" + re.escape(forma).replace(r"\ ", r"\s+") + r"(?![\w-])", re.I)
            for indice, (numero, testo_riga, _) in enumerate(prosa):
                occorrenze += [(indice, m.start(), m.end(), forma, m.group(0)) for m in schema.finditer(testo_riga)]
        # una forma corta dentro una più lunga della stessa voce («protezione civile» in «Dipartimento della protezione civile») non conta
        occorrenze = [o for o in occorrenze if not any(a[0] == o[0] and a[1] <= o[1] and o[2] <= a[2] and (a[2] - a[1]) > (o[2] - o[1])
                                                       for a in occorrenze)]
        estesa_vista = False
        for indice, inizio, fine, forma, scritto in sorted(occorrenze):
            numero, testo_riga, _ = prosa[indice]
            motivo = None
            if caso and _grafia_sbagliata(scritto, forma, testo_riga, inizio, fine, voce["nota"]):
                motivo = f"si scrive «{forma}»"
            elif consiglio and esteso:
                if forma.lower() == voce["forme"][0].lower():
                    estesa_vista = True
                elif not estesa_vista:
                    motivo = f"la prima volta scrivi per esteso «{voce['forme'][0]}»"
                    estesa_vista = True
            elif consiglio and scritto.lower() not in citate:
                motivo = "c'è un'indicazione"
            if motivo and (voce["voce"], numero) not in trovate:
                trovate[(voce["voce"], numero)] = {"riga": numero, "regola": "PAROLE-GLOSSARIO", "gravita": "valutare",
                                                   "fonte": f"Guida alle parole della PA › {voce['voce']}",
                                                   "messaggio": f"«{scritto}»: {motivo}. Dalla Guida: {voce['nota']}"}
    return list(trovate.values())


# ————————————————————————————————————————— versioni e file della skill —————————————————————————————————————————

def carica_json(percorso: Path, predefinito=None):
    try:
        return json.loads(percorso.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return predefinito


def scrivi_json(percorso: Path, dati) -> None:
    percorso.write_text(json.dumps(dati, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def scrivi_indice(cartella: Path, versioni: dict, documenti: list[dict], fonti: dict) -> None:
    righe = ["# Manuali ufficiali per i testi della PA", "",
             f"Testi scaricati dai repository ufficiali su GitHub il {versioni['aggiornato_il']}. Non modificarli a mano: si aggiornano "
             f"con `{COMANDO} aggiorna`, che dice anche cosa è cambiato.", "",
             "| File | Documento | Editore e licenza | Versione del testo |", "|---|---|---|---|"]
    for documento in documenti:
        info = versioni["documenti"].get(documento["id"], {})
        fonte = fonti[documento["fonte"]]
        righe.append(f"| {documento['uscita']} | [{documento['titolo']}]({documento['url']}) | {fonte['editore']}, {fonte['licenza']} | "
                     f"cambiato l'ultima volta il {info.get('cambiato_il', '?')} |")
    righe += ["", "Repository e commit usati:", ""]
    for fid, fonte in fonti.items():
        info = versioni["fonti"].get(fid, {})
        righe.append(f"- {fonte['nome']}: {fonte['repo']} (ramo {fonte['ramo']}), commit {info.get('commit', '?')[:7]} del "
                     f"{data_italiana(info.get('data', '?'))}.")
    if versioni.get("design_system"):
        righe += ["", f"Versione della documentazione del design system .italia: {versioni['design_system']}."]
    righe += ["", "Attribuzione: i testi di Designers Italia (Dipartimento per la trasformazione digitale) sono pubblicati con licenza "
              f"CC BY 4.0 ({LICENZE['CC BY 4.0']}); le Linee guida di design di AgID con licenza CC0 1.0. Le pagine dei Fondamenti sono "
              "convertite da YAML a Markdown senza cambiare il testo; i file .rst sono i sorgenti originali, uniti in un file per documento "
              "(ogni parte comincia con «.. file: nome»).", "",
              "File di servizio: versioni.json (versioni e impronte), regole.json (regole che lo script controlla, confermate sul testo "
              "dei manuali), glossario.json (voci della Guida alle parole della PA)."]
    (cartella / "INDICE.md").write_text("\n".join(righe) + "\n", encoding="utf-8")


def aggiorna(uscita: Path, cache: Path, fonti: dict = FONTI, documenti: list[dict] = DOCUMENTI, mostra_differenze: bool = False,
             adesso: str | None = None, confronto: Path | None = None) -> dict:
    """Scarica i manuali, riscrive i file, ricalcola regole e glossario. Restituisce il resoconto delle differenze.
    Confronta con versioni.json della cartella di uscita oppure, se è nuova, con quello della skill (o con «confronto»)."""
    uscita.mkdir(parents=True, exist_ok=True)
    if confronto is not None:
        vecchie = carica_json(confronto) or {"fonti": {}, "documenti": {}}
    else:
        vecchie = carica_json(uscita / "versioni.json") or carica_json(MANUALI / "versioni.json") or {"fonti": {}, "documenti": {}}
    oggi = adesso or datetime.now(FUSO).strftime("%d/%m/%Y %H:%M")
    copie = {fid: copia_aggiornata(fid, fonte, cache, documenti) for fid, fonte in fonti.items()}
    resoconto = {"documenti": [], "regole_spente": [], "regole_spente_ora": [], "design_system": None, "novita_design_system": []}
    nuove = {"aggiornato_il": oggi, "fonti": {}, "documenti": {}, "design_system": None}
    for fid, (cartella, commit, data) in copie.items():
        nuove["fonti"][fid] = {"repo": fonti[fid]["repo"], "ramo": fonti[fid]["ramo"], "commit": commit, "data": data}
    for documento in documenti:
        cartella, commit, data = copie[documento["fonte"]]
        sorgenti = leggi_sorgenti(documento, cartella)
        firma = impronta(sorgenti)
        if documento["tipo"] == "pagina":
            testo = pagina_in_markdown(sorgenti[0][1], documento, fonti[documento["fonte"]], commit, data)
        else:
            testo = testo_rst(sorgenti)
        file = uscita / documento["uscita"]
        prima = vecchie["documenti"].get(documento["id"], {})
        if not prima:
            stato = "nuovo"
        elif prima.get("sha256_sorgente") == firma:
            stato = "uguale"
        else:
            stato = "cambiato"
        differenze = []
        if stato == "cambiato":
            vecchio_testo = file.read_text(encoding="utf-8") if file.is_file() else ""
            if not vecchio_testo and (MANUALI / documento["uscita"]).is_file():
                vecchio_testo = (MANUALI / documento["uscita"]).read_text(encoding="utf-8")
            differenze = list(difflib.unified_diff(corpo_senza_intestazione(vecchio_testo).splitlines(),
                                                   corpo_senza_intestazione(testo).splitlines(),
                                                   f"prima/{documento['uscita']}", f"dopo/{documento['uscita']}", lineterm="", n=1))
        file.write_text(testo, encoding="utf-8")
        nuove["documenti"][documento["id"]] = {"file": documento["uscita"], "url": documento["url"], "sha256_sorgente": firma,
                                               "cambiato_il": oggi[:10] if stato != "uguale" else prima.get("cambiato_il", oggi[:10])}
        aggiunte = sum(1 for r in differenze if r.startswith("+") and not r.startswith("+++"))
        tolte = sum(1 for r in differenze if r.startswith("-") and not r.startswith("---"))
        resoconto["documenti"].append({"id": documento["id"], "titolo": documento["titolo"], "stato": stato, "righe_aggiunte": aggiunte,
                                       "righe_tolte": tolte, "differenze": differenze if mostra_differenze else differenze[:0]})
    if "designers" in copie:
        nuove["design_system"] = versione_design_system(copie["designers"][0])
        resoconto["design_system"] = nuove["design_system"]
        resoconto["novita_design_system"] = novita_design_system(copie["designers"][0], vecchie.get("design_system"))
    regole_prima = carica_json(uscita / "regole.json") or carica_json(MANUALI / "regole.json") or {}
    guida = next((d for d in documenti if d["id"] == "guida-parole-pa"), None)
    if guida:
        scrivi_json(uscita / "glossario.json", leggi_glossario((uscita / guida["uscita"]).read_text(encoding="utf-8")))
    regole = conferma_regole(uscita)
    scrivi_json(uscita / "regole.json", regole)
    resoconto["regole_spente"] = [rid for rid, r in regole.items() if not r["confermata"]]
    resoconto["regole_spente_ora"] = [rid for rid in resoconto["regole_spente"] if regole_prima.get(rid, {}).get("confermata", True)]
    scrivi_json(uscita / "versioni.json", nuove)
    scrivi_indice(uscita, nuove, documenti, fonti)
    return resoconto


def controlla(versioni: dict, cache: Path, fonti: dict = FONTI, documenti: list[dict] = DOCUMENTI) -> dict:
    """Confronta con le fonti online senza toccare i file della skill."""
    esito = {"stato": "aggiornati", "cambiati": [], "fonti_cambiate": [], "errore": None}
    try:
        for fid, fonte in fonti.items():
            remoto = commit_remoto(fonte)
            if remoto == versioni.get("fonti", {}).get(fid, {}).get("commit"):
                continue
            esito["fonti_cambiate"].append(fid)
            cartella, _, _ = copia_aggiornata(fid, fonte, cache, documenti)
            for documento in (d for d in documenti if d["fonte"] == fid):
                prima = versioni.get("documenti", {}).get(documento["id"], {}).get("sha256_sorgente")
                try:
                    firma = impronta(leggi_sorgenti(documento, cartella))
                except FileNotFoundError as e:
                    esito["cambiati"].append({"id": documento["id"], "titolo": documento["titolo"], "url": documento["url"], "nota": str(e)})
                    continue
                if firma != prima:
                    esito["cambiati"].append({"id": documento["id"], "titolo": documento["titolo"], "url": documento["url"],
                                              "nota": "nuovo documento" if not prima else "testo cambiato"})
    except ErroreRete as e:
        esito.update(stato="non raggiungibili", errore=str(e))
        return esito
    if esito["cambiati"]:
        esito["stato"] = "cambiati"
    return esito


def crea_pacchetto(uscita_manuali: Path, destinazione: Path) -> int:
    """Crea il file .skill con la skill e i manuali appena scaricati (anche se la cartella della skill è di sola lettura)."""
    n = 0
    with zipfile.ZipFile(destinazione, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(CARTELLA_SKILL.rglob("*")):
            if f.is_dir() or "__pycache__" in f.parts or f.suffix == ".pyc":
                continue
            relativo = f.relative_to(CARTELLA_SKILL)
            if relativo.parts[:2] == ("references", "manuali") and uscita_manuali.resolve() != MANUALI.resolve():
                continue
            z.write(f, f"{CARTELLA_SKILL.name}/{relativo.as_posix()}")
            n += 1
        if uscita_manuali.resolve() != MANUALI.resolve():
            for f in sorted(uscita_manuali.iterdir()):
                if f.is_file():
                    z.write(f, f"{CARTELLA_SKILL.name}/references/manuali/{f.name}")
                    n += 1
    return n


# ————————————————————————————————————————— comandi —————————————————————————————————————————

def cartella_manuali(argomenti) -> Path:
    return Path(argomenti.manuali).expanduser() if getattr(argomenti, "manuali", None) else MANUALI


def comando_versioni(argomenti) -> int:
    cartella = cartella_manuali(argomenti)
    versioni = carica_json(cartella / "versioni.json")
    if not versioni:
        print(f"Nessun versioni.json in {cartella}: lancia «aggiorna».")
        return 1
    regole = carica_json(cartella / "regole.json", {})
    print(f"Manuali scaricati il {versioni['aggiornato_il']} (cartella {cartella})")
    for documento in DOCUMENTI:
        info = versioni["documenti"].get(documento["id"], {})
        print(f"  {documento['titolo']}: testo cambiato l'ultima volta il {info.get('cambiato_il', '?')}")
    if versioni.get("design_system"):
        print(f"  Documentazione del design system .italia: versione {versioni['design_system']}")
    spente = [rid for rid, r in regole.items() if not r.get("confermata")]
    print(f"Regole controllate dallo script: {len(regole) - len(spente)} attive" + (f", spente {', '.join(spente)}" if spente else ""))
    return 0


def comando_controlla(argomenti) -> int:
    percorso = Path(argomenti.versioni) if argomenti.versioni else cartella_manuali(argomenti) / "versioni.json"
    versioni = carica_json(percorso)
    if not versioni:
        print(f"Non trovo {percorso}: lancia «aggiorna».")
        return 2
    esito = controlla(versioni, Path(argomenti.cache))
    esito["versione_nella_skill"] = versioni.get("aggiornato_il")
    if argomenti.issue and esito["stato"] == "cambiati":
        Path(argomenti.issue).write_text(testo_issue(esito, versioni), encoding="utf-8")
    if argomenti.json:
        print(json.dumps(esito, ensure_ascii=False, indent=1))
    elif esito["stato"] == "aggiornati":
        extra = " (i repository hanno novità che non riguardano questi testi)" if esito["fonti_cambiate"] else ""
        print(f"Manuali aggiornati: i testi in uso (scaricati il {versioni['aggiornato_il']}) sono uguali a quelli online{extra}.")
    elif esito["stato"] == "cambiati":
        print(f"I manuali sono cambiati rispetto ai testi in uso (scaricati il {versioni['aggiornato_il']}):")
        for c in esito["cambiati"]:
            print(f"  - {c['titolo']} ({c['nota']}): {c['url']}")
        print(f"Lancia «{COMANDO} aggiorna» e leggi le parti cambiate prima di scrivere.")
    else:
        print(f"Non riesco a controllare i manuali online ({esito['errore']}). Uso i testi scaricati il {versioni['aggiornato_il']}: "
              "scrivilo nella consegna.")
    return {"aggiornati": 0, "cambiati": 1}.get(esito["stato"], 2)


def testo_issue(esito: dict, versioni: dict) -> str:
    righe = [f"I manuali per scrivere i testi della PA sono cambiati rispetto alla copia della skill scrittura-pubblica-amministrazione "
             f"(testi scaricati il {versioni.get('aggiornato_il', '?')}). Controllo del {datetime.now(FUSO).strftime('%d/%m/%Y')}:", ""]
    righe += [f"- [{c['titolo']}]({c['url']}): {c['nota']}" for c in esito["cambiati"]]
    righe += ["", "Cosa fare:", "",
              "1. Nella cartella della skill: `python3 scripts/manuali.py aggiorna --mostra` e leggi cosa è cambiato.",
              "2. Se cambia una regola già usata sul sito: `python3 scripts/manuali.py testo content/` e proponi le correzioni con una pull "
              "request per volta.",
              "3. Sostituisci la copia installata della skill: in Claude Code si aggiorna nella sua cartella; nell'app carica il file creato con "
              "`aggiorna --pacchetto scrittura-pubblica-amministrazione.skill`."]
    return "\n".join(righe) + "\n"


def _link_confronto(fonte: dict, prima: str, dopo: str) -> str:
    corti = f"{prima[:7]} → {dopo[:7]}" if prima else f"commit {dopo[:7]}"
    if prima and fonte["repo"].startswith("https://github.com/"):
        return f"[{corti}]({fonte['repo']}/compare/{prima}...{dopo})"
    return corti


def resoconto_markdown(resoconto: dict, prima: dict, dopo: dict, fonti: dict = FONTI, righe_per_documento: int = 60,
                       caratteri_max: int = 30000) -> str:
    """Le novità di un aggiornamento in Markdown, per l'issue settimanale del sito. Stringa vuota se non è cambiato niente."""
    cambiati = [d for d in resoconto["documenti"] if d["stato"] != "uguale"]
    spente = resoconto.get("regole_spente_ora", resoconto["regole_spente"])
    if not cambiati and not spente:
        return ""
    righe = [f"Confronto con la copia del {prima.get('aggiornato_il', '?')}, sui repository ufficiali di AgID e Designers Italia.", ""]
    for d in cambiati:
        url = (dopo.get("documenti", {}).get(d["id"]) or {}).get("url") or PER_ID.get(d["id"], {}).get("url", "")
        quanto = f"testo cambiato (+{d['righe_aggiunte']} −{d['righe_tolte']} righe)" if d["stato"] == "cambiato" else "documento nuovo"
        righe.append(f"- **{d['titolo']}**: {quanto}" + (f" · [pagina]({url})" if url else ""))
    repository = []
    for fid, fonte in fonti.items():
        vecchio = prima.get("fonti", {}).get(fid, {}).get("commit", "")
        nuovo = dopo.get("fonti", {}).get(fid, {}).get("commit", "")
        if nuovo and nuovo != vecchio:
            repository.append(f"- {fonte['nome']}: {_link_confronto(fonte, vecchio, nuovo)}")
    if repository:
        righe += ["", "Repository cambiati (il confronto mostra tutte le modifiche, anche quelle che non toccano i testi):", ""] + repository
    if resoconto.get("novita_design_system"):
        righe += ["", "Novità della documentazione del design system: " + "; ".join(resoconto["novita_design_system"])]
    if spente:
        righe += ["", "Regole dello script che il testo dei manuali non conferma più (spente finché non si rivedono): "
                  + ", ".join(spente)]
    usati = sum(len(r) + 1 for r in righe)
    for d in cambiati:
        if not d["differenze"]:
            continue
        corpo = d["differenze"][2:] if len(d["differenze"]) > 2 and d["differenze"][0].startswith("---") else d["differenze"]
        tagliate = max(0, len(corpo) - righe_per_documento)
        blocco = ["", "<details><summary>Righe cambiate: " + d["titolo"] + "</summary>", "", "````diff", *corpo[:righe_per_documento], "````"]
        if tagliate:
            blocco.append(f"… altre {tagliate} righe nella copia aggiornata.")
        blocco += ["", "</details>"]
        lunghezza = sum(len(r) + 1 for r in blocco)
        if usati + lunghezza > caratteri_max:
            righe += ["", "Le altre righe cambiate sono nella copia aggiornata dei manuali (troppe per questo testo)."]
            break
        righe += blocco
        usati += lunghezza
    return "\n".join(righe) + "\n"


def comando_aggiorna(argomenti) -> int:
    uscita = Path(argomenti.uscita).expanduser() if argomenti.uscita else MANUALI
    if argomenti.pacchetto and not DENTRO_LA_SKILL:
        # Fuori dalla skill CARTELLA_SKILL è il repository intero: il pacchetto lo conterrebbe tutto.
        print(f"Il file .skill si crea solo dalla cartella della skill: in {CARTELLA_SKILL} non c'è SKILL.md.")
        return 2
    prima = carica_json(uscita / "versioni.json") or carica_json(MANUALI / "versioni.json") or {"fonti": {}, "documenti": {}}
    if uscita.resolve() == MANUALI.resolve() and not os.access(MANUALI, os.W_OK):
        print("La cartella della skill è di sola lettura (succede nell'app): usa --uscita CARTELLA e poi --pacchetto per il file .skill.")
        return 2
    try:
        resoconto = aggiorna(uscita, Path(argomenti.cache), mostra_differenze=argomenti.mostra or bool(argomenti.resoconto))
    except ErroreRete as e:
        print(f"Non riesco a scaricare i manuali: {e}")
        return 2
    except FileNotFoundError as e:
        print(f"Un manuale non è più dove lo cercavo: {e}. Controlla il repository e aggiorna l'elenco in {COMANDO.split()[-1]}.")
        return 2
    if argomenti.resoconto:
        testo = resoconto_markdown(resoconto, prima, carica_json(uscita / "versioni.json", {}))
        destinazione = Path(argomenti.resoconto)
        if testo:
            destinazione.write_text(testo, encoding="utf-8")
        elif destinazione.exists():
            destinazione.unlink()
    if argomenti.json:
        print(json.dumps(resoconto, ensure_ascii=False, indent=1))
    else:
        cambiati = [d for d in resoconto["documenti"] if d["stato"] != "uguale"]
        print(f"Manuali scaricati in {uscita}.")
        if not cambiati:
            print("Nessun testo cambiato.")
        for d in cambiati:
            dettaglio = f" (+{d['righe_aggiunte']} −{d['righe_tolte']} righe)" if d["stato"] == "cambiato" else ""
            print(f"  {d['stato'].upper()}: {d['titolo']}{dettaglio}")
            for riga in d["differenze"] if argomenti.mostra else []:
                print("     " + riga)
        if resoconto["novita_design_system"]:
            print("Novità della documentazione del design system: " + "; ".join(resoconto["novita_design_system"]))
        if resoconto["regole_spente"]:
            print("Regole dello script non più confermate dal testo dei manuali (spente finché non le rivedi): "
                  + ", ".join(resoconto["regole_spente"]))
        if cambiati:
            print("Prossimi passi: leggi le parti cambiate; se cambiano regole già usate sul sito, proponi ad Alessandro le correzioni; "
                  f"se lo script ha regole spente, rivedile in {COMANDO.split()[-1]} (REGOLE).")
    if argomenti.pacchetto:
        n = crea_pacchetto(uscita, Path(argomenti.pacchetto).expanduser())
        print(f"Creato {argomenti.pacchetto} ({n} file): installalo al posto della versione vecchia della skill.")
    return 0


def file_da_controllare(percorsi: list[str]) -> list[Path]:
    trovati = []
    for p in map(Path, percorsi):
        if p.is_dir():
            trovati += sorted(x for x in p.rglob("*.md") if x.is_file())
        else:
            trovati.append(p)
    return trovati


def comando_testo(argomenti) -> int:
    cartella = cartella_manuali(argomenti)
    regole = carica_json(cartella / "regole.json")
    glossario = carica_json(cartella / "glossario.json", [])
    versioni = carica_json(cartella / "versioni.json", {})
    if not regole:
        print(f"Non trovo regole.json in {cartella}: lancia «aggiorna».")
        return 2
    spente = [rid for rid, r in regole.items() if not r["confermata"]]
    risultati, errori_totali = [], 0
    for file in file_da_controllare(argomenti.file):
        testo = sys.stdin.read() if str(file) == "-" else file.read_text(encoding="utf-8")
        esito = controlla_testo(testo, regole, glossario)
        esito["file"] = str(file)
        risultati.append(esito)
        errori_totali += sum(1 for s in esito["segnalazioni"] if s["gravita"] == "correggere")
    if argomenti.json:
        print(json.dumps({"manuali_del": versioni.get("aggiornato_il"), "regole_spente": spente, "file": risultati}, ensure_ascii=False, indent=1))
    else:
        print(f"Controllo con i manuali scaricati il {versioni.get('aggiornato_il', '?')}: {len(regole) - len(spente)} regole attive"
              + (f", spente {', '.join(spente)} (rivedile)" if spente else "") + ".")
        for esito in risultati:
            print(f"\n{esito['file']}")
            if not esito["segnalazioni"]:
                print("  Nessuna segnalazione.")
            for gravita, etichetta in (("correggere", "DA CORREGGERE"), ("valutare", "DA VALUTARE"), ("nota", "NOTE")):
                gruppo = [s for s in esito["segnalazioni"] if s["gravita"] == gravita]
                if gruppo:
                    print(f"  {etichetta}")
                    for s in gruppo:
                        print(f"  - riga {s['riga']}: {s['messaggio']} [{s['fonte']}]")
            if esito.get("gulpease"):
                g = esito["gulpease"]
                print(f"  Indice Gulpease {g['valore']} su {g['parole']} parole: i Fondamenti lo citano tra i test di leggibilità, senza soglie.")
        print("\nLo script segnala, non decide: per ogni punto vale il testo del manuale citato tra parentesi quadre.")
    return 1 if argomenti.severo and errori_totali else 0


# ————————————————————————————————————————— autotest —————————————————————————————————————————

PAGINA_CON_PROBLEMI = """---
title: "Esercitazione Di Protezione Civile Con I Volontari Del Gruppo Comunale A Genzano Di Roma Nel 2026"
description: "Esercitazione di protezione civile con i volontari"
---
# Esercitazione

Si comunica che il giorno 24/10/2026 alle ore 9.30 i volontari della Protezione Civile si troveranno in piazza. Il Sindaco sarà presente.

Benvenuti a tutti! Per informazioni scrivete una e-mail a info@esempio.it oppure telefonate allo 06 1234567. La quota è di 5 € e il percorso è lungo 2.5 km. Sono attese 12000 persone. Il COC sarà aperto. Si è provveduto a chiudere la strada. Ogni anno 3.500 cittadini partecipano.

Le regole sono nel d.lgs. 1/2018, art. 12. Chi arriva tardi paga un'ammenda.

## Programma

#### Dettagli

- Ritrovo alle 8:30
  - con il giubbino
- [Vedi il programma](programma.pdf)
- [qui](https://esempio.it/mappa)

![](foto.jpg)

Attenzione! L'ESERCITAZIONE INIZIA PUNTUALE. Temperatura prevista 25°C. Distanza 3km. Il testo <u>importante</u>.
Prima. Seconda frase. Terza frase. Quarta frase. Quinta frase. Sesta frase.
"""

PAGINA_PULITA = """---
title: "Esercitazione di Protezione civile a Genzano di Roma"
description: "Sabato 24 ottobre 2026 i volontari provano il piano di emergenza in piazza Frasconi."
lastmod: 2026-10-15
---
Sabato 24 ottobre 2026, dalle 9:30 alle 12:30, i volontari provano il piano di emergenza comunale in piazza Frasconi. Ti chiediamo di non lasciare l'auto in piazza.

## Cosa succede

Durante la prova senti la sirena per 3 minuti. Non devi fare nulla: è solo un test.

Per partecipare:

1. Scrivi a [protezionecivile@esempio.it](mailto:protezionecivile@esempio.it).
2. Indica nome e numero di telefono.
3. Aspetta la conferma.

## Contatti

Telefono: [+39 06 123 456 78](tel:+390612345678). Il sindaco ringrazia chi partecipa.
"""

GLOSSARIO_PROVA = """.. file: index.rst

Titolo
======

.. file: le-parole-della-pubblica-amministrazione/a.rst

A
=

abrogare (abrogazione)
     Limita l’uso di questo termine ai contesti normativi.

     |

Agenda digitale (italiana)
     Solo la prima lettera è maiuscola.

     |

ammenda
     Preferisci l’uso di “multa” o “contravvenzione”.

     .. admonition:: use

        *Dovranno pagare una multa.*

     .. admonition:: use-not

        *Comporterà l’applicazione di un’ammenda.*

     |

.. file: le-parole-della-pubblica-amministrazione/o.rst

O
=

online, on-line oppure on line?
     Preferisci “online”, anche se tutte e tre le versioni sono corrette.

conto corrente, c/c
     Scrivilo per esteso.
"""


def autotest() -> int:
    errori = []

    def prova(condizione, descrizione, dettaglio=""):
        print(("OK   " if condizione else "ERRORE ") + descrizione)
        if not condizione:
            errori.append(descrizione)
            if dettaglio:
                print("     " + str(dettaglio)[:600])

    # 1. glossario
    voci = leggi_glossario(GLOSSARIO_PROVA)
    nomi = [v["voce"] for v in voci]
    prova(nomi == ["abrogare (abrogazione)", "Agenda digitale (italiana)", "ammenda", "online, on-line oppure on line?", "conto corrente, c/c"],
          "glossario: voci lette, titolo e indice esclusi", nomi)
    prova(voci[0]["forme"] == ["abrogare", "abrogazione"] and voci[1]["forme"] == ["Agenda digitale", "Agenda digitale italiana"]
          and voci[3]["forme"] == ["online", "on-line", "on line"] and voci[4]["forme"] == ["conto corrente", "c/c"],
          "glossario: forme delle voci", [v["forme"] for v in voci])
    prova(voci[2]["va_bene"] == ["Dovranno pagare una multa."] and voci[2]["non_va_bene"] == ["Comporterà l’applicazione di un’ammenda."]
          and voci[2]["nota"].startswith("Preferisci"), "glossario: nota ed esempi", voci[2])

    # 2. conversione di una pagina dei Fondamenti
    try:
        import yaml  # noqa: F401
        pagina = ("components:\n  hero:\n    title: Linguaggio\n    subtitle: Scrivi chiaro.\n  sectionsEditorial:\n    - components:\n"
                  "      - name: TextImageCta\n        title: Parlare la lingua delle persone\n        headingLevel: 2\n        text: |\n"
                  "          Vedi [test](/risorse/x/) e ![Esempio](/img.png \"t\")\n      - name: Table\n        head:\n"
                  "          - tag:\n              label: VA BENE\n          - tag:\n              label: NON VA BENE\n        rows:\n"
                  "          - cols:\n            - text: Scopri\n            - text: Vedi | leggi\n        ctas:\n          - label: Vai\n"
                  "            url: /design-system/x/\n")
        md = pagina_in_markdown(pagina.encode(), PER_ID["fondamenti-linguaggio"], FONTI["designers"], "abcdef1234", "2026-10-05T16:23:20+02:00")
        prova(md.startswith("# Linguaggio\n") and FINE_INTESTAZIONE in md and "## Parlare la lingua delle persone" in md
              and "[test](https://designers.italia.it/risorse/x/)" in md and "(Immagine: Esempio)" in md
              and "| VA BENE | NON VA BENE |" in md and "| Scopri | Vedi \\| leggi |" in md
              and "→ [Vai](https://designers.italia.it/design-system/x/)" in md and "commit abcdef1 del 05/10/2026" in md,
              "conversione YAML → Markdown dei Fondamenti", md)
    except ImportError:
        print("SALTATA conversione dei Fondamenti: manca PyYAML")

    # 3. regole confermate sui manuali in uso e controllo di due pagine
    if (MANUALI / "versioni.json").is_file():
        regole = conferma_regole(MANUALI)
        spente = [r for r, v in regole.items() if not v["confermata"]]
        prova(not spente, "tutte le regole dello script sono confermate dal testo dei manuali in uso", spente)
        salvate = carica_json(MANUALI / "regole.json", {})
        prova(salvate == regole, "regole.json allineato ai manuali in uso", [k for k in regole if salvate.get(k) != regole[k]])
        prova(regole["CONT-TITOLO"]["valore"] == 70 and regole["CONT-SOMMARIO-LUNGHEZZA"]["valore"] == 160
              and regole["CONT-PARAGRAFI"]["valore"] == 5 and regole["CONT-LIVELLI"]["valore"] == 4,
              "valori letti dai manuali (70, 160, 5 frasi, H4)", {k: regole[k]["valore"] for k in regole if regole[k]["valore"]})
        glossario = carica_json(MANUALI / "glossario.json", [])
        prova(len(glossario) > 80 and any(v["voce"].startswith("Protezione civile") for v in glossario), "glossario dei manuali in uso letto",
              len(glossario))
        esito = controlla_testo(PAGINA_CON_PROBLEMI, regole, glossario)
        trovate = {s["regola"] for s in esito["segnalazioni"]}
        attese = {"CONT-TITOLO", "LING-MAIUSCOLO", "CONT-SOMMARIO-PUNTO", "CONT-SOMMARIO-TITOLO", "CONT-H1", "CONT-LIVELLI", "LING-DATE",
                  "LING-ORARI", "TONO-TU", "LING-TELEFONO", "LING-EMAIL", "LING-EMAIL-LINK", "LING-UNITA", "LING-SIGLE", "PAROLE-GLOSSARIO",
                  "INCL-MASCHILE", "CONT-LINK", "CONT-ALT", "LING-NORME", "PAROLE-EURO", "LING-MIGLIAIA", "LING-DECIMALI", "CONT-PARAGRAFI",
                  "CONT-SOTTOELENCHI", "MICRO-CONFERMA", "LING-SOTTOLINEATO", "INCL-VEDI", "LING-ATTIVI", "LG-AGGIORNAMENTO"}
        prova(attese <= trovate, "pagina con problemi: trovate tutte le regole attese", sorted(attese - trovate))
        messaggi = " ".join(s["messaggio"] for s in esito["segnalazioni"])
        prova("«Protezione Civile»: si scrive «Protezione civile»" in messaggi and "«Sindaco»: si scrive «sindaco»" in messaggi
              and "«ammenda»" in messaggi and "(9:30)" in messaggi and "«3km»" in messaggi and "«25°C»" in messaggi
              and "(12.000)" in messaggi and "(3500)" in messaggi and "(2,5)" in messaggi, "pagina con problemi: messaggi precisi", messaggi[:1500])
        esito = controlla_testo(PAGINA_PULITA, regole, glossario)
        prova(not esito["segnalazioni"], "pagina pulita: nessuna segnalazione",
              [(s["riga"], s["regola"], s["messaggio"]) for s in esito["segnalazioni"]])
        prova(esito.get("gulpease") and 40 < esito["gulpease"]["valore"] <= 100, "indice Gulpease calcolato", esito.get("gulpease"))
        spenta = {**regole, "CONT-TITOLO": {**regole["CONT-TITOLO"], "confermata": False}}
        esito = controlla_testo(PAGINA_CON_PROBLEMI, spenta, glossario)
        prova("CONT-TITOLO" not in {s["regola"] for s in esito["segnalazioni"]}, "una regola non confermata non viene applicata")
    else:
        print(f"SALTATE le prove sulle regole: in {MANUALI} non ci sono ancora i manuali (lancia «aggiorna»)")
    prova(MANUALI.relative_to(CARTELLA_SKILL).as_posix() == ("references/manuali" if DENTRO_LA_SKILL else ".manuale/manuali-agid"),
          "cartella dei manuali giusta per dove si trova lo script", MANUALI)
    prova(FUSO is None or datetime.now(FUSO).utcoffset().total_seconds() in (3600, 7200), "date e ore dei manuali in ora italiana", FUSO)

    # 4. aggiornamento e controllo con repository finti in locale
    if shutil.which("git") is None:
        print("SALTATE le prove di aggiornamento: git non è installato")
    else:
        with tempfile.TemporaryDirectory() as tmp:
            radice = Path(tmp)
            fonti = {}
            contenuti = {
                "lg-design": {"note-lettura.rst": "Note\n=====\n\nSI DEVE.\n",
                              "requisiti.rst": "Requisiti\n=========\n\n- SI DOVREBBE pubblicare, su ogni pagina del sito internet, la data "
                                               "dell'ultimo aggiornamento o verifica del contenuto.\n"},
                "designers": {f"src/data/content/design-system/fondamenti/{n}.yaml":
                              f"components:\n  hero:\n    title: {t}\n    subtitle: Prova di {t}.\n" for n, t in FONDAMENTI.items()},
                "parole-pa": {"index.rst": "Guida\n=====\n", "le-parole-della-pubblica-amministrazione/a.rst":
                              GLOSSARIO_PROVA.split(".. file: le-parole-della-pubblica-amministrazione/a.rst\n\n")[1].split(".. file:")[0]},
                "mod": {f"doc/progettazione-dei-contenuti/{n}.rst": f"{t}\n{'=' * len(t)}\n\nTesto di prova.\n" for n, t in MOD_PAGINE.items()},
            }
            contenuti["designers"][VERSIONAMENTO] = ("components:\n  x: 1\n# Documentazione (questo sito)\n#  label: \"1.13.0\"\n"
                                                     "text: |\n  ### v1.13.0\n  15 luglio 2026\n")
            contenuti["designers"]["altro/file-grande.txt"] = "non serve\n"
            for fid, fonte in FONTI.items():
                repo = radice / "remoti" / fid
                (repo).mkdir(parents=True)
                for nome, testo in contenuti[fid].items():
                    (repo / nome).parent.mkdir(parents=True, exist_ok=True)
                    (repo / nome).write_text(testo, encoding="utf-8")
                for comando in (["init", "-q", "-b", fonte["ramo"]], ["add", "-A"],
                                ["-c", "user.name=prova", "-c", "user.email=prova@esempio.it", "commit", "-q", "-m", "primo"]):
                    git(["-C", repo, *comando])
                git(["-C", repo, "config", "uploadpack.allowFilter", "true"])
                fonti[fid] = {**fonte, "repo": (repo.resolve()).as_uri()}
            cache, uscita = radice / "cache", radice / "manuali"
            try:
                resoconto = aggiorna(uscita, cache, fonti=fonti, adesso="15/10/2026 16:00", confronto=radice / "nessuno.json")
                stati = {d["id"]: d["stato"] for d in resoconto["documenti"]}
                prova(set(stati.values()) == {"nuovo"} and (uscita / "fondamenti-linguaggio.md").is_file()
                      and (uscita / "guida-parole-pa.rst").is_file() and (uscita / "versioni.json").is_file()
                      and (uscita / "INDICE.md").is_file(), "aggiorna: file scritti in una cartella nuova", stati)
                prova(not (cache / "designers" / "altro" / "file-grande.txt").exists(), "aggiorna: dal sito di Designers Italia solo i file che servono")
                prova(resoconto["design_system"] == "1.13.0", "aggiorna: versione del design system letta", resoconto["design_system"])
                glossario = carica_json(uscita / "glossario.json", [])
                prova([v["voce"] for v in glossario][:3] == ["abrogare (abrogazione)", "Agenda digitale (italiana)", "ammenda"],
                      "aggiorna: glossario ricostruito", glossario[:2])
                versioni = carica_json(uscita / "versioni.json")
                esito = controlla(versioni, cache, fonti=fonti)
                prova(esito["stato"] == "aggiornati", "controlla: nessuna novità", esito)
                repo = radice / "remoti" / "designers"
                (repo / "altro" / "file-grande.txt").write_text("cambiato ma non serve\n", encoding="utf-8")
                git(["-C", repo, "-c", "user.name=prova", "-c", "user.email=prova@esempio.it", "commit", "-q", "-am", "altro"])
                esito = controlla(versioni, cache, fonti=fonti)
                prova(esito["stato"] == "aggiornati" and esito["fonti_cambiate"] == ["designers"],
                      "controlla: novità del repository che non toccano i manuali", esito)
                (repo / "src/data/content/design-system/fondamenti/linguaggio.yaml").write_text(
                    "components:\n  hero:\n    title: Linguaggio\n    subtitle: Testo nuovo.\n", encoding="utf-8")
                git(["-C", repo, "-c", "user.name=prova", "-c", "user.email=prova@esempio.it", "commit", "-q", "-am", "linguaggio"])
                esito = controlla(versioni, cache, fonti=fonti)
                prova(esito["stato"] == "cambiati" and [c["id"] for c in esito["cambiati"]] == ["fondamenti-linguaggio"],
                      "controlla: cambiato il fondamento Linguaggio", esito)
                testo = testo_issue(esito, versioni)
                prova("Fondamenti del design system .italia: Linguaggio" in testo and "testi scaricati il 15/10/2026 16:00" in testo
                      and "Cosa fare" in testo and "workflow" not in testo, "avviso in Markdown per chi usa la skill", testo[:300])
                resoconto = aggiorna(uscita, cache, fonti=fonti, mostra_differenze=True, adesso="22/10/2026 09:00")
                cambiato = next(d for d in resoconto["documenti"] if d["id"] == "fondamenti-linguaggio")
                prova(cambiato["stato"] == "cambiato" and any("Testo nuovo" in r for r in cambiato["differenze"])
                      and all(d["stato"] == "uguale" for d in resoconto["documenti"] if d["id"] != "fondamenti-linguaggio"),
                      "aggiorna: dice cosa è cambiato e solo lì", cambiato)
                versioni_prima, versioni = versioni, carica_json(uscita / "versioni.json")
                md = resoconto_markdown(resoconto, versioni_prima, versioni, fonti)
                prova("**Fondamenti del design system .italia: Linguaggio**: testo cambiato" in md and "+Testo nuovo." in md
                      and "````diff" in md and " → " in md and "Contenuti" not in md.split("Repository cambiati")[0],
                      "resoconto in Markdown: documento, righe e commit", md[:500])
                prova(resoconto_markdown(aggiorna(uscita, cache, fonti=fonti, adesso="22/10/2026 09:30"), versioni, versioni, fonti) == "",
                      "resoconto in Markdown: vuoto se non cambia niente")
                versioni = carica_json(uscita / "versioni.json")
                prova(versioni["documenti"]["fondamenti-linguaggio"]["cambiato_il"] == "22/10/2026"
                      and versioni["documenti"]["fondamenti-contenuti"]["cambiato_il"] == "15/10/2026", "versioni.json: date di cambiamento")
                prova(controlla(versioni, cache, fonti=fonti)["stato"] == "aggiornati", "controlla: dopo l'aggiornamento di nuovo in pari")
                rotte = {**fonti, "mod": {**fonti["mod"], "repo": (radice / "non-esiste").resolve().as_uri()}}
                prova(controlla(versioni, cache, fonti=rotte)["stato"] == "non raggiungibili", "controlla: fonte non raggiungibile → codice 2")
                if DENTRO_LA_SKILL:
                    pacchetto = radice / "prova.skill"
                    n = crea_pacchetto(uscita, pacchetto)
                    with zipfile.ZipFile(pacchetto) as z:
                        nomi_zip = z.namelist()
                        versioni_zip = json.loads(z.read(f"{CARTELLA_SKILL.name}/references/manuali/versioni.json"))
                    prova(n > 5 and f"{CARTELLA_SKILL.name}/SKILL.md" in nomi_zip and versioni_zip["aggiornato_il"] == "22/10/2026 09:30",
                          "pacchetto .skill con i manuali nuovi", nomi_zip[:5])
                else:
                    print("SALTATA la prova del pacchetto .skill: lo script non è nella cartella della skill")
            except ErroreRete as e:
                prova(False, "repository finti raggiungibili con git", e)
    print(f"\n{'Tutto bene' if not errori else str(len(errori)) + ' errori'}")
    return 1 if errori else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--autotest", action="store_true", help="prova lo script senza rete")
    sotto = parser.add_subparsers(dest="comando")
    p = sotto.add_parser("versioni", help="di quando sono i manuali che la skill sta usando")
    p.add_argument("--manuali", help="cartella dei manuali (predefinita: references/manuali nella skill, .manuale/manuali-agid nel sito)")
    p = sotto.add_parser("controlla", help="i manuali online sono cambiati? 0 no, 1 sì, 2 non raggiungibili")
    p.add_argument("--manuali")
    p.add_argument("--versioni", help="versioni.json da confrontare (per il workflow su GitHub)")
    p.add_argument("--cache", default=str(CACHE), help=f"cartella delle copie scaricate (predefinita {CACHE})")
    p.add_argument("--issue", help="se i manuali sono cambiati scrive qui un avviso in Markdown")
    p.add_argument("--json", action="store_true")
    p = sotto.add_parser("aggiorna", help="scarica i manuali, riscrive la copia in uso e dice cosa è cambiato")
    p.add_argument("--uscita", help="scrive i manuali in un'altra cartella invece che nella copia in uso")
    p.add_argument("--pacchetto", help="crea anche il file .skill aggiornato, per esempio scrittura-pubblica-amministrazione.skill")
    p.add_argument("--mostra", action="store_true", help="mostra le righe cambiate")
    p.add_argument("--resoconto", help="se qualcosa è cambiato scrive qui le novità in Markdown (per l'issue settimanale del sito); "
                                       "se non è cambiato niente il file non c'è")
    p.add_argument("--cache", default=str(CACHE))
    p.add_argument("--json", action="store_true")
    p = sotto.add_parser("testo", help="controlla pagine Markdown con le regole dei manuali")
    p.add_argument("file", nargs="+", help="file .md, cartelle (tutti i .md dentro) o - per lo standard input")
    p.add_argument("--manuali")
    p.add_argument("--json", action="store_true")
    p.add_argument("--severo", action="store_true", help="esce con codice 1 se ci sono cose da correggere")
    argomenti = parser.parse_args()
    if argomenti.autotest:
        return autotest()
    comandi = {"versioni": comando_versioni, "controlla": comando_controlla, "aggiorna": comando_aggiorna, "testo": comando_testo}
    if argomenti.comando not in comandi:
        parser.print_help()
        return 0
    return comandi[argomenti.comando](argomenti)


if __name__ == "__main__":
    sys.exit(main())
