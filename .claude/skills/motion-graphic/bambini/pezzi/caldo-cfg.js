/* ===================== CONFIG — testi, tempi ===================== */
/* Fonti: pagina /rischi-prevenzione/ondate-di-calore/ del sito; Ministero della Salute, «Ondate di calore —
   Dieci consigli utili» (ore più calde dalle 11 alle 18, registro data/dati_canonici.yaml). */
const CONFIG = {
  titolo: "Il caldo: come proteggersi",
  hud: "CALDO",
  posterT: 0,
  scene: [
    { ill: "sole", illh: 520, dur: 5, chip: "Protezione Civile · Genzano di Roma",
      righe: ["Quando fa", "<span class='a'>troppo caldo</span>"], sotto: "<b>Ondate di calore: come proteggersi.</b>",
      sottotitolo: "Quando fa troppo caldo: come proteggersi dalle ondate di calore." },
    { ill: "acqua", illh: 420, dur: 7, chip: "Bevi spesso",
      righe: ["Bevi", "<span class='a'>acqua</span>"], sotto: "Anche se non hai sete. <b>Fresca, non ghiacciata.</b>",
      sottotitolo: "Bevi acqua spesso, anche se non hai sete. Meglio fresca, non ghiacciata, a piccoli sorsi." },
    { ill: "ore", illh: 420, dur: 7, chip: "Le ore più calde",
      righe: ["Dalle 11", "alle <span class='a'>18</span>"], sotto: "Resta al fresco e all'ombra. <b>Niente sforzi.</b>",
      sottotitolo: "Dalle 11 alle 18 resta al fresco o all'ombra e non fare sforzi." },
    { ill: "vestiti", illh: 240, dur: 8, chip: "Come vestirsi", listaAt: [1.0, 2.8, 4.9],
      righe: ["Leggero", "e <span class='a'>chiaro</span>"], lista: [
        ["gilet", "Abiti leggeri e chiari"],
        ["cappello", "Cappello e occhiali da sole"],
        ["frutta", "Pasti leggeri, frutta e verdura"] ],
      sottotitolo: "Indossa abiti leggeri e chiari, cappello e occhiali da sole. Fai pasti leggeri, con frutta e verdura." },
    { ill: "auto", illh: 420, dur: 7, chip: "Mai in auto",
      righe: ["Mai chiusi", "in <span class='a'>auto</span>"], sotto: "Né persone né animali, <b>nemmeno per poco</b>.",
      sottotitolo: "Non lasciare mai persone o animali in un'auto parcheggiata al sole." },
    { ill: "vicini", illh: 420, dur: 7, chip: "Aiuta gli altri",
      righe: ["Pensa", "ai <span class='a'>vicini</span>"], sotto: "Chiedi come stanno <b>gli anziani e chi vive da solo</b>.",
      sottotitolo: "Insieme alla tua famiglia, chiedi come stanno i vicini anziani e chi vive da solo." },
    { ill: "malore", illh: 420, dur: 8, chip: "Se qualcuno sta male",
      righe: ["Al fresco,", "e chiama il <span class='a'>112</span>"], sotto: "Avvisa un adulto. <b>Portatelo all'ombra.</b>",
      sottotitolo: "Se qualcuno sta male per il caldo, avvisa un adulto e chiamate il 112. Intanto portatelo in un posto fresco." },
    { ill: "sereno", illh: 200, dur: 7, chip: "Genzano di Roma · Protezione Civile", finale: true,
      righe: ["Acqua, ombra", "e <span class='a'>fresco</span>"], sotto: "<b>protezionecivilegenzano.it</b>",
      grande: "112", fonte: "Fonti: Ministero della Salute, «Ondate di calore»;<br>pagina «Ondate di calore» del sito",
      sottotitolo: "Acqua, ombra e fresco. In emergenza chiama il 112." }
  ]
};
