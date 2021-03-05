# -*- coding: utf-8 -*-

"""A collection of global settings used throughout the Sowingo's Microservices Template
Demo Flask Application.

Also, We use .env* files to store local development environment variables in
the local directory - these are loaded into the local environment.

:copyright: (c) 2020 by Sowingo.com Corp.
"""

import os, sys
import logging

logger = logging.getLogger(__name__)

#
# A simple lambda function to fetch values from the environment for a key
# and set to a default if none found.
#
optional = lambda key, default=None: os.environ.get(key, default)

def required(key):
    """A helper which checks for presence of a key in the environment, if not
    raises a KeyError.

    :param:`key` - The key which should be present in the current environment.
    :returns: - The environment value stored for key :param:`key` provided.
    """

    try:
        if key in os.environ:
            return os.environ.get(key)
        else:
            raise KeyError
    except KeyError:
        logger.error("{0} is a required environment variable [Set in .env]"\
                     .format(key))
        sys.exit(-1)

SQLALCHEMY_DATABASE_URI = required('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEFAULT_LOG_LEVEL = optional('DEFAULT_LOG_LEVEL', 'DEBUG')
PORT = required('PORT')
