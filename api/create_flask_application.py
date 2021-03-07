# -*- coding: utf-8 -*-

"""The modules where the actual creation of the Sowingo's Microservices Template
flask Application.

NOTE: This is called regardless of whether the application is used as a CLI or
via uwsgi.

:copyright: (c) 2020 by Sowingo.com Corp.
"""

import logging
import flask
import importlib
from flask_migrate import Migrate, MigrateCommand

from . import core
from .version import __version__ as version

#
# We use some special formatting when logging output to the terminal while
# using Sowingo's Microservices Template's CLI or uwsgi application.
#
logging.basicConfig(
    level=logging.INFO,
    format= \
        '[%(levelname)s]\t[%(asctime)s] [%(filename)s:%(lineno)s -- %(funcName)s] %(message)s')

logger = logging.getLogger(__name__)

EXTENSIONS = [
    core.db,
    core.ma
]

MODULES = [
    'api.sample_module',
    'api.users',
    'api.vacations',
]


def initialize_module(app, module):
    """A helper function to call all the init methods of all moduels and
    use Flask's concept of blueprint to make applications modular.

    See https://flask.palletsprojects.com/en/1.1.x/blueprints/ for ref and some
    notes on Flask Blueprints

    :args:`app` - The current flask app.
    :args:`module` - Accepts a module defined within the API which based on
        Flask's Blueprint concept.
    :returns:`None` - Nothing is returned from this method.
    """
    init_func = getattr(module, 'init', None)
    blueprint = getattr(module, 'blueprint', None)

    if init_func:
        init_func(app)

    elif blueprint is not None:
        app.register_blueprint(module.blueprint)


def create_app(config=None):
    """The kickstarter which creates a Flask application and sets up the
    rest of the framework for Sowingo's Microservices Template's application.

    This method initializes all the core extensions, services and modules
    required to run the Sowingo's Microservices Template Flask Application.

    :param:`config` - An optional argument to be used when setting up the
        current flask app's config. See `app.config`
    :returns:`app` - Returns the current initialized flask application.
    """
    logger.info('Init :: Creating Flask Application')
    app = flask.Flask(__name__)
    migrate = Migrate()
    logger.info('Init :: Loading Application Settings')
    app.config.from_object('api.settings')
    logger.info('Init :: Loading Core Extensions')
    for extension in EXTENSIONS:
        extension.init_app(app)
        migrate.init_app(app, extension)

    logger.info('Init :: Initializing Service Registry')
    app.services = core.services.ServiceRegistry(app)

    logger.info('Init :: Registering Modules')
    for module_name in MODULES:
        module = importlib.import_module(module_name)
        initialize_module(app, module)

    logger.debug('Init :: Welcome to Sowingo\'s Microservices Template Application' \
                 + ' [app_version: {}]'.format(version))
    return app
