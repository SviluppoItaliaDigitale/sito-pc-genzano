#!/usr/bin/env python3
"""
Prove di scripts/carica-aruba.py contro un server FTPS locale (pyftpdlib,
TLS con certificato autofirmato): nessun collegamento ad Aruba.

Ogni prova costruisce una build finta, prepara il server com'era dopo
l'ultimo giro riuscito (file + file di stato nel formato dell'azione
FTP-Deploy) e lancia lo script come processo vero, con più collegamenti.
Il server registra ogni comando (STOR, RNTO, DELE, MKD, RMD) con l'ora,
così l'ordine si controlla davvero.

Prove (richieste di Alessandro dell'11/11/2026 comprese):
  1. solo i file cambiati; cartelle nuove prima dei loro file; risorse,
     poi pagine, poi indici, poi cancellazioni; manifesto e stato per
     ultimi; documenti/ mai toccata;
  2. file cambiato due volte in due giri consecutivi: arriva l'ultima;
  3. giro interrotto a metà (processo ucciso): il successivo completa,
     anche per un file che nel frattempo è tornato alla versione di prima;
  4. file rifiutato una volta: si riprova e arriva;
  5. due giri avviati quasi insieme: il secondo aspetta il primo;
  6. server che non rinomina sopra un file esistente: si cancella e si
     rinomina, contenuto giusto;
  7. accesso rifiutato: uscita 3 (ripiego ammesso), nulla toccato;
  8. senza file di stato ma con il manifesto servito: si usa il manifesto;
     senza nessuno dei due: uscita 4, nulla toccato;
  9. un file che non si riesce a caricare: uscita 1, manifesto e stato
     del server NON aggiornati, elenco in sospeso lasciato;
 10. il server accetta meno collegamenti di quelli chiesti: si prosegue
     con quelli accettati.

Uso: python3 scripts/prova-carica-aruba.py   (serve: pip install pyftpdlib pyopenssl)
Exit 0 se tutte le prove passano.
"""

from __future__ import annotations

import hashlib
import importlib.util
import logging
import json
import os
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

QUI = Path(__file__).resolve().parent
SCRIPT = QUI / "carica-aruba.py"
STATO = ".ftp-deploy-sync-state-2026-06-09.json"

try:
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.handlers import TLS_FTPHandler
    from pyftpdlib.servers import ThreadedFTPServer
except ImportError:
    print("Serve pyftpdlib e pyopenssl: pip install pyftpdlib pyopenssl")
    sys.exit(2)

spec = importlib.util.spec_from_file_location("carica_aruba", SCRIPT)
ca = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ca)  # type: ignore[union-attr]

logging.getLogger("pyftpdlib").setLevel(logging.ERROR)
EVENTI: list[tuple[float, str, str]] = []
GUASTI: dict = {}
LOCK = threading.Lock()


def rel_di(handler, path: str) -> str:
    radice = os.path.join(os.path.realpath(handler.fs.root), "www.sito")
    return os.path.relpath(os.path.realpath(path), radice).replace(os.sep, "/")


class Gestore(TLS_FTPHandler):
    def _ev(self, cmd: str, rel: str) -> None:
        with LOCK:
            EVENTI.append((time.time(), cmd, rel))

    def ftp_STOR(self, file, mode="w"):
        rel = rel_di(self, file)
        with LOCK:
            rifiuta = GUASTI.get("rifiuta_una_volta")
            if rifiuta and rel.endswith(rifiuta + ca.SUFFISSO_TMP) and not GUASTI.get("rifiutato"):
                GUASTI["rifiutato"] = True
                self.respond("451 Prova: rifiutato una volta.")
                return
            sempre = GUASTI.get("rifiuta_sempre")
            if sempre and rel == ca.tmp_di(sempre):
                self.respond("451 Prova: rifiutato.")
                return
        if GUASTI.get("lento"):
            time.sleep(GUASTI["lento"])
        self._ev("STOR", rel)
        return super().ftp_STOR(file, mode)

    def ftp_RNTO(self, path):
        rel = rel_di(self, path)
        if GUASTI.get("no_rinomina_sopra") and os.path.exists(path):
            self.respond("553 Prova: il file di destinazione esiste.")
            return
        self._ev("RNTO", rel)
        return super().ftp_RNTO(path)

    def ftp_DELE(self, path):
        self._ev("DELE", rel_di(self, path))
        return super().ftp_DELE(path)

    def ftp_MKD(self, path):
        esisteva = os.path.exists(path)
        r = super().ftp_MKD(path)
        if not esisteva and os.path.isdir(path):
            self._ev("MKD", rel_di(self, path))
        return r

    def ftp_RMD(self, path):
        r = super().ftp_RMD(path)
        if not os.path.exists(path):
            self._ev("RMD", rel_di(self, path))
        return r


def porta_libera() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


class Banco:
    def __init__(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="prova-carica-"))
        self.root = self.tmp / "ftp"
        self.sito = self.root / "www.sito"
        self.sito.mkdir(parents=True)
        cert = self.tmp / "cert.pem"
        subprocess.run(["openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-days", "1",
                        "-subj", "/CN=localhost", "-keyout", str(cert), "-out", str(cert)],
                       check=True, capture_output=True)
        aut = DummyAuthorizer()
        aut.add_user("prova", "segreta", str(self.root), perm="elradfmwMT")
        Gestore.authorizer = aut
        Gestore.certfile = str(cert)
        Gestore.tls_control_required = True
        Gestore.tls_data_required = True
        self.porta = porta_libera()
        self.server = ThreadedFTPServer(("127.0.0.1", self.porta), Gestore)
        self.server.max_cons = 64
        threading.Thread(target=self.server.serve_forever, kwargs={"timeout": 0.5}, daemon=True).start()

    def env(self, password: str = "segreta") -> dict:
        e = dict(os.environ)
        e.update({"FTP_SERVER": f"127.0.0.1:{self.porta}", "FTP_USERNAME": "prova",
                  "FTP_PASSWORD": password, "FTP_SERVER_DIR": "/www.sito/", "FTP_TLS_INSECURE": "1"})
        e.pop("GITHUB_OUTPUT", None)
        return e

    def chiudi(self) -> None:
        self.server.close_all()
        shutil.rmtree(self.tmp, ignore_errors=True)


def scrivi_build(public: Path, file: dict[str, bytes]) -> None:
    if public.exists():
        shutil.rmtree(public)
    for rel, dati in file.items():
        p = public / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(dati)
    man = {"sha": "prova", "file": {r: hashlib.sha256(d).hexdigest() for r, d in file.items()
                                    if not r.startswith("documenti/") and not r.startswith("pagefind/")}}
    (public / "build-manifest.json").write_text(json.dumps(man, sort_keys=True), encoding="utf-8")


def semina_server(b: Banco, public: Path, con_stato: bool = True) -> None:
    """Il server com'era dopo l'ultimo giro riuscito: i file della build e
    il suo stato."""
    for p in public.rglob("*"):
        if p.is_file():
            dest = b.sito / p.relative_to(public)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dest)
    if con_stato:
        loc, dirs = ca.elenco_locale(public)
        (b.sito / STATO).write_bytes(ca.stato_json(loc, dirs))


def lancia(b: Banco, public: Path, *extra: str, password: str = "segreta",
           manifesto: Path | None = None, attendi: bool = True):
    cmd = [sys.executable, str(SCRIPT), "--public", str(public), "--stato-nome", STATO,
           "--connessioni", "4", "--pausa-lucchetto", "1", *extra]
    if manifesto:
        cmd += ["--manifesto-servito", str(manifesto)]
    p = subprocess.Popen(cmd, env=b.env(password), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if not attendi:
        return p
    out, _ = p.communicate(timeout=180)
    return p.returncode, out


def contenuto(b: Banco, rel: str) -> bytes | None:
    p = b.sito / rel
    return p.read_bytes() if p.is_file() else None


ERRORI: list[str] = []


def verifica(cond: bool, msg: str, out: str = "") -> None:
    if cond:
        print(f"  ✅ {msg}")
    else:
        print(f"  ❌ {msg}")
        if out:
            print("     --- uscita dello script ---")
            print("\n".join("     " + r for r in out.splitlines()[-40:]))
        ERRORI.append(msg)


def reset() -> None:
    with LOCK:
        EVENTI.clear()
        GUASTI.clear()


def base_v1() -> dict[str, bytes]:
    return {
        "index.html": b"<html>home v1</html>",
        "comunicazioni/index.html": b"elenco v1",
        "comunicazioni/vecchio/index.html": b"articolo vecchio",
        "chi-siamo/index.html": b"chi siamo",
        "css/sito.css": b"body{}",
        "images/vecchia.webp": b"IMG1",
        "pagefind/fragment/it_aaa.pf_fragment": b"frammento a",
        "pagefind/pagefind-entry.json": b'{"v":1}',
        "sitemap.xml": b"<urlset>v1</urlset>",
        "build-info.js": b'SITE_BUILD_SHA="v1"',
    }


def prova_1(b: Banco) -> None:
    print("\n1. Solo i file cambiati, nell'ordine giusto; documenti/ intatta")
    reset()
    public = b.tmp / "p1"
    v1 = base_v1()
    scrivi_build(public, v1)
    semina_server(b, public)
    (b.sito / "documenti").mkdir(exist_ok=True)
    (b.sito / "documenti" / "storico.pdf").write_bytes(b"PDF a mano")
    v2 = dict(v1)
    v2["comunicazioni/nuovo/index.html"] = b'<img src="/images/nuova.webp"> articolo nuovo'
    v2["images/nuova.webp"] = b"IMG2"
    v2["index.html"] = b"<html>home v2</html>"
    v2["comunicazioni/index.html"] = b"elenco v2"
    v2["pagefind/fragment/it_bbb.pf_fragment"] = b"frammento b"
    del v2["pagefind/fragment/it_aaa.pf_fragment"]
    v2["pagefind/pagefind-entry.json"] = b'{"v":2}'
    del v2["comunicazioni/vecchio/index.html"]
    v2["build-info.js"] = b'SITE_BUILD_SHA="v2"'
    v2["documenti/locale.pdf"] = b"non deve salire"
    scrivi_build(public, v2)
    rc, out = lancia(b, public)
    verifica(rc == 0, "uscita 0", out)
    finali = [e for e in EVENTI if e[1] == "RNTO"]
    nomi = [e[2] for e in finali]
    attesi = {"comunicazioni/nuovo/index.html", "images/nuova.webp", "index.html", "comunicazioni/index.html",
              "pagefind/fragment/it_bbb.pf_fragment", "pagefind/pagefind-entry.json", "build-info.js",
              "build-manifest.json", STATO}
    sostituiti = {n for n in nomi if not n.startswith(".carica-aruba-prova")}
    verifica(sostituiti == attesi, f"caricati solo i file cambiati ({len(sostituiti)}: {sorted(sostituiti)})", out)
    verifica("chi-siamo/index.html" not in nomi and "css/sito.css" not in nomi, "i file invariati non si toccano")
    t = {e[2]: e[0] for e in EVENTI if e[1] == "RNTO"}
    mkd = {e[2]: e[0] for e in EVENTI if e[1] == "MKD"}
    stor_nuovo = min(e[0] for e in EVENTI if e[1] == "STOR" and e[2].startswith("comunicazioni/nuovo/"))
    verifica("comunicazioni/nuovo" in mkd and mkd["comunicazioni/nuovo"] < stor_nuovo, "la cartella nuova esiste prima dei suoi file")
    risorse = [t["images/nuova.webp"], t["pagefind/fragment/it_bbb.pf_fragment"]]
    pagine = [t["comunicazioni/nuovo/index.html"]]
    indici = [t["index.html"], t["comunicazioni/index.html"], t["pagefind/pagefind-entry.json"], t["build-info.js"]]
    verifica(max(risorse) < min(pagine), "risorse (immagini, ricerca) prima delle pagine")
    verifica(max(pagine) < min(indici), "pagine prima degli indici")
    dele = [e for e in EVENTI if e[1] == "DELE" and not e[2].startswith(".") and not e[2].endswith(ca.SUFFISSO_TMP)
            and "/." not in e[2] and e[2] not in ("index.html",)]
    dele_veri = [e for e in dele if e[2] in ("pagefind/fragment/it_aaa.pf_fragment", "comunicazioni/vecchio/index.html")]
    verifica(len(dele_veri) == 2 and min(e[0] for e in dele_veri) > max(indici), "cancellazioni dopo tutti i caricamenti")
    verifica(t["build-manifest.json"] > max(e[0] for e in dele_veri) and t[STATO] > t["build-manifest.json"],
             "manifesto e stato per ultimi")
    verifica(contenuto(b, "comunicazioni/vecchio/index.html") is None and not (b.sito / "comunicazioni/vecchio").exists(),
             "file e cartella tolti dalla build spariscono dal server")
    verifica(contenuto(b, "documenti/storico.pdf") == b"PDF a mano" and contenuto(b, "documenti/locale.pdf") is None,
             "documenti/ non si tocca né si carica")
    verifica(not any(p.name.endswith(ca.SUFFISSO_TMP) for p in b.sito.rglob("*")), "nessun nome provvisorio rimasto")
    verifica(not (b.sito / ca.SOSPESI).exists() and not (b.sito / ca.LUCCHETTO).exists(),
             "elenco in sospeso e lucchetto tolti a fine giro")
    stato = json.loads((b.sito / STATO).read_text(encoding="utf-8"))
    nomi_stato = {e["name"]: e.get("hash") for e in stato["data"] if e["type"] == "file"}
    verifica(nomi_stato.get("index.html") == hashlib.sha256(b"<html>home v2</html>").hexdigest()
             and "documenti/locale.pdf" not in nomi_stato, "file di stato nel formato dell'azione, aggiornato e senza documenti/")
    verifica(all(contenuto(b, r) == d for r, d in v2.items() if not r.startswith("documenti/")), "sul server c'è esattamente la build")
    rc, out = lancia(b, public)
    n = len([e for e in EVENTI if e[1] == "RNTO"])
    verifica(rc == 0 and "0 risorse, 0 pagine, 0 indici" in out, "un secondo giro senza cambiamenti non carica nulla", out)
    _ = n


def prova_2(b: Banco) -> None:
    print("\n2. File cambiato due volte in due giri consecutivi")
    reset()
    public = b.tmp / "p2"
    v = base_v1()
    scrivi_build(public, v)
    semina_server(b, public)
    v["chi-siamo/index.html"] = b"chi siamo v2"
    scrivi_build(public, v)
    rc1, out1 = lancia(b, public)
    v["chi-siamo/index.html"] = b"chi siamo v3"
    scrivi_build(public, v)
    rc2, out2 = lancia(b, public)
    verifica(rc1 == 0 and rc2 == 0, "due giri riusciti", out1 + out2)
    verifica(contenuto(b, "chi-siamo/index.html") == b"chi siamo v3", "sul server c'è l'ultima versione")


def prova_3(b: Banco) -> None:
    print("\n3. Giro interrotto a metà, poi giro successivo")
    reset()
    public = b.tmp / "p3"
    v1 = base_v1()
    for i in range(30):
        v1[f"pagine/p{i:02d}/index.html"] = f"pagina {i} v1".encode()
    scrivi_build(public, v1)
    semina_server(b, public)
    v2 = dict(v1)
    for i in range(30):
        v2[f"pagine/p{i:02d}/index.html"] = f"pagina {i} v2".encode()
    scrivi_build(public, v2)
    GUASTI["lento"] = 0.15
    p = lancia(b, public, attendi=False)
    t0 = time.time()
    while time.time() - t0 < 60:
        if len([e for e in EVENTI if e[1] == "RNTO" and e[2].startswith("pagine/")]) >= 6:
            break
        time.sleep(0.05)
    p.send_signal(signal.SIGKILL)  # morte senza pulizia: il lucchetto resta
    p.wait()
    GUASTI.clear()
    caricati = sorted({e[2] for e in EVENTI if e[1] == "RNTO" and e[2].startswith("pagine/")})
    verifica(len(caricati) >= 6 and (b.sito / ca.SOSPESI).exists(), f"giro ucciso dopo {len(caricati)} pagine; elenco in sospeso sul server")
    stato_prima = (b.sito / STATO).read_bytes()
    verifica(json.loads(stato_prima)["data"] and hashlib.sha256(v1["chi-siamo/index.html"]).hexdigest() in stato_prima.decode(),
             "il file di stato non è stato aggiornato dal giro interrotto")
    # Nel frattempo la build torna indietro per una delle pagine già caricate:
    # senza l'elenco in sospeso, stato (v1) e build (v1) coinciderebbero e
    # sul server resterebbe la v2.
    tornata = caricati[0]
    v3 = dict(v2)
    v3[tornata] = v1[tornata]
    scrivi_build(public, v3)
    rc, out = lancia(b, public, "--lucchetto-morto", "2")
    verifica(rc == 0, "il giro successivo riesce (lucchetto del giro morto tolto)", out)
    verifica("Lucchetto del giro" in out, "il lucchetto del giro morto viene riconosciuto")
    verifica(contenuto(b, tornata) == v1[tornata], f"{tornata}: tornato alla versione della build, non la v2 del giro interrotto")
    verifica(all(contenuto(b, r) == d for r, d in v3.items()), "sul server c'è esattamente la build")
    verifica(not (b.sito / ca.SOSPESI).exists(), "elenco in sospeso tolto")


def prova_4(b: Banco) -> None:
    print("\n4. File rifiutato una volta")
    reset()
    public = b.tmp / "p4"
    v = base_v1()
    scrivi_build(public, v)
    semina_server(b, public)
    v["chi-siamo/index.html"] = b"chi siamo nuovo"
    scrivi_build(public, v)
    GUASTI["rifiuta_una_volta"] = "index.html"  # il provvisorio di chi-siamo/index.html o di index.html
    rc, out = lancia(b, public)
    verifica(rc == 0 and GUASTI.get("rifiutato"), "rifiutato una volta, giro riuscito", out)
    verifica("riuscito al tentativo 2" in out, "il file si riprova e arriva", out)
    verifica(contenuto(b, "chi-siamo/index.html") == b"chi siamo nuovo", "contenuto giusto sul server")


def prova_5(b: Banco) -> None:
    print("\n5. Due giri avviati quasi insieme")
    reset()
    public_a = b.tmp / "p5a"
    public_b = b.tmp / "p5b"
    v = base_v1()
    scrivi_build(public_a, v)
    semina_server(b, public_a)
    va = dict(v)
    vb = dict(v)
    for i in range(12):
        va[f"x/a{i}.html"] = b"A"
    va["chi-siamo/index.html"] = b"giro A"
    vb["chi-siamo/index.html"] = b"giro B"
    scrivi_build(public_a, va)
    scrivi_build(public_b, vb)
    GUASTI["lento"] = 0.1
    pa = lancia(b, public_a, attendi=False)
    time.sleep(0.3)
    pb = lancia(b, public_b, attendi=False)
    out_a, _ = pa.communicate(timeout=180)
    out_b, _ = pb.communicate(timeout=180)
    lucc = [e for e in EVENTI if e[2] == ca.LUCCHETTO and e[1] in ("MKD", "RMD")]
    seq = [e[1] for e in sorted(lucc)]
    verifica(pa.returncode == 0 and pb.returncode == 0, "entrambi i giri riusciti", out_a + out_b)
    verifica("attendo che finisca" in out_b, "il secondo giro aspetta il primo", out_b)
    verifica(seq == ["MKD", "RMD", "MKD", "RMD"], f"i lucchetti non si sovrappongono ({seq})")
    verifica(contenuto(b, "chi-siamo/index.html") == b"giro B" and contenuto(b, "x/a0.html") is None,
             "alla fine il server è la build del secondo giro (arrivato dopo)")


def prova_6(b: Banco) -> None:
    print("\n6. Server che non rinomina sopra un file esistente")
    reset()
    public = b.tmp / "p6"
    v = base_v1()
    scrivi_build(public, v)
    semina_server(b, public)
    v["chi-siamo/index.html"] = b"chi siamo 6"
    scrivi_build(public, v)
    GUASTI["no_rinomina_sopra"] = True
    rc, out = lancia(b, public)
    verifica(rc == 0 and "rinomina sopra un file esistente: no" in out, "il caso si riconosce e il giro riesce", out)
    verifica(contenuto(b, "chi-siamo/index.html") == b"chi siamo 6", "contenuto giusto sul server")


def prova_7(b: Banco) -> None:
    print("\n7. Accesso rifiutato")
    reset()
    public = b.tmp / "p7"
    scrivi_build(public, base_v1())
    rc, out = lancia(b, public, password="sbagliata")
    verifica(rc == 3, "uscita 3: ripiego ammesso", out)
    verifica(not EVENTI, "nulla toccato sul server")


def prova_8(b: Banco) -> None:
    print("\n8. Senza file di stato")
    reset()
    for p in list(b.sito.iterdir()):
        shutil.rmtree(p) if p.is_dir() else p.unlink()
    public = b.tmp / "p8"
    v = base_v1()
    scrivi_build(public, v)
    semina_server(b, public, con_stato=False)
    rc, out = lancia(b, public)
    verifica(rc == 4 and not [e for e in EVENTI if e[1] in ("STOR", "DELE") and ca.LUCCHETTO not in e[2]],
             "né stato né manifesto: uscita 4, nessun file toccato", out)
    reset()
    man = b.tmp / "manifesto-servito.json"
    shutil.copy(public / "build-manifest.json", man)
    v["chi-siamo/index.html"] = b"chi siamo 8"
    scrivi_build(public, v)
    rc, out = lancia(b, public, manifesto=man)
    nomi = {e[2] for e in EVENTI if e[1] == "RNTO"}
    verifica(rc == 0 and "manifesto servito" in out, "con il manifesto servito si carica", out)
    verifica("chi-siamo/index.html" in nomi and "pagefind/fragment/it_aaa.pf_fragment" in nomi and "css/sito.css" not in nomi,
             "cambiati + file che il manifesto non elenca (ricerca); gli altri no")
    verifica((b.sito / STATO).exists(), "il file di stato ora c'è")


def prova_9(b: Banco) -> None:
    print("\n9. Un file che non si riesce a caricare")
    reset()
    public = b.tmp / "p9"
    v = base_v1()
    scrivi_build(public, v)
    semina_server(b, public)
    stato_prima = (b.sito / STATO).read_bytes()
    man_prima = (b.sito / "build-manifest.json").read_bytes()
    v["chi-siamo/index.html"] = b"chi siamo 9"
    v["images/vecchia.webp"] = b"IMG9"
    scrivi_build(public, v)
    GUASTI["rifiuta_sempre"] = "chi-siamo/index.html"
    rc, out = lancia(b, public)
    verifica(rc == 1, "uscita 1: deploy rosso, niente ripiego", out)
    verifica((b.sito / STATO).read_bytes() == stato_prima and (b.sito / "build-manifest.json").read_bytes() == man_prima,
             "manifesto e file di stato del server non aggiornati")
    verifica((b.sito / ca.SOSPESI).exists() and not (b.sito / ca.LUCCHETTO).exists(),
             "elenco in sospeso lasciato, lucchetto tolto")
    GUASTI.clear()
    rc, out = lancia(b, public)
    verifica(rc == 0 and contenuto(b, "chi-siamo/index.html") == b"chi siamo 9", "il giro successivo completa", out)


def prova_10(b: Banco) -> None:
    print("\n10. Il server accetta meno collegamenti di quelli chiesti")
    reset()
    public = b.tmp / "p10"
    v = base_v1()
    scrivi_build(public, v)
    semina_server(b, public)
    for i in range(20):
        v[f"z/p{i}.html"] = f"pagina {i}".encode()
    scrivi_build(public, v)
    b.server.max_cons_per_ip = 3  # il collegamento principale più due
    try:
        rc, out = lancia(b, public)
    finally:
        b.server.max_cons_per_ip = 0
    verifica(rc == 0 and "rifiutati dal server" in out, "si prosegue con i collegamenti accettati", out)
    verifica(all(contenuto(b, r) == d for r, d in v.items()), "sul server c'è esattamente la build")


def main() -> int:
    b = Banco()
    try:
        for prova in (prova_1, prova_2, prova_3, prova_4, prova_5, prova_6, prova_7, prova_8, prova_9, prova_10):
            prova(b)
            # ogni prova riparte da un server vuoto
            for p in list(b.sito.iterdir()):
                shutil.rmtree(p) if p.is_dir() else p.unlink()
    finally:
        b.chiudi()
    print()
    if ERRORI:
        print(f"❌ {len(ERRORI)} controlli non superati.")
        return 1
    print("✅ Tutte le prove del caricamento superate.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
