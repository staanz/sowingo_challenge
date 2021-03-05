# -*- coding: utf-8 -*-
"""Sowingo Micrservices Template - Sample Module Endpoints.

:copyright: (c) 2020 by Sowingo.com Corp.
"""

from flask_restful import Resource
from flask import current_app

class SampleModuleAPI(Resource):
    """A class housing http service methods for this sample module.

    NOTE: THIS IS JUST A SAMPLE. THIS HAS NO REAL WORLD USE.
    """
    def get(self):
        """The implementation of the HTTP GET method which is serviced by the
        sample module.

        NOTE: THIS IS JUST A SAMPLE. THIS HAS NO REAL WORLD USE.
        """
        return current_app.services.sample_module_service.send_response()
