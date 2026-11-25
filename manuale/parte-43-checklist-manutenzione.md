# Parte 43 — Checklist di manutenzione del sito (per un secondo referente)

*Aggiunta il 19/11/2026. Serve a chi affianca o sostituisce il referente del sito: dice che cosa controllare, quando e dove, senza dover conoscere tutto il progetto. Ogni voce rimanda alla parte del manuale o alla regola che la spiega per intero.*

## 43.1 Ogni giorno (5 minuti)

| Controllo | Dove | Che cosa fare se non va |
|---|---|---|
| La barra di allerta in homepage dice livello, rischi e validità del bollettino del giorno | homepage del sito e bollettino del Centro Funzionale Regionale | Si ripara il dato in `data/allerta.json` (livello, titolo e descrizione insieme: Parte 09 § 9.3). Arancione o rossa: avvisare il referente. |
| La pubblicazione dell'ultima modifica è andata a buon fine | GitHub → Actions → «Build e Deploy» | Un run rosso si rilancia una volta; se resta rosso si apre il log e si guarda il primo errore. |
| Nessuna issue «urgente» aperta da più di un giorno | GitHub → Issues, etichetta `urgente` | Si legge la issue: dice da sola che cosa non va e come si ripara. |

## 43.2 Ogni settimana (30 minuti, di lunedì)

- **Issue automatiche del lunedì**: link rotti, refusi, incongruenze fra i testi, freschezza, glossario, versione facile. La routine giornaliera ne lavora la maggior parte; si controlla che non ne restino aperte da più di una settimana (Parte 10).
- **Articoli programmati della settimana**: si aprono uno per uno quelli in uscita nei prossimi sette giorni e si controlla che la data annunciata nel titolo coincida con il giorno di uscita (`scripts/check-data-uscita.py`).
- **Notizie del territorio in evidenza**: in `/comunicazioni/` il riquadro «Da Genzano e dai Castelli Romani» deve mostrare le notizie locali degli ultimi 30 giorni. Se una notizia locale manca, il suo articolo ha il canale sbagliato (sotto, § 43.4).
- **Social**: la issue «Salute del sistema» elenca gli articoli rimasti senza post.

## 43.3 Ogni mese

- **Audit interno** del 3 del mese: si legge il rapporto in `riferimenti-interni/audit-interni/` e si controllano le PR rimaste aperte (Categoria B).
- **Export del gestionale degli interventi**: se la issue di promemoria è aperta, si scarica l'export e si aggiornano gli open data (cumulativo o parziale: Parte 10, § «Open data interventi»).
- **Pagina Stato del sistema** (`/stato-sistema/`): la data «aggiornato» deve essere di oggi.

## 43.4 Quando si scrive o si corregge un articolo

1. Frontmatter completo dall'archetipo `archetypes/comunicazioni.md`, compreso il **canale**:
   - `territorio` per ciò che accade a Genzano e nei Castelli Romani (interventi e vita del Gruppo, atti del Comune, lavori, eventi in città);
   - `italia` per le notizie di protezione civile nazionali e regionali (decreti, stati di emergenza, notizie della Regione);
   - `approfondimenti` per storia, anniversari, scienza e prevenzione.
   Il canale si sceglie leggendo l'articolo, non dal badge. Lo controlla `scripts/check-canale-articoli.py`, che blocca la PR se manca.
2. Copertina tipografica generata prima del commit (`scripts/genera-cover.py`), foto solo nel corpo.
3. Controlli prima del commit: refusi (`scripts/check-refusi.py`), dati già pubblicati (`scripts/cerca-incongruenze.py --da-git origin/main`), date e scarto orario.
4. Pubblicazione: ramo di lavoro → PR → controlli verdi → unione → verifica che il deploy finisca. Mai modifiche dirette su `main`.

## 43.5 Che cosa non si fa mai da soli

- Non si cambia il livello di allerta senza il bollettino ufficiale sotto gli occhi.
- Non si pubblicano a mano post con badge `Allerta` o `Emergenza` senza averne parlato col referente.
- Non si tocca `data/emergenza.json` (modalità emergenza) se non per un'emergenza vera dichiarata dalle autorità.
- Non si eliminano immagini, documenti o allegati dal sito.

## 43.6 Dove sono le cose

| Cerchi | Dove |
|---|---|
| Regole complete | `CLAUDE.md` e `.claude/rules/` |
| Bacheca dei lavori in corso fra le sessioni | `COORDINAMENTO.md` |
| Indice di questo manuale | `MANUALE-SITO.md` |
| Automazioni e orari | Parte 10 e `.claude/rules/10-automazioni-github-actions.md` |
