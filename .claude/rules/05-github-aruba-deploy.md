# GitHub + Aruba — Deploy e Infrastruttura

## Ambienti di pubblicazione

Il sito viene pubblicato su due ambienti distinti ad ogni push su `main`:

| Ambiente | URL | Metodo |
|---|---|---|
| Aruba (produzione) | https://www.protezionecivilegenzano.it/ | FTP via GitHub Actions |
| GitHub Pages (preview) | https://sviluppoitaliadigitale.github.io/sito-pc-genzano/ | GitHub Pages API |

## Workflow CI/CD

Il file `.github/workflows/deploy.yml` gestisce il deploy automatico:
1. Esegue `hugo --minify --baseURL "https://www.protezionecivilegenzano.it/"` per Aruba
2. Esegue `hugo --minify` per GitHub Pages
3. Carica su Aruba via FTP usando i secret GitHub: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`
4. Pubblica su GitHub Pages tramite l'azione ufficiale

## Regole operative

- Il branch `main` è il branch di produzione: ogni push avvia il deploy.
- I secret FTP non vanno mai committati nel repository.
- Monitora i deploy nella tab Actions del repository GitHub.
- In caso di build rotta, il deploy non avviene: il sito rimane all'ultima versione funzionante.

## Regole di compatibilità

Ogni modifica deve essere compatibile con:
- Build statica di Hugo (nessun server-side rendering, nessuna API runtime)
- Deploy FTP su Aruba (percorsi degli asset devono essere corretti per entrambi i baseURL)
- GitHub Pages con subpath `/sito-pc-genzano/` (usa `{{ absURL }}` o `{{ relURL }}` nei template, mai percorsi assoluti hardcoded)
- Certificato HTTPS esistente su Aruba (non modificare la configurazione DNS senza coordinamento)

## Rollback

Per tornare a una versione precedente:
```bash
git revert HEAD          # Crea un commit di ripristino (preferibile)
git push origin main     # Avvia il redeploy
```
Evita `git reset --hard` su `main` se il commit è già stato pushato.

## Verifica prima del push

Prima di fare push su `main`, verifica sempre:
- `hugo server` non mostra errori in console
- Il build `hugo --minify` completa senza errori
- I percorsi di immagini, PDF e asset statici sono corretti
- Il frontmatter degli articoli usa il formato data `AAAA-MM-GG`
- Nessun articolo con `draft: false` ha contenuti incompleti

## Divieti

- Non fare push su `main` con un build rotto.
- Non committare credenziali, token o secret nel repository.
- Non modificare il workflow CI/CD senza verificare la compatibilità con entrambi gli ambienti.
- Non introdurre asset con percorsi hardcoded che funzionino solo su un ambiente.
- Non eliminare o rinominare file già pubblicati senza gestire i redirect appropriati (Aruba non ha redirect automatici).
