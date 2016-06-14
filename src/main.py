# -*- coding: utf-8 -*-
'''
Created on 10/06/2016

:copyright: (c) 2016 by Martin Grønholdt.
:license: GPLv3, see LICENSE for more details.
'''
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from logging import handlers
from uuid import uuid4
import json
import logging
from Queue import Queue
from Queue import Empty
from flask_bootstrap import Bootstrap
from hosts import Hosts


__version__ = '0.0.2'

APP = Flask(__name__)
APP.config['SECRET_KEY'] = uuid4().hex
APP.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
Bootstrap(APP)
QUEUE = Queue()

NAME = 'oblivion'
HOSTS = Hosts('test')

# Start logger
if APP.config['DEBUG']:
    APP.logger.setLevel(logging.DEBUG)
    file_log = handlers.RotatingFileHandler("sitecheck.log",
                                       maxBytes=10000000,
                                       backupCount=5)
    file_log.setLevel(logging.DEBUG)
    file_log.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s'))
    APP.logger.addHandler(file_log)
else:
    APP.logger.setLevel(logging.CRITICAL)
    file_log = handlers.RotatingFileHandler("sitecheck.log",
                                       maxBytes=10000000,
                                       backupCount=5)
    file_log.setLevel(logging.WARNING)
    file_log.setFormatter(logging.Formatter('%(asctime)s - %(filename)s - %(funcName)s - %(levelname)s: %(message)s'))
    APP.logger.addHandler(file_log)


@APP.route('/')
def index():
    """
    Main status page.
    """
    return render_template('main.html', NAME=NAME, version=__version__,
                           hosts=HOSTS.hosts)


@APP.route('/import', methods=['GET', 'POST'])
def upload_file():
    """
    Get the list of host from new line separated strings.
    """
    if request.method == 'POST':
        APP.logger.debug('Importing hosts.')
        import_file = request.files['file']
        for host in import_file:
            if not host.startswith('#'):
                HOSTS.addHost(host=unicode(host, 'utf-8').strip())
        HOSTS.saveJSON()
        return redirect(url_for('index'))


@APP.route('/action', methods=['GET', 'POST'])
def action():
    """
    Perfom an action on some hosts.
    """
    if request.method == 'POST':
        APP.logger.debug('Action: ' + str(request.form))
        if request.form['action'] == 'ping':
            hosts = json.loads(request.form['hosts'])
            for host in hosts:
                APP.logger.debug('Pinging: ' + str(host.encode('utf8')))
                HOSTS.hosts[host].ping()
                QUEUE.put(item=HOSTS.hosts[host], block=False)

            HOSTS.saveJSON()

        return redirect(url_for('index'))


@APP.route('/updates', methods=['GET', 'POST'])
def get_updated_hosts():
    """
    Send a list of updated hosts.
    """
    if request.method == 'POST':
        APP.logger.debug('Action: ' + str(request.form))
        if request.form['action'] == 'get':
            try:
                host = QUEUE.get(block=False)
                return json.dumps(host.getDict())

            except Empty:
                return '[]'

        return redirect(url_for('index'))


if __name__ == '__main__':
    APP.run()


