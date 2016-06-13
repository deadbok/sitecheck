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


class HostList(object):
    """
    List of servers to check.
    """

    def __init__(self, name):
        """
        Constructor.
        """
        self.name = name
        self.filename = name.strip() + '.json'
        self.hosts = list()
        if not os.path.isfile(self.filename):
            self.saveJSON()

    def loadJSON(self):
        """
        Load host data from a JSON formatted text file.
        """
        with io.open(self.filename, 'r', encoding='utf-8') as json_file:
            self.host = json.decoder(unicode(json_file.read()))
        json_file.close()

    def saveJSON(self):
        """
        Save host data to a JSON formatted text file.
        """
        with io.open(self.filename, 'w', encoding='utf-8') as json_file:
            json_file.write(unicode(json.dumps([host.getDict() for host in self.hosts],
                                               ensure_ascii=False,
                                               skipkeys=True), 'utf-8'))

        json_file.close()

    def addHosts(self, hosts):
        for host in hosts:
            self.hosts.append(Host(host))

    def getHostList(self):
        names = list()
        for host in self.hosts:
            names.append(host.name)

        return(names)

    def getJSON(self):
        return json.encoder(self.hosts)
