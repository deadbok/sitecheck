# encoding=utf-8
'''
Created on 11/06/2016

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
'''
from server.host import Host
from server.pattern import Pattern


class Hosts:
    """
    List of servers to check.
    """

    def __init__(self, hosts=None):
        """
        Constructor.
        """
        self.hosts = dict()
        if hosts is not None:
            for host in hosts:
                self.add_host(host_dict=host)

    def add_host(self, host='', host_dict=None):
        """
        Add host.
        """
        if (host != '') and (host_dict is None):
            self.hosts[host] = Host(host)
        elif (host == '') and (host_dict is not None):
            self.hosts[host_dict['name']] = Host(host_dict=host_dict)

    def add_hosts_by_name(self, hosts):
        """
        Add a list of host object.
        """
        for host in hosts:
            self.add_host(host=host)

    def remove_host(self, host='', host_dict=None):
        """
        Remove host.
        """
        if (host != '') and (host_dict is None):
            del self.hosts[host]
        elif (host == '') and (host_dict is not None):
            del self.hosts[host_dict.name]

    def remove_hosts_by_name(self, hosts):
        """
        Remove a list of host object.
        """
        for host in hosts:
            self.remove_host(host=host)

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
            self.hosts[host].match_scan([Pattern('captcha', True)])
