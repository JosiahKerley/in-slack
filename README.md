About
=====
in-slack is a command line tool used to send STDOUT to slack.

Usage
=====

Simple:
```
in-slack cat /etc/hosts
```

Advanced:
```
usage: in-slack.py [-h] [--command [COMMAND [COMMAND ...]]]
                   [--username USERNAME] [--channel CHANNEL] [--url URL]
                   [--emoji EMOJI] [--compound COMPOUND] [--style STYLE]

Command line utility for sending STDOUT to Slack

optional arguments:
  -h, --help            show this help message and exit
  --command [COMMAND [COMMAND ...]], -c [COMMAND [COMMAND ...]]
                        Command to be executed
  --username USERNAME, -U USERNAME
                        Slack Username to use
  --channel CHANNEL, -C CHANNEL
                        Channel to post to
  --url URL, -u URL     Slack webhook url
  --emoji EMOJI, -e EMOJI
                        Emoji icon to post with
  --compound COMPOUND, -n COMPOUND
                        Number of lines to compound per post
  --style STYLE, -s STYLE
                        Style (code) of post
```

Settings:

```
export INSLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxxxxxxxx/xxxxxxxxx/xxxxxxxxxxxxxxxxxxxxxxxx
export INSLACK_CHANNEL=#general
export INSLACK_SHOW_COMMAND=true
export INSLACK_COMPOUND=25
export INSLACK_STYLE=false
export INSLACK_ICON_EMOJI=:computer:
export INSLACK_USERNAME=`hostname`
```
