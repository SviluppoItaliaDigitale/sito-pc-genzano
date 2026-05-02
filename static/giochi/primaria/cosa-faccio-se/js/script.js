document.addEventListener('DOMContentLoaded', () => {
    const selectScreen = document.getElementById('select-screen');
    const storyScreen = document.getElementById('story-screen');
    const endScreen = document.getElementById('end-screen');
    const scenarioList = document.getElementById('scenario-list');
    const scenarioBadge = document.getElementById('scenario-badge');
    const stepNum = document.getElementById('step-num');
    const storyCard = document.getElementById('story-card');
    const storyText = document.getElementById('story-text');
    const choicesContainer = document.getElementById('choices-container');
    const storyFeedback = document.getElementById('story-feedback');
    const endMessage = document.getElementById('end-message');
    const endErrors = document.getElementById('end-errors');
    const anotherBtn = document.getElementById('another-btn');

    const scenarios = [
        {
            id: 'terremoto', title: 'Terremoto a scuola', icon: '\uD83C\uDFEB',
            steps: [
                {
                    text: 'Sei in classe durante la lezione di italiano. All\'improvviso senti il pavimento tremare e i vetri vibrare. La scossa e forte. Cosa fai?',
                    choices: [
                        { text: 'Mi alzo e corro verso la porta per uscire', correct: false, tip: 'Durante la scossa non si corre! Le scale e i corridoi possono essere più pericolosi.' },
                        { text: 'Mi riparo sotto il banco e mi proteggo la testa con le braccia', correct: true, tip: 'Perfetto! Sotto il banco sei protetto dagli oggetti che possono cadere.' },
                        { text: 'Mi avvicino alla finestra per guardare fuori', correct: false, tip: 'Le finestre possono rompersi durante un terremoto. Stai lontano!' }
                    ]
                },
                {
                    text: 'La scossa e finita. La maestra dice di prepararsi a uscire. Alcuni compagni vogliono prendere zaini e giubbotti. Cosa fai?',
                    choices: [
                        { text: 'Prendo il mio zaino, ci sono le mie cose importanti', correct: false, tip: 'Gli zaini rallentano la fila e possono far inciampare. La sicurezza viene prima delle cose!' },
                        { text: 'Mi metto in fila senza prendere niente e seguo la maestra', correct: true, tip: 'Giusto! In evacuazione si esce leggeri e ordinati.' }
                    ]
                },
                {
                    text: 'Siete in fila nel corridoio. Un compagno vuole prendere l\'ascensore perché ha paura delle scale. Cosa gli dici?',
                    choices: [
                        { text: '"Hai ragione, l\'ascensore e più veloce"', correct: false, tip: 'L\'ascensore può bloccarsi dopo un terremoto. Non si usa mai!' },
                        { text: '"No, dopo un terremoto si usano solo le scale. Vieni con noi!"', correct: true, tip: 'Bravo! L\'ascensore può restare bloccato. Le scale sono la via sicura.' }
                    ]
                },
                {
                    text: 'Siete arrivati al punto di raccolta nel cortile. La maestra fa l\'appello. Un compagno manca. Cosa fai?',
                    choices: [
                        { text: 'Torno dentro a cercarlo', correct: false, tip: 'Non rientrare mai nell\'edificio! Dillo alla maestra, sara lei a coordinarsi con i soccorritori.' },
                        { text: 'Lo dico subito alla maestra', correct: true, tip: 'Esatto! La maestra avvisera chi di dovere. Tu resta al punto di raccolta.' }
                    ]
                }
            ],
            endMsg: 'Hai gestito il terremoto a scuola come un vero esperto! Ricorda: abbassati, riparati, aspetta.'
        },
        {
            id: 'temporale', title: 'Temporale al parco', icon: '\u26C8\uFE0F',
            steps: [
                {
                    text: 'Sei al parco con gli amici. Il cielo diventa scuro all\'improvviso, senti un tuono in lontananza e il vento aumenta. Cosa fai?',
                    choices: [
                        { text: 'Continuo a giocare, e solo un tuono lontano', correct: false, tip: 'I temporali possono arrivare molto in fretta. Meglio non aspettare!' },
                        { text: 'Mi metto sotto il grande albero per ripararmi', correct: false, tip: 'Mai sotto gli alberi durante un temporale! I fulmini colpiscono gli oggetti alti.' },
                        { text: 'Chiedo ai miei amici di andare subito verso un edificio', correct: true, tip: 'Ottima scelta! Un edificio in muratura e il posto più sicuro.' }
                    ]
                },
                {
                    text: 'State correndo verso casa, ma il temporale vi raggiunge. Piove fortissimo, ci sono fulmini. Vedete un gazebo in metallo e un bar con le porte aperte. Dove andate?',
                    choices: [
                        { text: 'Sotto il gazebo in metallo, e più vicino', correct: false, tip: 'Le strutture metalliche attirano i fulmini. Meglio un edificio chiuso!' },
                        { text: 'Dentro il bar, al riparo dalle intemperie', correct: true, tip: 'Perfetto! Un edificio chiuso e il riparo migliore durante un temporale.' }
                    ]
                },
                {
                    text: 'Siete al sicuro dentro il bar. Un amico vuole chiamare la mamma con il telefono, un altro vuole stare vicino alla vetrina per guardare i fulmini. Cosa consigli?',
                    choices: [
                        { text: '"Chiamare la mamma va bene, ma restiamo lontani dalle finestre"', correct: true, tip: 'Giusto! Il telefono cellulare si può usare, ma le finestre possono essere pericolose.' },
                        { text: '"Andiamo alla vetrina, i fulmini sono bellissimi da guardare!"', correct: false, tip: 'Le finestre possono rompersi con la grandine o il vento. Meglio stare al centro del locale.' }
                    ]
                },
                {
                    text: 'Il temporale e passato, ma in strada ci sono rami caduti e pozzanghere grandi. Cosa fai per tornare a casa?',
                    choices: [
                        { text: 'Cammino normalmente, tanto ha smesso di piovere', correct: false, tip: 'Dopo un temporale ci possono essere pericoli nascosti: rami instabili, cavi elettrici, buche sotto le pozzanghere.' },
                        { text: 'Cammino con attenzione, evito le pozzanghere e i rami a terra', correct: true, tip: 'Bravo! Dopo il temporale bisogna fare attenzione a quello che il vento e la pioggia hanno lasciato per strada.' }
                    ]
                }
            ],
            endMsg: 'Hai superato il temporale senza un graffio! Ricorda: durante i fulmini, mai sotto gli alberi, cerca un edificio chiuso.'
        },
        {
            id: 'fumo', title: 'Fumo in casa', icon: '\uD83D\uDD25',
            steps: [
                {
                    text: 'Sei nella tua camera e senti un odore strano. Vai in corridoio e vedi del fumo uscire dalla porta della cucina. Cosa fai?',
                    choices: [
                        { text: 'Apro la porta della cucina per vedere cosa succede', correct: false, tip: 'Non aprire mai una porta se esce fumo! L\'aria potrebbe alimentare le fiamme.' },
                        { text: 'Chiamo subito un adulto in casa e non apro la porta', correct: true, tip: 'Giusto! Avvisa subito un adulto senza aprire la porta da cui esce il fumo.' }
                    ]
                },
                {
                    text: 'La mamma ti dice di uscire di casa insieme. Il corridoio verso l\'uscita e pieno di fumo. Come ti muovi?',
                    choices: [
                        { text: 'Corro veloce attraverso il fumo per uscire prima possibile', correct: false, tip: 'Correndo respiri più fumo. Il fumo tossico e la causa principale dei problemi in un incendio!' },
                        { text: 'Mi abbasso e cammino vicino al pavimento, coprendo naso e bocca', correct: true, tip: 'Perfetto! Il fumo sale verso l\'alto, vicino al pavimento l\'aria e più pulita.' }
                    ]
                },
                {
                    text: 'Siete usciti dal palazzo. La mamma chiama i soccorsi. Quale numero compone?',
                    choices: [
                        { text: '118', correct: false, tip: 'Nel Lazio non si chiama più il 118 per le emergenze. L\'unico numero da chiamare e il 112!' },
                        { text: '112', correct: true, tip: 'Esatto! Il 112 e l\'unico numero di emergenza nel Lazio. La centrale invia subito i Vigili del Fuoco.' }
                    ]
                },
                {
                    text: 'Mentre aspettate i vigili del fuoco, ti viene in mente che hai lasciato il tablet in camera. Un vicino dice che può rientrare a prenderlo. Cosa dici?',
                    choices: [
                        { text: '"Si grazie, e nella mia camera a destra!"', correct: false, tip: 'Non si rientra mai in un edificio con un incendio in corso! Nessun oggetto vale il rischio.' },
                        { text: '"No, e pericoloso! Aspettiamo i vigili del fuoco"', correct: true, tip: 'Bravissimo! Nessun oggetto vale la vita. Solo i vigili del fuoco possono rientrare in sicurezza.' }
                    ]
                }
            ],
            endMsg: 'Hai gestito l\'incendio in modo perfetto! Ricorda: abbassati nel fumo, non rientrare mai, chiama il 112.'
        },
        {
            id: 'alluvione', title: 'Pioggia fortissima', icon: '\uD83C\uDF0A',
            steps: [
                {
                    text: 'E pomeriggio e piove molto forte da ore. La mamma guarda il telefono e dice che c\'e un\'allerta arancione per rischio alluvione. Cosa fai?',
                    choices: [
                        { text: 'Niente, tanto siamo in casa', correct: false, tip: 'L\'allerta arancione non va ignorata! Bisogna prepararsi e seguire le indicazioni.' },
                        { text: 'Chiedo alla mamma se dobbiamo salire ai piani alti e preparare le cose importanti', correct: true, tip: 'Ottimo! Con allerta arancione e bene prepararsi, salire ai piani alti e tenere pronti documenti e telefono.' }
                    ]
                },
                {
                    text: 'Guardate dalla finestra: l\'acqua in strada sta salendo. Il papà vuole scendere in garage a spostare l\'auto. Cosa gli dici?',
                    choices: [
                        { text: '"Vai, però sbrigati!"', correct: false, tip: 'Il garage e un piano interrato: l\'acqua lo riempie velocemente. E molto pericoloso scendere!' },
                        { text: '"No papà, non scendere! L\'auto si può sostituire, tu no!"', correct: true, tip: 'Giusto! Mai scendere in cantina o garage durante un\'alluvione. L\'acqua può intrappolarti.' }
                    ]
                },
                {
                    text: 'L\'acqua ha raggiunto il primo piano e state tutti al secondo. Manca la corrente. Il nonno ha sete e vuole aprire il rubinetto. Cosa dici?',
                    choices: [
                        { text: '"Certo nonno, bevi pure"', correct: false, tip: 'Durante un\'alluvione l\'acqua del rubinetto potrebbe essere contaminata. Meglio non berla!' },
                        { text: '"Aspetta nonno, usiamo le bottiglie d\'acqua. Quella del rubinetto potrebbe non essere buona"', correct: true, tip: 'Bravo! In alluvione l\'acqua potabile potrebbe essere inquinata. Usa solo acqua in bottiglia.' }
                    ]
                },
                {
                    text: 'L\'acqua ha smesso di salire e sta scendendo piano. Un amico ti scrive che sta andando in bici a vedere la situazione in centro. Ti chiede di venire. Cosa fai?',
                    choices: [
                        { text: 'Lo raggiungo, sono curioso di vedere', correct: false, tip: 'Dopo un\'alluvione le strade possono essere pericolose: tombini aperti, fango, correnti residue. Non uscire!' },
                        { text: 'Gli dico di restare a casa e aspettare che le autorita diano il via libera', correct: true, tip: 'Perfetto! Dopo l\'alluvione si esce solo quando le autorita confermano che e sicuro.' }
                    ]
                }
            ],
            endMsg: 'Hai protetto la tua famiglia durante l\'alluvione! Ricorda: mai scendere ai piani bassi, non bere l\'acqua del rubinetto, aspetta il via libera.'
        },
        {
            id: 'incendio-bosco', title: 'Fumo nel bosco', icon: '\uD83C\uDF32',
            steps: [
                {
                    text: 'Sei in gita scolastica al parco dei Castelli Romani. Senti puzza di bruciato e vedi una colonna di fumo bianco dietro gli alberi, a circa 200 metri. Cosa fai per primo?',
                    choices: [
                        { text: 'Mi avvicino a vedere che succede', correct: false, tip: 'Mai avvicinarsi al fumo in un bosco! Il fuoco può correre velocissimo e cambiare direzione col vento.' },
                        { text: 'Avviso subito la maestra o un adulto', correct: true, tip: 'Giusto! La prima cosa è segnalare agli adulti, che valuteranno e chiameranno il 112.' }
                    ]
                },
                {
                    text: 'La maestra chiama il 112. Mentre parla, ti chiede: "In che parte del parco siamo?". Guardi intorno. Cosa le dici?',
                    choices: [
                        { text: '"Non lo so, sei tu l\'adulta!"', correct: false, tip: 'Anche tu puoi aiutare. Osserva i cartelli, il sentiero, i riferimenti del parco.' },
                        { text: 'Le leggo il cartello del sentiero e le indico dove sta il fumo rispetto a noi', correct: true, tip: 'Perfetto! Le informazioni precise aiutano i soccorsi a trovarvi e a capire dov’è l’incendio.' }
                    ]
                },
                {
                    text: 'La maestra dice di allontanarsi dal fumo. Il vento soffia dalla parte del fumo verso di voi. In che direzione vi muovete?',
                    choices: [
                        { text: 'Contro vento, verso la fonte del fumo', correct: false, tip: 'Mai andare contro il fumo! L’aria calda e i gas sono pericolosi.' },
                        { text: 'Ci spostiamo sopravento o di lato, dove il vento ci dà le spalle', correct: true, tip: 'Bravo! Così il vento allontana il fumo da te, e le fiamme non avanzano nella tua direzione.' }
                    ]
                },
                {
                    text: 'Siete al sicuro sulla strada asfaltata. Un compagno vuole filmare il fumo col telefono e postarlo sui social. Cosa gli dici?',
                    choices: [
                        { text: '"Dai fai una bella foto, la mettiamo sul gruppo"', correct: false, tip: 'Non è il momento di distrarsi. E diffondere immagini può creare panico prima che le autorità abbiano verificato.' },
                        { text: '"Lascia stare il telefono, concentriamoci su metterci in sicurezza"', correct: true, tip: 'Giusto! Il telefono serve per chiamare il 112 o i genitori, non per fare video.' }
                    ]
                }
            ],
            endMsg: 'Hai segnalato un possibile incendio boschivo come un volontario esperto! Ricorda: non avvicinarti, chiama il 112, spostati sopravento.'
        },
        {
            id: 'blackout', title: 'Va via la corrente', icon: '\uD83D\uDCA1',
            steps: [
                {
                    text: 'È sera e stai facendo i compiti. Improvvisamente si spengono le luci e il Wi-Fi. Tutto il quartiere è al buio. Cosa fai?',
                    choices: [
                        { text: 'Uso la torcia del telefono per cercare una candela e l’accendo', correct: false, tip: 'Le candele possono provocare incendi! Meglio usare solo torce elettriche o lampade a batteria.' },
                        { text: 'Accendo la torcia del telefono e chiamo un genitore', correct: true, tip: 'Giusto! Le torce a batteria sono sicure. Durante un blackout le candele sono rischiose.' }
                    ]
                },
                {
                    text: 'La mamma dice che il frigorifero non funziona. Vuoi aprirlo per prendere un succo di frutta. Cosa è meglio fare?',
                    choices: [
                        { text: 'Lo apro, tanto c’è sempre stato freddo', correct: false, tip: 'Ogni volta che apri il frigo senza corrente, il freddo si disperde e il cibo si rovina prima.' },
                        { text: 'Lo apro il meno possibile, solo per lo stretto necessario', correct: true, tip: 'Bravo! Tenere il frigo chiuso aiuta a conservare il cibo più a lungo durante un blackout.' }
                    ]
                },
                {
                    text: 'Il blackout dura da 3 ore. Fa freddo. Il papà pensa di accendere un fornelletto a gas in salotto per scaldare. Cosa gli dici?',
                    choices: [
                        { text: '"Sì buona idea, così ci scaldiamo"', correct: false, tip: 'I fornelletti a gas in casa producono monossido di carbonio, un gas velenoso e senza odore. Mai in ambiente chiuso.' },
                        { text: '"No papà, è pericoloso! Mettiamoci coperte e stiamo tutti in una stanza"', correct: true, tip: 'Giusto! Il monossido di carbonio può essere mortale. Per scaldarsi si usano coperte o si va tutti in una stanza piccola.' }
                    ]
                },
                {
                    text: 'La corrente torna dopo 5 ore. Cosa controlli per prima cosa?',
                    choices: [
                        { text: 'Accendo tutto subito: TV, PC, lavatrice', correct: false, tip: 'Accendere tutto insieme sovraccarica l’impianto. Meglio riaccendere un elettrodomestico alla volta.' },
                        { text: 'Accendo un apparecchio alla volta e controllo che il frigo funzioni', correct: true, tip: 'Bravo! Meno sovraccarico, meno rischio di far scattare di nuovo il contatore.' }
                    ]
                }
            ],
            endMsg: 'Hai gestito il blackout con calma e buon senso! Ricorda: torce a batteria (no candele), frigo chiuso, mai fornelletti in casa.'
        },
        {
            id: 'neve-ghiaccio', title: 'Neve e ghiaccio', icon: '\u2744\uFE0F',
            steps: [
                {
                    text: 'Al mattino ti alzi e vedi tutto bianco: è nevicato. La mamma deve andare al lavoro in auto. Cosa le suggerisci?',
                    choices: [
                        { text: '"Prendi subito la macchina, vai piano"', correct: false, tip: 'Prima bisogna pulire i vetri, controllare le gomme e vedere se davvero serve uscire. Piano non basta.' },
                        { text: '"Controlla i vetri, le gomme da neve o le catene, e se proprio devi uscire, parti pulita"', correct: true, tip: 'Bravo! Con la neve l’auto va preparata. Se non serve davvero, meglio rimandare o usare mezzi pubblici.' }
                    ]
                },
                {
                    text: 'Vai a scuola a piedi. Il marciapiede è ghiacciato. Come cammini?',
                    choices: [
                        { text: 'Cammino normale, con le mani in tasca per non avere freddo', correct: false, tip: 'Con le mani in tasca se scivoli non riesci a proteggerti. Tienile fuori!' },
                        { text: 'A passi corti, con le mani libere, scarpe con suola ruvida', correct: true, tip: 'Giusto! Passi corti e mani libere ti fanno mantenere l’equilibrio e, se cadi, puoi proteggerti meglio.' }
                    ]
                },
                {
                    text: 'Davanti alla scuola c’è una lastra di ghiaccio nera, quasi invisibile ("ghiaccio nero"). Un compagno corre e sta per scivolarci sopra. Cosa fai?',
                    choices: [
                        { text: 'Lo guardo e rido', correct: false, tip: 'Cadere sul ghiaccio fa male sul serio. Meglio prevenire che curare.' },
                        { text: 'Gli urlo "Attento al ghiaccio!" e gli indico dove passare', correct: true, tip: 'Bravo! Avvisare un amico è fare prevenzione, come un piccolo volontario.' }
                    ]
                },
                {
                    text: 'A scuola vi dicono che la neve continuerà e l’uscita potrebbe essere anticipata. La maestra chiede alla classe cosa è utile fare. Cosa proponi?',
                    choices: [
                        { text: 'Niente, tanto ci pensano i grandi', correct: false, tip: 'Anche tu puoi contribuire, con piccoli gesti utili e responsabili.' },
                        { text: 'Aiuto a tenere pulite le vie di fuga, avviso i compagni e mi vesto pronto', correct: true, tip: 'Perfetto! Ordine, comunicazione e attrezzatura sono i tre pilastri della protezione civile.' }
                    ]
                }
            ],
            endMsg: 'Hai affrontato neve e ghiaccio con la testa giusta! Ricorda: passi corti, auto preparata, avvisare gli altri.'
        },
        {
            id: 'persona-smarrita', title: 'Un nonno si è perso', icon: '\uD83E\uDDD3',
            steps: [
                {
                    text: 'In pizzeria con i genitori vedi un signore anziano da solo, confuso, che chiede "Dov’è casa mia?". Cosa fai?',
                    choices: [
                        { text: 'Lo ignoro, non sono affari miei', correct: false, tip: 'Un anziano confuso può essere in pericolo. Non ignorare mai chi chiede aiuto.' },
                        { text: 'Lo dico subito ai miei genitori e al gestore del locale', correct: true, tip: 'Bravo! La prima cosa è coinvolgere gli adulti. Il gestore può controllare le telecamere e chiamare aiuto.' }
                    ]
                },
                {
                    text: 'Il signore si chiama Luigi ma non ricorda l’indirizzo. I tuoi genitori chiamano il 112. L’operatore chiede una descrizione. Cosa è utile dire?',
                    choices: [
                        { text: '"È un signore vecchio"', correct: false, tip: 'Serve una descrizione precisa: altezza, capelli, vestiti, se porta occhiali o bastone.' },
                        { text: '"Si chiama Luigi, è alto circa 1,70 m, capelli bianchi, giacca grigia, senza cappello"', correct: true, tip: 'Perfetto! Una descrizione precisa aiuta chi lo sta cercando a riconoscerlo subito.' }
                    ]
                },
                {
                    text: 'Mentre aspettate, Luigi vuole uscire dalla pizzeria e andare "a cercare casa da solo". Cosa fai?',
                    choices: [
                        { text: 'Lo lascio andare, ha detto che conosce la strada', correct: false, tip: 'Se è confuso non deve uscire da solo. In strada potrebbe perdersi ancora di più.' },
                        { text: 'Gli parlo con calma, gli offro dell’acqua e lo convinco ad aspettare con noi', correct: true, tip: 'Bravo! Parlare con calma ai confusi li rassicura. Offrire acqua o un posto a sedere aiuta a guadagnare tempo.' }
                    ]
                },
                {
                    text: 'Arriva la polizia chiamata dal 112. Un agente ti chiede cosa hai visto. Cosa fai?',
                    choices: [
                        { text: 'Mi nascondo, non voglio parlare', correct: false, tip: 'La tua testimonianza è utile. Puoi parlare con un adulto accanto a te.' },
                        { text: 'Racconto con calma cosa ho visto, restando accanto ai miei genitori', correct: true, tip: 'Bravissimo! Sei stato un piccolo cittadino attivo. Anche tu hai contribuito a far ritrovare la famiglia di Luigi.' }
                    ]
                }
            ],
            endMsg: 'Hai aiutato una persona fragile con intelligenza e gentilezza! Ricorda: chiama il 112, dai descrizioni precise, resta con chi si è perso.'
        }
    ];

    let currentScenario, stepIndex, errors, consecutiveErrors;
    // Punti chiave per il "Pausa per riflettere" box che appare dopo 2 errori
    // consecutivi: aiuta il bambino a fermarsi e ripensare alle regole base
    // dello scenario, prima di continuare a sbagliare.
    const PAUSA_PUNTI = {
      terremoto: ['Sotto un tavolo robusto', 'Lontano dalle finestre', 'Mai correre durante la scossa', 'Mai usare l\'ascensore'],
      incendio: ['Esci subito senza tornare indietro', 'Mai usare l\'ascensore', 'Copri naso e bocca con un panno', 'Chiama il 112'],
      alluvione: ['Sali ai piani alti', 'Mai entrare in cantina o garage', 'Mai attraversare sottopassi allagati', 'Chiudi acqua, gas, luce'],
      temporale: ['Stai in casa, lontano da finestre', 'Niente cellulari sotto carica', 'Niente doccia o lavandino', 'Aspetta che passi'],
      fuga_gas: ['Apri tutte le finestre', 'Chiudi il rubinetto del gas', 'Niente fiamme né interruttori', 'Esci e chiama il 112'],
      smarrimento: ['Resta dove sei', 'Cerca un adulto in divisa', 'Non seguire sconosciuti', 'Memorizza nome e telefono di un adulto'],
      bullismo: ['Parla con un adulto di fiducia', 'Non rispondere con violenza', 'Salva le prove (screenshot)', 'Chiedi aiuto: non sei solo'],
      maltempo_scuola: ['Segui le indicazioni dei docenti', 'Resta nei corridoi sicuri', 'Mai aprire le finestre', 'Aspetta che passi']
    };

    function renderScenarioList() {
        selectScreen.classList.remove('hide');
        storyScreen.classList.add('hide');
        endScreen.classList.add('hide');
        scenarioList.innerHTML = '';
        scenarios.forEach(sc => {
            const col = document.createElement('div');
            col.className = 'col-6 col-md-3';
            col.innerHTML = '<div class="scenario-card" role="button" tabindex="0" aria-label="' + sc.title + '"><span class="sc-icon">' + sc.icon + '</span><span class="sc-title">' + sc.title + '</span></div>';
            col.querySelector('.scenario-card').addEventListener('click', () => startScenario(sc));
            scenarioList.appendChild(col);
        });
    }

    function startScenario(sc) {
        currentScenario = sc;
        stepIndex = 0;
        errors = 0;
        consecutiveErrors = 0;
        selectScreen.classList.add('hide');
        storyScreen.classList.remove('hide');
        scenarioBadge.textContent = sc.title;
        showStep();
    }

    function showStep() {
        const step = currentScenario.steps[stepIndex];
        stepNum.textContent = (stepIndex + 1) + ' / ' + currentScenario.steps.length;
        storyText.textContent = step.text;
        storyCard.style.animation = 'none';
        storyCard.offsetHeight;
        storyCard.style.animation = '';
        storyFeedback.classList.add('hide');
        choicesContainer.innerHTML = '';
        if (window.GameCoach && window.GameCoach.clearHint) { window.GameCoach.clearHint(); }
        step.choices.forEach(ch => {
            const btn = document.createElement('button');
            btn.className = 'choice-btn';
            btn.textContent = ch.text;
            btn.addEventListener('click', () => handleChoice(btn, ch, step));
            choicesContainer.appendChild(btn);
        });
    }

    // Mappa scenario → pagina teoria del sito
    const TEORIA_SCENARIO = {
        'terremoto':       { url: '/rischi-prevenzione/rischio-sismico/',       titolo: 'rischio sismico' },
        'temporale':       { url: '/rischi-prevenzione/temporali-intensi/',     titolo: 'temporali intensi' },
        'fumo':            { url: '/rischi-prevenzione/rischio-incendio/',      titolo: 'rischio incendio' },
        'alluvione':       { url: '/rischi-prevenzione/rischio-idrogeologico/', titolo: 'rischio idrogeologico' },
        'incendio-bosco':  { url: '/rischi-prevenzione/rischio-incendio/',      titolo: 'rischio incendio' },
        'blackout':        { url: '/rischi-prevenzione/blackout/',              titolo: 'blackout' },
        'neve-ghiaccio':   { url: '/rischi-prevenzione/',                       titolo: 'rischi e prevenzione' },
        'persona-smarrita':{ url: '/numeri-utili/',                             titolo: 'numeri di emergenza' }
    };

    function handleChoice(btn, choice, step) {
        const allBtns = choicesContainer.querySelectorAll('.choice-btn');
        allBtns.forEach(b => { b.disabled = true; });
        if (choice.correct) {
            btn.classList.add('right');
            storyFeedback.className = 'story-feedback correct';
            storyFeedback.innerHTML = '<strong><i class="bi bi-check-circle-fill me-1"></i> Giusto!</strong> ' + choice.tip;
            storyFeedback.classList.remove('hide');
            if (window.GameCoach && window.GameCoach.clearHint) { window.GameCoach.clearHint(); }
            consecutiveErrors = 0; // risposta giusta azzera il contatore
            setTimeout(() => {
                stepIndex++;
                if (stepIndex < currentScenario.steps.length) { showStep(); }
                else { showEnd(); }
            }, 2200);
        } else {
            btn.classList.add('wrong-choice');
            errors++;
            consecutiveErrors++;
            storyFeedback.className = 'story-feedback wrong';
            storyFeedback.innerHTML = '<strong><i class="bi bi-x-circle-fill me-1"></i> Non proprio...</strong> ' + choice.tip;
            storyFeedback.classList.remove('hide');
            // Layer 3: hint contestuale con link teoria in base allo scenario
            if (window.GameCoach && window.GameCoach.hint) {
                const t = TEORIA_SCENARIO[currentScenario.id] || { url: '/rischi-prevenzione/', titolo: 'rischi e prevenzione' };
                window.GameCoach.hint('Vuoi capire il perché? Leggi la pagina ' + t.titolo + ' del sito.', t.url);
            }
            setTimeout(() => {
                allBtns.forEach(b => {
                    if (!b.classList.contains('wrong-choice')) { b.disabled = false; }
                });
                storyFeedback.classList.add('hide');
                // Mini-recupero: dopo 2 errori consecutivi mostro un box
                // "Pausa per riflettere" con i punti chiave dello scenario,
                // poi azzero il contatore (cosi' non ricompare immediatamente).
                if (consecutiveErrors >= 2) {
                    mostraPausaRecupero();
                    consecutiveErrors = 0;
                }
            }, 2200);
        }
    }

    function mostraPausaRecupero() {
        const punti = PAUSA_PUNTI[currentScenario.id];
        if (!punti) return;
        const overlay = document.createElement('div');
        overlay.className = 'pausa-overlay';
        overlay.innerHTML = '<div class="pausa-box">' +
          '<h3>🌿 Pausa per riflettere</h3>' +
          '<p>Stai sbagliando un po\' di scelte. Fermati e ripensa a queste regole:</p>' +
          '<ul>' + punti.map(p => '<li>' + p + '</li>').join('') + '</ul>' +
          '<button type="button" class="btn btn-primary">Riprendo!</button>' +
          '</div>';
        document.body.appendChild(overlay);
        const closeBtn = overlay.querySelector('button');
        closeBtn.addEventListener('click', () => overlay.remove());
        closeBtn.focus();
    }

    function showEnd() {
        storyScreen.classList.add('hide');
        endScreen.classList.remove('hide');
        endMessage.textContent = currentScenario.endMsg;
        endErrors.textContent = errors;
        var totaleSteps = currentScenario.steps.length;
        var punti = Math.max(0, totaleSteps - errors);
        if (window.GiochiUtil) window.GiochiUtil.salvaEMostraAttestato('cosa-faccio-se', punti, totaleSteps, '#end-screen');
    }

    anotherBtn.addEventListener('click', renderScenarioList);
    renderScenarioList();
});
