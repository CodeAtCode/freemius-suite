#!/bin/bash
# First parameter not mandatory is the folder of the plugin, if not set use the current working directory
# Second parameter not mandatory is the root file of the plugin, if not set use the foldername of the plugin (not require the extension of the file)

pluginfolder=$1
originalfoldername=`basename $pluginfolder`
wd=$PWD
if [ -z $1 ]; then
    originalfoldername=`basename $PWD`
fi
fileroot=$2
if [ -z $2 ]; then
    fileroot=`basename $pluginfolder`
fi

r=$(( $RANDOM % 10 ));
foldername="$originalfoldername-$r"

echo "-Generating the zip in progress..."

cp -ar $pluginfolder /tmp/$foldername

cd /tmp/$foldername

version=`grep "^Stable tag:" README.txt | awk -F' ' '{print $NF}'`

echo "-Cleaning in Progress..."
rm -rf ./.git*
rm -rf ./.sass-cache
rm -rf ./.directory
rm -rf ./node_modules
rm -rf ./wp-config-test.php
rm -rf ./*.yml
rm -rf ./package.json
rm -rf ./Gruntfile.js
rm -rf ./composer.lock
rm -rf ./.netbeans*
rm -rf ./.php_cs
rm -rf ./assets
rm -rf ./admin/assets/sass
rm -rf ./admin/assets/coffee
rm -rf ./public/assets/sass
rm -rf ./public/assets/coffee
rm -rf ./*.zip
#This contain the test stuff
rm -rf ./vendor
rm -rf ./tests

#Detect if there are composer dependencies
dep=`cat composer.json | python -c "import json,sys;sys.stdout.write('true') if 'require' in json.load(sys.stdin)==False else sys.stdout.write('')"`7
if [ ! -z ${dep// } ]; then
    echo "-Downloading clean composer dependencies..."
    composer update --no-dev &> /dev/null
else
    rm -rf composer.json
fi

#Remove Fake_Freemius - it is the only requirement for Freemius
if [ -f './includes/Fake_Freemius.php' ]; then
    echo "-Cleaning for Freemius"
    rm -rf ./includes/Fake_Freemius.php
    rowff=`grep -n "/includes/Fake_Freemius.php" $fileroot.php | awk -F: '{print $1}'`
    rowff+='d'
    sed -i "$rowff" $fileroot.php
    #If Freemius SDK is commented remove the comments
    rowfs=`grep -n "/includes/freemius/start.php" $fileroot.php | awk -F: '{print $1}'`
    rowfs+='s'
    sed -i "$rowfs/\/\///" $fileroot.php
fi

zip -r $wd/$originalfoldername-$version.zip ./ &> /dev/null

rm -rf /tmp/$foldername

echo "-Done!"
