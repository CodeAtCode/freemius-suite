#!/usr/bin/python3
import sys, configparser,urllib3,subprocess, os.path
from _sha1 import sha1
from base64 import b64encode
from datetime import datetime
from http.client import HTTPConnection
import hmac

if os.path.isfile('config.ini'):
    # Load configuration
    config = configparser.RawConfigParser()
    config.readfp(open('config.ini')) 
else:
    print('Configuration file is missing!')
    sys.exit()
    
if len(sys.argv) == 0:
    print('The folder of the script is required!')
    sys.exit()

def create_signature(string_to_sign):
    """ Create the signature for HMAC-SHA1 """
    return b64encode(hmac.new(config.get('Login', 'secretkey').encode('utf-8'), string_to_sign.encode('utf-8'), sha1).digest()).decode()

def create_token_header():
    """ Create an header http://docs.freemius.apiary.io/#introduction/the-authentication-header """
    string_to_sign = "GET\n"+\
                     "application/x-www-form-urlencoded\n"+\
                     datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
    signature = {
                 'FS ': config.get('Login', 'user') + ':' + config.get('Login', 'pubkey') + ':' + create_signature(string_to_sign)
    }
    return signature

def generate_request_parameter(parameter={}):
    devid = {'developer_id': config.get('Login', 'user')}
    # Merge the dicts
    return urllib3.request.urlencode(dict(list(parameter.items()) + list(devid.items())))

def get_plugin_version(path):
    stabletag = subprocess.check_output('grep "^Stable tag:" ' + sys.argv[1] + '/README.txt', shell=True).decode("utf-8") 
    return stabletag.replace('Stable tag:','').replace(' ', '').rstrip()

#Do the ping!
conn = HTTPConnection('api.freemius.com')
conn.request('GET', '/v1/ping.json', generate_request_parameter(), create_token_header())
response = conn.getresponse()
if response.reason == 'OK':
    print(' Authentication on Freemius it\'s working! Hooray!')
else:
    print(' Authentication on Freemius is not working!')
    sys.exit()
    
packagecommands = ''
plugin_slug = os.path.basename(os.path.dirname(sys.argv[1]))
if len(sys.argv) > 2:
    packagecommands = sys.argv[1] + " " + sys.argv[2]
elif len(sys.argv) > 1:
    packagecommands = sys.argv[1]

if not os.path.isfile('./' + plugin_slug + '-' + get_plugin_version(sys.argv[1]) + '.zip'):
    subprocess.call("./package.sh " + packagecommands, shell=True)
else:
    print(' Already available a ' + plugin_slug + '-' + get_plugin_version(sys.argv[1]) + '.zip file, not packaging again')

conn.request('GET', '/v1/plugins.json', generate_request_parameter({'plugin_id':config.get(plugin_slug, 'id')}), create_token_header())
response = conn.getresponse()
if response.reason == 'OK':
    print(response.read())
    