#!/usr/bin/env python3
"""Prove di check-cucina-emergenza.py, il controllo della sezione /cucina-emergenza/.

Il controllo è bloccante sulle PR e ogni mese rilegge i collegamenti: se smette di vedere un errore, nessuno
se ne accorge. Sei gruppi di prove, nessuna richiesta fuori dalla macchina:
  1. senza rete: i casi sbagliati (sito non istituzionale, file Word, PDF fuori dai dati, collegamento
     mancante, verifica troppo vecchia, sintesi europea su un altro sito o senza il suo collegamento…) che
     deve respingere con il messaggio giusto, e la copia intatta che deve passare;
  2. risposte dei siti, con un server finto in locale: un PDF vero è letto, un 404 è un collegamento rotto,
     una pagina di verifica anti-bot o un rifiuto (403) non sono né rotti né controllati, e nemmeno un sito
     che dà tempo scaduto o un errore del server (5xx) o che chiude la connessione senza rispondere, alla
     richiesta semplice e al browser; una pagina qualsiasi al posto del PDF, o un 400, è una fonte non
     letta, anche quando l'altra richiesta è rimasta senza risposta, e lo sono un nome che non si risolve,
     un certificato scaduto e troppi collegamenti rimasti senza controllo (più di SOGLIA_FERMO e più di un
     quinto di quelli da aprire);
  3. browser di riserva: se Playwright manca o Chromium non parte, il controllo non si interrompe, classifica
     ciò che ha già letto e scrive il rapporto, che dice perché il ripiego è mancato;
  4. sintesi europee, con un registro e un archivio finti in locale: una pubblicazione nuova, un fascicolo
     cambiato, un prodotto sparito e una rettifica nuova sono novità; un atto che l'archivio non ha più è un
     collegamento rotto, ma solo dopo la conferma della richiesta singola; registro o archivio muti sono
     fonti non lette, e anche un archivio che non restituisce più le rettifiche già note. In più, le
     funzioni di scripts/aggiorna-documenti-unici.py che decidono quale documento è di quale prodotto
     (denominazione intera fra virgolette o numero di fascicolo: «Bra» non è «fibra») e il suo lavoro su un
     catalogo finto: ciò che non si legge o non si sa interpretare non cambia i dati;
  5. letture annotate (--aggiorna-data): di ogni collegamento resta il giorno dell'ultima lettura riuscita,
     da qualunque rete, e la data di verifica dei dati è il più vecchio di quei giorni. Non avanza se un
     collegamento non è mai stato letto, non torna indietro, e con un collegamento rotto o una fonte non
     letta non si annota nulla.

  6. disciplinari nuovi, tolti e aggiornati: un prodotto italiano registrato che il catalogo non ha, un
     allegato nuovo nelle pagine del Ministero, un prodotto tolto dal registro, un file sparito, un file che
     allo stesso indirizzo pesa diversamente dai dati; il rapporto lo dice in ogni giro fatto con la rete.

Uso:  python3 scripts/prova-check-cucina-emergenza.py public
Lavora su copie in una cartella temporanea: i file del repository non si toccano. Uscita 0 se ogni prova
va come atteso, 1 altrimenti.
"""
import contextlib
import http.server
import importlib.util
import io
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
import types
import urllib.parse
from datetime import date, timedelta
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
SCRIPT = "check-cucina-emergenza.py"
SCRIPT_SINTESI = "aggiorna-documenti-unici.py"
esiti = []
# Che cosa rispondono il registro europeo e l'archivio dell'UE finti: lo cambia ogni prova.
FINTO = {"registro": [], "stato_registro": 200, "stato_archivio": 200, "fuori_dal_gruppo": set(), "inesistenti": set(),
         "rettifiche": {}}


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
            "/negato.pdf": (400, "text/plain", b"Bad request"),
            "/attesa.pdf": (202, "text/html; charset=UTF-8", b""),  # EUR-Lex alle richieste di un programma
            "/qualsiasi.pdf": (200, "text/html; charset=UTF-8", QUALSIASI)}


class SitoFinto(http.server.BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        percorso, _, domanda = self.path.partition("?")
        if percorso == "/chiude.pdf":  # il sito chiude la connessione senza rispondere
            self.close_connection = True
            with contextlib.suppress(OSError):
                self.connection.shutdown(socket.SHUT_RDWR)
            return
        if percorso == "/parziale.pdf" and self.headers.get("Range") == "bytes=0-7":
            # come il sito del Ministero: alla richiesta parziale risponde 206 e dichiara il peso del file intero
            corpo = RISPOSTE["/vero.pdf"][2]
            self.send_response(206)
            self.send_header("Content-Type", "application/pdf")
            self.send_header("Content-Range", f"bytes 0-7/{len(corpo)}")
            self.send_header("Content-Length", "8")
            self.send_header("Last-Modified", "Wed, 12 Dec 2012 07:52:23 GMT")
            self.end_headers()
            self.wfile.write(corpo[:8])
            return
        if percorso == "/pagina-poi-pdf.pdf":  # alla richiesta parziale una pagina, a quella intera il PDF
            percorso = "/qualsiasi.pdf" if self.headers.get("Range") else "/vero.pdf"
        if percorso == "/registro":  # elenco del registro europeo eAmbrosia
            stato, tipo, corpo = FINTO["stato_registro"], "application/json", json.dumps(FINTO["registro"]).encode("utf-8")
        elif percorso == "/archivio":  # domande SPARQL all'archivio dell'UE, a gruppi di numeri CELEX
            testo = urllib.parse.parse_qs(domanda).get("query", [""])[0]
            numeri = re.findall(r'"([0-9A-Z()]+)"\^\^', testo)
            if "corrects_resource_legal" in testo:
                righe = [{"atto": {"value": n}, "rettifica": {"value": r}, "data": {"value": quando}}
                         for n in numeri for r, quando in FINTO["rettifiche"].get(n, [])]
            else:
                righe = [{"celex": {"value": n}} for n in numeri if n not in FINTO["fuori_dal_gruppo"]]
            stato, tipo = FINTO["stato_archivio"], "application/sparql-results+json"
            corpo = json.dumps({"results": {"bindings": righe}}).encode("utf-8")
        elif percorso.startswith("/celex/"):  # un atto solo: 303 se esiste, 404 se no
            esiste = urllib.parse.unquote(percorso[len("/celex/"):]) not in FINTO["inesistenti"]
            self.send_response(303 if esiste else 404)
            if esiste:
                self.send_header("Location", "/vero.pdf")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        else:
            if percorso == "/lento.pdf":  # risponde quando chi chiede ha già rinunciato
                time.sleep(1.2)
            stato, tipo, corpo = RISPOSTE.get(percorso, (500, "text/plain", b"errore"))
        if stato != 200 and percorso in ("/registro", "/archivio"):
            corpo = b"errore"
        try:
            self.send_response(stato)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)
        except OSError:  # chi chiedeva ha chiuso la connessione (prova del tempo scaduto)
            pass


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


class BrowserCheCade:
    """Finto Playwright: Chromium parte, ma ogni richiesta finisce con l'errore che Playwright dà quando il sito
    chiude la connessione. È su più righe: dopo la prima c'è il registro delle chiamate."""

    def __init__(self):
        contesto = types.SimpleNamespace(request=types.SimpleNamespace(get=self.chiedi))
        browser = types.SimpleNamespace(new_context=lambda **parole: contesto, close=lambda: None)
        self.chromium = types.SimpleNamespace(launch=lambda: browser)

    def chiedi(self, url, timeout=None):
        raise RuntimeError(f"APIRequestContext.get: socket hang up\nCall log:\n  - → GET {url}\n    - user-agent: prova")

    def start(self):
        return self

    def stop(self):
        pass


class BrowserConPagina:
    """Finto Playwright con una pagina: le risposte alle richieste si danno in fila (l'ultima vale per le
    successive) e la navigazione può interrompersi, come quando un PDF fa partire lo scaricamento."""

    def __init__(self, risposte, titolo="Documento", inciampo=None):
        self.risposte, self.richieste, self.inciampo = list(risposte), 0, inciampo
        pagina = types.SimpleNamespace(goto=self.vai, wait_for_timeout=lambda millisecondi: None, title=lambda: titolo,
                                       inner_text=lambda selettore: "", close=lambda: None)
        contesto = types.SimpleNamespace(request=types.SimpleNamespace(get=self.chiedi), new_page=lambda: pagina)
        browser = types.SimpleNamespace(new_context=lambda **parole: contesto, close=lambda: None)
        self.chromium = types.SimpleNamespace(launch=lambda: browser)

    def vai(self, url, wait_until=None, timeout=None):
        if self.inciampo:
            raise RuntimeError(self.inciampo)

    def chiedi(self, url, timeout=None):
        stato, corpo = self.risposte[min(self.richieste, len(self.risposte) - 1)]
        self.richieste += 1
        return types.SimpleNamespace(status=stato, ok=200 <= stato < 300, body=lambda: corpo)

    def start(self):
        return self

    def stop(self):
        pass


def prove_delle_letture(controllo):
    """--aggiorna-data: le letture si annotano collegamento per collegamento, da qualunque rete, e la data di
    verifica è il giorno del collegamento letto da più tempo. Mai avanti senza prove, mai indietro."""
    adesso = controllo.oggi_in_italia()
    oggi, ieri, domani = adesso.isoformat(), (adesso - timedelta(days=1)).isoformat(), (adesso + timedelta(days=1)).isoformat()
    mese_fa = (adesso - timedelta(days=30)).isoformat()
    a, b, c, pagina = ("https://www.esempio.it/a.pdf", "https://www.esempio.it/b.pdf",
                       "https://www.esempio.it/catalogo/c.pdf", "https://www.esempio.it/pagina-a")
    documenti = {"gruppi": [{"documenti": [{"id": "a", "url": a, "pagina": {"url": pagina}}, {"id": "b", "url": b}]}]}
    catalogo = {"voci": [{"nome": "Prodotto", "formato": "pdf", "url": c, "byte": 1000},
                         {"nome": "Solo Word", "formato": "docx", "url": "https://www.esempio.it/catalogo/d.docx"}]}
    tutti = {a, b, c, pagina}
    veri = (controllo.RADICE, controllo.FILE_DOCUMENTI, controllo.FILE_CATALOGO, controllo.FILE_LETTURE,
            controllo.carica, controllo.controlla_dati, controllo.controlla_rete, sys.argv)
    elenchi = (controllo.errori, controllo.non_letti, controllo.novita, controllo.protetti, controllo.muti,
               controllo.da_rivedere, controllo.senza_browser, controllo.note_letture, *controllo.disciplinari.values())
    with tempfile.TemporaryDirectory() as temporanea:
        radice = Path(temporanea)
        controllo.RADICE = radice
        controllo.FILE_DOCUMENTI = radice / "cucina_emergenza.yaml"
        controllo.FILE_CATALOGO = radice / "disciplinari.json"
        controllo.FILE_LETTURE = radice / ".manuale" / "letture.json"

        def prepara(data, letture=None, letti_oggi=()):
            controllo.FILE_DOCUMENTI.write_text(f'# prova\nverificato: "{data}"\n', encoding="utf-8")
            controllo.FILE_CATALOGO.write_text('{\n  "verificato": "%s",\n  "voci": []\n}\n' % data, encoding="utf-8")
            documenti["verificato"] = catalogo["verificato"] = data
            controllo.FILE_LETTURE.parent.mkdir(exist_ok=True)
            if letture is None:
                controllo.FILE_LETTURE.unlink(missing_ok=True)
            else:
                controllo.FILE_LETTURE.write_text(letture if isinstance(letture, str) else json.dumps(letture), encoding="utf-8")
            for elenco in elenchi:
                elenco.clear()
            for insieme in (controllo.metodi, controllo.letti, controllo.pesi, controllo.confronti):
                insieme.clear()
            controllo.letti.update(letti_oggi)

        def scritta():
            return (re.search(r'^verificato: "([^"]+)"', controllo.FILE_DOCUMENTI.read_text(encoding="utf-8"), re.M).group(1),
                    json.loads(controllo.FILE_CATALOGO.read_text(encoding="utf-8"))["verificato"])

        def annotate():
            try:
                return json.loads(controllo.FILE_LETTURE.read_text(encoding="utf-8"))
            except FileNotFoundError:
                return None

        def giro(rotti=(), fonti=(), fermi=(), letti_oggi=(), argomenti=("--rete", "--aggiorna-data"), pesa=None):
            """Un giro intero di main(), di norma con --rete --aggiorna-data e senza --file: le richieste sono finte.
            `pesa`: quanti byte il sito dichiara oggi per il PDF del catalogo."""
            def rete_finta(*argomenti):
                controllo.letti.update(letti_oggi)
                if pesa:
                    controllo.pesi[c] = (pesa, "2026-11-20")
                controllo.errori.extend(rotti)
                controllo.non_letti.extend(fonti)
                controllo.muti.extend(fermi)
            controllo.carica = lambda: (documenti, catalogo)
            controllo.controlla_dati = lambda *argomenti: None
            controllo.controlla_rete = rete_finta
            sys.argv = [SCRIPT, *argomenti]
            uscita = io.StringIO()
            with contextlib.redirect_stdout(uscita):
                codice = controllo.main()
            return codice, uscita.getvalue()

        try:
            prepara(mese_fa, letti_oggi=tutti)
            controllo.aggiorna_verifica(documenti, catalogo)
            esito("letture: tutto letto oggi, la data di verifica diventa oggi nei due file e ogni collegamento ha il suo giorno",
                  scritta() == (oggi, oggi) and annotate() == dict.fromkeys(tutti, oggi) and documenti["verificato"] == oggi,
                  f"{scritta()} {annotate()}")

            prepara(mese_fa, letti_oggi=tutti - {b})
            controllo.aggiorna_verifica(documenti, catalogo)
            esito("letture: un collegamento mai letto tiene ferma la data, e il rapporto lo nomina",
                  scritta() == (mese_fa, mese_fa) and annotate() == dict.fromkeys(tutti - {b}, oggi)
                  and any("non risultano mai letti" in riga and b in riga for riga in controllo.note_letture),
                  f"{scritta()} {annotate()} {controllo.note_letture}")

            prepara(mese_fa, {a: ieri, b: mese_fa, c: ieri, pagina: ieri}, letti_oggi=tutti - {b})
            controllo.aggiorna_verifica(documenti, catalogo)
            esito("letture: un collegamento non letto oggi conserva il suo giorno, e la data resta quella",
                  scritta() == (mese_fa, mese_fa) and annotate() == {a: oggi, b: mese_fa, c: oggi, pagina: oggi}
                  and any(b in riga and controllo.giorno(mese_fa) in riga for riga in controllo.note_letture),
                  f"{scritta()} {annotate()} {controllo.note_letture}")

            prepara(mese_fa, {a: ieri, b: mese_fa, c: ieri, pagina: ieri}, letti_oggi={b})
            controllo.aggiorna_verifica(documenti, catalogo)
            esito("letture: riletto da un'altra rete il solo collegamento fermo, la data avanza al più vecchio degli altri",
                  scritta() == (ieri, ieri) and annotate() == {a: ieri, b: oggi, c: ieri, pagina: ieri}, f"{scritta()} {annotate()}")

            prepara(ieri, dict.fromkeys(tutti, mese_fa))
            controllo.aggiorna_verifica(documenti, catalogo)
            esito("letture: la data di verifica non torna mai indietro",
                  scritta() == (ieri, ieri) and annotate() == dict.fromkeys(tutti, mese_fa), f"{scritta()} {annotate()}")

            prepara(mese_fa, {a: domani, b: "2026-02-31", c: ieri, pagina: 5, "https://www.esempio.it/tolto.pdf": oggi})
            controllo.aggiorna_verifica(documenti, catalogo)
            esito("letture: un giorno nel futuro o scritto male vale come mai letto, e un collegamento uscito dai dati si toglie",
                  scritta() == (mese_fa, mese_fa) and annotate() == {c: ieri}, f"{scritta()} {annotate()}")

            prepara(mese_fa, "{ non è json", letti_oggi=tutti)
            controllo.aggiorna_verifica(documenti, catalogo)
            esito("letture: un file delle letture rovinato riparte da ciò che si legge oggi",
                  scritta() == (oggi, oggi) and annotate() == dict.fromkeys(tutti, oggi), f"{scritta()} {annotate()}")

            prepara(mese_fa, dict.fromkeys(tutti, mese_fa))
            codice, testo = giro(rotti=[f"documento «b»: HTTP 404: {b}"], letti_oggi=tutti - {b})
            esito("giro con un collegamento rotto: uscita 1, nessuna lettura annotata, data ferma",
                  codice == 1 and annotate() == dict.fromkeys(tutti, mese_fa) and scritta() == (mese_fa, mese_fa)
                  and "Letture annotate" not in testo, f"uscita {codice}, {annotate()}")

            prepara(mese_fa, dict.fromkeys(tutti, mese_fa))
            codice, testo = giro(fonti=[("www.esempio.it", "pagina del Ministero: HTTP 502")], letti_oggi=tutti)
            esito("giro con una fonte non letta: uscita 2, nessuna lettura annotata, data ferma",
                  codice == 2 and annotate() == dict.fromkeys(tutti, mese_fa) and scritta() == (mese_fa, mese_fa),
                  f"uscita {codice}, {annotate()}")

            prepara(mese_fa, {a: ieri, b: ieri, c: ieri, pagina: ieri})
            codice, testo = giro(fermi=[f"documento «b»: Error: APIRequestContext.get: socket hang up: {b}"], letti_oggi=tutti - {b})
            esito("giro con un sito che non risponde: uscita 3, le altre letture si annotano e la data arriva al giorno di quel collegamento",
                  codice == 3 and annotate() == {a: oggi, b: ieri, c: oggi, pagina: oggi} and scritta() == (ieri, ieri)
                  and f"Data scritta nei dati: {ieri}." in testo and "Letture annotate" in testo
                  and "--rete --browser --aggiorna-data" in testo, f"uscita {codice}, {annotate()}, {scritta()}")

            prepara(mese_fa, {a: ieri, b: ieri, c: ieri, pagina: ieri})
            codice, testo = giro(letti_oggi=tutti - {c})
            esito("giro senza rilievi e senza --file: i PDF del catalogo restano al loro giorno, e la data si ferma lì",
                  codice == 0 and scritta() == (ieri, ieri) and annotate() == {a: oggi, b: oggi, c: ieri, pagina: oggi}
                  and c in testo and "non può andare oltre" in testo and "Nessun problema." in testo,
                  f"uscita {codice}, {scritta()}, {annotate()}")

            prepara(mese_fa, {a: ieri, b: ieri, c: ieri, pagina: ieri})
            codice, testo = giro(letti_oggi=tutti, argomenti=("--rete", "--file", "--aggiorna-data"))
            esito("giro senza rilievi con --file, tutto letto: uscita 0, data di oggi",
                  codice == 0 and scritta() == (oggi, oggi) and "Ogni collegamento è stato letto in questo giro." in testo
                  and "Nessun problema." in testo, f"uscita {codice}, {scritta()}")

            prepara(mese_fa, {a: ieri, b: oggi, c: ieri, pagina: ieri})   # «b» letto oggi da un'altra rete
            codice, testo = giro(fermi=[f"documento «b»: Error: APIRequestContext.get: socket hang up: {b}"], letti_oggi=tutti - {b},
                                 argomenti=("--rete", "--file", "--aggiorna-data"))
            esito("giro con un sito che non risponde, già letto oggi da un'altra rete: uscita 3, data di oggi, e il rapporto lo spiega",
                  codice == 3 and scritta() == (oggi, oggi) and annotate() == dict.fromkeys(tutti, oggi)
                  and "letto oggi da un'altra rete" in testo and "letto in questo giro" not in testo,
                  f"uscita {codice}, {scritta()}, {annotate()}")

            # un giro cominciato ieri sera e finito dopo la mezzanotte: le letture portano il giorno dell'inizio
            prepara(mese_fa, dict.fromkeys(tutti, mese_fa))
            orologio_vero = controllo.oggi_in_italia
            controllo.oggi_in_italia = lambda: adesso - timedelta(days=1)

            def dopo_la_mezzanotte(*argomenti):
                controllo.oggi_in_italia = orologio_vero
                controllo.letti.update(tutti)
            try:
                controllo.carica = lambda: (documenti, catalogo)
                controllo.controlla_dati = lambda *argomenti: None
                controllo.controlla_rete = dopo_la_mezzanotte
                sys.argv = [SCRIPT, "--rete", "--file", "--aggiorna-data"]
                with contextlib.redirect_stdout(io.StringIO()):
                    codice = controllo.main()
            finally:
                controllo.oggi_in_italia = orologio_vero
            esito("un giro a cavallo della mezzanotte annota il giorno in cui è cominciato",
                  codice == 0 and annotate() == dict.fromkeys(tutti, ieri) and scritta() == (ieri, ieri),
                  f"uscita {codice}, {annotate()}, {scritta()}")

            prepara(mese_fa, [1, 2], letti_oggi=tutti)
            controllo.aggiorna_verifica(documenti, catalogo)
            esito("letture: un file delle letture che non è una mappa riparte da ciò che si legge oggi",
                  scritta() == (oggi, oggi) and annotate() == dict.fromkeys(tutti, oggi), f"{scritta()} {annotate()}")

            prepara(mese_fa, {a: ieri, b: ieri, c: ieri, pagina: ieri}, letti_oggi=tutti)
            controllo.aggiorna_verifica(documenti, catalogo, ieri)
            esito("letture: il giorno annotato è quello in cui il giro è cominciato, non quello in cui finisce",
                  annotate() == dict.fromkeys(tutti, ieri) and scritta() == (ieri, ieri), f"{scritta()} {annotate()}")

            # date diverse nei due file (non dovrebbe capitare: lo blocca il controllo dei dati): avanza solo la più vecchia
            prepara(mese_fa, dict.fromkeys(tutti, ieri))
            controllo.FILE_CATALOGO.write_text('{\n  "verificato": "%s",\n  "voci": []\n}\n' % oggi, encoding="utf-8")
            catalogo["verificato"] = oggi
            controllo.aggiorna_verifica(documenti, catalogo)
            esito("letture: con date diverse nei due file avanza solo quella rimasta indietro, l'altra non torna indietro",
                  scritta() == (ieri, oggi) and (documenti["verificato"], catalogo["verificato"]) == (ieri, oggi), f"{scritta()}")

            # --unisci-letture: le letture di un giro sommate a quelle già annotate (il workflow, sopra l'ultimo main)
            altro = radice / "letture-del-giro.json"
            prepara(mese_fa, {a: ieri, b: mese_fa, c: ieri, pagina: ieri})   # su main: «b» fermo a un mese fa
            altro.write_text(json.dumps({a: oggi, b: oggi, c: mese_fa, pagina: domani, "https://www.esempio.it/tolto.pdf": oggi}),
                             encoding="utf-8")
            codice, testo = giro(argomenti=("--unisci-letture", str(altro)))
            esito("--unisci-letture: per ogni collegamento vale il giorno più recente, il futuro e gli indirizzi tolti si scartano, la data è il più vecchio",
                  codice == 0 and annotate() == {a: oggi, b: oggi, c: ieri, pagina: ieri} and scritta() == (ieri, ieri)
                  and "Letture sommate" in testo, f"uscita {codice}, {annotate()}, {scritta()}")

            prepara(mese_fa, {a: ieri, b: mese_fa, c: ieri, pagina: ieri})
            altro.write_text("[1, 2]", encoding="utf-8")
            codice, testo = giro(argomenti=("--unisci-letture", str(altro)))
            esito("--unisci-letture con un file che non è una mappa: uscita 1, nulla cambia",
                  codice == 1 and annotate() == {a: ieri, b: mese_fa, c: ieri, pagina: ieri} and scritta() == (mese_fa, mese_fa)
                  and "deve essere una mappa" in testo, f"uscita {codice}, {annotate()}")

            prepara(mese_fa, {a: ieri, b: mese_fa, c: ieri, pagina: ieri})
            codice, testo = giro(argomenti=("--unisci-letture", str(radice / "non-esiste.json")))
            esito("--unisci-letture con un file che non c'è: uscita 1, nulla cambia",
                  codice == 1 and annotate() == {a: ieri, b: mese_fa, c: ieri, pagina: ieri} and scritta() == (mese_fa, mese_fa),
                  f"uscita {codice}, {annotate()}")

            prepara(ieri, {a: mese_fa, b: ieri, c: ieri, pagina: ieri})   # data portata avanti a mano: stato non valido
            altro.write_text(json.dumps({a: oggi}), encoding="utf-8")
            codice, testo = giro(argomenti=("--unisci-letture", str(altro)))
            esito("--unisci-letture su dati con la data portata avanti a mano: uscita 1, non somma nulla",
                  codice == 1 and annotate() == {a: mese_fa, b: ieri, c: ieri, pagina: ieri} and "non si porta avanti a mano" in testo,
                  f"uscita {codice}, {annotate()}")

            # il giro intero confronta il peso dei file solo con --file, dopo aver letto tutto
            prepara(ieri, dict.fromkeys(tutti, ieri))
            codice, testo = giro(letti_oggi=tutti, argomenti=("--rete", "--file", "--aggiorna-data"), pesa=1234)
            esito("giro con --file: un PDF del catalogo che oggi pesa diversamente dai dati è una novità (uscita 3), e le letture si annotano",
                  codice == 3 and "«Prodotto»: il file allo stesso indirizzo è cambiato: nei dati pesa 1000 byte, ora 1234 "
                  "(il sito del Ministero lo data al 20/11/2026)" in testo and "### Disciplinari nuovi, tolti o aggiornati" in testo
                  and scritta() == (oggi, oggi), f"uscita {codice}, {scritta()}, {testo[:600]}")
            prepara(ieri, dict.fromkeys(tutti, ieri))
            codice, testo = giro(letti_oggi=tutti, argomenti=("--rete", "--file", "--aggiorna-data"), pesa=1000)
            esito("giro con --file: con lo stesso peso dei dati nessuna novità (uscita 0)",
                  codice == 0 and "il file allo stesso indirizzo è cambiato" not in testo and "peso di 1 file del Ministero su 1" in testo,
                  f"uscita {codice}, {testo[:600]}")
            prepara(ieri, dict.fromkeys(tutti, ieri))
            codice, testo = giro(letti_oggi=tutti, pesa=1234)
            esito("giro senza --file: il peso non si confronta, e la riga dei disciplinari lo dice",
                  codice == 0 and "il file allo stesso indirizzo è cambiato" not in testo
                  and "peso dei file non confrontato: giro senza --file" in testo, f"uscita {codice}, {testo[:600]}")

            prepara(mese_fa, {a: ieri, c: ieri, pagina: ieri})
            codice, testo = giro(argomenti=())
            esito("senza rete: un collegamento senza lettura annotata è un avviso, non un errore",
                  codice == 0 and "Avviso: 1 collegamenti dei dati non hanno una lettura annotata" in testo and b in testo,
                  f"uscita {codice}, {testo[:300]}")
        finally:
            (controllo.RADICE, controllo.FILE_DOCUMENTI, controllo.FILE_CATALOGO, controllo.FILE_LETTURE,
             controllo.carica, controllo.controlla_dati, controllo.controlla_rete, sys.argv) = veri
            controllo.scadenza = float("inf")
            for elenco in elenchi:
                elenco.clear()
            for insieme in (controllo.metodi, controllo.letti, controllo.pesi, controllo.confronti):
                insieme.clear()


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
            for elenco in (controllo.errori, controllo.non_letti, controllo.protetti, controllo.da_rivedere, controllo.muti,
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


def prove_dello_script_delle_sintesi(ue):
    """Le funzioni di scripts/aggiorna-documenti-unici.py che decidono quale documento è di quale prodotto."""
    testo = ("C 440/7 Gazzetta ufficiale dell'Unione europea 26.11.2016 Pubblicazione di una domanda di modifica "
             "DOCUMENTO UNICO «TERRE TARENTINE» N. UE: PDO-IT-02120 1. Denominazione Terre Tarentine 2. Stato membro")
    forme = ue.denominazioni(["Terre Tarentine"])
    esito("sintesi: il titolo «DOCUMENTO UNICO» seguito dalla denominazione fra virgolette è riconosciuto",
          ue.che_sintesi_contiene(testo, forme) == ("unico", "")
          and ue.che_sintesi_contiene(testo.replace("DOCUMENTO UNICO", "documento unico"), forme) == ("", "")
          and ue.che_sintesi_contiene(testo.replace("DOCUMENTO UNICO", "SCHEDA RIEPILOGATIVA"), forme) == ("scheda", ""))
    bra = ue.denominazioni(["Bra"])
    fibra = "DOCUMENTO UNICO «Fibra di lino delle Fiandre» N. UE: PGI-BE-0001 1. Denominazione «Fibra di lino delle Fiandre»"
    esito("sintesi: un nome corto non si riconosce dentro un'altra parola («Bra» non è «fibra»)",
          ue.che_sintesi_contiene(testo, bra) == ("", "") and ue.che_sintesi_contiene(fibra, bra) == ("", "")
          and ue.che_sintesi_contiene("DOCUMENTO UNICO «Bra» N. UE: PDO-IT-0002-AM03 1. Denominazione «Bra»", bra) == ("unico", "")
          and ue.che_sintesi_contiene("DOCUMENTO UNICO «BRA DOP» 1. Denominazione", bra) == ("unico", ""))
    prosciutto = "DOCUMENTO UNICO «Prosciutto Toscano» N. UE: PDO-IT-1337 1. Denominazione «Prosciutto Toscano»"
    esito("sintesi: la sintesi di un altro prodotto che ne contiene il nome non si collega: è un dubbio da guardare",
          ue.che_sintesi_contiene(prosciutto, ue.denominazioni(["Toscano"])) == ("", "unico")
          and ue.che_sintesi_contiene(prosciutto, ue.denominazioni(["Prosciutto Toscano"])) == ("unico", ""))
    montasio = {"montasio"}
    esito("sintesi: il numero di fascicolo sotto il titolo vale come la denominazione, nei due formati della Gazzetta",
          ue.che_sintesi_contiene("DOCUMENTO UNICO «NOME SCRITTO IN ALTRO MODO» N. UE: PDO-IT-0012-AM01", montasio, "PDO-IT-0012") == ("unico", "")
          and ue.che_sintesi_contiene("SCHEDA RIEPILOGATIVA «ALTRO» N. CE: IT-PDO-0117-0012", montasio, "PDO-IT-0012") == ("scheda", "")
          and ue.che_sintesi_contiene("DOCUMENTO UNICO «ALTRO» N. UE: PDO-IT-02251", montasio, "PDO-IT-0012") == ("", "")
          and ue.che_sintesi_contiene("DOCUMENTO UNICO «ALTRO» N. UE: PGI-IT-0012", montasio, "PDO-IT-0012") == ("", "")
          and ue.che_sintesi_contiene("DOCUMENTO UNICO «Montasio» N. UE: PDO-IT-02251 – 20.12.2016", montasio, "PDO-IT-0012") == ("unico", "")
          and ue.ha_il_fascicolo("N. UE: DOP-IT-00012", "PDO-IT-0012") and not ue.ha_il_fascicolo("PDO-IT-0012", ""))
    stelvio = ue.denominazioni(["Stelvio o Stilfser"])
    esito("sintesi: «A / B», «A o B», «S.» per «San» e gli apostrofi tipografici danno le stesse denominazioni",
          ue.parole("TERRA D’OTRANTO") == ue.parole("Terra d'Otranto") == "terra d otranto"
          and stelvio == {"stelvio o stilfser", "stelvio", "stilfser"}
          and "pomodoro san marzano dell agro sarnese nocerino" in ue.denominazioni(["Pomodoro S. Marzano dell'Agro Sarnese-Nocerino"])
          and ue.che_sintesi_contiene("DOCUMENTO UNICO «Stelvio»/«Stilfser» N. UE", stelvio) == ("unico", "")
          and ue.che_sintesi_contiene("DOCUMENTO UNICO «Stilfser / Stelvio» N. UE", stelvio) == ("unico", "")
          and ue.compatto("Südtiroler Apfel") in ue.parti_del_nome("Mela Alto Adige o Südtiroler Apfel")
          and ue.compatto("Vermouth di Torino") in ue.parti_del_nome("Vermut di Torino / Vermouth di Torino"))
    uno = {"giIdentifier": "EUGI1", "fileNumber": "PDO-IT-0001", "protectedNames": ["Formaggio Alfa"], "status": "registered"}
    due = {"giIdentifier": "EUGI2", "fileNumber": "PDO-IT-0009", "protectedNames": ["Formaggio Alfa"], "status": "registered"}
    domanda = dict(due, status="applied")
    voce = {"nome": "Formaggio Alfa"}
    esito("sintesi: un prodotto si abbina al registro solo se la voce con quel nome è una",
          ue.abbina(voce, ue.indice_per_nome([uno])) is uno and ue.abbina(voce, ue.indice_per_nome([uno, due])) is None
          and ue.abbina(voce, ue.indice_per_nome([uno, domanda])) is uno and ue.abbina(voce, ue.indice_per_nome([])) is None)
    prima = {"publications": [{"text": "Official Journal C 1, 1.1.2020", "uri": "https://eur-lex.europa.eu/a"},
                              {"text": "Ares(2024)1", "uri": "88549"}]}
    dopo = {"publications": prima["publications"] + [{"text": "Official Journal C, C/2026/2790", "uri": "http://data.europa.eu/eli/C/2026/2790/oj"}]}
    lettera = {"publications": prima["publications"] + [{"text": "Ares(2026)2", "uri": "90001"}]}
    esito("sintesi: l'impronta del registro cambia con una pubblicazione nuova, anche senza data; non con una lettera",
          ue.impronta_del_registro(prima) != ue.impronta_del_registro(dopo)
          and ue.impronta_del_registro(prima) == ue.impronta_del_registro(lettera)
          and ue.impronta_del_registro({"publications": []}) == "" and ue.ultima_pubblicazione(dopo) == "2020-01-01")
    esito("sintesi: il numero CELEX si ricava dalle forme di indirizzo del registro; le rettifiche restano fuori",
          ue.celex_di("https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX%3A52016XC1126%2801%29") == ("52016XC1126(01)", None)
          and ue.celex_di("http://data.europa.eu/eli/reg_impl/2021/1174/oj") == ("32021R1174", None)
          and ue.celex_di("http://data.europa.eu/eli/C/2025/3944/oj") == (None, "http://publications.europa.eu/resource/oj/C_202503944")
          and ue.celex_di("http://data.europa.eu/eli/C/2025/3944/corrigendum/2025-10-20/oj") == (None, None))
    esito("sintesi: un numero CELEX di vecchio tipo («C1998/405/05») si legge; uno con altri segni si scarta",
          ue.celex_di("https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX%3AC1998%2F405%2F05") == ("C1998/405/05", None)
          and ue.celex_di("https://eur-lex.europa.eu/?uri=CELEX%3A52016XC1126%2801%29%22%20%7D%20UNION") == (None, None)
          and ue.a_gruppi(["52020XC0101(01)", "52020XC0101(01)", 'x" } UNION {', "C1998/405/05", None]) == [["52020XC0101(01)"]])
    atto = "26.11.2016 IT Gazzetta ufficiale dell'Unione europea C 440/7 DOCUMENTO UNICO «TERRE TARENTINE»"
    vecchia = ("Rettifica alla pubblicazione di una domanda di modifica (Gazzetta ufficiale dell'Unione europea C 440 del "
               "26 novembre 2016) Pagina 7, paragrafo 3.2. del documento unico: anziché: «≤ 70 %» leggasi: «≥ 70 %».")
    nuova = ("Rettifica della pubblicazione della comunicazione di una modifica ordinaria approvata "
             "(Gazzetta ufficiale dell'Unione europea C, C/2025/3944, 16 luglio 2025) Pagina 6, documento unico")
    altrui = ("Rettifica della comunicazione della Commissione nell'ambito dell'applicazione della direttiva 2006/42/CE "
              "relativa alle macchine (Gazzetta ufficiale dell'Unione europea C 136 del 26 maggio 2010) A pagina 32")
    ciauscolo, ribera = ue.denominazioni(["Ciauscolo"]), ue.denominazioni(["Arancia di Ribera"])
    esito("sintesi: una rettifica si collega se cita il prodotto, il numero dell'atto o il suo fascicolo della Gazzetta con l'anno",
          ue.rettifica_cita_l_atto(vecchia, "52016XC1126(01)", atto, forme, "2016-11-26")
          and ue.rettifica_cita_l_atto(nuova, "52025XC03944", "testo dell'atto", ciauscolo)
          and ue.rettifica_cita_l_atto("Rettifica … «Ciauscolo» N. UE: PGI-IT-0557", "52010XC0101(01)", "", ciauscolo))
    esito("sintesi: una rettifica di un altro atto, o dello stesso fascicolo in un altro anno, non si collega",
          not ue.rettifica_cita_l_atto(altrui, "52010XC0526(04)", "C 135/40 DOCUMENTO UNICO «ARANCIA DI RIBERA»", ribera, "2010-05-26")
          and not ue.rettifica_cita_l_atto(nuova, "52025XC03945", "testo dell'atto", bra)
          and not ue.rettifica_cita_l_atto(vecchia, "52016XC1126(01)", atto, forme, "2017-11-26")
          and not ue.rettifica_cita_l_atto(vecchia, "52016XC1126(01)", atto, forme)
          and not ue.rettifica_cita_l_atto("Comunicazione sul prodotto «Ciauscolo»", "52010XC0101(01)", "", ciauscolo))
    righe = [{"atto": {"value": "A"}, "rettifica": {"value": "AR(02)"}, "data": {"value": "2021-05-01"}},
             {"atto": {"value": "A"}, "rettifica": {"value": "AR(01)"}, "data": {"value": "2020-03-09"}},
             {"atto": {"value": "A"}, "rettifica": {"value": "AR(01)"}, "data": {"value": "2020-03-01"}},
             {"atto": {"value": "A"}, "rettifica": {"value": "AR(01)"}},
             {"atto": {"value": "B"}, "rettifica": {"value": "BR(01)"}}]
    esito("sintesi: le rettifiche dell'archivio si raccolgono per atto, una riga per rettifica con la data più vecchia",
          ue.righe_delle_rettifiche(righe) == {"A": [("AR(01)", "2020-03-01"), ("AR(02)", "2021-05-01")], "B": [("BR(01)", "")]})
    vero = (RADICE / "data" / "disciplinari.json").read_text(encoding="utf-8")
    esito("sintesi: il file dei dati è scritto nel formato dello script (un elemento per riga)",
          ue.testo_del_catalogo(json.loads(vero)) == vero,
          "dopo una modifica a mano: python3 scripts/aggiorna-documenti-unici.py --riscrivi")


def prove_del_lavoro_sulle_sintesi(ue):
    """cerca_sintesi, le rettifiche e main di scripts/aggiorna-documenti-unici.py, con un deposito già pieno e
    un archivio finto: ciò che non si legge o non si sa interpretare non deve cambiare i dati. Nessuna
    richiesta parte davvero: interroga e chiedi dello script sono sostituiti per la durata delle prove."""
    veri = (ue.interroga, ue.chiedi, ue.FILE_CATALOGO, ue.RADICE, ue.shutil, sys.argv)
    domande, tentate = [], []
    eurlex = "https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX%3A"

    def archivio(risposta):
        def interroga(domanda):
            domande.append(domanda)
            return risposta(domanda) if callable(risposta) else risposta
        ue.interroga = interroga

    def nessuna_richiesta(*argomenti, **parole):
        tentate.append(argomenti[:1])  # nessuna di queste prove deve arrivare a chiedere qualcosa a un sito
        return 0, b""

    def pulisci():
        ue.non_letti.clear()
        del domande[:]

    try:
        with tempfile.TemporaryDirectory() as cartella:
            ue.chiedi = nessuna_richiesta
            deposito = ue.Deposito(Path(cartella) / "deposito")

            def atto(celex, testo, pagine=3, kb=100):
                nome = re.sub(r"[^0-9A-Za-z]", "_", celex)
                deposito.scrivi({"pagine": pagine, "kb": kb}, "atti", f"{nome}.json")
                (deposito.base / "atti" / f"{nome}.txt").write_text(testo, encoding="utf-8")

            def manca(celex, ore_fa=0):
                percorso = deposito.base / "atti" / (re.sub(r"[^0-9A-Za-z]", "_", celex) + ".json")
                percorso.write_text(json.dumps({"manca": "l'archivio non ha l'atto in italiano"}), encoding="utf-8")
                if ore_fa:
                    quando = time.time() - ore_fa * 3600
                    os.utime(percorso, (quando, quando))

            def citata(quando, celex=None, uri=None, testo="Official Journal C 1"):
                return {"date": quando, "text": testo, "uri": uri or eurlex + urllib.parse.quote(celex, safe="")}

            def cerca(nome, *pubblicazioni, fascicolo="PDO-IT-0001"):
                pulisci()
                return ue.cerca_sintesi(deposito, {"nome": nome}, {"fileNumber": fascicolo, "protectedNames": [nome]},
                                        {"registration": {"officialPublication": list(pubblicazioni)}})

            unico = "pagina 3 DOCUMENTO UNICO «Formaggio Alfa» N. UE: PDO-IT-0001-AM01 1. Denominazione «Formaggio Alfa»" + " testo" * 60
            scheda = "pagina 3 SCHEDA RIEPILOGATIVA «Formaggio Alfa» N. CE: IT-PDO-0117-0001 1. Denominazione" + " testo" * 60
            senza_titolo = "Regolamento di esecuzione della Commissione recante iscrizione di una denominazione" + " testo" * 60
            atto("52022XC0303(01)", unico, pagine=7, kb=640)
            atto("52008XC0505(02)", scheda)
            atto("32023R0001", senza_titolo)
            archivio(None)  # se una di queste ricerche interrogasse l'archivio, non avrebbe risposta
            sintesi, letto, dubbi = cerca("Formaggio Alfa", citata("05-05-2008", "52008XC0505(02)"),
                                          citata("09-01-2023", "32023R0001"), citata("03-03-2022", "52022XC0303(01)"))
            esito("sintesi, ricerca: vale il documento unico più recente, non la scheda più vecchia né l'atto senza titolo",
                  letto and not dubbi and not domande and sintesi == {
                      "tipo": "unico", "url": "https://eur-lex.europa.eu/legal-content/IT/TXT/PDF/?uri=CELEX:52022XC0303%2801%29",
                      "data": "2022-03-03", "pagine": 7, "kb": 640}, f"{sintesi} {letto} {dubbi}")
            sintesi, letto, dubbi = cerca("Formaggio Alfa", citata("05-05-2008", "52008XC0505(02)"), citata("09-01-2023", "32023R0001"))
            esito("sintesi, ricerca: senza un documento unico vale la scheda riepilogativa",
                  letto and not dubbi and (sintesi or {}).get("tipo") == "scheda" and sintesi["data"] == "2008-05-05", f"{sintesi}")
            sintesi, letto, dubbi = cerca("Formaggio Alfa", citata("09-01-2023", "32023R0001"))
            esito("sintesi, ricerca: nessuna pubblicazione con il titolo, nessuna sintesi e nessun dubbio",
                  sintesi is None and letto and not dubbi)
            sintesi, letto, dubbi = cerca("Formaggio Alfa", citata("03-03-2022", "52022XC0303(01)"),
                                          citata("20-10-2025", uri="http://data.europa.eu/eli/C/2025/3944/corrigendum/2025-10-20/oj"))
            esito("sintesi, ricerca: una rettifica citata dal registro si salta, non ferma la ricerca",
                  letto and not dubbi and (sintesi or {}).get("data") == "2022-03-03" and not domande)

            nuova = citata("16-07-2025", uri="http://data.europa.eu/eli/C/2025/3944/oj", testo="Official Journal C, C/2025/3944")
            sintesi, letto, dubbi = cerca("Formaggio Alfa", citata("03-03-2022", "52022XC0303(01)"), nuova)
            esito("sintesi, ricerca: se l'archivio non risponde sulla pubblicazione più recente, il prodotto non si decide",
                  sintesi is None and not letto and not dubbi and len(ue.non_letti) == 1 and len(domande) == 1,
                  f"{sintesi} {letto} {dubbi} {ue.non_letti}")
            archivio([])
            sintesi, letto, dubbi = cerca("Formaggio Alfa", citata("03-03-2022", "52022XC0303(01)"), nuova)
            esito("sintesi, ricerca: una pubblicazione che l'archivio non conosce è da guardare a mano, non si salta",
                  sintesi is None and letto and len(dubbi) == 1 and "non sa interpretare" in dubbi[0] and not ue.non_letti, f"{dubbi}")
            atto("52025XC03944", unico.replace("AM01", "AM02"), pagine=5, kb=300)
            archivio(lambda domanda: [{"celex": {"value": "52025XC03944"}}] if "sameAs" in domanda else [])
            sintesi, letto, dubbi = cerca("Formaggio Alfa", citata("03-03-2022", "52022XC0303(01)"), nuova)
            esito("sintesi, ricerca: la pubblicazione citata con l'indirizzo ELI si trova chiedendo il numero CELEX all'archivio",
                  letto and not dubbi and (sintesi or {}).get("url", "").endswith("CELEX:52025XC03944") and sintesi["data"] == "2025-07-16",
                  f"{sintesi} {dubbi}")
            archivio(None)
            sintesi, letto, dubbi = cerca("Formaggio Alfa", citata("03-03-2022", "52022XC0303(01)"), nuova)
            esito("sintesi, ricerca: il numero già chiesto all'archivio si ricorda e non si richiede",
                  letto and not dubbi and (sintesi or {}).get("data") == "2025-07-16" and not domande, f"{sintesi} {domande}")

            sintesi, letto, dubbi = cerca("Formaggio Alfa", citata("03-03-2022", "52022XC0303(01)"), citata(None, "32023R0001"))
            esito("sintesi, ricerca: una pubblicazione senza data è da guardare a mano (non si sa qual è la più recente)",
                  sintesi is None and letto and len(dubbi) == 1 and "senza data" in dubbi[0], f"{dubbi}")
            sintesi, letto, dubbi = cerca("Formaggio Alfa", citata("03-03-2022", "52022XC0303(01)"),
                                          citata("01-02-2024", uri="https://www.esempio.it/gazzetta/1", testo="Official Journal L 1"))
            esito("sintesi, ricerca: un indirizzo che lo script non sa leggere è da guardare a mano",
                  sintesi is None and letto and len(dubbi) == 1 and "non sa interpretare" in dubbi[0], f"{dubbi}")
            atto("52021XC0707(03)", "DOCUMENTO UNICO «Prosciutto Toscano» N. UE: PDO-IT-1337 1. Denominazione «Prosciutto Toscano»" + " testo" * 60)
            sintesi, letto, dubbi = cerca("Toscano", citata("07-07-2021", "52021XC0707(03)"), fascicolo="PDO-IT-0200")
            esito("sintesi, ricerca: la sintesi di un altro prodotto, citata per questo, è da guardare a mano e non si collega",
                  sintesi is None and letto and len(dubbi) == 1 and "non come denominazione" in dubbi[0], f"{sintesi} {dubbi}")
            atto("C1998/405/05", scheda)
            sintesi, letto, dubbi = cerca("Formaggio Alfa", citata("24-12-1998", uri=eurlex + "C1998%2F405%2F05"))
            esito("sintesi, ricerca: una sintesi in un atto con il numero CELEX di vecchio tipo è da guardare a mano",
                  sintesi is None and letto and len(dubbi) == 1 and "vecchio tipo" in dubbi[0], f"{sintesi} {dubbi}")

            pochi_giorni_fa = date.today() - timedelta(days=5)
            appena_uscito = f"5{pochi_giorni_fa:%Y}XC{pochi_giorni_fa:%m%d}(07)"
            manca(appena_uscito)
            sintesi, letto, dubbi = cerca("Formaggio Alfa", citata("03-03-2022", "52022XC0303(01)"),
                                          citata(f"{pochi_giorni_fa:%d-%m-%Y}", appena_uscito))
            esito("sintesi, ricerca: un atto appena uscito senza testo italiano in archivio non si salta: si riprova",
                  sintesi is None and letto and len(dubbi) == 1 and "non ha ancora il testo in italiano" in dubbi[0], f"{sintesi} {dubbi}")
            manca("52012XC0404(05)")
            sintesi, letto, dubbi = cerca("Formaggio Alfa", citata("05-05-2008", "52008XC0505(02)"), citata("04-04-2012", "52012XC0404(05)"))
            esito("sintesi, ricerca: un atto vecchio senza testo italiano si salta, e vale la pubblicazione precedente",
                  letto and not dubbi and (sintesi or {}).get("data") == "2008-05-05", f"{sintesi} {dubbi}")
            atto("52022XC0303(01)R(01)", unico)
            sintesi, letto, dubbi = cerca("Formaggio Alfa", citata("03-03-2022", "52022XC0303(01)"),
                                          citata("10-10-2023", "52022XC0303(01)R(01)"))
            esito("sintesi, ricerca: una rettifica citata con il suo numero CELEX non diventa la sintesi",
                  letto and not dubbi and (sintesi or {}).get("url", "").endswith("CELEX:52022XC0303%2801%29"), f"{sintesi} {dubbi}")
            pulisci()
            a_mano = ue.cerca_sintesi(deposito, {"nome": "Formaggio Alfa"}, {"fileNumber": "PDO-IT-0001", "protectedNames": ["Formaggio Alfa"]},
                                      {"registration": {"officialPublication": [citata("03-03-2022", "52022XC0303(01)"),
                                                                                citata(None, "32023R0001")]}}, a_mano=True)
            esito("sintesi, ricerca: chi lancia lo script per un prodotto (--nome) salta la pubblicazione senza data",
                  a_mano[1] and not a_mano[2] and (a_mano[0] or {}).get("data") == "2022-03-03", f"{a_mano}")

            del_giorno = citata("26-09-2014", uri="https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:C:2014:336:FULL",
                                testo="Official Journal C 336, 26.09.2014")
            atto("52014XC0926(01)", senza_titolo)
            atto("52014XC0926(02)", unico.replace("Formaggio Alfa", "Salame Beta").replace("PDO-IT-0001", "PGI-IT-0002"))
            atto("52014XC0926(03)", unico)
            sintesi, letto, dubbi = cerca("Formaggio Alfa", del_giorno)
            esito("sintesi, ricerca: se il registro cita solo il fascicolo della Gazzetta, si provano gli avvisi di quel giorno",
                  letto and not dubbi and (sintesi or {}).get("url", "").endswith("CELEX:52014XC0926%2803%29") and not domande,
                  f"{sintesi} {dubbi} {domande}")
            for n in (3, 4, 5):
                manca(f"52014XC0926({n:02d})")
            sintesi, letto, dubbi = cerca("Formaggio Alfa", del_giorno)
            esito("sintesi, ricerca: dopo tre avvisi di fila senza testo italiano la ricerca del giorno si ferma",
                  sintesi is None and letto and not dubbi and not domande and not ue.non_letti, f"{sintesi} {domande}")

            # atti: il file si scarica solo dall'archivio, un numero strano non entra in una domanda, un «manca» scade
            pulisci()
            archivio([{"tipo": {"value": "pdfa1a"}, "item": {"value": "http://altrove.esempio.it/atto.pdf"}}])
            fuori = ue.atto_in_italiano(deposito, "52030XC0101(01)")
            esito("sintesi, atti: un file fuori dal sito dell'archivio non si scarica, ed è una fonte non letta",
                  fuori is None and not tentate and any("fuori dal suo sito" in riga for riga in ue.non_letti),
                  f"{fuori} {tentate} {ue.non_letti}")
            pulisci()
            esito("sintesi, atti: un numero CELEX con altri segni non entra in una domanda all'archivio",
                  ue.atto_in_italiano(deposito, '52030XC0101(01)" } UNION {') == {"manca": "numero CELEX non valido"} and not domande)
            manca("52031XC0101(01)")
            manca("52031XC0101(02)", ore_fa=ue.ORE_REGISTRO + 1)
            archivio([])
            pulisci()
            fresco, scaduto = ue.atto_in_italiano(deposito, "52031XC0101(01)"), ue.atto_in_italiano(deposito, "52031XC0101(02)")
            esito("sintesi, atti: un atto che l'archivio non aveva in italiano si richiede dopo 12 ore, non prima",
                  "manca" in fresco and "manca" in scaduto and len(domande) == 1 and "52031XC0101(02)" in domande[0], f"{domande}")

            due = [{"celex": {"value": "32025R0001"}}, {"celex": {"value": "52025XC09999"}}]
            archivio(due)
            diritto = ue.celex_della_risorsa(deposito, "http://publications.europa.eu/resource/oj/C_202509999")
            archivio(due[::-1])
            rovescio = ue.celex_della_risorsa(deposito, "http://publications.europa.eu/resource/oj/C_202509998")
            archivio([{"celex": {"value": "52025XC09997"}}, {"celex": {"value": "52025XC09996"}}])
            incerto = ue.celex_della_risorsa(deposito, "http://publications.europa.eu/resource/oj/C_202509997")
            esito("sintesi, atti: fra più numeri CELEX della stessa risorsa vale l'unico avviso della serie C; se sono due non si sceglie",
                  diritto == rovescio == "52025XC09999" and incerto == "", f"{diritto} {rovescio} {incerto!r}")
            (deposito.base / "atti" / "52032XC0101_01_.json").write_text('{"pagine": 3, "kb"', encoding="utf-8")
            atto("52032XC0101(02)", unico)
            (deposito.base / "atti" / "52032XC0101_02_.txt").unlink()
            archivio([])
            pulisci()
            troncato, senza_testo = ue.atto_in_italiano(deposito, "52032XC0101(01)"), ue.atto_in_italiano(deposito, "52032XC0101(02)")
            esito("sintesi, atti: un file del deposito rimasto a metà, o senza il suo testo, vale come non scaricato e si richiede",
                  "manca" in troncato and "manca" in senza_testo and len(domande) == 2, f"{troncato} {senza_testo} {len(domande)}")
            archivio([{"atto": {"value": "52020XC0101(01)"}}])
            esito("sintesi, rettifiche: una risposta dell'archivio in una forma inattesa vale come archivio muto",
                  ue.rettifiche_nell_archivio(["52020XC0101(01)"]) is None)

            # rettifiche: si collega quella che cita l'atto; una recente senza testo italiano non si archivia
            atto("52016XC1126(01)", "26.11.2016 IT Gazzetta ufficiale dell'Unione europea C 440/7 DOCUMENTO UNICO «TERRE TARENTINE»" + " testo" * 60)
            atto("52016XC1126(01)R(01)", "Rettifica alla pubblicazione di una domanda di modifica (Gazzetta ufficiale dell'Unione "
                 "europea C 440 del 26 novembre 2016) Pagina 7: anziché: «≤ 70 %» leggasi: «≥ 70 %»." + " testo" * 60, pagine=1, kb=390)
            manca("52016XC1126(01)R(02)")
            manca("52016XC1126(01)R(03)")
            terre = {"nome": "Terre Tarentine", "sintesi": {"tipo": "unico", "data": "2016-11-26", "pagine": 6, "kb": 400,
                                                             "url": ue.EURLEX_PDF.format("52016XC1126%2801%29")}}
            oggi = date.today().isoformat()
            pulisci()
            avvisi = ue.aggiorna_rettifiche(deposito, terre, [("52016XC1126(01)R(01)", "2017-02-02"), ("52016XC1126(01)R(02)", "2017-03-03"),
                                                              ("52016XC1126(01)R(03)", oggi)], ue.denominazioni(["Terre Tarentine"]))
            esito("sintesi, rettifiche: collegata quella che cita l'atto, annotata la vecchia senza testo italiano, in attesa la recente",
                  terre["sintesi"].get("rettifiche") == [{"url": ue.EURLEX_PDF.format("52016XC1126%2801%29R%2801%29"), "data": "2017-02-02",
                                                          "pagine": 1, "kb": 390}]
                  and terre["sintesi"].get("rettifiche_altre") == ["52016XC1126(01)R(02)"]
                  and len(avvisi or []) == 1 and "52016XC1126(01)R(03)" in avvisi[0] and not domande, f"{terre['sintesi']} {avvisi}")
            come_era = json.dumps(terre, sort_keys=True)
            note_oggi = [("52016XC1126(01)R(01)", "2017-02-02"), ("52016XC1126(01)R(02)", "2017-03-03")]
            testo_della_rettifica = (deposito.base / "atti" / "52016XC1126_01_R_01_.txt").read_text(encoding="utf-8")
            manca("52016XC1126(01)R(01)")
            avvisi = ue.aggiorna_rettifiche(deposito, terre, note_oggi, ue.denominazioni(["Terre Tarentine"]), sempre=True)
            esito("sintesi, rettifiche: una rettifica collegata di cui oggi manca il testo italiano resta collegata, e lo script lo dice",
                  json.dumps(terre, sort_keys=True) == come_era and len(avvisi or []) == 1 and "resta com'era" in avvisi[0],
                  f"{terre['sintesi']} {avvisi}")
            atto("52016XC1126(01)R(01)", testo_della_rettifica, pagine=1, kb=390)
            testo_dell_atto = (deposito.base / "atti" / "52016XC1126_01_.txt").read_text(encoding="utf-8")
            manca("52016XC1126(01)")
            pulisci()
            senza_atto = ue.aggiorna_rettifiche(deposito, terre, note_oggi, ue.denominazioni(["Terre Tarentine"]), sempre=True)
            esito("sintesi, rettifiche: se oggi manca il testo italiano dell'atto, è una fonte non letta e le rettifiche restano",
                  senza_atto is None and json.dumps(terre, sort_keys=True) == come_era and len(ue.non_letti) == 1,
                  f"{senza_atto} {ue.non_letti}")
            atto("52016XC1126(01)", testo_dell_atto)
            avvisi = ue.aggiorna_rettifiche(deposito, terre, [], ue.denominazioni(["Terre Tarentine"]), sempre=True)
            rimaste = json.dumps(terre, sort_keys=True) == come_era
            tolte = ue.aggiorna_rettifiche(deposito, terre, [], ue.denominazioni(["Terre Tarentine"]), sempre=True, anche_meno=True)
            esito("sintesi, rettifiche: se l'archivio non restituisce più una rettifica nota, resta com'era; si toglie solo con --nome",
                  rimaste and len(avvisi or []) == 1 and "non restituisce più" in avvisi[0] and "52016XC1126(01)R(01)" in avvisi[0]
                  and tolte == [] and "rettifiche" not in terre["sintesi"] and "rettifiche_altre" not in terre["sintesi"],
                  f"{rimaste} {avvisi} {tolte} {terre['sintesi']}")

            # main: un catalogo finto, con registro e schede già nel deposito
            ue.RADICE = Path(cartella)
            ue.FILE_CATALOGO = Path(cartella) / "disciplinari.json"
            ue.shutil = types.SimpleNamespace(which=lambda programma: "/usr/bin/" + programma)
            alfa = {"giIdentifier": "EUGI0001", "fileNumber": "PDO-IT-0001", "protectedNames": ["Formaggio Alfa"], "status": "registered",
                    "countries": ["IT"], "productType": "FOOD",
                    "publications": [{"text": "Official Journal C 61, 3.3.2022", "uri": eurlex + "52022XC0303%2801%29"}]}
            scheda_alfa = {"registration": {"officialPublication": [citata("03-03-2022", "52022XC0303(01)")]}}
            catalogo = {"verificato": "2026-11-24", "voci": [{"nome": "Formaggio Alfa", "tipo": "DOP"}, {"nome": "Pizza Finta", "tipo": "STG"}]}
            ue.FILE_CATALOGO.write_text(ue.testo_del_catalogo(catalogo), encoding="utf-8")

            def lancia_main(*argomenti, registro=None, scheda_del_prodotto=None):
                pulisci()
                if registro is not None:
                    deposito.scrivi(registro, "elenco.json")
                if scheda_del_prodotto is not None:
                    deposito.scrivi(scheda_del_prodotto, "schede", "EUGI0001.json")
                sys.argv = [SCRIPT_SINTESI, "--cartella", str(deposito.base), *argomenti]
                uscita_testo = io.StringIO()
                with contextlib.redirect_stdout(uscita_testo), contextlib.redirect_stderr(uscita_testo):
                    try:
                        codice = ue.main()
                    except SystemExit as e:
                        codice = e.code
                return codice, uscita_testo.getvalue(), ue.FILE_CATALOGO.read_text(encoding="utf-8")

            archivio([])
            codice, detto, scritto = lancia_main(registro=[alfa], scheda_del_prodotto=scheda_alfa)
            voce = json.loads(scritto)["voci"][0]
            esito("sintesi, lavoro: un prodotto mai letto prende fascicolo, sintesi e impronta del registro (uscita 0)",
                  codice == 0 and voce.get("fascicolo") == "PDO-IT-0001" and voce.get("sintesi", {}).get("data") == "2022-03-03"
                  and voce.get("registro_ue") == ue.impronta_del_registro(alfa) and "sintesi" not in json.loads(scritto)["voci"][1],
                  f"uscita {codice}: {detto[-300:]}")
            prima = scritto
            cresciuto = dict(alfa, publications=alfa["publications"] + [{"text": "Official Journal C, C/2026/100",
                                                                           "uri": "http://data.europa.eu/eli/C/2026/100/oj"}])
            scheda_cresciuta = {"registration": scheda_alfa["registration"], "amendment": [
                {"type": "STANDARD_AMENDMENT", "status": "APPROVED",
                 "officialPublication": [citata("05-01-2026", uri="http://data.europa.eu/eli/C/2026/100/oj", testo="Official Journal C, C/2026/100")]}]}
            archivio(None)
            codice, detto, scritto = lancia_main(registro=[cresciuto], scheda_del_prodotto=scheda_cresciuta)
            esito("sintesi, lavoro: pubblicazione nuova e archivio muto, il file dei dati resta identico e l'uscita è 1",
                  codice == 1 and scritto == prima and "non si sono fatte leggere" in detto, f"uscita {codice}: {detto[-300:]}")
            archivio([])
            codice, detto, scritto = lancia_main()
            esito("sintesi, lavoro: pubblicazione che non si sa interpretare, il file resta identico, impronta compresa (uscita 3)",
                  codice == 3 and scritto == prima and "Da guardare" in detto and "resta com'era" in detto, f"uscita {codice}: {detto[-300:]}")
            atto("52026XC00100", unico.replace("AM01", "AM03"), pagine=4, kb=250)
            archivio(lambda domanda: [{"celex": {"value": "52026XC00100"}}] if "sameAs" in domanda else [])
            codice, detto, scritto = lancia_main()
            voce = json.loads(scritto)["voci"][0]
            esito("sintesi, lavoro: quando l'archivio risponde, la sintesi passa alla pubblicazione nuova e l'impronta si aggiorna",
                  codice == 0 and voce["sintesi"]["data"] == "2026-01-05" and voce["sintesi"]["url"].endswith("CELEX:52026XC00100")
                  and voce["registro_ue"] == ue.impronta_del_registro(cresciuto) and not list(ue.FILE_CATALOGO.parent.glob("*.tmp")),
                  f"uscita {codice}: {detto[-300:]}")
            prima = scritto
            archivio([])
            codice, detto, scritto = lancia_main(registro=[alfa], scheda_del_prodotto=scheda_alfa)
            esito("sintesi, lavoro: se la ricerca di oggi darebbe una sintesi più vecchia di quella pubblicata, il file resta identico (uscita 3)",
                  codice == 3 and scritto == prima and "una sintesi più vecchia (2022-03-03)" in detto, f"uscita {codice}: {detto[-300:]}")
            terza = "http://data.europa.eu/eli/C/2026/200/oj"
            rinumerato = dict(cresciuto, fileNumber="PDO-IT-0099",
                              publications=cresciuto["publications"] + [{"text": "Official Journal C, C/2026/200", "uri": terza}])
            scheda_rinumerata = {"registration": scheda_alfa["registration"], "amendment": scheda_cresciuta["amendment"] + [
                {"type": "STANDARD_AMENDMENT", "status": "APPROVED",
                 "officialPublication": [citata("09-02-2026", uri=terza, testo="Official Journal C, C/2026/200")]}]}
            archivio(None)
            codice, detto, scritto = lancia_main(registro=[rinumerato], scheda_del_prodotto=scheda_rinumerata)
            dopo = json.loads(scritto)["voci"][0]
            esito("sintesi, lavoro: se il registro cambia il fascicolo e la pubblicazione nuova non si legge, cambia solo il fascicolo, e si conta",
                  codice == 1 and dopo["fascicolo"] == "PDO-IT-0099" and dopo["sintesi"] == voce["sintesi"]
                  and dopo["registro_ue"] == voce["registro_ue"] and "Voci cambiate: 1." in detto, f"uscita {codice}: {detto[-300:]}")
            prima = scritto
            codice, detto, scritto = lancia_main("--nome", "Formaggio Che Non Esiste")
            esito("sintesi, lavoro: un nome che il catalogo non ha ferma lo script, senza toccare il file",
                  codice == 2 and scritto == prima and "non c'è un prodotto con questo nome" in detto, f"uscita {codice}: {detto[-200:]}")
            archivio([])
            codice, detto, scritto = lancia_main(registro=[dict(cresciuto, protectedNames=["Formaggio Con Un Altro Nome"])])
            esito("sintesi, lavoro: un prodotto che il registro non ha più con quel nome resta com'era ed è da guardare (uscita 3)",
                  codice == 3 and scritto == prima and "Senza una voce con lo stesso nome" in detto, f"uscita {codice}: {detto[-300:]}")
            codice, detto, scritto = lancia_main("--nome", "Pizza Finta", registro=[rinumerato])
            esito("sintesi, lavoro: una STG chiesta con --nome ferma lo script con il motivo",
                  codice == 2 and scritto == prima and "le STG non sono nel registro" in detto, f"uscita {codice}: {detto[-200:]}")
            codice, detto, scritto = lancia_main("--nome", "Formaggio Alfa", registro=[alfa], scheda_del_prodotto=scheda_alfa)
            accettata = json.loads(scritto)["voci"][0]
            esito("sintesi, lavoro: chi lancia lo script per quel prodotto (--nome) accetta la sintesi più vecchia",
                  codice == 0 and accettata["sintesi"]["data"] == "2022-03-03" and accettata["registro_ue"] == ue.impronta_del_registro(alfa),
                  f"uscita {codice}: {detto[-300:]}")
            atto("52021XC0909(04)", unico.replace("Formaggio Alfa", "Olio Gamma").replace("PDO-IT-0001", "PDO-IT-0003"))
            gamma = {"giIdentifier": "EUGI0003", "fileNumber": "PDO-IT-0003", "protectedNames": ["Olio Gamma"], "status": "registered",
                     "countries": ["IT"], "productType": "FOOD", "publications": [{"text": "Ares(2021)1", "uri": "88549"}]}
            deposito.scrivi({"registration": {"officialPublication": [citata("09-09-2021", "52021XC0909(04)")]}}, "schede", "EUGI0003.json")
            ue.FILE_CATALOGO.write_text(ue.testo_del_catalogo({"verificato": "2026-11-24", "voci": [{"nome": "Olio Gamma", "tipo": "DOP"}]}),
                                        encoding="utf-8")
            codice, detto, scritto = lancia_main(registro=[gamma])
            esito("sintesi, lavoro: senza pubblicazioni con un indirizzo nell'elenco del registro la sintesi non si scrive (uscita 3)",
                  codice == 3 and "sintesi" not in json.loads(scritto)["voci"][0] and "non cita pubblicazioni con un indirizzo" in detto,
                  f"uscita {codice}: {detto[-300:]}")
            esito("sintesi: nessuna di queste prove ha chiesto qualcosa a un sito", not tentate, f"{tentate}")
    finally:
        ue.interroga, ue.chiedi, ue.FILE_CATALOGO, ue.RADICE, ue.shutil, sys.argv = veri
        ue.non_letti.clear()


def prove_delle_sintesi(controllo, base):
    """Registro europeo e archivio dell'UE finti: che cosa è novità, che cosa è rotto, che cosa è fonte non letta."""
    ue = controllo.documenti_unici()
    prove_dello_script_delle_sintesi(ue)
    pausa_vera, ue.PAUSA = ue.PAUSA, 0
    try:
        dentro, fuori = ue.chiedi(base + "/vero.pdf", solo_da=base + "/"), ue.chiedi(base + "/celex/52020XC0101", solo_da=base + "/celex/")
    finally:
        ue.PAUSA = pausa_vera
    esito("sintesi, atti: un file che arriva, dopo un rinvio, da un altro indirizzo non si accetta",
          dentro[0] == 200 and dentro[1].startswith(b"%PDF") and fuori == (0, b""), f"{dentro[0]} {fuori}")
    prove_del_lavoro_sulle_sintesi(ue)
    veri = (ue.REGISTRO, controllo.SPARQL_UE, controllo.ARCHIVIO_UE)
    ue.REGISTRO, controllo.SPARQL_UE, controllo.ARCHIVIO_UE = base + "/registro", base + "/archivio", base + "/celex/{}"
    pdf = "https://eur-lex.europa.eu/legal-content/IT/TXT/PDF/?uri=CELEX:{}"

    def del_registro(numero, nome, *pubblicazioni):
        return {"giIdentifier": "EUGI" + numero[-4:], "fileNumber": numero, "protectedNames": [nome], "status": "registered",
                "countries": ["IT"], "productType": "FOOD",
                "publications": [{"text": f"Official Journal C {n}, {quando}", "uri": f"https://eur-lex.europa.eu/{n}"}
                                 for n, quando in pubblicazioni]}

    registro = [del_registro("PDO-IT-0001", "Formaggio Alfa", (1, "1.1.2020")),
                del_registro("PGI-IT-0002", "Salame Beta", (2, "2.2.2021"), (3, "3.3.2022")),
                del_registro("PDO-IT-0003", "Olio Gamma", (4, "4.4.1997")),
                {"giIdentifier": "EUGI9999", "fileNumber": "PDO-FR-0001", "protectedNames": ["Fromage"], "status": "registered",
                 "countries": ["FR"], "productType": "FOOD", "publications": []}]
    impronta = {v["protectedNames"][0]: ue.impronta_del_registro(v) for v in registro}
    catalogo = {"voci": [
        {"nome": "Formaggio Alfa", "tipo": "DOP", "fascicolo": "PDO-IT-0001", "registro_ue": impronta["Formaggio Alfa"],
         "sintesi": {"tipo": "unico", "url": pdf.format("52020XC0101%2801%29"), "data": "2020-01-01", "pagine": 3, "kb": 100}},
        {"nome": "Salame Beta", "tipo": "IGP", "fascicolo": "PGI-IT-2", "registro_ue": impronta["Salame Beta"],
         "sintesi": {"tipo": "unico", "url": pdf.format("52021XC0202%2802%29"), "data": "2021-02-02", "pagine": 5, "kb": 200,
                     "rettifiche": [{"url": pdf.format("52021XC0202%2802%29R%2801%29"), "data": "2021-06-01", "pagine": 1, "kb": 50}],
                     "rettifiche_altre": ["52021XC0202(02)R(02)"]}},
        {"nome": "Olio Gamma", "tipo": "DOP", "fascicolo": "PDO-IT-0003", "registro_ue": impronta["Olio Gamma"]},
        {"nome": "Pizza Finta", "tipo": "STG"}]}
    note = {"52021XC0202(02)": [("52021XC0202(02)R(01)", "2021-06-01"), ("52021XC0202(02)R(02)", "2021-07-01")]}

    def giro(nome, atteso, registro_finto=registro, disciplinari=(0, 0, 0), **finto):
        """`disciplinari`: quante righe il giro deve mettere fra i disciplinari nuovi, tolti e aggiornati."""
        FINTO.update({"registro": registro_finto, "stato_registro": 200, "stato_archivio": 200, "fuori_dal_gruppo": set(),
                      "inesistenti": set(), "rettifiche": note})
        FINTO.update(finto)
        for elenco in (controllo.errori, controllo.non_letti, controllo.novita, controllo.protetti, controllo.da_rivedere,
                       controllo.muti, *controllo.disciplinari.values()):
            elenco.clear()
        controllo.metodi.clear()
        controllo.di_fila.clear()
        controllo.confronti.clear()
        controllo.controlla_europa(json.loads(json.dumps(catalogo)))
        visto = (len(controllo.errori), len(controllo.non_letti), len(controllo.novita), controllo.metodi["archivio dell'UE"])
        testo = " | ".join(controllo.errori + [t for _, t in controllo.non_letti] + controllo.novita)
        fra_i_disciplinari = tuple(len(controllo.disciplinari[k]) for k in ("nuovi", "tolti", "aggiornati"))
        esito(nome, visto == atteso[:4] and all(pezzo in testo for pezzo in atteso[4:]) and fra_i_disciplinari == disciplinari,
              f"rotti, non letti, novità, atti trovati: {visto}; atteso {atteso[:4]} con {atteso[4:]}; nuovi, tolti, "
              f"aggiornati: {fra_i_disciplinari}, attesi {disciplinari}; {testo[:300]}")

    try:
        giro("sintesi: registro e archivio uguali ai dati, nessun rilievo (il fascicolo «PGI-IT-2» vale «PGI-IT-0002»)", (0, 0, 0, 3))
        esito("registro: il giro conta i prodotti italiani registrati che ha confrontato, e sa di aver letto l'archivio per intero",
              controllo.confronti.get("registro") == 3 and controllo.confronti.get("archivio") is True, controllo.confronti)
        giro("sintesi: una pubblicazione nuova nel registro è una novità, fra i disciplinari aggiornati",
             (0, 0, 1, 3, "Formaggio Alfa", "pubblicazioni diverse", "07/07/2026"), disciplinari=(0, 0, 1),
             registro_finto=[del_registro("PDO-IT-0001", "Formaggio Alfa", (1, "1.1.2020"), (7, "7.7.2026"))] + registro[1:])
        giro("sintesi: un fascicolo cambiato nel registro è una novità", (0, 0, 1, 3, "Salame Beta", "PGI-IT-0099"),
             registro_finto=[registro[0], dict(registro[1], fileNumber="PGI-IT-0099")] + registro[2:])
        giro("sintesi: un prodotto che il registro non ha più è una novità, fra i disciplinari tolti",
             (0, 0, 1, 3, "Olio Gamma", "non c'è più un solo prodotto"), disciplinari=(0, 1, 0),
             registro_finto=registro[:2] + registro[3:])
        giro("sintesi: due voci del registro con lo stesso nome sono una novità sola, e nessuna delle due è un prodotto nuovo",
             (0, 0, 1, 3, "Olio Gamma"), disciplinari=(0, 1, 0),
             registro_finto=registro + [dict(registro[2], giIdentifier="EUGI8888", fileNumber="PDO-IT-0888")])
        # disciplinari nuovi e tolti (Alessandro, 25/11/2026): il registro europeo li dice con una richiesta sola
        nuovo = dict(del_registro("PGI-IT-0004", "Pane Delta", (9, "9.9.2026")), giType="PGI", euProtectionDate="2026-09-09")
        giro("registro: un prodotto italiano registrato che il catalogo non ha è un disciplinare nuovo",
             (0, 0, 1, 3, "prodotto nuovo nel registro europeo", "«Pane Delta»", "IGP, fascicolo PGI-IT-0004", "09/09/2026"),
             disciplinari=(1, 0, 0), registro_finto=registro + [nuovo])
        giro("registro: una domanda e una pubblicazione non ancora registrate non sono disciplinari nuovi", (0, 0, 0, 3),
             registro_finto=registro + [dict(nuovo, status="applied"), dict(nuovo, giIdentifier="EUGI0005", status="published")])
        esito("registro: nel conto dei prodotti confrontati entrano solo quelli registrati, non le domande",
              controllo.confronti.get("registro") == 3, controllo.confronti)
        giro("registro: un prodotto che il catalogo non ha, ma segnato come tolto, non è un disciplinare nuovo", (0, 0, 0, 3),
             registro_finto=registro + [dict(nuovo, removedFlag=True)])
        giro("registro: un prodotto del catalogo segnato come tolto è un disciplinare tolto",
             (0, 0, 1, 3, "Olio Gamma", "non è più fra i prodotti registrati", "segnato come tolto"), disciplinari=(0, 1, 0),
             registro_finto=registro[:2] + [dict(registro[2], removedFlag=True)] + registro[3:])
        giro("registro: un prodotto del catalogo che non ha più lo stato «registered» è un disciplinare tolto",
             (0, 0, 1, 3, "Olio Gamma", "non è più fra i prodotti registrati", "«applied»"), disciplinari=(0, 1, 0),
             registro_finto=registro[:2] + [dict(registro[2], status="applied")] + registro[3:])
        giro("sintesi: registro muto, fonte non letta; l'archivio si controlla lo stesso", (0, 1, 0, 3, "registro europeo eAmbrosia", "HTTP 500"),
             stato_registro=500)
        giro("sintesi: registro senza prodotti italiani, fonte non letta", (0, 1, 0, 3, "senza prodotti italiani"),
             registro_finto=registro[3:])
        giro("sintesi: registro che ha perso più di metà dei prodotti, fonte letta male e nessuna novità", (0, 1, 0, 3, "2 prodotti su 3"),
             registro_finto=registro[:1] + registro[3:])
        giro("sintesi: un atto che l'archivio non ha più è un collegamento rotto", (1, 0, 0, 2, "Formaggio Alfa", "52020XC0101(01)", "non esiste"),
             fuori_dal_gruppo={"52020XC0101(01)"}, inesistenti={"52020XC0101(01)"})
        giro("sintesi: una risposta a gruppi incompleta non rompe nulla, se l'atto da solo risponde", (0, 0, 0, 3),
             fuori_dal_gruppo={"52020XC0101(01)", "52021XC0202(02)R(01)"})
        giro("sintesi: una rettifica che i dati non conoscono è una novità, fra i disciplinari aggiornati",
             (0, 0, 1, 3, "Formaggio Alfa", "52020XC0101(01)R(01)", "05/05/2025"), disciplinari=(0, 0, 1),
             rettifiche=dict(note, **{"52020XC0101(01)": [("52020XC0101(01)R(01)", "2025-05-05")]}))
        giro("sintesi: archivio muto, due fonti non lette (esistenza e rettifiche) e nessun collegamento rotto", (0, 2, 0, 0, "non ha detto se esistono", "rettifiche nuove"),
             stato_archivio=503)
        esito("archivio: se non si è fatto leggere, il giro non lo dà per letto (gli «aggiornati» restano da verificare)",
              controllo.confronti.get("archivio") is False and controllo.confronti.get("registro") == 3, controllo.confronti)
        giro("sintesi: se l'archivio non restituisce più le rettifiche che i dati conoscono, la risposta non vale (fonte non letta)",
             (0, 1, 0, 3, "non ha restituito 2 rettifiche", "52021XC0202(02)R(01)", '--nome "Salame Beta"'), rettifiche={})

        # documenti su EUR-Lex: l'esistenza la dice l'archivio dell'UE, poi si chiede l'indirizzo del PDF
        def eurlex(nome, percorso, atteso):
            FINTO.update({"stato_archivio": 200, "inesistenti": set()})
            for elenco in (controllo.errori, controllo.non_letti, controllo.novita, controllo.protetti, controllo.da_rivedere, controllo.muti):
                elenco.clear()
            controllo.metodi.clear()
            controllo.di_fila.clear()
            controllo.letti.clear()
            indirizzo = f"{base}{percorso}?uri=CELEX:52020XC0101%2801%29"
            controllo.controlla_ue("documento «prova»", indirizzo)
            controllo.chiudi_da_rivedere(False)
            visto = (len(controllo.errori), len(controllo.non_letti), len(controllo.protetti), len(controllo.muti),
                     controllo.metodi["richiesta diretta"], controllo.metodi["archivio dell'UE"], int(controllo.letti == {indirizzo}))
            esito(nome, visto == atteso and (atteso[6] or not controllo.letti),
                  f"rotti, non letti, protetti, muti, letti, confermati dall'archivio, segnato per le letture: {visto}; atteso {atteso}")

        eurlex("EUR-Lex: il PDF risponde, letto con la richiesta diretta", "/vero.pdf", (0, 0, 0, 0, 1, 0, 1))
        eurlex("EUR-Lex: risposta 202 senza contenuto, vale l'esistenza nell'archivio dell'UE", "/attesa.pdf", (0, 0, 0, 0, 0, 1, 1))
        eurlex("EUR-Lex: errore del server sull'indirizzo del PDF, «non controllato» e non fonte non letta", "/guasto.pdf", (0, 0, 0, 1, 0, 0, 0))
        eurlex("EUR-Lex: rifiuto (403) sull'indirizzo del PDF, «non controllato» e non fonte non letta", "/rifiuto.pdf", (0, 0, 1, 0, 0, 0, 0))
        eurlex("EUR-Lex: un 400 sull'indirizzo del PDF resta una fonte non letta", "/negato.pdf", (0, 1, 0, 0, 0, 0, 0))
        eurlex("EUR-Lex: un 404 sull'indirizzo del PDF è un collegamento rotto", "/manca.pdf", (1, 0, 0, 0, 0, 0, 0))
        vuoto = {"voci": [{"nome": "Formaggio Alfa", "tipo": "DOP"}, {"nome": "Pizza Finta", "tipo": "STG"}]}
        for elenco in (controllo.errori, controllo.non_letti, controllo.novita):
            elenco.clear()
        FINTO["stato_registro"] = 500
        controllo.controlla_europa(vuoto)
        esito("sintesi: un catalogo senza dati europei non interroga il registro",
              not controllo.errori and not controllo.non_letti and not controllo.novita)
    finally:
        ue.REGISTRO, controllo.SPARQL_UE, controllo.ARCHIVIO_UE = veri
        for elenco in (controllo.errori, controllo.non_letti, controllo.novita, *controllo.disciplinari.values()):
            elenco.clear()
        controllo.metodi.clear()
        controllo.confronti.clear()


def prove_dei_disciplinari(controllo, base):
    """Disciplinari nuovi, tolti e aggiornati (Alessandro, 25/11/2026: si controlla sempre): il peso dei file, le
    pagine del Ministero, e il riepilogo che il rapporto porta in ogni giro fatto con la rete."""
    def pulisci():
        for elenco in (controllo.errori, controllo.non_letti, controllo.novita, controllo.protetti, controllo.da_rivedere,
                       controllo.muti, *controllo.disciplinari.values()):
            elenco.clear()
        for insieme in (controllo.metodi, controllo.di_fila, controllo.motivo, controllo.letti, controllo.pesi, controllo.confronti):
            insieme.clear()

    def fra_i_disciplinari():
        return tuple(len(controllo.disciplinari[k]) for k in ("nuovi", "tolti", "aggiornati"))

    # il peso che il sito dichiara: il totale di una risposta parziale, la lunghezza di una intera
    casi = [((206, {"content-range": "bytes 0-7/185003", "content-length": "8"}), 185003),
            ((200, {"content-length": "4009"}), 4009),
            ((200, {"content-length": "4009", "content-encoding": "gzip"}), None),
            ((206, {"content-range": "bytes 0-7/*"}), None),
            ((206, {"content-length": "8"}), None),
            ((200, {}), None)]
    sbagliati = [(caso, controllo.peso_del_file(*caso), atteso) for caso, atteso in casi if controllo.peso_del_file(*caso) != atteso]
    esito("peso di un file: totale di Content-Range nelle risposte parziali, Content-Length in quelle intere, nulla se il sito non lo dice",
          not sbagliati, sbagliati)
    esito("data di un file: il giorno di Last-Modified, vuoto se manca o non si legge",
          controllo.data_del_file({"last-modified": "Wed, 12 Dec 2012 07:52:23 GMT"}) == "2012-12-12"
          and controllo.data_del_file({}) == "" and controllo.data_del_file({"last-modified": "ieri"}) == "")

    # file del catalogo: il server finto dichiara 4009 byte per /vero.pdf
    vero = len(RISPOSTE["/vero.pdf"][2])
    pulisci()
    uguale = {"voci": [{"nome": "Uguale", "formato": "pdf", "url": base + "/vero.pdf?a", "byte": vero,
                        "extra": [{"etichetta": "Modifica temporanea", "url": base + "/vero.pdf?b", "byte": vero}]},
                       {"nome": "Solo Word", "formato": "docx", "url": base + "/qualsiasi.pdf"}]}
    controllo.controlla_file_del_catalogo(uguale)
    controllo.confronta_pesi(uguale)
    esito("file del catalogo con lo stesso peso dei dati: nessuna novità, e il giro dice quanti ne ha confrontati",
          not controllo.novita and not controllo.errori and fra_i_disciplinari() == (0, 0, 0) and controllo.confronti.get("file") == [2, 2],
          f"{controllo.novita} {controllo.confronti}")
    pulisci()
    cambiato = {"voci": [{"nome": "Cambiato", "formato": "pdf", "url": base + "/vero.pdf?a", "byte": vero - 9},
                         {"nome": "Uguale", "formato": "pdf", "url": base + "/vero.pdf?b", "byte": vero,
                          "extra": [{"etichetta": "Modifica temporanea", "url": base + "/vero.pdf?c", "byte": vero + 1}]}]}
    controllo.controlla_file_del_catalogo(cambiato)
    controllo.confronta_pesi(cambiato)
    testo = " | ".join(controllo.novita)
    esito("file aggiornato allo stesso indirizzo (peso diverso dai dati): novità fra i disciplinari aggiornati, con i due pesi",
          len(controllo.novita) == 2 and fra_i_disciplinari() == (0, 0, 2) and not controllo.errori
          and f"«Cambiato»: il file allo stesso indirizzo è cambiato: nei dati pesa {vero - 9} byte, ora {vero}" in testo
          and "«Uguale», Modifica temporanea" in testo and controllo.letti == {base + "/vero.pdf?a", base + "/vero.pdf?b", base + "/vero.pdf?c"},
          f"{fra_i_disciplinari()} {testo}")
    pulisci()
    sparito = {"voci": [{"nome": "Sparito", "formato": "pdf", "url": base + "/manca.pdf", "byte": 100},
                        {"nome": "Non letto", "formato": "pdf", "url": base + "/rifiuto.pdf", "byte": 100},
                        {"nome": "Senza peso nei dati", "formato": "pdf", "url": base + "/vero.pdf?d"}]}
    controllo.controlla_file_del_catalogo(sparito)
    controllo.confronta_pesi(sparito)
    esito("file del catalogo che risponde 404: collegamento rotto e disciplinare tolto; ciò che non si legge o non ha il peso nei dati non si confronta",
          len(controllo.errori) == 1 and fra_i_disciplinari() == (0, 1, 0) and not controllo.novita and controllo.confronti.get("file") == [0, 3],
          f"{controllo.errori} {controllo.novita} {controllo.confronti}")

    # il peso passa davvero dalle intestazioni della risposta ai dati del giro: risposta parziale (206), come il
    # sito del Ministero, e pagina al posto del PDF alla prima richiesta, con il file intero alla seconda
    pulisci()
    veri = {"voci": [{"nome": "Parziale", "formato": "pdf", "url": base + "/parziale.pdf", "byte": vero},
                     {"nome": "Due richieste", "formato": "pdf", "url": base + "/pagina-poi-pdf.pdf", "byte": vero}]}
    controllo.controlla_file_del_catalogo(veri)
    controllo.confronta_pesi(veri)
    esito("peso da una risposta parziale vera (206 con Content-Range): il totale del file, con il giorno che il sito dichiara",
          controllo.pesi.get(base + "/parziale.pdf") == (vero, "2012-12-12"), controllo.pesi)
    esito("peso dopo una pagina al posto del PDF: vale la risposta con il PDF, non quella con la pagina",
          controllo.pesi.get(base + "/pagina-poi-pdf.pdf", (0,))[0] == vero and len(RISPOSTE["/qualsiasi.pdf"][2]) != vero
          and not controllo.novita and controllo.confronti.get("file") == [2, 2], f"{controllo.pesi} {controllo.novita}")

    # un file che la richiesta semplice non legge e il browser sì: il peso è quello del file ricevuto dal browser
    def col_browser(risposte, catalogo_finto):
        pulisci()
        for voce in catalogo_finto["voci"]:
            controllo.da_rivedere.append((f"disciplinare «{voce['nome']}»", voce["url"], "TimeoutError: timed out"))
        vero_playwright = sys.modules.get("playwright.sync_api", "assente")
        sys.modules["playwright.sync_api"] = types.SimpleNamespace(sync_playwright=lambda: BrowserConPagina(risposte))
        try:
            controllo.chiudi_da_rivedere(True)
        finally:
            if vero_playwright == "assente":
                sys.modules.pop("playwright.sync_api", None)
            else:
                sys.modules["playwright.sync_api"] = vero_playwright
        controllo.confronta_pesi(catalogo_finto)

    pdf = b"%PDF-1.7\n" + b"x" * 100
    col_browser([(200, pdf)], {"voci": [{"nome": "Dal browser", "formato": "pdf", "url": "https://www.esempio.it/a.pdf", "byte": len(pdf) + 7}]})
    esito("file letto dal browser e aggiornato allo stesso indirizzo: il peso è quello del file ricevuto, ed è una novità",
          fra_i_disciplinari() == (0, 0, 1) and f"nei dati pesa {len(pdf) + 7} byte, ora {len(pdf)}" in " ".join(controllo.novita)
          and controllo.confronti.get("file") == [1, 1], f"{controllo.novita} {controllo.confronti}")
    col_browser([(404, b"")], {"voci": [{"nome": "Sparito al browser", "formato": "pdf", "url": "https://www.esempio.it/b.pdf", "byte": 10}]})
    esito("file del catalogo che risponde 404 al browser: collegamento rotto e disciplinare tolto",
          len(controllo.errori) == 1 and fra_i_disciplinari() == (0, 1, 0), f"{controllo.errori} {fra_i_disciplinari()}")

    # pagine del Ministero: allegati nuovi, allegati spariti, elenco ufficiale cambiato
    def allegato(pagina, nome):
        return f"https://www.masaf.gov.it/flex/cm/pages/ServeAttachment.php/L/IT/D/{nome}/P/BLOB%3AID%3D{pagina}/E/pdf?mode=download"

    catalogo = {"classi": [{"id": "formaggi", "pagina": "https://www.masaf.gov.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/100"}],
                "elenco_ufficiale": {"allegato": allegato(200, "elenco"), "aggiornato": "2026-10-15"},
                "allegati_noti": [{"url": allegato(100, "decreto"), "motivo": "decreto di riconoscimento del consorzio"}],
                "voci": [{"nome": "Formaggio Alfa", "formato": "pdf", "url": allegato(100, "alfa")},
                         {"nome": "Formaggio Beta", "formato": "pdf", "url": allegato(100, "beta"),
                          "extra": [{"etichetta": "Modifica temporanea", "url": allegato(8079, "beta-temporanea")}]}]}
    del_ministero = {"gruppi": [{"documenti": [{"id": "elenco-pat", "url": allegato(300, "pat")}]}]}
    intatte = {"100": {allegato(100, "alfa"): "Alfa", allegato(100, "beta"): "Beta", allegato(100, "decreto"): "Decreto"},
               "200": {allegato(200, "elenco"): "Elenco"}, "300": {allegato(300, "pat"): "Elenco PAT"},
               "8079": {allegato(8079, "beta-temporanea"): "Beta, modifica temporanea"}}
    vera = controllo.allegati_della_pagina

    def ministero(nome, pagine, atteso, *pezzi):
        """`atteso`: rotti, novità, (nuovi, tolti, aggiornati), pagine lette."""
        pulisci()
        controllo.allegati_della_pagina = pagine.get
        try:
            controllo.controlla_ministero(del_ministero, catalogo)
        finally:
            controllo.allegati_della_pagina = vera
        visto = (len(controllo.errori), len(controllo.novita), fra_i_disciplinari(), controllo.confronti.get("pagine"))
        testo = " | ".join(controllo.errori + controllo.novita)
        esito(nome, visto == atteso and all(pezzo in testo for pezzo in pezzi), f"{visto}, atteso {atteso}; {testo[:300]}")

    ministero("Ministero: pagine uguali ai dati, nessun rilievo e quattro pagine lette su quattro", intatte, (0, 0, (0, 0, 0), [4, 4]))
    ministero("Ministero: un allegato nuovo nella pagina di una classe è una novità, fra i disciplinari nuovi",
              dict(intatte, **{"100": dict(intatte["100"], **{allegato(100, "gamma"): "Formaggio Gamma"})}),
              (0, 1, (1, 0, 0), [4, 4]), "allegato nuovo «Formaggio Gamma»")
    ministero("Ministero: un disciplinare sparito dagli allegati è un collegamento rotto, fra i disciplinari tolti",
              dict(intatte, **{"100": {u: n for u, n in intatte["100"].items() if u != allegato(100, "beta")}}),
              (1, 0, (0, 1, 0), [4, 4]), "«Formaggio Beta»: il file non è più fra gli allegati")
    ministero("Ministero: un disciplinare sostituito (file sparito e allegato nuovo) compare fra i tolti e fra i nuovi",
              dict(intatte, **{"100": {allegato(100, "alfa"): "Alfa", allegato(100, "decreto"): "Decreto", allegato(100, "beta-2"): "Beta 2026"}}),
              (1, 1, (1, 1, 0), [4, 4]), "«Formaggio Beta»", "allegato nuovo «Beta 2026»")
    ministero("Ministero: un documento sparito dalla sua pagina è un collegamento rotto, ma non è un disciplinare tolto",
              dict(intatte, **{"300": {allegato(300, "altro"): "Altro"}}), (1, 0, (0, 0, 0), [4, 4]), "documento «elenco-pat»")
    ministero("Ministero: un allegato nuovo nella pagina delle modifiche temporanee è una novità, fra i disciplinari aggiornati",
              dict(intatte, **{"8079": dict(intatte["8079"], **{allegato(8079, "alfa-temporanea"): "Alfa, modifica temporanea"})}),
              (0, 1, (0, 0, 1), [4, 4]), "allegato nuovo «Alfa, modifica temporanea»")
    ministero("Ministero: l'elenco ufficiale cambiato è una novità, fra i disciplinari nuovi",
              dict(intatte, **{"200": {allegato(200, "elenco-nuovo"): "Elenco"}}), (0, 1, (1, 0, 0), [4, 4]), "ha cambiato l'elenco")
    ministero("Ministero: una pagina che non si legge non conta fra quelle confrontate",
              {k: v for k, v in intatte.items() if k != "8079"}, (0, 0, (0, 0, 0), [3, 4]))

    # il rapporto: la riga dei disciplinari c'è sempre con la rete, la sezione solo se c'è qualcosa
    documenti_veri, catalogo_vero = controllo.carica()
    pulisci()
    interi = {"registro": 335, "archivio": True, "pagine": [26, 26], "file": [336, 336]}

    def riga(anche_file=True, **cambiati):
        """La riga dei disciplinari del rapporto, con i confronti del giro cambiati come dice la prova."""
        controllo.confronti.clear()
        controllo.confronti.update({k: v for k, v in dict(interi, **cambiati).items() if v is not None})
        testo = controllo.rapporto(documenti_veri, catalogo_vero, True, anche_file)
        return next(r for r in testo.splitlines() if r.startswith("Disciplinari nuovi:")), testo

    quale, testo = riga()
    esito("rapporto: senza novità e con i confronti interi dice «nuovi: nessuno, tolti: nessuno, aggiornati: nessuno» e che cosa ha confrontato",
          quale.startswith("Disciplinari nuovi: nessuno. Tolti: nessuno. Aggiornati: nessuno.") and "335 prodotti italiani registrati" in quale
          and "peso di 336 file del Ministero su 336" in quale and "### Disciplinari nuovi" not in testo and "Nessun problema." in testo,
          testo[:500])
    quale, _ = riga(registro=None)
    esito("rapporto: con il registro non letto nessuna delle tre voci dice «nessuno»",
          "nessuno" not in quale and quale.count("registro europeo non letto") == 3, quale)
    quale, _ = riga(pagine=[24, 26])
    esito("rapporto: con due pagine del Ministero non lette, nuovi e tolti non dicono «nessuno»; gli aggiornati sì",
          quale.startswith("Disciplinari nuovi: confronto incompleto (2 pagine del Ministero su 26 non lette). Tolti: confronto incompleto (")
          and "Aggiornati: nessuno." in quale, quale)
    quale, _ = riga(archivio=False)
    esito("rapporto: con l'archivio dell'UE non letto per intero, gli aggiornati non dicono «nessuno»",
          "Disciplinari nuovi: nessuno. Tolti: nessuno. Aggiornati: confronto incompleto (archivio dell'UE non letto per intero)." in quale, quale)
    quale, _ = riga(file=[300, 336])
    esito("rapporto: con una parte dei file non pesata, gli aggiornati non dicono «nessuno»",
          "Aggiornati: confronto incompleto (peso confrontato per 300 file su 336)." in quale and "Tolti: nessuno." in quale, quale)
    quale, _ = riga(anche_file=False)
    esito("rapporto: in un giro senza --file gli aggiornati dicono che il peso non è stato confrontato, anche se un giro precedente lo aveva fatto",
          "Aggiornati: confronto incompleto (peso dei file non confrontato: giro senza --file)." in quale and "peso di 336 file" not in quale, quale)
    testo = controllo.rapporto(documenti_veri, catalogo_vero, False, False)
    esito("rapporto: senza rete la riga dei disciplinari non c'è (nessun confronto fatto)", "Disciplinari nuovi" not in testo, testo[:300])
    pulisci()
    righe = {"nuovi": "prodotto nuovo nel registro europeo: «Pane Delta»", "tolti": "disciplinare «Olio Gamma»: tolto",
             "aggiornati": "disciplinare «Formaggio Alfa»: il file allo stesso indirizzo è cambiato"}
    for chiave, riga in righe.items():
        controllo.disciplinari[chiave].append(riga)
    controllo.errori.append(righe["tolti"])
    controllo.novita.extend([righe["nuovi"], righe["aggiornati"], "documento «prova»: è uscita una versione consolidata più recente"])
    testo = controllo.rapporto(documenti_veri, catalogo_vero, True, True)
    sezione = testo.split("### Disciplinari nuovi, tolti o aggiornati", 1)[-1].split("### ", 1)[0]
    altre = testo.split("### Novità sulle fonti, da valutare", 1)[-1]
    esito("rapporto: i disciplinari nuovi, tolti e aggiornati hanno la loro sezione, con come si lavorano",
          "Disciplinari nuovi: 1, con il confronto incompleto (" in testo and all(voce in sezione for voce in righe.values())
          and "Nuovi (" in sezione and "Tolti (" in sezione and "Aggiornati (" in sezione and "Come si lavorano" in sezione, testo[:700])
    esito("rapporto: le righe dei disciplinari non si ripetono fra le altre novità, che restano nella loro sezione",
          "versione consolidata più recente" in altre and righe["nuovi"] not in altre and righe["aggiornati"] not in altre
          and testo.count(righe["nuovi"]) == 1, altre[:400])
    # lo stesso disciplinare con tre righe (sparito dagli allegati, 404, tolto dal registro) è un disciplinare solo
    pulisci()
    controllo.confronti.update(interi)
    for coda in (": il file non è più fra gli allegati", ": HTTP 404", ": nel registro europeo non è più fra i prodotti registrati"):
        controllo.disciplinari["tolti"].append("disciplinare «Olio Gamma»" + coda)
    controllo.disciplinari["tolti"].append("disciplinare «Salame Beta»: HTTP 404")
    controllo.errori.extend(controllo.disciplinari["tolti"])
    testo = controllo.rapporto(documenti_veri, catalogo_vero, True, True)
    esito("rapporto: il conto dei tolti è per disciplinare, non per riga (tre righe sullo stesso prodotto contano uno)",
          "Disciplinari nuovi: nessuno. Tolti: 2. Aggiornati: nessuno." in testo, testo[:400])
    pulisci()


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
        esito("dei cinque indirizzi chiesti, solo il PDF letto è segnato per le letture annotate",
              controllo.letti == {base + "/vero.pdf"}, controllo.letti)

        for elenco in (controllo.errori, controllo.non_letti, controllo.protetti, controllo.da_rivedere, controllo.muti):
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
        for elenco in (controllo.errori, controllo.non_letti, controllo.protetti, controllo.da_rivedere, controllo.muti):
            elenco.clear()
        finto = {"voci": [{"nome": f"Prodotto {n}", "formato": "pdf", "url": f"{base}/verifica.pdf?n={n}"} for n in range(12)]}
        controllo.controlla_file_del_catalogo(finto)
        controllo.chiudi_da_rivedere(False)
        esito("catalogo tutto dietro la verifica: dodici «non controllati», nessuna fonte non letta",
              len(controllo.protetti) == 12 and not controllo.non_letti and not controllo.errori,
              f"protetti {len(controllo.protetti)}, non letti {len(controllo.non_letti)}")
        for elenco in (controllo.errori, controllo.non_letti, controllo.protetti, controllo.da_rivedere, controllo.muti):
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
        esito("catalogo misto: i tre PDF letti sono segnati per le letture annotate, il 404 e il file Word no",
              controllo.letti == {base + "/vero.pdf", base + "/vero.pdf?b", base + "/vero.pdf?c"}, controllo.letti)
        # un sito che non risponde: tempo scaduto o errore del server. Regola guasti, punto 3: non è un collegamento
        # rotto e non rende rosso il controllo, ma resta nel rapporto e la data di verifica non si aggiorna
        def pulisci():
            for elenco in (controllo.errori, controllo.non_letti, controllo.protetti, controllo.da_rivedere, controllo.muti):
                elenco.clear()
            controllo.metodi.clear()
            controllo.di_fila.clear()
            controllo.motivo.clear()
            controllo.letti.clear()

        pulisci()
        attesa_vera, controllo.TEMPO_MASSIMO = controllo.TEMPO_MASSIMO, 0.3
        try:
            controllo.controlla_pdf("documento «lento»", base + "/lento.pdf")
        finally:
            controllo.TEMPO_MASSIMO = attesa_vera
        controllo.controlla_pdf("documento «guasto»", base + "/guasto.pdf")
        controllo.controlla_pdf("documento «negato»", base + "/negato.pdf")
        controllo.chiudi_da_rivedere(False)
        documenti, catalogo = controllo.carica()
        testo = controllo.rapporto(documenti, catalogo, True, False)
        esito("tempo scaduto ed errore del server (5xx): «non controllati», né rotti né fonti non lette",
              len(controllo.muti) == 2 and any("/lento.pdf" in m and "timed out" in m for m in controllo.muti)
              and any("/guasto.pdf" in m and "HTTP 500" in m for m in controllo.muti) and not controllo.errori,
              f"muti {controllo.muti}, rotti {controllo.errori}")
        esito("un 400 resta una fonte non letta", len(controllo.non_letti) == 1 and "/negato.pdf" in controllo.non_letti[0][1],
              controllo.non_letti)
        esito("il rapporto ha la sezione dei siti che non hanno risposto e non dice «Nessun problema»",
              "### Collegamenti non controllati: il sito non ha risposto" in testo and "Nessun problema." not in testo
              and "/lento.pdf" in testo, testo[:300])
        pulisci()
        for n in range(controllo.SOGLIA_FERMO + 2):
            controllo.controlla_pdf(f"documento «guasto {n}»", base + f"/guasto.pdf?n={n}")
        controllo.chiudi_da_rivedere(False)
        esito("un sito tutto muto: anche i file saltati restano «non controllati», non fonti non lette",
              len(controllo.muti) == controllo.SOGLIA_FERMO + 2 and not controllo.non_letti and not controllo.errori,
              f"muti {len(controllo.muti)}, non letti {len(controllo.non_letti)}")
        controllo.segnala_controllo_mancato(400)
        pochi_su_molti = not controllo.non_letti
        controllo.segnala_controllo_mancato(20)
        esito("troppi collegamenti senza controllo (più di SOGLIA_FERMO e più di un quinto): il giro non vale, è una fonte non letta",
              pochi_su_molti and len(controllo.non_letti) == 1
              and f"{controllo.SOGLIA_FERMO + 2} collegamenti su 20 non controllati" in controllo.non_letti[0][1]
              and controllo.non_letti[0][0].startswith("127.0.0.1"), f"{pochi_su_molti} {controllo.non_letti}")
        pulisci()
        controllo.protetti.extend(f"documento «{n}»: {controllo.ANTIBOT}: https://www.esempio.it/{n}.pdf"
                                  for n in range(controllo.SOGLIA_FERMO))
        controllo.segnala_controllo_mancato(controllo.SOGLIA_FERMO)
        esito("pochi collegamenti dietro una verifica anti-bot (fino a SOGLIA_FERMO) non fermano il giro, anche se sono tutti",
              not controllo.non_letti, controllo.non_letti)
        tre = {"gruppi": [{"documenti": [{"id": "a", "url": "https://www.esempio.it/a.pdf", "pagina": {"url": "https://www.esempio.it/a"}},
                                         {"id": "b", "url": "https://www.esempio.it/b.pdf",
                                          "pagina": {"url": "https://" + controllo.MASAF + "/pagina"}},
                                         {"id": "c", "url": "https://www.esempio.it/c.pdf"}]}]}
        esito("i collegamenti da aprire: documenti, pagine degli enti (non quelle del Ministero) e, con --file, i PDF del catalogo",
              controllo.collegamenti_da_aprire(tre, misto, False) == 4 and controllo.collegamenti_da_aprire(tre, misto, True) == 8,
              f"{controllo.collegamenti_da_aprire(tre, misto, False)} e {controllo.collegamenti_da_aprire(tre, misto, True)}")
        pulisci()
        senza_rete = controllo.rapporto(documenti, catalogo, False, False, rete_saltata=True)
        esito("il rapporto dice quando i siti non sono stati interrogati per colpa dei dati",
              "Le richieste ai siti non sono state fatte" in senza_rete and "Controllo fatto: dati." in senza_rete
              and "Le richieste ai siti non sono state fatte" not in controllo.rapporto(documenti, catalogo, True, False))
        pulisci()
        controllo.controlla_file_del_catalogo({"voci": [{"nome": f"Prodotto {n}", "formato": "pdf", "url": f"{base}/guasto.pdf?n={n}"}
                                                       for n in range(12)]})
        controllo.chiudi_da_rivedere(False)
        esito("catalogo su un sito muto: dodici «non controllati», nessuna fonte non letta",
              len(controllo.muti) == 12 and not controllo.non_letti and not controllo.errori,
              f"muti {len(controllo.muti)}, non letti {len(controllo.non_letti)}")

        # un sito che chiude la connessione senza rispondere (lo fa chi filtra gli indirizzi dei centri di calcolo):
        # il 25/11/2026 il sito dell'IZS lo ha fatto con i server di GitHub, e il giro è finito rosso per un documento
        pulisci()
        controllo.controlla_pdf("documento «chiude»", base + "/chiude.pdf")
        controllo.chiudi_da_rivedere(False)
        esito("un sito che chiude la connessione senza rispondere: «non controllato», né rotto né fonte non letta",
              len(controllo.muti) == 1 and "/chiude.pdf" in controllo.muti[0] and not controllo.non_letti and not controllo.errori,
              f"muti {controllo.muti}, non letti {controllo.non_letti}")

        pulisci()
        vero = sys.modules.get("playwright.sync_api", "assente")
        sys.modules["playwright.sync_api"] = types.SimpleNamespace(sync_playwright=BrowserCheCade)
        try:
            controllo.controlla_pdf("documento «chiude»", base + "/chiude.pdf")
            controllo.chiudi_da_rivedere(True)
        finally:
            if vero == "assente":
                sys.modules.pop("playwright.sync_api", None)
            else:
                sys.modules["playwright.sync_api"] = vero
        testo = controllo.rapporto(documenti, catalogo, True, False)
        esito("connessione chiusa alla richiesta semplice e al browser: «non controllato», con l'errore del browser su una riga",
              len(controllo.muti) == 1 and "socket hang up" in controllo.muti[0] and "\n" not in controllo.muti[0]
              and "Call log" not in testo and not controllo.non_letti and not controllo.senza_browser,
              f"muti {controllo.muti}, non letti {controllo.non_letti}, {controllo.senza_browser}")
        esito("il rapporto dice come si completa il controllo da un'altra rete",
              "### Collegamenti non controllati: il sito non ha risposto" in testo
              and "--rete --browser --aggiorna-data" in testo and controllo.FILE_LETTURE.name in testo, testo[-700:])

        # richiesta semplice e browser insieme: conta la risposta avuta, non il silenzio dell'altra
        pulisci()
        caduta = "Error: APIRequestContext.get: socket hang up"
        scaduto = "TimeoutError: timed out"
        casi = {"a": (scaduto, ("no", caduta)),                       # silenzio e silenzio: non controllato
                "b": (controllo.ALTRO, ("no", caduta)),               # una pagina al posto del PDF: fonte non letta
                "c": (scaduto, ("no", "anche il browser non ottiene un PDF (HTTP 200)")),
                "d": ("URLError: <urlopen error [Errno -2] Name or service not known>",
                      ("no", "Error: APIRequestContext.get: getaddrinfo ENOTFOUND www.esempio.it")),
                "e": ("ConnectionResetError: [Errno 104] Connection reset by peer", None),  # il browser non ha provato
                "f": (scaduto, ("no", controllo.ANTIBOT)),            # verifica anti-bot vista dal browser
                "g": ("SSLCertVerificationError: certificate has expired", ("no", caduta)),
                "h": (scaduto, ("pdf", "")),                          # il browser legge il PDF
                "i": (controllo.FUORI_TEMPO, ("no", "anche il browser non ottiene un PDF (HTTP 200)")),
                "j": (controllo.SALTATO, None),                       # saltato, e il browser non ha provato
                "k": (scaduto, ("no", "Error: APIRequestContext.get: connect ETIMEDOUT 192.0.2.1:443"))}
        controllo.da_rivedere.extend((f"documento «{nome}»", f"https://www.esempio.it/{nome}.pdf", nota)
                                     for nome, (nota, _) in casi.items())
        vera = controllo.riprova_con_browser
        controllo.riprova_con_browser = lambda voci: {f"https://www.esempio.it/{nome}.pdf": del_browser
                                                      for nome, (_, del_browser) in casi.items() if del_browser}
        try:
            controllo.chiudi_da_rivedere(True)
        finally:
            controllo.riprova_con_browser = vera
        fonti = {testo.split("»")[0][-1]: testo for _, testo in controllo.non_letti}
        esito("silenzio alla richiesta semplice e al browser (tempo scaduto, connessione chiusa): «non controllato»",
              sorted(m.split("»")[0][-1] for m in controllo.muti) == ["a", "e", "j", "k"]
              and "socket hang up" in next(m for m in controllo.muti if "«a»" in m), controllo.muti)
        esito("una risposta che non è il PDF conta più del silenzio dell'altra richiesta: fonte non letta",
              sorted(fonti) == ["b", "c", "d", "g", "i"] and controllo.ALTRO in fonti["b"] and "HTTP 200" in fonti["c"]
              and "HTTP 200" in fonti["i"],
              controllo.non_letti)
        esito("nome che non si risolve e certificato scaduto restano fonti non lette, con il loro motivo",
              "ENOTFOUND" in fonti.get("d", "") and "certificate has expired" in fonti.get("g", ""), controllo.non_letti)
        esito("verifica anti-bot vista dal browser dopo un tempo scaduto: né rotto né controllato",
              len(controllo.protetti) == 1 and "«f»" in controllo.protetti[0] and controllo.ANTIBOT in controllo.protetti[0],
              controllo.protetti)
        esito("il PDF letto dal browser è segnato per le letture annotate, e solo quello",
              controllo.letti == {"https://www.esempio.it/h.pdf"} and controllo.metodi["browser"] == 1, controllo.letti)

        # pagine degli enti accanto ai documenti: lette, dietro una verifica, senza risposta
        pulisci()
        vere = (controllo.controlla_ministero, controllo.controlla_europa)
        controllo.controlla_ministero = controllo.controlla_europa = lambda *argomenti: None
        try:
            controllo.controlla_rete({"gruppi": [{"documenti": [
                {"id": "x", "url": base + "/vero.pdf?x", "pagina": {"url": base + "/qualsiasi.pdf?pagina"}},
                {"id": "y", "url": base + "/vero.pdf?y", "pagina": {"url": base + "/verifica.pdf?pagina"}},
                {"id": "z", "url": base + "/vero.pdf?z", "pagina": {"url": base + "/chiude.pdf?pagina"}}]}]}, {"voci": []}, False)
        finally:
            controllo.controlla_ministero, controllo.controlla_europa = vere
        esito("pagine degli enti: quella che risponde è segnata per le letture; verifica anti-bot e connessione chiusa restano «non controllate»",
              controllo.letti == {base + "/vero.pdf?x", base + "/vero.pdf?y", base + "/vero.pdf?z", base + "/qualsiasi.pdf?pagina"}
              and len(controllo.protetti) == 1 and len(controllo.muti) == 1 and "/chiude.pdf?pagina" in controllo.muti[0]
              and not controllo.non_letti and not controllo.errori,
              f"letti {controllo.letti}, protetti {controllo.protetti}, muti {controllo.muti}, non letti {controllo.non_letti}")
        # i messaggi d'errore veri di urllib e di Playwright, uno per uno
        silenzi = ["TimeoutError: timed out", "URLError: <urlopen error timed out>", "HTTP 503",
                   "URLError: <urlopen error [Errno 104] Connection reset by peer>", "ConnectionResetError: [Errno 104] Connection reset by peer",
                   "RemoteDisconnected: Remote end closed connection without response", "URLError: <urlopen error [Errno 111] Connection refused>",
                   "URLError: <urlopen error [Errno 110] Connection timed out>", "URLError: <urlopen error [Errno 113] No route to host>",
                   "URLError: <urlopen error [Errno 101] Network is unreachable>", "BrokenPipeError: [Errno 32] Broken pipe",
                   "IncompleteRead: IncompleteRead(0 bytes read, 8 more expected)",
                   "SSLEOFError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1000)",
                   "Error: APIRequestContext.get: socket hang up", "Error: APIRequestContext.get: read ECONNRESET",
                   "Error: APIRequestContext.get: connect ECONNREFUSED 192.0.2.1:443", "Error: APIRequestContext.get: connect ETIMEDOUT 192.0.2.1:443",
                   "Error: APIRequestContext.get: connect EHOSTUNREACH 192.0.2.1:443", "Error: APIRequestContext.get: write EPIPE",
                   "Error: APIRequestContext.get: Client network socket disconnected before secure TLS connection was established",
                   "Error: Page.goto: net::ERR_CONNECTION_RESET at https://www.esempio.it/a.pdf",
                   "TimeoutError: APIRequestContext.get: Timeout 30000ms exceeded.", "anche il browser non ottiene un PDF (HTTP 502)",
                   controllo.SALTATO, controllo.FUORI_TEMPO]
        altro = ["HTTP 400", "HTTP 401", "HTTP 301", controllo.ALTRO, "anche il browser non ottiene un PDF (HTTP 200)", "EUR-Lex",
                 controllo.ANTIBOT, f"{controllo.RIFIUTO} (HTTP 403)",
                 "URLError: <urlopen error [Errno -2] Name or service not known>",
                 "URLError: <urlopen error [Errno -3] Temporary failure in name resolution>",
                 "SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: certificate has expired (_ssl.c:1000)",
                 "URLError: <urlopen error Tunnel connection failed: 403 Forbidden>",
                 "URLError: <urlopen error Tunnel connection failed: 503 Service Unavailable>",
                 "Error: APIRequestContext.get: getaddrinfo ENOTFOUND www.esempio.it",
                 "Error: Page.goto: net::ERR_NAME_NOT_RESOLVED at https://www.esempio.it/a.pdf",
                 "Error: Page.goto: net::ERR_CERT_DATE_INVALID at https://www.esempio.it/a.pdf",
                 "Error: Page.goto: net::ERR_ABORTED at https://www.esempio.it/a.pdf"]
        esito("tempo scaduto, errore del server, connessione chiusa, rifiutata o non raggiungibile: «il sito non ha risposto»",
              all(controllo.SILENZIO.search(s) for s in silenzi), [s for s in silenzi if not controllo.SILENZIO.search(s)])
        esito("nome che non si risolve, certificato, rifiuti e risposte diverse dal PDF non sono «il sito non ha risposto»",
              not any(controllo.SILENZIO.search(s) for s in altro), [s for s in altro if controllo.SILENZIO.search(s)])

        vera = controllo.urllib.request.urlopen

        def su_due_righe(*argomenti, **parole):
            raise OSError("prima riga\nseconda riga")
        controllo.urllib.request.urlopen = su_due_righe
        try:
            stato, _, errore = controllo.chiedi("https://www.esempio.it/a.pdf")
        finally:
            controllo.urllib.request.urlopen = vera
        esito("un errore di rete scritto su più righe entra nel rapporto su una riga sola",
              stato == 0 and errore == "OSError: prima riga seconda riga", f"{stato} {errore!r}")

        # il browser di riserva con una pagina vera: la visita che sblocca il PDF, il rifiuto, la pagina al posto del PDF
        def con_la_pagina(nota, finto):
            pulisci()
            controllo.da_rivedere.append(("documento «prova»", "https://www.esempio.it/prova.pdf", nota))
            vero = sys.modules.get("playwright.sync_api", "assente")
            sys.modules["playwright.sync_api"] = types.SimpleNamespace(sync_playwright=lambda: finto)
            try:
                controllo.chiudi_da_rivedere(True)
            finally:
                if vero == "assente":
                    sys.modules.pop("playwright.sync_api", None)
                else:
                    sys.modules["playwright.sync_api"] = vero
            return (len(controllo.errori), len(controllo.non_letti), len(controllo.protetti), len(controllo.muti),
                    controllo.metodi["browser"], len(controllo.letti))

        pdf = b"%PDF-1.7\n" + b"x" * 100
        interrotta = "Page.goto: net::ERR_ABORTED at https://www.esempio.it/prova.pdf\nCall log:\n  - navigating"
        visto = con_la_pagina(controllo.ANTIBOT, BrowserConPagina([(200, VERIFICA), (200, pdf)], inciampo=interrotta))
        esito("browser: la visita della pagina sblocca il PDF anche se la navigazione si interrompe per lo scaricamento",
              visto == (0, 0, 0, 0, 1, 1), f"rotti, non letti, protetti, muti, letti dal browser, segnati: {visto}")
        visto = con_la_pagina("TimeoutError: timed out", BrowserConPagina([(403, b"Forbidden")], inciampo=interrotta))
        esito("browser: un rifiuto (403) dopo una navigazione interrotta resta «né rotto né controllato», non una fonte non letta",
              visto == (0, 0, 1, 0, 0, 0) and controllo.RIFIUTO in controllo.protetti[0], f"{visto} {controllo.protetti} {controllo.non_letti}")
        visto = con_la_pagina("TimeoutError: timed out", BrowserConPagina([(200, QUALSIASI)]))
        esito("browser: una pagina qualsiasi al posto del PDF è una fonte non letta",
              visto == (0, 1, 0, 0, 0, 0) and "HTTP 200" in controllo.non_letti[0][1], f"{visto} {controllo.non_letti}")
        visto = con_la_pagina("TimeoutError: timed out", BrowserConPagina([(200, QUALSIASI)], titolo="Just a moment..."))
        esito("browser: una pagina di verifica riconosciuta dal titolo è «né rotto né controllato»",
              visto == (0, 0, 1, 0, 0, 0) and controllo.ANTIBOT in controllo.protetti[0], f"{visto} {controllo.protetti}")
        visto = con_la_pagina("TimeoutError: timed out", BrowserConPagina([(200, QUALSIASI), (404, b"")]))
        esito("browser: un 404 dopo la visita della pagina è un collegamento rotto",
              visto == (1, 0, 0, 0, 0, 0), f"{visto} {controllo.errori}")
        pulisci()
        prove_del_browser(controllo, base)
        prove_delle_letture(controllo)
        prove_delle_sintesi(controllo, base)
        prove_dei_disciplinari(controllo, base)
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
        for nome in (SCRIPT, SCRIPT_SINTESI):
            shutil.copy(RADICE / "scripts" / nome, base / "scripts" / nome)
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
        prova(base, "con i dati sbagliati i siti non si interrogano, e il rapporto lo dice (--rete)",
              nei_documenti(uno, uno.replace("https://", "http://")), "Le richieste ai siti non sono state fatte", "--rete")
        prova(base, "documento Word al posto del PDF", nei_documenti(uno, uno[:-4] + ".docx"), "non finisce con .pdf")
        prova(base, "parentesi nell'indirizzo", nei_documenti(uno, uno[:-4] + "(1).pdf"), "parentesi nell'indirizzo")
        prova(base, "disciplinare in PDF con un allegato Word", nel_catalogo(word_al_posto_del_pdf),
              "l'allegato del Ministero non è un PDF")
        prova(base, "allegato di un'altra pagina del Ministero", nel_catalogo(altra_pagina),
              "non è della pagina del Ministero della sua classe")
        prova(base, "stesso indirizzo su due disciplinari", nel_catalogo(doppione), "indirizzo già usato da un'altra voce")

        # il peso in byte: serve a riconoscere un file aggiornato senza cambiare indirizzo
        def senza_peso(dati):
            del next(v for v in dati["voci"] if v["formato"] == "pdf")["byte"]

        def peso_che_non_torna(dati):
            next(v for v in dati["voci"] if v["formato"] == "pdf")["byte"] += 5000

        def aggiuntivo_senza_peso(dati):
            del next(v for v in dati["voci"] if v.get("extra"))["extra"][0]["byte"]

        prova(base, "disciplinare in PDF senza il peso in byte", nel_catalogo(senza_peso), "manca «byte»")
        prova(base, "peso in KB che non torna con il peso in byte", nel_catalogo(peso_che_non_torna), "non torna con «byte»")
        prova(base, "documento aggiuntivo senza il peso in byte", nel_catalogo(aggiuntivo_senza_peso), "manca «byte»")
        prova(base, "data di verifica in formato sbagliato", nel_catalogo(data_sbagliata),
              "«verificato» deve essere una data AAAA-MM-GG")
        prova(base, "verifica dei collegamenti più vecchia della soglia (--eta 45)", nel_catalogo(verifica_vecchia),
              "la data di verifica dei collegamenti è ferma al", "--eta", "45")
        prova(base, "data di verifica nel futuro", nel_catalogo(verifica_futura), "«verificato» è una data futura")

        # letture annotate: il file, se c'è, è ben formato, e la data dei dati non è più recente delle letture
        def con_le_letture(letture):
            def cambia(caso):
                (caso / ".manuale").mkdir(exist_ok=True)
                testo = letture if isinstance(letture, str) else json.dumps(letture)
                (caso / ".manuale" / "cucina-emergenza-letture.json").write_text(testo, encoding="utf-8")
            return cambia

        scritta = catalogo["verificato"]
        prima_della_data = (date.fromisoformat(scritta) - timedelta(days=1)).isoformat()
        prova(base, "data di verifica portata avanti a mano: più recente di una lettura annotata",
              con_le_letture({in_pdf["url"]: prima_della_data, uno: scritta}), "non si porta avanti a mano")
        prova(base, "file delle letture con un giorno scritto male", con_le_letture({uno: "2026-1-05"}),
              "letture con il giorno scritto male o nel futuro")
        prova(base, "file delle letture con un giorno che non esiste", con_le_letture({uno: "2026-02-31"}),
              "letture con il giorno scritto male o nel futuro")
        prova(base, "file delle letture con un giorno nel futuro",
              con_le_letture({uno: (date.today() + timedelta(days=3)).isoformat()}), "letture con il giorno scritto male o nel futuro")
        prova(base, "file delle letture che non è una mappa", con_le_letture([uno]), "deve essere una mappa indirizzo → giorno")
        prova(base, "file delle letture rovinato", con_le_letture("{ non è json"), "il file delle letture non si legge")
        prova(base, "date di verifica diverse nei due file di dati",
              nel_catalogo(lambda dati: dati.update(verificato=prima_della_data)), "è diverso nei due file di dati")

        spec = importlib.util.spec_from_file_location("controllo_dei_dati", RADICE / "scripts" / SCRIPT)
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        tutti_i_collegamenti = modulo.collegamenti_da_leggere(*modulo.carica())
        vecchia = date.today() - timedelta(days=100)

        def vecchia_ovunque(caso):
            nel_catalogo(lambda dati: dati.update(verificato=vecchia.isoformat()))(caso)
            p = caso / "data" / "cucina_emergenza.yaml"
            p.write_text(re.sub(r'(?m)^verificato: "[^"]+"', f'verificato: "{vecchia.isoformat()}"', p.read_text(encoding="utf-8")),
                         encoding="utf-8")
            con_le_letture(dict(dict.fromkeys(tutti_i_collegamenti, date.today().isoformat()), **{uno: vecchia.isoformat()}))(caso)

        prova(base, "data di verifica ferma da troppo: il messaggio nomina il collegamento che la tiene ferma (--eta 45)",
              vecchia_ovunque, f"letti l'ultima volta il {vecchia:%d/%m/%Y}: {uno}.", "--eta", "45")

        caso = base.parent / "caso"
        if caso.exists():
            shutil.rmtree(caso)
        shutil.copytree(base, caso)
        con_le_letture({in_pdf["url"]: scritta, uno: scritta, "https://www.esempio.it/tolto.pdf": prima_della_data})(caso)
        r = lancia(caso, "--eta", "36500")
        esiti.append(r.returncode == 0)
        print(("ok  " if r.returncode == 0 else "NO  ")
              + "letture coerenti con la data passano, anche con un indirizzo che non è più nei dati")
        if r.returncode != 0:
            print("    " + "\n    ".join((r.stdout + r.stderr).strip().splitlines()[-12:]))
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

        # sintesi europee: documento unico o scheda riepilogativa, e le loro rettifiche
        con_sintesi = next((v for v in catalogo["voci"] if v.get("sintesi")), None)
        if con_sintesi is None:
            sys.exit("prova non eseguibile: nessun prodotto con la sintesi europea nei dati")
        europeo = con_sintesi["sintesi"]["url"]

        def nella_sintesi(funzione, quale=lambda v: v.get("sintesi")):
            def cambia(dati):
                funzione(next(v for v in dati["voci"] if quale(v)))
            return nel_catalogo(cambia)

        def stessa_sintesi(dati):
            con = [v for v in dati["voci"] if v.get("sintesi")]
            con[1]["sintesi"]["url"] = con[0]["sintesi"]["url"]

        def sintesi_su_stg(dati):
            next(v for v in dati["voci"] if v["tipo"] == "STG")["sintesi"] = dict(next(v for v in dati["voci"] if v.get("sintesi"))["sintesi"])

        def rettifica_piu_vecchia(voce):
            voce["sintesi"]["rettifiche"] = [{"url": voce["sintesi"]["url"] + "R%2801%29", "data": "1990-01-01", "pagine": 1, "kb": 10}]

        prova(base, "sintesi europea su un sito che non è EUR-Lex",
              nella_sintesi(lambda v: v["sintesi"].update(url=in_pdf["url"] + "&copia")), "si collega solo il PDF su EUR-Lex")
        prova(base, "sintesi europea di tipo sconosciuto",
              nella_sintesi(lambda v: v["sintesi"].update(tipo="riassunto")), "«sintesi» chiede il tipo")
        prova(base, "sintesi europea con la data nel futuro",
              nella_sintesi(lambda v: v["sintesi"].update(data=(date.today() + timedelta(days=3)).isoformat())), "«data» è una data futura")
        prova(base, "sintesi europea senza pagine", nella_sintesi(lambda v: v["sintesi"].pop("pagine")), "mancano pagine o peso del PDF")
        prova(base, "sintesi europea su una STG", nel_catalogo(sintesi_su_stg), "una STG non ha sintesi europea")
        prova(base, "stessa sintesi europea su due prodotti", nel_catalogo(stessa_sintesi),
              "sintesi europea: indirizzo già usato da un'altra voce")
        prova(base, "sintesi europea senza l'impronta del registro",
              nella_sintesi(lambda v: v.pop("registro_ue")), "non l'impronta «registro_ue»")
        prova(base, "impronta del registro scritta come una data",
              nella_sintesi(lambda v: v.update(registro_ue="2026-11-24")), "«registro_ue» è l'impronta")
        prova(base, "rettifica più vecchia dell'atto che corregge", nella_sintesi(rettifica_piu_vecchia),
              "è più vecchia dell'atto che corregge")
        prova(base, "catalogo costruito senza il collegamento a una sintesi europea",
              nella_pagina("disciplinari/index.html", lambda testo: testo.replace(europeo, europeo[:-4] + "0000", 1)),
              "la sintesi europea, o una sua rettifica, non compare")
        prova(base, "pagina che collega un PDF di EUR-Lex fuori dai dati",
              nella_pagina("disciplinari/index.html",
                           in_fondo('<a href="https://eur-lex.europa.eu/legal-content/IT/TXT/PDF/?uri=CELEX:52099XC0101%2801%29">Altro</a>')),
              "le pagine collegano un PDF che non è nei dati")

    prove_delle_risposte()
    print(f"\n{sum(esiti)} prove su {len(esiti)} come atteso")
    return 0 if all(esiti) else 1


if __name__ == "__main__":
    sys.exit(main())
