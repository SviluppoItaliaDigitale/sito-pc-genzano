document.addEventListener('DOMContentLoaded', () => {
    if (typeof scenarioData !== 'undefined' && scenarioData.length > 0) {
        const initialSituationContainer = document.getElementById('initial-situation-container');
        if(initialSituationContainer) {
            initialSituationContainer.innerHTML = `<p class="lead mb-0">${scenarioData[0].situation_update}</p>`;
        }
        loadQuestion(currentQuestionIndex);
    }
});

let currentQuestionIndex = 0;

/**
 * Algoritmo di Fisher-Yates (Knuth) Shuffle
 */
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
}

// A5: Score tracking variables (accessible from all functions)
let correctAnswers = 0;
let totalAnswered = 0;

function loadQuestion(index) {
    if (index >= scenarioData.length) {
        showFinalScreen();
        return;
    }
    const scenario = scenarioData[index];

    const situationText = document.getElementById('situation-text');
    if (index > 0) {
        situationText.innerText = scenario.situation_update;
        situationText.parentElement.classList.remove('d-none');
    } else {
        situationText.parentElement.classList.add('d-none');
    }

    document.getElementById('question-text').innerText = scenario.question;

    const choicesContainer = document.getElementById('choices-container');
    choicesContainer.innerHTML = '';

    let choices = [...scenario.choices];
    shuffleArray(choices);

    choices.forEach((choice, i) => {
        const button = document.createElement('button');
        button.className = 'btn btn-outline-primary btn-lg btn-choice';
        button.innerHTML = `<strong>${String.fromCharCode(65 + i)})</strong> ${choice.text}`;
        button.onclick = () => handleChoice(choice);
        choicesContainer.appendChild(button);
    });

    const progressBar = document.getElementById('progress-bar');
    const progressPercentage = (index / (scenarioData.length - 1)) * 100;
    progressBar.style.width = `${progressPercentage}%`;

    const progressText = document.getElementById('progress-text');
    progressText.innerText = `Domanda ${index + 1} di ${scenarioData.length}`;
}

function handleChoice(selectedChoice) {
    totalAnswered++;
    if (selectedChoice.is_correct) {
        correctAnswers++;
    }

    const feedbackAlert = document.getElementById('feedback-alert');
    const feedbackTitle = document.getElementById('feedback-title');
    const feedbackText = document.getElementById('feedback-text');

    feedbackAlert.classList.remove('alert-success', 'alert-danger', 'alert-warning');
    if (selectedChoice.is_correct) {
        feedbackAlert.classList.add('alert-success');
        feedbackTitle.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-check-circle-fill me-2" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8.354 10.646a.5.5 0 0 0 .708 0l3-3a.5.5 0 0 0-.708-.708L8.5 9.293 6.854 7.646a.5.5 0 1 0-.708.708l2 2z"/></svg> RISPOSTA CORRETTA`;
    } else {
        feedbackAlert.classList.add('alert-danger');
        feedbackTitle.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="bi bi-x-circle-fill me-2" viewBox="0 0 16 16"><path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"/></svg> RISPOSTA SBAGLIATA`;
    }
    feedbackText.innerText = selectedChoice.feedback;

    document.getElementById('question-and-choices').classList.add('d-none');
    document.getElementById('feedback-container').classList.remove('d-none');

    const nextButton = document.getElementById('next-question-btn');
    if (currentQuestionIndex >= scenarioData.length - 1) {
        nextButton.innerText = 'Concludi Scenario';
        nextButton.onclick = showFinalScreen;
    } else {
        nextButton.innerText = 'Prossima Domanda';
        nextButton.onclick = nextQuestion;
    }
}

function nextQuestion() {
    currentQuestionIndex++;
    document.getElementById('feedback-container').classList.add('d-none');
    document.getElementById('question-and-choices').classList.remove('d-none');
    loadQuestion(currentQuestionIndex);
}

// B5: Detect next scenario from filename pattern
function getNextScenarioUrl() {
    const path = window.location.pathname;
    const filename = path.split('/').pop();
    // Match pattern like terremoto_01_viabilita.html
    const match = filename.match(/^([a-z]+)_(\d+)_/);
    if (!match) return null;

    const prefix = match[1];
    const currentNum = parseInt(match[2], 10);
    const nextNum = String(currentNum + 1).padStart(2, '0');

    // Try to find next scenario link on the page or construct it
    // We check if there's a link in the category page by trying a fetch
    const nextPattern = `${prefix}_${nextNum}_`;
    return { prefix, nextPattern, currentNum };
}

function showFinalScreen() {
    const scenarioContainer = document.getElementById('scenario-container');
    const scenarioTitle = document.getElementById('main-scenario-title').innerText;
    const returnLink = document.getElementById('back-to-list-link-final').href;

    // A5: Calculate score
    const scorePercent = totalAnswered > 0 ? Math.round((correctAnswers / totalAnswered) * 100) : 0;
    let scoreClass, scoreMessage;
    if (scorePercent >= 80) {
        scoreClass = 'text-success';
        scoreMessage = 'Ottimo lavoro! Hai dimostrato una solida preparazione operativa.';
    } else if (scorePercent >= 50) {
        scoreClass = 'text-warning';
        scoreMessage = 'Buon tentativo. Rivedi gli scenari in cui hai sbagliato per migliorare.';
    } else {
        scoreClass = 'text-danger';
        scoreMessage = 'Hai ancora margine di miglioramento. Riprova questo scenario per consolidare le procedure.';
    }

    // B5: Next scenario navigation
    let nextScenarioHtml = '';
    const nextInfo = getNextScenarioUrl();
    if (nextInfo) {
        // Find all links on the category page to determine if next exists
        // We use a simpler approach: check known scenario counts
        const scenarioCounts = { terremoto: 6, idro: 7, aib: 7 };
        const maxScenarios = scenarioCounts[nextInfo.prefix] || 0;
        if (nextInfo.currentNum < maxScenarios) {
            // Build next URL by scanning sibling links
            const allLinks = document.querySelectorAll('a[href]');
            let categoryPage = '';
            allLinks.forEach(a => {
                const href = a.getAttribute('href');
                if (href && (href === 'terremoto.html' || href === 'idrogeologico.html' || href === 'aib.html')) {
                    categoryPage = href;
                }
            });
            if (categoryPage) {
                nextScenarioHtml = `<a href="${categoryPage}" class="btn btn-outline-primary btn-lg mt-2"><i class="bi bi-arrow-right me-1"></i> Prossimo scenario</a>`;
            }
        }
    }

    scenarioContainer.innerHTML = `
        <div class="text-center">
            <h1 class="h3 mb-3" style="color:var(--pc-primary);font-weight:700;">${scenarioTitle}</h1>
            <p class="lead">Hai completato tutte le fasi di questo intervento.</p>
            <div class="card mx-auto mt-4 mb-4" style="max-width:400px;">
                <div class="card-body">
                    <h2 class="h4 mb-2">Il tuo punteggio</h2>
                    <p class="display-4 fw-bold ${scoreClass}">${correctAnswers}/${totalAnswered}</p>
                    <p class="text-muted">${scorePercent}% di risposte corrette</p>
                    <p class="mt-2">${scoreMessage}</p>
                </div>
            </div>
            <div class="d-flex flex-wrap justify-content-center gap-2">
                <a href="${returnLink}" class="btn btn-primary btn-lg"><i class="bi bi-list-ul me-1"></i> Torna agli scenari</a>
                ${nextScenarioHtml}
            </div>
        </div>
    `;
}
