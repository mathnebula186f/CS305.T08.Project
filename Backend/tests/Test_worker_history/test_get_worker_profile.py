import json
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from HandymanHive.models import CustomUser, CustomWorker, WorkerDetails, Certification

class GetWorkerProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_worker_profile')  # replace with your url name
        self.worker = CustomWorker.objects.create(email='worker@test.com',age=20)
        self.worker_details = WorkerDetails.objects.create(email=self.worker.email)

    def test_get_worker_profile_success(self):
        data = {
            'email': 'user@test.com',
            'worker_email': self.worker.email
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "first_name": self.worker.first_name,
            "last_name": self.worker.last_name,
            "email": self.worker.email,
            "phone_number": self.worker.phone_number,
            "age": self.worker.age,
            "years_of_exp": self.worker_details.years_of_experience,
            "services": [],
            "certification": [],
            "verified": self.worker.verified,
            "address": self.worker.address,
            "state": self.worker.state,
            "latitude": self.worker_details.liveLatitude,
            "longitude": self.worker_details.liveLongitude,
        })

    def test_get_worker_profile_invalid_json(self):
        response = self.client.post(self.url, 'invalid json', content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_get_worker_profile_worker_not_exist(self):
        data = {
            'email': 'user@test.com',
            'worker_email': 'not_exist@test.com'
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_get_worker_profile_method_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    # @patch('your_app.views.CustomWorker.objects.get')
    @patch('HandymanHive.routes.profile.CustomWorker.objects.get')
    def test_get_worker_profile_generic_exception(self, mock_get):
        mock_get.side_effect = Exception('Test exception')

        data = {
            'email': 'user@test.com',
            'worker_email': self.worker.email
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)
