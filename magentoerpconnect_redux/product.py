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


from openerp.osv.orm import Model
from tasks import product as tasks


class product_product(Model):
    _inherit = 'product.product'

    def write(self, cr, uid, ids, vals, context=None):
        for product_id in ids:
            #if 'name' in vals:
            #    cr._on_commit_task(tasks.death_loop.s(product_id, vals.keys()))
            #else:
            cr._on_commit_task(tasks.export.s(product_id, vals.keys()))
        return super(product_product, self).write(
                cr, uid, ids, vals, context=context)

