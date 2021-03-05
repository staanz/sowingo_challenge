from api.vacations.resources.vacations_helper import overlap_checker
from datetime import datetime, timedelta
from api.core import Vacation
import pytest

"""
Test to check if the overlapping days between two vacation objects are calculated correctly
"""


@pytest.fixture
def vacation1():
    vacation = Vacation(vacation_start=datetime.utcnow(),
                        vacation_end=datetime.utcnow() + timedelta(days=10)
                        )
    return vacation


@pytest.fixture
def vacation2():
    vacation = Vacation(vacation_start=datetime.utcnow() + timedelta(days=5),
                        vacation_end=datetime.utcnow() + timedelta(days=15)
                        )
    return vacation


@pytest.fixture
def vacation3():
    vacation = Vacation(vacation_start=datetime.utcnow() + timedelta(days=20),
                        vacation_end=datetime.utcnow() + timedelta(days=30)
                        )
    return vacation


def test_overlap_checker1(vacation1, vacation2):
    assert overlap_checker(vacation2, vacation1) == 5


def test_overlap_checker2(vacation3, vacation1):
    assert overlap_checker(vacation3, vacation1) == 0


def test_overlap_checker3(vacation2, vacation3):
    assert overlap_checker(vacation2, vacation3) == 0
