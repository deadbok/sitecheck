# encoding=utf-8
'''
Created on 11/06/2016

:copyright: (c) 2016 by Martin Grønholdt.
:license: GPLv3, see LICENSE for more details.
'''
import io
import json
import os.path
from host import Host


class Hosts(object):
    """
    List of servers to check.
    """

    def __init__(self, name):
        """
        Constructor.
        """
        self.name = name
        self.filename = name.strip() + '.json'
        self.hosts = dict()
        if not os.path.isfile(self.filename):
            self.saveJSON()
        else:
            self.loadJSON()

    def loadJSON(self):
        """
        Load host data from a JSON formatted text file.
        """
        with io.open(self.filename, 'r', encoding='utf-8') as json_file:
            json_hosts = json_file.read()
            if json_hosts != '':
                json_hosts = json.loads(json_hosts)
                for json_host in json_hosts:
                    self.hosts[json_host['name']] = Host(host_dict=json_host)

        json_file.close()

    def saveJSON(self):
        """
        Save host data to a JSON formatted text file.
        """
        with io.open(self.filename, 'w', encoding='utf-8') as json_file:
            json_file.write(json.dumps([host.get_dict() for host in self.hosts.values()],
                                       ensure_ascii=False,
                                       skipkeys=True))

        json_file.close()

    def addHost(self, host='', host_dict=None):
        """
        Add host.
        """
        if ((host != '') and (host_dict is None)):
            self.hosts[host] = Host(host)
        elif ((host == '') and (host_dict is not None)):
            self.hosts[host] = Host(host_dict=host_dict)

    def addHosts(self, hosts):
        for host in hosts:
            self.addHost(host=host)

    def addHostDicts(self, dicts):
        """
        Add hosts from a list of dictionaries.
        """
        for host_dict in dicts:
            self.addHost(host_dict=host_dict)

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
