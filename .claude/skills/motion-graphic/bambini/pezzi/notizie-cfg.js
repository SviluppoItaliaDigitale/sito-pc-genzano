/* ===================== CONFIG — testi, tempi ===================== */
/* Fonti: scheda del sito «Notizie false in emergenza» (regola dei tre controlli: fonte, data e
   luogo, conferma ufficiale; non inoltrare ciò che non è verificato); Dipartimento della Protezione
   Civile, IT-alert sistema nazionale di allarme pubblico; 112 numero unico di emergenza nel Lazio. */
const CONFIG = {
  titolo: "Notizie vere e notizie false in emergenza",
  hud: "NOTIZIE",
  posterT: 0,
  scene: [
    { ill: "telefono", illh: 520, dur: 5, chip: "Protezione Civile · Genzano di Roma",
      righe: ["Notizie vere,", "notizie <span class='a'>false</span>"], sotto: "<b>Come riconoscerle in un'emergenza.</b>",
      sottotitolo: "Notizie vere e notizie false: come riconoscerle in un'emergenza." },
    { ill: "chat", illh: 460, dur: 6, chip: "Cosa sapere",
      righe: ["Girano", "<span class='a'>in fretta</span>"], sotto: "Messaggi inoltrati, <b>foto vecchie</b>, voci senza fonte.",
      sottotitolo: "In un'emergenza girano in fretta anche notizie false: messaggi inoltrati, foto vecchie, voci senza una fonte." },
    { ill: "lente", illh: 240, dur: 9, chip: "Tre controlli", listaAt: [3.0, 3.9, 6.95],
      righe: ["Prima di", "<span class='a'>crederci</span>"], lista: [
        ["persone", "Chi lo dice?"],
        ["calendario", "È di oggi? Parla di qui?"],
        ["scudo", "Lo confermano le fonti ufficiali?"] ],
      sottotitolo: "Prima di crederci, fai tre controlli. Chi lo dice? È di oggi, e parla davvero del nostro paese? Lo confermano le fonti ufficiali?" },
    { ill: "fonti", illh: 420, dur: 8, chip: "Le fonti ufficiali",
      righe: ["Dove", "<span class='a'>controllare</span>"],
      sottotitolo: "Le fonti ufficiali sono il Comune, la Protezione Civile, i messaggi di allarme sul cellulare e il sito del nostro Gruppo comunale." },
    { ill: "inoltra", illh: 440, dur: 7, chip: "Se non sei sicuro",
      righe: ["Non", "<span class='a'>inoltrare</span>"], sotto: "Una notizia falsa <b>spaventa e confonde</b>.",
      sottotitolo: "Se non sei sicuro, non inoltrare il messaggio. Una notizia falsa spaventa le persone e confonde chi deve aiutare." },
    { ill: "adulto", illh: 420, dur: 7, chip: "Se ti fa paura",
      righe: ["Parlane con", "un <span class='a'>adulto</span>"], sotto: "Un genitore, un insegnante: <b>controllate insieme</b>.",
      sottotitolo: "Se un messaggio ti fa paura, parlane con un adulto di fiducia, un genitore o un insegnante, e controllate insieme." },
    { ill: "sereno", illh: 200, dur: 7, chip: "Genzano di Roma · Protezione Civile", finale: true,
      righe: ["Segui solo", "le fonti <span class='a'>ufficiali</span>"], sotto: "<b>protezionecivilegenzano.it</b>",
      grande: "112", fonte: "Fonti: Dipartimento della Protezione Civile (IT-alert);<br>scheda «Notizie false in emergenza»",
      sottotitolo: "Segui solo le fonti ufficiali. In emergenza chiama il 112." }
  ]
};
