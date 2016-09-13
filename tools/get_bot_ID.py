"""
python3 get_bot_ID.py <bot_name> <API_token>
    example
        <bot_name> ant
        <API_token> xoxb-xxxxxxxxxxx-xxxxxxxxxxxxxxx
"""
import os, sys
from slackclient import SlackClient


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(__doc__)
        sys.exit(0)
    BOT_NAME = sys.argv[1]
    slack_client = SlackClient(sys.argv[2])
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
    else:
        print("could not find bot user with the name " + BOT_NAME)