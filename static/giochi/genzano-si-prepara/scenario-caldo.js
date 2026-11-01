/* Genzano si prepara — scenario «Luglio rovente».
 * Le indicazioni ripetono le pagine canoniche del sito:
 *   /rischi-prevenzione/ondate-di-calore/ (prima, durante, dopo, cosa non fare, categorie a rischio)
 *   /rischi-prevenzione/persone-necessita-specifiche/
 * Ore più calde: dalle 11 alle 18 (data/dati_canonici.yaml, «caldo-ore-piu-calde»).
 * Se una di quelle pagine cambia un'indicazione, si aggiorna anche qui.
 * Lo scenario è inventato; i luoghi sono quelli veri di Genzano.
 */
(function (g) {
  'use strict';

  var LINK = '/rischi-prevenzione/ondate-di-calore/';

  var S = {
    id: 'caldo',
    ordine: 4,
    icona: 'bi-thermometer-sun',
    titolo: 'Luglio rovente',
    rischio: 'Ondata di calore',
    durata: 'Circa 8 minuti',
    intro: [
      'Abiti a Genzano con tuo figlio Flavio e la nonna Lina, che ha più di 80 anni e prende alcuni farmaci ogni giorno.',
      'È luglio. Genzano non ha un bollettino sulle ondate di calore tutto suo: il più vicino è quello di Roma, del Ministero della Salute.',
      'Il bollettino di Roma segna livello 3 da domani: un\'ondata di calore pericolosa per tutti, non solo per anziani e persone fragili.'
    ],
    allerta: {
      testo: 'Ondate di calore: livello 3 a Roma, la città più vicina con il bollettino',
      fonte: 'Ministero della Salute',
      colore: 'rosso',
      icona: 'bi-thermometer-sun'
    },
    transizione: {
      titolo: 'L\'ondata di calore è finita',
      testo: 'Dopo cinque giorni le temperature scendono di qualche grado. Anche nel dopo le scelte contano.',
      bottone: 'Vai a sabato'
    },
    ricorda: [
      'In estate consulta ogni giorno il bollettino sulle ondate di calore del Ministero della Salute, anche con l\'app Caldo e Salute: [ondate di calore](/rischi-prevenzione/ondate-di-calore/).',
      'Quando fa molto caldo, senti ogni giorno i vicini anziani e le persone sole: [persone con necessità specifiche](/rischi-prevenzione/persone-necessita-specifiche/).'
    ],

    prima: {
      ora: 'Domenica, ore 19:00',
      luogo: 'casa',
      meteo: 'caldo',
      testo: 'Stasera hai tempo per quattro cose. Quali scegli?',
      avanti: 'È lunedì: andiamo avanti',
      posti: 4,
      azioni: [
        { id: 'vicino', luogo: 'casa', peso: 3,
          testo: 'Passo dal signor Pasquale, che vive solo, e ci accordiamo per sentirci ogni giorno.',
          perche: 'Gli anziani soli sono tra i più a rischio: con il caldo si contattano i vicini anziani e le persone sole.',
          link: LINK + '#categorie-rischio' },
        { id: 'farmaci', luogo: 'casa', peso: 2,
          testo: 'Sposto i farmaci della nonna in un posto fresco, lontano dal sole.',
          perche: 'I farmaci non si lasciano esposti al calore: possono perdere efficacia.',
          link: LINK },
        { id: 'ventilatore', luogo: 'casa', peso: 2,
          testo: 'Controllo che il ventilatore e il condizionatore funzionino.',
          perche: 'Scoprirlo prima evita di restare senza fresco proprio nei giorni peggiori.',
          link: LINK + '#cosa-fare-prima' },
        { id: 'acqua', luogo: 'casa', peso: 2,
          testo: 'Faccio una scorta d\'acqua in casa.',
          perche: 'Con il caldo si beve molta acqua: la scorta evita di uscire nelle ore più calde per comprarla.',
          link: LINK + '#cosa-fare-prima' },
        { id: 'app', luogo: 'casa', peso: 2,
          testo: 'Installo l\'app Caldo e Salute per leggere ogni giorno il bollettino.',
          perche: 'Il bollettino cambia di giorno in giorno: consultarlo ogni giorno aiuta a organizzarsi.',
          link: '/comunicazioni/2026-06-07-caldo-salute-app-bollettini/' },
        { id: 'programma', luogo: 'piazza', peso: 2,
          testo: 'Organizzo la settimana: spesa e commissioni la mattina presto, fuori dalle ore più calde.',
          perche: 'Con l\'ondata di calore non si esce nelle ore più calde, dalle 11 alle 18.',
          link: LINK + '#cosa-fare-durante' },
        { id: 'bibite', luogo: 'casa', peso: 0,
          testo: 'Compro una scorta di bibite gassate e zuccherate.',
          perche: 'Contro il caldo si beve acqua; si evitano alcolici e bevande zuccherate.',
          link: LINK + '#cosa-fare-durante' },
        { id: 'gelate', luogo: 'casa', peso: 0,
          testo: 'Preparo tanto ghiaccio per bere bevande gelate dopo pranzo.',
          perche: 'Le bevande gelate in grandi quantità a stomaco pieno possono causare malesseri: meglio acqua fresca, non ghiacciata, a piccoli sorsi.',
          link: LINK }
      ]
    },

    eventi: [
      { id: 'uscita', fase: 'durante', ora: 'Lunedì, ore 13:00', luogo: 'piazza', meteo: 'caldo',
        titolo: 'Una commissione in piazza',
        testo: function (p) {
          return (p.app ? 'L\'app ti ricorda che oggi a Roma c\'è il livello 3. ' : '') +
            'Devi passare in piazza Tommaso Frasconi per una commissione. Fuori ci sono 37 gradi.' +
            (p.programma ? ' Avevi già organizzato la settimana per uscire la mattina presto.' : '');
        },
        scelte: [
          { testo: 'Ci vado adesso a piedi, tanto è vicino.', punti: 0,
            perche: 'Durante un\'ondata di calore non si esce nelle ore più calde, dalle 11 alle 18.' },
          { testo: 'Ci vado domattina presto, o stasera dopo le 18, e intanto resto al fresco.', punti: 3,
            perche: 'Giusto. Si esce fuori dalle ore più calde, con abiti leggeri e chiari, cappello e occhiali da sole.' },
          { testo: 'Ci vado adesso, ma di corsa, per stare fuori meno tempo.', punti: 0,
            perche: 'Gli sforzi fisici intensi nelle ore più calde sono proprio da evitare.' }
        ],
        link: LINK + '#cosa-fare-durante' },

      { id: 'auto', fase: 'durante', ora: 'Lunedì, ore 18:30', luogo: 'parcheggio', meteo: 'caldo',
        titolo: 'Flavio si è addormentato',
        testo: function () {
          return 'Hai fatto la spesa dopo le 18. Al parcheggio Flavio si è addormentato in auto. Devi entrare solo un attimo in farmacia.';
        },
        scelte: [
          { testo: 'Lo lascio dormire, con il finestrino un po\' aperto: è solo un minuto.', punti: 0,
            perche: 'Non si lasciano mai persone o animali in un\'auto parcheggiata al sole, neanche per poco: l\'auto chiusa si scalda in fretta.' },
          { testo: 'Lo sveglio e lo porto con me.', punti: 3,
            perche: 'Giusto. Mai persone o animali da soli in un\'auto parcheggiata al sole.' },
          { testo: 'Lo lascio con il motore acceso e l\'aria condizionata.', punti: 0,
            perche: 'Un bambino non si lascia mai da solo in auto: se il motore si spegne, l\'auto chiusa si scalda in fretta.' }
        ],
        link: LINK + '#cosa-fare-durante' },

      { id: 'casa', fase: 'durante', ora: 'Martedì, ore 14:00', luogo: 'casa', meteo: 'caldo',
        titolo: 'In casa si soffoca',
        testo: function (p) {
          return 'Il sole batte sulle finestre del soggiorno e in casa fa molto caldo.' +
            (p.ventilatore ? ' Il ventilatore funziona: l\'hai controllato domenica.' : ' Il ventilatore non parte: non l\'avevi controllato.');
        },
        scelte: [
          { testo: 'Abbasso le tapparelle nelle ore di sole e preparo per pranzo frutta e verdura.', punti: 3,
            perche: 'Giusto. Nelle ore di sole diretto si abbassano le tapparelle e si rinfrescano gli ambienti; i pasti sono leggeri, con frutta e verdura.' },
          { testo: 'Apro tutte le finestre per fare corrente, anche dove batte il sole.', punti: 1,
            perche: 'Nelle ore di sole diretto conviene abbassare le tapparelle, per non far entrare il caldo. Le finestre si aprono quando fuori fa più fresco.' },
          { testo: 'Preparo un pranzo abbondante, con fritti e dolci.', punti: 0,
            perche: 'Con il caldo si fanno pasti leggeri, privilegiando frutta e verdura.' }
        ],
        link: LINK + '#cosa-fare-durante' },

      { id: 'nonna', fase: 'durante', ora: 'Martedì, ore 16:00', luogo: 'casa', meteo: 'caldo',
        titolo: 'La nonna non ha sete',
        testo: function (p) {
          return 'La nonna Lina dice che non ha sete e da stamattina non ha bevuto quasi niente.' +
            (p.acqua ? '' : ' In casa è rimasta poca acqua.') +
            (p.farmaci ? '' : ' Le sue medicine sono sulla mensola accanto alla finestra, al sole.');
        },
        scelte: function (p) {
          return [
            p.acqua
              ? { testo: 'Le porto acqua fresca, non ghiacciata, e la invito a bere a piccoli sorsi e spesso, anche senza sete.', punti: 3,
                  perche: 'Giusto. Con il caldo si beve molta acqua anche se non si sente sete: gli anziani sono tra i più a rischio.' }
              : { testo: 'Esco a comprare l\'acqua, anche se sono le 16, e poi la faccio bere a piccoli sorsi.', punti: 2,
                  perche: 'Farla bere è giusto, anche senza sete. Ma uscire nelle ore più calde espone anche te: con una scorta in casa non sarebbe servito.' },
            { testo: 'Se non ha sete, va bene così.', punti: 0,
              perche: 'Si beve molta acqua anche se non si sente sete: gli anziani sono tra le persone più a rischio con il caldo.' },
            { testo: 'Le preparo una bibita gelata e zuccherata.', punti: 0,
              perche: 'Si evitano bevande zuccherate e, in grandi quantità, quelle gelate: meglio acqua fresca a piccoli sorsi.' }
          ];
        },
        link: LINK + '#cosa-fare-durante' },

      { id: 'pasquale', fase: 'durante', ora: 'Mercoledì, ore 17:00', luogo: 'casa', meteo: 'caldo',
        titolo: 'Il vicino che vive solo',
        testo: function (p) {
          return (p.vicino
            ? 'Il signor Pasquale oggi non ha risposto alla vostra telefonata. Vai subito a citofonargli.'
            : 'Da un paio di giorni non vedi il signor Pasquale, che vive solo. Passi a trovarlo.') +
            ' Ti apre confuso, con la pelle calda e arrossata, e dice che gli gira la testa.';
        },
        scelte: function (p) {
          return [
            { testo: 'Chiamo subito il 112. Intanto lo porto in un posto fresco, lo faccio sdraiare con le gambe sollevate e gli metto panni umidi su fronte e collo.', punti: p.vicino ? 3 : 2,
              perche: p.vicino
                ? 'Giusto. Sono segnali di un colpo di calore: si chiama subito il 112 e, in attesa dei soccorsi, si fa quello che dice la pagina sulle ondate di calore.'
                : 'Giusto: con i segnali del colpo di calore si chiama subito il 112. Sentendolo ogni giorno, te ne saresti accorto prima.' },
            { testo: 'Gli do un bicchiere di vino per tirarlo su.', punti: 0,
              perche: 'Con il caldo si evitano gli alcolici. Confusione, pelle calda e vertigini sono segnali da 112.' },
            { testo: 'Gli dico di riposare e passo domani.', punti: 0,
              perche: 'I primi sintomi del malessere da calore non si sottovalutano: con questi segnali si chiama subito il 112.' }
          ];
        },
        link: LINK + '#cosa-fare-dopo' },

      { id: 'dopo', fase: 'dopo', ora: 'Sabato, ore 11:30', luogo: 'casa', meteo: 'sereno',
        titolo: 'Il caldo cala',
        testo: function () {
          return 'Le temperature sono scese di qualche grado. Flavio vuole giocare a calcio con gli amici a mezzogiorno.';
        },
        scelte: [
          { testo: 'Continuiamo a bere acqua, e la partita la facciamo la sera, quando fa più fresco.', punti: 3,
            perche: 'Giusto. Si continua a bere anche quando la temperatura scende, e gli sforzi si fanno nelle ore più fresche.' },
          { testo: 'È finita: niente più attenzioni, si gioca a mezzogiorno.', punti: 0,
            perche: 'Si continua a idratarsi anche quando la temperatura scende, e gli sforzi intensi nelle ore più calde restano da evitare.' },
          { testo: 'Gioca pure a mezzogiorno, basta il cappello.', punti: 1,
            perche: 'Il cappello aiuta, ma gli sforzi fisici intensi si fanno nelle ore più fresche.' }
        ],
        link: LINK + '#cosa-fare-dopo' }
    ],

    resoconto: [
      { se: 'vicino',
        si: 'Il signor Pasquale era sentito ogni giorno: il malore è stato scoperto subito.',
        no: 'Il signor Pasquale è rimasto solo per giorni: il malore è stato scoperto tardi.' },
      { se: 'farmaci',
        si: 'Le medicine della nonna erano in un posto fresco.',
        no: 'Le medicine della nonna sono rimaste al sole: il calore può alterarne l\'efficacia.' },
      { se: 'acqua',
        si: 'In casa c\'era acqua per tutti, senza uscire nelle ore calde.',
        no: 'L\'acqua è finita e qualcuno è dovuto uscire nelle ore più calde.' },
      { se: 'ventilatore',
        si: 'Il ventilatore funzionava quando serviva.',
        no: 'Il ventilatore si è rivelato rotto proprio nei giorni peggiori.' },
      { se: 'app',
        si: 'Ogni giorno sapevate a che livello era il bollettino.',
        no: 'Non sapevate come cambiava il bollettino da un giorno all\'altro.' },
      { se: 'programma',
        si: 'Spesa e commissioni erano già organizzate fuori dalle ore più calde.',
        no: 'Le commissioni capitavano nelle ore più calde.' }
    ]
  };

  g.GenzanoScenari = g.GenzanoScenari || {};
  g.GenzanoScenari[S.id] = S;
})(window);
