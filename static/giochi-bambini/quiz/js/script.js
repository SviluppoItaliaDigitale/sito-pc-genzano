document.addEventListener('DOMContentLoaded', () => {
    const startScreen = document.getElementById('start-screen');
    const quizScreen = document.getElementById('quiz-screen');
    const resultsScreen = document.getElementById('results-screen');
    const startButton = document.getElementById('start-btn');
    const restartButton = document.getElementById('restart-btn');
    const questionElement = document.getElementById('question');
    const answerButtonsElement = document.getElementById('answer-buttons');
    const scoreElement = document.getElementById('score');
    const totalQuestionsElement = document.getElementById('total-questions');
    const feedbackMessageElement = document.getElementById('feedback-message');
    const feedbackBox = document.getElementById('feedback-box');
    const progressFill = document.getElementById('progress-fill');
    const currentQSpan = document.getElementById('current-q');
    const totalQSpan = document.getElementById('total-q');
    const scoreLive = document.getElementById('score-live');

    let shuffledQuestions, currentQuestionIndex, score, selectedCount;

    // B2: Question count selector
    const countButtons = document.querySelectorAll('.question-count-selector .btn');
    selectedCount = 'all';
    countButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            countButtons.forEach(b => { b.classList.remove('active'); b.setAttribute('aria-checked', 'false'); });
            btn.classList.add('active');
            btn.setAttribute('aria-checked', 'true');
            selectedCount = btn.dataset.count;
        });
    });

    const questions = [
        // Terremoto
        {
            question: 'Cosa fai se senti una scossa di terremoto mentre sei in casa?',
            answers: [
                { text: 'Corro fuori in strada', correct: false },
                { text: 'Mi riparo sotto un tavolo robusto', correct: true },
                { text: 'Uso l\'ascensore per scendere', correct: false },
                { text: 'Mi affaccio alla finestra per vedere cosa succede', correct: false }
            ],
            explanation: 'Sotto un tavolo robusto sei protetto dalla caduta di oggetti. Non usare mai l\'ascensore durante un terremoto!'
        },
        {
            question: 'Dopo una scossa di terremoto, quale uscita devi usare?',
            answers: [
                { text: 'L\'ascensore, per fare in fretta', correct: false },
                { text: 'La finestra al piano terra', correct: false },
                { text: 'Le scale, con calma e senza correre', correct: true },
                { text: 'Resto sempre dentro casa', correct: false }
            ],
            explanation: 'Le scale sono la via di uscita più sicura. L\'ascensore potrebbe bloccarsi e la fretta può causare cadute.'
        },
        {
            question: 'Durante un terremoto a scuola, cosa fai?',
            answers: [
                { text: 'Scappo subito fuori dall\'aula', correct: false },
                { text: 'Mi nascondo sotto il banco e proteggo la testa', correct: true },
                { text: 'Mi metto vicino alla finestra', correct: false },
                { text: 'Chiamo i miei genitori al telefono', correct: false }
            ],
            explanation: 'Sotto il banco sei protetto da quello che può cadere. Le finestre possono rompersi, stai lontano!'
        },
        // Incendio
        {
            question: 'Se vedi un incendio in un bosco, cosa fai?',
            answers: [
                { text: 'Cerco di spegnerlo da solo', correct: false },
                { text: 'Chiamo subito il 112 o il 115', correct: true },
                { text: 'Faccio un video da postare', correct: false },
                { text: 'Non faccio niente, passerà da solo', correct: false }
            ],
            explanation: 'Mai provare a spegnere un incendio da solo! Chiama subito il 112 e allontanati dal fuoco.'
        },
        {
            question: 'In caso di incendio in un edificio, cosa NON devi fare?',
            answers: [
                { text: 'Camminare carponi vicino al pavimento', correct: false },
                { text: 'Usare l\'ascensore per scendere più veloce', correct: true },
                { text: 'Coprirmi naso e bocca con un panno bagnato', correct: false },
                { text: 'Seguire le indicazioni dell\'insegnante', correct: false }
            ],
            explanation: 'L\'ascensore può bloccarsi e riempirsi di fumo. Usa sempre le scale e copri naso e bocca.'
        },
        {
            question: 'Perché durante un incendio bisogna stare bassi vicino al pavimento?',
            answers: [
                { text: 'Perché il pavimento è più fresco', correct: false },
                { text: 'Perché il fumo caldo sale verso l\'alto e in basso si respira meglio', correct: true },
                { text: 'Per non farsi vedere dalle fiamme', correct: false },
                { text: 'Perché è più facile correre', correct: false }
            ],
            explanation: 'Il fumo tossico sale verso l\'alto. Vicino al pavimento l\'aria è più pulita e puoi respirare meglio.'
        },
        // Numeri di emergenza
        {
            question: 'Qual è il numero unico di emergenza da chiamare in Italia?',
            answers: [
                { text: '118', correct: false },
                { text: '115', correct: false },
                { text: '112', correct: true },
                { text: '113', correct: false }
            ],
            explanation: 'Il 112 è il numero unico di emergenza. Funziona per tutte le emergenze: polizia, ambulanza e vigili del fuoco.'
        },
        {
            question: 'Quando chiami il 112, cosa devi dire?',
            answers: [
                { text: 'Solo il mio nome', correct: false },
                { text: 'Cosa è successo, dove mi trovo e quante persone hanno bisogno di aiuto', correct: true },
                { text: 'Devo solo urlare "aiuto"', correct: false },
                { text: 'Non devo dire niente, loro sanno già tutto', correct: false }
            ],
            explanation: 'Quando chiami il 112, parla con calma e spiega cosa è successo, dove ti trovi e se qualcuno ha bisogno di aiuto.'
        },
        // Zaino di emergenza
        {
            question: 'Cosa non deve mancare in uno zaino di emergenza?',
            answers: [
                { text: 'Videogiochi e caricabatterie', correct: false },
                { text: 'Album di figurine', correct: false },
                { text: 'Torcia, acqua e un fischietto', correct: true },
                { text: 'Libri di scuola', correct: false }
            ],
            explanation: 'La torcia serve per vedere al buio, l\'acqua per bere e il fischietto per farti sentire dai soccorritori.'
        },
        {
            question: 'Perché nello zaino di emergenza serve un fischietto?',
            answers: [
                { text: 'Per giocare', correct: false },
                { text: 'Per farsi sentire dai soccorritori se si è bloccati', correct: true },
                { text: 'Per spaventare gli animali', correct: false },
                { text: 'Per chiamare gli amici', correct: false }
            ],
            explanation: 'Il fischietto si sente molto lontano e non ti fa stancare la voce. I soccorritori lo cercano!'
        },
        // Alluvione
        {
            question: 'Se piove molto forte e l\'acqua sale in strada, cosa fai?',
            answers: [
                { text: 'Esco a giocare con l\'acqua', correct: false },
                { text: 'Scendo in cantina a controllare', correct: false },
                { text: 'Vado ai piani alti e resto lontano dall\'acqua', correct: true },
                { text: 'Attraverso la strada allagata a piedi', correct: false }
            ],
            explanation: 'I piani alti sono il posto più sicuro. L\'acqua può essere pericolosa anche se sembra bassa!'
        },
        {
            question: 'Durante un\'alluvione, perché non bisogna scendere in cantina?',
            answers: [
                { text: 'Perché è buio', correct: false },
                { text: 'Perché l\'acqua può riempirla velocemente e restare intrappolati', correct: true },
                { text: 'Perché c\'è troppo disordine', correct: false },
                { text: 'Perché fa freddo', correct: false }
            ],
            explanation: 'La cantina è il primo posto che si riempie d\'acqua. Si rischia di restare intrappolati senza via di uscita.'
        },
        // Evacuazione scuola
        {
            question: 'Quando suona l\'allarme di evacuazione a scuola, cosa fai?',
            answers: [
                { text: 'Prendo tutte le mie cose dallo zaino', correct: false },
                { text: 'Mi metto in fila e seguo l\'insegnante verso il punto di raccolta', correct: true },
                { text: 'Corro il più veloce possibile verso l\'uscita', correct: false },
                { text: 'Aspetto che i miei genitori vengano a prendermi', correct: false }
            ],
            explanation: 'Segui l\'insegnante in fila ordinata. Non portare le cose e non correre: la calma salva la vita!'
        },
        {
            question: 'A cosa serve il punto di raccolta della scuola?',
            answers: [
                { text: 'È il posto dove si gioca durante l\'intervallo', correct: false },
                { text: 'È il luogo sicuro dove ritrovarsi per controllare che ci siano tutti', correct: true },
                { text: 'È dove si parcheggia', correct: false },
                { text: 'È il posto dove aspettare l\'autobus', correct: false }
            ],
            explanation: 'Al punto di raccolta l\'insegnante fa l\'appello per verificare che nessuno manchi. È un posto sicuro!'
        },
        // Protezione Civile
        {
            question: 'Chi sono i volontari di Protezione Civile?',
            answers: [
                { text: 'Persone che aiutano la comunità durante le emergenze, senza essere pagate', correct: true },
                { text: 'Soldati dell\'esercito', correct: false },
                { text: 'Dottori dell\'ospedale', correct: false },
                { text: 'Vigili urbani', correct: false }
            ],
            explanation: 'I volontari sono persone comuni che dedicano il loro tempo libero per aiutare gli altri durante le emergenze.'
        },
        {
            question: 'Cosa significa il colore arancione in un\'allerta meteo?',
            answers: [
                { text: 'Tutto tranquillo, nessun pericolo', correct: false },
                { text: 'Fenomeni intensi: bisogna fare molta attenzione', correct: true },
                { text: 'Si può uscire a giocare', correct: false },
                { text: 'È solo un consiglio, non è importante', correct: false }
            ],
            explanation: 'Arancione significa attenzione! Possono arrivare piogge forti o vento. Meglio restare al sicuro.'
        },
        // Sicurezza generale
        {
            question: 'Se senti odore di gas in casa, cosa fai?',
            answers: [
                { text: 'Accendo la luce per vedere meglio', correct: false },
                { text: 'Apro le finestre, esco e chiamo un adulto', correct: true },
                { text: 'Cerco da dove viene con un accendino', correct: false },
                { text: 'Non faccio niente, è normale', correct: false }
            ],
            explanation: 'Il gas è pericoloso! Non toccare interruttori e non usare fiamme. Apri le finestre e chiama subito un adulto.'
        },
        {
            question: 'Perché è importante conoscere le vie di fuga della propria scuola?',
            answers: [
                { text: 'Per correre più veloci degli altri', correct: false },
                { text: 'Per sapere dove andare in caso di emergenza, senza perdere tempo', correct: true },
                { text: 'Per uscire prima durante l\'intervallo', correct: false },
                { text: 'Non è importante, ci pensa l\'insegnante', correct: false }
            ],
            explanation: 'Se conosci la via di fuga, in emergenza sai subito dove andare. La preparazione è la migliore protezione!'
        }
    ];

    function startGame() {
        startScreen.classList.add('hide');
        resultsScreen.classList.add('hide');
        quizScreen.classList.remove('hide');

        let pool = [...questions].sort(() => Math.random() - 0.5);
        if (selectedCount !== 'all') {
            const count = parseInt(selectedCount, 10);
            pool = pool.slice(0, Math.min(count, pool.length));
        }
        shuffledQuestions = pool;
        currentQuestionIndex = 0;
        score = 0;
        totalQSpan.textContent = shuffledQuestions.length;
        updateProgress();
        setNextQuestion();
    }

    function updateProgress() {
        currentQSpan.textContent = currentQuestionIndex + 1;
        const pct = (currentQuestionIndex / shuffledQuestions.length) * 100;
        progressFill.style.width = pct + '%';
        scoreLive.textContent = score + ' corrette';
    }

    function setNextQuestion() {
        resetState();
        showQuestion(shuffledQuestions[currentQuestionIndex]);
        updateProgress();
    }

    function showQuestion(question) {
        questionElement.innerText = question.question;
        const shuffledAnswers = [...question.answers].sort(() => Math.random() - 0.5);
        shuffledAnswers.forEach(answer => {
            const button = document.createElement('button');
            button.innerText = answer.text;
            button.classList.add('btn');
            if (answer.correct) { button.dataset.correct = answer.correct; }
            button.addEventListener('click', selectAnswer);
            answerButtonsElement.appendChild(button);
        });
    }

    function selectAnswer(e) {
        const selectedButton = e.target;
        const correct = selectedButton.dataset.correct === 'true';
        const currentQ = shuffledQuestions[currentQuestionIndex];

        if (correct) { score++; }

        // Show correct/wrong on all buttons
        Array.from(answerButtonsElement.children).forEach(button => {
            setStatusClass(button, button.dataset.correct === 'true');
            button.disabled = true;
        });

        // A2: Show feedback explanation
        feedbackBox.classList.remove('hide', 'correct', 'wrong');
        if (correct) {
            feedbackBox.classList.add('correct');
            feedbackBox.innerHTML = '<div class="feedback-title">Risposta esatta!</div>' + currentQ.explanation;
        } else {
            feedbackBox.classList.add('wrong');
            feedbackBox.innerHTML = '<div class="feedback-title">Risposta sbagliata</div>' + currentQ.explanation;
        }

        // Update live score
        scoreLive.textContent = score + ' corrette';

        // Wait longer so the child can read the explanation, then advance
        setTimeout(() => {
            currentQuestionIndex++;
            if (currentQuestionIndex < shuffledQuestions.length) {
                setNextQuestion();
            } else {
                showResults();
            }
        }, 3000);
    }

    function showResults() {
        quizScreen.classList.add('hide');
        resultsScreen.classList.remove('hide');
        scoreElement.innerText = score;
        totalQuestionsElement.innerText = shuffledQuestions.length;
        const percentage = (score / shuffledQuestions.length) * 100;
        if (percentage >= 90) { feedbackMessageElement.innerText = "Fantastico! Sei un vero esperto di sicurezza!"; }
        else if (percentage >= 70) { feedbackMessageElement.innerText = "Molto bravo! Conosci bene le regole di sicurezza."; }
        else if (percentage >= 50) { feedbackMessageElement.innerText = "Non male! Riprova per imparare ancora di più."; }
        else { feedbackMessageElement.innerText = "Puoi fare di meglio! Rileggi i consigli e riprova il quiz."; }
    }

    function resetState() {
        feedbackBox.classList.add('hide');
        while (answerButtonsElement.firstChild) { answerButtonsElement.removeChild(answerButtonsElement.firstChild); }
    }

    function setStatusClass(element, correct) {
        if (correct) { element.classList.add('correct'); } else { element.classList.add('wrong'); }
    }

    startButton.addEventListener('click', startGame);
    restartButton.addEventListener('click', startGame);
});
