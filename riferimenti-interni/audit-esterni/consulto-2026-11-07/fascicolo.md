# Fascicolo del sito per l'audit del 07/11/2026

Fascicolo preparato per i revisori che non possono aprire il sito: contiene ciò che il sito pubblicato mostrava il 07/11/2026 fra le 11:13 e pochi minuti dopo (ora italiana).

- **Come è fatto.** Ogni pagina è stata scaricata da https://www.protezionecivilegenzano.it con una richiesta HTTP vera. Per ogni pagina: codice di risposta, peso dell'HTML, tempo di risposta, titolo, descrizione, lingua dichiarata, numero di titoli H1, immagini senza testo alternativo, struttura dei titoli (H1, H2, H3) e il testo del contenuto principale (elemento `<main>`), tagliato quando è lungo. Le intestazioni HTTP sono quelle della home. Menu e numero di pagine vengono dal repository pubblico e dalla mappa del sito.
- **Limiti.** Il JavaScript non è stato eseguito: le parti che il browser costruisce dopo il caricamento (assistente, cruscotto, barra dell'allerta aggiornata, ricerca) qui compaiono solo con il testo di partenza. Nessuna prova di accessibilità in un browser. Prima dell'invio lo strumento toglie dal testo numeri di telefono, email e codici: dove leggi «[telefono tolto]» o «[email tolta]» il sito mostra un numero o un indirizzo, e non è un difetto del sito.

## 1. Il sito in breve

- **Chi lo pubblica.** Il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma (vedi il testo della pagina «Chi siamo» al § 3).
- **Come è fatto.** Sito statico generato con Hugo e il tema Bootstrap Italia, pubblicato su un hosting Aruba (copia di anteprima su GitHub Pages); repository pubblico `SviluppoItaliaDigitale/sito-pc-genzano`.
- **Pagine nella mappa del sito** (`/sitemap.xml`): 1492. Per sezione (prime 25): comunicazioni 535, formazione 503, dossier 53, formazionepc 42, giochi 38, manuale 35, catalogo-giochi 35, abili-a-proteggere 33, standard-iso 32, conoscere 29, rischi-prevenzione 21, normativa 10, scuole 8, english 7, kit-organizzazioni 5, francais 5, deutsch 5, facile-da-leggere 5, sala-stampa 4, romana 4, espanol 4, esperanto 4, portugues 4, quizpc 3, stato-del-territorio 2.
- **Menu principale** (da `hugo.toml`):
  - Home (/)
  - Per il Cittadino: Da dove comincio? (/da-dove-comincio/); Cosa Fare Adesso (/cosa-fare-adesso/); Allerte Meteo (/allerte-meteo/); Rischi e Prevenzione (/rischi-prevenzione/); Cartografia (/cartografia/); Numeri Utili (/numeri-utili/); Piano Familiare (/piano-familiare/); Kit pronti per situazioni vulnerabili (/formazione/kit-calamita/); Cruscotto del territorio (/cruscotto/)
  - Per le scuole: Formazione e scuole (/formazione/); Percorsi didattici pronti (/formazione/percorsi-didattici/); Crea la mia lezione (/formazione/crea-la-mia-lezione/); Schede didattiche stampabili (/formazione/schede-stampabili/); Per i docenti — Ed. Civica (/formazione/educazione-civica/); Storie e Racconti (/formazione/storie-e-racconti/); Giochi della Sicurezza (/giochi/); Il libro che si esplora (/formazione/libro-che-si-esplora/); Esperimenti e attività (/formazione/esperimenti/); Laboratorio meteo (/laboratorio-meteo/)
  - Accessibilità e Supporti: Abili a Proteggere (/abili-a-proteggere/); Facile da Leggere (/facile-da-leggere/); Contenuti in LIS (/lis/); Tabelle di comunicazione (CAA) (/tabelle-comunicazione/); Poster di emergenza multilingua (/poster-emergenza/)
  - Volontariato: Diventa Volontario (/diventa-volontario/); Chi Siamo (/chi-siamo/); La campagna social (/campagna-volontari/); Per gli enti e le scuole (/per-gli-enti/); Il nostro patrono (/san-pio-da-pietrelcina/); Addestramento e buone pratiche (/esercitazioni/)
  - Risorse: Conoscere la Protezione Civile (/conoscere/); Manuale di Protezione Civile (/manuale/); Dossier interattivi (/dossier/); FAQ (/faq/); Glossario (/glossario/); Area Download (/area-download/); Normativa (/normativa/); Strumenti in Tempo Reale (/strumenti/); Audio e podcast (/audio-e-podcast/)
  - Comunicazioni (/comunicazioni/)
  - Contatti (/contatti/)

## 2. Misure del sito pubblicato

| Pagina | Codice | HTML (KB) | Tempo (s) | Lingua | H1 | Immagini (senza alt / alt vuoto) | Link | Script | Fogli di stile | Titolo |
|---|---|---|---|---|---|---|---|---|---|---|
| `/` | 200 | 99.9 | 0.93 | it | 1 | 16 (0 / 10) | 164 | 27 | 5 | Protezione Civile Genzano di Roma |
| `/emergenza/` | 200 | 12.8 | 0.64 | it | 1 | 0 (0 / 0) | 20 | 0 | 0 | Pagina di Emergenza — Protezione Civile Genzano di Roma |
| `/cosa-fare-adesso/` | 200 | 129.1 | 0.78 | it | 1 | 6 (0 / 1) | 143 | 22 | 4 | Cosa fare adesso — Protezione Civile Genzano di Roma |
| `/allerte-meteo/` | 200 | 175.2 | 0.77 | it | 1 | 13 (0 / 1) | 181 | 24 | 5 | Allerte meteo — Protezione Civile Genzano di Roma |
| `/numeri-utili/` | 200 | 124.2 | 0.77 | it | 1 | 6 (0 / 1) | 137 | 22 | 4 | Numeri utili — Protezione Civile Genzano di Roma |
| `/rischi-prevenzione/` | 200 | 82.8 | 0.66 | it | 1 | 6 (0 / 1) | 164 | 22 | 4 | Rischi e prevenzione — Protezione Civile Genzano di Roma |
| `/rischi-prevenzione/rischio-sismico/` | 200 | 163.3 | 0.98 | it | 1 | 8 (0 / 1) | 172 | 24 | 4 | Rischio Sismico: Cosa Fare — Protezione Civile Genzano di Roma |
| `/rischi-prevenzione/rischio-idrogeologico/` | 200 | 150.7 | 0.9 | it | 1 | 8 (0 / 1) | 167 | 24 | 4 | Rischio Idrogeologico — Protezione Civile Genzano di Roma |
| `/piano-emergenza/` | 200 | 131.3 | 0.76 | it | 1 | 6 (0 / 1) | 136 | 22 | 4 | Piano di emergenza comunale — Protezione Civile Genzano di Roma |
| `/aree-attesa/` | 200 | 120.7 | 1.1 | it | 1 | 6 (0 / 1) | 120 | 22 | 4 | Aree di attesa di Genzano di Roma — Protezione Civile Genzano di Roma |
| `/piano-familiare/` | 200 | 153.9 | 0.89 | it | 1 | 9 (0 / 1) | 138 | 22 | 4 | Piano di emergenza familiare — Protezione Civile Genzano di Roma |
| `/diventa-volontario/` | 200 | 136.6 | 0.85 | it | 1 | 8 (0 / 1) | 137 | 22 | 4 | Diventa volontario — Protezione Civile Genzano di Roma |
| `/chi-siamo/` | 200 | 135.6 | 0.97 | it | 1 | 11 (0 / 1) | 122 | 22 | 4 | Chi siamo — Protezione Civile Genzano di Roma |
| `/contatti/` | 200 | 120.9 | 0.76 | it | 1 | 6 (0 / 1) | 129 | 22 | 5 | Contatti e sede — Protezione Civile Genzano di Roma |
| `/accessibilita/` | 200 | 112.3 | 0.76 | it | 1 | 6 (0 / 1) | 141 | 22 | 4 | Dichiarazione di accessibilità — Protezione Civile Genzano di Roma |
| `/formazione/` | 200 | 132.5 | 0.88 | it | 1 | 6 (0 / 1) | 172 | 22 | 4 | Formazione e scuole — Protezione Civile Genzano di Roma |
| `/facile-da-leggere/` | 200 | 131.5 | 0.76 | it | 1 | 17 (0 / 1) | 134 | 22 | 4 | Facile da leggere — Protezione Civile Genzano di Roma |
| `/english/` | 200 | 73.0 | 0.65 | en | 1 | 5 (0 / 1) | 129 | 22 | 4 | English — Civil Protection Genzano di Roma — PC Genzano di Roma |
| `/assistente/` | 200 | 136.1 | 0.76 | it | 1 | 5 (0 / 1) | 110 | 22 | 4 | Assistente — Cosa devo fare? — Protezione Civile Genzano di Roma |
| `/cruscotto/` | 200 | 296.4 | 0.88 | it | 1 | 13 (0 / 2) | 223 | 22 | 5 | Cruscotto del territorio — Protezione Civile Genzano di Roma |
| `/privacy/` | 200 | 82.0 | 0.65 | it | 1 | 6 (0 / 1) | 140 | 22 | 4 | Privacy e cookie policy — Protezione Civile Genzano di Roma |
| `/lim/` | 200 | 122.6 | 0.75 | it | 1 | 6 (0 / 1) | 132 | 23 | 4 | Protezione civile sulla LIM: giochi, schede e lezioni per la lavagna interattiva — PC Genzano di Roma |
| `/comunicazioni/` | 200 | 836.7 | 1.28 | it | 1 | 539 (0 / 535) | 1207 | 23 | 4 | Comunicazioni e Notizie — Protezione Civile Genzano di Roma |
| `/monitor/` | 200 | 319.4 | 0.88 | it | 0 | 1 (0 / 0) | 2 | 4 | 1 | Sala situazioni — Protezione Civile Genzano di Roma |
| `/giochi/` | 200 | 9.6 | 0.43 | it | 1 | 0 (0 / 0) | 8 | 4 | 6 | Arena PC Genzano — Giochi della Sicurezza |
| `/cerca/` | 200 | 67.7 | 0.66 | it | 1 | 5 (0 / 1) | 110 | 23 | 5 | Cerca nel sito — Protezione Civile Genzano di Roma |
| `/mappa-sito/` | 200 | 120.6 | 0.76 | it | 1 | 6 (0 / 1) | 276 | 22 | 4 | Mappa del Sito — Protezione Civile Genzano di Roma |
| `/sala-stampa/` | 200 | 128.9 | 0.95 | it | 1 | 6 (0 / 1) | 156 | 22 | 4 | Sala stampa — Protezione Civile Genzano di Roma |
| `/laboratorio-meteo/` | 200 | 83.4 | 0.65 | it | 1 | 5 (0 / 1) | 131 | 22 | 4 | Laboratorio meteo: gioca con i dati del clima — PC Genzano di Roma |
| `/glossario/` | 200 | 134.6 | 0.76 | it | 1 | 6 (0 / 1) | 224 | 23 | 4 | Glossario di protezione civile — Protezione Civile Genzano di Roma |
| `/faq/` | 200 | 133.1 | 0.96 | it | 1 | 6 (0 / 1) | 140 | 23 | 4 | Domande frequenti — Protezione Civile Genzano di Roma |
| `/normativa/` | 200 | 124.0 | 0.75 | it | 1 | 7 (0 / 2) | 139 | 22 | 4 | Normativa di protezione civile — Protezione Civile Genzano di Roma |
| `/volontariato/` → /diventa-volontario/ | 200 | 136.6 | 1.2 | it | 1 | 8 (0 / 1) | 137 | 22 | 4 | Diventa volontario — Protezione Civile Genzano di Roma |
| `/meteo/` → /allerte-meteo/ | 200 | 175.2 | 1.19 | it | 1 | 13 (0 / 1) | 181 | 24 | 5 | Allerte meteo — Protezione Civile Genzano di Roma |
| `/pagina-che-non-esiste/` | 404 | 64.1 | 0.65 | it | 1 | 5 (0 / 1) | 120 | 22 | 4 | Pagina non trovata — Protezione Civile Genzano di Roma |

Intestazioni HTTP della home (tutte quelle che riguardano sicurezza, cache e licenza):

```
Server: aruba-proxy
Content-Type: text/html; charset=UTF-8
X-Content-Type-Options: nosniff
X-Frame-Options: SAMEORIGIN
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(self), microphone=(), camera=()
Cross-Origin-Opener-Policy: same-origin-allow-popups
Strict-Transport-Security: max-age=31536000; includeSubDomains
Link: <https://creativecommons.org/licenses/by-nc-sa/4.0/>; rel="license"
TDM-Reservation: 1
TDM-Policy: https://www.protezionecivilegenzano.it/note-legali/
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: https:; font-src 'self' data:; connect-src 'self' https://raw.githubusercontent.com https://api.github.com https://*.openstreetmap.org https://*.tile.openstreetmap.org https://webservices.ingv.it https://*.ingv.it https://radar-api.protezionecivile.it https://*.protezionecivile.it https://api.open-meteo.com https://marine-api.open-meteo.com https://air-quality-api.open-meteo.com https://archive-api.open-meteo.com https://*.arpalazio.gov.it https://eccharts.ecmwf.int https://rapidmapping.emergency.copernicus.eu https://maps.mistralportal.it https://meteohub.agenziaitaliameteo.it https://earthquake.usgs.gov https://eonet.gsfc.nasa.gov https://www.seismicportal.eu https://www.ioc-sealevelmonitoring.org https://services.swpc.noaa.gov https://api.v2.sondehub.org https://celestrak.org https://*.celestrak.org https://view.eumetsat.int https://stac.dataspace.copernicus.eu https://gibs.earthdata.nasa.gov https://sdr.noantri.org https://sdr-plus.i6iqx.it wss://sdr.noantri.org wss://sdr-plus.i6iqx.it wss://ws1.blitzortung.org wss://ws3.blitzortung.org wss://ws7.blitzortung.org wss://ws8.blitzortung.org https://gc.zgo.at https://apicuollo.goatcounter.com; frame-src https://www.vesselfinder.com https://embed.windy.com https://www.windy.com https://embed.waze.com https://sdr.noantri.org https://sdr-plus.i6iqx.it https://*.ingv.it https://terremoti.ingv.it https://map.blitzortung.org https://www.youtube.com https://www.youtube-nocookie.com https://*.protezionecivile.gov.it https://*.regione.lazio.it https://mappe.protezionecivile.gov.it; frame-ancestors 'self'; form-action 'self'; base-uri 'self'; object-src 'none'; upgrade-insecure-requests
Cache-Control: no-store, no-cache, must-revalidate, max-age=0
Pragma: no-cache
Expires: 0
Last-Modified: Sat, 07 Nov 2026 10:08:03 GMT
```

`/robots.txt` (codice 200):

```
User-agent: *
Allow: /
Sitemap: https://www.protezionecivilegenzano.it/sitemap.xml
Sitemap: https://www.protezionecivilegenzano.it/news-sitemap.xml

# Nota: le URL legacy del vecchio sito (*.html, /documenti/*, ecc.) NON
# sono più bloccate da robots.txt. Il blocco impediva a Googlebot di
# scansionare la pagina e quindi di seguire il Redirect 301 del .htaccess
# o il meta refresh dell'alias HTML, lasciandole indefinitamente nello
# stato "Esclusa per noindex" o "Bloccata da robots.txt" in Search Console.
# Lasciandole accessibili al crawler, Google segue il 301 server-side e
# aggiorna l'indice in 1-2 cicli di scansione.

# Cartelle infrastrutturali del vecchio CMS Joomla (/cache/, /sito_pc/,
# /sitovecchio/): rispondono già con un 301 verso la home dal .htaccess.
# Non vanno bloccate qui, altrimenti Googlebot non può seguire il redirect
# e le URL restano "bloccate da robots.txt" in Search Console (audit 25/09/2026).
```

Ultimi articoli (dal feed `/comunicazioni/index.xml`, codice 200):

- Sat, 07 Nov 2026 — Piemonte, 5-6 novembre 1994: l'alluvione del Tanaro che cambiò le regole (/comunicazioni/2026-11-07-piemonte-1994-alluvione-tanaro/)
- Fri, 06 Nov 2026 — Piano di emergenza condominiale: anche il palazzo ha bisogno del suo piano (/comunicazioni/2026-11-06-piano-emergenza-condominio/)
- Thu, 05 Nov 2026 — Palo della luce danneggiato in corso Don Minzoni: area messa in sicurezza (/comunicazioni/2026-11-05-palo-luce-via-belardi-messa-in-sicurezza/)
- Thu, 05 Nov 2026 — 5 novembre, Giornata mondiale per la consapevolezza sui maremoti: cosa deve sapere chi va al mare (/comunicazioni/2026-11-05-giornata-mondiale-consapevolezza-maremoti/)
- Thu, 05 Nov 2026 — Ondate di freddo: come prepararsi e proteggere gli anziani (/comunicazioni/2026-11-05-ondate-freddo-prevenzione-anziani/)
- Wed, 04 Nov 2026 — Neve e catene: la mossa giusta si fa a casa (/comunicazioni/2026-11-04-neve-catene-video/)
- Wed, 04 Nov 2026 — Genova, 4 novembre 2011: l'alluvione del Fereggiano e la lezione dei rii tombati (/comunicazioni/2026-11-04-genova-2011-alluvione-fereggiano/)
- Wed, 04 Nov 2026 — 4 novembre 1966: l'alluvione di Firenze e la nascita degli Angeli del fango (/comunicazioni/2026-11-04-alluvione-firenze-1966-angeli-fango/)
- Wed, 04 Nov 2026 — 4 novembre: le Forze Armate e il loro ruolo nella Protezione Civile (/comunicazioni/2026-11-04-forze-armate-ruolo-protezione-civile/)
- Tue, 03 Nov 2026 — Vincolo idrogeologico nel Lazio: la Regione propone di sostituire le mappe del 1923 (/comunicazioni/2026-11-03-vincolo-idrogeologico-lazio-mappe-1923-riordino/)
- Tue, 03 Nov 2026 — Terremoto: una casa vista dall'interno, un video in 3D (/comunicazioni/2026-11-03-terremoto-casa-interno-video-3d/)
- Tue, 03 Nov 2026 — Pneumatici invernali e catene: le regole dal 15 novembre (/comunicazioni/2026-11-03-pneumatici-invernali-catene-novembre/)
- Mon, 02 Nov 2026 — Commemorazione dei defunti: memoria e cura collettiva (/comunicazioni/2026-11-02-commemorazione-defunti-cultura-lutto/)
- Sun, 01 Nov 2026 — Albero caduto in viale Fratelli Rosselli: colpite due auto in sosta (/comunicazioni/2026-11-01-albero-caduto-viale-fratelli-rosselli-auto/)
- Sun, 01 Nov 2026 — Ognissanti: viabilità nei pressi dei cimiteri e comportamenti (/comunicazioni/2026-11-01-ognissanti-cimiteri-viabilita/)
- Sat, 31 Oct 2026 — Halloween a Genzano: il Gruppo in piazza Frasconi con la Misericordia (/comunicazioni/2026-10-31-halloween-genzano-piazza-frasconi/)
- Sat, 31 Oct 2026 — San Giuliano di Puglia, 31 ottobre 2002: il terremoto che cambiò la sicurezza sismica delle scuole italiane (/comunicazioni/2026-10-31-san-giuliano-puglia-2002-scuole-sicure/)
- Fri, 30 Oct 2026 — Norcia, 30 ottobre 2016: la scossa più forte d'Italia degli ultimi 30 anni (/comunicazioni/2026-10-30-norcia-2016-decimo-anniversario-sequenza-centro-italia/)
- Fri, 30 Oct 2026 — Halloween in sicurezza: consigli per genitori e bambini (/comunicazioni/2026-10-30-halloween-sicurezza-bambini/)
- Thu, 29 Oct 2026 — Il terremoto dalla A alla Z: un video in 3D, da Messina 1908 a oggi (/comunicazioni/2026-10-29-terremoto-dalla-a-alla-z-video-3d/)
- Thu, 29 Oct 2026 — Tempesta Vaia, 29 ottobre 2018: il vento che ha cambiato il volto delle Dolomiti (/comunicazioni/2026-10-29-tempesta-vaia-2018-vento-foreste-cambiamento-climatico/)
- Wed, 28 Oct 2026 — La differenza è una scelta: il nostro video sul volontariato (/comunicazioni/2026-10-28-la-differenza-e-una-scelta-video/)
- Wed, 28 Oct 2026 — Fuoco a bordo di un veicolo: un video in 3D su cosa fare e come usare l'estintore (/comunicazioni/2026-10-28-estintori-veicoli-video-3d/)
- Wed, 28 Oct 2026 — Dentro l'estintore: un video in 3D su come funziona e quale usare (/comunicazioni/2026-10-28-estintori-video-3d/)
- Wed, 28 Oct 2026 — Come si rileva il danno sismico a una chiesa: la scheda Modello A-DC del Dipartimento di Protezione Civile (/comunicazioni/2026-10-28-scheda-rilievo-danno-beni-culturali-chiese/)

## 3. Testo delle pagine principali

### `/` — Protezione Civile Genzano di Roma

- Descrizione: Sito ufficiale del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma. Allerte meteo, rischi, prevenzione e come diventare volontario.
- Titoli: H1 Protezione Civile Genzano di Roma · H2 Da dove iniziare? · H3 Sono in emergenza ora · H3 Voglio prepararmi · H3 Sono docente o scuola · H3 Sono caregiver o persona fragile · H3 Sono un genitore · H3 Sono uno studente o studentessa · H2 Cosa fare in caso di... · H2 Numeri di Emergenza · H2 Il Gruppo e il territorio · H3 Palo della luce danneggiato in corso Don Minzoni: area messa in sicurezza · H3 Albero caduto in viale Fratelli Rosselli: colpite due auto in sosta · H3 Halloween a Genzano: il Gruppo in piazza Frasconi con la Misericordia · H3 La differenza è una scelta: il nostro video sul volontariato · H3 Dal 23 al 25 ottobre: rami pericolanti e una ricerca alle Piagge · H2 Meteo a Genzano di Roma e nel Lazio · H2 Servizi per il cittadino · H3 Da dove comincio? · H3 Cosa devo fare? · H3 Facile da Leggere · H3 Rischi e Prevenzione · H3 Numeri Utili · H3 Cartografia Operativa · H3 Strumenti in Tempo Reale · H3 Lo stato del territorio · H3 Abili a Proteggere · H3 Area Download · H2 «Non c'è Protezione Civile senza di te» · H2 Approfondimenti · H3 Piemonte, 5-6 novembre 1994: l'alluvione del Tanaro che cambiò le regole · H3 Piano di emergenza condominiale: anche il palazzo ha bisogno del suo piano · H3 5 novembre, Giornata mondiale per la consapevolezza sui maremoti: cosa deve sapere chi va al mare · H2 Comunità e canali · H2 Giochi della Sicurezza · H3 Piccoli Esploratori · H3 Scuola Primaria · H3 Ragazzi e Famiglie · H3 Tutti i giochi · H2 QR code dell'articolo

```text
Numero Unico Emergenza: 112
|
Sala Operativa Protezione Civile Lazio: 803 555
|
NESSUNA ALLERTA
— Non sono previsti fenomeni significativi sul nostro territorio.
Bollettino Ufficiale
Verificato:
7 novembre 2026, 07:11
· Fonte:
Centro Funzionale Lazio
Protezione Civile
Genzano di Roma
Gruppo Comunale Volontari — istituito nel 1991, volontari al servizio della comunità dal 1981.
Allerte Meteo
Piano di Emergenza
Diventa Volontario
45
Anni di Attività
: leggi la storia del Gruppo nella pagina Chi siamo
12
Mezzi e attrezzature
: vedi l'elenco nella pagina Chi siamo
20+
Emergenze Nazionali
: vedi eventi e calamità significative nella pagina Chi siamo
365
Giorni di Operatività
: scopri il Gruppo nella pagina Chi siamo
Da dove iniziare?
Scegli la card che fa al caso tuo: ti porta in 1 click ai contenuti giusti.
Sono in emergenza ora
Pagina ultra-leggera: 112, stato allerta, cosa fare adesso, numeri essenziali, aree di attesa.
Voglio prepararmi
Piano familiare interattivo, kit emergenza, rischi del territorio, aree di attesa, allerte meteo.
Sono docente o scuola
Kit didattici per ogni fascia, schede stampabili, storie, giochi, normativa scolastica.
Sono caregiver o persona fragile
Kit pronti per anziani, neonati, disabilità, terapie salvavita, animali, caregiver, italiano L2.
Sono un genitore
Piano familiare, fiabe e storie della sicurezza, kit pronti per situazioni vulnerabili, attività a casa dopo la scuola.
Sono uno studente o studentessa
Giochi della sicurezza per fascia (3-19 anni), storie e racconti, versione facile da leggere, cosa è un rischio.
Cosa fare in caso di...
Terremoto
Scopri come proteggerti
Alluvione
Norme di comportamento
Incendio
Previeni e segnala
Piano Familiare
Crea il tuo piano
Numeri di Emergenza
Numero Unico Emergenze
112
Per qualsiasi emergenza
Sala Operativa PC Lazio
803 555
Segnalazioni non urgenti
Tutti i numeri utili
Il Gruppo e il territorio
Avvisi, interventi e attività del Gruppo Comunale a Genzano di Roma e nei Castelli Romani.
Attività
5 novembre 2026
Palo della luce danneggiato in corso Don Minzoni: area messa in sicurezza
Giovedì pomeriggio un palo della luce urtato da un mezzo si è piegato in corso Don Minzoni. Il Gruppo ha delimitato l'area; il palo è stato rimosso.
Attività
Albero caduto in viale Fratelli Rosselli: colpite due auto in sosta
1 novembre 2026
Attività
Halloween a Genzano: il Gruppo in piazza Frasconi con la Misericordia
31 ottobre 2026
Volontariato
La differenza è una scelta: il nostro video sul volontariato
28 ottobre 2026
Aggiornamento
Dal 23 al 25 ottobre: rami pericolanti e una ricerca alle Piagge
25 ottobre 2026
Tutte le comunicazioni
Meteo a Genzano di Roma e nel Lazio
Temperatura e cielo previsti oggi, con il dettaglio completo di Genzano di Roma. Aggiornata automaticamente su dati aperti Open-Meteo.
Previsione meteo informativa
— non sostituisce i
bollettini ufficiali di allertamento
del Centro Funzionale Regionale del Lazio.
Lazio e dettaglio completo di Genzano di Roma.
Scarica
Condividi
Approfondisci il meteo
Vuoi vedere di più?
Sulla pagina
Allerte meteo
trovi la carta sinottica dell'Italia, l'animazione e il radar pioggia in tempo reale.
Dati in tempo reale
Cruscotto del territorio
[… testo tagliato: la pagina continua per circa 3048 caratteri]
```

### `/emergenza/` — Pagina di Emergenza — Protezione Civile Genzano di Roma

- Descrizione: Pagina ultra-leggera per consultazione rapida in caso di emergenza o rete debole. Solo testo essenziale, niente widget pesanti.
- Titoli: H1 Pagina di Emergenza — chiama il 112 in caso di pericolo · H2 Numeri essenziali · H2 Cosa fare ora

```text
Pagina di Emergenza — chiama il 112 in caso di pericolo
ℹ️
Pagina ultra-leggera
per emergenze e rete debole. Per il sito completo:
homepage
. Per accessibilità cognitiva:
facile da leggere
.
In emergenza chiama subito
112
Numero Unico Emergenze (NUE)
📞 Chiama ora
Stato allerta meteo: NESSUNA ALLERTA
(livello verde)
Non sono previsti fenomeni significativi sul nostro territorio.
Verificato:
7 novembre 2026, 07:11
(dato dell'ultima pubblicazione del sito)
· Fonte:
Centro Funzionale Lazio
Numeri essenziali
112
Numero Unico Emergenze —
chiama
803 555
Sala Op. PC Lazio (segnalazioni non urgenti) —
chiama
06 9362600
Gruppo PC Genzano (info, non emergenze) —
chiama
Cosa fare ora
Mantieni la calma.
Pensa con lucidità prima di agire.
Chiama il 112
se c'è un pericolo per te o per altri.
Non intralciare i soccorsi.
Non recarti sui luoghi dell'emergenza per curiosità.
Segui solo fonti ufficiali
(questo sito, Comune, Regione, DPC).
Aiuta chi è in difficoltà
se puoi farlo in sicurezza (anziani, bambini, disabili).
Tieni il telefono carico
e usalo solo per comunicazioni necessarie.
Trova l'area di attesa più vicina
Il telefono ti chiede il permesso di usare la posizione. La distanza si calcola sul tuo dispositivo: la posizione non viene inviata a nessuno.
🔦 Modalità Lanterna
(torcia, bussola, schermo sempre acceso)
Cosa fare adesso (per tipo di emergenza)
Tutti i numeri utili
Sistema di allertamento meteo
Crea/consulta il tuo Piano Familiare
Aree di attesa di Genzano
Facile da leggere (testo semplificato)
Kit calamità bambini
(schede stampabili)
Kit calamità anziani
(schede stampabili)
Kit calamità RSA
(schede operative)
Sito completo
Gruppo Comunale Volontari Protezione Civile — Genzano di Roma
Versione lite per banda debole o emergenze.
```

### `/cosa-fare-adesso/` — Cosa fare adesso — Protezione Civile Genzano di Roma

- Descrizione: Azioni immediate in caso di emergenza a Genzano di Roma: chi chiamare, cosa fare e quali informazioni consultare.
- Titoli: H1 Cosa fare adesso · H2 Chiama subito · H2 Cosa sta succedendo? · H2 Regole generali valide sempre · H2 Risorse utili · H2 Vedi anche · H2 Strumenti di Prevenzione · H2 Materiali pronti su questo tema · H3 Video: i colori dell'allerta meteo · H3 Video: allerta meteo, cosa fare colore per colore · H3 Video orizzontale: i colori dell'allerta meteo · H3 Video orizzontale: allerta meteo, cosa fare colore per colore · H3 Video in 3D: come nasce un'allerta meteo · H3 Infografica: Allerta meteo · H3 Presentazione: Allerta meteo · H3 Presentazione (PDF): Allerta meteo · H2 QR code dell'articolo

```text
Cosa fare adesso
In questa pagina
Pagina rivista il
6 maggio 2026
.
Chiama subito
112
Numero Unico Europeo per le emergenze: chiamalo se c'è un pericolo immediato per persone, edifici, viabilità o ambiente.
803 555
Sala Operativa Regionale Protezione Civile Lazio, per segnalazioni secondo le indicazioni regionali.
Cosa sta succedendo?
Scegli la situazione più vicina a quella che stai vivendo. Troverai indicazioni pratiche e comportamenti da evitare.
Terremoto
Scossa sismica avvertita
Alluvione o allagamento
Acqua alta, frana, smottamento
Incendio
Incendio boschivo o urbano visibile
Vento forte
Raffiche violente, caduta rami
Temporale violento
Fulmini, grandine, piogge intense
Blackout
Manca la corrente elettrica
Regole generali valide sempre
Mantieni la calma.
Osserva la situazione e agisci in sicurezza.
Chiama il 112
se c’è un pericolo immediato o qualcuno è ferito.
Non intralciare i soccorsi.
Non andare sul luogo dell’emergenza per curiosità.
Segui solo fonti ufficiali.
Non diffondere informazioni non verificate.
Aiuta chi è in difficoltà
solo se puoi farlo senza metterti in pericolo.
Tieni il telefono carico
e usalo solo per comunicazioni necessarie.
Cosa NON fare in qualunque emergenza
Non chiamare il 112 per curiosità o per chiedere informazioni
: tieni la linea libera per chi sta davvero male.
Non recarti sui luoghi dell’evento
per vedere cosa è successo: rallenti i soccorsi e ti metti in pericolo.
Non condividere notizie non verificate
sui social: rilancia solo fonti ufficiali (Protezione Civile, Comune, Centro Funzionale Lazio).
Non bloccare le strade di accesso
ai mezzi di soccorso con la tua auto.
Non rientrare in un edificio danneggiato
prima del nullaosta dei Vigili del Fuoco.
Risorse utili
Consulta lo stato dell’allerta meteo
Trova le aree di emergenza del Piano Comunale
Apri la cartografia operativa
Leggi come contattare il Gruppo
Prepara il kit di emergenza
Vedi anche
Schede “1 minuto per proteggerti”
— sei azioni concrete in un minuto, stampabili e condivisibili
Numeri utili
— chi chiamare in caso di emergenza
Rischi e prevenzione
— comportamenti per ogni tipo di rischio
Dopo l’emergenza
— cosa fare quando l’evento è passato
Allerte meteo
— stato di allerta in corso
Piano familiare
— preparare il piano di emergenza in famiglia
Strumenti di Prevenzione
Panoramica Rischi
Piano di Emergenza
Piano Familiare
Allertamento Meteo
Cartografia Operativa
Kit di Emergenza
Materiali pronti su questo tema
Video da guardare, infografiche da condividere, presentazioni
per docenti. Liberamente scaricabili: la licenza è indicata su
ogni materiale.
Video MP4
Video: i colori dell'allerta meteo
Video verticale con voce e sottotitoli (45 secondi) che spiega verde, gialla, arancione e rossa. Pronto da condividere su WhatsApp e social.
3.0 MB
Licenza CC BY-NC-SA 4.0
(scarica il file)
Video MP4
Video: allerta meteo, cosa fare colore per colore
Video verticale con voce e sottotitoli (59 secondi) con le azioni da fare per ogni colore dell'allerta, dal verde al rosso.
4.1 MB
Licenza CC BY-NC-SA 4.0
(scarica il file)
Video MP4
Video orizzontale: i colori dell'allerta meteo
[… testo tagliato: la pagina continua per circa 1361 caratteri]
```

### `/allerte-meteo/` — Allerte meteo — Protezione Civile Genzano di Roma

- Descrizione: Consulta le allerte meteo per Genzano di Roma e capisci il significato dei codici colore.
- Titoli: H1 Allerte meteo · H2 Stato attuale dell’allerta · H2 Stato attuale: NESSUNA ALLERTA · H2 Ricevi le allerte su Telegram · H2 Che cosa fare, colore per colore · H3 I colori dell’allerta in due video · H3 VERDE — Nessuna allerta · H3 GIALLA — Criticità ordinaria · H3 ARANCIONE — Criticità moderata · H3 ROSSA — Criticità elevata · H2 Previsione meteo di oggi · H2 Cartina animata del Lazio e carta sinottica dell'Italia · H3 Animazione del Lazio — prossime 72 ore · H3 Carta sinottica dell'Italia · H2 Mappa meteo interattiva · H3 Mappa meteo interattiva Windy centrata su Genzano di Roma · H2 Radar pioggia in tempo reale (Protezione Civile) · H2 Previsione meteo per Genzano di Roma · H2 Come funziona il sistema di allertamento · H3 Come nasce un’allerta, in un video · H3 Previsione meteo e allerta non sono la stessa cosa · H2 Tipi di rischio monitorati · H2 Domande frequenti · H2 Approfondimenti dall’archivio · H2 Fonti ufficiali · H2 Vedi anche · H2 Mettiti alla prova nel libro · H2 Strumenti di Prevenzione · H2 Materiali pronti su questo tema · H3 Video: i colori dell'allerta meteo · H3 Video: allerta meteo, cosa fare colore per colore · H3 Video orizzontale: i colori dell'allerta meteo · H3 Video orizzontale: allerta meteo, cosa fare colore per colore · H3 Video in 3D: come nasce un'allerta meteo · H3 Infografica: Allerta meteo · H3 Presentazione: Allerta meteo · H3 Presentazione (PDF): Allerta meteo · H2 QR code dell'articolo

```text
Allerte meteo
In questa pagina
Pagina rivista il
14 ottobre 2026
.
Le allerte meteo indicano i possibili effetti al suolo di pioggia, temporali, vento e altri fenomeni. Servono a prepararsi prima che la situazione diventi pericolosa.
Stato attuale dell’allerta
Lo stato sotto è letto direttamente dai
bollettini ufficiali del Centro Funzionale Regionale del Lazio
per il Comune di Genzano di Roma. È lo stesso valore mostrato nella barra in cima alla
homepage
e aggiornato automaticamente quando cambia il livello.
Stato attuale: NESSUNA ALLERTA
Codice verde · Comune di Genzano di Roma
Non sono previsti fenomeni significativi sul nostro territorio.
L'ultima verifica automatica della fonte risale
al 07/11 alle 07:11
: lo stato mostrato potrebbe non rispecchiare il bollettino in vigore.
Controlla la situazione attuale sul
bollettino della Regione Lazio
(si apre in una nuova finestra)
.
Fonte ufficiale
Verificato:
7 novembre 2026, 07:11
· Fonte:
Centro Funzionale Regionale Lazio
(si apre in una nuova finestra)
Il livello riguarda la criticità idrogeologica, idraulica e per temporali. Gli avvisi per vento, neve, caldo, gelo e mareggiate e il rischio di incendi boschivi compaiono nelle barre in cima alla homepage.
Bollettino ufficiale Regione Lazio
(si apre in una nuova finestra)
Spiegazione a parole di «Allerta»
Il livello di allerta di oggi per Genzano di Roma, letto dai bollettini ufficiali di criticità idrogeologica, idraulica e per temporali.
Che cosa mostra
Il riquadro dice il livello di oggi, la descrizione dei fenomeni previsti e, se c’è, l’allerta di domani. Il livello è il più alto previsto per Genzano fra rischio idrogeologico, idraulico e per temporali, nella zona di allerta F, Bacini Costieri Sud. Sotto ci sono l’ora della verifica e il pulsante per aprire il bollettino ufficiale.
Colori e simboli
Verde: nessuna allerta. Non sono previsti fenomeni significativi, ma un temporale locale e improvviso resta possibile.
Giallo: allerta gialla, criticità ordinaria.
Arancione: allerta arancione, criticità moderata.
Rosso: allerta rossa, criticità elevata.
Il livello è sempre scritto anche a parole. L’icona è uno scudo con la spunta per il verde, un triangolo di pericolo per il giallo e per l’arancione, un ottagono per il rosso.
Ogni quanto si aggiorna
Un controllo automatico legge i bollettini più volte all’ora e, se il livello cambia, aggiorna subito il sito. L’ora accanto a «Verificato» è quella dell’ultima verifica registrata: il sito la riscrive circa ogni 6 ore, oppure subito se il livello cambia. Se ha più di 12 ore, il riquadro avverte che il dato potrebbe non essere quello in vigore.
Che cosa non dice
Riguarda solo la criticità idrogeologica, idraulica e per temporali. Gli avvisi per vento, neve, caldo, gelo e mareggiate e il rischio di incendi boschivi compaiono nelle barre in cima alla homepage.
Non dice che cosa fare: le azioni per ogni livello sono nella pagina
Allerte meteo
.
Fa fede il bollettino ufficiale del Centro Funzionale Regionale del Lazio: in caso di dubbio, aprilo con il pulsante.
Fonte:
Centro Funzionale Regionale del Lazio e Dipartimento della Protezione Civile, bollettini di criticità.
[… testo tagliato: la pagina continua per circa 18491 caratteri]
```

### `/numeri-utili/` — Numeri utili — Protezione Civile Genzano di Roma

- Descrizione: Numeri di emergenza, recapiti istituzionali e contatti utili per Genzano di Roma.
- Titoli: H1 Numeri utili · H2 In emergenza chiama il 112 · H2 Numeri di emergenza e soccorso · H3 Numero Unico Europeo · H3 Sala Operativa Regionale Lazio · H2 116117 — cure mediche non urgenti · H2 Recapiti del Gruppo di Protezione Civile · H2 Comune di Genzano di Roma · H2 Polizia Locale di Genzano di Roma · H2 Carabinieri — Stazione di Genzano di Roma · H2 Polizia di Stato — Commissariato di Genzano di Roma · H2 ASL Roma 6 — distretto di Genzano di Roma · H2 App utili · H2 Prima di chiamare · H2 In caso di emergenza · H2 Vedi anche · H2 QR code dell'articolo

```text
Numeri utili
In questa pagina
Pagina rivista il
24 maggio 2026
.
In emergenza chiama il 112
112
Numero Unico Europeo per le emergenze
— chiamalo per emergenze sanitarie, incendi, incidenti, soccorso tecnico, sicurezza pubblica e situazioni di pericolo immediato.
Numeri di emergenza e soccorso
Nel Lazio il numero da chiamare in caso di emergenza è il
112
. La centrale smista la chiamata al servizio competente: soccorso sanitario, Vigili del Fuoco, Forze dell’Ordine o altro ente di soccorso.
112
Numero Unico Europeo
Per emergenza in corso, pericolo immediato, persone ferite, incendio, incidente, soccorso tecnico o sicurezza pubblica.
803 555
Sala Operativa Regionale Lazio
Numero verde regionale di Protezione Civile. Per pericolo immediato resta sempre prioritario il 112.
116117 — cure mediche non urgenti
Per i problemi di salute che
non sono un’emergenza
puoi chiamare il
116117
, il numero europeo gratuito per le cure mediche non urgenti. È attivo
24 ore su 24
, è
multilingue
ed è già attivo per chi chiama da
Roma e provincia
, quindi anche da Genzano. Per le
emergenze
resta prioritario il
112
.
Numero:
116117
— gratuito da fisso e cellulare
Per:
continuità assistenziale (ex guardia medica), consigli sanitari non urgenti, informazioni sui servizi sanitari regionali e guardia medica turistica
Attivo:
tutti i giorni, 24 ore su 24, con assistenza multilingue
Approfondimento:
116117, il numero europeo per le cure mediche non urgenti
Recapiti del Gruppo di Protezione Civile
Questi recapiti sono
per informazioni e richieste non urgenti
. In caso di emergenza, chiama sempre il
112
.
Sede:
Via Sicilia, 13-15 — 00045 Genzano di Roma (RM)
Telefono:
+39 06 9362600
Email:
segreteria@protezionecivilegenzano.it
Comune di Genzano di Roma
Per informazioni amministrative, ufficio anagrafe e servizi al cittadino. Per
emergenze chiama il 112
, non il centralino comunale.
Sede:
Via Italo Belardi 81 — 00045 Genzano di Roma (RM)
Centralino:
+39 06 937111
Sito istituzionale:
comune.genzanodiroma.roma.it
Polizia Locale di Genzano di Roma
La Polizia Locale si occupa di viabilità, ordinanze, controlli stradali e attività amministrative. Per
emergenze in atto chiama il 112
, non i numeri del comando.
Sede:
Via Roma 31/A — 00045 Genzano di Roma (RM)
Telefono:
+39 06 9364687
·
+39 06 9397994
Email:
munipol@comune.genzanodiroma.roma.it
PEC:
polizia_locale@comunegenzanodiromapec.it
Carabinieri — Stazione di Genzano di Roma
I Carabinieri presidiano il territorio per la sicurezza pubblica e l’ordine. Per
emergenze in atto chiama il 112
, non il numero della stazione.
Sede:
Via Carlo Alberto Dalla Chiesa 2 — 00045 Genzano di Roma (RM)
Telefono:
+39 06 9363639
PEC:
trm27835@pec.carabinieri.it
Polizia di Stato — Commissariato di Genzano di Roma
Il Commissariato si occupa di sicurezza pubblica, denunce e attività di polizia. Per
emergenze in atto chiama il 112
, non il numero del commissariato.
Sede:
Via Chatillon 2 — 00045 Genzano di Roma (RM)
Telefono:
+39 06 9395681
PEC:
dipps172.5600@pecps.poliziadistato.it
ASL Roma 6 — distretto di Genzano di Roma
Per informazioni sanitarie ordinarie, prenotazioni, certificazioni e ufficio relazioni con il pubblico (URP). Per
[… testo tagliato: la pagina continua per circa 1528 caratteri]
```

### `/rischi-prevenzione/` — Rischi e prevenzione — Protezione Civile Genzano di Roma

- Descrizione: Informazioni sui rischi del territorio di Genzano di Roma e sui comportamenti da adottare prima, durante e dopo un'emergenza.
- Titoli: H1 Rischi e prevenzione · H2 Cosa puoi fare stasera · H2 Effetti a cascata: un rischio ne innesca un altro · H2 Pagine di consultazione rapida · H2 I più cercati · H2 Principali rischi · H2 Kit di emergenza essenziale · H2 Approfondimenti dall’archivio · H2 Vedi anche · H2 La prevenzione salva la vita · H2 Rischio Sismico · H2 Rischio Idrogeologico · H2 Rischio Incendi Boschivi · H2 Vento Forte · H2 Temporali Intensi · H2 Ondate di Calore · H2 Blackout e Interruzione Servizi · H2 Kit di Emergenza · H2 Persone con Necessità Specifiche

```text
Rischi e prevenzione
Conoscere i rischi del territorio aiuta a proteggere te, la tua famiglia e chi interviene nei soccorsi. In questa sezione trovi indicazioni pratiche sui principali rischi di Genzano di Roma e sui comportamenti da adottare prima, durante e dopo un’emergenza.
In caso di pericolo immediato, persone ferite, incendio, incidente o rischio per edifici e viabilità, chiama subito il
112
.
Cosa puoi fare stasera
La preparazione non richiede tempo né soldi. Cinque azioni che puoi fare
oggi stesso
:
Salva in rubrica il
112
e il numero della Sala Operativa Regionale
803 555
, e scrivili anche su un foglio di carta (in un blackout il telefono potrebbe essere scarico).
Metti in un punto fisso una
torcia
e una
radio a pile
(o a manovella) con le batterie cariche.
Riempi qualche
bottiglia d’acqua
e controlla la scadenza dei farmaci che usi ogni giorno.
Parla con la tua famiglia di
dove ritrovarsi
se doveste uscire di casa, e spiega ai bambini come e quando chiamare il 112.
Apri il
Piano Familiare
e compila la scheda con i recapiti e i punti di ritrovo.
Effetti a cascata: un rischio ne innesca un altro
Un evento raramente arriva da solo. Un
temporale violento
può far cadere alberi e linee elettriche, causando un
blackout
; il blackout può fermare le
pompe dell’acqua
e i
dispositivi salvavita
a casa; una
frana
può interrompere una strada e isolare un quartiere. Preparati pensando alla catena, non al singolo evento: il
kit di emergenza
e una scorta minima di acqua, cibo e farmaci ti coprono in tutti questi scenari.
Effetti a cascata: un problema può aggravare altri servizi essenziali, ma non tutte le conseguenze avvengono sempre.
Apri l'illustrazione ingrandita
(si apre in una nuova scheda)
·
Versione verticale leggibile su smartphone
(si apre in una nuova scheda)
Pagine di consultazione rapida
Queste pagine aiutano a orientarsi in pochi minuti, anche senza conoscenze tecniche.
Rischi principali in parole semplici
Spiegazione accessibile per bambini, persone con bisogni cognitivi e parlanti italiano L2.
Scuole di Genzano di Roma e rischi locali
Riferimenti per famiglie e personale scolastico, da integrare con il piano di emergenza del singolo istituto.
Sicurezza sullo scuolabus
Cosa fare in emergenza durante il tragitto: regole per bambini, autista e genitori.
Kit di emergenza economico e progressivo
Come comporre il kit un pezzo alla volta, senza marchi né prodotti specifici.
Dopo l'emergenza
Rientro sicuro, verifica di gas, luce e acqua, animali e notizie false quando l'evento è passato.
Biblioteca delle idee sbagliate
I luoghi comuni sulle emergenze: perché sono sbagliati, la fonte e una domanda di verifica.
Calcolatore della scorta per 72 ore
Acqua, pasti e farmaci per tre giorni, con la lista della spesa da spuntare e stampare.
I più cercati
Le quattro schede più consultate per il nostro territorio. Parti da qui se non sai da dove cominciare.
Rischio sismico
Cosa fare prima, durante e dopo una scossa. Zona sismica 2B, Colli Albani.
Rischio idrogeologico
Piogge intense, allagamenti, frane e smottamenti: il rischio più probabile in zona.
Rischio incendio
Incendi boschivi e di interfaccia. Campagna AIB giugno-settembre, Zona 9.
[… testo tagliato: la pagina continua per circa 3719 caratteri]
```

### `/rischi-prevenzione/rischio-sismico/` — Rischio Sismico: Cosa Fare — Protezione Civile Genzano di Roma

- Descrizione: Cosa fare prima, durante e dopo una scossa di terremoto per la sicurezza della tua famiglia.
- Titoli: H1 Rischio Sismico: Cosa Fare · H2 Terremoti recenti in Italia · H3 Mappa interattiva dei terremoti recenti in Italia — INGV · H2 Perché è rilevante sul nostro territorio · H2 Il rischio sismico a Genzano in numeri · H2 Segnali e situazioni tipiche · H2 Cosa fare PRIMA del terremoto · H2 Cosa fare DURANTE la scossa · H3 Se hai difficoltà di movimento · H2 Cosa fare DOPO la scossa · H2 Fonti e approfondimenti · H2 Chi chiamare · H2 Mettiti alla prova nel libro · H2 Strumenti di Prevenzione · H2 Materiali pronti su questo tema · H3 Video in 3D: terremoto, una casa vista dall'interno · H3 Video in 3D: il terremoto dalla A alla Z · H3 Presentazione (PDF): Rischio sismico · H3 Presentazione: Rischio sismico · H3 Infografica: Rischio sismico · H2 Approfondimenti video · H2 QR code dell'articolo

```text
Rischio Sismico: Cosa Fare
In caso di emergenza:
112
—
803 555
Cosa fare adesso
In questa pagina
Leggi in italiano semplice
A2
Esiste una versione di questo articolo in
italiano semplificato
(livello A2 — Quadro Europeo CEFR), pensata per
parlanti italiano L2
,
persone con disabilità cognitive
,
anziani
e
chi legge in fretta
. Frasi corte, parole comuni, niente sigle non spiegate.
Modalità Aula
Pagina rivista il
29 ottobre 2026
.
Il terremoto non si può prevedere. L’unica difesa è prepararsi prima: sapere cosa fare, avere il kit pronto, conoscere le vie di fuga.
Sei in pericolo in questo momento?
Se c'è un pericolo immediato per le persone — incendio, crollo, allagamento, persona ferita —
chiama subito il
112
, il numero unico di emergenza. Questa pagina serve a prepararsi
prima
: non sostituisce la chiamata di soccorso.
Hai poca rete? Le informazioni essenziali sono nella
pagina Emergenza
, leggera e veloce.
Sequenza illustrata di autoprotezione in un locale interno. Evita finestre e mobili instabili; non precipitarti fuori durante la scossa.
Apri l'illustrazione ingrandita
(si apre in una nuova scheda)
·
Versione verticale leggibile su smartphone
(si apre in una nuova scheda)
Terremoti recenti in Italia
Mappa e lista degli eventi sismici recenti rilevati dall’
Istituto Nazionale di Geofisica e Vulcanologia (INGV)
— fonte scientifica ufficiale in Italia. La vista mostra tutti i terremoti localizzati sul territorio nazionale; usa il menu interno per filtrare per magnitudo, profondità e periodo.
Nota:
i dati sono forniti da INGV in tempo reale. Un evento sismico registrato non significa necessariamente "scossa avvertita dalla popolazione": molti eventi di bassa magnitudo sono rilevati solo dagli strumenti. In caso di scossa avvertita, segui le indicazioni nella sezione "Cosa fare durante il terremoto" più in basso.
Mappa interattiva dei terremoti recenti in Italia — INGV
Terremoti recenti in Italia
Per visualizzare la mappa e la lista dei terremoti recenti devi caricare i contenuti forniti da
INGV
(Istituto Nazionale di Geofisica e Vulcanologia).
Carica la mappa INGV
In alternativa apri
terremoti.ingv.it
.
Elenco terremoti recenti consultabile su terremoti.ingv.it (Istituto Nazionale di Geofisica e Vulcanologia)
Perché è rilevante sul nostro territorio
Il Comune di Genzano di Roma è classificato in
zona sismica 2B
: secondo il Dipartimento della Protezione Civile, in zona 2 forti terremoti sono possibili. L’area dei Colli Albani, di origine vulcanica, è soggetta a scosse sismiche, generalmente di bassa magnitudo ma talvolta avvertite dalla popolazione. Questo rende essenziale conoscere i comportamenti corretti.
ℹ️
Sismicità e vulcanismo dei Colli Albani
: il Vulcano Laziale è quiescente, non spento; la sismicità di bassa magnitudo che caratterizza il territorio è in parte di origine vulcano-tettonica. Per il contesto vulcanologico, le emissioni di CO₂ in spazi confinati e le indicazioni operative dedicate vedi la pagina
Rischio Vulcanico (Colli Albani)
.
🤟
In Lingua dei Segni
: cosa significa “magnitudo”? Il
Glossario in LIS sul rischio sismico
[… testo tagliato: la pagina continua per circa 23866 caratteri]
```

### `/rischi-prevenzione/rischio-idrogeologico/` — Rischio Idrogeologico — Protezione Civile Genzano di Roma

- Descrizione: Le norme di comportamento da adottare in caso di alluvioni, frane e temporali intensi sul territorio di Genzano di Roma.
- Titoli: H1 Rischio Idrogeologico · H2 Perché è rilevante sul nostro territorio · H2 Segnali e situazioni tipiche · H2 Cosa fare PRIMA — Prepararsi · H2 Cosa fare DURANTE l’evento · H2 Cosa fare DOPO l’evento · H2 Fonti e approfondimenti · H2 Chi chiamare · H2 Mettiti alla prova nel libro · H2 Strumenti di Prevenzione · H2 Materiali pronti su questo tema · H3 Video in 3D: pioggia forte e alluvioni · H3 Video: alluvione e forti piogge, come comportarsi · H3 Video orizzontale: alluvione e forti piogge, come comportarsi · H3 Presentazione (PDF): Rischio idrogeologico · H3 Presentazione: Rischio idrogeologico · H3 Infografica: Rischio idrogeologico · H2 Approfondimenti video · H2 QR code dell'articolo

```text
Rischio Idrogeologico
In caso di emergenza:
112
—
803 555
Cosa fare adesso
In questa pagina
Leggi in italiano semplice
A2
Esiste una versione di questo articolo in
italiano semplificato
(livello A2 — Quadro Europeo CEFR), pensata per
parlanti italiano L2
,
persone con disabilità cognitive
,
anziani
e
chi legge in fretta
. Frasi corte, parole comuni, niente sigle non spiegate.
Modalità Aula
Pagina rivista il
24 ottobre 2026
.
Il rischio idrogeologico riguarda alluvioni, allagamenti, frane e smottamenti. Piogge intense e persistenti possono innescarli anche in poche ore.
Sei in pericolo in questo momento?
Se c'è un pericolo immediato per le persone — incendio, crollo, allagamento, persona ferita —
chiama subito il
112
, il numero unico di emergenza. Questa pagina serve a prepararsi
prima
: non sostituisce la chiamata di soccorso.
Hai poca rete? Le informazioni essenziali sono nella
pagina Emergenza
, leggera e veloce.
Il tuo browser non supporta la riproduzione del video.
Scarica il video (MP4)
.
Cosa fare prima, durante e dopo un’alluvione, in circa due minuti. La versione orizzontale, per la proiezione a scuola, è nelle
Risorse pronte
. Video: Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma, sulle indicazioni della campagna «Io non rischio» del Dipartimento della Protezione Civile.
Trascrizione del video
Alluvione e forti piogge: come comportarsi.
In un’alluvione l’acqua può salire all’improvviso, anche di uno o due metri in pochi minuti.
I punti più pericolosi: in casa, cantine, seminterrati e piani terra. Fuori, sottopassi, argini, ponti e le zone più basse.
Prima: informati sul piano di protezione civile del tuo Comune e segui le allerte. Prepara il kit di emergenza, e non tenere oggetti di valore in cantina.
Con l’allerta, non dormire nei seminterrati. Se devi spostarti, scegli un percorso lontano dalle zone che si allagano.
Se l’acqua arriva, non scendere in cantina o in garage per salvare le tue cose: rischi la vita. Sali ai piani alti, senza ascensore.
Chiudi il gas e stacca la corrente, ma non toccare gli impianti con mani o piedi bagnati. Non bere l’acqua del rubinetto: potrebbe essere contaminata.
Se sei all’aperto, allontanati dall’acqua: per la velocità con cui scorre, anche pochi centimetri possono farti cadere. Raggiungi un punto più alto, lontano da pendii e scarpate che possono franare.
Non usare l’auto: pochi centimetri d’acqua possono farti perdere il controllo o spegnere il motore. Evita sottopassi, argini e ponti.
Aiuta gli anziani e le persone con disabilità del tuo palazzo. Usa poco il cellulare: le linee libere servono ai soccorsi.
Dopo, segui le indicazioni delle autorità prima di rientrare o spalare il fango. Stai lontano dalle strade allagate: possono nascondere buche e tombini aperti. Bevi l’acqua del rubinetto solo se il Comune non lo vieta.
Segui solo le fonti ufficiali. Genzano di Roma è nella zona di allerta F. In emergenza chiama il 112.
Perché è rilevante sul nostro territorio
Genzano di Roma sorge sul bordo di un antico cratere vulcanico del
Vulcano Laziale
: il paese affaccia sul
lago di Nemi
[… testo tagliato: la pagina continua per circa 13386 caratteri]
```

### `/piano-emergenza/` — Piano di emergenza comunale — Protezione Civile Genzano di Roma

- Descrizione: Che cos'è il Piano di Emergenza Comunale di Genzano di Roma, quali aree prevede e cosa deve sapere il cittadino.
- Titoli: H1 Piano di emergenza comunale · H2 A cosa serve il Piano? · H2 Come leggere il Piano · H2 Chi coordina l’emergenza · H2 Le aree di emergenza · H3 Aree di attesa della popolazione (AA) · H3 Aree di ricovero della popolazione (AR) · H3 Aree di ammassamento soccorritori (AS) · H3 Edifici strategici · H2 Cosa deve fare il cittadino · H3 Prima dell’emergenza · H3 Durante l’emergenza · H3 Dopo l’emergenza · H2 Documenti scaricabili · H2 Strumenti di Prevenzione · H2 Materiali pronti su questo tema · H3 Video: i colori dell'allerta meteo · H3 Video: allerta meteo, cosa fare colore per colore · H3 Video orizzontale: i colori dell'allerta meteo · H3 Video orizzontale: allerta meteo, cosa fare colore per colore · H3 Video in 3D: come nasce un'allerta meteo · H3 Infografica: Allerta meteo · H3 Presentazione: Allerta meteo · H3 Presentazione (PDF): Allerta meteo · H2 QR code dell'articolo

```text
Piano di emergenza comunale
In questa pagina
Pagina rivista il
6 maggio 2026
.
Il Piano di Emergenza Comunale stabilisce come organizzare i soccorsi in caso di calamità. Indica i rischi del territorio, le aree di emergenza, le procedure operative e i soggetti che coordinano gli interventi.
A cosa serve il Piano?
Il Piano serve prima di tutto a
proteggere la popolazione
. Definisce chi fa cosa, quali risorse usare e come coordinare i soccorsi. Individua anche le
aree di emergenza
, cioè i luoghi da usare per l’attesa, il ricovero temporaneo e il supporto ai soccorritori.
L’impianto del Piano segue il
D.Lgs. 1/2018
(Codice della Protezione Civile) e le
direttive del Dipartimento della Protezione Civile
. Il testo del Piano non cita norme ISO. Per spiegare come si scelgono i punti di raccolta e come si tiene conto delle persone con esigenze specifiche, in questa pagina usiamo come riferimento anche la norma internazionale
ISO 22315:2014
Mass evacuation — Guidelines for planning
: è una spiegazione della redazione, non un contenuto del Piano.
Come leggere il Piano
Il Piano di Emergenza è un documento tecnico. Per il cittadino, però, le informazioni principali sono poche:
i rischi del territorio
— quali eventi possono colpire Genzano;
le aree di emergenza
— dove andare in caso di evacuazione;
la catena di comando
— chi coordina i soccorsi;
le procedure di allertamento
— come viene informata la popolazione.
Non serve leggere subito tutto il documento. Inizia dalle aree di emergenza più vicine a casa tua e al tuo luogo di lavoro. Puoi consultarle nella pagina
Cartografia operativa
.
Chi coordina l’emergenza
In ambito comunale, la prima autorità di protezione civile è il
Sindaco
. Quando la situazione lo richiede, il Sindaco può attivare il
Centro Operativo Comunale (COC)
. Il COC coordina le funzioni operative sul territorio: assistenza alla popolazione, volontariato, viabilità, comunicazione, servizi essenziali, censimento danni e supporto tecnico.
A Genzano di Roma, quando attivato, il
COC ha sede primaria presso il Comando di Polizia Locale
. Salvo diverse esigenze motivate (sede non agibile, evento che coinvolga direttamente la sede primaria, scelta operativa del Sindaco), quello è l’indirizzo di riferimento per il coordinamento operativo.
Il
Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
opera dentro questa catena di coordinamento. I volontari non vengono attivati direttamente dai cittadini, ma dagli enti competenti, secondo le procedure previste dal Piano e dal sistema regionale di protezione civile.
Per emergenze che coinvolgono più Comuni può intervenire anche il
Centro Operativo Intercomunale (COI)
. Genzano di Roma fa parte del
14° COI della Provincia di Roma — Castelli Romani Sud
.
In caso di pericolo immediato chiama il
112
. Non cercare di attivare direttamente squadre o singoli volontari: il coordinamento dei soccorsi deve passare dai canali ufficiali.
Le aree di emergenza
Aree di attesa della popolazione (AA)
Sono i
primi punti di raccolta
[… testo tagliato: la pagina continua per circa 4696 caratteri]
```

### `/aree-attesa/` — Aree di attesa di Genzano di Roma — Protezione Civile Genzano di Roma

- Descrizione: Dove andare a Genzano di Roma in caso di evacuazione: 10 aree di attesa della popolazione individuate dal Piano Comunale di Protezione Civile.
- Titoli: H1 Aree di attesa di Genzano di Roma · H2 Le 10 aree di attesa di Genzano di Roma · H2 Cosa fare quando raggiungi l’area · H2 Come riconoscere le aree sul territorio · H2 Prepara il piano familiare · H2 Vedi anche · H2 QR code dell'articolo

```text
Aree di attesa di Genzano di Roma
Pagina rivista il
13 maggio 2026
.
In caso di
evacuazione
o
dopo un evento sismico
, devi raggiungere subito una
area di attesa
: un luogo sicuro all’aperto dove ti raduni con gli altri cittadini, vieni censito e ricevi le prime informazioni.
Questa pagina elenca le 10 aree di attesa del Comune di Genzano di Roma. Per la
mappa interattiva
e tutte le altre aree (ammassamento soccorritori, ricovero della popolazione) vai a
Cartografia
.
Individua adesso la tua area
, non quando l'emergenza è in corso. Memorizza il codice (es. AA1) e il percorso a piedi.
Trova l'area di attesa più vicina
Il telefono ti chiede il permesso di usare la posizione. La distanza si calcola sul tuo dispositivo: la posizione non viene inviata a nessuno.
Le 10 aree di attesa di Genzano di Roma
Codice
Denominazione
Indirizzo
AA1
Palazzo Sforza Cesarini
Piazza Tommaso Frasconi
AA2
Via Piave
Parcheggio Via Piave
AA3
Via Toscana
Parcheggio incrocio Via Toscana / Via Lazio
AA4
Via Enrico Mattei
Parcheggio Via Enrico Mattei
AA5
Via Napoli
Parcheggio incrocio Via Napoli / Via Emilia Romagna
AA6
Palazzetto dello Sport
Parcheggio Via G. di Vittorio
AA7
Carlo Alberto dalla Chiesa
Parcheggio Scuola C. A. dalla Chiesa, Via Appia Vecchia
AA8
Zona Industriale
Parcheggio Via del Lavoro
AA9
Colli di Cicerone
Parcheggio Via Colli di Cicerone
AA10
Landi
Piazzale Frazione Landi
Gli indirizzi sono quelli dei cartelli installati sul territorio e verificati dal Gruppo: in caso di differenza valgono questi. In alcuni punti il testo del
Piano di Emergenza Comunale
in PDF riporta indirizzi diversi o non aggiornati.
Cosa fare quando raggiungi l’area
Resta nell’area
, non andare via prima che ti dicano cosa fare.
Fatti censire
dai volontari della Protezione Civile o dal personale comunale presente.
Aiuta chi è in difficoltà
se puoi farlo in sicurezza (anziani, bambini, disabili).
Non intralciare
mezzi di soccorso in arrivo.
Segui solo fonti ufficiali
(Comune, Protezione Civile, 112). Non amplificare voci o messaggi non verificati.
Come riconoscere le aree sul territorio
Ogni area di attesa è identificata da un
cartello con codice AA
: lo trovi all’ingresso del parcheggio o del piazzale. I cartelli sono stati installati nei punti previsti dal Piano Comunale di Protezione Civile.
Le immagini di tutti i cartelli (AA1–AA10) sono nella pagina
Cartografia
.
Prepara il piano familiare
Avere una
area di attesa di riferimento
è uno dei punti del Piano Familiare di Emergenza. Compila il tuo nella pagina
Piano Familiare
: è interattivo, stampabile, e i dati non escono dal tuo dispositivo.
Vedi anche
Cartografia
— mappa interattiva, aree di ammassamento, aree di ricovero, segnaletica
Cosa fare adesso
— azioni per tipo di emergenza
Piano Familiare
— compila il tuo piano
Numeri Utili
— emergenza 112, Sala Operativa PC Lazio 803 555
Piano di Emergenza Comunale
— il documento ufficiale
```

### `/piano-familiare/` — Piano di emergenza familiare — Protezione Civile Genzano di Roma

- Descrizione: Crea e stampa un piano di emergenza per la tua famiglia. I dati restano sul tuo computer e non vengono inviati al sito.
- Titoli: H1 Piano di emergenza familiare · H2 Perché serve un piano familiare · H2 Prima di compilare · H2 Compila il tuo piano · H3 1. La mia famiglia · H3 2. I nostri punti di ritrovo · H3 3. Contatti e risorse · H3 4. Esigenze specifiche (opzionale) · H2 Piano di emergenza familiare · H2 Consigli per famiglie con bambini · H2 Consigli per famiglie con anziani · H2 Consigli per persone con disabilità o bisogni specifici · H2 Consigli per gli animali domestici · H2 Checklist finale · H2 Quando aggiornare il piano · H2 Calcolatore dello zaino delle 72 ore · H2 Promemoria di controllo delle scorte · H2 Vedi anche · H2 Strumenti di Prevenzione · H2 Materiali pronti su questo tema · H3 Video: il kit di emergenza · H3 Video orizzontale: il kit di emergenza · H3 Presentazione (PDF): Kit emergenza famiglia · H3 Presentazione: Kit emergenza famiglia · H3 Infografica: Kit emergenza famiglia · H2 QR code dell'articolo

```text
Piano di emergenza familiare
In questa pagina
Pagina rivista il
28 giugno 2026
.
Compila il modulo per creare un piano di emergenza da stampare e conservare in casa.
I dati restano sul tuo computer
: non vengono inviati al sito, non vengono salvati online e non vengono trasmessi al Gruppo.
Un piano familiare aiuta tutti a sapere cosa fare se non c’è tempo per decidere con calma. È utile soprattutto quando in famiglia ci sono bambini, anziani, persone con disabilità, terapie da seguire o animali domestici.
Come usare questo piano
Compila il piano insieme alla famiglia. Rileggilo almeno una volta l’anno e aggiornalo quando cambiano casa, scuola, lavoro, numeri di telefono, farmaci, ausili o composizione del nucleo familiare.
Non sai da dove partire?
Prima di compilare il piano, scopri
quanto sei già preparato
: il
quiz “Quanto sei preparato?”
ti fa qualche domanda e ti restituisce un punteggio con i consigli su cosa migliorare. È il modo più veloce per capire cosa ti manca, prima di mettere nero su bianco il tuo piano.
Perché serve un piano familiare
Durante un’emergenza potresti non essere con i tuoi familiari. Se avete già deciso dove trovarvi, chi chiamare e cosa portare, sarà più facile agire in sicurezza.
Un piano familiare risponde a cinque domande:
Dove ci troviamo?
I punti di ritrovo concordati.
Chi chiamiamo?
Un contatto fuori città o fuori zona.
Cosa portiamo?
Il kit di emergenza e gli oggetti essenziali.
Chi ha bisogno di aiuto?
Bambini, anziani, persone con disabilità, terapie e animali domestici.
Cosa facciamo prima di uscire?
Gas, acqua, quadro elettrico, documenti, farmaci e chiavi, solo se si può fare in sicurezza.
Prima di compilare
Tieni a portata di mano:
numeri di telefono aggiornati dei familiari;
contatto di una persona fuori città o fuori zona;
indirizzo dei punti di ritrovo scelti;
elenco dei farmaci abituali e dei contatti sanitari essenziali;
informazioni su ausili, dispositivi, allergie o bisogni specifici;
dati utili per animali domestici, veterinario e trasportino;
posizione del kit di emergenza, delle chiavi, del quadro elettrico e dei rubinetti principali.
Non inserire più dati personali o sanitari del necessario. Il piano stampato può contenere informazioni sensibili: conservalo in un luogo accessibile ai familiari ma protetto.
Compila il tuo piano
1. La mia famiglia
Cognome della famiglia
Indirizzo di casa
Adulti
Bambini / ragazzi
Anziani o persone fragili
Animali domestici
2. I nostri punti di ritrovo
Punto di ritrovo vicino casa
Consulta le
aree di attesa
più vicine
Punto di ritrovo lontano da casa
3. Contatti e risorse
Contatto di riferimento fuori città
Medico di famiglia (nome e telefono)
Dove si trova il kit di emergenza?
Dove sono rubinetti gas/acqua e quadro elettrico?
4. Esigenze specifiche (opzionale)
Farmaci indispensabili
Ausili o necessità particolari
Note aggiuntive
Crea il mio piano
Piano di emergenza familiare
Protezione Civile Genzano di Roma — Gruppo Comunale Volontari
Documento generato il
Numeri di emergenza
112
Numero Unico Europeo per le emergenze
803 555
Sala Operativa Protezione Civile Lazio — segnalazioni secondo le indicazioni regionali
[… testo tagliato: la pagina continua per circa 7262 caratteri]
```

### `/diventa-volontario/` — Diventa volontario — Protezione Civile Genzano di Roma

- Descrizione: Come entrare nel Gruppo Comunale di Protezione Civile di Genzano di Roma: requisiti, formazione, impegno richiesto e contatti.
- Titoli: H1 Diventa volontario · H2 In breve · H2 Scarica la locandina · H2 Aderiamo alla campagna della Regione Lazio · H2 Chi può aderire · H2 Cosa fa un volontario · H2 Formazione · H2 Impegno richiesto · H2 Una giornata tipo del volontario · H3 Sabato mattina ordinario · H3 Sera con allerta meteo arancione · H3 Emergenza fuori comune (sisma, alluvione) · H2 Cosa NON fa un volontario · H2 Ruoli possibili — non serve essere “atleti” · H2 Come iscriversi · H2 Modulistica per l’iscrizione · H2 Domande frequenti · H3 Quanto tempo devo dedicare? · H3 L’iscrizione costa qualcosa? · H3 Serve esperienza? · H3 Posso partecipare se lavoro? · H3 Posso lasciare il Gruppo? · H2 Documenti utili · H2 Approfondimenti dall’archivio · H2 Vuoi saperne di più? · H2 Materiali pronti su questo tema · H3 Video: il kit di emergenza · H3 Video orizzontale: il kit di emergenza · H3 Presentazione (PDF): Kit emergenza famiglia · H3 Presentazione: Kit emergenza famiglia · H3 Infografica: Kit emergenza famiglia · H2 QR code dell'articolo

```text
Diventa volontario
In questa pagina
Pagina rivista il
25 giugno 2026
.
Diventare volontario di Protezione Civile significa mettere tempo, competenze e disponibilità al servizio della comunità. Non servono esperienze precedenti: il Gruppo ti affianca e ti forma prima dell’impiego operativo.
In breve
l'iscrizione è gratuita;
la formazione di base è obbligatoria;
l'impegno ordinario è di circa 16 ore al mese;
le attività si svolgono sotto coordinamento delle autorità competenti;
la piena operatività sul campo è prevista dal compimento dei 18 anni.
Scarica la locandina
Puoi stampare la locandina di reclutamento e condividerla in luoghi aperti al pubblico, nel rispetto delle autorizzazioni necessarie.
Scarica la locandina in PDF
Aderiamo alla campagna della Regione Lazio
Il Gruppo partecipa alla campagna regionale
«Non c'è Protezione Civile senza di te»
, che invita i cittadini — soprattutto i più giovani — a entrare nel volontariato di Protezione Civile. Nel
video più recente della campagna
il protagonista è un volontario del nostro Gruppo, intervistato durante un intervento antincendio boschivo.
Guarda tutti i materiali della campagna
Leggi l'articolo
Chi può aderire
Può chiedere di aderire chi possiede i requisiti previsti dal regolamento del Gruppo e dalla normativa vigente:
aver compiuto 16 anni;
essere cittadino italiano, cittadino dell’Unione Europea o cittadino extra UE con regolare permesso di soggiorno;
godere dei diritti civili e politici;
non aver riportato condanne penali ostative;
avere idoneità fisica alle attività previste, certificata dal medico.
I minorenni possono partecipare alla formazione e alle attività consentite. La piena operatività sul campo è prevista al compimento dei 18 anni.
Cosa fa un volontario
Le attività non riguardano solo le emergenze. Gran parte del lavoro è preparazione, prevenzione, formazione e supporto al territorio.
Un volontario può essere coinvolto in:
presidi durante allerte meteo e criticità locali;
attività antincendio boschivo, dopo specifica formazione;
supporto logistico e assistenza alla popolazione;
gestione delle comunicazioni radio;
esercitazioni e addestramenti;
incontri informativi con cittadini e scuole;
manutenzione ordinaria di mezzi, attrezzature e materiali;
supporto ad altre comunità in caso di emergenze sovracomunali.
Ogni attività viene svolta secondo le procedure del sistema di protezione civile e sotto il coordinamento delle autorità competenti.
Formazione
Prima dell’impiego operativo è previsto un percorso di formazione. Il corso di accesso affronta, in modo progressivo:
Il corso di accesso, passo dopo passo
struttura del Sistema nazionale di protezione civile;
rischi del territorio;
sicurezza personale e uso dei dispositivi di protezione;
procedure operative del Gruppo;
comunicazioni radio di base;
primo soccorso e autoprotezione;
comportamento corretto in scenario.
Dopo il corso base è possibile approfondire settori specifici, come antincendio boschivo, logistica, radiocomunicazioni, supporto alla popolazione, comunicazione, divulgazione e altre attività coerenti con le necessità del Gruppo.
Impegno richiesto
L’impegno ordinario è di circa
16 ore al mese
[… testo tagliato: la pagina continua per circa 8086 caratteri]
```

### `/chi-siamo/` — Chi siamo — Protezione Civile Genzano di Roma

- Descrizione: Storia, riferimenti istituzionali, direttivo, mezzi e attività del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma.
- Titoli: H1 Chi siamo · H2 Il Gruppo Comunale Volontari di Protezione Civile · H2 Riferimenti istituzionali · H3 Comune di Genzano di Roma · H3 Gruppo volontari · H2 Affiliazioni e riconoscimenti · H3 Quality Label — European Solidarity Corps · H3 Servizio Nazionale di Protezione Civile · H3 Coordinamento FE.PI.VOL. · H2 Accreditamenti · H3 WikiProcessi — Fondazione CIMA · H2 La nostra storia · H2 Il Consiglio direttivo · H2 Mezzi e attrezzature principali · H3 Land Rover Defender 130 · H3 EVO Cross 4 Pickup · H3 Nissan Cabstar · H3 Mercedes Actros · H3 Mercedes Atego · H3 Iveco VM90 · H3 Tenda sociale · H3 Vasca mobile · H3 Idrovora carrellata · H3 Fiat Doblò · H3 Iveco Stralis · H3 Iveco Cacciamali · H3 Astra BM201 · H2 Settori operativi · H3 Telecomunicazioni · H3 Web, social e divulgazione · H3 Divulgazione nelle scuole · H3 Droni · H3 Antincendio boschivo (AIB) · H3 Rischio idraulico e allagamenti · H2 Eventi e calamità significative · H2 Vedi anche · H2 QR code dell'articolo

```text
Chi siamo
In questa pagina
Pagina rivista il
15 ottobre 2026
.
Il Gruppo Comunale Volontari di Protezione Civile
Il Gruppo Comunale è stato istituito nel 1991 dal Consiglio Comunale e raccoglie l'esperienza dei volontari attivi a Genzano di Roma dal 1981. Svolge attività di prevenzione, supporto operativo, assistenza alla popolazione e informazione sui rischi, sempre nel quadro del sistema istituzionale di protezione civile.
🌍
Come lavoriamo:
scopri il nostro
modello di comunicazione accessibile a tutti
— un approccio documentato e replicabile, che condividiamo pubblicamente con chi si occupa di protezione civile.
Riferimenti istituzionali
Comune di Genzano di Roma
Sindaco:
Fabio Papalia
Assessore con delega alla Protezione Civile:
Massimo Bevilacqua (Vicesindaco)
Comandante Polizia Locale e Dirigente Protezione Civile:
Monica Palladinelli
Gruppo volontari
Il Gruppo Comunale Volontari è un'articolazione del Comune di Genzano di Roma, iscritta al RUNTS come Ente del Terzo Settore (sezione «Altri Enti del Terzo Settore»), con Statuto e Regolamento propri.
Opera in coordinamento con il Sindaco, autorità locale di protezione civile, con il Comando di Polizia Locale, con la Sala Operativa Regionale Lazio e con il coordinamento FEPIVOL.
Nomi e incarichi verificati direttamente dal Gruppo il
15 ottobre 2026
(in quanto articolazione del Comune, il Gruppo conosce di prima mano i propri referenti istituzionali). Prossima verifica prevista:
gennaio 2027
. Se noti un'informazione non aggiornata,
segnalacela
.
Affiliazioni e riconoscimenti
Il Gruppo aderisce a sistemi europei, nazionali e regionali di volontariato e protezione civile, sottoposti a verifica e accreditamento. Sono visibili nel footer di ogni pagina del sito.
Quality Label — European Solidarity Corps
Il Gruppo è organizzazione accreditata dal
Corpo europeo di solidarietà
(European Solidarity Corps, ESC) della Commissione europea. Il Quality Label certifica che l'organizzazione rispetta i principi e i requisiti di qualità del programma per ospitare attività di volontariato europeo.
Codice di accreditamento:
E10435833
Riferimento normativo:
Regolamento (UE) 2021/888 del 20 maggio 2021.
Servizio Nazionale di Protezione Civile
Il Gruppo è un gruppo comunale di volontariato di protezione civile ai sensi del
D.Lgs. 2 gennaio 2018, n. 1
(Codice della Protezione Civile), articolazione del Comune di Genzano di Roma, iscritto al Registro Regionale del Volontariato di Protezione Civile della Regione Lazio.
Coordinata dal
Dipartimento della Protezione Civile
(Presidenza del Consiglio dei Ministri) attraverso l'Agenzia regionale e il Sindaco quale autorità locale di protezione civile.
Coordinamento FE.PI.VOL.
Il Gruppo aderisce al
Coordinamento FE.PI.VOL.
— Federazione Pronto Intervento Volontariato ODV, rete delle organizzazioni di volontariato di protezione civile del Lazio.
FEPIVOL coordina interventi sovracomunali, formazione condivisa, esercitazioni congiunte e rappresentanza delle organizzazioni di volontariato presso le istituzioni regionali.
Accreditamenti
WikiProcessi — Fondazione CIMA
Ente accreditato alla piattaforma
WikiProcessi
di
Fondazione CIMA
,
[… testo tagliato: la pagina continua per circa 6084 caratteri]
```

### `/contatti/` — Contatti e sede — Protezione Civile Genzano di Roma

- Descrizione: Recapiti ordinari, sede e canali corretti da usare in emergenza o per richieste non urgenti.
- Titoli: H1 Contatti e sede · H2 In caso di emergenza · H2 Recapiti ordinari · H2 Canali ufficiali · H2 Quando contattarci · H3 Emergenza o pericolo immediato · H3 Comunicazioni regionali di Protezione Civile · H3 Informazioni sul Gruppo o volontariato · H3 Scuole, sito, media e collaborazioni · H2 Mappa della sede · H2 Vedi anche · H2 QR code dell'articolo

```text
Contatti e sede
In questa pagina
Pagina rivista il
24 ottobre 2026
.
In caso di emergenza
Il Gruppo Comunale di Protezione Civile
non può essere attivato direttamente dai cittadini
. Gli interventi vengono richiesti dalle autorità competenti, per garantire il coordinamento dei soccorsi.
112
Numero Unico Europeo per le emergenze
803 555
Sala Operativa Regionale Protezione Civile Lazio
Se c'è un pericolo immediato, chiama il 112. Le squadre del volontariato vengono attivate dagli enti competenti quando necessario.
Recapiti ordinari
Usa questi recapiti per
informazioni e richieste non urgenti
.
Sede:
Via Sicilia, 13-15 — 00045 Genzano di Roma (RM)
Telefono Segreteria:
+39 06 9362600
Email:
segreteria@protezionecivilegenzano.it
Giornalisti e redazioni:
contatti, comunicati e materiali nella
Sala stampa
Link utili:
Tutti i link web del Gruppo
Canali ufficiali
Segui i canali ufficiali per aggiornamenti, allerte e comunicazioni del Gruppo.
Facebook
Instagram
Telegram
X (Twitter)
Quando contattarci
Emergenza o pericolo immediato
Chiama il
112
per incendio, alluvione, terremoto, persona in pericolo, albero caduto su strada, smottamento, cavi pericolanti o altra situazione urgente.
Comunicazioni regionali di Protezione Civile
Fai riferimento alla Sala Operativa Regionale
803 555
, secondo le indicazioni ufficiali. Per pericolo immediato resta prioritario il 112.
Informazioni sul Gruppo o volontariato
Chiama la segreteria, vieni in sede o scrivi a
segreteria@protezionecivilegenzano.it
.
Scuole, sito, media e collaborazioni
Per progetti scolastici, segnalazioni sul sito, richieste media o collaborazioni scrivi a
segreteria@protezionecivilegenzano.it
. Per giornalisti e redazioni c'è la
sala stampa
.
Mappa della sede
Mappa:
© OpenStreetMap contributors
— Leaflet self-hosted.
Apri su OpenStreetMap
Sede:
Via Sicilia, 13-15 — 00045 Genzano di Roma (RM).
Vedi anche
Numeri utili
— chi chiamare in caso di emergenza
Cosa fare adesso
— azioni immediate per il cittadino
Diventa volontario
— iscrizione, requisiti e formazione
Sala stampa
— per giornalisti e redazioni: contatti, comunicati stampa, notizie, foto e logo
Mappa del sito
— tutte le sezioni del sito
```

### `/accessibilita/` — Dichiarazione di accessibilità — Protezione Civile Genzano di Roma

- Descrizione: Dichiarazione di accessibilità AGID: stato di conformità, contenuti non accessibili, modalità di valutazione, obiettivi annuali, feedback e contatti.
- Titoli: H1 Dichiarazione di accessibilità · H2 Stato di conformità · H2 Contenuti non accessibili · H3 Widget di terze parti · H3 Documenti PDF pubblicati sul sito · H3 Mappe interattive · H2 Redazione della dichiarazione · H2 Informazioni sul sito · H2 Modalità di valutazione · H3 Strumenti automatici · H3 Test manuali · H3 Test con tecnologie assistive · H3 Pagine campione testate · H2 Obiettivi di accessibilità (2026-2027) · H2 Criteri adottati · H2 Criteri AAA soddisfatti oltre l’obbligo · H2 Strumenti di accessibilità del sito · H2 Font utilizzati · H2 Lettura ad alta voce · H2 Versioni alternative degli articoli · H3 1. Audio — Leggi ad alta voce · H3 2. Braille — Scarica versione braille (BRF) · H3 3. PDF — Scarica trascrizione · H3 4. Italiano semplice — Versione facile da leggere (A2 CEFR) · H2 Versioni in altre lingue · H3 Otto versioni curate dal Gruppo · H3 Traduzione automatica del browser · H2 Supporto in emergenza · H3 Versione leggera /emergenza/ · H3 Modal “Chiama il 112” · H3 Assistente virtuale · H2 Glossario e supporti alla lettura · H2 Browser e lettura vocale · H2 Strumenti del dispositivo · H3 Zoom della pagina · H3 Lettori di schermo · H3 Contrasto e tema scuro · H2 Contenuti di terze parti · H3 Perché click-to-load è una scelta di accessibility-aware design · H3 Alternative testuali

```text
Dichiarazione di accessibilità
In questa pagina
Pagina rivista il
31 ottobre 2026
.
Questa pagina contiene la dichiarazione di accessibilità del sito della Protezione Civile di Genzano di Roma, redatta secondo il modello AGID e conforme alla
Direttiva (UE) 2016/2102
, alla
Legge 9 gennaio 2004 n. 4
(“Stanca”) e al
D.Lgs. 10 agosto 2018 n. 106
.
La dichiarazione si applica al sito
www.protezionecivilegenzano.it
.
Stato di conformità
Il sito è
parzialmente conforme
ai requisiti dello standard europeo armonizzato
EN 301 549 v3.2.1
(basato sulle
WCAG 2.1 livello AA
), con
tendenza esplicita alla piena conformità
. Il sito adotta inoltre come obiettivo ulteriore le
WCAG 2.2 livello AA
, che estendono le 2.1 con nuovi criteri: le 2.2 non sostituiscono la base normativa europea finché non saranno recepite in una versione armonizzata dello standard, ma sono già il riferimento dei nostri controlli interni.
Cosa risulta conforme nelle verifiche effettuate.
Ogni voce indica come e quando è stata verificata: i risultati valgono per le pagine e le date indicate, non come garanzia assoluta e permanente sull’intero sito.
Lighthouse Accessibilità: 100/100
— mediana su 9 run × 3 URL campione (home, archivio comunicazioni, numeri utili), verifica del 10 maggio 2026; il controllo automatico gira due volte al giorno (
lighthouse-audit.yml
) e segnala se il punteggio scende sotto 95: garantisce quindi che non ci siano regressioni, non che il punteggio sia ancora 100 nel momento in cui leggi.
Best Practices: 100/100
e
SEO: 100/100
— stesse condizioni di test.
Performance: 95/100
— mediana (LCP 2,3 s, TBT 70-130 ms, CLS 0,024-0,058), stesse condizioni di test.
Gate axe-core su ogni modifica
— dal luglio 2026 ogni proposta di modifica al sito passa un controllo automatico axe-core (WCAG 2.2 AA) su 11 pagine campione prima della pubblicazione: dal 15 agosto 2026 il gate è
bloccante
, cioè una violazione confermata impedisce la pubblicazione della modifica; da fine maggio 2026 a oggi non se n’è registrata nessuna. Restano segnalati controlli “da revisione manuale” (non violazioni accertate), esaminati progressivamente.
Contrasto colore WCAG AA
: nei test (automatici axe-core + calcoli manuali sui componenti del tema) non risultano testi sotto la soglia 4,5:1 sulle pagine campione; le regressioni note emerse in passato sono state corrette e sono documentate nel repository pubblico.
Navigazione da tastiera
: percorsi Tab/Shift+Tab/Enter/Esc verificati manualmente sulle pagine campione (elenco più sotto), senza trappole da tastiera riscontrate. Sulle mini-app interattive (giochi, quiz, schede stampabili) la navigazione completa richiede JavaScript attivo.
Focus visibile
: ogni elemento interattivo ha outline visibile (3px) al focus.
Skip link
: “Vai al contenuto principale” presente in cima alle pagine generate dal sito; sulle mini-app interattive è fornito via JavaScript insieme al resto dell’intestazione.
Landmark ARIA
: header/nav/main/footer presenti nativamente sulle pagine generate dal sito; sulle mini-app interattive (giochi, quiz, schede stampabili) sono iniettati via JavaScript e richiedono quindi JavaScript attivo.
Alt text
[… testo tagliato: la pagina continua per circa 29992 caratteri]
```

### `/formazione/` — Formazione e scuole — Protezione Civile Genzano di Roma

- Descrizione: Corsi per volontari, materiali per le scuole, giochi educativi e risorse sulla protezione civile per cittadini, docenti e famiglie.
- Titoli: H1 Formazione e scuole · H2 Da dove cominciare · H2 Sono un cittadino · H2 Sono un docente · H2 Voglio diventare volontario · H2 Cerco materiali accessibili · H2 Voglio imparare giocando · H2 Cerco corsi e manuali · H2 Formazione per i volontari · H2 Materiale didattico per le scuole · H3 Percorso guidato per scuole e famiglie · H3 Kit per fascia d’età · H2 Inclusione e bisogni specifici · H2 Storie, giochi e attività · H2 Aree tematiche · H2 Risorse educative online · H2 Approfondimenti dall’archivio · H2 Vedi anche · H2 QR code dell'articolo

```text
Formazione e scuole
In questa pagina
Pagina rivista il
6 maggio 2026
.
Pronto per la LIM.
Si usa col dito sulla lavagna interattiva della classe, anche a schermo intero, e funziona sui browser delle lavagne meno recenti.
Come usarlo in classe
La formazione aiuta volontari, cittadini e scuole a riconoscere i rischi e ad agire con più sicurezza. In questa pagina trovi i percorsi principali e i materiali più utili.
Da dove cominciare
Scegli il percorso più adatto al tuo bisogno.
Sono un cittadino
Leggi le azioni di autoprotezione per terremoto, alluvione, incendio, temporali, vento, caldo, blackout ed evacuazione.
Apri la guida per il cittadino
Sono un docente
Trova kit didattici, schede stampabili, percorsi pronti, attività inclusive e materiali per educazione civica.
Scegli i materiali per la scuola
Voglio diventare volontario
Scopri requisiti, corso base, impegno richiesto e modalità di adesione al Gruppo Comunale.
Leggi come diventare volontario
Cerco materiali accessibili
Consulta kit e schede per anziani, persone con disabilità, caregiver, bambini fragili e persone con difficoltà linguistiche.
Vai ai kit accessibili
Voglio imparare giocando
Apri giochi educativi gratuiti per infanzia, primaria, ragazzi e famiglie, senza registrazione.
Apri i giochi della sicurezza
Catalogo informativo
Cerco corsi e manuali
Consulta aree tematiche su primo soccorso, rischio incendio, radiocomunicazioni, manuale da campo e psicologia dell'emergenza.
Vai alle aree tematiche
Formazione per i volontari
Ogni nuovo volontario segue un corso base prima dell’impiego operativo. Il percorso introduce:
Sistema nazionale di protezione civile;
rischi del territorio di Genzano di Roma;
Piano di Emergenza Comunale e procedure operative;
sicurezza personale e uso delle dotazioni;
nozioni di primo soccorso;
comunicazioni radio in emergenza;
comportamento corretto in scenario.
I volontari già operativi partecipano ad aggiornamenti ed esercitazioni periodiche, tra cui:
esercitazioni pratiche sul territorio;
corsi specialistici, per esempio AIB, rischio idrogeologico e TLC;
addestramento su mezzi, attrezzature e procedure;
formazione dei divulgatori per gli incontri nelle scuole;
simulazioni coordinate con il sistema regionale;
incontri con altri enti del sistema di protezione civile.
Materiale didattico per le scuole
Le illustrazioni didattiche sono affiancate da
testo esplicativo
, descrizioni alternative e indicazioni stampabili. Un’immagine aiuta a comprendere un passaggio, ma non deve essere l’unico modo per ottenere un’informazione importante.
Il sito raccoglie materiali per docenti, studenti e famiglie. Sono disponibili kit per fasce d’età, schede stampabili, attività inclusive, giochi educativi, storie e percorsi pronti.
Percorso guidato per scuole e famiglie
Non sai da dove partire? Scegli la tua situazione: ogni scelta ti porta ai materiali già pronti.
Prima volta? Parti da qui
Scegli il tuo ruolo e arriva subito ai materiali giusti.
Programma dell'anno
Cinque incontri da ottobre a maggio per ogni età, con le lezioni già composte e il lavoro finale della classe.
Il Gruppo nella tua scuola
[… testo tagliato: la pagina continua per circa 5808 caratteri]
```

### `/facile-da-leggere/` — Facile da leggere — Protezione Civile Genzano di Roma

- Descrizione: Protezione civile in versione semplice: 112, terremoto, pioggia forte, incendio, temporale, vento, blackout, caldo e zaino di emergenza. Testi brevi e facili.
- Titoli: H1 Facile da leggere · H2 📞 Numero di emergenza · H2 🌍 Se trema la terra · H2 🌧️ Se piove molto forte · H2 🔥 Se vedi fumo · H2 ⛈️ Se c'è un temporale · H2 💨 Se c'è vento forte · H2 💡 Se manca la luce · H2 ☀️ Se fa molto caldo · H2 📱 Se ricevi un IT-alert · H2 🔎 Se non trovi una persona della famiglia · H2 🚪 Se devi lasciare la casa · H2 🐕 Se hai un animale con te · H2 🎒 Zaino di emergenza · H2 📍 Dove andare · H2 🆘 Chi ti aiuta · H2 📚 Vuoi saperne di più? · H2 ✉️ Vuoi scriverci? · H2 📄 Schede con i simboli da scaricare · H2 🎧 Vuoi ascoltare invece di leggere? · H2 Approfondimenti video · H2 QR code dell'articolo

```text
Facile da leggere
Pagina rivista il
6 maggio 2026
.
Questa pagina usa parole semplici e frasi corte. È pensata per tutti, anche per chi ha difficoltà a leggere o conosce poco l'italiano. Questa pagina è disponibile anche in
inglese
,
esperanto
,
rumeno
e
arabo
.
📞
Numero di emergenza
Per ogni emergenza chiama il
112
.
È
gratis
. Funziona anche senza credito.
📞 Chiama il 112
Quando rispondono, dì:
come ti chiami;
cosa è successo;
dove sei.
Parla piano. Non chiudere la chiamata.
🌍
Se trema la terra
Se senti tremare la terra:
vai sotto un tavolo;
metti le mani sulla testa;
aspetta fermo.
Non fare queste cose:
non scappare di corsa;
non usare l'ascensore;
non andare alla finestra.
Quando la scossa finisce, esci con calma se il luogo non è sicuro.
🌧️
Se piove molto forte
Se piove tanto e l'acqua sale:
resta in casa;
vai al piano alto;
stacca la luce con un adulto, solo se puoi farlo senza pericolo.
Non fare queste cose:
non andare in cantina;
non passare nei sottopassaggi;
non bere l'acqua del rubinetto se le autorità dicono che non è sicura.
🔥
Se vedi fumo
Se vedi molto fumo in casa:
avvisa subito un adulto;
esci di casa;
chiama il
112
.
Non fare queste cose:
non tornare indietro;
non prendere l'ascensore;
non aprire le finestre.
⛈️
Se c'è un temporale
Se ci sono fulmini e vento forte:
resta in casa;
chiudi le finestre;
aspetta che passi.
Non stare:
sotto un albero;
in piscina;
sul balcone.
💨
Se c'è vento forte
Se il vento soffia molto forte:
resta in casa;
chiudi finestre e porte;
stai lontano dalle finestre.
Non fare queste cose:
non stare sotto un albero;
non camminare vicino ai muri vecchi;
non andare sul balcone.
Le cose sui balconi possono cadere. Mettile dentro casa, se puoi farlo senza pericolo.
💡
Se manca la luce
Se in casa non c'è più la corrente:
resta calmo;
usa una torcia con le pile;
tieni chiuso il frigorifero;
aspetta che torni la luce.
Non fare queste cose:
non accendere candele: usa solo la torcia con le pile;
non prendere l'ascensore;
non usare barbecue o bracieri dentro casa.
Se usi una macchina che ti aiuta a respirare o a vivere, chiama subito il
112
.
☀️
Se fa molto caldo
In estate ci sono giorni con caldo molto forte:
bevi acqua spesso;
resta in casa nelle ore più calde;
chiudi le tapparelle quando c'è il sole;
mangia frutta e verdura.
Non fare queste cose:
non uscire al sole forte;
non bere alcolici;
non lasciare bambini o animali in macchina.
Se ti senti male, chiedi aiuto a un adulto. Se una persona perde i sensi, chiama il
112
.
📱
Se ricevi un IT-alert
IT-alert
è un messaggio che lo Stato manda sul tuo telefono quando c'è un pericolo grande.
il telefono fa un suono forte, diverso dal solito (se è in silenzioso, il suono può non partire);
appare un messaggio sullo schermo;
leggi tutto il messaggio con calma;
fai quello che dice il messaggio.
Non fare queste cose:
non spegnere il telefono;
non chiamare il 112 per dire che hai ricevuto il messaggio;
non avere paura: serve a proteggerti.
Il messaggio arriva a tutti i telefoni in una zona. Non sei tu da solo.
🔎
Se non trovi una persona della famiglia
In una emergenza la famiglia può separarsi. Niente panico.
[… testo tagliato: la pagina continua per circa 4126 caratteri]
```

### `/english/` — English — Civil Protection Genzano di Roma — PC Genzano di Roma

- Descrizione: Essential information in English for tourists and foreign residents: emergency numbers, what to do in the main risks, key contacts.
- Titoli: H1 English — Civil Protection Genzano di Roma · H2 Welcome · H2 📞 Emergency number · H2 🌍 Earthquake · H2 🌧️ Heavy rain & flooding · H2 🔥 Fire · H2 ⛈️ Thunderstorms · H2 📦 Emergency kit at home · H2 📱 IT-alert · H2 🗺️ Where to go in emergency · H2 📚 Detailed pages in English · H2 🌍 For practitioners and institutions · H2 📞 Contacts

```text
English — Civil Protection Genzano di Roma
This page summarizes essential Civil Protection information in English. For full details (in Italian), visit
the homepage
. If you need urgent help, call
112
.
Welcome
The
Civil Protection Volunteers Group of Genzano di Roma
is a public service of the Municipality. We help citizens before, during and after emergencies — earthquakes, floods, wildfires, severe weather. Our work is
voluntary and free of charge
.
This page gives you
essential information
in English. The full website is in Italian (use your browser’s translation feature for the rest).
📞 Emergency number
For
any emergency
in Italy, call:
📞 Call 112
112
is the European Single Emergency Number. It is:
Free
, even without credit on your SIM
Available
across the European Union
Connected to fire brigade, ambulance, police and Carabinieri
Working
without app or internet
When the operator answers, say:
What happened
(accident / fire / medical / crime)
Where you are
(street, number, town)
If anyone is hurt
Stay calm, speak slowly, do
not hang up
until the operator does.
🌍 Earthquake
Italy is a seismic country. Genzano is in
seismic zone 2B
, where strong earthquakes are possible. If you feel shaking:
Take cover under a sturdy table or against an interior wall
Cover your head with your hands
Stay where you are until the shaking stops
Do
not
run outside immediately
Do
not
use elevators
Stay away from windows and bookcases
After the shaking, exit calmly using the stairs and reach the closest
"Area di Attesa"
(waiting area). See the
map of waiting areas
.
🌧️ Heavy rain & flooding
The Castelli Romani area is exposed to intense rainfall (especially May-October). If a strong storm or flood is expected:
Stay indoors at upper floors
Avoid basements and underground parking
Do
not
drive through flooded underpasses
Do
not
approach rivers or torrents
Move valuables and electrical equipment to higher floors
Check the official weather alert at
Lazio Region
.
🔥 Fire
If you see smoke or flames:
Call
112
immediately
Leave the building using the stairs (never use elevators)
Close doors behind you (slows the fire spread)
Stay low if there is smoke (cleaner air near the floor)
Do
not
go back for belongings
For wildfires (June-September is high risk in Lazio), report immediately by calling 112.
⛈️ Thunderstorms
Sudden intense storms with lightning are common in summer. During a storm:
Stay indoors
Close windows and unplug appliances
Do
not
shelter under trees
Do
not
swim in pools or lakes
Avoid rivers and underpasses
📦 Emergency kit at home
Keep a small backpack ready with:
Water: 4 liters per person, per day, for 3 days (Ready.gov/FEMA)
Long-life food (biscuits, energy bars)
Flashlight with spare batteries
Thermal blanket and whistle
Phone charger
Important medications
Copy of ID documents
Cash (small amount)
📱 IT-alert
Italy has a national alert system called
IT-alert
. In case of major emergency it sends a message with a distinctive sound to mobile phones in the affected area — no app or internet needed, your phone just needs to be on and within mobile network coverage. The message is in Italian and English. More info:
it-alert.it
.
🗺️ Where to go in emergency
[… testo tagliato: la pagina continua per circa 1427 caratteri]
```

### `/assistente/` — Assistente — Cosa devo fare? — Protezione Civile Genzano di Roma

- Descrizione: Assistente guidato per sapere cosa fare in emergenza: terremoto, incendio, gas, allerta meteo, allagamento, volontariato, numeri utili, IT-alert.
- Titoli: H1 Assistente — Cosa devo fare? · H2 Avvertenze

```text
Assistente — Cosa devo fare?
Un assistente guidato per aiutarti a capire cosa fare in alcune situazioni frequenti e per orientarti tra le pagine del sito. Scegli il percorso più vicino alla tua situazione: ti guideremo con domande semplici fino alla risposta.
Emergenza in corso?
Chiama subito il
112
(Numero Unico Europeo di Emergenza). Questo assistente non sostituisce la chiamata al 112: fornisce solo indicazioni generali di autoprotezione basate sulle fonti ufficiali.
Cerca direttamente nel sito
Fai una domanda a voce
La domanda a voce usa il riconoscimento vocale del browser. Alcuni browser (Chrome, Edge) inviano l'audio ai server del produttore per trascriverlo: usa la voce solo se sei d'accordo. Tutto ciò che chiedi a voce puoi anche scriverlo o sceglierlo dai percorsi guidati.
Oppure scegli un percorso guidato qui sotto.
Avvertenze
Le indicazioni di questo assistente sono redatte dal Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma sulla base delle fonti ufficiali (Dipartimento Nazionale di Protezione Civile, Agenzia di Protezione Civile della Regione Lazio, Comune di Genzano di Roma). Sono indicazioni di carattere generale: in emergenza reale segui sempre le istruzioni delle autorità competenti e, se la situazione è grave, chiama il
112
.
Ogni risposta rimanda alle pagine istituzionali del sito per l'approfondimento.
```

### `/cruscotto/` — Cruscotto del territorio — Protezione Civile Genzano di Roma

- Descrizione: Cruscotto multidisciplinare in tempo reale: terremoti e vulcani (INGV), radar pioggia, satellite, meteo, allerta, incendi, aria e mare, in un'unica pagina.
- Titoli: H1 Cruscotto del territorio · H2 Cruscotto terremoti in Italia · H2 Monitoraggio del Distretto Vulcanico dei Colli Albani · H2 Radar pioggia in tempo reale (Protezione Civile) · H2 Radar pioggia ItaliaMeteo · H2 Immagini da satellite dell'Italia e dei dintorni di Genzano di Roma · H3 Sentinel-2: che cosa guardare nella scena · H3 Radar: cambiamenti rispetto al passaggio precedente · H3 Passaggi usati per il mosaico (ultime 48 ore su Genzano) · H3 Prossimo passaggio di giorno sopra Genzano · H3 Confronto prima e dopo · H3 Misure Sentinel-3: temperatura del suolo e fuochi · H3 Mappature d'emergenza Copernicus in Italia · H2 Satellite ItaliaMeteo (Meteosat · EUMETSAT) · H2 Previsioni ufficiali ItaliaMeteo · H2 Carte di previsione europee a medio termine — ECMWF OpenCharts · H2 Osservazioni in tempo reale ItaliaMeteo · H2 Stato attuale: NESSUNA ALLERTA · H2 Focolai rilevati da satellite negli ultimi 7 giorni · H2 Qualità dell'aria e pollini a Genzano di Roma · H3 Inquinanti · H3 Pollini (grani/m³ — valore indicativo) · H3 Previsione regionale (mappe ufficiali ARPA Lazio — modello FARM) · H2 Qualità dell'aria europea — Copernicus CAMS · H2 Attivazioni Copernicus EMS Rapid Mapping · H2 Stato del mare sulla costa laziale · H2 Previsioni del mare ItaliaMeteo (onde) · H2 La lettura ragionata dei dati · H2 Le fonti del cruscotto · H2 QR code dell'articolo

```text
Cruscotto del territorio
Un’unica pagina per consultare i dati di rischio del territorio, da
fonti ufficiali e aperte
. Scegli il tema con i pulsanti qui sotto. Sono dati
indicativi
: per le allerte valgono i bollettini del
Centro Funzionale Regionale del Lazio
, in emergenza chiama il
112
.
Sotto ogni scheda c’è la sua
spiegazione a parole
: che cosa mostra, come si leggono i colori e i simboli, ogni quanto si aggiorna e che cosa non dice. Le spiegazioni di tutte le schede, insieme a quelle dei grafici del Laboratorio meteo, sono raccolte anche in una pagina sola, da leggere o ascoltare:
Le mappe e i grafici spiegati a parole
.
Vuoi
esplorare i dati nel tempo
? Nel
Laboratorio meteo
costruisci grafici di temperatura, pioggia e vento dei Castelli Romani, con tabella dei dati e download.
Terremoti
Vulcani
Radar pioggia
Radar ItaliaMeteo
Satellite (EUMETSAT)
Satellite ItaliaMeteo
Meteo
Previsioni ItaliaMeteo
Meteo Europa (ECMWF)
Osservazioni ItaliaMeteo
Allerta
Incendi
Aria e pollini
Aria Europa (CAMS)
Emergenze EU (EMS)
Mare
Mare ItaliaMeteo
Cruscotto terremoti in Italia
24 ore
7 giorni
tutti
M≥2
M≥3
M≥4
Italia
Castelli Romani
—
Eventi nel periodo
—
Magnitudo massima
—
Eventi M≥3
—
Ultimo evento
—
· clicca un'intestazione per ordinare, una riga per aprire la scheda completa del terremoto.
Elenco dei terremoti rilevati nel periodo e nell'area selezionati, con data, magnitudo, zona, profondità, latitudine e longitudine. Ordinabile per ogni colonna.
Data e ora italiana
↓
Magnitudo
Zona
Profondità (km)
Distanza (km)
Lat
Lon
Colore dei cerchi, per magnitudo:
sotto 2
da 2 a 3
da 3 a 4
da 4 a 5
5 e oltre
· più grande il cerchio, più forte la scossa.
Fonte ufficiale
Dati:
INGV — Istituto Nazionale di Geofisica e Vulcanologia
(si apre in una nuova finestra)
(FDSN, open data). Aggiornamento automatico. In emergenza chiama il
112
.
Spiegazione a parole di «Terremoti»
La mappa e la tabella mostrano i terremoti registrati dall’INGV negli ultimi 7 giorni, o nelle ultime 24 ore, in Italia o nei Castelli Romani.
Che cosa mostra
Ogni cerchio è un terremoto, nel punto dell’epicentro. Con i pulsanti scegli il periodo, la magnitudo minima e la zona: tutta l’Italia oppure i Castelli Romani, un riquadro di circa 44 per 50 km attorno a Genzano. Il pulsante «tutti» vuol dire dalla magnitudo 1,5 in su. Sopra la mappa ci sono quattro numeri: quanti terremoti, la magnitudo più alta, quanti hanno magnitudo 3 o più e quanto tempo fa è avvenuto l’ultimo. Sotto, la tabella mostra 30 terremoti con ora italiana, magnitudo, zona, profondità e distanza da Genzano: all’inizio i più recenti. Toccando un’intestazione li riordini e le 30 righe cambiano: con «Magnitudo», per esempio, diventano le 30 scosse più forti. Toccando una riga si apre la scheda completa di quel terremoto.
Colori e simboli
Il colore del cerchio dice la magnitudo: grigio sotto 2, giallo da 2 a 3, arancione da 3 a 4, rosso da 4 a 5, rosso scuro da 5 in su.
Più il cerchio è grande, più la magnitudo è alta.
La stella blu è Genzano di Roma.
Ogni quanto si aggiorna
[… testo tagliato: la pagina continua per circa 58062 caratteri]
```

### `/privacy/` — Privacy e cookie policy — Protezione Civile Genzano di Roma

- Descrizione: Informativa sul trattamento dei dati personali e sull'uso dei cookie nel sito della Protezione Civile di Genzano di Roma.
- Titoli: H1 Privacy e cookie policy · H2 Titolare del trattamento · H2 Contatto privacy · H2 Dati trattati durante la navigazione · H2 Base giuridica · H2 Conservazione · H2 Diritti dell’interessato · H2 Cookie utilizzati dal sito · H2 Dati che restano solo nel tuo browser · H2 Statistiche di visita anonime · H2 Widget di terze parti (si caricano solo se li apri tu) · H2 Pagine che si collegano da sole alle fonti dei dati · H2 Trasferimento dati a terzi: piattaforma ActivePager · H2 Cartografia interattiva · H2 Laboratorio meteo · H2 Link esterni · H2 Come gestire i cookie nel browser · H2 Vedi anche · H2 QR code dell'articolo

```text
Privacy e cookie policy
In questa pagina
Pagina rivista il
31 ottobre 2026
.
Questa pagina spiega quali dati possono essere trattati durante la navigazione del sito e come sono gestiti cookie, widget esterni e strumenti interattivi.
Il sito non usa pubblicità, profilazione o sistemi di tracciamento commerciale.
Titolare del trattamento
Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma
Via Sicilia, 13-15 — 00045 Genzano di Roma (RM)
C.F. 92011880588
Email:
segreteria@protezionecivilegenzano.it
Contatto privacy
Il Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma è costituito dal Comune di Genzano di Roma ai sensi dell’art. 35 del D.Lgs. 1/2018 ed è iscritto al RUNTS nella sezione «Altri Enti del Terzo Settore». Per i trattamenti svolti nell’ambito dell’attività comunale di protezione civile, il Responsabile della protezione dei dati (RPD) di riferimento è quello designato dal Comune di Genzano di Roma, i cui recapiti sono pubblicati nell’
informativa privacy del Comune
. Il sito, essendo statico, non raccoglie né conserva sui propri server dati personali oltre a quelli tecnici descritti più avanti; l’unica eccezione riguarda l’accesso alla piattaforma riservata ai volontari (Activepager), descritto più sotto nella sezione dedicata.
Per informazioni sul trattamento dei dati personali, per esercitare i diritti previsti dal GDPR o per segnalare un problema relativo alla privacy puoi scrivere a
segreteria@protezionecivilegenzano.it
.
Dati trattati durante la navigazione
Il sito è prevalentemente statico. Non prevede registrazione utenti, login pubblico o profilazione.
Durante la navigazione possono essere trattati dati tecnici necessari al funzionamento del sito, come:
indirizzo IP;
tipo di browser;
sistema operativo;
pagine richieste;
data e ora della richiesta;
dati tecnici necessari alla sicurezza e alla manutenzione.
Questi dati sono usati per garantire il funzionamento del sito, la sicurezza tecnica e la risoluzione di eventuali problemi.
Base giuridica
Il trattamento dei dati tecnici di navigazione si basa sull’esecuzione di un compito di interesse pubblico (art. 6, par. 1, lett. e del Regolamento (UE) 2016/679): l’informazione alla popolazione sui rischi e sulle attività di protezione civile prevista dal D.Lgs. 1/2018. La conservazione dei dati tecnici per garantire la sicurezza della rete e dell’informazione risponde a quanto indicato dal considerando 49 del Regolamento.
Conservazione
I dati tecnici sono conservati per il tempo necessario alle finalità indicate e comunque non oltre 12 mesi, salvo esigenze di sicurezza, accertamento di illeciti o obblighi di legge.
Diritti dell’interessato
Puoi esercitare i diritti previsti dal GDPR, tra cui:
accesso ai dati personali;
rettifica;
cancellazione;
limitazione del trattamento;
opposizione al trattamento;
reclamo al
Garante per la protezione dei dati personali
.
Per esercitare i diritti puoi scrivere a
segreteria@protezionecivilegenzano.it
.
Cookie utilizzati dal sito
I cookie sono piccoli file di testo che il browser salva sul dispositivo durante la navigazione.
[… testo tagliato: la pagina continua per circa 7167 caratteri]
```

### `/lim/` — Protezione civile sulla LIM: giochi, schede e lezioni per la lavagna interattiva — PC Genzano di Roma

- Descrizione: Giochi, storie, schede, quiz e lezioni di protezione civile pronti per la LIM: si usano col dito, a schermo intero, anche sulle lavagne con browser non aggiornato.
- Titoli: H1 Protezione civile sulla LIM: giochi, schede e lezioni per la lavagna interattiva · H2 Che cosa vuol dire «Pronto per la LIM» · H2 Come si usa in classe · H2 Che cosa trovi · H2 Domande frequenti · H2 QR code dell'articolo

```text
Protezione civile sulla LIM: giochi, schede e lezioni per la lavagna interattiva
In questa pagina
I materiali del sito per le scuole sono pensati per essere usati
sulla lavagna interattiva multimediale (LIM)
della classe: giochi, storie, schede, quiz, il libro che si esplora, gli esperimenti e lo strumento che compone una lezione. Le pagine che lo sono portano il riquadro
«Pronto per la LIM»
.
Che cosa vuol dire «Pronto per la LIM»
Ogni settimana un controllo automatico apre tutte queste pagine come le apre una lavagna interattiva e verifica che:
si usino col solo tocco
, senza mouse né tastiera: dove un gioco si gioca trascinando, si può anche toccare l’oggetto e poi il posto giusto;
i pulsanti siano grandi
, almeno 44 pixel nei giochi, comodi da toccare per un bambino in piedi davanti alla lavagna;
la pagina stia nello schermo
del proiettore, a 1024×768 e 1366×768 pixel e con lo zoom al 150%, senza barre di scorrimento orizzontali;
funzionino anche sui browser delle lavagne meno recenti
: le pagine sono provate con un browser Chromium del 2018 (versione 69, quello delle lavagne con Android 9 e dei computer di classe non aggiornati) e con le versioni attuali di Chromium e di Firefox;
non ci siano errori
che fermano il gioco o la pagina.
Se un controllo non va a buon fine, il problema viene segnalato e corretto prima della pubblicazione successiva.
Come si usa in classe
Dalla lavagna, in cinque passi
Apri la pagina dal browser della LIM o del computer collegato. Non serve installare nulla né creare un account.
Nei giochi tocca
«Schermo intero»
, in alto a destra: spariscono le barre del browser e il gioco occupa tutta la lavagna. Per uscire tocca di nuovo il pulsante.
Per proiettare una pagina di testo (un rischio, una storia, una scheda del kit) usa
«Modalità Aula»
: la pagina diventa una sequenza di schermate con il testo grande, da scorrere con «Avanti» e «Indietro».
Se il testo è piccolo per chi sta in fondo all’aula, ingrandisci: nelle storie e nei libri pop-up tocca
«+»
nella barra in alto, nel libro che si esplora
«Pagina sinistra»
o
«Pagina destra»
, poi scorri col dito per spostarti;
«↺ Ripristina»
riporta tutto com’era. Sulle lavagne che lo permettono funziona anche il pizzico con due dita, e nelle altre pagine lo zoom del browser: restano nello schermo anche al 150%.
Nei giochi con «Ascolta» o «Leggi ad alta voce» il testo si sente dalle casse della LIM.
Che cosa trovi
Giochi della sicurezza
, divisi per infanzia, primaria e ragazzi, compreso
«Genzano si prepara»
, la simulazione sulla mappa vera di Genzano.
Crea la mia lezione
: scegli classe, tempo e argomento e il sito compone la lezione con i materiali pubblicati.
Il libro che si esplora
, con la
versione in italiano semplice
e le
schede da stampare
.
Storie e racconti
da leggere insieme o ascoltare.
Schede stampabili
, da proiettare o da stampare.
Esperimenti e attività
,
Laboratorio meteo
e
Quanto sei preparato?
.
Percorsi didattici pronti
e i kit per
infanzia
,
primaria
,
secondaria di primo grado
e
secondaria di secondo grado
.
Abili a proteggere
e le
tabelle di comunicazione
, per la classe inclusiva.
Domande frequenti
Con quali lavagne interattive funzionano?
[… testo tagliato: la pagina continua per circa 1051 caratteri]
```

### Ultimo articolo: `/comunicazioni/2026-11-07-piemonte-1994-alluvione-tanaro/` — Piemonte, 5-6 novembre 1994: l'alluvione del Tanaro che cambiò le regole — PC Genzano di Roma

- Descrizione: Alba, Asti, Alessandria, Ceva: nel novembre 1994 il Tanaro e il Po uscirono dagli argini. Da quella tragedia nacquero i piani di assetto idrogeologico.
- Titoli: H1 Piemonte, 5-6 novembre 1994: l'alluvione del Tanaro che cambiò le regole · H2 Il Tanaro esce dal suo letto · H2 Perché fu un punto di svolta · H2 Cosa insegna · H2 Per approfondire · H2 Approfondimenti video · H2 QR code dell'articolo · H2 Leggi anche Informazione · H3 Genova, 4 novembre 2011: l'alluvione del Fereggiano e la lezione dei rii tombati · H3 4 novembre 1966: l'alluvione di Firenze e la nascita degli Angeli del fango · H3 4 novembre: le Forze Armate e il loro ruolo nella Protezione Civile · H2 Resta aggiornato sulle allerte · H3 Iscriviti al canale Telegram

```text
Piemonte, 5-6 novembre 1994: l'alluvione del Tanaro che cambiò le regole
In questa pagina
Informazione
7 novembre 2026
Gruppo Comunale Volontari PC Genzano
Nei primi giorni di
novembre 1994
una perturbazione rimase ferma per giorni sul Piemonte. Le piogge, intense e continue tra il 4 e il 6 novembre, gonfiarono il
Tanaro
, la
Bormida
e infine il
Po
. Le città lungo i fiumi furono invase dall’acqua:
Alba
,
Asti
,
Alessandria
,
Ceva
e decine di centri minori. Le vittime furono 68 secondo il Dipartimento della Protezione Civile, gli evacuati circa 5.500, i danni ingenti.
Il Tanaro esce dal suo letto
Il Tanaro è un fiume di pianura alimentato dalle Alpi Marittime e dalle Langhe. Nel novembre 1994 la piena superò ogni livello conosciuto. Ad Alba l’acqua invase i quartieri bassi e le zone industriali; ad Asti raggiunse il centro. Ad Alessandria il Tanaro entrò in città nella notte tra il 5 e il 6 novembre, sorprendendo gli abitanti dei quartieri vicini al fiume. A Ceva, in alta valle, il fiume portò via strade e ponti.
Il Po, ricevendo tutta quell’acqua, andò in piena anche nel tratto vercellese. Il sistema di previsione e allerta di allora non era in grado di dire ai Comuni cosa sarebbe successo e quando.
Perché fu un punto di svolta
L’alluvione del 1994 fece capire che il rischio dei fiumi andava
conosciuto prima
, non subito dopo. Negli anni seguenti si consolidarono strumenti che oggi diamo per scontati: la
mappatura delle aree allagabili
con diversi tempi di ritorno, i
piani di assetto idrogeologico
dei bacini. Arrivarono anche i
vincoli
sulle costruzioni nelle fasce fluviali. La legge 267 del 1998, dopo la frana di Sarno, avrebbe completato quel percorso. Il sistema dei Centri Funzionali e dell’allertamento per colori sarebbe arrivato nel decennio successivo.
Il 1994 fu anche una grande prova per il
volontariato di protezione civile
: volontari da tutta Italia aiutarono le città piemontesi colpite.
Cosa insegna
Le alluvioni fluviali sono più lente delle colate di fango o dei torrenti coperti: danno ore, a volte giorni, di preavviso. Quel tempo va usato. Le regole del Dipartimento della Protezione Civile:
Conosci le aree allagabili
del tuo Comune e dove sono le zone sicure: sono nel piano di protezione civile.
Con un’allerta in corso
, non dormire nei piani seminterrati e tieni pronti documenti, farmaci, torcia e radio.
Se arriva l’acqua
, sali ai piani alti; non scendere in cantina per salvare i beni.
Non usare l’auto
per spostarti in zone allagate.
Dopo
, non transitare nelle strade coperte d’acqua e bevi l’acqua del rubinetto solo se ordinanze o avvisi del Comune non lo vietano.
Per approfondire
Sul nostro sito:
Rischio idrogeologico: cosa fare prima, durante e dopo
4 novembre 1966: l’alluvione di Firenze e la nascita degli Angeli del fango
Trent’anni dall’alluvione della Versilia: il 19 giugno 1996
Piano familiare di emergenza
Fonti istituzionali:
ISPRA — Dissesto idrogeologico in Italia
ARPA Piemonte — Eventi alluvionali
L’alluvione del Piemonte — Servizio nazionale della Protezione Civile
Dipartimento della Protezione Civile — Rischio meteo-idro: sei preparato?
Approfondimenti video
Selezione di video pertinenti dai canali istituzionali del Dipartimento di Protezione Civile e dal progetto Abili a Proteggere. I video sono ospitati sui canali ufficiali — il click apre YouTube in una nuova scheda.
Alluvione di Sarno del 5 maggio 1998, le cause della frana e la ricostruzione della tragedia
Geopop — divulgazione scientifica
↗
(video su YouTube, si apre in una nuova scheda)
La mappa delle frane in Italia: i territori più a rischio e i dati sul dissesto idrogeologico
Geopop — divulgazione scientifica
↗
(video su YouTube, si apre in una nuova scheda)
Rilocalizzazioni degli edifici residenziali dalle aree a rischio idrogeologico
CMCC — Centro Euro-Mediterraneo sui Cambiamenti Climatici
↗
(video su YouTube, si apre in una nuova scheda)
Io non rischio Alluvione – Cosa fare durante un’allerta, durante e dopo un’alluvione
Io non rischio
↗
(video su YouTube, si apre in una nuova scheda)
Io non rischio Alluvione – Cosa sapere e cosa fare fin da subito
Io non rischio
↗
(video su YouTube, si apre in una nuova scheda)
Selezione effettuata automaticamente in base alle parole chiave del contenuto, rivista periodicamente. I video sono di proprietà dei rispettivi enti — il Gruppo Comunale Volontari di Genzano cura la cernita e l'attribuzione tematica.
Resta aggiornato sulle allerte
Iscriviti al canale Telegram
Ricevi sul telefono una notifica automatica quando cambia il
livello di allerta meteo
per Genzano di Roma e — augurandoci di non doverle mai inviare — le
comunicazioni di emergenza
sul territorio.
Niente spam: solo cambiamenti significativi dello stato. L'iscrizione è anonima e puoi disiscriverti in qualsiasi momento dal canale stesso.
Iscriviti al canale
Ci trovi anche su:
Facebook
Instagram
X
Modalità di pubblicazione e tempi di risposta nella
Social Media Policy
.
Torna a tutte le comunicazioni
```

