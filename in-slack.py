#!/usr/bin/python
#
#   in-slack is a command line tool used to send STDOUT to slack.
#
#      Example
# in-slack cat /etc/hosts
#
#   Example settings:
# export INSLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxxxxxxxx/xxxxxxxxx/xxxxxxxxxxxxxxxxxxxxxxxx
# export INSLACK_CHANNEL=#general
# export INSLACK_SHOW_COMMAND=true
# export INSLACK_COMPOUND=25
# export INSLACK_STYLE=false
# export INSLACK_ICON_EMOJI=:construction:
# export INSLACK_USERNAME=`hostname`


## Imports
import os
import sys
import pwd
import json
import socket
import urllib2
from subprocess import Popen, PIPE, STDOUT


## Default settings
settings = {
  'INSLACK_WEBHOOK_URL':  False,
  'INSLACK_CHANNEL':      '#general',
  'INSLACK_SHOW_COMMAND': True,
  'INSLACK_COMPOUND':     25,
  'INSLACK_STYLE':        'code',
  'INSLACK_ICON_EMOJI':   ':computer:',
  'INSLACK_USERNAME':     '%s@%s'%(pwd.getpwuid(os.getuid())[0],socket.gethostname())
}


## Load settings
for key in os.environ:
  if key.startswith('INSLACK_'):
    val = os.environ[key]
    if val.isdigit():
      settings[key] = int(val)
    elif val == 'True' or val == 'true' or val == 'False' or val == 'false':
      settings[key] = bool(val)
    else:
      settings[key] = val


## Verify settings
if settings['INSLACK_WEBHOOK_URL'] == False:
  print('INSLACK_WEBHOOK_URL is unset!')
  sys.exit(1)


## Send a string to slack
def sendtoslack(text,url=settings['INSLACK_WEBHOOK_URL'],username=settings['INSLACK_USERNAME'],channel=settings['INSLACK_CHANNEL'],icon_emoji=settings['INSLACK_ICON_EMOJI']):
  values = {}
  values['text'] = text
  values['username'] = username
  values['channel'] = channel
  values['icon_emoji'] = icon_emoji
  data = json.dumps(values)
  req = urllib2.Request(url, data)
  response = urllib2.urlopen(req)
  the_page = response.read()


## Run a command
def run(command,show_command=settings['INSLACK_SHOW_COMMAND'],compound=settings['INSLACK_COMPOUND'],style=settings['INSLACK_STYLE']):
  if show_command: sendtoslack('`%s`'%(' '.join(command)))
  line_count = 0
  buff = ''
  proc = Popen(command, bufsize=1, stdout=PIPE, stderr=STDOUT, close_fds=True)
  for line in iter(proc.stdout.readline, b''):
    buff += line
    line_count += 1
    if compound:
      if (line_count % compound) == 0:
        text = buff
        if style == 'code':
          text = '```%s```'%(text)
        sendtoslack(text)
        print(buff)
        buff = ''
    else:
      text = buff
      print(text)
      sendtoslack(text)
  proc.stdout.close()
  proc.wait()
  if compound:
    text = buff
    if style == 'code':
      text = '```%s```'%(text)
    if not text == '``````':
      sendtoslack(text)
      print(buff)
      buff = ''



## Main
if __name__ == "__main__":
  run(sys.argv[1:])
