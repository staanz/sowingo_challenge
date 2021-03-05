# -*- coding: utf-8 -*-

"""The core of all the database related 'magic' happens and is available
throughout the Sowingo's Microservices Template Flask Application.

:copyright: (c) 2020 by Sowingo.com Corp.
"""

from datetime import datetime

import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from api.utils import uuids

#
# The db is the global sqlalchmey object which is used to perform queries,
# updates, inserts, deletes etc... throughout the application.
#

db = SQLAlchemy(session_options={'autoflush': False})
ma = Marshmallow()
db.Model.metadata.naming_convention = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}

__all__ = [
    'db',
    'ma',
    'Model',
    'User',
    'Vacation',
    'user_schema',
    'users_schema',
    'vacation_schema',
    'vacations_schema',
]


class BaseModelMixin(object):
    """A mixin to aid models development within the Flask application.

    This has all the common 'elements' of a model which may be used to create
    schemas by the modules when required - namely: id, created_at, updated_at

    NOTE: This allows us to create modular and re-usable models without having
    to repeatedly define the parts of schemas which are common to all.
    """
    created_at = sa.Column(sa.DateTime(timezone=True),
                           default=datetime.utcnow())
    updated_at = sa.Column(sa.DateTime(timezone=True),
                           default=datetime.utcnow(),
                           onupdate=datetime.utcnow())

    @sa.ext.declarative.declared_attr
    def id(cls):
        prefix = getattr(cls, '__id_prefix__', None)
        return sa.Column('id', sa.String, primary_key=True,
                         default=lambda: uuids.uuid_with_prefix(prefix))

    @classmethod
    def find_by_id(cls, id):
        # return cls.query.filter_by(id=id)
        return cls.query.get(id)

    def save(self):
        db.session.add(self)
        # db.session.flush()
        db.session.commit()

    # def __repr__(self):
    #     return '{}({!r})'.format(self.__class__.__name__, self.id)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        return u'{}({})'.format(self.__class__.__name__, self.id)


class Model(db.Model, BaseModelMixin):
    """An abstract class which will be used by modules within the application
    when bulding models for persistence in a database.

    NOTE: This inherits from the BaseModelMixin we have defined above.
    """
    __abstract__ = True


class User(db.Model, BaseModelMixin):
    """ User Table
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    permission_class = db.Column(db.String, nullable=False, default='employee')

    def vacations(self):
        return Vacation.query.filter_by(requester_id=self.id)

    def check_vacation_remaining(self, start=None, end=None):
        days_used = 0
        if start and end:
            request_duration = (datetime.strptime(end, '%Y-%m-%d') - datetime.strptime(start, '%Y-%m-%d')).days
        else:
            request_duration = 0
        vacations = self.vacations().filter(Vacation.status.in_(['approved', 'pending']))
        for v in vacations:
            days_used += v.duration()
        return 30 - days_used - request_duration

    def __repr__(self):
        return 'User ' + self.email + ' of type ' + self.permission_class

    # __abstract__ = True


class Vacation(db.Model, BaseModelMixin):
    """Vacation table
    """
    __tablename__ = 'vacations'
    id = db.Column(db.Integer, primary_key=True)
    vacation_start = db.Column(db.DateTime(timezone=True), nullable=False)
    vacation_end = db.Column(db.DateTime(timezone=True), nullable=False)
    status = db.Column(db.String, nullable=False, default='pending')
    requester_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    validator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def __repr__(self):
        start = datetime.strftime(self.vacation_start, '%Y-%m-%d')
        end = datetime.strftime(self.vacation_end, '%Y-%m-%d')
        requested_by = 'Requested by ' + self.requester().email + ' '
        between = ' between ' + start + ' and ' + end + ' '
        status = self.status
        status = status + ' by ' + self.validator().email if self.validator_id else status
        return requested_by + between + status
        # return 'this is the model'

    def requester(self):
        return User.find_by_id(self.requester_id)

    def validator(self):
        return User.find_by_id(self.validator_id)

    def duration(self):
        return (self.vacation_end - self.vacation_start).days + 1

    def period(self):
        start = datetime.strftime(self.vacation_start, '%Y-%m-%d')
        end = datetime.strftime(self.vacation_end, '%Y-%m-%d')
        return start + ' to ' + end

    # __abstract__ = True


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'permission_class')


class VacationSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'vacation_start', 'vacation_end', 'status', 'requester_id',
            'validator_id', 'something')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
vacation_schema = VacationSchema()
vacations_schema = VacationSchema(many=True)
