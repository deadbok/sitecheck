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
    def onMessage(self, payload, isBinary):
        if not isBinary:
            log.msg(payload.decode('utf8'))
            msg = json.loads(payload.decode('utf8'))
            log.msg('Action: ' + msg['action'])
            if msg['action'] == 'get':
                self.sendMessage(json.dumps({ "hosts": str(len(HOSTS.hosts))}).encode('utf-8'), False)
                for host in HOSTS.hosts.values():
                    self.sendMessage(json.dumps(host.getDict()).encode('utf-8'), False)
        else:
            log.msg('Binary message received and discarded.')


if __name__ == '__main__':
    log.startLogging(sys.stdout)

    factory = WebSocketServerFactory(u"ws://127.0.0.1:5683")
    factory.protocol = SiteCheckProtocol

    reactor.listenTCP(5683, factory)
    reactor.run()
