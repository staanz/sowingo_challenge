# -*- coding: utf-8 -*-
"""Sowingo Micrservices Template - Sample Module Endpoints.

:copyright: (c) 2020 by Shanthanu Varma for Sowingo.com Corp.
"""

from flask_restful import Resource
from flask import request, make_response
from api.core import User, user_schema
from .users_helper import token_required, get_token


class UserViewAPI(Resource):
    """
    Routes to retrieve and/or update user records.
    At present, only the retrieve GET method for self is implemented
    """

    @token_required
    def get(self, current_user):
        """
        Method to retrieve current user
        """
        return make_response({'current_user': user_schema.dump(current_user)})

    def post(self):
        """
        Method to update user objects
        """
        pass


class UserSignUpAPI(Resource):
    """
    Routes for User SignUp
    """
    def post(self):
        """
        Post method to create a new user
        expected data = {'email':'something@something.com',
                        'password':'password_string'
                        'type':'employee_type'}
        "type" is optional; if not provided "employee" is taken by default
        Returns a confirmation if successful with the user details
        """
        data = request.get_json()
        user = User()
        # Return error if required fields are missing
        if 'email' not in data.keys() or 'password' not in data.keys():
            return make_response({'message': 'email and/or password missing'}, 400)

        # Return error if email is already taken
        if len(User.query.filter_by(email=data['email']).all()):
            return make_response({'message': 'email already taken!'}, 400)

        user.email = data['email']
        user.password = data['password']
        user.permission_class = data['type'] if 'type' in data.keys() else 'employee'

        # Basic check if writable
        try:
            user.save()
        except Exception as e:
            # TODO: Need to set up excepts for specific errors
            return make_response({'message': 'something went wrong :/'}, 500)
        return make_response({'message': 'Signup successful',
                              'user details': user_schema.dump(user)}, 201)


class UserLoginAPI(Resource):
    """
    User Login Routes
    """
    def get(self):
        """
        GET method to authenticate a user using JWT
        expected data = {'email':'something@something.com',
                        'password':'password_string'}
        Returns a token valid for 14 days if email and password is valid
        """
        data = request.get_json()
        email = data['email']
        password = data['password']
        if email and password:
            user = User.query.filter_by(email=email).first()
            if user and user.password == password:
                token = get_token(email)  # TODO: Fix app secret key in method helpers file
                return make_response({'token': token})
            else:
                return make_response({'message': 'User does not exist'}, 400)
        return make_response({'message': 'Invalid Details'}, 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    pass


class UserLogoutAPI(Resource):
    def get(self):
        """
        User signout functionality. Not implemented for this exercise
        """
        return {}
    pass
