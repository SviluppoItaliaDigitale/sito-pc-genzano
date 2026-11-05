/* ===================== CONFIG — testi, tempi ===================== */
/* Fonti: pagina /allerte-meteo/ del sito (cosa fare per ogni colore); data/codici_colore.yaml; Genzano di Roma =
   zona di allerta F (registro data/dati_canonici.yaml); bollettini del Centro Funzionale della Regione Lazio. */
const CONFIG = {
  titolo: "I colori dell'allerta meteo",
  hud: "ALLERTA",
  posterT: 0,
  scene: [
    { ill: "semaforo", illh: 520, dur: 5, chip: "Protezione Civile · Genzano di Roma",
      righe: ["I colori", "dell'<span class='a'>allerta</span>"], sotto: "<b>Verde, giallo, arancione, rosso.</b>",
      sottotitolo: "Verde, giallo, arancione, rosso: i colori dell'allerta meteo." },
    { ill: "zone", illh: 420, dur: 7, chip: "Ogni giorno",
      righe: ["Un colore", "per ogni <span class='a'>zona</span>"], sotto: "Lo dà la Regione Lazio. Genzano è nella <b>zona F</b>.",
      sottotitolo: "Ogni giorno la Regione Lazio guarda le previsioni e dà un colore a ogni zona. Genzano è nella zona F." },
    { ill: "verde", illh: 420, dur: 6, chip: "Verde",
      righe: ["Nessuna", "<span class='a'>allerta</span>"], sotto: "Niente di speciale: <b>resta informato</b>.",
      sottotitolo: "Verde: nessuna allerta. Non serve fare niente di speciale: resta informato." },
    { ill: "gialla", illh: 420, dur: 8, chip: "Allerta gialla",
      righe: ["Stai", "<span class='a'>attento</span>"], sotto: "Lontano da <b>fossi, torrenti e sottopassi</b>.",
      sottotitolo: "Gialla: in alcuni posti pioggia e temporali possono essere forti. Stai lontano da fossi, torrenti e sottopassi." },
    { ill: "arancione", illh: 420, dur: 8, chip: "Allerta arancione",
      righe: ["Esci solo", "se <span class='a'>serve</span>"], sotto: "E il <b>kit di emergenza</b> è pronto.",
      sottotitolo: "Arancione: fenomeni diffusi e pericolosi. Si esce solo se serve, e il kit di emergenza è pronto." },
    { ill: "rossa", illh: 260, dur: 9, chip: "Allerta rossa", listaAt: [2.5, 5.0, 7.9],
      righe: ["Resta", "al <span class='a'>sicuro</span>"], lista: [
        ["casa", "Non uscire se non serve"],
        ["cantina", "Lontano da cantine e strade allagate"],
        ["comune", "Segui le autorità"] ],
      sottotitolo: "Rossa: fenomeni molto forti. Non uscire se non è necessario, stai lontano da cantine e strade allagate, e segui le autorità." },
    { ill: "sito", illh: 420, dur: 6, chip: "Dove si guarda",
      righe: ["Guardalo", "<span class='a'>insieme</span>"], sotto: "Il colore di oggi è sul <b>sito del Gruppo</b>.",
      sottotitolo: "Il colore di oggi si trova sul sito del Gruppo. Guardatelo insieme, in famiglia." },
    { ill: "fine", illh: 200, dur: 6, chip: "Genzano di Roma · Protezione Civile", finale: true,
      righe: ["Ogni colore,", "i suoi <span class='a'>gesti</span>"], sotto: "<b>protezionecivilegenzano.it</b>",
      grande: "112", fonte: "Fonti: pagina «Allerte meteo» del sito;<br>Centro Funzionale della Regione Lazio",
      sottotitolo: "Ogni colore ha i suoi gesti. In emergenza chiama il 112." }
  ]
};
