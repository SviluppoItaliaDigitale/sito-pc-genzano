#!/usr/bin/env python3
"""
Guardia anti-stale del sito su Aruba: confronta le pagine servite con il
manifesto della build e, se può, ripara.

Come funziona. Ogni build scrive /build-manifest.json (impronta sha256 di
ogni file, scripts/genera-manifest-build.py). Questo script scarica le
pagine dal sito live, con richiesta senza cache, e confronta l'impronta
del contenuto con quella del manifesto. Una pagina diversa è una pagina
rimasta vecchia: qualunque ne sia la causa (caricamento FTP interrotto,
stato di sincronizzazione che la crede aggiornata, file toccato a mano).

Che cosa controlla:
  - sempre: /build-info.js, /build-manifest.json e le pagine critiche
    (home, allerte, numeri utili, emergenza, archivio, ultimo articolo…);
  - con --precedente <manifesto della build prima>: tutti i file che il
    deploy doveva cambiare (al massimo --max-cambiati, poi un campione) e
    quelli che doveva togliere, che devono rispondere con un errore;
  - con --campione N: N pagine HTML scelte a caso nel manifesto (semino
    con --seme, così ogni giro controlla pagine diverse);
  - con --pagine /a/ /b/: pagine indicate a mano.

Riparazione (--ripara): i file diversi vengono ricaricati via FTPS dalla
build locale (--public), quelli tolti dalla build cancellati dal server,
poi tutto ricontrollato. Credenziali da FTP_SERVER,
FTP_USERNAME, FTP_PASSWORD (le stesse di deploy.yml), cartella remota
FTP_SERVER_DIR. Mai la cartella documenti/, gestita a mano sul server.

Nasce il 01/10/2026 al posto di verifica-fingerprint-live.sh, che leggeva
la meta pc-build-sha di 15 pagine: quella meta costringeva a ricaricare
tutte le pagine a ogni deploy, e il confronto diceva solo «quale build»,
non se il contenuto fosse davvero quello costruito. Storia dell'incidente:
01/07/2026, su Aruba convivevano chi-siamo di aprile, allerte-meteo di
maggio e la home di luglio, con un semaforo di allerta vecchio.

Uso:
  python3 scripts/verifica-deploy-aruba.py                       # dal live
  python3 scripts/verifica-deploy-aruba.py --manifesto public/build-manifest.json \
      --public public --precedente /tmp/manifesto-prima.json --ripara   # in deploy.yml
  python3 scripts/verifica-deploy-aruba.py --pagine /chi-siamo/ /numeri-utili/
  python3 scripts/verifica-deploy-aruba.py --diagnostica         # solo impronte

Exit 0 se tutto coincide, 1 se qualcosa resta diverso, 2 per errori d'uso.
Solo Python standard.
"""

from __future__ import annotations

import argparse
import datetime as dt
import ftplib
import hashlib
import json
import os
import random
import re
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

BASE_DEFAULT = "https://www.protezionecivilegenzano.it"
MANIFESTO = "build-manifest.json"
BUILD_INFO = "build-info.js"

# Pagine controllate a ogni giro: alto traffico, catena dell'allerta, e quelle
# trovate vecchie negli incidenti (01/07/2026, 09/06/2026, 13/05/2026).
CRITICHE = [
    "index.html", "allerte-meteo/index.html", "emergenza/index.html",
    "cosa-fare-adesso/index.html", "numeri-utili/index.html", "chi-siamo/index.html",
    "contatti/index.html", "rischi-prevenzione/index.html", "accessibilita/index.html",
    "diventa-volontario/index.html", "area-download/index.html", "formazione/index.html",
    "comunicazioni/index.html", "piano-emergenza/index.html", "piano-familiare/index.html",
    "faq/index.html", "glossario/index.html", "normativa/index.html", "strumenti/index.html",
    "cartografia/index.html", "podcast/index.html", "allerta-cap.xml",
    "allerta-stato/index.json", "sitemap.xml",
    # Pagine in cui le illustrazioni svolgono una funzione didattica, non decorativa.
    "formazione/esperimenti/index.html", "formazione/rischio-incendio/index.html",
    "rischi-prevenzione/rischio-sismico/index.html",
    "rischi-prevenzione/rischio-idrogeologico/index.html",
    "rischi-prevenzione/rischio-incendio/index.html",
    "rischi-prevenzione/temporali-intensi/index.html",
    "rischi-prevenzione/vento-forte/index.html",
    "rischi-prevenzione/blackout/index.html",
    "rischi-prevenzione/rischio-vulcanico/index.html",
    "rischi-prevenzione/kit-emergenza/index.html",
    "rischi-prevenzione/sicurezza-scuolabus/index.html",
    "rischi-prevenzione/rischi-in-parole-semplici/index.html",
]

UA = "PCGenzanoVerificaDeploy/2.0 (+https://www.protezionecivilegenzano.it/)"


def log(msg: str = "") -> None:
    print(msg, flush=True)


def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def url_di(base: str, rel: str) -> str:
    """URL pubblico di un file del manifesto: le index.html come cartella."""
    if rel == "index.html":
        return base + "/"
    if rel.endswith("/index.html"):
        return base + "/" + rel[: -len("index.html")]
    return base + "/" + rel


class _SenzaRedirect(urllib.request.HTTPRedirectHandler):
    """Non seguire i redirect: un 3xx è una regola del server, non il file."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        return None


_APRI = urllib.request.build_opener(_SenzaRedirect)


def scarica(url: str, timeout: int = 25) -> tuple[int, bytes]:
    """GET senza cache e SENZA seguire i redirect. Restituisce (status, corpo);
    status 0 = nessuna risposta, 3xx = il server reindirizza altrove.

    I redirect non si seguono perché .htaccess reindirizza i vecchi URL del
    sito Joomla (`/pianodiemergenza.html` → `/piano-emergenza/`) che Hugo
    genera anche come pagine alias: seguendo il 301 si confrontava la pagina
    di arrivo con l'impronta dell'alias e il file risultava «diverso» pur
    essendo quello della build (falso positivo del 01/10/2026).
    """
    sep = "&" if "?" in url else "?"
    req = urllib.request.Request(
        f"{url}{sep}cb={int(time.time())}{random.randint(1000, 9999)}",
        headers={"User-Agent": UA, "Cache-Control": "no-cache", "Pragma": "no-cache",
                 "Accept-Encoding": "identity"})
    try:
        with _APRI.open(req, timeout=timeout) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except (urllib.error.URLError, OSError, ValueError):
        return 0, b""


def reindirizzato(st: int) -> bool:
    return st in (301, 302, 303, 307, 308)


def verificabile(rel: str) -> bool:
    parti = rel.split("/")
    if any(p.startswith(".") for p in parti):
        return False
    if parti[0] in ("documenti",):
        return False
    return True


def leggi_manifesto_locale(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def scarica_con_riprova(url: str, prove: int = 3, pausa: int = 5) -> tuple[int, bytes]:
    """Come scarica(), ma ritenta quando non arriva nessuna risposta (status 0:
    connessione azzerata, timeout). Un solo inciampo di rete su questi due file
    faceva dichiarare il sito «non leggibile» senza aver guardato le pagine."""
    st, corpo = 0, b""
    for i in range(prove):
        st, corpo = scarica(url)
        if st != 0:
            break
        if i < prove - 1:
            time.sleep(pausa)
    return st, corpo


def leggi_manifesto_live(base: str) -> tuple[dict | None, bytes]:
    st, corpo = scarica_con_riprova(f"{base}/{MANIFESTO}")
    if st != 200 or not corpo:
        return None, b""
    try:
        return json.loads(corpo.decode("utf-8")), corpo
    except ValueError:
        return None, corpo


def leggi_build_info(base: str) -> tuple[str, str]:
    """(sha, time) da /build-info.js, vuoti se illeggibile."""
    st, corpo = scarica_con_riprova(f"{base}/{BUILD_INFO}")
    if st != 200:
        return "", ""
    testo = corpo.decode("utf-8", "replace")
    sha = re.search(r'SITE_BUILD_SHA\s*=\s*"([^"]*)"', testo)
    tm = re.search(r'SITE_BUILD_TIME\s*=\s*"([^"]*)"', testo)
    return (sha.group(1) if sha else ""), (tm.group(1) if tm else "")


def ultimo_articolo(file: dict[str, str]) -> str | None:
    art = sorted(k for k in file if re.match(r"comunicazioni/2\d{3}-\d{2}-\d{2}-[^/]+/index\.html$", k)
                 and not k.split("/")[1].endswith("-facile"))
    return art[-1] if art else None


# ──────────────────────────────────────────────────────────────
# FTPS con riuso della sessione TLS sul canale dati (richiesto da molti
# server; senza, la STOR fallisce con «session reuse required»).
# ──────────────────────────────────────────────────────────────

class FTPS(ftplib.FTP_TLS):
    def ntransfercmd(self, cmd, rest=None):
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conn = self.context.wrap_socket(conn, server_hostname=self.host,
                                            session=self.sock.session)  # type: ignore[attr-defined]
        return conn, size


def apri_ftps() -> tuple[FTPS, str] | None:
    server = os.environ.get("FTP_SERVER", "")
    utente = os.environ.get("FTP_USERNAME", "")
    password = os.environ.get("FTP_PASSWORD", "")
    cartella = os.environ.get("FTP_SERVER_DIR", "/www.protezionecivilegenzano.it/")
    if not (server and utente and password):
        log("⚠️  Riparazione non possibile: FTP_SERVER / FTP_USERNAME / FTP_PASSWORD non impostati.")
        return None
    porta = 21
    if ":" in server:
        server, p = server.rsplit(":", 1)
        porta = int(p)
    # Tre livelli di verifica TLS, dal più severo in giù: (1) catena + nome
    # host; (2) solo catena, perché il certificato dell'FTP di Aruba è
    # emesso per un nome diverso da quello con cui ci si collega (verificato
    # il 01/10/2026: «Hostname mismatch»); (3) nessuna verifica, cioè la
    # stessa posizione dell'action FTP-Deploy (`security: loose`, il suo
    # default) che carica il sito da mesi. Il canale resta cifrato in tutti
    # e tre i casi; si scrive nel log a quale livello ci si è fermati.
    livelli: list[tuple[str, ssl.SSLContext]] = []
    if os.environ.get("FTP_TLS_INSECURE") != "1":  # il server di prova locale è autofirmato
        pieno = ssl.create_default_context()
        livelli.append(("verifica piena", pieno))
        senza_nome = ssl.create_default_context()
        senza_nome.check_hostname = False
        livelli.append(("catena verificata, nome host non controllato", senza_nome))
    nessuna = ssl.create_default_context()
    nessuna.check_hostname = False
    nessuna.verify_mode = ssl.CERT_NONE
    livelli.append(("senza verifica del certificato, come l'action FTP-Deploy", nessuna))
    ftp = None
    ultimo = ""
    for nome, ctx in livelli:
        try:
            ftp = FTPS(context=ctx, timeout=60)
            ftp.connect(server, porta)
            ftp.login(utente, password)
            ftp.prot_p()
            ftp.set_pasv(True)
            ftp.cwd(cartella)
            if nome != "verifica piena":
                log(f"⚠️  FTPS collegato con: {nome}.")
            break
        except ftplib.all_errors as e:  # all_errors è già una tupla e comprende OSError
            ultimo = f"{type(e).__name__}: {e}"
            try:
                ftp.close()  # type: ignore[union-attr]
            except Exception:
                pass
            ftp = None
            if "CERTIFICATE_VERIFY_FAILED" not in ultimo and "SSL" not in type(e).__name__:
                break  # credenziali, cartella, rete: un livello più basso non aiuta
    if ftp is None:
        log(f"⚠️  Connessione FTPS non riuscita: {ultimo}")
        return None
    return ftp, cartella


def carica(ftp: FTPS, radice_remota: str, public: Path, rel: str) -> bool:
    locale = public / rel
    if not locale.is_file():
        log(f"   ✗ {rel}: non esiste nella build locale, non lo carico")
        return False
    parti = rel.split("/")
    try:
        ftp.cwd(radice_remota)
        for cartella in parti[:-1]:
            try:
                ftp.cwd(cartella)
            except ftplib.error_perm:
                ftp.mkd(cartella)
                ftp.cwd(cartella)
        with locale.open("rb") as f:
            ftp.storbinary(f"STOR {parti[-1]}", f)
        return True
    except ftplib.all_errors as e:  # all_errors è già una tupla e comprende OSError
        log(f"   ✗ {rel}: caricamento fallito ({type(e).__name__}: {e})")
        return False


def cancella(ftp: FTPS, radice_remota: str, rel: str) -> bool:
    """Toglie dal server un file che la build non contiene più."""
    try:
        ftp.cwd(radice_remota)
        ftp.delete(rel)
    except ftplib.all_errors as e:
        log(f"   ✗ {rel}: cancellazione fallita ({type(e).__name__}: {e})")
        return False
    # Le cartelle rimaste vuote si tolgono (una cartella vuota risponderebbe
    # ancora, con 403 o con un elenco, invece del 404 che la build prevede).
    parti = rel.split("/")[:-1]
    while parti:
        try:
            ftp.rmd("/".join(parti))
        except ftplib.all_errors:
            break
        parti.pop()
    return True


# ──────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default=BASE_DEFAULT)
    ap.add_argument("--manifesto", help="manifesto locale (default: scaricato dal sito)")
    ap.add_argument("--public", help="build locale, per la riparazione")
    ap.add_argument("--precedente", help="manifesto della build precedente: verifica tutto ciò che doveva cambiare")
    ap.add_argument("--pagine", nargs="*", default=[], help="pagine da controllare (/chi-siamo/ oppure chi-siamo/index.html)")
    ap.add_argument("--campione", type=int, default=0, help="N pagine HTML a caso dal manifesto")
    ap.add_argument("--seme", default="", help="seme del campione (es. il numero del run)")
    ap.add_argument("--max-cambiati", type=int, default=250, help="oltre, i file cambiati si campionano")
    ap.add_argument("--sha-atteso", "--sha", dest="sha_atteso", default="", help="SHA del deploy che ha generato il manifesto")
    ap.add_argument("--tentativi", "--retries", dest="tentativi", type=int, default=4)
    ap.add_argument("--attesa", "--wait", dest="attesa", type=int, default=30, help="secondi fra un tentativo e l'altro")
    ap.add_argument("--ore-massime", "--stale-hours", dest="ore_massime", type=int, default=12,
                    help="età massima dell'ultima build servita")
    ap.add_argument("--ripara", action="store_true", help="ricarica via FTPS i file diversi (serve --public)")
    ap.add_argument("--diagnostica", action="store_true", help="stampa le impronte senza giudicare")
    a = ap.parse_args()
    base = a.base.rstrip("/")

    log(f"=== Verifica del sito live contro il manifesto della build: {base} ===")

    # 1. Il manifesto di riferimento.
    manifesto_locale_bytes = b""
    if a.manifesto:
        manifesto = leggi_manifesto_locale(Path(a.manifesto))
        manifesto_locale_bytes = Path(a.manifesto).read_bytes()
        log(f"Manifesto locale: build {manifesto.get('sha')} ({manifesto.get('n_file')} file)")
    else:
        manifesto, _ = leggi_manifesto_live(base)
        if manifesto is None:
            log(f"❌ /{MANIFESTO} non leggibile dal sito: o il deploy non lo ha ancora caricato, o il sito non risponde.")
            return 1
        log(f"Manifesto live: build {manifesto.get('sha')} del {manifesto.get('time')} ({manifesto.get('n_file')} file)")
    file: dict[str, str] = manifesto.get("file") or {}
    errori: list[str] = []

    # 2. Coerenza fra manifesto, build-info.js e SHA atteso.
    sha_live, time_live = leggi_build_info(base)
    if a.sha_atteso and manifesto.get("sha") and not a.sha_atteso.startswith(manifesto["sha"]) \
            and not manifesto["sha"].startswith(a.sha_atteso):
        # Non è un errore: con due deploy ravvicinati il controllo del primo
        # parte quando il secondo è già online (i controlli si accodano). Si
        # verifica il sito contro ciò che dichiara di servire; se il manifesto
        # fosse vecchio per un caricamento a metà, lo dice il confronto con
        # build-info.js in fondo.
        log(f"ℹ️  Il manifesto servito è della build {manifesto['sha']}, non della {a.sha_atteso} attesa: "
            "probabile deploy successivo già online; verifico contro quello.")
    if time_live:
        try:
            t = dt.datetime.fromisoformat(time_live.replace("Z", "+00:00"))
            eta_h = (dt.datetime.now(dt.timezone.utc) - t).total_seconds() / 3600
            log(f"build-info.js: build {sha_live or '?'} del {time_live} ({eta_h:.1f} h fa)")
            if eta_h > a.ore_massime:
                errori.append(f"SITO CONGELATO: l'ultima build servita ha {eta_h:.0f} h (> {a.ore_massime} h)")
        except ValueError:
            log(f"build-info.js: orario non leggibile ({time_live!r})")
    else:
        log("⚠️  /build-info.js non leggibile")

    # 3. Che cosa controllare.
    da_controllare: dict[str, str] = {}  # rel → motivo
    for rel in CRITICHE:
        if rel in file:
            da_controllare[rel] = "critica"

    # Le tavole CAST/UDL sono una famiglia didattica a rilascio progressivo.
    # Verificarle TUTTE a ogni giro, non solo se selezionate dal campione:
    # l'FTP incrementale interrotto da merge ravvicinati può lasciare singole
    # SVG mancanti pur avendo già caricato la pagina HTML che le richiama.
    # La ricerca nel manifesto include automaticamente ogni tavola futura.
    for rel in file:
        if rel.startswith("formazione/illustrazioni-udl/") and rel.endswith(".svg") and verificabile(rel):
            da_controllare[rel] = "illustrazione CAST/UDL"

    ua = ultimo_articolo(file)
    if ua:
        da_controllare[ua] = "ultimo articolo"
    da_controllare[BUILD_INFO] = "build-info"
    for p in a.pagine:
        rel = p.strip("/")
        rel = "index.html" if rel == "" else (rel if "." in rel.split("/")[-1] else rel + "/index.html")
        if rel in file:
            da_controllare[rel] = "richiesta"
        else:
            errori.append(f"{p}: non è nel manifesto della build")
    rimossi: list[str] = []  # nel manifesto precedente, non più nella build: devono sparire dal sito
    if a.precedente:
        prima = leggi_manifesto_locale(Path(a.precedente)).get("file") or {}
        cambiati = sorted(k for k, v in file.items() if prima.get(k) != v and verificabile(k))
        rimossi = sorted(k for k in prima if k not in file and verificabile(k))
        log(f"File che questo deploy doveva cambiare o aggiungere: {len(cambiati)}; da togliere: {len(rimossi)}")
        if len(cambiati) > a.max_cambiati:
            rnd = random.Random(a.seme or None)
            scelti = rnd.sample(cambiati, a.max_cambiati)
            log(f"  (sono tanti: ne controllo {a.max_cambiati} a caso oltre alle pagine critiche)")
        else:
            scelti = cambiati
        for k in scelti:
            da_controllare.setdefault(k, "cambiato")
    if a.campione > 0:
        html = sorted(k for k in file if k.endswith(".html") and verificabile(k))
        rnd = random.Random(a.seme or None)
        for k in rnd.sample(html, min(a.campione, len(html))):
            da_controllare.setdefault(k, "campione")
    da_controllare = {k: v for k, v in da_controllare.items() if verificabile(k)}
    log(f"Pagine e file da controllare: {len(da_controllare)}")

    # 4. Controllo con ritentativi (propagazione subito dopo il caricamento).
    def controlla(rels: list[str]) -> dict[str, str]:
        """rel → esito: 'ok' | 'diverso' | 'assente(<status>)' | 'irraggiungibile'."""
        esiti = {}
        for rel in rels:
            st, corpo = scarica(url_di(base, rel))
            if rel in rimossi_set:
                # Deve NON esserci più: qualunque risposta diversa da 200 va bene.
                esiti[rel] = "irraggiungibile" if st == 0 else ("ok" if st != 200 else "ancora online")
                continue
            if st == 0:
                esiti[rel] = "irraggiungibile"
            elif reindirizzato(st):
                # Il server manda altrove (regola .htaccess): il file della build
                # non è confrontabile da fuori, e non è un file rimasto vecchio.
                esiti[rel] = f"ok(redirect {st})"
            elif st != 200:
                esiti[rel] = f"assente({st})"
            else:
                atteso = manifesto_locale_bytes and rel == MANIFESTO and sha256(manifesto_locale_bytes) or file.get(rel, "")
                if rel == MANIFESTO and manifesto_locale_bytes:
                    esiti[rel] = "ok" if corpo == manifesto_locale_bytes else "diverso"
                else:
                    esiti[rel] = "ok" if sha256(corpo) == atteso else "diverso"
        return esiti

    rimossi_set = set(rimossi[: a.max_cambiati])
    for k in rimossi_set:
        da_controllare[k] = "tolto dalla build"
    elenco = sorted(da_controllare)
    if manifesto_locale_bytes:
        elenco.append(MANIFESTO)
    esiti: dict[str, str] = {}
    pendenti = elenco
    for tentativo in range(1, max(1, a.tentativi) + 1):
        esiti.update(controlla(pendenti))
        pendenti = [r for r in elenco if not esiti.get(r, "").startswith("ok")]
        if a.diagnostica or not pendenti or tentativo == a.tentativi:
            break
        log(f"Tentativo {tentativo}: {len(pendenti)} file non coincidono, riprovo fra {a.attesa}s…")
        time.sleep(a.attesa)

    if a.diagnostica:
        for rel in elenco:
            log(f"  {esiti.get(rel, '?'):16s} {rel}  [{da_controllare.get(rel, 'manifesto')}]")
        log("(modalità diagnostica: nessun giudizio)")
        return 0

    # 5. Riparazione: ricarico dalla build locale i file diversi, poi ricontrollo.
    if pendenti and a.ripara:
        if not a.public:
            log("⚠️  --ripara richiede --public (la build locale da cui ricaricare).")
        else:
            public = Path(a.public)
            da_caricare = [r for r in pendenti if not esiti[r].startswith("irraggiungibile") and r not in rimossi_set]
            da_togliere = [r for r in pendenti if esiti[r] == "ancora online"]
            log(f"Riparazione: ricarico via FTPS {len(da_caricare)} file, ne tolgo {len(da_togliere)}…")
            conn = apri_ftps()
            if conn:
                ftp, radice = conn
                caricati = 0
                for rel in da_caricare:
                    if carica(ftp, radice, public, rel):
                        caricati += 1
                        log(f"   ↑ {rel}")
                for rel in da_togliere:
                    if cancella(ftp, radice, rel):
                        caricati += 1
                        log(f"   ✕ {rel}")
                try:
                    ftp.quit()
                except ftplib.all_errors:
                    pass
                log(f"Sistemati {caricati}/{len(da_caricare) + len(da_togliere)}. Ricontrollo…")
                time.sleep(5)
                esiti.update(controlla(pendenti))
                pendenti = [r for r in elenco if not esiti.get(r, "").startswith("ok")]

    # 6. Esito.
    log("")
    log("## Esito")
    for rel in pendenti:
        log(f"  ❌ {esiti[rel]:16s} {rel}  [{da_controllare.get(rel, 'manifesto')}]")
    ok = len(elenco) - len(pendenti)
    redir = [r for r in elenco if esiti.get(r, "").startswith("ok(redirect")]
    log(f"  {ok}/{len(elenco)} file coincidono con il manifesto della build.")
    for rel in redir:
        log(f"  ℹ️  {rel}: il server reindirizza ({esiti[rel]}), regola .htaccess — non confrontabile, non è un file vecchio.")
    for e in errori:
        log(f"  ❌ {e}")
    if sha_live and manifesto.get("sha") and sha_live != manifesto["sha"] and not pendenti and not a.manifesto:
        errori.append(f"build-info.js è della build {sha_live}, il manifesto della {manifesto['sha']}: caricamento a metà")
        log(f"  ❌ {errori[-1]}")
    log("")
    if not pendenti and not errori:
        log("✅ Le pagine servite coincidono con la build. Nessun file rimasto vecchio.")
        return 0
    log("❌ Guardia anti-stale: file diversi dalla build o incoerenze. Rimedio: rilanciare il deploy "
        "(lo step «Verifica e ripara» ricarica solo i file diversi) oppure "
        "`python3 scripts/verifica-deploy-aruba.py --manifesto public/build-manifest.json --public public --ripara` "
        "con le credenziali FTP. Mai cambiare lo state-name in deploy.yml (incidente 03/07/2026).")
    return 1


if __name__ == "__main__":
    sys.exit(main())
