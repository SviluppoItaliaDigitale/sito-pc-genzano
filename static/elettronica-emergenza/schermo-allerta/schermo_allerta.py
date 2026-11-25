#!/usr/bin/env python3
"""Schermo dell'allerta meteo per la sede, con Raspberry Pi.

Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
https://www.protezionecivilegenzano.it/elettronica-emergenza/schermo-allerta/
Licenza del codice: EUPL 1.2 (testo in LICENZA-EUPL-1.2.txt).

Legge lo stato pubblico dell'allerta pubblicato dal sito del Gruppo
(/allerta-stato/index.json, dati con licenza CC BY 4.0) e lo mostra a tutto
schermo: livello, titolo, descrizione, ora dell'ultimo controllo.

Regole:
- se la lettura non riesce, lo schermo lo dice e tiene l'ultimo dato letto
  bene, con la sua ora: un errore di lettura non cambia mai il livello;
- se l'ultimo controllo del sito ha piu' di 6 ore, lo schermo passa al grigio
  e scrive che lo stato e' da confermare sul bollettino ufficiale;
- lo schermo informa e basta: non sostituisce il bollettino del Centro
  Funzionale regionale, IT-alert ne' il 112.

Solo libreria standard di Python 3 (tkinter, urllib, json, zoneinfo).
Uso:
    python3 schermo_allerta.py                 # a tutto schermo
    python3 schermo_allerta.py --finestra      # in una finestra, per provare
    python3 schermo_allerta.py --una-volta     # legge, stampa e esce (senza schermo)
    python3 schermo_allerta.py --file prova.json --una-volta
Per uscire dal tutto schermo: tasto Esc.
"""

import argparse
import configparser
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

FUSO = ZoneInfo("Europe/Rome")
CARTELLA = Path(__file__).resolve().parent

PREDEFINITI = {
    "indirizzo": "https://www.protezionecivilegenzano.it/allerta-stato/index.json",
    "intervallo_minuti": "5",
    "ore_validita": "6",
    "timeout_secondi": "20",
}

# Colori di sfondo e testo, con contrasto almeno 4,5:1 (verificato).
COLORI = {
    "verde": ("#1b5e20", "#ffffff"),
    "gialla": ("#ffd600", "#000000"),
    "arancione": ("#ff9800", "#000000"),
    "rossa": ("#b71c1c", "#ffffff"),
    "da_confermare": ("#4a4a4a", "#ffffff"),
}
NOMI_LIVELLO = {
    "verde": "Nessuna allerta",
    "gialla": "Allerta gialla",
    "arancione": "Allerta arancione",
    "rossa": "Allerta rossa",
}
GIORNI = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]
MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio",
        "agosto", "settembre", "ottobre", "novembre", "dicembre"]


class LetturaNonValida(Exception):
    """Il dato letto non ha la forma attesa."""


def carica_configurazione(percorso):
    cfg = configparser.ConfigParser()
    cfg.read_dict({"schermo": PREDEFINITI})
    if percorso and Path(percorso).is_file():
        cfg.read(percorso, encoding="utf-8")
    s = cfg["schermo"]
    return {
        "indirizzo": s.get("indirizzo"),
        "intervallo": max(1, s.getint("intervallo_minuti")) * 60,
        "ore_validita": s.getfloat("ore_validita"),
        "timeout": s.getfloat("timeout_secondi"),
    }


def data_estesa(dt):
    return f"{GIORNI[dt.weekday()]} {dt.day} {MESI[dt.month - 1]}"


def ora_italiana(testo):
    dt = datetime.fromisoformat(testo)
    if dt.tzinfo is None:
        raise LetturaNonValida("orario senza fuso")
    return dt.astimezone(FUSO)


def valida(dati):
    """Controlla la forma del dato e restituisce i soli campi che servono."""
    if not isinstance(dati, dict):
        raise LetturaNonValida("non è un oggetto JSON")
    livello = dati.get("livello")
    if livello not in NOMI_LIVELLO:
        raise LetturaNonValida(f"livello sconosciuto: {livello!r}")
    for campo in ("titolo", "descrizione", "ultimo_controllo"):
        if not isinstance(dati.get(campo), str):
            raise LetturaNonValida(f"manca il campo {campo}")
    try:
        controllo = ora_italiana(dati["ultimo_controllo"])
    except ValueError as e:
        raise LetturaNonValida(f"ultimo_controllo non leggibile: {e}") from e
    domani = dati.get("domani") if isinstance(dati.get("domani"), dict) else {}
    return {
        "livello": livello,
        "titolo": dati["titolo"].strip() or NOMI_LIVELLO[livello],
        "descrizione": dati["descrizione"].strip(),
        "ultimo_controllo": controllo,
        "emergenza": bool(dati.get("emergenza_attiva")),
        "emergenza_titolo": str(dati.get("emergenza_titolo") or "").strip(),
        "domani": domani,
    }


def leggi(cfg, file_locale=None):
    if file_locale:
        testo = Path(file_locale).read_text(encoding="utf-8")
    else:
        richiesta = urllib.request.Request(
            cfg["indirizzo"], headers={"User-Agent": "schermo-allerta-sede/1.0"})
        with urllib.request.urlopen(richiesta, timeout=cfg["timeout"]) as r:
            if r.status != 200:
                raise LetturaNonValida(f"risposta HTTP {r.status}")
            testo = r.read(200_000).decode("utf-8")
    try:
        dati = json.loads(testo)
    except json.JSONDecodeError as e:
        raise LetturaNonValida(f"JSON non valido: {e}") from e
    return valida(dati)


class Stato:
    """Ultimo dato letto bene ed esito dell'ultima lettura."""

    def __init__(self, cfg, file_locale=None):
        self.cfg = cfg
        self.file_locale = file_locale
        self.dato = None
        self.errore = None
        self.ultimo_tentativo = None

    def aggiorna(self):
        self.ultimo_tentativo = datetime.now(FUSO)
        try:
            self.dato = leggi(self.cfg, self.file_locale)
            self.errore = None
        except (OSError, urllib.error.URLError, LetturaNonValida, UnicodeDecodeError) as e:
            # Il dato in vigore non cambia: si dice solo che la lettura non è riuscita.
            self.errore = str(e) or e.__class__.__name__

    def righe(self, adesso=None):
        """Testi e colori da mostrare: (sfondo, testo, titolo, righe)."""
        adesso = adesso or datetime.now(FUSO)
        if self.dato is None:
            sfondo, colore = COLORI["da_confermare"]
            righe = ["Non riesco a leggere lo stato dell'allerta.",
                     "Consulta il bollettino del Centro Funzionale della Regione Lazio."]
            if self.errore:
                righe.append(f"Ultimo tentativo alle {self.ultimo_tentativo:%H:%M}: lettura non riuscita.")
            return sfondo, colore, "Stato dell'allerta da confermare", righe

        d = self.dato
        scaduto = adesso - d["ultimo_controllo"] > timedelta(hours=self.cfg["ore_validita"])
        # il livello vale per il giorno del controllo: dopo mezzanotte non si mostra come quello di oggi
        altro_giorno = d["ultimo_controllo"].astimezone(FUSO).date() != adesso.astimezone(FUSO).date()
        vecchio = scaduto or altro_giorno
        controllo = f"{data_estesa(d['ultimo_controllo'])} alle {d['ultimo_controllo']:%H:%M}"
        righe = []
        if vecchio:
            sfondo, colore = COLORI["da_confermare"]
            titolo = "Stato dell'allerta da confermare"
            if scaduto:
                righe.append(f"Ultimo controllo del sito: {controllo}, oltre "
                             f"{self.cfg['ore_validita']:g} ore fa.")
            else:
                righe.append(f"Ultimo controllo del sito: {controllo}, prima della mezzanotte.")
            righe.append(f"Ultimo stato letto: {NOMI_LIVELLO[d['livello']].lower()}.")
            righe.append("Consulta il bollettino del Centro Funzionale della Regione Lazio.")
        else:
            sfondo, colore = COLORI[d["livello"]]
            titolo = d["titolo"]
            oggi = f"Oggi, {data_estesa(adesso)}: {NOMI_LIVELLO[d['livello']].lower()}"
            righe.append(oggi + ".")
            if d["descrizione"]:
                righe.append(d["descrizione"])
            righe.append(f"Verificato: {controllo}.")
        dom = d["domani"]
        if dom.get("livello") in NOMI_LIVELLO and dom.get("livello") != "verde" and dom.get("data"):
            try:
                giorno = datetime.fromisoformat(dom["data"])
                rischi = ", ".join(r for r in dom.get("rischi", []) if isinstance(r, str))
                testo = f"Previsto per {data_estesa(giorno)}: {NOMI_LIVELLO[dom['livello']].lower()}"
                righe.append(testo + (f" ({rischi})." if rischi else "."))
            except ValueError:
                pass
        if d["emergenza"]:
            righe.append("Emergenza in corso" + (f": {d['emergenza_titolo']}" if d["emergenza_titolo"] else "") + ".")
        if self.errore:
            righe.append(f"Lettura non riuscita alle {self.ultimo_tentativo:%H:%M}: "
                         "resta il dato dell'ultimo controllo riuscito.")
        return sfondo, colore, titolo, righe


PIEDE = ("Fonte: protezionecivilegenzano.it, dal bollettino ufficiale. "
         "Schermo informativo, non sostituisce i canali ufficiali. In pericolo chiama il 112.")


def stampa(stato):
    sfondo, _, titolo, righe = stato.righe()
    print(titolo)
    for r in righe:
        print(" ", r)
    print(PIEDE)
    if stato.errore:
        print(f"[lettura non riuscita: {stato.errore}]", file=sys.stderr)


def schermo(stato, finestra):
    import tkinter as tk

    radice = tk.Tk()
    radice.title("Stato dell'allerta")
    if finestra:
        radice.geometry("1024x600")
    else:
        radice.geometry(f"{radice.winfo_screenwidth()}x{radice.winfo_screenheight()}+0+0")
        radice.attributes("-fullscreen", True)
        radice.config(cursor="none")
    radice.bind("<Escape>", lambda _e: radice.destroy())

    cornice = tk.Frame(radice)
    cornice.pack(fill="both", expand=True)
    etichetta_titolo = tk.Label(cornice, font=("DejaVu Sans", 64, "bold"), wraplength=1000, justify="left", anchor="w")
    etichetta_titolo.pack(fill="x", padx=48, pady=(48, 24))
    etichetta_righe = tk.Label(cornice, font=("DejaVu Sans", 30), wraplength=1000, justify="left", anchor="nw")
    etichetta_righe.pack(fill="both", expand=True, padx=48)
    etichetta_piede = tk.Label(cornice, font=("DejaVu Sans", 16), wraplength=1000, justify="left", anchor="w", text=PIEDE)
    etichetta_piede.pack(fill="x", padx=48, pady=24)

    def ridisegna():
        sfondo, colore, titolo, righe = stato.righe()
        larghezza = max(400, radice.winfo_width() - 96)
        cornice.config(bg=sfondo)
        for w in (etichetta_titolo, etichetta_righe, etichetta_piede):
            w.config(bg=sfondo, fg=colore)
        etichetta_titolo.config(text=titolo, wraplength=larghezza)
        etichetta_righe.config(text="\n\n".join(righe), wraplength=larghezza)
        etichetta_piede.config(wraplength=larghezza)
        # Caratteri piu' piccoli finche' tutto il testo entra nello schermo:
        # nessuna riga deve restare fuori, nemmeno il piede con il 112.
        altezza = radice.winfo_height()
        for scala in (1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.45, 0.4):
            etichetta_titolo.config(font=("DejaVu Sans", int(64 * scala), "bold"))
            etichetta_righe.config(font=("DejaVu Sans", max(14, int(30 * scala))))
            etichetta_piede.config(font=("DejaVu Sans", max(12, int(16 * scala))))
            radice.update_idletasks()
            occupata = (etichetta_titolo.winfo_reqheight() + etichetta_righe.winfo_reqheight()
                        + etichetta_piede.winfo_reqheight() + 48 + 24 + 48)
            if altezza <= 1 or occupata <= altezza:
                break

    def ciclo_lettura():
        stato.aggiorna()
        ridisegna()
        radice.after(stato.cfg["intervallo"] * 1000, ciclo_lettura)

    def ciclo_orologio():
        ridisegna()  # "Oggi" e le 6 ore si ricalcolano ogni minuto, anche a mezzanotte
        radice.after(60_000, ciclo_orologio)

    radice.bind("<Configure>", lambda _e: ridisegna() if _e.widget is radice else None)
    radice.after(100, ciclo_lettura)
    radice.after(60_000, ciclo_orologio)
    radice.mainloop()


def main():
    p = argparse.ArgumentParser(description="Schermo dell'allerta meteo per la sede.")
    p.add_argument("--configurazione", default=str(CARTELLA / "configurazione.ini"))
    p.add_argument("--file", help="legge un file JSON locale invece del sito (per provare)")
    p.add_argument("--finestra", action="store_true", help="in una finestra invece che a tutto schermo")
    p.add_argument("--una-volta", action="store_true", help="legge una volta, stampa il testo ed esce")
    a = p.parse_args()

    cfg = carica_configurazione(a.configurazione)
    stato = Stato(cfg, a.file)
    if a.una_volta:
        stato.aggiorna()
        stampa(stato)
        return 0 if stato.errore is None else 1
    schermo(stato, a.finestra)
    return 0


if __name__ == "__main__":
    sys.exit(main())
