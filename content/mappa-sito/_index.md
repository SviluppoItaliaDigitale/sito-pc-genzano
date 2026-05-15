---
title: "Mappa del Sito"
description: "Tutte le pagine del sito della Protezione Civile di Genzano di Roma organizzate per area tematica: servizi, rischi, allerte, formazione, strumenti, contatti."
layout: "single"
aliases:
  - /sitemap.html
  - /mappa/
sitemap:
  priority: 0.6
  changefreq: monthly
---

In questa pagina trovi **tutte le sezioni del sito** organizzate per tema. Se sai già cosa cerchi, salta ai 4 accessi rapidi qui sotto.

{{< profili-rapidi >}}

<div class="alert alert-info" role="note">
<p class="mb-0"><i class="bi bi-search me-2" aria-hidden="true"></i><strong>Cerchi qualcosa di specifico?</strong> Usa il <a href="/cerca/">motore di ricerca interno</a> oppure premi <kbd>Ctrl+F</kbd> (Windows/Linux) o <kbd>Cmd+F</kbd> (Mac) sulla tastiera.</p>
</div>

<style>
.ms-section {
  margin: 2.5rem 0 1rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid #003366;
  color: #003366;
  display: flex;
  align-items: center;
  gap: 0.7rem;
}
.ms-section .ms-section-icon {
  width: 2.5rem;
  height: 2.5rem;
  background: #003366;
  color: #fff;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  flex-shrink: 0;
}
.ms-section h2 {
  margin: 0;
  font-size: 1.4rem;
  flex: 1;
}

.ms-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.ms-card {
  background: #fff;
  border-radius: 12px;
  padding: 1.1rem 1.2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  border-left: 5px solid #003366;
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.ms-card:hover, .ms-card:focus {
  transform: translateY(-3px);
  box-shadow: 0 10px 22px rgba(0, 51, 102, 0.14);
  text-decoration: none;
  color: inherit;
}
.ms-card-icon {
  font-size: 2rem;
  color: #003366;
  margin-bottom: 0.5rem;
}
.ms-card-title {
  color: #003366;
  font-weight: 700;
  font-size: 1.05rem;
  margin: 0 0 0.3rem 0;
  line-height: 1.3;
}
.ms-card-desc {
  font-size: 0.9rem;
  color: #495057;
  line-height: 1.4;
  margin: 0;
}
.ms-card-arrow {
  margin-top: auto;
  padding-top: 0.5rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #003366;
}

/* Variante colore per area "emergenza" */
.ms-card.ms-emerg { border-left-color: #dc3545; }
.ms-card.ms-emerg .ms-card-icon, .ms-card.ms-emerg .ms-card-title, .ms-card.ms-emerg .ms-card-arrow { color: #dc3545; }
/* Variante per "formazione" */
.ms-card.ms-edu { border-left-color: #7c3aed; }
.ms-card.ms-edu .ms-card-icon, .ms-card.ms-edu .ms-card-title, .ms-card.ms-edu .ms-card-arrow { color: #7c3aed; }
/* Variante per "strumenti" */
.ms-card.ms-tool { border-left-color: #0891b2; }
.ms-card.ms-tool .ms-card-icon, .ms-card.ms-tool .ms-card-title, .ms-card.ms-tool .ms-card-arrow { color: #0891b2; }
/* Variante per "comunicazione" */
.ms-card.ms-comm { border-left-color: #15803d; }
.ms-card.ms-comm .ms-card-icon, .ms-card.ms-comm .ms-card-title, .ms-card.ms-comm .ms-card-arrow { color: #15803d; }
/* Variante per "documenti" */
.ms-card.ms-doc { border-left-color: #6c757d; }
.ms-card.ms-doc .ms-card-icon, .ms-card.ms-doc .ms-card-title, .ms-card.ms-doc .ms-card-arrow { color: #6c757d; }
/* Variante per "speciale/accessibilità" */
.ms-card.ms-spec { border-left-color: #b45309; }
.ms-card.ms-spec .ms-card-icon, .ms-card.ms-spec .ms-card-title, .ms-card.ms-spec .ms-card-arrow { color: #b45309; }
</style>

<div class="ms-section"><span class="ms-section-icon"><i class="bi bi-house-heart-fill"></i></span><h2>Servizi al cittadino</h2></div>

<div class="ms-grid">
<a class="ms-card" href="/assistente/">
  <div class="ms-card-icon"><i class="bi bi-question-circle-fill"></i></div>
  <p class="ms-card-title">Cosa devo fare?</p>
  <p class="ms-card-desc">Assistente guidato passo-passo: rispondi a domande semplici e ricevi indicazioni in caso di emergenza.</p>
  <span class="ms-card-arrow">Apri assistente →</span>
</a>
<a class="ms-card" href="/piano-familiare/">
  <div class="ms-card-icon"><i class="bi bi-house-heart"></i></div>
  <p class="ms-card-title">Piano Familiare</p>
  <p class="ms-card-desc">Crea e stampa il piano di emergenza della tua famiglia: numeri, punti di ritrovo, kit.</p>
  <span class="ms-card-arrow">Crea il piano →</span>
</a>
<a class="ms-card" href="/cartografia/">
  <div class="ms-card-icon"><i class="bi bi-map-fill"></i></div>
  <p class="ms-card-title">Cartografia Operativa</p>
  <p class="ms-card-desc">Le aree di emergenza del Piano Comunale: aree di attesa, ricovero e ammassamento.</p>
  <span class="ms-card-arrow">Consulta →</span>
</a>
<a class="ms-card ms-tool" href="/strumenti/">
  <div class="ms-card-icon"><i class="bi bi-broadcast-pin"></i></div>
  <p class="ms-card-title">Strumenti in Tempo Reale</p>
  <p class="ms-card-desc">strumenti istituzionali: Windy, INGV, Radar DPC, MeteoAM, ISPRA, EFFIS, ARPA, ANAS.</p>
  <span class="ms-card-arrow">Apri hub →</span>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#dc3545"><i class="bi bi-exclamation-triangle-fill"></i></span><h2>Allerte ed emergenze</h2></div>

<div class="ms-grid">
<a class="ms-card ms-emerg" href="/allerte-meteo/">
  <div class="ms-card-icon"><i class="bi bi-cloud-rain-heavy-fill"></i></div>
  <p class="ms-card-title">Allerte Meteo</p>
  <p class="ms-card-desc">Codici colore, sistema di allertamento, widget Windy/Radar DPC/MeteoAM, fonti ufficiali.</p>
  <span class="ms-card-arrow">Apri →</span>
</a>
<a class="ms-card ms-emerg" href="/numeri-utili/">
  <div class="ms-card-icon"><i class="bi bi-telephone-fill"></i></div>
  <p class="ms-card-title">Numeri Utili</p>
  <p class="ms-card-desc">112, ARES 118, 803 555, contatti del Comune e del Gruppo. Solo numeri verificati.</p>
  <span class="ms-card-arrow">Apri →</span>
</a>
<a class="ms-card ms-emerg" href="/cosa-fare-adesso/">
  <div class="ms-card-icon"><i class="bi bi-list-check"></i></div>
  <p class="ms-card-title">Cosa fare adesso</p>
  <p class="ms-card-desc">Comportamenti concreti durante un'emergenza in corso. Pagina di consultazione rapida.</p>
  <span class="ms-card-arrow">Apri →</span>
</a>
<a class="ms-card ms-emerg" href="/piano-emergenza/">
  <div class="ms-card-icon"><i class="bi bi-shield-fill-check"></i></div>
  <p class="ms-card-title">Piano di Emergenza Comunale</p>
  <p class="ms-card-desc">Struttura e contenuti del Piano di Emergenza del Comune di Genzano di Roma.</p>
  <span class="ms-card-arrow">Apri →</span>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#dc3545"><i class="bi bi-bookmark-star-fill"></i></span><h2>Cosa fare in caso di…</h2></div>

<div class="ms-grid">
<a class="ms-card ms-emerg" href="/rischi-prevenzione/rischio-sismico/">
  <div class="ms-card-icon"><i class="bi bi-activity"></i></div>
  <p class="ms-card-title">Terremoto</p>
  <p class="ms-card-desc">Comportamenti prima/durante/dopo, mappa terremoti recenti INGV, Genzano in zona sismica 2B.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/rischio-vulcanico/">
  <div class="ms-card-icon"><i class="bi bi-droplet-half"></i></div>
  <p class="ms-card-title">Rischio vulcanico (Colli Albani)</p>
  <p class="ms-card-desc">Vulcano Laziale quiescente, sismicità di bassa magnitudo, emissioni di CO₂ in spazi confinati (cantine, pozzi, scantinati). Fonti INGV e ISPRA.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/rischio-idrogeologico/">
  <div class="ms-card-icon"><i class="bi bi-water"></i></div>
  <p class="ms-card-title">Frane e alluvioni</p>
  <p class="ms-card-desc">Rischio idrogeologico sul territorio dei Castelli Romani, comportamenti, fonti ISPRA.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/rischio-incendio/">
  <div class="ms-card-icon"><i class="bi bi-fire"></i></div>
  <p class="ms-card-title">Incendi boschivi</p>
  <p class="ms-card-desc">Periodo AIB giugno-settembre, prevenzione, segnalazione tramite 112.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/temporali-intensi/">
  <div class="ms-card-icon"><i class="bi bi-lightning-charge-fill"></i></div>
  <p class="ms-card-title">Temporali intensi</p>
  <p class="ms-card-desc">Pioggia forte, fulmini, grandine. Mappa fulmini in tempo reale (Lightning Maps).</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/vento-forte/">
  <div class="ms-card-icon"><i class="bi bi-wind"></i></div>
  <p class="ms-card-title">Vento forte</p>
  <p class="ms-card-desc">Raffiche, mareggiate, alberi caduti, precauzioni domestiche.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/ondate-di-calore/">
  <div class="ms-card-icon"><i class="bi bi-thermometer-sun"></i></div>
  <p class="ms-card-title">Ondate di calore</p>
  <p class="ms-card-desc">Temperature estreme, attenzione ad anziani e bambini, idratazione, qualità dell'aria.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/blackout/">
  <div class="ms-card-icon"><i class="bi bi-lightning-charge"></i></div>
  <p class="ms-card-title">Blackout</p>
  <p class="ms-card-desc">Interruzioni elettriche prolungate, comportamenti, riferimenti.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/persone-necessita-specifiche/">
  <div class="ms-card-icon"><i class="bi bi-person-arms-up"></i></div>
  <p class="ms-card-title">Persone con esigenze specifiche</p>
  <p class="ms-card-desc">Disabilità, anziani fragili, donne in gravidanza, bambini molto piccoli.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/kit-emergenza/">
  <div class="ms-card-icon"><i class="bi bi-bag-check-fill"></i></div>
  <p class="ms-card-title">Kit di emergenza</p>
  <p class="ms-card-desc">Cosa mettere nello zaino di emergenza domestico, lista completa e priorità.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/kit-emergenza-economico-progressivo/">
  <div class="ms-card-icon"><i class="bi bi-piggy-bank"></i></div>
  <p class="ms-card-title">Kit di emergenza economico e progressivo</p>
  <p class="ms-card-desc">Come comporre il kit un pezzo alla volta, senza marchi né prodotti specifici.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/rischi-in-parole-semplici/">
  <div class="ms-card-icon"><i class="bi bi-easel"></i></div>
  <p class="ms-card-title">Rischi principali in parole semplici</p>
  <p class="ms-card-desc">Spiegazione accessibile per bambini, persone con bisogni cognitivi e parlanti italiano L2.</p>
</a>
<a class="ms-card ms-emerg" href="/rischi-prevenzione/scuole-genzano-rischi-locali/">
  <div class="ms-card-icon"><i class="bi bi-mortarboard"></i></div>
  <p class="ms-card-title">Scuole di Genzano e rischi locali</p>
  <p class="ms-card-desc">Riferimenti generali per famiglie e personale scolastico, da integrare con il piano di emergenza del singolo istituto.</p>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#7c3aed"><i class="bi bi-mortarboard-fill"></i></span><h2>Formazione e didattica</h2></div>

<div class="ms-grid">
<a class="ms-card ms-edu" href="/formazione/">
  <div class="ms-card-icon"><i class="bi bi-book-half"></i></div>
  <p class="ms-card-title">Hub Formazione</p>
  <p class="ms-card-desc">Punto centrale della formazione: kit didattici, schede, giochi, primo soccorso.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/scuole-da-dove-cominciare/">
  <div class="ms-card-icon"><i class="bi bi-compass-fill"></i></div>
  <p class="ms-card-title">Scuole: da dove cominciare</p>
  <p class="ms-card-desc">Cruscotto unico per ogni ruolo: scegli se sei docente di infanzia/primaria/sec I/sec II, di sostegno/BES, Dirigente/DSGA/RSPP, oppure genitore — e in 2 click arrivi ai materiali giusti.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/percorsi-didattici/">
  <div class="ms-card-icon"><i class="bi bi-rocket-takeoff-fill"></i></div>
  <p class="ms-card-title">Percorsi didattici pronti</p>
  <p class="ms-card-desc">Percorsi pronti all'uso per docenti con poco tempo: PC base, rischio meteo, terremoto, piano familiare, fake news, sicurezza nei luoghi di lavoro/PCTO. Ognuno con destinatari, durata, obiettivi e materiali linkati.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/scuole-strumenti/">
  <div class="ms-card-icon"><i class="bi bi-folder-fill"></i></div>
  <p class="ms-card-title">Strumenti per le scuole (moduli)</p>
  <p class="ms-card-desc">Fac-simile editabili e stampabili in A4: Pacchetto A (ingaggio generico — richiesta, liberatoria minori GDPR, circolare, attestato) e Pacchetto B (PCTO formale — convenzione, progetto formativo, registro+valutazione+certificazione). Per Dirigenti, DSGA, DPO, tutor scolastici.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/dirigenti-e-rspp/">
  <div class="ms-card-icon"><i class="bi bi-building-fill-check"></i></div>
  <p class="ms-card-title">Dirigenti scolastici e RSPP</p>
  <p class="ms-card-desc">Pagina dedicata DS, DSGA, RSPP, ASPP: ruoli del Gruppo, cosa può/non può fare, coordinamento con il piano di emergenza, gestione alunni con disabilità in evacuazione, PCTO con copertura INAIL, casi specifici.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/quadro-normativo-scuola/">
  <div class="ms-card-icon"><i class="bi bi-journals"></i></div>
  <p class="ms-card-title">Quadro normativo per la scuola</p>
  <p class="ms-card-desc">Riepilogo delle norme che regolano l'uso dei materiali del Gruppo nelle scuole: Educazione Civica, PCTO, sicurezza, inclusione, privacy, accessibilità. Una pagina, una fonte unica di verità.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/educazione-civica/">
  <div class="ms-card-icon"><i class="bi bi-mortarboard-fill"></i></div>
  <p class="ms-card-title">Per i docenti — Ed. Civica</p>
  <p class="ms-card-desc">Mappa dei materiali sui 3 Nuclei Concettuali del D.M. 183/2024 (a.s. 2024/2025), Goal Agenda 2030, calendario delle 33 ore, rubriche di valutazione, sezione PCTO e disponibilità del Gruppo nelle scuole.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/schede-stampabili/">
  <div class="ms-card-icon"><i class="bi bi-printer-fill"></i></div>
  <p class="ms-card-title">Schede stampabili</p>
  <p class="ms-card-desc">Schede A4 pronte per la stampa: schede colorabili, case study delle maxi-emergenze italiane (Primaria, Sec I, Sec II), discipline curriculari, ed. civica, allertamento, rubriche valutative.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/storie-e-racconti/">
  <div class="ms-card-icon"><i class="bi bi-book-half"></i></div>
  <p class="ms-card-title">Storie e Racconti</p>
  <p class="ms-card-desc">Fiabe e racconti per bambini 3-11 anni con valore pedagogico per la scuola: ogni storia ha un attimo decisivo + sezione "Per il/la docente" con obiettivi, competenze chiave europee, attività in classe e riferimenti curricolari.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/kit-scuola-infanzia/">
  <div class="ms-card-icon"><i class="bi bi-stars"></i></div>
  <p class="ms-card-title">Kit Scuola Infanzia</p>
  <p class="ms-card-desc">Materiale didattico per insegnanti 3-6 anni: percorso 4 incontri, filastrocche, schede.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/kit-scuola-primaria/">
  <div class="ms-card-icon"><i class="bi bi-pencil-fill"></i></div>
  <p class="ms-card-title">Kit Scuola Primaria</p>
  <p class="ms-card-desc">Materiale didattico per insegnanti 6-11 anni: percorso modulare, esperimenti, role-play, verifiche.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/kit-scuola-secondaria-primo-grado/">
  <div class="ms-card-icon"><i class="bi bi-bookmark-fill"></i></div>
  <p class="ms-card-title">Kit Secondaria I grado</p>
  <p class="ms-card-desc">Materiale 11-14 anni: UdA, casi studio italiani (Amatrice, Ischia), service learning.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/kit-scuola-secondaria-secondo-grado/">
  <div class="ms-card-icon"><i class="bi bi-journal-bookmark-fill"></i></div>
  <p class="ms-card-title">Kit Secondaria II grado</p>
  <p class="ms-card-desc">Materiale 14-19 anni: PCTO, tracce Esame di Stato, dibattiti, compiti di realtà.</p>
</a>
<a class="ms-card ms-edu" href="/giochi/">
  <div class="ms-card-icon"><i class="bi bi-controller"></i></div>
  <p class="ms-card-title">Giochi della Sicurezza</p>
  <p class="ms-card-desc">Giochi educativi gratuiti per bambini 3-19 anni: terremoto, evacuazione, 112.</p>
</a>
<a class="ms-card ms-edu" href="/abili-a-proteggere/">
  <div class="ms-card-icon"><i class="bi bi-heart-fill"></i></div>
  <p class="ms-card-title">Abili a Proteggere</p>
  <p class="ms-card-desc">Attività accessibili per persone con difficoltà cognitive o motorie, anziani e bambini fragili: pulsanti grandi, testi semplici, nessun timer.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/easy-to-read-scuola/">
  <div class="ms-card-icon"><i class="bi bi-bookmark-heart-fill"></i></div>
  <p class="ms-card-title">Easy-to-Read per le scuole</p>
  <p class="ms-card-desc">Schede semplificate (112, terremoto, evacuazione, zaino) con frasi corte e pittogrammi ARASAAC. Per alunni con disabilità intellettiva, BES/DSA, italiano L2.</p>
</a>
<a class="ms-card ms-edu" href="/formazione/psicologia-emergenza/">
  <div class="ms-card-icon"><i class="bi bi-emoji-smile"></i></div>
  <p class="ms-card-title">Psicologia dell'emergenza</p>
  <p class="ms-card-desc">Reazioni emotive normali e segnali di attenzione, modello OMS Psychological First Aid (Look · Listen · Link), indicazioni per fascia d'età e per la scuola dopo un evento avverso. Pagina divulgativa: non sostituisce lo psicologo.</p>
</a>
<a class="ms-card ms-edu" href="/glossario/">
  <div class="ms-card-icon"><i class="bi bi-book"></i></div>
  <p class="ms-card-title">Glossario PC</p>
  <p class="ms-card-desc">50+ sigle e termini tecnici (PAI, COC, DICOMAC, IT-alert, ecc.) spiegati in parole semplici.</p>
</a>
<a class="ms-card ms-edu" href="/standard-iso/">
  <div class="ms-card-icon"><i class="bi bi-rulers"></i></div>
  <p class="ms-card-title">Standard ISO per la PC</p>
  <p class="ms-card-desc">Hub di consultazione su 30 standard internazionali ISO rilevanti per la Protezione Civile (emergency management, gestione del rischio, comunicazione di crisi, segnaletica, adattamento climatico).</p>
</a>
<a class="ms-card ms-edu" href="/feed-rss/">
  <div class="ms-card-icon"><i class="bi bi-rss-fill"></i></div>
  <p class="ms-card-title">Feed RSS</p>
  <p class="ms-card-desc">Ricevi le notizie del Gruppo nel tuo aggregatore preferito (Feedly, Inoreader, Thunderbird, NetNewsWire). 14 feed dedicati per sezione del sito. Niente registrazione, niente cookie, niente dati personali.</p>
</a>
<a class="ms-card ms-edu" href="/stato-sistema/">
  <div class="ms-card-icon"><i class="bi bi-activity"></i></div>
  <p class="ms-card-title">Stato del sistema</p>
  <p class="ms-card-desc">Cruscotto pubblico di trasparenza tecnica: stato di allerta, modalità del sito, automazioni di manutenzione con semaforo, conformità AGID e WCAG.</p>
</a>
<a class="ms-card ms-edu" href="/storia/">
  <div class="ms-card-icon"><i class="bi bi-clock-history"></i></div>
  <p class="ms-card-title">Storia del territorio</p>
  <p class="ms-card-desc">Linea del tempo dei Castelli Romani: natura vulcanica, terremoti storici, evoluzione del sistema di protezione civile. Ogni voce con fonte istituzionale.</p>
</a>
<a class="ms-card ms-edu" href="/lanterna/">
  <div class="ms-card-icon"><i class="bi bi-lightbulb"></i></div>
  <p class="ms-card-title">Modalità Lanterna</p>
  <p class="ms-card-desc">Pagina ultra-leggera di sopravvivenza: torcia, bussola, schermo sempre acceso, 112 sempre in alto. Per poca batteria, rete debole, di notte.</p>
</a>
<a class="ms-card ms-edu" href="/lis/">
  <div class="ms-card-icon"><i class="bi bi-hand-index-thumb"></i></div>
  <p class="ms-card-title">Contenuti in LIS</p>
  <p class="ms-card-desc">I contenuti vitali sulla sicurezza in Lingua Italiana dei Segni, per le persone sorde segnanti. Video con sottotitoli e trascrizione completa.</p>
</a>
<a class="ms-card ms-edu" href="/quiz-preparazione/">
  <div class="ms-card-icon"><i class="bi bi-clipboard-check"></i></div>
  <p class="ms-card-title">Quanto sei preparato?</p>
  <p class="ms-card-desc">Quiz adattivo e non giudicante: scopri cosa ti manca per essere pronto a un'emergenza. Profilo di preparazione, piano d'azione su misura, badge scaricabile.</p>
</a>
<a class="ms-card ms-edu" href="/open-data/">
  <div class="ms-card-icon"><i class="bi bi-database"></i></div>
  <p class="ms-card-title">Open Data</p>
  <p class="ms-card-desc">I dataset delle attività del Gruppo (interventi, ore di volontariato, esercitazioni, formazione, dotazioni) in formato aperto CSV e JSON, riusabili sotto licenza CC BY 4.0.</p>
</a>
<a class="ms-card ms-edu" href="/podcast/">
  <div class="ms-card-icon"><i class="bi bi-mic-fill"></i></div>
  <p class="ms-card-title">Podcast</p>
  <p class="ms-card-desc">Il podcast del Gruppo Comunale: episodi audio sui rischi locali, esercitazioni, interviste. Feed RSS per Spotify, Apple Podcasts e ogni app.</p>
</a>
<a class="ms-card ms-edu" href="/faq/">
  <div class="ms-card-icon"><i class="bi bi-patch-question-fill"></i></div>
  <p class="ms-card-title">Domande frequenti</p>
  <p class="ms-card-desc">domande con risposta su allerte, emergenze, prevenzione, volontariato e numeri.</p>
</a>
<a class="ms-card ms-edu" href="/trasparenza/">
  <div class="ms-card-icon"><i class="bi bi-eye-fill"></i></div>
  <p class="ms-card-title">Trasparenza</p>
  <p class="ms-card-desc">Natura giuridica del Gruppo (articolazione del Comune iscritta al RUNTS, determina G14230 del 28/10/2024), riferimenti al portale RUNTS per statuto e atti, procedura di accesso civico generalizzato (D.Lgs. 33/2013).</p>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#7f1d1d"><i class="bi bi-printer-fill"></i></span><h2>Kit Calamità — Schede stampabili per categorie vulnerabili</h2></div>

<div class="ms-grid">
<a class="ms-card ms-emerg" href="/formazione/kit-calamita/">
  <div class="ms-card-icon"><i class="bi bi-grid-3x3-gap-fill"></i></div>
  <p class="ms-card-title">Hub Kit Calamità</p>
  <p class="ms-card-desc">Cruscotto di 12 kit operativi: scegli la tua situazione e arrivi alle schede pronte. Standard NCTSN, IFRC, WHO, Sphere, FEANTSA, UNHCR, IOM, IFE, MISP, WSAVA, Eurocarers.</p>
</a>
<a class="ms-card ms-emerg" href="/formazione/kit-calamita-bambini/">
  <div class="ms-card-icon"><i class="bi bi-emoji-smile"></i></div>
  <p class="ms-card-title">Kit Bambini 3-14 anni</p>
  <p class="ms-card-desc">PFA Children NCTSN/IFRC/WHO/UNHCR/Sphere. 4 fasce + inclusione (autismo, L2, ipovisione).</p>
</a>
<a class="ms-card ms-emerg" href="/formazione/kit-calamita-neonati/">
  <div class="ms-card-icon"><i class="bi bi-balloon-heart"></i></div>
  <p class="ms-card-title">Kit Neonati 0-3 anni</p>
  <p class="ms-card-desc">IFE Core Group v3.0 + WHO Code latte materno. Termoregolazione, allattamento, segnali rossi.</p>
</a>
<a class="ms-card ms-emerg" href="/formazione/kit-calamita-anziani/">
  <div class="ms-card-icon"><i class="bi bi-person-arms-up"></i></div>
  <p class="ms-card-title">Kit Anziani in casa</p>
  <p class="ms-card-desc">HelpAge + WHO mhGAP + SIGG/AIP. Carta identità, reminiscence, calendario orientativo.</p>
</a>
<a class="ms-card ms-emerg" href="/formazione/kit-calamita-caregiver-familiari/">
  <div class="ms-card-icon"><i class="bi bi-heart-pulse-fill"></i></div>
  <p class="ms-card-title">Kit Caregiver familiari</p>
  <p class="ms-card-desc">L. 205/2017 + Carta Eurocarers 2014 + WHO Self-care 2022. Carta assistito, piano allettato.</p>
</a>
<a class="ms-card ms-emerg" href="/formazione/kit-calamita-strutture-sanitarie/">
  <div class="ms-card-icon"><i class="bi bi-hospital-fill"></i></div>
  <p class="ms-card-title">Kit Strutture Sanitarie / RSA</p>
  <p class="ms-card-desc">Min. Salute + AGENAS + WHO Hospital Safety Index. Triage SALT geriatrico, comfort BPSD.</p>
</a>
<a class="ms-card ms-emerg" href="/formazione/kit-calamita-disabilita-adulti/">
  <div class="ms-card-icon"><i class="bi bi-universal-access-circle"></i></div>
  <p class="ms-card-title">Kit Disabilità Adulti</p>
  <p class="ms-card-desc">CRPD ONU art. 11 + L. 18/2009 + WHO. 4 categorie (motoria, sensoriale, cognitiva, psichiatrica).</p>
</a>
<a class="ms-card ms-emerg" href="/formazione/kit-calamita-terapie-salvavita/">
  <div class="ms-card-icon"><i class="bi bi-capsule-pill"></i></div>
  <p class="ms-card-title">Kit Terapie Salvavita</p>
  <p class="ms-card-desc">WHO Health Cluster + Sphere + ARERA. Dialisi, ossigenoterapia, oncologici, trapiantati.</p>
</a>
<a class="ms-card ms-emerg" href="/formazione/kit-calamita-gravidanza/">
  <div class="ms-card-icon"><i class="bi bi-flower2"></i></div>
  <p class="ms-card-title">Kit Gravidanza e neomamme</p>
  <p class="ms-card-desc">MISP IAWG + WHO + UNFPA + Sphere. 5 priorità MISP, segnali rossi, parto improvviso.</p>
</a>
<a class="ms-card ms-emerg" href="/formazione/kit-calamita-senza-fissa-dimora/">
  <div class="ms-card-icon"><i class="bi bi-house-x"></i></div>
  <p class="ms-card-title">Kit Senza Fissa Dimora</p>
  <p class="ms-card-desc">FEANTSA ETHOS + FIO.PSD + Min. Lavoro 2015. Identificazione minima, mappa risorse Castelli.</p>
</a>
<a class="ms-card ms-emerg" href="/formazione/kit-calamita-italiano-l2/">
  <div class="ms-card-icon"><i class="bi bi-translate"></i></div>
  <p class="ms-card-title">Kit Italiano L2 / Stranieri</p>
  <p class="ms-card-desc">UNHCR CwC 2020 + IOM CCCM + Sphere. Carta multilingua + frasario in 7 lingue.</p>
</a>
<a class="ms-card ms-emerg" href="/formazione/kit-calamita-animali/">
  <div class="ms-card-icon"><i class="bi bi-piggy-bank"></i></div>
  <p class="ms-card-title">Kit Animali domestici</p>
  <p class="ms-card-desc">D.Lgs. 1/2018 art. 12 + L. 281/1991 + WSAVA. Lezione Katrina/PETS Act 2006.</p>
</a>
<a class="ms-card ms-emerg" href="/formazione/kit-calamita-volontari-pc/">
  <div class="ms-card-icon"><i class="bi bi-shield-shaded"></i></div>
  <p class="ms-card-title">Kit Volontari PC (auto-cura)</p>
  <p class="ms-card-desc">IFRC Caring + NCTSN STS + WHO mhGAP + ProQOL-5. Auto-valutazione, decompressione.</p>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#15803d"><i class="bi bi-megaphone-fill"></i></span><h2>Comunicazioni e canali</h2></div>

<div class="ms-grid">
<a class="ms-card ms-comm" href="/comunicazioni/">
  <div class="ms-card-icon"><i class="bi bi-newspaper"></i></div>
  <p class="ms-card-title">Archivio Comunicazioni</p>
  <p class="ms-card-desc">Tutte le notizie pubblicate dal Gruppo: allerte, eventi, formazione, attivazioni, novità.</p>
</a>
<a class="ms-card ms-comm" href="/social-media-policy/">
  <div class="ms-card-icon"><i class="bi bi-share-fill"></i></div>
  <p class="ms-card-title">Social Media Policy</p>
  <p class="ms-card-desc">Le regole con cui il Gruppo usa i propri canali social: Facebook, Instagram, X, Telegram.</p>
</a>
<a class="ms-card ms-comm" href="/cerca/">
  <div class="ms-card-icon"><i class="bi bi-search"></i></div>
  <p class="ms-card-title">Motore di ricerca interno</p>
  <p class="ms-card-desc">Cerca tra tutte le pagine del sito per parole chiave, titolo, contenuto.</p>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon"><i class="bi bi-people-fill"></i></span><h2>Sul Gruppo</h2></div>

<div class="ms-grid">
<a class="ms-card" href="/chi-siamo/">
  <div class="ms-card-icon"><i class="bi bi-info-circle-fill"></i></div>
  <p class="ms-card-title">Chi siamo</p>
  <p class="ms-card-desc">Storia, struttura e missione del Gruppo Comunale Volontari di Genzano (dal 1981).</p>
</a>
<a class="ms-card" href="/contatti/">
  <div class="ms-card-icon"><i class="bi bi-envelope-fill"></i></div>
  <p class="ms-card-title">Contatti</p>
  <p class="ms-card-desc">Sede in Via Sicilia 13-15, email, recapiti per emergenze e attività ordinarie.</p>
</a>
<a class="ms-card" href="/diventa-volontario/">
  <div class="ms-card-icon"><i class="bi bi-person-plus-fill"></i></div>
  <p class="ms-card-title">Diventa Volontario</p>
  <p class="ms-card-desc">Come iscriversi al Gruppo, requisiti, formazione obbligatoria, cosa puoi fare.</p>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#003366"><i class="bi bi-journals"></i></span><h2>Normativa di Protezione Civile</h2></div>

<div class="ms-grid">
<a class="ms-card ms-doc" href="/normativa/">
  <div class="ms-card-icon"><i class="bi bi-bookmark-fill"></i></div>
  <p class="ms-card-title">Hub Normativa</p>
  <p class="ms-card-desc">Indice degli approfondimenti normativi: chi fa cosa nel Servizio Nazionale, dal Sindaco al Capo Dipartimento.</p>
  <span class="ms-card-arrow">Apri →</span>
</a>
<a class="ms-card ms-doc" href="/normativa/testo-unico-protezione-civile/">
  <div class="ms-card-icon"><i class="bi bi-book-fill"></i></div>
  <p class="ms-card-title">Codice della Protezione Civile</p>
  <p class="ms-card-desc">D.Lgs. 1/2018 spiegato in 7 Capi: finalità, organizzazione, previsione, pianificazione, emergenze, volontariato.</p>
  <span class="ms-card-arrow">Apri →</span>
</a>
<a class="ms-card ms-doc" href="/normativa/testo-unico-protezione-civile/capo-3-previsione-prevenzione/">
  <div class="ms-card-icon"><i class="bi bi-eye-fill"></i></div>
  <p class="ms-card-title">Capo III — Previsione e prevenzione</p>
  <p class="ms-card-desc">Sistema di allertamento, comunicazione del rischio, formazione: il cuore della cultura di protezione civile.</p>
  <span class="ms-card-arrow">Leggi →</span>
</a>
<a class="ms-card ms-doc" href="/normativa/testo-unico-protezione-civile/capo-4-pianificazione/">
  <div class="ms-card-icon"><i class="bi bi-clipboard-data-fill"></i></div>
  <p class="ms-card-title">Capo IV — Pianificazione</p>
  <p class="ms-card-desc">Piano nazionale, regionale, provinciale e comunale: come si pianifica una emergenza prima che accada.</p>
  <span class="ms-card-arrow">Leggi →</span>
</a>
<a class="ms-card ms-doc" href="/normativa/testo-unico-protezione-civile/capo-6-volontariato/">
  <div class="ms-card-icon"><i class="bi bi-person-hearts"></i></div>
  <p class="ms-card-title">Capo VI — Volontariato</p>
  <p class="ms-card-desc">Diritti e doveri del volontario di Protezione Civile: tutele lavorative, rimborsi, formazione.</p>
  <span class="ms-card-arrow">Leggi →</span>
</a>
<a class="ms-card ms-doc" href="/normativa/evoluzione-procedure-emergenza/">
  <div class="ms-card-icon"><i class="bi bi-clock-history"></i></div>
  <p class="ms-card-title">Evoluzione delle procedure di emergenza</p>
  <p class="ms-card-desc">Come sono cambiate le procedure di Protezione Civile in Italia: da Vajont (1963) al sistema attuale.</p>
  <span class="ms-card-arrow">Leggi →</span>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#0891b2"><i class="bi bi-grid-3x3-gap-fill"></i></span><h2>Strumenti, risorse, download</h2></div>

<div class="ms-grid">
<a class="ms-card ms-tool" href="/strumenti/">
  <div class="ms-card-icon"><i class="bi bi-broadcast-pin"></i></div>
  <p class="ms-card-title">Strumenti in Tempo Reale</p>
  <p class="ms-card-desc">Hub dei strumenti online: meteo, terremoti, idrogeologico, incendi, qualità aria.</p>
</a>
<a class="ms-card ms-tool" href="/cartografia/">
  <div class="ms-card-icon"><i class="bi bi-geo-alt-fill"></i></div>
  <p class="ms-card-title">Cartografia Operativa</p>
  <p class="ms-card-desc">Aree di Attesa (10), Aree di Ricovero (4), Aree di Ammassamento (2) con cartelli e indirizzi.</p>
</a>
<a class="ms-card ms-tool" href="/area-download/">
  <div class="ms-card-icon"><i class="bi bi-download"></i></div>
  <p class="ms-card-title">Area Download</p>
  <p class="ms-card-desc">Documenti, modulistica, normativa: PDF scaricabili del Piano, ordinanze, materiale ufficiale.</p>
</a>
<a class="ms-card ms-tool" href="/siti-utili/">
  <div class="ms-card-icon"><i class="bi bi-link-45deg"></i></div>
  <p class="ms-card-title">Siti utili</p>
  <p class="ms-card-desc">Link a istituzioni di Protezione Civile: DPC, Regione Lazio, INGV, ISPRA, Comune.</p>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#b45309"><i class="bi bi-universal-access-circle"></i></span><h2>Versioni speciali e accessibilità</h2></div>

<div class="ms-grid">
<a class="ms-card ms-spec" href="/facile-da-leggere/">
  <div class="ms-card-icon"><i class="bi bi-emoji-smile-fill"></i></div>
  <p class="ms-card-title">Facile da leggere</p>
  <p class="ms-card-desc">Le informazioni essenziali in versione semplice. Frasi corte, parole facili. Per tutti.</p>
</a>
<a class="ms-card ms-spec" href="/english/">
  <div class="ms-card-icon"><i class="bi bi-translate"></i></div>
  <p class="ms-card-title">English version</p>
  <p class="ms-card-desc">Essential Civil Protection info in English for tourists and foreign residents.</p>
</a>
<a class="ms-card ms-spec" href="/accessibilita/">
  <div class="ms-card-icon"><i class="bi bi-eye-fill"></i></div>
  <p class="ms-card-title">Dichiarazione di Accessibilità</p>
  <p class="ms-card-desc">Conformità WCAG 2.2 AA, contenuti di terze parti, meccanismo di feedback.</p>
</a>
</div>

<div class="ms-section"><span class="ms-section-icon" style="background:#6c757d"><i class="bi bi-file-earmark-text-fill"></i></span><h2>Documenti legali e privacy</h2></div>

<div class="ms-grid">
<a class="ms-card ms-doc" href="/privacy/">
  <div class="ms-card-icon"><i class="bi bi-shield-lock-fill"></i></div>
  <p class="ms-card-title">Privacy e Cookie</p>
  <p class="ms-card-desc">Informativa GDPR, gestione dei cookie, widget di terze parti, diritti dell'utente.</p>
</a>
<a class="ms-card ms-doc" href="/note-legali/">
  <div class="ms-card-icon"><i class="bi bi-file-text-fill"></i></div>
  <p class="ms-card-title">Note Legali</p>
  <p class="ms-card-desc">Titolarità, condizioni d'uso, copyright dei contenuti del sito.</p>
</a>
<a class="ms-card ms-doc" href="/social-media-policy/">
  <div class="ms-card-icon"><i class="bi bi-chat-square-quote-fill"></i></div>
  <p class="ms-card-title">Social Media Policy</p>
  <p class="ms-card-desc">Linee guida e regole di comportamento sui canali social ufficiali del Gruppo.</p>
</a>
</div>

---

<p class="text-center text-muted mt-4">
<i class="bi bi-info-circle me-1" aria-hidden="true"></i>
Pagina aggiornata automaticamente quando vengono pubblicate nuove sezioni del sito.
Se trovi un link rotto o una pagina mancante, segnalacelo a
<a href="mailto:segreteria@protezionecivilegenzano.it">segreteria@protezionecivilegenzano.it</a>.
</p>
