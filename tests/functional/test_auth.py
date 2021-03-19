"""
This file contains the functional tests pertaining to user management functionality (registration, logging in, logging out)
"""

import pytest

def test_get_registration_form(test_client):
    """
    GIVEN a flask application
    WHEN a GET request for '/register' is received
    THEN check that the registration form renders correctly
    """

    response = test_client.get('/register')

    assert response.status_code == 200
    assert b'Register' in response.data
    assert b'User Name' in response.data
    assert b'Password' in response.data
    assert b'Confirm Password' in response.data
    assert b'Submit' in response.data

@pytest.mark.parametrize('username, password, confirm_password', [('', 'password', 'password'),('admin', '', 'password'),('admin', 'password', ''),('', '', 'password'), ('', 'password', ''),('admin', '', '') ,('', '', ''), ('admin', 'password123', 'password')])
def test_usuccessful_registration_errors_in_fields(test_client, username, password, confirm_password):
    """
    GIVEN a flask application
    WHEN a POST request for '/register' is received but there is a missing field(s) or the passwords dont match
    THEN check that the user is told to fix the errors
    """
    
    response = test_client.post('/register', data={'username': username, 'password': password, 'confirm_password': confirm_password}, follow_redirects=True)

    assert response.status_code ==200
    assert b'Register' in response.data
    assert b'Error in form data!' in response.data

def test_usuccessful_registration_existing_user(test_client):
    """
    GIVEN a flask application
    WHEN a POST request for '/register' is received from an existing user
    THEN check that the user is redirected to the login page and told to login
    """
    
    test_client.post('/register', data={'username': 'username', 'password': 'password', 'confirm_password': 'password'}, follow_redirects=True)
    response = test_client.post('/register', data={'username': 'username', 'password': 'password', 'confirm_password': 'password'}, follow_redirects=True)

    print(response.data.decode())

    assert response.status_code ==200
    assert b'Login' in response.data
    assert b'You already have an account! Please login.' in response.data
    

def test_successful_registration_new_user(test_client):
    """
    GIVEN a flask application
    WHEN a POST request for '/register' is received from a new user and they are successfully added to the database
    THEN check that the user is redirected to the login page to sign in. 
    """
    
    response = test_client.post('/register', data={'username': 'admin', 'password': 'password', 'confirm_password': 'password'}, follow_redirects=True)

    assert response.status_code ==200
    assert b'Login' in response.data
    assert b'You have been registered. Please sign in to access your account.' in response.data
    
def test_get_login_form(test_client):
    """
    GIVEN a flask application
    WHEN a GET request for '/login' is received
    THEN check that the login page renders correctly
    """

    response = test_client.get('/login')

    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'User Name' in response.data
    assert b'Password' in response.data
    assert b'Submit' in response.data

@pytest.mark.parametrize('username, password', [('', 'password123'),('default_user', ''),('', '')])
def test_usuccessful_login_errors_in_fields(test_client, username, password):
    """
    GIVEN a flask application
    WHEN a POST request for '/login' is received but there is a missing field(s) 
    THEN check that the user is told to fix the errors
    """
    
    response = test_client.post('/login', data={'username': username, 'password': password}, follow_redirects=True)

    assert response.status_code ==200
    assert b'Login' in response.data
    assert b'Error in form data!' in response.data


@pytest.mark.parametrize('username, password', [('administrator', 'password123'),('default_user', 'password')])
def test_login_invalid_credentials(test_client, register_default_user, username, password):
    """
    GIVEN a flask application
    WHEN a POST request for 'login' is received but the credentials are not recognised (incorrect username or incorrect password)
    THEN tell the user to sign in with correct credentials

    """

    response = test_client.post('/login', data={'username':username, 'password': password}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Invalid credentials. Please try again or sign up for an account.' in response.data
    assert b'Login' in response.data
    assert b'User Name' in response.data
    assert b'Password' in response.data
    assert b'Submit' in response.data

def test_login_valid_login_and_logout(test_client, register_default_user):
    """
    GIVEN a flask application
    WHEN a POST request is received for '/login' and the credentials are correct
    THEN log the user in and redirect them to the profile page
    """

    response = test_client.post('/login', data={'username':'default_user', 'password': 'password123'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'You are now logged in.' in response.data
    assert b'Profile' in response.data

    """
    GIVEN a flask application
    WHEN a logged in user makes a GET request for 'logout'
    THEN check that they get logged out of the app and redirected to the home page
    """

    response = test_client.get('/logout', follow_redirects=True)

    assert response.status_code == 200
    assert b'You are now logged out.' in response.data
    assert b'Home' in response.data

def test_login_valid_next_path(test_client, register_default_user):
    """
    GIVEN a flask application
    WHEN a POST request is received for '/login' and the credentials are correct, and the url contains a valid 'next' path
    THEN check that the user is redirected to the requested page after being logged in
    """

    response = test_client.post('login?next=%2Ftasks', data={'username':'default_user', 'password': 'password123'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Tasks' in response.data

def test_login_invalid_next_path(test_client, register_default_user):
    """
    GIVEN a flask application
    WHEN a POST request is received for '/login' and the credentials are correct, and the url contains an invalid 'next' path eg a full path
    THEN check that the user is redirected to the profile page instead 
    """

    response = test_client.post('login?next=http://www.badsite.com', data={'username':'default_user', 'password': 'password123'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Profile' in response.data

def test_login_when_already_logged_in(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a GET request is received for '/login' when the user is already logged in
    THEN redirect the user to the profile page with a message that they are already logged in
    """

    response = test_client.get('/login', follow_redirects=True)

    assert response.status_code == 200
    assert b'Profile' in response.data
    assert b'You are already logged in!' in response.data

def test_registration_when_already_logged_in(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a GET request is received for '/register' when the user is already logged in
    THEN redirect the user to the profile page with a message that they already have an account and are logged in
    """

    response = test_client.get('/register', follow_redirects=True)

    assert response.status_code == 200
    assert b'Profile' in response.data
    assert b'You already have an account and are logged in!' in response.data

def test_profile_not_logged_in(test_client):
    """
    GIVEN a flask application
    WHEN a GET request is received for '/profile' from a user who is not logged in
    THEN check that they are redirected to the log in page 
    """

    response = test_client.get('/profile', follow_redirects=True)

    assert response.status_code == 200
    assert b'Please log in to access this page.' in response.data
    assert b'Login' in response.data

def test_profile_logged_in(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a GET request is received for '/profile' from a user who is logged in
    THEN check that the profile page renders correctly 
    """

    response = test_client.get('/profile', follow_redirects=True)

    assert response.status_code == 200
    assert b'Profile' in response.data
    assert b'You are logged in as:' in response.data
    assert b'User Name: default_user' in response.data

@pytest.mark.parametrize('url', ['/register', '/login', '/profile', '/', '/tasks'])
def test_navbar_not_logged_in(test_client, url):
    """
    GIVEN a flask application
    WHEN a GET request is received for any page from a user that is not logged in
    THEN check that the navigation bar is appropriate
    """

    response = test_client.get(url, follow_redirects=True)

    assert response.status_code == 200
    assert b'HOME' in response.data
    assert b'REGISTER' in response.data
    assert b'LOGIN' in response.data

@pytest.mark.parametrize('url', ['/register', '/login', '/profile', '/', '/tasks'])
def test_navbar_logged_in(test_client, url, login_default_user):
    """
    GIVEN a flask application
    WHEN a GET request is received for any page from a user that is logged in
    THEN check that the navigation bar is appropriate
    """

    response = test_client.get(url, follow_redirects=True)

    assert response.status_code == 200
    assert b'HOME' in response.data
    assert b'TASKS' in response.data
    assert b'PROFILE' in response.data
    assert b'LOGOUT' in response.data