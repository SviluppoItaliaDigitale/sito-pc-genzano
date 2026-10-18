#!/usr/bin/env python3
"""Prove della conservazione degli allegati: integrità, ripristino e guasti."""
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "allegati", Path(__file__).with_name("immagini-meteo-release.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class AllegatiPermanenti(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.dati = b"contenuto originale del video\x00\xff"
        self.info = {"percorso": "video/prova.mp4", "byte": len(self.dati),
                     "sha256": hashlib.sha256(self.dati).hexdigest()}
        self.nome = "prova.mp4"
        self.dest = self.root / "static" / self.info["percorso"]
        for p in (patch.object(mod, "REPO_ROOT", self.root),
                  patch.object(mod, "PERMANENTI", {self.nome: self.info}),
                  patch.object(mod, "repo_slug", return_value="proprietario/sito")):
            p.start()
            self.addCleanup(p.stop)

    def test_originale_integro_non_richiede_rete(self):
        self.dest.parent.mkdir(parents=True)
        self.dest.write_bytes(self.dati)
        with patch.object(mod.urllib.request, "urlopen") as rete:
            self.assertEqual(mod.scarica_permanenti(), 0)
        rete.assert_not_called()
        self.assertEqual(self.dest.read_bytes(), self.dati)

    def test_ripristino_integrale_dalla_release(self):
        with patch.object(mod.urllib.request, "urlopen", return_value=io.BytesIO(self.dati)):
            self.assertEqual(mod.scarica_permanenti(), 0)
        self.assertEqual(self.dest.read_bytes(), self.dati)

    def test_release_irraggiungibile_ripiega_sul_sito(self):
        errore = urllib.error.HTTPError("https://github.com/asset", 503, "guasto", {}, None)
        with patch.object(mod.urllib.request, "urlopen", side_effect=[errore, io.BytesIO(self.dati)]) as rete:
            self.assertEqual(mod.scarica_permanenti(), 0)
        self.assertEqual(rete.call_count, 2)
        self.assertEqual(self.dest.read_bytes(), self.dati)

    def test_dati_troncati_bloccano_la_pubblicazione(self):
        with patch.object(mod.urllib.request, "urlopen", side_effect=[io.BytesIO(self.dati[:-1]), io.BytesIO(b"")]):
            self.assertEqual(mod.scarica_permanenti(), 1)
        self.assertFalse(self.dest.exists())
        self.assertEqual(list(self.dest.parent.iterdir()), [])

    def test_stesso_peso_ma_impronta_diversa_non_viene_accettato(self):
        errati = b"X" * len(self.dati)
        with patch.object(mod.urllib.request, "urlopen", side_effect=[io.BytesIO(errati), io.BytesIO(errati)]):
            self.assertEqual(mod.scarica_permanenti(), 1)
        self.assertFalse(self.dest.exists())

    def test_file_locale_diverso_non_viene_sovrascritto(self):
        self.dest.parent.mkdir(parents=True)
        self.dest.write_bytes(b"una nuova versione da verificare")
        with patch.object(mod.urllib.request, "urlopen") as rete:
            self.assertEqual(mod.scarica_permanenti(), 1)
        rete.assert_not_called()
        self.assertEqual(self.dest.read_bytes(), b"una nuova versione da verificare")

    def test_risposta_sovradimensionata_non_diventa_un_allegato(self):
        with patch.object(mod.urllib.request, "urlopen", return_value=io.BytesIO(self.dati + b"X")):
            self.assertFalse(mod.copia_permanente("https://esempio.it/file", self.dest, self.info))
        self.assertFalse(self.dest.exists())

    def test_download_fallito_preserva_una_copia_precedente(self):
        self.dest.parent.mkdir(parents=True)
        self.dest.write_bytes(self.dati)
        with patch.object(mod.urllib.request, "urlopen", side_effect=urllib.error.URLError("rete assente")):
            self.assertFalse(mod.copia_permanente("https://esempio.it/file", self.dest, self.info))
        self.assertEqual(self.dest.read_bytes(), self.dati)

    def test_guasto_permanenti_ferma_anche_il_comando_del_deploy(self):
        with patch.object(mod, "scarica_permanenti", return_value=1), patch.object(mod, "gh") as gh:
            self.assertEqual(mod.scarica(rigoroso=True), 1)
        gh.assert_not_called()

    def test_backup_esistente_non_viene_sovrascritto(self):
        self.dest.parent.mkdir(parents=True)
        self.dest.write_bytes(self.dati)
        risposta = json.dumps({"assets": [{"name": self.nome}]})
        with patch.object(mod, "gh", return_value=subprocess.CompletedProcess([], 0, risposta, "")) as gh, \
             patch.object(mod.urllib.request, "urlopen", return_value=io.BytesIO(self.dati)):
            self.assertEqual(mod.carica_permanenti(), 0)
        self.assertTrue(all(c.args[0] == "api" for c in gh.call_args_list))


if __name__ == "__main__":
    unittest.main()
