#!/bin/bash
# First parameter not mandatory is the folder of the plugin, if not set use the current working directory
# Second parameter not mandatory is the root file of the plugin, if not set use the foldername of the plugin (not require the extension of the file)

if [ "$(uname -s)" = 'Linux' ]; then
    pluginfolder=$(readlink -f "$1")
else
    pluginfolder=$(readlink "$1")
fi

output='/tmp'
if [ -z "$1" ]; then
    pluginfolder=$(pwd)
fi

originalfoldername=$(basename "$pluginfolder")
packagename=$2
if [ -z "$2" ]; then
    packagename=$(basename "$pluginfolder")
fi
fileroot="$packagename.php"
fullpathfile="$pluginfolder/$packagename.php"

if [ ! -f "$fullpathfile" ]; then
    echo "$fullpathfile file not exists"
    exit 1
fi

mktemp -d "/tmp/$originalfoldername"
foldername="/tmp/$originalfoldername"

cd "$pluginfolder" || exit

version=$(grep "^Stable tag:" README.txt | awk -F' ' '{print $NF}')

if [ -x "$(command -v wp-readme-last-wp-tested)" ]; then
    wp-readme-last-wp-tested README.txt
    if [ -n $(git diff-index --quiet HEAD) ]; then
        git add README.txt
        git commit -m "bumped Tested Up field in README.txt" -n
        git push origin master
    fi
fi

git tag -a "$version" -m "$version"
git checkout master
git push origin "$version"
echo "-Created the git tag for $version version"

cp -r "$pluginfolder" "$foldername"
cd "$foldername" || exit

echo "-Generating the zip in progress..."

echo "-Cleaning in Progress..."
rm -rf ./.git*
rm -rf ./.sass-cache
rm -rf ./.directory
rm -rf ./.eslintrc.json
rm -rf ./node_modules
rm -rf ./nbproject
rm -rf ./composer/
rm -rf ./wp-config-test.php
rm -rf ./*.yml
rm -rf ./*.neon
rm -rf ./*.ini
rm -rf ./*.sh
rm -rf ./*.xml
rm -rf ./.*.cache
rm -rf ./.env
rm -rf ./.gitignore
rm -rf ./.editorconfig
rm -rf ./package.json
rm -rf ./package-lock.json
rm -rf ./Gruntfile.js
rm -rf ./gulpfile.js
rm -rf ./composer.lock
rm -rf ./.travis*
rm -rf ./.php_cs
rm -rf ./wp-content
rm -rf ./*.zip
#This contain the test stuff
rm -rf ./tests

#This contain the WP repo assets
if [ -d './wp-assets' ]; then
    rm -rf ./wp-assets
else
    rm -rf ./assets
fi

if [ -s './composer.json' ]; then
    #Detect if there are composer dependencies
    dep=$(cat "./composer.json" | jq 'has("require")')
    if [ "$dep" == 'true' ]; then
        echo "-Downloading clean composer dependencies..."
        rm -rf vendor
        composer update --no-dev &> /dev/null
    else
        rm -rf ./composer.json
    fi
fi

#Remove Fake_Freemius - it is the only requirement for Freemius
if [ -s './Fake_Freemius.php' ]; then
    echo "-Cleaning for Freemius"
    rm -rf ./Fake_Freemius.php
    rowff=$(grep -n "/Fake_Freemius.php" "$fileroot" | awk -F: '{print $1}')
    rowff+='s'
    sed -i "$rowff/.*/		require_once dirname( __FILE__ ) \\. '\\/vendor\\/freemius\\/wordpress-sdk\\/start.php'\;/" "$fileroot"
fi

zip -r "$output"/"$packagename"-"$version".zip ./ &> /dev/null

rm -rf "$foldername"

echo " -Package generated!"
