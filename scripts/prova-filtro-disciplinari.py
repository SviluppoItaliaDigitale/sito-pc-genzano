#!/usr/bin/env python3
"""Prova nel browser il filtro del catalogo dei disciplinari (/cucina-emergenza/disciplinari/).

Apre la pagina del sito costruito con Chromium e usa il filtro come lo userebbe una persona: scrive nella
casella, sceglie dai menu con il tocco e con le frecce della tastiera, preme i pulsanti, anche con lo schermo
di un telefono e di una tavoletta. Confronta ciò che resta nell'elenco con i dati di data/disciplinari.json:
ogni prodotto si deve trovare scrivendo il suo nome, ogni parola chiave dei dati deve trovare i suoi
prodotti, ogni voce dei due menu deve mostrare i prodotti giusti.

Nasce il 25/11/2026: il filtro «funzionava» per la build e per tutti i controlli, ma «olio» trovava sette
oli su cinquantuno, «formaggi» due formaggi, «salumi» e «pesce» nessun prodotto, «roma» tutta
l'Emilia-Romagna, e dal telefono dopo la scelta della regione non si vedeva nessuna reazione. Se n'è accorto
chi usa il sito, non un controllo.

Uso:
  python3 scripts/prova-filtro-disciplinari.py public
  python3 scripts/prova-filtro-disciplinari.py public --base https://www.protezionecivilegenzano.it/
  python3 scripts/prova-filtro-disciplinari.py --dal-vivo        (dopo un deploy: la pagina pubblicata)

Con la cartella il sito non si serve da un server: le richieste all'indirizzo di base ricevono i file della
cartella, tutte le altre sono fermate. Con --dal-vivo si apre la pagina pubblicata all'indirizzo di base e
l'elenco si confronta con i dati del repository: se i dati sono cambiati e non sono ancora online, la prova
non torna, ed è giusto così. Serve Playwright con Chromium.

Uscite: 0 tutto come atteso; 1 almeno una prova non torna; 2 la prova non si è potuta fare (pagina, dati o
browser mancanti).
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit

RADICE = Path(__file__).resolve().parent.parent
PAGINA = "cucina-emergenza/disciplinari/"
FILTRO_JS = RADICE / "themes" / "flavour-pcgenzano" / "static" / "js" / "disciplinari.js"

LEGGI_VISIBILI = """() => Array.from(document.querySelectorAll('.disc-voce'))
  .filter(li => !li.hidden && getComputedStyle(li).display !== 'none')
  .map(li => { const n = li.querySelector('.disc-nome'); const a = n.querySelector('a');
               return ((a ? a.firstChild : n.firstChild).textContent || '').trim(); })"""

# Le righe in vista, nell'ordine della pagina: [nome, riga delle regioni, gruppo].
LEGGI_RIGHE = """() => Array.from(document.querySelectorAll('.disc-voce'))
  .filter(li => !li.hidden && getComputedStyle(li).display !== 'none')
  .map(li => { const n = li.querySelector('.disc-nome'); const a = n.querySelector('a'); const l = li.querySelector('.disc-luogo');
               return [((a ? a.firstChild : n.firstChild).textContent || '').trim(), l ? l.textContent.trim() : '',
                       li.closest('[data-disc-gruppo]').getAttribute('data-disc-gruppo')]; })"""

# Molte ricerche in un colpo solo: per ogni coppia [parole, prodotto] scrive le parole nella casella, come fa
# chi digita (valore e evento «input»), e restituisce le coppie in cui il prodotto non è rimasto nell'elenco.
CERCA_TANTE = """coppie => { const c = document.getElementById('disc-cerca'); const leggi = %s; const perse = [];
  for (const [parole, prodotto] of coppie) {
    c.value = parole; c.dispatchEvent(new Event('input', { bubbles: true }));
    if (!leggi().includes(prodotto)) perse.push(parole + ' → ' + prodotto);
  }
  c.value = ''; c.dispatchEvent(new Event('input', { bubbles: true })); return perse; }""" % LEGGI_VISIBILI

# Un elemento è «scoperto» se sta tutto nello schermo e niente gli sta sopra nei punti in cui lo si tocca.
SCOPERTO = """([selettore, punti]) => { const e = document.querySelector(selettore);
  if (!e || e.hidden || !e.getClientRects().length) return 'non c\\'è';
  const r = e.getBoundingClientRect();
  if (r.top < 0 || r.bottom > window.innerHeight) return 'fuori dallo schermo (da ' + Math.round(r.top) + ' a ' + Math.round(r.bottom) + ' px su ' + window.innerHeight + ')';
  const y = r.top + r.height / 2;
  const dove = { sinistra: r.left + 12, centro: r.left + r.width / 2, destra: r.right - 12, testo: r.left + Math.min(r.width / 2, 90) };
  for (const punto of punti) {
    const sopra = document.elementFromPoint(dove[punto], y);
    if (!sopra || !(sopra === e || e.contains(sopra)))
      return 'coperto a ' + punto + ' da ' + (sopra ? (sopra.id ? '#' + sopra.id : (sopra.className || sopra.tagName)) : 'niente');
  }
  return ''; }"""


def norm(testo):
    testo = unicodedata.normalize("NFD", testo.lower())
    testo = "".join(c for c in testo if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", testo).strip()


def parole_vuote():
    """Le parole che la casella ignora: l'elenco VUOTE dello script della pagina, letto dal file."""
    blocco = re.search(r"var VUOTE = \{\};\s*\((.*?)\)\.split\(' '\)", FILTRO_JS.read_text(encoding="utf-8"), re.S)
    return set(" ".join(re.findall(r"'([^']*)'", blocco.group(1))).split()) if blocco else set()


class Prova:
    def __init__(self, catalogo):
        self.catalogo = catalogo
        self.voci = catalogo["voci"]
        self.parole_di_classe = {c["id"]: c.get("parole", []) for c in catalogo["classi"]}
        self.errori = []
        self.fatte = 0

    def nomi(self, condizione):
        return {v["nome"] for v in self.voci if condizione(v)}

    def classe(self, *classi):
        return self.nomi(lambda v: v["classe"] in classi)

    def regione(self, regione):
        return self.nomi(lambda v: regione in v["regioni"])

    def con_la_parola(self, parola):
        return self.nomi(lambda v: parola in v.get("parole", []) or parola in self.parole_di_classe[v["classe"]])

    def controlla(self, che_cosa, vero, dettaglio=""):
        self.fatte += 1
        if not vero:
            self.errori.append(f"{che_cosa}{': ' + str(dettaglio) if dettaglio else ''}")

    def uguali(self, che_cosa, trovati, attesi):
        trovati, attesi = set(trovati), set(attesi)
        in_piu, mancano = sorted(trovati - attesi)[:4], sorted(attesi - trovati)[:4]
        self.controlla(che_cosa, trovati == attesi,
                       f"{len(trovati)} trovati, {len(attesi)} attesi; in più {in_piu}, mancano {mancano}")


def visibili(pagina):
    return pagina.evaluate(LEGGI_VISIBILI)


def scrivi(pagina, testo):
    pagina.fill("#disc-cerca", testo)
    return visibili(pagina)


def attendi_fermo(pagina):
    """La pagina può scorrere in modo dolce: si aspetta che si fermi prima di misurare."""
    pagina.evaluate("""() => new Promise(fatto => {
        let prima = window.scrollY, uguali = 0;
        const giro = setInterval(() => {
          uguali = window.scrollY === prima ? uguali + 1 : 0;
          prima = window.scrollY;
          if (uguali >= 4) { clearInterval(giro); fatto(); }
        }, 60);
        setTimeout(() => { clearInterval(giro); fatto(); }, 3000);
    })""")


def nascosto(pagina, selettore):
    """Nascosto davvero, cioè non disegnato: l'attributo «hidden» da solo non basta, se un foglio di stile lo scavalca."""
    return pagina.evaluate("s => { const e = document.querySelector(s); return !e || getComputedStyle(e).display === 'none'; }", selettore)


def righe(pagina):
    return pagina.evaluate(LEGGI_RIGHE)


def luogo_atteso(voce, regione):
    """Con una regione in evidenza la riga dice quella, e quante altre ne ha il prodotto."""
    altre = len(voce["regioni"]) - 1
    return regione + ("" if not altre else " e un’altra regione" if altre == 1 else f" e altre {altre} regioni")


def fuori_ordine(elenco, per_nome, posto):
    """Con una regione in evidenza, in ogni gruppo: prima chi ha meno regioni e, a parità, l'ordine della pagina."""
    sbagliati, ultimo = [], {}
    for nome, _, gruppo in elenco:
        chiave = (len(per_nome[nome]["regioni"]), posto[nome])
        if gruppo in ultimo and chiave < ultimo[gruppo]:
            sbagliati.append(nome)
        ultimo[gruppo] = chiave
    return sbagliati


def conteggio(pagina, atteso):
    """Il conteggio si scrive poco dopo l'ultima scelta: si aspetta il testo atteso, non un tempo fisso, e si
    restituisce quello che c'è."""
    try:
        pagina.wait_for_function("t => document.querySelector('[data-disc=\"conteggio\"]').textContent.trim() === t",
                                 arg=atteso, timeout=3000)
    except Exception:  # il testo atteso non è arrivato: la prova lo dirà con quello che legge
        pass
    return pagina.inner_text('[data-disc="conteggio"]').strip()


def scoperto(pagina, selettore, *punti):
    return pagina.evaluate(SCOPERTO, [selettore, list(punti)])


def fuoco(pagina):
    return pagina.evaluate("document.activeElement ? (document.activeElement.id || document.activeElement.getAttribute('data-disc') || document.activeElement.tagName) : ''")


def opzioni(pagina, selettore):
    """Le voci di un menu: [valore, nome senza il numero, numero scritto fra parentesi]."""
    return pagina.evaluate("""s => Array.from(document.querySelector(s).options).filter(o => o.value).map(o => {
        const m = o.text.match(/^(.*?)\\s*\\((\\d+)\\)\\s*$/); return [o.value, m ? m[1] : o.text.trim(), m ? Number(m[2]) : -1]; })""", selettore)


def prove_della_ricerca(p, pagina):
    tutte = {v["nome"] for v in p.voci}
    tot = len(tutte)
    all_apertura = righe(pagina)
    per_nome = {v["nome"]: v for v in p.voci}
    posto = {riga[0]: i for i, riga in enumerate(all_apertura)}
    p.controlla("i nomi dei prodotti sono tutti diversi", len(per_nome) == len(p.voci) == len(posto), f"{len(per_nome)} nomi, {len(p.voci)} voci")
    p.controlla("all'apertura ogni riga elenca le regioni del prodotto",
                all(luogo == ", ".join(per_nome[nome]["regioni"]) for nome, luogo, _ in all_apertura if nome in per_nome),
                str([f"{n}: «{l}»" for n, l, _ in all_apertura if n in per_nome and l != ", ".join(per_nome[n]["regioni"])][:3]))
    p.uguali("all'apertura si vedono tutti i prodotti", visibili(pagina), tutte)
    p.controlla("il riquadro dei filtri compare", not nascosto(pagina, '[data-disc="filtri"]'))
    p.controlla("all'apertura il conteggio dice quanti prodotti ci sono", conteggio(pagina, f"{tot} prodotti.") == f"{tot} prodotti.")
    p.controlla("senza filtri non c'è il pulsante per andare all'elenco", nascosto(pagina, '[data-disc="vai"]'))
    p.controlla("senza filtri non c'è il pulsante «Mostra tutti i prodotti»", nascosto(pagina, '[data-disc="azzera"]'))
    p.controlla("senza filtri non c'è la riga dei prodotti trovati", nascosto(pagina, '[data-disc="trovati"]'))

    # Ogni prodotto si trova scrivendo il suo nome: intero, senza accenti, e con la sua prima parola.
    vuote = parole_vuote()
    p.controlla("l'elenco delle parole che la ricerca ignora si legge dallo script della pagina", len(vuote) > 20, f"{len(vuote)} parole")
    coppie = []
    for v in p.voci:
        coppie.append([v["nome"], v["nome"]])
        if norm(v["nome"]) != v["nome"].lower():
            coppie.append([norm(v["nome"]), v["nome"]])
        prima = next((w for w in norm(v["nome"]).split() if w not in vuote), "")
        if prima:
            coppie.append([prima, v["nome"]])
    perse = pagina.evaluate(CERCA_TANTE, coppie)
    p.controlla("ogni prodotto si trova scrivendo il suo nome (intero, senza accenti, con la prima parola)", not perse,
                f"{len(perse)} ricerche su {len(coppie)} non trovano il prodotto: {perse[:4]}")

    # Ogni parola chiave dei dati (campo «parole» di classi e prodotti) trova tutti i suoi prodotti.
    chiavi = sorted({w for v in p.voci for w in v.get("parole", [])} | {w for ws in p.parole_di_classe.values() for w in ws})
    p.controlla("i dati hanno parole chiave", len(chiavi) >= 20, f"{len(chiavi)} parole")
    perse = pagina.evaluate(CERCA_TANTE, [[w, nome] for w in chiavi for nome in sorted(p.con_la_parola(w))])
    p.controlla("ogni parola chiave dei dati trova tutti i suoi prodotti", not perse, f"{len(perse)} non trovati: {perse[:4]}")

    # Il tipo di prodotto scritto a parole: tutta la classe, e niente delle altre.
    for parola, classi, estranee in (
        ("olio", ("oli",), ("formaggi", "salumi")),
        ("formaggi", ("formaggi",), ("oli", "salumi")),
        ("formaggio", ("formaggi",), ("oli", "salumi")),
        ("salumi", ("salumi",), ("formaggi", "oli")),
        ("pesce", ("pesce",), ("ortofrutta", "formaggi")),
        ("pasta", ("pasta",), ("formaggi", "ortofrutta")),
        ("carne", ("carni-fresche",), ("formaggi", "oli")),
    ):
        visti = set(scrivi(pagina, parola))
        p.controlla(f"«{parola}» trova tutti i prodotti del suo tipo", p.classe(*classi) <= visti,
                    f"mancano {sorted(p.classe(*classi) - visti)[:4]}")
        p.controlla(f"«{parola}» non trova prodotti di altri tipi", not (p.classe(*estranee) & visti),
                    f"in più {sorted(p.classe(*estranee) & visti)[:4]}")
    for frase in ("olio di oliva", "olio d'oliva", "olio extravergine di oliva", "Olio Extravergine d’Oliva"):
        p.uguali(f"«{frase}» trova gli oli, tutti e solo quelli", scrivi(pagina, frase), p.classe("oli"))
    p.controlla("«olive» trova le olive da tavola e nessun olio",
                "Oliva di Gaeta" in (visti := set(scrivi(pagina, "olive"))) and not (p.classe("oli") & visti),
                f"{len(visti)} trovati")

    # Parole di tutti i giorni che nel nome non ci sono.
    for parola in ("legumi", "agrumi", "cereali", "spezie"):
        attesi = p.con_la_parola(parola)
        p.controlla(f"i dati hanno prodotti con la parola «{parola}»", len(attesi) >= 3)
        p.uguali(f"«{parola}» trova i prodotti che hanno quella parola nei dati", scrivi(pagina, parola), attesi)
    p.controlla("«maiale» trova la Cinta Senese", "Cinta Senese" in scrivi(pagina, "maiale"))
    p.uguali("«cozze» trova la Cozza di Scardovari", scrivi(pagina, "cozze"), {"Cozza di Scardovari"})
    p.controlla("«alici» trova le acciughe e la colatura",
                {"Acciughe sotto sale del Mar Ligure", "Colatura di alici di Cetara"} <= set(scrivi(pagina, "alici")))
    p.uguali("«ricette» trova le ricette tradizionali", scrivi(pagina, "ricette"), p.con_la_parola("ricetta"))
    p.controlla("i dati hanno almeno due ricette tradizionali", len(p.con_la_parola("ricetta")) >= 2)

    # Mai un pezzo in mezzo alla parola.
    visti = set(scrivi(pagina, "roma"))
    p.controlla("«roma» trova i prodotti romani", {"Pecorino Romano", "Abbacchio Romano", "Ricotta Romana", "Olio di Roma"} <= visti)
    p.controlla("«roma» non trova l'Emilia-Romagna",
                not ({"Parmigiano Reggiano", "Mortadella Bologna", "Prosciutto di Parma", "Coppia Ferrarese"} & visti))
    p.controlla("«roma»: ogni prodotto trovato ha una parola del nome che comincia così",
                all(any(parola.startswith("roma") for parola in norm(nome).split()) for nome in visti),
                str(sorted(n for n in visti if not any(w.startswith("roma") for w in norm(n).split()))[:4]))
    visti = set(scrivi(pagina, "pane"))
    p.controlla("«pane» trova il pane, anche quello che non ha «pane» nel nome",
                {"Pane casareccio di Genzano", "Pane di Altamura", "Coppia Ferrarese", "Pagnotta del Dittaino"} <= visti)
    p.controlla("«pane» non trova Valli Trapanesi né la pancetta", not ({"Valli Trapanesi", "Pancetta Piacentina"} & visti))
    p.uguali("«pane di Genzano» trova il pane di Genzano", scrivi(pagina, "pane di Genzano"), {"Pane casareccio di Genzano"})
    p.uguali("«porchetta di Ariccia»", scrivi(pagina, "porchetta di Ariccia"), {"Porchetta di Ariccia"})

    # Regioni: parola intera, anche in due parole e con le parole generiche intorno.
    p.uguali("«lazio» trova i prodotti del Lazio", scrivi(pagina, "lazio"), p.regione("Lazio"))
    p.uguali("«emilia romagna» trova i prodotti dell'Emilia-Romagna", scrivi(pagina, "emilia romagna"), p.regione("Emilia-Romagna"))
    p.uguali("«prodotti tipici dell'Umbria» trova i prodotti dell'Umbria", scrivi(pagina, "prodotti tipici dell'Umbria"), p.regione("Umbria"))
    p.controlla("«trentino» trova i prodotti della Provincia autonoma di Trento",
                p.regione("Provincia autonoma di Trento") <= set(scrivi(pagina, "trentino")))
    p.uguali("«dop lazio» trova i prodotti DOP del Lazio", scrivi(pagina, "dop lazio"),
             p.nomi(lambda v: v["tipo"] == "DOP" and "Lazio" in v["regioni"]))
    p.uguali("«stg» trova le specialità tradizionali garantite", scrivi(pagina, "stg"), p.nomi(lambda v: v["tipo"] == "STG"))

    # Più parole, in qualunque ordine, con articoli e preposizioni.
    p.uguali("«pecorino romano»", scrivi(pagina, "pecorino romano"), {"Pecorino Romano"})
    p.controlla("un solo prodotto: il conteggio è al singolare", conteggio(pagina, f"1 prodotto su {tot}.") == f"1 prodotto su {tot}.",
                pagina.inner_text('[data-disc="conteggio"]'))
    p.controlla("un solo prodotto: la riga dei trovati e il pulsante sono al singolare",
                pagina.inner_text('[data-disc="trovati"]').startswith("1 prodotto trovato.")
                and pagina.inner_text('[data-disc="vai"]').strip() == "Vai al prodotto trovato")
    p.uguali("«romano pecorino»", scrivi(pagina, "romano pecorino"), {"Pecorino Romano"})
    p.uguali("«prosciutto di parma»", scrivi(pagina, "prosciutto di parma"), {"Prosciutto di Parma"})
    p.uguali("«mozzarella bufala»", scrivi(pagina, "mozzarella bufala"), {"Mozzarella di Bufala Campana"})
    # Plurali, luoghi, accenti e apostrofi del telefono.
    p.uguali("«lenticchie» trova le lenticchie", scrivi(pagina, "lenticchie"), p.nomi(lambda v: v["nome"].startswith("Lenticchia")))
    p.controlla("«Amatrice» trova l'Amatriciana e il Prosciutto Amatriciano",
                {"Amatriciana tradizionale", "Prosciutto Amatriciano"} <= set(scrivi(pagina, "Amatrice")))
    p.controlla("«dell’alto» con l'apostrofo curvo trova la Patata dell'Alto Viterbese",
                "Patata dell'Alto Viterbese" in scrivi(pagina, "dell’alto"))
    p.controlla("«PECORINO» in maiuscolo vale come in minuscolo", len(scrivi(pagina, "PECORINO")) == len(scrivi(pagina, "pecorino")) >= 5)
    con_accento = p.nomi(lambda v: "Canicattì" in v["nome"])
    p.controlla("i dati hanno un prodotto di Canicattì", len(con_accento) == 1)
    p.uguali("«canicattì» con l'accento", scrivi(pagina, "canicattì"), con_accento)
    p.uguali("«canicatti» senza l'accento", scrivi(pagina, "canicatti"), con_accento)

    # Le ricette STG con la regione della loro tradizione.
    p.controlla("l'Amatriciana tradizionale compare fra i prodotti del Lazio", "Amatriciana tradizionale" in p.regione("Lazio"))

    # Solo parole che la ricerca ignora: l'elenco resta intero, e la pagina lo dice.
    for generica in ("prodotti tipici", "di", "i prodotti tipici della"):
        p.uguali(f"«{generica}» da solo lascia tutti i prodotti", scrivi(pagina, generica), tutte)
    atteso = f"{tot} prodotti. Le parole scritte non restringono l’elenco."
    p.controlla("con sole parole generiche il conteggio dice che l'elenco non si restringe", conteggio(pagina, atteso) == atteso,
                pagina.inner_text('[data-disc="conteggio"]'))
    p.controlla("con sole parole generiche la riga in cima all'elenco lo spiega",
                not nascosto(pagina, '[data-disc="trovati"]') and "non restringono" in pagina.inner_text('[data-disc="trovati"]'))
    p.controlla("con sole parole generiche c'è «Mostra tutti i prodotti» e non il pulsante dei trovati",
                not nascosto(pagina, '[data-disc="azzera"]') and nascosto(pagina, '[data-disc="vai"]'))
    pagina.press("#disc-cerca", "Enter")
    p.controlla("con sole parole generiche l'invio porta alla spiegazione", fuoco(pagina) == "disc-trovati", fuoco(pagina))
    pagina.click('[data-disc="azzera"]')
    p.controlla("«Mostra tutti i prodotti» svuota la casella e riporta lì il fuoco",
                pagina.input_value("#disc-cerca") == "" and fuoco(pagina) == "disc-cerca", fuoco(pagina))

    # Titoli dei gruppi e voci dell'indice: restano solo quelli con prodotti.
    scrivi(pagina, "olio")
    p.controlla("con «olio» il titolo «Formaggi» sparisce", nascosto(pagina, "#disc-formaggi"))
    p.controlla("con «olio» il titolo «Oli e grassi» resta", not nascosto(pagina, "#disc-oli"))
    voce_indice = "s => { const a = document.querySelector('a[href=\"' + s + '\"]'); const li = a && a.closest('li'); return li ? (li.hidden ? 'nascosta' : 'in vista') : 'manca'; }"
    p.controlla("con «olio» la voce «Formaggi» dell'indice sparisce", pagina.evaluate(voce_indice, "#disc-formaggi") == "nascosta",
                pagina.evaluate(voce_indice, "#disc-formaggi"))
    p.controlla("con «olio» la voce «Oli e grassi» dell'indice resta", pagina.evaluate(voce_indice, "#disc-oli") == "in vista",
                pagina.evaluate(voce_indice, "#disc-oli"))

    # Nessun risultato.
    p.uguali("una parola che non esiste non trova nulla", scrivi(pagina, "zzzz"), set())
    p.controlla("senza risultati compare il messaggio", not nascosto(pagina, '[data-disc="nessuno"]'))
    p.controlla("senza risultati non c'è il pulsante per andare all'elenco", nascosto(pagina, '[data-disc="vai"]'))
    p.controlla("senza risultati il conteggio lo dice",
                conteggio(pagina, "Nessun prodotto per questa ricerca.") == "Nessun prodotto per questa ricerca.")
    pagina.press("#disc-cerca", "Enter")
    p.controlla("senza risultati l'invio porta al messaggio", fuoco(pagina) == "nessuno", fuoco(pagina))
    p.controlla("senza risultati il messaggio dice quale parola non è in nessun prodotto",
                "nessun prodotto ha la parola «zzzz»" in pagina.inner_text('[data-disc="nessuno"]'), pagina.inner_text('[data-disc="nessuno"]'))
    p.uguali("«vino birra» non trova nulla", scrivi(pagina, "vino birra"), set())
    messaggio = pagina.inner_text('[data-disc="nessuno"]')
    p.controlla("«vino birra»: il messaggio nomina tutte e due le parole", "queste parole: «vino», «birra»" in messaggio, messaggio)
    for frase in ("prosciutto crudo", "pecorino parma"):
        p.uguali(f"«{frase}»: due parole che ci sono, ma mai nello stesso prodotto", scrivi(pagina, frase), set())
        messaggio = pagina.inner_text('[data-disc="nessuno"]')
        p.controlla(f"«{frase}»: il messaggio dice che le parole non stanno insieme e non dà la colpa a una",
                    "mai nello stesso prodotto" in messaggio and "nessun prodotto ha" not in messaggio, messaggio)
    # Una parola che c'è, ma non nella regione scelta; una regione e un tipo che insieme non hanno prodotti.
    valori = {nome: valore for valore, nome, _ in opzioni(pagina, "#disc-regione")}
    senza_pecorino = next(r for r in sorted(valori) if not any("pecorino" in norm(n).split() for n in p.regione(r)))
    pagina.select_option("#disc-regione", valori[senza_pecorino])
    p.uguali(f"«pecorino» con la regione {senza_pecorino} non trova nulla", scrivi(pagina, "pecorino"), set())
    messaggio = pagina.inner_text('[data-disc="nessuno"]')
    p.controlla("il messaggio dice che i prodotti ci sono, ma non con la regione scelta",
                "ma non con la regione o il tipo scelti" in messaggio, messaggio)
    scrivi(pagina, "")
    gruppi_dati = p.catalogo["gruppi"]
    vuota = next(((r, g) for r in sorted(valori) for g in gruppi_dati if not (p.regione(r) & p.classe(*g["classi"]))), None)
    p.controlla("i dati hanno una regione senza prodotti di un certo tipo", vuota is not None)
    if vuota:
        pagina.select_option("#disc-regione", valori[vuota[0]])
        pagina.select_option("#disc-gruppo", vuota[1]["id"])
        p.uguali(f"{vuota[0]} e «{vuota[1]['id']}» insieme non hanno prodotti", visibili(pagina), set())
        messaggio = pagina.inner_text('[data-disc="nessuno"]')
        p.controlla("il messaggio dice che nella regione non ci sono prodotti di quel tipo",
                    "Nella regione scelta non ci sono prodotti di questo tipo." in messaggio, messaggio)
    pagina.select_option("#disc-regione", "")
    pagina.select_option("#disc-gruppo", "")

    # I due menu, voce per voce: i prodotti giusti e il numero scritto accanto al nome.
    scrivi(pagina, "")
    regioni = opzioni(pagina, "#disc-regione")
    p.uguali("il menu delle regioni ha tutte le regioni dei dati", [nome for _, nome, _ in regioni],
             {r for v in p.voci for r in v["regioni"]})
    sbagliate, righe_sbagliate, ordini_sbagliati = [], [], []
    for valore, nome, quanti in regioni:
        pagina.select_option("#disc-regione", valore)
        elenco = righe(pagina)
        visti = {riga[0] for riga in elenco}
        if visti != p.regione(nome) or quanti != len(visti):
            sbagliate.append(f"{nome}: {len(visti)} in elenco, {len(p.regione(nome))} nei dati, {quanti} nel menu")
            continue
        righe_sbagliate += [f"{nome}, {n}: «{l}»" for n, l, _ in elenco if l != luogo_atteso(per_nome[n], nome)]
        ordini_sbagliati += [f"{nome}: {n}" for n in fuori_ordine(elenco, per_nome, posto)]
    p.controlla("ogni regione del menu mostra i suoi prodotti e il numero giusto", not sbagliate, "; ".join(sbagliate[:4]))
    p.controlla("con una regione scelta ogni riga dice quella regione e quante altre ne ha il prodotto, non l'elenco di tutte",
                not righe_sbagliate, f"{len(righe_sbagliate)} righe: {righe_sbagliate[:3]}")
    p.controlla("con una regione scelta, in ogni gruppo vengono prima i prodotti di quella sola regione, poi quelli con più regioni",
                not ordini_sbagliati, f"{len(ordini_sbagliati)} fuori posto: {ordini_sbagliati[:4]}")
    pagina.select_option("#disc-regione", "")
    p.controlla("tolta la regione, righe e ordine tornano quelli della pagina", righe(pagina) == all_apertura,
                str([a for a, b in zip(righe(pagina), all_apertura) if a != b][:2]))

    # La regione scritta nella casella vale come quella scelta dal menu.
    for scritta, nome in (("lazio", "Lazio"), ("emilia romagna", "Emilia-Romagna"), ("prodotti della Valle d'Aosta", "Valle d'Aosta")):
        scrivi(pagina, scritta)
        elenco = righe(pagina)
        p.uguali(f"«{scritta}» scritto nella casella trova i prodotti di quella regione", [riga[0] for riga in elenco], p.regione(nome))
        p.controlla(f"«{scritta}» scritto nella casella: le righe dicono {nome} e quante altre regioni",
                    all(l == luogo_atteso(per_nome[n], nome) for n, l, _ in elenco if n in per_nome),
                    str([f"{n}: «{l}»" for n, l, _ in elenco if n in per_nome and l != luogo_atteso(per_nome[n], nome)][:3]))
        p.controlla(f"«{scritta}» scritto nella casella: prima i prodotti con meno regioni",
                    not fuori_ordine(elenco, per_nome, posto), str(fuori_ordine(elenco, per_nome, posto)[:4]))
    scrivi(pagina, "pecorino")
    p.controlla("una parola che non è una regione lascia nelle righe tutte le regioni del prodotto",
                all(l == ", ".join(per_nome[n]["regioni"]) for n, l, _ in righe(pagina)),
                str([f"{n}: «{l}»" for n, l, _ in righe(pagina) if l != ", ".join(per_nome[n]["regioni"])][:3]))
    scrivi(pagina, "")
    p.controlla("svuotata la casella, righe e ordine tornano quelli della pagina", righe(pagina) == all_apertura)
    gruppi = {g["id"]: g for g in p.catalogo["gruppi"]}
    tipi = opzioni(pagina, "#disc-gruppo")
    p.uguali("il menu dei tipi ha tutti i gruppi dei dati", [valore for valore, _, _ in tipi], set(gruppi))
    sbagliati = []
    for valore, nome, _ in tipi:  # il menu dei tipi non scrive il numero accanto al nome
        pagina.select_option("#disc-gruppo", valore)
        visti, attesi = set(visibili(pagina)), p.classe(*gruppi.get(valore, {}).get("classi", []))
        if visti != attesi or not visti:
            sbagliati.append(f"{nome}: {len(visti)} in elenco, {len(attesi)} nei dati")
    p.controlla("ogni tipo del menu mostra i suoi prodotti", not sbagliati, "; ".join(sbagliati[:4]))
    pagina.select_option("#disc-gruppo", "")

    # Menu, indirizzo, riga dei trovati, pulsanti.
    pagina.evaluate("window.scrollTo(0, 0)")
    pagina.evaluate("""() => { const r = document.querySelector('[data-disc="filtri"]').getBoundingClientRect();
                               window.scrollBy({ top: r.top - 120, left: 0, behavior: 'instant' }); }""")
    prima = pagina.evaluate("window.scrollY")
    pagina.select_option("#disc-regione", "lazio")
    p.uguali("regione Lazio dal menu", visibili(pagina), p.regione("Lazio"))
    p.controlla("se conteggio e pulsanti sono già in vista, la scelta dal menu non sposta la pagina",
                pagina.evaluate("window.scrollY") == prima, f"da {prima} a {pagina.evaluate('window.scrollY')} px")
    p.controlla("la scelta resta nell'indirizzo", "regione=lazio" in pagina.url, pagina.url)
    trovati = pagina.inner_text('[data-disc="trovati"]')
    p.controlla("la riga dei trovati dice quanti sono e quale regione",
                f"{len(p.regione('Lazio'))} prodotti trovati." in trovati and "Regione: Lazio." in trovati, trovati)
    soli = len([n for n in p.regione("Lazio") if per_nome[n]["regioni"] == ["Lazio"]])
    condivisi = len(p.regione("Lazio")) - soli
    p.controlla("la riga dei trovati spiega l'ordine: prima i prodotti solo di questa regione, poi gli altri",
                f"Per primi i prodotti solo di questa regione ({soli}), poi quelli che ne hanno anche altre ({condivisi})." in trovati, trovati)
    p.controlla("il pulsante per andare all'elenco dice quanti sono",
                pagina.inner_text('[data-disc="vai"]').strip() == f"Vai ai {len(p.regione('Lazio'))} prodotti trovati")
    pagina.select_option("#disc-gruppo", "salumi")
    p.uguali("regione Lazio e tipo salumi", visibili(pagina), p.regione("Lazio") & p.classe("salumi"))
    p.controlla("la riga dei trovati dice anche il tipo", "Tipo di prodotto: Salumi" in pagina.inner_text('[data-disc="trovati"]'))
    pagina.click('[data-disc="vai"]')
    p.controlla("il pulsante porta il fuoco sulla riga dei trovati", fuoco(pagina) == "disc-trovati", fuoco(pagina))
    attendi_fermo(pagina)
    alto = pagina.evaluate("document.getElementById('disc-trovati').getBoundingClientRect().top")
    p.controlla("dopo il pulsante la riga dei trovati è in vista, sotto la testata", 60 <= alto <= 260, f"a {alto:.0f} px dall'alto")
    pagina.click('[data-disc="azzera"]')
    p.uguali("«Mostra tutti i prodotti» rimette tutto", visibili(pagina), tutte)
    p.controlla("dopo «Mostra tutti i prodotti» l'indirizzo non ha più filtri",
                "regione=" not in pagina.url and "tipo=" not in pagina.url and "q=" not in pagina.url, pagina.url)
    p.controlla("dopo «Mostra tutti i prodotti» spariscono riga e pulsanti",
                nascosto(pagina, '[data-disc="trovati"]') and nascosto(pagina, '[data-disc="vai"]') and nascosto(pagina, '[data-disc="azzera"]'))

    # Le frecce della tastiera sul menu: l'elenco segue ogni scelta, il fuoco resta sul menu.
    pagina.focus("#disc-regione")
    seguite = []
    for _ in range(4):
        pagina.keyboard.press("ArrowDown")
        scelta = pagina.evaluate("(() => { const s = document.getElementById('disc-regione'); return s.options[s.selectedIndex].text.replace(/\\s*\\(\\d+\\)\\s*$/, ''); })()")
        seguite.append(set(visibili(pagina)) == p.regione(scelta) and fuoco(pagina) == "disc-regione")
    p.controlla("con le frecce della tastiera l'elenco segue ogni regione e il fuoco resta sul menu", all(seguite), str(seguite))
    pagina.select_option("#disc-regione", "")

    # L'invio della tastiera porta all'elenco.
    scrivi(pagina, "olio")
    pagina.press("#disc-cerca", "Enter")
    p.controlla("l'invio porta il fuoco sulla riga dei trovati", fuoco(pagina) == "disc-trovati", fuoco(pagina))


def prove_dall_indirizzo(p, pagina, indirizzo):
    tutte = {v["nome"] for v in p.voci}
    gruppi = {g["id"]: g for g in p.catalogo["gruppi"]}

    def apri(coda):
        pagina.goto(indirizzo + coda, wait_until="load")
        pagina.wait_for_selector('[data-disc="filtri"]:not([hidden])')

    apri("?q=olio&regione=lazio")
    p.uguali("un indirizzo con parole e regione riapre l'elenco filtrato", visibili(pagina), p.classe("oli") & p.regione("Lazio"))
    p.controlla("un indirizzo con i filtri riempie casella e menu",
                pagina.input_value("#disc-cerca") == "olio" and pagina.input_value("#disc-regione") == "lazio")
    p.controlla("un indirizzo con i filtri mostra subito la riga dei trovati e il pulsante",
                not nascosto(pagina, '[data-disc="trovati"]') and not nascosto(pagina, '[data-disc="vai"]'))
    apri("?tipo=formaggi")
    p.uguali("un indirizzo con il tipo riapre quel tipo", visibili(pagina), p.classe(*gruppi["formaggi"]["classi"]))
    p.controlla("un indirizzo con il tipo sceglie la voce del menu", pagina.input_value("#disc-gruppo") == "formaggi")
    apri("?regione=atlantide&tipo=draghi")
    p.uguali("un indirizzo con valori che non esistono mostra tutti i prodotti", visibili(pagina), tutte)
    p.controlla("un indirizzo con valori che non esistono lascia i menu vuoti",
                pagina.input_value("#disc-regione") == "" and pagina.input_value("#disc-gruppo") == "")


def prove_schermo_piccolo(p, pagina, indirizzo, schermo):
    """Telefono e tavoletta: dopo una scelta dal menu il conteggio e i pulsanti devono essere in vista e
    scoperti (la barra in basso, la striscia dei cookie e i pulsanti flottanti non li coprono); il pulsante
    porta all'elenco. La barra in basso e la striscia dei cookie devono esserci, altrimenti la prova non prova."""
    pagina.goto(indirizzo, wait_until="load")
    pagina.wait_for_selector('[data-disc="filtri"]:not([hidden])')
    try:
        pagina.wait_for_function("(() => { const e = document.getElementById('cookie-banner'); return e && e.getClientRects().length > 0; })()", timeout=5000)
    except Exception:
        pass
    in_vista = pagina.evaluate("""() => ['.bottom-nav', '#cookie-banner', '#sos-button', '#a11yToolbarOpen'].filter(s => {
        const e = document.querySelector(s); return e && e.getClientRects().length > 0 && getComputedStyle(e).visibility !== 'hidden'; })""")
    p.controlla(f"{schermo}: ci sono la barra in basso, la striscia dei cookie e i pulsanti flottanti, come alla prima visita",
                len(in_vista) == 4, f"in vista solo {in_vista}")
    # Il riquadro a un terzo dello schermo, come quando ci si arriva scorrendo: conteggio e pulsanti finiscono in basso.
    pagina.evaluate("""() => { const r = document.querySelector('[data-disc="filtri"]').getBoundingClientRect();
                               window.scrollBy({ top: r.top - window.innerHeight * 0.34, left: 0, behavior: 'instant' }); }""")
    attendi_fermo(pagina)
    pagina.select_option("#disc-regione", "lazio")
    attendi_fermo(pagina)
    for che_cosa, selettore, punti in (("il conteggio", '[data-disc="conteggio"]', ("sinistra", "testo")),
                                       ("il pulsante dei trovati", '[data-disc="vai"]', ("sinistra", "centro", "destra")),
                                       ("«Mostra tutti i prodotti»", '[data-disc="azzera"]', ("sinistra", "centro", "destra"))):
        stato = scoperto(pagina, selettore, *punti)
        p.controlla(f"{schermo}: dopo la scelta della regione {che_cosa} è in vista e scoperto", not stato, stato)
    menu = pagina.evaluate("document.getElementById('disc-regione').getBoundingClientRect().top")
    p.controlla(f"{schermo}: il menu appena usato resta nello schermo", menu >= 0, f"a {menu:.0f} px dall'alto")
    p.controlla(f"{schermo}: la scelta dal menu non sposta il fuoco", fuoco(pagina) in ("disc-regione", "BODY"), fuoco(pagina))
    p.controlla(f"{schermo}: la pagina non è più larga dello schermo",
                not pagina.evaluate("document.documentElement.scrollWidth > window.innerWidth + 1"))
    p.uguali(f"{schermo}: regione Lazio dal menu", visibili(pagina), p.regione("Lazio"))
    # Altre scelte di fila, come con le frecce: la pagina non deve ballare né nascondere di nuovo l'esito.
    for valore in ("umbria", "sicilia", "lazio"):
        pagina.select_option("#disc-regione", valore)
    attendi_fermo(pagina)
    stato = scoperto(pagina, '[data-disc="vai"]', "sinistra", "centro", "destra")
    p.controlla(f"{schermo}: dopo più scelte di fila il pulsante dei trovati resta in vista e scoperto", not stato, stato)
    pagina.click('[data-disc="vai"]')
    attendi_fermo(pagina)
    alto = pagina.evaluate("document.getElementById('disc-trovati').getBoundingClientRect().top")
    p.controlla(f"{schermo}: il pulsante porta l'elenco in cima allo schermo", 40 <= alto <= 260, f"a {alto:.0f} px dall'alto")
    p.controlla(f"{schermo}: il pulsante porta il fuoco sulla riga dei trovati", fuoco(pagina) == "disc-trovati", fuoco(pagina))


SCHERMI = (
    ("computer", {"viewport": {"width": 1280, "height": 900}}),
    ("telefono", {"viewport": {"width": 390, "height": 844}, "has_touch": True, "is_mobile": True, "device_scale_factor": 2}),
    ("tavoletta", {"viewport": {"width": 768, "height": 1024}, "has_touch": True}),
)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cartella", nargs="?", help="cartella del sito costruito (public)")
    ap.add_argument("--dal-vivo", action="store_true", help="prova la pagina pubblicata all'indirizzo di base, senza cartella")
    ap.add_argument("--base", default="https://www.protezionecivilegenzano.it/", help="indirizzo di base con cui il sito è stato costruito")
    args = ap.parse_args()

    if bool(args.cartella) == args.dal_vivo:
        ap.error("serve la cartella del sito costruito oppure --dal-vivo, non tutti e due")
    cartella = Path(args.cartella).resolve() if args.cartella else None
    base = args.base if args.base.endswith("/") else args.base + "/"
    if cartella and not (cartella / PAGINA / "index.html").is_file():
        print(f"NON ESEGUITA: in {cartella} manca {PAGINA}index.html")
        return 2
    try:
        catalogo = json.loads((RADICE / "data" / "disciplinari.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as errore:
        print(f"NON ESEGUITA: data/disciplinari.json non si legge ({errore})")
        return 2
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("NON ESEGUITA: manca Playwright (pip install playwright; playwright install chromium)")
        return 2

    percorso_base = urlsplit(base).path
    mancanti = set()  # file del sito che la pagina chiede e non trova: una risorsa che manca falsa la prova

    def servi(rotta):
        richiesta = urlsplit(rotta.request.url)
        if not rotta.request.url.startswith(base):
            return rotta.abort()
        relativo = richiesta.path[len(percorso_base):]
        file = (cartella / relativo).resolve()
        if file.is_dir():
            file = file / "index.html"
        if cartella not in file.parents or not file.is_file():
            mancanti.add(richiesta.path)
            return rotta.fulfill(status=404, body="")
        return rotta.fulfill(path=str(file))

    def annota(risposta):
        if risposta.url.startswith(base) and risposta.status >= 400:
            mancanti.add(f"{urlsplit(risposta.url).path} ({risposta.status})")

    p = Prova(catalogo)
    errori_js = []
    indirizzo = base + PAGINA
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            for schermo, forma in SCHERMI:
                contesto = browser.new_context(**forma)
                if cartella:
                    contesto.route("**/*", servi)
                pagina = contesto.new_page()
                pagina.set_default_timeout(15000)  # un elemento che manca ferma la prova in pochi secondi, non in mezzo minuto
                pagina.on("pageerror", lambda errore: errori_js.append(str(errore)))
                if not cartella:
                    pagina.on("response", annota)
                if schermo == "computer":
                    pagina.goto(indirizzo, wait_until="load", timeout=60000)
                    pagina.wait_for_selector('[data-disc="filtri"]:not([hidden])', timeout=20000)
                    prove_della_ricerca(p, pagina)
                    prove_dall_indirizzo(p, pagina, indirizzo)
                else:
                    prove_schermo_piccolo(p, pagina, indirizzo, schermo)
                contesto.close()
            browser.close()
    except Exception as errore:  # il browser non parte, la pagina non si apre, il riquadro non compare
        riga = " ".join(str(errore).split())[:300]
        if p.fatte == 0:
            print(f"NON ESEGUITA: {riga}")
            return 2
        p.errori.append(f"la prova si è interrotta: {riga}")
    p.controlla("nessun errore JavaScript nella pagina", not errori_js, "; ".join(errori_js)[:300])
    p.controlla("la pagina trova tutti i file del sito che chiede", not mancanti, ", ".join(sorted(mancanti)[:6]))

    for errore in p.errori:
        print(f"NON TORNA: {errore}")
    dove = "sul sito pubblicato" if args.dal_vivo else "sulla build"
    print(f"Filtro dei disciplinari, {dove}: {p.fatte - len(p.errori)} prove su {p.fatte} come atteso.")
    return 1 if p.errori else 0


if __name__ == "__main__":
    sys.exit(main())
