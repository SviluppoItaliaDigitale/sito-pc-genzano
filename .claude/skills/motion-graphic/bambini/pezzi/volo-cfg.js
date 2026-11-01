/* ===================== CONFIG — testi, tempi ===================== */
/* Fonti: pagina /diventa-volontario/ del sito (dai 16 anni si può chiedere di aderire, piena operatività
   sul campo dai 18; il Gruppo non si attiva su chiamata dei cittadini, in emergenza si chiama il 112);
   pagina /conoscere/ (il Servizio nazionale della protezione civile è un sistema di enti e volontariato). */
const CONFIG = {
  titolo: "La protezione civile e i volontari",
  hud: "VOLONTARI",
  posterT: 0,
  scene: [
    { ill: "gruppo", illh: 520, dur: 6, chip: "Protezione Civile · Genzano di Roma",
      righe: ["Che cos'è la", "<span class='a'>protezione civile</span>"], sotto: "<b>Tante persone che lavorano insieme.</b>",
      sottotitolo: "La protezione civile è un sistema: tante persone e tanti enti che lavorano insieme." },
    { ill: "chi", illh: 420, dur: 7, chip: "Chi ne fa parte",
      righe: ["Tutti", "<span class='a'>insieme</span>"],
      sottotitolo: "Ne fanno parte il Comune, i Vigili del Fuoco, la sanità e i volontari." },
    { ill: "volontari", illh: 420, dur: 8, chip: "I volontari",
      righe: ["I volontari", "del <span class='a'>Gruppo</span>"], sotto: "Si formano, si addestrano <b>e aiutano il territorio</b>.",
      sottotitolo: "Il Gruppo comunale di Genzano è fatto di volontari: si formano, si addestrano e aiutano il territorio." },
    { ill: "catena", illh: 420, dur: 8, chip: "In emergenza",
      righe: ["Prima", "il <span class='a'>112</span>"], sotto: "Il Gruppo non si chiama direttamente: <b>lo attivano le autorità</b>.",
      sottotitolo: "Il Gruppo non si chiama direttamente: in emergenza chiami il 112, e sono le autorità ad attivare i volontari." },
    { ill: "entra", illh: 420, dur: 7, chip: "Puoi esserci anche tu",
      righe: ["Dai <span class='a'>16 anni</span>"], sotto: "Puoi chiedere di entrare nel Gruppo. <b>Sul campo dai 18.</b>",
      sottotitolo: "Dai 16 anni puoi chiedere di entrare nel Gruppo. Sul campo si va dai 18 anni." },
    { ill: "parte", illh: 240, dur: 8, chip: "Fai la tua parte", listaAt: [2.1, 3.2, 5.2],
      righe: ["Anche tu", "<span class='a'>conti</span>"], lista: [
        ["pericolo", "Conosci i rischi"],
        ["famiglia", "Prepara il piano della famiglia"],
        ["persone", "Aiuta chi ha bisogno"] ],
      sottotitolo: "Anche tu fai la tua parte: conosci i rischi, prepara il piano della famiglia e aiuta chi ha bisogno." },
    { ill: "sereno", illh: 200, dur: 7, chip: "Genzano di Roma · Protezione Civile", finale: true,
      righe: ["Diventa", "<span class='a'>volontario</span>"], sotto: "<b>protezionecivilegenzano.it</b>",
      grande: "112", fonte: "Fonti: pagine «Diventa volontario»<br>e «Conoscere la protezione civile» del sito",
      sottotitolo: "Scopri come diventare volontario sul sito del Gruppo. In emergenza chiama il 112." }
  ]
};
