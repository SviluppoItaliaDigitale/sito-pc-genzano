/* Genzano si prepara — scenario «Il temporale di ottobre».
 * Testi e regole del primo scenario. Le indicazioni ripetono, con le stesse
 * parole dove possibile, le pagine canoniche del sito:
 *   /rischi-prevenzione/rischio-idrogeologico/  /rischi-prevenzione/temporali-intensi/
 *   /rischi-prevenzione/vento-forte/  /rischi-prevenzione/blackout/
 *   /rischi-prevenzione/persone-necessita-specifiche/  /allerte-meteo/
 * Se una di quelle pagine cambia un'indicazione, si aggiorna anche qui.
 * Lo scenario è inventato; i luoghi della mappa sono quelli veri di Genzano.
 */
(function (g) {
  'use strict';

  var S = {
    id: 'temporale',
    titolo: 'Il temporale di ottobre',
    rischio: 'Rischio idrogeologico e temporali',
    durata: 'Circa 10 minuti',
    intro: [
      'Abiti a Genzano con tuo figlio Flavio e la nonna Lina. La nonna dorme nella stanza al piano seminterrato.',
      'È giovedì pomeriggio. Sul telefono leggi che il Centro Funzionale della Regione Lazio ha emesso un\'allerta arancione per rischio idrogeologico e temporali sulla Zona F, quella di Genzano, valida per domani.'
    ],
    allerta: {
      livello: 'arancione',
      testo: 'Allerta arancione per rischio idrogeologico e temporali — Zona F — valida venerdì',
      fonte: 'Centro Funzionale della Regione Lazio'
    },

    /* ---------- PRIMA: scegli come usare il tempo che hai ---------- */
    prima: {
      ora: 'Giovedì, ore 17:00',
      luogo: 'casa',
      testo: 'Prima di cena hai tempo per quattro cose. Quali scegli?',
      posti: 4,
      azioni: [
        { id: 'nonna', luogo: 'casa', peso: 3,
          testo: 'Sposto la nonna Lina nella camera di Flavio, al primo piano, finché dura l\'allerta.',
          perche: 'Con l\'allerta non si dorme nei seminterrati: sono i primi locali ad allagarsi.',
          link: '/rischi-prevenzione/temporali-intensi/' },
        { id: 'bollettino', luogo: 'casa', peso: 2,
          testo: 'Leggo il bollettino e i consigli sulla pagina Allerte meteo, e organizzo la giornata di domani.',
          perche: 'Conoscere l\'allerta permette di evitare spostamenti inutili quando il tempo peggiora.',
          link: '/allerte-meteo/' },
        { id: 'kit', luogo: 'casa', peso: 2,
          testo: 'Controllo il kit di emergenza: torcia, radio a pile, batterie cariche.',
          perche: 'Un temporale può togliere la corrente: con il kit pronto resti autonomo.',
          link: '/rischi-prevenzione/kit-emergenza/' },
        { id: 'caditoia', luogo: 'casa', peso: 2,
          testo: 'Libero dalle foglie la caditoia davanti a casa.',
          perche: 'Se le caditoie sono intasate, l\'acqua si raccoglie nei punti più bassi: cantine e garage.',
          link: '/rischi-prevenzione/rischio-idrogeologico/' },
        { id: 'auto', luogo: 'casa', peso: 2,
          testo: 'Tolgo l\'auto dal garage interrato e la parcheggio in una strada più in alto, lontano dagli alberi.',
          perche: 'Mettere al sicuro l\'auto prima evita la tentazione più pericolosa: scendere in garage durante l\'allagamento.',
          link: '/rischi-prevenzione/rischio-idrogeologico/' },
        { id: 'vicino', luogo: 'casa', peso: 2,
          testo: 'Passo dal signor Pasquale, il vicino che vive solo: gli lascio il mio numero e gli chiedo se ha bisogno di qualcosa.',
          perche: 'La rete di vicinato è la prima risorsa in emergenza, soprattutto per chi vive solo.',
          link: '/rischi-prevenzione/persone-necessita-specifiche/' },
        { id: 'cantina', luogo: 'casa', peso: 1,
          testo: 'Porto via dalla cantina gli album di foto e le cose di valore.',
          perche: 'Non si lasciano oggetti di valore in cantine o garage a rischio di allagamento.',
          link: '/rischi-prevenzione/rischio-idrogeologico/' },
        { id: 'balcone', luogo: 'casa', peso: 1,
          testo: 'Ritiro dal balcone i vasi e le sedie che il vento può far volare.',
          perche: 'Con i temporali arrivano raffiche improvvise: gli oggetti sul balcone possono cadere in strada.',
          link: '/rischi-prevenzione/vento-forte/' },
        { id: 'giro', luogo: 'lago', peso: 0,
          testo: 'Faccio un giro in auto fino al lago per vedere com\'è il cielo.',
          perche: 'Non prepara niente: il tempo prima di un\'allerta vale di più se lo usi per la casa e per le persone.',
          link: '/allerte-meteo/' },
        { id: 'catena', luogo: 'casa', peso: 0,
          testo: 'Inoltro a tutti i gruppi un messaggio che dice «domani chiudono tutte le scuole del Lazio».',
          perche: 'Un messaggio non verificato confonde le persone. Le decisioni sulle scuole le comunicano i canali ufficiali.',
          link: '/allerte-meteo/' }
      ]
    },

    /* ---------- DURANTE e DOPO: gli eventi uno dopo l'altro ---------- */
    eventi: [
      { id: 'fulmini', fase: 'durante', ora: 'Venerdì, ore 16:30', luogo: 'parco', meteo: 'pioggia',
        titolo: 'Tuoni sul parco',
        testo: function (p) {
          return (p.bollettino
            ? 'Hai letto l\'allerta: dopo la scuola tu e Flavio tornate subito a casa, a piedi, passando per il Parco Sforza-Cesarini. '
            : 'Dopo la scuola hai portato Flavio a giocare al Parco Sforza-Cesarini. ') +
            'Il temporale arriva prima del previsto: il cielo diventa nero, si sentono i tuoni e iniziano i lampi. Siete vicino a un grande albero, da solo in mezzo al prato.';
        },
        scelte: [
          { testo: 'Ci ripariamo sotto il grande albero.', punti: 0,
            perche: 'Gli alberi isolati attirano i fulmini: sotto un albero sei più in pericolo, non meno.' },
          { testo: 'Raggiungiamo subito un edificio solido, o l\'auto con i finestrini chiusi.', punti: 3,
            perche: 'Giusto. Un edificio solido o un\'auto con tetto rigido e finestrini chiusi sono ripari sicuri dai fulmini.' },
          { testo: 'Restiamo sulla panchina sotto l\'ombrello e aspettiamo che passi.', punti: 0,
            perche: 'All\'aperto, con un ombrello e vicino a un albero, sei esposto ai fulmini. Bisogna entrare al chiuso.' }
        ],
        link: '/rischi-prevenzione/temporali-intensi/' },

      { id: 'strada', fase: 'durante', ora: 'Venerdì, ore 18:00', luogo: 'strada', meteo: 'pioggia',
        titolo: 'La strada allagata',
        testo: function (p) {
          return (p.bollettino
            ? 'Sapevi dell\'allerta e stai rientrando presto dal lavoro. '
            : 'Non hai guardato l\'allerta e sei ancora in giro in auto con la pioggia forte. ') +
            'In fondo a una strada in discesa l\'acqua copre l\'asfalto. Sembrano pochi centimetri.';
        },
        scelte: [
          { testo: 'Passo piano: sono pochi centimetri.', punti: 0,
            perche: 'Sotto l\'acqua non vedi buche e tombini aperti, e pochi centimetri bastano a far perdere aderenza o a spegnere il motore.' },
          { testo: 'Scendo dall\'auto per vedere quanto è profonda.', punti: 0,
            perche: 'A piedi nell\'acqua che scorre si rischia di essere trascinati. Non si attraversano strade allagate, né a piedi né in auto.' },
          { testo: 'Torno indietro e faccio un\'altra strada, più in alto.', punti: 3,
            perche: 'Giusto. Una strada o un sottopasso allagati non si attraversano mai: si cambia percorso, verso un punto più alto.' }
        ],
        link: '/rischi-prevenzione/rischio-idrogeologico/' },

      { id: 'messaggio', fase: 'durante', ora: 'Venerdì, ore 19:30', luogo: 'casa', meteo: 'pioggia',
        titolo: 'Un messaggio che fa paura',
        testo: function () {
          return 'Sei a casa. In un gruppo arriva un messaggio: «La diga sta per cedere, scappate tutti! Giratelo!». Non c\'è nessuna fonte.';
        },
        scelte: [
          { testo: 'Lo giro subito a tutti: meglio avvisare.', punti: 0,
            perche: 'Un messaggio falso fa uscire le persone in strada proprio durante il temporale, e rallenta i soccorsi.' },
          { testo: 'Non lo inoltro e controllo i canali ufficiali del Comune e della protezione civile.', punti: 3,
            perche: 'Giusto. Se un messaggio ti spaventa, verificalo prima di inoltrarlo: segui solo le fonti ufficiali.' },
          { testo: 'Esco in auto per andare a vedere.', punti: 0,
            perche: 'Uscire durante un temporale forte, per di più verso un pericolo, ti espone a strade allagate e fulmini.' }
        ],
        link: '/allerte-meteo/' },

      { id: 'vento', fase: 'durante', ora: 'Venerdì, ore 21:00', luogo: 'casa', meteo: 'pioggia',
        titolo: 'Raffiche di vento',
        testo: function (p) {
          return p.balcone
            ? 'Arrivano raffiche fortissime. Sul balcone non c\'è più niente che possa volare: l\'hai ritirato ieri.'
            : 'Arrivano raffiche fortissime. Un vaso vola giù dal balcone e si rompe sul marciapiede. Per fortuna in strada non c\'era nessuno.';
        },
        scelte: [
          { testo: 'Esco sul balcone a sistemare le altre cose.', punti: 0,
            perche: 'Durante il vento forte non ci si espone per recuperare oggetti: si resta dentro.' },
          { testo: 'Resto dentro, lontano da finestre e porte finestre.', punti: 3,
            perche: 'Giusto. Durante il temporale si sta al chiuso, lontano da finestre e porte finestre.' },
          { testo: 'Apro la finestra per fare un video ai fulmini.', punti: 0,
            perche: 'Davanti a una finestra aperta sei esposto a vento, oggetti che volano e fulmini. Il video può aspettare.' }
        ],
        link: '/rischi-prevenzione/vento-forte/' },

      { id: 'blackout', fase: 'durante', ora: 'Venerdì, ore 22:00', luogo: 'casa', meteo: 'buio',
        titolo: 'Va via la corrente',
        testo: function (p) {
          return p.kit
            ? 'Va via la corrente in tutta la via. La torcia e la radio a pile sono dove le hai lasciate ieri, con le batterie cariche.'
            : 'Va via la corrente in tutta la via. Non sai dove sia la torcia e le batterie della radio sono scariche.';
        },
        scelte: function (p) {
          return [
            { testo: 'Accendo le candele in salotto.', punti: 0,
              perche: 'Le candele possono provocare un incendio. Al buio si usano torce, non candele.' },
            p.kit
              ? { testo: 'Uso la torcia e ascolto le notizie con la radio a pile. Tengo chiuso il frigorifero.', punti: 3,
                  perche: 'Giusto. Torcia e radio a pile sono la luce e l\'informazione sicure; il frigorifero chiuso conserva il cibo per ore.' }
              : { testo: 'Uso la luce del telefono per poco, per non scaricarlo, e tengo chiuso il frigorifero.', punti: 1,
                  perche: 'È la scelta meno peggio, ma il telefono ti serve carico per chiamare il 112. Con il kit pronto avresti avuto torcia e radio.' },
            { testo: 'Scendo in cantina a cercare una torcia.', punti: 0,
              perche: 'Con la pioggia forte non si scende in cantina: è il primo locale che si allaga.' }
          ];
        },
        link: '/rischi-prevenzione/blackout/' },

      { id: 'acqua', fase: 'durante', ora: 'Venerdì, ore 23:00', luogo: 'casa', meteo: 'buio',
        titolo: 'L\'acqua entra in casa',
        testo: function (p) {
          var t = p.caditoia
            ? 'La caditoia davanti casa porta via molta acqua, ma la pioggia è troppa: un filo d\'acqua entra nel seminterrato.'
            : 'La caditoia davanti casa è piena di foglie: l\'acqua si ferma davanti al portone ed entra nel seminterrato.';
          t += p.nonna
            ? ' La nonna Lina dorme al primo piano: è al sicuro.'
            : ' La nonna Lina dorme proprio lì, nella stanza del seminterrato! Per ora l\'acqua è ancora bassa.';
          if (!p.auto) t += ' E l\'auto è nel garage interrato.';
          return t;
        },
        scelte: function (p) {
          var s = [];
          if (p.nonna) {
            s.push({ testo: 'Resto su e chiudo la porta che porta al piano di sotto. Se l\'acqua arriva agli impianti e posso farlo senza rischi, stacco gas e corrente.', punti: 3,
              perche: 'Giusto. Si resta ai piani alti, si chiudono le porte verso i locali bassi e, solo senza rischi, si staccano gas e corrente.' });
            s.push({ testo: 'Scendo a mettere degli stracci sotto la porta della cantina.', punti: 0,
              perche: 'Non si scende mai in cantine, garage o locali interrati durante un allagamento.' });
          } else {
            s.push({ testo: 'Corro giù, sveglio la nonna e la porto subito al primo piano per le scale, senza fermarmi a prendere niente.', punti: 2,
              perche: 'In questo momento è la cosa giusta: le persone prima delle cose, per le scale e non in ascensore. Ma averla spostata prima avrebbe evitato di scendere con l\'acqua che entra.' });
            s.push({ testo: 'Portiamo su la nonna con l\'ascensore, è più comodo.', punti: 0,
              perche: 'Con l\'acqua in casa e il rischio di blackout l\'ascensore può bloccarsi. Si usano le scale.' });
          }
          if (!p.auto) {
            s.push({ testo: 'Scendo in garage a spostare l\'auto.', punti: 0,
              perche: 'Cantine e garage si allagano per primi e la spinta dell\'acqua può bloccare la porta. L\'auto si sostituisce, una persona no.' });
          } else {
            s.push({ testo: 'Vado ad aprire il portone per far uscire l\'acqua.', punti: 0,
              perche: 'Per aprire il portone dovresti scendere dove l\'acqua sta entrando. Si resta ai piani alti.' });
          }
          return s;
        },
        link: '/rischi-prevenzione/rischio-idrogeologico/' },

      { id: 'albero', fase: 'durante', ora: 'Venerdì, ore 23:45', luogo: 'casa', meteo: 'buio',
        titolo: 'Un albero sulla strada',
        testo: function () {
          return 'Dalla finestra vedi che un albero è caduto in strada e ha tirato giù un cavo elettrico. Qualcuno potrebbe passare di lì.';
        },
        scelte: [
          { testo: 'Chiamo il 112 e dico dove si trova il pericolo. Resto lontano dal cavo.', punti: 3,
            perche: 'Giusto. Le situazioni di pericolo si segnalano al 112, che manda chi deve intervenire. Ai cavi caduti non ci si avvicina.' },
          { testo: 'Chiamo direttamente i volontari della protezione civile di Genzano.', punti: 1,
            perche: 'Il Gruppo Comunale non può essere attivato direttamente dai cittadini: si chiama il 112. Sono il Comune e le sale operative ad attivare i volontari.' },
          { testo: 'Scendo a spostare i rami per liberare la strada.', punti: 0,
            perche: 'Un cavo elettrico caduto può essere ancora in tensione. Non ci si avvicina e non si toccano i rami.' }
        ],
        link: '/rischi-prevenzione/temporali-intensi/' },

      { id: 'cantina', fase: 'dopo', ora: 'Sabato, ore 8:00', luogo: 'casa', meteo: 'sereno',
        titolo: 'La mattina dopo',
        testo: function () {
          return 'Ha smesso di piovere. Il Comune ha attivato il Centro Operativo Comunale e le squadre sono al lavoro. Nel seminterrato ci sono venti centimetri d\'acqua e fango.';
        },
        scelte: [
          { testo: 'Scendo e accendo la luce per vedere i danni.', punti: 0,
            perche: 'Non si entra in locali allagati dove ci sono impianti elettrici: accendere la luce può essere pericoloso.' },
          { testo: 'Non scendo finché non è sicuro, non tocco impianti bagnati e faccio le foto dei danni dall\'alto delle scale.', punti: 3,
            perche: 'Giusto. Si aspetta che sia sicuro, non si toccano impianti bagnati e si documentano i danni con le foto per le richieste di risarcimento.' },
          { testo: 'Comincio a svuotare l\'acqua con i secchi, a piedi nudi.', punti: 0,
            perche: 'Nell\'acqua del seminterrato possono esserci impianti in tensione, vetri e fango contaminato. Si aspetta che sia sicuro.' }
        ],
        link: '/rischi-prevenzione/rischio-idrogeologico/' },

      { id: 'rubinetto', fase: 'dopo', ora: 'Sabato, ore 8:30', luogo: 'casa', meteo: 'sereno',
        titolo: 'Il caffè della mattina',
        testo: function () {
          return 'Vuoi preparare il caffè con l\'acqua del rubinetto. Dopo un allagamento l\'acquedotto potrebbe avere problemi.';
        },
        scelte: [
          { testo: 'Controllo se il Comune ha pubblicato avvisi sull\'acqua prima di berla.', punti: 3,
            perche: 'Giusto. Dopo un\'alluvione l\'acqua del rubinetto si beve solo se ordinanze o avvisi del Comune non lo vietano.' },
          { testo: 'La bevo: l\'acqua del rubinetto è sempre buona.', punti: 0,
            perche: 'Non sempre: dopo un allagamento l\'acqua può essere contaminata. Prima si controllano gli avvisi del Comune.' },
          { testo: 'Chiedo nel gruppo dei vicini cosa ne pensano.', punti: 1,
            perche: 'I vicini possono aiutare, ma la risposta giusta la danno gli avvisi ufficiali del Comune.' }
        ],
        link: '/rischi-prevenzione/rischio-idrogeologico/' },

      { id: 'pasquale', fase: 'dopo', ora: 'Sabato, ore 9:00', luogo: 'casa', meteo: 'sereno',
        solo: function (p) { return !p.vicino; },
        titolo: 'Il vicino che vive solo',
        testo: function () {
          return 'Il signor Pasquale, che vive solo, stamattina non si è visto. Di solito alle otto è già sul balcone.';
        },
        scelte: [
          { testo: 'Passo a citofonargli. Se non risponde e temo che stia male, chiamo il 112.', punti: 3,
            perche: 'Giusto. Si aiuta chi è in difficoltà se lo si può fare senza esporsi a pericoli, e si chiama il 112 se una persona può essere in pericolo.' },
          { testo: 'Aspetto qualche giorno: magari è partito.', punti: 0,
            perche: 'Una persona anziana sola, dopo una notte di temporale, può avere bisogno d\'aiuto subito.' },
          { testo: 'Scrivo un post sui social per chiedere se qualcuno l\'ha visto.', punti: 1,
            perche: 'Può aiutare, ma è lento. Prima si passa a vedere; se si teme un pericolo, si chiama il 112.' }
        ],
        link: '/rischi-prevenzione/persone-necessita-specifiche/' }
    ],

    /* ---------- Il resoconto: che cosa ha cambiato la preparazione ---------- */
    resoconto: [
      { se: 'nonna',
        si: 'La nonna Lina ha dormito al primo piano: quando l\'acqua è entrata nel seminterrato era già al sicuro.',
        no: 'La nonna Lina dormiva nel seminterrato: avete dovuto portarla su di notte, con l\'acqua che entrava.' },
      { se: 'auto',
        si: 'L\'auto era parcheggiata in alto: nessuno ha dovuto pensare di scendere in garage.',
        no: 'L\'auto era nel garage interrato: in garage l\'acqua può bloccare la porta, e la tentazione di scendere è forte.' },
      { se: 'caditoia',
        si: 'La caditoia pulita ha portato via buona parte dell\'acqua davanti al portone.',
        no: 'La caditoia piena di foglie ha fatto ristagnare l\'acqua proprio davanti al portone.' },
      { se: 'kit',
        si: 'Durante il blackout avevate torcia e radio a pile pronte.',
        no: 'Durante il blackout la torcia non si trovava e la radio era scarica.' },
      { se: 'cantina',
        si: 'Gli album di foto erano già al sicuro: l\'acqua in cantina non ha rovinato i ricordi.',
        no: 'Gli album di foto erano in cantina: l\'acqua li ha rovinati.' },
      { se: 'balcone',
        si: 'Dal balcone non è caduto niente.',
        no: 'Un vaso è caduto dal balcone sul marciapiede: poteva colpire qualcuno.' },
      { se: 'vicino',
        si: 'Il signor Pasquale aveva il tuo numero: sapeva a chi chiedere aiuto.',
        no: 'Il signor Pasquale ha passato la notte da solo, senza sapere a chi chiedere aiuto.' },
      { se: 'bollettino',
        si: 'Conoscevi l\'allerta e hai organizzato la giornata di conseguenza.',
        no: 'Non conoscevi l\'allerta: il temporale ti ha sorpreso in giro.' }
    ]
  };

  g.GenzanoScenari = g.GenzanoScenari || {};
  g.GenzanoScenari[S.id] = S;
})(window);
