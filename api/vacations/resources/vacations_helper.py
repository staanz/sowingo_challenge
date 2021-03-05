"""
This is a helper file to handle the vacation related logic
"""

from api.core import Vacation, User
from flask import make_response


def vacation_query(email=None, status=None):
    """
    A helper method to build queries with conditional WHERE clauses
    """
    vs = Vacation.query
    if email:
        vs = vs.join(User, User.id == Vacation.requester_id).filter(User.email == email)
    if status:
        vs = vs.filter(Vacation.status == status)
    return vs.order_by(Vacation.requester_id.desc(), Vacation.status.asc()).all()


def vacation_request_validity_checker(start, end, current_user):
    """
    A helper method to check if the requested vacation period is a valid request
    Some of these checks may be best handled from front-end
    """
    if start > end:  # Check to see if end date and start date are logically valid
        return None, None, 'end date cannot be before start date', 400

    if len(Vacation.query.filter_by(
            requester_id=current_user.id, vacation_start=start, vacation_end=end
    ).all()):  # Check to see if the exact same vacation period is already created; avoids erroneous double submits
        # TODO: Implement this in a cleaner manner
        return None, None, 'you have already requested a vacation for this period!', 400

    remaining = current_user.check_vacation_remaining(start, end)
    if remaining < 0:  # Check if sum of approved, pending, plus new request vacation duration exceeds allowable 30 days
        # TODO: Implement this in a cleaner manner
        return None, None, 'you are exceeding your 30 day allowance by ' + str(abs(remaining)), 400

    vacation = Vacation()
    vacation.vacation_start = start
    vacation.vacation_end = end
    vacation.requester_id = current_user.id

    # TODO: Implement this in a cleaner manner
    return vacation, remaining, 'request successful', 201


def overlap_checker(v1, v2):
    """
    A helper function to check if two vacation records have any overlapping days
    Logic checks if latest start date and earliest end date have any days (>0) in between
    If yes, it means they intersect
    If so, return the number of overlapping days
    """
    start1 = v1.vacation_start
    start2 = v2.vacation_start
    end1 = v1.vacation_end
    end2 = v2.vacation_end
    latest_start = max(start1, start2)
    earliest_end = min(end1, end2)
    overlap = max(0, (earliest_end - latest_start).days + 1)
    return overlap


def overlapped_dates(vacations):
    """
    A helper method to return a nested dict of pairs of vacations that overlap each other from a list of vacations
    Uses overlap_checker method to check how many days of overlap there is
    """
    overlaps = {}
    for i, vacation in enumerate(vacations[:-1]):
        for next_vacation in vacations[i + 1:]:
            overlap_days = overlap_checker(vacation, next_vacation)
            if overlap_days:
                overlaps[i] = {'ids': (vacation.id, next_vacation.id),
                               'days': overlap_days}
    return overlaps
