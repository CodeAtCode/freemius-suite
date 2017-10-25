<?php
    require_once 'freemius-php-api/freemius/FreemiusBase.php';
    require_once 'freemius-php-api/freemius/Freemius.php';

    $sandbox = ($argv[6] === 'true');
    define( 'FS__API_SCOPE', 'developer' );
    define( 'FS__API_DEV_ID', $argv[1] );
    define( 'FS__API_PUBLIC_KEY', $argv[2] );
    define( 'FS__API_SECRET_KEY', $argv[3] );

    // Init SDK.
    $api = new Freemius_Api(FS__API_SCOPE, FS__API_DEV_ID, FS__API_PUBLIC_KEY, FS__API_SECRET_KEY, $sandbox);

    $deploy = $api->Api('plugins/'.$argv[5].'/tags.json', 'POST', array(
        'add_contributor' => false
    ), array(
        'file' => $argv[4]
    ));

    $result = $api->Api('plugins/'.$argv[5].'/tags/'.$deploy->id.'.zip', 'GET', array(), array( ));

    $path = pathinfo($argv[4]);
    $newzipname = $path['dirname'] . '/' . basename($argv[4], '.zip');
    $newzipname .= '.free.zip';

    file_put_contents($newzipname,$result);
