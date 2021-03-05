from flask import Flask
import json
import pytest
from api.user_auth.resources.user_auth_api import UserLoginAPI


@pytest.fixture
def employee_user_details():
    return {
        'email': 'test@gmail.com',
        'password': 'password',
        'type': 'employee'
    }

@pytest.fixture
def supervisor_user_details():
    return {
        'email': 'test@gmail.com',
        'password': 'password',
        'type': 'supervisor'
    }


def some_func(a):
    return a+4


def test_some_func():
    assert some_func(3) == 7
