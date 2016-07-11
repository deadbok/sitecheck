# encoding=utf-8
'''
Created on 11/06/2016

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
'''
import json
from server.host import Host


class Hosts:
    """
    List of servers to check.
    """

    def __init__(self, hosts=None, patterns=None):
        """
        Constructor.
        """
        self.patterns = patterns
        self.hosts = dict()
        if hosts is not None:
            for host in hosts:
                self.add(host_dict=host)
        if self.patterns is not None:
            self.patterns.register_add_listener(self.on_added_pattern)

    def add(self, host='', host_dict=None):
        """
        Add host.
        """
        if (host != '') and (host_dict is None):
            self.hosts[host] = Host(host)
        elif (host == '') and (host_dict is not None):
            self.hosts[host_dict['name']] = Host(host_dict=host_dict)

    def add_by_names(self, hosts):
        """
        Add a list of host object.
        """
        for host in hosts:
            self.add(host=host)

    def remove(self, host='', host_dict=None):
        """
        Remove host.
        """
        if (host != '') and (host_dict is None):
            del self.hosts[host]
        elif (host == '') and (host_dict is not None):
            del self.hosts[host_dict.name]

    def remove_by_names(self, hosts):
        """
        Remove a list of host object.
        """
        for host in hosts:
            self.remove(host=host)

    def get_dict_list(self):
        """
        Get a list of all host data-
        """
        hosts = list()
        for host in self.hosts.values():
            hosts.append(host.get_dict())

        return hosts

    def ping(self, host):
        """
        Ping a named host.
        """
        if host in self.hosts.keys():
            self.hosts[host].ping()

    def diff(self, host):
        """
        Diff a named host.
        """
        if host in self.hosts.keys():
            self.hosts[host].diff_index_page()
            if len(self.patterns.patterns):
                self.hosts[host].match_scan(self.patterns.patterns.values())

    def send(self, host, state, protocol):
        """
        Send a named host.
        """
        if host in self.hosts.keys():
            self.hosts[host].send(state, protocol)

    def send_removed(self, host, state, protocol):
        """
        Send removed message for a host.
        """
        response = dict()
        response['version'] = state.server['version']
        response['total'] = len(self.hosts)
        response['type'] = 'host'
        response['length'] = -1
        response['data'] = [host]
        protocol.sendMessage(json.dumps(response).encode('utf-8'), False)

    def on_added_pattern(self, pattern):
        """
        Run a new pattern oń existing diffs.
        """
        for host in self.hosts.keys():
            self.hosts[host].match_scan([pattern])
