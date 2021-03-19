"""
This file contains the functional tests pertaining to task master functionality (add/delete/update/mark as complete)
"""

def test_name(test_client):
    """
    GIVEN a flask application
    WHEN
    THEN 
    """
    pass

def test_get_tasks_logged_in(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a GET request is received for '/tasks' from a logged in user
    THEN check that the page renders correctly

    """

    response = test_client.get('/tasks')

    assert response.status_code == 200
    assert b'Task Master' in response.data
    assert b'To do' in response.data
    assert b'Add a new task' in response.data
    assert b'Completed tasks' in response.data
    assert b'Task' in response.data
    assert b'Submit' in response.data

def test_get_tasks_not_logged_in(test_client):
    """
    GIVEN a flask application
    WHEN a GET request is received for '/tasks' from a user whose not logged in
    THEN check that they are redirected to the login page

    """

    response = test_client.get('/tasks', follow_redirects=True)

    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Please log in to access this page' in response.data
    assert b'To do' not in response.data
    assert b'Add a new task' not in response.data
    assert b'Completed tasks' not in response.data

def test_add_task_logged_in(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a POST request for '/tasks' is received from a logged in user
    THEN check that the task is added to the database and displayed correctly
    """
    
    response = test_client.post('/tasks', data={'new_task': 'Learn docker'}, follow_redirects=True)

    print(response.data.decode())

    assert response.status_code == 200
    assert b'Learn docker' in response.data
    assert b'Delete' in response.data
    assert b'Update' in response.data
    assert b'Mark as complete' in response.data
    assert b'New task added!' in response.data

def test_add_task_not_logged_in(test_client):
    """
    GIVEN a flask application
    WHEN a POST request for '/tasks' is received from a user that is not logged in
    THEN check that the user is redirected to the login page
    """
    
    response = test_client.post('/tasks', data={'new_task': 'Learn docker'}, follow_redirects=True)

    print(response.data.decode())

    assert response.status_code == 200
    assert b'Login' in response.data
    assert b'Please log in to access this page' in response.data

def test_add_task_already_exists(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a POST request for '/tasks' is received but the task already exists
    THEN check that the user is told the task already exists
    """
    test_client.post('/tasks', data={'new_task': 'Learn something'}, follow_redirects=True)
    
    response = test_client.post('/tasks', data={'new_task': 'Learn something'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Task already exists!' in response.data

def test_delete_task_logged_in(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a GET request for '/delete_task/<int:task_id>' is received from a logged in user
    THEN check that the task gets deleted
    """

    test_client.post('/tasks', data={'new_task': 'First task'}, follow_redirects=True)
    
    response = test_client.get('/delete_task/3', follow_redirects=True)

    assert response.status_code == 200
    assert b'First task' not in response.data
    assert b'Task has been deleted!' in response.data

def test_delete_task_not_logged_in(test_client):
    """
    GIVEN a flask application
    WHEN a GET request for '/delete_task/<int:task_id>' is received from a user not logged in
    THEN check that they are redirected to the login page
    """
    
    response = test_client.get('/delete_task/3', follow_redirects=True)

    assert response.status_code == 200
    assert b'Please log in to access this page.' in response.data
    assert b'Login' in response.data

def test_mark_complete_logged_in(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a GET request for '/mark_complete/<int:task_id>' is received from a logged in user
    THEN check that the task gets marked as complete
    """

    test_client.post('/tasks', data={'new_task': 'First task'}, follow_redirects=True)
    
    response = test_client.get('/mark_complete/3', follow_redirects=True)

    assert response.status_code == 200
    assert b'First task' in response.data
    assert b'Task completed!' in response.data

def test_mark_complete_not_logged_in(test_client):
    """
    GIVEN a flask application
    WHEN a GET request for '/mark_complete/<int:task_id>' is received from a user not logged in
    THEN check that they are redirected to the login page
    """
    
    response = test_client.get('/delete_task/3', follow_redirects=True)

    assert response.status_code == 200
    assert b'Please log in to access this page.' in response.data
    assert b'Login' in response.data

def test_update_task_logged_in(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a GET request for '/update_task/<int:task_id>' is received from a logged in user
    THEN check that the update task form gets rendered correctly
    """

    test_client.post('/tasks', data={'new_task': 'First task'}, follow_redirects=True)
    
    response = test_client.get('/update_task/3', follow_redirects=True)

    assert response.status_code == 200
    assert b'First task' in response.data
    assert b'Update Task' in response.data
    assert b'Task' in response.data
    assert b'Submit' in response.data

def test_update_task_not_logged_in(test_client):
    """
    GIVEN a flask application
    WHEN a GET request for '/update_task/<int:task_id>' is received from a user not logged in
    THEN check that they are redirected to the login page
    """
    
    response = test_client.get('/update_task/3', follow_redirects=True)

    assert response.status_code == 200
    assert b'Please log in to access this page.' in response.data
    assert b'Login' in response.data

def test_post_update_task_logged_in(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a POST request for '/update_task/<int:task_id>' is received from a logged in user
    THEN check that the task gets updated correctly
    """

    test_client.post('/tasks', data={'new_task': 'First task'}, follow_redirects=True)
    
    response = test_client.post('/update_task/3', data={'updated_task': 'First task has been updated'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'First task has been updated' in response.data
    assert b'Task updated!' in response.data

def test_post_update_task_not_logged_in(test_client):
    """
    GIVEN a flask application
    WHEN a POST request for '/update_task/<int:task_id>' is received from a user not logged in
    THEN check that they are redirected to the login page
    """
    
    response = test_client.post('/update_task/3', data={'updated_task': 'First task has been updated'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Please log in to access this page.' in response.data
    assert b'Login' in response.data


def test_post_update_task_missing_field(test_client, login_default_user):
    """
    GIVEN a flask application
    WHEN a POST request for '/update_task/<int:task_id>' is received from a logged in user but there is no data in the form
    THEN check that the user is given a warning
    """

    test_client.post('/tasks', data={'new_task': 'First task'}, follow_redirects=True)
    
    response = test_client.post('/update_task/3', data={'updated_task': ''}, follow_redirects=True)

    assert response.status_code == 200
    assert b'First task' in response.data
    assert b'Update Task' in response.data
    assert b'Task' in response.data
    assert b'Submit' in response.data
    assert b'Error in the form!' in response.data

