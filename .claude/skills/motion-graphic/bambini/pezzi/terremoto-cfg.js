/* ===================== CONFIG — testi, tempi ===================== */
/* Fonti: Dipartimento della Protezione Civile, «Sei preparato?» del rischio sismico
   (rischi.protezionecivile.gov.it/it/sismico/sei-preparato/), campagna «Io non rischio»;
   pagina /rischi-prevenzione/rischio-sismico/ del sito; Scatola delle esercitazioni (lo zaino
   resta in classe). 112 numero unico di emergenza nel Lazio. */
const CONFIG = {
  titolo: "Terremoto: cosa fare prima, durante e dopo",
  hud: "TERREMOTO",
  posterT: 0,
  scene: [
    { ill: "scuola", illh: 520, dur: 5, chip: "Protezione Civile · Genzano di Roma",
      righe: ["Terremoto:", "<span class='a'>cosa fare</span>"], sotto: "<b>Prima, durante e dopo la scossa.</b>",
      sottotitolo: "Terremoto: cosa fare prima, durante e dopo la scossa." },
    { ill: "sismografo", illh: 420, dur: 6, chip: "Cosa sapere",
      righe: ["Arriva", "<span class='a'>senza avviso</span>"], sotto: "Nessuno sa dire quando. <b>Possiamo sapere che cosa fare.</b>",
      sottotitolo: "Nessuno può sapere quando arriverà un terremoto. Possiamo però sapere che cosa fare." },
    { ill: "prima", illh: 220, dur: 8, chip: "Prima", listaAt: [1.1, 5.9, 8.0],
      righe: ["Preparati"], lista: [
        ["casa", "Trova i posti sicuri della casa"],
        ["pin", "Conosci l'area di attesa più vicina"],
        ["zaino", "Prepara il kit e il piano della famiglia"] ],
      sottotitolo: "Prima: trova i posti sicuri della casa, come un tavolo resistente o un muro portante. Conosci l'area di attesa più vicina e prepara con la famiglia il kit e il piano di emergenza." },
    { ill: "tavolo", illh: 480, dur: 8, chip: "Durante la scossa",
      righe: ["Abbassati,", "<span class='a'>copriti</span>, tieniti"], sotto: "Sotto un tavolo resistente o il banco. <b>Proteggi la testa.</b>",
      sottotitolo: "Durante la scossa, se sei al chiuso: abbassati, riparati sotto un tavolo resistente o sotto il banco, e tieniti forte. Proteggi la testa con le braccia." },
    { ill: "pericolo", illh: 420, dur: 7, chip: "Durante la scossa",
      righe: ["Non correre", "<span class='a'>fuori</span>"], nota: "Aspetta che la scossa <b>finisca</b>",
      sottotitolo: "Non correre fuori: aspetta che la scossa finisca. Stai lontano da finestre e mobili alti, e non usare l'ascensore." },
    { ill: "aperto", illh: 420, dur: 7, chip: "Se sei all'aperto",
      righe: ["Cerca uno", "spazio <span class='a'>aperto</span>"], sotto: "Lontano da <b>edifici, alberi, lampioni e fili elettrici</b>.",
      sottotitolo: "Se sei all'aperto, allontanati da edifici, alberi, lampioni e fili elettrici, e aspetta in uno spazio aperto." },
    { ill: "fila", illh: 420, dur: 8, chip: "A scuola",
      righe: ["Segui", "l'<span class='a'>insegnante</span>"], sotto: "Esci in fila, senza correre. <b>Lo zaino resta in classe.</b>",
      sottotitolo: "A scuola, finita la scossa, segui l'insegnante. Esci in fila, senza correre, e raggiungi con la classe il punto di raccolta. Lo zaino resta in classe." },
    { ill: "dopo", illh: 220, dur: 9, chip: "Dopo", listaAt: [0.9, 3.4, 6.0, 7.9],
      righe: ["Esci con", "<span class='a'>prudenza</span>"], lista: [
        ["persone", "Controlla che chi è con te stia bene"],
        ["scarpe", "Metti le scarpe, niente ascensore"],
        ["pin", "Raggiungi l'area di attesa"],
        ["telefono", "Usa poco il telefono"] ],
      sottotitolo: "Dopo, controlla che chi è con te stia bene. Metti le scarpe, esci senza ascensore, raggiungi l'area di attesa e usa poco il telefono." },
    { ill: "sereno", illh: 200, dur: 7, chip: "Genzano di Roma · Protezione Civile", finale: true,
      righe: ["Prepariamoci", "<span class='a'>prima</span>"], sotto: "<b>protezionecivilegenzano.it</b>",
      grande: "112", fonte: "Fonte: Dipartimento della Protezione Civile,<br>«Sei preparato?» e campagna «Io non rischio»",
      sottotitolo: "Il terremoto non avvisa: prepariamoci prima. In emergenza chiama il 112." }
  ]
};
