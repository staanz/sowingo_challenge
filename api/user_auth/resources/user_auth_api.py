# -*- coding: utf-8 -*-
"""Sowingo Micrservices Template - Sample Module Endpoints.

:copyright: (c) 2020 by Sowingo.com Corp.
"""

from flask_restful import Resource
from flask import current_app, Flask, request, make_response
import jwt
import logging
from datetime import datetime as dt, timedelta as td
from api.core import User, db, user_schema, users_schema
from functools import wraps

SECRET_KEY = 'randomlygeneratedkeyforencoding'


def token_required(f):
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
        # This is a hack as decorators to return arg is a bit more complex :(
        return f(*args, current_user=current_user, **kwargs)

    return decorated


class UserViewAPI(Resource):
    """
    """

    @token_required
    def get(self, current_user):
        """
        """
        return make_response({'current_user': user_schema.dump(current_user)})

    def post(self):
        """
        """
        pass


class UserSignUpAPI(Resource):

    def post(self):
        # logger = logging.getLogger(__name__)
        # logger.info('****************')
        data = request.get_json()
        user = User()
        if 'email' not in data.keys() or 'password' not in data.keys():
            return make_response({'message': 'email and/or password missing'}, 400)
        if len(User.query.filter_by(email=data['email']).all()):
            return make_response({'message': 'email already taken!'}, 400)
        user.email = data['email']
        user.password = data['password']
        user.permission_class = data['type'] if data['type'] else 'employee'
        try:
            db.session.add(user)
            db.session.commit()
        except:
            return make_response({'message': 'something went wrong :/'}, 500)
        return make_response({'message': 'Signup successful for ' + user_schema.dump(user)}, 201)


class UserLoginAPI(Resource):
    def get(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        if email and password:
            user = User.query.filter_by(email=email).first()
            if user:
                if user.password == password:
                    token = jwt.encode({
                        'email': email,
                        'exp': dt.utcnow() + td(days=14),
                    }, SECRET_KEY)
                    return make_response({'token': token})
            else:
                return make_response({'message': 'User does not exist'}, 400)

        return make_response({'message': 'Invalid Details'}, 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    pass


class UserLogoutAPI(Resource):
    def get(self):
        return {}
    pass
