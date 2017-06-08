"""A slack chat bot doing scripts on the server
---
a slack bot can execute commands by slack chat room ( @bot_name: command ),
wherein these commands are specified in a folder.

NAME
    antbot

SYNOPSIS
    antbot [OPTION]

DESCRIPTION
    -h, --help
        show usage

    -c, --copy
        copy config file to current folder

COPYRIGHT
    MIT Licence

SOURCE
    https://github.com/yanganto/Ant

"""

from os import environ, path, getcwd, walk

from slackclient import SlackClient

BOT_ID = None
SLACK_BOT_TOKEN = None
SCRIPTS_FOLDER = None
BOT_NAME = None
LOG_FILE = None
OUTPUT = False
ENCODING = 'utf-8'
MENTION=False
COMMANDS = list()
DEBUG_CHANNEL = ""

# loading essential parameter from environment
if environ.get('BOT_ID'):
    BOT_ID = environ.get('BOT_ID')
if environ.get('SLACK_BOT_TOKEN'):
    SLACK_BOT_TOKEN = environ.get('SLACK_BOT_TOKEN')
if environ.get('BOT_NAME'):
    BOT_NAME = environ.get('BOT_NAME')
if environ.get("SCRIPTS_FOLDER"):
    SCRIPTS_FOLDER = environ.get("SCRIPTS_FOLDER")

_config_file_path = None

# load config from user settings
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
            if var == 'OUTPUT':
                OUTPUT = line.split('=')[1].strip().lower() == 'true'
            if var == 'ENCODING':
                ENCODING = line.split('=')[1].strip()
            if var == 'MENTION':
                MENTION = line.split('=')[1].strip().lower() == 'true'
            if var == 'DEBUG_CHANNEL':
                DEBUG_CHANNEL = line.split('=')[1].strip()

# load config from current folder
if path.isfile('./ant.conf'):
    _config_file_path = './ant.conf'

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
            if var == 'OUTPUT':
                OUTPUT = line.split('=')[1].strip().lower() == 'true'
            if var == 'ENCODING':
                ENCODING = line.split('=')[1].strip()
            if var == 'MENTION':
                MENTION = line.split('=')[1].strip().lower() == 'true'
            if var == 'DEBUG_CHANNEL':
                DEBUG_CHANNEL = line.split('=')[1].strip()

# get BOT ID if not provide
if not BOT_ID and BOT_NAME:
    slack_client = SlackClient(SLACK_BOT_TOKEN)
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                BOT_ID = user.get('id')

# script folder fall back as pwd
if not SCRIPTS_FOLDER:
    SCRIPTS_FOLDER = getcwd()

# get commands
for dir_path, dir_names, files in walk(SCRIPTS_FOLDER):
    for fullname in files:
        if fullname == 'ant.conf':
            continue
        COMMANDS.append(fullname)

