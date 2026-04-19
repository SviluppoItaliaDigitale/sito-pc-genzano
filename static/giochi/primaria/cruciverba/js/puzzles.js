/* Cruciverba della Sicurezza — Raccolta schemi
   Ogni schema specifica una griglia (rows × cols) e un elenco di parole con
   posizione (row, col), direzione (A = across, D = down) e definizione.
   Le lettere in cui due parole si incrociano devono coincidere. */

window.CRUCIVERBA_PUZZLES = {

  // ═══════════════════════════════════════════════════════════════
  // FACILE — schemi "a pettine" con una parola principale e 8–10 rami
  // ═══════════════════════════════════════════════════════════════
  facile: [

    // ── Schema F1 ─────────────────────────────────────────────
    {
      id: 'facile-1',
      rows: 10,
      cols: 5,
      title: 'Schema "Protezione civile"',
      words: [
        { n: 1,  dir: 'A', row: 0, col: 0, answer: 'PAURA', clue: 'Emozione che si prova davanti a un pericolo' },
        { n: 1,  dir: 'D', row: 0, col: 0, answer: 'PROTEZIONE', clue: 'Si abbina a "civile" nel nome del nostro gruppo' },
        { n: 2,  dir: 'A', row: 1, col: 0, answer: 'RADIO', clue: 'Strumento dei volontari per comunicare a distanza' },
        { n: 3,  dir: 'A', row: 2, col: 0, answer: 'ORSO', clue: 'Grosso animale dei boschi' },
        { n: 4,  dir: 'A', row: 3, col: 0, answer: 'TORRE', clue: 'Alta struttura spesso con la campana' },
        { n: 5,  dir: 'A', row: 4, col: 0, answer: 'ESCA', clue: 'Attira pesci e animali' },
        { n: 6,  dir: 'A', row: 5, col: 0, answer: 'ZAINO', clue: 'Contiene ciò che serve in emergenza' },
        { n: 7,  dir: 'A', row: 6, col: 0, answer: 'IDEA', clue: 'Pensiero che nasce nella mente' },
        { n: 8,  dir: 'A', row: 7, col: 0, answer: 'ONDA', clue: 'Si alza sul mare' },
        { n: 9,  dir: 'A', row: 8, col: 0, answer: 'NEVE', clue: 'Cade dal cielo d\'inverno' },
        { n: 10, dir: 'A', row: 9, col: 0, answer: 'ELMO', clue: 'Casco antico, anche dei soldati' }
      ]
    },

    // ── Schema F2 ─────────────────────────────────────────────
    {
      id: 'facile-2',
      rows: 9,
      cols: 5,
      title: 'Schema "Volontari"',
      words: [
        { n: 1, dir: 'A', row: 0, col: 0, answer: 'VENTO', clue: 'Si sente soffiare tra gli alberi' },
        { n: 1, dir: 'D', row: 0, col: 0, answer: 'VOLONTARI', clue: 'Offrono il loro tempo per aiutare senza essere pagati' },
        { n: 2, dir: 'A', row: 1, col: 0, answer: 'ORSO', clue: 'Dorme nella tana durante l\'inverno' },
        { n: 3, dir: 'A', row: 2, col: 0, answer: 'LUCE', clue: 'Illumina al buio' },
        { n: 4, dir: 'A', row: 3, col: 0, answer: 'OASI', clue: 'Area di ristoro nel deserto' },
        { n: 5, dir: 'A', row: 4, col: 0, answer: 'NEVE', clue: 'Candida e fredda, copre i monti' },
        { n: 6, dir: 'A', row: 5, col: 0, answer: 'TORRE', clue: 'Alta costruzione di guardia' },
        { n: 7, dir: 'A', row: 6, col: 0, answer: 'AIUTO', clue: 'Lo chiedi in caso di bisogno' },
        { n: 8, dir: 'A', row: 7, col: 0, answer: 'RADIO', clue: 'Comunica a distanza via onde' },
        { n: 9, dir: 'A', row: 8, col: 0, answer: 'IDEA', clue: 'Pensiero geniale che ti viene in mente' }
      ]
    }

  ],

  // ═══════════════════════════════════════════════════════════════
  // MEDIO — parola principale orizzontale e verticali che scendono
  // ═══════════════════════════════════════════════════════════════
  medio: [

    // ── Schema M1 ─────────────────────────────────────────────
    {
      id: 'medio-1',
      rows: 7,
      cols: 11,
      title: 'Schema "Prevenzione"',
      words: [
        { n: 1,  dir: 'A', row: 0, col: 0, answer: 'PREVENZIONE', clue: 'Insieme di azioni per evitare che un pericolo si verifichi' },
        { n: 1,  dir: 'D', row: 0, col: 0, answer: 'PAURA', clue: 'Reazione di allarme davanti al pericolo' },
        { n: 2,  dir: 'D', row: 0, col: 1, answer: 'RADIO', clue: 'Trasmette segnali tra le squadre di soccorso' },
        { n: 3,  dir: 'D', row: 0, col: 2, answer: 'ERBA', clue: 'Cresce nei prati e nei boschi' },
        { n: 4,  dir: 'D', row: 0, col: 3, answer: 'VENTO', clue: 'Può alimentare gli incendi se è forte' },
        { n: 5,  dir: 'D', row: 0, col: 4, answer: 'ELMO', clue: 'Protegge il capo, sinonimo di casco' },
        { n: 6,  dir: 'D', row: 0, col: 5, answer: 'NEVE', clue: 'Fiocchi bianchi che cadono dal cielo' },
        { n: 7,  dir: 'D', row: 0, col: 6, answer: 'ZAINO', clue: 'Lo prepari con acqua, torcia e documenti' },
        { n: 8,  dir: 'D', row: 0, col: 7, answer: 'IDEA', clue: 'Soluzione che ti viene in mente' },
        { n: 9,  dir: 'D', row: 0, col: 8, answer: 'ORSO', clue: 'Animale che vive nei boschi' },
        { n: 10, dir: 'D', row: 0, col: 9, answer: 'NUMERI', clue: 'Quelli di emergenza: 112, 115, 118...' },
        { n: 11, dir: 'D', row: 0, col: 10, answer: 'ESCA', clue: 'Attrae gli animali o accende il fuoco' }
      ]
    },

    // ── Schema M2 ─────────────────────────────────────────────
    {
      id: 'medio-2',
      rows: 7,
      cols: 9,
      title: 'Schema "Emergenza"',
      words: [
        { n: 1, dir: 'A', row: 0, col: 0, answer: 'EMERGENZA', clue: 'Situazione urgente che richiede interventi immediati' },
        { n: 1, dir: 'D', row: 0, col: 0, answer: 'ERBA', clue: 'Copre prati e campi' },
        { n: 2, dir: 'D', row: 0, col: 1, answer: 'MARE', clue: 'Grande distesa d\'acqua salata' },
        { n: 3, dir: 'D', row: 0, col: 2, answer: 'ESCA', clue: 'Usata dal pescatore per attirare i pesci' },
        { n: 4, dir: 'D', row: 0, col: 3, answer: 'RADIO', clue: 'Usata dai volontari per comunicare' },
        { n: 5, dir: 'D', row: 0, col: 4, answer: 'GIOCO', clue: 'Divertimento dei bambini, anche educativo' },
        { n: 6, dir: 'D', row: 0, col: 5, answer: 'ELMO', clue: 'Copricapo di protezione per la testa' },
        { n: 7, dir: 'D', row: 0, col: 6, answer: 'NEVE', clue: 'Copre i monti d\'inverno' },
        { n: 8, dir: 'D', row: 0, col: 7, answer: 'ZAINO', clue: 'Lo prepari per l\'emergenza' },
        { n: 9, dir: 'D', row: 0, col: 8, answer: 'AIUTO', clue: 'Richiesta di soccorso' }
      ]
    }

  ],

  // ═══════════════════════════════════════════════════════════════
  // DIFFICILE — parole più lunghe e schemi più ricchi
  // ═══════════════════════════════════════════════════════════════
  difficile: [

    // ── Schema D1 ─────────────────────────────────────────────
    {
      id: 'difficile-1',
      rows: 12,
      cols: 9,
      title: 'Schema "Volontariato"',
      words: [
        { n: 1,  dir: 'D', row: 0, col: 0, answer: 'VOLONTARIATO', clue: 'Attività di chi aiuta gratuitamente gli altri' },
        { n: 1,  dir: 'A', row: 0, col: 0, answer: 'VIGILE', clue: 'Agente che regola il traffico (del fuoco o urbano)' },
        { n: 2,  dir: 'A', row: 1, col: 0, answer: 'OMBRELLO', clue: 'Protegge dalla pioggia' },
        { n: 3,  dir: 'A', row: 2, col: 0, answer: 'LAVORO', clue: 'Attività che fai ogni giorno' },
        { n: 4,  dir: 'A', row: 3, col: 0, answer: 'OCEANO', clue: 'Grandissima distesa d\'acqua salata' },
        { n: 5,  dir: 'A', row: 4, col: 0, answer: 'NUMERI', clue: 'Quelli di emergenza sono pochi ma essenziali' },
        { n: 6,  dir: 'A', row: 5, col: 0, answer: 'TORCIA', clue: 'Fa luce al buio, sempre nello zaino' },
        { n: 7,  dir: 'A', row: 6, col: 0, answer: 'ALLERTA', clue: 'Avviso che un pericolo potrebbe arrivare' },
        { n: 8,  dir: 'A', row: 7, col: 0, answer: 'RADIO', clue: 'Trasmette voci e messaggi via onde' },
        { n: 9,  dir: 'A', row: 8, col: 0, answer: 'IDRANTE', clue: 'Da qui i pompieri prendono l\'acqua' },
        { n: 10, dir: 'A', row: 9, col: 0, answer: 'AIUTO', clue: 'Lo chiedi in caso di emergenza' },
        { n: 11, dir: 'A', row: 10, col: 0, answer: 'TERREMOTO', clue: 'Movimento improvviso del suolo' },
        { n: 12, dir: 'A', row: 11, col: 0, answer: 'ORSO', clue: 'Animale selvatico dei boschi' }
      ]
    },

    // ── Schema D2 ─────────────────────────────────────────────
    {
      id: 'difficile-2',
      rows: 9,
      cols: 9,
      title: 'Schema "Sicurezza"',
      words: [
        { n: 1, dir: 'A', row: 0, col: 0, answer: 'SICUREZZA', clue: 'Sensazione e condizione di chi non corre pericoli' },
        { n: 1, dir: 'D', row: 0, col: 0, answer: 'SCOSSA', clue: 'Movimento del terremoto' },
        { n: 2, dir: 'D', row: 0, col: 1, answer: 'INCENDIO', clue: 'Fuoco che brucia fuori controllo' },
        { n: 3, dir: 'D', row: 0, col: 2, answer: 'CASCO', clue: 'Protegge la testa del volontario' },
        { n: 4, dir: 'D', row: 0, col: 3, answer: 'UGOLA', clue: 'Si trova in fondo alla gola' },
        { n: 5, dir: 'D', row: 0, col: 4, answer: 'RADIO', clue: 'Comunica fra le squadre di soccorso' },
        { n: 6, dir: 'D', row: 0, col: 5, answer: 'ERBA', clue: 'Verde e bassa, copre i prati' },
        { n: 7, dir: 'D', row: 0, col: 6, answer: 'ZAINO', clue: 'Contiene tutto il necessario per l\'emergenza' },
        { n: 8, dir: 'D', row: 0, col: 7, answer: 'ZOLLA', clue: 'Pezzo di terra o terreno' },
        { n: 9, dir: 'D', row: 0, col: 8, answer: 'ALLERTA', clue: 'Stato di avviso per un possibile pericolo' }
      ]
    }

  ]
};
