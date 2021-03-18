import pytest
from project.models import User
from project import create_app, db


@pytest.fixture(scope='module')
def new_user():
    """
    A fixture that instantiates an object of the User class. Used to test the User model.
    """
    user = User('admin', 'password123')
    return user

@pytest.fixture(scope='session')
def test_client():
    """
    A fixture that instantiates and configures a flask application instance for testing and then creates a test_client for it. Used by unit and functional tests to make requests to the flask application instance configured for testing.
    """
    test_app = create_app()
    test_app.config.from_object('config.TestingConfig')

    # Create a test client object
    with test_app.test_client() as testing_client:
        # Create an application context
        with test_app.app_context():
            # Log
            test_app.logger.info('Inside the test_client fixture')
            
            # Create all tables in the database
            db.create_all()

            yield testing_client#this is where testing occurs

            # Establish application context and delete all the tables in the database
            with test_app.app_context():
                db.drop_all()

@pytest.fixture(scope='module')
def register_default_user(test_client):
    """
    A fixture that takes a user object and adds them to the database so that they can be a registered user of the application. Used by login functional tests to test the login functionality.
    """
    test_client.post('/register', data={'username': 'default_user', 'password':'password123', 'confirm_password': 'password123'}, follow_redirects=True)
    return

@pytest.fixture(scope='function')
def login_default_user(test_client, register_default_user):
    """
    A fixture that logs in and logs out the default user obejct. Used by login functional tests to test the login functionality (login when a user is already logged in).
    """
    test_client.post('/login', data={'username': 'default_user', 'password':'password123'}, follow_redirects=True)

    yield

    test_client.get('/logout')


