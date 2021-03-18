"""
This file contains the unit tests for the custom error handlers
"""

def test_error_handler_404(test_client):
    """
    GIVEN a flask application
    WHEN a GET request is received for an undefined route
    THEN check that the custom error handler function renders 404.html properly
    """

    response = test_client.get('/undefined')

    assert response.status_code == 404
    assert b'404' in response.data
    assert b'Page Not Found' in response.data

def test_error_handler_405(test_client):
    """
    GIVEN a flask application
    WHEN a POST request is received for a route that only accepts GET requests
    THEN check that the custom error handler function renders 405.html properly
    """

    response = test_client.post('/', data={}, follow_redirects=True)

    assert response.status_code == 405
    assert b'405' in response.data
    assert b'Method Not Allowed' in response.data

def test_error_handler_500(test_client):
    """
    GIVEN a flask application
    WHEN an internal server error occurs
    THEN check that the custom error handler function renders 500.html properly
    """

    response = test_client.get('/500')

    assert response.status_code == 500
    assert b'500' in response.data
    assert b'Internal Server Error' in response.data