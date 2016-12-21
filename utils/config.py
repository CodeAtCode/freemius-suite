import sys, configparser, os.path


if len(sys.argv) == 0:
    print('The folder of the script is required!')
    sys.exit()

if os.path.isfile('config.ini'):
    # Load configuration
    ini = configparser.RawConfigParser()
    ini.readfp(open('config.ini'))
else:
    print('Configuration file is missing!')
    sys.exit()
