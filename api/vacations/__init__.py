import flask
import six
from flask_restful import Api

from .resources import vacations_api
from .services import VacationsService

ROUTES = {
    '/': vacations_api.VacationViewAPI,
    '/overview': vacations_api.VacationOverviewAPI,
    '/overlaps': vacations_api.VacationOverlapsAPI,
    '/validate': vacations_api.VacationValidateAPI
}


def init(app):
    blueprint = flask.Blueprint('vacations', __name__,
                                url_prefix='/vacations')
    api = Api(blueprint)

    for pattern, endpoint in six.iteritems(ROUTES):
        api.add_resource(endpoint, pattern)

    app.register_blueprint(blueprint)
    app.services.register_service('vacations_service',
                                  VacationsService())
