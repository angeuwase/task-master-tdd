import pytest
from project.models import User
#from project import create_app, db


@pytest.fixture(scope='module')
def new_user():
    user = User('admin', 'password123')
    return user