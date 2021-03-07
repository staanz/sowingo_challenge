import flask
import six
from flask_restful import Api

from .resources import users_api
from .services import UsersService

ROUTES = {
    '/': users_api.UserViewAPI,
    '/login': users_api.UserLoginAPI,
    '/signup': users_api.UserSignUpAPI,
    # '/logout': 'log out route',  # TODO: For future implementation
    # '/profile': 'user profile route'  # TODO: For future implementation
}


def init(app):
    blueprint = flask.Blueprint('users', __name__,
                                url_prefix='/users')
    api = Api(blueprint)

    for pattern, endpoint in six.iteritems(ROUTES):
        api.add_resource(endpoint, pattern)

    app.register_blueprint(blueprint)
    app.services.register_service('users_service',
                                  UsersService())
