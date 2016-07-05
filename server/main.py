"""
Main Site Check WebSockets server routines.

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
"""
import os
import sys
import json
import threading
from queue import Queue
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from twisted.internet import reactor
from twisted.python import log

from hosts import Hosts


__version__ = '0.4.4'
HOSTS = Hosts('test')
QUEUE = Queue()


class SiteCheckProtocol(WebSocketServerProtocol):
    """
    Server side implementation of the WebSocket protocol.
    """
    def send_hosts(self, hosts):
        """
        Send the complete data set a list of hosts.
        """
        response = dict()
        response['version'] = __version__
        response['total_hosts'] = len(HOSTS.hosts)
        response['hosts'] = list()
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
        response = dict()
        response['version'] = __version__
        response['total_hosts'] = len(HOSTS.hosts)
        response['length'] = len(hosts)
        response['hosts'] = list()
        for host in hosts:
            if host in HOSTS.hosts.keys():
                response['hosts'].append(HOSTS.hosts[host].get_dict())
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
        response = dict()
        response['version'] = __version__
        response['total_hosts'] = len(HOSTS.hosts)
        response['length'] = -len(hosts)
        response['hosts'] = hosts
        self.sendMessage(json.dumps(response).encode('utf-8'), False)

    def get(self, hosts):
        """
        Get data for a list of host names. `*` for all.
        """
        if hosts[0] == '*':
            self.send_hosts(HOSTS.hosts)
        else:
            self.send_hosts_by_name(hosts)

    def diff(self, hosts):
        """
        Run a diff on current and last index on a list of hosts.
        """
        for host in hosts:
            log.msg('Host: ' + host)
            QUEUE.put((host, HOSTS.diff, self.send_hosts_by_name))

    def ping(self, hosts):
        """
        Ping a list of hosts.
        """
        for host in hosts:
            log.msg('Host: ' + host)
            QUEUE.put((host, HOSTS.ping, self.send_hosts_by_name))

    def add(self, hosts):
        """
        Add a list of hosts.
        """
        log.msg('Adding: ' + str(hosts))
        for host in hosts:
            if host != '':
                QUEUE.put((host, HOSTS.add_host, self.send_hosts_by_name))

    def remove(self, hosts):
        """
        Remove a list of hosts.
        """
        log.msg('Removing: ' + str(hosts))
        for host in hosts:
            if host != '':
                QUEUE.put((host, HOSTS.remove_host,
                           self.send_removed_hosts_by_name))

    messages_handlers = {'get': get, 'diff': diff, 'ping': ping,
                         'add': add, 'remove': remove}

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
        self.messages_handlers[msg['action']](self, msg['hosts'])

        # Process the queue.
        QUEUE.join()
        HOSTS.save_json()


class StatusThread(threading.Thread):
    """
    Thread to do processing of request from the client.
    """
    def __init__(self):
        """
        Constructor.
        """
        threading.Thread.__init__(self)

    def run(self):
        """
        Perform the action, all data and functions are retrieved from the
        queue.
        """
        while True:
            action = QUEUE.get()

            action[1](action[0])
            action[2]([action[0]])

            QUEUE.task_done()


if __name__ == '__main__':
    log.startLogging(sys.stdout)

    FACTORY = WebSocketServerFactory(u"ws://127.0.0.1:5683")
    FACTORY.protocol = SiteCheckProtocol

    # Create directory for diffs if needed.
    if not os.path.isdir('sites'):
        os.mkdir('sites')

    # Create the queue and thread pool.
    for i in range(10):
        t = StatusThread()
        t.daemon = True
        t.start()

    reactor.listenTCP(5683, FACTORY)
    reactor.run()
