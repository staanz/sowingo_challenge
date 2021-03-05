import flask
import six
from flask_restful import Api

from .resources import vacation_validate_api
from .services import VacationValidateService

ROUTES = {
    '/': vacation_validate_api.VacationViewAPI,
    '/validate': vacation_validate_api.VacationValidateAPI,
    '/single': vacation_validate_api.VacationViewSingleAPI,
    '/overlaps': vacation_validate_api.VacationOverlapsAPI
}


def init(app):
    blueprint = flask.Blueprint('vacation_validate', __name__,
                                url_prefix='/vacation_validate')
    api = Api(blueprint)

    for pattern, endpoint in six.iteritems(ROUTES):
        api.add_resource(endpoint, pattern)

    app.register_blueprint(blueprint)
    app.services.register_service('vacation_validate_service',
                                  VacationValidateService())
