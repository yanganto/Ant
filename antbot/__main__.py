import subprocess
import logging
from os import path, walk
from datetime import datetime

from slackclient import SlackClient
from nameko.timer import timer
from nameko.runners import ServiceRunner

from antbot import SLACK_BOT_TOKEN, BOT_ID, SCRIPTS_FOLDER, JOBS_FOLDER, COMMANDS, LOG_FILE, __doc__, OUTPUT, ENCODING, MENTION, DEBUG_CHANNEL, DEFAULT_SCRIPT, JOBS_CHANNEL

AT_BOT = "<@" + BOT_ID + ">" if BOT_ID else ""
READ_WEBSOCKET_DELAY = 1

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
        run_command_and_return(command_list, command, channel, user)

    elif DEFAULT_SCRIPT:
        command_list = [c for c in command.strip().split() if not c.isspace()]
        run_command_and_return([DEFAULT_SCRIPT] + command_list, command, channel, user)
    else:
        slack_client.api_call("chat.postMessage", channel=channel, as_user=True, text="I don't know what you say, type *help* to know the commands I can use")
        logging.info("UNHANDLE COMMAND: " + command)

def run_command_and_return(command_list, command, channel, user="", output=False):
    ps = subprocess.run(command_list, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    if ps.returncode is not 0:
        response = command + ' raise exception: ' + str(ps.returncode)
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        logging.error(response + " " + ps.stdout.decode(ENCODING, 'ignore'))
    else:
        logging.info("STDOUT: " + ps.stdout.decode(ENCODING, 'ignore'))

    if OUTPUT or output:
        slack_client.api_call("chat.postMessage", channel=channel, text=ps.stdout.decode(ENCODING, 'ignore'),
                as_user=True)
    else:
        slack_api_call("chat.postMessage", channel=channel, text=command + " Complete", as_user=True, user=user)

    if DEBUG_CHANNEL:
        slack_client.api_call("chat.postMessage", channel=DEBUG_CHANNEL, text=ps.stdout.decode(ENCODING, 'ignore'),
                as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and output['text'].startswith(AT_BOT):
                return output['text'].split(AT_BOT)[1].strip(), output['channel'], output['user']
    return None, None, None

class Worker(object):
    name = "bot_worker"
    logging.basicConfig(level=logging.DEBUG, format='LINE %(lineno)-4d  %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M', filename=LOG_FILE, filemode='w')
    if slack_client and slack_client.rtm_connect():
        logging.info("Chat bot connected and running!")

    @timer(interval=READ_WEBSOCKET_DELAY)
    def command_working_proccesser(self):
        command, channel, user = parse_slack_output(slack_client.rtm_read())
        if command and channel:
            handle_command(command, channel, user)

    @timer(interval=60)
    def regular_job_processer(self):
        if JOBS_FOLDER and JOBS_CHANNEL:
            for dirpath, _, commands in walk(JOBS_FOLDER):
                if commands and datetime.now().minute % int(path.basename(dirpath)) == 0:
                    for command in commands:
                        print(dirpath, _, command)
                        print(datetime.now().minute, dirpath, path.basename(dirpath))
                        response = "executing " + command
                        logging.info(response)
                        slack_client.api_call("chat.postMessage", channel=JOBS_CHANNEL, text=response, as_user=True)

                        command_list = [c for c in command.strip().split() if not c.isspace()]
                        command_list[0] = path.join(dirpath, command_list[0])
                        run_command_and_return(command_list, command, JOBS_CHANNEL, output=True)

def main():
    runner = ServiceRunner(config={})
    runner.add_service(Worker)
    runner.start()
    try:
        runner.wait()
    except KeyboardInterrupt:
        runner.stop()
    pass


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
Configure file is missing or improper
type following command to copy a config file to current folder, or in ~/.config

$ antbot -c

or see the usage

$ antbot -h 

""")
        sys.exit(1)

    logging.debug('config load')
    main()

if __name__ == "__main__":
    cli()
