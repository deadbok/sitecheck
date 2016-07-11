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
from server.patterns import Patterns


class ServerState():
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
        self.server['msg'] = ''
        self.server['msg_state'] = 'neutral'
        self.patterns = Patterns()
        self.hosts = Hosts(patterns=self.patterns)
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

                # self.server = data['server']
                self.patterns = Patterns(data['patterns'])
                self.hosts = Hosts(data['hosts'], self.patterns)
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
            data['patterns'] = self.patterns.get_dict_list()
            data['plugins'] = self.plugins

            json_file.write(json.dumps(data,
                                       ensure_ascii=False,
                                       skipkeys=True,
                                       indent=4,
                                       sort_keys=True))

        json_file.close()

    def send_info(self, dummy, state, protocol):
        """
        Send server info message.
        """
        response = dict()
        response['version'] = state.server['version']
        response['total'] = len(self.hosts.hosts)
        response['type'] = 'host'
        response['length'] = 0
        response['data'] = []
        protocol.sendMessage(json.dumps(response).encode('utf-8'), False)

    def send_empty(self, stype, state, protocol):
        """
        Send empty message..
        """
        response = dict()
        response['version'] = state.server['version']
        response['total'] = len(self.__dict__[stype + 's'].__dict__[stype + 's'])
        response['type'] = stype
        response['length'] = 0
        response['data'] = []
        protocol.sendMessage(json.dumps(response).encode('utf-8'), False)
