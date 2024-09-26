import json
from django.test import TestCase, Client
from django.urls import reverse
from HandymanHive.models import CustomWorker, Certification

from unittest.mock import patch

class WorkerVerificationStatusTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('worker_verification_status')  # replace with your actual url name
        self.worker = CustomWorker.objects.create(email='worker@test.com', age=30)
        self.cert1 = Certification.objects.create(worker_email=self.worker.email, status='approved')
        self.cert2 = Certification.objects.create(worker_email=self.worker.email, status='pending')

    def test_worker_verification_status_post(self):
        data = {
            "email": self.worker.email,
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['verification_ratio'], 0.5)

    def test_worker_verification_status_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 400)

    def test_worker_verification_status_exception(self):
        data = {
            "email": 'nonexistent@test.com',
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)

    @patch('django.db.models.QuerySet.filter')
    def test_worker_verification_status_exception(self, mock_filter):
        mock_filter.side_effect = Exception('Database error')  # This will cause `Certification.objects.filter()` to raise an exception
        data = {
            "email": self.worker.email,
        }
        response = self.client.post(self.url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 500)
