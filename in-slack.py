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
import shlex
import socket
import urllib2
import argparse
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
    elif val == 'True' or val == 'true':
      settings[key] = True
    elif val == 'False' or val == 'false':
      settings[key] = False
    else:
      settings[key] = val


## Verify settings
if settings['INSLACK_WEBHOOK_URL'] == False:
  print('INSLACK_WEBHOOK_URL is unset!')
  sys.exit(1)


## Parse user input
command = sys.argv[1:]
if command[0].startswith('-'):  ## Assuming you want inline options
  parser = argparse.ArgumentParser(description='Command line utility for sending STDOUT to Slack')
  parser.add_argument('--command',  '-c', action="store", dest="command",  default=False, help='Command to be executed', nargs='*')
  parser.add_argument('--username', '-U', action="store", dest="username", default=None,  help='Slack Username to use [%s]'%(str(settings['INSLACK_USERNAME'])))
  parser.add_argument('--channel',  '-C', action="store", dest="channel",  default=None,  help='Channel to post to [%s]'%(str(settings['INSLACK_CHANNEL'])))
  parser.add_argument('--url',      '-u', action="store", dest="url",      default=None,  help='Slack webhook url [%s]'%(str(settings['INSLACK_WEBHOOK_URL'])))
  parser.add_argument('--emoji',    '-e', action="store", dest="emoji",    default=None,  help='Emoji icon to post with [%s]'%(str(settings['INSLACK_ICON_EMOJI'])))
  parser.add_argument('--compound', '-n', action="store", dest="compound", default=None,  help='Number of lines to compound per post [%s]'%(str(settings['INSLACK_COMPOUND'])))
  parser.add_argument('--style',    '-s', action="store", dest="style",    default=None,  help='Style (code) of post [%s]'%(str(settings['INSLACK_STYLE'])))
  results = parser.parse_args()
  if not results.command:
    print('No command specified! (use -c)')
    sys.exit(1)
  command = results.command
  if not results.username == None:
    settings['INSLACK_USERNAME'] = results.username
  if not results.url == None:
    settings['INSLACK_WEBHOOK_URL'] = results.url
  if not results.channel == None:
    settings['INSLACK_CHANNEL'] = results.channel
  if not results.emoji == None:
    if results.emoji.startswith(':'):
      settings['INSLACK_ICON_EMOJI'] = results.emoji
    else:
      settings['INSLACK_EMOJI_ICON'] = ':%s:'%(results.emoji)
  if not results.compound == None:
    settings['INSLACK_COMPOUND'] = int(results.compound)
  if not results.style == None:
    settings['INSLACK_STYLE'] = results.style


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
  run(command)
