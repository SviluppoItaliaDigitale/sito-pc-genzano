---
paths:
  - "themes/**"
  - "layouts/**"
  - "assets/**"
  - "static/images/**"
  - "static/video/**"
  - "static/manuali/**"
  - "static/formazione/**"
  - "static/app-shared/**"
  - "static/open-data/**"
  - "content/manuale/**"
  - "content/chi-siamo/**"
  - "content/note-legali/**"
  - "content/area-download/**"
  - "content/risorse-pronte/**"
  - "content/social-media-policy/**"
  - "content/sala-stampa/**"
  - "data/risorse_pronte.yaml"
  - "scripts/genera-*"
  - "scripts/microtesto*"
  - "scripts/video*/**"
---

# Grafiche, loghi, deck, manuale, video e licenza

Regole spostate da `CLAUDE.md` l'11/11/2026, con il testo integrale: affiliazioni e composizione dei loghi, presentazione del sito, Manuale di Protezione Civile, video del Gruppo e licenza dei contenuti. Si caricano quando si lavora su tema, grafiche, generatori, manuale, video e pagine legali. La sintesi resta in `CLAUDE.md`.

## Affiliazioni e riconoscimenti europei — Quality Label ESC + codice obbligatorio

🔴 Il Gruppo è organizzazione accreditata dal **Corpo europeo di solidarietà** (European Solidarity Corps, ESC) della Commissione europea. **Vincolo cogente** ai sensi del **Regolamento (UE) 2021/888**: il logo Quality Label **deve essere mostrato sempre accompagnato dal codice di accreditamento dell'organizzazione**. Mai logo nudo.

- **Codice del Gruppo:** `E10435833` (sempre accanto al logo, in tutte le grafiche e i materiali di comunicazione).
- **Logo ufficiale UE:** `static/images/quality-label-esc.png` (PNG 400×400). Versione hi-res per stampa/deck in `static/images/logo-esc-quality-label-it.png` (4016×4016). Pacchetto ufficiale UE in `static/manuali/loghi-esc-italiano-pacchetto-ufficiale.zip` (PDF vettoriale + PNG).
- **Loghi affiliazione del Gruppo** = **2**, non 3: Quality Label ESC (+codice) e **SNPC Volontariato** (`static/images/logo-snpc-volontariato.png`). Il logo PC Genzano è la firma istituzionale del Gruppo (banner, header, schede): **non si conta tra le affiliazioni** per evitare duplicazione.

**Dove sono già esposti (non duplicare):**

| Superficie | Implementazione |
|---|---|
| Footer site-wide Hugo | `themes/flavour-pcgenzano/layouts/partials/footer.html` (blocco `.esc-quality-label`) |
| Footer pagine statiche | `static/app-shared/site-chrome.js` (stesso blocco iniettato JS) |
| Pagina `/chi-siamo/` | Sezione "Affiliazioni e riconoscimenti europei" con descrizione + codice + Reg. UE 2021/888 |
| Carosello social Instagram | Slide finale "Affiliazioni" via `crea_slide_affiliazioni()` in `scripts/genera-immagini-social.py` (E10435833 in colore accento) |
| Schede stampabili A4 | Banda piè pagina in stampa via `.scheda::after` in `static/formazione/kit-calamita-shared/print.css` (immagine `static/images/footer-print-affiliazioni.png`) |
| Deck di presentazione | Slide "Affiliazioni e riconoscimenti europei" in `scripts/genera-presentazione.py` |

**Cosa NON serve fare:**

- **Mai aggiungere i 2 loghi al banner cover degli articoli** (fascia blu col titolo). Il vincolo UE è già soddisfatto dal footer site-wide; aggiungerli al banner sovraffolla il titolo e rompe l'identità visiva.
- **Mai batch retroattivo** sulle ~577 immagini esistenti per aggiungere i loghi. La ricompressione WebP degrada la qualità senza valore aggiunto (i loghi sono già nel footer di ogni pagina che le mostra).
- **Mai modificare i pittogrammi ISO 7010 / ARASAAC** per aggiungere loghi: violerebbe le licenze d'uso terze.

**Cosa fare in nuove grafiche/slide future:** se la grafica include un blocco "affiliazioni / riconoscimenti", usare **sempre** i 3 loghi affiliazione insieme + codice `E10435833` ben leggibile accanto al Quality Label. Mai logo ESC senza codice. Mai aggiungere PC Genzano tra gli "affiliati" (è la firma).

**🔴 Composizione standard di ogni nuova grafica istituzionale = ESATTAMENTE 4 LOGHI, MAI DOPPIONI:**

1. **Firma PC Genzano** (logo del Gruppo) — nell'**header/banner/intestazione** della grafica (cover articoli, header schede A4, barra brand top slide social, prima pagina deck). Identità visiva del Gruppo.
2. **Quality Label ESC + codice E10435833** — nel **footer/blocco affiliazioni** della grafica. Mai logo nudo (vincolo cogente Reg. UE 2021/888).
3. **Coordinamento FEPIVOL** — nel **footer/blocco affiliazioni** insieme agli altri 2.
4. **SNPC Volontariato** — nel **footer/blocco affiliazioni** insieme agli altri 2.

**Regole di composizione, vietato deviare:**

- La firma (1) è sempre **separata** dalle affiliazioni (2-4): mai mescolare PC Genzano tra le card affiliazione (sarebbe doppione).
- **Mai inserire lo stesso logo due volte** nella stessa grafica.
- **Mai inserire un 5° logo** (PC Lazio, Comune, Croce Rossa, ANPAS, VVF, INGV, ecc.): quei loghi sono di enti coordinatori/operatori del Sistema PC e vanno citati nei contenuti testuali o nel footer site-wide del sito, MAI nella grafica istituzionale del Gruppo.

**Vale anche per grafiche realizzate con AI esterne** (ChatGPT, Gemini, Midjourney, Canva, Adobe Express, DALL-E, ecc.): includere sempre nel prompt la regola "esattamente 4 loghi, mai doppioni, mai 5° logo, ESC sempre con codice E10435833" + fornire i 4 file dal repo. Specifiche complete + pattern brief da incollare alle AI esterne in `.claude/rules/02-content-design-pa.md § "Composizione standard"` (auto-incluso in `CONTESTO-PROGETTO.md` rigenerato).

Le grafiche già aggiornate seguono questo schema: cover articoli, slide social, schede A4, deck, /chi-siamo/ § Affiliazioni. Footer site-wide del sito: blocco chrome del portale (non grafica isolata), ha 4 loghi con PC Lazio come ente territoriale al posto della firma PC Genzano (che è già nel banner top del sito, mai duplicato nel footer).

---

## Presentazione del sito (deck) — rigenerare a ogni cambiamento di struttura o dati

🟢 Esiste un **deck istituzionale di presentazione del portale**: `static/manuali/presentazione-struttura-sito.pdf` (+ `.pptx` editabile), generato da `scripts/genera-presentazione.py`, linkato dall'**Area Download** (`content/area-download/_index.md` § "Presentazione del sito").

🔴 **Regola precisa:** ogni volta che una **sezione/area del sito viene aggiunta, modificata o eliminata**, o quando cambiano **dati, contatti, fonti o standard** mostrati nel deck (es. menu, schede del cruscotto, recapiti, affiliazioni come FEPIVOL), **rigenera il deck e ripubblicalo nello stesso commit** della modifica. Il deck non deve mai restare disallineato dal sito.

**Come:** `python scripts/genera-presentazione.py` (serve un venv con `python-pptx pillow fonttools brotli` + **LibreOffice** per l'export PDF). Lo script ricava font-icone (Bootstrap Icons self-hostate), logo e contatti **dal repo**, produce PPTX+PDF in `static/manuali/`. Se aggiungi una sezione al sito, aggiungi la slide corrispondente nel generatore. Vincoli del deck: **nessun riferimento a strumenti automatici/IA**, logo + contatti reali, rischi mostrati come **copertura** (non dettaglio del singolo rischio), slide di autorevolezza con fonti/standard, agenda a pulsanti + navigazione (frecce + "torna all'agenda").

---

## Manuale di Protezione Civile — opera viva, sincronizzazione obbligatoria

🔴 Il **Manuale di Protezione Civile** (`/manuale/`, sezione Hugo a impianto accademico: reader online + PDF) è un'**opera viva**. Regola cogente: **quando aggiorni una norma, un dato istituzionale o un contenuto che il manuale riprende, AGGIORNA nello stesso lavoro il capitolo o l'appendice corrispondente del manuale.** Un aggiornamento del sito che lascia il manuale disallineato è un lavoro incompleto.

**Trigger di aggiornamento obbligatorio:**
- Una **norma citata** nel manuale cambia / viene abrogata / sostituita (D.Lgs., L., DPCM, direttiva, **ISO/UNI**) → aggiorna il capitolo che la tratta (es. il commentario al Codice) e ricontrolla la vigenza con `pc-normative-verifier`. *(Caso reale 10/06/2026: UNI 11656:2016 ritirata e sostituita dalla 11656:2023 — citare sempre l'edizione vigente.)*
- Un **contenuto del sito** che il manuale rielabora cambia (`/conoscere/`, `/rischi-prevenzione/`, `/normativa/`, `/standard-iso/`, glossario, numeri utili, eventi storici) → riallinea capitolo/appendice.
- Un **dato istituzionale** cambia (recapiti, sede, affiliazioni, organizzazione) → aggiornalo dove il manuale lo riporta.

**Meccanismi automatici (fanno parte dell'opera viva):**
- **Fonte unica**: reader online e PDF nascono dallo stesso Markdown → modificando un capitolo si aggiornano entrambi.
- **Data "aggiornato il" automatica (dal 17/08/2026)**: la data di ultima revisione mostrata su `/manuale/` e sul frontespizio del PDF è il **`.Lastmod` git più recente tra frontespizio e capitoli**, calcolato a build dal partial `manuale-ultima-revisione.html` — niente campo manuale da aggiornare (il vecchio `dataUltimaRevisione` in `_index.md` era rimasto fermo al 10/06 con capitoli aggiornati fino al 16/08 ed è stato rimosso). Richiede checkout `fetch-depth: 0` (già in `deploy.yml` e `genera-manuale-pdf.yml`).
- **Appendici generate** dai dati del sito (glossario, normativa, ISO, numeri utili, eventi) → si riallineano da sole al build; non si toccano a mano.
- **PDF**: rigenera con `~/.manuale-venv/bin/python scripts/genera-manuale-pdf.py` dopo ogni modifica ai capitoli, poi aggiorna la sua riga nell'inventario dei PDF con `python3 scripts/audit-pdf-accessibilita.py --aggiorna /manuali/manuale-protezione-civile.pdf` (senza, la PR si ferma su `--check-inventario`); il workflow `genera-manuale-pdf.yml` rigenera in automatico PDF e riga dell'inventario a ogni push su `content/manuale/**` o sui layout/CSS del manuale.
- **Watcher**: `normativa-watcher.yml` va esteso a `content/manuale/` perché apra una issue quando una norma citata nel manuale cambia (flag per la revisione umana, **non** riscrittura automatica → NO INVENZIONI).

**NO INVENZIONI resta assoluto**: ogni affermazione e ogni aggiornamento è ricondotto a una **fonte primaria verificata**. Per il commentario dei testi unici si usa il **testo vigente** scaricato dalla fonte ufficiale (Normattiva via `curl`+`pandoc`; mai parafrasare una norma a memoria). Estratti autentici in `riferimenti-interni/commentario-testi-unici/` (non deployati). **Registro accademico = eccezione dichiarata al gate AGID**: NON invocare `pc-article-reviewer` sui capitoli del manuale (rigetterebbe la prosa accademica); vale un gate dedicato di fonti/citazioni/struttura. Decisioni e stato del progetto nella memory `project_manuale_protezione_civile`.

---

## Video del Gruppo — sempre per uso non commerciale

🟢 **Decisione dell'utente del 24/10/2026**: *«Tutti i nostri video sono per uso non commerciale!»*. Ogni video del Gruppo (motion graphic, video in 3D, montaggi, Reel, video degli articoli, puntate e podcast video) serve a informare e formare i cittadini: niente pubblicità, sponsor, vendite o monetizzazione dei canali, su nessuna piattaforma.

- Nei video si possono usare materiali e strumenti con licenza o piano **solo per uso non commerciale**: per esempio contenuti in CC BY-NC o CC BY-NC-SA, i pittogrammi ARASAAC, il modello italiano di allineamento dei sottotitoli in CC BY-NC 4.0. Valgono tutte le loro altre condizioni: l'attribuzione e, per i materiali «SA», la stessa licenza sul video.
- 🔴 **Mai il nome dello strumento o del sito che ha prodotto voce, musica o immagini** (decisione dell'utente del 24/10/2026, che conferma § «Nessun riferimento all'IA»): né nel video, né nel titolo, né nella descrizione, nei sottotitoli, nei metadati o nei post. La voce **Luca** resta nel video sugli incendi e negli altri video in cui c'è, senza alcun riferimento al sito che l'ha generata. L'utente conosce le condizioni dei piani gratuiti (informato il 24/10/2026): non si chiede di nuovo e non si propone mai di aggiungere attribuzioni a strumenti.
- 🟢 **Ordine delle voci e crediti (decisione dell'utente del 12/11/2026)**: prima voce sempre Luca finché ci sono crediti; poi la voce gratuita Damien (solo video non commerciali e non finanziati), poi Serena. Dentro il video non va nulla di esterno ai lavori del Gruppo; i crediti dovuti per licenza (musica CC BY, rilievo, e con Damien la riga «Voce sintetica: modello distribuito con licenza Coqui Public Model License (coqui.ai/cpml).») vanno nella descrizione del video sul sito e nei post social dove il video compare. Questa riga è l'unica eccezione al divieto del punto precedente, perché la impone la licenza. Dettagli: skill `motion-graphic`, § «Voce, musica ed effetti: ordine e licenze».
- Il controllo spetta a `pc-produzione-multimediale` (mandato operativo, punto «Licenze»).

---

## Licenza del sito — CC BY-NC-SA 4.0 (dal 24/10/2026)

🔴 **Decisione dell'utente del 24/10/2026**: *«Proprio tutto il sito sotto licenza NC!»*. I contenuti del Gruppo (testi, articoli, pagine, foto e grafiche, video, podcast, kit, schede, documenti, presentazioni) sono distribuiti con licenza **CC BY-NC-SA 4.0**. Eccezioni dichiarate in `/note-legali/#licenza-dei-contenuti`: **dati aperti CC BY 4.0** (CAD, art. 1, c. 1, lett. l-ter: i dati aperti devono ammettere anche l'uso commerciale), **codice dell'Open Kit EUPL 1.2**, **comunicati stampa** che le testate possono pubblicare citando la fonte, **materiali di terzi** con la loro licenza (anche adattati con la fascia blu), **loghi** esclusi. Le copie già prese in CC BY 4.0 restano utilizzabili alle condizioni di allora (le licenze CC non si revocano).

Punti da tenere allineati quando la licenza o un'eccezione cambia: note legali, social media policy, Sala stampa, Risorse pronte (+ `data/risorse_pronte.yaml`), Open Kit (pagina + `scripts/genera-open-kit.py`), `jsonld-copyright.html`, piè di pagina (Hugo + `site-chrome.js`), `.htaccess` (header di licenza solo sulle pagine e sui dati aperti, mai su immagini, PDF, video, codice e caratteri, perché lì convivono file di terzi; `DATI_APERTI`/`DATI_TERZI`: un nuovo file di dati di terzi in `static/open-data/` va in `DATI_TERZI`), `copy-attribution.js`, attestato dei giochi, deck di presentazione.
