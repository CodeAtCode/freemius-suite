#!/bin/bash

# Slack bash script https://gist.github.com/andkirby/67a774513215d7ba06384186dd441d9e

file=$(readlink -f "$1")
if [[ ${file: -4} != ".zip" ]]; then
    echo "The file $file is not a zip."
    exit 1
fi

folder=$(basename "$1")
wd="/tmp/$folder.XXXX"
wd=$(mktemp -d "$wd")

echo "- Extracting free version $file"

cd "/tmp/" || exit
mkdir -p "$wd"
extract="$wd/upload"
if [ ! -f "$file" ]; then
    echo "$file doesn't exists"
    exit
fi

unzip "$file" -d "$extract" &> /dev/null
cd "$wd" || exit

# Get the plugin root file
rootfile=$(grep -R "WordPress-Plugin-Boilerplate-Powered" . | awk -F: '{print $1}')
# Get plugin version
version=$(grep " * Version:" "$rootfile" | awk -F' ' '{print $NF}')

# Get the domain for WP SVN
wpdomain=$(grep " * Text Domain:" "$rootfile" | awk -F' ' '{print $NF}')

if [ -z "$wpdomain" ]; then
    exit 1
fi

if [ -s "$extract/$wpdomain/composer.json" ]; then
    cd "$extract/$wpdomain"
    echo "- Regenerating composer files!"
    composer dumpautoload -o
    cd -
fi

echo "- Deploy on SVN started!"
echo "- Wait few minutes for the procedure!"

echo "- Cloning SVN locally"
svn co "https://plugins.svn.wordpress.org/$wpdomain" > /dev/null

echo "- Copying new plugin version on SVN locally"
cp -r "$extract/$wpdomain/." ./"$wpdomain"/trunk
cp -r "./$wpdomain"/trunk/. "$wpdomain"/tags/"$version"

echo "- Deploying new plugin version on SVN remote"
cd "$wpdomain" || exit
# This command force to add all the files, also if they are new
svn add --force * --auto-props --parents --depth infinity -q > /dev/null
svn ci -m "tagging version $version" 2>&1 | grep 'Error running context'
if [[ $? -eq 0 ]]
then
#     slack-message "Error on deploy on WordPress SVN of $version!"
    echo "- Deploy of the new free version failed!"
    exit 0
else
#     slack-message "Deploy on WordPress SVN of $version done!"
    echo "- Deploy of the new free version done!"
    exit 1
fi
cd /tmp/ || exit
rm -fr "./$wd"
echo " "
