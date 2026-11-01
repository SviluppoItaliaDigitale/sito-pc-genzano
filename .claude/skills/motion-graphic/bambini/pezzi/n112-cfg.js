/* ===================== CONFIG — testi, tempi ===================== */
/* Fonti: pagina /numeri-utili/ del sito (§ «Prima di chiamare»: dove sei, cosa è successo, feriti,
   parla con calma e non chiudere finché l'operatore non te lo dice); scheda «Chiamo il 112»
   (chi sei, dove sei, cosa è successo, se ci sono feriti; con un adulto vicino si chiama insieme).
   112 numero unico di emergenza nel Lazio. */
const CONFIG = {
  titolo: "Il 112: come si chiama in emergenza",
  hud: "112",
  posterT: 0,
  scene: [
    { ill: "numero", illh: 520, dur: 5, chip: "Protezione Civile · Genzano di Roma",
      righe: ["Il <span class='a'>112</span>", "per le emergenze"], sotto: "<b>Un solo numero per ogni emergenza.</b>",
      sottotitolo: "Il 112 è il numero da chiamare in ogni emergenza." },
    { ill: "quando", illh: 420, dur: 7, chip: "Quando chiamarlo",
      righe: ["Quando serve", "<span class='a'>aiuto</span>"],
      sottotitolo: "Chiamalo se qualcuno sta male, se vedi fuoco o fumo, se c'è un incidente o un pericolo serio." },
    { ill: "dire", illh: 240, dur: 8, chip: "Al telefono", listaAt: [1.4, 2.1, 2.7, 4.2],
      righe: ["Che cosa", "<span class='a'>dire</span>"], lista: [
        ["persone", "Chi sei"],
        ["pin", "Dove sei"],
        ["fumetto", "Che cosa è successo"],
        ["cerotto", "Se ci sono feriti"] ],
      sottotitolo: "Al telefono di' chi sei, dove sei, che cosa è successo e se ci sono feriti." },
    { ill: "calma", illh: 420, dur: 7, chip: "Al telefono",
      righe: ["Parla con", "<span class='a'>calma</span>"], sotto: "Rispondi alle domande. <b>Non chiudere finché l'operatore non te lo dice.</b>",
      sottotitolo: "Parla con calma e rispondi alle domande. Non chiudere finché l'operatore non te lo dice." },
    { ill: "insieme", illh: 420, dur: 7, chip: "Se sei un bambino",
      righe: ["Chiama con", "un <span class='a'>adulto</span>"], sotto: "Se c'è un adulto vicino, avvisalo. <b>Se sei da solo, chiama tu.</b>",
      sottotitolo: "Se c'è un adulto vicino, avvisalo e chiamate insieme. Se sei da solo, chiama tu." },
    { ill: "scherzo", illh: 420, dur: 7, chip: "Non è un gioco",
      righe: ["Mai per", "<span class='a'>scherzo</span>"], sotto: "Una chiamata per scherzo <b>occupa la linea</b> di chi ha bisogno.",
      sottotitolo: "Non chiamare mai per scherzo: occupi la linea di chi ha davvero bisogno di aiuto." },
    { ill: "sereno", illh: 200, dur: 7, chip: "Genzano di Roma · Protezione Civile", finale: true,
      righe: ["Ricorda", "il <span class='a'>numero</span>"], sotto: "<b>protezionecivilegenzano.it</b>",
      grande: "112", fonte: "Fonti: pagina «Numeri utili» del sito;<br>scheda «Chiamo il 112»",
      sottotitolo: "Ricorda il numero: 112. Uno, uno, due." }
  ]
};
