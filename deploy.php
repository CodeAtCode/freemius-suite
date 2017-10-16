<?php
    require_once 'freemius-php-api/freemius/FreemiusBase.php';
    require_once 'freemius-php-api/freemius/Freemius.php';

    define( 'FS__API_SCOPE', 'developer' );
    define( 'FS__API_DEV_ID', $argv[1] );
    define( 'FS__API_PUBLIC_KEY', $argv[2] );
    define( 'FS__API_SECRET_KEY', $argv[3] );

    // Init SDK.
    $api = new Freemius_Api(FS__API_SCOPE, FS__API_DEV_ID, FS__API_PUBLIC_KEY, FS__API_SECRET_KEY, true);

    $result = $api->Api('plugins/115/tags.json', 'POST', array(
        'add_contributor' => false
    ), array(
        'file' => $argv[4]
    ));

    print_r($result);
