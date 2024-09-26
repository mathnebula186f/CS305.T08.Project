import json
from datetime import timedelta
from django.utils import timezone
import pytest
from django.test import RequestFactory
from django.urls import reverse
from HandymanHive.routes.user_auth import verify_login_otp
from HandymanHive.models import CustomUser, CustomWorker

@pytest.fixture
def factory():
    return RequestFactory()

@pytest.fixture
def admin_list():
    return ["admin@example.com"]

@pytest.mark.django_db
def test_verify_login_otp_worker_valid(factory, admin_list):
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
        otp="123456",
        otp_valid_till=timezone.now() + timedelta(minutes=50),
    )
    request = factory.post(
        reverse("verify_login_otp"),
        data=json.dumps({"email": worker.email, "otp": "123456", "isWorker": "True", "notification_id": "test_id"}),
        content_type="application/json",
    )
    request.session = {"admin_list": admin_list}  # Pass admin_list in the session
    response = verify_login_otp(request)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data["message"] == "OTP verified successfully"
    assert data["isAdmin"] == "False"
    assert "token" in data

@pytest.mark.django_db
def test_verify_login_otp_user_valid(factory, admin_list):
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
        otp="123456",
        otp_valid_till=timezone.now() + timedelta(minutes=50),
    )
    request = factory.post(
        reverse("verify_login_otp"),
        data=json.dumps({"email": user.email, "otp": "123456", "isWorker": "False", "notification_id": "test_id"}),
        content_type="application/json",
    )
    request.session = {"admin_list": admin_list}  # Pass admin_list in the session
    response = verify_login_otp(request)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data["message"] == "OTP verified successfully"
    assert data["isAdmin"] == "False"
    assert "token" in data

@pytest.mark.django_db
def test_verify_login_otp_admin_user(factory, admin_list):
    user = CustomUser.objects.create(
        email="admin@example.com",
        phone_number="1234567890",
        first_name="Test",
        last_name="User",
        age=30,
        gender="Male",
        address="Test Address",
        city="Test City",
        state="Test State",
        zip_code="123456",
        otp="123456",
        otp_valid_till=timezone.now() + timedelta(minutes=50),
    )
    request = factory.post(
        reverse("verify_login_otp"),
        data=json.dumps({"email": user.email, "otp": "123456", "isWorker": "False", "notification_id": "test_id"}),
        content_type="application/json",
    )
    request.session = {"admin_list": admin_list}  # Pass admin_list in the session
    response = verify_login_otp(request)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data["message"] == "OTP verified successfully"
    assert "token" in data

@pytest.mark.django_db
def test_verify_login_otp_user_not_exists(factory, admin_list):
    request = factory.post(
        reverse("verify_login_otp"),
        data=json.dumps({"email": "nonexistent@example.com", "otp": "123456", "isWorker": "False", "notification_id": "test_id"}),
        content_type="application/json",
    )
    request.session = {"admin_list": admin_list}  # Pass admin_list in the session
    response = verify_login_otp(request)
    assert response.status_code == 404
    data = json.loads(response.content)
    assert data["error"] == "Invalid OTP"

@pytest.mark.django_db
def test_verify_login_otp_invalid_otp(factory, admin_list):
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
        otp="123456",
        otp_valid_till=timezone.now() + timedelta(minutes=50),
    )
    request = factory.post(
        reverse("verify_login_otp"),
        data=json.dumps({"email": worker.email, "otp": "invalid", "isWorker": "True", "notification_id": "test_id"}),
        content_type="application/json",
    )
    request.session = {"admin_list": admin_list}  # Pass admin_list in the session
    response = verify_login_otp(request)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data["error"] == "Invalid OTP"

@pytest.mark.django_db
def test_verify_login_otp_expired_otp(factory, admin_list):
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
        otp="123456",
        otp_valid_till=timezone.now() - timedelta(minutes=10),
    )
    request = factory.post(
        reverse("verify_login_otp"),
        data=json.dumps({"email": worker.email, "otp": "123456", "isWorker": "True", "notification_id": "test_id"}),
        content_type="application/json",
    )
    request.session = {"admin_list": admin_list}  # Pass admin_list in the session
    response = verify_login_otp(request)
    assert response.status_code == 500
    data = json.loads(response.content)
    assert data["error"] == "OTP expired"

def test_verify_login_otp_invalid_request_method(factory, admin_list):
    request = factory.get(reverse("verify_login_otp"))
    request.session = {"admin_list": admin_list}  # Pass admin_list in the session
    response = verify_login_otp(request)
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data["error"] == "Invalid request method"