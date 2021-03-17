"""
This file contains tests for the models defined in models.py
"""

def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new user object is created
    THEN check that the object has the expected attributes and that the password is hashed
    """
    assert new_user.username == 'admin'
    assert new_user.hashed_password != 'password123'
    assert new_user.is_password_valid('password123') == True
    assert new_user.is_password_valid('password') == False
    

