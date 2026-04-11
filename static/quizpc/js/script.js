// A4: Modale Bootstrap per conferma (sostituisce confirm())
function showConfirmModal(message, onConfirm) {
    var modalEl = document.getElementById('confirmModal');
    var bodyEl = document.getElementById('confirmModalBody');
    var actionBtn = document.getElementById('confirmModalAction');
    bodyEl.textContent = message;
    var modal = new bootstrap.Modal(modalEl);
    var handler = function() {
        actionBtn.removeEventListener('click', handler);
        modal.hide();
        onConfirm();
    };
    actionBtn.addEventListener('click', handler);
    modal.show();
}

function confirmExit(event, url) {
    event.preventDefault();
    showConfirmModal("Sei sicuro di voler abbandonare il quiz? I tuoi progressi andranno persi.", function() {
        localStorage.removeItem('quizResults');
        localStorage.removeItem('selectedCategories');
        window.location.href = url;
    });
}

document.addEventListener('DOMContentLoaded', function () {
    var MAX_QUIZ_LENGTH = 60;
    var QUIZ_DURATION_MINUTES = 45;

    var candidateName = localStorage.getItem('candidateName');
    var selectedCategoriesJSON = localStorage.getItem('selectedCategories');

    if (!candidateName || !selectedCategoriesJSON) {
        window.location.href = 'start_quiz.html';
        return;
    }

    var timerInterval;
    var quizQuestions = [];
    var userAnswers = [];
    var userChoices = [];
    var currentQuestionIndex = 0;
    var isTransitioning = false;

    var totalQuestionsEl = document.getElementById('total-questions');
    var questionNumberEl = document.getElementById('question-number');
    var questionCategoryEl = document.getElementById('question-category');
    var questionTextEl = document.getElementById('question-text');
    var answersContainerEl = document.getElementById('answers-container');
    var progressBarEl = document.getElementById('progress-bar');
    var finishBtn = document.getElementById('finish-btn');
    var questionWrapper = document.getElementById('question-animation-wrapper');
    var exitBtn = document.getElementById('exitBtn');

    if (exitBtn) {
        exitBtn.addEventListener('click', function(e) {
            confirmExit(e, 'start_quiz.html');
        });
    }

    function shuffle(array) {
        for (var i = array.length - 1; i > 0; i--) {
            var j = Math.floor(Math.random() * (i + 1));
            var tmp = array[i]; array[i] = array[j]; array[j] = tmp;
        }
        return array;
    }

    function startQuiz() {
        var selectedCategories = JSON.parse(selectedCategoriesJSON);

        if (!selectedCategories || selectedCategories.length === 0) {
            window.location.href = 'start_quiz.html';
            return;
        }

        var availableQuestions = FULL_QUESTION_BANK.filter(function(q) {
            return selectedCategories.indexOf(q.category) !== -1;
        });

        if (availableQuestions.length === 0) {
            window.location.href = 'start_quiz.html';
            return;
        }

        var quizLength = Math.min(availableQuestions.length, MAX_QUIZ_LENGTH);
        quizQuestions = shuffle(availableQuestions.slice()).slice(0, quizLength);
        userAnswers = new Array(quizQuestions.length).fill(null);
        userChoices = new Array(quizQuestions.length).fill(null);

        questionNumberEl.textContent = 1;
        totalQuestionsEl.textContent = quizQuestions.length;

        loadQuestion(currentQuestionIndex);
        startTimer(QUIZ_DURATION_MINUTES * 60);
        updateProgressBar();
    }

    function startTimer(duration) {
        var timer = duration;
        var timerEl = document.getElementById('timer');
        timerInterval = setInterval(function () {
            var minutes = parseInt(timer / 60, 10);
            var seconds = parseInt(timer % 60, 10);
            timerEl.textContent = (minutes < 10 ? '0' : '') + minutes + ':' + (seconds < 10 ? '0' : '') + seconds;
            if (--timer < 0) {
                clearInterval(timerInterval);
                endQuiz();
            }
        }, 1000);
    }

    function loadQuestion(index) {
        isTransitioning = true;
        questionWrapper.classList.remove('question-fade-in');
        questionWrapper.classList.add('question-fade-out');

        setTimeout(function() {
            var questionData = quizQuestions[index];
            questionNumberEl.textContent = index + 1;
            questionCategoryEl.textContent = 'Categoria: ' + questionData.category;
            questionTextEl.textContent = questionData.question;
            answersContainerEl.innerHTML = '';
            answersContainerEl.classList.remove('answered');

            var answersToShuffle = questionData.answers.map(function(answer, i) {
                return { text: answer, isCorrect: i === questionData.correct };
            });
            var displayAnswers = shuffle(answersToShuffle);

            displayAnswers.forEach(function(answerObj) {
                var answerEl = document.createElement('a');
                answerEl.href = '#';
                answerEl.classList.add('list-group-item', 'list-group-item-action');
                answerEl.setAttribute('role', 'option');
                answerEl.innerHTML = '<span>' + answerObj.text + '</span>';
                answerEl.dataset.isCorrect = answerObj.isCorrect;
                answerEl.addEventListener('click', handleAnswerClick);
                answersContainerEl.appendChild(answerEl);
            });

            updateProgressBar();
            questionWrapper.classList.remove('question-fade-out');
            questionWrapper.classList.add('question-fade-in');

            setTimeout(function() { isTransitioning = false; }, 50);
        }, 400);
    }

    function handleAnswerClick(e) {
        e.preventDefault();

        if (answersContainerEl.classList.contains('answered') || isTransitioning) return;

        answersContainerEl.classList.add('answered');
        isTransitioning = true;

        var selectedAnswer = e.currentTarget;
        var wasCorrect = selectedAnswer.dataset.isCorrect === 'true';

        userAnswers[currentQuestionIndex] = wasCorrect;
        userChoices[currentQuestionIndex] = selectedAnswer.querySelector('span').textContent;

        selectedAnswer.classList.add('answered-selected');

        setTimeout(function() {
            if (currentQuestionIndex < quizQuestions.length - 1) {
                currentQuestionIndex++;
                loadQuestion(currentQuestionIndex);
            } else {
                endQuiz();
            }
        }, 400);
    }

    function endQuiz() {
        clearInterval(timerInterval);
        window.removeEventListener('beforeunload', beforeUnloadHandler);

        var correctAnswers = userAnswers.filter(function(a) { return a === true; }).length;
        var totalQuestionsInQuiz = quizQuestions.length;
        var passMark = Math.ceil(totalQuestionsInQuiz * 0.75);
        var pass = (correctAnswers >= passMark);

        var now = new Date();
        var dateStr = now.getFullYear().toString() + String(now.getMonth() + 1).padStart(2, '0') + String(now.getDate()).padStart(2, '0');
        var timeStr = String(now.getHours()).padStart(2, '0') + String(now.getMinutes()).padStart(2, '0');
        var nameInitials = (localStorage.getItem('candidateName') || 'XX').split(' ').map(function(n) { return n[0]; }).join('').toUpperCase();
        var uniqueId = 'PCGZ-' + dateStr + '-' + timeStr + '-' + nameInitials + '-' + correctAnswers;

        var results = {
            uniqueId: uniqueId,
            totalQuestions: totalQuestionsInQuiz,
            correctAnswers: correctAnswers,
            answeredCount: userAnswers.filter(function(a) { return a !== null; }).length,
            score: totalQuestionsInQuiz > 0 ? (correctAnswers / totalQuestionsInQuiz) * 100 : 0,
            passed: pass,
            quizQuestions: quizQuestions,
            userAnswers: userAnswers,
            userChoices: userChoices
        };

        localStorage.setItem('quizResults', JSON.stringify(results));
        window.location.href = 'results.html';
    }

    function updateProgressBar() {
        var progress = (currentQuestionIndex / quizQuestions.length) * 100;
        progressBarEl.style.width = progress + '%';
    }

    finishBtn.addEventListener('click', function() {
        var unanswered = userAnswers.filter(function(a) { return a === null; }).length;
        var confirmMsg = unanswered > 0
            ? 'Hai ancora ' + unanswered + ' domande senza risposta. Terminare il quiz?'
            : 'Terminare il quiz?';
        showConfirmModal(confirmMsg, endQuiz);
    });

    var beforeUnloadHandler = function(event) { event.preventDefault(); event.returnValue = ''; };
    window.addEventListener('beforeunload', beforeUnloadHandler);

    startQuiz();
});
