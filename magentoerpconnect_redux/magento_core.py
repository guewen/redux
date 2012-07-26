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

from openerp.osv.orm import Model, fields


class magento_instance(Model):
    _name = 'magento.instance'

    _columns = {
        'name': fields.char('Name', required=True),
        'location': fields.char('Location', required=True),
        'apiusername': fields.char('User Name'),
        'apipass': fields.char('Password'),
        'default_category_id': fields.many2one(
            'product.category',
            'Default Product Category',
            help="The category set on products when?? TODO."
            "\nOpenERP requires a main category on products for accounting."),
        'default_lang_id': fields.many2one(
            'res.lang',
            'Default Language',
            help="The language used for synchronizations with Magento."),
    }

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Magento instance\'s name already exist.')
    ]

# migration TODO
# external.referential -> magento.instance
# columns:
#   default_pro_cat => default_category_id
#   default_lang_id => default_lang_id


class magento_website(Model):
    _name = 'magento.website'

    _columns = {
        'name': fields.char('Name', required=True),
        'code' :fields.char('Code'),
        'instance_id': fields.many2one(
            'magento.instance',
            'Magento Instance',
            required=True),
        'sort_order': fields.integer('Sort Order'),
    }


class magento_store(Model):
    _name = 'magento.store'

    _inherits = {'sale.shop': 'shop_id'}

    _columns = {
        'name': fields.char('Name', required=True),
        'website_id': fields.many2one(
            'magento.website',
            'Magento Website',
            required=True),
        'shop_id': fields.many2one(
            'sale.shop',
            'Sale Shop',
            required=True,
            ondelete="cascade"),
        'default_category_id': fields.many2one(
            'product.category',
            'Default Product Category',
            help="The category set on products when?? TODO."
            "\nOpenERP requires a main category on products for accounting."),
    }


class magento_store_view(Model):
    _name = 'magento.store.view'

    _columns = {
        'name': fields.char('Name', required=True),
        'code': fields.char('Code'),
        'store_id':fields.many2one('magento.store',
                                   'Magento Store',
                                   ondelete='cascade', required=True),
        'enabled':fields.boolean('Enabled'),
        'sort_order':fields.integer('Sort Order'),
        'lang_id': fields.many2one('res.lang', 'Language'),
    }


# migration TODO
# external.shop.group -> magento.website
# columns:
#   default_pro_cat => default_category_id
#   default_lang_id => default_lang_id
