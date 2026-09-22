<?php
declare(strict_types=1);
/* ============================================================================
   PONTE VERSO SALUTE LAZIO — stato dei pronto soccorso per la Sala situazioni
   ============================================================================

   PERCHE' ESISTE. Il servizio della Regione risponde bene a una richiesta
   normale, ma se la richiesta porta l'intestazione Origin — cioe' se parte da
   una pagina web di un altro sito — risponde 400. Dal browser quindi non si
   legge (verificato il 22/09/2026 con GET e con OPTIONS). La richiesta parte
   allora da questo server, che quel vincolo non ce l'ha, e torna alla pagina
   come roba nostra: stessa origine, nessun terzo contattato dal browser,
   niente da aggiungere alla CSP, nessun servizio esterno che sappia chi sta
   guardando. E' lo stesso ponte gia' in uso per i mezzi aerei; le ragioni per
   cui questa e' l'unica eccezione al sito statico stanno in
   .claude/rules/05-github-aruba-deploy.md § "L'unica eccezione al sito statico".

   LICENZA E RIUSO. Il dato e' pubblicato dalla Regione Lazio come open data
   ("Pronto Soccorso - Accessi in tempo reale", dati.lazio.it) sotto Creative
   Commons Attribuzione 4.0, e la Regione invita espressamente a costruirci
   applicazioni. L'attribuzione viaggia dentro la risposta e sta scritta nella
   scheda della pagina: non si toglie.

   COSA NON E'. Non e' un proxy generico: l'indirizzo di destinazione e' fisso
   e scritto qui dentro, non arriva da chi chiama. Niente $_GET, niente $_POST.

   🔴 COSA QUESTO DATO NON DICE. Non e' una guida per scegliere dove andare.
   In emergenza si chiama il 112: e' la centrale che decide l'ospedale in base
   alle condizioni della persona e alle specialita' disponibili, e un codice
   rosso non fa la fila. Il numero di pazienti in attesa serve a chi il PC
   lo presidia per farsi un'idea del carico sul territorio, non al cittadino
   per mettersi in auto verso l'ospedale che sembra piu' sgombro.
   ============================================================================ */

const FONTE        = 'https://server.salutelazio.it/server/external-services';
const LAT          = 41.7085;   // Genzano di Roma
const LON          = 12.6916;
const QUANTI       = 10;        // pronto soccorso piu' vicini di cui chiedere lo stato
const CACHE_STATO  = 60;        // lo stato cambia di continuo: copia locale di un minuto
const CACHE_ELENCO = 21600;     // l'elenco degli ospedali cambia una volta ogni tanto
const TIMEOUT_SEC  = 8;
const UA           = 'PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/ Sala situazioni, Protezione Civile Genzano di Roma)';

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');
header('X-Content-Type-Options: nosniff');

function esci(array $dati, int $codice = 200): void {
    http_response_code($codice);
    echo json_encode($dati, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

function scarica(string $url): ?string {
    if (function_exists('curl_init')) {
        $c = curl_init($url);
        curl_setopt_array($c, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT        => TIMEOUT_SEC,
            CURLOPT_CONNECTTIMEOUT => 5,
            CURLOPT_USERAGENT      => UA,
            CURLOPT_FOLLOWLOCATION => false,
            CURLOPT_HTTPHEADER     => ['Accept: application/json'],
        ]);
        $r  = curl_exec($c);
        $ok = ($r !== false && curl_getinfo($c, CURLINFO_RESPONSE_CODE) === 200);
        curl_close($c);
        return $ok ? (string)$r : null;
    }
    $ctx = stream_context_create(['http' => [
        'timeout' => TIMEOUT_SEC,
        'header'  => "Accept: application/json\r\nUser-Agent: " . UA . "\r\n",
    ]]);
    $r = @file_get_contents($url, false, $ctx);
    return $r === false ? null : (string)$r;
}

/** Scarico con copia locale. Se la fonte tace si riusa la copia anche scaduta,
 *  marcandola: chi legge deve poter dire da quando quel numero non si muove. */
function conCache(string $url, string $chiave, int $validita): ?array {
    $f = sys_get_temp_dir() . '/pcgz-ps-' . preg_replace('/[^a-z0-9_-]/i', '', $chiave) . '.json';
    if (is_readable($f) && (time() - (int)@filemtime($f)) < $validita) {
        $d = json_decode((string)@file_get_contents($f), true);
        if (is_array($d)) return $d;
    }
    $grezzo = scarica($url);
    if ($grezzo === null) {
        if (is_readable($f)) {
            $d = json_decode((string)@file_get_contents($f), true);
            if (is_array($d)) { $d['_vecchia'] = (int)@filemtime($f); return $d; }
        }
        return null;
    }
    $d = json_decode($grezzo, true);
    if (!is_array($d)) return null;
    @file_put_contents($f, $grezzo, LOCK_EX);
    return $d;
}

function km(float $la1, float $lo1, float $la2, float $lo2): float {
    $p1 = deg2rad($la1); $p2 = deg2rad($la2);
    $dp = deg2rad($la2 - $la1); $dl = deg2rad($lo2 - $lo1);
    $a  = sin($dp / 2) ** 2 + cos($p1) * cos($p2) * sin($dl / 2) ** 2;
    return 6371.0 * 2 * atan2(sqrt($a), sqrt(1 - $a));
}

/* --- 1. l'elenco dei pronto soccorso del Lazio (tipo 006) --- */
$qElenco = http_build_query([
    'westLng'  => 11.4, 'southLat' => 40.7,
    'eastLng'  => 14.1, 'northLat' => 42.9,
    'zoom'     => 9,    'lang'     => 'it',
    'page'     => 1,    'limit'    => 100,
]) . '&facilityTypeIds=006';

$elenco = conCache(FONTE . '/facilities/structures/list?' . $qElenco, 'elenco', CACHE_ELENCO);
$voci   = is_array($elenco['items'] ?? null) ? $elenco['items'] : [];

if (!$voci) {
    esci([
        'ospedali'  => [],
        '_sorgente' => ['diretta' => false, 'errore' => 'elenco dei pronto soccorso non raggiungibile'],
    ], 200);
}

/* --- 2. i piu' vicini a Genzano: sono quelli che contano per noi --- */
$vicini = [];
foreach ($voci as $v) {
    $g  = $v['geometry'] ?? null;
    $la = isset($g['latitude'])  ? (float)$g['latitude']  : null;
    $lo = isset($g['longitude']) ? (float)$g['longitude'] : null;
    $id = $v['emergencyOrganizationId'] ?? null;
    if ($la === null || $lo === null || !$id) continue;
    $vicini[] = [
        'id'        => (string)$id,
        'nome'      => (string)($v['name'] ?? ''),
        'indirizzo' => (string)($v['plainAddress'] ?? ''),
        'telefono'  => (string)($v['contactPhone'] ?? ''),
        'lat'       => $la,
        'lon'       => $lo,
        'km'        => round(km(LAT, LON, $la, $lo), 1),
    ];
}
usort($vicini, static fn(array $a, array $b): int => $a['km'] <=> $b['km']);
$vicini = array_slice($vicini, 0, QUANTI);

/* --- 3. lo stato di ciascuno --- */
$ospedali = [];
$piuVecchio = 0;
foreach ($vicini as $o) {
    $st = conCache(
        FONTE . '/facilities/structures/emergency-status?facilityId=' . rawurlencode($o['id']),
        'stato-' . $o['id'],
        CACHE_STATO
    );
    if ($st === null) {
        $o['stato'] = null;
        $ospedali[] = $o;
        continue;
    }
    if (!empty($st['_vecchia'])) {
        $piuVecchio = max($piuVecchio, (int)$st['_vecchia']);
    }

    $codici  = [];
    $inAttesa = 0;
    foreach (($st['groups'] ?? []) as $g) {
        $tot = (int)($g['total'] ?? 0);
        $inAttesa += $tot;
        $codici[] = [
            'codice'    => (string)(($g['group']['code'] ?? '')),
            'etichetta' => (string)(($g['group']['labels']['it'] ?? '')),
            'pazienti'  => $tot,
            'attesaMediaMin'   => (int)round(((int)($g['avgWaitSeconds'] ?? 0)) / 60),
            'attesaMassimaMin' => (int)round(((int)($g['maxWaitSeconds'] ?? 0)) / 60),
            'colore'    => (string)($g['color'] ?? ''),
        ];
    }
    $o['stato'] = [
        'inAttesa' => $inAttesa,
        'codici'   => $codici,
    ];
    $ospedali[] = $o;
}

esci([
    'ospedali'  => $ospedali,
    '_sorgente' => [
        'diretta'      => true,
        'letto'        => gmdate('c'),
        'fonte'        => 'Regione Lazio — Salute Lazio',
        'licenza'      => 'CC BY 4.0',
        'attribuzione' => 'Dati del pronto soccorso: Regione Lazio — Salute Lazio (CC BY 4.0)',
        'copia_vecchia_del' => $piuVecchio ? gmdate('c', $piuVecchio) : null,
        'avvertenza'   => 'In emergenza si chiama il 112: e\' la centrale che decide l\'ospedale. '
                        . 'Questi numeri dicono il carico sui pronto soccorso, non dove conviene andare.',
        'nota'         => 'I dieci pronto soccorso piu\' vicini a Genzano di Roma, dall\'elenco regionale delle strutture.',
    ],
]);
