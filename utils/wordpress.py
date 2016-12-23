import sys, subprocess, os.path


def get_plugin_version(path=''):
    if path == '':
        path = sys.argv[1]
    command = 'grep "^Stable tag:" ' + sys.argv[1] + '/README.txt'
    stabletag = subprocess.check_output(command, shell=True).decode("utf-8")
    return stabletag.replace('Stable tag:', '').replace(' ', '').rstrip()


def plugin_slug():
    return os.path.basename(os.path.dirname(sys.argv[1] + '/'))


def get_zip_name():
    return plugin_slug() + '-' + get_plugin_version() + '.zip'


def generate_package():
    # Prepare the command
    packagecommands = ''
    if len(sys.argv) > 2:
        packagecommands = sys.argv[1] + " " + sys.argv[2]
    elif len(sys.argv) > 1:
        packagecommands = sys.argv[1]
    # Package the plugin
    package = get_zip_name()
    if not os.path.isfile('./' + package):
        subprocess.call("./package.sh " + packagecommands, shell=True)
    else:
        print(' Already available a %s file, not packaging again' % package)
