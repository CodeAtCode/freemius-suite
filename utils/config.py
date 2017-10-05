import sys, configparser, os.path

path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
path = path + '/config.ini'

if len(sys.argv) == 0:
    print('The folder of the script is required!')
    sys.exit()

if os.path.isfile(path):
    # Load configuration
    ini = configparser.RawConfigParser()
    ini.readfp(open(path))
else:
    print('Configuration file is missing!')
    sys.exit()
