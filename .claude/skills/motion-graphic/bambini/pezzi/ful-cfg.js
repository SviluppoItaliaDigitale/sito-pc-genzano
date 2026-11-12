/* ===================== CONFIG — testi, tempi ===================== */
/* Fonti: Dipartimento della Protezione Civile, «Rischio meteo-idro. Sei preparato?», sezione
   «In caso di temporali e fulmini» (rischi.protezionecivile.gov.it/it/meteo-idro/sei-preparato/),
   verificata il 12/11/2026; pagina /rischi-prevenzione/temporali-intensi/ del sito.
   112 numero unico di emergenza nel Lazio. I tempi di listaAt seguono la voce (durate.json). */
const CONFIG = {
  titolo: "Temporali e fulmini: come stare al sicuro",
  hud: "TEMPORALI",
  posterT: 0,
  scene: [
    { ill: "temporale", illh: 520, dur: 8, chip: "Protezione Civile · Genzano di Roma",
      righe: ["Temporali e", "<span class='a'>fulmini</span>"], sotto: "<b>Come stare al sicuro.</b>",
      sottotitolo: "Temporali e fulmini: come stare al sicuro. Un temporale si forma in fretta e lascia poco tempo per ripararsi." },
    { ill: "prima", illh: 420, dur: 8, chip: "Prima di uscire",
      righe: ["Guarda le", "<span class='a'>previsioni</span>"], sotto: "E l'allerta del giorno. <b>Cielo scuro? Cambia programma.</b>",
      sottotitolo: "Prima di una gita o di una partita all'aperto, guarda le previsioni e l'allerta del giorno. Se il cielo si fa scuro, cambia programma." },
    { ill: "tuono", illh: 420, dur: 8, chip: "Se senti il tuono",
      righe: ["Sei già in", "<span class='a'>pericolo</span>"], sotto: "Il temporale è a pochi chilometri. <b>Raggiungi subito un luogo chiuso.</b>",
      sottotitolo: "Se senti il tuono, anche lontano, il temporale è a pochi chilometri: sei già in pericolo. Raggiungi subito un luogo chiuso." },
    { ill: "riparo", illh: 240, dur: 10, chip: "Il riparo giusto", listaAt: [1.8, 4.3, 7.4],
      righe: ["Dentro un", "<span class='a'>edificio</span>"], lista: [
        ["riparoCasa", "Un edificio"],
        ["riparoAuto", "L'automobile, tutta chiusa"],
        ["riparoNo", "Tettoie, gazebo, balconi: no"] ],
      sottotitolo: "Il riparo giusto è un edificio. Se non c'è, va bene l'automobile, con porte e finestrini chiusi. Tettoie, gazebo e balconi non riparano." },
    { ill: "aperto", illh: 240, dur: 10, chip: "Se sei all'aperto", listaAt: [2.0, 6.8, 7.9, 9.6],
      righe: ["Mai sotto", "un <span class='a'>albero</span>"], lista: [
        ["noAlbero", "Alberi, alti e appuntiti"],
        ["noPalo", "Pali e tralicci"],
        ["noRete", "Recinzioni di metallo"],
        ["noAcqua", "Acqua"] ],
      sottotitolo: "Non ripararti sotto un albero: i fulmini colpiscono le cose alte e appuntite. Stai lontano da pali, tralicci, recinzioni di metallo e dall'acqua." },
    { ill: "casa", illh: 420, dur: 10, chip: "In casa",
      righe: ["Al sicuro", "anche <span class='a'>in casa</span>"], sotto: "Finestre chiuse, spine staccate. <b>Telefono fisso no, cellulare sì.</b>",
      sottotitolo: "In casa chiudi le finestre e stacca le spine di televisore e computer. Non usare il telefono fisso: il cellulare sì. Doccia e piatti, dopo il temporale." },
    { ill: "sereno", illh: 200, dur: 7, chip: "Genzano di Roma · Protezione Civile", finale: true,
      righe: ["Aspetta", "<span class='a'>30 minuti</span>"], sotto: "<b>protezionecivilegenzano.it</b>",
      grande: "112", fonte: "Fonte: Dipartimento della Protezione Civile,<br>«In caso di temporali e fulmini»",
      sottotitolo: "Aspetta 30 minuti dopo l'ultimo tuono, prima di tornare fuori. In emergenza chiama il 112." }
  ]
};
