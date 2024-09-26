import pytest
import json
from django.test import Client
from django.urls import reverse
from HandymanHive.models import AbstractUser, CustomWorker,  CustomUser
from django.contrib.auth.models import User
from django.test import TestCase
from unittest.mock import patch

@pytest.mark.django_db
class TestSignup(TestCase):

    def setUp(self):
        self.client = Client()
        self.signup_url = 'user_signup'

    def test_valid_signup(self):
        client = Client()
        valid_data = {
            "email": "jaiswalabhi0786@gmail.com",
            "isWorker": False,
        }
        response = client.post(reverse('user_signup'), json.dumps(valid_data), content_type='application/json')
        assert response.status_code == 200
        assert "OTP sent successfully" in response.json().get("message", "")

    def test_signup_worker_existing_email(self):
        CustomWorker.objects.create(email='test@example.com',age=20)
        response = self.client.post(reverse(self.signup_url), json.dumps({
            'email': 'test@example.com',
            'isWorker': 'True'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"error": "Email already exists"})

    
    def test_signup_user_existing_email(self):
        CustomUser.objects.create(email='test@example.com',age=20)
        response = self.client.post(reverse(self.signup_url), json.dumps({
            'email': 'test@example.com',
            'isWorker': 'False'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"error": "Email already exists"})

    def test_signup_existing_abstractuser(self):
        AbstractUser.objects.create(email='test@example.com')
        response = self.client.post(reverse(self.signup_url), json.dumps({
            'email': 'test@example.com',
            'isWorker': 'True'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "OTP sent successfully"})

    def test_signup_new_user(self):
        response = self.client.post(reverse(self.signup_url), json.dumps({
            'email': 'new@example.com',
            'isWorker': 'False'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "OTP sent successfully"})

    def test_invalid_request_method(self):
        response = self.client.get(reverse(self.signup_url))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid request method"})


    # @patch('path.to.your.send_otp_email')
    @patch('HandymanHive.routes.user_auth.send_otp_email')
    def test_signup_send_otp_exception(self, mock_send_otp_email):
        mock_send_otp_email.side_effect = Exception('Error sending OTP')
        response = self.client.post(reverse(self.signup_url), json.dumps({
            'email': 'new@example.com',
            'isWorker': 'False'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "Error sending OTP"})

    @patch('HandymanHive.routes.user_auth.send_otp_email')
    def test_signup_existing_abstractuser2(self, mock_send_otp_email):
        mock_send_otp_email.side_effect = Exception('Error sending OTP')
        AbstractUser.objects.create(email='test@example.com')
        response = self.client.post(reverse(self.signup_url), json.dumps({
            'email': 'test@example.com',
            'isWorker': 'True'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "Error sending OTP"})


    def test_duplicate_signup(self):
        client = Client()
        duplicate_data = {
            "email": "test@example.com",
            "isWorker": False,
        }
        response = client.post(reverse('user_signup'), json.dumps(duplicate_data), content_type='application/json')
        assert response.status_code == 200

    def test_invalid_email_signup(self):
        client = Client()
        invalid_data = {
            "email": "test",
            "isWorker": False,
        }
        response = client.post(reverse('user_signup'), json.dumps(invalid_data), content_type='application/json')
        assert response.status_code == 200

    def test_empty_email_signup(self):
        client = Client()
        invalid_data = {
            "email": "",
            "isWorker": False,
        }
        response = client.post(reverse('user_signup'), json.dumps(invalid_data), content_type='application/json')
        assert response.status_code == 200

