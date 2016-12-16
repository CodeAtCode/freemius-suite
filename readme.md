#Freemius Suite
[![License](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)   

The focus of this project is to have a suite of scripts to automatize few steps on the deploy of a new version of a plugin on Freemius.

##package.sh

This script from a folder generate a zip package ready to be uploaded on Freemius.  
It also switch from Fake_Freemius if in the code is enabled.  
Generate a zip in the working directory where the plugin is executed.

`package.sh [plugin-folder] [plugin-root-filename]`

* The first parameter is the plugin folder, if not set use the current working directory.
* The second parameter is the root filename of the plugin (where there are the Plugin Header Comments) without the extension, if not set use the plugin folder name.

##deploy.py

This script require a `config.ini` with the user id, the public key and secret key.  
After this the script do a ping to Freemius to check if the data login are working, next execute `package.sh`, the parameters are the same of `package.sh`.  
*WIP* deploy the zip generated and switch as new version, next download the free version and upload on SVN.

