---
paths:
  - "content/**"
  - "archetypes/**"
  - "data/**"
  - "bozze/**"
  - "social-bozze/**"
  - "static/images/**"
  - "static/video/**"
  - "static/formazione/**"
  - "static/giochi/**"
  - "scripts/genera-cover.py"
  - "scripts/auto-cover-mancanti.py"
  - "scripts/applica-fascia-foto.*"
  - "scripts/genera-social*"
  - "scripts/genera-immagini-social.py"
  - "scripts/social*"
  - "scripts/check-*"
---

# Articoli, foto, gate editoriali e social

Regole spostate da `CLAUDE.md` l'11/11/2026, con il testo integrale, per non caricarle in ogni sessione: si caricano quando si lavora su articoli, pagine, dati, foto, materiali scolastici e bozze social. La sintesi dei divieti assoluti resta in `CLAUDE.md`.

## Foto utente e banner — guarda PRIMA, scrivi DOPO

🔴 Quattro regole cogenti (dettagli in rule 02 + memory `feedback_foto_articoli_guarda_prima`):

1. **Banner col titolo, generato LOCALMENTE prima del commit.** Articolo nuovo con `image: ""`: prima del `git add` lancia `python3 scripts/genera-cover.py <file>`, Read della cover `static/images/<slug>.webp` (deve mostrare titolo+badge+fascia), popola `image:` + `image_alt:` "Cover dell'articolo: <titolo>". Non affidarsi al workflow CI `scarica-foto-automatica.yml` (gira dopo `deploy.yml`). **Rete di sicurezza deterministica (dal 04/06/2026):** `deploy.yml` esegue `scripts/auto-cover-mancanti.py` come step **pre-build** (accanto a QR/Braille), quindi un articolo con `image: ""` non può più andare live col banner SVG di default — ma resta tua responsabilità generare e Read la cover prima del commit (il pre-build è fail-safe, non una scusa per saltare lo step).
2. **Read di OGNI foto utente prima di scrivere caption/alt.** Read multimodale = vedi l'immagine. Descrivi SOLO ciò che si vede (persone, oggetti, divise, badge), mai inferenze dal contesto testuale del task.
3. **Attribuzione default = "Foto: Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma".** Mai a terzi (FEPIVOL/Comune/DPC) solo perché nel task ci sono loro testi. Eccezioni con evidenza certa: pattern nome file social terzi, foto prese dai profili social ufficiali del **Comune di Genzano** (consentite dal 06/11/2026, sempre con «Foto: Comune di Genzano di Roma, dal profilo … ufficiale»; rule 02 § omonimo), Wikimedia/NASA/USGS/NOAA via `pc-image-fixer`, foto storiche con autore noto.
4. **Web check obbligato di OGNI entità citata** (associazione/ente/persona/sigla): WebFetch con denominazione tra virgolette. Se 0 risultati ed è associazione locale poco indicizzata, **non sciogliere l'acronimo a indovinare** (es. *"V.E.R. Formia"*, non *"E.R. Formia"*): cita la sigla come la leggi nella fonte.

**Gate pre-commit con foto utente:** cover+`image:` ✓ · Read di tutte le foto ✓ · caption solo visibile ✓ · attribuzione Gruppo ✓ · web check entità ✓ · **nome mezzo/attrezzatura verificato in `content/chi-siamo/_index.md` § "Mezzi e attrezzature principali"** (la livrea sul fianco non è il modello del veicolo — dettagli in rule 02 § "Nomi dei nostri mezzi") ✓ · gate AGID `pc-article-reviewer` ✓. Un solo punto non verificato → **non committare**.

---

## Auto-gate AGID prima del commit di un articolo

🟢 Ogni articolo nuovo o modificato in modo sostanziale in `content/comunicazioni/`: **prima del `git add` invoca `pc-article-reviewer`** sul file. Commit solo dopo via libera (o dopo aver applicato i fix). Gate **obbligato**, vale anche su singolo articolo. Poi, se l'utente ha detto «pubblica», prosegui con push+PR+merge.

**Eccezione — registro non-AGID solo su richiesta esplicita dell'utente** (comunicato stampa, lettera istituzionale, paper scientifico, relazione tecnica, memoria difensiva, bando, delibera, ordinanza, scheda accademica, o altro genere richiesto): sospendi il gate per quel documento e diventa il miglior professionista di quel genere, applicando le **convenzioni di genere** (piramide rovesciata+5W per il comunicato; intestazione+protocollo per la lettera; IMRaD per il paper; ecc.). Vale solo per quel documento; il prossimo articolo ricade nel gate standard. **L'eccezione la decide l'utente.** Default = AGID 9.5/10 con gate obbligato.

---

## Gate dei fatti e dei materiali scolastici — l'audit esterno non deve più servire

🔴 **Istruzione permanente dell'utente (06/09/2026)**: *«queste cose non devono mai più capitare: non devo più rivolgermi ad altre intelligenze artificiali per fare un audit e poi passartelo»*. Un audit esterno aveva trovato 24 rilievi (11 P1) tutti fondati, con i gate del sito tutti verdi: fatti sbagliati su una tragedia (Rigopiano), istruzioni di sicurezza per bambini da correggere (Tartaruga saggia), rubriche che valutavano la paura, esercizi che spacciavano ipotesi per legge, dati climatici diversi dal dataset, note di sicurezza perse in stampa, pacchetti non paritari, ZIP inutilizzabili offline, privacy e accessibilità da riallineare, favicon vuota, ancore rotte. Da quel giorno valgono quattro gate in più, tutti **obbligati prima del `git add`**:

| Gate | Quando | Agente / script |
|---|---|---|
| **Calendario** | ogni articolo programmato nuovo o modificato, ogni correzione di una data dentro un articolo in coda (nata il 28/09/2026: «15 ottobre: si chiude la stagione AIB» uscito il 28 settembre) | `pc-calendario-editoriale`; `scripts/check-data-uscita.py` (bloccante in `validate-pr.yml`, serale in `controllo-data-uscita.yml`) |
| **Fatti e fonti** | ogni contenuto con dati verificabili (date, orari, bilanci, quantità, cause, norme, citazioni, dati da dataset): articoli, pagine, schede, kit, dossier, manuale | `pc-fact-checker` (richiamato anche da `pc-article-reviewer` § 12); `scripts/check-dati-schede.py`; `scripts/check-dati-canonici.py` (registro `data/dati_canonici.yaml`, bloccante su PR; lo alimenta `pc-coerenza-trasversale`) |
| **Materiali scolastici** | ogni scheda stampabile, kit scuola, kit calamità, rubrica, gioco, percorso nuovo o modificato (`static/formazione/**`, `content/formazione/**`, `static/giochi/**`) | `pc-didattica-reviewer` (sicurezza DPC, pedagogia, età, normativa scuola vigente, esercizi, parità dei 4 formati, licenze, **uso sulla LIM**); `scripts/check-parita-schede.py`; `scripts/check-lim.py` e `scripts/check-sintassi-js.cjs` (regola `lim-scuole.md`) |
| **Scienza e cronaca** | contenuti che spiegano fenomeni, cause, scale, codici colore; articoli di cronaca, anniversari, vicende giudiziarie, contenuti con persone | `pc-revisore-scientifico`, `pc-desk-giornalistico` |
| **Coerenza dei dati** (dal 17/10/2026) | ogni contenuto nuovo o modificato con un dato che il sito scrive anche altrove (orari, quantità, giorni, distanze, numeri, bilanci): il valore nuovo deve coincidere con quello già pubblicato, altrimenti si allinea tutto alla fonte | `pc-coerenza-trasversale` (richiamato da `pc-article-reviewer` § 12-bis e `pc-didattica-reviewer` § 6-bis); `scripts/cerca-incongruenze.py --da-git origin/main` (bloccante su PR) e settimanale su tutto il sito (`controllo-incongruenze.yml`) |
| **Integrità e conformità** | asset, ZIP, ancore, codifiche, stati UI; pagine legali; traduzioni; dati aperti e feed; codice e workflow | `pc-integrita-tecnica`, `pc-conformita-legale`, `pc-revisore-traduzioni`, `pc-dati-e-feed`, `pc-revisore-codice`, `pc-revisore-automazioni`, `pc-sicurezza`; `scripts/check-integrita-asset.py`, `scripts/check-ancore.py` |

**Regole cogenti che i gate applicano:** ogni numero, data o causa ha una **fonte primaria nominata** (INGV, DPC, VVF, ISPRA, Normattiva, MIM, dataset del sito) oppure viene riformulato come stima o ipotesi didattica; un dato sensibile (vittime, cause, istruzioni di sicurezza, norme vigenti) senza fonte è **bloccante**; una correzione fattuale si applica in **tutti** i file che ripetono il dato (schede, dossier, articoli, versioni facili, traduzioni); le istruzioni di autoprotezione per bambini coincidono con il DPC e non contengono divieti o garanzie assoluti senza scenario; le rubriche non usano paura, pianto o agitazione come livello; le avvertenze per l'adulto stanno **dentro** il wrapper stampabile; pagina, stampa singola, «Stampa tutto» e ZIP dicono la stessa cosa (gate `pacchetti-schede` in `validate-pr.yml`).

**Audit interno ricorrente:** `pc-audit-completo` (routine mensile `trig_01RMQwDs5Ku2mRfkwkDZnKmx`, il 3 del mese alle 06:00 italiane) produce lo stesso rapporto di un auditor esterno (rilievi con prova, impatto, correzione, verifica, priorità), corregge la Categoria A fino a live, lascia in PR la Categoria B e apre issue con responsabile per ciò che va validato da Comune, RPD, RSPP o docenti; rapporti in `riferimenti-interni/audit-interni/`. `audit-sito.yml` §§ 46-49 esegue ogni 6 ore integrità asset, ancore, parità schede e dati vs dataset; `scadenze-conformita.yml` tiene il calendario legale (23 settembre, 31 marzo, revisioni annuali).

---

## Umanizzazione della scrittura — prosa naturale, senza tic da IA

🟢 **Dal 19/08/2026, per ogni testo destinato al sito** (articoli, pagine, caption, social): scrivi autentica prosa editoriale italiana — concreta, specifica, con ritmo variato entro il registro breve AGID — evitando i tic statistici degli LLM catalogati da [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Sintesi dei divieti: perifrasi al posto di «è» («rappresenta/costituisce/si configura come»), grappoli di lessico da IA («cruciale/fondamentale/significativo/panorama/testimonianza» — conta la densità, non la singola parola), importanza gonfiata su fatti ordinari, pseudoanalisi al gerundio («evidenziando così…», «sottolineando…»), consenso inventato senza fonte (bloccante), più di un «non solo X, ma anche Y» per articolo, terne-riempitivo di aggettivi, conclusioni prefabbricate («in conclusione», «guardando al futuro»), frasi da assistente virtuale nel contenuto.

**Subordinata ad AGID**: in conflitto vince sempre la regola AGID/WCAG/rischio. **Eccezioni**: versioni `-facile.md` (A2, mai umanizzarle), pagine rischio (strutture fisse), registri di genere richiesti. **Italiano impeccabile sempre** (riferimento nazionale: dubbi → Treccani/Crusca; `check-refusi.py` sui file toccati). Il check è integrato in `pc-article-reviewer` § 10; per le AI esterne è in `AGENTS.md` § 3.5. Versione completa: rule `02-content-design-pa.md` § "Umanizzazione della scrittura" + `manuale/parte-02` § 2.24.

---

## Gate di legalità — Circolare DPC 6/8/2018 (manifestazioni pubbliche)

🔴 Per ogni articolo che descrive cosa fa il Gruppo durante un **evento pubblico** (sagra, festa patronale, Infiorata, commemorazione, manifestazione sportiva, concerto, cerimonia, processione, mercatino, incidente stradale esteso):

**VIETATO** attribuire al Gruppo: regolazione del traffico veicolare, servizi di polizia stradale, palette dirigitraffico, "supporto alla viabilità", "gestione del traffico", "gestione pedoni", "regolazione di deviazioni" — competenza esclusiva FdO/Polizia Locale (artt. 11-12 Codice della Strada, D.Lgs. 285/1992).

**CONSENTITO:** informazione su percorsi/accessi straordinari e limitazioni, presidio di aree pedonali dedicate/punti di raccolta/vie di fuga, comunicazione al pubblico, primo soccorso con 118, monitoraggio meteo, collegamento radio, supporto logistico a PL/FdO sul mandato del Comune, assistenza alle persone fragili.

Articoli operativi: includi un **disclaimer normativo** con link alla [Circolare DPC 6/8/2018](https://www.protezionecivile.gov.it/it/normativa/circolare-del-6-agosto-2018-manifestazioni-pubbliche-precisazioni-sullattivazione-e-limpiego-del-volontariato-di-protezione-civile/). Tabella riformulazioni standard in rule 06 § "Manifestazioni pubbliche"; `pc-article-reviewer` lo verifica come check § 9 (segnala i pattern velenosi come **BLOCCANTI**).

---

## Automatismo totale sugli articoli — Claude decide, l'utente corregge

🟢 Articolo nuovo: eseguo da solo TUTTI i passaggi tecnici ed editoriali (incluso il frontmatter) senza chiedere. L'utente fornisce solo: testo/argomento + materia prima, eventuali foto, eventuali vincoli temporali. Se sbaglio, l'utente corregge — il default è agire, non chiedere.

**Decido in automatico:**

| Campo | Logica di default |
|---|---|
| **Badge** | Cascata: `Allerta`(previsto)→`Emergenza`(in corso)→`Aggiornamento`(concluso)→`Esercitazione`→`Attività`(intervento Gruppo)→`Formazione`→`Volontariato`→`Radiocomunicazioni`→`Prevenzione`→`Evento`→`Avviso`→`Informazione`→`Comunicazione`(fallback). Prevalgono i badge operativi. |
| **Canale** (dal 30/08/2026) | **Derivato dal badge, di norma NON si scrive nel frontmatter**: `Informazione`/`Prevenzione`/`Formazione` → canale "Approfondimenti" (magazine); tutti gli altri badge → canale "Il Gruppo e il territorio" (operativo, in evidenza homepage). Override `canale: "gruppo"`\|`"approfondimenti"` solo se il default sbaglia (es. un'`Informazione` di servizio locale → `gruppo`). Logica nel partial `canale-articolo.html`; dettagli in rule 02 § "Canali editoriali dell'archivio". |
| **Versione facile A2** (`<slug>-facile.md`) | Sì se badge `Allerta`/`Emergenza`/`Prevenzione`, o norme dense (D.Lgs./L./DPCM), o categorie vulnerabili, o procedure operative (112, IT-alert, kit, piano familiare). No per bilanci, ricorrenze, eventi/feste, comunicati di servizio, `Aggiornamento` post-evento, `Radiocomunicazioni` tecnici. |
| **`area`** | "Genzano di Roma" default; cambio se l'articolo è altrove (es. Giro Formia → "Formia (LT)"); vuoto se nazionale/generico. |
| **`scadenza`** | Vuoto, salvo bandi/eventi/allerte con scadenza intrinseca. |
| **`tts: true`** | Sempre (blacklist su pagine legali hard-coded nei template). |
| **`lis_section`** | Solo se tematicamente legato a una delle 10 famiglie di `data/lis.yaml`; altrimenti ometto. |
| **Cover banner** | Sempre (`genera-cover.py` + `image:`/`image_alt:`, REGOLA 1). |
| **Foto utente** | Read → `applica-fascia-foto.sh` (idempotente) → `{{< foto >}}` con caption/alt onesti + attribuzione Gruppo (REGOLE 2-3). |
| **Slide social** (`social_citazione` / `social_punti`) | Compilati DAL testo dell'articolo, **mai inventati**: `social_citazione` = una frase forte/chiave dell'articolo (tra virgolette); `social_punti` = 3-4 punti chiave (date, luoghi, azioni di autoprotezione, numeri utili). Alimentano le slide "citazione" e "In sintesi" del carosello social (`genera-immagini-social.py`). Ometto se l'articolo è troppo breve o privo di contenuto sintetizzabile (es. comunicato di una riga). 🔴 **Devono uscire interi nelle grafiche** (dal 13/10/2026, dopo il post sul soccorso alpino con tre punti tagliati a metà frase): il generatore riduce il corpo o divide la sintesi su più slide e, se non basta, si ferma senza immagini; `scripts/check-grafiche-social.py` lo verifica prima del commit ed è bloccante sulle PR. **`social_video`** (dal 23/09/2026): se l'articolo è fatto di video, `social_video: "/video/<nome>.mp4"` fa uscire un **Reel** su Instagram e un **post video** su Facebook al posto delle immagini; più video si uniscono in un unico MP4 verticale 720×1280 (H.264 Main 3.1, traccia audio anche muta), perché un articolo è un post e il carosello ritaglierebbe il 9:16. **`social_crediti`** (dal 12/11/2026): i crediti che una licenza obbliga a dare per il video (musica, dati del rilievo, licenza della voce di riserva) in una riga; `genera-social.py` la mette parola per parola in fondo ai testi di Instagram e Facebook, prima degli hashtag (`comunicazione-social.md` § «Voce, musica ed effetti dei video»). |
| **Orari degli interventi** | 🔴 **Sempre arrotondati**, mai al minuto ("verso le 18", "poco prima delle 10", "in tarda serata", "fin oltre le 23") — il minuto esatto resta nel registro interno, non negli articoli (rule 10 § promemoria export interventi; richiamo utente 28/08/2026 dopo un articolo live con 9:44/18:04/23:10). |
| **Fonti giornalistiche** | 🔴 **Sempre parafrasate, mai citate nel corpo**: niente "(Castelli Notizie)"/"(Il Mamilio)" inline, niente virgolettati attribuiti a testate, niente frasi copiate. Nel corpo si riprendono **solo i fatti** che il nostro registro non ha, riscritti con parole nostre (attribuzione generica "secondo le cronache locali" se serve); i riferimenti alle testate con link stanno **solo in fondo**, tra le fonti di "Per approfondire" (istruzione utente 28/08/2026; versione completa in rule 02 § "Fonti giornalistiche negli articoli"). |
| **Altri automatismi** | Web check entità (REGOLA 4) · QR (`genera-qr-articoli.py`, doppia rete CI) · indice Pagefind rigenerato in CI dal deploy (mai committato) · spell-check (`check-refusi.py` + `dizionario-pc.txt`) · gate AGID (`pc-article-reviewer`) · commit+push+(se autorizzato)PR+merge. |

**NON decido:** materia prima (testo/foto/argomento), vincoli temporali espliciti, comandi di pubblicazione, genere alternativo non-AGID.

**A fine lavoro** comunico una riga con le decisioni: *"Badge: …; versione facile: …; area: …; scadenza: …; lis_section: …; slide social: …"*. Non chiedo prima — pubblico, poi aggiusto se serve.

---

## Verifica visiva pre-commit su markup HTML nelle pagine

🔴 **Quando modifichi/aggiungi markup HTML custom dentro `content/**/*.md`** (card Bootstrap, blocchi `<div>` con `d-flex`/grid, layout custom, immagini in box affiancati), **`hugo --quiet --minify` NON BASTA**: la build può essere pulita mentre il rendering visivo è rotto. Incidente del 27/05/2026: card affiliazioni con `<div class="d-flex"><img></div>` viste come immagini giganti che schiacciavano il testo affiancato a 5ch di larghezza, con parole a capo lettera per lettera ("schifo" segnalato dall'utente sul live).

**Procedura obbligatoria pre-commit** (5 passi):

1. `hugo server --port 1314 --bind 127.0.0.1 --logLevel error > /tmp/hugo-server.log 2>&1 &` in background
2. `mcp__playwright__browser_navigate` su `http://127.0.0.1:1314/sito-pc-genzano/<percorso-pagina>/` (nota: dev server usa subpath GitHub Pages)
3. `mcp__playwright__browser_take_screenshot` con `element` + `target=".<selettore>"` zoomato sul nuovo blocco
4. **Read del PNG** per verifica multimodale del rendering (vedi davvero come appare)
5. **Solo se il rendering è corretto** → `kill %1` + commit + push. Se sbagliato → fix CSS/markup + ripetere

**Eccezioni** (la verifica visiva non serve):

- Modifiche puramente Markdown standard (paragrafi, liste, link, blockquote, code, tabelle MD pipe).
- Modifiche a frontmatter, data files YAML/JSON, CSS già scoped a classe esistente che NON crea nuova struttura.
- Fix testuale che non cambia struttura DOM (refusi, datazione, link).
- Modifiche a template Hugo / partial che NON introducono nuovi pattern di layout (es. cambio testo, aggiunta classe utility a element esistente).

**Per markup HTML custom (card, grid, flex con img, sezioni inline) la verifica visiva è SEMPRE obbligatoria.** Anche se "sembra ovvio". Meglio 30 secondi di Playwright che 1 ora di figura barbina sul live.

---

## Pubblicazione automatica social — cosa non esce mai da solo

🔴 Dal 20/09/2026 Instagram e Facebook pubblicano **da soli** dal repo **privato** `SviluppoItaliaDigitale/social-pc-genzano`, che legge il materiale da `social-bozze/` di questo repo. 🔴 **Dal 21/09/2026 i post escono in concomitanza con l'articolo sul sito**, non a orari fissi: l'innesco è `genera-social-bozze.yml`, che `deploy.yml` chiama **al termine di ogni deploy** e che sveglia il repo privato appena un articolo pronto risponde sul sito; i post distanziati di mezz'ora li chiama `sveglia-social.yml` in modalità attesa (che resta anche come rete due volte al giorno); i post sono distanziati di almeno mezz'ora fra loro e nessuno esce prima che la pagina risponda davvero sul sito. Il sito non cambia: continua solo a generare le bozze. Vincoli scritti nel codice, non nella configurazione:

- **Mai in automatico i badge `Allerta` ed `Emergenza`**: valgono nel momento in cui escono, si pubblicano a mano.
- **Mai le versioni facili** (`-facile`), **mai un articolo non ancora online** sul sito.
- 🔴 **Gli articoli calendarizzati escono anche loro** (22/09/2026). Il repo privato pubblica solo ciò che ha il materiale in `social-bozze/`, e fino a quel giorno il materiale nasceva solo al commit, quando un articolo scritto in anticipo ha ancora data futura: veniva saltato e nessuno lo riprendeva. Ora nasce quando l'articolo va online (`scripts/social-pronti.py`, testi di riserva dal frontmatter se Gemini non risponde), e il controllo di salute giornaliero segnala ogni articolo online da oltre tre ore rimasto senza materiale o non pubblicato, e i retrodatati (data più vecchia di tre giorni) che il repo privato scarta e vanno pubblicati a mano (salvo `social: false`, dal 05/11/2026: l'articolo resta solo sul sito, senza materiale né segnalazioni). 🔴 `workflow_run` non scatta per i run lanciati col `GITHUB_TOKEN`: un innesco "dopo il deploy" si fa con un dispatch esplicito da `deploy.yml`, mai con `workflow_run`. Dettagli in rule 10 § "Pubblicazione automatica social".
- **Un post per articolo**, appena l'articolo è online; finestra di recupero di 3 giorni (non ripesca l'archivio).
- **Commenti Instagram disattivati** sui post automatici (i canali sono presidiati a orari definiti, vedi `/social-media-policy/`).
- **Menzioni verificate**: `@dpcgov_official`, `@regionelazio.official`, `@comunegenzanodiroma`, `@fepiv_ol`. Un handle non si aggiunge mai per somiglianza col nome dell'ente (rule 02, web check obbligato).

🔴 **Dopo la pubblicazione**: su **Facebook** il testo si riscrive (`scripts/modifica-post.py fb-testo`), su **Instagram no** — l'API accetta solo i commenti, verificato sul campo. Le **immagini non si cambiano su nessuna delle due**: una foto aggiunta a un articolo già pubblicato entra nei post successivi, non in quelli usciti. Per fermare o spostare una pubblicazione si modifica `coda-social.yaml` dell'altro repo, anche da telefono. Dettagli operativi in `manuale/parte-42-pubblicazione-automatica-social.md`, regole in rule 10 § "Pubblicazione automatica social".

---

## Auto-integrazione approfondimenti (video + link) — pre-autorizzata

🟢 Istruzione permanente (20/05/2026): integra da sola gli **approfondimenti pertinenti** (video + link a siti della nostra lista) in articoli e pagine, senza OK caso per caso. Copre l'intero flusso fino a live.

**A) Video** — trigger: issue dai workflow `check-video-lis.yml`, `check-video-dpc-eventi.yml`, `aggiorna-video-correlati.yml`. Se pertinente: video LIS → voce in `data/lis.yaml` (famiglia + `fonte`); video divulgativi/correlati → fix nel **generatore** `scripts/genera-video-correlati.py` (`DENY_VIDEO_IDS`/keyword/gate), **mai solo nel YAML** (rigenerato ogni mese, rule 10); eventuale callout contestuale. Poi chiudi l'issue citando il commit.

**B) Link "Per approfondire"** in fondo all'articolo, ordine AGID: (1) **Sul nostro sito** — linkografia interna, sempre per prima (rule 02 punto 4, agent `pc-internal-linker`); (2) **Fonti istituzionali** (da `content/siti-utili/_index.md`); (3) **Divulgativi** (Geopop, NatGeo Italia, Rai Cultura/News, CICAP, Link4Universe, Wired Italia) etichettando la fonte; (4) **Video Local Team** (`localteam.it`, whitelist) solo clip con esperti/fonti istituzionali, evitando protesta/polemica/cronaca politica, singolo video (non l'hub "insight"), URL pulito.

🔴 **GATE DI PERTINENZA:** video/link solo se trattano una tematica realmente coperta dall'articolo/pagina. Fuori contesto = niente ("approfondimento pertinente o niente"). **Se la pertinenza/classificazione è ambigua, fermati e chiedi.** Pulisci sempre i parametri di tracking (`?si=`, `utm_*`, ecc.). L'apertura di un'issue non avvia da sola una sessione Claude: la regola si applica quando una sessione incontra l'issue o lavora sull'articolo.
