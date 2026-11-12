/* ===================== DISEGNI (originali, stile pennarello) ===================== */
const CIELO = (c = "#c5d3e0") => `<rect width="600" height="510" fill="${c}"/>`;
const NERA = (x, y, s = 1, c = "#868e96", cls = "") => `<g class="${cls}" transform="translate(${x} ${y}) scale(${s})"><path d="M0 40 Q-4 10 26 12 Q34 -14 64 -4 Q84 -22 106 0 Q132 2 128 30 Q140 44 120 52 H8 Q-10 52 0 40Z" fill="${c}" stroke="${INK}" stroke-width="${(4 / s).toFixed(1)}" stroke-linejoin="round"/></g>`;
const PIOGGIA = (n = 26, x0 = 0, x1 = 600, y0 = 0, y1 = 440, cls = "pioggia") => `<g class="${cls}" stroke="#4dabf7" stroke-width="5" stroke-linecap="round" data-y0="${y0}" data-y1="${y1}">${Array.from({ length: n }, (_, i) =>
  `<path data-i="${i}" data-x="${(x0 + hash(i + 31) * (x1 - x0)).toFixed(0)}" d="M0 0 l-8 22"/>`).join("")}</g>`;
/* fulmine disegnato: la punta è nell'origine */
const SAETTA = (cls, x, y, s = 1) => `<g class="${cls}" transform="translate(${x} ${y}) scale(${s})" opacity="0"><path d="M42 -150 L4 -80 L28 -80 L0 0 L56 -98 L30 -98 L52 -150Z" fill="#ffd43b" stroke="${INK}" stroke-width="${(5 / s).toFixed(1)}" stroke-linejoin="round"/></g>`;
const TXT = (x, y, size, testo, fill = INK, extra = "") => `<text x="${x}" y="${y}" text-anchor="middle" font-family="Titillium Web" font-weight="900" font-size="${size}" fill="${fill}" ${extra}>${testo}</text>`;
const SI = `<circle cx="78" cy="78" r="20" fill="#40c057" ${O}/><path d="M68 78 L76 87 L89 70" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/>`;
const NO = `<circle cx="78" cy="78" r="19" fill="#fff" stroke="#e03131" stroke-width="7"/><path d="M66 90 L90 66" stroke="#e03131" stroke-width="7"/><circle cx="78" cy="78" r="23" fill="none" stroke="${INK}" stroke-width="3"/>`;
const I_PINO = `<rect x="43" y="66" width="14" height="26" fill="#a0703c" ${O}/><path d="M50 6 L80 70 H20Z" fill="#40c057" ${O}/>`;
const I_TRAL = `<path d="M40 14 L28 92 M60 14 L72 92 M40 14 H60 M18 30 H82 M36 46 H64 M32 68 H68 M36 46 L68 68 M64 46 L32 68 M32 68 L72 92 M68 68 L28 92" fill="none" stroke="#868e96" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/><path d="M40 14 L28 92 M60 14 L72 92 M18 30 H82" fill="none" ${O} stroke-width="3"/>`;
const I_RETE = `<path d="M14 26 V90 M50 26 V90 M86 26 V90" stroke="#868e96" stroke-width="9" stroke-linecap="round"/><path d="M14 40 H86 M14 72 H86 M14 72 L50 40 L86 72 M14 40 L50 72 L86 40" fill="none" ${O} stroke-width="4"/>`;
const I_ACQUA = `<path d="M50 10 C66 34 78 46 78 62 a28 28 0 0 1 -56 0 C22 46 34 34 50 10Z" fill="#74c0fc" ${O}/><path d="M38 62 a12 12 0 0 0 10 12" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round"/>`;
const I_TETT = `<path d="M8 40 L50 14 L92 40Z" fill="#ff8787" ${O}/><path d="M18 40 V90 M82 40 V90" ${O} stroke-width="6"/><path d="M34 50 l-5 14 M52 56 l-5 14 M68 50 l-5 14 M44 74 l-5 14" stroke="#4dabf7" stroke-width="5" stroke-linecap="round"/>`;
const POZZE = `<g fill="#74c0fc" ${O} stroke-width="4"><ellipse cx="150" cy="446" rx="72" ry="11"/><ellipse cx="430" cy="478" rx="56" ry="9"/></g>`;
const ico = inner => `<svg viewBox="0 0 100 100">${inner}</svg>`;
Object.assign(ICONE, {
  riparoCasa: ico(INTERNO("casa") + SI), riparoAuto: ico(INTERNO("auto") + SI), riparoNo: ico(I_TETT + NO),
  noAlbero: ico(I_PINO + NO), noPalo: ico(I_TRAL + NO), noRete: ico(I_RETE + NO), noAcqua: ico(I_ACQUA + NO)
});
const ILL = {
  temporale: () => `<svg ${S0}>${CIELO("#d0ebff")}<rect class="buio" width="600" height="510" fill="#3b4a66" opacity=".2"/>
    ${PIOGGIA(30, 60, 600, 150, 450)}
    <g class="colline"><path d="M-10 440 Q150 400 300 436 T610 430 V520 H-10Z" fill="#8ce99a" ${O}/></g>
    <g ${O}><rect x="430" y="356" width="96" height="84" fill="#ffe066"/><path d="M420 362 L478 316 L536 362Z" fill="#fa5252"/><rect x="464" y="392" width="28" height="48" fill="#c08a4f"/></g>
    ${SAETTA("saetta", 322, 420, 1.62)}
    <g class="nuvolone">${NERA(96, 22, 3.1, "#6c7785")}${NERA(40, 96, 1.5, "#868e96")}${NERA(388, 92, 1.4, "#868e96")}</g>
    <rect class="velo" width="600" height="510" fill="#fff" opacity="0"/>
    ${PG("flavio")}</svg>`,
  prima: () => `<svg ${S0}>${CIELO("#d0ebff")}${SOLE(505, 88, 40)}<rect class="buio" width="600" height="510" fill="#3b4a66" opacity="0"/>
    <g class="arriva">${NERA(0, 0, 2.3, "#6c7785")}</g>${PRATO(430)}
    <g ${O}><rect x="16" y="330" width="104" height="100" fill="#ffe066"/><path d="M6 336 L68 286 L130 336Z" fill="#fa5252"/><rect x="52" y="372" width="34" height="58" fill="#c08a4f"/></g>
    <g ${O} fill="none"><path d="M470 440 V320 H584 V440" stroke-width="9"/><path d="M470 440 V320 H584 V440" stroke="#fff" stroke-width="4"/><path d="M490 322 V438 M512 322 V438 M536 322 V438 M560 322 V438 M472 350 H582 M472 382 H582 M472 412 H582" stroke-width="2"/></g>
    <g class="palla"><circle r="17" fill="#fff" ${O}/><path d="M0 -8 L8 -2 L5 7 L-5 7 L-8 -2Z" fill="${INK}"/></g>
    ${PG("flavio")}${PG("silvia", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}
    ${POP("prev", 285, 150, `<rect x="-104" y="-84" width="208" height="168" rx="20" fill="#fff" ${O}/>${TXT(0, -50, 24, "PREVISIONI")}
      <g transform="translate(-52 -34) scale(.8)"><path d="M0 40 Q-4 10 26 12 Q34 -14 64 -4 Q84 -22 106 0 Q132 2 128 30 Q140 44 120 52 H8 Q-10 52 0 40Z" fill="#868e96" ${O}/><path d="M66 46 L50 72 H64 L54 96 L84 62 H68 L78 46Z" fill="#ffd43b" ${O} stroke-width="4"/></g>
      <rect class="barra" x="-86" y="42" width="172" height="32" rx="10" fill="#ffd43b" stroke="${INK}" stroke-width="4"/>${TXT(0, 66, 22, "ALLERTA")}`)}</svg>`,
  tuono: () => `<svg ${S0}>${CIELO()}${PIOGGIA(16, 0, 380, 120, 440)}
    <g class="onde" fill="none" stroke="${INK}" stroke-width="7" stroke-linecap="round">${[0, 1, 2].map(i => `<path data-i="${i}" d=""/>`).join("")}</g>
    ${NERA(18, 22, 2.2, "#6c7785")}${PRATO(440, "#8ce99a")}
    <g ${O}><rect x="398" y="196" width="220" height="250" fill="#ffe066"/><rect x="386" y="172" width="240" height="28" rx="6" fill="#fa5252"/>
      <rect x="428" y="318" width="76" height="128" rx="6" fill="#fff4d6"/><rect x="528" y="236" width="56" height="60" rx="6" fill="#ffe8a1"/><path d="M556 236 V296"/></g>
    ${POP("km", 232, 262, `<rect x="-124" y="-30" width="248" height="60" rx="22" fill="#fff" ${O}/>${TXT(0, 9, 25, "POCHI CHILOMETRI", "#c2410c")}`)}
    ${PG("flavio")}${SPUNTA("ok", 466, 258, 32)}</svg>`,
  riparo: () => `<svg ${S0}>${CIELO()}${NERA(30, 18, 1.5, "#6c7785")}${NERA(250, 34, 1.3)}${NERA(440, 12, 1.4, "#6c7785")}
    <rect x="-10" y="372" width="620" height="150" fill="#8ce99a" ${O}/>${POZZE}
    <g ${O}><rect x="34" y="204" width="150" height="168" fill="#ffe066"/><path d="M22 210 L109 138 L196 210Z" fill="#fa5252"/>
      <rect x="54" y="262" width="62" height="110" rx="6" fill="#fff4d6"/><rect x="132" y="236" width="38" height="42" rx="4" fill="#ffe8a1"/></g>
    ${PG("flavio")}
    <path d="M34 262 H54 V372 H34Z" fill="#ffe066" stroke="none"/><path d="M34 204 V372" ${O}/>
    ${POP("auto", 300, 326, `<g transform="scale(1.5) translate(-50 -50)">${INTERNO("auto")}</g>`)}
    <g ${O}><path d="M424 256 V372 M576 256 V372" stroke-width="7"/><path d="M404 258 L500 196 L596 258Z" fill="#ff8787"/><path d="M404 258 q12 16 24 0 q12 16 24 0 q12 16 24 0 q12 16 24 0 q12 16 24 0 q12 16 24 0 q12 16 24 0 q12 16 24 0" fill="#fff"/></g>
    ${PIOGGIA(34, 0, 620, 60, 372)}
    ${SPUNTA("ok1", 172, 170, 30)}${SPUNTA("ok2", 366, 262, 28)}${DIVIETO("no3", 500, 318, 40)}</svg>`,
  aperto: () => `<svg ${S0}>${CIELO()}${NERA(110, 14, 1.9, "#6c7785")}${NERA(400, 30, 1.3)}
    <rect x="-10" y="362" width="620" height="160" fill="#8ce99a" ${O}/>${POZZE}
    <ellipse cx="512" cy="372" rx="82" ry="13" fill="#74c0fc" ${O} stroke-width="4"/>
    <g class="rete" ${O}><path d="M400 300 V362 M440 300 V362 M480 300 V362" stroke="#868e96" stroke-width="9"/><path d="M400 300 V362 M440 300 V362 M480 300 V362" stroke-width="2"/>
      <path d="M400 312 H480 M400 348 H480 M400 348 L440 312 L480 348 M400 312 L440 348 L480 312" fill="none" stroke-width="3"/></g>
    <g class="tral" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M330 180 L312 362 M346 180 L364 362 M330 180 H346 M300 206 H376 M326 236 H350 M320 290 H356 M326 236 L356 290 M350 236 L320 290 M320 290 L364 362 M356 290 L312 362" stroke="${INK}" stroke-width="8"/>
      <path d="M330 180 L312 362 M346 180 L364 362 M330 180 H346 M300 206 H376 M326 236 H350 M320 290 H356 M326 236 L356 290 M350 236 L320 290 M320 290 L364 362 M356 290 L312 362" stroke="#ced4da" stroke-width="3"/>
      <path d="M376 206 Q480 232 610 200 M300 206 Q290 212 284 206" stroke="${INK}" stroke-width="3"/></g>
    <g class="pino" ${O}><rect x="206" y="322" width="18" height="40" fill="#a0703c"/><path d="M215 204 L262 330 H168Z" fill="#40c057"/></g>
    ${SAETTA("saetta", 215, 204, .62)}${PIOGGIA(30, 0, 620, 60, 362)}
    <rect class="velo" width="600" height="510" fill="#fff" opacity="0"/>
    ${PG("flavio")}
    ${DIVIETO("n0", 215, 286, 38)}${DIVIETO("n1", 338, 262, 24)}${DIVIETO("n2", 428, 322, 24)}${DIVIETO("n3", 548, 368, 22)}</svg>`,
  casa: () => `<svg ${S0}><defs><clipPath id="ful-fin"><rect x="34" y="56" width="132" height="132"/></clipPath></defs>${STANZA}
    <rect x="34" y="56" width="132" height="132" fill="#8fa3b8"/><g clip-path="url(#ful-fin)">${PIOGGIA(10, 40, 180, 50, 190)}</g>
    <g class="ante" ${O}><rect class="antaS" x="34" y="56" width="66" height="132" fill="#d0ebff"/><rect class="antaD" x="100" y="56" width="66" height="132" fill="#d0ebff"/></g>
    <rect x="28" y="50" width="144" height="144" rx="6" fill="none" ${O} stroke-width="9"/>
    <g ${O}><rect x="36" y="336" width="116" height="14" rx="5" fill="#c08a4f"/><path d="M52 350 V420 M136 350 V420" stroke-width="7"/>
      <rect x="58" y="308" width="72" height="28" rx="8" fill="#e03131"/><rect x="52" y="292" width="84" height="18" rx="9" fill="#e03131"/><path d="M130 322 q22 6 14 26" fill="none" stroke-width="4"/>
      <circle cx="94" cy="323" r="8" fill="#fff"/></g>
    <g ${O}><rect x="200" y="352" width="244" height="68" rx="8" fill="#c08a4f"/><path d="M322 352 V420"/>
      <rect x="214" y="238" width="136" height="100" rx="10" fill="#495057"/><rect class="tv" x="226" y="250" width="112" height="76" rx="4" fill="#74c0fc"/><path d="M262 338 V352 M302 338 V352"/>
      <path d="M366 348 H436 L428 304 H374Z" fill="#495057"/><rect class="pcs" x="381" y="311" width="40" height="30" fill="#74c0fc" stroke="none"/>
      <rect x="486" y="296" width="40" height="50" rx="8" fill="#fff"/><circle cx="499" cy="321" r="3.5" fill="${INK}"/><circle cx="513" cy="321" r="3.5" fill="${INK}"/></g>
    <path class="filo" d="" fill="none" stroke="${INK}" stroke-width="6" stroke-linecap="round"/>
    <g class="spina" ${O}><rect x="-13" y="-10" width="26" height="24" rx="6" fill="#343a40"/></g>
    ${PG("flavio")}<g class="cell"><rect x="-16" y="-30" width="32" height="56" rx="7" fill="#495057" ${O}/><rect x="-10" y="-22" width="20" height="36" rx="3" fill="#a5d8ff"/></g>
    ${POP("dopo", 338, 124, `<rect x="-122" y="-70" width="244" height="140" rx="22" fill="#fff" ${O}/>
      <g transform="translate(-76 -14)" ${O}><path d="M-22 -26 H8 Q22 -26 22 -10" fill="none" stroke-width="6"/><path d="M6 -6 H38" stroke-width="7"/>
        <path d="M10 6 l-4 12 M22 6 l-2 14 M34 6 l2 12" stroke="#4dabf7"/></g>
      <g transform="translate(-4 -12)" ${O}><circle r="26" fill="#fff"/><circle r="14" fill="#e7f5ff" stroke-width="3"/></g>
      <g transform="translate(72 -12) scale(.62) translate(-50 -52)">${INTERNO("orologio")}</g>
      ${TXT(0, 50, 21, "DOPO IL TEMPORALE")}`)}
    ${SPUNTA("okf", 164, 62, 26)}${DIVIETO("nof", 94, 318, 40)}${SPUNTA("okc", 572, 268, 24)}</svg>`,
  sereno: () => `<svg ${S0}>${CIELO("#d0ebff")}<rect class="buio" width="600" height="510" fill="#3b4a66" opacity=".3"/>
    ${SOLE(492, 176, 40)}<g class="via">${NERA(0, 0, 1.9, "#868e96")}</g>${PRATO(400)}
    <g class="orol" transform="translate(140 214)"><circle r="78" fill="#fff" ${O} stroke-width="6"/><path class="spicchio" d="" fill="#8ce99a" stroke="none"/>
      <g ${O} stroke-width="4">${Array.from({ length: 12 }, (_, i) => `<path d="M0 -70 V-${i % 3 ? 62 : 56}" transform="rotate(${i * 30})"/>`).join("")}</g>
      <path class="lanc" d="M0 0 V-56" ${O} stroke-width="8"/><path d="M0 0 L-26 -22" ${O} stroke-width="8"/><circle r="8" fill="${INK}"/></g>
    ${POP("min", 140, 340, `<rect x="-92" y="-32" width="184" height="64" rx="22" fill="#ffd43b" ${O}/>${TXT(0, 12, 34, "30 minuti")}`)}
    ${PG("flavio")}${PG("silvia", { tipo: "silvia", maglia: "#9775fa", pantaloni: "#f783ac", capelli: "#3b2412" })}</svg>`
};
