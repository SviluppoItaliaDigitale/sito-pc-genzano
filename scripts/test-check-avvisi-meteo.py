#!/usr/bin/env python3
"""Prove di scripts/check-avvisi-meteo.py: validità degli avvisi meteo e salvataggio.

Senza rete: il testo dei PDF è incollato qui, pagina e PDF sono finti, l'ora è
fissa. Uscita 0 se tutte le prove passano, 1 altrimenti. Gira su ogni pull
request in validate-pr.yml.

Nasce l'11/11/2026: l'avviso per vento «dal mattino di domani, giovedì
12.11.2026, e per le successive 24-36 ore» risultava valido dal giorno del file
per 36 ore (fino a venerdì alle 12 invece che a fine giornata), e una validità
corretta con lo stesso tipo e livello non veniva mai salvata.
"""

import importlib.util
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

QUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("check_avvisi_meteo", QUI / "check-avvisi-meteo.py")
cam = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cam)
ROMA = cam.ROME_TZ

# Estratto testuale (pdftotext -layout) dell'allertamento regionale emesso
# l'11/11/2026, con gli a capo e gli spazi del PDF vero.
ALLERTAMENTO_11_11_2026 = """REGIONE.LAZIO.REGISTRO UFFICIALE.U.1139712.11-11-2026

             ALLERTAMENTO DEL SISTEMA DI PROTEZIONE CIVILE REGIONALE
                         PER I SEGUENTI RISCHI: VENTO , CRITICITA’ IDROGEOLOGICA ED IDRAULICA .

      La Presidenza del Consiglio dei Ministri - Dipartimento della Protezione Civile ha emesso l’                      Avviso di condizioni
      meteorologiche avverse n.26072 del 11.11.2026 con indicazione che:

      dal mattino di domani, giovedì 12.11.2026, e per le successive 24-36 ore, si prevedono sul Lazio:
      Venti da forti a burrasca sud-occidentali, con raffiche fino a burrasca forte sui crinali appenninici. Mareggiate
      lungo le coste esposte.
      Altresì, dalla tarda mattinata di domani, giovedì 12.11.2026, e per le successive 24-36 ore, si prevedono
      precipitazioni da sparse a diffuse, anche a carattere di rovescio o temporale, specie sulle zone interne.
      I fenomeni saranno accompagnati da rovesci di forte intensità, forti raffiche di vento e frequente attività
      elettrica.
      Si invitano pertanto gli Enti destinatari ad attivare le fasi operative previste dalla propria pianificazione di
      Protezione Civile ed adottare tutti gli adempimenti di competenza.

                                               ALLERTA PER VENTO
       ALLERTA GIALLA su tutte le Zone di Allerta
"""

ESITI = []


def prova(nome, ottenuto, atteso):
    ok = ottenuto == atteso
    ESITI.append(ok)
    print(f"{'✓' if ok else '✗'} {nome}" + ("" if ok else f"\n    atteso:   {atteso!r}\n    ottenuto: {ottenuto!r}"))


def iso(x):
    return x.isoformat(timespec="seconds") if x is not None else None


def validita(testo, nome_file, tipo):
    inizio, fine, descr, dal, durata = cam.estrai_validita_e_descrizione(testo, cam.estrai_data_da_nome(nome_file), tipo)
    return iso(inizio), iso(fine), descr, dal, durata


# 1. Il PDF vero dell'11/11/2026: vento dal mattino del 12, per 24-36 ore.
prova("allertamento dell'11/11/2026, vento",
      validita(ALLERTAMENTO_11_11_2026, "Allertamento12-11-2026.pdf", "vento"),
      ("2026-11-12T06:00:00+01:00", "2026-11-14T00:00:00+01:00",
       "Venti da forti a burrasca sud-occidentali, con raffiche fino a burrasca forte sui crinali appenninici",
       "dal mattino", "24-36 ore"))

# 2. La frase sulle piogge cita le «raffiche di vento» dei temporali: non deve
#    allungare l'avviso del vento. Per i temporali vale invece quella frase.
prova("allertamento dell'11/11/2026, temporali",
      validita(ALLERTAMENTO_11_11_2026, "Allertamento12-11-2026.pdf", "temporali")[:2] + validita(ALLERTAMENTO_11_11_2026, "Allertamento12-11-2026.pdf", "temporali")[3:],
      ("2026-11-12T10:00:00+01:00", "2026-11-14T01:00:00+01:00", "dalla tarda mattinata", "24-36 ore"))

# 3. La forma che lo script riconosceva già: «dalle prime ore di domani».
prova("dalle prime ore di domani, con data",
      validita("Si comunica che dalle prime ore di domani, martedì 31.03.2026, e per le successive 24-36 ore, "
               "si prevedono sul Lazio: venti forti nord-orientali. ", "vento 30 03 2026.pdf", "vento"),
      ("2026-03-31T00:00:00+02:00", "2026-04-01T18:00:00+02:00", "venti forti nord-orientali", "dalle prime ore", "24-36 ore"))

# 4. «Domani» senza data: il giorno si conta dal protocollo, non dal nome del file.
prova("domani senza data, dal protocollo",
      validita("REGIONE.LAZIO.REGISTRO UFFICIALE.U.1.05-12-2026\n dal pomeriggio di domani e per le successive 24 ore "
               "si prevedono sul Lazio: nevicate fino a quote collinari. ", "Allertamento06-12-2026.pdf", "neve")[:2]
      + validita("REGIONE.LAZIO.REGISTRO UFFICIALE.U.1.05-12-2026\n dal pomeriggio di domani e per le successive 24 ore "
                 "si prevedono sul Lazio: nevicate fino a quote collinari. ", "Allertamento06-12-2026.pdf", "neve")[3:],
      ("2026-12-06T12:00:00+01:00", "2026-12-07T18:00:00+01:00", "dal pomeriggio", "24 ore"))

# 5. Ora esplicita.
prova("dalle ore 12 di domani",
      validita("dalle ore 12 di domani, venerdì 13.11.2026, e per le successive 12-18 ore, si prevedono sul Lazio: "
               "venti di burrasca. ", "Allertamento13-11-2026.pdf", "vento")[:2],
      ("2026-11-13T12:00:00+01:00", "2026-11-14T06:00:00+01:00"))

# 5-bis. «Tarda sera» e «prima mattinata»: prima non erano riconosciute e la validità
#        ricadeva sulla regola di ripiego (giorno del file, 36 ore).
prova("dalla tarda sera di domani",
      validita("dalla tarda sera di domani, sabato 14.11.2026, e per le successive 12 ore, si prevedono sul Lazio: "
               "venti forti. ", "Allertamento14-11-2026.pdf", "vento")[:2],
      ("2026-11-14T21:00:00+01:00", "2026-11-15T12:00:00+01:00"))
prova("dalla prima mattinata di domani",
      validita("dalla prima mattinata di domani, sabato 14.11.2026, e per le successive 12 ore, si prevedono sul Lazio: "
               "venti forti. ", "Allertamento14-11-2026.pdf", "vento")[:2],
      ("2026-11-14T06:00:00+01:00", "2026-11-14T22:00:00+01:00"))

# 5-ter. Minuti: la fine si arrotonda all'ora dopo, mai prima.
prova("dalle ore 18.30 di oggi",
      validita("dalle ore 18.30 di oggi, mercoledì 11.11.2026, e per le successive 24 ore, si prevedono sul Lazio: "
               "venti forti. ", "Allertamento11-11-2026.pdf", "vento")[:2],
      ("2026-11-11T18:00:00+01:00", "2026-11-12T19:00:00+01:00"))

# 5-quater. «Domani» senza data e senza data di emissione nel testo: non si
#    indovina dal nome del file (porta il giorno di validità), si usa la regola
#    di prima e il giro lo segnala.
prova("domani senza data né emissione",
      validita("dal pomeriggio di domani e per le successive 24 ore si prevedono sul Lazio: venti forti. ",
               "Allertamento12-11-2026.pdf", "vento"),
      ("2026-11-12T00:00:00+01:00", "2026-11-13T12:00:00+01:00", "venti forti", None, None))

# 6. Nessuna frase di validità: resta la regola di prima (giorno del file, 36 ore).
prova("senza frasi di validità",
      validita("ALLERTA PER VENTO: ALLERTA GIALLA. Si invitano gli Enti ad attivare le fasi operative previste "
               "dalla propria pianificazione.", "Allertamento12-11-2026.pdf", "vento"),
      ("2026-11-12T00:00:00+01:00", "2026-11-13T12:00:00+01:00", None, None, None))

# 7. «dalla propria pianificazione», «dal successivo Bollettino»: non sono validità.
prova("nessuna falsa frase di validità",
      cam.frasi_validita("adempimenti previsti dalla propria pianificazione, confermata dal successivo Bollettino di "
                         "criticità e dalla modellistica idrologica.", datetime(2026, 11, 11, tzinfo=ROMA)),
      [])


# 8. Il giro completo, con pagina e PDF finti e l'ora fissa all'11/11/2026 18:00:
#    la validità corretta si salva anche con lo stesso tipo e livello, e un
#    secondo giro con lo stesso PDF non cambia più nulla.
class OraFissa(datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime(2026, 11, 11, 18, 0, tzinfo=tz)


class RispostaFinta:
    def __init__(self, dati):
        self.dati = dati

    def read(self):
        return self.dati

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def giro(cartella):
    uscita = Path(cartella) / "uscita.txt"
    uscita.write_text("", encoding="utf-8")
    os.environ["GITHUB_OUTPUT"] = str(uscita)
    os.environ.pop("FONTI_KO_FILE", None)
    cam.main()
    righe = dict(r.split("=", 1) for r in uscita.read_text(encoding="utf-8").split("\n") if "=" in r)
    return righe.get("changed")


with tempfile.TemporaryDirectory() as cartella:
    allerta = Path(cartella) / "allerta.json"
    vecchio = {
        "tipo": "vento", "livello": "gialla",
        "validita_inizio": "2026-11-12T00:00:00+01:00", "validita_fine": "2026-11-13T12:00:00+01:00",
        "url": "https://www.regione.lazio.it/sites/default/files/allertamentiregionali-allegati/2026/Allertamento12-11-2026.pdf",
        "fonte_data": "2026-11-12",
        "descrizione": "Venti da forti a burrasca sud-occidentali, con raffiche fino a burrasca forte sui crinali appenninici",
    }
    allerta.write_text(json.dumps({"livello": "verde", "avviso_meteo": vecchio}), encoding="utf-8")
    cam.ALLERTA_PATH = allerta
    cam.datetime = OraFissa
    cam.http_get_text = lambda url: ('<a href="/sites/default/files/allertamentiregionali-allegati/2026/'
                                     'Allertamento12-11-2026.pdf">Allertamento</a>')
    cam.urllib.request.urlopen = lambda req, timeout=None: RispostaFinta(b"%PDF-1.4 finto")
    cam.parse_pdf = lambda dati: ALLERTAMENTO_11_11_2026
    stdout = sys.stdout
    sys.stdout = open(os.devnull, "w", encoding="utf-8")
    try:
        primo = giro(cartella)
        salvato = json.loads(allerta.read_text(encoding="utf-8"))["avviso_meteo"]
        secondo = giro(cartella)
    finally:
        sys.stdout.close()
        sys.stdout = stdout
    prova("validità corretta salvata con lo stesso tipo e livello", primo, "true")
    prova("validità salvata", (salvato["validita_inizio"], salvato["validita_fine"],
                               salvato.get("validita_dal"), salvato.get("validita_durata")),
          ("2026-11-12T06:00:00+01:00", "2026-11-14T00:00:00+01:00", "dal mattino", "24-36 ore"))
    prova("secondo giro con lo stesso PDF: nessun cambio", secondo, "false")


# 9. Validità non leggibile nel bollettino nuovo (revisione dell'11/11/2026): la
#    stima «giorno del file per 36 ore» non accorcia né fa scadere un avviso in
#    vigore dello stesso tipo e livello; un livello diverso invece si salva.
def senza_validita(livello):
    return ("REGIONE.LAZIO.REGISTRO UFFICIALE.U.1139799.12-11-2026\n"
            "ALLERTAMENTO DEL SISTEMA DI PROTEZIONE CIVILE REGIONALE\n"
            "PER I SEGUENTI RISCHI: VENTO .\n"
            "Si confermano sul Lazio venti da forti a burrasca sud-occidentali.\n"
            f"ALLERTA PER VENTO\n ALLERTA {livello} su tutte le Zone di Allerta\n")


IN_VIGORE = {
    "tipo": "vento", "livello": "gialla",
    "validita_inizio": "2026-11-12T06:00:00+01:00", "validita_fine": "2026-11-14T00:00:00+01:00",
    "url": "https://www.regione.lazio.it/sites/default/files/allertamentiregionali-allegati/2026/Allertamento12-11-2026.pdf",
    "fonte_data": "2026-11-12", "validita_dal": "dal mattino", "validita_durata": "24-36 ore",
}


def giro_con(testo, nome_pdf):
    with tempfile.TemporaryDirectory() as cartella:
        allerta = Path(cartella) / "allerta.json"
        allerta.write_text(json.dumps({"livello": "verde", "avviso_meteo": dict(IN_VIGORE)}), encoding="utf-8")
        cam.ALLERTA_PATH = allerta
        cam.http_get_text = lambda url: ('<a href="/sites/default/files/allertamentiregionali-allegati/2026/'
                                         f'{nome_pdf}">Allertamento</a>')
        cam.parse_pdf = lambda dati: testo
        stdout = sys.stdout
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
        try:
            cambiato = giro(cartella)
        finally:
            sys.stdout.close()
            sys.stdout = stdout
        return cambiato, json.loads(allerta.read_text(encoding="utf-8")).get("avviso_meteo")


cambiato, avviso = giro_con(senza_validita("GIALLA"), "Allertamento12-11-2026.pdf")
prova("stima di validità, stesso tipo e livello: avviso in vigore intatto", (cambiato, avviso), ("false", IN_VIGORE))
cambiato, avviso = giro_con(senza_validita("ARANCIONE"), "Allertamento12-11-2026.pdf")
prova("stima di validità, livello più alto: si salva", (cambiato, avviso["livello"]), ("true", "arancione"))
cambiato, avviso = giro_con(senza_validita("GIALLA"), "Allertamento10-11-2026.pdf")
prova("scaduto solo secondo la stima: l'avviso in vigore non si toglie", (cambiato, avviso), ("false", IN_VIGORE))

print(f"\n{sum(ESITI)}/{len(ESITI)} prove superate")
sys.exit(0 if all(ESITI) else 1)
