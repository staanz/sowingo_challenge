# -*- coding: utf-8 -*-
"""Sowingo Micrservices Template - Vacations Module Endpoints.

:copyright: (c) 2020 by Shanthanu Varma for Sowingo.com Corp.
"""

from flask_restful import Resource
from flask import jsonify, request, make_response
import logging
from datetime import datetime as dt
from api.core import Vacation, vacations_schema, vacation_schema, user_schema
from api.users.resources.users_helper import token_required
from .vacations_helper import vacation_query, overlapped_dates, vacation_request_validity_checker


class VacationViewAPI(Resource):
    """
    Routes to retrieve, create and/or update user records.
    At present, only the retrieve GET method for self is implemented
    """
    @token_required
    def get(self, current_user):
        """
        GET method to retrieve a user's own vacation requests, expects a valid user token in 'x-access-token' in header
        Request can also include optional filters {"status_filter": "STATUS"} to filter vacation records
        Will return a JSON response with current user object, remaining vacation days, and all vacation objects
        """
        data = request.get_json()
        status = data['status_filter'] if 'status_filter' in data.keys() else None

        vs = vacation_query(email=current_user.email, status=status)
        remaining = abs(current_user.check_vacation_remaining())
        vacations = vacations_schema.dump(vs)
        return jsonify({'user': user_schema.dump(current_user),
                        'vacation days remaining': remaining,
                        'vacations': vacations})

    @token_required
    def post(self, current_user):
        """
        POST method to create new vacation request expects valid token in 'x-access-token' in request header and
        JSON body with vacation details:
        {   "vacation_start": "DATE IN STRING FORMAT as YYYY-MM-DD",
            "vacation_end": "DATE IN STRING FORMAT as YYYY-MM-DD"
        }
        Returns a confirmation with vacation details if successful
        Timezone conversion is not implemented for this exercise
        """
        data = request.get_json()
        if 'start' not in data.keys() or 'end' not in data.keys():
            return make_response({'message': 'start date or end date missing'}, 400)

        # Convert string format date objects into datetime object
        # TODO: need to include logic to detect local timezone of request origin and convert to UTC format
        start = dt.strptime(data['start'], '%Y-%m-%d')
        end = dt.strptime(data['end'], '%Y-%m-%d')

        # Vacation validity check logic is in helper
        vacation, remaining, message, code = vacation_request_validity_checker(start, end, current_user)
        if vacation:
            try:
                vacation.save()
                pass
            except:  # TODO: avoid general exception handling
                return make_response({'message': 'something went wrong!'}, 503)
            vacation = vacation_schema.dump(vacation)
        return make_response({'message': message,
                              'details': vacation,
                              'remaining days': remaining,
                              }, code)

    @token_required
    def put(self, current_user):
        """
        Method to alter user's own vacation requests
        This method is not implemented for this exercise
        """
        return {}


class VacationOverviewAPI(Resource):
    """
    Routes for managers to view all vacation requests
    Can view Overall, individual users', and filter by vacation status
    """
    @token_required
    def get(self, current_user):
        """
        GET method expects 'x-access-token' for a user object with manager permission class
        Can optionally include "status_filter": "STATUS" and/or "email_filter": "email" as JSON body
        """
        if current_user.permission_class != 'manager':  # TODO: Ideally implement decorator for manager checks
            return make_response({'message': 'you are not allowed here'}, 403)
        data = request.get_json()

        status = data['status_filter'] if 'status_filter' in data.keys() else None
        email = data['email_filter'] if 'email_filter' in data.keys() else None
        vs = vacation_query(email=email, status=status)
        vacations = vacations_schema.dump(vs)
        return jsonify({'current_user': user_schema.dump(current_user),
                        'vacations': vacations})


class VacationOverlapsAPI(Resource):
    """
    Routes for managers to view overlaps in requested vacations of status pending or approved
    (logically, rejected vacations would not matter in this case)
    """
    @token_required
    def get(self, current_user):
        """
        GET method expects 'x-access-token' for a user object with manager permission class
        Returns pairs of vacation objects that overlap each other along with number of days of overlap
        """
        if current_user.permission_class != 'manager':  # TODO: Ideally implement decorator for manager checks
            return make_response({'message': 'you are not allowed here'}, 403)
        vacations = Vacation.query.filter(Vacation.status.in_(['approved', 'pending'])).all()
        olaps = overlapped_dates(vacations)
        """
        "olaps" is a nested dictionary object that looks like:
        {
         "1":   {
                    "ids": (v1, v2) --> tuple containing ids of the overlapping vacations,
                    "days": 10 --> number of days of overlap between v1 and v2
                }
         "2":   {
                    "ids": (v3, v7) --> tuple containing ids of the overlapping vacations,
                    "days": 10 --> number of days of overlap between v3 and v7
                }
         "3":   {
                    "ids": (vx, vy) --> tuple containing ids of the overlapping vacations,
                    "days": 10 --> number of days of overlap between vx and vy
                }
        }
        """
        if not len(olaps):
            return make_response({'message': 'nothing for now'})
        overlaps = {}
        # Convert olaps into a readable format to be returned as JSON object
        for i, (k, v) in enumerate(olaps.items()):
            v1 = Vacation.find_by_id(v['ids'][0])
            v2 = Vacation.find_by_id(v['ids'][1])
            overlaps['Overlapping set ' + str(i + 1)] = {'v1': vacation_schema.dump(v1),
                                                         'v2': vacation_schema.dump(v2),
                                                         'overlapping duration': v['days']}
        return make_response({'overlaps': overlaps})


class VacationValidateAPI(Resource):
    """
    Routes for managers to approve or reject a vacation request
    Returns a confirmation upon successful validation of vacation request
    """
    @token_required
    def put(self, current_user):
        """
        PUT method expects 'x-access-token' for a user object with manager permission class and
        JSON body with {"id": vacation_id, "status": "STATUS"}
        """
        if current_user.permission_class != 'manager':  # TODO: Ideally implement decorator for manager checks
            return make_response({'message': 'you are not allowed here'}, 403)
        data = request.get_json()

        # Return error message if any details missing
        if 'id' not in data.keys() or 'status' not in data.keys():
            return make_response({'message': 'incomplete details'}, 400)

        vacation = Vacation.find_by_id(data['id'])
        vacation.status = data['status']
        vacation.validator_id = current_user.id
        # TODO: need to change the generic exception handling to specific handler
        try:
            vacation.save()
        except:
            return make_response({'message': 'something went wrong!'}, 503)
        message = 'you have ' + vacation.status + ' the request from ' + vacation.requester().email + ' between ' + vacation.period()
        return make_response({'message': message}, 201)
