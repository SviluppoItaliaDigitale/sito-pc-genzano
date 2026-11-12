#!/usr/bin/env python3
"""Prove delle fonti del livello di allerta (scripts/check-allerta.py).

Dall'11/11/2026 il bollettino nazionale si legge dal repository ufficiale del
Dipartimento; il mirror opendatasicilia è solo la riserva, letta quando la
fonte ufficiale non dà un bollettino valido adesso. Le prove usano i testi e
i valori veri del bollettino dell'11/11/2026 ore 15:40 (zona Bacini Costieri
Sud: oggi nessuna allerta, domani gialla per rischio idrogeologico), senza
rete: le richieste sono sostituite da dati finti.

Uso: python3 scripts/test-check-allerta.py   (solo libreria standard)
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path
from unittest.mock import patch
from zoneinfo import ZoneInfo

QUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("check_allerta", QUI / "check-allerta.py")
CA = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CA)

ROMA = ZoneInfo("Europe/Rome")
NESSUNA = "Assenza di fenomeni significativi prevedibili / NESSUNA ALLERTA"

BOLLETTINO = {
    "type": "first",
    "name": "Bollettino del 11 novembre 2026 ore 15:40",
    "today": {"html_descrition": "<p>Per la giornata di oggi,  mercoledì 11 novembre 2026:<br/>"
                                 "<b>MODERATA CRITICITA' PER RISCHIO IDRAULICO / ALLERTA ARANCIONE:</b></p>"},
    "tomorrow": {"html_descrition": "<p>Per la giornata di domani,  giovedì 12 novembre 2026:<br/>"
                                    "<b>Lazio</b>: Bacini Costieri Sud, Bacini di Roma</p>"},
}


def zona(nome, comuni, mappa=NESSUNA, idrogeo=NESSUNA, temporali=NESSUNA, idraulico=NESSUNA):
    return {"type": "Polygon", "arcs": [[0]], "properties": {
        "Rappresentata nella mappa": mappa,
        "Per rischio idraulico": idraulico,
        "Per rischio temporali": temporali,
        "Per rischio idrogeologico": idrogeo,
        "Nome zona": nome,
        "Comuni": comuni,
    }}


def carta(*zone, nome="20261111_1540_today"):
    return {"type": "Topology", "arcs": [], "objects": {nome: {"type": "GeometryCollection",
                                                              "geometries": list(zone)}}}


CARTA_OGGI = carta(
    zona("Bacini di Roma", ["Albano Laziale", "Ariccia", "Roma"]),
    zona("Bacini Costieri Sud", ["Albano Laziale", "Ariccia", "Genzano di Roma", "Velletri"]),
)
CARTA_DOMANI = carta(
    zona("Bacini di Roma", ["Albano Laziale", "Ariccia", "Roma"],
         mappa="Ordinaria per rischio idrogeologico / ALLERTA GIALLA", idrogeo="Ordinaria / ALLERTA GIALLA"),
    zona("Bacini Costieri Sud", ["Albano Laziale", "Ariccia", "Genzano di Roma", "Velletri"],
         mappa="Ordinaria per rischio idrogeologico / ALLERTA GIALLA", idrogeo="Ordinaria / ALLERTA GIALLA"),
    nome="20261111_1540_tomorrow",
)


def ora(anno, mese, giorno, h, m=0):
    return datetime(anno, mese, giorno, h, m, tzinfo=ROMA)


def fonte_finta(timbro="20261111_1540", carte=None, bollettino=None):
    """http_get_json finto che ricorda gli indirizzi chiesti."""
    carte = carte or {"today": CARTA_OGGI, "tomorrow": CARTA_DOMANI}
    chiesti = []

    def prendi(url, timeout=None):
        chiesti.append(url)
        if url == f"{CA.DPC_RAW}{timbro}.json":
            return bollettino or BOLLETTINO
        for chiave, valore in carte.items():
            if url == f"{CA.DPC_RAW}topojson/{timbro}_{chiave}.json":
                if isinstance(valore, Exception):
                    raise valore
                return valore
        raise OSError(f"404 {url}")
    return prendi, chiesti


def riga_csv(inizio, fine, pubblicazione, criticita=NESSUNA, idrogeo=NESSUNA):
    return {"comune_nome": "Genzano di Roma", "data_pubblicazione": pubblicazione,
            "data_validita_inizio": inizio, "data_validita_fine": fine,
            "avviso_criticita": criticita, "avviso_idrogeologico": idrogeo,
            "avviso_temporali": NESSUNA, "avviso_idraulico": NESSUNA}


@contextlib.contextmanager
def ambiente(**pubblicato):
    """File temporanei per allerta.json, uscite del workflow e fonti non lette.
    Le chiavi passate (per esempio domani=…) si aggiungono allo stato pubblicato."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        allerta = tmp / "allerta.json"
        allerta.write_text(json.dumps({
            "livello": "verde", "titolo": "NESSUNA ALLERTA", "descrizione": "x",
            "ultimo_aggiornamento": "2026-11-01T10:00:00+01:00",
            "ultimo_controllo": "2026-11-01T10:00:00+01:00",
            "avviso_meteo": {"tipo": "vento", "livello": "gialla"},
            **pubblicato,
        }), encoding="utf-8")
        env = {"GITHUB_OUTPUT": str(tmp / "out.txt"), "FONTI_KO_FILE": str(tmp / "ko.txt")}
        with patch.dict(os.environ, env), patch.object(CA, "ALLERTA_PATH", allerta):
            yield tmp, allerta


def uscite(tmp):
    righe = (tmp / "out.txt").read_text(encoding="utf-8").splitlines() if (tmp / "out.txt").exists() else []
    return dict(r.split("=", 1) for r in righe if "=" in r)


def fonti_ko(tmp):
    f = tmp / "ko.txt"
    return f.read_text(encoding="utf-8") if f.exists() else ""


def gira_main(adesso, **sostituzioni):
    class OraFissa(datetime):
        @classmethod
        def now(cls, tz=None):
            return adesso.astimezone(tz) if tz else adesso.replace(tzinfo=None)

    with contextlib.ExitStack() as pila:
        pila.enter_context(patch.object(CA, "datetime", OraFissa))
        for nome, valore in sostituzioni.items():
            pila.enter_context(patch.object(CA, nome, valore))
        pila.enter_context(contextlib.redirect_stdout(io.StringIO()))
        try:
            CA.main()
        except SystemExit:
            pass


def mirror_vietato(*a, **k):
    raise AssertionError("il mirror non va letto quando la fonte ufficiale copre adesso")


class ZonaDiGenzano(unittest.TestCase):
    def test_trova_la_zona_dai_comuni(self):
        z = CA.zona_genzano(CARTA_DOMANI)
        self.assertEqual(z["Nome zona"], "Bacini Costieri Sud")
        self.assertEqual(z["Per rischio idrogeologico"], "Ordinaria / ALLERTA GIALLA")

    def test_senza_genzano_e_un_errore_non_nessuna_allerta(self):
        with self.assertRaises(ValueError):
            CA.zona_genzano(carta(zona("Bacini di Roma", ["Roma"])))
        with self.assertRaises(ValueError):
            CA.zona_genzano({})

    def test_campi_cambiati_sono_un_errore(self):
        c = carta(zona("Bacini Costieri Sud", ["Genzano di Roma"]))
        del c["objects"]["20261111_1540_today"]["geometries"][0]["properties"]["Per rischio temporali"]
        with self.assertRaises(ValueError):
            CA.zona_genzano(c)

    def test_due_zone_vale_il_livello_piu_alto(self):
        c = carta(zona("A", ["Genzano di Roma"], temporali="Ordinaria per rischio temporali / ALLERTA GIALLA"),
                  zona("B", ["Genzano di Roma"], temporali="Moderata / ALLERTA ARANCIONE"))
        with contextlib.redirect_stdout(io.StringIO()):
            z = CA.zona_genzano(c)
        self.assertEqual(z["Per rischio temporali"], "Moderata / ALLERTA ARANCIONE")


class GiorniEValidita(unittest.TestCase):
    PUBBL = datetime(2026, 11, 11, 15, 40, tzinfo=ROMA)

    def test_giorni_dal_timbro(self):
        with ambiente() as (tmp, _):
            g = CA.giorni_del_bollettino(BOLLETTINO, self.PUBBL)
            self.assertEqual(fonti_ko(tmp), "")
        self.assertEqual(str(g["oggi"]), "2026-11-11")
        self.assertEqual(str(g["domani"]), "2026-11-12")

    def test_testo_diverso_dal_timbro_si_segnala(self):
        altro = json.loads(json.dumps(BOLLETTINO))
        altro["tomorrow"]["html_descrition"] = "<p>Per la giornata di domani, venerdì 13 novembre 2026:</p>"
        with ambiente() as (tmp, _), contextlib.redirect_stdout(io.StringIO()):
            g = CA.giorni_del_bollettino(altro, self.PUBBL)
            self.assertIn("vale il timbro", fonti_ko(tmp))
        self.assertEqual(str(g["domani"]), "2026-11-12")

    def test_validita_come_il_mirror(self):
        oggi = CA.riga_dpc(CA.zona_genzano(CARTA_OGGI), self.PUBBL.date(), self.PUBBL, "oggi")
        self.assertEqual(oggi["data_validita_inizio"], "2026-11-11T15:40:00+01:00")
        self.assertEqual(oggi["data_validita_fine"], "2026-11-11T23:59:59+01:00")
        domani = CA.riga_dpc(CA.zona_genzano(CARTA_DOMANI), datetime(2026, 11, 12).date(), self.PUBBL, "domani")
        self.assertEqual(domani["data_validita_inizio"], "2026-11-12T00:00:00+01:00")
        self.assertEqual(domani["avviso_criticita"], "Ordinaria per rischio idrogeologico / ALLERTA GIALLA")


class LetturaUfficiale(unittest.TestCase):
    def test_la_carta_di_ieri_non_si_scarica(self):
        prendi, chiesti = fonte_finta()
        with ambiente(), contextlib.redirect_stdout(io.StringIO()), \
                patch.object(CA, "timbro_dpc", lambda: ("20261111_1540", "fonte ufficiale", [])), \
                patch.object(CA, "http_get_json", prendi):
            righe, dubbi = CA.leggi_dpc_ufficiale(ora(2026, 11, 12, 9))
        self.assertEqual(sorted(righe), ["domani"])
        self.assertEqual(dubbi, set())    # il bollettino dell'11/11 non copre il 13/11: non è un guasto
        self.assertFalse(any(u.endswith("_today.json") for u in chiesti))
        self.assertTrue(CA.copre_adesso(righe, ora(2026, 11, 12, 9)))

    def test_carta_illeggibile_si_segnala(self):
        prendi, _ = fonte_finta(carte={"today": OSError("timeout"), "tomorrow": CARTA_DOMANI})
        with ambiente() as (tmp, _), contextlib.redirect_stdout(io.StringIO()), \
                patch.object(CA, "timbro_dpc", lambda: ("20261111_1540", "fonte ufficiale", [])), \
                patch.object(CA, "http_get_json", prendi):
            righe, dubbi = CA.leggi_dpc_ufficiale(ora(2026, 11, 11, 18))
            self.assertIn("today", fonti_ko(tmp))
        self.assertEqual(sorted(righe), ["domani"])
        self.assertEqual(dubbi, {date(2026, 11, 11)})

    def test_fonte_muta_oggi_e_domani_in_dubbio(self):
        with ambiente(), contextlib.redirect_stdout(io.StringIO()), \
                patch.object(CA, "timbro_dpc", lambda: ("", "", ["albero non raggiungibile"])):
            righe, dubbi = CA.leggi_dpc_ufficiale(ora(2026, 11, 11, 18))
        self.assertEqual(righe, {})
        self.assertEqual(dubbi, {date(2026, 11, 11), date(2026, 11, 12)})


class SceltaDelTimbro(unittest.TestCase):
    def _modulo(self, candidati, problemi=(), completi=None):
        m = CA.modulo_timbro_dpc()
        m.candidati_dalle_fonti = lambda: (list(candidati), list(problemi))
        m.terna_completa = (lambda t: True) if completi is None else (lambda t: t in completi)
        return m

    def test_api_ferma_e_mirror_fermo_vince_lo_snapshot(self):
        # 11/11/2026: albero e commit non raggiungibili, mirror all'8/11,
        # snapshot all'11/11: non si deve tornare all'8/11.
        m = self._modulo([("20261108_1422", "mirror opendatasicilia")],
                         ["albero ufficiale non raggiungibile (HTTP Error 403)"])
        with patch.object(CA, "modulo_timbro_dpc", lambda: m), \
                patch.object(CA, "timbro_snapshot", lambda: "20261111_1540"):
            timbro, via, _ = CA.timbro_dpc()
        self.assertEqual(timbro, "20261111_1540")
        self.assertIn("snapshot", via)

    def test_albero_ufficiale_piu_nuovo_dello_snapshot(self):
        m = self._modulo([("20261111_1910", "fonte ufficiale"), ("20261111_1540", "fonte ufficiale")])
        with patch.object(CA, "modulo_timbro_dpc", lambda: m), \
                patch.object(CA, "timbro_snapshot", lambda: "20261111_1540"):
            timbro, via, _ = CA.timbro_dpc()
        self.assertEqual((timbro, via), ("20261111_1910", "fonte ufficiale"))

    def test_senza_carte_si_scende_al_precedente(self):
        m = self._modulo([("20261111_1910", "fonte ufficiale"), ("20261111_1540", "fonte ufficiale")],
                         completi={"20261111_1540"})
        with patch.object(CA, "modulo_timbro_dpc", lambda: m), \
                patch.object(CA, "timbro_snapshot", lambda: ""):
            timbro, _, problemi = CA.timbro_dpc()
        self.assertEqual(timbro, "20261111_1540")
        self.assertTrue(any("20261111_1910" in p for p in problemi))

    def test_ricerca_rotta_resta_lo_snapshot(self):
        def rotto():
            raise RuntimeError("file mancante")
        with patch.object(CA, "modulo_timbro_dpc", rotto), \
                patch.object(CA, "timbro_snapshot", lambda: "20261111_1540"):
            timbro, via, problemi = CA.timbro_dpc()
        self.assertEqual(timbro, "20261111_1540")
        self.assertTrue(problemi)

    def test_nessun_timbro(self):
        m = self._modulo([])
        with patch.object(CA, "modulo_timbro_dpc", lambda: m), \
                patch.object(CA, "timbro_snapshot", lambda: ""):
            self.assertEqual(CA.timbro_dpc()[0], "")


class FonteUfficialePrimaIlMirrorDopo(unittest.TestCase):
    def test_ufficiale_valida_il_mirror_non_si_legge(self):
        prendi, _ = fonte_finta()
        with ambiente() as (tmp, allerta):
            gira_main(ora(2026, 11, 11, 18, 30),
                      timbro_dpc=lambda: ("20261111_1540", "fonte ufficiale", []),
                      http_get_json=prendi, fetch_csv=mirror_vietato,
                      fallback_pdf_regione_lazio=lambda now: {})
            dati = json.loads(allerta.read_text(encoding="utf-8"))
            out = uscite(tmp)
            self.assertEqual(fonti_ko(tmp), "")
        self.assertEqual(out["source"], "dpc-ufficiale")
        self.assertEqual(dati["livello"], "verde")
        self.assertEqual(dati["domani"]["livello"], "gialla")
        self.assertEqual(dati["domani"]["rischi"], ["rischio idrogeologico"])
        self.assertEqual(dati["domani"]["data"], "2026-11-12")
        self.assertEqual(dati["avviso_meteo"]["tipo"], "vento")   # blocchi degli altri script intatti

    def test_dopo_mezzanotte_domani_diventa_oggi(self):
        prendi, _ = fonte_finta()
        with ambiente() as (tmp, allerta):
            gira_main(ora(2026, 11, 12, 8),
                      timbro_dpc=lambda: ("20261111_1540", "fonte ufficiale", []),
                      http_get_json=prendi, fetch_csv=mirror_vietato,
                      fallback_pdf_regione_lazio=lambda now: {})
            dati = json.loads(allerta.read_text(encoding="utf-8"))
        self.assertEqual(dati["livello"], "gialla")
        self.assertEqual(dati["titolo"], "ALLERTA GIALLA — rischio idrogeologico")
        self.assertNotIn("domani", dati)

    def test_ufficiale_muta_si_usa_il_mirror(self):
        letti = []

        def mirror(url, label):
            letti.append(label)
            if label == "oggi":
                return riga_csv("2026-11-11T14:22:59+01:00", "2026-11-11T23:59:59+01:00",
                                "2026-11-11T14:22:59+01:00",
                                "Moderata / ALLERTA ARANCIONE", "Moderata / ALLERTA ARANCIONE")
            return None
        with ambiente() as (tmp, allerta):
            gira_main(ora(2026, 11, 11, 18),
                      timbro_dpc=lambda: ("", "", ["albero ufficiale non raggiungibile"]),
                      fetch_csv=mirror, fallback_pdf_regione_lazio=lambda now: {})
            dati = json.loads(allerta.read_text(encoding="utf-8"))
            out = uscite(tmp)
            ko = fonti_ko(tmp)
        self.assertEqual(sorted(letti), ["domani", "oggi"])
        self.assertEqual(out["source"], "opendatasicilia")
        self.assertEqual(dati["livello"], "arancione")
        self.assertIn("Repository ufficiale del Dipartimento", ko)

    def test_bollettino_ufficiale_scaduto_si_usa_il_mirror(self):
        # Ultimo bollettino trovato del 9/11 (oggi 9/11, domani 10/11): l'11/11
        # alle 10 non copre più nulla, quindi si legge la riserva.
        vecchio = {
            "today": {"html_descrition": "<p>Per la giornata di oggi, lunedì 9 novembre 2026:</p>"},
            "tomorrow": {"html_descrition": "<p>Per la giornata di domani, martedì 10 novembre 2026:</p>"},
        }
        prendi, chiesti = fonte_finta(timbro="20261109_1402", bollettino=vecchio)
        letti = []

        def mirror(url, label):
            letti.append(label)
            return None
        with ambiente() as (tmp, allerta):
            gira_main(ora(2026, 11, 11, 10),
                      timbro_dpc=lambda: ("20261109_1402", "snapshot del repository", []),
                      http_get_json=prendi, fetch_csv=mirror,
                      fallback_pdf_regione_lazio=lambda now: {})
            ko = fonti_ko(tmp)
        self.assertEqual(sorted(letti), ["domani", "oggi"])
        self.assertIn("giorni già passati", ko)
        self.assertNotIn("vale il timbro", ko)
        self.assertFalse(any("topojson" in u for u in chiesti))   # carte scadute non scaricate

    def test_stesso_giorno_regione_piu_alta_vale_il_massimo(self):
        prendi, _ = fonte_finta()
        regione = {"oggi": riga_csv("2026-11-11T00:00:00+01:00", "2026-11-11T23:59:59+01:00",
                                    "2026-11-11T12:00:00+01:00",
                                    "Moderata per temporali / ALLERTA ARANCIONE", NESSUNA)}
        regione["oggi"]["avviso_temporali"] = "Moderata / ALLERTA ARANCIONE"
        with ambiente() as (tmp, allerta):
            gira_main(ora(2026, 11, 11, 18, 30),
                      timbro_dpc=lambda: ("20261111_1540", "fonte ufficiale", []),
                      http_get_json=prendi, fetch_csv=mirror_vietato,
                      fallback_pdf_regione_lazio=lambda now: regione)
            dati = json.loads(allerta.read_text(encoding="utf-8"))
            out = uscite(tmp)
        self.assertEqual(out["source"], "dpc-ufficiale+pdf-regione-lazio")
        self.assertEqual(dati["livello"], "arancione")

    def test_regione_piu_recente_supera_il_dipartimento_del_giorno_prima(self):
        # Il 12/11 alle 14 il Dipartimento ha ancora il bollettino dell'11/11
        # (domani gialla); la Regione ha pubblicato il 12/11 e dice verde: vale
        # il bollettino più recente, come prima con il mirror.
        prendi, _ = fonte_finta()
        regione = {"oggi": riga_csv("2026-11-12T00:00:00+01:00", "2026-11-12T23:59:59+01:00",
                                    "2026-11-12T12:00:00+01:00")}
        with ambiente() as (tmp, allerta):
            gira_main(ora(2026, 11, 12, 14),
                      timbro_dpc=lambda: ("20261111_1540", "fonte ufficiale", []),
                      http_get_json=prendi, fetch_csv=mirror_vietato,
                      fallback_pdf_regione_lazio=lambda now: regione)
            dati = json.loads(allerta.read_text(encoding="utf-8"))
        self.assertEqual(dati["livello"], "verde")


PRE_ALLERTA = {"livello": "gialla", "titolo": "Previsto giallo",
               "rischi": ["rischio idrogeologico"], "data": "2026-11-12"}
CARTA_DOMANI_VERDE = carta(
    zona("Bacini Costieri Sud", ["Albano Laziale", "Ariccia", "Genzano di Roma", "Velletri"]),
    nome="20261111_1540_tomorrow",
)


class PrudenzaSullaPreAllerta(unittest.TestCase):
    """Un errore di lettura non abbassa né cancella la pre-allerta pubblicata
    (revisione della PR #1841: un timeout sulla carta di domani, con la
    Regione muta, la toglieva e la segnalava come rientrata)."""

    def _gira(self, carte=None, regione=None, timbro=("20261111_1540", "fonte ufficiale", [])):
        prendi, _ = fonte_finta(carte=carte)
        letti = []

        def mirror(url, label):
            letti.append(label)
            return None    # mirror fermo o muto
        with ambiente(domani=dict(PRE_ALLERTA)) as (tmp, allerta):
            gira_main(ora(2026, 11, 11, 18, 30), timbro_dpc=lambda: timbro,
                      http_get_json=prendi, fetch_csv=mirror,
                      fallback_pdf_regione_lazio=lambda now: regione or {})
            return json.loads(allerta.read_text(encoding="utf-8")), uscite(tmp), letti, fonti_ko(tmp)

    def test_carta_di_domani_illeggibile_resta_la_pre_allerta(self):
        dati, out, letti, ko = self._gira(carte={"today": CARTA_OGGI, "tomorrow": OSError("timeout")})
        self.assertEqual(sorted(letti), ["domani", "oggi"])    # la riserva si legge
        self.assertEqual(dati["domani"], PRE_ALLERTA)
        self.assertEqual(out["sostanziale"], "false")         # niente deploy urgente né Telegram
        self.assertIn("tomorrow", ko)

    def test_regione_piu_bassa_non_abbassa_se_il_dipartimento_non_si_legge(self):
        regione = {"domani": riga_csv("2026-11-12T00:00:00+01:00", "2026-11-12T23:59:59+01:00",
                                      "2026-11-11T12:00:00+01:00")}
        dati, out, _, _ = self._gira(carte={"today": CARTA_OGGI, "tomorrow": OSError("timeout")},
                                     regione=regione)
        self.assertEqual(dati["domani"]["livello"], "gialla")
        self.assertEqual(out["sostanziale"], "false")

    def test_regione_piu_alta_vale_anche_se_il_dipartimento_non_si_legge(self):
        regione = {"domani": riga_csv("2026-11-12T00:00:00+01:00", "2026-11-12T23:59:59+01:00",
                                      "2026-11-11T12:00:00+01:00",
                                      "Moderata per rischio idrogeologico / ALLERTA ARANCIONE",
                                      "Moderata / ALLERTA ARANCIONE")}
        dati, out, _, _ = self._gira(carte={"today": CARTA_OGGI, "tomorrow": OSError("timeout")},
                                     regione=regione)
        self.assertEqual(dati["domani"]["livello"], "arancione")
        self.assertEqual(out["sostanziale"], "true")

    def test_domani_letto_verde_toglie_davvero_la_pre_allerta(self):
        dati, out, letti, _ = self._gira(carte={"today": CARTA_OGGI, "tomorrow": CARTA_DOMANI_VERDE})
        self.assertEqual(letti, [])                            # fonte ufficiale completa: niente riserva
        self.assertEqual(dati["domani"]["livello"], "verde")
        self.assertEqual(out["sostanziale"], "true")

    def test_dipartimento_muto_resta_la_pre_allerta(self):
        regione = {"oggi": riga_csv("2026-11-11T00:00:00+01:00", "2026-11-11T23:59:59+01:00",
                                    "2026-11-11T12:00:00+01:00")}
        dati, out, letti, _ = self._gira(regione=regione, timbro=("", "", ["albero non raggiungibile"]))
        self.assertEqual(sorted(letti), ["domani", "oggi"])
        self.assertEqual(dati["livello"], "verde")
        self.assertEqual(dati["domani"], PRE_ALLERTA)
        self.assertEqual(out["sostanziale"], "false")

    def test_a_mezzanotte_la_pre_allerta_di_oggi_non_si_tiene(self):
        # Il 12/11 la pre-allerta «per il 12/11» è diventata il livello di oggi:
        # anche con la carta di domani mancante non resta come pre-allerta.
        prendi, _ = fonte_finta(carte={"today": CARTA_OGGI, "tomorrow": CARTA_DOMANI})
        with ambiente(domani=dict(PRE_ALLERTA)) as (tmp, allerta):
            gira_main(ora(2026, 11, 12, 0, 5), timbro_dpc=lambda: ("20261111_1540", "fonte ufficiale", []),
                      http_get_json=prendi, fetch_csv=mirror_vietato,
                      fallback_pdf_regione_lazio=lambda now: {})
            dati = json.loads(allerta.read_text(encoding="utf-8"))
        self.assertEqual(dati["livello"], "gialla")
        self.assertNotIn("domani", dati)


class PreAllertaConLivelliDiversi(unittest.TestCase):
    """12/11/2026: domani arancione idrogeologico e gialla idraulica (Regione Lazio,
    prot. U.1143007). La barra non deve dire che l'arancione vale anche per l'idraulico."""

    def test_il_rischio_piu_basso_porta_il_suo_livello(self):
        prendi, _ = fonte_finta()
        domani = riga_csv("2026-11-12T00:00:00+01:00", "2026-11-12T23:59:59+01:00",
                          "2026-11-11T12:00:00+01:00",
                          "Moderata per rischio idrogeologico / ALLERTA ARANCIONE",
                          "Moderata / ALLERTA ARANCIONE")
        domani["avviso_idraulico"] = "Ordinaria / ALLERTA GIALLA"
        with ambiente() as (tmp, allerta):
            gira_main(ora(2026, 11, 11, 18, 30),
                      timbro_dpc=lambda: ("20261111_1540", "fonte ufficiale", []),
                      http_get_json=prendi, fetch_csv=mirror_vietato,
                      fallback_pdf_regione_lazio=lambda now: {"domani": domani})
            dati = json.loads(allerta.read_text(encoding="utf-8"))
        self.assertEqual(dati["domani"]["livello"], "arancione")
        self.assertEqual(dati["domani"]["rischi"],
                         ["rischio idrogeologico", "rischio idraulico (gialla)"])


    def test_pubblicato_con_testo_vecchio_si_riscrive(self):
        """Stesso livello, rischi scritti senza livello: la barra va riscritta."""
        prendi, _ = fonte_finta()
        domani = riga_csv("2026-11-12T00:00:00+01:00", "2026-11-12T23:59:59+01:00",
                          "2026-11-11T12:00:00+01:00",
                          "Moderata per rischio idrogeologico / ALLERTA ARANCIONE",
                          "Moderata / ALLERTA ARANCIONE")
        domani["avviso_idraulico"] = "Ordinaria / ALLERTA GIALLA"
        vecchio = {"livello": "arancione", "titolo": "Previsto arancione",
                   "rischi": ["rischio idrogeologico", "rischio idraulico"], "data": "2026-11-12"}
        with ambiente(domani=vecchio, ultimo_controllo="2026-11-11T18:28:00+01:00") as (tmp, allerta):
            gira_main(ora(2026, 11, 11, 18, 30),
                      timbro_dpc=lambda: ("20261111_1540", "fonte ufficiale", []),
                      http_get_json=prendi, fetch_csv=mirror_vietato,
                      fallback_pdf_regione_lazio=lambda now: {"domani": domani})
            dati = json.loads(allerta.read_text(encoding="utf-8"))
        self.assertEqual(dati["domani"]["rischi"],
                         ["rischio idrogeologico", "rischio idraulico (gialla)"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
