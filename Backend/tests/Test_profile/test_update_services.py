import json
from django.test import TestCase
from django.urls import reverse
from HandymanHive.models import WorkerDetails, Service
from HandymanHive.routes import update_services

class UpdateServicesTestCase(TestCase):
    def setUp(self):
        # Create a sample worker
        self.worker_email = "worker@example.com"
        self.worker = WorkerDetails.objects.create(email=self.worker_email)

        # Create some sample services
        self.service1 = Service.objects.create(name="Service A")
        self.service2 = Service.objects.create(name="Service B")

    def test_update_services_valid(self):
        # Test valid service update
        data = {
            "email": self.worker_email,
            "services": ["Service A", "Service B"]
        }
        response = self.client.post(reverse("update_service"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.services_offered.count(), 2)

    def test_update_services_invalid_email(self):
        # Test with invalid email
        data = {
            "email": "invalid@example.com",
            "services": ["Service A"]
        }
        response = self.client.post(reverse("update_service"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 500)

    def test_update_services_empty_services(self):
        # Test with empty services list
        data = {
            "email": self.worker_email,
            "services": []
        }
        response = self.client.post(reverse("update_service"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.services_offered.count(), 0)

    def test_update_services_duplicate_services(self):
        # Test with duplicate service names
        data = {
            "email": self.worker_email,
            "services": ["Service A", "Service A"]
        }
        response = self.client.post(reverse("update_service"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.worker.refresh_from_db()
        self.assertEqual(self.worker.services_offered.count(), 1)

    def test_update_services_missing_fields(self):
        # Test with missing fields
        data = {
            "services": ["Service A"]
        }
        response = self.client.post(reverse("update_service"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 500)

    def test_update_services_worker_not_available(self):
        # Test with unavailable worker
        self.worker.isAvailable = False
        self.worker.save()
        data = {
            "email": self.worker_email,
            "services": ["Service A"]
        }
        response = self.client.post(reverse("update_service"), json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200)
