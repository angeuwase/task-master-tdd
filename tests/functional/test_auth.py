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
    assert b'register' in response.data

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
    assert b'login' in response.data

