/* ===================== CONFIG — testi, tempi ===================== */
/* Fonti: pagina /rischi-prevenzione/rischio-incendio/ del sito (cause, periodo giugno-settembre, come comportarsi,
   via di fuga verso una strada o un corso d'acqua, mai dove soffia il vento né in salita); 112 per segnalare. */
const CONFIG = {
  titolo: "Il fuoco nel bosco: come nasce e che cosa fare",
  hud: "INCENDI",
  posterT: 0,
  scene: [
    { ill: "bosco", illh: 520, dur: 5, chip: "Protezione Civile · Genzano di Roma",
      righe: ["Il fuoco", "nel <span class='a'>bosco</span>"], sotto: "<b>Come nasce e che cosa fare.</b>",
      sottotitolo: "Il fuoco nel bosco: come nasce e che cosa fare." },
    { ill: "cause", illh: 420, dur: 7, chip: "Come nasce",
      righe: ["Quasi sempre", "da una <span class='a'>persona</span>"],
      sottotitolo: "Quasi sempre un incendio nasce da una persona: un mozzicone, un fiammifero, un fuoco lasciato acceso." },
    { ill: "cresce", illh: 420, dur: 7, chip: "Come cresce",
      righe: ["Cresce", "in <span class='a'>fretta</span>"], sotto: "Erba secca, caldo e vento. Pericolo più alto <b>da giugno a settembre</b>.",
      sottotitolo: "Erba secca, caldo e vento lo fanno crescere in fretta. Da giugno a settembre il pericolo è più alto." },
    { ill: "area", illh: 420, dur: 8, chip: "Per evitarlo",
      righe: ["Solo nelle aree", "<span class='a'>attrezzate</span>"], sotto: "Con un adulto, e si spegne bene. <b>Con il vento, mai.</b>",
      sottotitolo: "Il fuoco si accende solo nelle aree attrezzate, con un adulto, e si spegne bene. Con il vento, mai." },
    { ill: "vedi", illh: 420, dur: 8, chip: "Se vedi fiamme o fumo",
      righe: ["Avvisa", "un <span class='a'>adulto</span>"], sotto: "Il numero da chiamare è il <b>112</b>.",
      sottotitolo: "Se vedi fiamme o fumo, allontanati e avvisa subito un adulto. Il numero da chiamare è il 112." },
    { ill: "solo", illh: 420, dur: 6, chip: "Se sei solo",
      righe: ["Chiama tu", "il <span class='a'>112</span>"], sotto: "E di' <b>dove sei</b>.",
      sottotitolo: "Se sei solo e il pericolo è vero, chiama tu il 112, e di' dove sei." },
    { ill: "fuga", illh: 420, dur: 8, chip: "Se il fuoco è vicino",
      righe: ["Verso una", "<span class='a'>strada</span>"], sotto: "O un corso d'acqua. Mai dove soffia il vento, <b>mai in salita</b>.",
      sottotitolo: "Allontanati verso una strada o un corso d'acqua. Non andare dove soffia il vento, e non scappare in salita." },
    { ill: "spettacolo", illh: 420, dur: 8, chip: "Non è uno spettacolo",
      righe: ["Non fermarti", "a <span class='a'>guardare</span>"], sotto: "E nella <b>zona bruciata</b> non si entra.",
      sottotitolo: "L'incendio non è uno spettacolo: non ci si ferma a guardare. E nella zona bruciata non si entra." },
    { ill: "verde", illh: 200, dur: 6, chip: "Genzano di Roma · Protezione Civile", finale: true,
      righe: ["Il bosco", "è di <span class='a'>tutti</span>"], sotto: "<b>protezionecivilegenzano.it</b>",
      grande: "112", fonte: "Fonti: pagina «Rischio incendio» del sito;<br>Dipartimento della Protezione Civile, «Io non rischio»",
      sottotitolo: "Il bosco è di tutti. In emergenza chiama il 112." }
  ]
};
