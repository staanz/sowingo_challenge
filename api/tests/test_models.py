from api.core import User
import pytest


@pytest.fixture
def user_object1():
    return User(
        email='something@gmail.com',
        password='somethingelse',
        permission_class='employee'
    )


def test_check_vacation_remaining(user_object1):
    """
    Test to check if the User model object is calculating the correct number of
    vacation days remaining
    todo: need to complete this test
    """
    assert user_object1.check_vacation_remaining() == 30
