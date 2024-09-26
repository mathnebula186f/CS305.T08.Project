from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
import json
from HandymanHive.models import Service, WorkerDetails, CustomWorker
from HandymanHive.routes.recommendation import get_workers_on_price

class GetWorkersOnPriceTestCase(TestCase):
    def setUp(self):
        # self.client = Client()
        self.factory = RequestFactory()
        # Create test data
        self.service = Service.objects.create(name="Test Service")
        self.worker = CustomWorker.objects.create(email="test@example.com", first_name="John", last_name="Doe",age=30)
        self.worker_details = WorkerDetails.objects.create(
            email=self.worker,
            isAvailable=True,
            min_price=10,
            max_price=20
        )
        self.worker_details.services_offered.add(self.service)

    def test_get_workers_success(self):
        # Test successful retrieval of workers based on service name
        data = {"service_name": "Test Service"}
        request = self.factory.get('/get_workers_on_price/', data, content_type='application/json')
        response = get_workers_on_price(request)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['top_five_custom_workers']), 1)

    def test_service_not_found(self):
        # Test handling of invalid service name
        url = reverse("get_workers_on_price")
        data = {"service_name": "Invalid Service"}
        response = self.client.get(url, (data), content_type="application/json")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["error"], "Service not found")

    def test_invalid_request_method(self):
        # Test handling of invalid request method
        url = reverse("get_workers_on_price")
        response = self.client.post(url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Invalid request method")

    def test_exception_handling(self):
        # Test handling of exceptions
        # Simulate exception by deleting the worker details
        self.worker_details.delete()
        url = reverse("get_workers_on_price")
        data = {"service_name": "Test Service"}
        response = self.client.get(url, (data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(len(data['top_five_custom_workers']), 0)
