from api import factory

celery = factory.create_worker()
