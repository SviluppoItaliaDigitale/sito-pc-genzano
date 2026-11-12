/* ===================== CONFIG — testi, tempi ===================== */
/* Fonti: Dipartimento della Protezione Civile, pagina «Rischio meteo-idro. Sei preparato?», sezione
   «Cosa fare in caso di venti e mareggiate» (rischi.protezionecivile.gov.it/it/meteo-idro/sei-preparato/),
   verificata il 12/11/2026; pagina /rischi-prevenzione/vento-forte/ del sito.
   I `dur` sono stime (caratteri della frase / 15 + 1,7 s): quando c'è durate.json valgono le durate vere
   e ogni momento dei disegni si sposta da solo, perché è calcolato con quando() sulla parola pronunciata. */
const CONFIG = {
  titolo: "Vento forte: che cosa fare",
  hud: "VENTO FORTE",
  posterT: 0,
  scene: [
    { ill: "titolo", illh: 520, dur: 7.8, chip: "Protezione Civile · Genzano di Roma",
      righe: ["Vento <span class='a'>forte</span>:", "che cosa fare"], sotto: "Cadono <b>rami, tegole e vasi</b>.",
      sottotitolo: "Vento forte: che cosa fare. Le raffiche possono spezzare i rami e far cadere tegole e vasi." },
    { ill: "balcone", illh: 420, dur: 9.3, chip: "Prima",
      righe: ["Metti tutto", "al <span class='a'>riparo</span>"], sotto: "Vasi e sedie di balconi e davanzali: <b>dentro casa o fissati bene</b>.",
      sottotitolo: "Prima che arrivi il vento, metti al riparo o fissa bene vasi, sedie e tutto quello che sta su balconi e davanzali." },
    { ill: "parcheggio", illh: 420, dur: 7.1, chip: "Prima di uscire",
      righe: ["Guarda", "l'<span class='a'>allerta</span>"], sotto: "Parcheggia <b>lontano da alberi e impalcature</b>.",
      sottotitolo: "Guarda l'allerta del giorno, e parcheggia l'auto lontano da alberi e impalcature." },
    { ill: "casa", illh: 420, dur: 8.6, chip: "Durante",
      righe: ["Resta", "in <span class='a'>casa</span>"], sotto: "Chiudi tutto e <b>stai lontano dai vetri</b>.",
      sottotitolo: "Quando il vento soffia forte, resta in casa se puoi. Chiudi porte e finestre, e stai lontano dai vetri." },
    { ill: "fuori", illh: 240, dur: 12.3, chip: "Se sei fuori",
      get listaAt() { return ["i parchi", "impalcature", "cartelloni", "cornicioni"].map(p => quando(4, p) - .5); },
      righe: ["Lontano", "dagli <span class='a'>alberi</span>"], lista: [
        ["alberi", "Parchi e strade alberate"],
        ["impalcatura", "Impalcature"],
        ["cartellone", "Cartelloni"],
        ["cornicione", "Cornicioni"] ],
      sottotitolo: "Se sei fuori, evita i parchi e le strade alberate: i rami che si spezzano sono il pericolo più frequente. Stai lontano da impalcature, cartelloni e cornicioni." },
    { ill: "strada", illh: 420, dur: 9.0, chip: "In auto o in moto",
      righe: ["In strada", "<span class='a'>rallenta</span>"], sotto: "Le raffiche fanno sbandare <b>all'uscita delle gallerie e sui viadotti</b>.",
      sottotitolo: "In auto o in moto rallenta: le raffiche fanno sbandare, soprattutto all'uscita delle gallerie e sui viadotti." },
    { ill: "dopo", illh: 200, dur: 9.2, chip: "Genzano di Roma · Protezione Civile", finale: true,
      righe: ["Cavi a terra:", "<span class='a'>non toccare</span>"], sotto: "<b>protezionecivilegenzano.it</b>",
      grande: "112", fonte: "Fonte: Dipartimento della Protezione Civile,<br>«Cosa fare in caso di venti e mareggiate»",
      sottotitolo: "Dopo il vento, non toccare i cavi caduti a terra. Se un albero o un cavo blocca la strada, chiama il 112." }
  ]
};
/* secondi dall'inizio della scena k in cui la voce pronuncia `parola` (in proporzione ai caratteri della frase) */
function quando(k, parola) {
  const s = CONFIG.scene[k], D = (DUR.length && DUR[k] != null) ? DUR[k] + 1.2 : s.dur;
  const i = Math.max(0, s.sottotitolo.indexOf(parola));
  return .45 + (D - 1.2) * i / s.sottotitolo.length;
}
