import json
from django.test import TestCase, Client
from django.urls import reverse
from HandymanHive.models import CustomWorker
from unittest.mock import patch

class GetWorkersTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('get_workers')
        self.worker1 = CustomWorker.objects.create(email='worker1@test.com', first_name='Worker', last_name='One', verified=True,age=20)

    def test_get_workers_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        workers_data = response.json()['workers']
        self.assertEqual(len(workers_data), 1)
        self.assertEqual(workers_data[0]['email'], self.worker1.email)

    def test_get_workers_invalid_method(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 400)



    @patch('django.db.models.Manager.all')
    def test_get_workers_exception(self, mock_all):
        mock_all.side_effect = Exception('Database error')  # This will cause `CustomWorker.objects.all()` to raise an exception
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 500)
