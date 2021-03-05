# -*- coding: utf-8 -*-
"""Sowingo Micrservices Template - Sample Module Endpoints.

:copyright: (c) 2020 by Sowingo.com Corp.
"""

from flask_restful import Resource
from flask import current_app, Flask, jsonify, request, make_response
import logging
from datetime import datetime as dt, timedelta as td
from api.core import User, Vacation, db, vacation_schema, vacations_schema, user_schema
from api.user_auth.resources.user_auth_api import token_required
from .validation_helper import *


class VacationViewAPI(Resource):
    """
    """

    @token_required
    def get(self, current_user):
        """
        """
        if current_user.permission_class != 'supervisor':  # todo ideally use a decorator
            return make_response({'message': 'you are not allowed here'}, 403)
        data = request.get_json()

        status = data['status_filter'] if 'status_filter' in data.keys() else None
        email = data['email_filter'] if 'email_filter' in data.keys() else None

        vs = Vacation.query.filter_by(status=status) if status else Vacation.query
        vs = vs.filter_by(email=email) if email else vs
        vs = vs.order_by(Vacation.requester_id.desc(), Vacation.status.asc()).all()

        # vacations = vacations_builder(vs)
        vacations = vacations_schema.dump(vs)
        return jsonify({'user': current_user.email,
                        'vacations': vacations})


class VacationViewSingleAPI(Resource):
    """
    """

    @token_required
    def get(self, current_user):
        """
        """
        if current_user.permission_class != 'supervisor':  # todo ideally use a decorator
            return make_response({'message': 'you are not allowed here'}, 403)
        data = request.get_json()

        status = data['status_filter'] if 'status_filter' in data.keys() else None
        if 'email' not in data.keys():
            return make_response({'message': 'missing employee email'}, 400)
        email = data['email']

        vs = Vacation.query.join(User, User.id == Vacation.requester_id).filter(User.email == email)
        vs = vs.filter_by(status=status) if status else vs
        vs = vs.order_by(Vacation.status.asc()).all()
        vacations = vacations_schema.dump(vs)
        employee = User.query.filter_by(email=email).first()
        return jsonify({'current_user': current_user.email,
                        'employee': employee.email,
                        'vacation days remaining': employee.check_vacation_remaining(),
                        'vacations': vacations})


class VacationValidateAPI(Resource):
    @token_required
    def put(self, current_user):
        if current_user.permission_class != 'supervisor':  # todo ideally use a decorator
            return make_response({'message': 'you are not allowed here'}, 403)
        data = request.get_json()
        if 'id' not in data.keys() or 'status' not in data.keys():
            return make_response({'message': 'incomplete details'}, 400)
        vacation = Vacation.find_by_id(data['id'])
        vacation.status = data['status']
        vacation.validator_id = current_user.id
        try:
            db.session.commit()
        except:
            return make_response({'message': 'something went wrong!'}, 503)
        message = 'you have ' + vacation.status + ' the request from ' + vacation.requester().email + ' between ' + vacation.period()
        return make_response({'message': message}, 201)


class VacationOverlapsAPI(Resource):
    @token_required
    def get(self, current_user):
        if current_user.permission_class != 'supervisor':  # todo ideally use a decorator
            return make_response({'message': 'you are not allowed here'}, 403)

        vacations = Vacation.query.filter(Vacation.status.in_(['approved', 'pending'])).all()
        olaps = overlapped_dates(vacations)
        if not len(olaps):
            return make_response({'message': 'nothing for now'})
        overlaps = {}
        for i, (k, v) in enumerate(olaps.items()):
            v1 = Vacation.find_by_id(v['ids'][0])
            v2 = Vacation.find_by_id(v['ids'][1])
            overlaps['Overlapping set ' + str(i + 1)] = {'v1': vacation_schema.dump(v1),
                                                         'v2': vacation_schema.dump(v2),
                                                         'overlapping duration': v['days']}

        return make_response({'overlaps': overlaps})
