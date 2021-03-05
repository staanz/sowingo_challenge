# -*- coding: utf-8 -*-
"""Sowingo Micrservices Template - Sample Module Endpoints.

:copyright: (c) 2020 by Sowingo.com Corp.
"""

from flask_restful import Resource
from flask import current_app, Flask, jsonify, request, make_response
import logging
from datetime import datetime as dt, timedelta as td
from api.core import Vacation, vacations_schema, vacation_schema
from api.user_auth.resources.user_auth_api import token_required


class VacationViewAPI(Resource):
    """
    """

    @token_required
    def get(self, current_user):
        """
        """
        data = request.get_json()

        status = data['status_filter'] if 'status_filter' in data.keys() else None
        vs = current_user.vacations()
        vs = vs.filter_by(status=status) if status else vs.all()
        remaining = abs(current_user.check_vacation_remaining())
        vacations = vacations_schema.dump(vs)
        return jsonify({'user': current_user.email,
                        'vacation days remaining': remaining,
                        'vacations': vacations})


class VacationNewAPI(Resource):
    @token_required
    def post(self, current_user):
        logger = logging.getLogger(__name__)
        data = request.get_json()
        if 'start' not in data.keys() or 'end' not in data.keys():
            return make_response({'message': 'start date or end date missing'}, 400)
        start = dt.strptime(data['start'], '%Y-%m-%d')
        end = dt.strptime(data['end'], '%Y-%m-%d')
        vacation = Vacation()
        if start > end:
            return make_response({'message': 'end date cannot be before start date'}, 400)
        if len(Vacation.query.filter_by(
                requester_id=current_user.id, vacation_start=data['start'], vacation_end=data['end']
        ).all()):
            return make_response(
                {'message': 'you have already requested a vacation for this period!'},
                400)
        remaining = current_user.check_vacation_remaining(data['start'], data['end'])
        if remaining < 0:
            return make_response({'message': 'you are exceeding your 30 day allowance by ' + str(abs(remaining))}, 400)
        vacation.vacation_start = start
        vacation.vacation_end = end
        vacation.requester_id = current_user.id
        if vacation.duration() > 30:
            return make_response({'message': 'cannot request more than 30 days'}, 400)
        """
        """
        try:
            vacation.save()
            pass
        except:
            return make_response({'message': 'something went wrong!'}, 503)
        logger.info('****************')
        message = 'request successful'
        return make_response({'message': message,
                              'details': vacation_schema.dump(vacation),
                              'remaining days': remaining,
                              }, 201)
