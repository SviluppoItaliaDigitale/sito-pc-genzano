#!/usr/bin/env python3
"""
Caricamento del sito su Aruba: solo i file cambiati, con più collegamenti
FTPS in parallelo, ogni file sostituito in un colpo solo e ricontrollato.

Perché esiste (11/11/2026). L'azione FTP-Deploy carica un file per volta su
un solo collegamento: un deploy con un articolo nuovo (circa 590 file fra
pagine, indice di ricerca e cancellazioni) durava 6 minuti e mezzo, e con la
verifica dopo il caricamento il sito andava online in 13-18 minuti. Richiesta
di Alessandro: online in 1-2 minuti dall'unione, come gli altri siti. Sue
condizioni (11/11/2026), tutte rispettate qui:
  1. vanno online solo i file modificati;
  2. mai due caricamenti nello stesso momento (fila del workflow, più il
     lucchetto sul server qui sotto);
  3. un file cambiato più volte arriva sempre nella versione più recente,
     mai una vecchia dopo una nuova;
  4. niente file a metà, persi o bloccati: nome provvisorio e poi
     rinomina, ripresa dei file falliti, controllo finale; se anche un solo
     file non torna, uscita in errore e manifesto del server non aggiornato;
  5. prima i file da cui dipendono le pagine, poi le pagine, poi gli indici,
     per ultime le cancellazioni.

Che cosa fa, in ordine:
  - prende il lucchetto sul server (cartella `.carica-aruba-lucchetto`:
    MKD è atomico, il secondo che arriva aspetta); un lucchetto senza
    battito da 5 minuti è di un caricamento morto e si toglie;
  - legge lo stato del server: il file di stato dell'azione FTP-Deploy
    (`--stato-nome`, stesso formato e stessa impronta sha256), il manifesto
    servito dal sito (`--manifesto-servito`) e l'elenco dei file in sospeso
    lasciato da un giro interrotto (`.carica-aruba-in-sospeso.json`);
  - calcola il piano: file nuovi o diversi, file in sospeso, file che il
    manifesto servito dà diversi dalla build (deriva), cancellazioni;
  - scrive PRIMA di toccare qualunque file l'elenco in sospeso (tutto ciò
    che sta per toccare): se il giro muore a metà, il successivo ricarica
    quei file anche se la build nel frattempo è tornata alla versione di
    prima;
  - carica per fasi, ognuna finita prima della successiva: cartelle nuove,
    risorse (CSS, JS, immagini, PDF, frammenti della ricerca), pagine HTML
    (le nuove per prime), indici (home, elenchi, feed, sitemap, ingresso
    della ricerca, build-info.js), cancellazioni, cartelle vuote;
  - ogni file va su un nome provvisorio nella stessa cartella e poi si
    rinomina sul nome vero; subito dopo si riscarica e se ne confronta
    l'impronta con la build; fino a 4 tentativi per file;
  - alla fine controlla la dimensione di tutti i file caricati e l'assenza
    di quelli cancellati; solo se tutto torna carica il manifesto della
    build, poi il file di stato, poi toglie l'elenco in sospeso.

Se qualcosa fallisce dopo il primo file toccato, esce con 1: il workflow
diventa rosso, il manifesto servito e il file di stato restano quelli
dell'ultimo giro riuscito, e il giro successivo ricarica tutto ciò che è
ancora diverso più ciò che era in sospeso. Se fallisce prima di toccare
qualunque cosa (collegamento, accesso), esce con 3 e il workflow può usare
l'azione FTP-Deploy come ripiego: legge lo stesso file di stato, quindi
riparte da dove questo script l'ha lasciato.

🔴 Il file di stato porta il nome di sempre (`state-name` in deploy.yml) e
lo stesso formato: non si cambia mai (incidente del 03/07/2026, un nome
nuovo vuol dire ricaricare tutto il sito, ore). Mai `documenti/`, gestita
a mano sul server.

Credenziali da FTP_SERVER (anche host:porta), FTP_USERNAME, FTP_PASSWORD,
cartella FTP_SERVER_DIR. FTP_TLS_INSECURE=1 solo per il server di prova
locale (certificato autofirmato). Le credenziali non si stampano mai.

Uso:
  python3 scripts/carica-aruba.py --public public \
      --stato-nome .ftp-deploy-sync-state-2026-06-09.json \
      --manifesto-servito /tmp/manifesto-precedente.json --connessioni 4
  python3 scripts/carica-aruba.py ... --piano      # solo il piano, nessuna modifica

Uscita: 0 tutto caricato e verificato · 1 caricamento iniziato e non
riuscito (niente ripiego) · 2 errore d'uso · 3 nulla toccato (ripiego
ammesso) · 4 nessun riferimento sullo stato del server (né file di stato né
manifesto: il ripiego ricaricherebbe tutto, quindi no) · 5 il server è
occupato da un altro caricamento oltre l'attesa massima.
Prove: scripts/prova-carica-aruba.py (server FTPS locale). Solo Python standard.
"""

from __future__ import annotations

import argparse
import ftplib
import hashlib
import io
import json
import os
import queue
import re
import signal
import socket
import ssl
import sys
import threading
import time
from pathlib import Path, PurePosixPath

LUCCHETTO = ".carica-aruba-lucchetto"
LUCCHETTO_INFO = f"{LUCCHETTO}/chi.json"
SOSPESI = ".carica-aruba-in-sospeso.json"
SUFFISSO_TMP = ".pcgz-tmp"
MANIFESTO = "build-manifest.json"
BATTITO_S = 60           # ogni quanto il lucchetto dice «sono vivo»
LUCCHETTO_MORTO_S = 300  # oltre (5 battiti mancati), il lucchetto è di un caricamento morto
TENTATIVI = 4
DESCRIZIONE_STATO = (
    "DO NOT DELETE THIS FILE. This file is used to keep track of which files have been synced "
    "in the most recent deployment. If you delete this file a resync will need to be done "
    "(which can take a while) - read more: https://github.com/SamKirkland/FTP-Deploy-Action")

# Pagine che il cittadino cerca per prime: dentro la fase delle pagine
# vanno subito dopo quelle nuove.
PAGINE_PRIMA = (
    "emergenza/index.html", "allerte-meteo/index.html", "cosa-fare-adesso/index.html",
    "numeri-utili/index.html",
)

ESITI = {0: "ok", 1: "rosso", 2: "uso", 3: "ripiego", 4: "blocca", 5: "occupato"}


def log(msg: str = "") -> None:
    print(msg, flush=True)


def escluso(rel: str) -> bool:
    """Ciò che il caricamento non tocca mai: documenti/ (gestita a mano sul
    server, come `exclude: **/documenti/**` dell'azione), i file di servizio
    dell'azione e di questo script, i nomi provvisori."""
    parti = rel.split("/")
    if "documenti" in parti:
        return True
    nome = parti[-1]
    if nome.startswith(".ftp-deploy-sync") or nome.startswith(".carica-aruba-") \
            or nome.endswith(SUFFISSO_TMP) or rel.startswith(LUCCHETTO):
        return True
    return False


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for blocco in iter(lambda: f.read(1 << 20), b""):
            h.update(blocco)
    return h.hexdigest()


def elenco_locale(public: Path) -> tuple[dict[str, tuple[int, str]], set[str]]:
    """rel → (dimensione, sha256) dei file della build; cartelle."""
    file: dict[str, tuple[int, str]] = {}
    cartelle: set[str] = set()
    for radice, dirs, nomi in os.walk(public, followlinks=False):
        rrel = os.path.relpath(radice, public).replace(os.sep, "/")
        rrel = "" if rrel == "." else rrel
        tieni = []
        for d in sorted(dirs):
            rel = f"{rrel}/{d}" if rrel else d
            if os.path.islink(os.path.join(radice, d)) or escluso(rel):
                continue
            tieni.append(d)
            cartelle.add(rel)
        dirs[:] = tieni
        for n in nomi:
            rel = f"{rrel}/{n}" if rrel else n
            p = Path(radice) / n
            if p.is_symlink() or not p.is_file() or escluso(rel):
                continue
            file[rel] = (p.stat().st_size, sha256_file(p))
    return file, cartelle


def stato_json(file: dict[str, tuple[int, str]], cartelle: set[str]) -> bytes:
    """Il file di stato nel formato dell'azione FTP-Deploy v4.4.0
    (JSON.stringify(stato, undefined, 4): rientro di 4 spazi, cartelle
    senza «size», file con size e hash sha256 esadecimale)."""
    dati = [{"type": "folder", "name": c} for c in sorted(cartelle)]
    dati += [{"type": "file", "name": r, "size": s, "hash": h} for r, (s, h) in sorted(file.items())]
    obj = {"description": DESCRIZIONE_STATO, "version": "1.0.0",
           "generatedTime": int(time.time() * 1000), "data": dati}
    return json.dumps(obj, indent=4, ensure_ascii=False).encode("utf-8")


def fase_di(rel: str) -> str:
    if rel == MANIFESTO:
        return "manifesto"
    nome = rel.rsplit("/", 1)[-1]
    if (rel in ("index.html", "build-info.js", "pagefind/pagefind-entry.json", "robots.txt")
            or rel == "comunicazioni/index.html"
            or re.search(r"(^|/)page/\d+/index\.html$", rel)
            or nome.endswith(".xml") or nome == "index.json"):
        return "indici"
    if nome.endswith((".html", ".htm")):
        return "pagine"
    return "risorse"


def cartella_di(rel: str) -> str:
    return rel.rsplit("/", 1)[0] if "/" in rel else ""


def tmp_di(rel: str) -> str:
    c = cartella_di(rel)
    nome = "." + rel.rsplit("/", 1)[-1] + SUFFISSO_TMP
    return f"{c}/{nome}" if c else nome


# ──────────────────────────────────────────────────────────────
# FTPS
# ──────────────────────────────────────────────────────────────

class FTPS(ftplib.FTP_TLS):
    """Riuso della sessione TLS sul canale dati (Aruba lo richiede, come
    scripts/verifica-deploy-aruba.py)."""

    def ntransfercmd(self, cmd, rest=None):
        conn, size = ftplib.FTP.ntransfercmd(self, cmd, rest)
        if self._prot_p:
            conn = self.context.wrap_socket(conn, server_hostname=self.host,
                                            session=self.sock.session)  # type: ignore[attr-defined]
        return conn, size


class ErroreAccesso(Exception):
    pass


# ftplib.all_errors è una tupla (comprende OSError): si unisce, non si annida.
ERRORI_RETE = ftplib.all_errors + (ErroreAccesso,)


class Server:
    """Parametri di collegamento e livello TLS che funziona (lo si trova una
    volta, poi ogni collegamento lo riusa)."""

    def __init__(self) -> None:
        server = os.environ.get("FTP_SERVER", "")
        self.utente = os.environ.get("FTP_USERNAME", "")
        self.password = os.environ.get("FTP_PASSWORD", "")
        self.cartella = os.environ.get("FTP_SERVER_DIR", "/www.protezionecivilegenzano.it/")
        if not (server and self.utente and self.password):
            raise ErroreAccesso("FTP_SERVER / FTP_USERNAME / FTP_PASSWORD non impostati")
        self.porta = 21
        if ":" in server:
            server, p = server.rsplit(":", 1)
            self.porta = int(p)
        self.host = server
        self.ctx: ssl.SSLContext | None = None
        self._lock = threading.Lock()

    def _livelli(self) -> list[tuple[str, ssl.SSLContext]]:
        # Stessi tre livelli di verifica-deploy-aruba.py: il certificato
        # dell'FTP di Aruba è emesso per un nome diverso dall'host (01/10/2026).
        liv: list[tuple[str, ssl.SSLContext]] = []
        if os.environ.get("FTP_TLS_INSECURE") != "1":
            liv.append(("verifica piena", ssl.create_default_context()))
            c = ssl.create_default_context()
            c.check_hostname = False
            liv.append(("catena verificata, nome host non controllato", c))
        c = ssl.create_default_context()
        c.check_hostname = False
        c.verify_mode = ssl.CERT_NONE
        liv.append(("senza verifica del certificato, come l'azione FTP-Deploy", c))
        return liv

    def apri(self) -> FTPS:
        with self._lock:
            livelli = [("già scelto", self.ctx)] if self.ctx else self._livelli()
        ultimo = ""
        for nome, ctx in livelli:
            ftp = FTPS(context=ctx, timeout=60)
            try:
                ftp.connect(self.host, self.porta)
                ftp.login(self.utente, self.password)
                ftp.prot_p()
                ftp.set_pasv(True)
                ftp.cwd(self.cartella)
                ftp.voidcmd("TYPE I")
                with self._lock:
                    if self.ctx is None:
                        self.ctx = ctx
                        if nome != "verifica piena":
                            log(f"ℹ️  FTPS: {nome}.")
                return ftp
            except ftplib.all_errors as e:
                ultimo = f"{type(e).__name__}: {e}"
                try:
                    ftp.close()
                except Exception:
                    pass
                if "CERTIFICATE_VERIFY_FAILED" not in ultimo and "SSL" not in type(e).__name__:
                    break
        raise ErroreAccesso(f"collegamento FTPS non riuscito ({ultimo})")


class Collegamenti:
    """Un collegamento per thread, riaperto dopo un errore."""

    def __init__(self, server: Server) -> None:
        self.server = server
        self.locale = threading.local()
        self.tutti: list[FTPS] = []
        self._lock = threading.Lock()

    def prendi(self) -> FTPS:
        ftp = getattr(self.locale, "ftp", None)
        if ftp is None:
            ftp = self.server.apri()
            self.locale.ftp = ftp
            with self._lock:
                self.tutti.append(ftp)
        return ftp

    def butta(self) -> None:
        ftp = getattr(self.locale, "ftp", None)
        self.locale.ftp = None
        if ftp is not None:
            try:
                ftp.close()
            except Exception:
                pass

    def chiudi_tutti(self) -> None:
        with self._lock:
            for f in self.tutti:
                try:
                    f.quit()
                except Exception:
                    try:
                        f.close()
                    except Exception:
                        pass
            self.tutti = []


def scarica_bytes(ftp: FTPS, rel: str) -> bytes | None:
    """Contenuto di un file del server; None se non esiste (550)."""
    buf = io.BytesIO()
    try:
        ftp.retrbinary(f"RETR {rel}", buf.write)
    except ftplib.error_perm as e:
        if str(e).startswith("550"):
            return None
        raise
    return buf.getvalue()


def sha_remoto(ftp: FTPS, rel: str) -> str | None:
    h = hashlib.sha256()
    try:
        ftp.retrbinary(f"RETR {rel}", h.update)
    except ftplib.error_perm as e:
        if str(e).startswith("550"):
            return None
        raise
    return h.hexdigest()


def esiste(ftp: FTPS, rel: str) -> bool:
    try:
        ftp.size(rel)
        return True
    except ftplib.error_perm:
        return False


# ──────────────────────────────────────────────────────────────

class Caricamento:
    def __init__(self, a: argparse.Namespace) -> None:
        self.a = a
        self.public = Path(a.public)
        self.server = Server()
        self.coll = Collegamenti(self.server)
        self.toccato = False          # da qui in poi niente ripiego
        self.rinomina_sopra: bool | None = None  # il server rinomina sopra un file esistente?
        self._rlock = threading.Lock()
        self.cartelle_fatte: set[str] = set()
        self._clock = threading.Lock()
        self.errori: list[str] = []
        self.battito_stop = threading.Event()
        self.lucchetto_mio = False
        self.contatori = {"caricati": 0, "tentativi_in_più": 0, "cancellati": 0}

    def con_riprova(self, fn):
        """Esegue fn(ftp) sul collegamento del thread; se il collegamento
        cade (non un rifiuto 5xx del server), lo riapre e riprova fino a 3
        volte. Serve ai passi in fila: un collegamento rimasto fermo durante
        le fasi in parallelo può essere stato chiuso dal server."""
        ultimo: Exception | None = None
        for t in range(1, 4):
            try:
                return fn(self.coll.prendi())
            except ERRORI_RETE as e:
                if isinstance(e, ftplib.error_perm):
                    raise
                ultimo = e
                self.coll.butta()
                time.sleep(2 * t)
        assert ultimo is not None
        raise ultimo

    # ── lucchetto ──────────────────────────────────────────────
    def _scrivi_info_lucchetto(self, ftp: FTPS) -> None:
        info = json.dumps({"run": self.a.run_id, "battito": int(time.time())}).encode()
        ftp.storbinary(f"STOR {LUCCHETTO_INFO}", io.BytesIO(info))

    def prendi_lucchetto(self) -> bool:
        inizio = time.time()
        avvisato = False

        def prova_mkd(ftp: FTPS) -> bool:
            try:
                ftp.mkd(LUCCHETTO)
            except ftplib.error_perm:
                return False
            self.lucchetto_mio = True
            self._scrivi_info_lucchetto(ftp)
            return True

        while True:
            if self.con_riprova(prova_mkd):
                log(f"🔒 Lucchetto preso (giro {self.a.run_id}).")
                return True
            ftp = self.coll.prendi()
            dati = self.con_riprova(lambda f: scarica_bytes(f, LUCCHETTO_INFO))
            chi, battito = "?", 0
            try:
                d = json.loads(dati or b"{}")
                chi, battito = str(d.get("run", "?")), int(d.get("battito", 0))
            except ValueError:
                pass
            eta = time.time() - battito if battito else None
            if eta is None:
                # cartella senza info leggibile: un giro morto fra MKD e STOR, o appena nato
                eta = self.a.lucchetto_morto + 1 if time.time() - inizio > 60 else 0
            if eta is not None and eta > self.a.lucchetto_morto:
                log(f"⚠️  Lucchetto del giro {chi} senza battito da {int(eta)} s: lo tolgo.")
                for cmd in (lambda: ftp.delete(LUCCHETTO_INFO), lambda: ftp.rmd(LUCCHETTO)):
                    try:
                        cmd()
                    except ftplib.error_perm:
                        pass
                continue
            if time.time() - inizio > self.a.attesa_lucchetto:
                log(f"❌ Il server è occupato dal caricamento del giro {chi} da oltre "
                    f"{self.a.attesa_lucchetto} s: non carico insieme a lui.")
                return False
            if not avvisato:
                log(f"⏳ Un altro caricamento (giro {chi}) è in corso: attendo che finisca.")
                avvisato = True
            time.sleep(self.a.pausa_lucchetto)

    def _battito(self) -> None:
        while not self.battito_stop.wait(BATTITO_S):
            try:
                ftp = self.server.apri()
                self._scrivi_info_lucchetto(ftp)
                ftp.quit()
            except Exception as e:  # il battito non deve mai fermare il caricamento
                log(f"⚠️  Battito del lucchetto non scritto ({type(e).__name__}).")

    def lascia_lucchetto(self) -> None:
        self.battito_stop.set()
        if not self.lucchetto_mio:
            return
        try:
            ftp = self.server.apri()
            try:
                ftp.delete(LUCCHETTO_INFO)
            except ftplib.error_perm:
                pass
            ftp.rmd(LUCCHETTO)
            ftp.quit()
            log("🔓 Lucchetto lasciato.")
        except Exception as e:
            log(f"⚠️  Lucchetto non tolto ({type(e).__name__}: {e}): il prossimo giro lo toglierà dopo "
                f"{self.a.lucchetto_morto // 60} minuti senza battito.")

    # ── operazioni sui file ────────────────────────────────────
    def assicura_cartella(self, ftp: FTPS, c: str) -> None:
        if not c:
            return
        parti = c.split("/")
        for i in range(1, len(parti) + 1):
            sub = "/".join(parti[:i])
            with self._clock:
                if sub in self.cartelle_fatte:
                    continue
            try:
                ftp.mkd(sub)
            except ftplib.error_perm:
                pass  # esiste già (o lo dirà la STOR)
            with self._clock:
                self.cartelle_fatte.add(sub)

    def _sostituisci(self, ftp: FTPS, tmp: str, rel: str) -> None:
        """Rinomina il provvisorio sul nome vero. Se il server non permette
        di rinominare sopra un file esistente, cancella prima il vecchio:
        il file manca per il tempo di un comando, mai a metà."""
        if self.rinomina_sopra is not False:
            try:
                ftp.rename(tmp, rel)
                return
            except ftplib.error_perm:
                if self.rinomina_sopra:
                    raise
        try:
            ftp.delete(rel)
        except ftplib.error_perm:
            pass
        ftp.rename(tmp, rel)

    def prova_rinomina(self) -> None:
        self.con_riprova(self._prova_rinomina)

    def _prova_rinomina(self, ftp: FTPS) -> None:
        """Il server rinomina sopra un file esistente? Si prova una volta
        con due file di servizio, così il log del primo deploy lo dice."""
        a, b = ".carica-aruba-prova-a", ".carica-aruba-prova-b"
        try:
            ftp.storbinary(f"STOR {a}", io.BytesIO(b"nuovo"))
            ftp.storbinary(f"STOR {b}", io.BytesIO(b"vecchio"))
            try:
                ftp.rename(a, b)
                self.rinomina_sopra = scarica_bytes(ftp, b) == b"nuovo"
            except ftplib.error_perm:
                self.rinomina_sopra = False
        finally:
            for n in (a, b):
                try:
                    ftp.delete(n)
                except ftplib.error_perm:
                    pass
        log("ℹ️  Il server rinomina sopra un file esistente: "
            + ("sì, la sostituzione è atomica." if self.rinomina_sopra else
               "no, si cancella il vecchio e si rinomina subito dopo (assenza di un istante, mai un file a metà)."))

    def carica_uno(self, rel: str, atteso: str) -> bool:
        locale = self.public / rel
        tmp = tmp_di(rel)
        ultimo = ""
        for t in range(1, TENTATIVI + 1):
            try:
                ftp = self.coll.prendi()
                self.assicura_cartella(ftp, cartella_di(rel))
                with locale.open("rb") as f:
                    ftp.storbinary(f"STOR {tmp}", f)
                self._sostituisci(ftp, tmp, rel)
                letto = sha_remoto(ftp, rel)
                if letto == atteso:
                    with self._rlock:
                        self.contatori["caricati"] += 1
                        self.contatori["tentativi_in_più"] += t - 1
                    if t > 1:
                        log(f"   ↻ {rel}: riuscito al tentativo {t}")
                    return True
                ultimo = "contenuto sul server diverso dalla build"
            except ERRORI_RETE as e:
                ultimo = f"{type(e).__name__}: {str(e)[:160]}"
                self.coll.butta()
            log(f"   ⚠️  {rel}: tentativo {t} non riuscito ({ultimo})")
            if t < TENTATIVI:
                time.sleep(min(2 * t, 8))
        # Nome provvisorio rimasto: lo si toglie, se si riesce.
        try:
            self.coll.prendi().delete(tmp)
        except Exception:
            self.coll.butta()
        self.errori.append(f"{rel}: non caricato dopo {TENTATIVI} tentativi ({ultimo})")
        return False

    def cancella_uno(self, rel: str) -> bool:
        ultimo = ""
        for t in range(1, TENTATIVI + 1):
            try:
                ftp = self.coll.prendi()
                try:
                    ftp.delete(rel)
                except ftplib.error_perm as e:
                    if not str(e).startswith("550"):
                        raise
                if not esiste(ftp, rel):
                    with self._rlock:
                        self.contatori["cancellati"] += 1
                    return True
                ultimo = "ancora presente"
            except ERRORI_RETE as e:
                ultimo = f"{type(e).__name__}: {str(e)[:160]}"
                self.coll.butta()
            if t < TENTATIVI:
                time.sleep(min(2 * t, 8))
        self.errori.append(f"{rel}: non cancellato ({ultimo})")
        return False

    def in_parallelo(self, lavori: list, funzione, nome: str) -> bool:
        if not lavori:
            return True
        t0 = time.time()
        q: queue.Queue = queue.Queue()
        for x in lavori:
            q.put(x)
        esiti: list[bool] = []
        lock = threading.Lock()

        rifiutati: list[str] = []

        def lavoratore() -> None:
            try:
                self.coll.prendi()
            except ErroreAccesso as e:
                # Il server non accetta un collegamento in più (limite per
                # indirizzo): si prosegue con quelli che ci sono.
                with lock:
                    rifiutati.append(str(e)[:120])
                return
            while True:
                try:
                    x = q.get_nowait()
                except queue.Empty:
                    return
                try:
                    ok = funzione(*x) if isinstance(x, tuple) else funzione(x)
                except Exception as e:  # un errore imprevisto conta come fallimento, mai come riuscita
                    self.errori.append(f"{x}: errore imprevisto ({type(e).__name__}: {str(e)[:160]})")
                    ok = False
                with lock:
                    esiti.append(ok)

        n = max(1, min(self.a.connessioni, len(lavori)))
        th = [threading.Thread(target=lavoratore, daemon=True) for _ in range(n)]
        for x in th:
            x.start()
        for x in th:
            x.join()
        falliti = len(lavori) - esiti.count(True)
        if rifiutati:
            log(f"   ℹ️  {nome}: {len(rifiutati)} collegamenti su {n} rifiutati dal server, "
                f"lavoro fatto con {n - len(rifiutati)} ({rifiutati[0]})")
        log(f"   {nome}: {len(lavori) - falliti}/{len(lavori)} in {time.time() - t0:.1f} s"
            + (f" — ❌ {falliti} non riusciti" if falliti else ""))
        return falliti == 0

    # ── piano ──────────────────────────────────────────────────
    def piano(self, loc: dict, loc_dirs: set) -> dict | None:
        ftp = self.coll.prendi()
        stato = None
        grezzo = scarica_bytes(ftp, self.a.stato_nome)
        if grezzo is not None:
            try:
                stato = json.loads(grezzo.decode("utf-8"))
            except ValueError:
                log("⚠️  File di stato del server illeggibile.")
                stato = None
        manifesto = None
        if self.a.manifesto_servito and Path(self.a.manifesto_servito).is_file():
            try:
                manifesto = json.loads(Path(self.a.manifesto_servito).read_text(encoding="utf-8"))
            except ValueError:
                manifesto = None
        sospesi_raw = scarica_bytes(ftp, SOSPESI)
        sospesi: list[str] = []
        if sospesi_raw:
            try:
                d = json.loads(sospesi_raw.decode("utf-8"))
                sospesi = [r for r in d.get("file", []) if isinstance(r, str) and not escluso(r)]
                log(f"⚠️  Il giro {d.get('run', '?')} si è interrotto: {len(sospesi)} file in sospeso da ricaricare o togliere.")
            except ValueError:
                log("⚠️  Elenco dei file in sospeso illeggibile: lo ignoro e mi affido al confronto.")

        srv: dict[str, str] = {}
        srv_dirs: set[str] = set()
        if stato is not None:
            for e in stato.get("data", []):
                nome = e.get("name", "")
                if not nome or escluso(nome):
                    continue
                if e.get("type") == "file":
                    srv[nome] = e.get("hash", "")
                elif e.get("type") == "folder":
                    srv_dirs.add(nome)
            fonte = f"file di stato del server ({len(srv)} file)"
        elif manifesto is not None:
            srv = {k: v for k, v in (manifesto.get("file") or {}).items() if not escluso(k)}
            fonte = (f"manifesto servito ({len(srv)} file; senza file di stato, i file che il "
                     "manifesto non elenca, come i frammenti della ricerca, si ricaricano tutti)")
        else:
            log("❌ Né il file di stato né il manifesto servito sono leggibili: non so che cosa c'è sul "
                "server. Non carico (il ripiego ricaricherebbe l'intero sito per ore).")
            return None
        log(f"Riferimento: {fonte}.")

        carica = {r for r, (_, h) in loc.items() if srv.get(r) != h}
        deriva: set[str] = set()
        if manifesto is not None and stato is not None:
            for r, h in (manifesto.get("file") or {}).items():
                if r in loc and h != loc[r][1] and r not in carica and not escluso(r):
                    deriva.add(r)
        if deriva:
            log(f"⚠️  {len(deriva)} file che il manifesto servito dà diversi dalla build: li ricarico.")
        carica |= deriva
        cancella = {r for r in srv if r not in loc}
        if manifesto is not None:
            cancella |= {r for r in (manifesto.get("file") or {}) if r not in loc and not escluso(r)}
        for r in sospesi:
            (carica if r in loc else cancella).add(r)
        cartelle_via = sorted((d for d in srv_dirs if d not in loc_dirs), key=lambda d: -d.count("/"))
        return {"carica": carica, "cancella": cancella, "cartelle_via": cartelle_via,
                "srv": srv, "srv_dirs": srv_dirs, "sospesi": set(sospesi)}

    # ── giro intero ────────────────────────────────────────────
    def esegui(self) -> int:
        t_inizio = time.time()
        if not self.public.is_dir():
            log(f"❌ {self.public}: cartella della build inesistente.")
            return 2
        loc, loc_dirs = elenco_locale(self.public)
        if MANIFESTO not in loc:
            log(f"❌ {MANIFESTO} manca nella build: va generato prima (genera-manifest-build.py).")
            return 2
        log(f"Build: {len(loc)} file, {len(loc_dirs)} cartelle ({time.time() - t_inizio:.1f} s per le impronte).")
        try:
            self.coll.prendi()
        except ErroreAccesso as e:
            log(f"❌ {e}")
            return 3
        if not self.a.piano and not self.prendi_lucchetto():
            return 5
        try:
            if not self.a.piano:
                threading.Thread(target=self._battito, daemon=True).start()
            p = self.con_riprova(lambda _f: self.piano(loc, loc_dirs))
            if p is None:
                return 4
            carica = p["carica"] - {MANIFESTO}
            fasi: dict[str, list[str]] = {"risorse": [], "pagine": [], "indici": []}
            for r in carica:
                fasi[fase_di(r)].append(r)
            nuovi = {r for r in carica if r not in p["srv"]}
            fasi["risorse"].sort(key=lambda r: (-loc[r][0], r))  # i grandi per primi: finiscono insieme
            fasi["pagine"].sort(key=lambda r: (r not in nuovi, r not in PAGINE_PRIMA, r))
            fasi["indici"].sort(key=lambda r: (r == "build-info.js", r))
            cancella = sorted(p["cancella"])
            peso = sum(loc[r][0] for r in carica)
            log(f"Piano: {len(fasi['risorse'])} risorse, {len(fasi['pagine'])} pagine, "
                f"{len(fasi['indici'])} indici ({peso / 1e6:.1f} MB; {len(nuovi)} file nuovi), "
                f"{len(cancella)} cancellazioni, {len(p['cartelle_via'])} cartelle da togliere.")
            if self.a.piano:
                for nome in ("risorse", "pagine", "indici"):
                    for r in fasi[nome]:
                        log(f"  {nome:8s} {'nuovo   ' if r in nuovi else 'cambiato'} {r}")
                for r in cancella:
                    log(f"  cancella          {r}")
                return 0

            # Prima di toccare qualunque file: l'elenco in sospeso.
            tutti = sorted(set(carica) | set(cancella) | p["sospesi"] | {MANIFESTO})
            self.toccato = True
            sospesi = json.dumps({"run": self.a.run_id, "inizio": int(time.time()), "file": tutti}).encode("utf-8")
            self.con_riprova(lambda f: f.storbinary(f"STOR {SOSPESI}", io.BytesIO(sospesi)))
            self.prova_rinomina()

            nuove_cartelle = sorted({cartella_di(r) for r in carica if cartella_di(r)} - p["srv_dirs"],
                                    key=lambda d: (d.count("/"), d))
            if nuove_cartelle:
                t0 = time.time()
                for d in nuove_cartelle:  # in fila: le genitrici prima delle figlie
                    self.con_riprova(lambda f, d=d: self.assicura_cartella(f, d))
                log(f"   cartelle nuove: {len(nuove_cartelle)} in {time.time() - t0:.1f} s")

            for nome in ("risorse", "pagine", "indici"):
                lavori = [(r, loc[r][1]) for r in fasi[nome]]
                if not self.in_parallelo(lavori, self.carica_uno, nome):
                    return self._fallito()
            if not self.in_parallelo(cancella, self.cancella_uno, "cancellazioni"):
                return self._fallito()
            for d in p["cartelle_via"]:  # in fila, dalle più profonde
                try:
                    self.con_riprova(lambda f, d=d: f.rmd(d))
                except ftplib.error_perm:
                    pass  # non vuota (file non della build) o già tolta: resta

            # Controllo finale: dimensione di ogni file caricato, assenza dei cancellati.
            t0 = time.time()
            diversi: list[str] = []
            dlock = threading.Lock()

            def controlla(r: str) -> bool:
                for t in range(1, 3):
                    try:
                        dim = self.coll.prendi().size(r)
                        if dim != loc[r][0]:
                            with dlock:
                                diversi.append(f"{r}: {dim} byte sul server, {loc[r][0]} nella build")
                            return False
                        return True
                    except ERRORI_RETE as e:
                        self.coll.butta()
                        if t == 2:
                            with dlock:
                                diversi.append(f"{r}: non leggibile ({type(e).__name__})")
                return False
            self.in_parallelo(sorted(carica), controlla, "controllo finale")
            if diversi:
                self.errori.extend(diversi)
                return self._fallito()
            log(f"   controllo finale chiuso in {time.time() - t0:.1f} s")

            # Tutto torna: manifesto, poi stato, poi via l'elenco in sospeso.
            if MANIFESTO in p["carica"] and not self.carica_uno(MANIFESTO, loc[MANIFESTO][1]):
                return self._fallito()
            stato = stato_json(loc, loc_dirs)
            tmp = tmp_di(self.a.stato_nome)

            def scrivi_stato(f: FTPS) -> str | None:
                f.storbinary(f"STOR {tmp}", io.BytesIO(stato))
                self._sostituisci(f, tmp, self.a.stato_nome)
                return sha_remoto(f, self.a.stato_nome)
            if self.con_riprova(scrivi_stato) != hashlib.sha256(stato).hexdigest():
                self.errori.append("file di stato: contenuto sul server diverso da quello scritto")
                return self._fallito()

            def togli_sospesi(f: FTPS) -> None:
                try:
                    f.delete(SOSPESI)
                except ftplib.error_perm:
                    pass
            self.con_riprova(togli_sospesi)
            c = self.contatori
            log(f"✅ Caricamento riuscito in {time.time() - t_inizio:.0f} s: {c['caricati']} file caricati e "
                f"ricontrollati ({c['tentativi_in_più']} tentativi in più), {c['cancellati']} cancellati.")
            return 0
        except ERRORI_RETE as e:
            self.errori.append(f"{type(e).__name__}: {str(e)[:200]}")
            if not self.toccato:
                log(f"❌ Errore prima di toccare qualunque file: {self.errori[-1]}")
                return 3
            return self._fallito()
        finally:
            if not self.a.piano:
                self.lascia_lucchetto()
            self.coll.chiudi_tutti()

    def _fallito(self) -> int:
        log("")
        log("❌ Caricamento non completo. Il manifesto servito e il file di stato restano quelli "
            "dell'ultimo giro riuscito; l'elenco dei file in sospeso resta sul server, quindi il "
            "prossimo giro li ricarica tutti.")
        for e in self.errori[:40]:
            log(f"   • {e}")
        if len(self.errori) > 40:
            log(f"   … e altri {len(self.errori) - 40}")
        return 1


def _interrompi(*_args) -> None:
    raise KeyboardInterrupt


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--public", default="public")
    ap.add_argument("--stato-nome", required=True, help="nome del file di stato dell'azione FTP-Deploy (state-name)")
    ap.add_argument("--manifesto-servito", default="", help="manifesto scaricato dal sito prima del caricamento")
    ap.add_argument("--connessioni", type=int, default=4)
    ap.add_argument("--run-id", default=os.environ.get("GITHUB_RUN_ID", f"locale-{os.getpid()}"))
    ap.add_argument("--attesa-lucchetto", type=int, default=1200, help="secondi massimi di attesa se il server è occupato")
    ap.add_argument("--pausa-lucchetto", type=int, default=10)
    ap.add_argument("--lucchetto-morto", type=int, default=LUCCHETTO_MORTO_S,
                    help="secondi senza battito dopo i quali un lucchetto è di un giro morto")
    ap.add_argument("--piano", action="store_true", help="mostra il piano senza modificare il server")
    a = ap.parse_args()
    if a.connessioni < 1 or a.connessioni > 10:
        log("❌ --connessioni fra 1 e 10.")
        return 2
    socket.setdefaulttimeout(90)
    # Un job annullato o scaduto riceve SIGINT e poi SIGTERM: in entrambi i
    # casi si esce dai blocchi finally, quindi il lucchetto si lascia e
    # l'elenco in sospeso resta sul server per il giro successivo.
    signal.signal(signal.SIGTERM, _interrompi)
    try:
        rc = Caricamento(a).esegui()
    except ErroreAccesso as e:
        log(f"❌ {e}")
        rc = 3
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write(f"esito={ESITI.get(rc, 'rosso')}\n")
    return rc


if __name__ == "__main__":
    sys.exit(main())
