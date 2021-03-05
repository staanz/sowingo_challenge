import pytest


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
