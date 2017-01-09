#!/bin/bash

file=$(readlink -f $1)
if [[ $file =~ \.zip$ ]];
    echo "The file $file is not a zip."
    exit 1
fi
r=$(( RANDOM % 10 ));
wd="$1-$r"
extract="$wd/upload"

echo "Deploy on SVN started!"
echo "Wait few minutes for the procedure!"
cd /tmp/
mkdir $wd
unzip $file -d $extract > /dev/null
cd $extract 
zipfolder=$(ls -d */|head -n 1)
cd /tmp/
cd $wd

# Get the plugin root file
rootfile=$(grep -R "WordPress-Plugin-Boilerplate-Powered" . | awk -F: '{print $1}')
# Get plugin version
version=$(grep " * Version:" "$rootfile" | awk -F' ' '{print $NF}')
# Get the domain for WP SVN
wpdomain=$(grep " * Text Domain:" "$rootfile" | awk -F' ' '{print $NF}')

if [ -z $wpdomain ]; then
    exit 1
fi

echo "Cloning SVN locally"
svn co "https://plugins.svn.wordpress.org/$wpdomain" > /dev/null

echo "Copying new plugin version on SVN locally"
cp -r "/tmp/$extract/$zipfolder/*" ./"$wpdomain"/trunk/
cp -r "./$wpdomain"/trunk "$wpdomain"/tags/"$version"

echo "Deploying new plugin version on SVN remote"
cd "$wpdomain"
svn add --force * --auto-props --parents --depth infinity -q > /dev/null
svn ci -m "tagging version $version"
 
cd /tmp/
rm -fr "./$wd"
echo " "
echo "Deploy of the new version done!"
