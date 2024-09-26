from django.test import TestCase, Client
from django.urls import reverse
from HandymanHive.models import CustomUser, CustomWorker, Request, WorkHistory
import json
from unittest.mock import patch

class GetUserHistoryTest(TestCase):
    def setUp(self):
        self.client = Client()
        # self.url = reverse('update_request')  
        self.url = reverse('get_user_history')
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

    def test_nonexistent_user(self):
        data = {'email': 'nonexistent@test.com'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_successful_history_fetch(self):
        data = {'email': 'user@test.com'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['done_works']), WorkHistory.objects.filter(user=self.user, status='Done').count())
        self.assertEqual(len(response.json()['progress_works']), WorkHistory.objects.filter(user=self.user, status='In Progress').count())

    
    @patch('HandymanHive.routes.profile.CustomUser.objects.get')
    def test_generic_exception(self, mock_get):
        mock_get.side_effect = Exception('Test exception')  # Mock an exception
        data = {'email': 'user@test.com'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_successful_history_fetch_with_user_done(self):
        # Create a WorkHistory object with userdone=True
        WorkHistory.objects.create(user=self.user, worker=self.worker, service='Test Service', status='In Progress', userdone=True)

        data = {'email': 'user@test.com'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['done_works']), WorkHistory.objects.filter(user=self.user, status='Done').count())
        self.assertEqual(len(response.json()['progress_works']), WorkHistory.objects.filter(user=self.user, status='In Progress').count())

        # Check that the status of the work in progress is 'Done'
        for work in response.json()['progress_works']:
            if work['service'] == 'Test Service':
                self.assertEqual(work['status'], 'Done')
