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
import sys
from html import escape
from pathlib import Path

# Le illustrazioni vivono in un modulo a parte: sono tante e hanno una loro
# libreria di primitive, tenerle qui renderebbe illeggibile la lista dei testi.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from illustrazioni_esperimenti import figura, mancanti  # noqa: E402

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
        "impara": "Conta quanto il magma è vischioso, cioè quanta fatica fa a scorrere: non è la stessa cosa della densità, che dice quanto pesa a parità di volume. Nel magma fluido i gas escono man mano; in quello vischioso restano intrappolati, la pressione cresce e l'eruzione è esplosiva. Sono i gas a far scoppiare l'eruzione, il magma vischioso li trattiene.",
        "pc": "Vulcani diversi si monitorano in modo diverso e le vie di evacuazione cambiano col tipo di rischio. Sul sito: «Il vulcanismo dei Colli Albani».",
        "sicurezza": None,
    },
    {
        "tema": "Terremoti", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Il terremoto di gelatina",
        "materiali": "Una teglia di gelatina solida e compatta, stuzzicadenti, marshmallow (o cubetti di formaggio).",
        "passi": [
            "Costruisci due torrette uguali infilando gli stuzzicadenti nei marshmallow.",
            "Appoggia una torre sulla gelatina e l'altra accanto, sul fondo rigido della teglia o su un tagliere.",
            "Scuoti delicatamente la teglia sempre allo stesso modo: simuli le onde sismiche (ondulatorie, di lato, e sussultorie, dall'alto in basso).",
            "Guarda quale delle due oscilla di più. Poi rifai la prova con una torre alta e una bassa, tutte e due sulla gelatina.",
        ],
        "impara": "La stessa torre oscilla molto di più sulla gelatina che sul fondo rigido: il terreno molle amplifica le scosse. E fra due torri sulla stessa gelatina, quella alta e stretta si muove più di quella bassa e larga. Attenzione: non vuol dire che una casa bassa sia sempre più sicura di una casa alta — conta come è costruita, non solo quanto è alta.",
        "pc": "Il terremoto non si può impedire, ma si possono costruire e rinforzare case che lo reggono: è la prevenzione edilizia (edilizia antisismica). Sul sito: «Il rischio sismico in Italia».",
        "sicurezza": "Gli stuzzicadenti sono appuntiti: usali con un adulto.",
    },
    {
        "tema": "Terremoti", "eta": "🟠 Ragazzi",
        "titolo": "Quando il terreno perde sostegno",
        "domanda": "Come fa un terreno solido a comportarsi come un liquido durante un terremoto?",
        "materiali": "Due contenitori trasparenti uguali, sabbia fine, acqua, due oggetti pesanti piccoli e uguali (due biglie di vetro o due dadi da brodo), un tavolo su cui battere.",
        "passi": [
            "Riempi il primo contenitore di sabbia asciutta e appoggia una biglia sulla superficie.",
            "Riempi il secondo con la stessa sabbia e aggiungi acqua fino a bagnarla tutta, senza che resti uno strato d'acqua sopra; appoggia l'altra biglia.",
            "Batti le mani sul tavolo vicino ai due contenitori, allo stesso modo per dieci secondi.",
            "Guarda le due biglie: nella sabbia satura la biglia affonda, in quella asciutta resta dov'è.",
        ],
        "cambia": "Solo l'acqua nella sabbia: stessa sabbia, stessa biglia, stesse vibrazioni.",
        "atteso": "Nella sabbia satura la biglia sprofonda e la superficie diventa lucida; nella sabbia asciutta non succede quasi nulla.",
        "impara": "In un terreno sabbioso pieno d'acqua le vibrazioni fanno perdere il contatto fra i granelli: per qualche secondo il terreno si comporta come un liquido e non sostiene più quello che ci sta sopra. Si chiama liquefazione, e l'acqua nel terreno è la condizione che la rende possibile.",
        "limite": "Qui le vibrazioni durano pochi secondi e la scala è quella di una bacinella: in un terremoto vero il fenomeno riguarda strati di terreno profondi diversi metri e coinvolge le fondazioni degli edifici.",
        "pc": "Per questo la carta della pericolosità sismica locale guarda anche che terreno c'è sotto, non solo quanto forte può essere la scossa: lo stesso terremoto fa danni diversi su roccia e su sabbia satura.",
        "sicurezza": "Si batte sul tavolo, non sui contenitori. Asciuga subito l'acqua versata: il pavimento bagnato scivola.",
    },
    {
        "tema": "Terremoti", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Costruiamo un sismografo",
        "domanda": "Come si fa a registrare un movimento che dura pochi secondi?",
        "materiali": "Una scatola di cartone robusta, un bicchiere di plastica, dello spago, un pennarello a punta fine, qualche sasso o monete, una striscia di carta lunga (va bene un rotolo da cassa).",
        "passi": [
            "Ritaglia una finestra sul lato della scatola e fai passare la striscia di carta da parte a parte, così puoi tirarla piano.",
            "Buca il fondo del bicchiere, infilaci il pennarello con la punta che sfiora la carta e riempilo di sassi.",
            "Appendi il bicchiere allo spago al centro della scatola: deve restare fermo e sospeso, sfiorando la carta.",
            "Uno tira la striscia piano e sempre uguale, un altro scuote la scatola: prima poco, poi forte, poi di nuovo poco.",
        ],
        "cambia": "Quanto forte si scuote la scatola. La velocità con cui si tira la carta resta la stessa.",
        "atteso": "Sulla carta compare una linea quasi dritta quando la scatola è ferma, e zig-zag tanto più ampi quanto più forte si scuote.",
        "impara": "Il pennarello resta fermo per inerzia mentre il foglio si muove con la terra: così si registra un terremoto. Il tracciato dice quanto e per quanto ha tremato: racconta un terremoto già avvenuto. Nessuno strumento prevede quando arriverà il prossimo.",
        "limite": "Un sismografo vero registra frazioni di millimetro in tre direzioni; questo vede solo gli scossoni grossi, in un verso solo.",
        "pc": "L'INGV registra così i terremoti italiani e li pubblica in pochi minuti: li trovi nel cruscotto del sito, scheda «Terremoti».",
        "sicurezza": "Il buco nel bicchiere lo fa un adulto. La scatola si scuote appoggiata al tavolo, non sollevata.",
    },
    {
        "tema": "Terremoti", "eta": "🟠 Ragazzi",
        "titolo": "Il ritmo che fa oscillare una torre",
        "domanda": "Perché in uno stesso terremoto un palazzo oscilla moltissimo e quello accanto quasi niente?",
        "materiali": "Un cartoncino rigido come base, tre cannucce o listelli flessibili di altezza diversa (10, 20 e 30 cm), pongo o nastro biadesivo, tre gommini uguali da mettere in cima.",
        "passi": [
            "Fissa le tre cannucce in piedi sulla base con il pongo e metti un gommino in cima a ciascuna: sono tre edifici di altezza diversa.",
            "Muovi la base avanti e indietro molto lentamente, con un ritmo regolare: guarda quale torre oscilla di più.",
            "Aumenta un po' il ritmo, sempre regolare, e guarda di nuovo. Poi vai veloce.",
            "Per ogni ritmo segna quale torre si muove di più.",
        ],
        "cambia": "Solo la frequenza con cui muovi la base: l'ampiezza del movimento resta la stessa.",
        "atteso": "Ogni torre ha il suo ritmo: la più alta risponde ai movimenti lenti, la più bassa a quelli veloci. Al ritmo giusto una torre oscilla moltissimo mentre le altre due restano quasi ferme.",
        "impara": "Ogni struttura ha una frequenza propria. Quando il terreno si muove con quel ritmo, le oscillazioni si sommano invece di annullarsi: è la risonanza. Non esiste quindi un'altezza «sicura»: dipende da come il ritmo dell'edificio incontra il ritmo del terremoto.",
        "limite": "Un edificio vero ha molte frequenze proprie, non una sola, e la sua risposta dipende da materiali, fondazioni e collegamenti fra le parti.",
        "pc": "È il motivo per cui la normativa antisismica fa calcolare il comportamento dinamico dell'edificio, non solo la sua resistenza a spinta ferma.",
        "sicurezza": None,
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
        "tema": "Misurare la pioggia", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Quanta pioggia è caduta?",
        "domanda": "Quando il bollettino dice «50 millimetri di pioggia», quanta acqua è caduta davvero?",
        "materiali": "Una bottiglia di plastica trasparente da 1,5 litri, forbici, un righello, nastro adesivo, un pennarello indelebile, qualche sasso.",
        "passi": [
            "Un adulto taglia la bottiglia all'altezza della spalla: sotto è il bicchiere, la parte di sopra capovolta fa da imbuto.",
            "Metti i sassi sul fondo perché non voli via, incastra l'imbuto e fissa il righello fuori, con lo zero al fondo piatto.",
            "Riempi d'acqua fino allo zero: è il livello di partenza, perché il fondo della bottiglia non è piatto davvero.",
            "Mettilo all'aperto lontano da muri e alberi. Ogni giorno alla stessa ora leggi i millimetri, segnali in tabella e svuoti fino allo zero.",
        ],
        "cambia": "Solo la giornata: posizione, ora della lettura e livello di partenza restano uguali.",
        "atteso": "In una pioggia normale salgono pochi millimetri; in un temporale forte anche 20-30 in poche ore.",
        "impara": "Un millimetro di pioggia è un litro d'acqua per ogni metro quadrato. Il numero del bollettino è una previsione, il tuo è una misura: confrontarli fa capire la differenza.",
        "limite": "Misuri un punto solo: un temporale può scaricare il doppio a trecento metri. Per questo il Centro Funzionale usa una rete di stazioni e il radar.",
        "pc": "I livelli di allerta nascono dalla pioggia attesa su un'intera zona. Sul sito: «Allerte meteo» e «Laboratorio meteo», per confrontare le tue misure con le serie storiche.",
        "sicurezza": "Il taglio lo fa un adulto. Non si esce a leggere durante il temporale: si aspetta che passi.",
    },
    {
        "tema": "Maremoti", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "L'onda di maremoto",
        "materiali": "Una vaschetta lunga (o teglia) con un po' d'acqua, un libretto o una paletta.",
        "passi": [
            "Metti un libro sotto un\u2019estremit\u00e0 della vaschetta: quel lato si alza e l\u2019acqua l\u00ec \u00e8 bassa, come una spiaggia in pendenza. All\u2019altra estremit\u00e0 l\u2019acqua resta pi\u00f9 profonda: \u00e8 il mare aperto.",
            "Dal lato profondo dai una spinta decisa all\u2019acqua con la paletta, verso la spiaggia.",
            "Guarda l\u2019onda correre verso il lato rialzato: dove il fondale si alza rallenta, si accorcia e cresce in altezza.",
        ],
        "impara": "L'onda nasce da uno spostamento improvviso di tanta acqua (terremoto sottomarino, frana, eruzione). Dove il mare è profondo corre veloce ed è bassa; quando il fondale si alza verso riva rallenta e l'acqua si accumula in altezza. Non è l'onda del vento, che muove solo la superficie: qui si muove tutta la colonna d'acqua, e per questo ha molta più forza.",
        "pc": "Al mare, se senti un forte terremoto o vedi il mare ritirarsi all'improvviso, allontanati subito verso un punto alto. Sul sito: «Il rischio da maremoto».",
        "sicurezza": None,
    },
    {
        "tema": "Alluvioni urbane", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Il tombino ostruito",
        "domanda": "Perché una strada si allaga anche quando i tombini ci sono?",
        "materiali": "Una bacinella, un colino o una retina, una bottiglia d'acqua, foglie secche (o pezzetti di carta), un cronometro.",
        "passi": [
            "Appoggia il colino sopra un contenitore vuoto: è il tombino, il contenitore è la fognatura.",
            "Versa un litro d'acqua a velocità costante e conta i secondi che impiega a scendere tutta.",
            "Ora copri metà del colino con le foglie e ripeti versando allo stesso modo, contando di nuovo i secondi.",
            "Coprilo quasi del tutto e ripeti una terza volta. Segna i tre tempi e guarda quanta acqua resta sopra.",
        ],
        "cambia": "Solo quante foglie coprono la griglia.",
        "atteso": "Col colino libero l'acqua scende quasi subito; con la griglia mezza coperta ci mette molto di più e si forma un ristagno; quasi chiusa, l'acqua resta quasi tutta sopra.",
        "impara": "Il tombino non è un buco che ingoia tutto: ha una portata, cioè una quantità massima d'acqua che può far passare in un secondo. Le foglie di un temporale autunnale la riducono di colpo, e l'acqua che non scende si ferma in strada.",
        "limite": "Nella realtà conta anche quanto è piena la fognatura più a valle: un tombino pulito non serve a niente se il collettore è già al massimo.",
        "pc": "È il motivo per cui la pulizia delle caditoie prima della stagione delle piogge è prevenzione vera. Segnalare un tombino ostruito al Comune è un gesto utile.",
        "sicurezza": "Si lavora sopra un lavandino o all'aperto. Non avvicinarsi ai tombini veri, tanto meno quando piove.",
    },
    {
        "tema": "Acqua e terreno", "eta": "🟢 Infanzia · 🔵 Primaria",
        "titolo": "L'acqua risale da sola",
        "domanda": "L'acqua può andare verso l'alto senza che nessuno la spinga?",
        "materiali": "Due bicchieri, acqua, colorante alimentare o succo scuro, una striscia di carta assorbente, una di stoffa e una di carta plastificata.",
        "passi": [
            "Colora l'acqua e mettine un dito in un bicchiere.",
            "Appoggia nel bicchiere la striscia di carta assorbente, tenendola dritta, e guardala per due minuti.",
            "Ripeti con la stoffa e con la carta plastificata, sempre due minuti.",
            "Confronta fin dove è salita l'acqua nei tre materiali e segna il livello con una matita.",
        ],
        "cambia": "Solo il materiale della striscia.",
        "atteso": "Nella carta assorbente l'acqua sale di parecchi centimetri, nella stoffa un po' meno, nella carta plastificata quasi per niente.",
        "impara": "Dentro i materiali porosi ci sono tanti canaletti sottilissimi, e l'acqua ci sale dentro da sola: si chiama capillarità. Succede anche nel terreno e nei muri.",
        "limite": "Nel muro di una casa allagata l'acqua sale più piano e molto più in alto di così, e porta con sé sali che restano anche quando è asciugato.",
        "pc": "È la ragione per cui dopo un allagamento i muri restano umidi per settimane e gli intonaci vanno rifatti: l'acqua non se ne va solo perché il pavimento è asciutto.",
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
        "impara": "La fiamma si spegne perché nel barattolo l'ossigeno scende sotto il livello che serve per bruciare: non finisce del tutto, ne resta ancora parecchio. Per bruciare il fuoco ha bisogno di tre cose insieme — il triangolo del fuoco: combustibile, comburente (ossigeno) e calore. Togline una e il fuoco si spegne.",
        "pc": "È il principio dello spegnimento: le linee tagliafuoco tolgono il combustibile, l'acqua toglie il calore. Sul sito: «Il rischio da incendi boschivi».",
        "sicurezza": "C'è una fiamma: SOLO con un adulto, mai per l'infanzia. Tieni lontani capelli, maniche e carta; non lasciare la candela incustodita.",
    },
    {
        "tema": "Incendi boschivi", "eta": "🟢 Infanzia · 🔵 Primaria",
        "titolo": "Il bosco di tessere",
        "domanda": "Perché a volte un incendio si ferma da solo e a volte no?",
        "materiali": "Una scatola di tessere del domino (o tessere di cartoncino che stiano in piedi).",
        "passi": [
            "Metti le tessere in fila, una vicinissima all'altra, e falle cadere: è un bosco fitto.",
            "Rifai la fila allargando le distanze finché la caduta si ferma da sola.",
            "Rimetti la fila fitta ma togli tre tessere in mezzo, lasciando un vuoto: prova di nuovo.",
            "Prova a disegnare su un foglio dove metteresti i vuoti per proteggere una casa messa in fondo alla fila.",
        ],
        "cambia": "La distanza fra le tessere e dove si lascia il vuoto.",
        "atteso": "La fila fitta cade tutta; oltre una certa distanza la caduta si ferma; il vuoto in mezzo la ferma sempre.",
        "impara": "Perché il fuoco avanzi serve altro materiale da bruciare a portata: se la vegetazione è continua avanza, se è interrotta si ferma. È un'analogia, non un modello del fuoco: le tessere non hanno vento, calore né pendenza.",
        "limite": "In un incendio vero il fuoco può saltare le interruzioni con le faville portate dal vento, e sale in salita molto più in fretta che in piano: per questo le fasce tagliafuoco da sole non bastano.",
        "pc": "La pulizia del sottobosco e le fasce tagliafuoco servono proprio a togliere continuità al combustibile. È la parte «prevenzione» della campagna antincendio.",
        "sicurezza": None,
    },
    {
        "tema": "Ondate di calore", "eta": "🟢 Infanzia · 🔵 Primaria",
        "titolo": "Sole o ombra? Chiaro o scuro?",
        "materiali": "Due termometri (o uno da spostare), un foglio bianco e uno nero, un posto al sole.",
        "passi": [
            "Al sole, appoggia un termometro sotto il foglio nero e uno sotto il bianco: dopo dieci minuti confronta.",
            "Ripeti mettendo i due fogli all'ombra: la differenza quasi sparisce.",
            "Per misurare la temperatura dell'aria, invece, tieni il termometro all'ombra e ventilato: è così che la misurano le stazioni meteo.",
        ],
        "impara": "I colori scuri assorbono più luce del sole e si scaldano di più: è l'irraggiamento. Il termometro al sole misura quanto si è scaldato lui, non l'aria: per questo i termometri delle stazioni meteo stanno all'ombra, dentro una casetta ventilata.",
        "pc": "Sono le regole delle ondate di calore: stare all'ombra nelle ore calde, vestirsi leggeri e chiari, bere spesso. Sul sito: «Ondate di calore».",
        "sicurezza": None,
    },
    {
        "tema": "Ondate di calore", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Quale materiale conserva il calore?",
        "domanda": "Come si tiene fresca una casa quando fuori fa caldissimo?",
        "materiali": "Tre barattoli di vetro uguali con coperchio, acqua tiepida, un termometro, alluminio da cucina, un panno di lana o pile, un giornale.",
        "passi": [
            "Riempi i tre barattoli con la stessa quantità di acqua tiepida, misurata: la temperatura di partenza deve essere uguale per tutti.",
            "Avvolgi il primo nell'alluminio, il secondo nella lana, il terzo nel giornale. Un quarto barattolo senza niente fa da confronto, se ne hai uno.",
            "Mettili tutti nello stesso posto, lontano da sole e correnti.",
            "Misura la temperatura di ciascuno dopo 10, 20 e 30 minuti e scrivi i numeri in tabella.",
        ],
        "cambia": "Solo il materiale che avvolge il barattolo.",
        "atteso": "Tutti si raffreddano, ma a velocità diverse: quello nudo perde calore più in fretta, quelli avvolti lo trattengono più a lungo.",
        "impara": "Isolare non vuol dire «tenere caldo»: vuol dire rallentare il passaggio di calore, in tutte e due le direzioni. Lo stesso materiale che d'inverno tiene dentro il calore, d'estate lo tiene fuori.",
        "limite": "Qui misuri un barattolo fermo in una stanza. In una casa contano anche il sole che entra dalle finestre, le persone, gli elettrodomestici e il ricambio d'aria.",
        "pc": "Nelle ondate di calore si chiudono persiane e tapparelle nelle ore calde e si arieggia la notte: è lo stesso principio, applicato alle stanze.",
        "sicurezza": "Acqua tiepida, non bollente: la riscalda un adulto e la versa lui nei barattoli.",
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
            "Con una registrazione di un temporale, o guardando dalla finestra di casa, conta i secondi fra il lampo e il tuono.",
            "Dividi per 3: ottieni circa la distanza del temporale in chilometri.",
            "Ripeti: se i secondi diminuiscono, il temporale si sta avvicinando.",
        ],
        "impara": "La luce arriva subito, il suono molto più piano: contando i secondi si stima la distanza. Ma il conteggio serve a capire se il temporale si avvicina, non a decidere se si è al sicuro: se senti il tuono, il fulmine può già raggiungerti. Variante: strofina un palloncino sui capelli e avvicinalo a un dito al buio — la scintilla è elettricità statica, come un mini fulmine.",
        "pc": "Quando senti il primo tuono entra subito in un edificio o in un'auto chiusa e restaci finché non sono passati 30 minuti dall'ultimo tuono. Lontano da alberi isolati e specchi d'acqua. Sul sito: «Cosa fare con i temporali intensi».",
        "sicurezza": "Si osserva SOLO da dentro casa o da un luogo riparato, mai all'aperto durante il temporale.",
    },
    {
        "tema": "Siccità", "eta": "🟢 Infanzia · 🔵 Primaria",
        "titolo": "L'acqua che sparisce (la siccità)",
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
        "tema": "Umidità e nebbia", "eta": "🟢 Infanzia · 🔵 Primaria",
        "titolo": "Le goccioline vengono dall'aria",
        "domanda": "Da dove arriva l'acqua sul bicchiere della bibita fredda?",
        "materiali": "Due bicchieri uguali, acqua fredda con ghiaccio, acqua a temperatura ambiente, un panno asciutto.",
        "passi": [
            "Riempi un bicchiere di acqua con ghiaccio e l'altro di acqua a temperatura ambiente.",
            "Asciuga bene l'esterno di tutti e due, e falli vedere: sono asciutti.",
            "Aspetta cinque minuti senza toccarli.",
            "Guarda e tocca l'esterno dei due bicchieri: quello freddo è bagnato, l'altro no.",
        ],
        "cambia": "Solo la temperatura dell'acqua dentro il bicchiere.",
        "atteso": "Sul bicchiere freddo si formano goccioline; su quello a temperatura ambiente no.",
        "impara": "Nell'aria c'è sempre acqua che non si vede, sotto forma di vapore. Quando l'aria tocca una superficie fredda si raffredda e non riesce più a tenerla tutta: il vapore diventa goccioline. L'acqua non è passata attraverso il vetro, viene dall'aria.",
        "limite": "È lo stesso meccanismo delle nuvole e della nebbia, ma lì l'aria si raffredda salendo in quota o toccando il terreno freddo, non un bicchiere.",
        "pc": "Capire l'umidità serve a leggere le previsioni: nebbia, rugiada e brina nascono tutte da questo passaggio, e la nebbia è un rischio vero per chi guida.",
        "sicurezza": None,
    },
    {
        "tema": "Rischio chimico", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Come si sparge una \"nube\"",
        "materiali": "Un batuffolo con un po' di caffè in polvere o scorza di limone. In classe preferisci questi al profumo: ci può essere chi ha asma o allergie. Senza odori: un piccolo diffusore di bolle di sapone, e si alza la mano quando arriva una bolla.",
        "passi": [
            "Mettiti in un angolo della stanza con il batuffolo chiuso.",
            "I compagni si dispongono fermi in punti diversi della stanza.",
            "Apri il batuffolo: ognuno alza la mano appena sente l'odore.",
        ],
        "impara": "L'odore, come un gas, si diffonde nell'aria e si sposta con le correnti: raggiunge prima chi è vicino e sottovento. Ma l'olfatto non misura la pericolosità: molti gas pericolosi — il monossido di carbonio per primo — non si sentono affatto, e un odore forte non vuol dire per forza veleno. Non si annusa per capire se l'aria è sicura.",
        "pc": "In caso di nube tossica da un incidente industriale, spesso la cosa giusta NON è scappare ma chiudersi in casa (chiudere porte, finestre e aerazione) e seguire le autorità. Sul sito: «Il rischio chimico-industriale».",
        "sicurezza": "Mai prodotti chimici o spray. Chiedi prima se qualcuno ha asma o allergie: in quel caso usa la variante con le bolle di sapone.",
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
        "impara": "Il pepe scappa perché il sapone abbassa la tensione superficiale dell'acqua: è questo che vedi, non il lavaggio dei germi. Lavarsi le mani funziona per un'altra ragione: il sapone stacca lo sporco e i microbi dalla pelle mentre le strofini, e l'acqua li porta via nel risciacquo. Per vedere quella parte usa la variante col glitter: prima solo acqua, poi sapone e venti secondi di sfregamento.",
        "pc": "L'igiene è la prima difesa contro le epidemie: strofinare almeno venti secondi, dita e polsi compresi, poi risciacquare. Sul sito: «Il rischio sanitario».",
        "sicurezza": None,
    },
    {
        "tema": "Acqua sicura", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Acqua limpida significa potabile?",
        "domanda": "Se un'acqua è trasparente, vuol dire che si può bere?",
        "materiali": "Due bottiglie d'acqua del rubinetto, terra e foglioline per sporcare la prima, un cucchiaino di sale per la seconda, un imbuto, carta da filtro (o un tovagliolo di carta), due bicchieri trasparenti.",
        "passi": [
            "Prepara la prima bottiglia mescolando acqua e terra: è torbida e si vede.",
            "Prepara la seconda sciogliendo bene il sale: resta trasparente come prima.",
            "Filtra la prima con l'imbuto e la carta da filtro: guarda l'acqua che esce.",
            "Filtra allo stesso modo la seconda: non si assaggia nessuna delle due, nemmeno questa. Confronta solo l'aspetto delle due acque filtrate.",
        ],
        "cambia": "Che cosa è stato aggiunto all'acqua: una cosa che si vede o una che non si vede.",
        "atteso": "Il filtro toglie la terra e l'acqua torna limpida; l'acqua col sale era limpida prima e resta limpida dopo, perché il sale è rimasto dentro.",
        "impara": "Il filtro trattiene quello che è in sospensione, non quello che è disciolto. Un'acqua limpida può contenere sali, sostanze chimiche o microbi che non si vedono: limpidezza e sicurezza sono due cose diverse.",
        "limite": "Un filtro vero per l'acqua da bere usa più strati e spesso una disinfezione: questo è un modello, non un potabilizzatore.",
        "pc": "In emergenza l'acqua sicura è quella che le autorità dichiarano tale, o quella in bottiglia sigillata del kit. Un'ordinanza di non potabilità vale anche se dal rubinetto esce acqua trasparente.",
        "sicurezza": "L'acqua di questo esperimento NON si beve e non si assaggia, nemmeno quella filtrata: si guarda soltanto. A fine attività si butta e ci si lava le mani.",
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
        "tema": "Comunicazione", "eta": "🔵 Primaria · 🟠 Ragazzi",
        "titolo": "Il messaggio arriva corretto?",
        "domanda": "Perché alla radio si ripete quello che si è appena sentito?",
        "materiali": "Un foglio con cinque messaggi scritti (per esempio: «Via Italo Belardi 14, secondo piano, due persone»), carta e penna per chi riceve.",
        "passi": [
            "Primo giro: chi trasmette legge il messaggio una volta sola, a voce normale, e chi riceve scrive quello che ha capito. Nessuno può chiedere di ripetere.",
            "Confrontate: quante parole sono arrivate storte? Segnate il numero di errori.",
            "Secondo giro, messaggi nuovi: chi riceve ripete ad alta voce quello che ha scritto e chi trasmette conferma con «corretto» oppure corregge. Solo allora si passa al messaggio dopo.",
            "Contate di nuovo gli errori e confrontate i due numeri. Se potete, rifate il primo giro con un po' di rumore di fondo.",
        ],
        "cambia": "Solo la conferma: nel secondo giro chi riceve ripete e chi trasmette conferma.",
        "atteso": "Nel secondo giro gli errori calano molto, soprattutto su numeri e nomi propri. Col rumore di fondo la differenza diventa ancora più grande.",
        "impara": "Ripetere sembra una perdita di tempo e invece è il modo più rapido per accorgersi subito di un errore, quando costa poco correggerlo. Nei messaggi di emergenza i numeri e gli indirizzi sono la parte che si sbaglia più facilmente.",
        "limite": "Qui nessuno rischia niente se un messaggio arriva storto. In un'emergenza vera un indirizzo sbagliato manda i soccorsi dalla parte opposta.",
        "pc": "È il motivo per cui nelle comunicazioni radio si ripete e si conferma, e per cui l'operatore del 112 fa ripetere l'indirizzo. Si compita anche lettera per lettera quando serve.",
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
        "titolo": "La voce che guida",
        "materiali": "Una benda per gli occhi, qualche ostacolo morbido.",
        "passi": [
            "In una stanza illuminata e sicura crea un piccolo percorso con ostacoli morbidi.",
            "Un bambino chiude gli occhi (o si benda, se se la sente): non è il fumo, è un esercizio di ascolto.",
            "Un compagno lo guida verso l'uscita usando solo la voce, con indicazioni chiare e una alla volta. Poi si invertono i ruoli.",
        ],
        "impara": "Quanto contano l'ascolto, la calma e avere una sola voce che guida: con due persone che parlano insieme il percorso diventa subito più difficile. Provatelo.",
        "pc": "Durante un'evacuazione si segue chi guida e la segnaletica, senza correre e senza parlare tutti insieme. Se invece c'è del fumo la regola cambia: si va a carponi verso l'uscita, perché l'aria respirabile resta in basso — è un'altra cosa da questo esercizio. Sul sito: «Cosa fare in caso di blackout».",
        "sicurezza": "Usa ostacoli morbidi e libera il pavimento; un adulto sorveglia sempre il percorso.",
    },
    {
        "tema": "Sensori e allarmi", "eta": "🟠 Ragazzi",
        "titolo": "Un piccolo allarme di livello",
        "domanda": "Come fa uno strumento a sapere da solo quando è il momento di suonare?",
        "materiali": "Una bacinella, un tappo di sughero, due fili elettrici sottili, un LED, una pila da 4,5 volt con portapile, nastro adesivo, uno stecchino di legno.",
        "passi": [
            "Collega il LED alla pila lasciando il circuito interrotto: due capi liberi che accendono il LED quando si toccano.",
            "Fissa un capo a uno stecchino verticale sul bordo, all'altezza che scegli come soglia; l'altro sul tappo che galleggia.",
            "Versa acqua piano: quando il tappo arriva alla soglia i capi si toccano e il LED si accende.",
            "Sposta la soglia più in alto e più in basso; poi muovi l'acqua con la mano mentre il livello le è vicino.",
        ],
        "cambia": "L'altezza della soglia, e se l'acqua è ferma o mossa.",
        "atteso": "Il LED si accende quando il galleggiante arriva alla soglia. Con l'acqua mossa lampeggia anche se il livello medio non è cambiato: è un falso allarme.",
        "impara": "Un sensore misura, ma è la soglia decisa da qualcuno a trasformare la misura in allarme. Troppo bassa: allarmi continui, e la gente smette di dar retta. Troppo alta: l'allarme arriva tardi. Le onde spiegano perché i sistemi veri mediano le misure prima di decidere.",
        "limite": "È un prototipo didattico a pile, non un dispositivo di sicurezza: non si usa per sorvegliare niente davvero.",
        "pc": "Gli idrometri sui fiumi funzionano così, con soglie ufficiali: superata una soglia scatta una fase di allerta e si avvisano i Comuni.",
        "sicurezza": "Solo pila da 4,5 volt e LED: mai la corrente di casa vicino all'acqua. Il circuito lo controlla un adulto prima di versare l'acqua.",
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
  <!-- URL preferito: la copia su GitHub Pages rimanda alla produzione. -->
  <link rel="canonical" href="https://www.protezionecivilegenzano.it/formazione/schede-stampabili/esperimenti-protezione-civile/">
  <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
  <link rel="stylesheet" href="/formazione/schede-stampabili/assets/scheda-print.css">
  <style>
    /* Un solo h1 nel fascicolo (WCAG 1.3.1, audit 25/09/2026 F11): i titoli
       degli esperimenti sono h2, le loro sezioni h3 con la stessa classe e lo
       stesso aspetto di prima. L'h1 sta nell'introduzione a schermo. */
    .esp-intro .esp-h1 {{ font-size: 1.15rem; color: var(--scheda-blu); margin: 0 0 0.35rem; }}
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
    .esp-domanda {{
      background: #eaf2fb;
      border-left: 3px solid #003366;
      font-style: italic;
    }}
    .esp-limite {{
      background: #fffaf0;
      border-left: 3px solid #b45309;
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
      /* Le schede con domanda, variabile, risultato atteso e limite del modello
         hanno quattro blocchi in più e da sole sforerebbero il foglio: la
         promessa del fascicolo è un esperimento per foglio, quindi si stringono
         qui invece di spezzarsi su due pagine. Solo in stampa: a schermo il
         testo resta alla dimensione piena. */
      .scheda-page.esp-compatta {{ font-size: 0.9rem; }}
      .esp-compatta .esp-block, .esp-compatta .esp-pc, .esp-compatta .esp-sicurezza {{
        margin: 0.3rem 0; line-height: 1.35;
      }}
      .esp-compatta .esp-pc, .esp-compatta .esp-sicurezza, .esp-compatta .esp-domanda, .esp-compatta .esp-limite {{
        padding: 0.35rem 0.6rem;
      }}
      .esp-compatta .esp-passi li {{ margin-bottom: 0.15rem; line-height: 1.3; }}
      .esp-compatta .scheda-h2 {{ margin: 0.5rem 0 0.2rem; }}
      /* Il riquadro «Cosa ho osservato» a 4,5rem mangiava il foglio: sei schede
         su 33 finivano su due pagine, fra cui una vecchia. In stampa basta una
         riga per annotare, e la promessa «un esperimento per foglio» regge. */
      /* La compattazione tipografica vale per TUTTE le schede, non solo per le
         più lunghe: serve a lasciare su ogni foglio lo spazio per l'illustrazione
         del montaggio. Prima era legata alla presenza del blocco «La domanda» e
         le schede più vecchie restavano a corpo pieno, senza spazio per il disegno. */
      .scheda-page .scheda-box-disegno {{ min-height: 2rem !important; }}
      /* Altezza definita = il flex sa quanto spazio ha da distribuire alla figura. */
      /* L'area stampabile non è il foglio intero: `@page` di scheda-print.css
         tiene 5mm di margine per lato, quindi restano 28,7cm. Dare alla scheda
         un'altezza maggiore produce un foglio bianco dopo ciascuna (66 pagine
         invece di 33): misurato, non supposto. 28,4cm lascia un filo di gioco. */
      .scheda-page {{ height: 28.4cm; margin: 0 auto; box-shadow: none; }}
      /* Secondo livello, per gli esperimenti con più testo: senza questo il
         disegno su quelle schede scendeva a ~14mm, una dimensione in cui non si
         legge più che cosa mostra. Il livello lo decide la lunghezza del testo,
         non una lista di titoli scritta a mano: un esperimento nuovo e lungo lo
         riceve da solo. */
      .scheda-page.esp-fitta {{ font-size: 0.84rem; }}
      .esp-fitta .esp-passi li {{ margin-bottom: 0.1rem; line-height: 1.25; }}
      .esp-fitta .esp-block, .esp-fitta .esp-pc, .esp-fitta .esp-sicurezza {{
        margin: 0.3rem 0; line-height: 1.35;
      }}
      .esp-fitta .scheda-h2 {{ margin: 0.4rem 0 0.15rem; }}
      .esp-fitta .scheda-box-disegno {{ min-height: 1.5rem !important; }}
      /* Schede dense: disegno e spazio per annotare dividono la stessa riga. */
      .esp-osserva {{ display: flex; gap: 0.6rem; align-items: stretch; flex: 1 1 0; min-height: 0; }}
      .esp-osserva .esp-figura {{ flex: 0 0 auto; margin: 0; max-height: none; align-self: stretch; }}
      .esp-osserva .scheda-box-disegno {{ flex: 1 1 auto; min-height: 1.5rem !important; }}
    }}
    /* La figura si prende lo spazio che AVANZA sul foglio, non una misura fissa.
       La scheda è un contenitore flex in colonna: dandole un'altezza definita in
       stampa e alla figura `flex: 1`, il disegno cresce dove la scheda è vuota e
       si stringe dove è piena. Così la promessa «un esperimento per foglio» regge
       da sola, anche quando un domani si aggiunge un esperimento lungo: nessuna
       taratura per scheda da rifare a mano.
       Il primo tentativo era una figura flottata a destra: su un contenitore flex
       il float è ignorato, la figura si prendeva una riga intera (+180 px) e
       dodici schede su 33 finivano su due pagine. */
    .esp-figura {{
      flex: 1 1 0;
      min-height: 52px;
      max-height: 250px;
      align-self: center;
      display: flex;
      justify-content: center;
      width: auto;
      max-width: 100%;
      margin: 0.35rem 0 0.45rem;
      padding: 0.3rem 0.5rem;
      border: 1px solid #cfd8e3;
      border-radius: 5px;
      background: #fff;
      break-inside: avoid;
    }}
    /* height:100% + width:auto = il disegno mantiene le proporzioni e riempie
       in altezza; `preserveAspectRatio` di default lo centra senza deformarlo. */
    .esp-figura svg {{ height: 100%; width: auto; max-width: 100%; display: block; }}
    /* A schermo lo spazio non è contingentato come sul foglio, quindi il minimo
       può essere generoso. Deve stare in un blocco `screen` esplicito: messo nel
       blocco generale si applicherebbe anche in stampa e, avendo la stessa
       specificità della regola dentro `@media print` ma venendo dopo, vincerebbe
       lei — il minimo di stampa resterebbe 140px e la figura non potrebbe più
       stringersi per stare nel foglio. */
    @media screen {{
      .esp-figura {{ min-height: 140px; }}
    }}
    .esp-osserva {{ display: flex; gap: 0.6rem; align-items: stretch; }}
    .esp-osserva .scheda-box-disegno {{ flex: 1 1 auto; }}
    @media screen and (max-width: 620px) {{ .esp-osserva {{ display: block; }} }}

    @media screen and (max-width: 620px) {{
      .esp-figura {{ float: none; width: 100%; margin: 0.4rem 0 0.6rem; }}
      .esp-compatta .esp-figura {{ width: 100%; }}
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
    <h1 class="esp-h1">Esperimenti di protezione civile: {n} schede A4</h1>
    <strong>Un esperimento per foglio.</strong> Puoi stampare tutto il fascicolo oppure, dalla finestra di stampa, scegliere <strong>solo le pagine</strong> che ti servono. Ogni scheda indica età consigliata, materiali, procedura, cosa si impara e le note di sicurezza. Versione completa e interattiva: <a href="/formazione/esperimenti/">Esperimenti e attività di protezione civile</a>.
  </div>
"""

def _densita(e):
    """Caratteri di testo della scheda: proxy di quanto riempie il foglio.

    Serve a scegliere il livello di compattazione senza tenere una lista di
    titoli: un esperimento aggiunto domani riceve il livello giusto da solo.
    La soglia è tarata sulla resa reale misurata in stampa, non a occhio.
    """
    campi = ("domanda", "materiali", "cambia", "atteso", "impara", "limite", "pc", "sicurezza")
    return sum(len(str(e.get(c) or "")) for c in campi) + sum(len(p) for p in e["passi"])


SOGLIA_DENSA = 1300  # caratteri: sopra questa soglia la scheda è piena (tarato in stampa)


def _densa(e):
    """Scheda troppo piena per reggere l'illustrazione sopra il testo.

    Su queste il disegno scende accanto al riquadro «Cosa ho osservato»,
    riprendendosi lo spazio che quel riquadro occupa comunque: sopra il testo
    sarebbe finito a 18mm, una misura in cui non si capisce più che cosa mostra.
    """
    return _densita(e) > SOGLIA_DENSA


PAGE = """
  <article class="scheda-page{estesa}">
    <header class="scheda-header">
      <div class="scheda-logo" aria-hidden="true">PC</div>
      <div class="scheda-intestazione">
        <div class="scheda-ente">Protezione Civile &mdash; Genzano di Roma</div>
        <h2 class="scheda-titolo-principale">{titolo}</h2>
        <div class="scheda-sottotitolo">Esperimento di protezione civile &mdash; {tema}</div>
      </div>
    </header>

    <div class="scheda-meta">
      <span><strong>Et&agrave; consigliata:</strong> {eta}</span>
      <span><strong>Tema:</strong> {tema}</span>
    </div>

{domanda}{figura_alto}    <div class="esp-block"><span class="et">Materiali.</span> {materiali}</div>

    <h3 class="scheda-h2">Come si fa</h3>
    <ol class="esp-passi">
{passi}
    </ol>
{cambia}{atteso}
    <div class="esp-block"><span class="et">Cosa si impara.</span> {impara}</div>
{limite}
    <div class="esp-pc"><strong>In chiave protezione civile.</strong> {pc}</div>
{sicurezza}
    <h3 class="scheda-h2">&#9999;&#65039; Cosa ho osservato</h3>
    <div class="esp-osserva">{figura_basso}<div class="scheda-box-disegno" style="min-height: 4.5rem;"></div></div>

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
        # Campi introdotti il 14/09/2026 su rilievo dell'audit esterno: un
        # esperimento senza domanda di partenza, senza la variabile da cambiare
        # e senza il punto in cui il modello smette di somigliare alla realtà
        # insegna anche le cose sbagliate. Sono opzionali: le schede più vecchie
        # non li hanno ancora e restano valide.
        def blocco(campo, etichetta, classe="esp-block"):
            if not e.get(campo):
                return ""
            return '    <div class="{}"><span class="et">{}</span> {}</div>\n'.format(
                classe, etichetta, escape(e[campo]))

        domanda = blocco("domanda", "La domanda.", "esp-domanda")
        cambia = blocco("cambia", "Cosa si cambia.")
        atteso = blocco("atteso", "Che cosa aspettarsi.")
        limite = blocco("limite", "Dove il modello si ferma.", "esp-limite")
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
                domanda=domanda, cambia=cambia, atteso=atteso, limite=limite,
                estesa=" esp-compatta" + (" esp-fitta" if _densa(e) else ""),
                figura_alto="" if _densa(e) else figura(e["titolo"]),
                figura_basso=figura(e["titolo"]) if _densa(e) else "",
                impara=escape(e["impara"]),
                pc=escape(e["pc"]),
                sicurezza=sicurezza,
            )
        )
    parts.append(FOOT)
    return "".join(parts)


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    # Un esperimento senza disegno non deve passare in silenzio: il fascicolo
    # sarebbe l'unico foglio nudo fra 33 illustrati e nessuno se ne accorgerebbe.
    senza = mancanti([e["titolo"] for e in ESPERIMENTI])
    if senza:
        raise SystemExit(
            "Esperimenti senza illustrazione in illustrazioni_esperimenti.py:\n  - "
            + "\n  - ".join(senza)
            + "\nAggiungi la scena e la voce nel registro SCENE.")

    OUT.write_text(render(), encoding="utf-8")
    print(f"Scritto {OUT} ({len(ESPERIMENTI)} schede)")


if __name__ == "__main__":
    main()
