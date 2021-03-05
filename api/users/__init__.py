import flask
import six
from flask_restful import Api

from .resources import users_api
from .services import UserAuthService

ROUTES = {
    '/': users_api.UserViewAPI,
    '/login': users_api.UserLoginAPI,
    '/signup': users_api.UserSignUpAPI,
    # '/logout': 'log out route',  # TODO: For future implementation
    # '/profile': 'user profile route'  # TODO: For future implementation
}


def init(app):
    blueprint = flask.Blueprint('user_auth', __name__,
                                url_prefix='/user_auth')
    api = Api(blueprint)

    for pattern, endpoint in six.iteritems(ROUTES):
        api.add_resource(endpoint, pattern)

    app.register_blueprint(blueprint)
    app.services.register_service('user_auth_service',
                                  UserAuthService())
