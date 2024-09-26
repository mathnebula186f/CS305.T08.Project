import json
from datetime import timedelta
from django.utils import timezone
import pytest
from django.test import RequestFactory
from django.urls import reverse
from HandymanHive.routes.user_auth import user_login
from HandymanHive.models import CustomUser, CustomWorker

@pytest.fixture
def factory():
    return RequestFactory()

@pytest.mark.django_db
def test_user_login_post_worker_exists(factory):
    worker = CustomWorker.objects.create(
        email="test@example.com",
        phone_number="1234567890",
        first_name="Test",
        last_name="User",
        age=30,
        gender="Male",
        address="Test Address",
        city="Test City",
        state="Test State",
        zip_code="123456",
    )
    request = factory.post(
        reverse("user_login"),
        data=json.dumps({"email": worker.email, "isWorker": "True"}),
        content_type="application/json",
    )
    response = user_login(request)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data["message"] == "OTP sent successfully"
    worker.refresh_from_db()
    assert worker.otp is not None
    assert worker.otp_valid_till > timezone.now()

@pytest.mark.django_db
def test_user_login_post_user_exists(factory):
    user = CustomUser.objects.create(
        email="test@example.com",
        phone_number="1234567890",
        first_name="Test",
        last_name="User",
        age=30,
        gender="Male",
        address="Test Address",
        city="Test City",
        state="Test State",
        zip_code="123456",
    )
    request = factory.post(
        reverse("user_login"),
        data=json.dumps({"email": user.email, "isWorker": "False"}),
        content_type="application/json",
    )
    response = user_login(request)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data["message"] == "OTP sent successfully"
    user.refresh_from_db()
    assert user.otp is not None
    assert user.otp_valid_till > timezone.now()

@pytest.mark.django_db
def test_user_login_post_user_not_exists(factory):
    request = factory.post(
        reverse("user_login"),
        data=json.dumps({"email": "nonexistent@example.com", "isWorker": "False"}),
        content_type="application/json",
    )
    response = user_login(request)
    assert response.status_code == 404
    data = json.loads(response.content)
    assert data["error"] == "User with this email does not exist."

def test_user_login_invalid_request_method(factory):
    request = factory.get(reverse("user_login"))
    response = user_login(request)
    assert response.status_code == 400
    data = json.loads(response.content)
    assert data["error"] == "Invalid request method"

def test_user_login_exception(factory, monkeypatch):
    def mock_generate_otp():
        raise Exception("Test exception")

    monkeypatch.setattr("HandymanHive.routes.user_auth.generate_otp", mock_generate_otp)

    request = factory.post(
        reverse("user_login"),
        data=json.dumps({"email": "test@example.com", "isWorker": "False"}),
        content_type="application/json",
    )
    response = user_login(request)
    assert response.status_code == 500
    data = json.loads(response.content)
    assert data["error"] == "Error sending OTP"