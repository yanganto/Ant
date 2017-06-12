import time
import subprocess
import logging
from os import path

from slackclient import SlackClient

from antbot import SLACK_BOT_TOKEN, BOT_ID, SCRIPTS_FOLDER, COMMANDS, LOG_FILE, __doc__, OUTPUT, ENCODING, MENTION, DEBUG_CHANNEL

AT_BOT = "<@" + BOT_ID + ">:" if BOT_ID else ""

slack_client = SlackClient(SLACK_BOT_TOKEN) if SLACK_BOT_TOKEN else None

def slack_api_call(type, channel, text, as_user=True, user=""):
    message_text = text
    if MENTION and user:
        message_text = "<@" + user + "> " + message_text
    slack_client.api_call(type, channel=channel, text=message_text, as_user=True)

def handle_command(command, channel, user):
    """
        Receives commands and execute the commands in SCRIPTS_FOLDER
    """
    cmd = command.strip().split()[0]
    if cmd.lower().startswith('help'):
        response = "I can execute following scripts, please specify\n" + ", ".join(['*' + c + '*' for c in COMMANDS])
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    elif cmd in COMMANDS:
        response = "executing " + command
        logging.info(response)
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

        command_list = [c for c in command.strip().split() if not c.isspace()]
        command_list[0] = path.join(SCRIPTS_FOLDER, command_list[0])

        ps = subprocess.run(command_list, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
        if ps.returncode is not 0:
            response = command + ' raise exception: ' + str(ps.returncode)
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
            logging.error(response + " " + ps.stdout.decode(ENCODING, 'ignore'))
        else:
            logging.info("STDOUT: " + ps.stdout.decode(ENCODING, 'ignore'))

        if OUTPUT:
            slack_client.api_call("chat.postMessage", channel=channel, text=ps.stdout.decode(ENCODING, 'ignore'),
                    as_user=True)
        else:
            slack_api_call("chat.postMessage", channel=channel, text="Complete", as_user=True, user=user)

        if DEBUG_CHANNEL:
            slack_client.api_call("chat.postMessage", channel=DEBUG_CHANNEL, text=ps.stdout.decode(ENCODING, 'ignore'),
                    as_user=True)

    else:
        slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                              text="I don't know what you say, type *help* to know the commands I can use")
        logging.info("UNKNOWN: " + command)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip(), output['channel'], output['user']
    return None, None, None


def main():
    READ_WEBSOCKET_DELAY = 1
    logging.basicConfig(level=logging.DEBUG, format='LINE %(lineno)-4d  %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M', filename=LOG_FILE, filemode='w')
    if slack_client and slack_client.rtm_connect():
        logging.info("Chat bot connected and running!")
        while True:
            command, channel, user = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel, user)
            time.sleep(READ_WEBSOCKET_DELAY)


def cli():
    import sys
    import getopt
    import shutil
    from os import getcwd
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, "chv", ["copy", "help", "verbose"])
    except getopt.GetoptError as e:
        print(__doc__)
        sys.exit("invalid option: " + str(e))

    for o, a in opts:
        if o in ('-h', '--help'):
            print(__doc__)
            sys.exit(0)
        if o in ('-c', '--copy'):
            pkg_folder = path.dirname(path.abspath(__file__))
            shutil.copy(path.join(pkg_folder, 'ant.conf.example'), path.join(getcwd(), 'ant.conf'))
            print('please configure ' + path.join(getcwd(), 'ant.conf'))
            sys.exit(0)
        if o in ('-v', '--verbose'):
            logging.getLogger().setLevel(logging.DEBUG)
            logging.debug('debug mode')


    if not slack_client:
        print("""
!!! Configure file is missing or improper
type following command to copy a config file to current folder
$ antbot -c
""")
        sys.exit(1)

    logging.debug('config load')
    main()

if __name__ == "__main__":
    cli()
