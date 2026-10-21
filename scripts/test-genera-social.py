#!/usr/bin/env python3
"""Prove delle regole che genera-social.py passa a Gemini.

Dal 21/10/2026 il prompt contiene anche la regola comune sui social
(comunicazione-social.md), senza la sezione sulla Misericordia di Ariccia: qui
si controlla che la sezione esca davvero, che il resto resti e che un titolo
cambiato nella regola venga segnalato invece di passare in silenzio.

Uso: python3 scripts/test-genera-social.py   (solo libreria standard)
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))
spec = importlib.util.spec_from_file_location("genera_social", QUI / "genera-social.py")
S = importlib.util.module_from_spec(spec)
spec.loader.exec_module(S)


class RegoleDelPrompt(unittest.TestCase):
    def test_regola_social_senza_la_misericordia(self):
        regole = S.carica_rules()
        self.assertIn("# === comunicazione-social.md ===", regole)
        for resta in ("## Tono di voce", "## Testi e didascalie",
                      "## Parole e immagini su disabilità e fragilità",
                      "## Persone nelle foto", "## Controllo prima di pubblicare"):
            self.assertIn(resta, regole)
        for esce in ("## Solo per la Misericordia di Ariccia", "Montserrat", "#003F85",
                     "Dal 1244 al fianco del prossimo"):
            self.assertNotIn(esce, regole)
        for nome in ("02-content-design-pa.md", "03-accessibility.md",
                     "06-protezione-civile-scientifica.md"):
            self.assertIn(f"# === {nome} ===", regole)

    def test_togli_sezione_fino_al_titolo_successivo(self):
        testo = ("# Regola\n\n## Prima\nuno\n\n## Da togliere\ndue\n### Dentro\ntre\n\n"
                 "## Dopo\nquattro\n")
        nuovo, trovata = S.togli_sezione(testo, "## Da togliere")
        self.assertTrue(trovata)
        self.assertEqual(nuovo, "# Regola\n\n## Prima\nuno\n\n## Dopo\nquattro\n")

    def test_titolo_cambiato_si_segnala(self):
        errori = io.StringIO()
        with patch.dict(S.SEZIONI_ESCLUSE,
                        {"comunicazione-social.md": ["## Titolo che non esiste"]}), \
                contextlib.redirect_stderr(errori):
            S.carica_rules()
        self.assertIn("non trovata", errori.getvalue())


if __name__ == "__main__":
    unittest.main(verbosity=2)
