# -*- coding: utf-8 -*-
"""Sowingo Micrservices Template - Sample Module Services.

:copyright: (c) 2020 by Sowingo.com Corp.
"""

import logging

from .constants import SAMPLE_MODULE_NAME

class SampleModuleService(object):
    """A collection of services implemented by the sample module which can be
    accessed via Flask current_app's service registry.

    NOTE: THIS IS JUST A SAMPLE. THIS HAS NO REAL WORLD USE.
    """
    def __init__(self):
        """A basic Initialization for the class which just sets up the logger
        for further use within the class.

        NOTE: THIS IS JUST A SAMPLE. THIS HAS NO REAL WORLD USE.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing Services for module - %s"
                         %(SAMPLE_MODULE_NAME)
        )
    def send_response(self):
        """A helper service method which just sends back a simple string
        response to the caller.

        :return:`response` - A simple string response sent to the caller.

        NOTE: THIS IS JUST A SAMPLE. THIS HAS NO REAL WORLD USE.
        """

        response = {
            "message" : "This is a sample response from the %s"
            % (SAMPLE_MODULE_NAME),
        }

        return response
