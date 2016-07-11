# encoding=utf-8
'''
Package for the server part of Site Status.

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
'''
import six
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
            try:
                action = QUEUE.get()

                if not isinstance(action[0], six.string_types):
                    name = action[0]['name']
                else:
                    name = action[0]

                log.msg('In thread "' + self.name +
                        '" working on host "' + name + '"')

                if action[1] is not None:
                    action[1](action[0])
                if action[2] is not None:
                    action[2](name, action[3], action[4])

                QUEUE.task_done()
            except:
                log.err('Exception in "' + self.name + '"')
