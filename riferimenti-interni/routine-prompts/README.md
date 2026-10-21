# Testi delle routine di Claude — sito della Protezione Civile di Genzano di Roma

Copia di riferimento dei testi delle routine di Claude che lavorano su questo repository. La fonte operativa resta la routine (https://claude.ai/code/routines/<id>); questa cartella versiona il testo e serve a chi lavora al posto di Claude quando è ferma: ChatGPT esegue le routine di oggi da questi file (`AGENTS.md`, § «Quando Claude è fermo, lavori tu al suo posto»). Quando cambi il testo di una routine, cambi anche il suo file nello stesso lavoro.

Orari in ora italiana. Le routine di Claude con l'orario fissato in UTC si spostano di un'ora con il cambio dell'ora: qui sono scritti tutti e due.

| Routine | Quando | Testo | Già fatta oggi se… |
|---|---|---|---|
| Lavorazione autonoma issue automatiche (backlog a zero) (`trig_01EL97B5vF55j3JAWGiNiNCM`) | ogni giorno alle 14:00 italiane con l'ora legale, alle 13:00 con l'ora solare | [`lavorazione-issue-automatiche.md`](lavorazione-issue-automatiche.md) | issue automatiche chiuse o commentate oggi dall'account di Alessandro, PR unite oggi da questa routine |
| Rassegna normativa e albo pretorio → articolo (`trig_01TKRgVQ2spnYvCfNYkhAAQt`) | ogni giorno alle 07:52, alle 12:52 e alle 19:52 italiane | [`rassegna-normativa-albo.md`](rassegna-normativa-albo.md) | ogni giro ha il suo segno: un commento della rassegna su una issue `normativa-watcher` scritto dopo l'orario del giro (articoli pubblicati o motivi di scarto); se manca per l'ultimo giro passato, falla: un giro recupera anche quelli saltati prima, e gli atti già lavorati si riconoscono dalle issue |
| Cura schede didattiche scuole (`trig_01JvpACoLYuvaHH8VBvuCzaG`) | ogni lunedì alle 07:00 italiane con l'ora legale, alle 06:00 con l'ora solare | [`cura-schede-didattiche.md`](cura-schede-didattiche.md) | PR o commit di oggi su `static/formazione/schede-stampabili/` o sui kit per le scuole |
| Cura kit calamità categorie vulnerabili (`trig_013VgcKgHzKYkUrJeeDP7EX5`) | ogni martedì alle 07:00 italiane con l'ora legale, alle 06:00 con l'ora solare | [`cura-kit-calamita.md`](cura-kit-calamita.md) | PR o commit di oggi su `content/formazione/kit-calamita*` o sulle schede dei kit |
| Lettura sintattica articoli in uscita (gate linguistico settimanale) (`trig_015yjxdHQ1nxq246YjDRm98N`) | ogni mercoledì alle 06:37 italiane con l'ora legale, alle 05:37 con l'ora solare | [`lettura-sintattica.md`](lettura-sintattica.md) | PR o commit di oggi sugli articoli calendarizzati in `content/comunicazioni/` |
| Audit interno completo del sito (mensile) (`trig_01RMQwDs5Ku2mRfkwkDZnKmx`) | il 3 di ogni mese alle 06:00 italiane con l'ora legale, alle 05:00 con l'ora solare | [`audit-interno-mensile.md`](audit-interno-mensile.md) | rapporto di oggi in `riferimenti-interni/audit-interni/AAAA-MM-GG-audit-interno.md` |

Elenco di tutte le routine di Alessandro, anche degli altri repository, e che cosa vuol dire «fai le routine di oggi»: `ROUTINE.md` del repository `assistente-personale`.
