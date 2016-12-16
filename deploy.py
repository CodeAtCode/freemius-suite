#!/usr/bin/python3
import sys, configparser,urllib3,urllib
from base64 import b64encode
from datetime import datetime
from Crypto.Hash import SHA, HMAC

# Load configuration
config = configparser.RawConfigParser()
config.readfp(open('config.ini')) 

def create_signature(secret_key, string):
    """ Create the signed message from api_key and string_to_sign """
    hmac = HMAC.new(secret_key, string.encode('utf-8'), SHA)
    return b64encode(hmac.hexdigest())

def create_token():
    string_to_sign = "GET\n"+\
                     "application/x-www-form-urlencoded\n"+\
                     datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
    hmac = create_signature(config.get('Login', 'secretkey'), string_to_sign)
    signature = {'FS ': config.get('Login', 'user') + ':' + config.get('Login', 'pubkey') + hmac}
    return signature

data = urllib.parse.urlencode('')
req = urllib3.request('https://fast-api.freemius.com/v1/developers/' + config.get('Login', 'user') + '/ping.json', data, create_token())
response = urllib3.request.urlopen(req)
print(response)