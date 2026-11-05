/* ===================== CONFIG — testi, tempi ===================== */
/* Fonti: pagina /rischi-prevenzione/rischio-vulcanico/ del sito; registro data/dati_canonici.yaml
   (ultima eruzione circa 36.000 anni fa, INGV; vulcano quiescente, DPC; sorveglianza INGV con GPS e
   misure dei gas). CO2: si accumula in cantine, scantinati, pozzi e fossi; aerare prima di entrare,
   non entrare nei pozzi, non soccorrere entrando in uno spazio chiuso, chiamare il 112. */
const CONFIG = {
  titolo: "Il vulcano dei Colli Albani",
  hud: "VULCANO",
  posterT: 0,
  scene: [
    { ill: "vulcano", illh: 520, dur: 6, chip: "Protezione Civile · Genzano di Roma",
      righe: ["Il vulcano", "sotto i <span class='a'>Castelli</span>"], sotto: "<b>I Colli Albani sono un vulcano.</b>",
      sottotitolo: "Genzano sorge su un vulcano: i Colli Albani. I laghi di Albano e di Nemi sono antichi crateri." },
    { ill: "dorme", illh: 420, dur: 7, chip: "Cosa sapere",
      righe: ["Quiescente,", "non <span class='a'>spento</span>"], sotto: "L'ultima eruzione è di <b>circa 36.000 anni fa</b>.",
      sottotitolo: "L'ultima eruzione è avvenuta circa 36.000 anni fa. Oggi il vulcano è quiescente: non è spento." },
    { ill: "sorveglia", illh: 420, dur: 7, chip: "Chi lo controlla",
      righe: ["Sempre", "<span class='a'>sorvegliato</span>"], sotto: "L'INGV misura <b>il suolo e i gas</b>, ogni giorno.",
      sottotitolo: "Lo sorveglia l'Istituto Nazionale di Geofisica e Vulcanologia, che misura i movimenti del suolo e i gas." },
    { ill: "gas", illh: 240, dur: 9, chip: "Il gas invisibile", listaAt: [4.6, 5.3, 6.0],
      righe: ["Un gas", "<span class='a'>invisibile</span>"], lista: [
        ["cantina", "Cantine e scantinati"],
        ["pozzo", "Pozzi"],
        ["fosso", "Fossi e buche"] ],
      sottotitolo: "Dal sottosuolo esce anidride carbonica: non ha colore né odore e si raccoglie nei posti bassi e chiusi." },
    { ill: "aria", illh: 420, dur: 7, chip: "Cosa fare",
      righe: ["Prima fai", "<span class='a'>cambiare l'aria</span>"], sotto: "Apri e aspetta. <b>Nei pozzi non si entra mai.</b>",
      sottotitolo: "Prima di entrare in una cantina chiusa da tempo, apri e fai cambiare l'aria. Nei pozzi non si entra mai." },
    { ill: "soccorso", illh: 420, dur: 8, chip: "Se qualcuno sta male",
      righe: ["Non entrare:", "chiama il <span class='a'>112</span>"], sotto: "Esci all'aria aperta. <b>Arrivano i Vigili del Fuoco.</b>",
      sottotitolo: "Se qualcuno sta male in un posto chiuso, non entrare a prenderlo: esci all'aria aperta e chiama il 112." },
    { ill: "sereno", illh: 200, dur: 7, chip: "Genzano di Roma · Protezione Civile", finale: true,
      righe: ["Informati", "dalle fonti <span class='a'>ufficiali</span>"], sotto: "<b>protezionecivilegenzano.it</b>",
      grande: "112", fonte: "Fonti: INGV, scheda «Colli Albani»;<br>Dipartimento della Protezione Civile",
      sottotitolo: "Segui le notizie dell'INGV, non le voci sui social. In emergenza chiama il 112." }
  ]
};
