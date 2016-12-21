#!/usr/bin/python3
import sys, configparser, urllib3, subprocess
import hashlib, hmac, base64, os.path, json
from datetime import datetime
from http.client import HTTPConnection

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
    """ Create the signature for HMAC-SHA256 """
    # Require to be a byte and not a string
    hmacencode = hmac.new(
                          config.get('Login', 'secretkey').encode('utf-8'),
                          string_to_sign.encode('utf-8'),
                          hashlib.sha256
                 ).hexdigest().encode('utf-8')
    b64 = str(base64.b64encode(hmacencode))
    b64 = b64.rstrip().replace('=', '').replace('+/', '-_')[:-1][2:]
    return b64


def token_header(url=None, method='GET'):
    """ Create an header
    http://docs.freemius.apiary.io/#introduction/the-authentication-header """
    url = url or ''
    contenttype = 'application/json'
    # HTTP Method, MD5 Content on PUT/POST or empty for GET,
    # application/json only for PUT/POST or empty for GET,
    # Date and url
    string_to_sign = method + "\n\n\n" +\
        datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000') + "\n" + url
    if method == 'GET':
        contenttype = ''
    signature = {
                 'Authorization':
                 'FS ' + config.get('Login', 'user') + ':' +
                 config.get('Login', 'pubkey') + ':' +
                 create_signature(string_to_sign),
                 'Date':
                 datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000'),
                 'Content-Type': contenttype
    }
    return signature


def generate_req_parameters(parameter=None):
    parameter = parameter or {}
    devid = {'developer_id': config.get('Login', 'user')}
    # Merge the dicts
    merge = dict(list(parameter.items()) + list(devid.items()))
    return urllib3.request.urlencode(merge)


def get_plugin_version(path):
    command = 'grep "^Stable tag:" ' + sys.argv[1] + '/README.txt'
    stabletag = subprocess.check_output(command, shell=True).decode("utf-8")
    return stabletag.replace('Stable tag:', '').replace(' ', '').rstrip()


# Do the ping
conn = HTTPConnection('sandbox-api.freemius.com')
url = '/v1/ping.json'
conn.request('GET', url, generate_req_parameters(), {})
response = conn.getresponse()
# To reuse the same connection
response.read()
if response.reason == 'OK':
    print(' Service online! Hooray!')
else:
    print(' Service not online!')
    sys.exit()
# Prepare the command
packagecommands = ''
plugin_slug = os.path.basename(os.path.dirname(sys.argv[1]))
if len(sys.argv) > 2:
    packagecommands = sys.argv[1] + " " + sys.argv[2]
elif len(sys.argv) > 1:
    packagecommands = sys.argv[1]
# Package the plugin
version = get_plugin_version(sys.argv[1])
packagename = plugin_slug + '-' + version + '.zip'
if not os.path.isfile('./' + packagename):
    subprocess.call("./package.sh " + packagecommands, shell=True)
else:
    print(' Already available a ' + packagename + ' file, not packaging again')
# The first part of the url is always the same
devurl = '/v1/developers/' + config.get('Login', 'user') +\
         '/plugins/' + config.get(plugin_slug, 'id')
# Print the tags list and check if already on Freemius
print("\n--------------------")
url = devurl + '/tags.json'
conn.request('GET', url, '', token_header(url))
response = conn.getresponse()
if response.reason == 'OK':
    needjson = json.loads(response.read().decode('utf-8'))
    for tags in needjson['tags']:
        print(' - %s require %s, tested up on %s, uploaded on %s' %
              (tags['version'], tags['requires_platform_version'],
               tags['tested_up_to_version'], tags['created']))
        if tags['version'] == version:
            print('Version %s is already available on Freemius!' % version)
            sys.exit()
else:
    print('Plugin not exist or the authentication data are wrong.')
    sys.exit()
# Deploy the zip
print("--------------------")
print(' Deploying in progress of the %s' % version)
url = devurl + '/tags.json'
body = "-----BOUNDARY\nContent-Disposition: form-data;name='add_contributor'\n" \
"\n\ntrue\n-----BOUNDARY" \
"Content-Disposition: form-data; name='file'; filename='%s'\n" \
"Content-Type: application/zip\nContent-Transfer-Encoding: base64" \
"\n%s\n-----BOUNDARY--"
# Get the zip content as base64
with open(packagename, "rb") as zipcontent:
    b64zipcontent = base64.b64encode(zipcontent.read())
body = body % (packagename, b64zipcontent)
conn.request('POST', url, body, token_header(url, 'POST'))
response = conn.getresponse()
print(response.read())