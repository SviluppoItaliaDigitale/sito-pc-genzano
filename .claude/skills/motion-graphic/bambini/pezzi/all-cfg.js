/* ===================== CONFIG — testi, tempi ===================== */
/* Fonti: pagina /rischi-prevenzione/rischio-idrogeologico/ del sito (cosa fare prima, durante e dopo; testo del video
   per adulti del 25/09/2026); pagina /allerte-meteo/; Dipartimento della Protezione Civile, «Io non rischio» — alluvione. */
const CONFIG = {
  titolo: "Quando piove forte: come stare al sicuro dall'acqua",
  hud: "ACQUA",
  posterT: 0,
  scene: [
    { ill: "pioggia", illh: 520, dur: 5, chip: "Protezione Civile · Genzano di Roma",
      righe: ["Quando piove", "<span class='a'>forte</span>"], sotto: "<b>Come stare al sicuro dall'acqua.</b>",
      sottotitolo: "Quando piove forte: come stare al sicuro dall'acqua." },
    { ill: "sale", illh: 420, dur: 6, chip: "Attenzione",
      righe: ["L'acqua sale", "<span class='a'>in fretta</span>"], sotto: "Anche in <b>pochi minuti</b>.",
      sottotitolo: "Con la pioggia forte, l'acqua può salire all'improvviso, anche in pochi minuti." },
    { ill: "pericoli", illh: 420, dur: 8, chip: "I posti pericolosi",
      righe: ["Dove stare", "<span class='a'>attenti</span>"],
      sottotitolo: "I posti più pericolosi sono cantine, garage, sottopassi e le zone basse vicino a fossi e torrenti." },
    { ill: "prima", illh: 300, dur: 7, chip: "Prima", listaAt: [1.1, 3.9],
      righe: ["Prima,", "<span class='a'>preparati</span>"], lista: [
        ["allarme", "Guarda con la famiglia il colore dell'allerta"],
        ["zaino", "Tenete pronto il kit di emergenza"] ],
      sottotitolo: "Prima: guarda con la tua famiglia il colore dell'allerta e tenete pronto il kit di emergenza." },
    { ill: "sali", illh: 420, dur: 8, chip: "Se l'acqua arriva",
      righe: ["Sali ai piani", "<span class='a'>alti</span>"], sotto: "Mai in cantina o in garage. <b>Niente ascensore.</b>",
      sottotitolo: "Se l'acqua arriva, non scendere in cantina o in garage. Sali ai piani alti, senza usare l'ascensore." },
    { ill: "fuori", illh: 420, dur: 8, chip: "Se sei fuori",
      righe: ["Lontano", "dall'<span class='a'>acqua</span>"], sotto: "Anche poca acqua, se corre, <b>fa cadere</b>. Vai più in alto.",
      sottotitolo: "Se sei fuori, allontanati dall'acqua: se scorre veloce, anche poca acqua può farti cadere. Vai in un posto più alto." },
    { ill: "auto", illh: 420, dur: 7, chip: "Ricordalo ai grandi",
      righe: ["In auto, mai", "nei <span class='a'>sottopassi</span>"], sotto: "Né sulle <b>strade allagate</b>.",
      sottotitolo: "Ricordalo anche ai grandi: in auto, mai nei sottopassi o sulle strade allagate." },
    { ill: "dopo", illh: 420, dur: 7, chip: "Dopo",
      righe: ["Niente giochi", "nell'<span class='a'>acqua</span>"], sotto: "Può nascondere <b>buche e tombini aperti</b>.",
      sottotitolo: "Dopo, non giocare nell'acqua o nel fango: possono nascondere buche e tombini aperti." },
    { ill: "arcobaleno", illh: 200, dur: 7, chip: "Genzano di Roma · Protezione Civile", finale: true,
      righe: ["Solo fonti", "<span class='a'>ufficiali</span>"], sotto: "<b>protezionecivilegenzano.it</b>",
      grande: "112", fonte: "Fonti: pagina «Rischio idrogeologico» del sito;<br>Dipartimento della Protezione Civile, «Io non rischio»",
      sottotitolo: "Segui solo le fonti ufficiali. In emergenza chiama il 112." }
  ]
};
