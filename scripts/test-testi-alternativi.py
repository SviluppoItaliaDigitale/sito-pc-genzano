#!/usr/bin/env python3
"""Prove dei testi alternativi delle grafiche social (testi-alternativi.json).

Con un articolo finto in una cartella provvisoria: il generatore deve scrivere
un JSON valido e completo nei tre casi (post con una sola immagine, carosello
con citazione e sintesi, carosello con foto), con i testi presi solo da ciò che
la grafica disegna; --solo-testi-alternativi deve aggiungerlo senza toccare le
immagini e rifiutarsi se le immagini non corrispondono più all'articolo.

Uso: python3 scripts/test-testi-alternativi.py   (serve Pillow)
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

from PIL import Image

QUI = Path(__file__).resolve().parent
sys.path.insert(0, str(QUI))
import social_comune  # noqa: E402

spec = importlib.util.spec_from_file_location("genera_immagini_social",
                                              QUI / "genera-immagini-social.py")
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)

FIRMA = "Foto: Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma."


def scrivi_articolo(root: Path, slug: str, campi: list[str], corpo: str = "") -> Path:
    """Articolo finto in root/content/comunicazioni, con cover e foto vere.
    `campi` sono le righe del frontmatter."""
    immagini = root / "static" / "images"
    immagini.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (1200, 630), (0, 51, 102)).save(immagini / f"{slug}.jpg")
    for nome, colore in (("prova-foto-1.jpg", (180, 60, 40)),
                         ("prova-foto-2.jpg", (40, 120, 60))):
        Image.new("RGB", (900, 600), colore).save(immagini / nome)
    md = root / "content" / "comunicazioni" / f"{slug}.md"
    md.parent.mkdir(parents=True, exist_ok=True)
    righe = list(campi) + [f'image: "/images/{slug}.jpg"']
    md.write_text("---\n" + "\n".join(righe) + "\n---\n\n" + textwrap.dedent(corpo),
                  encoding="utf-8")
    return md


def impronte(cartella: Path) -> dict:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(cartella.glob("*.jpg"))}


class Base(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.bozze = self.root / "social-bozze"
        for p in (patch.object(G, "ROOT", self.root),
                  patch.object(G, "BOZZE_DIR", self.bozze),
                  patch.object(social_comune, "SOCIAL_BOZZE", self.bozze)):
            p.start()
            self.addCleanup(p.stop)

    def leggi_json(self, cartella: Path) -> dict:
        dati = json.loads((cartella / G.TESTI_ALTERNATIVI).read_text(encoding="utf-8"))
        nomi = sorted(p.name for p in cartella.glob("feed-*.jpg"))
        nomi.sort(key=lambda n: int(n.rsplit("-", 1)[1].split(".")[0]) if "carosello" in n else 0)
        self.assertEqual(G.controlla_testi_alternativi(dati, nomi), [])
        self.assertEqual(dati["versione"], 1)
        self.assertEqual(list(dati["feed"]), nomi, "una voce per ogni immagine del feed")
        for testo in list(dati["feed"].values()) + [dati["storia"]]:
            self.assertLessEqual(G.alt_lunghezza(testo), G.ALT_MAX)
            self.assertRegex(testo, r"[.!?…][»”\"’')\]]*$")
            self.assertNotRegex(testo.lower(), r"^(immagine|foto|fotografia) di ")
        return dati


class TreCasi(Base):
    def test_post_con_una_sola_immagine(self):
        md = scrivi_articolo(self.root, "2026-01-02-prova-singolo", [
            'title: "Prova del post singolo: «titolo» con virgolette"',
            "date: 2026-01-02",
            'description: "Descrizione di prova della storia."',
            'badge: "Informazione"',
        ])
        art = G.estrai_articolo(md)
        out = self.root / "uscita-singolo"
        G.genera_immagini(art, [("titolo", None)], out)
        self.assertTrue((out / "feed-post.jpg").is_file())
        self.assertFalse(list(out.glob("feed-carosello-*.jpg")))
        dati = self.leggi_json(out)
        self.assertEqual(list(dati["feed"]), ["feed-post.jpg"])
        self.assertEqual(
            dati["feed"]["feed-post.jpg"],
            "Grafica del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma "
            "con l'etichetta «Informazione» e il titolo "
            "«Prova del post singolo: “titolo” con virgolette».")
        self.assertIn("«Descrizione di prova della storia»", dati["storia"])

    def test_carosello_con_citazione_e_sintesi(self):
        punti = [f"Punto numero {i} della sintesi, scritto per intero e abbastanza "
                 f"lungo da occupare più righe nella slide della sintesi" for i in range(1, 7)]
        md = scrivi_articolo(self.root, "2026-01-03-prova-sintesi", [
            'title: "Prova del carosello con citazione e sintesi"',
            "date: 2026-01-03",
            'description: "Descrizione della storia."',
            'badge: "Prevenzione"',
            'social_citazione: "«Una frase forte dell\'articolo, intera.»"',
            "social_punti:",
        ] + [f'  - "{p}"' for p in punti])
        art = G.estrai_articolo(md)
        slides = G.piano_carosello(art)
        sintesi = [d for k, d in slides if k == "punti"]
        self.assertGreater(len(sintesi), 1, "la prova deve dividere la sintesi su più slide")
        out = self.root / "uscita-sintesi"
        G.genera_immagini(art, slides, out)
        dati = self.leggi_json(out)
        testi = list(dati["feed"].values())
        self.assertEqual(testi[1], "Citazione dall'articolo: "
                                   "«Una frase forte dell'articolo, intera».")
        sintesi_alt = [t for t in testi if t.startswith("In sintesi")]
        self.assertEqual(len(sintesi_alt), len(sintesi))
        self.assertTrue(sintesi_alt[0].startswith(f"In sintesi, 1 di {len(sintesi)}."))
        # Tutti i punti, interi e nell'ordine dell'articolo.
        unito = " ".join(sintesi_alt)
        posizioni = [unito.index(p + ".") for p in punti]
        self.assertEqual(posizioni, sorted(posizioni))
        self.assertIn("codice E10435833", testi[-1])

    def test_carosello_con_foto(self):
        md = scrivi_articolo(self.root, "2026-01-04-prova-foto", [
            'title: "Prova del carosello con le foto"',
            "date: 2026-01-04",
            'description: "Breve."',
            'badge: "Attività"',
        ], corpo="""
            ## Una sezione

            {{< foto src="/images/prova-foto-1.jpg"
                     alt="Foto di gruppo dei volontari davanti al mezzo 🚒"
                     caption="La squadra al rientro. Foto: Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma." >}}

            {{< foto src="/images/prova-foto-2.jpg"
                     alt="Il ponte visto dal greto del torrente"
                     caption="Il ponte. Foto: Sailko — CC BY 3.0 — via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Ponte_(1).jpg). [Fonte originale](https://commons.wikimedia.org/wiki/File:Ponte_(1).jpg)." >}}
        """)
        art = G.estrai_articolo(md)
        slides = G.piano_carosello(art)
        out = self.root / "uscita-foto"
        G.genera_immagini(art, slides, out)
        dati = self.leggi_json(out)
        foto = [t for (k, _), t in zip(slides, dati["feed"].values()) if k == "foto"]
        self.assertEqual(foto, [
            f"Gruppo dei volontari davanti al mezzo. {FIRMA}",
            "Il ponte visto dal greto del torrente. "
            "Foto: Sailko — CC BY 3.0 — via Wikimedia Commons.",
        ])
        self.assertIn("Sopra il titolo, la foto dell'articolo. Gruppo dei volontari",
                      dati["storia"])


class Regole(unittest.TestCase):
    def test_limite_a_frasi_intere(self):
        frase = "Una frase descrittiva di prova con parole normali e senza sigle. "
        testo = (frase * 30).strip()
        corto = G.alt_limita(testo)
        self.assertLessEqual(G.alt_lunghezza(corto), G.ALT_MAX)
        self.assertTrue(corto.endswith("sigle."))
        self.assertTrue(testo.startswith(corto))

    def test_una_sola_frase_troppo_lunga(self):
        testo = " ".join(["parola"] * 400) + "."
        corto = G.alt_limita(testo)
        self.assertLessEqual(G.alt_lunghezza(corto), G.ALT_MAX)
        self.assertTrue(corto.endswith("parola…"), "mai una parola a metà")

    def test_attribuzioni(self):
        casi = {
            "Testo. (Foto: profilo social ufficiale della Regione)":
                "Foto: profilo social ufficiale della Regione.",
            "Foto: ARI Sezione di Catania. I radioamatori durante l'esercitazione.":
                "Foto: ARI Sezione di Catania.",
            "La grafica ufficiale della campagna. Grafica: Dipartimento della Protezione Civile.":
                "Grafica: Dipartimento della Protezione Civile.",
            "Una didascalia senza attribuzione.": "",
            "Mappa di intensità del terremoto.": "",
            "Foto: J. Smith — CC BY 4.0 — via Wikimedia Commons.":
                "Foto: J. Smith — CC BY 4.0 — via Wikimedia Commons.",
        }
        for didascalia, attesa in casi.items():
            self.assertEqual(G.attribuzione_foto(didascalia), attesa, didascalia)

    def test_affiliazioni_dalla_slide(self):
        self.assertEqual(
            G.alt_affiliazioni(),
            "Affiliazioni e riconoscimenti del Gruppo, con i loghi: Quality Label "
            "European Solidarity Corps, codice E10435833; Coordinamento FE.PI.VOL. "
            "Volontariato Lazio; Servizio Nazionale di Protezione Civile.")

    def test_controllo_trova_gli_errori(self):
        dati = {"versione": 1, "feed": {"feed-carosello-1.jpg": "Immagine di prova"},
                "storia": "Testo ✅ con emoji."}
        problemi = " ".join(G.controlla_testi_alternativi(
            dati, ["feed-carosello-1.jpg", "feed-carosello-2.jpg"]))
        for atteso in ("non sono le immagini", "senza punto finale",
                       "immagine di", "emoji"):
            self.assertIn(atteso, problemi)


class SoloTestiAlternativi(Base):
    def prepara(self):
        md = scrivi_articolo(self.root, "2026-01-05-prova-aggiunta", [
            'title: "Prova dell\'aggiunta ai materiali già fatti"',
            "date: 2026-01-05",
            'description: "Descrizione."',
            'badge: "Formazione"',
            'social_citazione: "Una citazione."',
        ])
        art = G.estrai_articolo(md)
        cartella = self.bozze / G.slug_to_path(art["slug"])
        G.genera_immagini(art, G.piano_carosello(art), cartella)
        (cartella / G.TESTI_ALTERNATIVI).unlink()   # materiale di prima del 21/10/2026
        return md, cartella

    def test_aggiunge_senza_toccare_le_immagini(self):
        md, cartella = self.prepara()
        prima = impronte(cartella)
        scritto, motivo = G.aggiungi_testi_alternativi(md)
        self.assertTrue(scritto, motivo)
        self.assertEqual(impronte(cartella), prima)
        self.leggi_json(cartella)
        self.assertIn(G.TESTI_ALTERNATIVI, (cartella / "README.md").read_text(encoding="utf-8"))
        self.assertEqual(G.aggiungi_testi_alternativi(md), (False, "già presente"))

    def test_rifiuta_immagini_di_un_testo_vecchio(self):
        md, cartella = self.prepara()
        md.write_text(md.read_text(encoding="utf-8").replace(
            "Prova dell'aggiunta", "Titolo cambiato dopo le immagini"), encoding="utf-8")
        prima = impronte(cartella)
        scritto, motivo = G.aggiungi_testi_alternativi(md)
        self.assertFalse(scritto)
        self.assertIn("non corrisponde", motivo)
        self.assertFalse((cartella / G.TESTI_ALTERNATIVI).exists())
        self.assertEqual(impronte(cartella), prima)

    def test_facoltativo_per_il_materiale_completo(self):
        md, cartella = self.prepara()
        for nome in social_comune.TESTI:
            (cartella / f"{nome}.txt").write_text("Testo.\n", encoding="utf-8")
        self.assertFalse((cartella / G.TESTI_ALTERNATIVI).exists())
        self.assertTrue(social_comune.materiale_completo(md.stem))


if __name__ == "__main__":
    unittest.main(verbosity=2)
