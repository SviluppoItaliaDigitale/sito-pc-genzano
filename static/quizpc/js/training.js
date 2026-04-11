document.addEventListener('DOMContentLoaded', function () {
    const selectedCategoriesJSON = localStorage.getItem('trainingCategories');

    // Se non ci sono categorie selezionate, torna alla pagina di configurazione
    if (!selectedCategoriesJSON) {
        window.location.href = 'start_training.html';
        return;
    }

    let trainingQuestions = [];
    let currentQuestionIndex = 0;
    let correctCount = 0;
    let wrongCount = 0;
    const correctBadge = document.getElementById('training-correct');
    const wrongBadge = document.getElementById('training-wrong');

    // Selezione degli elementi dall'HTML
    const totalQuestionsEl = document.getElementById('total-questions');
    const questionNumberEl = document.getElementById('question-number');
    const questionCategoryEl = document.getElementById('question-category');
    const questionTextEl = document.getElementById('question-text');
    const answersContainerEl = document.getElementById('answers-container');
    const nextBtn = document.getElementById('next-btn');
    const questionWrapper = document.getElementById('question-animation-wrapper');
    const explanationBox = document.getElementById('explanation-box');

    // Funzione per mescolare un array
    function shuffle(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    // Funzione per avviare l'allenamento
    function startTraining() {
        const selectedCategories = JSON.parse(selectedCategoriesJSON);
        
        const availableQuestions = FULL_QUESTION_BANK.filter(q => selectedCategories.includes(q.category));
        
        if (availableQuestions.length === 0) {
            alert("Errore: Non sono state trovate domande per le categorie selezionate.");
            window.location.href = 'start_training.html';
            return;
        }

        trainingQuestions = shuffle([...availableQuestions]);
        totalQuestionsEl.textContent = trainingQuestions.length;
        correctCount = 0;
        wrongCount = 0;
        if (correctBadge) correctBadge.textContent = '0 ✓';
        if (wrongBadge) wrongBadge.textContent = '0 ✗';

        loadQuestion(currentQuestionIndex);
    }

    // Funzione per caricare una domanda
    function loadQuestion(index) {
        questionWrapper.classList.remove('question-fade-in');
        questionWrapper.classList.add('question-fade-out');
        
        setTimeout(() => {
            const questionData = trainingQuestions[index];
            questionNumberEl.textContent = index + 1;
            questionCategoryEl.textContent = `Categoria: ${questionData.category}`;
            questionTextEl.textContent = questionData.question;
            
            // Resetta l'interfaccia per la nuova domanda
            answersContainerEl.innerHTML = '';
            answersContainerEl.classList.remove('answered');
            explanationBox.style.display = 'none';
            explanationBox.innerHTML = '';
            nextBtn.style.display = 'none';
            
            const displayAnswers = shuffle(questionData.answers.map((answer, i) => ({ text: answer, isCorrect: i === questionData.correct })));
            
            displayAnswers.forEach(answerObj => {
                const answerEl = document.createElement('a');
                answerEl.href = '#';
                answerEl.classList.add('list-group-item', 'list-group-item-action');
                answerEl.innerHTML = `<span>${answerObj.text}</span>`;
                answerEl.dataset.isCorrect = answerObj.isCorrect;
                answerEl.addEventListener('click', handleAnswerClick);
                answersContainerEl.appendChild(answerEl);
            });
            
            questionWrapper.classList.remove('question-fade-out');
            questionWrapper.classList.add('question-fade-in');
        }, 400);
    }

    // Funzione per gestire il click sulla risposta (CUORE DELLA MODALITÀ)
    function handleAnswerClick(e) {
        e.preventDefault();
        
        // Impedisce di cliccare più volte
        if (answersContainerEl.classList.contains('answered')) {
            return;
        }
        answersContainerEl.classList.add('answered');
        
        const selectedAnswer = e.currentTarget;
        const wasCorrect = selectedAnswer.dataset.isCorrect === 'true';

        // 1. Fornisce il feedback visivo immediato
        Array.from(answersContainerEl.children).forEach(child => {
            if (child.dataset.isCorrect === 'true') {
                child.classList.add('correct'); // Evidenzia in verde la risposta giusta
            }
        });
        
        if (wasCorrect) {
            correctCount++;
            if (correctBadge) correctBadge.textContent = correctCount + ' ✓';
        } else {
            selectedAnswer.classList.add('incorrect');
            wrongCount++;
            if (wrongBadge) wrongBadge.textContent = wrongCount + ' ✗';
        }

        // 2. Mostra la spiegazione
        const questionData = trainingQuestions[currentQuestionIndex];
        explanationBox.innerHTML = `<div class="alert alert-info mt-3"><strong>Spiegazione:</strong> ${questionData.explanation}</div>`;
        explanationBox.style.display = 'block';

        // 3. Mostra il pulsante per proseguire
        if (currentQuestionIndex < trainingQuestions.length - 1) {
            nextBtn.textContent = 'Prossima Domanda';
        } else {
            nextBtn.textContent = 'Ricomincia Allenamento';
        }
        nextBtn.style.display = 'block';
    }

    // Logica del pulsante "Prossima"
    nextBtn.addEventListener('click', () => {
        if (currentQuestionIndex < trainingQuestions.length - 1) {
            currentQuestionIndex++;
            loadQuestion(currentQuestionIndex);
        } else {
            // Se è l'ultima domanda, mostra messaggio e ricomincia
            explanationBox.innerHTML = '<div class="alert alert-success mt-3"><strong>Complimenti!</strong> Hai completato tutte le domande per queste categorie. L\'allenamento verrà ricaricato.</div>';
            explanationBox.style.display = 'block';
            currentQuestionIndex = 0;
            setTimeout(function() { startTraining(); }, 2000);
        }
    });

    // Avvia l'allenamento al caricamento della pagina
    startTraining();
});