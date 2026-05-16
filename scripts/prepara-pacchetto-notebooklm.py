#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prepara-pacchetto-notebooklm.py — Genera pacchetti pronti per NotebookLM.

Per ogni tema chiave del sito (rischio sismico, idrogeologico, AIB, allerta
meteo, kit emergenza) produce in ~/Scrivania/notebooklm-pacchetti/<tema>/
una serie di file Markdown con:
  - 00-INDICE.md         → cosa fare passo per passo
  - 01-fonti.md          → lista URL del sito + fonti istituzionali da caricare
  - 02-prompt-podcast.md → prompt italiano AGID per Overview audio
  - 03-prompt-infografica.md
  - 04-prompt-presentazione.md
  - 05-prompt-quiz.md
  - 06-prompt-flashcard.md

L'utente apre la cartella del tema, copia-incolla nel notebook NotebookLM,
genera, scarica i file e li lascia in ~/Scrivania/notebooklm-output/<tema>/.

Uso:
    python3 scripts/prepara-pacchetto-notebooklm.py
    python3 scripts/prepara-pacchetto-notebooklm.py --tema rischio-sismico
    python3 scripts/prepara-pacchetto-notebooklm.py --aggiungi <slug> "Titolo"

Idempotente: rigenera tutti i file sovrascrivendoli (i prompt sono "fonte di
verità" qui, non in cartella). Se l'utente personalizza un prompt, lo deve
salvare in altro file.
"""

from __future__ import annotations
import argparse
import sys
from pathlib import Path
from textwrap import dedent

HOME = Path.home()
PACCHETTI_DIR = HOME / "Scrivania" / "notebooklm-pacchetti"
OUTPUT_DIR = HOME / "Scrivania" / "notebooklm-output"
SITO_BASE = "https://www.protezionecivilegenzano.it"

# Dati per ogni tema. Ogni voce contiene:
#   titolo: nome leggibile (italiano)
#   pagina_sito: URL canonico della pagina rischio sul sito
#   articoli_correlati: URL articoli del sito sul tema (da prendere come fonti)
#   fonti_istituzionali: PDF e URL esterni da scaricare/copiare
#   focus_podcast: argomenti da coprire nel podcast (lista)
#   icona_emoji: per il README della cartella
TEMI = {
    "rischio-sismico": {
        "titolo": "Rischio sismico nei Castelli Romani",
        "pagina_sito": f"{SITO_BASE}/rischi-prevenzione/rischio-sismico/",
        "articoli_correlati": [
            f"{SITO_BASE}/comunicazioni/2026-11-23-irpinia-1980/",
            f"{SITO_BASE}/comunicazioni/2026-04-06-aquila-2009/",
            f"{SITO_BASE}/comunicazioni/2026-08-24-amatrice-2016/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "Manuale 'Io non rischio terremoto' (DPC): scarica PDF da https://iononrischio.protezionecivile.it",
            "Mappa pericolosità sismica MPS04 (INGV): pagina https://emidius.mi.ingv.it/MPS04/",
            "Linee guida ricostruzione (Casa Italia): https://www.casaitalia.governo.it",
            "Standard ISO 22324 (codici colore allerta) — pagina sito: " + SITO_BASE + "/standard-iso/iso-22324/",
        ],
        "focus_podcast": [
            "Perché Genzano e i Castelli Romani sono sismicamente attivi (vulcanismo dei Colli Albani spento ma non estinto, faglie attive)",
            "Storia sismica recente: Irpinia 1980, L'Aquila 2009, Centro Italia 2016 (dati INGV)",
            "Cosa fare PRIMA: piano familiare, kit emergenza, agganciare mobili, conoscere via di fuga",
            "Cosa fare DURANTE: triangolo della vita è FALSO, posizioni sicure (sotto tavolo robusto, vano porta portante)",
            "Cosa fare DOPO: verifica gas e acqua, evacuazione ordinata, ricongiungimento familiare",
            "Dove informarsi: Centro Funzionale Regionale Lazio, INGV terremoti.ingv.it, Comune",
        ],
        "icona_emoji": "🏠💥",
    },
    "rischio-idrogeologico": {
        "titolo": "Rischio idrogeologico (frane e alluvioni) nei Castelli Romani",
        "pagina_sito": f"{SITO_BASE}/rischi-prevenzione/rischio-idrogeologico/",
        "articoli_correlati": [
            f"{SITO_BASE}/allerte-meteo/",
            f"{SITO_BASE}/cosa-succede-quando-scatta-allerta/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "PAI (Piano Assetto Idrogeologico) Regione Lazio: https://www.regione.lazio.it",
            "Rapporto ISPRA dissesto idrogeologico (ultima edizione): https://www.isprambiente.gov.it",
            "Manuale 'Io non rischio alluvione' (DPC + ANPAS): https://iononrischio.protezionecivile.it",
            "Linee guida CNR-IRPI su frane: https://www.irpi.cnr.it",
        ],
        "focus_podcast": [
            "Cosa è il dissesto idrogeologico e perché interessa Genzano (versanti calderici, suoli vulcanici)",
            "Differenza fra frana e alluvione",
            "Segnali da osservare: crepe nei muri, alberi inclinati, gorgoglii in cantine, scolatoi otturati",
            "Cosa fare PRIMA: piano familiare adattato, area attesa, allontanare oggetti dalle finestre",
            "Cosa fare DURANTE alluvione: salire ai piani alti, non scendere in cantina, evitare guadi",
            "Cosa fare DOPO: documentare danni, segnalare a 803 555 o Comune, non bere acqua del rubinetto se torbida",
            "Codici colore allerta meteo (verde-giallo-arancione-rosso) e dove leggere il bollettino",
        ],
        "icona_emoji": "🌧️🏔️",
    },
    "rischio-incendio": {
        "titolo": "Rischio incendi boschivi (AIB) sui Castelli Romani",
        "pagina_sito": f"{SITO_BASE}/rischi-prevenzione/rischio-incendio/",
        "articoli_correlati": [
            f"{SITO_BASE}/comunicazioni/2026-06-15-campagna-aib/",
            f"{SITO_BASE}/allerte-meteo/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "Bollettino pericolosità incendi boschivi (CFR Lazio, RISICOLazio): https://www.regione.lazio.it/bollettini/rischi-incendi",
            "Piano AIB Regione Lazio: https://www.regione.lazio.it",
            "Manuale 'Io non rischio incendio boschivo' (DPC): https://iononrischio.protezionecivile.it",
            "Legge 353/2000 incendi boschivi: https://www.normattiva.it",
        ],
        "focus_podcast": [
            "Cosa è un incendio boschivo: definizione legale (L. 353/2000)",
            "Perché i Castelli Romani sono a rischio (macchia mediterranea, vento, ricreazione boschiva)",
            "Zona AIB di Genzano = 9 (Castelli Romani): cosa significa nella scala BASSO-MEDIO-MODERATO-ELEVATO",
            "Periodo a rischio (giugno-settembre) e ordinanze comunali tipiche",
            "Cosa NON fare: niente fuochi, niente sigarette nei boschi, niente barbecue improvvisati, mai gettare vetro",
            "Cosa fare se vedi fumo: 112 SUBITO, non avvicinarsi, dare indicazioni precise",
            "Cosa fare se sei intrappolato in un incendio in arrivo: zone di sicurezza, mai correre in salita",
        ],
        "icona_emoji": "🔥🌲",
    },
    "allerta-meteo": {
        "titolo": "Allerta meteo nel Lazio: come leggere i bollettini",
        "pagina_sito": f"{SITO_BASE}/allerte-meteo/",
        "articoli_correlati": [
            f"{SITO_BASE}/cosa-succede-quando-scatta-allerta/",
            f"{SITO_BASE}/comunicazioni/2026-05-07-zone-allerta-lazio-come-leggere-bollettino/",
            f"{SITO_BASE}/standard-iso/iso-22324/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "Direttiva PCM 27 febbraio 2004 sul sistema di allertamento: https://www.normattiva.it",
            "Centro Funzionale Regionale Lazio (bollettini): https://www.regione.lazio.it/bollettini",
            "ISO 22324:2015 — Public warning by color codes: pagina sito " + SITO_BASE + "/standard-iso/iso-22324/",
            "Manuale 'Io non rischio': sezione 'In allerta meteo': https://iononrischio.protezionecivile.it",
        ],
        "focus_podcast": [
            "Cos'è l'allerta meteo: previsione, non evento (è prima che succeda qualcosa)",
            "I 4 codici colore: verde (nessuna criticità), giallo (ordinaria), arancione (moderata), rosso (elevata)",
            "Differenza fondamentale fra ALLERTA (previsione) e EMERGENZA (evento in corso)",
            "Le zone di allerta del Lazio: come funzionano, dove cerchi la zona di Genzano (Castelli Romani)",
            "Chi pubblica il bollettino: Centro Funzionale Regionale (CFR), non il meteo TV",
            "Cosa fare in giallo, arancione, rosso: azioni concrete crescenti",
            "I 3 tipi di rischio nel bollettino: idrogeologico, idraulico, temporali",
            "App e canali: dove ricevere le allerte (sito Regione, app IT-alert, canali ufficiali)",
        ],
        "icona_emoji": "⛈️📊",
    },
    "kit-emergenza": {
        "titolo": "Kit emergenza famiglia: cosa preparare prima di un evento",
        "pagina_sito": f"{SITO_BASE}/rischi-prevenzione/kit-emergenza/",
        "articoli_correlati": [
            f"{SITO_BASE}/piano-familiare/",
            f"{SITO_BASE}/cosa-fare-adesso/",
            f"{SITO_BASE}/formazione/kit-calamita/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "Manuale 'Io non rischio' (DPC) — sezione 'Kit emergenza': https://iononrischio.protezionecivile.it",
            "Linee guida IFRC (Croce Rossa Internazionale): https://www.ifrc.org",
            "Sphere Handbook 2018 — standard umanitari minimi: https://spherestandards.org",
            "Manuale FIC cucina emergenza (sito): " + SITO_BASE + "/area-download/",
        ],
        "focus_podcast": [
            "Tre kit distinti: KIT VAI (evacuazione rapida), KIT CASA (autonomia 72 ore), KIT AUTO",
            "KIT VAI: cosa metterci e cosa no, peso massimo (8-10 kg adulto, 3 kg bambino)",
            "KIT CASA: acqua 3 litri/persona/giorno per 3 giorni, cibo non deperibile, torcia a manovella",
            "KIT AUTO: triangolo, giubbino, coperta isotermica, kit primo soccorso, acqua",
            "Documenti da fotocopiare e tenere in copia (carta identità, libretto sanitario, polizze)",
            "Adattamenti per categorie vulnerabili: bambini (omogeneizzati, pannolini), anziani (farmaci), animali",
            "Manutenzione del kit: ruotare cibo e acqua, controllare batterie 2 volte all'anno",
            "Dove conservare: posto fresco asciutto, accessibile senza luce elettrica, vicino all'uscita",
        ],
        "icona_emoji": "🎒💧",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Template dei prompt — uso f-string per personalizzare per tema
# ─────────────────────────────────────────────────────────────────────────────

FILTRO_AGID = """Scrivi in italiano semplice e chiaro per cittadini non tecnici (anziani, famiglie, ragazzi delle medie). Frasi corte sotto le 20 parole. Voce attiva. Niente burocratese ("ad uopo", "nelle more di", "ai sensi"). Cita sempre la fonte istituzionale (DPC, INGV, ISPRA, Centro Funzionale Regionale Lazio, ISO) quando dai un dato. Tono prudente e operativo, mai allarmistico. Non usare emoji decorativi nel testo. Numeri in cifre, non in lettere. Nel Lazio l'unico numero di emergenza è il 112 (NUE) — non citare più 115, 118, 1515 come numeri da chiamare."""


def prompt_podcast(tema_data: dict) -> str:
    focus = "\n".join(f"{i+1}. {x}" for i, x in enumerate(tema_data["focus_podcast"]))
    return dedent(f"""\
        # Prompt per Overview audio (Podcast NotebookLM)
        ## Tema: {tema_data["titolo"]}

        **Cosa fare**: nello Studio di NotebookLM clicca "Overview audio".
        Poi clicca "Personalizza" PRIMA di generare. Incolla il prompt sotto
        nel campo "Istruzioni di personalizzazione".

        ---

        ## PROMPT (copia-incolla)

        Genera un podcast di circa 20-25 minuti sul tema "{tema_data["titolo"]}".

        Pubblico target: cittadini comuni di Genzano di Roma e dei Castelli
        Romani — famiglie, anziani, studenti delle scuole superiori, persone
        senza conoscenze tecniche di Protezione Civile.

        ## Stile linguistico

        {FILTRO_AGID}

        ## Struttura del podcast (rispetta l'ordine)

        {focus}

        ## Tono dei due speaker

        Speaker 1: conduttore, fa domande semplici dal punto di vista del
        cittadino comune. Non sa niente all'inizio, impara con noi.

        Speaker 2: esperto, risponde con calma. Cita le fonti quando dà un
        dato. Usa esempi concreti riferiti a Genzano e ai Castelli Romani.
        Non fa lezioni, racconta storie e dà istruzioni operative.

        Entrambi sono prudenti: non drammatizzano, non scherzano sulle
        vittime di eventi passati, non danno consigli azzardati.

        ## Cose vietate

        - Non parlare del "triangolo della vita" come consiglio (è una
          tecnica disinformata, lo dice esplicitamente la Croce Rossa).
        - Non citare il 115/118/1515 come numero di emergenza nel Lazio:
          l'unico è il 112.
        - Non dire "purtroppo" / "drammaticamente" / "tragicamente":
          tono prudente, non emotivo.
        - Non inventare statistiche: se non sei sicuro di un numero,
          ometti o di' "circa".

        ## Chiusura del podcast

        Concludi sempre con:
        - "Per saperne di più visita il sito della Protezione Civile di
          Genzano di Roma: protezionecivilegenzano.it"
        - "In caso di emergenza chiama il 112."
        - "Per segnalazioni non urgenti chiama la Sala Operativa Regionale
          al 803 555."
    """)


def prompt_infografica(tema_data: dict) -> str:
    return dedent(f"""\
        # Prompt per Infografica (NotebookLM)
        ## Tema: {tema_data["titolo"]}

        **Cosa fare**: nello Studio di NotebookLM clicca "Infografica".
        Personalizza incollando il prompt sotto. Scarica l'immagine PNG.

        ---

        ## PROMPT (copia-incolla)

        Crea un'infografica formato quadrato 1080×1080 pixel (per Instagram
        e per stampa A4) sul tema "{tema_data["titolo"]}".

        ## Stile grafico

        - Sfondo: bianco o azzurro chiarissimo (#f4f7fb)
        - Colori principali: blu istituzionale #003366 per titoli e bordi
        - Accenti: ambra #b45309 per avvertimenti
        - Niente colori sgargianti, niente gradienti vistosi
        - Font: sans-serif pulito (Roboto, Lato o simili)
        - Stile: piatto, istituzionale, simile a infografiche del
          Dipartimento di Protezione Civile

        ## Contenuto

        - Titolo grande in alto: massimo 6 parole
        - 5-6 punti chiave con icona + frase di 6-10 parole ciascuna
        - In basso piccolo: "Fonti: DPC, INGV, ISPRA, Regione Lazio"
        - Spazio vuoto in basso a sinistra (~150×150 px): è dove
          aggiungeremo il logo PC Genzano in post-produzione

        ## Linguaggio

        {FILTRO_AGID}

        ## Cose vietate

        - Niente emoji decorativi nel titolo
        - Niente caratteri Unicode speciali ("𝐁𝐎𝐋𝐃", "𝓢𝓬𝓻𝓲𝓹𝓽")
        - Niente maiuscole continue in frasi intere
        - Niente affermazioni non verificabili
    """)


def prompt_presentazione(tema_data: dict) -> str:
    return dedent(f"""\
        # Prompt per Presentazione PPTX (NotebookLM)
        ## Tema: {tema_data["titolo"]}

        **Cosa fare**: nello Studio di NotebookLM clicca "Presentazione".
        Personalizza incollando il prompt sotto. Scarica il file PPTX.
        I docenti delle scuole lo useranno per le ore di Educazione
        Civica sul tema Protezione Civile.

        ---

        ## PROMPT (copia-incolla)

        Crea una presentazione di 15 slide per un'ora di lezione di
        Educazione Civica (D.M. 183/2024, 33 ore annuali) sul tema
        "{tema_data["titolo"]}". Target: classe di terza media (13-14
        anni) o prima superiore (14-15 anni).

        ## Struttura obbligatoria

        Slide 1: Titolo + nome scuola lasciato vuoto + data lezione
        vuota + logo segnaposto in basso a sinistra.

        Slide 2-3: Inquadramento del tema (che cos'è, quando succede,
        perché ci riguarda — riferimento al territorio dei Castelli
        Romani).

        Slide 4-6: Cosa fare PRIMA dell'evento (preparazione,
        prevenzione, conoscenza del territorio).

        Slide 7-9: Cosa fare DURANTE l'evento (azioni di
        autoprotezione, posizioni sicure, errori comuni da evitare).

        Slide 10-11: Cosa fare DOPO l'evento (recupero, segnalazione,
        ricongiungimento familiare).

        Slide 12: Il numero da chiamare — sempre 112. Mai 115, 118,
        1515 (sono superati nel Lazio dal 2017).

        Slide 13: Il ruolo del volontariato di Protezione Civile
        (riferimento al Gruppo Comunale di Genzano).

        Slide 14: Un caso storico italiano del tema (per esempio:
        Irpinia 1980 per sismico, Sarno 1998 per idrogeologico, Liguria
        2007 per incendi).

        Slide 15: Risorse e link utili (sito Protezione Civile Genzano,
        DPC, INGV, app IT-alert).

        ## Per ogni slide includi

        - Titolo breve (massimo 6 parole)
        - 3-4 bullet point (massimo 12 parole ciascuno)
        - 1 "Nota docente" in basso (in font più piccolo, italico):
          suggerisce al docente cosa dire ad alta voce, quale domanda
          fare alla classe, quale attività proporre.

        ## Linguaggio

        {FILTRO_AGID}

        ## Stile visivo

        - Colori: blu istituzionale #003366 per titoli, sfondo bianco
        - Niente animazioni o transizioni (i docenti devono poterla
          modificare senza problemi)
        - 1 immagine per slide quando rilevante (per esempio: mappa
          di pericolosità sismica per il rischio sismico)
    """)


def prompt_quiz(tema_data: dict) -> str:
    return dedent(f"""\
        # Prompt per Quiz (NotebookLM)
        ## Tema: {tema_data["titolo"]}

        **Cosa fare**: nello Studio di NotebookLM clicca "Quiz".
        Personalizza incollando il prompt sotto. Esporta le domande
        in formato testo o JSON.

        ---

        ## PROMPT (copia-incolla)

        Genera un quiz di 10 domande a risposta multipla sul tema
        "{tema_data["titolo"]}".

        ## Target

        Studenti scuole superiori, famiglie, cittadini comuni di
        Genzano di Roma. Pubblico non specialistico.

        ## Struttura

        - 10 domande in totale
        - Difficoltà progressiva:
          - Domande 1-3: facili (riconoscimento di concetti base)
          - Domande 4-7: medie (comprensione di procedure e regole)
          - Domande 8-10: difficili (applicazione a casi concreti)

        ## Per ogni domanda

        - Testo della domanda: massimo 25 parole, italiano semplice
        - 4 risposte: 1 corretta, 3 plausibili ma sbagliate (no risposte
          assurde, devono essere errori "verosimili" che un cittadino
          potrebbe davvero fare)
        - Spiegazione della risposta corretta: 1-2 frasi che dicono
          il "perché" e citano la fonte istituzionale (es. "Centro
          Funzionale Regionale Lazio" o "DPC" o "ISO 22324")

        ## Argomenti obbligatori (almeno 1 domanda per ciascuno)

        - Numero da chiamare in caso di emergenza nel Lazio (112)
        - Differenza fra allerta (previsione) ed emergenza (evento)
        - Codici colore allerta meteo (verde, giallo, arancione, rosso)
        - Un comportamento sbagliato comune da NON fare durante l'evento
        - Un'azione di prevenzione concreta che il cittadino può fare
          prima dell'evento

        ## Linguaggio

        {FILTRO_AGID}
    """)


def prompt_flashcard(tema_data: dict) -> str:
    return dedent(f"""\
        # Prompt per Flashcard (NotebookLM)
        ## Tema: {tema_data["titolo"]}

        **Cosa fare**: nello Studio di NotebookLM clicca "Flashcard".
        Personalizza incollando il prompt sotto. Esporta le carte come
        PDF o copia il testo: le useremo per i kit didattici delle
        scuole come schede stampabili A4.

        ---

        ## PROMPT (copia-incolla)

        Crea un mazzo di 20 flashcard sul tema "{tema_data["titolo"]}"
        per studenti di scuola media (11-13 anni) o prima superiore.

        ## Per ogni carta

        - LATO A (domanda): breve, in italiano semplice, massimo 12
          parole. Una sola domanda per carta, no domande multiple.
        - LATO B (risposta): massimo 30 parole, italiano semplice,
          con un esempio concreto quando possibile. Cita la fonte
          se è un dato numerico o una regola operativa.

        ## Distribuzione (20 carte totali)

        - 5 carte sulla scienza/fenomeno (cosa è, perché succede,
          chi lo studia, come si misura)
        - 5 carte sulla storia italiana del tema (eventi noti,
          date, magnitudo o estensione)
        - 5 carte sulla preparazione (kit emergenza, piano familiare,
          conoscenza del territorio, dove informarsi)
        - 5 carte sull'azione (cosa fare durante l'evento, cosa NON
          fare, numero da chiamare)

        ## Linguaggio

        {FILTRO_AGID}

        ## Stile

        - Niente carte "trabocchetto" o con doppi sensi
        - Niente carte che richiedono memoria di numeri lunghi (es.
          coordinate geografiche, numeri di telefono lunghi)
        - Una sola domanda concreta per carta
    """)


# ─────────────────────────────────────────────────────────────────────────────
# Generatore di file
# ─────────────────────────────────────────────────────────────────────────────

def fonti_md(tema_slug: str, tema_data: dict) -> str:
    articoli = "\n".join(f"- {url}" for url in tema_data["articoli_correlati"])
    istituzionali = "\n".join(f"- {fonte}" for fonte in tema_data["fonti_istituzionali"])
    return dedent(f"""\
        # Fonti da caricare nel notebook NotebookLM
        ## Tema: {tema_data["titolo"]}

        **Cosa fare**: apri NotebookLM, crea un nuovo notebook chiamato
        "{tema_data["titolo"]}", poi clicca "Aggiungi fonti" e incolla
        UNO PER UNO gli URL e i file della lista sotto.

        ⚠️ NotebookLM PRO accetta fino a 300 fonti. Tu ne caricherai
        circa 10-15: meglio poche fonti pertinenti che tante poco
        utili.

        ---

        ## Fonti dal nostro sito (URL diretti)

        Incolla questi URL uno alla volta nella casella "Aggiungi fonti"
        → opzione "Link" / "URL". NotebookLM le scarica e le legge in
        automatico.

        - {tema_data["pagina_sito"]} ← pagina principale del tema
        {articoli}

        ## Fonti istituzionali (PDF e siti esterni)

        Per le fonti istituzionali con PDF, scaricali dal sito ufficiale
        e poi caricali in NotebookLM (opzione "Carica file"). Per le
        pagine HTML, incolla l'URL come per gli articoli del sito.

        {istituzionali}

        ## Suggerimento

        Cerca anche video YouTube ufficiali sul tema (Protezione Civile
        Nazionale, INGV, Regione Lazio) e incolla anche quelli:
        NotebookLM legge i sottotitoli e li usa come fonti.

        ---

        ## Una volta caricate tutte le fonti

        Aspetta che NotebookLM le "legga" (30-60 secondi, vedi la rotella
        accanto a ogni fonte). Poi vai ai prompt:

        - `02-prompt-podcast.md` → genera podcast audio
        - `03-prompt-infografica.md` → genera infografica
        - `04-prompt-presentazione.md` → genera PPTX docenti
        - `05-prompt-quiz.md` → genera quiz
        - `06-prompt-flashcard.md` → genera flashcard
    """)


def indice_md(tema_slug: str, tema_data: dict) -> str:
    return dedent(f"""\
        # Pacchetto NotebookLM — {tema_data["icona_emoji"]} {tema_data["titolo"]}

        Questo è il pacchetto pronto da usare in NotebookLM. Segui i
        passi sotto in ordine: a fine procedura avrai 5 contenuti
        professionali per il sito (podcast, infografica, presentazione,
        quiz, flashcard).

        ---

        ## Cosa fare in 4 passi

        ### Passo 1 — Crea il notebook
        - Apri <https://notebooklm.google.com>
        - Clicca "Crea notebook" in alto a destra
        - Quando ti chiede il titolo, scrivi: "{tema_data["titolo"]}"

        ### Passo 2 — Carica le fonti
        - Apri il file `01-fonti.md` qui nella cartella
        - Segui le istruzioni dentro per caricare URL del sito + PDF
          istituzionali nel notebook
        - Aspetta che NotebookLM "legga" tutte le fonti (rotella accanto
          a ogni voce → diventa spunta verde quando è pronto)

        ### Passo 3 — Imposta italiano una volta sola
        - Clicca l'ingranaggio ⚙️ in alto a destra
        - Vai su "Output language" / "Lingua di output"
        - Scegli **Italiano**
        - Salva

        ### Passo 4 — Genera i 5 output
        Apri gli altri 5 file di questa cartella nell'ordine:

        1. `02-prompt-podcast.md` → clicca "Overview audio" nello Studio
           a destra, poi "Personalizza", incolla il prompt, genera, scarica MP3
        2. `03-prompt-infografica.md` → clicca "Infografica", stesso
           procedimento, scarica PNG
        3. `04-prompt-presentazione.md` → clicca "Presentazione", scarica PPTX
        4. `05-prompt-quiz.md` → clicca "Quiz", esporta domande
        5. `06-prompt-flashcard.md` → clicca "Flashcard", esporta PDF

        ---

        ## Dove lasciare i file scaricati

        Crea una cartella sul Desktop chiamata `notebooklm-output`
        (se non esiste già: io te la creo automaticamente con questo
        pacchetto). Dentro, c'è la sottocartella `{tema_slug}/`.

        Trascina lì i file scaricati da NotebookLM. Rinominali così:

        - Podcast audio → `podcast.mp3`
        - Infografica → `infografica.png`
        - Presentazione → `presentazione.pptx`
        - Quiz (testo o JSON) → `quiz.txt` o `quiz.json`
        - Flashcard PDF → `flashcard.pdf`

        Quando hai messo i file, scrivi a Claude:

        > "Ho caricato gli output di NotebookLM per il tema {tema_slug}.
        > Pubblicali sul sito."

        Claude li trova in automatico, li rinomina con la convenzione
        del sito, li mette nelle cartelle giuste, aggiorna il catalogo
        delle "Risorse pronte" su /risorse-pronte/, fa commit e push.
        In 5 minuti i tuoi materiali sono live e scaricabili dai
        cittadini sul sito.

        ---

        ## Tempo necessario

        - Setup notebook (passi 1-3): **10 minuti** (solo la prima volta)
        - Generazione dei 5 output (passo 4): **~20 minuti** di click +
          attesa (il podcast da solo richiede ~5 minuti di elaborazione)
        - Drop dei file nella cartella di output: **2 minuti**

        Totale: ~30 minuti di lavoro tuo per 5 contenuti completi
        sul tema. Una sessione settimanale = un tema nuovo a settimana
        = 52 contenuti a regime in un anno.
    """)


def scrivi_pacchetto(tema_slug: str, tema_data: dict) -> int:
    """Scrive tutti e 6 i file nella cartella di un tema. Ritorna numero file."""
    cartella = PACCHETTI_DIR / tema_slug
    cartella.mkdir(parents=True, exist_ok=True)
    output_cartella = OUTPUT_DIR / tema_slug
    output_cartella.mkdir(parents=True, exist_ok=True)

    files = {
        "00-INDICE.md": indice_md(tema_slug, tema_data),
        "01-fonti.md": fonti_md(tema_slug, tema_data),
        "02-prompt-podcast.md": prompt_podcast(tema_data),
        "03-prompt-infografica.md": prompt_infografica(tema_data),
        "04-prompt-presentazione.md": prompt_presentazione(tema_data),
        "05-prompt-quiz.md": prompt_quiz(tema_data),
        "06-prompt-flashcard.md": prompt_flashcard(tema_data),
    }

    for nome, contenuto in files.items():
        (cartella / nome).write_text(contenuto, encoding="utf-8")

    return len(files)


def scrivi_readme_top() -> None:
    """README di alto livello che spiega cosa c'è nella cartella pacchetti."""
    elenco = "\n".join(
        f"- **{slug}/** {data['icona_emoji']} — {data['titolo']}"
        for slug, data in TEMI.items()
    )
    readme = dedent(f"""\
        # Pacchetti NotebookLM per il sito Protezione Civile Genzano

        Qui ci sono i pacchetti pronti per generare contenuti professionali
        in NotebookLM senza dover scrivere nulla.

        ## Cosa c'è qui dentro

        {elenco}

        ## Come si usa

        1. Scegli un tema (es. `rischio-sismico/`)
        2. Apri `00-INDICE.md` di quel tema: ti dice cosa fare in 4 passi
        3. Genera i 5 output in NotebookLM (~30 minuti totali)
        4. Trascina i file scaricati in `~/Scrivania/notebooklm-output/<tema>/`
        5. Scrivi a Claude: "Pubblica gli output NotebookLM di <tema>"
        6. In 5 minuti i materiali sono live su <https://www.protezionecivilegenzano.it/risorse-pronte/>

        ## Cosa producono i pacchetti

        Per ogni tema ottieni:
        - 🎧 Podcast audio (20-25 minuti, 2 voci AI dialogano)
        - 🎨 Infografica 1080×1080 per Instagram + stampa A4
        - 📊 Presentazione PPTX per docenti delle scuole
        - ✅ Quiz a 10 domande per il sito
        - 🎴 Flashcard 20 carte per studio scuole

        Tutto è pubblicato con licenza CC BY-NC-SA 4.0: gli utenti del
        sito possono scaricare, condividere, riutilizzare per uso non
        commerciale citando la fonte.

        ## Aggiungere un nuovo tema

        Se vuoi un pacchetto su un tema non in elenco (es. ondate di
        calore, blackout, vulcanico), scrivi a Claude:

        > "Aggiungi un pacchetto NotebookLM per il tema X"

        Claude lancia `python3 scripts/prepara-pacchetto-notebooklm.py
        --aggiungi X` e ti crea il pacchetto in pochi secondi.
    """)
    (PACCHETTI_DIR / "00-LEGGIMI.md").write_text(readme, encoding="utf-8")


def scrivi_readme_output() -> None:
    """README della drop zone."""
    output_readme = dedent("""\
        # Drop zone — output scaricati da NotebookLM

        Questa cartella è dove trascini i file scaricati da NotebookLM
        per ogni tema. Claude li legge da qui e li pubblica sul sito.

        ## Struttura attesa per ogni tema

        Esempio per il tema "rischio-sismico":

        ```
        notebooklm-output/rischio-sismico/
            ├── podcast.mp3              (15-30 MB, dura 20-25 min)
            ├── infografica.png          (1080×1080, ~500 KB)
            ├── presentazione.pptx       (5-15 MB)
            ├── quiz.txt                 (o quiz.json)
            └── flashcard.pdf            (1-3 MB)
        ```

        Non tutti i file devono essere presenti: se hai generato solo il
        podcast, lascia solo `podcast.mp3` nella cartella. Claude pubblica
        quello che trova.

        ## Quando hai finito

        Scrivi a Claude:

        > "Ho caricato gli output di NotebookLM per il tema X. Pubblicali."

        Claude in ~5 minuti:
        - Rinomina i file con la convenzione del sito
        - Li mette nelle cartelle giuste del repository
        - Aggiunge la card alla pagina /risorse-pronte/
        - Aggiorna il feed RSS del podcast se c'è un MP3
        - Fa commit + push → il sito li serve in <3 minuti dopo il push

        ## Riusare la stessa cartella

        Quando hai finito di pubblicare, Claude svuota la cartella
        del tema così è pronta per il prossimo aggiornamento dello
        stesso tema (es. nuova versione del podcast a marzo).
    """)
    (OUTPUT_DIR / "00-LEGGIMI.md").write_text(output_readme, encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Genera pacchetti NotebookLM pronti all'uso per il sito PC Genzano.",
    )
    parser.add_argument(
        "--tema",
        help="Genera solo il pacchetto per questo tema. Default: tutti.",
        choices=list(TEMI.keys()),
    )
    parser.add_argument(
        "--lista",
        action="store_true",
        help="Elenca i temi disponibili e esce.",
    )
    args = parser.parse_args()

    if args.lista:
        print("Temi disponibili:")
        for slug, data in TEMI.items():
            print(f"  {slug:30s} {data['icona_emoji']} {data['titolo']}")
        return 0

    PACCHETTI_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    temi_da_processare = [args.tema] if args.tema else list(TEMI.keys())

    print(f"📦 Generazione pacchetti in: {PACCHETTI_DIR}")
    print(f"📥 Drop zone output in:    {OUTPUT_DIR}")
    print()

    totale = 0
    for slug in temi_da_processare:
        data = TEMI[slug]
        n = scrivi_pacchetto(slug, data)
        print(f"  ✓ {slug:30s} → {n} file scritti")
        totale += n

    scrivi_readme_top()
    scrivi_readme_output()
    print()
    print(f"📊 Totale: {totale} file pacchetti + 2 README su Desktop.")
    print(f"➡ Apri ora: {PACCHETTI_DIR}/00-LEGGIMI.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
