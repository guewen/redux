#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Celery Worker for Magentoerpconnect Redux

This script executes OpenERP instances to run Celery tasks.

Celery Worker re-uses openerp-server command-line options but does
not honor all of them.


To run with `celery worker --app=redux_worker -l info -E`

Use celeryev to view events


"""


import sys
# FIXME: config file?
openerp_path = '/home/guewen/code/openerp/redux/server'
sys.path.insert(0, openerp_path)


import logging
import os

import openerp
__author__ = openerp.release.author
__version__ = openerp.release.version
__redux_version__ = '0.1'


from celery import Celery

def report_configuration():
    """ Log the server version and some configuration values.

    This function assumes the configuration has been initialized.
    """
    config = openerp.tools.config
    _logger.info("OpenERP version %s", __version__)
    _logger.info("Magentoerpconnect Redux version %s", __redux_version__)
    # TODO add celery config
    for name, value in [('addons paths', config['addons_path']),
                        ('database hostname', config['db_host'] or 'localhost'),
                        ('database port', config['db_port'] or '5432'),
                        ('database user', config['db_user'])]:
        _logger.info("%s: %s", name, value)

# Also use the `openerp` logger for the main script.
_logger = logging.getLogger('openerp')

os.environ['TZ'] = 'UTC'
#openerp.tools.config.parse_config(sys.argv[1:])

config = openerp.tools.config

# FIXME: config file?
config['db_name'] = 'redux'
config['addons_path'] = (
    '/home/guewen/code/openerp/redux/server/openerp/addons,'
    '/home/guewen/code/openerp/redux/addons,'
    '/home/guewen/code/openerp/redux/openerp-web/addons,'
    '/home/guewen/code/openerp/redux/magentoerpconnect-redux'
)

if not config['db_name']:
    raise 'Database is mandatory. Use option -d or --database to set it.'

openerp.modules.module.initialize_sys_path()
openerp.modules.loading.open_openerp_namespace()
openerp.netsvc.init_logger()

#TODO what is this used for
openerp.multi_process = True # enable multi-process signaling
report_configuration()

celery = Celery('tasks', backend='amqp', broker='amqp://')
#celery.config_from_object('celeryconfig')

import openerp.addons.magentoerpconnect_redux.tasks as tasks

print "OpenERP Celery Worker. Hit Ctrl-C to exit."
print "Documentation is available at the top of the `celery_worker` file."
print "Monitoring database: %s" % config['db_name']

