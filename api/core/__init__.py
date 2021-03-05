# -*- coding: utf-8 -*-

"""A list of CORE servcies which are used by the modules defined throughout
the Flask Application.

This allows us to build re-usable modular core services which may be used from
within modules of this application. For now, we have only two such core
services but setting it up like this allows us to scale the application when
we add more core services for e.g. like caching, events, sessions etc...

:copyright: (c) 2020 by Sowingo.com Corp.
"""

from .database import db, User, Vacation, ma, vacations_schema, vacation_schema, user_schema, users_schema
from .services import ServiceRegistry

EXTENSIONS = [
    db,
    ma,
    User,
    Vacation,
    vacation_schema,
    vacations_schema,
    user_schema,
    users_schema
]

__all__ = [
    'db',
    'ma',
    'User',
    'Vacation',
    'ServiceRegistry',
    'vacation_schema',
    'vacations_schema',
    'users_schema',
    'user_schema'
    # 'sample_module'
]
