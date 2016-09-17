AntBot
---
a slack bot doing simple script jobs

Usage
---
- `antbot -c` to copy the config file to current folder
- `antbot` to run the bot
- `antbot -h` for help

Config
---
please set up following parameters in config file as ant.conf (in working folder or in ~/.config);
or set up as environment parameters: 
- BOT_ID (you can skip if BOT_NAME is set)
- BOT_NAME
- SLACK_BOT_TOKEN (api key provided by slack)
- SCRIPTS_FOLDER (script job you want to provide)
- LOG_FILE

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


MIT Licence
---
Copyright (c) 2016 Antonio Yang (yanganto) Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
