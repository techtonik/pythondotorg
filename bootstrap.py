#!/usr/bin/env python3
"""
Bootstrap script to get development environment on Windows.

 * [x] check Python 3
   * [ ] locate Python 3
 * [x] check virtualenv is installed
   * [ ] install if it is not installed
   * [ ] download and run locally
 * [x] create virtualenv in .virtenv
   * [ ] write description to .virtenv/README.md
 * [x] install requirements
 * [x] create manage.bat


The code is placed into public domain by
   anatoly techtonik <techtonik@gmail.com>

"""

# --- imports ---

import platform
import sys

# --- constants ---

PY3K = sys.version_info >= (3, 0)
ISWIN = platform.system() == 'Windows'
VDIR = '.virtenv/'

# --- helpers ---

# --[inline shellrun 2.0 import run]
import subprocess

class Result(object):
    def __init__(self, command=None, retcode=None, output=None):
        self.command = command or ''
        self.retcode = retcode
        self.output = output
        self.success = False
        if retcode == 0:
            self.success = True

def run(command):
    process = subprocess.Popen(command, shell=True)
    process.communicate()
    return Result(command=command, retcode=process.returncode)
# --[/inline]

if PY3K:
    interpreter = sys.executable
else:
    # [ ] try to detect Python 3
    sys.exit('This project only works with Python 3.')

print('--- creating virtualenv in .virtenv/ subdir ---')
if not run(interpreter + " -m virtualenv .virtenv").success:
    print('Error running virtualenv..')
    input('Press Enter to install virtualenv, Ctrl-C to quit..')
    if not run(interpreter + " -m pip install virtualenv").success:
        print('Error instlling virtualenv..')
        input('Press Enter to quit..')
        sys.exit(-1)
    if not run(interpreter + " -m virtualenv .virtenv").success:
        print('Error running virtualenv..')
        input('Press Enter to quit..')
        sys.exit(-1)


if ISWIN:
    interpreter = '.virtenv\\Scripts\\python.exe'
else:
    interpreter = '.virtenv/bin/python'
    

print('--- installing requirements ---')

if not run(interpreter + ' -m pip install -r requirements.txt').success:
    sys.exit('Error installing requirements.txt')


print('--- writing manage.bat file ---')
batfile = """\
@rem Autogenerated by bootstrap.py script.

@echo off
"{python}" manage.py %*
""".format(
  python=interpreter,
)
open('manage.bat', 'w').write(batfile)
input('Done. Press Enter..')
