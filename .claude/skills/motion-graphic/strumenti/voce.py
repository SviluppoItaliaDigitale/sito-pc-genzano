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
import argparse, json, re, subprocess, sys, time, urllib.parse, urllib.request, wave
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
    return re.sub(r"[A-Za-zÀ-ÿ]+", sost, testo)


def fonemi(modello):
    try:
        from piper import PiperVoice
        return PiperVoice.load(str(modello))
    except Exception as e:  # il controllo è un aiuto, non blocca la voce
        print(f"[voce] fonemi non disponibili: {e}")
        return None


DIPI = "https://www.dipionline.it/dizionario/api/trascrizione"
CACHE_DIPI = MOTION / ".cache" / "dipi.json"


def forma_base(parola):
    """Toglie gli accenti forzati per la voce (Gandòlfo → Gandolfo), tranne quello finale (città)."""
    import unicodedata
    corpo = "".join(c for c in unicodedata.normalize("NFD", parola[:-1]) if unicodedata.category(c) != "Mn")
    return unicodedata.normalize("NFC", corpo) + parola[-1:]


def dipi(parola, cache):
    """Trascrizione del DiPI (Dizionario di pronuncia italiana, Canepari), con cache."""
    parola = forma_base(parola)
    k = parola.lower()
    if k not in cache:
        try:
            req = urllib.request.Request(DIPI, data=urllib.parse.urlencode({"lemma": parola}).encode(),
                                         headers={"User-Agent": "PCGenzano-motion/1.0 (protezionecivilegenzano.it)"})
            with urllib.request.urlopen(req, timeout=20) as r:
                d = json.load(r)
            cache[k] = [] if d.get("noResults") or d.get("errorOccurred") else d.get("transcriptions", [])
            time.sleep(1)  # una richiesta al secondo: servizio gratuito
        except Exception:
            return None  # non in cache: si riprova la volta dopo
    return cache[k]


def norma(ipa):
    """Riduce le due notazioni a (vocali dall'accento in poi, vocale accentata)."""
    t = re.sub(r"\([^)]*\)", "", ipa)  # note tra parentesi: (-ó-, avv.), (hôtel)
    t = re.split(r"[,;•◆\[]", t)[0].strip().strip("/*°").lower()
    if "ˈ" not in t:
        t = t.replace("ˌ", "ˈ")  # parole atone nel DiPI: vale l'accento secondario
    for a, b in (("ʤ", "dʒ"), ("ʧ", "tʃ"), ("ʦ", "ts"), ("ʣ", "dz"), ("ɾ", "r"), ("ɪ", "i"), ("ʊ", "u"),
                 ("iʲ", "i"), ("ʲ", ""), ("ː", ""), ("ɡ", "g"), (" ", ""), (".", ""), ("ˌ", "")):
        t = t.replace(a, b)
    acc = t.rfind("ˈ")
    if acc < 0:
        return (None, "")
    coda = t[acc + 1:]
    tonica = re.search(r"[aeiouɛɔ]", coda)
    # sillabe dall'accento alla fine = gruppi vocalici, senza le semivocali (dio/djo contano uguale)
    gruppi = re.findall(r"[aeiouɛɔ]+", coda.replace("j", "").replace("w", ""))
    return (len(gruppi), tonica.group(0) if tonica else "")


def da_controllare(parola, ipa, inizio_frase=False):
    """Parola non piana o nome proprio: i casi da verificare sul vocabolario."""
    if parola[0].isupper() and not inizio_frase:
        return True
    sillabe = re.findall(r"[aeiouɛɔəɪʊ]+", ipa.replace("ː", ""))
    if len(sillabe) < 2 or "ˈ" not in ipa:
        return False
    dopo = ipa.split("ˈ", 1)[1]
    if len(re.findall(r"[aeiouɛɔəɪʊ]+", dopo)) != 2:
        return True
    # e/o accentate: aperta o chiusa cambia la parola (pèsca/pésca), si verifica il timbro
    tonica = re.search(r"[aeiouɛɔ]", dopo)
    return bool(tonica) and tonica.group(0) in "eoɛɔ"


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
    try:
        cache_dipi = json.loads(CACHE_DIPI.read_text()) if CACHE_DIPI.exists() else {}
    except ValueError:
        cache_dipi = {}
    report = []
    durate = []
    (cartella / "fonemi.txt").unlink(missing_ok=True)  # mai un report di un giro precedente
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
            for m in re.finditer(r"[A-Za-zÀ-ÿ]+", parlato):
                parola = m.group(0)
                if len(parola) < 3:  # articoli e congiunzioni: la voce li legge dentro la frase
                    continue
                inizio = not parlato[:m.start()].strip() or parlato[:m.start()].rstrip()[-1] in ".!?:"
                ipa = "".join(sum(voce_pv.phonemize(parola), []))
                verificata = parola.lower() in voci or parola.lower() in {g.lower() for g in voci.values()}
                segno = "✓" if verificata else "!" if da_controllare(parola, ipa, inizio) else " "
                nota = ""
                if segno == "!":
                    rif = dipi(parola, cache_dipi)
                    if rif:
                        n_voce, n_rif = norma(ipa), norma(rif[0])
                        if n_voce == n_rif:
                            segno, nota = "=", f"DiPI {rif[0]}"
                        else:
                            segno, nota = "≠", f"DiPI {rif[0]}  ← accento o timbro diversi: correggere"
                    elif rif == []:
                        nota = "non nel DiPI: Treccani / Wikipedia"
                    else:
                        nota = "DiPI non raggiungibile"
                report.append(f"{segno} {parola:20} {ipa:22} {nota}".rstrip())
        subprocess.run([sys.executable, "-m", "piper", "-m", str(modello),
                        "--length-scale", a.length_scale, "--sentence-silence", "0.35",
                        "-f", str(wav)], input=parlato, text=True, check=True,
                       capture_output=True)
        with wave.open(str(wav)) as w:
            d = round(w.getnframes() / w.getframerate(), 3)
        durate.append(d)
        print(f"[voce] scena {k}: {d:.2f} s  «{parlato}»")
    (cartella / "durate.json").write_text(json.dumps(durate))
    if cache_dipi:
        CACHE_DIPI.parent.mkdir(parents=True, exist_ok=True)
        CACHE_DIPI.write_text(json.dumps(cache_dipi, ensure_ascii=False))
    if report:
        (cartella / "fonemi.txt").write_text(
            "# = conferma il DiPI   ≠ il DiPI dice altro: correggere   ! da verificare a mano (Treccani, Wikipedia)   ✓ già nel lessico\n"
            + "\n".join(report) + "\n", encoding="utf-8")
        n = sum(1 for r in report if r[:1] in "!≠")
        print(f"[voce] fonemi in {(cartella / 'fonemi.txt').relative_to(ROOT)}: {n} parole da verificare o correggere")
    print(f"[voce] durate in {(cartella / 'durate.json').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
