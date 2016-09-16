"""
    Generate the configs
"""

from os import environ, path, getcwd, walk
import platform

from slackclient import SlackClient

BOT_ID = None
SLACK_BOT_TOKEN = None
SCRIPTS_FOLDER = None
BOT_NAME = None
if platform.system() == 'Windows':
    LOG_FILE = '/'
else:
    LOG_FILE = '/var/log/ant.log'
COMMANDS = list()

_config_file_path = None

if path.isfile('./ant.conf'):
    _config_file_path = './ant.conf'
if path.isfile('~/.config/ant.conf'):
    _config_file_path = '~/ant.conf'

if _config_file_path:
    with open(_config_file_path) as config:
        for line in config:
            line = line.strip()
            if line.startswith('#'):
                continue
            var = line.split('=')[0].strip()
            if var == 'BOT_ID':
                BOT_ID = line.split('=')[1].strip()
            if var == 'SLACK_BOT_TOKEN':
                SLACK_BOT_TOKEN = line.split('=')[1].strip()
            if var == 'SCRIPTS_FOLDER':
                SCRIPTS_FOLDER = line.split('=')[1].strip()
            if var == 'BOT_NAME':
                BOT_NAME = line.split('=')[1].strip()
            if var == 'LOG_FILE':
                LOG_FILE = line.split('=')[1].strip()
else:
    BOT_ID = environ.get('BOT_ID')
    SLACK_BOT_TOKEN = environ.get('SLACK_BOT_TOKEN')
    SCRIPTS_FOLDER = environ.get("SCRIPTS_FOLDER")

if not SLACK_BOT_TOKEN:
    raise EnvironmentError('Lack of API TOKEN')

if not BOT_ID and BOT_NAME:
    slack_client = SlackClient(SLACK_BOT_TOKEN)
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                BOT_ID = user.get('id')

if not BOT_ID:
    raise EnvironmentError('Lack of BOT ID')

if not SCRIPTS_FOLDER:
    SCRIPTS_FOLDER = getcwd()

for dir_path, dir_names, files in walk(SCRIPTS_FOLDER):
    for fullname in files:
        if fullname == 'ant.conf':
            continue
        COMMANDS.append(fullname)

