import json
import jwt
from django.test import TestCase, Client
from django.urls import reverse
from HandymanHive.models import CustomUser, CustomWorker
class GetUserDataTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_user_data')  # replace with your actual url name
        self.user = CustomUser.objects.create(email='testuser@test.com',age=30)
        self.worker = CustomWorker.objects.create(email='testworker@test.com',age=20)

    def test_get_user_data_post(self):
        data = {
            "email": self.user.email,
            "isWorker": "False"
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['worker_details']['email'], self.user.email)

    def test_get_user_data_worker_post(self):
        data = {
            "email": self.worker.email,
            "isWorker": "True"
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['worker_details']['email'], self.worker.email)

    def test_get_user_data_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_get_user_data_user_not_found(self):
        data = {
            "email": 'nonexistent@test.com',
            "isWorker": "False"
        } 
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_get_user_data_invalid_token(self):
        data = {
            "email": self.user.email,
            "isWorker": "False"
        }
        with self.settings(SECRET_KEY='wrong_secret_key'):
            response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_user_data_expired_token(self):
        data = {
            "email": self.user.email,
            "isWorker": "False"
        }
        with self.settings(JWT_EXPIRATION_TIME=-1):
            response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
