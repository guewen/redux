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
import openerp
import openerp.pooler
from celery import Celery

_logger = logging.getLogger(__name__)

# share instanciation with celery_worker
celery = Celery('tasks', backend='amqp', broker='amqp://')
#celery.config_from_object('celeryconfig')


@celery.task
def add(x, y):
    print x + y
    return x + y

#[add.delay(1, i) for i in xrange(1, 1000)]

dbname = 'redux'


@celery.task
def death_loop(product_id, fields, dbname='redux'):  # get dbname with partial?
    db, registry = openerp.pooler.get_db_and_pool(dbname, pooljobs=False)
    cr = db.cursor()
    _logger.info('Death loop on product %s', product_id)
    _logger.info('Fields to update: %s', fields)
    try:
        # TODO create an dedicated user
        # use get_user_context

        # Big Loop of the DEATH!
        # (update product triggers a new export task :-)

        registry.get('product.product').write(
            cr, openerp.SUPERUSER_ID, [product_id],
            {'name': 'test'})
    except Exception, e:
        cr.rollback()
        raise
    else:
        cr.commit()
    finally:
        cr.close()
    return True


@celery.task
def export(product_id, fields, dbname='redux'):  # get dbname with partial?
    db, registry = openerp.pooler.get_db_and_pool(dbname, pooljobs=False)
    cr = db.cursor()
    _logger.info('Exporting product %s', product_id)
    _logger.info('Fields to update: %s', fields)
    try:
        # TODO create an dedicated user
        # use get_user_context
        product_obj = registry.get('product.product')

        product = product_obj.browse(cr, openerp.SUPERUSER_ID, product_id)

        t = new_transform(openerp62,
                          magento17,
                          'product.product',
                          product=product,
                          fields=fields)

        print t.transform()

    except Exception, e:
        cr.rollback()
        raise
    else:
        cr.commit()
    finally:
        cr.close()
    return True


class Reference(object):

    def __init__(self, service, version):
        self.service = service
        self.version = version

    def __str__(self):
        return str(vars(self))

    def __eq__(self, other):
        return vars(self) == vars(other)


openerp62 = Reference(service='openerp', version='6.2')
magento17 = Reference(service='magento', version='1.7')


class Transform(object):

    model = None
    source_reference = None
    target_reference = None

    def __init__(self, *args, **kwargs):
        # init cr, uid, context
        super(Transform, self).__init__()

    @classmethod
    def class_for(cls, source_reference, target_reference, model):
        return (cls.source_reference == source_reference and
                cls.target_reference == target_reference and
                cls.model == model)

    @staticmethod
    def _browse_extract(record, fields):
        """ Return the same fields with a "-transformed"
        text appended
        """
        return dict([(field, "%s-transformed" % getattr(record, field))
                      for field in fields])

    def transform(self):
        raise NotImplementedError("Not implemented in base class")


class OpenerpProductTransform(Transform):

    model = 'product.product'
    source_reference = openerp62
    target_reference = magento17

    def __init__(self, product, fields=None, *args, **kwargs):
        super(OpenerpProductTransform, self).__init__(*args, **kwargs)
        self.product = product
        self.fields = fields

    def transform(self):
        return self._browse_extract(self.product, self.fields)


def new_transform(source_reference, target_reference, model, *args, **kwargs):
    for cls in Transform.__subclasses__():
        #TODO goto sub-sub-classes as well
        # take the uppest sub class to allow openerp modules
        if cls.class_for(source_reference, target_reference, model):
            return cls(*args, **kwargs)
    raise ValueError
