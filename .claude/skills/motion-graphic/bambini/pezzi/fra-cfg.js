/* ===================== CONFIG — testi, tempi ===================== */
/* Fonti: Dipartimento della Protezione Civile, «Rischio meteo-idro. Sei preparato?», sezione «In caso di frana»
   (rischi.protezionecivile.gov.it/it/meteo-idro/sei-preparato/), verificata il 12/11/2026: allontanarsi di lato
   verso un punto più alto e stabile, rannicchiarsi e proteggere la testa, non sostare sotto alberi e pali, non
   avvicinarsi al ciglio della frana, segnalare il pericolo a chi arriva sulla strada. Pagina del sito
   /rischi-prevenzione/rischio-idrogeologico/ (pendii ripidi di Genzano verso il lago di Nemi; segnali: terreno
   che si crepa, alberi che si inclinano). 112 numero unico di emergenza nel Lazio.
   I `dur` sono stime (circa 15 caratteri al secondo + 1,7 s) finché manca la voce: con durate.json li sostituisce
   lo stampo. I tempi degli elenchi e dei disegni sono calcolati in fra-anim.js sulla durata vera della scena. */
const CONFIG = {
  titolo: "Le frane: riconoscerle e mettersi al sicuro",
  hud: "FRANE",
  posterT: 0,
  scene: [
    { ill: "titolo", illh: 520, dur: 8.8, chip: "Protezione Civile · Genzano di Roma",
      righe: ["Le <span class='a'>frane</span>"], sotto: "Terra, fango o roccia che <b>scivola lungo un pendio</b>.",
      sottotitolo: "Le frane: riconoscerle e mettersi al sicuro. Una frana è terra, fango o roccia che scivola lungo un pendio." },
    { ill: "pioggia", illh: 420, dur: 10.6, chip: "Quando succede",
      righe: ["Piogge forti", "o <span class='a'>lunghe</span>"], sotto: "A Genzano ci sono <b>pendii ripidi</b>, come verso il lago di Nemi.",
      sottotitolo: "Succede soprattutto con piogge forti, o che durano a lungo. Anche a Genzano ci sono pendii ripidi, come quelli verso il lago di Nemi." },
    { ill: "segnali", illh: 240, dur: 9.9, chip: "Occhi aperti",
      righe: ["I <span class='a'>segnali</span>"], lista: [
        ["crepa", "Crepe nel terreno o nei muri"],
        ["storto", "Alberi e pali che si inclinano"],
        ["smotta", "Piccoli smottamenti"],
        ["comune", "Se li noti, avvisa il Comune"] ],
      sottotitolo: "I segnali: crepe nel terreno o nei muri, alberi e pali che si inclinano, piccoli smottamenti. Se li noti, avvisa il Comune." },
    { ill: "casa", illh: 420, dur: 8, chip: "Attenzione",
      righe: ["Niente la", "<span class='a'>ferma</span>"], sotto: "Se la terra si muove, <b>allontanati subito</b>.",
      sottotitolo: "Nessun muro e nessuna casa possono fermare una frana. Se la terra si muove, allontanati subito." },
    { ill: "lato", illh: 420, dur: 11.1, chip: "Se viene verso di te",
      righe: ["Spostati", "<span class='a'>di lato</span>"], sotto: "Verso un punto <b>più alto e stabile</b>. Mai sotto alberi e pali.",
      sottotitolo: "Se la frana viene verso di te, spostati di lato, fuori dal suo percorso, verso un punto più alto e stabile. Non fermarti sotto alberi e pali." },
    { ill: "rannicchia", illh: 420, dur: 9.4, chip: "Se non riesci a scappare",
      righe: ["Rannicchiati,", "proteggi la <span class='a'>testa</span>"], sotto: "Lontano dal <b>bordo della frana</b>: può cedere ancora.",
      sottotitolo: "Se non riesci a scappare, rannicchiati e proteggi la testa. Non avvicinarti al bordo della frana: può cedere ancora." },
    { ill: "strada", illh: 200, dur: 8.3, chip: "Genzano di Roma · Protezione Civile", finale: true,
      righe: ["Fermati <span class='a'>lontano</span>", "e avvisa"], sotto: "<b>protezionecivilegenzano.it</b>",
      grande: "112", fonte: "Fonte: Dipartimento della Protezione Civile,<br>«In caso di frana»",
      sottotitolo: "Se trovi una frana sulla strada, fermati lontano, avvisa chi sta arrivando e chiama il 112." }
  ]
};
