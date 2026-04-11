// ===================================================================================
// MAIN LOADER
// Questo script definisce le categorie e unisce tutti i banchi di domande
// caricati dai file separati in un unico array.
// DEVE essere caricato DOPO tutti i file del banco domande.
// ===================================================================================

const CATEGORIES = [
    "Principi e Organizzazione",
    "Rischio Sismico",
    "Rischio Alluvione",
    "Incendi Boschivi",
    "Operatività e Logistica",
    "Piano Comunale Genzano"
];

// Unisce tutti gli array di domande in un unico grande banco dati.
// Questa variabile sarà usata dagli altri script (quiz, studio, risultati).
const FULL_QUESTION_BANK = [
    ...DOMANDE_PRINCIPI,
    ...DOMANDE_RISCHIO_SISMICO,
    ...DOMANDE_RISCHIO_ALLUVIONE,
    ...DOMANDE_INCENDI_BOSCHIVI,
    ...DOMANDE_OPERATIVITA,
    ...DOMANDE_PIANO_COMUNALE
];