document.addEventListener('DOMContentLoaded', function () {
    const resultsData = JSON.parse(localStorage.getItem('quizResults'));
    const candidateName = localStorage.getItem('candidateName');
    const candidateId = localStorage.getItem('candidateId');

    if (!resultsData || !candidateName) {
        window.location.href = 'index.html';
        return;
    }

    // --- POPOLAMENTO ATTESTATO ---
    document.getElementById('cert-candidate-name').textContent = candidateName;
    if(candidateId) {
        document.getElementById('cert-candidate-id').textContent = `Matricola/Ente: ${candidateId}`;
    }
    var now = new Date();
    var dateOptions = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    var dateFormatted = now.toLocaleDateString('it-IT', dateOptions);
    document.getElementById('cert-date').textContent = dateFormatted;
    var datePlaceEl = document.getElementById('cert-date-place');
    if (datePlaceEl) datePlaceEl.textContent = dateFormatted;
    document.getElementById('cert-unique-id').textContent = 'Codice verifica: ' + resultsData.uniqueId;
    
    const resultBadge = document.createElement('span');
    resultBadge.classList.add('result-badge');
    if (resultsData.passed) {
        resultBadge.classList.add('promosso');
        resultBadge.textContent = "PROMOSSO";
    } else {
        resultBadge.classList.add('bocciato');
        resultBadge.textContent = "NON IDONEO";
    }
    document.getElementById('cert-result').appendChild(resultBadge);

    const scoreText = `con un punteggio di ${resultsData.correctAnswers} risposte corrette su ${resultsData.totalQuestions} (${resultsData.score.toFixed(2)}%)`;
    document.getElementById('cert-score').textContent = scoreText;

    // --- POPOLAMENTO RIEPILOGHI ---
    document.getElementById('summary-total').textContent = resultsData.totalQuestions;
    document.getElementById('summary-correct').textContent = resultsData.correctAnswers;
    document.getElementById('summary-incorrect').textContent = resultsData.totalQuestions - resultsData.correctAnswers;
    document.getElementById('score-percentage').textContent = resultsData.score.toFixed(2);
    
    const scoreProgressBar = document.getElementById('score-progress-bar');
    scoreProgressBar.style.width = `${resultsData.score}%`;
    scoreProgressBar.setAttribute('aria-valuenow', resultsData.score);
    scoreProgressBar.textContent = `${resultsData.score.toFixed(0)}%`;
    if (resultsData.passed) {
        scoreProgressBar.classList.add('bg-success');
    } else {
        scoreProgressBar.classList.add('bg-danger');
    }

    // --- RIEPILOGO PER CATEGORIA ---
    const categorySummaryList = document.getElementById('category-summary-list');
    const categoryResults = {};

    resultsData.quizQuestions.forEach((q, index) => {
        if (!categoryResults[q.category]) {
            categoryResults[q.category] = { correct: 0, total: 0 };
        }
        categoryResults[q.category].total++;
        if (resultsData.userAnswers[index] === true) {
            categoryResults[q.category].correct++;
        }
    });

    for (const category in categoryResults) {
        const res = categoryResults[category];
        const percentage = res.total > 0 ? (res.correct / res.total) * 100 : 0;
        const item = document.createElement('div');
        item.className = 'category-summary-item mb-3';
        item.innerHTML = `
            <div class="d-flex justify-content-between">
                <strong>${category}</strong>
                <span>${res.correct} / ${res.total}</span>
            </div>
            <div class="progress" style="height: 20px; font-size: 0.9rem;">
                <div class="progress-bar ${percentage >= 75 ? 'bg-success' : 'bg-warning'}" role="progressbar" style="width: ${percentage}%;" aria-valuenow="${percentage}" aria-valuemin="0" aria-valuemax="100">${percentage.toFixed(0)}%</div>
            </div>
        `;
        categorySummaryList.appendChild(item);
    }
    
    // --- GESTIONE BOTTONI ---
    const reviewBtn = document.getElementById('reviewQuizBtn');
    const reviewContainer = document.getElementById('review-container');
    reviewBtn.addEventListener('click', () => {
        if (reviewContainer.style.display === 'none') {
            generateReview();
            reviewContainer.style.display = 'block';
            reviewBtn.textContent = 'Nascondi Revisione';
            reviewBtn.classList.remove('btn-info');
            reviewBtn.classList.add('btn-secondary');
        } else {
            reviewContainer.innerHTML = '';
            reviewContainer.style.display = 'none';
            reviewBtn.textContent = 'Rivedi il Quiz';
            reviewBtn.classList.remove('btn-secondary');
            reviewBtn.classList.add('btn-info');
        }
    });

    const shareBtn = document.getElementById('shareBtn');
    shareBtn.addEventListener('click', () => {
        const shareText = `Ho completato il quiz formativo della Protezione Civile di Genzano di Roma con ${resultsData.correctAnswers} risposte corrette su ${resultsData.totalQuestions}!`;
        if (navigator.share) {
            navigator.share({
                title: 'Risultato Quiz Protezione Civile',
                text: shareText,
                url: window.location.href
            }).catch(console.error);
        } else {
            navigator.clipboard.writeText(shareText + " " + window.location.href);
            alert("Testo del risultato copiato negli appunti!");
        }
    });
    
    function generateReview() {
        resultsData.quizQuestions.forEach((question, index) => {
            const card = document.createElement('div');
            card.className = 'card mb-4';
            
            const isCorrect = resultsData.userAnswers[index] === true;
            const isAnswered = resultsData.userAnswers[index] !== null;

            card.classList.add(isCorrect ? 'border-success' : 'border-danger');

            let headerText = `Domanda ${index + 1}`;
            if (isCorrect) {
                headerText += ' - Risposta Corretta';
            } else if (isAnswered) {
                headerText += ' - Risposta Errata';
            } else {
                headerText += ' - Senza Risposta';
            }
            
            let cardBody = `
                <div class="card-header fw-bold">${headerText}</div>
                <div class="card-body">
                    <h5 class="card-title">${question.question}</h5>
                    <p class="card-text text-muted">Categoria: ${question.category}</p>
                    <ul class="list-group">
            `;

            const shuffledAnswers = question.answers.map((ans, i) => ({ text: ans, originalIndex: i }));

            shuffledAnswers.forEach(answer => {
                const isCorrectAnswer = answer.originalIndex === question.correct;
                const isUserChoice = answer.text === resultsData.userChoices[index];

                let classList = 'list-group-item';
                if(isCorrectAnswer) classList += ' correct';
                if(isUserChoice && !isCorrectAnswer) classList += ' user-choice incorrect';
                
                cardBody += `<li class="${classList}">${answer.text}</li>`;
            });
            
            cardBody += `</ul>`;
            
            if(!isCorrect) {
                cardBody += `
                    <div class="mt-3 alert alert-info">
                        <strong>Spiegazione:</strong> ${question.explanation}
                    </div>
                `;
            }

            cardBody += `</div></div>`;
            card.innerHTML = cardBody;
            reviewContainer.appendChild(card);
        });
    }
});