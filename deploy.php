<?php
    require_once 'freemius-php-api/freemius/FreemiusBase.php';
    require_once 'freemius-php-api/freemius/Freemius.php';

	$sandbox      = ( $argv[6] === 'true' );
	$release_mode = ! isset( $argv[7] ) || empty( $argv[7] ) ? 'released' :  $argv[7];
	define( 'FS__API_SCOPE', 'developer' );
	define( 'FS__API_DEV_ID', $argv[1] );
	define( 'FS__API_PUBLIC_KEY', $argv[2] );
	define( 'FS__API_SECRET_KEY', $argv[3] );

    echo "- Deploy in progress on Freemius\n";

    try {
        // Init SDK.
        $api = new Freemius_Api(FS__API_SCOPE, FS__API_DEV_ID, FS__API_PUBLIC_KEY, FS__API_SECRET_KEY, $sandbox);

        if (!is_object($api)) {
            print_r($deploy);
            die();
        }

        $deploy = $api->Api('plugins/'.$argv[5].'/tags.json');
        if ( $deploy->tags[0]->version === $argv[6] ) {
                $deploy = $deploy->tags[0];
                echo '-Package already deployed on Freemius'."\n";
        } else {
            // Upload the zip
            $deploy = $api->Api('plugins/'.$argv[5].'/tags.json', 'POST', array(
                'add_contributor' => false
            ), array(
                'file' => $argv[4]
            ));

            if (!property_exists($deploy, 'id')) {
                print_r($deploy);
                die();
            }

            echo "- Deploy done on Freemius\n";

            // Set as released
            $is_released = $api->Api('plugins/'.$argv[5].'/tags/'.$deploy->id.'.json', 'PUT', array(
                'release_mode' => $release_mode
            ), array());

            echo "- Set as released on Freemius\n";
        }

        // Generate url to download the zip
        $zip = $api->GetSignedUrl('plugins/'.$argv[5].'/tags/'.$deploy->id.'.zip');

        $path = pathinfo($argv[4]);
        $newzipname = $path['dirname'] . '/' . basename($argv[4], '.zip');
        $newzipname .= '.free.zip';

        file_put_contents($newzipname,file_get_contents($zip));

        echo "- Download Freemius free version\n";
    }
    catch (Exception $e) {
        echo "- Freemius server has problems\n";
        die();
    }
