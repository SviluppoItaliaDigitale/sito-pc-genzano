/* Domande dell'assistente «Diventa volontario» del Gruppo Comunale Volontari di Protezione Civile di
   Genzano di Roma (motore in assistente-volontari.js). Dati presi dalla pagina /diventa-volontario/
   (età da 16 anni, piena operatività a 18, ruoli, circa 16 ore al mese, colloquio conoscitivo, documenti)
   e dalle indicazioni di Alessandro del 18/11/2026 (patenti B, C, D ed E con BE, CE, DE; documenti
   chiesti solo dopo il colloquio). Nessuna richiesta di rete, nessun dato salvato nel browser. */
(function () {
  "use strict";
  var radice = document.querySelector("[data-assistente-volontari]");
  if (!radice || !window.AssistenteVolontari) return;

  var EMAIL = "segreteria@protezionecivilegenzano.it";
  var telefono = function (x) {
    return /^[+0-9][0-9 .\/()-]{5,}$/.test(x) && x.replace(/\D/g, "").length >= 6 ||
      "Il numero sembra incompleto. Scrivi solo il numero, per esempio 333 1234567.";
  };
  var email = function (x) {
    return x === "—" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(x) || "Controlla l'indirizzo email: manca qualcosa.";
  };

  window.AssistenteVolontari(radice, {
    classeBottone: "btn btn-primary",
    classeBottoneChiaro: "btn btn-outline-primary",
    saluto: "Benvenuto. Questo assistente ti fa alcune domande per conoscerti prima del colloquio con il Gruppo. Servono circa 3 minuti.",
    intestazione: "Richiesta di colloquio per diventare volontario del Gruppo Comunale di Protezione Civile di Genzano di Roma. Risposte date all'assistente del sito:",
    recapitoCopia: EMAIL,
    domande: [
      { k: "privacy", t: "scelta",
        q: "Prima di iniziare: le risposte restano sul tuo dispositivo. Il sito non le riceve e non le salva. Alla fine prepariamo un'email con le tue risposte: la controlli e la invii tu alla segreteria del Gruppo, che la usa solo per contattarti.",
        o: ["Ho capito, inizio", "Non ora"],
        ferma: { "Non ora": "Va bene. Puoi ricominciare quando vuoi, oppure chiamare la sede al 06 9362600." } },
      { k: "eta", t: "scelta", etichetta: "Età",
        q: "Quanti anni hai?",
        o: ["Meno di 16 anni", "16 o 17 anni", "18 anni o più"],
        ferma: { "Meno di 16 anni": "Grazie per l'interesse. Per aderire al Gruppo bisogna aver compiuto 16 anni. Intanto puoi scoprire come prepararti alle emergenze nelle pagine Rischi e prevenzione del sito." },
        dopo: function (v) {
          return v === "16 o 17 anni" ? "Da minorenne puoi partecipare alla formazione e alle attività consentite. La piena operatività sul campo è prevista dai 18 anni. Per l'iscrizione serve il consenso di un genitore o di chi esercita la responsabilità genitoriale." : "";
        } },
      { k: "nome", t: "testo", max: 120, etichetta: "Nome e cognome", autocompleta: "name",
        q: "Come ti chiami? Scrivi nome e cognome." },
      { k: "comune", t: "testo", max: 120, etichetta: "Comune di residenza", autocompleta: "address-level2",
        q: "In quale comune abiti?" },
      { k: "ruoli", t: "multi", etichetta: "Attività di interesse",
        q: "Quali attività ti interessano? Puoi sceglierne più di una.",
        o: ["Logistica e magazzino", "Sala radio e comunicazioni", "Segreteria operativa", "Educazione nelle scuole", "Supporto agli eventi", "Cucina da campo", "Antincendio boschivo", "Guida dei mezzi", "Comunicazione e social", "Non lo so ancora"],
        esclusiva: "Non lo so ancora",
        dopo: function (v) {
          return v === "Non lo so ancora" ? "Nessun problema: ne parliamo al colloquio. Il Gruppo ha bisogno di competenze diverse." : "";
        } },
      { k: "patenti", t: "multi", etichetta: "Patenti",
        q: "Quali patenti hai? Puoi sceglierne più di una.",
        o: ["B", "BE", "C", "CE", "D", "DE", "Nessuna"],
        esclusiva: "Nessuna",
        dopo: function () {
          return "Le patenti B, C, D ed E (BE, CE, DE) ci aiutano a guidare i nostri mezzi, ma non sono obbligatorie: c'è posto anche per chi non guida.";
        } },
      { k: "competenze", t: "multi", etichetta: "Competenze ed esperienze",
        q: "Hai competenze o esperienze utili? Puoi sceglierne più di una.",
        o: ["Radio o radioamatore", "Primo soccorso", "Informatica", "Lavori manuali", "Assistenza alle persone", "Lingue straniere", "Altro volontariato", "Nessuna in particolare"],
        esclusiva: "Nessuna in particolare",
        dopo: function (v) {
          return /Nessuna/.test(v) ? "Non servono esperienze precedenti: il Gruppo ti forma prima dell'impiego operativo." : "";
        } },
      { k: "disponibilita", t: "multi", etichetta: "Disponibilità",
        q: "Quando sei disponibile? Puoi sceglierne più di una.",
        o: ["Mattina nei giorni feriali", "Pomeriggio nei giorni feriali", "Sera nei giorni feriali", "Sabato", "Domenica e festivi", "Di notte durante allerte ed emergenze"] },
      { k: "impegno", t: "scelta", etichetta: "Impegno di circa 16 ore al mese",
        q: "L'impegno ordinario è di circa 16 ore al mese, tra turni, formazione e addestramento. Pensi di riuscire?",
        o: ["Sì", "Forse, ne parliamo al colloquio", "No, per ora"],
        dopo: function (v) {
          return v === "Sì" ? "" : "La disponibilità si concorda tenendo conto della tua vita personale e lavorativa: ne parliamo al colloquio.";
        } },
      { k: "telefono", t: "testo", max: 40, tipo: "tel", etichetta: "Telefono", autocompleta: "tel", v: telefono,
        q: "Il tuo numero di telefono, per fissare il colloquio." },
      { k: "email", t: "testo", max: 160, tipo: "email", etichetta: "Email", autocompleta: "email", facoltativa: true, v: email,
        q: "La tua email, se vuoi lasciarla." },
      { k: "note", t: "testo", max: 600, etichetta: "Note", facoltativa: true,
        q: "Vuoi aggiungere qualcosa su di te?" }
    ],
    chiusura: function (a) {
      return [
        "Grazie, " + a.nome + ". Il primo passo è un colloquio conoscitivo: ti contattiamo per fissarlo.",
        "In fase di colloquio ti chiederemo i documenti per l'iscrizione, tra cui il certificato medico di sana e robusta costituzione, e verificheremo i requisiti, compresa l'assenza di condanne penali ostative."
      ];
    },
    canali: [
      { testo: "Invia l'email alla segreteria", principale: true,
        indirizzo: function (t, a) { return "mailto:" + EMAIL + "?subject=" + encodeURIComponent("Diventare volontario - " + a.nome) + "&body=" + encodeURIComponent(t); } },
      { testo: "Chiama la sede: 06 9362600",
        indirizzo: function () { return "tel:+39069362600"; } }
    ],
    dopoInvio: "Ricordati di premere Invia nell'app di posta che si apre. Se non si apre nulla, usa «Copia il testo» e incollalo in un'email a " + EMAIL + "."
  });
})();
