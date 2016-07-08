# encoding=utf-8
"""
Main Site Check WebSockets server routines.

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
"""


import json
from queue import Queue
from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.websocket import WebSocketServerFactory
from twisted.python import log

QUEUE = Queue()


class SiteStatusProtocol(WebSocketServerProtocol):
    """
    Server side implementation of the WebSocket protocol.
    """
    def __init__(self, factory):
        self.factory = factory

    def _init_response(self):
        """
        Create a response dictionary with standard fields populated.
        """
        response = dict()
        response['version'] = self.factory.state.server['version']
        response['total_hosts'] = len(self.factory.state.hosts.hosts)
        response['hosts'] = list()
        return response

    def send_hosts(self, hosts):
        """
        Send the complete data set for a list of hosts.
        """
        response = self._init_response()
        for host in hosts.values():
            response['hosts'].append(host.get_dict())
            # Split in packages of 10
            if len(response['hosts']) == 10:
                response['length'] = len(response['hosts'])
                self.sendMessage(json.dumps(response).encode('utf-8'), False)
                response['hosts'] = list()
        # Send the rest
        if (len(response['hosts']) < 10) and (len(response['hosts']) > 0):
            response['length'] = len(response['hosts'])
            self.sendMessage(json.dumps(response).encode('utf-8'), False)
        elif len(response['hosts']) == 0:
            response['length'] = 0
            self.sendMessage(json.dumps(response).encode('utf-8'), False)

    def send_hosts_by_name(self, hosts):
        """
        Send the complete data set for a list of host names.
        """
        response = self._init_response()
        for host in hosts:
            server_hosts = self.factory.state.hosts.hosts
            if host in server_hosts.keys():
                response['hosts'].append(server_hosts[host].get_dict())
                # Split in packages of 10
                if len(response) == 10:
                    response['length'] = len(response['hosts'])
                    self.sendMessage(json.dumps(response).encode('utf-8'),
                                     False)
                    response['hosts'] = list()
        # Send the rest
        if (len(response) < 10) and (len(response) > 0):
            response['length'] = len(response['hosts'])
            self.sendMessage(json.dumps(response).encode('utf-8'), False)
        elif len(response['hosts']) == 0:
            response['length'] = 0
            self.sendMessage(json.dumps(response).encode('utf-8'), False)

    def send_removed_hosts_by_name(self, hosts):
        """
        Send the host names for a list of removed host names.
        """
        response = self._init_response()
        response['length'] = -len(hosts)
        response['hosts'] = hosts
        self.sendMessage(json.dumps(response).encode('utf-8'), False)

    def get(self, hosts):
        """
        Get data for a list of host names. `*` for all.
        """
        if hosts[0] == '*':
            self.send_hosts(self.factory.state.hosts.hosts)
        else:
            self.send_hosts_by_name(hosts)

    def diff(self, hosts):
        """
        Run a diff on current and last index on a list of hosts.
        """
        for host in hosts:
            log.msg('Host: ' + host)
            QUEUE.put((host, self.factory.state.hosts.diff,
                       self.send_hosts_by_name))

    def ping(self, hosts):
        """
        Ping a list of hosts.
        """
        for host in hosts:
            log.msg('Host: ' + host)
            QUEUE.put((host, self.factory.state.hosts.ping,
                       self.send_hosts_by_name))

    def add(self, hosts):
        """
        Add a list of hosts.
        """
        log.msg('Adding: ' + str(hosts))
        for host in hosts:
            if host != '':
                QUEUE.put((host, self.factory.state.hosts.add_host,
                           self.send_hosts_by_name))

    def remove(self, hosts):
        """
        Remove a list of hosts.
        """
        log.msg('Removing: ' + str(hosts))
        for host in hosts:
            if host != '':
                QUEUE.put((host, self.factory.state.hosts.remove_host,
                           self.send_removed_hosts_by_name))

    message_handlers = {'get': {'host': get, 'pattern': None},
                        'diff': {'host': diff, 'pattern': None},
                        'ping': {'host': ping, 'pattern': None},
                        'add': {'host': add, 'pattern': None},
                        'remove': {'host': remove, 'pattern': None}}

    def onMessage(self, payload, isBinary):
        """
        Handle request for host actions.
        """
        if isBinary:
            log.msg('Binary message received and discarded.')
            return

        log.msg(payload.decode('utf8'))
        msg = json.loads(payload.decode('utf8'))
        log.msg('Action: ' + msg['action'])
        if msg['action'] in self.message_handlers.keys():
            if self.message_handlers[msg['action']][msg['type']] is not None:
                self.message_handlers[msg['action']][msg['type']](self,
                                                                  msg['param'])
            else:
                self.factory.state.config['msg'] = ('Unknown action "' +
                                                    msg['action'] +
                                                    '" on type "' +
                                                    msg['type'])
                self.factory.state.config['msg_state'] = 'bad'
                log.err(self.factory.state.config['msg'])
        else:
            self.factory.state.config['msg'] = ('Unknown action "' +
                                                msg['action'] +
                                                '" on type "' +
                                                msg['type'])
            self.factory.state.config['msg_state'] = 'bad'
            log.err(self.factory.state.config['msg'])

        # Process the queue.
        QUEUE.join()

        self.factory.state.json_export()


class SiteStatusFactory(WebSocketServerFactory):
    """
    Factory to a SiteStatus servers and make a JSON files data available.
    """

    protocol = SiteStatusProtocol

    def __init__(self, wsuri, state):
        WebSocketServerFactory.__init__(self, wsuri)
        self.state = state

    def buildProtocol(self, addr):
        """
        Create an instance of a subclass of Protocol.
        """
        # pylint: disable=unused-argument
        protocol = self.protocol(self)
        return protocol
