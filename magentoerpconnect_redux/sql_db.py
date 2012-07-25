# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2012 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
import openerp.sql_db
from openerp.sql_db import Cursor

_logger = logging.getLogger(__name__)


def cursor(self, serialized=True):
    cursor_type = serialized and 'serialized ' or ''
    _logger.debug('create %scursor to %r', cursor_type, self.dbname)
    return CursorWithTasks(self._pool, self.dbname, serialized=serialized)

# monkey patch cursor instanciation method in order to use the Cursor
# with tasks
# would be great to have a clean mean to do this
openerp.sql_db.Connection.original_cursor = openerp.sql_db.Connection.cursor
openerp.sql_db.Connection.cursor = cursor


class CursorWithTasks(Cursor):

    def __init__(self, pool, dbname, serialized=True):
        super(CursorWithTasks, self).__init__(pool, dbname, serialized=serialized)
        self.tasks = None

    def _on_commit_task(self, subtask):
        # TODO: raise if autocommit is on
        if self.tasks is None:
            self.tasks = []
        self.tasks.append(subtask)

    def _apply_tasks(self):
        if self.tasks is not None:
            for task in self.tasks:
                try:
                    task.apply_async()
                except Exception, e:
                    _logger.exception("Unable to apply task %s", task)
                else:
                    _logger.info("Applied task %s", task)

    def _flush_tasks(self):
        self.tasks = None

    def commit(self):
        res = super(CursorWithTasks, self).commit()
        self._apply_tasks()
        return res

    def rollback(self):
        res = super(CursorWithTasks, self).rollback()
        self._flush_tasks()
        return res
