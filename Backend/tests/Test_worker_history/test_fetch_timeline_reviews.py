from django.test import TestCase, Client
from django.urls import reverse
from HandymanHive.models import CustomUser, CustomWorker, Request, WorkHistory, WorkerDetails
import json
from unittest.mock import patch
from django.utils import timezone

class FetchTimelineDetailsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # self.url = reverse('get_worker_history')
        self.url = reverse('fetch_timeline_details')
        self.user = CustomUser.objects.create(email='user@test.com',age=30)
        self.worker = CustomWorker.objects.create(email='worker@test.com',age=20)
        self.service = 'Test Service'
        self.request_obj = Request.objects.create(user=self.user, worker=self.worker, service=self.service)

    def test_invalid_json(self):
        response = self.client.post(self.url, 'invalid_json', content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_missing_fields(self):
        data = {'user_email': 'user@test.com'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_nonexistent_user_or_worker(self):
        data = {'user_email': 'nonexistent@test.com', 'worker_email': 'worker@test.com', 'service': self.service}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_work(self):
        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': 'Nonexistent Service'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_successful_timeline_fetch(self):
        # Create a WorkHistory object with userdone=True and workerdone=True
        WorkHistory.objects.create(user=self.user, worker=self.worker, service=self.service, status='Done', userdone=True, workerdone=True)
        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['timeline_details']), 3)  # Work Started, User marked as Done, Work Completed

    @patch('HandymanHive.routes.profile.CustomUser.objects.get')
    def test_generic_exception(self, mock_get):
        mock_get.side_effect = Exception('Test exception')  # Mock an exception
        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)




    def test_successful_timeline_fetch_with_user_done(self):
        # Create a WorkHistory object with userdone=True
        work = WorkHistory.objects.create(user=self.user, worker=self.worker, service=self.service, status='In Progress', userdone=True)
        work.user_done_on = timezone.now()
        work.save()

        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['timeline_details']), 2)  # Work Started, User marked as Done

    def test_successful_timeline_fetch_with_worker_done(self):
        # Create a WorkHistory object with workerdone=True
        work = WorkHistory.objects.create(user=self.user, worker=self.worker, service=self.service, status='In Progress', workerdone=True)
        work.worker_done_on = timezone.now()
        work.save()

        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['timeline_details']), 2)  # Work Started, Worker marked as Done



class FetchReviewsTest(TestCase):
    # ... existing setup ...
    def setUp(self):
        self.client = Client()
        # self.url = reverse('get_worker_history')
        self.url = reverse('fetch_reviews')
        self.user = CustomUser.objects.create(email='user@test.com',age=30)
        self.worker = CustomWorker.objects.create(email='worker@test.com',age=20)
        self.service = 'Test Service'
        self.request_obj = Request.objects.create(user=self.user, worker=self.worker, service=self.service)


    def test_invalid_json(self):
        response = self.client.post(self.url, 'invalid_json', content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_missing_fields(self):
        data = {'user_email': 'user@test.com'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_nonexistent_worker_details(self):
        data = {'user_email': 'user@test.com', 'worker_email': 'nonexistent@test.com'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_successful_reviews_fetch(self):
        # Create a WorkerDetails object with a review
        WorkerDetails.objects.create(email='worker@test.com', customer_reviews=[{'user': 'Test User', 'rating': 5, 'service': 'Test Service', 'review': 'Great work!', 'time': '2022-01-01 00:00:00'}])

        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['reviews']), 1)

    # @patch('your_app.views.fetch_reviews.WorkerDetails.objects.get')
    @patch('HandymanHive.routes.profile.WorkerDetails.objects.get')
    def test_generic_exception(self, mock_get):
        mock_get.side_effect = Exception('Test exception')  # Mock an exception
        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

