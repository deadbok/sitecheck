# coding=utf-8
'''
Created on 06/06/2016

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
'''
from subprocess import Popen, PIPE
import shlex
import locale

ENCODING = locale.getdefaultlocale()[1]


def get_simple_cmd_output(cmd):
    """
    Execute an external command and get its output.
    """
    # Split the command and arguments
    args = shlex.split(cmd)
    # Return everything from stdout
    ret = Popen(args, stdout=PIPE)
    # Convert to string
    ret_out = ret.communicate()[0].decode(ENCODING)

    return(ret.returncode, ret_out)
