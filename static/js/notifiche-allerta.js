/* notifiche-allerta.js — Notifiche browser per l'allerta meteo (idea #2 roadmap).
 *
 * SENZA Service Worker (la PWA è vietata per scelta di progetto): le notifiche
 * funzionano SOLO finché una scheda del sito resta aperta. È un palliativo
 * onesto, dichiarato chiaramente all'utente.
 *
 * Come funziona:
 *  - l'utente attiva l'opt-in dal toggle sulla pagina /allerte-meteo/
 *    (contenitore #notifiche-allerta-toggle);
 *  - una volta attivo, questo script — caricato su ogni pagina — interroga
 *    ogni pochi minuti l'endpoint pubblico window.PCGENZANO_ALLERTA_URL;
 *  - se il livello SALE ad arancione/rosso (o c'è un'emergenza attiva) e lo
 *    stato è cambiato rispetto all'ultimo visto, lancia una notifica nativa
 *    del browser + vibrazione su mobile dove supportata.
 *
 * Privacy: nessun tracciamento, nessun ID utente. Interroga solo il JSON
 * pubblico dell'allerta. Le preferenze stanno in localStorage.
 */
(function () {
  "use strict";

  var KEY = "pcgenzano-notifiche-allerta";
  var ENDPOINT = window.PCGENZANO_ALLERTA_URL || "/allerta-stato/index.json";
  var POLL_NORMALE = 5 * 60 * 1000; // 5 minuti
  var POLL_INTENSO = 90 * 1000;     // 90 secondi se siamo già in arancione/rosso
  var timer = null;

  function stato() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; }
    catch (e) { return {}; }
  }
  function salva(s) {
    try { localStorage.setItem(KEY, JSON.stringify(s)); } catch (e) {}
  }
  function livelloGrave(liv) {
    var l = String(liv || "").toLowerCase();
    return l.indexOf("arancion") > -1 || l.indexOf("ross") > -1;
  }

  function notifica(titolo, corpo) {
    if (!("Notification" in window) || Notification.permission !== "granted") return;
    try {
      var n = new Notification(titolo, {
        body: corpo,
        tag: "pcgenzano-allerta",
        lang: "it",
        requireInteraction: true
      });
      n.onclick = function () {
        window.focus();
        window.location.href = (window.PCGENZANO_ALLERTE_PAGE || "/allerte-meteo/");
        n.close();
      };
    } catch (e) {}
    if (navigator.vibrate) { try { navigator.vibrate([200, 100, 200, 100, 200]); } catch (e) {} }
  }

  function controlla(primaVolta) {
    fetch(ENDPOINT, { cache: "no-store" })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d) return;
        var s = stato();
        var cambiato = d.livello !== s.lastLivello ||
                       d.ultimo_aggiornamento !== s.lastAggiornamento ||
                       (d.emergenza_attiva && !s.lastEmergenza);
        var grave = livelloGrave(d.livello) || d.emergenza_attiva;

        if (!primaVolta && cambiato && grave) {
          if (d.emergenza_attiva) {
            notifica("Emergenza in corso — PC Genzano",
                     (d.emergenza_titolo || "È attiva un'emergenza.") + " Apri il sito per le indicazioni.");
          } else {
            notifica("Allerta meteo " + (d.livello || "") + " — PC Genzano",
                     (d.titolo || "Il livello di allerta è salito.") + " Tocca per i dettagli.");
          }
        }
        // aggiorna lo stato visto
        s.lastLivello = d.livello;
        s.lastAggiornamento = d.ultimo_aggiornamento;
        s.lastEmergenza = !!d.emergenza_attiva;
        salva(s);

        // ritmo di polling adattivo
        var intervallo = grave ? POLL_INTENSO : POLL_NORMALE;
        if (timer) { clearTimeout(timer); }
        timer = setTimeout(function () { controlla(false); }, intervallo);
      })
      .catch(function () {
        if (timer) { clearTimeout(timer); }
        timer = setTimeout(function () { controlla(false); }, POLL_NORMALE);
      });
  }

  function avviaPolling() {
    if (timer) { clearTimeout(timer); }
    controlla(true); // prima chiamata: stabilisce la baseline, NON notifica
  }
  function fermaPolling() {
    if (timer) { clearTimeout(timer); timer = null; }
  }

  // ── Toggle UI (solo dove c'è il contenitore, cioè /allerte-meteo/) ──
  function rendiToggle(box) {
    var supportato = "Notification" in window;
    var s = stato();
    box.innerHTML = "";

    var card = document.createElement("div");
    card.className = "notifiche-allerta-card";

    var h = document.createElement("h2");
    h.className = "notifiche-allerta-titolo";
    h.innerHTML = '<i class="bi bi-bell me-2" aria-hidden="true"></i>Notifiche di allerta sul browser';
    card.appendChild(h);

    var p = document.createElement("p");
    p.className = "notifiche-allerta-desc";
    card.appendChild(p);

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "btn btn-primary notifiche-allerta-btn";

    var nota = document.createElement("p");
    nota.className = "notifiche-allerta-nota small";
    nota.innerHTML = "Le notifiche funzionano <strong>solo finché tieni aperta una scheda del sito</strong> " +
      "(non è un'app: è una scelta di progetto per evitare versioni del sito non aggiornate). " +
      "Nessun dato personale viene raccolto: il sito controlla solo il bollettino pubblico. " +
      "Per un avviso che arriva sempre, iscriviti anche al canale Telegram qui sotto.";

    function aggiorna() {
      var st = stato();
      if (!supportato) {
        p.textContent = "Il tuo browser non supporta le notifiche. Usa il canale Telegram qui sotto.";
        btn.hidden = true;
        return;
      }
      if (Notification.permission === "denied") {
        p.textContent = "Hai bloccato le notifiche per questo sito. Per riattivarle, sblocca le notifiche dalle impostazioni del browser.";
        btn.hidden = true;
        return;
      }
      if (st.enabled && Notification.permission === "granted") {
        p.textContent = "Notifiche attive. Riceverai un avviso se il livello di allerta sale ad arancione o rosso, o se è in corso un'emergenza.";
        btn.textContent = "Disattiva le notifiche";
        btn.className = "btn btn-outline-primary notifiche-allerta-btn";
      } else {
        p.textContent = "Attiva le notifiche del browser per ricevere un avviso quando il livello di allerta sale.";
        btn.textContent = "Attiva le notifiche di allerta";
        btn.className = "btn btn-primary notifiche-allerta-btn";
      }
      btn.hidden = false;
    }

    btn.addEventListener("click", function () {
      var st = stato();
      if (st.enabled) {
        st.enabled = false; salva(st); fermaPolling(); aggiorna();
        return;
      }
      Notification.requestPermission().then(function (perm) {
        if (perm === "granted") {
          st.enabled = true; salva(st); avviaPolling();
        }
        aggiorna();
      }).catch(function () { aggiorna(); });
    });

    card.appendChild(btn);
    card.appendChild(nota);
    box.appendChild(card);
    aggiorna();
  }

  document.addEventListener("DOMContentLoaded", function () {
    var box = document.getElementById("notifiche-allerta-toggle");
    if (box) { rendiToggle(box); }
    // polling in background su QUALSIASI pagina, se l'utente ha già attivato
    var s = stato();
    if (s.enabled && "Notification" in window && Notification.permission === "granted") {
      avviaPolling();
    }
  });
})();
