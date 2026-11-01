/* Genzano si prepara — scenario «La scossa della sera».
 * Le indicazioni ripetono le pagine canoniche del sito:
 *   /rischi-prevenzione/rischio-sismico/ (prima, durante, dopo, «Se hai difficoltà di movimento»)
 *   /rischi-prevenzione/dopo-emergenza/ (gas, rientro)   /rischi-prevenzione/idee-sbagliate/
 * Se una di quelle pagine cambia un'indicazione, si aggiorna anche qui.
 * Lo scenario è inventato; i luoghi e le aree di attesa sono quelli veri di Genzano.
 */
(function (g) {
  'use strict';

  var LINK = '/rischi-prevenzione/rischio-sismico/';

  function nomeArea(p) {
    return p.area ? 'l\'area di attesa ' + p.area.id + ', ' + p.area.nome : 'l\'area di attesa più vicina';
  }

  var S = {
    id: 'terremoto',
    ordine: 2,
    icona: 'bi-house-exclamation-fill',
    titolo: 'La scossa della sera',
    rischio: 'Rischio sismico',
    durata: 'Circa 10 minuti',
    intro: [
      'Abiti a Genzano con tuo figlio Flavio e la nonna Lina, che cammina con il deambulatore.',
      'Genzano è in zona sismica 2B, a sismicità media: qui la terra trema soprattutto con sciami di scosse, di solito piccole ma a volte avvertite.',
      'Il terremoto non si può prevedere: non esistono segnali premonitori affidabili. Ci si prepara prima. È domenica pomeriggio e hai un po\' di tempo per la casa.'
    ],
    allerta: {
      testo: 'Nessuna allerta: i terremoti non si possono prevedere',
      fonte: 'INGV e Dipartimento della Protezione Civile',
      colore: 'info',
      icona: 'bi-info-circle-fill'
    },
    transizione: {
      titolo: 'La scossa è finita',
      testo: 'Dopo pochi secondi la terra smette di tremare. Adesso comincia il dopo: anche qui le scelte contano.',
      bottone: 'Che cosa facciamo adesso?',
      meteo: 'notte'
    },
    ricorda: [
      'Fissa alle pareti mobili alti e librerie, e allontana gli oggetti pesanti dai letti: [rischio sismico](/rischi-prevenzione/rischio-sismico/).',
      'Compila il [piano familiare](/piano-familiare/) e tieni pronto il [kit di emergenza](/rischi-prevenzione/kit-emergenza/) vicino all\'ingresso.'
    ],

    prima: {
      ora: 'Domenica, ore 16:00',
      luogo: 'casa',
      testo: 'Hai tempo per quattro cose. Quali scegli?',
      avanti: 'È martedì sera: andiamo avanti',
      posti: 4,
      azioni: [
        { id: 'mobili', luogo: 'casa', peso: 3,
          testo: 'Fisso alle pareti con staffe e tasselli la libreria e l\'armadio alto del salotto.',
          perche: 'In un terremoto a ferire sono soprattutto i crolli e gli oggetti che cadono: i mobili alti si fissano alle pareti.',
          link: LINK },
        { id: 'piano', luogo: 'area-vicina', peso: 3,
          testo: 'Compilo con tutta la famiglia il piano familiare e scopriamo qual è l\'area di attesa più vicina a casa.',
          perche: 'Sapere prima dove ritrovarsi e qual è l\'area di attesa evita di cercarla di notte, dopo la scossa.',
          link: '/piano-familiare/' },
        { id: 'punti', luogo: 'casa', peso: 2,
          testo: 'Individuo con Flavio i punti sicuri della casa: sotto il tavolo robusto della cucina e vicino ai muri portanti.',
          perche: 'Durante la scossa non c\'è tempo per pensare: chi sa già dove ripararsi ci va subito.',
          link: LINK },
        { id: 'nonna', luogo: 'casa', peso: 2,
          testo: 'Con la nonna Lina scegliamo una sedia robusta vicino a un muro portante, lontano da finestre e mobili alti.',
          perche: 'Chi cammina con il deambulatore non deve correre verso un tavolo durante la scossa: si siede su una sedia robusta vicino a un muro portante e si copre testa e collo.',
          link: LINK + '#riparo-mobilita' },
        { id: 'kit', luogo: 'casa', peso: 2,
          testo: 'Preparo il kit di emergenza vicino all\'ingresso, con scarpe robuste e torcia.',
          perche: 'Dopo la scossa si esce al buio, tra vetri e calcinacci: scarpe e torcia devono essere a portata di mano.',
          link: '/rischi-prevenzione/kit-emergenza/' },
        { id: 'gas', luogo: 'casa', peso: 2,
          testo: 'Imparo dove si chiudono il gas e l\'interruttore generale della luce, e lo mostro a tutti.',
          perche: 'Dopo la scossa, prima di uscire, si chiudono il gas e l\'interruttore generale dell\'elettricità. Se invece senti odore di gas, non tocchi interruttori.',
          link: LINK + '#cosa-fare-dopo' },
        { id: 'mensola', luogo: 'casa', peso: 2,
          testo: 'Tolgo la mensola con i vasi sopra il letto di Flavio.',
          perche: 'Gli oggetti pesanti si allontanano da letti e divani: in una scossa cadono su chi dorme.',
          link: LINK },
        { id: 'tecnico', luogo: 'casa', peso: 1,
          testo: 'Chiamo un tecnico per capire quanto è sicura la casa e se si può migliorare.',
          perche: 'Molte case sono più vecchie delle norme di oggi: un tecnico può valutarle e indicare come migliorarle, anche con gli incentivi del Sismabonus.',
          link: LINK },
        { id: 'previsione', luogo: 'casa', peso: 0,
          testo: 'Cerco in rete chi annuncia la data del prossimo terremoto.',
          perche: 'Il terremoto non si può prevedere: non fidarti di chi dice di saperlo fare. Il tempo serve a preparare la casa.',
          link: LINK + '#segnali' },
        { id: 'candele', luogo: 'casa', peso: 0,
          testo: 'Compro delle candele per quando va via la luce.',
          perche: 'Al buio si usano torce, non candele: possono provocare un incendio, e dopo una scossa può esserci gas nell\'aria.',
          link: '/rischi-prevenzione/blackout/' }
      ]
    },

    eventi: [
      { id: 'scossa', fase: 'durante', ora: 'Martedì, ore 21:10', luogo: 'casa', meteo: 'scossa',
        titolo: 'La terra trema',
        testo: function (p) {
          return 'Siete in cucina dopo cena. All\'improvviso il pavimento trema forte, i bicchieri tintinnano e la lampada oscilla.' +
            (p.punti ? ' Flavio sa già dove andare: ne avete parlato domenica.' : '');
        },
        scelte: [
          { testo: 'Corriamo fuori di casa.', punti: 0,
            perche: 'Non si corre fuori durante la scossa: calcinacci e oggetti in caduta causano la maggior parte delle vittime. E non si usano scale e ascensore.' },
          { testo: 'Ci abbassiamo sotto il tavolo robusto della cucina, ci copriamo testa e collo e ci teniamo, lontano dalla finestra.', punti: 3,
            perche: 'Giusto. Abbassati, copriti sotto un tavolo robusto o vicino a un muro portante, e tieniti: proteggi testa e collo, lontano da finestre e mobili alti.' },
          { testo: 'Vado alla finestra per vedere che cosa succede fuori.', punti: 0,
            perche: 'Durante la scossa ci si allontana da finestre, vetri, specchi e mobili pesanti: possono rompersi o cadere.' }
        ],
        link: LINK + '#cosa-fare-durante' },

      { id: 'nonnalina', fase: 'durante', ora: 'Martedì, ore 21:10', luogo: 'casa', meteo: 'scossa',
        titolo: 'La nonna in salotto',
        testo: function (p) {
          return p.nonna
            ? 'La nonna Lina è in salotto, sulla sedia robusta vicino al muro portante che avete scelto domenica. Ti chiama.'
            : 'La nonna Lina è in salotto, sulla poltrona accanto alla vetrata. Non riesce ad alzarsi in fretta e ti chiama.';
        },
        scelte: function (p) {
          return [
            p.nonna
              ? { testo: 'Le grido di restare seduta, piegata in avanti, coprendosi testa e collo con le braccia o con un cuscino.', punti: 3,
                  perche: 'Giusto. Chi ha difficoltà di movimento non si sposta se rischia di cadere: resta seduto dove è al sicuro e si copre testa e collo.' }
              : { testo: 'Le grido di restare seduta, piegata in avanti, coprendosi testa e collo con le braccia o con un cuscino.', punti: 2,
                  perche: 'Giusto non farla muovere se rischia di cadere. Ma è accanto alla vetrata: scegliere prima un posto sicuro, vicino a un muro portante, l\'avrebbe protetta meglio.' },
            { testo: 'Le grido di alzarsi e di venire sotto il tavolo con noi.', punti: 0,
              perche: 'Con il deambulatore, alzarsi e camminare mentre la terra trema fa rischiare una caduta: non si tenta di raggiungere un tavolo.' },
            { testo: 'Attraverso il salotto di corsa per andare da lei mentre tutto trema.', punti: 0,
              perche: 'Muoversi durante la scossa espone te agli oggetti che cadono. Prima ci si protegge, e si dice subito alla nonna come proteggersi.' }
          ];
        },
        link: LINK + '#riparo-mobilita' },

      { id: 'gasodore', fase: 'dopo', ora: 'Martedì, ore 21:12', luogo: 'casa', meteo: 'notte',
        titolo: 'Odore di gas',
        testo: function (p) {
          return 'State tutti bene. In cucina però senti un leggero odore di gas.' +
            (p.gas ? ' Sai dov\'è il rubinetto del contatore: l\'hai mostrato a tutti domenica.' : ' Non sai bene dove si chiude il gas.');
        },
        scelte: function (p) {
          return [
            { testo: 'Accendo la luce per vedere da dove viene.', punti: 0,
              perche: 'Con l\'odore di gas non si accendono luci o fiamme e non si usano interruttori: una scintilla può bastare.' },
            p.gas
              ? { testo: 'Non tocco interruttori né fiamme, apro le finestre, chiudo il contatore e ci avviamo all\'uscita. Il 112 lo chiamo da fuori.', punti: 3,
                  perche: 'Giusto. Finestre aperte, contatore chiuso, tutti fuori, e i soccorsi si chiamano dall\'esterno: nel locale con il gas non si usa nessun telefono.' }
              : { testo: 'Non tocco interruttori né fiamme, apro le finestre e ci avviamo tutti all\'uscita. Il 112 lo chiamo da fuori.', punti: 2,
                  perche: 'Giusto uscire e chiamare da fuori, senza usare telefoni in casa. Sapere prima dove si chiude il contatore ti avrebbe permesso di chiuderlo subito.' },
            { testo: 'Chiamo subito il 112 con il cellulare, qui in cucina.', punti: 0,
              perche: 'Nel locale con il gas non si usa nessun telefono, né fisso né cellulare: si esce e si chiama il 112 da fuori.' }
          ];
        },
        link: '/rischi-prevenzione/dopo-emergenza/' },

      { id: 'uscire', fase: 'dopo', ora: 'Martedì, ore 21:15', luogo: 'casa', meteo: 'notte',
        titolo: 'Uscire di casa',
        testo: function (p) {
          return 'State per lasciare la casa. È andata via la luce e sul pavimento ci sono vetri rotti.' +
            (p.kit ? ' Il kit con le scarpe robuste e la torcia è vicino all\'ingresso.' : ' Le scarpe sono in camera e la torcia non si trova.');
        },
        scelte: function (p) {
          return [
            { testo: 'Prendiamo l\'ascensore: la nonna fa fatica con le scale.', punti: 0,
              perche: 'Dopo una scossa l\'ascensore può bloccarsi e lasciarvi intrappolati. Si scende per le scale, aiutando la nonna.' },
            p.kit
              ? { testo: 'Mettiamo le scarpe, prendiamo il kit e scendiamo per le scale con calma, aiutando la nonna.', punti: 3,
                  perche: 'Giusto. Si esce con prudenza, con le scarpe ai piedi, perché possono esserci vetri e calcinacci.' }
              : { testo: 'Cerchiamo al buio le scarpe, facendo attenzione ai vetri, poi scendiamo per le scale aiutando la nonna.', punti: 2,
                  perche: 'Giusto uscire con le scarpe e per le scale. Con il kit pronto all\'ingresso avreste perso meno tempo al buio.' },
            { testo: 'Usciamo scalzi per fare prima.', punti: 0,
              perche: 'Dopo una scossa possono esserci vetri e calcinacci: si esce con le scarpe ai piedi.' }
          ];
        },
        link: LINK + '#cosa-fare-dopo' },

      { id: 'strada', fase: 'dopo', ora: 'Martedì, ore 21:25', luogo: 'casa', meteo: 'notte',
        titolo: 'In strada',
        testo: function (p) {
          return 'Siete in strada. Molti vicini sono fermi sotto i balconi a parlare.' +
            (p.piano ? ' Sapete già dove andare: ' + nomeArea(p) + '.' : ' Non sapete qual è l\'area di attesa più vicina.');
        },
        scelte: function (p) {
          return [
            { testo: 'Restiamo qui sotto i balconi, al riparo.', punti: 0,
              perche: 'Dopo la scossa si sta lontano dagli edifici: cornicioni, vetri e calcinacci possono ancora cadere.' },
            p.piano
              ? { testo: 'Andiamo a piedi a ' + nomeArea(p) + ', lontano da edifici, alberi e fili elettrici.', punti: 3,
                  perche: 'Giusto. Le aree di attesa sono i luoghi sicuri dove ritrovarsi e ricevere le prime informazioni.' }
              : { testo: 'Cerco sul telefono l\'area di attesa più vicina e ci andiamo a piedi, lontano da edifici e fili elettrici.', punti: 2,
                  perche: 'Giusto andare all\'area di attesa. Con il piano familiare l\'avreste saputo già, senza cercarla di notte.' },
            { testo: 'Torno un attimo in casa a prendere il portafoglio.', punti: 0,
              perche: 'Non si rientra in casa finché le autorità non lo consentono: un edificio che ha retto la prima scossa può avere lesioni che non si vedono.' }
          ];
        },
        link: '/aree-attesa/' },

      { id: 'telefono', fase: 'dopo', ora: 'Martedì, ore 21:45', luogo: 'area-vicina', meteo: 'notte',
        titolo: 'All\'area di attesa',
        testo: function (p) {
          return 'Siete arrivati a ' + nomeArea(p) + '. Ci sono altre famiglie e i volontari della protezione civile, attivati dal Comune, che danno le prime informazioni. Tutti hanno il telefono in mano.';
        },
        scelte: [
          { testo: 'Telefono a tutti i parenti, uno dopo l\'altro, per raccontare la scossa.', punti: 0,
            perche: 'Dopo un terremoto le linee si saturano: il telefono si usa solo in caso di vera emergenza, per lasciarle libere.' },
          { testo: 'Uso il telefono solo se serve davvero e seguo le informazioni dei canali ufficiali.', punti: 3,
            perche: 'Giusto. Le linee servono ai soccorsi; le notizie si prendono dalle autorità, via radio o dai canali ufficiali.' },
          { testo: 'Faccio una diretta sui social per far vedere com\'è la situazione.', punti: 0,
            perche: 'Non si usa il telefono per curiosità: le linee e la rete servono a chi ha un\'emergenza.' }
        ],
        link: LINK + '#cosa-fare-dopo' },

      { id: 'voce', fase: 'dopo', ora: 'Martedì, ore 22:30', luogo: 'area-vicina', meteo: 'notte',
        titolo: 'Un messaggio sul telefono',
        testo: function () {
          return 'Arriva un messaggio: «Stanotte alle 3 ci sarà una scossa più forte, lo dice un esperto. Giratelo a tutti!».';
        },
        scelte: [
          { testo: 'Lo inoltro: meglio che lo sappiano tutti.', punti: 0,
            perche: 'Nessuno può dire quando arriverà una scossa. Un messaggio falso spaventa e confonde: le notizie non verificate non si diffondono.' },
          { testo: 'Non lo inoltro: i terremoti non si possono prevedere. Seguo solo le informazioni del Comune e della protezione civile.', punti: 3,
            perche: 'Giusto. Non esistono previsioni dei terremoti: si seguono solo le fonti ufficiali.' },
          { testo: 'Torno a casa a prendere le coperte prima delle tre.', punti: 0,
            perche: 'Non si rientra in casa finché le autorità non lo consentono, e non si decide in base a un messaggio senza fonte.' }
        ],
        link: '/rischi-prevenzione/idee-sbagliate/' },

      { id: 'rientro', fase: 'dopo', ora: 'Mercoledì, ore 9:00', luogo: 'casa', meteo: 'sereno',
        titolo: 'Tornare a casa?',
        testo: function () {
          return 'È mattina. Da fuori la casa sembra a posto, ci sono solo alcune crepe nell\'intonaco. Vorresti rientrare.';
        },
        scelte: [
          { testo: 'Rientro: le crepe sono piccole.', punti: 0,
            perche: 'Un edificio che ha retto la prima scossa può avere lesioni che non si vedono, e possono arrivare altre scosse.' },
          { testo: 'Aspetto che le autorità dicano che si può rientrare, dopo le verifiche dei tecnici.', punti: 3,
            perche: 'Giusto. Si rientra solo quando le autorità lo consentono: gli edifici lesionati non si usano prima del via libera dei tecnici.' },
          { testo: 'Entro solo un minuto a prendere i vestiti.', punti: 0,
            perche: 'Non si rientra negli edifici danneggiati nemmeno per recuperare oggetti.' }
        ],
        link: '/rischi-prevenzione/dopo-emergenza/' }
    ],

    resoconto: [
      { se: 'mobili',
        si: 'La libreria e l\'armadio erano fissati alle pareti: sono rimasti al loro posto.',
        no: 'La libreria non era fissata ed è caduta sul pavimento del salotto. Per fortuna lì non c\'era nessuno.' },
      { se: 'mensola',
        si: 'Sopra il letto di Flavio non c\'era più niente che potesse cadere.',
        no: 'La mensola sopra il letto di Flavio è caduta sul cuscino: se la scossa fosse arrivata di notte, poteva colpirlo.' },
      { se: 'nonna',
        si: 'La nonna Lina era nel posto sicuro che avevate scelto insieme.',
        no: 'La nonna Lina era accanto alla vetrata: un vetro rotto poteva ferirla.' },
      { se: 'punti',
        si: 'Flavio sapeva già dove ripararsi e ci è andato subito.',
        no: 'Nei primi secondi Flavio non sapeva dove ripararsi.' },
      { se: 'piano',
        si: 'Sapevate già qual era l\'area di attesa e dove ritrovarvi.',
        no: 'Avete dovuto cercare l\'area di attesa di notte, con le linee telefoniche intasate.' },
      { se: 'kit',
        si: 'Scarpe robuste e torcia erano pronte all\'ingresso.',
        no: 'Avete cercato scarpe e torcia al buio, tra i vetri.' },
      { se: 'gas',
        si: 'Sapevate dove chiudere il gas: l\'avete fatto subito.',
        no: 'Non sapevate dove si chiude il gas: avete perso tempo a cercare il contatore.' },
      { se: 'tecnico',
        si: 'Un tecnico aveva già indicato come rendere la casa più sicura: è la prevenzione che conta di più.',
        no: 'Non sapete ancora quanto è sicura la vostra casa: un tecnico può valutarla e indicare come migliorarla.' }
    ]
  };

  g.GenzanoScenari = g.GenzanoScenari || {};
  g.GenzanoScenari[S.id] = S;
})(window);
