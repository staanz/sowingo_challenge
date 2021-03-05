from flask import Flask
from api.vacation_validate.resources.validation_helper import overlap_checker
from datetime import datetime, timedelta
from api.core import Vacation
import pytest


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


def test_overlap_checker(vacation1, vacation2):
    assert overlap_checker(vacation2, vacation1) == 5
