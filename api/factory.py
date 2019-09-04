import os
import logging
from flask import Flask
from api.controller import routes, tasks, celery

logger = logging.getLogger()

def create_app():
    return entrypoint(mode='app')

def create_worker():
    return entrypoint(mode='worker')

def get_app_config():
    return ['redis://redis:6379/0', 'redis://redis:6379/0']

def entrypoint(mode='app'):
    app = Flask(__name__)
    
    urls = get_app_config()
    app.config['CELERY_BROKER_URL'] = urls[0]
    app.config['CELERY_RESULT_BACKEND'] = urls[1]    

    configure_celery(app, tasks.celery)

    # register blueprints
    app.register_blueprint(routes.bp,url_prefix='/api/v1')

    if mode=='app':
        return app
    elif mode=='worker':
        return celery

def configure_celery(app, celery):

    # set broker url and result backend from app config
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']

    # subclass task base for app context
    TaskBase = celery.Task
    class AppContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = AppContextTask

    # run finalize to process decorated tasks
    celery.finalize()