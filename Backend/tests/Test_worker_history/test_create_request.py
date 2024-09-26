import json
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from HandymanHive.models import CustomUser, CustomWorker, Request

class CreateRequestTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create_request')  
        self.user = CustomUser.objects.create(email='user@test.com',age=20)
        self.worker = CustomWorker.objects.create(email='worker@test.com',age=20)

    def test_create_request_success(self):
        with patch('HandymanHive.routes.send_notfication') as mock_send:
            data = {
                'user_email': self.user.email,
                'worker_email': self.worker.email,
                'service': 'Test Service'
            }
            response = self.client.post(self.url, json.dumps(data), content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {'status': 'success', 'message': 'Request created successfully'})

    def test_create_request_invalid_json(self):
        response = self.client.post(self.url, 'invalid json', content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_request_missing_fields(self):
        data = {'user_email': self.user.email}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_create_request_user_not_exist(self):
        data = {
            'user_email': 'not_exist@test.com',
            'worker_email': self.worker.email,
            'service': 'Test Service'
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_create_request_worker_not_exist(self):
        data = {
            'user_email': self.user.email,
            'worker_email': 'not_exist@test.com',
            'service': 'Test Service'
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_create_request_method_not_allowed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)


    # @patch('your_app.views.CustomUser.objects.get')
    @patch('HandymanHive.routes.profile.CustomUser.objects.get')
    def test_create_request_generic_exception(self, mock_get):
        mock_get.side_effect = Exception('Test exception')

        data = {
            'user_email': self.user.email,
            'worker_email': self.worker.email,
            'service': 'Test Service'
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"status": "error", "message": "Error creating request"})
