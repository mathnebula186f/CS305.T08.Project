from django.test import TestCase, Client
from django.urls import reverse
from HandymanHive.models import CustomUser, CustomWorker, Request, WorkHistory, WorkerDetails
import json
from unittest.mock import patch

class UpdateUserWorksTest(TestCase):
    def setUp(self):
        self.client = Client()
        # self.url = reverse('get_worker_history')
        self.url = reverse('update_user_works')
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
        data = {'user_email': 'nonexistent@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Done'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_work(self):
        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': 'Nonexistent Service', 'status': 'Done'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_reject_work_not_in_progress(self):
        # Create a WorkHistory object with status='Done'
        WorkHistory.objects.create(user=self.user, worker=self.worker, service=self.service, status='Done')

        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Reject'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_done_work_not_in_progress(self):
        # Create a WorkHistory object with status='Done'
        WorkHistory.objects.create(user=self.user, worker=self.worker, service=self.service, status='Done')

        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Done'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_successful_work_rejection(self):
        # Create a WorkHistory object with status='In Progress'
        WorkHistory.objects.create(user=self.user, worker=self.worker, service=self.service, status='In Progress')

        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Reject'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(WorkHistory.objects.filter(user=self.user, worker=self.worker, service=self.service).exists())

    def test_successful_work_acceptance(self):
        # Create a WorkHistory object with status='In Progress'
        WorkHistory.objects.create(user=self.user, worker=self.worker, service=self.service, status='In Progress')

        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Done'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(WorkHistory.objects.filter(user=self.user, worker=self.worker, service=self.service, userdone=True).exists())


    @patch('HandymanHive.routes.profile.CustomUser.objects.get')
    def test_generic_exception(self, mock_get):
        mock_get.side_effect = Exception('Test exception')  # Mock an exception
        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Done'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)

    def test_successful_work_acceptance_with_worker_done(self):
        # Create a WorkHistory object with status='In Progress' and workerdone=True
        WorkHistory.objects.create(user=self.user, worker=self.worker, service=self.service, status='In Progress', workerdone=True)

        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Done', 'user_review': 'Great work!', 'user_rating': 5}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        work = WorkHistory.objects.get(user=self.user, worker=self.worker, service=self.service)
        self.assertTrue(work.userdone)
        self.assertEqual(work.status, 'Done')

    def test_successful_work_acceptance_with_review(self):
        # Create a WorkHistory object with status='In Progress'
        WorkHistory.objects.create(user=self.user, worker=self.worker, service=self.service, status='In Progress')

        # Create a WorkerDetails object for the worker
        WorkerDetails.objects.create(email='worker@test.com')

        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Done', 'user_review': 'Great work!', 'user_rating': 5}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        worker_details = WorkerDetails.objects.get(email='worker@test.com')
        self.assertEqual(len(worker_details.customer_reviews), 1)
        self.assertEqual(worker_details.customer_reviews[0]['review'], 'Great work!')
        self.assertEqual(worker_details.customer_reviews[0]['rating'], 5)


class UpdateWorkerWorksTest(TestCase):
    def setUp(self):
        self.client = Client()
        # self.url = reverse('get_worker_history')
        self.url = reverse('update_worker_works')
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
        data = {'user_email': 'nonexistent@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Done'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_nonexistent_work(self):
        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': 'Nonexistent Service', 'status': 'Done'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_reject_work_not_in_progress(self):
        # Create a WorkHistory object with status='Done'
        WorkHistory.objects.create(user=self.user, worker=self.worker, service=self.service, status='Done')

        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Reject'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_done_work_not_in_progress(self):
        # Create a WorkHistory object with status='Done'
        WorkHistory.objects.create(user=self.user, worker=self.worker, service=self.service, status='Done')

        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Done'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_successful_work_rejection(self):
        # Create a WorkHistory object with status='In Progress'
        WorkHistory.objects.create(user=self.user, worker=self.worker, service=self.service, status='In Progress')

        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Reject'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(WorkHistory.objects.filter(user=self.user, worker=self.worker, service=self.service).exists())

    def test_successful_work_acceptance(self):
        # Create a WorkHistory object with status='In Progress'
        WorkHistory.objects.create(user=self.user, worker=self.worker, service=self.service, status='In Progress')

        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Done'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        work = WorkHistory.objects.get(user=self.user, worker=self.worker, service=self.service)
        self.assertTrue(work.workerdone)

    @patch('HandymanHive.routes.profile.CustomUser.objects.get')
    def test_generic_exception(self, mock_get):
        mock_get.side_effect = Exception('Test exception')  # Mock an exception
        data = {'user_email': 'user@test.com', 'worker_email': 'worker@test.com', 'service': self.service, 'status': 'Done'}
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)
