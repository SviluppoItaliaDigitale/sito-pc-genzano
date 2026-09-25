---
name: motion-graphic
description: Video divulgativi di protezione civile fatti interamente in codice (motion graphic) per social, sito e media, in più formati (9:16 Reel/TikTok/Storie/WhatsApp, 4:5 feed, 1:1, 16:9 YouTube/sito/TV). Usala ogni volta che l'utente chiede un video, un Reel, una clip, un'animazione, una "puntata" o un "motion graphic" illustrativo o divulgativo, anche senza nominare la skill.
---

# Motion graphic PC Genzano

Video divulgativi fatti in codice: una pagina HTML autonoma (JS vanilla) disegna ogni fotogramma in funzione del tempo; Chromium la cattura fotogramma per fotogramma e ffmpeg la codifica in MP4. Stessa sorgente, più formati.

**Puntate approvate (riferimento di stile, testate dall'utente)** in `motion/src/`:

| Sorgente | Contenuto | Note |
|---|---|---|
| `allerta-meteo-colori.src.html` | Allerta meteo in 4 colori | spazzata diagonale a 4 bande, pioggia, cerchio dal pallino HUD |
| `allerta-cosa-fare.src.html` | Cosa fare dal verde al rosso | stessa struttura, consigli per livello |
| `kit-emergenza.src.html` | Kit di emergenza, con voce | voce in `motion/voce/kit-emergenza/voce.mp3`, oggetti che volano nello zaino |

Sono solo 9:16 (dimensioni scritte a 1080×1920). **Prima di una puntata nuova, apri almeno una di queste**: riprendi da lì aiutanti, stile e ritmo. Per una puntata in più formati parti dal modello `modello/modello.src.html`, che ha lo stesso motore con i formati già gestiti, e porta dentro le scene dalle puntate approvate.

## Consegna

Per ogni video, in `motion/out/<nome>/` (non committato):

| File | Uso |
|---|---|
| `<nome>-<fmt>.mp4` | **master social**: H.264 High 4.1, 30 fps, yuv420p bt709, faststart, traccia audio (voce o muta) |
| `<nome>-<fmt>-web.mp4` | **versione sito**: 720 px sul lato corto, H.264 **Main 3.1**, audio sempre presente, faststart |
| `<nome>-<fmt>-poster.webp` | anteprima per il sito |
| `<nome>.vtt` | sottotitoli WebVTT, quando c'è la voce |
| `motion/dist/<nome>.html` | pagina autonoma (font e audio in base64) che parte nel browser; tocco = pausa; `?fmt=4x5` ecc. per gli altri formati |

Inviare con `SendUserFile` il master del formato richiesto e l'HTML. Durata tipica 20–55 s.

🔴 **Sul sito va SOLO la versione `-web`.** Il 23/09/2026 i master 1080×1920 High 4.1 senza audio non si riproducevano bene: sono stati ricodificati a 720×1280 Main 3.1 con traccia muta (commit «Video allerta meteo: ricodifica nel formato dei video che funzionano»). È anche il formato che la pubblicazione automatica social richiede per `social_video` (CLAUDE.md, tabella «Automatismo totale»).

## Formati

| `fmt` | Master | Web | Dove si usa | HUD | Testi importanti |
|---|---|---|---|---|---|
| `9x16` | 1080×1920 | 720×1280 | Reel, TikTok, Storie IG/FB, stato WhatsApp, Shorts, `social_video` degli articoli | x 96, y 212 | y 330–1400; niente testo in fondo né a destra in basso |
| `4x5` | 1080×1350 | 720×900 | post nel feed Instagram/Facebook (occupa più schermo del quadrato) | x 96, y 64 | y 190–1130; la griglia del profilo taglia ~40 px ai lati |
| `1x1` | 1080×1080 | 720×720 | feed universale, X, LinkedIn, Telegram | x 80, y 56 | y 160–900 |
| `16x9` | 1920×1080 | 1280×720 | YouTube, pagine e articoli del sito, TV e testate, proiezioni a scuola e negli incontri | x 120, y 56 | y 170–880, margini laterali 160 |

Scelta predefinita: **9:16**. Se l'utente dice «per i social e il sito» producine due (9:16 + 16:9); «per tutto» → tutti e quattro. Nel 16:9 non allargare la colonna verticale: usa la larghezza (griglie 2×2, due colonne testo/illustrazione).

## Contenuti: regole

1. **Verifica ogni affermazione su fonti ufficiali** prima di scrivere: DPC (rischi.protezionecivile.gov.it, tabella allerte e criticità), campagna «Io non rischio» (iononrischio.gov.it), Regione Lazio. Citare le fonti nella risposta e mettere «Fonte: …» nel video. Gate del repo: `pc-fact-checker` sui dati, `pc-revisore-scientifico` su fenomeni e comportamenti.
2. **Dati noti e verificati**: gialla = criticità ordinaria («occasionale pericolo per le persone»), arancione = moderata («pericolo»), rossa = elevata («grave pericolo»); verde = nessuna allerta. Genzano di Roma = **Zona di allerta F · Bacini Costieri Sud**. Numero unico di emergenza **112**. Sito: protezionecivilegenzano.it.
3. **Numeri sensibili** (litri d'acqua del kit, quantità, procedure) solo se validati: nel dubbio, formulazione senza cifra (es. «per almeno 3 giorni») e segnalarlo all'utente, da far controllare al coordinatore.
4. Se le norme ufficiali non sono divise per livello e le divido io, **dirlo esplicitamente** nella consegna.
5. **Tono**: seconda persona singolare, istituzionale ma diretto, zero allarmismo. Preferire forme neutre («Informati», «Controlla»). Niente tic da IA (rule 02 § «Umanizzazione»).
6. **Niente emblema della Croce Rossa** (croce rossa su bianco) né loghi ufficiali: per il pronto soccorso un «+» bianco su fondo azzurro. Personaggi e scene sempre originali e semplici (stile piatto).
7. **Nessun riferimento all'IA** nel video, nei titoli, nei nomi dei file, nei metadati, nei commit e nelle PR (CLAUDE.md § «Nessun riferimento all'IA»).
8. Il Gruppo **non regola il traffico**: mai scene di volontari con palette o che dirigono auto (Circolare DPC 6/8/2018).

## Stile visivo

- Fondo blu notte `#0a1220`, azzurro `#2e90fa`, arancio `#f59e0b`, testo `#eef2f7`, attenuato `#93a1b5`.
- Colori allerta: verde `#34b25a`, giallo `#ffcc00`, arancione `#ff8a00`, rosso `#ef4136`; su questi, testo blu notte.
- Font: Titillium Web 400/600/700/900 (titoli 900), Roboto Mono 500/700 per chip ed etichette maiuscole spaziate. `build.py` li scarica una volta (`npm pack @fontsource/…`, subset latin) e li incorpora in base64.
- Barra in alto (HUD) a pillola alta 72: pallini o caselle di avanzamento + etichetta (es. «ALLERTA METEO», «KIT DI EMERGENZA»). Posizione per formato nella tabella.
- **Il primo fotogramma mostra già contenuto** (fa da anteprima su WhatsApp e da poster).
- Movimenti: scritte che salgono da una maschera (overflow hidden, padding .12em/.22em), pop con easeOutBack, transizione a cerchio di colore dal pallino dell'HUD, spazzata finale con 4 bande colorate, pioggia su canvas che aumenta col livello, lampi rari (max 2 al secondo, overlay bianco ≤ 0,3: WCAG 2.3.1).
- Contrasto: testo chiaro su blu notte, blu notte sui colori di allerta; mai bianco su giallo o arancione.

## Motore (schema obbligatorio)

- Stage `#stage` delle dimensioni del formato; in anteprima scalato con `transform: translate(-50%,-50%) scale(s)`, con `?render=1` a 1:1 senza interfaccia. Formato da `?fmt=` (predefinito `9x16`), tabella `FORMATI` con dimensioni e zone sicure esposte come variabili CSS.
- **Tutto deterministico**: una funzione `render(t)` imposta ogni stile in base al tempo `t`. Niente animazioni CSS, niente `Math.random`, niente `Date`: usare `hash(n)=frac(sin(n*12.9898+78.233)*43758.5453)`.
- Espone `window.__ready=true` (dopo `document.fonts.load` di ogni peso), `window.TOTAL`, `window.renderFrame(t)`; per la voce `window.VOICE_AT` (secondo d'inizio di ogni frase, `null` dove non c'è) e `window.SUBS` (`[{da,a,testo}]` per il VTT); facoltativi `window.KEYFRAMES` (istanti dei provini) e `window.POSTER_T`.
- Aiutanti: `prog(u,s,d)`, easing outCubic/outQuart/inOutCubic/outBack, `reveal()`, `fadeUp()`, `pop()`, `drawRain()` a due passate, `wavePath()` per l'acqua.
- Le scene si generano da un array `CONFIG.scene`; ogni scena ha inizio `START[k]` e durata propria. In cima al file il blocco CONFIG con testi, colori e tempi: è l'unica parte da toccare per le correzioni di testo.
- Segnaposto nel sorgente: `/*FONTS*/`, `/*DUR*/[]` (durate voce), `/*AUDIO*/""` o `src="/*AUDIO*/"` (traccia voce).

## Flusso di lavoro

```bash
S=.claude/skills/motion-graphic/strumenti
cp .claude/skills/motion-graphic/modello/modello.src.html motion/src/<nome>.src.html   # poi modifica CONFIG e scene
python3 $S/voce.py <nome>                          # solo con voce: legge motion/voce/<nome>/testi.txt
python3 $S/render.py <nome> --formati 9x16,16x9 --provini   # 1. fogli di provini: GUARDALI con Read
python3 $S/render.py <nome> --formati 9x16,16x9            # 2. video (+ web, poster, vtt, verifica)
python3 $S/render.py <nome> --formati 9x16 --sito AAAA-MM-GG-slug   # copia web+poster(+vtt) in static/video/
```

Dipendenze installate al volo dagli script: `playwright` (Python) con il Chromium di `/opt/pw-browsers` (**non** eseguire `playwright install`), `pillow`, ffmpeg di sistema oppure `imageio-ffmpeg` (ffmpeg statico con libx264). Circa 0,25 s a fotogramma per formato: oltre ~35 s di video o più formati, lancia in background e controlla il log.

**Controlli obbligatori:**
1. **Prima del video**: leggere `provini-<fmt>.png` (Read multimodale) e cercare sovrapposizioni, discendenti tagliati, testi troppo larghi o fuori dalla zona sicura, contrasto.
2. **Dopo**: leggere `verifica-<fmt>.png` (tre fotogrammi estratti dall'MP4 finito).
3. Controllare con `ffprobe` che la versione web sia Main 3.1 con traccia audio.

## Voce (opzionale)

- Piper TTS, voce `it_IT-paola-medium` (scaricata da huggingface.co/rhasspy/piper-voices in `motion/.cache/piper`). `voce.py` legge `motion/voce/<nome>/testi.txt`: **una riga per scena**, nello stesso ordine di `CONFIG.scene`, `-` per le scene senza voce. Numeri in lettere, parole inglesi a orecchio (es. «pàuer banc»). Parametro: `--length-scale 1.15` (rallentare di più non aiuta: allungando i suoni in modo uniforme le vocali si stiracchiano e le parole si capiscono peggio).
- **Pause di lettura.** Da sola la voce quasi non si ferma sulla virgola (0–0,09 s misurati), poco sui due punti (0,28 s) e per niente sui puntini: gli elenchi escono tirati. `voce.py` legge la riga **intera** (così l'intonazione resta quella naturale: spezzarla non va, perché la voce chiude in discesa anche un pezzo che finisce con la virgola) e poi allunga la pausa dopo ogni segno: virgola 0,32 s · punto e virgola, due punti 0,50 · trattino 0,40 · punto, ? e ! 0,85 · puntini 0,90 (tabella `PAUSE`; ritmo scelto a orecchio dall'utente il 24/09/2026 fra tre campioni). Il punto esatto si trova allineando lo spettro del testo fino al segno, letto da solo, con quello della frase intera (DTW), e la pausa si inserisce nel silenzio che comincia lì, oppure, se la voce lega le parole, nel punto di minima energia con dissolvenze di 8 ms. **Si scrive la punteggiatura come la leggerebbe uno speaker**: una virgola dove serve respirare, i due punti prima di una spiegazione. 🔴 **Dentro la frase la pausa si allunga solo dove la voce respira già** (silenzio naturale di almeno 60 ms, `GAP_NATURALE`): negli elenchi la voce lega le parole, e un silenzio infilato a forza suona come un inceppo, non come una pausa (segnalato dall'utente ascoltando il video sull'alluvione, 25/09/2026: «in alcuni punti la lettura si blocca»). A fine frase e con `|` la pausa si allunga sempre. Per una pausa **senza segno scritto** si usa `|` nel testo parlato (0,45 s; non compare nei sottotitoli, che stanno nella scena). Verificato il 24/09/2026 trascrivendo con un riconoscitore vocale ogni tratto fra due pause delle tre puntate: nessuna parola spostata da un tratto all'altro.
- Durata scena = durata frase + 0,45 s prima + 0,75 s dopo (+0,5 s se c'è un'uscita animata): il modello lo calcola da `DUR`.
- `render.py` monta la traccia: `adelay` di ogni frase a `VOICE_AT[k]`, `amix normalize=0`, `apad`, `atrim` a TOTAL, `loudnorm I=-16:TP=-1.5`, mp3 96k; poi la unisce al video e la incorpora nell'HTML (pulsante «Tocca per avviare (con audio)»).
- **Registrazione umana**: se l'utente manda la propria voce, montarla in `motion/voce/<nome>/voce.mp3` (allineata ai `VOICE_AT`) — `render.py` e `build.py` la usano al posto di Piper.
- Sottotitoli sempre visibili in un riquadro (43 px, y≈1240 nel 9:16) + file `.vtt`. Il testo **parlato** sta in `testi.txt` (numeri in lettere: «centododici»), quello **mostrato** nel campo `sottotitolo` della scena (numeri in cifre: «112»): tenerli allineati parola per parola.
- **Controllo della pronuncia prima del rendering** (senza ascoltare): `voce.py` scrive `motion/voce/<nome>/fonemi.txt`, cioè come Piper pronuncerà ogni parola in IPA (`ˈ` = accento; `ɛ`/`ɔ` = e/o aperte, `e`/`o` = chiuse). Le parole a rischio (accento non sulla penultima, nomi propri, sigle, e ogni parola con **e/o accentata**, perché aperta o chiusa cambia la pronuncia) sono confrontate **in automatico con il DiPI**, il *Dizionario di pronuncia italiana* di Luciano Canepari (dipionline.it, contiene anche i nomi di luogo), con una richiesta al secondo e cache in `motion/.cache/dipi.json`. Segni: `=` il DiPI conferma; `≠` accento o timbro diversi, **da correggere**; `!` parola assente dal DiPI (spesso una forma coniugata: si cerca la forma base, es. «cresce» → «crescere», poi Treccani), da verificare a mano; `✓` già nel lessico.
- **Fonti, in quest'ordine**: (1) **DiPI** (automatico); (2) **Vocabolario Treccani** per le parole comuni (il lemma riporta accento e timbro, es. «àncora»); (3) **Wikipedia in italiano** per i nomi di luogo: trascrizione `{{IPA|…}}` nell'incipit della voce (API `action=parse&prop=wikitext&section=0`, con User-Agent e pause di 20–25 s: senza, risponde 429); (4) se nessuna fonte la riporta, si chiede all'utente. Il **DOP della RAI** (dizionario.rai.it) al 24/09/2026 ha il **certificato HTTPS scaduto**: non si consulta finché non viene rinnovato (la verifica TLS non si disattiva mai).
- **Correzione**: si forza l'accento scrivendolo (grave = aperta o accento semplice, acuto = chiusa: «àncora», «Gandòlfo», «pésca») nel **lessico condiviso** `motion/voce/pronuncia.tsv` (parola, grafia per la voce, fonte), che `voce.py` applica a tutte le puntate; le parole verificate e già corrette si registrano con la grafia uguale alla parola, così non si ricontrollano. Mai correggere a orecchio. Errori trovati così nella puntata sugli incendi (24/09/2026): «incéndio», «centodòdici», «protéggerlo», «còrre» — la voce sbaglia il timbro più spesso dell'accento.
- **Non posso ascoltare l'audio**: chiedere sempre all'utente di verificare la pronuncia e offrire di rimontare su una sua registrazione.

## Pubblicazione sul sito

- File in `static/video/AAAA-MM-GG-slug.mp4` + `-poster.webp` (+ `.vtt`); i formati diversi dal 9:16 hanno il suffisso `-4x5`, `-1x1`, `-16x9`.
- Nell'articolo: shortcode `{{< video src="/video/…mp4" poster="/video/…-poster.webp" titolo="…" >}}` e, sotto, la **trascrizione** del parlato o dei testi (WCAG 1.2: il video non è l'unico veicolo dell'informazione). Lo shortcode `video` oggi non gestisce `<track>`: i sottotitoli sono impressi nel video, il `.vtt` resta pronto per quando servirà (YouTube, testate, un'estensione dello shortcode). Tutti i gate dell'articolo restano (`pc-article-reviewer`, cover, ecc.).
- Per i social automatici: `social_video: "/video/AAAA-MM-GG-slug.mp4"` nel frontmatter (versione web 9:16).
- Sorgenti in `motion/src/` e testi della voce in `motion/voce/` **si committano** (sono la memoria del lavoro: le puntate del 23/09/2026 erano sopravvissute solo come HTML finiti); `motion/out/`, `motion/dist/`, `motion/.cache/` e i `line_*.wav` no.

## Chiusura della consegna

Una riga su cosa contiene il video e in quali formati, note sui dati da validare (e su eventuali divisioni per livello fatte da me), fonti in fondo come link.
