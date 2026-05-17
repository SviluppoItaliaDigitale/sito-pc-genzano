# Prompt per le 14 schede colorabili Infanzia

**Strumento target**: ChatGPT (DALL·E 3) o Gemini Imagen / Midjourney.

**Output atteso per ogni prompt**: 1 PNG A4 verticale, line art bianco/nero, salvato in `~/Scrivania/disegni/<slug>.png` (vedi nome canonico in ogni prompt).

## Regole comuni — copiate in OGNI prompt per evitare i difetti emersi sulla v1 volontario

🔴 **Per evitare i 5 difetti riscontrati nella prima generazione** (refuso "comunirare", data "Maggio 2024" sbagliata, stemma Genzano inventato, numerazione incoerente, motto inventato), il prompt impone tassativamente:

1. **Tutto il testo in italiano corretto** — l'AI deve scrivere ESATTAMENTE le didascalie fornite, parola per parola, senza inventare né alterare lettere.
2. **NESSUNO stemma, nessun logo, nessun emblema** — niente scudi, niente loghi del Comune, niente loghi di volontariato. Lo spazio in alto va lasciato vuoto (solo titolo centrato).
3. **NESSUNA data** nel footer. Solo URL `protezionecivilegenzano.it`.
4. **NESSUNO slogan/motto** ("Insieme per..." ecc.) — non vanno inventati.
5. **Numerazione coerente** — TUTTE le 6 vignette devono avere il numero cerchiato grande in alto-sinistra, dentro al box. Stessa dimensione, stessa posizione.

Questi punti vanno inseriti come istruzioni hard nel prompt (sezione "VINCOLI ASSOLUTI").

Gli elementi mancanti (**logo ufficiale del Gruppo Comunale** — già contiene lo stemma del Comune di Genzano al centro — + data revisione + URL stilizzato) li sovrappongo io in post-produzione con Pillow una volta che l'immagine è in `~/Scrivania/disegni/`, prima di pubblicarla.

**Logo già pronto in repo**: `static/images/logo-pc-genzano-hires.png` (1080×1080 px, 127 KB) — versione alta risoluzione del logo del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma. Include già la corona civica + colonna SPQG + corona d'alloro + nastro tricolore del Comune. È un logo **tutto-in-uno**: non servono stemmi separati. Verrà posizionato centrato nella fascia superiore vuota delle schede generate dall'AI, dimensione finale ~250×250 px sull'A4 della scheda 1024×1536.

---

## TEMPLATE BASE riusabile (sostituisci i campi `{...}` per ogni scheda)

```
Coloring page for Italian kindergarten children (age 4-6), A4 portrait
orientation, 1024x1536 pixels resolution. Pure black line art on white
background — NO shading, NO grey fills, NO color. Cartoon kawaii style:
characters with big round eyes, friendly smiles, simple rounded shapes,
thick clean outlines (2-3 pixel weight).

LAYOUT (top to bottom):

1. TOP HEADER: empty horizontal space of about 120 pixels (will be filled
   later with official logos in post-production). DO NOT draw any shield,
   crest, coat of arms, badge, logo or emblem. Just leave white space.

2. TITLE: large cartoon font centered, on TWO lines, exactly this text:
   "{TITLE_LINE_1}"
   "{TITLE_LINE_2}"

3. SUBTITLE: smaller font centered, exactly:
   "Colora i disegni e impara cosa fare in 6 passi facili!"

4. 6 NUMBERED PANELS arranged in a 2 columns × 3 rows grid. Each panel:
   - rectangular box with thick rounded-corner border
   - in the TOP-LEFT corner, a black filled CIRCLE with the panel number
     in white inside (1, 2, 3, 4, 5, 6 respectively)
   - illustration inside the box (line art only)
   - caption text below the illustration, INSIDE the box, in clean cartoon
     uppercase font, exactly as written below (NO TYPOS, NO PARAPHRASING,
     NO MISSING LETTERS)

   Panel 1 — illustration: {SCENE_1}
   Panel 1 — caption: "{CAPTION_1}"

   Panel 2 — illustration: {SCENE_2}
   Panel 2 — caption: "{CAPTION_2}"

   Panel 3 — illustration: {SCENE_3}
   Panel 3 — caption: "{CAPTION_3}"

   Panel 4 — illustration: {SCENE_4}
   Panel 4 — caption: "{CAPTION_4}"

   Panel 5 — illustration: {SCENE_5}
   Panel 5 — caption: "{CAPTION_5}"

   Panel 6 — illustration: {SCENE_6}
   Panel 6 — caption: "{CAPTION_6}"

5. BOTTOM FOOTER: empty horizontal space of about 60 pixels (will be filled
   later with the URL and revision date in post-production). DO NOT add
   slogans, mottos, URLs or dates.

CIVIL PROTECTION VOLUNTEER UNIFORM (when present in scenes):
- white safety helmet with a black equilateral TRIANGLE symbol on the
  front (this is the official Italian Civil Protection symbol)
- high-visibility vest with the abbreviation "PC" written on the chest
- friendly smiling face, large round eyes

ABSOLUTE CONSTRAINTS — DO NOT VIOLATE:
✗ NO shields, NO coats of arms, NO badges, NO logos, NO emblems
✗ NO dates (no "2024", "2025", "2026", "Maggio", "rev.")
✗ NO slogans, NO mottos, NO "Insieme...", NO "Aiutare..." in footer
✗ NO URL inside the image
✗ NO color (only black ink on white)
✗ NO Italian text changes — copy each caption letter by letter

ITALIAN TEXT QUALITY: each Italian caption must be rendered with PERFECT
spelling. Pay extra attention to words like "comunicare", "soccorrere",
"distribuire", "allestire" — NEVER drop or duplicate letters.
```

---

## Le 14 schede — campi da sostituire nel template

### 1. `colorare-volontario-infanzia` 🤝
**Nome file output**: `~/Scrivania/disegni/volontario.png`

- TITLE_LINE_1: `IL VOLONTARIO`
- TITLE_LINE_2: `DELLA PROTEZIONE CIVILE`
- SUBTITLE: `Colora le immagini e scopri cosa fanno i volontari!`
- SCENE_1: Civil protection volunteer waving hello with one hand raised, smiling
- CAPTION_1: `Il volontario è sempre pronto ad aiutare.`
- SCENE_2: Civil protection volunteer holding a walkie-talkie radio near the mouth, speaking
- CAPTION_2: `Usa la radio per parlare con gli altri volontari.`
- SCENE_3: Civil protection volunteer crouched down helping an elderly woman with a walking stick
- CAPTION_3: `Aiuta le persone in difficoltà.`
- SCENE_4: Civil protection volunteer handing a water bottle to a small girl, basket of food nearby
- CAPTION_4: `Distribuisce acqua e cibo a tutti.`
- SCENE_5: Civil protection van with side door open, volunteer driver waving from inside, triangle PC symbol visible on hood
- CAPTION_5: `Arriva sul posto con i mezzi della Protezione Civile.`
- SCENE_6: Two civil protection volunteers setting up a triangular field tent with poles, tent has PC triangle symbol
- CAPTION_6: `Allestisce le tende per accogliere le persone.`

---

### 2. `colorare-frana-infanzia` ⛰️
**Nome file output**: `~/Scrivania/disegni/frana.png`

- TITLE_LINE_1: `COSA FACCIO`
- TITLE_LINE_2: `SE VEDO UNA FRANA?`
- SCENE_1: A hillside with rocks and stones falling down a slope, motion lines showing movement
- CAPTION_1: `Vedo sassi che cadono dalla collina.`
- SCENE_2: A child running away from a hillside, looking worried but determined, motion lines
- CAPTION_2: `Mi allontano subito.`
- SCENE_3: A child looking up at an adult (parent or teacher), pointing back toward danger, talking
- CAPTION_3: `Avviso un adulto.`
- SCENE_4: A child stopped with hand up in "stop" gesture, NO entry symbol (circle with diagonal line) over the danger zone
- CAPTION_4: `Non torno mai indietro.`
- SCENE_5: A child safe inside a house, sitting in an armchair, window with curtains
- CAPTION_5: `Sto al sicuro dentro casa.`
- SCENE_6: Two civil protection volunteers (white helmet with PC triangle, vest with "PC") inspecting the hillside with a clipboard
- CAPTION_6: `Arrivano i volontari della Protezione Civile.`

---

### 3. `colorare-alluvione-infanzia` 🌊
**Nome file output**: `~/Scrivania/disegni/alluvione.png`

- TITLE_LINE_1: `COSA FACCIO`
- TITLE_LINE_2: `SE C'È UNA GRANDE PIOGGIA?`
- SCENE_1: A child climbing up stairs in a house, arrow pointing UP, water at the bottom level
- CAPTION_1: `Vado al piano di sopra.`
- SCENE_2: A flooded underpass with water, big NO entry circle/diagonal line warning
- CAPTION_2: `Non passo nei sottopassaggi allagati.`
- SCENE_3: A staircase going DOWN to a basement with water at the bottom, big NO entry warning
- CAPTION_3: `Non scendo in cantina o nel garage.`
- SCENE_4: An adult reaching up to an electrical wall socket, unplugging a cord
- CAPTION_4: `Un adulto stacca la corrente.`
- SCENE_5: A child holding a telephone, dialing, numbers "1 1 2" visible on the phone screen
- CAPTION_5: `Se serve, chiamo il 112.`
- SCENE_6: A child at a window on the upper floor of a house, looking out calmly, water below
- CAPTION_6: `Aspetto al sicuro i soccorsi.`

---

### 4. `colorare-pompiere-infanzia` 🚒
**Nome file output**: `~/Scrivania/disegni/pompiere.png`

- TITLE_LINE_1: `IL MIO AMICO`
- TITLE_LINE_2: `POMPIERE`
- SUBTITLE: `Colora i disegni e conosci il pompiere e i suoi attrezzi!`
- SCENE_1: A close-up of a firefighter's helmet with chinstrap, classic Italian firefighter design (large helmet with side flaps protecting neck)
- CAPTION_1: `Ha il casco con la visiera.`
- SCENE_2: A pair of tall rubber boots, side by side
- CAPTION_2: `Ha gli stivali grandi.`
- SCENE_3: A firefighter's jacket with horizontal reflective stripes across chest and arms
- CAPTION_3: `Ha la giacca a strisce.`
- SCENE_4: A smiling firefighter holding a fire hose, water spraying onto flames
- CAPTION_4: `Spegne il fuoco.`
- SCENE_5: A firefighter carrying a small child in his arms, both smiling
- CAPTION_5: `Mi aiuta sempre.`
- SCENE_6: A telephone with "112" shown on screen, and a fire truck in the background
- CAPTION_6: `Lo chiamo con il 112.`

---

### 5. `colorare-incendio-infanzia` 🔥
**Nome file output**: `~/Scrivania/disegni/incendio.png`

- TITLE_LINE_1: `COSA FACCIO`
- TITLE_LINE_2: `SE VEDO DEL FUMO?`
- SCENE_1: A child pointing toward smoke coming from a room, looking up at an adult who is paying attention
- CAPTION_1: `Avviso subito un adulto.`
- SCENE_2: A child closing a door behind himself, hand on doorknob, smoke on the other side
- CAPTION_2: `Chiudo la porta.`
- SCENE_3: A child crouching low to the floor with hand over mouth, smoke drawn in cloudy lines above
- CAPTION_3: `Resto basso, sotto il fumo.`
- SCENE_4: An emergency exit sign (rectangle with arrow and running person symbol) on a wall, child walking toward it
- CAPTION_4: `Esco seguendo il cartello di uscita.`
- SCENE_5: A child walking away from a building with smoke, big NO entry warning over a path back to the building
- CAPTION_5: `Non torno indietro.`
- SCENE_6: A group of children standing with their teacher near a sign that reads "PUNTO DI RACCOLTA"
- CAPTION_6: `Vado al punto di raccolta.`

---

### 6. `colorare-temporale-infanzia` ⛈️
**Nome file output**: `~/Scrivania/disegni/temporale.png`

- TITLE_LINE_1: `COSA FACCIO`
- TITLE_LINE_2: `SE C'È UN TEMPORALE?`
- SCENE_1: A child running toward a house door, rain falling, lightning bolt in the sky
- CAPTION_1: `Corro a casa o in un posto al chiuso.`
- SCENE_2: An adult unplugging a television set during a storm
- CAPTION_2: `Un adulto stacca la TV e gli apparecchi.`
- SCENE_3: A large tree being struck by lightning, big NO entry warning underneath the tree
- CAPTION_3: `Non sto sotto un albero.`
- SCENE_4: A swimming pool with rain falling, big NO entry warning over it, lightning bolt nearby
- CAPTION_4: `Non vado in piscina o nel lago.`
- SCENE_5: A child sitting comfortably on a sofa inside a house, looking out the window at the rain
- CAPTION_5: `Aspetto al sicuro in casa.`
- SCENE_6: A flooded puddle/pothole with NO entry warning, child stopping
- CAPTION_6: `Non corro nelle pozzanghere.`

---

### 7. `colorare-112-infanzia` 📞
**Nome file output**: `~/Scrivania/disegni/numero-112.png`

- TITLE_LINE_1: `COME CHIAMO`
- TITLE_LINE_2: `IL 112?`
- SCENE_1: A child noticing smoke or a fall, looking concerned but calm
- CAPTION_1: `Vedo un'emergenza.`
- SCENE_2: A child taking a deep breath, picking up a telephone from a table
- CAPTION_2: `Resto calmo e prendo il telefono.`
- SCENE_3: Close-up of a telephone keypad with the numbers "1 — 1 — 2" highlighted
- CAPTION_3: `Faccio uno, uno, due.`
- SCENE_4: A child speaking into the telephone, name tag visible saying "FLAVIO"
- CAPTION_4: `Dico il mio nome.`
- SCENE_5: A child speaking into the telephone, pointing to ground/place, map visible
- CAPTION_5: `Dico dove mi trovo.`
- SCENE_6: A child sitting by the door waiting, ambulance/fire truck arriving with siren lights drawn as motion lines
- CAPTION_6: `Aspetto i soccorsi che arrivano.`

---

### 8. `colori-mezzi-soccorso-infanzia` 🚑
**Nome file output**: `~/Scrivania/disegni/mezzi-soccorso.png`

Questa scheda ha **struttura diversa**: invece di 6 vignette racconto-azione, ha 6 vignette MEZZO + COLORE-DA-RICORDARE.

- TITLE_LINE_1: `I COLORI`
- TITLE_LINE_2: `DEI MEZZI DI SOCCORSO`
- SUBTITLE: `Colora ogni mezzo con il suo colore giusto!`
- Panel 1 — illustration: A fire truck with ladder, side view, recognizable Italian style. Caption: `Il camion dei pompieri: ROSSO.`
- Panel 2 — illustration: An ambulance with cross symbol on the side. Caption: `L'ambulanza: BIANCA con strisce.`
- Panel 3 — illustration: A civil protection van with PC triangle on the side. Caption: `Il furgone della PC: ARANCIONE o BLU.`
- Panel 4 — illustration: A police car. Caption: `L'auto della polizia: BLU con strisce.`
- Panel 5 — illustration: A Carabinieri car. Caption: `L'auto dei Carabinieri: BLU SCURO.`
- Panel 6 — illustration: A forestry/AIB firefighter helicopter or pickup truck. Caption: `Il mezzo antincendio boschivo: GIALLO.`

---

### 9. `colorare-neve-infanzia` ❄️
**Nome file output**: `~/Scrivania/disegni/neve.png`

- TITLE_LINE_1: `COSA FACCIO`
- TITLE_LINE_2: `SE NEVICA FORTE?`
- SCENE_1: A child wearing winter hat, scarf, gloves, warm jacket, big smile
- CAPTION_1: `Mi vesto bene caldo.`
- SCENE_2: A child walking slowly on a snowy street, looking down at icy ground carefully
- CAPTION_2: `Cammino piano, c'è ghiaccio.`
- SCENE_3: A snowy street with cars, big NO entry warning over a ball/game in the middle of the road
- CAPTION_3: `Non gioco in mezzo alla strada.`
- SCENE_4: A child indoors with hot drink in mug, sitting by a window with snow falling outside
- CAPTION_4: `Sto a casa al caldo.`
- SCENE_5: A child with shovel helping an adult clear snow from a doorstep
- CAPTION_5: `Aiuto a spalare la neve.`
- SCENE_6: A telephone showing "112" and a civil protection 4x4 vehicle on snowy road
- CAPTION_6: `Se serve, chiamiamo il 112.`

---

### 10. `colorare-terremoto-infanzia` 🐢
**Nome file output**: `~/Scrivania/disegni/terremoto.png`

- TITLE_LINE_1: `COSA FACCIO`
- TITLE_LINE_2: `QUANDO TREMA LA TERRA?`
- SCENE_1: A child crouched UNDER a sturdy table, hands protecting head
- CAPTION_1: `Vado sotto al tavolo.`
- SCENE_2: A child standing with both hands clasped over his head
- CAPTION_2: `Metto le mani sulla testa.`
- SCENE_3: A friendly cartoon turtle tucked into its shell, peaceful
- CAPTION_3: `Aspetto fermo come la tartaruga.`
- SCENE_4: A teacher walking in front of a line of children, all holding hands
- CAPTION_4: `Esco in fila con la maestra.`
- SCENE_5: An elevator with doors, big NO entry warning over the elevator
- CAPTION_5: `Non uso l'ascensore.`
- SCENE_6: A group of children with their teacher standing near a sign "PUNTO DI RACCOLTA"
- CAPTION_6: `Vado al punto di raccolta.`

---

### 11. `colorare-vento-infanzia` 💨
**Nome file output**: `~/Scrivania/disegni/vento.png`

- TITLE_LINE_1: `COSA FACCIO`
- TITLE_LINE_2: `SE C'È VENTO FORTE?`
- SCENE_1: A child inside a house looking out a window, with trees bending in the wind outside
- CAPTION_1: `Sto dentro casa.`
- SCENE_2: An adult or child closing a window, latching it shut
- CAPTION_2: `Chiudo bene le finestre.`
- SCENE_3: A large tree bending heavily under wind, branches breaking, big NO entry warning beneath it
- CAPTION_3: `Non sto sotto gli alberi.`
- SCENE_4: A balcony with flower pots blowing over in the wind, big NO entry warning over the balcony
- CAPTION_4: `Non vado sul balcone.`
- SCENE_5: A child carrying outdoor toys (ball, bike) into a garage or shelter
- CAPTION_5: `Metto i giochi al riparo.`
- SCENE_6: A child sitting safely indoors with a book, clock on wall, wind drawn outside through window
- CAPTION_6: `Aspetto che il vento passi.`

---

## Le 4 schede "speciali" (struttura diversa dalle 6-vignette)

Le ultime 4 schede non seguono lo schema 6-vignette. Hanno prompt dedicati.

### 12. `filastrocca-illustrata-infanzia` 🐢 — Filastrocca della Tartaruga

**Nome file output**: `~/Scrivania/disegni/filastrocca-tartaruga.png`

```
Coloring page for Italian kindergarten children (age 4-6), A4 portrait,
1024x1536 px, pure black line art on white background, NO color.

LAYOUT:
1. TOP: empty 120px space for logos (do not draw anything there)
2. Large title in cartoon font, two lines centered:
   "LA FILASTROCCA"
   "DELLA TARTARUGA"
3. Subtitle: "Colora la tartaruga e impara cosa fare in un terremoto!"

4. ONE LARGE central illustration (about 60% of page): a friendly cartoon
   turtle with a big segmented shell (the segments can be colored
   separately). The turtle has big eyes and a gentle smile, tucked
   slightly into its shell. Around the turtle, dotted lines suggest
   tremors. Decorative elements: stars, hearts.

5. Below the turtle, the filastrocca poem written in cartoon uppercase
   font, exactly this text (each line on its own line, NO TYPOS):

   "QUANDO LA TERRA TREMA UN PO',
    COME LA TARTARUGA IO STARÒ.
    MI METTO SOTTO IL TAVOLINO,
    LE MANI SULLA TESTA CON UN BEL FILO.
    ASPETTO FERMA, NON HO PAURA,
    LA MIA MAESTRA MI FA SICURA."

6. BOTTOM: empty 60px footer (for URL/date in post-production)

VINCOLI ASSOLUTI: NO logos, NO shields, NO dates, NO slogans, NO URL,
NO color. Italian text must be SPELLED EXACTLY as above.
```

---

### 13. `disegna-aiutante-infanzia` ✏️ — Disegna il tuo aiutante

**Nome file output**: `~/Scrivania/disegni/disegna-aiutante.png`

```
Coloring page for Italian kindergarten children (age 4-6), A4 portrait,
1024x1536 px, pure black line art on white background, NO color.

LAYOUT:
1. TOP: empty 120px space for logos
2. Title centered in cartoon font, two lines:
   "DISEGNA"
   "IL TUO AIUTANTE"
3. Subtitle: "Come immagini il volontario che ti aiuta? Disegnalo tu!"

4. CENTRAL AREA: a large DOTTED OUTLINE (about 70% of page height) of a
   civil protection volunteer figure — only the silhouette in dotted/dashed
   lines, like a guide for the child to follow and complete. Inside the
   silhouette: a few HINTS drawn in dotted lines too:
   - white helmet outline at the top (with small triangle hint)
   - vest outline on the torso (with letters "PC" hinted faintly)
   - friendly face area with just two dots for eyes (no full features)
   - empty hands the child can fill with whatever object they want

5. To the right of the silhouette: 3-4 empty oval bubbles labeled in
   cartoon font:
   - "OCCHI" (eyes)
   - "BOCCA" (mouth)
   - "COSA TIENE IN MANO?" (what is he holding?)
   - "I COLORI" (the colors)

6. BOTTOM: empty 60px footer

VINCOLI ASSOLUTI: NO logos, NO shields, NO dates, NO slogans, NO URL.
The silhouette must be DOTTED LINES (not solid) so the child can trace
and complete it.
```

---

### 14. `pregrafismo-linee-infanzia` ✏️ — Pregrafismo: le linee della PC

**Nome file output**: `~/Scrivania/disegni/pregrafismo-linee.png`

```
Coloring page for Italian kindergarten children (age 3-5), A4 portrait,
1024x1536 px, pure black line art on white background, NO color.

LAYOUT:
1. TOP: empty 120px space for logos
2. Title: "LE LINEE DELLA PROTEZIONE CIVILE"
3. Subtitle: "Segui le linee tratteggiate con la matita!"

4. FOUR EXERCISES stacked vertically, each in its own section with a small
   illustration on the LEFT and a row of dotted line on the RIGHT:

   Exercise 1: LINEE DRITTE
   - LEFT: drawing of a civil protection helmet
   - RIGHT: 3 horizontal dotted lines stretching across, child traces them

   Exercise 2: ZIG-ZAG
   - LEFT: drawing of a lightning bolt
   - RIGHT: 2 zig-zag dotted lines

   Exercise 3: ONDE
   - LEFT: drawing of water waves
   - RIGHT: 2 wavy dotted lines

   Exercise 4: SPIRALI
   - LEFT: drawing of a tornado/whirl
   - RIGHT: 3 spiral dotted shapes to trace

5. BOTTOM: empty 60px footer

VINCOLI ASSOLUTI: NO logos, NO shields, NO dates, NO slogans, NO URL.
Each label MUST be spelled exactly: "LINEE DRITTE", "ZIG-ZAG", "ONDE",
"SPIRALI".
```

---

### 15. `riconosci-forme-infanzia` 🔺 — Riconosci le forme dei cartelli

**Nome file output**: `~/Scrivania/disegni/riconosci-forme.png`

```
Coloring page for Italian kindergarten children (age 3-5), A4 portrait,
1024x1536 px, pure black line art on white background, NO color.

LAYOUT:
1. TOP: empty 120px space for logos
2. Title: "LE FORME DEI CARTELLI"
3. Subtitle: "Ogni cartello ha la sua forma. Coloriamoli insieme!"

4. SIX large signs displayed in a 2 columns × 3 rows grid, each in its
   own labeled section:

   Sign 1: CIRCLE with a diagonal slash (Italian NO ENTRY / Divieto)
   Caption: "IL CERCHIO È UN DIVIETO."

   Sign 2: SQUARE green outline with running figure (Italian USCITA DI
   EMERGENZA / Emergency exit)
   Caption: "IL QUADRATO MOSTRA L'USCITA."

   Sign 3: EQUILATERAL TRIANGLE with exclamation mark
   Caption: "IL TRIANGOLO È UN PERICOLO."

   Sign 4: CIRCLE (filled outline only) plain — for "OBBLIGO"
   Caption: "IL CERCHIO BLU È UN OBBLIGO."

   Sign 5: RECTANGLE with cross symbol (for medical/first aid)
   Caption: "IL RETTANGOLO È INFORMAZIONE."

   Sign 6: TRIANGLE with the official Civil Protection triangle inside
   Caption: "QUESTO TRIANGOLO È LA PROTEZIONE CIVILE."

5. BOTTOM: empty 60px footer

VINCOLI ASSOLUTI: NO logos, NO shields, NO dates, NO slogans, NO URL.
Caption text must be spelled EXACTLY.
```

---

## Workflow operativo

Per ogni scheda:

1. **Apri ChatGPT (DALL·E 3) o Gemini Imagen**.
2. Copia il **TEMPLATE BASE** sopra, sostituisci i campi `{...}` con i valori della scheda specifica.
3. Genera → scarica la PNG → rinominala col nome canonico (es. `frana.png`).
4. Salva in `~/Scrivania/disegni/`.
5. Quando hai 1+ immagine pronta, dimmelo. Io:
   - **Verifico visualmente** col tool Read (cerco refusi tipografici, stemmi inventati, date)
   - **Sovrappongo in post-produzione** (Pillow): logo Gruppo Comunale + stemma Comune Genzano + data revisione corretta nel footer + URL stilizzato
   - **Ottimizzo** in PNG grayscale 16 colori (~280 KB)
   - **Aggiorno HTML** della scheda con wrapper minimale (toolbar + img)
   - **Commit + push + deploy**

---

## File checkpoint visivi disponibili in repo

✅ **Logo ufficiale del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma**
   - Path: `static/images/logo-pc-genzano-hires.png`
   - Dimensione: 1080×1080 px, PNG RGBA con trasparenza, ~127 KB
   - Contiene già lo stemma del Comune di Genzano al centro (corona civica + colonna SPQG + alloro + nastro tricolore) — non serve un secondo file separato

✅ **Versione web del logo** (per il sito):
   - `static/images/logo-pc-genzano.png` 480×480 (236 KB) — usata in navbar, structured-data, kit
   - `static/images/logo-pc-genzano.webp` 480×480 (54 KB) — versione WebP per browser moderni

Tutti i file servono allo scopo, niente da recuperare a parte. Font tipografico per data/URL nel footer: **Liberation Sans Bold** (già nel sistema, usato anche da `genera-cover.py` per coerenza istituzionale).
