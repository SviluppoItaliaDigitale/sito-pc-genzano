# Motion graphic — sorgenti dei video divulgativi

Cartella di lavoro dei video fatti in codice. **Non viene deployata** (Hugo non la legge): sul sito vanno solo le versioni web copiate in `static/video/`.

| Cartella | Contenuto | Nel repo |
|---|---|---|
| `src/<nome>.src.html` | sorgente della puntata (segnaposto `/*FONTS*/`, `/*DUR*/[]`, `/*AUDIO*/`) | sì |
| `voce/<nome>/testi.txt` | frasi della voce, una per scena | sì |
| `voce/<nome>/voce.mp3` | traccia voce già pronta (es. registrazione) | sì |
| `voce/<nome>/durate.json` | durate delle frasi generate da Piper | sì |
| `out/<nome>/` | MP4 master e web, poster, provini, verifiche | no |
| `dist/<nome>.html` | pagina autonoma con font e audio incorporati | no |

Istruzioni complete: `.claude/skills/motion-graphic/SKILL.md`.

Puntate: `allerta-meteo-colori`, `allerta-cosa-fare`, `kit-emergenza` (con voce) — 23/09/2026, solo 9:16.
