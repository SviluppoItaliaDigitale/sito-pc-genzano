/* ===================== DISEGNI (originali, stile pennarello) ===================== */
/* albero a chioma tonda, origine ai piedi: si piega con skewX (vedi piega() nelle animazioni) */
const ALB = (cls, c = "#40c057") => `<g class="${cls}" ${O}><path d="M-10 0 L-7 -92 H7 L10 0Z" fill="#a0703c"/>
  <path d="M-60 -90 Q-86 -130 -50 -150 Q-52 -198 0 -198 Q52 -200 54 -150 Q88 -128 60 -90 Q30 -68 0 -84 Q-30 -68 -60 -90Z" fill="${c}"/>
  <path d="M-26 -128 q10 -12 22 0 M10 -150 q10 -12 22 0" fill="none" stroke-width="4"/></g>`;
const SOFFI = (cls, n = 4, c = "#4dabf7") => `<g class="${cls}" fill="none" stroke="${c}" stroke-width="6" stroke-linecap="round">${Array.from({ length: n }, (_, i) =>
  `<path data-i="${i}" d="M0 0 h64 q20 0 20 -15 q0 -13 -13 -13" opacity="0"/>`).join("")}</g>`;
const FOGLIE = (cls, n = 8) => `<g class="${cls}" stroke="${INK}" stroke-width="2.5" stroke-linejoin="round">${Array.from({ length: n }, (_, i) =>
  `<path data-i="${i}" d="M-10 0 q10 -11 20 0 q-10 11 -20 0Z" fill="${["#40c057", "#f59f00", "#82c91e", "#e8590c"][i % 4]}" opacity="0"/>`).join("")}</g>`;
const VASO = (cls, fiore = "#f783ac") => `<g class="${cls}"><g ${O} stroke-width="4"><path d="M-3 -24 Q-22 -44 -8 -56 Q0 -46 0 -30 Q4 -52 18 -54 Q22 -38 3 -24Z" fill="#40c057"/>
  <circle cx="-9" cy="-56" r="7" fill="${fiore}"/><circle cx="17" cy="-55" r="7" fill="${fiore}"/>
  <path d="M-17 -24 H17 L11 0 H-11Z" fill="#e8590c"/><rect x="-20" y="-30" width="40" height="9" rx="3" fill="#ff922b"/></g></g>`;
const TEGOLA = cls => `<g class="${cls}"><path d="M-24 -6 Q0 -18 24 -6 V7 Q0 -5 -24 7Z" fill="#e8590c" ${O} stroke-width="4"/></g>`;
const BOTTO = (cls, x, y) => `<g class="${cls}" transform="translate(${x} ${y})"><g fill="none" stroke="#e8590c" stroke-width="6" stroke-linecap="round">${[0, 1, 2, 3, 4, 5, 6].map(i =>
  `<path d="M0 -16 V-34" transform="rotate(${-78 + i * 26})"/>`).join("")}</g></g>`;
const SEDIA = `<g ${O} stroke-width="4"><path d="M-20 0 V-44 M20 0 V-44 M-20 -44 V-92" fill="none" stroke-width="6"/><rect x="-25" y="-50" width="50" height="10" rx="4" fill="#4dabf7"/>
  <rect x="-26" y="-94" width="12" height="40" rx="5" fill="#4dabf7"/></g>`;
const AUTO = (cls, c = "#ff8787") => `<g class="${cls}"><g transform="translate(-50 -81)" ${O}><path d="M8 68 V52 L22 32 H66 L84 52 H92 V68Z" fill="${c}"/><path d="M28 36 H62 L74 50 H22Z" fill="#d0ebff"/>
  <circle cx="28" cy="70" r="11" fill="#495057"/><circle cx="72" cy="70" r="11" fill="#495057"/><circle cx="89" cy="58" r="3.5" fill="#ffd43b" stroke-width="2"/></g></g>`;
const MOTO = cls => `<g class="${cls}"><g ${O} stroke-width="4"><path d="M-24 -13 L-6 -32 H14 L26 -13 M14 -32 L22 -50 H30" fill="none" stroke-width="6"/>
  <rect x="-16" y="-42" width="32" height="13" rx="6" fill="#e03131"/>
  <path d="M-8 -42 L0 -68 L14 -62 L20 -50" fill="none" stroke="#4263eb" stroke-width="13"/>
  <circle cx="2" cy="-80" r="12" fill="#ffd43b"/><path d="M6 -84 H14 V-77 H6Z" fill="#343a40" stroke-width="2"/>
  <circle cx="-24" cy="-13" r="13" fill="#495057"/><circle cx="26" cy="-13" r="13" fill="#495057"/></g></g>`;
const FUMETTO112 = `<g class="fum"><g><rect x="-58" y="-28" width="116" height="56" rx="24" fill="#fff" ${O}/><text x="0" y="14" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="36" fill="#e03131">112</text></g></g>`;
const CELL = `<g class="cell"><rect x="-16" y="-30" width="32" height="56" rx="7" fill="#495057" ${O}/></g>`;
const MANO = `<g stroke="${INK}" stroke-width="3" stroke-linejoin="round" fill="#ffd8b1"><rect x="-17" y="-28" width="7.5" height="26" rx="3.7"/><rect x="-8.5" y="-33" width="7.5" height="31" rx="3.7"/>
  <rect x="0" y="-33" width="7.5" height="31" rx="3.7"/><rect x="8.5" y="-28" width="7.5" height="26" rx="3.7"/><rect x="-17" y="-8" width="33" height="32" rx="11"/>
  <rect x="12" y="-2" width="16" height="8" rx="4" transform="rotate(-35 12 2)"/></g>`;
const NON_TOCCARE = (cls, x, y, r = 50) => `<g class="${cls}" transform="translate(${x} ${y})"><g><circle r="${r}" fill="#fff" stroke="#e03131" stroke-width="${r * .26}"/>${MANO}
  <path d="M${-r * .66} ${r * .66} L${r * .66} ${-r * .66}" stroke="#e03131" stroke-width="${r * .24}"/><circle r="${r * 1.13}" fill="none" stroke="${INK}" stroke-width="4"/></g></g>`;
Object.assign(ICONE, {
  alberi: `<svg viewBox="0 0 100 100"><rect x="26" y="52" width="9" height="38" fill="#a0703c" ${O}/><circle cx="30" cy="40" r="22" fill="#40c057" ${O}/><rect x="64" y="58" width="9" height="32" fill="#a0703c" ${O}/><circle cx="68" cy="48" r="19" fill="#82c91e" ${O}/></svg>`,
  impalcatura: `<svg viewBox="0 0 100 100"><path d="M22 94 V8 M78 94 V8 M22 66 L78 40 M22 40 L78 14" fill="none" ${O}/><rect x="12" y="36" width="76" height="9" rx="2" fill="#e9b872" ${O}/><rect x="12" y="64" width="76" height="9" rx="2" fill="#e9b872" ${O}/></svg>`,
  cartellone: `<svg viewBox="0 0 100 100"><path d="M30 56 V94 M70 56 V94" ${O}/><rect x="10" y="12" width="80" height="46" rx="5" fill="#fff" ${O}/><circle cx="32" cy="35" r="11" fill="#ffd43b" stroke="none"/><path d="M52 28 H80 M52 42 H72" stroke="#4dabf7" stroke-width="7" stroke-linecap="round"/></svg>`,
  cornicione: `<svg viewBox="0 0 100 100"><rect x="14" y="30" width="50" height="64" fill="#ffe066" ${O}/><rect x="6" y="16" width="66" height="15" rx="3" fill="#ced4da" ${O}/><rect x="28" y="48" width="20" height="24" fill="#a5d8ff" ${O}/><path d="M76 44 L92 50 L84 64Z" fill="#ced4da" ${O}/><path d="M80 26 V36 M90 30 V40" stroke="#e8590c" stroke-width="5" stroke-linecap="round"/></svg>`
});
const RINGHIERA = `<g ${O}><rect x="-10" y="400" width="620" height="18" fill="#ced4da"/><path d="${Array.from({ length: 17 }, (_, i) => `M${14 + i * 36} 312 V400`).join(" ")}" fill="none" stroke-width="6"/><rect x="-10" y="298" width="620" height="14" rx="4" fill="#495057"/></g>`;
const ILL = {
  /* 1 — alberi piegati, foglie in volo, una tegola e un vaso che cadono */
  titolo: () => `<svg ${S0}><rect width="600" height="510" fill="#d8ecff"/>${NUVOLA(210, 26, .55)}${SOFFI("soffi", 5)}${PRATO(446, "#8ce99a")}
    <g ${O}><rect x="408" y="232" width="210" height="216" fill="#ffe066"/><path d="M384 238 L504 148 L640 238Z" fill="#fa5252"/>
      <path d="M428 222 q10 -9 20 0 M462 198 q10 -9 20 0 M496 174 q10 -9 20 0 M520 214 q10 -9 20 0" fill="none" stroke-width="4"/>
      <rect x="446" y="286" width="76" height="70" fill="#a5d8ff"/><path d="M484 286 V356" /><rect x="438" y="356" width="92" height="11" rx="3" fill="#ced4da"/>
      <rect x="548" y="350" width="60" height="98" fill="#c08a4f"/></g>
    ${ALB("a1")}${ALB("a2", "#69db7c")}${BOTTO("b1", 398, 440)}${BOTTO("b2", 470, 440)}${TEGOLA("teg")}${VASO("vaso")}${FOGLIE("foglie", 9)}${PG("flavio")}</svg>`,
  /* 2 — balcone: un vaso in casa, sedia e vaso legati alla ringhiera, il vaso del davanzale dentro */
  balcone: () => `<svg ${S0}><rect width="600" height="510" fill="#ffe8cc"/><path d="M0 60 H600 M0 200 H40 M200 200 H600" stroke="#f3c999" stroke-width="4"/><rect y="418" width="600" height="92" fill="#f3c999"/>
    <g ${O}><rect x="52" y="120" width="142" height="282" rx="6" fill="#fff"/><rect class="vano" x="64" y="132" width="118" height="270" fill="#2c5282"/>
      <rect x="396" y="92" width="150" height="150" rx="6" fill="#fff"/><rect x="408" y="104" width="126" height="126" fill="#2c5282"/>
      <g class="ante"><rect x="408" y="104" width="63" height="126" fill="#a5d8ff"/><rect x="471" y="104" width="63" height="126" fill="#a5d8ff"/><path d="M420 122 l14 16 M484 122 l14 16" stroke="#fff"/></g>
      <rect x="386" y="240" width="170" height="13" rx="3" fill="#ced4da"/></g>
    ${VASO("vD", "#ffd43b")}${VASO("vA")}<g class="sed" transform="translate(538 400)">${SEDIA}</g><g transform="translate(462 400) scale(1.45)">${VASO("vB", "#da77f2")}</g>
    ${PG("flavio")}${RINGHIERA}
    <path class="cinghia" d="M424 304 V352 Q424 372 444 372 H556 Q576 372 576 352 V304" fill="none" stroke="#f59f00" stroke-width="9" stroke-linecap="round" stroke-dasharray="330" stroke-dashoffset="330"/>
    ${SPUNTA("ok1", 186, 128, 26)}${SPUNTA("ok2", 578, 300, 26)}${SPUNTA("ok3", 548, 96, 24)}</svg>`,
  /* 3 — allerta del giorno; auto sotto l'albero (no), auto nello spazio libero (sì) */
  parcheggio: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(40, 20, .5)}
    <g ${O}><rect x="206" y="128" width="96" height="282" fill="#ffd8a8"/><rect x="226" y="150" width="26" height="34" fill="#a5d8ff"/><rect x="264" y="150" width="26" height="34" fill="#a5d8ff"/>
      <path d="M192 410 V150 M242 410 V150 M292 410 V150 M192 320 L242 240 M242 320 L292 240" fill="none"/><rect x="182" y="234" width="120" height="10" rx="2" fill="#e9b872"/><rect x="182" y="318" width="120" height="10" rx="2" fill="#e9b872"/></g>
    <rect x="-10" y="408" width="620" height="110" fill="#adb5bd" stroke="${INK}" stroke-width="5"/><path d="M398 500 V424 M590 500 V424" stroke="#fff" stroke-width="6" stroke-linecap="round"/>
    <g ${O}><path d="M566 408 V300"/><rect x="540" y="246" width="52" height="52" rx="8" fill="#1c7ed6"/></g><text x="566" y="286" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="38" fill="#fff">P</text>
    ${ALB("a1")}${AUTO("autoA")}${FOGLIE("foglie", 5)}${PG("flavio")}${AUTO("autoB", "#74c0fc")}
    <g class="avv" transform="translate(456 100)"><g><rect x="-122" y="-68" width="244" height="136" rx="22" fill="#fff" ${O}/><path class="barra" d="M-122 -24 V-46 Q-122 -68 -100 -68 H100 Q122 -68 122 -46 V-24Z" fill="#ffd43b" ${O}/>
      <text x="0" y="-33" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="28" fill="${INK}">ALLERTA</text>
      <text x="-24" y="34" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="30" fill="${INK}">oggi: vento</text>
      <path d="M68 16 h20 q12 0 12 -9 q0 -8 -8 -8 M68 32 h28 q12 0 12 9 q0 8 -8 8" fill="none" stroke="#4dabf7" stroke-width="6" stroke-linecap="round"/></g></g>
    ${DIVIETO("no", 150, 300, 50)}${SPUNTA("si", 478, 318, 38)}</svg>`,
  /* 4 — in casa: porta e finestra si chiudono, Flavio si allontana dai vetri */
  casa: () => `<svg ${S0}>${STANZA}<clipPath id="ven-vetro"><rect x="52" y="92" width="186" height="206"/></clipPath>
    <g ${O}><rect x="310" y="104" width="96" height="66" rx="4" fill="#fff"/><path d="M318 162 L344 128 L362 148 L376 136 L398 162Z" fill="#8ce99a" stroke-width="3"/><circle cx="384" cy="122" r="7" fill="#ffd43b" stroke-width="3"/></g>
    <rect x="40" y="80" width="210" height="230" rx="8" fill="#fff" ${O}/><rect x="52" y="92" width="186" height="206" fill="#cfe8ff"/>
    <g clip-path="url(#ven-vetro)"><path d="M40 270 Q150 250 250 274 V310 H40Z" fill="#8ce99a" stroke="${INK}" stroke-width="4"/>${ALB("a1", "#69db7c")}${FOGLIE("foglie", 6)}</g>
    <rect x="52" y="92" width="186" height="206" fill="none" ${O}/>
    <g class="antaS" ${O}><rect x="0" y="92" width="93" height="206" fill="#a5d8ff" fill-opacity=".6"/><path d="M0 195 H93 M16 112 l16 20" stroke="#fff"/><path d="M0 195 H93"/></g>
    <g class="antaD" ${O}><rect x="0" y="92" width="93" height="206" fill="#a5d8ff" fill-opacity=".6"/><path d="M0 195 H93"/></g>
    <rect x="30" y="308" width="230" height="14" rx="4" fill="#ced4da" ${O}/>
    <g ${O}><rect x="462" y="168" width="116" height="254" fill="#fff"/><rect x="474" y="180" width="92" height="242" fill="#cfe8ff"/></g>
    <g class="porta" ${O}><rect x="0" y="180" width="92" height="242" fill="#c08a4f"/><rect x="12" y="196" width="68" height="90" rx="4" fill="none" stroke-width="4"/><circle cx="78" cy="310" r="6" fill="#ffd43b" stroke-width="3"/></g>
    ${SOFFI("soffi", 3)}
    <g class="dist" fill="none" stroke="#40c057" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"><path d="M268 462 H368"/><path d="M344 442 L370 462 L344 482"/></g>
    ${PG("flavio")}${SPUNTA("ok", 410, 262, 28)}</svg>`,
  /* 5 — viale alberato: divieto, un ramo si spezza e cade; Flavio resta lontano */
  fuori: () => `<svg ${S0}><rect width="600" height="510" fill="#d8ecff"/>${NUVOLA(60, 22, .55)}${NUVOLA(400, 40, .5)}${SOFFI("soffi", 4)}
    <path d="M-10 372 H610 V520 H-10Z" fill="#8ce99a" stroke="${INK}" stroke-width="5"/><path d="M-10 404 H610 V520 H-10Z" fill="#e9d5bf" stroke="${INK}" stroke-width="5"/>
    <path d="M10 456 H590" stroke="#fff" stroke-width="6" stroke-dasharray="26 20"/>
    ${ALB("a1", "#69db7c")}${ALB("a2")}
    <g class="ramo"><g ${O}><path d="M0 0 L58 10" fill="none" stroke="#a0703c" stroke-width="11"/>
      <path d="M40 -14 Q66 -30 86 -8 Q104 8 84 26 Q60 36 42 22 Q28 8 40 -14Z" fill="#40c057"/></g></g>
    ${BOTTO("crac", 318, 248)}${FOGLIE("foglie", 7)}${PG("flavio")}${DIVIETO("no", 190, 262, 56)}</svg>`,
  /* 6 — uscita della galleria e viadotto: l'auto e la moto rallentano, la raffica le fa oscillare */
  strada: () => `<svg ${S0}><rect width="600" height="510" fill="#d0ebff"/>${NUVOLA(330, 24, .55)}
    <path d="M150 400 Q300 330 420 380 T620 350 V520 H150Z" fill="#b2f2bb" stroke="${INK}" stroke-width="4"/>
    <path d="M150 450 Q320 410 460 452 T620 440 V520 H150Z" fill="#8ce99a" stroke="${INK}" stroke-width="5"/><path d="M230 520 Q330 462 470 486 T620 470" fill="none" stroke="#74c0fc" stroke-width="16" stroke-linecap="round"/>
    <g ${O}><rect x="296" y="322" width="28" height="200" fill="#adb5bd"/><rect x="436" y="322" width="28" height="200" fill="#adb5bd"/><rect x="574" y="322" width="28" height="200" fill="#adb5bd"/>
      <rect x="140" y="300" width="480" height="24" fill="#ced4da"/><path d="M190 282 H620 M250 282 V300 M320 282 V300 M390 282 V300 M460 282 V300 M530 282 V300 M600 282 V300" fill="none" stroke-width="4"/></g>
    <g ${O}><path d="M232 300 V236"/><path d="M232 176 L266 236 H198Z" fill="#fff" stroke="#e03131" stroke-width="7"/><path d="M220 226 V208 M220 210 L246 214 L246 222 L220 220" fill="#e03131" stroke-width="3"/></g>
    <g ${O}><path d="M478 300 V206"/></g><g class="manica" transform="translate(478 212)"><g ${O} stroke-width="4"><path d="M0 -12 L70 -5 V5 L0 12Z" fill="#fff"/><path d="M0 -12 L18 -10 V10 L0 12Z M36 -8.5 L54 -6.5 V6.5 L36 8.5Z" fill="#e03131"/></g></g>
    ${MOTO("moto")}${AUTO("mac", "#ffa94d")}
    <path d="M-10 520 V150 Q50 84 120 140 Q172 184 188 300 V520Z" fill="#a9d18e" stroke="${INK}" stroke-width="5"/>
    <path d="M150 300 V238 Q150 208 176 208 H190 V300Z" fill="#343a40" stroke="${INK}" stroke-width="5"/><path d="M190 204 V300" stroke="#ced4da" stroke-width="9"/><path d="M190 204 V300" stroke="${INK}" stroke-width="2"/>
    <path d="M30 220 q14 -16 28 0 M84 180 q14 -16 28 0 M70 300 q14 -16 28 0" fill="none" stroke="${INK}" stroke-width="4" stroke-linecap="round"/>
    ${SOFFI("soffi", 6, "#1c7ed6")}</svg>`,
  /* 7 — dopo: cavo a terra (non toccare), albero sulla strada, Flavio chiama il 112 */
  dopo: () => `<svg ${S0}><rect width="600" height="510" fill="#d8ecff"/>${NUVOLA(250, 40, .5)}${NUVOLA(470, 110, .45)}
    <path d="M-10 366 H610 V520 H-10Z" fill="#adb5bd" stroke="${INK}" stroke-width="5"/><path d="M10 446 H590" stroke="#fff" stroke-width="6" stroke-dasharray="26 20"/>
    <g ${O}><rect x="58" y="96" width="16" height="274" fill="#a0703c"/><rect x="36" y="112" width="60" height="11" rx="3" fill="#a0703c"/><path d="M40 117 Q10 142 -14 132" fill="none" stroke="#343a40"/></g>
    <path d="M92 117 Q124 236 108 330 Q102 366 146 362 Q196 354 232 366" fill="none" stroke="#343a40" stroke-width="7" stroke-linecap="round"/>
    <g class="scint" fill="#ffd43b" stroke="${INK}" stroke-width="2.5" stroke-linejoin="round">${[[244, 352], [256, 372], [236, 338]].map(([x, y], i) => `<path data-i="${i}" d="M0 -11 L3 -3 L11 0 L3 3 L0 11 L-3 3 L-11 0 L-3 -3Z" transform="translate(${x} ${y})"/>`).join("")}</g>
    <g ${O}><path d="M430 372 L436 344 L560 330 L566 372Z" fill="#a0703c"/><path d="M430 372 L412 352 M432 356 L416 334 M440 346 L434 322" fill="none" stroke="#a0703c" stroke-width="8"/>
      <path d="M520 360 Q486 330 512 296 Q508 250 560 250 Q600 240 620 280 V384 Q560 396 520 360Z" fill="#40c057"/><path d="M548 300 q10 -12 22 0 M560 340 q10 -12 22 0" fill="none" stroke-width="4"/></g>
    <g class="att"><g>${ICOSVG("pericolo", 0, 0, .62)}</g></g>
    ${PG("flavio")}${CELL}${FUMETTO112}${NON_TOCCARE("nt", 196, 236, 48)}</svg>`
};
