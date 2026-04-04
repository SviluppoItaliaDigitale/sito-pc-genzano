# GUIDA — Come caricare il sito evoluto v2.0
# Protezione Civile Genzano di Roma
# Data: Aprile 2026

## PREREQUISITI

Assicurati di avere:
- Il file `sito-pc-genzano-evoluto.zip` scaricato
- Hugo installato sul PC (`hugo version` per verificare)
- Git configurato e funzionante
- Accesso al repository GitHub


## PASSO 1 — Backup del sito attuale

Prima di tutto, fai una copia di sicurezza:

```bash
cd ~
cp -r sito-pc-genzano sito-pc-genzano-BACKUP-$(date +%Y%m%d)
```

Questo crea una cartella tipo `sito-pc-genzano-BACKUP-20260404` con tutto il sito attuale.


## PASSO 2 — Copia lo ZIP nella home

Copia il file ZIP scaricato nella tua home directory.
Se lo hai scaricato nella cartella Download:

```bash
cp ~/Scaricati/sito-pc-genzano-evoluto.zip ~/
```

(oppure `cp ~/Downloads/sito-pc-genzano-evoluto.zip ~/` se il sistema è in inglese)


## PASSO 3 — Estrai lo ZIP sovrascrivendo i file

```bash
cd ~/sito-pc-genzano
unzip -o ~/sito-pc-genzano-evoluto.zip
```

Il flag `-o` sovrascrive i file esistenti senza chiedere conferma.
I file nuovi vengono aggiunti, quelli esistenti vengono aggiornati.

IMPORTANTE: lo ZIP NON cancella file che esistono già nel repo ma non
sono nello ZIP (es. immagini che hai aggiunto tu). È sicuro.


## PASSO 4 — Copia lo script di gestione

Lo script `gestione-sito.sh` è dentro lo ZIP ma nella cartella del sito.
Copialo nella home:

```bash
cp ~/sito-pc-genzano/gestione-sito.sh ~/gestione-sito.sh
chmod +x ~/gestione-sito.sh
```


## PASSO 5 — Test locale

Verifica che tutto funzioni:

```bash
cd ~/sito-pc-genzano
hugo server
```

Apri il browser su http://localhost:1313/ e verifica:

- [ ] Homepage si carica correttamente
- [ ] Menu principale funziona (7 voci)
- [ ] Barra allerta meteo visibile
- [ ] Barra numeri emergenza visibile (rossa)
- [ ] Link "Area Volontari" visibile nello slim header in alto
- [ ] Data e ora visibili sopra il footer
- [ ] Ultimo aggiornamento sito visibile sopra il footer
- [ ] Sezione "Cosa fare in caso di..." con 4 card
- [ ] Sezione "Servizi per il cittadino" con 4 card
- [ ] Sezione notizie in evidenza
- [ ] Footer con 3 colonne (contatti, servizi, link utili)
- [ ] Pagina Rischi e Prevenzione mostra 9 card
- [ ] Pagina Allerte Meteo ampliata con spiegazione codici
- [ ] Pagina Cosa Fare Adesso raggiungibile
- [ ] Pagina FAQ raggiungibile
- [ ] Pagina Numeri Utili raggiungibile
- [ ] Pagina Formazione raggiungibile
- [ ] Piano Familiare con form ampliato
- [ ] Area Download con tabelle

Premi Ctrl+C per fermare il server locale.


## PASSO 6 — Test modalità emergenza (opzionale)

Per verificare che la modalità emergenza funzioni:

```bash
cd ~/sito-pc-genzano
nano data/emergenza.json
```

Cambia `"attiva": false` in `"attiva": true` e aggiungi un titolo:

```json
{
  "attiva": true,
  "tipo": "arancione",
  "titolo": "TEST EMERGENZA",
  "descrizione": "Questo è un test della modalità emergenza.",
  "link": "",
  "ultimo_aggiornamento": ""
}
```

Rilancia `hugo server` e verifica che la homepage si riorganizzi.
Poi rimetti `"attiva": false` prima di pubblicare!


## PASSO 7 — Pubblica online

Quando tutto è verificato:

```bash
cd ~/sito-pc-genzano
git add .
git status
```

Controlla che i file modificati/aggiunti siano quelli attesi.
Poi:

```bash
git commit -m "Evoluzione sito v2.0 — hub rischi, doppia modalità, nuove sezioni, utility bar"
git push
```

GitHub Actions farà automaticamente:
1. Build Hugo con baseURL Aruba → deploy FTP su Aruba
2. Rebuild Hugo con baseURL GitHub Pages → deploy GitHub Pages

Puoi monitorare il deploy su:
https://github.com/SviluppoItaliaDigitale/sito-pc-genzano/actions


## PASSO 8 — Verifica in produzione

Dopo 2-3 minuti dal push, verifica su entrambi i siti:

- https://www.protezionecivilegenzano.it/
- https://sviluppoitaliadigitale.github.io/sito-pc-genzano/

Controlla le stesse cose del Passo 5.


## RIEPILOGO COMANDI RAPIDI

```bash
# Backup
cp -r ~/sito-pc-genzano ~/sito-pc-genzano-BACKUP-$(date +%Y%m%d)

# Estrai aggiornamento
cd ~/sito-pc-genzano && unzip -o ~/sito-pc-genzano-evoluto.zip

# Copia script gestione
cp ~/sito-pc-genzano/gestione-sito.sh ~/gestione-sito.sh && chmod +x ~/gestione-sito.sh

# Test locale
cd ~/sito-pc-genzano && hugo server

# Pubblica
cd ~/sito-pc-genzano && git add . && git commit -m "Aggiornamento" && git push

# Menu gestione
bash ~/gestione-sito.sh
```


## IN CASO DI PROBLEMI

Se qualcosa va storto dopo il push:

```bash
# Ripristina dal backup
cd ~
rm -rf sito-pc-genzano
cp -r sito-pc-genzano-BACKUP-XXXXXXXX sito-pc-genzano
cd sito-pc-genzano
git checkout .
git push --force
```

Oppure, per annullare solo l'ultimo commit:

```bash
cd ~/sito-pc-genzano
git revert HEAD
git push
```


## CONTATTI

Per assistenza tecnica sul sito: chiedi a Claude con l'handover del progetto.
Il file HANDOVER-PROGETTO-PC-GENZANO.md contiene tutta la documentazione.
