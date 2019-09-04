import logging
from flask import Flask
from api.controller import routes, tasks, celery

logger = logging.getLogger()


def create_app():
    return entrypoint(mode='app')


def create_worker():
    return entrypoint(mode='worker')


def entrypoint(mode='app'):
    app = Flask(__name__)

    app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379/0'

    configure_celery(app, tasks.celery)

    # Register blueprints
    app.register_blueprint(routes.bp,url_prefix='/api/v1')

    if mode=='app':
        return app
    elif mode=='worker':
        return celery


def configure_celery(app, celery):

    # Set broker url and result backend from app config
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']

    # Subclass task base for app context
    task_base = celery.Task

    class AppContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return task_base.__call__(self, *args, **kwargs)
    celery.Task = AppContextTask

    # Run finalize to process decorated tasks
    celery.finalize()
