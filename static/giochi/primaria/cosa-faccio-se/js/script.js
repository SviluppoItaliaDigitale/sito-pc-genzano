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
                        { text: 'Mi alzo e corro verso la porta per uscire', correct: false, tip: 'Durante la scossa non si corre! Le scale e i corridoi possono essere piu pericolosi.' },
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
                    text: 'Siete in fila nel corridoio. Un compagno vuole prendere l\'ascensore perche ha paura delle scale. Cosa gli dici?',
                    choices: [
                        { text: '"Hai ragione, l\'ascensore e piu veloce"', correct: false, tip: 'L\'ascensore puo bloccarsi dopo un terremoto. Non si usa mai!' },
                        { text: '"No, dopo un terremoto si usano solo le scale. Vieni con noi!"', correct: true, tip: 'Bravo! L\'ascensore puo restare bloccato. Le scale sono la via sicura.' }
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
                        { text: 'Chiedo ai miei amici di andare subito verso un edificio', correct: true, tip: 'Ottima scelta! Un edificio in muratura e il posto piu sicuro.' }
                    ]
                },
                {
                    text: 'State correndo verso casa, ma il temporale vi raggiunge. Piove fortissimo, ci sono fulmini. Vedete un gazebo in metallo e un bar con le porte aperte. Dove andate?',
                    choices: [
                        { text: 'Sotto il gazebo in metallo, e piu vicino', correct: false, tip: 'Le strutture metalliche attirano i fulmini. Meglio un edificio chiuso!' },
                        { text: 'Dentro il bar, al riparo dalle intemperie', correct: true, tip: 'Perfetto! Un edificio chiuso e il riparo migliore durante un temporale.' }
                    ]
                },
                {
                    text: 'Siete al sicuro dentro il bar. Un amico vuole chiamare la mamma con il telefono, un altro vuole stare vicino alla vetrina per guardare i fulmini. Cosa consigli?',
                    choices: [
                        { text: '"Chiamare la mamma va bene, ma restiamo lontani dalle finestre"', correct: true, tip: 'Giusto! Il telefono cellulare si puo usare, ma le finestre possono essere pericolose.' },
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
                        { text: 'Corro veloce attraverso il fumo per uscire prima possibile', correct: false, tip: 'Correndo respiri piu fumo. Il fumo tossico e la causa principale dei problemi in un incendio!' },
                        { text: 'Mi abbasso e cammino vicino al pavimento, coprendo naso e bocca', correct: true, tip: 'Perfetto! Il fumo sale verso l\'alto, vicino al pavimento l\'aria e piu pulita.' }
                    ]
                },
                {
                    text: 'Siete usciti dal palazzo. La mamma chiama i vigili del fuoco. Quale numero compone?',
                    choices: [
                        { text: '118', correct: false, tip: 'Il 118 e per le emergenze sanitarie. Per gli incendi si chiama il 115 o il 112!' },
                        { text: '115 oppure il 112', correct: true, tip: 'Esatto! Il 115 sono i Vigili del Fuoco, il 112 e il numero unico per tutte le emergenze.' }
                    ]
                },
                {
                    text: 'Mentre aspettate i vigili del fuoco, ti viene in mente che hai lasciato il tablet in camera. Un vicino dice che puo rientrare a prenderlo. Cosa dici?',
                    choices: [
                        { text: '"Si grazie, e nella mia camera a destra!"', correct: false, tip: 'Non si rientra mai in un edificio con un incendio in corso! Nessun oggetto vale il rischio.' },
                        { text: '"No, e pericoloso! Aspettiamo i vigili del fuoco"', correct: true, tip: 'Bravissimo! Nessun oggetto vale la vita. Solo i vigili del fuoco possono rientrare in sicurezza.' }
                    ]
                }
            ],
            endMsg: 'Hai gestito l\'incendio in modo perfetto! Ricorda: abbassati nel fumo, non rientrare mai, chiama il 115 o il 112.'
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
                    text: 'Guardate dalla finestra: l\'acqua in strada sta salendo. Il papa vuole scendere in garage a spostare l\'auto. Cosa gli dici?',
                    choices: [
                        { text: '"Vai, pero sbrigati!"', correct: false, tip: 'Il garage e un piano interrato: l\'acqua lo riempie velocemente. E molto pericoloso scendere!' },
                        { text: '"No papa, non scendere! L\'auto si puo sostituire, tu no!"', correct: true, tip: 'Giusto! Mai scendere in cantina o garage durante un\'alluvione. L\'acqua puo intrappolarti.' }
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
        }
    ];

    let currentScenario, stepIndex, errors;

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
        step.choices.forEach(ch => {
            const btn = document.createElement('button');
            btn.className = 'choice-btn';
            btn.textContent = ch.text;
            btn.addEventListener('click', () => handleChoice(btn, ch, step));
            choicesContainer.appendChild(btn);
        });
    }

    function handleChoice(btn, choice, step) {
        const allBtns = choicesContainer.querySelectorAll('.choice-btn');
        allBtns.forEach(b => { b.disabled = true; });
        if (choice.correct) {
            btn.classList.add('right');
            storyFeedback.className = 'story-feedback correct';
            storyFeedback.innerHTML = '<strong><i class="bi bi-check-circle-fill me-1"></i> Giusto!</strong> ' + choice.tip;
            storyFeedback.classList.remove('hide');
            setTimeout(() => {
                stepIndex++;
                if (stepIndex < currentScenario.steps.length) { showStep(); }
                else { showEnd(); }
            }, 2200);
        } else {
            btn.classList.add('wrong-choice');
            errors++;
            storyFeedback.className = 'story-feedback wrong';
            storyFeedback.innerHTML = '<strong><i class="bi bi-x-circle-fill me-1"></i> Non proprio...</strong> ' + choice.tip;
            storyFeedback.classList.remove('hide');
            setTimeout(() => {
                allBtns.forEach(b => {
                    if (!b.classList.contains('wrong-choice')) { b.disabled = false; }
                });
                storyFeedback.classList.add('hide');
            }, 2200);
        }
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
