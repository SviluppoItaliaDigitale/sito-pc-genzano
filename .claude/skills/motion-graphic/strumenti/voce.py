#!/usr/bin/env python3
"""Genera la voce fuori campo con Piper TTS (voce it_IT-paola-medium).

    python3 .claude/skills/motion-graphic/strumenti/voce.py <nome> [--length-scale 1.08]

Legge  motion/voce/<nome>/testi.txt   una riga per scena, nello stesso ordine
                                       di CONFIG.scene; "-" = scena senza voce.
Scrive motion/voce/<nome>/line_<k>.wav (non committati)
       motion/voce/<nome>/durate.json  durata in secondi di ogni frase (null = nessuna)

       motion/voce/<nome>/fonemi.txt   come Piper pronuncerà ogni parola (IPA, ˈ = accento)

Regole di scrittura dei testi: numeri in lettere, parole inglesi scritte a
orecchio («pàuer banc»), una frase per scena.

Pronuncia. L'audio NON si può ascoltare da qui, ma si può leggere come Piper
pronuncerà ogni parola: fonemi.txt riporta la trascrizione IPA e segnala con
«!» le parole che non sono piane (accento non sulla penultima) e i nomi propri,
cioè i casi in cui la voce sbaglia più spesso. Per quelle parole si controlla
l'accento sul Vocabolario Treccani (treccani.it/vocabolario) e, se la voce
sbaglia, si forza l'accento scrivendolo: «àncora», «sùbito», «pésca». La
correzione va nel lessico condiviso motion/voce/pronuncia.tsv, così vale per
tutte le puntate. Si chiede comunque all'utente di ascoltare.
"""
import argparse, json, re, subprocess, sys, urllib.request, wave
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MOTION = ROOT / "motion"
PIPER = MOTION / ".cache" / "piper"
BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main/it/it_IT/paola/medium/"
MODELLO = "it_IT-paola-medium.onnx"


def assicura_piper():
    try:
        import piper  # noqa: F401
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "--break-system-packages",
                        "piper-tts"], check=True)
    PIPER.mkdir(parents=True, exist_ok=True)
    for f in (MODELLO, MODELLO + ".json"):
        if not (PIPER / f).exists():
            print(f"[voce] scarico {f}")
            urllib.request.urlretrieve(BASE + f, PIPER / f)
    return PIPER / MODELLO


VOCALI = "aeiouàèéìíòóùú"


def lessico():
    """motion/voce/pronuncia.tsv: parola<TAB>grafia per la voce<TAB>fonte."""
    f = MOTION / "voce" / "pronuncia.tsv"
    voci = {}
    if f.exists():
        for riga in f.read_text(encoding="utf-8").splitlines():
            if riga.strip() and not riga.startswith("#"):
                parti = riga.split("\t")
                if len(parti) >= 2:
                    voci[parti[0].strip().lower()] = parti[1].strip()
    return voci


def applica_lessico(testo, voci):
    def sost(m):
        w = m.group(0)
        g = voci.get(w.lower())
        if not g:
            return w
        return g[0].upper() + g[1:] if w[0].isupper() else g
    return re.sub(r"[A-Za-zÀ-ÿ']+", sost, testo)


def fonemi(modello):
    try:
        from piper import PiperVoice
        return PiperVoice.load(str(modello))
    except Exception as e:  # il controllo è un aiuto, non blocca la voce
        print(f"[voce] fonemi non disponibili: {e}")
        return None


def da_controllare(parola, ipa):
    """Parola non piana o nome proprio: i casi da verificare sul vocabolario."""
    if parola[0].isupper():
        return True
    sillabe = re.findall(r"[aeiouɛɔəɪʊ]+", ipa.replace("ː", ""))
    if len(sillabe) < 3 or "ˈ" not in ipa:
        return False
    dopo = ipa.split("ˈ", 1)[1]
    return len(re.findall(r"[aeiouɛɔəɪʊ]+", dopo)) != 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nome")
    ap.add_argument("--length-scale", default="1.08")
    a = ap.parse_args()
    cartella = MOTION / "voce" / a.nome
    testi = cartella / "testi.txt"
    if not testi.exists():
        sys.exit(f"Manca {testi}: una riga per scena, '-' per le scene senza voce")
    modello = assicura_piper()
    voci = lessico()
    voce_pv = fonemi(modello)
    report = []
    durate = []
    for k, riga in enumerate(testi.read_text(encoding="utf-8").splitlines()):
        riga = riga.strip()
        wav = cartella / f"line_{k}.wav"
        if not riga or riga == "-":
            durate.append(None)
            wav.unlink(missing_ok=True)
            continue
        parlato = applica_lessico(riga, voci)
        if voce_pv:
            report.append(f"## scena {k}: {parlato}")
            for parola in re.findall(r"[A-Za-zÀ-ÿ']+", parlato):
                ipa = "".join(sum(voce_pv.phonemize(parola), []))
                segno = "!" if da_controllare(parola, ipa) else " "
                report.append(f"{segno} {parola:20} {ipa}")
        subprocess.run([sys.executable, "-m", "piper", "-m", str(modello),
                        "--length-scale", a.length_scale, "--sentence-silence", "0.35",
                        "-f", str(wav)], input=parlato, text=True, check=True,
                       capture_output=True)
        with wave.open(str(wav)) as w:
            d = round(w.getnframes() / w.getframerate(), 3)
        durate.append(d)
        print(f"[voce] scena {k}: {d:.2f} s  «{parlato}»")
    (cartella / "durate.json").write_text(json.dumps(durate))
    if report:
        (cartella / "fonemi.txt").write_text(
            "# ! = da verificare sul Vocabolario Treccani (accento non sulla penultima o nome proprio)\n"
            + "\n".join(report) + "\n", encoding="utf-8")
        n = sum(1 for r in report if r.startswith("!"))
        print(f"[voce] fonemi in {(cartella / 'fonemi.txt').relative_to(ROOT)}: {n} parole da verificare")
    print(f"[voce] durate in {(cartella / 'durate.json').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
