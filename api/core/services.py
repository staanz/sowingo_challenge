# -*- coding: utf-8 -*-

"""The service registry core which allows modules to have a micro-service
style support built into the application.

This is initialized when the flask application is initialized. See
:function:`create_app` defined under the create_flask_application.

:copyright: (c) 2020 by Sowingo.com Corp.
"""

__all__ = [
    'ServiceRegistry'
]

class ServiceRegistry(object):
    """The service registry core which allows modules to have a micro-service
    support built into the application.

    This allows us to build re-usable services which may be used from
    within modules, scripts or other services of this application. For now,
    all the modules and their services live within the application but
    setting it up like this allows us to easily break it down in
    Microservices, when required.

    This is basically the service registry core of the flask application.
    """
    app = None
    registered_services = None

    def __init__(self, app=None):
        self.app = None
        self.registered_services = {}

        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

    def register_service(self, name, service):
        self.registered_services[name] = service

    def __getattr__(self, name):
        if name in self.registered_services:
            return self.registered_services[name]
        else:
            raise AttributeError(u'No such attribute: {}'.format(name))
