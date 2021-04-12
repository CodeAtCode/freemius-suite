<?php
    require_once 'freemius-php-api/freemius/FreemiusBase.php';
    require_once 'freemius-php-api/freemius/Freemius.php';

	$sandbox      = ( $argv[6] === 'true' );
	$release_mode = ! isset( $argv[8] ) || empty( $argv[8] ) ? 'released' :  $argv[8];
	define( 'FS__API_SCOPE', 'developer' );
	define( 'FS__API_DEV_ID', $argv[1] );
	define( 'FS__API_PUBLIC_KEY', $argv[2] );
	define( 'FS__API_SECRET_KEY', $argv[3] );

    echo "- Deploy started on Freemius\n";

    try {
        // Init SDK.
        $api = new Freemius_Api(FS__API_SCOPE, FS__API_DEV_ID, FS__API_PUBLIC_KEY, FS__API_SECRET_KEY, $sandbox);

        if (!is_object($api)) {
            print_r($deploy);
            die();
        }

        $deploy = $api->Api('plugins/'.$argv[5].'/tags.json');
        echo "- Detection of latest tag released\n";
        
        if ( $deploy->tags[0]->version === $argv[6] ) {
                $deploy = $deploy->tags[0];
                echo '-Package already deployed on Freemius'."\n";
        } else {
            echo "- Deploy in progress\n";
            // Upload the zip
            $deploy = $api->Api('plugins/'.$argv[5].'/tags.json', 'POST', array(
                'add_contributor' => false
            ), array(
                'file' => $argv[4]
            ));

            if (!property_exists($deploy, 'id')) {
                print_r($deploy);
                echo "- Deploy error\n";
                exit(3);
            }

            echo "- Deploy done on Freemius\n";

            $is_released = $api->Api('plugins/'.$argv[5].'/tags/'.$deploy->id.'.json', 'PUT', array(
                'release_mode' => $release_mode
            ), array());

            echo "- Set as released on Freemius\n";
        }

        echo "- Download Freemius free version\n";
        
        // Generate url to download the zip
        $zip = $api->GetSignedUrl('plugins/'.$argv[5].'/tags/'.$deploy->id.'.zip');

        $path = pathinfo($argv[4]);
        $newzipname = $path['dirname'] . '/' . basename($argv[4], '.zip');
        $newzipname .= '.free.zip';

        file_put_contents($newzipname,file_get_contents($zip));
        
        echo "- Downloaded Freemius free version\n";
        exit();
    } catch (Exception $e) {
        echo "- Freemius server has problems\n";
        exit(3);
    }
