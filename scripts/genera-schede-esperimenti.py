#!/usr/bin/env python3
"""Genera il documento stampabile A4 degli esperimenti di protezione civile.

Produce static/formazione/schede-stampabili/esperimenti-protezione-civile/index.html:
un unico documento con un .scheda-page per esperimento (1 esperimento = 1 foglio A4),
con page-break forzato in stampa e supporto ?autoprint=1, coerente con il template
scheda-print.css e con il pattern dei "pacchetti" di stampa già usati sul sito.

I contenuti sono la versione stampabile (sintetica) della pagina Hugo
/formazione/esperimenti/. Per modificare un esperimento, edita la lista ESPERIMENTI
qui sotto e rilancia: python3 scripts/genera-schede-esperimenti.py
"""
from html import escape
from pathlib import Path

OUT = Path("static/formazione/schede-stampabili/esperimenti-protezione-civile/index.html")

# eta: stringa con badge emoji + fascia ; materiali: stringa ; passi: lista ;
# impara: stringa ; pc: stringa (taglio protezione civile) ; sicurezza: stringa|None
ESPERIMENTI = [
    {
        "tema": "Vulcani", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Vulcano lento o vulcano esplosivo?",
        "materiali": "Due bicchieri, una cannuccia, acqua, purè di patate denso (o ketchup).",
        "passi": [
            "Metti l'acqua nel primo bicchiere e il purè denso nel secondo.",
            "Soffia piano con la cannuccia nell'acqua: l'aria esce facile e tranquilla.",
            "Soffia nel purè: l'aria fatica, si accumula e poi \"scoppia\" schizzando.",
        ],
        "impara": "La viscosità (densità) del magma decide il tipo di eruzione: magma fluido = eruzione dolce (effusiva); magma denso = eruzione violenta (esplosiva).",
        "pc": "Vulcani diversi si monitorano in modo diverso e le vie di evacuazione cambiano col tipo di rischio. Sul sito: «Il vulcanismo dei Colli Albani».",
        "sicurezza": None,
    },
    {
        "tema": "Terremoti", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Il terremoto di gelatina",
        "materiali": "Una teglia di gelatina solida e compatta, stuzzicadenti, marshmallow (o cubetti di formaggio).",
        "passi": [
            "Costruisci delle torrette infilando gli stuzzicadenti nei marshmallow.",
            "Appoggia le torri sulla gelatina.",
            "Scuoti delicatamente la teglia: simuli le onde sismiche (ondulatorie, di lato, e sussultorie, dall'alto in basso).",
        ],
        "impara": "La gelatina si comporta come un terreno molle, che amplifica le scosse. Le torri alte e strette cadono; quelle basse, larghe alla base o rinforzate a triangolo, resistono.",
        "pc": "Il terremoto non si può evitare, ma le case sicure sì: è la prevenzione edilizia (edilizia antisismica). Sul sito: «Il rischio sismico in Italia».",
        "sicurezza": "Gli stuzzicadenti sono appuntiti: usali con un adulto.",
    },
    {
        "tema": "Frane e alluvioni", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "La spugna e il fango",
        "materiali": "Una spugna da cucina asciutta, un piatto, acqua, un po' di terra o sabbia.",
        "passi": [
            "Appoggia la spugna inclinata sul piatto e mettici sopra un po' di terra.",
            "Versa l'acqua prima goccia a goccia: la spugna assorbe.",
            "Versa l'acqua tutta insieme: la spugna si satura e l'acqua scorre via trascinando la terra.",
        ],
        "impara": "Il terreno ha un limite di assorbimento. Quando piove troppo e troppo in fretta, si satura, cede e può franare.",
        "pc": "È il motivo dei livelli di allerta meteo (gialla, arancione, rossa) legati alla pioggia attesa. Sul sito: «Il rischio idrogeologico» e «Allerte meteo».",
        "sicurezza": None,
    },
    {
        "tema": "Frane e alluvioni", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Le radici che tengono la terra",
        "materiali": "Due vaschette inclinate (una con terra nuda, una con una zolla di erba con radici), due bottiglie col tappo forato.",
        "passi": [
            "Riempi una vaschetta con terra nuda e l'altra con terra coperta da una zolla d'erba.",
            "Fai \"piovere\" con forza su entrambe usando le bottiglie forate.",
            "Osserva e confronta l'acqua che esce dal fondo delle due vaschette.",
        ],
        "impara": "Dalla terra nuda esce acqua marrone e si formano solchi (erosione); dalla terra con l'erba esce acqua più pulita e il terreno resta fermo. Le radici trattengono il suolo.",
        "pc": "Spiega perché disboscare o cementificare aumenta il rischio di frane e alluvioni: il verde è una difesa del territorio.",
        "sicurezza": None,
    },
    {
        "tema": "Alluvioni urbane", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Città di asfalto, città di prato",
        "materiali": "Due vassoi (uno con terra o un panno spugnoso, uno con un foglio di plastica liscio), una bottiglia d'acqua.",
        "passi": [
            "Inclina entrambi i vassoi sopra un lavandino.",
            "Versa la stessa quantità d'acqua su ciascuno.",
            "Cronometra quanto tempo impiega l'acqua a scorrere via in ognuno.",
        ],
        "impara": "Sul terreno l'acqua si infiltra lentamente; sulla superficie liscia scorre tutta e subito. Più asfalto e cemento (consumo di suolo) = più acqua verso fognature e fossi, che si sovraccaricano.",
        "pc": "È il motivo per cui gli allagamenti urbani colpiscono anche zone lontane dai fiumi. Sul sito: «Il rischio idrogeologico».",
        "sicurezza": None,
    },
    {
        "tema": "Maremoti", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "L'onda di maremoto",
        "materiali": "Una vaschetta lunga (o teglia) con un po' d'acqua, un libretto o una paletta.",
        "passi": [
            "Tieni un lato della vaschetta un po' più alto, come una spiaggia in pendenza.",
            "Dai una spinta decisa all'acqua con la paletta dal lato profondo.",
            "Osserva l'onda che corre verso il lato basso e cresce avvicinandosi.",
        ],
        "impara": "L'onda nasce da uno spostamento improvviso di tanta acqua (terremoto sottomarino, frana, eruzione) e cresce quando arriva vicino alla riva. Non è l'onda del vento: ha molta più forza.",
        "pc": "Al mare, se senti un forte terremoto o vedi il mare ritirarsi all'improvviso, allontanati subito verso un punto alto. Sul sito: «Il rischio da maremoto».",
        "sicurezza": None,
    },
    {
        "tema": "Incendi boschivi", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Il triangolo del fuoco",
        "materiali": "Una candelina, un barattolo di vetro, un piattino.",
        "passi": [
            "Un adulto accende la candelina sul piattino.",
            "Coprite la candelina con il barattolo capovolto.",
            "Osservate: dopo pochi secondi la fiamma si indebolisce e si spegne.",
        ],
        "impara": "La fiamma si spegne perché nel barattolo l'ossigeno si riduce (basta che scenda sotto un certo livello). Per bruciare il fuoco ha bisogno di tre cose insieme — il triangolo del fuoco: combustibile, comburente (ossigeno) e calore. Togline una e il fuoco si spegne.",
        "pc": "È il principio dello spegnimento: le linee tagliafuoco tolgono il combustibile, l'acqua toglie il calore. Sul sito: «Il rischio da incendi boschivi».",
        "sicurezza": "C'è una fiamma: SOLO con un adulto, mai per l'infanzia. Tieni lontani capelli, maniche e carta; non lasciare la candela incustodita.",
    },
    {
        "tema": "Ondate di calore", "eta": "🟢 Infanzia · 🔵 Primaria",
        "titolo": "Sole o ombra? Chiaro o scuro?",
        "materiali": "Due termometri (o uno da spostare), un foglio bianco e uno nero, un posto al sole.",
        "passi": [
            "Metti un termometro al sole e uno all'ombra; confronta dopo dieci minuti.",
            "Al sole, appoggia un termometro sotto il foglio nero e uno sotto il bianco.",
            "Confronta le temperature.",
        ],
        "impara": "All'ombra fa molto più fresco e i colori scuri si scaldano più di quelli chiari.",
        "pc": "Sono le regole delle ondate di calore: stare all'ombra nelle ore calde, vestirsi leggeri e chiari, bere spesso. Sul sito: «Ondate di calore».",
        "sicurezza": None,
    },
    {
        "tema": "Neve e gelo", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Il sale che scioglie il ghiaccio",
        "materiali": "Due cubetti di ghiaccio uguali, due piattini, un cucchiaino di sale.",
        "passi": [
            "Metti un cubetto su ciascun piattino.",
            "Spargi il sale solo su uno dei due.",
            "Aspetta e osserva quale cubetto si scioglie prima.",
        ],
        "impara": "Il sale abbassa la temperatura a cui l'acqua ghiaccia, così il ghiaccio col sale si scioglie più in fretta.",
        "pc": "Ecco perché d'inverno si sparge il sale sulle strade ghiacciate. Attenzione al ghiaccio nero, sottile e quasi invisibile. Sul sito: «Il rischio da neve e gelo».",
        "sicurezza": None,
    },
    {
        "tema": "Vento forte", "eta": "🟢 Infanzia · 🔵 Primaria",
        "titolo": "La forza del vento (la manica a vento)",
        "materiali": "Un sacchetto di plastica leggero o un calzino, un cerchio di cartoncino, dello spago, un bastoncino.",
        "passi": [
            "Fissa l'apertura del sacchetto al cerchio di cartoncino.",
            "Lega lo spago e appendi la manica a vento all'aperto.",
            "Osserva come si gonfia e in che direzione punta.",
        ],
        "impara": "La manica mostra direzione e forza del vento: più si alza in orizzontale, più il vento è forte.",
        "pc": "Con il vento forte gli oggetti volano e gli alberi possono cadere. Sul sito: «Cosa fare con il vento forte».",
        "sicurezza": None,
    },
    {
        "tema": "Temporali e fulmini", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Quanto è lontano il temporale?",
        "materiali": "Gli occhi, le orecchie e un modo per contare. Si osserva da un luogo sicuro, al chiuso.",
        "passi": [
            "Quando vedi un lampo, conta i secondi fino al tuono.",
            "Dividi per 3: ottieni circa la distanza del temporale in chilometri.",
            "Ripeti: se i secondi diminuiscono, il temporale si avvicina.",
        ],
        "impara": "La luce arriva subito, il suono molto più piano. Se tra lampo e tuono passano meno di 30 secondi, sei in zona di pericolo: meglio stare al riparo. Variante: strofina un palloncino sui capelli e avvicinalo a un dito al buio — la scintilla è elettricità statica, come un mini fulmine.",
        "pc": "Durante un temporale resta al chiuso, lontano da alberi isolati e specchi d'acqua. Sul sito: «Cosa fare con i temporali intensi».",
        "sicurezza": "Si osserva SOLO da dentro casa o da un luogo riparato, mai all'aperto durante il temporale.",
    },
    {
        "tema": "Siccità", "eta": "🟢 Infanzia · 🔵 Primaria",
        "titolo": "L'acqua che sparisce",
        "materiali": "Due piattini con la stessa quantità d'acqua, un pennarello per segnare il livello.",
        "passi": [
            "Segna il livello dell'acqua in entrambi i piattini.",
            "Metti un piattino al sole e uno all'ombra.",
            "Controlla il livello dopo qualche ora e il giorno dopo.",
        ],
        "impara": "Al sole e con il caldo l'acqua evapora più in fretta. Con poche piogge e tanto caldo, l'acqua disponibile diminuisce.",
        "pc": "È la siccità, un rischio lento. Risparmiare acqua (chiudere il rubinetto, segnalare le perdite) aiuta tutti. Sul sito: «Il rischio da deficit idrico».",
        "sicurezza": None,
    },
    {
        "tema": "Rischio chimico", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Come si sparge una \"nube\"",
        "materiali": "Un batuffolo con qualche goccia di vaniglia, profumo o un po' di caffè (un odore forte e innocuo).",
        "passi": [
            "Mettiti in un angolo della stanza con il batuffolo chiuso.",
            "I compagni si dispongono fermi in punti diversi della stanza.",
            "Apri il batuffolo: ognuno alza la mano appena sente l'odore.",
        ],
        "impara": "L'odore, come un gas, si diffonde nell'aria e si sposta con le correnti: raggiunge prima chi è vicino e sottovento.",
        "pc": "In caso di nube tossica da un incidente industriale, spesso la cosa giusta NON è scappare ma chiudersi in casa (chiudere porte, finestre e aerazione) e seguire le autorità. Sul sito: «Il rischio chimico-industriale».",
        "sicurezza": "Usa solo sostanze innocue (vaniglia, caffè): mai prodotti chimici o spray irritanti.",
    },
    {
        "tema": "Rischio sanitario", "eta": "🟢 Infanzia · 🔵 Primaria",
        "titolo": "Caccia ai germi (il potere del sapone)",
        "materiali": "Un piatto fondo con acqua, pepe macinato, un goccio di sapone per piatti.",
        "passi": [
            "Spargi il pepe sull'acqua: sono i \"germi\".",
            "Tocca l'acqua con un dito pulito: il pepe resta lì.",
            "Bagna il dito nel sapone e ritocca l'acqua: il pepe \"scappa\" verso i bordi.",
        ],
        "impara": "Il sapone rompe la tensione dell'acqua e allontana lo sporco: ecco perché lavarsi le mani col sapone funziona davvero. (Variante: glitter sulle mani da togliere prima con sola acqua, poi col sapone.)",
        "pc": "L'igiene è la prima difesa contro le epidemie. Sul sito: «Il rischio sanitario».",
        "sicurezza": None,
    },
    {
        "tema": "Rischio nucleare", "eta": "🟠 Ragazzi",
        "titolo": "Più lontano, più al riparo",
        "materiali": "Una torcia (o la luce del telefono), un righello, un libro spesso.",
        "passi": [
            "Punta la torcia sulla mano da vicino: la luce è forte.",
            "Allontana la torcia: la luce sulla mano diventa più debole.",
            "Metti il libro tra la torcia e la mano: la luce non passa.",
        ],
        "impara": "È un'analogia (la luce si vede, le radiazioni no): più sei lontano dalla fonte e più il tempo è breve, meno energia ricevi; un muro (schermatura) ti protegge.",
        "pc": "Sono i tre principi della radioprotezione — distanza, tempo, schermatura. Sul sito: «Il rischio nucleare e radiologico».",
        "sicurezza": None,
    },
    {
        "tema": "Prepararsi", "eta": "🟢 Infanzia · 🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Cosa metto nello zaino?",
        "materiali": "Uno zaino e tanti oggetti (torcia, radio a pile, bottiglia d'acqua, fischietto, una barretta, un peluche, le chiavi, un videogioco, un fumetto, una coperta…).",
        "passi": [
            "Disponi tutti gli oggetti sul tavolo.",
            "Sfida a tempo (2 minuti): metti nello zaino solo le cose davvero indispensabili in un'emergenza.",
            "Alla fine analizzate insieme le scelte.",
        ],
        "impara": "A dare priorità a sicurezza e comunicazione: fischietto per farsi sentire, torcia per il buio, acqua, radio per le notizie. Il peluche può restare: serve a stare tranquilli.",
        "pc": "È il kit di emergenza di famiglia. Sul sito: «Kit di emergenza».",
        "sicurezza": None,
    },
    {
        "tema": "Pianificare", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "La mappa dei pericoli e dei luoghi sicuri",
        "materiali": "Carta e colori.",
        "passi": [
            "Disegnate la pianta della casa (o della classe).",
            "Segnate in rosso i pericoli (mensole non fissate, oggetti sopra i letti, vetri, prese sovraccariche) e in verde i punti più sicuri.",
            "Segnate dove sono gli interruttori generali di luce e gas.",
        ],
        "impara": "Ad allenare lo sguardo a riconoscere i punti critici prima che accada qualcosa.",
        "pc": "Durante un terremoto la regola è «mi getto, mi copro, resto»: sotto un tavolo robusto, lontano da finestre e mobili alti, proteggendo la testa. Le porte e gli architravi NON sono posti sicuri e NON si usano gli ascensori. Sul sito: «Piano familiare».",
        "sicurezza": None,
    },
    {
        "tema": "Segnaletica", "eta": "🟢 Infanzia · 🔵 Primaria",
        "titolo": "Memory dei segnali di sicurezza",
        "materiali": "Cartoncini con i simboli di sicurezza (uscita di emergenza, punto di raccolta, estintore, direzione di evacuazione).",
        "passi": [
            "Prepara le coppie di cartoncini con i simboli.",
            "Gioca a memory, oppure nascondi i cartelli per la stanza.",
            "Chi trova un cartello spiega o mima cosa fare quando lo vede.",
        ],
        "impara": "A riconoscere la segnaletica di emergenza che si trova a scuola, al supermercato, al cinema.",
        "pc": "Sono i segnali internazionali ISO 7010. Trovi i simboli da stampare nel catalogo dei pittogrammi del sito.",
        "sicurezza": None,
    },
    {
        "tema": "Comunicazione", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "La chiamata perfetta al 112",
        "materiali": "Due telefoni giocattolo (o spenti).",
        "passi": [
            "Un adulto fa l'operatore del 112, il bambino è il cittadino.",
            "L'adulto propone uno scenario (es.: «Flavia vede del fumo dal bosco dietro casa») e fa domande.",
            "Il bambino risponde con calma: chi è, cosa vede e soprattutto dove si trova esattamente.",
        ],
        "impara": "Gli operatori hanno bisogno di informazioni precise per mandare i soccorsi giusti. Urlare o piangere non aiuta: la calma e la precisione sì.",
        "pc": "Il 112 è il Numero Unico di Emergenza, l'unico da chiamare nel Lazio. Sul sito: gioco «La chiamata al 112» e «Numeri utili».",
        "sicurezza": None,
    },
    {
        "tema": "Comunicazione", "eta": "🟢 Infanzia · 🔵 Primaria",
        "titolo": "Il telefono con i bicchieri",
        "materiali": "Due bicchieri di plastica, uno spago lungo, uno stuzzicadenti.",
        "passi": [
            "Fai un forellino sul fondo di ogni bicchiere.",
            "Fai passare lo spago e fermalo con un pezzetto di stuzzicadenti.",
            "Tendete bene lo spago: uno parla nel bicchiere, l'altro ascolta.",
        ],
        "impara": "La voce viaggia come vibrazione lungo lo spago teso. La comunicazione ha bisogno di un canale che funzioni.",
        "pc": "In emergenza le reti telefoniche possono cadere: per questo i volontari usano la radio, che non dipende dalla rete dei cellulari. Sul sito: «Telecomunicazioni in emergenza».",
        "sicurezza": None,
    },
    {
        "tema": "Evacuazione", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Il percorso al buio",
        "materiali": "Una benda per gli occhi, qualche ostacolo morbido.",
        "passi": [
            "In una stanza sicura crea un piccolo percorso con ostacoli morbidi.",
            "Benda un bambino (come se ci fosse fumo o un blackout).",
            "Un compagno lo guida verso l'uscita usando solo la voce, con indicazioni chiare. Poi si invertono i ruoli.",
        ],
        "impara": "L'importanza dell'ascolto, della calma e di avere una guida designata durante un'evacuazione.",
        "pc": "Con fumo o poca luce si esce piegati, vicino al pavimento dove l'aria è più pulita, seguendo la segnaletica e chi guida. Sul sito: «Cosa fare in caso di blackout».",
        "sicurezza": "Usa ostacoli morbidi e libera il pavimento; un adulto sorveglia sempre il percorso.",
    },
]

HEAD = """<!DOCTYPE html>
<html lang="it" dir="ltr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Schede stampabili: Esperimenti di protezione civile (A4)</title>
  <meta name="description" content="Schede A4 stampabili: {n} esperimenti e attività di protezione civile per la scuola e la famiglia. Un esperimento per foglio. Stampa tutto o solo le pagine che ti servono.">
  <meta name="robots" content="index, follow">
  <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
  <link rel="stylesheet" href="/formazione/schede-stampabili/assets/scheda-print.css">
  <style>
    .esp-intro {{
      max-width: 21cm; margin: 1rem auto 0; padding: 0.8rem 1.2rem;
      background: #eaf2fb; border-left: 4px solid var(--scheda-blu);
      border-radius: 0 8px 8px 0; font-size: 0.95rem; line-height: 1.5; color: #333;
    }}
    .esp-passi {{ margin: 0.3rem 0 0.6rem 1.1rem; padding: 0; }}
    .esp-passi li {{ margin-bottom: 0.3rem; line-height: 1.45; }}
    .esp-block {{ margin: 0.5rem 0; line-height: 1.5; }}
    .esp-block .et {{ color: var(--scheda-blu); font-weight: 700; }}
    .esp-pc {{
      margin: 0.5rem 0; padding: 0.55rem 0.85rem;
      background: #eaf2fb; border-left: 4px solid var(--scheda-blu);
      border-radius: 0 6px 6px 0; font-size: 0.92rem; line-height: 1.45;
    }}
    .esp-sicurezza {{
      margin: 0.5rem 0; padding: 0.55rem 0.85rem;
      background: #fff8e6; border-left: 4px solid var(--scheda-oro);
      border-radius: 0 6px 6px 0; font-size: 0.9rem; line-height: 1.45; color: #664d03;
    }}
    /* Stampa: forza un esperimento per foglio A4 */
    @media print {{
      .scheda-toolbar, .esp-intro, .no-print {{ display: none !important; }}
      body {{ background: #fff; }}
      .scheda-page {{ page-break-after: always; break-after: page; }}
      .scheda-page:last-of-type {{ page-break-after: auto; break-after: auto; }}
    }}
  </style>
</head>
<body>
  <div class="scheda-toolbar no-print">
    <a href="/formazione/schede-stampabili/">&larr; Torna alle schede</a>
    <span class="scheda-titolo">Esperimenti di protezione civile &mdash; {n} schede A4</span>
    <button type="button" onclick="window.print()">&#128424;&#65039; Stampa o salva come PDF</button>
  </div>

  <div class="esp-intro no-print">
    <strong>Un esperimento per foglio.</strong> Puoi stampare tutto il fascicolo oppure, dalla finestra di stampa, scegliere <strong>solo le pagine</strong> che ti servono. Ogni scheda indica età consigliata, materiali, procedura, cosa si impara e le note di sicurezza. Versione completa e interattiva: <a href="/formazione/esperimenti/">Esperimenti e attività di protezione civile</a>.
  </div>
"""

PAGE = """
  <article class="scheda-page">
    <header class="scheda-header">
      <div class="scheda-logo" aria-hidden="true">PC</div>
      <div class="scheda-intestazione">
        <div class="scheda-ente">Protezione Civile &mdash; Genzano di Roma</div>
        <h1 class="scheda-titolo-principale">{titolo}</h1>
        <div class="scheda-sottotitolo">Esperimento di protezione civile &mdash; {tema}</div>
      </div>
    </header>

    <div class="scheda-meta">
      <span><strong>Et&agrave; consigliata:</strong> {eta}</span>
      <span><strong>Tema:</strong> {tema}</span>
    </div>

    <div class="esp-block"><span class="et">Materiali.</span> {materiali}</div>

    <h2 class="scheda-h2">Come si fa</h2>
    <ol class="esp-passi">
{passi}
    </ol>

    <div class="esp-block"><span class="et">Cosa si impara.</span> {impara}</div>

    <div class="esp-pc"><strong>In chiave protezione civile.</strong> {pc}</div>
{sicurezza}
    <h2 class="scheda-h2">&#9999;&#65039; Cosa ho osservato</h2>
    <div class="scheda-box-disegno" style="min-height: 4.5rem;"></div>

    <footer class="scheda-footer">
      <span class="scheda-site">protezionecivilegenzano.it</span>
      <span>Esperimenti di protezione civile &middot; {tema} &middot; rev. 2026</span>
    </footer>
  </article>
"""

FOOT = """
  <script>
    // Auto-stampa se chiamato con ?autoprint=1
    (function() {
      try {
        var params = new URLSearchParams(window.location.search);
        if (params.get('autoprint') === '1') {
          window.addEventListener('load', function() {
            setTimeout(function() { window.print(); }, 800);
          });
        }
      } catch (e) {}
    })();
  </script>
</body>
</html>
"""


def render():
    n = len(ESPERIMENTI)
    parts = [HEAD.format(n=n)]
    for e in ESPERIMENTI:
        passi = "\n".join(
            "      <li>{}</li>".format(escape(p)) for p in e["passi"]
        )
        sicurezza = ""
        if e.get("sicurezza"):
            sicurezza = '    <div class="esp-sicurezza"><strong>&#9888;&#65039; Sicurezza.</strong> {}</div>\n'.format(
                escape(e["sicurezza"])
            )
        parts.append(
            PAGE.format(
                titolo=escape(e["titolo"]),
                tema=escape(e["tema"]),
                eta=escape(e["eta"]),
                materiali=escape(e["materiali"]),
                passi=passi,
                impara=escape(e["impara"]),
                pc=escape(e["pc"]),
                sicurezza=sicurezza,
            )
        )
    parts.append(FOOT)
    return "".join(parts)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(), encoding="utf-8")
    print(f"Scritto {OUT} ({len(ESPERIMENTI)} schede)")


if __name__ == "__main__":
    main()
