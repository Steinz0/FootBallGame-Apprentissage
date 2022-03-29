from celery import Celery

celery_app = Celery('tasks', backend='amqp://localhost:5672', broker='amqp://localhost:5672')

@celery_app.task
def one(text):
    return text[::-1]