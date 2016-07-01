# encoding=utf-8
'''
Created on 11/06/2016

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
'''
import os.path
import re
from datetime import datetime
from twisted.python import log

from commands import get_simple_cmd_output


IP_REGEXP = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
HOST_REGEXP = r'from\s((\w+\.)+\w+)\s+'


def time_stamp(in_datetime, epoch=datetime(1970, 1, 1)):
    unix_time = in_datetime - epoch
    return (unix_time.microseconds + (unix_time.seconds + unix_time.days * 86400) * 10 ** 6) / 10 ** 6


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
            self.state = 'neutral'
            self.state_msg = 'None'
            self.ipaddr = None
            self.replyHost = None
            self.time = 0
            self.diff = ''
            self.msgs = []
        elif (host == '') and (host_dict is not None):
            self.from_dict(host_dict)

    def get_dict(self):
        host = dict()
        host['name'] = self.name
        host['state'] = self.state
        host['state_msg'] = self.state_msg
        host['ip'] = self.ipaddr
        host['replyHost'] = self.replyHost
        host['time'] = self.time
        host['diff'] = self.diff
        host['msgs'] = self.msgs
        return host

    def from_dict(self, host_dict):
        """
        Set values from a dictionary.
        """
        self.name = host_dict['name']
        self.state = host_dict['state']
        if 'state_msg' in host_dict.keys():
            self.state_msg = host_dict['state_msg']
        else:
            self.state_msg = 'None'
        self.ipaddr = host_dict['ip']
        self.replyHost = host_dict['replyHost']
        self.time = host_dict['time']
        if 'diff' in host_dict.keys():
            self.diff = host_dict['diff']
        else:
            self.diff = ''
        if 'msgs' in host_dict.keys():
            self.msgs = host_dict['msgs']
        else:
            self.msgs = []

    def ping(self):
        """
        Ping the host and extract status from the command.
        
        @todo: Generate sane output when command fails.
        """
        # ping command
        cmd = "ping -c 1 " + self.name.strip()
        # Run
        res = get_simple_cmd_output(cmd)

        log.msg('Ping output: ' + res[1])

        if res[0] == 0:
            self.state_msg = 'Ping response'
            self.state = 'good'
        else:
            self.state = 'bad'
            self.state_msg = 'No answer'

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

        self.time = time_stamp(datetime.utcnow())

    def diff_index_page(self):
        """
        Diff /index.html of the host with last copy.
        
        @todo: Generate sane output when command fails.
        """
        # curl command
        cmd = "curl -s -L " + self.name.strip()
        # Run
        res = get_simple_cmd_output(cmd)
        if res[0] == 0:
            self.state_msg = 'Index response'
            self.state = 'good'
        else:
            self.state = 'bad'
            self.state_msg = 'No answer'

        index_file_name = "sites/" + self.name + "-index.html"
        # Rename the old one if it is there
        if os.path.isfile(index_file_name):
            os.rename(index_file_name, index_file_name + ".old")

        # Save new index.html
        index_file = open(index_file_name, "w")
        if index_file is not None:
            index_file.write(res[1])
            index_file.close()
        else:
            log.err("Could not write: " + index_file_name)

        if os.path.isfile(index_file_name + ".old"):
            log.msg("Diffing: " + index_file_name)
            # diff command
            cmd = "diff -u1 " + index_file_name + ".old " + index_file_name
            # Run
            res = get_simple_cmd_output(cmd)
            if res[0] > 1:
                self.state = 'bad'
                self.state_msg = 'Index diff failed'

            self.diff = res[1]
            if self.diff != '':
                self.state = 'neutral'
                self.state_msg = 'Index changed'
        else:
            self.diff = "No old index"
            self.state = 'neutral'
            self.state_msg = 'No previous index'

        self.time = time_stamp(datetime.utcnow())

    def match_scan(self, patterns):
        """
        Find matches in the index diff.
        """
        log.msg('Scanning diff for patterns.')
        self.msgs = []
        for pattern in patterns:
            for line in self.diff.split('\n'):
                matches = pattern.match(line)
                if len(matches.matches) > 0:
                    self.msgs.append(matches.get_dict())
                    for match in matches.matches:
                        if (((self.state == 'good') or
                            (self.state == 'neutral')) and
                            ((match.score == 'neutral') or
                             (match.score == 'bad'))):
                            self.state = match.score

