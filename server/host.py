# encoding=utf-8
'''
Created on 11/06/2016

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
'''
import re
import json
import os.path
from datetime import datetime
from twisted.python import log

from server.commands import get_simple_cmd_output


IP_REGEXP = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
HOST_REGEXP = r'from\s((\w+\.)+\w+)\s+'


def time_stamp(in_datetime, epoch=datetime(1970, 1, 1)):
    """
    Create a UNIX timesptamp from a datetime object.
    """
    return (in_datetime - epoch).total_seconds()


class Host:
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
            self.reply_host = None
            self.time = 0
            self.diff = ''
            self.msgs = []
        elif (host == '') and (host_dict is not None):
            self.__dict__ = host_dict

    def get_dict(self):
        """
        Create a dictionary from the host data.
        """
        return self.__dict__

    def from_dict(self, host_dict):
        """
        Set values from a dictionary.
        """
        self.__dict__ = host_dict

    def ping(self):
        """
        Ping the host and extract status from the command.

        @todo: Generate sane output when the command fails.
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
            self.reply_host = re_host.group(1)
        else:
            self.reply_host = "Unknown"

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

        @todo: Generate sane output when the command fails.
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
        log.msg('Scanning ' + self.name + ' diff for patterns.')
        self.msgs = []
        for pattern in patterns:
            for line in self.diff.split('\n'):
                matches = pattern.match(line)
                if len(matches.matches) > 0:
                    self.msgs.append(matches.get_dict())
                    for match in matches.matches:
                        # Modify the global state of the host if things are
                        # getting worse.
                        if (((self.state == 'good') or
                             (self.state == 'neutral')) and
                            ((match['score'] == 'neutral') or
                             (match['score'] == 'bad'))):
                            self.state = match['score']

    def send(self, state, protocol):
        """
        Send the complete data set for this host.
        """
        response = dict()
        response['version'] = state.server['version']
        response['total'] = len(state.hosts.hosts)
        response['type'] = 'host'
        response['length'] = 1
        response['data'] = [self.get_dict()]
        protocol.sendMessage(json.dumps(response).encode('utf-8'), False)
