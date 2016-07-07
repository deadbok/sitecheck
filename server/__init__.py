# encoding=utf-8
'''
Package for the server part of Site Status.

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
'''
import threading
from twisted.python import log
from server.protocol import QUEUE
from server.protocol import SiteStatusProtocol
from server.protocol import SiteStatusFactory
from server.state import ServerState
from server.version import __version__


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
