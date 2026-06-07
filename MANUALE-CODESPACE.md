# 📘 Guida Codespace — passo passo

Lavorare sul sito **da GitHub Codespaces**, anche dal telefono, quando il PC di
casa fa i capricci. Guida semplice, passo passo.

Pensa al Codespace come a **un computer in affitto dentro GitHub**: si accende,
ci lavori dal browser, e quando spegni non costa più nulla. Sul sito è già tutto
preparato (`.devcontainer/setup.sh`): si configura da solo.

> Le ore gratuite sono ~60 al mese — più che sufficienti se ricordi di **spegnere**
> il Codespace quando finisci (Parte C).

---

## 🟢 PARTE A — Da fare UNA VOLTA SOLA (le password segrete)

Servono perché alcune cose (cartine social via Gemini, lettura siti via Firecrawl,
pubblicazione su Aruba) hanno bisogno di chiavi segrete. Le metti una volta e
GitHub le ricorda.

1. Vai su **github.com** e fai login.
2. In alto a destra clicca la tua **foto profilo** → **Settings** (Impostazioni).
3. Menù a sinistra, scorri fino a **Codespaces**, cliccaci.
4. Sezione **Codespaces secrets** → **New secret** (Nuovo segreto).
5. Aggiungi questi segreti, **uno per volta**. Per ognuno: Nome → Valore → in
   *Repository access* scegli `sito-pc-genzano`.

   | Nome (scrivilo identico) | Cos'è |
   |---|---|
   | `GEMINI_API_KEY` | chiave per le bozze social/cartine |
   | `FIRECRAWL_API_KEY` | chiave per leggere i siti istituzionali |
   | `FTP_SERVER` | indirizzo del server Aruba |
   | `FTP_USERNAME` | utente Aruba |
   | `FTP_PASSWORD` | password Aruba |

   > 💡 I valori li hai già: Gemini nel file `~/.bashrc` del PC, gli altri nei
   > *Secrets* del repo su GitHub. Se non li hai sottomano, va bene metterne
   > **solo alcuni** ora e aggiungere il resto dopo. Senza, il Codespace funziona
   > lo stesso: solo quei servizi specifici non vanno.

✅ Questa parte si fa **una volta sola**. Le prossime volte si salta alla Parte B.

---

## 🔵 PARTE B — Ogni volta che vuoi lavorare

### Accendere il Codespace

1. Apri la pagina del repository:
   **github.com/SviluppoItaliaDigitale/sito-pc-genzano**
2. Clicca il pulsante verde **`<> Code`**.
3. Clicca la linguetta **Codespaces**.
4. Clicca **Create codespace on main** (pulsante verde).
   - Se ne avevi già uno, compare nella lista: cliccaci sopra invece di crearne
     un altro.
5. Si apre **Visual Studio Code dentro il browser**. Aspetta qualche minuto: in
   basso scorre del testo — è `setup.sh` che installa **tutto** (Hugo, Claude
   Code, le skill, gli agent…).
6. **Hai finito di aspettare** quando compare la scritta `Ambiente pronto.` con il
   riepilogo (skill, agent, Hugo).

### Vedere il sito mentre lavori

1. In basso ci sono le linguette **TERMINAL / PORTS / PROBLEMS…** → clicca
   **TERMINAL**.
2. Clicca nel riquadro nero, scrivi e premi **Invio**:
   ```
   hugo server
   ```
3. Compare un avviso con **"Open in Browser"** (oppure vai nella linguetta
   **PORTS** e clicca l'icona del mondo 🌐 accanto alla porta **1313**).
4. Si apre il sito in una nuova scheda: ogni modifica a un file lo aggiorna da
   solo. 🎉

### Usare Claude (come adesso)

1. Apri un **secondo terminale**: clicca il **`+`** in alto a destra del riquadro
   (così Hugo continua nel primo).
2. Scrivi e premi **Invio**:
   ```
   claude
   ```
   Da qui parli con Claude — con skill, agent e MCP già pronti.
   - La prima volta chiede il login: segui le istruzioni a schermo (apri il link,
     incolla il codice).

---

## 💾 PARTE C — Salvare il lavoro e spegnere

⚠️ **Importante:** il lavoro nel Codespace **non va sul sito da solo**. Va salvato
su GitHub (in gergo: *commit + push*). Il modo più semplice: dentro `claude`
scrivi **"pubblica"** e fa tutto lui.

In alternativa, a mano nel terminale:
```
git add -A
git commit -m "descrizione di cosa hai fatto"
git push
```

### Spegnere (per non sprecare le ore gratuite)

1. Torna su **github.com/SviluppoItaliaDigitale/sito-pc-genzano** → **`<> Code`**
   → **Codespaces**.
2. Accanto al tuo Codespace clicca i **tre puntini `…`**:
   - **Stop codespace** → lo **mette in pausa** (riprende dove avevi lasciato).
   - **Delete** → lo **cancella del tutto** (usa solo dopo aver fatto *push* di tutto).

> 🟡 Se non lo spegni, GitHub lo ferma da solo dopo 30 minuti di inattività.

---

## 📱 Dal telefono

Funziona uguale: apri il sito di GitHub dal browser del telefono e segui gli
stessi passi. Per un'esperienza migliore c'è l'**app GitHub** (sull'app store):
apri il repo → tab **Codespaces** → crea/apri.

---

## ❓ Problemi comuni

| Cosa vedi | Cosa fare |
|---|---|
| `claude: command not found` | Chiudi e riapri il terminale (il PATH si aggiorna), oppure scrivi `export PATH="$HOME/.local/bin:$PATH"` |
| Firecrawl/Gemini non funzionano | Manca il segreto: torna alla **Parte A**, poi **Stop + riapri** il Codespace |
| Il sito non si apre | Controlla che `hugo server` sia ancora in esecuzione nel primo terminale; usa la porta **1313** in **PORTS** |
| Setup non finito / errori | Rilancia a mano: `bash .devcontainer/setup.sh` (è sicuro ripeterlo) |

---

> 🔧 **Per chi mantiene il sito:** tutto l'ambiente è in un unico file
> `.devcontainer/setup.sh`. La versione di Hugo lì dentro deve restare identica a
> quella in `.github/workflows/deploy.yml`. Le skill/agent/MCP rispecchiano il PC.
