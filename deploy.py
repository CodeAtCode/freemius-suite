#!/usr/bin/python3
import sys, configparser,urllib3
from _sha1 import sha1
from base64 import b64encode
from datetime import datetime
from http.client import HTTPConnection
import hmac

# Load configuration
config = configparser.RawConfigParser()
config.readfp(open('config.ini')) 

def create_signature(string_to_sign):
    """ Create the signed message from api_key and string_to_sign """
    signed = hmac.new(config.get('Login', 'secretkey').encode('utf-8'), string_to_sign.encode('utf-8'), sha1).digest()
    return b64encode(signed).decode()

def create_token_header():
    string_to_sign = "GET\n"+\
                     "application/x-www-form-urlencoded\n"+\
                     datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
    signature = {
                 'FS ': config.get('Login', 'user') + ':' + config.get('Login', 'pubkey') + ':' + create_signature(string_to_sign),
                "Content-type": "application/x-www-form-urlencoded",
    }
    return signature

def generate_parameter():
    return urllib3.request.urlencode({'developer_id': config.get('Login', 'user')})
    
conn = HTTPConnection('fast-api.freemius.com')
conn.request('GET', '/v1/ping.json', generate_parameter(), create_token_header())
response = conn.getresponse()
print(response.status, response.reason)
data = response.read()
print(data)