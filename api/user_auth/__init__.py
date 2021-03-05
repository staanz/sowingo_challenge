import flask
import six
from flask_restful import Api

from .resources import user_auth_api
from .services import UserAuthService

ROUTES = {
    '/': user_auth_api.UserViewAPI,
    '/login': user_auth_api.UserLoginAPI,
    '/signup': user_auth_api.UserSignUpAPI,
    # '/logout': 'log out route',
    # '/profile': 'user profile route'
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
