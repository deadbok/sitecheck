# encoding=utf-8
'''
Created on 10/06/2016

:copyright: (c) 2016 by Martin Grønholdt.
:license: GPLv3, see LICENSE for more details.
'''
import json
import threading
from werkzeug.utils import secure_filename
from flask import Flask
from flask import request
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_socketio import SocketIO
from uuid import uuid4
from hostlist import HostList

__version__ = '0.0.1'

APP = Flask(__name__)
APP.config['SECRET_KEY'] = uuid4().hex
APP.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
Bootstrap(APP)
socketio = SocketIO(APP)

NAME = 'oblivion'
HOSTLIST = HostList('test')


@APP.route('/')
def index():
    """
    Main status page.
    """
    # Don't like doing this every time.
    HOSTLIST.loadJSON()
    return render_template('main.html', NAME=NAME, version=__version__,
                           hosts=HOSTLIST.hosts)


@APP.route('/import', methods=['GET', 'POST'])
def upload_file():
    """
    Get the list of host from new line separated strings.
    """
    if request.method == 'POST':
        import_file = request.files['file']
        HOSTLIST.addHosts(import_file.readlines())
        HOSTLIST.saveJSON()
        # TODO show only newly added hosts
        return render_template('import.html', NAME=NAME, version=__version__,
                               hosts=HOSTLIST.getHostList())


@socketio.on('hello')
def hello():
    socketio.emit('hello')


@socketio.on('ping')
def ping():
    socketio.emit('log_line', 'Ping')


class workerThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            host = q.get()
            q.task_done()


if __name__ == '__main__':
    # APP.run()
    socketio.run(APP)


