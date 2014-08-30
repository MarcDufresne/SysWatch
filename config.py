from ConfigParser import ConfigParser
import os


HOME_DIR = os.path.expanduser("~")
CONFIG_FOLDER = '/.syswatch/'
CONFIG_FILE = '/.syswatch/syswatch.conf'


def check_config_file():

    if not os.path.exists(HOME_DIR + CONFIG_FOLDER):
        os.makedirs(HOME_DIR + CONFIG_FOLDER)

    config_file = HOME_DIR + CONFIG_FILE

    if not os.path.isfile(config_file):
        with open(config_file, 'w') as c_file:
            c_file.write('[Monitoring]\n')
            c_file.write('DISKS: /,/media/ext\n')
            c_file.write('PROCESSES: ServerMonitorClient.py,htop\n')
            c_file.write('# Define disks and processes by separating them by a comma like the example above.')
            c_file.close()

    return config_file


def load_config_file():

    config = ConfigParser()
    config.read(HOME_DIR + CONFIG_FILE)

    sections = config.sections()

    options = []

    for section in sections:
        options.extend(config.items(section))

    configs = {}

    for option in options:
        configs[option[0]] = option[1]

    return configs