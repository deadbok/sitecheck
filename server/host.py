# encoding=utf-8
'''
Created on 11/06/2016

:copyright: (c) 2016 by Martin Grønholdt.
:license: GPLv3, see LICENSE for more details.
'''
import re
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
        if (host != '') and (host_dict is None):
            self.name = host
            self.state = 'None'
            self.ipaddr = None
            self.replyHost = None
            self.time = 0
        elif (host == '') and (host_dict is not None):
            self.from_dict(host_dict)

    def time_stamp(self, in_datetime, epoch=datetime(1970, 1, 1)):
        unix_time = in_datetime - epoch
        return (unix_time.microseconds + (unix_time.seconds + unix_time.days * 86400) * 10 ** 6) / 10 ** 6

    def get_dict(self):
        host = dict()
        host['name'] = self.name
        host['state'] = self.state
        host['ip'] = self.ipaddr
        host['replyHost'] = self.replyHost
        host['time'] = self.time
        return host

    def from_dict(self, host_dict):
        """
        Set values from a dictionary.
        """
        self.name = host_dict['name']
        self.state = host_dict['state']
        self.ipaddr = host_dict['ip']
        self.replyHost = host_dict['replyHost']
        self.time = host_dict['time']

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
            self.state = 'Ping response'
        else:
            self.state = 'No answer'

        host_re = re.compile(HOST_REGEXP)
        re_host = host_re.search(res[1])
        if re_host is not None:
            self.replyHost = re_host.group(1)
        else:
            self.replyHost = "Unknown"

        ip_re = re.compile(IP_REGEXP)
        ip_addr = ip_re.search(res[1])
        if ip_addr is not None:
            self.ipaddr = ip_addr.group()
        else:
            self.ipaddr = "Unknown"

        self.time = self.time_stamp(datetime.utcnow())
