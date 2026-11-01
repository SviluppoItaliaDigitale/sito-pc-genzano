/* ===================== CONFIG — testi, tempi ===================== */
/* Fonti: pagina /rischi-prevenzione/kit-emergenza/ del sito (elenco del kit, almeno tre giorni, controllo ogni sei mesi);
   Dipartimento della Protezione Civile, «Io non rischio». Nessuna quantità in litri: la pagina del sito le dà per esteso. */
const CONFIG = {
  titolo: "Il kit di emergenza",
  hud: "KIT",
  posterT: 0,
  scene: [
    { ill: "zaino", illh: 520, dur: 5, chip: "Protezione Civile · Genzano di Roma",
      righe: ["Il kit di", "<span class='a'>emergenza</span>"], sotto: "Uno zaino pronto <b>per i primi tre giorni</b>.",
      sottotitolo: "Il kit di emergenza: uno zaino sempre pronto, per i primi tre giorni." },
    { ill: "cibo", illh: 420, dur: 6, chip: "Da mettere nello zaino",
      righe: ["Acqua", "e <span class='a'>cibo</span>"], sotto: "Per <b>almeno tre giorni</b>. E l'apriscatole!",
      sottotitolo: "Acqua da bere e cibo che dura a lungo, per almeno tre giorni. E l'apriscatole!" },
    { ill: "luce", illh: 420, dur: 5, chip: "Da mettere nello zaino",
      righe: ["Torcia", "e <span class='a'>radio</span>"], sotto: "A pile, con le <b>batterie di ricambio</b>.",
      sottotitolo: "Una torcia e una radio a pile, con le batterie di ricambio." },
    { ill: "cura", illh: 420, dur: 5, chip: "Da mettere nello zaino",
      righe: ["Pronto", "<span class='a'>soccorso</span>"], sotto: "E le <b>medicine</b> di ogni giorno.",
      sottotitolo: "Il kit di pronto soccorso e le medicine che si prendono ogni giorno." },
    { ill: "documenti", illh: 420, dur: 5, chip: "Da mettere nello zaino",
      righe: ["Documenti", "e <span class='a'>soldi</span>"], sotto: "Le copie, in una <b>busta impermeabile</b>.",
      sottotitolo: "Le copie dei documenti in una busta impermeabile, e un po' di soldi." },
    { ill: "suoni", illh: 420, dur: 5, chip: "Da mettere nello zaino",
      righe: ["Caricabatterie", "e <span class='a'>fischietto</span>"], sotto: "Il fischietto serve <b>per farsi sentire</b>.",
      sottotitolo: "Il caricabatterie del telefono, e un fischietto per farsi sentire." },
    { ill: "vestiti", illh: 420, dur: 5, chip: "Da mettere nello zaino",
      righe: ["Vestiti", "e <span class='a'>coperta</span>"], sotto: "E il cibo per <b>il tuo animale</b>.",
      sottotitolo: "Vestiti di ricambio, una coperta, e il cibo per il tuo animale." },
    { ill: "porta", illh: 200, dur: 8, chip: "Genzano di Roma · Protezione Civile", finale: true,
      righe: ["Preparalo", "<span class='a'>insieme</span>"], sotto: "Vicino alla porta. <b>Ogni 6 mesi</b> controlla scadenze e batterie.",
      fonte: "Fonti: pagina «Kit di emergenza» del sito;<br>Dipartimento della Protezione Civile",
      sottotitolo: "Tenetelo vicino alla porta, e ogni sei mesi controllate scadenze e batterie. Preparatelo oggi, insieme!" }
  ]
};
