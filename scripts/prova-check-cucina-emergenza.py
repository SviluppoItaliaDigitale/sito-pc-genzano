#!/usr/bin/env python3
"""Prove di check-cucina-emergenza.py, il controllo della sezione /cucina-emergenza/.

Il controllo è bloccante sulle PR e ogni mese rilegge i collegamenti: se smette di vedere un errore, nessuno
se ne accorge. Due gruppi di prove, nessuna richiesta fuori dalla macchina:
  1. senza rete: quindici casi sbagliati (sito non istituzionale, file Word, PDF fuori dai dati, collegamento
     mancante, verifica troppo vecchia…) che deve respingere con il messaggio giusto, e la copia intatta che
     deve passare;
  2. risposte dei siti, con un server finto in locale: un PDF vero è letto, un 404 è un collegamento rotto,
     una pagina di verifica anti-bot o un rifiuto (403) non sono né rotti né controllati, una pagina qualsiasi
     al posto del PDF è una fonte non letta;
  3. browser di riserva: se Playwright manca o Chromium non parte, il controllo non si interrompe, classifica
     ciò che ha già letto e scrive il rapporto, che dice perché il ripiego è mancato.

Uso:  python3 scripts/prova-check-cucina-emergenza.py public
Lavora su copie in una cartella temporanea: i file del repository non si toccano. Uscita 0 se ogni prova
va come atteso, 1 altrimenti.
"""
import http.server
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import types
from datetime import date, timedelta
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
SCRIPT = "check-cucina-emergenza.py"
esiti = []


def lancia(cartella, *altro):
    return subprocess.run([sys.executable, str(cartella / "scripts" / SCRIPT), "--public", str(cartella / "public"), *altro],
                          capture_output=True, text=True)


def prova(base, nome, cambia, atteso, *altro):
    """Copia la base, applica il cambiamento sbagliato e pretende uscita 1 con il messaggio atteso."""
    caso = base.parent / "caso"
    if caso.exists():
        shutil.rmtree(caso)
    shutil.copytree(base, caso)
    cambia(caso)
    r = lancia(caso, *altro)
    riuscita = r.returncode == 1 and atteso in r.stdout
    esiti.append(riuscita)
    print(("ok  " if riuscita else "NO  ") + nome)
    if not riuscita:
        print(f"    uscita {r.returncode}, atteso il messaggio «{atteso}»")
        print("    " + "\n    ".join((r.stdout + r.stderr).strip().splitlines()[-12:]))


def nei_documenti(vecchio, nuovo):
    def cambia(caso):
        p = caso / "data" / "cucina_emergenza.yaml"
        testo = p.read_text(encoding="utf-8")
        if vecchio not in testo:
            sys.exit(f"prova non eseguibile: «{vecchio}» non è più in cucina_emergenza.yaml")
        p.write_text(testo.replace(vecchio, nuovo, 1), encoding="utf-8")
    return cambia


def nel_catalogo(funzione):
    def cambia(caso):
        p = caso / "data" / "disciplinari.json"
        dati = json.loads(p.read_text(encoding="utf-8"))
        funzione(dati)
        p.write_text(json.dumps(dati, ensure_ascii=False, indent=2), encoding="utf-8")
    return cambia


def nella_pagina(quale, funzione):
    def cambia(caso):
        p = caso / "public" / "cucina-emergenza" / quale
        prima = p.read_text(encoding="utf-8")
        dopo = funzione(prima)
        if dopo == prima:
            sys.exit(f"prova non eseguibile: la pagina {quale} non è cambiata")
        p.write_text(dopo, encoding="utf-8")
    return cambia


def in_fondo(collegamento):
    """Aggiunge un collegamento alla fine del contenuto della pagina."""
    return lambda testo: testo.replace("</main>", collegamento + "</main>", 1)


VERIFICA = (b"<!doctype html><head><meta charset='utf-8'><title>Servizio di sicurezza</title><style>*{margin:0}</style></head>"
            b"<body><h1>Browser Validation Page</h1><p>www.esempio.it is using security service for protection against "
            b"online attacks. This process is automatic. You will be redirected once the validation is complete</p></body>")
QUALSIASI = (b"<!doctype html><html><head><title>Pagina del sito</title>"
             b"<script src='https://www.google.com/recaptcha/api.js'></script></head>"
             b"<body><h1>Documento spostato</h1><p>Cerca nel sito.</p></body></html>")
RISPOSTE = {"/vero.pdf": (200, "application/pdf", b"%PDF-1.7\n" + b"x" * 4000),
            "/verifica.pdf": (200, "text/html; charset=UTF-8", VERIFICA),
            "/rifiuto.pdf": (403, "text/plain", b"Forbidden"),
            "/manca.pdf": (404, "text/plain", b"Not found"),
            "/qualsiasi.pdf": (200, "text/html; charset=UTF-8", QUALSIASI)}


class SitoFinto(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        stato, tipo, corpo = RISPOSTE.get(self.path.split("?")[0], (500, "text/plain", b"errore"))
        self.send_response(stato)
        self.send_header("Content-Type", tipo)
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)


def esito(nome, riuscita, dettaglio=""):
    esiti.append(riuscita)
    print(("ok  " if riuscita else "NO  ") + nome + (f" ({dettaglio})" if dettaglio and not riuscita else ""))


class BrowserCheNonParte:
    """Finto Playwright: c'è la libreria, ma Chromium (o una sua libreria di sistema) non si avvia."""

    def __init__(self, dove):
        self.dove = dove
        self.fermato = False
        self.chromium = types.SimpleNamespace(launch=self.lancia)

    def __enter__(self):  # anche come «with sync_playwright() as pw», la forma che il controllo usava prima
        return self.start()

    def __exit__(self, *args):
        self.stop()

    def lancia(self):
        raise RuntimeError("Executable doesn't exist at /percorso/chromium\nPlease run: playwright install")

    def start(self):
        if self.dove == "avvio":
            raise OSError("driver non trovato")
        return self

    def stop(self):
        self.fermato = True


def prove_del_browser(controllo, base):
    """Il ripiego con il browser è facoltativo: se non parte, il giro deve arrivare in fondo e scrivere il rapporto."""
    vero = sys.modules.get("playwright.sync_api", "assente")
    documenti, catalogo = controllo.carica()
    casi = (("Chromium non parte", "lancio", "Chromium non parte"),
            ("Playwright non parte", "avvio", "Playwright non parte"),
            ("Playwright non è installato", None, "Playwright non è installato"))
    try:
        for nome, dove, motivo in casi:
            finto = BrowserCheNonParte(dove)
            sys.modules["playwright.sync_api"] = (types.SimpleNamespace(sync_playwright=lambda finto=finto: finto)
                                                  if dove else None)  # None: l'importazione fallisce
            for elenco in (controllo.errori, controllo.non_letti, controllo.protetti, controllo.da_rivedere,
                           controllo.senza_browser):
                elenco.clear()
            controllo.metodi.clear()
            controllo.di_fila.clear()
            controllo.motivo.clear()
            for percorso in ("/vero.pdf", "/manca.pdf", "/qualsiasi.pdf", "/verifica.pdf"):
                controllo.controlla_pdf(f"documento «{percorso}»", base + percorso)
            try:
                controllo.chiudi_da_rivedere(True)
                testo = controllo.rapporto(documenti, catalogo, True, False)
                interrotto = ""
            except Exception as e:  # è proprio ciò che la prova deve escludere
                testo, interrotto = "", f"{type(e).__name__}: {e}"
            esito(f"browser di riserva, {nome}: il controllo arriva in fondo e classifica ciò che ha letto",
                  not interrotto and len(controllo.errori) == 1 and len(controllo.non_letti) == 1
                  and len(controllo.protetti) == 1 and controllo.metodi["richiesta diretta"] == 1,
                  interrotto or f"rotti {len(controllo.errori)}, non letti {len(controllo.non_letti)}, "
                                f"protetti {len(controllo.protetti)}")
            esito(f"browser di riserva, {nome}: il rapporto c'è e dice perché il ripiego è mancato",
                  "Ripiego con il browser non disponibile" in testo and motivo in testo
                  and "### Collegamenti rotti o dati sbagliati" in testo
                  and "### Fonti che non si sono fatte leggere" in testo and "Please run" not in testo,
                  testo[:300])
            if dove == "lancio":
                esito("browser di riserva: dopo un avvio fallito Playwright viene comunque fermato", finto.fermato)
    finally:
        if vero == "assente":
            sys.modules.pop("playwright.sync_api", None)
        else:
            sys.modules["playwright.sync_api"] = vero
        controllo.senza_browser.clear()


def prove_delle_risposte():
    """Come lo script classifica le risposte di un sito: si usa un server finto su questa macchina."""
    spec = importlib.util.spec_from_file_location("controllo", RADICE / "scripts" / SCRIPT)
    controllo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(controllo)
    controllo.PAUSA = 0
    # le attese fra un tentativo e l'altro non servono alla prova: al modulo si dà un orologio suo, senza
    # toccare time.sleep del resto del processo
    controllo.time = types.SimpleNamespace(time=time.time, sleep=lambda secondi: None)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), SitoFinto)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_address[1]}"
    try:
        attesi = {"/vero.pdf": "pdf", "/verifica.pdf": "protetto", "/rifiuto.pdf": "protetto", "/manca.pdf": "assente",
                  "/qualsiasi.pdf": "altro", "/guasto.pdf": "muto"}
        for percorso, atteso in attesi.items():
            ottenuto, nota = controllo.leggi_pdf(base + percorso)
            esito(f"risposta {percorso}: «{atteso}»", ottenuto == atteso, f"ottenuto «{ottenuto}»: {nota}")
        esito("una pagina normale con uno script di terzi non è una verifica anti-bot",
              not controllo.sembra_verifica(QUALSIASI) and controllo.sembra_verifica(VERIFICA))

        for percorso in ("/vero.pdf", "/verifica.pdf", "/rifiuto.pdf", "/manca.pdf", "/qualsiasi.pdf"):
            controllo.controlla_pdf(f"documento «{percorso}»", base + percorso)
        controllo.chiudi_da_rivedere(False)
        esito("un 404 è un collegamento rotto", len(controllo.errori) == 1 and "/manca.pdf" in controllo.errori[0], controllo.errori)
        esito("verifica anti-bot e rifiuto: né rotti né controllati",
              len(controllo.protetti) == 2 and not any("verifica.pdf" in t or "rifiuto.pdf" in t for _, t in controllo.non_letti),
              controllo.protetti)
        esito("una pagina qualsiasi al posto del PDF è una fonte non letta",
              len(controllo.non_letti) == 1 and "/qualsiasi.pdf" in controllo.non_letti[0][1], controllo.non_letti)
        esito("il PDF vero è letto", controllo.metodi["richiesta diretta"] == 1)

        for elenco in (controllo.errori, controllo.non_letti, controllo.protetti, controllo.da_rivedere):
            elenco.clear()
        controllo.di_fila.clear()
        controllo.motivo.clear()
        for n in range(controllo.SOGLIA_FERMO + 2):
            controllo.controlla_pdf(f"documento «verifica {n}»", base + "/verifica.pdf")
        controllo.chiudi_da_rivedere(False)
        esito("un sito tutto dietro la verifica: anche i file saltati restano «non controllati», non rotti",
              len(controllo.protetti) == controllo.SOGLIA_FERMO + 2 and not controllo.non_letti and not controllo.errori,
              f"protetti {len(controllo.protetti)}, non letti {len(controllo.non_letti)}")

        # lo stesso con i PDF del catalogo, che si leggono CONTEMPORANEE alla volta
        for elenco in (controllo.errori, controllo.non_letti, controllo.protetti, controllo.da_rivedere):
            elenco.clear()
        finto = {"voci": [{"nome": f"Prodotto {n}", "formato": "pdf", "url": f"{base}/verifica.pdf?n={n}"} for n in range(12)]}
        controllo.controlla_file_del_catalogo(finto)
        controllo.chiudi_da_rivedere(False)
        esito("catalogo tutto dietro la verifica: dodici «non controllati», nessuna fonte non letta",
              len(controllo.protetti) == 12 and not controllo.non_letti and not controllo.errori,
              f"protetti {len(controllo.protetti)}, non letti {len(controllo.non_letti)}")
        for elenco in (controllo.errori, controllo.non_letti, controllo.protetti, controllo.da_rivedere):
            elenco.clear()
        controllo.metodi.clear()
        misto = {"voci": [{"nome": "Vero", "formato": "pdf", "url": base + "/vero.pdf"},
                          {"nome": "Mancante", "formato": "pdf", "url": base + "/manca.pdf"},
                          {"nome": "Solo Word", "formato": "docx", "url": base + "/qualsiasi.pdf"},
                          {"nome": "Con decreto", "formato": "pdf", "url": base + "/vero.pdf?b",
                           "extra": [{"etichetta": "Modifica temporanea", "url": base + "/vero.pdf?c"}]}]}
        controllo.controlla_file_del_catalogo(misto)
        controllo.chiudi_da_rivedere(False)
        esito("catalogo misto: tre PDF letti, un 404 fra i rotti, il file Word non si chiede",
              controllo.metodi["richiesta diretta"] == 3 and len(controllo.errori) == 1 and not controllo.non_letti,
              f"letti {controllo.metodi['richiesta diretta']}, rotti {controllo.errori}, non letti {controllo.non_letti}")
        prove_del_browser(controllo, base)
    finally:
        server.shutdown()


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    costruite = Path(sys.argv[1]) / "cucina-emergenza"
    if not (costruite / "index.html").exists():
        sys.exit(f"{costruite}: pagine non costruite (serve la build di Hugo)")
    with tempfile.TemporaryDirectory() as temporanea:
        base = Path(temporanea) / "base"
        (base / "scripts").mkdir(parents=True)
        shutil.copy(RADICE / "scripts" / SCRIPT, base / "scripts" / SCRIPT)
        shutil.copytree(RADICE / "data", base / "data",
                        ignore=lambda cartella, nomi: [n for n in nomi if n not in ("cucina_emergenza.yaml", "disciplinari.json")])
        shutil.copytree(costruite, base / "public" / "cucina-emergenza")

        r = lancia(base, "--eta", "36500")
        esiti.append(r.returncode == 0)
        print(("ok  " if r.returncode == 0 else "NO  ") + "la copia intatta passa")
        if r.returncode != 0:
            print("    " + "\n    ".join((r.stdout + r.stderr).strip().splitlines()[-12:]))

        documenti = (base / "data" / "cucina_emergenza.yaml").read_text(encoding="utf-8")
        trovato = re.search(r'url: "?(https://www\.salute\.gov\.it/[^"\s]+\.pdf)', documenti)
        if not trovato:
            sys.exit("prova non eseguibile: nessun documento del Ministero della Salute nei dati")
        uno = trovato.group(1)
        catalogo = json.loads((base / "data" / "disciplinari.json").read_text(encoding="utf-8"))
        in_pdf = next(v for v in catalogo["voci"] if v["formato"] == "pdf")
        in_word = next((v for v in catalogo["voci"] if v["formato"] == "docx"), None)
        word = in_word["url"] if in_word else in_pdf["url"].replace("/E/pdf", "/E/docx")

        def word_al_posto_del_pdf(dati):
            voce = next(v for v in dati["voci"] if v["formato"] == "pdf")
            voce["url"] = voce["url"].replace("/E/pdf", "/E/docx")

        def altra_pagina(dati):
            voce = next(v for v in dati["voci"] if v["formato"] == "pdf")
            voce["url"] = re.sub(r"BLOB%3AID%3D\d+", "BLOB%3AID%3D99999", voce["url"])

        def doppione(dati):
            pdf = [v for v in dati["voci"] if v["formato"] == "pdf"]
            pdf[1]["url"] = pdf[0]["url"]

        def data_sbagliata(dati):
            dati["verificato"] = "24/11/2026"

        def verifica_vecchia(dati):
            dati["verificato"] = (date.today() - timedelta(days=100)).isoformat()

        def verifica_futura(dati):
            dati["verificato"] = (date.today() + timedelta(days=3)).isoformat()

        def senza_un_collegamento(testo):
            for forma in (in_pdf["url"].replace("&", "&amp;"), in_pdf["url"]):
                if forma in testo:
                    return testo.replace(forma, "https://www.masaf.gov.it/altro", 1)
            return testo

        prova(base, "documento su un sito non istituzionale",
              nei_documenti(uno, uno.replace("www.salute.gov.it", "www.esempio-privato.it")), "non è fra gli enti ammessi")
        prova(base, "indirizzo http", nei_documenti(uno, uno.replace("https://", "http://")), "indirizzo non https")
        prova(base, "documento Word al posto del PDF", nei_documenti(uno, uno[:-4] + ".docx"), "non finisce con .pdf")
        prova(base, "parentesi nell'indirizzo", nei_documenti(uno, uno[:-4] + "(1).pdf"), "parentesi nell'indirizzo")
        prova(base, "disciplinare in PDF con un allegato Word", nel_catalogo(word_al_posto_del_pdf),
              "l'allegato del Ministero non è un PDF")
        prova(base, "allegato di un'altra pagina del Ministero", nel_catalogo(altra_pagina),
              "non è della pagina del Ministero della sua classe")
        prova(base, "stesso indirizzo su due disciplinari", nel_catalogo(doppione), "indirizzo già usato da un'altra voce")
        prova(base, "data di verifica in formato sbagliato", nel_catalogo(data_sbagliata),
              "«verificato» deve essere una data AAAA-MM-GG")
        prova(base, "verifica dei collegamenti più vecchia della soglia (--eta 45)", nel_catalogo(verifica_vecchia),
              "l'ultimo controllo completo dei collegamenti è del", "--eta", "45")
        prova(base, "data di verifica nel futuro", nel_catalogo(verifica_futura), "«verificato» è una data futura")
        prova(base, "pagina che collega un file Word",
              nella_pagina("disciplinari/index.html", in_fondo(f'<a href="{word.replace("&", "&amp;")}">Word</a>')),
              "le pagine collegano un file che non è un PDF")
        prova(base, "pagina che collega un PDF di un ente, ma fuori dai dati",
              nella_pagina("index.html", in_fondo('<a href="https://www.salute.gov.it/imgs/altro_documento.pdf">Altro</a>')),
              "le pagine collegano un PDF che non è nei dati")
        prova(base, "pagina che collega un PDF su un sito qualsiasi",
              nella_pagina("index.html", in_fondo('<a href="https://www.sito-qualsiasi.it/manuale.pdf">Altro</a>')),
              "le pagine collegano un PDF che non è nei dati")
        prova(base, "catalogo costruito senza un collegamento dei dati",
              nella_pagina("disciplinari/index.html", senza_un_collegamento), "non compare nel catalogo costruito")
        prova(base, "pagina del catalogo non costruita",
              lambda caso: shutil.rmtree(caso / "public" / "cucina-emergenza" / "disciplinari"), "pagina non costruita")

    prove_delle_risposte()
    print(f"\n{sum(esiti)} prove su {len(esiti)} come atteso")
    return 0 if all(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
