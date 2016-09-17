AntBot
---
a slack bot doing simple script jobs
> a slack bot can execute commands by slack chat room ( @bot_name: command ), 
> wherein these commands are specified in a folder.



Usage
---
start a bot
- `antbot -c` to copy the config file to current folder
- add your bot key into config file
- `antbot` to run the bot  

use in slack
- `@bot_name: help` to show the command can be executed by the bot
- `@bot_name: command` to execute that command

help
- `antbot -h` for help

Configure
---
please set up at least following parameters in config file as ant.conf (in working folder or in ~/.config);
or set up as environment parameters: 
- BOT_ID or BOT_NAME
- SLACK_BOT_TOKEN (api key provided by slack)
- SCRIPTS_FOLDER (script job you want to provide, default is current folder)

**Other not parameters can be set in config file**

Environment
---
- python 3.5
- slackclient 

Change Log
---
Version 0.0.1
- basic bot

Version 0.0.3
- command line document
- copy config example
- show command execution output to slack (optional)

Version 0.0.4
- fix the bug on STDOUT encoding
- Parameter patching rull ./ant.conf > ~/.ant.conf > environment parameters

Version 0.0.6
- fix the requirement


MIT Licence
---
Copyright (c) 2016 Antonio Yang (yanganto) Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
