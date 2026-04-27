# Riferimenti Interni — Documentazione di Lavoro

Questa cartella contiene **documentazione di lavoro** per chi gestisce il sito e i contenuti del Gruppo Comunale Volontari di Protezione Civile di Genzano di Roma. **Non viene deployata** sul sito pubblico (Hugo costruisce solo da `content/`, `static/`, `themes/`, `data/`, `assets/`, `layouts/`).

## Perché esiste

Alcuni standard tecnici e linee guida che adottiamo (ISO 22329:2021, CWA CEN/CENELEC) sono coperti da copyright o sono in fase di consultazione: **non possiamo redistribuirli pubblicamente** sul sito istituzionale, ma il Gruppo deve poterli **consultare** durante la redazione e l'aggiornamento dei contenuti.

Questa cartella è il punto di archivio per:

- documenti tecnici a pagamento di cui il Gruppo ha copia legittima;
- bozze in fase di consultazione pubblica che potrebbero non restare scaricabili;
- materiale di lavoro non destinato alla pubblicazione (verbali interni, note di redazione, riferimenti normativi).

## Convenzione

- **Tutto quello che è in questa cartella resta nel repo git** (sincronizzato fra i maintainer e con AI di supporto come Claude Code).
- **Niente di questa cartella finisce sul sito pubblico**. Hugo non la legge perché non rientra nelle sue cartelle native.
- **Niente link diretti dal sito pubblico** (`content/`, `static/`, `themes/`) verso file qui dentro.

## Materiali pubblici equivalenti

Per ogni documento copyrighted qui dentro, indichiamo dove trovare la versione liberamente accessibile (se esiste) o come acquistarla:

| Documento interno | Versione pubblica | Note |
|---|---|---|
| `comunicazione-emergenze/iso-22329-2021-social-media-emergencies.pdf` | [Anteprima ISO](https://www.iso.org/standard/50064.html) (solo scope + indice) | Norma a pagamento (~CHF 88). In Italia tramite UNI. |
| `comunicazione-emergenze/cwa-cen-cenelec-draft-social-media-messages.pdf` | [CEN-CENELEC Workshop Agreements](https://www.cencenelec.eu/european-standardization/cen-cenelec-workshop-agreements/) | Documento in fase di *open for comments*. Disponibile solo durante la consultazione. |

I contenuti operativi di queste due fonti sono già **recepiti e tradotti** nel `MANUALE-SITO.md` Parte 13.7 (struttura messaggi allerta, hashtag, accessibilità post). Il volontario o redattore non ha bisogno di consultare gli originali per il lavoro quotidiano.

## Contenuto attuale

### `comunicazione-emergenze/`

Fonti su comunicazione di crisi e uso dei social media in emergenza. Recepite in MANUALE-SITO.md Parte 13.7 e nelle regole `02-content-design-pa.md`, `03-accessibility.md`, `06-protezione-civile-scientifica.md`.

- **`iso-22329-2021-social-media-emergencies.pdf`** (382 KB)
  *Security and resilience — Emergency management — Guidelines for the use of social media in emergencies*. ISO 2021. © ISO, copyright protected. Detenuto in copia legittima dal Gruppo.
- **`cwa-cen-cenelec-draft-social-media-messages.pdf`** (1.0 MB)
  *Guidelines for effective social media messages in crisis and emergency situations*. CEN/CENELEC Workshop Agreement, draft *open for comments*.

## Documenti pubblici (NON in questa cartella)

I documenti rilasciati con licenza pubblica o di pubblico dominio stanno in `static/manuali/` e sono linkati pubblicamente dal sito:

- `static/manuali/cna-best-practices-social-media-crisis-2023.pdf` — CNA white paper, *Approved for public release. Unlimited distribution.*
- `static/manuali/fema-saver-innovative-uses-social-media-emergency-management.pdf` — FEMA SAVER program, U.S. Department of Homeland Security, *approved for public release; distribution is unlimited.*

## Aggiungere un nuovo documento

1. Verifica la licenza: pubblico dominio / Creative Commons / approved for public release → `static/manuali/`. Copyrighted, a pagamento, draft di consultazione → `riferimenti-interni/<categoria>/`.
2. Aggiorna la tabella sopra con il documento e il link alla versione pubblica equivalente (se esiste).
3. Aggiorna `MANUALE-SITO.md` (Parte 13.9 o sezione tematica pertinente) con il riferimento.
4. Se è pubblico, aggiungilo anche a `content/siti-utili/_index.md` con etichetta di accessibilità (🟢 gratuito / 💶 a pagamento / 🔒 membership).
