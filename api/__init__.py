# -*- coding: utf-8 -*-

"""This entry point which creates the Sowingo's Microservices Template flask
Application.

Also starts the script manager which allows a CLI style interface to the
application.

:copyright: (c) 2020 by Sowingo.com Corp.
"""

import logging
import sys

from flask_script import Manager

from api.scripts import *

from .create_flask_application import create_app as create_flask_app


def run_manage_py(app=None):
    """The 'main' function which acts as the entry point for starting the flask
    script / shell application.

    :param:`app` - An optional argument to pass around a flask
        application instance.
        [Default: None]

    :returns:`None` - This method does not return anything (Infact this method
        does not 'return' at all until exit.)
    """
    #
    # Either use the existing flask provided as an argument or initialize
    # a brand new flask application.
    #
    app = app or create_flask_app()

    #
    # Initialize the flask script manager which provides CLI capabilites to
    # Sowingo's Microservices Template Flask application.
    #
    manager = Manager(app)

    logger = logging.getLogger(__name__)
    try:
        logger.info('Running the script manager...\n')
        #
        # Import all available commands and add it to the command managers
        # repository of acceptable CLI commands.
        #
        commands = {
        }
        for command in commands.items():
            manager.add_command(*command)
        #
        # Launching Sowingo's Microservices Template's CLI.
        #
        manager.run()
    except KeyboardInterrupt:
        sys.exit('\nCaught user (keyboard) interrupt. Exiting!\n')


def create_app(app=None):
    """The 'main' function which acts as the entry point for starting the flask
    application.

    :param:`app` - An optional argument to pass around a flask
        application instance.
        [Default: None]

    :returns:`app` - An instance of the created (or existing) flask
        application.
    """
    #
    # Either use the existing flask provided as an argument or initialize
    # a brand new flask application.
    #
    return app or create_flask_app()
