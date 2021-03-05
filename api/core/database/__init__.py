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
    This class defined the users table and all the class related methods and logic
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    permission_class = db.Column(db.String, nullable=False, default='employee')

    def vacations(self):
        """ returns this employee's vacation requests;
        Vacation query WHERE Vacation.requester_id = User.id
        """
        return Vacation.query.filter_by(requester_id=self.id)

    def check_vacation_remaining(self, start=None, end=None):
        """
        Checks how many vacation days the employee has remaining
        from the annual allowable 30 days limit, based on pending
        and approved vacation requests.

        NOTE: for simplicity of the exercise, not including the logic
        to check if the used days is across a 1-yr time period. It only
        checks if the total used thus far is <= 30

        Also checks during new request if the total used + new request
        will exceed 30 and returns by how much it will exceed
        """
        days_used = 0
        if start and end:
            request_duration = (end - start).days
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
    This class defined the vacations table and all the class related methods and logic
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
        """
        Returns the user object (employee) that created this vacation request
        """
        return User.find_by_id(self.requester_id)

    def validator(self):
        """
        Returns the user obect (manager) that validated this vacation request.
        For requests that are still pending, this will not return anything
        """
        return User.find_by_id(self.validator_id) if self.validator_id else None

    def duration(self):
        """
        Returns the number of days in this vacation request
        """
        return (self.vacation_end - self.vacation_start).days + 1

    def period(self):
        """
        A string representation of the start and end of this vacation
        """
        start = datetime.strftime(self.vacation_start, '%Y-%m-%d')
        end = datetime.strftime(self.vacation_end, '%Y-%m-%d')
        return start + ' to ' + end

    # __abstract__ = True


class UserSchema(ma.Schema):
    """
    Structure for User serialization.
    For simplicity, this is only used to dump model object, therefore, password excluded
    """
    class Meta:
        fields = ('id', 'email', 'permission_class')


class VacationSchema(ma.Schema):
    """
    Structure for Vacation serialization
    """
    class Meta:
        fields = (
            'id', 'vacation_start', 'vacation_end', 'status', 'requester_id',
            'validator_id', 'something')


user_schema = UserSchema()
users_schema = UserSchema(many=True)
vacation_schema = VacationSchema()
vacations_schema = VacationSchema(many=True)
