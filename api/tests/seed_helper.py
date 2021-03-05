import pandas as pd
import random
from datetime import datetime as dt, timedelta as td


def create_users(min, max, manager=False):
    total = random.randint(min, max + 1)
    users = {'email': [], 'password': [], 'permission_class': []}
    permission_class = 'manager' if manager else 'employee'

    for i in range(total):
        users['email'].append(permission_class + str(i) + '@gmail.com')
        users['password'].append('password ' + str(i))
        users['permission_class'].append(permission_class)
    return pd.DataFrame(users)


def create_vacations(min, max, users):
    vacations = {
        'vacation_start': [],
        'vacation_end': [],
        'status': [],
        'requester_id': [],
    }
    for i in range(len(users)):
        user = users.iloc[0]
        for j in range(random.randint(min, max + 1)):
            start = dt.utcnow() + td(days=random.randint(2, 30))
            end = start + td(days=random.randint(4, 5))
            vacations['vacation_start'].append(start)
            vacations['vacation_end'].append(end)
            vacations['status'].append('pending')
            vacations['requester_id'].append(user['id'])

    # return vacations
    return pd.DataFrame(vacations)


def create_overlapping_vacations(min, max, users, vacations):
    total = random.randint(min, max + 1)
    o_vacations = {
        'vacation_start': [],
        'vacation_end': [],
        'status': [],
        'requester_id': [],
    }
    for i in range(total):
        vacation = vacations.iloc[random.randint(1, len(vacations))]
        user = users.iloc[random.randint(1, len(users)-1)]
        start = vacation['vacation_start']
        end = vacation['vacation_end']
        new_start = start + td(days=3)
        new_end = end + td(days=3)
        o_vacations['vacation_start'].append(new_start)
        o_vacations['vacation_end'].append(new_end)
        o_vacations['status'].append('pending')
        o_vacations['requester_id'].append(user["id"])

    return pd.DataFrame(o_vacations)
