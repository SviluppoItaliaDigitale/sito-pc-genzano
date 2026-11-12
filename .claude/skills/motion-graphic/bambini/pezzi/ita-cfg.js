/* ===================== CONFIG — testi, tempi ===================== */
/* Fonti: it-alert.gov.it, pagine «Come funziona», «Messaggi», «Quando si usa» e «Domande frequenti»,
   verificate il 12/11/2026; registro data/dati_canonici.yaml (voci it-alert-*).
   Il riquadro sul telefono è un avviso generico disegnato per il video: non riproduce la grafica del messaggio vero.
   I tempi delle scene («dur») sono stime (circa 15 caratteri al secondo + 1,7 s) finché manca durate.json:
   le animazioni usano frazioni della scena e si adattano da sole alle durate vere (vedi «voce()» nei disegni). */
const CONFIG = {
  titolo: "IT-alert: il messaggio che avvisa del pericolo",
  hud: "IT-ALERT",
  posterT: 0,
  scene: [
    { ill: "avviso", illh: 520, dur: 8.2, chip: "Protezione Civile · Genzano di Roma",
      righe: ["<span class='a'>IT-alert</span>:", "il messaggio", "che avvisa"], sotto: "<b>Il sistema di allarme pubblico italiano.</b>",
      sottotitolo: "IT-alert: il messaggio che avvisa di un grave pericolo. È il sistema di allarme pubblico italiano." },
    { ill: "zona", illh: 420, dur: 10, chip: "A chi arriva",
      righe: ["Ai telefoni", "<span class='a'>nella zona</span>"], sotto: "Tutti quelli accesi. <b>Niente app, niente iscrizione.</b>",
      sottotitolo: "Arriva su tutti i telefoni accesi che si trovano nella zona del pericolo. Non serve scaricare un'app, e non serve iscriversi." },
    { ill: "suono", illh: 420, dur: 10, chip: "Come si riconosce",
      righe: ["Un suono", "<span class='a'>diverso</span>"], sotto: "Sullo schermo, un testo che comincia con <b>IT-alert</b>.",
      sottotitolo: "Il telefono fa un suono diverso dalle solite suonerie, e sullo schermo compare un testo che comincia con la scritta IT-alert." },
    { ill: "casi", illh: 240, dur: 12.5, chip: "Quando si usa",
      righe: ["Poche", "emergenze <span class='a'>gravi</span>"], lista: [
        ["fabbrica", "Incidente in uno stabilimento industriale"],
        ["nucleare", "Incidente nucleare"],
        ["diga", "Crollo di una grande diga"],
        ["vulcano", "Attività di alcuni vulcani"] ],
      sottotitolo: "Si usa per poche emergenze gravi: un incidente in uno stabilimento industriale, un incidente nucleare, il crollo di una grande diga, l'attività di alcuni vulcani." },
    { ill: "nonsi", illh: 420, dur: 10.1, chip: "Quando non si usa",
      righe: ["Terremoti", "e meteo: <span class='a'>no</span>"], sotto: "Per il maltempo: <b>il colore dell'allerta</b> sul sito del Gruppo.",
      sottotitolo: "Non si usa per i terremoti e nemmeno per le allerte meteo. Per il maltempo, guarda il colore dell'allerta sul sito del Gruppo." },
    { ill: "passi", illh: 420, dur: 7.7, chip: "Se lo ricevi",
      righe: ["Fermati", "e <span class='a'>leggi tutto</span>"], sotto: "Poi <b>segui le indicazioni</b> delle autorità.",
      sottotitolo: "Se lo ricevi, fermati e leggi tutto il messaggio. Poi segui le indicazioni delle autorità." },
    { ill: "prova", illh: 200, dur: 9.2, chip: "Genzano di Roma · Protezione Civile", finale: true,
      righe: ["<span class='a'>TEST</span>:", "solo una prova"], sotto: "<b>protezionecivilegenzano.it</b>",
      grande: "112", fonte: "Fonte: it-alert.gov.it,<br>Dipartimento della Protezione Civile",
      sottotitolo: "Se il messaggio comincia con la parola TEST, è solo una prova: non devi fare niente. In emergenza chiama il 112." }
  ]
};
