#!/bin/bash

wsd="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
savepwd=$PWD

# Download Freemius API wrapper in php
if [ ! -d "$wsd/freemius-php-api" ]; then
    git clone git@github.com:Freemius/php-sdk.git "$wd"/freemius-php-api
fi
if [ ! -f "$wsd/config.ini" ]; then
    echo "file config.ini missing"
    exit
fi

# Read the config.ini
eval $(crudini --get --format=sh  "$wsd"/config.ini $1)
eval $(crudini --get --format=sh  "$wsd"/config.ini Login)

. "$wsd"/package.sh $path $filename

filezip="$wd"/"$packagename"-"$version".zip

php "$wsd"/deploy.php $user $pubkey $secretkey $filezip $id $sandbox

rm $filezip
