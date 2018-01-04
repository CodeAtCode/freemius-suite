#!/bin/bash

wsd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
output='/tmp'

# Download Freemius API wrapper in php
if [ ! -d "$wsd/freemius-php-api" ]; then
    echo "Download Freemius PHP SDK"
    git clone git@github.com:Freemius/php-sdk.git "$wsd"/freemius-php-api
fi
if [ ! -f "$wsd/config.ini" ]; then
    echo "file config.ini missing"
    exit
fi

echo "-Deploy process started"

# Read the config.ini
eval $(crudini --get --format=sh  "$wsd"/config.ini $1)
eval $(crudini --get --format=sh  "$wsd"/config.ini Login)

. "$wsd"/package.sh $path $filename

filezip="$output"/"$packagename"-"$version".zip

slack-message "Upload to Freemius and download in progress"

php "$wsd"/deploy.php $user $pubkey $secretkey $filezip $id $sandbox

rm $filezip

filezipfree="$output"/"$packagename"-"$version".free.zip

. "$wsd"/release.sh $filezipfree
