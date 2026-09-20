_[Indice manuale](README.md)_

# Parte 42 — Pubblicazione automatica su Instagram e Facebook

Dal **20 settembre 2026** i contenuti del sito escono da soli su Instagram e Facebook. Non serve
più copiare e incollare le bozze: il materiale che il sito già produce viene preso, messo in coda
e pubblicato due volte al giorno.

Questa Parte spiega cosa succede senza di te, cosa puoi fermare e cosa non si può più cambiare
una volta che un post è uscito.

## 42.1 — Dove vive il sistema

La pubblicazione **non sta nel repository del sito**. Sta in un repository separato e **privato**,
[`social-pc-genzano`](https://github.com/SviluppoItaliaDigitale/social-pc-genzano).

Il motivo è pratico, non organizzativo: le credenziali delle pagine social non possono stare in un
repository pubblico. Le immagini invece **devono** restare nel repository del sito, perché
Instagram le scarica da un indirizzo pubblico e da un repository privato non ci arriverebbe.

La dipendenza va in una direzione sola: il repository privato legge quello del sito, mai il
contrario. Nel sito non è cambiato nulla, continua a generare bozze e immagini come sempre
(vedi [Parte 11](parte-11-testi-per-i-social-instagram-facebook-x-telegram.md) e
[Parte 16](parte-16-bozze-social-gestione-quota-api.md)).

## 42.2 — Cosa succede, e quando

1. Pubblichi un articolo sul sito.
2. Il sito genera da solo i testi e le immagini social in `social-bozze/AAAA/MM/<slug>/`.
3. Due volte al giorno il sistema guarda cosa è pronto, lo mette in coda **uno al giorno**, e
   pubblica quello arrivato a scadenza.
4. Le fasce sono **08:30 e 18:30**, ora italiana.

Su Instagram esce il carosello con tutte le immagini dell'articolo, più la **storia** da 24 ore.
Su Facebook esce lo stesso materiale con il **testo scritto per Facebook**, che è più disteso e
contiene il link all'articolo. Sono due testi diversi, come raccomanda la Parte 11: qui la
differenza è che vengono scritti e usati senza che tu debba fare niente.

Il token di Instagram scade ogni sessanta giorni e si rinnova da solo il **primo e il sedici** di
ogni mese. Il permesso della pagina Facebook non scade.

## 42.3 — Cosa non esce mai in automatico

Queste esclusioni sono scritte nel codice, non in una configurazione modificabile, perché
riguardano la responsabilità del Gruppo.

- **Gli articoli con badge `Allerta` o `Emergenza`.** Valgono nel momento esatto in cui escono:
  un'allerta pubblicata dal sistema a orario fisso, magari dodici ore dopo, è peggio di nessuna
  allerta. Si pubblicano a mano, quando servono.
- **Le versioni in italiano semplice.** Vivono accanto all'articolo completo, sul sito.
- **Gli articoli non ancora online.** Se un articolo è programmato per domani, la voce resta in
  coda e riparte al giro successivo, quando l'articolo è davvero leggibile.

C'è anche un limite di ritmo: **un solo post automatico al giorno**, e il sistema guarda indietro
solo di tre giorni. Se resta fermo per una settimana non recupera l'arretrato pubblicando sette
post di fila.

## 42.4 — I commenti su Instagram

Sui post automatici i **commenti sono disattivati**, subito dopo la pubblicazione.

La ragione è nella nostra stessa [social media policy](parte-13-social-media-policy-pubblica.md):
i canali sono presidiati dal lunedì al venerdì, indicativamente dalle 9 alle 18. Un post che esce
alle 18:30 di sabato e raccoglie commenti che nessuno legge fino a lunedì è un impegno che non
possiamo mantenere. Meglio non aprirlo.

Si possono riaprire, sul singolo post o per tutti. Su Facebook la stessa cosa si imposta dalle
impostazioni della Pagina, non dal sistema.

## 42.5 — Gli enti menzionati

In coda a ogni didascalia il sistema aggiunge le menzioni degli enti e, se non è già scritto nel
testo, il luogo **Genzano di Roma**.

| Ente | Instagram | Facebook |
|---|---|---|
| Dipartimento della Protezione Civile | `@dpcgov_official` | nome per esteso |
| Regione Lazio | `@regionelazio.official` | nome per esteso |
| Comune di Genzano di Roma | `@comunegenzanodiroma` | nome per esteso |
| Coordinamento Fe.p.i.vol. | `@fepiv_ol` | nome per esteso |

Due cose da sapere. Su **Facebook la chiocciola non crea un collegamento**: la Content Publishing
API non produce menzioni di Pagina, quindi gli enti si scrivono per esteso, che è onesto e
leggibile. E il **luogo cliccabile**, quello che compare sopra il post, richiede un identificativo
che si ottiene solo con un'app configurata con Facebook Login: finché non c'è, il luogo resta
scritto nella didascalia.

🔴 Un handle non si aggiunge mai per somiglianza col nome dell'ente. Quello del coordinamento era
`@fepiv_ol`, mentre esiste un profilo omonimo senza chiocciola che non ha nulla a che vedere con
lui. Taggare un estraneo da un account istituzionale è peggio che non taggare nessuno: vale la
regola del controllo di ogni entità citata
([rule 02](../.claude/rules/02-content-design-pa.md)).

## 42.6 — Fermare o spostare una pubblicazione

Tutto lo stato sta in un solo file, `coda-social.yaml`, nel repository privato. Si modifica anche
dal telefono, dall'interfaccia di GitHub.

```yaml
- slug: 2026-09-18-festa-del-pane-2026
  pubblica_il: '2026-09-21T08:30:00+02:00'   # ora italiana
  storia: true
  stato: in_coda                             # in_coda | pubblicato | errore | saltato
```

- Per **fermare** un post: porta `stato` a `saltato` prima dell'orario indicato.
- Per **spostarlo**: cambia `pubblica_il`.
- Per **anticiparlo**: metti un orario già passato, e uscirà al primo giro utile.

## 42.7 — Correggere un post già pubblicato

Qui le due piattaforme si comportano in modo molto diverso, e non è una scelta nostra.

| | Facebook | Instagram |
|---|---|---|
| Testo | si riscrive | non si tocca |
| Immagini | non si cambiano | non si cambiano |
| Eliminare il post | sì | solo a mano dall'app |
| Commenti | dalle impostazioni della Pagina | si aprono e si chiudono |

Verificato sul campo il 20 settembre 2026: una richiesta di riscrittura della didascalia Instagram
risponde che l'unico parametro accettato sono i commenti.

In pratica: **un testo sbagliato su Facebook si corregge**, su Instagram no. L'unica via è
cancellare il post dall'applicazione del telefono e rimetterlo in coda.

Lo strumento è `scripts/modifica-post.py` nel repository privato:

```bash
python3 scripts/modifica-post.py mostra <slug>
python3 scripts/modifica-post.py fb-testo <slug> --da-bozza
python3 scripts/modifica-post.py fb-elimina <slug> --conferma
python3 scripts/modifica-post.py ig-commenti <slug> --stato aperti
```

`--da-bozza` riprende il testo aggiornato da `facebook.txt`: correggi prima il materiale nel sito,
poi allinea il post.

**Le immagini invece si correggono solo prima.** Se aggiungi una foto a un articolo già
pubblicato, quella foto entrerà nei post successivi, non in quelli già usciti.

## 42.8 — Quando qualcosa si rompe

Il sistema apre una segnalazione nel repository privato e la chiude da solo quando rientra. Dopo
**tre tentativi falliti** una voce si ferma in stato `errore` invece di riprovare all'infinito.

| Segnalazione | Cosa fare |
|---|---|
| Token non valido | lancia il rinnovo; se fallisce, rigenera il token dal pannello Meta |
| Pubblicazione in errore | leggi il motivo, correggi il materiale nel sito, riporta la voce a `in_coda` |
| Rinnovo fallito | rilancia il workflow; controlla che il token GitHub non sia stato revocato |

Per provare senza pubblicare niente: **Actions → Pubblicazione automatica social → Run workflow**,
con `dry_run` a `true`. Mostra cosa uscirebbe, quante immagini e quanto è lunga la didascalia,
senza chiamare nessuna piattaforma.

## 42.9 — Tre difetti trovati solo pubblicando davvero

Vale la pena ricordarli, perché nessuno dei tre si vedeva in simulazione e tutti e tre davano lo
stesso messaggio d'errore fuorviante, `Only photo or video can be accepted as media type`.

1. **Le immagini erano JPEG progressive.** Instagram accetta solo baseline. Il generatore ora le
   salva così, con una nota nel codice perché non venga rimesso.
2. **Le variabili non impostate arrivano come stringa vuota.** In GitHub Actions una variabile non
   definita non è assente: vale `""`. Il valore predefinito non scattava mai.
3. **Le immagini venivano chieste al repository privato**, dove Instagram non può entrare. La
   variabile che indica il repository del sito è riservata da GitHub e non si può sovrascrivere:
   il tentativo spariva in silenzio.

Da lì la regola che resta: **il messaggio d'errore riporta l'indirizzo della prima immagine**. Un
guasto dello stesso tipo, la prossima volta, si legge al primo colpo.

## 42.10 — Documentazione collegata

- Regole operative e vincoli: [`.claude/rules/10-automazioni-github-actions.md`](../.claude/rules/10-automazioni-github-actions.md) § "Pubblicazione automatica social"
- Generazione delle bozze: [Parte 11](parte-11-testi-per-i-social-instagram-facebook-x-telegram.md) e [Parte 16](parte-16-bozze-social-gestione-quota-api.md)
- Regole di scrittura e accessibilità social: [Parte 13](parte-13-social-media-policy-pubblica.md)
- Credenziali, attivazione e diagnosi: README del repository `social-pc-genzano`
