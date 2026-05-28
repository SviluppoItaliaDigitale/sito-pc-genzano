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
REPO_ROOT = Path(__file__).resolve().parent.parent
PACCHETTI_DIR = HOME / "Scrivania" / "notebooklm-pacchetti"
OUTPUT_DIR = HOME / "Scrivania" / "notebooklm-output"
SITO_BASE = "https://www.protezionecivilegenzano.it"

# Keyword matching per individuare gli articoli del sito pertinenti a un tema.
# Match case-insensitive nel body + frontmatter dei .md di content/comunicazioni/.
KEYWORDS_TEMA = {
    "rischio-sismico": [
        "terremoto", "terremoti", "sisma", "sismic", "magnitudo", "shake",
        "fagli", "INGV", "ipocentro", "epicentro", "Richter", "Mercalli",
        "Irpinia", "L'Aquila", "Amatrice", "Centro Italia",
    ],
    "rischio-idrogeologico": [
        "frana", "frane", "alluvion", "idrogeologic", "dissesto", "PAI",
        "esondazion", "allagament", "smottament", "torrent", "Sarno",
        "Genova", "ARSIAL", "ISPRA",
    ],
    "rischio-incendio": [
        "incendio", "incendi", "AIB", "antincendio", "boschiv", "rogo",
        "RISICO", "Zona AIB", "L. 353/2000", "Canadair",
    ],
    "allerta-meteo": [
        "allerta", "allerte", "bollettin", "criticità",
        "Centro Funzionale", "codice colore", "vento forte", "temporal",
        "ondata di calore", "neve", "zona di allerta",
    ],
    "kit-emergenza": [
        "kit emergenza", "kit di emergenza", "piano familiare", "evacuazione",
        "kit vai", "kit casa", "kit auto", "preparazione", "72 ore",
        "vulnerabili", "anzian", "neonat", "famiglia", "scorte",
    ],
    "rischio-vulcanico": [
        "vulcanic", "vulcano", "Colli Albani", "Distretto Vulcanico",
        "INGV-OV", "Osservatorio Vesuviano", "quiescente", "magma",
        "caldera", "lago Albano", "lago di Nemi", "gas vulcanic",
    ],
    "ondate-di-calore": [
        "caldo", "ondata di calore", "ondate di calore", "Piano caldo",
        "temperatura percepita", "colpo di calore", "disidratazione",
        "anzian", "neonat", "ASL Roma 6", "ISS", "bollettino calore",
    ],
    "temporali-intensi": [
        "temporal", "downburst", "fulmin", "raffiche", "grandine",
        "nubifragio", "supercella", "tromba d'aria", "tornado",
    ],
    "vento-forte": [
        "vento forte", "raffiche", "tramontana", "burrasca", "burian",
        "alberi caduti", "ponteggi", "impalcature", "vela",
    ],
    "blackout": [
        "blackout", "black out", "interruzione elettrica", "Terna",
        "rete elettrica", "frigorifero", "ascensore bloccato",
        "terapie salvavita", "concentratore ossigeno", "dialisi",
    ],
    "dopo-emergenza": [
        "dopo l'emergenza", "post-evento", "ricostruzione", "AeDES",
        "agibilità", "segnalazione danni", "supporto psicologico",
        "ritorno a casa", "verifica abitazione",
    ],
    "nue-112": [
        "112", "NUE", "Numero Unico Emergenze", "Where Are U",
        "chiamata muta", "geolocalizzazione", "centrale unica",
        "smistamento", "operatore 112",
    ],
    "it-alert": [
        "IT-alert", "IT alert", "ITalert", "allarme pubblico",
        "cell broadcast", "DPC notifiche", "test IT-alert",
    ],
    "piano-familiare": [
        "piano familiare", "piano di famiglia", "punto di incontro",
        "contatto fuori area", "prove emergenza", "ricongiungimento",
        "documenti famiglia", "bambini scuola emergenza",
    ],
    "aree-emergenza": [
        "aree di emergenza", "area di attesa", "area di accoglienza",
        "area di ammassamento", "centro accoglienza", "tendopoli",
        "Cartografia", "punti raccolta",
    ],
    "animali-emergenza": [
        "animal", "cane", "gatto", "veterinari", "trasportino",
        "microchip", "anagrafe canina", "petardi", "randagism",
        "stalla", "fattoria", "bestiame", "pet", "ENPA", "LAV",
        "WSAVA", "L. 281/1991", "L. 189/2004",
    ],
}

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
        # articoli_correlati: derivati AUTOMATICAMENTE dal filesystem
        # via keyword matching su content/comunicazioni/*.md.
        # Sempre URL reali, mai inventati.
        "articoli_correlati": [
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "Campagna 'Io non rischio' (DPC): https://iononrischio.protezionecivile.it",
            "INGV — Istituto Nazionale di Geofisica e Vulcanologia: https://www.ingv.it",
            "Terremoti in tempo reale (INGV): https://terremoti.ingv.it",
            "Standard ISO 22324 (codici colore allerta) — pagina del nostro sito: " + SITO_BASE + "/standard-iso/iso-22324/",
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
        # articoli_correlati: pagine canoniche del sito (sempre esistenti).
        # Gli articoli /comunicazioni/ pertinenti vengono aggiunti dal
        # keyword matching automatico (vedi trova_articoli_reali()).
        "articoli_correlati": [
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
    "rischio-vulcanico": {
        "titolo": "Rischio vulcanico nei Colli Albani: cosa sapere davvero",
        "pagina_sito": f"{SITO_BASE}/rischi-prevenzione/rischio-vulcanico/",
        "articoli_correlati": [
            f"{SITO_BASE}/rischi-prevenzione/rischio-sismico/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "INGV — Osservatorio Vesuviano, sezione Colli Albani: https://www.ov.ingv.it",
            "INGV — Distretto Vulcanico dei Colli Albani: https://www.ingv.it",
            "Carta vulcanologica e classificazione DPC: https://www.protezionecivile.gov.it/it/dossier/rischio-vulcanico",
            "ISPRA — Carta geologica d'Italia foglio Albano: https://www.isprambiente.gov.it",
        ],
        "focus_podcast": [
            "I Colli Albani sono un vulcano quiescente, non estinto: cosa significa davvero (l'INGV li monitora costantemente)",
            "Storia eruttiva: ultima eruzione esplosiva ~36.000 anni fa; sismicità di sciame dimostra il sistema vivo",
            "Cosa monitora INGV-OV: sismicità, deformazione del suolo, gas (CO2, radon), livello laghi Albano e Nemi",
            "Differenza fra rischio sismico vulcanico (sciami) e rischio eruttivo (oggi non imminente)",
            "Falsi miti: \"il vulcano è morto\" / \"se esplode arriva fino a Roma in 5 minuti\" — la realtà documentata",
            "Cosa farebbe la PC nazionale in caso di anomalia: piano nazionale, livelli di allerta (verde-giallo-arancione-rosso)",
            "Cosa può fare il cittadino oggi: informarsi alle fonti INGV, non fidarsi di video allarmistici sui social",
        ],
        "icona_emoji": "🌋",
    },
    "ondate-di-calore": {
        "titolo": "Ondate di calore: come proteggersi davvero",
        "pagina_sito": f"{SITO_BASE}/rischi-prevenzione/ondate-di-calore/",
        "articoli_correlati": [
            f"{SITO_BASE}/rischi-prevenzione/persone-necessita-specifiche/",
            f"{SITO_BASE}/numeri-utili/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "Piano nazionale Ondate di Calore (Ministero Salute): https://www.salute.gov.it/portale/caldo/",
            "Bollettino caldo Roma — Ministero Salute (HHWWS): https://www.salute.gov.it/portale/caldo/dettaglioContenutiCaldo.jsp",
            "Istituto Superiore di Sanità — Linee guida ondate calore: https://www.iss.it",
            "ASL Roma 6 — servizi per anziani e fragili in estate: https://www.aslroma6.it",
            "OMS — Heat-health action plans: https://www.who.int",
        ],
        "focus_podcast": [
            "Cos'è un'ondata di calore: definizione tecnica (≥ 3 giorni consecutivi con temperatura percepita oltre soglia)",
            "Differenza fra temperatura misurata e temperatura percepita (umidità + vento)",
            "Chi rischia davvero di più: anziani soli, neonati, malati cronici, lavoratori all'aperto, persone senza casa",
            "Sintomi colpo di calore: confusione, pelle calda e secca, mancata sudorazione — è un'emergenza, 112",
            "Cosa fare in casa: ombreggiare al mattino, areare la notte, idratazione regolare (anche senza sete)",
            "Cosa fare fuori: evitare 11-17, vestiti chiari, cappello, mai bambini/animali in auto al sole",
            "Servizi attivi a Genzano e nei Castelli: bollettino quotidiano, numero verde regionale anziani, ASL Roma 6",
            "Falsi miti: \"il caldo non uccide\", \"basta bere birra\", \"i ventilatori bastano sempre\"",
        ],
        "icona_emoji": "🌡️☀️",
    },
    "temporali-intensi": {
        "titolo": "Temporali intensi: fulmini, grandine, downburst",
        "pagina_sito": f"{SITO_BASE}/rischi-prevenzione/temporali-intensi/",
        "articoli_correlati": [
            f"{SITO_BASE}/allerte-meteo/",
            f"{SITO_BASE}/rischi-prevenzione/vento-forte/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "Centro Funzionale Regionale Lazio — bollettino temporali: https://www.regione.lazio.it/bollettini",
            "DPC — rischio temporali: https://www.protezionecivile.gov.it",
            "ESSL European Severe Storms Laboratory: https://www.essl.org",
            "Manuale 'Io non rischio' sezione temporali: https://iononrischio.protezionecivile.it",
        ],
        "focus_podcast": [
            "Cos'è un temporale intenso: cumulonembo, supercella, sistema multicellulare — perché alcuni fanno paura",
            "Fenomeni associati pericolosi: fulmini, grandine grossa, downburst (raffica discendente), tromba d'aria",
            "Downburst spiegato semplice: la raffica che esce dal temporale verso il basso, può raggiungere 150 km/h",
            "Cosa fare se sei all'aperto: cercare riparo solido SUBITO, non sotto un albero isolato, non in mezzo a campo",
            "Cosa fare in auto: rallentare, fermarsi se la visibilità si annulla, non sotto cavalcavia se grandine grossa",
            "Cosa fare in casa: chiudere finestre, scollegare elettrodomestici sensibili, restare lontano da finestre",
            "Falsi miti: \"il fulmine non colpisce due volte\", \"la gomma dell'auto isola\" — la verità tecnica",
            "Codici colore del bollettino temporali del CFR Lazio: giallo / arancione / rosso e cosa cambia",
        ],
        "icona_emoji": "⛈️⚡",
    },
    "vento-forte": {
        "titolo": "Vento forte: alberi, ponteggi, raffiche",
        "pagina_sito": f"{SITO_BASE}/rischi-prevenzione/vento-forte/",
        "articoli_correlati": [
            f"{SITO_BASE}/allerte-meteo/",
            f"{SITO_BASE}/rischi-prevenzione/temporali-intensi/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "Scala Beaufort (riferimento internazionale velocità vento): https://www.metoffice.gov.uk",
            "Centro Funzionale Regionale Lazio — bollettino vento: https://www.regione.lazio.it/bollettini",
            "Direttiva PCM 27/02/2004 sull'allertamento: https://www.normattiva.it",
            "Manuale 'Io non rischio' (sezione vento e fulmini): https://iononrischio.protezionecivile.it",
        ],
        "focus_podcast": [
            "Quando il vento diventa pericoloso: soglie operative (>60 km/h = avviso, >90 km/h = forte)",
            "Tipi di vento nei Castelli: tramontana fredda da nord-est, scirocco caldo da sud-est, raffiche temporalesche",
            "Cosa si stacca per primo: rami secchi, tegole, antenne, vasi sui balconi, cartelloni, ponteggi non a norma",
            "Cosa fare PRIMA in casa: assicurare oggetti sui balconi, riparare tegole pericolanti, potare rami secchi",
            "Cosa fare DURANTE: stare lontano da alberi e impalcature, non parcheggiare sotto chiome ampie",
            "Cosa fare in auto con vento forte: ridurre velocità, evitare camion in sorpasso, attenzione su ponti e viadotti",
            "Cosa NON fare: salire su tetti per controllare, attraversare pinete o filari con vento di tempesta",
            "Avvisi meteo vento del Lazio: come leggere il bollettino specifico (diverso da quello criticità)",
        ],
        "icona_emoji": "💨🌬️",
    },
    "blackout": {
        "titolo": "Blackout: come prepararsi davvero, senza panico",
        "pagina_sito": f"{SITO_BASE}/rischi-prevenzione/blackout/",
        "articoli_correlati": [
            f"{SITO_BASE}/rischi-prevenzione/kit-emergenza/",
            f"{SITO_BASE}/rischi-prevenzione/persone-necessita-specifiche/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "Terna — gestore rete trasmissione nazionale: https://www.terna.it",
            "DPC — rischio blackout elettrico: https://www.protezionecivile.gov.it",
            "ARERA — Autorità regolazione energia: https://www.arera.it",
            "Manuale 'Io non rischio' sezione blackout: https://iononrischio.protezionecivile.it",
        ],
        "focus_podcast": [
            "Tipi di blackout: locale (cabina), zonale (linea), nazionale (rete) — perché la durata cambia tutto",
            "Storia: blackout italiano del 28 settembre 2003 (rete intera 18 ore) — cosa ci ha insegnato",
            "Cosa preparare PRIMA: torcia a manovella, batterie ricariche, candele in luogo sicuro, contante piccolo taglio",
            "Frigorifero e congelatore: regola delle 4 ore (frigo) e 24-48 ore (freezer pieno chiuso)",
            "Persone in terapia salvavita (concentratori ossigeno, dialisi, CPAP): piano con ASL, alimentazione di backup",
            "Ascensore bloccato: pulsante allarme, non forzare le porte, attendere — chiamare 112 solo se persone fragili",
            "Comunicazione famiglia in blackout: telefono cellulare usa rete dati ma cella satura, SMS funziona meglio",
            "Quando torna la luce: ricollegare elettrodomestici uno alla volta per evitare picchi e sovraccarichi",
        ],
        "icona_emoji": "🔌🕯️",
    },
    "dopo-emergenza": {
        "titolo": "Dopo l'emergenza: la fase che nessuno racconta",
        "pagina_sito": f"{SITO_BASE}/rischi-prevenzione/dopo-emergenza/",
        "articoli_correlati": [
            f"{SITO_BASE}/rischi-prevenzione/rischio-sismico/",
            f"{SITO_BASE}/rischi-prevenzione/rischio-idrogeologico/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "DPC — Scheda AeDES per agibilità post-sisma: https://www.protezionecivile.gov.it",
            "Codice della Protezione Civile (D.Lgs. 1/2018) — fase post-evento: https://www.normattiva.it",
            "OMS — Mental Health and Psychosocial Support in Emergencies: https://www.who.int",
            "IFRC — Recovery and reconstruction: https://www.ifrc.org",
        ],
        "focus_podcast": [
            "Le 4 fasi del ciclo: previsione, prevenzione, soccorso, superamento — perché il superamento è la più lunga",
            "Verifica abitazione: non rientrare prima del via libera dei tecnici se ci sono dubbi strutturali",
            "Scheda AeDES: cos'è, chi la compila, le 6 categorie (A agibile / B con interventi / C parzialmente / D temporaneamente / E inagibile / F inagibile per altro)",
            "Segnalazione danni al Comune: tempistiche, documentazione fotografica, foto con data",
            "Acqua e cibo dopo alluvione/sisma: bollire l'acqua se torbida, scartare cibo che ha perso refrigerazione",
            "Supporto psicologico post-evento: ansia post-traumatica è normale, quando chiedere aiuto (ASL, Croce Rossa, associazioni)",
            "Bambini dopo un'emergenza: parlarne con linguaggio adeguato all'età, ripristinare routine",
            "Truffe post-emergenza: falsi tecnici, finti volontari — riconoscerli e segnalarli (carabinieri 112)",
        ],
        "icona_emoji": "🏚️🤝",
    },
    "nue-112": {
        "titolo": "NUE 112: come si chiama davvero il numero unico di emergenza",
        "pagina_sito": f"{SITO_BASE}/numeri-utili/",
        "articoli_correlati": [
            f"{SITO_BASE}/cosa-fare-adesso/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "EENA — European Emergency Number Association: https://eena.org",
            "112.gov.it — Sito istituzionale italiano del 112: https://www.112.gov.it",
            "Decisione 91/396/CEE del Consiglio europeo (istituzione del 112): https://eur-lex.europa.eu",
            "App 'Where Are U' — geolocalizzazione 112: https://www.where-are-u.it",
        ],
        "focus_podcast": [
            "Dal 2017 nel Lazio l'UNICO numero da chiamare in emergenza è il 112 — perché ha sostituito 115, 118, 1515",
            "Cosa succede quando chiami: l'operatore di centrale unica risponde, identifica l'emergenza, smista a VVF/118/CC/PS",
            "Cosa dire all'operatore: cosa sta succedendo, dove (indirizzo preciso o riferimenti visibili), quante persone coinvolte, telefono di richiamo",
            "Geolocalizzazione: il 112 ha già la tua posizione approssimativa, ma confermala. App 'Where Are U' la rende precisa al metro",
            "Chiamata muta: se non puoi parlare, l'operatore lo capisce (silenzio + ascolto rumori) e invia comunque aiuti",
            "112 da estero: in tutta l'Unione Europea (più Regno Unito, Norvegia, Islanda, Svizzera) funziona uguale",
            "Falsi miti: \"costa\" (è gratuito), \"se sbaglio numero mi multano\" (no, ma chiamate a vuoto sì), \"posso chiamare per info\" (no — info al 1500 o al Comune)",
            "Numeri NON di emergenza utili: 803 555 Sala Operativa PC Lazio, 1530 Guardia Costiera (mare e laghi)",
        ],
        "icona_emoji": "📞🆘",
    },
    "it-alert": {
        "titolo": "IT-alert: il sistema italiano di allarme pubblico",
        "pagina_sito": f"{SITO_BASE}/comunicazioni/2026-05-15-iso-22322-public-warning-it-alert/",
        "articoli_correlati": [
            f"{SITO_BASE}/standard-iso/iso-22322/",
            f"{SITO_BASE}/allerte-meteo/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "IT-alert — sito ufficiale Dipartimento Protezione Civile: https://www.it-alert.it",
            "DPC — pagina informativa IT-alert: https://www.protezionecivile.gov.it",
            "ISO 22322:2022 — Public warning: pagina sito " + SITO_BASE + "/standard-iso/iso-22322/",
            "Direttiva del Codice Comunicazioni Elettroniche UE (cell broadcast): https://eur-lex.europa.eu",
        ],
        "focus_podcast": [
            "Cos'è IT-alert: sistema nazionale di allarme pubblico via cell broadcast (tecnologia mobile, non SMS, non app)",
            "Come arriva: notifica push speciale con suono forte anche se cellulare in silenzioso (escluso modalità aereo)",
            "Per cosa: maremoto, incidente nucleare, collasso grande diga, attività vulcanica intensa, evento esplosivo radiologico (5 scenari nazionali) + sperimentazione regionali",
            "Differenza con allerta meteo: IT-alert è per evento in corso o imminente, allerta meteo CFR è previsionale",
            "Test nazionali 2023-2025: come riconoscere un test (testo dice 'TEST') e cosa NON fare durante un test",
            "Falsi miti: \"è spam\", \"è dei russi\", \"posso disattivarlo\" — perché su iOS/Android non si disattiva sui canali governativi",
            "Cosa fare quando squilla: leggere subito, seguire le istruzioni del messaggio, NON cliccare link sospetti se ce ne sono (i veri IT-alert non hanno link cliccabili)",
            "Accessibilità: messaggi pensati per essere letti anche da chi non sente bene; futuro vibrazione e modalità accessibilità",
        ],
        "icona_emoji": "📱🚨",
    },
    "piano-familiare": {
        "titolo": "Piano familiare di emergenza: l'unica cosa che funziona quando manca tutto",
        "pagina_sito": f"{SITO_BASE}/piano-familiare/",
        "articoli_correlati": [
            f"{SITO_BASE}/rischi-prevenzione/kit-emergenza/",
            f"{SITO_BASE}/cosa-fare-adesso/",
            f"{SITO_BASE}/numeri-utili/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "Manuale 'Io non rischio — Piano famiglia' (DPC): https://iononrischio.protezionecivile.it",
            "FEMA — Family Emergency Plan: https://www.ready.gov/plan",
            "IFRC — Family preparedness toolkit: https://www.ifrc.org",
            "American Red Cross — Make a plan: https://www.redcross.org",
        ],
        "focus_podcast": [
            "Cosa è un piano familiare: 1 foglio A4 condiviso da tutti i membri della famiglia con risposte concrete",
            "Punto di incontro vicino casa (se devi uscire subito) e punto di incontro lontano (se quartiere irraggiungibile)",
            "Contatto fuori-area: una persona fuori provincia da chiamare tutti, perché le linee locali si saturano subito",
            "Bambini a scuola in emergenza: chi va a prenderli, chi è autorizzato sul registro, dove andate dopo",
            "Persone fragili in famiglia: anziano con difficoltà motorie, neonato, animale domestico — chi se ne occupa",
            "Documenti: copia digitale (cloud + chiavetta) e copia cartacea nel kit (carta identità, patente, libretto sanitario, polizze)",
            "Prove pratiche: fare la prova del piano almeno una volta all'anno (come prova evacuazione a scuola)",
            "Riadattare il piano ai rischi reali di Genzano: scossa sismica + rientro casa + verifica gas + via di fuga concreta",
        ],
        "icona_emoji": "📋👨‍👩‍👧",
    },
    "aree-emergenza": {
        "titolo": "Aree di emergenza di Genzano: dove andare se evacuano la mia via",
        "pagina_sito": f"{SITO_BASE}/cartografia/",
        "articoli_correlati": [
            f"{SITO_BASE}/piano-emergenza/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "Linee guida DPC sui Piani di Emergenza Comunali: https://www.protezionecivile.gov.it",
            "Direttiva PCM 9 novembre 2012 (piani comunali): https://www.normattiva.it",
            "Cartografia Geoportale Regione Lazio: https://geoportale.regione.lazio.it",
            "Codice della Protezione Civile (D.Lgs. 1/2018) art. 12: https://www.normattiva.it",
        ],
        "focus_podcast": [
            "Cosa sono le 'aree di emergenza': i 3 tipi previsti dal Piano Comunale (Attesa / Accoglienza / Ammassamento)",
            "Area di Attesa: prima destinazione dopo l'evento, vicina a casa, breve sosta (ore) — piazze, parcheggi",
            "Area di Accoglienza: dove si dorme se la casa è inagibile per giorni — palestre scolastiche, centri sociali, tendopoli",
            "Area di Ammassamento Soccorritori: dove si concentrano mezzi e squadre VVF/ANPAS — il cittadino NON ci va",
            "Le aree di Genzano: dove sono sulla cartografia del nostro sito, segnaletica fisica sul territorio",
            "Come ci si arriva: a piedi se vicino (preferibile), in auto solo se davvero distante (rischio code)",
            "Cosa portare: il kit di emergenza famiglia (vai-bag), documenti, farmaci, animali con trasportino",
            "Coordinamento: chi gestisce le aree (Comune + Gruppo Volontari + VVF + ASL), come saperlo (Comune, sito, 112 NON per info)",
        ],
        "icona_emoji": "🗺️🚏",
    },
    "animali-emergenza": {
        "titolo": "Animali in emergenza: come proteggere chi non può chiedere aiuto",
        "pagina_sito": f"{SITO_BASE}/formazione/kit-calamita-animali/",
        # Solo URL gia' pubblicati/stabili: gli articoli stagionali su animali
        # (11/2026 emergenze, 11/2026 stalle/fattorie, 12/2026 capodanno,
        # 07-08/2026 caldo) sono in calendario e darebbero 404 se linkati ora.
        "articoli_correlati": [
            f"{SITO_BASE}/comunicazioni/2026-04-23-cani-gatti-caldo-ondate-calore/",
            f"{SITO_BASE}/rischi-prevenzione/kit-emergenza/",
            f"{SITO_BASE}/rischi-prevenzione/persone-necessita-specifiche/",
            f"{SITO_BASE}/normativa/",
            f"{SITO_BASE}/glossario/",
        ],
        "fonti_istituzionali": [
            "🔴 Decreto del Capo del Dipartimento Protezione Civile n. 167 del 21 gennaio 2026 (GU n. 45 del 24/02/2026) — 'Indicazioni operative concernenti le attività di protezione civile in materia di soccorso e assistenza agli animali': https://www.protezionecivile.gov.it/it/normativa/decreto-cd-n-167-del-21-gennaio-2026/ — è la norma di riferimento del Sistema nazionale per gli animali in emergenza, con 3 allegati (indicazioni complete, azioni in pianificazione, azioni in emergenza)",
            "Codice della Protezione Civile (D.Lgs. 1/2018) artt. 1, 2 comma 6, 7 — base normativa citata dal DCD 167/2026: https://www.normattiva.it",
            "L. 281/1991 — Legge quadro animali d'affezione e prevenzione randagismo: https://www.normattiva.it",
            "L. 189/2004 — Reato di maltrattamento e abbandono degli animali: https://www.normattiva.it",
            "D.Lgs. 134/2022, 135/2022, 136/2022 — Identificazione animali, sanità animale, fauna selvatica (citati dal DCD 167/2026): https://www.normattiva.it",
            "Regolamenti UE 2016/429 e 2019/2035 — Malattie animali trasmissibili: https://eur-lex.europa.eu",
            "D.Lgs. 146/2001 — Protezione degli animali negli allevamenti: https://www.normattiva.it",
            "Ministero della Salute — Anagrafe canina nazionale e microchip: https://www.salute.gov.it/portale/temi/p2_6.jsp?id=212",
            "WSAVA — World Small Animal Veterinary Association, emergency preparedness: https://wsava.org",
            "ENPA — Ente Nazionale Protezione Animali, vademecum emergenze: https://www.enpa.it",
            "LAV — Lega Anti Vivisezione, sezione emergenze: https://www.lav.it",
            "ASL Roma 6 — Servizio veterinario competente per Genzano: https://www.aslroma6.it",
        ],
        "focus_podcast": [
            "🆕 Il decreto del 21 gennaio 2026 (DCD 167/2026) cambia tutto: per la prima volta il Dipartimento della Protezione Civile ha pubblicato indicazioni operative ufficiali su come gestire gli animali nelle emergenze, integrate nel Sistema Nazionale di PC (GU n. 45 del 24/02/2026)",
            "Cosa dice il DCD 167/2026 in pratica: 3 allegati — indicazioni operative complete, azioni e responsabilità in fase di pianificazione (prima dell'emergenza), azioni e responsabilità in fase di emergenza (durante e dopo)",
            "Perché gli animali contano nel piano emergenza: in tante famiglie l'animale è parte della famiglia, e il Codice PC lo riconosce esplicitamente (D.Lgs. 1/2018 artt. 1, 2 c.6, 7)",
            "Falsi miti da smontare: \"torna da solo\" (no, spesso si perde o muore), \"nei centri non li accolgono\" (oggi col DCD 167/2026 il Sistema PC li integra ufficialmente), \"l'animale capisce e segue\" (in panico scappa nella direzione sbagliata)",
            "Cosa preparare PRIMA: microchip registrato e dati aggiornati, trasportino familiare (NON solo per il viaggio dal vet), kit dedicato 7 giorni (cibo, acqua, farmaci, ciotole, lettiera, guinzaglio, oggetto familiare per ridurre stress)",
            "Carta d'identità animale: foglio A4 con foto, nome, microchip, veterinario, farmaci, alimentazione, allergie — fondamentale se vi separate (coerente con la fase 'pianificazione' del DCD 167/2026)",
            "Cosa fare DURANTE evacuazione: portarli con voi sempre che è sicuro, trasportino o guinzaglio (mai in braccio in panico), tenere distanza da altri animali stressati",
            "Cosa fare se l'animale è SPARITO durante l'evento: ricerca strutturata, foto al canile, ASL veterinaria, gruppi locali Facebook, mai \"aspettiamo che torni\"",
            "Capodanno e petardi: stress acuto, fughe, traumi — sedazione veterinaria (mai fai-da-te), stanza buia con musica, microchip funzionante",
            "Animali di stalla e fattoria: piano specifico per cavalli, bovini, ovini — evacuazione vs riparo in stalla a seconda dell'evento (incendio = evacuare, terremoto = mai correre vicino agli zoccoli); D.Lgs. 146/2001 + Reg. UE 2016/429 come quadro sanitario",
            "Animali esotici e non convenzionali (conigli, tartarughe, uccelli, rettili): bisogni termici e alimentari particolari, contattare veterinario specializzato",
            "Cosa NON fare: lasciarli chiusi in auto al sole, slegarli in un'evacuazione di massa \"così si salvano da soli\", abbandonarli (è reato L. 189/2004)",
        ],
        "icona_emoji": "🐾🦮",
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

        ### Passo 2 — Carica le fonti (5-6 click totali)

        🎯 **PASSO 2A — 1 upload (contenuti del nostro sito)**:
        nella cartella c'è un file chiamato
        `AAA-FONTI-SITO-AGGREGATE-{tema_slug}.md`. Contiene già aggregati
        TUTTI i contenuti del sito sul tema (pagina rischio + articoli
        + glossario): da 145 a 267 contenuti in un singolo file.

        In NotebookLM clicca "Aggiungi fonti" → "Carica file" → seleziona
        il file `AAA-FONTI-...`. Un solo click e hai dentro tutto il
        sito sul tema.

        🔗 **PASSO 2B — 4 incoll URL (fonti istituzionali esterne)**:
        apri il file `LINKS-DA-INCOLLARE.txt`. Vedi gli URL delle fonti
        istituzionali (DPC "Io non rischio", INGV, ISPRA, ecc.):

        Per ognuno (sono 3-5 in totale):
        1. Copia l'URL
        2. In NotebookLM clicca "Aggiungi fonti" → "Link" (o "URL")
        3. Incolla l'URL e conferma

        NotebookLM scarica e legge la pagina automaticamente. Aspetta
        che la spunta verde appaia accanto ad ogni voce (10-30 secondi).

        ⚠️ NotebookLM **non** visita link contenuti dentro a file
        caricati: per quello c'è il passo 2B (URL incollati direttamente
        come fonti).

        Totale passo 2: **5-6 click per ~270 contenuti del sito + 4-5
        fonti istituzionali ufficiali**.

        ### Passo 3 — Imposta italiano una volta sola
        - Clicca l'ingranaggio ⚙️ in alto a destra
        - Vai su "Output language" / "Lingua di output"
        - Scegli **Italiano**
        - Salva

        ### Passo 4 — Genera i 3 output
        Apri gli altri 3 file di questa cartella nell'ordine:

        1. `02-prompt-podcast.md` → clicca "Overview audio" nello Studio
           a destra, poi "Personalizza", incolla il prompt, genera, scarica audio
        2. `03-prompt-infografica.md` → clicca "Infografica", stesso
           procedimento, scarica PNG
        3. `04-prompt-presentazione.md` → clicca "Presentazione", scarica
           sia PPTX (per docenti che modificano) sia PDF (per chi vuole solo aprire)

        ℹ️ Quiz e Flashcard saltati: NotebookLM non li scarica come file,
        condivide solo un link che consumerebbe la quota PRO del tuo profilo
        a ogni visita dei cittadini sul sito. Li valuteremo in futuro come
        HTML statici nativi del sito.

        ---

        ## Dove lasciare i file scaricati

        Crea una cartella sul Desktop chiamata `notebooklm-output`
        (se non esiste già: io te la creo automaticamente con questo
        pacchetto). Dentro, c'è la sottocartella `{tema_slug}/`.

        Trascina lì i file scaricati da NotebookLM. Rinominali così:

        - Podcast audio → `podcast.m4a` (NotebookLM lo dà in M4A) o `podcast.mp3`
        - Infografica → `infografica.png`
        - Presentazione PPTX → `presentazione.pptx`
        - Presentazione PDF (stesso contenuto in PDF) → `presentazione.pdf`

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


def trova_articoli_reali(tema_slug: str, max_articoli: int = 4) -> list[str]:
    """Cerca in content/comunicazioni/ gli articoli più pertinenti al tema
    via keyword matching su body+frontmatter. Ritorna lista di URL pubblici
    REALI (mai inventati). Massimo `max_articoli` URL, ordinati per data
    decrescente (più recenti prima).

    Esclude draft e articoli senza data nel nome.
    """
    keywords = [kw.lower() for kw in KEYWORDS_TEMA.get(tema_slug, [])]
    if not keywords:
        return []
    comunicazioni_dir = REPO_ROOT / "content" / "comunicazioni"
    if not comunicazioni_dir.is_dir():
        return []

    matches = []
    for f in comunicazioni_dir.glob("*.md"):
        # Filtra per pattern data AAAA-MM-GG nel nome
        if len(f.stem) < 10 or f.stem[4] != "-" or f.stem[7] != "-":
            continue
        try:
            testo = f.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if "draft: true" in testo:
            continue
        testo_lower = testo.lower()
        # Conta quante keyword del tema appaiono (peso = pertinenza)
        score = sum(1 for kw in keywords if kw in testo_lower)
        if score > 0:
            matches.append((f.stem, score))

    # Ordina per score decrescente, poi per data decrescente (slug più recente in cima)
    matches.sort(key=lambda x: (-x[1], -ord(x[0][0]) if x[0] else 0))  # placeholder
    matches.sort(key=lambda x: x[0], reverse=True)  # data desc dal nome
    matches.sort(key=lambda x: -x[1])  # poi per score desc

    return [f"{SITO_BASE}/comunicazioni/{slug}/" for slug, _score in matches[:max_articoli]]


def aggrega_fonti_sito(tema_slug: str, tema_data: dict) -> tuple[str, int]:
    """Genera un singolo file Markdown con tutti i contenuti del sito
    pertinenti al tema, da caricare in NotebookLM come fonte unica.

    Match: keyword nel body + frontmatter di content/comunicazioni/*.md,
    più la pagina /rischi-prevenzione/<tema>.md (e altre pagine canoniche
    note come /allerte-meteo/_index.md, /rischi-prevenzione/kit-emergenza.md).

    Esclude articoli draft:true. Pagina rischio sempre come primo capitolo.
    """
    keywords = [kw.lower() for kw in KEYWORDS_TEMA.get(tema_slug, [])]
    contenuti = []  # lista di (titolo_visibile, percorso_relativo, testo_completo)

    # 1. Pagina principale del tema (canonica). Mapping slug → file sul filesystem.
    pagine_canoniche = {
        "rischio-sismico": "content/rischi-prevenzione/rischio-sismico.md",
        "rischio-idrogeologico": "content/rischi-prevenzione/rischio-idrogeologico.md",
        "rischio-incendio": "content/rischi-prevenzione/rischio-incendio.md",
        "allerta-meteo": "content/allerte-meteo/_index.md",
        "kit-emergenza": "content/rischi-prevenzione/kit-emergenza.md",
    }
    pagina_canonica = pagine_canoniche.get(tema_slug)
    if pagina_canonica:
        path = REPO_ROOT / pagina_canonica
        if path.exists():
            contenuti.append(("PAGINA PRINCIPALE", pagina_canonica, path.read_text(encoding="utf-8")))

    # 2. Articoli /comunicazioni/ pertinenti al tema (keyword matching)
    if keywords:
        comunicazioni_dir = REPO_ROOT / "content" / "comunicazioni"
        for f in sorted(comunicazioni_dir.glob("*.md")):
            try:
                testo = f.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if "draft: true" in testo:
                continue
            testo_lower = testo.lower()
            # Almeno 1 keyword deve apparire
            if any(kw in testo_lower for kw in keywords):
                contenuti.append((f"ARTICOLO: {f.stem}", f"content/comunicazioni/{f.name}", testo))

    # 3. Glossario voci pertinenti
    glossario_path = REPO_ROOT / "content" / "glossario" / "_index.md"
    if glossario_path.exists():
        glossario_text = glossario_path.read_text(encoding="utf-8")
        glossario_lower = glossario_text.lower()
        if any(kw in glossario_lower for kw in keywords):
            contenuti.append(("GLOSSARIO", "content/glossario/_index.md", glossario_text))

    # Costruisci il file aggregato
    n = len(contenuti)
    header = dedent(f"""\
        # Fonti del sito Protezione Civile Genzano — Aggregato per NotebookLM
        ## Tema: {tema_data["titolo"]}

        Questo file aggrega **{n} contenuti** del sito istituzionale di Protezione
        Civile di Genzano di Roma sul tema "{tema_data["titolo"]}".

        Origine: <https://www.protezionecivilegenzano.it>
        Generato il: (vedi data file)

        Carica questo singolo file in NotebookLM come fonte: NotebookLM lo legge
        come unica fonte tematica e ti permette di generare podcast, infografiche,
        presentazioni, quiz e flashcard basate su questi contenuti istituzionali.

        Tutti i contenuti del sito sono pubblicati con licenza CC BY-NC-SA 4.0.

        ---

    """)
    parts = [header]
    for titolo, percorso, testo in contenuti:
        parts.append(f"\n\n# ════════════════════════════════════════\n# {titolo}\n# Origine: {percorso}\n# ════════════════════════════════════════\n\n{testo}\n\n")
    return "\n".join(parts), n


def scrivi_pacchetto(tema_slug: str, tema_data: dict) -> int:
    """Scrive tutti i file nella cartella di un tema. Ritorna numero file."""
    cartella = PACCHETTI_DIR / tema_slug
    cartella.mkdir(parents=True, exist_ok=True)
    output_cartella = OUTPUT_DIR / tema_slug
    output_cartella.mkdir(parents=True, exist_ok=True)

    # Aggrega fonti del sito in un singolo MD
    fonti_aggregate, n_fonti = aggrega_fonti_sito(tema_slug, tema_data)

    # File TXT con solo gli URL puliti (uno per riga) delle fonti istituzionali
    # esterne. L'utente lo apre, copia un URL alla volta, incolla nel campo
    # "Aggiungi link" di NotebookLM. 3-5 incoll totali per tema.
    import re as _re
    links_esterni = [
        f"# URL fonti istituzionali esterne — Tema: {tema_data['titolo']}",
        "# Apri questo file, copia un URL alla volta, incollalo in NotebookLM",
        "# alla voce 'Aggiungi fonti' → 'Link'. NotebookLM scarica e legge la pagina.",
        "# (NotebookLM NON visita link contenuti in altri file: serve incollare l'URL diretto)",
        "",
        "# === Fonti istituzionali esterne raccomandate (3-5 URL): ===",
    ]
    for fonte in tema_data["fonti_istituzionali"]:
        urls = _re.findall(r"https?://[^\s,;\"<>)\]]+", fonte)
        for u in urls:
            links_esterni.append(u)
    links_esterni.append("")
    links_esterni.append("# === Pagine canoniche del nostro sito (sempre esistenti): ===")
    links_esterni.append(tema_data["pagina_sito"])
    for url in tema_data["articoli_correlati"]:
        links_esterni.append(url)

    # Articoli /comunicazioni/ DERIVATI dal filesystem via keyword matching.
    # SEMPRE URL reali (file .md effettivamente presenti in content/comunicazioni/).
    articoli_reali = trova_articoli_reali(tema_slug, max_articoli=4)
    if articoli_reali:
        links_esterni.append("")
        links_esterni.append("# === Articoli /comunicazioni/ pertinenti al tema ===")
        links_esterni.append("# (Già aggregati nel file MD principale, qui solo come riferimento)")
        for url in articoli_reali:
            links_esterni.append(url)

    # Pulizia file ridondanti/deprecati da generazioni precedenti.
    # - 01-fonti.md → ridondante con AAA-FONTI + LINKS-DA-INCOLLARE
    # - 05-prompt-quiz.md / 06-prompt-flashcard.md → NotebookLM non fornisce
    #   download diretto, solo link condivisi che consumerebbero quota PRO
    #   del proprietario notebook ad ogni visita utente. Saltati per ora;
    #   se servirà in futuro li gestiremo come HTML statici nativi del sito.
    for vecchio_nome in ("01-fonti.md", "05-prompt-quiz.md", "06-prompt-flashcard.md"):
        vecchio = cartella / vecchio_nome
        if vecchio.exists():
            vecchio.unlink()

    files = {
        "00-INDICE.md": indice_md(tema_slug, tema_data),
        "02-prompt-podcast.md": prompt_podcast(tema_data),
        "03-prompt-infografica.md": prompt_infografica(tema_data),
        "04-prompt-presentazione.md": prompt_presentazione(tema_data),
        f"AAA-FONTI-SITO-AGGREGATE-{tema_slug}.md": fonti_aggregate,
        "LINKS-DA-INCOLLARE.txt": "\n".join(links_esterni) + "\n",
    }

    for nome, contenuto in files.items():
        (cartella / nome).write_text(contenuto, encoding="utf-8")

    # Stampa info aggregazione
    print(f"     fonti aggregate: {n_fonti} contenuti del sito in 1 unico file")
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
