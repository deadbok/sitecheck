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

    def get_info(self, hosts):
        """
        Get server info.
        """
        # pylint: disable=unused-argument
        log.msg('Get server info.')
        QUEUE.put(('', None, self.factory.state.send_info,
                   self.factory.state, self))

    def get_hosts(self, hosts):
        """
        Get data for a list of host names. `*` for all.
        """
        if hosts[0] == '*':
            for host in self.factory.state.hosts.hosts.keys():
                log.msg('Get host: ' + host)
                QUEUE.put((host, None,
                           self.factory.state.hosts.send,
                           self.factory.state, self))
            if len(self.factory.state.hosts.hosts) == 0:
                self.factory.state.send_empty('host', self.factory.state,
                                              self)
        else:
            for host in hosts:
                log.msg('Get host: ' + host)
                QUEUE.put((host, None,
                           self.factory.state.hosts.send,
                           self.factory.state, self))

    def diff_hosts(self, hosts):
        """
        Run a diff on current and last index on a list of hosts.
        """
        for host in hosts:
            log.msg('Diff host: ' + host)
            QUEUE.put((host, self.factory.state.hosts.diff,
                       self.factory.state.hosts.send,
                       self.factory.state, self))

    def ping_hosts(self, hosts):
        """
        Ping a list of hosts.
        """
        for host in hosts:
            log.msg('Ping host: ' + host)
            QUEUE.put((host, self.factory.state.hosts.ping,
                       self.factory.state.hosts.send,
                       self.factory.state, self))

    def add_hosts(self, hosts):
        """
        Add a list of hosts.
        """
        log.msg('Adding: ' + str(hosts))
        for host in hosts:
            if host != '':
                QUEUE.put((host, self.factory.state.hosts.add,
                           self.factory.state.hosts.send,
                           self.factory.state, self))

    def remove_hosts(self, hosts):
        """
        Remove a list of hosts.
        """
        log.msg('Removing: ' + str(hosts))
        for host in hosts:
            if host != '':
                QUEUE.put((host, self.factory.state.hosts.remove,
                           self.factory.state.hosts.send_removed,
                           self.factory.state, self))

    def get_patterns(self, patterns):
        """
        Get data for a list of pattern names. `*` for all.
        """
        log.msg('Get patterns: ' + str(patterns))
        if patterns[0] == '*':
            for pattern in self.factory.state.patterns.patterns.keys():
                log.msg('Get pattern: ' + pattern)
                QUEUE.put((pattern, None,
                           self.factory.state.patterns.send,
                           self.factory.state, self))
            if len(self.factory.state.patterns.patterns) == 0:
                self.factory.state.send_empty('pattern', self.factory.state,
                                              self)
        else:
            for pattern in patterns:
                log.msg('Get pattern: ' + pattern)
                QUEUE.put((pattern, None,
                           self.factory.state.patterns.send,
                           self.factory.state, self))

    def add_patterns(self, patterns):
        """
        Add a list of patterns.
        """
        log.msg('Adding: ' + str(patterns))
        for pattern in patterns:
            if pattern != '':
                QUEUE.put((pattern, self.factory.state.patterns.add,
                           self.factory.state.patterns.send,
                           self.factory.state, self))

    def remove_patterns(self, patterns):
        """
        Remove a list of patterns.
        """
        log.msg('Removing: ' + str(patterns))
        for pattern in patterns:
            if pattern != '':
                QUEUE.put((pattern, self.factory.state.patterns.remove,
                           self.factory.state.patterns.send_removed,
                           self.factory.state, self))

    message_handlers = {'info': {'host': get_info, 'pattern': get_info},
                        'get': {'host': get_hosts, 'pattern': get_patterns},
                        'diff': {'host': diff_hosts, 'pattern': None},
                        'ping': {'host': ping_hosts, 'pattern': None},
                        'add': {'host': add_hosts, 'pattern': add_patterns},
                        'remove': {'host': remove_hosts,
                                   'pattern': remove_patterns}}

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
        log.msg('Type: ' + msg['type'])
        log.msg('Parameters: ' + str(msg['param']))
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
                                                msg['action'] + '"')
            self.factory.state.config['msg_state'] = 'bad'
            log.err(self.factory.state.config['msg'])

        # Process the queue.
        QUEUE.join()

        # Save state if changed.
        if msg['action'] != 'info':
            self.factory.state.json_export()


class SiteStatusFactory(WebSocketServerFactory):
    """
    Factory to create SiteStatus server instances and make a JSON files data
    available.
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
