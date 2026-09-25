#!/usr/bin/env python3
"""Genera la voce fuori campo con Piper TTS (voce it_IT-paola-medium).

    python3 .claude/skills/motion-graphic/strumenti/voce.py <nome> [--length-scale 1.15]

Legge  motion/voce/<nome>/testi.txt   una riga per scena, nello stesso ordine
                                       di CONFIG.scene; "-" = scena senza voce.
Scrive motion/voce/<nome>/line_<k>.wav (non committati)
       motion/voce/<nome>/durate.json  durata in secondi di ogni frase (null = nessuna)

       motion/voce/<nome>/fonemi.txt   come Piper pronuncerà ogni parola (IPA, ˈ = accento)

Regole di scrittura dei testi: numeri in lettere, parole inglesi scritte a
orecchio («pàuer banc»), una riga per scena. La punteggiatura decide le
pause (tabella PAUSE: virgola 0,32 s, due punti 0,50, punto 0,85...);
"|" = pausa di respiro senza segno scritto.

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


# Pause di lettura, in secondi, come le fa uno speaker: la voce di Piper da sola
# quasi non si ferma sulla virgola (0-0,09 s misurati), poco sui due punti
# (0,28) e per niente sui puntini. "|" = pausa di respiro senza segno scritto.
# Valori scelti a orecchio dall'utente il 24/09/2026 fra tre campioni (versione «B»).
PAUSE = {",": 0.32, ";": 0.50, ":": 0.50, "—": 0.40, "–": 0.40,
         ".": 0.85, "?": 0.85, "!": 0.85, "…": 0.90, "|": 0.45}
# Dentro la frase (virgola, due punti, trattino) la pausa si allunga solo se la
# voce fa già un respiro naturale di almeno GAP_NATURALE secondi: dove lega le
# parole, un silenzio infilato a forza suona come un inceppo (segnalato
# ascoltando il video sull'alluvione, 25/09/2026). A fine frase e con "|" si
# allunga sempre.
GAP_NATURALE = 0.06
FINE_FRASE = set(".?!…|")
SOGLIA = 500          # ampiezza sotto cui un tratto è silenzio (int16)
FINESTRA = 0.01       # 10 ms


def _energia(x, sr):
    import numpy as np
    w = int(sr * FINESTRA)
    n = len(x) // w
    return np.abs(x[:n * w].reshape(n, w)).max(axis=1)


def _sintesi(voce, testo, cfg):
    import io, numpy as np
    b = io.BytesIO()
    with wave.open(b, "wb") as w:
        voce.synthesize_wav(testo, w, cfg)
    b.seek(0)
    with wave.open(b) as w:
        sr = w.getframerate()
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).copy(), sr


def _fine_voce(x, sr):
    e = _energia(x, sr)
    attivi = [i for i, v in enumerate(e) if v > SOGLIA]
    return (attivi[-1] + 1) * FINESTRA if attivi else 0.0


def _spettro(x, sr):
    """Bande spettrali logaritmiche normalizzate, un vettore ogni 10 ms."""
    import numpy as np
    hop, n = int(sr * FINESTRA), int(sr * 0.025)
    y = x.astype(float)
    if len(y) < n:
        y = np.pad(y, (0, n - len(y)))
    fr = np.lib.stride_tricks.sliding_window_view(y, n)[::hop] * np.hanning(n)
    mag = np.abs(np.fft.rfft(fr, axis=1))
    bordi = np.unique(np.geomspace(3, mag.shape[1] - 1, 25).astype(int))
    bande = np.stack([mag[:, a:b].mean(axis=1) for a, b in zip(bordi[:-1], bordi[1:])], axis=1)
    f = np.log(bande + 1e-3)
    return f - f.mean(axis=1, keepdims=True)


def _fine_in_frase(prefisso, frase, sr):
    """Istante (s) in cui il prefisso, letto da solo, finisce dentro la frase intera.
    DTW a fine libera: il prefisso si allinea tutto a un tratto iniziale della frase."""
    import numpy as np
    a = _spettro(prefisso[: int(_fine_voce(prefisso, sr) * sr) + 1], sr)
    b = _spettro(frase, sr)
    d = np.linalg.norm(a[:, None, :] - b[None, :, :], axis=2)
    D = np.full((len(a) + 1, len(b) + 1), np.inf)
    D[0, 0] = 0
    for i in range(1, len(a) + 1):
        riga, prec = D[i], D[i - 1]
        for j in range(1, len(b) + 1):
            riga[j] = d[i - 1, j - 1] + min(prec[j - 1], prec[j], riga[j - 1])
    j = int(np.argmin(D[len(a), 1:] / (len(a) + np.arange(1, len(b) + 1))))
    return (j + 1) * FINESTRA


def confini(testo):
    """Testo da leggere (senza "|") e, per ogni segno, (posizione, pausa voluta)."""
    testo = re.sub(r"\s+", " ", testo.strip()).replace("…", "...")
    testo = re.sub(r"\s*\|\s*", "|", testo)
    pulito, out, i = "", [], 0
    while i < len(testo):
        if testo[i] == "|":
            out.append((len(pulito), PAUSE["|"], "|"))
            if pulito:
                pulito += " "
            i += 1
            continue
        if testo.startswith("...", i):
            pulito += "..."
            out.append((len(pulito), PAUSE["…"], "…"))
            i += 3
            continue
        c = testo[i]
        pulito += c
        if c in PAUSE:
            dopo = testo[i + 1:i + 2]
            # il punto dentro una sigla o un numero non è una pausa
            if not (c in ".," and dopo and not dopo.isspace() and dopo != "|"):
                out.append((len(pulito), PAUSE[c], c))
        i += 1
    fine = len(pulito.rstrip())
    return pulito.strip(), [(p, d, c) for p, d, c in out if 0 < p < fine]   # il segno finale chiude la riga


APPLICATE = []   # posizioni nel testo dove l'ultima chiamata ha allungato la pausa (per le verifiche)


def leggi_con_pause(voce, testo, cfg):
    """Sintetizza la riga intera (intonazione naturale) e allunga le pause.

    Per ogni segno si stima dove cade nell'audio (durata del testo fino al
    segno, letto da solo), si cerca lì vicino il tratto più silenzioso e lo si
    porta alla durata di PAUSE. Si inserisce solo dove l'audio è già quasi
    muto: mai dentro una parola. Restituisce (campioni, sr, rapporto)."""
    import numpy as np
    pulito, segni = confini(testo)
    x, sr = _sintesi(voce, pulito, cfg)
    e = _energia(x, sr)
    tagli, note = [], []
    APPLICATE.clear()
    for pos, voluta, segno in segni:
        forte = segno in FINE_FRASE
        prefisso, _ = _sintesi(voce, pulito[:pos], cfg)
        t = _fine_in_frase(prefisso, x, sr)
        c = int(round(t / FINESTRA))
        lo, hi = max(0, c - 8), min(len(e), c + 12)   # il silenzio comincia a ridosso della fine allineata
        # tratti di silenzio nella finestra ±0,3 s: si prende quello che COMINCIA
        # più vicino a dove finisce la voce del testo fino al segno. Non il più
        # lungo: se la voce non si ferma sulla virgola, il silenzio più lungo è
        # la chiusura di una consonante («al-ti») e la pausa finirebbe nella parola.
        migliore, run, inizio = None, 0, lo
        for j in range(lo, hi + 1):
            muto = j < hi and e[j] <= SOGLIA
            if muto:
                if run == 0:
                    inizio = j
                run += 1
            elif run:
                cand = (-abs(inizio - c), run, inizio)
                if migliore is None or cand > migliore:
                    migliore = cand
                run = 0
        if not forte and (migliore is None or migliore[1] * FINESTRA < GAP_NATURALE):
            continue   # la voce lega le parole: si lascia scorrere
        if migliore is None:
            # solo "|": si taglia nel punto di minima energia a ridosso della
            # fine allineata, con dissolvenze
            lo2, hi2 = max(0, c - 5), min(len(e), c + 6)
            j = lo2 + int(np.argmin(e[lo2:hi2]))
            if e[j] > e.max() * 0.35:
                note.append(f"nessun punto adatto dopo «{pulito[max(0,pos-12):pos]}»: pausa non inserita")
                continue
            esistente, centro = 0.0, j + 0.5
        else:
            esistente = migliore[1] * FINESTRA
            centro = migliore[2] + migliore[1] / 2
        aggiunta = max(0.0, voluta - esistente)
        if aggiunta > 0.005:
            tagli.append((int(centro * FINESTRA * sr), int(aggiunta * sr)))
            APPLICATE.append(pos)
    pezzi, ultimo = [], 0
    f = int(sr * 0.008)                      # dissolvenze di 8 ms: nessun clic sul taglio
    y = x.astype(float)
    for campione, n in sorted(tagli):
        a, b = max(ultimo, campione - f), min(len(y), campione + f)
        y[a:campione] *= np.linspace(1, 0, campione - a)
        y[campione:b] *= np.linspace(0, 1, b - campione)
        pezzi += [y[ultimo:campione], np.zeros(n)]
        ultimo = campione
    pezzi.append(y[ultimo:])
    return np.concatenate(pezzi).astype(np.int16), sr, note, pulito


DIPI = "https://www.dipionline.it/dizionario/api/trascrizione"
CACHE_DIPI = MOTION / ".cache" / "dipi.json"


def forma_base(parola):
    """Toglie gli accenti forzati per la voce (Gandòlfo → Gandolfo), tranne quello finale (città)."""
    import unicodedata
    corpo = "".join(c for c in unicodedata.normalize("NFD", parola[:-1]) if unicodedata.category(c) != "Mn")
    return unicodedata.normalize("NFC", corpo) + parola[-1:]


def dipi(parola, cache):
    """Trascrizione del DiPI (Dizionario di pronuncia italiana, Canepari), con cache.
    Il DiPI distingue le maiuscole: «Verde» a inizio frase non c'è, «verde» sì; per i nomi
    propri vale il contrario. Si prova la forma scritta e poi la minuscola."""
    parola = forma_base(parola)
    k = parola.lower()
    if k in cache:
        return cache[k]
    trovate = None
    for forma in dict.fromkeys([parola, parola.lower()]):
        try:
            req = urllib.request.Request(DIPI, data=urllib.parse.urlencode({"lemma": forma}).encode(),
                                         headers={"User-Agent": "PCGenzano-motion/1.0 (protezionecivilegenzano.it)"})
            with urllib.request.urlopen(req, timeout=20) as r:
                d = json.load(r)
            time.sleep(1)  # una richiesta al secondo: servizio gratuito
        except Exception:
            return None  # errore di rete: non si salva, si riprova la volta dopo
        if d.get("errorOccurred"):
            return None
        if not d.get("noResults") and d.get("transcriptions"):
            trovate = d["transcriptions"]
            break
    cache[k] = trovate or []
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
    ap.add_argument("--length-scale", default="1.15")
    a = ap.parse_args()
    cartella = MOTION / "voce" / a.nome
    testi = cartella / "testi.txt"
    if not testi.exists():
        sys.exit(f"Manca {testi}: una riga per scena, '-' per le scene senza voce")
    modello = assicura_piper()
    voci = lessico()
    voce_pv = fonemi(modello)
    if voce_pv is None:
        sys.exit("Piper non si carica: senza la voce non si generano le frasi")
    from piper import SynthesisConfig
    cfg = SynthesisConfig(length_scale=float(a.length_scale))
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
                if len(parola) < 3 and not parola.isupper():  # articoli e congiunzioni sì, sigle (UE, PC) no
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
        campioni, sr, note, letto = leggi_con_pause(voce_pv, parlato, cfg)
        with wave.open(str(wav), "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes(campioni.tobytes())
        d = round(len(campioni) / sr, 3)
        for n in note:
            print(f"[voce] scena {k}: {n}")
        durate.append(d)
        print(f"[voce] scena {k}: {d:.2f} s  «{letto}»")
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
