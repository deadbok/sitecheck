"""
Main Site Check Websocket server routines.
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


__version__ = '0.3.2'
HOSTS = Hosts('test')
QUEUE = Queue()


class SiteCheckProtocol(WebSocketServerProtocol):
    def send_hosts(self, hosts):
        """
        Send the complete data set a list of hosts.
        """
        response = dict()
        response['length'] = len(hosts)
        response['hosts'] = list()
        for host in hosts.values():
            response['hosts'].append(host.get_dict())
        self.sendMessage(json.dumps(response).encode('utf-8'), False)
        log.msg('Send: ' + str(hosts))

    def send_hosts_by_name(self, hosts):
        """
        Send the complete data set a list of host names.
        """
        response = dict()
        response['length'] = len(hosts)
        response['hosts'] = list()
        for host in hosts:
            response['hosts'].append(HOSTS.hosts[host].get_dict())
        self.sendMessage(json.dumps(response).encode('utf-8'), False)
        log.msg('Send: ' + str(hosts))

    def onMessage(self, payload, isBinary):
        if not isBinary:
            log.msg(payload.decode('utf8'))
            msg = json.loads(payload.decode('utf8'))
            log.msg('Action: ' + msg['action'])
            if msg['action'] == 'get':
                if msg['hosts'][0] == '*':
                    self.send_hosts(HOSTS.hosts)
                else:
                    self.send_hosts_by_name(msg['hosts'])
            if msg['action'] == 'diff':
                for host in msg['hosts']:
                    log.msg('Host: ' + host)
                    QUEUE.put((host, HOSTS.diff, self.send_hosts_by_name))
            if msg['action'] == 'ping':
                for host in msg['hosts']:
                    log.msg('Host: ' + host)
                    QUEUE.put((host, HOSTS.ping, self.send_hosts_by_name))
            if msg['action'] == 'add':
                log.msg('Adding: ' + str(msg['hosts']))
                for host in msg['hosts']:
                    if host != '':
                        QUEUE.put((host, HOSTS.addHost,
                                   self.send_hosts_by_name))
            QUEUE.join()
            HOSTS.saveJSON()
        else:
            log.msg('Binary message received and discarded.')


class status_thread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            action = QUEUE.get()

            action[1](action[0])
            action[2]([action[0]])

            QUEUE.task_done()


if __name__ == '__main__':
    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:5683")
    factory.protocol = SiteCheckProtocol

    # Create directory for diffs if needed.
    if not os.path.isdir('sites'):
        os.mkdir('sites')

    # Create the queue and thread pool.
    for i in range(10):
        t = status_thread()
        t.daemon = True
        t.start()

    reactor.listenTCP(5683, factory)
    reactor.run()
