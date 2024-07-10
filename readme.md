# Freemius Suite

[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)   

The focus of this project is to have a suite of scripts to automatize few steps on the deploy of a new version of a plugin on Freemius and on WordPress SVN.

## Requirements

* crudini (parse the config.ini easily from bash)
* php-cli
* jq on OSX

# Install it

Just copy and rename `config-sample.ini` to `config.ini` and set as you need.

# How to use it

## deploy.sh

This script use the `config.ini` file to get the settings like dev id etc.  

`deploy.sh [your-section]`

Automatically will execute all the script suite with deploying on Fremmius and on WordPress SVN of the free version.

## package.sh

This script from a folder generate a zip package ready (with `composer update --no-dev`) to be uploaded on Freemius.  
It also switch from `Fake_Freemius` (a fake class to simulate Freemius SDK) if in the code is enabled.  
Generate a zip in the working directory where the plugin is executed.

`package.sh [plugin-folder] [plugin-root-filename]`

* The first parameter is the plugin folder, if not set use the current working directory.
* The second parameter is the root filename of the plugin (where there are the Plugin Header Comments) without the extension, if not set use the plugin folder name.

This script will also execute [wp-readme-last-wp-tested](https://github.com/WPBP/tools/blob/master/wp-readme-last-wp-tested.sh) if command isfound, that let you to automatically bump the Tested Up field with the latest WordPress release in the readme.

## release.sh

This script from a zip file, unzip the package and push a new version of WP SVN.  
It use internally the string `WordPress-Plugin-Boilerplate-Powered` to find the plugin root file, so change based on your needs.

`package.sh [plugin-file-zip]`

* The first parameter is the zip of the plugin.

## deploy.php

This script require a `config.ini` with the user id, the public key and secret key and the plugins to deployt with path.  

`deploy.php [user] []pubkey [secretkey] [zip-file] [freemius-plugin-id] [sandbox:true|false] [version] [releasemode:pending|beta|released]`

The script will download the API wrapper in PHP of Freemius, next execute `package.sh` (that will get the parameters from the config.ini).  
Will execute the deploy system using the official API to upload and download the package.  
The last parameter is not used in the suite.
