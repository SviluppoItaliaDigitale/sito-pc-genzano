_[Indice manuale](README.md)_

# Parte 5 — Checklist pre-pubblicazione

### Checklist articolo

**Frontmatter:**

- [ ] `title` presente, chiaro, max ~80 caratteri
- [ ] `date` in formato `AAAA-MM-GG` senza virgolette e senza timezone
- [ ] `description` sotto i 160 caratteri
- [ ] `badge` uno dei valori dalla tabella o nuovo (riceverà colore automatico)
- [ ] `priorita` solo `"normale"` o `"urgente"`
- [ ] `autore` presente
- [ ] `image` o stringa vuota `""`
- [ ] `scadenza` compilata solo se serve, altrimenti `""`
- [ ] `area` compilata se rilevante
- [ ] `allegati` con titolo completo (tipo + dimensione) e URL corretto
- [ ] `draft: false` per pubblicare

**Testo:**

- [ ] Titolo descrittivo, non enfatico
- [ ] Apertura con il fatto principale in grassetto
- [ ] Gerarchia H2/H3 coerente (no salti H2→H4)
- [ ] Frasi sotto le 20 parole in media
- [ ] Voce attiva, pochi passivi
- [ ] Nessuna nominalizzazione evitabile
- [ ] Parole comuni, no burocratese
- [ ] Elenchi puntati per 3+ elementi paralleli
- [ ] Grassetto solo per parole chiave
- [ ] Link con testo descrittivo
- [ ] Numeri di telefono nel formato leggibile (06 9362 600)
- [ ] Date estese nel testo ("15 maggio 2026")
- [ ] Ortografia e grammatica verificate
- [ ] Accenti e apostrofi corretti

**Contenuto:**

- [ ] Fonti citate per dati meteo, allerte, rischi
- [ ] Numeri di emergenza verificati: nel Lazio solo **112** (NUE) per il cittadino, più 803 555 e 1530
- [ ] Nessuna informazione non verificata
- [ ] Linguaggio inclusivo

**Immagine:**

- [ ] Formato WebP, 1200 px, <200 KB
- [ ] Fascia blu con logo e testo istituzionale
- [ ] Nome file `AAAA-MM-GG-descrizione.webp`
- [ ] In `static/images/`
- [ ] Diritti d'uso verificati
- [ ] Alt text significativo

**Tecnica:**

- [ ] Nome file `AAAA-MM-GG-titolo-breve.md` in `content/comunicazioni/`
- [ ] `hugo server -D` non mostra errori
- [ ] Articolo visibile in home e in `/comunicazioni/`
- [ ] Link interni funzionano
- [ ] Mobile-friendly (testa la preview su schermo stretto)

### Checklist pagina

**Frontmatter:**

- [ ] `title` presente e chiaro
- [ ] `description` sotto i 160 caratteri
- [ ] `aliases` se la pagina sostituisce un URL storico
- [ ] `draft: false`

**Testo:** (come per articolo)

**Tecnica:**

- [ ] File in `content/<sezione>/` (`_index.md` per hub, `<slug>.md` per sotto-pagine)
- [ ] Se va nel menu: voce aggiunta in `hugo.toml` con peso corretto
- [ ] URL accessibile in locale (`hugo server`)

### Checklist immagine

Vedi Parte 3.12.

---

_[Indice manuale](README.md)_

[← Parte 04 — Scrivere una pagina (diverso da articolo)](parte-04-scrivere-una-pagina-diverso-da-articolo.md) · [↑ Indice](README.md) · [Parte 06 — Procedura di aggiornamento manuale →](parte-06-procedura-di-aggiornamento-manuale.md)
