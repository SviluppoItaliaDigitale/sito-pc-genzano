/* Genzano si prepara — scenario «Fumo sulla collina».
 * Le indicazioni ripetono le pagine canoniche del sito:
 *   /rischi-prevenzione/rischio-incendio/ (prima, durante, dopo, cosa non fare)
 *   /allerte-meteo/ (bollettino di pericolosità incendi, Genzano è in Zona AIB 9)
 *   /rischi-prevenzione/persone-necessita-specifiche/
 * Se una di quelle pagine cambia un'indicazione, si aggiorna anche qui.
 * Lo scenario è inventato; i luoghi sono quelli veri di Genzano.
 */
(function (g) {
  'use strict';

  var LINK = '/rischi-prevenzione/rischio-incendio/';

  var S = {
    id: 'incendio',
    ordine: 3,
    icona: 'bi-fire',
    titolo: 'Fumo sulla collina',
    rischio: 'Incendio boschivo',
    durata: 'Circa 10 minuti',
    casa: 'margine',
    intro: [
      'Abiti con tuo figlio Flavio e la nonna Lina in una casa con giardino, al margine del bosco a ovest del paese.',
      'È luglio: non piove da settimane e soffia un vento caldo. Da giugno a settembre una piccola fiamma può diventare un grande incendio.',
      'Il bollettino della Regione Lazio dà per oggi una pericolosità elevata sulla Zona 9, quella dei Castelli Romani e di Genzano.'
    ],
    allerta: {
      testo: 'Pericolosità incendi boschivi elevata — Zona AIB 9',
      fonte: 'Centro Funzionale della Regione Lazio',
      colore: 'rosso',
      icona: 'bi-fire'
    },
    transizione: {
      titolo: 'L\'incendio è spento',
      testo: 'Dopo ore di lavoro le squadre di soccorso hanno spento l\'incendio. Adesso comincia il dopo: anche qui le scelte contano.',
      bottone: 'Vai al giorno dopo'
    },
    ricorda: [
      'Durante la stagione degli incendi controlla il bollettino di pericolosità su [Allerte meteo](/allerte-meteo/).',
      'Se vedi un incendio chiama subito il 112, con indicazioni precise: [rischio incendio](/rischi-prevenzione/rischio-incendio/).'
    ],

    prima: {
      ora: 'Sabato, ore 10:00',
      luogo: 'margine',
      meteo: 'caldo',
      testo: 'Stamattina hai tempo per quattro cose. Quali scegli?',
      avanti: 'È pomeriggio: andiamo avanti',
      posti: 4,
      azioni: [
        { id: 'sterpaglie', luogo: 'margine', peso: 3,
          testo: 'Taglio l\'erba secca e tolgo le sterpaglie intorno a casa e nel terreno di proprietà.',
          perche: 'Togliere la vegetazione secca intorno alla casa crea uno spazio difendibile; tenere puliti i terreni è anche un obbligo di legge.',
          link: LINK + '#cosa-fare-prima' },
        { id: 'vie', luogo: 'margine', peso: 3,
          testo: 'Decido con la famiglia due strade per allontanarci, in direzioni diverse.',
          perche: 'Il fuoco può cambiare direzione: serve sapere prima anche una via di fuga alternativa.',
          link: LINK + '#cosa-fare-durante' },
        { id: 'istruzioni', luogo: 'margine', peso: 2,
          testo: 'Ripasso con Flavio che cosa dire al 112 se vediamo un incendio: Comune, località, un riferimento visibile, direzione del fumo.',
          perche: 'Indicazioni precise aiutano i soccorsi a trovare subito il punto giusto.',
          link: LINK + '#cosa-fare-durante' },
        { id: 'kit', luogo: 'margine', peso: 2,
          testo: 'Preparo il kit «Vai» per allontanarci in fretta, vicino alla porta.',
          perche: 'Se bisogna andare via subito non c\'è tempo per cercare documenti, farmaci e torcia.',
          link: '/rischi-prevenzione/kit-emergenza/#kit-vai' },
        { id: 'vicino', luogo: 'margine', peso: 2,
          testo: 'Passo dal signor Pasquale, il vicino che vive solo: gli lascio il mio numero e gli dico che oggi il pericolo è elevato.',
          perche: 'La rete di vicinato è la prima risorsa in emergenza, soprattutto per chi vive solo.',
          link: '/rischi-prevenzione/persone-necessita-specifiche/' },
        { id: 'bollettino', luogo: 'margine', peso: 1,
          testo: 'Leggo i consigli sulla pagina Allerte meteo e li racconto a casa.',
          perche: 'Sapere che il pericolo è elevato fa stare tutti più attenti a fuochi, mozziconi e fumo.',
          link: '/allerte-meteo/' },
        { id: 'brucio', luogo: 'margine', peso: 0,
          testo: 'Brucio in giardino il mucchio di foglie secche.',
          perche: 'Per bruciare sterpaglie o residui vegetali si contatta il Comune: ci sono norme locali e spesso serve un\'autorizzazione. Con il pericolo elevato un fuoco all\'aperto può sfuggire di mano.',
          link: LINK + '#cosa-fare-prima' },
        { id: 'barbecue', luogo: 'bosco', peso: 0,
          testo: 'Organizzo un barbecue nel bosco per domani.',
          perche: 'Nel periodo di massimo rischio non si accendono fuochi nelle aree boschive o vicino, nemmeno fuori dalle aree attrezzate.',
          link: LINK + '#cosa-fare-prima' }
      ]
    },

    eventi: [
      { id: 'mozzicone', fase: 'prima', ora: 'Sabato, ore 14:00', luogo: 'bosco', meteo: 'caldo',
        titolo: 'La sigaretta dal finestrino',
        testo: function () {
          return 'Sei in auto con un amico sulla strada che costeggia il bosco. Lui finisce la sigaretta e sta per gettarla dal finestrino.';
        },
        scelte: [
          { testo: 'Gli dico di spegnerla bene nel posacenere dell\'auto.', punti: 3,
            perche: 'Giusto. Mozziconi e fiammiferi accesi non si gettano mai, soprattutto dall\'auto: basta l\'erba secca a bordo strada.' },
          { testo: 'Lascio stare: è solo un mozzicone.', punti: 0,
            perche: 'Con la vegetazione secca e il vento, un mozzicone acceso può far partire un incendio.' },
          { testo: 'Gli dico di gettarla dove c\'è l\'asfalto.', punti: 0,
            perche: 'Un mozzicone acceso non si getta mai, nemmeno sull\'asfalto: basta poco per far partire un incendio.' }
        ],
        link: LINK + '#cosa-fare-prima' },

      { id: 'fumo', fase: 'durante', ora: 'Sabato, ore 15:30', luogo: 'bosco', meteo: 'fumo',
        titolo: 'Una colonna di fumo',
        testo: function (p) {
          return 'Dal giardino vedi una colonna di fumo che sale dal bosco, a ovest del paese.' +
            (p.istruzioni ? ' Sai già che cosa dire al 112.' : '');
        },
        scelte: function (p) {
          return [
            p.istruzioni
              ? { testo: 'Chiamo subito il 112 e dico Comune, località, un riferimento visibile e la direzione del fumo.', punti: 3,
                  perche: 'Giusto. Nel Lazio il 112 è l\'unico numero di emergenza e attiva vigili del fuoco, forestali ed eventuale soccorso sanitario.' }
              : { testo: 'Chiamo subito il 112 e cerco di spiegare dov\'è il fumo.', punti: 2,
                  perche: 'Giusto chiamare subito il 112. Sapere prima che cosa dire (Comune, località, un riferimento visibile, direzione del fumo) aiuta i soccorsi a trovare subito il punto.' },
            { testo: 'Scrivo sui social che c\'è fumo e aspetto che chiami qualcun altro.', punti: 0,
              perche: 'Se vedi un incendio chiama immediatamente il 112: non si dà per scontato che lo abbia già fatto qualcuno.' },
            { testo: 'Vado con un secchio a spegnerlo finché è piccolo.', punti: 0,
              perche: 'Non ci si avvicina alle fiamme e non si prova a spegnere un incendio da soli con mezzi di fortuna.' }
          ];
        },
        link: LINK + '#cosa-fare-durante' },

      { id: 'stradafumo', fase: 'durante', ora: 'Sabato, ore 15:50', luogo: 'bosco', meteo: 'fumo',
        titolo: 'Il fumo sulla strada',
        testo: function () {
          return 'Stai tornando a casa a piedi con Flavio dal negozio. Il fumo ha invaso la strada che porta a casa e non si vede più in fondo.';
        },
        scelte: [
          { testo: 'Lo attraversiamo di corsa: casa è lì dietro.', punti: 0,
            perche: 'Nelle strade invase dal fumo la visibilità può annullarsi, e il fumo non va sottovalutato: respirarlo è pericoloso.' },
          { testo: 'Torniamo indietro e facciamo un\'altra strada, lontano dal fumo.', punti: 3,
            perche: 'Giusto. Non si attraversano e non si percorrono le strade invase dal fumo.' },
          { testo: 'Ci fermiamo a guardare e a fare un video.', punti: 0,
            perche: 'Non si sosta nelle strade percorse dal fumo: è pericoloso e intralcia i soccorsi.' }
        ],
        link: LINK + '#cosa-fare-durante' },

      { id: 'casa', fase: 'durante', ora: 'Sabato, ore 16:30', luogo: 'margine', meteo: 'fumo',
        titolo: 'Il fuoco si avvicina',
        testo: function (p) {
          var t = 'Siete a casa. Il fuoco scende verso le case al margine del bosco; il fumo arriva da ovest, la strada verso est è libera.';
          t += p.sterpaglie
            ? ' Intorno alla casa l\'erba è tagliata: al fuoco resta meno da bruciare vicino al muro.'
            : ' L\'erba secca del giardino arriva fino al muro di casa.';
          if (p.vie) t += ' Sapete già quale strada prendere.';
          return t;
        },
        scelte: function (p) {
          return [
            p.vie
              ? { testo: 'Ci allontaniamo subito verso est, lontano dal fumo e dal fuoco, con la nonna.', punti: 3,
                  perche: 'Giusto. Se puoi allontanarti in sicurezza, fallo subito, in direzione opposta a quella del fumo e del fuoco.' }
              : { testo: 'Ci allontaniamo verso est, lontano dal fumo, e cerchiamo la strada mentre andiamo.', punti: 2,
                  perche: 'Giusto allontanarsi subito, lontano dal fumo e dal fuoco. Con una strada già decisa, e una di riserva, sareste partiti senza esitare.' },
            { testo: 'Saliamo sulla collina dietro casa per vedere meglio.', punti: 0,
              perche: 'Non si fugge in salita davanti a un fronte di fuoco: le fiamme salgono più velocemente di quanto tu possa correre.' },
            { testo: 'Bagno con il tubo le fiamme spinte dal vento.', punti: 0,
              perche: 'Non si getta acqua su fiamme alimentate dal vento: il fuoco può cambiare direzione all\'improvviso.' }
          ];
        },
        link: LINK + '#cosa-fare-durante' },

      { id: 'pasquale', fase: 'durante', ora: 'Sabato, ore 16:40', luogo: 'margine', meteo: 'fumo',
        solo: function (p) { return !p.vicino; },
        titolo: 'Il vicino che vive solo',
        testo: function () {
          return 'Mentre vi allontanate ti accorgi che il signor Pasquale, il vicino che vive solo, non è uscito di casa.';
        },
        scelte: [
          { testo: 'Lo dico subito al 112 e ai soccorritori che incontro, indicando la sua casa.', punti: 3,
            perche: 'Giusto. Si chiama il 112 se una persona può essere in pericolo, e si seguono le indicazioni delle squadre di soccorso.' },
          { testo: 'Torno indietro da solo verso il fumo per andarlo a prendere.', punti: 0,
            perche: 'Si aiuta chi è in difficoltà solo se lo si può fare senza esporsi a pericoli: andare verso il fumo e il fuoco non lo è.' },
          { testo: 'Penso che se ne sia già andato.', punti: 0,
            perche: 'Chi vive solo può non accorgersi del pericolo o non riuscire ad andare via: se può essere in pericolo, va segnalato subito al 112.' }
        ],
        link: '/rischi-prevenzione/persone-necessita-specifiche/' },

      { id: 'bruciato', fase: 'dopo', ora: 'Domenica, ore 10:00', luogo: 'bosco', meteo: 'sereno',
        titolo: 'Il bosco bruciato',
        testo: function () {
          return 'Il giorno dopo il fumo non c\'è più. Flavio vorrebbe andare a vedere il bosco bruciato.';
        },
        scelte: [
          { testo: 'Andiamo a vedere da vicino: ormai è spento.', punti: 0,
            perche: 'Nella zona percorsa dal fuoco possono esserci tronchi instabili e braci ancora attive sotto la cenere.' },
          { testo: 'Non entriamo nella zona bruciata; se vediamo il fuoco riprendere chiamiamo il 112.', punti: 3,
            perche: 'Giusto. Nella zona percorsa dal fuoco non si entra, e le riprese di fuoco si segnalano al 112.' },
          { testo: 'Portiamo dei secchi d\'acqua per spegnere le braci rimaste.', punti: 0,
            perche: 'Non si bonifica da soli l\'area incendiata: lo fanno le squadre antincendio.' }
        ],
        link: LINK + '#cosa-fare-dopo' },

      { id: 'rientro', fase: 'dopo', ora: 'Domenica, ore 11:00', luogo: 'margine', meteo: 'sereno',
        titolo: 'Tornare a casa',
        testo: function (p) {
          return p.sterpaglie
            ? 'La casa non è stata toccata dal fuoco: intorno l\'erba era tagliata. Una casa vicina ha il tetto annerito.'
            : 'Il fuoco è arrivato fino al vostro giardino e ha annerito una parete di casa.';
        },
        scelte: [
          { testo: 'Rientriamo solo quando le squadre di soccorso lo dicono, e facciamo verificare la casa se il fuoco l\'ha toccata.', punti: 3,
            perche: 'Giusto. Si seguono le indicazioni delle squadre di soccorso e, se l\'abitazione è stata interessata dal fuoco, si fa verificare la stabilità della struttura prima di rientrare.' },
          { testo: 'Rientriamo subito: la casa sembra a posto.', punti: 0,
            perche: 'Prima si aspettano le indicazioni delle squadre di soccorso; e se il fuoco ha toccato la casa, ne va fatta verificare la struttura, perché i danni possono non vedersi.' },
          { testo: 'Entro a prendere qualcosa e poi esco.', punti: 0,
            perche: 'Si rientra quando le squadre di soccorso dicono che si può: la zona può essere ancora pericolosa.' }
        ],
        link: LINK + '#cosa-fare-dopo' }
    ],

    resoconto: [
      { se: 'sterpaglie',
        si: 'L\'erba intorno alla casa era tagliata: al fuoco restava meno da bruciare e la casa non è stata toccata.',
        no: 'L\'erba secca arrivava fino alla casa: il fuoco ha annerito una parete.' },
      { se: 'vie',
        si: 'Sapevate già quale strada prendere e siete partiti subito.',
        no: 'Avete perso minuti preziosi a decidere quale strada prendere.' },
      { se: 'istruzioni',
        si: 'Al 112 hai dato subito indicazioni precise.',
        no: 'Al 112 hai faticato a spiegare dov\'era il fumo.' },
      { se: 'kit',
        si: 'Il kit «Vai» era pronto vicino alla porta.',
        no: 'Siete usciti senza documenti, farmaci e torcia.' },
      { se: 'vicino',
        si: 'Il signor Pasquale aveva il tuo numero e vi ha chiamati subito: è venuto via con voi.',
        no: 'Il signor Pasquale non aveva ancora lasciato casa: l\'avete scoperto solo mentre vi allontanavate.' },
      { se: 'bollettino',
        si: 'In casa tutti sapevano che il pericolo era elevato.',
        no: 'In casa nessuno sapeva che il pericolo era elevato.' }
    ]
  };

  g.GenzanoScenari = g.GenzanoScenari || {};
  g.GenzanoScenari[S.id] = S;
})(window);
