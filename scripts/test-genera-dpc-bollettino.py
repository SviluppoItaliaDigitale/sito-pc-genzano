#!/usr/bin/env python3
"""Prove della scelta del bollettino DPC più recente.

Il mirror può restare fermo su un timbro ancora valido: non deve impedire di
prendere il bollettino ufficiale più nuovo, e una fonte che non risponde non
deve azzerare lo snapshot.

Uso: python3 scripts/test-genera-dpc-bollettino.py   (solo libreria standard)
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

QUI = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "genera_dpc_bollettino", QUI / "genera-dpc-bollettino.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)


def _albero(nomi, troncato=False, tipo="blob"):
    return {"truncated": troncato,
            "tree": [{"path": n, "type": tipo} for n in nomi]}


class LetturaDelleFonti(unittest.TestCase):
    def test_ora_del_bollettino_non_diventa_utc(self):
        csv = ("data_pubblicazione,zona\n"
               "2026-11-08T14:22:59+01:00,Lazi-F\n")
        self.assertEqual(S.timbro_da_csv(csv), "20261108_1422")

    def test_csv_con_virgola_dentro_un_campo(self):
        csv = ('data_pubblicazione,avviso\n'
               '2026-11-09T14:02:00+01:00,"nessuna, davvero"\n')
        self.assertEqual(S.timbro_da_csv(csv), "20261109_1402")

    def test_csv_senza_data_non_e_un_timbro(self):
        self.assertIsNone(S.timbro_da_csv("zona,avviso\nLazi-F,verde\n"))
        self.assertIsNone(S.timbro_da_csv(""))
        self.assertIsNone(S.timbro_da_csv("data_pubblicazione\nnon-una-data\n"))
        self.assertIsNone(S.timbro_da_csv("data_pubblicazione\n"))

    def test_terna_nell_albero(self):
        jsons = ["20261109_1402.json", "20261108_1422.json", "leggimi.txt",
                 "20261107_1405.json"]
        topo = ["20261109_1402_today.json", "20261109_1402_tomorrow.json",
                "20261108_1422_today.json"]
        self.assertEqual(S.timbri_completi(jsons, topo), ["20261109_1402"])

    def test_albero_troncato_non_si_usa(self):
        with self.assertRaises(RuntimeError):
            S.timbri_da_alberi(_albero(["20261109_1402.json"], troncato=True),
                               _albero(["20261109_1402_today.json",
                                        "20261109_1402_tomorrow.json"]))

    def test_timbri_nominati_dai_file_dei_commit(self):
        nomi = ["files/topojson/20261109_1402_today.json",
                "files/preview/20261108_1422.jpg", "README.md"]
        self.assertEqual(S.timbri_nei_nomi(nomi), ["20261109_1402", "20261108_1422"])


class SceltaDelPiuRecente(unittest.TestCase):
    def test_il_mirror_fermo_non_batte_la_fonte_ufficiale(self):
        candidati = [("20261109_1402", "fonte ufficiale"),
                     ("20261108_1422", "fonte ufficiale"),
                     ("20261108_1422", "mirror opendatasicilia")]
        timbro, via, by, incompleti = S.scegli_timbro(candidati, lambda t: True)
        self.assertEqual(timbro, "20261109_1402")
        self.assertEqual(via, "fonte ufficiale")
        self.assertEqual(incompleti, [])
        self.assertIn("mirror opendatasicilia", by["20261108_1422"])

    def test_fonti_concordi(self):
        candidati = [("20261109_1402", "fonte ufficiale"),
                     ("20261109_1402", "mirror opendatasicilia")]
        timbro, via, _, _ = S.scegli_timbro(candidati, lambda t: True)
        self.assertEqual(timbro, "20261109_1402")
        self.assertIn("concordi", via)
        self.assertIn("fonte ufficiale", via)
        self.assertIn("mirror opendatasicilia", via)

    def test_il_piu_nuovo_incompleto_si_salta(self):
        candidati = [("20261110_0900", "mirror opendatasicilia"),
                     ("20261109_1402", "fonte ufficiale")]
        timbro, via, _, incompleti = S.scegli_timbro(
            candidati, lambda t: t == "20261109_1402")
        self.assertEqual((timbro, via), ("20261109_1402", "fonte ufficiale"))
        self.assertEqual(incompleti, ["20261110_0900"])

    def test_nessuna_terna(self):
        timbro, via, _, incompleti = S.scegli_timbro(
            [("20261109_1402", "fonte ufficiale")], lambda t: False)
        self.assertEqual(timbro, "")
        self.assertEqual(via, "")
        self.assertEqual(incompleti, ["20261109_1402"])

    def test_non_si_torna_indietro(self):
        self.assertEqual(S.decisione("20261109_1402", "20261108_1422"), "scrivi")
        self.assertEqual(S.decisione("20261109_1402", "20261109_1402"), "invariato")
        self.assertEqual(S.decisione("20261108_1422", "20261109_1402"), "piu_vecchio")
        self.assertEqual(S.decisione("20261108_1422", "20261109_1402", manuale=True),
                         "scrivi")
        self.assertEqual(S.decisione("20261109_1402", ""), "scrivi")

    def test_il_log_dice_fonte_e_timbro_scartato(self):
        candidati = [("20261109_1402", "fonte ufficiale"),
                     ("20261108_1422", "fonte ufficiale"),
                     ("20261108_1422", "mirror opendatasicilia")]
        testo = S.messaggio_scelta(
            "20261109_1402", "fonte ufficiale", candidati, [],
            ["mirror non raggiungibile (timeout)"])
        self.assertIn("scelto 20261109_1402 (fonte ufficiale)", testo)
        self.assertIn("più vecchi: 20261108_1422 dal mirror opendatasicilia", testo)
        self.assertIn("mirror non raggiungibile", testo)


class MainConFontiFinte(unittest.TestCase):
    def _gira(self, out: Path, **patch_kw):
        buf = io.StringIO()
        with patch.object(S, "OUT", out), contextlib.redirect_stdout(buf):
            gestori = [patch.object(S, nome, valore) for nome, valore in patch_kw.items()]
            for g in gestori:
                g.start()
            try:
                codice = S.main()
            finally:
                for g in gestori:
                    g.stop()
        return codice, buf.getvalue(), (
            json.loads(out.read_text(encoding="utf-8")) if out.exists() else None)

    def test_aggiorna_oltre_il_mirror_fermo(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "dpc-bollettino.json"
            out.write_text(json.dumps({
                "stamp": "20261108_1422", "name": "vecchio"}) + "\n", encoding="utf-8")
            stato = {"commit": 0}

            def commit():
                stato["commit"] += 1
                return []

            codice, log, scritto = self._gira(
                out,
                timbri_ufficiali=lambda: ["20261109_1402", "20261108_1422"],
                timbri_dai_commit=commit,
                stamp_dal_mirror=lambda: "20261108_1422",
                terna_completa=lambda t: True,
                prendi=lambda url, json_atteso=True: {
                    "name": "Bollettino del 09 novembre 2026 ore 14:02"},
            )
        self.assertEqual(codice, 0)
        self.assertEqual(stato["commit"], 0)
        self.assertEqual(scritto["stamp"], "20261109_1402")
        self.assertEqual(scritto["name"], "Bollettino del 09 novembre 2026 ore 14:02")
        self.assertEqual(scritto["_snapshot"]["timbro_da"], "fonte ufficiale")
        self.assertIn("scelto 20261109_1402 (fonte ufficiale)", log)
        self.assertIn("più vecchi: 20261108_1422 dal mirror opendatasicilia", log)
        self.assertIn("aggiornato: 20261109_1402", log)

    def test_senza_albero_resta_il_ripiego_dei_commit(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "dpc-bollettino.json"
            codice, log, scritto = self._gira(
                out,
                timbri_ufficiali=lambda: (_ for _ in ()).throw(OSError("rete")),
                timbri_dai_commit=lambda: ["20261109_1402"],
                stamp_dal_mirror=lambda: "20261108_1422",
                terna_completa=lambda t: True,
                prendi=lambda url, json_atteso=True: {"name": "Bollettino nuovo"},
            )
        self.assertEqual(codice, 0)
        self.assertEqual(scritto["stamp"], "20261109_1402")
        self.assertIn("API dei commit", scritto["_snapshot"]["timbro_da"])
        self.assertIn("albero ufficiale non raggiungibile", log)
        self.assertIn("20261108_1422", log)

    def test_fonte_ufficiale_muta_si_usa_il_mirror(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "dpc-bollettino.json"
            codice, log, scritto = self._gira(
                out,
                timbri_ufficiali=lambda: (_ for _ in ()).throw(OSError("rete")),
                timbri_dai_commit=lambda: (_ for _ in ()).throw(OSError("quota")),
                stamp_dal_mirror=lambda: "20261109_1402",
                terna_completa=lambda t: True,
                prendi=lambda url, json_atteso=True: {"name": "Dal mirror"},
            )
        self.assertEqual(codice, 0)
        self.assertEqual(scritto["stamp"], "20261109_1402")
        self.assertEqual(scritto["_snapshot"]["timbro_da"], "mirror opendatasicilia")
        self.assertIn("API dei commit non raggiungibile", log)

    def test_entrambe_mute_lasciano_lo_snapshot(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "dpc-bollettino.json"
            prima = json.dumps({"stamp": "20261108_1422", "name": "resta"}) + "\n"
            out.write_text(prima, encoding="utf-8")
            codice, log, scritto = self._gira(
                out,
                timbri_ufficiali=lambda: (_ for _ in ()).throw(OSError("rete")),
                timbri_dai_commit=lambda: (_ for _ in ()).throw(OSError("quota")),
                stamp_dal_mirror=lambda: (_ for _ in ()).throw(OSError("mirror")),
                terna_completa=lambda t: True,
            )
            self.assertEqual(codice, 0)
            self.assertEqual(scritto["stamp"], "20261108_1422")
            self.assertEqual(out.read_text(encoding="utf-8"), prima)
            self.assertIn("nessun bollettino completo", log)

    def test_non_sostituisce_con_un_timbro_piu_vecchio(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "dpc-bollettino.json"
            prima = json.dumps({"stamp": "20261109_1402", "name": "gia nuovo"}) + "\n"
            out.write_text(prima, encoding="utf-8")
            codice, log, _ = self._gira(
                out,
                timbri_ufficiali=lambda: ["20261108_1422"],
                stamp_dal_mirror=lambda: "20261108_1422",
                terna_completa=lambda t: True,
            )
            self.assertEqual(codice, 0)
            self.assertEqual(out.read_text(encoding="utf-8"), prima)
            self.assertIn("più vecchio dello snapshot 20261109_1402", log)

    def test_invariato_non_riscrive(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "dpc-bollettino.json"
            prima = '{"stamp": "20261109_1402", "name": "uguale"}\n'
            out.write_text(prima, encoding="utf-8")
            codice, log, _ = self._gira(
                out,
                timbri_ufficiali=lambda: ["20261109_1402"],
                stamp_dal_mirror=lambda: "20261109_1402",
                terna_completa=lambda t: True,
            )
            self.assertEqual(codice, 0)
            self.assertEqual(out.read_text(encoding="utf-8"), prima)
            self.assertIn("concordi", log)
            self.assertIn("invariato", log)


if __name__ == "__main__":
    unittest.main(verbosity=2)
