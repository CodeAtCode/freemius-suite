import urllib3, hashlib, hmac, base64
from utils import config, functions
from datetime import datetime


def req_parameters(parameter=None):
    parameter = parameter or {}
    devid = {'developer_id': config.ini.get('Login', 'user')}
    # Merge the dicts
    merge = dict(list(parameter.items()) + list(devid.items()))
    return urllib3.request.urlencode(merge)


def sanitize_b64_header(string):
    string = str(base64.b64encode(string))
    string = string.rstrip().replace('=', '').replace('+/', '-_')
    string = functions.cut_bytes_delimeter(string)
    return string


def create_signature(string_to_sign):
    """ Create the signature for HMAC-SHA256 """
    # Require to be a byte and not a string
    hmacencode = hmac.new(
                          config.ini.get('Login', 'secretkey').encode('utf-8'),
                          string_to_sign.encode('utf-8'),
                          hashlib.sha256
                 ).hexdigest().encode('utf-8')
    return sanitize_b64_header(hmacencode)


def token_header(url, method='GET', contenttype='application/json', body=''):
    """ Create an header
    http://docs.freemius.apiary.io/#introduction/the-authentication-header """
    # HTTP Method, MD5 Content on PUT/POST or empty for GET,
    # application/json only for PUT/POST or empty for GET,
    # Date and url
    if method == 'GET':
        contenttype = ''
    if body != '':
        body = hashlib.md5(body.encode('utf-8')).hexdigest()
        body = functions.bytes_to_string(body)
    string_to_sign = method + "\n" + body + "\n" + contenttype + "\n" +\
        datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000') + "\n" + url
    print(string_to_sign)
    signature = {
                 'Authorization':
                 'FS ' + config.ini.get('Login', 'user') + ':' +
                 config.ini.get('Login', 'pubkey') + ':' +
                 create_signature(string_to_sign),
                 'Date':
                 datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000'),
                 'Content-Type': contenttype
    }
    return signature
