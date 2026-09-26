// ===================================================================================
// SAFE STORAGE
// Accesso protetto a localStorage per la mini-app del quiz.
// In navigazione privata, con i dati dei siti bloccati o a quota esaurita,
// localStorage può lanciare un'eccezione anche al solo accesso: ogni lettura
// e scrittura passa da qui e non interrompe mai la pagina.
// DEVE essere caricato PRIMA degli altri script che leggono o salvano dati.
// ===================================================================================

window.safeStorage = {
    get: function (key) {
        try {
            return window.localStorage.getItem(key);
        } catch (e) {
            return null;
        }
    },
    // Restituisce true se il valore è stato salvato, false altrimenti.
    // Chi salva dati che servono alla pagina successiva DEVE controllare
    // l'esito: proseguire dopo una scrittura fallita porta a una pagina che
    // non trova i dati e rimanda indietro, perdendo ciò che l'utente ha fatto.
    set: function (key, value) {
        try {
            window.localStorage.setItem(key, value);
            return true;
        } catch (e) {
            return false;
        }
    },
    remove: function (key) {
        try {
            window.localStorage.removeItem(key);
        } catch (e) {
            // Nulla da rimuovere o memoria non accessibile.
        }
    },
    // Rimuove solo le chiavi indicate. Mai localStorage.clear(): il quiz
    // condivide l'origine con il resto del sito, e svuotare tutto
    // cancellerebbe anche le preferenze di accessibilità e di lettura.
    removeMany: function (keys) {
        for (var i = 0; i < keys.length; i++) {
            this.remove(keys[i]);
        }
    },
    // Messaggio da mostrare quando il browser non consente di salvare:
    // dice che cosa succede e come rimediare, invece di un rimando muto.
    MESSAGGIO: 'Il browser non consente di salvare i dati del quiz, quindi non si può proseguire. ' +
        'Succede di solito in navigazione privata o quando i dati dei siti sono bloccati: ' +
        'apri la pagina in una finestra normale oppure consenti i dati per questo sito, poi riprova.',
    // Inserisce (una sola volta) un avviso role="alert" subito dopo l'elemento indicato.
    avviso: function (dopo, testo) {
        var esistente = document.getElementById('storageError');
        if (esistente) { esistente.textContent = testo || this.MESSAGGIO; esistente.focus(); return; }
        var box = document.createElement('div');
        box.id = 'storageError';
        box.className = 'alert alert-warning mt-3';
        box.setAttribute('role', 'alert');
        box.setAttribute('tabindex', '-1');
        box.textContent = testo || this.MESSAGGIO;
        dopo.insertAdjacentElement('afterend', box);
        box.focus();
    }
};
