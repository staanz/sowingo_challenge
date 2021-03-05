"""
This is a helper file to handle the token authentication logic
"""

from flask import request, make_response
from datetime import datetime as dt, timedelta as td
from functools import wraps
from api.core import User
import jwt

SECRET_KEY = 'randomlygeneratedkeyforencoding'  # TODO: this should be a randomly generated key


def get_token(email):
    """
    A helper function to generate the token based on the user's email address
    Valid for 14 days
    """
    token = jwt.encode({
        'email': email,
        'exp': dt.utcnow() + td(days=14),
    }, SECRET_KEY)
    return token


def token_required(f):
    """
    A decorator to be used for routes requiring authentication
    The token is expected as part of the header as {"x-access-token": "token"}
    If token is valid, will return back the corresponding user object as current_user
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            message = 'Token is missing'
            return make_response({'message': message}, 401)
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = User.query.filter_by(email=data['email']).first()
            if not current_user:
                return make_response({'user no longer exists!'}, 404)
        except:
            message = 'Token is invalid'
            return make_response({'message': message}, 401)
        """
        This is a hack as decorators for class methods is a bit more complex
        As calling function is a class method and has "self" as first arg,
        when current_user is returned first, it is assigned to "self"
        """
        # TODO: Fix this implementation
        return f(*args, current_user=current_user, **kwargs)
    return decorated
