from django.test import TestCase
from django.test import Client
from django.urls import reverse
from HandymanHive.models import CustomWorker, Service, WorkerDetails
import json
import pytest


class InsertWorkerTestCase(TestCase):
    def setUp(self):
        # Initialize the test client
        self.client = Client()

    @pytest.mark.skip(reason="Skipping this test case")
    def test_insert_worker_success(self):
        # Test successful insertion of worker
        url = reverse("insert_worker")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Worker added successfully')
        self.assertTrue(CustomWorker.objects.exists())

    @pytest.mark.skip(reason="Skipping this test case")
    def test_worker_insertion_with_existing_email(self):
        # Insert a worker with a specific email
        existing_email = "john.smith@gmail.com"
        CustomWorker.objects.create(email=existing_email,age=20)

        # Attempt to insert another worker with the same email
        url = reverse("insert_worker")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], "Worker added successfully")
        self.assertEqual(CustomWorker.objects.filter(email=existing_email).count(), 1)


    @pytest.mark.skip(reason="Skipping this test case")
    def test_insert_worker_already_exists(self):
        # Create a worker with the same email
        CustomWorker.objects.create(email='test@gmail.com',age=20)
        # Test inserting a worker with the same email
        url = reverse("insert_worker")
        response = self.client.post(url)
        # response = self.client.post('/insert_worker/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Worker added successfully')
        self.assertEqual(CustomWorker.objects.count(), 553)
