"""
    A slack chat bot doing  scripts
"""

import time
import subprocess
import logging
from os import path

from slackclient import SlackClient

from antbot import SLACK_BOT_TOKEN, BOT_ID, SCRIPTS_FOLDER, COMMANDS, LOG_FILE

AT_BOT = "<@" + BOT_ID + ">:"

slack_client = SlackClient(SLACK_BOT_TOKEN)


def handle_command(command, channel):
    """
        Receives commands and execute the commands in SCRIPTS_FOLDER
    """
    cmd = command.strip().split()[0]
    if cmd.lower().startswith('help'):
        response = "I can execute following scripts, please specify\n" + ", ".join(COMMANDS)
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

    elif cmd in COMMANDS:
        response = "executing " + command
        logging.info(response)
        slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

        ps = subprocess.run(path.join(SCRIPTS_FOLDER, command.strip()))
        if ps.returncode is not 0:
            response = command + ' raise exception: ' + str(ps.returncode)
            slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
            if ps.stdout:
                logging.error(response + " " + ps.stdout)
            if ps.stderr:
                logging.error(response + " " + ps.stderr)
        else:
            logging.info("STDOUT: " + ps.stdout)
    else:
        slack_client.api_call("chat.postMessage", channel=channel, as_user=True,
                              text="I don't know what you say, type *help* to know the commands")
        logging.info("UNHANDLE: " + command)


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
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']
    return None, None


def main():
    READ_WEBSOCKET_DELAY = 1
    logging.basicConfig(level=logging.DEBUG, format='LINE %(lineno)-4d  %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M', filename=LOG_FILE, filemode='w')
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

if __name__ == "__main__":
    main()
