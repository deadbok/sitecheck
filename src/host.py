# encoding=utf-8
'''
Created on 11/06/2016

:copyright: (c) 2016 by Martin Grønholdt.
:license: GPLv3, see LICENSE for more details.
'''
import json
from commands import get_simple_cmd_output


class Host(object):
    """
    List of servers to check.
    """

    def __init__(self, host):
        """
        Constructor.
        """
        self.name = host
        self.alive = None
        self.ip = None
        self.replyHost = None
        self.time = None

    def getDict(self):
        host = dict()
        host['name'] = self.name
        host['alive'] = self.alive
        host['ip'] = self.ip
        host['replyHost'] = self.replyHost
        host['time'] = self.time
        return(host)

    def getJSON(self):
        return(json.encoder(self))

    def ping(self):
        """
        Ping the host and extract status from the command.
        """
        print("Pinging " + host.strip())
        # ping command
        cmd = "ping -c 1 " + host.strip()
        # Run
        res = get_simple_cmd_output(cmd)

        if res[0] == 0:
            self.alive = True
        else:
            self.alive = False

        host_re = re.compile(host_regexp)
        re_host = host_re.search(res[1])
        if re_host is not None:
            self.replyHost = re_host.group(1)
        else:
            self.replyHost = "Unknown"

        ip_re = re.compile(ip_regexp)
        ip = ip_re.search(res[1])
        if ip is not None:
            self.ip = ip.group()
        else:
            self.ip = "Unknown"

