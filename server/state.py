# encoding=utf-8
"""
Global state of the server. Supports export/import of JSON files.

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
"""
import io
import json
from twisted.python import log
from server.version import __version__
from server.hosts import Hosts


class ServerState(object):
    """
    Load/save data and configuration from a JSON file.
    """
    def __init__(self):
        """
        Constructor.

        Create a mostly empty state.
        """
        self.filename = None
        self.server = dict()
        self.server['version'] = __version__
        self.hosts = Hosts()
        self.patterns = list()
        self.plugins = dict()

    def json_import(self, filename=None):
        """
        Import Site Check state from a JSON file.
        """
        if filename is None:
            filename = self.filename
        else:
            self.filename = filename

        with io.open(filename, 'r', encoding='utf-8') as json_file:
            json_data = json_file.read()
            if json_data != '':
                data = json.loads(json_data)

                self.server = data['server']
                self.hosts = Hosts(data['hosts'])
                self.patterns = data['patterns']
                self.plugins = data['plugins']
            else:
                log.err('Empty JSON data file.')

        json_file.close()

    def json_export(self, filename=None):
        """
        Export Site Status state to a JSON file.
        """
        if filename is None:
            filename = self.filename
        else:
            self.filename = filename

        with io.open(filename, 'w', encoding='utf-8') as json_file:
            data = dict()
            data['server'] = self.server
            data['hosts'] = self.hosts.get_dict_list()
            data['patterns'] = self.patterns
            data['plugins'] = self.plugins

            json_file.write(json.dumps(data,
                                       ensure_ascii=False,
                                       skipkeys=True,
                                       indent=4,
                                       sort_keys=True))

        json_file.close()
