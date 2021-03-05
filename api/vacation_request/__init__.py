import flask
import six
from flask_restful import Api

from .resources import vacation_request_api
from .services import VacationRequestService

ROUTES = {
    '/': vacation_request_api.VacationViewAPI,
    '/new': vacation_request_api.VacationNewAPI,
    # '/logout': 'log out route',
    # '/profile': 'user profile route'
}


def init(app):
    blueprint = flask.Blueprint('vacation_request', __name__,
                                url_prefix='/vacation_request')
    api = Api(blueprint)

    for pattern, endpoint in six.iteritems(ROUTES):
        api.add_resource(endpoint, pattern)

    app.register_blueprint(blueprint)
    app.services.register_service('vacation_request_service',
                                  VacationRequestService())
