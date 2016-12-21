from http.client import HTTPConnection
from utils import auth, config, wordpress, functions
import sys, json


def conn():
    return HTTPConnection('fast-sandbox-api.freemius.com')


fconn = conn()


def ping():
    global fconn
    url = '/v1/ping.json'
    fconn.request('GET', url, auth.req_parameters(), {})
    response = fconn.getresponse()
    # To reuse the same connection
    response.read()
    if response.reason == 'OK':
        print(' Service online! Hooray!')
    else:
        print(' Service not online!')
        sys.exit()


def devurl(append):
    # The first part of the url is always the same
    return '/v1/developers/' + config.ini.get('Login', 'user') +\
            '/plugins/' + config.ini.get(wordpress.plugin_slug(), 'id') +\
            '/' + append


def check_tags():
    global fconn
    # Print the tags list and check if already on Freemius
    print("\n--------------------")
    url = devurl('tags.json')
    fconn.request('GET', url, '', auth.token_header(url))
    response = fconn.getresponse()
    if response.reason == 'OK':
        version = wordpress.get_plugin_version()
        needjson = json.loads(response.read().decode('utf-8'))
        for tags in needjson['tags']:
            print(' - %s require %s, tested up on %s, uploaded on %s' %
                  (tags['version'], tags['requires_platform_version'],
                   tags['tested_up_to_version'], tags['created']))
            if tags['version'] == version:
                print("\nVersion %s is already available on Freemius!" %
                      version)
                sys.exit()
    else:
        print('Plugin not exist or the authentication data are wrong.')
        sys.exit()


def deploy_plugin():
    global fconn
    version = wordpress.get_plugin_version()
    packagename = wordpress.get_zip_name()
    print("--------------------")
    print(' Deploying in progress of the %s' % version)
    boundary = functions.boundary()
    url = devurl('tags.json')
    body = boundary + "\nContent-Disposition: form-data; name=\"data\"" \
        "\n\n{\"file\":{},\"add_contributor\":false}\n" + boundary + "\n" \
        "Content-Disposition: form-data; name='file'; filename='%s'\n" \
        "Content-Type: application/zip\n\n%s\n" + boundary + "\n"
    # Get the zip content as base64
    zipcontent = open(packagename, "rb").read()
#        b64zipcontent = zipcontent.read()
    #    b64zipcontent = str(base64.b64encode(zipcontent.read()))
    #    b64zipcontent = b64zipcontent.rstrip().replace('=', '').replace('+/', '-_')[:-1][2:]
    zipcontent = functions.bytes_to_string(zipcontent)
    zipcontent = zipcontent.replace('\n', '')
    body = body % (packagename, zipcontent)
    contenttype = 'multipart/form-data; boundary=' + boundary
    header = auth.token_header(url, 'POST', contenttype, body)
    fconn.request('POST', url, body, header)
    response = fconn.getresponse()
    print(response.read())
    print(" Deploying done!")
