<?php
declare(strict_types=1);
/* ============================================================================
   PONTE VERSO adsb.lol — mezzi aerei in tempo reale per la Sala situazioni
   ============================================================================

   PERCHE' ESISTE. Il browser non puo' leggere adsb.lol da solo: la fonte
   risponde ma non manda l'intestazione CORS, quindi la pagina viene fermata
   dal browser stesso (verificato con GET reali il 22/09/2026, come per
   adsb.fi, airplanes.live e OpenSky). La richiesta parte allora da questo
   server, che quel vincolo non ce l'ha, e torna alla pagina come roba nostra:
   stessa origine, nessun terzo contattato dal browser, niente da aggiungere
   alla CSP e nessun servizio esterno che sappia chi sta guardando.

   LICENZA. I dati sono di adsb.lol sotto Open Database License (ODbL) v1.0,
   la stessa di OpenStreetMap, che consente esplicitamente la ridistribuzione
   con attribuzione. E' la ragione per cui si usa questa fonte e non ADS-B
   Exchange, che tecnicamente si incorporerebbe ma lo vieta nelle proprie
   condizioni d'uso. L'attribuzione viaggia dentro la risposta e sta scritta
   nella scheda della pagina: non si toglie.

   COSA NON E'. Non e' un proxy generico: l'indirizzo di destinazione e'
   fisso e scritto qui dentro, non arriva da chi chiama. Un proxy che accetta
   un URL dall'esterno diventa un ponte per raggiungere qualunque cosa a nome
   del nostro dominio, ed e' esattamente il genere di regalo che non si fa.

   COME SI COMPORTA CON LA FONTE. Una copia locale di pochi secondi fa da
   cuscinetto: cento visitatori contemporanei restano poche richieste al
   minuto verso adsb.lol invece di cento. La fonte chiede di essere avvisata
   per usi di produzione: se il traffico dovesse crescere, si scrive loro.
   ============================================================================ */

const FONTE       = 'https://api.adsb.lol/v2';
const LAT         = 41.7085;      // Genzano di Roma
const LON         = 12.6916;
const RAGGIO_NM   = 250;          // tetto della fonte, ~463 km: copre l'area operativa
const CACHE_SEC   = 12;           // eta' massima della copia locale
const TIMEOUT_SEC = 8;            // oltre, si risponde "fonte non raggiungibile"
const UA          = 'PCGenzanoBot/1.0 (+https://www.protezionecivilegenzano.it/ Sala situazioni, Protezione Civile Genzano di Roma)';

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');           // coerente con la politica del sito
header('X-Content-Type-Options: nosniff');

function esci(array $dati, int $codice = 200): void {
    http_response_code($codice);
    echo json_encode($dati, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
    exit;
}

/* --- regole di classificazione: un posto solo, condiviso con il generatore --- */
$regole = @file_get_contents(__DIR__ . '/volo-classificazione.json');
$R = $regole === false ? null : json_decode($regole, true);
if (!is_array($R)) {
    esci(['errore' => 'regole di classificazione non leggibili'], 500);
}

/* --- scarico, con una copia locale di pochi secondi come cuscinetto --- */
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
        $r = curl_exec($c);
        $ok = ($r !== false && curl_getinfo($c, CURLINFO_RESPONSE_CODE) === 200);
        curl_close($c);
        return $ok ? (string)$r : null;
    }
    $ctx = stream_context_create(['http' => [
        'timeout' => TIMEOUT_SEC, 'header' => "Accept: application/json\r\nUser-Agent: " . UA . "\r\n",
    ]]);
    $r = @file_get_contents($url, false, $ctx);
    return $r === false ? null : (string)$r;
}

function conCache(string $url, string $chiave): ?array {
    $f = sys_get_temp_dir() . '/pcgz-aerei-' . $chiave . '.json';
    if (is_readable($f) && (time() - (int)@filemtime($f)) < CACHE_SEC) {
        $d = json_decode((string)@file_get_contents($f), true);
        if (is_array($d)) return $d;
    }
    $grezzo = scarica($url);
    if ($grezzo === null) {
        // fonte muta: si riusa la copia locale anche se scaduta, ma chi legge
        // dovra' sapere che non e' fresca — l'eta' la calcola chi chiama
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

/* --- distanza in km sulla sfera, come nel generatore --- */
function km(float $la1, float $lo1, float $la2, float $lo2): float {
    $r = 6371.0;
    $p1 = deg2rad($la1); $p2 = deg2rad($la2);
    $dp = deg2rad($la2 - $la1); $dl = deg2rad($lo2 - $lo1);
    $a = sin($dp / 2) ** 2 + cos($p1) * cos($p2) * sin($dl / 2) ** 2;
    return $r * 2 * atan2(sqrt($a), sqrt(1 - $a));
}

function numero($v): ?float {
    if (!is_numeric($v)) return null;
    $f = (float)$v;
    return is_nan($f) ? null : $f;
}

function scheda(array $a, array $R): ?array {
    $la = numero($a['lat'] ?? null); $lo = numero($a['lon'] ?? null);
    if ($la === null || $lo === null) return null;
    $dist = km(LAT, LON, $la, $lo);
    if ($dist > (float)$R['raggio_notevoli_km']) return null;

    $aTerra = (string)($a['alt_baro'] ?? '') === 'ground';
    $quota  = $aTerra ? 0.0 : numero($a['alt_baro'] ?? null);
    $cat    = (string)($a['category'] ?? '');
    $tipo   = strtoupper(trim((string)($a['t'] ?? '')));
    $sq     = (string)($a['squawk'] ?? '');
    $em     = strtolower((string)($a['emergency'] ?? ''));

    $etichette = [];
    // 🔴 Si classifica sul DESIGNATORE ICAO, non su una descrizione testuale:
    //    questa fonte la descrizione non la manda. Confronto esatto, non per
    //    sottostringa — un "contiene" su codici di quattro lettere aggancia
    //    parenti che non c'entrano.
    if ($tipo !== '' && in_array($tipo, array_map('strtoupper', $R['tipi_antincendio']), true)) {
        $etichette[] = 'antincendio';
    }
    if ($cat === 'A7') $etichette[] = 'elicottero';
    $inEmergenza = isset($R['emergenze'][$sq]) || ($em !== '' && !in_array($em, ['none', 'no', 'null'], true));
    if ($inEmergenza) $etichette[] = 'emergenza';
    if ($quota !== null && !$aTerra && $quota <= (float)$R['quota_bassa_ft']) $etichette[] = 'bassa-quota';

    $v = [
        'hex'              => $a['hex'] ?? null,
        'immatricolazione' => ($a['r'] ?? null) ?: null,
        'volo'             => trim((string)($a['flight'] ?? '')) ?: null,
        // la fonte non manda una descrizione del modello: si riporta il
        // designatore ICAO, che e' un dato e non una nostra interpretazione
        'modello'          => null,
        'tipo_icao'        => $tipo ?: null,
        'categoria'        => $R['categorie'][$cat] ?? 'non dichiarata',
        'lat'              => round($la, 3),
        'lon'              => round($lo, 3),
        'quota_ft'         => $quota,
        'a_terra'          => $aTerra,
        'velocita_kt'      => numero($a['gs'] ?? null),
        'rotta'            => numero($a['dir'] ?? null) ?? numero($a['track'] ?? null),
        'km_da_genzano'    => (int)round($dist),
        'etichette'        => $etichette,
    ];
    if ($inEmergenza) {
        $v['motivo'] = $R['emergenze'][$sq] ?? ('codice di emergenza «' . $em . '»');
    }
    return $v;
}

/* --- due letture: l'area attorno a Genzano, e chi dichiara emergenza ovunque --- */
$area = conCache(sprintf('%s/point/%s/%s/%d', FONTE, LAT, LON, RAGGIO_NM), 'area');
$sos  = conCache(FONTE . '/sqk/7700', 'sos');

if ($area === null && $sos === null) {
    esci(['errore' => 'adsb.lol non raggiungibile in questo momento'], 502);
}

$vecchia = 0;
foreach ([$area, $sos] as $blocco) {
    if (is_array($blocco) && !empty($blocco['_vecchia'])) $vecchia = max($vecchia, (int)$blocco['_vecchia']);
}

$visti = [];
foreach ([$area, $sos] as $blocco) {
    if (!is_array($blocco)) continue;
    foreach (($blocco['ac'] ?? []) as $a) {
        if (!is_array($a)) continue;
        $hex = (string)($a['hex'] ?? '');
        if ($hex !== '' && isset($visti[$hex])) continue;     // lo stesso velivolo puo' stare in entrambe
        $v = scheda($a, $R);
        if ($v !== null) $visti[$hex !== '' ? $hex : count($visti)] = $v;
    }
}
$lista = array_values($visti);
usort($lista, static fn($x, $y) => $x['km_da_genzano'] <=> $y['km_da_genzano']);

esci([
    'velivoli'  => $lista,
    '_sorgente' => [
        'diretta'      => true,
        'letto'        => gmdate('c'),
        'fonte'        => 'adsb.lol',
        'licenza'      => 'ODbL 1.0',
        'attribuzione' => 'Dati dei velivoli: adsb.lol (ODbL 1.0)',
        'raggio_km'    => (int)round(RAGGIO_NM * 1.852),
        'nota'         => 'Area attorno a Genzano piu\' i velivoli che trasmettono il codice di emergenza 7700, ovunque si trovino.',
        // se la fonte e' muta e si sta servendo una copia scaduta, lo si dice:
        // chi legge deve poter distinguere "adesso" da "l'ultima volta che ha risposto"
        'copia_vecchia_del' => $vecchia ? gmdate('c', $vecchia) : null,
    ],
]);
