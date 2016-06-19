import sys
import json
from twisted.python import log
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory
from autobahn.twisted.websocket import WebSocketServerProtocol
from hosts import Hosts

__version__ = '0.0.3'
HOSTS = Hosts('test')


class SiteCheckProtocol(WebSocketServerProtocol):
    def sendHosts(self, hosts):
        """
        Send the complete data set a list of hosts.
        """
        response = dict()
        response['length'] = len(hosts)
        response['hosts'] = list()
        for host in hosts.values():
            response['hosts'].append(host.getDict())
        self.sendMessage(json.dumps(response).encode('utf-8'), False)
        log.msg('Send: ' + str(hosts))

    def sendHostsByName(self, hosts):
        """
        Send the complete data set a list of host names.
        """
        response = dict()
        response['length'] = len(hosts)
        response['hosts'] = list()
        for host in hosts:
            response['hosts'].append(HOSTS.hosts[host].getDict())
        self.sendMessage(json.dumps(response).encode('utf-8'), False)
        log.msg('Send: ' + str(hosts))

    def onMessage(self, payload, isBinary):
        if not isBinary:
            log.msg(payload.decode('utf8'))
            msg = json.loads(payload.decode('utf8'))
            log.msg('Action: ' + msg['action'])
            if msg['action'] == 'get':
                if msg['hosts'][0] == '*':
                    self.sendHosts(HOSTS.hosts)
                else:
                    self.sendHostsByName(msg['hosts'])
            if msg['action'] == 'ping':
                for host in msg['hosts']:
                    log.msg('Host: ' + host)
                    HOSTS.hosts[host].ping()
                    self.sendHostsByName([host])
                HOSTS.saveJSON()
            if msg['action'] == 'add':
                log.msg('Adding: ' + str(msg['hosts']))
                for host in msg['hosts']:
                    if host != '':
                        HOSTS.addHost(host)
                        self.sendHostsByName([host])
                HOSTS.saveJSON()
        else:
            log.msg('Binary message received and discarded.')


if __name__ == '__main__':
    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:5683")
    factory.protocol = SiteCheckProtocol

    reactor.listenTCP(5683, factory)
    reactor.run()
