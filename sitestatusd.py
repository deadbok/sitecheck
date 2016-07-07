#!/usr/bin/python3
# encoding=utf-8
'''
Executable for starting the Site Status sever.

:copyright: (c) 2016 by Martin Grønholdt.
:license: MIT, see LICENSE for more details.
'''
import os
import sys
import argparse
from twisted.internet import reactor
from twisted.python import log
from server import SiteStatusFactory
from server import StatusThread
from server import __version__
from server import ServerState


if __name__ == '__main__':
    log.startLogging(sys.stdout)
    log.msg("Site Status server V" + str(__version__))

    # Parse command line
    ARG_PARSER = argparse.ArgumentParser()
    ARG_PARSER.add_argument('datafile',
                            help='JSON file containing configuration and ' +
                            'host data.')
    ARGS = ARG_PARSER.parse_args()

    STATE = ServerState()
    # Create state file if it's not there.
    if os.path.isfile(ARGS.datafile):
        STATE.json_import(ARGS.datafile)
    else:
        STATE.json_export(ARGS.datafile)

    FACTORY = SiteStatusFactory(u"ws://127.0.0.1:5683", STATE)

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
