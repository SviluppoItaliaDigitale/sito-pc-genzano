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


class CreditiDeiVideo(unittest.TestCase):
    CRED = "Musica: «Prova» di Autore (sito.example), CC BY 4.0."

    def test_prima_degli_hashtag(self):
        ig = "Titolo\n\nTesto.\n\nLink in bio.\n\n\n\n#Uno #Due"
        esito = S.con_crediti(ig, self.CRED)
        self.assertTrue(esito.endswith("\n\n\n\n#Uno #Due"))
        self.assertIn("Link in bio.\n\n" + self.CRED, esito)

    def test_senza_hashtag_e_senza_doppioni(self):
        esito = S.con_crediti("Testo.", self.CRED)
        self.assertEqual(esito, "Testo.\n\n" + self.CRED)
        self.assertEqual(S.con_crediti(esito, self.CRED), esito)

    def test_senza_crediti_non_cambia(self):
        self.assertEqual(S.con_crediti("Testo.\n\n#Uno", ""), "Testo.\n\n#Uno")


class LinkDelSito(unittest.TestCase):
    """Dal 15/11/2026: i link del sito scritti da Gemini tornano all'indirizzo
    canonico (post del Polesine e di Giampilieri usciti con il dominio sbagliato)."""
    U = "https://www.protezionecivilegenzano.it/comunicazioni/2026-11-14-polesine-1951-alluvione-del-po/"

    def test_dominio_con_refuso(self):
        for sbagliato in ("www.rotezionecivilegenzano.it", "www.tectionecivilegenzano.it"):
            t = S.correggi_link(f"Leggi: https://{sbagliato}/comunicazioni/2026-11-14-polesine-1951-alluvione-del-po/", self.U)
            self.assertEqual(t, "Leggi: " + self.U)

    def test_articolo_sbagliato(self):
        t = S.correggi_link("Vedi https://www.protezionecivilegenzano.it/comunicazioni/2026-07-10-altro/.", self.U)
        self.assertEqual(t, "Vedi " + self.U + ".")

    def test_hashtag_attaccato(self):
        t = S.correggi_link(self.U + "#PCGenzano #Genzano", self.U)
        self.assertEqual(t, self.U + " #PCGenzano #Genzano")

    def test_altri_link_restano(self):
        for t in ("https://www.protezionecivilegenzano.it/allerte-meteo/",
                  "https://www.comune.genzanodiroma.roma.it/notizie/",
                  "https://www.protezionecivile.gov.it/it/",
                  "[Leggi sul sito](" + self.U + ")"):
            self.assertEqual(S.correggi_link(t, self.U), t)

    def test_ancora_dei_link_esterni_intatta(self):
        corpo = "Fonte: https://example.org/manuale#sezione_2 e https://example.org/x#Genzano."
        self.assertEqual(S.correggi_link(corpo, self.U), corpo)

    def test_ancora_di_una_pagina_del_sito_intatta(self):
        corpo = "Vedi https://www.protezionecivilegenzano.it/allerte-meteo/#indice e [Leggi](" + self.U + "#cosa-fare)"
        self.assertEqual(S.correggi_link(corpo, self.U), corpo)

    def test_salva_bozze_corregge(self):
        art = {"url": self.U}
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            S.salva_bozze("2026-11-14-polesine-1951-alluvione-del-po",
                          {"facebook": "Leggi https://www.rotezionecivilegenzano.it/x/"}, art, dry_run=True)
        stampato = out.getvalue() + err.getvalue()
        self.assertIn("Leggi " + self.U, stampato)
        self.assertNotIn("www.rotezione", stampato)


if __name__ == "__main__":
    unittest.main(verbosity=2)
