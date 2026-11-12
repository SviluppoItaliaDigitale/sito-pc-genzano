/* ===================== DISEGNI (originali, stile pennarello) ===================== */
/* Tempi legati alla voce, non a secondi fissi: voce(D, f) è l'istante della scena in cui la voce è alla frazione f
   della frase; quando(k, "parole") lo calcola dal punto in cui quelle parole stanno nel sottotitolo della scena k.
   Vale con le durate stimate («dur») e con quelle vere di durate.json. */
const voce = (D, f) => .45 + Math.max(0, D - 1.2) * f;
const DS = k => (DUR.length && DUR[k] != null) ? DUR[k] + 1.2 : CONFIG.scene[k].dur;
const quando = (k, parole) => { const s = CONFIG.scene[k].sottotitolo; return voce(DS(k), Math.max(0, s.lastIndexOf(parole)) / s.length); };
CONFIG.scene[3].listaAt = ["un incidente in uno", "un incidente nucleare", "il crollo", "l'attività"].map(p => +(quando(3, p) - .15).toFixed(2));

Object.assign(ICONE, {
  fabbrica: `<svg viewBox="0 0 100 100"><rect x="64" y="20" width="16" height="42" fill="#e8590c" ${O}/><circle cx="76" cy="10" r="7" fill="#dee2e6" stroke="${INK}" stroke-width="4"/><circle cx="88" cy="16" r="5" fill="#dee2e6" stroke="${INK}" stroke-width="4"/>
    <path d="M8 90 V56 L30 68 V56 L52 68 V56 H92 V90Z" fill="#ffc078" ${O}/><rect x="18" y="74" width="12" height="10" fill="#fff" stroke="${INK}" stroke-width="3"/><rect x="40" y="74" width="12" height="10" fill="#fff" stroke="${INK}" stroke-width="3"/><rect x="66" y="70" width="14" height="20" fill="#495057" stroke="${INK}" stroke-width="3"/></svg>`,
  nucleare: `<svg viewBox="0 0 100 100"><circle cx="42" cy="12" r="8" fill="#fff" stroke="${INK}" stroke-width="4"/><circle cx="58" cy="9" r="7" fill="#fff" stroke="${INK}" stroke-width="4"/>
    <path d="M26 92 Q40 56 32 22 H68 Q60 56 74 92Z" fill="#dee2e6" ${O}/><circle cx="50" cy="64" r="15" fill="#ffd43b" stroke="${INK}" stroke-width="4"/>
    <g stroke="${INK}" stroke-width="7" stroke-linecap="butt"><path d="M50 60 V52"/><path d="M53.5 66 L60.4 70"/><path d="M46.5 66 L39.6 70"/></g><circle cx="50" cy="64" r="2.6" fill="${INK}"/></svg>`,
  diga: `<svg viewBox="0 0 100 100"><path d="M6 42 H52 V88 H6Z" fill="#74c0fc" ${O}/><path d="M12 54 q6 -6 12 0 t12 0" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>
    <path d="M48 24 H66 L82 88 H48Z" fill="#adb5bd" ${O}/><path d="M57 32 L63 46 L55 56 L65 70 L60 82" fill="none" stroke="#e03131" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M4 88 H96" ${O}/><path d="M86 62 q5 8 0 12 q-5 -4 0 -12Z" fill="#74c0fc" stroke="${INK}" stroke-width="3"/></svg>`,
  vulcano: `<svg viewBox="0 0 100 100"><circle cx="48" cy="16" r="10" fill="#ced4da" stroke="${INK}" stroke-width="4"/><circle cx="62" cy="9" r="7" fill="#ced4da" stroke="${INK}" stroke-width="4"/>
    <path d="M6 90 L38 36 H62 L94 90Z" fill="#a0703c" ${O}/><path d="M38 36 H62 L58 56 Q50 46 44 60Z" fill="#ff922b" ${O}/></svg>`
});

/* telefono generico (origine al centro) e riquadro di avviso inventato per il video */
const ITEL = (cls, schermo = "") => `<g class="${cls}"><g ${O}><rect x="-80" y="-160" width="160" height="320" rx="26" fill="#495057"/>
  <rect x="-68" y="-130" width="136" height="250" rx="8" fill="#e7f5ff"/><rect x="-22" y="-149" width="44" height="7" rx="3.5" fill="#868e96" stroke="none"/><circle cx="0" cy="140" r="9" fill="#868e96" stroke="none"/></g>${schermo}</g>`;
const AVVISO = (cls, parola = "IT-alert") => `<g class="${cls}"><g>
  <rect x="-60" y="-114" width="120" height="204" rx="14" fill="#fff" ${O}/>
  <path d="M0 -104 L24 -62 H-24Z" fill="#ffd43b" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/><path d="M0 -90 V-77" stroke="${INK}" stroke-width="5" stroke-linecap="round"/><circle cx="0" cy="-69" r="2.8" fill="${INK}"/>
  <rect class="evid" x="-53" y="-52" width="106" height="32" rx="7" fill="#ffe066"/>
  <text x="0" y="-27" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="25" fill="${INK}">${parola}</text>
  ${[-4, 14, 32, 50, 68].map((y, i) => `<rect class="riga" data-i="${i}" x="-48" y="${y}" width="${[96, 86, 96, 78, 54][i]}" height="8" rx="4" fill="${INK}" opacity=".4"/>`).join("")}</g></g>`;
const TREMA = (cls, col = "#ff922b") => `<g class="${cls}" fill="none" stroke="${col}" stroke-width="8" stroke-linecap="round">
  ${[0, 1, 2].map(i => `<path data-i="${i}" d="M${98 + i * 22} ${-34 - i * 18} q${12 + i * 5} ${34 + i * 18} 0 ${68 + i * 36}"/><path data-i="${i}" d="M${-98 - i * 22} ${-34 - i * 18} q${-12 - i * 5} ${34 + i * 18} 0 ${68 + i * 36}"/>`).join("")}</g>`;
const MINITEL = (cls, x, y) => `<g class="${cls}" transform="translate(${x} ${y})"><rect x="-11" y="-19" width="22" height="38" rx="5" fill="#495057" stroke="${INK}" stroke-width="4"/><rect class="lcd" x="-7" y="-14" width="14" height="25" rx="2" fill="#a5d8ff"/>
  <g class="seg"><g><path d="M0 -62 L17 -32 H-17Z" fill="#ffd43b" stroke="${INK}" stroke-width="4" stroke-linejoin="round"/><path d="M0 -52 V-43" stroke="${INK}" stroke-width="4" stroke-linecap="round"/><circle cx="0" cy="-37.5" r="2" fill="${INK}"/></g></g></g>`;
/* divieto «trasparente»: lascia vedere il disegno che sta sotto */
const NO = (cls, x, y, r = 40, k = .24) => { const w = r * k, b = r * .68; return `<g class="${cls}" transform="translate(${x} ${y})"><g fill="none" stroke-linecap="round">
  <circle r="${r}" stroke="${INK}" stroke-width="${w + 8}"/><path d="M${-b} ${b} L${b} ${-b}" stroke="${INK}" stroke-width="${w + 8}"/>
  <circle r="${r}" stroke="#e03131" stroke-width="${w}"/><path d="M${-b} ${b} L${b} ${-b}" stroke="#e03131" stroke-width="${w}"/></g></g>`; };
const NUMERO = (cls, x, y, n) => `<g class="${cls}" transform="translate(${x} ${y})"><g><circle r="21" fill="#ffd43b" stroke="${INK}" stroke-width="5"/><text x="0" y="10" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="28" fill="${INK}">${n}</text></g></g>`;
const ETI = (x, y, w, testo) => `<rect x="${x - w / 2}" y="${y - 21}" width="${w}" height="30" rx="15" fill="#fff" stroke="${INK}" stroke-width="3"/><text x="${x}" y="${y}" text-anchor="middle" font-family="Titillium Web" font-weight="800" font-size="19" fill="${INK}">${testo}</text>`;
const TXT = (x, y, s, testo, peso = 800, col = INK) => `<text x="${x}" y="${y}" text-anchor="middle" font-family="Titillium Web" font-weight="${peso}" font-size="${s}" fill="${col}">${testo}</text>`;
const LIVELLI = [["#40c057", "verde"], ["#ffd43b", "giallo"], ["#ff922b", "arancione"], ["#e03131", "rosso"]];

const ILL = {
  avviso: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(26, 36, .6)}${NUVOLA(440, 28, .5)}${PRATO(452)}
    <g class="vib">${TREMA("tr")}</g>${ITEL("tel", AVVISO("avv"))}${PG("flavio")}</svg>`,
  zona: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(150, 30, .5)}${PRATO(420)}
    <ellipse cx="350" cy="452" rx="238" ry="36" fill="#ffe066" opacity=".7"/><ellipse cx="350" cy="452" rx="238" ry="36" fill="none" stroke="#e8590c" stroke-width="5" stroke-dasharray="14 12" stroke-linecap="round"/>
    <g class="anelli" fill="none" stroke="#4dabf7" stroke-width="7">${[0, 1, 2, 3].map(i => `<circle data-i="${i}" cx="92" cy="142" r="20"/>`).join("")}</g>
    <g ${O}><path d="M70 418 L92 150 L114 418" fill="none"/><path d="M76 350 L108 350 M80 290 L104 290 M84 230 L100 230 M76 350 L104 290 M108 350 L80 290 M80 290 L100 230 M104 290 L84 230" fill="none" stroke-width="4"/><circle cx="92" cy="142" r="11" fill="#e03131"/></g>
    ${PG("flavio")}${PG("silvia", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}${PG("papa", { tipo: "adulto", maglia: "#40c057", pantaloni: "#495057", capelli: "#5c3d1e", pelle: "#f1c27d" })}
    ${MINITEL("t0", 284, 414)}${MINITEL("t1", 390, 414)}${MINITEL("t2", 504, 401)}
    <g class="b0" transform="translate(345 104)"><g><circle r="46" fill="#fff" ${O}/><rect x="-25" y="-25" width="50" height="50" rx="13" fill="#4dabf7" ${O}/><path d="M0 -13 V9 M-9 1 L0 10 L9 1" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></g></g>
    <g class="b1" transform="translate(495 104)"><g><circle r="46" fill="#fff" ${O}/><rect x="-20" y="-27" width="40" height="54" rx="5" fill="#fff4d6" ${O}/><path d="M-11 -13 H11 M-11 -1 H11 M-11 11 H3" stroke="${INK}" stroke-width="4" stroke-linecap="round"/></g></g>
    ${NO("n0", 345, 104, 46)}${NO("n1", 495, 104, 46)}
    <g class="e0"><g>${ETI(345, 186, 112, "niente app")}</g></g><g class="e1"><g>${ETI(495, 186, 172, "niente iscrizione")}</g></g></svg>`,
  suono: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>${NUVOLA(430, 30, .5)}${PRATO(455)}
    <g class="vib">${TREMA("tr", "#9775fa")}</g>
    ${ITEL("tel", `<g class="alt" ${O}><path d="M-34 -22 H-14 L12 -46 V34 L-14 10 H-34Z" fill="#9775fa"/><path d="M28 -30 q16 24 0 48" fill="none" stroke="#9775fa" stroke-width="8"/></g>${AVVISO("avv")}`)}
    ${PG("flavio")}</svg>`,
  casi: () => `<svg ${S0}><rect width="600" height="510" fill="#fff9db"/>${NUVOLA(60, 24, .5)}${NUVOLA(400, 40, .55)}${PRATO(378)}
    ${[["fabbrica", 215, 222], ["nucleare", 322, 262], ["diga", 429, 222], ["vulcano", 536, 262]].map(([n, x, y], j) =>
      `<circle cx="${x}" cy="${y}" r="48" fill="none" stroke="${INK}" stroke-width="4" stroke-dasharray="8 10" opacity=".3"/><g class="c${j}" transform="translate(${x} ${y})"><g><circle r="50" fill="#fff" ${O}/><g transform="translate(-35 -35) scale(.7)">${INTERNO(n)}</g></g></g>`).join("")}
    ${PG("flavio")}${MINITEL("t0", 134, 282)}</svg>`,
  nonsi: () => `<svg ${S0}><rect width="600" height="510" fill="#e7f5ff"/>${PRATO(462)}
    <g class="k0" transform="translate(152 132)"><g><rect x="-122" y="-100" width="244" height="200" rx="24" fill="#fff" ${O}/>
      <g class="casa" ${O}><g transform="scale(.82)"><path d="M-52 46 V-26 L0 -70 L52 -26 V46Z" fill="#ffe066"/><path d="M-62 -22 L0 -76 L62 -22" fill="none" stroke="#e03131" stroke-width="9"/><rect x="-12" y="8" width="24" height="38" fill="#c08a4f"/>
        <path d="M22 -30 L12 -8 L26 4 L16 28" fill="none" stroke-width="4"/></g></g>
      ${TXT(0, 86, 24, "Terremoto")}</g></g>
    <g class="k1" transform="translate(448 132)"><g><rect x="-122" y="-100" width="244" height="200" rx="24" fill="#fff" ${O}/>
      <g transform="translate(0 6) scale(.8)"><path d="M-58 -18 Q-62 -48 -32 -46 Q-24 -72 6 -62 Q26 -80 48 -58 Q74 -56 70 -28 Q82 -14 62 -6 H-50 Q-68 -6 -58 -18Z" fill="#adb5bd" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>
      <g class="gocce" stroke="#4dabf7" stroke-width="6" stroke-linecap="round">${[0, 1, 2, 3, 4, 5].map(i => `<path data-i="${i}" d="M0 0 l-6 16"/>`).join("")}</g></g>
      ${TXT(0, 86, 24, "Allerta meteo")}</g></g>
    ${NO("n0", 152, 116, 68, .15)}${NO("n1", 448, 116, 68, .15)}
    <g class="sito" transform="translate(352 368)"><g><rect x="-196" y="-106" width="392" height="212" rx="18" fill="#fff" ${O}/><path d="M-196 -70 H196" ${O}/>
      <circle cx="-174" cy="-88" r="5" fill="${INK}"/><circle cx="-156" cy="-88" r="5" fill="${INK}"/><rect x="-136" y="-100" width="290" height="24" rx="12" fill="#e7f5ff" stroke="${INK}" stroke-width="3"/>
      ${TXT(9, -82, 17, "protezionecivilegenzano.it", 700)}${TXT(0, -40, 22, "Il colore dell'allerta", 900)}
      ${LIVELLI.map(([c, n], i) => `<g class="col" data-i="${i}" transform="translate(${-132 + i * 88} 16)"><g><circle r="31" fill="#dee2e6" data-c="${c}" stroke="${INK}" stroke-width="5"/></g></g>${TXT(-132 + i * 88, 76, 17, n)}`).join("")}</g></g>
    ${PG("flavio")}</svg>`,
  passi: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(20, 30, .5)}${NUVOLA(450, 22, .45)}${PRATO(448)}
    ${ITEL("tel", AVVISO("avv"))}
    <g class="alt" transform="translate(98 236)"><g><path d="M-16 -38 H16 L38 -16 V16 L16 38 H-16 L-38 16 V-16Z" fill="#e03131" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>${TXT(0, 9, 26, "ALT", 900, "#fff")}</g></g>
    ${PG("flavio")}${PG("vol", { tipo: "adulta", maglia: "#ffd43b", pantaloni: "#1c4fa0", capelli: "#5c3d1e" })}
    <g class="fre" transform="translate(498 206)"><g><rect x="-62" y="-36" width="124" height="72" rx="26" fill="#fff" ${O}/><path d="M-10 34 L-2 56 L18 34" fill="#fff" ${O}/>
      <path d="M-34 0 H26 M6 -20 L28 0 L6 20" fill="none" stroke="${INK}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/><path d="M-34 0 H26 M6 -20 L28 0 L6 20" fill="none" stroke="#40c057" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></g></g>
    ${NUMERO("n1", 150, 208, 1)}${NUMERO("n2", 372, 122, 2)}${NUMERO("n3", 572, 176, 3)}</svg>`,
  prova: () => `<svg ${S0}><rect width="600" height="510" fill="#ebfbee"/>${NUVOLA(40, 22, .5)}${NUVOLA(430, 18, .5)}${PRATO(392)}
    ${ITEL("tel", AVVISO("avv", "TEST"))}${SPUNTA("ok", 216, 164, 30)}
    <g class="niente" transform="translate(420 150)"><g><rect x="-152" y="-27" width="304" height="54" rx="27" fill="#fff" ${O}/>${TXT(0, 9, 26, "Non devi fare niente", 900)}</g></g>
    ${PG("flavio")}${PG("silvia", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}</svg>`
};
