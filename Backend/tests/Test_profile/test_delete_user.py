import json
from django.test import RequestFactory
from HandymanHive.models import CustomWorker, CustomUser
from HandymanHive.routes.profile import delete_user
import pytest


@pytest.mark.django_db
def test_delete_user_worker_exists():
    # Create a CustomWorker instance for testing
    worker = CustomWorker.objects.create(email="worker@example.com",age="5")
    
    # Prepare request data
    data = {
        "email": "worker@example.com",
        "isWorker": "True"
    }
    request = RequestFactory().post('/delete_user/', json.dumps(data), content_type='application/json')
    
    # Call the view function
    response = delete_user(request)
    
    # Check if the user has been deleted
    assert response.status_code == 200
    assert not CustomWorker.objects.filter(email="worker@example.com").exists()

@pytest.mark.django_db
def test_delete_user_user_exists():
    # Create a CustomUser instance for testing
    user = CustomUser.objects.create(email="user@example.com",age="5")
    
    # Prepare request data
    data = {
        "email": "user@example.com",
        "isWorker": "False"
    }
    request = RequestFactory().post('/delete_user/', json.dumps(data), content_type='application/json')
    
    # Call the view function
    response = delete_user(request)
    
    # Check if the user has been deleted
    assert response.status_code == 200
    assert not CustomUser.objects.filter(email="user@example.com").exists()

@pytest.mark.django_db
def test_delete_user_no_user_exists():
    # Prepare request data for a non-existing user
    data = {
        "email": "non_existing@example.com",
        "isWorker": "True"
    }
    request = RequestFactory().post('/delete_user/', json.dumps(data), content_type='application/json')
    
    # Call the view function
    response = delete_user(request)
    
    # Check if the response is as expected
    assert response.status_code == 200
    assert "User deleted successfully" in response.json().get("message", "")

@pytest.mark.django_db
def test_delete_user_invalid_request_method():
    # Prepare a GET request instead of POST
    request = RequestFactory().get('/delete_user/')
    
    # Call the view function
    response = delete_user(request)
    
    # Check if the response is as expected
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid request method"}