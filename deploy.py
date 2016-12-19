#!/usr/bin/python3
import sys, configparser,urllib3,subprocess
from _sha1 import sha1
from base64 import b64encode
from datetime import datetime
from http.client import HTTPConnection
import hmac

# Load configuration
config = configparser.RawConfigParser()
config.readfp(open('config.ini')) 

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

#Do the ping!
conn = HTTPConnection('api.freemius.com')
conn.request('GET', '/v1/ping.json', generate_request_parameter(), create_token_header())
response = conn.getresponse()
if response.reason == 'OK':
    print(' Authentication on Freemius it\'s working! Hooray!')
else:
    print(' Authentication on Freemius is not working!')
    exit
    
packagecommands = ''
if len(sys.argv) > 1:
    packagecommands = sys.argv[1] + " " + sys.argv[2]
elif len(sys.argv) > 0:
    packagecommands = sys.argv[1]
subprocess.call("./package.sh " + packagecommands, shell=True)

conn.request('GET', '/v1/plugins.json', generate_request_parameter({'plugin_id':config.get('Login', 'pubkey')}), create_token_header())
response = conn.getresponse()
if response.reason == 'OK':
    print(response.read())
    