from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from HandymanHive.models import AbstractUser, CustomUser, CustomWorker
from datetime import timedelta
from django.utils import timezone
import json
import jwt
from django.test import Client


class VerifyOtpTest(TestCase):
    def setUp(self):
        self.verify_otp_url = reverse('verify_otp')
        self.client = Client()
        self.user_details = {
            "phone_number": "1234567890",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "age": "30",
            "gender": "Male",
            "address": "123 Test St",
            "city": "Test City",
            "state": "Test State",
            "zip_code": "12345"
        }
        self.user = AbstractUser.objects.create(
            email='test@example.com', 
            otp='123456', 
            otp_valid_till=timezone.now() + timedelta(minutes=15),
            user_details=json.dumps(self.user_details),
            is_worker='True'
        )

    def test_verify_otp_existing_worker(self):
        CustomWorker.objects.create(email='test@example.com',age=20)
        response = self.client.post(self.verify_otp_url, json.dumps({
            'email': 'test@example.com',
            'otp': '123456',
            'isWorker': 'True',
            'notification_id': '123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"error": "Email already exists"})

    def test_verify_otp_existing_user(self):
        CustomUser.objects.create(email='test@example.com',age=20)
        response = self.client.post(self.verify_otp_url, json.dumps({
            'email': 'test@example.com',
            'otp': '123456',
            'isWorker': 'False',
            'notification_id': '123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json(), {"error": "Email already exists"})

    

    # @patch('jwt.encode')

    @patch('jwt.encode')
    def test_verify_otp_existing_abstractuser(self, mock_jwt_encode):
        mock_jwt_encode.return_value = 'test_token'
        response = self.client.post(self.verify_otp_url, json.dumps({
            'email': 'test@example.com',
            'otp': '123456',
            'isWorker': 'True',
            'notification_id': '123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "OTP verified successfully", "isAdmin": "False"})

    

    def test_verify_otp_invalid(self):
        response = self.client.post(self.verify_otp_url, json.dumps({
            'email': 'test@example.com',
            'otp': '654321',
            'isWorker': 'True',
            'notification_id': '123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 300)
        self.assertEqual(response.json(), {"error": "Invalid OTP"})

    @patch('jwt.encode')
    def test_verify_otp_exception(self, mock_jwt_encode):
        mock_jwt_encode.side_effect = Exception('Error Verifying OTP')
        response = self.client.post(self.verify_otp_url, json.dumps({
            'email': 'test@example.com',
            'otp': '123456',
            'isWorker': 'True',
            'notification_id': '123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"error": "Error Verifying OTP"})

    def test_invalid_request_method(self):
        response = self.client.get(self.verify_otp_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"error": "Invalid request method"})

    def test_verify_otp_expired(self):
        self.user.otp_valid_till = timezone.now() - timedelta(minutes=15)
        self.user.save()
        response = self.client.post(self.verify_otp_url, json.dumps({
            'email': 'test@example.com',
            'otp': '123456',
            'isWorker': 'True',
            'notification_id': '123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 300)
        self.assertEqual(response.json(), {"error": "OTP expired"})

    def test_user_not_found(self):
        response = self.client.post(self.verify_otp_url, json.dumps({
            'email': 'test@example.com',
            'otp': '123456',
            'isWorker': 'False',
            'notification_id': '123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"message": "User not found"})

