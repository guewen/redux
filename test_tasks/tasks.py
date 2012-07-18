from celery import Celery
celery.config_from_object('celeryconfig')
celery = Celery('tasks', backend='amqp', broker='amqp://guest@localhost//')

@celery.task
def add(x, y):
    return x + y

