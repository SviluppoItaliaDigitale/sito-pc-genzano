#!/usr/bin/env python3
"""Prove di check-cucina-emergenza.py, il controllo della sezione /cucina-emergenza/.

Il controllo è bloccante sulle PR e ogni mese rilegge i collegamenti: se smette di vedere un errore, nessuno
se ne accorge. Quattro gruppi di prove, nessuna richiesta fuori dalla macchina:
  1. senza rete: i casi sbagliati (sito non istituzionale, file Word, PDF fuori dai dati, collegamento
     mancante, verifica troppo vecchia, sintesi europea su un altro sito o senza il suo collegamento…) che
     deve respingere con il messaggio giusto, e la copia intatta che deve passare;
  2. risposte dei siti, con un server finto in locale: un PDF vero è letto, un 404 è un collegamento rotto,
     una pagina di verifica anti-bot o un rifiuto (403) non sono né rotti né controllati, e nemmeno un sito
     che dà tempo scaduto o un errore del server (5xx); una pagina qualsiasi al posto del PDF, o un 400, è
     una fonte non letta, e lo sono troppi collegamenti rimasti senza controllo (più di SOGLIA_FERMO e più
     di un quinto di quelli da aprire);
  3. browser di riserva: se Playwright manca o Chromium non parte, il controllo non si interrompe, classifica
     ciò che ha già letto e scrive il rapporto, che dice perché il ripiego è mancato;
  4. sintesi europee, con un registro e un archivio finti in locale: una pubblicazione nuova, un fascicolo
     cambiato, un prodotto sparito e una rettifica nuova sono novità; un atto che l'archivio non ha più è un
     collegamento rotto, ma solo dopo la conferma della richiesta singola; registro o archivio muti sono
     fonti non lette, e anche un archivio che non restituisce più le rettifiche già note. In più, le
     funzioni di scripts/aggiorna-documenti-unici.py che decidono quale documento è di quale prodotto
     (denominazione intera fra virgolette o numero di fascicolo: «Bra» non è «fibra») e il suo lavoro su un
     catalogo finto: ciò che non si legge o non si sa interpretare non cambia i dati.

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
            esito("sintesi: nessuna di queste prove ha chiesto qualcosa a un sito", not tentate, f"{tentate}")
    finally:
        ue.interroga, ue.chiedi, ue.FILE_CATALOGO, ue.RADICE, ue.shutil, sys.argv = veri
        ue.non_letti.clear()


def prove_delle_sintesi(controllo, base):
    """Registro europeo e archivio dell'UE finti: che cosa è novità, che cosa è rotto, che cosa è fonte non letta."""
    ue = controllo.documenti_unici()
    prove_dello_script_delle_sintesi(ue)
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

    def giro(nome, atteso, registro_finto=registro, **finto):
        FINTO.update({"registro": registro_finto, "stato_registro": 200, "stato_archivio": 200, "fuori_dal_gruppo": set(),
                      "inesistenti": set(), "rettifiche": note})
        FINTO.update(finto)
        for elenco in (controllo.errori, controllo.non_letti, controllo.novita, controllo.protetti, controllo.da_rivedere, controllo.muti):
            elenco.clear()
        controllo.metodi.clear()
        controllo.di_fila.clear()
        controllo.controlla_europa(json.loads(json.dumps(catalogo)))
        visto = (len(controllo.errori), len(controllo.non_letti), len(controllo.novita), controllo.metodi["archivio dell'UE"])
        testo = " | ".join(controllo.errori + [t for _, t in controllo.non_letti] + controllo.novita)
        esito(nome, visto == atteso[:4] and all(pezzo in testo for pezzo in atteso[4:]),
              f"rotti, non letti, novità, atti trovati: {visto}; atteso {atteso[:4]} con {atteso[4:]}; {testo[:300]}")

    try:
        giro("sintesi: registro e archivio uguali ai dati, nessun rilievo (il fascicolo «PGI-IT-2» vale «PGI-IT-0002»)", (0, 0, 0, 3))
        giro("sintesi: una pubblicazione nuova nel registro è una novità", (0, 0, 1, 3, "Formaggio Alfa", "pubblicazioni diverse", "07/07/2026"),
             registro_finto=[del_registro("PDO-IT-0001", "Formaggio Alfa", (1, "1.1.2020"), (7, "7.7.2026"))] + registro[1:])
        giro("sintesi: un fascicolo cambiato nel registro è una novità", (0, 0, 1, 3, "Salame Beta", "PGI-IT-0099"),
             registro_finto=[registro[0], dict(registro[1], fileNumber="PGI-IT-0099")] + registro[2:])
        giro("sintesi: un prodotto che il registro non ha più è una novità", (0, 0, 1, 3, "Olio Gamma", "non c'è più un solo prodotto"),
             registro_finto=registro[:2] + registro[3:])
        giro("sintesi: due voci del registro con lo stesso nome sono una novità", (0, 0, 1, 3, "Olio Gamma"),
             registro_finto=registro + [dict(registro[2], giIdentifier="EUGI8888", fileNumber="PDO-IT-0888")])
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
        giro("sintesi: una rettifica che i dati non conoscono è una novità", (0, 0, 1, 3, "Formaggio Alfa", "52020XC0101(01)R(01)", "05/05/2025"),
             rettifiche=dict(note, **{"52020XC0101(01)": [("52020XC0101(01)R(01)", "2025-05-05")]}))
        giro("sintesi: archivio muto, due fonti non lette (esistenza e rettifiche) e nessun collegamento rotto", (0, 2, 0, 0, "non ha detto se esistono", "rettifiche nuove"),
             stato_archivio=503)
        giro("sintesi: se l'archivio non restituisce più le rettifiche che i dati conoscono, la risposta non vale (fonte non letta)",
             (0, 1, 0, 3, "non ha restituito 2 rettifiche", "52021XC0202(02)R(01)"), rettifiche={})

        # documenti su EUR-Lex: l'esistenza la dice l'archivio dell'UE, poi si chiede l'indirizzo del PDF
        def eurlex(nome, percorso, atteso):
            FINTO.update({"stato_archivio": 200, "inesistenti": set()})
            for elenco in (controllo.errori, controllo.non_letti, controllo.novita, controllo.protetti, controllo.da_rivedere, controllo.muti):
                elenco.clear()
            controllo.metodi.clear()
            controllo.di_fila.clear()
            controllo.controlla_ue("documento «prova»", f"{base}{percorso}?uri=CELEX:52020XC0101%2801%29")
            controllo.chiudi_da_rivedere(False)
            visto = (len(controllo.errori), len(controllo.non_letti), len(controllo.protetti), len(controllo.muti),
                     controllo.metodi["richiesta diretta"], controllo.metodi["archivio dell'UE"])
            esito(nome, visto == atteso, f"rotti, non letti, protetti, muti, letti, confermati dall'archivio: {visto}; atteso {atteso}")

        eurlex("EUR-Lex: il PDF risponde, letto con la richiesta diretta", "/vero.pdf", (0, 0, 0, 0, 1, 0))
        eurlex("EUR-Lex: risposta 202 senza contenuto, vale l'esistenza nell'archivio dell'UE", "/attesa.pdf", (0, 0, 0, 0, 0, 1))
        eurlex("EUR-Lex: errore del server sull'indirizzo del PDF, «non controllato» e non fonte non letta", "/guasto.pdf", (0, 0, 0, 1, 0, 0))
        eurlex("EUR-Lex: rifiuto (403) sull'indirizzo del PDF, «non controllato» e non fonte non letta", "/rifiuto.pdf", (0, 0, 1, 0, 0, 0))
        eurlex("EUR-Lex: un 400 sull'indirizzo del PDF resta una fonte non letta", "/negato.pdf", (0, 1, 0, 0, 0, 0))
        eurlex("EUR-Lex: un 404 sull'indirizzo del PDF è un collegamento rotto", "/manca.pdf", (1, 0, 0, 0, 0, 0))
        vuoto = {"voci": [{"nome": "Formaggio Alfa", "tipo": "DOP"}, {"nome": "Pizza Finta", "tipo": "STG"}]}
        for elenco in (controllo.errori, controllo.non_letti, controllo.novita):
            elenco.clear()
        FINTO["stato_registro"] = 500
        controllo.controlla_europa(vuoto)
        esito("sintesi: un catalogo senza dati europei non interroga il registro",
              not controllo.errori and not controllo.non_letti and not controllo.novita)
    finally:
        ue.REGISTRO, controllo.SPARQL_UE, controllo.ARCHIVIO_UE = veri
        for elenco in (controllo.errori, controllo.non_letti, controllo.novita):
            elenco.clear()
        controllo.metodi.clear()


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
        # un sito che non risponde: tempo scaduto o errore del server. Regola guasti, punto 3: non è un collegamento
        # rotto e non rende rosso il controllo, ma resta nel rapporto e la data di verifica non si aggiorna
        def pulisci():
            for elenco in (controllo.errori, controllo.non_letti, controllo.protetti, controllo.da_rivedere, controllo.muti):
                elenco.clear()
            controllo.metodi.clear()
            controllo.di_fila.clear()
            controllo.motivo.clear()

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
              "### Collegamenti non controllati: il sito non ha risposto in tempo" in testo and "Nessun problema." not in testo
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
        pulisci()
        prove_del_browser(controllo, base)
        prove_delle_sintesi(controllo, base)
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
