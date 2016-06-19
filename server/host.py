# encoding=utf-8
'''
Created on 11/06/2016

:copyright: (c) 2016 by Martin Grønholdt.
:license: GPLv3, see LICENSE for more details.
'''
import re
import json
from datetime import datetime
from twisted.python import log
from commands import get_simple_cmd_output

IP_REGEXP = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
HOST_REGEXP = r'from\s((\w+\.)+\w+)\s+'


class Host(object):
    """
    List of servers to check.
    """

    def __init__(self, host='', host_dict=None):
        """
        Constructor.
        """
        if ((host != '') and (host_dict is None)):
            self.name = host
            self.alive = None
            self.ip = None
            self.replyHost = None
            self.time = 'Never'
        elif ((host == '') and (host_dict is not None)):
            self.fromDict(host_dict)

    def timeStamp(self, dt, epoch=datetime(1970, 1, 1)):
        td = dt - epoch
        return (td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6) / 10 ** 6

    def getDict(self):
        host = dict()
        host['name'] = self.name
        host['alive'] = self.alive
        host['ip'] = self.ip
        host['replyHost'] = self.replyHost
        host['time'] = self.time
        return(host)

    def fromDict(self, host_dict):
        """
        Set values from a dictionary.
        """
        self.name = host_dict['name']
        self.alive = host_dict['alive']
        self.ip = host_dict['ip']
        self.replyHost = host_dict['replyHost']
        self.time = host_dict['time']

    def getJSON(self):
        return(json.encoder(self))

    def ping(self):
        """
        Ping the host and extract status from the command.
        """
        # ping command
        cmd = "ping -c 1 " + self.name.strip()
        # Run
        res = get_simple_cmd_output(cmd)

        log.msg('Ping output: ' + res[1])

        if res[0] == 0:
            self.alive = True
        else:
            self.alive = False

        host_re = re.compile(HOST_REGEXP)
        re_host = host_re.search(res[1])
        if re_host is not None:
            self.replyHost = re_host.group(1)
        else:
            self.replyHost = "Unknown"

        ip_re = re.compile(IP_REGEXP)
        ip = ip_re.search(res[1])
        if ip is not None:
            self.ip = ip.group()
        else:
            self.ip = "Unknown"

        self.time = self.timeStamp(datetime.utcnow())

