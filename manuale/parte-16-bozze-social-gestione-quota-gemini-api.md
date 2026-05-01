_[Indice manuale](README.md)_

# Parte 16 — Bozze social: gestione quota Gemini API

Lo script `genera-social.py` usa il **tier gratuito Gemini 2.5 Flash** che ha limiti:
- **15 richieste/minuto** (RPM): rate limit transitorio
- **~50 richieste/giorno** (RPD): hard limit, dopo restituisce HTTP 429 finché non
  si resetta a mezzanotte UTC

**Conseguenze pratiche:**
- Una rigenerazione massiva su 372 articoli **non sta in un solo lancio**: si fermerà
  dopo ~50 articoli.
- Sui prossimi articoli pubblicati il workflow CI `genera-social-bozze.yml` continua
  a funzionare correttamente (1 articolo per push = ben sotto il limite).

**Strategia di rigenerazione massiva** (quando serve):
1. Lancia `bash scripts/genera-social.sh --all` la prima volta — produrrà ~50 bozze
   prima del 429.
2. Il giorno successivo (dopo mezzanotte UTC), rilancia lo stesso comando: lo script
   è idempotente, salta automaticamente le bozze già esistenti e processa le rimanenti.
3. Continua per ~7-8 giorni fino a coprire tutti i 372 articoli, oppure lascia che il
   workflow CI le generi naturalmente sui nuovi push.

**In alternativa**: passare al tier a pagamento (~€0.10/1M token = pochi euro per
372 bozze) e fare in un colpo solo. Decisione editoriale, non tecnica.

**Le immagini Instagram** generate via Pillow (`genera-immagini-social.py`) **non hanno
rate limit** e si rigenerano in pochi minuti per tutti i 372 articoli. Indipendenti
dalla quota Gemini.

---

_[Indice manuale](README.md)_

[← Parte 15 — Homepage enhancements v1.0 (aprile 2026)](parte-15-homepage-enhancements-v1-0-aprile-2026.md) · [↑ Indice](README.md) · [Parte 17 — Coach didattico nei giochi e TTS esteso (maggio 2026) →](parte-17-coach-didattico-nei-giochi-e-tts-esteso-maggio-2026.md)
