# Parte 36 — Cruscotto del territorio (schede dati in tempo reale)

Il **Cruscotto del territorio** (`/cruscotto/`, alias `/dashboard/`) raccoglie in un'unica pagina i dati di rischio del territorio, presi da **fonti ufficiali e aperte**. È pensato per il cittadino e per gli enti: un colpo d'occhio su terremoti, meteo, radar, satellite, allerta, incendi, aria e mare, senza dover saltare fra dieci siti diversi.

> I dati del cruscotto sono **indicativi**. Per le allerte valgono sempre i bollettini del Centro Funzionale Regionale del Lazio; in emergenza si chiama il **112**. Questo avviso è scritto in cima alla pagina e non va rimosso.

## 36.1 Com'è fatto

La pagina (`content/cruscotto/_index.md`, `layout: "single"`) è un **commutatore a schede** (`role="tablist"`): in alto una fila di pulsanti `.cruscotto-tab`, sotto i pannelli `.cruscotto-panel` (uno visibile per volta, gli altri `hidden`). Ogni scheda è uno **shortcode** dedicato `{{< dashboard-… >}}` nel tema (`themes/flavour-pcgenzano/layouts/shortcodes/`).

Sotto l'introduzione c'è un **richiamo al Laboratorio meteo** (box `.cruscotto-callout`) per chi vuole costruire grafici dei dati nel tempo (vedi Parte 37).

## 36.2 Le schede e le loro fonti

| Scheda | Shortcode | Fonte dati (aperta) |
|---|---|---|
| Terremoti | `dashboard-terremoti` | INGV (FDSN) |
| Vulcani | `dashboard-vulcani` | INGV |
| Radar pioggia | `dashboard-radar` | Radar-DPC (Dipartimento Protezione Civile) |
| Radar ItaliaMeteo | `dashboard-radar-im` | ItaliaMeteo / MeteoHub (Mistral) |
| Satellite (EUMETSAT) | `dashboard-satellite` | EUMETSAT |
| Satellite ItaliaMeteo | `dashboard-satellite-im` | ItaliaMeteo |
| Meteo | `dashboard-meteo` | Open-Meteo (modelli ECMWF) |
| Previsioni ItaliaMeteo | `dashboard-previsioni-im` | ItaliaMeteo (ICON-2I) |
| **Meteo Europa (ECMWF)** | `dashboard-ecmwf` | ECMWF OpenCharts (carte auto-ospitate, vedi 36.3) |
| Osservazioni ItaliaMeteo | `dashboard-italiameteo-osservazioni` | ItaliaMeteo (stazioni) |
| Allerta | `dashboard-allerta` | `data/allerta.json` (Centro Funzionale Lazio) |
| Incendi | `dashboard-incendi` | EFFIS |
| Aria e pollini | `dashboard-aria` | Open-Meteo Air Quality + ARPA Lazio |
| Aria Europa (CAMS) | `dashboard-aria-cams` | Copernicus CAMS (ECMWF) |
| Emergenze EU (EMS) | `dashboard-ems` | Copernicus EMS Rapid Mapping |
| Mare | `dashboard-mare` | Open-Meteo Marine |
| Mare ItaliaMeteo | `dashboard-mare-im` | ItaliaMeteo (onde WW3) |

**Principio privacy-first:** dove possibile niente iframe/embed di terzi nel browser; le carte statiche (ECMWF, cartina Lazio) sono **auto-ospitate** dopo essere state scaricate da workflow. Le chiamate dirette ad API aperte (INGV, Open-Meteo, radar DPC, EUMETSAT, CAMS, EMS, ItaliaMeteo) sono già in whitelist `connect-src` del `.htaccess` — se aggiungi una fonte nuova, aggiungi anche il suo host alla CSP.

## 36.3 Scheda "Meteo Europa (ECMWF)" — carte auto-ospitate

La scheda mostra carte sinottiche europee a medio termine (pressione/vento, temperatura/vento, precipitazioni, CAPE/CIN) prese dall'**OpenCharts API pubblica di ECMWF** (CC BY 4.0, nessuna API key). Non sono embed: il workflow `ecmwf-charts.yml` (4×/giorno) le scarica, le converte in WebP e le salva in `static/images/ecmwf/<slug>.webp`, con i metadati in `data/ecmwf_charts.json`. Lo shortcode `dashboard-ecmwf` legge il JSON e mostra ogni carta con la **data di validità della previsione** e il passo orario (es. +72h) — così si capisce *per quando* vale la carta, non solo quando è stata prelevata.

## 36.4 Monitoraggio automatico delle fonti

Le fonti esterne possono cambiare URL o cadere, lasciando una scheda vuota **senza** errore visibile. Per questo il workflow `controllo-fonti-cruscotto.yml` (lunedì) lancia `scripts/check-fonti-cruscotto.py`: pinga le ~16 fonti e apre un'issue (label `automazione + cruscotto`) se almeno una è giù. Eseguibile in locale: `python3 scripts/check-fonti-cruscotto.py` (exit code = numero fonti in errore).

## 36.5 Aggiungere o modificare una scheda

1. Crea/aggiorna lo shortcode `themes/flavour-pcgenzano/layouts/shortcodes/dashboard-<nome>.html`.
2. Aggiungi il pulsante `.cruscotto-tab` e il pannello `.cruscotto-panel` in `content/cruscotto/_index.md` (rispetta `role="tab"`/`role="tabpanel"`, `aria-controls`, `aria-selected`, `tabindex`).
3. Se la scheda chiama un'API esterna dal browser, aggiungi l'host a `connect-src` nel `.htaccess`.
4. Aggiungi la fonte a `scripts/check-fonti-cruscotto.py` perché venga monitorata.
5. **Verifica visiva** (CLAUDE.md § "Verifica visiva pre-commit su markup HTML"): è markup custom, va guardato con Playwright prima del commit.

## 36.6 Cosa non fare

- Non trasformare il cruscotto in un bollettino ufficiale: resta **indicativo**, l'avviso 112/Centro Funzionale non si tocca.
- Non aggiungere embed con cookie di terze parti: rompe la promessa privacy-first e richiederebbe un banner di consenso.
- Non mettere l'indice di pagina/scrollspy qui: il cruscotto è una pagina-strumento, è già escluso dal gate dell'indice (Parte 38).
