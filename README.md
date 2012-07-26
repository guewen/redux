# magentoerpconnect-redux

Proof of concept! Do not try this at home!

For openerp 6.2

Dependencies :

 * celery
 * rabbitmq-server

Addons path and configuration is hardcoded in `redux_worker.py`

They should be adapted to your configuration.

If you are really motivated to test:

 * Start the openerp server
 * run the celery worker with the same configuration (in `redux_worker.py`)

       cd magentoerpconnect_redux
       celery worker --app=redux_worker -l info -E

 * Install the product and magentoerpconnect_redux modules
 * Edit a product
 * Check the server logs and celery worker logs


