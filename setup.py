#!/usr/bin/env python
import os
import sys
from distutils.core import setup

## Globals
here = os.path.dirname(os.path.realpath(__file__))
install_file = '/usr/bin/in-slack'

setup(name='Distutils',
  version='1.0',
  description='A command line utility to send STDOUT to Slack',
  author='Josiah Kerley',
  author_email='josiahkerley@gmail.com',
  url='https://github.com/JosiahKerley/in-slack',
)


## Copy
if 'install' in sys.argv:
  with open('%s/in-slack.py'%(here),'r') as f:
    file_content = f.read()
  with open(install_file,'w') as f:
    f.write(file_content)
  os.system('chmod +x "%s"'%(install_file))
