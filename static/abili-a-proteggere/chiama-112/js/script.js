/* Chiama il 112 — Attività accessibile Abili a Proteggere */
(function () {
  'use strict';

  const TARGET = '112';
  let dialed = '';
  let currentStep = 0;

  // Conversation steps: operator asks, user picks an answer
  const conversation = [
    {
      operator: 'Pronto, 112. Qual è la tua emergenza?',
      answers: [
        { text: 'C\u2019è un incendio!', correct: true },
        { text: 'Voglio ordinare una pizza.', correct: false }
      ]
    },
    {
      operator: 'Dove ti trovi? Dimmi il tuo indirizzo o un posto che conosci.',
      answers: [
        { text: 'Sono a casa, in via Roma 10.', correct: true },
        { text: 'Non lo so e non importa.', correct: false }
      ]
    },
    {
      operator: 'Come ti chiami?',
      answers: [
        { text: 'Mi chiamo Mario.', correct: true },
        { text: 'Non voglio dirlo.', correct: false }
      ]
    },
    {
      operator: 'Ci sono altre persone con te?',
      answers: [
        { text: 'Sì, siamo in tre.', correct: true },
        { text: 'Non te lo dico.', correct: false }
      ]
    },
    {
      operator: 'Bene, i soccorsi stanno arrivando. Resta in un posto sicuro e non riattaccare. Bravo!',
      answers: null // end
    }
  ];

  // DOM
  const introScreen = document.getElementById('intro-screen');
  const phoneScreen = document.getElementById('phone-screen');
  const conversationScreen = document.getElementById('conversation-screen');
  const endScreen = document.getElementById('end-screen');
  const phoneNumber = document.getElementById('phone-number');
  const displayText = document.getElementById('display-text');
  const callBtn = document.getElementById('call-btn');
  const clearBtn = document.getElementById('clear-btn');
  const chatArea = document.getElementById('chat-area');
  const answerArea = document.getElementById('answer-area');
  const startBtn = document.getElementById('start-btn');
  const restartBtn = document.getElementById('restart-btn');

  function show(el) { el.classList.remove('hide'); }
  function hide(el) { el.classList.add('hide'); }

  // Highlight the next key to press
  function highlightNextKey() {
    document.querySelectorAll('.key-btn').forEach(function (b) {
      b.classList.remove('key-highlight');
    });
    if (dialed.length < TARGET.length) {
      var nextDigit = TARGET[dialed.length];
      var btn = document.querySelector('.key-btn[data-digit="' + nextDigit + '"]');
      if (btn) btn.classList.add('key-highlight');
    }
  }

  // Update the display
  function updateDisplay() {
    phoneNumber.textContent = dialed;
    if (dialed === TARGET) {
      displayText.textContent = 'Numero corretto! Premi il telefono verde per chiamare.';
      callBtn.disabled = false;
      document.querySelectorAll('.key-btn').forEach(function (b) {
        b.classList.remove('key-highlight');
      });
      callBtn.classList.add('key-highlight');
    } else if (dialed.length >= TARGET.length) {
      displayText.textContent = 'Numero sbagliato. Cancella e riprova!';
      callBtn.disabled = true;
    } else {
      var remaining = TARGET.length - dialed.length;
      var digits = TARGET.split('').map(function (d, i) {
        return i < dialed.length ? d : '_';
      }).join(' — ');
      displayText.textContent = 'Digita: ' + digits;
      callBtn.disabled = true;
    }
    highlightNextKey();
  }

  // Keypad click
  document.querySelectorAll('.key-btn[data-digit]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      if (dialed.length >= 3) return;
      var digit = btn.getAttribute('data-digit');
      var expected = TARGET[dialed.length];
      if (digit === expected) {
        dialed += digit;
        updateDisplay();
      } else {
        btn.classList.add('key-wrong');
        setTimeout(function () { btn.classList.remove('key-wrong'); }, 400);
      }
    });
  });

  // Clear
  clearBtn.addEventListener('click', function () {
    dialed = '';
    callBtn.disabled = true;
    callBtn.classList.remove('key-highlight');
    updateDisplay();
  });

  // Call button
  callBtn.addEventListener('click', function () {
    if (dialed !== TARGET) return;
    hide(phoneScreen);
    show(conversationScreen);
    currentStep = 0;
    chatArea.innerHTML = '';
    showConversationStep();
  });

  // Show a conversation step
  function showConversationStep() {
    var step = conversation[currentStep];
    // Operator message
    addBubble(step.operator, 'operator');

    if (!step.answers) {
      // Final step
      setTimeout(function () {
        hide(conversationScreen);
        show(endScreen);
      }, 2500);
      return;
    }

    // Show answer buttons after a short delay
    setTimeout(function () {
      answerArea.innerHTML = '';
      // Shuffle answers for variety
      var shuffled = step.answers.slice().sort(function () { return Math.random() - 0.5; });
      shuffled.forEach(function (ans) {
        var btn = document.createElement('button');
        btn.className = 'answer-btn';
        btn.textContent = ans.text;
        btn.addEventListener('click', function () {
          handleAnswer(btn, ans);
        });
        answerArea.appendChild(btn);
      });
    }, 800);
  }

  function handleAnswer(btn, answer) {
    if (answer.correct) {
      btn.classList.add('correct');
      // Disable all buttons
      document.querySelectorAll('.answer-btn').forEach(function (b) {
        b.disabled = true;
      });
      // Add user bubble
      addBubble(answer.text, 'user');
      // Next step
      setTimeout(function () {
        answerArea.innerHTML = '';
        currentStep++;
        showConversationStep();
      }, 1000);
    } else {
      btn.classList.add('wrong');
      setTimeout(function () {
        btn.classList.remove('wrong');
      }, 600);
    }
  }

  function addBubble(text, type) {
    var bubble = document.createElement('div');
    bubble.className = 'chat-bubble ' + (type === 'operator' ? 'chat-operator' : 'chat-user');
    bubble.textContent = text;
    chatArea.appendChild(bubble);
    chatArea.scrollTop = chatArea.scrollHeight;
  }

  // Start
  startBtn.addEventListener('click', function () {
    hide(introScreen);
    show(phoneScreen);
    dialed = '';
    updateDisplay();
  });

  // Restart
  restartBtn.addEventListener('click', function () {
    hide(endScreen);
    show(introScreen);
    dialed = '';
    callBtn.disabled = true;
    callBtn.classList.remove('key-highlight');
  });
})();
