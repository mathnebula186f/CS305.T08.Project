from django.test import TestCase, Client
from django.urls import reverse
from HandymanHive.models import CustomUser, CustomWorker, Request, WorkHistory
import json
from unittest.mock import patch

class UpdateRequestTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('update_request')  
        self.user = CustomUser.objects.create(email='user@test.com',age=30)
        self.worker = CustomWorker.objects.create(email='worker@test.com',age=20)
        self.service = 'Test Service'
        self.request_obj = Request.objects.create(user=self.user, worker=self.worker, service=self.service)

    def test_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_invalid_json(self):
        response = self.client.post(self.url, 'invalid_json', content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_missing_fields(self):
        data = {'user_email': 'user@test.com'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_nonexistent_user_or_worker(self):
        data = {'user_email': 'nonexistent@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Accept'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_request_not_found(self):
        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': 'Nonexistent Service', 'status': 'Accept'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_successful_request_update(self):
        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Accept'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Request.objects.filter(user=self.user, worker=self.worker, service=self.service).exists())
        self.assertTrue(WorkHistory.objects.filter(user=self.user, worker=self.worker, service=self.service).exists())


    @patch('HandymanHive.routes.profile.CustomUser.objects.get')
    def test_generic_exception(self, mock_get):
        mock_get.side_effect = Exception('Test exception')  # Mock an exception
        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Accept'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)



from unittest.mock import patch

class GetUserRequestsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_user_requests')
        self.user = CustomUser.objects.create(email='user@test.com',age=30)
        self.worker = CustomWorker.objects.create(email='worker@test.com',age=20)
        self.service = 'Test Service'
        self.request_obj = Request.objects.create(user=self.user, worker=self.worker, service=self.service)

    def test_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_invalid_json(self):
        response = self.client.post(self.url, 'invalid_json', content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_missing_fields(self):
        data = {}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_nonexistent_worker(self):
        data = {'email': 'nonexistent@test.com'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_successful_request_fetch(self):
        data = {'email': 'worker@test.com'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['requests']), Request.objects.filter(worker=self.worker, status='Pending').count())


    @patch('HandymanHive.routes.profile.CustomWorker.objects.get')
    def test_generic_exception(self, mock_get):
        mock_get.side_effect = Exception('Test exception')  # Mock an exception
        data = {'email': 'worker@test.com'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)

