"""
This file contains the unit tests for the application.
"""
def test_index_page(test_client):
    """
    GIVEN a flask application
    WHEN
    THEN 
    """
    
    response = test_client.get('/')

    assert response.status_code == 200
    assert b'Task Master' in response.data
    assert b'A flask application developed using test-driven development principles.' in response.data







