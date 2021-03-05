# -*- coding: utf-8 -*-
"""Sowingo Micrservices Template - Sample Module.

:copyright: (c) 2020 by Sowingo.com Corp.
"""

import flask
import six
from flask_restful import Api

from .resources import sample_module_api
from .services import SampleModuleService

ROUTES = {
    '/': sample_module_api.SampleModuleAPI,
}


def init(app):
    """The entry point for the module. This called as part of the overall
    Flask application Initialization.

    :param:`app` - The instance of the current Flask App.

    NOTE: THIS IS JUST A SAMPLE. THIS HAS NO REAL WORLD USE.
    """
    blueprint = flask.Blueprint('sample_module', __name__,
                                url_prefix='/sample_module')
    api = Api(blueprint)

    for pattern, endpoint in six.iteritems(ROUTES):
        api.add_resource(endpoint, pattern)

    app.register_blueprint(blueprint)
    app.services.register_service('sample_module_service',
                                  SampleModuleService())
