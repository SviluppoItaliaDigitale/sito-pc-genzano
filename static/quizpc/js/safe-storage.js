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
    set: function (key, value) {
        try {
            window.localStorage.setItem(key, value);
        } catch (e) {
            // Nessuna memoria disponibile: si prosegue senza salvare.
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
    }
};
